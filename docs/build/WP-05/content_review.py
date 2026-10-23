"""WP-05 content: environmental review cluster (SL-C08, SC-C03, SC-C04, SC-C09, DB-C50, DB-C52, FH-C01).

Text rules: regulation-neutral L1/L2 text (instruments only in enactments and L5); no Tribal content outside held
records (Tribal enactments are reserved for TN under ADR-0007 section D and are not authored here).
Evidence: [J] SC/SL judgment unless sources are listed; sensitivity edges cite V2 verified facts.
"""
from wp05dsl import T, I, E

WS = ["work-sample"]
RA = ["record-audit"]
SEW = ["seeded-error-work-sample"]
BARS = ["structured-interview-bars"]
SIM = ["simulation-role-play"]
MOOT = ["moot-defense"]
PORT = ["portfolio-review"]
KT = ["knowledge-test"]
TB = ["task-book-observation"]

COMPETENCIES = [
    # ------------------------------------------------------------------ SL-C08
    {
        "id": "seed:SL-C08",
        "label": "Conduct environmental impact review of proposed actions",
        "alt": ["environmental review", "NEPA review", "state environmental policy act review",
                "CEQA, SEPA, MEPA or SEQR review", "environmental assessment and impact statement preparation"],
        "definition": "The capability to scope, prepare or direct, and conclude the analysis of a proposed action's "
                      "reasonably foreseeable environmental effects and alternatives under the review procedures that "
                      "govern the deciding agency, so that the decision record shows the effects were considered. "
                      "Excludes choosing the level of review, consultation on protected species and historic-property "
                      "review, which are separate competencies.",
        "statement": "Scopes, prepares or directs, and concludes the environmental review of a proposed action under the "
                     "procedures that govern the deciding agency: defines purpose, alternatives and effects boundaries, "
                     "integrates interdisciplinary analysis, keeps within page and time limits, and documents how "
                     "effects were considered in the decision.",
        "span": ("L1", "L4"),
        "derived": [("v1:6.1.4", "split-from")],
        "sources": ["SC-011", "SC-012", "SC-014", "SC-038", "SL-070", "SL-038", "V2-01", "V2-02", "V2-04"],
        "editorial": "WP-05 (A5 SC; SL reviewed the state and local enactments). Successor of v1 6.1.4 (split with "
                     "SC-C03); written regulation-neutral after removal of the government-wide NEPA regulations "
                     "(final 2026-01-08) so that agency-specific and state procedures attach as enactments and L5 "
                     "instruments [E: V2-01]. Production tasks are split from AI-assisted review tasks (G-2). Tribal "
                     "environmental-review enactment reserved for TN under the hold. Basis [J]: SC report sections 4-5, "
                     "SL report section 2(a,d).",
        "sensitivity": [
            ("DM-01", "Review scope narrowed by the 2025 Supreme Court decision and department procedures.", "E", ["V2-01", "V2-02"]),
            ("DM-02", "Statutory page and time limits and sponsor-paid acceleration change how reviews are scheduled.", "E", ["V2-04"]),
            ("DM-04", "Public involvement for lower levels of review became discretionary under department procedures.", "E", ["SC-038"]),
            ("DM-05", "Lead and cooperating agency rules codified in statute.", "E", ["V2-01"]),
            ("DM-08", "Deference and remedy doctrine set how much analysis the record needs.", "E", ["V2-02", "V2-03"]),
            ("DM-14", "Digital-first documents, data standard and AI drafting tools change production.", "E", ["V2-08"]),
        ],
        "tasks": [
            T("seed:v1-6.1.4-T1", "Prepare an environmental assessment of a proposed action, analyzing the reasonably "
              "foreseeable effects of the action and its alternatives within the procedure's page and time limits",
              "WF-REVIEW", profiles=["WP-PROJECT"], derived=[("v1:6.1.4:T1", "rewritten")],
              regime={"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "general", "currencyDecay": "M"}),
            T("seed:v1-6.1.4-T2", "Scope the review of a proposed action with cooperating agencies and the public, setting "
              "the purpose, alternatives and effects boundaries the analysis will cover",
              "WF-REVIEW", modes=["MODE-ENGAGE"], rel=["public", "intergovernmental"], profiles=["WP-PROJECT"],
              derived=[("v1:6.1.4:T2", "rewritten")]),
            T("seed:v1-6.1.4-T3", "Lead an interdisciplinary team through an environmental review, assigning resource "
              "analyses and reconciling conflicting findings into one effects analysis",
              "WF-REVIEW", profiles=["WP-PROJECT"], formation="yes", derived=[("v1:6.1.4:T3", "rewritten")]),
            T("seed:sc-review-ai-drafted-sections", "Verify AI-drafted sections of an environmental document against the "
              "project record, correcting unsupported statements and recording which text was machine-drafted",
              "WF-REVIEW", formation="yes", profiles=["WP-PROJECT"],
              note="Specification/review counterpart of the production task (G-2); AI drafting tools for review "
                   "documents are in production or beta [E: SC-009]."),
            T("seed:sc-write-review-decision", "Write the decision document for a reviewed action, explaining how the "
              "analyzed effects, alternatives and public comments informed the choice made",
              "WF-REVIEW", profiles=["WP-PROJECT"], accountable="The decision is signed by an accountable official; "
              "courts defer to that official's reasoned explanation."),
            T("seed:sc-joint-review-document", "Prepare a joint environmental review document that satisfies both state and "
              "federal review procedures for one action, mapping each procedural requirement to its section",
              "WF-REVIEW", profiles=["WP-PROJECT"]),
        ],
        "levels": {
            "L1": [
                I("Compiles the affected-environment section for one resource from assigned sources under a reviewer's "
                  "direction, citing every source used.", WS + RA, tasks=["seed:v1-6.1.4-T1"],
                  evidence=["draft section", "source list"]),
                I("Flags each factual statement in an AI-drafted resource section that lacks a source in the project "
                  "record before the section goes to the reviewer.", SEW, mode="assisted",
                  tasks=["seed:sc-review-ai-drafted-sections"], evidence=["annotated draft", "verification log"]),
            ],
            "L2": [
                I("Prepares an environmental assessment for a routine action within the procedure's page and time limits, "
                  "accepted by the responsible official without substantive rework.", WS + PORT, attr="ATT-AUT",
                  tasks=["seed:v1-6.1.4-T1"], evidence=["environmental assessment", "review comments"]),
                I("Defines the alternatives and effects boundaries for a routine review and records the reason each "
                  "excluded effect or alternative falls outside the analysis.", WS, attr="ATT-GUI",
                  tasks=["seed:v1-6.1.4-T2"], evidence=["scoping record"]),
                I("Verifies AI-drafted sections of an environmental document against the project record, correcting or "
                  "removing each unsupported statement and logging the change.", SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:sc-review-ai-drafted-sections"], evidence=["verification log"]),
            ],
            "L3": [
                I("Leads the review of a contested or multi-agency action, reconciling conflicting resource findings into "
                  "one effects analysis that counsel accepts as defensible.", PORT + BARS, attr="ATT-CPX",
                  tasks=["seed:v1-6.1.4-T3"], evidence=["effects analysis", "counsel review memo"]),
                I("Adapts a review when the governing procedure changes mid-review, documenting which procedure version "
                  "applies to each step without restarting completed analysis.", BARS + RA, attr="ATT-GUI",
                  tasks=["seed:v1-6.1.4-T1"], obs4=2, evidence=["procedure-version log"]),
                I("Reviews other analysts' AI-assisted drafts for a review team, setting the share of statements checked "
                  "against sources and recording each rejection reason.", RA + SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:sc-review-ai-drafted-sections"], evidence=["sampling plan", "rejection log"]),
            ],
            "L4": [
                I("Sets review templates, effects-analysis standards and quality checks for an agency program, revising "
                  "them when procedures or case law change.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-write-review-decision"], evidence=["program standards", "revision log"]),
                I("Designs a program's human-AI drafting workflow for environmental documents, specifying which sections "
                  "may be machine-drafted and the acceptance checks each must pass.", PORT, attr="ATT-AUG",
                  mode="supervisory", tasks=["seed:sc-review-ai-drafted-sections"], evidence=["workflow design"]),
                I("Certifies analysts to lead reviews independently after evaluating their review files against the "
                  "program standard.", RA + PORT, attr="ATT-FOR", tasks=["seed:v1-6.1.4-T3"],
                  evidence=["certification record"]),
            ],
        },
        "enactments": [
            E("seed:ena-sl-c08-federal", "Federal agency environmental review", "federal-agency",
              basis="NEPA as amended by the Fiscal Responsibility Act of 2023 (page and time limits, lead and cooperating "
                    "agencies), implemented through each department's own procedures after CEQ's government-wide "
                    "regulations were removed (final 2026-01-08); sponsor-paid acceleration under NEPA section 112.",
              principal="The lead agency's responsible official; department leadership.",
              venue="Federal courts under substantial deference (Seven County, 2025); inspectors general; Congress.",
              note="The same review skill is enacted against different, versioned department procedures (DOI handbook; "
                   "USDA 7 CFR 1b; DOT; EPA proposed), so knowing which procedure and version governs each step is part "
                   "of federal performance [E: V2-01].",
              instruments=["nepa-fra-2023", "ceq-nepa-regs-removal", "ceq-nepa-guidance-2025", "doi-nepa-procedures",
                           "usda-nepa-procedures", "dot-nepa-procedures", "epa-nepa-procedures", "nepa-s112-fee",
                           "seven-county", "usfs-objection-rule", "ceq-permitting-data-standard"],
              evidence="E", sources=["V2-01", "V2-02", "V2-04", "V2-08"]),
            E("seed:ena-sl-c08-state", "State agency environmental review", "state-agency",
              basis="State environmental policy acts (for example CEQA, Washington SEPA, Minnesota MEPA, New York SEQR) "
                    "and their implementing rules; some state acts carry substantive mitigation duties that federal "
                    "review does not; state transportation agencies may carry federal review responsibilities by "
                    "assignment and run both regimes in one job.",
              principal="The state lead agency's decision-maker or board.",
              venue="State courts; state administrative appeal bodies.",
              note="SL review: states staff whole units for their own acts (MPCA Environmental Review Unit) and DOTs "
                   "run both regimes in one position (Caltrans) [E: SL-070, SL-038]. State exemptions and streamlining "
                   "change on their own schedules (California 2025 trailer bills) [E: V2-16].",
              instruments=["ceqa-2025-reforms"], addTasks=["seed:sc-joint-review-document"],
              sl_reviewed=True, evidence="E", sources=["SL-070", "SL-038", "V2-16"]),
            E("seed:ena-sl-c08-local", "Local government as lead or cooperating agency", "county",
              basis="Local lead-agency duties under a state environmental policy act; cooperating-agency status on "
                    "federal reviews where the local government has jurisdiction by law or special expertise.",
              principal="Elected board, council or planning commission acting on the project.",
              venue="Local administrative appeals; state courts.",
              note="SL review: county and city planners prepare or supervise documents for elected bodies that sit on "
                   "the dais, so review findings must be briefed in public meetings (see SC-C18) [J].",
              sl_reviewed=True),
            E("seed:ena-sl-c08-consultant", "Consultant preparing review documents", "firm",
              position="service-provider",
              basis="Contract with the agency or the project sponsor; the agency remains responsible for the document "
                    "and must evaluate it independently before adopting it.",
              principal="The client (agency or sponsor); the agency's responsible official for adequacy.",
              venue="Agency adequacy review; professional ethics rules; contract remedies.",
              note="Mirror of SC-C04 (the agency directing and evaluating sponsor-prepared documents). Independence under "
                   "the sponsor-pays model is a TX-B obligation (PS-C18) [J].",
              instruments=["nepa-s112-fee"]),
        ],
    },
    # ------------------------------------------------------------------ SC-C03
    {
        "id": "seed:SC-C03",
        "label": "Select, justify and document the appropriate level of environmental review",
        "alt": ["categorical exclusion determination", "level-of-review determination", "CE / EA / EIS determination"],
        "definition": "The capability to decide which level of environmental review a proposed action requires and to "
                      "record that decision so it can be followed and defended. Covers exclusion screening, "
                      "extraordinary-circumstance review, adoption of another agency's exclusion where allowed, "
                      "significance determinations and acceleration options. Excludes conducting the review itself.",
        "statement": "Screens a proposed action against the deciding agency's exclusion categories and "
                     "extraordinary-circumstance criteria, decides whether an excluded action, an assessment or a full "
                     "impact statement is required, weighs available acceleration options, and documents the "
                     "determination in a structured form that the responsible official and a reviewing court can follow.",
        "span": ("L1", "L4"),
        "derived": [("v1:6.1.4", "split-from")],
        "sources": ["SC-009", "SC-010", "SC-013", "SC-014", "SC-038", "V2-01", "V2-04"],
        "editorial": "WP-05 (A5 SC). Successor of v1 6.1.4 (split with SL-C08). Level-of-review selection is where the "
                     "2025-26 reforms act most directly (exclusion consolidation and adoption, deadlines, fees) [E: "
                     "V2-01, V2-04]; automated exclusion screening moves human judgment to extraordinary circumstances "
                     "[E: SC-037, V2-08]. Indicators adapted from SC proficiency anchors SC-A-C03-1..4 [J].",
        "sensitivity": [
            ("DM-03", "Exclusion categories, adoption across agencies and statutory exclusions are expanding.", "E", ["V2-01", "SC-014"]),
            ("DM-02", "Deadlines and sponsor-paid acceleration bear on the choice of review level.", "E", ["V2-04"]),
            ("DM-14", "Rules-based and AI screening of routine exclusions is in deployment.", "E", ["V2-08"]),
        ],
        "tasks": [
            T("seed:sc-screen-categorical-exclusion", "Screen a proposed action against the agency's exclusion categories and "
              "extraordinary-circumstance criteria, recording the screening result and its basis for the official",
              "WF-REVIEW", profiles=["WP-PROJECT"]),
            T("seed:sc-determine-review-level", "Determine whether a proposed action requires an environmental assessment or "
              "a full impact statement, documenting the significance reasoning in the project record",
              "WF-REVIEW", formation="yes", profiles=["WP-PROJECT"]),
            T("seed:sc-adopt-other-agency-exclusion", "Adopt another agency's exclusion category for a proposed action where "
              "procedures allow, documenting why the actions are comparable",
              "WF-REVIEW", profiles=["WP-PROJECT"]),
            T("seed:sc-review-automated-screening", "Review automated exclusion-screening results for a batch of routine "
              "actions, confirming or overriding each flagged extraordinary circumstance",
              "WF-REVIEW", formation="yes", profiles=["WP-PROJECT"],
              note="Review counterpart of the screening task where rules-based or AI screening compresses production (G-2)."),
            T("seed:sc-advise-acceleration-option", "Advise a project sponsor on sponsor-funded expedited review, stating the "
              "schedule, cost and record-quality risks of each available option",
              "WF-REVIEW", modes=["MODE-ENGAGE"], rel=["client"], profiles=["WP-PROJECT"]),
        ],
        "levels": {
            "L1": [
                I("Applies the agency's exclusion checklist to a routine action, citing the category relied on and "
                  "escalating any possible extraordinary circumstance to the reviewer.", WS + KT,
                  tasks=["seed:sc-screen-categorical-exclusion"], evidence=["screening record"], v1=["v1:6.1.4:foundational:I1"]),
                I("Checks automated screening flags for a routine action against the source map layers, recording each "
                  "flag accepted or rejected for the reviewer.", SEW, mode="assisted",
                  tasks=["seed:sc-review-automated-screening"], evidence=["screening log"]),
            ],
            "L2": [
                I("Makes exclusion, assessment or impact-statement determinations for typical actions that the responsible "
                  "official accepts, recording the significance reasoning for each.", RA + PORT, attr="ATT-AUT",
                  tasks=["seed:sc-determine-review-level"], evidence=["determination file"]),
                I("Documents the adoption of another agency's exclusion category, stating why the actions are comparable "
                  "and why no extraordinary circumstance applies.", WS, attr="ATT-KNO",
                  tasks=["seed:sc-adopt-other-agency-exclusion"], evidence=["adoption record"]),
                I("Overrides an automated screening result after checking it against contradicting site information, "
                  "recording the evidence that justified the override.", SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:sc-review-automated-screening"], evidence=["override log"]),
            ],
            "L3": [
                I("Resolves borderline level-of-review cases such as segmentation, programmatic tiering or emergencies "
                  "with written advice that holds up on internal legal review.", BARS + RA, attr="ATT-CPX",
                  tasks=["seed:sc-determine-review-level"], evidence=["advice memo"]),
                I("Advises a sponsor and the responsible official on sponsor-funded acceleration, stating the schedule, "
                  "cost and record-quality risks of each option in writing.", WS + BARS, attr="ATT-SCO",
                  tasks=["seed:sc-advise-acceleration-option"], evidence=["advice memo"]),
            ],
            "L4": [
                I("Drafts new or revised exclusion categories for an agency program, supported by an evidence record that "
                  "the covered actions have no significant effect.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-screen-categorical-exclusion"], evidence=["category proposal", "evidence record"]),
                I("Specifies the screening rules for automated exclusion review and the sample of results staff must "
                  "verify by hand each quarter.", PORT, attr="ATT-AUG", mode="supervisory",
                  tasks=["seed:sc-review-automated-screening"], evidence=["screening specification"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c03-federal", "Federal level-of-review determination", "federal-agency",
              basis="NEPA section 106 (as amended 2023) thresholds and each department's exclusion lists and "
                    "extraordinary-circumstance criteria; adoption of another agency's exclusion under NEPA section 109; "
                    "sponsor-paid acceleration under section 112.",
              principal="The responsible official who signs the determination.",
              venue="Federal courts; internal legal review; inspectors general.",
              note="Exclusion categories now differ by department and change by procedure revision, so the "
                   "determination must cite the category and procedure version relied on [E: V2-01].",
              instruments=["nepa-fra-2023", "doi-nepa-procedures", "usda-nepa-procedures", "dot-nepa-procedures",
                           "epa-nepa-procedures", "nepa-s112-fee"], evidence="E", sources=["V2-01", "V2-04"]),
            E("seed:ena-sc-c03-state", "State exemption and threshold determination", "state-agency",
              basis="Statutory and categorical exemptions and initial-study or checklist thresholds under state "
                    "environmental policy acts; state streamlining statutes.",
              principal="The state or local lead agency.", venue="State courts.",
              note="SL review: state exemption regimes change on legislative schedules (California's 2025 trailer bills "
                   "added infill and infrastructure exemptions) [E: V2-16].",
              instruments=["ceqa-2025-reforms"], sl_reviewed=True, evidence="E", sources=["V2-16"]),
        ],
    },
    # ------------------------------------------------------------------ SC-C04
    {
        "id": "seed:SC-C04",
        "label": "Direct and evaluate applicant- or contractor-prepared environmental documents",
        "alt": ["applicant-prepared EA/EIS oversight", "third-party document oversight"],
        "definition": "The capability of the deciding agency to set the scope and standards for environmental documents "
                      "that project sponsors or their contractors prepare, to evaluate their adequacy and objectivity, "
                      "and to document its own independent evaluation before adopting them. Excludes preparing the "
                      "document, which is the service-provider enactment of environmental impact review.",
        "statement": "Sets the scope, standards and independence safeguards for environmental documents prepared by "
                     "project sponsors or their contractors, evaluates their adequacy and objectivity, requires "
                     "corrections, and documents the agency's own independent evaluation before the agency adopts the "
                     "document as its own.",
        "span": ("L2", "L4"),
        "sources": ["SC-014", "SC-038", "V2-04"],
        "editorial": "WP-05 (A5 SC). Agency staff shift from authoring to supervising under sponsor-prepared and "
                     "sponsor-paid review [E: SC-014, SC-038, V2-04]. Mirror: the service-provider enactment of SL-C08 "
                     "(preparer) [J].",
        "sensitivity": [
            ("DM-02", "Sponsor-paid acceleration increases sponsor- and contractor-prepared documents.", "E", ["V2-04"]),
            ("DM-15", "The acceleration fee is set at a share of preparation cost, so oversight is funded by the sponsor.", "E", ["V2-04"]),
        ],
        "tasks": [
            T("seed:sc-issue-preparer-standards", "Issue scope and content standards to a sponsor's contractor preparing an "
              "environmental document, specifying data, methods and the agency's review checkpoints",
              "WF-REVIEW", profiles=["WP-PROJECT"]),
            T("seed:sc-evaluate-sponsor-document", "Evaluate a sponsor-prepared environmental document for adequacy and "
              "objectivity, returning specific deficiencies the preparer must correct before adoption",
              "WF-REVIEW", formation="yes", profiles=["WP-PROJECT"]),
            T("seed:sc-document-independent-evaluation", "Document the agency's independent evaluation of a sponsor-prepared "
              "document before adoption, recording what was verified and what was changed",
              "WF-REVIEW", profiles=["WP-PROJECT"], accountable="The agency remains responsible for the content of an "
              "adopted document and must show its own evaluation."),
            T("seed:sc-screen-preparer-conflicts", "Screen a contractor's disclosure statement for financial or other interest "
              "in the project outcome before the contractor begins preparing the document",
              "WF-REVIEW", formation="no", also=["seed:PS-C18"]),
        ],
        "levels": {
            "L2": [
                I("Returns a sponsor-prepared document with itemized deficiencies, each tied to the scope standard or "
                  "record evidence it fails, within the review schedule.", WS + SEW,
                  tasks=["seed:sc-evaluate-sponsor-document"], evidence=["deficiency letter"]),
                I("Records the agency's independent evaluation of a sponsor-prepared section, listing each conclusion "
                  "checked against the record before adoption.", RA,
                  tasks=["seed:sc-document-independent-evaluation"], evidence=["evaluation memo"]),
            ],
            "L3": [
                I("Detects unsupported conclusions planted in a sponsor-prepared document at the detection rate the "
                  "program sets for senior reviewers.", SEW, attr="ATT-CPX",
                  tasks=["seed:sc-evaluate-sponsor-document"], evidence=["seeded-error test result"]),
                I("Negotiates corrections with a sponsor's contractor on a contested document, holding the agency's "
                  "position where evidence is disputed and recording how each issue was resolved.", SIM + RA,
                  attr="ATT-SCO", tasks=["seed:sc-evaluate-sponsor-document"], evidence=["issue log"]),
                I("Checks AI-assisted portions of a sponsor-prepared document against sources after requiring the "
                  "preparer to disclose which content was machine-drafted.", SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:sc-document-independent-evaluation"], evidence=["disclosure", "verification log"]),
            ],
            "L4": [
                I("Writes a program's standards for applicant-prepared documents, covering scope letters, independence "
                  "disclosures and adoption checks, with the audit criteria reviewers apply.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-issue-preparer-standards"], evidence=["program standard"]),
                I("Certifies staff to evaluate applicant-prepared documents independently after reviewing their "
                  "evaluation files against the program standard.", RA + PORT, attr="ATT-FOR",
                  tasks=["seed:sc-document-independent-evaluation"], evidence=["certification record"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c04-federal", "Federal oversight of sponsor-prepared documents", "federal-agency",
              basis="NEPA section 107(f) (sponsor preparation with agency supervision and independent evaluation) and "
                    "department procedures for applicant-prepared documents; sponsor-paid acceleration under section 112.",
              principal="The responsible official who adopts the document.",
              venue="Federal courts; agency legal review.",
              note="Department procedures keep specific steps for applicant-prepared documents and require the bureau to "
                   "document its evaluation [E: SC-038].",
              instruments=["nepa-fra-2023", "doi-nepa-procedures", "nepa-s112-fee"], evidence="E",
              sources=["SC-038", "V2-04"]),
            E("seed:ena-sc-c04-state", "State lead agency use of consultant-prepared documents", "state-agency",
              basis="State environmental policy acts that let applicants or consultants prepare documents only if the "
                    "lead agency exercises and documents its independent judgment.",
              principal="The state or local lead agency.", venue="State courts.",
              note="SL review: same oversight skill; the independent-judgment test is set by state statute and case law "
                   "rather than federal procedure [J].",
              sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ SC-C09
    {
        "id": "seed:SC-C09",
        "label": "Coordinate lead, cooperating and participating agencies to a shared schedule",
        "alt": ["interagency coordination", "cooperating agency management", "permitting coordination plan"],
        "definition": "The capability to organize several agencies with authority over one action into agreed roles and "
                      "one schedule, and to keep that schedule and its public record accurate. Covers role agreements, "
                      "joint schedules, cooperating-agency decisions and jurisdiction disputes. Excludes oversight of "
                      "delegated programs, which is a separate competency.",
        "statement": "Establishes and runs the roles, joint schedule and milestones among the lead, cooperating and "
                     "participating agencies for a multi-agency action, resolves disputes about jurisdiction and "
                     "timing, decides cooperating-agency requests with reasons, and keeps the shared schedule and public "
                     "milestone data accurate.",
        "span": ("L1", "L4"),
        "derived": [("v1:6.5.2", "split-from")],
        "sources": ["SC-010", "SC-014", "V2-01", "V2-03"],
        "editorial": "WP-05 (A5 SC). Successor of the coordination part of v1 6.5.2 (split with SC-C14). The 2023 "
                     "amendments codified lead-agency and one-document rules; dashboard milestones make schedule "
                     "performance observable [E: SC-010, V2-01]. Indicators adapted from SC-A-C09-1..4 [J].",
        "sensitivity": [
            ("DM-05", "Lead, cooperating and participating roles and joint schedules are now statutory.", "E", ["V2-01"]),
            ("DM-02", "Deadlines and schedule enforcement shape coordination.", "E", ["V2-04"]),
            ("DM-14", "Public permitting dashboards and the data standard make milestones auditable.", "E", ["V2-08"]),
        ],
        "tasks": [
            T("seed:v1-6.5.2-T1", "Coordinate review steps with other agencies holding authority over the same action, so "
              "that duplicated analyses and conflicting requirements are identified early",
              "WF-REVIEW", modes=["MODE-ENGAGE"], rel=["intergovernmental"], profiles=["WP-PROJECT"],
              derived=[("v1:6.5.2:T1", "rewritten")]),
            T("seed:v1-6.5.2-T2", "Represent the agency in an interagency working group on a shared project, stating the "
              "agency's positions within the authority delegated to the representative",
              "WF-REVIEW", modes=["MODE-ENGAGE"], rel=["intergovernmental"], derived=[("v1:6.5.2:T2", "rewritten")]),
            T("seed:v1-6.5.2-T3", "Align milestones and data exchange formats across jurisdictions for a shared project, "
              "recording the agreed dates in the joint schedule",
              "WF-REVIEW", rel=["intergovernmental"], formation="no", derived=[("v1:6.5.2:T3", "rewritten")]),
            T("seed:sc-decide-cooperating-request", "Decide a request for cooperating-agency status on a review, stating the "
              "reasons for granting or denying the request in the record",
              "WF-REVIEW", rel=["intergovernmental"], profiles=["WP-PROJECT"]),
            T("seed:sc-update-permitting-dashboard", "Update public milestone and dashboard entries for a covered project, "
              "reconciling each entry against agency source documents every reporting period",
              "WF-REVIEW", formation="no", profiles=["WP-PROJECT"]),
        ],
        "levels": {
            "L1": [
                I("Updates milestone tracker and public dashboard entries for a project so that every entry matches its "
                  "agency source document in a data-accuracy audit.", RA, tasks=["seed:sc-update-permitting-dashboard"],
                  evidence=["dashboard entries", "source documents"]),
                I("Prepares interagency meeting materials listing each agency's open decisions and due dates from the "
                  "joint schedule.", WS, tasks=["seed:v1-6.5.2-T3"], evidence=["meeting packet"]),
            ],
            "L2": [
                I("Runs coordination for a single multi-agency review, keeping the joint schedule current and escalating "
                  "each unresolved conflict to the lead with options.", RA + ["counterpart-360"], attr="ATT-AUT",
                  tasks=["seed:v1-6.5.2-T1"], evidence=["joint schedule", "escalation memos"]),
                I("Drafts a cooperating-agency decision that states the requesting agency's jurisdiction or special "
                  "expertise and the reasons for the decision.", WS, attr="ATT-KNO",
                  tasks=["seed:sc-decide-cooperating-request"], evidence=["decision letter"]),
            ],
            "L3": [
                I("Negotiates the division of analysis and timing among agencies on a contested or covered project, "
                  "documenting each agreed responsibility in the coordination plan.", SIM + PORT, attr="ATT-SCO",
                  tasks=["seed:v1-6.5.2-T2"], evidence=["coordination plan"]),
                I("Re-plans the joint schedule when one agency's procedure or deadline changes, stating the critical-path "
                  "effect to every participating agency in writing.", WS + BARS, attr="ATT-CPX",
                  tasks=["seed:v1-6.5.2-T3"], evidence=["revised schedule", "notice"]),
            ],
            "L4": [
                I("Designs standing interagency coordination agreements and escalation rules that participating agencies "
                  "apply across a project portfolio.", PORT, attr="ATT-GUI", tasks=["seed:v1-6.5.2-T1"],
                  evidence=["standing agreement"]),
                I("Coaches project coordinators on interagency disputes, evaluating their coordination plans against the "
                  "program standard before projects start.", PORT, attr="ATT-FOR", obs4=2,
                  tasks=["seed:v1-6.5.2-T2"], evidence=["coaching record", "plan reviews"]),
                I("Writes the program's coordination-plan template and milestone definitions, with the data checks that "
                  "public dashboard entries must pass.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-update-permitting-dashboard"], evidence=["template", "data checks"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c09-federal", "Federal lead agency coordination", "federal-agency",
              basis="NEPA section 107 lead, cooperating and participating agency rules (as amended 2023); FAST-41 "
                    "coordination plans and the public dashboard for covered projects; department procedures allowing "
                    "reasoned denials of cooperating-agency requests.",
              principal="The lead agency's responsible official; the Permitting Council for covered projects.",
              venue="Federal courts; Permitting Council dispute escalation; Congress.",
              note="Schedule performance is now publicly visible, which makes milestone accuracy an assessable entry-level "
                   "task [E: SC-010].",
              instruments=["nepa-fra-2023", "fast-41", "ceq-permitting-data-standard", "doi-nepa-procedures",
                           "speed-act"], evidence="E", sources=["V2-01", "V2-03", "V2-08"]),
            E("seed:ena-sc-c09-state-local", "State or local agency as cooperating agency", "state-agency",
              basis="Jurisdiction by law or special expertise over part of a federal action; state law for joint "
                    "state-federal documents.",
              principal="The state agency head or local elected body that authorizes participation.",
              venue="State courts for state decisions; federal dispute escalation for the joint schedule.",
              note="SL review: state and county staff decide whether participation is worth the staff time and what "
                   "authority their representative carries; pending federal legislation would expand county "
                   "cooperating status [E: V2-03 for status; J for effect].",
              instruments=["speed-act"], sl_reviewed=True, evidence="E", sources=["V2-03"]),
        ],
    },
    # ------------------------------------------------------------------ DB-C50
    {
        "id": "seed:DB-C50",
        "label": "Review effects of proposed actions on historic properties and resolve them through consultation",
        "alt": ["Section 106 review", "historic preservation review", "cultural resource compliance"],
        "definition": "The capability to identify historic properties a proposed action may affect, assess the effects, "
                      "consult the parties the governing procedure names and resolve adverse effects in an "
                      "implementable agreement. Determinations of cultural significance rest with the communities "
                      "concerned and are not assessed by this competency.",
        "statement": "Identifies historic properties in a proposed action's area of potential effects, assesses whether "
                     "the action would adversely affect them, consults preservation offices and other consulting "
                     "parties, and resolves adverse effects through agreed measures recorded in a form the deciding "
                     "agency can implement and monitor.",
        "span": ("L1", "L4"),
        "sources": ["V2-14", "SC-039"],
        "editorial": "WP-05 (A5 SC). Survivor DB-C50 absorbs FH-C08. Historic-property review becomes the critical path "
                     "when environmental review accelerates, because sponsor-paid acceleration does not speed it [E: "
                     "SC-039]. Text is regulation-neutral because a rewrite of the federal regulations is at OIRA "
                     "and unpublished [E: V2-14]. Consultation obligations owed to Tribal nations, THPO coordination "
                     "and determinations of significance to Tribes are held content (TN-C11, ADR-0007) and are not "
                     "authored here; TN owns any Tribal enactment.",
        "sensitivity": [
            ("DM-07", "The federal historic-preservation regulations are being rewritten (NPRM at OIRA).", "E", ["V2-14"]),
            ("DM-02", "Review deadlines elsewhere put pressure on consultation timelines.", "E", ["SC-039"]),
        ],
        "tasks": [
            T("seed:sc-define-area-potential-effects", "Define the area of potential effects for a proposed undertaking, "
              "documenting the direct and indirect effect pathways that justify its boundary",
              "WF-REVIEW", profiles=["WP-PROJECT"]),
            T("seed:sc-recommend-property-eligibility", "Apply eligibility criteria to properties identified in an area of "
              "potential effects, documenting the evidence behind each eligibility recommendation",
              "WF-REVIEW", field="on-site-preferred", formation="yes",
              signoff="regulatory-definition",
              note="Professional-qualification standards define who may make some identification and evaluation "
                   "findings (sign-off authority: regulatory definition)."),
            T("seed:sc-assess-historic-effects", "Assess whether a proposed action would adversely affect each eligible "
              "property, recording the criteria and evidence applied to each finding",
              "WF-REVIEW", formation="yes", profiles=["WP-PROJECT"]),
            T("seed:sc-negotiate-effect-resolution", "Negotiate measures that resolve adverse effects with consulting parties, "
              "recording the agreed measures in an agreement document the agency can implement",
              "WF-REVIEW", modes=["MODE-RESOLVE", "MODE-ENGAGE"], rel=["intergovernmental", "stakeholder"],
              profiles=["WP-PROJECT"]),
            T("seed:sc-sequence-preservation-review", "Schedule historic-property review alongside the environmental review, "
              "so that consultation findings are available before the agency makes its decision",
              "WF-REVIEW", formation="no", profiles=["WP-PROJECT"]),
        ],
        "levels": {
            "L1": [
                I("Compiles a records search of known historic properties for an assigned area of potential effects, "
                  "citing the inventory consulted for each entry.", WS + RA,
                  tasks=["seed:sc-define-area-potential-effects"], evidence=["records search"]),
                I("Drafts an eligibility recommendation for a single property from assigned survey data, stating the "
                  "criteria applied for the reviewer.", WS, tasks=["seed:sc-recommend-property-eligibility"],
                  evidence=["draft recommendation"]),
            ],
            "L2": [
                I("Prepares effect findings for routine undertakings that the preservation office concurs with without "
                  "requests for more information.", PORT + RA, attr="ATT-AUT",
                  tasks=["seed:sc-assess-historic-effects"], evidence=["effect findings", "concurrence letters"]),
                I("Defines the area of potential effects for an undertaking and records the effect pathways that justify "
                  "its boundary.", WS, attr="ATT-KNO", tasks=["seed:sc-define-area-potential-effects"],
                  evidence=["boundary memo"]),
            ],
            "L3": [
                I("Negotiates an agreement resolving adverse effects among several consulting parties, recording each "
                  "party's position and the measures adopted.", SIM + PORT, attr="ATT-SCO",
                  tasks=["seed:sc-negotiate-effect-resolution"], evidence=["agreement document", "consultation record"]),
                I("Adapts the review when the governing procedure changes or a property is discovered during "
                  "implementation, documenting the revised steps.", BARS + RA, attr="ATT-GUI", obs4=2,
                  tasks=["seed:sc-sequence-preservation-review"], evidence=["revised review plan"]),
                I("Writes the consultation record for a multi-party review so that each party's comment, the agency's "
                  "response and any resulting change are traceable.", RA, attr="ATT-SCO",
                  tasks=["seed:sc-negotiate-effect-resolution"], evidence=["consultation record"]),
            ],
            "L4": [
                I("Designs a program-level alternative to case-by-case review for a class of routine undertakings, with "
                  "criteria and monitoring the consulting parties can audit.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-assess-historic-effects"], evidence=["program alternative"]),
                I("Certifies staff to lead consultations independently after observing their conduct of consultation "
                  "meetings against the program standard.", TB + PORT, attr="ATT-FOR",
                  tasks=["seed:sc-negotiate-effect-resolution"], evidence=["certification record"]),
            ],
        },
        "enactments": [
            E("seed:ena-db-c50-federal", "Federal agency official for an undertaking", "federal-agency",
              basis="NHPA section 106 and the ACHP regulations (36 CFR part 800); a rewrite advanced by the ACHP on "
                    "2026-07-24 is at OIRA and unpublished; program alternatives and programmatic agreements.",
              principal="The agency official with jurisdiction over the undertaking.",
              venue="ACHP comment process; federal courts.",
              note="Federal agencies carry the review duty for their undertakings, including permits and funding they "
                   "provide; acceleration of environmental review does not shorten this review [E: SC-039, V2-14].",
              instruments=["nhpa-s106-regs"], evidence="E", sources=["V2-14", "SC-039"]),
            E("seed:ena-db-c50-state", "State historic preservation office review", "state-agency",
              position="regulator",
              basis="The state historic preservation office's consulting role in federal reviews and state "
                    "historic-preservation laws for state-funded or state-permitted actions.",
              principal="The state historic preservation officer.",
              venue="State courts for state-law reviews; the federal consultation record.",
              note="SL review: SHPO reviewers concur or object to agency findings; the same identification and effects "
                   "skills are performed from the reviewing side (mirror of the agency-official enactment) [J].",
              sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ DB-C52
    {
        "id": "seed:DB-C52",
        "label": "Analyze cumulative burdens and distributional effects of environmental decisions",
        "alt": ["environmental justice screening and assessment", "EJ analysis", "cumulative impact analysis",
                "existing burden report", "disproportionate impact analysis"],
        "definition": "The capability to characterize existing environmental and health burdens on the communities a "
                      "decision affects, estimate how the decision changes those burdens and how its effects are "
                      "distributed, and document the analysis in the form the applicable procedure requires. Excludes "
                      "community engagement design and partnership building, which are separate competencies.",
        "statement": "Characterizes the existing environmental and health burdens on communities affected by a proposed "
                     "decision, estimates how the decision adds to or reduces those burdens and how its effects are "
                     "distributed, states the uncertainty in screening data and methods, and documents the analysis in "
                     "the form the applicable review or permit procedure requires.",
        "span": ("L2", "L4"),
        "derived": [("v1:6.7.2", "merged-from")],
        "sources": ["DB-060", "WP05-001", "WP05-002", "WP05-003", "SC-014"],
        "editorial": "WP-05 (A5 SC). Survivor named by the work performed under ADR-0016 (v1 6.7.2 merged in); EJ labels "
                     "are altLabels. Federal executive-order bases were revoked in January 2025 while state "
                     "cumulative-impact statutes remain in force [E: WP05-001, WP05-002, WP05-003], so venue "
                     "applicability is computed from the actor enactments' instruments (ADR-0016 section 3); the "
                     "federal-revocation and state-statute instruments are not yet in the L5 registry (see WP-05 "
                     "worklog). Screening tools go to L4 with dates. Q4 default: no exclusions in federal default views.",
        "sensitivity": [
            ("DM-01", "Federal review scope narrowed and executive-order direction to analyze distributional effects revoked.", "E", ["WP05-001", "V2-02"]),
            ("DM-10", "State cumulative-impact statutes set substantive permit standards (denial or conditions).", "E", ["WP05-002", "WP05-003"]),
            ("DM-04", "Participation requirements for affected communities differ by venue.", "J", None),
        ],
        "tasks": [
            T("seed:v1-6.7.2-T1", "Screen a proposed project's area for existing environmental and health burdens using "
              "screening indicators, recording each indicator's source, date and known limitations",
              "WF-REVIEW", derived=[("v1:6.7.2:T1", "rewritten")],
              note="v1 named two screening tools; tools move to L4 with availability dates (one federal tool's "
                   "availability changed in 2025)."),
            T("seed:v1-6.7.2-T2", "Estimate how a proposed permit or project changes cumulative burdens on affected "
              "communities, stating the uncertainty and assumptions behind each estimate",
              "WF-REVIEW", formation="yes", derived=[("v1:6.7.2:T2", "rewritten")]),
            T("seed:v1-6.7.2-T3", "Present burden-analysis findings to affected residents in plain language, recording the "
              "questions raised and how the analysis responds to each",
              "WF-REVIEW", modes=["MODE-ENGAGE"], rel=["public"], derived=[("v1:6.7.2:T3", "rewritten")]),
            T("seed:sc-document-burden-analysis", "Document a distributional-effects analysis in the permit or review "
              "record in the form the applicable procedure requires, citing every data source used",
              "WF-REVIEW", formation="no"),
            T("seed:sc-validate-burden-screening", "Validate a burden screening for a permit decision against local "
              "monitoring or health data, documenting where the screening misrepresents conditions",
              "WF-REVIEW", formation="yes"),
        ],
        "levels": {
            "L2": [
                I("Screens a project area with current burden indicators, recording each indicator's source, vintage and "
                  "known limitation in the analysis file.", WS + RA, tasks=["seed:v1-6.7.2-T1"],
                  evidence=["screening file"]),
                I("Estimates the change in cumulative burden from a routine permit decision, stating the uncertainty range "
                  "and the assumptions that drive it.", WS, tasks=["seed:v1-6.7.2-T2"], evidence=["burden estimate"]),
                I("Checks screening outputs against local monitoring data, flagging each indicator that misrepresents "
                  "conditions in the project area.", SEW, mode="assisted", tasks=["seed:sc-validate-burden-screening"],
                  evidence=["validation memo"]),
            ],
            "L3": [
                I("Designs the burden-analysis method for a non-routine decision where screening data conflict, "
                  "documenting why the chosen indicators fit the decision.", WS + BARS, attr="ATT-GUI",
                  tasks=["seed:v1-6.7.2-T2"], evidence=["method memo"]),
                I("Presents burden findings and their uncertainty to affected residents in plain language, answering each "
                  "question raised or recording it for follow-up.", SIM + TB, attr="ATT-SCO", obs4=2,
                  tasks=["seed:v1-6.7.2-T3"], evidence=["meeting record"]),
                I("Reviews a burden screening produced with automated tools, testing a sample of indicator values against "
                  "source data and recording each correction made.", SEW + RA, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:sc-validate-burden-screening"], evidence=["sample log"]),
            ],
            "L4": [
                I("Sets a program's burden-analysis standards, including indicator selection, uncertainty statements and "
                  "data-currency checks, for use across permit types.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-document-burden-analysis"], evidence=["program standard"]),
                I("Reviews staff burden analyses against the program standard, returning each deficiency with the "
                  "evidence needed to correct it.", RA, attr="ATT-FOR", tasks=["seed:sc-document-burden-analysis"],
                  evidence=["review comments"]),
            ],
        },
        "enactments": [
            E("seed:ena-db-c52-federal", "Federal agency distributional analysis", "federal-agency",
              basis="No current government-wide executive-order basis: EO 12898 was revoked by EO 14173 (2025-01-21) and "
                    "EO 14096 by EO 14148 (2025-01-20). Analysis remains possible where a statute, a program rule or the "
                    "agency's own procedures call for it; revocation does not change statutory duties.",
              principal="The deciding official.", venue="Federal courts; inspectors general.",
              note="ADR-0016: applicability is computed, not asserted. With the federal instruments linked (pending L5 "
                   "registration), federal applicability computes to no-current-basis while statute-based duties keep "
                   "the work permitted; Q4 default shows the computed value with a note and no exclusion.",
              evidence="E", sources=["WP05-001"]),
            E("seed:ena-db-c52-state", "State cumulative-impact permitting", "state-agency", position="regulator",
              basis="State cumulative-impact and disproportionate-burden statutes for listed permit types: New Jersey's "
                    "2020 law and rules N.J.A.C. 7:1C (in force 2023-04-17; affirmed by the Appellate Division "
                    "2026-01-05) and New York ECL 70-0118 with SEQR amendments effective 2026-06-12 (permit-procedure "
                    "amendments still in progress).",
              principal="The state permitting agency and its commissioner.",
              venue="State administrative hearings; state courts.",
              note="SL review: the analysis is a regulatory product here; it can lead to denial or site-specific "
                   "conditions for covered facilities [E: WP05-002, WP05-003].",
              sl_reviewed=True, evidence="E", sources=["WP05-002", "WP05-003", "DB-060"]),
            E("seed:ena-db-c52-ngo", "Community organization or advocate analysis", "community-organization",
              position="advocate",
              basis="No decision authority; participation rights in comment periods and hearings, and standing to "
                    "challenge decisions where the law provides.",
              principal="Members and affected residents; funders.",
              venue="The agency's comment record; administrative hearings; courts.",
              note="The same analysis is produced to influence a decision rather than make it; methods and uncertainty "
                   "statements are judged by the deciding agency and courts [J]."),
        ],
    },
    # ------------------------------------------------------------------ FH-C01
    {
        "id": "seed:FH-C01",
        "label": "Assess effects on protected species and conduct interagency consultation on proposed actions",
        "alt": ["ESA Section 7 consultation", "biological assessment preparation", "listed species consultation"],
        "definition": "The capability of an action agency, or of a consulting wildlife or fisheries agency, to determine "
                      "and document a proposed action's effects on listed species and designated critical habitat and "
                      "to complete interagency consultation, carrying its terms into the action. Excludes species "
                      "status assessments for listing decisions.",
        "statement": "Determines whether a proposed action may affect listed species or designated critical habitat, "
                     "prepares the biological assessment, consults the wildlife or fisheries agency to reach "
                     "concurrence or an opinion, and carries the resulting terms, conservation measures and reporting "
                     "duties into the action's design and decision.",
        "span": ("L1", "L4"),
        "sources": ["V2-05", "SC-018", "SC-019", "SC-020", "SC-039"],
        "editorial": "WP-05 (A5 SC; FH candidate). Recurs across forest, water, energy, transport and wildlife modules "
                     "(G-4). Species rules changed in 2025-26 (harm definition rescinded, effective 2026-09-14, "
                     "litigated; blanket protective rule eliminated; consultation rules proposed) [E: V2-05], so the "
                     "text is regulation-neutral and the rules attach in L5.",
        "sensitivity": [
            ("DM-06", "Consultation, take and protective-rule frameworks narrowed and are litigated.", "E", ["V2-05", "SC-019", "SC-020"]),
            ("DM-10", "The take definition no longer covers habitat modification alone.", "E", ["V2-05"]),
            ("DM-02", "Acceleration of environmental review does not speed consultation.", "E", ["SC-039"]),
        ],
        "tasks": [
            T("seed:sc-compile-species-occurrence", "Compile species and habitat occurrence information for an action area, "
              "documenting the sources and survey dates used for each listed species",
              "WF-REVIEW", formation="partial"),
            T("seed:sc-prepare-biological-assessment", "Prepare a biological assessment for a proposed action, stating the "
              "effects determination for each listed species and critical habitat with supporting evidence",
              "WF-REVIEW", formation="yes", profiles=["WP-PROJECT"]),
            T("seed:sc-negotiate-conservation-measures", "Negotiate conservation measures with the consulting wildlife agency, "
              "recording in the project description each agreed measure and the effect it avoids or reduces",
              "WF-REVIEW", modes=["MODE-RESOLVE"], rel=["intergovernmental"], formation="yes"),
            T("seed:sc-track-consultation-terms", "Track the terms and reporting conditions of a completed consultation through "
              "implementation, notifying the consulting agency when a reinitiation trigger occurs",
              "WF-MONITOR", formation="partial"),
            T("seed:sc-review-ai-effects-determination", "Review an effects determination drafted with AI assistance against "
              "the species and project records, correcting each conclusion the records do not support",
              "WF-REVIEW", formation="yes"),
        ],
        "levels": {
            "L1": [
                I("Compiles occurrence records for listed species in an assigned action area, citing the database or "
                  "survey and its date for every record.", WS + RA, tasks=["seed:sc-compile-species-occurrence"],
                  evidence=["occurrence table"]),
                I("Checks a draft project description against the consultation checklist, referring each missing element "
                  "to the biologist leading the consultation.", WS, tasks=["seed:sc-prepare-biological-assessment"],
                  evidence=["checklist"]),
            ],
            "L2": [
                I("Prepares a biological assessment for a routine action whose effects determinations the consulting "
                  "agency accepts without requests for more information.", PORT + RA, attr="ATT-AUT",
                  tasks=["seed:sc-prepare-biological-assessment"], evidence=["biological assessment", "concurrence"]),
                I("States the effects determination for each species with its supporting evidence, distinguishing "
                  "effects of the action from baseline conditions.", WS, attr="ATT-KNO",
                  tasks=["seed:sc-prepare-biological-assessment"], evidence=["effects section"]),
                I("Corrects each unsupported conclusion in an AI-drafted effects determination after checking it against "
                  "the species and project records.", SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:sc-review-ai-effects-determination"], evidence=["verification log"]),
            ],
            "L3": [
                I("Negotiates conservation measures with the consulting agency on a contested action, documenting the "
                  "effect each measure is expected to avoid or reduce.", SIM + PORT, attr="ATT-SCO",
                  tasks=["seed:sc-negotiate-conservation-measures"], evidence=["measures table"]),
                I("Applies changed species rules or listing status to an ongoing consultation, recording which "
                  "determinations must be revisited and why.", BARS + WS, attr="ATT-GUI",
                  tasks=["seed:sc-track-consultation-terms"], evidence=["change memo"]),
            ],
            "L4": [
                I("Designs a programmatic consultation approach for a class of recurring actions, with effect thresholds "
                  "and reporting the consulting agency can audit.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-prepare-biological-assessment"], evidence=["programmatic framework"]),
                I("Certifies biologists to lead consultations after reviewing their assessments against the program's "
                  "quality standard.", RA + PORT, attr="ATT-FOR", tasks=["seed:sc-prepare-biological-assessment"],
                  evidence=["certification record"]),
            ],
        },
        "enactments": [
            E("seed:ena-fh-c01-action-agency", "Federal action agency", "federal-agency",
              basis="ESA section 7(a)(2) duty of the agency that funds, authorizes or carries out the action, under the "
                    "joint consultation regulations (50 CFR part 402) as amended and proposed for amendment.",
              principal="The action agency's deciding official.",
              venue="Federal courts (citizen suits); the consulting agency's opinion.",
              note="Rule changes in 2025-26 (harm rescission effective 2026-09-14, litigated; blanket 4(d) rule "
                   "eliminated; section 4 and 7 rules proposed) change determinations, not the consultation skill "
                   "[E: V2-05].",
              instruments=["esa-harm-rescission", "esa-4d-4b2-rules", "esa-s4-s7-regs-2025"], evidence="E",
              sources=["V2-05", "SC-019", "SC-020"]),
            E("seed:ena-fh-c01-consulting-agency", "Federal consulting wildlife or fisheries agency", "federal-regulator",
              position="regulator",
              basis="The consulting agency's duty to issue concurrences, biological opinions and incidental take "
                    "statements.",
              principal="The consulting agency's regional or field office head.",
              venue="Federal courts.",
              note="Mirror of the action-agency enactment: the same effects analysis is reviewed and answered with "
                   "binding terms [J].",
              instruments=["esa-harm-rescission", "esa-s4-s7-regs-2025"], evidence="E", sources=["V2-05"]),
            E("seed:ena-fh-c01-state", "State wildlife agency and state species law", "state-agency",
              basis="State endangered-species statutes and permits; state agencies also act as non-federal applicants "
                    "or designated representatives where a federal nexus exists.",
              principal="The state wildlife agency director or commission.", venue="State courts.",
              note="SL review: state species laws can be broader or narrower than federal law and do not change when "
                   "federal rules change [J].", sl_reviewed=True),
        ],
    },
]
