# WP-03 worklog: competency authoring, Field Craft (A3 FC)

- **Agent:** `emstagent:fc-agent@wp-03` (model `claude-opus-5-5`; prompts `prompts/wp03-authoring.md@1`, `prompts/wp03-craft-rating.md@1`). Raters: `emstagent:fc-rater-1@wp03` … `-3@wp03`.
- **Status of everything here:** agent-drafted. `status: draft`, `validationStatus: draft`, `reviewStatus: unreviewed`. Content evidence label J (basis in each `editorialNote`), E only where sources are cited (FC-C14, FC-C14 ignition task, v1 4.2.5). Ratings: `raterType: llm`, evidence label S. **Nothing here is SME agreement, Delphi retention or job-analysis confirmation.**
- **Counts:** generated, never typed: `counts.json` and `competency_index.csv` (by `reports.py`), `manifest.csv` (by `build_wp03.py`), rating consistency printed by `rating/to_records.py`.

## Method and reproducibility

- Content is written as compact specs in `src/g1_assess.py` … `src/g6_enactments.py` and turned into one-record-per-file YAML by `build_wp03.py` (library `src/wp03lib.py`; credential links `src/cred_links.py`). v1 seeds are edited in place: id, notation, legacy facets and lineage are kept (`derivedFrom` `carried` → `rewritten`; split and merge lineage added); `v1Seed` is removed once every published level has v2 indicators. Original seeds are cached in `.seed_cache/` so regeneration never loses v1 fields.
- G-2 split: every task carries its split role in `editorialNote` (execution to protocol; adaptation or decision in place; specification, review or defence; design; formation of others).
- Credential gates (T-8): tasks link records in `data/v2/registers/credentials/` (WP-07) where they exist; otherwise `reproductionRegime.credentialGate` holds the author's draft level and the note says the gate is not yet in the register.
- Craft ratings: `rating/make_frames.py` builds blind frames (random unit code + task text only; no competency, domain, module, v1 code or prior label; Tribal-trigger text excluded); three passes in different orders (`rating/pass1-3.txt`); `rating/to_records.py` writes `data/v2/assessments/emst-craft@0.1/wp03-fc-pass{1,2,3}.jsonl`, pinned to task text hashes. **Caveat:** the three passes are one model in one session that also wrote the tasks. Agreement among them is run-to-run consistency only (LLM-coder gate level G0, `validation/protocol_llm_coder_gate.md` §1.1). They must not be shown to human raters during a reliability study or pooled into any gate statistic.

## Log

- 13:40 Read S1 brief, build plan §1 and WP-03, AUTHORING_GUIDE, SPEC §5/§7/§8/§10, ADR-0003/0004/0005/0025, vocab (crafts, proficiency, work functions, lifecycle), IO lint rules and craft codebook, LLM-coder gate, FC Phase 2 folder. Baseline validator 0 errors.
- 14:05 Generator and groups 1–2 written (field assessment; field side of data and AI). Lint fixes (B07 compounds, PUB-08 mode, B05/B04 verb starts).
- 14:10 **Lane collision resolved:** WP-04 (DC, owner of the D2 rows) had already re-pointed and rewritten v1 2.3.1 T1–T3 and 2.3.4 T1–T3. WP-03 dropped those files from its specs and wrote replacement FC tasks instead (`seed:fc-sensor-siting-bias`, `seed:fc-rec-*`). WP-07 rewrote v1 4.4.1 T3 for TX-C, so WP-03 no longer re-points 4.4.1 T2/T3. Content review of the DC versions as target owner: acceptable; suggest WP-04 reword `seed:v1-2.3.4-T3` ("train field teams … mobile forms") because it is L4 tool fluency.
- 14:40 Groups 3–6 written (build and implement; safety and operations; people and land; FC enactment of DC-CAND-13). Credential gates linked once the WP-07 register appeared.
- 15:30 Three rating passes; records written; X1 regenerated (`scripts/migrate_v1.py --x1-only`). Validator: 0 errors repo-wide; 0 warnings and 0 IO-lint hits on WP-03 records (only `I-STALE-ASSESSMENT` on v1 prior-evidence tags pinned to old v1 task text, as designed).
- 16:00 Reports, CR-FC-001, CR-FC-002, handoffs.

## What WP-03 authored (see `competency_index.csv`)

- **v1 seeds rewritten or carried:** 1.1.2, 1.1.5, 1.4.3, 1.7.1, 4.1.1, 4.1.2, 4.1.3, 4.1.4, 4.2.1, 4.2.2, 4.2.4, 4.2.5, 4.4.2, 4.4.5, 4.5.1, 4.5.2, 4.5.5.
- **Split targets:** `seed:v1-4.4.1-A` (field risk; absorbs FC-C19, FC-C27), `seed:v1-4.4.4-A` (hazardous, industrial and energized sites; absorbs PS-C24), `seed:v1-4.5.3-A` (field vehicles).
- **Candidates (core):** FC-C01, C02, C03, C11, C12, C14, C16, C18, C20, C21, C22, C23, C24, C26, C28, C31; FS-C04; DB-C03 (FC primary by the merged candidate file).
- **FC enactment of DC-CAND-13** (`core/enactments/seed-ena-dc-cand-13-fc.yaml`): ecological plausibility and field ground truth; tasks `seed:fc-txa-*` (in `additionalTasks`); indicator variants `seed:ind-fcena-dc-cand-13-*` at L1–L3 (listed only on the Enactment; DC-CAND-13 declares its own `levels[]`).
- **Re-pointed only (text left to the owner):** v1 1.2.1 T2/T3 → `seed:v1-1.2.2`; v1 1.6.2 T2/T3 → `seed:v1-1.6.1`.
- **Coverage:** `disposition_coverage.csv` maps every FC-lane row of both disposition files to a WP-03 record, a merge into one, or another lane (CR or handoff). No row is unaccounted for.

## Protect suggestions for the Editorial Board (not set; SPEC §10.3 needs two of PC-1 severe failure, PC-2 reproduction ≥ 5 years, PC-3 supply fragile in ≥ 2 scenarios)

| Record | PC-1 | PC-2 | PC-3 | Basis [label] |
|---|---|---|---|---|
| `seed:v1-1.4.3` species identification | misidentified listed or invasive species: legal duty, irreversible harm | regional multi-taxon expertise across seasons | FS stress test fragile; entry seasonal roles cut | [J]; FS `scenario_stress_test_v1.csv` (v1-derived, prior evidence); [E: V1-04] |
| `seed:v1-4.1.3` water-quality field work | compliance and drinking-water decisions rest on field samples | — | FS: high reproduction risk in two scenarios | [J]; FS stress test |
| `seed:v1-4.4.1-A` field risk management | life safety | — | crew supervisors shrink with seasonal and probationary cuts | [J]; [E: FC-013, FC-014] |
| `seed:v1-4.5.2` chainsaw and power equipment | life safety | — | FS fragile; trail and sawyer capacity lost | [E: FC-015]; FS stress test |
| `seed:FC-C20` crew leadership and judgment transfer | — | crew-lead formation spans several seasons | entry paths cut now | [J]; [E: V1-04, FC-016] |
| `seed:FC-C22` site history and reference conditions | — | place knowledge built over many seasons | lost when long-tenure staff leave | [J]; [E: V1-01] |
| `seed:FC-C02` ground truth (consider) | decisions on unvalidated remote or AI products (broken trust) | — | counter-signal: validation absorbed into vendor services | [J]; mvp_role_set R05 counter-signal |
| `seed:v1-4.2.5` trails (consider) | — | rock and drainage work learned over seasons | trail miles maintained fell 22% in 2025 | [E: FC-015] |
| module `seed:v1-4.3.2` prescribed fire (WP-06 lane) | life safety, escapes | burn-boss formation is multi-year | FS stress test | [J]; plan example |
| module `seed:v1-1.3.2` forest mensuration (WP-06 lane) | — | inventory QA expertise | FS fragile | [J]; plan example |

## Handoffs

- **WP-06 (DB): field enactments of core FC competencies in wave-1 modules:** `handoff_wp06_field_enactments.csv` (generated by `handoff_wp06.py`; the `already_enacted` column is computed, so rerun it). It proposes at least three module enactments for each WP-03 competency that has none yet, plus gaps in the fire records: credential gates on 4.3.1 and 4.3.2 tasks, a contingency-declaration (rare-event) task, an L1 holding-crew anchor, and a contributing link from `seed:db-4.3.2-t4` to `seed:FC-C14`. Module enactments WP-06 already wrote for FC-C01, C02, C03, C11, C12, C14, C16, C21, C24, C26, C31, DB-C03, 1.4.3, 4.1.3 and 4.2.2 were not touched. **CR-FC-002:** DB-C19 and DB-C13 field content from merged FC-C05 and FC-C17; FC-C29 → PS-C06 deferred to wave 3; v1 4.5.3 T1 and 4.6.2 T2/T3 must move into `modules/worklands/tasks/` (they cannot be re-pointed from `core/`, so `W-SUPERSEDED-TARGET` remains on them until then).
- **WP-05 (SC): CR-FC-001.** Field-performance additions to SL-C03 from merged FC-C04 (beyond-checklist detection, adaptation task, inspector's own field measurements).
- **WP-04 (DC):** (1) `seed:v1-4.5.4-T3` (process UAS imagery) is kept as a *contributing* task of FC-C14; please link it as primary to the DC remote-sensing practice; (2) reword `seed:v1-2.3.4-T3` (tool fluency); (3) the FC enactment of DC-CAND-13 is in place; please keep its indicators out of DC-CAND-13 `levels[]`; (4) L4 seeds needed: field identification apps, mobile data collection, positioning receivers, sondes and loggers, acoustic recorders and camera traps, uncrewed aircraft and ignition systems, precision-agriculture systems.
- **WP-07 (IO/LC): credentials** not yet in the register, needed as gates (draft levels are already on the tasks): sawyer certification (chainsaw and crosscut); small-boat operator certification; off-highway vehicle and all-terrain vehicle authorization; electrofishing safety qualification; interagency aviation training for aerial surveys; agency uncrewed-aircraft pilot qualification for public-aircraft operations; tree risk assessment qualification; utility line-clearance qualification. Also `seed:v1-4.4.1-T2` still supports the superseded v1 4.4.1 (TX-C successor's task).
- **WP-08 (FH): `handoff_wp08_task_bundles.csv`.** Suggested task bundles for P1 roles R01–R09, with `suggest_formationTask` for every entry-level role in COR-1 and COR-2 (R01, R02, R03, R06) and `suggest_neededAtEntry`. These are [S] suggestions computed by an explicit rule (stated in each row). WP-08 and IO set the flags; an LLM is never the sole coder of `neededAtEntry` or `critical`.
- **WP-12 (CP):** FC craft ratings are G0. Render them as "assessment pending", never as a blend. `fieldDependency` and `formationDependency` are author attributes (not α-gated tags) and can be shown labelled "editorial draft".
- **TN (G-TN):** no WP-03 record carries Tribal content or triggers. Flags for TN to decide: a possible held enactment of FC-C21 (working on the land) and FC-C22 (site history) with knowledge holders in sovereign communities; consent rules for reference collections and sound and image libraries (1.4.3 L4 indicator b); cultural fire (TN-C06) left untouched; FC-C13 (cultural resource field survey, MOD-16, wave 2) not authored.
- **DE:** `tests/test_migration.py::test_222_competency_and_666_task_seeds`, `…deterministic_and_current` and `…cld_prior_evidence…` assume no v1 seed has been authored, so every authoring WP breaks them (edit-in-place is the AUTHORING_GUIDE rule). `test_schema_build` fails until the schema is regenerated per RULINGS_FOR_DE.

## Not finished or open

- Credential gates for the gates missing from the register (listed above) are recorded only as draft levels.
- No KnowledgeStatements authored (optional; awareness bundles for field safety would help LC).
- FS-C06's programme-governance content sits in FC-C14 L4. L5 is not defined, pending SME confirmation of strategic demand (ADR-0004 §4).
- `typicalTimeToLevel` and publication-rule checks are deliberately empty: they need job-analysis and Delphi data.
- The 0/1/2 scale is provisional until IO's craft-scale pilot. Human blind re-rating of the ~60-task field set (P-FC-16) is still needed to test the "H only from FC/SC" artifact.
