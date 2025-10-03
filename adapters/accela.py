import re
from typing import List
from adapters_base import BaseAdapter

ACCELA_SIGNATURES = [
    r"/CitizenAccess/",
    r"/citizenaccess/",
    r"Accela",
]

class AccelaAdapter(BaseAdapter):
    VENDOR_NAME = "accela"

    @classmethod
    def detect(cls, html: str, url: str) -> bool:
        hay = (html or "") + " " + (url or "")
        return any(re.search(sig, hay, re.IGNORECASE) for sig in ACCELA_SIGNATURES)

    def fetch_forms(self) -> List[str]:
        html = self.fetch()
        soup = self.soup(html)
        forms: List[str] = []
        for a in soup.select('a[href]'):
            href = a.get('href')
            if self.is_pdf_link(href):
                forms.append(requests.compat.urljoin(self.start_url, href))
        # Accela portals often hide forms behind search; return landing for manual follow-up
        if not forms:
            forms.append(self.start_url)
        return list(dict.fromkeys(forms))
