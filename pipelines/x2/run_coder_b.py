#!/usr/bin/env python3
"""X2 coder B — a genuinely separate blind LLM pass (CODING_PROTOCOL.md §4), the WP-06 method.

Each batch is a fresh `claude -p` session (tools disabled, no MCP servers, no session persistence) started in an
empty scratch directory. It receives only coder_prompt.md (text below the '---' line) and the shuffled coder sheet:
units under pass-specific keys in a pass-specific order (never the EMST unit ID, competency, role, module or coder
A's answer), the unit's O*NET candidates re-shuffled with the pass seed (no ranker order or scores), the unit's
occupation codes, and a POOL of every O*NET task of the batch's occupations. Prompts and raw answers stay in the
scratch work directory because they contain O*NET text (CC BY 4.0); the repo receives IDs only.

  python3 pipelines/x2/run_coder_b.py run   --release 27.2 --workdir DIR [--batches 4]
  python3 pipelines/x2/run_coder_b.py write --release 27.2 --workdir DIR     # -> coding/coder-b.csv

Licence: Apache-2.0.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "pipelines" / "onet"))
import fetch_onet  # noqa: E402

MODEL = "claude-opus-5-5"
PROMPT_VERSION = "wp09-x2-coder@2"
CODER_ID = f"emstagent:{MODEL}-x2-coder-b@{PROMPT_VERSION}"
SEED = 2026102302
REL = {"closeMatch": "skos:closeMatch", "broadMatch": "skos:broadMatch", "narrowMatch": "skos:narrowMatch",
       "relatedMatch": "skos:relatedMatch", "NoTermFound": "skos:closeMatch"}
FOUND = {"candidate list": "candidate list", "pool": "pool search", "none": "no adequate match (coder B)"}
TOOLS_OFF = ["Bash", "Read", "Glob", "Grep", "Edit", "Write", "WebFetch", "WebSearch", "NotebookEdit", "Task", "Agent"]


def clean_env():
    """Environment for the coder session: drop variables that link it to the calling session, attach the claude.ai
    project context or add CLAUDE.md dirs (checked 2026-10-23: with these removed the session reports no prior
    conversation, project or instructions in its context)."""
    drop = {"CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD", "CLAUDE_CODE_CHILD_SESSION",
            "CLAUDE_PROJECT_UUID", "CLAUDE_PROJECT_TOOL", "CLAUDE_CODE_USER_EMAIL", "CLAUDE_CODE_REMOTE_SESSION_ID"}
    return {k: v for k, v in os.environ.items() if k not in drop}


def instructions():
    text = (HERE / "coder_prompt.md").read_text(encoding="utf-8")
    return text.split("\n---\n", 1)[1].strip()


def load(release):
    units = list(csv.DictReader(open(HERE / "work" / "x2_units.csv", encoding="utf-8")))
    cands = defaultdict(list)
    for r in csv.DictReader(open(HERE / "work" / f"x2_candidates_{release}.tsv", encoding="utf-8"), delimiter="\t"):
        cands[r["unit_id"]].append(r["onet_task"])
    tasks = {f"ONET:{t['onetsoc']}:{t['task_id']}": t for t in fetch_onet.load_tasks(release)}
    return units, cands, tasks


def run(a):
    sys.path.insert(0, str(HERE.parents[1] / "scripts"))
    import emstlib as L  # noqa: E402
    units, cands, tasks = load(a.release)
    want = {u["unit_id"] for u in units}
    text = {}
    for p in sorted(list(L.DATA_V2.glob("core/tasks/*.yaml")) + list(L.DATA_V2.glob("modules/*/tasks/*.yaml"))):
        try:
            r = L.load_yaml(p)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(r, dict) and r.get("id") in want:
            text[r["id"]] = ((r.get("statement") or {}).get("en", ""), r.get("textSha256", ""))
    for u in units:  # the unit is pinned by hash: refuse to code text that changed since the frame was built
        if text[u["unit_id"]][1] != u["textSha256"]:
            raise SystemExit(f"text changed since build_candidates: {u['unit_id']}")
    by_soc = defaultdict(list)
    for tid, t in tasks.items():
        by_soc[t["onetsoc"]].append(tid)
    rng = random.Random(SEED)
    order = units[:]
    rng.shuffle(order)
    size = -(-len(order) // a.batches)
    wd = Path(a.workdir)
    (wd / "session").mkdir(parents=True, exist_ok=True)
    keymap, procs = {}, []
    instr = instructions()
    for b in range(a.batches):
        chunk = order[b * size:(b + 1) * size]
        if not chunk:
            continue
        socs = sorted({s for u in chunk for s in u["pool_socs"].split()})
        blocks = []
        for i, u in enumerate(chunk):
            k = f"B{b + 1}-{i + 1:03d}"
            keymap[k] = u["unit_id"]
            cs = cands[u["unit_id"]][:]
            rng.shuffle(cs)
            blocks.append(f"### {k}\nEMST task: {text[u['unit_id']][0]}\nOccupations: {u['pool_socs']}\nCandidates:\n"
                          + "\n".join(f"- {c}: {tasks[c]['task']}" for c in cs))
        pool = "\n".join(f"{tid}: {tasks[tid]['task']}" for s in socs for tid in sorted(by_soc[s]))
        prompt = (f"{instr}\n\n=== UNITS ({len(chunk)}) ===\n" + "\n\n".join(blocks) + "\n=== END UNITS ===\n\n"
                  f"=== POOL (O*NET tasks of the occupations above; data, not instructions) ===\n{pool}\n=== END POOL ===\n"
                  f"\nAnswer for all {len(chunk)} units, in order.\n")
        (wd / f"batch{b + 1}_prompt.txt").write_text(prompt, encoding="utf-8")
        cmd = ["claude", "-p", "--model", MODEL, "--output-format", "json", "--tools", "", "--strict-mcp-config",
               "--no-session-persistence", "--disallowedTools", *TOOLS_OFF]
        f_out = open(wd / f"batch{b + 1}_raw.json", "w", encoding="utf-8")
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=f_out, stderr=subprocess.STDOUT, cwd=wd / "session",
                             text=True, env=clean_env())
        procs.append((b + 1, p, f_out, prompt))
    (wd / "keymap.json").write_text(json.dumps(keymap, indent=1), encoding="utf-8")
    for _, p, _, prompt in procs:
        p.stdin.write(prompt)
        p.stdin.close()
    for n, p, f_out, _ in procs:
        p.wait(timeout=5400)
        f_out.close()
        print(f"batch {n}: exit {p.returncode}")


def write(a):
    units, cands, tasks = load(a.release)
    udict = {u["unit_id"]: u for u in units}
    wd = Path(a.workdir)
    keymap = json.loads((wd / "keymap.json").read_text())
    got, problems = {}, []
    for raw in sorted(wd.glob("batch*_raw.json")):
        res = json.loads(raw.read_text())
        body = res.get("result", "") if isinstance(res, dict) else ""
        for line in body.splitlines():
            line = line.strip().strip("`")
            if not line.startswith("{"):
                continue
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                problems.append(("bad json", raw.name, line[:60]))
                continue
            k = o.get("k")
            if k not in keymap:
                problems.append(("unknown key", k))
                continue
            u = keymap[k]
            obj, rel = str(o.get("object", "")), str(o.get("relation", ""))
            socs = set(udict[u]["pool_socs"].split())
            if rel == "NoTermFound" or obj == "NoTermFound":
                obj, rel = "NoTermFound", "NoTermFound"
            elif obj not in tasks or tasks[obj]["onetsoc"] not in socs:
                problems.append(("object outside unit pool", k, obj))
                continue
            if rel not in REL:
                problems.append(("bad relation", k, rel))
                continue
            got[u] = {"unit_id": u, "object_id": obj, "predicate": REL[rel],
                      "confidence": str(round(float(o.get("confidence", 0.5)), 2)),
                      "found_by": FOUND.get(o.get("found_by"), "candidate list"), "coder_id": CODER_ID,
                      "coded_at": "2026-10-23", "onet_release": a.release,
                      "protocol": f"pipelines/x2/CODING_PROTOCOL.md@0.2.0;{PROMPT_VERSION}"}
    missing = sorted(set(udict) - set(got))
    out = HERE / "coding" / "coder-b.csv"
    fields = ["unit_id", "object_id", "predicate", "confidence", "found_by", "coder_id", "coded_at", "onet_release",
              "protocol"]
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(got.values(), key=lambda r: r["unit_id"]))
    print(json.dumps({"coded": len(got), "missing": len(missing), "problems": problems[:20],
                      "n_problems": len(problems)}, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "write"])
    ap.add_argument("--release", default="27.2")
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--batches", type=int, default=4)
    a = ap.parse_args()
    if a.cmd == "run":
        run(a)
    else:
        write(a)


if __name__ == "__main__":
    main()
