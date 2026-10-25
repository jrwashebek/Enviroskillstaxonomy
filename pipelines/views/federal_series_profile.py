#!/usr/bin/env python3
"""Federal Series Profile generator (ADR-0006 section 4; SPEC section 14 computed views; WP-08).

For each OPM series that X4 (data/v2/crosswalks/opm-series/<snapshot>.sssom.tsv) maps to a P1, P2 or P4 role with a
positive, non-negated predicate, assemble a series-shaped profile from the role's federal variant: dated series status
from the L6 register (never shown as realigned while only proposed), indicative grade bands from the variant, major
duties per band in role-record order, Factor 1 knowledge from the competency targets and knowledge statements,
positive-education flag, credential gates, and the disclaimer. Display-gate@1.1.0 governs every bundle value (CR-FIX-B-001;
ADR-0031 §4.4): % time and importance only from job-analysis-confirmed, critical / needed-at-entry / distinguishing only
after a pid: reviewer, target levels labelled editorial drafts; otherwise the gate's label is printed and no value.
P3 roles are excluded (they appear only in the what's-coming view, ADR-0006). Tribal variants are never read.
Rule federal-series-profile@0.2.0 (rc.1 fix pass, ADR-0032; review M10): X4 rows below skos:closeMatch are left out
(never an alignment), the model's number is `agentConfidence (uncalibrated)`, and every row is labelled an unreviewed
agent candidate.

Outputs  docs/build/WP-08/generated/federal-series/<code>.json and .md, index.json, federal_variant_index.json
Licence: Apache-2.0.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import viewlib as V  # noqa: E402

GEN = "pipelines/views/federal_series_profile.py@0.3.0"
RULE_VERSION = "0.2.0"
AGENT_CONFIDENCE = "agentConfidence (uncalibrated)"
UNREVIEWED = "unreviewed agent candidate (not reviewed by a person)"
X4 = V.L.DATA_V2 / "crosswalks" / "opm-series" / "2026-10-23.sssom.tsv"
TIERS = {"P1", "P2", "P4"}
STRENGTH = {"skos:exactMatch": 5, "skos:closeMatch": 4, "skos:broadMatch": 3, "skos:narrowMatch": 3, "skos:relatedMatch": 1}
FEEDER = {"destination after corps hiring authority", "technician feeder"}  # X4 rows that name a pipeline, not the role's series
GROUPS = [("developmental and full performance", ["entry", "journey"]), ("senior and lead", ["senior", "lead", "strategic"])]


def status_statement(rec):
    st = rec.get("seriesStatus", "active")
    code = rec["seriesCode"]
    if st == "active":
        return f"Active (EMST OPM series register, as of {V.AS_OF})."
    if st == "proposed-realignment":
        succ = rec.get("successorSeries", "another series")
        return (f"Active under its current code {code}. OPM's Phase One list proposes realignment to {succ}; the proposal "
                f"is not final as of {V.AS_OF}. This profile is shown under {code} and will move only if OPM finalizes it.")
    if st.startswith("realigned-to:"):
        return f"Realigned to {st.split(':', 1)[1]} effective {rec.get('effectiveDate', 'date not recorded')}."
    if st == "cancelled":
        return f"Cancelled (effective {rec.get('effectiveDate', 'date not recorded')})."
    return st


def bands_for(variant, role):
    parsed = V.band_pairs(variant.get("indicativeGradeOrBand"))
    levels = [r["key"] for r in role["roleLevels"]]
    if parsed and all(lv for _, lv in parsed):
        groups = []
        for name, lvls in GROUPS:
            sel = [(b, lv) for b, lv in parsed if set(lv) & set(lvls) and set(lv) <= set(levels) | set(lvls)]
            sel = [(b, [x for x in lv if x in levels]) for b, lv in sel]
            sel = [(b, lv) for b, lv in sel if lv]
            if sel:
                groups.append({"group": name, "indicativeBand": "; ".join(f"{b} ({'/'.join(lv)})" for b, lv in sel),
                               "roleLevels": [x for b, lv in sel for x in lv]})
        return groups
    # no parseable band (e.g. wage-grade scheme): one group over all levels
    return [{"group": "all levels", "indicativeBand": V.band_text(variant.get("indicativeGradeOrBand")),
             "roleLevels": levels}]


CTX = "federal-series-profile"


def role_block(d, role, variant, row):
    items = V.effective_bundle(role, variant)
    imp_ok = V.shows(role, "competencyTargets.importance", CTX)
    dist_ok = V.shows(role, "competencyTargets.distinguishing", CTX)
    crit_ok = V.shows(role, "taskBundle.critical", CTX)
    entry_ok = V.shows(role, "taskBundle.neededAtEntry", CTX)
    blocks = []
    for g in bands_for(variant, role):
        sel = V.at_levels(items, g["roleLevels"])
        tg = V.targets_at(d, role, g["roleLevels"])
        f1 = []
        for t in tg:                 # every target at these levels, in record order (importance never selects)
            ks = [k["statement"]["en"] for k in d.ks_by_comp.get(t["competency"], [])][:3]
            lv = ", ".join(f"{k} {v}" for k, v in t["targetLevels"].items())
            f1.append({"competency": t["competency"], "statement": f"Knowledge of and skill in: {t['label'][0].lower()}{t['label'][1:]} (EMST target {lv}, editorial draft).",
                       "knowledgeStatements": ks, "importance": t["importance"] if imp_ok else None,
                       "distinguishing": t["distinguishing"] if dist_ok else None})
        blocks.append({**g, "majorDuties": V.duties(d, role, sel, CTX), "pctTimeNotice": V.TIME_NOTICE,
                       "neededAtEntryTasks": [i["task"] for i in sel if i.get("neededAtEntry")] if entry_ok else None,
                       "criticalTasks": [i["task"] for i in sel if i.get("critical")] if crit_ok else None,
                       "distinguishingCompetencies": [t["competency"] for t in tg if t["distinguishing"]] if dist_ok else None,
                       "jobAnalysisValues": V.PENDING_JA if not (crit_ok and entry_ok) else None,
                       "factor1Knowledge": f1})
    other = V.parse_other(row.get("other"))
    return {"role": role["id"], "roleTitle": d.label(role["id"]), "tier": d.tier(role), "variant": variant["id"],
            "functionStatement": role["functionStatement"]["en"], "authorityPosition": variant.get("authorityPosition"),
            "x4": {"record": row["record_id"], "predicate": row["predicate_id"], AGENT_CONFIDENCE: float(row["confidence"] or 0),
                   "appliesTo": other.get("applies_to"), "reviewStatus": UNREVIEWED if not row.get("reviewer_id") else other.get("review_status"),
                   "evidence": other.get("evidence")},
            "credentialGates": V.gate_view(d, variant.get("credentialGates")),
            "signOffAuthority": variant.get("signOffAuthority"),
            "instruments": V.link_items(d, variant.get("instruments")),
            "bands": blocks,
            "changeView": f"docs/build/WP-08/generated/change_view/{d.role_key(role)}.json" if d.tier(role) == "P1" else None}


def render_md(p):
    s = p["series"]
    out = [f"# Federal Series Profile: {s['code']} {s['title']}", "",
           f"> **{p['disclaimer']}**", ">", f"> {p['evidenceNotice']}", "",
           f"- **Series status:** {s['statusStatement']}",
           f"- **Occupational group:** {s.get('group') or 'not recorded'}",
           f"- **Qualification standard:** {s.get('qualificationStandardVersion') or 'not recorded'}",
           f"- **Positive education requirement:** {'yes' if s.get('positiveEducationRequirement') else 'no' if s.get('positiveEducationRequirement') is False else 'not recorded'} ({s['educationNote']})",
           f"- **Register record:** `{s['registerRecord']}` (re-check by {s.get('registerReviewBy') or 'n/a'})",
           f"- **USA Hire / general competencies:** {p['generalCompetencies']}",
           f"- **Generated:** {p['stamp']['generator']}, rule {p['stamp']['ruleId']}@{p['stamp']['ruleVersion']} ({p['stamp']['ruleStatus']}), as of {p['stamp']['asOf']}", ""]
    for r in p["roles"]:
        out += [f"## {r['roleTitle']} — federal variant ({r['tier']})", "",
                f"*Function:* {r['functionStatement']}", "",
                f"*X4 match:* `{r['x4']['predicate']}` (agentConfidence (uncalibrated) {r['x4'][AGENT_CONFIDENCE]}, applies to: {r['x4']['appliesTo']}; "
                f"{r['x4']['reviewStatus']}, evidence {r['x4']['evidence']}). *Authority position (editorial):* {r['authorityPosition']}.", ""]
        if r["credentialGates"]["shown"] or r["credentialGates"]["notShownUntilIssuerVerified"]:
            out.append("*Credential gates (issuer verified):* " + V.gate_text(r["credentialGates"]))
            out.append("")
        for b in r["bands"]:
            out += [f"### {b['group'].capitalize()} — indicative band {b['indicativeBand']} (not a classification criterion)", "",
                    "**Major duties (agent draft, in record order)**", "", f"*{b['pctTimeNotice']}*", ""]
            if b.get("jobAnalysisValues"):
                out += [f"*Critical and needed-at-entry tasks: {b['jobAnalysisValues']}*", ""]
            for du in b["majorDuties"]:
                out.append(f"- **{du['duty']}**" + (f" — {du['pctTime']}%" if du["pctTime"] is not None else ""))
                for t in du["tasks"][:4]:
                    flags = ", ".join(x for x, on in (("critical", t["critical"]), ("needed at entry", t["neededAtEntry"]),
                                                      ("formation task, editorial draft", t["formationTask"])) if on)
                    out.append(f"  - {t['statement']}" + (f" *({flags})*" if flags else ""))
            out += ["", "**Factor 1 — knowledge required (draft language; target levels are editorial drafts)**", ""]
            for f in b["factor1Knowledge"]:
                out.append(f"- {f['statement']}" + (" *Distinguishing.*" if f["distinguishing"] else ""))
                for ks in f["knowledgeStatements"]:
                    out.append(f"  - {ks}")
            out.append("")
        if r["changeView"]:
            out += [f"*How this role is changing:* see `{r['changeView']}` (assessment pending; watch signals only).", ""]
    if p.get("feederOrDestinationRoles"):
        out += ["## Feeder and destination roles (not classified in this series)", ""]
        for f in p["feederOrDestinationRoles"]:
            out.append(f"- `{f['role']}` — {f['relation']} (`{f['predicate']}`)")
        out.append("")
    if p.get("rolesWithoutFederalVariant"):
        out += ["*Roles crosswalked to this series without a federal variant in the MVP set:* " +
                ", ".join(f"`{x}`" for x in p["rolesWithoutFederalVariant"]), ""]
    out += ["---", f"{p['disclaimer']} Series codes proposed for realignment are shown under their current code until OPM "
            "finalizes a change. Grade bands are indicative only and are never a classification criterion.", ""]
    return "\n".join(out)


def main():
    d = V.Data()
    rows = V.read_set(X4)
    by_series = {}
    fed_index = {}
    below = 0
    for row in rows:
        obj = row["object_id"]
        if not obj.startswith("OPMseries:") or row.get("predicate_modifier") == "Not":
            continue
        if STRENGTH.get(row["predicate_id"], 0) < STRENGTH["skos:closeMatch"]:
            below += 1                     # rule 0.2.0: below closeMatch is not an alignment; never shown (ADR-0032, M10)
            continue
        role = d.get(row["subject_id"])
        if not role or d.tier(role) not in TIERS:
            continue
        variant = d.variant_for(role["id"], "federal")
        code = obj.split(":", 1)[1]
        applies = V.parse_other(row.get("other")).get("applies_to", "")
        if applies in FEEDER:
            by_series.setdefault(code, {"rows": [], "noVariant": [], "feeder": []}).setdefault("feeder", []).append(
                {"role": role["id"], "relation": applies, "predicate": row["predicate_id"]})
            continue
        if variant is None or V.held(variant):
            by_series.setdefault(code, {"rows": [], "noVariant": [], "feeder": []})["noVariant"].append(role["id"])
            continue
        by_series.setdefault(code, {"rows": [], "noVariant": [], "feeder": []})["rows"].append((role, variant, row))
        fed_index.setdefault(variant["id"], []).append({"series": code, "predicate": row["predicate_id"],
                                                        AGENT_CONFIDENCE: float(row["confidence"] or 0)})
    index = []
    for code in sorted(by_series):
        rec = d.series.get(code)
        if rec is None:
            continue
        ent = by_series[code]
        edu = rec.get("positiveEducationRequirement")
        prof = {"stamp": V.stamp("federal-series-profile", RULE_VERSION, GEN), "disclaimer": V.DISCLAIMER,
                "evidenceNotice": V.EVIDENCE_NOTICE,
                "series": {"code": code, "title": rec["prefLabel"]["en"], "seriesStatus": rec.get("seriesStatus"),
                           "statusStatement": status_statement(rec), "successorSeriesProposed": rec.get("successorSeries")
                           if rec.get("seriesStatus") == "proposed-realignment" else None,
                           "group": (rec.get("scopeNote") or {}).get("en", "").replace("Occupational group: ", "").rstrip("."),
                           "qualificationStandardVersion": rec.get("qualificationStandardVersion"),
                           "positiveEducationRequirement": edu,
                           "educationNote": "from EMST's series record; not yet checked against the OPM qualification standard, so confirm with the HR office",
                           "registerRecord": rec["id"], "registerReviewBy": rec.get("reviewBy"),
                           "events": rec.get("events") or []},
                "generalCompetencies": "not mapped in this release (X9 USA Hire and FWCI parts not built; WP-09 open item 6)",
                "roles": [role_block(d, r, v, row) for r, v, row in sorted(
                    ent["rows"], key=lambda x: (-STRENGTH.get(x[2]["predicate_id"], 0), -float(x[2]["confidence"] or 0), x[0]["id"]))],
                "rolesWithoutFederalVariant": sorted(set(ent["noVariant"])),
                "feederOrDestinationRoles": ent.get("feeder", [])}
        if not prof["roles"]:
            continue
        V.write_json(V.OUT / "federal-series" / f"{code}.json", prof)
        V.write_text(V.OUT / "federal-series" / f"{code}.md", render_md(prof))
        index.append({"series": code, "title": prof["series"]["title"], "seriesStatus": rec.get("seriesStatus"),
                      "roles": [r["role"] for r in prof["roles"]]})
    # every P1-P2 federal variant appears, with its series or the X4 no-term reason
    for r in d.roles():
        if d.tier(r) not in ("P1", "P2"):
            continue
        v = d.variant_for(r["id"], "federal")
        if v and v["id"] not in fed_index:
            fed_index[v["id"]] = []
    for vid, series in sorted(fed_index.items()):
        v = d.get(vid)
        role = d.get(v["variantOf"])
        lines = [f"# Federal Series Profile (variant index): {d.label(vid)}", "", f"> **{V.DISCLAIMER}**", "",
                 f"- **Role:** {d.label(role['id'])} (`{role['id']}`, {d.tier(role)}); authority position (editorial): {v.get('authorityPosition')}",
                 f"- **Indicative band:** {V.band_text(v.get('indicativeGradeOrBand'))} (not a classification criterion)",
                 f"- **Generated:** {GEN}, rule federal-series-profile@{RULE_VERSION} ({V.stamp('federal-series-profile', RULE_VERSION, GEN)['ruleStatus']}), as of {V.AS_OF}", "", "## Series", ""]
        if series:
            for x in series:
                rec = d.series.get(x["series"]) or {}
                lines.append(f"- {x['series']} {(rec.get('prefLabel') or {}).get('en', '')} — `{x['predicate']}` (agentConfidence (uncalibrated) {x[AGENT_CONFIDENCE]}; unreviewed agent candidate); "
                             f"status: {status_statement(rec) if rec else 'not in register'} See `federal-series/{x['series']}.md`.")
        else:
            lines.append("No federal series at skos:closeMatch or stronger: X4 records NoTermFound or only broader or partial "
                         "candidates for this role, which are not an alignment (for corps members, the series listed in X4 "
                         "are destinations after corps hiring authorities, not the role's own series).")
        lines += ["", "---", V.DISCLAIMER, ""]
        V.write_text(V.OUT / "federal-series" / "variants" / f"{V.L.id_to_stem(vid)}.md", "\n".join(lines))
    V.write_json(V.OUT / "federal-series" / "index.json", {"stamp": V.stamp("federal-series-profile", RULE_VERSION, GEN),
                                                           "disclaimer": V.DISCLAIMER, "series": index,
                                                           "excludedBelowCloseMatch": below,
                                                           "note": "Only X4 rows at skos:closeMatch or stronger are shown; every row is an unreviewed agent candidate."})
    V.write_json(V.OUT / "federal-series" / "federal_variant_index.json",
                 {"stamp": V.stamp("federal-series-profile", RULE_VERSION, GEN), "disclaimer": V.DISCLAIMER,
                  "note": "Every P1-P2 federal variant with the series X4 maps it to; an empty list means X4 records NoTermFound for the role.",
                  "variants": dict(sorted(fed_index.items()))})
    print(f"federal series profiles: {len(index)}; federal variants indexed: {len(fed_index)}")


if __name__ == "__main__":
    main()
