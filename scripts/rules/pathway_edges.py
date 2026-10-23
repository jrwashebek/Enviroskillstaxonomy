"""pathway-edges@0.1.0 (vocab/rules/pathway-edges@0.1.0.yaml; RULINGS_FOR_DE §19.1).

Port of the edge functions in site/lib/model.mjs (CP) onto released records. Exploratory mobility edges between
released role variants for View 3; no edge or pathway is ever labelled recommended (ADR-0023, ADR-0027). Overlap
compares the origin's targets at its highest role level with the destination's targets at its first role level
(editorial design values); no importance or time-share weighting before job analysis. Held and Tribal records are
never read.
"""
from __future__ import annotations

from rules import hr_common as H

LEVEL_ORD = {"A": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}
LABEL = "exploratory; editorial draft target levels; not a recommendation"


def _levels(role):
    keys = [r["key"] for r in role.get("roleLevels") or [] if isinstance(r, dict)]
    return sorted(keys, key=lambda k: H.LEVEL_KEYS.index(k) if k in H.LEVEL_KEYS else 99)


def _targets(role):
    return {t["competency"]: t for t in role.get("competencyTargets") or [] if isinstance(t, dict) and t.get("competency")}


def compute(released, stamp):
    variants = [v for _, v in sorted(released.items()) if v.get("type") == "RoleVariant" and not H.held(v)
                and released.get(v.get("variantOf")) and not H.held(released[v["variantOf"]])]
    pathways = [p for p in released.values() if p.get("type") == "Pathway" and not H.held(p)]
    frictions = [f for f in released.values() if f.get("type") == "FrictionRecord" and not H.held(f)]
    edges = []
    for v in variants:
        ro = released[v["variantOf"]]
        lo = _levels(ro)
        if not lo:
            continue
        origin, from_level = _targets(ro), lo[-1]
        named = set(ro.get("progressesTo") or [])
        for w in variants:
            if w["variantOf"] == v["variantOf"]:
                continue                       # same role, other actor: a variant switch, not a pathway
            rw = released[w["variantOf"]]
            lw = _levels(rw)
            if not lw:
                continue
            to_level = lw[0]
            dest = {c: t for c, t in _targets(rw).items() if (t.get("targetLevels") or {}).get(to_level)}
            if not dest:
                continue
            shared, gap = 0, []
            for cid, t in sorted(dest.items()):
                have = ((origin.get(cid) or {}).get("targetLevels") or {}).get(from_level)
                want = t["targetLevels"][to_level]
                if have and LEVEL_ORD.get(have, 0) >= LEVEL_ORD.get(want, 0):
                    shared += 1
                else:
                    gap.append({"competency": cid, "fromLevel": have, "toLevel": want})
            lp = [p for p in pathways if p.get("fromVariant") in (v["id"], ro["id"]) and p.get("toVariant") in (w["id"], rw["id"])]
            is_named = rw["id"] in named or w["id"] in named
            if not is_named and not lp and shared * 2 < len(dest):
                continue
            fr = [{"frictionType": f.get("frictionType"), "severity": f.get("severity"), "basis": f.get("basis")}
                  for f in frictions if (f.get("fromVariant") == v["id"] and f.get("toVariant") == w["id"])
                  or (not f.get("fromVariant") and f.get("fromActor") == v.get("sectorActor") and f.get("toActor") == w.get("sectorActor"))]
            edges.append({"from": v["id"], "to": w["id"], "fromLevel": from_level, "toLevel": to_level,
                          "shared": {"N": shared, "M": len(dest)},
                          "statement": f"shares {shared} of {len(dest)} destination competencies at the destination's target level",
                          "gap": gap, "named": is_named,
                          "pathways": [{"id": p["id"], "pathwayType": p.get("pathwayType"), "cloOutcomes": p.get("cloOutcomes") or [],
                                        "formationProvisions": [fp for s in p.get("sequence") or [] if isinstance(s, dict)
                                                                for fp in s.get("formationProvisions") or []],
                                        "recommended": False} for p in sorted(lp, key=lambda x: x["id"])]
                          or "no learning pathway recorded",
                          "frictions": fr, "label": LABEL, **stamp})
    return {"edges": edges, "note": "No edge or pathway is ever labelled recommended (ADR-0023, ADR-0027).", **stamp}
