from supabase import create_client
import requests, time

# Supabase init
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

def get_pending_jobs(limit=10):
    return supabase.table("crawl_queue")\
        .select("*")\
        .eq("status", "pending")\
        .limit(limit).execute().data

def update_job_status(job_id, status, notes=None):
    supabase.table("crawl_queue").update({
        "status": status,
        "last_checked": "now()",
        "notes": notes
    }).eq("id", job_id).execute()

def save_forms(jurisdiction_id, urls):
    supabase.table("jurisdictions").update({
        "forms_url": urls[0] if urls else None
    }).eq("id", jurisdiction_id).execute()

def run_job(job):
    try:
        if job["crawl_type"] == "portal":
            urls = crawl_portal(job["url"])  # adapter logic
        elif job["crawl_type"] == "pdf":
            urls = find_pdfs(job["url"])
        elif job["crawl_type"] == "discovery":
            urls = discover_urls(job["jurisdiction_id"])
        else:
            urls = []

        save_forms(job["jurisdiction_id"], urls)
        update_job_status(job["id"], "done", f"Found {len(urls)} forms")
    except Exception as e:
        update_job_status(job["id"], "failed", str(e))

if __name__ == "__main__":
    jobs = get_pending_jobs()
    for job in jobs:
        update_job_status(job["id"], "in_progress")
        run_job(job)
        time.sleep(2)   # politeness delay
