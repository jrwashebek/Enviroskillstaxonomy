# Data engineering for EMST v2: repository, data model, releases and migration

**Role:** Data Engineer & Repository Steward (DE) · **Phase:** 1 · **Date:** 2026-10-23
**Companion documents:**
- [`docs/audit/data-audit.md`](../../audit/data-audit.md): the v1 data-quality audit (every number cited here is there).
- [`data/v1_baseline/`](../../../data/v1_baseline/README.md): the normalized, tested v1 baseline.
- `proposed/`: a draft record schema, worked examples and CI/release workflows.

Evidence labels: **[E]** evidence with a source ID in `sources.csv` (DE-001…DE-021 are v1 artifacts, DE-022+ external), **[J]** my judgment and its basis, **[S]** speculation and what would settle it.

**A note on sources.** The shared web-search budget ran out early in this session, and a direct fetch of the BLS SOC page was not permitted. External practice I could read first-hand:
- SemVer 2.0.0 (DE-023), SSSOM (DE-024), Frictionless Table Schema (DE-025) and CFF (DE-026), fetched from their GitHub sources;
- OSMT (DE-027) and the CTDL-ASN vocabulary (DE-028), read from clones another team agent had made;
- the LMPs repository (DE-022).

ESCO, CASE, SKOS, PROV-O and the SOC manual are cited from prior knowledge and marked `unverified`. IA (standards) and LM/FH (SOC) should confirm the points that rest on them.

---

## 1. Summary

The v1 database is not a source of truth in any operational sense. It is five hand-edited copies of one spreadsheet lineage. Its authority claim points at a superseded copy. It has no validation, so four boolean spellings and undocumented codes entered freely. Its derived fields (modal exposure, CLD, family counts) can't be reproduced from its own inputs. And a third of its assessment content was lost in the original import from text. [E: data-audit §§1, 4–6]

None of these failures came from bad analysis. All of them came from the medium. v2 fixes the medium:

1. **Text records in git as the single source of truth.** Authored entities are one reviewed file each. High-volume machine records (assessments, mappings, signals) are line-oriented files. Every record is validated against a JSON Schema and cross-record rules in CI, and nothing reaches `main` without passing.
2. **Store atoms, compute everything else.** Authored text, atomic ratings (with rater, date, instrument and the hash of the text rated), links, events and mappings are stored. Every summary, including modal exposure, CLD, stability/change indicators, craft blends, breadth and dashboard counts, is computed at build time by versioned rules. The schema cannot represent a summary, so a summary cannot drift.
3. **Opaque persistent IDs, entity-level lifecycle, semantic versioning of the taxonomy, and change records as data.** Release notes, the change log and the README status are generated.
4. **Crosswalks as SSSOM-style mapping sets** with predicate, justification, confidence, author/reviewer and target version. This includes the v1→v2 crosswalk, which must account for every v1 competency and task.
5. **v1 provenance on every migrated record** through a `derived_from` object that resolves to a hash-pinned row of `data/v1_baseline/`. v1 tags migrate only as **prior evidence**, never as v2 values.

Most of this is borrowed from the LMPs pipeline, which already does provenance per record, schema validation, CI, tagged releases, gold-set evaluation, a generated README status and a CC0/Apache split (DE-022). What LMPs lacks, and a taxonomy needs, is identity management over time: IDs that outlive edits, deprecation and supersession, crosswalks with confidence, and multi-rater assessment data (§4).

Phase 1 work is in the repo and reproducible:
- `scripts/extract_v1.py`, `scripts/v1_source_text.py`, `scripts/v1_exposure_records.py`, `scripts/diff_v1_versions.py`, `scripts/audit_v1.py`;
- the baseline tables;
- 65 passing tests (`tests/test_v1_baseline.py`, `tests/test_proposed_schema.py`).

---

## 2. What v1 teaches the repository design

Each failure class found in the audit, the mechanism that let it happen, and the control v2 needs:

| v1 failure (audit §) | Mechanism | v2 control |
|---|---|---|
| Five database copies; authority claim points to a superseded copy (§1) | Files passed between sessions; no diff, no history | One git repository; releases are tags; lineage is `git log` |
| `Yes/No` vs `TRUE/FALSE`; `Highest`/`Ungraded` severities; free-text provenance labels (§4) | No validation on write | JSON Schema with enumerations generated from governed vocabulary files; CI blocks the merge |
| Stored modal, count and flag fields disagree with their inputs (§§1.6, 5) | Derived values typed by hand next to inputs | Derived values cannot be stored (schema `additionalProperties: false`); computed in the build |
| 2,104 indicators truncated; D5 content mis-parsed (§6) | Fixed-width columns; one-off import with no reconciliation | Arrays instead of numbered columns; every import ships with a reconciliation test against its source |
| Exposure codes assigned to different text than the database shows (§7) | Classification sessions worked from paraphrased text; codes copied back by position | Each assessment stores the SHA-256 of the exact statement rated; build flags stale assessments |
| Dashboards, data dictionary and change log stale (§13) | Hand-maintained summaries | All generated from data in CI |
| Lost values (dual-primary stages, D7.2 lenses) that exist only in prose records (§§1.4, 5) | Working records and database are separate systems | The record is the working record: assessments carry their rationale |
| Single rater, no agreement data (§14) | No place to store a second rating | Assessment records are per rater; agreement is computed and published |

[J] The common thread is that v1 kept *conclusions* and threw away the *observations* behind them. v2's data model should be observation-first.

---

## 3. What to borrow from the LMPs pipeline

All rows rest on [E: DE-022] (files named in the second column) and are judged [J].

| LMPs pattern | Where in LMPs | Adopt? | Adaptation for EMST |
|---|---|---|---|
| **Provenance on every record**: source URL, SHA-256, retrieval time, extraction method, confidence, reviewer | README "What is in each plan record"; `source.json` per document | **Yes** | A `provenance` object on every record (method, created_by/at, evidence label, source_ids, reviewers, confidence, tool version). Add `derived_from` for v1 lineage. Rater identity is pseudonymous (§12). |
| **JSON Schema validation** of every output record | `schema/openlmp.schema.json` (draft 2020-12); `test_schema_and_ceq_export` | **Yes** | `schema/emst.schema.json` for source records, not only outputs. Enumerations are generated from `vocab/`. Draft in `proposed/emst-record.schema.json`. |
| **CI tests on push/PR** | `.github/workflows/ci.yml` (pytest on code/schema paths) | **Yes, extended** | Also validates all data, checks the v1 baseline still rebuilds byte-identically, and checks generated docs/views are current (`proposed/workflows/ci.yml`) |
| **Tagged release workflow** building bundles and uploading with `gh` | `.github/workflows/release.yml` (tags `v*`, `data-*`) | **Yes** | Release on `vX.Y.Z` and `-rc.N`. Release notes generated from change records. SSSOM, SKOS, CSV, JSON-LD, CASE exports. Zenodo DOI. |
| **Gold-set evaluation** by independent annotators, with inter-annotator agreement | `evaluation/gold/GUIDELINES.md`, `evaluation/SCORES.md` (137 components, κ = 0.939 on 7 double-annotated pages) | **Yes, central** | Gold sets for exposure assessments, craft weights, task–competency links and NLP mappings. Publish agreement (κ/α) per instrument version. Fail CI when an automated tagger drops below the threshold IO sets. |
| **Generated README status block** | `scripts/update_readme_status.py`, `<!-- status:start -->` | **Yes** | Counts by layer, module, status and release, plus agreement scores. No hand-typed counts anywhere. |
| **Rule-only baseline kept beside enriched output** | `components.rule.json` | **Yes, as a principle** | Keep the v1 baseline frozen and comparable, so v2 improvements are measured against it |
| **Task/result files any annotator can answer** (LLM, person, chat), with annotator provenance header | `annotations/tasks|results`, `PROMPT-enrich.md`, `check_results.py` | **Yes** | The natural format for SME review packets, Delphi rounds and LLM-assisted drafting. Every answer carries `{annotator, date, prompt_version}`. |
| **Stage stamps / idempotent reruns** | `openlmp/stamps.py` | Partly | Builds are small, so full rebuilds are fine. Keep code-revision stamps on computed views. |
| **Hold-back list for sensitive content** | `registry/_holdback.yaml`; governance "Never published" | **Yes** | For Tribal and CARE-governed material (TN's protocol), personal data, and third-party copyrighted text |
| **Licence split**: Apache-2.0 code; CC0-1.0 schema, vocabularies, docs, data | `LICENSE`, `LICENSE-DATA` | **Yes**, subject to §12 caveats | |
| **CITATION.cff** | repo root | Yes | Plus Zenodo DOI per release |
| **Governance**: `standard-change` issues; 30-day comment period and migration script for breaking changes; semver with version on every record | `docs/governance.md`; `SPEC.md` §7 | **Yes, extended** | Entity-level lifecycle and supersession (§8); decisions as ADRs referenced by change records |
| **Bot commits pipeline outputs straight to `main`** | `.github/workflows/pipeline.yml` | **No** | A taxonomy is a reviewed standard. Automated jobs (signal ingestion, NLP mapping) open PRs; humans merge. |
| Run requests via a control file | `control/run-request.yaml` | Later | Useful for the signal-ingestion pipeline (IA/LM), not for the taxonomy core |

---

## 4. What v2 needs that LMPs doesn't have

LMPs converts documents that have their own identity (a plan is a plan). A taxonomy *is* the identity system, and its concepts change. [J]

1. **Entity-level identity and lifecycle.**
   - LMPs versions its schema (`openlmp_version`); EMST must version concepts.
   - Each record carries status (`draft → candidate → published → deprecated/superseded/withdrawn`), `version_introduced`, `version_changed`, and `supersedes`/`superseded_by`.
   - OSMT uses a comparable lifecycle for skill descriptors (Draft, Workspace, Published, Archived, Unarchived, Deleted) [E: DE-027]. Mine adds "superseded" because a taxonomy must point users to the successor.
2. **Semantic versioning of the taxonomy itself**, separate from schema and code versions, with taxonomy-specific bump rules (§8). SemVer's contract is defined for a "public API" [E: DE-023]. Here the public API is the set of published IDs and their meanings.
3. **Crosswalks with confidence and justification.**
   - SSSOM makes confidence (0–1, "the creator's confidence … that the mapping record is correct") and a controlled `mapping_justification` (e.g. `semapv:ManualMappingCuration`, `semapv:LexicalMatching`, `semapv:LLMBasedMatching`) first-class, alongside author, reviewer and mapping-set version [E: DE-024].
   - CTDL-ASN supplies alignment predicates whose definitions suit competency crosswalks: `ceasn:exactAlignment` ("coextensive"), `broadAlignment`, `narrowAlignment`, `majorAlignment`, `minorAlignment` [E: DE-028].
   - v1's family→SOC sheet had neither confidence nor justification beyond a 3-level label [E: DE-001].
4. **Deprecation and supersession records**, and **change records as data** that generate release notes and the change log. v1's change log was good in design (entry type, scope, before/after, rationale) but hand-kept and incomplete [E: DE-009].
5. **Multi-rater assessment data**, with agreement computed per instrument version and a hash link to the exact text assessed (§6.3).
6. **Computed views** with versioned rules (§7).
7. **Module namespaces and stewardship**, if the CA's federated option holds: CODEOWNERS per `modules/<slug>/`, module-level validation, and a core schema that modules cannot override.
8. **Release candidates as frozen review packets** for Delphi and the NGO pilot, so reviewers comment on an immutable artifact.
9. **Upstream tracking**: crosswalk sets record the version of O*NET, ESCO, SOC or OPM they target. A target release triggers a re-validation job.

---

## 5. Proposed repository layout

```
emst/
├── README.md                 status block generated from data (LMPs pattern)
├── CHARTER.md  TEAM_BRIEF.md  CITATION.cff  CONTRIBUTING.md  CODEOWNERS
├── LICENSE (Apache-2.0, code)   LICENSE-DATA (CC0-1.0, data/schema/vocab/docs; see §12)
├── pyproject.toml            pinned deps: openpyxl, jsonschema, pyyaml, scikit-learn (audit only), pytest
├── vocab/                    L0 reference vocabularies, one YAML per scheme (SKOS-exportable):
│   ├── crafts.yaml  levels.yaml  sector_actors.yaml  work_functions.yaml  subsectors.yaml
│   ├── exposure_instrument/<version>.yaml
│   ├── provenance_methods.yaml  statuses.yaml  change_types.yaml
│   └── rules/<rule-id>@<version>.yaml         (versioned rules for computed views, §7)
├── data/
│   ├── v1_baseline/          frozen normalized v1 (this phase); hash-pinned; never edited
│   └── v2/
│       ├── core/
│       │   ├── competencies/<id>.yaml   one authored record per file
│       │   ├── tasks/<id>.yaml
│       │   └── knowledge/<id>.yaml
│       ├── roles/<id>.yaml
│       ├── modules/<slug>/…   same structure, namespaced IDs, own CODEOWNERS
│       ├── tools/tools.jsonl            fast layer
│       ├── assessments/<instrument>/<batch>.jsonl   one rating per rater per task
│       ├── signals/<yyyy>/<source>.jsonl            dated change events
│       ├── crosswalks/<target>/<target-version>.sssom.tsv (+ .yml metadata)
│       │   └── emst-v1/emst-v1_to_v2.sssom.tsv      complete accounting of v1
│       ├── ids/registry.csv              every minted ID; append-only
│       └── changes/<release>.jsonl       change records (data) → release notes
├── schema/                   emst.schema.json, generated/enums.schema.json, tableschema/*.json, emst.context.jsonld
├── scripts/                  extract_v1, migrate_v1, mint_ids, validate_v2, build_views, export, release_notes
├── tests/
├── evaluation/               gold/, scores.json, SCORES.md, thresholds.yaml
├── docs/
│   ├── decisions/ADR-NNNN-*.md
│   ├── standard/SPEC.md  data-dictionary.md (generated)  governance.md
│   ├── audit/  research/  package/
├── legacy/v1/                frozen snapshot (MANIFEST with hashes)
├── dist/                     git-ignored build output; attached to releases
└── .github/workflows/        ci.yml, release.yml (drafts in docs/research/data-engineering/proposed/workflows/)
```

**Format trade-off [J].**
- **YAML, one file per authored entity.** SMEs and reviewers read diffs per competency, merge conflicts stay local, and CODEOWNERS can assign module reviewers.
- **JSONL or TSV for machine-volume records.** Assessments, signals and mappings run to thousands of lines and are produced by scripts.
- **The cost** is two serializations. Mitigation: one loader, one schema, and CSV/JSON-LD exports generated for consumers.

---

## 6. Enforcing typing, vocabularies and provenance (schema design)

### 6.1 Four validation layers

| Layer | Tool | Catches |
|---|---|---|
| 1. Record schema | JSON Schema 2020-12 (`Draft202012Validator`) [E: DE-034] | wrong types (booleans as `"Yes"`), unknown enumeration values, missing required provenance, forbidden fields (any stored summary), malformed IDs, `superseded` without successor, `E` label without a source |
| 2. Generated enumerations | `scripts/build_schema_enums.py` reads `vocab/*.yaml` → `schema/generated/enums.schema.json`; CI `--check` | vocabulary drift: a new code must enter via a reviewed vocab PR, and the schema follows automatically |
| 3. Cross-record rules | `scripts/validate_v2.py` | referential integrity (task_ids, superseded_by and tool_ids exist); ID registry append-only and no reuse; assessment `task_text_sha256` equals the task's current hash (else **stale**); every `E` source ID resolves in a `sources.csv`; every v1 key appears in the v1→v2 crosswalk; no module redefines a core ID |
| 4. Tabular exports | Frictionless Table Schema `primaryKey` / `foreignKeys` [E: DE-025] | integrity of published CSVs for consumers who never see the JSON |

### 6.2 Demonstration

`proposed/emst-record.schema.json` is a working draft covering competency, task, exposure assessment, mapping and change record. `proposed/examples.json` holds five records migrated from v1 3.1.1. It shows the title/description split, three indicators recovered from the source text beyond the import cap, the task with its real text hash, the v1 exposure call as prior evidence, the v1→v2 mapping row and the change record.

`tests/test_proposed_schema.py` validates the examples. It then reproduces each v1 drift class and confirms the schema rejects it:

| v1 drift class | Rejected |
|---|---|
| `Yes`/`No` boolean | yes |
| `Highest` severity | yes |
| stored modal or count field | yes |
| H task with an AI vector | yes |
| v1-migrated record without `derived_from` | yes |
| `E` label without a source | yes |
| free-text provenance method | yes |
| assessment without a text hash | yes |
| `superseded` without a successor | yes |
| a v1 code used as an ID | yes |

All 18 tests pass. [E: test run 2026-10-23]

**What a schema cannot enforce [J]:**
- whether a classification is *right* (gold sets and agreement, §11);
- whether an "editorial" edit changed meaning (reviewer attestation in the change record, §8);
- whether two records are duplicates (embedding screen plus SME, IA's lane).

Layer 3 and review handle these, not layer 1.

### 6.3 The text-hash link (prevents v1's worst exposure defect)

Every task stores `text_sha256` of its normalized statement, recomputed by the build. Every assessment stores `task_text_sha256`, the hash of the statement the rater actually saw.

If they differ, the build marks the assessment **stale**:
- it is excluded from computed views;
- it is listed in the release report until it is re-rated or a reviewer re-attests it (change type `editorial` with an attestation).

Under this rule v1's D1 and D3 records (82 and 98 tasks classified against different text) could not have been merged silently. [J]

---

## 7. Stored vs computed

The principle: **store observations and decisions; compute summaries.** Rules for computed views live in `vocab/rules/<id>@<version>.yaml`. `scripts/build_views.py` writes them to `dist/views/` with `computed_by: {rule_id, rule_version, build_commit}`. CI recomputes and compares. The schema forbids these fields in source data.

| Item (CA §4 list and v1 fields) | v2 treatment | Inputs | Notes |
|---|---|---|---|
| Competency-level exposure summary (v1 "modal") | **Computed** | task assessments (non-stale, per rater) → consensus per task → competency distribution | Publish the **distribution** (counts of A/Ac/H/S/V) and a label from one published rule, e.g. majority, else "mixed". v1's undocumented rule is irreproducible (63/222 mismatches). |
| CLD indicator (task, competency, pathway) | **Computed** | task consensus automation type + career-ladder position; role pathway links for the pathway level | v1 rule "P-position Ac/S/V" breaks in 11 of 222 stored flags. Severity becomes a per-task rating, not a stored competency label. |
| Stability tier / change indicators | **Computed** | assessments + dated driver events (signals layer) + rule | v1 tier rule held (C05 = 0). It moved 37 competencies in one rule change, which is exactly why it should be a versioned computation. |
| Breadth (v1 "Zero Core", Foundational Prep) | **Computed** | family/role relevance ratings | |
| Family relevance counts (Core/Supporting counts) | **Computed** | stored per-competency × family (or role) relevance ratings | Ratings are atoms with rater and date. Counts are views (v1 D7 counts wrong in 7/7). |
| Craft blend (competency, role) | **Computed** | task craft weights × task importance in role | CA hypothesis; weights stored per rater |
| Reform-flag count | **Computed** | driver-event links | |
| Dashboard, README and documentation counts | **Computed** | everything | Generated at release |
| Data dictionary | **Generated** | schema + vocab | |
| Labels, definitions, task statements, indicators, level anchors | **Stored** (authored) | — | with provenance and lifecycle |
| Ratings: exposure, craft weights, relevance, lenses | **Stored** (atomic, per rater) | — | instrument version, date, rationale, text hash, confidence |
| Links: task↔competency, role↔task (importance, time share), task↔tool | **Stored** | — | |
| Change signals and driver events | **Stored** (dated) | — | source, jurisdiction, status |
| Mappings / crosswalks | **Stored** (SSSOM rows) | — | target version, confidence, justification |
| Change records, decisions (ADR), ID registry | **Stored** | — | |

---

## 8. Identifiers, versioning and deprecation

**ID minting rules** (format placeholder until IA's DP-9 decision):

1. **Opaque, type-prefixed, never reused, never re-meant.** Example `emst:c-7K3QX9`, with an optional module namespace `emst:water/t-…`. The body is 6 random Crockford base32 characters (about 10⁹ space, no I/L/O/U). No hierarchy in the ID: v1's D.SA.N codes broke when Domain 7 was inserted, and the source narrative still cites a stale numbering [E: DE-011].
2. **One writer.** `scripts/mint_ids.py` appends to `data/v2/ids/registry.csv` (id, type, module, minted_on, minted_by, status, superseded_by, first_release). CI rejects edits other than status transitions.
3. **Stable only from `published`.** Draft and candidate records may change freely. Once published, a change of meaning requires a **new ID**, and the old record becomes `superseded` with `superseded_by`.
4. **Splits and merges** mint new IDs. Each old ID points to all successors; the change record carries the relation.
5. **Retired content** keeps its ID in the registry (status `withdrawn`) so old references resolve to an explanation, not a 404.
6. **v1 codes are aliases, never IDs.** They appear as `legacy_codes: ["v1:3.1.1"]` and in the v1→v2 crosswalk.

**Taxonomy semantic versioning** (adapting SemVer [E: DE-023]; public API = published IDs + their meanings + the schema):

| Bump | When |
|---|---|
| **MAJOR** | A published ID withdrawn without successor; a change to the meaning of an L0 vocabulary term or of the level scale; removal or rename of a schema field |
| **MINOR** | New entities, modules or vocabulary terms; deprecations or supersessions **with** successors; new optional fields |
| **PATCH** | Editorial fixes attested as meaning-preserving; corrections to provenance or metadata |

- Every change record declares `semver_impact`. The release check fails if the tag is smaller than the largest declared impact.
- **Independent cadences, pinned together.** Crosswalk sets carry their own `mapping_set_version` and target version [E: DE-024], tools and signals publish dated snapshots, and each taxonomy release pins the snapshot versions it ships with. [J] This matches the CA's layered cadence hypothesis without needing seven semver streams.

---

## 9. Release process

1. **Change** by PR only, using templates `standard-change`, `content-change` and `mapping-change`. Each PR adds change records referencing an ADR or decision point. Module PRs need the module steward's approval (CODEOWNERS); core PRs need the editors.
2. **CI gates** (`proposed/workflows/ci.yml`):
   - baseline rebuild check;
   - enumerations current;
   - full validation;
   - views and docs current;
   - tests;
   - gold-set thresholds for any automated tagger.
3. **Release candidate** `vX.Y.Z-rc.N`: a frozen review packet (exports plus generated SME/Delphi task files in the LMPs annotation format) with a 30-day comment window for MAJOR, matching LMPs governance [E: DE-022].
4. **Release** `vX.Y.Z` (`proposed/workflows/release.yml`):
   - validate;
   - semver check;
   - build views;
   - export JSON-LD, CSV with Table Schema, SKOS concept schemes, SSSOM crosswalks and a CASE package (IA owns the mappings);
   - generate release notes from change records;
   - `SHA256SUMS`;
   - GitHub release;
   - Zenodo DOI;
   - CITATION.cff updated.
5. **After release**: the README status block and the dashboard data regenerate. Crosswalk re-validation jobs watch upstream releases.

---

## 10. Migration plan v1 → v2

| Phase | What | Output | Status |
|---|---|---|---|
| **M0 Freeze and extract** | Archive v1 verbatim with hashes. Extract a normalized baseline. Diff all versions. Reconcile against the source text and the working records. Audit. | `legacy/v1/`, `data/v1_baseline/` (+`source_text/`, `qa/`), 47 baseline tests | **Done** |
| **M1 Seed** | `scripts/migrate_v1.py` turns the baseline into **draft** v2 records in `data/v2/seed/`. Content comes from the source text where it is more complete (D5 Knowledge/Application, all 6,484 source indicators, the 19 title splits). v1 tags become **prior-evidence assessments** (rater `v1-analyst-01`, `rater_confidence` from the D2 codes, D1/D3 marked text-misaligned, low confidence). Dual-primary stages and D7.2 lenses are recovered from the Task 10 and D7 records. | Draft records with `derived_from`; no published IDs | After CA structure decision |
| **M2 Decide** | The CA's carry/change/retire register (`docs/audit/v1_carry_forward_register.csv`) becomes machine-readable at row level: `migration_decisions.csv` (v1_key, decision, target, ADR). The migrate script applies it and generates `emst-v1_to_v2.sssom.tsv`. | v1→v2 crosswalk; **completeness test: all 222 competencies and 666 tasks accounted for** | Phase 3 |
| **M3 Re-derive** | Exposure, craft weights and relevance re-rated against v2 text by several raters (IO/LM protocols). Gold sets built. Agreement published. | Assessment batches; `evaluation/SCORES.md` | Phase 3–4 |
| **M4 Candidate** | Mint IDs for records going to `candidate`. Release `2.0.0-rc.1` for the NGO pilot and Delphi as a frozen packet. | rc release | |
| **M5 Publish** | `2.0.0` | release + DOI | |

**How v1 codes map forward.** Every v1 competency and task gets one or more rows in `crosswalks/emst-v1/emst-v1_to_v2.sssom.tsv`:

| v1 outcome | Predicate | Notes |
|---|---|---|
| Carried or rewritten | `emst:replacedBy` → v2 ID | `skos:exactMatch` only if text is carried verbatim |
| Split | several `emst:replacedBy` rows | |
| Merged | several subjects → one object | |
| Retired | `emst:retiredWithoutReplacement` | object `sssom:NoTermFound` |

All rows use `mapping_justification: semapv:ManualMappingCuration` and record the ADR. [J] A CI test enforces that nothing in v1 disappears without a recorded decision.

---

## 11. Quality gates beyond the schema

- **Reconciliation tests for every import.** The v1 extract is checked against the source text: 645/645 tasks, 1,075/1,075 sector notes, and pinned counts of the known defects. Any future bulk import (O*NET tasks, OPM series, plan requirements) ships with the same kind of test.
- **Determinism.** Builds are byte-reproducible from pinned inputs (`extract_v1.py --check`).
- **Gold sets and agreement (LMPs pattern).** For each rated layer, a stratified sample (I suggest 10% of tasks, at least 60, stratified by module and craft) is double-coded blind. Publish Cohen's κ or Krippendorff's α per dimension per instrument version. IO sets the thresholds. Automated or LLM-assisted taggers are scored against the gold set before their outputs can merge. [J] v1's only reliability evidence is self-agreement on re-work: D2 database vs D2 records agree on all five dimensions for 37/105 tasks and on automation type for 77/105 [E: data-audit §7]. That is a warning, not a measurement.
- **Pinned counts.** Release notes state counts that tests assert, so a silent change fails.

---

## 12. Licensing, sensitive data and third-party content

- **Licences:** Apache-2.0 for code; CC0-1.0 for schema, vocabularies, documentation and EMST-authored data, as in LMPs [E: DE-022].
- **Caveats** [J; licence facts unverified this session, so IA/LM/AS should confirm]:
  1. CC0 means anyone can fork and rebrand. AS should confirm that is acceptable for a standard whose value depends on one authoritative version. The usual answer is CC0 data plus a trademark or "official release" convention.
  2. Crosswalk files that embed upstream text (O*NET task statements, ESCO labels) may carry attribution licences. Store upstream **IDs only** in CC0 files, and put any upstream text in separately licensed, attributed files.
  3. v1 content is the project lead's own work and needs an explicit CC0 dedication from them.
- **Third-party copyrighted material** stays out of the repo. The legacy capture already excludes the SAF Accreditation Handbook (git-ignored `reference_only/`) [E: DE-021]. This is the precedent.
- **Sensitive and governed data:**
  - a hold-back list for Tribal or CARE-governed content (TN's protocol decides what may enter at all);
  - no person-level data in the public repo;
  - rater IDs pseudonymous, with the identity map held outside the repo;
  - Delphi responses published as aggregates only (CP's lane).

---

## 13. Answers to CA architecture questions

*(docs/research/chief-architect/architecture_hypotheses.md §6, DE)*

**Q1. Can the schema enforce the entity typing, controlled vocabularies and provenance rules in the audit, so that v1's vocabulary drift cannot recur?**

**Yes, for everything that is syntactic or structural, and that covers every drift class the audit found. No, for semantic correctness, which needs agreement data and review.** [E for the demonstration; J for the boundary]

- **Typing.** One schema with a discriminated `type`: competency, task, knowledge, role, tool, exposure assessment, signal, mapping, change record. Each type has `additionalProperties: false`, so a record cannot carry fields of another type or a stored summary. The draft covers five of these types and passes 18 tests, including ten negative cases that each reproduce a v1 defect (§6.2).
- **Vocabularies.**
  - Every coded field's enumeration is generated from `vocab/*.yaml`. A new value (v1's `Highest`, `Ungraded`, `Yes`) therefore needs a reviewed vocabulary PR. It cannot appear in data first.
  - Booleans are JSON booleans.
  - Code fields are strings with patterns, never spreadsheet floats.
  - Conditional rules encode instrument logic (H ⇒ vector none and horizon N; `superseded` ⇒ `superseded_by`).
- **Provenance.**
  - `provenance` is required on every record, with method from a controlled list, evidence label, and source IDs required when the label is E.
  - `derived_from` is required when the method is `v1_migration`.
  - Assessments must carry rater, date, instrument version and the hash of the text rated.
- **Cross-record rules** that a JSON Schema cannot express (referential integrity, append-only ID registry, stale assessments, sources resolving, v1 completeness) run in `validate_v2.py` in CI (§6.1).
- **Out of reach of any schema:** whether a classification is right, whether an edit changed meaning, and whether two records duplicate each other. These are handled by gold sets and agreement (§11), change-record attestation (§8) and an embedding duplicate screen with SME review (IA).

**Q2. Which fields are stored and which are computed views? Propose build-time computation for the §4 list.**

See the table in §7. Briefly:

- **Stored:** authored text; atomic ratings (per rater: exposure, craft weights, family or role relevance, lenses); links (task↔competency, role↔task with importance, task↔tool); dated events; mappings; decisions; the ID registry.
- **Computed:** every item on your §4 list (stability and change indicators, breadth or zero-Core, family relevance counts, competency-level exposure summaries, CLD at task, competency and pathway level, craft blends, dashboard counts), plus everything v1 stored as a derived column (modal fields, reform count, family counts, CLD flag, tier).
- **How they are computed:**
  1. Rules are versioned YAML in `vocab/rules/`.
  2. `scripts/build_views.py` computes them at build time into `dist/views/`.
  3. Each view row records `rule_id`, `rule_version` and `build_commit`.
  4. CI recomputes and compares.
  5. Releases ship the views as CSV/JSON for spreadsheet users.
  6. The schema forbids them in source records.

  Changing a rule (as v1 did when "Ac tasks now trigger Transition" moved 37 competencies) becomes a reviewed, versioned change whose effect the release notes report automatically.
- **Exposure summaries:** publish the per-competency **distribution** rather than a single modal label, or the label plus the distribution under one published rule. The audit shows the single label hid inconsistent rules.
- **Pathway-level CLD** needs role pathway links and task career positions. Those are inputs you already plan in L3 and L5.

**Q3. How will v1 provenance (v1 code, sheet, row, version, provenance code) be carried on every migrated record?**

Through three mechanisms, all already exercised in `proposed/examples.json`:

1. **`derived_from[]` on every migrated record** (required by the schema when `method = v1_migration`):

   | Field | Content |
   |---|---|
   | `v1_key` | e.g. `v1:3.1.1:T2`; resolves to a row in `data/v1_baseline/` |
   | `v1_table`, `v1_sheet`, `v1_row`, `v1_fields` | location in the v1 workbook |
   | `v1_workbook_sha256` | the v1 *version*: copyB's hash, pinned in `BUILD_INFO.json` |
   | `v1_exposure_provenance` | session_direct / reconstructed_d2 / d6_exposure_file_reconciled_2026_03 / … |
   | `source_text_line` | when content was recovered from the source text |
   | `relation` | carried / rewritten / split_from / merged_from / recovered / prior_evidence / reference_only |

   Indicators recovered from the source text carry their own `derived_from` at indicator level.
2. **`legacy_codes`** aliases (`v1:3.1.1`) on the v2 entity, for lookup and display.
3. **The v1→v2 SSSOM crosswalk.** It accounts for every v1 competency and task, including retirements, with the ADR for each decision. A CI test fails if any v1 key is unaccounted for.

Earlier v1 versions are reachable too. `data/v1_baseline/version_diffs.csv` records every cell that changed along the five-workbook lineage, keyed by the same v1 code and column. A v2 record can therefore be traced to copyB, and from copyB to any prior value. The per-task working records that justified v1 exposure calls (786 rows in `exposure_sources.csv`, with rationale and D2 confidence codes) attach to the prior-evidence assessments.

---

## 14. Proposals

- **P-DE-01 Adopt copyB as the v1 baseline.** Treat `data/v1_baseline/` as the only v1 input to v2 work: frozen, hash-pinned, tested. Other roles should cite `v1:` keys, not spreadsheet cells. [E: data-audit §1]
- **P-DE-02 Rank the source text above the database for v2 seed content.** This reverses v1's hierarchy for content, not tags. The source is complete where the database is not (D5 Knowledge/Application, 2,104 indicators) and identical where both exist. [E: data-audit §6]
- **P-DE-03 Migrate every v1 tag as prior evidence only.** These are assessment records with rater `v1-analyst-01`, low confidence and flags for known misalignment (D1 and D3 text, D2 divergence). No v1 tag becomes a v2 value without re-rating. [E: data-audit §7; J]
- **P-DE-04 Store atoms, compute summaries.** The schema forbids derived fields; versioned rules produce views at build (§7).
- **P-DE-05 Hash-link every assessment to the exact text rated.** Stale assessments are excluded from views until re-rated or re-attested (§6.3).
- **P-DE-06 Opaque persistent IDs with an append-only registry, entity lifecycle and supersession.** v1 codes are aliases only (§8). Format is subject to IA's DP-9.
- **P-DE-07 Semantic versioning of the taxonomy** with the bump rules in §8. Change records as data generate release notes. Crosswalk sets and fast layers are versioned independently and pinned per release.
- **P-DE-08 All crosswalks as SSSOM-style mapping sets** with confidence, justification, author/reviewer and target version, using SKOS and CTDL-ASN predicates. This includes the v1→v2 crosswalk with a completeness test.
- **P-DE-09 CI and release workflows as drafted in `proposed/workflows/`.** Bots open PRs and never push to `main`. Generated README status, data dictionary and dashboards.
- **P-DE-10 Gold sets and published agreement** for every rated layer and every automated tagger, following the LMPs evaluation pattern (§11).
- **P-DE-11 Licensing:** Apache-2.0 for code and CC0-1.0 for EMST-authored data, with upstream text kept out of CC0 files, a hold-back list for CARE-governed material, and pseudonymous raters (§12).
- **P-DE-12 Recover lost v1 values before seeding:** the 5 dual-primary second stages (Task 10 register), the D7.2 lens values (D7 record), and the D5 content and indicators (source text). [E: data-audit §§1.4, 5, 6]
- **P-DE-13 Retire from v1:**
  - the Workforce Signals sheet, Structure Summary, Profession Family View and Data Dictionary sheet (generate them instead);
  - all stored modal, count and flag columns;
  - Pre-Task 15A's before/after statistics;
  - hand-typed distribution numbers in v1 narratives (`v1_assessment.csv`).

---

## 15. Disagreements and trade-offs

1. **With v1's source-of-truth hierarchy** (database > source text, DE-012). For content I recommend the reverse (P-DE-02). Trade-off: the source text has stale cross-reference numbering and narrative content of uneven quality, so it must be parsed, which I have done and tested, and reviewed.
2. **Strict text-hash pinning vs editorial churn.** Pinning makes every typo fix stale its assessments. Mitigation: meaning-preserving edits can be re-attested by a reviewer instead of re-rated. The cost is reviewer time. The alternative, no pinning, is exactly how v1's D1/D3 misalignment happened.
3. **Computed vs stored for spreadsheet users.** Computing summaries prevents drift but makes source files less self-contained. Mitigation: release CSVs include all computed views, so nobody needs the source to get a number.
4. **With the LMPs bot-commits-to-main pattern.** Right for a document-conversion pipeline, wrong for a governed standard. Machine outputs (NLP mappings, signals) arrive as PRs.
5. **CC0 vs control.** CC0 maximizes adoption and interoperability, and it lets forks rebrand. I lean CC0 plus an "official release" convention. AS should weigh in.
6. **With the CA's federated option (C), on timing, not substance.** Namespaced module IDs must be settled (DP-9) **before** any ID is published. Changing the namespace scheme after the first release is a MAJOR bump for every module record. The data engineering for modules (CODEOWNERS, per-module validation) is cheap. The ID decision is not.
7. **Two serializations** (YAML for authored, JSONL/TSV for volume). Simpler would be one format. I judge reviewability of authored text worth the cost.

---

## 16. Issues outside my area that affect the vision

- **IO.** Proficiency text is formulaic. The Knowledge stem is fixed by level 88–98% of the time, and 77.6% of Expert Knowledge/Application statements are status or influence claims ("Shapes…", "Publishes influential…"). Expert indicators reward publishing and leading. That is a defensibility problem for hiring uses and an equity problem for practitioners who don't publish (Tribal, state, local, private field staff). [E: data-audit §8; J on consequences]
- **LM / FH.** The family→SOC crosswalk has suspect codes:
  - F10 → 19-1012, where Farm and Home Management Educators is 25-9021;
  - F12 → 33-1021, where Fire Inspectors is 33-2021;
  - implausible secondaries: Library Technicians for Environmental Education, Health Information Technologists for Environmental Health & Justice.

  It must not be used until re-derived. [J; SOC page not fetchable this session]
- **CA, LM, and the sister "Skills Taxonomy" research project.** v1 narrative statistics are stale: "9 confirmed S calls" is now 4, and the A/Ac/H/V shares have moved. Any literature produced from v1 should be checked against the baseline before it is cited. [E: data-audit §7]
- **IA.** TF-IDF finds 16 cross-area conceptual overlaps (e.g. drone operation 2.3.2/4.5.4, CBPR 5.6.5/6.7.3, conservation finance 3.4.2/6.6.4). This is a lower bound; an embedding screen should run before v2 content is frozen. [E: data-audit §11]
- **CM / FH.** The source text holds unmined role-profile material (example positions, pathway tables, job profiles with credentials and salary ranges). It is useful role-signal seed, but it uses stale skill-area numbering and a second, conflicting set of career-year bands. [E: DE-011]
- **TN / CP.** Rater pseudonymity, Delphi data handling and the hold-back mechanism need protocols before any external rater or Tribal content touches the repo.
- **AS: year five.** The pipeline uses only Python, standard libraries, JSON Schema and GitHub Actions. Releases archive to Zenodo, so a host change loses nothing. Whoever maintains it needs one data engineer-day a month, not a team. [J]

---

## 17. Open questions for the Chief Taxonomy Architect

1. Do you accept copyB as the v1 baseline, and **"v1 tags migrate as prior evidence only"** (P-DE-01, P-DE-03)?
2. Do you accept that for **content** the source text outranks the v1 database (P-DE-02)?
3. **DP-9 timing:** may I generate seed records with throwaway `seed:` keys now and mint persistent IDs only at `candidate`? That avoids publishing IDs before the namespace decision.
4. Should competency-level exposure be published as a **distribution** (my recommendation) or a single label under a published rule?
5. **Release model:** one taxonomy semver plus independently versioned crosswalk and signal snapshots pinned per release (my proposal), or a semver per layer?
6. Which **export formats** are required at 2.0.0 (JSON-LD, SKOS, CASE, CTDL, CSV)? This is IA's recommendation, your decision.
7. Is Delphi or SME response data in scope for the repository (aggregates only), or held elsewhere?

---

## Appendix: files produced in Phase 1 (DE)

| Path | What |
|---|---|
| `scripts/extract_v1.py` | v1 baseline extractor (deterministic; `--check`) |
| `scripts/v1_source_text.py` | parser for the source competency text |
| `scripts/v1_exposure_records.py` | parser for the per-domain exposure working records |
| `scripts/diff_v1_versions.py` | cell-level lineage diff of the five database workbooks |
| `scripts/audit_v1.py` | data-quality audit metrics |
| `data/v1_baseline/` | baseline tables, `source_text/`, `qa/`, `version_diffs.csv`, `BUILD_INFO.json`, `README.md` |
| `tests/test_v1_baseline.py` | 47 tests |
| `tests/test_proposed_schema.py` | 18 tests |
| `docs/audit/data-audit.md` | the audit |
| `docs/research/data-engineering/` | `report.md` (this file), `sources.csv`, `v1_assessment.csv`, `ecosystem.csv`, `proposed/` (schema, examples, workflows) |
