#!/usr/bin/env python3
"""X9 (part) — EMST competencies -> OPM Executive Core Qualifications, current five-ECQ framework only (ADR-0022).

The framework (chart updated 2025-10-01) was verified on the OPM page on 2026-10-23 (WP09-013; SC-058). Retired ECQ
competencies (Political Savvy, Partnering, Influencing/Negotiating and others) are never mapping targets; where an
EMST competency's natural target was a retired name, the row is skos:closeMatch sssom:NoTermFound with the reason.
FWCI general/technical competencies (2210 only, Apr 2026) and USA Hire coverage are later X9 parts.
ECQ "Technical Skill" (ECQ3-C1) is deliberately not enumerated: every EMST practice competency is a narrower,
domain-specific instance of it. Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "linker"))
import sssomlib as S  # noqa: E402
from emst_linker import corpus  # noqa: E402

TOOL = "pipelines/crosswalks/x9_ecq.py@0.1.0"
VERSION = "2025-10-01"


def main():
    legend = {r["ecq_id"]: r for r in csv.DictReader(open(HERE / "reference" / f"opm_ecq_{VERSION}.csv", encoding="utf-8"))}
    comps, _, rel = corpus.load()
    live = {c["id"]: c for c in comps}
    rows, stale = [], []
    for d in csv.DictReader(open(HERE / "curation" / "x9_ecq.csv", encoding="utf-8")):
        if d["subject_id"] not in live:
            stale.append(d["subject_id"])
            continue
        if d["ecq"] == "NoTermFound":
            obj, wk = S.NO_TERM, S.NO_TERM
        else:
            if d["ecq"] not in legend or not legend[d["ecq"]]["parent_id"]:
                raise SystemExit(f"{d['ecq']} is not a current ECQ competency")
            obj, wk = f"OPMECQ:{d['ecq']}", d["predicate"]
        rows.append(dict(
            record_id=f"emst-x9-ecq:{d['subject_id'].split(':', 1)[1]}:{obj.split(':', 1)[1]}",
            subject_id=d["subject_id"], subject_label=live[d["subject_id"]]["label"],
            subject_source="emstsrc:emst-v2-competencies", predicate_id=d["predicate"], predicate_modifier=d["modifier"],
            object_id=obj, object_source="emstsrc:opm-ecq", object_source_version=f"OPM ECQs, chart updated {VERSION}",
            mapping_justification="semapv:LLMBasedMatching", confidence=d["confidence"], author_id=S.AUTHOR,
            mapping_date=S.TODAY, mapping_tool=TOOL,
            other=S.other_field(weakest_match_type=wk, review_status="candidate", evidence="S", rater_type="llm",
                                model=S.MODEL, prompt=S.PROMPT,
                                ecq_parent=(f"OPMECQ:{legend[d['ecq']]['parent_id']}" if obj != S.NO_TERM else "")),
            comment=d["rationale"] + " Requires human SME confirmation; SES qualification decisions are not based on EMST."))
    S.write_set("opm-ecq", VERSION, {
        "mapping_set_version": "0.1.0-draft",
        "mapping_set_title": "X9 (ECQ part) EMST competencies to OPM Executive Core Qualifications (five-ECQ framework, 2025-10-01)",
        "mapping_set_description": (
            "Agent-drafted candidate mappings to the 15 competencies of the current five ECQs (names verified on OPM's "
            "page 2026-10-23). Object IDs OPMECQ:ECQn-Cm are EMST keys (OPM assigns none); legend in "
            "pipelines/crosswalks/reference/opm_ecq_2025-10-01.csv; ecq_parent in `other`. broadMatch = the EMST "
            "competency is a domain or practitioner-level enactment of the ECQ competency; relatedMatch = partial overlap. "
            "Retired ECQ names (e.g. Partnering, Influencing/Negotiating, Political Savvy) are never targets: such cases "
            "are NoTermFound with the reason. Technical Skill (ECQ3-C1) is intentionally not enumerated. Not for SES "
            "qualification or rating decisions."),
        "subject_source": "emstsrc:emst-v2-competencies", "subject_source_version": f"2.0.0-draft (corpus sha256 {rel[:16]})",
        "object_source": "emstsrc:opm-ecq", "object_source_version": f"chart updated {VERSION}",
        "mapping_tool": TOOL,
        "see_also": ["https://www.opm.gov/policy-data-oversight/senior-executive-service/executive-core-qualifications/"],
    }, rows, {"OPMECQ": "https://w3id.org/emst/ext/opm-ecq/2025-10-01/", "emstsrc": "https://w3id.org/emst/sources/"})
    print(json.dumps({"set": S.summarize(rows), "stale_subjects_skipped": stale}, indent=1))


if __name__ == "__main__":
    main()
