#!/usr/bin/env python3
"""Run-to-run consistency of WP-05's three LLM craft-rating passes (IO protocol_llm_coder_gate.md section 4.2).

This is NOT inter-rater reliability, SME agreement or a gate statistic: the three passes are one rater type (same
model, same session as the author; different unit orderings). Output goes to generated/ only. Licence: Apache-2.0.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "validation"))
from reliability import bootstrap_alpha, krippendorff_alpha  # noqa: E402


def main():
    passes = []
    for n in (1, 2, 3):
        with (HERE / f"ratings_pass{n}.csv").open(encoding="utf-8") as f:
            passes.append({r["task_id"]: r for r in csv.DictReader(f)})
    ids = sorted(passes[0])
    out = {"note": "run-to-run consistency of one LLM rater type (3 orderings); not reliability; LLM-coder gate G0",
           "units": len(ids), "crafts": {}}
    modal_rows = []
    for craft in ("FC", "DC", "SC"):
        data = [[int(p[i][craft]) for p in passes] for i in ids]     # units x raters
        a = krippendorff_alpha(data, level="ordinal")
        bs = bootstrap_alpha(data, level="ordinal", B=2000)
        lo, hi = round(bs["ciLower"], 3), round(bs["ciUpper"], 3)
        exact = sum(1 for j in range(len(ids)) if len(set(data[j])) == 1) / len(ids)
        out["crafts"][craft] = {"alpha_ordinal": round(a, 3), "ci95": [lo, hi], "share_all_three_equal": round(exact, 3)}
    for i in ids:
        vals = {c: [int(p[i][c]) for p in passes] for c in ("FC", "DC", "SC")}
        modal_rows.append({"task": i, **{c: "|".join(map(str, v)) for c, v in vals.items()},
                           "split": any(len(set(v)) > 1 for v in vals.values())})
    (HERE / "generated").mkdir(exist_ok=True)
    (HERE / "generated" / "craft_run_consistency.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    with (HERE / "generated" / "craft_split_units.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["task", "FC", "DC", "SC", "split"])
        w.writeheader()
        w.writerows(r for r in modal_rows if r["split"])
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
