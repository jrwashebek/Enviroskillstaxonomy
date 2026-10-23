"""WP-10 ChangeSignal seed: standing demand signals, deployment, headcount, policy-watch and scenario signposts.

Every signal: driver tags, reliability A-D, source + sourceRelease, personalData = false, evidenceLabel S
(SPEC 5.14: S until a human reviews it), signalStatus = watch (no seeded signal has named human review, so none
can satisfy the ADR-0028 evidence rule yet). Only derived aggregates are stored: no posting text, no names,
no person-level rows. Tribal-related signals are quarantined (careFlag = true, held = True).
"""
import os
import re

from wp10_common import (ROOT, base, provenance, write_jsonl, sha256_file, RECHECK_PENDING,
                         WATCH_REVIEW_BY, AS_OF, TOOL_VERSION, PROMPT_VERSION)

LMR = "docs/research/labor-market-ai-impact"
PRED = {"exact": "skos:exactMatch", "close": "skos:closeMatch", "related": "skos:relatedMatch",
        "broad": "skos:broadMatch", "narrow": "skos:narrowMatch"}


def role(k):
    """RoleProfile seed key (CR-IA-001 ruling: seed:<role_key>); WP-08 authored all 37 MVP role profiles."""
    return "seed:" + k


def wf(k):
    return "vocab:work_functions#" + k


def actor(k):
    return "vocab:sector_actors#" + k


def ttype(target):
    if re.match(r"^seed:R\d{2}-", target):
        return "RoleProfile"
    if target.startswith("seed:ins/"):
        return "Instrument"
    if target.startswith("vocab:"):
        return "VocabularyTerm"
    raise ValueError(target)


def sig(key, label, *, targetId, measure, observed, comparison=None, geography="US", sectorActor=None,
        source, release, corpus, method, crosswalkPath, matchType, direction, dconf, drivers, steep, novelty,
        reliability, corroboration, family, indep, impact, sources, signposts=None, registered=False,
        held=False, note=None, definition=None, baseline=None, sensitivity=None, points=None, targetType=None):
    if measure.get("value") is None:
        raise ValueError("measure.value must be a number: " + key)
    nota = None
    r = base("seed:sig/" + key, "ChangeSignal", label, definition=definition, editorial_note=note, held=held, notation=nota)
    m = {"name": measure["name"], "value": measure["value"], "unit": measure["unit"],
         "ci95": measure.get("ci95"), "n": measure.get("n"), "denominator": measure.get("denominator") or "not applicable"}
    if isinstance(m["n"], float):
        m["n"] = int(m["n"])
    mb = measure.get("baseline")
    if mb:
        b = {k: mb[k] for k in ("ci95", "n", "note") if mb.get(k) is not None}
        if mb.get("value") is not None:
            b["value"] = mb["value"]
        m["baseline"] = b
    ms_ = measure.get("sensitivity")
    if ms_:
        m["sensitivity"] = {k: ms_[k] for k in ("weighting", "value", "baselineValue") if ms_.get(k) is not None}
    r.update({
        "targetType": targetType or ttype(targetId),
        "targetId": targetId,
        "measure": m,
        "observedPeriod": observed,
        "geography": geography,
        "source": source,
        "sourceRelease": release,
        "corpus": corpus,
        "method": method,
        "toolVersion": TOOL_VERSION,
        "promptVersion": PROMPT_VERSION,
        "crosswalkPath": crosswalkPath if isinstance(crosswalkPath, list) else [crosswalkPath],
        "crosswalkMinMatchType": PRED[matchType],
        "direction": direction,
        "directionConfidence": dconf,
        "drivers": drivers,
        "steepCategory": steep,
        "novelty": novelty,
        "reliability": reliability,
        "corroboration": corroboration,
        "careFlag": bool(held),
        "tribalPrograms": bool(held),
        "personalData": False,
        "evidenceLabel": "S",
        "reviewStatus": "unreviewed",
        "reviewBy": WATCH_REVIEW_BY if not held else RECHECK_PENDING,
        "signalStatus": "watch",
        "signalFamily": family,
        "independenceKey": indep,
        "impact": impact,
        "provenance": provenance(sources, "E"),
    })
    if family == "deployment":
        r["registeredDeployment"] = bool(registered)
    if signposts:
        r["scenarioSignposts"] = signposts
    if points:
        r["pointsToward"] = points
    if comparison:
        r["comparisonPeriod"] = comparison
    if sectorActor:
        r["sectorActor"] = sectorActor
    return r


# ---------------------------------------------------------------------------------------------- OpenLMP
def openlmp_signals():
    import wp10_lmp
    d = wp10_lmp.compute()
    cat_sha = sha256_file(d["catalog_path"])
    corpus = {"version": "OpenLMP 0.1.0 (catalog generated 2026-10-21)", "sha256": cat_sha, "license": "CC0-1.0"}
    e82, e12 = d["eras"]["1982-rule"], d["eras"]["2012-rule"]
    obs = {"start": "2012", "end": AS_OF[:4],
           "note": "Plans and amendments under the 2012 Planning Rule framework (catalogued plan years %s-%s); a framework era, not a calendar window" % tuple(e12["years"])}
    comp = {"start": "1982", "end": "2012",
            "note": "Plans under the 1982 Planning Rule framework (catalogued plan years %s-%s; many remain in force)" % tuple(e82["years"])}
    common = dict(observed=obs, comparison=comp, geography="US-West", sectorActor="federal",
                  source="LM-144", release="OpenLMP 0.1.0; WP-10 derivation 2026-10-23", corpus=corpus,
                  steep="political", family="plan-requirements", indep="openlmp-usfs-western-plans",
                  sources=["LM-144", "LM-017", "LM-018"])
    meth = ("Cross-era comparison of plan components (not a time series of the same plans). Headline weights each "
            "plan equally (share or rate computed within plan, then averaged; ci95 = mean +/- 1.96 SE across plans); "
            "component-weighted value kept as the ADR-0028 sensitivity check. Keyword and OpenLMP coordination-tag "
            "definitions reused from LM Phase 2 (lmp_demand_signals.py). Mentions measure what plans name, not obligation.")

    def ratio(a, b):
        return round(a / b, 2) if b else None

    out = []
    # 1 monitoring workload
    m12, m82 = e12["monitoring_share_plan_equal"], e82["monitoring_share_plan_equal"]
    out.append(sig("openlmp/monitoring-share-2012-vs-1982",
                   "Monitoring requirements as a share of plan components: 2012-rule vs 1982-rule land management plans",
                   targetId=wf("WF-MONITOR"),
                   measure={"name": "monitoring_component_share_plan_equal", "value": m12["value"], "unit": "share of plan components",
                            "ci95": m12["ci95"], "n": m12["n"], "denominator": "plans (each weighted equally)",
                            "baseline": {"value": m82["value"], "ci95": m82["ci95"], "n": m82["n"]},
                            "sensitivity": {"weighting": "component", "value": e12["monitoring_share_component_weighted"],
                                            "baselineValue": e82["monitoring_share_component_weighted"]}},
                   method=meth, crosswalkPath="OpenLMP component_type=monitoring -> work function WF-MONITOR (definitional)",
                   matchType="close", direction="grow", dconf="med", drivers=["policy-reform"], novelty=1, reliability="B",
                   corroboration=1, impact=2,
                   note="Robust to weighting: CIs do not overlap under plan-equal weighting. Plans name indicators and reporting, not field methods (remote sensing in 3 of 1,506 monitoring questions; LM Phase 2), so this is demand for indicator design, evaluation and reporting.",
                   **common))
    # 2 term mention rates
    terms = [
        ("climate_change", "Climate-change content in plan direction", wf("WF-PLAN"), ["climate", "policy-reform"], "environmental"),
        ("data_or_models", "Data and model dependence of plan direction", wf("WF-ASSESS"), ["policy-reform"], "technological"),
        ("at_risk_species_scc", "At-risk species and species-of-conservation-concern content in plan direction", wf("WF-ASSESS"), ["policy-reform"], "environmental"),
        ("carbon", "Carbon content in plan direction", wf("WF-PLAN"), ["climate", "policy-reform"], "environmental"),
        ("remote_sensing_lidar_drone", "Remote sensing, LiDAR and drone mentions in plan direction", wf("WF-MONITOR"), ["sensing-tech", "policy-reform"], "technological"),
        ("partnership_collaboration", "Partnership and collaboration language in plan direction", "vocab:work_functions#MODE-ENGAGE", ["policy-reform"], "political"),
    ]
    for k, label, target, drivers, steep in terms:
        a, b = e12["terms_per_1000_plan_equal"][k], e82["terms_per_1000_plan_equal"][k]
        overlap = (a["ci95"] and b["ci95"] and a["ci95"][0] <= b["ci95"][1])
        c = dict(common)
        c["steep"] = steep
        out.append(sig("openlmp/term-%s-2012-vs-1982" % k.replace("_", "-"),
                       "%s: mentions per 1,000 plan components, 2012-rule vs 1982-rule plans" % label,
                       targetId=target,
                       measure={"name": "mentions_per_1000_components_plan_equal:" + k, "value": a["value"], "unit": "mentions per 1,000 components",
                                "ci95": a["ci95"], "n": a["n"], "denominator": "plans (each weighted equally)",
                                "baseline": {"value": b["value"], "ci95": b["ci95"], "n": b["n"]},
                                "sensitivity": {"weighting": "component", "value": e12["terms_per_1000_component_weighted"][k],
                                                "baselineValue": e82["terms_per_1000_component_weighted"][k]}},
                       method=meth, crosswalkPath="keyword family '%s' in plan component text -> %s (topical; mention not obligation)" % (k, target),
                       matchType="related", direction="grow", dconf="low" if overlap else "med", drivers=drivers, novelty=1,
                       reliability="B", corroboration=1, impact=1 if k in ("carbon", "remote_sensing_lidar_drone") else 2,
                       note=("Plan-equal and component-weighted CIs overlap or base is small: treat as weak." if overlap else
                             "Direction robust to weighting (non-overlapping plan-equal CIs)."), **c))
    # 3 coordination touchpoints (non-Tribal), with the weighting finding
    tps = [("partnership", "Partnership coordination touchpoints", "stakeholder"),
           ("cross_boundary", "Cross-boundary coordination touchpoints", "intergovernmental"),
           ("state_agency", "State-agency coordination touchpoints", "intergovernmental")]
    for k, label, rel in tps:
        a, b = e12["touchpoints_per_1000_plan_equal"][k], e82["touchpoints_per_1000_plan_equal"][k]
        cw12, cw82 = e12["touchpoints_per_1000_component_weighted"][k], e82["touchpoints_per_1000_component_weighted"][k]
        pe_ratio, cw_ratio = ratio(a["value"], b["value"]), ratio(cw12, cw82)
        overlap = a["ci95"][0] <= b["ci95"][1] and b["ci95"][0] <= a["ci95"][1]
        direction = "grow" if (pe_ratio and pe_ratio > 1.25 and cw_ratio and cw_ratio > 1.25) else "stable"
        out.append(sig("openlmp/touchpoint-%s-2012-vs-1982" % k.replace("_", "-"),
                       "%s per 1,000 plan components, 2012-rule vs 1982-rule plans" % label,
                       targetId="vocab:work_functions#MODE-ENGAGE",
                       measure={"name": "coordination_touchpoints_per_1000_plan_equal:" + k, "value": a["value"], "unit": "tagged components per 1,000",
                                "ci95": a["ci95"], "n": a["n"], "denominator": "plans (each weighted equally)",
                                "baseline": {"value": b["value"], "ci95": b["ci95"], "n": b["n"]},
                                "sensitivity": {"weighting": "component", "value": cw12, "baselineValue": cw82}},
                       method=meth + " relationshipType=" + rel + ".",
                       crosswalkPath="OpenLMP coordination tag '%s' -> MODE-ENGAGE (relationshipType %s)" % (k, rel),
                       matchType="related", direction=direction, dconf="low", drivers=["policy-reform"], novelty=1,
                       reliability="B", corroboration=1, impact=2,
                       note=("Weighting matters: plan-equal ratio %s vs component-weighted ratio %s; plan-equal CIs %s. "
                             "LM Phase 2's 'coordination about tripled' is component-weighted and partly reflects a few large plans."
                             % (pe_ratio, cw_ratio, "overlap" if overlap else "do not overlap")),
                       **common))
    # 4 Tribal touchpoints: computed, quarantined (careFlag) - TN decides any representation
    a, b = e12["touchpoints_per_1000_plan_equal"]["tribal"], e82["touchpoints_per_1000_plan_equal"]["tribal"]
    out.append(sig("openlmp/touchpoint-tribal-2012-vs-1982", "Tribal coordination touchpoints in plan components (held)",
                   targetId="vocab:work_functions#MODE-ENGAGE",
                   measure={"name": "coordination_touchpoints_per_1000_plan_equal:tribal", "value": a["value"], "unit": "tagged components per 1,000",
                            "ci95": a["ci95"], "n": a["n"], "denominator": "plans (each weighted equally)",
                            "baseline": {"value": b["value"], "ci95": b["ci95"], "n": b["n"]}},
                   method=meth, crosswalkPath="held", matchType="related", direction="grow", dconf="low",
                   drivers=["policy-reform"], novelty=1, reliability="B", corroboration=1, impact=2, held=True,
                   note="Quarantined under the Tribal gate (ADR-0007). Government-to-government relations are never public participation; TN decides whether and how this is shown.",
                   **common))
    return out


# ---------------------------------------------------------------------------------------------- OMB AI inventory
def omb_signals():
    p = os.path.join(ROOT, LMR, "omb_ai_inventory_env_bureaus_2025.csv")
    corpus = {"version": "2025 Federal Agency AI Use Case Inventory (README summary as of 2026-04-13); LM bureau extract",
              "sha256": sha256_file(p), "license": "public-domain-us-government (no licence statement seen; V4-15)"}
    common = dict(observed={"start": "2025-01-01", "end": "2025-12-22", "note": "2025 inventory cycle; agency submissions due 2025-12-22"},
                  geography="US", sectorActor="federal", source="LM-138", release="2025 inventory; public 2026-01-28; README 2026-04-13",
                  corpus=corpus, steep="technological", family="deployment", indep="ombegov-ai-inventory",
                  sources=["LM-138", "LM-027"])
    meth = ("Counts of individually reported use cases in nine environmental bureaus (USGS, NOAA, USDA NRE incl. USFS, EPA, "
            "USDA FPAC incl. NRCS, FWS, BOR, BLM, NPS), keyword-classified into function families (LM Phase 2 omb_inventory_env.py). "
            "'Deployed' = development_stage deployed only (the OMB README pools deployed+piloted; NOAA reported no stages). "
            "Self-reported by agencies; availability and registration are not proof of use.")
    rows = [  # family, n, deployed, target, label, direction, drivers, registered, note
        ("species-detection", 89, 11, wf("WF-ASSESS"), "AI species and wildlife detection (acoustic, camera, image)", "augment", ["AI", "sensing-tech"], True,
         "Largest environmental AI cluster; classical ML and computer vision, not LLMs."),
        ("remote-sensing", 63, 11, wf("WF-ASSESS"), "AI remote sensing, imagery and LiDAR analysis", "augment", ["AI", "sensing-tech"], True, None),
        ("water-hydrology", 36, 10, wf("WF-MONITOR"), "AI in water and hydrology monitoring and modelling", "augment", ["AI", "sensing-tech"], True, None),
        ("fire-smoke", 31, 8, wf("WF-RESPOND"), "AI in fire and smoke detection, prediction and operations", "augment", ["AI", "sensing-tech"], True, None),
        ("forecasting", 33, 2, wf("WF-ASSESS"), "AI in weather and climate forecasting", "augment", ["AI"], True, None),
        ("genai-drafting", 41, 4, wf("WF-REVIEW"), "Generative AI drafting, summarization and chat (bureau-built)", "augment", ["AI"], True,
         "Separate from the consolidated COTS file, which shows drafting tools licensed near agency-wide (see the COTS signal)."),
        ("inspection-compliance", 12, 4, wf("WF-ENFORCE"), "AI in inspection, compliance and enforcement", "augment", ["AI"], True, None),
        ("nepa-permitting", 5, 0, wf("WF-REVIEW"), "AI in NEPA, environmental review and permitting", "stable", ["AI"], False,
         "Counter-signal to automation claims for review: 0 of 5 deployed in the 2025 inventory; PNNL shared services (separate signal) are offered to reviewers but agencies registered no deployed review AI."),
        ("public-comment", 3, 1, "vocab:work_functions#MODE-ENGAGE", "AI in public-comment analysis", "augment", ["AI"], True, None),
    ]
    out = []
    for fam, n, dep, target, label, direction, drivers, registered, note in rows:
        out.append(sig("omb-ai-inventory-2025/%s" % fam, "%s: registered federal environmental-bureau use cases (2025 inventory)" % label,
                       targetId=target,
                       measure={"name": "use_cases_deployed", "value": dep, "unit": "use cases at development_stage=deployed",
                                "ci95": None, "n": n, "denominator": "use cases in the function family (all stages)"},
                       method=meth, crosswalkPath="OMB use case text -> keyword function family '%s' -> %s" % (fam, target),
                       matchType="related", direction=direction, dconf="med" if dep >= 4 else "low", drivers=drivers,
                       novelty=1, reliability="A", corroboration=1, impact=2, registered=registered and dep > 0, note=note, **common))
    # COTS availability (drafting tools at workforce scale)
    out.append(sig("omb-ai-inventory-2025/cots-genai-drafting-scale", "Commercial generative-AI drafting and summarization tools licensed at workforce scale (EPA, DOI, USDA)",
                   targetId=wf("WF-REVIEW"),
                   measure={"name": "departments_with_cots_genai_drafting_at_10000_plus_users", "value": 3, "unit": "departments",
                            "ci95": None, "n": 3, "denominator": "environmental departments examined (EPA, DOI, USDA)"},
                   method="Consolidated COTS use-case file: EPA M365 Copilot/Azure OpenAI 10,000-50,000 users; DOI writing tools 50,000+; USDA Copilot Chat 50,000+ (LM Phase 2 omb_cots_ai_env_departments_2025.csv). Licences are availability, not use.",
                   crosswalkPath="COTS use case (drafting, summarizing, retrieval) -> document-centred tasks in WF-REVIEW and WF-MONITOR.attest (generic, not environmental-specific)",
                   matchType="related", direction="augment", dconf="med", drivers=["AI"], novelty=1, reliability="A",
                   corroboration=1, impact=3, registered=True,
                   note="Generic documentation compression (v1 'Ac' zone) is available at tool-access level now; this does not show time savings or headcount effects (XR-03).",
                   **common))
    return out


# ---------------------------------------------------------------------------------------------- headcount (OPM data via verified analyses)
def headcount_signals():
    out = []
    corpus_pps = {"version": "PPS Fed Figures (OPM data Sep 2024 - Jan 2026)", "sha256": None, "license": "not stated (aggregate figures cited)"}
    common = dict(geography="US", sectorActor="federal", steep="political", family="headcount", indep="opm-ehri-fwd",
                  matchType="close", novelty=1, corroboration=1)
    obs = {"start": "2024-09-30", "end": "2026-01-31"}
    out.append(sig("headcount/usfs-gt25pct-2024-09-to-2026-01", "U.S. Forest Service headcount fell by more than a quarter (Sep 2024 - Jan 2026)",
                   targetId=actor("federal"),
                   measure={"name": "headcount_change_share", "value": -0.25, "unit": "share (upper bound: 'more than a quarter')",
                            "ci95": None, "n": None, "denominator": "USFS employees Sep 2024 (PPS base)"},
                   observed=obs, source="LM-128", release="PPS analysis of OPM data to Jan 2026", corpus=corpus_pps,
                   method="Secondary analysis of OPM data (PPS). PPS gives no exact USFS percentage; USDA OIG puts the 2025 loss at 16% on a different base - do not mix bases (V1-02).",
                   crosswalkPath="agency headcount -> organization (no series split)", direction="decline", dconf="high",
                   drivers=["fiscal", "policy-reform", "workforce-capacity"], reliability="B", impact=3, sources=["LM-128"],
                   note="Driver is fiscal and policy (deferred resignation, RIF, hiring freeze), not AI. Must never be read as automation.", **common))
    out.append(sig("headcount/nps-gt25pct-2024-09-to-2026-01", "National Park Service headcount fell by more than a quarter (Sep 2024 - Jan 2026)",
                   targetId=actor("federal"),
                   measure={"name": "headcount_change_share", "value": -0.25, "unit": "share (upper bound: 'more than a quarter')",
                            "ci95": None, "n": None, "denominator": "NPS employees Sep 2024 (PPS base)"},
                   observed=obs, source="LM-128", release="PPS analysis of OPM data to Jan 2026", corpus=corpus_pps,
                   method="Secondary analysis of OPM data (PPS) (V1-02).", crosswalkPath="agency headcount -> organization",
                   direction="decline", dconf="high", drivers=["fiscal", "policy-reform", "workforce-capacity"], reliability="B", impact=3,
                   sources=["LM-128"], **common))
    out.append(sig("headcount/park-rangers-minus-34pct", "Federal park rangers fell 34.1% (Sep 2024 - Jan 2026)",
                   targetId=role("R21-park-ranger-visitor-resource"),
                   measure={"name": "headcount_change_share", "value": -0.341, "unit": "share", "ci95": None, "n": None,
                            "denominator": "federal park rangers Sep 2024"},
                   observed=obs, source="LM-128", release="PPS analysis of OPM data to Jan 2026", corpus=corpus_pps,
                   method="Secondary analysis of OPM data (PPS) (V1-02).",
                   crosswalkPath="OPM series 0025 Park Ranger -> mvp_role_set R21 federal variant (X4 pending)", direction="decline",
                   dconf="high", drivers=["fiscal", "policy-reform", "workforce-capacity"], reliability="B", impact=2, sources=["LM-128"], **common))
    out.append(sig("headcount/federal-under-30-share", "Under-30 share of the federal civilian workforce fell from 8.9% to 7.9% (Sep 2024 - Jan 2026)",
                   targetId=actor("federal"),
                   measure={"name": "under_30_share", "value": 0.079, "unit": "share of employees", "ci95": None, "n": None,
                            "denominator": "federal civilian employees", "baseline": {"value": 0.089, "ci95": None, "n": None}},
                   observed={"start": "2026-01-31", "end": "2026-01-31"}, comparison={"start": "2024-09-30", "end": "2024-09-30"},
                   source="LM-128", release="PPS analysis of OPM data to Jan 2026", corpus=corpus_pps,
                   method="Secondary analysis of OPM data (PPS) (V1-02). Entry-path health input (ADR-0008 s6).",
                   crosswalkPath="governmentwide -> entry-level role variants (computed later)", direction="decline", dconf="high",
                   drivers=["fiscal", "policy-reform", "workforce-capacity", "demographic"], reliability="B", impact=3, sources=["LM-128"],
                   note="Entry-path signal: the rung is thinning through hiring policy, not AI (LM Phase 2 Q2).", **common))
    out.append(sig("headcount/federal-civilian-minus-12pct", "Federal civilian workforce fell from 2,313,216 to 2,035,344 (Sep 2024 - Jan 2026)",
                   targetId=actor("federal"),
                   measure={"name": "headcount", "value": 2035344, "unit": "employees", "ci95": None, "n": None, "denominator": "federal civilian employees",
                            "baseline": {"value": 2313216, "ci95": None, "n": None}},
                   observed={"start": "2026-01-31", "end": "2026-01-31"}, comparison={"start": "2024-09-30", "end": "2024-09-30"},
                   source="LM-128", release="PPS analysis of OPM data to Jan 2026", corpus=corpus_pps,
                   method="PPS from OPM data (V1-01). Do not attribute OPM's own ~317,000 departures tally to PPS.",
                   crosswalkPath="governmentwide -> organization", direction="decline", dconf="high",
                   drivers=["fiscal", "policy-reform", "workforce-capacity"], reliability="B", impact=3, sources=["LM-128"], **common))
    out.append(sig("headcount/epa-12849-jan-2026", "EPA staffing at 12,849 at end of January 2026 (-24% in a year)",
                   targetId=actor("federal"),
                   measure={"name": "headcount", "value": 12849, "unit": "employees", "ci95": None, "n": None, "denominator": "EPA employees",
                            "baseline": {"value": None, "ci95": None, "n": None, "note": "more than 4,000 higher a year earlier"}},
                   observed={"start": "2026-01-31", "end": "2026-01-31"}, comparison={"start": "2025-01-20", "end": "2025-01-20"},
                   source="LM-129", release="Inside Climate News analysis of OPM data, 2026-03-06",
                   corpus={"version": "OPM data via ICN", "sha256": None, "license": "news analysis (figures cited)"},
                   method="News analysis of OPM data (V1-03). The 30.3-year median service applies only to the ~2,000 who left at year-end 2025 (vs 10.8 years for remaining staff).",
                   crosswalkPath="agency headcount -> organization", direction="decline", dconf="high",
                   drivers=["fiscal", "policy-reform", "workforce-capacity", "demographic"], reliability="B", impact=3, sources=["LM-129"],
                   note="Top-of-ladder mechanism: tacit expertise left fastest at year-end 2025 (ADR-0008 s6 top-of-ladder loss).", **common))
    out.append(sig("headcount/usfs-seasonal-hiring-2025-2026", "USFS hired no non-fire seasonal staff in 2025; committed to 2,000 seasonals for 2026",
                   targetId=role("R02-field-resource-technician"),
                   measure={"name": "non_fire_seasonal_hires_committed", "value": 2000, "unit": "seasonal positions (2026 commitment)", "ci95": None,
                            "n": None, "denominator": "USFS seasonal hiring", "baseline": {"value": 0, "ci95": None, "n": None, "note": "2025 non-fire seasonal hires"}},
                   observed={"start": "2026-02-12", "end": "2026-03-18"}, comparison={"start": "2025-01-01", "end": "2025-12-31"},
                   source="LM-131", release="Congressional letter 2026-03-18 relaying agency statements",
                   corpus={"version": "letter text", "sha256": None, "license": "US government work"},
                   method="Congressional letter relaying USFS statements (V1-04); no USDA primary release located.",
                   crosswalkPath="GS-0462 forestry technician seasonal -> R02 federal variant (entry level)", direction="decline", dconf="med",
                   drivers=["fiscal", "workforce-capacity"], reliability="C", impact=3, sources=["LM-131"],
                   note="Entry-path-at-risk signal for COR-1; formation substrate disrupted by budget, not AI.", **common))
    return out


# ---------------------------------------------------------------------------------------------- postings (Conservation Job Board)
def postings_signals():
    out = []
    common = dict(observed={"start": "2025-03-01", "end": "2025-09-30"}, comparison={"start": "2024-03-01", "end": "2024-09-30"},
                  geography="US", sectorActor="ngo", source="LM-130", release="National Parks Traveler 2025-11-10",
                  corpus={"version": "Conservation Job Board postings (one board)", "sha256": None, "license": "figures cited"},
                  method="Year-over-year change in postings on one board, with a survey of 337 conservation employers (V1-14). Scope is one board, not the conservation labour market.",
                  steep="economic", family="postings-pds", indep="conservation-job-board", matchType="related", novelty=1,
                  reliability="C", corroboration=1, sources=["LM-130"])
    out.append(sig("postings/conservation-job-board-internships-2025", "Paid conservation internship postings fell 43.8% year over year (Mar-Sep 2025, one board)",
                   targetId=role("R02-field-resource-technician"),
                   measure={"name": "postings_yoy_change", "value": -0.438, "unit": "share", "ci95": None, "n": None, "denominator": "paid internship postings, same months 2024"},
                   crosswalkPath="internship postings -> entry level of R02 (feeder)", direction="decline", dconf="med",
                   drivers=["fiscal"], impact=2, signposts=["vocab:scenarios#SP-03"], **common))
    out.append(sig("postings/conservation-job-board-americorps-2025", "AmeriCorps conservation positions posted fell 42% year over year (Mar-Sep 2025, one board)",
                   targetId=role("R01-conservation-corps-member"),
                   measure={"name": "postings_yoy_change", "value": -0.42, "unit": "share", "ci95": None, "n": None, "denominator": "AmeriCorps postings, same months 2024"},
                   crosswalkPath="AmeriCorps conservation postings -> R01", direction="decline", dconf="med",
                   drivers=["fiscal", "policy-reform"], impact=2, signposts=["vocab:scenarios#SP-03"],
                   note="2025 grant terminations were largely reinstated in plaintiff jurisdictions and settled for FY2026 (driver events); re-read in the 2026 window.", **common))
    out.append(sig("postings/conservation-job-board-all-2025", "All conservation postings fell 29.4% year over year (Mar-Sep 2025, one board)",
                   targetId=actor("ngo"),
                   measure={"name": "postings_yoy_change", "value": -0.294, "unit": "share", "ci95": None, "n": None, "denominator": "all postings, same months 2024"},
                   crosswalkPath="board-wide -> organization", direction="decline", dconf="med", drivers=["fiscal", "policy-reform"], impact=2,
                   signposts=["vocab:scenarios#SP-03"], **common))
    return out


# ---------------------------------------------------------------------------------------------- deployment and capability: review tooling
def review_tooling_signals():
    out = []
    out.append(sig("deployment/permitting-ai-shared-services", "PNNL PermitAI shared services: SearchNEPA available to federal NEPA reviewers; DraftNEPABench released",
                   targetId=wf("WF-REVIEW"),
                   measure={"name": "shared_ai_services_available_to_federal_reviewers", "value": 1, "unit": "service in use (SearchNEPA)", "ci95": None,
                            "n": None, "denominator": "PermitAI modules (SearchNEPA, CommentNEPA, WriteNEPA, EngageNEPA, PermitCE, PermitReg, PermitLex)"},
                   observed={"start": "2025-05-02", "end": "2026-06-29"}, geography="US", sectorActor="federal", source="LM-110",
                   release="PNNL PermitAI project page; news release 2026-06-29", corpus={"version": "project pages", "sha256": None, "license": "US government work"},
                   method="Programme pages read in V2-08. Production or beta status of each module NOT confirmed; '1-5 hours saved per EIS subsection' NOT confirmed; NEPATEC 3.0 release NOT confirmed. DraftNEPABench: 102 test cases from 19 agencies (with OpenAI).",
                   crosswalkPath="tool class 'AI search, comment analysis and drafting for environmental review' (L4, DC lane) -> WF-REVIEW",
                   matchType="related", direction="augment", dconf="low", drivers=["AI", "policy-reform"], steep="technological", novelty=2,
                   reliability="B", corroboration=1, family="deployment", indep="pnnl-permitai", impact=3, registered=False,
                   sources=["LM-110", "SC-009"],
                   note="Reclassified from SC's PI-TECH-04 (tools are L4, not instruments). Availability is not registered deployment: the 2025 OMB inventory shows 0 of 5 review/permitting use cases deployed."))
    out.append(sig("capability/draftnepabench-coding-agents", "Benchmark of AI agents drafting EIS sections (DraftNEPABench, PNNL with OpenAI)",
                   targetId=wf("WF-REVIEW"),
                   measure={"name": "benchmark_test_cases", "value": 102, "unit": "test cases", "ci95": None, "n": 19, "denominator": "contributing agencies"},
                   observed={"start": "2026-05-27", "end": "2026-06-29"}, geography="US", sectorActor="federal", source="LM-110",
                   release="Presented 2026-05-27/29; PNNL release 2026-06-29", corpus={"version": "DraftNEPABench", "sha256": None, "license": "not checked"},
                   method="Capability evidence only (benchmark exists); performance results not read. Vendor co-developed.",
                   crosswalkPath="benchmark task 'draft EIS subsection' -> production half of split review tasks (WP-05 split, FS Futures Wheel)",
                   matchType="related", direction="automate", dconf="low", drivers=["AI"], steep="technological", novelty=3, reliability="B",
                   corroboration=1, family="capability", indep="pnnl-openai-draftnepabench", impact=3, sources=["LM-110", "DC-032"],
                   note="Supports watch item DC-CAND-17. 'Automate' here is the benchmark's aim, not an observed outcome."))
    return out


# ---------------------------------------------------------------------------------------------- policy watch signals (pre-publication)
def policy_watch_signals():
    out = []
    out.append(sig("policy/nhpa-s106-nprm-at-oira", "Section 106 regulations rewrite: ACHP voted to advance an NPRM (2026-07-24); at OIRA; unpublished",
                   targetId="seed:ins/nhpa-s106-regs",
                   measure={"name": "rulemaking_stage", "value": 0, "unit": "published proposals (0 = pre-publication at OIRA)", "ci95": None, "n": None, "denominator": None},
                   observed={"start": "2026-07-24", "end": "2026-10-09"}, geography="US", sectorActor="federal", source="LM-112",
                   release="Kelley Drye 2026-09-11; ACHP news through 2026-10-09", corpus={"version": "secondary + agency news index", "sha256": None, "license": "cited"},
                   method="Verified V2-14. Reported draft content (single agency-prepared report; 'address' replacing avoid/minimize/mitigate; narrower area of potential effects; discretionary public participation) is pre-publication and can change at OIRA.",
                   crosswalkPath="instrument -> DM-07 historic-preservation-review -> sensitivity edges (computed)", matchType="close",
                   direction="reshape", dconf="low", drivers=["policy-reform"], steep="political", novelty=2, reliability="B", corroboration=1,
                   family="policy", indep="federal-register-pipeline", impact=3, sources=["LM-112"],
                   note="When NEPA accelerates, s.106 and ESA review become the critical path (SC). Final rule considered unlikely before 2027. Re-check Federal Register before publication; ACHP meets 2026-11-10."))
    out.append(sig("policy/faa-part-108-final-at-oira", "FAA Part 108 BVLOS final rule at OIRA since 2026-07-10; unpublished as of 2026-10-21",
                   targetId="seed:ins/faa-part-108",
                   measure={"name": "rulemaking_stage", "value": 0, "unit": "published final rules (0 = at OIRA)", "ci95": None, "n": None, "denominator": None},
                   observed={"start": "2026-07-10", "end": "2026-10-21"}, geography="US", sectorActor="federal", source="LM-116",
                   release="Trade press 2026-09-08 and 2026-10-21", corpus={"version": "trade press", "sha256": None, "license": "cited"},
                   method="Verified V2-17 from trade press; no final rule found in Federal Register searches. EO 14307's 2026-02-01 deadline passed.",
                   crosswalkPath="instrument -> DM-17 operator-certification, DM-14 -> drone programme roles (FS CM-2 trigger)", matchType="close",
                   direction="reshape", dconf="low", drivers=["policy-reform", "sensing-tech"], steep="political", novelty=1, reliability="C",
                   corroboration=2, family="policy", indep="federal-register-pipeline", impact=2, sources=["LM-116", "FS-022"],
                   signposts=["vocab:scenarios#SP-09"],
                   note="Scenario signpost for sensing timing; FS contingent move CM-2 (BVLOS programme leads) waits on publication."))
    return out


# ---------------------------------------------------------------------------------------------- FS weak signals supporting watch items and signposts
def foresight_signals():
    """A subset of FS weak_signals.csv recoded as ChangeSignal records because watch items and signposts cite them.
    FS remains owner of the full weak-signal register; the rest migrate in FS's monthly scan."""
    out = []
    fs = dict(geography="US", release="docs/research/strategic-foresight/weak_signals.csv (2026-10-23)",
              corpus={"version": "FS weak_signals.csv", "sha256": sha256_file(os.path.join(ROOT, "docs/research/strategic-foresight/weak_signals.csv")),
                      "license": "CC0-1.0 (team research)"},
              method="Recoded from FS weak-signal register (coding per horizon_scanning_protocol.md s6); single-source event signal.",
              matchType="related", corroboration=1)
    rows = [
        # key, WS, label, targetType, target, measure(name,value,unit,denominator), observed date, sectorActor, direction, drivers, steep, novelty, rel, family, indep, impact, sources, signposts, note
        ("ws-29-mercor-agent-training", "WS-29", "AI-training marketplace recruits experienced agency and consulting environmental experts to build agent training environments",
         "work-function", wf("WF-REVIEW"), ("expert_task_rate_usd", 1150, "USD per task (lower bound of 1,150-1,450)", "one listing"), "2026-06-12", "private",
         "automate", ["AI"], "technological", 3, "C", "postings-pds", "mercor-listing", 3, ["FS-038"], None,
         "Leading indicator that agentic AI for permitting, remediation and ESG/GHG reporting is being trained now; also an income path for displaced experts. Supports DC-CAND-17."),
        ("ws-13-consulting-ai-comment-tools", "WS-13", "Consulting firms deploy AI comment-sorting tools and explore AI scoping",
         "work-function", "vocab:work_functions#MODE-ENGAGE", ("firms_reported", 1, "firms named in source (e.g. one large consultancy)", "consulting firms"), "2025-10-07", "private",
         "augment", ["AI", "market"], "economic", 2, "C", "deployment", "trade-press-consulting", 2, ["FS-008"], None,
         "Entry-level comment analysis and drafting automated in the private delivery chain first. Supports PS-C19 (pricing and disclosure of AI-augmented services)."),
        ("ws-26-carep-credential", "WS-26", "First AI-readiness credential for environmental review professionals launched (university with a training provider)",
         "work-function", wf("WF-REVIEW"), ("credentials_launched", 1, "credential", "environmental-review AI credentials"), "2026-04-15", "academic",
         "new", ["AI"], "social", 3, "B", "postings-pds", "credential-launch", 2, ["FS-027"], None,
         "Tool-fluency credentials begin to shape PDs; EMST can anchor durable content (L4 vs L1 typing)."),
        ("ws-08-disaster-database-discontinued", "WS-08", "Federal billion-dollar disaster database ended; revived by a nonprofit with its former federal lead",
         "work-function", wf("WF-ASSESS"), ("datasets_discontinued_then_revived", 1, "dataset", "federal climate-risk datasets"), "2025-11-03", "ngo",
         "reshape", ["fiscal", "policy-reform", "climate"], "environmental", 2, "B", "policy", "fs-data-discontinuity", 2, ["FS-037"], ["vocab:scenarios#SP-11"],
         "Public climate-risk data function migrates to a nonprofit refugium. Supports FS-C16."),
        ("ws-10-obbba-ira-rescissions", "WS-10", "Unobligated IRA conservation, NPS hiring and USFS NEPA staffing funds rescinded",
         "organization", actor("federal"), ("programme_lines_rescinded", 3, "named programme lines (UCF, NPS hiring, USFS NEPA staff)", "IRA lines cited by FS-036"), "2025-07-04", "federal",
         "decline", ["fiscal", "policy-reform"], "political", 1, "B", "policy", "fs-fiscal", 3, ["FS-036"], None,
         "Removes funded hiring lines and implementation pipelines; also removes community forestry technical-assistance capacity (FS-C16)."),
        ("ws-31-firesat-operational", "WS-31", "Three operational FireSat satellites launched; early-adopter data Q4 2026; global access 2028",
         "role-profile", role("R08-fire-intelligence-analyst"), ("operational_satellites", 3, "satellites", "planned constellation of 50+"), "2026-07-07", "ngo",
         "new", ["sensing-tech", "AI"], "technological", 2, "B", "deployment", "earth-fire-alliance", 3, ["FS-011"], ["vocab:scenarios#SP-08"],
         "Continuous detection data arrives before agencies have defined roles to use it (FS CM-3 trigger: agency ingestion with known access terms)."),
        ("ws-36-fire-season-2026", "WS-36", "2026 fire season at 63,884 fires and 9.0 million acres YTD (133% and 145% of the 10-year average) as of 2026-10-11",
         "role-profile", role("R06-wildland-fire-operations"), ("acres_burned_share_of_10yr_avg", 1.45, "ratio to 10-year average", "10-year average YTD acres"), "2026-10-11", "federal",
         "grow", ["climate"], "environmental", 1, "A", "workload", "nifc-imsr", 3, ["FS-034"], ["vocab:scenarios#SP-10"],
         "Predetermined pressure in all scenarios; a workload signal, not a skill-change signal (family workload never counts toward the evidence rule; CR-LM-001)."),
        ("ws-14-epa-ai-strategy", "WS-14", "EPA AI strategy under M-25-21: AI literacy, AI competencies in recruitment, enterprise AI team, high-impact AI controls",
         "organization", actor("federal"), ("strategy_published", 1, "strategy", "agency AI strategies"), "2025-10-01", "federal",
         "new", ["AI", "policy-reform"], "political", 2, "A", "policy", "agency-ai-strategy", 2, ["FS-031"], None,
         "AI governance roles formalized inside a regulator (relevant to R32 environmental AI assurance officer)."),
        ("ws-33-gao-opm-capacity", "WS-33", "GAO: OPM headcount -35% since Dec 2024; HR Solutions -36%; Workforce Policy -45%",
         "organization", actor("federal"), ("headcount_change_share", -0.35, "share", "OPM employees Dec 2024"), "2026-07-20", "federal",
         "decline", ["fiscal", "policy-reform", "workforce-capacity"], "political", 2, "A", "headcount", "gao-opm", 2, ["FS-029"], ["vocab:scenarios#SP-01"],
         "The classification and skills-policy machinery EMST's first users rely on is thinned (adoption-relevant)."),
    ]
    for (key, ws, label, _ttype, target, meas, date, sact, direction, drivers, steep, novelty, rel, family, indep, impact, sources, signposts, note) in rows:
        out.append(sig("foresight/" + key, label, targetId=target,
                       measure={"name": meas[0], "value": meas[1], "unit": meas[2], "ci95": None, "n": None, "denominator": meas[3]},
                       observed={"start": date, "end": date}, sectorActor=sact, crosswalkPath="FS %s -> %s" % (ws, target), source=sources[0],
                       direction=direction, dconf="low", drivers=drivers, steep=steep, novelty=novelty, reliability=rel, family=family,
                       indep=indep, impact=impact, sources=sources, signposts=signposts, note=note, **fs))
    # DC-CAND-17 deployment evidence: agentic use cases in USDA/DOI/EPA inventory (DC-001)
    out.append(sig("deployment/agentic-use-cases-usda-doi-epa-2025", "Agentic AI use cases in the 2025 USDA, DOI and EPA inventories: 8 of 438, 2 deployed (both administrative)",
                   targetId=wf("WF-ASSESS"),
                   measure={"name": "agentic_use_cases_deployed", "value": 2, "unit": "deployed agentic use cases (administrative)", "ci95": None, "n": 8,
                            "denominator": "agentic-classed use cases among 438 USDA/DOI/EPA use cases"},
                   observed={"start": "2025-01-01", "end": "2025-12-22"}, geography="US", sectorActor="federal", source="DC-001",
                   release="2025 inventory (DC Phase 2 extract)", corpus={"version": "OMB 2025 inventory", "sha256": None, "license": "US government work"},
                   method="DC Phase 2 count (DC-001). Environmental agentic cases are pilots or pre-deployment.",
                   crosswalkPath="inventory classification 'agentic' -> analysis workflows (WF-ASSESS) generic", matchType="related",
                   direction="new", dconf="low", drivers=["AI"], steep="technological", novelty=3, reliability="A", corroboration=1,
                   family="deployment", indep="ombegov-ai-inventory", impact=2, registered=False, sources=["DC-001"],
                   note="Supports DC-CAND-17; environmental deployments not yet evidenced (S)."))
    out.append(sig("policy/omb-m-26-04-llm-contract-terms", "OMB M-26-04 requires LLM solicitations to include acceptable-use, model/system/data cards and feedback terms",
                   targetId="seed:ins/omb-m-26-04",
                   measure={"name": "llm_solicitation_terms_required", "value": 1, "unit": "memo in force (1 = requirement applies)", "ci95": None, "n": None, "denominator": "OMB memoranda governing LLM procurement"},
                   observed={"start": "2025-12-11", "end": "2026-03-11"}, geography="US", sectorActor="federal", source="LM-111",
                   release="M-26-04 (2025-12-11)", corpus={"version": "memo text", "sha256": None, "license": "US government work"},
                   method="Policy signal (V2-09). Disclosure of AI use and validation becomes a contract term for LLM purchases; consultancies selling AI-augmented services face disclosure terms.",
                   crosswalkPath="instrument -> DM-14 -> contractor service disclosure (PS-C19)", matchType="related", direction="reshape",
                   dconf="low", drivers=["policy-reform", "AI", "market"], steep="political", novelty=2, reliability="A", corroboration=1,
                   family="policy", indep="federal-register-pipeline", impact=2, sources=["LM-111"], note="Supports PS-C19."))
    return out


# ---------------------------------------------------------------------------------------------- scenario signposts (FS dashboard, vocab/scenarios.yaml)
def signpost_signals():
    """Readings of the FS signpost dashboard (vocab/scenarios.yaml signposts, proposed notations SP-01..SP-12 in
    CR-LM-001, in the order they appear in the vocabulary). pointsToward records which scenarios or axis poles the
    reading points to; it is FS's call at quarterly triage, coded here as a draft."""
    out = []

    def sp(key, label, spid, measure, observed, sact, source, release, method, direction, drivers, rel, family, indep, impact,
           sources, points, note):
        r = sig("signpost/" + key, label, targetId="vocab:scenarios#" + spid, measure=measure,
                observed=observed, geography="US", sectorActor=sact, source=source, release=release,
                corpus={"version": release, "sha256": None, "license": "cited"},
                method=method, crosswalkPath="signpost reading -> %s (vocab/scenarios.yaml signposts)" % spid, matchType="close",
                direction=direction, dconf="low", drivers=drivers, steep="political", novelty=1, reliability=rel, corroboration=1,
                family=family, indep=indep, impact=impact, sources=sources, signposts=["vocab:scenarios#" + spid], note=note,
                points=points)
        return r

    out.append(sp("sp-01-entry-share-federal", "Signpost SP-01 (AX-1): under-30 share of federal workforce 7.9% (Jan 2026) vs 8.9% (Sep 2024)", "SP-01",
                  {"name": "under_30_share", "value": 0.079, "unit": "share", "ci95": None, "n": None, "denominator": "federal civilian employees",
                   "baseline": {"value": 0.089, "ci95": None, "n": None}},
                  {"start": "2026-01-31", "end": "2026-01-31"}, "federal", "LM-128", "PPS to Jan 2026",
                  "Governmentwide proxy until series-level FWD pulls exist for 0401, 0408, 0460, 0486, 0028, 0819, 1315, 1340 (FH to finalize the list).",
                  "decline", ["fiscal", "policy-reform", "workforce-capacity"], "B", "headcount", "opm-ehri-fwd", 3, ["LM-128"],
                  ["AX-1:thin-fragmented", "SC3", "SC4"], "Entry cohorts are not being restored as of Jan 2026."))
    out.append(sp("sp-02-staffing-floor-fy2026", "Signpost SP-02 (AX-1): FY2026 Interior-Environment enacted at $42.56bn vs $26.85bn requested", "SP-02",
                  {"name": "enacted_to_request_ratio", "value": 1.59, "unit": "ratio (42.56 / 26.85)", "ci95": None, "n": None, "denominator": "President's request"},
                  {"start": "2026-01-23", "end": "2026-01-23"}, "federal", "LM-126", "CRS R48726 (2026-03-19)",
                  "Appropriations as stabilizer (V1-15); USFS staffing-maintenance language per FS WS-19 (FS-049) not re-verified.",
                  "stable", ["fiscal"], "A", "policy", "crs-appropriations", 3, ["LM-126", "FS-019", "FS-049"],
                  ["AX-1:rebuilt-coordinated", "SC1", "SC2"], "Congress as stabilizer; points toward rebuilt-coordinated only if staffing directives are enforced (money and staffing decouple)."))
    out.append(sp("sp-03-conservation-entry-postings", "Signpost SP-03 (AX-1): conservation internship postings -43.8% and AmeriCorps positions -42% (Mar-Sep 2025 vs 2024, one board)", "SP-03",
                  {"name": "internship_postings_yoy_change", "value": -0.438, "unit": "share", "ci95": None, "n": None, "denominator": "same months 2024"},
                  {"start": "2025-03-01", "end": "2025-09-30"}, "ngo", "LM-130", "National Parks Traveler 2025-11-10",
                  "One board; semi-annual cadence; the 2026 reading is due.", "decline", ["fiscal", "policy-reform"], "C", "postings-pds",
                  "conservation-job-board", 2, ["LM-130"], ["AX-1:thin-fragmented", "SC4"], "Recovery of internship share would be an SC1/SC2 signpost."))
    out.append(sp("sp-05-high-impact-ai-env-departments", "Signpost SP-05 (AX-2): high-impact AI use cases in the 2025 inventory - DOI 0, USDA 4, EPA 2", "SP-05",
                  {"name": "high_impact_use_cases", "value": 6, "unit": "use cases (DOI 0 + USDA 4 + EPA 2)", "ci95": None, "n": 438,
                   "denominator": "use cases in DOI (247), USDA (162) and EPA (29)"},
                  {"start": "2025-01-01", "end": "2025-12-22"}, "federal", "LM-138", "OMB 2025 inventory README (2026-04-13)",
                  "Department totals from the README (V4-15). Environmental review/permitting: 0 of 5 bureau use cases deployed (LM extract).",
                  "stable", ["AI"], "A", "deployment", "ombegov-ai-inventory", 3, ["LM-138"],
                  None, "AI is not yet in high-stakes environmental decisions; consistent with an early trusted path or a contested one. Next reading: 2026 inventory."))
    out.append(sp("sp-08-firesat-access", "Signpost SP-08 (SC1/SC3): three operational FireSat satellites; early-adopter data from Q4 2026; global access 2028", "SP-08",
                  {"name": "operational_satellites", "value": 3, "unit": "satellites", "ci95": None, "n": None, "denominator": "planned 50+"},
                  {"start": "2026-07-07", "end": "2026-07-09"}, "ngo", "FS-011", "Earth Fire Alliance 2026-07-09",
                  "Announcement (FS-011); data access terms not yet read.", "new", ["sensing-tech"], "B", "deployment", "earth-fire-alliance", 2,
                  ["FS-011"], ["SC1", "SC3"], "CM-3 trigger is agency ingestion with known access terms; proprietary access would point to SC3."))
    out.append(sp("sp-09-part-108", "Signpost SP-09 (sensing timing): FAA Part 108 final rule at OIRA since 2026-07-10, unpublished as of 2026-10-21", "SP-09",
                  {"name": "final_rule_published", "value": 0, "unit": "boolean", "ci95": None, "n": None, "denominator": None},
                  {"start": "2026-07-10", "end": "2026-10-21"}, "federal", "LM-116", "trade press 2026-10-21", "V2-17 (trade press).",
                  "stable", ["policy-reform", "sensing-tech"], "C", "policy", "federal-register-pipeline", 2, ["LM-116"],
                  None, "FS CM-2 (BVLOS programme leads) waits on publication."))
    out.append(sp("sp-10-fire-season-2026", "Signpost SP-10 (predetermined pressure): 2026 acres burned at 145% of the 10-year average YTD (2026-10-11)", "SP-10",
                  {"name": "acres_share_of_10yr_avg", "value": 1.45, "unit": "ratio", "ci95": None, "n": None, "denominator": "10-year average YTD acres"},
                  {"start": "2026-01-01", "end": "2026-10-11"}, "federal", "FS-034", "NIFC IMSR 2026-10-11", "NIFC situation report (FS-034).",
                  "grow", ["climate"], "A", "workload", "nifc-imsr", 3, ["FS-034"], ["SC4"],
                  "Predetermined in all scenarios; SC4 risk of burnout and ladder breaks."))
    out.append(sp("sp-11-discontinued-datasets", "Signpost SP-11 (SC3/SC4): a federal disaster-cost dataset discontinued and revived outside government (2025)", "SP-11",
                  {"name": "datasets_discontinued_identified", "value": 1, "unit": "datasets", "ci95": None, "n": None, "denominator": "not a census"},
                  {"start": "2025-01-01", "end": "2025-11-03"}, "ngo", "FS-037", "Climate Central 2025-11-03",
                  "Single identified case (FS-037); no systematic tracker read.", "decline", ["fiscal", "policy-reform"], "B", "policy",
                  "fs-data-discontinuity", 2, ["FS-037"], ["SC3", "SC4"], "Data continuity outside government; DE mirrors critical series (ADR-0028 s4)."))
    return out


def build():
    groups = {
        "data/v2/signals/2026/openlmp.jsonl": openlmp_signals(),
        "data/v2/signals/2026/omb-ai-inventory-2025.jsonl": omb_signals(),
        "data/v2/signals/2026/opm-headcount.jsonl": headcount_signals(),
        "data/v2/signals/2026/conservation-job-board.jsonl": postings_signals(),
        "data/v2/signals/2026/review-tooling.jsonl": review_tooling_signals(),
        "data/v2/signals/2026/policy-watch.jsonl": policy_watch_signals(),
        "data/v2/signals/2026/foresight.jsonl": foresight_signals(),
        "data/v2/signals/2026/scenario-signposts.jsonl": signpost_signals(),
    }
    try:
        import wp10_web
        groups.update(wp10_web.build_groups())
    except ImportError:
        pass
    n = 0
    held = 0
    for path, recs in groups.items():
        write_jsonl(path, recs)
        n += len(recs)
        held += sum(1 for r in recs if r.get("careFlag"))
    return {"ChangeSignal": n, "ChangeSignal_held_tribal": held}
