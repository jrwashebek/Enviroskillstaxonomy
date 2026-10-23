#!/usr/bin/env python3
"""Merge the shared-schema CSVs written by each research role into one set of files.

Reads docs/research/<role>/{sources,candidate_competencies,role_signals,v1_assessment,ecosystem}.csv
and docs/audit/v1_carry_forward_register.csv, validates headers against TEAM_BRIEF.md section 5,
and writes docs/research/_merged/*.csv plus a validation report. Rows are never altered; a
`role_folder` column is added so every row stays traceable to the role that produced it.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "docs" / "research"
OUT = RESEARCH / "_merged"

SCHEMAS = {
    "sources": "source_id,title,author_or_publisher,date_published,url,source_type,accessed,used_for,quality,status,why_chosen",
    "candidate_competencies": "cand_id,proposed_title,description,craft_primary,craft_secondary,subsector,sector_actors,change_type,driver,evidence_label,source_ids,related_v1_codes,rationale,proposed_by",
    "role_signals": "signal_id,role_title,sector_actor,subsector,signal_type,description,driver,horizon,evidence_label,source_ids,related_v1_codes,proposed_by",
    "v1_assessment": "element,v1_location,verdict,rationale,evidence_label,source_ids,proposed_by",
    "ecosystem": "entity_id,name,entity_type,owner_or_host,sector_focus,what_it_illuminates,latest_release_or_status,how_emst_connects,integration_detail,url,evidence_label,source_ids,proposed_by",
}

csv.field_size_limit(sys.maxsize)


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        rows = [r for r in reader]
        return (reader.fieldnames or []), rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    report: dict = {"files": [], "totals": {}}
    for name, header in SCHEMAS.items():
        expected = header.split(",")
        merged: list[dict] = []
        inputs = sorted(RESEARCH.glob(f"*/{name}.csv"))
        if name == "v1_assessment":
            audit = ROOT / "docs" / "audit" / "v1_carry_forward_register.csv"
            if audit.exists():
                inputs.append(audit)
        for path in inputs:
            if path.parent.name.startswith("_"):
                continue
            try:
                fields, rows = read_csv(path)
            except Exception as exc:  # noqa: BLE001 - report and continue
                report["files"].append({"file": str(path.relative_to(ROOT)), "error": repr(exc)})
                continue
            missing = [c for c in expected if c not in fields]
            extra = [c for c in fields if c not in expected]
            report["files"].append({
                "file": str(path.relative_to(ROOT)),
                "rows": len(rows),
                "missing_columns": missing,
                "extra_columns": extra,
                "header_exact": fields == expected,
            })
            for r in rows:
                row = {c: (r.get(c) or "").strip() for c in expected}
                row["role_folder"] = path.parent.name
                merged.append(row)
        with (OUT / f"{name}.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=expected + ["role_folder"])
            w.writeheader()
            w.writerows(merged)
        report["totals"][name] = len(merged)
    (OUT / "merge_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["totals"], indent=2))
    bad = [f for f in report["files"] if f.get("error") or f.get("missing_columns")]
    if bad:
        print(f"{len(bad)} file(s) with problems; see {OUT / 'merge_report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
