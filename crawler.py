import os
import requests
from supabase import create_client

from adapters.registry import detect_adapter
from utils import setup_logger, get_supabase_client

logger = setup_logger()


def get_pending_jobs(supabase, limit=5):
    """Fetch pending crawl jobs from Supabase crawl_queue."""
    result = supabase.table("crawl_queue") \
        .select("*") \
        .eq("status", "pending") \
        .limit(limit) \
        .execute()
    return result.data or []


def update_job_status(supabase, job_id, status, notes=None):
    """Update crawl job status in Supabase."""
    supabase.table("crawl_queue").update({
        "status": status,
        "last_checked": "now()",
        "notes": notes
    }).eq("id", job_id).execute()


def update_jurisdiction_forms(supabase, jurisdiction_id, forms):
    """Save discovered form URLs into jurisdictions table."""
    if not forms:
        return
    supabase.table("jurisdictions").update({
        "forms_url": forms[0]  # TODO: support multi-form later
    }).eq("id", jurisdiction_id).execute()


def run_job(supabase, job):
    """Run a single crawl job using the adapter registry."""
    job_id = job["id"]
    jurisdiction_id = job["jurisdiction_id"]
    url = job.get("url")

    try:
        # fetch HTML
        logger.info(f"Fetching {url} for job {job_id}")
        resp = requests.get(url, headers={"User-Agent": "PermitCrawler/1.0"}, timeout=30)
        resp.raise_for_status()
        html = resp.text

        # detect which adapter to use
        adapter = detect_adapter(url, html)
        logger.info(f"Using adapter: {adapter.VENDOR_NAME}")

        # fetch forms
        forms = adapter.fetch_forms()
        logger.info(f"Discovered {len(forms)} forms")

        # save results
        update_jurisdiction_forms(supabase, jurisdiction_id, forms)
        update_job_status(supabase, job_id, "done", f"Found {len(forms)} forms")

    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        update_job_status(supabase, job_id, "failed", str(e))


if __name__ == "__main__":
    supabase = get_supabase_client()
    jobs = get_pending_jobs(supabase)

    if not jobs:
        logger.info("No pending jobs.")
    else:
        for job in jobs:
            update_job_status(supabase, job["id"], "in_progress")
            run_job(supabase, job)
