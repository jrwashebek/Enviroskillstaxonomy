# EMST public interface prototype: design and build specification

This file is the contract between design and development.
- **Why:** `RESEARCH_SYNTHESIS.md`. Requirement IDs R-1 to R-17 are defined there.
- **Data shape:** `DATA.md`.
- **Visual components and their markup:** `DESIGN_SYSTEM.md`.
- **Words:** `CONTENT_GUIDE.md` and `app/assets/js/content.js`.

## 0. Architecture (fixed)

- **Single page with hash routes** in `app/index.html`. All views are generated in the browser from the data files in `app/data/`, which are generated from the explorer's view model and must never be hand-edited.
- **CSP:** `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'; frame-src 'none'`. Therefore:
  - no inline scripts, inline styles or `style=` attributes; use classes;
  - no `fetch`, XHR, storage, cookies, `pushState` or writes to `location`;
  - no third-party requests;
  - no `innerHTML`: build every node with `h()` from `lib/dom.js`.
- **Navigation happens only through `<a href="#/…">` links.** A script may update a link's `href` and call `.click()` on an anchor the user activated through a control. It must never assign to `location`.
- **No user-typed text in URLs.** Search queries stay in memory, so search results are not linkable. That is a deliberate privacy trade-off.
- **ES modules** are loaded statically from `assets/js/main.js`. No dynamic `import()`. Data loads with `lib/data.js` (`<script src>` injection).

### Module ownership

| File | Owner | Purpose |
|---|---|---|
| `lib/dom.js`, `lib/data.js`, `lib/router.js`, `lib/search.js`, `lib/format.js` | lead | done |
| `ui.js` | lead | shared components (§3) |
| `main.js` | lead | boot, header, search combobox, footer, routes |
| `content.js` | content designer | all cross-cutting copy (§4) |
| `export.js` | lead | copy-as-text, CSV, print helpers |
| `views/home.js`, `views/search.js`, `views/roles.js`, `views/competencies.js`, `views/about.js` | developer A | |
| `views/role.js` | developer B | the most important page |
| `views/competency.js`, `views/task.js`, `views/compare.js`, `views/changing.js`, `views/hr.js` | developer C | |

Each view module exports `async function render({params, section, path})` returning `{title, node}`. A view must never touch another view's file.

## 1. Routes

| Route | View | Title pattern |
|---|---|---|
| `#/` | home | "EMST · Environmental Management Skills Taxonomy" |
| `#/search` | search results (query in memory) | "Search results" |
| `#/roles` | roles index | "Roles" |
| `#/role/:slug` | role | role title |
| `#/role/:slug/:actor` | role, with that employer variant selected | role title (employer) |
| `#/competencies` | competencies index | "Competencies" |
| `#/competency/:slug` | competency | title |
| `#/task/:slug` | task | "Task: first 8 words…" |
| `#/compare`, `#/compare/:a`, `#/compare/:a/:b` | compare | "Compare roles" |
| `#/changing` | what's changing | "What's changing" |
| `#/series`, `#/series/:code` | federal series | "OPM series 0460 Forestry" |
| `#/classes`, `#/class/:slug` | state and local classes | class title |
| `#/about`, `#/about/:page` | about the data | page title |

**About pages:**
- `read` (How to read EMST: the key)
- `made` (How it was made)
- `status` (Release status)
- `data` (Data and downloads)
- `corrections` (Corrections and contributing)
- `held` (Held records)
- `accessibility`
- `privacy`

**Deep links:** `#/role/x@tasks` scrolls to and focuses the element with `id="tasks"`. Section ids are listed per page below.

## 2. Pages

The acceptance criteria (AC) for each page are binding.

### 2.1 Home `#/`

**Purpose:** get people to the right role quickly (R-1, R-8). Make the status honest in one line (R-4, R-13).

**Order:**
1. **H1:** plain-language purpose, for example "Shared words for environmental work".
2. **Lede:** what EMST is, in one or two sentences.
3. **The search field again, large,** with three example chips ("forestry technician", "Rx burn", "0460"). Clicking a chip runs that search.
4. **"What do you want to do?"** Five task links, verbs first, not audiences:
   - Look up what a role involves → `#/roles`
   - Compare two roles → `#/compare`
   - Find competencies and levels for a course or training plan → `#/competencies`
   - See what's changing → `#/changing`
   - Download or cite the data → `#/about/data`
5. **Browse by job family:** 17 cards showing title and role count. Job families come from `core.jobFamilies`. Each links to `#/roles` with that filter preselected; the filter state is passed in memory through a module-level variable, not the URL.
6. **Browse by employer type:** federal, state, local, NGO, private, academic, with variant counts.
7. **"What you can use EMST for":** three lines (OK for, not for, how it was made), plus a link to the key.
8. **Release facts:**
   - counts: 37 roles, 223 competencies and 1,317 tasks. Each figure needs its badges (`core.figs`); use the compact badge form;
   - release ID and date;
   - "Not a government website".

**AC:**
- The first meaningful action is above the fold at 390×844.
- No audience picker.
- No figure without its tier and evidence badge.

### 2.2 Header, status ribbon and footer (built by the lead in `main.js`)

**Header:**
- skip link;
- wordmark "EMST", linking home;
- search combobox (§3.3);
- navigation: Roles, Competencies, Compare, What's changing, About the data. Below 768px this collapses into a disclosure button labelled "Menu".

**Status ribbon,** directly under the header on every page and quiet in style:
- "Draft release 2.0.0-rc.1";
- "Drafted by AI agents, not yet reviewed by people";
- the link "What this means" → `#/about/read`.

**Footer:**
- "An independent open project. Not a government website.";
- `text.authorship` in plain words;
- licence (CC0 data, Apache-2.0 code);
- release ID and build commit (short);
- links: Accessibility, Privacy, Corrections, GitHub.

The footer is short. The old 387-word footer is gone; that text lives in About.

### 2.3 Search results `#/search`

**Results:**
- grouped by kind, in this order: roles, OPM series and state classes, competencies, tasks, then tools, credentials and signals;
- counts per group, with "Show all N";
- each result shows its title (matched words marked with `<mark>`), kind, and one line of context;
- each result says **why it matched**: "Also called: range conservationist", "OPM series code 0454", "Spelling: hydrologist", "Synonym: Rx burn → prescribed fire".

**Notes at the top:** spelling corrections and synonyms used (`notes` from `SearchIndex.search`).

**Zero results** (R-2):
- say plainly that EMST doesn't cover it yet, or offer to try other words;
- suggest three to five related searches (prefixes in the vocabulary, or the nearest roles by fuzzy match);
- offer browse links, and "Suggest a role or task we're missing", which opens the corrections page with the query shown, so the user can copy it.

**AC:**
- These queries put a relevant role or series in the top three results: "foresty", "GS-0460", "Rx burn", "range con", "hydrolgist", "permit writer", "hotshot", "GIS".
- "veteran" and "game warden" give an honest zero or near-zero answer with next steps.

### 2.4 Roles index `#/roles`

**Filters,** a chip group shown above results with live counts:
- job family;
- employer type;
- depth: "Full profile" (P1) / "Starter profile" (P2 and P4). P3 roles are not listed here; a link points to What's changing.

**Results:**
- grouped by job family by default; alternatively A–Z;
- a role card shows title, "Also called" (up to 2), function statement, employers as text chips, task and competency counts, and the status line in its compact form;
- the number of results is announced in a polite live region when filters change.

**AC:**
- Every filter is a native checkbox or radio button styled as a chip.
- Keyboard-only users can filter and reach results.
- A filter that leaves no roles gives a clear empty state with "Clear filters".

### 2.5 Role page `#/role/:slug` (developer B; the core page)

**Order and section ids:**
1. **Page header** (`id="overview"`):
   - breadcrumb: Roles › job family;
   - H1 role title;
   - "Also called …";
   - lede: the function statement;
   - `def` under "More about this role" (a disclosure) when it is longer than 280 characters;
   - meta row: employer chips, depth label, lifecycle chip if not established.
2. **Status line** (`ui.statusLine(record)`): use tier as "Use for / Not for", plus AI-drafted and review state, with links to "About this record" and the key.
3. **On this page:** a compact list of section links.
4. **The work** (`id="tasks"`):
   - **Filter by role level:** All, Entry, Journey, Senior, Lead, from `levels[]` and `tasks[].roleLevels`.
   - **Group by:** competency (default; group on each task's primary competency, in `targets` order) or flat list.
   - **Show the first 8 tasks, then "Show all N tasks".** Each task shows:
     - its statement, linking to the task page;
     - its competency link;
     - a "Formation task" tag where `formation`, with a tooltip-free inline explanation on first use: "learned through supervised practice".
   - **Tasks added by the selected employer variant** appear in this list with an "Added for state roles"-style tag.
   - **One pending summary at the end** (`ui.pendingSummary`), naming what isn't assessed: importance, time share, critical, needed-at-entry, craft blend, exposure to automation. It gives the count assessed ("0 of 29 tasks"), why, and what would change it. **No per-row "pending".**
5. **Competencies** (`id="competencies"`):
   - a table: competency (link) × role levels (Entry … Lead), with the target level as a named level chip (for example "L3 Proficient"; the names come from `labels.level`);
   - default rows are `isDefault`; "Show N more (modules and emerging)" reveals the rest;
   - `text.targetsNote` sits under the table;
   - **On mobile:** one card per competency, listing level by role level.
6. **With other employers** (`id="employers"`): a tab list of variants by actor (federal, state, local, NGO, private, academic, in that order). The `/:actor` route preselects a tab. Each panel shows:
   - the variant definition;
   - authority position;
   - sign-off (or the "pending" text);
   - credentials that may be involved (`text.credentialMayBeInvolved`, and the count still being verified);
   - linked policy instruments (with `text.unverified` where `unv`);
   - grade bands with `text.gradeNote`;
   - jurisdiction context;
   - tasks that differ from the role bundle;
   - class and translation crosswalk rows (`ui.crosswalkList`);
   - **`text.hrDisclaimer` when `hr` is set** (federal and state).
7. **Connections** (`id="connections"`):
   - OPM series (`hrSeries`), linking to `#/series/:code`, with the plain match type, "AI-suggested, not reviewed" and the realignment flag;
   - state and local classes (`hrClasses`), linking to `#/class/:slug`;
   - O\*NET-SOC and SOC rows from `crosswalks`: code, plain match type, and an external link to `https://www.onetonline.org/link/summary/<code>` for O\*NET-SOC codes, with no query string;
   - roles this one grows from (`feeders`, `entryFrom`) and grows into (`progressesTo`);
   - `text.crosswalkNote` sits under the lists.
8. **Where it can lead** (`id="paths"`, exploratory):
   - up to 6 destination roles from `paths.edges` whose `from` is one of this role's variants, with `shown: true`, de-duplicated by destination role;
   - each shows "shares N of M of the competencies that role needs" (from `statement`), "Compare" (→ `#/compare/this/that`) and frictions if present;
   - `paths.notice` at the top, styled as an exploratory notice.
9. **How it's changing** (`id="changing"`):
   - signals about this role (`signals[]`): title, family, source grade in words, "watch";
   - emerging competencies (`chg.emerging`);
   - **the honest summary:** "No change indicator has moved: all signals are on watch" (from `change.changeIndicators`);
   - a link to What's changing;
   - `text.noSignal` if there are none.
10. **About this record** (`id="about"`):
    - `ui.evidenceLadder`;
    - provenance in plain words: drafted by AI agents (`ev.by` as role names), date, method, evidence label explained, sources (IDs), review status;
    - record ID and release;
    - `ui.recordActions`: Copy citation, Suggest a correction, Print, Copy tasks as text, Download CSV.

**AC:**
- No more than about 15 tab stops before the first task.
- Total height at 390px is no more than 40% of the current explorer's role-variant page (about 11,000px) with default disclosures.
- No string matches `/effective-use-tier@|closeMatch|relatedMatch|agentDraft|raterType|OBS-4/` anywhere in visible text.
- Every pending value is summarized once per section.
- Print shows the role title, status line, tasks, competencies, release ID and the URL.

### 2.6 Competency page `#/competency/:slug` (developer C)

**Sections:**
1. **Header** (`overview`): breadcrumb (Competencies › module), H1, statement as lede, type label, module, "Also called".
2. **Status line.**
3. **Levels** (`levels`): `ui.levelLadder` for levels in `span`. Each level shows:
   - its name and the descriptor from `labels.levelDescriptors`;
   - its indicators, with a "distinguished by …" note (`attr`) where present;
   - `text.indicatorPlacement` under the ladder.

   Indicators are exploratory, so a small notice says they are not assessment criteria yet.
4. **Used in roles** (`roles`): each role with its target level by role level. **This fixes the explorer's one-way navigation.**
5. **Tasks** (`tasks`): the tasks this competency serves, primary first.
6. **Knowledge** (`knowledge`): knowledge statements (`ks`) with their lowest level.
7. **How employers differ** (`enactments`): enactments grouped by actor or authority position.
8. **Tools** (`tools`).
9. **Related elsewhere** (`crosswalks`): ESCO, OPM ECQ and DOL AI literacy, using plain match types. Non-matches (`not`) appear as "Checked: not a match". `text.crosswalkNote` sits beneath.
10. **About this record** (`about`), plus the v1 lineage codes in a disclosure titled "Earlier version (v1)".

### 2.7 Task page `#/task/:slug` (developer C)

- **H1:** "Task" as an eyebrow, with the statement as the heading.
- **Status line.**
- **Competencies it uses; roles it appears in** (with a formation tag).
- **Assessment status, summarized once:** work function, craft and exposure, from the gated texts.
- **"Matching O\*NET tasks"** from `x2`. "No O\*NET task found" rows read: "Two AI coders found no matching O\*NET task". Matched rows show the O\*NET task ID and plain match type.
- **Tools; credentials that may be involved.**
- **The v1 evidence drawer:** a closed disclosure labelled with `v1.lab`, plus `text.v1DrawerBody`. Values are listed as given and never counted.
- **About this record.**

### 2.8 Compare `#/compare[/:a[/:b]]` (developer C)

**Choosing roles:**
- two native `<select>`s, each listing P1, P2 and P4 roles grouped by job family;
- choosing updates the href of a "Compare" link (`#/compare/a/b`), which the user activates;
- a "Swap" link reverses the order.

**Results, in this order:**
1. A caveat notice (`paths.notice` plus "Sharing competencies doesn't mean you qualify. Employers set their own requirements.").
2. A one-sentence summary, for example "They share 7 of the 18 competencies the second role needs, and 3 tasks."
3. `ui.overlapBar`, with a text equivalent.
4. **Shared competencies**, with each role's highest target level and the level gap ("L2 → L3").
5. **Only in role A; only in role B.**
6. **Shared tasks.**
7. **What to check**, from role B's variants:
   - credentials that may be involved;
   - OPM series and state classes linked;
   - friction fields from `paths.translations` where present.
8. **If a computed pathway edge exists** between their variants: its statement and its gap list (exploratory).

**AC:**
- No percentage and no single score.
- Works with the keyboard alone.
- Readable at 320px (the columns stack).

### 2.9 What's changing `#/changing` (developer C)

**Order:**
1. Intro (`change.notice`), plus a "How to read this" disclosure covering source grades, watch state and signposts.
2. **Summary line:** N signals, all on watch; "No change indicator has moved".
3. **Signals:** filterable by family. Each card shows:
   - title and family;
   - the measure, with `few` handled through `text.tooFew`;
   - the period;
   - the source grade, in words and letter;
   - what it is about, linked;
   - review-by date.
4. **Emerging roles (P3):** cards with function, horizon, review-by and counter-signal ("What would show this isn't happening").
5. **Emerging competencies.**
6. **Policy instruments:**
   - title, status as of the release, and next review;
   - `unv` instruments show only the title plus `text.unverified`;
   - events with `sup` show the type without a date.
7. **Scenarios:** axes, the four scenarios as cards, the no-regret moves.

### 2.10 Federal series and state classes (developer C, `views/hr.js`)

**Series and classes index:** a sortable table. Series columns are code, title, status (realignment flag), roles linked (close) and generated profile (yes or no).

**Series page:**
- `hr.disclaimer` first, in a notice;
- status;
- the realignment notice (`text.realignment`);
- quality standard (with its verify flag);
- the positive education requirement, as an agent judgment;
- roles linked: close matches shown, candidates in a disclosure;
- core competencies;
- if a generated profile exists: duties by grade band (**no percentages**, with `hr.pctTimeNote`) and factor 1 knowledge.

**Class page:**
- disclaimer;
- jurisdiction, agency, level, supervisory;
- "Official specification" external link with its retrieved date;
- minimum qualifications (paraphrase, labelled as such), degree rule, licences;
- pay, with its effective date;
- the State Class View mappings, if present.

### 2.11 About pages (developer A, copy from the content designer)

**`read` (How to read EMST)** is the public key. Every label used anywhere is listed with its meaning and an example:
- the use tiers as "You can / You can't", with three concrete examples each. Describe and exploratory are reached; develop and select are not reached in this release, and the page says what would unlock them;
- AI-drafted;
- review status;
- evidence labels E, J and S;
- assessment pending;
- lifecycle;
- crosswalk match types;
- source grades;
- formation task;
- the held-records notice.

**Each status chip in the UI links here,** to the anchor for that label.

**The other pages:**
- `made`: the evidence ladder for the whole release; who drafted it (AI agents under a charter set by the project lead); what has not happened yet (practitioner review, reliability studies); the plan.
- `status`: the release gate items from `core.status.gate`, with plain-language explanations.
- `data`: downloads (links to the repository's `dist/` files on GitHub), licence, how to cite, IDs (candidate until 2.0.0), "caveats travel with the data".
- `corrections`: how to report; "Copy reference" for a record; the GitHub Issues link; what happens next; the non-GitHub route, if the project lead approves one (show the gap honestly for now).
- `held`: `core.status.held.policy` and the count. **Nothing else.**
- `accessibility`: the target standard and the known limits of the prototype.
- `privacy`: what the site does not collect.

## 3. Shared components (`ui.js`, built by the lead)

All components take data objects in the shapes `DATA.md` describes and return DOM nodes.

| Function | Use |
|---|---|
| `pageHeader({crumbs, eyebrow, title, alt, lede, meta})` | Every page |
| `statusLine(rec, {compact})` | Every record (R-4) |
| `pendingSummary({what[], assessed, total, why, next})` | Once per section with gated values (R-5) |
| `evidenceLadder(rec)` | "About this record" |
| `provenance(rec, core)` | "About this record" |
| `recordActions({id, title, kind, url, exports})` | "About this record" |
| `matchType(row, noun)` | Crosswalk rows in plain words |
| `crosswalkList(rows, {noun, linkFn})` | Crosswalk rows in plain words |
| `levelChip(code)`, `levelLadder(levels, {span, target})` | Proficiency levels |
| `badge(kind, value)` | Tier, evidence, lifecycle, AI, match |
| `figBadges(fig)` | Figures |
| `notice(kind, title, body)` | info, exploratory, hr, held, caution |
| `disclosure(summary, body, {open})` | Native `<details>` |
| `tabs(list, {selected, label})` | Variant switcher (ARIA tabs, arrow keys) |
| `chips(name, options, {multi, onChange})` | Filters |
| `onThisPage(sections)` | Section navigation |
| `card(...)`, `emptyState(...)`, `liveCount(...)` | General |
| `jargon(text)` | Wraps known acronyms in `<abbr title>` on first use per page, from `content.js` GLOSSARY (R-9) |

### 3.3 Search combobox (`main.js`)

Built on the ARIA 1.2 combobox pattern with a listbox popup:
- suggestions appear after 2 characters, at most 8, grouped by kind, with a "See all results" option last;
- arrow keys move through options; Enter activates the option, or "See all results" when none is selected; Escape closes;
- a polite status message says "N suggestions";
- the query is held in memory for the results view.

## 4. Copy (`content.js`, content designer)

The content designer exports `COPY` and `GLOSSARY`.

**`COPY` keys:**
- `site`: name, tagline, ribbon, notGov, footer lines;
- `use`: per tier, `{label, short, youCan[], youCant[], why}`;
- `ai`: the status line text variants;
- `review`: per review status;
- `evidence`: E, J and S as `{label, plain}`;
- `lifecycle`;
- `pending`: section templates;
- `match`: predicate × noun in plain words, plus not and none;
- `sourceGrade`;
- `formation`;
- `levels`: plain names and short descriptions, if `labels.levelDescriptors` is too technical;
- `zero`: zero-results copy;
- `compare`: caveat and summary templates;
- `actions`: copy citation, correction steps, export headers;
- `about`: full text for each about page, as structured blocks;
- `held`: must quote `core.status.held.policy` verbatim and add nothing beyond a short heading.

**`GLOSSARY`:** term → expansion and a plain definition, for 60–100 field and HR terms and acronyms (NEPA, BMP, UAS, WUI, ICS, PD, FES, KSA, IDP …).

**Rules:**
- US spelling in new UI copy.
- Grade 8 reading level or lower for UI copy.
- Sentence case.
- No internal codes.
- Respect `do_not_say` and the claims rules. Never claim alignment, validation or accreditation.

## 5. Quality gates (QA will check)

1. **Privacy and security.** No network, storage, cookie, `pushState` or `innerHTML` use. No inline style or script. No external fetch: the only external URLs are `<a href>` navigations with no query string.
2. **Accessibility.**
   - axe-core WCAG 2.2 A/AA: 0 violations on every route.
   - Keyboard pass on the home, role, competency and compare pages.
   - Reflow at 320px.
   - Focus moves to the H1 on every route change, and the change is announced.
   - `forced-colors` usable.
   - Every chart or bar has a text equivalent.
3. **Content.** No internal jargon (see the role AC regex). Every figure has its badges. The HR disclaimer appears wherever `hr` is set. The paths notice appears on every pathway view. The held-records page shows only the policy text and the count.
4. **Performance.** App shell (HTML, CSS, JS and fonts) at most 200 KB gzipped. The first role view needs only `core.js` plus one role file.
5. **Truthfulness.** Every number on screen comes from `app/data/`. Nothing is hand-typed.
