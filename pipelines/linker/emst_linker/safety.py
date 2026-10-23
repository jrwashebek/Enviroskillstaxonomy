"""Mandatory pre-link stages (ADR-0019 §7; ADR-0012; ADR-0007 §D).

1. PII stripping: e-mail addresses, phone numbers, URLs with query strings and "Contact: <Name>" style lines are
   replaced with placeholders before any text is indexed, linked, logged or stored.
2. Tribal quarantine: items whose source is a Tribal employer, or whose text mentions Tribal governments,
   Indigenous knowledge, treaty rights or government-to-government relations, are set aside unprocessed. They are
   counted, never linked, never sent to an LLM stage, and released only under the Tribal Council's protocol.
3. Untrusted input: text is data, never instructions. Linking is deterministic retrieval here; any later LLM stage
   must wrap text in delimiters and verify evidence spans as substrings (``verify_span``).
"""
from __future__ import annotations

import re

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b")
URLQ = re.compile(r"https?://\S+\?\S+")
CONTACT = re.compile(r"(?im)^\s*(?:contact|point of contact|poc|hiring manager|supervisor)\s*[:\-].*$")
TRIBAL = re.compile(r"(?i)\b(tribe|tribal|tribes|indigenous|native american|alaska native|first nations?|treaty|"
                    r"government-to-government|traditional ecological knowledge|tek\b|thpo|bureau of indian affairs)")


def strip_pii(text: str) -> tuple[str, int]:
    n = 0
    for rx, ph in ((EMAIL, "[email]"), (PHONE, "[phone]"), (URLQ, "[url]"), (CONTACT, "[contact line removed]")):
        text, k = rx.subn(ph, text)
        n += k
    return text, n


def quarantine(text: str, source_employer_type: str | None = None) -> bool:
    if (source_employer_type or "").lower() == "tribal":
        return True
    return bool(TRIBAL.search(text or ""))


def verify_span(span: str, text: str) -> bool:
    """An LLM-proposed evidence span is accepted only if it occurs verbatim in the input (ADR-0019 §4)."""
    return bool(span) and span in text
