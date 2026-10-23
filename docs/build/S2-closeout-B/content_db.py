"""DB (A6) content for S2 close-out builder B: core residue DB-C42 and DB-C05 (work-order rows 2-3).

Content evidence label J (DB Phase 2 candidates and sources named in each record); basis in editorialNote.
"""
from s2b_lib import AG  # noqa: F401

DBR = ["DB"]
T = "task-book-observation"
WS = "work-sample"
RA = "record-audit"
SEW = "seeded-error-work-sample"
SIM = "simulation-role-play"
PR = "portfolio-review"

ICS_GATE = [{"credential": "seed:crd-nims-ics-training", "kind": "required"}]

DB_C42 = {
    "id": "seed:DB-C42", "roles": DBR, "row": "2",
    "label": "Coordinate environmental response operations within incident command",
    "alt": ["Environmental emergency response", "Incident command system (ICS) roles",
            "Serve in incident roles as a collateral duty"],
    "definition": (
        "Performing an assigned environmental, technical-specialist, unit or command role inside a standardized "
        "incident command structure during wildfire, spill, flood, drinking water or public-health emergencies: taking "
        "a position, working to incident objectives by operational period, supplying environmental inputs to the "
        "incident action plan, keeping the unit log and resource status, building unified command across agencies, and "
        "handing over or demobilizing. Covers collateral-duty service by staff whose primary job is not response. "
        "Excludes suppression tactics (v1 4.3.1), field emergency communication and incident reporting (v1 4.4.5), "
        "public risk communication (DB-C29) and position qualifications, which are credential gates."),
    "statement": (
        "Takes an assigned position in an incident command structure during environmental emergencies, works to the "
        "incident objectives for each operational period, supplies environmental inputs to the incident action plan, "
        "keeps the unit log and resource status current, and hands the position over or demobilizes without loss of "
        "commitments, coordinating with cooperating agencies under unified command."),
    "reusability": "cross-subsector",
    "learningDesign": {"assessmentContext": {"en": "Assess on incident assignments or functional exercises with a position task book and a qualified evaluator; rare-event skill, so simulation and exercises carry most of the formation."},
                       "recommendedModes": ["SIM", "WBL", "MEN"], "prerequisites": ["seed:v1-4.4.5"]},
    "sources": ["DB-030", "DB-053", "FH-025", "FH-035"],
    "derived": [{"v1Key": "v1:4.3.1", "relation": "split-from", "note": "incident command system part of v1 4.3.1 (v1_disposition.csv: ICS participation goes to core DB-C42)"},
                {"v1Key": "v1:4.3.1:advanced:I9", "relation": "rewritten"},
                {"v1Key": "v1:4.3.1:advanced:I7", "relation": "rewritten"},
                {"v1Key": "v1:4.3.1:intermediate:I8", "relation": "rewritten"}],
    "adr": ["ADR-0030", "ADR-0003", "ADR-0004", "ADR-0018"],
    "note": (
        "S2 close-out B (A6 DB; ADR-0030 §4 core residue). Survivor of DG-DB-C42: absorbs FH-C09 (incident roles as a "
        "collateral duty; the qualifications themselves are Credential gates, ADR-0003 T-8) and the incident command "
        "part of v1 4.3.1 (wildland firefighting stays in MOD-11). Operating within a standardized incident command "
        "structure is shared by fire, spill, flood and public-health response, so the task core recurs across modules; "
        "module enactments in hazards, forest and envhealth. Needed by R06-R08 (P1) and R26, R30 (P2). The "
        "position-qualification systems and their alignment dates are L5 instruments and Credential records, not text "
        "here. Basis [J]: DB and FH Phase 2 candidates and sources."),
    "levels": {
        "L1": [
            {"id": "seed:ind-db-c42-l1-a", "mode": "unaided", "methods": [T, RA],
             "text": "Reports to the supervisor named in the incident organization chart after check-in, recording the assignment, reporting time and resource order in the unit log.",
             "served": ["seed:db-c42-take-position"]},
            {"id": "seed:ind-db-c42-l1-b", "mode": "unaided", "methods": [RA, T],
             "text": "Records each operational period's actions, resource changes and safety events in the unit log so that the log reconciles with the incident action plan at shift change.",
             "served": ["seed:db-c42-unit-log"], "derived": [{"v1Key": "v1:4.3.1:intermediate:I8", "relation": "rewritten"}]},
        ],
        "L2": [
            {"id": "seed:ind-db-c42-l2-a", "mode": "unaided", "methods": [T, WS], "att": "ATT-AUT",
             "text": "Prepares the environmental inputs to an incident action plan for one operational period, listing sampling locations, protective-action thresholds and resource needs before the planning deadline.",
             "served": ["seed:db-c42-iap-inputs"]},
            {"id": "seed:ind-db-c42-l2-b", "mode": "unaided", "methods": [T, SIM], "att": "ATT-CPX",
             "text": "Adjusts an assigned environmental task when field observations differ from the incident action plan, notifying the supervisor and recording the change before the next briefing.",
             "served": ["seed:db-c42-take-position"]},
            {"id": "seed:ind-db-c42-l2-c", "mode": "unaided", "methods": [T, RA], "att": "ATT-AUT",
             "text": "Briefs an incoming relief on the position's open tasks, hazards and commitments from the unit log before the assignment is transferred.",
             "served": ["seed:db-c42-transfer"]},
        ],
        "L3": [
            {"id": "seed:ind-db-c42-l3-a", "mode": "unaided", "methods": [T, PR], "att": "ATT-SCO",
             "text": "Sets environmental unit objectives across operational periods, reconciling cooperating agencies' sampling and cleanup priorities into one plan that the planning section accepts.",
             "served": ["seed:db-c42-iap-inputs", "seed:db-c42-unified-command"]},
            {"id": "seed:ind-db-c42-l3-b", "mode": "assisted", "methods": [SEW, T], "att": "ATT-AUG",
             "text": "Reviews a template- or AI-drafted incident action plan section against current field reports, correcting or rejecting each item that conflicts with observed conditions before approval.",
             "served": ["seed:db-c42-review-drafted-iap"]},
            {"id": "seed:ind-db-c42-l3-c", "mode": "unaided", "methods": [WS, RA], "att": "ATT-SCO",
             "text": "Conducts an after-action review of the environmental unit's response, recording what happened, why, and the corrective action assigned to each named position.",
             "served": ["seed:db-c42-aar"], "derived": [{"v1Key": "v1:4.3.1:advanced:I7", "relation": "rewritten"}]},
        ],
        "L4": [
            {"id": "seed:ind-db-c42-l4-a", "mode": "unaided", "methods": [SIM, PR], "att": "ATT-SCO",
             "text": "Establishes unified command for a multi-jurisdiction environmental emergency, documenting each agency's authority, objectives and delegated responsibilities in the initial incident action plan.",
             "served": ["seed:db-c42-unified-command"], "derived": [{"v1Key": "v1:4.3.1:advanced:I9", "relation": "rewritten"}]},
            {"id": "seed:ind-db-c42-l4-b", "mode": "unaided", "methods": [T, PR], "att": "ATT-FOR",
             "text": "Plans trainee and collateral-duty assignments within an incident organization so that each trainee works under a qualified evaluator and lapsed position currency is recorded.",
             "served": ["seed:db-c42-collateral-release", "seed:db-c42-take-position"]},
        ],
    },
    "tasks": [
        {"id": "seed:db-c42-take-position", "wf": "WF-RESPOND", "field": "on-site-preferred", "formation": "partial",
         "text": "Take an assigned incident position by reviewing the incident action plan with the supervisor and confirming communications before the operational period begins",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "multi-year-or-rare-event", "placeBoundness": "general",
                    "credentialGate": "internal-qualification", "currencyDecay": "H"},
         "gates": ICS_GATE + [{"credential": "seed:crd-wildland-fire-position-qualification", "kind": "preferred"}],
         "contrib": ["seed:v1-4.4.1-B"]},
        {"id": "seed:db-c42-iap-inputs", "wf": "WF-RESPOND", "field": "on-site-preferred", "formation": "yes",
         "text": "Prepare the environmental inputs to the incident action plan, listing sampling locations, protective-action thresholds and resource needs for the next operational period",
         "regime": {"mentorshipDependence": "H", "cycleDependence": "multi-year-or-rare-event", "placeBoundness": "general",
                    "credentialGate": "internal-qualification", "currencyDecay": "M"}, "gates": ICS_GATE},
        {"id": "seed:db-c42-review-drafted-iap", "wf": "WF-RESPOND", "field": "on-site-preferred", "formation": "yes",
         "text": "Review a template- or AI-drafted incident action plan section against current field reports, correcting items that conflict with observed conditions before approval",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "multi-year-or-rare-event", "placeBoundness": "general",
                    "credentialGate": "internal-qualification", "currencyDecay": "M"},
         "note": "G-2 split: review and correction of a drafted plan section, alongside the production task seed:db-c42-iap-inputs."},
        {"id": "seed:db-c42-unit-log", "wf": "WF-RESPOND", "field": "on-site-preferred", "formation": "no",
         "text": "Maintain the unit log and resource status for an operational period so that the record reconciles with the incident action plan at shift change",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "general",
                    "credentialGate": "internal-qualification", "currencyDecay": "M"}},
        {"id": "seed:db-c42-transfer", "wf": "WF-RESPOND", "field": "on-site-preferred", "formation": "partial",
         "text": "Brief an incoming relief or incident management team on objectives, open hazards and commitments before transferring a position or command",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "multi-year-or-rare-event", "placeBoundness": "general",
                    "credentialGate": "internal-qualification", "currencyDecay": "M"}},
        {"id": "seed:db-c42-unified-command", "wf": "WF-RESPOND", "field": "on-site-preferred", "formation": "partial",
         "rel": ["intergovernmental"],
         "text": "Establish unified command with cooperating agencies for a multi-jurisdiction environmental emergency, recording each agency's authority, objectives and delegated responsibilities",
         "regime": {"mentorshipDependence": "H", "cycleDependence": "multi-year-or-rare-event", "placeBoundness": "general",
                    "credentialGate": "internal-qualification", "currencyDecay": "H"}, "gates": ICS_GATE},
        {"id": "seed:db-c42-collateral-release", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "no",
         "text": "Arrange release from primary duties with the home-unit supervisor before accepting an incident assignment, documenting who covers the primary work",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "seasonal", "placeBoundness": "general",
                    "credentialGate": "none", "currencyDecay": "L"},
         "note": "From FH-C09 (collateral-duty incident service)."},
        {"id": "seed:db-c42-aar", "wf": "WF-LEARN", "field": "remote-capable", "formation": "partial",
         "text": "Conduct an after-action review of an environmental response, recording corrective actions and the position responsible for each",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "multi-year-or-rare-event", "placeBoundness": "general",
                    "credentialGate": "none", "currencyDecay": "M"}},
    ],
    "enactments": [
        {"id": "seed:ena-db-c42-hazards", "module": "hazards", "subsectors": ["C03"],
         "label": "Emergency management enactment of environmental response within incident command",
         "note": "Flood, storm and multi-hazard response under emergency management: the environmental unit supports debris management, hazardous-materials and oil response, drinking water and wastewater emergencies and damage assessment within the emergency operations centre and field command; disaster declarations and public assistance documentation drive record-keeping from the first operational period."},
        {"id": "seed:ena-db-c42-forest", "module": "forest", "subsectors": ["L07", "L01"],
         "label": "Wildland fire enactment of environmental response within incident command",
         "note": "Wildland fire incidents staff command and general staff and technical-specialist positions from fire and non-fire staff, many serving as a collateral duty; resource advisers, burned-area and smoke specialists work to incident objectives, and position task books and currency rules govern who may fill each position."},
        {"id": "seed:ena-db-c42-envhealth", "module": "envhealth", "subsectors": ["H01", "H02"],
         "label": "Public health enactment of environmental response within incident command",
         "note": "Environmental health staff work within incident command during outbreaks, water or food contamination, chemical releases, extreme heat and shelter operations: they supply exposure assessments, sampling plans and protective-action recommendations to the incident action plan and coordinate with public health emergency preparedness structures."},
    ],
}

DB_C05 = {
    "id": "seed:DB-C05", "roles": DBR, "row": "3",
    "label": "Manage physical assets and capital plans with risk-based asset management",
    "alt": ["Asset management", "Equipment and fleet management", "Facilities operations and maintenance",
            "Capital improvement planning"],
    "definition": (
        "Keeping physical assets (treatment plants and pipe networks, roads and trails, buildings and field stations, "
        "fleets and field equipment) able to deliver a stated level of service at the lowest defensible life-cycle cost: "
        "inventory, condition and criticality assessment, likelihood and consequence-of-failure scoring, maintenance "
        "planning, repair, renewal and replacement decisions, and long-term capital and financial plans. Covers facility "
        "operation and maintenance and equipment management as contexts. Excludes operating treatment processes "
        "(DB-C01, DB-C02), protecting operational technology (DB-C06) and executing public budgets (SC-C10)."),
    "statement": (
        "Maintains an asset inventory with condition and criticality, scores likelihood and consequence of failure, "
        "plans maintenance and renewal against stated levels of service, and builds capital and financial plans that "
        "justify repair, renewal or replacement timing and funding, so that infrastructure, facilities and equipment "
        "keep delivering service at the lowest defensible life-cycle cost."),
    "reusability": "cross-subsector",
    "sources": ["DB-041", "DB-042"],
    "derived": [{"v1Key": "v1:3.3.2", "relation": "merged-from", "note": "equipment and asset management"},
                {"v1Key": "v1:3.3.3", "relation": "merged-from", "note": "facilities operations and maintenance"}],
    "adr": ["ADR-0030", "ADR-0003", "ADR-0004", "ADR-0018"],
    "note": (
        "S2 close-out B (A6 DB; ADR-0030 §4 core residue). Absorbs v1 3.3.2 (equipment and asset management) and "
        "3.3.3 (facilities operations and maintenance), which are contexts of risk-based asset management (SC verdict: "
        "not Statecraft). Recurs in utilities, parks and facilities, roads and trails, and fleets (G-4); module "
        "enactments in water, forest and parks were written in WP-06. Technical, managerial and financial capacity is a "
        "main determinant of small-system compliance [J]. Asset-management and maintenance software is L4. Needed by "
        "R25 and R21 (P2). Basis [J]: DB Phase 2 candidate DB-C05 and sources."),
    "levels": {
        "L1": [
            {"id": "seed:ind-db-c05-l1-a", "mode": "unaided", "methods": [RA, T],
             "text": "Records asset condition during a scheduled inspection using the programme's condition-rating scale, attaching photographs so that each rating can be checked.",
             "served": ["seed:v1-3.3.3-T1", "seed:v1-3.3.2-T1"], "derived": [{"v1Key": "v1:3.3.2:foundational:I5", "relation": "rewritten"}]},
            {"id": "seed:ind-db-c05-l1-b", "mode": "unaided", "methods": [T, RA],
             "text": "Reports an equipment or facility defect as a work order with location, symptom and safety effect before the asset is returned to service or tagged out.",
             "served": ["seed:v1-3.3.3-T1"], "derived": [{"v1Key": "v1:3.3.2:foundational:I3", "relation": "rewritten"},
                                                          {"v1Key": "v1:3.3.3:foundational:I2", "relation": "rewritten"}]},
        ],
        "L2": [
            {"id": "seed:ind-db-c05-l2-a", "mode": "unaided", "methods": [WS, RA], "att": "ATT-AUT",
             "text": "Schedules preventive maintenance for an asset class from manufacturer intervals and failure history, revising intervals when work-order records show repeat failures.",
             "served": ["seed:v1-3.3.2-T2"], "derived": [{"v1Key": "v1:3.3.2:intermediate:I2", "relation": "rewritten"}]},
            {"id": "seed:ind-db-c05-l2-b", "mode": "unaided", "methods": [WS, RA], "att": "ATT-CPX",
             "text": "Scores likelihood and consequence of failure for a set of assets with the programme's risk matrix, documenting the evidence behind each score.",
             "served": ["seed:db-c05-risk-score"]},
            {"id": "seed:ind-db-c05-l2-c", "mode": "assisted", "methods": [SEW, RA], "att": "ATT-AUG",
             "text": "Checks automated condition scores against a sample of inspection records, correcting each score that the records do not support before it enters the renewal plan.",
             "served": ["seed:db-c05-review-auto-scores"]},
        ],
        "L3": [
            {"id": "seed:ind-db-c05-l3-a", "mode": "unaided", "methods": [WS, PR], "att": "ATT-SCO",
             "text": "Prepares a renewal and replacement plan for an asset portfolio that ranks projects by risk and life-cycle cost and states the level of service each protects.",
             "served": ["seed:db-c05-renewal-plan"], "derived": [{"v1Key": "v1:3.3.2:advanced:I4", "relation": "rewritten"},
                                                                 {"v1Key": "v1:3.3.2:advanced:I5", "relation": "rewritten"}]},
            {"id": "seed:ind-db-c05-l3-b", "mode": "unaided", "methods": [WS, PR], "att": "ATT-SCO",
             "text": "Prepares a capital improvement plan that links each project to rate, reserve or grant funding and shows the service effect of deferring it.",
             "served": ["seed:db-c05-cip"]},
        ],
        "L4": [
            {"id": "seed:ind-db-c05-l4-a", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Sets an organization's asset management policy, defining levels of service, risk tolerance and the rules that decide between repair, renewal and replacement.",
             "served": ["seed:db-c05-renewal-plan"]},
            {"id": "seed:ind-db-c05-l4-b", "mode": "unaided", "methods": [SIM, PR], "att": "ATT-CPX",
             "text": "Defends an asset management plan to a governing body or funder, stating the risk and cost consequences of each funding alternative and the evidence behind them.",
             "served": ["seed:db-c05-defend-plan"]},
        ],
    },
    "tasks": [
        {"id": "seed:v1-3.3.2-T1", "wf": "WF-OPERATE", "field": "on-site-preferred", "formation": "no",
         "text": "Maintain an inventory of vehicles, tools and field equipment that records location, condition and planned replacement date for each item",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "system-specific", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-3.3.2-T2", "wf": "WF-OPERATE", "field": "remote-capable", "formation": "partial",
         "text": "Schedule preventive maintenance and safety inspections for critical assets from failure history and manufacturer intervals",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "seasonal", "placeBoundness": "system-specific", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:v1-3.3.2-T3", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "no",
         "text": "Allocate vehicles and field equipment across crews and projects using utilization records and seasonal demand",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "seasonal", "placeBoundness": "site-specific", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-3.3.3-T1", "wf": "WF-OPERATE", "field": "on-site-required", "formation": "partial",
         "text": "Inspect buildings, field stations and storage facilities for safety, code and maintenance deficiencies, entering each deficiency as a work order",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "site-specific", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:v1-3.3.3-T2", "wf": "WF-OPERATE", "field": "on-site-required", "formation": "partial",
         "text": "Verify that fuel, chemical and waste storage at field stations meets containment and labelling requirements, recording each corrective action",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "site-specific", "credentialGate": "none", "currencyDecay": "M"},
         "contrib": ["seed:v1-4.4.4-A"]},
        {"id": "seed:v1-3.3.3-T3", "wf": "WF-PLAN", "field": "remote-capable", "formation": "no",
         "text": "Plan facility upgrades for energy use and accessibility, ranking projects by life-cycle cost and compliance need",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "site-specific", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:db-c05-risk-score", "wf": "WF-ASSESS", "field": "remote-capable", "formation": "yes",
         "text": "Score likelihood and consequence of failure for each critical asset from condition data and service consequences, documenting the basis for each score",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "system-specific", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:db-c05-review-auto-scores", "wf": "WF-MONITOR", "field": "remote-capable", "formation": "yes",
         "text": "Review automated asset condition scores against a sample of inspection records, correcting unsupported scores before they enter the renewal plan",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "system-specific", "credentialGate": "none", "currencyDecay": "M"},
         "note": "G-2 split: review of automated scoring alongside the production task seed:db-c05-risk-score."},
        {"id": "seed:db-c05-renewal-plan", "wf": "WF-PLAN", "field": "remote-capable", "formation": "partial",
         "text": "Prepare a renewal and replacement plan that ranks asset projects by risk, life-cycle cost and the level of service each protects",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "system-specific", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:db-c05-cip", "wf": "WF-RESOURCE", "field": "remote", "formation": "partial",
         "text": "Prepare a capital improvement plan that ties each asset project to rate, reserve or grant funding and states the effect of deferral",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "system-specific", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:db-c05-defend-plan", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "partial",
         "modes": ["MODE-ENGAGE"],
         "text": "Present asset management funding alternatives to a governing body, stating the service and risk consequences of each alternative",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
    ],
}

SPECS = [DB_C42, DB_C05]
