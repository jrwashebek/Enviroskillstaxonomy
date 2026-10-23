# WP-15: required text corrections to the flagship report

- **Report:** `docs/package/report/flagship_report.md` (draft 0.9, 2026-10-23). **Claim list:** `docs/package/report/claims_used.csv` (264 claims).
- **Checked by:** LM (A9), 2026-10-23, against primary sources via the web. Register rows: `docs/methods/claims_register.csv`, RPT-01 to RPT-26. The PM added and verified SBH-01, SBH-02 and STATE-PA-01. Sources: `docs/methods/sources.csv` LM-164 to LM-179.
- **Owner of the edits:** the WP-14 report lead. LM does not edit `docs/package/`. Line numbers refer to the file as it stood on 2026-10-23.
- **How to apply:** each correction is a straight swap of exact old wording for new wording. After the edits, update the matching `claim_as_written` cells in `claims_used.csv`.

## A. Required before any external release (5)

| # | Claim | Line | Register | Problem |
|---|---|---|---|---|
| A1 | WP14-C008 | 18 | RPT-03 (OMB COTS file) | At 10,000+ users, USDA licenses only a search and knowledge-retrieval assistant (50,000+). Its word-processor assistant is at 101–1,000. Interior's tool at that scale is a writing tool. Neither department licenses "drafting and summarizing assistants" at that scale. |
| A2 | WP14-C078 | 122 | RPT-14 (LM-170) | The source says 99% of trained pilots are "collateral duty". It does not say they are field staff. |
| A3 | WP14-C155 | 288 | RPT-14 | Same source issue. "Absorbed into field roles" is not supported; "added to existing jobs" is. |
| A4 | WP14-C122 | 211 | RPT-24 (LM-178) | GDPval includes compliance officers (SOC 13-1041), which is in EMST's in-scope set. "Best-known" is an unsupported superlative. |
| A5 | WP14-C177 | 328 | RPT-22 (LM-176) | The source is one Danish study. As written, the claim generalizes it. |

**A1** (line 18)
- Old: `Drafting and summarizing assistants are licensed at 10,000 or more users in EPA, the Department of the Interior and USDA: available at workforce scale, which is not the same as used [8].`
- New: `Commercial AI tools are licensed at 10,000 or more users in EPA (drafting, summarizing and search tools), the Department of the Interior (a writing tool) and USDA (a search and knowledge-retrieval assistant): available at workforce scale, which is not the same as used [8].`

**A2** (line 122)
- Old: `Most of those pilots are field staff who also fly: 99% of the agency's trained pilots fly as a collateral duty [60].`
- New: `Flying is mostly a secondary duty: the agency's national UAS program manager has said that 99% of its trained pilots are collateral-duty pilots, whose primary job is something else [60].`

**A3** (line 288)
- Old: `The strongest evidence comes from drones, which are absorbed into field roles more than they create new ones: 99% of Forest Service trained pilots fly as a collateral duty [60].`
- New: `The strongest evidence comes from drones, which so far are added to existing jobs more than they create new ones: 99% of Forest Service trained pilots fly as a collateral duty alongside another primary job [60].`

**A4** (line 211)
- Old: `GDPval, the best-known benchmark of AI performance on real occupational tasks, includes no environmental occupations [81].`
- New: `GDPval, a widely cited benchmark of AI performance on real occupational tasks, covers 44 occupations; none is in environmental science, forestry or environmental engineering, though it includes compliance officers, an occupation EMST tracks [81].`

**A5** (line 328)
- Old: `Time savings so far show no measurable effect on earnings or hours [79].`
- New: `In Danish data, chatbot time savings have so far shown no measurable effect on earnings or recorded hours [79].`

## B. Recommended (precision; not blocking)

**B1** WP14-C120 (line 210) and reference [80] (line 599). Register: RPT-23 (LM-177). The quoted finding comes from the 2026-05-07 analysis, not the 2025-10-01 report.
- Old: `The Budget Lab at Yale reports no clear labour-market effects yet [80].`
- New: `The Budget Lab at Yale's May 2026 analysis found "no clear effects yet" on the labour market [80].`
- Old (ref): `80. The Budget Lab at Yale. *Evaluating the Impact of AI on the Labor Market (report and tracker)*. 2025-10-01; tracker 2026-10-14.`
- New (ref): `80. The Budget Lab at Yale. *What We Do and Don't Know About How AI is Affecting the Labor Market* (analysis) and AI labor-market tracker. 2026-05-07; tracker updated 2026-10-14.`
- Keep the URL. Change the check note to `(verified; check: LM-177)`.

**B2** WP14-C156 (line 288). Register: RPT-15 (LM-179). Uses fiscal years and GAO's own comparison.
- Old: `When Interior restricted drones, flights fell sharply (BLM's from 3,643 to 528 between 2019 and 2023), and monitoring of one endangered butterfly shifted to on-foot staff covering a much smaller area [91].`
- New: `When Interior restricted drones, flights fell sharply (BLM's from 3,643 in FY2019 to 528 in FY2023), and habitat monitoring for one endangered butterfly shifted to two staff on foot; GAO notes that drones would have covered nine times the area [91].`

**B3** WP14-C082 (line 131). Register: RPT-16 (LM-171). The source says "headcount and budgets".
- Old: `46% reported headcount or budget growth over two years`
- New: `46% said their company had increased sustainability headcount and budgets over two years`

**B4** WP14-C006 (line 18). Register: RPT-02. Applicability is derived from one platform's conversations; it does not measure use.
- Old: `and they show environmental occupations using AI less than their exposure implies [7, 6].`
- New: `and on Microsoft's applicability measure most environmental occupations score below their capability exposure [7, 6].`

**B5** Line 220, known/unknown table (this row is not in `claims_used.csv`). Same issue as B4.
- Old: `| Environmental workers use AI less than their exposure implies |`
- New: `| Environmental occupations score lower on platform-usage measures than their exposure implies |`

## C. No text change, noted

- **WP14-C077** (4,536 drone hours). The FY24 USFS UAS report also gives 4,525 hours in Section 5. 4,536 matches the report's summary table; keep it.
- **WP14-C084** (E2, −36,949), **C094** (AEI shares) and **C006/C169** (25 of 32 below the Eloundou percentile; LM Phase 2 said 20 of 24 on a smaller set) are `verified-partial`. The wording is safe as written.
- **WP14-C169** (line 169): "widest for foresters and forest technicians" is consistent with the data. The largest gaps are forest fire inspectors, forest and conservation technicians, then foresters and natural sciences managers.
- **Upstream (FC lane, not LM):** `docs/research/field-craft/report.md` lines 26 and 209 carry the same "field staff who also fly" / "absorbed into field roles" form as A2 and A3. Fix it there, so it does not re-enter later drafts.
