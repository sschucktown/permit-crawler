import re
from typing import List
from adapters_base import BaseAdapter
import requests

TYLER_SIGNATURES = [
    r"tylertech",
    r"energov",
    r"etrakit",
    r"css\.tylerapp",
]

class TylerAdapter(BaseAdapter):
    VENDOR_NAME = "tyler"

    @classmethod
    def detect(cls, html: str, url: str) -> bool:
        hay = (html or "") + " " + (url or "")
        return any(re.search(sig, hay, re.IGNORECASE) for sig in TYLER_SIGNATURES)

    def fetch_forms(self) -> List[str]:
        html = self.fetch()
        soup = self.soup(html)
        forms: List[str] = []
        for a in soup.select('a[href]'):
            href = a.get('href')
            if self.is_pdf_link(href):
                forms.append(requests.compat.urljoin(self.start_url, href))
        # EnerGov/ETRAKiT often require auth; return portal URL if PDFs not public
        if not forms:
            forms.append(self.start_url)
        return list(dict.fromkeys(forms))
