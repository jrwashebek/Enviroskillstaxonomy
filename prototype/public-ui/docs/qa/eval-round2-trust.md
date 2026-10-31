# Evaluation round 2: trust, honesty and content review

- **Evaluator:** "trust", an AI agent acting as an independent expert reviewer. No users took part, and there are no user quotes. Every judgement here is the reviewer's own **[J]**, measured on the build.
- **Build:** prototype round 2, release 2.0.0-rc.1, production `index.html` and bundle, 31 October 2026.
  - `app/data` matches a fresh `buildModel` projection byte for byte (71 of 71 files).
  - The baseline is the current explorer (`site/_site`).
- **Severity:** Nielsen's 0–4 scale.
- **Working files:** the reviewer's scripts, rendered text (490 pages), exports, screenshots and the sanitizer's before/after change log are in the design working folder.

## Round 1 → round 2 (baseline = current explorer)

| Metric (round 1 method) | Baseline | Round 1 | Round 2 |
|---|---|---|---|
| "Development" claim in a use or HR notice | Every page, plus the HR notice | HR notice on hub, series, class, role tabs, Compare and export | **0 of 515 pages.** A latent copy is still in `core.text.useNotice`. |
| Explore-only content offered for planning or training | Home "check development gaps"; gap-check tool | 3 places | **0** |
| Records citing no source that say "from sources" | Every page | All (37 roles, 1,268 tasks, 102 competencies) | **0 mismatches on 473 record pages** |
| "Not a government website", home, phone (y / page height) | 2,525 / 4,290 (footer) | 5,342 / 6,287 | **8 / 6,494** (release strip, every page) |
| Series page says it is not from OPM | No (footer only) | No (footer only) | **79 of 79** (phone y = 558); class pages 38 of 38 |
| "OPM series" headings and "factor 1" on series pages | Yes | Yes | **0 of 79** |
| Qualify caveat on role-page destinations | 0 | 0 | **60 of 60** |
| Role page and Compare "N of M" for the same pair | No Compare page | Inconsistent, unlabelled | Labelled; Compare explains the difference. Its computed path equals the role page in 60 of 60. |
| Held-content descriptions outside the policy | 6 notes on 2 pages | 6 notes on 2 pages | **0** in 490 pages and all of `app/data` |
| Hold-term search | "No results" for 6 of 6 | Respelled, or "not covered yet" plus "Suggest" | **16 of 30** to Held records only; **14 of 30 still fail** |
| Latent Tribal agent label | — | Present | Removed |
| Internal-code leaks in prose, 11 common pages | 55 | 46 | **1** |
| Role page caveat lines, disclosures closed | n/a | 21; 5 before the first task, in 3 units | 20; **7 before the first task, in 4 units** |
| Readability, all interface blocks (FKGL / SMOG / Dale–Chall) | — | 5.9 / 9.1 / 6.3 | 5.8 / 9.2 / 6.1 |
| HR notice grade | 9.6 | 9.8 | **8.3** |
| HR default-view note grade | — | 17.8 | **8.8** |
| Numbers recomputed from `app/data` | — | 30 of 30 | **86 of 86**, plus 240 of 240 "N of M" checks |
| Role CSV carries pending and HR-basis caveats | — | No | **No** |
| Series CSV carries pending and HR-basis caveats | — | No CSV | **Yes** |
| Series index zeros | — | "0" on 65 series | "0 close · N other" |
| Malformed measures | "(n = 36)", "19.98" | "out of 19 agencies", "80.57" | "from 19 contributing agencies"; at most 1 decimal |

## Verdict per lens

| Lens | Verdict |
|---|---|
| **U5, federal HR and classification** | **Much safer.** "Not from OPM / {State}" sits in the first screen, bands read "(not a classification)", and the duty exports carry every notice. Still there: the USWDS font pairing, the "For HR and classifiers" label, a role CSV with no HR-basis note, and lineage notes in series-link reasons. |
| **U8, seasonal firefighter on a phone** | **Mostly.** Every destination says "doesn't mean you qualify", moves down are dropped with a count, and entry-level comparisons are tagged. But the HR notice now sits above the task list in the default federal view, so the first task is at y = 2,107. |
| **U7, skeptical researcher** | **Partly.** Provenance follows source presence, and every number checked matches. But on-screen record text differs from the release files in 312 strings without saying so. Also: 114 evidence labels were deleted, some sentences broke, and source names expose build-machine paths. |

## Round 1 findings: status

| ID | Status | Evidence |
|---|---|---|
| O1 HR notice claims development | **Fixed** | "This view describes work. It is not ready for training or development plans." |
| O2 Explore-only offered for planning | **Fixed** | Home, role competency table, HR hub and competency notice all say explore only. The levels export carries the caveat. |
| O3 Provenance over-claim | **Fixed** | 0 mismatches on 473 record pages |
| O4 Series and class pages read as government products | **Fixed on the page** | Eyebrow, H1, "not from OPM" (79 of 79), "not FES factor levels", "(not a classification)". The fonts are unchanged. |
| O5 "N of M" | **Fixed** | Stated levels plus the qualify caveat (60 of 60). Compare explains the difference, but at grade 14.4 (N5). |
| O6 Footer implies review | **Fixed** | "No person has reviewed them yet." |
| O7 What's changing | **Fixed** | The caveat now comes first. The page says "EMST makes no forecast…" and the role counts are correct. |
| O8 "Required" beside "may be involved" | **Fixed** | |
| U1 CSV drops caveats | **Partly fixed** | Series CSV fixed. The role CSV is unchanged. |
| U2 Zeros hide links | **Fixed** | |
| U3 Ladders contradict each other | **Fixed** | "Cleared for training or hiring input: not yet" |
| U4 Malformed measures | **Fixed** | |
| U5 Internal codes leak | **Partly fixed** | On the common pages, 46 → 1. Across 490 pages, leaks remain on 150, mostly one lineage note in series-link reasons. |
| U6 Minor | **Partly fixed** | "The order of this list" now sits under the bulleted pending list, so "this list" is ambiguous. |
| T1 Held content described | **Fixed in the prototype, not at source** | No build test covers held-description phrasing. The explorer still shows the notes. |
| T2 Search mishandles hold terms | **Partly fixed** | 14 of 30 trigger queries still say "not covered yet", or respell "treaty". `HOLD_RX` covers only some of the triggers in `governed_content.yaml`. |
| L1 Latent agent label | **Fixed** | |
| Government look-alike | **Partly fixed** | The statement is at y = 8 on every page. The fonts, wordmark and navigation label are unchanged. |

## Over-claiming (round 2 scan)

- **Method:** searched 515 pages for develop-tier, select-tier and eligibility words.
- **Interface text:** every hit is a negation, for example:
  - "not ready for training or development plans" (162);
  - "doesn't mean you qualify" (70);
  - "Cleared for training or hiring input: not yet".
- **Other hits:** tier definitions marked "No record reaches this use yet", or task statements in which recommending is part of the work.
- **Result:** no over-claim found.

## Sanitizer fidelity

- **Method:** a patched copy of `tools/build-data.mjs` recorded every string `scrub()` changed, and its output was byte-identical to `app/data`.
  - The log holds 508 changed occurrences, which are 312 unique pairs.
  - About 100 were read by hand: all code-to-title substitutions, all held-clause removals, all label fixes, and a seeded random sample of 36.

| Outcome | Count | Notes |
|---|---|---|
| Meaning kept, clearer | Most of the sample | Code parentheticals removed. "WP-10 derivation" became "derived". Held clauses removed. Full vocabulary labels (14 strings, 95 occurrences) are all correct. |
| Meaning kept, now awkward | 3 or more | `permit drafting ("Issue environmental permits…" air enactment)`; one keeps the module code "waterq"; "at development stage: deployed" |
| **Evidence labels deleted (N1)** | 72 bare "[J]" and 39 "[E: …]" or "[J; …]" | Split qualifiers lost, such as "for status; J for effect" |
| **Attribution removed (N1)** | 49 | The "SL review:" prefix is dropped, so the agent's review note reads as plain fact. |
| Meaning shifted slightly | 49 | "Requires PS confirmation." became "Requires private-sector review." |
| **Broken text (N2)** | 9 | A comma-code rule deleted ", SL-C04", so the second referent is lost. Also ".." endings, "(titles/dates via):", and lower-case starts after "ADR-0016:" was removed. |
| **Contradiction made visible (N2)** | 1 | A "case records" note now names a competency whose definition excludes inspections. This is a data error; report it to the data owner. |
| Codes left behind | about 20 pages | TX-A to TX-E, LC-C-07, R08, R24, MOD-01, IA-CC-04/05, plus 238 "FH Phase 2 … X1" lineage notes |

Competency titles and task statements were never changed. The policy texts pass through untouched.

## New problems (round 2)

- **N1 (2). The sanitizer erases the line between judgement and fact.** Translate the labels instead of deleting them: "[J]" becomes "(AI agent's judgment)", "[E: …]" becomes "(sourced)" with its qualifier kept, and "SL review:" becomes "State and local review (AI agent):".
- **N2 (2). Broken or distorted sentences, and leftover codes.** Add golden-file tests, resolve every code in a comma list, collapse "..", and map module codes to names.
- **N3 (2). Display text differs from the release without saying so.** Disclose it on About the data, in record provenance and in DATA.md.
- **N4 (2). Source names expose build-machine paths and internal file names.** This affects 5 source records and 11 pages.
- **U1 residual (2).** The role CSV has no pending columns and no HR-basis note.
- **N5 (1).** Compare's "Why this differs" reads at grade 14.4.
- **N6 (1).** The HR notice comes before the task list in the default federal role view: 7 caveat statements in 4 units before the first task. The duplicate AI badge remains.
- **N7 (1).** Latent strings ship in `core.js`: `core.text.useNotice` (a development claim) and `core.text.authorship` (an over-claim).
- **N8 (1) [J].** The release strip echoes the USWDS "official website" banner. Test it in CT-0.
- **N9 (1). Small wording issues:**
  - a possessive on a title in brackets: "…(continuous operations)'s draft profile";
  - the series duties export is framed "Describes work only", while the series page is "Explore only";
  - "S" is unexplained in "Demand by scenario (…, S; not a finding)";
  - "Not for decisions." appears twice in the v1 drawer.

What's changing is clean. 107 signals merge into 73 rows; the reviewer's own grouping rule gives the same 73, no merged group differs in any field, and the counts sum.

## Plain language (interface text only)

| Text | Round 1 | Round 2 |
|---|---|---|
| All blocks: FKGL / SMOG / Dale–Chall | 5.9 / 9.1 / 6.3 | 5.8 / 9.2 / 6.1 |
| HR notice | 9.8 | 8.3 |
| Held policy plus statement (verbatim) | 9.1 | 9.1 |
| HR default-view note | 17.8 | 8.8 |
| Footer authorship | 4.6 | 3.3 |
| New: Compare "Why this differs" | — | **14.4** |
| New: role "N of M" sentence | — | 6.9 |
| New: "not from OPM" | — | 5.3 |

## Tribal hold

- **`#/about/held`:** pass. It shows the policy, the count and the statement only.
- **T1:** fixed on screen, but no build test covers held-description phrasing.
- **T2 (3):** 14 of 30 trigger queries still fail. The failing queries are acronyms, treaty and sovereignty terms, and data-governance principle names; the list is in the reviewer's working folder. The failure mode is unchanged: the page says "not covered yet" and invites submissions.
- **L1:** fixed.

## Government look-alike [J]

The independence statement is the first line of every page. Series and class pages put "not from OPM / {jurisdiction}" in the first screen, and their H1s carry no "OPM" prefix. Still pushing towards "government":
- Public Sans with Merriweather;
- the acronym wordmark;
- the "For HR and classifiers" label;
- the banner-like strip.

The reviewer expects CT-0 to show far fewer critical misreadings than in round 1. That is an expectation, not a test result.

## Numbers

- The round 1 script gives 30 of 37 OK; the 7 differences are format only.
- A new independent script gives **86 of 86**. It covers home, a fire role, Compare, the HR hub, series 0456, the series index, What's changing and the held count.
- The "N of M" check across every listed role gives 60 of 60 against an independent recompute, and 60 of 60 between Compare and the role page.
- Grade bands: all 689 task placements fall in their band's role levels.

## Top 5 remaining problems

1. **T2 (3).** Build the search hold list from all `governed_content.yaml` triggers, and test all 30 queries.
2. **N1 (2).** Translate evidence labels and agent attributions; don't delete them.
3. **N2 (2).** Fix broken sentences and leftover codes, add golden tests, and report the "case records" note to the data owner.
4. **U1 residual (2).** Give the role CSV the series CSV's caveats.
5. **N3 (2).** Disclose the display cleaning. N4, build-machine paths in source names, is a close sixth.
