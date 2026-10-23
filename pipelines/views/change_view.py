#!/usr/bin/env python3
"""Role-change view inputs for the 13 P1 roles (View 1 "How is this role changing?"; ADR-0027 section 1-2; WP-08).

Joins WP-08's authored change atoms (docs/build/WP-08/change_view_inputs.yaml: which tasks are being reshaped and by
which driver, agent drafts) with the evidence the explorer must show beside them:
- v2 assessment status per task: "assessment pending" unless a v2 multi-rater ExposureAssessment exists;
- change signals (L5): those named on the atom, plus signals targeting the role, its variants' sector actors and its
  editorial primary work function; status (watch/active), family, drivers, reliability. Change indicators count
  active signals only (ADR-0028); none are active, so no indicator moves;
- external occupation-level context attached through X3 (labelled, never task-level; licence excludes it from release);
- v1 prior evidence pointers (evidence drawer only, never a value).
Held signals and records are never read. Output: docs/build/WP-08/generated/change_view/<role_key>.json and summary.csv.
Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viewlib as V  # noqa: E402

GEN = "pipelines/views/change_view.py@0.1.0"
ATOMS = V.ROOT / "docs" / "build" / "WP-08" / "change_view_inputs.yaml"
PENDING = "assessment pending (no v2 multi-rater assessment for this task)"


def sig_summary(s):
    return {"id": s["id"], "label": s["prefLabel"]["en"], "signalStatus": s.get("signalStatus"),
            "signalFamily": s.get("signalFamily"), "direction": s.get("direction"), "drivers": s.get("drivers"),
            "reliability": s.get("reliability"), "sourceRelease": s.get("sourceRelease"), "evidenceLabel": s.get("evidenceLabel"),
            "reviewBy": s.get("reviewBy")}


def main():
    d = V.Data()
    atoms = V.L.load_yaml(ATOMS)["atoms"]
    by_role = defaultdict(list)
    for a in atoms:
        by_role[a["role"]].append(a)
    sigs = {s["id"]: s for s in d.signals if not V.held(s)}
    by_target = defaultdict(list)
    for s in sigs.values():
        by_target[str(s.get("targetId", ""))].append(s)
    rows = []
    for role in d.roles():
        if d.tier(role) != "P1":
            continue
        rk = role["id"].split(":", 1)[1]
        actors = sorted({v["sectorActor"] for v in d.variants_of[role["id"]] if not V.held(v)})
        ctx = []
        for key in [f"mvp-role:{rk}", role["id"]] + [f"vocab:sector_actors#{a}" for a in actors] + \
                   [f"vocab:work_functions#{role['primaryWorkFunction']}"]:
            ctx += by_target.get(key, [])
        role_atoms = [a for a in by_role[role["id"]] if a["target"] == "role"]
        task_atoms = defaultdict(list)
        for a in by_role[role["id"]]:
            if a["target"] != "role":
                task_atoms[a["target"]].append(a)
        tasks = []
        share_by_kind = defaultdict(float)
        for i in role["taskBundle"]:
            tid = i["task"]
            ats = task_atoms.get(tid, [])
            kinds = sorted({a["kind"] for a in ats})
            share_by_kind[kinds[0] if kinds else "no reshaping claim drafted"] += i["timeShare"]
            named = [sigs[s] for a in ats for s in a["signals"] if s in sigs]
            v2 = d.v1asm.get("__v2__" + tid, [])
            tasks.append({"task": tid, "statement": d.statement(tid), "timeShare": i["timeShare"],
                          "roleLevels": i.get("roleLevels"), "critical": i["critical"], "neededAtEntry": i["neededAtEntry"],
                          "formationTask": i.get("formationTask", False),
                          "change": [{"kind": a["kind"], "drivers": a["drivers"], "note": a["note"],
                                      "instruments": [{"id": x, "label": d.label(x)} for x in a["instruments"]]} for a in ats],
                          "evidence": {"v2Assessment": PENDING if not v2 else v2,
                                       "namedSignals": [sig_summary(s) for s in named],
                                       "activeSignals": sum(1 for s in named if s.get("signalStatus") == "active"),
                                       "v1PriorEvidence": {"records": d.v1asm.get(tid, []),
                                                           "display": "evidence drawer only: v1 single-analyst prior, LLM-assisted, unvalidated - not for decisions"}
                                       if d.v1asm.get(tid) else None},
                          "workFunction": "Assessment pending (Task.workFunction is gated, ADR-0029 section 6)"})
            for a in ats:
                rows.append({"role": role["id"], "task": tid, "kind": a["kind"], "drivers": " ".join(a["drivers"]),
                             "timeShare": i["timeShare"], "namedSignals": len(named), "activeSignals": 0,
                             "v2Assessment": "pending" if not v2 else "present"})
        ext = []
        for r in d.external.get(f"mvp-role:{rk}", []) + d.external.get(role["id"], []):
            es = r.get("externalSource") or {}
            ext.append({"id": r["id"], "index": es.get("index"), "release": es.get("release"), "unit": es.get("unit"),
                        "matchType": r.get("crosswalkMinMatchType"), "values": es.get("values"),
                        "dispersion": es.get("dispersion"), "license": r.get("license"),
                        "label": "Occupation-level external index; not specific to this role's tasks",
                        "display": "context only" if r.get("crosswalkMinMatchType") in ("skos:exactMatch", "skos:closeMatch")
                        else "evidence drawer only (matched more broadly than closeMatch)",
                        "releaseNote": "licence LicenseRef-EMST-third-party-index-derived: excluded from release outputs until the index terms are verified"})
        role_level_signals = []
        for a in role_atoms:
            role_level_signals.append({"kind": a["kind"], "drivers": a["drivers"], "note": a["note"],
                                       "instruments": [{"id": x, "label": d.label(x)} for x in a["instruments"]],
                                       "signals": [sig_summary(sigs[s]) for s in a["signals"] if s in sigs]})
        view = {"stamp": V.stamp("role-change-inputs", "0.1.0", GEN), "role": role["id"], "roleTitle": d.label(role["id"]),
                "summary": role["definition"]["en"],
                "evidenceNotice": ("Reshaping claims are agent drafts (raterType llm, validationStatus draft, evidence S). "
                                   "No task has a v2 multi-rater assessment yet, so every task shows 'assessment pending'. "
                                   "Change indicators count active signals only (ADR-0028); all linked signals are at "
                                   "watch, so no change indicator moves. v1 values appear only as prior-evidence pointers."),
                "timeShareByClaim": {k: round(v, 3) for k, v in sorted(share_by_kind.items())},
                "roleLevelChange": role_level_signals,
                "contextSignals": [sig_summary(s) for s in sorted(ctx, key=lambda s: s["id"])],
                "changeIndicator": {"active": sum(1 for s in ctx if s.get("signalStatus") == "active"),
                                    "status": "no change indicator (0 active signals; ADR-0028 two-family, two-period, human-reviewed rule)"},
                "externalContext": ext, "tasks": tasks}
        V.write_json(V.OUT / "change_view" / f"{rk}.json", view)
    with open(V.OUT / "change_view" / "summary.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["role", "task", "kind", "drivers", "timeShare", "namedSignals", "activeSignals", "v2Assessment"])
        w.writeheader()
        w.writerows(rows)
    print(f"change views: {len({r['role'] for r in rows})} roles, {len(rows)} task claims")


if __name__ == "__main__":
    main()
