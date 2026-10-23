#!/usr/bin/env python3
"""Build the chart datasets for the flagship report "How environmental jobs are changing".

WP-14 (A10: AS with CP), EMST v2, 2026-10-23. Licence of this script: Apache-2.0.
The CSV outputs are CC BY 4.0 as part of the report; third-party values keep their own
terms and are credited in each row (docs/governance/LICENSING.md section 5).

Run from the repository root:
    python3 -I docs/package/report/figures/build_figures.py

Rules this script enforces (WP-14 acceptance; ADR-0027; PROJECT_LEAD_DECISIONS Q7):
  * No EMST agent rating (raterType llm), no v1 value and no craft blend is charted.
  * No values derived from third-party index datasets whose licence the V-pass has not
    recorded (Eloundou et al. replication labels; Microsoft results files): they carry
    LicenseRef-EMST-third-party-index-derived and are excluded from release outputs
    (ADR-0013 amendment, CR-LM-002). The exposure-profile chart is therefore NOT built.
  * Tribal-flagged or held records are excluded (ADR-0007 section D); the script fails
    if one would be written.
  * Every hard-coded value is checked against the text of the verification record it
    comes from, so a later correction to that record breaks the build instead of
    silently diverging.
  * Deterministic: same inputs, same outputs.
"""
import csv
import glob
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
OUT = os.path.dirname(os.path.abspath(__file__))
VER = os.path.join(ROOT, "docs", "research", "_verification")
LM = os.path.join(ROOT, "docs", "research", "labor-market-ai-impact")
SIG = os.path.join(ROOT, "data", "v2", "signals", "2026")

AS_OF = "2026-10-23"


# ---------------------------------------------------------------- helpers
def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_csv(name, header, rows):
    path = os.path.join(OUT, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow([r.get(h, "") for h in header])
    return path


KEY_FACTS = {r["fact_id"]: r for r in read_csv(os.path.join(VER, "ALL_key_facts.csv"))}
QUEUE = {}
for r in read_csv(os.path.join(VER, "ALL_queue_results.csv")):
    QUEUE.setdefault(r["item_id"], r)
CLAIMS = {r["claim_id"]: r for r in read_csv(os.path.join(ROOT, "docs", "methods", "claims_register.csv"))}


def check(source_id, *needles):
    """Fail the build unless every needle appears in the verification text for source_id."""
    if source_id in KEY_FACTS:
        text = KEY_FACTS[source_id]["correct_statement"] + " " + KEY_FACTS[source_id]["note"]
        status = KEY_FACTS[source_id]["verification_status"]
    elif source_id in QUEUE:
        text = QUEUE[source_id]["finding"]
        status = QUEUE[source_id]["verification_status"]
    elif source_id in CLAIMS:
        text = CLAIMS[source_id]["claim"]
        status = CLAIMS[source_id]["status"]
    else:
        sys.exit(f"build_figures: unknown verification id {source_id}")
    if status not in ("verified", "corrected", "superseded", "verified-partial", "derived"):
        sys.exit(f"build_figures: {source_id} has status {status}; not usable")
    for n in needles:
        if n not in text:
            sys.exit(f"build_figures: '{n}' not found in verification record {source_id}; re-check the figure")
    return status


def no_tribal(rec):
    flags = (rec.get("careFlag"), rec.get("tribalPrograms"), rec.get("indigenousDataFlag"))
    if any(flags) or rec.get("approvalStatus") == "pending-tribal-review":
        return False
    return True


INDEX = []


def register(fid, fname, headline, chart, source_note, tier="describe", evidence="E (external sources read and verified; see source_ids per row)"):
    INDEX.append({
        "figure_id": fid, "file": fname, "headline": headline, "suggested_chart_form": chart,
        "source_note": source_note, "use_tier": tier, "evidence_label": evidence, "as_of": AS_OF,
    })


# ---------------------------------------------------------------- F1 public capacity
def f1():
    sig = {d["id"]: d for d in read_jsonl(os.path.join(SIG, "opm-headcount.jsonl"))}
    for d in sig.values():
        assert no_tribal(d)
    fed = sig["seed:sig/headcount/federal-civilian-minus-12pct"]["measure"]
    check("V1-01", "2,313,216", "2,035,344", "12%")
    check("V1-02", "more than a quarter", "34.1%")
    check("V1-03", "12,849", "(24%)")
    check("LM-030", "23.8%")
    rows = [
        {"unit": "Federal civilian workforce (all agencies)", "measure": "net change in employees",
         "value_pct": round(100 * (fed["value"] - fed["baseline"]["value"]) / fed["baseline"]["value"], 1),
         "value_kind": "exact", "level_start": fed["baseline"]["value"], "level_end": fed["value"],
         "period_start": "2024-09", "period_end": "2026-01", "base": "on-board employees, PPS analysis of OPM data",
         "publisher": "Partnership for Public Service", "source_ids": "V1-01;WF-01"},
        {"unit": "USDA Forest Service", "measure": "net change in employees", "value_pct": -25.0,
         "value_kind": "lower bound (source says 'more than a quarter'; no exact figure published)",
         "period_start": "2024-09", "period_end": "2026-01", "base": "on-board employees, PPS analysis of OPM data",
         "publisher": "Partnership for Public Service", "source_ids": "V1-02;WF-02"},
        {"unit": "National Park Service", "measure": "net change in employees", "value_pct": -25.0,
         "value_kind": "lower bound (source says 'more than a quarter'; no exact figure published)",
         "period_start": "2024-09", "period_end": "2026-01", "base": "on-board employees, PPS analysis of OPM data",
         "publisher": "Partnership for Public Service", "source_ids": "V1-02;WF-02"},
        {"unit": "Federal park rangers (occupation)", "measure": "net change in employees", "value_pct": -34.1,
         "value_kind": "exact", "period_start": "2024-09", "period_end": "2026-01",
         "base": "on-board employees in the occupation, PPS analysis of OPM data",
         "publisher": "Partnership for Public Service", "source_ids": "V1-02;WF-02"},
        {"unit": "Environmental Protection Agency", "measure": "net change in employees", "value_pct": -24.0,
         "value_kind": "approximate (source: 'more than 4,000 (24%)')", "level_end": 12849,
         "period_start": "2025-01", "period_end": "2026-01", "base": "employees, Inside Climate News analysis of OPM data",
         "publisher": "Inside Climate News", "source_ids": "V1-03;WF-03"},
        {"unit": "USDA Natural Resources Conservation Service", "measure": "net change in employees", "value_pct": -23.8,
         "value_kind": "approximate", "period_start": "2024-09", "period_end": "2025-11",
         "base": "employees, Agri-Pulse analysis of OPM data (different period from PPS rows)",
         "publisher": "Agri-Pulse", "source_ids": "LM-030"},
    ]
    hdr = ["unit", "measure", "value_pct", "value_kind", "level_start", "level_end", "period_start", "period_end", "base", "publisher", "source_ids"]
    write_csv("f01_public_capacity_change.csv", hdr, rows)
    register("F01", "f01_public_capacity_change.csv",
             "Between Sep 2024 and Jan 2026 the federal civilian workforce fell 12%, and the two largest land-management agencies each lost more than a quarter of their staff: a fiscal and policy shock, not an AI effect.",
             "Dot plot of percentage change by unit, one row per unit, each labelled with its own period and base; lower-bound rows drawn as an open marker with an arrow; no bars, no ranking across bases; table beside the chart.",
             "Partnership for Public Service (OPM data, to Jan 2026); Inside Climate News (OPM data, Mar 6 2026); Agri-Pulse (OPM data, Jan 21 2026). Bases differ by row and must not be compared as one series; USDA OIG reports a different USFS figure (16% in 2025) on another base. Sector-wide figures exclude Tribal, state, local, NGO and private workforces.")


# ---------------------------------------------------------------- F2 AI by type x stage
def f2():
    rows = read_csv(os.path.join(LM, "omb_ai_inventory_env_bureaus_2025.csv"))
    check("OMB-02", "504", "61 of the 347")
    types = ["Classical ML", "Computer Vision", "Generative AI", "NLP", "Agentic AI", "Reinforcement Learning", "Other", "Not classified"]
    stages = ["Deployed", "Pilot", "Pre-deployment", "Retired", "Stage not reported"]
    grid = {(t, s): 0 for t in types for s in stages}
    for r in rows:
        t = r["classification"] or "Not classified"
        s = r["development_stage"] or "Stage not reported"
        grid[(t, s)] += 1
    out = []
    for t in types:
        rec = {"ai_type": t}
        for s in stages:
            rec[s] = grid[(t, s)]
        rec["total"] = sum(grid[(t, s)] for s in stages)
        out.append(rec)
    tot = {"ai_type": "All types"}
    for s in stages:
        tot[s] = sum(grid[(t, s)] for t in types)
    tot["total"] = len(rows)
    out.append(tot)
    assert tot["total"] == 504 and tot["Deployed"] == 61 and (tot["total"] - tot["Stage not reported"]) == 347
    hdr = ["ai_type"] + stages + ["total"]
    write_csv("f02_federal_env_ai_use_cases_type_by_stage.csv", hdr, out)
    register("F02", "f02_federal_env_ai_use_cases_type_by_stage.csv",
             "Most AI in federal environmental bureaus is classical machine learning for science work, and most of it is not yet deployed: 61 of the 347 use cases that report a stage are in production.",
             "Stacked horizontal bars by AI type (segments = development stage, Deployed first), with the 'stage not reported' segment shown hatched and labelled; table beside the chart.",
             "OMB 2025 Federal Agency AI Use Case Inventory (README as of Apr 13 2026), environmental bureaus of USDA, DOI, DOC (NOAA) and EPA as extracted by EMST LM (docs/research/labor-market-ai-impact/scripts/omb_inventory_env.py). 'Deployed' = development_stage 'Deployed' only; OMB's README pools deployed and piloted. NOAA reported no stages. Self-reported by agencies; registration is not use.")


# ---------------------------------------------------------------- F3 AI by function
def f3():
    rows = read_csv(os.path.join(LM, "omb_ai_inventory_env_function_counts.csv"))
    check("OMB-02", "0 of 5 NEPA/permitting use cases are deployed")
    out = []
    for r in rows:
        n, dep = int(r["n_use_cases"]), int(r["n_deployed"])
        out.append({"function_family": r["function_keyword_family"], "use_cases_all_stages": n,
                    "deployed": dep, "not_deployed_or_unreported": n - dep})
    out.sort(key=lambda x: (-x["use_cases_all_stages"], x["function_family"]))
    nepa = [x for x in out if x["function_family"].startswith("NEPA")][0]
    assert nepa["use_cases_all_stages"] == 5 and nepa["deployed"] == 0
    write_csv("f03_federal_env_ai_use_cases_by_function.csv",
              ["function_family", "use_cases_all_stages", "deployed", "not_deployed_or_unreported"], out)
    register("F03", "f03_federal_env_ai_use_cases_by_function.csv",
             "Species detection, remote sensing, water and fire lead federal environmental AI; none of the five use cases in NEPA, environmental review or permitting is deployed.",
             "Horizontal bars of use cases per function family with the deployed share as a darker inner bar; families overlap (keyword-classified), so no totals row; table beside the chart.",
             "OMB 2025 Federal Agency AI Use Case Inventory; EMST LM keyword classification of use-case names and descriptions (a use case can fall in more than one family). 'Deployed' = development_stage 'Deployed' only.")


# ---------------------------------------------------------------- F4 COTS drafting at scale
def f4():
    rows = read_csv(os.path.join(LM, "omb_cots_ai_env_departments_2025.csv"))
    check("V4-15", "consolidated COTS use cases")
    keep_dept = {"Department of Agriculture": "USDA", "Department of the Interior": "DOI", "Environmental Protection Agency": "EPA"}
    big = {"10,000-50,000", "50,000+"}
    kw = ("draft", "written communications", "summariz", "knowledge retrieval", "transcrib")
    out = []
    for r in rows:
        dept = keep_dept.get(r["Agency"])
        if not dept or r["Agency Use (Y/N)?"] != "Y" or r["Estimated # of Licenses/Users"] not in big:
            continue
        uc = r["AI Use Case"]
        if not any(k in uc.lower() for k in kw):
            continue
        out.append({"department": dept, "commercial_ai_use_case_category": uc,
                    "licence_or_user_band": r["Estimated # of Licenses/Users"]})
    out.sort(key=lambda x: (x["department"], x["commercial_ai_use_case_category"]))
    assert {x["department"] for x in out} == {"USDA", "DOI", "EPA"}
    write_csv("f04_commercial_genai_drafting_tools_at_scale.csv",
              ["department", "commercial_ai_use_case_category", "licence_or_user_band"], out)
    register("F04", "f04_commercial_genai_drafting_tools_at_scale.csv",
             "Commercial AI tools for drafting, summarizing, writing and search are licensed at 10,000 or more users in each of the three main federal environmental departments: availability at workforce scale, which is not the same as use.",
             "Small table (department x use-case category) with the licence band as the cell value; no chart needed. Product names are deliberately omitted.",
             "OMB 2025 consolidated COTS AI use cases (ombegov GitHub), rows for USDA, DOI and EPA marked in use with a band of 10,000+ licences or users. Licence bands are agency estimates; they measure availability, not frequency or quality of use.")


# ---------------------------------------------------------------- F5/F6 plan requirements
def f5_f6():
    recs = read_jsonl(os.path.join(SIG, "openlmp.jsonl"))
    check("PLAN-01", "30.7%", "2.7%", "22.2%", "1.8%")
    check("PLAN-02", "11.9 to 24.9", "4.7 to 5.0", "6.2 to 4.3")
    f5rows, f6rows = [], []
    for d in recs:
        if not no_tribal(d):
            continue  # Tribal touchpoints are quarantined (careFlag); TN decides how they are shown
        m = d["measure"]
        base, sens = m.get("baseline", {}), m.get("sensitivity", {})
        name = m["name"]
        row = {
            "measure": name.split(":")[-1].replace("_plan_equal", "").replace("_", " "),
            "unit": m["unit"],
            "rule_1982_plan_equal": base.get("value"), "rule_1982_ci95_low": (base.get("ci95") or [None, None])[0],
            "rule_1982_ci95_high": (base.get("ci95") or [None, None])[1], "rule_1982_n_plans": base.get("n"),
            "rule_2012_plan_equal": m.get("value"), "rule_2012_ci95_low": (m.get("ci95") or [None, None])[0],
            "rule_2012_ci95_high": (m.get("ci95") or [None, None])[1], "rule_2012_n_plans": m.get("n"),
            "rule_1982_component_weighted": sens.get("baselineValue"), "rule_2012_component_weighted": sens.get("value"),
            "signal_id": d["id"],
        }
        lo82, hi82 = row["rule_1982_ci95_low"], row["rule_1982_ci95_high"]
        lo12, hi12 = row["rule_2012_ci95_low"], row["rule_2012_ci95_high"]
        if None in (lo82, hi82, lo12, hi12):
            row["plan_equal_cis_overlap"] = "not computed"
        else:
            row["plan_equal_cis_overlap"] = "yes" if max(lo82, lo12) <= min(hi82, hi12) else "no"
        if name.startswith("monitoring_component_share"):
            row["measure"] = "monitoring components (share of plan components)"
            f5rows.append(row)
        else:
            f6rows.append(row)
    assert len(f5rows) == 1 and len(f6rows) == 9
    hdr = ["measure", "unit", "rule_1982_plan_equal", "rule_1982_ci95_low", "rule_1982_ci95_high", "rule_1982_n_plans",
           "rule_2012_plan_equal", "rule_2012_ci95_low", "rule_2012_ci95_high", "rule_2012_n_plans",
           "rule_1982_component_weighted", "rule_2012_component_weighted", "plan_equal_cis_overlap", "signal_id"]
    write_csv("f05_plan_monitoring_share_by_rule.csv", hdr, f5rows)
    f6rows.sort(key=lambda x: x["measure"])
    write_csv("f06_plan_content_rates_by_rule.csv", hdr, f6rows)
    note = ("OpenLMP 0.1.0 plan components (catalog 2026-10-21, CC0), derived by EMST LM (docs/methods/scripts/wp10_lmp.py). "
            "Cross-era comparison of different plans, not a time series; about 95% of components are USDA Forest Service plans, all in western states. "
            "Headline weights each plan equally (95% CI = mean +/- 1.96 SE); component-weighted values are the sensitivity check. Mentions measure what plans name, not obligations. "
            "Tribal touchpoints are excluded pending Tribal Advisory Council review.")
    register("F05", "f05_plan_monitoring_share_by_rule.csv",
             "Forest plans written under the 2012 Planning Rule devote about 31% of their components to monitoring, against about 3% under the 1982 rule: a durable demand for monitoring design, evaluation and reporting.",
             "Paired dot plot (1982 rule vs 2012 rule) with 95% CI whiskers for the plan-equal values; component-weighted values as hollow markers; table beside the chart.", note)
    register("F06", "f06_plan_content_rates_by_rule.csv",
             "Newer plans name climate, data and models, and carbon far more often; the apparent tripling of coordination is mostly a weighting artifact, with only partnership touchpoints rising (and weakly) when each plan counts equally.",
             "Small multiples, one panel per measure: 1982 vs 2012 plan-equal means with CI whiskers, component-weighted as hollow markers; panels where CIs overlap labelled 'not distinguishable'; table beside the chart.", note)


# ---------------------------------------------------------------- F7 BLS projections
def f7():
    recs = read_jsonl(os.path.join(SIG, "bls-ep-2025-35.jsonl"))
    check("BLS-01", "+3.5%", "data scientists +34.6%")
    reg = CLAIMS["BLS-02"]["claim"]
    wanted = {  # SOC -> (label in BLS-02 claim text, SOC major group)
        "19-2041": ("environmental scientists +6%", "19 Life, physical and social science"),
        "17-2081": ("environmental engineers +6.3%", "17 Architecture and engineering"),
        "19-1031": ("conservation scientists +5.3%", "19 Life, physical and social science"),
        "19-1032": ("foresters +2.2%", "19 Life, physical and social science"),
        "19-1023": ("zoologists and wildlife biologists +3.6%", "19 Life, physical and social science"),
        "19-4042": ("environmental science and protection technicians +7%", "19 Life, physical and social science"),
        "45-4011": ("forest and conservation workers -2%", "45 Farming, fishing and forestry"),
        "51-8031": ("water and wastewater operators -6%", "51 Production"),
        "33-2011": ("firefighters +4%", "33 Protective service"),
        "11-9121": ("natural sciences managers +8.2%", "11 Management"),
        "13-1041": ("compliance officers +3.8%", "13 Business and financial operations"),
        "15-2051": (None, "15 Computer and mathematical"),
    }
    seen = {}
    for d in recs:
        soc = d["id"].split("/")[2]
        if soc in wanted and soc not in seen:
            seen[soc] = d
    out = []
    for soc, (needle, grp) in wanted.items():
        d = seen[soc]
        v = d["measure"]["value"]
        if needle:
            assert needle in reg, f"BLS-02 claim text lacks '{needle}'"
            expect = float(needle.rsplit(" ", 1)[1].replace("%", "").replace("+", ""))
            assert abs(expect - v) < 1e-9, (soc, v, expect)
            src = "BLS-02;" + ";".join(d["provenance"]["sources"])
        else:
            assert abs(v - 34.6) < 1e-9
            src = "BLS-01;V4-07"
        occ = d["prefLabel"]["en"].split(" for ", 1)[1].split(" (")[0]
        out.append({"soc_2018": soc, "occupation": occ, "soc_major_group": grp, "projected_change_2025_35_pct": v,
                    "all_occupations_pct": d["measure"]["baseline"]["value"],
                    "relative_to_all_occupations": "faster" if v > 3.5 + 1 else ("slower or declining" if v < 3.5 - 1 else "about average"),
                    "source_ids": src})
    out.sort(key=lambda x: -x["projected_change_2025_35_pct"])
    write_csv("f07_bls_projections_2025_35.csv",
              ["soc_2018", "occupation", "soc_major_group", "projected_change_2025_35_pct", "all_occupations_pct", "relative_to_all_occupations", "source_ids"], out)
    register("F07", "f07_bls_projections_2025_35.csv",
             "Official 2025-35 projections show analytical, engineering and technician occupations growing faster than the +3.5% all-occupation average, foresters slower, and forest and conservation workers and water operators declining.",
             "Dot plot of projected percentage change by occupation with a vertical reference line at +3.5%; 'about average' band of +/-1 point shaded; data scientists shown with an axis break; table beside the chart.",
             "U.S. Bureau of Labor Statistics, Employment Projections 2025-35 (released Aug 27 2026), Table 1.2 and Occupational Outlook Handbook pages. Projections are context, not evidence of skill change; BLS does not attribute these occupation projections to AI. The 'about average' band (+/-1 point) is an EMST display convention, not a BLS category. Wildland firefighters are not counted separately.")


# ---------------------------------------------------------------- F8 entry-path indicators
def f8():
    cjb = {d["id"]: d for d in read_jsonl(os.path.join(SIG, "conservation-job-board.jsonl"))}
    hc = {d["id"]: d for d in read_jsonl(os.path.join(SIG, "opm-headcount.jsonl"))}
    check("V1-14", "29.4%", "43.8%", "42%")
    check("V1-04", "did not hire seasonal staff in 2025", "2,000 seasonals")
    check("V1-02", "8.9%", "7.9%")
    check("LM-034", "fell by 22%")
    rows = []
    for key, lab in [("seed:sig/postings/conservation-job-board-all-2025", "All postings"),
                     ("seed:sig/postings/conservation-job-board-internships-2025", "Paid internship postings"),
                     ("seed:sig/postings/conservation-job-board-americorps-2025", "AmeriCorps position postings")]:
        m = cjb[key]["measure"]
        rows.append({"indicator": f"Conservation Job Board: {lab}", "value": round(100 * m["value"], 1), "unit": "% change year over year",
                     "period": "Mar 1-Sep 30 2025 vs same months 2024", "scope": "one job board (not the whole conservation labour market)",
                     "source_ids": "V1-14;WF-05"})
    u30 = hc["seed:sig/headcount/federal-under-30-share"]["measure"]
    rows.append({"indicator": "Federal civilian workforce: share of employees under 30", "value": round(100 * u30["value"], 1),
                 "unit": "percent of employees (was {:.1f} in Sep 2024)".format(100 * u30["baseline"]["value"]),
                 "period": "Jan 2026", "scope": "all federal civilian employees", "source_ids": "V1-02;WF-02"})
    sh = hc["seed:sig/headcount/usfs-seasonal-hiring-2025-2026"]["measure"]
    rows.append({"indicator": "USDA Forest Service: non-fire seasonal hires", "value": sh["baseline"]["value"], "unit": "hires in 2025",
                 "period": "2025 hiring season", "scope": "USFS non-fire seasonal positions (congressional letter relaying agency statements)",
                 "source_ids": "V1-04;WF-04"})
    rows.append({"indicator": "USDA Forest Service: seasonal positions committed for 2026", "value": sh["value"], "unit": "positions committed (Feb 12 2026)",
                 "period": "2026 hiring season", "scope": "USFS seasonal commitment (congressional letter relaying agency statements)",
                 "source_ids": "V1-04;WF-04"})
    rows.append({"indicator": "USDA Forest Service: trail miles maintained", "value": -22.0, "unit": "% change, 2025 vs prior year",
                 "period": "2025", "scope": "USFS Trail Program Status Report as cited in a congressional letter",
                 "source_ids": "LM-034;FC-015"})
    write_csv("f08_entry_path_indicators.csv", ["indicator", "value", "unit", "period", "scope", "source_ids"], rows)
    register("F08", "f08_entry_path_indicators.csv",
             "The entry rungs are thinning now, for fiscal and policy reasons: no non-fire seasonal hiring at the Forest Service in 2025, conservation internship postings down 44% on one board, and fewer than 8 in 100 federal employees under 30.",
             "Indicator table (one row per indicator, each with its own unit, period and scope) with a small inline bar for the percentage rows only; do not plot rows on a common axis.",
             "National Parks Traveler (Nov 10 2025) on Conservation Job Board data; Partnership for Public Service (OPM data); Office of Rep. Neguse (Mar 23 2026) relaying USFS statements; Rep. Schrier et al. letter (Mar 23 2026) citing the USFS Trail Program Status Report. Each row has its own base. These are signals with fiscal and policy drivers; none is attributed to AI.")


# ---------------------------------------------------------------- F9 policy timeline
VERIFIED_IDS_EXTRA = {"WP05-001", "WP05-002", "WP05-003", "WP05-004", "CP-043", "IO-034", "IO-022", "IO-020", "IO-028", "DC-016"}
# Sources re-verified in the WP-15 pass (docs/methods/WP15_SIGNOFF.md; docs/methods/sources.csv LM-154 ... LM-161)
WP15_IDS = {"LM-154", "LM-155", "LM-156", "LM-157", "LM-158", "LM-159", "LM-160", "LM-161"}


def is_verified_source(s):
    return s[:3] in ("V1-", "V2-", "V3-", "V4-") or s in VERIFIED_IDS_EXTRA or s in WP15_IDS


def f9():
    ins = {d["id"]: d for d in read_jsonl(os.path.join(ROOT, "data", "v2", "instruments", "instruments.jsonl"))}
    hold_path = os.path.join(ROOT, "data", "v2", "governance", "tribal_hold.yaml")
    hold_text = open(hold_path, encoding="utf-8").read() if os.path.exists(hold_path) else ""
    domain = {
        "ceq-nepa": "Environmental review", "doi-nepa": "Environmental review", "usda-nepa": "Environmental review",
        "seven-county": "Environmental review", "speed-act": "Environmental review", "nepa-s112": "Environmental review",
        "ceq-permitting": "Permitting technology", "permitting-tech": "Permitting technology",
        "esa-harm": "Species and habitat", "wotus": "Water", "ghg-endangerment": "Air and climate",
        "ca-sb-253": "Disclosure and markets", "ca-sb-261": "Disclosure and markets", "eu-omnibus": "Disclosure and markets",
        "ceqa": "Environmental review (state)", "eo-12898": "Cumulative-burden analysis (federal basis)",
        "eo-14096": "Cumulative-burden analysis (federal basis)", "eo-14008": "Cumulative-burden analysis (federal basis)",
        "eo-14148": "Cumulative-burden analysis (federal basis)", "eo-14173": "Federal HR and selection",
        "nj-ej": "Cumulative-burden analysis (state basis)", "ny-ecl": "Cumulative-burden analysis (state basis)",
        "eo-14303": "Scientific integrity", "eo-14356": "Federal HR and selection", "opm-": "Federal HR and selection",
        "schedule-policy": "Federal HR and selection", "ofccp": "Federal HR and selection",
        "omb-m-": "AI governance", "co-sb": "AI governance", "dol-ai": "AI governance and literacy",
        "american-security-drone": "Field technology", "faa-part-108": "Field technology",
        "uswfs": "Wildland fire", "wildland-fire-quals": "Wildland fire", "fy2026-interior": "Appropriations",
        "americorps": "Entry pathways", "workforce-pell": "Workforce system", "aswa-2026": "Workforce system",
        "dol-tegl": "Workforce system", "baaja-s5653": "Environmental review", "co-ag-admt": "AI governance",
        "usfs-objection": "Environmental review",
    }
    def dom(iid):
        k = iid.replace("seed:ins/", "")
        for pre, lab in domain.items():
            if k.startswith(pre):
                return lab
        return None
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "v2", "events", "*.jsonl"))):
        for d in read_jsonl(f):
            if not ("2025-01-01" <= d["eventDate"] <= "2027-12-31"):
                continue
            i = ins.get(d["instrument"], {})
            if not no_tribal(d) or not no_tribal(i) or "tribal" in d["instrument"] or (d["instrument"] in hold_text and hold_text):
                continue
            srcs = d.get("sources") or []
            ok = bool(srcs) and (all(is_verified_source(x) for x in srcs) or any(x in WP15_IDS for x in srcs))
            if d.get("evidenceLabel") != "E" or not ok:
                continue
            lab = dom(d["instrument"])
            if lab is None:
                continue
            kind = "recorded event" if d["eventDate"] <= AS_OF else "scheduled (published date)"
            rows.append({"date": d["eventDate"], "kind": kind, "event_type": d["eventType"], "status_after": d["statusAfter"],
                         "domain": lab, "jurisdiction": i.get("jurisdiction", ""),
                         "label": d["prefLabel"]["en"], "instrument_id": d["instrument"], "source_ids": ";".join(d["sources"])})
    # Scheduled dates published in verified records (not yet DriverEvents); each checked against its record.
    sched = [
        ("2026-11-10", "California SB 253: first Scope 1-2 reports due", "Disclosure and markets", "US-CA", "V2-15;DISC-01", ("V2-15", "Nov 10, 2026")),
        ("2027-01-01", "Colorado SB 26-189 (automated decision tools: notice and disclosure) takes effect", "AI governance", "US-CO", "CP-043;AIGOV-02", ("CP-043", "effective Jan 1, 2027")),
        ("2027-01-01", "FedRAMP Consolidated Rules mandatory for all stakeholders", "AI governance", "US", "V2-10;CMP-02", ("V2-10", "Jan 1, 2027 mandatory")),
        ("2027-01", "USWFS-USFS aligned federal wildland fire qualification standards take effect (the alignment is between USWFS and USFS standards)", "Wildland fire", "US", "V3-13;WF-10", ("V3-13", "effective January 2027")),
        ("2026-10-26", "Colorado Attorney General: comments and hearing on interim draft SB 26-189 rules", "AI governance", "US-CO", "LM-155;AIGOV-03", ("AIGOV-03", "2026-10-26")),
        ("2027-02-01", "AmeriCorps litigation stay ends (settlement covers FY2026 only)", "Entry pathways", "US", "V1-05;WF-06", ("V1-05", "Feb 1, 2027")),
        ("2027-03-19", "EU CSRD transposition deadline after Omnibus I", "Disclosure and markets", "EU", "V2-15;DISC-02", ("V2-15", "Mar 19, 2027")),
        ("2027-04-26", "ADA Title II web accessibility compliance date for public entities of 50,000+ (WCAG 2.1 AA)", "Accessibility", "US", "V2-11;CMP-01", ("V2-11", "Apr 26, 2027")),
    ]
    for date, label, lab, jur, src, (cid, needle) in sched:
        check(cid, needle)
        rows.append({"date": date, "kind": "scheduled (published date)", "event_type": "scheduled", "status_after": "",
                     "domain": lab, "jurisdiction": jur, "label": label, "instrument_id": "", "source_ids": src})
    # Pending actions recorded only as watch signals (no event type exists for pre-publication actions).
    check("V2-14", "Jul 24, 2026")
    check("V2-17", "Jul 10, 2026")
    rows.append({"date": "2026-07-24", "kind": "pending (watch)", "event_type": "advanced to OIRA review", "status_after": "unpublished",
                 "domain": "Environmental review", "jurisdiction": "US", "label": "ACHP votes to advance a proposed rewrite of 36 CFR part 800 (Section 106); at OIRA, unpublished as of Oct 9 2026",
                 "instrument_id": "", "source_ids": "V2-14;NHPA-01"})
    rows.append({"date": "2026-07-10", "kind": "pending (watch)", "event_type": "final rule at OIRA review", "status_after": "unpublished",
                 "domain": "Field technology", "jurisdiction": "US", "label": "FAA Part 108 (BVLOS) final rule at OIRA review; unpublished as of Oct 21 2026 (trade-press status)",
                 "instrument_id": "", "source_ids": "V2-17;UAS-01"})
    rows.sort(key=lambda r: (r["date"], r["domain"], r["label"]))
    write_csv("f09_policy_instrument_timeline_2025_2027.csv",
              ["date", "kind", "event_type", "status_after", "domain", "jurisdiction", "label", "instrument_id", "source_ids"], rows)
    register("F09", "f09_policy_instrument_timeline_2025_2027.csv",
             "In 2025-26 policy instruments reshaped review, authorization, hiring and disclosure work faster than any technology did, and more dated changes are already scheduled for 2027.",
             "Horizontal timeline with one swimlane per domain; recorded events as filled markers, scheduled dates as hollow markers, pending actions as dashed markers; status labels in text, not colour alone; table beside the chart.",
             "EMST L5 instrument registry and driver events (data/v2/instruments, data/v2/events; agent-recorded, unreviewed) filtered to events whose dates rest on verified records (V1-V4 key facts and the corrections register); scheduled and pending items from the same verified records. Litigation outcomes after the dates shown were not checked. Held (Tribal-related) instruments excluded.")


# ---------------------------------------------------------------- F10 corridors
def f10():
    roles = [r for r in read_csv(os.path.join(ROOT, "docs", "decisions", "mvp_role_set.csv")) if r["corridor"].startswith("COR")]
    assert len(roles) == 13
    corridor_name = {
        "COR-1": "Corps and field entry -> technician -> monitoring and data -> geospatial",
        "COR-2": "Fire operations -> fuels and prescribed fire -> fire intelligence",
        "COR-3": "Restoration and land stewardship -> review, permitting and compliance -> programme management",
    }
    out = []
    seq = {}
    for r in roles:
        cv_path = os.path.join(ROOT, "docs", "build", "WP-08", "generated", "change_view", r["role_key"] + ".json")
        cv = json.load(open(cv_path, encoding="utf-8"))
        seq[r["corridor"]] = seq.get(r["corridor"], 0) + 1
        variants = [v for v in r["sector_actor_variants"].split("|") if "held" not in v]
        out.append({
            "corridor": r["corridor"], "corridor_name": corridor_name[r["corridor"]], "step": seq[r["corridor"]],
            "role_key": r["role_key"], "role_title": r["title"], "work_function": r["function"].replace("WF-", "").title(),
            "role_levels": r["levels"].replace("|", "; "), "lifecycle_state": r["lifecycle_state"],
            "sector_actor_variants_released": "; ".join(variants),
            "change_indicator_active": cv["changeIndicator"]["active"],
            "context_signals_attached_watch": len(cv["contextSignals"]),
            "v2_multi_rater_assessment": "pending",
        })
    assert all(x["change_indicator_active"] == 0 for x in out)
    write_csv("f10_p1_corridors_and_roles.csv",
              ["corridor", "corridor_name", "step", "role_key", "role_title", "work_function", "role_levels", "lifecycle_state",
               "sector_actor_variants_released", "change_indicator_active", "context_signals_attached_watch", "v2_multi_rater_assessment"], out)
    register("F10", "f10_p1_corridors_and_roles.csv",
             "EMST v2's first 13 role profiles form three corridors that cross all three crafts and end in state and federal role variants; no role yet has a change indicator that has passed EMST's evidence rule.",
             "Three horizontal swimlanes (one per corridor) of role boxes in step order, with levels as a band inside each box and 'emerging' roles outlined dashed; a footer row per box shows 'change indicator: none active' and the count of watch signals. No craft blends or change ratings are drawn: those are agent drafts awaiting multi-rater assessment.",
             "EMST mvp_role_set.csv (ADR-0006, CA decision) and WP-08 generated change views (docs/build/WP-08/generated/change_view/). Indicator status is computed by the ADR-0028 evidence rule (two independent signal families, two periods, named human review); every attached signal is at watch status. Tribal variants are held and not shown.",
             tier="describe", evidence="Structure: CA decision (ADR-0006). Indicator status: computed. No agent ratings shown.")


def main():
    f1(); f2(); f3(); f4(); f5_f6(); f7(); f8(); f9(); f10()
    INDEX.append({
        "figure_id": "NOT-BUILT-1", "file": "",
        "headline": "Two exposure profiles (analytical vs field occupations on capability and usage indices)",
        "suggested_chart_form": "Held: would be a paired dot plot of occupation percentiles on a capability index and a usage index.",
        "source_note": "Not built. Values derive from the Eloundou et al. replication labels and Microsoft 'Working with AI' results files, whose licence terms are not yet in the third-party licence register (ADR-0013 amendment; CR-LM-002). The finding appears in the report as attributed prose. Build once AS/CP record the terms.",
        "use_tier": "", "evidence_label": "", "as_of": AS_OF})
    INDEX.append({
        "figure_id": "NOT-BUILT-2", "file": "",
        "headline": "Craft blend by priority role",
        "suggested_chart_form": "Omitted.",
        "source_note": "Omitted by rule: every v2 craft rating is an agent draft (raterType llm, validationStatus draft) pending the IO craft-rating pilot and the alpha gate (ADR-0005, ADR-0024); v1 craft tags are prior evidence only. Charting either would display an LLM rating or a v1 value.",
        "use_tier": "", "evidence_label": "", "as_of": AS_OF})
    write_csv("figures_index.csv", ["figure_id", "file", "headline", "suggested_chart_form", "source_note", "use_tier", "evidence_label", "as_of"], INDEX)
    print(f"build_figures: wrote {len([i for i in INDEX if i['file']])} figure datasets and figures_index.csv to {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
