# CR-CA-001: Lifecycle describes the work, not the record

- **From:** D-DATA (AI agent holding the CA, LM, IO and IA codes for the rc.1 fix pass) · **To:** CA (vocabulary steward of `vocab/lifecycle_states.yaml`), LM (evidence rule), IO (use tiers), FS (role lifecycle) · **Date:** 2026-10-25 · **Type:** vocabulary meaning and rule change · **SemVer impact:** MINOR for the vocabulary and schema (new `lifecycleBasis`; `watch` allowed on L1–L4); no ID changes
- **Affects:** `vocab/lifecycle_states.yaml`; `schema/src/emst.schema.src.yaml` (`LifecycleBasis`, `RecordBase.lifecycleBasis`); `vocab/rules/effective-use-tier@1.1.0.yaml` and `scripts/rules/effective_use_tier.py`; `scripts/rules/lifecycle_basis.py`; `scripts/validate_v2.py` (`E/W-LIFECYCLE-BASIS`); 440 records (`docs/build/rc1-fix/generated/lifecycle_changes.csv`)
- **Evidence label:** E for the defects (review M7, reproduced on the data); J for the new wording
- **Raised by:** `docs/review/data_method_review.md` M7; decided by the orchestrator in `docs/review/DATA_FIX_BRIEF.md` item 4
- **Ruling:** accepted in ADR-0032 §2

## Problem

`vocab/lifecycle_states.yaml` defined `established` as "Validated and stable", with `max_use_tier: select`. 198 of the 224 released competencies were `established`, and every one was `validationStatus: draft`, so the state claimed a validation that had not happened. In the other direction, records marked `proposed` or `emerging` did not meet the vocabulary's own entry thresholds ("≥ 3 independent signals of ≥ 2 types from ≥ 2 sector actors"; "≥ 10 postings or PDs across ≥ 2 actor types in 12 months, or a named operating programme"), and nothing checked them.

## Change

1. **Meaning.** The lifecycle state describes the work in the sector. `established`: "Long-standing work in the sector; EMST content validation is tracked separately in validationStatus." The superseded text is kept as `meaning_before_2026_10_25`.
2. **No lifecycle cap on use tier.** `max_use_tier` is removed from every state. effective-use-tier@1.1.0 replaces 1.0.0 (kept as superseded). The tier is capped by the ADR-0024 evidence, `validationStatus` and the display gate. `withdrawn`, `lapsed` and `merged` records have no tier.
3. **`watch` on L1–L4.** A record whose work is hypothesized but does not meet the `proposed` test is `watch`, with `reviewBy`.
4. **Machine-readable entry tests** (`entry_test.any_of`):
   - `proposed`: `signals` (≥ 3 independent signals under change-indicator@1.1.0 ER-1, one observation counted once, from ≥ 2 signal families and ≥ 2 sector actors) or `mandate` (an Instrument with an `effective` DriverEvent on or before the test date);
   - `emerging`: `postings-pds` (≥ 10 postings or PDs in 12 months across ≥ 2 actor types, from postings-pds signals over distinct observations) or `operating-programme` (a named programme with a resolving E-labelled source); roles also need ≥ 1 `feederRoles[]` entry.
5. **`lifecycleBasis`** is stored on each `proposed` or `emerging` record from `candidate`: `{testedFor, test, result, evidence[], mandate, operatingProgramme, counts{signals, distinctObservations, independentSignals, signalFamilies, sectorActors, postingsOrPds, actorTypes, feederRoles}, assessedOn, assessedBy, note}`. `result` must be `met`; the validator recomputes the counts from the evidence (`E-LIFECYCLE-BASIS`; a warning on drafts). Records moved to `watch` keep their `not-met` basis as the record of the test.

## Effect

No record met a test. 440 records moved from proposed or emerging to `watch`: 8 role profiles, 26 competencies, 44 role variants, 147 tasks, 201 indicators, 3 enactments and 11 pathways. No ID changes. The package and the release notes must stop describing these roles and competencies as emerging (`docs/build/rc1-fix/DATA_DONE.md`).
