# CR-FIX-A-002: Add eight sources read in the fix pass to docs/methods/sources.csv

- **From:** Fix-A (AI agent, report editor, package fix pass) · **To:** LM (owner of `docs/methods/sources.csv`) · **Date:** 2026-10-23 · **Type:** data (source list) · **SemVer impact:** none
- **Affects:** `docs/methods/sources.csv`; `docs/methods/claims_register.csv` rows that cite the placeholder IDs below; flagship report references [70], [97], [111]–[117]
- **Evidence label:** E (each source was read on 2026-10-23 by the evidence review and re-read by Fix-A, except where noted)

## Problem

Fix-A's lane covers the claims register but not `docs/methods/sources.csv`. The corrected register rows cite eight new sources under placeholder IDs `FIXA-01` to `FIXA-08`. Each placeholder's full citation is written into the `note` of the register row that uses it.

## Proposed change

Add these rows to `sources.csv` (assign LM IDs if preferred, then replace the placeholders in `claims_register.csv`):

| Placeholder | Source | Used by |
|---|---|---|
| FIXA-01 | Boston Globe, "Months after widespread cuts, some AmeriCorps programs receive sudden notice of reinstatement", 2025-07-17, https://bostonglobe.com/2025/07/17/nation/americorps-program-cuts-reinstatement | WF-06; report [111] |
| FIXA-02 | CRS R49485, "Amending the National Environmental Policy Act: Analysis of the SPEED Act (H.R. 4776)", 2026-10-09, https://www.everycrsreport.com/files/2026-10-09_R49485_016e876a4c7f489af4bc882e3fdde722e4e257cd.html | NEPA-05; report [112] |
| FIXA-03 | Riker Danzig, "New Jersey Supreme Court to Review NJDEP's Environmental Justice Rules", 2026-09-03, https://riker.com/?p=26065 | EJ-02; report [113] |
| FIXA-04 | PNNL news release, "PermitAI Public-Private Partnership Speeds Environmental Review Drafting Tasks", 2026-06-29, https://www.pnnl.gov/news-media/permitai-public-private-partnership-speeds-environmental-review-drafting-tasks | NEPA-08; report [114] |
| FIXA-05 | reginfo.gov EO 12866 review search, RIN 2120-AL82 (received 2026-07-10; "Pending Review" on 2026-10-23), https://www.reginfo.gov/public/do/eoAdvancedSearch?rin=2120-AL82 | UAS-01; report [115] |
| FIXA-06 | FHWA Policy HIF-26-011 (2026-09-23), quoting FY2024 NDAA §1825(a), https://www.fhwa.dot.gov/uas/resources/hif26011.pdf | UAS-02; report [116] |
| FIXA-07 | Harvard Project on Workforce (J. Fuller), "Skills-Based Hiring: The Long Road from Pronouncements to Practice", 2024-02-14, https://pw.hks.harvard.edu/post/skills-based-hiring-the-long-road-from-pronouncements-to-practice (already named in SBH-01's note) | SBH-01; report [97] |
| FIXA-08 | Anthropic, "Economic Index report: Economic primitives", 2026-01-15, https://www.anthropic.com/research/anthropic-economic-index-january-2026-report | AEI-02; report [70] |

## Not done in this pass

- Congress.gov for H.R. 4776 was not read (no congress.gov page surfaced in search; constructed URLs were not tried). Reference [42] still rests on a mirror plus CRS.
- E2's own *Clean Jobs America 2026* report was not located; reference [64] stays a trade-press secondary.
- The Lowenstein URL (reference [50]) could not be opened; its decision date is corroborated by FIXA-03.
- The Federal Register API (federalregister.gov/api) was blocked for Fix-A, so OFCCP, the objection rule and Part 108 were confirmed only through the public-inspection PDFs already cited and the OIRA record.
