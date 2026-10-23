"""Batch H: DC-primary core candidates from other roles' research (lane rule: craft_primary DC).
DB-C06 (absorbs LC-C-06), DB-C21, PS-C09 (absorbs DB-C36; split part of v1 6.6.1), PS-C07 (split part of v1 6.6.1)."""
from lib import df
from spec import T, build

S = []
ST = lambda c, n: f"seed:v1-{c}-T{n}"  # noqa: E731

S.append(dict(
    id="seed:DB-C06", prefix="db-c06", span=("L1", "L4"), evidence="J", sources=["DB-042"],
    title="Protect operational technology at environmental utilities and facilities", alt=["Operational-technology cybersecurity for environmental systems"],
    definition="The capability to keep the operational technology that runs environmental plants, monitoring networks and facilities secure and recoverable: knowing what is connected, controlling remote access and changes, recognizing and reporting anomalous control or sensor behaviour, and running incident response with manual fallback. Security products are L4.",
    statement="Keeps operational technology at environmental utilities, monitoring networks and facilities secure and recoverable: maintains an inventory of connected assets and their network zones; follows and enforces remote-access, patching and change procedures; recognizes and reports anomalous control or sensor behaviour; and runs incident-response drills with tested manual fallback.",
    note="Candidate DB-C06 (core-v2.0; WF-OPERATE), DC primary per the merged candidate list; SC secondary. Survivor: absorbs LC-C-06 (OT cybersecurity for monitoring and utility systems). Authored by WP-04 under the lane rule (craft_primary DC); DB to review.",
    tasks=[
        T("inv", "seed:dc-db06-asset-inventory", "Maintain an inventory of connected control and monitoring assets with their network zone, remote-access paths and owner.", "WF-OPERATE", "on-site-preferred", "partial",
          regime={"placeBoundness": "system-specific", "currencyDecay": "M"}),
        T("report", "seed:dc-db06-report-anomaly", "Report anomalous control or sensor behaviour that may indicate a cyber incident, following the facility's incident procedure while keeping operation safe.", "WF-OPERATE", "on-site-preferred", "partial",
          regime={"placeBoundness": "system-specific"}),
        T("access", "seed:dc-db06-remote-access", "Review remote access to control and monitoring systems under the change procedure, removing access that is no longer needed.", "WF-OPERATE", "remote-capable", "partial"),
        T("drill", "seed:dc-db06-fallback-drill", "Run an incident-response drill that switches a plant or monitoring network to manual operation, recording the time to a safe state and the gaps found.", "WF-RESPOND", "on-site-required", "yes",
          regime={"mentorshipDependence": "M", "cycleDependence": "multi-year-or-rare-event", "placeBoundness": "system-specific", "currencyDecay": "H"}),
        T("risk", "seed:dc-db06-risk-assessment", "Assess cyber risk to a facility's operational technology, ranking fixes by their consequence for treatment, monitoring or safety.", "WF-ASSESS", "remote-capable", "partial"),
    ],
    inds=[
        ("L1", "Reports anomalous control or sensor behaviour through the facility's incident procedure, recording the time, system and observed effect.", "u", ["sjt", "tbo"], ["report"]),
        ("L1", "Follows the remote-access and removable-media rules for control and monitoring systems, as confirmed in a system access audit.", "u", ["ra"], ["access"]),
        ("L2", "Maintains the inventory of connected assets with network zone, access paths and owner, correcting entries found wrong in a walkdown.", "u", ["ra"], ["inv"], {"attr": "aut"}),
        ("L2", "Switches a process or monitoring network to manual operation in a drill, reaching a safe state within the facility's target time.", "u", ["tbo"], ["drill"], {"attr": "cpx", "safety": True}),
        ("L3", "Assesses cyber risk to a facility's operational technology, ranking fixes by consequence for treatment, monitoring or safety.", "u", ["pr"], ["risk"], {"attr": "cpx"}),
        ("L3", "Runs incident-response drills with manual fallback for a team, documenting the gaps found and the corrective actions assigned.", "u", ["tbo", "pr"], ["drill"], {"attr": "for"}),
        ("L4", "Sets operational-technology security requirements for a utility or programme covering segmentation, access, change control and recovery testing.", "u", ["pr"], ["risk", "access"], {"attr": "gui"}),
        ("L4", "Reviews operational-technology incidents across facilities, revising requirements where incidents show recurring weaknesses.", "u", ["pr"], ["report"], {"attr": "sco"}),
    ]))

S.append(dict(
    id="seed:DB-C21", prefix="db-c21", span=("L2", "L4"), lifecycle="emerging", evidence="J", sources=["DB-021", "DB-025"],
    title="Investigate and manage emerging contaminants across media", alt=["PFAS and other emerging contaminants"],
    definition="The capability to plan and interpret investigations of contaminants whose health criteria, regulatory standards and analytical methods are still evolving: identifying sources and pathways across water, soil, air and waste, respecting analytical method limits, communicating risk while criteria change, and selecting interim response and treatment.",
    statement="Plans and interprets investigations of contaminants whose criteria, standards and analytical methods are still evolving: identifies sources and pathways across water, soil, air and waste; chooses sampling and analytical methods within their detection limits; communicates risk while criteria change; and selects interim response and treatment options with stated uncertainty.",
    note="Candidate DB-C21 (core-v2.0; WF-ASSESS; lifecycle emerging pending >= 30 postings or PDs across >= 3 actor types), DC primary per the merged candidate list; SC secondary. Authored by WP-04 under the lane rule; DB to review. Criteria and rules are L5 instruments.",
    tasks=[
        T("plan", "seed:dc-db21-investigation-plan", "Plan an investigation of an emerging contaminant, specifying media, sampling locations, analytical methods and their reporting limits.", "WF-PLAN", "remote-capable", "partial"),
        T("src", "seed:dc-db21-source-pathways", "Identify likely sources and transport pathways of an emerging contaminant across water, soil, air and waste from site history and sampling data.", "WF-ASSESS", "remote-capable", "partial"),
        T("interp", "seed:dc-db21-interpret-results", "Interpret emerging-contaminant results against current and proposed criteria, stating how the conclusions change if the criteria change.", "WF-ASSESS", "remote", "partial"),
        T("interim", "seed:dc-db21-interim-response", "Recommend interim response and treatment options for an emerging contaminant, comparing performance evidence, cost and handling of residuals.", "WF-PLAN", "remote", "partial"),
        T("comm", "seed:dc-db21-risk-communication", "Communicate emerging-contaminant findings to affected residents while criteria are changing, explaining what is known, unknown and being done.", "WF-ASSESS", "remote-capable", "partial",
          supports=["seed:DB-C21", ("seed:DB-C29", "contributing")], modes=["MODE-ENGAGE"], rel=["public"]),
    ],
    inds=[
        ("L2", "Plans sampling for an emerging contaminant with analytical methods whose reporting limits are below the criteria being compared.", "u", ["ws"], ["plan"]),
        ("L2", "Interprets results against current and proposed criteria, reporting how the conclusion changes under each.", "u", ["ws"], ["interp"]),
        ("L3", "Identifies sources and pathways at a site with several media and interacting releases, documenting the evidence and the uncertainty for each pathway.", "u", ["pr"], ["src"], {"attr": "cpx"}),
        ("L3", "Explains findings to affected residents while criteria are changing, stating what is known, unknown and being done.", "u", ["sim", "bars"], ["comm"], {"attr": "sco"}),
        ("L4", "Sets a programme's approach to emerging contaminants, specifying analytical, criteria-tracking and interim-response rules revised as standards change.", "u", ["pr"], ["plan", "interim"], {"attr": "gui"}),
        ("L4", "Recommends interim treatment across a programme's sites, documenting performance evidence, residuals handling and the basis for each choice.", "u", ["pr"], ["interim"], {"attr": "sco"}),
    ]))

S.append(dict(
    id="seed:PS-C09", prefix="ps-c09", span=("L1", "L4"), evidence="E", sources=["PS-001", "PS-006", "PS-007", "PS-008", "PS-013"],
    derived=[df("v1:6.6.1", "split-from", "organizational and jurisdictional GHG inventories (v1_disposition 6.6.1 position 1)")],
    title="Build organizational and jurisdictional greenhouse gas inventories for disclosure and reporting",
    alt=["Build corporate greenhouse gas inventories across Scopes 1-3 for multiple disclosure regimes", "Prepare greenhouse gas inventories for organizations and jurisdictions"],
    definition="The capability to build greenhouse gas inventories for organizations and jurisdictions: setting boundaries, collecting activity data, selecting emission factors and estimation methods, compiling value-chain emissions, quantifying uncertainty, documenting data quality and controls, and mapping one inventory to several disclosure and reporting requirements. Accounting standards are L4; disclosure rules are L5.",
    statement="Builds greenhouse gas inventories for organizations and jurisdictions: sets organizational and operational boundaries; collects activity data; selects emission factors and estimation methods; compiles value-chain emissions; quantifies uncertainty; documents data quality, controls and an audit trail; and maps one inventory to several disclosure and reporting requirements.",
    note="Candidate PS-C09 (core-v2.0; WF-MONITOR.attest), DC primary per the merged candidate list. Survivor: absorbs DB-C36 (jurisdictional variant) and the inventory part of v1 6.6.1 (split). Authored by WP-04 under the lane rule; PS and WP-05 to review. Module enactments exist in air, water and waste (WP-06).",
    tasks=[
        T("t1", ST("6.6.1", 1), "Compile a greenhouse gas inventory for an organization or jurisdiction, documenting boundaries, activity data, emission factors and methods for each source.", "WF-MONITOR.attest", "remote", "partial", rewrite=True,
          note="Split from v1 6.6.1: inventories -> PS-C09; project quantification (T2) -> PS-C06 in the markets module (left for WP-06/WP-05); verification plans (T3) -> PS-C07."),
        T("bound", "seed:dc-ps09-boundaries", "Set the organizational and operational boundaries of a greenhouse gas inventory, documenting the consolidation approach and any excluded sources.", "WF-MONITOR.attest", "remote", "partial"),
        T("vc", "seed:dc-ps09-value-chain", "Estimate value-chain emissions by category, choosing among supplier-specific, average-data and spend-based methods and stating each category's data quality.", "WF-MONITOR.attest", "remote", "partial"),
        T("unc", "seed:dc-ps09-uncertainty", "Quantify the uncertainty of a greenhouse gas inventory by source, identifying the sources that dominate total uncertainty.", "WF-MONITOR", "remote", "partial",
          supports=["seed:PS-C09", ("seed:DC-CAND-11", "contributing")]),
        T("map", "seed:dc-ps09-regime-mapping", "Map one greenhouse gas inventory to the boundary, category and assurance requirements of several disclosure regimes, documenting each reconciliation.", "WF-MONITOR.attest", "remote", "partial"),
        T("trail", "seed:dc-ps09-audit-trail", "Maintain the evidence trail and controls behind inventory figures so that an assurance provider can trace each figure to its source data.", "WF-MONITOR.attest", "remote", "partial",
          supports=["seed:PS-C09", ("seed:DC-CAND-05", "contributing")]),
    ],
    inds=[
        ("L1", "Collects activity data for assigned emission sources following the inventory's data procedures, recording the source document for each value.", "u", ["ra"], ["t1"]),
        ("L1", "Applies the assigned emission factors to activity data, with each calculation traceable and confirmed by a reviewer's check.", "u", ["ra"], ["t1"]),
        ("L2", "Compiles a complete inventory for an organization or jurisdiction, documenting boundaries, methods and factors for every source.", "u", ["ws", "ra"], ["t1", "bound"], {"attr": "aut"}),
        ("L2", "Estimates value-chain emissions by category with stated methods and data quality, flagging categories estimated from spend data.", "u", ["ws"], ["vc"], {"attr": "kno"}),
        ("L3", "Quantifies inventory uncertainty by source, identifying the dominant sources and the data improvements that would reduce total uncertainty.", "u", ["ws", "pr"], ["unc"], {"attr": "cpx"}),
        ("L3", "Maps one inventory to several disclosure regimes, documenting each reconciliation of boundary, category and method.", "u", ["pr"], ["map"], {"attr": "cpx"}),
        ("L4", "Sets inventory methods and controls for an organization or jurisdiction, documenting the basis for boundary, factor and estimation choices.", "u", ["pr"], ["bound", "trail"], {"attr": "gui"}),
        ("L4", "Prepares an inventory's evidence trail and controls so that an assurance provider can trace each reported figure to its source data.", "u", ["ra", "pr"], ["trail"], {"attr": "sco"}),
    ]))

S.append(dict(
    id="seed:PS-C07", prefix="ps-c07", span=("L2", "L4"), evidence="J", sources=["PS-003"],
    derived=[df("v1:6.6.1", "split-from", "independent verification (v1_disposition 6.6.1 position 3)")],
    title="Verify greenhouse gas assertions and environmental claims independently", alt=["Greenhouse gas validation and verification"],
    definition="The capability to plan and conduct independent validation and verification of greenhouse gas inventories, offset and removal projects and environmental claims against recognized standards: risk-based sampling, site visits, materiality thresholds, evidence evaluation and independence safeguards, ending in a reasoned opinion. Accredited-verifier status is a Credential.",
    statement="Plans and conducts independent validation and verification of greenhouse gas inventories, offset and removal projects and environmental claims against recognized standards: assesses risk, sets materiality, samples evidence and sites, visits facilities or project areas, evaluates misstatements, maintains independence, and issues a reasoned opinion with its basis.",
    note="Candidate PS-C07 (core-v2.0; WF-ENFORCE.assure; independent-verifier authority position), DC primary per the merged candidate list; SC secondary. Split part of v1 6.6.1 (verification). Accredited-verifier status is a Credential (T-8). Authored by WP-04 under the lane rule; PS and WP-05 to review.",
    tasks=[
        T("t3", ST("6.6.1", 3), "Develop a verification plan for a greenhouse gas assertion, setting materiality, risk-based sampling and site-visit scope before evidence is gathered.", "WF-ENFORCE.assure", "remote", "partial", rewrite=True,
          note="Split from v1 6.6.1 (monitoring and verification plans) -> PS-C07."),
        T("sample", "seed:dc-ps07-sample-evidence", "Sample the source data and calculations behind a greenhouse gas assertion, recalculating selected figures and recording each discrepancy found.", "WF-ENFORCE.assure", "remote-capable", "partial"),
        T("visit", "seed:dc-ps07-site-visit", "Conduct a verification site visit to a facility or project area, confirming that reported sources, equipment and land conditions exist as described.", "WF-ENFORCE.assure", "on-site-required", "yes"),
        T("mat", "seed:dc-ps07-misstatements", "Evaluate identified misstatements against the materiality threshold, deciding whether the assertion can receive a positive verification opinion.", "WF-ENFORCE.assure", "remote", "partial"),
        T("indep", "seed:dc-ps07-independence", "Check verifier independence before an engagement, declining or disclosing any relationship that would impair it.", "WF-ENFORCE.assure", "remote", "no",
          supports=["seed:PS-C07", ("seed:PS-C18", "contributing")]),
        T("opinion", "seed:dc-ps07-opinion", "Issue a verification opinion stating its basis, scope, materiality and unresolved issues so that users can judge the assurance given.", "WF-ENFORCE.assure", "remote", "partial"),
    ],
    inds=[
        ("L2", "Recalculates sampled figures in a greenhouse gas assertion from source data, recording each discrepancy and its size.", "u", ["ws"], ["sample"]),
        ("L2", "Confirms during a site visit that reported sources, equipment and land conditions exist as described, documenting any difference found.", "u", ["tbo"], ["visit"]),
        ("L3", "Develops a verification plan with materiality, risk-based sampling and site-visit scope matched to the assertion's risks.", "u", ["pr"], ["t3"], {"attr": "cpx"}),
        ("L3", "Evaluates misstatements against materiality, documenting the basis for the opinion and any qualifications.", "u", ["pr", "md"], ["mat", "opinion"], {"attr": "gui"}),
        ("L4", "Verifies contested assertions or those resting on modelled estimates, such as removal projects, documenting the reasoning behind each judgment for peer review.", "u", ["pr"], ["mat"], {"attr": "cpx"}),
        ("L4", "Sets a verification body's procedures for independence, materiality and sampling, reviewing engagements for compliance.", "u", ["pr"], ["indep", "t3"], {"attr": "sco"}),
    ]))

for spec in S:
    build(spec)
print("batch H written:", len(S), "competencies")
