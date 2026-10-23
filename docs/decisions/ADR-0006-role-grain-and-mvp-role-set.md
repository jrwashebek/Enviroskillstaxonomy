# ADR-0006: Role-profile grain and the first role set — function × level with sector-actor variants; series × grade band as a generated federal view

- **Decision point:** DP-6 (MVP role grain and first role set)
- **Status:** accepted (grain); **provisional-pending-verification** (series crosswalk statuses rest on OPM's April 2026 consolidation, which is only *proposed* [E: V1-10])
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** FH, CP, SL, AS, CM, FS, PS, DB, LC, IO, TN
- **Related:** ADR-0004 (levels), ADR-0007 (sector actors), ADR-0017 (authority position), ADR-0022 (crosswalks), ADR-0023 (mobility), `docs/decisions/mvp_role_set.csv`

## Context — the conflict

- **FH (P-FH-01, P-FH-13):** the federal unit of use is **OPM series × grade band**; the first role set is the 13 priority series at two grade bands (26 profiles). "Could an HR specialist use this tomorrow?" requires series codes, grade bands, duty statements and Factor 1 language.
- **CP (§11 DP-6):** grain is **function × level of responsibility with sector-actor variants**, *not* series × grade, because series are being consolidated and are federal-only, and grade is a pay construct state classes do not match; 12–15 profiles (~30–40 variants) on three corridors ending in state and federal roles.
- **SL (P-SL-01, SL-Q1):** function × authority position with sector-actor variants plus a jurisdiction overlay; no per-state roles; a separate role (not a variant) only when task overlap is low (< ~60%) or a licence defines a legal scope of practice; 12 state/local MVP roles.
- **CM (open Q3):** pick roles to cover 10–15 pre-registered pathways. **FS (P-FS-05):** seed 8 emerging roles as `proposed`/`emerging`.

## Decision

1. **The stored grain is the function-defined role profile.** A `RoleProfile` has a function statement independent of any organization or tool, a primary work function and authority position, a task bundle (importance, time share, criticality, needed-at-entry, formation flag), competency targets (level per role level, importance, distinguishing), entry and progression links, and **role levels** (entry, journey, senior, lead, strategic) defined as bands of L1–L5 (ADR-0004).
2. **Sector-actor variants** (`RoleVariant`) share the function and the core task bundle and add or drop tasks, authority, instruments, credential gates, frictions and crosswalks. Variants exist for federal, state, local, tribal (held, ADR-0007), ngo, private and academic as needed.
3. **Separate role vs variant (SL rule, adopted):** create a separate role profile when (a) a licence or certification defines a legal scope of practice that changes which tasks may be performed (certified operator in responsible charge; REHS; PE), or (b) importance-weighted core-task overlap with the nearest role is below 0.60 (starting rule; IO and CM calibrate it against native state crosswalks and observed moves).
4. **FH's series × grade-band profile is a generated view, not the grain.** For each OPM series, the build assembles a **Federal Series Profile** from every federal variant crosswalked to that series (dated, status-aware), grouped by indicative grade band, in FES-compatible form: major duties with % time, Factor 1 knowledge statements, needed-at-entry and distinguishing flags, positive-education flags, USA Hire general competencies, and the disclaimer "not a classification basis / not a job analysis / not for RIF or rating decisions" (P-FH-05, P-FH-10). State class views are generated the same way from SL's minimal-common-fields records (P-SL-07).
5. **Job families** (v1 F1–F15 successors) are computed groupings of role profiles for navigation only; F4 and F13 are split (P-DB-14); no Tribal profession family (TN veto 5); no F16 (ADR-0020).
6. **First role set (v2.0): 37 role profiles in four tiers** (full list with crosswalks in `mvp_role_set.csv`):

   | Tier | Purpose | Roles | Depth in Phase 4 |
   |---|---|---|---|
   | **P1 Corridors** (pilot-critical) | Three corridors that cross all three crafts and end in state and federal variants (CP, AS): **COR-1** corps & field entry → technician → monitoring/data → geospatial (R01–R05); **COR-2** fire operations → fuels/prescribed fire → fire intelligence (R06–R08); **COR-3** restoration/land stewardship → environmental review, permitting, compliance → program management (R09–R13) | 13 (incl. 2 emerging) | Full: task bundles with time shares, anchored competency targets, all variants, crosswalks, change view |
   | **P2 Federal/state design-partner set** | Covers FH's 13 priority series (with P1) and SL's 12 state/local roles: forester, wildlife and fisheries biologists, hydrologist, rangeland, soil conservation, ecologist, park ranger/visitor & resource management, environmental engineer, enforcement case manager, drinking-water program analyst, certified water/wastewater operator, environmental health specialist, remediation project manager, air quality specialist, solid waste & materials specialist, hazard mitigation & floodplain manager | 17 | Starter-kit depth: 15–40 draft tasks, 6–10 critical competencies with target-level anchors, series/class crosswalks (FH §9 Q1 "usable tomorrow") |
   | **P3 What's coming** | FS's emerging roles not already in P1: AI-assisted review lead, environmental AI assurance officer, permitting-technology product owner, intergovernmental stewardship agreement manager, knowledge continuity lead, GHG and nature data controller | 6 | `proposed`/`emerging` lifecycle; FS's six extra fields (counter-signal, review_by…); shown only in the "what's coming" view |
   | **P4 Sector extension** | Facility environmental compliance specialist (regulated-party mirror of the inspector), to test regulator ↔ regulated mobility | 1 | Draft |

7. **Corridor pathways pre-registered for validation** (CM P-CM-01) are drawn from P1–P2: corps alum → agency technician; federal field technician → state/county technician; fire → county wildfire planner/fuels specialist; federal NEPA coordinator → state environmental review; state water-quality specialist → permit writer; wildlife graduate → consulting biologist; regulator ↔ facility compliance; technician → ground-truth steward.

## Rationale and evidence

- OPM's series layer is moving: 115 series are **proposed** for realignment (0410/0437/0480/0487→0401; 0455→0404; 0029→0303; 0688→0601), with no final decision as of 2026-10-23 [E: V1-10]. Fire intelligence work spreads across 0132, 1340, 1560, 2210, 0462 and 0401 [E: FH-040 via FH §4]. A series-keyed grain would re-key profiles whenever OPM acts; a function-keyed grain changes one crosswalk row (FH §9 Q2 itself recommends anchoring profiles to function).
- State classes are broader than series and level-encoded differently; one class spans many roles; the same function appears across very different classes (permit writing in PA Environmental Engineering Specialist, MI Environmental Quality Analyst, TX EPS III, CA Environmental Scientist) [E: SL-079, SL-073, SL-050, SL-038].
- FH's real need — a series-shaped artifact an HR specialist can use tomorrow — is met by the generated Federal Series Profile, which keeps FH's fields (REQ-FH-01…20) and disclaimers.
- CM: mobility similarity needs importance-weighted task bundles on role variants sharing a function ID (P-CM-04).

## Consequences

- DE/IA implement `RoleProfile`, `RoleVariant`, `JobFamily` (computed) and the two generated views (Federal Series Profile, State Class View).
- FH's `opm_series_register.csv` becomes a dated L6 register with `status ∈ {active, proposed-realignment, realigned-to:XXXX, cancelled}` (P-FH-02; FH open Q5 answered yes).
- P1 depth over P2 breadth follows CM's "depth over breadth"; P2 meets AS's 0400 Kit and Job-Analysis Starter Pack needs (P-AS-02, P-AS-03).

## Dissent and trade-offs

- **FH** may see the series view as second-class. The trade-off FH named — tight coupling to OPM (fast adoption) vs loose coupling (portability) — is resolved for loose coupling in storage and tight coupling in the generated view, plus an explicit offer to feed OPM's FWCI (P-FH-03; ADR-0014).
- **SL** prefers authority position as the second key of the grain; adopted as a required variant attribute (ADR-0017), not a key, because one function variant can sit in more than one position.
- **Trade-off named:** 37 profiles is more than CP's 12–15; it is held manageable by tiered depth. P2 and P3 are not shown in the NGO pilot's default views.
