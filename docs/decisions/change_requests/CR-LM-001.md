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

## CA ruling

- **Ruling:** **accept with changes** (items 1–3 and 5–10 accepted, some with changes; item 4 split: occupation targets rejected in favour of X3 attachment, organization targets accepted with limits) · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** ADR-0028 (amendment), ADR-0029 §8, SPEC §5.14, §5.16, `vocab/change_types.yaml`, `vocab/driver_mechanisms.yaml`, `vocab/scenarios.yaml`, `vocab/rules/change-indicator@1.0.0.yaml`, DECISION_LOG `CR-LM-001`
- **Implementation:** DE (schema, validator, rule port, tests) per `RULINGS_FOR_DE.md` §8; LM (seed migration from `notation` to typed fields; re-targeting).

| # | Ruling |
|---|---|
| 1 | **Accept the typed fields.** `signalFamily` comes from `vocab/change_types.yaml#signal_families` (added). Each family carries `counts_toward`: `projection` and `workload` never count; `policy` counts toward **role-change** indicators only. This ratifies LM's reading of ADR-0028: §2's family list has no policy family, and §3 adds policy for role change only. `signalFamily` and `independenceKey` are MUST when `signalStatus = active`. `registeredDeployment` (boolean) is allowed only when `signalFamily = deployment`. `impact` is an integer 1–3 (FS protocol §6). `scenarioSignposts[]` items are `vocab:scenarios#SP-NN`. `pointsToward[]` items are a scenario ID (`SC1`…`SC4`) or an axis pole written `AX-n:<pole>` (e.g. `AX-1:thin-fragmented`). `measure.baseline{value, ci95, n, note}` and `measure.sensitivity{weighting, value, baselineValue}` are added to the closed `measure`. **Change:** the interim `EMST-*` notation entries must be moved into the typed fields before any signal reaches `candidate`; after that, `notation` must not carry an `EMST-` scheme (validator error at `candidate`). |
| 2 | **Accept with changes.** The provider table moves to `vocab/change_types.yaml#independence_keys` (LM steward), carried verbatim from `evidence_rule.py#PROVIDERS`. `independenceKey` is a slug, **not** a generated enumeration, because new datasets appear between vocabulary reviews. An **active** signal's key MUST be listed in the table (a human has then asserted its providers). A **watch** signal may use an unlisted key, which is treated as its own provider and produces a warning. Adding or changing a key is a vocabulary PR that LM stewards and the CA merges. |
| 3 | **Accept.** The CA wrote `vocab/rules/change-indicator@1.0.0.yaml` from `docs/methods/ci/evidence_rule.py` (versioned 1.0.0, like the other rules, not "1.0"). DE ports the code into `scripts/` and moves `test_evidence_rule.py` and `evidence_rule_cases.yaml` into `tests/`, keeping the regression that no seeded agent signal moves an indicator. LM stays the method owner and removes the `docs/methods/ci/` copies once the port passes. |
| 4 | **Occupation: rejected as a target type.** Occupation-grain signals (BLS, O*NET-SOC) attach to RoleProfile or RoleVariant through the X3 path, with `crosswalkPath` and `crosswalkMinMatchType`, as the seed already does. That keeps every target an EMST entity and keeps ER-3 (≥ close) applicable. **Organization: accepted with limits.** `targetType: organization` is allowed with `targetId` as an external code in a declared scheme, `opm-agency:<code>` or `census-gov:<id>`, so government employers only. It is never a Tribal government, Tribal organization or Tribal enterprise (ADR-0007 V3; CI error). It is never a named NGO or private firm: those enter only as aggregates by sector actor and industry. Measures with n < 5 are suppressed (ADR-0012). Organization-target signals feed staffing-outcome and entry-path context. They never move a role change indicator directly; series-level headcount reaches roles through X4, as now. The seed's signals that now target `vocab:sector_actors#federal` with an agency named in the label are re-targeted to the agency code where they concern one agency; they stay at sector-actor level where they concern the sector. |
| 5 | **Accept** `statusAfter` from a vocabulary: `vocab/driver_mechanisms.yaml#instrument_statuses`, with the twelve seeded values plus `under-review` (the status after a `submitted-for-review` event). |
| 6 | **Accept** `eventType: submitted-for-review` (submitted to a review body before issuance, e.g. OIRA, dated by that body's public record). The Section 106 rewrite and the FAA Part 108 final rule may now be recorded as events. They are not in force, so they never change an instrument's `currentStatus` to in-force. |
| 7 | **Accept** `instrumentType: agency-order` (Secretarial and agency orders). LM re-types SO 3448 and similar records. |
| 8 | **Accept.** The twelve signposts carry `SP-01`…`SP-12` in their current order (applied). SP-12 (Tribal co-stewardship agreements) carries `access: tribal-council-only`: readings may be recorded only as the Tribal Council decides, and CI quarantines any SP-12 reading as it does a `careFlag` signal. |
| 9 | **Ratified.** `scripts/validate_v2.py` already reads every `docs/**/sources.csv`, including `docs/methods/sources.csv`. |
| 10 | **Accept.** LM re-points `mvp-role:<key>` targets to RoleProfile seed keys once WP-08 has authored them. Until then the validator warns on `mvp-role:` targets, and the release gate excludes any record that still carries one: it points to a planning CSV, not a record. |
