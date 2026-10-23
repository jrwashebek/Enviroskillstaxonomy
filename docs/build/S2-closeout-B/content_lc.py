"""LC (A8, with IO review) content for S2 close-out builder B: v1 3.3.1 and v1 5.1.1 rewritten in place
(work-order rows 18-19; ADR-0030 §3.1 M2, M3). Content evidence label J; basis in editorialNote.
"""
LCIO = ["LC", "IO"]
LC = ["LC"]
T, WS, RA, SEW, SIM, PR, SJT, BARS, C360 = ("task-book-observation", "work-sample", "record-audit",
                                            "seeded-error-work-sample", "simulation-role-play", "portfolio-review",
                                            "situational-judgment-test", "structured-interview-bars", "counterpart-360")


def d(key, rel="rewritten"):
    return {"v1Key": key, "relation": rel}


SUPV = {
    "id": "seed:v1-3.3.1", "roles": LCIO, "row": "18",
    "label": "Supervise staff and volunteers in environmental work",
    "alt": ["Personnel management and supervision", "Remote and hybrid team leadership", "Volunteer programme management",
            "First-line supervision"],
    "definition": (
        "Directing, developing and evaluating the people who do environmental work, whether permanent, seasonal or term "
        "staff, volunteers, or staff working remotely, in the field or in hybrid arrangements: setting work plans and "
        "performance expectations, assigning and checking work, giving and documenting feedback, addressing performance "
        "and conduct problems within personnel rules and any labour agreement, and planning each person's development. "
        "Volunteer recruitment, scheduling, training and recognition are tasks of this competency in park, land-trust, "
        "wildlife and community-science settings. Excludes designing formation sequences (v1 7.2.2, TX-D), certifying "
        "task performance against position standards (IO-C01), leading a field crew's daily work (FC-C20) and designing "
        "merit-based recruitment and selection (v1 5.3.4-B)."),
    "statement": (
        "Sets work plans and performance expectations for staff and volunteers, assigns and checks their work, gives "
        "documented feedback, addresses performance and conduct problems within personnel rules and any labour "
        "agreement, gives remote, field and office staff equal information and assessment, and plans each person's "
        "development so that judgment-forming work is not skipped."),
    "reusability": "transversal",
    "learningDesign": {"assessmentContext": {"en": "Assess through supervisory work products (work plans, reviews, improvement plans, development plans) audited against personnel rules, structured interviews with behavioural anchors and counterpart feedback; the labour-agreement indicator is jurisdiction-dependent."},
                       "recommendedModes": ["CL", "MEN", "WBL", "CAP"], "prerequisites": ["seed:IO-C01"]},
    "sources": ["LC-034"],
    "derived": [d("v1:3.5.2", "merged-from"), d("v1:5.4.3", "merged-from")],
    "adr": ["ADR-0030", "ADR-0025", "ADR-0026", "ADR-0004", "ADR-0003", "ADR-0011"],
    "note": (
        "S2 close-out B (A8 LC with IO review; ADR-0030 §3.1 M3). Rewritten in place as the survivor for supervision of "
        "staff and volunteers: absorbs v1 3.5.2 (remote and hybrid teams) and v1 5.4.3 (volunteer programmes), which are "
        "workforce contexts of supervision; the volunteer tasks are kept with a park, land-trust and community-science "
        "context. Formation-of-others link to TX-D (v1 7.2.2) through the development-plan task (contributing) and an "
        "ATT-FOR indicator; labour-agreement indicator per the SL verdict. Crosswalk to OPM general competencies and the "
        "current executive core qualifications goes through X9, not parallel definitions (FH verdict). v1 Expert "
        "indicators naming influence or recognition are retired (B03). Needed at senior levels of every P1 role. "
        "Basis [J]."),
    "levels": {
        "L1": [
            {"id": "seed:lc-supv-l1-a", "mode": "unaided", "methods": [T, RA],
             "text": "Briefs seasonal staff or volunteers on the day's tasks, safety rules and quality standard before work starts, recording attendance and each person's assignment.",
             "served": ["seed:v1-5.4.3-T2"], "derived": [d("v1:3.3.1:foundational:I1"), d("v1:3.3.1:foundational:I3"), d("v1:5.4.3:foundational:I3")]},
            {"id": "seed:lc-supv-l1-b", "mode": "unaided", "methods": [SJT, T],
             "text": "Reports a performance or conduct concern about a worker to the supervisor on the day it is observed, describing the behaviour observed and its effect on the work.",
             "served": ["seed:v1-5.4.3-T2"], "derived": [d("v1:3.3.1:foundational:I6"), d("v1:3.3.1:foundational:I7")]},
        ],
        "L2": [
            {"id": "seed:lc-supv-l2-a", "mode": "unaided", "methods": [WS, RA], "att": "ATT-AUT",
             "text": "Writes an annual work plan for each direct report with measurable performance expectations tied to the unit's programme of work.",
             "served": ["seed:v1-3.3.1-T1"], "derived": [d("v1:3.3.1:intermediate:I1")]},
            {"id": "seed:lc-supv-l2-b", "mode": "unaided", "methods": [RA, BARS], "att": "ATT-AUT",
             "text": "Conducts a performance review that cites observed work products and events for each rating, recording the employee's response and the coaching agreed.",
             "served": ["seed:v1-3.3.1-T2"], "derived": [d("v1:3.3.1:intermediate:I2"), d("v1:3.3.1:intermediate:I3")]},
            {"id": "seed:lc-supv-l2-c", "mode": "unaided", "methods": [RA, C360], "att": "ATT-SCO",
             "text": "Schedules check-ins, assignments and recognition for remote, field and office staff on the same cycle, recording each contact so that no group is assessed on less information.",
             "served": ["seed:v1-3.5.2-T1", "seed:v1-3.5.2-T2"], "derived": [d("v1:3.5.2:intermediate:I3"), d("v1:3.5.2:intermediate:I6")]},
            {"id": "seed:lc-supv-l2-d", "mode": "unaided", "methods": [RA, SJT], "att": "ATT-GUI",
             "text": "Follows the labour agreement's notice, representation and grievance steps before changing a represented employee's assignment or addressing a performance problem, documenting each step.",
             "served": ["seed:lc-supv-labour-steps"]},
        ],
        "L3": [
            {"id": "seed:lc-supv-l3-a", "mode": "unaided", "methods": [WS, RA], "att": "ATT-CPX",
             "text": "Prepares a performance improvement plan that states the deficient standard, the support offered, the review dates and the consequence, within personnel rules and the labour agreement.",
             "served": ["seed:lc-supv-pip"], "derived": [d("v1:3.3.1:advanced:I7"), d("v1:3.3.1:advanced:I4")]},
            {"id": "seed:lc-supv-l3-b", "mode": "unaided", "methods": [PR, RA], "att": "ATT-FOR",
             "text": "Plans each staff member's development by pairing formation tasks with a mentor and an unaided-practice quota, reviewing progress against the plan at each performance review.",
             "served": ["seed:lc-supv-development-plan"], "derived": [d("v1:3.3.1:advanced:I2")]},
            {"id": "seed:lc-supv-l3-c", "mode": "unaided", "methods": [WS, PR], "att": "ATT-SCO",
             "text": "Designs a volunteer programme's recruitment, training, supervision and recognition steps for a site or project, with safety and liability controls for each volunteer role.",
             "served": ["seed:v1-5.4.3-T1", "seed:v1-5.4.3-T3"], "derived": [d("v1:5.4.3:advanced:I1"), d("v1:5.4.3:advanced:I7")]},
            {"id": "seed:lc-supv-l3-d", "mode": "assisted", "methods": [SEW, RA], "att": "ATT-AUG",
             "text": "Checks an AI-drafted performance narrative against observed work records, deleting each statement the records do not support before the review is signed.",
             "served": ["seed:lc-supv-review-drafted-appraisal"]},
        ],
        "L4": [
            {"id": "seed:lc-supv-l4-a", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Sets a unit's supervision standards for work plans, reviews, telework and volunteer roles, writing the guidance that new supervisors are trained and assessed against.",
             "served": ["seed:v1-3.5.2-T3", "seed:v1-3.3.1-T1"], "derived": [d("v1:3.3.1:advanced:I9"), d("v1:3.5.2:advanced:I11")]},
            {"id": "seed:lc-supv-l4-b", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Prepares a succession plan for critical positions that names the knowledge and formation each needs, the people in development and the date each will be ready.",
             "served": ["seed:lc-supv-succession"], "derived": [d("v1:3.3.1:advanced:I8")]},
        ],
    },
    "tasks": [
        {"id": "seed:v1-3.3.1-T1", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "partial",
         "text": "Write annual work plans for field and office staff that state measurable performance expectations tied to the unit's programme of work",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "seasonal", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-3.3.1-T2", "wf": "WF-MANAGE", "field": "on-site-preferred", "formation": "partial",
         "text": "Conduct a performance review that cites observed work products for each rating and sets coaching actions for the next period",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "seasonal", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:v1-3.3.1-T3", "wf": "WF-MANAGE", "field": "on-site-preferred", "formation": "partial",
         "text": "Onboard a new staff member with a written first-month plan covering safety, duties, systems access and scheduled supervisor check-ins",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"},
         "note": "Hiring and selection design belongs to v1 5.3.4-B and FH-C13; this task keeps onboarding."},
        {"id": "seed:v1-3.5.2-T1", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "no",
         "text": "Hold regular team meetings that give remote, field and office staff the same information and a turn to raise issues",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-3.5.2-T2", "wf": "WF-MANAGE", "field": "remote", "formation": "no",
         "text": "Review assignments, recognition and promotion recommendations for differences between remote, field and office staff, correcting differences the work does not explain",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "seasonal", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-3.5.2-T3", "wf": "WF-MANAGE", "field": "remote", "formation": "no",
         "text": "Set team norms for response times, meeting load and after-hours contact so that distributed staff can protect field and focus time",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-5.4.3-T1", "wf": "WF-MANAGE", "field": "on-site-preferred", "formation": "partial", "rel": ["public"],
         "text": "Recruit volunteers for monitoring, trail or education work, matching each volunteer to a role whose skill and safety requirements they meet",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "seasonal", "placeBoundness": "site-specific", "credentialGate": "none", "currencyDecay": "L"},
         "note": "Volunteer programme context (ADR-0030 §3.1 M3): parks, land trusts, wildlife and community-science projects."},
        {"id": "seed:v1-5.4.3-T2", "wf": "WF-MANAGE", "field": "on-site-required", "formation": "partial", "rel": ["public"],
         "text": "Supervise volunteers during an event or a day of field work, checking work quality and compliance with safety rules at set intervals",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "seasonal", "placeBoundness": "site-specific", "credentialGate": "none", "currencyDecay": "M"},
         "contrib": ["seed:v1-4.4.1-B"]},
        {"id": "seed:v1-5.4.3-T3", "wf": "WF-MANAGE", "field": "remote", "formation": "no",
         "text": "Maintain volunteer records of hours, training and assignments for reporting and recognition, protecting each volunteer's personal information",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:lc-supv-labour-steps", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "partial",
         "text": "Apply the labour agreement's notice and representation steps before changing assignments, schedules or discipline for represented staff",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "system-specific", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:lc-supv-pip", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "partial",
         "text": "Prepare a performance improvement plan that states the deficient standard, the support offered, review dates and consequences",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "multi-year-or-rare-event", "placeBoundness": "system-specific", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:lc-supv-development-plan", "wf": "WF-LEARN", "field": "remote-capable", "formation": "yes",
         "text": "Plan each staff member's development by pairing formation tasks with a mentor and an unaided-practice quota before AI-assisted shortcuts",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "seasonal", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"},
         "contrib": ["seed:v1-7.2.2"], "note": "Formation-of-others link to TX-D (v1 7.2.2), contributing."},
        {"id": "seed:lc-supv-review-drafted-appraisal", "wf": "WF-MANAGE", "field": "remote", "formation": "yes",
         "text": "Review an AI-drafted performance appraisal narrative against the supervisor's own observations, removing any statement the record does not support",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "seasonal", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"},
         "note": "G-2 split: review of a drafted appraisal alongside the production task seed:v1-3.3.1-T2."},
        {"id": "seed:lc-supv-succession", "wf": "WF-MANAGE", "field": "remote", "formation": "partial",
         "text": "Prepare a succession plan for critical positions naming the knowledge required, the people in development and readiness dates",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "multi-year-or-rare-event", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"},
         "contrib": ["seed:FH-C07"]},
    ],
}

COMM = {
    "id": "seed:v1-5.1.1", "roles": LC, "row": "19",
    "label": "Communicate technical environmental information in writing and speech",
    "alt": ["Written communication for diverse audiences", "Public speaking and presentation", "Science communication and storytelling",
            "Public information and media relations", "Plain-language writing", "Digital outreach"],
    "definition": (
        "Turning technical environmental information (findings, data, plans, rules and decisions) into accurate written, "
        "spoken and visual products for specialist and public audiences: plain-language summaries, reports, fact sheets, "
        "presentations, public-meeting remarks, news releases, media interviews, testimony and digital posts. Covers "
        "audience analysis, accuracy checks with subject experts, accessibility and translation, clearance, and answering "
        "public and media questions. Excludes risk and crisis messaging under uncertainty (DB-C29, TX-E), briefing "
        "decision-makers for authoritative decisions (SC-C18), designing public engagement (SC-C06) and interpretation "
        "(v1 5.1.3)."),
    "statement": (
        "Analyzes the audience and purpose, then writes, presents and adapts technical environmental information into "
        "accurate, accessible products for specialist and public audiences, checks them with subject experts before "
        "release, and answers public and media questions without overstating certainty, so that readers and listeners "
        "can use the information correctly."),
    "reusability": "transversal",
    "learningDesign": {"assessmentContext": {"en": "Assess through work samples (summaries, fact sheets, releases) scored against a plain-language and accuracy rubric, observed presentations and simulated media interviews."},
                       "recommendedModes": ["WS", "CL", "SIM", "MEN"]},
    "sources": ["LC-034"],
    "derived": [d("v1:5.1.2", "merged-from"), d("v1:5.1.5", "merged-from"), d("v1:5.5.4", "merged-from"), d("v1:5.1.4", "merged-from")],
    "adr": ["ADR-0030", "ADR-0004", "ADR-0003", "ADR-0011"],
    "note": (
        "S2 close-out B (A8 LC; ADR-0030 §3.1 M2). Rewritten in place as the survivor for communicating technical "
        "environmental information in writing and speech: absorbs v1 5.1.2 (presentation), 5.1.5 (science communication), "
        "5.5.4 (public information and media relations) and, through it, 5.1.4 (digital outreach; platforms are L4). "
        "Risk and crisis messaging stays in DB-C29 (TX-E); generic public relations is referenced from O*NET and ESCO "
        "(G-8); crosswalk to OPM Writing and Oral Communication goes through X9 (FH verdict). v1 D5 indicators restored "
        "from source text were rewritten; Expert indicators naming recognition or publication are retired (B03, B04). "
        "Needed by R12 and R13 (P1). Basis [J]."),
    "levels": {
        "L1": [
            {"id": "seed:lc-comm-l1-a", "mode": "unaided", "methods": [WS, RA],
             "text": "Writes a plain-language summary of a technical document that a subject expert confirms is accurate and that meets the programme's readability target.",
             "served": ["seed:v1-5.1.1-T2", "seed:v1-5.1.1-T1"], "derived": [d("v1:5.1.1:foundational:I1")]},
            {"id": "seed:lc-comm-l1-b", "mode": "unaided", "methods": [WS, RA],
             "text": "Revises a draft after review, resolving each reviewer comment or recording why it was declined.",
             "served": ["seed:v1-5.1.1-T1"], "derived": [d("v1:5.1.1:foundational:I3")]},
            {"id": "seed:lc-comm-l1-c", "mode": "unaided", "methods": [SEW, WS],
             "text": "Flags each technical term in a draft that the intended audience is unlikely to know, replacing or defining it before release.",
             "served": ["seed:v1-5.1.1-T3"], "derived": [d("v1:5.1.1:foundational:I4")]},
        ],
        "L2": [
            {"id": "seed:lc-comm-l2-a", "mode": "unaided", "methods": [WS, RA], "att": "ATT-AUT",
             "text": "Produces a fact sheet or report section that passes review without substantive revision, with every figure traced to its source.",
             "served": ["seed:v1-5.1.1-T1", "seed:v1-5.1.5-T1"], "derived": [d("v1:5.1.1:intermediate:I1")]},
            {"id": "seed:lc-comm-l2-b", "mode": "unaided", "methods": [T, SIM], "att": "ATT-CPX",
             "text": "Presents technical findings at a public meeting, answering questions within the evidence and referring each question it cannot answer to a named follow-up.",
             "served": ["seed:v1-5.1.2-T1", "seed:v1-5.1.2-T2"], "derived": [d("v1:5.1.2:intermediate:I3"), d("v1:5.1.2:intermediate:I2")]},
            {"id": "seed:lc-comm-l2-c", "mode": "unaided", "methods": [WS, RA], "att": "ATT-KNO",
             "text": "Formats a public document to the programme's accessibility standard for headings, alternative text, contrast and reading level before release.",
             "served": ["seed:v1-5.1.1-T3"], "derived": [d("v1:5.1.1:intermediate:I3")]},
            {"id": "seed:lc-comm-l2-d", "mode": "assisted", "methods": [SEW, WS], "att": "ATT-AUG",
             "text": "Checks an AI-drafted or machine-translated public document against its source, correcting each error of fact, emphasis or tone before release.",
             "served": ["seed:lc-comm-verify-drafted"]},
        ],
        "L3": [
            {"id": "seed:lc-comm-l3-a", "mode": "unaided", "methods": [WS, SIM], "att": "ATT-CPX",
             "text": "Explains a contested technical topic to a mixed audience in writing or speech, presenting the evidence and its limits so that reviewers from opposing positions find no misstatement.",
             "served": ["seed:v1-5.1.1-T2", "seed:v1-5.1.2-T1"], "derived": [d("v1:5.1.1:advanced:I1"), d("v1:5.1.1:advanced:I5")]},
            {"id": "seed:lc-comm-l3-b", "mode": "unaided", "methods": [SIM, RA], "att": "ATT-SCO",
             "text": "Answers a journalist's questions on a technical finding within the cleared facts, correcting any misreported figure in writing after publication.",
             "served": ["seed:v1-5.5.4-T1", "seed:v1-5.5.4-T3"], "derived": [d("v1:5.5.4:advanced:I3")]},
            {"id": "seed:lc-comm-l3-c", "mode": "unaided", "methods": [WS, PR], "att": "ATT-FOR",
             "text": "Edits others' technical drafts against the style guide and plain-language standard, returning each draft with marked corrections and the reason for each.",
             "served": ["seed:v1-5.1.5-T3"], "derived": [d("v1:5.1.1:advanced:I4"), d("v1:5.1.5:advanced:I3")]},
        ],
        "L4": [
            {"id": "seed:lc-comm-l4-a", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Sets a programme's communication standards, writing the style guide and the review and clearance steps that staff products pass before public release.",
             "served": ["seed:lc-comm-style-guide"], "derived": [d("v1:5.1.1:advanced:I2")]},
            {"id": "seed:lc-comm-l4-b", "mode": "unaided", "methods": [WS, SIM], "att": "ATT-CPX",
             "text": "Prepares testimony for a legislative or high-profile public hearing that states the technical findings, their uncertainty and the programme's position separately.",
             "served": ["seed:lc-comm-testimony"], "derived": [d("v1:5.1.1:expert:I2"), d("v1:5.1.2:expert:I3")]},
            {"id": "seed:lc-comm-l4-c", "mode": "unaided", "methods": [PR, WS], "att": "ATT-SCO",
             "text": "Plans communication for a programme's release of a contested decision or report, assigning messages, channels and spokespeople and keeping a question log that is reviewed after each event.",
             "served": ["seed:v1-5.5.4-T2", "seed:v1-5.1.4-T3"], "derived": [d("v1:5.5.4:expert:I1")]},
        ],
    },
    "tasks": [
        {"id": "seed:v1-5.1.1-T1", "wf": "WF-MANAGE", "field": "remote", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Draft a fact sheet that explains land use rules or programme requirements in plain language for a public audience",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-5.1.1-T2", "wf": "WF-ASSESS", "field": "remote", "formation": "yes", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Translate a scientific report into a plain-language summary for the public, confirming accuracy with the report's authors before release",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:v1-5.1.1-T3", "wf": "WF-MANAGE", "field": "remote", "formation": "partial", "modes": ["MODE-ENGAGE"],
         "text": "Tailor one technical message for policymakers, young people and local residents, adjusting content, format and reading level for each",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-5.1.2-T1", "wf": "WF-MANAGE", "field": "on-site-preferred", "formation": "yes", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Present technical findings at a community meeting or public hearing, answering questions within the evidence",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:v1-5.1.2-T2", "wf": "WF-ASSESS", "field": "on-site-preferred", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["stakeholder"],
         "text": "Represent the programme's findings at a conference or stakeholder forum, stating the evidence and its limits",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-5.1.2-T3", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "partial", "modes": ["MODE-ENGAGE"],
         "text": "Rehearse a public presentation with a non-specialist listener, revising the terms and visuals the listener could not follow",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-5.1.5-T1", "wf": "WF-ASSESS", "field": "remote", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Write an article or multimedia script that explains a field project's methods and findings for a general audience",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-5.1.5-T2", "wf": "WF-ASSESS", "field": "remote", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Design an infographic or chart that explains a data trend to the public, stating the data source and its uncertainty",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"},
         "contrib": ["seed:v1-2.1.5"]},
        {"id": "seed:v1-5.1.5-T3", "wf": "WF-LEARN", "field": "remote-capable", "formation": "partial",
         "text": "Coach technical staff to explain their work to public audiences, giving feedback on accuracy, plain language and delivery",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-5.5.4-T1", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Represent the agency in a media interview on a technical matter, keeping every statement within the cleared facts",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:v1-5.5.4-T2", "wf": "WF-MANAGE", "field": "remote", "formation": "partial", "modes": ["MODE-ENGAGE"],
         "text": "Develop key messages and supporting facts for a programme initiative or public concern, clearing each fact with a subject expert",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-5.5.4-T3", "wf": "WF-MANAGE", "field": "remote", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Respond to public or media inquiries about a programme decision with cleared information within the programme's response deadline",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
        {"id": "seed:v1-5.1.4-T1", "wf": "WF-MANAGE", "field": "remote", "formation": "no", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Write posts for the programme's public digital channels that explain a technical topic accurately within each channel's length limits",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "H"},
         "note": "Channel platforms are L4 tools; the durable task is accurate short-form explanation."},
        {"id": "seed:v1-5.1.4-T2", "wf": "WF-MANAGE", "field": "remote", "formation": "no", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Respond to public comments and questions on the programme's digital channels following its moderation and records policy",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:v1-5.1.4-T3", "wf": "WF-LEARN", "field": "remote", "formation": "no",
         "text": "Evaluate digital outreach with reach and comprehension measures, revising the content plan when measures show the audience is not reached",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:lc-comm-verify-drafted", "wf": "WF-MANAGE", "field": "remote", "formation": "yes", "modes": ["MODE-ENGAGE"],
         "text": "Verify an AI-drafted or machine-translated public document against its source, correcting each error of fact, emphasis or tone before release",
         "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "M"},
         "contrib": ["seed:DC-CAND-13"], "note": "G-2 split: verification of drafted or translated text alongside the production tasks."},
        {"id": "seed:lc-comm-testimony", "wf": "WF-MANAGE", "field": "remote-capable", "formation": "partial", "modes": ["MODE-ENGAGE"], "rel": ["public"],
         "text": "Prepare written testimony for a legislative or public hearing that separates technical findings, their uncertainty and the programme's position",
         "regime": {"mentorshipDependence": "H", "cycleDependence": "multi-year-or-rare-event", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "M"}},
        {"id": "seed:lc-comm-style-guide", "wf": "WF-MANAGE", "field": "remote", "formation": "no",
         "text": "Write the programme's style guide and clearance steps for public documents, including its plain-language and accessibility rules",
         "regime": {"mentorshipDependence": "L", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "none", "currencyDecay": "L"}},
    ],
}

SPECS = [SUPV, COMM]
