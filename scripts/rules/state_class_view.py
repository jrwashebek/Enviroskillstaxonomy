"""state-class-view@0.2.0 (vocab/rules/state-class-view@0.2.0.yaml; RULINGS_FOR_DE §19.1; ADR-0032).

Port of pipelines/views/state_class_view.py (WP-08): one view per released StateClassRecord whose emstMapping names a
released role variant, with the class facts beside the variant at the mapped role level(s). Competency targets are
computed from the role, never copied into the register. Also an index of every P1-P2 state and local variant.
Held records, Tribal variants and Tribal-employer class records are never read.

0.2.0 (rc.1 fix pass, review M10; DATA_FIX_BRIEF §5): mappings below skos:closeMatch are left out (never an
alignment); the model's own number is `agentConfidence (uncalibrated)`; one file per class lists EVERY mapped variant
(`variants[]`), so a class mapped to several variants no longer keeps only the last one written.
"""

from __future__ import annotations

from rules import hr_common as H

PILOTS = "TX, WA and PA (state), Lewis County WA (county environmental health), Philadelphia Water Department (municipal utility)"


def class_facts(c):
    pay = c.get("payMinMax") or {}
    jur = c.get("jurisdictionId")
    return {"jurisdiction": jur.get("label") if isinstance(jur, dict) else jur, "employerType": c.get("employerType"),
            "agency": c.get("agency"), "classCode": c.get("classCode"), "classTitle": c.get("classTitle"),
            "series": c.get("seriesId"), "level": c.get("levelIndex"), "supervisoryStatus": c.get("supervisoryStatus"),
            "specEffectiveDate": c.get("specEffectiveDate"), "mqLocation": c.get("mqLocation"),
            "mqParaphrase": (c.get("mqText") or {}).get("paraphrase") if isinstance(c.get("mqText"), dict) else None,
            "degreeRule": c.get("degreeRule"), "licensesRequired": c.get("licensesRequired") or [],
            "pay": {"basis": c.get("payBasis"), "min": pay.get("min"), "max": pay.get("max"),
                    "label": c.get("payGradeLabel") or pay.get("rangeLabel"), "effective": c.get("payEffectiveDate")},
            "reviewBy": c.get("reviewBy")}


def _jur_code(c):
    """Jurisdiction part of the file stem, from the class notation scheme `class-<JUR>` (TX, WA, PA-PHL, WA-LEWIS): the stem
    the WP-08 generator takes from the class seed key, so view file names stay stable across minting (ADR-0031 §2)."""
    for n in c.get("notation") or []:
        scheme = str((n or {}).get("scheme") or "") if isinstance(n, dict) else ""
        if scheme.startswith("class-"):
            return scheme[len("class-"):].replace("/", "-").replace(":", "-")
    jur = c.get("jurisdictionId")
    code = jur.get("code") if isinstance(jur, dict) else jur
    return str(code or "unknown").replace("/", "-").replace(":", "-")


STRENGTH = {"skos:exactMatch": 5, "skos:closeMatch": 4, "skos:broadMatch": 3, "skos:narrowMatch": 3, "skos:relatedMatch": 1}
MIN_STRENGTH = STRENGTH["skos:closeMatch"]
AGENT_CONFIDENCE = "agentConfidence (uncalibrated)"


def compute(released, stamp):
    out, by_variant, below = {}, {}, 0
    for cid, c in sorted(released.items()):
        if c.get("type") != "StateClassRecord" or H.held(c) or str(c.get("employerType", "")).startswith("tribal"):
            continue
        maps = c.get("emstMapping") or []
        maps = maps if isinstance(maps, list) else [maps]
        blocks = []
        for m in maps:
            if not isinstance(m, dict):
                continue
            variant = released.get(m.get("roleVariant"))
            role = released.get((variant or {}).get("variantOf"))
            if not variant or not role or H.held(variant) or H.held(role):
                continue
            if STRENGTH.get(m.get("matchType"), 0) < MIN_STRENGTH:
                below += 1                                   # 0.2.0: not an alignment; never shown (ADR-0032, M10)
                continue
            levels = [x for x in str(m.get("roleLevel") or "").split("|") if x]
            home = variant.get("homeModule") or role.get("homeModule") or "core"
            tasks, collapsed = [], []
            for i in H.at_levels(H.effective_bundle(role, variant), levels):
                (tasks if H.in_main_section(released, i["task"], home) else collapsed).append(H.gated_task(released, role, i))
            blocks.append({"variant": variant["id"], "role": role["id"], "roleLevels": levels,
                           "match": {"type": m.get("matchType"), AGENT_CONFIDENCE: m.get("confidence"),
                                     "review": "unreviewed agent candidate (not reviewed by a person)" if not m.get("reviewer") else "reviewed"},
                           "targets": H.targets_at(released, role, levels), "tasks": tasks,
                           "gates": H.credential_gates(released, variant), "collapsed": collapsed})
        if not blocks:
            continue
        jur, code = _jur_code(c), str(c.get("classCode") or cid.split("--")[-1])
        doc = {"jurisdiction": jur, "classCode": code, "classRecord": cid, "classFacts": class_facts(c),
               "variants": blocks, "disclaimers": [H.DISCLAIMER], **stamp}
        out[f"views/state_class_views/{jur}--{code}.json"] = doc
        for b in blocks:
            by_variant.setdefault(b["variant"], []).append({"classRecord": cid, "classCode": code, "roleLevels": b["roleLevels"]})
    for role in H.roles(released):
        if H.tier(role) not in ("P1", "P2"):
            continue
        for actor in ("state", "local"):
            v = H.variant_for(released, role["id"], actor)
            if v and not H.held(v):
                by_variant.setdefault(v["id"], [])
    out["views/state_class_views/index.json"] = {
        "variants": dict(sorted(by_variant.items())), "disclaimers": [H.DISCLAIMER],
        "excludedBelowCloseMatch": below,
        "note": (f"An empty list means no class is mapped at skos:closeMatch or stronger in the pilot jurisdictions ({PILOTS}). "
                 "Broader or partial mappings are not an alignment and are left out; every mapping is an unreviewed agent "
                 "candidate, and agentConfidence (uncalibrated) is the drafting model's own number."), **stamp}
    return out
