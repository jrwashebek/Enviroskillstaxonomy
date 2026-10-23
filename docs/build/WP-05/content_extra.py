"""WP-05 content: further SC-primary core rows needed by P1 roles or targeted by other lanes' tasks (lane rule:
target competency's primary craft is SC): SC-C02 (record; receives v1 6.4.4 split part), SC-C07 (negotiation),
SC-C06 (discretionary engagement; receives v1 6.4.4 T1), SC-C15 (multi-regime disclosure; receives v1 3.6.2)."""
from wp05dsl import T, I, E

WS = ["work-sample"]
RA = ["record-audit"]
SEW = ["seeded-error-work-sample"]
BARS = ["structured-interview-bars"]
SIM = ["simulation-role-play"]
MOOT = ["moot-defense"]
PORT = ["portfolio-review"]
KT = ["knowledge-test"]
C360 = ["counterpart-360"]

COMPETENCIES = [
    # ------------------------------------------------------------------ SC-C02
    {
        "id": "seed:SC-C02",
        "label": "Build and maintain a defensible administrative record",
        "alt": ["administrative record", "record of decision support", "response to comments", "AI provenance in the record"],
        "definition": "The capability to document the reasons for a decision as it is made, including alternatives, "
                      "boundaries, responses to substantive comments, consultation outcomes and the provenance of "
                      "analyses (AI-assisted content included), so that a court, inspector general or successor can "
                      "reconstruct why the decision was reasonable.",
        "statement": "Documents the reasons for decisions as they are made: the alternatives considered, how scope and "
                     "effects boundaries were drawn, responses to substantive comments, consultation outcomes and the "
                     "provenance of analyses including AI-assisted content, so that a reviewing court, inspector general "
                     "or successor can reconstruct why the decision was reasonable.",
        "span": ("L1", "L4"),
        "derived": [("v1:6.4.4", "split-from")],
        "sources": ["SC-012", "SC-009", "SC-037", "SC-010", "SC-011", "V2-02", "V2-03", "V2-08"],
        "editorial": "WP-05 (A5 SC). Survivor: absorbs FS-C03 (AI provenance in the record) and SC-C05 (supervise "
                     "AI-assisted drafting and comment analysis for legal defensibility); SC-C05's legal-adequacy anchors "
                     "survive as indicators here and in the SC enactment of AI-output validation (DC-CAND-13, WP-04) "
                     "(ADR-0025). Receives the record half of v1 6.4.4 (split with DC-CAND-16). Under substantial "
                     "deference the reasoned explanation is the main defense; about 0.4 percent of submissions on one "
                     "2025 docket were unique, so merged comment groups can hide the comment that matters [E: V2-02, "
                     "SC-011]. Indicators adapted from SC-A-C02-1..4 and SC-A-C05-1..4.",
        "sensitivity": [
            ("DM-08", "Deference and remedy doctrine make the reasoned explanation the main defense.", "E", ["V2-02"]),
            ("DM-04", "Pending standing rules would tie challenges to substantive, unique comments.", "E", ["V2-03"]),
            ("DM-14", "Record management and AI provenance are minimum requirements of federal permitting systems.", "E", ["V2-08", "SC-037"]),
        ],
        "tasks": [
            T("seed:sc-index-record-documents", "Index documents into the administrative record with dates, authors and "
              "provenance labels, marking which content was produced with AI assistance",
              "WF-REVIEW", formation="no", profiles=["WP-PROJECT"]),
            T("seed:sc-confirm-comment-responses", "Confirm that every substantive comment in a docket has a reasoned "
              "response, sampling machine-grouped comments for unique points the grouping missed",
              "WF-REVIEW", modes=["MODE-RESOLVE"], formation="yes", profiles=["WP-PROJECT", "WP-RULEMAKING"]),
            T("seed:v1-6.4.4-T3", "Publish comment summaries and the agency's responses in the record, linking each "
              "response to the substantive comments it answers",
              "WF-REVIEW", modes=["MODE-ENGAGE"], rel=["public"], formation="partial",
              derived=[("v1:6.4.4:T3", "rewritten")]),
            T("seed:sc-certify-administrative-record", "Certify an administrative record for litigation by its deadline, "
              "checking completeness against the decision documents and the record index",
              "WF-REVIEW", modes=["MODE-RESOLVE"], formation="partial", signoff="legal-signatory"),
            T("seed:sc-write-reasoned-explanation", "Write the reasoned explanation that links the evidence in the record "
              "to each choice made in a decision",
              "WF-REVIEW", formation="yes", profiles=["WP-PROJECT"]),
        ],
        "levels": {
            "L1": [
                I("Files documents to the record index with correct dates, authors and provenance labels, including AI "
                  "assistance, so that a quality-assurance sample meets the record checklist.", RA,
                  tasks=["seed:sc-index-record-documents"], evidence=["record index"]),
                I("Checks cited facts and sources in an AI-drafted response to comments, logging each error found before "
                  "the draft goes to the reviewer.", SEW, mode="assisted", tasks=["seed:v1-6.4.4-T3"],
                  evidence=["verification log"]),
            ],
            "L2": [
                I("Certifies the record for an assessment-level decision by its deadline, with decision memo, comment "
                  "responses and consultation outcomes present and no gap found in quality review.", RA + WS,
                  attr="ATT-AUT", tasks=["seed:sc-certify-administrative-record"], evidence=["certified record"],
                  critical=True),
                I("Samples machine-grouped public comments to check how many substantive comments were missed or "
                  "merged, recording each unique substantive comment found.", SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:sc-confirm-comment-responses"], evidence=["sampling log"]),
                I("Confirms in a test docket with known unique comments that every substantive comment has a reasoned "
                  "response, at the detection rate the program sets.", SEW, attr="ATT-KNO", mode="assisted",
                  tasks=["seed:sc-confirm-comment-responses"], evidence=["comment-response matrix"]),
            ],
            "L3": [
                I("Writes the reasoned explanation for a controversial decision, linking the record evidence to each "
                  "choice and anticipating the claims likely to be raised.", WS + MOOT, attr="ATT-CPX",
                  tasks=["seed:sc-write-reasoned-explanation"], evidence=["decision rationale"]),
                I("Defends a decision rationale in a moot oral defense, answering each challenge with a record citation.",
                  MOOT, attr="ATT-SCO", tasks=["seed:sc-write-reasoned-explanation"], evidence=["moot record"]),
                I("Writes a project's AI-use plan for the record, stating which tasks used AI, the checks applied and who "
                  "signed off, accepted by counsel.", WS + PORT, attr="ATT-AUG", mode="supervisory",
                  tasks=["seed:sc-index-record-documents"], evidence=["AI-use plan"]),
            ],
            "L4": [
                I("Sets an organization's record and AI-provenance standards, with audit criteria that units apply to "
                  "every decision record.", PORT, attr="ATT-GUI", tasks=["seed:sc-index-record-documents"],
                  evidence=["record standard"]),
                I("Evaluates staff record files against the organization's standard, returning each with the defects to "
                  "correct before certification.", RA, attr="ATT-FOR", tasks=["seed:sc-certify-administrative-record"],
                  evidence=["review comments"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c02-federal", "Federal administrative record", "federal-agency",
              basis="Judicial review on the administrative record; the 2025 Supreme Court standard of substantial "
                    "deference in environmental review; record-management requirements in federal permitting "
                    "technology standards; federal AI-use policy for agencies.",
              principal="The deciding official, with agency counsel.", venue="Federal courts; inspectors general.",
              note="Structured, provenance-tagged records (for example LLM-extracted, validated or unreviewed field "
                   "tags) are a workable pattern for AI provenance [E: SC-009].",
              instruments=["seven-county", "ceq-permitting-data-standard", "permitting-tech-action-plan", "omb-m-25-21",
                           "speed-act"], evidence="E", sources=["V2-02", "V2-03", "V2-08", "SC-009"]),
            E("seed:ena-sc-c02-state", "State record of proceedings", "state-agency",
              basis="State administrative procedure acts and state environmental policy act record requirements.",
              principal="The state lead agency and attorney general.", venue="State courts.",
              note="SL review: state record rules and certification deadlines differ; the record discipline "
                   "transfers [J].", instruments=["ceqa-2025-reforms"], sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ SC-C07
    {
        "id": "seed:SC-C07",
        "label": "Negotiate permit conditions, mitigation and agreements using interest-based methods",
        "alt": ["interest-based negotiation", "permit negotiation", "settlement negotiation", "mitigation negotiation"],
        "definition": "The capability to prepare for and conduct negotiations over permit conditions, mitigation, "
                      "settlement terms and partnership agreements so that the result is within each party's authority "
                      "and can be implemented and verified. Mediation as a neutral is a separate competency (conflict "
                      "resolution and mediation).",
        "statement": "Prepares for and conducts negotiations over permit conditions, mitigation, settlement terms or "
                     "partnership agreements: separates interests from positions, generates options, knows each party's "
                     "alternatives to agreement and authority limits, and turns agreements into terms that can be "
                     "implemented and verified.",
        "span": ("L1", "L4"),
        "sources": ["SC-050", "SC-052", "SC-018", "SC-019"],
        "editorial": "WP-05 (A5 SC). Core Statecraft practice with actor enactments (ADR-0025 section 4), paired with "
                     "v1 5.2.4 (conflict resolution and mediation, carried). The negotiation-training literature "
                     "(SC-050, SC-052) was not re-read this session, so teachability claims are [J]. Not defined by the "
                     "withdrawn OPM ECQ competency names (influencing/negotiating, partnering). Indicators adapted from "
                     "SC-A-C07-1..4.",
        "sensitivity": [
            ("DM-06", "Changes in species protection rules widen the room for negotiated measures.", "E", ["V2-05"]),
            ("DM-12", "Agreement authorities set what partners may agree to.", "E", ["SC-030"]),
        ],
        "tasks": [
            T("seed:sc-prepare-negotiation-brief", "Prepare a negotiation brief stating own and counterpart interests, "
              "alternatives to agreement, the issue list and the limits of one's authority",
              "WF-AUTHORIZE", modes=["MODE-RESOLVE"], formation="partial"),
            T("seed:sc-negotiate-permit-conditions", "Negotiate permit conditions or mitigation with an applicant, "
              "generating options that meet the governing requirements and recording the agreed terms",
              "WF-AUTHORIZE", modes=["MODE-RESOLVE"], rel=["stakeholder"], formation="yes"),
            T("seed:sc-lead-multiparty-negotiation", "Lead a multi-party negotiation over a settlement or partnership "
              "agreement, keeping each party's commitments within its authority",
              "WF-AUTHORIZE", modes=["MODE-RESOLVE"], rel=["intergovernmental", "stakeholder"], formation="yes"),
            T("seed:sc-convert-agreement-terms", "Convert a negotiated agreement into implementable terms, checking each "
              "term against a verification method before signature",
              "WF-AUTHORIZE", modes=["MODE-RESOLVE"], formation="partial", also=["seed:SC-C16"]),
        ],
        "levels": {
            "L1": [
                I("Prepares a negotiation brief listing own and counterpart interests, alternatives to agreement, issues "
                  "and authority limits, scored in a standardized simulation.", SIM,
                  tasks=["seed:sc-prepare-negotiation-brief"], evidence=["negotiation brief"]),
                I("Records the positions, offers and agreed points of each negotiation session for the lead negotiator, "
                  "with no agreed term missing from the record.", RA, tasks=["seed:sc-negotiate-permit-conditions"],
                  evidence=["session record"]),
            ],
            "L2": [
                I("Leads a routine negotiation over permit conditions or mitigation in a standardized role-play, reaching "
                  "terms that stay within authority and the scenario's requirements.", SIM, attr="ATT-AUT",
                  tasks=["seed:sc-negotiate-permit-conditions"], evidence=["simulation score sheet"]),
                I("Generates at least two options that meet the parties' stated interests before proposing terms in a "
                  "negotiation simulation.", SIM, attr="ATT-GUI", tasks=["seed:sc-negotiate-permit-conditions"],
                  evidence=["option list"]),
            ],
            "L3": [
                I("Leads a multi-party negotiation in a non-routine simulation, keeping each party's commitments within "
                  "its authority and recording how deadlocks were broken.", SIM, attr="ATT-CPX",
                  tasks=["seed:sc-lead-multiparty-negotiation"], evidence=["simulation record"]),
                I("Converts a negotiated agreement into terms with a verification method for each, accepted by counsel "
                  "without substantive revision.", WS, attr="ATT-SCO", tasks=["seed:sc-convert-agreement-terms"],
                  evidence=["agreement terms"]),
                I("Concludes contested permit or settlement terms that counterparts rate as clear and workable in "
                  "structured counterpart feedback.", C360 + PORT, attr="ATT-SCO", obs4=2,
                  tasks=["seed:sc-lead-multiparty-negotiation"], evidence=["counterpart feedback"]),
            ],
            "L4": [
                I("Sets an organization's negotiation mandates and escalation rules for recurring negotiation types, "
                  "stating the authority limits for each role.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-prepare-negotiation-brief"], evidence=["mandate document"]),
                I("Revises the program's model terms after reviewing each year which negotiated terms failed in "
                  "implementation.", PORT + RA, attr="ATT-GUI", tasks=["seed:sc-convert-agreement-terms"],
                  evidence=["model terms", "review record"]),
                I("Coaches negotiators through preparation and debrief of live negotiations, evaluating each brief "
                  "against the organization's preparation standard.", PORT, attr="ATT-FOR", obs4=2,
                  tasks=["seed:sc-prepare-negotiation-brief"], evidence=["coaching record"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c07-regulator", "Regulator negotiating conditions and settlements", "state-agency",
              position="regulator",
              basis="Permit and enforcement authority; legal minimums the regulator cannot negotiate away.",
              principal="The permit or enforcement decision-maker.", venue="Permit appeals; courts.",
              note="SL review: the regulator's mandate sets the floor; interests can be traded above it [J].",
              sl_reviewed=True),
            E("seed:ena-sc-c07-regulated-party", "Applicant or permittee negotiating terms", "firm",
              position="regulated-party",
              basis="No authority; rights to comment, appeal and propose alternatives.",
              principal="Facility management, project finance and counsel.", venue="Agency decisions; appeals.",
              note="Mirror of the regulator enactment for regulator-to-regulated mobility [J]."),
            E("seed:ena-sc-c07-advocate", "Advocate negotiating settlements and agreements", "advocacy-organization",
              position="advocate",
              basis="Standing in litigation or administrative appeals; coalition agreements.",
              principal="The board and members.", venue="Courts; settlement approval.",
              note="Advocates negotiate from litigation leverage rather than decision authority [J]."),
        ],
    },
    # ------------------------------------------------------------------ SC-C06
    {
        "id": "seed:SC-C06",
        "label": "Design proportionate public engagement when participation is discretionary",
        "alt": ["public involvement design", "engagement planning", "public participation", "inclusive engagement"],
        "definition": "The capability to decide when, with whom and how to engage the public and interested parties "
                      "beyond what a procedure requires, to document why, and to close the loop with participants. "
                      "Consultation owed to other governments is a distinct relationship and is not covered here.",
        "statement": "Decides when, with whom and how to engage the public and interested parties beyond legal "
                     "minimums, based on legitimacy risk, the interests affected, community relationships and litigation "
                     "exposure; documents the rationale; runs the engagement; and shows participants what their input "
                     "changed.",
        "span": ("L1", "L4"),
        "sources": ["SC-038", "SC-014", "SC-039", "SC-042"],
        "editorial": "WP-05 (A5 SC). Proportionate engagement design when participation is discretionary (SC verdict on "
                     "5.2.x); pairs with the v1 5.3.4 split A record (accessible, inclusive engagement). Under department "
                     "procedures adopted in 2026, lower levels of review need no public involvement, so engagement "
                     "becomes a judgment someone must make and defend [E: SC-038]. Receives v1 6.4.4 T1 (input process "
                     "design). Government-to-government consultation is held content (TN-C02) and kept separate. "
                     "Indicators adapted from SC-A-C06-1..4.",
        "sensitivity": [
            ("DM-04", "Required public involvement shrank; discretion over engagement grew.", "E", ["SC-038", "V2-01"]),
            ("DM-02", "Shortened comment and objection windows change engagement timing.", "E", ["V2-04"]),
        ],
        "tasks": [
            T("seed:v1-6.4.4-T1", "Design the process for collecting and responding to public input on a proposed action, "
              "sized to the action's legitimacy and litigation risk",
              "WF-REVIEW", modes=["MODE-ENGAGE"], rel=["public"], formation="partial",
              derived=[("v1:6.4.4:T1", "rewritten")]),
            T("seed:sc-distinguish-required-participation", "Distinguish the participation steps a procedure requires "
              "from those that are discretionary for a proposed action, recording the basis for each",
              "WF-REVIEW", modes=["MODE-ENGAGE"], formation="partial"),
            T("seed:sc-write-engagement-plan", "Write an engagement plan stating who will be engaged, by which methods and "
              "when, and why that scope fits the decision",
              "WF-REVIEW", modes=["MODE-ENGAGE"], rel=["public", "stakeholder"], formation="partial"),
            T("seed:sc-publish-what-we-heard", "Publish a record showing participants how their input changed the decision "
              "or why it did not",
              "WF-REVIEW", modes=["MODE-ENGAGE"], rel=["public"], formation="partial"),
        ],
        "levels": {
            "L1": [
                I("Lists the participation steps a procedure requires and those that are discretionary for a seeded "
                  "case, with no required step omitted.", KT + WS, tasks=["seed:sc-distinguish-required-participation"],
                  evidence=["checklist"]),
                I("Logs contacts and comments for an engagement process so that every input sampled in audit appears in "
                  "the record with its date and source.", RA, tasks=["seed:v1-6.4.4-T1"], evidence=["contact log"]),
            ],
            "L2": [
                I("Writes an engagement plan sized to the decision's legitimacy and litigation risk, with methods matched "
                  "to the parties involved, accepted by the responsible official.", WS, attr="ATT-AUT",
                  tasks=["seed:sc-write-engagement-plan"], evidence=["engagement plan"]),
                I("Writes the record for participants stating how each theme of input changed the decision or why it did "
                  "not.", WS,
                  attr="ATT-SCO", tasks=["seed:sc-publish-what-we-heard"], evidence=["what-we-heard record"]),
            ],
            "L3": [
                I("Designs engagement for a contested decision with several publics, timed to the decision points, and "
                  "records how the design changed when conflict escalated.", PORT, attr="ATT-CPX",
                  tasks=["seed:sc-write-engagement-plan"], evidence=["engagement design", "change log"]),
                I("Justifies in writing a decision to engage beyond, or only to, the legal minimum, citing the legitimacy "
                  "and litigation risks weighed.", WS + BARS, attr="ATT-GUI",
                  tasks=["seed:sc-distinguish-required-participation"], evidence=["justification memo"]),
            ],
            "L4": [
                I("Sets an organization's policy on when to engage beyond legal minimums, with criteria staff apply and "
                  "an annual evaluation of outcomes.", PORT, attr="ATT-GUI", tasks=["seed:v1-6.4.4-T1"],
                  evidence=["policy", "evaluation"]),
                I("Evaluates engagement plans across a portfolio against the policy criteria, returning each plan with the "
                  "changes required before launch.", RA, attr="ATT-FOR", tasks=["seed:sc-write-engagement-plan"],
                  evidence=["plan reviews"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c06-federal", "Federal discretionary public involvement", "federal-agency",
              basis="Department environmental-review procedures that make public involvement discretionary for lower "
                    "levels of review and require comment solicitation for impact statements; objection rules.",
              principal="The responsible official.", venue="Federal courts; objection reviewers; Congress.",
              note="Federal engagement moved from a compliance step to a reasoned choice in 2026 [E: SC-038].",
              instruments=["doi-nepa-procedures", "usda-nepa-procedures", "ceq-nepa-regs-removal", "usfs-objection-rule"],
              evidence="E", sources=["SC-038", "V2-01"]),
            E("seed:ena-sc-c06-local", "Local open-meeting and hearing requirements", "county",
              basis="State open-meeting laws and local hearing requirements for land-use and permit decisions.",
              principal="The elected board or planning commission.", venue="Public hearings; state courts.",
              note="SL review: local engagement is mostly required hearings; discretion lies in what happens before "
                   "them [J].", sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ SC-C15
    {
        "id": "seed:SC-C15",
        "label": "Manage regulated-entity disclosure and compliance across divergent regimes",
        "alt": ["sustainability reporting and disclosure", "climate disclosure", "GHG disclosure",
                "assurance-ready disclosure", "regulatory reporting across jurisdictions"],
        "definition": "The capability of a regulated organization to determine which mandatory disclosure and reporting "
                      "regimes apply to it, to produce controlled, assurance-ready data and narrative, and to manage "
                      "regulator, assurance-provider and investor relationships as regimes start, change or are "
                      "enjoined. Reporting frameworks are L4 tools; regimes are L5 instruments.",
        "statement": "Determines which mandatory disclosure and reporting regimes apply to an organization across "
                     "jurisdictions, builds controlled processes that produce assurance-ready data, prepares for external "
                     "assurance, and manages regulator, assurance-provider and investor relationships as rules start, "
                     "change or are enjoined.",
        "span": ("L1", "L4"),
        "derived": [("v1:3.6.2", "merged-from")],
        "sources": ["SC-027", "SC-028", "SC-029", "V2-15"],
        "editorial": "WP-05 (A5 SC). Survivor for disclosure across divergent regimes: absorbs DB-C44, FS-C18, PS-C05 "
                     "and v1 3.6.2 (merged). Actor-specific competency authorized by ADR-0007 B.5(4). California's first "
                     "Scope 1 and 2 reports are due 2026-11-10, its climate-risk report is enjoined and the EU scope "
                     "narrowed [E: V2-15]. v1 3.6.2 tasks named sensors, AI tools and ledgers; tools move to L4. "
                     "Indicators adapted in part from IO exemplar rewrites for v1 3.6.2.",
        "sensitivity": [
            ("DM-13", "Mandatory disclosure regimes are starting, narrowing or enjoined by jurisdiction.", "E", ["V2-15"]),
            ("DM-10", "Federal greenhouse-gas reporting and standards are being reconsidered.", "E", ["V2-06"]),
        ],
        "tasks": [
            T("seed:v1-3.6.2-T1", "Prepare a mandatory disclosure report from controlled data collected across operations, "
              "tracing each reported figure to its source system",
              "WF-MONITOR.attest", formation="no", derived=[("v1:3.6.2:T1", "rewritten")]),
            T("seed:v1-3.6.2-T2", "Map each disclosure requirement of the regimes that apply to the organization to the "
              "data and control that satisfy it, flagging gaps",
              "WF-MONITOR.attest", formation="partial", derived=[("v1:3.6.2:T2", "rewritten")]),
            T("seed:v1-3.6.2-T3", "Prepare disclosure data and control documentation for external assurance, answering "
              "each assurance finding with evidence or a correction",
              "WF-MONITOR.attest", formation="partial", derived=[("v1:3.6.2:T3", "rewritten")]),
            T("seed:sc-determine-disclosure-applicability", "Determine which disclosure regimes apply to the organization "
              "by jurisdiction, size and activity, recording each applicability decision and its review date",
              "WF-MONITOR.attest", formation="partial"),
            T("seed:sc-replan-disclosure", "Adjust the organization's reporting plan when a disclosure rule is enjoined, "
              "narrowed or starts, briefing executives on changed obligations and risks",
              "WF-MONITOR.attest", modes=["MODE-ENGAGE"], formation="partial"),
        ],
        "levels": {
            "L1": [
                I("Collects metric data from designated source systems using the reporting-period request, recording "
                  "source, date and any estimation method for each value.", RA + WS,
                  tasks=["seed:v1-3.6.2-T1"], evidence=["data collection workbook"]),
                I("Checks automated data feeds for a disclosure against source records for a sample period, recording "
                  "each discrepancy.", SEW, mode="assisted", tasks=["seed:v1-3.6.2-T1"], evidence=["check log"]),
            ],
            "L2": [
                I("Traces each reported metric to its source data and calculation method, so that an assurance provider "
                  "can re-perform the calculation.", WS + RA, attr="ATT-AUT",
                  tasks=["seed:v1-3.6.2-T3"], evidence=["metric workpapers"]),
                I("Records an applicability decision for each disclosure regime by jurisdiction, size and activity, with "
                  "the evidence relied on and a review date.", WS, attr="ATT-KNO",
                  tasks=["seed:sc-determine-disclosure-applicability"], evidence=["applicability register"]),
            ],
            "L3": [
                I("Responds to assurance-provider findings by correcting or defending each finding with documented "
                  "evidence within the assurance timetable.", SIM + RA, attr="ATT-SCO", mode="assisted",
                  tasks=["seed:v1-3.6.2-T3"], evidence=["finding responses"]),
                I("Re-plans the organization's reporting when a regime is enjoined, narrowed or starts, stating changed "
                  "obligations and risks to executives in writing.", WS + BARS, attr="ATT-CPX",
                  tasks=["seed:sc-replan-disclosure"], evidence=["reporting plan memo"]),
            ],
            "L4": [
                I("Designs the organization's disclosure control process across regimes, with data ownership, review "
                  "steps, AI-tool use rules and sign-off, so that it passes internal-audit review.", PORT,
                  attr="ATT-GUI", mode="supervisory", tasks=["seed:v1-3.6.2-T2"], evidence=["control design"]),
                I("Evaluates site and function reporting leads against the control framework before approving them to "
                  "submit data for disclosure.", RA, attr="ATT-FOR", tasks=["seed:v1-3.6.2-T1"],
                  evidence=["evaluation record"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c15-private", "Company subject to several disclosure regimes", "firm",
              position="regulated-party",
              basis="State climate-disclosure statutes and regulations (California's emissions and climate-risk laws, "
                    "the latter enjoined), the EU sustainability-reporting directive as narrowed in 2026, and federal "
                    "reporting programmes under reconsideration.",
              principal="Executives, the board and investors.",
              venue="State regulators; EU national authorities; assurance providers; securities litigation.",
              note="Jurisdictional judgment is now as much of the job as reporting [E: V2-15].",
              instruments=["ca-sb-253", "ca-sb-261", "eu-omnibus-i", "sec-climate-disclosure", "ghgrp-reconsideration"],
              evidence="E", sources=["V2-15", "V2-06"]),
            E("seed:ena-sc-c15-consultant", "Consultant preparing disclosures for clients", "firm",
              position="service-provider",
              basis="Engagement terms with the reporting company; independence limits where the firm also provides "
                    "assurance.",
              principal="The client.", venue="Assurance review; professional standards.",
              note="Preparers cannot also assure the same disclosure; see PS-C18 [J]."),
        ],
    },
]
