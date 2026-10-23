# EMST v2 — Phase 4 build plan

- **Author:** CA (Chief Taxonomy Architect) · **Date:** 2026-10-23 · **Status:** accepted for Phase 4 kickoff
- **Builds:** ADR-0001 … ADR-0028, `docs/standard/SPEC.md`, `vocab/*.yaml`, `candidate_disposition.csv`, `v1_disposition.csv`, `mvp_role_set.csv`
- **Target:** `2.0.0-rc.1`, the describe/develop-grade release for the NGO pilot and the federal and state design partners (SPEC §19.1; ADR-0014, ADR-0024)
- **Team shape:** 10 build agents plus two gate roles (TN hold reviewer, CA integrator), in one intensive phase of five sprints

## 1. Ground rules for every work package

1. **Build from the decisions, not from memory.** Each WP reads its ADRs and CSV rows first. If a WP finds a decision unworkable, it opens a change request to the CA (ADR-0009) and does not work around it.
2. **Agent output is draft evidence, not validation.** Every value an agent rates or tags is recorded with `raterType = llm` (frozen model and prompt version) or `analyst`, `validationStatus = draft`, and evidence label `S` until a human reviews it (ADR-0024 §5; `vocab/evidence_labels.yaml#rater_types`). No WP may report agent ratings as SME agreement, Delphi retention or job-analysis confirmation. Gold sets, Delphi panels and reliability studies are **designed** in Phase 4 and **run with people** in Stage 1.
3. **Store atoms, compute summaries.** No counts, modal values, blends, tiers or roll-ups are typed into source records or documents; CI generates them (ADR-0021; P-DE-13). Counts in this plan are planning estimates only.
4. **The Tribal hold is a build invariant.** Everything listed in ADR-0007 §D is authored, if at all, as internal drafts with `approval_status = pending-tribal-review`, excluded from every release artifact by CI. No agent contacts, or writes as if it speaks for, any Tribal nation or practitioner. TN reviews every WP's output for leaks before merge (gate G-TN).
5. **No personal data, ever** (ADR-0012 I-1, I-2). Fixtures and examples are synthetic and labelled as such.
6. **Typing and naming rules apply to all text** (ADR-0003 T-1…T-8, G-1…G-9; ADR-0016 naming rule): no L4 product or L5 instrument named in L1/L2 text; function-based titles; programme labels only as `altLabel`.
7. **Corrected facts only** (ADR-0027 corrected-facts list, `docs/research/_verification/`). Any date-sensitive claim used in a kit, view or publication goes through WP-15 before release.
8. **Each role writes in its own lane.** Agents write only under the paths their WP names; they do not edit `legacy/`, `data/v1_baseline/` or other WPs' outputs, and they do not `git commit` (the CA integrates).

## 2. Agents, lanes and gates

| Agent | Role code(s) | Owns | Contributes to |
|---|---|---|---|
| A1 | **DE** | WP-01 (co), WP-02, WP-16 (co) | WP-09, WP-10 data plumbing |
| A2 | **IA** | WP-01 (co), WP-09, linker in WP-10 | WP-12 export formats |
| A3 | **FC** | WP-03 | WP-06 field enactments, WP-07, WP-08 task bundles |
| A4 | **DC** | WP-04 | WP-06 data enactments, WP-09 X12, WP-10 L4 seed |
| A5 | **SC** (with SL content review) | WP-05 | WP-06 regulatory enactments, WP-10 instrument registry (P-SC-14 owner) |
| A6 | **DB** | WP-06 | WP-08 module roles R24–R30 |
| A7 | **FH** (with SL, PS) | WP-08 | WP-09 X3–X5, X8, X9, X11; WP-13 kits |
| A8 | **IO** (with LC) | WP-11, WP-07 | lint rules in WP-01; review of WP-03–WP-08 |
| A9 | **LM** (with FS) | WP-10, WP-15 | WP-14 evidence chapters |
| A10 | **CP** with **AS** and **CM** | WP-12, WP-13, WP-14 | WP-08 display and claims review |
| Gate | **TN** | G-TN hold review on every merge | WP-13 Tribal gate procedures |
| Gate | **CA** | integration, change requests, release decision (WP-16) | ADR upkeep, DECISION_LOG |

Where one agent carries several codes, the junior codes review rather than author (e.g. SL reviews A5's state enactments; LC co-authors WP-07 with IO).

## 3. Sequence

| Sprint | Focus | WPs | Exit condition |
|---|---|---|---|
| S0 Foundations | schema, IDs, CI, migration, lint rules | WP-01, WP-02, WP-11 (lint and codebooks first) | v1 seed records validate; CI blocks seeded violations |
| S1 Content | competencies, tasks, modules, transversal layer, L5 seeds, crosswalk starts | WP-03, WP-04, WP-05, WP-06, WP-07, WP-09 (X1, X2 for P1 tasks), WP-10 | every core and wave-1 module disposition row has a draft record |
| S2 Roles and views | role profiles, generated series and class views, explorer | WP-08, WP-12, WP-09 (X3–X5, X7, X12) | P1 roles at full depth render in the explorer |
| S3 Package | governance and pilot docs, kits, publications, verification | WP-13, WP-14, WP-15 | every published claim verified or labelled |
| S4 Integration | release candidate | WP-16 | release gate passes (§5) |

Critical path: WP-01 → WP-02 → (WP-03…WP-07) → WP-08 → WP-12 → WP-14 → WP-16. WP-10 and WP-11 run alongside from S0.

## 4. Work packages

### WP-01 Schema, repository and CI (owner A1 DE + A2 IA)

- **Inputs:** SPEC §4–§5, §12, §17–§18; ADR-0010, ADR-0021; `vocab/*.yaml`; IA `data_model_v2.md` and schema properties; DE proposals; `tests/test_proposed_schema.py`.
- **Outputs:** `schema/emst.schema.json` (JSON Schema 2020-12, enums generated from `vocab/`); `schema/emst.context.jsonld`; `scripts/validate_v2.py` (cross-record rules); `scripts/mint_id.py` (single writer, CSPRNG, Crockford base32 with check symbol, append-only `data/v2/ids/registry.csv`); `scripts/build_release.py` (JSON-LD bundle, CSV + datapackage, SKOS, SSSOM); CI workflow; fixtures with seeded violations.
- **Acceptance:** all 19 vocab files load and generate enums; one valid and one invalid fixture per entity type (SPEC §5.1–5.24) pass/fail as expected; ID regex and check symbol verified on 10,000 minted IDs with zero collisions; registry append-only and "no module redefines a core ID" tests fail on seeded violations; Tribal-hold, personal-data, typing-lint and computed-field-in-source checks fail on seeded violations; two consecutive builds produce byte-identical bundles.

### WP-02 v1 migration (owner A1 DE)

- **Inputs:** `data/v1_baseline/` (copyB, hash-pinned) and `source_text/`; `v1_disposition.csv`; ADR-0011; DE P-DE-01…13.
- **Outputs:** seed records for all 222 competencies and 666 tasks (`status = draft`, `derivedFrom`, `seed:` keys until minted); restored D5 Knowledge/Application text and indicators, 2,104 truncated indicators and 19 title/description splits from source text; v1 tags as `ExposureAssessment` and tag records with `raterType = v1-analyst` (rater `v1-analyst-01`), low confidence; X1 v1→v2 SSSOM crosswalk generated from `v1_disposition.csv` (split, merge, `sssom:NoTermFound` for 3.4.3); legacy facets `v1_domain`, `v1_skill_area`.
- **Acceptance:** CI v1-completeness passes (every v1 key appears in X1 exactly once per decision); no stored summary field migrated; restored text diffs reviewed on a 10% sample; counts by decision generated, not typed.

### WP-03 Competency authoring — Field Craft (owner A3 FC)

- **Inputs:** `candidate_disposition.csv` rows with FC targets; `v1_disposition.csv` rows targeting FC practices (D4 carries and rewrites, field-risk split of 4.4.1, 4.4.4 core part, 4.5.3 core part, 1.4.3, 4.1.x); ADR-0003, ADR-0004, ADR-0005, ADR-0025 (FC enactment of TX-A); FC report.
- **Outputs:** core FC practice competency records with tasks (production vs adaptation-in-place split, G-2), indicators at each level in span (2–5 per level, `augmentationMode`, `useClass`, `obs4`), credential gates (T-8), field and formation dependency attributes, draft craft ratings (0/1/2) from three independent agent passes recorded as `llm` raters; FC enactment indicators for DC-CAND-13; field enactments for wave-1 modules handed to WP-06.
- **Acceptance:** every FC disposition row maps to a record or a documented merge; typing and indicator lint clean; every competency links ≥ 1 task (≥ 3 for P1 role targets); description ≤ 60 words; formation tasks flagged for every entry-level role in COR-1 and COR-2; protect suggestions (e.g. 1.3.2, 1.4.3, 4.1.3, 4.3.2) listed for Editorial Board decision, not set.

### WP-04 Competency authoring — Data Craft and the responsible-AI layer (owner A4 DC)

- **Inputs:** DC candidate rows; D2 rows of `v1_disposition.csv`; ADR-0003 T-1…T-5, ADR-0025; DC report and L4 seed list.
- **Outputs:** core DC practice competencies and tasks; TX-A floor (DC-CAND-01, -02, -13 with FC/DC/SC enactments, v1 7.2.3, DC-CAND-05 at L1); DC specialist responsible-AI competencies (DC-CAND-14, -15, -16, -19, -20, -21); `data/v2/tools/tools.jsonl` L4 seed (~53 DC entries plus FC field instruments and PS reporting tools, with DC's review triggers); X12 crosswalk to the DOL AI Literacy Framework (TEN 07-25) using its official area names.
- **Acceptance:** no technology family in any title (G-5); every tool moved out of v1 text appears in L4 with lifecycle state; DC-CAND-17 stays an L5 watch item; X12 validates as SSSOM with `NoTermFound` where DOL lacks environmental validation content.

### WP-05 Competency authoring — Statecraft and the regulatory core (owner A5 SC; SL reviews)

- **Inputs:** SC, SL, FH, PS candidate rows with core targets; D6 rows of `v1_disposition.csv`; ADR-0007 (enactments), ADR-0016, ADR-0017, ADR-0028; V2 key facts.
- **Outputs:** core competencies for review (SL-C08, SC-C03, SC-C04, SC-C09, DB-C50, DB-C52, FH-C01), authorization (SL-C02 with regulator and resource-manager variants, SC-C01, SC-C14, 5.5.2), inspection and enforcement (SL-C03, SL-C04, SL-C10, DB-C25, DB-C26), rules and resources (SC-C10, SC-C11, SC-C12, SC-C16, SC-C17, SC-C18, 6.4.5, 6.4.3), agreements (SC-C08, 3.1.4), TX-B (7.1.2, 7.1.3, PS-C18, SL-C16); structured actor enactments (authority basis, principals, delegated constraints); sensitivity edges from tasks to L5 instruments; regulation-neutral text with versions in L5.
- **Acceptance:** no instrument named in L1/L2 text; every regulatory competency has regulator and regulated-party mirror links where they exist (`Competency.mirrors[]` on the authority side, migrated in S2; ADR-0030); `venueApplicability` computes from the status of typed `requires` links (`venue-applicability@1.0.0`; ADR-0030) for the DEI/EJ-sensitive items (ADR-0016) on test fixtures; SC-C13 and every Tribal enactment stay held.

### WP-06 Wave-1 module editorial sections (owner A6 DB; FC, DC, SC enactments)

- **Inputs:** module rows in both disposition CSVs; `vocab/modules.yaml`, `vocab/subsectors.yaml`; ADR-0018; DB `module_steward_candidates.csv`.
- **Outputs:** namespaced records in `data/v2/modules/{water,waterq,air,waste,envhealth,hazards,forest,wildlife,parks}/` for every wave-1 module row, plus the early drafts named in the dispositions (FH-C03 in `worklands`, IA-CC-05 enactment in `forest`); module enactments of core competencies; a one-page module brief per section (scope, subsectors, candidate advisory partners labelled *candidate*, licensure and credential gates).
- **Acceptance:** three-module and home-module rules pass CI on every record (no module redefines a core ID; no core competency enacted in fewer than three modules without a recorded exception); every module record cites a subsector code; no partner named as committed.

### WP-07 Transversal and learning layer (owner A8 IO with LC; FC, FH contribute)

- **Inputs:** ADR-0025 (TX-A…TX-F), ADR-0026 (learning layer), ADR-0004; LC pathway templates and accreditation crosswalk notes; IO, FH, FS, CM candidate rows merged into TX-D.
- **Outputs:** TX-C, TX-D (v1 7.2.2 survivor, IO-C01, FH-C07), TX-E, TX-F (PS-C01–C03) records and enactments; course-level outcomes inside L1; exploratory learning pathways for the three P1 corridors with formation tasks and "by-hand" quotas where AI compresses learning tasks; evidence-equivalence register seed (X10) and credential register (`data/v2/registers/credentials/`) with issuer, gate type and verification status (GBCI for LEED AP and ISSP; ISEP; Water Professionals International).
- **Acceptance:** no pathway labelled "recommended" (ADR-0023, ADR-0027); every pathway step links tasks and role levels; credential rows carry verification status; accreditation text paraphrased and cited, never copied (SAF handbook rule).

### WP-08 Role profiles and generated HR views (owner A7 FH; SL, PS, CM contribute)

- **Inputs:** `mvp_role_set.csv`; ADR-0006, ADR-0017; FH `opm_series_register.csv`; SL `state_classification_sample.csv` and minimal common fields; PS reference job architecture; outputs of WP-03…WP-07.
- **Outputs:** 37 `RoleProfile` records with `RoleVariant`s (authority position, sector actor, industry, ownership, delivery model, sign-off authority); P1 at full depth (15–40 tasks with importance and time share, critical and needed-at-entry flags, 6–12 critical competencies with target levels by role level, all variants, change view); P2 at starter-kit depth; P3 with lifecycle, `reviewBy` and named counter-signal; P4 draft; generators for the Federal Series Profile and the State Class View; dated OPM series register (status incl. `proposed-realignment`); job families computed for navigation.
- **S2 work orders (amended 2026-10-23, ADR-0030 §4–§6):** cross-lane content from CR-FC-001, CR-FC-002 and CR-DB-001, the SC/DB/LM instrument-role edits, and the 21 unauthored releasable core rows are written inside WP-08 by the agents named in `docs/decisions/integration/s2_work_orders.csv`: rows needed by P1 roles in S2, the rest by the end of S3; anything unauthored at WP-16 is deferred to rc.2 and counted. The S1 builders (`docs/build/WP-03…WP-07`) are frozen: `data/v2/` records are the source of truth. `RoleVariant.instruments[]` are typed `{instrument, role}`. No net-new core competency without a CA offset (headroom after the ADR-0030 merges: 5).
- **Acceptance:** every role validates; mirror roles linked (R11 ↔ R37 ↔ applicant variant; R12 ↔ R37); each generated Federal Series Profile carries the "not a classification basis / not a job analysis / not for RIF or rating decisions" disclaimer; series proposed for realignment are never shown as realigned; Tribal variants held; no role profile carries personal data.

### WP-09 Crosswalks X1–X12 (owner A2 IA; FH, SL, LC, PS, DC co-own named sets)

- **Inputs:** ADR-0022 (X1–X12), `vocab/mapping_predicates.yaml`; O*NET 31.0 (plus 27.x for Eloundou-labelled tasks), SOC 2018, ESCO v1.2.1, CIP 2020, OPM series register, state class records, PS job architecture, DOL AI Literacy Framework.
- **Outputs:** SSSOM 1.0 mapping sets in `data/v2/crosswalks/<target>/<version>.sssom.tsv` (+ `.yml`): X1 (from WP-02), X2 for P1 corridor tasks (two independent coders), X3 with the verified v1 SOC errors fixed, X4, X5 for PA, TX and WA plus one county EH department and one municipal utility, X6 subset, X7 re-run on v1.2.1, X8 seed, X9 (current five-ECQ framework only), X10, X11 seed, X12; the competency-level linker (DP-18) with a gold-set design.
- **Acceptance:** every set validates against SSSOM 1.0, with the SSSOM 1.1 justification `semapv:LLMBasedMatching` accepted as a declared extension for unreviewed agent drafts and re-validated against 1.1 when it is final (amended 2026-10-23, CR-IA-002); role and variant subjects use `seed:<role_key>` and `seed:<role_key>/<sector_actor>[/<slice>]` (CR-IA-001); external IDs only, no upstream text in CC0 files (ADR-0013); `NoTermFound` recorded with reason; mapping justification and weakest match type on every row; X2 inter-coder κ reported; linker never publishes uncorrected top-1 counts (ADR-0019).

### WP-10 Change-signal and exposure seeding (owner A9 LM with FS; SC registry, IA linker, DC tools)

- **Inputs:** ADR-0008, ADR-0015, ADR-0028; `vocab/exposure_instrument_v2.yaml`, `driver_mechanisms.yaml`, `change_types.yaml`, `scenarios.yaml`; LM, FS, SC research; V2 and V4 key facts.
- **Outputs:** L5 instrument registry and dated driver events seeded from SC's 34 instruments as corrected by V2 (CEQ rule removal, Seven County, SPEED Act status, ESA harm rescission, GHG endangerment rescission, WOTUS proposed, Section 106 NPRM, SB 253, Colorado SB 26-189, OFCCP rescission of 41 CFR 60-3, OPM interim final rule removing UGESP references); v1 exposure values as prior evidence; external-index assessments on X2-matched tasks (Eloundou, Anthropic Economic Index releases, Microsoft Working with AI v6, BLS Employment Projections 2025–35 AI exposure categories); standing demand signals (OpenLMP, OMB AI use-case inventory, OPM FWD, October 2026 USAJOBS and state-board baseline snapshot); watch items (DC-CAND-17, PS-C19, FS-C16; TN-C13 held); scenario signposts.
- **Acceptance:** every signal carries driver tags, reliability A–D, source release and `personalData = false`; the two-family evidence rule blocks any change indicator supported by one family (CI test); external-index values are aggregated, never single-match; AEI's API automation-pattern share is never described as job automation; Tribal-flagged signals quarantined.

- **Lane (amended 2026-10-23, CR-LM-003 / ADR-0029 §10):** WP-10 writes `data/v2/signals/`, `data/v2/instruments/`, `data/v2/events/`, `data/v2/core/watch-items/`, `data/v2/assessments/external/` and `docs/methods/`. Its builder stays in `docs/methods/scripts/` as LM's authoring tool: it is deterministic, writes only in this lane, and is never run by CI or the release build. The evidence rule moves to `scripts/` and `tests/` (DE). SC contributes registry content through LM.

### WP-11 Validation kit (owner A8 IO)

- **Inputs:** ADR-0004, ADR-0005, ADR-0008, ADR-0015, ADR-0024; IO report; LC indicator-writing model (v1 7.2.x).
- **Outputs:** indicator lint (twelve banned constructions) and publication rules as CI checks (to WP-01); codebooks for craft ratings, work-function and authority-position tagging, and exposure XR-01…XR-07; reliability study protocol (120–200 units × 6 raters; Krippendorff's α with bootstrap CI, lower-bound gates .80/.667); pre-registered modified Delphi protocol with exact Lawshe critical values; cognitive-interview protocol (n ≈ 10–15); craft-scale pilot design; matrix-sampled job-analysis survey instrument for the first clusters (ADR-0024 §9); adverse-impact plan and documentation templates framed by the SIOP Principles, the AERA/APA/NCME Standards, job-relatedness under the Chance to Compete Act and Title VII disparate-impact defensibility (never "UGESP compliance"); LLM-coder gate protocol; gold-set specifications (≥ 10% of tasks, stratified).
- **Acceptance:** each protocol states its pre-registration fields, sample, analysis and stop rules; display gates encoded so values with α < .667 cannot render; no protocol reports agent ratings as human agreement.

### WP-12 Product: explorer and views (owner A10 CP; IA formats)

- **Inputs:** ADR-0012, ADR-0027; CP MVP design; outputs of WP-08 and WP-10.
- **Outputs:** Tier 1 static, local-first explorer with View 1 Role Change, View 2 Gap check (local-only), View 3 Pathways (exploratory), View 4 What's coming, for the 13 P1 roles; Federal Series Profile and State Class View pages; evidence drawer showing v1 values only as prior evidence; accessibility conformance report (WCAG 2.2 AA); security packet (applicability statement, SBOM, SSDF mapping, signed release).
- **Display rules (amended 2026-10-23, ADR-0030 §6):** `federalApplicability`/`venueApplicability` only from `views/venue_applicability.json` (`venue-applicability@1.0.0`), with "basis not yet linked" and "basis linked, status not yet verified" labels; generic CLOs, with enactment anchors behind an enactment filter; `employer-mandated` credentials labelled "Required by employer or agency policy"; mirrors from the computed `mirroredBy`; LLM craft passes as "assessment pending"; held items as counts only.
- **Acceptance:** no network request carries user-entered data; no personal data stored server-side; axe/Lighthouse accessibility checks pass at AA; every figure shows its use tier and evidence label; "assessment pending" shown where no v2 multi-rater assessment exists; claims-hygiene lint passes.

### WP-13 Governance, pilot and adoption documents (owner A10 AS with CM; TN gate procedures)

- **Inputs:** ADR-0007, ADR-0009, ADR-0013, ADR-0014, ADR-0023; AS governance charter draft; CM metrics and gates; `questions_for_project_lead.md` answers when available.
- **Outputs:** governance charter for adoption (Steward, Editorial Board, TSC, Advisory Council, Tribal Advisory Council with the consent authority the lead decides, Module Stewards, Validation Panels, Sentinel Network) with terms of reference; Module Stewardship Agreement template; contribution and change-request guide; commitment register (with year-five owner field); Stage 1a NGO pilot design and MOU template; Stage 1b design-partner packages (0400 Kit for 0401 and 0404 first, Job-Analysis Starter Pack, federal-to-state crosswalk with PA); restated theory of change one-pager; gate G1/G2 metric definitions; Tribal gate procedures (no outreach until reviewer compensation is funded and a TAC exists); licence notices (CC0, CC BY 4.0, Apache-2.0, third-party register); Ecosystem Atlas re-verification.
- **Acceptance:** no organization is described as committed without a dated commitment record; every governance body has decision rights, quorum and appeal path; documents carry the decisions' provisional status where an ADR is provisional.

### WP-14 Sector-facing package (owner A10 AS with CP; LM, FS, CM and all craft leads contribute)

- **Inputs:** ADR-0027 §5 and corrected-facts list; WP-08, WP-10, WP-12 outputs; LM, FS, FC, DC, SC, DB, PS, SL syntheses (TN synthesis only in the form TN approves for non-Tribal audiences).
- **Outputs:** flagship report "How environmental jobs are changing" (CC BY 4.0); briefing deck for federal, state and NGO audiences (mandate-framed: merit, skills-based hiring, mission readiness, knowledge retention); the interactive explorer (WP-12) as the companion; two-page role-change briefs for the 13 P1 roles; the Forester PD regenerated in FES format and labelled "subject to classification review".
- **Acceptance:** every figure and claim cites a verified source with tier label; career-ladder finding presented as a hypothesis with mechanism and evidence status; no v1 single-analyst statistic except as methodology history unless the lead decides otherwise (Q7); no Tribal content; nonpartisan posture (ADR-0016 §6); WP-15 sign-off on every date-sensitive statement.

### WP-15 Verification pass and claims register (owner A9 LM; AS co-signs)

- **Inputs:** `docs/research/_verification/`; every claim used in WP-08 kits, WP-12 views, WP-13 and WP-14.
- **Outputs:** claims register (claim, source, verification date, status, owner, re-check date); re-verification of remaining `[J]` claims used externally; watch list of moving facts (OPM series realignment, SPEED Act in Senate EPW, WOTUS, Section 106 NPRM, FAA Part 108, Colorado SB 26-189 effective Jan 1 2027, ADA Title II dates, ESCO language count).
- **Acceptance:** zero unverified claims in released artifacts; each moving fact has a re-check date before rc.1 and before 2.0.0.

### WP-16 Integration and release candidate (owner CA with A1 DE)

- **Inputs:** all WP outputs; SPEC §18 conformance; ADR-0024 release criteria.
- **Outputs:** `2.0.0-rc.1` build; generated release notes and counts (competencies by kind, module and lifecycle; roles by tier; held items, reported only as a count); delta file; updated DECISION_LOG and any superseding ADRs; comment-window plan.
- **Acceptance:** release gate in §5 passes.

## 5. Release gate for 2.0.0-rc.1

1. CI green on schema, cross-record rules, typing and indicator lint, Tribal hold, personal data, computed-field and v1-completeness checks.
2. Core size within the ADR-0003 G-9 range of 120–180 competencies (practice, knowledge areas and transversal, held items included), generated by CI and checked by the release self-check (ADR-0030 §3.1: S1 projection 180, 175 after five merges of unauthored v1 seeds); the planning estimate from the dispositions is about 169 published plus 11 held (180, the top of the range), so any net-new core competency needs an offsetting merge approved by the CA, and further consolidation of D3 and D5 items is preferred to growth.
3. Every published element shows its use tier; nothing is `select`; every displayed tag meets the α gate or is hidden.
4. All wave-1 module sections present; wave-2 and wave-3 content absent except the early drafts named in the dispositions.
5. 37 role profiles at their tier depth; Federal Series Profile and State Class View generated for every federal and state variant in P1–P2.
6. X1 complete; X2 for P1 tasks; X3, X4, X5 (pilot states), X7 and X12 at reviewed-subset level.
7. WP-15 sign-off on every external claim; ACR and security packet attached.
8. The lead's answers to `questions_for_project_lead.md` Q1–Q2 recorded (TAC authority; CC0 dedication); without Q2, rc.1 ships with v1-derived text excluded from the CC0 data files.

## 6. Risks the plan carries

| Risk | Where it bites | Mitigation |
|---|---|---|
| Agent ratings mistaken for validation | WP-03–WP-08, WP-14 | `raterType` and `validationStatus` mandatory; display shows evidence label; WP-14 acceptance forbids it |
| Core grows past 180 during authoring | WP-03–WP-07 | CA reviews any net-new core competency; G-4 test in CI |
| Tribal content leaks through enactments, signals or examples | all | CI hold checks; G-TN review on every merge |
| Moving federal facts (series realignment, NEPA procedures, SPEED Act) | WP-08, WP-12, WP-14 | instrument registry and dated register rows; WP-15 re-check dates |
| v1-derived text licensing unresolved | WP-02, WP-16 | Q2; fallback excludes v1-derived text from CC0 files |
| Partner names read as commitments | WP-06, WP-13, WP-14 | "candidate" label; commitment register is the only source of committed status |
