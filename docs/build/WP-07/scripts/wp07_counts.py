#!/usr/bin/env python3
"""Generate WP-07 counts from the records on disk (never typed by hand). Usage: python3 docs/build/WP-07/scripts/wp07_counts.py"""
import collections
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402

AGENT = "emstagent:lc-agent@wp-07"
c = collections.Counter()
clusters = collections.Counter()
ena_kinds = collections.Counter()
task_kind = collections.Counter()
cred_ver = collections.Counter()
for loc, rec in L.iter_records(REPO / "data" / "v2"):
    if not isinstance(rec, dict):
        continue
    agents = (rec.get("provenance") or {}).get("agent") or []
    t = rec.get("type")
    if t == "CraftRating" and str(rec.get("raterId", "")).startswith("emstagent:lc-craft-rater-"):
        c["CraftRating"] += 1
        continue
    if AGENT not in agents:
        continue
    c[t] += 1
    if t == "Competency":
        clusters[rec.get("transversalCluster")] += 1
    elif t == "Enactment":
        ena_kinds[rec.get("enactmentKind")] += 1
    elif t == "Task":
        task_kind["v1 seed rewritten in place" if str(rec["id"]).startswith("seed:v1-") else "new"] += 1
    elif t == "Credential":
        cred_ver["issuer-verified" if rec["issuerVerified"]["verified"] else "unverified"] += 1
x10 = [ln.split("\t") for ln in (REPO / "data/v2/crosswalks/emst-x10-evidence-equivalence/2.0.0-draft.sssom.tsv").read_text().splitlines()[1:]]
prov = list(csv.DictReader(open(REPO / "docs/build/WP-07/formation_provisions.csv", encoding="utf-8")))
paths = list((REPO / "docs/build/WP-07/staging/pathways").glob("*.yaml"))
steps = sum(len(L.load_yaml(p).get("sequence", [])) for p in paths)
out = {"records_by_type": dict(sorted(c.items())), "competencies_by_cluster": dict(sorted(clusters.items())),
       "enactments_by_kind": dict(ena_kinds), "tasks": dict(task_kind), "credentials": dict(cred_ver),
       "x10_rows": len(x10), "x10_negated": sum(1 for r in x10 if r[3] == "Not"),
       "pathways_staged": len(paths), "pathway_steps": steps, "formation_provisions": len(prov),
       "formation_by_response": dict(collections.Counter(r["response"] for r in prov))}
print(json.dumps(out, indent=1))
