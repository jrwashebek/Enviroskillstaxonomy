# Stage 1b — Federal and State Design-Partner Packages (outline and contents lists)

- **Work package:** WP-13 · **Author:** A10b (AS) · **Date:** 2026-10-23 · **Licence:** CC BY 4.0 (this outline); package data files CC0 1.0
- **Builds:** ADR-0014 (rollout; **provisional-pending-verification**), ADR-0006 (roles; series crosswalk statuses provisional on OPM's proposed consolidation), ADR-0017 (authority position, sign-off), ADR-0022 (X2, X4, X5, X9), ADR-0024 (use tiers; first job-analysis clusters), ADR-0027 (kits first; claims hygiene), ADR-0012 (no personal data), ADR-0016 (naming; computed applicability), ADR-0007 (Tribal variants held); `PHASE4_BUILD_PLAN.md` WP-08, WP-09, WP-11, WP-12.
- **What this document is:** the package structure, the contents list and the acceptance checks. **The content is filled by WP-08 (role profiles and generated HR views, A7 FH with SL and PS), WP-09 (crosswalks, A2 IA with FH and SL) and WP-11 (validation kit, A8 IO)**; WP-12 supplies accessible formats and the security packet; WP-15 verifies every date-sensitive statement before any package leaves the repository.

> **Stage 1b is approved.** The project lead accepted Q5 on 2026-10-23 (`docs/decisions/PROJECT_LEAD_DECISIONS.md`): Stage 1a (the NGO pilot) and Stage 1b (this federal and state design-partner track) run **in parallel from 2027**, and Stage 1b **co-produces artifacts** with partner agencies. Nothing is used in selection before selection-grade evidence exists for that function cluster (ADR-0024). These packages are offered to prospective design partners for co-production as soon as each package's content passes its acceptance checks and WP-15. <!-- DECIDED Q5 (2026-10-23, PROJECT_LEAD_DECISIONS.md): parallel tracks accepted; Stage 1b co-produces artifacts from 2027 -->

> **No agency named here has committed.** USFS, DOI/USWFS, OPM, Pennsylvania and the other agencies below are **prospective** design partners. Each becomes a design partner only when a signed letter is in the commitment register (charter Art. 12). <!-- PENDING Q3: signatory for EMST letters is the project lead by default. -->

---

## 0. Facts every package must state correctly (verified 2026-10-23)

| Topic | Correct statement | Source |
|---|---|---|
| OPM series consolidation | OPM's Apr 24 2026 CHCO memo issued a **proposed** Phase One list of 115 series for realignment (incl. 0410/0437/0480/0487 → 0401; 0455 → 0404); agency feedback was due May 11 2026; **no final-decision memo had appeared by Oct 23 2026**. Packages say "proposed for realignment", never "realigned". | [E: V1-10] |
| Competency-based standards | OPM issued competency-based classification and qualification standards for 2210 on Apr 13 2026 under the Federal Workforce Competency Initiative (FWCI); OPM targets 300+ series by end of FY2026 and 600+ by end of FY2027. EMST **feeds** FWCI and does not compete with it. | [E: V1-11; P-FH-03] |
| Technical assessments | Natural Resources Management is **Tier 2** for Chance to Compete technical assessments **with no Tier 2 date**; FY2028 is the governmentwide full-implementation target. From Sep 30 2025 self-assessment questionnaires may not rate and rank (with exceptions); in FY2025, 91.23% of delegated-examining announcements relied solely on self-report questionnaires. | [E: V1-17, V1-09] |
| Selection defensibility framing | Selection-grade validation is framed by the SIOP Principles, the AERA/APA/NCME Standards, job-relatedness under the Chance to Compete Act and Title VII disparate-impact defensibility — **never "UGESP compliance"** (DOJ opinion Jun 9 2026; OPM interim final rule Jul 31 2026 removing UGESP references; OFCCP rescission of 41 CFR 60-3 effective Oct 26 2026). | [E: V4; ADR-0024 rationale] |
| AI-drafted PD language | OPM's Aug 27 2026 memo treats AI-assisted drafting of PDs as generally **not** high-impact when the responsible official independently reviews, revises and adopts the draft; rating, ranking and scoring are presumed high-impact. | [E: V1-13] |
| Executive Core Qualifications | The five-ECQ framework (Oct 1 2025) no longer contains Political Savvy, Partnering or Influencing/Negotiating; no package cites the ECQs as the warrant for statecraft content. | [E: V2 SC-058; ADR-0027 §3] |
| Pennsylvania | Pennsylvania counts federal experience as equivalent (EO 2025-01), writes federal titles into minimum-qualification text, matched titles with generative AI, and reports 1,350 hires with federal experience by Aug 2026. | [E: SL-031, SL-080] |
| Fire qualifications | USWFS–USFS aligned federal qualification standards take effect Jan 2027; NWCG is not a party; NWCG updated PMS 310-1 on Jan 23 2026. | [E: V3-13] |
| Accessibility | Packages meet WCAG 2.2 AA (a superset of Section 508's WCAG 2.0 AA and the WCAG 2.1 AA required by ADA Title II, whose compliance dates are Apr 26 2027 / Apr 26 2028). | [E: V2-11, V2-12] |

## 1. Elements common to every package

| # | Element | Content | Supplied by |
|---|---|---|---|
| C1 | **Cover sheet** | package name and version; EMST release ID and DOI pinned; **use tier** on its face (`describe` or `develop`; never `select` in v2.0); evidence labels explained; date of the facts table | WP-13 template; WP-16 release IDs |
| C2 | **Guardrail notice** | "Not a classification basis. Not a job analysis. Not for RIF, adverse action or performance ratings. Not a selection instrument; any selection use requires the agency's own job analysis." Redesigned PD language labelled "subject to classification review" (P-FH-09, P-FH-10; ADR-0012 I-2) | WP-08 generator |
| C3 | **Status of every external dependency** | OPM series status (`active | proposed-realignment | realigned-to | cancelled`) with `asOf`; crosswalk set versions and review level (navigation / analytics / selection thresholds, ADR-0022 §4) | WP-09 |
| C4 | **"Does this affect me?" change notice** and machine-readable delta for each package update | | WP-16 |
| C5 | **Accessible formats** | tagged PDF and DOCX for narrative; CSV + Frictionless datapackage for data; WCAG 2.2 AA conformance statement | WP-12 |
| C6 | **Security and privacy packet** | applicability statement (no personal data collected; no hosted service; local-first), SBOM and signed artifacts for data and tools; PTA starter for agencies rehosting on .gov | WP-12 |
| C7 | **No personal data** | packages contain no person-level data; examples are synthetic and labelled; aggregate data returned by partners carry n ≥ 5 | all |
| C8 | **Held content** | Tribal role variants and Tribal-related competencies are excluded (held under ADR-0007); the package says so in one sentence | WP-08; G-TN review |
| C9 | **Computed applicability** | items whose only basis is a rescinded or inactive federal instrument are shown with computed `federalApplicability` and an explanatory note <!-- PENDING Q4: exclusion from federal default views once confirmed --> | WP-08, WP-10 |
| C10 | **Feedback route** | how the partner files errata, crosswalk corrections and change requests (`CONTRIBUTING.md`); named EMST contact role | WP-13 |
| C11 | **Commitment record** | the letter of intent (Annex) and its register entry, with year-five owner | WP-13 |

---

## 2. Package A — the 0400 Kit (0401 and 0404 first)

**Purpose.** Give a federal classification office and OPM's FWCI team copy-ready, function-based competency models and PD language for **0401 General Natural Resources Management and Biological Sciences** and **0404 Biological Science Technician** — the two destination series in OPM's *proposed* Phase One realignment — with a task-level crosswalk showing that duties from series proposed for realignment are preserved. Second wave: 0460 Forestry, 0408 Ecology, 0486 Wildlife Biology, 0028 Environmental Protection Specialist (ADR-0014 §1; P-AS-02).

**Prospective users.** One agency classification office (USFS or a DOI bureau) drafting three to five PDs through normal classification review; OPM Workforce Policy and Innovation reviewing the kit as an input to FWCI technical frameworks for the 0400 group. Collective-bargaining notice for PD changes is anticipated; AFGE, NFFE, NTEU and PEER are briefed on non-punitive use before use (ADR-0014 consequences).

**Role coverage** (from `mvp_role_set.csv`; federal variants only; Tribal variants held):

| Series | EMST role profiles whose federal variants map to the series (crosswalk statuses from WP-09 X4) |
|---|---|
| 0401 | R04 geospatial and remote sensing analyst · R05 ground-truth and validation steward · R07 fuels and prescribed fire specialist · R08 fire intelligence analyst · R09 restoration project lead · R10 environmental review specialist · R13 resource programme manager · R15 wildlife biologist and R16 fisheries biologist (0486/0482 proposed → 0401) · R20 ecologist (0408/0410 proposed → 0401) · R34 stewardship agreement manager and R35 knowledge continuity lead (emerging; exploratory only) |
| 0404 | R02 field resource technician (0455 proposed → 0404) · R03 monitoring and data technician · R05 · R16 · R18 rangeland technician variant (0455 proposed → 0404) · R01 corps member as feeder (non-federal) |

**Contents list.**

| ID | Component | What it contains | Built by | Record types / format | Acceptance check |
|---|---|---|---|---|---|
| A1 | **Federal Series Profile — 0401** (generated) | role variants mapped to the series by indicative grade band; task bundles with importance and time share; critical and needed-at-entry flags; 6–12 critical competencies with target levels by role level; anchored indicators at each level in span; credential gates; sign-off authority; change view (tier-labelled; "assessment pending" where no v2 multi-rater assessment exists) | WP-08 generator over WP-03–WP-07 records | generated view; PDF/DOCX + CSV | carries C2 disclaimer; every number traces to a stored record; no computed field typed |
| A2 | **Federal Series Profile — 0404** (generated) | as A1, with formation tasks flagged for every entry-level variant and by-hand quotas where AI compresses learning tasks | WP-08; WP-07 formation rules | as A1 | formation tasks flagged (COR-1 acceptance in WP-03) |
| A3 | **Competency model by series** | competencies at five levels with observable indicators, named by function; crosswalk to FWCI general and technical competencies where OPM has published them | WP-08; WP-09 X9 | CSV skills-library import + narrative | lint-clean; X9 rows reviewed; no ECQ legacy names |
| A4 | **PD language library** | duty statements by grade band in FES factor order, drafted from task bundles, for duties absorbed from series proposed for realignment (e.g. former 0480 fish and wildlife administration work, 0455 range technician work); each statement labelled "subject to classification review" | WP-08 (FH); classifier review | DOCX + CSV with task IDs | FH classifier review recorded; AI-assistance disclosed per OPM's Aug 27 2026 memo pattern |
| A5 | **Task-level crosswalk: series proposed for realignment → destination series** | for 0410, 0437, 0480, 0487 → 0401 and 0455 → 0404: each source-series duty mapped to EMST tasks and to the destination series' role variants, with match type and `NoTermFound` where duties do not carry over | WP-09 (X4 + task links) | SSSOM + flattened CSV | validates as SSSOM 1.0; status `proposed-realignment` on every source series; never "realigned" |
| A6 | **Series register extract** | the dated OPM series register rows for the kit's series: status, `asOf`, successor series if any, qualification-standard version, positive-education flag | WP-08 / WP-09 X4 | CSV | re-checked quarterly until OPM finalizes Phase One |
| A7 | **O*NET and SOC context** | X3 role variant → O*NET-SOC 2019 and X2 task → O*NET task IDs for the kit's roles, so agencies can join external data | WP-09 | SSSOM + CSV | reviewed-subset level; no alignment claim beyond the reviewed set |
| A8 | **OPM-ready change log** | what changed between kit versions and why | WP-16 | Markdown + delta | generated from change records |
| A9 | **"How to cite EMST in a PD" one-pager** and two-hour train-the-trainer outline | | WP-13 | PDF | WCAG 2.2 AA |

**Out of scope for v2.0:** selection-grade content, USA Hire or SME-QA items for operational use (those come from Package B evidence), Tribal variants, and any statement that OPM has adopted, reviewed or endorsed the kit.

**Sequencing.** Kit draft targeted for Q1 2027 alongside rc.1; if Phase 4 slips, the NGO pilot start holds and the 0400 Kit slips, not the reverse (ADR-0014 consequences). Second-wave series follow the same contents list.

---

## 3. Package B — Job-Analysis Starter Pack (one Tier 2 natural-resources series)

**Purpose.** Let one agency talent team run a job analysis for one natural-resources series (0401 or 0404; federal variants of R09 and R13, ADR-0024 §9 cluster 5) on **3–5 vacancies**, producing documentation the agency owns and returning **de-identified aggregate** SME ratings to EMST under a data-use agreement. This is EMST's first defensible validation evidence (P-AS-03, P-FH-06).

**Why now, honestly stated.** Natural Resources Management is Tier 2 with no Tier 2 date [E: V1-17]; agencies nevertheless need position-specific, job-analysis-based technical assessments by the FY2028 governmentwide target, and only about 15% of agencies employ I-O psychologists [E: FH-017 via ADR-0014]. The pack reduces the cost of doing it well; it does not substitute for the agency's own job analysis.

**Contents list.**

| ID | Component | What it contains | Built by | Acceptance check |
|---|---|---|---|---|
| B1 | **Task inventory** | the series' EMST tasks (15–40 per P1 role), written to job-analysis standard, with sector-actor variant notes removed for the federal context | WP-08 (FH) from WP-03–WP-05 records | every task links ≥ 1 competency; ≤ 60 words; lint-clean |
| B2 | **Matrix-sampled SME survey instrument** | ≤ ~80 tasks per respondent; importance, frequency, consequence of error, needed at entry, AI mode (ADR-0024 §8); demographic items **excluded** from the EMST-returned data | WP-11 (IO) | pre-registration fields stated; sample and stop rules; PRA status noted for any non-federal respondents |
| B3 | **Competency–task linkage sheet** | competencies are job-related only via linkage to ≥ 1 critical task | WP-11 | linkage rule encoded |
| B4 | **Proficiency anchors** | indicators at each level in span, with observability ratings (OBS-4) | WP-07, WP-11 | OBS-4 ≥ 2 for develop use |
| B5 | **SME-QA benchmark drafts by grade band** | draft benchmarks for the agency's SMEs to revise | WP-08 (FH) | labelled draft; agency adopts |
| B6 | **Structured-interview question bank and one work-sample prompt** | drafts tied to critical tasks | WP-11 with FH | labelled draft; multi-method, never a single high-impact hurdle |
| B7 | **Documentation templates** | validation documentation framed by the SIOP Principles, the AERA/APA/NCME Standards, job-relatedness under the Chance to Compete Act and Title VII defensibility; adverse-impact plan template; job-analysis record aligned with OPM's job-analysis rule as amended Jul 31 2026 | WP-11 | contains no "UGESP compliance" language |
| B8 | **Data-use agreement template** | aggregate-only return of ratings (n ≥ 5 per cell), pseudonymous rater IDs held by the agency or a research partner, no applicant data, no identity map in EMST | WP-13 (from `pilot_mou_template.md` Schedule B) | conforms to ADR-0012 I-1 §3 |
| B9 | **Measurement plan** | SME hours, time-to-hire against the agency's target, reliability of ratings (α with CI), and what EMST learns for its validation status | WP-11; CM | metrics defined before use |

**What EMST receives:** aggregate task ratings and linkage results by series and grade band, rater-agreement statistics, and the agency's permission to cite them as job-analysis evidence for that series (`validationStatus = job-analysis-confirmed` for the specific job family only, ADR-0024 §3). **What EMST never receives:** applicant data, rater identities, individual ratings.

---

## 4. Package C — Federal-to-State Environmental Crosswalk, validated with Pennsylvania

**Purpose.** Route released federal environmental staff to state environmental vacancies by mapping federal series and EMST federal role variants to Pennsylvania state classes, validated by Pennsylvania classification staff, using Pennsylvania's own federal-equivalency work as the gold set (P-SL-08). It is a **fast-track** artifact: translation and crediting need no prediction, so it may ship before any pathway recommendation (ADR-0014 §5).

**Prospective users.** Pennsylvania's central HR and environmental agency HR; displaced federal staff and their counsellors; later Texas and Washington (three contrasting state models) plus one county environmental health department and one municipal utility (ADR-0014 §1; P-SL-09).

**Contents list.**

| ID | Component | What it contains | Built by | Acceptance check |
|---|---|---|---|---|
| C-1 | **X5 Pennsylvania class records** | the state classes in scope (environmental protection, environmental engineering, natural resources, oil and gas, compliance and related classes) in SL's minimal common fields (16 MUST of 28), dated, class-level with position overrides only where flagged | WP-09 (SL co-owner) | MUST fields present; `asOf` set; re-run each 1 July or on plan revision |
| C-2 | **Mapping set: federal series and EMST federal variants → PA classes** | SSSOM 1.0 with SKOS predicates, `NoTermFound` with reasons, justification, weakest match type, author and reviewer IDs | WP-09 | validates; every row human-reviewed by a PA classification analyst before any selection-context use (two reviewers, ≥ closeMatch) |
| C-3 | **Gold-set comparison** | agreement between the EMST-derived mapping and Pennsylvania's published federal-title equivalencies; disagreements listed | WP-09 (IA) with CM | κ and coverage reported; confidence published (Pennsylvania's GenAI matching did not publish confidence [E: SL-027]) |
| C-4 | **Friction records** for each mapped pair | qualification gate, residency (e.g. PA DEP in-state residency [E: SL-084]), pay mapping and direction, list or status gates, licence and certification reciprocity, hiring time | WP-08 (SL, CM) | `FrictionRecord` fields complete for pre-registered pathways (M-02) |
| C-5 | **State Class View** (generated) for each mapped class | EMST tasks and competencies behind the class; federal origin variants; gaps | WP-08 generator | carries C2 disclaimer |
| C-6 | **Translation view for movers** | "your federal role → Pennsylvania classes you may qualify for, and what to show" — directional coverage, frictions, no recommendation | WP-12 | labelled exploratory where pathway scoring is used |
| C-7 | **Flattened CSV for HR users** | | WP-09 | |
| C-8 | **Validation outcome data** (if Pennsylvania agrees) | aggregate counts of hires with prior federal service by former series and new class (n ≥ 5), as the first validation dataset for pathways (ADR-0023 §6) | Pennsylvania, under DUA | aggregate only (ADR-0012 I-1 §4) |

---

## 5. Other Stage 1b packages (outline only; specified later)

- **State class-spec crosswalks** for Texas and Washington, one county environmental health department and one municipal utility (same structure as Package C).
- **Fire crosswalk** keyed to the USWFS–USFS aligned federal qualification standards (effective Jan 2027) and NWCG PMS 310-1 positions, linking to — never competing with — those qualification systems.
- **Skills-gap template** for federal staffing plans (EO 14356 annual plans with quarterly updates [E: V1-08]) and state workforce plans; minimum cell 5.
- **Workforce-board sector kit** for in-demand occupation lists, ETPL review and Workforce Pell programme approval (programmes are identified and approved by **governors working with state workforce boards**, then reviewed by ED [E: V3-03]).

---

## Annex — Design-partner letter of intent (template; CC0)

> **Letter of intent — EMST design partnership, `[year]`**
>
> `[Agency / office]` intends to work with the EMST project as a **design partner** in `[year]` to co-produce `[Package A: the 0400 Kit for series ___ | Package B: a job-analysis starter pack for series ___ | Package C: the federal-to-state crosswalk for ___]`.
>
> `[Agency]` intends to: (a) name `[n]` subject-matter experts by role; (b) `[draft three to five PDs with the kit and send them through normal classification review | run the SME survey with its own incumbents for 3–5 vacancies | review the crosswalk rows for its classes]`; (c) share only de-identified documents and aggregate results (cells of at least five) under a separate data-use agreement; (d) give feedback through EMST's change-request process.
>
> EMST intends to: provide the package free of charge with named support; label all content with its use tier and the disclaimer that it is not a classification basis, job analysis or selection instrument; never use partner data to rank or assess individuals; and describe `[Agency]` as a design partner only after this letter is countersigned and entered in the EMST commitment register.
>
> This letter is not a contract, creates no funding obligation, and does not constitute agency endorsement of EMST. Either party may end the partnership by written notice.
>
> For `[Agency]`: `[role title]` · date — For EMST: `[project lead]` <!-- PENDING Q3 --> · date — Register ID: `CR-[yyyy]-[nnn]` · Year-five owner: `[role / organization]`
