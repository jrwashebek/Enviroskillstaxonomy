#!/usr/bin/env python3
"""Print WP-06 counts generated from docs/build/WP-06/manifest.csv, the records and the rating batches (never typed)."""
import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402
rows = list(csv.DictReader(open(HERE / "manifest.csv", encoding="utf-8")))
by = defaultdict(Counter)
for r in rows:
    by[r["module"]][r["type"]] += 1
types = ["Competency", "Task", "Indicator", "Enactment"]
print("module," + ",".join(types))
for m in sorted(by):
    print(m + "," + ",".join(str(by[m][t]) for t in types))
print("TOTAL," + ",".join(str(sum(by[m][t] for m in by)) for t in types))
print("origin:", dict(Counter((r["type"], r["origin"]) for r in rows)))
life = Counter(); gates = 0; moved = 0
for r in rows:
    rec = L.load_yaml(REPO / r["path"])
    if r["type"] == "Competency":
        life[rec.get("lifecycleState")] += 1
    if r["type"] == "Task" and rec.get("credentialGates"):
        gates += 1
    if r["origin"].endswith("+moved"):
        moved += 1
print("competency lifecycle:", dict(life), "| tasks with credential gates:", gates)
ratings = {}
for n in (1, 2, 3):
    p = REPO / "data/v2/assessments/emst-craft@0.1" / f"wp06-db-pass{n}.jsonl"
    ratings[n] = sum(1 for _ in open(p, encoding="utf-8")) if p.exists() else 0
print("craft ratings per pass:", ratings)
cov = list(csv.DictReader(open(HERE / "three_module_coverage.csv", encoding="utf-8")))
enacted = [c for c in cov if int(c["n_wave1_modules"]) > 0]
print("core competencies with wave-1 module enactments:", len(enacted), "| of which in >=3 modules:", sum(1 for c in enacted if int(c["n_wave1_modules"]) >= 3))
print("module briefs:", len(list((REPO / "docs/modules").glob("MOD-*.md"))))
