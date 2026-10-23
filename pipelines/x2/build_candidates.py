#!/usr/bin/env python3
"""X2 step 1 — build the P1 task frame, its O*NET candidate pools and machine candidates (ADR-0022 X2).

Units: live, non-held v2 tasks in p1_frame.yaml#taskToP1Roles (WP-08 P1 bundles), pinned by textSha256. Pool per unit: O*NET tasks
of the O*NET-SOC codes X3 maps to the unit's P1 roles. Candidates: emst_linker hybrid index over the pool, top-K.
Outputs (IDs and scores only; O*NET text never enters the repo):
  pipelines/x2/work/x2_units.csv                      unit_id, competency, roles, textSha256, pool size
  pipelines/x2/work/x2_candidates_<rel>.tsv           unit_id, rank, onet_task (ONET:<soc>:<task id>), score
  --sheet PATH (outside the repo)                     coder sheet WITH O*NET task text, for blind coders
Usage: EMST_ONET_CACHE=... python pipelines/x2/build_candidates.py --release 27.2 [--k 8] [--sheet OUT.csv]
Licence: Apache-2.0.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "pipelines" / "linker"))
sys.path.insert(0, str(ROOT / "pipelines" / "onet"))
sys.path.insert(0, str(ROOT / "pipelines" / "crosswalks"))
import emstlib as L  # noqa: E402
import fetch_onet  # noqa: E402
import sssomlib as S  # noqa: E402
from emst_linker import corpus  # noqa: E402
from emst_linker.index import HybridIndex  # noqa: E402

WORK = HERE / "work"


def role_pools():
    pools = defaultdict(set)
    for r in S.read_set(S.XW / "onet-soc" / "2019.sssom.tsv"):
        if r.get("predicate_modifier") == "Not" or r["object_id"] == S.NO_TERM:
            continue
        rk = r["subject_id"].split(":", 1)[1].split("/")[0]
        pools[rk[:3]].add(r["object_id"].split(":", 1)[1])
    return pools


def p1_units(frame):
    """Units = exactly the tasks in p1_frame.yaml#taskToP1Roles (WP-08 P1 bundles; frame >= 0.2.0).

    Roles come from the frame entry for the task, not from its competency. Held, superseded or withdrawn tasks are
    dropped and reported. `competency` is the task's first `supports` competency (for reporting only).
    """
    held = corpus.held_keys()
    units, seen = [], set()
    for p in sorted(list(L.DATA_V2.glob("core/tasks/*.yaml")) + list(L.DATA_V2.glob("modules/*/tasks/*.yaml"))):
        try:
            r = L.load_yaml(p)
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(r, dict) or r.get("id") not in frame:
            continue
        seen.add(r["id"])
        if r.get("status") in ("superseded", "withdrawn") or corpus.is_held(r, held):
            continue
        sup = [(s.get("competency") or "") for s in (r.get("supports") or [])]
        units.append({"unit_id": r["id"], "competency": sup[0] if sup else "", "roles": sorted(frame[r["id"]]),
                      "text": (r.get("statement") or {}).get("en", ""), "textSha256": r.get("textSha256", ""),
                      "module": r.get("module")})
    missing = sorted(set(frame) - seen)
    return units, missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", default="27.2")
    ap.add_argument("--k", type=int, default=8)
    ap.add_argument("--sheet")
    ap.add_argument("--seed", type=int, default=20261023)
    a = ap.parse_args()
    fdoc = L.load_yaml(HERE / "p1_frame.yaml")
    if "taskToP1Roles" not in fdoc:
        raise SystemExit("p1_frame.yaml has no taskToP1Roles (frame < 0.2.0); regenerate it from the WP-08 bundles")
    frame = fdoc["taskToP1Roles"]
    frame_sha = L.sha256_file(HERE / "p1_frame.yaml")
    onet = fetch_onet.load_tasks(a.release)
    by_soc = defaultdict(list)
    for t in onet:
        by_soc[t["onetsoc"]].append(t)
    pools = role_pools()
    units, missing = p1_units(frame)
    WORK.mkdir(exist_ok=True)
    cand_rows, sheet_rows = [], []
    rng = random.Random(a.seed)
    for u in units:
        socs = sorted(set().union(*[pools.get(r, set()) for r in u["roles"]]))
        pool = [t for s in socs for t in by_soc.get(s, [])]
        u["pool_socs"] = " ".join(socs)
        u["pool_size"] = len(pool)
        if not pool:
            continue
        idx = HybridIndex([t["task"] for t in pool], [f"ONET:{t['onetsoc']}:{t['task_id']}" for t in pool], semantic="none")
        order, Sc, raw = idx.rank([u["text"]], min(a.k, len(pool)))
        cands = [(r, idx.ids[j], round(float(Sc[0, j]), 4), pool[j]) for r, j in enumerate(order[0], 1)]
        for r, oid, sc, t in cands:
            cand_rows.append({"unit_id": u["unit_id"], "rank": r, "onet_task": oid, "score": sc})
        shuffled = cands[:]
        rng.shuffle(shuffled)      # coders see candidates in random order, without scores (blind to the ranker)
        for _, oid, _, t in shuffled:
            sheet_rows.append({"unit_id": u["unit_id"], "emst_task": u["text"], "onet_task": oid, "onet_soc": t["onetsoc"],
                               "onet_task_text": t["task"], "onet_task_type": t["task_type"]})
    with open(WORK / "x2_units.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["unit_id", "competency", "roles", "module", "textSha256", "pool_socs", "pool_size"])
        w.writeheader()
        for u in units:
            w.writerow({k: (" ".join(u[k]) if k == "roles" else u.get(k, "")) for k in w.fieldnames})
    with open(WORK / f"x2_candidates_{a.release}.tsv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["unit_id", "rank", "onet_task", "score"], delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(cand_rows)
    if a.sheet:
        with open(a.sheet, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(sheet_rows[0]))
            w.writeheader()
            w.writerows(sheet_rows)
    (WORK / "x2_frame.json").write_text(json.dumps({"frameVersion": fdoc.get("frameVersion"), "frame_sha256": frame_sha,
        "frame_tasks": len(frame), "units": len(units), "missing_or_dropped": missing, "release": a.release,
        "k": a.k, "seed": a.seed}, indent=1) + "\n")
    print(json.dumps({"frameVersion": fdoc.get("frameVersion"), "frame_tasks": len(frame), "missing": len(missing),
                      "units": len(units), "units_with_pool": sum(1 for u in units if u.get("pool_size")),
                      "candidate_rows": len(cand_rows), "release": a.release,
                      "pool_size_median": sorted(u.get("pool_size", 0) for u in units)[len(units) // 2] if units else 0}, indent=1))


if __name__ == "__main__":
    main()
