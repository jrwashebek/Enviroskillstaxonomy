# CR-FIX-B-003: Register rows needed before the briefs, deck and PD can state four federal HR facts

- **From:** Fix-B (AI agent, briefs/deck/PD editor, package fix pass) · **To:** LM (claims register); FH (federal HR
  facts) · **Date:** 2026-10-23 · **Type:** research and register rows · **SemVer impact:** none
- **Affects:** `docs/methods/claims_register.csv`; `data/v2` SeriesRecord `seed:opm-series/0460` and instrument
  `seed:ins/good-neighbor-authority`; brief R01; deck slide 15; `docs/package/forester_pd_fes_draft.md`
- **Evidence label:** J (raised by package review issues 17, 18 and 20)

## Problem

The package review asks the package to state four facts plainly. None has a claims-register row or a checked source in
EMST's records, so Fix-B softened or omitted each one rather than add an unchecked claim:

| Fact the review asks for | Where | What Fix-B did |
|---|---|---|
| The 0460 Forestry series' positive education requirement, checked against the OPM qualification standard (issue 18(f)) | Forester PD | Kept EMST's series-record flag but said it has not been checked and that the HR office should confirm it; removed "FH judgment pending verification" |
| A checked citation for "Good Neighbor Authority incl. EXPLORE Act amendments" (issue 18(g)) | Forester PD | Dropped the "incl. EXPLORE Act amendments" qualifier from the instrument label in the PD (register row REG-08 marks the EXPLORE Act date as unverified) |
| The Public Lands Corps noncompetitive hiring authority, with its terms and its interaction with EO 14356 (issue 20) | R01 | Kept "corps hiring authorities" and added "EMST has not yet checked those authorities' current terms" |
| SME-QA and USA Hire as the routes where task-based job analysis enters Merit Hiring Plan assessments (issue 17(a)) | Deck slide 15 | Not named (same as Fix-A in the report) |

## Proposed change

Read the primary sources (OPM qualification standard for 0460; the statute or Forest Service guidance on Good Neighbor
Authority as amended; the Public Lands Corps statute and OPM or agency guidance on its hiring authority; OPM's SME-QA and USA Hire
pages), add a register row for each with safe wording and do_not_say forms, and correct the 0460 SeriesRecord's
`editorialNote` and the instrument label if needed.

## After a decision

With rows in place: the PD generator can print the education requirement without the caveat (it reads
`positiveEducationRequirement`) and the full instrument label; R01's HR line can name the Public Lands Corps authority;
deck slide 15 can name SME-QA and USA Hire.
