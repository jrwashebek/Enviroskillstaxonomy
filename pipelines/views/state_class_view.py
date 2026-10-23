#!/usr/bin/env python3
"""State Class View generator (ADR-0006 section 4; SPEC section 5.21; WP-08 with SL).

For each dated StateClassRecord (data/v2/registers/state_classes/, X5) that names a role variant, render the class facts
next to the EMST role variant at the mapped role level(s): competency targets with level (computed from the role, never
copied into the register), the variant's tasks at those levels with indicative time share, credential gates and the
disclaimer. Also writes an index over every P1-P2 state and local variant, with its mapped classes or the statement that
no class is mapped in the pilot jurisdictions. Held records are never read.

Outputs  docs/build/WP-08/generated/state-class/<jur>--<code>.json and .md, variant_index.json
Licence: Apache-2.0.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viewlib as V  # noqa: E402

GEN = "pipelines/views/state_class_view.py@0.1.0"
PILOTS = "TX, WA and PA (state), Lewis County WA (county environmental health), Philadelphia Water Department (municipal utility)"


def class_facts(c):
    pay = c.get("payMinMax") or {}
    return {"jurisdiction": (c.get("jurisdictionId") or {}).get("label") if isinstance(c.get("jurisdictionId"), dict) else c.get("jurisdictionId"),
            "employerType": c.get("employerType"), "agency": c.get("agency"), "classCode": c.get("classCode"),
            "classTitle": c.get("classTitle"), "series": c.get("seriesId"), "level": c.get("levelIndex"),
            "supervisoryStatus": c.get("supervisoryStatus"), "specEffectiveDate": c.get("specEffectiveDate"),
            "mqLocation": c.get("mqLocation"), "mqParaphrase": (c.get("mqText") or {}).get("paraphrase"),
            "degreeRule": c.get("degreeRule"), "licensesRequired": c.get("licensesRequired") or [],
            "pay": {"basis": c.get("payBasis"), "min": pay.get("min"), "max": pay.get("max"),
                    "label": c.get("payGradeLabel") or pay.get("rangeLabel"), "effective": c.get("payEffectiveDate")},
            "specUrl": (c.get("workDescriptionText") or {}).get("url"), "reviewBy": c.get("reviewBy")}


def mapping_block(d, m):
    vid = m.get("roleVariant")
    variant = d.get(vid)
    role = d.get(variant["variantOf"]) if variant else None
    if not variant or not role or V.held(variant):
        return None
    levels = [x for x in (m.get("roleLevel") or "").split("|") if x]
    items = V.at_levels(V.effective_bundle(role, variant), levels)
    tasks = sorted(items, key=lambda i: -i["shareWithin"])[:12]
    return {"roleVariant": vid, "role": role["id"], "roleTitle": d.label(role["id"]), "tier": d.tier(role),
            "authorityPosition": variant.get("authorityPosition"), "roleLevels": levels,
            "matchType": m.get("matchType"), "confidence": m.get("confidence"),
            "review": "unreviewed agent draft" if not m.get("reviewer") else f"reviewed by {m['reviewer']} on {m.get('reviewDate')}",
            "crosswalkRecord": m.get("crosswalkRecord"),
            "competencyTargets": V.targets_at(d, role, levels),
            "topTasks": [{"task": i["task"], "statement": d.statement(i["task"]), "pctTime": round(100 * i["shareWithin"], 1),
                          "critical": i.get("critical", False), "neededAtEntry": i.get("neededAtEntry", False)} for i in tasks],
            "credentialGates": [{"credential": g["credential"], "label": d.label(g["credential"]), "kind": g["kind"]}
                                for g in variant.get("credentialGates") or []]}


def render_md(v):
    f = v["class"]
    out = [f"# State Class View: {f['classTitle']} ({f['classCode']}), {f['jurisdiction']}", "",
           f"> **{v['disclaimer']}**", ">", f"> {v['evidenceNotice']}", "",
           f"- **Agency / employer:** {f['agency']} ({f['employerType']})",
           f"- **Series and level:** {f['series']}; level {(f['level'] or {}).get('ordinal')} ({(f['level'] or {}).get('label')}); {f['supervisoryStatus']}",
           f"- **Spec effective:** {f['specEffectiveDate']}; record re-check by {f['reviewBy']} (dated record; re-run each 1 July)",
           f"- **Minimum qualifications:** {f['mqParaphrase'] or 'see spec'} (binding text lives in: {f['mqLocation']}; degree rule: {f['degreeRule']})",
           f"- **Licences:** " + ("; ".join(f"{x.get('credential')} ({x.get('timing')})" for x in f["licensesRequired"]) or "none recorded"),
           f"- **Pay:** {f['pay']['label'] or ''} {('USD ' + str(f['pay']['min']) + '–' + str(f['pay']['max'])) if f['pay']['min'] else '(amounts not retrieved)'} {f['pay']['basis'] or ''}, effective {f['pay']['effective']}",
           f"- **Spec text:** stored by URL and hash only ({f['specUrl']})",
           f"- **Generated:** {v['stamp']['generator']}, rule {v['stamp']['ruleId']}@{v['stamp']['ruleVersion']} ({v['stamp']['ruleStatus']}), as of {v['stamp']['asOf']}", ""]
    for m in v["mappings"]:
        out += [f"## EMST role: {m['roleTitle']} ({m['roleVariant'].split('/', 1)[1]} variant, {'/'.join(m['roleLevels'])} level; {m['tier']})", "",
                f"*Match:* `{m['matchType']}`, confidence {m['confidence']}, {m['review']} (`{m['crosswalkRecord']}`). "
                f"*Authority position (editorial):* {m['authorityPosition']}.", "",
                "**Competency targets at this level (agent draft)**", ""]
        for t in m["competencyTargets"]:
            if t["importance"] < 3:
                continue
            out.append(f"- {t['label']} — {', '.join(f'{k} {x}' for k, x in t['targetLevels'].items())}" +
                       (" *(distinguishing)*" if t["distinguishing"] else ""))
        out += ["", "**Main tasks at this level (indicative % of time, agent draft)**", ""]
        for t in m["topTasks"]:
            flags = ", ".join(x for x, on in (("critical", t["critical"]), ("needed at entry", t["neededAtEntry"])) if on)
            out.append(f"- {t['statement']} — {t['pctTime']}%" + (f" *({flags})*" if flags else ""))
        if m["credentialGates"]:
            out += ["", "*Credential gates (draft):* " + "; ".join(f"{g['label']} ({g['kind']})" for g in m["credentialGates"])]
        out.append("")
    out += ["---", v["disclaimer"] + " The class specification, not this view, governs classification and qualification.", ""]
    return "\n".join(out)


def main():
    d = V.Data()
    by_variant = {}
    n = 0
    for cid in sorted(d.by_type["StateClassRecord"]):
        c = d.get(cid)
        if V.held(c):
            continue
        maps = [mb for mb in (mapping_block(d, m) for m in c.get("emstMapping") or [] if m.get("roleVariant")) if mb]
        if not maps:
            continue
        view = {"stamp": V.stamp("state-class-view", "0.1.0", GEN), "disclaimer": V.DISCLAIMER,
                "evidenceNotice": V.EVIDENCE_NOTICE, "classRecord": cid, "class": class_facts(c), "mappings": maps}
        stem = V.L.id_to_stem(cid).replace("seed-class--", "")
        V.write_json(V.OUT / "state-class" / f"{stem}.json", view)
        V.write_text(V.OUT / "state-class" / f"{stem}.md", render_md(view))
        n += 1
        for m in maps:
            by_variant.setdefault(m["roleVariant"], []).append({"classRecord": cid, "classTitle": c.get("classTitle"),
                                                                "roleLevels": m["roleLevels"], "matchType": m["matchType"],
                                                                "view": f"state-class/{stem}.md"})
    for r in d.roles():
        if d.tier(r) not in ("P1", "P2"):
            continue
        for actor in ("state", "local"):
            v = d.get(f"{r['id']}/{actor}")
            if v and v["id"] not in by_variant:
                by_variant[v["id"]] = []
    for vid, classes in sorted(by_variant.items()):
        v = d.get(vid)
        role = d.get(v["variantOf"])
        lv = [r["key"] for r in role["roleLevels"]]
        lines = [f"# State Class View (variant): {d.label(vid)}", "", f"> **{V.DISCLAIMER}**", ">", f"> {V.EVIDENCE_NOTICE}", "",
                 f"- **Role:** {d.label(role['id'])} (`{role['id']}`, {d.tier(role)}); authority position (editorial): {v.get('authorityPosition')}",
                 f"- **Generated:** {GEN}, rule state-class-view@0.1.0 (proposed), as of {V.AS_OF}", "", "## Mapped classes", ""]
        if classes:
            lines += [f"- {c['classTitle']} (`{c['classRecord']}`), {'/'.join(c['roleLevels'])} level, `{c['matchType']}` — see `{c['view']}`" for c in classes]
        else:
            lines.append(f"No class is mapped in the pilot jurisdictions ({PILOTS}). The role's targets below are what a "
                         "jurisdiction would crosswalk its own class specification against.")
        lines += ["", "## Competency targets by role level (agent draft)", ""]
        for t in V.targets_at(d, role, lv):
            if t["importance"] >= 4 or t["distinguishing"]:
                lines.append(f"- {t['label']} — " + ", ".join(f"{k} {x}" for k, x in t["targetLevels"].items()))
        lines += ["", "---", V.DISCLAIMER, ""]
        V.write_text(V.OUT / "state-class" / "variants" / f"{V.L.id_to_stem(vid)}.md", "\n".join(lines))
    V.write_json(V.OUT / "state-class" / "variant_index.json",
                 {"stamp": V.stamp("state-class-view", "0.1.0", GEN), "disclaimer": V.DISCLAIMER,
                  "note": f"Every P1-P2 state and local variant with its mapped class records; an empty list means no class is mapped in the pilot jurisdictions ({PILOTS}).",
                  "variants": dict(sorted(by_variant.items()))})
    print(f"state class views: {n}; state/local variants indexed: {len(by_variant)}; "
          f"with a mapped class: {sum(1 for v in by_variant.values() if v)}")


if __name__ == "__main__":
    main()
