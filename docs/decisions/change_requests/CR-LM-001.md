# CR-LM-001: Fields the ADR-0028 evidence rule needs on ChangeSignal, plus small L5 vocabulary gaps

- **From:** LM (A9, with FS), WP-10 · **To:** CA (decider), DE (schema, validator, WP-01) · **Date:** 2026-10-23 · **Type:** X (structural; schema and vocabulary) · **SemVer impact:** minor (new optional fields and terms)
- **Affects:** SPEC §5.14, §5.16; `schema/emst.schema.json` `ChangeSignal`, `DriverEvent`, `Instrument`, `WatchItem`; `vocab/change_types.yaml`, `vocab/scenarios.yaml`; `scripts/validate_v2.py` source loading
- **Evidence label:** J (LM; the gaps were found by writing the WP-10 seed against the schema and by implementing the rule in `docs/methods/ci/evidence_rule.py`)

## Problem

ADR-0028 §2 decides that a change indicator moves only when **two independent signal families** agree, signals **persist** (two periods, or one period plus a **registered deployment**), the crosswalk path is ≥ close, the **driver** is declared, and a named human has reviewed. It also forbids any indicator resting on a **single vendor's data** (ADR-0008 §4) and counts **two indices on the same data family as one**. The schema has no field for the signal's family, its upstream data lineage, or registered deployment, so CI cannot apply the rule. The same gap blocks the computed `priorityScore` (impact × reliability × (novelty + corroboration)): `impact` is not stored.

This matters in practice. BLS's new AI exposure categories (2025–35 projections) build "observed" exposure from Anthropic and Microsoft usage data and "theoretical" exposure from Felten–Raj–Seamans, Eloundou et al. and Eisfeldt et al. [E: V4-07; BLS publication page read 2026-10-23]. Without a lineage field, CI would count BLS and AEI as two independent families when they share a vendor.

## Interim encoding used in the WP-10 seed (validates today)

The seed carries these values as `notation` entries with `EMST-` schemes, so nothing is lost and the migration is mechanical:

| Interim `notation.scheme` | Proposed typed field | Values |
|---|---|---|
| `EMST-signalFamily` | `signalFamily` | capability · observed-use · deployment · postings-pds · headcount · plan-requirements · worker-report · policy · projection · workload |
| `EMST-independenceKey` | `independenceKey` | free key naming the upstream dataset (e.g. `anthropic-economic-index`, `bls-ai-exposure-observed`); providers per key in a governed table (`docs/methods/ci/evidence_rule.py#PROVIDERS` until DE moves it to `vocab/`) |
| `EMST-registeredDeployment` | `registeredDeployment` | boolean; deployment family only |
| `EMST-impact` | `impact` | 1–3 (FS protocol §6) |
| `EMST-signpost` | `scenarioSignposts[]` | `vocab:scenarios#SP-NN` |
| `EMST-pointsToward` | `pointsToward[]` | scenario IDs or axis poles, on signpost readings |
| `EMST-measureBaseline` | `measure.baseline{value, ci95, n, note}` | ADR-0028 §1 lists a baseline; the schema's `measure` is closed |
| `EMST-measureSensitivity` | `measure.sensitivity{weighting, value, baselineValue}` | ADR-0028 §4 requires component-weighted sensitivity checks for plan series |

## Proposed change

1. Add the typed fields in the table to `ChangeSignal` (optional; `signalFamily` and `independenceKey` required once `signalStatus = active`). Generate `signalFamily` from a new `vocab/change_types.yaml#signal_families`, with `projection` and `workload` marked "context only, never counts toward ER-1".
2. Move the provider table into `vocab/change_types.yaml#independence_keys` (key → providers[]), stewarded by LM, so "single vendor" is a vocabulary fact, not code.
3. Port `docs/methods/ci/evidence_rule.py` into the build's indicator rule (`vocab/rules/change-indicator@1.0.yaml`) and move `docs/methods/ci/test_evidence_rule.py` + `evidence_rule_cases.yaml` into `tests/` (they pass today: every synthetic case, plus a regression asserting that no seeded agent signal moves an indicator).
4. `targetType` values: allow an **organization** target (ADR-0008 (c) staffing outcome is "role variant or organization") and an **occupation** target (BLS, O*NET-SOC), or rule that occupation signals always attach through X3 to role profiles (the seed does the latter; organization signals currently target `vocab:sector_actors#federal` with the agency named in the label).
5. `DriverEvent.statusAfter`: generate from a vocabulary. The seed uses `pending-legislation | proposed | interim-in-force | final-not-yet-effective | in-force | in-force-litigated | enjoined | stayed | vacated | rescinded | repealed | issued`.
6. `DriverEvent.eventType`: add `submitted-for-review` (OIRA). The Section 106 rewrite and the FAA Part 108 final rule are both at OIRA; the seed records them as watch-status policy signals, not events.
7. `Instrument.instrumentType`: add `agency-order` (Secretarial Orders such as SO 3448 are now typed `executive-order`).
8. `vocab/scenarios.yaml`: give the twelve signposts notations `SP-01`…`SP-12` in their current order, so readings can target them (`vocab:scenarios#SP-NN`); SP-12 (Tribal co-stewardship agreements) is readable only through the Tribal Council.
9. `scripts/validate_v2.py` `_load_source_ids`: also read `docs/methods/sources.csv`. The seed cites resolvable V-pass fact IDs today and keeps the precise page rows (LM-101…LM-153) there.
10. Re-point `targetId: mvp-role:<key>` (ExternalRef to `docs/decisions/mvp_role_set.csv`) to RoleProfile seed keys once WP-08 authors them; a one-line rewrite in `docs/methods/scripts/wp10_signals.py#role` and `wp10_web.py`.

## Consequences if not accepted

The rule cannot run in CI; reviewers must apply it by hand and the single-vendor test is unenforceable. The interim notation encoding keeps the data but is a misuse of `notation` (aliases) that should not survive to `candidate`.
