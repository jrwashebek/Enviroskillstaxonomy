# R4: Evaluation of the EMST Explorer and content audit of the 2.0.0-rc.1 data

Evaluator role: usability and accessibility. Date: 30 October 2026.

**Object.** The built explorer in `/home/claude/emst/site/_site` (764 pages, release 2.0.0-rc.1, build a0d7281), served read-only on 127.0.0.1, and the release data in `/home/claude/emst/dist/2.0.0-rc.1/`. Nothing in `/home/claude/emst` was changed.

**Method and limits.** This is an expert inspection: a crawl, heuristic review, cognitive walkthroughs, scripted search, accessibility and performance tests, and a content audit. No real users took part, so any statement about what users "will" do is judgment **[J]**. Scripts, raw outputs and 85 screenshots are in `research working folder: r4/`; below, `shots/x.png` means `…/research/r4/shots/x.png`. Tools: Chromium 153 through Playwright, axe-core 4.14.0, textstat 0.7.3, BeautifulSoup 4.15.

**Evidence labels:** **[E]** I read or measured it (path given); **[J]** professional judgment (basis given); **[S]** speculation (what would settle it).

---

## Executive summary

The explorer is unusually well engineered for privacy, claims hygiene and baseline accessibility. On the 18 pages I tested it has zero axe-core WCAG 2.2 A/AA violations, with disclosures both open and closed. It makes no external requests, and the display gate fails closed **[E]** (`r4/a11y_results.txt`; `site/reports/browser-checks.json`). The redesign must keep all of that (§8).

The problem is the layer people read. The site states what it doesn't know, but says it so often, and in such internal language, that a first-time user will struggle to find the work itself **[J, based on the counts below and the walkthroughs in §3]**. The 1,317 concrete, well-written task statements are the product's main asset. They are buried under 28,165 "Assessment pending" strings and 2,098 v1 drawers.

### Top 10 problems, ranked by severity × frequency

Severity uses Nielsen's 0–4 scale. Frequency runs from 1 (one page or one user group) to 4 (nearly every page). Both scores are **[J]**; the counts behind them are **[E]**.

| # | Problem | Sev | Freq | Score | Key evidence |
|---|---|---|---|---|---|
| 1 | **Status signals swamp content.** "Assessment pending" appears 28,165 times on 346 pages: a median of 185 per role-variant page. Each task row has 2 "pending" cells, and each task disclosure has 3 "pending" lines plus a v1 drawer. The first chart is empty dotted bars. | 3 | 4 | 12 | `r4/ui_vocab.txt`; `shots/kbd-task-disclosure-open-1280.png`; `shots/role-change-chart-1280.png` |
| 2 | **Internal jargon and machine IDs appear in the interface.** Leaks include "effective-use-tier@1.1.0" (7,101 times, on all 764 pages), "closeMatch", "TXclass:2688", "PJ 050" and "FH Phase 2 … through X1". Codes like "(DB-C49)" sit in 43 of 223 competency definitions. Every page also carries a 387-word footer about "`agentDraft` sub-object, raterType … OBS-4". | 3 | 4 | 12 | `r4/ui_vocab.txt`; footer in `shots/search-forestry-tech-1280.png` |
| 3 | **Role-variant pages are very long and repetitive.** These 121 pages are the core page type. Each has a median of 7,903 words, 42 disclosures and 241 tab stops, and is 27,600 px tall at 390 px. Every task appears twice, and tasks are not headings. | 3 | 3 | 9 | `r4/crawl_summary.txt`; `r4/shots_metrics.json`; `r4/a11y_results.txt` |
| 4 | **Search is brittle.** It matches exact substrings of titles and alternative labels, and shows no snippets. 18 of 50 realistic queries return "No results", including "foresty", "GS-0460", "Rx burn", "UAS", "veteran", "hotshot" and "water quality technician". "GIS" matches inside "ecoloGISt", and record IDs can't be searched. | 3 | 3 | 9 | `r4/search_results.txt` |
| 5 | **Navigation runs one way and is flat.** No competency page links to any role (0 of 223), and 656 of 1,317 tasks belong to no role. The 17 job families and the work functions are never used for navigation. The roles index is a flat A–Z list whose 121 variant links say only "Federal government", "State government" and so on. | 3 | 3 | 9 | `r4/content_audit.txt` §5–6; §1.2 |
| 6 | **Use-tier and evidence labels contradict each other and aren't explained in place.** The roles index says "exploratory" while each role says "describe". Indicators read "use class develop; effective use tier exploratory". Every role says "Evidence: S speculation". Badges don't link to any explanation. | 3 | 3 | 9 | `shots/roles-index-1280.png`; `shots/competency-contracts-1280-full.png` |
| 7 | **Record text reads at a postgraduate level.** Median Flesch-Kincaid grade is 14.2 for tasks, 17.4 for competency definitions and 19.7 for role definitions. 77% of tasks score above grade 12. | 2 | 4 | 8 | `r4/content_audit.txt` §2 |
| 8 | **The mobile experience is weak.** At 390 px the 10-item nav wraps to 4 lines, with no menu. The first action on the home page starts 986 px down. The chart's labels shrink to about 5 px and clip, and nearly vanish in forced-colours mode. | 2 | 4 | 8 | `shots/home-390.png`; `shots/role-change-chart-390.png`; `shots/forced-colors-role-chart-1280.png` |
| 9 | **The full 515 KB USWDS stylesheet blocks rendering on every page.** On Slow 3G, first paint takes 14.8–25 s uncompressed, or about 5.4 s with gzip. It is unknown whether the host will compress. | 2 | 4 | 8 | `r4/perf_results.txt`; `r4/perf_gzip_results.txt` |
| 10 | **HR views often lead nowhere.** 42 of 79 federal-series pages have no role and no competency. Only 4 jurisdictions have class views, and nothing shows a class and a role side by side. | 3 | 2 | 6 | `shots/federal-series-0101-empty-1280.png`; Appendix A |

**Close behind:**

- "Challenge this" drops the user's context (score 6).
- Record IDs are shown only at the bottom of pages and don't resolve yet (6).
- Pathway overlap is always computed at the lead level (5).
- Small text bugs (4).
- The accessibility statement claims a screen-reader checklist that the conformance report says hasn't been run (2).

**What to change first [J]:**

- Lead with the work (tasks, competencies, levels).
- Show status once per context, in plain words, linked to an explanation.
- Move machine provenance into a "technical details" layer and the downloads.
- Make search forgiving.
- Link both ways, and let people browse by job family and employer type.

---

## 1. Information architecture

### 1.1 Inventory and depth [E] (`r4/crawl.py`, `r4/crawl_summary.txt`)

A breadth-first crawl from `/` reached 763 of the 764 HTML files. The only orphan is `/404.html`, and there are no broken internal links.

| Page type | Count | Depth | Median / max KB (raw) | Median words in main | Median disclosures |
|---|---|---|---|---|---|
| Competency | 223 | 2–4 | 27 / 86 | 1,679 | 9 |
| Role variant ("How it is changing") | 121 | 2 | 111 / 160 | 7,903 | 42 |
| Gap check for a variant | 121 | 2 | 92 / 170 | 4,745 | 34 |
| Pathway for a variant | 121 | 2 | 12 / 25 | 514 | 0 |
| Federal series profile | 79 | 2 | 9 / 41 | 296 | 0 |
| State or local class view | 38 | 2 | 15 / 17 | 773 | 1 |
| Role (variant chooser) | 31 | 2 | 12 / 14 | 424 | 0 |
| Module editorial section | 11 | 3 | 7 / 10 | 84 | 0 |
| Gap-check tools (chosen competencies; team grid) | 2 | 2 | 502 / 975 | 22,848 | 231 |
| Hubs and singletons | 17 | 0–2 | — | — | — |

Pages by depth: 1 at depth 0, 14 at depth 1, 681 at depth 2, 60 at depth 3 and 7 at depth 4.

The site is shallow and wide: almost everything is 2 clicks from home **[E]**. Depth is not the problem; the hub lists are. The roles index is 11,928 px tall at 390 px, and the federal-series index is a flat list of 79 rows **[E]** (`r4/shots_metrics.json`).

### 1.2 Navigation and labels [E]

**Main nav, same on every page:** Home · Roles · Gap check · Pathways · What's coming · Federal series · State and local classes · Competencies · Evidence · Search.

**Elsewhere:**

- Footer only: Download and cite, Challenge a judgment, How to read the evidence, Privacy, Accessibility, Security.
- Modules: linked only from the competencies hub.
- Breadcrumbs appear on every page.
- Each variant page has a switcher: "How it is changing · Gap check · Where it can lead".

**One view, several names [E]:**

- Pathways: "Pathways" (nav), "Where roles can lead" (h1), "Where it can lead" (switcher), "Explore where a role can lead" (home).
- Gap check: "Gap check", "Check development gaps" and "Check gaps" (the last appears 14 times on a pathway page).
- Evidence: the nav says "Evidence" but the page is titled "How to read the evidence". "Evidence" reads like "sources" **[J]**.

**Structure as navigated [E]:**

- Home → Roles (flat A–Z list) → Role → Variant → [How it is changing | Gap check | Where it can lead].
- Competencies → three lists by kind (practice 136, transversal 18, knowledge area 9) → Competency → Tasks, shown as disclosures.
- Federal series → 79 rows → Series.
- State and local classes → 38 rows in 4 jurisdictions → Class.

**What the structure lacks [E]:**

- The bundle's 17 job families and 12 primary work functions never appear as navigation.
- Links run one way. Roles link to competencies, but no competency or task links back to a role. The grep found 0 role links on all 223 competency pages.
- Repeated link texts have different targets. On the roles index, "State government" has 30 targets and "Federal government" 29 (`r4/linktext.py`).

### 1.3 Screenshots [E]

Each key type was captured at 1280 and 390 px wide, as `-1280.png`, `-390.png` and `-full.png` where the page is under 9,000 px tall. Pages captured: `home`, `roles-index`, `role-forester`, `role-variant-forester-federal`, `role-variant-frt-ngo`, `competencies-index`, `competency-contracts`, `federal-series-index`, `federal-series-0460`, `federal-series-0101-empty`, `state-classes-index`, `state-class-tx-2682`, `pathways-index`, `pathway-wildfire-federal`, `gap-check-index`, `gap-check-frt-federal`, `whats-coming`, `evidence`, `search`, `download`, `challenge`, `modules`.

At 390 px, the release banner, site title and wrapped nav push every h1 down to 308–374 px. The home page's first h2 starts at 986 px (529 px at 1280). A role-variant page is 27,634 px tall, and What's coming is 42,964 px **[E]**.

---

## 2. Heuristic evaluation

**Heuristics:** Nielsen H1–H10, plus three content heuristics: C1 plain language, C2 information scent, C3 honesty of status displays. Severities are **[J]**; evidence is **[E]**.

| # | Heuristic | Page / element | Sev | Evidence | Recommendation |
|---|---|---|---|---|---|
| 1 | C3, H8 | Role variant: task table and disclosures | 3 | The forester federal page says "Assessment pending" 215 times; every row reads "Assessment pending (job analysis)" plus "Assessment pending" (`shots/kbd-task-disclosure-open-1280.png`) | State once per page that no task is rated yet, and why. Drop empty columns until a value exists. Use one pending line per task. |
| 2 | C3, H1 | Role variant: first section, "How the work is shifting" | 2 | Dotted bars "0 of 19 assessed" … "0 of 35 assessed" (`shots/role-change-chart-1280.png`) | Replace with one sentence until there is data, and lead with tasks. |
| 3 | C3, H4 | Roles index; competencies; indicators | 3 | The summary says "Use tier: exploratory (lowest tier among the records counted)" while each role says "describe". Indicators read "(unaided; use class develop; effective use tier exploratory; evidence J, unreviewed)". | Show one tier per context, translated into uses ("OK for planning and curriculum mapping; not for hiring or training records"). Hide the declared ceiling. |
| 4 | C3, C1 | Role badges | 2 | "Evidence: S speculation; AI-agent draft, unreviewed" (`shots/role-forester-1280.png`) | Say "Drafted by AI, not yet checked by people" and link it. Keep E/J/S in a details layer. "Speculation" reads as "made up" **[J]**. |
| 5 | C1, H2 | Badges, chart notes, HR views | 3 | Screen-reader-only text ", computed by effective-use-tier@1.1.0" (7,101 times). Also "Computed with rule role-change@0.1.0", "Generated by pipelines/views/federal_series_profile.py@0.3.0" and "TXclass:2688 (relatedMatch, 2026-10-23)". | Put provenance in a collapsed "How this was computed" section and in the downloads. Show match types as words. |
| 6 | C1 | Competency definitions | 3 | 43 of 223 contain agent codes, e.g. "Excludes facility operation (DB-C16) and producer-responsibility administration (DB-C17)" | Remove the codes from definition text and keep them as data. |
| 7 | C1, H8 | Footer, every page | 2 | A 387-word median footer: "…sit only in an `agentDraft` sub-object, with their raterType, validationStatus … *_status columns" | Cut it to 3 lines (what, who, how to comment). Move the data notice to Download. |
| 8 | H2, C1 | Variant headers | 2 | A field technician is labelled "Authority position: Resource manager · Land trust". "In short" is the same template sentence ("acts as resource manager for lands, waters or programmes the employer holds") on 79 of 121 variants. | Write one variant-specific sentence each. Rename "Authority position" in plain words. |
| 9 | H2 (bug) | Local variants of wildland fire, field resource technician and hydrologist | 2 | Shows "Special district (water": the label "Special district (water, sanitation, air, fire, park, mosquito control)" is cut at the first comma (`vocab/sector_actors.yaml:38`) | Fix it. A fire role labelled "water" damages trust. |
| 10 | H8, H7 | Role-variant page length | 3 | 7,903 words median; tasks in the table *and* in 35 disclosures; 27,634 px at 390 px; 59 Tabs to reach the first task | Show one task list with expandable detail, grouped by duty, with a filter by level (entry, journey, senior, lead). |
| 11 | H6, C2 | Competency pages | 3 | No "roles that use this"; 0 of 223 link to a role | Add reverse links to roles, variants and series, and show each task's roles. |
| 12 | C2 | Roles index | 2 | 31 roles A–Z; variant links named only by employer type | Group by job family. Filter by employer type. Name each link with its role. |
| 13 | H7, C2 | Search | 3 | §4: 18 of 50 queries return nothing; 2 return false positives | Match on token prefixes with small typo tolerance. Add synonyms, strip "GS-" prefixes, look up IDs, group results by type and add snippets. |
| 14 | H9, H10 | "No results." | 2 | No suggestion or fallback is offered | Offer "Did you mean", links to browse, and a "suggest a synonym" route to Issues. |
| 15 | H7 | Search access | 2 | Search lives only on /search/, 14 Tabs from the top | Add a header search box. It can stay local. |
| 16 | C2, H9 | Federal series | 2 | 42 of 79 pages say both "No federal role variant is crosswalked to this series" and "No established core competency is associated" (`shots/federal-series-0101-empty-1280.png`). The index doesn't flag them. | Mark these "no EMST content yet" in the index, or filter them out. |
| 17 | C2 | State classes | 2 | Only Texas (27), Washington (8), Philadelphia (2) and Lewis County (1) | Say the coverage up front. Offer a "compare your own class" method. |
| 18 | H3, H7 | "Challenge this" | 3 | Links to the generic /challenge/ page, so the record ID stays behind. There is no copy button, and filing needs a GitHub account. | Per-record "Report a problem" with copy buttons for ID, release and page, pre-written issue text, and a link to the repo's issue-template chooser. |
| 19 | H6 | Record ID | 2 | "emst:core/CMP-X72VMYB" appears only in the last section. The w3id IRI isn't shown, and the URL uses a different form (`/competencies/cmp-x72vmyb/`). | Put the ID, the IRI (marked "reserved, not yet resolvable") and a citation line by the title, with a copy button. |
| 20 | H10, C1 | /evidence/ | 2 | Shows raw placeholders: "α = {alpha} (95% CI {ci_lower}–{ci_upper}; {n_units} units)"; keys like "assessment_pending"; "Krippendorff's alpha whose lower 95% bound…" | Rewrite for general readers. Move the gate rules to an appendix. |
| 21 | H10, C3 | Badges | 2 | Badges are spans, not links. The only links to /evidence/ on a role page are the 2 in the footer. | Link the first badge on each page, or add a "What do these labels mean?" disclosure (no hover). |
| 22 | H4 (bugs) | Assorted | 1 | "Practice competencys" (competencies hub and gap check); "1 results."; "journey\|senior" on Texas classes; "Ghg nature data controller"; "v1 vector: none (?)"; duplicate identical v1 rows | Fix in templates and copy. |
| 23 | C3 | /about/accessibility/ | 2 | Claims "a manual keyboard and screen-reader checklist run before each release". `site/ACR.md` lines 32–38 list screen-reader testing as "Not yet done". | Make the statement match the ACR. |
| 24 | H8 | Mobile header; SVG chart | 2 | Nav wraps to 4 lines; chart labels about 5 px and clipped ("0 of 35 assessec"); invisible in forced colours | Use a menu button below about 640 px. Draw the chart in HTML or `currentColor`. |
| 25 | H7 | Exports | 2 | Federal-series and class views have no export ("DOCX … PD skeleton … not built"). Downloads have no roles CSV, and the JSON-LD bundle isn't linked. | Add a CSV for each view, a print layout, role and variant CSVs, and a bundle link. |
| 26 | C1 | Indicator annotations | 2 | Every indicator carries inline text such as "(assisted; distinguished by augmented practice (tools and ai); use class develop; …)" | Show as small labelled fields in a details layer. |
| 27 | H2, C3 | Pathways hub and pages | 2 | Destinations shown as "PJ 050", "PJ 054". "no friction records in this build (that does not mean there are none)" repeats after every sector. | Name the destinations. Say "no frictions recorded" once per pathway. |
| 28 | H5 (positive) | Gap check | 0 | Asks to confirm "Clear everything" when answers are unsaved, and warns on `beforeunload` (`assets/js/gap-check.js` 207–226) | Keep. |

---

## 3. Cognitive walkthroughs

At each step I asked four questions: (1) does the user know what to do, (2) can they see the control, (3) do they connect it to their goal, (4) do they understand the feedback? The Q1–Q4 column marks each answer in order, so "✓✓✓✗" means the first three pass and the fourth fails. Judgments are **[J]**, based on the rendered pages **[E]**.

### 3.1 U5, federal HR specialist: draft duties for a GS-0460 forester position description

| Step | Q1–Q4 | Notes |
|---|---|---|
| 1. Nav "Federal series" | ✓✓✓✓ | The hub copy speaks to "federal HR specialists, classifiers and training officers". |
| 2. Find 0460 among 79 rows | ✓✓✓✓ | Only the code is a link. In search, "GS-0460" fails but "0460" works. |
| 3. Read the 0460 page | ✓✓✓✗ | The HR disclaimers come first, which suits this user. Then come "close fit, agent confidence (uncalibrated) 0.85" and "Generated by pipelines/views/…py@0.3.0". |
| 4. Find the major duties | ✓✓✓✗ | Close to a position-description skeleton: duties grouped by competency with tasks underneath, by "indicative" GS band; "% time: set by the supervisor"; a Factor 1 knowledge list. But a module label repeats 14 times, and the education flag is "judgment by … an AI agent; not yet checked against the OPM qualification standard". |
| 5. Get the text into a draft | ✗✗✗✗ | No copy, CSV or DOCX for this view. Only manual selection or browser print. |

**Outcome: partial.** The content fits the task; the output format doesn't.

### 3.2 U1, corps programme lead: what a "field resource technician" does, and what to train first

| Step | Q1–Q4 | Notes |
|---|---|---|
| 1. Home → "See how a role is changing" | ✓✓✓✓ | The home cards are clear. |
| 2. Find the role in the A–Z list | ✓✓✓✓ | About the 14th entry. The list is 11,928 px on mobile. |
| 3. Role page | ✓✓✓✓ | "Also called: biological science technician, natural resource technician, field technician" confirms the right role. |
| 4. Choose a variant (NGO) | ✓✓✗✗ | "Authority position: Resource manager · Land trust" won't describe a corps. It is also unclear whether "Conservation corps member" is the better fit. |
| 5. Read the work | ✓✓✓✗ | 35 concrete tasks, each with two "pending" cells. "In short" is boilerplate. |
| 6. Decide what to train first | ✗✗✗✗ | Importance and needed-at-entry are gated, so nothing is ordered. The "Formation task" column is explained only far below. The gap check ranks one person's gaps, which doesn't answer a programme question. |

**Outcome: understands the role; fails "what to train first".** An entry-level view would answer it while still respecting the gate. It would list entry targets and formation tasks first, labelled "editorial draft, not a priority ranking".

### 3.3 U8, seasonal wildland firefighter: find year-round roles that overlap their skills

| Step | Q1–Q4 | Notes |
|---|---|---|
| 1. Search "firefighter" | ✓✓✓✓ | One result, "Wildland fire operations (crew to supervisor)", found through an alternative label. "hotshot", "seasonal" (tasks only) and "veteran" fail; "engine" returns engineers. |
| 2. Federal variant → "Where it can lead" | ✓✓✓✓ | The switcher is visible. |
| 3. Read the destinations | ✓✓✗✗ | Destinations: fuels specialist, fire intelligence analyst, **conservation corps member**, park ranger. Overlap compares "this role's targets at its **lead** level", which overstates it for an entry-level seasonal worker, and the user can't change the level. The local variant shows "Special district (water". |
| 4. Year-round? | ✗✗✗✗ | No information on seasonality, tenure, pay, location or hiring authority. |

**Outcome: fails the core goal.** Pathways should take the user's level as input and say plainly what EMST doesn't cover.

### 3.4 U6, community-college curriculum designer: competencies and proficiency levels for a water-quality technician programme

| Step | Q1–Q4 | Notes |
|---|---|---|
| 1. Search "water quality technician" | ✓✓✓✗ | "No results." |
| 2. Search "water quality" | ✓✓✓✓ | 9 hits: 2 competencies and 7 tasks; no role. |
| 3. Competency page | ✓✓✓✓ | The strongest page for this goal: observable indicators for L1–L4 with criteria ("…post-use checks within the program's acceptance limits"). |
| 4. Find the programme's other competencies | ✗✗✗✗ | The page doesn't link to the roles that use this competency. The right role, "Monitoring and data technician" (also called "hydrologic technician"), can only be found by guessing. |
| 5. Take the set away | ✓✓✗✗ | Only whole-taxonomy CSVs, or the gap check's priorities CSV. No way to save a chosen set of competencies with their levels. |

**Outcome: partial.** The level content is excellent, but assembling a set needs reverse links and a role-to-programme view.

### 3.5 U4, state training officer: compare their state's class with an EMST role

| Step | Q1–Q4 | Notes |
|---|---|---|
| 1. Nav "State and local classes" | ✓✓✓✓ | |
| 2. Find their class | ✓✓✓✗ | Only 4 jurisdictions are covered, so for most states this is a dead end. |
| 3. (Texas) Natural Resources Specialist I | ✓✓✓✗ | "No EMST role variant is mapped … at closeMatch or stronger". The candidates include a "partial fit … 0.2" for Water and wastewater treatment operator. |
| 4. Compare duties | ✗✗✗✗ | Class duties are linked, not stored, so there's no side-by-side view. The user needs two tabs (PDF spec and role page). |

**Outcome: fails for most states; laborious for the four covered.** One option that respects the licence and privacy rules: put the role's tasks next to a local-only "paste your class duties" panel **[J]**.

### 3.6 U7, researcher: download the data and cite one competency by its persistent ID

| Step | Q1–Q4 | Notes |
|---|---|---|
| 1. Footer "Download and cite" | ✓✗✓✓ | The link is only in the footer, below a 387-word block. |
| 2. Download | ✓✓✓✗ | CSVs exist for competencies, tasks, indicators, links, mappings and the HCM import. **No role or variant CSV**, and the JSON-LD and SKOS files aren't linked. The CSVs show `use_tier_ceiling` next to `effective_use_tier`, which is good. |
| 3. Cite a competency | ✓✗✗✗ | Only a release-level citation is offered. The ID is at the page bottom. The IRI appears only in the CSV. Per ADR-0010, w3id IRIs are "reserved, not resolvable", and IDs stay "candidate" until 2.0.0. |
| 4. Search the ID | ✗ | No results. |

**Outcome: data partly obtained; citation by persistent ID isn't truly possible yet**, and the page should say so where it offers the citation.

### 3.7 U9, practitioner: report that a task statement is wrong

| Step | Q1–Q4 | Notes |
|---|---|---|
| 1. Open the task disclosure | ✓✓✓✓ | |
| 2. "Challenge this (quote task ID emst:forest/TSK-XAADCTA)" | ✓✓✓✗ | Opens the generic /challenge/ page. |
| 3. Copy the ID | ✗✗✓✗ | The user has to go back to find it, and there's no copy control. |
| 4. Open an issue | ✓✓✓✗ | Needs a GitHub account. The link goes to the issues list, not to a template. |

**Outcome: likely abandonment by people without GitHub [J].**

### 3.8 Anyone: understand what "assessment pending" and "exploratory" mean

| Step | Q1–Q4 | Notes |
|---|---|---|
| 1. Home status box | ✓✓✓✓ | Explains "assessment pending" in one sentence. |
| 2. Meet the labels on a role page | ✓✓✗✗ | Plain spans, with no link or explanation nearby. |
| 3. Find /evidence/ | ✓✓✗✓ | The nav word "Evidence" doesn't promise definitions. |
| 4. Read it | ✓✓✓✗ | The use-tier table is clear. The display-gate section loses lay readers (Krippendorff's alpha, `assessment_pending`, `{alpha}`). |

**Outcome: partial.** The definitions exist but aren't connected to where the labels appear.

---

## 4. Search test [E] (`r4/search_test.js`, `r4/search_results.txt`)

**How search works.** The index has 1,817 entries embedded in /search/ (353 KB raw, 89 KB gzip). Every query term must appear as a substring of the title plus alternative labels. Results are capped at 50 and show title and type only, and tasks link to their competency page. Nothing is sent anywhere, which is deliberate.

| Query | Result | Verdict |
|---|---|---|
| range con | 6; Rangeland management specialist first, then tasks about "out-of-range entries" | Good top hit, noisy tail |
| rangeland | 8 (role, 2 variants, 0454, 2 competencies, 2 tasks) | Good |
| GS-0454, GS-0460 | none | **Fail** ("GS-" prefix not handled) |
| 0454, 0460 | 1 each | Good |
| forestry tech | 0462 series only; misses Field resource technician | Partial |
| fire | 52 (shows 50), types interleaved | OK |
| prescribed burn / prescribed fire | 3 / 10 | Good |
| Rx burn | none | **Fail** |
| NEPA | 2 (role via alternative label, 1 competency); no tasks | Thin |
| wetland delineation | 1 competency | Good |
| GIS | 43, including Ecologist, Hydrologist, Wildlife biologist | **False positives** ("-logist") |
| drone / UAS | 1 task / none | Thin / **fail** |
| water quality | 9 | Good |
| water quality technician | none | **Fail** |
| permit writer | 5 | Good |
| seasonal | 7 tasks | No role guidance |
| corps | 5 | Good |
| veteran, hotshot, game warden, environmental scientist | none | **Fail** |
| foresty, hydrolgist | none | **Fail** (no typo tolerance) |
| firefighter | 1 role | Good |
| park ranger | 10; five Texas classes rank above the EMST role | Ranking |
| chainsaw, sawyer, invasive, stormwater, EHS | 4, 1, 10, 8, 2 | Good |
| Texas / Washington / California | 27 / 9 / none | Shows the coverage gap |
| TX 2682; emst:core/CMP-X72VMYB; CMP-X72VMYB; 19-1032 | none | **Fail** (codes and IDs aren't indexed) |
| O\*NET | 34 hits on "network" | **False positives** ("\*" is stripped) |
| assessment pending, exploratory | none | Help terms aren't indexed |

**Summary [E].** 18 of 50 queries returned nothing, and 2 more returned mostly false positives. Successful queries depend on alternative labels. Those exist for 84% of roles and 79% of competencies, but for no task, variant or indicator. Results never show why a record matched, and one status line reads "1 results."

**[J]** A forgiving local search would fix most of these failures without any network request. It needs token prefixes, edit distance 1–2, and a curated synonym table: Rx → prescribed; UAS → drone; GS-0460 → 0460; range con → range conservationist; plus a "not covered" list such as game warden.

---

## 5. Accessibility

### 5.1 axe-core, WCAG 2.0, 2.1 and 2.2 A/AA plus best practice [E] (`r4/a11y.js`, `r4/a11y_results.txt`)

I ran axe on 18 pages, with every `<details>` closed and again with all open. Playwright's `bypassCSP` was needed to inject axe; the site's CSP correctly blocks inline scripts. Pages covered:

- home and the roles, competencies, series and pathways hubs;
- a role and two role variants;
- a competency, series 0462 and a Texas class;
- a pathway, a variant gap check, the team grid and the 975 KB chosen-competencies page;
- What's coming, search with results, and the evidence page.

**Results:**

- **Violations:** 0 on all 18 pages, in both states.
- **Incomplete:** color contrast on SVG chart text (8 nodes per role-variant page), and 154 nodes on the chosen-competencies page when open.
- **Best practice:** `landmark-unique`. Up to 59 table regions per role page share the label "v1 prior codes for this task".
- **Target size:** native radios are 13×13 px, but their labels are clickable and 24 px tall, so WCAG 2.5.8 is met.

### 5.2 Keyboard pass [E] (`r4/keyboard.js`, `r4/keyboard_results.json`)

| Page | Findings |
|---|---|
| Role variant | Skip link is first, visible, and moves focus into main. A 4 px focus ring showed on all 125 stops checked, and no hidden element took focus. Enter and Space toggle disclosures. **Burden:** 241 focusable elements; 59 Tabs to the first task disclosure; 101 to the first competency. |
| Gap check | Logical order. Arrow keys work inside radio groups. "See summary" moves focus to the h2 "Your development priorities", and a polite live region is present. 373 focusable elements. |
| Search | 14 Tabs to reach the input. Results are announced by a `role="status"` region. Enter doesn't change the URL (by design). Tab moves into the results. |

### 5.3 Reflow at 320 px, zoom and forced colours [E]

- **Reflow:** no page-level horizontal scroll on any page at 320 px. Wide tables scroll inside labelled regions, which the WCAG 1.4.10 data-table exception allows.
- **Zoom:** at 640 px (200% of 1280) nothing overflows.
- **Length:** at 320 px with disclosures open, a role variant is 79,814 px tall and the chosen-competencies page 413,328 px.
- **Chart at 390 px:** labels are about 5 px and clipped. The chart is `aria-hidden` and has a table copy, so this is a usability problem rather than a conformance failure **[J]**.
- **Forced colours:** the chart's text nearly disappears.

### 5.4 Headings and landmarks [E]

- **Headings:** every page has exactly one h1 and no skipped levels.
- **Landmarks:** a "Release and use notice" region, header, nav "Main", nav "Breadcrumb", main and footer. Variant pages add nav "Views for this role variant".
- **Gaps [J]:**
  - Content units aren't headings. A role page's 35 tasks are `<summary>` elements (the page has 9 h2 and 3 h3). A gap check's 24 competencies are fieldset legends, and the series and search hubs have only an h1. Screen-reader users can't jump from task to task.
  - Screen-reader noise: ", computed by effective-use-tier@1.1.0" is read after every tier badge, 43 times on one page.
  - Ambiguous link names: "State government" ×30 and "Check gaps" ×14 out of context. The ACR already lists 2.4.4 as partial.

### 5.5 What the explorer's own checks guarantee, and what they miss [E] (`site/README.md`, `site/reports/*.json`, `site/ACR.md`)

**Guaranteed:**

- On every page, by a static build check:
  - a CSP, no inline code and no external fetches;
  - one h1, no skipped levels, a `lang` attribute and a unique title;
  - a release ID, use notice and badges on every figure;
  - the HR disclaimers and the "pending" and "never a recommendation" wording;
  - no retired claims, Tribal-hold terms, emails or phone numbers.
- On 71 of 764 pages (9%), in a browser:
  - axe A/AA with disclosures closed and open;
  - no requests;
  - reflow and text spacing;
  - visible focus on the **first 12** Tab stops.
- For the tools:
  - the gap check makes no request and changes no storage or URL;
  - the team grid needs at least 5 files;
  - typing in search makes no request.

**Missed [J]:**

1. **Comprehension.** No readability, jargon or ID-leak check; internal codes pass every test.
2. **Volume.** No budget for page length, repetition or tab stops.
3. **Real assistive-technology use.** No screen-reader testing yet (the ACR says so). That would catch screen-reader-only noise, missing task headings and duplicate region names.
4. **Focus after the 12th Tab stop**, and the number of Tabs a task needs.
5. **Forced colours and chart legibility** at small widths.
6. **Findability.** Search quality, empty dead-end pages (the 42 series), and copy bugs such as "competencys" and "Special district (water".
7. **Page coverage:** 693 pages rely on template sameness.
8. **Accuracy of public statements**, such as the accessibility page against the ACR.

---

## 6. Performance [E] (`r4/perf*.js`, `r4/perf_sizes.py`)

**Requests:** 6–7 per page: the HTML, `uswds.min.css`, `emst.css`, `emst.js` and 2–3 woff2 fonts. All JavaScript on the site totals 20.7 KB.

**Page weights:**

| Item | Raw | gzip |
|---|---|---|
| All 764 HTML pages | 39.4 MB | 6.6 MB |
| Largest page: `/gap-check/competencies/` | 975 KB | 115 KB |
| `/search/` | 360 KB | 93 KB |
| Largest role variant | 160 KB | 16 KB |
| **`uswds.min.css`, loaded on every page and render-blocking** | **515 KB** | **60 KB** |

**Load times** at 390 px with the cache disabled, using CDP network emulation:

| Profile | Serving | First contentful paint | Load | Transferred |
|---|---|---|---|---|
| Slow 3G (2,000 ms RTT, 400 kbps) | uncompressed | 14.8 s (most) – 25.4 s | 17.6–35.8 s | 582–1,551 KB |
| Slow 3G | gzip | 5.4–5.7 s | 8.2–8.6 s | 123–222 KB |
| Fast 3G (562 ms, 1.44 Mbps) | uncompressed | 4.2–7.1 s | 5.0–10.0 s | 582–1,551 KB |
| Fast 3G | gzip | 1.55–1.64 s | 2.3–2.5 s | 123–222 KB |
| No network throttle, CPU 4× slower | — | DOMContentLoaded 0.25–0.48 s | — | — |

With the CPU throttled, search answered in 262 ms, including its 150 ms debounce.

**[J]** Rendering is cheap; the network cost is almost all the full USWDS stylesheet. Whether the eventual host compresses is unknown **[S: settle by checking `Content-Encoding` on the real host]**. Even with gzip, field users on weak signal wait about 5 s on every page. The redesign should ship only the CSS it uses, load one font or use system fonts, and split the search index and the 975 KB page.

---

## 7. Content audit of the release data [E] (`r4/content_audit.py`, `r4/content_audit.txt`, `r4/content_audit.json`)

Source: `emst.bundle.jsonld`, which has 13,562 graph nodes.

### 7.1 Lengths (words: median, p90, max)

| Field | Median | p90 | Max |
|---|---|---|---|
| Task statement (identical to prefLabel in all 1,317 tasks) | 19 | 22 | 27 |
| Indicator statement | 20 | 24 | 30 |
| Knowledge statement | 18 | 26 | 33 |
| Competency label | 9 | 11 | 15 |
| Competency definition | 46 | 63 | 106 |
| Competency statement | 43 | 50 | 57 |
| Role label | 4 | 6 | 6 |
| Role function statement | 15 | 22 | 25 |
| Role definition | 37 | 45 | 50 |
| Variant definition | 20 | 27 | 41 |
| Job family definition | 15 | 16 | 16 |

**[J]** Tasks have no short label, so every list and search result shows a sentence of about 134 characters. Each competency page also shows a definition and a statement that say much the same thing, each about 45 words long.

### 7.2 Reading level

| Text | FK grade, median | Flesch Reading Ease, median | Share above grade 12 | Share above grade 16 |
|---|---|---|---|---|
| Tasks (1,317) | 14.2 | 27 | 77% | 25% |
| Indicators (1,699) | 13.9 | 32 | 78% | 24% |
| Knowledge statements (51) | 13.4 | 37 | 67% | 22% |
| Competency labels (223) | 14.3 | 8 | 67% | 35% |
| Competency definitions (223) | 17.4 | 12 | 98% | 69% |
| Competency statements (223) | 24.0 | −1 | 100% | 99% |
| Role function statements (37) | 14.2 | 24 | 76% | 27% |
| Role definitions (37) | 19.7 | 10 | 97% | 81% |

**Caveat [J].** These formulas assume running prose, and each EMST item is one long sentence, which inflates grades. Competency statements are semicolon-chained lists. Treat the grades as relative warnings, not precise values. The high share of long words (median 0.25 of task words) is a real barrier for U2 and U8. I didn't re-check current federal plain-language guidance online.

**Hardest to read:**

- Task, FK 24.9: "Establish unified command with cooperating agencies for a multi-jurisdiction environmental emergency, recording each agency's authority, objectives and delegated responsibilities."
- Task, FK 23.3: "Evaluate a sponsor-prepared environmental document for adequacy and objectivity, returning specific deficiencies the preparer must correct before adoption."
- Competency definition, FK 31.0 (62 words): "The capability to document the reasons for a decision as it is made, including alternatives, boundaries, responses to substantive comments, consultation outcomes and the provenance of analyses (AI-assisted content included), so that a court, inspector general or successor can reconstruct…"
- Competency definition, FK 28.7: "The capability to determine and document the sensitivity of rare-species locations, cultural-resource information, personal data and information held under data-holder agreements; to apply generalization, withholding or controlled access…"
- Role definition, FK 25.6: "Regulatory role that develops enforcement cases from referral to settlement or litigation: investigating violations, assembling evidence files, calculating penalties, negotiating consent orders and testifying…"

**Easiest to read, for contrast:** "Lead a small crew through a field day, matching tasks to skill and checking novice work early and often" (FK 6.0).

### 7.3 Acronyms and jargon

- **Acronyms:** 49 distinct acronyms in public text; 326 of 3,467 records contain at least one. Most frequent: AI (511), QC (22), QA (14), DNA (12), GHG (5). They appear in 8% of tasks and indicators but 34% of competencies.
- **Internal codes in public text:** DB (27), TX (8), SL (7), C02 (6), FC (5), CAND (5), FH (4). These sit in 43 competency definitions and render 93 times on 66 pages.
- **Common long words in task statements:** monitoring (93), documenting (90), conditions (89), decision (85), evidence (76), environmental (61), management (60), reporting (56), analysis (49), requirements (41), criteria (39), protocol (39), automated (39), verify (39), uncertainty (37).
- **AI-era vocabulary in tasks:** model (90), validat- (40), AI-generated (18), provenance (6).
- **Interface vocabulary,** totals across 764 pages (`r4/ui_vocab.txt`):

  | Term | Occurrences | Pages |
  |---|---|---|
  | "unreviewed" | 12,658 | 745 |
  | "Use tier" | 12,603 | 764 |
  | "AI-agent draft" (and variants) | 10,005 | 764 |
  | rule-version strings | 8,457 | 764 |
  | "editorial draft" | 3,346 | 417 |
  | "not for decisions" | 2,101 | 262 |
  | match-type terms such as "closeMatch" | 690 | 217 |
  | state-class codes such as "TXclass:" | 448 | 101 |
  | WP-nn codes | 351 | 278 |
  | REG-nn codes | 328 | 73 |

### 7.4 Alternative labels and plain job titles

- **Alternative labels:** roles 31 of 37 (84%; 84 labels); competencies 176 of 223 (79%; 508); job families 4 of 17; variants, tasks, indicators and knowledge statements none.
- **Plain job-title synonyms:** 31 of 37 roles have at least one. The 6 without are all P3 watch roles. Examples: "wildland firefighter", "burn boss", "range conservationist", "sanitarian", "GIS analyst", "district ranger".
- **Probe of 38 common US titles: 12 present, 26 absent [E].** The absent ones are range technician, forestry technician, hotshot, smokejumper, engine captain, game warden, conservation officer, environmental scientist, water quality technician or specialist, GIS technician, NEPA planner, wetland scientist, soil scientist, fisheries technician, wildlife technician, stormwater inspector, drone pilot, environmental compliance officer, EHS manager, crew leader, corpsmember, AmeriCorps, arborist, botanist and archaeologist. Some are out of scope, and that is still useful to say in search **[J]**.

### 7.5 Hierarchy depth and breadth

- **Modules:** core plus 11. Competencies: core 163, forest 16, waste 10, water 6, water quality 6, wildlife 6, hazards 4, parks 4, air 3, environmental health 3, extractives 1, working lands 1. Tasks: core 1,025; forest 72 is the largest module.
- **Competency kinds:** practice 196, transversal 18, knowledge area 9. Lifecycle: established 197, watch 26.
- **Job families:** 17, flat, computed (`views/job_families.json`). Members per family: 14, 10, 6, 4, 3, 3, then 2 or fewer. One family has no members. The median role belongs to 1 family, the maximum is 3. **None of this is used in the explorer.**
- **Work functions:** 12 primary values on roles (Assess 7, Authorize 5, Enforce 5, …). Tasks have 17 values, all gated agent drafts.
- **Roles:**
  - Tiers: P1 13, P2 17, P3 6, P4 1.
  - Variants per role: median 4 (range 2–6). By sector: state 35, federal 34, local 25, private 25, NGO 15, academic 6.
  - Authority positions: resource manager 42, regulator 31, advisor or researcher 27, service provider 23, regulated party 14, other 3.
  - Each role has a median of 28 tasks (22–35) and 15 competency targets (11–31).
- **Competencies:** a median of 3 described levels (9 have none) and 8 indicators (0–25). Common level spans are L1–L4 (103) and L2–L4 (66).
- **Coverage gap:** 656 of 1,317 tasks (50%) belong to no role bundle, even counting the 24 tasks added through variant `taskAdds`. They are reachable only through competency pages.

### 7.6 Most-connected records

- **Competencies in all 37 roles:** the 4 AI-and-data transversals.
  - "Interpret and question environmental data products in everyday work"
  - "Use AI tools responsibly in everyday environmental work"
  - "Validate AI-generated work products before professional use" (22 tasks, the most of any competency)
  - "Record provenance and AI involvement in work products"
- **Next most-targeted competencies:** risk communication under uncertainty (12 roles), supervising staff and volunteers (11), safety and stop-work authority (9), project delivery (8).
- **Low reuse:** 27 competencies are targeted by no role. The median competency is used by 2 roles and served by 6 tasks. Each task serves a median of 1 competency.
- **Tasks in the most roles:**
  - answering public questions about an uncertain risk (8 roles);
  - drafting a public advisory (7);
  - chain-of-custody records (7);
  - field duplicates and blanks (7);
  - the enforcement chain: inspect, collect evidence, investigate, assemble the case file (5 each).
- **[J]** These cross-role "spine" competencies are what transferability users (U1, U2, U8) need. The current IA never surfaces them.

### 7.7 Data-user hygiene

- In the bundle, `useTier` holds the *declared ceiling*, and it reads "develop" on 2,880 records.
- The effective tier (`views/effective_use_tier.json`) is lower: exploratory for 1,949 records and describe for 1,789. What binds it: the level rule 1,913 times, evidence 1,029, the declared ceiling 796.
- The CSVs separate the two columns correctly. The bundle should do the same, or carry a bold note, so that importers don't read "develop" as permission **[J]**.

---

## 8. Strengths the redesign must keep

These are **[E]** unless marked otherwise.

1. **Privacy by architecture.** The site has no cookies, storage, analytics, third-party requests or `fetch`. Its CSP sets `connect-src 'none'` and `form-action 'none'`. Search is embedded; the gap check is local and saves to a file; the team grid shows nothing for fewer than 5 files. A failing build check enforces all of it. New features (better search, comparisons, exports) must fit inside this envelope.
2. **The fail-closed display gate and the v1 drawer.** "0 rated values out of 8,256 slots" is stated honestly. Keep the mechanism; change only how it is presented.
3. **Claims-hygiene build checks.** "Unverified — not for citation"; withheld signals are counted; crosswalks are "navigation aids, not alignment claims"; pathways are "never a recommendation". Extend these checks to readability and ID leaks.
4. **HR guardrails in HR language.** "Not a classification basis…"; "% time: set by the supervisor"; "indicative" GS bands; credentials described as "may be involved … not a requirement". These suit U4 and U5 **[J]**.
5. **Baseline accessibility.** 0 axe violations; native disclosures and fieldsets; skip link; 4 px focus ring; every chart has a caption, a summary and a table; a pattern, not colour alone; reflow to 320 px; ratings work without JavaScript; an honest ACR.
6. **Content quality.** Tasks are concrete action-object-condition statements. Indicators are observable, with "so that" criteria. Roles carry "Also called" synonyms. The Factor 1 knowledge list helps U5. This is the asset to put first **[J]**.
7. **Transparent authorship and one call to action.** Pages say the records were "drafted by AI agents … not yet reviewed by independent human experts". Credit goes to the "EMST project lead", feedback goes to GitHub Issues, and the Tribal boundary is shown only as a count and a policy statement.
8. **Lean delivery.** 20.7 KB of JavaScript and 6–7 requests per page, with no server. A portable build works from disk, with SBOMs and checksums.
9. **Error prevention in the gap check.** Confirmation before clearing, a guard on leaving the page, focus moved to the results, and a polite live region.

---

## Appendix A: Numbers not given above [E]

- **Site:** 764 HTML pages and 835 files (43.6 MB raw). From the explorer's own report (`site/reports/check-output.json`): 803 external links, 932 figures, 2,098 v1 drawers.
- **"Assessment pending" per page:** role variants median 185 (max 239); competencies median 24 (max 88).
- **Main text per page:** median 1,644 words.
- **Crosswalk coverage:** 65 of 79 series and 18 of 38 classes have no role mapped at closeMatch or stronger.
- **Empty series pages (42):** 0021, 0023, 0090, 0101, 0110, 0170, 0190, 0193, 0201, 0301, 0343, 0403, 0413, 0414, 0430, 0434, 0435, 0437, 0440, 0459, 0471, 0480, 0485, 0487, 0499, 0601, 0688, 0690, 0698, 0802, 0893, 1170, 1306, 1320, 1341, 1350, 1360, 1372, 1373, 1380, 1712, 2151.
- **Search index:** 1,317 tasks, 163 core and 60 module competencies, 121 variants, 79 series, 38 classes, 31 roles, 6 emerging roles, 2 watch items.
- **Tab stops:** role variant 241; variant gap check 373; chosen-competencies page 2,658.

## Appendix B: Scripts and outputs

Everything is in `research working folder: r4/`. The site was served read-only with `python3 -m http.server 8765 --bind 127.0.0.1` from `site/_site` and stopped afterwards. Node scripts were run as `NODE_PATH=/opt/npm-tools/node_modules node <script>`.

| Script | What it does | Output |
|---|---|---|
| `crawl.py` | Static BFS crawl: page types, depth, headings, nav, sizes | `crawl.json`, `crawl_summary.txt` |
| `pagetext.py` | Extracts the visible text of `<main>` | stdout |
| `shots.js` | Screenshots of 22 page types at 1280 and 390 px, plus first-content metrics | `shots/`, `shots_metrics.json` |
| `search_test.js` | 50 queries typed into /search/ | `search_results.json`, `.txt` |
| `a11y.js` | axe-core (wcag2a through wcag22aa, plus best practice) with disclosures closed and open; landmarks, headings, tab stops, 320 px reflow | `a11y_results.json`, `.txt` |
| `keyboard.js` | Keyboard pass on role variant, gap check and search | `keyboard_results.json`, `shots/kbd-*.png` |
| `targets.js`, `linktext.py` | Small-target check; ambiguous link text | stdout |
| `forced.js`, `chartclip.js` | Forced colours, 200% zoom, chart legibility | `shots/forced-*`, `shots/role-change-chart-*`, `shots/zoom200-*` |
| `perf.js`, `perf_gzip.js`, `perf_cpu.js` | Network emulation uncompressed and gzip (in-process read-only server); 4× CPU throttle | `perf_results.txt`, `perf_gzip_results.txt`, `perf_cpu.txt` |
| `perf_sizes.py` | Raw and gzip sizes by page type and asset | `perf_sizes.txt` |
| `ui_vocab.py` | Status and jargon counts in built pages | `ui_vocab.txt` |
| `content_audit.py` | Data audit: lengths, readability, acronyms, alternative labels, hierarchy, connectivity, tiers | `content_audit.txt`, `.json` |

**Currency [J].** This report treats WCAG 2.2 (2023) as current and uses Chrome DevTools' 3G presets as of my knowledge cutoff. Either may have changed; I didn't check online.

**Sources (all local):**

- `site/README.md`, `site/ACR.md`, `site/reports/browser-checks.json`, `site/reports/check-output.json`
- `site/_site/**`, including `assets/js/gap-check.js` and `assets/js/search.js`
- `vocab/sector_actors.yaml`
- `docs/decisions/ADR-0010-ids-serialization-versioning.md`
- `dist/2.0.0-rc.1/emst.bundle.jsonld`, `csv/*`, `views/*`, `RELEASE_NOTES.md`
