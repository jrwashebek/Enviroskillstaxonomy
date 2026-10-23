"""S2 close-out A content, A5 SC rows due by S3: v1-6.2.5 (policy and land-use scenario development; boundary with
DC-CAND-12 operational forecast systems and FS-C15 horizon scanning) and v1-5.3.1 (observable cultural humility,
separate from relations owed to other governments and from the DEI/EJ items; Tribal-specific indicators held, none
authored here)."""
from s2adsl import T, I, WS, RA, SIM, PORT, C360, TBO

ADR_SC = ["ADR-0003", "ADR-0004", "ADR-0007", "ADR-0016", "ADR-0017", "ADR-0025", "ADR-0030"]

COMPETENCIES = [
    # ------------------------------------------------------------------ v1-6.2.5
    {
        "id": "seed:v1-6.2.5", "agents": ["SC"], "adr": ADR_SC,
        "label": "Develop and compare policy and land-use scenarios for environmental decisions",
        "alt": ["scenario planning", "scenario analysis", "alternative futures", "land-use scenarios",
                "participatory scenario planning"],
        "definition": "The capability to build a small set of plausible future conditions for a planning area or policy "
                      "question, under varying ecological, social and economic drivers, and to compare how management or "
                      "policy alternatives perform across them so that decision-makers see trade-offs and choices that "
                      "hold up. Operational forecast systems and organizational horizon scanning are separate competencies.",
        "statement": "Defines the question, drivers and uncertainties for a planning area or policy choice; builds "
                     "contrasting, plausible scenarios with stakeholders; models or estimates how alternatives perform "
                     "under each; shows the trade-offs in maps and tables decision-makers can use; and states which "
                     "alternatives perform acceptably across every scenario.",
        "span": ("L2", "L4"),
        "editorial": "S2 close-out A (A5 SC; reviewers A4 DC and FS). Kept as policy and land-use scenario analysis (FS "
                     "verdict). Boundaries: DC-CAND-12 builds, runs and validates operational forecast and scenario "
                     "systems (the model infrastructure); FS-C15 scans horizons and turns change signals into workforce "
                     "decisions (ADR-0025 §4). Here the deliverable is a comparison of decision alternatives across "
                     "scenarios.",
        "sensitivity": [
            ("DM-01", "What effects and alternatives a review must cover decides whether scenario comparisons are "
                      "required or discretionary in plans and reviews.", "J", None),
        ],
        "tasks": [
            T("seed:v1-6.2.5-T1", "Model future land-use conditions for a planning area under contrasting scenarios, "
              "documenting the drivers, assumptions and data behind each", "WF-PLAN", formation="partial"),
            T("seed:v1-6.2.5-T2", "Run a participatory scenario workshop in which stakeholders define the drivers and "
              "uncertainties that the scenarios will vary", "WF-PLAN", formation="partial", modes=["MODE-ENGAGE"],
              rel=["stakeholder"]),
            T("seed:v1-6.2.5-T3", "Present scenario results in maps and comparison tables that show each alternative's "
              "outcomes under every scenario", "WF-PLAN", formation="no"),
            T("seed:sc-identify-robust-alternatives", "Identify the alternatives that perform acceptably under every "
              "scenario, stating the threshold used and the trade-offs of each", "WF-PLAN", formation="partial"),
        ],
        "levels": {
            "L2": [
                I("Models land-use outcomes under at least three contrasting scenarios, documenting each scenario's "
                  "drivers and assumptions for review.", WS, tasks=["seed:v1-6.2.5-T1"], evidence=["scenario model run"]),
                I("Presents scenario results in maps and tables that let a reviewer compare every alternative under every "
                  "scenario without further analysis.", WS, tasks=["seed:v1-6.2.5-T3"], evidence=["comparison tables"]),
            ],
            "L3": [
                I("Runs a scenario workshop in which participants set the drivers and uncertainties, recording how each was "
                  "chosen.", SIM + PORT, attr="ATT-AUT", tasks=["seed:v1-6.2.5-T2"], evidence=["workshop record"]),
                I("Identifies the alternatives that meet a stated threshold under every scenario and states their "
                  "trade-offs, accepted by the decision-maker as the basis for comparison.", WS, attr="ATT-CPX",
                  tasks=["seed:sc-identify-robust-alternatives"], evidence=["robustness table"]),
            ],
            "L4": [
                I("Designs the scenario process for a contested planning decision across agencies, linking scenario "
                  "outputs to the decision's alternatives and record.", PORT, attr="ATT-SCO",
                  tasks=["seed:v1-6.2.5-T2", "seed:sc-identify-robust-alternatives"], evidence=["process design"]),
                I("Reviews staff scenario analyses against the organization's method standard, returning each with the "
                  "assumptions to justify before release.", RA, attr="ATT-FOR",
                  tasks=["seed:v1-6.2.5-T1"], evidence=["review comments"]),
            ],
        },
    },
    # ------------------------------------------------------------------ v1-5.3.1
    {
        "id": "seed:v1-5.3.1", "agents": ["SC"], "adr": ADR_SC,
        "label": "Practise cultural humility in community, field and team work",
        "alt": ["cross-cultural communication", "cultural competence", "cultural protocols", "cultural humility"],
        "definition": "The capability to recognize that one's own cultural assumptions shape how one communicates and "
                      "works, to seek and follow the norms and protocols of the people one works with, and to change "
                      "conduct when told it caused harm, in meetings, site visits and teams. Relations owed to other "
                      "governments and inclusive programme design are separate competencies.",
        "statement": "Asks about and follows the communication norms and protocols of the communities and colleagues one "
                     "works with, adapts language and meeting practice to them, seeks guidance from the people a community "
                     "recognizes as cultural advisers before engagement or site visits, and changes conduct when told it "
                     "caused offence or harm.",
        "span": ("L1", "L3"),
        "editorial": "S2 close-out A (A5 SC; reviewer TN (G-TN)). Reframed as observable cultural humility (TN verdict; "
                     "ADR-0016 §5): separate from relations owed to other governments, which are held content (ADR-0007 "
                     "§D), and from the inclusive-engagement and community-partnership items (v1 5.3.4-A, 5.3.5). "
                     "Indicators specific to Tribal nations are held and not authored here; TN may add them inside the "
                     "hold as enactment variants.",
        "tasks": [
            T("seed:v1-5.3.1-T1", "Adapt the language, format and pace of a meeting or field briefing to the communication "
              "norms of the people attending", "WF-REVIEW", formation="partial", modes=["MODE-ENGAGE"],
              rel=["public"]),
            T("seed:v1-5.3.1-T2", "Ask a community's recognized cultural advisers about norms and protocols before planning "
              "an engagement or site visit, recording the guidance given", "WF-REVIEW", formation="partial",
              modes=["MODE-ENGAGE"], rel=["public"]),
            T("seed:v1-5.3.1-T3", "Follow the protocols a community has stated for meetings and site visits, such as "
              "permissions, timing and places not to enter", "WF-ASSESS", field="on-site-preferred",
              formation="yes", modes=["MODE-ENGAGE"], rel=["public"]),
            T("seed:sc-change-conduct-after-feedback", "Change one's conduct after a community member or colleague says it "
              "caused offence or harm, recording the feedback and the change made", "WF-REVIEW", formation="yes",
              modes=["MODE-ENGAGE"]),
        ],
        "levels": {
            "L1": [
                I("Asks a community's recognized advisers about norms before a site visit and records the guidance, with no "
                  "guidance item missed in the post-visit review.", RA, tasks=["seed:v1-5.3.1-T2"],
                  evidence=["guidance record"]),
                I("Follows a community's stated permissions and timing during a site visit, as observed by the supervising "
                  "lead.", TBO, tasks=["seed:v1-5.3.1-T3"], evidence=["observation record"]),
            ],
            "L2": [
                I("Adapts the language, format and pace of a meeting to the norms the community's advisers stated, with each "
                  "requested adaptation confirmed in structured feedback from the community's representatives.", C360, attr="ATT-AUT", obs4=2,
                  tasks=["seed:v1-5.3.1-T1"], evidence=["structured feedback"]),
                I("Records the meeting adaptations made for a community and the advisers' guidance behind each, so that a "
                  "colleague can repeat them.", RA, attr="ATT-KNO",
                  tasks=["seed:v1-5.3.1-T1", "seed:v1-5.3.1-T2"], evidence=["adaptation record"]),
                I("Changes conduct after feedback that it caused offence, recording the feedback and the change, confirmed "
                  "by the person who raised it.", C360 + RA, attr="ATT-GUI",
                  tasks=["seed:sc-change-conduct-after-feedback"], evidence=["feedback record"]),
            ],
            "L3": [
                I("Prepares a team's briefing on a community's stated norms and protocols before engagement, checked with "
                  "the community's advisers before use.", PORT + RA, attr="ATT-SCO",
                  tasks=["seed:v1-5.3.1-T2"], evidence=["team briefing"]),
                I("Reviews a team's site-visit records against the community's stated protocols, recording each lapse and "
                  "the corrective step agreed.", RA, attr="ATT-FOR",
                  tasks=["seed:v1-5.3.1-T3", "seed:sc-change-conduct-after-feedback"], evidence=["review record"]),
            ],
        },
    },
]
