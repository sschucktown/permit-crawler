import re
from typing import List
from adapters.base import BaseAdapter
import requests

CIVICPLUS_SIGNATURES = [
    r"civicplus\.com",
    r"civicclerk",
    r"civicweb",
    r"modules\.\.\.?/documentcenter",
    r"SiteID=",
]

class CivicPlusAdapter(BaseAdapter):
    VENDOR_NAME = "civicplus"

    @classmethod
    def detect(cls, html: str, url: str) -> bool:
        hay = (html or "") + " " + (url or "")
        return any(re.search(sig, hay, re.IGNORECASE) for sig in CIVICPLUS_SIGNATURES)

    def fetch_forms(self) -> List[str]:
        html = self.fetch()
        soup = self.soup(html)
        forms: List[str] = []
        # typical CivicPlus DocumentCenter links
        for a in soup.select('a[href]'):
            href = a.get('href')
            if self.is_pdf_link(href):
                forms.append(requests.compat.urljoin(self.start_url, href))
        return list(dict.fromkeys(forms))
