"""WP-05 content: authorization cluster (SL-C02 with regulator and resource-manager variants, SC-C01, SC-C14, v1 5.5.2)."""
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
    # ------------------------------------------------------------------ SL-C02
    {
        "id": "seed:SL-C02",
        "label": "Issue environmental permits and resource-use authorizations as the deciding authority",
        "alt": ["permit writing", "permit writer", "NPDES permit writer", "air permit engineer", "Title V permitting",
                "dredge-and-fill permit review", "special-use permit administration", "grazing permit administration"],
        "definition": "The capability of the authority that decides an application to evaluate it, derive and draft the "
                      "limits, conditions and monitoring that implement the governing requirements, answer public "
                      "comment, and issue, condition or deny the permit or authorization on a defensible record. "
                      "Excludes the applicant's side of the process and the programme knowledge of each permit type, "
                      "which module enactments carry.",
        "statement": "Evaluates applications against the applicable law, rules and technical standards; derives limits, "
                     "conditions and monitoring requirements from the technical record; drafts the permit or "
                     "authorization and its fact sheet or decision rationale; responds to comments; and issues, "
                     "conditions or denies it on a record that withstands administrative and judicial review.",
        "span": ("L1", "L4"),
        "derived": [("v1:6.1.3", "split-from"), ("v1:6.7.5", "split-from")],
        "sources": ["SL-079", "SL-073", "SL-076", "SL-050", "SL-088", "SC-021", "V2-06", "V2-07"],
        "editorial": "WP-05 (A5 SC; SL reviewed the state and local enactments). Survivor for permit and authorization "
                     "writing: absorbs DB-C07, DB-C12 (air permitting part of v1 6.7.5) and C-LM-03 and the regulator half "
                     "of v1 6.1.3. Regulator and resource-manager variants are actor enactments with authorityPosition; "
                     "programme specifics (water discharge, air operating, waste, wetland fill, land-use authorizations) "
                     "are module enactments (WP-06). v1 described this work from the applicant side; state postings "
                     "describe the permit-writer side [E: SL-079, SL-088]. Mirror links: SC-C01 regulated-party "
                     "enactment (applicant pathway) and DB-C26 (permittee compliance).",
        "sensitivity": [
            ("DM-11", "Delegated and assumed permit programmes can revert to federal administration.", "E", ["SC-021"]),
            ("DM-09", "Jurisdictional scope (which waters, sources or lands are covered) is being narrowed by rule.", "E", ["V2-07"]),
            ("DM-10", "Substantive standards behind some permit limits were rescinded and are litigated.", "E", ["V2-06"]),
            ("DM-14", "Electronic permitting and AI drafting change production of permits and fact sheets.", "E", ["V2-08"]),
            ("DM-15", "Permit fees and cost recovery fund many state permit programmes.", "J", None),
        ],
        "learning": "Assess with permit-file work samples (limit derivation, condition drafting) and seeded-error "
                    "review of AI-drafted permits; programme-specific anchors come from module enactments.",
        "tasks": [
            T("seed:sc-check-permit-completeness", "Review a permit application for administrative and technical "
              "completeness, issuing a deficiency notice that lists each missing element and its basis",
              "WF-AUTHORIZE", formation="partial", profiles=["WP-REGPROGRAM"]),
            T("seed:sc-derive-permit-limits", "Derive permit limits and conditions from the applicable technical standards "
              "and the facility's technical record, documenting the calculation basis for each limit",
              "WF-AUTHORIZE", formation="yes", profiles=["WP-REGPROGRAM"],
              regime={"mentorshipDependence": "H", "cycleDependence": "none", "placeBoundness": "general", "currencyDecay": "M"}),
            T("seed:sc-draft-permit-fact-sheet", "Draft a permit and its fact sheet so that each condition is measurable, "
              "enforceable and traceable to its legal or technical basis",
              "WF-AUTHORIZE", formation="yes", profiles=["WP-REGPROGRAM"], also=["seed:SC-C16"]),
            T("seed:sc-review-ai-drafted-permit", "Review an AI-drafted permit or fact sheet against the application record "
              "and permit template, correcting each condition that lacks a traceable basis",
              "WF-AUTHORIZE", formation="yes", profiles=["WP-REGPROGRAM"],
              note="Review counterpart of the drafting task (G-2): drafting compresses, limit derivation and "
                   "defensibility do not [E: SL-079; J]."),
            T("seed:sc-respond-permit-comments", "Respond to public comments on a draft permit, revising conditions where a "
              "comment shows an error and explaining each decision in the response document",
              "WF-AUTHORIZE", modes=["MODE-ENGAGE"], rel=["public"], profiles=["WP-REGPROGRAM"]),
            T("seed:sc-issue-resource-use-authorization", "Decide a request to use public land or water resources, setting the "
              "authorization's terms, fees and monitoring conditions within the governing management plan",
              "WF-AUTHORIZE", formation="yes", field="on-site-preferred",
              note="Resource-manager variant task (special uses, grazing, mineral and right-of-way authorizations)."),
        ],
        "levels": {
            "L1": [
                I("Completes an application completeness check against the program checklist, listing each missing "
                  "element and the rule provision that requires it.", WS + RA,
                  tasks=["seed:sc-check-permit-completeness"], evidence=["completeness checklist", "deficiency notice"]),
                I("Calculates limits for a routine facility from a supplied template and data, matching a qualified "
                  "writer's check calculation within the program's tolerance.", WS,
                  tasks=["seed:sc-derive-permit-limits"], evidence=["limit calculation"]),
            ],
            "L2": [
                I("Drafts a routine permit and fact sheet in which every condition cites its legal or technical basis, "
                  "accepted by the supervisor without substantive rework.", WS + PORT, attr="ATT-AUT",
                  tasks=["seed:sc-draft-permit-fact-sheet"], evidence=["permit", "fact sheet"]),
                I("Derives limits and monitoring requirements for a routine facility, documenting each assumption and data "
                  "source used in the calculation.", WS, attr="ATT-KNO", tasks=["seed:sc-derive-permit-limits"],
                  evidence=["calculation workbook"]),
                I("Verifies an AI-drafted permit section against the application record, correcting or removing each "
                  "condition whose basis cannot be traced.", SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:sc-review-ai-drafted-permit"], evidence=["verification log"]),
            ],
            "L3": [
                I("Writes permits for non-routine facilities where standards conflict or data are uncertain, documenting "
                  "in the fact sheet how each conflict was resolved.", PORT + BARS, attr="ATT-CPX",
                  tasks=["seed:sc-derive-permit-limits"], evidence=["permit file"]),
                I("Responds to contested comments and appeals on a draft permit, revising conditions where errors are "
                  "shown and defending the rest on the record.", MOOT + PORT, attr="ATT-SCO",
                  tasks=["seed:sc-respond-permit-comments"], evidence=["response to comments"]),
                I("Reviews other writers' AI-assisted permit drafts, setting the share of conditions checked against "
                  "source data and recording each rejection reason.", RA + SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:sc-review-ai-drafted-permit"], evidence=["sampling plan", "rejection log"]),
            ],
            "L4": [
                I("Sets permit templates, limit-derivation procedures and quality checks for a permit program, revising "
                  "them when standards or case law change.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-draft-permit-fact-sheet"], evidence=["program procedures"]),
                I("Certifies permit writers for independent issuance after reviewing their permit files against the "
                  "program's quality standard.", RA + PORT, attr="ATT-FOR", tasks=["seed:sc-draft-permit-fact-sheet"],
                  evidence=["certification record"]),
            ],
        },
        "enactments": [
            E("seed:ena-sl-c02-state-regulator", "State permit writer in a delegated or state programme", "state-agency",
              position="regulator",
              basis="State statute and rules; for delegated or authorized federal programmes (water discharge permits, "
                    "air operating permits, hazardous waste permits, assumed dredge-and-fill permits) also the federal "
                    "authorization. Delegated constraints: state requirements at least as stringent as the federal "
                    "minimum; federal review of and objection to draft permits; withdrawal or reversion of authority.",
              principal="The agency director or bureau chief who signs permits; the permit appeal board.",
              venue="State environmental hearing or permit appeal boards; state courts; federal objection and "
                    "programme oversight.",
              note="SL review: the state permit writer is the modal state regulatory job (PA NPDES permit writer; MI "
                   "EGLE permit analysts; TX Environmental Protection Specialist III) [E: SL-079, SL-076, SL-050]. "
                   "Florida's assumed 404 programme reverted to the Corps in 2026, showing that delegated authority "
                   "is contingent [E: SC-021].",
              instruments=["florida-404-assumption", "wotus-definition"], sl_reviewed=True, evidence="E",
              sources=["SL-079", "SL-076", "SL-050", "SC-021", "V2-07"]),
            E("seed:ena-sl-c02-federal-regulator", "Federal permitting authority", "federal-regulator",
              position="regulator",
              basis="Federal permit programmes where no state is authorized, and federal programmes never delegated "
                    "(such as the Corps dredge-and-fill programme outside assumed states); federal objection authority "
                    "over state-issued permits in delegated programmes.",
              principal="The regional administrator or district engineer who signs the permit.",
              venue="Federal administrative appeals boards; federal courts.",
              note="Same permit-writing performance; the authority basis is federal and the oversight relationship runs "
                   "the other way (mirror of the state delegated enactment of SC-C14) [J].",
              instruments=["wotus-definition", "ghg-endangerment-rescission"], evidence="E", sources=["V2-06", "V2-07"]),
            E("seed:ena-sl-c02-local-regulator", "Local air district or local permitting authority", "special-district",
              position="regulator",
              basis="State delegation of permitting to air districts, county environmental departments or municipal "
                    "pretreatment programmes.",
              principal="The district governing board or air pollution control officer.",
              venue="District hearing boards; state courts.",
              note="SL review: local districts issue and enforce permits under state law; the board is a direct "
                   "political principal, unlike a state bureau [J].", sl_reviewed=True),
            E("seed:ena-sl-c02-federal-resource-manager", "Federal land manager issuing resource-use authorizations",
              "federal-land-manager", position="resource-manager",
              basis="Land-management statutes and regulations authorizing special uses, grazing, mineral and "
                    "right-of-way authorizations, decided within the governing land management plan.",
              principal="The authorized officer (district ranger, field manager or superintendent).",
              venue="Administrative appeals or objection processes; federal courts.",
              note="Resource-manager variant: the authority decides over a resource it holds rather than over another "
                   "party's emissions; terms, fees and monitoring conditions replace effluent or emission limits [J].",
              instruments=["usfs-objection-rule"], addTasks=["seed:sc-issue-resource-use-authorization"]),
            E("seed:ena-sl-c02-state-resource-manager", "State land or trust-land authorizations", "state-agency",
              position="resource-manager",
              basis="State land board, trust-land or state forest statutes authorizing leases, easements and use "
                    "permits on state-held land and water.",
              principal="The state land board or commissioner.", venue="State courts.",
              note="SL review: trust-land managers also carry a fiduciary duty to trust beneficiaries, which changes how "
                   "fees and terms are justified [J].",
              addTasks=["seed:sc-issue-resource-use-authorization"], sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ SC-C01
    {
        "id": "seed:SC-C01",
        "label": "Map the decision authority and procedural pathway for a proposed action",
        "alt": ["permitting pathway planning", "regulatory strategy", "permit strategy", "authority mapping"],
        "definition": "The capability to identify every institution with authority over a proposed action and the "
                      "governing procedure for each decision, and to sequence those decisions into a pathway a team can "
                      "follow. Shared by regulators advising applicants and by applicants, sponsors and their "
                      "consultants. Excludes deciding the authorizations themselves.",
        "statement": "Identifies every institution with authority over a proposed action, the legal basis and procedure "
                     "version that govern each decision, which decisions are sequential or concurrent, the consultation "
                     "triggers and the critical path, and produces an authority map and pathway plan the project team, "
                     "applicant or agency can act on.",
        "span": ("L1", "L4"),
        "derived": [("v1:6.1.3", "split-from")],
        "sources": ["SC-011", "SC-014", "SC-021", "SC-039", "SC-040", "V2-01"],
        "editorial": "WP-05 (A5 SC). Survivor: absorbs PS-C11 and the applicant-side half of v1 6.1.3. Shared core of "
                     "regulator and applicant work (mirror roles) [J]. With government-wide NEPA regulations removed and "
                     "delegations able to revert, knowing which authority and which procedure version applies is now a "
                     "core skill [E: V2-01, SC-021]. Indicators adapted from SC-A-C01-1..4.",
        "sensitivity": [
            ("DM-05", "Multi-agency roles and one-document rules set the sequence of decisions.", "E", ["V2-01"]),
            ("DM-11", "Delegated programme holders can change when authority reverts.", "E", ["SC-021"]),
            ("DM-09", "Jurisdictional scope decides which authorizations are triggered.", "E", ["V2-07"]),
            ("DM-02", "Deadlines and acceleration options change the critical path.", "E", ["V2-04"]),
        ],
        "tasks": [
            T("seed:v1-6.1.3-T1", "Guide an applicant or project team through the authorizations a proposed action needs, "
              "explaining the sequence, information requirements and decision-maker for each",
              "WF-AUTHORIZE", modes=["MODE-ENGAGE"], rel=["client"], derived=[("v1:6.1.3:T1", "rewritten")]),
            T("seed:v1-6.1.3-T2", "Review a project proposal to identify every authorization, consultation and review it "
              "triggers, recording the governing procedure version for each",
              "WF-AUTHORIZE", formation="yes", derived=[("v1:6.1.3:T2", "rewritten")]),
            T("seed:v1-6.1.3-T3", "Track the status of each authorization for a project against the pathway plan, "
              "notifying the project team when a delay moves the critical path",
              "WF-AUTHORIZE", formation="no", derived=[("v1:6.1.3:T3", "rewritten")]),
            T("seed:sc-prepare-authority-map", "Prepare an authority map and pathway plan for a multi-permit project, "
              "sequencing concurrent and dependent decisions and identifying the critical path",
              "WF-AUTHORIZE", formation="yes", profiles=["WP-PROJECT"]),
            T("seed:sc-replan-pathway", "Update a pathway plan when a governing procedure, delegation status or "
              "jurisdictional rule changes during a project, stating the schedule and cost effects",
              "WF-AUTHORIZE", formation="yes", profiles=["WP-PROJECT"]),
        ],
        "levels": {
            "L1": [
                I("Lists the main authorizations a defined project is likely to need from reference lists, naming the "
                  "governing procedure and its date for each and flagging items it cannot confirm.", WS + KT,
                  tasks=["seed:v1-6.1.3-T2"], evidence=["authority checklist"]),
                I("Updates a project's permit-status tracker from agency correspondence so that every entry matches its "
                  "source document in audit.", RA, tasks=["seed:v1-6.1.3-T3"], evidence=["status tracker"]),
            ],
            "L2": [
                I("Produces a sequenced authority map for a multi-permit project, separating concurrent from dependent "
                  "decisions and naming the critical path and consultation triggers.", WS + PORT, attr="ATT-AUT",
                  tasks=["seed:sc-prepare-authority-map"], evidence=["authority map", "pathway plan"]),
                I("Briefs an applicant on each authorization's information requirements and decision-maker, recording "
                  "the commitments and due dates agreed.", SIM + RA, attr="ATT-SCO", tasks=["seed:v1-6.1.3-T1"],
                  evidence=["meeting record"]),
            ],
            "L3": [
                I("Re-plans a project pathway when a procedure, delegation status or jurisdictional rule changes "
                  "mid-review, keeping completed steps and recording the options considered.", BARS + WS,
                  attr="ATT-CPX", tasks=["seed:sc-replan-pathway"], evidence=["revised pathway plan"]),
                I("Resolves an overlapping-jurisdiction question for leadership with a written analysis of each agency's "
                  "authority and the risks of each sequencing option.", WS + BARS, attr="ATT-GUI",
                  tasks=["seed:sc-prepare-authority-map"], evidence=["analysis memo"]),
            ],
            "L4": [
                I("Designs pathway templates and screening logic that a program's project teams use to identify "
                  "authorizations, with a procedure-version log kept for each.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-prepare-authority-map"], evidence=["templates", "version log"]),
                I("Negotiates a standing arrangement with other agencies that settles a recurring authority question for a "
                  "class of projects, recording the agreed division in writing.", PORT, attr="ATT-SCO",
                  tasks=["seed:sc-replan-pathway"], evidence=["standing agreement"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c01-regulated-party", "Applicant or project sponsor pathway strategy", "firm",
              position="regulated-party",
              basis="No decision authority; obligations as applicant under each authorizing programme; options such as "
                    "sponsor-paid accelerated review and covered-project status.",
              principal="Executives, project finance and the project owner.",
              venue="Agency decisions and permit appeals; project lenders and investors.",
              note="Mirror of SL-C02 (the deciding authority): the same authority map, built to secure rather than "
                   "decide authorizations [J; PS-C11 absorbed].",
              instruments=["nepa-s112-fee", "fast-41"], evidence="E", sources=["V2-04"]),
            E("seed:ena-sc-c01-agency", "Agency pre-application and project coordination", "state-agency",
              position="regulator",
              basis="The agency's own authorities plus its role in multi-agency coordination; pre-application "
                    "assistance programmes.",
              principal="The agency's permitting director.", venue="State courts; agency appeal bodies.",
              note="SL review: state permit coordinators map pathways for applicants across state, federal and local "
                   "authorizations; delegated-programme holders must be confirmed for each permit type [J].",
              instruments=["florida-404-assumption"], sl_reviewed=True),
            E("seed:ena-sc-c01-consultant", "Consultant permitting strategist", "firm", position="service-provider",
              basis="Contract with the sponsor; professional obligations to the client and to accurate submissions.",
              principal="The client.", venue="Agency decisions; contract remedies; professional ethics rules.",
              note="Delivers the regulated-party enactment for a client; independence and disclosure duties apply "
                   "(PS-C18) [J]."),
        ],
    },
    # ------------------------------------------------------------------ SC-C14
    {
        "id": "seed:SC-C14",
        "label": "Operate within, or oversee, delegated and assumed regulatory programs",
        "alt": ["primacy program administration", "delegated program management", "state program authorization",
                "oversight of local program delivery"],
        "definition": "The capability to run a regulatory program under authority delegated, approved or assumed from "
                      "another level of government, or to oversee such a program, including the conditions on which "
                      "the authority rests and the plan for its withdrawal or reversion. Covers state-to-local "
                      "delegation and federal oversight of state programs.",
        "statement": "Administers a state or local program that holds delegated, primacy or assumed authority, or "
                     "oversees one: meets and documents the conditions on which the authority rests, manages the "
                     "oversight relationship and its reporting, keeps program rules at least as stringent as the "
                     "authority requires, and plans for withdrawal or reversion of authority.",
        "span": ("L2", "L5"),
        "derived": [("v1:6.5.2", "split-from")],
        "sources": ["SC-021", "SC-023", "SL-071", "SL-072", "SL-079", "SL-085", "SL-088"],
        "editorial": "WP-05 (A5 SC; SL reviewed). Survivor: absorbs SL-C01 (administer a delegated or primacy program) "
                     "and SL-C11 (oversee local or delegated delivery) and the delegation part of v1 6.5.2. Actor-specific "
                     "competency authorized by ADR-0007 B.5(3) because the authority is contingent on another "
                     "government's predicates and can revert [E: SC-021]. v1 text never named primacy or delegation "
                     "[E: SL-087]. The Tribal treatment-as-state variant is held content and is not authored here. "
                     "Level span reaches L5; L5 indicators await SME confirmation (proficiency_levels L5 note).",
        "sensitivity": [
            ("DM-11", "Delegation, assumption and primacy are fragile and can revert after litigation.", "E", ["SC-021"]),
            ("DM-09", "Narrower federal jurisdiction pushes states toward their own programmes.", "E", ["V2-07"]),
            ("DM-19", "Federal programme grants that fund delegated programmes are set annually.", "J", None),
        ],
        "tasks": [
            T("seed:sc-prepare-delegated-workplan", "Prepare a delegated program's annual work plan and performance report "
              "for the overseeing agency, documenting each commitment met, missed or renegotiated",
              "WF-AUTHORIZE.delegated", formation="partial", profiles=["WP-REGPROGRAM"]),
            T("seed:sc-assess-rule-stringency", "Assess whether a proposed change to program rules keeps them at least as "
              "stringent as the delegated authority requires, documenting each provision compared",
              "WF-AUTHORIZE.delegated", formation="yes", profiles=["WP-REGPROGRAM"]),
            T("seed:sc-audit-local-delivery", "Audit a local government's delivery of a delegated program against its "
              "agreement, issuing findings with the corrective actions required",
              "WF-AUTHORIZE.delegated", field="on-site-preferred", formation="yes", rel=["intergovernmental"],
              profiles=["WP-REGPROGRAM"]),
            T("seed:sc-answer-oversight-objection", "Respond to an overseeing agency's objection to a permit issued under "
              "delegated authority, revising the permit or defending it with a written record",
              "WF-AUTHORIZE.delegated", modes=["MODE-RESOLVE"], rel=["intergovernmental"], formation="yes"),
            T("seed:sc-plan-authority-reversion", "Prepare a contingency plan for withdrawal or reversion of delegated "
              "authority, identifying the pending actions, records and staff that would transfer",
              "WF-AUTHORIZE.delegated", formation="partial"),
        ],
        "levels": {
            "L2": [
                I("Prepares a delegated program's work plan and performance report with each commitment traced to "
                  "program records that pass the overseeing agency's review.", RA + WS,
                  tasks=["seed:sc-prepare-delegated-workplan"], evidence=["work plan", "performance report"]),
                I("Compares a proposed program rule with the corresponding minimum provision by provision, documenting "
                  "any provision that would be less stringent.", WS, tasks=["seed:sc-assess-rule-stringency"],
                  evidence=["comparison table"]),
            ],
            "L3": [
                I("Responds to an overseeing agency's objection to a permit with a written analysis that resolves the "
                  "objection or defends the permit on the record.", WS + MOOT, attr="ATT-SCO",
                  tasks=["seed:sc-answer-oversight-objection"], evidence=["response memo"]),
                I("Audits a local government's delivery of a delegated program against the agreement, issuing findings "
                  "that cite the evidence for each corrective action.", RA + WS, attr="ATT-SCO",
                  tasks=["seed:sc-audit-local-delivery"], evidence=["audit report"]),
            ],
            "L4": [
                I("Designs a contingency plan for withdrawal or reversion of the program's authority, listing pending "
                  "actions, records and staff with the transfer steps for each.", PORT, attr="ATT-CPX",
                  tasks=["seed:sc-plan-authority-reversion"], evidence=["contingency plan"]),
                I("Negotiates the terms of a delegation or performance agreement with the overseeing agency, recording "
                  "each obligation, metric and dispute-resolution step agreed.", SIM + PORT, attr="ATT-SCO",
                  tasks=["seed:sc-prepare-delegated-workplan"], evidence=["agreement"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c14-state-delegated", "State agency administering a delegated or primacy program",
              "state-agency", position="regulator",
              basis="Federal approval, delegation or assumption of a state program (water discharge, air operating "
                    "permit, hazardous waste, drinking water primacy, assumed dredge-and-fill). Delegated constraints: "
                    "equivalence or minimum-stringency requirements, federal review of program changes and permits, "
                    "reporting and work-plan commitments tied to programme grants, withdrawal procedures.",
              principal="The state agency head; the federal regional office as overseer.",
              venue="Federal programme review and withdrawal proceedings; federal courts (the Florida assumption was "
                    "vacated in 2026); state courts for state-law actions.",
              note="SL review: most state environmental work is delegated or primacy programme delivery (MI EGLE lead "
                   "and copper compliance; PA NPDES; TX programmes) [E: SL-071, SL-079, SL-050].",
              instruments=["florida-404-assumption", "wotus-definition"], sl_reviewed=True, evidence="E",
              sources=["SC-021", "SL-071", "SL-079", "V2-07"]),
            E("seed:ena-sc-c14-federal-overseer", "Federal regional office overseeing state programs", "federal-regulator",
              position="regulator",
              basis="Federal authority to approve, review, object to and withdraw state programs; programme grant "
                    "conditions.",
              principal="The regional administrator.", venue="Federal courts; Congress.",
              note="Mirror of the state delegated enactment: the same program conditions, monitored from the overseeing "
                   "side [J]."),
            E("seed:ena-sc-c14-state-overseer-local", "State agency overseeing local or delegated delivery", "state-agency",
              position="regulator",
              basis="State statutes delegating programme delivery to counties, cities, conservation districts or local "
                    "health departments, with state technical authority over local staff.",
              principal="The state program manager.", venue="State courts; state funding conditions.",
              note="SL review: Wisconsin DATCP specialists hold technical authority over county land conservation staff; "
                   "state staff audit and build local capacity rather than issue the permits themselves "
                   "[E: SL-085].", sl_reviewed=True, evidence="E", sources=["SL-085"]),
            E("seed:ena-sc-c14-local-delegate", "Local government delivering a delegated program", "county",
              position="regulator",
              basis="State delegation agreement or statute assigning programme delivery to the local government.",
              principal="The local health officer, district board or county board.",
              venue="State oversight audits; state courts.",
              note="SL review: the local delegate carries the same dual relationship as a state primacy agency, one "
                   "level down [J].", sl_reviewed=True),
        ],
    },
    # ------------------------------------------------------------------ v1 5.5.2
    {
        "id": "seed:v1-5.5.2",
        "label": "Process permit applications and administer issued authorizations",
        "alt": ["permit administration", "permit desk", "recreation and research permits"],
        "definition": "The capability to process routine permit and authorization applications within delegated limits, "
                      "explain conditions to holders, keep permit records accurate and track holders' compliance with "
                      "reporting and permit terms. The entry point that feeds authorization work; excludes deciding "
                      "non-routine permits.",
        "statement": "Receives and screens applications for routine permits and authorizations such as recreation, "
                     "research, special-use or registration permits, issues standard authorizations within delegated "
                     "limits, explains conditions to permit holders, keeps permit records and electronic case files "
                     "accurate, and tracks holders' compliance with reporting and permit terms.",
        "span": ("L1", "L3"),
        "derived": [],
        "sources": ["SC-037", "V2-08"],
        "editorial": "WP-05 (A5 SC). v1 5.5.2 rewrite: kept as the digital-permitting operations entry point that feeds "
                     "authorization work (SL-C02) [J]. Electronic permitting moves routine checks to automated "
                     "eligibility screening; the review of misclassified applications stays human [E: SC-037, V2-08].",
        "sensitivity": [
            ("DM-14", "Electronic permitting and automated completeness checks change the entry task bundle.", "E", ["V2-08", "SC-037"]),
            ("DM-15", "Permit fees and cost recovery are set by the programme.", "J", None),
        ],
        "tasks": [
            T("seed:v1-5.5.2-T1", "Process applications for routine recreation, research or resource-use permits, issuing "
              "standard authorizations within the limits delegated to the position",
              "WF-AUTHORIZE", formation="partial", derived=[("v1:5.5.2:T1", "rewritten")]),
            T("seed:v1-5.5.2-T2", "Explain permit conditions and environmental responsibilities to permit holders before use "
              "begins, recording each holder's acknowledgment of the conditions",
              "WF-AUTHORIZE", modes=["MODE-ENGAGE"], rel=["public"], field="on-site-preferred",
              derived=[("v1:5.5.2:T2", "rewritten")]),
            T("seed:v1-5.5.2-T3", "Maintain permit records and electronic case files, tracking holders' reporting and expiry "
              "dates and referring missed conditions for follow-up",
              "WF-AUTHORIZE", formation="no", derived=[("v1:5.5.2:T3", "rewritten")]),
            T("seed:sc-review-automated-permit-checks", "Review automated eligibility and completeness checks on electronic "
              "permit applications, correcting misclassified applications before decisions are issued",
              "WF-AUTHORIZE", formation="partial",
              note="Review counterpart of routine processing where electronic permitting automates checks (G-2)."),
        ],
        "levels": {
            "L1": [
                I("Issues standard permits from the program's decision table so that every permit sampled in audit "
                  "matches the table and the application record.", RA, tasks=["seed:v1-5.5.2-T1"],
                  evidence=["issued permits", "audit sample"]),
                I("Explains a permit's conditions to a holder at issuance using the program's condition summary, recording "
                  "the holder's acknowledgment in the case file.", TB + RA, tasks=["seed:v1-5.5.2-T2"],
                  evidence=["acknowledgment records"]),
                I("Maintains electronic case files so that reporting and expiry dates sampled in audit match the issued "
                  "permit terms.", RA, tasks=["seed:v1-5.5.2-T3"], evidence=["case files"]),
            ],
            "L2": [
                I("Resolves non-standard applications within delegated limits, documenting the reason for each condition "
                  "added or request referred to the authorizing officer.", RA + WS, attr="ATT-AUT",
                  tasks=["seed:v1-5.5.2-T1"], evidence=["case files"]),
                I("Corrects misclassified applications found by automated completeness checks after verifying each "
                  "against the application, recording the basis before the decision issues.", SEW, attr="ATT-AUG",
                  mode="assisted", tasks=["seed:sc-review-automated-permit-checks"], evidence=["correction log"]),
            ],
            "L3": [
                I("Revises the program's decision table and condition library when rules or recurring compliance problems "
                  "change, with a change log reviewers can audit.", PORT + RA, attr="ATT-GUI",
                  tasks=["seed:v1-5.5.2-T1"], evidence=["decision table", "change log"]),
                I("Evaluates new permit staff's case files against the program checklist before granting them issuing "
                  "authority for non-standard applications.", RA + TB, attr="ATT-FOR",
                  tasks=["seed:v1-5.5.2-T3"], evidence=["evaluation record"]),
            ],
        },
        "enactments": [],
    },
]
