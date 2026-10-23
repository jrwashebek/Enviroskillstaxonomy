"""WP-07 exploratory learning pathways for the three P1 corridors (ADR-0026 §4; ADR-0023 §5; LC pathway template).

Every pathway is EXPLORATORY: `recommended: false` until CM's M-03 validation gate passes (ADR-0023). Pathways are
role-profile deltas (R1: teach only the gap); each step names the CLOs (competency x level; the builder resolves them to
the indicator IDs that exist), the tasks the learner performs and the target-role level the step belongs to.
Formation provisions implement ADR-0026 R6-R7 (provisional): human-essential formation tasks -> observed work-based
learning; augmented formation tasks -> supervised repetitions plus a validation drill; compressive, supervised or
substituted formation tasks -> a by-hand quota of unaided products before review-and-certify credit. Quota sizes are
LC judgment [J], to be calibrated in the pilot (time-to-proficiency, 90-day unaided transfer).

Role references use the P1 role keys of docs/decisions/mvp_role_set.csv as seed keys (`seed:<role_key>`); WP-08 builds
those RoleProfile records later (CR-LC-001 asks WP-08 to adopt the keys).

`v1prior` strings in provisions are v1 single-analyst Task 13 codes (automation type / tacit density / ladder position),
used only as design prompts, never as v2 findings (ADR-0011 rule 4; ADR-0027 §2).
"""

OBS, REP, DRILL, QUOTA = "observed-wbl", "supervised-repetitions+validation-drill", "validation-drill", "by-hand-quota"

R01 = "seed:R01-conservation-corps-member"
R02 = "seed:R02-field-resource-technician"
R03 = "seed:R03-monitoring-data-technician"
R04 = "seed:R04-geospatial-remote-sensing-analyst"
R05 = "seed:R05-ground-truth-validation-steward"
R06 = "seed:R06-wildland-fire-operations"
R07 = "seed:R07-fuels-prescribed-fire-specialist"
R08 = "seed:R08-fire-intelligence-analyst"
R09 = "seed:R09-restoration-project-lead"
R10 = "seed:R10-environmental-review-specialist"
R11 = "seed:R11-environmental-permit-writer"
R12 = "seed:R12-environmental-compliance-inspector"
R13 = "seed:R13-resource-program-manager"

TXA_NOTE = "TX-A floor: every role profile carries L1 on data interpretation, responsible AI use and AI-output validation (ADR-0025)."
SUPERVISOR = ("Supervisor formation plan required: the learner's supervisor works to seed:v1-7.2.2 at L2 or above and a named "
              "mentor or evaluator to seed:IO-C01 at L3 (ADR-0026 R7). Training use only; never a selection instrument (IO).")


def step(n, level, clos, tasks, note, provisions=()):
    return {"step": n, "roleLevel": level, "clos": clos, "tasks": tasks, "note": note, "provisions": list(provisions)}


def prov(task, response, quota, release, v1prior=""):
    return {"task": task, "response": response, "quota": quota, "release": release, "v1prior": v1prior}


PATHWAYS = []

# ------------------------------------------------------------------------------------------------ COR-1 field -> data
PATHWAYS.append(dict(
    id="seed:lc-pw-cor1-corps-to-field-technician", corridor="COR-1", type="new-hire", src=R01, dst=R02,
    prefLabel="Exploratory pathway: conservation corps member to field resource technician (entry)",
    definition=("Moves a conservation corps member or alumnus into an entry field resource technician role by building field "
                "safety, protocol data collection, identification and the data and AI floor through supervised field work. "
                "Exploratory: not validated against observed moves (ADR-0023)."),
    modes=["WBL", "FD", "MEN", "CL", "OL", "AIP"],
    hours=240, months=12,
    cost=("[J] Mostly paid placement and mentor time (about 40-80 mentor hours per trainee per season); corps supply is fragile "
          "because the AmeriCorps settlement covers FY2026 only [E: V1-05]."),
    rpl=["seed:crd-wilderness-first-aid", "seed:crd-wildland-fire-position-qualification"],
    alt=["None proposed: this pathway is itself the formation route for field craft; simulation is used only for rare events such as a medical evacuation [J]."],
    steps=[
        step(1, "entry", [("seed:v1-4.4.1-B", "L1"), ("seed:v1-4.4.1-A", "L1"), ("seed:v1-4.4.2", "L1"), ("seed:FC-C18", "L1")],
             ["seed:lc-txc-exercise-stop-work", "seed:lc-txc-report-near-miss", "seed:fc-risk-stopwork", "seed:v1-4.4.2-T1", "seed:v1-4.4.3-T2"],
             "Safety, first aid and navigation before any data work; observed in the field (R5).",
             [prov("seed:v1-4.4.3-T2", OBS, "3 off-trail navigations by map and compass, observed", "evaluator sign-off on an evaluation course", "A/Med/P"),
              prov("seed:v1-4.4.2-T1", OBS, "2 scenario patient assessments, observed", "instructor sign-off", "H/Hi/P")]),
        step(2, "entry", [("seed:FC-C23", "L1"), ("seed:v1-4.1.1", "L1"), ("seed:v1-1.4.3", "L1"), ("seed:FC-C24", "L1")],
             ["seed:v1-4.1.5-T1", "seed:v1-4.1.1-T1", "seed:v1-1.4.3-T1", "seed:fc-coc-complete"],
             "Protocol data collection and identification under a crew lead; no identification aid is credited yet.",
             [prov("seed:v1-1.4.3-T1", REP, "50 unaided identifications checked by an experienced observer", "error rate within the programme's practical-test threshold", "A/Hi/P"),
              prov("seed:v1-4.1.1-T1", REP, "10 plots established and recorded under supervision", "calibration-plot cover within tolerance", "A/Hi/P")]),
        step(3, "entry", [("seed:v1-4.1.1", "L2"), ("seed:v1-1.4.3", "L2"), ("seed:FC-C23", "L2")],
             ["seed:fc-veg-adapt-protocol", "seed:fc-id-adjudicate-ai", "seed:v1-4.1.2-T3"],
             "Independent work across normal variation; AI identification aids are credited only after the step 2 quota.",
             [prov("seed:fc-id-adjudicate-ai", DRILL, "1 seeded-error identification set", "detects the seeded errors at the programme's threshold", "")]),
        step(4, "entry", [("seed:DC-CAND-01", "L1"), ("seed:DC-CAND-02", "L1"), ("seed:DC-CAND-13", "L1"), ("seed:v1-7.2.3", "L1")],
             ["seed:fc-txa-field-check", "seed:fc-txa-plausibility", "seed:dc-02-check-output"],
             TXA_NOTE + " Drills use the learner's own season data.",
             [prov("seed:fc-txa-field-check", DRILL, "1 seeded-error field product", "every consequential error flagged", "")]),
        step(5, "journey", [("seed:FC-C24", "L2"), ("seed:v1-4.4.1-B", "L2")],
             ["seed:v1-4.1.1-T2", "seed:fc-qc-collect", "seed:lc-txc-deliver-briefing"],
             "Season capstone: an end-to-end survey unit with QC samples and a crew briefing, signed off on a task book (IO-C01 evaluator)."),
    ],
))

PATHWAYS.append(dict(
    id="seed:lc-pw-cor1-field-technician-to-geospatial-analyst", corridor="COR-1", type="reskill", src=R02, dst=R04,
    prefLabel="Exploratory pathway: field resource technician to geospatial and remote sensing analyst",
    definition=("Reskills a journey-level field technician into a geospatial and remote sensing analyst role, teaching only the "
                "role-profile delta (spatial analysis, image analysis, data QC, validation and decision support) and keeping the "
                "learner's field ground truth as a defined 20-30% field component (ADR-0026 R6; LC-PW-03 branch A). Exploratory."),
    modes=["CL", "OL", "FD", "WBL", "AIP", "CAP", "MEN"],
    hours=320, months=9,
    cost="[J] 250-400 structured hours; a community-college certificate may fit Workforce Pell where a governor-approved programme exists [E: V3-03].",
    rpl=["seed:crd-gisp", "seed:crd-remote-pilot-certificate"],
    alt=["Calibration assignments on the learner's former field programme replace lost cruising or plot seasons for new entrants only if the agency keeps entry field seasons; this pathway must not be used to stop hiring field entrants [J]."],
    steps=[
        step(1, "journey", [("seed:v1-2.1.4", "L1"), ("seed:v1-2.1.4", "L2"), ("seed:DC-CAND-08", "L1")],
             ["seed:v1-2.1.1-T2", "seed:v1-2.1.4-T1", "seed:v1-2.2.4-T1"],
             "Spatial analysis and scripting; tool modules are tagged and expire (R8).",
             [prov("seed:v1-2.2.4-T1", QUOTA, "1 processing step done by hand on a sample", "the script reproduces the manual result", "Ac/Lo/P")]),
        step(2, "journey", [("seed:v1-2.1.2", "L1"), ("seed:v1-2.1.2", "L2"), ("seed:v1-2.2.3", "L2")],
             ["seed:dc-212-preprocess", "seed:v1-2.1.2-T2", "seed:v1-2.1.2-T3", "seed:v1-2.2.3-T2"],
             "Image analysis and data quality; automated classification is credited only after the by-hand quota.",
             [prov("seed:v1-2.1.2-T2", QUOTA, "2 reference tiles interpreted and digitized by hand", "learner names the classifier's characteristic confusions", "Ac/Lo/P"),
              prov("seed:v1-2.2.3-T2", QUOTA, "1 full manual dataset audit", "audit record reviewed by a senior analyst", "Ac/Lo/P")]),
        step(3, "journey", [("seed:FC-C02", "L1"), ("seed:FC-C02", "L2")],
             ["seed:fc-gt-collect-blind", "seed:fc-gt-mismatch", "seed:fc-veg-validate-remote"],
             "No pixel without plot (R6): field calibration practicum, 20-30% of pathway time, observed in the field.",
             [prov("seed:fc-gt-collect-blind", OBS, "1 field validation sample collected blind to predictions", "reference protocol followed; evaluator sign-off", "")]),
        step(4, "journey", [("seed:DC-CAND-13", "L2"), ("seed:DC-CAND-11", "L2"), ("seed:DC-CAND-09", "L2")],
             ["seed:dc-13-sample-validate", "seed:dc-212-circularity-check", "seed:dc-09-independent-validation", "seed:dc-11-retain-uncertainty"],
             "Validation at volume and honest uncertainty.",
             [prov("seed:dc-13-sample-validate", DRILL, "1 seeded-error batch", "batch error estimate within the stated interval", "")]),
        step(5, "journey", [("seed:DC-CAND-22", "L2"), ("seed:SC-C18", "L2")],
             ["seed:dc-22-decision-map", "seed:sc-write-decision-memo"],
             "No model without a decision owner (R6): capstone calibration report and decision memo defended to the accountable official."),
    ],
))

PATHWAYS.append(dict(
    id="seed:lc-pw-cor1-field-technician-to-ground-truth-steward", corridor="COR-1", type="upskill", src=R02, dst=R05,
    prefLabel="Exploratory pathway: field resource technician to ground-truth and validation steward (emerging role)",
    definition=("Upskills a journey-level field technician into the emerging ground-truth and validation steward role: designing "
                "and collecting field reference data, calibrating observers, judging the fitness of remote and AI products, and "
                "transferring that judgment to others. The target role is emerging, with the counter-signal that validation may be "
                "absorbed into vendor services (mvp_role_set.csv). Exploratory."),
    modes=["FD", "WBL", "MEN", "CL", "CAP"],
    hours=200, months=12,
    cost="[J] Mostly field time and senior-analyst mentoring; reference-data campaigns are the main direct cost.",
    rpl=[],
    alt=["Seasonal reference-data campaigns shared across agencies can supply field exposure where single programmes lack plots [S]."],
    steps=[
        step(1, "journey", [("seed:FC-C02", "L2"), ("seed:FS-C04", "L2")],
             ["seed:fc-gt-design-sample", "seed:fs-c04-collect-labels", "seed:fs-c04-maintain"],
             "Reference-data design and collection with an analyst.",
             [prov("seed:fs-c04-collect-labels", OBS, "1 labelled sample campaign, observed", "metadata complete; evaluator sign-off", "")]),
        step(2, "journey", [("seed:FC-C31", "L2"), ("seed:DC-CAND-03", "L2")],
             ["seed:fc-qa-calibration-session", "seed:fc-qa-blind-check", "seed:dc-03-sample-design"],
             "Observer calibration and sampling design.",
             [prov("seed:fc-qa-blind-check", OBS, "1 blind re-measurement of a crew sample", "differences computed against tolerances", "")]),
        step(3, "senior", [("seed:DC-CAND-09", "L2"), ("seed:DC-CAND-13", "L3"), ("seed:FC-C02", "L3")],
             ["seed:fs-c04-regional-validation", "seed:fc-gt-fitness", "seed:dc-13-accept-batch"],
             "Fitness-for-use decisions on remote and AI products."),
        step(4, "senior", [("seed:IO-C01", "L3"), ("seed:FH-C07", "L2")],
             ["seed:lc-txd-rate-performance", "seed:lc-txd-field-walkthrough", "seed:fc-qa-retrain-decision"],
             "Formation of others and knowledge continuity: evaluate observers and capture site-specific knowledge from departing staff."),
        step(5, "senior", [("seed:DC-CAND-11", "L2"), ("seed:SC-C18", "L2")],
             ["seed:dc-11-brief-official", "seed:fc-gt-feedback"],
             "No model without a decision owner (R6): brief the accountable official on what the validation supports."),
    ],
))

PATHWAYS.append(dict(
    id="seed:lc-pw-cor1-field-technician-to-monitoring-data-technician", corridor="COR-1", type="upskill", src=R02, dst=R03,
    prefLabel="Exploratory pathway: field resource technician to monitoring and data technician",
    definition=("Upskills a field technician into the monitoring and data technician role, shifting work from collection to "
                "sensor deployment, data verification and pipeline quality while keeping manual reference measurements as a "
                "standing check against sensors. Exploratory."),
    modes=["FD", "WBL", "OL", "AIP", "MEN"],
    hours=160, months=6,
    cost="[J] Sensor and meter access plus mentor time; state-approved continuing-education hours may count where programmes allow.",
    rpl=[],
    alt=["Manual grab samples and meter readings stay in routine practice as the reference for every sensor (LC-PW-05 pattern) [J]."],
    steps=[
        step(1, "journey", [("seed:FC-C01", "L1"), ("seed:FC-C01", "L2"), ("seed:FC-C24", "L2")],
             ["seed:v1-2.3.1-T1", "seed:fc-sensor-service", "seed:fc-sensor-sidebyside", "seed:v1-4.1.3-T3"],
             "Sensor deployment and servicing, observed in the field.",
             [prov("seed:v1-2.3.1-T1", OBS, "3 sensor installations, observed", "installation records complete; evaluator sign-off", "A/Hi/P"),
              prov("seed:v1-4.1.3-T3", QUOTA, "manual meter reading at every service visit", "logged drift within method tolerance", "V/Med/P")]),
        step(2, "journey", [("seed:v1-2.2.3", "L1"), ("seed:v1-2.2.3", "L2"), ("seed:DC-CAND-04", "L2")],
             ["seed:dc-223-apply-checks", "seed:dc-223-review-flags", "seed:v1-2.6.4-T2", "seed:dc-04-versioning"],
             "Data verification and pipeline quality; automated flags are credited only after the by-hand review.",
             [prov("seed:v1-2.6.4-T2", QUOTA, "1 month of automated flags reviewed by hand", "false-flag and missed-error rates reported", "V/Lo/P")]),
        step(3, "journey", [("seed:v1-4.1.3", "L2"), ("seed:DC-CAND-13", "L2")],
             ["seed:v1-4.1.3-T1", "seed:v1-1.2.4-T1", "seed:fc-sensor-manual-visit"],
             "Reference measurements and the decision to make an unscheduled manual visit.",
             [prov("seed:v1-1.2.4-T1", OBS, "5 observed grab-sampling events", "zero custody defects", "H/Hi/P")]),
        step(4, "journey", [("seed:DC-CAND-11", "L1"), ("seed:DC-CAND-05", "L1")],
             ["seed:dc-11-retain-uncertainty", "seed:dc-02-disclose-use"],
             TXA_NOTE),
    ],
))

# ------------------------------------------------------------------------------------------------ COR-2 fire
PATHWAYS.append(dict(
    id="seed:lc-pw-cor2-corps-to-fire-operations", corridor="COR-2", type="new-hire", src=R01, dst=R06,
    prefLabel="Exploratory pathway: conservation corps member to wildland fire operations (entry)",
    definition=("Moves a corps member into entry wildland fire operations through safety culture, fireline and saw work, fire "
                "behaviour basics and prescribed-fire crew work, evaluated on qualifying assignments. Position qualifications are "
                "gates, not levels (ADR-0003 T-8). Exploratory."),
    modes=["WBL", "FD", "SIM", "CL", "MEN"],
    hours=200, months=12,
    cost="[J] Entry training plus one to two seasons of supervised assignments; aligned federal qualification standards take effect January 2027 [E: V3-13].",
    rpl=["seed:crd-wilderness-first-aid"],
    alt=["Sand-table and scenario simulation for rare events (entrapment, escaped prescribed fire) only; never in place of graduated exposure on assignments (ADR-0026 FC vs LC trade-off)."],
    steps=[
        step(1, "entry", [("seed:v1-4.4.1-B", "L1"), ("seed:v1-4.4.1-A", "L1"), ("seed:v1-4.4.2", "L1"), ("seed:FC-C18", "L1")],
             ["seed:lc-txc-exercise-stop-work", "seed:fc-risk-heat-recognize", "seed:v1-4.4.3-T2", "seed:v1-4.4.2-T1"],
             "Safety culture first: stop-work, heat and smoke illness, navigation and first aid."),
        step(2, "entry", [("seed:v1-4.3.1", "L1"), ("seed:v1-4.5.2", "L1"), ("seed:v1-4.4.5", "L1")],
             ["seed:v1-4.3.1-T1", "seed:v1-4.3.1-T3", "seed:v1-4.5.2-T1", "seed:v1-4.4.5-T1"],
             "Fireline, mop-up, saw work and emergency communication, evaluated only on the assignment type each task is coded for (R5) [E: LC-104].",
             [prov("seed:v1-4.3.1-T1", OBS, "task-book tasks on qualifying incidents", "evaluator sign-off in coded context", "H/Hi/P"),
              prov("seed:v1-4.5.2-T1", OBS, "felling within certification limits, observed by a saw evaluator", "evaluator sign-off", "H/Hi/P")]),
        step(3, "entry", [("seed:v1-4.3.4", "L1"), ("seed:v1-4.3.2", "L1")],
             ["seed:v1-4.3.4-T1", "seed:v1-4.2.3-T1", "seed:v1-4.2.3-T2"],
             "Fire weather and prescribed-fire crew work.",
             [prov("seed:v1-4.3.4-T1", REP, "10 hand calculations of fuel moisture and indices from on-site observations", "within tolerance of the reference calculation", "A/Med/P"),
              prov("seed:v1-4.2.3-T1", OBS, "ignition on qualifying prescribed fires under a firing boss", "evaluator sign-off", "H/Hi/P")]),
        step(4, "journey", [("seed:v1-4.4.1-B", "L2"), ("seed:v1-4.3.1", "L2")],
             ["seed:lc-txc-deliver-briefing", "seed:db-4.3.1-t5", "seed:fc-risk-briefing"],
             "Journey step: briefings and directing a small crew's tactical assignment, with turn-down practice (TX-C L2-L3)."),
    ],
))

PATHWAYS.append(dict(
    id="seed:lc-pw-cor2-fire-operations-to-fire-intelligence", corridor="COR-2", type="reskill", src=R06, dst=R08,
    prefLabel="Exploratory pathway: wildland fire operations to fire intelligence analyst",
    definition=("Reskills journey-level fire operations staff into continuous fire intelligence: predicting fire behaviour, fusing "
                "and adjudicating detections, producing maps and forecasts, ground-truthing automated products and briefing "
                "uncertainty to incident leaders (LC-PW-03 branch B). The target role is emerging (mvp_role_set.csv). Exploratory."),
    modes=["WBL", "SIM", "CL", "AIP", "MEN", "FD"],
    hours=300, months=18,
    cost="[J] Course work plus one to two fire seasons of duty-officer and incident assignments; detail slots are scarce after 2025-26 staffing losses [E: V1-02].",
    rpl=["seed:crd-wildland-fire-position-qualification", "seed:crd-gisp"],
    alt=["Replayed historical incidents in simulation for rare large-fire events; duty-officer shadowing during the season [J]."],
    steps=[
        step(1, "journey", [("seed:v1-4.3.4", "L2"), ("seed:v1-4.3.4", "L3")],
             ["seed:v1-4.3.4-T2", "seed:db-4.3.4-t4", "seed:v1-4.3.4-T1"],
             "Fire behaviour prediction compared with observed behaviour.",
             [prov("seed:v1-4.3.4-T2", REP, "5 hand-worked spread and intensity predictions checked against observed behaviour", "prediction errors explained before modelled outputs are credited", "A/Hi/C")]),
        step(2, "journey", [("seed:FS-C05", "L2"), ("seed:DC-CAND-13", "L2")],
             ["seed:FS-C05-T2", "seed:FS-C05-T1", "seed:FS-C05-T4"],
             "Fusing and adjudicating detections; accuracy tracking.",
             [prov("seed:FS-C05-T2", DRILL, "1 seeded-error detection set", "false alarms and misses both caught", "")]),
        step(3, "journey", [("seed:v1-2.1.4", "L2"), ("seed:v1-2.1.5", "L2"), ("seed:DC-CAND-12", "L2")],
             ["seed:v1-2.1.1-T3", "seed:dc-12-skill-tracking", "seed:v1-2.7.3-T2"],
             "Incident maps and forecast systems; tool modules expire (R8)."),
        step(4, "journey", [("seed:FC-C02", "L2")],
             ["seed:fc-txa-field-check", "seed:fc-gt-collect-blind"],
             "No pixel without plot (R6): field checks of automated perimeters and fuels products during the season.",
             [prov("seed:fc-txa-field-check", OBS, "field checks on 3 incidents or burns", "evaluator sign-off", "")]),
        step(5, "journey", [("seed:DC-CAND-11", "L2"), ("seed:DB-C29", "L2"), ("seed:DB-C29", "L3")],
             ["seed:dc-11-incident-confidence-briefing", "seed:FS-C05-T3", "seed:v1-4.3.4-T3", "seed:lc-txe-answer-public-questions"],
             "No model without a decision owner (R6): briefing confidence to incident leaders and the public."),
    ],
))

PATHWAYS.append(dict(
    id="seed:lc-pw-cor2-fire-operations-to-fuels-specialist", corridor="COR-2", type="upskill", src=R06, dst=R07,
    prefLabel="Exploratory pathway: wildland fire operations to fuels and prescribed fire specialist",
    definition=("Upskills senior fire operations staff into fuels and prescribed fire work: burn planning, smoke management, "
                "go/no-go decisions on qualifying burns, treatment-effectiveness monitoring, project funding and delivery, and "
                "evaluating burn crew trainees. Exploratory."),
    modes=["WBL", "FD", "CL", "MEN", "SIM"],
    hours=240, months=24,
    cost="[J] Trainee assignments on qualifying prescribed fires depend on burn windows, so calendar time is long.",
    rpl=["seed:crd-wildland-fire-position-qualification", "seed:crd-state-prescribed-burn-manager"],
    alt=["Burn-window shortfalls are covered by burn-plan reviews and tabletop go/no-go exercises, which do not replace observed burns [J]."],
    steps=[
        step(1, "journey", [("seed:v1-4.3.2", "L2"), ("seed:v1-4.3.3", "L2")],
             ["seed:v1-4.3.2-T1", "seed:v1-4.3.3-T1", "seed:db-4.3.3-t4"],
             "Burn plans and field-verified fuels assessment.",
             [prov("seed:db-4.3.3-t4", OBS, "field verification of 2 fuels maps", "corrections recorded; evaluator sign-off", "")]),
        step(2, "journey", [("seed:DB-C15", "L2"), ("seed:DB-C29", "L2")],
             ["seed:DB-C15-T2", "seed:DB-C15-T5", "seed:lc-txe-draft-advisory"],
             "Smoke management and public smoke messaging."),
        step(3, "senior", [("seed:v1-4.3.2", "L3"), ("seed:v1-4.3.4", "L3")],
             ["seed:v1-4.3.2-T2", "seed:db-4.3.2-t4"],
             "Go/no-go and ignition supervision as a trainee on qualifying prescribed fires (R5).",
             [prov("seed:v1-4.3.2-T2", OBS, "go/no-go decisions on qualifying burns under a qualified burn boss", "task-book sign-off", "H/Hi/X")]),
        step(4, "senior", [("seed:DC-CAND-03", "L2"), ("seed:v1-4.3.3", "L3")],
             ["seed:v1-4.3.3-T3", "seed:v1-4.3.2-T3", "seed:dc-03-questions"],
             "Monitoring treatment effectiveness and fire effects."),
        step(5, "senior", [("seed:PS-C03", "L2"), ("seed:PS-C02", "L2"), ("seed:SC-C08", "L2")],
             ["seed:v1-3.1.1-T3", "seed:lc-txf-write-approach", "seed:v1-6.5.3-T2"],
             "Funding and delivering fuels projects with partners (TX-F, agreements)."),
        step(6, "senior", [("seed:IO-C01", "L3")],
             ["seed:lc-txd-rate-performance", "seed:lc-txd-give-feedback"],
             "Formation of others: evaluating burn crew trainees on task books."),
    ],
))

# ------------------------------------------------------------------------------------------------ COR-3 field -> statecraft
PATHWAYS.append(dict(
    id="seed:lc-pw-cor3-restoration-lead-to-review-specialist", corridor="COR-3", type="reskill", src=R09, dst=R10,
    prefLabel="Exploratory pathway: restoration project lead to environmental review specialist (field to statecraft bridge)",
    definition=("Moves a restoration project lead into environmental review: mapping authorizations, setting the level of review, "
                "preparing and checking analyses, coordinating agencies and the public, analyzing comments and defending the "
                "record. It is the field-to-statecraft collaboration bridge kit (P-CM-06). Exploratory."),
    modes=["CL", "WBL", "MEN", "SIM", "AIP", "CAP"],
    hours=160, months=9,
    cost="[J] 120-200 structured hours plus one live review under a senior reviewer.",
    rpl=["seed:crd-cerp"],
    alt=["Shadow-drafting on live reviews and a moot defence before counsel replace the formation once supplied by drafting whole documents [J]."],
    steps=[
        step(1, "journey", [("seed:SC-C01", "L2"), ("seed:v1-1.8.5-A", "L2")],
             ["seed:v1-6.1.3-T2", "seed:sc-prepare-authority-map", "seed:lc-txe-trace-effects"],
             "Authorizations, pathway and effects across systems."),
        step(2, "journey", [("seed:SC-C03", "L2"), ("seed:SL-C08", "L2")],
             ["seed:sc-screen-categorical-exclusion", "seed:v1-6.1.4-T1", "seed:sc-review-ai-drafted-sections"],
             "Level of review and the analysis; reviewing AI-drafted sections is credited only after the by-hand quota (LC-PW-02).",
             [prov("seed:v1-6.1.4-T1", QUOTA, "2 effects sections drafted unaided from the project record", "accepted by a senior reviewer without substantive revision", "A/Hi/C")]),
        step(3, "journey", [("seed:SC-C09", "L2"), ("seed:DB-C29", "L2")],
             ["seed:v1-6.5.2-T1", "seed:v1-6.1.4-T2"],
             "Coordinating agencies and scoping with the public.",
             [prov("seed:v1-6.1.4-T2", OBS, "2 scoping meetings under a senior reviewer", "observer notes against the engagement plan", "H/Hi/C")]),
        step(4, "journey", [("seed:DC-CAND-16", "L1"), ("seed:DC-CAND-13", "L2")],
             ["seed:v1-6.4.4-T2", "seed:dc-13-check-comment-grouping"],
             "Comment analysis: machine-assisted coding is credited only after the by-hand quota.",
             [prov("seed:v1-6.4.4-T2", QUOTA, "1 comment set of at least 200 comments coded by hand", "substantive comments all recovered", "S/Lo/P")]),
        step(5, "journey", [("seed:v1-7.1.3", "L2"), ("seed:SC-C18", "L2")],
             ["seed:v1-7.1.3-T2", "seed:sc-write-decision-memo"],
             "Integrity and the decision memo; capstone moot defence of a level-of-review decision before mock counsel."),
    ],
))

PATHWAYS.append(dict(
    id="seed:lc-pw-cor3-compliance-inspector-onboarding", corridor="COR-3", type="new-hire", src=R12, dst=R12,
    prefLabel="Exploratory pathway: onboarding a new environmental compliance inspector to independent inspection",
    definition=("Takes a new hire from entry to journey level in the compliance inspector role over about twelve months: "
                "safety, independence, field sampling, shadowed then observed inspections, enforcement documentation, public "
                "contact and AI-output validation (LC-PW-01 adapted). Exploratory."),
    modes=["WBL", "FD", "CL", "OL", "SIM", "AIP", "MEN", "CAP"],
    hours=250, months=12,
    cost="[J] 200-300 structured hours alongside productive work; the binding cost is evaluator time for observed inspections.",
    rpl=["seed:crd-hazwoper"],
    alt=["Mock inspections at a training facility can stand in for scarce live inspections in the shadowing stage only [J]."],
    steps=[
        step(1, "entry", [("seed:v1-4.4.1-B", "L1"), ("seed:SL-C03", "L1"), ("seed:PS-C18", "L1")],
             ["seed:lc-txc-report-near-miss", "seed:sc-plan-inspection", "seed:sc-disclose-assignment-interests"],
             "Facility safety, inspection planning and independence."),
        step(2, "entry", [("seed:v1-4.1.3", "L1"), ("seed:FC-C24", "L1")],
             ["seed:v1-1.2.4-T1", "seed:v1-4.1.3-T1", "seed:fc-coc-complete"],
             "Field sampling with custody; supervised repetitions before any automated QC is credited.",
             [prov("seed:v1-1.2.4-T1", OBS, "5 observed sampling events", "zero custody defects", "H/Hi/P")]),
        step(3, "entry", [("seed:SL-C03", "L2"), ("seed:v1-2.2.3", "L1")],
             ["seed:v1-6.1.2-T1", "seed:sc-collect-inspection-evidence", "seed:sc-write-inspection-report", "seed:v1-2.2.3-T2"],
             "Shadow 10 inspections, then lead 5 under observation; inspection reports reviewed by a senior inspector.",
             [prov("seed:v1-6.1.2-T1", OBS, "10 shadowed then 5 observed inspections", "evaluator sign-off (IO-C01 regulatory-inspector enactment)", "A/Hi/C"),
              prov("seed:v1-2.2.3-T2", QUOTA, "1 manual audit of a facility's monitoring reports", "audit reviewed before automated screening is credited", "Ac/Lo/P")]),
        step(4, "entry", [("seed:DB-C29", "L1"), ("seed:SL-C10", "L1")],
             ["seed:lc-txe-answer-public-questions", "seed:sc-answer-compliance-questions"],
             "Public contact and compliance assistance."),
        step(5, "journey", [("seed:DC-CAND-13", "L1"), ("seed:v1-7.1.3", "L1")],
             ["seed:v1-7.2.1-T2", "seed:v1-7.1.3-T1"],
             TXA_NOTE,
             [prov("seed:v1-7.2.1-T2", DRILL, "1 seeded-error AI compliance summary", "every error that changes a compliance conclusion flagged", "H/Hi/P")]),
        step(6, "journey", [("seed:SL-C04", "L2")],
             ["seed:v1-6.1.5-T2", "seed:sc-select-enforcement-response"],
             "Enforcement documentation; capstone end-to-end inspection file at month 11."),
    ],
))

PATHWAYS.append(dict(
    id="seed:lc-pw-cor3-inspector-to-permit-writer", corridor="COR-3", type="upskill", src=R12, dst=R11,
    prefLabel="Exploratory pathway: compliance inspector to environmental permit writer",
    definition=("Upskills a journey-level inspector into permit writing: completeness review, deriving limits, drafting "
                "enforceable conditions and fact sheets, reviewing AI-drafted permits, responding to comments and guarding "
                "independence. Mirrors the pre-registered state pathway from water-quality specialist to permit writer. Exploratory."),
    modes=["CL", "WBL", "MEN", "AIP", "SIM"],
    hours=180, months=12,
    cost="[J] Mostly supervised permit work under a senior writer.",
    rpl=["seed:crd-state-inspector-credential"],
    alt=["Drafting conditions for retired permits as practice cases where live drafting is scarce [J]."],
    steps=[
        step(1, "journey", [("seed:SL-C02", "L1"), ("seed:SL-C02", "L2")],
             ["seed:sc-check-permit-completeness", "seed:sc-derive-permit-limits"],
             "Completeness review and deriving limits."),
        step(2, "journey", [("seed:SC-C16", "L2"), ("seed:SC-C12", "L2")],
             ["seed:sc-draft-permit-fact-sheet", "seed:sc-update-procedure-version"],
             "Enforceable conditions and current procedures; by-hand drafting before AI-drafted permits are reviewed.",
             [prov("seed:sc-draft-permit-fact-sheet", QUOTA, "2 permits' conditions and fact sheets drafted unaided", "each condition traceable to its basis; senior writer accepts", "")]),
        step(3, "journey", [("seed:DC-CAND-13", "L2")],
             ["seed:sc-review-ai-drafted-permit", "seed:sc-verify-ai-draft-instrument"],
             "Reviewing AI-drafted permits, credited after the step 2 quota.",
             [prov("seed:sc-review-ai-drafted-permit", DRILL, "1 seeded-error AI-drafted permit", "every condition lacking a basis corrected", "")]),
        step(4, "journey", [("seed:DB-C29", "L2"), ("seed:SC-C01", "L2")],
             ["seed:sc-respond-permit-comments", "seed:v1-6.1.3-T1"],
             "Public comments and guiding applicants."),
        step(5, "journey", [("seed:PS-C18", "L2"), ("seed:v1-7.1.3", "L2")],
             ["seed:sc-screen-assignment-conflicts", "seed:v1-7.1.3-T2"],
             "Independence across the regulator-regulated boundary."),
    ],
))

PATHWAYS.append(dict(
    id="seed:lc-pw-cor3-specialist-to-programme-manager", corridor="COR-3", type="upskill", src=R10, dst=R13,
    prefLabel="Exploratory pathway: senior environmental specialist to natural resource and environmental programme manager",
    definition=("Upskills a senior review, permitting or inspection specialist (R10 shown; R11 and R12 follow the same steps with "
                "recognition of prior learning) into programme management, where public budgets, formation of others, knowledge "
                "continuity, project and funding delivery, systems trade-offs and briefing concentrate. Exploratory."),
    modes=["CL", "WBL", "MEN", "COP", "CAP"],
    hours=120, months=18,
    cost="[J] Short courses plus a rotation or acting assignment; mentor time from a serving programme manager.",
    rpl=[],
    alt=["An acting assignment or rotation supplies the formation once gained by long apprenticeship to a manager [J]."],
    steps=[
        step(1, "senior", [("seed:SC-C10", "L2"), ("seed:SC-C10", "L3")],
             ["seed:sc-prepare-budget-justification", "seed:sc-reconcile-appropriations", "seed:sc-brief-appropriators"],
             "Public budgets and appropriations."),
        step(2, "senior", [("seed:v1-7.2.2", "L2"), ("seed:v1-7.2.2", "L3"), ("seed:IO-C01", "L3")],
             ["seed:v1-7.2.2-T1", "seed:v1-7.2.2-T2", "seed:lc-txd-give-feedback"],
             "Formation of others: the learner writes a supervisor formation plan for one entry role in the unit."),
        step(3, "senior", [("seed:FH-C07", "L3")],
             ["seed:lc-txd-identify-single-incumbent", "seed:lc-txd-elicit-interview", "seed:v1-3.5.4-T1"],
             "Knowledge continuity before departures."),
        step(4, "lead", [("seed:PS-C03", "L3"), ("seed:PS-C02", "L3"), ("seed:SC-C08", "L3")],
             ["seed:v1-3.1.3-T3", "seed:lc-txf-decide-pursuit", "seed:v1-6.5.4-T1"],
             "Delivering and funding work with partners."),
        step(5, "lead", [("seed:v1-1.8.5-A", "L3"), ("seed:SC-C11", "L3"), ("seed:SC-C18", "L3"), ("seed:v1-7.1.2", "L3")],
             ["seed:lc-txe-compare-interventions", "seed:sc-assess-reversal-risk", "seed:sc-brief-decision-maker", "seed:v1-7.1.2-T2"],
             "Systems trade-offs, durable choices and briefing."),
        step(6, "lead", [("seed:v1-7.2.2", "L4"), ("seed:v1-4.4.1-B", "L4")],
             ["seed:lc-txc-design-learning-process", "seed:lc-txd-set-by-hand-quota", "seed:lc-txd-advise-ai-adoption"],
             "Lead step: programme-level formation and safety-culture design. Supervision (v1 3.3.1 successor) CLOs are added when authored."),
    ],
))
