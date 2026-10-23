"""Batch F: remaining DC-primary v1 practice seeds in other domains (lane rule: v1 Craft Primary = DC).
1.5.1, 1.5.2, 1.5.3 (+DB-C38), 1.7.2, 1.7.4 (+1.7.3), 1.7.5, 3.7.3, 5.4.4, 5.6.2, 6.3.2, 6.7.1."""
from spec import T, build

S = []
ST = lambda c, n: f"seed:v1-{c}-T{n}"  # noqa: E731
NOTE = "Rewritten by WP-04 (DC lane: v1 craft primary DC, used only to route the seed; v1 tags are prior evidence, not v2 values)."

S.append(dict(
    id="seed:v1-1.5.1", seed=True, prefix="ind-v1-1.5.1", span=("L1", "L4"),
    title="Analyze and interpret climate observations and projections for management decisions", alt=["Climate data analysis and interpretation"],
    definition="The capability to obtain, process and interpret historical climate records and downscaled projections for a place, choosing scenarios, ensembles and downscaling methods suited to the decision, and to translate results into decision-relevant terms with their uncertainty. Specific climate data portals and model archives are L4.",
    statement="Obtains, processes and interprets historical climate records and downscaled projections for a management unit; chooses scenarios, ensembles and downscaling methods suited to the decision; analyzes trends and extremes; and translates results into decision-relevant variables with ranges and stated limits for managers and planners.",
    note=NOTE + " Tool-free per T-1 (v1_disposition 1.5.1).",
    tasks=[
        T("t1", ST("1.5.1", 1), "Process downscaled climate projections for a management unit, documenting the scenarios, models and downscaling method used and their known biases.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t2", ST("1.5.1", 2), "Analyze historical climate records for shifts in temperature, precipitation or extreme events, testing whether trends exceed natural variability.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t3", ST("1.5.1", 3), "Translate climate model outputs into decision-relevant variables for resource managers, stating the range across models and scenarios.", "WF-PLAN", "remote", "partial", rewrite=True,
          supports=["seed:v1-1.5.1", ("seed:DC-CAND-11", "contributing")]),
        T("ens", "seed:dc-151-ensemble-choice", "Choose the scenarios and model ensemble for a climate analysis from the decision's time horizon and risk tolerance, recording the rationale.", "WF-PLAN", "remote", "partial"),
    ],
    inds=[
        ("L1", "Retrieves the specified climate variables for a management unit from an assigned source, recording the scenario, model and period of each series.", "u", ["ws", "ra"], ["t1"]),
        ("L1", "Summarizes a historical climate record for a site as trends and extremes, matching a reviewer's check of the same record.", "u", ["ws"], ["t2"]),
        ("L2", "Analyzes trends and extremes in a climate record, testing whether a change exceeds natural variability before reporting it.", "u", ["ws"], ["t2"], {"attr": "kno"}),
        ("L2", "Reports projections for a management unit as ranges across models and scenarios, stating the known biases of the downscaling used.", "u", ["ws"], ["t1", "t3"], {"attr": "gui"}),
        ("L3", "Chooses scenarios, ensembles and downscaling for a non-routine decision, documenting why they fit its horizon and risk tolerance.", "u", ["pr"], ["ens"], {"attr": "cpx"}),
        ("L3", "Translates climate projections into the variables a management decision turns on, such as fire-weather days or low-flow duration, with stated limits.", "u", ["pr", "bars"], ["t3"], {"attr": "sco"}),
        ("L4", "Sets a programme's standards for climate data use, covering approved scenarios, ensemble practice and how uncertainty is reported.", "u", ["pr"], ["ens"], {"attr": "gui"}),
        ("L4", "Resolves conflicting climate analyses for a contested plan, documenting which projections the programme relies on and why.", "u", ["pr", "bars"], ["t3"], {"attr": "cpx"}),
    ]))

S.append(dict(
    id="seed:v1-1.5.2", seed=True, prefix="ind-v1-1.5.2", span=("L2", "L4"),
    title="Assess climate vulnerability of species, ecosystems, infrastructure and communities", alt=["Climate vulnerability assessment"],
    definition="The capability to evaluate how climate change threatens species, ecosystems, infrastructure and communities by assessing exposure, sensitivity and adaptive capacity with an established framework, stating confidence, and to rank vulnerabilities so that adaptation can be prioritized. Named index tools are L4.",
    statement="Evaluates how climate change threatens species, ecosystems, infrastructure and communities: assesses exposure, sensitivity and adaptive capacity with an established framework; states the confidence of each rating and the evidence behind it; ranks vulnerabilities; and turns findings into prioritized recommendations for managers.",
    note=NOTE + " Carried (wording rewritten); vulnerability index tools moved to L4 (seed:tool-climate-vulnerability-indices).",
    tasks=[
        T("t1", ST("1.5.2", 1), "Conduct a vulnerability assessment for focal species or ecosystems with an established framework, stating the evidence and confidence for each rating.", "WF-ASSESS", "remote-capable", "partial", rewrite=True),
        T("t2", ST("1.5.2", 2), "Rate climate exposure, sensitivity and adaptive capacity for each management unit from documented evidence, flagging ratings that rest on expert judgment alone.", "WF-ASSESS", "remote-capable", "partial", rewrite=True),
        T("t3", ST("1.5.2", 3), "Synthesize vulnerability findings into ranked recommendations for managers, showing how confidence differs among the ranked items.", "WF-PLAN", "remote", "partial", rewrite=True),
    ],
    inds=[
        ("L2", "Rates exposure, sensitivity and adaptive capacity for an assigned species or unit with a stated framework, citing the evidence for each rating.", "u", ["ws"], ["t1", "t2"]),
        ("L2", "Flags vulnerability ratings that rest on expert judgment alone, stating what evidence would confirm or change them.", "u", ["ws"], ["t2"]),
        ("L3", "Designs a vulnerability assessment across several species, systems or communities, choosing the framework and documenting how ratings are combined.", "u", ["pr"], ["t1"], {"attr": "cpx"}),
        ("L3", "Ranks vulnerabilities for managers with confidence shown for each item, so that low-confidence rankings are not treated as firm.", "u", ["pr"], ["t3"], {"attr": "sco"}),
        ("L4", "Sets vulnerability-assessment methods for a programme or region, specifying frameworks, evidence standards and update cycles.", "u", ["pr"], ["t1"], {"attr": "gui"}),
        ("L4", "Reconciles vulnerability assessments made by different partners for a shared landscape, documenting the agreed ratings and remaining disagreements.", "u", ["pr", "bars"], ["t3"], {"attr": "sco"}),
    ]))

S.append(dict(
    id="seed:v1-1.5.3", seed=True, prefix="ind-v1-1.5.3", span=("L2", "L4"),
    title="Plan climate adaptation and integrate climate risk into plans and capital decisions", alt=["Climate adaptation planning"],
    definition="The capability to develop adaptation strategies and actions for species, ecosystems, infrastructure and communities, to evaluate options against climate risk and uncertainty, and to integrate climate risk into management plans, infrastructure design and capital decisions. Decision-support software is L4.",
    statement="Develops adaptation strategies and actions for species, ecosystems, infrastructure and communities; evaluates options against climate risk, cost and uncertainty; integrates climate risk into management plans, infrastructure design criteria and capital decisions; and sets monitoring triggers for revisiting choices as conditions change.",
    note=NOTE + " Absorbs DB-C38 (integrate climate risk into infrastructure and capital decisions; candidate_disposition merge-into v1:1.5.3). FS-C16 stays a watch item.",
    tasks=[
        T("t1", ST("1.5.3", 1), "Facilitate an adaptation planning workshop with resource managers and stakeholders, recording the options considered and the reasons for each choice.", "WF-PLAN", "remote-capable", "partial", rewrite=True,
          modes=["MODE-ENGAGE"], rel=["stakeholder"]),
        T("t2", ST("1.5.3", 2), "Develop climate adaptation strategies that fit the organization's mandates and planning frameworks, stating the climate assumptions each strategy depends on.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("t3", ST("1.5.3", 3), "Evaluate adaptation options against climate risk, cost and uncertainty, documenting how each option performs across plausible futures.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("cap", "seed:dc-153-capital-climate-risk", "Integrate projected climate loads into design criteria for an infrastructure or capital project, documenting the scenario and return period used.", "WF-PLAN", "remote", "partial",
          note="Absorbs DB-C38 (climate risk in infrastructure and capital decisions)."),
        T("trig", "seed:dc-153-adaptation-triggers", "Set monitoring triggers that prompt revisiting an adaptation decision when observed conditions cross stated thresholds.", "WF-LEARN", "remote", "partial"),
    ],
    inds=[
        ("L2", "Drafts adaptation options for an assigned unit or asset, stating the climate assumption each option depends on.", "u", ["ws"], ["t2"]),
        ("L2", "Records the options considered in an adaptation workshop and the reasons for each choice, so that the decision can be revisited.", "u", ["ra"], ["t1"]),
        ("L3", "Evaluates adaptation options across plausible futures for cost and risk, documenting which options hold up across scenarios.", "u", ["pr"], ["t3"], {"attr": "cpx"}),
        ("L3", "Integrates projected climate loads into the design criteria of a capital project, documenting the scenario and return period chosen.", "u", ["pr"], ["cap"], {"attr": "kno"}),
        ("L4", "Sets an organization's approach to climate risk in plans and capital decisions, specifying scenarios, design margins and review triggers.", "u", ["pr"], ["cap", "trig"], {"attr": "sco"}),
        ("L4", "Sets monitoring triggers for adaptation decisions across a programme, revising decisions when observed conditions cross the thresholds.", "u", ["pr", "ra"], ["trig"], {"attr": "gui"}),
    ]))

S.append(dict(
    id="seed:v1-1.7.2", seed=True, prefix="ind-v1-1.7.2", span=("L3", "L4"), lifecycle="emerging",
    title="Plan assisted migration and managed relocation of species and genotypes", alt=["Assisted migration and managed relocation"],
    definition="The capability to evaluate candidate species, populations and situations for assisted migration, seed transfer or translocation, weigh ecological, genetic and invasion risks against benefits, and design implementation and monitoring protocols that test outcomes.",
    statement="Evaluates candidate species, populations and sites for assisted migration, seed transfer or translocation; weighs ecological, genetic, disease and invasion risks against expected benefits under projected climates; designs implementation and monitoring protocols that test outcomes; and documents decisions for review.",
    note=NOTE + " Carried (wording rewritten); lifecycle emerging (v1_disposition 1.7.2). Management application is enacted in forest (seed transfer) and wildlife (translocation) modules (WP-06).",
    tasks=[
        T("t1", ST("1.7.2", 1), "Evaluate candidate species, populations and sites for assisted migration against projected climate suitability and documented biological limits.", "WF-PLAN", "remote-capable", "yes", rewrite=True),
        T("t2", ST("1.7.2", 2), "Assess the ecological, genetic, disease and invasion risks and expected benefits of a proposed managed relocation, documenting the evidence.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t3", ST("1.7.2", 3), "Design implementation and monitoring protocols for an assisted migration trial so that survival and effects at the receiving site can be measured.", "WF-PLAN", "remote-capable", "yes", rewrite=True),
    ],
    inds=[
        ("L3", "Evaluates a candidate assisted migration against climate suitability, genetic and invasion risks, documenting the evidence for each risk rating.", "u", ["pr"], ["t1", "t2"]),
        ("L3", "Designs a monitoring protocol for an assisted migration trial that measures survival and effects at the receiving site against stated thresholds.", "u", ["pr"], ["t3"]),
        ("L4", "Sets a programme's decision criteria for assisted migration and seed transfer, specifying evidence requirements and conditions for stopping a trial.", "u", ["pr"], ["t1", "t3"], {"attr": "gui"}),
        ("L4", "Reviews assisted-migration proposals across a programme, recommending approval, modification or rejection with the documented basis for each.", "u", ["pr", "bars"], ["t2"], {"attr": "sco"}),
    ]))

S.append(dict(
    id="seed:v1-1.7.4", seed=True, prefix="ind-v1-1.7.4", span=("L2", "L4"),
    title="Plan for ecological transformation with resist, accept or direct strategies", alt=["Ecological transformation management", "Climate refugia identification"],
    definition="The capability to plan management of ecosystems undergoing fundamental change by choosing, with evidence, whether to resist, accept or direct transformation; identifying climate refugia; and setting goals for function and value where historical conditions cannot be restored.",
    statement="Plans management of ecosystems undergoing fundamental change: identifies trajectories and climate refugia; chooses, with stated evidence, whether to resist, accept or direct transformation at each site; sets goals for ecological function and value where historical conditions cannot be restored; and monitors whether the chosen strategy is working.",
    note=NOTE + " Absorbs v1 1.7.3 refugia identification (its tasks point here).",
    tasks=[
        T("r1", ST("1.7.3", 1), "Map potential climate refugia from topographic, hydrologic and climate data, stating the assumptions and validation of the refugia model.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("r2", ST("1.7.3", 2), "Evaluate whether mapped refugia can support climate-sensitive species, using field and monitoring evidence of their current condition.", "WF-ASSESS", "remote-capable", "yes", rewrite=True),
        T("r3", ST("1.7.3", 3), "Integrate refugia into conservation prioritization and land protection plans, documenting how refugia rank against other criteria.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("t1", ST("1.7.4", 1), "Develop a management strategy for an ecosystem in transition, choosing to resist, accept or direct change at each site with stated evidence.", "WF-PLAN", "remote-capable", "yes", rewrite=True),
        T("t2", ST("1.7.4", 2), "Set management goals for function and value where historical reference conditions are no longer achievable, documenting the reasoning.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("t3", ST("1.7.4", 3), "Monitor whether a transformation strategy sustains the targeted ecological functions, revising the strategy when indicators fall below thresholds.", "WF-LEARN", "remote-capable", "partial", rewrite=True),
    ],
    inds=[
        ("L2", "Maps potential climate refugia for an assigned area from topographic, hydrologic and climate data, stating the model's assumptions.", "u", ["ws"], ["r1"]),
        ("L2", "Compiles field and monitoring evidence of current condition for mapped refugia, flagging refugia without supporting observations.", "u", ["ws"], ["r2"]),
        ("L3", "Chooses resist, accept or direct strategies for sites in transition, documenting the evidence and the conditions that would change the choice.", "u", ["pr"], ["t1"], {"attr": "cpx"}),
        ("L3", "Sets function-based goals where historical conditions cannot be restored, stating the indicators and thresholds used to judge success.", "u", ["pr"], ["t2", "t3"], {"attr": "gui"}),
        ("L4", "Sets a programme's framework for transformation decisions across a landscape, specifying evidence requirements and review cycles.", "u", ["pr"], ["t1", "r3"], {"attr": "sco"}),
        ("L4", "Revises transformation strategies across a landscape when monitoring shows targeted functions declining, documenting each change and its basis.", "u", ["pr", "ra"], ["t3"], {"attr": "aut"}),
    ]))

S.append(dict(
    id="seed:v1-1.7.5", seed=True, prefix="ind-v1-1.7.5", span=("L3", "L4"),
    title="Plan for non-analog ecological futures", alt=["Non-analog futures planning"],
    definition="The capability to recognize when future conditions are likely to lack historical precedent, such as novel climates or species combinations, and to design plans that remain robust and adaptable across such futures rather than optimized for one expected state.",
    statement="Recognizes when future ecological conditions are likely to be non-analog, such as novel climates or species combinations; designs plans that perform acceptably across divergent futures rather than one expected state; builds flexibility, monitoring triggers and adaptive capacity into long-term plans; and documents the assumptions that would invalidate them.",
    note=NOTE + " Carried (wording rewritten); linked to FS-C15 horizon scanning and to validation under nonstationarity (DC-CAND-12).",
    tasks=[
        T("t1", ST("1.7.5", 1), "Identify where future conditions in a planning area are likely to be non-analog, such as novel climates or species combinations, citing the analyses used.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t2", ST("1.7.5", 2), "Design a planning approach that performs acceptably across divergent futures, testing candidate strategies against a set of contrasting scenarios.", "WF-PLAN", "remote", "partial", rewrite=True),
        T("t3", ST("1.7.5", 3), "Build monitoring triggers and decision points into a long-term plan so that it can change course when assumptions fail.", "WF-PLAN", "remote", "partial", rewrite=True),
    ],
    inds=[
        ("L3", "Identifies where a planning area is likely to face non-analog conditions, citing the analyses and stating their confidence.", "u", ["pr"], ["t1"]),
        ("L3", "Tests candidate strategies against contrasting scenarios, documenting which strategies perform acceptably across all of them.", "u", ["pr"], ["t2"]),
        ("L4", "Sets a programme's approach to planning under non-analog futures, specifying scenario sets, robustness criteria and decision points.", "u", ["pr"], ["t2", "t3"], {"attr": "gui"}),
        ("L4", "Builds decision points and monitoring triggers into a long-term plan, documenting the assumptions whose failure would change course.", "u", ["pr"], ["t3"], {"attr": "sco"}),
    ]))

S.append(dict(
    id="seed:v1-3.7.3", seed=True, prefix="ind-v1-3.7.3", span=("L2", "L4"),
    title="Assess environmental impacts across product life cycles to guide circular design", alt=["Product lifecycle assessment and design"],
    definition="The capability to conduct life-cycle assessment of products, materials and services to an accepted method, with stated system boundaries, functional units, inventory data quality and impact methods, and to use the results to guide design for durability, repair, disassembly and material recovery. LCA software and inventory databases are L4.",
    statement="Conducts life-cycle assessments of products, materials and services with stated goal, scope, system boundaries and functional unit; documents inventory data quality and impact methods; tests sensitivity of conclusions; and uses results to guide design for durability, repair, disassembly and material recovery, including traceability of materials across the chain.",
    note=NOTE + " Carried (wording rewritten): v1 tasks named cloud LCA software, AI-powered design tools and blockchain passports; those are L4 (seed:tool-lca-software, seed:tool-distributed-ledger-tools).",
    tasks=[
        T("t1", ST("3.7.3", 1), "Conduct a life-cycle assessment of a product or material with a stated goal, scope, functional unit and documented inventory data quality.", "WF-ASSESS", "remote", "no", rewrite=True),
        T("t2", ST("3.7.3", 2), "Recommend design changes that improve a product's disassembly, repair and material recovery, quantifying the life-cycle effect of each change.", "WF-PLAN", "remote", "no", rewrite=True),
        T("t3", ST("3.7.3", 3), "Specify the material and provenance data a product passport must carry so that materials can be traced and recovered at end of life.", "WF-PLAN", "remote", "no", rewrite=True),
        T("sens", "seed:dc-373-lca-sensitivity", "Test how a life-cycle assessment's conclusions change with system boundaries, allocation rules and inventory choices, reporting which conclusions are robust.", "WF-ASSESS", "remote", "no"),
    ],
    inds=[
        ("L2", "Conducts a life-cycle assessment to an accepted method with stated goal, scope, functional unit and inventory data quality.", "u", ["ws"], ["t1"]),
        ("L2", "Documents the impact methods and data sources of a life-cycle assessment so that a reviewer can repeat it.", "u", ["ra"], ["t1"]),
        ("L3", "Tests the sensitivity of life-cycle conclusions to boundaries, allocation and inventory choices, reporting which conclusions are robust.", "u", ["ws", "pr"], ["sens"], {"attr": "cpx"}),
        ("L3", "Recommends circular-design changes with the quantified life-cycle effect of each, stating the assumptions behind the estimates.", "u", ["pr"], ["t2"], {"attr": "sco"}),
        ("L4", "Sets life-cycle assessment standards for an organization's products, specifying methods, data-quality requirements and review before public claims.", "u", ["pr"], ["t1", "sens"], {"attr": "gui"}),
        ("L4", "Specifies the material and provenance data that product passports must carry across a supply chain, documenting the data-quality rules.", "u", ["pr"], ["t3"], {"attr": "sco"}),
    ]))

S.append(dict(
    id="seed:v1-5.4.4", seed=True, prefix="ind-v1-5.4.4", span=("L1", "L4"),
    title="Coordinate community-science data collection to programme data-quality standards", alt=["Citizen science coordination"],
    definition="The capability to design and run programmes in which members of the public collect environmental data, with protocols, training, verification and data-quality controls that make the contributions usable for monitoring and management, while protecting participants and sensitive information.",
    statement="Designs and runs programmes in which members of the public collect environmental data: sets questions, protocols and training; verifies submissions and controls data quality; protects participants' personal data and sensitive species locations; compiles and analyzes contributions with their known biases; and reports results back to participants.",
    note=NOTE + " Carried (wording rewritten); community-science platforms are L4 (seed:tool-inaturalist).",
    tasks=[
        T("t1", ST("5.4.4", 1), "Design a community-science project for ecological monitoring, matching the protocol and sampling to what volunteers can collect reliably.", "WF-PLAN", "remote-capable", "partial", rewrite=True, modes=["MODE-ENGAGE"], rel=["public"]),
        T("t2", ST("5.4.4", 2), "Train volunteers to follow the standardized protocol and submit accurate observations, checking a sample of their submissions afterwards.", "WF-ASSESS", "on-site-preferred", "partial", rewrite=True, modes=["MODE-ENGAGE"], rel=["public"]),
        T("t3", ST("5.4.4", 3), "Analyze community-science contributions, accounting for observer effort and spatial bias before reporting results.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("ver", "seed:dc-544-verify-submissions", "Verify community-science submissions against the protocol and expert review, flagging records that cannot be used and explaining why.", "WF-MONITOR", "remote-capable", "partial"),
    ],
    inds=[
        ("L1", "Checks volunteer submissions against the protocol checklist, flagging incomplete or out-of-range records for expert review.", "u", ["ra"], ["ver"]),
        ("L1", "Explains the protocol to volunteers in a session, so that their next submissions pass the checklist.", "u", ["tbo"], ["t2"]),
        ("L2", "Analyzes community-science data with adjustment for observer effort and spatial bias, stating the remaining limits of the results.", "u", ["ws"], ["t3"], {"attr": "kno"}),
        ("L2", "Withholds or generalizes sensitive species locations and participants' personal data before sharing community-science results.", "u", ["ws"], ["t3"], {"attr": "aut"}),
        ("L3", "Designs a community-science project whose protocol and sampling match what volunteers can collect reliably for the stated question.", "u", ["pr"], ["t1"], {"attr": "cpx"}),
        ("L3", "Sets verification rules for submissions with expert reviewers, measuring the share of records that meet the programme's data-quality standard.", "u", ["pr", "ra"], ["ver"], {"attr": "sco"}),
        ("L4", "Sets a programme's standards for using community-science data in monitoring and management decisions, including quality thresholds and reporting back to participants.", "u", ["pr"], ["t1", "t3"], {"attr": "gui"}),
        ("L4", "Evaluates whether community-science data meet the programme's decision needs, revising protocols or uses where they do not.", "u", ["pr"], ["t3"], {"attr": "sco"}),
    ]))

S.append(dict(
    id="seed:v1-5.6.2", seed=True, prefix="ind-v1-5.6.2", span=("L1", "L4"),
    title="Conduct social science research on the human dimensions of environmental issues", alt=["Social science research methods"],
    definition="The capability to design and carry out qualitative and quantitative social science research, such as surveys, interviews and focus groups, on the human dimensions of environmental issues, with sound sampling, ethical protections for participants, appropriate analysis and accessible reporting.",
    statement="Designs and carries out surveys, interviews, focus groups and other social science research on the human dimensions of environmental issues; samples respondents to support the intended inference; protects participants' consent and confidentiality; analyzes qualitative and quantitative data with appropriate methods; and reports findings accessibly with their limits.",
    note=NOTE + " Carried (wording rewritten). Research with Tribal communities follows the held TN content (ADR-0007) and is not authored here.",
    tasks=[
        T("t1", ST("5.6.2", 1), "Design a survey, interview or focus-group study of stakeholder perspectives with a sampling plan that supports the intended inference.", "WF-ASSESS", "remote-capable", "partial", rewrite=True, modes=["MODE-ENGAGE"], rel=["stakeholder"]),
        T("t2", ST("5.6.2", 2), "Analyze quantitative and qualitative social science data with methods suited to the design, documenting coding rules and statistical choices.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t3", ST("5.6.2", 3), "Present social science findings to managers and the public in accessible formats, stating the sample's limits and what the findings do not show.", "WF-ASSESS", "remote-capable", "partial", rewrite=True, modes=["MODE-ENGAGE"], rel=["public"]),
        T("eth", "seed:dc-562-participant-protection", "Obtain informed consent and protect respondents' confidentiality in a social science study, removing identifying details before data are shared.", "WF-ASSESS", "remote-capable", "partial"),
    ],
    inds=[
        ("L1", "Conducts assigned interviews or surveys following the study protocol, recording responses accurately and noting deviations.", "u", ["tbo", "ra"], ["t1"]),
        ("L1", "Removes identifying details from collected responses before data are shared, as checked against the study's confidentiality rules.", "u", ["ra"], ["eth"]),
        ("L2", "Designs a survey or interview study with a sampling plan that supports the intended inference, documenting known sources of bias.", "u", ["ws"], ["t1"], {"attr": "aut"}),
        ("L2", "Analyzes qualitative responses with a documented coding scheme, reporting agreement between coders on a double-coded sample.", "u", ["ws"], ["t2"], {"attr": "kno"}),
        ("L3", "Designs a mixed-methods study for a non-routine question, documenting how qualitative and quantitative results will be combined.", "u", ["pr"], ["t1", "t2"], {"attr": "cpx"}),
        ("L3", "Presents findings to managers and the public with the sample's limits stated, so that the results are not over-generalized.", "u", ["bars", "pr"], ["t3"], {"attr": "sco"}),
        ("L4", "Sets research standards for a programme's social science work, covering sampling, consent, confidentiality and reporting.", "u", ["pr"], ["eth", "t1"], {"attr": "gui"}),
        ("L4", "Reviews social science studies used in programme decisions, documenting where design or analysis limits the conclusions.", "u", ["pr"], ["t2"], {"attr": "sco"}),
    ]))

S.append(dict(
    id="seed:v1-6.3.2", seed=True, prefix="ind-v1-6.3.2", span=("L2", "L4"),
    title="Assess ecosystem services with production-function models validated against observations", alt=["Ecosystem services assessment"],
    definition="The capability to identify, quantify and map ecosystem services such as flood mitigation, water purification, carbon storage, pollination and recreation with production-function models, validate the models against observations, and communicate service benefits with their uncertainty. Named ecosystem-service model products are L4.",
    statement="Identifies, quantifies and maps ecosystem services such as flood mitigation, water purification, carbon storage, pollination and recreation with production-function models; validates model estimates against observations; states uncertainty and the beneficiaries assumed; and communicates service benefits in planning and outreach without overstating precision.",
    note=NOTE + " Tool names (InVEST, ARIES) moved to L4 (seed:tool-ecosystem-service-models); durable method is production-function modelling and validation (DC verdict).",
    tasks=[
        T("t1", ST("6.3.2", 1), "Quantify ecosystem services such as flood mitigation, carbon storage or pollination for a planning area, stating the beneficiaries and assumptions.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t2", ST("6.3.2", 2), "Model ecosystem service supply and flow with a production-function model, validating its estimates against field or monitoring observations.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t3", ST("6.3.2", 3), "Communicate ecosystem service benefits in planning or outreach materials, showing the uncertainty of each estimate.", "WF-PLAN", "remote", "no", rewrite=True, modes=["MODE-ENGAGE"]),
    ],
    inds=[
        ("L2", "Quantifies an assigned ecosystem service for a planning area with a stated model, documenting its inputs, beneficiaries and assumptions.", "u", ["ws"], ["t1"]),
        ("L2", "Reports ecosystem service estimates with ranges, so that readers can distinguish confident from uncertain estimates.", "u", ["ws"], ["t3"]),
        ("L3", "Validates a production-function model against field or monitoring observations, reporting where estimates fall outside observed ranges.", "u", ["ws", "pr"], ["t2"], {"attr": "cpx"}),
        ("L3", "Compares ecosystem service outcomes of management alternatives, documenting the sensitivity of the ranking to model assumptions.", "u", ["pr"], ["t1", "t2"], {"attr": "kno"}),
        ("L4", "Sets a programme's ecosystem-service assessment methods, specifying models, validation requirements and how uncertainty is reported.", "u", ["pr"], ["t2"], {"attr": "gui"}),
        ("L4", "Reviews ecosystem-service claims in plans or proposals, documenting where estimates lack validation or overstate precision.", "u", ["pr"], ["t3"], {"attr": "sco"}),
    ]))

S.append(dict(
    id="seed:v1-6.7.1", seed=True, prefix="ind-v1-6.7.1", span=("L2", "L4"),
    title="Assess human health risks from environmental exposures", alt=["Environmental health risk assessment"],
    definition="The capability to evaluate potential health effects of environmental exposures to chemicals, pollutants and other hazards through hazard identification, exposure assessment, dose-response and risk characterization, with stated uncertainty, and to communicate findings to affected communities and decision-makers. Jurisdiction-specific methods and screening levels are supplied by enactments.",
    statement="Evaluates potential health effects of environmental exposures to chemicals, pollutants and other hazards: identifies hazards and exposure pathways, estimates exposures, applies dose-response information, characterizes risk with stated uncertainty and sensitive populations, and communicates findings to affected communities and decision-makers.",
    note=NOTE + " Carried (wording rewritten); recurs in remediation, air, chemicals and environmental health (v1_disposition 6.7.1). Required methods vary by jurisdiction and programme (jurisdictionVariable indicators).",
    tasks=[
        T("t1", ST("6.7.1", 1), "Conduct an exposure assessment for an environmental contaminant, identifying pathways, receptors and exposure concentrations with documented assumptions.", "WF-ASSESS", "remote-capable", "partial", rewrite=True),
        T("t2", ST("6.7.1", 2), "Calculate health risks from environmental exposures with the methods the applicable requirements specify, stating the uncertainty of each estimate.", "WF-ASSESS", "remote", "partial", rewrite=True),
        T("t3", ST("6.7.1", 3), "Communicate health risk findings to affected communities and decision-makers, explaining what the estimates mean for exposure and action.", "WF-ASSESS", "remote-capable", "partial", rewrite=True,
          supports=["seed:v1-6.7.1", ("seed:DB-C29", "contributing")], modes=["MODE-ENGAGE"], rel=["public"]),
    ],
    inds=[
        ("L2", "Identifies exposure pathways and receptors for an assigned site, documenting the assumptions behind each exposure estimate.", "u", ["ws"], ["t1"]),
        ("L2", "Calculates risk estimates with the methods the applicable requirements specify, reporting the uncertainty of each estimate.", "u", ["ws"], ["t2"], {"jv": True}),
        ("L3", "Characterizes risk for a site with multiple contaminants and sensitive populations, documenting how uncertainty affects the conclusion.", "u", ["pr"], ["t1", "t2"], {"attr": "cpx"}),
        ("L3", "Explains risk findings to an affected community in plain terms, answering questions about exposure and recommended actions.", "u", ["sim", "bars"], ["t3"], {"attr": "sco"}),
        ("L4", "Sets a programme's risk-assessment procedures within the applicable requirements, specifying exposure assumptions and uncertainty reporting.", "u", ["pr"], ["t2"], {"attr": "gui", "jv": True}),
        ("L4", "Reviews risk assessments prepared by others for a contested decision, documenting where methods or assumptions do not support the conclusions.", "u", ["pr", "md"], ["t2"], {"attr": "sco"}),
    ]))

for spec in S:
    build(spec)
print("batch F written:", len(S), "competencies")
