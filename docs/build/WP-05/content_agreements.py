"""WP-05 content: agreements cluster (SC-C08, v1 3.1.4 absorbing 3.3.4). Agreements with Tribal governments route
through TN-C04 (held) and are not authored here."""
from wp05dsl import T, I, E

WS = ["work-sample"]
RA = ["record-audit"]
SEW = ["seeded-error-work-sample"]
BARS = ["structured-interview-bars"]
SIM = ["simulation-role-play"]
PORT = ["portfolio-review"]
KT = ["knowledge-test"]

COMPETENCIES = [
    # ------------------------------------------------------------------ SC-C08
    {
        "id": "seed:SC-C08",
        "label": "Design and administer cross-jurisdictional stewardship agreements",
        "alt": ["Good Neighbor Agreement administration", "shared stewardship agreements", "stewardship agreements",
                "interagency agreements", "memoranda of understanding"],
        "definition": "The capability to design and run master and project agreements under which agencies, other "
                      "governments and nonprofit partners share stewardship work across jurisdictional boundaries, "
                      "within legal limits on delegating governmental functions, and to keep them working through "
                      "turnover. Excludes contract and grant administration in general.",
        "statement": "Designs and runs master and project agreements under which agencies, other governments and nonprofit "
                     "partners share stewardship work: scopes work within legal limits on delegating inherently "
                     "governmental functions, sets roles, reporting, revenue retention and reinvestment, and keeps "
                     "agreements working through staff turnover and changes of administration.",
        "span": ("L1", "L5"),
        "derived": [("v1:6.5.3", "merged-from"), ("v1:6.5.4", "merged-from")],
        "sources": ["SC-030", "SC-031", "SC-032", "SC-034"],
        "editorial": "WP-05 (A5 SC). Survivor: absorbs FS-C14 and CC-CM-03 and v1 6.5.3 and 6.5.4 (merged). Agreement "
                     "authority is expanding: 540 agreements in FY2025 (426 with states, 50 with counties), county "
                     "revenue retention through FY2028, recreation agreements new, a state statute extending state "
                     "authority, and a bill for 20-year agreements [E: SC-030, SC-031, SC-034, SC-032]. Agreements with "
                     "Tribal governments (and co-stewardship content) route through TN-C04 under the hold. Indicators "
                     "adapted from SC-A-C08-1..4. L5 indicators await SME confirmation.",
        "sensitivity": [
            ("DM-12", "Shared implementation agreement authorities are expanding.", "E", ["SC-030", "SC-034"]),
            ("DM-15", "Revenue retention and reinvestment change agreement finance.", "E", ["SC-030"]),
        ],
        "tasks": [
            T("seed:v1-6.5.3-T1", "Draft a memorandum of understanding or interagency agreement that assigns shared "
              "responsibilities, resources and decision rights for a joint program",
              "WF-RESOURCE", profiles=["WP-AGREEMENT"], rel=["intergovernmental"], derived=[("v1:6.5.3:T1", "rewritten")]),
            T("seed:v1-6.5.3-T2", "Define each partner's roles, resource commitments and reporting protocols in a project "
              "agreement within the parties' legal authorities",
              "WF-RESOURCE", profiles=["WP-AGREEMENT"], rel=["intergovernmental"], derived=[("v1:6.5.3:T2", "rewritten")]),
            T("seed:v1-6.5.3-T3", "Monitor an agreement's deliverables, invoices and revenue ledger against its terms, "
              "amending the agreement when scope or partners change",
              "WF-RESOURCE", profiles=["WP-AGREEMENT"], formation="no", derived=[("v1:6.5.3:T3", "rewritten")]),
            T("seed:v1-6.5.4-T1", "Lead a planning process spanning watershed or ecosystem boundaries, producing a shared "
              "work plan that each participating jurisdiction formally adopts",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["intergovernmental"], profiles=["WP-AGREEMENT"], formation="yes",
              derived=[("v1:6.5.4:T1", "rewritten")]),
            T("seed:v1-6.5.4-T2", "Reconcile conflicting regulatory requirements and priorities across jurisdictions for a "
              "shared landscape project, documenting the approach each party accepts",
              "WF-PLAN", modes=["MODE-RESOLVE"], rel=["intergovernmental"], formation="yes",
              derived=[("v1:6.5.4:T2", "rewritten")]),
            T("seed:v1-6.5.4-T3", "Facilitate engagement among several jurisdictions and interested parties for a shared "
              "stewardship program, recording the commitments each makes",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["intergovernmental", "stakeholder"],
              derived=[("v1:6.5.4:T3", "rewritten")]),
            T("seed:sc-scope-inherent-functions", "Scope partner work under a stewardship agreement so that no inherently "
              "governmental function is delegated, documenting the legal review of each work item",
              "WF-RESOURCE", profiles=["WP-AGREEMENT"], formation="partial"),
        ],
        "levels": {
            "L1": [
                I("Prepares project agreement documents from approved templates with no clause omitted or altered "
                  "without approval in legal review.", RA, tasks=["seed:v1-6.5.3-T1"], evidence=["agreement draft"]),
                I("Reconciles an agreement's deliverables, invoices and retained-revenue ledger against its terms each "
                  "period, reporting each discrepancy to the agreement manager.", RA + WS,
                  tasks=["seed:v1-6.5.3-T3"], evidence=["ledger reconciliation"]),
            ],
            "L2": [
                I("Drafts a project agreement within the parties' authorities, setting roles, reporting and revenue "
                  "reinvestment terms that pass legal review without substantive rework.", WS + RA, attr="ATT-AUT",
                  tasks=["seed:v1-6.5.3-T2"], evidence=["executed agreement", "legal review"]),
                I("Documents for each partner work item why it is not an inherently governmental function, with "
                  "legal-review sign-off before the agreement is executed.", RA, attr="ATT-KNO",
                  tasks=["seed:sc-scope-inherent-functions"], evidence=["work-item review"]),
            ],
            "L3": [
                I("Designs a master agreement for a multi-partner program with dispute-resolution and turnover "
                  "provisions that every partner accepts in writing.", PORT + BARS, attr="ATT-CPX",
                  tasks=["seed:v1-6.5.3-T1"], evidence=["master agreement"]),
                I("Resolves a partner dispute under an agreement through its agreed process, recording the issue, the "
                  "options considered and the resolution adopted.", SIM + RA, attr="ATT-SCO",
                  tasks=["seed:v1-6.5.4-T2"], evidence=["dispute record"]),
            ],
            "L4": [
                I("Drafts enabling policy or model legislation for an agreement program, with a review of the authorities "
                  "and limits it relies on.", PORT, attr="ATT-GUI", tasks=["seed:v1-6.5.3-T1"],
                  evidence=["draft policy or bill"]),
                I("Evaluates a portfolio of agreements each year against program outcomes and audit findings, "
                  "recommending which to renew, amend or close.", PORT + RA, attr="ATT-SCO",
                  tasks=["seed:v1-6.5.3-T3"], evidence=["portfolio evaluation"]),
            ],
        },
        "enactments": [
            E("seed:ena-sc-c08-federal", "Federal land agency agreement manager", "federal-land-manager",
              position="resource-manager",
              basis="Good Neighbor Authority (with the 2025 amendments on revenue retention and recreation agreements), "
                    "stewardship agreement and cooperative agreement authorities; limits on delegating inherently "
                    "governmental functions.",
              principal="The forest supervisor or state director and the agreements officer.",
              venue="Agreement audits; inspectors general; Congress.",
              note="Federal staff increasingly manage agreements rather than deliver work directly [E: SC-030].",
              instruments=["good-neighbor-authority", "long-term-gna-act", "fix-our-forests-act"], evidence="E",
              sources=["SC-030", "SC-031", "SC-032"]),
            E("seed:ena-sc-c08-state", "State forestry or resource agency as agreement partner", "state-agency",
              basis="State statutes authorizing the agency to perform work on federal lands and retain or reinvest "
                    "receipts (for example Colorado's 2026 statute extending state authority to Interior agencies).",
              principal="The state forester or agency head.", venue="State audits; state legislature.",
              note="SL review: state partners need agreement, procurement and revenue-ledger skills that their class "
                   "specifications rarely name [J; E: SC-034 for the statute].",
              instruments=["co-hb26-1205", "good-neighbor-authority"], sl_reviewed=True, evidence="E",
              sources=["SC-034"]),
            E("seed:ena-sc-c08-county", "County agreement partner retaining revenue", "county",
              basis="Agreement authority extended to counties with revenue retention through FY2028.",
              principal="The county board.", venue="County audits; federal agreement oversight.",
              note="SL review: counties became partners with fiscal duties (ledgers, reinvestment) and need staff who "
                   "can run them [E: SC-030].", instruments=["good-neighbor-authority"], sl_reviewed=True,
              evidence="E", sources=["SC-030"]),
            E("seed:ena-sc-c08-ngo", "Nonprofit stewardship partner", "watershed-group",
              basis="Cooperative and stewardship agreements with agencies; grant terms.",
              principal="The board and funders; the agency agreement officer.",
              venue="Agreement audits; funder reporting.",
              note="Nonprofit partners deliver work and convene partners but cannot exercise governmental functions "
                   "delegated by the agreement [J]."),
        ],
    },
    # ------------------------------------------------------------------ v1 3.1.4
    {
        "id": "seed:v1-3.1.4",
        "label": "Administer contracts, grants and intergovernmental agreements",
        "alt": ["contract and agreement administration", "contracting officer's representative", "grants management",
                "cooperative agreement administration", "procurement"],
        "definition": "The capability to prepare, monitor, amend and close out contracts, grants, cooperative and "
                      "intergovernmental agreements and routine purchases so that deliverables, payments and changes "
                      "comply with the instrument and the procurement and financial-assistance requirements that apply. "
                      "Agreement design across jurisdictions is a separate competency.",
        "statement": "Prepares scopes of work and agreement documents for contracts, grants, cooperative agreements and "
                     "intergovernmental instruments; selects the instrument type that fits the relationship; monitors "
                     "deliverables, invoices and compliance with terms and cross-cutting requirements; and amends or "
                     "closes out agreements with a complete file.",
        "span": ("L1", "L4"),
        "derived": [("v1:3.3.4", "merged-from")],
        "sources": [],
        "editorial": "WP-05 (A5 SC). v1 3.1.4 rewrite (title defect fixed); absorbs 3.3.4 (procurement). Intergovernmental "
                     "instruments (cooperative agreements, stewardship agreements, personnel assignments, delegation "
                     "agreements, grant work plans) added with SC-C08 for agreement design (SL, IO verdicts). Indicators "
                     "adapted in part from IO exemplar rewrites for v1 3.1.4.",
        "sensitivity": [
            ("DM-15", "Fees and agreement revenue change what agreements must account for.", "J", None),
            ("DM-19", "Programme funding cuts and reinstatements change grant and agreement portfolios.", "J", None),
        ],
        "tasks": [
            T("seed:v1-3.1.4-T1", "Write a scope of work for a contractor or partner that states deliverables, acceptance "
              "criteria, schedule and reporting in verifiable terms",
              "WF-RESOURCE", formation="partial", derived=[("v1:3.1.4:T1", "rewritten")]),
            T("seed:v1-3.1.4-T2", "Track invoices and deliverables against contract or agreement terms, withholding payment "
              "approval for deliverables that fail acceptance criteria",
              "WF-RESOURCE", formation="no", derived=[("v1:3.1.4:T2", "rewritten")]),
            T("seed:v1-3.1.4-T3", "Review a proposed agreement for compliance with procurement, grant and cross-cutting "
              "requirements before signature, listing each deficiency and its correction",
              "WF-RESOURCE", formation="partial", derived=[("v1:3.1.4:T3", "rewritten")]),
            T("seed:sc-select-agreement-instrument", "Select the legal instrument for a proposed relationship, choosing among "
              "contract, grant, cooperative agreement and intergovernmental agreement by purpose and control",
              "WF-RESOURCE", formation="partial"),
            T("seed:v1-3.3.4-T1", "Order supplies, tools and services through the organization's procurement procedures, "
              "documenting the purchasing authority and funding source for each order",
              "WF-RESOURCE", formation="no", strength="contributing", derived=[("v1:3.3.4:T1", "rewritten")]),
            T("seed:v1-3.3.4-T2", "Reconcile purchase orders and invoices against deliveries received, referring each "
              "discrepancy to the finance office before payment",
              "WF-RESOURCE", formation="no", strength="contributing", derived=[("v1:3.3.4:T2", "rewritten")]),
            T("seed:v1-3.3.4-T3", "Confirm with finance and contracting staff that a proposed purchase meets procurement "
              "rules, recording the rule applied and any approval obtained",
              "WF-RESOURCE", formation="no", strength="contributing", derived=[("v1:3.3.4:T3", "rewritten")]),
        ],
        "levels": {
            "L1": [
                I("Maintains the official file for an assigned contract or agreement so that every deliverable, invoice, "
                  "modification and communication is recorded and retrievable for audit.", RA,
                  tasks=["seed:v1-3.1.4-T2"], evidence=["agreement file"]),
                I("Checks invoices against the instrument's payment terms and accepted deliverables, routing each "
                  "discrepancy to the responsible official before approval.", SEW, mode="assisted",
                  tasks=["seed:v1-3.1.4-T2", "seed:v1-3.3.4-T2"], evidence=["invoice review log"]),
            ],
            "L2": [
                I("Drafts a statement of work with measurable deliverables, acceptance criteria and schedule that a "
                  "contracting or grants officer accepts without substantive revision.", WS, attr="ATT-AUT",
                  tasks=["seed:v1-3.1.4-T1"], evidence=["statement of work"]),
                I("Selects the instrument type for a proposed relationship, documenting the purpose and degree-of-control "
                  "reasons for the choice.", WS + KT, attr="ATT-KNO", tasks=["seed:sc-select-agreement-instrument"],
                  evidence=["instrument memo"]),
            ],
            "L3": [
                I("Resolves a non-routine agreement issue such as a scope change or performance dispute by preparing the "
                  "modification or corrective-action record and its justification for the authorized official.",
                  SIM + BARS, attr="ATT-CPX", tasks=["seed:v1-3.1.4-T3"], evidence=["modification record"]),
                I("Amends an agreement when scope, partners or funding change, documenting the legal authority and "
                  "approvals for each amendment.", RA, attr="ATT-GUI", tasks=["seed:v1-3.1.4-T3"],
                  evidence=["amendment file"]),
            ],
            "L4": [
                I("Sets agreement templates and review checklists for a program's recurring instrument types, with the "
                  "contracting or legal office's confirmation that they meet the applicable requirements.", PORT,
                  attr="ATT-GUI", jv=True, tasks=["seed:v1-3.1.4-T1"], evidence=["templates", "review record"]),
                I("Certifies staff to administer agreements above a set value after reviewing their agreement files "
                  "against program standards.", RA + PORT, attr="ATT-FOR", tasks=["seed:v1-3.1.4-T2"],
                  evidence=["certification record"]),
            ],
        },
        "enactments": [
            E("seed:ena-v1-3-1-4-federal", "Federal acquisition and financial assistance", "federal-agency",
              basis="Federal acquisition regulations, the uniform grants guidance and the statute distinguishing "
                    "contracts, grants and cooperative agreements; personnel-assignment authority for intergovernmental "
                    "staff exchanges.",
              principal="The contracting or grants officer, with the program representative.",
              venue="Bid protests; audits; inspectors general.",
              note="Contracting officer's representative duties carry a certification gate (Credential, not a level) "
                   "[J]; the governing regulations are L5 instruments to register (worklog)."),
            E("seed:ena-v1-3-1-4-state-local", "State and local procurement and grants", "state-agency",
              basis="State procurement codes, state grant rules and intergovernmental cooperation acts.",
              principal="The state purchasing office or the local governing body.",
              venue="State procurement protests; state audits.",
              note="SL review: state and local purchasing thresholds and competition rules differ widely; the "
                   "administration skill transfers, the thresholds do not [J].", sl_reviewed=True),
        ],
    },
]
