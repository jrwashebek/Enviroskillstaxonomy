# CR-DE-004: Three points from implementing ADR-0029 (seed-v1 stubs, evidence-rule reason codes, rule-file pointers)

- **From:** DE (A1), WP-01 · **To:** CA (decider) · **Date:** 2026-10-23 · **Type:** C (clarification of ADR-0029 §1.3, §8.3) · **SemVer impact:** none
- **Affects:** `schema/src/emst.schema.src.yaml#RecordBase`; `scripts/validate_v2.py` (`E-SEED-CANDIDATE`); `vocab/rules/change-indicator@1.0.0.yaml#reason_codes`, `#implementation`; `vocab/rules/display-gate@1.0.0.yaml` / `validation/display_gates.yaml#agreement_result_schema.ruleVersion`
- **Evidence label:** E (the repository state as of 2026-10-23); J for the interim choices

## Problems and interim choices

1. **ADR-0029 §1.3 as written invalidates 118 migration stubs.** The ruling forbids `validationStatus: seed-v1` with `status` ∈ {candidate, published, deprecated, superseded, withdrawn}. WP-02 wrote every v1 item whose decision is merge, split, move-to-tools, retire or hold as a seed-keyed stub with `status: superseded` or `withdrawn` and `validationStatus: seed-v1`, which records accurately that the content was never validated. §3 says the migration output does not change. The two rulings conflict for these 118 records. No one minted them and they never reach a release, because the release profile ships minted IDs only.
   **Interim (built):** the rule applies to candidate, published and deprecated in every case, and to superseded and withdrawn only when the record has a minted `emst:` ID. Seed-keyed superseded or withdrawn v1 stubs stay valid. `mint_id.py promote` refuses every seed-v1 record. A test (`tests/test_schema_rulings.py::test_seed_v1_never_reaches_candidate`) pins the behaviour.
   **Proposed:** confirm the interim. Alternatively, rule that the stubs take a different `validationStatus`; that changes migration output and needs a vocabulary value.
2. **Two reason codes outside `change-indicator@1.0.0.yaml#reason_codes`.** The port (`scripts/rules/change_indicator.py`) needs to say why a record that targets the indicator did not count:
   - `ER-0-NOT-ACTIVE`: a watch signal, under the rule's `active_signals` clause;
   - `ER-0-ORGANIZATION-TARGET`: under `organization_targets`.

   **Proposed:** add both to `reason_codes`.
3. **Rule-file pointers.**
   - `change-indicator@1.0.0.yaml#implementation` still reads "(to be ported by DE …)". The port is at that path. Proposed: drop the parenthesis. LM can retire `docs/methods/ci/` once CA confirms; the tests now live in `tests/test_evidence_rule.py` with `tests/fixtures/evidence_rule_cases.yaml`.
   - `validation/reliability.py` stamps agreement results with `ruleVersion: 1.0.0-draft`. The emitter (`scripts/rules/agreement.py`) overwrites the stamp with the active `display-gate` version (1.0.0), so every stamp resolves to a rule file. Proposed: IO aligns `display_gates.yaml#agreement_result_schema.ruleVersion`.
   - Rule files name `scripts/build_release.py#Release.views`. The class is `Builder`, and `Release` is now an alias, so the pointer resolves. No change is needed unless CA prefers the real name.

## Consequences if not accepted

For item 1, 118 records fail validation, or the migration output must change. For items 2 and 3, tests accept the two extra codes as documented additions, and the stale rule-file wording remains.

## CA ruling

- **Ruling:** **accept 1–3** · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** ADR-0030 §1.1 (amends ADR-0029 §1 item 3), SPEC §4 (draft.3), `vocab/rules/*.yaml`, DECISION_LOG `CR-DE-004`
- **Implementation:** DE per `RULINGS_FOR_DE.md` §13; LM and IO as below.

1. **Seed-v1 stubs: interim confirmed.** `E-SEED-CANDIDATE` applies to `candidate`, `published` and `deprecated` in every case, and to `superseded` and `withdrawn` only when the record carries a minted `emst:` ID. A seed-keyed v1 stub that is `superseded` or `withdrawn` keeps `validationStatus: seed-v1`. That value is accurate: the content was never validated, and the stub never reaches a release (the release profile ships minted IDs only). No new vocabulary value; migration output unchanged. `mint_id.py promote` keeps refusing every seed-v1 record. ADR-0029 §1 item 3 is amended to this wording.
2. **Reason codes: accepted.** The CA has added `ER-0-NOT-ACTIVE` (watch signal; `active_signals` clause) and `ER-0-ORGANIZATION-TARGET` (`organization_targets` clause) to `change-indicator@1.0.0.yaml#reason_codes`. Both name exclusions the definition already makes, so outputs do not change and the version stays 1.0.0 (recorded in its `changeNote`; no release has been built under it). Tests treat them as ordinary codes, not documented extras.
3. **Pointers.**
   - The CA has dropped "(to be ported by DE …)" from `change-indicator@1.0.0.yaml#implementation`.
   - The CA has changed every `scripts/build_release.py#Release.views` pointer to the real name, `#Builder.views`. DE keeps the `Release = Builder` alias until rc.1 is tagged, then may remove it.
   - **LM** deletes `docs/methods/ci/` now: the port passes in `tests/test_evidence_rule.py`.
   - **IO** sets `validation/display_gates.yaml#agreement_result_schema.ruleVersion` to `1.0.0`. DE's emitter keeps overwriting the stamp as a guard.
