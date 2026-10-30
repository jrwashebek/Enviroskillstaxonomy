# EMST public interface: research synthesis

**Status:** desk research and expert inspection, 30 October 2026. **No real users have taken part yet.** Everything here about what people need is a hypothesis to test. The plan to test it is in §8.
**Prepared by:** Claude, as HCD lead, with an agent research team for the EMST project lead.
**Inputs:** four studies in `docs/research/`:
- R1, a benchmark of 19 public taxonomy services;
- R2, user-needs evidence for nine user groups;
- R3, standards, trust and accessibility;
- R4, an evaluation of the current explorer plus a data content audit.

**Evidence labels:** [E] sourced, with the study and section given; [J] judgment; [S] speculation.

---

## 1. The problem in one paragraph

EMST's data is the most detailed open description of environmental management work we found: 1,317 concrete tasks, 223 competencies with five-level indicators, and 37 roles with variants by employer [E: R4 §7]. The current explorer protects that data well. It sets no cookies, makes no third-party requests, hides values that are not validated, and has zero axe violations on 18 tested pages [E: R4 §5, §8]. But people would struggle to use it:
- the status layer swamps the work itself: "Assessment pending" appears 28,165 times, a median of 185 times per role page [E: R4 #1];
- internal vocabulary leaks onto every page, for example "effective-use-tier@1.1.0" 7,101 times [E: R4 #2];
- search fails on 18 of 50 realistic queries [E: R4 #4];
- navigation runs one way, with no competency linking back to a role [E: R4 #5].

The redesign problem is to **keep every honesty and privacy rule while making the work itself readable, findable and usable by people who are not taxonomists.**

---

## 2. What we learned: twelve insights

| # | Insight | Evidence | What it means for the design |
|---|---|---|---|
| I1 | **The work is the product, but status swamps it.** The task statements are well written and specific. People can't find them under status labels, double listings and 42 collapsible sections per page. | R4 #1, #3; R4 §8 | Lead every page with the work. Show status **once per context**, in plain words, linked to an explanation. |
| I2 | **People look for work by the title they know, in their own words.** Applicants search by title; titles carry 25 times more distinctions than SOC codes. EMST users need official titles, descriptive titles, series codes, NWCG and fire slang, and both British and American spellings ("programme" appears 957 times in rc.1). | R2 §8, §11.2, T9; R4 #4 | Make search forgiving: synonyms, codes, typos, prefixes, spelling variants. **Explain why each result matched.** When the work isn't covered, say so and offer a way to suggest it. |
| I3 | **The commonest need is translation across employers. The biggest risk is implying eligibility.** Seven of nine internal personas ask "what is my work called elsewhere, and does it count?". Military translators fail by matching titles and implying fit; a task-level method found about 9 times more matches, but needed expert review. | R2 §11.1, §8, T2; R1 anti-pattern 4 | Show what is shared and what to check, at **task and competency level**, with the caveat at the point of comparison. Never "you qualify". Never a single match score. |
| I4 | **Honest AI disclosure costs trust only where trust hasn't been earned.** "AI-generated" labels lower perceived accuracy because readers assume no human was involved, and in rc.1 none was. Being exposed by someone else costs more than disclosing yourself. Describing the human role, and the review path, reduces the penalty. | R3 §4; R2 §11.3 | Give every record one plain line saying what AI did and what people have not yet done. Show the planned review path. Put details on demand. |
| I5 | **What a record may be used for is the white space no benchmark fills.** But verbal labels drift towards meaning "50/50" unless anchored with examples. | R1 §6; R2 §11.4 | Turn use tiers into "**You can use this for … / Don't use it for …**" with concrete examples. Put HR-specific prohibitions on HR-relevant pages. |
| I6 | **"Pending" must never read as zero.** Blank or zero-filled cells distort judgments. EMST currently repeats "pending" in every row and draws empty charts. | R3 §3; R4 #1 | Show pending values **once per section, as a count** ("0 of 29 tasks assessed"). Say why and what would change it. Never in a chart. Sort it last. |
| I7 | **Navigation must run both ways and use the structures people think in.** No competency links to a role. Half the tasks belong to no role. The 17 job families and employer types are never used for navigation. | R4 #5, §1.2 | Link both ways (role ↔ competency ↔ task). Browse by job family, employer type and module. Comparison is a first-class route. |
| I8 | **Federal HR already has an AI PD tool (USA Class), and its rules are moving.** EMST's place is reference language that travels into other tools, dated and versioned. OPM proposed consolidating 115 series in April 2026, and rules keep changing through FY2027. | R2 §2, T8; R1 §3.16 | Offer copy, print and CSV of task language, carrying source, date, release ID and the HR disclaimer. Put "as of" on every borrowed OPM, O\*NET or state reference. Flag proposed realignments. No assessment or PD builders. |
| I9 | **Plain language and phones set the floor.** Record text reads at grade 14–20. 28% of US adults read at or below Level 1. Smartphone-only access is common among lower-income users. Most fire lines have little or no signal. | R4 §7.2; R2 §8; R3 §2, §8 | Summary first. Short labels. Expand jargon and acronyms on demand. A strict performance budget. Print-quality task lists. |
| I10 | **Corrections need an easy channel and a visible answer.** Ignored newcomers leave. GitHub suits code better than text. Peer bodies (NIST, NICE) keep an email fallback, which EMST's build forbids. | R2 §10, T5; R1 rec. 9 | Let people copy a reference (record ID and release) in one tap, open GitHub Issues, and see a corrections register. **Decision for the project lead:** a non-GitHub route. |
| I11 | **Look independent, not governmental.** USWDS forbids its banner on non-.gov sites. A federal look implies endorsement, but federal users still need something credible and familiar. | R3 §6 | Use a field-guide visual identity on accessible, familiar patterns. Say "An independent open project. Not a government website." Run comprehension test CT-0 to check it. |
| I12 | **Numbers on crosswalks create false precision, and the current site shows non-matches as matches.** "Confidence 0.5" appears on unreviewed AI rows. 108 rows marked "not a match" in the source (102 ESCO, 5 SOC, 1 OPM series) render as matches on today's explorer. | R1 rec. 6; checked against `dist/` and `site/src/_includes/macros.njk` | Use plain match types ("Broader category · AI-suggested, not reviewed"), with no decimals on screen. Show "not a match" rows as non-matches. **Report the explorer bug to its owner.** |

---

## 3. Who we are designing for: five modes, not nine personas

The nine user groups overlap: a corps programme lead also supervises, and an HR specialist also plans. Their jobs cluster into five **modes**. One person can move between modes in a single visit. We use modes rather than invented named personas, so that this unvalidated evidence does not get a human face it hasn't earned. [J; the internal CP plan says "simulated voices are not research"]

| Mode | Who (user groups) | Core job | Stakes | Must never |
|---|---|---|---|---|
| **M1 Describe the work** | Federal and state HR, classifiers (U5, U4); supervisors (U3) | "When I write or check a description of a job, I want current, specific task language with its source and date, so the description is accurate and defensible." | High: legal and merit rules | Use EMST as a job analysis, classification basis, crediting plan, assessment, RIF or appraisal input |
| **M2 Develop people and programmes** | NGO and corps training leads (U1), educators and curriculum designers (U6), supervisors (U3) | "When I plan training or a course, I want the competencies a role needs, at each level, in words I can map to, so learners build what the work needs." | Medium | Treat draft indicators as validated assessment criteria; rank staff |
| **M3 Find my next move** | Early-career staff and corps members (U2), career changers including veterans and seasonal firefighters (U8) | "When I'm deciding my next step, I want to see what my work is called elsewhere and what overlaps, so I can search and train with the right words." | High: personal livelihoods | Read overlap as eligibility; "you qualify" |
| **M4 Anticipate change** | Workforce planners and boards (U5, U6); programme leads (U1, U4) | "When I plan for the next few years, I want honest signals of what is changing, with how strong the evidence is, so I neither overreact nor miss it." | Medium | Read watch signals as forecasts |
| **M5 Use, check and improve the data** | Researchers and developers (U7); practitioners and subject-matter experts (U9) | "When I reuse or correct EMST, I want stable IDs, provenance and an answered correction route, so my work is reproducible and my fixes count." | Medium | Strip caveats when republishing; post personal data in issues |

**Tribal natural-resource professionals** are not a mode. EMST has no standing to design for them until the Tribal Advisory Council process decides how they take part (ADR-0007; R3 §5). The interface shows only the held-records count and the policy statement.

---

## 4. Top tasks (ranked hypothesis, to be tested with a top-tasks survey)

| Rank | Task | Modes | Prototype route |
|---|---|---|---|
| 1 | Find a role by the title I know and see what the work involves | all | Search → Role |
| 2 | See which competencies a role needs, at what level | M2, M1 | Role → Competencies |
| 3 | See what my work is called with other employers, and what overlaps | M3 | Role → "Elsewhere"; Compare |
| 4 | Understand what I may and may not use this for | all | Status line → How to read EMST |
| 5 | Copy, print or export task language with its source and date | M1, M2 | Role → Copy / Print / CSV |
| 6 | Look up a competency's levels and indicators for a course or plan | M2 | Competency |
| 7 | See what is changing for a role, honestly | M4 | Role → Changing; What's changing |
| 8 | Look up an OPM series or state class and its linked roles | M1 | Series / Class pages |
| 9 | Download and cite the data | M5 | Data & downloads; "Cite this" |
| 10 | Report something wrong | M5 | "Suggest a correction" on every record |

---

## 5. Design principles

1. **Lead with the work.** Tasks, competencies and levels come first. Status, provenance and machinery come second, one click away. (I1)
2. **Say it once, plainly, and link to more.** One status line per record; one count per pending section; a single public key that explains every label. No jargon on screen that is not explained on the same screen. (I1, I4, I6)
3. **Meet people in their own words.** Titles, codes, slang, spellings and typos all lead somewhere. When something isn't covered, say so honestly and offer a next step. (I2)
4. **Describe work; never judge a person.** No "you qualify", no scores of people, no rankings. Every comparison carries its caveat at the point of use. (I3, I5)
5. **Every claim carries its basis and its date.** Who drafted it, from what, when, and whether a person has checked it. Borrowed references carry "as of" dates. (I4, I8, I12)
6. **Any way in, both ways through.** Search, job family, employer type, competency and task all connect, and every link has a way back. (I7)
7. **Light enough for a phone in the field; good enough to print.** A performance budget, reflow to 320px, print styles, no hover-only content. (I9)
8. **Make the correction loop visible.** Every record says how to report a problem, and what happened to reports. (I10)

---

## 6. Requirements traceability (must-haves for the prototype)

| ID | Requirement | Source |
|---|---|---|
| R-1 | Forgiving search across roles, competencies, tasks, OPM series, state classes, tools and credentials. Synonyms, codes, typos, prefixes and British/American spelling. "Why this matched" on every result. | I2; R1 P6; R4 #4 |
| R-2 | An honest zero-results answer: suggest related terms, browse routes and "Suggest a role or task we're missing". | I2; R4 search test |
| R-3 | Role page leads with function, then the top tasks ("8 of 29 · Show all"), then competencies by role level. | I1; R1 P4 |
| R-4 | One status line per record: use tier as "You can use this for / Don't use it for", plus "Drafted by AI agents · not yet reviewed by people", linked to the key. | I4, I5; R1 rec. 1–3; R3 §4 |
| R-5 | Pending values summarized once per section with a count and the reason. Never a cell of "pending". Never a chart of empty bars. | I6; R3 §3 |
| R-6 | Employer variants shown as a switcher, with the differences (credentials, sign-off, instruments) stated. | I3; R1 §6 |
| R-7 | Comparison of two roles: shared, only-A and only-B competencies and tasks; target-level gaps; what to check (credentials). Caveat at the top. No single score. | I3; R1 rec. 7 |
| R-8 | Two-way links: competency → roles; task → roles and competencies. Browse by job family and employer type. | I7; R4 #5 |
| R-9 | Crosswalks in plain match types, with no decimals on screen, review state shown, and non-matches shown as non-matches. Borrowed references dated. Proposed OPM realignments flagged. | I8, I12 |
| R-10 | Copy as plain text, print and CSV for a role's tasks and competencies. Every export carries the release ID, date, source line and the HR disclaimer. | I8; ADR-0027 (PD skeleton export) |
| R-11 | "Cite this" and "Suggest a correction" on every record: copy the reference, open GitHub Issues, explain what happens next. | I10; R1 rec. 9–10 |
| R-12 | A "How to read EMST" key: every label with an example; use tiers with examples of allowed and forbidden uses; what "AI-drafted" means and the review path; the held-records statement. | I4, I5; R1 P2; R3 §3–5 |
| R-13 | Independent identity: "Not a government website" statement; no government banner. | I11; R3 §6 |
| R-14 | WCAG 2.2 AA:<br>• keyboard;<br>• route changes announced, with focus moved to the H1;<br>• reflow at 320px;<br>• no hover-only content;<br>• forced-colours mode works. | ADR-0027 §4; R3 §1 |
| R-15 | Privacy:<br>• no cookies, storage, analytics, fetch or third-party requests;<br>• no user input in URLs (so search queries are not linkable; a deliberate trade-off). | site README; R3 §9 |
| R-16 | Performance:<br>• first view at most 200 KB gzipped before data;<br>• core data at most 60 KB gzipped;<br>• each page's data loads on demand. | R3 §8; R4 #9 |
| R-17 | Every governance rule inherited through the explorer's view model:<br>• display gate;<br>• claims register;<br>• Tribal hold;<br>• withheld credential gates and signals;<br>• HR disclaimers. | BRIEF constraints; DATA.md |

---

## 7. Information architecture

```
Header:  EMST [home]   [Search a job title, task, skill or code …]   Roles · Competencies · Compare · What's changing · About the data
         Status ribbon: Draft release 2.0.0-rc.1 · Drafted by AI agents, not yet reviewed by people · What this means →

Home  (#/)
  ├─ Search (primary)        ├─ Top tasks (five plain verbs, not audiences)
  ├─ Browse by job family     ├─ Browse by employer type
  └─ "What you can use EMST for" (three lines) · release facts · not a government website

Roles  (#/roles)                      filter: job family · employer type · depth (P1–P4 as plain words) · lifecycle
  └─ Role  (#/role/:slug[@section])   sections: Overview · The work (tasks) · Competencies · With other employers (variants)
                                      · Connections (series, classes, O*NET) · Where it can lead (exploratory)
                                      · How it is changing · About this record (provenance) · Copy / Print / CSV · Cite · Correct
Competencies (#/competencies)         filter: module · type · level span · used in role
  └─ Competency (#/competency/:slug)  Overview · Levels L1–L5 with indicators · Used in roles · Tasks · How employers differ
                                      · Related elsewhere (ESCO etc.) · About this record
Task (#/task/:slug)                   statement · competencies · roles · assessment status (once) · O*NET task matches · v1 evidence drawer
Compare (#/compare[/:a[/:b]])         choose two roles → overlap, differences, level gaps, what to check
What's changing (#/changing)          signals (watch) · emerging roles · policy instruments · scenarios · what would change our view
Federal series (#/series[/:code]) · State classes (#/classes[/:slug])   HR disclaimer on every page
About the data (#/about[/:page])      How to read EMST (key) · How it was made · Release status · Data & downloads
                                      · Corrections & contributing · Held records · Accessibility · Privacy
Search results (#/search)             grouped by kind; "why this matched"; query never enters the URL
```

The content model (fields per page) and component mapping are in `DESIGN_SPEC.md`.

---

## 8. Validation plan: what must be tested with real people before launch

| Study | Question | Method and sample | Pass criterion |
|---|---|---|---|
| **CT-0 to CT-5 comprehension** (R3 §11) | Do people correctly read:<br>• "not a government site";<br>• "AI-drafted";<br>• "assessment pending";<br>• use tiers;<br>• crosswalk match strength;<br>• the held-records notice? | 5–8 per mode per round until no harmful misreading, then about 80 (28% lower-literacy) | ≥ 72/80 correct; ≤ 2/80 harmful misreadings. Any "yes, I can use this to hire" counts as harmful |
| **Words people type** (R2 unknown 3) | What do people call their jobs? | Collect 200–300 real titles from USAJOBS, state boards and corps postings (desk); then a first-click and search test with 30+ people | ≥ 85% of real titles reach a relevant role in the top 3 results |
| **Top-tasks survey** | Is the ranking in §4 right? | Gerry McGovern top-tasks survey via pilot partners, 100+ responses | Ranks the top 5 tasks |
| **Task-based usability** | Can each mode finish its core task unaided? | 5 per mode, moderated and remote, phone and desktop, ≥ 2 assistive-technology users per round | ≥ 80% task success; zero eligibility misreadings in M3 |
| **Translator harm test** (R2 unknown 5) | Does Compare make people believe they qualify? | Veterans and seasonal firefighters, n ≈ 12 | No false "I qualify" conclusions |
| **HR fit** (R2 unknown 2) | Where does EMST fit beside USA Class and USA Staffing? | Contextual inquiry, 6–8 federal and 6–8 state HR staff (PRA-aware) | A named slot in their workflow, or a decision to stop |
| **Correction channel** (R2 unknown 6) | Do SMEs file corrections, and through which channel? | Concierge test, 10–15 SMEs, GitHub against an alternative | Completion ≥ 70%, median under 3 minutes |
| **Field and print** (R2 unknown 4) | Does the site work at low signal and on paper? | In-season diary study and a device lab | Task list usable offline from a print or saved file |

The prototype includes everything these studies need to run.

---

## 9. Decisions for the project lead (raised by the research)

1. **Non-GitHub correction route** (I10, R2 T5). The explorer's build forbids e-mail addresses on pages. Options:
   - keep GitHub only;
   - allow one project contact address;
   - a static form hosted elsewhere, which breaks the no-third-party rule.
2. **Credit for contributors** (R2 §10). The "no personal names" rule may deter experts who want credit. Option: opt-in credit in release notes.
3. **"Open to Collaborate" Notice** (R3 §5; open question Q11). Only if EMST makes that commitment. Never apply TK or BC Labels or Notices.
4. **Spelling.** US users and official US titles use American spelling. Consider American spelling for labels in a US-facing release (R2 T9). The prototype normalizes spelling in search only.
5. **Positioning against USA Class** (R2 §2). EMST supplies reference language; it builds no PD drafting tool. Confirm this before the full PD builder planned for v2.1 (ADR-0027).
6. **Explorer bug to fix:** the current explorer renders 108 crosswalk rows that the SSSOM source marks "not a match" (`predicate_modifier: Not`) as ordinary matches: 102 ESCO (X7), 5 SOC (X3) and 1 OPM series (X4).
   - **Cause:** `site/src/_includes/macros.njk` line 53 prints the predicate without its modifier. The view model's `closeOrBetter` flag is correct.
   - **Effect:** some show as "close" matches.
   - **The prototype shows them as non-matches.**
