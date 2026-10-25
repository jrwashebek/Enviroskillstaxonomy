"""federal-series-profile@0.2.0 (vocab/rules/federal-series-profile@0.2.0.yaml; RULINGS_FOR_DE §19.1; ADR-0032).

0.2.0 (rc.1 fix pass, review M10; DATA_FIX_BRIEF §5): rows below skos:closeMatch (broad, narrow, related) are left
out; they are never an alignment. The drafting model's own number is shown as `agentConfidence (uncalibrated)`, and
every row says it is an unreviewed agent candidate until a pid: reviewer is recorded.

Port of pipelines/views/federal_series_profile.py (WP-08) onto released records and the released X4 mapping rows.
One profile per OPM series that X4 maps, with a positive non-negated predicate, to a released P1, P2 or P4 role,
assembled from the role's federal variant. P3 roles are excluded; Tribal variants and held records are never read.
"""
from __future__ import annotations

from rules import hr_common as H

TIERS = {"P1", "P2", "P4"}
STRENGTH = {"skos:exactMatch": 5, "skos:closeMatch": 4, "skos:broadMatch": 3, "skos:narrowMatch": 3, "skos:relatedMatch": 1}
MIN_STRENGTH = STRENGTH["skos:closeMatch"]           # 0.2.0: nothing below closeMatch enters a profile
AGENT_CONFIDENCE = "agentConfidence (uncalibrated)"
UNREVIEWED = "unreviewed agent candidate (not reviewed by a person)"
FEEDER = {"destination after corps hiring authority", "technician feeder"}
X4_PREFIX = "opm-series/"


def series_status(rec, as_of, released):
    st = rec.get("seriesStatus", "active")
    code = rec["seriesCode"]
    if st == "proposed-realignment":
        text = (f"Active under its current code {code}. A realignment to {rec.get('successorSeries', 'another series')} is "
                f"proposed and not final as of {as_of}; the profile stays under {code} until OPM finalizes it.")
    elif str(st).startswith("realigned-to:"):
        text = f"Realigned to {st.split(':', 1)[1]} effective {rec.get('effectiveDate', 'date not recorded')}."
    elif st == "cancelled":
        text = f"Cancelled (effective {rec.get('effectiveDate', 'date not recorded')})."
    else:
        text = f"{st} (EMST OPM series register, as of {as_of})."
    events = [e for e in rec.get("events") or [] if e in released]
    return {"value": st, "statement": text, "asOf": as_of, "events": events}


def parse_band(band):
    out = []
    for part in (band or "").split(";"):
        part = part.strip()
        if not part:
            continue
        if "[" in part and part.endswith("]"):
            b, lv = part[:-1].split("[", 1)
            out.append((b.strip(), [x.strip() for x in lv.split("|")]))
        else:
            out.append((part, []))
    return out


def bands(variant, role):
    g = variant.get("indicativeGradeOrBand") or {}
    levels = [r["key"] for r in role.get("roleLevels") or [] if isinstance(r, dict)]
    if g.get("byRoleLevel"):
        return [{"roleLevel": k, "indicativeBand": v, "label": "not a classification criterion"}
                for k, v in g["byRoleLevel"].items() if k in levels]
    parsed = parse_band(g.get("band"))
    if parsed and all(lv for _, lv in parsed):
        return [{"roleLevel": lv, "indicativeBand": b, "label": "not a classification criterion"}
                for b, lvs in parsed for lv in lvs if lv in levels]
    return [{"roleLevel": "all", "indicativeBand": g.get("band", "not recorded"), "label": "not a classification criterion"}]


def role_block(released, role, variant, row, ks_by_comp):
    items = H.effective_bundle(role, variant)
    levels = [r["key"] for r in role.get("roleLevels") or [] if isinstance(r, dict)]
    home = variant.get("homeModule") or role.get("homeModule") or "core"
    duties, knowledge, collapsed = [], [], []
    for lv in levels:
        for i in H.at_levels(items, [lv]):
            t = H.gated_task(released, role, i)
            t["roleLevel"] = lv
            (duties if H.in_main_section(released, i["task"], home) else collapsed).append(t)
    for t in H.targets_at(released, role, levels):
        entry = {**t, "knowledgeStatements": [k for k in ks_by_comp.get(t["competency"], [])][:3]}
        (knowledge if H.in_main_section(released, t["competency"], home) else collapsed).append(entry)
    other = H.parse_other(row.get("other"))
    reviewed = any(str(x).startswith("pid:") for x in (row.get("reviewer_id") or "").split("|") if x)
    return {"role": role["id"], "roleTitle": H.label(released, role["id"]), "tier": H.tier(role), "variant": variant["id"],
            "homeModule": home, "authorityPosition": variant.get("authorityPosition"), "authorityPositionLabel": "editorial",
            "x4": {"record": row.get("record_id"), "predicate": row.get("predicate_id"), AGENT_CONFIDENCE: row.get("confidence"),
                   "appliesTo": other.get("applies_to"),
                   "reviewStatus": other.get("review_status") if reviewed else UNREVIEWED},
            "bands": bands(variant, role), "duties": duties, "knowledge": knowledge,
            "gates": H.credential_gates(released, variant), "collapsed": collapsed}


def compute(released, mappings, stamp, as_of):
    """Returns {relative view path: document}."""
    series = {r["seriesCode"]: r for r in released.values() if r.get("type") == "SeriesRecord" and r.get("seriesCode")}
    ks_by_comp = {}
    for k in released.values():
        if k.get("type") == "KnowledgeStatement" and not H.held(k):
            sup = k.get("supports") or []
            for c in (sup if isinstance(sup, list) else [sup]):
                c = c.get("competency") if isinstance(c, dict) else c
                ks_by_comp.setdefault(c, []).append((k.get("statement") or {}).get("en", ""))
    rows = [r for name, rs in mappings.items() if name.startswith(X4_PREFIX) for r in rs]
    by_series, below = {}, 0
    for row in rows:
        obj = row.get("object_id", "")
        if not obj.startswith("OPMseries:") or row.get("predicate_modifier") == "Not":
            continue
        if STRENGTH.get(row.get("predicate_id"), 0) < MIN_STRENGTH:
            below += 1                                  # 0.2.0: not an alignment; never shown (ADR-0032, M10)
            continue
        role = released.get(row.get("subject_id"))
        if not role or role.get("type") != "RoleProfile" or H.held(role) or H.tier(role) not in TIERS:
            continue
        if H.parse_other(row.get("other")).get("applies_to", "") in FEEDER:
            continue
        variant = H.variant_for(released, role["id"], "federal")
        if variant is None or H.held(variant):
            continue
        by_series.setdefault(obj.split(":", 1)[1], []).append((role, variant, row))
    out, index = {}, []
    for code in sorted(by_series):
        rec = series.get(code)
        if rec is None:
            continue
        entries = sorted(by_series[code], key=lambda x: (-STRENGTH.get(x[2].get("predicate_id"), 0), x[0]["id"]))
        doc = {"seriesCode": code, "title": H.label(released, rec["id"]), "seriesStatus": series_status(rec, as_of, released),
               "roles": [role_block(released, r, v, row, ks_by_comp) for r, v, row in entries],
               "disclaimers": [H.DISCLAIMER], **stamp}
        out[f"views/federal_series_profiles/{code}.json"] = doc
        index.append({"seriesCode": code, "seriesStatus": doc["seriesStatus"]["value"], "roles": [r["role"] for r in doc["roles"]]})
    out["views/federal_series_profiles/index.json"] = {
        "series": index, "disclaimers": [H.DISCLAIMER],
        "excludedBelowCloseMatch": below,
        "note": ("Only X4 rows at skos:closeMatch or stronger are shown; broader or partial rows are not an alignment and are "
                 "left out. Every row is an unreviewed agent candidate; agentConfidence (uncalibrated) is the drafting "
                 "model's own number."), **stamp}
    return out
