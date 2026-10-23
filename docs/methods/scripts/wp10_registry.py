"""WP-10 L5 instrument registry and dated driver events.

Seeds: SC's 34 instruments (docs/research/statecraft/policy_landscape_2026.csv) as corrected by the V2/V4
verification pass (docs/research/_verification/), plus the instruments WP-10 names (Section 106 regulations,
Colorado SB 26-189, OFCCP rescission of 41 CFR 60-3, OPM interim final rule removing UGESP references) and
verified FH/FC/SL/fiscal events (ADR-0028 s3). currentStatus is NOT stored: it is computed from events.

Every event date here traces to a verified fact (V1-xx, V2-xx, V3-xx, V4 register rows) or to an SC/FS source
row; events that rest only on SC/FS rows and were not re-verified say so in editorialNote and carry the
pending re-check date.
"""
from wp10_common import base, provenance, slug, RECHECK_PENDING, RECHECK_SETTLED, RECHECK_HISTORIC

# statusAfter values used (proposed vocabulary in CR-LM-001):
STATUS_AFTER = ["pending-legislation", "proposed", "interim-in-force", "final-not-yet-effective", "in-force",
                "in-force-litigated", "enjoined", "stayed", "vacated", "rescinded", "repealed", "issued"]

# Each instrument: key, sc (SC instrument_id or None), label, citation, itype, juris, mech, src, held, note, events
# Each event: (eventType, date, direction, statusAfter, sources, evidenceLabel, reviewBy, note)
I = []


def add(key, sc, label, citation, itype, juris, mech, src, events, note=None, held=False):
    I.append(dict(key=key, sc=sc, label=label, citation=citation, itype=itype, juris=juris, mech=mech,
                  src=src, events=events, note=note, held=held))


P, S, H = RECHECK_PENDING, RECHECK_SETTLED, RECHECK_HISTORIC

# ---------------------------------------------------------------- NEPA and review procedure
add("nepa-fra-2023", "PI-NEPA-01", "NEPA as amended by the Fiscal Responsibility Act of 2023",
    "42 U.S.C. 4321 et seq., as amended by P.L. 118-5 (2023)", "statute", "US", ["DM-02", "DM-05"],
    ["SC-010", "SC-012"],
    [("enacted", "2023-06-03", "reshapes", "in-force", ["SC-010"], "J", H,
      "Statutory page limits and deadlines; one-document and lead-agency provisions. Day of signing is J (SC rows give June 2023).")])
add("ceq-nepa-regs-removal", "PI-NEPA-02", "Removal of CEQ NEPA implementing regulations (40 CFR 1500-1508)",
    "90 FR 10610 (interim final rule); 91 FR 618 (final rule)", "regulation", "US", ["DM-01", "DM-04", "DM-05"],
    ["LM-101", "SC-011", "SC-040"],
    [("interim", "2025-02-25", "contracts", "final-not-yet-effective", ["LM-101"], "E", H, "Interim final rule published (V2-01)."),
     ("effective", "2025-04-11", "contracts", "interim-in-force", ["LM-101"], "E", H, "Interim removal effective (V2-01)."),
     ("final", "2026-01-08", "contracts", "in-force", ["LM-101"], "E", S,
      "Adopted as final without change, effective 2026-01-08 (V2-01). Agencies follow their own procedures.")])
add("ceq-nepa-guidance-2025", "PI-NEPA-03", "CEQ guidance to agencies on NEPA procedures and procedures template",
    "CEQ memorandum (2025-02-19); revised guidance and template, 90 FR 47734", "guidance", "US", ["DM-02", "DM-05"],
    ["LM-101", "SC-011", "SC-040"],
    [("final", "2025-02-19", "reshapes", "issued", ["SC-011", "SC-040"], "E", H, "Initial memorandum (SC rows)."),
     ("final", "2025-10-02", "reshapes", "issued", ["LM-101"], "E", S, "Revised guidance and template (cited in V2-01).")])
add("doi-nepa-procedures", "PI-NEPA-04", "Department of the Interior NEPA procedures and the DOI NEPA Handbook",
    "43 CFR part 46 (slimmed) and 'Department of the Interior Handbook: National Environmental Policy Act Implementing Procedures'; 91 FR 8738",
    "regulation", "US", ["DM-01", "DM-04", "DM-05"], ["LM-102", "SC-014"],
    [("interim", "2025-07-03", "reshapes", "interim-in-force", ["SC-014"], "E", H, "Interim rule (SC row)."),
     ("final", "2026-02-24", "reshapes", "in-force", ["LM-102"], "E", S,
      "Final rule effective on publication; most procedures moved to the DOI NEPA Handbook (not '516 DM 1') (V2-01).")])
add("usda-nepa-procedures", "PI-NEPA-05", "USDA NEPA procedures (7 CFR part 1b); Forest Service 36 CFR part 220 rescinded",
    "7 CFR part 1b; FR Doc 2026-06537", "regulation", "US", ["DM-02", "DM-03"], ["LM-103", "SC-009"],
    [("final", "2026-04-03", "reshapes", "in-force", ["LM-103"], "E", S,
      "Published and effective 2026-04-03; applies to CEs immediately, EAs published after 2026-05-18, EISs with NOI after 2026-07-02 (V2-01). FR page number unconfirmed; cite FR Doc.")])
add("dot-nepa-procedures", "PI-NEPA-06", "Department of Transportation NEPA procedures",
    "DOT NEPA implementing procedures (final rule)", "regulation", "US", ["DM-02", "DM-03", "DM-05"], ["SC-009", "SC-011"],
    [("final", "2026-09-01", "reshapes", "in-force", ["SC-009"], "E", P,
      "Date from SC row; not re-verified in V2. Split from SC's grouped PI-NEPA-06.")],
    note="SC grouped several agencies' procedures in PI-NEPA-06; WP-10 seeds one instrument per agency so status computes per instrument.")
add("epa-nepa-procedures", "PI-NEPA-06", "Environmental Protection Agency NEPA procedures",
    "EPA NEPA implementing procedures (proposed rule)", "regulation", "US", ["DM-02", "DM-03"], ["SC-009", "SC-011"],
    [("proposed", "2026-06-25", "reshapes", "proposed", ["SC-009"], "E", P, "Date from SC row; not re-verified in V2.")])
add("seven-county", "PI-NEPA-07", "Seven County Infrastructure Coalition v. Eagle County",
    "Seven County Infrastructure Coalition v. Eagle County, No. 23-975 (U.S. 2025)", "court-decision", "US",
    ["DM-01", "DM-08"], ["LM-104", "SC-012"],
    [("decided", "2025-05-29", "contracts", "in-force", ["LM-104"], "E", H,
      "8-0 judgment (reversed and remanded); 5-justice majority opinion; 3 concurred in the judgment; Gorsuch did not participate (V2-02). Not '5-3'.")])
add("nepa-s112-fee", "PI-NEPA-08", "NEPA section 112 project-sponsor opt-in fee for expedited review",
    "42 U.S.C. 4336f as added by P.L. 119-21 (One Big Beautiful Bill Act)", "statute", "US", ["DM-02", "DM-15"],
    ["LM-106", "SC-013"],
    [("enacted", "2025-07-04", "reshapes", "in-force", ["LM-106", "SC-013"], "E", S,
      "125% fee for 180-day EA / 1-year EIS deadlines (statute as summarized by counsel); no public count of projects using it (V2-04). Does not speed ESA or NHPA reviews.")])
add("speed-act", "PI-NEPA-09", "SPEED Act (H.R. 4776)", "H.R. 4776, 119th Congress", "statute", "US",
    ["DM-01", "DM-03", "DM-04", "DM-08"], ["LM-105", "SC-010"],
    [("passed-chamber", "2025-12-18", "contracts", "pending-legislation", ["LM-105"], "E", P,
      "Passed House 221-196 (Roll Call 356); referred to Senate EPW the same day; no later action (V2-03). Not law. Senate S. 3224 differs (not checked).")])
add("fast-41", "PI-NEPA-10", "FAST-41 (Title 41 of the FAST Act) and the Federal Permitting Improvement Steering Council",
    "42 U.S.C. 4370m et seq.; P.L. 114-94", "statute", "US", ["DM-02", "DM-05"], ["SC-010", "SC-009"],
    [("enacted", "2015-12-04", "reshapes", "in-force", ["SC-010"], "J", H, "Historic baseline; signing day is J.")])

# ---------------------------------------------------------------- permitting technology and AI governance
add("permitting-tech-pm-2025", "PI-TECH-01", "Presidential Memorandum 'Updating Permitting Technology for the 21st Century'",
    "Presidential Memorandum of 2025-04-15", "memo", "US", ["DM-14"], ["LM-110", "SC-037"],
    [("final", "2025-04-15", "expands", "in-force", ["LM-110"], "E", S, "Signed 2025-04-15 (V2-08).")])
add("permitting-tech-action-plan", "PI-TECH-01", "CEQ Permitting Technology Action Plan",
    "CEQ Permitting Technology Action Plan (2025-05-30)", "guidance", "US", ["DM-14"], ["LM-110", "SC-037"],
    [("final", "2025-05-30", "expands", "issued", ["LM-110"], "E", S,
      "Minimum functional requirements, initial data standard, roadmap, governance (V2-08). Split from SC's PI-TECH-01.")])
add("ceq-permitting-data-standard", "PI-TECH-02", "CEQ NEPA and Permitting Data and Technology Standard",
    "NEPA and Permitting Data and Technology Standard, v1.2", "standard-with-legal-force", "US", ["DM-14"], ["LM-110", "SC-009"],
    [("final", "2025-08-18", "expands", "in-force", ["LM-110"], "E", S,
      "Version 1.2 published 2025-08-18; no newer version as of 2026-10-21; say 'v1.2' (V2-08). Licence not stated on the standard page.")],
    note="Adoption is directed by the 2025-04-15 memorandum, hence standard-with-legal-force. Its L4 technical-standard entry belongs to DC (WP-04).")
add("epermit-act", "PI-TECH-03", "ePermit Act (H.R. 4503)", "H.R. 4503, 119th Congress", "statute", "US", ["DM-14"],
    ["SC-015", "SC-016", "SC-017"],
    [("passed-chamber", "2025-12-09", "expands", "pending-legislation", ["SC-016", "SC-017"], "E", P,
      "Passed House unanimously (SC rows; not re-verified in V2). Senate companion introduced by Feb 2026.")])
add("omb-m-25-21", "PI-AI-01", "OMB M-25-21 Accelerating Federal Use of AI through Innovation, Governance, and Public Trust",
    "OMB Memorandum M-25-21 (replaced M-24-10)", "memo", "US", ["DM-14"], ["LM-111", "SC-037"],
    [("final", "2025-04-03", "reshapes", "in-force", ["LM-111"], "E", S, "Issued 2025-04-03, replacing M-24-10 (V2-09).")])
add("omb-m-25-22", None, "OMB M-25-22 Driving Efficient Acquisition of Artificial Intelligence in Government",
    "OMB Memorandum M-25-22 (replaced M-24-18)", "memo", "US", ["DM-14"], ["LM-111"],
    [("final", "2025-04-03", "reshapes", "in-force", ["LM-111"], "E", S,
      "Issued 2025-04-03; applies to solicitations from about 180 days after issuance; bars training on non-public agency data without consent (V2-09).")])
add("omb-m-26-04", None, "OMB M-26-04 Increasing Public Trust in AI Through Unbiased AI Principles (LLM procurement terms)",
    "OMB Memorandum M-26-04 (implements EO 14319)", "memo", "US", ["DM-14"], ["LM-111"],
    [("final", "2025-12-11", "reshapes", "in-force", ["LM-111"], "E", S,
      "Dated 2025-12-11 (not January 2026); agency procurement policy updates due 2026-03-11; sunsets two years after issuance unless extended (V2-09).")])
add("dol-ai-literacy-framework", None, "DOL Artificial Intelligence Literacy Framework (ETA TEN 07-25)",
    "Training and Employment Notice 07-25", "guidance", "US", ["DM-14", "DM-19"], ["LM-140"],
    [("final", "2026-02-13", "expands", "issued", ["LM-140"], "E", S,
      "Official content areas: Understand AI Principles; Explore AI Uses; Direct AI Effectively; Evaluate AI Outputs; Use AI Responsibly (DC-016 correction).")])

# ---------------------------------------------------------------- ESA, CWA, CAA, NHPA
add("esa-harm-rescission", "PI-ESA-01", "Rescission of the ESA regulatory definition of 'harm'",
    "50 CFR 17.3 and 222.102; 91 FR 43300", "regulation", "US", ["DM-06", "DM-10"], ["LM-107", "SC-018"],
    [("proposed", "2025-04-17", "contracts", "proposed", ["LM-107"], "E", H, "Proposed at 90 FR 16102 (V2-05)."),
     ("final", "2026-07-14", "contracts", "final-not-yet-effective", ["LM-107"], "E", S, "Final rule published (V2-05)."),
     ("effective", "2026-09-14", "contracts", "in-force-litigated", ["LM-107"], "E", P,
      "Effective 2026-09-14 (not 2026-09-12). Suits filed in W.D. Wash. in mid-July 2026 (V2-05). Prospective only; s.7 adverse-modification duties and critical habitat designations unchanged.")])
add("esa-4d-4b2-rules", "PI-ESA-02", "ESA blanket 4(d) rule elimination and section 4(b)(2) critical-habitat exclusions rule",
    "50 CFR 17.31 and 17.90", "regulation", "US", ["DM-06", "DM-10"], ["SC-019"],
    [("final", "2026-07-21", "contracts", "final-not-yet-effective", ["SC-019"], "E", P, "SC row; not re-verified in V2."),
     ("effective", "2026-08-20", "contracts", "in-force", ["SC-019"], "E", P, "SC row; not re-verified in V2.")])
add("esa-s4-s7-regs-2025", "PI-ESA-03", "ESA section 4 and section 7 regulations restoring the 2019 framework (proposed)",
    "50 CFR parts 402 and 424 (proposed revisions)", "regulation", "US", ["DM-06"], ["SC-020"],
    [("proposed", "2025-11-19", "contracts", "proposed", ["SC-020"], "E", P,
      "Announcement date per FWS press release; FR publication date (2025-11-19/21) not confirmed; final not confirmed as of 2026-10-23.")])
add("wotus-definition", "PI-CWA-01", "Clean Water Act 'waters of the United States' definition (post-Sackett revision)",
    "33 CFR 328.3 and 40 CFR 120.2 (proposed revisions)", "regulation", "US", ["DM-09"], ["LM-109", "SC-023"],
    [("proposed", "2025-11-20", "contracts", "proposed", ["LM-109"], "E", P, "FR Doc 2025-20402 (V2-07)."),
     ("proposed", "2026-09-09", "contracts", "proposed", ["LM-109"], "E", P,
      "Supplemental proposal FR Doc 2026-18317; comments due 2026-10-09; no final rule as of Oct 2026 (V2-07). The amended 2023 rule remains the baseline.")])
add("florida-404-assumption", "PI-CWA-02", "Florida assumption of the CWA section 404 programme",
    "CWA s.404(g) state assumption (Florida); Center for Biological Diversity v. Zeldin (D.C. Cir.)", "permit-programme", "US-FL",
    ["DM-11", "DM-08"], ["SC-021"],
    [("decided", "2026-03-27", "contracts", "vacated", ["SC-021"], "E", P,
      "D.C. Circuit affirmed that the ESA biological opinion for the assumption was deficient; permitting authority reverted to the Corps; rehearing en banc requested (SC row; not re-verified in V2).")])
add("ghg-endangerment-rescission", "PI-CAA-01", "Rescission of the 2009 GHG endangerment finding and federal vehicle GHG standards",
    "91 FR 7686 (CAA s.202(a))", "regulation", "US", ["DM-10"], ["LM-108", "SC-024"],
    [("final", "2026-02-18", "contracts", "final-not-yet-effective", ["LM-108"], "E", S, "Published 2026-02-18 (finalized 2026-02-12) (V2-06)."),
     ("effective", "2026-04-20", "contracts", "in-force-litigated", ["LM-108"], "E", P,
      "Petitions for review in the D.C. Circuit, Nos. 26-1037 and 26-1061; merits status after June 2026 not checked (V2-06).")])
add("ghgrp-reconsideration", "PI-CAA-02", "EPA Greenhouse Gas Reporting Program reconsideration",
    "40 CFR part 98 (proposed revisions)", "regulation", "US", ["DM-13", "DM-10"], ["SC-026"],
    [("proposed", "2025-09-12", "contracts", "proposed", ["SC-026"], "E", P, "Final status not verified.")])
add("nhpa-s106-regs", None, "Protection of Historic Properties regulations (NHPA section 106)",
    "36 CFR part 800", "regulation", "US", ["DM-07"], ["LM-112"], [],
    note="Baseline rule in force; baseline event date to be supplied in SC's quarterly refresh. The pending rewrite (ACHP vote 2026-07-24; at OIRA; unpublished) is recorded as a watch-status policy signal, not an event, because no proposal has been published (V2-14). See CR-LM-001 on a 'submitted-for-review' event type.")

# ---------------------------------------------------------------- disclosure regimes
add("ca-sb-253", "PI-DISC-01", "California SB 253 Climate Corporate Data Accountability Act and CARB implementing regulation",
    "Cal. Health & Safety Code 38532; CARB SB 253/261 regulation", "disclosure-regime", "US-CA", ["DM-13"], ["LM-113", "SC-027"],
    [("final", "2026-10-12", "expands", "in-force", ["LM-113"], "E", P,
      "OAL approved CARB's initial regulation 2026-10-12, effective immediately; first Scope 1-2 reports due 2026-11-10; Scope 3 from 2027 (V2-15). 'Assurance not required for 2026' not confirmed; do not state it.")],
    note="SC grouped SB 253 and SB 261; WP-10 seeds them separately because their status differs.")
add("ca-sb-261", "PI-DISC-01", "California SB 261 climate-related financial risk reporting",
    "Cal. Health & Safety Code 38533", "disclosure-regime", "US-CA", ["DM-13"], ["LM-113", "FS-014"],
    [("enjoined", "2025-11-18", "contracts", "enjoined", ["LM-113", "FS-014"], "E", P,
      "Ninth Circuit injunction pending appeal; CARB says it will not enforce while it stands (V2-15).")])
add("sec-climate-disclosure", "PI-DISC-02", "SEC climate-related disclosure rules (2024)", "17 CFR parts 210, 229, 232, 239, 249 (2024 amendments)",
    "disclosure-regime", "US", ["DM-13"], ["SC-029"],
    [("stayed", "2024-04-04", "contracts", "stayed", ["SC-029"], "E", H, "Stayed; never effective (SC row)."),
     ("proposed", "2026-05-29", "contracts", "stayed", ["SC-029"], "E", P, "Rescission proposed (SC row; not re-verified in V2).")])
add("eu-omnibus-i", "PI-DISC-03", "EU Omnibus I Directive amending CSRD and CSDDD", "Omnibus I Directive (OJ 2026-02-26)",
    "disclosure-regime", "EU", ["DM-13"], ["LM-114", "SC-028"],
    [("enacted", "2026-02-26", "contracts", "final-not-yet-effective", ["LM-114"], "E", S, "Published in the Official Journal (V2-15)."),
     ("effective", "2026-03-18", "contracts", "in-force", ["LM-114"], "E", S,
      "In force; CSRD transposition by 2027-03-19; CSDDD compliance from 2029-07-26 (V2-15). Directive number not captured; cite by OJ date.")])

# ---------------------------------------------------------------- agreements, forests, state environmental policy acts
add("good-neighbor-authority", "PI-GNA-01", "Good Neighbor Authority incl. EXPLORE Act amendments",
    "16 U.S.C. 2113a; P.L. 118-234 s.351", "agreement-authority", "US", ["DM-12", "DM-15"], ["SC-030", "SC-031"],
    [("enacted", "2025-01-04", "expands", "in-force", ["SC-031"], "J", H,
      "EXPLORE Act amendments (counties and Tribes may retain revenue through FY2028; recreation GNA). Signing day is J; SC-031 dated 2025-01-07.")])
add("long-term-gna-act", "PI-GNA-02", "Long-term Good Neighbor Authority Act (H.R. 7951)", "H.R. 7951, 119th Congress", "statute", "US",
    ["DM-12"], ["SC-032"],
    [("introduced", "2026-03-19", "expands", "pending-legislation", ["SC-032"], "E", P, "SC row; farm bill drafts pending.")])
add("co-hb26-1205", "PI-GNA-03", "Colorado HB26-1205 Colorado State Forest Service Good Neighbor Authority", "Colorado HB26-1205",
    "statute", "US-CO", ["DM-12"], ["SC-034"],
    [("enacted", "2026-04-13", "expands", "final-not-yet-effective", ["SC-034"], "E", S, "Signed (SC row)."),
     ("effective", "2026-08-12", "expands", "in-force", ["SC-034"], "E", S, "SC row.")])
add("fix-our-forests-act", "PI-FOR-01", "Fix Our Forests Act (H.R. 471 / S. 1462)", "H.R. 471 and S. 1462, 119th Congress", "statute", "US",
    ["DM-03", "DM-08", "DM-12"], ["SC-033"],
    [("passed-chamber", "2025-01-23", "contracts", "pending-legislation", ["SC-033"], "E", P,
      "Passed House; cleared Senate committee Oct 2025; enactment not confirmed as of the last reachable source (2025-11-10).")])
add("usfs-objection-rule", "PI-FOR-02", "Forest Service project-level objection rule", "36 CFR part 218", "regulation", "US",
    ["DM-02", "DM-04"], ["SC-009"],
    [("final", "2026-10-13", "contracts", "final-not-yet-effective", ["SC-009"], "E", P, "SC row (sister-repo research); not re-verified in V2."),
     ("effective", "2026-11-12", "contracts", "in-force", ["SC-009"], "E", P, "Scheduled effective date; confirm on or after the date.")],
    note="Split from SC's PI-FOR-02 (objection rule and Roadless proposal have different status).")
add("roadless-rule-rescission", "PI-FOR-02", "Roadless Area Conservation Rule rescission (proposed)", "36 CFR part 294 subpart B (proposed rescission)",
    "regulation", "US", ["DM-10", "DM-04"], ["SC-009"],
    [("proposed", "2026-08-20", "contracts", "proposed", ["SC-009"], "E", P,
      "Proposed rule and DEIS; comments closed 2026-09-21 (371,657 received per SC row); no final rule.")])
add("ceqa-2025-reforms", "PI-SEPA-01", "California CEQA reforms in 2025 budget trailer bills (AB 130 and SB 131)", "AB 130 and SB 131 (2025)",
    "statute", "US-CA", ["DM-03"], ["LM-115"],
    [("enacted", "2025-06-30", "contracts", "in-force", ["LM-115"], "E", S,
      "Infill-housing exemption, rezoning exemptions, infrastructure exemptions and streamlining; cite the pair together (V2-16 lifts SC's NOT VERIFIED placeholder).")])

# ---------------------------------------------------------------- Tribal-related instruments: HELD (ADR-0007; TN gate)
add("tribal-co-stewardship-policy", "PI-TRIBE-01", "Federal Tribal co-stewardship policy instruments (held)",
    "Held pending Tribal review", "executive-order", "US", ["DM-12"], ["SC-035", "SC-036"],
    [("rescinded", "2025-03-14", "contracts", "rescinded", ["SC-035"], "E", P, "Held. Event wording to be set under the Tribal gate (V2-13 has the verified facts).")],
    held=True, note="Tribal-related: quarantined under ADR-0007 section D; excluded from every release artifact until a Tribal Advisory Council approves.")
add("consultation-duties-outside-nepa", "PI-TRIBE-02", "Consultation duties outside NEPA (held)",
    "Held pending Tribal review", "statute", "US", ["DM-06", "DM-07"], ["SC-038", "SC-039"], [],
    held=True, note="Tribal-related framing (government-to-government consultation): quarantined; TN decides representation. Sovereignty-based consultation is not to be labelled a reform to be streamlined (SC).")

# ---------------------------------------------------------------- selection, hiring and workforce-capacity instruments
add("ofccp-eo11246-regs-rescission", None, "OFCCP rescission of Executive Order 11246 implementing regulations (incl. 41 CFR 60-3)",
    "41 CFR parts 60-1, 60-2, 60-3 (as codified for EO 11246), 60-4, 60-20, 60-40, 60-50, 60-999; FR Doc 2026-17114", "regulation", "US",
    ["DM-16", "DM-10"], ["LM-118"],
    [("final", "2026-08-21", "contracts", "final-not-yet-effective", ["LM-118"], "E", S, "Final rule published (IO-028)."),
     ("effective", "2026-10-26", "contracts", "rescinded", ["LM-118"], "E", "2026-10-27",
      "Scheduled effective date, three days after this seed; confirm on or after the date. OFCCP states the rule does not affect UGESP's existence more broadly (IO-020).")])
add("opm-ugesp-references-ifr", None, "OPM interim final rule removing UGESP references from OPM hiring regulations",
    "5 CFR part 300 and related parts; FR Doc 2026-15586; 91 FR 48236", "regulation", "US", ["DM-16"], ["LM-119"],
    [("interim", "2026-07-31", "reshapes", "interim-in-force", ["LM-119"], "E", P,
      "Effective on publication with 60-day comment; cites the 2026-06-09 DOJ OLC opinion; 5 CFR 300.103 still requires job analysis and a rational relationship to performance (IO-022). Never describe EMST use as 'UGESP compliance'.")])
add("co-sb-24-205", None, "Colorado SB 24-205 Consumer Protections for Artificial Intelligence (as amended)", "Colorado SB 24-205",
    "statute", "US-CO", ["DM-13", "DM-14"], ["LM-117"],
    [("enjoined", "2026-04-27", "contracts", "enjoined", ["LM-117"], "E", S, "Federal court order blocked enforcement (IO-034)."),
     ("rescinded", "2026-05-14", "contracts", "repealed", ["LM-117"], "E", S, "Repealed and replaced by SB 26-189; never took effect as written (CP-043).")])
add("co-sb-26-189", None, "Colorado SB 26-189 automated decision-making technology notice and disclosure law", "Colorado SB 26-189",
    "statute", "US-CO", ["DM-13", "DM-14"], ["LM-117"],
    [("enacted", "2026-05-14", "reshapes", "final-not-yet-effective", ["LM-117"], "E", P,
      "Signed 2026-05-14; effective 2027-01-01 with enforcement dependent on AG rulemaking; notice, post-adverse-decision disclosure, correction and human review on request in consequential decisions incl. employment (CP-043, IO-034).")])
add("eo-14356-hiring-accountability", None, "Executive Order 14356 Ensuring Continued Accountability in Federal Hiring", "EO 14356",
    "executive-order", "US", ["DM-16"], ["LM-120"],
    [("final", "2025-10-15", "contracts", "in-force", ["LM-120"], "E", S,
      "Strategic Hiring Committees approve each vacancy; annual staffing plans with quarterly updates; no hiring ratio in the EO itself (V1-08).")])
add("opm-merit-hiring-plan", None, "OPM Merit Hiring Plan", "OPM Merit Hiring Plan (2025-05-29)", "memo", "US", ["DM-16"], ["LM-121"],
    [("final", "2025-05-29", "reshapes", "in-force", ["LM-121"], "E", S,
      "From 2025-09-30 self-assessment questionnaires only for minimum qualifications, not rating and ranking (V1-09).")])
add("opm-series-realignment-proposal", None, "OPM Modernization and Consolidation of Occupational Series (Phase One proposal)",
    "OPM CHCO memo 2026-04-24", "memo", "US", ["DM-16"], ["LM-122"],
    [("proposed", "2026-04-24", "reshapes", "proposed", ["LM-122"], "E", P,
      "115 series proposed for realignment (e.g., 0410/0437/0480/0487 to 0401; 0455 to 0404; 0029 to 0303; 0688 to 0601). No final decision memo as of 2026-10-23 (V1-10). Say 'proposed for realignment'.")],
    note="SeriesRecord events in data/v2/registers/opm_series (FH/DE lane) should reference this instrument.")
add("schedule-policy-career", None, "Schedule Policy/Career (OPM final rule and EO 14410)", "91 FR 5580; EO 14410", "regulation", "US",
    ["DM-16"], ["LM-124"],
    [("final", "2026-02-06", "reshapes", "final-not-yet-effective", ["LM-124"], "E", S, "OPM final rule published (V1-12)."),
     ("effective", "2026-03-09", "reshapes", "in-force-litigated", ["LM-124"], "E", P, "Effective; litigation pending (V1-12)."),
     ("final", "2026-06-03", "reshapes", "in-force-litigated", ["LM-124"], "E", P,
      "EO 14410 placed listed positions in Schedule Policy/Career; ~8,000 employees per press analysis, not the EO text (V1-12).")])
add("opm-ai-in-hiring-memo", None, "OPM memo Use of Artificial Intelligence in the Federal Hiring Process", "OPM CHCO memo 2026-08-27",
    "guidance", "US", ["DM-14", "DM-16"], ["LM-123"],
    [("final", "2026-08-27", "reshapes", "issued", ["LM-123"], "E", S,
      "Drafting PDs with AI generally not high-impact when the official independently reviews and adopts; rating and ranking presumed high-impact (V1-13). OPM views, not OMB determinations.")])
add("uswfs-so-3448", None, "Secretarial Order 3448 establishing the U.S. Wildland Fire Service", "DOI SO 3448 (directed by SO 3443)",
    "executive-order", "US", ["DM-16", "DM-05"], ["LM-125"],
    [("final", "2026-01-12", "reshapes", "in-force", ["LM-125"], "E", S,
      "Unifies BIA, BLM, NPS and FWS fire plus OWF and OAS; USFS fire NOT moved (consolidation only proposed in the FY2027 budget) (V1-06).")],
    note="instrumentType executive-order is used for a department-level Secretarial Order; CR-LM-001 proposes a 'secretarial-order' or 'agency-order' value.")
add("wildland-fire-quals-alignment", None, "USWFS-USFS aligned federal wildland fire qualification standards (IQCS 2026 Transition Plan)",
    "2026 IQCS Transition Plan; Federal Wildland Fire Qualifications Supplement", "standard-with-legal-force", "US", ["DM-17", "DM-16"], ["LM-141"],
    [("final", "2026-01-28", "reshapes", "issued", ["LM-141"], "E", P,
      "Aligned standards effective January 2027; alignment is USWFS-USFS federal standards, not NWCG (V3-13).")])
add("fy2026-interior-approps", None, "FY2026 Interior, Environment and Related Agencies appropriations (P.L. 119-74, Division C)",
    "P.L. 119-74, Division C", "statute", "US", ["DM-19", "DM-16"], ["LM-126", "FS-019"],
    [("enacted", "2026-01-23", "contracts", "in-force", ["LM-126"], "E", S,
      "$42.56bn, down $809M (1.9%) from FY2025, vs a $26.85bn request (V1-15).")])
add("obbba-ira-rescissions", None, "Rescission of unobligated IRA conservation and staffing funds (P.L. 119-21)", "P.L. 119-21 (2025)",
    "statute", "US", ["DM-19", "DM-16"], ["FS-036"],
    [("enacted", "2025-07-04", "contracts", "in-force", ["FS-036"], "E", H,
      "Includes urban and community forestry, NPS hiring and USFS NEPA staff lines (FS WS-10; amounts per FS-036, not re-verified in V2).")])
add("americorps-grant-terminations", None, "AmeriCorps FY2025 grant terminations, injunction and 2026 settlement",
    "Maryland et al. v. AmeriCorps (D. Md.); settlement 2026-09-11", "court-decision", "US", ["DM-19"], ["LM-127"],
    [("enjoined", "2025-06-05", "expands", "enjoined", ["LM-127"], "E", H,
      "Preliminary injunction only in the 24 plaintiff states + DC; terminated programmes there reinstated (V1-05)."),
     ("decided", "2026-09-11", "expands", "in-force", ["LM-127"], "E", P,
      "Settlement: no anticipated FY2026 mass terminations; 30 days notice; litigation stayed through 2027-02-01. Covers FY2026 and the coalition only (V1-05).")])
add("workforce-pell", None, "Workforce Pell Grants final rule", "Workforce Pell final rule (ED)", "regulation", "US", ["DM-19"], ["LM-142"],
    [("final", "2026-05-18", "expands", "in-force", ["LM-142"], "E", S,
      "Pell for eligible 150-599 clock-hour programmes from 2026-07-01; governors with state workforce boards identify in-demand occupations (V3-03).")])
add("aswa-2026-hr-8210", None, "A Stronger Workforce for America Act of 2026 (H.R. 8210; WIOA reauthorization)", "H.R. 8210, 119th Congress",
    "statute", "US", ["DM-19"], ["LM-142"],
    [("introduced", "2026-04-06", "reshapes", "pending-legislation", ["LM-142"], "E", P,
      "Ordered reported 19-14 by House Education and Workforce on 2026-04-21; no floor vote or Senate action found; WIOA not reauthorized (V3-03).")])
add("faa-part-108", None, "FAA Part 108 Normalizing Unmanned Aircraft Systems Beyond Visual Line of Sight Operations", "14 CFR part 108 (proposed)",
    "regulation", "US", ["DM-17", "DM-14"], ["LM-116", "FS-022"],
    [("proposed", "2025-08-07", "expands", "proposed", ["LM-116"], "E", P,
      "NPRM FR Doc 2025-14992; comment period reopened Jan 2026; final rule at OIRA since 2026-07-10, unpublished as of 2026-10-21 (V2-17; trade press). The OIRA stage is recorded as a watch signal.")])
add("american-security-drone-act", None, "American Security Drone Act of 2023 federal-funds restrictions", "FY2024 NDAA (P.L. 118-31), ASDA provisions",
    "statute", "US", ["DM-15"], ["LM-116"],
    [("effective", "2025-12-22", "contracts", "in-force", ["LM-116"], "E", S,
      "Covered UAS from foreign-adversary-linked manufacturers may not be procured, operated or maintained with federal funds (V2-17). Section numbers not confirmed.")])
add("tx-hb-3923", None, "Texas HB 3923 (degree requirements in state hiring)", "Texas HB 3923 (89th Legislature)", "state-hr-order", "US-TX",
    ["DM-16"], ["SL-010", "SL-015"],
    [("effective", "2025-09-01", "reshapes", "in-force", ["SL-010"], "E", S, "SL state policy lever SL-L01 (not re-verified in V-passes).")],
    note="State HR events count as the policy family toward role change indicators but cannot alone move a skill-change indicator (ADR-0028 s3).")
add("dol-tegl-07-25", None, "DOL TEGL 07-25 WIOA state plan modifications PY2026-2027", "Training and Employment Guidance Letter 07-25",
    "guidance", "US", ["DM-19"], ["SL-009"],
    [("final", "2026-01-26", "reshapes", "issued", ["SL-009"], "E", S, "Modifications due 2026-03-03 (extension to 2026-04-30) (SL-L13).")])


def build():
    instruments, events = [], []
    disposition = []
    for x in I:
        iid = "seed:ins/" + x["key"]
        rec = base(iid, "Instrument", x["label"], editorial_note=x["note"],
                   notation=([{"scheme": "SC-policy-landscape-2026", "value": x["sc"]}] if x["sc"] else None), held=x["held"])
        rec.update({
            "citation": x["citation"],
            "instrumentType": x["itype"],
            "jurisdiction": x["juris"],
            "mechanisms": x["mech"],
            "provenance": provenance(x["src"], "E"),
        })
        instruments.append(rec)
        for (etype, date, direction, status_after, src, label, review_by, note) in x["events"]:
            eid = "seed:evt/%s/%s/%s" % (x["key"], etype, date)
            ev = base(eid, "DriverEvent", "%s: %s %s" % (x["label"], etype, date), editorial_note=note, held=x["held"])
            ev.update({
                "instrument": iid,
                "eventType": etype,
                "eventDate": date,
                "jurisdiction": x["juris"],
                "direction": direction,
                "statusAfter": status_after,
                "sources": sorted(src),
                "evidenceLabel": label,
                "recordedBy": "emstagent:A9-LM@claude-opus-5-5",
                "reviewBy": review_by,
                "provenance": provenance(src, label),
            })
            events.append(ev)
        disposition.append((x["sc"] or "", iid, "held-tribal" if x["held"] else "seeded", x["label"]))
    # SC rows not seeded as instruments, with reasons
    disposition.append(("PI-TECH-04", "seed:sig/deployment/permitting-ai-shared-services", "reclassified-to-signal",
                        "PNNL PermitAI shared services are tools (L4, DC lane) not legal instruments (ADR-0003 T-7); recorded as a deployment-family ChangeSignal"))
    disposition.append(("PI-SEPA-02", "", "not-seeded",
                        "Placeholder for other state environmental policy acts; unverified; SL/DB to supply per-state instruments in the quarterly refresh"))
    return instruments, events, disposition
