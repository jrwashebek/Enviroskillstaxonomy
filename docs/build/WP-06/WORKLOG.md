# WP-06 worklog — wave-1 module editorial sections (A6 DB)

- **Agent:** `emstagent:db-agent@wp-06` (model `claude-opus-5-5`, prompt `wp06-module-authoring@1`) · **Started:** 2026-10-23T14:00Z
- **Lane:** module-targeted rows of `candidate_disposition.csv` and `v1_disposition.csv` for the nine wave-1 namespaces (`water`, `waterq`, `air`, `waste`, `envhealth`, `hazards`, `forest`, `wildlife`, `parks`); the two early drafts named in the dispositions (FH-C03 in `worklands`; IA-CC-05 homed in `extract` with its public-lands enactment and tasks in `forest`); module enactments of core competencies; one module brief per section in `docs/modules/`.
- **Status of everything here:** agent-drafted. `validationStatus: draft`, `reviewStatus: unreviewed`, content evidence label J (basis in each record's `editorialNote`), ratings evidence label S. Nothing here is SME agreement, Delphi retention or job-analysis confirmation. No partner is committed; every partner named is a *candidate*.

## Method and files

| File | What it is |
|---|---|
| `src/<namespace>.yaml` | Authoring sources, one per section (+ `src/zz_late_enactments.yaml` for enactments of core records authored concurrently by FC, DC, SC and WP-07). |
| `build_wp06.py` | Writes one record per file under `data/v2/modules/<ns>/{competencies,tasks,indicators,enactments}/`; edits v1 seeds in place (keeps `id`, `notation`, v1 facets, `v1Seed`; `carried` → `rewritten`); idempotent; a full run removes records no source defines any more. |
| `credential_gates.yaml` | Task → Credential links into WP-07's register (`data/v2/registers/credentials/`), merged by the generator. |
| `rate_crafts.py`, `ratings/` | Three blind craft-rating passes (see below); prompts, key maps and raw answers kept for audit. |
| `coverage.py` → `three_module_coverage.csv` | Generated three-module coverage of every live core competency. |
| `build_briefs.py` → `docs/modules/MOD-*.md` | One-page briefs; record lists generated from the data. |
| `counts.py`, `manifest.csv` | Every record WP-06 wrote; all counts are generated from these. |

Re-run order: `build_wp06.py` → `rate_crafts.py write` (only if task text changed: then re-run `rate_crafts.py run` first) → `coverage.py` → `build_briefs.py` → `scripts/migrate_v1.py --x1-only` → `scripts/validate_v2.py`.

## Log

- 14:00 Read S1 brief, build plan §1 and WP-06, AUTHORING_GUIDE, ADR-0003, ADR-0018, vocab (modules, subsectors, proficiency levels, work functions), dispositions, `mvp_role_set.csv`, V3 verification facts and corrections, IO lint rules and craft codebook, DB Phase 2 files. Baseline validator: 0 errors.
- 14:10–14:25 Generator written; sources authored and validated in priority order: `water` (R24, R25), `envhealth` (R26), `waste` (R27, R29), `air` (R28), `hazards` (R30), `forest` (R14, R06–R08, R18), `wildlife` (R15, R16), `waterq`, `parks`, `worklands` early draft.
- v1 6.7.5 split: its three task seeds moved from `core/tasks/` to `modules/air/tasks/` and re-pointed to DB-C13 / DB-C14 (core may not depend on module records). X1 regenerated (`migrate_v1.py --x1-only`): 6.7.5 → DB-C13, DB-C14, SL-C02; 4.4.4 → DB-C20 (+ FC's core part, HAZWOPER); 6.6.2 → DB-C47; 4.2.3 → v1-4.3.2; 3.7.4 → v1-3.7.1.
- 14:25 Read `RULINGS_FOR_DE.md` (ADR-0029) when the validator briefly failed mid-update: no WP-06 change needed (WP-06 never writes `Competency.enactments`; `distinguishingAttribute` is already on every indicator above the lowest level).
- 14:28–14:40 Three blind craft-rating passes run and written (`data/v2/assessments/emst-craft@0.1/wp06-db-pass{1,2,3}.jsonl`). Rater notes matching the Tribal-hold trigger list were dropped from the records (one pass-2 note on an international-agreement task); raw answers stay in `ratings/` for audit.
- 14:45 WP-07's credential register appeared; credential gates wired onto tasks (`credential_gates.yaml`). Task text unchanged, so ratings stay current.
- Final: validator 0 errors overall; WP-06 records carry only `W-REF-PENDING` (enactments and one task pointing at planned core targets DB-C05 and PS-C09, not yet authored). IO lint in release mode: 0 failing; only A03 (info) hits.

## Craft ratings (ADR-0005; codebook `emst-craft-codebook@1.0.0-draft`)

Each pass is a separate `claude -p` session (model `claude-opus-5-5`) started in an empty scratch directory with tools disabled. The rater saw the full IO codebook and the task statements only, in a pass-specific shuffled order under pass-specific keys; never the competency, module, v1 code or another pass's rating. Rater IDs `emstagent:db-craft-rater-{1,2,3}@wp06`; `raterType: llm`; evidence label S. **Limits:** the three passes are the same model family with the same codebook, so they are not independent in the human-rater sense; they are agent draft evidence only and are inadmissible for the display gate (CR-IO-002). Agreement is computed by CI, not here. No task was returned as "cannot code".

## Decisions taken while authoring (for CA / IO review)

1. Competency titles follow the dispositions but drop compound verbs and programme names where the typing lint requires (e.g. DB-C08 "Develop pollutant load allocations…" with *TMDL development* as `altLabel`; DB-C43 without the programme acronym).
2. Indicators exist at every level in each `levelSpan` (2 per level), so spans were set to the levels authored (L1–L3, L1–L4 or L2–L4).
3. Production vs review-and-defence split (G-2) added wherever AI or automation compresses production: report certification (DB-C01, DB-C02), permit drafting (SL-C02 air and water enactments), AI-drafted analyses (DB-C20, DB-C40, DB-C41, PS-C13), automated detections (FS-C05, SL-C06, LC-C-07, DB-C09).
4. Credential gates are Credential links (`credentialGates`) plus `reproductionRegime.credentialGate` and `signOffAuthority`, never levels (T-8). `kind: preferred` wherever the gate is jurisdiction-dependent or an employer preference [J].
5. v1 seeds keep `v1Seed` for reviewers (stripped from releases); every published level has v2 indicators.
6. IA-CC-05 is homed in `extract` (wave 2) with its tasks in `forest`, per ADR-0018 s.4 and the disposition ("wave 1 drafting via MOD-11 enactment").
7. Protect suggestions (v1 1.3.2, 4.3.2) are noted for the Editorial Board, not set (ADR-0015).

## Not authored (and why)

- **TN-C06** (forest): held under ADR-0007 §D; TN drafts only.
- **Wave-2/3 module rows** (MOD-05, -07a/b, -08, -10, -13, -14 except FH-C03, -16, -17, -18): out of wave-1 scope; their v1 seeds stay as migrated.
- **Actor enactment notes TN requested** for v1 1.3.5, 1.4.5, 4.3.1, 4.3.5: held.

## Enactments to wire when the core record exists (not yet authored in `data/v2/core/`)

| Core competency | Modules to enact | Note |
|---|---|---|
| DB-C05 asset management | water, forest, parks | enactments already written; `W-REF-PENDING` until authored |
| PS-C09 GHG inventories | air, waste, water | enactments already written; `W-REF-PENDING` |
| DB-C06 operational-technology security | water, air, waste | not written (would dangle) |
| DB-C42 environmental response within incident command | hazards, forest, envhealth | not written |
| PS-C15 land rights, rights-of-way and realty | forest (public-lands realty), water (utility easements), parks | not written (ADR-0018 s.4) |
| SL-C12 financial assistance to local governments | water (revolving funds), waste, hazards | not written |
| DB-C21 emerging contaminants across media | water, waste, envhealth, air | not written |

## Open issues and change requests

- **CR-DB-001** (`docs/decisions/change_requests/CR-DB-001.md`): no CI check or exception register for the three-module rule; Enactment has no `subsectors` field; DB-C53 placed both core (ADR-0018 §2) and MOD-18 (disposition); cross-module early-draft pattern; wildlife harvest-management gap (scope question); L5 instruments missing for module regimes (to WP-10); credential gates (to WP-07).
- **DE tests:** `tests/test_migration.py` (`test_222_competency_and_666_task_seeds`, `test_migration_is_deterministic_and_current`, `test_cld_prior_evidence…`, `test_seed_records_validate_without_errors`) assume v1 seeds keep `provenance.method: v1-migration`; every authoring WP's in-place rewrite (as the AUTHORING_GUIDE instructs) breaks them. Not a data error; DE to adapt the tests.
- **FC lane:** the three v1 4.4.4 task seeds in `core/tasks/` still support the superseded 4.4.4 seed; they belong to FC's core successor (`seed:v1-4.4.4-A`), not to DB-C20.

## Hand-offs

**WP-08 (role profiles).** Module competencies by role (enactment IDs are `seed:ena-<competency>-<module>`):

| Role | Module competencies | Key enactments |
|---|---|---|
| R24 Drinking water programme analyst | SL-C06 | sc-c14, sl-c03, fc-c16, db-c29, sl-c10, sc-c12 (`water`) |
| R25 Water and wastewater operator | DB-C01, DB-C02 (collection/stormwater variant: v1-4.7.3) | db-c03, fc-c24, db-c05, dc-cand-04 (`water`) |
| R26 Environmental health specialist | SL-C07, LC-C-07, DB-C39 | sl-c04, fc-c16, fc-c24, 1.4.3, db-c29, fc-c31 (`envhealth`) |
| R27 Remediation project manager | DB-C20, DB-C19, PS-C13 (private variant), DB-C18 (federal facility) | 6.7.1, fc-c16, fc-c24, sl-c04, db-c29 (`waste`) |
| R28 Air quality specialist | DB-C13, DB-C14, DB-C15 | sl-c02, sl-c03, sl-c04, sc-c14, ps-c09, db-c52, dc-cand-12 (`air`) |
| R29 Solid waste and materials specialist | DB-C16, DB-C17, SL-C14, v1-3.7.1, v1-3.7.2, v1-3.7.5 | sl-c10, ps-c09, db-c03 (`waste`) |
| R30 Hazard mitigation and floodplain manager | DB-C40, DB-C43, DB-C41, FC-C25 | sl-c08, db-c50, 1.5.2, db-c29 (`hazards`) |
| R14 Forester | v1-1.3.1 … v1-1.3.5, FH-C02, PS-C23 (private), v1-4.3.3 | 1.4.3, 6.2.3, sl-c08, fh-c01, sc-c08 (`forest`) |
| R06 / R07 / R08 Fire | v1-4.3.1, v1-4.3.2, v1-4.3.3, v1-4.3.4, v1-4.3.5, FS-C05 (R08) | db-c15, fc-c14, dc-cand-12 (`forest`) |
| R18 Rangeland management specialist | IA-CC-01, FC-C08 | sl-c02 (resource-manager variant) (`forest`) |
| R15 Wildlife biologist | FC-C15, v1-6.5.5 (federal) — harvest management gap, see CR-DB-001 §5 | 1.4.3, fh-c01, fc-c03, dc-cand-03 (`wildlife`) |
| R16 Fisheries and aquatic biologist | v1-1.4.5, DB-C49, FH-C10, FC-C15 | fc-c12, fc-c11 (`wildlife`) |
| R17 Hydrologist | DB-C10, DB-C11, FC-C07 | 4.1.3, fc-c01 (`waterq`) |
| R21 Park ranger | v1-5.5.1, IA-CC-02, IA-CC-03, IA-CC-07 | 5.1.3, fc-c26, fc-c21 (`parks`) |
| R19 Soil conservationist | FH-C03 (`worklands`, early draft) | — |
| R11 / R12 / R23 permit writer, inspector, enforcement | — | `seed:ena-sl-c02-*`, `seed:ena-sl-c03-*`, `seed:ena-sl-c04-*` (air, waterq, waste, water, envhealth, forest) |

Federal-to-state and regulator ↔ regulated mobility pairs are carried by mirror enactments: SL-C06 ↔ `ena-db-c26-water`; SL-C02/SL-C03 air ↔ `ena-db-c26-air`; DB-C18 ↔ `ena-sl-c03-waste`.

**WP-12 (explorer).** Module records are editorial sections, not stewarded modules, and stay out of default HR views (ADR-0018 consequences). Enactments point at their competency; the inverse list is computed (`inverse-links@1.1.0`, ADR-0029). Lifecycle-`emerging` module competencies (DB-C17, DB-C39, FC-C25, FS-C05) carry `reviewBy` and belong in the what's-coming view. IA-CC-05 is an early draft in `extract` (wave 2). Briefs: `docs/modules/MOD-*.md`.
