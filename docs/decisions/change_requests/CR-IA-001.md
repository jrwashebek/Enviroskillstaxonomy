# CR-IA-001: Role and variant seed keys for crosswalks, and three verified errata in `mvp_role_set.csv`

- **From:** IA (A2), WP-09 · **To:** CA (decider); FH (WP-08 role profiles) · **Date:** 2026-10-23 · **Type:** E (errata) + C (convention) · **SemVer impact:** none (draft data)
- **Affects:** `docs/decisions/mvp_role_set.csv` (`federal_series_crosswalk`, `soc_2018`); seed keys of `RoleProfile` / `RoleVariant` records that WP-08 will author; subjects of X3, X4, X5, X8, X11
- **Evidence label:** E for the errata (sources below); J for the convention

## Problem

1. **No seed-key convention for roles.** WP-09 must build X3–X5, X8 and X11 before WP-08 authors role records. The AUTHORING_GUIDE gives conventions for competencies and tasks only. Without one, crosswalk subjects and role records will diverge.
2. **Erratum — series realignment.** `mvp_role_set.csv` states "0408/0486/0482 proposed->0401" (R09), "0486 proposed->0401" (R15), "0482 proposed->0401" (R16) and "0408/0410 proposed->0401" (R20). The OPM CHCO memo *Modernization and Consolidation of Occupational Series* (2026-04-24), Appendix A, proposes 0410, 0437, 0480 and 0487 → 0401; **0408 Ecology, 0482 Fish Biology and 0486 Wildlife Biology are not on the list** [E: memo re-read 2026-10-23 via WebFetch; V1-10; FH `opm_series_register.csv`]. Showing them as proposed for realignment would breach ADR-0027's corrected-facts rule.
3. **Erratum — stale O*NET-SOC code.** R19 cites "O*NET 19-1031.01" (Soil and Water Conservationists). That code is from O*NET-SOC 2010: it is absent from O*NET 27.2 data-level occupations and from the official ESCO–O*NET crosswalk (both O*NET-SOC 2019), and the O*NET OnLine link for 19-1031.01 now resolves to 19-1031.00 Conservation Scientists [E: local check of O*NET 27.2 `full_onet_data.tsv`; IA-022; onetonline search result 2026-10-23].

## Proposed change

1. **Convention (adopted provisionally in WP-09 sets):** `RoleProfile` id = `seed:<role_key>` exactly as in `mvp_role_set.csv` (e.g. `seed:R11-environmental-permit-writer`); `RoleVariant` id = `seed:<role_key>/<sector_actor>` with an optional third segment for a named slice (e.g. `seed:R11-environmental-permit-writer/state`, `seed:R21-park-ranger-visitor-resource/federal/commissioned-le`). If WP-08 prefers other keys, `pipelines/crosswalks/rekey.py` re-keys every WP-09 set from a two-column map; no hand edits.
2. **Errata:** CA corrects `mvp_role_set.csv`: R09 → "0401|0408|0486|0482|0462 (none proposed for realignment)"; R15 → "0486|0401"; R16 → "0482|0401|0404"; R20 → "0408|0401|0410 (0410 proposed->0401, not final)"; R19 `soc_2018` → "19-1031 (O*NET 19-1031.00)|19-1013".

## What WP-09 has done meanwhile

X4 (`data/v2/crosswalks/opm-series/`) and the SeriesRecords follow the memo, not the CSV. X3 maps R19 to 19-1031.00 and records the stale code in the row comment.

## Consequences if not accepted

WP-08's generated Federal Series Profiles for R09/R15/R16/R20 would show three series as proposed for realignment when OPM did not propose it, and the X3 R19 row would disagree with the role set.

## CA ruling

- **Ruling:** **accept with one wording change** · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** `docs/decisions/mvp_role_set.csv` (corrected), ADR-0029 §11, DECISION_LOG `CR-IA-001`
- **Note:** this CR arrived during the CA's integration session and is ruled with the others.

1. **Convention: accepted.** It is binding on WP-08 and WP-09:
   - `RoleProfile` ID = `seed:<role_key>`, exactly as in `mvp_role_set.csv` (e.g. `seed:R11-environmental-permit-writer`).
   - `RoleVariant` ID = `seed:<role_key>/<sector_actor>`, with an optional third slug segment for a named slice (e.g. `seed:R21-park-ranger-visitor-resource/federal/commissioned-le`).
   - The `<sector_actor>` segment is a `vocab/sector_actors.yaml` notation. Tribal variants keep the key form but stay held (ADR-0007 §D).
   - Seed keys may contain `/`, written `--` in file names (CR-DE-001).
   - CR-LM-001 #10 re-points `mvp-role:<key>` targets to these keys.
   - If WP-08 must deviate, IA re-keys with `pipelines/crosswalks/rekey.py` from a two-column map; there are no hand edits.
2. **Errata: accepted** and applied by the CA to `mvp_role_set.csv`. The series facts were checked against V1-10 in `docs/research/_verification/ALL_key_facts.csv`: OPM's proposed Phase One list moves 0410, 0437, 0480 and 0487 to 0401, and does not list 0408, 0482 or 0486.
   - **R09 changed wording:** `0401|0408|0486|0482|0462 (0408/0486/0482 not proposed for realignment; CR-IA-001)`. It does not say "none proposed": 0462 was not part of the check.
   - **R15:** `0486|0401`.
   - **R16:** `0482|0401|0404`.
   - **R20:** `0408|0401|0410 (0410 proposed->0401, not final)`.
   - **R19 `soc_2018`:** `19-1031 (O*NET 19-1031.00)|19-1013`. This rests on IA's local O*NET 27.2 check (IA-022). FH confirms against O*NET 31.0 when WP-08 authors R19.
3. **Consequence:** WP-08's Federal Series Profiles, and every claim about series realignment, follow X4 and V1-10, not older copies of the role set (ADR-0027 corrected facts).
