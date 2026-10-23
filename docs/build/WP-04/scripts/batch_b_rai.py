"""Batch B: DC specialist responsible-AI competencies (DC-CAND-14, -15, -16, -19, -20, -21) and their v1 task re-pointing."""
from lib import Bundle, competency, df, rewrite_seed_task, task, write

CAND = lambda c: [{"scheme": "EMST-candidate", "value": c}]  # noqa: E731
OUT_T = []
E = dict(lifecycle="emerging")

# =============================================================================== DC-CAND-14
C = "seed:DC-CAND-14"
T = {"t1": "seed:v1-2.5.5-T1", "t2": "seed:v1-2.5.5-T2", "t3": "seed:v1-2.5.5-T3", "o2": "seed:v1-7.1.4-T2",
     "seed": "seed:dc-14-seeded-errors", "req": "seed:dc-14-oversight-requirements"}
OUT_T += [
    rewrite_seed_task(T["t1"], "Specify the review and approval points in an automated permit-review or field-data workflow, stating which outputs a person must approve before release.",
                      [C], "WF-PLAN", "remote", "partial", **E),
    rewrite_seed_task(T["t2"], "Map a multi-step review workflow with its decision points, controls and escalation paths before any step is automated.",
                      [C], "WF-PLAN", "remote", "partial", **E),
    rewrite_seed_task(T["t3"], "Monitor an AI-assisted review workflow using override rates, time on item and seeded-error catch rates, redesigning it when review becomes perfunctory.",
                      [C], "WF-MONITOR", "remote", "partial", **E),
    rewrite_seed_task(T["o2"], "Design human oversight for an AI-assisted workflow, defining reviewer qualifications, review rates by risk and the triggers for escalation.",
                      [C], "WF-PLAN", "remote", "partial", **E,
                      note="Split from v1 7.1.4 (oversight design → DC-CAND-14; ADR-0025 §3)."),
    task(T["seed"], "Insert seeded errors into an AI-assisted review queue to measure whether reviewers catch them, reporting the catch rate for the workflow.",
         [C], "WF-MONITOR", "remote", "no", sources=["DC-001"], evidence="E", **E),
    task(T["req"], "Set organizational requirements for human oversight of AI-assisted work by risk tier, reporting oversight performance to the governance body.",
         [C], "WF-MANAGE", "remote", "partial", sources=["DC-007"], evidence="E", **E),
]
b = Bundle(C, "dc-cand-14")
b.ind("L2", "Specifies review rates by risk, confidence thresholds, escalation triggers and reviewer qualifications for one AI-assisted workflow, in a design a peer can implement.", "s", ["ws"], [T["t1"], T["o2"]], **E)
b.ind("L2", "Shows in the workflow design that a reviewer can change or halt each automated outcome, naming the record that captures the override.", "s", ["ws"], [T["t2"], T["t1"]], **E)
b.ind("L3", "Measures whether review is substantive using override rates, time on item and seeded-error catch rates, redesigning the workflow when review degrades.", "s", ["ra", "ws"], [T["t3"], T["seed"]], attr="aug", **E)
b.ind("L3", "Keeps reviewers independent of the tool's producer in the workflow design, documenting the separation of roles and any exceptions.", "s", ["pr"], [T["o2"]], attr="sco", **E)
b.ind("L4", "Sets organizational oversight requirements by risk tier for AI-assisted work, specifying review rates and reviewer qualifications for each tier.", "s", ["pr", "bars"], [T["req"]], attr="sco", **E)
b.ind("L4", "Reports oversight performance across AI-assisted workflows to the governance body, flagging workflows where review is not changing outcomes.", "s", ["pr"], [T["req"]], attr="sco", **E)
b.write_indicators()
write(competency(
    C, "Design human-in-the-loop review for AI-assisted environmental workflows",
    "The capability to specify where people review, approve or override AI outputs in a workflow and to show that the review is substantive. It covers review rates by risk, confidence thresholds, escalation triggers, reviewer qualifications and independence, audit logs and review-quality measures. It excludes doing the validation (transversal floor) and authorizing the design (statecraft).",
    "Specifies where people review, approve or override AI outputs in an environmental workflow: risk-based review rates, confidence thresholds and escalation triggers, reviewer qualifications, independence from the tool's producer and audit logs; measures whether review is substantive rather than perfunctory; and redesigns the workflow when review quality degrades.",
    "practice", ("L2", "L4"), b.levels(), evidence="E", sources=["DC-007", "DC-001", "DC-045", "DC-020"],
    derived=[df("v1:2.5.5", "merged-from", "process modelling with decision points and controls"), df("v1:7.1.4", "split-from", "oversight design (ADR-0025 §3)")],
    alt=["Human oversight design for AI-assisted work"], notation=CAND("DC-CAND-14"), reusability="cross-subsector", **E,
    note="DC specialist responsible-AI competency (ADR-0025 §2 layer 2). Distinct from DC-CAND-13 (doing validation) and DC-CAND-19 (deciding risk tier). Authorization of the design is the SC enactment of DC-CAND-13 (seed:v1-7.1.4-A)."))

# =============================================================================== DC-CAND-15
C = "seed:DC-CAND-15"
T = {k: f"seed:dc-15-{k}" for k in ("label-reference", "build-set", "benchmark", "judge-check", "task-rubric", "retest", "programme")}
OUT_T += [
    task(T["label-reference"], "Label items for a reference set following written guidelines without seeing tool outputs, flagging ambiguous items for adjudication.",
         [C], "WF-MONITOR", "remote-capable", "partial", sources=["DC-037"], evidence="E", **E),
    task(T["build-set"], "Build a representative reference set for an environmental task with a sampling frame, labelling guide and a double-labelled subset with agreement statistics.",
         [C], "WF-MONITOR", "remote", "partial", sources=["DC-037", "DC-060"], evidence="E", **E),
    task(T["benchmark"], "Benchmark candidate AI tools and the current human process on the same reference set, reporting error by condition with a recommendation.",
         [C], "WF-MONITOR", "remote", "partial", sources=["DC-032", "DC-041"], evidence="E", **E),
    task(T["judge-check"], "Test automated scoring of AI outputs against human scoring on a sample before an evaluation relies on that scoring.",
         [C], "WF-MONITOR", "remote", "partial", sources=["DC-032"], evidence="E", **E),
    task(T["task-rubric"], "Design realistic multi-step environmental work tasks with reference answers and grading rubrics for evaluating AI tools and agents.",
         [C], "WF-PLAN", "remote", "yes", **E, note="Absorbs FS-C17 (candidate_disposition merge-into DC-CAND-15)."),
    task(T["retest"], "Re-test an adopted AI tool on its reference set after each model update, recording any change in error rates by condition.",
         [C], "WF-MONITOR", "remote", "no", **E),
    task(T["programme"], "Establish an organizational evaluation programme with shared reference sets and scheduled re-testing that is required before AI adoption or procurement.",
         [C], "WF-MANAGE", "remote", "partial", **E),
]
b = Bundle(C, "dc-cand-15")
b.ind("L1", "Labels reference items following the written guide without seeing tool outputs, matching expert labels on the check subset within the set tolerance.", "u", ["ws", "brm"], [T["label-reference"]], **E)
b.ind("L1", "Flags ambiguous reference items with a note stating the competing labels, so that adjudicators can resolve them.", "u", ["ws"], [T["label-reference"]], **E)
b.ind("L2", "Builds a reference set for one task with a sampling frame, labelling guide and double-labelled subset, reporting the agreement statistic.", "u", ["ws"], [T["build-set"]], attr="aut", **E)
b.ind("L2", "Computes precision and recall, or the task's equivalent measures, for an AI tool against the reference set, with intervals.", "u", ["ws"], [T["benchmark"]], attr="kno", **E)
b.ind("L3", "Compares candidate tools and the current human process on the same reference set, reporting error by subgroup or condition with a recommendation.", "u", ["pr", "bars"], [T["benchmark"]], attr="cpx", **E)
b.ind("L3", "Tests automated scoring of AI outputs against human scoring on a sample before an evaluation relies on it, documenting the agreement.", "a", ["ws"], [T["judge-check"]], attr="aug", **E)
b.ind("L3", "Designs multi-step environmental work tasks with reference answers and grading rubrics that separate acceptable from unacceptable AI outputs.", "u", ["pr"], [T["task-rubric"]], attr="gui", **E)
b.ind("L4", "Establishes an organizational evaluation programme that requires local evaluation before adoption or procurement, with shared reference sets and scheduled re-testing.", "u", ["pr", "bars"], [T["programme"]], attr="sco", **E)
b.ind("L4", "Reports evaluation results and re-test findings after each model update in a form procurement and governance bodies use for decisions.", "u", ["pr"], [T["retest"], T["programme"]], attr="sco", **E)
b.write_indicators()
write(competency(
    C, "Build task-specific evaluation sets and benchmark AI tools before adoption",
    "The capability to construct a representative, independently labelled reference set for a specific environmental task, measure candidate AI tools and the current human process against it, and document results so that adoption, procurement and monitoring decisions rest on local evidence. It includes designing task rubrics for evaluating AI on multi-step work.",
    "Constructs representative, independently labelled reference sets for specific environmental tasks; measures candidate AI tools and the current human process against them, including error by condition and citation accuracy; tests automated scoring against human scoring before relying on it; and documents results so that adoption, procurement and monitoring decisions rest on local evidence.",
    "practice", ("L1", "L4"), b.levels(), evidence="E", sources=["DC-037", "DC-032", "DC-060", "DC-041", "DC-001"],
    alt=["AI evaluation and benchmarking"], notation=CAND("DC-CAND-15"), reusability="cross-subsector", **E,
    note="DC specialist responsible-AI competency (ADR-0025 §2). Survivor: absorbs FS-C17. Distinct from v1 7.2.3 (individual calibration): this is an organizational evidence product. Benchmark names live in L4."))

# =============================================================================== DC-CAND-16
C = "seed:DC-CAND-16"
T = {"v1t2": "seed:v1-6.4.4-T2", **{k: f"seed:dc-16-{k}" for k in ("extract-table", "error-rates", "coding-scheme", "pipeline", "rules")}}
OUT_T += [
    rewrite_seed_task(T["v1t2"], "Code a public comment set into themes with machine assistance, tracing every coded statement to its source passage before summarizing for decision-makers.",
                      [C, ("seed:SC-C02", "contributing")], "WF-REVIEW", "remote", "partial", modes=["MODE-ENGAGE"], rel=["public"], **E,
                      note="Split from v1 6.4.4 (DC-CAND-16 part); responding to substantive comments in the record is SC-C02."),
    task(T["extract-table"], "Extract requirements from a plan or permit into a table with machine assistance, verifying each row against the cited page and paragraph.",
         [C], "WF-REVIEW", "remote", "partial", sources=["DC-001", "DC-035"], evidence="E", **E),
    task(T["error-rates"], "Measure the omission and fabrication rates of a machine-assisted extraction on a sample against a gold set, documenting limits for the responsible official.",
         [C], "WF-MONITOR", "remote", "partial", sources=["DC-037", "DC-032"], evidence="E", **E),
    task(T["coding-scheme"], "Design an extraction or coding scheme for a document set, with category definitions and decision rules that two coders can apply consistently.",
         [C], "WF-PLAN", "remote", "partial", **E),
    task(T["pipeline"], "Maintain a reusable text-analysis pipeline through model changes, re-running its evaluation set after each change before outputs enter a record.",
         [C], "WF-OPERATE", "remote", "no", sources=["DC-033"], evidence="E", **E),
    task(T["rules"], "Set organizational rules for when machine-derived text analyses may enter decision documents and how they are disclosed and audited.",
         [C], "WF-MANAGE", "remote", "partial", **E),
]
b = Bundle(C, "dc-cand-16")
b.ind("L1", "Extracts content from a plan, permit or comment set with an approved tool, verifying each extracted statement against the cited passage.", "a", ["sews"], [T["extract-table"], T["v1t2"]], **E)
b.ind("L1", "Marks each extracted row with its source page and paragraph, rejecting rows that cannot be traced to a passage.", "a", ["ra"], [T["extract-table"]], **E)
b.ind("L2", "Designs an extraction or coding scheme for a document set, with category definitions and decision rules two coders apply with recorded agreement.", "u", ["ws"], [T["coding-scheme"]], attr="gui", **E)
b.ind("L2", "Checks a machine-assisted extraction against a gold-set sample, reporting omission and fabrication rates and their limits to the responsible official.", "a", ["ws"], [T["error-rates"]], attr="aug", **E)
b.ind("L3", "Builds a reusable text-analysis pipeline whose citation tracing and evaluation checks run on every batch before outputs enter an administrative record.", "a", ["pr"], [T["pipeline"]], attr="sco", **E)
b.ind("L3", "Re-tests the pipeline on its evaluation set after a model change, stopping outputs from entering the record until error rates return within tolerance.", "s", ["ws", "ra"], [T["pipeline"]], attr="aug", **E)
b.ind("L4", "Sets organizational rules for when machine-derived text analyses may enter decision documents, specifying disclosure and audit requirements.", "u", ["pr", "bars"], [T["rules"]], attr="sco", **E)
b.ind("L4", "Audits a sample of decision documents for compliance with the text-analysis rules, reporting non-compliant uses and the corrections made.", "u", ["ra"], [T["rules"]], attr="sco", **E)
b.write_indicators()
write(competency(
    C, "Analyze regulatory, planning and public-comment text at scale with traceable citations",
    "The capability to extract, classify and summarize content from plans, environmental documents, permits, consultation documents and public comments with machine assistance, so that every extracted statement traces to a source passage and omission and fabrication rates are measured. Legal sufficiency judgments stay with the responsible official (statecraft).",
    "Uses machine-assisted extraction, classification and summarization on plans, environmental documents, permits, consultation documents and public comments; requires every extracted statement to trace to a source passage; measures omission and fabrication rates on a sample; documents limits for the responsible official; and maintains reusable pipelines through model changes, leaving the legal sufficiency judgment with the official.",
    "practice", ("L1", "L4"), b.levels(), evidence="E", sources=["DC-001", "DC-032", "DC-033", "DC-035", "DC-037"],
    derived=[df("v1:6.4.4", "split-from", "AI-assisted comment analysis with traceable citations")],
    alt=["Analyze regulatory, planning and public-comment text with LLMs, with traceable citations", "LLM-assisted text analysis"],
    notation=CAND("DC-CAND-16"), reusability="cross-subsector", **E,
    note="DC specialist responsible-AI competency (ADR-0025 §2) with SC secondary: outputs enter an administrative record. Title made technology-neutral per G-5 (the candidate title named LLMs; kept as altLabel). Agency tools are supplemental with analyst verification [E: DC-001]."))

# =============================================================================== DC-CAND-19
C = "seed:DC-CAND-19"
T = {"o1": "seed:v1-7.1.4-T1", **{k: f"seed:dc-19-{k}" for k in ("check-inventory", "risk-assessment", "propose-tier", "challenge", "triggers", "programme")}}
OUT_T += [
    rewrite_seed_task(T["o1"], "Evaluate a proposed AI adoption for a decision-support use against accountability, risk-tier and oversight criteria before the accountable official authorizes it.",
                      [C, ("seed:DC-CAND-13", "contributing")], "WF-MANAGE", "remote", "partial", **E,
                      note="Split from v1 7.1.4 (risk tiering → DC-CAND-19); listed as an additional task of the SC enactment seed:v1-7.1.4-A (authorization)."),
    task(T["check-inventory"], "Check that a model or AI output feeding a consequential decision is on the organization's inventory with an assigned owner before relying on it.",
         [C], "WF-MONITOR", "remote", "no", sources=["DC-007"], evidence="E", **E),
    task(T["risk-assessment"], "Complete a model risk assessment for a proposed use, covering purpose, consequence, failure modes, affected parties, validation status and monitoring plan.",
         [C], "WF-ASSESS", "remote", "partial", sources=["DC-007", "DC-005"], evidence="E", **E),
    task(T["propose-tier"], "Propose a risk tier for a model use from its risk assessment, stating the validation, review and monitoring requirements the tier carries.",
         [C], "WF-PLAN", "remote", "partial", sources=["DC-007", "DC-001"], evidence="E", **E),
    task(T["challenge"], "Provide independent challenge to a model owner's validation, recording findings and the conditions under which the model may stay in use.",
         [C], "WF-MONITOR", "remote", "partial", sources=["DC-059"], **E),
    task(T["triggers"], "Set monitoring and re-validation triggers for a deployed model, such as data drift, model updates or new uses, with criteria for pausing it.",
         [C], "WF-MONITOR", "remote", "partial", **E),
    task(T["programme"], "Run a model risk programme across an organization's portfolio, with inventory, tiering, independent validation and reporting to the governance body.",
         [C], "WF-MANAGE", "remote", "partial", sources=["DC-001"], evidence="E", **E),
]
b = Bundle(C, "dc-cand-19")
b.ind("L2", "Completes a model risk assessment for a use covering purpose, consequence, failure modes, affected parties, validation status and monitoring plan, proposing a tier.", "u", ["ws"], [T["risk-assessment"], T["propose-tier"]], **E)
b.ind("L2", "Checks that each model output used in a consequential decision is on the inventory with an assigned owner, flagging unlisted uses.", "a", ["ra", "sjt"], [T["check-inventory"]], **E)
b.ind("L3", "Provides independent challenge to a model owner's validation, documenting findings and the conditions for continued use.", "u", ["pr", "bars"], [T["challenge"]], attr="sco", **E)
b.ind("L3", "Sets monitoring and re-validation triggers for a deployed model, recommending pause or retirement when a trigger is met.", "u", ["pr"], [T["triggers"]], attr="gui", **E)
b.ind("L4", "Runs a model risk programme across a portfolio, maintaining the inventory, tier assignments and independent validation schedule reported to governance.", "u", ["pr", "bars"], [T["programme"]], attr="sco", **E)
b.ind("L4", "Decides when a model must not be used for a consequential decision, documenting the basis and notifying affected programmes.", "u", ["pr"], [T["programme"], T["o1"]], attr="aut", **E)
b.write_indicators()
write(competency(
    C, "Assess and manage model risk for consequential environmental decisions",
    "The capability to inventory models and AI systems that inform decisions, tier them by consequence, set proportional requirements for validation, documentation, independent review, monitoring and retirement, and decide when a model must not be used. Authorizing adoption stays with statecraft.",
    "Maintains an inventory of models and AI systems that inform environmental decisions; tiers them by consequence for payments, permits, enforcement, safety, rights and protected resources; sets proportional requirements for validation, documentation, independent review, monitoring and retirement; provides independent challenge to model owners; and decides when a model must not be used.",
    "practice", ("L2", "L4"), b.levels(), evidence="E", sources=["DC-001", "DC-007", "DC-005", "DC-059", "DC-051"],
    derived=[df("v1:7.1.4", "split-from", "risk tiering (ADR-0025 §3)")],
    alt=["Model risk management"], notation=CAND("DC-CAND-19"), reusability="cross-subsector", **E,
    note="DC specialist responsible-AI competency (ADR-0025 §2). Survivor: absorbs FS-C02 and the risk-tiering part of v1 7.1.4. The high-impact environmental archetypes are models that drive payments or enforcement [E: DC-001]. Policy instruments that define high-impact use live in the L5 registry."))

# =============================================================================== DC-CAND-20
C = "seed:DC-CAND-20"
T = {k: f"seed:dc-20-{k}" for k in ("requirements", "data-rights", "evaluate-claims", "read-documentation", "test-deliverable", "monitor-contract")}
OUT_T += [
    task(T["requirements"], "Write technical requirements and acceptance tests for an AI or analytics service before solicitation, tied to a local evaluation set.",
         [C], "WF-RESOURCE", "remote", "partial", sources=["DC-007"], evidence="E", **E),
    task(T["data-rights"], "Specify data-rights, portability and exit terms for an analytics contract so that public and partner data cannot train vendor models without consent.",
         [C], "WF-RESOURCE", "remote", "partial", sources=["DC-007"], evidence="E", **E, note="Absorbs FS-C10 (contracts that protect public data rights)."),
    task(T["evaluate-claims"], "Evaluate vendor performance claims for an AI service against a local evaluation set, reporting where the claims are not supported.",
         [C, ("seed:DC-CAND-15", "contributing")], "WF-RESOURCE", "remote", "partial", sources=["DC-041"], evidence="E", **E),
    task(T["read-documentation"], "Review the model, system and data documentation supplied with an AI service, flagging gaps against the solicitation's requirements.",
         [C], "WF-RESOURCE", "remote", "no", sources=["DC-008"], evidence="E", **E),
    task(T["test-deliverable"], "Test an AI service deliverable against the contract's acceptance criteria, recommending acceptance or rejection to the contracting officer with the results.",
         [C], "WF-RESOURCE", "remote", "partial", **E),
    task(T["monitor-contract"], "Monitor a contracted AI service's performance and change notices during the contract, triggering re-testing when the vendor changes the model.",
         [C], "WF-MONITOR", "remote", "no", sources=["DC-007"], evidence="E", **E),
]
b = Bundle(C, "dc-cand-20")
b.ind("L2", "Writes acceptance tests for an AI or analytics service that a vendor can run and a reviewer can score from the contract alone.", "u", ["ws"], [T["requirements"], T["test-deliverable"]], **E)
b.ind("L2", "Reviews the documentation supplied with an AI service against the solicitation's requirements, listing each missing or inadequate element.", "u", ["ws", "ra"], [T["read-documentation"]], **E)
b.ind("L3", "Evaluates vendor claims for an AI service on a local evaluation set, reporting the conditions where performance falls below the stated requirement.", "u", ["ws", "pr"], [T["evaluate-claims"]], attr="cpx", **E)
b.ind("L3", "Drafts data-rights, portability and exit terms for an analytics contract that bar training on public or partner data without consent.", "u", ["ws"], [T["data-rights"]], attr="kno", **E)
b.ind("L4", "Sets procurement standards for AI and analytics services across an organization, specifying required documentation, acceptance testing and monitoring by risk tier.", "u", ["pr", "bars"], [T["requirements"], T["monitor-contract"]], attr="sco", **E)
b.ind("L4", "Advises contracting officers on AI service acceptance and exit decisions, documenting the technical basis for each recommendation.", "u", ["pr"], [T["test-deliverable"]], attr="sco", **E)
b.write_indicators()
write(competency(
    C, "Specify, evaluate and accept AI and analytics services in procurement",
    "The capability to write requirements and acceptance tests for AI and analytics services, require model and data documentation and public data-rights terms, evaluate vendor claims against local evidence, and monitor contracted performance through to exit. Contracting authority stays with the warranted official.",
    "Writes requirements and acceptance tests for AI and analytics services; requires model and data documentation, data-rights terms that bar training on public or partner data without consent, portability and exit provisions, performance monitoring and change notification; evaluates vendor claims against a local evaluation set; and recommends acceptance or rejection of deliverables against the tests.",
    "practice", ("L2", "L4"), b.levels(), evidence="E", sources=["DC-007", "DC-008", "DC-041", "DC-001"],
    alt=["AI and analytics procurement"], notation=CAND("DC-CAND-20"), reusability="cross-subsector", **E,
    note="DC specialist responsible-AI competency; primary work function WF-RESOURCE (candidate_disposition). Survivor: absorbs FS-C10. Federal acquisition memos are L5 instruments; documentation formats (model, system and data cards) are L4."))

# =============================================================================== DC-CAND-21
C = "seed:DC-CAND-21"
T = {"a1": "seed:v1-3.5.5-T1", "a2": "seed:v1-3.5.5-T2", "a3": "seed:v1-3.5.5-T3", "o3": "seed:v1-7.1.4-T3",
     **{k: f"seed:dc-21-{k}" for k in ("governance-body", "catalogue", "sharing-agreements", "measures")}}
OUT_T += [
    rewrite_seed_task(T["a1"], "Set organizational rules that make the AI tools used in environmental work transparent and accountable, assigning an owner and review cycle to each use.",
                      [C], "WF-MANAGE", "remote", "partial", **E),
    rewrite_seed_task(T["a2"], "Review the organization's AI use cases for bias, transparency and accountability risks, directing corrective action where a use falls short.",
                      [C, ("seed:DC-CAND-19", "contributing")], "WF-MANAGE", "remote", "partial", **E),
    rewrite_seed_task(T["a3"], "Set governance rules that keep consequential AI-assisted decisions with accountable people and that weigh affected communities' input on AI priorities.",
                      [C], "WF-MANAGE", "remote", "partial", modes=["MODE-ENGAGE"], rel=["stakeholder"], **E,
                      note="Rewritten actor-neutral: the v1 framing of this task was retired by TN; its replacement indicator (no ingestion without consent) is held under TN-C03 (v1_disposition 3.5.5)."),
    rewrite_seed_task(T["o3"], "Monitor the effects of organizational AI governance on practitioner competence and review quality, revising the framework when either declines.",
                      [C], "WF-MANAGE", "remote", "partial", **E,
                      note="Split from v1 7.1.4; governance-framework monitoring goes to DC-CAND-21 (ADR-0025 §3)."),
    task(T["governance-body"], "Charter a data and AI governance body for an environmental organization, with stewardship roles, decision rights and data representation.",
         [C], "WF-MANAGE", "remote", "partial", sources=["DC-007", "DC-022"], evidence="E", **E),
    task(T["catalogue"], "Maintain an enterprise data catalogue and AI use-case inventory with an owner, sensitivity class and determination recorded for each entry.",
         [C], "WF-MANAGE", "remote", "no", sources=["DC-002"], evidence="E", **E),
    task(T["sharing-agreements"], "Negotiate data-sharing agreements with partner organizations that set access, use, attribution and withdrawal terms for shared environmental data.",
         [C], "WF-MANAGE", "remote", "partial", modes=["MODE-ENGAGE"], rel=["stakeholder"], **E),
    task(T["measures"], "Report data and AI value and risk measures for the organization's portfolio to executives, recommending investment and retirement decisions.",
         [C], "WF-MANAGE", "remote", "partial", sources=["DC-013"], evidence="E", **E),
]
b = Bundle(C, "dc-cand-21")
b.ind("L4", "Charters a data and AI governance body with stewardship roles, decision rights and escalation paths, documenting its scope and membership by function.", "u", ["pr"], [T["governance-body"]], **E)
b.ind("L4", "Maintains an enterprise data catalogue and AI use-case inventory in which every entry has an owner, sensitivity class and determination.", "u", ["ra"], [T["catalogue"]], **E)
b.ind("L4", "Directs corrective action on AI use cases that fail transparency or accountability reviews, recording the decision and a follow-up date.", "u", ["ra", "bars"], [T["a2"], T["a1"]], **E)
b.ind("L5", "Sets the organization's data and AI strategy with measures of value and risk, reporting results against them to executives or a board.", "u", ["pr", "bars"], [T["measures"]], attr="sco", **E)
b.ind("L5", "Negotiates data-sharing agreements across organizations that set access, use, attribution and withdrawal terms, recording each party's obligations.", "u", ["pr"], [T["sharing-agreements"]], attr="sco", **E)
b.ind("L5", "Revises the governance framework when monitoring shows declining practitioner competence or review quality, documenting the change and its basis.", "u", ["pr"], [T["o3"], T["a3"]], attr="gui", **E)
b.write_indicators()
write(competency(
    C, "Govern enterprise environmental data and AI portfolios",
    "The capability to set and run an organization's data and AI strategy: governance bodies and stewardship roles, data catalogue and inventory, data-sharing agreements, AI use-case inventory and determinations, workforce data and AI capability, and measures of data and AI value and risk.",
    "Sets and runs an organization's environmental data and AI strategy: governance bodies and stewardship roles, data catalogue and inventory, data-sharing agreements, AI use-case inventory and determinations, workforce data and AI capability, and measures of data and AI value and risk, keeping consequential decisions with accountable people.",
    "practice", ("L4", "L5"), b.levels(), evidence="E", sources=["DC-007", "DC-002", "DC-022", "DC-013", "DC-020"],
    derived=[df("v1:3.5.5", "merged-from", "ethical AI leadership folds into portfolio governance (v1_disposition 3.5.5)")],
    alt=["Enterprise data and AI governance"], notation=CAND("DC-CAND-21"), reusability="cross-subsector", **E,
    note="DC specialist responsible-AI competency at strategic span L4–L5 (candidate_disposition: WF-MANAGE, L4-L5). Receives the durable content of v1 3.5.5; the TN-required consent indicator for that content is held under TN-C03 and not authored here. Lifecycle emerging: enterprise data governance is long established, AI-portfolio governance is new (DC-007, DC-022)."))

for t in OUT_T:
    write(t, "tasks")
print("batch B written:", len(OUT_T), "tasks")
