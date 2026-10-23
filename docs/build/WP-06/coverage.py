#!/usr/bin/env python3
"""Generate docs/build/WP-06/three_module_coverage.csv: for every live core competency, the wave-1 modules in which a
module Enactment (any author) enacts it, and the three-module status (ADR-0003 G-4; ADR-0018 home-module rule).
Computed from data/v2 on each run; counts here are generated, never typed into records."""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402

DATA = REPO / "data" / "v2"
WAVE1 = ["water", "waterq", "air", "waste", "envhealth", "hazards", "forest", "wildlife", "parks"]


def main():
    enacted = defaultdict(set)
    for p in (DATA / "modules").glob("*/enactments/*.yaml"):
        r = L.load_yaml(p)
        if r.get("enactmentKind") == "module" and r.get("status") not in ("superseded", "withdrawn"):
            enacted[r["competency"]].add(r["enactedInModule"])
    rows = []
    for p in sorted((DATA / "core" / "competencies").glob("*.yaml")):
        r = L.load_yaml(p)
        if r.get("status") in ("superseded", "withdrawn") or r.get("indigenousDataFlag"):
            continue
        mods = sorted(m for m in enacted.get(r["id"], set()) if m in WAVE1)
        ctype = r.get("competencyType", "")
        if r.get("validationStatus") == "seed-v1":
            status = "unauthored-seed"
        elif ctype == "transversal" or r.get("transversalCluster"):
            status = "transversal (enacted by craft/actor/module; rule applies to its task core)"
        elif len(mods) >= 3:
            status = "meets-three-module-rule-in-wave-1"
        else:
            status = "below-three-in-wave-1 (wave-2 module enactments or a recorded CA exception needed)"
        rows.append({"competency": r["id"], "prefLabel": r["prefLabel"]["en"], "competencyType": ctype,
                     "wave1_modules": "|".join(mods), "n_wave1_modules": str(len(mods)), "status": status})
    out = HERE / "three_module_coverage.csv"
    out.write_text(L.csv_text(list(rows[0].keys()), rows), encoding="utf-8")
    print(f"wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
