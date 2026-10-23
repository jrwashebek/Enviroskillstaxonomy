# ADR-0010: Identifiers, canonical serialization and versioning — reconciling DE and IA

- **Decision point:** DP-9 part b (ID scheme; canonical serialization; versioning)
- **Status:** accepted
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** DE, IA, CP, AS, LC, TN
- **Related:** ADR-0009, ADR-0013 (licensing), ADR-0021 (entities, stored vs computed), ADR-0022 (crosswalks); SPEC §10–11

## Context — two drafts

| Aspect | DE (`docs/research/data-engineering/proposed/`) | IA (`data_model_v2.md`, `emst-v2.schema.json`, `emst.context.jsonld`) |
|---|---|---|
| Canonical store | Text records in git: **one YAML file per authored entity**; JSONL for assessments/signals/changes; SSSOM TSV for mappings | **JSON-LD bundle** (SKOS + PROV) is canonical; CSV, SKOS, CASE, CTDL, RSD generated |
| Field names | snake_case | camelCase JSON-LD terms with a published context |
| Entity coverage | 5 types (competency, task, assessment, mapping, change) | 20+ types (adds role profile, family, tool, credential, learning resource, signal, driver event, source…) |
| ID form | `emst:c-7K3QX9`, optional `emst:water/t-…`; 6 Crockford base32; lowercase type letters | `emst:core/CMP-T6N5VE4`; namespace always explicit; 3-letter TYPE; 6 base32 + **Luhn mod-32 check symbol**; w3id IRIs |
| Minting | random; one writer; append-only registry; **IDs minted only at `candidate`**, `seed:` keys before | **deterministic** migration minting from v1 key hash, then frozen; random for new |
| Versioning | one taxonomy SemVer + independently versioned crosswalk and snapshot layers pinned per release | SemVer per release, per layer, per module, per concept, per schema |
| Validation | `additionalProperties: false`; stored summaries unrepresentable; text-hash staleness; `derived_from` required for v1 migration; enumerations generated from `vocab/` | provenance required; supersession requires `replacedBy`; ID check symbols validated |

Both agree on the principles: the repository is the only editable copy; every other format is generated; opaque persistent IDs never reused or re-meant; v1 codes are aliases; supersession not deletion; SSSOM crosswalks; provenance on every record.

## Decision

### 1. Canonical serialization — one choice

**The canonical, editable source of truth is the set of source records in the repository, in DE's layout:** one YAML file per authored entity under `data/v2/{core,modules/<ns>}/<type>/<ID>.yaml`; JSONL for high-volume machine records (`assessments/`, `signals/`, `events/`, `changes/`); SSSOM TSV plus YAML metadata for every mapping set; L0 vocabularies as YAML concept schemes in `vocab/`.

**Those records use IA's data model and JSON-LD term names.** Field names are the camelCase terms of `schema/emst.context.jsonld`, so every source record is a JSON-LD node once the context is applied (YAML-LD). There is **one schema** (`schema/emst.schema.json`, JSON Schema 2020-12): IA's entity catalogue as the base, hardened with DE's invariants (closed objects; no stored summaries; required provenance; `derivedFrom` required when `method = v1-migration`; `E` label requires a source; text-hash on assessments; enumerations generated from `vocab/*.yaml`; CI `--check`).

**The JSON-LD bundle is the normative *release* serialization** — generated deterministically from source records at each tag, together with CSV + Frictionless datapackage, SKOS Turtle, SSSOM, CTDL-ASN, CASE 1.1, RSD and Open Badges 3.0 alignment targets. No export is ever hand-edited.

**Why this choice:** per-entity text files make SME and steward review possible (a reviewer reads one competency's diff), keep merge conflicts local, and let CODEOWNERS assign module namespaces to stewards (ADR-0009). A single bundle file works for consumers and fails for many concurrent editors. Using IA's terms in the source keeps the semantic model in one place, so the bundle is a pure assembly step, not a translation. This satisfies IA's own first commitment ("the repository is the canonical store; every other format is a generated export").

### 2. Identifier scheme

- **Form (IA's):** `emst:<namespace>/<TYPE>-<6 Crockford base32><1 Luhn mod-32 check>`; IRI `https://w3id.org/emst/<namespace>/<TYPE>-<code>`. The check symbol catches transcription errors in HR spreadsheets and PDs.
- **TYPE prefixes:** VOC (vocabulary term), CMP (competency), KNW (knowledge statement), IND (indicator), TSK (task), ROL (role profile), VAR (role variant), ENA (enactment), FAM (job family), TL (tool/method/standard), INS (instrument), EVT (driver event), CRD (credential), LRN (learning resource), PTH (pathway), BND (credential bundle view), SIG (change signal), ASM (assessment), FRC (friction record), SRC (source), MAP (mapping record), CHG (change record). Type is fixed at minting; a wrongly typed concept is superseded, not retyped.
- **Namespace = minting authority** (DOI-prefix pattern): `core`; registered module namespaces (`water`, `waterq`, `air`, `waste`, `ehs`, `envhealth`, `extract`, `energy`, `climate`, `hazards`, `markets`, `forest`, `wildlife`, `marine`, `worklands`, `parks`, `culture`, `built`, `lab`); reserved `tribal-<steward>` namespaces under ADR-0007. The TSC registers namespaces; promotion to core keeps the original ID; a fork mints in its own namespace.
- **Minting (DE's):** random 30-bit bodies from a CSPRNG, one writer (`scripts/mint_ids.py`), append-only registry `data/v2/ids/registry.csv` (id, type, namespace, minted_on, minted_by, status, superseded_by, first_release); collisions rejected and re-minted. **Persistent IDs are minted only when a record reaches `candidate`**; draft and seed records use throwaway `seed:` keys (answers DE open Q3). IA's deterministic hash-from-v1-key minting is **not** adopted: v1→v2 is many-to-many (splits, merges, rewrites), and a v1-derived identity would imply a sameness the migration does not assert. Reproducibility comes from the frozen registry.
- **Derived identifiers:** CASE, CTID and RSD UUIDs = UUIDv5 of the EMST IRI (IA).
- **v1 codes** are aliases only (`notation[{scheme: "EMSTv1", value: "2.1.1"}]`), and every v1 competency and task is accounted for in `crosswalks/emst-v1/emst-v1_to_v2.sssom.tsv` with a CI completeness test (P-DE-08).
- If L2 + indicators approach 10⁵ records in a namespace×type, move to 8 symbols in a MAJOR schema version.

### 3. Editorial status (distinct from lifecycle state, ADR-0015)

`draft → candidate → published → deprecated | superseded | withdrawn`. IDs are stable from `published`; a change of meaning mints a new ID and sets `superseded` + `replacedBy`; withdrawn IDs resolve to a tombstone with an explanation.

### 4. Versioning

- **One taxonomy SemVer** for the release (DE bump rules: MAJOR = published ID withdrawn without successor, change of meaning of an L0 term or level scale, schema field removal; MINOR = new entities/modules/terms, supersessions with successors, optional fields; PATCH = attested meaning-preserving edits, provenance fixes). Each change record declares `semverImpact`; CI fails if the tag is smaller.
- **Schema SemVer** separately.
- **Fast layers** (tools, signals, events) publish **dated snapshots**; **crosswalk sets** carry `mapping_set_version` and pinned `object_source_version`; each taxonomy release pins the snapshots it ships with.
- **Stewarded modules** (v2.2+) carry MINOR.PATCH inside a core MAJOR (charter Art. 6.1).
- **No per-concept SemVer:** concepts carry `versionIntroduced`, `lastChangedIn` and `changeNote[]`.
- Each release ships a **delta file** (added, changed, superseded, withdrawn).

### 5. Other model rules

- Provenance object required on every record (IA's fields + DE's `derivedFrom` lineage: `v1Key`, sheet, row, workbook SHA-256, v1 provenance code, source-text line, relation ∈ {carried, rewritten, split-from, merged-from, recovered, prior-evidence, reference-only}).
- Human-readable text fields are language maps; `en` required.
- Rater and agent identities are pseudonymous; identity maps live outside the repo (ADR-0012).
- **Exports required at 2.0.0** (DE open Q6): JSON-LD bundle, CSV + datapackage (incl. an HCM import library and delta feed), SKOS Turtle, SSSOM, CTDL-ASN (primary public linked-data channel; Credential Registry publication during the pilot, P-IA-15), CASE 1.1 (claim conformance only after validating against 1EdTech's schema; CASE 1.1 final Feb 2024, public Apr 2025 [E: V4-10]), RSD; OB 3.0 alignment via IRIs (cite document version 1.4.5 [E: V4-12]). SSSOM 1.0 conformant with 1.1 slots as declared extensions (1.1 is alpha only [E: V4-13]).

## Consequences

- DE merges IA's schema and context into `schema/` and extends its tests (65 passing) to the unified schema in Phase 4 WP-01.
- `w3id.org/emst/` must be registered and owned by the steward (AS); until then IRIs are reserved, not resolvable.

## Dissent and trade-offs

- **IA** preferred the JSON-LD bundle as the canonical store. Its semantics are kept in full; only the storage layout differs. Trade-off: two serializations (YAML source, JSON-LD release) versus reviewability; mitigated by one loader, one schema, one context.
- **IA** preferred deterministic migration minting and SemVer per layer and per concept; rejected as above for simplicity and to avoid implied v1 identity.
- **DE** had no check symbol and lowercase single-letter types; IA's form is adopted for human legibility. Trade-off: slightly longer IDs.
- **CP:** opaque IDs are harder to remember; sequential IDs invite people to read meaning into them, which is how v1 codes became structural (IA disagreement).
