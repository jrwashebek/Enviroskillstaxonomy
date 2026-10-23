# EMST v2 data model — draft proposal (IA)

**Status:** DRAFT 0.1.0 for CA decision. Aligned to the CA layered hypothesis (L0–L6 + namespaced modules,
`docs/research/chief-architect/architecture_hypotheses.md` §4) [IA-038]. Machine-readable artifacts:
`emst-v2.schema.json` (JSON Schema 2020-12), `emst.context.jsonld` (JSON-LD 1.1 context), worked examples in
`examples/` built by `scripts/build_examples.py` and checked by `scripts/validate_outputs.py` (all checks pass:
schema meta-validation, example validation plus three negative tests, JSON-LD expansion to 1,424 triples, Turtle
parse, SSSOM column checks, ID check symbols).

Labels: [E] evidence (source IDs in `sources.csv`), [J] judgment, [S] speculation.

---

## 1. Design commitments

1. **The repository is the canonical store; every other format is a generated export.** JSON-LD bundles in the
   repo are the source of truth; CSV, SKOS, CASE, CTDL-ASN, RSD and HCM import files are build outputs. No export
   is ever edited by hand. This is the single most important anti-lock-in rule [J]. v1 had the opposite
   arrangement (Airtable as editing master, GitHub as archive) [E: IA-035].
2. **Semantics come from open W3C vocabularies** (SKOS for concepts and mapping relations, PROV for provenance,
   Dublin Core for versioning) so that ESCO, CTDL and any RDF consumer can read EMST without a custom adapter
   [E: IA-052, IA-012, IA-022]. Structure is enforced separately with JSON Schema, as OpenLMP does [E: IA-031].
3. **Crosswalks are separate, versioned artifacts (SSSOM), not fields on concepts** [E: IA-014]. A concept never
   embeds "its" O*NET code; a mapping record says who asserted which relation, with what confidence, against
   which version of the other system.
4. **Provenance on every record and on every machine-derived value**, borrowed from OpenLMP (method,
   confidence, agent, review status) and extended with v1 lineage and the EMST evidence label [E: IA-030, IA-031].
5. **IDs are opaque, persistent, never reused, never re-pointed.** v1 codes survive only as aliases.

## 2. Identifier scheme

### 2.1 Form

```
compact:  emst:<namespace>/<TYPE>-<6 Crockford base32 symbols><1 Luhn mod-32 check symbol>
IRI:      https://w3id.org/emst/<namespace>/<TYPE>-<code>
example:  emst:core/CMP-T6N5VE4   ->  https://w3id.org/emst/core/CMP-T6N5VE4   (v1 2.1.1)
```

- **TYPE** is a three-letter entity prefix (VOC, CMP, TSK, KNW, IND, ROL, FAM, TL, CRD, LRN, SIG, ASM, EVT, SRC,
  MST, MAP). The prefix is fixed at minting; a concept never changes type. If the type is wrong, the concept is
  superseded by a new one of the right type.
- **namespace** is the *minting authority*: `core` or a module steward's namespace (`water`, `fire`, `esg`, …).
  It does not track where the concept currently lives (that is the `module` field). This is the DOI-prefix
  pattern: a concept that moves from a module into core keeps its original IRI [J].
- **Crockford base32** avoids I, L, O and U, so codes survive being read aloud, typed or printed. The check symbol
  is Luhn mod-32 over the same alphabet, so every symbol is IRI-, filename- and shell-safe. (Crockford's own
  mod-37 check adds `* ~ $ = U`; the first draft produced `SIG-2JJN7D$`, which breaks shells and some URL
  handlers, so it was replaced.) The validator checks every ID.
- **w3id.org** gives persistent IRIs that redirect to wherever the repo publishes. It is community-run and
  governed by pull request [E: IA-055], so the IRIs survive a change of host or steward. That answers part of AS's
  "who maintains this in year five" question [J]. Namespace registration was not confirmed this session.

### 2.2 Minting

- **Migration (once):** `TYPE-code = base32(first 30 bits of SHA-256("emst-v1-migration:" + v1 key)) + check`.
  This makes the DE migration build reproducible. The minted IDs are then frozen in an ID registry
  (`registry/ids.csv`: id, type, minted_at, minted_by, origin, status, replaced_by) and never recomputed.
- **New concepts:** random 30-bit codes from a CSPRNG, checked against the registry.
- **Collisions:** 30 bits gives 1.07 × 10⁹ codes per namespace and type. Collisions are negligible for
  competencies (~10³) but not for indicators. At 2 × 10⁴ indicators the birthday probability is about 0.17. The
  registry must reject a collision and re-mint (migration: append `#2` to the seed). If L2 grows past about
  10⁵ statements, move to 8 symbols in a major schema version [J; arithmetic].

### 2.3 Derived identifiers for other systems

| System | Identifier | Derivation |
|---|---|---|
| CASE 1.1 (`identifier`) | UUID | UUIDv5(namespace = UUIDv5(URL, "https://w3id.org/emst/"), name = EMST IRI) |
| Credential Registry (CTID) | `ce-<uuid>` | same UUID with `ce-` prefix |
| RSD / OSMT (`uuid`, `id`) | UUID, IRI | same UUID; `id` = EMST IRI |
| Open Badges 3.0 Alignment | `targetUrl`, `targetCode` | EMST IRI; v1 code or UUID |

Because they are derived deterministically from the IRI, re-exporting never changes them, and no second
registry is needed [J].

### 2.4 Lifecycle, deprecation, supersession

`status ∈ {draft, proposed, active, deprecated, superseded, withdrawn}`. The rules below follow the NICE
statement pattern of Retained / New / Withdrawn with major-vs-minor by backward compatibility [E: CA-033 via
IA-048].

- **Clarify** wording without changing meaning: patch or minor concept version, same ID.
- **Change meaning, split or merge:** new ID(s). The old record becomes `superseded` with `replacedBy` (the
  schema enforces this) and stays resolvable forever.
- **Remove:** `withdrawn`, with a change note. Never delete the record.
- **v1 aliases:** `notation[{scheme: "EMSTv1", value: "2.1.1"}]`. A v1 code can therefore point to several v2
  concepts after a split. The ID registry and the v1→v2 SSSOM file (`EMSTv1:2.1.1 skos:exactMatch
  emst:core/CMP-T6N5VE4`) record that.

## 3. Entities by layer

| Layer (CA) | Entity (`type`) | Prefix | Key fields (beyond the common base) | Nearest external equivalents |
|---|---|---|---|---|
| L0 | VocabularyTerm | VOC | vocabulary (craft, sector-actor, work-function, subsector, jurisdiction, level-of-responsibility, tool-type, signal-type), ordinal | skos:Concept in a ConceptScheme; CTDL concept schemes |
| L1 | Competency | CMP | competencyType (core/transversal/module), statement, workFunctions, subsectors, craft (CraftProfile), proficiency[ProficiencyAnchor{level, knowledge, application, indicators[Indicator], practicedAtLevel}], enactments[{sectorActor, jurisdiction, note}], families | ceasn:Competency; CASE CFItem; ESCO skill; RSD; IEEE 1484.20.3 competency definition |
| L1 | Indicator (embedded, own ID) | IND | statement, observable, assessmentMethods | CASE CFRubricCriterion; OB3 alignment target |
| L2 | Task | TSK | statement, supports[{competency, strength}], knowledge[], tools[], workFunctions, craft, v1Tier, exposureSummary (computed) | ceterms:Task; O*NET task statement; NICE T-statement |
| L2 | KnowledgeStatement | KNW | statement | NICE K-statement; ESCO knowledge concept |
| L3 | RoleProfile | ROL | function, sectorActor, variantOf, lifecycleStatus, taskBundle[{task, importance, timeShare}], competencyTargets[{competency, level, importance}], entryFrom, progressesTo, frictions | ceterms:WorkRole / ceterms:Occupation; O*NET-SOC occupation; OPM series (via L6); JDX Job |
| L3 | ProfessionFamily | FAM | members | v1 F1–F15 (navigation view) |
| L4 | Tool | TL | toolType (software-category, software-product, instrument, model, protocol, standard, reporting-framework, dataset), vendorNeutral, productExamples, expectedHalfLifeYears | O*NET Technology Skills; Lightcast skills |
| — | Credential, LearningResource | CRD, LRN | ctid, covers / cip, teaches | ceterms:Credential; CTDL LearningOpportunity; OB3 Achievement |
| L5 | ChangeSignal | SIG | signalType, about[], sectorActor[], jurisdiction[], observedPeriod, comparisonPeriod, measure{name, value, unit, ci95, n, denominator}, direction, linkerQuality, corpus, caveats | (none standard: EMST-specific) |
| L5 | ExposureAssessment | ASM | task, instrument, scenario, values{…}, assessedAt | v1 Task 13 rows; AEI task shares (LM) |
| L5 | DriverEvent | EVT | jurisdiction, instrument, eventDate, eventStatus, affects[], expectedEffect | replaces v1 reform booleans (CA) |
| L6 | Mapping (SSSOM record) | MAP / record_id | SSSOM slots + review_status | sssom:Mapping |
| — | Source | SRC | url, sha256, publisher, published, accessed, rights | dct:BibliographicResource |

Every concept carries the common base: `id, type, prefLabel, altLabel, hiddenLabel, definition, scopeNote,
notation[], layer, module, inScheme, broader, related, status, version, firstRelease, lastChangedRelease,
replaces, replacedBy, changeNote[], license, provenance`.

**Why the links point from tasks to competencies** (`Task.supports`), and not the other way: CA's lean makes
tasks the internal spine and competencies a curated view [E: IA-038]. Storing the link once, on the many side,
avoids two-sided edits drifting apart. The build computes the inverse (`Competency.tasks`) for exports [J].

**What is computed, never stored** (agreeing with CA §4): craft blends for competencies and roles,
`exposureSummary`, stability, family relevance counts, every dashboard number, and the inverse relations. The
v1 Workforce Signals sheet shows what happens otherwise: its stored summary under-counted the per-competency
reform flags by 59 [E: IA-034].

## 4. Multilingual labels

All human-readable text is a language map (`{"en": "...", "es": "..."}`), mapped to `@container: @language`
in the context so each value becomes a language-tagged literal. Language is never a separate record. CASE 1.1
added multilingual support and `isTranslationOf` [E: IA-003, IA-004]. ESCO covers 27 languages
[E: IA-028, as of 2023], so labels can be aligned language by language. Spanish matters first for US
federal/state users [J]. Translations carry their own provenance (human/LLM, reviewer).

## 5. Versioning

| What | Scheme | Rule |
|---|---|---|
| Taxonomy release | SemVer `MAJOR.MINOR.PATCH` (`emst_version`) | MAJOR: any concept withdrawn or superseded in core, or schema-breaking change. MINOR: new concepts, new optional fields. PATCH: wording fixes |
| Layer versions | SemVer per layer (`layer_versions`) | Layers run on different cadences (CA §4: L0 annual … L5 continuous) |
| Module versions | SemVer per module (`modules[]`) | Module stewards release inside core rules |
| Concept | SemVer `version` + `changeNote[]` | Meaning changes trigger a new ID, not a major version (§2.4) |
| Schema | SemVer `schema_version` | Additive = minor; renamed/removed fields = major (OpenLMP rule) [E: IA-030] |
| Crosswalks | `mapping_set_version` + pinned `object_source_version` | Each upstream release (O*NET quarterly, ESCO minor) produces a new mapping-set version |

Each release ships a **delta file** (added, changed, superseded, withdrawn IDs), as ESCO does for v1.2.1
[E: CA-030] and CA recommends [E: IA-038].

## 6. Provenance

The `provenance` object is required on every record. Its fields:

- `method ∈ {v1-migration, human-authoring, sme-panel, delphi, llm, rule, lexical-linker, import, computed}`
- `agent[]` (ORCID or `emstagent:` software agents with versions)
- `generatedAt`
- `derivedFrom[]` (v1Key, v1Code, sheet, row, workbookSha256, v1ProvenanceCode, entity)
- `sources[]`
- `evidenceLabel ∈ {E, J, S}`
- `confidence`
- `reviewStatus ∈ {unreviewed, spot_checked, reviewed, validated, gold}`
- `reviewers[]`, `reviewedAt`
- `interRaterAgreement{statistic, value, nRaters}`
- `toolVersion`, `promptVersion`, `notes`

The OpenLMP pattern is carried over nearly verbatim: method, confidence, enriched_by, review_status, plus prompt
version for LLM enrichment [E: IA-030, IA-031]. Two fields are additions. `evidenceLabel` makes the team's
evidence standard machine-readable. `interRaterAgreement` gives IO a place to record reliability, which v1
lacked entirely [E: IA-038].

v1 lineage is complete in the examples. For instance, `derivedFrom: v1:2.1.1, sheet Competencies, row 42,
workbookSha256 6085795e…` is the hash recorded by DE's BUILD_INFO [E: IA-034]. The T13 provenance code
(e.g. `reconstructed_d2`) moves into `v1ProvenanceCode`.

## 7. Modules (namespaced extensions)

- A module is a namespace plus a steward plus a release line (`modules[]` in the bundle).
- Module concepts may reference core concepts freely. Core concepts may not depend on module concepts. This
  keeps core releasable alone [J].
- **Conformance rule for a module release:** it validates against the same schema; every concept has
  provenance; it has no IDs outside its namespace; and it publishes its crosswalks as SSSOM.
- **Promotion to core** keeps the ID and changes `module` to `core`, with a change note.
- **Forks** are detectable: two publishers asserting different records for one IRI violate the registry. A fork
  must mint in its own namespace [J].

## 8. Export profiles: v1 2.1.1 in each

All examples are generated from DE's v1 baseline. They cover two competencies (2.1.1, 6.1.2) with their 6 tasks,
48 indicators, 6 exposure assessments, ESCO mappings, one O*NET-SOC link and change signals.

| Profile | File | Audience | What is lost |
|---|---|---|---|
| Native JSON-LD bundle | `examples/emst-v2.bundle.example.jsonld` | Developers, RDF stores | Nothing (canonical) |
| CSV bundle + Frictionless `datapackage.json` + SSSOM TSV | `examples/csv_bundle/` | HR analysts, HCM import, spreadsheets | Nesting; language maps flattened to `_en` columns |
| SKOS (Turtle) | `examples/emst-v2.skos.example.ttl` | Thesaurus tools, ESCO-style consumers | Proficiency anchors, provenance detail; only accepted, non-negated mappings |
| CASE 1.1 package | `examples/emst-v2.case-1.1.example.json` | LMS / assessment / curriculum systems | close/broad/narrow collapse to `isRelatedTo`; provenance kept only in `notes` |
| CTDL-ASN JSON-LD | `examples/emst-v2.ctdl-asn.example.jsonld` | Credential Registry, credential/job linking | Exposure and signal layers (no CTDL home) |
| RSD (OSMT API v2 shape) | `examples/emst-v2.rsd.example.json` | OSMT users (colleges, employers) | Everything except label, statement, category, keywords, exact/close alignments, occupations |
| Open Badges 3.0 alignment | `examples/ob3-alignment.example.json` | Credential issuers | n/a (points at EMST) |

**Native (abridged):**

```json
{"id": "emst:core/CMP-T6N5VE4", "type": "Competency", "layer": "L1", "module": "core", "competencyType": "core",
 "prefLabel": {"en": "Geographic Information Systems (GIS) operation"},
 "statement": {"en": "Using specialized mapping software to create, analyze, and display maps and geographic information."},
 "notation": [{"scheme": "EMSTv1", "value": "2.1.1"}], "status": "proposed", "version": "0.1.0",
 "craft": {"v1Primary": "DC", "v1Secondary": "FC", "ordinal": {"FC": "supporting", "DC": "defining", "SC": "none"}, "computed": false},
 "proficiency": [{"level": "EMSTv1level:foundational", "knowledge": {"en": "Understands GIS concepts (layers, attributes, projections, spatial relationships)"},
                  "application": {"en": "Performs basic GIS operations"},
                  "indicators": [{"id": "emst:core/IND-XZZVH7F", "statement": {"en": "Creates simple maps using existing data layers"}}]}, "…"],
 "provenance": {"method": "v1-migration", "evidenceLabel": "J", "reviewStatus": "unreviewed",
                "derivedFrom": [{"v1Key": "v1:2.1.1", "sheet": "Competencies", "row": 42, "workbookSha256": "6085795e…"}]}}
```

The bundle also holds:

- the Task `emst:core/TSK-9YY1TPK` ("Create and update spatial layers…", `supports` → CMP-T6N5VE4);
- its ExposureAssessment `ASM-…` (instrument `emst-v1-task13`, values A/Lo/P/AI/1, `v1ProvenanceCode`
  reconstructed_d2);
- a Mapping (`skos:closeMatch` → `ESCO:440f64e5-…` "use geographic information systems", confidence 0.85,
  `semapv:LLMBasedMatching`, reviewer `emstagent:claude-in-session-IA`, comment "requires human SME
  confirmation");
- a ChangeSignal carrying its own `linkerQuality` (P@1 0.53, CI 0.39–0.67) and caveats.

**CSV bundle (competencies.csv row):**
`emst:core/CMP-T6N5VE4, https://w3id.org/emst/core/CMP-T6N5VE4, 2.1.1, Geographic Information Systems (GIS) operation, "Using specialized…", L1, core, proposed, 0.1.0, DC, FC, 9a1fc089-b8c5-5a91-a7b7-0da22ec7c430, ce-9a1fc089-…, v1-migration, v1:2.1.1, 6085795e…`

**SKOS:** `<…/CMP-T6N5VE4> a skos:Concept; skos:prefLabel "Geographic Information Systems (GIS) operation"@en;
skos:notation "2.1.1"^^emstv:v1Code; skos:closeMatch esco:440f64e5-…; skos:narrowMatch esco:bad66a63-… (create GIS
reports); skos:relatedMatch esco:377861af-… (geographic information systems, a knowledge concept)`.

**CASE 1.1:** CFItem `identifier 9a1fc089-…` (UUIDv5), `uri` = EMST IRI, `CFItemType "Competency"`,
`humanCodingScheme "2.1.1"`. Tasks are CFItems linked by `isChildOf`. ESCO mappings become `isRelatedTo` with
`destinationNodeURI.targetType "ESCO"`, and the SKOS predicate is preserved in `notes`. Caveat: field names
follow CASE 1.0 knowledge plus the 1.1 change list [E: IA-003]. The 1.1 information model itself could not be
opened (blocked), so validate against 1EdTech's JSON Schema before claiming conformance.

**CTDL-ASN:** `ceasn:Competency` with `ceterms:ctid ce-9a1fc089-…`, `ceasn:competencyLabel`,
`ceasn:competencyText`, `ceasn:codedNotation "2.1.1"`, `ceasn:isPartOf` the framework. Mappings are rendered as
`ceasn:majorAlignment` (close), `ceasn:narrowAlignment` and `ceasn:minorAlignment` (related). The O*NET-SOC link
is a `ceterms:occupationType` CredentialAlignmentObject (15-1299.02 GIS Technologists and Technicians), the
same shape the RSD-in-CTDL sample uses [E: IA-012]. The SKOS→CTDL-ASN predicate mapping is my judgment [J]; CE
should confirm it.

**RSD:** `{"type": "RichSkillDescriptor", "id": <EMST IRI>, "uuid": "9a1fc089-…", "skillName": …,
"skillStatement": …, "category": "Geospatial Technologies", "alignments": [ESCO closeMatch only],
"occupations": [{"code": "15-1299.02", "frameworkName": "o*net"}]}`. Field names are taken from the OSMT API v2
test fixture [E: IA-013].

**OB 3.0:** `Achievement.alignment[{targetUrl: <EMST IRI>, targetCode: "2.1.1", targetType:
"ceasn:Competency"}]`, plus a second alignment with `targetType: "CFItem"`. Both values are in the OB 3.0
AlignmentTargetType enumeration [E: IA-015].

## 9. How workforce platforms take it in (and how to avoid lock-in)

Vendor ingestion documentation for Workday Skills Cloud, SAP SuccessFactors Talent Intelligence Hub, Oracle HCM
and Eightfold could not be read this session [IA-051, unverified; CP-066 reports the same]. What follows is a
vendor-neutral delivery contract [J], to be verified in the pilot:

1. **Import library:** the CSV bundle, one row per competency/task, with a stable `competency_id`, `uri`,
   label, statement, `version`, `status` and `replaced_by`. Every enterprise skills library known to the author
   can import "skills with external IDs" from CSV [S: confirm per vendor].
2. **Change feed:** the release delta (added / changed / superseded / withdrawn) as CSV and JSON, so a platform
   can update without re-importing. Platforms that cannot honor `replacedBy` must at least deactivate superseded
   IDs.
3. **Mapping audit:** require vendors that infer skills to export their mapping from their internal ontology to
   EMST IDs as SSSOM. This makes vendor inference auditable and portable [J]. It is the concrete anti-lock-in
   clause for procurement language (AS/CP).
4. **No vendor IDs as primary keys** anywhere in EMST. Lightcast or vendor skill IDs appear only as mapping
   objects, and only where their licences allow it [IA-045 unverified].
5. **APIs are a convenience, not the contract:** a read-only API (e.g. generated from the bundle) can come later.
   The contract is the versioned files plus w3id IRIs, which survive any API's retirement. The O*NET Web Services
   v1.9→v2.0 transition is a reminder that APIs churn [E: IA-021].

## 10. Open issues for CA

- DP-1/DP-3: The schema supports both spines. Task-only role profiles and competency-centred packaging can
  coexist without schema change.
- DP-4: Levels are referenced by ID (`EMSTv1level:*` now, L0 level-of-responsibility terms later), so the
  proficiency decision does not block the schema.
- DP-5: CraftProfile allows weights or ordinal, each with its own provenance.
- DP-7: Sector actors are an L0 vocabulary; v1's five sector notes are carried as provisional enactments with
  alias refs (`EMSTv1:sector/*`).
- Licence: CC BY 4.0 (used in the examples) vs CC0 is unresolved (v1 had both) [E: IA-035]. This needs an AS/CP
  decision.
