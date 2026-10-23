#!/usr/bin/env python3
"""S2 close-out A: three LLM craft-rating passes over the tasks build_s2a.py writes (emst-craft@0.1).

Each pass coded task text only (no competency, v1 code or prior label shown), in its own random order
(random.seed(pass) over build_s2a.py --list-tasks). Ratings are typed in rating/pass{n}.txt as
"<position> FC DC SC confidence". Same model and session as the author, so not blind to the authoring context:
run-to-run consistency only, LLM-coder gate G0 (validation/protocol_llm_coder_gate.md). raterType llm, evidence S.
Writes data/v2/assessments/emst-craft@0.1/s2a-pass{n}.jsonl and generated/craft_run_consistency.json.
Licence: Apache-2.0 (code); records CC0-1.0.
"""
import json
import random
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

GEN = "2026-10-23T18:10:00Z"
OUT = L.DATA_V2 / "assessments" / "emst-craft@0.1"


def tasks():
    out = subprocess.run([sys.executable, str(HERE / "build_s2a.py"), "--list-tasks"], capture_output=True, text=True,
                         check=True).stdout
    return [tuple(l.split(" \t ", 1)) for l in out.splitlines() if l.strip()]


def main():
    base = tasks()
    table = {}
    for n in (1, 2, 3):
        rows = list(base)
        random.seed(n)
        random.shuffle(rows)
        lines = [l.split() for l in (HERE / "rating" / f"pass{n}.txt").read_text().splitlines() if l.strip()]
        if len(lines) != len(rows):
            raise SystemExit(f"pass {n}: {len(lines)} ratings for {len(rows)} tasks")
        recs = []
        for pos, fc, dc, sc, conf in lines:
            tid, text = rows[int(pos) - 1]
            table.setdefault(tid, []).append((int(fc), int(dc), int(sc)))
            stem = L.id_to_stem(tid)
            recs.append({
                "id": f"seed:asm/s2a-pass{n}/{stem}", "type": "CraftRating",
                "prefLabel": {"en": f"S2 close-out A pass {n} craft rating of {tid}"}, "layer": "L5", "module": "core",
                "status": "draft", "license": "CC0-1.0", "sensitivity": "public",
                "task": tid, "taskTextSha256": L.text_sha256(text), "scale": "ordinal-0-2",
                "values": {"FC": int(fc), "DC": int(dc), "SC": int(sc)}, "raterType": "llm",
                "raterId": f"emstagent:s2a-rater-{n}@s2-closeout-a", "assessedAt": "2026-10-23",
                "method": ("codebook emst-craft-codebook@1.0.0-draft sections 3-6 applied to task text only, units in a "
                           f"pass-specific random order (seed {n}); same model and session as the author, so not blind to "
                           "authoring context: run-to-run consistency only, LLM-coder gate level G0"),
                "confidence": conf, "instrument": "emst-craft@0.1",
                "codebookVersion": "emst-craft-codebook@1.0.0-draft (vocab/crafts.yaml 1.0.0-draft)",
                "evidenceLabel": "S", "sources": [],
                "provenance": {"method": "llm-assisted", "agent": [f"emstagent:s2a-rater-{n}@s2-closeout-a"],
                               "generatedAt": GEN, "toolVersion": "claude-opus-5-5",
                               "promptVersion": f"docs/build/S2-closeout-A/rating/pass{n}.txt@s2a-craft@1",
                               "evidenceLabel": "S", "reviewStatus": "unreviewed", "adr": ["ADR-0005", "ADR-0030"]}})
        recs.sort(key=lambda r: r["id"])
        L.write_jsonl(OUT / f"s2a-pass{n}.jsonl", recs)
    agree = Counter()
    for tid, vals in table.items():
        for i, c in enumerate(("FC", "DC", "SC")):
            agree[(c, len({v[i] for v in vals}) == 1)] += 1
    summary = {"tasks": len(table), "note": "run-to-run consistency of one model, not inter-rater reliability",
               "allThreePassesEqual": {c: agree[(c, True)] for c in ("FC", "DC", "SC")},
               "anyDisagreement": {c: agree[(c, False)] for c in ("FC", "DC", "SC")},
               "splitUnits": sorted(t for t, v in table.items() if len(set(v)) > 1)}
    (HERE / "generated").mkdir(exist_ok=True)
    (HERE / "generated" / "craft_run_consistency.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "splitUnits"}, indent=1), len(summary["splitUnits"]))


if __name__ == "__main__":
    main()
