#!/usr/bin/env python3
"""WP-06 blind craft-rating passes (authoring aid for A6 DB).

Three independent llm-rater passes over every Task WP-06 wrote or rewrote (docs/build/WP-06/manifest.csv). Each pass is
a separate `claude -p` session started in an empty directory with tools disabled. The rater sees only the IO craft
codebook (validation/codebook_craft_ratings.md) and the task statements, shuffled with a pass-specific seed under
pass-specific keys: never the task's competency, module, v1 code or any other rating (codebook §2, XR-01).

  python3 docs/build/WP-06/rate_crafts.py run      # run the three passes (writes ratings/pass<n>_raw.json)
  python3 docs/build/WP-06/rate_crafts.py write    # parse the raw answers into CraftRating JSONL batches

Outputs: data/v2/assessments/emst-craft@0.1/wp06-db-pass<n>.jsonl (raterType llm, evidence label S, draft) and
docs/build/WP-06/ratings/cannot_code.csv. Agreement is computed by CI, never here.
"""
from __future__ import annotations

import csv
import json
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402

RAT = HERE / "ratings"
OUT = REPO / "data" / "v2" / "assessments" / "emst-craft@0.1"
MODEL = "claude-opus-5-5"
PROMPT_VERSION = "wp06-craft-blind@1"
CODEBOOK = REPO / "validation" / "codebook_craft_ratings.md"
CODEBOOK_VERSION = "emst-craft-codebook@1.0.0-draft"
ASSESSED = "2026-10-23"
GEN_AT = "2026-10-23T14:30:00Z"
WORKDIR = Path("/tmp/claude-0/-home-claude/fbbe9940-26ca-5e5a-9a05-1e06b16da4ee/scratchpad/wp06/rater")
TOOLS_OFF = ["Bash", "Read", "Glob", "Grep", "Edit", "Write", "WebFetch", "WebSearch", "NotebookEdit", "Task", "Agent"]

INSTRUCTIONS = """You are rater {n} in a blind craft-rating study. Apply the codebook below exactly. Rate each task
statement on its own, using only its text. Do not use tools. Do not try to find the source of the tasks.

For each task give FC, DC and SC on the 0/1/2 scale (codebook sections 1-4 and 6), and a confidence from 1 (guess) to
5 (certain). If you cannot code a task (codebook section 7), set "cannot" to one of: not a task, compound, missing
information, held content, two readings; otherwise set "cannot" to null. Add a note of at most 12 words only when
useful.

Answer with JSON Lines only: one object per task, in the order given, with exactly these keys:
{{"k": "<key>", "FC": 0|1|2, "DC": 0|1|2, "SC": 0|1|2, "conf": 1-5, "cannot": null|"<reason>", "note": "<text>"}}
No prose before or after the JSON Lines.

=== CODEBOOK ===
{codebook}
=== END CODEBOOK ===

=== TASKS ({count}) ===
{tasks}
=== END TASKS ===
"""


def tasks():
    rows = [r for r in L.read_csv(HERE / "manifest.csv") if r["type"] == "Task"]
    out = []
    for r in rows:
        rec = L.load_yaml(REPO / r["path"])
        out.append({"id": rec["id"], "text": rec["statement"]["en"], "sha": rec["textSha256"], "module": rec["module"],
                    "stem": L.id_to_stem(rec["id"])[len("seed-"):]})
    return sorted(out, key=lambda t: t["id"])


def frame(n, ts):
    order = list(ts)
    random.Random(1000 + n).shuffle(order)
    keyed = [(f"R{n}-{i + 1:03d}", t) for i, t in enumerate(order)]
    lines = "\n".join(f"{k}: {t['text']}" for k, t in keyed)
    prompt = INSTRUCTIONS.format(n=n, codebook=CODEBOOK.read_text(encoding="utf-8"), count=len(keyed), tasks=lines)
    return prompt, {k: t["id"] for k, t in keyed}


def run():
    RAT.mkdir(parents=True, exist_ok=True)
    WORKDIR.mkdir(parents=True, exist_ok=True)
    ts = tasks()
    procs = []
    for n in (1, 2, 3):
        prompt, keymap = frame(n, ts)
        (RAT / f"pass{n}_prompt.txt").write_text(prompt, encoding="utf-8")
        (RAT / f"pass{n}_keymap.json").write_text(json.dumps(keymap, indent=1), encoding="utf-8")
        cmd = ["claude", "-p", "--model", MODEL, "--output-format", "json", "--disallowedTools", *TOOLS_OFF]
        f_out = open(RAT / f"pass{n}_raw.json", "w", encoding="utf-8")
        procs.append((n, subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=f_out, stderr=subprocess.STDOUT, cwd=WORKDIR, text=True), f_out, prompt))
    for n, p, f_out, prompt in procs:
        p.stdin.write(prompt)
        p.stdin.close()
    for n, p, f_out, _ in procs:
        p.wait(timeout=3600)
        f_out.close()
        print(f"pass {n}: exit {p.returncode}")


def _triggers():
    out = []
    for t in L.load_yaml(REPO / "schema" / "lint" / "governed_content.yaml")["tribal_hold"]["triggers"]:
        pat, cs = (t["pattern"], t.get("cs")) if isinstance(t, dict) else (t, False)
        out.append(re.compile(pat, 0 if cs else re.I))
    return out


TRIGGERS = _triggers()


def conf_label(c):
    return "low" if c <= 2 else ("med" if c == 3 else "high")


def write():
    ts = {t["id"]: t for t in tasks()}
    OUT.mkdir(parents=True, exist_ok=True)
    cannot_rows = []
    for n in (1, 2, 3):
        raw = json.loads((RAT / f"pass{n}_raw.json").read_text(encoding="utf-8"))
        model = sorted((raw.get("modelUsage") or {MODEL: {}}).keys(), key=lambda m: "opus" not in m)[0]
        keymap = json.loads((RAT / f"pass{n}_keymap.json").read_text(encoding="utf-8"))
        answers = {}
        for line in raw["result"].splitlines():
            line = line.strip().strip(",")
            if not line.startswith("{"):
                continue
            try:
                a = json.loads(line)
            except json.JSONDecodeError:
                continue
            answers[a.get("k")] = a
        rows = []
        rater = f"emstagent:db-craft-rater-{n}@wp06"
        missing = [k for k in keymap if k not in answers]
        for k, tid in sorted(keymap.items(), key=lambda kv: kv[1]):
            a = answers.get(k)
            t = ts[tid]
            if a is None:
                cannot_rows.append({"pass": n, "task": tid, "reason": "no answer returned"})
                continue
            if a.get("cannot"):
                cannot_rows.append({"pass": n, "task": tid, "reason": a["cannot"]})
                continue
            rec = {"id": f"seed:asm/wp06-db-pass{n}/{t['stem']}", "type": "CraftRating",
                   "prefLabel": {"en": f"WP-06 pass {n} craft rating of {tid}"},
                   "layer": "L5", "module": t["module"], "status": "draft", "license": "CC0-1.0", "sensitivity": "public",
                   "task": tid, "taskTextSha256": t["sha"], "scale": "ordinal-0-2",
                   "values": {"FC": int(a["FC"]), "DC": int(a["DC"]), "SC": int(a["SC"])},
                   "raterType": "llm", "raterId": rater, "assessedAt": ASSESSED,
                   "method": "blind coding per the IO craft codebook; separate model session per pass, task text only, shuffled order, tools disabled",
                   "confidence": conf_label(int(a.get("conf", 3))), "instrument": "emst-craft@0.1",
                   "codebookVersion": CODEBOOK_VERSION, "evidenceLabel": "S", "sources": []}
            if a.get("note") and not any(rx.search(str(a["note"])) for rx in TRIGGERS):
                rec["rationale"] = {"en": str(a["note"])[:200]}   # notes touching held subjects are dropped (ADR-0007 §D)
            rec["provenance"] = {"method": "llm-assisted", "agent": [rater], "generatedAt": GEN_AT, "evidenceLabel": "S",
                                 "reviewStatus": "unreviewed", "toolVersion": model, "promptVersion": PROMPT_VERSION,
                                 "adr": ["ADR-0005", "ADR-0024"]}
            rows.append(rec)
        L.write_jsonl(OUT / f"wp06-db-pass{n}.jsonl", rows)
        print(f"pass {n}: {len(rows)} ratings written, {len(missing)} missing answers, model {model}")
    with open(RAT / "cannot_code.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["pass", "task", "reason"])
        w.writeheader()
        w.writerows(cannot_rows)
    print(f"cannot-code or missing: {len(cannot_rows)}")


if __name__ == "__main__":
    {"run": run, "write": write}[sys.argv[1]]()
