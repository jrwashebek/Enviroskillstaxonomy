"""P3 'what's coming' roles R31-R36 (proposed/emerging; reviewBy and named counter-signal) and P4 draft R37."""
from wp08lib import C, Role, T, X

J, S, LD, E = "journey", "senior", "lead", "entry"


def em(signals, feeders, horizon, scenarios, counter, review="2027-10-23"):
    return {"signals": [f"seed:{s}" for s in signals], "feeders": feeders, "horizon": horizon, "scenarios": scenarios,
            "counter": counter, "reviewBy": review}


def fd(role, deltas):
    return {"role": f"seed:{role}", "competencyDeltas": [
        {"competency": f"seed:{c}", **({"fromLevel": a} if a else {}), "toLevel": b} for c, a, b in deltas]}


ROLES = [
    Role(key="R31-ai-assisted-review-lead", tier="P3", area="core", wf="WF-REVIEW", levels=[S, LD], life="emerging",
         title="AI-assisted environmental review lead", auto=True, per=3, use_tier="exploratory",
         definition=("Emerging lead role that designs and runs environmental review workflows in which AI tools draft, "
                     "code or screen content, setting validation and human-review rules so the record and decision "
                     "remain defensible."),
         function="Keep AI-assisted environmental review accurate, traceable and defensible.",
         comps=[C("DC-CAND-16", 5, "L3 L4", dist=True), C("DC-CAND-13", 5, "L3 L4"), C("SL-C08", 5, "L3 L4"),
                C("SC-C02", 4, "L3 L4"), C("DC-CAND-14", 4, "L3 L4"), C("SC-C04", 4, "L3 L4"), C("DC-CAND-15", 3, "L3 L3"),
                C("PS-C18", 3, "L3 L3")],
         emerging=em(["sig/bls-ep-2025-35/19-2041/R31-ai-assisted-review-lead", "sig/capability/draftnepabench-coding-agents",
                      "sig/deployment/permitting-ai-shared-services", "sig/foresight/ws-26-carep-credential"],
                     [fd("R10-environmental-review-specialist", [("DC-CAND-16", "L3", "L4"), ("DC-CAND-14", None, "L3"),
                                                                 ("DC-CAND-13", "L3", "L4")])],
                     "1-3y", {"SC1": "up", "SC2": "flat", "SC3": "up", "SC4": "down"},
                     "AI review tools are retired or confined to pilots (as with an earlier federal comment-analysis tool), "
                     "so no lead role forms."),
         entry_from=["R10-environmental-review-specialist"]),
    Role(key="R32-environmental-ai-assurance-officer", tier="P3", area="core", wf="WF-ENFORCE", levels=[S, LD],
         life="proposed", title="Environmental AI assurance officer", auto=True, per=3, use_tier="exploratory",
         definition=("Proposed role that benchmarks AI tools before adoption, assesses and tiers model risk for "
                     "consequential environmental decisions, designs human oversight and gives independent challenge "
                     "to model owners."),
         function="Give decision-makers independent assurance that AI used in consequential environmental work is fit and governed.",
         comps=[C("DC-CAND-15", 5, "L3 L4", dist=True), C("DC-CAND-19", 5, "L3 L4"), C("DC-CAND-14", 4, "L3 L4"),
                C("DC-CAND-20", 4, "L3 L4"), C("DC-CAND-08", 4, "L3 L4"), C("v1-7.1.3", 4, "L3 L3"),
                C("DC-CAND-07", 3, "L3 L3"), C("PS-C18", 3, "L3 L3")],
         emerging=em(["sig/bls-ep-2025-35/13-1041/R32-environmental-ai-assurance-officer",
                      "sig/bls-ep-2025-35/15-2051/R32-environmental-ai-assurance-officer",
                      "sig/policy/omb-m-26-04-llm-contract-terms"],
                     [fd("R04-geospatial-remote-sensing-analyst", [("DC-CAND-09", "L4", "L4"), ("DC-CAND-19", None, "L3"),
                                                                   ("DC-CAND-15", None, "L3")])],
                     "3-5y", {"SC1": "up", "SC2": "up", "SC3": "external", "SC4": "down"},
                     "Assurance remains a collateral duty with no positions.", review="2027-10-23"),
         entry_from=["R04-geospatial-remote-sensing-analyst"]),
    Role(key="R33-permitting-technology-product-owner", tier="P3", area="core", wf="WF-MANAGE", levels=[S, LD],
         life="emerging", title="Permitting technology product owner", auto=True, per=3, use_tier="exploratory",
         definition=("Emerging role that owns permitting and review technology products: mapping the decisions they "
                     "serve, specifying and accepting AI and analytics services, setting human-review points and "
                     "keeping data publishable."),
         function="Deliver permitting technology that serves the actual authorization decisions and stays accountable.",
         comps=[C("DC-CAND-20", 5, "L3 L4", dist=True), C("DC-CAND-22", 5, "L3 L4"), C("SC-C01", 4, "L3 L3"),
                C("DC-CAND-14", 4, "L3 L4"), C("DC-CAND-06", 4, "L3 L4"), C("PS-C03", 4, "L3 L4"), C("SC-C12", 3, "L3 L3"),
                C("DC-CAND-16", 3, "L3 L3")],
         emerging=em(["sig/bls-ep-2025-35/11-3021/R33-permitting-technology-product-owner",
                      "sig/bls-ep-2025-35/15-1299/R33-permitting-technology-product-owner",
                      "sig/deployment/permitting-ai-shared-services"],
                     [fd("R11-environmental-permit-writer", [("DC-CAND-20", None, "L3"), ("DC-CAND-22", None, "L3")])],
                     "1-3y", {"SC1": "up", "SC2": "flat", "SC3": "up", "SC4": "down"},
                     "Products are bought as turnkey vendor services with no in-house product ownership."),
         entry_from=["R11-environmental-permit-writer", "R10-environmental-review-specialist"]),
    Role(key="R34-stewardship-agreement-manager", tier="P3", area="forest", wf="WF-RESOURCE", levels=[J, S, LD],
         life="emerging", title="Intergovernmental stewardship agreement manager", auto=True, per=3, use_tier="exploratory",
         definition=("Emerging role that designs and administers cross-jurisdictional stewardship and partner "
                     "implementation agreements, scopes partner work, tracks deliverables and revenue, and keeps "
                     "inherently governmental functions with the agency."),
         function="Get shared stewardship work done across jurisdictions under agreements that are lawful, funded and delivered.",
         comps=[C("SC-C08", 5, "L2 L3 L4", dist=True), C("v1-3.1.4", 5, "L2 L3 L4"), C("FH-C02", 4, "L2 L3 L3"),
                C("v1-5.2.5", 4, "L2 L3 L4"), C("SC-C07", 4, "L2 L3 L3"), C("SC-C10", 3, "L2 L3 L3"),
                C("PS-C03", 3, "L2 L3 L3"), C("v1-5.2.3", 3, "L2 L3 L3"), C("FC-C21", 3, "L2 L2 L3")],
         emerging=em(["sig/bls-ep-2025-35/13-1199/R34-stewardship-agreement-manager",
                      "sig/bls-ep-2025-35/19-1031/R34-stewardship-agreement-manager"],
                     [fd("R14-forester", [("SC-C08", "L2", "L3"), ("v1-3.1.4", None, "L3")]),
                      fd("R09-restoration-project-lead", [("SC-C08", None, "L3")])],
                     "1-3y", {"SC1": "up", "SC2": "up", "SC3": "external", "SC4": "reshape"},
                     "Agreement authorities stall or lapse and partner implementation reverts to ordinary contracting."),
         entry_from=["R14-forester", "R09-restoration-project-lead"],
         note="Agreement content specific to held relationships is excluded (ADR-0007 section D)."),
    Role(key="R35-knowledge-continuity-lead", tier="P3", area="core", wf="WF-LEARN", levels=[S, LD], life="proposed",
         title="Knowledge continuity lead", auto=True, per=3, use_tier="exploratory",
         definition=("Proposed role that identifies single-incumbent knowledge, elicits and transfers tacit and "
                     "institutional knowledge before departures, designs developmental experiences that keep formation "
                     "tasks, and curates authoritative guidance."),
         function="Keep an organization's critical know-how transferable when experienced staff leave.",
         comps=[C("FH-C07", 5, "L3 L4", dist=True), C("v1-7.2.2", 5, "L3 L4"), C("IO-C01", 4, "L3 L4"),
                C("DC-CAND-18", 4, "L3 L4"), C("FC-C20", 3, "L3 L3"), C("DC-CAND-07", 3, "L3 L3"), C("PS-C03", 3, "L3 L3"),
                C("FC-C22", 3, "L3 L3")],
         emerging=em(["sig/bls-ep-2025-35/11-3131/R35-knowledge-continuity-lead",
                      "sig/bls-ep-2025-35/13-1151/R35-knowledge-continuity-lead", "sig/headcount/epa-12849-jan-2026"],
                     [fd("R13-resource-program-manager", [("FH-C07", "L3", "L4"), ("DC-CAND-18", None, "L3")])],
                     "now", {"SC1": "flat", "SC2": "up", "SC3": "reshape", "SC4": "down"},
                     "No dedicated positions after attrition stabilizes.", review="2027-10-23"),
         entry_from=["R13-resource-program-manager"]),
    Role(key="R36-ghg-nature-data-controller", tier="P3", area="core", wf="WF-MONITOR", levels=[J, S, LD], life="emerging",
         title="GHG and nature data controller", auto=True, per=3, use_tier="exploratory",
         definition=("Emerging role that builds greenhouse gas and nature inventories, maps them to divergent disclosure "
                     "regimes, keeps the evidence trail and controls behind reported figures and prepares them for "
                     "independent assurance."),
         function="Make an organization's environmental disclosures accurate, traceable and ready for assurance.",
         comps=[C("PS-C09", 5, "L2 L3 L4", dist=True), C("SC-C15", 5, "L2 L3 L4"), C("PS-C07", 4, "L2 L3 L3"),
                C("DC-CAND-05", 4, "L2 L3 L4"), C("DC-CAND-08", 4, "L2 L3 L3"), C("v1-2.2.3", 4, "L2 L3 L3"),
                C("DC-CAND-11", 3, "L2 L3 L3"), C("v1-6.3.2", 2, "- L2 L3")],
         emerging=em(["sig/bls-ep-2025-35/13-2011/R36-ghg-nature-data-controller",
                      "sig/bls-ep-2025-35/19-2041/R36-ghg-nature-data-controller"],
                     [fd("R37-facility-environmental-compliance-specialist", [("PS-C09", "L3", "L4"), ("SC-C15", "L3", "L4")])],
                     "now", {"SC1": "up", "SC2": "flat", "SC3": "up", "SC4": "down"},
                     "Disclosure scope cuts (the EU omnibus amendments; a federal climate disclosure rule that never took "
                     "effect) reduce demand."),
         entry_from=["R37-facility-environmental-compliance-specialist/private"],
         note="Air quality specialists (R28, air module) are a further feeder; the link is recorded on R28's side."),
    # ------------------------------------------------------------------ P4
    Role(key="R37-facility-environmental-compliance-specialist", tier="P4", area="core", wf="WF-ENFORCE",
         levels=[E, J, S, LD], life="established", title="Facility environmental compliance specialist",
         alt=["environmental compliance specialist", "EHS specialist (environmental)", "permit compliance coordinator"],
         definition=("Regulated-party role that runs a facility's environmental compliance system: compliance calendars "
                     "and procedures from permits and rules, monitoring and reports for certification, exceedance "
                     "investigation, agency inspections and disclosure across regimes. Mirror of the inspector and "
                     "permit writer."),
         function="Keep a regulated facility in documented compliance with its permits, rules and reporting obligations.",
         comps=[C("DB-C26", 5, "L1 L2 L3 L4", dist=True), C("SC-C15", 4, "L1 L2 L3 L4"), C("PS-C18", 4, "L1 L2 L3 L3"),
                C("SC-C12", 4, "L1 L2 L3 L3"), C("v1-4.4.4-A", 4, "L1 L2 L2 L2"), C("FC-C24", 4, "L1 L2 L3 L3"),
                C("v1-4.4.1-B", 4, "L1 L2 L3 L4"), C("SC-C02", 3, "L1 L2 L2 L3"), C("PS-C09", 3, "- L2 L3 L3"),
                C("SC-C01", 3, "- L2 L3 L3"), C("SC-C07", 3, "- L2 L3 L3"), C("DC-CAND-05", 3, "L1 L2 L2 L3")],
         tasks=[
             T("v1-6.1.2-T2", 5, 3, "CE"), T("sc-update-compliance-calendar", 5, 2, "CE"),
             T("sc-prepare-compliance-report", 5, 3, "CE"), T("sc-investigate-exceedance", 5, 2, "C", "jsl"),
             T("v1-6.1.2-T3", 4, 1, "", "jsl"), T("sc-determine-disclosure-applicability", 4, 1, "", "sl"),
             T("v1-3.6.2-T1", 4, 1, "", "jsl"), T("v1-3.6.2-T2", 4, 1, "", "sl"), T("sc-replan-disclosure", 3, 0.5, "", "sl"),
             T("sc-screen-regulatory-alerts", 4, 1, "E"), T("sc-update-procedure-version", 4, 1), T("sc-write-change-notice", 3, 0.5, "", "sl"),
             T("fc-coc-complete", 5, 1, "CE"), T("fc-qc-collect", 4, 1, "E"), T("fc-haz-hasp", 5, 0.5, "CE"),
             T("v1-4.4.4-T1", 5, 0.5, "CE"), T("lc-txc-exercise-stop-work", 5, 0.3, "CE"), T("lc-txc-deliver-briefing", 4, 0.5, "", "jsl"),
             T("sc-apply-post-employment-rules", 4, 0.3, "C"), T("sc-disclose-assignment-interests", 4, 0.3, "E"),
             T("sc-index-record-documents", 3, 0.5), T("dc-ps09-boundaries", 3, 0.5, "", "sl"), T("v1-6.6.1-T1", 3, 0.5, "", "jsl"),
             T("v1-6.1.3-T3", 3, 0.5, "", "jsl"), T("sc-negotiate-permit-conditions", 3, 0.5, "", "sl"),
             T("dc-05-provenance-record", 3, 0.5, "E")],
         change=[
             X("sc-prepare-compliance-report", "transforming", ["AI", "policy-reform"],
               "Automated compilation of monitoring reports compresses production; certification review stays.",
               instruments=["report-certification-rules", "npdes-ereporting-rule"]),
             X("sc-determine-disclosure-applicability", "transforming", ["policy-reform", "market"],
               "Disclosure regimes diverge across jurisdictions and change through litigation.",
               instruments=["ca-sb-253", "eu-omnibus-i"]),
         ],
         entry_from=["R12-environmental-compliance-inspector/state", "R11-environmental-permit-writer/state"],
         note=("P4 draft. Mirror links (ADR-0017 section 4): R12 (inspector) and R11 (permit writer) are the regulator "
               "mirrors; the applicant-side preparer is the private applicant-preparer variant of this role. Recorded "
               "in X11 and generated/mirror_links.json.")),
]
