#!/usr/bin/env python3
"""Generated counts for WP-08 views (never typed). Output: docs/build/WP-08/generated/counts.json. Licence: Apache-2.0."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viewlib as V  # noqa: E402

o = V.OUT
fed = json.loads((o / "federal-series" / "federal_variant_index.json").read_text())["variants"]
sc = json.loads((o / "state-class" / "variant_index.json").read_text())["variants"]
fam = json.loads((o / "job_families.json").read_text())
mir = json.loads((o / "mirror_links.json").read_text())
cv = list((o / "change_view").glob("R*.json"))
counts = {
    "federalSeriesProfiles": len(list((o / "federal-series").glob("[0-9]*.json"))),
    "federalSeriesProposedRealignment": sum(1 for p in (o / "federal-series").glob("[0-9]*.json")
                                            if json.loads(p.read_text())["series"]["seriesStatus"] == "proposed-realignment"),
    "federalVariantsIndexed": len(fed), "federalVariantsWithSeries": sum(1 for v in fed.values() if v),
    "stateClassViews": len(list((o / "state-class").glob("*--*.json"))),
    "stateLocalVariantsIndexed": len(sc), "stateLocalVariantsWithClass": sum(1 for v in sc.values() if v),
    "jobFamilies": len(fam["families"]), "familyMemberships": sum(len(f["members"]) for f in fam["families"]),
    "rolesWithoutFamily": len(fam["unassigned"]),
    "mirrorPairs": len(mir["pairs"]), "mirrorAcceptanceChecksPassed": sum(c["linked"] for c in mir["acceptanceChecks"]),
    "changeViews": len(cv),
    "changeViewTaskClaims": sum(sum(len(t["change"]) for t in json.loads(p.read_text())["tasks"]) for p in cv),
}
V.write_json(o / "counts.json", counts)
print(json.dumps(counts, indent=1))
