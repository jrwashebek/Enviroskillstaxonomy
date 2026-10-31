# Evaluation round 2: usability and accessibility, before and after

- **Evaluator:** "usability-a11y", an AI agent working as an independent evaluator. It reused round 1's methods and scripts. No users took part and no screen reader was run, so every result is expert judgement or a scripted measurement.
  - [E] means measured or observed, [J] means expert judgement, [S] means speculation.
- **Build:** production `app/index.html` and bundle (inputs `0a8bbe4ac744619f`), tested 31 October 2026, 00:03–00:46 UTC.
  - The baseline is the current explorer (`site/_site`). Its role-page, search and first-load numbers were re-measured and match round 1. Its walkthrough results are carried over from round 1.
- **Evidence:** the evaluator's scripts, raw outputs and 103 screenshots are kept in the design working folder.
- **Data changed during the test:** the data was rebuilt at about 00:40 by round 2.5 work. Measurements were taken before that, except the link and vocabulary scans and a hold-word re-check.
- **Round 2.5 follow-up:** the release-gate and severity-3 problems this report found have since been fixed and re-tested. See the last section.

## Verdict

**Much better, but not yet through the release gate.** Most of round 1's usability problems are fixed. Two WCAG problems remained in search: dark-mode contrast on highlighted words in focused results, and suggestions in forced colours. Back focus, hold-word gaps, and first load on two page types were serious defects.

## Round 1 → round 2

Role-page figures are medians over 120 role-variant routes at 390 px, default state.

| Metric | Explorer (re-measured) | Round 1 | **Round 2** |
|---|---|---|---|
| Role page words (all / visible) | 7,303 / 3,359 | 2,397 / 1,263 | **2,566 / 1,131** |
| Role page tab stops (R4 selector / reachable) | 188 / 130 | 145 / 74 | **152 / 72** |
| Tabs to first task, forester federal, 1280 (390) | 59 | 27 (16) | **24 (19)**; top action bar at 17 (12) |
| Role page height at 390 px | 23,201 | 9,873 | **8,803** |
| "Assessment pending" per role page | 185 | 2 | **2** |
| Disclosures per role page | 42 | 9.5 | **11.5** (two sections collapsed on purpose) |
| Search zero-result queries (50) | 18/50 | 4/50 | **3/50** ("veteran", "California", "O\*NET") |
| Search top-3 relevance (44 queries) | 61% | 86% | **95%**; still failing: "seasonal", "sawyer" |
| "No results match all the words" banner shown | — | 9/50 | **6/50** |
| First suggestion is also the first result | — | 41/45 | **43/47** |
| Competency → role links | 0/223 | 191/223 | **191/223** (the other 32 say none exists yet) |
| Rule-version strings; `closeMatch`-type leaks | 7,101; 690 | 0; 0 | **0; 0** |
| Agent and source codes in visible text, 692 routes | — | 533 (218 pages) | **447 (209 pages)** |
| What's changing height at 390 px | — | 78,994 | **4,750**, sections collapsed (default) |
| Role page requests; KB gzip / uncompressed | 7; 135 / 734 | 40; 292 / 1,470 | **13; 271 / 1,432** |

### First load: route H1 painted, gzip, 390 × 844, cache off (mean of 2 runs)

| Page | Explorer, Slow 3G | R1, Slow 3G | **R2, Slow 3G** | Explorer, Fast 3G | R1, Fast 3G | **R2, Fast 3G** |
|---|---|---|---|---|---|---|
| Home | 5.40 s | 21.2 s | **4.88 s** | 1.57 s | 6.0 s | **1.42 s** |
| Role, forester federal | 5.41 s | 23.7 s | **7.80 s** | 1.58 s | 6.7 s | **2.24 s** |
| Role, field resource technician | — | — | **7.81 s** | — | — | **2.24 s** |
| Competency | — | 24.4 s | **8.23 s (over budget)** | — | — | **2.35 s** |
| What's changing | — | 24.1 s | **8.09 s (over budget)** | — | 6.9 s | **2.34 s** |

On the role page, "Where it can lead" fills in at 11.7 s on Slow 3G.

## Walkthroughs (round 1's eight scenarios)

| # | Scenario | Explorer | R1 | **R2** | Why |
|---|---|---|---|---|---|
| 1 | Duties for a federal GS-0460 position description | Partial | Success | **Success** | The series page has duties by GS band with 62 task statements. The text copy and the 63-row CSV carry grades and notices. Role-page "Copy tasks as text" still has no grade. |
| 2 | Corps lead: what a field resource technician does; what to train first | Fail | Partial | **Partial** | Choosing the nonprofit version takes one action. "What to train first" can't be answered, by design: competency levels are explore only. The panel still says "Land trust" (data). |
| 3 | Seasonal firefighter: year-round roles that overlap | Fail | Partial | **Partial** | The numbers agree with Compare, and the caveat is present. "seasonal firefighter" still shows the "no full match" banner, and no page covers pay, seasonality or hiring authority. |
| 4 | Water-quality technician programme | Partial | Success with friction | **Success with friction** | Explore-only notice added. The "no full match" banner still appears. Back from a competency dropped focus (fixed in round 2.5). |
| 5 | State class compared with an EMST role | Fail | Fail | **Fail** (partial for 38 classes) | Still 4 jurisdictions, and no control to compare a class with a role. |
| 6 | Download data and cite a competency by ID | Partial | Partial | **Partial, improved** | The ID search finds one best match, and the citation copies the ID. Release files are still not posted. |
| 7 | Report a wrong task | Likely abandonment | Success with a GitHub account | **Same** | On task pages the report controls are still at the bottom. |
| 8 | Understand "assessment pending" and use tiers | Partial | Success | **Success** | Back returns focus to "What this allows". |

## WCAG 2.2 AA checks

| Check | Round 2 result |
|---|---|
| **axe-core:** 57 routes, disclosures closed and open, each employer tab, light and dark, 1280 and 390 (580 runs) | **Light: 0. Dark: 1**, contrast 1.47:1 on `<mark>` in a focused search result. `region` warnings gone. `heading-order` only on the not-found page. |
| **Keyboard:** search combobox, role employer select, role action bar, What's changing hub, Compare | **Pass** for all five |
| **Focus contrast, dark** | The round 1 failure is fixed (0 of 1,049 stops fail). **New:** 102 of 141 focused search-result links fail at 1.48:1. |
| **Back focus restoration** | **Partial:** 46 of 62 role-page cases restored. |
| **Back from a link to a page section** | Pass, with one minor exception |
| **Reflow at 320 px, 400% zoom and text spacing** | Pass |
| **Forced colours: overlap bar** | Pass |
| **Forced colours: search suggestions** | **Fail:** the selected title is drawn as a block, and in the dark palette the matched letters vanish |
| **Live regions** | Pass. Minor: in What's changing, "Show all" announces the overall count. |

## Round 1 findings: status

| Round 1 finding | Status |
|---|---|
| 1. First load about 4× slower | **Partly fixed.** Home and role pages are within budget; competency and What's changing were 0.1–0.2 s over. |
| 2. Employer choice hidden | **Fixed** |
| 3. Search contradicts itself | **Partly fixed.** Best-match tier added. The banner still appears for "TX 2682". Suggestions and results order differ for a record ID query. |
| 4. What's changing too tall | **Fixed** (a hub with sections, not separate sub-pages) |
| 5. HR output not ready | **Fixed** on series pages |
| 6. Pathway numbers disagree | **Partly fixed.** 60 of 60 pairs match Compare. There is no "my level" choice and no note on pay, seasonality or hiring authority. |
| 7. Common terms miss | **Partly fixed.** "seasonal" and "O\*NET" still fail. |
| 8. Codes, file names and a "null" bug | **Partly fixed.** No "null"; codes 533 → 447; some file names remain. |
| 9. Role pages long, actions only at the bottom | **Fixed** on role pages. Task pages still have actions at the bottom. |
| 10. Data out and corrections in depend on GitHub | **Not fixed** (decision pending) |
| a11y 1: dark-mode focus on task links | **Fixed** |
| a11y 2: stale `aria-activedescendant` | **Fixed** |
| a11y 3: skip link rewrote the URL | **Fixed** |
| a11y 4: search suggestions in forced colours | **Not fixed** in round 2. Fixed in round 2.5; see below. |
| a11y 5: search and Compare announced only "… loaded" | **Fixed** |
| Assigned to round 2: "Show all" focus, Compare title and headings, overlap pattern, home figures | **Fixed** |
| Filter links that work in a new tab | **Partly fixed.** The role page's family breadcrumb still goes to `#/roles`. |

## New problems found in round 2

- **N1 (3). Back drops focus for links in collapsed or late-loading content.** "Where it can lead" lost 12 of 12, because it fills in after the H1 and a hidden copy of the same link sits in a closed disclosure. Competency-table links lost 5 of 15.
- **N2 (3). Some hold-type queries reached "Suggest a role or task we're missing".** 7 of 37 failed: word forms such as "tribally" and "intertribal", "first nation", typos inside two-word phrases, and run-together phrases.
- **N3 (3; WCAG 1.4.3). Highlighted words in focused search results** were unreadable in dark mode (1.48:1).
- **N4 (2). "Where it can lead" mostly lists entry-level profiles for senior and lead roles.** 29 of 60 destinations are tagged "Entry level", and 12 of 26 roles show only entry-level destinations. Compare explains these, but the role page shows only the tag.
- **N5 (1). Minor:**
  - in What's changing, a family's "Show all" announces the overall count;
  - a deep link to `@employers` focuses a closed section;
  - the 404 page goes from h1 to h3;
  - backing into a page reached through a section link focuses the section.

## Top 5 remaining problems at the end of round 2

1. N3, dark-mode `<mark>` in focused results (WCAG 1.4.3).
2. Search suggestions in forced colours.
3. N1, Back focus.
4. First load over budget on competency (8.23 s) and What's changing (8.09 s).
5. N2, hold-word gaps.

## Round 2.5 follow-up (lead, re-tested with the evaluator's scripts)

1. **N3: fixed.** Inside a focused link, `mark` inherits the link's colours and keeps bold and underline. The evaluator's search-focus scan now finds 0 of 141 focused links below 4.5:1 in dark mode (worst 11.88:1) and 0 in light mode.
2. **Forced colours: fixed.**
   - The selected option and every child use Highlight and HighlightText, with no block.
   - Matched letters in other options use the system Mark and MarkText colours.
   - The evaluator's computed-style probe shows readable pairs in both palettes.
3. **N1: fixed in the router.** On Back, the router focuses the first *visible* copy of the remembered link. It waits up to 1.5 s for sections that fill in late, then falls back to a copy inside a closed disclosure, which it opens. For 3 s, if the section re-renders, focus follows the link instead of dropping to the page body. Results of the evaluator's Back test are under "Back focus after round 2.5" below.
4. **N2: fixed.** Search uses all governed triggers plus word forms, typo-tolerant two-word phrases and run-together phrases. `tools/check-hold-search.cjs` passes 39 hold queries and 14 controls.
5. **First load:** re-measured after round 2.5; see `performance-round2.md` and the summary in the project report.
