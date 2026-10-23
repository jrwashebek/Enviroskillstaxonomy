# ADR-0008: Exposure and change model — three constructs, dated and attributed, scenario-conditioned only where it matters

- **Decision point:** DP-8 (exposure/change model; external measures; v1 values; scenario conditioning)
- **Status:** accepted; external-index versions verified by V4 on 2026-10-23 (AEI releases, Microsoft "Working with AI" v6, Canaries Aug 2026, ILO WP 140, BLS 2025–35 with AI exposure categories, O*NET 31.0); index **ingest** remains provisional on the curated EMST-task → O*NET-task crosswalk (ADR-0022)
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** LM, FS, FC, DC, SC, IO, IA, TN, DB, CP, CM, LC
- **Related:** ADR-0005 (field dependency), ADR-0015 (lifecycle, protect), ADR-0021 (stored vs computed), ADR-0028 (signal layer), `vocab/exposure_instrument_v2.yaml`, `vocab/scenarios.yaml`

## Context

v1's instrument is right in concept and unit (tasks; Ac; CLD; robotics/convergent vectors; A/V current-deployment rule) and wrong as an instrument: one LLM-assisted rater, no reliability; tacit density nearly determines automation type; the "FC/DC structural property" is built in by standing rule R1 and contradicted by 9 H tasks on DC-primary competencies; D7's all-H calls are normative; horizon 3 never used; no external calibration [E: audit §10; LM §5.1; FC §8 Q4]. Exposure codes were often assigned to *different text* than the database shows (D1 82/120 and D3 98/105 tasks below 0.8 similarity; D2 database agrees with its own working records on 37/105) [E: data-audit §7].

LM proposed three constructs (P-LM-01); FS proposed a three-part change model with scenario conditioning (P-FS-04). They are compatible and are merged here.

## Decision

### 1. Every exposure judgment is an `ExposureAssessment` record about one L2 task

Fields: task ID and the **SHA-256 of the exact task text rated** (stale if text changes, P-DE-05); optional role variant and sector actor; instrument and codebook version; rater type (`expert-panel | sme | analyst | llm | external-index | v1-analyst`), pseudonymous rater ID; date; method; confidence; evidence label and sources; optional `scenario_id` and `strategy_id`. Many assessments per task coexist; agreement is computed and shown.

### 2. Three constructs, never fused into one code

| Construct | Unit | Scenario-conditioned? | Values (codebook v2) |
|---|---|---|---|
| **(a) Technical exposure (performability) by vector** | task | **No** — dated | vector ∈ {llm-cognitive, robotics, sensing, convergent}; level E0–E3 per vector (E1 = time cut ≥ 50% at equal quality; aligns with Eloundou) |
| **(b) Deployment mode and adoption pathway** | task × sector actor (deployment) / strategy tag | No (observed); strategy is a tag | mode ∈ {human-executes, human-assisted (A), compressive (Ac: substantial time compression with review-and-certify), human-supervises-system (V), system-executes (S)}; deployment stage ∈ {none, pilot, deployed-limited, deployed-scaled}; strategy ∈ {substitution, augmentation, augmentation-for-formation} |
| **(c) Outcome** | role variant / organization (staffing) and task (scenario impact) | **Yes, only for tasks above an exposure threshold or flagged formation tasks** | staffing outcome ∈ {grow, stable, compress, decline, insufficient-evidence} with driver tags; scenario rows (SC1–SC4): demand direction ∈ {up, flat, reshape, external, down} and reproduction risk L/M/H |

Supporting task attributes (stored separately, ADR-0005): `field_dependency`, `formation_dependency`, tacit/experience requirement (assessed independently, used as a *predictor*, not inferred from mode), `accountability_constraint` (legal requirement for a human in responsible charge; descriptive), and `governed_data` (TN rule R13).

### 3. Codebook v2 rules (replace R1–R12; unique, versioned IDs `XR-NN@2.0`)

- **XR-01** Code blind to parent competency, domain, craft and any prior label (drops R1's expectation clause; P-FC-16).
- **XR-02** Descriptive and normative judgments are separate fields: "no deployed tool performs any part of the core task" (descriptive) vs `should_remain_human_reason` (normative, e.g. accountability); v1 "H" is decomposed into `field_dependency` + mode + the normative field (LM §5.2, FC Q4).
- **XR-03** Ac is a task-level **time-compression** rating; **headcount compression is never a task property** — it is a role/organization staffing outcome (LM §5.2).
- **XR-04** S, V and "deployed now" claims require deployment evidence (registered deployment or observed directive use); otherwise downgrade to Ac with an `s_watch` flag (P-LM-04). v1's four S calls migrate this way, with the original call kept as a v1 assessment.
- **XR-05** Governed data: a task handling confidential Tribal information or Indigenous knowledge carries `governed_data = tribal`; its mode may be A or Ac only "where the Tribe authorizes AI use", otherwise human-executes (P-TN-09). Re-code 6.5.1 T3, 5.3.2 T3, 5.3.3 T2.
- **XR-06** Never attach a single external match label; aggregate across matched O*NET tasks weighted by match type and show dispersion (LM pilot: labels differed for 13 of 21 two-match cases).
- **XR-07** Exposure assessed on module tasks before any sector-wide conclusion (P-DB-13) — robotics-exposed subsectors (MRF sorting, process control, lab automation, pipe inspection, CEMS) were absent from v1.

### 4. External measures (P-LM-03, verified V4)

- **Ingest as attributed assessments keyed to O*NET task and release:** Eloundou et al. human and GPT-4 E-labels and T-rubric (aggregate, never single-match); Anthropic Economic Index task usage and collaboration-mode shares across its six numbered releases (2025-02-10 … 2026-06-26), plus `labor_market_impacts` (2026-03-05) and `robot_exposure` (2026-09-30) as the first robotics calibrator, with an insufficient-evidence rule [E: V4-01]; Microsoft "Working with AI" applicability via O*NET task → DWA → IWA (cite v6 title) [E: V4-02]; **BLS AI exposure categories** (theoretical vs observed, new with the 2025–35 projections, released 2026-08-27) as an official comparator [E: V4-07]; OMB AI use-case inventory deployment stage as a sector-actor attribute on *functions* [E: LM-027, DC-001].
- **Context only:** AIOE/LM-AIOE, Webb, ILO WP 140 (May 2025), WEF Future of Jobs 2025, PwC, MGI [E: V4-04, V4-05].
- **Benchmarks, not assessments:** Canaries (22–25-year-olds in the most-exposed occupations ~19% below trend by June 2026; descriptive, reduced hiring, ADP under-covers government) [E: V4-03]; Humlum–Vestergaard.
- **Sensing tracker** (no index exists): build from agency programme reports, protocols and the inventory's species and remote-sensing clusters; co-owned FC/DC/LM (P-LM-05).
- **Independence and disclosure:** EMST is built with an AI vendor's model and ingests that vendor's usage data; every release discloses this and applies a triangulation rule (no change indicator may rest on AEI alone) (LM §10).

### 5. v1 values

All v1 exposure values (786 classification rows, `data/v1_baseline/exposure_sources.csv`) migrate as `rater_type = v1-analyst`, `rater_id = v1-analyst-01`, `confidence = low`, with flags `text_misaligned` (D1, D3), `reconstructed_d2` / `d2_divergent`, `reconciled_d6_2026_03`, `normative_h` (D7). They are **prior evidence only**: never shown as v2 values, never aggregated into public numbers, never used to move a change indicator (P-DE-03, P-IO-14; CP display policy in ADR-0027).

### 6. Computed indicators (never stored; versioned rules)

Competency and role exposure **distributions** (not a single modal label; P-DE-04, DE open Q4); **CLD** as a pathway-level indicator — share of an entry role's formation tasks assessed Ac/V/S, adjusted for designed alternative formation routes, with **driver attribution** (AI, sensing, automation, fiscal, policy) and a **top-of-ladder loss** mechanism for senior reviewer attrition (P-LM-06); **entry-path health** per role (formation tasks still present in entry roles; entry hiring exists; P-FC-11); **robustness class** (robust / contingent / fragile) and **scenario-sensitivity profile** replacing the stability tier (P-FS-04).

### 7. Scenarios (L0)

The scenario set **SC1 Assured Augmentation, SC2 Human Premium, SC3 Platform Stewardship, SC4 Patchwork Retreat** (capacity rebuilt/coordinated vs thin/fragmented × AI trusted/assured vs brittle/contested) is a versioned L0 vocabulary with signposts, refreshed every 3 years (first 2029) (P-FS-01). v1's investment × adoption-mode axes retire; augmentation/substitution becomes the strategy set.

## Rationale and evidence

- The literature measures exposure, deployment mode and outcome separately; v1's single code forced coders to answer all three at once (LM §5.2). In the 60-task pilot, 30% of v1 tasks had no O*NET analogue (candidate new work), matched Ac tasks were externally rated exposed in 11 of 13, and S was not corroborated [E: LM pilot].
- Environmental work has two exposure profiles: analytical and regulatory occupations at the 81st–99th percentile on Eloundou, field and operations at the 10th–33rd [E: LM-008]; usage data under-sample government work [E: LM-009, LM-007].
- 2025–26 public-workforce change is fiscal and policy-driven, not AI (FC §3; LM §3.3) — driver attribution keeps contraction from masquerading as automation.

## Consequences

- Phase 4 must fund the two-coder EMST-task → O*NET-task crosswalk (LM open Q5) before any calibration; until then the role-change view shows only v2 multi-rater assessments, flagged as pending where none exist.
- DE enforces text-hash staleness; IO's α gate governs which assessment fields are displayed.

## Dissent and trade-offs

- **LM vs "usable tomorrow":** HR users want one label per role; LM wants components shown. Resolved: one computed headline per role (direction + confidence) with drill-down to components (LM disagreement 5).
- **FC:** "Human-Essential" was persuasive but wrong for presence-required *and* augmented field work; the two-field model is less quotable and more accurate.
- **DC:** indices built from LLM usage under-measure environmental data work dominated by classical ML on sensor and EO data — hence the sensing tracker and inventory-based deployment signals.
- **SC:** reads 6.4.4 T2 (comment analysis) as Ac, not S (P-SC-11) — consistent with XR-04.
