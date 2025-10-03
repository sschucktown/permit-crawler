import requests
from bs4 import BeautifulSoup
import re

# TODO: replace this with Google Custom Search API for more reliability
SEARCH_URL = "https://www.google.com/search?q={query}"  # placeholder only

KEYWORDS = [
    "permit", "permits", "building", "planning", "pdf",
    "application", "portal", "forms"
]


def google_search(query: str, max_results: int = 10) -> list[str]:
    """
    Very naive search placeholder.
    In production, replace with Google Custom Search API (CSE).
    """
    url = SEARCH_URL.format(query=requests.utils.quote(query))
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http") and ".google." not in href:
            links.append(href)
    return links[:max_results]


def filter_permit_urls(urls: list[str]) -> list[str]:
    filtered = []
    for url in urls:
        # must be .gov or .us
        if not (".gov" in url or url.endswith(".us")):
            continue
        # must contain keywords
        if any(re.search(k, url, re.IGNORECASE) for k in KEYWORDS):
            filtered.append(url)
    return filtered


def discover_urls(jurisdiction_name: str) -> list[str]:
    """
    Run discovery search for a jurisdiction to find permit-related URLs.
    """
    query = f"{jurisdiction_name} building permits site:.gov"
    raw_results = google_search(query)
    return filter_permit_urls(raw_results)


if __name__ == "__main__":
    # Example test
    test_jurisdiction = "Charleston County SC"
    results = discover_urls(test_jurisdiction)
    print(f"Discovered URLs for {test_jurisdiction}:\n", results)
