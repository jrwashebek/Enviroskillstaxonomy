"""Batch E2: core DC candidate competencies (DC-CAND-03, -04, -06, -07, -08, -09, -11, -12, -18, -22), v1 2.4.4,
and re-pointing of tasks of superseded D2 seeds (2.3.1 split; 2.3.4, 2.5.1, 2.5.3, 2.7.1, 2.7.2 move-to-tools)."""
from lib import df, rewrite_seed_task, write
from spec import T, build

S = []
SEEDT = lambda c, n: f"seed:v1-{c}-T{n}"  # noqa: E731

# ------------------------------------------------------------------ DC-CAND-03 monitoring design
C = "seed:DC-CAND-03"
S.append(dict(
    id=C, prefix="dc-cand-03", span=("L2", "L4"), evidence="J", sources=["DC-035", "DC-044", "DC-001"],
    title="Design monitoring and sampling for valid environmental inference", alt=["Monitoring design"],
    definition="The capability to specify monitoring questions, indicators, sampling frames, sample sizes and detection methods so that results support the inferences and decisions they are meant to inform, including power to detect change and handling of imperfect detection, across field crews, sensors, remote sensing, environmental DNA, acoustic and community-science methods.",
    statement="Specifies monitoring questions, indicators, sampling frames, sample sizes and detection methods, whether field crews, sensors, remote sensing, environmental DNA, acoustic recorders or community science, so that results support the inferences and decisions they inform; estimates power to detect change; plans for imperfect detection; and ties monitoring to plan requirements and decision triggers.",
    note="Survivor (candidate_disposition DC-CAND-03): absorbs C-LM-01 (plan-level monitoring design, plan-requirement anchors P-LM-08) and the design content of v1 2.2.2. FC secondary: indicator selection and site representativeness need field judgment. Monitoring is the largest structured data demand in land-management plans (3,843 monitoring components) [E: DC-035].",
    tasks=[
        T("q", "seed:dc-03-questions", "Define the monitoring questions, indicators and decision triggers for a plan or programme so that each indicator answers a stated management question.", "WF-PLAN", "remote", "partial", sources=["DC-035"], evidence="E"),
        T("frame", "seed:dc-03-sample-design", "Design the sampling frame, allocation and sample size for a monitoring programme, documenting the inference each design choice supports.", "WF-PLAN", "remote-capable", "partial"),
        T("power", "seed:dc-03-power", "Estimate the power of a monitoring design to detect a specified change over a stated period, revising the design when power is insufficient.", "WF-PLAN", "remote", "partial"),
        T("det", "seed:dc-03-detection", "Plan for imperfect detection in a monitoring design, choosing repeat visits or detection models suited to the methods used.", "WF-PLAN", "remote", "partial"),
        T("mix", "seed:dc-03-method-mix", "Choose the mix of field, sensor, remote-sensing and community methods for a monitoring programme from cost, detection and comparability evidence.", "WF-PLAN", "remote-capable", "yes"),
        T("review", "seed:dc-03-review-design", "Review a monitoring programme's results against its design, recommending changes to sites, frequency or methods where its questions are not being answered.", "WF-LEARN", "remote", "partial"),
    ],
    inds=[
        ("L2", "Designs a sampling frame and allocation for a routine monitoring question, documenting the population the results represent.", "u", ["ws"], ["frame"]),
        ("L2", "Estimates sample size for a stated detectable change and confidence, using variance from pilot or published data.", "u", ["ws"], ["power"]),
        ("L3", "Designs a monitoring programme that combines field, sensor or remote methods, stating how detection differences between methods are handled.", "u", ["ws", "pr"], ["mix", "det"], {"attr": "cpx"}),
        ("L3", "Links each monitoring indicator to the management question and decision trigger it serves, removing indicators that answer no question.", "u", ["pr"], ["q"], {"attr": "sco"}),
        ("L4", "Sets monitoring design standards for a plan or programme, including power targets, detection handling and review cycles.", "u", ["pr"], ["q", "power"], {"attr": "gui"}),
        ("L4", "Evaluates whether a programme's monitoring answers its questions, ordering design changes where it does not and recording the evidence.", "u", ["pr"], ["review"], {"attr": "sco"}),
    ]))

# ------------------------------------------------------------------ DC-CAND-04 sensor pipelines (split from 2.3.1)
C = "seed:DC-CAND-04"
S.append(dict(
    id=C, prefix="dc-cand-04", span=("L2", "L4"), evidence="E", sources=["DC-001", "DC-046"],
    derived=[df("v1:2.3.1", "split-from", "network design and data pipelines (v1_disposition 2.3.1 position 2)")],
    title="Engineer environmental sensor-network and streaming data pipelines", alt=["Sensor data engineering"],
    definition="The capability to design and operate the data path from deployed sensors, telemetry, cameras and recorders to analysis-ready data: ingest, time synchronization, automated quality checks and anomaly flags, gap handling, storage, versioning and alerting, including edge processing where bandwidth is limited. Field deployment, siting and calibration stay field craft.",
    statement="Designs and operates the data path from deployed sensors, telemetry, cameras and recorders to analysis-ready data: ingest, time synchronization, automated quality checks and anomaly flags, gap handling, storage, versioning and alerting, including processing at the edge where bandwidth is limited; and documents the pipeline so that data remain traceable.",
    note="Split target of v1 2.3.1 (DC part; field deployment, siting, calibration and failure detection go to FC-C01). Absorbs automated QC design from v1 2.6.4 jointly with v1 2.2.3. Product names to L4 (T-1). Module enactment exists in water (seed:ena-dc-cand-04-water, WP-06).",
    tasks=[
        T("t3", SEEDT("2.3.1", 3), "Transfer data from field sensors into the programme's data system, checking completeness and timestamps against the deployment log.", "WF-OPERATE", "remote-capable", "partial", rewrite=True,
          note="Split from v1 2.3.1: data path (DC-CAND-04); installation and calibration tasks go to FC-C01."),
        T("ingest", "seed:dc-04-ingest", "Design the ingest of telemetered sensor data into a time-synchronized store, with gap detection and alerts for stalled stations.", "WF-OPERATE", "remote", "partial"),
        T("qc", "seed:dc-04-stream-qc", "Configure automated quality checks and anomaly flags on a streaming sensor feed, routing flagged data to review before release.", "WF-MONITOR", "remote", "partial",
          supports=[C, ("seed:v1-2.2.3", "contributing")]),
        T("ver", "seed:dc-04-versioning", "Version raw, flagged and corrected sensor data separately so that any released value can be traced to its raw record.", "WF-OPERATE", "remote", "no",
          supports=[C, ("seed:DC-CAND-05", "contributing")]),
        T("edge", "seed:dc-04-edge-processing", "Specify processing at the edge for a remote sensor or recorder where bandwidth is limited, stating what is kept, summarized or discarded.", "WF-PLAN", "remote-capable", "partial"),
        T("std", "seed:dc-04-pipeline-standards", "Set pipeline standards for a programme's sensor networks covering timing, quality flags, versioning, retention and recovery.", "WF-MANAGE", "remote", "partial"),
    ],
    inds=[
        ("L2", "Operates a sensor data pipeline from ingest to analysis-ready data, resolving gaps and timestamp errors against the deployment log.", "u", ["ra", "ws"], ["t3", "ingest"]),
        ("L2", "Keeps raw, flagged and corrected data versions separate, so that any released value can be traced to its raw record.", "u", ["ra"], ["ver"]),
        ("L3", "Designs ingest, synchronization, gap handling and alerting for a sensor network, documenting the design so that another engineer can operate it.", "u", ["pr"], ["ingest"], {"attr": "sco"}),
        ("L3", "Configures automated quality flags on a streaming feed, testing them against known faults before data are released to users.", "s", ["ws"], ["qc"], {"attr": "aug"}),
        ("L4", "Sets pipeline standards for a programme's sensor networks covering timing, quality flags, versioning, retention and recovery.", "u", ["pr"], ["std"], {"attr": "gui"}),
        ("L4", "Specifies edge processing for remote deployments with limited bandwidth, stating what is kept, summarized or discarded and the resulting data limits.", "u", ["pr"], ["edge"], {"attr": "cpx"}),
    ]))

# ------------------------------------------------------------------ DC-CAND-06 stewardship and publication (absorbs 2.2.5, C-LM-04)
C = "seed:DC-CAND-06"
S.append(dict(
    id=C, prefix="dc-cand-06", span=("L1", "L4"), evidence="J", sources=["DC-001", "DC-046", "DC-036"],
    derived=[df("v1:2.2.5", "merged-from", "metadata documentation of fitness for use")],
    title="Steward and publish environmental data for reuse", alt=["Data stewardship", "Metadata standards and management"],
    definition="The capability to prepare environmental datasets for discovery and reuse by others: metadata and vocabulary standards, repositories, licences and persistent identifiers, documented fitness for use, sensitivity review before release and review of machine-generated metadata; including stewardship of the authoritative datasets that plans and decisions rely on.",
    statement="Prepares environmental datasets for discovery and reuse: applies metadata and vocabulary standards; chooses repositories, licences and persistent identifiers; documents fitness for use; runs sensitivity review before release; reviews machine-generated metadata for accuracy; and stewards the authoritative datasets that plans and decisions rely on, including their versions and supersession.",
    note="Survivor (candidate_disposition DC-CAND-06): absorbs C-LM-04 (authoritative plan datasets) and v1 2.2.5 metadata content. Metadata editors, templates and named metadata standards are L4.",
    tasks=[
        T("t1", SEEDT("2.2.5", 1), "Document a dataset's sources, methods, formats and fitness for use in a metadata record that meets the applicable standard.", "WF-OPERATE", "remote", "no", rewrite=True),
        T("t2", SEEDT("2.2.5", 2), "Review machine-generated metadata for a dataset against the data and methods, correcting errors before the record is published.", "WF-MONITOR", "remote", "partial", rewrite=True),
        T("t3", SEEDT("2.2.5", 3), "Update metadata and version information whenever a public dataset changes, so that users can tell which version supports a result.", "WF-OPERATE", "remote", "no", rewrite=True),
        T("pkg", "seed:dc-06-release-package", "Prepare a dataset for public release with a licence, persistent identifier and repository suited to its users and sensitivity.", "WF-OPERATE", "remote", "no"),
        T("auth", "seed:dc-06-authoritative-dataset", "Steward an authoritative dataset that a plan or decision relies on, recording versions, supersession and the decisions each version supported.", "WF-OPERATE", "remote", "partial", sources=["DC-035"], evidence="E"),
        T("sens", "seed:dc-06-sensitivity-gate", "Run a sensitivity review on a dataset before release, routing sensitive fields to the protection procedure before publication.", "WF-MONITOR", "remote", "partial",
          supports=[C, ("seed:DC-CAND-07", "contributing")]),
        T("std", "seed:dc-06-publication-standards", "Set data-publication standards for a programme covering metadata, licences, identifiers, sensitivity review and version control.", "WF-MANAGE", "remote", "partial"),
    ],
    inds=[
        ("L1", "Completes a metadata record for an assigned dataset with sources, methods, formats and contact role, passing the programme's metadata check.", "u", ["ra"], ["t1"]),
        ("L1", "Updates the version and change note of a dataset's metadata each time the data change, so that users can identify the version used.", "u", ["ra"], ["t3"]),
        ("L2", "Reviews machine-generated metadata against the data and methods, correcting errors before the record is published.", "a", ["sews"], ["t2"], {"attr": "aug"}),
        ("L2", "Documents a dataset's fitness for use, stating the uses it supports and those it does not.", "u", ["ra", "ws"], ["t1"], {"attr": "kno"}),
        ("L3", "Prepares a dataset for reuse with a licence, persistent identifier and repository chosen for its users and sensitivity, documenting the choices.", "u", ["pr"], ["pkg", "sens"], {"attr": "aut"}),
        ("L3", "Stewards an authoritative dataset that decisions rely on, recording versions, supersession and the decisions each version supported.", "u", ["ra", "pr"], ["auth"], {"attr": "sco"}),
        ("L4", "Sets data-publication standards for a programme covering metadata, licences, identifiers, sensitivity review and version control.", "u", ["pr"], ["std"], {"attr": "gui"}),
        ("L4", "Audits a programme's published datasets against the standards, reporting gaps in metadata, licensing or versioning with corrective actions.", "u", ["ra"], ["std"], {"attr": "sco"}),
    ]))

# ------------------------------------------------------------------ DC-CAND-07 sensitive information (Tribal-specific indicators held, not authored)
C = "seed:DC-CAND-07"
S.append(dict(
    id=C, prefix="dc-cand-07", span=("L1", "L4"), evidence="E", sources=["DC-029", "DC-036", "DC-001"],
    title="Protect sensitive ecological, cultural and personal information in data products", alt=["Sensitive-data protection"],
    definition="The capability to determine and document the sensitivity of rare-species locations, cultural-resource information, personal data and information held under data-holder agreements; to apply generalization, withholding or controlled access proportionate to the risk without altering the stored record; and to check derived products, including AI training sets and summaries, for leakage.",
    statement="Determines and documents the sensitivity of rare-species locations, cultural-resource information, personal data and information held under data-holder agreements; applies generalization, withholding or controlled access proportionate to the risk; never alters the stored record; records reasons and review dates; and checks derived products such as maps, model outputs, AI summaries and training sets for leakage.",
    note="Candidate DC-CAND-07 (core-v2.0; X07). Indicators touching Tribal data or Indigenous knowledge are drafted only inside the hold (TN-C03, TN-C07; ADR-0007 §D) and are NOT authored here; this record is the actor-neutral technical execution layer and must be co-designed with TN. Observable practices follow GBIF sensitive-data guidance (documented reason and review date; generalize only the distributed copy) [E: DC-029].",
    tasks=[
        T("rec", "seed:dc-07-identify-sensitive", "Identify sensitive items in own data, such as rare-species locations, cultural-resource information or personal data, before sharing any copy.", "WF-OPERATE", "remote-capable", "partial"),
        T("det", "seed:dc-07-sensitivity-determination", "Make a sensitivity determination for a dataset, recording the reason, category, generalization level and review date for each sensitive element.", "WF-OPERATE", "remote", "partial", sources=["DC-029"], evidence="E"),
        T("gen", "seed:dc-07-generalize-copy", "Generalize sensitive fields in the distributed copy of a dataset, or withhold them, while leaving the stored record unaltered and explaining each withheld field.", "WF-OPERATE", "remote", "no", sources=["DC-029"], evidence="E"),
        T("leak", "seed:dc-07-leakage-check", "Check derived products such as maps, model outputs, AI summaries and training sets for leakage of withheld sensitive information before release.", "WF-MONITOR", "remote", "partial"),
        T("access", "seed:dc-07-access-design", "Design access controls and data-sharing terms for sensitive data used in analytics or AI workflows, agreed with the data holders.", "WF-PLAN", "remote", "partial", modes=["MODE-ENGAGE"], rel=["stakeholder"]),
        T("policy", "seed:dc-07-policy", "Set an organizational sensitive-data policy with review cycles and a hold-back register, reporting compliance to the data holders.", "WF-MANAGE", "remote", "partial", sources=["DC-036"], evidence="E"),
    ],
    inds=[
        ("L1", "Identifies rare-species locations, cultural-resource information and personal data in a mixed dataset before any copy leaves own control.", "u", ["ws", "sjt"], ["rec"]),
        ("L1", "Applies the organization's withholding or generalization rule to sensitive items before sharing, as checked on a mixed scenario dataset.", "u", ["ws"], ["rec", "gen"]),
        ("L2", "Records a sensitivity determination with reason, category, generalization level and review date for each sensitive element of a dataset.", "u", ["ra"], ["det"], {"attr": "aut"}),
        ("L2", "Generalizes only the distributed copy of a dataset, leaving the stored record unaltered and replacing withheld fields with explanatory wording.", "u", ["ws"], ["gen"], {"attr": "kno"}),
        ("L3", "Checks AI training sets, embeddings, retrieval corpora and high-resolution outputs for leakage of withheld information, documenting the controls applied.", "a", ["ws", "pr"], ["leak"], {"attr": "aug"}),
        ("L3", "Designs access controls and sharing terms for sensitive data in an analytics workflow, recording the data holders' agreement to them.", "u", ["pr"], ["access"], {"attr": "sco"}),
        ("L4", "Sets the organization's sensitive-data policy with review cycles and a hold-back register, reporting compliance to data holders.", "u", ["pr"], ["policy"], {"attr": "gui"}),
        ("L4", "Audits released products for sensitive-data leakage across a programme, ordering corrections and recording each finding.", "u", ["ra"], ["leak", "policy"], {"attr": "sco"}),
    ]))

# ------------------------------------------------------------------ DC-CAND-08 reproducible analysis (absorbs 2.2.4)
C = "seed:DC-CAND-08"
S.append(dict(
    id=C, prefix="dc-cand-08", span=("L1", "L4"), evidence="E", sources=["DC-001", "DC-032", "DC-046", "DC-030", "DC-037"],
    derived=[df("v1:2.2.4", "merged-from", "durable core of programming and scripting: reproducibility, testing, review of AI-generated code")],
    title="Conduct reproducible, auditable environmental analysis, including AI-assisted code", alt=["Programming and scripting", "Reproducible analysis"],
    definition="The capability to carry out analyses as re-runnable workflows with version control, recorded environments and inputs, tested code including code generated by AI assistants, and packaging that lets a peer or auditor reproduce results. Programming languages and libraries are L4.",
    statement="Carries out environmental analyses as re-runnable workflows, scripted or fully documented, under version control with recorded environments and inputs; tests and reviews code, including code generated by AI assistants; and packages analyses so that a peer or auditor can reproduce the results and find defects.",
    note="Successor of v1 2.2.4 (candidate_disposition DC-CAND-08): language names to L4 (T-1). v1 2.2.4 carried the taxonomy's CLD-High finding: AI code generation compresses the practice that builds debugging capacity [E: DC-046]; L1–L2 indicators keep unaided scripting.",
    tasks=[
        T("t1", SEEDT("2.2.4", 1), "Write a script that automates a repetitive data-processing step, with tests that confirm it reproduces the manual result on sample data.", "WF-ASSESS", "remote", "no", rewrite=True),
        T("t2", SEEDT("2.2.4", 2), "Script a spatial or statistical analysis end to end so that a peer can re-run it from raw inputs to final figures.", "WF-ASSESS", "remote", "no", rewrite=True),
        T("t3", SEEDT("2.2.4", 3), "Build a reproducible reporting workflow that regenerates result tables and figures when the underlying data are updated.", "WF-ASSESS", "remote", "no", rewrite=True,
          supports=[C, ("seed:DC-CAND-22", "contributing")]),
        T("ai", "seed:dc-08-review-ai-code", "Review AI-generated analysis code line by line against the analysis plan, testing it on cases with known answers before use.", "WF-MONITOR", "remote", "partial", sources=["DC-001"], evidence="E"),
        T("env", "seed:dc-08-record-environment", "Record the software environment, package versions and inputs of an analysis so that it can be re-run years later.", "WF-OPERATE", "remote", "no", supports=[C, ("seed:DC-CAND-05", "contributing")]),
        T("repro", "seed:dc-08-reproduce-other", "Reproduce another analyst's results from their materials, documenting each discrepancy and its cause.", "WF-MONITOR", "remote", "partial"),
        T("std", "seed:dc-08-reproducibility-standards", "Set reproducibility standards for a programme's analyses, including version control, environment capture and code review requirements.", "WF-MANAGE", "remote", "partial"),
    ],
    inds=[
        ("L1", "Runs a documented analysis workflow from raw inputs to outputs, recording the versions and inputs used.", "u", ["ra"], ["env", "t2"]),
        ("L1", "Commits analysis changes to version control with messages that state what changed and why.", "u", ["ra"], ["t1"]),
        ("L2", "Scripts an analysis end to end without AI code generation so that a peer can re-run it from raw inputs to final figures.", "u", ["ws"], ["t2", "t1"], {"attr": "aut"}),
        ("L2", "Tests AI-generated analysis code on cases with known answers before use, correcting any defect found.", "a", ["sews"], ["ai"], {"attr": "aug"}),
        ("L3", "Reproduces another analyst's results from their materials, documenting each discrepancy and its cause.", "u", ["ws"], ["repro"], {"attr": "sco"}),
        ("L3", "Finds a planted defect in AI-assisted analysis code during review, explaining its effect on the results.", "a", ["sews"], ["ai"], {"attr": "aug"}),
        ("L4", "Sets reproducibility standards for a programme's analyses, including version control, environment capture and code review requirements.", "u", ["pr"], ["std"], {"attr": "gui"}),
        ("L4", "Audits a sample of the programme's analyses by re-running them, reporting which fail to reproduce and why.", "u", ["ra"], ["std", "repro"], {"attr": "sco"}),
    ]))

# ------------------------------------------------------------------ DC-CAND-09 model fitness-for-purpose (absorbs 2.6.5)
C = "seed:DC-CAND-09"
S.append(dict(
    id=C, prefix="dc-cand-09", span=("L1", "L4"), evidence="E", sources=["DC-001", "DC-005", "DC-012"],
    derived=[df("v1:2.6.5", "merged-from", "interpretability methods and limits")],
    title="Evaluate model fitness-for-purpose and validate against independent evidence", alt=["Model evaluation", "AI model interpretation and explainability"],
    definition="The capability to judge whether a statistical, process, learned or AI model is fit for a stated decision: checking assumptions and domain of applicability, designing independent validation, quantifying error by condition, detecting use outside the model's envelope, interpreting what drives predictions and documenting limits.",
    statement="Judges whether a statistical, process, learned or AI model is fit for a stated decision: checks assumptions and domain of applicability; designs independent validation with blocked hold-outs or field reference data; quantifies error by condition; detects use outside the model's envelope; explains which inputs drive predictions; and documents the limits.",
    note="Candidate DC-CAND-09 (core-v2.0): DC enactment of the validation floor at model level; absorbs v1 2.6.5 interpretability content (model-risk content in DC-CAND-19). FC secondary for ecological models: out-of-distribution failure is usually first seen in the field.",
    tasks=[
        T("t1", SEEDT("2.6.5", 1), "Identify which inputs drive a model's predictions with an interpretation method suited to the model, testing whether the drivers are ecologically plausible.", "WF-MONITOR", "remote", "partial", rewrite=True),
        T("t2", SEEDT("2.6.5", 2), "Explain a model's main drivers and failure conditions to managers with visuals that show what the model does and does not capture.", "WF-ASSESS", "remote", "partial", rewrite=True,
          supports=[C, ("seed:DC-CAND-11", "contributing")], modes=["MODE-ENGAGE"]),
        T("t3", SEEDT("2.6.5", 3), "Document a model's purpose, data period, domain of applicability and known limits in a model record available to its users.", "WF-MONITOR", "remote", "no", rewrite=True,
          supports=[C, ("seed:DC-CAND-05", "contributing")]),
        T("env", "seed:dc-09-envelope-check", "Check whether a planned use of a model output falls inside the model's intended purpose, data period and area before relying on it.", "WF-MONITOR", "remote", "partial"),
        T("val", "seed:dc-09-independent-validation", "Validate a model against independent evidence with spatially or temporally blocked hold-outs or field reference data, reporting error by condition.", "WF-MONITOR", "remote-capable", "partial", sources=["DC-001"], evidence="E"),
        T("novel", "seed:dc-09-novel-conditions", "Test a model's performance under novel or non-analog conditions, stating where its predictions should not be used.", "WF-MONITOR", "remote", "partial", sources=["DC-001"], evidence="E"),
        T("challenge", "seed:dc-09-review-model", "Review another team's model before its results are used, testing its assumptions, calibration and performance under the decision's conditions.", "WF-MONITOR", "remote", "partial"),
    ],
    inds=[
        ("L1", "States a model's intended purpose, input data period and area before using its output, flagging any use outside them.", "u", ["ws", "sjt"], ["env"]),
        ("L1", "Fills the fitness-for-use checklist for a model output so that a reviewer finds it consistent with the model record.", "u", ["ra"], ["env", "t3"]),
        ("L2", "Validates a model against independent data with spatial or temporal blocking, reporting error by condition such as ecosystem type or season.", "u", ["ws"], ["val"], {"attr": "cpx"}),
        ("L2", "Identifies where a model should not be used from its validation results, stating the domain of applicability in the model record.", "u", ["ws"], ["val", "t3"], {"attr": "kno"}),
        ("L3", "Conducts novel-condition and driver tests of a model, documenting where predictions degrade and whether the drivers are plausible.", "u", ["ws", "pr"], ["novel", "t1"], {"attr": "cpx"}),
        ("L3", "Challenges another team's model before its results are used, documenting tested assumptions, calibration findings and conditions for use.", "u", ["pr", "bars"], ["challenge"], {"attr": "sco"}),
        ("L4", "Sets validation standards proportional to decision consequence for an organization's models, documenting the basis for each tier.", "u", ["pr"], ["challenge"], {"attr": "gui"}),
        ("L4", "Decides when a programme's model is retired from decision use, recording the performance evidence and the replacement.", "u", ["pr"], ["novel"], {"attr": "aut"}),
    ]))

# ------------------------------------------------------------------ DC-CAND-11 uncertainty
C = "seed:DC-CAND-11"
S.append(dict(
    id=C, prefix="dc-cand-11", span=("L1", "L4"), evidence="E", sources=["DC-047", "DC-008", "DC-035", "DC-044"],
    title="Quantify and communicate uncertainty for environmental decisions", alt=["Uncertainty communication"],
    definition="The capability to characterize uncertainty from measurement, sampling, model structure, parameters, scenarios and AI error, and to express it in forms decision-makers can use, stating what would change the conclusion and keeping caveats under pressure to drop them.",
    statement="Characterizes uncertainty from measurement, sampling, model structure, parameters, scenarios and AI error; quantifies the dominant sources; expresses uncertainty in forms decision-makers can use, such as ranges, probabilities, confidence language and confidence maps; states what would change the conclusion; and keeps caveats when pressed to drop them.",
    note="Candidate DC-CAND-11 (core-v2.0). SC secondary: framing uncertainty for an authorizing official is a statecraft act; producing a correct probability is data craft. Only 38 of 58,544 plan components mention uncertainty [E: DC-035].",
    tasks=[
        T("keep", "seed:dc-11-retain-uncertainty", "Report results with the uncertainty the method provides, such as intervals or confidence classes, keeping it in every summary of the result.", "WF-ASSESS", "remote", "no"),
        T("src", "seed:dc-11-quantify-sources", "Quantify the dominant sources of uncertainty in an analysis, such as measurement, sampling, model and scenario, stating which result would change the recommendation.", "WF-ASSESS", "remote", "partial"),
        T("brief", "seed:dc-11-brief-official", "Brief an authorizing official on the uncertainty of an analysis in decision terms, such as the risk of a wrong call and the value of more information.", "WF-ASSESS", "remote-capable", "partial", modes=["MODE-ENGAGE"]),
        T("fire", "seed:dc-11-incident-confidence-briefing", "Brief incident or programme leaders on the confidence of fire behaviour and weather projections, updating the briefing when observations diverge.", "WF-RESPOND", "remote-capable", "yes",
          supports=[C, ("seed:v1-2.4.2", "contributing")], sources=["DC-047"], evidence="E",
          regime={"mentorshipDependence": "H", "cycleDependence": "seasonal", "currencyDecay": "M"}),
        T("conv", "seed:dc-11-conventions", "Set organizational conventions for uncertainty language and visuals, testing whether decision-makers interpret them correctly.", "WF-LEARN", "remote", "partial"),
    ],
    inds=[
        ("L1", "Reports a result with the interval, confidence class or detection probability the method provides, keeping it in every summary.", "u", ["ws", "ra"], ["keep"]),
        ("L1", "States in plain language what the uncertainty in a reported result means for its use, as checked against the analyst's note.", "u", ["ws"], ["keep"]),
        ("L2", "Quantifies the dominant sources of uncertainty in an analysis, such as measurement, sampling and model error, stating what result would change the recommendation.", "u", ["ws"], ["src"], {"attr": "cpx"}),
        ("L2", "Writes an uncertainty section for an analysis that separates measurement, sampling, model and scenario uncertainty for the reader.", "u", ["ws"], ["src"], {"attr": "kno"}),
        ("L3", "Briefs an authorizing official on uncertainty in decision terms, such as the risk of a wrong call and the value of more information.", "u", ["sim", "bars"], ["brief", "fire"], {"attr": "sco"}),
        ("L3", "Keeps a contested caveat in a decision product when pressed to drop it, documenting the disagreement and its basis.", "u", ["pr", "sjt"], ["brief"], {"attr": "aut"}),
        ("L4", "Sets organizational conventions for uncertainty language and visuals, documenting the evidence behind each convention.", "u", ["pr"], ["conv"], {"attr": "gui"}),
        ("L4", "Tests whether decision-makers interpret the organization's uncertainty conventions correctly, revising conventions that are misread.", "u", ["pr"], ["conv"], {"attr": "sco"}),
    ]))

# ------------------------------------------------------------------ DC-CAND-12 forecast and scenario systems (absorbs 2.7.3, FS-C11)
C = "seed:DC-CAND-12"
S.append(dict(
    id=C, prefix="dc-cand-12", span=("L2", "L4"), lifecycle="emerging", evidence="E", sources=["DC-001"],
    derived=[df("v1:2.7.3", "merged-from", "digital twin development and management")],
    title="Build, run and validate environmental forecast and scenario systems", alt=["Build, run and validate environmental forecast systems and digital twins", "Digital twin development and management"],
    definition="The capability to assemble observation streams, process models, learned emulators or hybrids, data assimilation and update cycles into operational forecast or what-if systems; define their fitness for the decisions served; validate them continuously under changing conditions; manage versions, access and retirement; and communicate when the system should not be trusted.",
    statement="Assembles observation streams, process models, learned emulators or hybrids, data assimilation and update cycles into operational forecast or what-if systems; defines their fitness for the decisions they serve; validates them continuously under changing conditions; manages versions, access and retirement; and communicates when the system should not be trusted.",
    note="Survivor (candidate_disposition DC-CAND-12; lifecycle emerging, develop-only): absorbs FS-C11 (digital-twin lifecycle stewardship) and v1 2.7.3. Title made technology-neutral (G-5); 'digital twin' kept as altLabel. Programme and model names live in L4.",
    tasks=[
        T("t1", SEEDT("2.7.3", 1), "Build an operational forecast or scenario system for an ecosystem or infrastructure asset that assimilates real-time sensor observations.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("t2", SEEDT("2.7.3", 2), "Simulate alternative management actions in a forecast or scenario system, reporting the spread of outcomes and the system's validated range.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("t3", SEEDT("2.7.3", 3), "Maintain an operational forecast system's data feeds and model versions, re-validating after each change before results are released.", "WF-OPERATE", "remote", "partial", rewrite=True),
        T("skill", "seed:dc-12-skill-tracking", "Track a forecast system's skill against observations over time, notifying users when skill falls below the level their decisions require.", "WF-MONITOR", "remote", "partial"),
        T("fit", "seed:dc-12-fitness-requirements", "Define the fitness requirements of a forecast system for the decisions it serves, including lead time, resolution and acceptable error.", "WF-PLAN", "remote", "partial"),
        T("retire", "seed:dc-12-restrict-retire", "Decide when an operational forecast or scenario system should be restricted or retired, documenting the evidence and informing its users.", "WF-MONITOR", "remote", "partial"),
    ],
    inds=[
        ("L2", "Runs an operational forecast cycle to the published schedule, checking input feeds and flagging runs with missing or suspect observations.", "s", ["tbo", "ra"], ["t3"]),
        ("L2", "Tracks a forecast system's skill against observations, reporting skill by lead time and condition to users each cycle.", "u", ["ra"], ["skill"]),
        ("L3", "Builds a forecast or scenario system that assimilates real-time observations, documenting its components, update cycle and validated range.", "u", ["pr"], ["t1", "t2"], {"attr": "cpx"}),
        ("L3", "Re-validates the system after each model or data change before results are released, holding releases that fail the acceptance criteria.", "s", ["ra", "ws"], ["t3"], {"attr": "aug"}),
        ("L4", "Defines a forecast system's fitness requirements for the decisions it serves, including lead time, resolution and acceptable error.", "u", ["pr"], ["fit"], {"attr": "sco"}),
        ("L4", "Decides when a forecast or scenario system is restricted or retired, documenting the skill evidence and informing its users.", "u", ["pr"], ["retire"], {"attr": "aut"}),
    ]))

# ------------------------------------------------------------------ DC-CAND-18 knowledge corpora (absorbs 2.5.4)
C = "seed:DC-CAND-18"
S.append(dict(
    id=C, prefix="dc-cand-18", span=("L2", "L4"), lifecycle="emerging", evidence="E", sources=["DC-001", "DC-022"],
    derived=[df("v1:2.5.4", "merged-from", "knowledge management systems, rewritten to the durable stewardship function")],
    title="Curate authoritative guidance and knowledge corpora for retrieval", alt=["Curate authoritative knowledge corpora for retrieval-augmented AI", "Knowledge management systems"],
    definition="The capability to select, version and maintain the documents, protocols, datasets and metadata that staff and AI assistants retrieve from, marking authority, currency and supersession, removing withdrawn guidance, testing retrieval quality and assigning ownership so that answers come from the current authoritative source.",
    statement="Selects, versions and maintains the documents, protocols, datasets and metadata that staff and AI assistants retrieve from; marks authority, currency and supersession; removes withdrawn guidance; tests retrieval quality against known questions; and assigns ownership so that assistants and searches answer from the current, authoritative source.",
    note="Successor of v1 2.5.4 (candidate_disposition DC-CAND-18; lifecycle emerging). Retrieval assistants over agency guidance are among the most common environmental generative-AI pilots [E: DC-001]. Links to TX-D knowledge continuity. Title made technology-neutral (G-5).",
    tasks=[
        T("t1", SEEDT("2.5.4", 1), "Organize technical documents into a searchable library, recording the authority, currency and owner of each document.", "WF-OPERATE", "remote", "no", rewrite=True),
        T("t2", SEEDT("2.5.4", 2), "Tag lessons learned and protocols with controlled terms so that staff and assistants retrieve the current version for a stated task.", "WF-OPERATE", "remote", "partial", rewrite=True),
        T("t3", SEEDT("2.5.4", 3), "Write a guide showing new staff how to find authoritative guidance and recognize superseded material in the organization's knowledge systems.", "WF-LEARN", "remote", "partial", rewrite=True),
        T("remove", "seed:dc-18-remove-withdrawn", "Remove withdrawn or superseded guidance from a retrieval corpus within a set time of its withdrawal, recording each removal.", "WF-OPERATE", "remote", "no"),
        T("test", "seed:dc-18-test-retrieval", "Test an assistant's retrieval over a curated corpus with known questions, reporting answers drawn from superseded or non-authoritative sources.", "WF-MONITOR", "remote", "partial"),
        T("own", "seed:dc-18-assign-ownership", "Assign an owner role and review cycle to each collection in a knowledge corpus, so that every source has a named steward.", "WF-MANAGE", "remote", "partial"),
    ],
    inds=[
        ("L2", "Records authority, currency and owner for each document added to a corpus, so that superseded material is identifiable.", "u", ["ra"], ["t1", "t2"]),
        ("L2", "Removes withdrawn guidance from a retrieval corpus within the set time of its withdrawal, recording each removal.", "u", ["ra"], ["remove"]),
        ("L3", "Tests retrieval over a curated corpus with known questions, reporting answers drawn from superseded or non-authoritative sources and the fixes made.", "a", ["ws"], ["test"], {"attr": "aug"}),
        ("L3", "Designs the structure and controlled terms of a knowledge corpus so that staff and assistants retrieve the current version for a stated task.", "u", ["pr"], ["t2"], {"attr": "cpx"}),
        ("L4", "Sets corpus stewardship rules for an organization, assigning owners, review cycles and supersession procedures to each collection.", "u", ["pr"], ["own"], {"attr": "sco"}),
        ("L4", "Audits a corpus used by AI assistants for stale or unauthorized sources, ordering removals and reporting the results to its owners.", "u", ["ra"], ["test", "own"], {"attr": "sco"}),
    ]))

# ------------------------------------------------------------------ DC-CAND-22 decision-support products (absorbs 2.4.3)
C = "seed:DC-CAND-22"
S.append(dict(
    id=C, prefix="dc-cand-22", span=("L2", "L4"), evidence="J", sources=["DC-044", "DC-001"],
    derived=[df("v1:2.4.3", "merged-from", "decision support systems, rewritten to the decision context")],
    title="Design decision-support products for actual decision contexts", alt=["Decision support systems"],
    definition="The capability to build maps, dashboards, scenario tools and briefings around the real decision, its timing, authority and constraints, to test them with decision-makers, to show trade-offs and uncertainty, and to evaluate whether the product changed or improved decisions. Decision-support software is L4.",
    statement="Builds maps, dashboards, scenario tools and briefings around the real decision, its timing, authority and constraints; tests them with decision-makers; shows trade-offs and uncertainty; and evaluates whether the product changed or improved decisions.",
    note="Successor of v1 2.4.3 (candidate_disposition DC-CAND-22): rewritten to the decision context rather than the software (T-1). SC secondary: decision mapping depends on authority and timing.",
    tasks=[
        T("t1", SEEDT("2.4.3", 1), "Evaluate trade-offs among management alternatives with a decision-support model, documenting the criteria, weights and sensitivity of the ranking.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("t2", SEEDT("2.4.3", 2), "Build a dashboard that integrates the data sources a land-management decision needs, showing data currency and uncertainty for each measure.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("t3", SEEDT("2.4.3", 3), "Revise a decision-support product after testing with decision-makers, recording which features changed decisions and which were ignored.", "WF-LEARN", "remote", "partial", rewrite=True),
        T("map", "seed:dc-22-decision-map", "Map the decision a product must support, including who decides, when, under what authority and with which constraints, before design starts.", "WF-PLAN", "remote", "partial"),
        T("eval", "seed:dc-22-evaluate-use", "Evaluate whether a decision-support product changed or improved decisions, using decision records and interviews with its users.", "WF-LEARN", "remote", "partial"),
    ],
    inds=[
        ("L2", "Builds a decision-support product from a documented description of the decision, its timing and its constraints.", "u", ["ws"], ["t2"]),
        ("L2", "Shows the trade-offs and uncertainty of each alternative in a decision-support product, as confirmed by users in a structured test.", "u", ["ws"], ["t1"]),
        ("L3", "Tests a decision-support product with decision-makers before release, revising features that users misread or ignore.", "u", ["pr"], ["t3"], {"attr": "sco"}),
        ("L3", "Maps who decides, when, under what authority and with which constraints before designing a product, confirming the map with the decision-maker.", "u", ["pr", "bars"], ["map"], {"attr": "cpx"}),
        ("L4", "Evaluates whether a programme's decision-support products changed or improved decisions, using decision records and user interviews.", "u", ["pr"], ["eval"], {"attr": "sco"}),
        ("L4", "Sets design standards for a programme's decision-support products, including decision mapping, user testing and evaluation after release.", "u", ["pr"], ["map", "eval"], {"attr": "gui"}),
    ]))

# ------------------------------------------------------------------ v1 2.4.4 network analysis (carry, rewritten)
C = "seed:v1-2.4.4"
S.append(dict(
    id=C, seed=True, prefix="ind-v1-2.4.4", span=("L2", "L4"),
    title="Analyze ecological and social-ecological networks with graph methods", alt=["Network analysis"],
    definition="The capability to represent connectivity and spread as networks and to analyze them with graph methods: habitat corridors and connectivity, spread of pests, disease or fire, and social-ecological and institutional networks, with attention to how nodes and links are defined.",
    statement="Represents environmental connectivity and spread as networks and analyzes them with graph methods: habitat corridors and connectivity, spread of pests, disease or fire, and social-ecological and institutional networks; tests how results depend on how nodes and links are defined; and states what the network does and does not capture.",
    note="Carried (wording rewritten) by WP-04 as a DC specialist competency.",
    tasks=[
        T("t1", SEEDT("2.4.4", 1), "Map ecological corridors and connectivity with graph-based methods, testing how results change with resistance values and node definitions.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t2", SEEDT("2.4.4", 2), "Analyze a social-ecological network of organizations and resources to identify gaps in coordination for a management decision.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t3", SEEDT("2.4.4", 3), "Model the spread of pests, disease or fire across a network of sites, identifying the nodes where intervention most reduces spread.", "WF-PLAN", "remote", "partial", rewrite=True),
    ],
    inds=[
        ("L2", "Builds a connectivity network from habitat and resistance data for an assigned area, documenting how nodes and links were defined.", "u", ["ws"], ["t1"]),
        ("L2", "Computes standard network measures for an assigned network, explaining what each measure means for the management question.", "u", ["ws"], ["t2"]),
        ("L3", "Tests how network results change with node definitions and resistance values, reporting which conclusions hold across the alternatives.", "u", ["ws", "pr"], ["t1"], {"attr": "cpx"}),
        ("L3", "Models spread across a network of sites, identifying the nodes where intervention most reduces spread and stating the uncertainty.", "u", ["ws"], ["t3"], {"attr": "cpx"}),
        ("L4", "Sets network-analysis methods for a programme's connectivity or spread assessments, documenting data, parameter and validation requirements.", "u", ["pr"], ["t1", "t3"], {"attr": "gui"}),
        ("L4", "Resolves disagreements between connectivity analyses in a contested plan, documenting which network representation the programme adopts and why.", "u", ["pr", "bars"], ["t1"], {"attr": "cpx"}),
    ]))

for spec in S:
    build(spec)

# ------------------------------------------------------------------ tasks of superseded D2 seeds whose durable remainder is in another lane
R = []
N = lambda s: s + " Re-pointed by WP-04 (DC; owner of the D2 v1 row); content review by the target's owner."  # noqa: E731
# 2.3.1 split: installation and calibration -> FC-C01
R.append(rewrite_seed_task(SEEDT("2.3.1", 1), "Install soil moisture, temperature and weather sensors at remote field sites, recording location, height, orientation and installation conditions.",
                           ["seed:FC-C01"], "WF-MONITOR", "on-site-required", "yes", note=N("Split from v1 2.3.1: field deployment and siting (FC-C01).")))
R.append(rewrite_seed_task(SEEDT("2.3.1", 2), "Troubleshoot sensor malfunctions in the field with side-by-side checks against a reference instrument, recording each fault and fix.",
                           ["seed:FC-C01"], "WF-MONITOR", "on-site-required", "yes", note=N("Split from v1 2.3.1: calibration and failure detection (FC-C01).")))
# 2.3.4 move-to-tools: residual -> FC-C23
R.append(rewrite_seed_task(SEEDT("2.3.4", 1), "Collect species and habitat observations with a mobile data-collection app, checking location accuracy and completeness before submission.",
                           ["seed:FC-C23"], "WF-ASSESS", "on-site-required", "partial", note=N("v1 2.3.4 moved to L4 (seed:tool-field-data-apps); residual to FC-C23; app names moved to L4.")))
R.append(rewrite_seed_task(SEEDT("2.3.4", 2), "Configure a mobile data-collection form to a monitoring protocol, with validation rules that block incomplete or out-of-range entries.",
                           ["seed:FC-C23", ("seed:v1-2.2.3", "contributing")], "WF-PLAN", "remote-capable", "partial", note=N("v1 2.3.4 moved to L4; residual to FC-C23.")))
R.append(rewrite_seed_task(SEEDT("2.3.4", 3), "Train field teams to collect data with the programme's mobile forms, resolving device and synchronization problems during deployments.",
                           ["seed:FC-C23"], "WF-LEARN", "on-site-preferred", "partial", note=N("v1 2.3.4 moved to L4; residual to FC-C23.")))
# 2.5.1 move-to-tools: residual -> v1 5.2.2 facilitation
R.append(rewrite_seed_task(SEEDT("2.5.1", 1), "Plan a virtual meeting for dispersed field and office teams so that participants with limited connectivity can take part.",
                           ["seed:v1-5.2.2"], "WF-MANAGE", "remote", "no", modes=["MODE-ENGAGE"], note=N("v1 2.5.1 moved to L4 (seed:tool-meeting-platforms); facilitation to v1 5.2.2.")))
R.append(rewrite_seed_task(SEEDT("2.5.1", 2), "Facilitate a virtual working session with shared screens and small-group discussion, recording each participant group's input.",
                           ["seed:v1-5.2.2"], "WF-MANAGE", "remote", "no", modes=["MODE-ENGAGE"], note=N("v1 2.5.1 moved to L4; facilitation to v1 5.2.2.")))
R.append(rewrite_seed_task(SEEDT("2.5.1", 3), "Provide alternative ways to participate when platform problems or accessibility needs prevent people from joining a virtual meeting.",
                           ["seed:v1-5.2.2"], "WF-MANAGE", "remote", "no", modes=["MODE-ENGAGE"], note=N("v1 2.5.1 moved to L4; facilitation to v1 5.2.2.")))
# 2.5.3 move-to-tools: residual -> PS-C03 (TX-F)
R.append(rewrite_seed_task(SEEDT("2.5.3", 2), "Prepare progress reports for leadership from the project's tracking records, stating schedule and budget variance.",
                           ["seed:PS-C03"], "WF-MANAGE", "remote", "no", note=N("v1 2.5.3 moved to L4 (seed:tool-project-management-software); residual to PS-C03 (TX-F).")))
# 2.5.3 T1 and T3 were consolidated by WP-07 into seed:v1-3.1.1-T2 (merged-from); keep that consolidation.
from lib import load_orig  # noqa: E402
for n in (1, 3):
    o = load_orig(SEEDT("2.5.3", n), "tasks")
    o["status"] = "superseded"
    o["replacedBy"] = ["seed:v1-3.1.1-T2"]
    o["editorialNote"] = {"en": "Consolidated by WP-07 into seed:v1-3.1.1-T2 (PS-C03; derivedFrom merged-from); product names moved to L4 seed:tool-project-management-software (WP-04). " + o.get("editorialNote", {}).get("en", "")}
    R.append(o)
# 2.7.1 move-to-tools (AR watch): durable residue is spatial visual communication (v1 2.1.5)
R.append(rewrite_seed_task(SEEDT("2.7.1", 1), "Prepare spatial overlays of buried infrastructure, past conditions or zoning for display in the field, stating their positional accuracy.",
                           ["seed:v1-2.1.5"], "WF-ASSESS", "remote", "no", note=N("v1 2.7.1 moved to L4 watch (seed:tool-ar-tool-family); the overlay-preparation residue is visual communication (v1 2.1.5).")))
R.append(rewrite_seed_task(SEEDT("2.7.1", 2), "Verify the positional accuracy of spatial overlays shown on field display devices before crews rely on them for inspection.",
                           ["seed:v1-2.1.5", ("seed:FC-C02", "contributing")], "WF-MONITOR", "on-site-required", "partial", note=N("v1 2.7.1 moved to L4 watch; device fluency is L4.")))
R.append(rewrite_seed_task(SEEDT("2.7.1", 3), "Specify which spatial overlays field crews need on mobile displays for a decision, with the accuracy each overlay must meet.",
                           ["seed:v1-2.1.5"], "WF-PLAN", "remote", "partial", note=N("v1 2.7.1 moved to L4 watch.")))
# 2.7.2 move-to-tools (VR watch): residual -> v1 5.4.1 education
R.append(rewrite_seed_task(SEEDT("2.7.2", 1), "Design an immersive simulation of a remote or sensitive environment for learners, stating which features are accurate and which are illustrative.",
                           ["seed:v1-5.4.1"], "WF-LEARN", "remote", "partial", modes=["MODE-ENGAGE"], note=N("v1 2.7.2 moved to L4 watch (seed:tool-vr-tool-family); instructional design to v1 5.4.1.")))
R.append(rewrite_seed_task(SEEDT("2.7.2", 2), "Use immersive simulation to train learners on wildfire behaviour or restoration practice, checking that it supplements rather than replaces field exposure.",
                           ["seed:v1-5.4.1"], "WF-LEARN", "remote", "yes", modes=["MODE-ENGAGE"], note=N("v1 2.7.2 moved to L4 watch; instructional design to v1 5.4.1.")))
R.append(rewrite_seed_task(SEEDT("2.7.2", 3), "Align immersive learning content with curriculum outcomes in partnership with educators, documenting the outcome each module serves.",
                           ["seed:v1-5.4.1"], "WF-LEARN", "remote", "no", modes=["MODE-ENGAGE"], note=N("v1 2.7.2 moved to L4 watch; instructional design to v1 5.4.1.")))
for r in R:
    write(r)
print("batch E2 written:", len(S), "competencies;", len(R), "re-pointed superseded tasks")
