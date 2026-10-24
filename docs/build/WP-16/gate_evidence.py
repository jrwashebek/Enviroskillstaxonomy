#!/usr/bin/env python3
"""Generate the numbers the rc.1 gate report cites (build plan §5; WP-16 Step 3). Read-only over dist/<version>/, the
claims register and the WP-15 sign-off; writes generated/gate_evidence.json. Nothing in the gate report is typed.
Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402
from rules import hr_common as H  # noqa: E402

VERSION = sys.argv[1] if len(sys.argv) > 1 else "2.0.0-rc.1"
DIST = ROOT / "dist" / VERSION
WAVE1 = ["air", "envhealth", "forest", "hazards", "parks", "waste", "water", "waterq", "wildlife"]
EARLY = {"extract", "worklands"}
X = {"X1": "emst-v1", "X2": "onet-task", "X3": "onet-soc|soc", "X4": "opm-series", "X5": "state-class-|local-class-",
     "X7": "esco", "X12": "dol-ai-literacy"}


def other(s):
    return dict(x.split("=", 1) for x in str(s or "").split(";") if "=" in x)


def main():
    bundle = json.loads((DIST / "emst.bundle.jsonld").read_text(encoding="utf-8"))
    graph = bundle["@graph"]
    recs = {r["id"]: r for r in graph if isinstance(r, dict) and "id" in r and r.get("type") not in ("Mapping",)}
    maps = [r for r in graph if isinstance(r, dict) and r.get("type") == "Mapping"]
    view = lambda p: json.loads((DIST / "views" / p).read_text(encoding="utf-8"))  # noqa: E731
    counts = view("counts.json")
    ev = {"version": VERSION, "counts": {k: counts[k] for k in ("byType", "competenciesByKind", "competenciesByModule",
                                                               "competenciesByLifecycle", "rolesByTier", "variantsBySectorActor",
                                                               "coreCompetencies", "heldRecords", "excluded", "redactedReferences",
                                                               "deferredTargets") if k in counts}}
    # item 2: core size (released core + held core reported as a count)
    notes = (DIST / "RELEASE_NOTES.md").read_text(encoding="utf-8")
    ev["item2_coreSizeLine"] = next((ln for ln in notes.splitlines() if ln.startswith("Core competencies:")), None)
    # item 3: use tiers, select, display gate
    eut = view("effective_use_tier.json")["rows"]
    gate = view("display_gate.json")["rows"]
    ev["item3"] = {
        "effectiveUseTierRows": len(eut), "effectiveUseTier": dict(Counter(r["effectiveUseTier"] for r in eut)),
        "elementsWithoutEffectiveTier": sorted({r["type"] for r in recs.values() if r.get("type") in
                                                ("Competency", "Task", "Indicator", "Enactment", "RoleProfile", "RoleVariant",
                                                 "KnowledgeStatement", "Pathway")} - {r["type"] for r in eut}),
        "selectAnywhere": sum(1 for r in recs.values() if "select" in (r.get("useTier"), r.get("useClass")))
        + sum(1 for r in eut if r["effectiveUseTier"] == "select"),
        "displayGateRows": len(gate), "displayGateDecisions": dict(Counter(r["decision"] for r in gate)),
        "displayGateRule": view("display_gate.json")["header"].get("ruleVersion")}
    # item 4: modules
    mods = Counter((r.get("module") or "core") for r in recs.values())
    ev["item4"] = {"wave1Present": {m: mods.get(m, 0) for m in WAVE1},
                   "otherModules": {m: n for m, n in sorted(mods.items()) if m not in WAVE1 and m != "core"},
                   "earlyDraftLabels": sorted({(r.get("prefLabel") or {}).get("en", "") for r in recs.values()
                                               if r.get("module") in EARLY and r.get("type") in ("Competency", "RoleProfile")})}
    # item 5: roles at tier depth; FSP and SCV coverage of P1-P2 federal and state variants
    roles = [r for r in recs.values() if r.get("type") == "RoleProfile"]
    depth = []
    for r in sorted(roles, key=lambda x: x["id"]):
        t = H.tier(r)
        ntask = len({i.get("task") for i in (r.get("taskBundle") or r.get("tasks") or []) if isinstance(i, dict)})
        ntarget = len(r.get("competencyTargets") or [])
        depth.append({"role": r["id"], "label": (r.get("prefLabel") or {}).get("en"), "tier": t, "tasks": ntask,
                      "targets": ntarget, "lifecycle": r.get("lifecycleState"), "reviewBy": r.get("reviewBy"),
                      "counterSignal": bool(r.get("counterSignal") or r.get("namedCounterSignal"))})
    rule = {"P1": (15, 40, 6, 12), "P2": (15, 40, 6, 10)}
    short = [d for d in depth if d["tier"] in rule and not (rule[d["tier"]][0] <= d["tasks"] <= rule[d["tier"]][1]
                                                            and rule[d["tier"]][2] <= d["targets"])]
    fsp_idx = view("federal_series_profiles/index.json")["series"]
    fsp_roles = {x for s in fsp_idx for x in s["roles"]}
    scv_idx = view("state_class_views/index.json")["variants"]
    p12 = [r for r in roles if H.tier(r) in ("P1", "P2")]
    fed = [(r["id"], v["id"]) for r in p12 for v in [H.variant_for(recs, r["id"], "federal")] if v]
    sta = [(r["id"], v["id"]) for r in p12 for v in [H.variant_for(recs, r["id"], "state")] if v]
    ev["item5"] = {"roles": len(roles), "byTier": dict(Counter(d["tier"] for d in depth)),
                   "p1p2OutsideDepthRule": short, "depthRule": "P1/P2: 15-40 tasks and at least 6 competency targets",
                   "p1p2FederalVariants": len(fed), "p1p2FederalVariantsInAnFsp": sum(1 for r, _ in fed if r in fsp_roles),
                   "p1p2FederalVariantsWithoutFsp": [r for r, _ in fed if r not in fsp_roles],
                   "fspFiles": len(fsp_idx),
                   "p1p2StateVariants": len(sta), "p1p2StateVariantsIndexed": sum(1 for _, v in sta if v in scv_idx),
                   "p1p2StateVariantsWithAClassView": sum(1 for _, v in sta if scv_idx.get(v)),
                   "scvFiles": len([p for p in (DIST / "views" / "state_class_views").glob("*.json") if p.name != "index.json"]),
                   "depth": depth}
    # item 6: crosswalks
    xw = {}
    for code, pref in X.items():
        rows = [m for m in maps if any(m.get("mapping_set_id", "").startswith(p) for p in pref.split("|"))]
        rs = Counter(other(m.get("other")).get("review_status", "(none)") for m in rows)
        rt = Counter(other(m.get("other")).get("rater_type", "(none)") for m in rows)
        just = Counter(m.get("mapping_justification") for m in rows)
        xw[code] = {"rows": len(rows), "reviewStatus": dict(rs), "raterType": dict(rt), "justification": dict(just),
                    "humanReviewed": sum(1 for m in rows if str(other(m.get("other")).get("reviewer", "")).startswith("pid:"))}
    x1 = [m for m in maps if m.get("mapping_set_id", "").startswith("emst-v1")]
    xw["X1"]["subjects"] = len({m["subject_id"] for m in x1})
    ev["item6"] = xw
    # item 7: claims register and sign-off
    reg = list(csv.DictReader(open(ROOT / "docs" / "methods" / "claims_register.csv", encoding="utf-8", newline="")))
    today = "2026-10-23"
    ev["item7"] = {"registerRows": len(reg), "byStatus": dict(Counter(r["status"] for r in reg)),
                   "unverifiedOrHeld": [r["claim_id"] for r in reg if r["status"] in ("unverified", "held")],
                   "recheckBy": dict(sorted(Counter(r["recheck_by"] for r in reg).items())),
                   "recheckOnOrBeforeToday": sum(1 for r in reg if r["recheck_by"][:4].isdigit() and r["recheck_by"] <= today),
                   "signoffStatusLine": next((ln for ln in (ROOT / "docs" / "methods" / "WP15_SIGNOFF.md").read_text(encoding="utf-8").splitlines()
                                              if ln.startswith("- **Owner:**")), None),
                   "acr": (ROOT / "site" / "ACR.md").exists(), "securityPacket": (ROOT / "site" / "SECURITY_PACKET.md").exists()}
    out = HERE / "generated" / "gate_evidence.json"
    out.write_text(json.dumps(ev, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    slim = {k: v for k, v in ev.items() if k not in ("counts",)}
    slim["item5"] = {k: v for k, v in ev["item5"].items() if k != "depth"}
    print(json.dumps(slim, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
