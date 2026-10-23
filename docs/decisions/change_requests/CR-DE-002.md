# CR-DE-002: Vocabulary gaps in `vocab/identifiers.yaml`, `vocab/mapping_predicates.yaml`, `vocab/crafts.yaml` and `vocab/state_class_fields.yaml`

- **From:** DE (A1), WP-01 · **To:** CA (decider; vocabulary owner) · **Date:** 2026-10-23 · **Type:** X (L0 vocabulary) · **SemVer impact:** minor (new terms); patch for the quoting fix
- **Affects:** `vocab/identifiers.yaml#types`, `vocab/mapping_predicates.yaml#mapping_sets`, `vocab/crafts.yaml#task_attributes.formation_dependency`, `vocab/state_class_fields.yaml`, `vocab/exposure_instrument_v2.yaml#v1_migration_mapping.flags`
- **Evidence label:** J (DE; found by generating the schema enumerations from all 19 vocabulary files)

## Problems

1. **No TYPE prefix for three entity kinds.** `vocab/competency_types.yaml#entity_kinds` lists `WatchItem`, `SeriesRecord` and `StateClassRecord`, but `vocab/identifiers.yaml#types` gives them no prefix, so they cannot be minted. Interim: `scripts/mint_id.py` refuses them and `validate_v2.py` reports `E-ID-PREFIX` if one carries an `emst:` ID; they keep `seed:` keys.
2. **X12 missing from the mapping-set registry.** ADR-0022 §2 and SPEC §15 define X12 (TX-A and AI practice → DOL AI Literacy Framework, TEN 07-25); `vocab/mapping_predicates.yaml#mapping_sets` stops at X11. The generated `v_mappingSetId` enumeration therefore lacks X12.
3. **YAML 1.1 booleans.** `vocab/crafts.yaml` writes `formation_dependency: values: [yes, partial, no]` unquoted. Standard YAML 1.1 loaders (PyYAML's default, most HR tooling) read `yes`/`no` as booleans, so the code list becomes `[true, 'partial', false]`. Interim: the EMST loader (`scripts/emstlib.py`) uses YAML 1.2 boolean rules, so the schema enum is `[yes, partial, no]`, and every writer quotes `'yes'`/`'no'`.
4. **State class fields not machine-readable.** `supervisory_status` is `format: enum` but its values appear only in prose ("Non-supervisory, lead, supervisor, manager, executive"); `appointment_route` mixes values with prose (`non-competitive (NY HELPS)`). The generator can only enforce enumerations written as `a|b|c`.
5. **v1 recovery flags.** The v1 tag migration recovered values from working records (Task 10 dual-primary register; D7 lens table). Exposure flags exist in the codebook; there is no flag for "recovered from a working record", so the migration records it in `v1Values.recovered_from` and `derivedFrom.relation = recovered`.

## Proposed change

1. Add `{prefix: WCH, entity: WatchItem}`, `{prefix: SER, entity: SeriesRecord}`, `{prefix: SCR, entity: StateClassRecord}` to `vocab/identifiers.yaml#types` and extend the ID regex alternation accordingly.
2. Add `{id: X12, name: "TX-A and AI practice → DOL AI Literacy Framework (TEN 07-25)", object_source_version: "TEN 07-25 (2026-02-13)"}` to `mapping_sets`.
3. Quote the values: `values: ['yes', partial, 'no']`.
4. Give `supervisory_status` and `appointment_route` pipe-separated machine values (e.g. `non-supervisory|lead|supervisor|manager|executive`), with prose in `definition`.
5. Optional: add `recovered_from_working_record` to `v1_migration_mapping.flags` if the CA wants recovery visible as a flag.

## Consequences if not accepted

Watch items, OPM series and state class records stay on seed keys through rc.1 (they can still be released only if a policy allows seed-keyed records, which the release gate does not); X12 validates only as an unregistered set; any non-EMST YAML consumer misreads `formation_dependency`.
