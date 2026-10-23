"""S2 close-out A content, A5 SC rows due in S2 (SL reviews state and local enactments): v1-3.2.4 (programme strategy and
change leadership; absorbs 3.2.1-3.2.3, 3.5.1, 3.5.3), v1-3.2.5 (adaptive management cycle; absorbs 3.1.5 and the
durable remainder of 3.4.5, ADR-0030 §3.1 M4), v1-5.3.5 (community partnerships; absorbs 5.6.3; EJ as altLabel),
v1-5.3.4-A (accessible, inclusive engagement and services; with SC-C06; absorbs 5.5.5; typed links), and the SC-C02
additions (records retention and disclosure from 3.3.5 and 2.5.2; ADR-0030 §3.1 M5)."""
from s2adsl import T, I, E, WS, RA, SEW, SIM, PORT, C360, TBO, R, EN, C, X

ADR_SC = ["ADR-0003", "ADR-0004", "ADR-0007", "ADR-0016", "ADR-0017", "ADR-0025", "ADR-0030"]

COMPETENCIES = [
    # ------------------------------------------------------------------ v1-3.2.4
    {
        "id": "seed:v1-3.2.4", "agents": ["SC", "SL"], "adr": ADR_SC,
        "label": "Set programme strategy and lead organizational and technological change in environmental programmes",
        "alt": ["strategic planning", "implementation strategy", "change management", "organizational assessment",
                "vision and mission", "goal setting", "digital transformation leadership", "theory of change"],
        "definition": "The capability to assess an environmental programme's mandate, capacity and conditions, set its "
                      "mission, goals and measurable objectives, turn them into an implementation strategy with resources, "
                      "milestones and owners, and lead the organizational and technological change the strategy needs "
                      "while protecting staff capacity and the work that forms new staff. Generic strategic-planning "
                      "techniques are referenced, not covered; horizon scanning is a separate competency.",
        "statement": "Assesses a programme's mandate, capacity and conditions; sets mission, goals and measurable "
                     "objectives with staff and partners; writes the implementation strategy with resources, milestones "
                     "and owners; and leads organizational and technological change, including AI adoption, sequencing "
                     "change to staff capacity and keeping the work that forms new staff.",
        "span": ("L2", "L5"),
        "sources": ["FH-008", "FH-030", "V2-08"],
        "editorial": "S2 close-out A (A5 SC with SL; reviewer CM). Survivor for programme strategy and change leadership; "
                     "absorbs 3.2.1 (organizational assessment), 3.2.2 (vision and mission), 3.2.3 (goal setting), 3.5.1 "
                     "(leading digital and technological change) and 3.5.3 (resilience and change fatigue). Their 15 task "
                     "seeds are rewritten here to environmental-programme context. Generic remainder referenced from "
                     "O*NET/ESCO (G-8). Horizon scanning is FS-C15 (ADR-0025 §4); adaptive management is v1 3.2.5; "
                     "formation consequences of AI adoption link to TX-D (v1 7.2.2).",
        "sensitivity": [
            ("DM-16", "Staffing contraction and reorganization change what a strategy can resource and how much change "
                      "staff can absorb.", "E", ["FH-008", "FH-030"]),
            ("DM-14", "Agency AI-use and permitting-technology policy sets the conditions under which programmes adopt AI "
                      "and automation.", "E", ["V2-08"]),
        ],
        "tasks": [
            T("seed:v1-3.2.1-T1", "Assess a programme's mandate, staff capacity, partners and external conditions before "
              "planning, stating the evidence behind each finding", "WF-PLAN", formation="partial"),
            T("seed:v1-3.2.1-T2", "Gather staff and partner views on a programme's priorities and constraints in structured "
              "sessions, recording each theme raised", "WF-PLAN", formation="no", modes=["MODE-ENGAGE"],
              rel=["stakeholder"]),
            T("seed:v1-3.2.1-T3", "Report the findings of a programme assessment to leadership, ranking the gaps between "
              "mandate and capacity that the strategy must close", "WF-PLAN", formation="partial"),
            T("seed:v1-3.2.2-T1", "Lead a workshop that revises a programme's mission against its legal mandate and the "
              "needs of the people it serves", "WF-PLAN", formation="partial", modes=["MODE-ENGAGE"]),
            T("seed:v1-3.2.2-T2", "Draft a programme's mission and vision statements so that each can be traced to its "
              "legal mandate and partners' stated priorities", "WF-PLAN", formation="no"),
            T("seed:v1-3.2.2-T3", "Revise a programme's strategic statements after each periodic evaluation, recording "
              "which findings prompted each change", "WF-PLAN", formation="no"),
            T("seed:v1-3.2.3-T1", "Translate a programme's environmental goals into measurable, time-bound objectives with "
              "a baseline and an indicator for each", "WF-PLAN", formation="partial"),
            T("seed:v1-3.2.3-T2", "Align teams across programmes or projects on shared outcomes, recording which team is "
              "accountable for each objective", "WF-MANAGE", formation="no"),
            T("seed:v1-3.2.3-T3", "Build a theory of change for a programme, stating the assumption behind each causal link "
              "from action to outcome", "WF-PLAN", formation="partial"),
            T("seed:v1-3.2.4-T1", "Set the actions, milestones and owners for executing a programme strategy, sequencing "
              "them by dependency and available capacity", "WF-PLAN", formation="partial"),
            T("seed:v1-3.2.4-T2", "Prepare a resource plan that matches staff capacity and budget to each strategic "
              "priority, showing what will not be done", "WF-MANAGE", formation="partial"),
            T("seed:v1-3.2.4-T3", "Build monitoring checkpoints and decision rules for adjusting course into a programme's "
              "implementation plan", "WF-PLAN", formation="partial", also=["seed:v1-3.2.5"]),
            T("seed:v1-3.5.1-T1", "Lead the adoption of an AI or automation tool in a programme, addressing staff concerns "
              "about workload, skills and the work that forms new staff", "WF-MANAGE", formation="partial"),
            T("seed:v1-3.5.1-T2", "Run a time-limited pilot of a new technology in a programme, with success criteria and "
              "an adoption decision recorded at the end", "WF-MANAGE", formation="no"),
            T("seed:v1-3.5.1-T3", "Decide which programme tasks stay with staff when automation is adopted, stating the "
              "accountability, formation or public-trust reason for each", "WF-MANAGE", formation="yes"),
            T("seed:v1-3.5.3-T1", "Sequence concurrent organizational changes so that no team absorbs more change than its "
              "agreed capacity in any quarter", "WF-MANAGE", formation="partial"),
            T("seed:v1-3.5.3-T2", "Monitor unit-level workload and attrition during a reorganization, adjusting the change "
              "schedule when a unit exceeds its agreed threshold", "WF-MANAGE", formation="partial"),
            T("seed:v1-3.5.3-T3", "Rank proposed changes by legal requirement, mission risk and cost of delay, deferring "
              "those below the line with a stated review date", "WF-MANAGE", formation="partial"),
        ],
        "levels": {
            "L2": [
                I("Writes measurable, time-bound objectives with a baseline and an indicator for each, for a programme "
                  "goal in a work-sample exercise.", WS, tasks=["seed:v1-3.2.3-T1"], evidence=["objectives table"],
                  v1=["v1:3.2.4:intermediate:I2"]),
                I("Sets actions, milestones and owners for a strategy section so that every objective has an accountable "
                  "owner and a dated milestone.", RA + WS, tasks=["seed:v1-3.2.4-T1"], evidence=["implementation table"],
                  v1=["v1:3.2.4:intermediate:I1", "v1:3.2.4:intermediate:I5"]),
            ],
            "L3": [
                I("Assesses a programme's mandate, capacity and conditions, ranking gaps with the evidence for each, "
                  "accepted by leadership as the planning basis.", WS + PORT, attr="ATT-AUT",
                  tasks=["seed:v1-3.2.1-T1", "seed:v1-3.2.1-T3"], evidence=["assessment report"]),
                I("Builds a theory of change for a programme that states the assumption behind each causal link and the "
                  "evidence that would test it.", WS, attr="ATT-KNO", tasks=["seed:v1-3.2.3-T3"],
                  evidence=["theory of change"]),
                I("Prepares a resource plan matching staff and budget to strategic priorities, stating what will not be "
                  "done and why.", WS, attr="ATT-CPX", tasks=["seed:v1-3.2.4-T2"], evidence=["resource plan"],
                  v1=["v1:3.2.4:advanced:I5"]),
            ],
            "L4": [
                I("Runs a time-limited technology pilot with success criteria, recording the adoption decision and the "
                  "tasks kept with staff for accountability or formation.", PORT, attr="ATT-AUG", mode="supervisory",
                  tasks=["seed:v1-3.5.1-T2", "seed:v1-3.5.1-T3"], evidence=["pilot record"]),
                I("Sequences concurrent changes in a reorganization so that no unit exceeds its agreed change capacity in a "
                  "quarter, adjusting the schedule when a threshold is crossed.", PORT, attr="ATT-SCO",
                  tasks=["seed:v1-3.5.3-T1", "seed:v1-3.5.3-T2"], evidence=["change schedule"]),
                I("Leads a mission revision whose result is traceable to the programme's legal mandate and partners' stated "
                  "priorities.", PORT, attr="ATT-GUI", tasks=["seed:v1-3.2.2-T1", "seed:v1-3.2.2-T2"],
                  evidence=["mission statement", "trace table"]),
            ],
            "L5": [
                I("Sets an organization's change portfolio across programmes, ranking changes by legal requirement, mission "
                  "risk and cost of delay, with deferred items given review dates.", PORT, attr="ATT-SCO",
                  tasks=["seed:v1-3.5.3-T3"], evidence=["change portfolio"]),
                I("Reviews programme strategies against the organization's planning standard each year, returning each "
                  "with the gaps to close before approval.", RA, attr="ATT-GUI",
                  tasks=["seed:v1-3.2.2-T3", "seed:v1-3.2.1-T3"], evidence=["review comments"]),
                I("Coaches programme managers through strategy and change plans, reviewing each plan with them against the "
                  "organization's standard.", PORT, attr="ATT-FOR", obs4=2,
                  tasks=["seed:v1-3.2.4-T1"], evidence=["coaching record"]),
            ],
        },
    },
    # ------------------------------------------------------------------ v1-3.2.5
    {
        "id": "seed:v1-3.2.5", "agents": ["SC", "SL"], "adr": ADR_SC,
        "label": "Run the adaptive management cycle and evaluate programme performance",
        "alt": ["adaptive management", "performance monitoring and evaluation", "programme evaluation",
                "Conservation Standards", "impact measurement", "results reporting", "lessons learned"],
        "definition": "The capability to run plan, monitor, evaluate and adjust cycles for environmental programmes and "
                      "projects: set performance measures and decision triggers, use monitoring results to evaluate "
                      "effectiveness, adjust plans and work plans when triggers are met, record what was learned and "
                      "report results and spending transparently. Generic evaluation methods are referenced, not covered; "
                      "private project delivery metrics are a separate competency.",
        "statement": "Sets performance measures and decision triggers for a programme or project, uses monitoring results "
                     "and new science or stakeholder input to evaluate effectiveness, adjusts plans and annual work plans "
                     "when triggers are met, records lessons learned, and reports results and spending to funders and the "
                     "public in a form they can check.",
        "span": ("L2", "L4"),
        "sources": ["SC-042"],
        "editorial": "S2 close-out A (A5 SC with SL; reviewers A3 FC and A4 DC). Survivor of the adaptive management cycle "
                     "(ADR-0030 §3.1 M4): absorbs v1 3.1.5 (performance monitoring and evaluation) and the durable "
                     "remainder of 3.4.5 (results and spending transparency; its dashboards and platforms go to L4). Plan, "
                     "monitor, evaluate and adjust is one cycle in environmental programmes, as in the Conservation "
                     "Standards (altLabel). Generic programme evaluation referenced from O*NET/ESCO (G-8); private "
                     "delivery metrics stay with PS-C03. The 3.1.5 task seeds re-pointed by DE are rewritten here.",
        "sensitivity": [
            ("DM-19", "Grant and appropriation reporting terms set which performance measures a programme must report.",
             "J", None),
        ],
        "tasks": [
            T("seed:v1-3.2.5-T1", "Set decision triggers that tie monitoring results to specific management adjustments, "
              "recording who decides when a trigger is met", "WF-LEARN", formation="partial"),
            T("seed:v1-3.2.5-T2", "Revise a management plan when new science or stakeholder input changes an assumption, "
              "recording the evidence and the change made", "WF-LEARN", formation="partial"),
            T("seed:v1-3.2.5-T3", "Revise the annual work plan from the year's monitoring results, stating which results "
              "changed which activities", "WF-LEARN", formation="partial"),
            T("seed:v1-3.1.5-T1", "Design performance measures for a programme or project that separate outputs from "
              "outcomes, with a baseline and a data source for each", "WF-LEARN", formation="partial"),
            T("seed:v1-3.1.5-T2", "Analyze monitoring data against a project's milestones and outcome measures, stating "
              "where results fall short and the likely reason", "WF-LEARN", formation="partial"),
            T("seed:v1-3.1.5-T3", "Prepare a project's final evaluation and lessons-learned summary, separating what the "
              "project achieved from what changed for other reasons", "WF-LEARN", formation="partial"),
            T("seed:sc-report-results-spending", "Report a programme's results and spending to funders and the public in a "
              "form that lets readers trace each outcome claim to its data", "WF-LEARN", formation="no",
              derived=[("v1:3.4.5", "merged-from")]),
        ],
        "levels": {
            "L2": [
                I("Designs performance measures that separate outputs from outcomes, with a baseline and data source for "
                  "each, accepted by the programme lead.", WS, tasks=["seed:v1-3.1.5-T1"], evidence=["measures table"]),
                I("Revises the annual work plan from monitoring results, stating for each changed activity the result that "
                  "prompted it.", RA, tasks=["seed:v1-3.2.5-T3"], evidence=["revised work plan"]),
                I("Reports results and spending so that a reviewer can trace each outcome claim in a sampled report to its "
                  "data source.", RA, tasks=["seed:sc-report-results-spending"], evidence=["results report"]),
            ],
            "L3": [
                I("Sets decision triggers that tie monitoring results to named management adjustments, with the "
                  "decision-maker for each trigger recorded.", WS, attr="ATT-CPX", tasks=["seed:v1-3.2.5-T1"],
                  evidence=["trigger table"]),
                I("Prepares a final evaluation that separates project effects from other causes of change, stating the "
                  "evidence and its limits.", WS + PORT, attr="ATT-KNO", tasks=["seed:v1-3.1.5-T3"],
                  evidence=["evaluation report"]),
                I("Revises a management plan when new science changes an assumption, recording the evidence and the change, "
                  "accepted by the approving official.", WS, attr="ATT-AUT", tasks=["seed:v1-3.2.5-T2"],
                  evidence=["plan amendment"]),
            ],
            "L4": [
                I("Leads an adaptive management cycle with partners across agencies, documenting each adjustment made when "
                  "a trigger was met over a full cycle.", PORT, attr="ATT-SCO", obs4=2, tasks=["seed:v1-3.2.5-T1"],
                  evidence=["cycle record"]),
                I("Sets an organization's evaluation standard for programmes, with criteria applied in each annual review "
                  "and lessons carried into the next plan.", PORT, attr="ATT-GUI",
                  tasks=["seed:v1-3.1.5-T3", "seed:v1-3.2.5-T2"], evidence=["evaluation standard"]),
                I("Reviews staff measure and trigger designs against the standard before monitoring begins, returning each "
                  "with the changes required.", RA, attr="ATT-FOR",
                  tasks=["seed:v1-3.1.5-T1", "seed:v1-3.2.5-T1"], evidence=["review comments"]),
            ],
        },
    },
    # ------------------------------------------------------------------ v1-5.3.5
    {
        "id": "seed:v1-5.3.5", "agents": ["SC", "SL"], "adr": ADR_SC,
        "label": "Build working partnerships with communities affected by environmental decisions",
        "alt": ["environmental justice", "EJ", "community partnerships", "community organizing",
                "frontline community engagement", "community benefits"],
        "definition": "The capability to build and keep working relationships with communities that bear the effects of "
                      "environmental decisions, so that they shape priorities, analyses and actions over time: identifying "
                      "and reaching the people affected, sharing information and decision timelines, supporting "
                      "community-led action and keeping commitments. Distributional analysis and relations owed to other "
                      "governments are separate competencies.",
        "statement": "Identifies the communities that bear a decision's effects and who speaks for them, builds "
                     "relationships before decisions are framed, shares information and timelines in usable forms, "
                     "involves communities in setting priorities and reviewing analyses, supports community-led action, "
                     "and keeps and reports on the commitments made.",
        "span": ("L1", "L4"),
        "sources": ["DB-060", "WP05-001", "WP05-002", "WP05-003"],
        "editorial": "S2 close-out A (A5 SC with SL; reviewers TN (G-TN) and CP). Named by the work performed under "
                     "ADR-0016's uniform rule; environmental justice is a search alias only. Absorbs v1 5.6.3 (community "
                     "organizing), which becomes the advocate-position enactment. Distributional and cumulative-burden "
                     "analysis is DB-C52; discretionary engagement design is SC-C06; stakeholder analysis is v1 5.2.1. "
                     "Content specific to Tribal nations is held and separated (TN verdict; ADR-0007 §D): no Tribal "
                     "enactment is authored. Federal applicability is computed from typed links: the revoked federal "
                     "orders are requires links whose status is rescinded, and the revoking orders are "
                     "removed-requirement.",
        "sensitivity": [
            ("DM-04", "Federal orders that required engagement with affected communities were revoked in 2025, while "
                      "state cumulative-impact laws require it for covered permits.", "E", ["WP05-001", "WP05-002",
                                                                                           "WP05-003"]),
            ("DM-10", "State burden and siting standards make community input part of what a permit decision must "
                      "address.", "E", ["WP05-002", "WP05-003"]),
        ],
        "tasks": [
            T("seed:v1-5.3.5-T1", "Identify the communities that bear a proposed decision's effects and the organizations "
              "that speak for each, recording how each was identified", "WF-ASSESS", formation="partial",
              modes=["MODE-ENGAGE"], rel=["public"]),
            T("seed:v1-5.3.5-T2", "Engage affected communities before a decision is framed, recording the priorities they "
              "raise and how each was considered", "WF-PLAN", formation="yes", modes=["MODE-ENGAGE"], rel=["public"]),
            T("seed:v1-5.3.5-T3", "Set programme priorities with an affected community's representatives, recording the "
              "commitments made and the date each is due", "WF-PLAN", formation="yes", modes=["MODE-ENGAGE"],
              rel=["public"]),
            T("seed:v1-5.6.3-T1", "Recruit community members into an advisory or monitoring effort on an environmental "
              "issue, recording which outreach channels reached people", "WF-PLAN", formation="partial",
              modes=["MODE-ENGAGE"], rel=["public"]),
            T("seed:v1-5.6.3-T2", "Set up a standing structure for community participation, such as an advisory group, "
              "with its terms of reference and meeting cycle", "WF-PLAN", formation="partial", modes=["MODE-ENGAGE"],
              rel=["public"]),
            T("seed:v1-5.6.3-T3", "Support a community-led action on an environmental issue with the information, training "
              "or resources the community requests", "WF-PLAN", formation="partial", modes=["MODE-ENGAGE"],
              rel=["public"]),
            T("seed:sc-share-decision-information", "Share decision timelines and draft analyses with affected communities "
              "in formats and languages they can use, before comment periods open", "WF-REVIEW", formation="partial",
              modes=["MODE-ENGAGE"], rel=["public"]),
            T("seed:sc-report-on-commitments", "Report back to an affected community on each commitment made, stating "
              "whether it was kept, changed or dropped and why", "WF-REVIEW", formation="partial",
              modes=["MODE-ENGAGE"], rel=["public"]),
        ],
        "levels": {
            "L1": [
                I("Lists the communities affected by a seeded proposal and the organizations that speak for each, with the "
                  "source of each identification.", WS, tasks=["seed:v1-5.3.5-T1"], evidence=["community list"]),
                I("Logs each community concern raised and the response given, so that every item sampled in audit appears "
                  "with its date and source.", RA, tasks=["seed:v1-5.3.5-T2"], evidence=["concern log"]),
            ],
            "L2": [
                I("Holds a pre-decision session with an affected community and records the priorities raised and how each "
                  "was considered, which the community's representatives confirm as accurate.", C360 + RA,
                  attr="ATT-AUT", obs4=2, tasks=["seed:v1-5.3.5-T2"], evidence=["session record"]),
                I("Shares draft analyses with an affected community in a usable format and language before the comment "
                  "period opens, recording the questions raised.", WS + RA, attr="ATT-SCO",
                  tasks=["seed:sc-share-decision-information"], evidence=["information package", "question log"]),
                I("Reports back on each commitment made to a community, stating whether it was kept, changed or dropped and "
                  "why.", RA, attr="ATT-GUI", tasks=["seed:sc-report-on-commitments"], evidence=["commitment report"]),
            ],
            "L3": [
                I("Sets programme priorities with an affected community's representatives in a contested setting, "
                  "recording each commitment made and its due date.", PORT + C360, attr="ATT-CPX", obs4=2,
                  tasks=["seed:v1-5.3.5-T3"], evidence=["priority agreement"]),
                I("Sets up a standing participation structure with terms of reference that community members helped write, "
                  "meeting on its agreed cycle for a year.", PORT, attr="ATT-SCO", tasks=["seed:v1-5.6.3-T2"],
                  evidence=["terms of reference", "meeting record"]),
                I("Supports a community-led action with the information or resources the community requested, recording "
                  "each request and the response given.", RA, attr="ATT-AUT", tasks=["seed:v1-5.6.3-T3"],
                  evidence=["request log"]),
            ],
            "L4": [
                I("Sets an organization's policy for community partnerships, including how commitments are tracked and "
                  "reported, with an annual review of commitments kept.", PORT, attr="ATT-GUI",
                  tasks=["seed:sc-report-on-commitments"], evidence=["policy", "annual review"]),
                I("Reviews units' commitment records against the policy each quarter, returning each record with the "
                  "overdue commitments to resolve.", RA, attr="ATT-SCO", tasks=["seed:sc-report-on-commitments"],
                  evidence=["review record"]),
                I("Mentors staff through building community partnerships, reviewing each partnership's commitment record "
                  "with them.", PORT, attr="ATT-FOR", obs4=2, tasks=["seed:v1-5.3.5-T3"],
                  evidence=["mentoring record"]),
            ],
        },
        "enactments": [
            E("seed:ena-v1-5-3-5-federal", "Federal agency community engagement", "federal-agency",
              basis="Programme statutes and agency engagement procedures; the government-wide environmental-justice orders "
                    "that directed engagement with affected communities were revoked in January 2025, so the work rests on "
                    "programme authority and agency discretion.",
              principal="The responsible official for the programme or decision.",
              venue="Federal courts; inspectors general; Congress.",
              note="ADR-0016: applicability is computed. With the revoked orders linked as requires and the revoking orders "
                   "as removed-requirement, the federal value computes no-current-basis while the work stays possible; the "
                   "Q4 default shows the value with a note and excludes nothing.",
              links=[("eo-12898", R, "Revoked 2025-01-21 by EO 14173."),
                     ("eo-14096", R, "Revoked 2025-01-20 by EO 14148."),
                     ("eo-14173", X, "Revoking order; never a basis."),
                     ("eo-14148", X, "Revoking order; never a basis.")],
              evidence="E", sources=["WP05-001"]),
            E("seed:ena-v1-5-3-5-state", "State cumulative-impact permitting engagement", "state-agency",
              position="regulator",
              basis="State cumulative-impact and siting laws that require engagement with overburdened communities for "
                    "covered permits, for example New Jersey's law and rules and New York's siting law with its review "
                    "amendments.",
              principal="The state permitting agency.", venue="State administrative hearings; state courts.",
              note="SL review: engagement is a regulatory step here; community input enters the record the permit decision "
                   "must address [E: WP05-002, WP05-003].",
              links=[("nj-ej-law", R, None), ("ny-ecl-70-0118", R, None)], sl_reviewed=True, evidence="E",
              sources=["WP05-002", "WP05-003", "DB-060"]),
            E("seed:ena-v1-5-3-5-advocate", "Community organization or advocate", "community-organization",
              position="advocate",
              basis="No decision authority; organizing, participation rights in comment periods and hearings, and standing "
                    "where the law provides.",
              principal="The organization's members and board.", venue="Agency proceedings; courts.",
              note="Community organizing (v1 5.6.3) is this competency's advocate-position enactment: the same relationship "
                   "work, done from the community side [J]."),
        ],
    },
    # ------------------------------------------------------------------ v1-5.3.4-A
    {
        "id": "seed:v1-5.3.4-A", "agents": ["SC", "SL"], "adr": ADR_SC,
        "label": "Design accessible, inclusive public engagement and services",
        "alt": ["accessibility accommodations", "diversity, equity and inclusion in public engagement", "DEI",
                "language access", "universal design of public programmes", "inclusive engagement"],
        "definition": "The capability to design public engagement, programmes, facilities and information so that every "
                      "affected or eligible member of the public can find, reach, understand and take part in them, "
                      "including people with disabilities and people with limited proficiency in the main language, and to "
                      "check participation for groups the design is not reaching. Deciding when to engage beyond legal "
                      "minimums is a separate competency.",
        "statement": "Designs engagement, services, facilities and information so that affected and eligible people can "
                     "find, reach, understand and take part in them: meets accessibility standards, provides "
                     "accommodations, interpretation and translation, chooses times, places and channels that fit the "
                     "people affected, and checks participation for groups not being reached.",
        "span": ("L1", "L4"),
        "derived": [("v1:5.3.4", "split-from")],
        "sources": ["SC-038", "WP05-001"],
        "editorial": "S2 close-out A (A5 SC with SL; reviewers A8 IO and CP; CA spot-check before WP-12 renders any federal "
                     "value, CR-SC-001 ruling item 2). Split target A of v1 5.3.4 (with v1-5.3.4-B); absorbs v1 5.5.5 "
                     "(accessibility accommodations), whose task seeds are rewritten here; v1 5.3.4-T1 is re-pointed here. "
                     "Named by the work performed under ADR-0016; DEI is a search alias only. Pairs with SC-C06 "
                     "(proportionate engagement when participation is discretionary). Typed links: the revoking orders "
                     "are linked as removed-requirement; the accessibility and language-access instruments that are the "
                     "current federal basis are not registered yet, so the federal value reads 'basis not yet linked' "
                     "(requested from LM in docs/build/S2-closeout-A/instruments_to_register.csv).",
        "sensitivity": [
            ("DM-04", "Where required public involvement shrinks, the accessibility of the engagement that remains is a "
                      "design choice that must be defended.", "E", ["SC-038"]),
            ("DM-10", "Accessibility standards for facilities, trails and digital services set minimum requirements for "
                      "public programmes.", "J", None),
        ],
        "tasks": [
            T("seed:v1-5.5.5-T1", "Check facilities, trails and public materials against the applicable accessibility "
              "standards, recording each barrier found and the fix scheduled", "WF-ASSESS",
              field="on-site-preferred", formation="partial", derived=[("v1:5.5.5:T1", "rewritten")]),
            T("seed:v1-5.5.5-T2", "Provide adaptive equipment, interpretation or an alternative format when a participant "
              "requests it, recording the request and the response time", "WF-OPERATE", field="on-site-preferred",
              formation="no", modes=["MODE-ENGAGE"], rel=["public"], derived=[("v1:5.5.5:T2", "rewritten")]),
            T("seed:v1-5.5.5-T3", "Include accessibility and language-access needs in a programme or engagement plan, "
              "budgeting the accommodations that expected participants will need", "WF-PLAN", formation="no",
              derived=[("v1:5.5.5:T3", "rewritten")]),
            T("seed:v1-5.3.4-T1", "Compare participation in a programme or engagement process with the population it "
              "serves, identifying the groups that the design is not reaching", "WF-ASSESS", formation="partial",
              derived=[("v1:5.3.4:T1", "rewritten")]),
            T("seed:sc-plan-language-access", "Plan interpretation and translation for an engagement process from the "
              "languages spoken in the affected area, stating which materials will be translated", "WF-REVIEW",
              formation="no", modes=["MODE-ENGAGE"], rel=["public"]),
            T("seed:sc-choose-engagement-channels", "Choose meeting times, places and channels for an engagement process "
              "that fit the work schedules, transport and connectivity of the people affected", "WF-REVIEW",
              formation="partial", modes=["MODE-ENGAGE"], rel=["public"]),
        ],
        "levels": {
            "L1": [
                I("Records each accessibility barrier found in a checklist inspection of a facility or trail against the "
                  "applicable standard, with its location and a photograph.", TBO + RA, tasks=["seed:v1-5.5.5-T1"],
                  evidence=["inspection checklist"]),
                I("Provides a requested alternative format or interpretation within the programme's stated response time "
                  "in a seeded request.", WS, tasks=["seed:v1-5.5.5-T2"], evidence=["request log"]),
            ],
            "L2": [
                I("Writes the accessibility and language-access section of an engagement plan, with accommodations "
                  "budgeted, accepted by the responsible official.", WS, attr="ATT-AUT",
                  tasks=["seed:v1-5.5.5-T3", "seed:sc-plan-language-access"], evidence=["plan section"]),
                I("Compares participation with the served population using available data and names the groups not "
                  "reached, stating the data's limits.", WS, attr="ATT-KNO", tasks=["seed:v1-5.3.4-T1"],
                  evidence=["participation analysis"]),
                I("Chooses meeting times, places and channels for a seeded case that fit the affected people's schedules, "
                  "transport and connectivity, justifying each choice.", WS, attr="ATT-CPX",
                  tasks=["seed:sc-choose-engagement-channels"], evidence=["engagement logistics plan"]),
            ],
            "L3": [
                I("Redesigns an engagement process after a participation check shows groups not reached, recording what "
                  "changed and the participation that followed.", PORT, attr="ATT-CPX", obs4=2,
                  tasks=["seed:v1-5.3.4-T1", "seed:sc-choose-engagement-channels"], evidence=["redesign record"]),
                I("Plans language access for a multilingual affected area, with translated materials and interpreters "
                  "matched to the languages documented in the plan.", WS, attr="ATT-SCO",
                  tasks=["seed:sc-plan-language-access"], evidence=["language-access plan"]),
                I("Schedules fixes for every barrier found in a facility or programme audit, ranked by the number of people "
                  "excluded and the cost of the fix.", WS + RA, attr="ATT-GUI", tasks=["seed:v1-5.5.5-T1"],
                  evidence=["fix schedule"]),
            ],
            "L4": [
                I("Sets an organization's accessibility and language-access standards for engagement and services, with "
                  "criteria units apply and an annual review of participation.", PORT, attr="ATT-GUI",
                  tasks=["seed:v1-5.5.5-T3"], evidence=["standard", "annual review"]),
                I("Reviews units' engagement plans against the organization's accessibility standard, returning each with "
                  "the changes required before launch.", RA, attr="ATT-FOR",
                  tasks=["seed:v1-5.5.5-T3", "seed:sc-plan-language-access"], evidence=["plan reviews"]),
            ],
        },
        "enactments": [
            E("seed:ena-v1-5-3-4-a-federal", "Federal programmes, facilities and engagement", "federal-agency",
              basis="Federal disability-rights law for federally conducted programmes, facilities and electronic "
                    "information; agency language-access policies; the executive orders that directed meaningful "
                    "engagement with affected communities on environmental decisions were revoked in January 2025.",
              principal="The responsible official for the programme or decision.",
              venue="Agency civil-rights offices; federal courts.",
              note="ADR-0016: applicability is computed. The revoking orders are linked as removed-requirement and never "
                   "decide the value; the disability-rights and language-access instruments are not yet registered, so "
                   "the federal value reads 'basis not yet linked' until LM registers them.",
              links=[("eo-14173", X, "Revoked EO 12898, whose participation and translation provisions applied to "
                                     "environmental decisions; never a basis."),
                     ("eo-14148", X, "Revoked EO 14096 and its engagement provisions; never a basis.")],
              evidence="E", sources=["WP05-001"]),
            E("seed:ena-v1-5-3-4-a-local", "Local government services and meetings", "county",
              basis="State and local government duties under federal disability law for programmes, services and websites; "
                    "state open-meeting laws and state or local language-access requirements where they exist.",
              principal="The department head or governing board.",
              venue="Federal and state civil-rights enforcement; courts.",
              note="SL review: local programmes run most public meetings and parks, so accessibility and language access "
                   "are routine local design work [J].", sl_reviewed=True),
        ],
    },
]

# ------------------------------------------------------------------ SC-C02 additions (ADR-0030 §3.1 M5)
SC_C02 = {
    "definition_old": "so that a court, inspector general or successor can reconstruct why the decision was reasonable.",
    "definition": "The capability to document the reasons for a decision as it is made, including alternatives, "
                  "boundaries, responses to substantive comments, consultation outcomes and the provenance of analyses "
                  "(AI-assisted content included), so that a court, inspector general or successor can reconstruct why "
                  "the decision was reasonable, and to keep those records intact, retained and disclosable under "
                  "retention schedules, litigation holds and public-records laws.",
    "derived": [("v1:3.3.5", "merged-from"), ("v1:2.5.2", "merged-from")],
    "sources": [],
    "editorial": "S2 close-out A (A5 SC; reviewer A4 DC, DC-CAND-07 boundary; ADR-0030 §3.1 M5): absorbs v1 3.3.5 "
                 "(records management) and, through it, 2.5.2 (collaborative document management). Records integrity, "
                 "retention, litigation holds and public-records disclosure attach to the decision record; the definition "
                 "gains one clause. Generic filing-system design is referenced (G-8) and tool training goes to L4; the six "
                 "re-pointed task seeds are rewritten to the durable record work. Protecting sensitive information inside "
                 "data products stays with DC-CAND-07.",
    "tasks": [
        T("seed:v1-3.3.5-T1", "Set up a project's file plan for documents, maps and permits, assigning each record series "
          "its retention schedule", "WF-MANAGE", formation="no", primary="seed:SC-C02"),
        T("seed:v1-3.3.5-T2", "Apply records retention schedules and privacy rules to programme files, documenting each "
          "disposal or hold decision", "WF-MANAGE", formation="no", primary="seed:SC-C02"),
        T("seed:v1-3.3.5-T3", "Train staff on retention schedules, litigation holds and public-records request procedures, "
          "testing their handling of sample requests", "WF-LEARN", formation="no", primary="seed:SC-C02"),
        T("seed:v1-2.5.2-T1", "Keep version control on documents that enter a decision record, so that each cited version "
          "can be retrieved with its date and author", "WF-MANAGE", formation="no", primary="seed:SC-C02"),
        T("seed:v1-2.5.2-T2", "Track the changes that outside partners make to a jointly drafted plan or report, recording "
          "who changed what before it enters the record", "WF-MANAGE", formation="no", primary="seed:SC-C02"),
        T("seed:v1-2.5.2-T3", "Apply the programme's naming and access rules to record files, so that auditors and "
          "successors can find each document and see who could change it", "WF-MANAGE", formation="no",
          primary="seed:SC-C02"),
        T("seed:sc-respond-records-request", "Respond to a public-records request for programme records, reviewing each "
          "document for exempt content and recording the basis for each withholding", "WF-MANAGE", formation="partial",
          modes=["MODE-ENGAGE"], rel=["public"], primary="seed:SC-C02"),
        T("seed:sc-place-litigation-hold", "Place a litigation hold on the records of a challenged decision, notifying each "
          "custodian and suspending scheduled disposal until counsel releases it", "WF-MANAGE", formation="partial",
          modes=["MODE-RESOLVE"], primary="seed:SC-C02"),
    ],
    "indicators": {
        "L1": [I("Applies the retention schedule to a sample of programme files, documenting each disposal or hold "
                 "decision, with no record under hold disposed of.", RA, tasks=["seed:v1-3.3.5-T2"],
                 evidence=["disposition log"], critical=True)],
        "L2": [I("Responds to a seeded public-records request by its deadline, citing an exemption for each withholding "
                 "and withholding no releasable record.", SEW, attr="ATT-KNO", tasks=["seed:sc-respond-records-request"],
                 evidence=["response package"], critical=True)],
        "L3": [I("Places a litigation hold on a challenged decision's records, notifying every custodian and suspending "
                 "scheduled disposal within the time counsel sets.", RA, attr="ATT-AUT",
                 tasks=["seed:sc-place-litigation-hold"], evidence=["hold notice", "custodian list"], critical=True)],
    },
}
