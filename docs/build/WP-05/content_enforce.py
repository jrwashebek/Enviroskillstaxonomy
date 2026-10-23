"""WP-05 content: inspection and enforcement cluster (SL-C03, SL-C04, SL-C10, DB-C25, DB-C26)."""
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
SJT = ["situational-judgment-test"]

COMPETENCIES = [
    # ------------------------------------------------------------------ SL-C03
    {
        "id": "seed:SL-C03",
        "label": "Conduct regulatory compliance inspections",
        "alt": ["compliance inspection", "environmental inspector", "facility inspection", "site inspection"],
        "definition": "The capability of a regulatory authority's inspector to plan and conduct inspections of "
                      "facilities, sites or activities, gather evidence to an evidentiary standard, document findings of "
                      "fact against permit conditions and rules, and start the response the enforcement policy sets. "
                      "Excludes building the enforcement case, which is a separate competency.",
        "statement": "Plans and conducts announced or unannounced inspections of facilities, sites or activities against "
                     "permit conditions and applicable rules; observes, measures and samples to evidentiary standard; "
                     "documents findings of fact; and issues or recommends compliance assistance, notices of violation "
                     "or referral as the program's enforcement response policy directs.",
        "span": ("L1", "L4"),
        "derived": [("v1:6.1.2", "split-from")],
        "sources": ["SL-050", "SL-078", "SL-083", "SL-059", "SL-088"],
        "editorial": "WP-05 (A5 SC; SL reviewed). Survivor for regulatory inspection: absorbs FC-C04, DB-C24 (part), "
                     "FH-C11 (part) and the authority half of v1 6.1.2. Inspection is the modal state and local "
                     "environmental task (TX EPS and NRS, PA EPS, FL DEP) [E: SL-050, SL-078, SL-059]. Field craft and "
                     "statecraft are both defining (findings of fact that must hold in an enforcement proceeding; "
                     "codebook E4). Indicators adapted in part from IO exemplar rewrites for v1 6.1.2. Mirror: DB-C26 "
                     "(facility compliance management, regulated party).",
        "sensitivity": [
            ("DM-09", "Jurisdictional scope decides which sites and waters are inspected under federal authority.", "E", ["V2-07"]),
            ("DM-11", "Inspection authority follows delegated programme status.", "E", ["SC-021"]),
            ("DM-14", "Remote sensing, continuous monitoring and electronic reporting change inspection targeting and evidence.", "J", None),
            ("DM-16", "Inspector staffing levels change inspection capacity without changing the skill.", "J", None),
        ],
        "learning": "Assess through accompanied inspections recorded on a task book, report audits and moot testimony; "
                    "chain-of-custody sampling is a safety- and legal-critical indicator.",
        "tasks": [
            T("seed:sc-plan-inspection", "Plan a compliance inspection from the facility's permit, compliance history and "
              "monitoring reports, listing the conditions to verify and the evidence to collect",
              "WF-ENFORCE", formation="partial", profiles=["WP-COMPLIANCE"]),
            T("seed:v1-6.1.2-T1", "Inspect a permitted facility or site against its permit conditions and applicable rules, "
              "recording observations, measurements and samples as evidence",
              "WF-ENFORCE", field="on-site-required", formation="yes", profiles=["WP-COMPLIANCE"],
              derived=[("v1:6.1.2:T1", "rewritten")],
              regime={"mentorshipDependence": "H", "cycleDependence": "none", "placeBoundness": "general", "currencyDecay": "M"}),
            T("seed:sc-collect-inspection-evidence", "Collect samples and photographs during an inspection under "
              "chain-of-custody procedures, so that the evidence is admissible in an enforcement proceeding",
              "WF-ENFORCE", field="on-site-required", formation="yes", profiles=["WP-COMPLIANCE"]),
            T("seed:sc-write-inspection-report", "Write an inspection report stating findings of fact for each condition "
              "inspected, separating the inspector's observations from conclusions",
              "WF-ENFORCE", formation="yes", profiles=["WP-COMPLIANCE"]),
            T("seed:sc-select-enforcement-response", "Select the response the enforcement policy sets for each inspection "
              "finding, issuing a notice of violation, assistance letter or referral",
              "WF-ENFORCE", formation="partial", profiles=["WP-COMPLIANCE"]),
        ],
        "levels": {
            "L1": [
                I("Conducts a routine inspection with a checklist under a lead inspector's direction, recording "
                  "observations, photographs and document requests so that each checklist item has supporting evidence.",
                  TB + RA, tasks=["seed:v1-6.1.2-T1"], evidence=["checklist", "photo log"],
                  v1=["v1:6.1.2:foundational:I1"]),
                I("Collects a compliance sample following the program's chain-of-custody procedure, with no custody or "
                  "preservation defect found in record audit.", TB + RA, tasks=["seed:sc-collect-inspection-evidence"],
                  evidence=["custody forms"], critical=True),
            ],
            "L2": [
                I("Conducts a routine inspection independently and writes a report in which each finding cites the "
                  "requirement, the supporting evidence and the compliance determination.", WS + TB, attr="ATT-AUT",
                  tasks=["seed:sc-write-inspection-report"], evidence=["inspection report"]),
                I("Selects the enforcement response for each finding from the program's response policy, documenting the "
                  "facts that place it in that category.", WS + SJT, attr="ATT-GUI",
                  tasks=["seed:sc-select-enforcement-response"], evidence=["response memo"]),
            ],
            "L3": [
                I("Inspects a non-routine or multi-media facility where conditions conflict or records are incomplete, "
                  "documenting how each ambiguity was resolved on site.", TB + PORT, attr="ATT-CPX",
                  tasks=["seed:v1-6.1.2-T1"], evidence=["inspection report"]),
                I("Explains the evidence chain behind each inspection finding under cross-examination in a hearing or "
                  "moot exercise.", MOOT, attr="ATT-SCO", tasks=["seed:sc-write-inspection-report"],
                  evidence=["moot record"]),
                I("Evaluates trainee inspectors' inspections against the position standard, recording the evidence for "
                  "each task-book sign-off.", TB + RA, attr="ATT-FOR", tasks=["seed:v1-6.1.2-T1"],
                  evidence=["task-book sign-offs"]),
            ],
            "L4": [
                I("Sets a program's inspection protocols, checklists and evidence standards, revising them after case "
                  "outcomes reveal evidentiary gaps.", PORT, attr="ATT-GUI", tasks=["seed:sc-plan-inspection"],
                  evidence=["protocols", "revision log"]),
                I("Certifies inspectors for independent inspection authority after observing their inspections against "
                  "the program's position standard.", TB + PORT, attr="ATT-FOR", tasks=["seed:v1-6.1.2-T1"],
                  evidence=["certification record"]),
            ],
        },
        "enactments": [
            E("seed:ena-sl-c03-state", "State regulatory inspector", "state-agency", position="regulator",
              basis="State inspection and right-of-entry authority under state statutes; inspections for delegated "
                    "federal programmes follow the programme's compliance-monitoring strategy and reporting duties.",
              principal="The state program manager and enforcement section.",
              venue="State administrative hearings and courts; federal programme oversight of inspection commitments.",
              note="SL review: inspection defines the TX Environmental Protection Specialist series and is a core duty "
                   "in PA and FL classes; entry-level inspector classes start at L1 with accompanied inspections "
                   "[E: SL-050, SL-078, SL-059].", sl_reviewed=True, evidence="E",
              sources=["SL-050", "SL-078", "SL-059"]),
            E("seed:ena-sl-c03-local", "Local government inspector", "county", position="regulator",
              basis="County or municipal codes and state-delegated inspection programmes (stormwater, pretreatment, "
                    "local air or waste programmes).",
              principal="The local department head; the elected board.",
              venue="Local hearing officers; state courts.",
              note="SL review: local inspectors often enforce through citations and stop-work orders rather than "
                   "administrative penalty orders [J].", sl_reviewed=True),
            E("seed:ena-sl-c03-federal", "Federal regulatory inspector", "federal-regulator", position="regulator",
              basis="Federal statutory inspection and information-request authorities; federal inspector credentials.",
              principal="The regional enforcement division.",
              venue="Federal administrative law judges; federal courts.",
              note="Federal inspectors work alongside or oversee state inspectors in delegated programmes [J]."),
        ],
    },
    # ------------------------------------------------------------------ SL-C04
    {
        "id": "seed:SL-C04",
        "label": "Develop and resolve environmental enforcement cases",
        "alt": ["enforcement case management", "enforcement case manager", "consent order negotiation",
                "penalty calculation"],
        "definition": "The capability to carry an enforcement matter from referral or inspection finding to resolution: "
                      "investigate, assemble admissible evidence, determine violations, calculate penalties, negotiate "
                      "orders and settlements, and support litigation, including testimony. Excludes the inspection "
                      "itself.",
        "statement": "Builds an enforcement case from referral or inspection finding through evidence assembly, violation "
                     "determination, penalty calculation under the program's policy, negotiation of compliance schedules "
                     "and consent orders, and settlement or litigation support, including testimony as a fact or "
                     "expert witness.",
        "span": ("L2", "L4"),
        "derived": [("v1:6.1.5", "merged-from")],
        "sources": ["SL-072", "SL-075", "SL-078", "SL-069"],
        "editorial": "WP-05 (A5 SC; SL reviewed). Survivor for enforcement cases from referral to settlement or "
                     "litigation: absorbs DB-C24 (part), FH-C11 (part) and v1 6.1.5 (merged). State agencies run "
                     "dedicated enforcement case-management roles (MI EGLE; MPCA) [E: SL-072, SL-075]. Penalty and "
                     "enforcement-response policies are L5 instruments not yet registered (worklog).",
        "sensitivity": [
            ("DM-10", "Changes to substantive standards change what can be enforced.", "E", ["V2-05", "V2-06"]),
            ("DM-08", "Judicial review and remedy doctrine shape settlement leverage.", "J", None),
            ("DM-16", "Enforcement staffing and referral capacity change case volumes without changing the skill.", "J", None),
        ],
        "tasks": [
            T("seed:v1-6.1.5-T1", "Investigate a reported environmental violation, establishing the facts, responsible party "
              "and applicable requirement before recommending an enforcement response",
              "WF-ENFORCE", field="on-site-preferred", formation="yes", profiles=["WP-COMPLIANCE"],
              derived=[("v1:6.1.5:T1", "rewritten")]),
            T("seed:v1-6.1.5-T2", "Assemble the evidence file for an enforcement case, linking each alleged violation to the "
              "inspection findings, records and samples that prove it",
              "WF-ENFORCE", formation="yes", profiles=["WP-COMPLIANCE"], derived=[("v1:6.1.5:T2", "rewritten")]),
            T("seed:v1-6.1.5-T3", "Testify as a fact or expert witness in an enforcement proceeding, explaining the evidence "
              "and methods behind each finding",
              "WF-ENFORCE", modes=["MODE-RESOLVE"], formation="yes", derived=[("v1:6.1.5:T3", "rewritten")]),
            T("seed:sc-calculate-civil-penalty", "Calculate a proposed civil penalty under the program's penalty policy, "
              "documenting the gravity, economic benefit and adjustment factors applied",
              "WF-ENFORCE", formation="partial", profiles=["WP-COMPLIANCE"]),
            T("seed:sc-negotiate-consent-order", "Negotiate a consent order with a regulated party, setting a compliance "
              "schedule, penalty and stipulated reporting the agency can enforce",
              "WF-ENFORCE", modes=["MODE-RESOLVE"], formation="yes", profiles=["WP-COMPLIANCE"], also=["seed:SC-C16"]),
        ],
        "levels": {
            "L2": [
                I("Assembles an enforcement case file in which each alleged violation is linked to admissible evidence, "
                  "accepted by counsel without requests for more evidence.", RA + PORT,
                  tasks=["seed:v1-6.1.5-T2"], evidence=["case file"]),
                I("Calculates a proposed penalty under the program's penalty policy, documenting each gravity, benefit and "
                  "adjustment factor so that a second reviewer reproduces the figure.", WS,
                  tasks=["seed:sc-calculate-civil-penalty"], evidence=["penalty worksheet"]),
            ],
            "L3": [
                I("Negotiates a consent order on a contested case within the agency's enforceable minimums, recording the "
                  "basis for each concession made.", SIM + PORT, attr="ATT-SCO",
                  tasks=["seed:sc-negotiate-consent-order"], evidence=["negotiation record", "consent order"]),
                I("Testifies to case findings in a hearing or moot exercise, answering cross-examination on each evidence "
                  "link without contradicting the record.", MOOT, attr="ATT-SCO", tasks=["seed:v1-6.1.5-T3"],
                  evidence=["moot record"]),
                I("Investigates a violation whose responsible party or applicable requirement is disputed, documenting the "
                  "facts and the basis for the party and requirement identified.", WS + BARS, attr="ATT-CPX",
                  tasks=["seed:v1-6.1.5-T1"], evidence=["investigation memo"]),
            ],
            "L4": [
                I("Sets case-development and settlement standards for an enforcement program, including penalty checks "
                  "and criteria for referral to counsel.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-calculate-civil-penalty"], evidence=["program standards"]),
                I("Reviews other case managers' settlement proposals against program standards, returning each with the "
                  "deficiencies to correct before approval.", RA, attr="ATT-FOR",
                  tasks=["seed:sc-negotiate-consent-order"], evidence=["review comments"]),
            ],
        },
        "enactments": [
            E("seed:ena-sl-c04-state", "State enforcement case manager", "state-agency", position="regulator",
              basis="State administrative order and penalty authority; referral to the attorney general for civil or "
                    "criminal action; enforcement commitments for delegated federal programmes.",
              principal="The enforcement section chief; the attorney general for referred cases.",
              venue="State administrative hearings; state courts; federal oversight of delegated-programme enforcement.",
              note="SL review: EGLE enforcement analysts carry cases through final settlement; MPCA runs a compliance "
                   "and enforcement unit [E: SL-072, SL-075].", sl_reviewed=True, evidence="E",
              sources=["SL-072", "SL-075"]),
            E("seed:ena-sl-c04-federal", "Federal enforcement case development", "federal-regulator",
              position="regulator",
              basis="Federal administrative and civil judicial enforcement authorities; referral to the Department of "
                    "Justice; federal penalty policies.",
              principal="The regional enforcement director; federal prosecutors for referred cases.",
              venue="Federal administrative law judges; federal courts.",
              note="Same case arc; federal penalty and response policies are L5 instruments to register [J]."),
            E("seed:ena-sl-c04-regulated-party", "Regulated party responding to enforcement", "firm",
              position="regulated-party",
              basis="No authority; rights to notice, hearing and appeal; settlement options under the agency's policy.",
              principal="Facility management and legal counsel.", venue="Administrative hearings; courts.",
              note="Mirror: the regulated party negotiates the same consent order from the other side and manages "
                   "corrective action through its compliance system (DB-C26) [J]."),
        ],
    },
    # ------------------------------------------------------------------ SL-C10
    {
        "id": "seed:SL-C10",
        "label": "Provide compliance and technical assistance to regulated entities and local governments",
        "alt": ["compliance assistance", "small business environmental assistance", "technical assistance to "
                "local governments"],
        "definition": "The capability to help regulated entities and local governments understand and meet their "
                      "environmental obligations before enforcement is needed, through guidance, training, site "
                      "assistance and help lines, while keeping assistance separate from enforcement as program policy "
                      "requires.",
        "statement": "Designs and delivers plain-language guidance, training, site assistance and help lines that help "
                     "regulated entities and local governments understand and meet their obligations before enforcement "
                     "is needed, keeping assistance separate from enforcement decisions as the program's policy requires.",
        "span": ("L1", "L3"),
        "sources": ["SL-059", "SL-080"],
        "editorial": "WP-05 (A5 SC; SL reviewed). Compliance and technical assistance recurs in every regulatory module "
                     "(G-4); FL DEP and PA DEP classes name it as a core duty, and v1 had public education but none "
                     "aimed at regulated parties [E: SL-059, SL-080]. Mirror: DB-C26 (the regulated party's compliance "
                     "system).",
        "sensitivity": [
            ("DM-16", "Assistance programmes shrink or grow with staffing and funding.", "J", None),
            ("DM-19", "Grant and assistance programmes fund many state assistance offices.", "J", None),
        ],
        "tasks": [
            T("seed:sc-write-compliance-guidance", "Prepare plain-language compliance guidance for a regulated sector, "
              "explaining each obligation, deadline and common error with worked examples",
              "WF-ENFORCE.assist", formation="partial", profiles=["WP-COMPLIANCE"]),
            T("seed:sc-assistance-site-visit", "Visit a small regulated facility on request to identify compliance gaps, "
              "recommending corrective steps without initiating enforcement where policy allows",
              "WF-ENFORCE.assist", field="on-site-required", formation="yes", modes=["MODE-ENGAGE"], rel=["stakeholder"]),
            T("seed:sc-train-local-staff", "Deliver compliance training to local government staff responsible for a "
              "delegated or shared program, testing participants on the obligations covered",
              "WF-ENFORCE.assist", modes=["MODE-ENGAGE"], rel=["intergovernmental"], field="on-site-preferred"),
            T("seed:sc-answer-compliance-questions", "Answer compliance questions from regulated entities through a help "
              "line or portal, recording each question and the guidance given for consistency review",
              "WF-ENFORCE.assist", formation="no", modes=["MODE-ENGAGE"], rel=["stakeholder"]),
        ],
        "levels": {
            "L1": [
                I("Answers routine compliance questions from approved guidance, recording each question and answer so "
                  "that a reviewer can confirm consistency with program positions.", RA,
                  tasks=["seed:sc-answer-compliance-questions"], evidence=["contact log"]),
                I("Prepares a compliance checklist for one obligation from approved guidance that a regulated user "
                  "completes correctly without assistance in a usability test.", WS,
                  tasks=["seed:sc-write-compliance-guidance"], evidence=["checklist", "test notes"]),
            ],
            "L2": [
                I("Conducts a compliance-assistance visit at a small facility, delivering a written gap list with "
                  "corrective steps that the program's guidance supports.", TB + WS, attr="ATT-AUT",
                  tasks=["seed:sc-assistance-site-visit"], evidence=["gap list"]),
                I("Writes plain-language guidance for a regulated sector that program counsel accepts before release, "
                  "with each obligation stated as an action and deadline.", WS, attr="ATT-SCO",
                  tasks=["seed:sc-write-compliance-guidance"], evidence=["guidance document"]),
            ],
            "L3": [
                I("Designs a sector assistance program from compliance data, targeting the most frequent violations and "
                  "recording the measures used to evaluate its effect.", PORT, attr="ATT-SCO",
                  tasks=["seed:sc-write-compliance-guidance"], evidence=["program design"]),
                I("Refers a facility from assistance to enforcement when policy criteria are met, documenting the facts and "
                  "the criterion applied.", WS + SJT, attr="ATT-GUI", tasks=["seed:sc-assistance-site-visit"],
                  evidence=["referral memo"]),
            ],
        },
        "enactments": [
            E("seed:ena-sl-c10-state", "State compliance assistance program", "state-agency", position="regulator",
              basis="State assistance mandates, including small-business environmental assistance programmes, and "
                    "agency policies separating assistance from enforcement.",
              principal="The assistance program manager.", venue="Agency policy review; legislative oversight.",
              note="SL review: assistance staff sit in the regulator's agency but must not become a back door to "
                   "enforcement or an informal exemption; policy defines when they refer [J].", sl_reviewed=True),
            E("seed:ena-sl-c10-state-to-local", "State technical assistance to local governments", "state-agency",
              position="regulator",
              basis="State programmes that delegate or share delivery with local governments and fund their capacity.",
              principal="The state program manager.", venue="State funding conditions; legislative oversight.",
              note="SL review: assistance to local governments builds the capacity that delegated delivery depends on "
                   "(SC-C14) [J].", sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ DB-C25
    {
        "id": "seed:DB-C25",
        "label": "Target inspections and verify compliance using monitoring data and analytics",
        "alt": ["data-driven compliance targeting", "remote compliance verification", "next-generation compliance"],
        "definition": "The capability to use self-reported monitoring data, continuous-monitoring and remote-sensing "
                      "records and compliance history to decide where to inspect and to verify reported values, "
                      "stating the method's error rates and the human review applied before any enforcement step. "
                      "Excludes building or operating the sensing systems.",
        "statement": "Uses self-reported monitoring data, continuous-monitoring and remote-sensing records and compliance "
                     "history to rank facilities for inspection, detect probable non-compliance and verify reported "
                     "values against independent evidence, documenting the method, its error rates and the human review "
                     "applied before any enforcement step.",
        "span": ("L2", "L4"),
        "lifecycle": "emerging",
        "reviewBy": "2027-10-23",
        "sources": ["SL-050"],
        "editorial": "WP-05 (A5 SC). Data-driven targeting and remote compliance verification is a distinct "
                     "judgment-bearing product across modules; lifecycle emerging with a 12-month review [J]. The DC "
                     "enactment of AI-output validation (TX-A) supplies the validation method; this competency owns the "
                     "regulatory use and the human-review gate before enforcement.",
        "sensitivity": [
            ("DM-14", "Electronic reporting, remote sensing and analytics are entering compliance programmes.", "J", None),
            ("DM-16", "Analytics are adopted partly to offset inspection-staff capacity.", "J", None),
        ],
        "tasks": [
            T("seed:sc-rank-facilities-inspection", "Rank regulated facilities for inspection using compliance history and "
              "monitoring data, documenting the risk factors and weights in the targeting method",
              "WF-ENFORCE", formation="partial", profiles=["WP-COMPLIANCE"]),
            T("seed:sc-review-anomaly-flags", "Review automated anomaly flags in facility monitoring reports, confirming or "
              "dismissing each flag against the underlying data before referral",
              "WF-ENFORCE", formation="yes", profiles=["WP-COMPLIANCE"]),
            T("seed:sc-verify-reported-values", "Verify a facility's self-reported emissions or discharge values against "
              "independent remote-sensing or ambient data, stating the discrepancy and its uncertainty",
              "WF-ENFORCE", formation="yes", profiles=["WP-COMPLIANCE"]),
            T("seed:sc-evaluate-targeting-method", "Evaluate a targeting method after an inspection cycle, comparing "
              "predicted and found violations and recording the adjustments needed",
              "WF-ENFORCE", formation="partial"),
        ],
        "levels": {
            "L2": [
                I("Confirms or dismisses each automated anomaly flag in a facility's monitoring reports after checking "
                  "the underlying data, recording the reason for each decision.", SEW, mode="assisted",
                  tasks=["seed:sc-review-anomaly-flags"], evidence=["flag review log"]),
                I("Ranks facilities with the program's targeting method, documenting the inputs used for each facility "
                  "so that a reviewer reproduces the ranking.", WS + RA, tasks=["seed:sc-rank-facilities-inspection"],
                  evidence=["ranking file"]),
            ],
            "L3": [
                I("Compares a facility's reported values with independent monitoring or remote-sensing data, stating the "
                  "discrepancy, its uncertainty and whether it supports referral.", WS, attr="ATT-CPX",
                  tasks=["seed:sc-verify-reported-values"], evidence=["verification memo"]),
                I("Evaluates the targeting method after an inspection cycle, reporting predicted versus found violations "
                  "and the bias checks applied across facility groups.", WS + RA, attr="ATT-AUG",
                  tasks=["seed:sc-evaluate-targeting-method"], evidence=["evaluation report"]),
            ],
            "L4": [
                I("Designs a program's data-driven targeting and verification method, specifying error-rate limits and "
                  "the human review required before any enforcement step.", PORT, attr="ATT-AUG", mode="supervisory",
                  tasks=["seed:sc-rank-facilities-inspection"], evidence=["method specification"]),
                I("Audits targeting outcomes each year for drift or unequal treatment across facility groups, recording "
                  "the corrective changes made to the method.", RA + PORT, attr="ATT-GUI", mode="supervisory",
                  tasks=["seed:sc-evaluate-targeting-method"], evidence=["audit report"]),
            ],
        },
        "enactments": [
            E("seed:ena-db-c25-state", "State regulator using compliance analytics", "state-agency", position="regulator",
              basis="State inspection-targeting discretion and electronic-reporting rules; federal compliance-monitoring "
                    "commitments for delegated programmes.",
              principal="The compliance program manager.", venue="Administrative hearings where data support a case; "
                                                                  "legislative oversight of targeting fairness.",
              note="SL review: analytic targeting is adopted unevenly across states; where used, the human-review gate "
                   "before enforcement is the regulatory safeguard [J].", sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ DB-C26
    {
        "id": "seed:DB-C26",
        "label": "Manage a regulated facility's environmental compliance system and obligations calendar",
        "alt": ["environmental management system", "facility EHS compliance", "compliance calendar management",
                "EHS compliance manager"],
        "definition": "The capability of a regulated organization to identify every environmental obligation that applies "
                      "to it, assign owners and deadlines, check performance against permit conditions, prepare reports "
                      "for certification, manage agency inspections from the regulated side and correct non-compliance. "
                      "The regulated-party mirror of inspection and enforcement.",
        "statement": "Identifies every environmental obligation that applies to a facility or organization, assigns owners "
                     "and deadlines in a compliance calendar, runs the management system that checks performance against "
                     "permit conditions, prepares reports for certification, manages agency inspections and audits from "
                     "the regulated side, and corrects non-compliance with documented root-cause action.",
        "span": ("L1", "L4"),
        "derived": [("v1:6.1.2", "split-from")],
        "sources": ["SL-088"],
        "editorial": "WP-05 (A5 SC). Survivor: absorbs PS-C10 and receives the compliance-management half of v1 6.1.2, "
                     "which v1 wrote from the regulated side (SL, PS verdicts) [E: SL-088]. Mirror of SL-C03, SL-C04 and "
                     "SL-C10 for regulator-to-regulated mobility (R12 to R37).",
        "sensitivity": [
            ("DM-13", "Reporting and disclosure requirements set what a facility must certify.", "E", ["V2-15"]),
            ("DM-10", "Changes to substantive standards change facility obligations.", "E", ["V2-06"]),
            ("DM-14", "Electronic reporting changes how reports are prepared and checked.", "J", None),
        ],
        "tasks": [
            T("seed:v1-6.1.2-T2", "Develop a facility compliance checklist and procedures from its permits and applicable "
              "rules, assigning an owner and deadline to each obligation",
              "WF-MONITOR", formation="partial", profiles=["WP-COMPLIANCE"], derived=[("v1:6.1.2:T2", "rewritten")]),
            T("seed:v1-6.1.2-T3", "Coordinate a regulatory agency's inspection or audit of the facility, providing requested "
              "records and documenting each finding raised",
              "WF-MONITOR", field="on-site-required", modes=["MODE-ENGAGE"], rel=["stakeholder"],
              derived=[("v1:6.1.2:T3", "rewritten")]),
            T("seed:sc-prepare-compliance-report", "Prepare a periodic compliance report for the facility, checking reported "
              "values against source data before the responsible official certifies it",
              "WF-MONITOR.attest", formation="partial", profiles=["WP-COMPLIANCE"], signoff="legal-signatory",
              accountable="A designated responsible or certifying official signs the report and is legally accountable "
                          "for its accuracy."),
            T("seed:sc-investigate-exceedance", "Investigate a permit exceedance at the facility, identifying the root cause "
              "and documenting corrective actions and the notice given to the agency",
              "WF-MONITOR", field="on-site-preferred", formation="yes", profiles=["WP-COMPLIANCE"]),
            T("seed:sc-update-compliance-calendar", "Update the facility compliance calendar when a permit, rule or "
              "reporting requirement changes, notifying each obligation owner of the change",
              "WF-MONITOR", formation="no", profiles=["WP-COMPLIANCE"]),
        ],
        "levels": {
            "L1": [
                I("Maintains the facility compliance calendar so that every obligation sampled in audit has an owner, a "
                  "due date and a completion record.", RA, tasks=["seed:sc-update-compliance-calendar"],
                  evidence=["compliance calendar"]),
                I("Checks reported monitoring values against laboratory and instrument records before a report goes for "
                  "certification, logging each discrepancy.", SEW + RA, tasks=["seed:sc-prepare-compliance-report"],
                  evidence=["check log"]),
            ],
            "L2": [
                I("Prepares a compliance report that the responsible official certifies without corrections, with each "
                  "value traced to its source record.", RA + WS, attr="ATT-AUT",
                  tasks=["seed:sc-prepare-compliance-report"], evidence=["report", "source trace"]),
                I("Investigates a permit exceedance and documents its root cause, corrective actions and agency notice "
                  "within the deadline the permit sets.", WS + RA, attr="ATT-CPX",
                  tasks=["seed:sc-investigate-exceedance"], evidence=["investigation report"]),
            ],
            "L3": [
                I("Manages an agency inspection or audit from the facility side, answering each finding with evidence or "
                  "a correction plan within the time requested.", SIM + RA, attr="ATT-SCO",
                  tasks=["seed:v1-6.1.2-T3"], evidence=["finding responses"]),
                I("Revises the facility's compliance procedures when a permit or rule changes, documenting each obligation "
                  "added, removed or changed and its owner.", RA, attr="ATT-GUI", tasks=["seed:v1-6.1.2-T2"],
                  evidence=["procedure revision log"]),
            ],
            "L4": [
                I("Designs an organization's compliance management system across facilities, with audit criteria, "
                  "escalation rules and management review records.", PORT, attr="ATT-GUI",
                  tasks=["seed:v1-6.1.2-T2"], evidence=["system design"]),
                I("Evaluates site compliance leads against the system's audit criteria before approving them to prepare "
                  "reports for certification at their facilities.", RA + PORT, attr="ATT-FOR",
                  tasks=["seed:sc-prepare-compliance-report"], evidence=["evaluation record"]),
            ],
        },
        "enactments": [
            E("seed:ena-db-c26-private", "Private facility compliance management", "firm", position="regulated-party",
              basis="Permit conditions and rules binding the facility; certification duties of the responsible "
                    "official; voluntary management-system standards.",
              principal="Facility management, corporate EHS and the board.",
              venue="Agency inspections and enforcement; certification liability; customer and lender audits.",
              note="Mirror of SL-C03 (inspection), SL-C04 (enforcement) and SL-C10 (assistance) [J]."),
            E("seed:ena-db-c26-public-utility", "Public utility or local government as regulated party", "municipality",
              position="regulated-party",
              basis="Permits held by the municipality as operator (treatment works, landfills, power plants), "
                    "alongside its regulatory roles elsewhere.",
              principal="The utility director and governing board.",
              venue="State and federal enforcement; ratepayer and council oversight.",
              note="SL review: one city can regulate as a health department and be regulated as a treatment-works "
                   "operator; authority position belongs to the variant, not the employer [J; ADR-0017].",
              sl_reviewed=True),
            E("seed:ena-db-c26-federal-facility", "Federal facility as regulated party", "federal-agency",
              position="regulated-party",
              basis="Federal facilities' obligations to comply with environmental requirements administered by states "
                    "and federal regulators.",
              principal="The installation commander or facility manager.",
              venue="State and federal enforcement; federal facility compliance agreements.",
              note="Same compliance system performed inside a federal installation [J]."),
        ],
    },
]
