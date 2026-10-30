# R3: Standards, trust and accessibility for the EMST public interface

- **Author:** the HCD team's standards, trust and accessibility researcher (an AI agent)
- **Date:** 30 October 2026
- **Status:** desk research. Nothing here has been tested with users.

**Evidence labels.**
- **[E]** I read the source, as listed under the section or in the repository.
- **[J]** Judgment, with its basis.
- **[S]** Speculation, with what would settle it.

**Sources marked †** were not re-read today, either because the fetch tool blocked them or because the request failed. They rest on my earlier reading of stable texts: WCAG and ARIA APG wording, the IPCC guidance note, W3C PROV and DataCite practice. Spot-check them before quoting.

These URLs were blocked or failed today:
- access-board.gov/ict/;
- the W3C *Understanding* page for SC 2.4.11;
- digital.gov/guides/plain-language;
- PMC12166545 (Wittenberg et al.);
- the Pew mobile fact sheet;
- the IPCC guidance-note PDF.

---

## Executive summary

1. **WCAG 2.2 AA, EMST's own gate, is the highest standard that applies.** [E]
   - Section 508 still uses WCAG 2.0 AA.
   - The ADA Title II rule uses WCAG 2.1 AA. An interim final rule of 20 April 2026 moved its deadlines to **26 April 2027** for entities serving 50,000 people or more, and **26 April 2028** for smaller entities.
   - WCAG 3 is still a draft.
   - These laws bind EMST's state and local adopters, not EMST itself.
2. **Plain language is a requirement.**
   - 28% of US adults are at or below PIAAC Level 1 in literacy (2023), and 34% in numeracy. [E]
   - Every page footer prints the full use notice, including `agentDraft`, `raterType` and `OBS-4`. [E: `base.njk` l.58–59]
3. **Honest uncertainty costs little trust.**
   - Numeric ranges barely moved trust (van der Bles 2020, N = 5,780). Vague verbal caveats moved it more. [E]
   - "Low-quality evidence" labels reduce trust *and* intended use (Schneider 2022, N = 6,489). [E] For EMST, less use in decisions is the intended effect.
4. **An "AI-generated" label is penalised because readers assume no human oversight** (Altay & Gilardi 2024, N = 4,976). [E]
   - For EMST, that assumption is true, so the trust cost is honest.
   - Say what the label means in one line, with detail on demand (Prajod 2026). [E]
   - Show the planned review path. Human review is what raises credibility most (Valenzuela 2026). [E]
5. **OPM's 27 August 2026 memo matches EMST's own rule.** AI-drafted job analyses and competency content need SME validation against actual duties. Without it, OMB M-25-21 treats the use as high-impact. [E]
   - EU AI Act Article 50 applies from 2 August 2026. It is unclear whether it reaches EMST. [E/J]
6. **Disclaimer fatigue is the main design risk.** Attention to repeated warnings fades (Vance 2018), and people skip boxed, ad-like elements (NN/g 2018). [E]
   - Use layers: one site-level page, one status line per record, and details on demand.
   - Make only the exceptions stand out.
7. **"Pending" must never read as zero** (Song & Szafir 2019). [E] Show it as words, sort it last, and keep it out of totals.
8. **Local Contexts Labels are for communities only.** [E] EMST must never apply one. An "Open to Collaborate" Notice is a decision for the project lead (Q11).
9. **Look independent, not governmental.** USWDS forbids its banner on .com and .org sites. [E] EMST must say plainly that it is not a government site.
10. **Field use.** [E]
    - 72% of rural adults have home broadband, against 84% in the suburbs. GAO notes most wildland fires have little or no cell coverage.
    - Search (95 KB gzip) and the gap check (118 KB gzip) are the heaviest pages.
    - Offline means print, files and a portable-site zip.
    - Learning means planned research, not analytics.

**Comprehension tests (§11).**
- **Format:** six tests, each run as formative rounds of 5–8 people per segment, then a summative test with 80 people, about 28% of them low-literacy.
- **Pass rule:** at least 72 of 80 correct, and no more than 2 of 80 critical misreadings.

---

## 0. Baseline: what the explorer already does [E]

Sources: `site/README.md`, `site/src/**`, `dist/2.0.0-rc.1/RELEASE_NOTES.md` and the SSSOM files.

**Privacy and security**
- There are no cookies, no browser storage, no analytics and no runtime requests. The CSP sets `connect-src 'none'` and `form-action 'none'`.
- External links may not carry query strings.

**Accessibility**
- axe-core runs on 50 pages, with disclosures both open and closed.
- Reflow is checked at 320 px, and focus is checked on the first 12 Tab stops.
- A conformance report is in `site/ACR.md`.

**Status display**
- Every figure carries a use-tier badge and an evidence badge, for example "Use tier: describe · Evidence: S speculation; AI-agent draft, unreviewed".
- The display gate fails closed: every task shows **Assessment pending**.

**Footer** (on every page)
- Release, build and gate metadata.
- The full use notice.
- The Indigenous-knowledge statement and the hold sentence.
- An AI-authorship paragraph.
- A GitHub Issues link.

**Participation and citation**
- The "Challenge a judgment" page says a GitHub account is needed.
- The repository has no `.github/ISSUE_TEMPLATE` and no `CITATION.cff`.

**Crosswalk data**
- Every crosswalk row is `semapv:LLMBasedMatching` with `review_status=llm-reviewed-candidate`.
- Predicates are close, broad, narrow and related matches, with agent "confidence" values from 0.4 to 0.6. ESCO, for example, has 129 close, 21 narrow, 8 broad and 180 related.

**Tribal hold**
- 163 Tribal-related records are held. The release notes give only the count.

---

## 1. Accessibility

### Findings

**The rules and how they apply**

| Instrument | Standard | Applies to | Dates (checked 30 Oct 2026) | EMST relevance |
|---|---|---|---|---|
| Section 508 | WCAG 2.0 AA | federal ICT | in force; no update announced [E] | federal adopters (U5) will ask for a conformance report |
| ADA Title II web rule | WCAG 2.1 AA | state and local government, including content provided through "contractual, licensing, or other arrangements"† | 26 Apr 2027 (population 50,000 or more); 26 Apr 2028 (smaller entities and special districts); interim final rule 20 Apr 2026; comments closed 22 Jun 2026; no later change found [E] | state adopters (U4) republishing EMST content |
| WCAG 2.2 | — | EMST's release gate | Recommendation, updated 12 Dec 2024; also ISO/IEC 40500:2025 [E] | covers everything in 2.1 AA except 4.1.1 Parsing, which was removed |

**Success criteria most at risk in a data-dense taxonomy**

[E for SC text: Deque's WCAG 2.2 summary; the rest †. Risk notes are J.]

| SC | Level | Risk in EMST |
|---|---|---|
| 1.3.1 Info and Relationships | A | Tables need `caption`, `th` and `scope`. Badges and "pending" must be real text. |
| 1.4.1 Use of Color | A | Use tier, match strength and "pending" must not be shown by colour alone. |
| 1.4.10 Reflow | AA | Data tables are exempt, but pages are not. Compare views and crosswalk tables are the risk. |
| 1.4.11 Non-text Contrast | AA | Badge outlines, focus rings and sort icons need 3:1 contrast. |
| 1.4.13 Content on Hover or Focus | AA | Do not use tooltips for definitions. |
| 2.4.11 Focus Not Obscured (Minimum) | AA | A sticky header, sticky table headers or a compare tray can hide focus. |
| 2.5.8 Target Size (Minimum) | AA | Targets must be 24×24 CSS px, or have 24 px of spacing. At risk: sort buttons, "?" toggles, copy-ID buttons, chips and pagination. |
| 3.2.6 Consistent Help | A | Help and challenge links must sit in the same relative order on every page. |
| 3.3.7 Redundant Entry | A | The gap-check re-open, compare selections and the challenge route must not ask for the same input twice. |
| 4.1.2 Name, Role, Value; 4.1.3 Status Messages | A / AA | Comboboxes, sort buttons and disclosures need correct names and states. Result and sort changes must be announced. |

**Patterns**

- **Autocomplete search**
  - The APG combobox pattern is complex, and assistive-technology support for it varies.†
  - GOV.UK's `accessible-autocomplete` now carries a notice that maintainers "are not currently responding to issues or pull requests". [E]
  - EMST's search already uses a plain search field, an on-page results list and a polite live count. [E: `site/src/search/index.njk`]
  - Keep it. Use a combobox only for choosing from fixed lists, such as a role or a series. [J: fewer ARIA states to get wrong; works without JS; matches GOV.UK site search]
- **Sortable tables**
  - In the APG sortable-table example, header cells contain buttons, and `aria-sort` is set only on the sorted column.†
  - The MOJ sortable table uses `aria-sort` and `data-sort-value`. It is marked "to be reviewed" and has no research behind it. [E]
- **Tabs or accordions**
  - GOV.UK says not to use tabs when "users need to compare information" across them, and says its tabs component "has not yet been tried in research with users". [E]
  - EMST role pages invite comparison, so use headings, an on-page contents list and `<details>`.
- **Compare views**
  - I found no compare component in GOV.UK or USWDS. My search was not systematic. [J]
  - Build compare as a data table with at most four entities as columns, attributes as row headers, and an announced "differences only" toggle.
  - At 320 px, stack it as one summary list per entity. USWDS offers a stacked table variant.†
- **Cognitive accessibility**
  - W3C COGA's *Making Content Usable* (Group Note, April 2021) [E] includes these patterns:
    - clear words;
    - summaries of long content;
    - avoiding too much content;
    - a clear page purpose;
    - easy-to-find help;
    - alternatives for numerical concepts.

### Requirements

| ID | Requirement | Priority | Source |
|---|---|---|---|
| A-01 | The interface must conform to WCAG 2.2 AA on every template, with disclosures both open and closed. | must | brief; WCAG 2.2 |
| A-02 | Each release should publish an ITI VPAT-format conformance report (WCAG and 508 editions) for federal and state procurement. | should | 508 practice†; J |
| A-03 | Help, challenge and "How EMST was made" links must sit in the same relative order on every page. | must | SC 3.2.6 |
| A-04 | All targets must be at least 24×24 CSS px or have 24 px spacing. | must | SC 2.5.8 |
| A-05 | Sticky elements must never hide focus. Use `scroll-padding`. Avoid sticky compare trays. | must | SC 2.4.11 |
| A-06 | Site search should stay a plain field with an on-page result list and a polite live count. Use a combobox only for fixed lists. | should | APG†; GOV.UK notice; J |
| A-07 | Sortable tables must put a button in each sortable `th`, set `aria-sort` only on the sorted column, keep a `caption`, and announce the result, for example "Sorted by importance, descending. 1,317 pending, listed last." | must | APG†; MOJ; SC 4.1.3 |
| A-08 | Record pages should use headings, a contents list and `<details>`, not tabs. | should | GOV.UK tabs |
| A-09 | Compare views must be data tables with row and column headers, at most 4 entities, and a stacked layout at 320 px. | must | SC 1.3.1, 1.4.10 |
| A-10 | Multi-step tools must carry forward what the user has already entered, including re-opened files and the record ID shown for copying. | must | SC 3.3.7 |
| A-11 | Definitions must be inline text or `<details>`, never tooltip-only. | must | SC 1.4.13; brief |
| A-12 | Each page should state its purpose in its first sentence and give a summary before long tables. | should | COGA |
| A-13 | Manual tests should cover NVDA with Firefox, JAWS with Chrome, VoiceOver on iOS, and zoom at 200% and 400%. | should | J: automated checks find only part of WCAG |

### Pitfalls
- Home-made tabs or comboboxes, or inherited libraries that are no longer maintained.
- `aria-sort` set on every column.
- Sort icons with no text equivalent.
- Meaning carried by colour or CSS `::before` content.
- Treating axe results as conformance.
- Designing to 2.1 AA because "that's the law".

---

## 2. Plain language and reading level

### Findings

**Literacy** [E: IES press release, 10 Dec 2024]
- The US average literacy score in PIAAC 2023 was 258, down from 271.
- 28% of adults were at or below Level 1 in literacy, and 34% at or below Level 1 in numeracy.
- [J] Many learners, corps members and career changers (U2, U8) read on phones. A sizeable minority will misread decimals such as "0.6" and percentages.

**Federal guidance**
- plainlanguage.gov now redirects to digital.gov guides. [E: observed redirect]
- The Center for Plain Language reports that the Federal Plain Language Guidelines were taken down. It has reposted the last version. [E, January 2026] Cite that copy.

**GOV.UK practice** [E: Surrey County Council guide citing GOV.UK and the GDS post "Clarity is king"]
- GOV.UK aims for a reading age of about 9.
- Specialists also prefer plain text because they understand it faster.

**Defining technical terms** [J: ISO 704†; SKOS†; the Data Cards "shared vocabulary" principle [E]]
- Give a one-sentence definition: the broader class plus what makes this term different.
- Add one field example and one "not to be confused with" note.
- Record practitioners' synonyms as `altLabel` or `hiddenLabel`, for example "prescribed fire", "controlled burn" and "Rx burn".
- Readability formulas penalise necessary technical terms. Use them as an alarm on interface text only.

**Internal jargon reaches the interface** [E]
- In the footer:
  - "display gates … release view stamped … use tiers"
  - "`agentDraft` sub-object, raterType, validationStatus … OBS-4 … *_status columns"
- In badges: "Evidence: S speculation".
- Coming in crosswalk and role views: "skos:closeMatch", "SSSOM", "P1 corridor", "enactment".

### Requirements

| ID | Requirement | Priority | Source |
|---|---|---|---|
| PL-01 | Interface text must target roughly US grades 6–8, checked with a readability formula and by a human edit. | must | PIAAC; GOV.UK; FDA low-literacy band, grades 4–8 [E] |
| PL-02 | The footer must not carry the use notice or build metadata. Replace them with one sentence and a link, "What EMST is and isn't for", and move the metadata to "About this release". | must | COGA "avoid too much content"; §3 habituation |
| PL-03 | Every record type must have a public definition: a one-sentence definition, a field example and a "not to be confused with" note. | must | ISO 704†; COGA |
| PL-04 | Search should index practitioners' synonyms, and pages should show "also called". | should | SKOS†; J |
| PL-05 | Internal codes (ADR, WP, CR and OBS numbers, raterType, SKOS and SSSOM predicates) must not appear in default views. | must | J |
| PL-06 | Numbers must come with words, for example "0 of 1,317 tasks assessed". Avoid decimals in default views. | must | PIAAC numeracy; COGA |
| PL-07 | A plain glossary should define "use", "assessment pending", "drafted by AI", "crosswalk", the four match types and "held until Tribal consent", linked at first use. | should | COGA; Data Cards |
| PL-08 | Labels should use task words, for example "What you can use this for", not "Use tier: describe". | should | GOV.UK; J |
| PL-09 | Federal-facing pages should use OPM's terms correctly: position description, job analysis, crediting plan, SME. | should | OPM memo [E] |

### Pitfalls
- Plain versions that drop the caveat.
- Grade-level targets applied to technical definitions.
- Abbreviations in badges.
- Writing only for HR specialists.

---

## 3. Communicating uncertainty and provenance

### Findings

**Trust research**
- **van der Bles et al. 2020** (*PNAS*; five studies, N = 5,780, including a BBC News field test) [E]:
  - numeric ranges had little effect on trust in the number (pooled d ≈ −0.15) and none on trust in the source (d ≈ −0.03);
  - vague verbal statements did more harm (d ≈ −0.55);
  - "estimated" and similar words did not signal uncertainty at all.
  - Their 2019 framework separates *direct* uncertainty, about a number, from *indirect* uncertainty, about evidence quality.†
- **Schneider et al. 2022** (*Judgment and Decision Making*; N = 6,489) [E]:
  - low-quality-evidence cues reduced trustworthiness and intended use;
  - high-quality cues barely helped;
  - ambiguous cues hurt as much as low-quality ones.
- **Kerr et al. 2022** (*PNAS Nexus*): balanced communication was trusted as much as persuasive messaging, or more, especially by people who were sceptical or neutral at the start. [E]
- **[J] What this means for EMST.** EMST's uncertainty is indirect: no review and no reliability study. Honest labels will lower use, and should. The worst outcome is an *ambiguous* label, which lowers trust without building understanding.

**Calibrated-language formats**
- **IPCC** (Mastrandrea et al. 2010)† uses two scales:
  - confidence, rated from evidence and agreement;
  - likelihood, with set probability ranges ("very likely" means 90–100%).
- Readers interpret IPCC terms *regressively, toward 50%*. Adding numeric ranges improved interpretation in 24 countries (Budescu et al. 2014). [E]
- **GRADE** certainty statements (Santesso et al. 2019) [E]:
  - "X reduces";
  - "X probably …";
  - "X may …";
  - "The evidence is very uncertain …".
- The GRADE statements were refined through workshops and a survey of 91 respondents, with a pre-set acceptance rule. Summary-of-findings tables show certainty with ⊕ symbols.†

**Documenting data**
- **Dataset Nutrition Label** (Holland et al. 2018): standardised modules. [E]
- **Datasheets for Datasets** (Gebru et al.): seven sections, including Uses (what the data should not be used for) and Maintenance (errata, how to contribute). [E]
- **Data Cards** (Pushkarna et al. 2022) [E]:
  - layered questions, from broad yes/no to detailed rationale;
  - written so the least-proficient reader can follow them;
  - unknowns stated explicitly.
- **W3C PROV**† provides `wasAttributedTo`, `wasGeneratedBy` and `SoftwareAgent`. These suit "drafted by an AI agent under a charter; checked by script; not reviewed by a person".

**Attention**
- **NN/g eyetracking (2018)** [E]:
  - people skip boxed, colourful, ad-like content and banners;
  - after dismissing one item they avoid that whole area ("hot potato").
- **Vance et al. 2018**: attention to repeated warnings fell over a week. Warnings that varied in form slowed the decline. [E]
- **GOV.UK** advises using notification banners "sparingly", because people "often miss them", and no more than one. [E]

**Pending, not zero**
- Song & Szafir 2019 [E]:
  - zero-filled values gave the lowest perceived quality and hurt averaging accuracy;
  - omitting values also lowered confidence.
- [J] EMST imputes nothing. The risks are blanks read as "none", "0" read as "not important", and sorts or totals that count pending values.

### Requirements

| ID | Requirement | Priority | Source |
|---|---|---|---|
| U-01 | Disclosure must be layered. (1) Site: a "How EMST was made" page in Data Card form, covering what EMST is, who and what made it, the checks that ran, what has **not** happened, permitted uses and how to contribute. (2) Record: one status line. (3) Value: the evidence drawer. | must | Data Cards; Datasheets; Prajod 2026 |
| U-02 | Record status must be one consistent line, not a stack of coloured boxes, for example: "Drafted by AI · Not yet reviewed by people · Use: explore and describe only". | must | NN/g; Vance; GOV.UK |
| U-03 | The default status should be quiet. Emphasis is reserved for exceptions such as "v1 value, not for decisions", unverified instruments and withheld counts. | should | Vance (variation slows habituation), applied through meaning; J |
| U-04 | "Assessment pending" must show as text, never as a blank, "0", "—" or "N/A", and its accessible name must match. | must | Song & Szafir; gate rule |
| U-05 | Pending values must sort last in both directions and stay out of counts, averages and charts. The exclusion must be stated: "0 of 1,317 assessed". | must | Song & Szafir; J |
| U-06 | Pending labels must say what will change them, without inventing a date: "Shown after a reliability study with practitioners reports. None has reported yet." | must | Kerr 2022; GRADE |
| U-07 | Evidence status should use a small fixed ladder of plain phrases in GRADE style, with the empty top rungs ("Reviewed by practitioners: none yet") visible. | should | GRADE [E]; IPCC† |
| U-08 | Each verbal certainty term must have one fixed definition, shown without hover. | must | Budescu 2014 |
| U-09 | Each record should carry machine-readable PROV in the JSON-LD bundle and on its page. | should | W3C PROV† |
| U-10 | "Not for decisions" must sit next to every v1 value, not only in the drawer heading. | must | brief §3 |

**Patterns.** Data Cards playbook (sites-research.google/datacardsplaybook†); Datasheets questions (arxiv.org/abs/1803.09010); GRADE informative statements; GOV.UK inset text and warning text for caveats that belong to the task in hand.

### Pitfalls
- 40 identical badge pairs on one page.
- "Draft" or "estimated" as the only cue.
- Grey "pending" text that fails contrast.
- Empty chart bars.
- "Confidence 0.6" shown as if it were a probability (§11 CT-4).

---

## 4. AI-generated content disclosure

### Findings

**Research on AI labels**
- **Altay & Gilardi 2024** (*PNAS Nexus*; N = 4,976, US and UK) [E]:
  - an "AI-generated" label lowered perceived accuracy and willingness to share, for true and false headlines and for human-made and AI-made ones;
  - the effect was about a third the size of a "false" label (2.66 against 9.33 points);
  - the cause is an assumed lack of human oversight. The penalty mostly disappeared when the label was defined as "AI helped draft or improve clarity".
  - The authors recommend explaining what labels mean.
- **Prajod et al. 2026** (arXiv 2601.09620; n = 34; indicative only) [E]:
  - one-line disclosure performed about the same as none on trust;
  - detailed disclosure lowered trust but increased source-checking;
  - many participants wanted detail on demand.
- **Valenzuela et al. 2026** (*Digital Journalism*; conjoint study in Chile): a policy of human review of all AI content was the strongest credibility driver. [E: Nieman Lab]

**US policy**
- **OMB M-25-21 and M-25-22** (3 April 2025) [E]:
  - define "high-impact" AI as output that is a principal basis for decisions with significant effects on rights or safety;
  - require minimum practices for high-impact use;
  - require public inventories of AI use cases.
- **OMB M-26-04** (11 December 2025): LLM procurement principles, including model and system cards. It sets no public labelling duty. [E]
- **OPM, "Use of Artificial Intelligence in the Federal Hiring Process"** (27 August 2026) [E]:
  - encourages AI drafting of position descriptions, job analyses and crediting plans, but an official must "independently review and adopt" the drafts;
  - AI-drafted job analyses and competency content need SME involvement and independent validation against "the position's actual duties and documented job-relatedness". Otherwise the use is treated as high-impact;
  - 5 CFR 300.103 still applies.

**EU AI Act** [E]
- Article 50 applies from 2 August 2026.
- Article 50(4): AI-generated text published to inform the public on matters of public interest must be disclosed, unless a person reviewed it and holds editorial responsibility.
- The Code of Practice was published on 10 June 2026 and found adequate on 8–9 July. The Guidelines followed on 20 July 2026.
- The AI Omnibus (Regulation (EU) 2026/1744) left Article 50 unchanged, apart from a 50(2) marking grace period to 2 December 2026 for systems already on the market.
- [J, not legal advice] Applicability to a US taxonomy is uncertain. The human-review exemption cannot apply. Voluntary disclosure already meets the aim.

**Record level or site level?** [J]
- Records travel: in CSV rows, citations, screenshots and imports into HR systems. A site-only label is lost on the way.
- A record-only label invites the "full automation" assumption. For EMST that assumption is correct but incomplete: it misses the person-set charter and the automated checks.
- Use both: a one-line record label that travels with the record, and a site-level explanation of the process.

### Requirements

| ID | Requirement | Priority | Source |
|---|---|---|---|
| AI-01 | The AI-drafting statement must travel with every record: on its page, in CSV and JSON-LD, and in citations. | must | Altay & Gilardi; brief §1 |
| AI-02 | The wording must state the process and the review status: "Drafted by AI agents. Not yet reviewed by people." | must | Altay & Gilardi |
| AI-03 | The site page must say what people did (set the charter), what agents did and which checks ran. It must also state what has **not** happened: no practitioner review, no reliability study and no job analysis. Give the review plan, with dates only if they are real. | must | Valenzuela; Kerr |
| AI-04 | Never use "verified", "validated", "official", "expert-reviewed", "AI-powered" or "smart". | must | ADR-0027 §3; J |
| AI-05 | Federal HR pages should say in OPM's terms that EMST drafts are not job analyses. Any use in a position description, job analysis or crediting plan needs the agency's own SME validation. Link the OPM memo. | should | OPM, Aug 2026 |
| AI-06 | Agent role titles ("Chief Taxonomy Architect") should not appear in default views. Where they must, label them "AI agent role" every time. | should | J |
| AI-07 | Credit must read "EMST project lead", with no personal names. | must | brief §7 |
| AI-08 | Process detail should sit in a "How was this drafted?" `<details>` rather than on every record. | should | Prajod; COGA |

### Pitfalls
- Generic boilerplate such as "may contain errors".
- AI authorship mentioned only in the footer.
- Overclaiming human involvement.
- Treating "AI-drafted" and "unverified" as the same thing. Altay & Gilardi found that readers do not read "AI" as "false".

---

## 5. Indigenous data governance

### Findings

**CARE principles** (GIDA 2019; Carroll et al. 2020) [E]
- Collective benefit, Authority to control, Responsibility and Ethics.
- A1 covers free, prior and informed consent.
- E3 asks metadata to record "provenance, purpose, limitations and consent-related obligations".
- CARE complements FAIR.

**Local Contexts** [E: Local Contexts Notices PDF; Creative Commons and Local Contexts guidance, 2026]
- **Labels** are applied only by Indigenous communities. **Notices** are applied by institutions through the Hub.
- The Notices:
  - **TK and BC** (disclosure): placeholders until a community adds Labels;
  - **Attribution Incomplete** (disclosure);
  - **Open to Collaborate** (engagement): a commitment to "new modes of collaboration, engagement, and partnership";
  - **Collections Care** (2026).
- The 2026 guidance:
  - "as open as possible and as closed as necessary";
  - there are "legitimate reasons not to … allow access";
  - Local Contexts Project IDs go in the Rights field.

**Mukurtu** [E: D-Lib 2017] Access follows community-defined protocols and relationships. EMST has no authorised audience and no content to show, so the matching pattern is no access by design.

**EMST rules** [E: ADR-0007 §C–D]
- Show only the count (163) and the policy statement.
- Indigenous knowledge is out of scope by design.
- The Tribal Advisory Council has binding consent authority.
- Q11 (inviting help to form the Council) is the project lead's question.
- The build fails on trigger terms that appear outside policy statements.

**[J] Notices for EMST**
- TK and BC Notices would wrongly signal that EMST holds Indigenous knowledge or biocultural material.
- "Open to Collaborate" is honest only if the project will act on it, and acting on it is outreach.

### Requirements

| ID | Requirement | Priority | Source |
|---|---|---|---|
| IG-01 | Show only the held count, with its release ID, and the policy statement. No titles, categories, per-domain or per-role breakdowns, placeholder rows or "locked" icons. | must | brief §5; ADR-0007 |
| IG-02 | The statement must say: (a) Indigenous knowledge is out of scope by design; (b) records about obligations to and work with Tribal nations are held until a Council formed by Tribal governments and inter-Tribal organisations consents; (c) EMST will not publish them without that consent. | must | ADR-0007; CARE A1 |
| IG-03 | Wording must not imply that Tribes refused, that the records are coming soon, that insiders can see them, or that EMST "protects" Tribes. Avoid "locked", "restricted", "redacted" and "censored". Prefer "held until Tribal consent". | must | J; test CT-5 |
| IG-04 | Never apply Local Contexts Labels, Indigenous imagery or decorative land acknowledgements. | must | Local Contexts; J |
| IG-05 | Do not apply TK or BC Notices. | should | Local Contexts; J |
| IG-06 | Apply "Open to Collaborate" only if the project lead decides to (Q11). **Decision point.** | could | Local Contexts; ADR-0007 |
| IG-07 | The policy must sit in one consistent place (footer link, "How EMST was made", release notes). A search for "Tribal" must return the policy page. | must | J |
| IG-08 | Whether role pages may say "Tribal employer variants are not shown (see policy)" is a **decision point**. The note would show users that Tribal employers were not overlooked, but it arguably "describes" held content. Default: link to the general policy only. | should | ADR-0007; J |
| IG-09 | Workforce statistics must carry ADR-0007's caveat that the Tribal workforce is under-measured. | should | ADR-0007 |

### Pitfalls
- Per-domain counts.
- Redaction-bar graphics.
- Celebratory or apologetic tone.
- Treating the count as a progress meter.
- Showing draft Tribal content to anyone, including test participants.

---

## 6. Design systems and trust signals

### Findings

**USWDS**
- The principles are: start with real user needs; earn trust; embrace accessibility; promote continuity; listen. They were updated in February 2025. [E]
- "Earn trust" tells sites to "identify your site as a federal government site". [E]
- The banner guidance: "Do NOT use the banner on non-government domains such as a .com or .org", or on test sites. [E]
- USWDS code is public domain†, but its look signals "government" to many US users. [S: settle with CT-0]
- EMST uses USWDS tables, process lists, radios and similar components, with no banner, header or identifier. [E]
- [J] The "Federal Series Profile" pages raise the risk that readers take EMST for an OPM product.

**GOV.UK patterns** [E for tabs, notification banner and feedback; others †]

| Pattern | Fit for EMST |
|---|---|
| Details | value-level "What does this mean?" |
| Summary list | record facts: ID, status, use, changed in release |
| Inset and warning text | caveats inside the content |
| Task list | gap-check progress |
| Step by step (GOV.UK publishing) | for example "Use EMST to plan a course" |
| "Contact a department or service team" | the challenge page |
| Feedback component | rebuilt in 2022 with the HTML `hidden` attribute so it works without JS [E] |

### Requirements

| ID | Requirement | Priority | Source |
|---|---|---|---|
| DS-01 | Never use the USWDS banner or identifier, seals, "official website" or a .gov-like domain. | must | USWDS banner |
| DS-02 | The header must say "An independent open project. Not a government website." | must | USWDS "Earn trust", reversed; J |
| DS-03 | OPM series and state class pages must say early on that EMST is not affiliated with OPM or the state, and that crosswalks are unreviewed AI matches. | must | ADR-0027 §3 |
| DS-04 | USWDS theme tokens (colour, typeface) should move away from the default federal look, while the accessible components stay. | should | J; CT-0 |
| DS-05 | Caveats should appear as inset or warning text, with at most one banner (release status). | should | GOV.UK banner |
| DS-06 | Disclosures should use native `<details>` and `hidden`. | should | GOV.UK; current practice |

### Pitfalls
- "Government-grade" styling used as a trust shortcut.
- OPM codes in hero type.
- Stacked banners.

---

## 7. Open and linked-data UX

### Findings

**CITATION.cff 1.2.0** [E]
- Required keys: `cff-version`, `message`, `title` and `authors`.
- `type: dataset` is supported.
- `authors` may be an **entity**, which fits "no personal names".
- `doi` takes a concept DOI or a version DOI.
- The repository has no `CITATION.cff`. [E] GitHub shows "Cite this repository" when the file exists.†

**DOIs.** A concept DOI plus one DOI per version, through Zenodo or DataCite, is the usual pattern.† It needs an external account, so it is a decision point.

**schema.org.** `DefinedTerm` takes `termCode` and `inDefinedTermSet`. [E] `DefinedTermSet` describes the scheme.†

**Skosmos.** Skosmos 3 was rewritten in Vue with UX and accessibility aims. The 3.0 core was planned for December 2025. [E: NKOS 2025] Its conventions are the hierarchy view, A–Z index, concept page with mappings and per-concept RDF download.† [J] Borrow them as static pages. Running Skosmos itself would need a server.

**IDs.** IDs are "candidate" until 2.0.0, and `delta.json` exists. [E]

**Downloads for non-developers.** [J] Lead with the task, for example "Get one role's tasks as a spreadsheet". Give size, rows, licence and AI status for each file, and offer a starter CSV with a data dictionary.

### Requirements

| ID | Requirement | Priority | Source |
|---|---|---|---|
| LD-01 | Every record must show its ID, the release ID, "candidate ID until 2.0.0" and a copy button. | must | RELEASE_NOTES |
| LD-02 | Add a CITATION.cff with `type: dataset`, an entity author and a message that names AI drafting and the lack of review. | should | CFF 1.2.0 |
| LD-03 | "Cite this" must include the release ID and the AI and review status, in plain text, BibTeX and RIS. | must | brief; Datasheets |
| LD-04 | DOIs through Zenodo or DataCite. **Decision point.** | could | DataCite† |
| LD-05 | Record pages should embed `DefinedTerm` JSON-LD plus PROV status. | should | schema.org; PROV† |
| LD-06 | Release notes should be readable by people (changes, held and withheld counts, known issues). Records should show "changed in this release". | should | Datasheets "Maintenance" |
| LD-07 | The download page must lead with tasks and plain per-file descriptions, and should offer a starter CSV with a dictionary. | must | J; COGA |
| LD-08 | Crosswalk downloads must keep `mapping_justification`, `confidence` and `review_status`, and the page must explain them. | must | ADR-0027; SSSOM [E] |
| LD-09 | Hierarchy and A–Z views could follow Skosmos conventions as static pages. | could | Skosmos† |

### Pitfalls
- Promising persistence before 2.0.0.
- Citations that drop the AI caveat.
- JSON-LD as the most prominent download.
- Crosswalk CSVs that strip the review status.

---

## 8. Low bandwidth, field use and print

### Findings

**Connectivity** [E]
- Pew (June 2026): home broadband is 72% in rural areas, 84% in suburbs and 75% in cities. 16% of adults are smartphone-only.
- GAO-25-107905 (September 2025) cites the Forest Service: "most wildland fires are in areas with limited or no cellular coverage". Satellite links are costly and need line of sight.
- [S] Crews print task lists. Confirm this in field research.

**Performance** [E]
- Core Web Vitals "good" thresholds, at the 75th percentile: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1.
- The median mobile page weighed about 2.16 MB in 2025 (HTTP Archive).

**EMST, measured in `site/_site`** [E]
- Average HTML page: about 33 KB.
- Home page: 4 KB gzip.
- Search: 368 KB raw, 95 KB gzip, because the index is embedded in the page.
- Gap-check competencies: 998 KB raw, 118 KB gzip.
- USWDS CSS: 61 KB gzip.
- The full site: 47 MB.

**Offline trade-off of the service-worker ban** [J]

| Option | Gains | Costs |
|---|---|---|
| Service worker plus cache (forbidden) | offline repeat visits | persistent storage; risk of stale releases; larger security and privacy surface; breaks the "no storage" promise and its tests |
| Print stylesheet (one `@media print` block exists) | paper task lists, nothing stored | must print status, IDs and caveats |
| Per-role PDF and CSV | portable files | caveats must be inside the file |
| Zip of `npm run build:portable` | the whole explorer from disk | about 47 MB; needs a "this copy is release X" notice |

### Requirements

| ID | Requirement | Priority | Source |
|---|---|---|---|
| LB-01 | Every page must meet the Core Web Vitals "good" thresholds on a throttled mid-range phone. | must | CWV |
| LB-02 | Budget: 50 KB gzip for an ordinary page and 150 KB for search and the gap check. Use at most one subset web-font family. | should | measured; J |
| LB-03 | The search index should be slimmed (titles, IDs and synonyms) to under 60 KB gzip. | should | measured 95 KB |
| LB-04 | Printed task lists must include the AI status line, the use statement, release and record IDs, the print date and the "Assessment pending" text, with no colour-only meaning. | must | brief; SC 1.4.1 |
| LB-05 | The download page should offer the portable site as a zip, with release ID, size and "check for newer". | should | `build:portable`; J |
| LB-06 | Pages must work without JS. Search and the gap check must say they need JS and offer alternatives (true today). | must | current practice |

### Pitfalls
- An analytics script or remote font added "just for the pilot".
- Printouts without caveats that then circulate as "the official list".
- Wide tables that are unusable on a phone.

---

## 9. Learning whether the site works, without analytics

### Findings

**Plausible** [E]
- Uses no cookies, and counts visitors with a daily-salted hash of IP address and user agent.
- Still records page, referrer, browser, operating system, approximate location and engagement events.
- Needs a script that sends requests. That breaks `connect-src 'none'` and the "no runtime requests" promise.

**GOV.UK "Is this page useful?"**
- It posts to a backend, and its no-JS fallback asks for an email address. [E]
- EMST forbids forms (`form-action 'none'`) and email addresses on its pages, so only a link to a GitHub issue form fits. [J]

**Methods compared** [J]

| Method | What it teaches | Privacy cost | Fit |
|---|---|---|---|
| None (status quo) | nothing | none | full; absence of evidence is not evidence of no use |
| Moderated research (§11) | *why* things fail; comprehension | consented, off-site | full; highest value |
| GitHub issue forms and reactions | errors and disputes | public, tied to an account | full; skewed to GitHub users |
| Opt-in survey hosted elsewhere | satisfaction, tasks | the host's terms | link only; self-selected |
| GitHub release download counts | downloads per file | none to EMST | full†; files on Releases only |
| Host aggregate logs | page counts, 404s | IP addresses at the host | must be disclosed |
| Plausible-style script | trends | low, but not zero | **breaks the CSP** |
| Pilot partner reports (U1) | use in context | reported through the partner | full; needs a template |

### Requirements

| ID | Requirement | Priority | Source |
|---|---|---|---|
| PF-01 | Keep the no-analytics, no-storage, no-request design. Learn through planned research, issue forms and download counts. | must | brief §6 |
| PF-02 | Each page should end with "Was this page useful? Tell us on GitHub", a link to an issue form, noting that GitHub needs an account. | should | GOV.UK, adapted |
| PF-03 | If the host keeps logs, the privacy page must say what is kept and for how long, and that only daily aggregates are used. | must | J |
| PF-04 | Run §11 research before any release that changes notices. | should | J |
| PF-05 | Run a link-out opt-in survey during the pilot. **Decision point.** | could | J |

---

## 10. Participation: suggest a correction, challenge a value

### Findings

**Wikidata** [E: Help:Ranking, archived]
- Values that were sourced but turned out wrong are kept with **deprecated rank** and a "reason for deprecated rank" (P2241).
- This stops the same error being re-entered and records how knowledge changed.
- [J] EMST could keep a visible challenge log in the same spirit.

**OpenStreetMap** [E: OSM talk list, August 2019; community forum, December 2023]
- Anyone can still create a note without an account.
- Anonymous comments and closing were disabled in August 2019 because of spam.
- Anonymous intake is valuable but needs moderation. [J]

**GitHub issue forms** [E]
- Field types: `input`, `textarea`, `dropdown`, `checkboxes` and `markdown`. Fields can be made required, and labels added automatically.
- A URL can pre-fill `title`, `body`, `labels` or `template`. A labels parameter returns a 404 unless the user has triage permission.
- **The explorer's build forbids query strings on external links** [E]. Pre-filling the record ID through the URL would break that rule. **Decision point.** Either:
  - keep the rule, and show the ID with a copy button so the form asks for it; or
  - allow `?template=` links.

**Barriers without a GitHub account** [J; S where marked]
- Creating an account.
- Posts are public, and agency staff may be barred from posting.
- An interface built for developers.
- English only.
- Workplace network blocks [S: ask U3–U5].
- Two-factor sign-in burden [S: check GitHub's current 2FA scope].
- The site forbids forms and email addresses, so a no-account route would have to be a form on a third-party service. **Decision point.**

### Requirements

| ID | Requirement | Priority | Source |
|---|---|---|---|
| P-01 | Add issue forms for: correct a record; challenge a crosswalk; accessibility barrier; question about use. Each needs a required record-ID field and a "no personal data" note. | should | GitHub forms |
| P-02 | Every record and crosswalk row must have a "Challenge this" link to the challenge page, with the ID shown for copying. | must | brief §7; SC 3.3.7 |
| P-03 | The challenge page must say that an account is required, that posts are public, and that agency staff should check their agency's policy. | must | current page [E] |
| P-04 | Accepted and rejected challenges should be listed in release notes. A record could show "n open challenges", computed when the site is built. | could | Wikidata; J |
| P-05 | A no-account route (third-party form or research sessions). **Decision point.** If there is none, the site must say so. | should | OSM; J |
| P-06 | Reporting an accessibility barrier should not require GitHub. **Decision point.** | should | J |

---

## 11. Comprehension tests to run with real people

### Approach

**Stage A: formative**
- Moderated think-aloud sessions, followed by probes.
- 5–8 people in each of three segments:
  - learners and job seekers (U2, U8);
  - supervisors, training and HR staff (U3–U6);
  - data users (U7).
- Iterate until a round of 8 shows no critical confusion.
- Basis:
  - NN/g: about 5 users is enough for qualitative work, and about 40 for most quantitative studies [E].
  - With 8 users, a problem that affects 20% of people shows up at least once with probability 0.83 [computed].

**Stage B: summative**
- Follow the FDA label-comprehension guidance [E]:
  - set a target for each notice in advance;
  - a notice passes if the **lower bound of the two-sided 95% confidence interval exceeds the target**;
  - include low-literacy participants in proportion to the population;
  - ask open questions before closed ones;
  - offer "I don't know";
  - avoid leading questions;
  - use scenario questions.
- Critical confusions follow ANSI Z535.3 (85% correct, fewer than 5% critical confusions) [E: CPSC 2019; IIID 1991].

**Sample size** [computed, Clopper–Pearson]
- With **n = 80**, a notice passes with **at least 72 of 80 correct** (lower bound above 0.80) and **no more than 2 of 80 critical misreadings** (upper bound below 0.10).
- If the true correct rate is 92%, n = 70–80 gives about 80% power.
- About **28% of participants should be at or below PIAAC Level 1**, identified with a validated screener.
- Add **n = 20–30 HR or classification staff** (U5) and treat their results as directional. At n = 30, even 28 correct only shows a lower bound above 0.75.

**Ethics** [J]
- Get consent. Collect no data on the EMST site, and run tests on prototype copies.
- Recruitment needs the project lead's approval, because the brief bars contacting anyone without it.
- **Do not recruit Tribal participants for CT-5 until the project lead decides how ADR-0007 applies.**
- Never show draft Tribal content to anyone.

**Each test** starts with an open question, "What does this tell you?", on real EMST screens.

### Tests

**CT-0: Who runs this site?** (5-second test, then probes)
- **Questions:**
  - "Who runs this website?"
  - "Is it a government site?"
  - "Who wrote the task lists?"
- **Pass:** at least 72 of 80 answer "not government" or "an independent project".
- **Critical misreadings:** "OPM", "a federal agency" or "experts wrote it".

**CT-1: "Drafted by AI, not yet reviewed by people"**
- **Questions:**
  1. "Who wrote this task list?"
  2. "Has anyone who does this job checked it? How do you know?"
  3. Scenario: "Your supervisor wants these tasks pasted into a position description today. What do you do?"
  4. "What must happen before you could rely on it?"
- **Pass:** at least 72 of 80 say "AI-drafted, not reviewed by people".
- **Critical misreadings:**
  - "reviewed by experts or the government";
  - "AI means it is false".
- **Diagnostic:** run a variant without the site-level explanation, to measure the "full automation" assumption.

**CT-2: "Assessment pending"**
- **Screen:** a task table sorted by an importance column showing "Assessment pending", with the line "0 of 42 assessed".
- **Questions:**
  1. "Which task is most important?" Correct: the page doesn't say yet.
  2. "What does 'Assessment pending' mean?"
  3. "Why is this task first?"
  4. "When will this change?" Correct: after a study; no date has been set.
- **Pass:** at least 72 of 80 correct on questions 1 and 2.
- **Critical misreadings:**
  - pending read as zero, low or "not important";
  - importance inferred from row order;
  - a believed date.
- **Diagnostic:** repeat the questions on a chart version.

**CT-3: What you can use this for (use tiers)**
- **Format:** scenarios, each answered Yes, No, Not yet or Don't know, followed by "why?".
- **Scenarios** (correct answer in brackets):
  - (a) Explore what a prescribed-fire course might cover. [Yes]
  - (b) Describe skill areas in a regional workforce plan. [Yes, with limits]
  - (c) Write a crew member's individual development plan. [Not yet: no record reaches *develop*]
  - (d) Screen or rank applicants. [No]
  - (e) Choose positions to cut in a reduction in force. [No]
  - (f) Rate an employee's performance. [No]
  - (g) Start an agency job analysis. [Only as input to the agency's own analysis with SMEs; nothing reaches *select* yet]
- **Pass:** at least 72 of 80 correct on each of (a)–(c).
- **Critical misreadings:** "Yes" to (d), (e) or (f). Each needs no more than 2 of 80. In the U5 sample, report every "Yes".
- **Diagnostic:** do empty *develop* and *select* rungs read as "coming soon"?

**CT-4: Crosswalk match strength**
- **Screen:** an EMST competency with rows marked "close match (similar, not the same)", "broader", "narrower" and "related", each labelled "AI match, not reviewed". One variant adds "agent confidence 0.6".
- **Questions:**
  1. "Is the EMST item the same as the O\*NET or ESCO item?" Correct: no.
  2. "Which link is strongest?"
  3. "Has a person checked these links?"
  4. "Could you tell a funder your course is 'aligned with O\*NET'?" Correct: no.
  5. (variant only) "What does 0.6 mean?"
- **Pass:** at least 72 of 80 correct on questions 1, 3 and 4.
- **Critical misreadings:**
  - "the same" or "equivalent";
  - "aligned" or "approved";
  - "60% chance it's right". If more than 2 of 80 give this answer, **hide the number in default views**. Budescu's evidence that numbers help applies to calibrated terms, and this number is not calibrated.

**CT-5: Tribal hold notice**
- **Screen:** the policy statement and count, shown at the footer-link destination and as a search result for "Tribal".
- **Questions:**
  1. "What is this telling you?"
  2. "Why aren't these records shown?" Correct: they are waiting for consent from a council formed by Tribal governments, and EMST won't publish them without it.
  3. "Does EMST describe Indigenous knowledge?" Correct: no, it is out of scope by design.
  4. "Can anyone see the records now?" Correct: no.
  5. "How does the notice come across?" Ask for a tone rating and a comment.
- **Pass:** at least 72 of 80 correct on questions 2–4.
- **Critical misreadings:**
  - "Tribes refused" or "are hiding something";
  - "EMST deleted Tribal work";
  - "insiders can see them";
  - "coming on a date".
- **Tone:** report descriptively only. Once a Tribal Advisory Council exists, its members, not this team, should set the tone criteria.

### Reporting
- For each test, report the number correct with its 95% confidence interval, the critical-misreading counts and anonymised verbatim misreadings.
- Break results down by literacy band and segment.
- If a notice fails, reword it, run it through Stage A again, then repeat Stage B.

---

## Decision points for the project lead

1. Whether to apply a Local Contexts "Open to Collaborate" Notice (IG-06, linked to Q11).
2. Whether role pages may point to the Tribal hold (IG-08).
3. Whether to mint DOIs through Zenodo or DataCite (LD-04).
4. Whether to allow `?template=` query strings on GitHub links (§10).
5. Whether to offer a no-account feedback or barrier-reporting route (P-05, P-06).
6. Whether to run a link-out opt-in survey during the pilot (PF-05).
7. Whether to approve recruitment for §11, and how CT-5 fits ADR-0007.

---

## Sources

Every source below was read today except those marked †. Repository files were read only.

**Repository**
- `site/README.md`
- `site/src/_includes/layouts/base.njk`
- `site/src/_includes/macros.njk`
- `site/src/challenge/index.njk`
- `site/src/download/index.njk`
- `site/src/search/index.njk`
- `site/src/about/accessibility.njk`
- `site/lib/model.mjs`
- `dist/2.0.0-rc.1/RELEASE_NOTES.md`
- `dist/2.0.0-rc.1/sssom/esco/1.2.0.sssom.tsv`
- `docs/decisions/ADR-0007-sector-actors-and-tribal-boundary.md`
- Sizes measured in `site/_site`

**§1 Accessibility and law**
- https://www.federalregister.gov/documents/2026/04/20/2026-07663/extension-of-compliance-dates-for-nondiscrimination-on-the-basis-of-disability-accessibility-of-web
- https://section508.gov/develop/applicability-conformance
- https://www.w3.org/WAI/
- https://dequeuniversity.com/resources/wcag-2.2
- https://www.w3.org/TR/coga-usable
- https://design-system.service.gov.uk/components/tabs/
- https://design-patterns.service.justice.gov.uk/components/sortable-table
- https://github.com/alphagov/accessible-autocomplete/issues/430
- † https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
- † https://www.w3.org/WAI/ARIA/apg/patterns/table/examples/sortable-table/
- † https://designsystem.digital.gov/components/table/

**§2 Plain language**
- https://ies.ed.gov/learn/press-release/u-s-adults-score-par-international-average-literacy-skills-below-international-average-numeracy-and
- https://centerforplainlanguage.org/the-federal-plain-language-guidelines-are-missing/
- https://www.surreycc.gov.uk/website/writing-guide/reading-levels-for-web-pages
- https://www.hhs.gov/guidance/sites/default/files/hhs-guidance-documents/FDA/Label-Comprehension-Studies-for-Nonprescription-Drug-Products.pdf

**§3 Uncertainty and provenance**
- https://core.ac.uk/download/305110478.pdf
- Schneider et al. 2022: https://core-prod.cambridgecore.org/core/services/aop-cambridge-core/content/view/721727C5DA7F0438804568657808D951/S1930297500008962a.pdf/effects_of_communicating_scientific_uncertainty_on_trust_and_decision_making_in_a_public_health_context.pdf
- https://www.repository.cam.ac.uk/items/97ce1489-e3fc-43f8-97f8-44b1c815e95d
- https://ideas.repec.org/a/nat/natcli/v4y2014i6d10.1038_nclimate2194.html
- https://link.springer.com/article/10.1007/s10584-022-03382-3
- https://archive.lstmed.ac.uk/13286/1/GRADE%20narrative%20statements%20pre%20proof%20plus%20appendices%2020191208.pdf
- https://experts.mcmaster.ca/display/publication3587715
- https://arxiv.org/abs/1805.03677v1
- https://huggingface.co/papers/1803.09010.md
- https://arxiv.org/pdf/2204.01075.pdf
- https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/
- https://misq.org/tuning-out-security-warnings-a-longitudinal-examination-of-habituation-through-fmri-eye-tracking-and-field-experiments.html
- https://design-system.service.gov.uk/components/notification-banner
- https://par.nsf.gov/servlets/purl/10111567
- † https://www.ipcc.ch/site/assets/uploads/2018/05/uncertainty-guidance-note.pdf
- † https://www.w3.org/TR/prov-overview/

**§4 AI disclosure**
- https://academic.oup.com/pnasnexus/article/3/10/pgae403/7795946
- https://arxiv.org/pdf/2601.09620
- https://www.niemanlab.org/?p=250977
- https://www.hunton.com/privacy-and-cybersecurity-law-blog/omb-issues-revised-policies-on-ai-use-and-procurement-by-federal-agencies
- https://www.fiddler.ai/blog/omb-m-26-04
- https://www.opm.gov/chcoc/latest-memos/use-of-artificial-intelligence-in-the-federal-hiring-process.pdf
- https://federalnewsnetwork.com/artificial-intelligence/2026/08/opm-calls-for-wider-ai-adoption-in-federal-hiring-process/
- https://www.legalithm.com/en/blog/eu-ai-act-what-applies-2-august-2026
- https://www.reedsmith.com/our-insights/blogs/viewpoints/102nbz0/transparency-obligations-for-ai-generated-content-the-code-of-practice-adequacy/

**§5 Indigenous data governance**
- https://www.imperial.ac.uk/research-and-innovation/support-for-staff/scholarly-communication/research-data-management/care-data-principles/
- https://localcontexts.org/wp-content/uploads/2023/04/Local-Contexts-Notices.pdf
- https://creativecommons.org/wp-content/uploads/2026/09/Guidance-for-Indigenous-Collections-and-Data_English_Final.pdf
- https://dlib.org/dlib/may17/christen/05christen.html

**§6 and §9–10 Design systems, learning and participation**
- https://designsystem.digital.gov/components/banner/
- https://designsystem.digital.gov/design-principles/
- https://insidegovuk.blog.gov.uk/2022/03/28/making-the-gov-uk-feedback-component-more-accessible
- https://plausible.io/data-policy
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
- https://docs.github.com/en/enterprise-server@3.20/issues/tracking-your-work-with-issues/using-issues/creating-an-issue
- https://lists.openstreetmap.org/pipermail/talk/2019-August/083213.html
- https://community.openstreetmap.org/t/we-dont-need-anonymous-notes/105335?page=4
- https://webcf.waybackmachine.org/web/20220322134249/https://www.wikidata.org/wiki/Special:MyLanguage/Help:Ranking

**§7 Linked data**
- https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md
- https://www.schema.org/termCode
- https://nkos.dublincore.org/2025NKOSworkshop/NKOS%20Skosmos%20and%20Annif.pdf

**§8 Connectivity and performance**
- https://www.pewresearch.org/Internet/fact-sheet/Internet-broadband/
- https://www.pewresearch.org/chart/home-broadband-use-by-community-type/
- https://www.gao.gov/assets/890/881915.pdf
- https://corewebvitals.io/core-web-vitals
- https://almanac.httparchive.org/nl/2025/page-weight

**§11 Testing**
- https://www.nngroup.com/videos/test-5-users-qual-vs-quant/
- https://www.Cpsc.Gov/s3fs-public/CPSC%20Gather%20Consumer%20Feedback%20-%20Final%20Report%20with%20CPSC%20Staff%20Statement%20-%20REDACTED%20and%20CLEARED.pdf
- https://www.iiid.net/wp-content/uploads/Symbol-Comprehension-Testing-Protocol.pdf
