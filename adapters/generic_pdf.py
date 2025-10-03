from typing import List
from urllib.parse import urljoin
from adapters_base import BaseAdapter

class GenericPDFAdapter(BaseAdapter):
    VENDOR_NAME = "generic_pdf"

    @classmethod
    def detect(cls, html: str, url: str) -> bool:
        # Always safe to use as fallback
        return True

    def fetch_forms(self) -> List[str]:
        html = self.fetch()
        soup = self.soup(html)
        forms: List[str] = []
        for a in soup.select('a[href]'):
            href = a.get('href')
            if self.is_pdf_link(href):
                forms.append(urljoin(self.start_url, href))
        # If no PDFs found, return page itself for manual review
        return list(dict.fromkeys(forms or [self.start_url]))
