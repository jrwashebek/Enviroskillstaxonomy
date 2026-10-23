"""role-change@0.1.0 (vocab/rules/role-change@0.1.0.yaml; RULINGS_FOR_DE §19.1).

Port of pipelines/views/change_view.py (WP-08) and the role-change summary in site/lib/model.mjs (CP) onto released
records and the computed display-gate view. View 1 "How is this role changing?" for each released P1 role and its
variants. It never reads docs/build/WP-08/change_view_inputs.yaml; v1 values and third-party index context never
appear; summaries count tasks, never time. Indicators move only under change-indicator@1.0.0, never here.
"""
from __future__ import annotations

from collections import defaultdict

from rules import hr_common as H


def _assessed_tasks(display_gate_doc):
    """Tasks whose v2 ExposureAssessment the display gate renders (production or tentative)."""
    out = set()
    for r in (display_gate_doc or {}).get("rows", []):
        if str(r.get("field", "")).startswith("ExposureAssessment:") and r.get("decision") in ("production", "tentative"):
            out.add(r.get("recordId"))
    return out


def _signal(s):
    return {"id": s["id"], "signalStatus": s.get("signalStatus"), "signalFamily": s.get("signalFamily"),
            "direction": s.get("direction"), "drivers": s.get("drivers"), "reliability": s.get("reliability")}


def compute(released, display_gate_doc, as_of, stamp):
    assessed = _assessed_tasks(display_gate_doc)
    events = H.events_by_instrument(released)
    instruments = {rid: r for rid, r in released.items() if r.get("type") == "Instrument" and not H.held(r)}
    by_mech = defaultdict(list)
    for iid, ins in sorted(instruments.items()):
        for m in ins.get("mechanisms") or []:
            by_mech[m].append(iid)
    signals = [r for r in released.values() if r.get("type") == "ChangeSignal" and not H.held(r)
               and r.get("license") != "LicenseRef-EMST-third-party-index-derived"]
    vof = H.variants_of(released)
    out, summary = {}, []
    for role in H.roles(released):
        if H.tier(role) != "P1":
            continue
        rk = H.role_key(role["id"])
        targets = {role["id"], f"vocab:work_functions#{role.get('primaryWorkFunction')}"}
        variants = vof.get(role["id"], [])
        targets |= {v["id"] for v in variants}
        sig = sorted((_signal(s) for s in signals if s.get("targetId") in targets), key=lambda s: s["id"])
        docs = []
        for v in [None] + variants:
            items = H.effective_bundle(role, v)
            levels = []
            for lv in [r["key"] for r in role.get("roleLevels") or [] if isinstance(r, dict)]:
                at = H.at_levels(items, [lv])
                tasks = [{"task": i["task"], "status": "assessed" if i["task"] in assessed else H.PENDING} for i in at]
                n_ass = sum(1 for t in tasks if t["status"] == "assessed")
                levels.append({"level": lv, "tasks": tasks, "counts": {"assessed": n_ass, "pending": len(tasks) - n_ass}})
            links = {}
            for lk in (v or {}).get("instruments") or []:
                if isinstance(lk, dict) and lk.get("instrument") in instruments:
                    links[lk["instrument"]] = {"instrument": lk["instrument"], "role": lk.get("role"), "via": "typed link"}
            mechs = set()
            for i in items:
                t = released.get(i["task"]) or {}
                mechs |= {e.get("mechanism") for e in t.get("instrumentSensitivity") or [] if isinstance(e, dict)}
                for s in t.get("supports") or []:
                    if isinstance(s, dict) and s.get("strength") == "primary":
                        c = released.get(s.get("competency")) or {}
                        mechs |= {e.get("mechanism") for e in c.get("instrumentSensitivity") or [] if isinstance(e, dict)}
            for m in sorted(x for x in mechs if x):
                for iid in by_mech.get(m, []):
                    links.setdefault(iid, {"instrument": iid, "role": None, "via": f"sensitivity edge {m}"})
            ins = [{**lk, "status": H.instrument_status(events, iid, as_of), "asOf": as_of} for iid, lk in sorted(links.items())]
            docs.append({"variant": (v or {}).get("id"), "roleLevels": levels, "instruments": ins})
        out[f"views/role_change/{rk}.json"] = {"role": role["id"], "variants": docs, "signals": sig,
                                               "note": "Counts tasks, never time; indicators move only under change-indicator@1.0.0.", **stamp}
        base = docs[0]
        summary.append({"role": role["id"], "levels": [{"level": lv["level"], **lv["counts"],
                                                        "label": f"{lv['counts']['assessed']} of {len(lv['tasks'])} tasks assessed"}
                                                       for lv in base["roleLevels"]]})
    out["views/role_change/summary.json"] = {"roles": summary, **stamp}
    return out
