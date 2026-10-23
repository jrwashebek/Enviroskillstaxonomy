# Gate G1 and G2 — metric definitions

- **Work package:** WP-13 · **Authors:** A10b (AS) with CM's metrics framework · **Date:** 2026-10-23 · **Licence:** CC BY 4.0 (this note); the definitions table `gate_metrics_G1_G2.csv` is data (CC0)
- **Builds:** ADR-0023 §7–§8 (accepted; the gates are its expansion criteria), ADR-0009 §2 (Workforce Voice Panel veto), ADR-0012 (no personal data), ADR-0027 §4 (WCAG 2.2 AA), ADR-0014 (stages); CM `metrics_framework.csv` (M-01…M-30); AS pilot design G1a–d.
- **Status:** definitions adopted where ADR-0023 fixes the threshold; **thresholds marked *proposed* must be co-signed by the real Workforce Voice Panel before the pilot starts**, so the goalposts cannot move later (CM panel design §1). <!-- PENDING Q9: the panel must be recruited and paid first. -->

## 1. What the gates decide

| Gate | Decision | When | Who decides |
|---|---|---|---|
| **G1** | Does EMST move from the Stage 1a NGO pilot (and Stage 1b co-production) to **Stage 2 federal and state adoption** (2028–29)? | March 2028 | the EB — or, if the EB is not yet constituted, the project lead as interim EB <!-- PENDING Q8 --> — with the Workforce Voice Panel's **binding usefulness veto** and ratification by stratum |
| **G2** | Does EMST move to **Stage 3, the whole sector including academia** (2029–31)? | at the G2 review after Stage 2 | the EB, with WVP ratification; the AC is consulted |

A gate **passes** only when every *hard* and *hard stop* condition passes and every *threshold* condition meets its threshold. *Supporting* metrics are reported, not decisive. *Watch* metrics run from day one and can trigger warnings at any time.

## 2. The gate conditions (summary; full definitions in the CSV)

### G1 (ADR-0023 §7, plus AS G1a–d)

| ID | Condition | Threshold | Type |
|---|---|---|---|
| G1-01 | "Does this help me?" (M-06) | ≥ 70% overall **and** ≥ 60% in every stratum | hard; WVP veto |
| G1-02 | Core-task completion and usability (M-07) | ≥ 80% completion; SUS ≥ 68 | threshold |
| G1-03 | EMST IDs in a real gate artifact (M-08) | ≥ 50% of pilot organizations; ≥ 30% repeat use | threshold |
| G1-04 | Pathway view validated or labelled exploratory (M-03) | validated (AUC ≥ 0.70 and ≥ 0.05 above the best naive baseline) **or** labelled exploratory throughout | hard |
| G1-05 | Friction register complete for pre-registered pathways (M-02) | 100% | hard |
| G1-06 | Accessibility and privacy clearance (M-05) | WCAG 2.2 AA ACR and privacy applicability statement signed | hard |
| G1-07 | Federal and state agreements (M-10) | ≥ 2 federal **and** ≥ 3 state signed register entries | threshold |
| G1-08 | Misuse incidents (M-11) | 0 | hard stop |
| G1-09 | Panel ratification (M-28) | majority within every stratum | hard; WVP veto |
| G1-10 | Role coverage (M-01) | ≥ 90% of requested roles | supporting |
| AS-G1a | Cohort retention | ≥ 10 of 12 organizations complete | threshold |
| AS-G1b | Willingness to continue without full stipend | ≥ 4 organizations sign continuation commitments | threshold |
| AS-G1c | Governance uptake | ≥ 2 pilot organizations in sentinel or advisory roles | threshold |
| AS-G1d | Stage 2 funding horizon (M-29) | ≥ 24 months secured or committed | threshold |

### G2 (ADR-0023 §7)

| ID | Condition | Threshold | Type |
|---|---|---|---|
| G2-01 | Credible contribution story for higher cross-actor hire rates (M-14) | increase vs comparison units ≥ the pre-registered minimum detectable effect, with a documented artifact chain, rated credible | hard |
| G2-02 | Movers' time-to-productivity and retention (M-15, M-16) | parity with internal hires | hard |
| G2-03 | No widening of equity gaps (M-17) | no gap widens; early-career, seasonal and corps strata at parity | hard |
| G2-04 | EMST IDs in live artifacts (M-18) | ≥ 2 federal agencies and ≥ 5 states; ≥ 80% crosswalk coverage | hard |
| G2-05 | Formation-task threshold on entry roles (M-19) | no entry role on a pilot pathway below threshold without mitigation | hard |
| G2-06 | Adoption breadth (M-25) | adopters in ≥ 5 actor types; **Tribal participation is never a target** | threshold |
| G2-07 | Stewardship funding horizon (M-29) | ≥ 5 years with a named steward | hard |
| G2-08 | Signal and crosswalk currency (M-30) | quarterly refresh with drift reported | threshold |
| G2-09 | Misuse incidents (M-11) | 0 | hard stop |
| G2-10 | Panel ratification (M-28) | majority within every stratum | hard |
| G2-11 | Role coverage for later actors (M-01) | ≥ 80% | supporting |

### Leading indicators from day one (ADR-0023 §8)

| ID | Indicator | Trigger |
|---|---|---|
| W-01 | Entry-cohort volume on field pathways (M-20) | a fall > 25% vs 2024 triggers a field-pathway warning to the EB, FC and LC |
| W-02 | Posting-language portability (M-26) | upward trend at partners vs comparison |
| W-03 | Degree-only screens on targeted pathways (M-27) | downward movement supports assumption A5 |

## 3. Measurement rules that apply to every metric

1. **Strata are never averaged away.** Where a threshold applies "in every stratum", each stratum is computed separately; a stratum with fewer than five participants is reported as *insufficient data*, not as a pass, and the panel decides whether the gate can close.
2. **Denominators are fixed in advance** in the pre-registration (released before the pilot starts). Organizations enrolled at kickoff are the denominator for organization-level metrics even if some withdraw.
3. **Computed, never typed.** Every gate value is computed from stored records (commitment register, artifact registry, friction register, research-partner aggregates) by a versioned rule; documents cite the computed value with its rule version (ADR-0021).
4. **No personal data.** EMST holds no person-level data (ADR-0012 I-1). Usability, diary and interview data are collected under IRB review by a research partner and returned as stratum aggregates; hire, retention and equity statistics are computed **by partners inside their own systems** and returned as aggregates with cells below five suppressed. Equity analysis therefore depends on partners' willingness to compute and share gap statistics; if none will, G2-03 cannot pass and the gate waits. **[J]** This reconciles CM's M-17 data source ("partner HR, consented") with ADR-0012.
5. **No telemetry.** The explorer is static and local-first; there is no in-tool analytics. CM's "in-tool prompt" for M-06 is implemented as a link to a survey hosted by the research partner, never as tracking.
6. **Attribution discipline.** A gain is attributed to EMST only if the artifact chain is documented, the gain exceeds comparison units, it does not coincide only with hiring-freeze lifting or hiring-reform events, and movers report EMST use (logic model §5); otherwise it is logged as "co-occurring, not attributable".
7. **Commitments count only from the register.** G1-07, AS-G1b–d, G2-04, G2-06 and G2-07 count only entries with `status ∈ {signed, active}` (`COMMITMENT_REGISTER.md`).
8. **Tribal participation** is never a target, never counted toward breadth and never solicited while the Tribal gate is closed (`docs/governance/tribal_gate_procedures.md`). <!-- PENDING Q1 -->

## 4. Changes from CM's Phase 2 framework (for CM to confirm)

| Item | Phase 2 text | Here | Why |
|---|---|---|---|
| M-05 standard | WCAG 2.1 AA | **WCAG 2.2 AA** | ADR-0027 §4 sets 2.2 AA as the release gate (a superset of Section 508 and ADA Title II requirements) |
| M-17 data source | "Partner HR (aggregate, consented)" | partner-computed aggregate gap statistics only | ADR-0012 I-1: EMST never receives individual demographic data |
| M-06 collection | "in-tool prompt (opt-in)" | survey link hosted by the research partner | ADR-0012 tier 1: no server, accounts, query logs or third-party requests |
| M-12 trust and opt-in | thresholds set by the panel before G1 | not a G1 condition in v2.0 | v2.0 ships no person-level feature; if one is ever proposed (Tier 2 only), the panel sets thresholds before it ships |
| AS G1a–d | proposed by AS | included as G1 threshold conditions | ADR-0023 §7 adopts them |
| M-01 | G1 gate in CM's table | supporting | not listed among ADR-0023 §7 conditions; reported for coverage decisions |
