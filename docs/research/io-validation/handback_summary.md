I did the work, but `report.md` was refused by the harness for subagents, so its full text is appended below for you to save. **Evidence limit:** the team's web-search budget was used up and fetches to ecfr.gov and opm.gov were blocked. All 72 external sources are marked `unverified`, and their current (October 2026) legal or program status needs confirming by FH or CP. The v1 appraisal is computed from repo data and rerun from a script.

**Verdict on v1:** it describes the field well but can't support selection or promotion.
- Its proficiency levels are tenure bands (0–2, 3–5, 6–10, 10+ years).
- In a blind sample of 1,165 statements from 43 competencies, 29.9% are directly observable and 15.4% can't be assessed as individual performance. At Expert level those figures are 5% and 61%, and only 1 of 43 Expert levels has a direct, non-proxy statement.
- Much of the level text is boilerplate: 211/222 Expert knowledge statements start "Shapes…".
- Domain 5 has no indicators at all, and 32% of the source indicators (2,104 of 6,484) never made it into the database.
- No tag has reliability evidence, and 11/222 career-ladder-destruction flags contradict their own rule.
- These figures rest on a single rater (me). They justify a redesign; two humans should re-code them before they're published.

**v2 model:** five levels (L1–L5) defined by responsibility on seven attributes, two of them new (working with AI, developing others). Each competency is defined only at the levels where the work exists, using indicators with an explicit condition and standard. Knowledge, credentials and tools move to separate layers. Every indicator says whether AI is excluded, permitted with checking, or supervised. Grades connect through position profiles, never "L3 = GS-12" tables.

**Validation:** validate tasks first and accept competencies through their links to critical tasks. Correct for the contraction sampling bias v1 itself predicted. Run a pre-registered Delphi with 15–25 per panel; v1's 3–5 reviewers per competency can't reach significance. Gate every tag on its reliability, and test any LLM tagger on held-out items. My own rule coder dropped from κ .79 to .69 out of sample.

**CA's four questions:**
1. The task spine can be validated first.
2. Craft-weight reliability is unknown, so run the designed pilot (150 tasks plus 40 competencies, 12 raters). A 3-level ordinal fallback lowers agreement rather than raising it.
3. Use generic levels plus level spans, with five levels.
4. Release v2.0 with use labels: training-grade now, selection-grade only after an employer's own job analysis.

**Top proposals:** P-IO-01, 07, 10, 11, 12, 13, 15.

**Biggest trade-off:** defensibility against coverage and speed. Selection-grade content arrives 12–24 months out, one function cluster at a time.

Files are in `docs/research/io-validation/`:
- proficiency_model_v2.md
- indicator_writing_rules.md
- validation_protocol.md
- exemplar_rewrites.csv
- v1_assessment.csv
- candidate_competencies.csv
- ecosystem.csv
- sources.csv
- v1_observability_ratings.csv
- v1_observability_population_rulecoded.csv
- analysis/

