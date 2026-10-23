# ADR-0022: The crosswalk programme (L6) and credentials, licensure and sign-off as first-class reference entities

- **Decision point:** DP-21 (new; CA) — crosswalk targets, method, priorities; where licensure lives
- **Status:** accepted; external versions verified 2026-10-23 (O*NET 31.0, O*NET-SOC 2019, SOC 2028 timeline, CIP 2020–SOC 2018, ESCO v1.2.1, SSSOM 1.0) [E: V3-01, V3-02, V3-09, V4-08, V4-09, V4-13]; the credential register is provisional until each row is verified
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** IA, LM, FH, SL, LC, PS, DB, DE, FC, IO, TN
- **Related:** ADR-0006, ADR-0010, ADR-0013 (IDs only), ADR-0017 (sign-off), ADR-0019 (thresholds)

## Context

v1's only crosswalk is family → SOC; v1 rates 7 of 15 mappings Low, and several are wrong: 19-1012 is Food Scientists and Technologists (labelled "Farm & Home Mgmt Educators", which is 25-9021); 33-1021 is First-Line Supervisors of Firefighting and Prevention Workers (labelled "Fire Inspectors", which are 33-2021/33-2022); 25-4031 Library Technicians and 29-9021 Health Information Technologists are misdirected; 19-2041 Environmental Scientists and Specialists, Including Health — the largest environmental SOC — is absent [E: IA-022, IA-019; DB-001 titles]. Public material claimed "validated against OPM and O*NET" without any competency-level crosswalk [E: CA-020]. Licensure, position qualifications and sign-off gate tasks in licensed subsectors, and SL, DB, FC, PS and LC each asked where credentials live.

## Decision

### 1. Method (all mapping sets)

SSSOM 1.0 mapping sets (1.1 slots `record_id`, `reviewer_agreement` as declared extensions), one set per upstream version, with SKOS predicates (`exactMatch`, `closeMatch`, `broadMatch`, `narrowMatch`, `relatedMatch`), negation (`predicate_modifier: Not`), `sssom:NoTermFound`, `semapv` justifications (incl. `LLMBasedMatching`), calibrated confidence kept separate from raw similarity, author and reviewer IDs, and pinned `object_source_version`. On each upstream release a CI diff sorts every row into carry / needs-review / deprecated / new-candidate (P-IA-04, P-DE-08). CTDL-ASN alignment predicates and CASE association types are export renderings. External **IDs only** in CC0 files (ADR-0013).

### 2. Mapping sets and priorities

| # | Set | Grain | Priority / owner |
|---|---|---|---|
| X1 | EMST v1 → v2 | every v1 competency and task (`replacedBy`, splits, merges, `retiredWithoutReplacement`) with CI completeness | Phase 4 WP-02 · DE |
| X2 | EMST task → **O*NET task and DWA** (O*NET 31.0; plus an explicit mapping to the O*NET 27.x tasks on which Eloundou labels sit) | task | **binding cost of external calibration**; two coders, κ ≥ 0.6 on match type; candidates restricted to the role family's O*NET-SOC pool; expect ~30% none and mostly partial | Phase 4 WP-05 · LM + IA |
| X3 | Role variant → **O*NET-SOC 2019 / SOC 2018** | role variant | replaces the family → SOC sheet; fix the verified errors; prepare a SOC 2028 re-map (final FRN planned 2027) | WP-05 · IA + FH + LM |
| X4 | Role variant → **OPM series register** | federal variant | register of 73 series with `status ∈ {active, proposed-realignment, realigned-to:XXXX, cancelled}`, `effectiveDate`, `successorSeries`, qualification-standard version, positive-education flag; each OPM issuance is a dated L5 event; re-checked quarterly until OPM finalizes Phase One (P-FH-02) | WP-05 · FH |
| X5 | Role variant → **state class records** | class (position overrides only in pilots and flagged-broad classes) | SL's 28 minimal common fields (16 MUST); dated, re-run each 1 July or on state-plan revision; native state crosswalks (TX military, NY 70.1, MN equivalents, PA federal equivalencies) used as gold sets (P-SL-01, P-SL-07, P-SL-08) | WP-05 · SL |
| X6 | Competency/CLO → **CIP 2020** via learning resources, and → accreditation criteria (SAF, ABET EAC/ETAC, EHAC, NAAEE 2025) | competency × level | versioned; I/R/E scale; paraphrase-and-cite, never copy (P-LC-08, P-LC-09) | WP-07 · LC |
| X7 | Competency → **ESCO v1.2.1** | competency | re-run the v1.2.0 prototype on v1.2.1; `NoTermFound` where ESCO lacks Tribal consultation, wildland fire or AI-validation concepts (IA §4) | WP-05 · IA |
| X8 | Role variant → **private reference job architecture** (industry × job family × career stream × level) | private variant | PS's 88-row seed; GSA labor-category data investigated as a public seed (P-PS-08) | WP-05 · PS |
| X9 | Competency → OPM FWCI general and technical competencies; USA Hire coverage; ECQs only in the current five-ECQ framework (Oct 1 2025; Political Savvy, Partnering and Influencing/Negotiating removed — mappings to those names are not made) [E: V2 SC-058] | competency | as OPM publishes (P-FH-03) | WP-05 · FH |
| X10 | Credential ↔ CLO **evidence-equivalence register** (RPL) | credential × CLO | NWCG quals, FAA Part 107, operator grades, HAZWOPER, CWB, PWS, GISP, REHS; IO validates (P-LC-07) | WP-07 · LC + IO |
| X11 | Public ↔ private translation (TR-01…TR-38) | competency/role pair | with friction fields (licensure gap, pay direction, posture change) (P-PS-07) | WP-08 · PS + CM |

### 3. Credentials, licensure and sign-off (answers SL Q4, FC Q5, PS Q3)

- **`Credential`** is a reference entity (registered in L6, CTDL-ready): issuer, credential type (`licence | certification | certificate | position-qualification | mandated-training-record`), issuing jurisdiction, legal basis, scope of practice, renewal, reciprocity, closure type (legal licensure / regulation-mandated training / voluntary — DB §6), and an issuer-verified flag.
- Credentials are linked as **`credentialGate`** on tasks and role variants (required, preferred, entry requirement), and as **`signOffAuthority`** where a credential confers legal sign-off (ADR-0017 §5). They **never stand in for proficiency** (ADR-0003 T-8).
- **Seed:** DB's 92-row register, corrected by V3: LEED AP and ISSP-SA/ISSP-CSP are issued by **GBCI**; IEMA is now **ISEP**; water and wastewater operator certifications are issued by **states**, with exams often from ABC (now **Water Professionals International**); every other row stays `issuer-verified = false` until checked (P-DB-07, P-DB-16).
- **Licensure-defined levels** (operator grades, NWCG/NIMS qualifications) map onto L1–L5 through module-specific anchors (ADR-0004 §8).

### 4. Acceptance thresholds by use (with IO and FH)

Selection-context mappings: two independent human reviewers, ≥ `closeMatch`, reviewer agreement recorded; analytics: reported coverage, predicate mix, κ and staleness per set; navigation: single-reviewed candidates labelled as such (ADR-0019 §8). **No public claim of O*NET, ESCO, OPM or state alignment until a reviewed set exists** (IA issue; ADR-0027).

### 5. Immediate corrections

Fix F10 and F12 code–title errors now; mark F8, F11 and F13 mappings misdirected; add 19-2041, 19-4042, 19-4071, 13-1041, 13-1199.05, 19-2041.01–.03, 19-2099.01; retire the family-level sheet as an anchor once X3 exists (P-IA-05, P-LM-10, P-FH-07, P-DB-15).

## Dissent and trade-offs

- **SSSOM vs a simple table:** heavier and unfamiliar to HR users; the only open format with per-row provenance, negation and "no term"; a flattened CSV is shipped alongside (IA disagreement 3).
- **SL: fidelity vs maintainability** — class-level crosswalks with position overrides only in pilots (SL disagreement 6), adopted.
- **Trade-off named:** a crosswalk programme is the largest recurring cost after content; it is what makes EMST usable inside every other system.
