"""WP-05 content: rules and resources cluster (SC-C10, SC-C11, SC-C12, SC-C16, SC-C17, SC-C18, v1 6.4.5, v1 6.3.4
absorbing 6.4.3). Statecraft competencies do not depend on the withdrawn OPM ECQ names (political savvy, partnering,
influencing/negotiating; OPM five-ECQ framework, Oct 2025 [E: SC-058 corrected]); X9 maps to the current framework only."""
from wp05dsl import T, I, E

WS = ["work-sample"]
RA = ["record-audit"]
SEW = ["seeded-error-work-sample"]
BARS = ["structured-interview-bars"]
SIM = ["simulation-role-play"]
MOOT = ["moot-defense"]
PORT = ["portfolio-review"]
KT = ["knowledge-test"]
SJT = ["situational-judgment-test"]
PLOG = ["prediction-log-calibration"]

COMPETENCIES = [
    # ------------------------------------------------------------------ SC-C10
    {
        "id": "seed:SC-C10",
        "label": "Formulate, justify and execute public budgets across appropriations cycles",
        "alt": ["public budgeting", "appropriations", "budget formulation and execution", "fee and cost recovery design"],
        "definition": "The capability to obtain and use public funds on terms that hold: building and defending budget "
                      "requests, executing funds within legal limits, planning for funding gaps, and designing fees, "
                      "cost recovery and retained revenue within authority. Excludes project budgeting and internal "
                      "cost tracking, which are general project management.",
        "statement": "Builds and defends program budget requests and justifications, executes funds within purpose, time "
                     "and amount limits, plans for continuing resolutions and funding lapses, designs and administers "
                     "fees, cost recovery and retained revenue within law, and links spending to outcomes that "
                     "legislators, boards and auditors accept.",
        "span": ("L1", "L5"),
        "derived": [("v1:3.1.2", "split-from")],
        "sources": ["SC-042", "SC-030", "SC-013", "V2-04"],
        "editorial": "WP-05 (A5 SC). Split from v1 3.1.2 (project budgeting goes to PS-C03); public fiscal and "
                     "appropriations work is a distinct Statecraft deliverable [J; SC verdict]. 2025 created fiscal "
                     "instruments with workforce effects (sponsor-paid review fees; agreement revenue retention) [E: "
                     "V2-04, SC-030]. Indicators adapted from SC-A-C10-1..4. Span reaches L5; L5 indicators await SME "
                     "confirmation.",
        "sensitivity": [
            ("DM-15", "Fees, cost recovery and revenue retention are expanding.", "E", ["V2-04", "SC-030"]),
            ("DM-19", "Programme funding is cut, rescinded or reinstated by appropriations.", "J", None),
            ("DM-16", "Staffing levels follow appropriations.", "J", None),
        ],
        "tasks": [
            T("seed:sc-reconcile-appropriations", "Reconcile program obligations and expenditures against appropriations, "
              "agreements and fee accounts each month, flagging any use outside purpose or period",
              "WF-RESOURCE", formation="no"),
            T("seed:sc-prepare-budget-justification", "Prepare a program budget request and justification linking each "
              "funding increment to outputs and outcomes the budget office can verify",
              "WF-RESOURCE", formation="partial"),
            T("seed:sc-plan-funding-lapse", "Prepare a continuing-resolution and funding-lapse contingency plan, ranking "
              "program activities by legal requirement and consequence of delay",
              "WF-RESOURCE", formation="partial"),
            T("seed:sc-design-fee-schedule", "Design a fee or cost-recovery schedule for a permit or service program within "
              "its statutory authority, documenting the cost basis for each fee",
              "WF-RESOURCE", formation="partial"),
            T("seed:sc-brief-appropriators", "Brief appropriations staff or a governing board on a program budget request, "
              "answering questions with figures traceable to the justification",
              "WF-RESOURCE", modes=["MODE-ENGAGE"], rel=["intergovernmental"], field="on-site-preferred", formation="yes"),
        ],
        "levels": {
            "L1": [
                I("Reconciles program obligations against appropriations and fee accounts each month, with no purpose, "
                  "time or amount error found in an audit sample.", RA, tasks=["seed:sc-reconcile-appropriations"],
                  evidence=["reconciliation"]),
                I("Refers each proposed expenditure of doubtful purpose or period of availability to the budget officer, "
                  "naming the funding rule in question.", WS + KT, tasks=["seed:sc-reconcile-appropriations"],
                  evidence=["referral log"]),
            ],
            "L2": [
                I("Prepares a program budget justification linking each requested increment to outputs and outcomes, "
                  "accepted by the budget office without substantive rework.", WS, attr="ATT-AUT",
                  tasks=["seed:sc-prepare-budget-justification"], evidence=["budget justification"]),
                I("Writes a continuing-resolution contingency plan that ranks program activities by legal requirement and "
                  "consequence of delay.", WS, attr="ATT-KNO", tasks=["seed:sc-plan-funding-lapse"],
                  evidence=["contingency plan"]),
            ],
            "L3": [
                I("Designs a fee or cost-recovery schedule within statutory authority, with a cost basis for each fee that "
                  "passes budget-office and legal review.", WS + PORT, attr="ATT-GUI",
                  tasks=["seed:sc-design-fee-schedule"], evidence=["fee schedule", "cost basis"]),
                I("Briefs appropriations staff or a governing board on a budget request in an observed or simulated "
                  "session, answering each question with traceable figures.", SIM, attr="ATT-SCO",
                  tasks=["seed:sc-brief-appropriators"], evidence=["briefing observation record"]),
            ],
            "L4": [
                I("Sets budget formulation guidance and performance measures for a multi-program unit, revising them after "
                  "audit findings or appropriations changes.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-prepare-budget-justification"], evidence=["budget guidance"]),
                I("Negotiates a durable funding mechanism such as retained revenue or dedicated fees with the budget "
                  "office and legislative staff, recording the agreed terms.", PORT, attr="ATT-SCO",
                  tasks=["seed:sc-design-fee-schedule"], evidence=["agreed terms"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c10-federal", "Federal programme budgeting", "federal-agency",
              basis="Annual appropriations acts and their conditions; appropriations law on purpose, time and amount; "
                    "OMB budget formulation and apportionment; rescissions of prior appropriations.",
              principal="The agency budget office, OMB and congressional appropriations committees.",
              venue="GAO and inspector-general audits; appropriations hearings.",
              note="FY2026 Interior appropriations and the 2025 rescission of unobligated conservation and staffing "
                   "funds set the current federal base [E: instrument registry seeds].",
              instruments=["fy2026-interior-approps", "obbba-ira-rescissions", "nepa-s112-fee"]),
            E("seed:ena-sc-c10-state", "State agency budgeting", "state-agency",
              basis="State budget acts (annual or biennial), dedicated and special funds, fee statutes and federal "
                    "programme grants with matching requirements.",
              principal="The governor's budget office and legislative fiscal committees.",
              venue="State auditor; legislative hearings.",
              note="SL review: permit-fee and dedicated-fund programmes are common; fee setting often needs legislative "
                   "approval [J].", sl_reviewed=True),
            E("seed:ena-sc-c10-local", "Local government and utility budgeting", "special-district",
              basis="Local budget law, enterprise funds and rate-setting authority; bonds; state revolving fund loans.",
              principal="The elected board or council; for utilities, the rate-setting body.",
              venue="Public budget hearings; rate cases; local audits.",
              note="SL review: rates and enterprise funds replace appropriations, and the board that approves the "
                   "budget is in the room [J].", sl_reviewed=True),
            E("seed:ena-sc-c10-agreement-revenue", "Agreement-retained revenue for state and county partners",
              "county",
              basis="Stewardship agreement authorities letting state and county partners retain and reinvest receipts "
                    "(county and other non-state retention through FY2028).",
              principal="The county board; the federal agreement officer.",
              venue="Agreement audits; federal and state oversight.",
              note="SL review: retained receipts create a new fiscal task for county and state forestry staff (ledgers, "
                   "reinvestment plans) [E: SC-030].", instruments=["good-neighbor-authority"], sl_reviewed=True,
              evidence="E", sources=["SC-030"]),
        ],
    },
    # ------------------------------------------------------------------ SC-C11
    {
        "id": "seed:SC-C11",
        "label": "Assess the durability and reversal risk of policy choices and time actions to policy windows",
        "alt": ["policy durability assessment", "reversal-risk analysis", "policy windows"],
        "definition": "The capability to judge how likely an instrument is to survive changes of administration, "
                      "litigation and budget cycles, to choose instrument types and timing accordingly and to plan for "
                      "reversal. A learnable judgment evidenced in written analyses and forecast records, not a trait.",
        "statement": "Judges how likely a rule, guidance document, handbook, agreement, permit or program is to survive "
                     "changes of administration, litigation and budget cycles; chooses instrument types and timing "
                     "accordingly; identifies coming decision windows; and prepares contingency plans for programs that "
                     "rest on unstable instruments.",
        "span": ("L3", "L5"),
        "sources": ["SC-039", "SC-040", "SC-011", "SC-021", "V2-01", "V2-05", "V2-06", "V2-07"],
        "editorial": "WP-05 (A5 SC). Senior Statecraft requirement driven by 2025-26 instrument volatility [E: V2-01, "
                     "V2-05, V2-06, V2-07; SC-021]. Defined by observable products (risk memos, decision calendars, "
                     "calibrated forecast logs), not by the withdrawn ECQ label 'political savvy'. Nonpartisan posture "
                     "(ADR-0016 section 6): the competency assesses durability; it gives no help with political "
                     "designations. L5 indicators drafted per the disposition (L3-L5) and await SME confirmation.",
        "sensitivity": [
            ("DM-08", "Judicial review and remedy doctrine decide whether instruments survive challenge.", "E", ["V2-02"]),
            ("DM-10", "Substantive standards were rescinded and are litigated.", "E", ["V2-05", "V2-06"]),
            ("DM-11", "Delegated authority reverted after litigation.", "E", ["SC-021"]),
            ("DM-01", "Procedures moved from regulation to guidance that is easier to change.", "E", ["V2-01", "SC-040"]),
        ],
        "tasks": [
            T("seed:sc-classify-program-instruments", "Classify each instrument a program relies on by type and the "
              "process needed to change it, recording who can change it and how quickly",
              "WF-RULE", formation="partial"),
            T("seed:sc-assess-reversal-risk", "Assess the reversal risk of a program's key instruments, recording the "
              "evidence, the likely triggers and a contingency for each high-risk instrument",
              "WF-RULE", formation="yes"),
            T("seed:sc-advise-instrument-choice", "Advise leadership on the choice and timing of an instrument for a new "
              "policy, comparing the durability, speed and litigation exposure of each option",
              "WF-RULE", modes=["MODE-ENGAGE"], formation="yes"),
            T("seed:sc-keep-forecast-log", "Record dated forecasts of instrument changes affecting the program, reviewing "
              "their accuracy against outcomes each quarter",
              "WF-RULE", formation="partial",
              note="Prediction logs make judgment observable but are personnel data: adopter-held only (vocab "
                   "assessment_methods)."),
        ],
        "levels": {
            "L3": [
                I("Writes a reversal-risk memo for a program's key instruments, stating for each the change process, "
                  "likely triggers, evidence and a contingency.", WS + BARS, tasks=["seed:sc-assess-reversal-risk"],
                  evidence=["risk memo"]),
                I("Identifies a program's decision windows for the next two years, including rule deadlines, budget "
                  "cycles, elections and litigation milestones, in a dated calendar.", WS,
                  tasks=["seed:sc-classify-program-instruments"], evidence=["decision calendar"]),
            ],
            "L4": [
                I("Advises leadership on instrument choice and timing for a new policy with a written comparison of "
                  "durability, speed and litigation exposure for each option.", WS + BARS, attr="ATT-SCO",
                  tasks=["seed:sc-advise-instrument-choice"], evidence=["options memo"]),
                I("Reviews the calibration of the program's logged forecasts of instrument changes each quarter, "
                  "adjusting contingency plans where forecasts proved wrong.", PLOG + RA, attr="ATT-KNO",
                  tasks=["seed:sc-keep-forecast-log"], evidence=["forecast log", "calibration review"]),
            ],
            "L5": [
                I("Sets an organization's policy-instrument strategy across programs, stating which commitments rest on "
                  "statute, rule, agreement or guidance and the review cycle for each.", PORT, attr="ATT-SCO",
                  tasks=["seed:sc-advise-instrument-choice"], evidence=["instrument strategy"]),
                I("Designs governance arrangements for a cross-agency program that state how commitments continue through "
                  "leadership transitions and funding lapses, with review dates.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-assess-reversal-risk"], evidence=["governance design"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c11-federal", "Federal career staff advising on durability", "federal-agency",
              basis="Agency authority to choose between rulemaking, guidance and agreements; courts' review standards.",
              principal="Appointed agency leadership.", venue="Federal courts; Congress; future administrations.",
              note="2025-26 moved procedures from regulation to handbooks and rescinded substantive standards, each "
                   "litigated; the same analysis applies in either direction of policy change [E: V2-01, V2-05, V2-06].",
              instruments=["ceq-nepa-regs-removal", "doi-nepa-procedures", "esa-harm-rescission",
                           "ghg-endangerment-rescission", "wotus-definition"], evidence="E",
              sources=["V2-01", "V2-05", "V2-06", "V2-07"]),
            E("seed:ena-sc-c11-state", "State programme responding to federal change", "state-agency",
              basis="State statutes and rules that can fill or not fill federal gaps; delegated-programme status.",
              principal="The agency head and governor's office.", venue="State courts; state legislature.",
              note="SL review: states decide whether to adopt state-law versions of narrowed federal standards; that "
                   "choice is the durability judgment at state level [J].",
              instruments=["florida-404-assumption", "wotus-definition"], sl_reviewed=True),
            E("seed:ena-sc-c11-ngo", "Advocate choosing venues and instruments", "advocacy-organization",
              position="advocate",
              basis="No decision authority; comment, litigation, legislative and coalition channels.",
              principal="The board, members and funders.", venue="Courts; legislatures; agency dockets.",
              note="Advocates apply the same reversal-risk analysis to choose where to act and what to defend [J]."),
            E("seed:ena-sc-c11-private", "Regulated party planning under two legal futures", "firm",
              position="regulated-party",
              basis="Obligations under current rules plus exposure to their reversal or reinstatement.",
              principal="Executives and the board.", venue="Regulators; investors; courts.",
              note="Disclosure regimes enjoined, narrowed or starting in 2026 show why firms plan compliance under "
                   "more than one legal future [E: V2-15].",
              instruments=["ca-sb-253", "ca-sb-261", "sec-climate-disclosure", "eu-omnibus-i"], evidence="E",
              sources=["V2-15"]),
        ],
    },
    # ------------------------------------------------------------------ SC-C12
    {
        "id": "seed:SC-C12",
        "label": "Track regulatory change and translate it into operating guidance",
        "alt": ["regulatory change management", "regulatory tracking", "legal update notices"],
        "definition": "The capability to detect changes in rules, guidance, court decisions and legislation, judge which "
                      "programs, decisions and staff they affect, and turn them into dated operating guidance so that "
                      "work in progress follows the governing version. The human counterpart of the L5 instrument "
                      "registry. Excludes legislative advocacy.",
        "statement": "Monitors rules, guidance, court decisions and legislation, with automated tracking where available; "
                     "judges which changes affect which programs, decisions, procedures and staff; issues dated change "
                     "notices; and updates procedures, templates and training so that work in progress follows the "
                     "governing version.",
        "span": ("L1", "L4"),
        "sources": ["SC-038", "SC-011", "SC-009", "SC-004"],
        "editorial": "WP-05 (A5 SC). Monitoring is largely automatable (v1 coded legislative tracking V), but translating "
                     "change into operations is not: agencies produced staff decks to explain new procedures [E: SC-004, "
                     "SC-038]. The 2025-26 pace of change makes this a standing function [J].",
        "sensitivity": [
            ("DM-01", "Procedure changes at department level need dated operating guidance.", "E", ["V2-01"]),
            ("DM-14", "Automated regulatory tracking compresses monitoring tasks.", "J", None),
            ("DM-10", "Substantive standards changed and are litigated, so guidance must track status.", "E", ["V2-05", "V2-06"]),
        ],
        "tasks": [
            T("seed:sc-screen-regulatory-alerts", "Screen automated regulatory-change alerts for a program each week, "
              "confirming which items affect its decisions and recording why the rest do not",
              "WF-RULE", formation="partial"),
            T("seed:sc-write-change-notice", "Write a dated change notice explaining what a new rule, guidance or court "
              "decision changes for staff, its effective dates and the work in progress it affects",
              "WF-RULE", formation="partial"),
            T("seed:sc-update-procedure-version", "Update program procedures and templates to a new governing version, "
              "recording which pending actions follow the old and new versions",
              "WF-RULE", formation="no"),
            T("seed:sc-train-on-regulatory-change", "Train staff on a significant regulatory change, testing their "
              "application of the new requirement on sample cases",
              "WF-LEARN", formation="partial"),
        ],
        "levels": {
            "L1": [
                I("Screens automated regulatory-change alerts for an assigned program, checking each against the source "
                  "text and recording whether it affects program decisions.", SEW, mode="assisted",
                  tasks=["seed:sc-screen-regulatory-alerts"], evidence=["alert log"]),
                I("Maintains a procedure-version log for an assigned program so that every pending action sampled in "
                  "audit shows the version governing it.", RA, tasks=["seed:sc-update-procedure-version"],
                  evidence=["version log"]),
            ],
            "L2": [
                I("Writes a dated change notice stating what changes, from when, and for which pending actions, accepted "
                  "by counsel without correction of substance.", WS, attr="ATT-AUT",
                  tasks=["seed:sc-write-change-notice"], evidence=["change notice"]),
                I("Updates program templates to a new governing version, recording each change and the pending actions "
                  "that remain under the earlier version.", RA + WS, attr="ATT-KNO",
                  tasks=["seed:sc-update-procedure-version"], evidence=["template change log"]),
            ],
            "L3": [
                I("Interprets a change whose effect is unclear or contested, setting out options and risks for leadership "
                  "in a memo that counsel accepts.", WS + BARS, attr="ATT-CPX",
                  tasks=["seed:sc-write-change-notice"], evidence=["interpretation memo"]),
                I("Calibrates the program's automated tracking by reviewing missed and false alerts each quarter and "
                  "adjusting the sources and filters used.", RA, attr="ATT-AUG", mode="supervisory",
                  tasks=["seed:sc-screen-regulatory-alerts"], evidence=["calibration log"]),
            ],
            "L4": [
                I("Designs an organization's change-management process linking tracked changes to procedures, templates "
                  "and training, with review dates for each.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-update-procedure-version"], evidence=["process design"]),
                I("Evaluates staff change notices against the process standard, returning each with specific corrections "
                  "before release.", RA, attr="ATT-FOR", tasks=["seed:sc-write-change-notice"],
                  evidence=["review comments"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c12-federal", "Federal programme change management", "federal-agency",
              basis="Department procedures, handbooks and guidance that change by internal process; Federal Register "
                    "rules; court decisions.",
              principal="Program leadership and the general counsel's office.",
              venue="Inspectors general; courts (decisions made under superseded versions).",
              note="The 2025-26 sequence (interim and final removal of government-wide regulations, department "
                   "procedures, court decisions) is the reference case for this competency [E: V2-01].",
              instruments=["ceq-nepa-regs-removal", "ceq-nepa-guidance-2025", "doi-nepa-procedures",
                           "usda-nepa-procedures", "esa-harm-rescission", "ghg-endangerment-rescission"],
              evidence="E", sources=["V2-01", "V2-05", "V2-06"]),
            E("seed:ena-sc-c12-private", "Regulatory affairs change tracking", "firm", position="regulated-party",
              basis="Obligations across jurisdictions that change on different schedules.",
              principal="Compliance leadership.", venue="Regulators; auditors; assurance providers.",
              note="Corporate regulatory affairs tracks divergent regimes (state, federal, EU) and translates them into "
                   "operating procedures [E: V2-15].",
              instruments=["ca-sb-253", "ca-sb-261", "eu-omnibus-i"], evidence="E", sources=["V2-15"]),
        ],
    },
    # ------------------------------------------------------------------ SC-C16
    {
        "id": "seed:SC-C16",
        "label": "Draft enforceable, implementable binding instruments",
        "alt": ["policy drafting", "permit condition drafting", "regulatory drafting", "agreement drafting"],
        "definition": "The capability to write the binding text of permits, agreements, rules, orders, policies and "
                      "decision documents so that it is within authority, clear, measurable, enforceable and workable, "
                      "and to test drafts before issue. Covers non-binding guidance as a lesser case.",
        "statement": "Writes permit conditions, agreement terms, rules, orders, policy language and decision documents "
                     "that are within authority, clear, measurable, enforceable and workable for the people who must "
                     "carry them out, and tests drafts against implementation, compliance-verification and "
                     "legal-challenge scenarios before they are issued.",
        "span": ("L1", "L4"),
        "derived": [("v1:6.4.2", "merged-from")],
        "sources": ["SC-009", "SC-042"],
        "editorial": "WP-05 (A5 SC). Receives v1 6.4.2 (merged). AI produces first drafts quickly, so value moves to "
                     "specifying, testing and owning the binding text [E: SC-009]; drafting is among the most "
                     "assessable statecraft skills because work samples can be scored [J]. Core Statecraft practice "
                     "with actor enactments, not transversal (ADR-0025 section 4).",
        "sensitivity": [
            ("DM-14", "AI drafting tools change production of binding text.", "E", ["SC-009"]),
            ("DM-08", "Courts' review standards set how clearly authority and reasons must be stated.", "E", ["V2-02"]),
        ],
        "tasks": [
            T("seed:v1-6.4.2-T1", "Write policy or instrument language that states each obligation, obligated party, "
              "deadline and verification method so that compliance can be determined",
              "WF-RULE", formation="partial", derived=[("v1:6.4.2:T1", "rewritten")]),
            T("seed:v1-6.4.2-T2", "Review a proposed policy or instrument for consistency with governing law, existing "
              "instruments and agency authority, listing each conflict found",
              "WF-RULE", formation="yes", derived=[("v1:6.4.2:T2", "rewritten")]),
            T("seed:v1-6.4.2-T3", "Test a draft instrument with the staff and parties who must implement it, revising "
              "terms they cannot carry out or verify",
              "WF-RULE", modes=["MODE-ENGAGE"], rel=["stakeholder"], formation="partial",
              derived=[("v1:6.4.2:T3", "rewritten")]),
            T("seed:sc-verify-ai-draft-instrument", "Verify each term of an AI-generated first draft of an instrument "
              "against the governing authority and record before the draft enters review",
              "WF-RULE", formation="yes",
              note="Review counterpart of drafting where AI compresses first-draft production (G-2)."),
            T("seed:sc-test-terms-scenarios", "Test draft permit conditions or agreement terms against compliance-"
              "verification and legal-challenge scenarios, recording each term revised and why",
              "WF-RULE", formation="yes"),
        ],
        "levels": {
            "L1": [
                I("Drafts conditions for a routine instrument from a template, naming in each condition the obligated "
                  "party, action, deadline and verification method.", WS, tasks=["seed:v1-6.4.2-T1"],
                  evidence=["draft conditions"]),
                I("Checks a draft instrument against a drafting checklist, flagging each undefined term, missing deadline "
                  "or unverifiable obligation for the drafter.", SEW, tasks=["seed:v1-6.4.2-T2"],
                  evidence=["checklist"]),
            ],
            "L2": [
                I("Drafts a routine set of permit conditions or agreement terms that passes the program's enforceability "
                  "review without substantive rework.", WS + RA, attr="ATT-AUT", tasks=["seed:v1-6.4.2-T1"],
                  evidence=["draft instrument", "review record"]),
                I("Verifies each term of an AI-generated draft against the governing authority and record, correcting or "
                  "striking terms that exceed authority or lack a basis.", SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:sc-verify-ai-draft-instrument"], evidence=["verification log"]),
            ],
            "L3": [
                I("Tests a non-routine draft against implementation, verification and challenge scenarios with "
                  "implementers and counsel, recording each term revised and why.", WS + PORT, attr="ATT-CPX",
                  tasks=["seed:sc-test-terms-scenarios"], evidence=["scenario test record"]),
                I("Drafts settlement or agreement terms during a negotiation that stay within authority and that both "
                  "parties' reviewers accept as clear.", SIM + WS, attr="ATT-SCO", tasks=["seed:v1-6.4.2-T3"],
                  evidence=["negotiated terms"]),
            ],
            "L4": [
                I("Writes an organization's drafting standards and model terms for a class of instruments, revising them "
                  "after enforcement or litigation outcomes.", PORT, attr="ATT-GUI", tasks=["seed:v1-6.4.2-T1"],
                  evidence=["drafting standard", "model terms"]),
                I("Reviews other drafters' instruments against the drafting standard, returning each with specific "
                  "revisions and the rule that requires them.", RA, attr="ATT-FOR", tasks=["seed:v1-6.4.2-T2"],
                  evidence=["review comments"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c16-regulator", "Agency drafting of binding instruments", "state-agency", position="regulator",
              basis="The agency's statutory authority; administrative procedure acts for rules; permit and order "
                    "authorities.",
              principal="The signing official.", venue="Administrative appeals; courts.",
              note="SL review: state drafters work to state administrative procedure acts and legislative rule review "
                   "that differ from the federal process [J].", sl_reviewed=True),
            E("seed:ena-sc-c16-local", "Local ordinance and condition-of-approval drafting", "municipality",
              basis="Police power and state enabling law for ordinances, zoning codes and conditions of approval.",
              principal="The council or planning commission.", venue="Local appeals; state courts.",
              note="SL review: legislative text (ordinances) and quasi-judicial conditions (permits, variances) are "
                   "drafted under different procedural rules in the same office [J].", sl_reviewed=True),
            E("seed:ena-sc-c16-advocate", "Model legislation and comment drafting by advocates", "advocacy-organization",
              position="advocate",
              basis="No authority; proposed text offered to legislators, agencies or parties.",
              principal="The organization's board and members.", venue="Legislatures; agency dockets.",
              note="Advocates draft text others will adopt; enforceability tests are the same [J]."),
        ],
    },
    # ------------------------------------------------------------------ SC-C17
    {
        "id": "seed:SC-C17",
        "label": "Assess litigation exposure and design decisions for resilience on remand",
        "alt": ["litigation risk assessment", "record defensibility", "remand planning"],
        "definition": "The capability to anticipate the legal challenges a decision will face under current doctrine, to "
                      "decide where added analysis, engagement or explanation reduces that risk, and to structure the "
                      "decision and record so that a remand can be completed without restarting. Excludes legal "
                      "representation, which counsel provides.",
        "statement": "Identifies the claims a decision is likely to face under current standards of deference, remedy and "
                     "standing; decides where more analysis, engagement or explanation reduces that risk; and "
                     "structures the record and decision so that a court remand can be completed without restarting the "
                     "action.",
        "span": ("L3", "L5"),
        "sources": ["SC-012", "SC-010", "SC-009", "V2-02", "V2-03"],
        "editorial": "WP-05 (A5 SC). Deference and remedy doctrine changed in 2025 (a deficient analysis does not "
                     "necessarily require vacatur), and pending legislation would mandate remand without vacatur and "
                     "limit standing [E: V2-02, V2-03]. Works with counsel; never replaces legal advice. L5 indicators "
                     "drafted per the disposition (L3-L5) and await SME confirmation.",
        "sensitivity": [
            ("DM-08", "Deference, standing, limitations periods and remedies are changing.", "E", ["V2-02", "V2-03"]),
            ("DM-01", "Narrower review scope changes which claims are viable.", "E", ["V2-02"]),
        ],
        "tasks": [
            T("seed:sc-identify-likely-claims", "Identify the claims a proposed decision is likely to face, rating each "
              "claim's likelihood under current deference, standing and remedy doctrine",
              "WF-REVIEW", modes=["MODE-RESOLVE"], formation="yes"),
            T("seed:sc-recommend-risk-reduction", "Recommend targeted additional analysis or engagement for a decision, "
              "stating the litigation risk each recommendation reduces and its schedule cost",
              "WF-REVIEW", modes=["MODE-RESOLVE"], formation="yes"),
            T("seed:sc-structure-severable-decision", "Structure a decision document and its record so that each severable "
              "element could be corrected on remand without vacating the whole decision",
              "WF-REVIEW", modes=["MODE-RESOLVE"], formation="yes"),
            T("seed:sc-pre-issuance-record-review", "Review a decision record with counsel before issuance, listing the "
              "record gaps that weaken the reasoned explanation and the fix for each",
              "WF-REVIEW", modes=["MODE-RESOLVE"], formation="yes", also=["seed:SC-C02"]),
        ],
        "levels": {
            "L3": [
                I("Rates the likelihood of each expected claim against a decision under current deference, standing and "
                  "remedy doctrine, citing the case law relied on.", WS + BARS,
                  tasks=["seed:sc-identify-likely-claims"], evidence=["claims memo"]),
                I("Recommends targeted additional analysis or engagement for a decision, stating the claim each "
                  "recommendation addresses and its schedule cost.", WS, tasks=["seed:sc-recommend-risk-reduction"],
                  evidence=["recommendation memo"]),
                I("Lists the record gaps that weaken a decision's reasoned explanation before issuance, with the fix for "
                  "each, in a review that counsel accepts.", RA + WS, tasks=["seed:sc-pre-issuance-record-review"],
                  evidence=["record gap list"]),
            ],
            "L4": [
                I("Structures a decision and its record into severable elements so that a remand on one element can be "
                  "completed without restarting the others.", WS + PORT, attr="ATT-CPX",
                  tasks=["seed:sc-structure-severable-decision"], evidence=["decision structure"]),
                I("Defends a decision's reasoning before mock counsel or a review panel, answering each challenge with "
                  "record citations.", MOOT, attr="ATT-SCO", tasks=["seed:sc-identify-likely-claims"],
                  evidence=["moot record"]),
            ],
            "L5": [
                I("Sets an organization's litigation-risk review process for high-consequence decisions, stating when counsel "
                  "review, added analysis or a moot defense is required.", PORT, attr="ATT-SCO",
                  tasks=["seed:sc-recommend-risk-reduction"], evidence=["review process"]),
                I("Reviews litigation outcomes across the organization's decisions each year, revising risk criteria "
                  "where predicted and actual outcomes diverged.", PLOG + PORT, attr="ATT-KNO",
                  tasks=["seed:sc-identify-likely-claims"], evidence=["outcome review"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c17-federal", "Federal decision defensibility", "federal-agency",
              basis="Judicial review of agency action; the 2025 Supreme Court standard of substantial deference in "
                    "environmental review; pending legislation on limitations periods, standing and remedies; agency "
                    "objection processes.",
              principal="The deciding official, with agency counsel and the Department of Justice.",
              venue="Federal courts.",
              note="PermitTEC-style case datasets can calibrate litigation-risk judgment for training [E: SC-009].",
              instruments=["seven-county", "speed-act", "usfs-objection-rule"], evidence="E",
              sources=["V2-02", "V2-03", "SC-009"]),
            E("seed:ena-sc-c17-state", "State decision defensibility", "state-agency",
              basis="State judicial review standards and state environmental policy act litigation.",
              principal="The state lead agency and attorney general.", venue="State courts.",
              note="SL review: state review statutes have their own limitation periods and remedy rules [J].",
              instruments=["ceqa-2025-reforms"], sl_reviewed=True),
            E("seed:ena-sc-c17-advocate", "Advocate litigation assessment", "advocacy-organization", position="advocate",
              basis="Standing and comment-exhaustion requirements; citizen-suit provisions.",
              principal="The board and members.", venue="Courts.",
              note="The mirror analysis: which claims are viable and worth bringing, and what comments preserve them "
                   "[E: V2-03 for pending standing rules].", instruments=["speed-act"], evidence="E", sources=["V2-03"]),
        ],
    },
    # ------------------------------------------------------------------ SC-C18
    {
        "id": "seed:SC-C18",
        "label": "Brief decision-makers and elected officials for authoritative decisions",
        "alt": ["decision briefing", "staff reports to governing bodies", "decision memos"],
        "definition": "The capability to prepare and give briefings, decision memos and staff reports that let an "
                      "accountable official or governing body make an authoritative decision, setting out the decision "
                      "required, options, evidence, risks and a recommendation, with frank advice within a nonpartisan "
                      "professional role.",
        "statement": "Prepares and delivers concise, candid briefings, decision memos and staff reports for decision-makers "
                     "and governing bodies, setting out the decision required, the options, evidence, risks and a "
                     "recommendation, and gives frank advice under time and political pressure while keeping within a "
                     "nonpartisan professional role.",
        "span": ("L2", "L5"),
        "sources": ["SC-042"],
        "editorial": "WP-05 (A5 SC). The UK Policy Profession Standards level this skill from understanding principals' "
                     "pressures to being trusted to give free and frank advice [E: SC-042]; v1 spread it across generic "
                     "communication items. Defined by the work product, not by withdrawn ECQ labels. Nonpartisan posture "
                     "(ADR-0016 section 6). L5 indicators await SME confirmation.",
        "sensitivity": [
            ("DM-16", "Changes in political appointment and career-staff rules change who is briefed and how.", "E", ["V1-12"]),
        ],
        "tasks": [
            T("seed:sc-write-decision-memo", "Write a decision memo for an accountable official, stating the decision "
              "required, options, evidence, risks and a recommendation within two pages",
              "WF-MANAGE", modes=["MODE-ENGAGE"], formation="partial"),
            T("seed:sc-prepare-staff-report", "Prepare a staff report for a governing body's public meeting, stating "
              "findings, options and the legal basis for each recommended action",
              "WF-AUTHORIZE", modes=["MODE-ENGAGE"], rel=["public"], formation="partial"),
            T("seed:sc-brief-decision-maker", "Brief a decision-maker orally on a pending decision under time pressure, "
              "answering questions and stating where the evidence is uncertain",
              "WF-MANAGE", modes=["MODE-ENGAGE"], field="on-site-preferred", formation="yes"),
            T("seed:sc-record-frank-advice", "Advise an official in writing when the evidence does not support a preferred "
              "option, recording the advice given in the decision file",
              "WF-MANAGE", modes=["MODE-ENGAGE"], formation="yes", also=["seed:v1-7.1.3"]),
        ],
        "levels": {
            "L2": [
                I("Writes a decision memo that states the decision required, options, evidence, risks and a "
                  "recommendation, accepted by the supervisor without restructuring.", WS,
                  tasks=["seed:sc-write-decision-memo"], evidence=["decision memo"]),
                I("Prepares a staff report for a governing body that states findings, options and legal basis, with no "
                  "item continued for missing information.", WS + RA, tasks=["seed:sc-prepare-staff-report"],
                  evidence=["staff report", "meeting minutes"]),
            ],
            "L3": [
                I("Briefs a decision-maker orally in an observed or simulated session, stating options and uncertainty "
                  "and answering each question within the briefing time.", SIM, attr="ATT-SCO",
                  tasks=["seed:sc-brief-decision-maker"], evidence=["observation record"]),
                I("States in writing when the evidence does not support a decision-maker's preferred option, giving the "
                  "reasons and the options that the evidence does support.", WS + SJT, attr="ATT-GUI",
                  tasks=["seed:sc-record-frank-advice"], evidence=["advice memo"]),
            ],
            "L4": [
                I("Sets briefing and decision-memo standards for an organization's decision process, with templates and "
                  "review steps used for every high-consequence decision.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-write-decision-memo"], evidence=["standards", "templates"]),
                I("Coaches staff on briefing elected or appointed officials, reviewing their memos and rehearsals against "
                  "the organization's standard before delivery.", PORT, attr="ATT-FOR", obs4=2,
                  tasks=["seed:sc-brief-decision-maker"], evidence=["coaching record"]),
                I("Reviews staff decision memos against the organization's standard, returning each with the gaps in "
                  "options, evidence or risk to fix.", RA, attr="ATT-FOR", tasks=["seed:sc-write-decision-memo"],
                  evidence=["review comments"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c18-federal", "Career staff briefing appointed officials", "federal-agency",
              basis="Delegations of decision authority within the department; merit-system and career-service rules.",
              principal="Appointed officials; for some decisions, the secretary.", venue="Congress; inspectors general.",
              note="Federal principals are distant and insulated by civil-service rules; changes to appointment "
                   "categories are tracked as L5 instruments, and EMST gives no help with political designations "
                   "(ADR-0016 section 6).", instruments=["schedule-policy-career"]),
            E("seed:ena-sc-c18-local", "Staff reports to elected boards and commissions", "county",
              basis="Open-meeting laws and the board's or commission's decision authority; quasi-judicial hearing rules.",
              principal="The elected board, council or appointed commission.",
              venue="Public meetings; local appeals; state courts.",
              note="SL review: local principals sit on the dais, so briefing happens in public and on the record [J].",
              sl_reviewed=True),
            E("seed:ena-sc-c18-state", "Briefing state leadership and commissions", "state-commission",
              basis="Commission or board authority over rules, permits or rates; governor's office decision routines.",
              principal="The commission, board or governor's office.", venue="Public hearings; state courts.",
              note="SL review: state commissions (environmental quality boards, utility commissions) decide in public "
                   "with staff recommendations [J].", sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ v1 6.4.5
    {
        "id": "seed:v1-6.4.5",
        "label": "Navigate legislative and governing-body processes for environmental programs",
        "alt": ["legislative process navigation", "legislative liaison", "testimony preparation", "fiscal notes"],
        "definition": "The capability to follow and take part in the legislative, appropriations and governing-body "
                      "processes that shape a program, providing technical assistance, testimony, briefings and fiscal "
                      "or implementation notes within the organization's rules on lobbying and official communication.",
        "statement": "Tracks bills, ordinances and appropriations measures that affect a program; prepares technical "
                     "assistance, testimony, briefings and fiscal or implementation notes for legislators, councils, "
                     "boards and commissions; and works with their staff within the organization's rules on lobbying "
                     "and official communications.",
        "span": ("L2", "L5"),
        "derived": [],
        "sources": ["SC-004"],
        "editorial": "WP-05 (A5 SC). v1 6.4.5 rewrite, broadened to legislative, appropriations and governing-body "
                     "processes (Congress, legislatures, county boards, utility commissions) [J; SC verdict]. Bill "
                     "tracking was coded V in v1 [E: SC-004]; the review and fiscal-note tasks remain human. The Tribal "
                     "council enactment is held content (not authored). L5 indicators await SME confirmation.",
        "sensitivity": [
            ("DM-19", "Programme funding is set or changed through appropriations measures.", "J", None),
            ("DM-14", "Automated bill tracking compresses monitoring tasks.", "E", ["SC-004"]),
        ],
        "tasks": [
            T("seed:v1-6.4.5-T1", "Track bills, ordinances and appropriations measures affecting the program, summarizing "
              "each relevant provision's effect on program operations",
              "WF-RULE", formation="no", derived=[("v1:6.4.5:T1", "rewritten")]),
            T("seed:v1-6.4.5-T2", "Prepare testimony or a briefing for a legislative committee or governing board, stating "
              "the program's technical position and its evidence",
              "WF-RULE", modes=["MODE-ENGAGE"], rel=["intergovernmental"], formation="partial",
              derived=[("v1:6.4.5:T2", "rewritten")]),
            T("seed:v1-6.4.5-T3", "Provide technical assistance to legislative or council staff on draft language, "
              "explaining the implementation and fiscal effects of each provision",
              "WF-RULE", modes=["MODE-ENGAGE"], rel=["intergovernmental"], formation="partial",
              derived=[("v1:6.4.5:T3", "rewritten")]),
            T("seed:sc-prepare-fiscal-note", "Prepare a fiscal or implementation note on a proposed bill or ordinance, "
              "estimating its staffing, cost and schedule effects on the program",
              "WF-RULE", formation="partial", also=["seed:SC-C10"]),
        ],
        "levels": {
            "L2": [
                I("Summarizes a bill or ordinance's effect on program operations provision by provision, accepted by the "
                  "legislative liaison without correction of substance.", WS, tasks=["seed:v1-6.4.5-T1"],
                  evidence=["bill summary"]),
                I("Prepares a fiscal or implementation note on a proposed measure with cost, staffing and schedule "
                  "estimates traceable to program data.", WS + RA, tasks=["seed:sc-prepare-fiscal-note"],
                  evidence=["fiscal note"]),
            ],
            "L3": [
                I("Delivers testimony or a briefing to a committee or board in an observed or simulated hearing, answering "
                  "members' questions within the organization's approved position.", SIM, attr="ATT-SCO",
                  tasks=["seed:v1-6.4.5-T2"], evidence=["hearing observation record"]),
                I("Provides drafting assistance to legislative staff, explaining the implementation effect of each "
                  "provision and recording the advice given.", WS + RA, attr="ATT-KNO",
                  tasks=["seed:v1-6.4.5-T3"], evidence=["technical assistance log"]),
            ],
            "L4": [
                I("Sets a program's legislative priorities, positions and coordination steps for a session, approved by "
                  "leadership before the session opens.", PORT, attr="ATT-SCO", tasks=["seed:v1-6.4.5-T2"],
                  evidence=["session plan"]),
                I("Reviews program staff's testimony drafts and rehearsals against the organization's communications "
                  "rules before they appear, returning specific revisions.", RA + PORT, attr="ATT-FOR",
                  tasks=["seed:v1-6.4.5-T2"], evidence=["review record"]),
            ],
        },
        "enactments": [
            E("seed:ena-v1-6-4-5-federal", "Federal agency congressional liaison", "federal-agency",
              basis="Agency legislative affairs procedures; technical assistance on request; restrictions on using "
                    "appropriated funds for lobbying.",
              principal="The agency's legislative affairs office and leadership; OMB clearance of testimony.",
              venue="Congressional committees.",
              note="Testimony and technical assistance are cleared positions, so the staff skill is accuracy within "
                   "the approved position [J]."),
            E("seed:ena-v1-6-4-5-state", "State legislative process", "state-agency",
              basis="State legislative procedures and fiscal-note requirements; agency rules on legislative contact.",
              principal="The agency's legislative liaison and the governor's office.",
              venue="Legislative committees; fiscal offices.",
              note="SL review: fiscal notes are often prepared by program staff on short deadlines during session [J].",
              sl_reviewed=True),
            E("seed:ena-v1-6-4-5-local", "County board, council or utility commission process", "county",
              basis="Local legislative procedure (ordinances, budgets) and state rules for utility commissions.",
              principal="The elected board or commission.", venue="Public meetings and hearings.",
              note="SL review: local legislative work and executive staff work are often done by the same people [J].",
              sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ v1 6.3.4 (absorbs 6.4.3)
    {
        "id": "seed:v1-6.3.4",
        "label": "Analyze the economic effects of environmental decisions",
        "alt": ["economic impact analysis", "benefit-cost analysis", "regulatory impact analysis",
                "regulatory impact assessment"],
        "definition": "The capability to estimate the economic effects of proposed projects, programs and rules, "
                      "including regional economic impact, benefit-cost and regulatory impact analysis, with methods "
                      "suited to the decision and stated uncertainty. Disciplinary knowledge sits in the economics "
                      "knowledge area; this competency is the applied analysis.",
        "statement": "Estimates the economic effects of proposed projects, programs and rules (regional economic impact, "
                     "benefit-cost and regulatory impact analysis), choosing methods suited to the decision, stating "
                     "assumptions and uncertainty, and presenting results that decision-makers and reviewers can trace "
                     "to data.",
        "span": ("L1", "L4"),
        "derived": [("v1:6.4.3", "merged-from")],
        "sources": [],
        "editorial": "WP-05 (A5 SC), because the WP-05 list names v1 6.4.3 and this record is its merge target; the "
                     "defining craft of most tasks is data craft, so WP-04 (DC) is asked to co-review. v1 6.3.4 "
                     "rewrite: economic analysis of environmental decisions; absorbs 6.4.3 (regulatory impact "
                     "analysis), with rulemaking as an actor enactment. Valuation knowledge sits in the economics "
                     "knowledge area (v1 6.3.1 successor).",
        "sensitivity": [
            ("DM-10", "Rule changes require new benefit-cost analyses.", "J", None),
            ("DM-01", "Economic effects analyzed in reviews depend on review scope.", "E", ["V2-02"]),
        ],
        "tasks": [
            T("seed:v1-6.3.4-T1", "Estimate how a proposed project or policy changes local employment, income and business "
              "activity, stating the model, assumptions and uncertainty",
              "WF-ASSESS", formation="no", derived=[("v1:6.3.4:T1", "rewritten")]),
            T("seed:v1-6.3.4-T2", "Prepare the economic section of an environmental document or grant application, citing "
              "the data and methods behind each estimate",
              "WF-ASSESS", formation="no", derived=[("v1:6.3.4:T2", "rewritten")]),
            T("seed:v1-6.3.4-T3", "Present economic findings to interested parties and elected officials, explaining "
              "assumptions and uncertainty without overstating precision",
              "WF-ASSESS", modes=["MODE-ENGAGE"], rel=["public"], formation="partial",
              derived=[("v1:6.3.4:T3", "rewritten")]),
            T("seed:v1-6.4.3-T1", "Assess how a proposed policy change affects environmental quality, regulated parties and "
              "program operations, documenting each effect pathway considered",
              "WF-RULE", formation="partial", derived=[("v1:6.4.3:T1", "rewritten")]),
            T("seed:v1-6.4.3-T2", "Estimate the costs and benefits of alternative regulatory approaches, monetizing effects "
              "where defensible and describing those that cannot be monetized",
              "WF-RULE", formation="no", derived=[("v1:6.4.3:T2", "rewritten")]),
            T("seed:v1-6.4.3-T3", "Prepare the regulatory impact analysis supporting a proposed rule, presenting costs, "
              "benefits and distributional effects of each alternative considered",
              "WF-RULE", formation="partial", profiles=["WP-RULEMAKING"], derived=[("v1:6.4.3:T3", "rewritten")]),
        ],
        "levels": {
            "L1": [
                I("Compiles the data tables for an economic analysis from assigned sources, citing source and vintage for "
                  "each figure and flagging gaps to the analyst.", WS + RA, tasks=["seed:v1-6.3.4-T2"],
                  evidence=["data tables"]),
                I("Runs a supplied regional input-output model for a defined project scenario, reproducing a reviewer's "
                  "check run within the stated tolerance.", WS, tasks=["seed:v1-6.3.4-T1"], evidence=["model run"]),
            ],
            "L2": [
                I("Prepares the economic section of an environmental document in which each estimate cites its data, "
                  "method and assumptions, accepted by the reviewer without rework.", WS, attr="ATT-AUT",
                  tasks=["seed:v1-6.3.4-T2"], evidence=["economic section"]),
                I("Estimates costs and benefits of alternatives for a routine rule, monetizing effects where defensible "
                  "and describing unmonetized effects qualitatively.", WS, attr="ATT-KNO",
                  tasks=["seed:v1-6.4.3-T2"], evidence=["benefit-cost tables"]),
            ],
            "L3": [
                I("Chooses and justifies the economic method for a non-routine decision, documenting why alternatives "
                  "were rejected and how uncertainty was characterized.", WS + BARS, attr="ATT-GUI",
                  tasks=["seed:v1-6.4.3-T3"], evidence=["method memo"]),
                I("Explains economic findings and their uncertainty to decision-makers and the public, answering each "
                  "challenge to assumptions with evidence.", SIM, attr="ATT-SCO", obs4=2,
                  tasks=["seed:v1-6.3.4-T3"], evidence=["observation record"]),
                I("Documents each effect pathway considered in a policy-change assessment, so that a reviewer can trace "
                  "every estimate to its data source.", RA + WS, attr="ATT-CPX", tasks=["seed:v1-6.4.3-T1"],
                  evidence=["pathway table"]),
            ],
            "L4": [
                I("Sets a program's economic-analysis guidelines, including discounting, uncertainty and distributional "
                  "requirements, with a revision log tied to peer-review findings.", PORT, attr="ATT-GUI",
                  tasks=["seed:v1-6.4.3-T3"], evidence=["guidelines", "revision log"]),
                I("Reviews other analysts' benefit-cost and impact analyses against the guidelines, returning each with "
                  "specific corrections before release.", RA, attr="ATT-FOR", tasks=["seed:v1-6.4.3-T2"],
                  evidence=["review comments"]),
            ],
        },
        "enactments": [
            E("seed:ena-v1-6-3-4-federal-rulemaking", "Federal regulatory impact analysis", "federal-regulator",
              position="regulator",
              basis="Executive-branch regulatory review requirements for significant rules and OMB guidance on "
                    "regulatory analysis; statutory analyses for small entities.",
              principal="The rulemaking office and OMB's regulatory review office.",
              venue="OMB review; public comment; judicial review of the rule.",
              note="Rulemaking enactment named in the v1 disposition for 6.4.3. The governing review order and OMB "
                   "guidance are L5 instruments not yet registered (worklog) [J]."),
            E("seed:ena-v1-6-3-4-state-rulemaking", "State economic impact statements for rules", "state-agency",
              position="regulator",
              basis="State administrative procedure act requirements for economic or fiscal impact statements on "
                    "proposed rules.",
              principal="The state rulemaking agency; legislative rule-review committees.",
              venue="Legislative rule review; state courts.",
              note="SL review: requirements vary widely by state, from short fiscal notes to full small-business impact "
                   "analyses [J].", sl_reviewed=True),
        ],
    },
]
