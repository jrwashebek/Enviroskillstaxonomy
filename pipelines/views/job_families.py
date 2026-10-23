#!/usr/bin/env python3
"""Job-family membership (navigation only) under the proposed rule job-family-membership@0.1.0.
Membership is computed here and never stored on RoleProfile or JobFamily records (ADR-0006 section 5; ADR-0021).
Output: docs/build/WP-08/generated/job_families.json. Licence: Apache-2.0."""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import viewlib as V  # noqa: E402

GEN = "pipelines/views/job_families.py@0.1.0"
RULE = V.L.load_yaml(HERE / "rules" / "job-family-membership@0.1.0.yaml")


def main():
    d = V.Data()
    p = RULE["parameters"]
    excl = set(p["excludeTargets"])
    fams = {fid: d.get(fid) for fid in p["families"]}
    missing = [f for f, r in fams.items() if r is None]
    if missing:
        raise SystemExit(f"rule names families that do not exist: {missing}")
    out = {fid: [] for fid in fams}
    assigned = set()
    for role in d.roles():
        tg = [t for t in role.get("competencyTargets") or [] if t["competency"] not in excl]
        tot = sum(t.get("importance", 1) for t in tg) or 1
        for fid, spec in p["families"].items():
            anchors = set(spec["anchors"])
            share = sum(t.get("importance", 1) for t in tg if t["competency"] in anchors) / tot
            in_mod = role.get("homeModule") in set(spec.get("modules") or [])
            basis = None
            if share >= p["minShare"]:
                basis = "anchor share"
            elif in_mod and share >= p["minShareInModule"]:
                basis = "home module and anchor share"
            if basis:
                out[fid].append({"role": role["id"], "roleTitle": d.label(role["id"]), "share": round(share, 3),
                                 "basis": basis, "whatsComing": role.get("lifecycleState") in ("proposed", "emerging")})
                assigned.add(role["id"])
    res = {"stamp": V.stamp(RULE["ruleId"], RULE["version"], GEN),
           "note": "Navigation only; not a classification or a career-ladder claim. Shares are over agent-draft target importances.",
           "families": [{"family": fid, "label": d.label(fid), "members": sorted(m, key=lambda x: -x["share"])}
                        for fid, m in out.items()],
           "unassigned": sorted(r["id"] for r in d.roles() if r["id"] not in assigned)}
    V.write_json(V.OUT / "job_families.json", res)
    print({d.label(f): len(m) for f, m in out.items()}, "unassigned:", res["unassigned"])


if __name__ == "__main__":
    main()
