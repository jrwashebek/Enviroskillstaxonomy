#!/usr/bin/env python3
"""WP-16 Step 1 edits to decision tables and the claims register (CA rulings, ADR-0031). Idempotent.

1. docs/decisions/candidate_disposition.csv: the three rows docs/decisions/integration/disposition_amendments.csv
   assigns to "CA with DE, WP-16" (DB-C56 new module row; DB-C53 and PS-C06 rationale extensions).        [§5.6]
2. docs/methods/claims_register.csv (brief Step 1.4; orchestrator requests):                              [§6]
   - PLAN-01 and OMB-02: the two data-text wrong forms re-quoted with single quotes (now enforced);
   - OMB-02 and RPT-04: "nine bureaus and two USDA mission areas" -> "nine agencies and bureaus and two USDA mission areas";
   - RPT-27: status verified -> derived (an EMST computation, like RPT-28).
CSV files are read and written with csv minimal quoting and CRLF line ends, which reproduces them byte for byte.
Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CANDS = ROOT / "docs/decisions/candidate_disposition.csv"
AMEND = ROOT / "docs/decisions/integration/disposition_amendments.csv"
REG = ROOT / "docs/methods/claims_register.csv"


def read(p):
    return list(csv.reader(io.StringIO(p.read_text(encoding="utf-8"))))


def write(p, rows):
    b = io.StringIO()
    csv.writer(b, lineterminator="\r\n").writerows(rows)
    if b.getvalue() != p.read_bytes().decode("utf-8"):
        p.write_text(b.getvalue(), encoding="utf-8", newline="")
        print(f"wrote {p.relative_to(ROOT)}")


def candidates():
    rows = read(CANDS)
    h = rows[0]
    ix = {k: i for i, k in enumerate(h)}
    by_id = {r[ix["cand_id"]]: r for r in rows[1:]}
    with open(AMEND, encoding="utf-8", newline="") as fh:
        amends = [a for a in csv.DictReader(fh) if a["file"] == "candidate_disposition.csv"]
    for a in amends:
        key = a["key"]
        target = a["amended_target"] if a["amended_target"] != "(as now)" else None
        if key not in by_id:
            # new row: DB-C56 (module candidate authored by DB in S2; CR-DB-001 #5)
            new = [""] * len(h)
            new[ix["cand_id"]] = key
            new[ix["role_folder"]] = "domain-bench"
            new[ix["proposed_title"]] = "Manage wildlife populations and harvest (season and bag setting from survey and harvest data)"
            new[ix["dedupe_group"]] = f"DG-{key}"
            new[ix["decision"]] = a["amended_decision"]
            new[ix["target"]] = target
            new[ix["rationale"]] = a["amended_rationale"] + " (CR-DB-001 #5; ADR-0030 §4; applied at WP-16, ADR-0031 §5.6)"
            rows.append(new)
            by_id[key] = new
        else:
            r = by_id[key]
            r[ix["decision"]] = a["amended_decision"]
            if target:
                r[ix["target"]] = target
            if not r[ix["rationale"]].startswith(a["amended_rationale"]):
                r[ix["rationale"]] = a["amended_rationale"]
    write(CANDS, rows)


PLAN_OLD = ('"monitoring requirements" (write \'components typed as monitoring\'; double-quoted so the explorer check does not '
            'yet enforce it while data/v2/signals/2026/openlmp.jsonl still uses the phrase, CR-FIX-A-003)')
PLAN_NEW = ("'monitoring requirements' (write 'components typed as monitoring'; enforced by the explorer check since WP-16 "
            "corrected the data text, ADR-0031)")
OMB_OLD = ('"nine environmental bureaus" (the 504 come from eleven units, two of them USDA mission areas; double-quoted so the '
           'explorer check does not yet enforce it while data/v2/signals/2026/omb-ai-inventory-2025.jsonl still uses the '
           'phrase, CR-FIX-A-003)')
OMB_NEW = ("'nine environmental bureaus' (the 504 come from eleven units, two of them USDA mission areas; enforced by the "
           "explorer check since WP-16 corrected the data text, ADR-0031)")
NINE_OLD = "(nine bureaus and two USDA mission areas"
NINE_NEW = "(nine agencies and bureaus and two USDA mission areas"


def register():
    rows = read(REG)
    h = rows[0]
    ix = {k: i for i, k in enumerate(h)}
    for r in rows[1:]:
        cid = r[ix["claim_id"]]
        if cid == "PLAN-01":
            r[ix["do_not_say"]] = r[ix["do_not_say"]].replace(PLAN_OLD, PLAN_NEW)
        if cid == "OMB-02":
            r[ix["do_not_say"]] = r[ix["do_not_say"]].replace(OMB_OLD, OMB_NEW)
        if cid in ("OMB-02", "RPT-04"):
            r[ix["claim"]] = r[ix["claim"]].replace(NINE_OLD, NINE_NEW)
        if cid == "RPT-27" and r[ix["status"]] == "verified":
            r[ix["status"]] = "derived"
    for r in rows[1:]:
        if r[ix["claim_id"]] == "PLAN-01" and PLAN_NEW not in r[ix["do_not_say"]]:
            sys.exit("PLAN-01 do_not_say not in the expected form")
        if r[ix["claim_id"]] == "OMB-02" and OMB_NEW not in r[ix["do_not_say"]]:
            sys.exit("OMB-02 do_not_say not in the expected form")
    write(REG, rows)


if __name__ == "__main__":
    candidates()
    register()
