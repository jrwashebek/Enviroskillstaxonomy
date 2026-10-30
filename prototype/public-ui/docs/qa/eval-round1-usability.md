# Evaluation round 1: usability, before and after

- **Evaluator:** "usability", an AI agent acting as an independent expert evaluator, using R4's methods unchanged. No real users took part; every outcome is expert judgment.
- **Build:** prototype round 1, tested 21:40–22:15 UTC on 30 October 2026. The prototype was being edited during the test.
- **Evidence:** scripts, logs and about 80 screenshots, kept in the design working folder.

## Before and after

| Metric | Old explorer (R4, re-measured) | Prototype, round 1 |
|---|---|---|
| Role page words (all text / visible) | 7,303 / 3,359 | **2,397 / 1,263** |
| Role page tab stops (R4 selector / reachable) | 188 / 130 | **145 / 74** |
| Tabs to first task, forester, 1280px | 59 | **27** (16 at 390px) |
| Role page height at 390px, median | 23,201px | **9,873px** |
| "Assessment pending" per role page | 185 | **2** |
| Disclosures per role page | 42 | **9.5** |
| Search zero-result queries (50 realistic queries) | 18/50 | **4/50** |
| Search top-3 relevance (44 content queries) | 27 (61%) | **38 (86%)** |
| Competency → role links | 0/223 | **191/223**; the rest say none exists yet |
| Rule-version strings and `closeMatch`-type leaks | 7,101 and 690 | **0 and 0** |
| First paint of the route H1, Slow 3G with gzip (home / role) | 5.4s / 5.45s | **21.2s / 23.7s (worse)** |
| Role page requests; KB transferred (gzip / uncompressed) | 7; 135 / 734 | 40; 292 / 1,470 |

**Cause of the slow first load.** The total bytes are within budget: the shell is 190 KiB gzipped and `core.js` is 59.8 KiB. The delay comes from a chain of requests, each waiting for the last: HTML with no content → `main.js` → 21 modules → `core.js` → role file and `paths.js`. Each request on Slow 3G costs a 2-second round trip.

## Walkthroughs (R4's eight scenarios)

| # | Scenario | Old | New |
|---|---|---|---|
| 1 | Duties for a federal GS-0460 position description | Partial | **Success** |
| 2 | Corps lead: what a field resource technician does, and what to train first | Fail | **Partial** |
| 3 | Seasonal firefighter: year-round roles that overlap | Fail | **Partial** |
| 4 | Water-quality technician programme | Partial | **Success with friction** |
| 5 | State class compared with an EMST role | Fail | **Fail** (partial for 20 classes) |
| 6 | Download data and cite a competency by ID | Partial | **Partial** |
| 7 | Report a wrong task | Likely abandonment | **Success with a GitHub account** |
| 8 | Understand "assessment pending" and use tiers | Partial | **Success** |

## Top 10 remaining problems, ranked by severity × frequency

1. **First load about 4× slower on poor networks (12).** Fix: prerender the shell; bundle and minify the scripts; load `core.js` in parallel; load `paths.js` lazily; reduce fonts. Budget: no more than 8s on Slow 3G with gzip.
2. **Employer choice hidden below the task list it filters (9).** The base route silently shows the federal version. Fix: an employer selector next to the role-level filter, and "Showing: federal version".
3. **Search contradicts itself (9).** "No results match all the words" appears above correct answers, and suggestions and results rank differently. Fix: one ranking, a "Best match" tier, and "no results" only when there are none.
4. **What's changing is 78,994px tall at 390px (6).** 51 of its 107 signal cards repeat 21 BLS projections. Fix: a hub with sub-pages, merged projection rows, and filters.
5. **HR output not ready for a position description (6).** Series "duties" are competency titles, the same in every band, and the copied text has no GS band. Fix: task statements by band, plus copy and CSV with the band.
6. **Pathway numbers disagree (6).** The role page says "6 of 15" and Compare says "8 of 17" for the same pair. Fix: one rule, stated level, a "my level" choice, and a note that EMST does not cover pay, seasonality or hiring authority.
7. **Common terms miss (6).** "environmental scientist", "seasonal", "UAS", record IDs and help terms. "O\*NET" is corrected to "one". Fix: synonyms, an ID index, help terms that route to the key, and codes exempt from typo correction.
8. **Codes, file names and a "null" bug in source lists (6).**
9. **Role pages still long, with actions only at the bottom (6).** Fix: a top action bar; collapse "With other employers" and "Connections".
10. **Getting data out and corrections in both depend on GitHub (6).** This needs a decision from the project lead.

**Also noted:**
- corps employer wording ("Land trust" on the nonprofit field resource technician);
- state-class coverage of only 4 jurisdictions;
- employer chips that look like buttons;
- the HR disclaimer shown twice on federal and state role pages;
- search suggests the word "qualify".

## Kept as strengths

- "Assessment pending" appears once per section, with a count and a reason, and links to the key.
- Both-way navigation between roles, competencies and tasks.
- The "doesn't mean you qualify" caveat at the point of comparison.
- The report template, which copies the record ID, title and release.
