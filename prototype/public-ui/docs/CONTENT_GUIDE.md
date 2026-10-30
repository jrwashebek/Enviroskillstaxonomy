# EMST public interface: content guide

**Owner:** content designer (an AI agent on the HCD team). **Date:** 30 October 2026. **Release:** `2.0.0-rc.1`.
**Copy lives in:** `app/assets/js/content.js`. **Stimuli for testing the key wording:** `docs/COMPREHENSION_TESTS.md`.
**Status:** no real person has read this copy yet. Every wording choice below is a hypothesis until the comprehension tests run (`RESEARCH_SYNTHESIS.md` §8).

**Evidence labels:** [E] I read the source (path given); [J] my judgment, with its basis; [S] speculation, with what would settle it.

---

## 1. Using `content.js`

| Export | What it is |
|---|---|
| `COPY` | All cross-cutting copy, in the shape the lead set in the brief. |
| `GLOSSARY` | 100 terms that appear in `app/data/`: `{ term: { exp, def } }`. |
| `fill(template, vars)` | Replaces `{name}` tokens. A token with no value is left in place, so QA sees it. |
| `fillBlocks(blocks, vars)` | *Extra.* Fills every string in an array of about-page blocks. |
| `aboutVars(core)` | *Extra.* Builds the about-page tokens from core data: `release`, `releaseDate`, `year`, `heldN`, `gateAsOf`, `gate1`…`gate8` and `gateFailed`. |

**Keys added beyond the brief's shape** (all optional for consumers): `site.full`, `site.lede`, `match.mirrorRole`, `match.disagree`, `ladder.state`, `actions.noAccount`, `errors`, `empty`. The reasons are in §5 and §8.

**Rules for consumers:**
- **Links inside about blocks** are written `[link text](href)`. Every href is a `#/` route or an `https` URL with no query string. **The about view must render these as `<a>` elements.** [J: the block types in the brief have no link type, and a bare URL is poor link text.]
- **Numbers are never typed into copy.** Every count arrives through a token, filled from `app/data/`. The only digits in the copy are dates of cited documents, the release-gate item numbers, the example series code "0460", the example record ID and "320 pixels".
- **"rc.1 fact" comments** mark sentences that are true of release 2.0.0-rc.1 only. For example: "every record is 'Not yet reviewed by people'", or "No record reaches the training or job analysis uses yet". Re-check them for every release, or derive them from data.
- **The held-records policy is quoted verbatim** from `core.status.held.policy`, in `about.held` and in the `held` section of `about.read`. The check in §6 compares it with the data on every run. Never paraphrase it.
- **Glossary matching** for the lead's `jargon()`:
  - all-capital keys match case-sensitively;
  - keys with lower-case letters match case-insensitively;
  - allow a plural "s" (IDPs, ECQs);
  - prefer the longest key (O\*NET-SOC before O\*NET or SOC);
  - when `exp` is empty, the term is not an abbreviation: link or show the definition, but do not wrap it in `<abbr>`.

---

## 2. Voice and tone

**We sound like** a careful field colleague who tells you plainly what the page is, what it is good for and what nobody has checked yet. [J: R3 §3, §4; RESEARCH_SYNTHESIS I4, I5]

| Do | Don't |
|---|---|
| Lead with the work, then state the status once, in one line. | Stack warnings, or repeat a caveat in every row. |
| Say what AI agents did **and** what people have not yet done. | Write "AI-generated" with no explanation, or "may contain errors". |
| Give concrete "You can / You can't" examples for every use. | Use verbal labels alone ("describe tier", "exploratory"). |
| Say "not yet" and name what would change it. | Promise dates, or say "coming soon". |
| Stay neutral about held records. Quote the policy and nothing more. | Apologize, celebrate, protect or explain on anyone's behalf. |
| Name the human role exactly: "the EMST project lead". | Use "we reviewed", "experts", "our team of specialists". |
| Put the strongest limit, decisions about people, where HR work happens. | Hide the limits in a footer. |

**Mechanics.**
- Plain US English and sentence case. Verbs come first in actions and steps.
- Sentences of 20 words or fewer, and one idea per sentence.
- Use straight apostrophes (don't) and curly quotation marks (“Assessment pending”).
- Use "AI agents", never a model or system acronym.
- Never claim alignment, validation, approval or official status.

---

## 3. Reading level

### Targets
- UI copy at **US grade 8 or lower**, aiming for grades 6–8 [E: R3 PL-01; DESIGN_SPEC §4].
- No UI string of 10 or more words above grade 10.
- Glossary definitions are reported separately. Readability formulas penalize necessary technical names such as "Natural Resources Conservation Service", and R3 lists "grade-level targets applied to technical definitions" as a pitfall [E: R3 §2]. For definitions, the formula is an alarm only.

### Method
- **Tool:** textstat 0.7.3 (Python), run over every string in `COPY` and every `GLOSSARY` definition.
- **Excluded:** the verbatim policy quote, because it is data text.
- **Preparing the text:**
  - tokens are filled with realistic values, for example two role titles for `compare.summary`;
  - links `[text](url)` are reduced to their text, and bare URLs become "the link";
  - "O\*NET" becomes "ONET";
  - a full stop is added to any label without end punctuation, so that each label counts as one sentence.

### Measured scores (30 October 2026)

| Text | FK grade | Flesch Reading Ease | Gunning Fog | Coleman–Liau | Words |
|---|---:|---:|---:|---:|---:|
| All UI copy, joined | 3.3 | 87.7 | 4.4 | 6.5 | 5,020 |
| **UI prose only (strings of 10+ words, joined)** | **3.8** | **86.4** | **4.9** | **6.3** | 3,900 (10.3 words per sentence) |
| About › How to read EMST | 3.6 | 86.9 | 5.3 | 6.2 | 1,765 |
| About › How it was made | 4.7 | 78.7 | 5.9 | 7.7 | 366 |
| About › Release status | 3.0 | 88.4 | 4.2 | 6.5 | 257 |
| About › Data and downloads | 2.9 | 88.6 | 4.9 | 6.3 | 292 |
| About › Corrections | 2.3 | 95.6 | 4.9 | 5.6 | 269 |
| About › Accessibility | 4.2 | 80.0 | 5.1 | 6.6 | 183 |
| About › Privacy | 3.6 | 86.9 | 5.0 | 6.2 | 117 |
| Use tiers (`use`) | 3.5 | 87.0 | 5.2 | 6.5 | 560 |
| AI line and detail (`ai`) | 3.6 | 86.8 | 5.8 | 6.9 | 89 |
| Pending (`pending`) | 3.7 | 81.3 | 6.6 | 6.0 | 84 |
| Matches (`match`) | 4.0 | 80.5 | 5.2 | 6.1 | 94 |
| Compare (`compare`) | 5.0 | 72.4 | 5.7 | 9.6 | 74 |
| Glossary definitions, joined | 7.8 | 65.2 | 8.1 | 10.1 | 1,447 |

**Per string (UI strings of 10 or more words, n = 202):**
- median grade 4.3, 90th percentile 6.4, maximum 9.9;
- 6 strings are above grade 8, and none is above grade 10.
- The six are:
  - "assistive technology" (9.9);
  - the governance link text (9.6);
  - `compare.summary` filled with two long role titles (8.8);
  - the AI agent role names (8.7);
  - `compare.caveat` (8.2);
  - "EMST stands for Environmental Management Skills Taxonomy…" (8.2).
- Each is held up by a necessary name or term.

**Glossary definitions (n = 100):** median grade 8.0, 90th percentile 10.7, maximum 17.0 (REHS, because of the credential's own name). 45 are above grade 8. Almost all of those are agency, law or credential names that cannot be shortened.

**Caveat [J]:**
- Formulas reward short sentences and short words. They do not measure whether people understand the words.
- The aggregate figures are flattered by short labels, which is why the prose-only row and the per-string figures are given.
- Only the comprehension tests can show whether this copy works.
- The record text itself is still written at grades 14 to 20 [E: R4 §7.2], and content.js does not change it.

---

## 4. Word list

### Use / avoid

| Use | Avoid | Why |
|---|---|---|
| Drafted by AI agents | AI-generated, AI-powered, smart, automated content, written by Claude (in UI lines) | Say what AI did. "AI agents" is the agreed term [E: brief]. |
| Not yet reviewed by people | unreviewed, unverified, unvalidated | Says who has not acted, and that it can still happen [E: R3 AI-02]. |
| the EMST project lead | personal names, "our experts", "the team" | No personal names [E: brief §7]. Do not overclaim human involvement [E: R3 §4 pitfalls]. |
| practitioners, people who do this work | SMEs (in general UI) | Plainer. Keep "subject-matter expert" on HR pages, where it is OPM's term [E: R3 PL-09]. |
| Describe and plan · Explore only · Train and develop · Job analysis input | describe tier, effective-use-tier, use class, selection-grade | Task words, not codes [E: R3 PL-08; DESIGN_SPEC §2.5 AC]. |
| You can / You can't | permitted / prohibited uses | Concrete anchors stop verbal labels drifting [E: R2 §11.4; R3 §3]. |
| Assessment pending; "0 of 29 tasks assessed" (from data) | N/A, —, 0, blank, TBD, coming soon | Pending must never read as zero [E: R3 U-04]. |
| Close fit, not the same · Broader series · More specific term · Related in part | closeMatch, relatedMatch, skos:, SSSOM, confidence 0.6 | No internal predicates, and no decimals on screen [E: R3 CT-4; brief]. |
| Not a match (noted by an AI agent) | Checked: not a match | "Checked" implies a person checked it [J]. |
| AI-suggested, not reviewed | candidate, llm-reviewed-candidate | Plain words [J]. |
| Held records; held until a council approves (policy text only) | locked, restricted, redacted, censored, coming soon, protected | [E: R3 IG-03] |
| An independent open project. Not a government website. | official, government-grade, federal look | [E: R3 DS-02; USWDS banner rule] |
| job or position description | PD (unexpanded) | PD is in the glossary; spell it out in UI copy. |
| reduction in force | RIF (unexpanded) | Same reason. |
| sharing competencies doesn't mean you qualify | you qualify, eligible, match score, % match | Never imply eligibility [E: R2 §8; RESEARCH_SYNTHESIS I3]. |
| possible destination; where it can lead | recommended path, recommended move | Pathways are never recommendations [E: core.text.pathwaysNotice]. |
| a reliability study; how well raters agree | Krippendorff's alpha, α gate, display gate | [E: R4 §3.8 walkthrough] |

**Never in UI text** (the check in §6 enforces these):
- effective-use-tier, closeMatch, relatedMatch, agentDraft, raterType, OBS-4, SSSOM, LLM;
- validated, accredited, approved, official, verified, expert-reviewed, AI-powered, smart;
- any form of "align";
- "recommend";
- UGESP;
- Local Contexts Label or Notice names;
- Tribal-hold trigger terms outside the verbatim policy.

### US spelling

New copy uses US spelling [E: DESIGN_SPEC §4]. The data uses British spelling in places ("programme" appears 957 times [E: R2 summary]). Do not "fix" data text in views: it is generated. Search already normalizes both spellings.

| US (use) | British (avoid in copy) |
|---|---|
| program | programme |
| behavior | behaviour |
| organization, organize | organisation, organise |
| analyze | analyse |
| license (noun and verb) | licence |
| color | colour |
| center | centre |
| judgment | judgement |
| modeling | modelling |
| catalog | catalogue |

**Exception:** the key `site.footer.licence` keeps the spelling in the brief's shape. Its text says "license".

---

## 5. Patterns

### Status line (one per record)
- **Form:** `use[tier].short` + ` · ` + `ai.line`, with a link to `#/about/read#use-…` and a link to the "About this record" section.
  - **Example:** "Use for describing work and planning. Not for decisions about people. · Drafted by AI agents. Not yet reviewed by people."
  - **Compact form,** for cards: `use[tier].label` + " · " + `ribbon.ai`, for example "Describe and plan · Drafted by AI agents, not yet reviewed by people".
- **When the record has `ev.v1`:** use `ai.v1` instead of `ai.line`.
- **When the date matters** (About this record): use `ai.lineDated` with `ev.d` formatted as a long date.
- **Layers:**
  - one line on the record;
  - `ai.detail` in "About this record";
  - the full story in `about.made`.
  - Do not repeat the line inside sections. [E: R3 U-01, U-02]
- **HR pages:** show `core.text.hrDisclaimer` verbatim, where the data sets `hr`. Do not rewrite it.

### Pending (once per section, never per row)
1. **Title:** `pending.title`
2. **Body:** `fill(pending.body, {assessed, total, unit})`, followed by the `pending.what` items that apply to that section, as a list or joined with commas.
3. **Then** `pending.why` and `pending.next`.
- **Sort pending rows last,** in both directions, and keep them out of counts and charts.
- **Example:** "Assessment pending. 0 of 29 tasks assessed so far. Not shown yet: importance, share of work time, whether it is critical, whether it is needed on day one."

### Matches (crosswalk rows)
- **Label:** `match[pred]`, with `{noun}` set to "series", "class", "term" or "O\*NET task".
- **Suffixes**, separated by " · ":
  - always `match.unreviewed`;
  - for O\*NET task rows, `match.twoCoders` when `st` is `two-llm-coders-agreed-target`, and `match.disagree` when it is `needs-adjudication`.
- **Special rows:**
  - `not` rows use `match.not`;
  - `none` rows use `match.none`;
  - `emst:mirrorRole` uses `match.mirrorRole`.
- **Under every list:** `match.note`. It replaces `core.text.crosswalkNote` in plain words, with the same meaning.
- **Never show `conf`.**
- **Examples:**
  - "Broader series · AI-suggested, not reviewed"
  - "No matching O\*NET task found · AI-suggested, not reviewed · AI coders disagreed; a person needs to decide"
- **[E] Why `disagree` exists:**
  - 114 O\*NET task rows have no match;
  - 45 of them have `st` "two-llm-coders-agreed-target";
  - 69 have "needs-adjudication".
  - So "Two AI coders found no matching O\*NET task" (DESIGN_SPEC §2.7) is true for only 45 of them.

### Use tiers in context
- **On HR pages** (series, classes, federal and state variants), show the "You can't" list near the top, not only the short line [J: R2 T1, T4].
- **Develop and select:**
  - always show `notReached` with them;
  - never present them as "coming soon";
  - never give dates.

### Zero results and empty states
- **Zero search results:**
  - Title: `fill(zero.title, {q})`. The query appears only in the page, never in the URL.
  - Then `zero.body`, related searches under `zero.tryTitle`, browse links under `zero.browseTitle`, and a link labeled `zero.suggest` to `#/about/corrections`.
- **Filters with no results:** `empty.filters` (title, body, action).
- **Rule:** an empty state is never hatched like "pending". Empty means "nothing matches"; pending means "not yet assessed" [E: gallery "Empty and loading"].

### Errors
- **Pattern:** say what happened, then what to do, in two short sentences. Never blame the user.
- **Strings:** `errors.notFound`, `errors.load`, `errors.copy` and `errors.noScript`.
- **No error message asks for personal data or an email.**

### Compare
1. `compare.caveat` and `core.text.pathwaysNotice` at the top.
2. Then the one-sentence `compare.summary`.
- **Never** a percentage, a score or "you qualify".
- **Section headings:** `compare.onlyA`, `compare.onlyB`, `compare.shared` and `compare.check`. Use `compare.noEdge` when no computed edge exists.

### Exports (copy, print, CSV)
- **Header:** `fill(actions.exportHeader, {title, release, date, url})`.
  - `{date}` is the date the user copied, printed or saved the file, not the release date [E: R3 LB-04 asks for the print date].
- **Footer:** `actions.exportFooter`.
- **CSV:** put the header lines in a leading comment block, or in a separate "About" sheet if a spreadsheet would break.
- **The lead's `export.js`** already has its own `exportFrame()`. Align it with these strings, or call `fill()` on them. Today the two differ in wording, though not in meaning.

### Corrections
- **Steps:** `actions.correctSteps`.
- Always pair them with the honest account-and-public notice, and with `actions.noAccount`.
- **Never** promise a reply time. The contributing guide is a draft [E: docs/governance/CONTRIBUTING.md].

---
## 6. Claims-hygiene check

### What is checked

The check scans every text value in `COPY`, plus every `GLOSSARY` key, expansion and definition: **748 strings**. Structural fields (`key`, `id`, `t` and `kind`) are code and are skipped. It uses the explorer's own rule sources, so the copy meets the same rules as the data.

| Source | Rules | Result |
|---|---|---|
| ADR-0027 §3 retired claims: "validated against OPM and O\*NET classification systems", "SAF-accredited competency standards", "38% Human-Essential", "68% in transition", stale v1 counts (215, 222, 292 competencies), "9 S calls", "FC/DC structural property". Also the explorer's related rules: recommended pathways, UGESP compliance, SB 24-205, realigned or consolidated series, the banned domain, the PNNL hours figure, validation claims, alignment claims, selection-grade claims and retired ECQ names. [E: `docs/decisions/ADR-0027-…md` §3; regexes copied from `prototype/public-ui/tools/verify-data.mjs`] | 15 regexes, with the same negation handling | **0 hits** |
| Claims register `do_not_say` [E: `docs/methods/claims_register.csv`, 124 rows, parsed by `site/lib/claims.mjs`] | 56 strict phrases matched anywhere; 14 short phrases matched near two anchor words from their claim (stricter than the explorer, which skips them); 2 conflation rules | **0 hits** |
| Curated wrong forms [E: `site/claims/do_not_publish.yaml`] | 29 patterns | **0 hits** |
| Tribal-hold trigger terms [E: `schema/lint/governed_content.yaml`] | 17 triggers, allowed only inside the verbatim policy | **0 hits** |
| Prototype content rules [E: brief; DESIGN_SPEC §2.5 AC; R3 AI-04, IG-03, IG-04; claims register FED-05] | B1 internal words · B2 never-say words · B3 any form of "align" · B4 Local Contexts names · B5 held-record wording (refused, coming soon, locked, redacted, censored, restricted, insiders) · B6 eligibility ("you qualify" unless negated) · B7 "recommend" · B8 e-mail · B9 phone · B10 query strings in links · B11 UGESP, or the OPM memo attributed to OMB | **0 hits** |
| Held policy | `about.held[0]` must equal `core.status.held.policy` | **verbatim: true** |

**The register's strict phrases**, so a reader can see what was looked for:
'NEPA regulations'; 'NEPA reform law'; '1-5 hours saved per EIS subsection'; 'notice of intent to sue'; 'announced 2026-09-04'; '>220,000 comments'; 'Bay Area AQMD v. EPA filed 2026-04-16'; 'proposed rule published'; 'assurance not required for 2026'; 'still not published as of July 2026'; 'Colorado AI Act in force'; 'UGESP compliance'; 'NRM fully implemented by FY2028'; 'consolidated'; 'departing staff median 30.3 years'; 'senior reviewers are leaving'; 'the conservation labour market fell 29%'; '$400M standing cut'; 'the terminations persisted elsewhere'; 'reinstated only in plaintiff states'; 'USFS fire merged into USWFS'; 'NWCG and USWFS'; 'NWCG is not a party'; 'BLS says X% of jobs will be automated'; '77% of jobs/tasks are automated'; '77% directive'; 'robots can do 74% of jobs'; 'Global Green Skills Report 2025'; 'nine environmental bureaus'; 'monitoring requirements'; 'durable demand'; 'coordination tripled'; 'state boards approve programmes'; '27 languages'; 'AI RMF 1.1 released'; 'effective Jul 4 2026'; 'NJ Supreme Court review is possible'; 'OPM confirms active'; 'skills-based hiring does not work'; '1 in 700 firms'; 'no change at all'; 'Colorado's reform failed'; '1,350 laid-off federal workers'; 'Pennsylvania counts federal experience as equivalent in its minimum qualifications'; 'among the most/least exposed occupations in the economy'; 'splits environmental work in two'; 'environmental workers use AI less'; 'drafting and summarizing assistants at 10,000+ users in USDA'; 'CRS counts 540 Good Neighbor agreements'; 'field staff who also fly'; 'absorbed into field roles'; 'headcount or budget'; 'time savings show no effect'; 'includes no environmental occupations'; 'no coalition exists'; 'most registered AI is classical machine learning'.

**Short phrases** (14 entries, 12 distinct phrases; each checked near its claim's anchor words): '516 DM 1', '5-3', 'enacted', 'v1.2.0', 'final', 'APHA v. EPA', '16-5', '~Nov 10?', 'maintain', 'realigned', 'MIT', '13%'.
**Conflations:** OMB-02 (deployed with deployed+piloted); RPT-05 (16% with "more than a quarter").

### Result (run on 30 October 2026)

```
Strings scanned: 748 (COPY text values, GLOSSARY keys, expansions and definitions; structural fields key, id, t and kind are code and are skipped).
Rules: 15 retired-claim regexes (ADR-0027 §3); 56 strict and 14 short register wrong forms, 2 conflation rules (claims_register.csv do_not_say); 29 do_not_publish patterns; 17 Tribal-hold triggers; 11 prototype content rules.
Held policy quoted verbatim: true. Deferred (double-quoted, not enforced by the explorer) register phrases also checked: 0.
PASS: 0 hits
```

**Proof that the check works:** a copy of `content.js` with 10 seeded violations failed with 19 hits. Every seeded violation was caught, several of them by more than one rule:
- "validated against OPM and O\*NET" (C01, C12, B2);
- "aligned with O\*NET" (C13, B3);
- "LLM" and "closeMatch" (B1);
- "Tribes refused … locked" (Tribal trigger, B5);
- "You qualify" (B6);
- an e-mail address (B8);
- "recommended pathway" (C06, B7);
- "SPEED Act was enacted" (NEPA-05);
- "realigned" (C09, FED-04);
- "official" (B2).

**What the check cannot see** [J]:
- whether a sentence implies something it does not say;
- tone;
- personal names, beyond the e-mail and phone patterns. I wrote none, and credit always reads "EMST project lead".

A human edit is still needed.

### The script

Save it, for example, as `prototype/public-ui/tools/check-content.mjs`. Run it with `EMST_ROOT=<repo root> node check-content.mjs`. It exits with status 1 on any hit.

```js
// Claims-hygiene check for app/assets/js/content.js. Usage: EMST_ROOT=<repo root> node check-content.mjs [path/to/content.js]
// Reuses the explorer's own rule sources so the copy is held to the same rules as the data:
//   site/lib/claims.mjs + docs/methods/claims_register.csv (do_not_say), site/claims/do_not_publish.yaml,
//   schema/lint/governed_content.yaml (Tribal-hold triggers), and the ADR-0027 §3 retired-claim regexes
//   copied from prototype/public-ui/tools/verify-data.mjs. Adds the prototype's own content rules.
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
const ROOT = (process.env.EMST_ROOT || "/home/claude/emst").replace(/\/?$/, "/");   // repository root
const require = createRequire(ROOT + "site/package.json");
const yaml = require("js-yaml");
const { parseRegister, parseCsv, phraseRx, sentencesOf, conflates } = await import(ROOT + "site/lib/claims.mjs");
const { COPY, GLOSSARY } = await import(process.argv[2] || ROOT + "prototype/public-ui/app/assets/js/content.js");
globalThis.window = {};
(await import("node:vm")).runInThisContext(readFileSync(ROOT + "prototype/public-ui/app/data/core.js", "utf8"));
const POLICY = window.EMSTDATA.core.status.held.policy;

// Strings to scan: every string value in COPY (keys are code, not text), plus every GLOSSARY key, exp and def.
const items = [];
const walk = (o, path) => { if (typeof o === "string") items.push({ path, text: o });
  else if (Array.isArray(o)) o.forEach((x, i) => walk(x, `${path}[${i}]`));
  else if (o && typeof o === "object") for (const [k, v] of Object.entries(o)) { if (STRUCT.has(k)) continue; walk(v, `${path}.${k}`); } };
const STRUCT = new Set(["key", "id", "t", "kind"]);   // structural fields: code identifiers, never shown as text
walk(COPY, "COPY");
for (const [k, g] of Object.entries(GLOSSARY)) { items.push({ path: `GLOSSARY key`, text: k }); walk(g, `GLOSSARY.${k}`); }

const NEG = /\b(never|not|no|nor|nothing|none|without|until|unless|before|isn't|aren't|cannot|neither|doesn't|don't)\b/i;
const negated = (text, idx, win = 80) => { let b = text.slice(Math.max(0, idx - win), idx);
  const cut = Math.max(b.lastIndexOf(". "), b.lastIndexOf("; "), b.lastIndexOf(": "), b.lastIndexOf("\n")); if (cut >= 0) b = b.slice(cut + 1); return NEG.test(b); };

// 1. ADR-0027 §3 retired claims (same regexes as verify-data.mjs / site/tools/check-output.mjs).
const RETIRED = [
  { id: "C01", rx: /validated against (?:the )?(?:OPM|O\*NET)/gi },
  { id: "C02", rx: /SAF[- ]accredited/gi },
  { id: "C03", rx: /\b38\s?%[^.]{0,60}human[- ]essential|\bhuman[- ]essential[^.]{0,40}\b38\s?%|\b68\s?%[^.]{0,40}transition|\b77\s?%[^.]{0,80}(?:automat|API)|\b21\s?%[^.]{0,30}of tasks/gi },
  { id: "C04", rx: /\b(?:215|222|292)\s+competencies\b/gi },
  { id: "C05", rx: /\b9 S calls\b|structural property/gi },
  { id: "C06", rx: /\brecommended (?:pathways?|routes?|moves?|destinations?|careers?|next steps?)\b|\b(?:pathways?|routes?|moves?|destinations?) (?:is|are|was|were) recommended\b/gi, neg: true },
  { id: "C07", rx: /UGESP[- ]complian(?:t|ce)/gi },
  { id: "C08", rx: /SB\s?24-205/gi },
  { id: "C09", rx: /\brealigned\b|\bconsolidated into\b/gi, neg: true },
  { id: "C10", rx: /usindigenousdata/gi },
  { id: "C11", rx: /1\s?[–-]\s?5 hours/gi },
  { id: "C12", rx: /\bvalidated (?:competenc\w*|taxonom\w*|indicators?|roles?|role profiles?|pathways?|framework|content|tasks?|profiles?|standards?)\b|\b(?:EMST|taxonomy|competencies|indicators|role profiles|pathways|this release|content)\b[^.]{0,30}\b(?:has|have|is|are|was|were) (?:been )?validated\b|\bvalidated by (?:practitioners|SMEs?|experts|(?:a )?panels?|(?:a )?Delphi)\b/gi, neg: true },
  { id: "C13", rx: /\b(?:aligned|alignment|conforms?) (?:with|to) (?:the )?(?:O\*NET|ESCO|OPM)/gi, neg: true },
  { id: "C14", rx: /\bselection[- ]grade\b|\bfor (?:hiring|selection) decisions\b/gi, neg: true },
  { id: "C15", rx: /\bPolitical Savvy\b|\bInfluencing\/Negotiating\b/g },
];
// 2. Claims register do_not_say (strict phrases anywhere; short phrases near two claim anchors; conflations) and
//    the curated do_not_publish patterns.
const reg = parseRegister(parseCsv(readFileSync(ROOT + "docs/methods/claims_register.csv", "utf8")));
const dnp = yaml.load(readFileSync(ROOT + "site/claims/do_not_publish.yaml", "utf8")).patterns;
// 3. Tribal-hold trigger terms: allowed only inside the verbatim policy statement.
const gc = yaml.load(readFileSync(ROOT + "schema/lint/governed_content.yaml", "utf8"));
const tribal = gc.tribal_hold.triggers.map((p) => (typeof p === "string" ? new RegExp(p, "i") : new RegExp(p.pattern, p.cs ? "" : "i")));
// 4. Prototype content rules (team brief, DESIGN_SPEC §2.5 AC, R3 AI-04, IG-03/04, FED-05).
const RULES = [
  { id: "B1 internal words", rx: /effective-use-tier|closeMatch|relatedMatch|agentDraft|raterType|OBS-4|SSSOM|\bLLMs?\b|skos:|semapv/i },
  { id: "B2 never-say words", rx: /\b(validated|accredit\w*|approved|official(ly)?|verified|expert-reviewed|AI-powered|smart)\b/i },
  { id: "B3 alignment wording", rx: /\balign\w*/i },
  { id: "B4 Local Contexts", rx: /Local Contexts|\b(TK|BC) (Label|Notice)s?\b|Open to Collaborate|Attribution Incomplete/i },
  { id: "B5 held-record wording", rx: /\b(refus\w*|coming soon|locked|redact\w*|censor\w*|restricted|insiders?)\b/i },
  { id: "B6 eligibility", rx: /\byou (qualify|are qualified|are eligible|meet the requirements)\b/i, neg: true },
  { id: "B7 recommendation", rx: /\brecommend\w*/i },
  { id: "B8 e-mail", rx: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b/ },
  { id: "B9 phone", rx: /\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b/ },
  { id: "B10 query string in a link", rx: /https?:\/\/[^\s)]*\?/ },
  { id: "B11 UGESP or OMB memo", rx: /UGESP|OMB[^.]{0,60}27 August 2026|27 August 2026[^.]{0,60}\bOMB\b/ },
];

const hits = [];
const counts = { retired: 0, strict: 0, short: 0, dnp: 0, conflations: 0, tribal: 0, rules: 0 };
for (const { path, text } of items) {
  const isPolicy = text === POLICY;
  for (const c of RETIRED) for (const m of text.matchAll(c.rx)) if (!(c.neg && negated(text, m.index))) hits.push([path, c.id, m[0]]);
  for (const w of reg.strict) if (phraseRx(w.phrase).test(text)) hits.push([path, `register ${w.claim}`, w.phrase]);
  for (const w of reg.short) { const rx = new RegExp(phraseRx(w.phrase).source, "i");
    if (rx.test(text) && w.anchors.filter((a) => text.toLowerCase().includes(a)).length >= 2) hits.push([path, `register short ${w.claim}`, w.phrase]); }
  for (const d of dnp) for (const m of text.matchAll(new RegExp(d.rx, "gi"))) {
    if (d.unless_before && NEG.test(text.slice(Math.max(0, m.index - 20), m.index))) continue; hits.push([path, `do_not_publish ${d.claim}`, m[0]]); }
  for (const s of sentencesOf(text)) for (const c of reg.conflations) if (conflates(s, c)) hits.push([path, `conflation ${c.claim}`, s]);
  if (!isPolicy) for (const t of tribal) { const m = text.match(t); if (m) hits.push([path, "Tribal-hold trigger outside the policy", m[0]]); }
  for (const r of RULES) { if (isPolicy && r.id.startsWith("B2")) continue;   // the verbatim policy is data text
    const m = text.match(new RegExp(r.rx.source, r.rx.flags.replace("g", "") + "g")) || [];
    for (const x of m) { const at = text.indexOf(x); if (r.neg && negated(text, at, 40)) continue; hits.push([path, r.id, x]); } }
}
console.log(`Strings scanned: ${items.length} (COPY text values, GLOSSARY keys, expansions and definitions; structural fields key, id, t and kind are code and are skipped).`);
console.log(`Rules: ${RETIRED.length} retired-claim regexes (ADR-0027 §3); ${reg.strict.length} strict and ${reg.short.length} short register wrong forms, ${reg.conflations.length} conflation rules (claims_register.csv do_not_say); ${dnp.length} do_not_publish patterns; ${tribal.length} Tribal-hold triggers; ${RULES.length} prototype content rules.`);
console.log(`Held policy quoted verbatim: ${COPY.about.held[0].text === POLICY}. Deferred (double-quoted, not enforced by the explorer) register phrases also checked: ${reg.deferred.length}.`);
for (const d of reg.deferred) for (const { path, text } of items) if (phraseRx(d.phrase).test(text)) hits.push([path, `deferred register ${d.claim}`, d.phrase]);
console.log(hits.length ? `FAIL: ${hits.length} hit(s)` : "PASS: 0 hits");
for (const h of hits) console.log("  ", h.join(" | "));
process.exitCode = hits.length ? 1 : 0;
```

---

## 7. Glossary counts

### Method
- **What was searched:** every string value in all 69 files in `app/data/` (219,906 strings), loaded with `vm.runInThisContext`.
- **Matching:**
  - terms match on word boundaries, and a plural "s" is allowed;
  - all-capital keys match case-sensitively; other keys match case-insensitively.
- **Rules applied:**
  - a term was kept only if it occurs at least once;
  - acronyms, HR terms and field terms were preferred;
  - a term was left out where its meaning in the data was ambiguous, or where I was not sure of the definition.
- **What the counts include:** occurrences in IDs, titles, notes and source citations, as well as prose.
  - The O\*NET count includes O\*NET-SOC.
  - The SOC count includes O\*NET-SOC and "SOC 2018".

**Result:** 100 entries, and every one occurs at least once. The lowest counts are 1, for OSHA, PD, classification standard and IQR. The total is 11,785 occurrences.

**Left out on purpose** [E/J]:
- **Counted 0 in the data:** WUI, KSA, FES and CTAP. FES is common HR vocabulary, but it does not appear.
- **Ambiguous in the data:**
  - WPEA here is part of Washington class titles, not the whistleblower act;
  - DM codes are internal mechanism codes;
  - "IT", "R", "USA".
- **Uncertain status:** USWFS. The claims register has open rows on it.
- **Risky to define without more checking:** NEPATEC, the SPEED Act, environmental justice and ABET.
- **Would need trigger words to define:** THPO, and any Tribal term. These are never defined here.
- **Banned in UI text:** LLM and SSSOM.

| Term | Expansion | Occurrences | Data files it appears in |
|---|---|---:|---|
| BLS | Bureau of Labor Statistics | 233 | change, role, search |
| CEQ | Council on Environmental Quality | 77 | change, comp, role |
| DOI | US Department of the Interior | 41 | change, comp, role, search |
| DOJ | US Department of Justice | 28 | change, role |
| DOL | US Department of Labor | 50 | change, comp, role |
| EPA | Environmental Protection Agency | 84 | change, comp, role, search |
| FAA | Federal Aviation Administration | 23 | change, role, search |
| NIFC | National Interagency Fire Center | 6 | change, role |
| NRCS | Natural Resources Conservation Service | 6 | hr, paths, role |
| NWCG | National Wildfire Coordinating Group | 3 | hr, paths, role |
| OIRA | Office of Information and Regulatory Affairs | 11 | change, comp, core, search |
| OMB | Office of Management and Budget | 79 | change, comp, role, search |
| OPM | Office of Personnel Management | 566 | change, comp, core, hr, role, search |
| OSHA | Occupational Safety and Health Administration | 1 | hr |
| USDA | US Department of Agriculture | 46 | change, comp, role, search |
| USFS | US Forest Service | 14 | change, hr, role, search |
| ADA | Americans with Disabilities Act | 28 | change, role |
| CAA | Clean Air Act | 55 | change, role |
| CEQA | California Environmental Quality Act | 5 | change, comp, role, search |
| CFR | Code of Federal Regulations | 342 | change, comp, role |
| CWA | Clean Water Act | 66 | change, role |
| EA | environmental assessment | 4 | comp, search |
| EIS | environmental impact statement | 8 | change, comp, role, search |
| EO | executive order | 84 | change, comp, role, search, task |
| ESA | Endangered Species Act | 17 | change, comp, role, search |
| FR | Federal Register | 121 | change, role |
| NEPA | National Environmental Policy Act | 162 | change, comp, core, hr, paths, role, search, task |
| NHPA | National Historic Preservation Act | 6 | change, comp, search |
| RCRA | Resource Conservation and Recovery Act | 26 | change, comp, role, search |
| TEGL | Training and Employment Guidance Letter | 12 | change, role |
| WIOA | Workforce Innovation and Opportunity Act | 24 | change, role |
| Title V | — | 41 | change, comp, role, search |
| Section 106 | — | 11 | change, comp, search |
| Section 7 | — | 9 | change, comp, role, search |
| Section 404 | — | 8 | change, comp, role |
| NPDES | National Pollutant Discharge Elimination System | 21 | change, comp, role, search |
| NSR | New Source Review | 17 | change, role |
| PSD | Prevention of Significant Deterioration | 34 | change, role |
| MS4 | municipal separate storm sewer system | 4 | comp, search |
| TMDL | total maximum daily load | 2 | comp, search |
| NFIP | National Flood Insurance Program | 2 | comp, search |
| SME | subject-matter expert | 824 | comp, core, hr, role |
| RIF | reduction in force | 86 | change, core, hr, role |
| GS | General Schedule | 387 | hr, role, search |
| WG | Wage Grade | 8 | hr, role |
| SES | Senior Executive Service | 42 | comp |
| ECQ | Executive Core Qualifications | 49 | comp |
| FWCI | Federal Workforce Competency Initiative | 13 | hr |
| IDP | individual development plan | 2 | core |
| PD | position description | 1 | change |
| O\*NET | Occupational Information Network | 1,376 | core, role, task |
| O\*NET-SOC | O\*NET Standard Occupational Classification codes | 72 | role |
| SOC | Standard Occupational Classification | 156 | role |
| ESCO | European Skills, Competences, Qualifications and Occupations | 677 | comp, core |
| job analysis | — | 1,234 | comp, core, hr, role, search, task |
| crediting plan | — | 2 | comp, search |
| qualification standard | — | 80 | change, comp, hr, role |
| classification standard | — | 1 | hr |
| class specification | — | 26 | comp, hr, role |
| OPM series | — | 417 | comp, hr, role, search |
| specialized experience | — | 8 | hr |
| positive education requirement | — | 4 | hr, role |
| adverse action | — | 3 | core, hr |
| task book | — | 8 | comp, core |
| conservation corps | — | 94 | change, comp, core, hr, paths, role, search, task |
| CFM | Certified Floodplain Manager | 11 | paths, role, search, task |
| CHMM | Certified Hazardous Materials Manager | 10 | paths, role, search, task |
| PE | Professional Engineer | 22 | paths, role |
| REHS | Registered Environmental Health Specialist | 15 | hr, role, search, task |
| QEP | Qualified Environmental Professional | 10 | paths, role, search |
| AI | artificial intelligence | 2,538 | change, comp, core, hr, paths, role, search, task |
| GIS | geographic information system | 37 | comp, core, hr, paths, role, search, task |
| lidar | light detection and ranging | 36 | change, comp, core, role, search, task |
| UAS | uncrewed aircraft system | 7 | comp, paths, role, search |
| QA | quality assurance | 19 | comp, core, role, search, task |
| QC | quality control | 22 | comp, core, role, search, task |
| GHG | greenhouse gas | 36 | change, comp, core, paths, role, search |
| PFAS | per- and polyfluoroalkyl substances | 6 | comp, search |
| HAZWOPER | Hazardous Waste Operations and Emergency Response | 5 | hr, paths, role |
| EHS | environment, health and safety | 21 | comp, core, role, search |
| ESG | environmental, social and governance | 8 | comp, core, search |
| ICS | Incident Command System | 2 | comp, search |
| IQCS | Incident Qualifications and Certification System | 15 | change, hr, role |
| IQR | interquartile range | 1 | core |
| Delphi panel | — | 2 | core |
| prescribed fire | — | 173 | change, comp, core, hr, paths, role, search, task |
| burn boss | — | 32 | comp, core, hr, role, search, task |
| ground-truth | — | 149 | change, comp, core, hr, paths, role, search, task |
| remote sensing | — | 173 | change, comp, core, hr, paths, role, search, task |
| silviculture | — | 5 | comp, core, paths, role, search |
| riparian | — | 11 | comp, core, role, search, task |
| remediation | — | 139 | change, comp, core, hr, paths, role, search, task |
| reclamation | — | 39 | comp, core, role, search, task |
| hazard mitigation | — | 133 | change, comp, core, hr, paths, role, search, task |
| adaptive management | — | 42 | comp, core, hr, role, search, task |
| chain of custody | — | 8 | comp, core |
| stop-work authority | — | 77 | comp, core, hr, role, search, task |
| field craft | — | 8 | change, comp, core, role |
| data craft | — | 15 | comp, core |
| statecraft | — | 11 | comp, core |

---

## 8. Decisions and questions for the lead

1. **Held records: the policy text alone may fail CT-5 question 3.**
   - The brief limits `about.held` to the verbatim policy, the count, a heading and a link.
   - The policy does not say that Indigenous knowledge is out of scope by design, which R3 IG-02(a) requires and CT-5 question 3 tests.
   - The explorer's own `core.release.indigenousStatement` says it, verbatim.
   - **Option:** allow that one verbatim sentence on the held page. COMPREHENSION_TESTS.md tests both versions (CT-5 A and B). [J]
2. **The gallery's held notice paraphrases the policy and adds "related to Tribal employers".**
   - This breaks the verbatim-only rule, and it describes held content.
   - It should use `COPY.about.held` instead. (The gallery is not my file. I flag it here only.) [E: `app/gallery.html`, "Notices" section]
3. **Download links.**
   - `dist/` is git-ignored, and `.../contents/dist` returns 404 on GitHub. [E: `.gitignore`; GitHub API, 30 October 2026]
   - So the data page says honestly that files are not yet posted, and it points to the README build instead.
   - Publishing a GitHub Release (or similar) is a **decision point**. Until then, a "Download" link would 404.
4. **Spec wording I changed, and why.**
   - "Checked: not a match" became **"Not a match (noted by an AI agent)"**, because "checked" implies a person.
   - "Two AI coders found no matching O\*NET task" became `match.none` + `match.twoCoders` or `match.disagree`, because 69 of the 114 no-match rows are disagreements.
   - The `validated` review status is labeled **"Passed its use test"**, and the top ladder rung **"Cleared for a stated use"**, because R3 AI-04 bans "validated" in copy. The keys are unchanged.
5. **Hosting logs.**
   - The privacy page says that the host "may keep basic server logs".
   - Name the host and its log policy before any public launch [E: R3 PF-03].
6. **The release is not cleared for external publication** (gate items 6 and 7) [E: `core.status.gate`]. The status page says so plainly.
   - If the prototype is shown outside the project before those items pass, the same notice should appear on the home page as well.
7. **A route without a GitHub account:** still undecided [E: RESEARCH_SYNTHESIS §9.1]. The copy says "under consideration".
8. **The AI line A/B test.**
   - The shipped `ai.line` is the short form (variant B in CT-1), and `ai.detail` names the human role and the review path.
   - If CT-1 shows that variant A reduces the "no human involved" and "AI means false" misreadings, swap `ai.line` for variant A's wording.
