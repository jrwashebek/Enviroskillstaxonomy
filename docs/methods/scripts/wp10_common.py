"""Shared helpers for the WP-10 change-signal and exposure seed (EMST v2, Phase 4).

Owner: A9 LM (with FS). Records follow docs/standard/SPEC.md (s4, s5.12, s5.14-5.16), ADR-0028 and DE's
schema/emst.schema.json + docs/standard/AUTHORING_GUIDE.md (layout, field names, AgentId and SourceId patterns).

Interim encodings (until CR-LM-001 is decided): the ADR-0028 evidence rule needs per-signal attributes the schema
does not yet type (signal family, independence key, impact, registered deployment, signposts informed). They are
carried as `notation` entries with schemes prefixed `EMST-` so records validate today and migrate mechanically.

Deterministic: fixed timestamps, sorted output, no randomness, no network.
"""
import hashlib
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
GENERATED_AT = "2026-10-23T12:00:00Z"
AS_OF = "2026-10-23"
TOOL_VERSION = "docs/methods/scripts/build_wp10.py@0.2.0"
PROMPT_VERSION = "PHASE4-WP10-A9-LM@2026-10-23"
AGENT = "emstagent:A9-LM@claude-opus-5-5"
AGENTS = [AGENT, "emstagent:wp10-builder@0.2.0"]

# Re-check dates (WP-15 discipline): pending/contested facts before rc.1; settled facts at +6 or +12 months.
RECHECK_PENDING = "2026-12-15"
RECHECK_SETTLED = "2027-04-23"
RECHECK_HISTORIC = "2027-10-23"
WATCH_REVIEW_BY = "2027-10-23"  # ADR-0015: watch items and signals review at +12 months

SIGNAL_FAMILIES = ["capability", "observed-use", "deployment", "postings-pds", "headcount",
                   "plan-requirements", "worker-report", "policy", "projection", "workload"]
EXTRA_SCHEMES = {  # interim notation schemes (CR-LM-001)
    "family": "EMST-signalFamily",
    "indep": "EMST-independenceKey",
    "impact": "EMST-impact",
    "registered": "EMST-registeredDeployment",
    "signpost": "EMST-signpost",
    "points": "EMST-pointsToward",
    "baseline": "EMST-measureBaseline",
    "sensitivity": "EMST-measureSensitivity",
}

# WP-10 source rows (docs/methods/sources.csv) -> IDs the validator resolves today (V-pass key facts or role
# sources.csv rows). The precise page stays in docs/methods/sources.csv and in each record's `source`/method text.
RESOLVE = {
    "LM-101": ["V2-01"], "LM-102": ["V2-01"], "LM-103": ["V2-01"], "LM-104": ["V2-02"], "LM-105": ["V2-03"],
    "LM-106": ["V2-04"], "LM-107": ["V2-05"], "LM-108": ["V2-06"], "LM-109": ["V2-07"], "LM-110": ["V2-08"],
    "LM-111": ["V2-09"], "LM-112": ["V2-14"], "LM-113": ["V2-15"], "LM-114": ["V2-15"], "LM-115": ["V2-16"],
    "LM-116": ["V2-17"], "LM-117": ["CP-043", "IO-034"], "LM-118": ["IO-028", "IO-020"], "LM-119": ["IO-022"],
    "LM-120": ["V1-08"], "LM-121": ["V1-09", "V1-17"], "LM-122": ["V1-10"], "LM-123": ["V1-13"], "LM-124": ["V1-12"],
    "LM-125": ["V1-06"], "LM-126": ["V1-15"], "LM-127": ["V1-05"], "LM-128": ["V1-01", "V1-02"], "LM-129": ["V1-03"],
    "LM-130": ["V1-14"], "LM-131": ["V1-04"], "LM-132": ["V4-07"], "LM-133": ["V4-07"], "LM-134": ["V4-01"],
    "LM-135": ["LM-071"], "LM-136": ["V4-02"], "LM-137": ["V4-03"], "LM-138": ["V4-15"], "LM-139": ["V1-16"],
    "LM-140": ["DC-016"], "LM-141": ["V3-13"], "LM-142": ["V3-03"], "LM-143": ["V4-08"], "LM-144": ["LM-017", "LM-018"],
    "LM-145": ["V4-07"], "LM-146": ["V4-07"], "LM-147": ["V4-07"], "LM-148": ["V4-07"], "LM-149": ["V4-07"],
    "LM-150": ["V4-07"], "LM-151": ["V4-07"],
}


def resolve(sources):
    out = []
    for s in sources:
        out.extend(RESOLVE.get(s, [s]))
    return sorted(set(out))


def provenance(sources, evidence_label="E", method="llm-assisted", confidence=None, adr="ADR-0028"):
    src = resolve(sources)
    if evidence_label == "E" and not src:
        raise ValueError("E label requires sources")
    p = {
        "method": method,
        "agent": AGENTS,
        "generatedAt": GENERATED_AT,
        "evidenceLabel": evidence_label,
        "reviewStatus": "unreviewed",
        "toolVersion": TOOL_VERSION,
        "promptVersion": PROMPT_VERSION,
        "adr": adr,
    }
    if src:
        p["sources"] = src
    if confidence is not None:
        p["confidence"] = confidence
    return p


def base(rec_id, rec_type, label, definition=None, editorial_note=None, notation=None, held=False, scope_note=None):
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
    if scope_note:
        r["scopeNote"] = {"en": scope_note}
    if editorial_note:
        r["editorialNote"] = {"en": editorial_note}
    if notation:
        r["notation"] = notation
    if held:
        # ADR-0007 s.D / SPEC 16.1: Tribal hold. Excluded from every release artifact by CI.
        r["sensitivity"] = "restricted-governed"
        r["indigenousDataFlag"] = True
        r["approvalStatus"] = "pending-tribal-review"
        r["aiUsePermitted"] = False
    return r


def extras(**kw):
    """Interim notation entries for fields the schema does not type yet (CR-LM-001)."""
    out = []
    for k, v in kw.items():
        if v is None:
            continue
        vals = v if isinstance(v, list) else [v]
        for x in vals:
            out.append({"scheme": EXTRA_SCHEMES[k], "value": str(x).lower() if isinstance(x, bool) else str(x)})
    return out


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


def write_yaml_record(reldir, rec):
    import sys
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import emstlib as L  # DE's canonical YAML dumper and id -> file-stem rule
    path = os.path.join(ROOT, reldir, L.id_to_stem(rec["id"]) + ".yaml")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(L.dump_yaml(rec))
    return path


def slug(s):
    out = []
    for ch in s.lower():
        out.append(ch if ch.isalnum() else "-")
    t = "".join(out)
    while "--" in t:
        t = t.replace("--", "-")
    return t.strip("-")
