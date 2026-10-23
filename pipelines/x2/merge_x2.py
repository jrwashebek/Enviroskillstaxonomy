#!/usr/bin/env python3
"""X2 — merge coder files into the SSSOM set data/v2/crosswalks/onet-task/<release>.sssom.tsv (ADR-0022).

One row per unit. With one coder, the row is that coder's decision (review_status=single-coder-candidate). With two
coders, the row takes the agreed object when both chose the same target (predicate = the weaker of the two types,
kept as weakest_match_type), or is marked needs-adjudication with both codes in `other`. IDs only (ADR-0013).
Usage: python pipelines/x2/merge_x2.py --release 27.2 [--coder-b coding/coder-b.csv]
Licence: Apache-2.0.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "crosswalks"))
import sssomlib as S  # noqa: E402

TOOL = "pipelines/x2/merge_x2.py@0.1.0"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", default="27.2")
    ap.add_argument("--coder-a", default=str(HERE / "coding" / "coder-a.csv"))
    ap.add_argument("--coder-b", default=str(HERE / "coding" / "coder-b.csv"))
    a = ap.parse_args()
    units = {r["unit_id"]: r for r in csv.DictReader(open(HERE / "work" / "x2_units.csv", encoding="utf-8"))}
    frame = json.loads((HERE / "work" / "x2_frame.json").read_text())
    A = {r["unit_id"]: r for r in csv.DictReader(open(a.coder_a, encoding="utf-8"))}
    B = {r["unit_id"]: r for r in csv.DictReader(open(a.coder_b, encoding="utf-8"))} if Path(a.coder_b).exists() else {}
    rows = []
    for u, ra in sorted(A.items()):
        if u not in units:
            continue   # unit left the frame since coding
        rb = B.get(u)
        status = "single-coder-candidate"
        obj, pred, conf = ra["object_id"], ra["predicate"], ra["confidence"]
        extra = {"coder_a": f"{ra['object_id']}|{ra['predicate']}"}
        if rb:
            extra["coder_b"] = f"{rb['object_id']}|{rb['predicate']}"
            extra["coder_b_id"] = rb["coder_id"]
            if rb["object_id"] == ra["object_id"]:
                status = "two-coder-agreed-target"
                pred = S.weakest(ra["predicate"], rb["predicate"]) if obj != "NoTermFound" else "skos:closeMatch"
                conf = str(round(min(float(ra["confidence"]), float(rb["confidence"])), 2))
            else:
                status = "needs-adjudication"
                pa = S.NO_TERM if ra["object_id"] == "NoTermFound" else ra["predicate"]
                pb = S.NO_TERM if rb["object_id"] == "NoTermFound" else rb["predicate"]
                extra["weakest_of_both"] = S.NO_TERM if S.NO_TERM in (pa, pb) else S.weakest(pa, pb)
        objid = S.NO_TERM if obj == "NoTermFound" else obj
        wk = S.NO_TERM if objid == S.NO_TERM else pred
        if status == "needs-adjudication":
            wk = extra["weakest_of_both"]
        uu = units[u]
        rows.append(dict(
            record_id=f"emst-x2:{u.split(':', 1)[1]}", subject_id=u, subject_source="emstsrc:emst-v2-tasks",
            predicate_id=pred, object_id=objid, object_source="emstsrc:onet-tasks",
            object_source_version=f"O*NET {a.release} task statements" + (" (Eloundou base; 31.0 re-pin pending)" if a.release.startswith("27") else ""),
            mapping_justification="semapv:LLMBasedMatching", confidence=conf, author_id=ra["coder_id"],
            mapping_date=S.TODAY, mapping_tool=TOOL,
            other=S.other_field(weakest_match_type=wk, review_status=status, evidence="S", rater_type="llm",
                                text_sha256=uu["textSha256"], competency=uu["competency"], p1_roles=uu["roles"],
                                pool=uu["pool_socs"], found_by=ra["found_by"], **extra),
            comment=("no-term reason: no O*NET task in the role family's occupations describes this work ("
                     + ("coders A and B" if status == "two-coder-agreed-target" else "coder A") + "). "
                     if objid == S.NO_TERM else "") + "Agent-coded candidate; second blind LLM coder "
                     + ("present (LLM-vs-LLM)." if rb else "pending.") + " Not for exposure joins until adjudicated (CODING_PROTOCOL.md §4)."))
    S.write_set("onet-task", a.release, {
        "mapping_set_version": "0.2.0-draft",
        "mapping_set_title": f"X2 EMST P1-corridor tasks to O*NET {a.release} task statements",
        "mapping_set_description": (
            "EMST v2 tasks in the P1 frame (pipelines/x2/p1_frame.yaml#taskToP1Roles, from WP-08's P1 bundles) coded against O*NET task "
            "statements of the role family's O*NET-SOC pool (from X3), per pipelines/x2/CODING_PROTOCOL.md. "
            f"Release {a.release}: the Eloundou-labelled task set ADR-0022 requires; O*NET 31.0 (target) was not "
            "downloadable on 2026-10-23 and will be produced by the upstream diff. DWAs pending (Tasks-to-DWAs file "
            "not available offline). review_status: single-coder-candidate | two-coder-agreed-target | "
            "needs-adjudication (row keeps coder A's object; weakest_match_type is the weaker of both codes). "
            "Coder agreement in pipelines/x2/work/x2_kappa.json (generated); with two LLM coders it is LLM-vs-LLM "
            "agreement, not human inter-coder reliability."),
        "subject_source": "emstsrc:emst-v2-tasks", "subject_source_version": f"2.0.0-draft (frame {frame['frameVersion']}, sha256 {frame['frame_sha256'][:12]})",
        "object_source": "emstsrc:onet-tasks", "object_source_version": f"O*NET {a.release}",
        "mapping_tool": TOOL,
        "see_also": ["https://www.onetcenter.org/dictionary/31.0/csv/task_statements.html",
                     "https://github.com/openai/GPTs-are-GPTs"],
        "comment": "O*NET content CC BY 4.0 (USDOL/ETA); this set stores O*NET IDs only.",
    }, rows, {"ONET": "https://w3id.org/emst/ext/onet-task/", "emstsrc": "https://w3id.org/emst/sources/"})
    print(json.dumps({"rows": len(rows), "coder_b_present": bool(B), **S.summarize(rows)}, indent=1))


if __name__ == "__main__":
    main()
