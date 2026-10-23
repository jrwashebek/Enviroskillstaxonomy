"""WP-07 content specification: TX-C, TX-D, TX-E and TX-F competencies, their indicators (the CLOs inside L1),
tasks, enactments and knowledge statements.

Author: emstagent:lc-agent@wp-07 (LC lead; IO co-owner reviews). Every value here is agent-drafted [J]; nothing is
SME agreement, Delphi retention or job-analysis confirmation. build_wp07.py turns this file into records under
data/v2/core/. Edit here and re-run the builder; do not hand-edit the generated records while this file is the source
(the worklog records when that changes at integration).

Indicator tuple: (level, letter, statement, augmentationMode, assessmentMethods, servedTaskKeys, distinguishingAttribute,
                  extras)  extras keys: jv, safety, v1 (v1 indicator keys rewritten), use, obs4, evidence, plan
Task dict keys: key, text, wf, field, form, supports, modes, rr, existing, v1 (v1 task key), merged (extra v1 task keys),
                note, gates
"""

# ------------------------------------------------------------------------------------------------ shared vocab
UNAIDED, ASSISTED, SUPERVISORY = "unaided", "assisted", "supervisory"

WS, SEW, BARS, SJT, SIM, TBO, REC, MOOT, POR, KT, BRM = (
    "work-sample", "seeded-error-work-sample", "structured-interview-bars", "situational-judgment-test",
    "simulation-role-play", "task-book-observation", "record-audit", "moot-defense", "portfolio-review",
    "knowledge-test", "blind-re-measurement")


def rr(m=None, c=None, p=None, g=None, d=None):
    out = {}
    if m: out["mentorshipDependence"] = m
    if c: out["cycleDependence"] = c
    if p: out["placeBoundness"] = p
    if g: out["credentialGate"] = g
    if d: out["currencyDecay"] = d
    return out


COMPETENCIES = []

# ================================================================================================ TX-C safety culture
TXC = "seed:v1-4.4.1-B"
COMPETENCIES.append(dict(
    id=TXC, slug="txc-safety", new=True, cluster="TX-C",
    prefLabel="Apply safety practices and stop-work authority across field, facility and incident settings",
    altLabel=["Safety culture", "Stop-work and turn-down authority", "Learning from incidents"],
    definition=("Applies an organization's safety-culture practices in everyday environmental work: recognizing and reporting "
                "hazards and near misses, exercising and honouring stop-work and turn-down authority, briefing and debriefing "
                "safety, and learning from incidents without blame, in field, facility and incident settings. Excludes the "
                "technical assessment and control of hazards for specific field operations (field risk management, a Field "
                "Craft practice competency) and the administration of occupational-safety programmes."),
    statement=("Recognizes, reports and acts on hazards and near misses, exercises and honours stop-work authority, runs "
               "safety briefings and after-action reviews, and builds a reporting culture in which colleagues raise concerns "
               "and learn from incidents, across field, facility and incident settings."),
    span=("L1", "L4"),
    learningDesign=dict(assessmentContext="field | incident | facility (observed in context; simulation for rare events)",
                        recommendedModes=["WBL", "MEN", "SIM", "CL"], typicalHoursPerLevelStep=24),
    derivedFrom=[{"v1Key": "v1:4.4.1", "relation": "split-from",
                  "note": "Safety-culture part of v1 4.4.1; field risk management is seed:v1-4.4.1-A (FC, WP-03); programme administration is referenced from O*NET/ESCO (v1_disposition.csv)."}],
    editorialNote=("TX-C successor split from v1 4.4.1 (ADR-0025 §1; v1_disposition.csv). Required of field and facility "
                   "roles (ADR-0025). Basis for the text: v1 4.4.1 indicators (foundational I5, I8; intermediate I2, I6, I7; "
                   "advanced I8) rewritten to IO's sentence pattern, and incident-qualification practice that codes the "
                   "setting a task must be evaluated in [E: LC-104]. Module enactments (forest: wildland fire turn-down; "
                   "water: plant and confined-space work; hazards: incident response) are handed to WP-06. v1 task "
                   "4.4.1-T3 (incident investigation) is re-pointed here; T1 and T2 stay with seed:v1-4.4.1-A."),
    sources=["LC-104"],
    indicators=[
        ("L1", "a", "Halts own task when a hazard not covered by the pre-work briefing appears, and reports it to the supervisor before work resumes.",
         UNAIDED, [TBO, SIM], ["seed:lc-txc-exercise-stop-work"], None, dict(safety=True, v1=["v1:4.4.1:foundational:I8"])),
        ("L1", "b", "Reports each near miss or unsafe condition seen on an assignment through the unit's reporting channel within the same shift, describing conditions, actions and outcome.",
         UNAIDED, [REC, TBO], ["seed:lc-txc-report-near-miss"], None, dict(v1=["v1:4.4.1:foundational:I5"])),
        ("L1", "c", "Identifies the escape routes and assembly points for the assigned work area before work begins, matching those named in the pre-work briefing.",
         UNAIDED, [TBO, KT], ["seed:lc-txc-deliver-briefing"], None, dict(safety=True)),
        ("L2", "a", "Delivers a pre-work safety briefing for a routine assignment that covers the hazards, controls, communications and stop-work procedure named in the unit's briefing standard.",
         UNAIDED, [TBO, WS], ["seed:lc-txc-deliver-briefing"], "ATT-AUT", dict(v1=["v1:4.4.1:intermediate:I2"])),
        ("L2", "b", "Exercises stop-work authority when conditions exceed the assignment's stated limits, and records the condition, decision and notification in the unit log.",
         UNAIDED, [TBO, SIM, REC], ["seed:lc-txc-exercise-stop-work"], "ATT-GUI", dict(safety=True)),
        ("L2", "c", "Checks automated hazard alerts such as weather, air-quality or gas-detector alarms against on-site observation before relying on them, and reports any disagreement to the lead.",
         ASSISTED, [SIM, TBO], ["seed:lc-txc-review-generated-briefing"], "ATT-AUG", dict(safety=True)),
        ("L3", "a", "Turns down or halts an assignment whose risk exceeds the approved plan despite schedule or production pressure, documenting the basis and the alternative offered.",
         UNAIDED, [SIM, BARS, REC], ["seed:lc-txc-exercise-stop-work"], "ATT-CPX", dict(safety=True)),
        ("L3", "b", "Conducts a no-blame review of a near miss or incident with the people involved, recording contributing conditions and corrective actions with owners and dates.",
         UNAIDED, [WS, REC], ["seed:v1-4.4.1-T3"], "ATT-SCO", dict(v1=["v1:4.4.1:intermediate:I6", "v1:4.4.1:intermediate:I7"])),
        ("L3", "c", "Coaches crew members to raise safety concerns by answering each raised concern within the shift and recording the response in the unit log.",
         UNAIDED, [TBO, REC], ["seed:lc-txc-report-near-miss"], "ATT-FOR", dict(v1=["v1:4.4.1:advanced:I8"])),
        ("L4", "a", "Designs a unit's learning-from-incidents process that specifies reporting channels, review triggers, no-blame safeguards and how lessons reach pre-work briefings.",
         UNAIDED, [WS, POR], ["seed:lc-txc-design-learning-process"], "ATT-GUI", dict()),
        ("L4", "b", "Audits a sample of the unit's briefings, stop-work records and incident reviews against its safety standard, and reports gaps with corrective actions to management.",
         UNAIDED, [REC, WS], ["seed:lc-txc-design-learning-process", "seed:v1-4.4.1-T3"], "ATT-SCO", dict()),
        ("L4", "c", "Sets the unit's stop-work and turn-down protocol, stating who may stop work, how stops are reviewed and how people who stop work are protected under applicable requirements.",
         UNAIDED, [WS, POR], ["seed:lc-txc-design-learning-process"], "ATT-GUI", dict(jv=True, safety=True)),
    ],
    tasks=[
        dict(key="seed:lc-txc-deliver-briefing", text="Deliver a pre-work safety briefing that covers site hazards, controls, communications and the stop-work procedure for the assigned work area",
             wf="WF-OPERATE", field="on-site-required", form="yes", supports=[(TXC, "primary")], rr=rr("M", "none", "general", None, "M")),
        dict(key="seed:lc-txc-exercise-stop-work", text="Exercise stop-work authority when field, facility or incident conditions exceed the stated safety limits of the assignment",
             wf="WF-OPERATE", field="on-site-required", form="yes", supports=[(TXC, "primary")], rr=rr("H", "multi-year-or-rare-event", "general", None, "M")),
        dict(key="seed:lc-txc-report-near-miss", text="Report near misses and unsafe conditions through the unit's reporting channel during the shift in which they occur",
             wf="WF-OPERATE", field="on-site-preferred", form="partial", supports=[(TXC, "primary")], rr=rr("L", "none", "general", None, "L")),
        dict(key="seed:v1-4.4.1-T3", existing=True, v1="v1:4.4.1:T3",
             text="Conduct a no-blame review of a near miss or incident with the people involved to identify contributing conditions and corrective actions",
             wf="WF-LEARN", field="on-site-preferred", form="partial", supports=[(TXC, "primary")], rr=rr("M", "multi-year-or-rare-event", "general", None, "M"),
             note="v1 4.4.1-T3 (incident investigation) re-pointed from the superseded v1 4.4.1 to its TX-C successor and rewritten (WP-07)."),
        dict(key="seed:lc-txc-review-generated-briefing", text="Review a template- or AI-generated hazard briefing against conditions observed on site before delivering it to the crew",
             wf="WF-OPERATE", field="on-site-required", form="yes", supports=[(TXC, "primary")], rr=rr("M", "seasonal", "ecosystem-type", None, "M"),
             note="Review half of the G-2 split: drafting the briefing is compressible; checking it against the site is not."),
        dict(key="seed:lc-txc-design-learning-process", text="Design a unit learning-from-incidents process that links reporting channels, review triggers and pre-work briefing content",
             wf="WF-MANAGE", field="remote-capable", form="partial", supports=[(TXC, "primary")], rr=rr("L", "none", "general", None, "L")),
    ],
    knowledge=[
        dict(key="seed:lc-ks-txc-stop-work", lowest="L1", methods=[KT],
             text="Stop-work authority lets any worker halt a task they judge unsafe; the task resumes only after the hazard is assessed and the plan revised, and the person who stopped it is not penalized."),
        dict(key="seed:lc-ks-txc-just-culture", lowest="L2", methods=[KT],
             text="A no-blame incident review separates system and condition causes from individual error and sanctions only reckless or wilful acts, so that people keep reporting near misses."),
    ],
    enactments=[],
))

# ================================================================================================ TX-D formation design (v1 7.2.2)
TXD1 = "seed:v1-7.2.2"
COMPETENCIES.append(dict(
    id=TXD1, slug="txd-formation", new=False, cluster="TX-D",
    prefLabel="Design developmental work experiences that preserve the formation of professional judgment",
    altLabel=["Designing workflows for tacit knowledge formation in AI-augmented practice", "Design AI-augmented apprenticeships",
              "Design performance-based qualification for field and technical work", "Design structured developmental field experiences"],
    definition=("Designs the sequence of supervised work, unaided practice, rotations, task-book assignments and qualification "
                "steps through which entry and developing staff form the judgment their role requires, including where AI or "
                "automation now performs tasks that once built it. Covers formation analysis of workflows, staged-exposure and "
                "by-hand rules, performance-based qualification design and evaluation of whether formation works. Excludes "
                "observing and certifying one person's performance (a separate TX-D competency) and leading a field crew."),
    statement=("Analyzes which tasks in a workflow form judgment, then designs developmental experiences (supervised repetitions, "
               "unaided by-hand quotas, rotations, task books and qualification steps) so that entry and developing staff still "
               "form that judgment when AI or automation performs those tasks, and evaluates whether the design works."),
    span=("L2", "L5"),
    learningDesign=dict(assessmentContext="desk-data | stakeholder (design products reviewed by a peer supervisor; field context for field roles)",
                        recommendedModes=["CL", "WS", "COP", "CAP"], typicalHoursPerLevelStep=16,
                        prerequisites=["seed:IO-C01"]),
    derivedFrom=None,  # existing seed: relation becomes rewritten
    editorialNote=("Rewritten v1 7.2.2 (TX-D formation survivor; ADR-0025). Absorbs FH-C06 (developmental field experiences), "
                   "FS-C13 (AI-augmented apprenticeships) and LC-C-01 (performance-based qualification design), per "
                   "candidate_disposition.csv. v1 levels mapped by IO's attribute test: v1 Foundational content (explaining "
                   "formation loss) becomes knowledge statements, not an L1 level; v1 Expert 'Publishes/Recognized' indicators "
                   "are retired (B03, B04). L5 is drafted because the ATT-FOR L5 descriptor ('sets formation pathways and "
                   "protects entry cohorts organization-wide') is this competency's core; it stays provisional until SME panels "
                   "confirm strategic demand (ADR-0004 §4). Required for supervisors and training officers (v1_disposition.csv)."),
    sources=["LC-034", "LC-104"],
    indicators=[
        ("L2", "a", "Maps the tasks of one entry role in the unit, showing which build judgment and which an AI tool or automation now performs, with an observed example for each.",
         UNAIDED, [WS], ["seed:v1-7.2.2-T1"], None, dict(v1=["v1:7.2.2:intermediate:I1"])),
        ("L2", "b", "Drafts a staged-exposure plan for one entry role that states which tasks the trainee performs unaided, how many times, and the check that releases work done with AI assistance.",
         UNAIDED, [WS], ["seed:v1-7.2.2-T2", "seed:lc-txd-set-by-hand-quota"], None, dict(v1=["v1:7.2.2:intermediate:I3"])),
        ("L2", "c", "Explains to a production-focused supervisor which formation step a proposed shortcut using AI would remove, using the unit's own task examples and a proposed alternative.",
         UNAIDED, [SIM, WS], ["seed:lc-txd-advise-ai-adoption"], None, dict(v1=["v1:7.2.2:intermediate:I4"])),
        ("L3", "a", "Designs a developmental sequence for an entry cohort that combines supervised repetitions, by-hand quotas, rotations and a qualification step, naming a mentor for each stage.",
         UNAIDED, [WS, POR], ["seed:v1-7.2.2-T2", "seed:lc-txd-plan-field-rotations"], "ATT-SCO", dict(v1=["v1:7.2.2:intermediate:I2"])),
        ("L3", "b", "Evaluates whether an AI-augmented workflow still produces staff who catch its errors, by giving recent entrants unaided seeded-error checks and comparing results with the role standard.",
         ASSISTED, [WS, REC], ["seed:v1-7.2.2-T3"], "ATT-AUG", dict(v1=["v1:7.2.2:advanced:I3"])),
        ("L3", "c", "Designs a task-book style qualification record for a field or technical position that lists each observable task, its required evaluation context and its sign-off standard.",
         UNAIDED, [WS], ["seed:lc-txd-design-task-book"], "ATT-CPX", dict()),
        ("L4", "a", "Sets the by-hand quota and release criterion for each compressed formation task in a programme, based on unaided-performance data from recent cohorts.",
         UNAIDED, [WS, REC], ["seed:lc-txd-set-by-hand-quota"], "ATT-GUI", dict()),
        ("L4", "b", "Advises programme leadership on the sequence for adopting an AI tool, stating which entry formation tasks it removes and the alternative formation route needed before deployment.",
         UNAIDED, [WS, BARS], ["seed:lc-txd-advise-ai-adoption"], "ATT-SCO", dict(v1=["v1:7.2.2:advanced:I2"])),
        ("L4", "c", "Designs the evaluator-calibration process for a programme's qualification system, specifying calibration cases, agreement checks and the action taken when evaluators diverge.",
         UNAIDED, [WS, POR], ["seed:lc-txd-design-task-book"], "ATT-FOR", dict()),
        ("L5", "a", "Establishes an organization-wide formation policy that protects entry-cohort intake and unaided-practice requirements when AI tools are adopted, recorded in a dated decision record.",
         UNAIDED, [POR, BARS], ["seed:lc-txd-advise-ai-adoption"], "ATT-SCO", dict(use="describe")),
        ("L5", "b", "Allocates mentor and evaluator capacity across programmes against projected formation needs, documenting the trade-off with production targets in the workforce plan.",
         UNAIDED, [POR, BARS], ["seed:lc-txd-plan-field-rotations"], "ATT-AUT", dict(use="describe")),
    ],
    tasks=[
        dict(key="seed:v1-7.2.2-T1", existing=True, v1="v1:7.2.2:T1",
             text="Analyze a workflow to identify which entry-level tasks form judgment and which of them AI tools or automation now perform",
             wf="WF-LEARN", field="remote-capable", form="yes", supports=[(TXD1, "primary")], rr=rr("M", "none", "general", None, "L")),
        dict(key="seed:v1-7.2.2-T2", existing=True, v1="v1:7.2.2:T2",
             text="Design a staged-exposure sequence for an entry role that sets the unaided repetitions required before AI-assisted performance is credited",
             wf="WF-LEARN", field="remote-capable", form="yes", supports=[(TXD1, "primary")], rr=rr("M", "none", "general", None, "L")),
        dict(key="seed:v1-7.2.2-T3", existing=True, v1="v1:7.2.2:T3",
             text="Evaluate whether a redesigned workflow still forms judgment by checking recent entrants' unaided performance against the role standard",
             wf="WF-LEARN", field="remote-capable", form="yes", supports=[(TXD1, "primary")], rr=rr("M", "none", "general", None, "L")),
        dict(key="seed:lc-txd-design-task-book", text="Design a task-book style qualification record that lists observable tasks, required evaluation context and sign-off standard for a position",
             wf="WF-LEARN", field="remote-capable", form="partial", supports=[(TXD1, "primary")], rr=rr("M", "none", "general", None, "L"),
             note="From LC-C-01 (performance-based qualification design), merged into v1 7.2.2."),
        dict(key="seed:lc-txd-set-by-hand-quota", text="Specify a by-hand quota of unaided work products for each compressed formation task before trainees move to review-and-certify work",
             wf="WF-LEARN", field="remote-capable", form="yes", supports=[(TXD1, "primary")], rr=rr("M", "none", "general", None, "L"),
             note="From FS-C13 and ADR-0026 R7 (by-hand quota)."),
        dict(key="seed:lc-txd-plan-field-rotations", text="Plan rotations and mentored field assignments that give entry staff graduated exposure to the conditions their role must handle",
             wf="WF-LEARN", field="remote-capable", form="yes", supports=[(TXD1, "primary")], rr=rr("M", "seasonal", "ecosystem-type", None, "L"),
             note="From FH-C06 (structured developmental field experiences), merged into v1 7.2.2."),
        dict(key="seed:lc-txd-advise-ai-adoption", text="Advise leadership on the formation consequences of adopting an AI tool before deployment, naming the alternative formation route required",
             wf="WF-LEARN", field="remote", form="partial", supports=[(TXD1, "primary")], rr=rr("L", "none", "general", None, "M")),
        dict(key="seed:v1-3.5.4-T3", existing=True, v1="v1:3.5.4:T3",
             text="Design development pathways that credit prior experience from non-traditional and cross-sector careers toward an entry role",
             wf="WF-LEARN", field="remote", form="no", supports=[(TXD1, "primary")], rr=rr("L", "none", "general", None, "L"),
             note="v1 3.5.4 (merged into FH-C07) T3 is formation-pathway design, so it is re-pointed to the TX-D formation survivor (WP-07)."),
    ],
    knowledge=[
        dict(key="seed:lc-ks-txd-formation-task", lowest="L2", methods=[KT],
             text="A formation task is an entry-level task with high or medium tacit content through which practitioners historically built the judgment needed to check later work, including AI output."),
        dict(key="seed:lc-ks-txd-by-hand-quota", lowest="L2", methods=[KT],
             text="A by-hand quota is a set number of unaided work products a learner completes before review-and-certify credit, sized so the learner can recognize the tool's characteristic errors."),
        dict(key="seed:lc-ks-txd-unaided-decline", lowest="L3", methods=[KT],
             text="Practice with unguarded AI assistance can raise practice-task scores while lowering later unaided performance, so formation is assessed with at least one AI-off component."),
    ],
    enactments=[
        dict(key="seed:lc-ena-txd-formation-fc", kind="craft", craft="FC",
             prefLabel="Field Craft enactment of formation design",
             note=("In field work, formation depends on graduated exposure to conditions across seasons and sites. The design "
                   "specifies supervised field repetitions, minimum field days per season and calibration against an experienced "
                   "observer before remote or automated methods are credited; at least 20-30% field time is kept in remote-sensing "
                   "reskilling (ADR-0026 R6). Simulation is used for rare events only, never in place of graduated field exposure.")),
        dict(key="seed:lc-ena-txd-formation-dc", kind="craft", craft="DC",
             prefLabel="Data Craft enactment of formation design",
             note=("In data and AI work, formation depends on producing analyses unaided before reviewing machine output. The design "
                   "specifies by-hand quotas, seeded-error validation drills and dual-condition assessment (one AI-off and one "
                   "AI-on component) for compressed or substituted entry tasks (ADR-0026 R7).")),
        dict(key="seed:lc-ena-txd-formation-sc", kind="craft", craft="SC",
             prefLabel="Statecraft enactment of formation design",
             note=("In statecraft, formation depends on drafting, defending and negotiating under supervision. The design keeps "
                   "shadow-drafting of decision documents, observed participation in meetings and hearings, a supervised defence of a "
                   "draft before a reviewer, and graduated responsibility for commitments, even where AI drafts first versions.")),
    ],
))

# ================================================================================================ TX-D evaluate and certify (IO-C01)
TXD2 = "seed:IO-C01"
COMPETENCIES.append(dict(
    id=TXD2, slug="txd-evaluate", new=True, cluster="TX-D",
    prefLabel="Evaluate and certify others' task performance against position standards",
    altLabel=["Task-book evaluator", "Mentor and assess practitioners on the job", "On-the-job evaluation and entrustment"],
    definition=("Observes trainees and staff performing position tasks in the required context, rates the performance against "
                "written standards on an entrustment-supervision scale, gives corrective feedback, mentors through supervised "
                "repetitions, and documents qualification or entrustment decisions that a second evaluator would reproduce. "
                "Excludes designing the qualification system (the TX-D formation-design competency) and personnel supervision."),
    statement=("Observes others perform position tasks in the required context, rates the performance against written standards "
               "on an entrustment-supervision scale, gives specific corrective feedback, and documents qualification or entrustment "
               "decisions with the evidence a second evaluator would need to reproduce them."),
    span=("L2", "L4"),
    learningDesign=dict(assessmentContext="field | incident | desk-data (evaluated in the context the position's tasks are coded for)",
                        recommendedModes=["WBL", "MEN", "CL", "SIM"], typicalHoursPerLevelStep=20),
    derivedFrom=[],
    editorialNote=("TX-D survivor (candidate IO-C01; ADR-0025 §1). Absorbs LC-C-02 (mentor and assess practitioners on the job). "
                   "Levels follow the ATT-FOR descriptors: L2 shows peers routine tasks, L3 evaluates task performance against "
                   "standards (task-book evaluator), L4 certifies others' qualification (vocab/proficiency_levels.yaml). The "
                   "evaluation-context rule follows incident-qualification practice, where performance on the wrong assignment "
                   "type is not valid for qualification and the final evaluator must be qualified in the position [E: LC-104]. "
                   "Basis for the competency itself: IO Phase 2 (IO-056, IO-057, IO-059, IO-060) and LC Phase 2 (LC-033, LC-034)."),
    sources=["LC-104", "LC-103"],
    indicators=[
        ("L2", "a", "Corrects each missed cue or check when observing a newer colleague repeat a routine task the observer has demonstrated, before the next repetition.",
         UNAIDED, [TBO], ["seed:lc-txd-give-feedback"], None, dict()),
        ("L2", "b", "Records the result of each supervised repetition of a trainee's task in the trainee's development record, noting the supervision level given and any step repeated.",
         UNAIDED, [REC], ["seed:lc-txd-document-decision"], None, dict()),
        ("L3", "a", "Rates a trainee's performance of coded task-book tasks on the entrustment-supervision scale so that a second trained evaluator watching the same performance assigns the same rating.",
         UNAIDED, [TBO, REC], ["seed:lc-txd-rate-performance"], "ATT-FOR", dict()),
        ("L3", "b", "Gives a trainee corrective feedback after an observed task that names the standard missed, the observed behaviour and the next repetition required.",
         UNAIDED, [TBO, SIM], ["seed:lc-txd-give-feedback"], "ATT-FOR", dict()),
        ("L3", "c", "Withholds sign-off on a task when the observed performance did not occur in the evaluation context the task is coded for, and records the reason.",
         UNAIDED, [REC, TBO], ["seed:lc-txd-document-decision"], "ATT-GUI", dict()),
        ("L3", "d", "Evaluates a trainee's AI-assisted work product by checking the trainee's documented verification of each machine-generated element, not only the final product.",
         ASSISTED, [SEW, REC], ["seed:lc-txd-review-assisted-work"], "ATT-AUG", dict()),
        ("L4", "a", "Certifies a candidate's qualification for a position after reviewing the completed performance record, evaluator ratings and currency, and records the decision and its basis.",
         UNAIDED, [REC, POR], ["seed:lc-txd-certify-qualification"], "ATT-FOR", dict()),
        ("L4", "b", "Reviews a sample of other evaluators' sign-offs against the recorded evidence and returns each rating the evidence does not support, with the reason.",
         UNAIDED, [REC], ["seed:lc-txd-certify-qualification"], "ATT-SCO", dict()),
        ("L4", "c", "Resolves a disputed qualification decision by re-observing the contested task or commissioning an independent evaluation, and records the resolution and basis.",
         UNAIDED, [REC, BARS], ["seed:lc-txd-certify-qualification"], "ATT-CPX", dict()),
    ],
    tasks=[
        dict(key="seed:lc-txd-rate-performance", text="Rate a trainee's observed performance of position tasks on the entrustment-supervision scale in the evaluation context each task requires",
             wf="WF-LEARN", field="on-site-preferred", form="yes", supports=[(TXD2, "primary")], rr=rr("H", "seasonal", "general", "internal-qualification", "M")),
        dict(key="seed:lc-txd-give-feedback", text="Give corrective feedback after each observed task that names the standard missed and the next repetition required",
             wf="WF-LEARN", field="on-site-preferred", form="yes", supports=[(TXD2, "primary")], rr=rr("M", "none", "general", None, "M")),
        dict(key="seed:lc-txd-document-decision", text="Document qualification or entrustment decisions with the observed evidence a second evaluator would need to reproduce them",
             wf="WF-LEARN", field="remote-capable", form="partial", supports=[(TXD2, "primary")], rr=rr("L", "none", "general", None, "L")),
        dict(key="seed:lc-txd-certify-qualification", text="Certify a candidate's qualification for a position from the completed performance record, evaluator ratings and currency evidence",
             wf="WF-LEARN", field="remote-capable", form="partial", supports=[(TXD2, "primary")], rr=rr("M", "none", "general", "internal-qualification", "L")),
        dict(key="seed:lc-txd-supervise-unaided-reps", text="Supervise a trainee's repetitions of a formation task performed without AI assistance before assisted performance is credited",
             wf="WF-LEARN", field="on-site-preferred", form="yes", supports=[(TXD2, "primary"), (TXD1, "contributing")], rr=rr("H", "seasonal", "general", None, "M"),
             note="From LC-C-02 (mentor and assess on the job), merged into IO-C01."),
        dict(key="seed:lc-txd-review-assisted-work", text="Review a trainee's AI-assisted work product by checking the documented verification of each machine-generated element",
             wf="WF-LEARN", field="remote-capable", form="yes", supports=[(TXD2, "primary")], rr=rr("M", "none", "general", None, "M"),
             note="G-2 review half: the trainee's production is compressible; the evaluator's check of verification is not."),
    ],
    knowledge=[
        dict(key="seed:lc-ks-txd-entrustment-scale", lowest="L3", methods=[KT],
             text="An entrustment-supervision scale rates the supervision a trainee still needs, from the assessor performing the task to no supervision needed, rather than rating the trainee against peers."),
    ],
    enactments=[
        dict(key="seed:lc-ena-txd-evaluate-incident", kind="actor", actorType="federal", authorityPosition="resource-manager",
             prefLabel="Incident-qualification enactment of evaluating and certifying others",
             authorityBasis="Interagency wildland fire and incident position qualification standards adopted by the employing agency",
             principal="The employing agency's certifying official, who certifies the trainee on the evaluators' recommendation",
             accountabilityVenue="Agency qualification review and the incident qualification records system",
             note=("Evaluation follows position task books: each task carries a code for the assignment type it must be performed on, "
                   "performance on another assignment type is not valid for qualification, evaluators must be qualified in the "
                   "position or supervise the trainee, the final evaluator must be qualified in it, and the agency, not the "
                   "evaluator, certifies [E: LC-104; template dated 2008, current task-book format to be re-checked against the "
                   "annually revised qualification standard, LC-103]. Applies to state and local fire agencies that use the same "
                   "system; aligned federal standards take effect January 2027 [E: V3-13].")),
        dict(key="seed:lc-ena-txd-evaluate-inspector", kind="actor", actorType="state", authorityPosition="regulator",
             prefLabel="Regulatory-inspector enactment of evaluating and certifying others",
             authorityBasis="The state programme's procedures for delegating inspection authority to trained staff",
             principal="The programme manager who issues inspector credentials on the evaluator's recommendation",
             accountabilityVenue="Programme credential records and enforcement-case review of inspection findings",
             note=("Trainee inspectors are evaluated on observed inspections before a credential to inspect independently is issued; "
                   "the evaluator checks findings of fact, evidence handling and the inspection report against the programme's "
                   "standard, because those products must withstand enforcement challenge. Procedures vary by state [J].")),
    ],
))

# ================================================================================================ TX-D knowledge continuity (FH-C07)
TXD3 = "seed:FH-C07"
COMPETENCIES.append(dict(
    id=TXD3, slug="txd-continuity", new=True, cluster="TX-D",
    prefLabel="Elicit, document and transfer tacit and institutional knowledge before people leave",
    altLabel=["Capture and transfer critical institutional and place-based knowledge before staff separate",
              "Structured knowledge handover", "Cross-generational knowledge exchange", "Knowledge continuity"],
    definition=("Identifies knowledge held by one or a few people that the work depends on (site histories, decision rationales, "
                "relationships, local protocols, field cues), elicits it through structured interviews, field walk-throughs and "
                "annotated records, transfers it through paired work and planned handover, and verifies that successors can apply "
                "it, at separation, retirement, reassignment and when work moves between organizations. Excludes general records "
                "management and the curation of retrieval corpora for AI tools (a Data Craft practice competency)."),
    statement=("Identifies critical knowledge held by one or a few people, elicits it through structured interviews, field "
               "walk-throughs and annotated records, transfers it through paired work and planned handover, and verifies that "
               "successors can apply it before the holder leaves or the work moves to another organization."),
    span=("L2", "L4"),
    learningDesign=dict(assessmentContext="field | stakeholder | desk-data (verified by observing the successor apply the knowledge)",
                        recommendedModes=["WBL", "MEN", "CL", "FD"], typicalHoursPerLevelStep=16),
    derivedFrom=[{"v1Key": "v1:3.5.4", "relation": "merged-from",
                  "note": "v1 3.5.4 (cross-generational leadership) merged into FH-C07; cross-generational bridging is operationalized as knowledge continuity."}],
    editorialNote=("TX-D knowledge-continuity survivor (FH-C07; ADR-0025 §1). Absorbs IO-C03 (elicit tacit expertise), FS-C12, "
                   "CC-CM-01 (structured handover) and C-LM-05 (institutional knowledge through attrition), and v1 3.5.4 "
                   "(candidate_disposition.csv; v1_disposition.csv). Basis: 2025-26 federal departures and EPA departures with a "
                   "30.3-year median service [E: V1-01, V1-03]. Knowledge whose holders have not chosen to share it is out of "
                   "scope; anything Tribal-related is held under ADR-0007 §D and handled by TN, not authored here."),
    sources=["V1-01", "V1-03"],
    indicators=[
        ("L2", "a", "Prepares a handover record for an assignment being transferred that lists open commitments, contacts, site conditions and decision history, so the successor can act without the predecessor.",
         UNAIDED, [WS, REC], ["seed:lc-txd-prepare-handover"], None, dict()),
        ("L2", "b", "Conducts a recorded field walk-through with a departing colleague at an assigned site, annotating each site-specific cue or hazard the colleague points out.",
         UNAIDED, [WS, TBO], ["seed:lc-txd-field-walkthrough"], None, dict()),
        ("L2", "c", "Verifies that a successor can apply a transferred procedure by observing the successor perform it once unaided, and records any step that still needs the predecessor.",
         UNAIDED, [TBO, REC], ["seed:lc-txd-verify-successor"], None, dict()),
        ("L3", "a", "Converts a structured critical-decision interview with an experienced practitioner into documented cues and decision rules that a second expert confirms as accurate.",
         UNAIDED, [WS, BARS], ["seed:lc-txd-elicit-interview"], "ATT-CPX", dict()),
        ("L3", "b", "Ranks the critical knowledge in a unit by how few people hold it and the risk of losing it, recording the basis for each ranking.",
         UNAIDED, [WS], ["seed:lc-txd-identify-single-incumbent"], "ATT-SCO", dict()),
        ("L3", "c", "Pairs departing and early-career staff on live assignments under a written transfer plan that names the knowledge to transfer and how its transfer will be checked.",
         UNAIDED, [WS, REC], ["seed:v1-3.5.4-T1"], "ATT-FOR", dict()),
        ("L3", "d", "Checks an AI-generated summary of a departing expert's records against the expert's own account and corrects each misstatement before it enters the knowledge base.",
         ASSISTED, [SEW, WS], ["seed:lc-txd-review-generated-summary"], "ATT-AUG", dict()),
        ("L4", "a", "Designs a programme's knowledge-continuity process that starts elicitation and handover from separation, retirement-eligibility or reassignment notices, with named owners and verification steps.",
         UNAIDED, [WS, POR], ["seed:lc-txd-identify-single-incumbent"], "ATT-GUI", dict()),
        ("L4", "b", "Evaluates a programme's completed knowledge transfers by testing whether a sample of successors applied the transferred knowledge without the predecessor, and reports gaps to management.",
         UNAIDED, [REC, WS], ["seed:lc-txd-verify-successor"], "ATT-SCO", dict()),
        ("L4", "c", "Sets acceptance criteria for knowledge-capture products such as interview records, decision rules and annotated maps, so that a successor can verify and apply each one.",
         UNAIDED, [WS], ["seed:lc-txd-elicit-interview"], "ATT-GUI", dict()),
    ],
    tasks=[
        dict(key="seed:lc-txd-identify-single-incumbent", text="Identify knowledge held by one or a few people in a unit by rating its criticality and its risk of loss",
             wf="WF-LEARN", field="remote-capable", form="partial", supports=[(TXD3, "primary")], rr=rr("L", "none", "site-specific", None, "L")),
        dict(key="seed:lc-txd-elicit-interview", text="Conduct a structured critical-decision interview with an experienced practitioner to elicit the cues behind key judgments",
             wf="WF-LEARN", field="remote-capable", form="partial", supports=[(TXD3, "primary")], rr=rr("M", "none", "general", None, "M"),
             note="From IO-C03 and FS-C12, merged into FH-C07."),
        dict(key="seed:lc-txd-field-walkthrough", text="Record a field walk-through with a departing colleague that annotates the site-specific cues, hazards and history they point out",
             wf="WF-LEARN", field="on-site-required", form="yes", supports=[(TXD3, "primary")], rr=rr("M", "seasonal", "site-specific", None, "M")),
        dict(key="seed:lc-txd-prepare-handover", text="Prepare a handover record of open commitments, contacts, site conditions and decision history for a transferred assignment",
             wf="WF-LEARN", field="remote-capable", form="partial", supports=[(TXD3, "primary")], rr=rr("L", "none", "site-specific", None, "L"),
             note="From CC-CM-01 (structured handover), merged into FH-C07."),
        dict(key="seed:lc-txd-verify-successor", text="Verify that a successor can apply transferred knowledge by observing unaided performance before the holder leaves",
             wf="WF-LEARN", field="on-site-preferred", form="yes", supports=[(TXD3, "primary")], rr=rr("M", "none", "site-specific", None, "M")),
        dict(key="seed:v1-3.5.4-T1", existing=True, v1="v1:3.5.4:T1",
             text="Pair departing and early-career staff on live assignments under a written plan that names the knowledge to transfer",
             wf="WF-LEARN", field="on-site-preferred", form="yes", supports=[(TXD3, "primary")], rr=rr("M", "seasonal", "site-specific", None, "M")),
        dict(key="seed:v1-3.5.4-T2", existing=True, v1="v1:3.5.4:T2",
             text="Run two-way knowledge exchanges in which experienced staff transfer field judgment and newer staff transfer current digital methods",
             wf="WF-LEARN", field="on-site-preferred", form="partial", supports=[(TXD3, "primary")], rr=rr("M", "none", "general", None, "M")),
        dict(key="seed:lc-txd-review-generated-summary", text="Review an AI-generated summary of a departing expert's records against the expert's own account before adding it to the knowledge base",
             wf="WF-LEARN", field="remote-capable", form="partial", supports=[(TXD3, "primary")], rr=rr("L", "none", "site-specific", None, "M"),
             note="G-2 review half: transcription and summary are compressible; checking them with the holder is not."),
    ],
    knowledge=[],
    enactments=[],
))

# ================================================================================================ TX-E systems thinking (1.8.5-A)
TXE1 = "seed:v1-1.8.5-A"
COMPETENCIES.append(dict(
    id=TXE1, slug="txe-systems", new=True, cluster="TX-E",
    prefLabel="Apply systems thinking across ecological, institutional and technical systems",
    altLabel=["Systems thinking", "Social-ecological systems analysis"],
    definition=("Represents an environmental problem as interacting ecological, institutional and technical systems: maps "
                "components, flows, feedbacks, delays and leverage points, traces how an intervention propagates (including "
                "unintended and cross-boundary effects), and uses the map to choose, sequence and monitor actions. Excludes the "
                "disciplinary knowledge of any single system (knowledge areas) and formal simulation modelling (Data Craft practice)."),
    statement=("Maps an environmental problem as interacting ecological, institutional and technical systems, identifies feedbacks, "
               "delays, trade-offs and leverage points, traces how a proposed action propagates across system and jurisdictional "
               "boundaries, and uses that analysis to choose, sequence and monitor actions."),
    span=("L1", "L4"),
    learningDesign=dict(assessmentContext="desk-data | stakeholder (system maps reviewed against case evidence; participatory sessions observed)",
                        recommendedModes=["CL", "CAP", "SIM", "COP"], typicalHoursPerLevelStep=16),
    derivedFrom=[{"v1Key": "v1:1.8.5", "relation": "split-from",
                  "note": "Systems-reasoning part of v1 1.8.5; food-systems content goes to v1 1.8.1 (MOD-14 worklands, WP-06)."}],
    editorialNote=("TX-E successor split from v1 1.8.5 (ADR-0025 §1; v1_disposition.csv). Accreditors treat systems reasoning as a "
                   "programme outcome developed across a curriculum (SAF integrative components; ABET general outcomes) [E: LC-001, "
                   "LC-002], which is why it is typed transversal: a programme maps it once. Also carries the domain-level "
                   "cross-cutting systems content of the v1 Policy and Regulatory domain source text (ADR-0025 table; CA-006). The "
                   "three v1 1.8.5 food-systems tasks are left for WP-06 to move to MOD-14 with v1 1.8.1."),
    sources=["LC-001", "LC-002"],
    indicators=[
        ("L1", "a", "Draws a system diagram for an assigned problem that shows the main components and flows named in the briefing materials, for review by a senior colleague.",
         UNAIDED, [WS], ["seed:lc-txe-map-system"], None, dict()),
        ("L1", "b", "Identifies, for an assigned management action, at least one effect on another resource, user group or agency outside the action's target, and reports it to the lead.",
         UNAIDED, [WS, KT], ["seed:lc-txe-trace-effects"], None, dict()),
        ("L2", "a", "Produces a causal-loop or stock-and-flow diagram for a routine management problem that marks each feedback loop and the evidence for each link.",
         UNAIDED, [WS], ["seed:lc-txe-map-system"], "ATT-AUT", dict()),
        ("L2", "b", "Traces a proposed action's likely second-order effects across ecological, institutional and technical components, citing the evidence or assumption behind each effect.",
         UNAIDED, [WS], ["seed:lc-txe-trace-effects"], "ATT-KNO", dict()),
        ("L2", "c", "Checks an AI-generated system map or causal summary against case evidence and field knowledge, correcting or removing each unsupported link before the map is used.",
         ASSISTED, [SEW], ["seed:lc-txe-review-generated-map"], "ATT-AUG", dict()),
        ("L3", "a", "Compares alternative interventions on a system map of a contested multi-party problem to identify leverage points, documenting the trade-offs for decision-makers.",
         UNAIDED, [WS, BARS], ["seed:lc-txe-compare-interventions"], "ATT-CPX", dict()),
        ("L3", "b", "Facilitates a participatory system-mapping session with parties holding different views, producing a shared map that records each point of disagreement.",
         UNAIDED, [SIM, WS], ["seed:lc-txe-facilitate-mapping"], "ATT-SCO", dict()),
        ("L3", "c", "Adapts a monitoring plan to detect the unintended cross-boundary effects predicted by the system map, naming the indicator and trigger for each effect.",
         UNAIDED, [WS], ["seed:lc-txe-trace-effects"], "ATT-GUI", dict()),
        ("L4", "a", "Designs the systems analysis for a landscape or programme plan, specifying the boundaries, actors, scenarios and decision triggers the plan will use.",
         UNAIDED, [WS, POR], ["seed:lc-txe-compare-interventions"], "ATT-SCO", dict()),
        ("L4", "b", "Reviews other teams' plans for omitted feedbacks and cross-boundary effects, returning each omission with the evidence that it matters.",
         UNAIDED, [WS, REC], ["seed:lc-txe-trace-effects"], "ATT-FOR", dict()),
    ],
    tasks=[
        dict(key="seed:lc-txe-map-system", text="Map a management problem as interacting ecological, institutional and technical components with their main flows and feedbacks",
             wf="WF-PLAN", field="remote-capable", form="partial", supports=[(TXE1, "primary")], rr=rr("L", "none", "ecosystem-type", None, "L")),
        dict(key="seed:lc-txe-trace-effects", text="Trace a proposed action's second-order effects across resources, users and jurisdictions before the action is selected",
             wf="WF-REVIEW", field="remote-capable", form="partial", supports=[(TXE1, "primary")], rr=rr("M", "none", "ecosystem-type", None, "L")),
        dict(key="seed:lc-txe-facilitate-mapping", text="Facilitate a participatory system-mapping session with parties who hold different views of a shared problem",
             wf="WF-PLAN", field="remote-capable", form="partial", supports=[(TXE1, "primary")], modes=["MODE-ENGAGE"], rr=rr("M", "none", "general", None, "M")),
        dict(key="seed:lc-txe-compare-interventions", text="Compare alternative interventions on a system map to identify leverage points and trade-offs for decision-makers",
             wf="WF-PLAN", field="remote", form="partial", supports=[(TXE1, "primary")], rr=rr("L", "none", "general", None, "L")),
        dict(key="seed:lc-txe-review-generated-map", text="Review an AI-generated system map or causal summary against case evidence and field knowledge before it is used",
             wf="WF-PLAN", field="remote-capable", form="yes", supports=[(TXE1, "primary")], rr=rr("M", "none", "ecosystem-type", None, "M"),
             note="G-2 review half."),
    ],
    knowledge=[
        dict(key="seed:lc-ks-txe-feedback-delay", lowest="L1", methods=[KT],
             text="Feedback loops and delays mean that the short-term response of an ecological or institutional system to an action can differ in sign from its long-term response."),
    ],
    enactments=[],
))

# ================================================================================================ TX-E risk communication (DB-C29)
TXE2 = "seed:DB-C29"
COMPETENCIES.append(dict(
    id=TXE2, slug="txe-riskcomm", new=True, cluster="TX-E",
    prefLabel="Communicate environmental and health risks under uncertainty",
    altLabel=["Risk and crisis communication", "Public advisories and notices"],
    definition=("Designs and delivers risk and crisis communication (advisories, do-not-drink and boil-water notices, smoke and heat "
                "messages, cleanup and exposure updates) that is accurate, timely, actionable and understood by affected publics, "
                "states uncertainty plainly, is tested for comprehension, and reaches people in the languages they use. Excludes "
                "environmental education and interpretation, and the underlying risk assessment."),
    statement=("Prepares and delivers risk and crisis messages that state what is known, what is uncertain and what people should "
               "do, tailored to affected audiences and their languages, tested for comprehension, coordinated with partner agencies, "
               "and updated as evidence changes."),
    span=("L1", "L4"),
    learningDesign=dict(assessmentContext="stakeholder | incident (message products scored; simulated public meetings and calls)",
                        recommendedModes=["CL", "SIM", "WBL", "MEN"], typicalHoursPerLevelStep=16),
    derivedFrom=[],
    editorialNote=("TX-E (candidate DB-C29; ADR-0025 §1). v1 communication competencies are educational or interpretive; risk "
                   "communication under uncertainty is a distinct, assessable performance required across modules (DB rationale; "
                   "DB-021, DB-030). Module enactments (water: public notification; envhealth: advisories; hazards and forest: "
                   "smoke and evacuation messaging) are handed to WP-06."),
    sources=[],
    indicators=[
        ("L1", "a", "Delivers an approved risk message to members of the public at a site or by phone using the current message map, and logs each question it does not answer.",
         UNAIDED, [SIM], ["seed:lc-txe-answer-public-questions"], None, dict()),
        ("L1", "b", "Checks a draft notice against the approved message map and flags every statement of fact, uncertainty or protective action that differs from it.",
         UNAIDED, [SEW, WS], ["seed:lc-txe-draft-advisory"], None, dict()),
        ("L2", "a", "Drafts a public advisory for a routine event that states the hazard, who is affected, what is uncertain and the protective action, in plain language at the programme's reading-level target.",
         UNAIDED, [WS], ["seed:lc-txe-draft-advisory"], "ATT-AUT", dict()),
        ("L2", "b", "Tests a draft risk message with a small sample of the intended audience and records each wording change made where readers misread it.",
         UNAIDED, [WS, REC], ["seed:lc-txe-test-comprehension"], "ATT-GUI", dict()),
        ("L2", "c", "Verifies an AI-drafted or machine-translated advisory against the source data and a fluent reviewer before release, correcting each change of meaning.",
         ASSISTED, [SEW, WS], ["seed:lc-txe-verify-generated-notice"], "ATT-AUG", dict()),
        ("L2", "d", "Translates a measured exposure value into a message that gives the value, its comparison standard and its uncertainty without overstating safety or danger.",
         UNAIDED, [WS], ["seed:lc-txe-draft-advisory"], "ATT-KNO", dict()),
        ("L3", "a", "Prepares a message map for an emerging incident with partner agencies, so that all parties issue consistent statements of hazard, uncertainty and protective action.",
         UNAIDED, [WS, SIM], ["seed:lc-txe-prepare-message-map"], "ATT-SCO", dict()),
        ("L3", "b", "Answers questions about an uncertain risk in a contested public meeting by stating what is known, what is not known and when new information will be available.",
         UNAIDED, [SIM, BARS], ["seed:lc-txe-answer-public-questions"], "ATT-CPX", dict()),
        ("L3", "c", "Revises standing advisories when new evidence changes the risk picture, documenting what changed and why for the public record.",
         UNAIDED, [WS, REC], ["seed:lc-txe-draft-advisory"], "ATT-GUI", dict()),
        ("L4", "a", "Designs a programme's risk-communication protocol that specifies message-approval roles, translation and comprehension testing, update triggers and partner coordination for recurring hazards.",
         UNAIDED, [WS, POR], ["seed:lc-txe-prepare-message-map"], "ATT-GUI", dict()),
        ("L4", "b", "Evaluates a programme's risk communication after an event against comprehension, timeliness and consistency evidence, and reports corrective actions to programme leadership.",
         UNAIDED, [WS, REC], ["seed:lc-txe-test-comprehension"], "ATT-SCO", dict()),
    ],
    tasks=[
        dict(key="seed:lc-txe-draft-advisory", text="Draft a public advisory that states the hazard, the people affected, the uncertainty and the protective action in plain language",
             wf="WF-RESPOND", field="remote-capable", form="partial", supports=[(TXE2, "primary")], modes=["MODE-ENGAGE"], rr=rr("M", "multi-year-or-rare-event", "general", None, "M")),
        dict(key="seed:lc-txe-test-comprehension", text="Test a draft risk message for comprehension with members of the intended audience before it is released",
             wf="WF-RESPOND", field="remote-capable", form="partial", supports=[(TXE2, "primary")], modes=["MODE-ENGAGE"], rr=rr("L", "none", "general", None, "L")),
        dict(key="seed:lc-txe-prepare-message-map", text="Prepare a shared message map with partner agencies for an emerging environmental or health incident",
             wf="WF-RESPOND", field="remote-capable", form="partial", supports=[(TXE2, "primary")], modes=["MODE-ENGAGE"], rr=rr("M", "multi-year-or-rare-event", "general", None, "M")),
        dict(key="seed:lc-txe-answer-public-questions", text="Answer public questions about an uncertain environmental risk at a meeting or by phone using the current message map",
             wf="WF-RESPOND", field="on-site-preferred", form="yes", supports=[(TXE2, "primary")], modes=["MODE-ENGAGE"], rr=rr("M", "multi-year-or-rare-event", "general", None, "M")),
        dict(key="seed:lc-txe-verify-generated-notice", text="Verify an AI-drafted or machine-translated risk notice against the source data and a fluent reviewer before release",
             wf="WF-RESPOND", field="remote", form="partial", supports=[(TXE2, "primary")], modes=["MODE-ENGAGE"], rr=rr("L", "none", "general", None, "M"),
             note="G-2 review half."),
    ],
    knowledge=[],
    enactments=[],
))

# ================================================================================================ TX-F scope (PS-C01)
TXF1 = "seed:PS-C01"
COMPETENCIES.append(dict(
    id=TXF1, slug="txf-scope", new=True, cluster="TX-F",
    prefLabel="Manage client and partner scope for environmental work",
    altLabel=["Manage client relationships and scope for environmental services", "Statement-of-work management", "Change-order management"],
    definition=("Defines what a client, sponsor or partner needs, negotiates scope, assumptions, exclusions and acceptance criteria, "
                "manages expectations, and controls scope changes through documented change orders or modifications, for "
                "environmental studies, permits, compliance services and partnership work. On the public side the same performance "
                "is enacted by contracting officers' technical representatives and agreement managers. Excludes pricing and "
                "proposal writing and delivery to budget and schedule (separate TX-F competencies)."),
    statement=("Defines the client's or partner's needs, negotiates scope, assumptions, exclusions and acceptance criteria, and "
               "controls changes through documented change orders or modifications, so that both parties agree what will be "
               "delivered, by when and at what cost, for environmental studies, permits, compliance and partnership work."),
    span=("L1", "L4"),
    learningDesign=dict(assessmentContext="stakeholder | desk-data (scope documents scored; negotiation simulations)",
                        recommendedModes=["CL", "SIM", "WBL", "MEN"], typicalHoursPerLevelStep=16),
    derivedFrom=[],
    editorialNote=("TX-F (candidate PS-C01; ADR-0025 §1; ADR-0003 G-8) with public enactments for technical representatives on "
                   "contracts and for grant and agreement managers. Private hiring criterion absent from v1 (PS rationale, PS-016)."),
    sources=[],
    indicators=[
        ("L1", "a", "Records each client or partner request that falls outside the agreed scope in the project change log, and refers it to the project manager the same day.",
         UNAIDED, [REC], ["seed:lc-txf-prepare-change-order"], None, dict()),
        ("L1", "b", "Checks a deliverable against the scope's acceptance criteria before it goes to the client or partner, and lists each criterion not met.",
         UNAIDED, [WS, SEW], ["seed:lc-txf-monitor-deliverables"], None, dict()),
        ("L2", "a", "Drafts a scope of work for a routine study or service with measurable deliverables, assumptions, exclusions and acceptance criteria that the client accepts without substantive revision.",
         UNAIDED, [WS], ["seed:lc-txf-draft-scope"], "ATT-AUT", dict()),
        ("L2", "b", "Prepares a change order or agreement modification for a scope change that states the cause, the effect on cost and schedule, and the approval required.",
         UNAIDED, [WS], ["seed:lc-txf-prepare-change-order"], "ATT-AUT", dict()),
        ("L2", "c", "Checks an AI-drafted scope of work against the client's stated needs and the practice's scope standard, correcting each missing exclusion or unmeasurable deliverable before issue.",
         ASSISTED, [SEW], ["seed:lc-txf-review-generated-scope"], "ATT-AUG", dict()),
        ("L3", "a", "Negotiates a scope change with a client or partner under schedule or budget pressure to a signed agreement on deliverables, cost and dates.",
         UNAIDED, [SIM, BARS, REC], ["seed:lc-txf-negotiate-scope-change"], "ATT-SCO", dict()),
        ("L3", "b", "Resolves a dispute over whether a deliverable meets its acceptance criteria by comparing it with the agreed criteria, and documents the resolution.",
         UNAIDED, [SIM, REC], ["seed:lc-txf-monitor-deliverables"], "ATT-CPX", dict()),
        ("L3", "c", "Prepares the scope for a multi-party or multi-phase effort that assigns each deliverable to a party and states its dependencies and handoff criteria.",
         UNAIDED, [WS], ["seed:lc-txf-draft-scope"], "ATT-CPX", dict()),
        ("L4", "a", "Develops standard scope, assumption and acceptance-criteria templates for a practice's recurring services, revised from lessons recorded at project closeout.",
         UNAIDED, [WS, POR], ["seed:lc-txf-draft-scope"], "ATT-GUI", dict()),
        ("L4", "b", "Reviews scopes prepared by others for unpriced risk, vague acceptance criteria and missing exclusions before issue, returning each deficiency with a correction.",
         UNAIDED, [WS, REC], ["seed:lc-txf-review-generated-scope"], "ATT-FOR", dict()),
    ],
    tasks=[
        dict(key="seed:lc-txf-draft-scope", text="Draft a scope of work with measurable deliverables, assumptions, exclusions and acceptance criteria for an environmental study or service",
             wf="WF-MANAGE", field="remote", form="partial", supports=[(TXF1, "primary")], rr=rr("M", "none", "general", None, "L")),
        dict(key="seed:lc-txf-prepare-change-order", text="Prepare a change order or agreement modification that states the cause and the cost and schedule effect of a scope change",
             wf="WF-MANAGE", field="remote", form="partial", supports=[(TXF1, "primary")], rr=rr("L", "none", "general", None, "L")),
        dict(key="seed:lc-txf-negotiate-scope-change", text="Negotiate a scope change with a client or partner to a documented agreement on deliverables, cost and dates",
             wf="WF-MANAGE", field="remote", form="partial", supports=[(TXF1, "primary")], modes=["MODE-RESOLVE"], rr=rr("M", "none", "general", None, "M")),
        dict(key="seed:lc-txf-monitor-deliverables", text="Monitor contractor or partner deliverables against the agreed acceptance criteria as the designated technical representative",
             wf="WF-MANAGE", field="remote-capable", form="partial", supports=[(TXF1, "primary")], rr=rr("L", "none", "general", "internal-qualification", "L")),
        dict(key="seed:lc-txf-review-generated-scope", text="Review an AI-drafted scope of work against the client's stated needs and the practice's scope standard before issue",
             wf="WF-MANAGE", field="remote", form="partial", supports=[(TXF1, "primary")], rr=rr("L", "none", "general", None, "M"),
             note="G-2 review half."),
    ],
    knowledge=[],
    enactments=[
        dict(key="seed:lc-ena-txf-scope-federal-technical-rep", kind="actor", actorType="federal", authorityPosition="funder",
             prefLabel="Contract technical-representative enactment of scope management",
             authorityBasis="Written designation by the contracting officer under the agency's acquisition procedures",
             principal="The contracting officer who holds the contract and alone may change its scope, price or schedule",
             accountabilityVenue="The contract file and the agency's acquisition oversight and audit",
             note=("Public-side mirror of client scope management: the technical representative monitors performance and acceptance "
                   "against the statement of work, documents deficiencies and recommends modifications, but cannot agree a change of "
                   "scope, price or schedule; requests that bypass the contracting officer are recorded and routed, not agreed [J]. "
                   "Designation usually requires a training-based certification, recorded as a credential gate, not a level.")),
        dict(key="seed:lc-ena-txf-scope-agreement-manager", kind="actor", actorType="state", authorityPosition="funder",
             prefLabel="Grant and agreement-manager enactment of scope management",
             authorityBasis="The financial-assistance award or partnership agreement and the awarding agency's grants policy",
             principal="The awarding official or grants officer who approves changes to the approved work plan",
             accountabilityVenue="The award file, programme monitoring and independent audit of public awards",
             note=("Scope is the approved work plan and budget; changes beyond the award's stated flexibility need prior written "
                   "approval from the awarding official, and the agency's involvement in the work is limited to what the agreement "
                   "states. Also enacted by federal and local awarding agencies and by NGO pass-through recipients [J].")),
    ],
))

# ================================================================================================ TX-F proposals (PS-C02)
TXF2 = "seed:PS-C02"
COMPETENCIES.append(dict(
    id=TXF2, slug="txf-proposals", new=True, cluster="TX-F",
    prefLabel="Develop proposals and grant applications for environmental work",
    altLabel=["Develop business and write winning proposals for environmental work", "Grant writing", "Capture planning"],
    definition=("Decides whether to pursue a funding or contract opportunity, plans the response, writes the technical approach, "
                "assembles qualifications and past performance, and prepares a compliant budget and price for requests for "
                "proposals, task orders, grants and cooperative agreements. Covers private business development and public, "
                "non-profit and local-government grant seeking. Excludes delivering the funded work and negotiating the resulting "
                "agreement's legal terms."),
    statement=("Makes documented go/no-go decisions on funding and contract opportunities, plans the response, writes a technical "
               "approach that answers the evaluation criteria, assembles qualifications and past performance, and prepares a "
               "compliant budget and price for proposals, task orders, grants and cooperative agreements."),
    span=("L1", "L4"),
    learningDesign=dict(assessmentContext="desk-data | stakeholder (proposal and budget work samples scored against the solicitation)",
                        recommendedModes=["CL", "WBL", "MEN", "CAP"], typicalHoursPerLevelStep=20),
    derivedFrom=[],
    editorialNote=("TX-F (candidate PS-C02; ADR-0025 §1; ADR-0003 G-8). 'Winning' is dropped from the title because an outcome "
                   "decided by funders is not the person's performance (IO B05). Public enactment: applicants to public financial "
                   "assistance. Proposal writing is also the main funding bottleneck for NGO and local-government programmes (PS rationale)."),
    sources=[],
    indicators=[
        ("L1", "a", "Checks a draft proposal or application against the solicitation's compliance requirements and lists every missing or non-conforming item before submission.",
         UNAIDED, [SEW, WS], ["seed:lc-txf-check-compliance"], None, dict()),
        ("L1", "b", "Assembles the qualifications and past-performance section of a proposal from the organization's records to the solicitation's format and page limits.",
         UNAIDED, [WS], ["seed:lc-txf-write-approach"], None, dict()),
        ("L2", "a", "Writes a technical approach section that answers each stated evaluation criterion with a method, schedule and staffing basis an internal reviewer can trace.",
         UNAIDED, [WS], ["seed:lc-txf-write-approach"], "ATT-AUT", dict()),
        ("L2", "b", "Prepares a budget and budget justification for a grant or task order that follows the funder's cost rules and ties each cost to a work-plan task.",
         UNAIDED, [WS], ["seed:lc-txf-prepare-proposal-budget"], "ATT-AUT", dict()),
        ("L2", "c", "Recommends go or no-go on an opportunity from a documented assessment of fit, competition, capacity and funder requirements.",
         UNAIDED, [WS, BARS], ["seed:lc-txf-decide-pursuit"], "ATT-GUI", dict()),
        ("L2", "d", "Verifies every claim of past performance, staffing and capacity in an AI-drafted proposal section against the organization's records, removing any claim it cannot support.",
         ASSISTED, [SEW], ["seed:lc-txf-review-generated-proposal"], "ATT-AUG", dict()),
        ("L3", "a", "Prepares a capture plan for a priority opportunity that records the funder's needs, competitors, partners and decision points before the solicitation is issued.",
         UNAIDED, [WS], ["seed:lc-txf-decide-pursuit"], "ATT-SCO", dict()),
        ("L3", "b", "Directs a proposal team to a compliant, on-time submission by assigning sections and setting internal review gates, recording how each review comment was resolved.",
         UNAIDED, [WS, REC], ["seed:lc-txf-check-compliance"], "ATT-SCO", dict()),
        ("L3", "c", "Revises a proposal after an independent internal review by addressing each scored weakness or recording why it was left unchanged.",
         UNAIDED, [WS, REC], ["seed:lc-txf-write-approach"], "ATT-GUI", dict()),
        ("L4", "a", "Sets a practice's pursuit criteria and proposal review gates, basing them on recorded results and funder debriefs from past submissions.",
         UNAIDED, [WS, POR], ["seed:lc-txf-decide-pursuit"], "ATT-GUI", dict()),
        ("L4", "b", "Reviews proposals prepared by others for compliance gaps, unsupported claims and price risk before submission, returning each issue with the evidence needed.",
         UNAIDED, [WS, REC], ["seed:lc-txf-review-generated-proposal"], "ATT-FOR", dict()),
    ],
    tasks=[
        dict(key="seed:lc-txf-decide-pursuit", text="Decide whether to pursue a funding or contract opportunity using a documented assessment of fit, capacity and competition",
             wf="WF-RESOURCE", field="remote", form="partial", supports=[(TXF2, "primary")], rr=rr("M", "none", "general", None, "M")),
        dict(key="seed:lc-txf-write-approach", text="Write a technical approach that answers each evaluation criterion of a solicitation or funding notice",
             wf="WF-RESOURCE", field="remote", form="partial", supports=[(TXF2, "primary")], rr=rr("M", "none", "general", None, "M")),
        dict(key="seed:lc-txf-prepare-proposal-budget", text="Prepare a budget and justification for a grant application or task order that follows the funder's cost rules",
             wf="WF-RESOURCE", field="remote", form="partial", supports=[(TXF2, "primary"), ("seed:PS-C03", "contributing")], rr=rr("M", "none", "general", None, "L")),
        dict(key="seed:lc-txf-check-compliance", text="Check a proposal or application against the solicitation's compliance requirements before it is submitted",
             wf="WF-RESOURCE", field="remote", form="no", supports=[(TXF2, "primary")], rr=rr("L", "none", "general", None, "L")),
        dict(key="seed:lc-txf-review-generated-proposal", text="Review an AI-drafted proposal section against the solicitation, the organization's records and the actual staffing plan before submission",
             wf="WF-RESOURCE", field="remote", form="partial", supports=[(TXF2, "primary")], rr=rr("L", "none", "general", None, "M"),
             note="G-2 review half: drafting is compressible; verifying claims of capacity and past performance is not."),
    ],
    knowledge=[],
    enactments=[
        dict(key="seed:lc-ena-txf-proposals-public-applicant", kind="actor", actorType="ngo", authorityPosition="service-provider",
             prefLabel="Public financial-assistance applicant enactment of proposal development",
             authorityBasis="The funding notice and the awarding agency's financial-assistance rules",
             principal="The applicant organization's authorized representative, who signs the application and its certifications",
             accountabilityVenue="The funder's merit review and post-award monitoring and audit",
             note=("For non-profit, local-government and agency applicants to public financial assistance, the performance shifts "
                   "from price competition to eligibility, cost share, allowable costs and reporting commitments; the signing "
                   "official certifies compliance, so the application must not promise capacity the organization cannot document. "
                   "Also enacted by local governments and conservation districts [J].")),
    ],
))

# ================================================================================================ TX-F delivery (PS-C03)
TXF3 = "seed:PS-C03"
COMPETENCIES.append(dict(
    id=TXF3, slug="txf-delivery", new=True, cluster="TX-F",
    prefLabel="Deliver environmental projects to budget, schedule and quality",
    altLabel=["Deliver billable environmental projects to budget, schedule and quality", "Project planning and scheduling",
              "Project risk management", "Project budgeting and cost control"],
    definition=("Plans and phases project work, builds and tracks the schedule and budget (including labour hours and estimate at "
                "completion), manages project risks and subcontractors, runs quality review before deliverables leave, and reports "
                "and invoices against the agreement, for billable services and for grant-funded and cost-recovery projects. "
                "Excludes public budget formulation and appropriations (a Statecraft practice competency), legal administration of "
                "contracts and agreements, and specific project-management software (tools layer)."),
    statement=("Plans and phases project work, sets and tracks the schedule and budget through estimate at completion, manages risks, "
               "subcontractors and seasonal or regulatory windows, runs quality review before deliverables are released, and reports "
               "progress and costs against the agreement for billable, grant-funded and cost-recovery projects."),
    span=("L1", "L4"),
    learningDesign=dict(assessmentContext="desk-data | stakeholder (project-control records audited; recovery simulations)",
                        recommendedModes=["CL", "WBL", "MEN", "SIM"], typicalHoursPerLevelStep=24),
    derivedFrom=[{"v1Key": "v1:3.1.1", "relation": "merged-from"},
                 {"v1Key": "v1:3.1.3", "relation": "merged-from"},
                 {"v1Key": "v1:3.1.2", "relation": "split-from", "note": "Project-budgeting part; public budget formulation and appropriations go to seed:SC-C10 (WP-05)."},
                 {"v1Key": "v1:2.5.3", "relation": "merged-from", "note": "Durable remainder of the move-to-tools decision; the software goes to L4 (seed:tool-project-management-software, WP-04)."}],
    editorialNote=("TX-F (candidate PS-C03; ADR-0025 §1; ADR-0003 G-8). Receives v1 3.1.1 and 3.1.3 (merge), project budgeting from "
                   "v1 3.1.2 (split) and the durable remainder of v1 2.5.3 (move-to-tools), per v1_disposition.csv. AI compresses "
                   "schedule and estimate drafting and pressures time-and-materials billing (PS rationale, PS-015), hence the G-2 "
                   "review task. Public enactments: cost-recovery work and grant-funded delivery."),
    sources=[],
    indicators=[
        ("L1", "a", "Records hours and costs against the correct project tasks each week, so that the project cost report reconciles with timesheets and invoices.",
         UNAIDED, [REC], ["seed:lc-txf-invoice-against-agreement"], None, dict(v1=["v1:3.1.2:foundational:I1"])),
        ("L1", "b", "Updates an assigned section of the project schedule with actual progress each week and flags each task forecast to miss its date.",
         UNAIDED, [REC, WS], ["seed:v1-3.1.1-T2"], None, dict(v1=["v1:3.1.1:foundational:I2"])),
        ("L1", "c", "Checks a deliverable against the project's quality-review checklist before it goes to the reviewer, and records each item corrected.",
         UNAIDED, [SEW, REC], ["seed:lc-txf-run-quality-review"], None, dict()),
        ("L2", "a", "Prepares a phased work plan and schedule for a routine project that sequences field work within seasonal and regulatory windows and shows each dependency.",
         UNAIDED, [WS], ["seed:v1-3.1.1-T1", "seed:v1-3.1.1-T3"], "ATT-AUT", dict(v1=["v1:3.1.1:intermediate:I2"])),
        ("L2", "b", "Calculates estimate at completion from actual costs and remaining effort each reporting period, and reports any variance beyond the agreed threshold with its cause.",
         UNAIDED, [WS, REC], ["seed:v1-3.1.2-T2"], "ATT-AUT", dict(v1=["v1:3.1.2:intermediate:I4"])),
        ("L2", "c", "Maintains a project risk register that records each risk's likelihood, impact, owner and mitigation, updated at every progress review.",
         UNAIDED, [REC], ["seed:v1-3.1.3-T1", "seed:v1-3.1.3-T2"], "ATT-AUT", dict(v1=["v1:3.1.3:intermediate:I3"])),
        ("L2", "d", "Checks an AI-generated schedule or cost forecast against the work plan, crew capacity and seasonal windows, correcting each infeasible item before baselining.",
         ASSISTED, [SEW], ["seed:lc-txf-review-generated-schedule"], "ATT-AUG", dict()),
        ("L3", "a", "Prepares re-baselined scope, schedule and cost options with their trade-offs for the client's or sponsor's decision when a project is forecast to overrun.",
         UNAIDED, [WS, SIM], ["seed:v1-3.1.2-T3", "seed:v1-3.1.3-T3"], "ATT-CPX", dict()),
        ("L3", "b", "Withholds acceptance of a subcontractor's deliverable that fails the agreed quality criteria, recording the deficiency and the corrective action required.",
         UNAIDED, [REC, SIM], ["seed:lc-txf-manage-subcontractor"], "ATT-SCO", dict()),
        ("L3", "c", "Directs quality review of a multi-author deliverable by assigning qualified reviewers and recording the disposition of every review comment before release.",
         UNAIDED, [REC, WS], ["seed:lc-txf-run-quality-review"], "ATT-FOR", dict()),
        ("L4", "a", "Develops project-control standards for a practice that specify baselines, progress measurement, variance thresholds and review cadence, tested on closed projects.",
         UNAIDED, [WS, POR], ["seed:v1-3.1.1-T2"], "ATT-GUI", dict()),
        ("L4", "b", "Allocates staff across a portfolio of concurrent projects from forecast hours and utilization, documenting the schedule and margin trade-off of each assignment.",
         UNAIDED, [WS, REC], ["seed:v1-3.1.1-T1"], "ATT-SCO", dict()),
        ("L4", "c", "Audits a sample of a practice's projects against its project-control standards, and reports systemic gaps with corrective actions to practice leadership.",
         UNAIDED, [REC], ["seed:v1-3.1.3-T3"], "ATT-SCO", dict()),
    ],
    tasks=[
        dict(key="seed:v1-3.1.1-T1", existing=True, v1="v1:3.1.1:T1",
             text="Break a large project into phased work packages with deliverables, dependencies and decision points",
             wf="WF-MANAGE", field="remote", form="partial", supports=[(TXF3, "primary")], rr=rr("M", "none", "general", None, "L")),
        dict(key="seed:v1-3.1.1-T2", existing=True, v1="v1:3.1.1:T2",
             text="Maintain the project schedule baseline and record actual progress against it at each reporting period",
             wf="WF-MANAGE", field="remote", form="no", supports=[(TXF3, "primary")], rr=rr("L", "none", "general", None, "L")),
        dict(key="seed:v1-3.1.1-T3", existing=True, v1="v1:3.1.1:T3",
             text="Sequence field work within seasonal, weather and regulatory windows when building the project schedule",
             wf="WF-MANAGE", field="remote-capable", form="yes", supports=[(TXF3, "primary")], rr=rr("M", "seasonal", "ecosystem-type", None, "M")),
        dict(key="seed:v1-3.1.2-T1", existing=True, v1="v1:3.1.2:T1",
             text="Prepare a project budget that ties labour, subcontract and direct costs to tasks under the funder's cost rules",
             wf="WF-MANAGE", field="remote", form="partial", supports=[(TXF3, "primary")], rr=rr("M", "none", "general", None, "L"),
             note="v1 3.1.2 split: project budgeting comes to PS-C03; public budget formulation goes to SC-C10 (WP-05)."),
        dict(key="seed:v1-3.1.2-T2", existing=True, v1="v1:3.1.2:T2",
             text="Calculate estimate at completion from actual costs and remaining effort at each reporting period",
             wf="WF-MANAGE", field="remote", form="no", supports=[(TXF3, "primary")], rr=rr("L", "none", "general", None, "L")),
        dict(key="seed:v1-3.1.2-T3", existing=True, v1="v1:3.1.2:T3",
             text="Justify a budget revision to the client or sponsor by linking each change to a scope change or realized risk",
             wf="WF-MANAGE", field="remote", form="partial", supports=[(TXF3, "primary")], rr=rr("L", "none", "general", None, "L")),
        dict(key="seed:v1-3.1.3-T1", existing=True, v1="v1:3.1.3:T1",
             text="Identify project risks such as weather delays, access limits or permit timing during project design",
             wf="WF-MANAGE", field="remote-capable", form="partial", supports=[(TXF3, "primary")], rr=rr("M", "seasonal", "ecosystem-type", None, "L")),
        dict(key="seed:v1-3.1.3-T2", existing=True, v1="v1:3.1.3:T2",
             text="Prepare a contingency plan for each critical project risk that names its trigger, response and owner",
             wf="WF-MANAGE", field="remote", form="partial", supports=[(TXF3, "primary")], rr=rr("L", "none", "general", None, "L")),
        dict(key="seed:v1-3.1.3-T3", existing=True, v1="v1:3.1.3:T3",
             text="Review project progress against the baseline at each reporting period to decide corrective actions",
             wf="WF-MANAGE", field="remote", form="partial", supports=[(TXF3, "primary")], rr=rr("M", "none", "general", None, "L")),
        dict(key="seed:lc-txf-run-quality-review", text="Run quality review of a deliverable before release, recording the disposition of every reviewer comment",
             wf="WF-MANAGE", field="remote", form="partial", supports=[(TXF3, "primary")], rr=rr("M", "none", "general", None, "L")),
        dict(key="seed:lc-txf-manage-subcontractor", text="Manage a subcontractor's deliverables and invoices against the subcontract's scope, schedule and quality terms",
             wf="WF-MANAGE", field="remote-capable", form="partial", supports=[(TXF3, "primary")], rr=rr("M", "none", "general", None, "L")),
        dict(key="seed:lc-txf-invoice-against-agreement", text="Invoice project work against the agreement's billing terms with supporting hours and deliverable-acceptance records",
             wf="WF-MANAGE", field="remote", form="no", supports=[(TXF3, "primary")], rr=rr("L", "none", "general", None, "L")),
        dict(key="seed:lc-txf-review-generated-schedule", text="Review an AI-generated project schedule or cost forecast against the work plan, crew capacity and seasonal windows before baselining it",
             wf="WF-MANAGE", field="remote", form="yes", supports=[(TXF3, "primary")], rr=rr("M", "seasonal", "ecosystem-type", None, "M"),
             note="G-2 review half: drafting the schedule is compressible; judging its feasibility on the ground is not."),
    ],
    knowledge=[
        dict(key="seed:lc-ks-txf-eac", lowest="L2", methods=[KT],
             text="Estimate at completion equals actual cost to date plus the estimated cost of remaining work; a variance is the difference between it and the approved budget."),
    ],
    enactments=[
        dict(key="seed:lc-ena-txf-delivery-cost-recovery", kind="actor", actorType="state", authorityPosition="regulator",
             prefLabel="Cost-recovery enactment of project delivery",
             authorityBasis="Statutory or regulatory authority for the agency to recover processing costs or charge fees, and the cost-recovery agreement with the applicant",
             principal="The agency's authorized officer, accountable to the applicant for costs and to the public for the decision",
             accountabilityVenue="Agency cost-recovery accounting and audit; the dispute procedure in the cost-recovery agreement",
             note=("In cost-recovery work the agency tracks staff hours and costs against an agreement with the applicant much as a "
                   "consultant bills a client, but payment must not affect the outcome of the decision; time and cost records are kept "
                   "separate from the decision record. Also enacted by federal land and resource agencies that recover processing costs [J].")),
        dict(key="seed:lc-ena-txf-delivery-grant-funded", kind="actor", actorType="ngo", authorityPosition="service-provider",
             prefLabel="Grant-funded enactment of project delivery",
             authorityBasis="The terms and conditions of the financial-assistance award and the applicable cost principles",
             principal="The awarding agency's grants officer",
             accountabilityVenue="Programme monitoring, progress reports, closeout and independent audit of public awards",
             note=("Budget changes beyond the award's flexibility, no-cost extensions and scope changes need prior approval; costs must be "
                   "allowable, allocable and documented; progress and financial reports follow the award schedule. Also enacted by "
                   "local governments, universities and state agencies that receive awards [J].")),
    ],
))

# Task seeds superseded by consolidation (v1 key -> consolidated live task). Each consolidated task carries the merged-from
# derivedFrom entry (see 'merged' above) so X1 maps the v1 task key to it.
# v1 2.5.3 T1-T3 are rewritten and re-pointed to PS-C03 by WP-04 (DC owns the D2 row); WP-07 reviews their content only.
SUPERSEDED_TASKS = []
