"""DC (A4) and LM with FS (A9) content for S2 close-out builder B: v1 5.6.5 rewritten in place (row 17), FS-C15
(row 10) and FS-C09 (row 9). Content evidence label J; basis in editorialNote.
"""
DC = ["DC"]
LMFS = ["LM", "FS"]
T, WS, RA, SEW, SIM, PR, BARS = ("task-book-observation", "work-sample", "record-audit", "seeded-error-work-sample",
                                 "simulation-role-play", "portfolio-review", "structured-interview-bars")
PLOG = "prediction-log-calibration"


def d(key, rel="rewritten"):
    return {"v1Key": key, "relation": rel}


def rg(m="M", c="none", p="general", g="none", u="M"):
    return {"mentorshipDependence": m, "cycleDependence": c, "placeBoundness": p, "credentialGate": g, "currencyDecay": u}


PARTICIPATORY = {
    "id": "seed:v1-5.6.5", "roles": DC, "row": "17",
    "label": "Conduct participatory and community-based environmental research",
    "alt": ["Participatory methods and community-based research", "Community-based participatory research (CBPR)",
            "Participatory mapping", "Co-produced research"],
    "definition": (
        "Designing and carrying out environmental research and monitoring in partnership with community members who "
        "share in setting questions, choosing methods, collecting and interpreting data and deciding how findings are "
        "used: partnership and data agreements, research ethics review and consent, participatory methods such as "
        "participatory mapping and photo-based methods, building community data capacity, joint interpretation and "
        "returning findings in usable form. Excludes community-science data collection to a programme protocol "
        "(v1 5.4.4), conventional social science surveys (v1 5.6.2), collaborative decision processes (v1 5.2.3) and "
        "cumulative-burden analysis (DB-C52)."),
    "statement": (
        "Builds a research partnership in which community members share in setting the questions, choosing methods, "
        "collecting and interpreting data and deciding how findings are used; agrees data ownership, access and consent "
        "terms before collection; builds community capacity to collect and analyze data; and returns findings in forms "
        "and languages the community can use."),
    "reusability": "cross-subsector",
    "learningDesign": {"assessmentContext": {"en": "Assess through partnership and data agreements, research protocols, joint-analysis records and partner feedback; field and community settings."},
                       "recommendedModes": ["WBL", "MEN", "CAP"]},
    "derived": [d("v1:6.7.3", "merged-from")],
    "adr": ["ADR-0030", "ADR-0016", "ADR-0007", "ADR-0004", "ADR-0003", "ADR-0011"],
    "note": (
        "S2 close-out B (A4 DC; ADR-0030 §4 core residue). Rewritten in place as the survivor for participatory and "
        "community-based research; absorbs v1 6.7.3 (CBPR; IA duplicate finding). The six v1 task seeds are rewritten so "
        "that the merged duplicates become distinct partnership, interpretation and data-agreement tasks. Enactments for "
        "partners with their own research codes stay held under ADR-0007 §D and are not authored here. Environmental "
        "justice is an altLabel context only (ADR-0016). v1 Expert indicators naming recognition or publication are "
        "retired (B03, B04). Needed by R09 (P1) and R26 (P2). Basis [J]."),
    "levels": {
        "L1": [
            {"id": "seed:dc-pr-l1-a", "mode": "unaided", "methods": [T, SIM],
             "text": "Explains a community study's consent terms and data-access rules to a participant before collecting any data, recording that consent was given.",
             "served": ["seed:dc-pr-ethics-consent"], "derived": [d("v1:6.7.3:foundational:I7"), d("v1:6.7.3:foundational:I1")]},
            {"id": "seed:dc-pr-l1-b", "mode": "unaided", "methods": [RA, T],
             "text": "Collects data with community co-researchers to the agreed protocol, recording who collected each record and any deviation from the protocol.",
             "served": ["seed:v1-5.6.5-T2"], "derived": [d("v1:6.7.3:foundational:I5")]},
        ],
        "L2": [
            {"id": "seed:dc-pr-l2-a", "mode": "unaided", "methods": [RA, PR], "att": "ATT-AUT",
             "text": "Co-designs research questions and methods with community partners in documented meetings, recording which partner proposals were adopted and why others were not.",
             "served": ["seed:v1-5.6.5-T1"], "derived": [d("v1:5.6.5:intermediate:I1"), d("v1:6.7.3:intermediate:I1")]},
            {"id": "seed:dc-pr-l2-b", "mode": "unaided", "methods": [WS, RA], "att": "ATT-KNO",
             "text": "Drafts a data agreement with community partners that states ownership, storage, access, publication review and the handling of data when the project ends.",
             "served": ["seed:v1-6.7.3-T3"]},
            {"id": "seed:dc-pr-l2-c", "mode": "unaided", "methods": [T, WS], "att": "ATT-CPX",
             "text": "Runs a participatory mapping or photo-based session with community members, checking the results back with participants before analysis.",
             "served": ["seed:dc-pr-participatory-mapping"], "derived": [d("v1:5.6.5:intermediate:I2")]},
        ],
        "L3": [
            {"id": "seed:dc-pr-l3-a", "mode": "unaided", "methods": [RA, PR], "att": "ATT-CPX",
             "text": "Interprets findings with community partners in a joint analysis session, recording where community and researcher interpretations differ and how the report presents each.",
             "served": ["seed:v1-6.7.3-T2"], "derived": [d("v1:6.7.3:intermediate:I6")]},
            {"id": "seed:dc-pr-l3-b", "mode": "unaided", "methods": [WS, RA], "att": "ATT-FOR",
             "text": "Designs a training sequence that lets community members collect and analyze project data to the study's quality standard, checking their first datasets against it.",
             "served": ["seed:v1-5.6.5-T2"], "derived": [d("v1:5.6.5:intermediate:I3"), d("v1:6.7.3:intermediate:I9")]},
            {"id": "seed:dc-pr-l3-c", "mode": "assisted", "methods": [SEW, RA], "att": "ATT-AUG",
             "text": "Reviews AI-generated coding or summaries of community-contributed text and images against the sources and partner review, correcting each misattribution before release.",
             "served": ["seed:dc-pr-review-ai-coding"]},
        ],
        "L4": [
            {"id": "seed:dc-pr-l4-a", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Sets an organization's terms for community research partnerships, covering benefit sharing, data governance, authorship and publication review, for use across projects.",
             "served": ["seed:v1-6.7.3-T1"], "derived": [d("v1:5.6.5:advanced:I1")]},
            {"id": "seed:dc-pr-l4-b", "mode": "unaided", "methods": [PR, RA], "att": "ATT-SCO",
             "text": "Evaluates a portfolio of community research partnerships against their agreed benefit and accountability terms, recording each shortfall and the corrective action agreed with partners.",
             "served": ["seed:dc-pr-evaluate-partnerships"], "derived": [d("v1:6.7.3:advanced:I5")]},
        ],
    },
    "tasks": [
        {"id": "seed:v1-5.6.5-T1", "wf": "WF-ASSESS", "field": "on-site-preferred", "formation": "yes", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Co-design research questions and methods with community partners, recording which partner proposals were adopted and why",
         "regime": rg("H", "none", "site-specific")},
        {"id": "seed:v1-5.6.5-T2", "wf": "WF-ASSESS", "field": "on-site-preferred", "formation": "yes", "rel": ["public"],
         "text": "Train community members to collect and analyze project data to the study's quality standard, checking their first datasets",
         "regime": rg("M", "seasonal", "site-specific"), "contrib": ["seed:v1-5.4.4"]},
        {"id": "seed:v1-5.6.5-T3", "wf": "WF-ASSESS", "field": "on-site-preferred", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Return research findings to community partners in agreed formats and languages, recording partner responses and requested follow-up",
         "regime": rg("M", "none", "site-specific", u="L")},
        {"id": "seed:v1-6.7.3-T1", "wf": "WF-PLAN", "field": "remote-capable", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Negotiate a research partnership agreement with community partners covering roles, benefits, authorship and the resolution of disagreements",
         "regime": rg("H", "none", "site-specific", u="L"),
         "note": "v1 6.7.3-T1 duplicated 5.6.5-T1 (co-design); rewritten as the partnership-agreement task."},
        {"id": "seed:v1-6.7.3-T2", "wf": "WF-ASSESS", "field": "on-site-preferred", "formation": "yes", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Interpret study results with community partners in a joint analysis session, recording where community and researcher interpretations differ",
         "regime": rg("H", "none", "site-specific"),
         "note": "v1 6.7.3-T2 duplicated 5.6.5-T2 (capacity building); rewritten as the joint-interpretation task."},
        {"id": "seed:v1-6.7.3-T3", "wf": "WF-PLAN", "field": "remote", "formation": "partial",
         "text": "Draft a data agreement with community partners stating ownership, storage, access, publication review and end-of-project handling",
         "regime": rg("M", "none", "general", u="L"), "contrib": ["seed:DC-CAND-07"],
         "note": "v1 6.7.3-T3 duplicated 5.6.5-T3 (accessible findings); rewritten as the data-agreement task."},
        {"id": "seed:dc-pr-ethics-consent", "wf": "WF-ASSESS", "field": "remote", "formation": "partial",
         "text": "Prepare the ethics review and consent materials for a community study, stating risks, data uses and withdrawal rights in plain language",
         "regime": rg("M", "none", "general", u="L")},
        {"id": "seed:dc-pr-participatory-mapping", "wf": "WF-ASSESS", "field": "on-site-required", "formation": "yes", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Run a participatory mapping session with community members, checking the mapped features back with participants before analysis",
         "regime": rg("M", "none", "site-specific")},
        {"id": "seed:dc-pr-review-ai-coding", "wf": "WF-ASSESS", "field": "remote", "formation": "yes",
         "text": "Review AI-generated coding or summaries of community-contributed text and images against the sources and partner review, correcting misattributions",
         "regime": rg("M", "none", "general"), "contrib": ["seed:DC-CAND-13"],
         "note": "G-2 split: review of machine coding alongside joint interpretation (seed:v1-6.7.3-T2)."},
        {"id": "seed:dc-pr-evaluate-partnerships", "wf": "WF-LEARN", "field": "remote-capable", "formation": "partial",
         "text": "Evaluate community research partnerships against their agreed benefit and accountability terms, recording shortfalls and agreed corrective actions",
         "regime": rg("M", "multi-year-or-rare-event", "general", u="L")},
    ],
}

HORIZON = {
    "id": "seed:FS-C15", "roles": LMFS, "row": "10",
    "label": "Scan horizons and translate change signals into workforce decisions",
    "alt": ["Strategic foresight for workforce planning", "Horizon scanning", "Weak-signal monitoring"],
    "definition": (
        "Monitoring technology, policy, labour-market and environmental change signals; maintaining scenarios and "
        "signposts; running structured foresight sessions with managers; and converting the results into dated "
        "workforce moves, both no-regret actions taken now and contingent actions with named triggers, each with an "
        "owner and a review date. Covers signal logging with source and independence, scenario maintenance and trigger "
        "monitoring. Excludes policy and land-use scenario analysis for a decision (v1 6.2.5), operational forecast and "
        "scenario systems (DC-CAND-12), planning for non-analog ecological futures (v1 1.7.5) and position-level "
        "staffing justification (FH-C14)."),
    "statement": (
        "Monitors technology, policy, labour-market and environmental change signals with their sources, maintains "
        "scenarios and signposts, runs foresight sessions with managers, and converts the results into workforce "
        "decisions: no-regret moves made now and contingent moves tied to named triggers, each with an owner and a "
        "review date, revisited when signposts move."),
    "reusability": "transversal",
    "learningDesign": {"assessmentContext": {"en": "Assess through signal logs, scenario and signpost records, session records and the contingent-action register, with prediction-log calibration over time."},
                       "recommendedModes": ["CL", "CAP", "COP"]},
    "sources": ["FS-032"],
    "adr": ["ADR-0030", "ADR-0025", "ADR-0028", "ADR-0004", "ADR-0003"],
    "note": (
        "S2 close-out B (A9 LM with FS; ADR-0030 §4 core residue). Horizon scanning is its own core practice, not a "
        "floor requirement (ADR-0025 §4), and was considered and not merged into v1 6.2.5 (ADR-0030 §3.1). Boundary: "
        "6.2.5 builds scenarios for one policy or land-use decision; DC-CAND-12 runs forecast systems; this competency "
        "turns signals into workforce moves. Spans L3-L5 (strategy cluster). The signal method mirrors EMST's own "
        "change-signal layer (ADR-0028: source, independence, signposts). Needed by R13 at the strategic level (P1) and "
        "R35 (P3). Basis [J]: FS Phase 2 candidate and horizon-scanning protocol."),
    "levels": {
        "L3": [
            {"id": "seed:fs-c15-l3-a", "mode": "unaided", "methods": [RA, PLOG],
             "text": "Logs change signals for a programme's workforce with source, date, source independence and the roles affected, retiring signals that later evidence contradicts.",
             "served": ["seed:fs-c15-log-signals"]},
            {"id": "seed:fs-c15-l3-b", "mode": "unaided", "methods": [RA, WS],
             "text": "Assesses whether recent signals move each scenario signpost, recording the assessment and its confidence in the programme's scenario record.",
             "served": ["seed:fs-c15-map-signposts"]},
            {"id": "seed:fs-c15-l3-c", "mode": "assisted", "methods": [SEW, RA],
             "text": "Checks an AI-generated horizon scan against its cited sources, removing each claim whose source is missing, misread or not independent before the scan is circulated.",
             "served": ["seed:fs-c15-review-ai-scan"]},
        ],
        "L4": [
            {"id": "seed:fs-c15-l4-a", "mode": "unaided", "methods": [SIM, RA], "att": "ATT-SCO",
             "text": "Facilitates a foresight session that tests a workforce plan against at least three scenarios, recording the actions that hold in every scenario.",
             "served": ["seed:fs-c15-foresight-session"]},
            {"id": "seed:fs-c15-l4-b", "mode": "unaided", "methods": [WS, RA], "att": "ATT-CPX",
             "text": "Writes contingent workforce actions with a named trigger, owner and lead time for each, so that managers can act when a signpost moves.",
             "served": ["seed:fs-c15-contingent-actions"]},
        ],
        "L5": [
            {"id": "seed:fs-c15-l5-a", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Sets the organization's horizon-scanning cycle, naming signal sources, independence rules, scenario review dates and the decision forum that acts on triggers.",
             "served": ["seed:fs-c15-scan-cycle"]},
            {"id": "seed:fs-c15-l5-b", "mode": "unaided", "methods": [SIM, PR], "att": "ATT-CPX",
             "text": "Advises executives on workforce investment under uncertainty, presenting no-regret and contingent options with their triggers and the evidence behind each.",
             "served": ["seed:fs-c15-advise-executives"]},
        ],
    },
    "tasks": [
        {"id": "seed:fs-c15-log-signals", "wf": "WF-PLAN", "field": "remote", "formation": "partial",
         "text": "Log workforce change signals with source, date, source independence and the roles affected, retiring signals that later evidence contradicts",
         "regime": rg("M", "none", "general", u="H")},
        {"id": "seed:fs-c15-review-ai-scan", "wf": "WF-PLAN", "field": "remote", "formation": "yes",
         "text": "Review an AI-generated horizon scan against its cited sources, removing claims whose source is missing, misread or not independent",
         "regime": rg("M", "none", "general", u="M"), "contrib": ["seed:DC-CAND-13"],
         "note": "G-2 split: review of a generated scan alongside the production task seed:fs-c15-log-signals."},
        {"id": "seed:fs-c15-map-signposts", "wf": "WF-PLAN", "field": "remote", "formation": "yes",
         "text": "Assess whether recent signals move each scenario signpost, recording the assessment and its confidence for the workforce plan",
         "regime": rg("H", "multi-year-or-rare-event", "general", u="M")},
        {"id": "seed:fs-c15-foresight-session", "wf": "WF-PLAN", "field": "remote-capable", "formation": "partial", "modes": ["MODE-ENGAGE"],
         "text": "Facilitate a foresight session that tests a workforce plan against several scenarios, recording the actions that hold in every scenario",
         "regime": rg("M", "none", "general", u="M")},
        {"id": "seed:fs-c15-contingent-actions", "wf": "WF-PLAN", "field": "remote", "formation": "partial",
         "text": "Write contingent workforce actions that name the trigger, owner and lead time for each action, with a review date",
         "regime": rg("M", "none", "general", u="L")},
        {"id": "seed:fs-c15-scan-cycle", "wf": "WF-MANAGE", "field": "remote", "formation": "no",
         "text": "Set the organization's horizon-scanning cycle, naming signal sources, independence rules, scenario review dates and the forum that acts on triggers",
         "regime": rg("L", "none", "general", u="L")},
        {"id": "seed:fs-c15-advise-executives", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "partial", "modes": ["MODE-ENGAGE"],
         "text": "Advise executives on workforce investment under uncertainty, presenting no-regret and contingent options with their triggers",
         "regime": rg("H", "multi-year-or-rare-event", "general", u="M"), "contrib": ["seed:SC-C18"]},
    ],
}

PRODUCT = {
    "id": "seed:FS-C09", "roles": LMFS, "row": "9", "lifecycle": "emerging", "reviewBy": "2027-10-23",
    "label": "Own and steward a public environmental technology product",
    "alt": ["Product management for permitting and case-management systems", "Public digital service product ownership",
            "Permitting technology product owner"],
    "definition": (
        "Owning a public-sector environmental technology product (a permitting or case-management system, a monitoring "
        "data portal or a public reporting service) over its life: researching how practitioners, applicants and the "
        "public use it, keeping a prioritized backlog and roadmap tied to programme outcomes, writing acceptance "
        "criteria, checking releases against data standards and records requirements, deciding what ships, and leading "
        "adoption and change with the staff who depend on it. Excludes procuring and accepting AI and analytics "
        "services (DC-CAND-20), governing enterprise data and AI portfolios (DC-CAND-21), designing decision-support "
        "products for one decision (DC-CAND-22) and engineering data pipelines (DC-CAND-04)."),
    "statement": (
        "Researches how staff, applicants and the public use an environmental technology product, keeps a prioritized "
        "backlog and roadmap tied to programme outcomes, writes acceptance criteria, checks releases against data "
        "standards and records requirements, decides what ships, and leads adoption with the staff who depend on it, so "
        "that the system serves the programme's legal and public duties."),
    "reusability": "cross-subsector",
    "learningDesign": {"assessmentContext": {"en": "Assess through research logs, backlog and decision logs, acceptance criteria and release records, with counterpart feedback from programme staff."},
                       "recommendedModes": ["WBL", "CAP", "COP"]},
    "sources": ["FS-007", "FS-044"],
    "adr": ["ADR-0030", "ADR-0015", "ADR-0025", "ADR-0004", "ADR-0003"],
    "note": (
        "S2 close-out B (A9 LM with FS; DC review pending; ADR-0030 §4 core residue). Role-defining core of R33 "
        "(permitting technology product owner); considered and not merged into DC-CAND-22 (ADR-0030 §3.1). Lifecycle "
        "emerging (ADR-0015): permitting data standards and federal permitting-technology plans create the need, and "
        "agencies rarely staff the role yet [J]; reviewBy set. Product-management and backlog software is L4. Needed by "
        "R33 (P3). Basis [J]: FS Phase 2 candidate and sources."),
    "levels": {
        "L2": [
            {"id": "seed:fs-c09-l2-a", "mode": "unaided", "methods": [WS, RA],
             "text": "Interviews practitioners about a step in a permitting or case-management workflow, recording the observed task, its problems and the evidence for each in the research log.",
             "served": ["seed:fs-c09-user-research"]},
            {"id": "seed:fs-c09-l2-b", "mode": "unaided", "methods": [WS, SEW],
             "text": "Writes acceptance criteria for a backlog item that state the user, the required behaviour and the test a release must pass.",
             "served": ["seed:fs-c09-acceptance-criteria"]},
        ],
        "L3": [
            {"id": "seed:fs-c09-l3-a", "mode": "unaided", "methods": [RA, BARS], "att": "ATT-AUT",
             "text": "Prioritizes the product backlog against programme outcomes and legal deadlines, recording the reason for each ranking change in the decision log.",
             "served": ["seed:fs-c09-prioritize-backlog"]},
            {"id": "seed:fs-c09-l3-b", "mode": "unaided", "methods": [RA, WS], "att": "ATT-KNO", "jv": True,
             "text": "Checks a release candidate against the applicable data-standard and records-retention requirements, holding the release until each nonconformance is fixed or accepted in writing.",
             "served": ["seed:fs-c09-release-check"]},
            {"id": "seed:fs-c09-l3-c", "mode": "assisted", "methods": [SEW, RA], "att": "ATT-AUG",
             "text": "Reviews AI-generated user stories or change summaries against user research and acceptance criteria, rejecting each item the evidence does not support.",
             "served": ["seed:fs-c09-review-ai-stories"]},
        ],
        "L4": [
            {"id": "seed:fs-c09-l4-a", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Sets a product roadmap across fiscal years that links each release to a programme outcome, a funding source and the staff training it needs.",
             "served": ["seed:fs-c09-roadmap"]},
            {"id": "seed:fs-c09-l4-b", "mode": "unaided", "methods": [RA, PR], "att": "ATT-SCO",
             "text": "Leads adoption of a release that changes staff workflows, tracking use and error measures and revising training or the product when targets are missed.",
             "served": ["seed:fs-c09-adoption"]},
        ],
    },
    "tasks": [
        {"id": "seed:fs-c09-user-research", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "partial", "modes": ["MODE-ENGAGE"],
         "text": "Interview practitioners and applicants about a permitting or case-management workflow, recording observed tasks, problems and supporting evidence",
         "regime": rg("M", "none", "system-specific", u="M")},
        {"id": "seed:fs-c09-acceptance-criteria", "wf": "WF-MANAGE", "field": "remote", "formation": "partial",
         "text": "Write acceptance criteria for each backlog item stating the user, the required behaviour and the release test",
         "regime": rg("M", "none", "system-specific", u="L")},
        {"id": "seed:fs-c09-prioritize-backlog", "wf": "WF-MANAGE", "field": "remote", "formation": "partial",
         "text": "Prioritize the product backlog against programme outcomes and legal deadlines, recording the reason for each ranking change",
         "regime": rg("M", "none", "system-specific", u="M")},
        {"id": "seed:fs-c09-release-check", "wf": "WF-MANAGE", "field": "remote", "formation": "partial",
         "text": "Check a release candidate against data-standard and records-retention requirements before approving its deployment",
         "regime": rg("M", "none", "system-specific", u="M"), "contrib": ["seed:SC-C02"]},
        {"id": "seed:fs-c09-review-ai-stories", "wf": "WF-MANAGE", "field": "remote", "formation": "yes",
         "text": "Review AI-generated user stories or change summaries against user research and acceptance criteria, rejecting unsupported items",
         "regime": rg("M", "none", "system-specific", u="M"), "contrib": ["seed:DC-CAND-13"],
         "note": "G-2 split: review of generated backlog items alongside the production task seed:fs-c09-acceptance-criteria."},
        {"id": "seed:fs-c09-roadmap", "wf": "WF-PLAN", "field": "remote", "formation": "partial",
         "text": "Prepare a multi-year product roadmap linking each release to a programme outcome, a funding source and a training need",
         "regime": rg("M", "none", "system-specific", u="L")},
        {"id": "seed:fs-c09-adoption", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "partial",
         "text": "Lead adoption of a release that changes staff workflows, tracking use and error measures and revising training when targets are missed",
         "regime": rg("M", "none", "system-specific", u="M")},
    ],
}

SPECS = [PARTICIPATORY, HORIZON, PRODUCT]
