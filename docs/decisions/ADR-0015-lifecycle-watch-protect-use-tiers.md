# ADR-0015: Lifecycle states, the `watch` pre-state, the `protect` overlay, and use tiers

- **Decision point:** DP-14 (lifecycle states, `watch` pre-state and `protect` overlay)
- **Status:** accepted (thresholds are starting values, recalibrated after the first annual Signals Review)
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** FS, IO, DC, LM, CP, AS, FC, SC, TN
- **Related:** ADR-0008, ADR-0010 (editorial status), ADR-0024 (validation evidence by use), ADR-0028 (signals and horizon scanning); `vocab/lifecycle_states.yaml`, `vocab/lifecycle_states.yaml#use_tiers`

## Context

v1's stability tier was a deterministic function of reform flags and Ac/S calls (zero rule violations), classed 150 of 222 as "Transition", and omitted workforce-reproduction stability [E: audit §11]. FS proposed lifecycle states on L1–L4 with evidence thresholds and review-by dates, a pre-content `watch` state in L5, and a stored `protect` overlay so that falling public demand is never read as licence to let a safety- or trust-critical capability lapse (P-FS-02, P-FS-03). DC proposed a `watch → active → legacy → retired` lifecycle for L4 tools (P-DC-04). IO and AS proposed use labels (P-IO-13; charter Art. 5.6).

## Decision

### 1. Two independent status dimensions on every L1–L4 record

- **Editorial status** (`status`, ADR-0010): `draft → candidate → published → deprecated | superseded | withdrawn` — *is this record released, and is its ID stable?*
- **Lifecycle state** (`lifecycleState`): *how established is this work in the world?* — states below. A record can be `published` and `emerging` at once.

### 2. Lifecycle states (FS thresholds adopted as starting values)

| State | Lives in | Meaning | Maximum use tier | Review by | Entry threshold |
|---|---|---|---|---|---|
| `watch` | **L5 only** (a watch item = signal cluster + hypothesized entity) | Something may be forming | exploratory | +12 months; **lapses** without new evidence | ≥ 2 signals, or 1 high-priority signal |
| `proposed` | L1–L4, persistent ID, non-normative flag | A draft definition exists, composed from L2 tasks | exploratory | +12 months | ≥ 3 independent signals of ≥ 2 types from ≥ 2 sector actors, **or** one mandate with an effective date |
| `emerging` | L1–L4 | Observable in work | develop (**never select**) | +24 months | ≥ 10 postings/PDs across ≥ 2 actor types in 12 months, **or** a named operating programme; feeder roles identified |
| `established` | L1–L4 | Validated and stable | select (only where IO evidence is met, ADR-0024) | +36 months | ≥ 30 postings/PDs across ≥ 3 actor types over 12 months, **or** a major employer's classification or PD standard; plus SME validation and assessable indicators |
| `declining` | L1–L4 | Demand falling or task substituted | all uses, flagged; development de-prioritized | +24 months | demand share down ≥ 30% over 24 months, **or** the S-confirmation checklist met; **protect check mandatory** |
| `withdrawn` | L1–L4 (ID and crosswalks kept) | No longer current | none (history) | — | below threshold 36 months, no protect flag, CA/Editorial Board approval |
| `lapsed` / `merged` | L5 / L1–L4 | Watch expired / absorbed into another ID | none / redirect | — | automatic / editorial decision |

- Tasks and tools use the same states. DC's L4 states map: `watch`=watch, `active`=established, `legacy`=declining, `retired`=withdrawn; L4 keeps DC's faster review triggers (quarterly for half-life ≤ 2 years; out-of-cycle on vendor end-of-life, pricing/access change, policy instrument issued or sunset, inventory retirement, curriculum retirement, security advisory) (P-DC-04).
- **Migration defaults:** v1 competencies enter as `established` only where FS's stress test and role verdicts agree; otherwise `emerging` or as candidates require; v1 "Emergent" tier items enter as `emerging` or `proposed` per evidence; tool-bound v1 items moved to L4 take DC's L4 states.
- Every future-facing record carries `reviewBy` and, for `proposed`/`emerging` roles, a **named counter-signal** (what would show it is not forming) (FS §7).

### 3. The `protect` overlay (stored governance decision, never computed)

- **Criteria:** at least two of — failure would be severe (life safety, legal duty, irreversible ecological harm, broken trust); reproducing the capability takes ≥ 5 years; supply is fragile in ≥ 2 scenarios (SC1–SC4).
- **Effects:** cannot move to `withdrawn` without Editorial Board approval plus sector consultation; priority for knowledge capture (NR-2) and for formation design (ADR-0026); shown in workforce-planning views.
- **Process:** FS's stress test (59 v1 competencies suggested, e.g. prescribed burning, forest mensuration, species identification, water-quality surveys) produces *suggestions*; the Editorial Board decides; Tribal-related items (e.g. 6.5.1) are decided only with Tribal Council consent.

### 4. Use tiers (`useTier`) — unifying IO's use classes and AS's validity tiers

| Use tier | Permitted uses | Equivalent labels |
|---|---|---|
| `exploratory` | foresight, "what's coming", curriculum exploration | AS "exploratory"; FS proposed/watch |
| `describe` | workforce analytics, planning, curriculum mapping | IO "describe/plan" |
| `develop` | training, task books, IDPs, self-assessment | IO "develop"; AS "training-grade" |
| `select` | hiring and promotion — **only as input to the employer's own job analysis** | IO "select/promote"; AS "selection-grade" |

A record's effective use tier is the **minimum** of (lifecycle cap, IO evidence met, tag reliability gate). Every indicator also carries `useClass` (ADR-0004). Kits state the tier on their face.

## Rationale and evidence

- Two speeds: HR users should never see churn in what they hire against, and foresight users should not wait a year to see a new role (FS §6.1). Demand is not supply: public demand falls first under SC3/SC4, so the taxonomy would otherwise record irreversible losses as routine decline (P-FS-03).
- The FS thresholds use corroboration across signal types for early states and postings only for `established`, because postings lag pilots and mandates (FS disagreement 4); `lapsed` and review-by dates limit the cost of false positives.
- IO: validity belongs to a use, not to a taxonomy; no release is "validated for selection" in itself (IO §8 Q4).

## Consequences

- CP's views filter by use tier: HR and selection-adjacent views show `established` content only; the "what's coming" view (P-FS-13) shows `watch`/`proposed`/`emerging`.
- DC-CAND-17 (supervise agentic AI, [S]) and similar candidates may enter v2.0 as `proposed` (answers DC open Q7).

## Dissent and trade-offs

- **IO** may want even training uses of emerging content gated by validation; FS accepts a hard bar on selection only. The CA sides with FS for `develop` use of `emerging` content, because a training officer acting on an AI-assurance gap in 2027 cannot wait for a 2029 validation study (FS disagreement 3).
- **LM** may prefer posting-volume evidence throughout; used for `established` only.
- **Trade-off named:** governance complexity and a standing scanning budget versus a taxonomy that is current at first release without destabilizing the validated core.
