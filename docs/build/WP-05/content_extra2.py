"""WP-05 content: remaining SC-primary core rows used by P1 corridor COR-3 (R13 resource programme manager, R10, R09):
v1 6.1.1 (absorbs 6.4.1), v1 6.2.3, SL-C12 (funder position)."""
from wp05dsl import T, I, E

WS = ["work-sample"]
RA = ["record-audit"]
SEW = ["seeded-error-work-sample"]
BARS = ["structured-interview-bars"]
PORT = ["portfolio-review"]
KT = ["knowledge-test"]
MOOT = ["moot-defense"]

COMPETENCIES = [
    # ------------------------------------------------------------------ v1 6.1.1 (absorbs 6.4.1)
    {
        "id": "seed:v1-6.1.1",
        "label": "Analyze environmental policies and policy options",
        "alt": ["environmental policy analysis", "policy research and analysis", "legal and policy comparison"],
        "definition": "The capability to analyze existing and proposed environmental policies, laws and administrative "
                      "proposals for their requirements, effects, burdens and alternatives, and to present options and "
                      "trade-offs decision-makers can act on. Economic estimation of effects is a separate competency.",
        "statement": "Analyzes existing and proposed environmental policies, laws and administrative proposals for their "
                     "requirements, effects, implementation burdens and alternatives, compares how jurisdictions treat "
                     "the same issue, and summarizes options and trade-offs in work products decision-makers can act on.",
        "span": ("L1", "L4"),
        "derived": [("v1:6.4.1", "merged-from")],
        "sources": ["SC-004"],
        "editorial": "WP-05 (A5 SC). v1 6.1.1 rewrite; absorbs 6.4.1 (policy research and analysis, merged). The "
                     "codifiable tasks through which juniors learned the law (legal comparison, literature review) were "
                     "coded substitution in v1 [E: SC-004]; the entry task becomes supervised verification of "
                     "AI-generated comparisons, kept as a formation task (ADR-0026). No agency inventory reports AI as "
                     "the principal basis for policy comparison (DC needs-evidence).",
        "sensitivity": [
            ("DM-14", "AI legal and policy comparison compresses entry analysis tasks.", "E", ["SC-004", "SC-009"]),
            ("DM-10", "Substantive standards under analysis changed in 2025-26.", "E", ["V2-05", "V2-06"]),
        ],
        "tasks": [
            T("seed:v1-6.1.1-T1", "Review existing policies against a program's conservation or regulatory objectives, "
              "documenting each gap or conflict found",
              "WF-RULE", formation="partial", derived=[("v1:6.1.1:T1", "rewritten")]),
            T("seed:v1-6.1.1-T2", "Compare federal, state and local requirements affecting a project area, recording where "
              "they overlap, conflict or leave gaps",
              "WF-RULE", formation="yes", derived=[("v1:6.1.1:T2", "rewritten")],
              note="Formation task: entry analysts learn the law here; keep a by-hand share when AI drafts comparisons."),
            T("seed:v1-6.1.1-T3", "Prepare a policy brief summarizing the legal and policy considerations for a decision, "
              "citing each source relied on",
              "WF-RULE", formation="partial", derived=[("v1:6.1.1:T3", "rewritten")]),
            T("seed:v1-6.4.1-T1", "Review policy literature and case studies to inform a management strategy, stating the "
              "quality of the evidence behind each finding",
              "WF-RULE", formation="no", derived=[("v1:6.4.1:T1", "rewritten")]),
            T("seed:v1-6.4.1-T2", "Analyze an administrative or legislative proposal for its environmental and operational "
              "implications, listing each provision's likely effect",
              "WF-RULE", formation="partial", derived=[("v1:6.4.1:T2", "rewritten")]),
            T("seed:v1-6.4.1-T3", "Summarize policy options and trade-offs for decision-makers in a briefing document, "
              "stating the evidence and uncertainty for each option",
              "WF-RULE", modes=["MODE-ENGAGE"], formation="partial", derived=[("v1:6.4.1:T3", "rewritten")]),
            T("seed:sc-verify-ai-policy-comparison", "Verify an AI-generated legal or policy comparison against the source "
              "texts, correcting each misstatement before the comparison is used",
              "WF-RULE", formation="yes"),
        ],
        "levels": {
            "L1": [
                I("Summarizes the requirements of an assigned policy or law against its source text in a seeded test, "
                  "citing each provision relied on.", KT + WS, tasks=["seed:v1-6.1.1-T1"], evidence=["summary"]),
                I("Checks an AI-generated comparison of requirements against the source texts, flagging each misstatement "
                  "before the comparison is used.", SEW, mode="assisted", tasks=["seed:sc-verify-ai-policy-comparison"],
                  evidence=["annotated comparison"]),
            ],
            "L2": [
                I("Compares how federal, state and local requirements treat one issue for a project area, recording each "
                  "overlap, conflict and gap with citations.", WS, attr="ATT-AUT", tasks=["seed:v1-6.1.1-T2"],
                  evidence=["comparison table"]),
                I("Writes a policy brief stating options, evidence and trade-offs for a routine decision, accepted by the "
                  "supervisor without restructuring.", WS, attr="ATT-KNO", tasks=["seed:v1-6.4.1-T3"],
                  evidence=["policy brief"]),
            ],
            "L3": [
                I("Analyzes an administrative or legislative proposal with uncertain or contested effects, stating the "
                  "likely effect of each provision and the evidence behind it.", WS + BARS, attr="ATT-CPX",
                  tasks=["seed:v1-6.4.1-T2"], evidence=["analysis memo"]),
                I("Reviews analysts' AI-assisted policy comparisons, setting the share of statements checked against "
                  "source texts and recording each correction.", RA + SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:sc-verify-ai-policy-comparison"], evidence=["review log"]),
            ],
            "L4": [
                I("Sets a program's policy-analysis standards, including source verification, evidence grading and option "
                  "presentation, for analysts to apply.", PORT, attr="ATT-GUI", tasks=["seed:v1-6.1.1-T3"],
                  evidence=["analysis standard"]),
                I("Designs supervised exercises in which entry analysts learn the law by checking AI-generated comparisons "
                  "against source texts, with the review steps each exercise requires.", PORT, attr="ATT-FOR",
                  mode="supervisory", tasks=["seed:v1-6.1.1-T2"], evidence=["exercise design"]),
            ],
        },
        "enactments": [],
    },
    # ------------------------------------------------------------------ v1 6.2.3
    {
        "id": "seed:v1-6.2.3",
        "label": "Prepare and revise management plans for publicly held lands",
        "alt": ["public land management planning", "forest plan revision", "resource management plan",
                "refuge comprehensive conservation plan"],
        "definition": "The capability to prepare, amend and revise management plans for publicly held lands and waters "
                      "under the governing planning procedure, writing plan components that later projects can be checked "
                      "against and carrying the plan through review, objection and approval. Comprehensive local "
                      "land-use planning is a module competency.",
        "statement": "Leads or contributes to the preparation, amendment and revision of management plans for publicly "
                     "held lands and waters under the governing planning procedure: frames desired conditions, objectives, "
                     "standards and monitoring, integrates interdisciplinary analysis and public input, and carries the "
                     "plan through review, objection and approval.",
        "span": ("L1", "L4"),
        "derived": [],
        "sources": ["SC-009"],
        "editorial": "WP-05 (A5 SC). v1 6.2.3 rewrite; recurs in forest, parks and wildlife-refuge modules (G-4). "
                     "Rewritten for 2026 procedures (some plan amendments may be categorically excluded; objection "
                     "windows shortened) as regulation-neutral text [J; SC verdict]. Plan components are a standing "
                     "demand signal (OpenLMP plan requirements, ADR-0028 section 4). v1 T3 named equity; renamed by the "
                     "work performed (effects on communities) under ADR-0016.",
        "sensitivity": [
            ("DM-03", "Some plan amendments may now be categorically excluded from full review.", "J", None),
            ("DM-02", "Objection and comment windows were shortened.", "E", ["SC-009"]),
            ("DM-10", "Rescission of land-use restrictions changes plan baselines.", "J", None),
        ],
        "tasks": [
            T("seed:v1-6.2.3-T1", "Coordinate an interdisciplinary team drafting a forest, range or refuge management plan, "
              "assigning plan components and reconciling conflicting resource objectives",
              "WF-PLAN", formation="yes", profiles=["WP-PROJECT"], derived=[("v1:6.2.3:T1", "rewritten")]),
            T("seed:v1-6.2.3-T2", "Follow the agency's planning procedure and schedule for a plan revision or amendment, "
              "documenting each required step and its completion",
              "WF-PLAN", formation="partial", derived=[("v1:6.2.3:T2", "rewritten")]),
            T("seed:v1-6.2.3-T3", "Incorporate climate, wildfire and community-effect considerations into a plan revision, "
              "stating the evidence behind each affected plan component",
              "WF-PLAN", formation="yes", derived=[("v1:6.2.3:T3", "rewritten")]),
            T("seed:sc-write-plan-components", "Write plan components such as desired conditions, objectives, standards "
              "and monitoring questions so that later projects can show consistency with them",
              "WF-PLAN", formation="yes"),
            T("seed:sc-resolve-plan-objections", "Resolve objections to a draft plan decision within the objection window, "
              "documenting each issue, the response and any change made to the plan",
              "WF-PLAN", modes=["MODE-RESOLVE"], rel=["public"], formation="partial"),
        ],
        "levels": {
            "L1": [
                I("Drafts a plan component for one resource under a supervisor's direction, stated in measurable terms "
                  "that pass the plan's consistency checklist.", WS, tasks=["seed:sc-write-plan-components"],
                  evidence=["draft component"]),
                I("Logs public and partner input on a plan revision so that every comment sampled in audit is traceable to "
                  "its source and disposition.", RA, tasks=["seed:v1-6.2.3-T2"], evidence=["comment log"]),
            ],
            "L2": [
                I("Writes desired conditions, objectives and standards for a resource area that later projects can be "
                  "checked against, accepted by the plan team leader.", WS, attr="ATT-AUT",
                  tasks=["seed:sc-write-plan-components"], evidence=["plan components"]),
                I("Documents completion of each step the planning procedure requires for a plan amendment, with dates and "
                  "decision records.", RA, attr="ATT-KNO", tasks=["seed:v1-6.2.3-T2"], evidence=["procedure log"]),
            ],
            "L3": [
                I("Leads an interdisciplinary plan team through a revision, reconciling conflicting resource objectives "
                  "into plan components the responsible official approves.", PORT + BARS, attr="ATT-CPX",
                  tasks=["seed:v1-6.2.3-T1"], evidence=["revision record"]),
                I("Resolves objections to a draft plan decision within the objection window, documenting each issue, the "
                  "response and any change to the plan.", RA + MOOT, attr="ATT-SCO",
                  tasks=["seed:sc-resolve-plan-objections"], evidence=["objection responses"]),
            ],
            "L4": [
                I("Designs a plan's monitoring program and amendment triggers, linking each monitoring question to the plan "
                  "components it evaluates.", PORT, attr="ATT-GUI", tasks=["seed:sc-write-plan-components"],
                  evidence=["monitoring program"]),
                I("Evaluates plan team leaders' revision files against program standards before granting them "
                  "responsibility for a revision.", RA, attr="ATT-FOR", tasks=["seed:v1-6.2.3-T1"],
                  evidence=["evaluation record"]),
            ],
        },
        "enactments": [
            E("seed:ena-v1-6-2-3-federal", "Federal land management planning", "federal-land-manager",
              position="resource-manager",
              basis="Land-management planning statutes and each agency's planning regulations and directives (forest "
                    "plans, resource management plans, refuge conservation plans); agency environmental-review "
                    "procedures, including exclusions for some amendments; objection rules.",
              principal="The responsible official (forest supervisor, state director or refuge manager).",
              venue="Objection reviewing officers; federal courts.",
              note="Objection windows and review levels for plans changed with the 2025-26 procedure revisions [J; "
                   "E: SC-009 for the objection rule].",
              instruments=["usfs-objection-rule", "usda-nepa-procedures", "doi-nepa-procedures",
                           "roadless-rule-rescission"], evidence="E", sources=["SC-009"]),
            E("seed:ena-v1-6-2-3-state", "State forest, wildlife and trust-land planning", "state-agency",
              position="resource-manager",
              basis="State statutes for state forest management plans, state wildlife action plans and trust-land "
                    "management plans.",
              principal="The state forester, wildlife director or land board.", venue="State courts; legislature.",
              note="SL review: state plans often carry revenue duties to trust beneficiaries alongside resource "
                   "objectives [J].", sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ SL-C12
    {
        "id": "seed:SL-C12",
        "label": "Administer environmental financial assistance to local governments",
        "alt": ["state revolving fund administration", "environmental grants and loans", "infrastructure financial assistance"],
        "definition": "The capability of a funding agency to run grant, loan and revolving-fund programmes that finance "
                      "local environmental infrastructure and resilience projects, from eligibility and priority setting "
                      "through technical and financial review, cross-cutting requirements, monitoring and closeout. "
                      "Applying for funds is a separate competency.",
        "statement": "Runs grant, loan and revolving-fund programs that finance local water, wastewater, stormwater, solid "
                     "waste and resilience projects: sets eligibility and priority systems, reviews applications "
                     "technically and financially, applies the cross-cutting requirements attached to awards, monitors "
                     "performance and closes out awards.",
        "span": ("L1", "L4"),
        "sources": [],
        "editorial": "WP-05 (A5 SC; SL candidate). Financial assistance to local governments recurs in water, waste, "
                     "hazards and climate modules (G-4) and had no v1 home [J; SL report, not evidenced this session]. "
                     "Funder authority position (ADR-0017). Programme names (state revolving funds) are altLabels; "
                     "capitalization grants and cross-cutting requirements are L5 instruments to register.",
        "sensitivity": [
            ("DM-19", "Programme funding is created, cut or reinstated through appropriations.", "J", None),
            ("DM-15", "Loan repayments, fees and set-asides fund programme administration.", "J", None),
        ],
        "tasks": [
            T("seed:sc-rank-funding-applications", "Rank local project applications on the program's priority list using "
              "the published scoring criteria, documenting the basis for each score",
              "WF-RESOURCE", formation="partial", rel=["intergovernmental"]),
            T("seed:sc-review-funding-feasibility", "Review a funding application's technical and financial feasibility, "
              "recording the conditions the applicant must meet before award",
              "WF-RESOURCE", formation="yes"),
            T("seed:sc-verify-award-crosscutters", "Verify that a funded project meets the cross-cutting requirements "
              "attached to its award, listing each requirement and its evidence",
              "WF-RESOURCE", formation="partial"),
            T("seed:sc-monitor-award-disbursements", "Monitor funded projects' disbursements and milestones, withholding "
              "payment where required documentation or performance is missing",
              "WF-RESOURCE", formation="no"),
            T("seed:sc-close-out-award", "Close out a financial assistance award, reconciling final costs, outcomes and "
              "compliance records against the award terms",
              "WF-RESOURCE", formation="no"),
        ],
        "levels": {
            "L1": [
                I("Checks a funding application for eligibility and completeness against the program checklist, listing "
                  "each missing item for the applicant.", WS + RA, tasks=["seed:sc-rank-funding-applications"],
                  evidence=["checklist"]),
                I("Reconciles disbursement requests against award terms and documentation, referring each discrepancy to "
                  "the program manager before payment.", RA, tasks=["seed:sc-monitor-award-disbursements"],
                  evidence=["reconciliation log"]),
            ],
            "L2": [
                I("Scores local project applications with the program's priority criteria so that a second reviewer "
                  "reproduces each score within tolerance.", WS, attr="ATT-AUT",
                  tasks=["seed:sc-rank-funding-applications"], evidence=["score sheets"]),
                I("Documents the evidence for each cross-cutting requirement attached to an award, with no requirement "
                  "left without evidence at closeout audit.", RA, attr="ATT-KNO",
                  tasks=["seed:sc-verify-award-crosscutters"], evidence=["requirement file"]),
            ],
            "L3": [
                I("Resolves a non-routine funding case such as a financially distressed applicant or a scope change, "
                  "documenting the conditions set and their legal basis.", WS + BARS, attr="ATT-CPX",
                  tasks=["seed:sc-review-funding-feasibility"], evidence=["case memo"]),
                I("Reviews technical feasibility findings prepared by staff engineers, returning each with the deficiencies "
                  "to resolve before award.", RA, attr="ATT-SCO", tasks=["seed:sc-review-funding-feasibility"],
                  evidence=["review comments"]),
            ],
            "L4": [
                I("Designs the program's priority-ranking system and annual use plan, with criteria and weights opened to "
                  "the overseeing agency's review and public comment.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-rank-funding-applications"], evidence=["ranking system", "use plan"]),
                I("Evaluates program staff's award files against program standards before granting them authority to "
                  "approve disbursements.", RA, attr="ATT-FOR", tasks=["seed:sc-close-out-award"],
                  evidence=["evaluation record"]),
            ],
        },
        "enactments": [
            E("seed:ena-sl-c12-state-funder", "State financial assistance program", "state-agency", position="funder",
              basis="State revolving-fund and grant statutes; federal capitalization grants with their cross-cutting "
                    "requirements; state bond authority.",
              principal="The state agency head or financing authority board.",
              venue="Federal programme reviews; state audits; legislative oversight.",
              note="SL review: state staff run eligibility, priority lists and closeout for hundreds of local "
                   "recipients; small systems need structured assistance to apply [J].",
              instruments=["fy2026-interior-approps"], sl_reviewed=True),
            E("seed:ena-sl-c12-federal-overseer", "Federal oversight of state financial assistance", "federal-regulator",
              position="funder",
              basis="Capitalization grant agreements and programme oversight of state funds.",
              principal="The regional programme office.", venue="Federal audits; Congress.",
              note="Mirror of the state funder enactment one level up [J].", instruments=["fy2026-interior-approps"]),
        ],
    },
]
