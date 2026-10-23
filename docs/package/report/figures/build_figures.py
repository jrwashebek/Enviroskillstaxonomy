#!/usr/bin/env python3
"""Build the chart datasets for the flagship report "How environmental jobs are changing".

WP-14 (A10: AS with CP), EMST v2, 2026-10-23; review-fix pass (Fix-A) 2026-10-23.
Licence of this script: Apache-2.0. The CSV outputs are CC BY 4.0 as part of the report;
third-party values keep their own terms and are credited in each row
(docs/governance/LICENSING.md section 5).

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
  * Key hard-coded values are checked against the text of the verification record they
    come from (a needle check: the build fails if the string no longer appears). It does
    not check every cell.
  * No figure cites a superseded verification record. check() fails on status
    'superseded', and every source_ids cell written to a figure passes through cite(),
    which fails on a superseded ID unless SUPERSEDED_SUCCESSORS names the current
    claims-register row that replaces it (and that row is itself checked).
  * F05 and F06 use plan-level bootstrap intervals (seeded) and sensitivity checks computed
    from openlmp_plan_level_extract.csv (written by extract_openlmp_plans.py); the build
    fails unless that extract reproduces the plan-equal means stored in the L5 signals.
  * Deterministic: same inputs, same outputs.
"""
import csv
import glob
import json
import os
import random
import statistics
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
            if "source_ids" in r:
                r = dict(r, source_ids=cite(r["source_ids"], name))
            w.writerow([r.get(h, "") for h in header])
    return path


KEY_FACTS = {r["fact_id"]: r for r in read_csv(os.path.join(VER, "ALL_key_facts.csv"))}
QUEUE = {}
for r in read_csv(os.path.join(VER, "ALL_queue_results.csv")):
    QUEUE.setdefault(r["item_id"], r)
CLAIMS = {r["claim_id"]: r for r in read_csv(os.path.join(ROOT, "docs", "methods", "claims_register.csv"))}
USABLE = ("verified", "corrected", "verified-partial", "derived")

# A superseded verification record may not be cited. Where a figure's input data still carry
# one (data/v2 provenance, outside this script's control), it is replaced by the current
# claims-register row named here, and the build checks that row is usable and still says
# what the figure needs (needle). Any other superseded ID fails the build.
SUPERSEDED_SUCCESSORS = {
    "CP-043": ("AIGOV-02", "SB 26-189"),   # Colorado SB 24-205 entry superseded by SB 26-189
    "IO-034": ("AIGOV-02", "SB 26-189"),
    "V4-07": ("BLS-01", "2025-35"),       # 2024-34 cycle claim superseded by the 2025-35 release
}


def record(source_id):
    """Return (text, status) for a verification record, or (None, None) if the ID is not one."""
    if source_id in KEY_FACTS:
        return (KEY_FACTS[source_id]["correct_statement"] + " " + KEY_FACTS[source_id]["note"],
                KEY_FACTS[source_id]["verification_status"])
    if source_id in QUEUE:
        return QUEUE[source_id]["finding"], QUEUE[source_id]["verification_status"]
    if source_id in CLAIMS:
        return CLAIMS[source_id]["claim"], CLAIMS[source_id]["status"]
    return None, None


def check(source_id, *needles):
    """Fail the build unless the record is usable (never superseded) and every needle appears in it."""
    text, status = record(source_id)
    if text is None:
        sys.exit(f"build_figures: unknown verification id {source_id}")
    if status not in USABLE:
        sys.exit(f"build_figures: {source_id} has status {status}; not usable")
    for n in needles:
        if n not in text:
            sys.exit(f"build_figures: '{n}' not found in verification record {source_id}; re-check the figure")
    return status


def cite(source_ids, where=""):
    """Apply the superseded rule to a ';'-separated source_ids cell (see SUPERSEDED_SUCCESSORS)."""
    out = []
    for s in [x for x in source_ids.split(";") if x]:
        _, status = record(s)
        if status == "superseded":
            if s not in SUPERSEDED_SUCCESSORS:
                sys.exit(f"build_figures: {where} cites superseded record {s} with no successor; re-check the figure")
            succ, needle = SUPERSEDED_SUCCESSORS[s]
            check(succ, needle)
            s = succ
        elif status is not None and status not in USABLE:
            sys.exit(f"build_figures: {where} cites {s} with status {status}; not usable")
        if s not in out:
            out.append(s)
    return ";".join(out)


def boot_ci(values, idx_sets):
    """Percentile bootstrap 95% interval of the mean, over pre-drawn resample index sets."""
    means = sorted(sum(values[i] for i in s) / len(s) for s in idx_sets)
    b = len(means)
    return means[int(0.025 * b)], means[int(0.975 * b) - 1]


def resamples(n, rng, b=10000):
    return [[int(rng.random() * n) for _ in range(n)] for _ in range(b)]


def no_tribal(rec):
    flags = (rec.get("careFlag"), rec.get("tribalPrograms"), rec.get("indigenousDataFlag"))
    if any(flags) or rec.get("approvalStatus") == "pending-tribal-review":
        return False
    return True


INDEX = []


E_DEFAULT = "E (external sources read; AI-agent checks recorded in the claims register; see source_ids per row)"
DERIV = "EMST derivation from an E source (counts and classification computed by EMST; not reviewed by a human)"


def register(fid, fname, headline, chart, source_note, tier="describe", evidence=E_DEFAULT):
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
        {"unit": "USDA Forest Service", "measure": "net change in employees", "value_pct": "", "value_pct_bound": -25.0,
         "value_kind": "bound only: a decline of more than 25% (source says 'more than a quarter'; no exact figure published); value_pct left blank so the row is not plotted as exact",
         "period_start": "2024-09", "period_end": "2026-01", "base": "on-board employees, PPS analysis of OPM data",
         "publisher": "Partnership for Public Service", "source_ids": "V1-02;WF-02"},
        {"unit": "National Park Service", "measure": "net change in employees", "value_pct": "", "value_pct_bound": -25.0,
         "value_kind": "bound only: a decline of more than 25% (source says 'more than a quarter'; no exact figure published); value_pct left blank so the row is not plotted as exact",
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
    hdr = ["unit", "measure", "value_pct", "value_pct_bound", "value_kind", "level_start", "level_end", "period_start", "period_end", "base", "publisher", "source_ids"]
    write_csv("f01_public_capacity_change.csv", hdr, rows)
    register("F01", "f01_public_capacity_change.csv",
             "Between Sep 2024 and Jan 2026 the federal civilian workforce fell 12%, and the two largest land-management agencies by staff each lost more than a quarter of their employees. The sources tie the decline to personnel and hiring actions (deferred resignations, hiring controls, grant terminations); AI's employment effect has not been measured.",
             "Dot plot of percentage change by unit, one row per unit, each labeled with its own period and base; the two bound-only rows (value_pct blank, value_pct_bound -25) drawn as an open marker with an arrow, never as an exact point; no bars, no ranking across bases; table beside the chart.",
             "Partnership for Public Service (OPM data, to Jan 2026; excludes USPS, the Foreign Service and much of the intelligence community); Inside Climate News (OPM data, Mar 6 2026); Agri-Pulse (OPM data, Jan 21 2026). Bases differ by row and must not be compared as one series; USDA OIG data reported in the press give a different USFS figure (16% in 2025) on another base. 'Largest' is by staff (BLM manages the most land). Federal figures only: they exclude Tribal, state, local, NGO and private workforces.",
             evidence="E for the values; J for the attribution sentence in the headline (sources: Inside Climate News on deferred resignations; EO 14356 on hiring controls; AmeriCorps litigation sources on grant terminations)")


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
    typed = tot["total"] - sum(grid[("Not classified", s)] for s in stages)
    cml = sum(grid[("Classical ML", s)] for s in stages)
    check("RPT-27", f"{cml} classical machine learning", f"{typed} report an AI type")
    epa_offices = {"OFA", "OAR", "OECA", "AO", "OCSPP", "OW"}
    units = {}
    for r in rows:
        b = r["agency_bureau"]
        u = "EPA" if (r["agency"] == "EPA" or b in epa_offices or b.startswith("Region ")) else b
        units[u] = units.get(u, 0) + 1
    assert len(units) == 11 and sum(units.values()) == 504, units
    check("OMB-02", "eleven environmental units", "USGS 187", "NOAA 157")
    unit_list = ", ".join(f"{u} {n}" for u, n in sorted(units.items(), key=lambda x: (-x[1], x[0])))
    hdr = ["ai_type"] + stages + ["total"]
    write_csv("f02_federal_env_ai_use_cases_type_by_stage.csv", hdr, out)
    register("F02", "f02_federal_env_ai_use_cases_type_by_stage.csv",
             f"Classical machine learning for science work is the largest type of registered AI in eleven federal environmental units ({cml} of the {typed} use cases that report a type; {tot['total'] - typed} report none), and most use cases are not yet deployed: 61 of the 347 that report a stage are in production.",
             "Stacked horizontal bars by AI type (segments = development stage, Deployed first), with the 'not classified' row and the 'stage not reported' segment shown hatched and labeled; table beside the chart.",
             f"OMB 2025 Federal Agency AI Use Case Inventory (README as of Apr 13 2026). Eleven environmental units, nine bureaus and two USDA mission areas, as extracted by EMST's labor-market analysis (docs/research/labor-market-ai-impact/scripts/omb_inventory_env.py): {unit_list} (EPA offices and regions pooled). 'Deployed' = development_stage 'Deployed' only; OMB's README pools deployed and piloted. NOAA's 157 records report neither a type nor a stage. Self-reported by agencies; registration is not use.",
             evidence=DERIV)


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
    check("RPT-28", "species and wildlife detection 89 (11 deployed)", "NEPA, environmental review and permitting 5 (0)")
    register("F03", "f03_federal_env_ai_use_cases_by_function.csv",
             "Species detection, remote sensing, water and fire lead federal environmental AI; none of the five use cases in NEPA, environmental review or permitting is deployed. NOAA's 157 records report no stage and are counted as not deployed or unreported.",
             "Horizontal bars of use cases per function family with the deployed share as a darker inner bar; families overlap (keyword-classified), so no totals row; table beside the chart.",
             "OMB 2025 Federal Agency AI Use Case Inventory, eleven environmental units (see F02); EMST keyword classification of use-case names and descriptions (a use case can fall in more than one family; the NEPA family's pattern includes the broad term 'permit'). 'Deployed' = development_stage 'Deployed' only; 'not_deployed_or_unreported' includes NOAA's 157 records, which report no stage.",
             evidence=DERIV)


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
                    "license_or_user_band": r["Estimated # of Licenses/Users"]})
    out.sort(key=lambda x: (x["department"], x["commercial_ai_use_case_category"]))
    assert {x["department"] for x in out} == {"USDA", "DOI", "EPA"}
    write_csv("f04_commercial_genai_drafting_tools_at_scale.csv",
              ["department", "commercial_ai_use_case_category", "license_or_user_band"], out)
    check("RPT-03", "knowledge-retrieval chat assistant at 50,000+", "writing tool at 50,000+")
    register("F04", "f04_commercial_genai_drafting_tools_at_scale.csv",
             "Commercial AI tools for drafting, summarizing, writing and search are licensed at 10,000 or more users in each of the three main federal environmental departments (at USDA the only such tool is a search and knowledge-retrieval assistant; at Interior, a writing tool): availability at workforce scale, which is not the same as use.",
             "Small table (department x use-case category) with the license band as the cell value; no chart needed. Product names are deliberately omitted.",
             "OMB 2025 consolidated COTS AI use cases (ombegov GitHub), rows for USDA, DOI and EPA marked in use with a band of 10,000+ licenses or users. Interior and USDA bands are department-wide, not limited to environmental staff. The keyword filter includes 'knowledge retrieval'; without it USDA would not appear, so do not describe the USDA row as a drafting or summarizing assistant. License bands are agency estimates; they measure availability, not frequency or quality of use.")


# ---------------------------------------------------------------- F5/F6 plan requirements
def f5_f6():
    recs = read_jsonl(os.path.join(SIG, "openlmp.jsonl"))
    check("PLAN-01", "30.7%", "2.7%", "22.2%", "1.8%", "17 of the 36", "24 of the 84")
    check("PLAN-02", "11.9 to 24.9", "4.7 to 5.0", "6.2 to 4.3")
    plans = read_csv(os.path.join(OUT, "openlmp_plan_level_extract.csv"))
    eras = {"1982-rule": [p for p in plans if p["rule"] == "1982-rule"], "2012-rule": [p for p in plans if p["rule"] == "2012-rule"]}
    def measure_col(name):  # signal measure name -> extract column
        if name.startswith("monitoring_component_share"):
            return "n_monitoring"
        kind, key = name.split(":")
        if kind.startswith("mentions_per_1000_components"):
            return "term_" + key
        if kind.startswith("coordination_touchpoints_per_1000"):
            return "touchpoint_" + key
        sys.exit(f"build_figures: unexpected OpenLMP measure {name}")

    def vals(ps, col):
        scale = 1.0 if col == "n_monitoring" else 1000.0
        return [scale * int(p[col]) / int(p["n_components"]) for p in ps]

    variants = [  # (variant id, label, filter)
        ("all", "all documents (headline; signal record values)", lambda p: True),
        ("no_monitoring_reports", "excluding monitoring evaluation reports", lambda p: p["doc_kind"] != "monitoring_report"),
        ("plans_only", "plan documents only (excluding monitoring reports and stand-alone monitoring plans)", lambda p: p["doc_kind"] == "plan"),
        ("with_monitoring", "excluding documents with no component typed as monitoring", lambda p: int(p["n_monitoring"]) > 0),
        ("plans_only_with_monitoring", "plan documents only, with at least one component typed as monitoring", lambda p: p["doc_kind"] == "plan" and int(p["n_monitoring"]) > 0),
    ]
    rng = random.Random(20261023)
    sub, idx = {}, {}
    for vid, _, keep in variants:
        for er, ps in eras.items():
            sub[(vid, er)] = [p for p in ps if keep(p)]
            idx[(vid, er)] = resamples(len(sub[(vid, er)]), rng)

    def stats(vid, er, col):
        v = vals(sub[(vid, er)], col)
        lo, hi = boot_ci(v, idx[(vid, er)])
        nd = 4 if col == "n_monitoring" else 2
        return round(statistics.fmean(v), nd), round(lo, nd), round(hi, nd), len(v)

    def overlap(a, b):
        return "yes" if max(a[1], b[1]) <= min(a[2], b[2]) else "no"

    f5rows, f6rows = [], []
    for d in recs:
        if not no_tribal(d):
            continue  # Tribal touchpoints are quarantined (careFlag); TN decides how they are shown
        m = d["measure"]
        name = m["name"]
        col = measure_col(name)
        sens = m.get("sensitivity", {})
        a82, a12 = stats("all", "1982-rule", col), stats("all", "2012-rule", col)
        # the extract must reproduce the stored plan-equal means and n (ties the extract to the signal record)
        nd = 4 if col == "n_monitoring" else 2
        assert (a82[0], a82[3]) == (round(m["baseline"]["value"], nd), m["baseline"]["n"]), (name, a82, m["baseline"])
        assert (a12[0], a12[3]) == (round(m["value"], nd), m["n"]), (name, a12, m["value"])
        label = name.split(":")[-1].replace("_", " ")
        if col == "n_monitoring":
            for vid, vlabel, _ in variants:
                s82, s12 = stats(vid, "1982-rule", col), stats(vid, "2012-rule", col)
                cw82 = sum(int(p["n_monitoring"]) for p in sub[(vid, "1982-rule")]) / sum(int(p["n_components"]) for p in sub[(vid, "1982-rule")])
                cw12 = sum(int(p["n_monitoring"]) for p in sub[(vid, "2012-rule")]) / sum(int(p["n_components"]) for p in sub[(vid, "2012-rule")])
                if vid == "all":
                    assert (round(cw82, 4), round(cw12, 4)) == (sens["baselineValue"], sens["value"])
                f5rows.append({"measure": "components typed as monitoring (share of document components)", "variant": vid, "documents_included": vlabel,
                               "unit": "share of document components",
                               "rule_1982_plan_equal": s82[0], "rule_1982_ci95_low": s82[1], "rule_1982_ci95_high": s82[2], "rule_1982_n_documents": s82[3],
                               "rule_2012_plan_equal": s12[0], "rule_2012_ci95_low": s12[1], "rule_2012_ci95_high": s12[2], "rule_2012_n_documents": s12[3],
                               "rule_1982_component_weighted": round(cw82, 4), "rule_2012_component_weighted": round(cw12, 4),
                               "plan_equal_cis_overlap": overlap(s82, s12), "ci_method": "percentile bootstrap over documents, 10,000 resamples, seed 20261023",
                               "signal_id": d["id"] if vid == "all" else ""})
        else:
            p82, p12 = stats("plans_only", "1982-rule", col), stats("plans_only", "2012-rule", col)
            f6rows.append({"measure": label, "unit": m["unit"],
                           "rule_1982_plan_equal": a82[0], "rule_1982_ci95_low": a82[1], "rule_1982_ci95_high": a82[2], "rule_1982_n_documents": a82[3],
                           "rule_2012_plan_equal": a12[0], "rule_2012_ci95_low": a12[1], "rule_2012_ci95_high": a12[2], "rule_2012_n_documents": a12[3],
                           "rule_1982_component_weighted": sens.get("baselineValue"), "rule_2012_component_weighted": sens.get("value"),
                           "plan_equal_cis_overlap": overlap(a82, a12),
                           "plans_only_1982": p82[0], "plans_only_1982_ci95_low": p82[1], "plans_only_1982_ci95_high": p82[2], "plans_only_1982_n": p82[3],
                           "plans_only_2012": p12[0], "plans_only_2012_ci95_low": p12[1], "plans_only_2012_ci95_high": p12[2], "plans_only_2012_n": p12[3],
                           "plans_only_cis_overlap": overlap(p82, p12),
                           "ci_method": "percentile bootstrap over documents, 10,000 resamples, seed 20261023", "signal_id": d["id"]})
    assert len(f5rows) == len(variants) and len(f6rows) == 9
    kinds = {k: sum(1 for p in eras["2012-rule"] if p["doc_kind"] == k) for k in ("monitoring_report", "monitoring_plan", "plan")}
    any82 = sum(1 for p in eras["1982-rule"] if int(p["n_monitoring"]) > 0)
    assert (kinds["monitoring_report"], kinds["monitoring_plan"], any82, len(eras["1982-rule"])) == (17, 5, 24, 84)
    po = [r for r in f5rows if r["variant"] == "plans_only"][0]
    hdr5 = ["measure", "variant", "documents_included", "unit", "rule_1982_plan_equal", "rule_1982_ci95_low", "rule_1982_ci95_high", "rule_1982_n_documents",
            "rule_2012_plan_equal", "rule_2012_ci95_low", "rule_2012_ci95_high", "rule_2012_n_documents",
            "rule_1982_component_weighted", "rule_2012_component_weighted", "plan_equal_cis_overlap", "ci_method", "signal_id"]
    write_csv("f05_plan_monitoring_share_by_rule.csv", hdr5, f5rows)
    f6rows.sort(key=lambda x: x["measure"])
    hdr6 = ["measure", "unit", "rule_1982_plan_equal", "rule_1982_ci95_low", "rule_1982_ci95_high", "rule_1982_n_documents",
            "rule_2012_plan_equal", "rule_2012_ci95_low", "rule_2012_ci95_high", "rule_2012_n_documents",
            "rule_1982_component_weighted", "rule_2012_component_weighted", "plan_equal_cis_overlap",
            "plans_only_1982", "plans_only_1982_ci95_low", "plans_only_1982_ci95_high", "plans_only_1982_n",
            "plans_only_2012", "plans_only_2012_ci95_low", "plans_only_2012_ci95_high", "plans_only_2012_n", "plans_only_cis_overlap",
            "ci_method", "signal_id"]
    write_csv("f06_plan_content_rates_by_rule.csv", hdr6, f6rows)
    note = ("OpenLMP 0.1.0 documents (catalog 2026-10-21, CC0), derived by EMST (docs/methods/scripts/wp10_lmp.py for the signal records; "
            "docs/package/report/figures/extract_openlmp_plans.py for the plan-level extract used here). Western national forests only: "
            "the comparison uses 120 USDA Forest Service documents (84 under the 1982 rule, 36 under the 2012 rule), and about 95% of all corpus components are Forest Service plans in western states. "
            "Cross-era comparison of different documents, not a time series. Each document is weighted equally (component-weighted values are a second check); "
            "95% intervals are percentile bootstrap intervals over documents (seeded), which replace the earlier normal approximation. "
            "Document type (plan, monitoring evaluation report, stand-alone monitoring plan) is classified by EMST from catalog titles. "
            "Components are as typed or extracted by OpenLMP, whose extraction method differs by era; mentions measure what documents name, not obligations or funded work. "
            "Tribal touchpoints are excluded pending Tribal Advisory Council review.")
    register("F05", "f05_plan_monitoring_share_by_rule.csv",
             f"In western national-forest documents, components typed as monitoring make up about 31% of each 2012-rule document against about 3% of each 1982-rule plan, but the gap mostly reflects document type: {kinds['monitoring_report']} of the 36 2012-rule documents are monitoring evaluation reports and {kinds['monitoring_plan']} are stand-alone monitoring plans. Among plan documents alone the shares are about {round(100 * po['rule_2012_plan_equal'])}% and {round(100 * po['rule_1982_plan_equal'])}%, with overlapping intervals; only {any82} of the 84 older plans have any component typed as monitoring, so the older baseline is probably partly an extraction artifact.",
             "Paired dot plot (1982 rule vs 2012 rule) with 95% bootstrap whiskers, one row per variant, headline row first and labeled as such; component-weighted values as hollow markers; rows whose intervals overlap labeled 'not distinguishable'; table beside the chart.",
             note, evidence="EMST derivation from OpenLMP (CC0); document-type classification and sensitivity checks by EMST; not reviewed by a human")
    register("F06", "f06_plan_content_rates_by_rule.csv",
             "In western national-forest documents, 2012-rule documents name climate change, data and models, and carbon far more often than 1982-rule plans, and the difference holds among plan documents alone. The apparent tripling of coordination is mostly a weighting artifact: partnership touchpoints rise, but distinguishably so only among plan documents.",
             "Small multiples, one panel per measure: 1982 vs 2012 plan-equal means with bootstrap whiskers for all documents and for plan documents only; component-weighted as hollow markers; panels where intervals overlap labeled 'not distinguishable'; table beside the chart.",
             note, evidence="EMST derivation from OpenLMP (CC0); document-type classification by EMST; not reviewed by a human")


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
        role = ("reference only (not an environmental occupation)" if soc == "15-2051" else
                "environmental occupation in EMST scope; broad occupation, mostly outside environmental work" if soc == "13-1041" else
                "environmental occupation in EMST scope")
        out.append({"soc_2018": soc, "occupation": occ, "soc_major_group": grp, "role_in_figure": role, "projected_change_2025_35_pct": v,
                    "all_occupations_pct": d["measure"]["baseline"]["value"],
                    "emst_band_relative_to_average": "faster" if v > 3.5 + 1 else ("slower or declining" if v < 3.5 - 1 else "about average"),
                    "source_ids": src})
    out.sort(key=lambda x: -x["projected_change_2025_35_pct"])
    write_csv("f07_bls_projections_2025_35.csv",
              ["soc_2018", "occupation", "soc_major_group", "role_in_figure", "projected_change_2025_35_pct", "all_occupations_pct", "emst_band_relative_to_average", "source_ids"], out)
    register("F07", "f07_bls_projections_2025_35.csv",
             "Official 2025-35 projections show analytical, engineering and technician occupations growing faster than the +3.5% all-occupation average, foresters slower, and forest and conservation workers and water operators declining.",
             "Dot plot of projected percentage change by occupation with a vertical reference line at +3.5%; EMST's 'about average' band of +/-1 point shaded and labeled as EMST's convention; data scientists shown with an axis break and labeled 'reference, not environmental'; table beside the chart.",
             "U.S. Bureau of Labor Statistics, Employment Projections 2025-35 (released Aug 27 2026), Table 1.2 and Occupational Outlook Handbook pages. Projections are context, not evidence of skill change; BLS does not attribute these occupation projections to AI. The faster / about average / slower bands (+/-1 point around +3.5%) are an EMST display convention, not BLS categories. Data scientists are a reference point, not an environmental occupation. Compliance officers (13-1041) is a broad occupation, mostly outside environmental work. Wildland firefighters are not counted separately.")


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
    check("WF-06", "July 2025", "coalition only")
    register("F08", "f08_entry_path_indicators.csv",
             "In federal land agencies and conservation corps the entry rungs thinned in 2025-26: no non-fire seasonal hiring at the Forest Service in 2025, conservation internship postings down 44% on one board, and fewer than 8 in 100 federal employees under 30.",
             "Indicator table (one row per indicator, each with its own unit, period and scope) with a small inline bar for the percentage rows only; do not plot rows on a common axis.",
             "National Parks Traveler (Nov 10 2025) on Conservation Job Board data; Partnership for Public Service (OPM data); Office of Rep. Neguse (press release Mar 23 2026 on a letter of Mar 18 2026) relaying USFS statements, including that the 2025 seasonal decision was due to budget constraints; Rep. Schrier et al. letter (Mar 23 2026) citing the USFS Trail Program Status Report. Each row has its own base. These signals followed personnel, hiring and grant decisions; none of these sources attributes them to AI. AmeriCorps context for the postings row: terminations were enjoined in the plaintiff states (Jun 2025), reinstatement eligibility was extended to grantees elsewhere (Jul 2025, uptake undocumented), and the Sep 2026 settlement covers FY2026 and the coalition jurisdictions only.")


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
        ("2027-01-01", "Colorado SB 26-189 (automated decision tools: notice and disclosure) takes effect", "AI governance", "US-CO", "AIGOV-02", ("AIGOV-02", "2027-01-01")),
        ("2027-01-01", "FedRAMP Consolidated Rules mandatory for all stakeholders", "AI governance", "US", "V2-10;CMP-02", ("V2-10", "Jan 1, 2027 mandatory")),
        ("2027-01", "USWFS-USFS aligned federal wildland fire qualification standards take effect (the alignment is between USWFS and USFS standards)", "Wildland fire", "US", "V3-13;WF-10", ("V3-13", "effective January 2027")),
        ("2026-10-26", "Colorado Attorney General: comments and hearing on interim draft SB 26-189 rules", "AI governance", "US-CO", "LM-155;AIGOV-03", ("AIGOV-03", "2026-10-26")),
        ("2027-02-01", "AmeriCorps litigation stay ends (the Sep 2026 settlement covers FY2026 and the coalition jurisdictions only)", "Entry pathways", "US", "V1-05;WF-06", ("V1-05", "Feb 1, 2027")),
        ("2027-03-19", "EU CSRD transposition deadline after Omnibus I", "Disclosure and markets", "EU", "V2-15;DISC-02", ("V2-15", "Mar 19, 2027")),
        ("2027-04-26", "ADA Title II web accessibility compliance date for public entities of 50,000+ (WCAG 2.1 AA)", "Accessibility", "US", "V2-11;CMP-01", ("V2-11", "Apr 26, 2027")),
    ]
    for date, label, lab, jur, src, (cid, needle) in sched:
        check(cid, needle)
        rows.append({"date": date, "kind": "scheduled (published date)", "event_type": "scheduled", "status_after": "",
                     "domain": lab, "jurisdiction": jur, "label": label, "instrument_id": "", "source_ids": src})
    # Recorded events published in corrected register rows but not yet DriverEvents in data/v2/events
    # (evidence review R15 and R33; data change requested in CR-FIX-A-003). Month precision as published.
    recorded = [
        ("2025-07", "notice", "reinstatement offered", "Entry pathways", "US",
         "AmeriCorps tells grantees whose grants were terminated on 25 Apr 2025, including programs in states outside the litigation, that they are eligible for reinstatement (uptake undocumented)",
         "WF-06", ("WF-06", "July 2025")),
        ("2026-07", "certification granted", "in effect pending appeal", "Cumulative-burden analysis (state basis)", "US-NJ",
         "New Jersey Supreme Court grants certification to review the NJDEP environmental justice rules; the rules remain in effect while the appeal is pending",
         "EJ-02", ("EJ-02", "certification in July 2026")),
    ]
    for date, etype, after, lab, jur, label, src, (cid, needle) in recorded:
        check(cid, needle)
        rows.append({"date": date, "kind": "recorded event", "event_type": etype, "status_after": after,
                     "domain": lab, "jurisdiction": jur, "label": label, "instrument_id": "", "source_ids": src})
    # Pending actions recorded only as watch signals (no event type exists for pre-publication actions).
    check("V2-14", "Jul 24, 2026")
    check("V2-17", "Jul 10, 2026")
    rows.append({"date": "2026-07-24", "kind": "pending (watch)", "event_type": "advanced to OIRA review", "status_after": "unpublished",
                 "domain": "Environmental review", "jurisdiction": "US", "label": "ACHP votes to advance a proposed rewrite of 36 CFR part 800 (Section 106); at OIRA, unpublished as of Oct 9 2026",
                 "instrument_id": "", "source_ids": "V2-14;NHPA-01"})
    check("UAS-01", "Pending Review")
    rows.append({"date": "2026-07-10", "kind": "pending (watch)", "event_type": "final rule at OIRA review", "status_after": "unpublished",
                 "domain": "Field technology", "jurisdiction": "US", "label": "FAA Part 108 (BVLOS) final rule at OIRA review; unpublished as of Oct 21 2026 (trade press); OIRA review record still pending on Oct 23 2026",
                 "instrument_id": "", "source_ids": "V2-17;UAS-01"})
    rows.sort(key=lambda r: (r["date"], r["domain"], r["label"]))
    write_csv("f09_policy_instrument_timeline_2025_2027.csv",
              ["date", "kind", "event_type", "status_after", "domain", "jurisdiction", "label", "instrument_id", "source_ids"], rows)
    changes = {"final", "effective", "enacted", "rescinded", "enjoined", "decided", "interim", "notice"}
    in_window = [r for r in rows if r["kind"] == "recorded event" and r["date"][:4] in ("2025", "2026")]
    n_change = sum(1 for r in in_window if r["event_type"] in changes)
    n_other = len(in_window) - n_change
    n_2027 = sum(1 for r in rows if r["kind"].startswith("scheduled") and r["date"][:4] == "2027")
    register("F09", "f09_policy_instrument_timeline_2025_2027.csv",
             f"EMST's registry records {n_change} dated policy actions in 2025-26 that changed or settled rules for review, authorization, hiring, disclosure or entry pathways (finalized, took effect, enacted, rescinded, enjoined, decided by a court, or a reinstatement offer), plus {n_other} other dated steps (proposals, bills, a court's grant of review); {n_2027} more dated changes are scheduled for 2027. The timeline holds no technology-adoption data, so it cannot by itself show that policy moved faster than technology.",
             "Horizontal timeline with one swimlane per domain; recorded events as filled markers, scheduled dates as hollow markers, pending actions as dashed markers; status labels in text, not color alone; table beside the chart.",
             "EMST L5 instrument registry and driver events (data/v2/instruments, data/v2/events; agent-recorded, unreviewed) filtered to events whose dates rest on verification records (V1-V4 key facts, the corrections register and the WP-15 re-checks of 2026-10-23). Filter rule: an event is admitted if all its sources are verification records, or if any source is a WP-15 re-check; some admitted events also cite a role source row that no verification pass re-checked (for example the objection-rule event cites SC-009). Two recorded events (AmeriCorps, July 2025; New Jersey Supreme Court, July 2026) come from corrected claims-register rows and are not yet in data/v2/events. Scheduled and pending items come from the same records; future dates are as of 2026-10-23 and must be re-checked. Superseded verification records are replaced by their current register rows (see SUPERSEDED_SUCCESSORS in the script). Bills are shown at their recorded stage only; none is law. Litigation outcomes after the dates shown were not checked. Held (Tribal-related) instruments excluded.",
             evidence="EMST record of external events (agent-recorded); dates checked against verification records and the claims register")


# ---------------------------------------------------------------- F10 corridors
def f10():
    roles = [r for r in read_csv(os.path.join(ROOT, "docs", "decisions", "mvp_role_set.csv")) if r["corridor"].startswith("COR")]
    assert len(roles) == 13
    corridor_name = {
        "COR-1": "Field and data corridor: corps and field entry -> technician -> monitoring and data -> geospatial",
        "COR-2": "Fire corridor: fire operations -> fuels and prescribed fire -> fire intelligence",
        "COR-3": "Stewardship and regulation corridor: restoration and land stewardship -> review, permitting and compliance -> program management",
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
             "EMST v2's first 13 role profiles form three corridors that are designed to cross all three crafts and end in state and federal role variants; no role yet has a change indicator that has passed EMST's evidence rule.",
             "Three horizontal swimlanes (one per corridor) of role boxes in step order, with levels as a band inside each box and 'emerging' roles outlined dashed; a footer row per box shows 'change indicator: none active' and the count of watch signals. No craft blends or change ratings are drawn: those are agent drafts awaiting multi-rater assessment.",
             "EMST mvp_role_set.csv (ADR-0006, a decision record drafted by EMST's AI agents) and the generated role change views (docs/build/WP-08/generated/change_view/). 'Designed to cross all three crafts' describes the corridor design; the craft ratings that would show it are agent drafts and are deliberately not charted. Indicator status is computed by the ADR-0028 evidence rule (two independent signal families, two periods, named human review); every attached signal is at watch status. Tribal variants are held and not shown.",
             tier="describe", evidence="Structure: EMST decision record (ADR-0006). Indicator status: computed. No agent ratings shown.")


def main():
    f1(); f2(); f3(); f4(); f5_f6(); f7(); f8(); f9(); f10()
    INDEX.append({
        "figure_id": "NOT-BUILT-1", "file": "",
        "headline": "Exposure gradient (capability and usage indices)",
        "suggested_chart_form": "Held: would be a paired dot plot of occupation percentiles on a capability index and a usage index.",
        "source_note": "Not built. Values derive from the Eloundou et al. replication labels and Microsoft 'Working with AI' results files, whose license terms are not yet in the third-party license register (ADR-0013 amendment; CR-LM-002). The finding appears in the report as attributed prose. Build once EMST records the terms; BLS's public-domain AI exposure categories are a license-free alternative once ingested.",
        "use_tier": "", "evidence_label": "", "as_of": AS_OF})
    INDEX.append({
        "figure_id": "NOT-BUILT-2", "file": "",
        "headline": "Craft blend by priority role",
        "suggested_chart_form": "Omitted.",
        "source_note": "Omitted by rule: every v2 craft rating is an agent draft (raterType llm, validationStatus draft) pending the craft-rating pilot and the agreement gate (ADR-0005, ADR-0024); v1 craft tags are prior evidence only. Charting either would display an LLM rating or a v1 value.",
        "use_tier": "", "evidence_label": "", "as_of": AS_OF})
    write_csv("figures_index.csv", ["figure_id", "file", "headline", "suggested_chart_form", "source_note", "use_tier", "evidence_label", "as_of"], INDEX)
    print(f"build_figures: wrote {len([i for i in INDEX if i['file']])} figure datasets and figures_index.csv to {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
