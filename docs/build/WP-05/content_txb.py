"""WP-05 content: TX-B professional integrity and accountability (v1 7.1.2, v1 7.1.3, PS-C18, SL-C16; ADR-0025).
Integrity is assessed through work products and procedures, never as a trait (IO B11). The v1 7.1.2 recognition of
Tribal governments as authorities with standing is held content (TN) and is written here actor-neutrally."""
from wp05dsl import T, I, E

WS = ["work-sample"]
RA = ["record-audit"]
SEW = ["seeded-error-work-sample"]
BARS = ["structured-interview-bars"]
SJT = ["situational-judgment-test"]
PORT = ["portfolio-review"]
KT = ["knowledge-test"]
MOOT = ["moot-defense"]

COMPETENCIES = [
    # ------------------------------------------------------------------ v1 7.1.2
    {
        "id": "seed:v1-7.1.2",
        "type": "transversal", "cluster": "TX-B", "reusability": "transversal",
        "label": "Authorize ecological interventions with legitimate standing and precaution",
        "alt": ["intervention authorization", "ecological precaution", "authorization with standing"],
        "definition": "The capability to establish, before a management intervention proceeds, that every party whose "
                      "authority, consent or standing it requires has authorized it, that precautionary criteria for "
                      "reversibility and uncertainty have been applied, and that monitoring and exit conditions are set "
                      "and recorded.",
        "statement": "Before a management intervention proceeds, identifies every party whose authority, consent or "
                     "standing it requires, tests the intervention against reversibility, uncertainty and precedent "
                     "criteria, sets monitoring obligations and exit conditions, and records who authorized it and on "
                     "what basis.",
        "span": ("L2", "L4"),
        "derived": [],
        "sources": [],
        "editorial": "WP-05 (A5 SC). v1 7.1.2 rewrite moved to the transversal layer with observable indicators "
                     "(ADR-0025). TN's verdict that Tribal governments are authorities with standing is preserved as a "
                     "held enactment for TN to draft under the Tribal hold; this record is written actor-neutrally and "
                     "names no Tribal content.",
        "tasks": [
            T("seed:v1-7.1.2-T1", "Evaluate a proposed ecological intervention against reversibility, precedent and "
              "uncertainty criteria, recording whether precautionary conditions apply and why",
              "WF-PLAN", formation="yes", derived=[("v1:7.1.2:T1", "rewritten")]),
            T("seed:v1-7.1.2-T2", "Identify every party whose authority, consent or standing a proposed intervention "
              "requires, documenting how each will authorize or be consulted",
              "WF-PLAN", modes=["MODE-ENGAGE"], rel=["intergovernmental", "stakeholder"], formation="yes",
              derived=[("v1:7.1.2:T2", "rewritten")]),
            T("seed:v1-7.1.2-T3", "Write an intervention decision framework stating authorization requirements, "
              "reversibility thresholds, monitoring obligations and exit conditions for a class of actions",
              "WF-PLAN", formation="partial", derived=[("v1:7.1.2:T3", "rewritten")]),
            T("seed:sc-halt-unauthorized-intervention", "Halt an intervention when a required authorization is missing, "
              "documenting the gap and the step needed to close it",
              "WF-BUILD", field="on-site-preferred", formation="yes"),
        ],
        "levels": {
            "L2": [
                I("Records, for a proposed intervention, each party whose authority or consent it needs and the evidence "
                  "that each authorization was obtained.", RA, tasks=["seed:v1-7.1.2-T2"],
                  evidence=["authorization record"], v1=["v1:7.1.2:intermediate:I1"]),
                I("Applies the program's reversibility and uncertainty criteria to a proposed intervention, documenting "
                  "whether precautionary conditions apply and the reason.", WS, tasks=["seed:v1-7.1.2-T1"],
                  evidence=["precaution screening"]),
            ],
            "L3": [
                I("Sets monitoring obligations and exit conditions for a novel intervention, stating the observation that "
                  "would trigger a halt or reversal.", WS + BARS, attr="ATT-CPX", tasks=["seed:v1-7.1.2-T3"],
                  evidence=["monitoring and exit plan"]),
                I("Halts an intervention when a required authorization is missing, documenting the gap and the step needed "
                  "to close it before work resumes.", SJT + RA, attr="ATT-AUT",
                  tasks=["seed:sc-halt-unauthorized-intervention"], evidence=["stop-work record"]),
            ],
            "L4": [
                I("Writes an intervention decision framework for a class of actions, with authorization, reversibility, "
                  "monitoring and exit criteria that reviewers can audit.", PORT, attr="ATT-GUI",
                  tasks=["seed:v1-7.1.2-T3"], evidence=["decision framework"]),
                I("Reviews staff intervention proposals against the framework, returning each proposal that lacks a "
                  "documented authorization or exit condition.", RA, attr="ATT-FOR", tasks=["seed:v1-7.1.2-T2"],
                  evidence=["review log"]),
            ],
        },
        "enactments": [],
    },
    # ------------------------------------------------------------------ v1 7.1.3
    {
        "id": "seed:v1-7.1.3",
        "type": "transversal", "cluster": "TX-B", "reusability": "transversal",
        "label": "Maintain the integrity of regulatory and scientific findings under institutional pressure",
        "alt": ["regulatory professional integrity", "scientific integrity", "integrity of findings"],
        "definition": "The capability to produce and report regulatory and scientific findings that represent the "
                      "evidence, including uncertainty, contrary evidence and AI assistance, to disclose conflicts, and "
                      "to use documented channels when pressure conflicts with professional obligations. Assessed "
                      "through work products and records, never as a trait.",
        "statement": "Produces and reports regulatory and scientific findings that reflect the evidence when employers, "
                     "clients, funders or schedules press otherwise: discloses conflicts, uncertainty, dissenting views "
                     "and AI assistance, documents requests to alter findings, and uses the organization's integrity "
                     "and escalation procedures.",
        "span": ("L1", "L4"),
        "derived": [],
        "sources": ["WP05-004"],
        "editorial": "WP-05 (A5 SC). v1 7.1.3 rewrite to TX-B, extended to AI provenance in the record, disclosure of AI "
                     "assistance and cross-boundary independence (with PS-C18) (SC, PS verdicts). v1 cited NEPA "
                     "scientific-integrity requirements; rule names move to L5 (federal scientific-integrity policies "
                     "are being updated under a 2025 executive order [E: WP05-004]). Indicators adapted from IO exemplar "
                     "rewrites for v1 7.1.3.",
        "sensitivity": [
            ("DM-14", "AI-assisted analysis creates new disclosure and provenance duties.", "J", None),
            ("DM-16", "Federal scientific-integrity policies are being revised under a 2025 order.", "E", ["WP05-004"]),
        ],
        "tasks": [
            T("seed:v1-7.1.3-T1", "Document any instruction or pressure to alter a regulatory or scientific finding, "
              "recording who made it, what was requested and the response given",
              "WF-MONITOR", formation="partial", derived=[("v1:7.1.3:T1", "rewritten")]),
            T("seed:v1-7.1.3-T2", "Disclose conflicts of interest, uncertainty, dissenting views and AI assistance in a "
              "regulatory submission or public document, following the organization's integrity policy",
              "WF-MONITOR.attest", formation="partial", derived=[("v1:7.1.3:T2", "rewritten")]),
            T("seed:v1-7.1.3-T3", "Write quality-assurance and escalation procedures that protect the independence of "
              "regulatory findings, including peer-review steps and documentation of changes",
              "WF-MANAGE", formation="yes", derived=[("v1:7.1.3:T3", "rewritten")]),
            T("seed:sc-escalate-integrity-conflict", "Escalate an unresolved integrity conflict through the organization's "
              "scientific-integrity or ethics channel, documenting the facts and the outcome",
              "WF-MONITOR", formation="partial"),
        ],
        "levels": {
            "L1": [
                I("Discloses actual or potential conflicts of interest in an assigned project through the organization's "
                  "disclosure procedure before work begins.", RA + SJT, tasks=["seed:v1-7.1.3-T2"],
                  evidence=["disclosure record"], v1=["v1:7.1.3:foundational:I4"]),
                I("Labels each AI-assisted passage in a work product after checking it against its sources, as the "
                  "organization's disclosure procedure requires.", SEW + RA, mode="assisted",
                  tasks=["seed:v1-7.1.3-T2"], evidence=["labelled work product", "check log"]),
            ],
            "L2": [
                I("Reports uncertainty, data limitations and evidence contrary to the preferred conclusion in a "
                  "regulatory analysis, so that a reviewer can see what the evidence does not support.", SEW + WS,
                  attr="ATT-AUT", tasks=["seed:v1-7.1.3-T2"], evidence=["analysis"],
                  v1=["v1:7.1.3:intermediate:I3"]),
                I("Records in the project file any direction received to change a technical finding or scope, with date, "
                  "source and the technical basis for any disagreement.", RA + SJT, attr="ATT-AUT",
                  tasks=["seed:v1-7.1.3-T1"], evidence=["project file entry"], v1=["v1:7.1.3:intermediate:I2"]),
            ],
            "L3": [
                I("Identifies which professional code provision and integrity policy apply to a contested situation and "
                  "selects the escalation path the policy provides, in a case-based exercise.", SJT + BARS,
                  attr="ATT-GUI", tasks=["seed:sc-escalate-integrity-conflict"], evidence=["case response"],
                  v1=["v1:7.1.3:intermediate:I1", "v1:7.1.3:intermediate:I4"]),
                I("Designs a project's peer-review and change-documentation steps so that every change to a finding after "
                  "review is traceable to evidence.", WS + RA, attr="ATT-SCO", tasks=["seed:v1-7.1.3-T3"],
                  evidence=["review plan"]),
            ],
            "L4": [
                I("Designs review and documentation procedures for a program that make changes to technical findings "
                  "traceable and reviewable, tested against past contested cases.", PORT, attr="ATT-GUI",
                  tasks=["seed:v1-7.1.3-T3"], evidence=["procedures", "test memo"], v1=["v1:7.1.3:advanced:I1"]),
                I("Investigates an allegation of compromised findings under the organization's procedure, documenting the "
                  "evidence, findings and corrective actions.", PORT + RA, attr="ATT-SCO",
                  tasks=["seed:sc-escalate-integrity-conflict"], evidence=["investigation report"],
                  v1=["v1:7.1.3:expert:I3"]),
            ],
        },
        "enactments": [
            E("seed:ena-v1-7-1-3-federal", "Federal scientific-integrity policies", "federal-agency",
              basis="Agency scientific-integrity policies, being updated under a 2025 executive order that keeps the "
                    "policies in effect on 2021-01-19 until updated and protects consideration of dissenting views.",
              principal="The agency scientific-integrity official and leadership.",
              venue="Agency scientific-integrity review; inspectors general; whistleblower channels.",
              note="The escalation channel and its protections are set by the current agency policy version, an L5 "
                   "instrument to register (worklog) [E: WP05-004].", evidence="E", sources=["WP05-004"]),
            E("seed:ena-v1-7-1-3-consultant", "Consultant integrity under client pressure", "firm",
              position="service-provider",
              basis="Professional codes of ethics, licensure rules where they apply, and contract terms.",
              principal="The client, with professional obligations to regulators and the public.",
              venue="Licensing boards; agency adequacy review; courts.",
              note="Client pressure on findings is the common case in sponsor-paid work; see PS-C18 for "
                   "independence safeguards [J]."),
        ],
    },
    # ------------------------------------------------------------------ PS-C18
    {
        "id": "seed:PS-C18",
        "type": "transversal", "cluster": "TX-B", "reusability": "transversal",
        "label": "Maintain independence and manage conflicts of interest across the regulator-regulated boundary",
        "alt": ["conflict of interest management", "independence safeguards", "revolving-door restrictions",
                "post-employment restrictions"],
        "definition": "The capability to identify, disclose and manage financial, employment and relationship conflicts "
                      "that arise when work or people cross between regulators, regulated parties and their consultants, "
                      "including recusal and post-employment restrictions, so that work products stay independent of "
                      "any party's interest in the outcome.",
        "statement": "Identifies, discloses and manages financial, employment and relationship conflicts that arise when "
                     "work crosses between regulators, regulated parties and their consultants, observes recusal and "
                     "post-employment restrictions, and keeps the work product independent of any party's interest in "
                     "its outcome.",
        "span": ("L1", "L4"),
        "sources": ["V2-04"],
        "editorial": "WP-05 (A5 SC; PS candidate). Independence across the regulator-regulated boundary (ADR-0025 TX-B); "
                     "v1 7.1.3 extended per the PS verdict. Sponsor-paid review and sponsor-prepared documents raise "
                     "the stakes [E: V2-04]. Post-employment restrictions are also a mobility friction "
                     "(friction type post-employment-ethics).",
        "sensitivity": [
            ("DM-02", "Sponsor-paid acceleration increases sponsor and contractor roles in review.", "E", ["V2-04"]),
            ("DM-16", "Hiring and appointment rule changes alter movement between sectors.", "J", None),
        ],
        "tasks": [
            T("seed:sc-disclose-assignment-interests", "Disclose financial, employment or relationship interests that "
              "could affect an assignment before work begins, using the organization's conflict form",
              "WF-MANAGE", formation="no"),
            T("seed:sc-recuse-covered-matter", "Recuse from a decision or review in which a former employer or client has "
              "an interest, documenting the recusal and the reassignment of the work",
              "WF-MANAGE", formation="no"),
            T("seed:sc-screen-assignment-conflicts", "Screen a proposed contractor or staff assignment for conflicts with "
              "the project's regulated parties, recording the screening result and any mitigation",
              "WF-MANAGE", formation="partial"),
            T("seed:sc-apply-post-employment-rules", "Apply post-employment restrictions when moving between a regulator "
              "and a regulated party, obtaining written ethics advice before contact on covered matters",
              "WF-MANAGE", formation="no"),
        ],
        "levels": {
            "L1": [
                I("Completes the conflict-of-interest disclosure for each assignment before work starts, with no "
                  "undisclosed interest found in an ethics audit.", RA, tasks=["seed:sc-disclose-assignment-interests"],
                  evidence=["disclosure forms"]),
                I("Refers a contact from a former employer or client on a covered matter to the ethics official before "
                  "responding, recording the referral.", SJT + RA, tasks=["seed:sc-apply-post-employment-rules"],
                  evidence=["referral record"]),
            ],
            "L2": [
                I("Recuses from a covered matter and documents the recusal and reassignment in the file before any "
                  "action on the matter.", RA, attr="ATT-AUT", tasks=["seed:sc-recuse-covered-matter"],
                  evidence=["recusal record"]),
                I("Screens a proposed contractor for conflicts with the project's regulated parties, recording the result "
                  "and any mitigation required before award.", WS + RA, attr="ATT-SCO",
                  tasks=["seed:sc-screen-assignment-conflicts"], evidence=["screening record"]),
            ],
            "L3": [
                I("Designs conflict mitigation for a project whose staff or contractors have cross-boundary histories, "
                  "with screening walls and records an ethics officer approves.", WS + PORT, attr="ATT-CPX",
                  tasks=["seed:sc-screen-assignment-conflicts"], evidence=["mitigation plan"]),
                I("Advises colleagues moving between regulator and regulated roles on the restrictions that apply, citing "
                  "the written ethics advice obtained.", BARS + SJT, attr="ATT-SCO", obs4=2,
                  tasks=["seed:sc-apply-post-employment-rules"], evidence=["advice record"]),
                I("Reviews a team's disclosure forms for a project against its regulated parties, flagging each "
                  "relationship that needs recusal or mitigation.", RA, attr="ATT-SCO",
                  tasks=["seed:sc-disclose-assignment-interests"], evidence=["review log"]),
            ],
            "L4": [
                I("Sets an organization's independence and conflict procedures for cross-boundary work, with audit steps "
                  "and an annual review of disclosures.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-screen-assignment-conflicts"], evidence=["procedures"]),
                I("Investigates a suspected independence breach under the organization's procedure, documenting the facts, "
                  "finding and corrective action.", PORT + RA, attr="ATT-SCO", tasks=["seed:sc-recuse-covered-matter"],
                  evidence=["investigation report"]),
            ],
        },
        "enactments": [
            E("seed:ena-ps-c18-federal", "Federal ethics and post-employment rules", "federal-agency",
              basis="Federal criminal conflict-of-interest and post-employment statutes and the standards of ethical "
                    "conduct for executive-branch employees; agency supplemental rules.",
              principal="The designated agency ethics official.", venue="Office of Government Ethics; inspectors "
                                                                         "general; prosecutors.",
              note="These rules are L5 instruments to register (worklog); they also generate the post-employment-ethics "
                   "friction on federal-to-private moves [J]."),
            E("seed:ena-ps-c18-state", "State and local ethics codes", "state-agency",
              basis="State ethics acts and local codes, with their own cooling-off periods and disclosure forms.",
              principal="The state ethics commission or agency ethics officer.", venue="State ethics commissions; courts.",
              note="SL review: cooling-off periods and covered-matter definitions differ by state [J].", sl_reviewed=True),
            E("seed:ena-ps-c18-consultant", "Consultant independence in sponsor-paid work", "firm",
              position="service-provider",
              basis="Disclosure statements required by the agency, contract terms and professional codes.",
              principal="The client and the agency that relies on the work.", venue="Agency adequacy review; "
                                                                               "professional ethics boards.",
              note="Preparer disclosure statements are the mirror of the agency's screening task in SC-C04 [J]."),
            E("seed:ena-ps-c18-verifier", "Independent verifier independence", "firm", position="independent-verifier",
              basis="Accreditation and programme rules on verifier independence, rotation and conflicts.",
              principal="The accreditation body and the verification client.", venue="Accreditation audits.",
              note="Verifiers carry formal independence rules that are stricter than consultants' [J]."),
        ],
    },
    # ------------------------------------------------------------------ SL-C16
    {
        "id": "seed:SL-C16",
        "type": "transversal", "cluster": "TX-B", "reusability": "transversal",
        "label": "Practice within licensure scope and responsible charge",
        "alt": ["scope of practice", "responsible charge", "professional seal", "licensed practice"],
        "definition": "The capability to perform, seal or certify only the work one's licence, registration or "
                      "certification permits, to exercise or work under responsible charge as licensing rules require, "
                      "and to certify AI-assisted deliverables only after personal verification. The credential itself "
                      "is a gate recorded on tasks and roles, not part of this competency.",
        "statement": "Performs, seals or certifies only the work that one's licence, registration or certification "
                     "permits; works under or exercises responsible charge as the licensing rules require; refers work "
                     "outside scope; and certifies AI-assisted deliverables only after personally verifying them to the "
                     "professional standard of care.",
        "span": ("L1", "L4"),
        "sources": ["SL-055", "SL-054", "SL-085", "SL-047"],
        "editorial": "WP-05 (A5 SC; SL candidate). Survivor: absorbs PS-C20 (certifying AI-drafted deliverables under "
                     "professional liability). State classes are split by licensure (TX engineering specialists barred "
                     "from engineering practice duties; geologic specialists under a licensed geologist; WI title "
                     "restriction) [E: SL-055, SL-054, SL-085]. Credentials are gates (T-8): the Credential register "
                     "(WP-07) supplies licence records for signOffAuthority links.",
        "sensitivity": [
            ("DM-17", "Licensure, certification and responsible-charge rules govern who may sign.", "E", ["SL-055", "SL-085"]),
            ("DM-14", "AI drafting raises the question of what a seal attests to.", "J", None),
        ],
        "tasks": [
            T("seed:sc-check-scope-of-practice", "Determine whether an assigned task falls within the scope of one's "
              "licence or certification, referring out-of-scope work to a qualified professional",
              "WF-MANAGE", formation="partial"),
            T("seed:sc-seal-deliverable", "Certify a professional deliverable under seal only after personally reviewing "
              "the work, including any AI-assisted portions, to the standard of care",
              "WF-MONITOR.attest", formation="yes", signoff="licensure",
              accountable="Licensing law makes the sealing professional personally responsible for the sealed work."),
            T("seed:sc-exercise-responsible-charge", "Exercise responsible charge over subordinates' professional work, "
              "directing and reviewing it so that the sealing professional can attest to it",
              "WF-MANAGE", formation="yes", signoff="licensure"),
            T("seed:sc-keep-sealed-work-records", "Keep the records licensing rules require for sealed work, including "
              "review notes and the basis for each certification",
              "WF-MONITOR.attest", formation="no"),
        ],
        "levels": {
            "L1": [
                I("Refers an assigned task outside the scope of the person's credential to the responsible licensed "
                  "professional, recording the referral before work proceeds.", SJT + RA,
                  tasks=["seed:sc-check-scope-of-practice"], evidence=["referral record"]),
                I("Records the supervising professional's review of each work product prepared under responsible charge, "
                  "as the licensing rules require.", RA, tasks=["seed:sc-exercise-responsible-charge"],
                  evidence=["review records"]),
            ],
            "L2": [
                I("Certifies a deliverable only after verifying every AI-assisted section against source data and "
                  "calculations, documenting the checks in the project file.", SEW + RA, attr="ATT-AUG",
                  mode="assisted", tasks=["seed:sc-seal-deliverable"], evidence=["check log", "sealed deliverable"],
                  critical=True),
                I("Keeps sealed-work records with review notes and the basis for each certification, with no gap found "
                  "in a records audit.", RA, attr="ATT-AUT", tasks=["seed:sc-keep-sealed-work-records"],
                  evidence=["sealed-work records"]),
            ],
            "L3": [
                I("Exercises responsible charge over a team's professional work, reviewing each deliverable at the points "
                  "the licensing rules require before sealing.", RA + PORT, attr="ATT-SCO",
                  tasks=["seed:sc-exercise-responsible-charge"], evidence=["review trail"]),
                I("Decides scope-of-practice questions for a project team in writing, citing the licensing rule relied on "
                  "and the referral made for out-of-scope work.", WS + SJT, attr="ATT-GUI",
                  tasks=["seed:sc-check-scope-of-practice"], evidence=["scope memo"]),
            ],
            "L4": [
                I("Sets an organization's procedures for responsible charge and sealing, including review of AI-assisted "
                  "deliverables, with periodic audits of sealed work.", PORT, attr="ATT-AUG", mode="supervisory",
                  tasks=["seed:sc-seal-deliverable"], evidence=["procedures", "audit results"]),
                I("Mentors licensure candidates through supervised professional work, documenting the experience record "
                  "that the licensing board requires.", RA + PORT, attr="ATT-FOR",
                  tasks=["seed:sc-exercise-responsible-charge"], evidence=["experience records"]),
            ],
        },
        "enactments": [
            E("seed:ena-sl-c16-state", "State employee in a licensure-split class", "state-agency",
              basis="State licensing acts (engineering, geology, environmental health, operator certification) and the "
                    "state class plan, which assigns sealing duties only to licensed classes.",
              principal="The licensed supervisor in responsible charge; the licensing board.",
              venue="State licensing boards.",
              note="SL review: class plans are split by licence, so moving into a licensed class is a credential gate, "
                   "not a proficiency step [E: SL-055, SL-054].", sl_reviewed=True, evidence="E",
              sources=["SL-055", "SL-054"]),
            E("seed:ena-sl-c16-private", "Consulting professional sealing deliverables", "firm",
              position="service-provider",
              basis="State licensing acts where the work is performed; firm certificates of authorization; "
                    "professional liability.",
              principal="The client, the licensing board and the public relying on the seal.",
              venue="Licensing boards; courts (professional liability).",
              note="Multi-state practice needs licences in each state; reciprocity is a mobility friction [J]."),
        ],
    },
]
