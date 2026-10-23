#!/usr/bin/env python3
"""Convert WP-03 rating passes (pass{1,2,3}.txt) into CraftRating JSONL batches.

Writes data/v2/assessments/emst-craft@0.1/wp03-fc-pass{n}.jsonl, one record per unit, pinned to the task text hash
recorded in key_private.csv at frame time (a rating goes stale automatically if the task text changes). Every value is
raterType llm, evidence label S, draft (PHASE4_BUILD_PLAN §1 rule 2). Agreement is never stored; consistency is
reported by summarize() as run-to-run consistency of one model family, not inter-rater reliability. Licence: Apache-2.0.
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = ROOT / "data/v2/assessments/emst-craft@0.1"
METHOD = ("codebook emst-craft-codebook@1.0.0-draft sections 3-7 applied to the task statement only, units in a "
          "pass-specific random order (frame seed {seed}); same model and session as the author, so blind to the parent "
          "competency in the frame but not to authoring context: run-to-run consistency only, LLM-coder gate level G0")


def load_pass(n):
    vals = {}
    for line in open(HERE / f"pass{n}.txt", encoding="utf-8"):
        if not line.strip() or line.startswith("#"):
            continue
        u, fc, dc, sc, conf = line.split()[:5]
        vals[u] = ({"FC": int(fc), "DC": int(dc), "SC": int(sc)}, conf)
    return vals


def main():
    key = {r["unit"]: r for r in csv.DictReader(open(HERE / "key_private.csv", encoding="utf-8"))}
    OUT.mkdir(parents=True, exist_ok=True)
    passes = {}
    for n, seed in ((1, 11), (2, 22), (3, 33)):
        vals = load_pass(n)
        missing = set(key) - set(vals)
        extra = set(vals) - set(key)
        if missing or extra:
            sys.exit(f"pass {n}: missing {sorted(missing)[:5]} extra {sorted(extra)[:5]}")
        passes[n] = vals
        rater = f"emstagent:fc-rater-{n}@wp03"
        lines = []
        for u in sorted(key, key=lambda x: key[x]["task"]):
            tid = key[u]["task"]
            v, conf = vals[u]
            stem = tid[len("seed:"):]
            rec = {"id": f"seed:asm/wp03-fc-pass{n}/{stem}", "type": "CraftRating",
                   "prefLabel": {"en": f"WP-03 FC pass {n} craft rating of {tid}"},
                   "layer": "L5", "module": "core", "status": "draft", "license": "CC0-1.0", "sensitivity": "public",
                   "task": tid, "taskTextSha256": key[u]["taskTextSha256"], "scale": "ordinal-0-2", "values": v,
                   "raterType": "llm", "raterId": rater, "assessedAt": "2026-10-23", "method": METHOD.format(seed=seed),
                   "confidence": conf, "instrument": "emst-craft@0.1",
                   "codebookVersion": "emst-craft-codebook@1.0.0-draft (vocab/crafts.yaml 1.0.0-draft)",
                   "evidenceLabel": "S", "sources": [],
                   "provenance": {"method": "llm-assisted", "agent": [rater], "generatedAt": "2026-10-23T16:00:00Z",
                                  "toolVersion": "claude-opus-5-5", "promptVersion": "wp03-craft-rating@1",
                                  "evidenceLabel": "S", "reviewStatus": "unreviewed", "adr": ["ADR-0005", "WP-03"]}}
            lines.append(json.dumps(rec, ensure_ascii=False, separators=(",", ":")))
        (OUT / f"wp03-fc-pass{n}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    summarize(passes, key)


def summarize(passes, key):
    units = sorted(key)
    print(f"units rated per pass: {len(units)}; passes: {len(passes)}")
    for c in ("FC", "DC", "SC"):
        same = sum(1 for u in units if len({passes[n][u][0][c] for n in passes}) == 1)
        print(f"{c}: identical across the three passes on {same} of {len(units)} units (run-to-run consistency, not reliability)")
    modal = Counter()
    for u in units:
        fc2 = Counter(passes[n][u][0]["FC"] for n in passes).most_common(1)[0][0]
        modal[fc2] += 1
    print("modal FC value across units:", dict(sorted(modal.items())))
    none2 = sum(1 for u in units if all(max(passes[n][u][0].values()) < 2 for n in passes))
    print(f"units with no craft at 2 in every pass (general professional practice): {none2}")


if __name__ == "__main__":
    main()
