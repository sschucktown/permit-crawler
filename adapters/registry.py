from typing import List, Type
from adapters_base import BaseAdapter
from adapters_accela import AccelaAdapter
from adapters_civicplus import CivicPlusAdapter
from adapters_tyler import TylerAdapter
from adapters_cloudpermit import CloudpermitAdapter
from adapters_generic_pdf import GenericPDFAdapter

# Detection order matters: vendor-specific before generic
REGISTERED_ADAPTERS: List[Type[BaseAdapter]] = [
    AccelaAdapter,
    CivicPlusAdapter,
    TylerAdapter,
    CloudpermitAdapter,
    GenericPDFAdapter,
]


def detect_adapter(url: str, html: str) -> BaseAdapter:
    for adapter_cls in REGISTERED_ADAPTERS:
        try:
            if adapter_cls.detect(html, url):
                return adapter_cls(url)
        except Exception:
            continue
    # Fallback
    return GenericPDFAdapter(url)
