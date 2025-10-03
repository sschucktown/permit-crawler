from typing import List, Optional
import requests
from bs4 import BeautifulSoup

class BaseAdapter:
    """Abstract base for vendor-specific permit portal adapters."""

    VENDOR_NAME = "base"

    def __init__(self, start_url: str):
        self.start_url = start_url
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "PermitCrawler/1.0"})

    @classmethod
    def detect(cls, html: str, url: str) -> bool:
        """Return True if this adapter should handle the given HTML/URL."""
        raise NotImplementedError

    def fetch(self) -> str:
        resp = self.session.get(self.start_url, timeout=30)
        resp.raise_for_status()
        return resp.text

    def fetch_forms(self) -> List[str]:
        """Return a list of form URLs (PDF or HTML) discovered in the portal."""
        raise NotImplementedError

    @staticmethod
    def is_pdf_link(href: Optional[str]) -> bool:
        return bool(href and href.lower().endswith(".pdf"))

    @staticmethod
    def soup(html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")
