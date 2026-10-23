**SL summary (Phase 2)**

The harness refused my `report.md` write, so its full text follows the line below. All CSVs and scripts are saved in `/home/claude/emst/docs/research/state-local/`, and `scripts/validate.py` passes.

**What breaks a federal-centric design**
- State and local environmental work is mostly the regulator's, operator's and overseer's job: permit writing, inspection, enforcement, primacy programs, utilities, environmental health. v1 is written from the applicant/land-manager side and has no text on operators, sanitarians, primacy, delegation or state environmental policy acts. Its 6.1.2 and 6.1.3 map to 29 and 18 of my 70 sampled classes, but they are written for the regulated party.
- States differ in ways a federal template can't absorb:
  - Qualifications live in different places: spec, bulletin, posting, agency, or set at recruitment.
  - Degree rules diverge for the same work: 31% of known rules require a degree, 37% allow substitution.
  - One class covers many roles, and level and pay encodings don't line up.
  - Union "shadow classes" (WA), licensure splits and decades-old specs (MN) complicate mapping.
- States already run their own crosswalks EMST should reuse: Texas military codes, New York's Section 70.1 transfer lists, Pennsylvania's federal-title equivalencies.

**Minimal common fields:** 28 fields, 16 required. Core: jurisdiction, employer type, agency, class code/title/series, level and supervisory status, spec date, duties text, MQ text and where it lives, degree rule, licenses (issuer, timing), pay basis/range/date, provenance, and the EMST mapping record (variant, level, match type, confidence, reviewer).

**Top mobility barriers:** federal pay at 77–183% of state pay, eligible-list and status gates, degree and licensure divergence, hiring time (90 days state, 136 local), pensions [J], residency, bargaining-unit change. Pennsylvania's equivalency order works (1,350 hires; federal titles written into MQs; AI matching), but no state program targets environmental agencies.

**Top proposals:**
- P-SL-01: role variants plus a dated per-class jurisdiction overlay, not per-state roles.
- P-SL-02: an authority-position facet.
- P-SL-03: add inspect, enforce, operate, fund and oversee functions.
- P-SL-04: a 12-role state/local MVP.
- P-SL-07: publish the minimal fields as the ingestion schema.
- P-SL-08: build the federal-to-state environmental crosswalk first, validated with Pennsylvania and tested against the native crosswalks.
- P-SL-11: make licensure a first-class entity.

**Verified status:** WIOA bill H.R. 8210 cleared committee only (19–14, 2026-04-21). TEGL 07-25 plan modifications were due 2026-03-03.

**Limits:** the shared search budget ran out after my 14th search. Colorado, Oregon, North Carolina and Montana specs weren't retrieved. Water operators, REHS, IPA, GNA, pensions and bargaining law are [J] and listed in a verification queue (§15).

**Files** (in `/home/claude/emst/docs/research/state-local/`):
- sources.csv (91)
- state_classification_sample.csv (70)
- state_policy_levers.csv (29)
- mobility_map.csv (21)
- minimal_common_fields.csv (28)
- candidate_competencies.csv (16)
- role_signals.csv (13)
- v1_assessment.csv (20)
- ecosystem.csv (33)
- scripts/
