#!/usr/bin/env python3
"""Generated counts for the WP-05 hand-back (never typed). Output: generated/wp05_counts.json. Licence: Apache-2.0."""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402


def main():
    written = set(json.loads((HERE / "generated" / "wp05_written.json").read_text())["records"])
    recs = {}
    for _loc, rec in L.iter_records(L.DATA_V2):
        if isinstance(rec, dict) and rec.get("id") in written:
            recs[rec["id"]] = rec
    ratings = []
    for p in (L.DATA_V2 / "assessments" / "emst-craft@0.1").glob("wp05-sc-pass*.jsonl"):
        ratings += [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    by_type = collections.Counter(r["type"] for r in recs.values())
    comps = [r for r in recs.values() if r["type"] == "Competency"]
    tasks = [r for r in recs.values() if r["type"] == "Task"]
    enas = [r for r in recs.values() if r["type"] == "Enactment"]
    inds = [r for r in recs.values() if r["type"] == "Indicator"]
    per_comp = collections.Counter(s["competency"] for t in tasks for s in t["supports"] if s["strength"] == "primary")
    out = {
        "recordsByType": dict(sorted(by_type.items())),
        "craftRatings": len(ratings),
        "ratingPasses": len({r["raterId"] for r in ratings}),
        "competenciesByType": dict(collections.Counter(c["competencyType"] for c in comps)),
        "competenciesEditedV1Seeds": sum(1 for c in comps if c["id"].startswith("seed:v1-")),
        "competenciesFromCandidates": sum(1 for c in comps if not c["id"].startswith("seed:v1-")),
        "tasksRewrittenV1Seeds": sum(1 for t in tasks if t["id"].startswith("seed:v1-")),
        "tasksNew": sum(1 for t in tasks if not t["id"].startswith("seed:v1-")),
        "minPrimaryTasksPerCompetency": min(per_comp.get(c["id"], 0) for c in comps),
        "indicatorsByMode": dict(collections.Counter(i["augmentationMode"] for i in inds)),
        "indicatorsObs4": dict(collections.Counter(str(i["obs4"]) for i in inds)),
        "enactmentsByAuthorityPosition": dict(collections.Counter(e.get("authorityPosition", "(unset)") for e in enas)),
        "enactmentsByActorFamily": dict(collections.Counter(e["actorType"] for e in enas)),
        "enactmentsLinkingRegisteredInstruments": sum(1 for e in enas if e.get("characteristicInstruments")),
        "enactmentsSlReviewed": sum(1 for e in enas if "emstagent:a5-sl-review@wp-05" in e["provenance"]["agent"]),
        "competenciesWithSensitivityEdges": sum(1 for c in comps if c.get("instrumentSensitivity")),
        "tribalRecordsAuthored": sum(1 for r in recs.values() if r.get("indigenousDataFlag")),
        "lifecycleEmerging": sorted(c["id"] for c in comps if c.get("lifecycleState") == "emerging"),
    }
    (HERE / "generated" / "wp05_counts.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
