import os
import hashlib
import logging

import pdfplumber
from supabase import create_client

# -------------------------------------------------
# Supabase client
# -------------------------------------------------

def get_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Supabase URL and Key must be set in environment variables.")
    return create_client(url, key)


# -------------------------------------------------
# Logging
# -------------------------------------------------

def setup_logger(name: str = "permit-crawler"):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    return logging.getLogger(name)


# -------------------------------------------------
# PDF utilities
# -------------------------------------------------

def extract_text_from_pdf(path: str) -> str:
    """Extracts all text from a PDF file."""
    try:
        with pdfplumber.open(path) as pdf:
            return " ".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        return f"[ERROR extracting text: {e}]"


def pdf_hash(content: bytes) -> str:
    """Return a SHA256 hash of a PDF file's content."""
    return hashlib.sha256(content).hexdigest()


# -------------------------------------------------
# Confidence scoring
# -------------------------------------------------

KEYWORDS = [
    "permit", "application", "building", "electrical", "plumbing",
    "hvac", "pool", "remodel", "roof", "deck"
]


def score_text_relevance(text: str) -> float:
    """Simple keyword scoring for relevance."""
    if not text:
        return 0.0
    hits = sum(1 for kw in KEYWORDS if kw.lower() in text.lower())
    return hits / len(KEYWORDS)


if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Testing utils module...")
    sb = get_supabase_client()
    logger.info("Supabase client initialized: %s", sb)}
