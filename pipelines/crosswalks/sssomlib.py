"""Shared writer and checker for EMST crosswalk mapping sets (WP-09, ADR-0022, SPEC §15).

Every set is SSSOM 1.0 TSV with an external `.sssom.yml` metadata file, one set per upstream version, written to
`data/v2/crosswalks/<target>/<target-version>.sssom.tsv`. Rows carry external IDs only (ADR-0013 §5): this module
refuses `object_label`, `match_string` and any column outside the validator's SSSOM allow-list, and checks that
each row states its justification, its weakest match type and its review status in `other`.

Licence: Apache-2.0 (code). Author: emstagent:ia-wp09@phase4.
"""
from __future__ import annotations

import csv
import io
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

XW = L.DATA_V2 / "crosswalks"
AUTHOR = "emstagent:ia-wp09@phase4"
MODEL = "claude-opus-5-5"
PROMPT = "wp09-crosswalk@1"
TODAY = "2026-10-23"
CC0 = "https://creativecommons.org/publicdomain/zero/1.0/"

# Column order for EMST mapping sets (subset of the validator's SSSOM_COLUMNS; SSSOM 1.1 record_id as extension).
COLUMNS = ["record_id", "subject_id", "subject_label", "subject_source", "subject_type", "predicate_id",
           "predicate_modifier", "object_id", "object_source", "object_source_version", "object_type",
           "mapping_justification", "confidence", "similarity_score", "similarity_measure", "author_id",
           "reviewer_id", "reviewer_agreement", "mapping_date", "mapping_tool", "mapping_cardinality", "see_also",
           "other", "comment"]
FORBIDDEN = {"object_label", "match_string"}          # upstream text never enters CC0 files
NO_TERM = "sssom:NoTermFound"
STRENGTH = {"skos:exactMatch": 5, "skos:closeMatch": 4, "skos:broadMatch": 3, "skos:narrowMatch": 3,
            "skos:relatedMatch": 2}
BASE_CURIES = {
    "emst": "https://w3id.org/emst/",
    "seed": "https://w3id.org/emst/seed/",
    "emstagent": "https://w3id.org/emst/agent/",
    "sssom": "https://w3id.org/sssom/",
    "semapv": "https://w3id.org/semapv/vocab/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
}
# SSSOM 1.1 slots used before 1.1 is final (V4-13): declared as extensions in every metadata file.
EXTENSIONS = [
    {"slot_name": "record_id", "property": "https://w3id.org/sssom/record_id", "type_hint": "xsd:string"},
    {"slot_name": "reviewer_agreement", "property": "https://w3id.org/sssom/reviewer_agreement",
     "type_hint": "xsd:double"},
]


def vocab_terms():
    v = L.load_yaml(L.VOCAB / "mapping_predicates.yaml")
    preds = {p["notation"] for p in v["skos_predicates"]} | {p["notation"] for p in v["emst_relations"]}
    return preds, set(v["justifications"])


def weakest(*preds: str) -> str:
    """Weakest predicate along a mapping path (exact > close > broad/narrow > related)."""
    ps = [p for p in preds if p in STRENGTH]
    if not ps:
        return ""
    lo = min(STRENGTH[p] for p in ps)
    cands = [p for p in ps if STRENGTH[p] == lo]
    if len(set(cands)) > 1 and lo == 3:   # broad then narrow (or reverse) composes to related
        return "skos:relatedMatch"
    return cands[0]


def chain(p1: str, p2: str) -> str:
    """Compose two SKOS mapping predicates (subject->mid, mid->object) conservatively."""
    if p1 == p2:
        return p1
    if "skos:exactMatch" in (p1, p2):
        return p2 if p1 == "skos:exactMatch" else p1
    if "skos:closeMatch" in (p1, p2):
        other = p2 if p1 == "skos:closeMatch" else p1
        return other
    if {p1, p2} == {"skos:broadMatch", "skos:narrowMatch"}:
        return "skos:relatedMatch"
    return "skos:relatedMatch"


def other_field(**kv) -> str:
    parts = []
    for k, v in kv.items():
        if v is None or v == "":
            continue
        s = str(v).replace(";", ",").replace("\t", " ").replace("\n", " ")
        parts.append(f"{k}={s}")
    return ";".join(parts)


def parse_other(s: str) -> dict:
    out = {}
    for part in (s or "").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


class SetError(Exception):
    pass


def check_rows(rows: list[dict], preds: set, justs: set) -> list[str]:
    errs = []
    seen = Counter()
    for i, r in enumerate(rows, 2):
        where = f"row {i} ({r.get('record_id')})"
        for k in r:
            if k in FORBIDDEN:
                errs.append(f"{where}: forbidden column {k} (upstream text; ADR-0013)")
            elif k not in COLUMNS:
                errs.append(f"{where}: column {k} not in EMST SSSOM profile")
        for k in ("record_id", "subject_id", "predicate_id", "object_id", "mapping_justification", "author_id",
                  "mapping_date", "other", "comment"):
            if not r.get(k):
                errs.append(f"{where}: {k} is required in EMST crosswalk rows")
        if r.get("predicate_id") not in preds:
            errs.append(f"{where}: predicate {r.get('predicate_id')!r} not in vocab")
        if r.get("mapping_justification") not in justs:
            errs.append(f"{where}: justification {r.get('mapping_justification')!r} not in vocab")
        if r.get("predicate_modifier") not in (None, "", "Not"):
            errs.append(f"{where}: predicate_modifier must be Not or empty")
        o = parse_other(r.get("other", ""))
        for k in ("weakest_match_type", "review_status", "evidence"):
            if k not in o:
                errs.append(f"{where}: other lacks {k}")
        if o.get("weakest_match_type") and o["weakest_match_type"] not in STRENGTH and o["weakest_match_type"] != NO_TERM:
            errs.append(f"{where}: weakest_match_type {o['weakest_match_type']} not a SKOS predicate or NoTermFound")
        if r.get("object_id") == NO_TERM and not re.search(r"no[- ]term reason:", r.get("comment", ""), re.I):
            errs.append(f"{where}: NoTermFound rows must state 'no-term reason:' in comment")
        # one NoTermFound convention (vocab/mapping_predicates.yaml#no_match_convention; ADR-0032, review M9)
        if r.get("object_id") == NO_TERM and r.get("predicate_id") in STRENGTH and r.get("predicate_modifier") != "Not":
            errs.append(f"{where}: a NoTermFound row never asserts a positive predicate: set predicate_modifier Not")
        if "held_variants" in o:
            errs.append(f"{where}: `other` must not mark held variants (ADR-0032, review m14)")
        for c in ("confidence", "similarity_score", "reviewer_agreement"):
            v = r.get(c)
            if v not in (None, ""):
                try:
                    x = float(v)
                    lo = -1 if c == "reviewer_agreement" else 0
                    if not lo <= x <= 1:
                        raise ValueError
                except ValueError:
                    errs.append(f"{where}: {c} out of range")
        for k, v in r.items():
            if isinstance(v, str) and ("\t" in v or "\n" in v):
                errs.append(f"{where}: {k} contains a tab or newline")
        seen[r.get("record_id")] += 1
    for rid, n in seen.items():
        if n > 1:
            errs.append(f"record_id {rid} repeated {n} times")
    return errs


def write_set(target: str, version: str, meta: dict, rows: list[dict], curies: dict) -> Path:
    """Validate and write `<target>/<version>.sssom.tsv` + `.sssom.yml`. Returns the TSV path."""
    preds, justs = vocab_terms()
    for r in rows:                         # NoTermFound convention applied on write (ADR-0032, review M9)
        if r.get("object_id") == NO_TERM and r.get("predicate_id") in STRENGTH:
            r["predicate_modifier"] = "Not"
    errs = check_rows(rows, preds, justs)
    if errs:
        raise SetError("\n".join(errs[:50]) + (f"\n... {len(errs)} errors" if len(errs) > 50 else ""))
    used = [c for c in COLUMNS if any(r.get(c) not in (None, "") for r in rows)]
    d = XW / target
    d.mkdir(parents=True, exist_ok=True)
    tsv = d / f"{version}.sssom.tsv"
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=used, delimiter="\t", lineterminator="\n", extrasaction="ignore",
                       quoting=csv.QUOTE_NONE, escapechar=None)
    w.writeheader()
    for r in rows:
        w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in used})
    tsv.write_text(buf.getvalue(), encoding="utf-8")
    cm = dict(BASE_CURIES)
    cm.update(curies)
    md = {
        "mapping_set_id": f"https://w3id.org/emst/crosswalks/{target}/{version}",
        "mapping_set_version": meta.pop("mapping_set_version", "0.1.0-draft"),
    }
    md.update(meta)
    md.setdefault("license", CC0)
    md.setdefault("creator_id", [AUTHOR])
    md.setdefault("mapping_date", TODAY)
    md["curie_map"] = cm
    md["extension_definitions"] = EXTENSIONS
    (d / f"{version}.sssom.yml").write_text(L.dump_yaml(md), encoding="utf-8")
    return tsv


def summarize(rows: list[dict]) -> dict:
    """Generated set statistics (never typed): subjects, coverage, predicate mix, NoTermFound, negations."""
    subj = {r["subject_id"] for r in rows}
    pos = [r for r in rows if r.get("predicate_modifier") != "Not" and r["object_id"] != NO_TERM]
    covered = {r["subject_id"] for r in pos}
    pm = Counter(r["predicate_id"] for r in pos)
    return {
        "rows": len(rows),
        "subjects": len(subj),
        "subjects_with_positive_mapping": len(covered),
        "no_term_found_rows": sum(1 for r in rows if r["object_id"] == NO_TERM),
        "negated_rows": sum(1 for r in rows if r.get("predicate_modifier") == "Not"),
        "predicate_mix": dict(sorted(pm.items())),
    }


def read_set(tsv: Path) -> list[dict]:
    with open(tsv, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))
