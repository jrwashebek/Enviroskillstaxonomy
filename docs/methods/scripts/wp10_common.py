"""Shared helpers for the WP-10 change-signal and exposure seed (EMST v2, Phase 4).

Owner: A9 LM (with FS). Records follow docs/standard/SPEC.md sections 4, 5.12, 5.14-5.16 and ADR-0028.
Fields that SPEC does not yet define but that the ADR-0028 evidence rule needs are listed in
PROPOSED_FIELDS and requested in docs/decisions/change_requests/CR-LM-001.md.

Deterministic: fixed timestamps, sorted output, no randomness, no network.
"""
import hashlib
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
GENERATED_AT = "2026-10-23T12:00:00Z"
AS_OF = "2026-10-23"
TOOL_VERSION = "docs/methods/scripts/build_wp10.py@0.1.0"
PROMPT_VERSION = "PHASE4-WP10-A9-LM@2026-10-23"
AGENTS = ["emstagent:A9-LM@claude-opus-5-5", "emstagent:wp10-builder@0.1.0"]

# Re-check dates (WP-15 discipline): pending/contested facts before rc.1; settled facts at +6 or +12 months.
RECHECK_PENDING = "2026-12-15"
RECHECK_SETTLED = "2027-04-23"
RECHECK_HISTORIC = "2027-10-23"
WATCH_REVIEW_BY = "2027-10-23"  # ADR-0015: watch items review at +12 months

# Fields used here that SPEC 5.14 / 5.12 does not define (CR-LM-001, CR-LM-002).
PROPOSED_FIELDS = {
    "ChangeSignal": ["signalStatus", "signalFamily", "independenceKey", "impact", "scenarioSignposts"],
    "ExposureAssessment": ["targetType", "targetId", "crosswalkPath", "crosswalkMinMatchType"],
}

SIGNAL_FAMILIES = [
    "capability", "observed-use", "deployment", "postings-pds", "headcount",
    "plan-requirements", "worker-report", "policy", "projection",
]


def provenance(sources, evidence_label="E", method="llm-assisted", confidence=None, note_adr="ADR-0028"):
    p = {
        "method": method,
        "agent": AGENTS,
        "generatedAt": GENERATED_AT,
        "sources": sorted(set(sources)),
        "evidenceLabel": evidence_label,
        "reviewStatus": "unreviewed",
        "toolVersion": TOOL_VERSION,
        "promptVersion": PROMPT_VERSION,
        "adr": note_adr,
    }
    if confidence is not None:
        p["confidence"] = confidence
    if evidence_label == "E" and not sources:
        raise ValueError("E label requires sources")
    return p


def base(rec_id, rec_type, label, definition=None, editorial_note=None, notation=None, held=False):
    r = {
        "id": rec_id,
        "type": rec_type,
        "prefLabel": {"en": label},
        "layer": "L5",
        "module": "core",
        "status": "draft",
        "license": "CC0-1.0",
        "sensitivity": "public",
    }
    if definition:
        r["definition"] = {"en": definition}
    if editorial_note:
        r["editorialNote"] = {"en": editorial_note}
    if notation:
        r["notation"] = notation
    if held:
        # ADR-0007 / SPEC 16.1: Tribal hold. Excluded from every release artifact by CI.
        r["sensitivity"] = "restricted-governed"
        r["indigenousDataFlag"] = True
        r["approvalStatus"] = "pending-tribal-review"
        r["aiUsePermitted"] = False
    return r


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_jsonl(relpath, records):
    path = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    records = sorted(records, key=lambda r: r["id"])
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def slug(s):
    out = []
    for ch in s.lower():
        out.append(ch if ch.isalnum() else "-")
    t = "".join(out)
    while "--" in t:
        t = t.replace("--", "-")
    return t.strip("-")
