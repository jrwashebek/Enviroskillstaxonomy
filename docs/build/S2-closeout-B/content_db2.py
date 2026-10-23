"""DB (A6) cross-lane and module content for S2 close-out builder B (work-order rows 26-30):
CR-FC-002 #1 (DB-C19), #2 (DB-C13); CR-DB-001 #3 (v1 2.2.3 laboratory data review), #5 (module candidate DB-C56);
ADR-0030 §3.2 (SL-C07 inspection core moved into an envhealth enactment of SL-C03; SL-C07 refocused).
Content evidence label J (FC Phase 2 report §2.3; DB Phase 2 report; CR rulings).
"""
import s2b_lib as S

DB = ["DB"]
T, WS, RA, SEW, SIM, PR = ("task-book-observation", "work-sample", "record-audit", "seeded-error-work-sample",
                           "simulation-role-play", "portfolio-review")
HAZ = [{"credential": "seed:crd-hazwoper", "kind": "entry"}]


def rg(m="M", c="none", p="general", g="none", u="M"):
    return {"mentorshipDependence": m, "cycleDependence": c, "placeBoundness": p, "credentialGate": g, "currencyDecay": u}


def _add_levels(want):
    def fn(rec):
        for lv in rec["levels"]:
            for k in want.get(lv["level"], []):
                if k not in lv["indicators"]:
                    lv["indicators"].append(k)
    return fn


def _contrib(*cids):
    def fn(rec):
        have = {s["competency"] for s in rec["supports"]}
        for c in cids:
            if c not in have:
                rec["supports"].append({"competency": c, "strength": "contributing"})
    return fn


# ------------------------------------------------------------------ row 26: DB-C19 (CR-FC-002 #1)
def db_c19_field_content():
    row, spec = "26", {"id": "seed:DB-C19", "roles": DB}
    S.build_task({"id": "seed:DB-C19-T6", "wf": "WF-ASSESS", "field": "on-site-required", "formation": "yes",
                  "text": "Halt intrusive work when field-screening readings exceed the site health and safety plan's action level, upgrading protection and recording the reading before work resumes",
                  "regime": rg("H", "none", "site-specific", "external-certificate", "M"), "gates": HAZ, "subsectors": ["P04", "W05"],
                  "contrib": ["seed:v1-4.4.4-A"],
                  "note": "CR-FC-002 #1 (from merged FC-C05): adaptation in place (G-2) beside the logging and sampling tasks."},
                 spec, "waste", row)
    S.build_task({"id": "seed:DB-C19-T7", "wf": "WF-ASSESS", "field": "on-site-required", "formation": "yes",
                  "text": "Collect soil-gas samples to the sampling plan, checking probe seals and leak-test results before each sample is accepted",
                  "regime": rg("H", "none", "site-specific", "external-certificate", "M"), "gates": HAZ, "subsectors": ["P04", "W05"],
                  "contrib": ["seed:FC-C24"], "note": "CR-FC-002 #1 (from merged FC-C05)."},
                 spec, "waste", row)
    S.put(S.indicator("seed:DB-C19", "seed:ind-db-c19-l2-c", "L2",
                      "Halts intrusive work when screening readings exceed the plan's action level, upgrading protection before work resumes and recording each reading.",
                      "unaided", [T, SIM], "waste", DB, ["seed:DB-C19-T6"], att="ATT-CPX", safety=True), "waste", row)
    S.patch("seed:DB-C19", _add_levels({"L2": ["seed:ind-db-c19-l2-c"]}), "DB", row,
            "S2 (CR-FC-002 #1 ruling): field content of merged FC-C05 added by DB: stop-and-upgrade task DB-C19-T6, soil-gas task DB-C19-T7, L2 halt indicator; contributing links to v1-4.4.4-A and FC-C24 (module to core). FC review pending.")
    S.patch("seed:DB-C19-T2", _contrib("seed:v1-4.4.4-A", "seed:FC-C24"), "DB", row,
            "S2 (CR-FC-002 #1): contributing links to core v1-4.4.4-A and FC-C24 added.")


# ------------------------------------------------------------------ row 27: DB-C13 (CR-FC-002 #2)
def db_c13_field_content():
    row, spec = "27", {"id": "seed:DB-C13", "roles": DB}
    S.build_task({"id": "seed:DB-C13-T7", "wf": "WF-MONITOR", "field": "on-site-required", "formation": "partial",
                  "text": "Document changes in conditions around a monitoring station, such as new obstructions, construction or vandalism, that affect siting criteria",
                  "regime": rg("M", "seasonal", "site-specific", "none", "M"), "subsectors": ["P01"],
                  "note": "CR-FC-002 #2 (from merged FC-C17): station-condition task."},
                 spec, "air", row)
    S.build_task({"id": "seed:DB-C13-T8", "wf": "WF-MONITOR", "field": "on-site-required", "formation": "partial",
                  "modes": ["MODE-ENGAGE"], "rel": ["public"],
                  "text": "Visit community hosts of low-cost air sensors, checking placement and power and explaining what the sensor data can and cannot show",
                  "regime": rg("M", "none", "site-specific", "none", "M"), "subsectors": ["P01", "X03"],
                  "contrib": ["seed:FC-C21"], "note": "CR-FC-002 #2 (from merged FC-C17): community low-cost sensor task; names no product."},
                 spec, "air", row)
    S.patch("seed:DB-C13", lambda r: None, "DB", row,
            "S2 (CR-FC-002 #2 ruling): field tasks of merged FC-C17 added by DB: station-condition task DB-C13-T7 and community low-cost sensor task DB-C13-T8 (contributing to core FC-C21). FC review pending.")


# ------------------------------------------------------------------ row 28: v1 2.2.3 (CR-DB-001 #3)
def v1_2_2_3_lab_review():
    row, spec = "28", {"id": "seed:v1-2.2.3", "roles": DB}
    S.build_task({"id": "seed:db-v1-2.2.3-lab-review", "wf": "WF-MONITOR", "field": "remote", "formation": "yes",
                  "text": "Review laboratory data packages, qualifiers and holding times to decide whether results can support a compliance decision",
                  "regime": rg("M", "none", "general", "none", "M"),
                  "note": "CR-DB-001 #3: the data-user side of module candidate DB-C53 (laboratory, MOD-18), which recurs across modules."},
                 spec, "core", row)
    S.put(S.indicator("seed:v1-2.2.3", "seed:ind-v1-2.2.3-l2-c", "L2",
                      "Reviews a laboratory data package against holding times, qualifiers and quality-control results, accepting, qualifying or rejecting each result for use in a compliance decision.",
                      "unaided", [SEW, RA], "core", DB, ["seed:db-v1-2.2.3-lab-review"], att="ATT-KNO"), "core", row)
    S.patch("seed:v1-2.2.3", _add_levels({"L2": ["seed:ind-v1-2.2.3-l2-c"]}), "DB", row,
            "S2 (CR-DB-001 #3 ruling): laboratory data review task seed:db-v1-2.2.3-lab-review and L2 indicator added by DB (data-user side of DB-C53, MOD-18). DC review pending.")


# ------------------------------------------------------------------ row 29: DB-C56 (CR-DB-001 #5)
DB_C56 = {
    "id": "seed:DB-C56", "roles": DB, "row": "29", "area": "wildlife", "subsectors": ["L02"],
    "reusability": "subsector-specific", "useTier": "describe",
    "label": "Set harvest regulations and manage game populations from survey and harvest data",
    "alt": ["Wildlife population and harvest management", "Season and bag-limit setting", "Game management"],
    "definition": (
        "Managing hunted and trapped wildlife populations toward stated population and harvest objectives: designing and "
        "running population and harvest surveys, estimating abundance, recruitment and harvest rates with their "
        "uncertainty, recommending seasons, bag limits and quotas through the agency's regulation process, and "
        "evaluating each season against the objectives. Excludes fish populations and fisheries harvest (v1 1.4.5, "
        "DB-C49), protected-species consultation (FH-C01), population dynamics as a knowledge area (v1 1.4.1) and "
        "wildlife capture and handling (FC-C15)."),
    "statement": (
        "Designs and runs population and harvest surveys, estimates abundance, recruitment and harvest rates with their "
        "uncertainty, recommends seasons, bag limits and quotas that meet stated population and harvest objectives "
        "through the agency's regulation process, and evaluates each season's outcome against those objectives before "
        "the next cycle."),
    "adr": ["ADR-0030", "ADR-0018", "ADR-0003", "ADR-0004"],
    "note": (
        "S2 close-out B (A6 DB; CR-DB-001 #5 ruling, ADR-0030 §1.3). Module candidate for MOD-12 wildlife (wave 1): "
        "wildlife population and harvest management is the core work of state fish and wildlife agencies and had no "
        "module competency. Module growth, not core, so G-9 is unaffected; the disposition row is added by the CA at "
        "WP-16 (disposition_amendments.csv). Authored for R15 at P2 starter-kit depth (L1-L3, two indicators per level). "
        "Field-survey anchors (T1, T2, L1 indicators) await FC review. Draws on core v1 4.1.2 (wildlife detection) and "
        "knowledge area v1 1.4.1. Basis [J]."),
    "levels": {
        "L1": [
            {"id": "seed:ind-db-c56-l1-a", "mode": "unaided", "methods": [T, RA],
             "text": "Conducts a population survey route or plot to protocol, recording sex, age class and location for each animal so that the records pass the programme's data check.",
             "served": ["seed:DB-C56-T1"]},
            {"id": "seed:ind-db-c56-l1-b", "mode": "unaided", "methods": [T, SEW],
             "text": "Determines age and sex of harvested animals at a check station against the programme's reference criteria, matching an experienced checker's determinations within tolerance.",
             "served": ["seed:DB-C56-T2"]},
        ],
        "L2": [
            {"id": "seed:ind-db-c56-l2-a", "mode": "unaided", "methods": [WS, RA], "att": "ATT-AUT",
             "text": "Estimates abundance and harvest rate for a management unit from survey and harvest data, stating the confidence interval and the assumptions behind each estimate.",
             "served": ["seed:DB-C56-T3"]},
            {"id": "seed:ind-db-c56-l2-b", "mode": "unaided", "methods": [WS, PR], "att": "ATT-CPX",
             "text": "Drafts season and bag-limit options for a management unit that link each option to the unit's population and harvest objectives.",
             "served": ["seed:DB-C56-T4"]},
        ],
        "L3": [
            {"id": "seed:ind-db-c56-l3-a", "mode": "unaided", "methods": [WS, PR], "att": "ATT-SCO",
             "text": "Evaluates a season's outcome against population and harvest objectives across units, recommending regulation changes and recording where survey precision limits the conclusion.",
             "served": ["seed:DB-C56-T7"]},
            {"id": "seed:ind-db-c56-l3-b", "mode": "assisted", "methods": [SEW, RA], "att": "ATT-AUG",
             "text": "Checks a model-generated harvest projection against independent survey trends, rejecting or qualifying the projection before it supports a regulation proposal.",
             "served": ["seed:DB-C56-T5"]},
        ],
    },
    "tasks": [
        {"id": "seed:DB-C56-T1", "wf": "WF-ASSESS", "field": "on-site-required", "formation": "yes", "subsectors": ["L02"],
         "text": "Conduct population surveys on standardized routes or plots, recording observations to protocol for abundance and recruitment estimates",
         "regime": rg("H", "seasonal", "ecosystem-type", "none", "M"), "contrib": ["seed:v1-4.1.2"]},
        {"id": "seed:DB-C56-T2", "wf": "WF-MONITOR", "field": "on-site-required", "formation": "yes", "subsectors": ["L02"],
         "text": "Collect biological samples and harvest data at check stations, verifying age and sex determinations against reference criteria",
         "regime": rg("H", "seasonal", "ecosystem-type", "none", "M")},
        {"id": "seed:DB-C56-T3", "wf": "WF-ASSESS", "field": "remote", "formation": "yes", "subsectors": ["L02"],
         "text": "Estimate abundance, recruitment and harvest rates for a management unit, stating confidence intervals and model assumptions",
         "regime": rg("M", "seasonal", "ecosystem-type", "none", "M"), "contrib": ["seed:v1-2.2.2"]},
        {"id": "seed:DB-C56-T4", "wf": "WF-RULE", "field": "remote", "formation": "partial", "subsectors": ["L02"],
         "text": "Draft season, bag-limit and quota recommendations that link each option to the unit's population and harvest objectives",
         "regime": rg("M", "seasonal", "ecosystem-type", "none", "L")},
        {"id": "seed:DB-C56-T5", "wf": "WF-MONITOR", "field": "remote", "formation": "yes", "subsectors": ["L02"],
         "text": "Review a model-generated harvest projection against independent survey trends before it supports a regulation proposal",
         "regime": rg("M", "seasonal", "ecosystem-type", "none", "M"),
         "note": "G-2 split: checking a generated projection alongside the estimation task DB-C56-T3."},
        {"id": "seed:DB-C56-T6", "wf": "WF-RULE", "field": "on-site-preferred", "formation": "partial", "subsectors": ["L02"],
         "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Present proposed harvest regulations at public hearings or commission meetings, explaining their biological basis and uncertainty",
         "regime": rg("M", "seasonal", "general", "none", "L"), "contrib": ["seed:v1-5.1.1"]},
        {"id": "seed:DB-C56-T7", "wf": "WF-LEARN", "field": "remote", "formation": "partial", "subsectors": ["L02"],
         "text": "Evaluate each season's harvest outcome against population objectives, recommending regulation changes for the next cycle",
         "regime": rg("M", "multi-year-or-rare-event", "ecosystem-type", "none", "L")},
    ],
}

# ------------------------------------------------------------------ row 30: SL-C07 refocus + SL-C03 envhealth enactment
MOVED_TASKS = ["seed:SL-C07-T1", "seed:SL-C07-T4", "seed:SL-C07-T5", "seed:SL-C07-T6"]
MOVED_INDS = ["seed:ind-sl-c07-l1-a", "seed:ind-sl-c07-l1-b", "seed:ind-sl-c07-l2-a", "seed:ind-sl-c07-l2-b",
              "seed:ind-sl-c07-l3-b", "seed:ind-sl-c07-l4-a", "seed:ind-sl-c07-l4-b"]

SL_C07 = {
    "id": "seed:SL-C07", "roles": DB, "row": "30", "area": "envhealth", "subsectors": ["H01"],
    "reusability": "subsector-specific", "useTier": "describe",
    "label": "Review plans and evaluate sites for environmental health permits",
    "alt": ["Environmental health plan review", "Onsite wastewater site evaluation", "Food establishment plan review",
            "Sanitarian plan review"],
    "definition": (
        "Deciding before construction or operation whether a proposed food establishment, onsite wastewater system, "
        "private well, public pool or similar facility can meet health codes: checking submissions, reviewing plans and "
        "design calculations, evaluating soils and separation distances in the field, setting approval conditions and "
        "deciding variances, practised by local and state environmental health programmes. Excludes routine and "
        "complaint inspections of operating facilities, which are the envhealth enactment of core SL-C03, outbreak "
        "investigation (LC-C-07) and laboratory analysis."),
    "statement": (
        "Checks permit submissions for completeness, reviews facility plans and design calculations against health codes, "
        "evaluates soils, separation distances and site conditions in the field, sets approval conditions that a "
        "pre-opening or final inspection can verify, and decides variances with the equivalent protection required, "
        "before construction or operating permits are issued."),
    "adr": ["ADR-0030", "ADR-0018", "ADR-0003", "ADR-0004"],
    "note": (
        "S2 close-out B (A6 DB; ADR-0030 §3.2 duplicate scan). Refocused on plan review and site evaluation for "
        "environmental health permits: its inspection core repeated core SL-C03, so the routine and complaint inspection "
        "tasks (T1, T4, T5, T6) and their indicators now belong to the envhealth enactment of SL-C03 "
        "(seed:ena-sl-c03-envhealth), with health-code indicator variants and imminent-hazard closure. Survivor for EH "
        "plan reviews; absorbs DB-C27. REHS/RS registration is a Credential, not a level (T-8). Module record, so the core "
        "count does not change. R26 role profile still targets SL-C07; WP-08 to add the SL-C03 target. Basis [J]."),
    "levels": {
        "L1": [
            {"id": "seed:ind-sl-c07-l1-c", "mode": "unaided", "methods": [T, RA],
             "text": "Describes a soil profile in a test pit for an onsite wastewater evaluation under a reviewer's direction, recording horizons, texture and saturation indicators that the reviewer confirms.",
             "served": ["seed:SL-C07-T7"]},
            {"id": "seed:ind-sl-c07-l1-d", "mode": "unaided", "methods": [WS, SEW],
             "text": "Checks a permit submission against the programme's submission checklist, returning each incomplete plan with a list of the missing documents and schedules.",
             "served": ["seed:SL-C07-T3", "seed:SL-C07-T8"]},
        ],
        "L2": [
            {"id": "seed:ind-sl-c07-l2-c", "mode": "unaided", "methods": [WS, RA], "att": "ATT-AUT",
             "text": "Reviews a routine food establishment plan independently against code provisions for equipment, finishes and plumbing, issuing conditions that a pre-opening inspection can verify.",
             "served": ["seed:SL-C07-T3"]},
            {"id": "seed:ind-sl-c07-l2-d", "mode": "unaided", "methods": [T, WS], "att": "ATT-AUT",
             "text": "Evaluates a routine onsite wastewater site independently, sizing the system from soil and flow data so that the permit passes supervisory review.",
             "served": ["seed:SL-C07-T2", "seed:SL-C07-T7"]},
        ],
        "L3": [
            {"id": "seed:ind-sl-c07-l3-a", "keep": True},
            {"id": "seed:ind-sl-c07-l3-c", "mode": "assisted", "methods": [SEW, RA], "att": "ATT-AUG",
             "text": "Checks an automated plan-review or system-sizing output against code provisions and site data, correcting each error before permit conditions are issued.",
             "served": ["seed:SL-C07-T9"]},
        ],
        "L4": [
            {"id": "seed:ind-sl-c07-l4-c", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Sets the programme's plan-review and site-evaluation standards, writing the submission requirements, review checklist and variance criteria that applicants and reviewers use.",
             "served": ["seed:SL-C07-T11"]},
            {"id": "seed:ind-sl-c07-l4-d", "mode": "unaided", "methods": [WS, RA], "att": "ATT-CPX",
             "text": "Decides a variance request for a site or plan that cannot meet code, documenting the equivalent protection required and the evidence relied on.",
             "served": ["seed:SL-C07-T10"]},
        ],
    },
    "tasks": [
        {"id": "seed:SL-C07-T7", "wf": "WF-AUTHORIZE", "field": "on-site-required", "formation": "yes", "subsectors": ["H01"],
         "text": "Describe soil profiles in test pits or borings for an onsite wastewater site evaluation, recording horizons, texture and seasonal saturation indicators",
         "regime": rg("H", "seasonal", "ecosystem-type", "none", "M"), "contrib": ["seed:v1-4.1.4"]},
        {"id": "seed:SL-C07-T8", "wf": "WF-AUTHORIZE", "field": "remote", "formation": "partial", "subsectors": ["H01"],
         "text": "Review public pool or spa construction plans against health-code requirements for circulation, disinfection and safety features before approval",
         "regime": rg("M", "none", "general", "none", "M")},
        {"id": "seed:SL-C07-T9", "wf": "WF-AUTHORIZE", "field": "remote", "formation": "yes", "subsectors": ["H01"],
         "text": "Check an automated plan-review or system-sizing output against code provisions and site data before issuing permit conditions",
         "regime": rg("M", "none", "general", "none", "M"),
         "note": "G-2 split: checking automated review output alongside the plan-review tasks T2 and T3."},
        {"id": "seed:SL-C07-T10", "wf": "WF-AUTHORIZE", "field": "remote-capable", "formation": "partial", "subsectors": ["H01"],
         "text": "Decide variance requests for sites or plans that cannot meet code, documenting the equivalent protection required",
         "regime": rg("M", "multi-year-or-rare-event", "general", "none", "L")},
        {"id": "seed:SL-C07-T11", "wf": "WF-MANAGE", "field": "remote", "formation": "no", "subsectors": ["H01"],
         "text": "Set submission requirements and review checklists for environmental health plan review and site evaluation",
         "regime": rg("L", "none", "general", "none", "L")},
    ],
}

ENA_ENVHEALTH_NOTE = (
    "Local and state environmental health programmes inspect food establishments, public pools and spas, housing, "
    "institutions and similar premises against health and sanitary codes: findings are ranked by public-health risk "
    "factor, operators are educated on site, and the inspector may order immediate correction or closure when an "
    "imminent health hazard exists, setting the conditions for reopening. Inspector standardization against a trainer "
    "and risk-based inspection frequencies are programme features. Plan review and site evaluation before permitting "
    "stay in SL-C07.")


def sl_c07_refocus():
    row = "30"
    # 1. envhealth enactment of core SL-C03 (DB lane: module enactment)
    rec = S.enactment("seed:ena-sl-c03-envhealth", "seed:SL-C03", "envhealth",
                      "Environmental public health enactment of regulatory compliance inspection", ENA_ENVHEALTH_NOTE, DB,
                      ["H01"], position="regulator", tasks=MOVED_TASKS, variants=MOVED_INDS,
                      editorial="S2 (ADR-0030 §3.2): inspection core moved here from module SL-C07; indicator variants are health-code anchors (generic SL-C03 CLO unchanged; CR-LC-001 #4).")
    S.put(rec, "envhealth", row)

    # 2. moved tasks: support core SL-C03 (module -> core, permitted)
    def to_sl_c03(r):
        r["supports"] = [{"competency": "seed:SL-C03", "strength": "primary"}]
    for tid in MOVED_TASKS:
        S.patch(tid, to_sl_c03, "DB", row,
                "S2 (ADR-0030 §3.2): re-pointed from SL-C07 to core SL-C03; listed in seed:ena-sl-c03-envhealth.additionalTasks. Text unchanged, so craft ratings stay current.")

    # 3. moved indicators: competency SL-C03, enactment variants (never in SL-C03.levels)
    def to_variant(r):
        r["competency"] = "seed:SL-C03"
    for iid in MOVED_INDS:
        S.patch(iid, to_variant, "DB", row,
                "S2 (ADR-0030 §3.2): health-code indicator variant of the envhealth enactment of SL-C03 (seed:ena-sl-c03-envhealth); moved from SL-C07.")

    # 4. refocused SL-C07 (own lane; WP-06 record edited in place)
    p, old = S.load("seed:SL-C07")
    area = "envhealth"
    for lvl, inds in SL_C07["levels"].items():
        for i in inds:
            if i.get("keep"):
                continue
            S.put(S.indicator("seed:SL-C07", i["id"], lvl, i["text"], i["mode"], i["methods"], area, DB, i.get("served"),
                              att=i.get("att")), area, row)
    for t in SL_C07["tasks"]:
        S.build_task(t, SL_C07, area, row)

    def refocus(r):
        r["prefLabel"] = {"en": SL_C07["label"]}
        r["altLabel"] = {"en": SL_C07["alt"]}
        r["definition"] = {"en": SL_C07["definition"]}
        r["statement"] = {"en": SL_C07["statement"]}
        r["levels"] = [{"level": k, "indicators": [i["id"] for i in v]} for k, v in sorted(SL_C07["levels"].items())]
        pv = r["provenance"]
        pv["promptVersion"] = pv.get("promptVersion", "") if "s2b" in pv.get("promptVersion", "") else pv.get("promptVersion", "") + " + s2b-db@1"
    S.patch("seed:SL-C07", refocus, "DB", row, SL_C07["note"])


SPECS = [DB_C56]
PATCHES = [db_c19_field_content, db_c13_field_content, v1_2_2_3_lab_review, sl_c07_refocus]
