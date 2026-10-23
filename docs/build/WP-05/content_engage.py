"""WP-05 content: relational and engagement core (v1 5.2.1-5.2.5; SC-primary in v1; used by COR-3 P1 roles R09, R10,
R13). Engagement with governments as sovereigns is a distinct relationship (government-to-government) and is held
content: these records stay actor-neutral, and Tribal-actor enactments requested by TN are not authored here."""
from wp05dsl import T, I, E

WS = ["work-sample"]
RA = ["record-audit"]
SEW = ["seeded-error-work-sample"]
BARS = ["structured-interview-bars"]
SIM = ["simulation-role-play"]
PORT = ["portfolio-review"]
KT = ["knowledge-test"]
TB = ["task-book-observation"]
C360 = ["counterpart-360"]

COMPETENCIES = [
    # ------------------------------------------------------------------ v1 5.2.1 (absorbs 3.6.3)
    {
        "id": "seed:v1-5.2.1",
        "label": "Identify and analyze the parties affected by or interested in a decision",
        "alt": ["stakeholder identification and analysis", "stakeholder mapping", "stakeholder engagement for sustainability"],
        "definition": "The capability to identify the people, organizations and governments a decision affects or "
                      "interests, analyze their interests, concerns, influence and legal standing, and use the analysis to "
                      "shape engagement. Covers corporate stakeholder analysis (investors, suppliers, communities).",
        "statement": "Identifies the people, organizations and governments affected by or interested in a decision, "
                     "analyzes their interests, concerns, influence and legal standing, separates parties owed formal "
                     "consultation from interested parties, and uses the analysis to shape the engagement approach and keep "
                     "it current as the decision develops.",
        "span": ("L1", "L4"),
        "derived": [("v1:3.6.3", "merged-from")],
        "sources": [],
        "editorial": "WP-05 (A5 SC). v1 5.2.1 rewrite; absorbs 3.6.3 (corporate stakeholder engagement, merged). The "
                     "IO/TN-requested indicator distinguishing sovereign governments (consulted government to government, "
                     "TN-C02, held) from stakeholders is written actor-neutrally at L2 (parties owed formal consultation "
                     "versus interested parties); the Tribal-specific framing stays with TN under the hold. Digital "
                     "platforms and sentiment tools from v1 3.6.3 move to L4.",
        "sensitivity": [
            ("DM-04", "Participation requirements decide which parties must be engaged and how.", "E", ["SC-038"]),
        ],
        "tasks": [
            T("seed:v1-5.2.1-T1", "Map the parties affected by or interested in a decision, recording each party's "
              "interests, concerns and influence on the decision",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["stakeholder", "public"], formation="partial",
              derived=[("v1:5.2.1:T1", "rewritten")]),
            T("seed:v1-5.2.1-T2", "Gather affected parties' perspectives on a proposed decision through interviews or "
              "surveys, recording responses against the questions asked",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["stakeholder", "public"], field="on-site-preferred",
              formation="partial", derived=[("v1:5.2.1:T2", "rewritten")]),
            T("seed:v1-5.2.1-T3", "Select engagement methods for each party group from the analysis, stating why each method "
              "fits that group's interests and capacity",
              "WF-PLAN", modes=["MODE-ENGAGE"], formation="partial", derived=[("v1:5.2.1:T3", "rewritten")]),
            T("seed:sc-separate-consultation-parties", "Separate parties owed formal consultation by law or agreement from "
              "interested parties, routing each party to the process that applies to it",
              "WF-PLAN", modes=["MODE-ENGAGE"], formation="yes"),
            T("seed:v1-3.6.3-T1", "Reach dispersed or hard-to-reach parties through online and in-person channels, recording "
              "which groups each channel reached and which it missed",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["public", "stakeholder"], formation="no",
              derived=[("v1:3.6.3:T1", "rewritten")]),
            T("seed:v1-3.6.3-T2", "Review automated theme or sentiment analysis of party input against a sample of the "
              "original submissions, correcting each misread priority",
              "WF-PLAN", modes=["MODE-ENGAGE"], formation="partial", derived=[("v1:3.6.3:T2", "rewritten")]),
            T("seed:v1-3.6.3-T3", "Identify the investors, suppliers and community groups affected by a company's "
              "environmental commitments, recording each group's expectations",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["stakeholder", "client"], formation="partial",
              derived=[("v1:3.6.3:T3", "rewritten")]),
        ],
        "levels": {
            "L1": [
                I("Builds a party map for a defined decision from records and staff knowledge, listing each party's stated "
                  "interests and how the party was identified.", WS, tasks=["seed:v1-5.2.1-T1"], evidence=["party map"]),
                I("Records interview or survey responses against the questions asked so that a reviewer can trace each "
                  "summarized concern to its source.", RA, tasks=["seed:v1-5.2.1-T2"], evidence=["response log"]),
            ],
            "L2": [
                I("Separates parties owed formal consultation by law or agreement from interested parties in the analysis, "
                  "routing each party to the process that applies.", WS + KT, attr="ATT-KNO",
                  tasks=["seed:sc-separate-consultation-parties"], evidence=["party analysis"]),
                I("Selects engagement methods for each party group from the analysis, stating why each method fits that "
                  "group's interests and capacity.", WS, attr="ATT-AUT", tasks=["seed:v1-5.2.1-T3"],
                  evidence=["method table"]),
                I("Checks automated theme or sentiment analysis of party input against a sample of original submissions, "
                  "correcting each misread priority.", SEW, attr="ATT-AUG", mode="assisted",
                  tasks=["seed:v1-3.6.3-T2"], evidence=["sample check log"]),
            ],
            "L3": [
                I("Updates the party analysis when a decision's scope or conflict changes, recording the parties added, "
                  "their concerns and the engagement change made.", RA + WS, attr="ATT-CPX",
                  tasks=["seed:v1-5.2.1-T1"], evidence=["analysis revision log"]),
                I("Finds the parties an initial analysis missed in a contested decision, documenting how they were found "
                  "and how they were then engaged.", BARS + WS, attr="ATT-SCO", tasks=["seed:v1-3.6.3-T1"],
                  evidence=["analysis memo"]),
            ],
            "L4": [
                I("Sets an organization's party-analysis method and template, with the checks analyses must pass before "
                  "engagement plans are approved.", PORT, attr="ATT-GUI", tasks=["seed:v1-5.2.1-T1"],
                  evidence=["method", "template"]),
                I("Reviews staff party analyses against the method, returning each with omitted parties or unsupported "
                  "influence ratings to fix.", RA, attr="ATT-FOR", tasks=["seed:v1-5.2.1-T3"],
                  evidence=["review comments"]),
            ],
        },
        "enactments": [
            E("seed:ena-v1-5-2-1-private", "Corporate stakeholder analysis", "firm", position="regulated-party",
              basis="No public authority; disclosure and supply-chain obligations and voluntary commitments.",
              principal="Executives and the board.", venue="Investors, customers and regulators.",
              note="The v1 3.6.3 corporate note: investors, suppliers and communities are analyzed with the same method "
                   "as public-decision stakeholders [J; PS verdict]."),
        ],
    },
    # ------------------------------------------------------------------ v1 5.2.2 (absorbs facilitation from 2.5.1)
    {
        "id": "seed:v1-5.2.2",
        "label": "Design and facilitate meetings among parties with differing views",
        "alt": ["meeting facilitation and design", "workshop facilitation", "virtual meeting facilitation"],
        "definition": "The capability to design and facilitate meetings, workshops and working sessions among parties "
                      "with differing views, in person or online, and to carry their outcomes into the decision. Meeting "
                      "platforms are L4 tools.",
        "statement": "Designs and facilitates meetings, workshops and working sessions among parties with differing views, "
                     "in person or online: sets purpose, agenda and ground rules, manages participation and group dynamics, "
                     "records outcomes and commitments, and follows up so that the meeting's results carry into the "
                     "decision.",
        "span": ("L1", "L4"),
        "derived": [("v1:2.5.1", "merged-from")],
        "sources": [],
        "editorial": "WP-05 (A5 SC). v1 5.2.2 carried with v2 indicators; absorbs the facilitation remainder of v1 2.5.1 "
                     "(platforms moved to L4; the 2.5.1 tasks were rewritten by WP-04 and already point here).",
        "sensitivity": [
            ("DM-04", "Discretion over participation changes when and how meetings are convened.", "E", ["SC-038"]),
        ],
        "tasks": [
            T("seed:v1-5.2.2-T1", "Plan a public workshop or collaborative planning session, setting its purpose, agenda, "
              "ground rules and participation arrangements for the expected participants",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["public", "stakeholder"], formation="partial",
              derived=[("v1:5.2.2:T1", "rewritten")]),
            T("seed:v1-5.2.2-T2", "Facilitate a working session among parties with differing views, managing participation "
              "so that each group's input is heard and recorded",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["public", "stakeholder"], field="on-site-preferred",
              formation="yes", derived=[("v1:5.2.2:T2", "rewritten")]),
            T("seed:v1-5.2.2-T3", "Document meeting outcomes and commitments, sending participants a summary and tracking "
              "each commitment to completion",
              "WF-PLAN", modes=["MODE-ENGAGE"], formation="no", derived=[("v1:5.2.2:T3", "rewritten")]),
        ],
        "levels": {
            "L1": [
                I("Records a meeting's discussion points, decisions and commitments so that participants confirm the "
                  "summary without substantive correction.", RA, tasks=["seed:v1-5.2.2-T3"],
                  evidence=["meeting summary"]),
                I("Prepares meeting logistics and materials from a facilitator's plan, including the access arrangements "
                  "participants requested in advance.", WS, tasks=["seed:v1-5.2.2-T1"], evidence=["meeting packet"]),
            ],
            "L2": [
                I("Facilitates a routine working session to its agenda, keeping each participant group's input on the "
                  "record and closing with agreed next steps.", TB + SIM, attr="ATT-AUT",
                  tasks=["seed:v1-5.2.2-T2"], evidence=["observation record"]),
                I("Designs a workshop agenda and participation format matched to the purpose and the parties, accepted by "
                  "the convening official.", WS, attr="ATT-GUI", tasks=["seed:v1-5.2.2-T1"], evidence=["agenda"]),
            ],
            "L3": [
                I("Facilitates a contested public meeting in an observed or simulated session, de-escalating conflict while "
                  "keeping the session to its stated purpose.", SIM + TB, attr="ATT-CPX",
                  tasks=["seed:v1-5.2.2-T2"], evidence=["observation record"]),
                I("Redesigns a multi-session process when participation or conflict changes, recording the reason for "
                  "each change and the participants' response.", PORT + RA, attr="ATT-GUI",
                  tasks=["seed:v1-5.2.2-T1"], evidence=["process change log"]),
            ],
            "L4": [
                I("Sets an organization's facilitation standards and meeting-design templates, with the evaluation used "
                  "after each public meeting.", PORT, attr="ATT-GUI", tasks=["seed:v1-5.2.2-T1"],
                  evidence=["standards", "evaluation form"]),
                I("Evaluates new facilitators in observed sessions against the organization's standard before they lead "
                  "public meetings alone.", TB, attr="ATT-FOR", tasks=["seed:v1-5.2.2-T2"],
                  evidence=["evaluation record"]),
            ],
        },
        "enactments": [],
    },
    # ------------------------------------------------------------------ v1 5.2.3
    {
        "id": "seed:v1-5.2.3",
        "label": "Run collaborative processes in which parties shape a decision",
        "alt": ["collaborative decision-making processes", "collaborative governance", "consensus building",
                "advisory committee management"],
        "definition": "The capability to convene and run working groups, advisory committees and consensus-seeking "
                      "forums in which affected parties help develop a plan or decision, with a defined charge, decision "
                      "rule and account of how the deciding authority uses the result.",
        "statement": "Convenes and runs collaborative processes such as working groups, advisory committees and "
                     "consensus-seeking forums in which affected parties help develop a plan or decision, defining each "
                     "body's charge and decision rule, the information parties share, and how the deciding authority will "
                     "use their recommendations.",
        "span": ("L2", "L4"),
        "derived": [],
        "sources": ["SC-051"],
        "editorial": "WP-05 (A5 SC). v1 5.2.3 carried with v2 indicators (collaborative competencies among federal "
                     "managers, SC-051, not re-read this session [J]). Tribal-actor enactment notes requested by TN are "
                     "drafted only under the ADR-0007 hold and are not authored here.",
        "sensitivity": [
            ("DM-04", "Required versus discretionary participation sets the room for collaboration.", "E", ["SC-038"]),
            ("DM-12", "Agreement authorities let collaborative groups take on implementation roles.", "E", ["SC-030"]),
        ],
        "tasks": [
            T("seed:v1-5.2.3-T1", "Convene a working group to co-develop a management strategy, defining its charge, "
              "membership, decision rule and how its recommendations will be used",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["stakeholder", "intergovernmental"], formation="yes",
              derived=[("v1:5.2.3:T1", "rewritten")]),
            T("seed:v1-5.2.3-T2", "Use consensus-building or participatory modeling methods with a working group, recording "
              "areas of agreement and disagreement and the reasons for each",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["stakeholder"], formation="yes",
              derived=[("v1:5.2.3:T2", "rewritten")]),
            T("seed:v1-5.2.3-T3", "Publish each step of a collaborative process and the information parties used, so that "
              "participants can see how their recommendations were treated",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["public"], formation="no", derived=[("v1:5.2.3:T3", "rewritten")]),
            T("seed:sc-explain-recommendation-use", "Explain to a collaborative group how the deciding authority used, "
              "modified or rejected its recommendations, giving the reasons for each",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["stakeholder"], formation="partial"),
        ],
        "levels": {
            "L2": [
                I("Writes a collaborative group's charter stating its charge, membership, decision rule and how the "
                  "deciding authority will use its recommendations.", WS, tasks=["seed:v1-5.2.3-T1"],
                  evidence=["charter"]),
                I("Records areas of agreement and disagreement at each session with the reasons parties gave, confirmed by "
                  "the group before the next session.", RA, tasks=["seed:v1-5.2.3-T2"], evidence=["session records"]),
            ],
            "L3": [
                I("Runs a multi-party collaborative process to recommendations that the deciding authority adopts in "
                  "whole or with stated reasons for each change.", PORT + C360, attr="ATT-CPX",
                  tasks=["seed:v1-5.2.3-T1"], evidence=["process record", "decision document"]),
                I("Uses a participatory modeling or consensus method suited to the group's question, documenting why the "
                  "method was chosen and its limits.", WS + BARS, attr="ATT-GUI", tasks=["seed:v1-5.2.3-T2"],
                  evidence=["method memo"]),
                I("Explains to a collaborative group in writing how each of its recommendations was used, modified or "
                  "rejected, with the reasons.", WS + RA, attr="ATT-SCO",
                  tasks=["seed:sc-explain-recommendation-use"], evidence=["response to recommendations"]),
            ],
            "L4": [
                I("Designs the collaborative structure for a long-running program, with charters, membership rotation and "
                  "decision rules that continue through staff turnover.", PORT, attr="ATT-GUI",
                  tasks=["seed:v1-5.2.3-T1"], evidence=["structure design"]),
                I("Coaches conveners of collaborative groups, reviewing their charters and session records against the "
                  "organization's standard.", PORT + RA, attr="ATT-FOR", tasks=["seed:v1-5.2.3-T2"],
                  evidence=["coaching record"]),
            ],
        },
        "enactments": [
            E("seed:ena-v1-5-2-3-federal", "Federal advisory and collaborative bodies", "federal-agency",
              basis="Federal rules on chartered advisory committees and on agency use of collaborative groups that are "
                    "not chartered committees.",
              principal="The deciding official and the committee's designated federal officer.",
              venue="Committee oversight; federal courts in rare challenges.",
              note="Whether a group needs a charter changes how it is convened; the governing advisory-committee statute "
                   "is an L5 instrument to register [J]."),
        ],
    },
    # ------------------------------------------------------------------ v1 5.2.4 (absorbs 5.5.3)
    {
        "id": "seed:v1-5.2.4",
        "label": "Resolve conflicts and mediate disputes over environmental decisions",
        "alt": ["conflict resolution and mediation", "complaint resolution", "environmental mediation"],
        "definition": "The capability to help parties in conflict over environmental decisions, services or land and "
                      "resource use reach durable agreements, from complaint resolution to mediation as a neutral. "
                      "Negotiating as a party is a separate competency (interest-based negotiation).",
        "statement": "Helps parties in conflict over environmental decisions, services or land and resource use reach "
                     "durable agreements: assesses the conflict, chooses an approach from complaint resolution and "
                     "facilitated negotiation to mediation as a neutral, manages communication and escalation, and records "
                     "agreements and their follow-up.",
        "span": ("L1", "L4"),
        "derived": [("v1:5.5.3", "merged-from")],
        "sources": [],
        "editorial": "WP-05 (A5 SC). v1 5.2.4 carried with v2 indicators in the Resolve and defend mode; absorbs 5.5.3 "
                     "(complaint resolution, merged to hold the core within the G-9 range); pairs with SC-C07 "
                     "(negotiating as a party).",
        "sensitivity": [
            ("DM-08", "Narrower judicial remedies shift disputes toward negotiated and mediated resolution.", "J", None),
        ],
        "tasks": [
            T("seed:sc-assess-conflict", "Assess a conflict before intervening, identifying the parties, issues, interests "
              "and whether mediation, negotiation or another process fits",
              "WF-PLAN", modes=["MODE-RESOLVE"], formation="yes"),
            T("seed:v1-5.2.4-T1", "Mediate a dispute between parties over land use or project effects as a neutral, "
              "recording the agreement or impasse reached",
              "WF-PLAN", modes=["MODE-RESOLVE"], rel=["stakeholder"], field="on-site-preferred", formation="yes",
              derived=[("v1:5.2.4:T1", "rewritten")]),
            T("seed:v1-5.2.4-T2", "Restate each party's concern during a tense exchange until the party confirms it was "
              "understood, so that the exchange can continue",
              "WF-PLAN", modes=["MODE-RESOLVE", "MODE-ENGAGE"], rel=["public", "stakeholder"], formation="yes",
              derived=[("v1:5.2.4:T2", "rewritten")]),
            T("seed:v1-5.2.4-T3", "Draft an agreement recording the shared goals and specific commitments parties reached, "
              "with the steps for handling future disagreement",
              "WF-PLAN", modes=["MODE-RESOLVE"], formation="partial", derived=[("v1:5.2.4:T3", "rewritten")]),
            T("seed:v1-5.5.3-T1", "Take a complaint from a member of the public about land use or services, recording the "
              "facts, the concern and the outcome the person seeks",
              "WF-OPERATE", modes=["MODE-RESOLVE", "MODE-ENGAGE"], rel=["public"], formation="no",
              derived=[("v1:5.5.3:T1", "rewritten")]),
            T("seed:v1-5.5.3-T2", "Investigate a complaint and respond within the program's time standard, explaining the "
              "finding and any corrective action taken",
              "WF-OPERATE", modes=["MODE-RESOLVE"], rel=["public"], field="on-site-preferred", formation="partial",
              derived=[("v1:5.5.3:T2", "rewritten")]),
            T("seed:v1-5.5.3-T3", "Escalate a complaint that exceeds one's authority or recurs, documenting the facts and the "
              "outcome for quality review",
              "WF-OPERATE", modes=["MODE-RESOLVE"], formation="no", derived=[("v1:5.5.3:T3", "rewritten")]),
        ],
        "levels": {
            "L1": [
                I("Records a complaint with its facts, the person's concern and the outcome sought, so that a supervisor "
                  "can act on it without re-contacting the person.", RA, tasks=["seed:v1-5.5.3-T1"],
                  evidence=["complaint record"]),
                I("Responds to a routine complaint within the program's time standard, explaining the finding and any "
                  "corrective action in writing.", RA + WS, tasks=["seed:v1-5.5.3-T2"], evidence=["response letter"]),
            ],
            "L2": [
                I("Restates each party's concern in a tense exchange until the party confirms it, in an observed or "
                  "simulated session scored on a rubric.", SIM + TB, attr="ATT-AUT", tasks=["seed:v1-5.2.4-T2"],
                  evidence=["observation record"]),
                I("Escalates complaints that exceed the person's authority or recur, documenting the facts and outcome for "
                  "quality review.", RA, attr="ATT-GUI", tasks=["seed:v1-5.5.3-T3"], evidence=["escalation log"]),
            ],
            "L3": [
                I("Mediates a dispute between parties as a neutral in an observed or simulated session, reaching an "
                  "agreement or a documented impasse.", SIM, attr="ATT-SCO", tasks=["seed:v1-5.2.4-T1"],
                  evidence=["mediation record"]),
                I("Writes a conflict assessment naming parties, issues and interests and recommending the process that "
                  "fits, accepted by the convening official.", WS + BARS, attr="ATT-CPX",
                  tasks=["seed:sc-assess-conflict"], evidence=["conflict assessment"]),
            ],
            "L4": [
                I("Designs an organization's dispute-resolution system, with intake, escalation and neutral-referral rules "
                  "and an annual review of outcomes.", PORT, attr="ATT-GUI", tasks=["seed:sc-assess-conflict"],
                  evidence=["system design"]),
                I("Evaluates staff mediations or complaint resolutions against the organization's standard, recording the "
                  "evidence for each evaluation.", RA + TB, attr="ATT-FOR", tasks=["seed:v1-5.2.4-T1"],
                  evidence=["evaluation record"]),
            ],
        },
        "enactments": [],
    },
    # ------------------------------------------------------------------ v1 5.2.5
    {
        "id": "seed:v1-5.2.5",
        "label": "Develop and manage partnerships for shared environmental goals",
        "alt": ["partnership development and management", "partner relations"],
        "definition": "The capability to build and sustain working partnerships with agencies, organizations and "
                      "community groups toward shared goals, from agreeing roles to tracking results and renewing or "
                      "closing the partnership. Designing binding cross-jurisdictional agreements is a separate competency.",
        "statement": "Builds and sustains working partnerships with agencies, organizations and community groups toward "
                     "shared goals: identifies partners whose interests align, agrees roles and contributions, coordinates "
                     "joint work, tracks partnership outcomes, and renews or closes partnerships based on results.",
        "span": ("L1", "L4"),
        "derived": [],
        "sources": [],
        "editorial": "WP-05 (A5 SC). v1 5.2.5 carried (SC carry) with observable anchors replacing generic proficiency "
                     "text. Binding agreement design sits in SC-C08; contract and grant administration in v1 3.1.4.",
        "sensitivity": [
            ("DM-12", "Agreement authorities set what partners can do together.", "E", ["SC-030"]),
            ("DM-19", "Partner funding programmes are cut or reinstated by appropriations.", "J", None),
        ],
        "tasks": [
            T("seed:v1-5.2.5-T1", "Establish a partnership with an agency, organization or community group, agreeing shared "
              "goals, each party's contribution and how progress will be reported",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["stakeholder", "intergovernmental"], formation="partial",
              derived=[("v1:5.2.5:T1", "rewritten")]),
            T("seed:v1-5.2.5-T2", "Record a partnership's roles and objectives in a written understanding that each "
              "partner's authorized official accepts",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["stakeholder", "intergovernmental"], formation="partial",
              also=["seed:SC-C08"], derived=[("v1:5.2.5:T2", "rewritten")]),
            T("seed:v1-5.2.5-T3", "Coordinate joint initiatives with partners, tracking partnership outcomes against the "
              "shared goals and reporting them to each partner",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["stakeholder"], formation="partial",
              derived=[("v1:5.2.5:T3", "rewritten")]),
            T("seed:sc-review-partnership-results", "Review a partnership's results with partners each year, deciding with "
              "them to renew, change or close it and recording the reasons",
              "WF-LEARN", modes=["MODE-ENGAGE"], rel=["stakeholder"], formation="partial"),
        ],
        "levels": {
            "L1": [
                I("Tracks partner contributions and joint-activity outputs against the partnership's work plan, with no "
                  "reported output lacking a source record.", RA, tasks=["seed:v1-5.2.5-T3"],
                  evidence=["tracking log"]),
                I("Prepares partner meeting materials and records the decisions and assignments made for the partnership "
                  "lead.", RA, tasks=["seed:v1-5.2.5-T3"], evidence=["meeting record"]),
            ],
            "L2": [
                I("Establishes a partnership with agreed goals, contributions and reporting that each partner's authorized "
                  "official accepts in writing.", WS, attr="ATT-AUT", tasks=["seed:v1-5.2.5-T1"],
                  evidence=["partnership understanding"]),
                I("Reports partnership outcomes against the shared goals to each partner, stating which goals were met and "
                  "why others were not.", WS, attr="ATT-SCO", tasks=["seed:v1-5.2.5-T3"],
                  evidence=["outcome report"]),
            ],
            "L3": [
                I("Sustains a multi-partner initiative through a change of partner leadership, recording how commitments "
                  "were reconfirmed.", PORT + C360, attr="ATT-CPX", obs4=2, tasks=["seed:v1-5.2.5-T1"],
                  evidence=["partnership record"]),
                I("Reviews a partnership's results with partners and decides with them to renew, change or close it, "
                  "recording the reasons.", PORT, attr="ATT-GUI", tasks=["seed:sc-review-partnership-results"],
                  evidence=["review record"]),
                I("Resolves a partner disagreement about contributions or credit, documenting the issue and the agreed "
                  "resolution.", RA, attr="ATT-SCO", tasks=["seed:v1-5.2.5-T3"], evidence=["resolution record"]),
            ],
            "L4": [
                I("Sets an organization's partnership strategy, with criteria for choosing, reviewing and closing "
                  "partnerships across programs.", PORT, attr="ATT-GUI", tasks=["seed:sc-review-partnership-results"],
                  evidence=["strategy"]),
                I("Coaches staff who manage partnerships, reviewing their partnership records against the strategy's "
                  "criteria.", PORT + RA, attr="ATT-FOR", tasks=["seed:v1-5.2.5-T1"], evidence=["coaching record"]),
            ],
        },
        "enactments": [],
    },
]
