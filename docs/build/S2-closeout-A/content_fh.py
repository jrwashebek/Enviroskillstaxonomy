"""S2 close-out A content, A7 FH rows: FH-C13 (absorbs IO-C02), FH-C14 (absorbs C-LM-06), CC-CM-02 (with CM; lifecycle
emerging), v1-5.3.4-B (split target; ADR-0016 naming). Sources: docs/research/federal-human-capital/ (report §2.1,
hr_use_cases.md (b) and (d)), docs/research/io-validation/, docs/research/mobility-workforce-voice/, verified key facts
V1-08 and V1-09 and the IO-022 correction (UGESP references removed from OPM hiring rules)."""
from s2adsl import T, I, E, WS, RA, SEW, BARS, SIM, PORT, C360, R, EN, C, X

ADR_FH = ["ADR-0003", "ADR-0004", "ADR-0016", "ADR-0017", "ADR-0023", "ADR-0030"]

COMPETENCIES = [
    # ------------------------------------------------------------------ FH-C13
    {
        "id": "seed:FH-C13", "agents": ["FH"], "adr": ADR_FH,
        "label": "Conduct job analyses and write job-related assessments for technical positions",
        "alt": ["job analysis", "crediting plan", "assessment benchmark", "subject-matter expert in hiring assessment",
                "structured interview questions", "technical assessment", "skills-based hiring"],
        "definition": "The capability, as a subject-matter expert, supervisor or hiring lead, to turn a technical "
                      "position's duties into a documented job analysis and into job-related assessment content "
                      "(proficiency benchmarks, crediting criteria, structured-interview questions with rating anchors and "
                      "work samples), and to rate applicants consistently against them. Designing and validating "
                      "assessment methods is the selection specialist's work and is referenced, not covered.",
        "statement": "Rates a position's tasks and competencies with other subject-matter experts and documents the job "
                     "analysis; writes proficiency benchmarks, crediting criteria, structured-interview questions with "
                     "rating anchors and work samples tied to it; rates applicants consistently against those criteria; "
                     "and reviews AI-drafted assessment content before it is adopted.",
        "span": ("L2", "L4"),
        "sources": ["FH-001", "FH-002", "FH-012", "FH-015", "FH-017", "FH-023", "IO-022", "IO-030", "IO-031", "IO-050",
                    "V1-09"],
        "editorial": "S2 close-out A (A7 FH; reviewer A8 IO). Survivor: absorbs IO-C02 (serve as a subject-matter expert in "
                     "merit-based hiring assessments; candidate_disposition.csv). Federal hiring now needs "
                     "position-specific technical assessments based on a job analysis, and self-assessment no longer "
                     "ranks applicants (from 2025-09-30), so line practitioners write and rate assessment content; in "
                     "FY2025 91 percent of delegated-examining announcements still relied on self-report only, and few "
                     "agencies employ selection specialists [E: FH-023, FH-002, FH-017, V1-09]. Job analysis remains "
                     "required after OPM removed the uniform-guidelines references from its hiring rules on 2026-07-31 "
                     "[E: IO-022]; 'UGESP compliance' is a register do-not-say form. AI may draft job analyses and "
                     "questions only under job-analysis requirements and human adoption [E: FH-015]. An EMST profile is "
                     "not a job analysis: SMEs adapt and rate it for the position (hr_use_cases.md (b)). Distinct from "
                     "CC-CM-02 (career translation for candidates; ADR-0030 §3.1) and from v1 5.3.4-B (merit-based "
                     "practice by the selecting official).",
        "sensitivity": [
            ("DM-16", "Hiring rules require position-specific technical assessments based on a job analysis and bar "
                      "self-assessment from ranking, so subject-matter experts write and rate assessment content.", "E",
             ["FH-023", "FH-002", "V1-09"]),
            ("DM-14", "Agency guidance lets AI draft job analyses and interview questions only under job-analysis "
                      "requirements and independent human review.", "E", ["FH-015"]),
        ],
        "tasks": [
            T("seed:fh-rate-position-tasks", "Rate the importance and frequency of a technical position's tasks with "
              "other subject-matter experts, linking each task to the competencies it requires", "WF-MANAGE",
              formation="partial"),
            T("seed:fh-write-proficiency-benchmark", "Write a proficiency benchmark describing qualified performance of a "
              "technical competency at the target grade band, drawn from the position's rated tasks", "WF-MANAGE",
              formation="yes"),
            T("seed:fh-write-interview-questions", "Write structured-interview questions with behavioural rating anchors for "
              "a technical competency, keying each question to rated tasks in the job analysis", "WF-MANAGE",
              formation="partial"),
            T("seed:fh-design-work-sample", "Design a work-sample exercise for a technical position, with a scoring key "
              "that the subject-matter experts agree on before it is used", "WF-MANAGE", formation="yes"),
            T("seed:fh-rate-applicants", "Rate applicants' experience records or interview responses against the benchmark "
              "and rating anchors, recording the evidence behind each rating", "WF-MANAGE", formation="partial"),
            T("seed:fh-calibrate-sme-ratings", "Calibrate ratings with the other subject-matter experts on sample applicant "
              "materials, resolving each discrepancy before the live applicant pool is rated", "WF-MANAGE",
              formation="partial"),
            T("seed:fh-review-ai-assessment-content", "Review AI-drafted job-analysis or assessment content against the "
              "position's duties, revising or rejecting each item before the subject-matter panel adopts it",
              "WF-MANAGE", formation="partial"),
        ],
        "levels": {
            "L2": [
                I("Rates a position's tasks for importance and frequency on the agency's scale and links each task to "
                  "competencies, with no task left unlinked in the job-analysis record.", RA + WS,
                  tasks=["seed:fh-rate-position-tasks"], evidence=["job-analysis rating sheet"]),
                I("Rates five calibration cases against a benchmark within one scale point of the expert-keyed rating on "
                  "at least four of them before rating live applicants.", WS,
                  tasks=["seed:fh-rate-applicants", "seed:fh-calibrate-sme-ratings"], evidence=["calibration record"],
                  critical=True),
                I("Records the evidence from each applicant's materials behind every rating, so that a second rater can "
                  "trace each score to its source.", RA, tasks=["seed:fh-rate-applicants"],
                  evidence=["rating record"]),
            ],
            "L3": [
                I("Writes a proficiency benchmark for a competency at a target grade band that the subject-matter panel "
                  "adopts without changing its job-related content.", WS + PORT, attr="ATT-AUT",
                  tasks=["seed:fh-write-proficiency-benchmark"], evidence=["benchmark"]),
                I("Writes structured-interview questions with a behavioural anchor for each rating point, each question "
                  "traceable to a rated task in the job analysis.", WS, attr="ATT-CPX",
                  tasks=["seed:fh-write-interview-questions"], evidence=["interview guide"]),
                I("Designs a work sample whose scoring key gives the same pass or fail result when two subject-matter "
                  "experts apply it to seeded responses.", WS, attr="ATT-KNO", tasks=["seed:fh-design-work-sample"],
                  evidence=["work sample", "scoring key"]),
                I("Reviews AI-drafted questions or benchmarks against the position's duties, logging each item revised or "
                  "rejected before panel adoption.", SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:fh-review-ai-assessment-content"], evidence=["review log"]),
            ],
            "L4": [
                I("Leads a subject-matter panel through the job analysis for a new or restructured position, resolving "
                  "rating disagreements and documenting the result as the job-analysis record.", PORT + RA,
                  attr="ATT-SCO", tasks=["seed:fh-rate-position-tasks", "seed:fh-calibrate-sme-ratings"],
                  evidence=["job-analysis record"]),
                I("Sets the assessment plan for a hiring action, assigning each critical competency to a measure and "
                  "stating why self-assessment is not used to rank applicants.", PORT, attr="ATT-GUI",
                  tasks=["seed:fh-write-proficiency-benchmark", "seed:fh-design-work-sample"],
                  evidence=["assessment plan"]),
                I("Coaches new subject-matter experts through calibration, reviewing each one's practice ratings against "
                  "the expert key before they rate live applicants.", PORT, attr="ATT-FOR", obs4=2,
                  tasks=["seed:fh-calibrate-sme-ratings"], evidence=["coaching record"]),
            ],
        },
        "enactments": [
            E("seed:ena-fh-c13-federal", "Federal subject-matter expert in technical assessment", "federal-agency",
              basis="Federal examining law as amended in 2024 (position-specific technical assessments based on a job "
                    "analysis); the 2025 merit hiring plan, under which self-assessment questionnaires may not rate and "
                    "rank applicants; the job-analysis requirement of 5 CFR 300.103, from which an interim final rule of "
                    "2026-07-31 removed the uniform-guidelines references; agency guidance on AI in hiring (2026-08-27).",
              principal="The hiring manager and the agency staffing or talent team, which owns the assessment.",
              venue="OPM oversight and delegated-examining audits; applicant complaints and appeals.",
              note="Shared certificates let other agencies reuse a certificate without reassessing, which raises the "
                   "value of common benchmarks across bureaus [E: FH-013].",
              links=[("opm-merit-hiring-plan", R, "Technical assessment and the end of self-assessment ranking."),
                     ("opm-ugesp-references-ifr", X, "Removed the uniform-guidelines references; the job-analysis "
                                                     "requirement remains. Never a basis."),
                     ("opm-ai-in-hiring-memo", C, "AI drafting stays subject to job analysis and human adoption.")],
              evidence="E", sources=["FH-023", "FH-002", "FH-012", "FH-013", "FH-015", "IO-022"]),
            E("seed:ena-fh-c13-state", "State or local merit-system examination", "state-agency",
              basis="State civil service and merit-system laws requiring job-related examinations; some states have "
                    "removed degree requirements from most positions.",
              principal="The state personnel agency or civil service commission, with the hiring unit's subject-matter "
                        "experts.",
              venue="Civil service commissions; state courts.",
              note="SL review: state examinations are often built centrally, with line experts reviewing items rather than "
                   "writing them [J].",
              links=[("tx-hb-3923", C, "Limits degree requirements in state hiring. Example state.")],
              sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ FH-C14
    {
        "id": "seed:FH-C14", "agents": ["FH"], "adr": ADR_FH,
        "label": "Justify positions and staffing with workload and mission evidence",
        "alt": ["position justification", "staffing plan", "workforce planning", "critical-skills risk register",
                "labour-market evidence in workforce plans", "vacancy request"],
        "definition": "The capability to show, with workload, statutory and plan requirements, critical-skill risk and "
                      "labour-market evidence, why a position or staffing level is needed, to choose between hiring and its "
                      "alternatives, and to defend the case before hiring committees and budget offices. Ranking or "
                      "selecting people for separation is excluded.",
        "statement": "Quantifies a unit's workload and its statutory and plan requirements, scores critical-skill risk, "
                     "reads labour-market and AI-exposure evidence with its limits, and writes position justifications and "
                     "staffing-plan entries a hiring committee or budget office can act on; chooses alternatives to hiring "
                     "where they fit; and defends each request under challenge.",
        "span": ("L3", "L5"),
        "sources": ["FH-006", "FH-008", "FH-029", "FH-030", "FH-045", "LM-001", "LM-008", "V1-08"],
        "editorial": "S2 close-out A (A7 FH; reviewer CM). Survivor: absorbs C-LM-06 (use labour-market and AI-change "
                     "evidence in workforce and training plans; candidate_disposition.csv). Since October 2025 a "
                     "strategic hiring committee approves the creation or filling of every federal vacancy and agencies "
                     "file annual staffing plans with quarterly updates from FY2026 Q2 [E: V1-08, FH-029]; every hire now "
                     "needs a competency-gap argument (hr_use_cases.md (d)). Risk scoring and supply counts are "
                     "unit-level aggregates; competitive levels and retention order for reductions in force follow "
                     "statute and regulation, never competency scores (excluded). Exposure scores are not job-loss "
                     "forecasts (C-LM-06).",
        "sensitivity": [
            ("DM-16", "Agency hiring committees approve each vacancy and annual staffing plans are required, so "
                      "supervisors must evidence need for every position.", "E", ["V1-08", "FH-029"]),
            ("DM-15", "Appropriations levels and rescissions of staffing funds set how many positions a programme can "
                      "sustain.", "J", None),
        ],
        "tasks": [
            T("seed:fh-quantify-unit-workload", "Quantify a unit's workload from caseloads, backlogs, statutory deadlines "
              "and plan-required monitoring, stating each data source and its limits", "WF-MANAGE", formation="partial"),
            T("seed:fh-score-critical-skill-risk", "Score critical-skill risk for a unit's competencies from criticality, "
              "scarcity, time to proficiency and the retirement eligibility of current holders", "WF-MANAGE",
              formation="partial"),
            T("seed:fh-write-position-justification", "Write a position justification citing the function, its statutory "
              "or plan basis, the competency gap and the consequence of leaving it unfilled", "WF-MANAGE",
              formation="partial"),
            T("seed:fh-prepare-staffing-plan-entry", "Prepare a programme's entries for the annual staffing plan, ranking "
              "requested positions by mission risk and stating the alternatives considered", "WF-RESOURCE",
              formation="partial"),
            T("seed:fh-interpret-labour-market-evidence", "Interpret labour-market, headcount and AI-exposure evidence for "
              "a workforce plan, stating why exposure scores are not forecasts of job loss", "WF-MANAGE",
              formation="no"),
            T("seed:fh-choose-staffing-alternative", "Choose between hiring, a detail, cross-training, partner delivery and "
              "a contract for each critical-skill gap, recording the reason for each choice", "WF-MANAGE",
              formation="partial"),
            T("seed:fh-defend-staffing-request", "Defend a staffing request before a hiring committee or budget office, "
              "answering each challenge with the workload and risk evidence", "WF-RESOURCE", formation="partial",
              modes=["MODE-RESOLVE"]),
        ],
        "levels": {
            "L3": [
                I("Writes a position justification citing the function, its basis, the competency gap and the "
                  "consequence of vacancy, accepted by the reviewing official without a request for more evidence.",
                  WS + RA, tasks=["seed:fh-write-position-justification"], evidence=["position justification"]),
                I("Quantifies a unit's workload from at least two independent data sources, stating each source's limits "
                  "in the workload table.", WS, tasks=["seed:fh-quantify-unit-workload"], evidence=["workload table"]),
                I("Flags each misreading of an exposure or posting measure in a seeded workforce-plan draft, including any "
                  "exposure score presented as a job-loss forecast.", SEW,
                  tasks=["seed:fh-interpret-labour-market-evidence"], evidence=["review notes"]),
            ],
            "L4": [
                I("Prepares a programme's staffing-plan entries ranked by mission risk, with an alternative to hiring "
                  "considered and recorded for each request.", WS + RA, attr="ATT-SCO",
                  tasks=["seed:fh-prepare-staffing-plan-entry", "seed:fh-choose-staffing-alternative"],
                  evidence=["staffing-plan entries"]),
                I("Scores critical-skill risk across a programme's units with a stated method, aggregated so that no "
                  "individual can be identified.", WS + RA, attr="ATT-CPX",
                  tasks=["seed:fh-score-critical-skill-risk"], evidence=["risk register"]),
                I("Defends a staffing request in a simulated committee review, answering each challenge with a figure "
                  "traceable to the workload and risk evidence.", SIM, attr="ATT-AUT",
                  tasks=["seed:fh-defend-staffing-request"], evidence=["simulation record"]),
            ],
            "L5": [
                I("Sets an organization's method for workload and critical-skill risk evidence, with criteria that units "
                  "apply in every annual staffing plan.", PORT, attr="ATT-GUI",
                  tasks=["seed:fh-quantify-unit-workload", "seed:fh-score-critical-skill-risk"],
                  evidence=["method standard"]),
                I("Reviews units' position justifications against the organization's method, returning each with the "
                  "evidence gaps to close before committee review.", RA, attr="ATT-FOR",
                  tasks=["seed:fh-write-position-justification"], evidence=["review comments"]),
            ],
        },
        "enactments": [
            E("seed:ena-fh-c14-federal", "Federal vacancy approval and annual staffing plan", "federal-agency",
              basis="An executive order of 2025-10-15 requires an agency strategic hiring committee to approve the "
                    "creation or filling of each vacancy and requires annual staffing plans with quarterly updates; OPM "
                    "staffing-plan guidance followed on 2026-07-30.",
              principal="The strategic hiring committee and the programme's approving official.",
              venue="OPM and OMB review of staffing plans; appropriations oversight.",
              note="The order sets no hiring ratio; an interim ratio applied through OPM and OMB guidance until plans "
                   "were filed [E: V1-08].",
              links=[("eo-14356-hiring-accountability", R, None),
                     ("obbba-ira-rescissions", C, "Rescinded unobligated staffing funds.")],
              evidence="E", sources=["V1-08", "FH-029", "FH-045"]),
            E("seed:ena-fh-c14-state", "State position control and budget request", "state-agency",
              basis="State budget acts and position-control rules administered by the state budget office; hiring freezes "
                    "by executive order in some states.",
              principal="The agency head and the state budget office.", venue="Legislative budget committees.",
              note="SL review: state position requests travel with the budget request, so the justification is written "
                   "for budget analysts as well as managers [J].", sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ CC-CM-02
    {
        "id": "seed:CC-CM-02", "agents": ["FH", "CM"], "adr": ADR_FH,
        "label": "Translate competencies and experience across sector-actor hiring systems",
        "alt": ["career translation", "skills translation", "experience crediting", "cross-sector career moves",
                "transferable skills", "public-private job translation"],
        "lifecycle": "emerging", "reviewBy": "2027-10-23",
        "definition": "The capability to express one's own or another person's competencies and experience in the terms a "
                      "different sector actor's hiring system credits (state class specifications, federal qualification "
                      "standards and specialized-experience language, private job architectures), with evidence its "
                      "assessors accept. Rating applicants inside a hiring system is a separate competency.",
        "statement": "Maps a person's competencies and experience to a target employer's classification, qualification or "
                     "job-architecture terms; marks which are credited, which need evidence and which are gaps; rewrites "
                     "the experience record against the target's requirements; assembles evidence assessors accept; and "
                     "states the basis and uncertainty of each equivalence claimed.",
        "span": ("L1", "L4"),
        "sources": ["CM-012", "CM-014", "CM-019", "FH-002", "V1-09"],
        "editorial": "S2 close-out A (A7 FH with CM; reviewer A2 IA for X11). Translation and crediting for people already "
                     "moving is the most urgent mobility job: 'what is my work called there, and does it count?' "
                     "(mobility report §2). Practitioners name articulation of skills in employers' terms as a barrier "
                     "[E: CM-012]; credential fluency gives a hiring advantage [E: CM-014]. Lifecycle emerging (review "
                     "2027-10-23): X11 public-private rows and the state class views are the reference translations; "
                     "pathways stay exploratory (ADR-0023). Kept separate from FH-C13 (hiring subject-matter experts) "
                     "because the users differ (ADR-0030 §3.1).",
        "sensitivity": [
            ("DM-16", "Skills-based hiring rules change what evidence counts: self-ratings no longer rank federal "
                      "applicants, and some states removed degree requirements.", "E", ["FH-002", "V1-09"]),
        ],
        "tasks": [
            T("seed:cm-map-target-requirements", "Map a person's competencies to a target position's classification or "
              "qualification requirements, marking each requirement as credited, needing evidence or a gap",
              "WF-MANAGE", formation="partial", lifecycle="emerging", reviewBy="2027-10-23"),
            T("seed:cm-rewrite-experience-record", "Rewrite an experience record for a target position so that each "
              "specialized-experience requirement is matched to described work with its dates, scope and results",
              "WF-MANAGE", formation="no", lifecycle="emerging", reviewBy="2027-10-23"),
            T("seed:cm-assemble-crediting-evidence", "Assemble the work products, credentials and supervisor statements "
              "that the target employer's assessors accept for each competency claimed", "WF-MANAGE",
              formation="no", lifecycle="emerging", reviewBy="2027-10-23"),
            T("seed:cm-translate-job-level", "Translate a job level in one sector actor's job architecture into the "
              "comparable grade band or class of another, stating the basis and its uncertainty", "WF-MANAGE",
              formation="partial", lifecycle="emerging", reviewBy="2027-10-23"),
            T("seed:cm-brief-assessment-method", "Brief a candidate on how a target hiring system will assess each claimed "
              "competency, so that the candidate prepares job-related evidence for it", "WF-MANAGE",
              formation="partial", lifecycle="emerging", reviewBy="2027-10-23"),
            T("seed:cm-build-translation-guide", "Build a translation guide between two sector actors' hiring terms for a "
              "recurring career move, checking each equivalence with the receiving employer", "WF-MANAGE",
              formation="partial", lifecycle="emerging", reviewBy="2027-10-23"),
        ],
        "levels": {
            "L1": [
                I("Marks each requirement of a target position as credited, needing evidence or a gap for a sample record, "
                  "matching the adviser's key on at least four of five requirements.", WS,
                  tasks=["seed:cm-map-target-requirements"], evidence=["requirements map"]),
                I("Rewrites a sample experience record so that every specialized-experience requirement of the target "
                  "position is matched to described work with dates and scope.", WS,
                  tasks=["seed:cm-rewrite-experience-record"], evidence=["rewritten record"]),
            ],
            "L2": [
                I("Assembles evidence for each claimed competency that a reviewing assessor accepts in a structured mock "
                  "review.", SIM + PORT, attr="ATT-AUT", tasks=["seed:cm-assemble-crediting-evidence"],
                  evidence=["evidence file"]),
                I("Identifies the requirements a target employer credits only with documented evidence, listing the "
                  "document needed for each.", WS, attr="ATT-KNO",
                  tasks=["seed:cm-map-target-requirements", "seed:cm-assemble-crediting-evidence"],
                  evidence=["evidence checklist"]),
            ],
            "L3": [
                I("Translates a job level between two sector actors' hiring systems for a candidate, stating the basis and "
                  "uncertainty, with the receiving employer's reviewer accepting the stated equivalence.", WS + PORT,
                  attr="ATT-CPX", tasks=["seed:cm-translate-job-level"], evidence=["translation memo"]),
                I("Briefs a candidate on how each claimed competency will be assessed in the target system, recording the "
                  "candidate's evidence plan for each.", SIM, attr="ATT-SCO", tasks=["seed:cm-brief-assessment-method"],
                  evidence=["evidence plan"]),
            ],
            "L4": [
                I("Builds a translation guide for a recurring career move, recording the receiving employer's confirmation "
                  "of each equivalence and the date it was last checked.", PORT, attr="ATT-GUI",
                  tasks=["seed:cm-build-translation-guide"], evidence=["translation guide"]),
                I("Coaches career advisers or corps staff through translating sample records, reviewing each translation "
                  "against the guide before they advise candidates.", PORT, attr="ATT-FOR", obs4=2,
                  tasks=["seed:cm-build-translation-guide", "seed:cm-rewrite-experience-record"],
                  evidence=["coaching record"]),
            ],
        },
    },
    # ------------------------------------------------------------------ v1-5.3.4-B
    {
        "id": "seed:v1-5.3.4-B", "agents": ["FH"], "adr": ADR_FH,
        "label": "Apply merit-based, job-related practices in recruitment and team management",
        "alt": ["diversity, equity and inclusion practices", "DEI", "fair hiring", "barrier removal in recruitment",
                "inclusive team management", "equal employment opportunity", "skills-based hiring"],
        "definition": "The capability of a supervisor or hiring lead to recruit, select, assign, develop and recognize staff "
                      "by job-related criteria applied the same way to everyone; to find and remove recruitment and "
                      "workplace barriers that are not job-related; to provide requested accommodations; and to check "
                      "outcomes for any stage where the criteria were not applied consistently. Writing assessment content "
                      "and general supervision are separate competencies.",
        "statement": "Recruits through sources that reach qualified applicants the unit has not reached, removes "
                     "requirements and barriers that are not job-related, applies the same job-related criteria to every "
                     "applicant and team member in selection, assignments, development and recognition, arranges "
                     "requested accommodations, and reviews outcomes for any stage where criteria were applied "
                     "inconsistently.",
        "span": ("L2", "L4"),
        "derived": [("v1:5.3.4", "split-from")],
        "sources": ["FH-002", "FH-011", "FH-012", "IO-022", "IO-030", "V1-09"],
        "editorial": "S2 close-out A (A7 FH; reviewers A8 IO and CP). Split target B of v1 5.3.4 (split with v1-5.3.4-A). "
                     "Named by the work performed under ADR-0016's uniform rule; DEI is a search alias only. Its content "
                     "is federally required where it is merit-based and job-related (the merit hiring plan) and its "
                     "removed instruments are linked as removed-requirement, so the computed federal value comes from "
                     "typed links (venue-applicability@1.0.0), not from a label. Boundaries: FH-C13 writes the assessment "
                     "content; v1 3.3.1 is general supervision; v1 5.3.4-A covers the public side.",
        "sensitivity": [
            ("DM-16", "Merit-hiring rules, the removal of the uniform-guidelines references and the rescission of the "
                      "contractor affirmative-action rules change which practices are required, permitted or removed "
                      "for federal employers and contractors.", "E", ["IO-022", "FH-012"]),
        ],
        "tasks": [
            T("seed:v1-5.3.4-T2", "Widen recruitment outreach to sources that reach qualified applicants the unit has not "
              "reached, recording where each applicant learned of the vacancy", "WF-MANAGE", formation="no",
              derived=[("v1:5.3.4:T2", "rewritten")]),
            T("seed:v1-5.3.4-T3", "Review recruitment, selection and promotion outcomes stage by stage, identifying any "
              "stage where the job-related criteria were not applied consistently", "WF-MANAGE", formation="no",
              derived=[("v1:5.3.4:T3", "rewritten")]),
            T("seed:fh-remove-non-job-requirements", "Remove qualification requirements that the job analysis does not "
              "support, such as a degree where demonstrated competency suffices, before a vacancy is announced",
              "WF-MANAGE", formation="no"),
            T("seed:fh-document-selection-reasons", "Document the job-related reasons for a selection decision so that "
              "every applicant considered is compared on the same criteria", "WF-MANAGE", formation="no"),
            T("seed:fh-assign-by-stated-criteria", "Assign work, development opportunities and recognition within a team "
              "using stated job-related criteria, recording the basis for each assignment", "WF-MANAGE",
              formation="partial"),
            T("seed:fh-arrange-accommodation", "Arrange a requested accommodation in the application process or workplace, "
              "recording the request, the adjustment made and the date it was made", "WF-MANAGE", formation="no"),
        ],
        "levels": {
            "L2": [
                I("Applies the unit's job-related criteria to every applicant in a selection simulation and documents the "
                  "reason for the choice against those criteria.", SIM + RA,
                  tasks=["seed:fh-document-selection-reasons"], evidence=["selection record"]),
                I("Arranges a requested accommodation in a seeded case within the organization's response time, recording "
                  "the request and the adjustment made.", WS, tasks=["seed:fh-arrange-accommodation"],
                  evidence=["accommodation record"]),
                I("Records the basis for each work assignment and development opportunity in a team over a review period, "
                  "using stated job-related criteria.", RA, tasks=["seed:fh-assign-by-stated-criteria"],
                  evidence=["assignment log"]),
            ],
            "L3": [
                I("Identifies the requirements in a draft vacancy announcement that the job analysis does not support, "
                  "stating the job-related alternative for each.", SEW, attr="ATT-KNO",
                  tasks=["seed:fh-remove-non-job-requirements"], evidence=["annotated announcement"]),
                I("Reviews a hiring cycle's outcomes stage by stage and names any stage where criteria were applied "
                  "inconsistently, with the corrective step for each.", WS, attr="ATT-CPX",
                  tasks=["seed:v1-5.3.4-T3"], evidence=["outcome review"]),
                I("Plans recruitment outreach for a vacancy that reaches sources the unit has not reached, recording where "
                  "applicants learned of it.", WS + RA, attr="ATT-SCO", tasks=["seed:v1-5.3.4-T2"],
                  evidence=["outreach plan", "source log"]),
            ],
            "L4": [
                I("Sets the organization's recruitment and selection procedures so that every stage uses criteria "
                  "traceable to a job analysis, with an annual review of outcomes.", PORT, attr="ATT-GUI",
                  tasks=["seed:fh-remove-non-job-requirements", "seed:v1-5.3.4-T3"], evidence=["procedure"]),
                I("Coaches supervisors through documenting job-related selection and assignment decisions, reviewing each "
                  "record against the procedure.", PORT, attr="ATT-FOR", obs4=2,
                  tasks=["seed:fh-document-selection-reasons", "seed:fh-assign-by-stated-criteria"],
                  evidence=["coaching record"]),
            ],
        },
        "enactments": [
            E("seed:ena-v1-5-3-4-b-federal", "Federal merit-based hiring and supervision", "federal-agency",
              basis="Merit system principles and federal examining law (job-related, position-specific assessment); the "
                    "2025 merit hiring plan; job analysis under 5 CFR 300.103 after the 2026 interim rule removed the "
                    "uniform-guidelines references; reasonable-accommodation duties under federal disability law. "
                    "Executive orders of January 2025 ended agency programmes under the DEI label and revoked the "
                    "contractor affirmative-action order.",
              principal="The selecting official and the agency human capital office.",
              venue="OPM oversight; the Merit Systems Protection Board; equal employment opportunity complaint processes.",
              note="ADR-0016: applicability is computed from typed links. Merit-based, job-related practice has a current "
                   "federal basis; the removed programmes are linked only as removed-requirement.",
              links=[("opm-merit-hiring-plan", R, "Merit-based, job-related assessment."),
                     ("opm-ugesp-references-ifr", X, "Removed the uniform-guidelines references; never a basis."),
                     ("eo-14173", X, "Ended programmes under the DEI label and revoked the contractor affirmative-action "
                                     "order; never a basis.")],
              evidence="E", sources=["FH-012", "IO-022", "IO-030"]),
            E("seed:ena-v1-5-3-4-b-private", "Private employer or federal contractor", "firm",
              basis="Federal and state anti-discrimination law and employer policy; for federal contractors, the "
                    "affirmative-action regulations under the revoked order were rescinded in 2026.",
              principal="The hiring manager and human resources.",
              venue="Federal and state civil-rights agencies; courts.",
              note="No requires link is registered for the private family yet, so the view reads 'basis not yet linked'.",
              links=[("ofccp-eo11246-regs-rescission", X, "Rescinded the contractor affirmative-action regulations; "
                                                          "never a basis."),
                     ("eo-14173", X, "Revoked the contractor affirmative-action order; never a basis.")],
              evidence="J"),
            E("seed:ena-v1-5-3-4-b-state", "State merit system", "state-agency",
              basis="State civil service and merit-system laws; state statutes and orders on skills-based hiring, for "
                    "example a 2025 Texas law limiting degree requirements in state hiring.",
              principal="The state personnel agency and the hiring unit.", venue="Civil service commissions; state courts.",
              note="SL review: state merit systems already require job-related selection; skills-based hiring laws add "
                   "the removal of unneeded degree requirements [J].",
              links=[("tx-hb-3923", R, "Example state.")], sl_reviewed=True),
        ],
    },
]
