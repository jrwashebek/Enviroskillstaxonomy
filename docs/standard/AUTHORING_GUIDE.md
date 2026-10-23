# EMST v2 authoring guide (for authoring agents and editors)

**Owner:** DE (WP-01/WP-02) · **Applies to:** FC, DC, SC, DB, FH, IO/LC, LM/FS and every editor · **Status:** binding how-to for Phase 4; the normative rules are in `docs/standard/SPEC.md`, the ADRs and `vocab/`. Licence: CC0-1.0.

If this guide and the SPEC disagree, the SPEC (and then the ADR) governs. Open a change request in `docs/decisions/change_requests/` instead of working around a rule.

---

## 1. The five rules that matter most

1. **One record per file** for authored entities, in YAML, using the field names of `schema/emst.schema.json` (camelCase). Unknown fields are rejected. Summaries are never stored (no counts, modal values, blends, tiers, roll-ups, inverse links): CI computes them.
2. **Drafts use `seed:` keys.** Never invent an `emst:` ID. IDs are minted only by `scripts/mint_id.py` when a record reaches `candidate`.
3. **Agent output is draft evidence.** Anything you draft: `status: draft`, `validationStatus: draft`, `provenance.method: llm-assisted` with `toolVersion` and `promptVersion`, `reviewStatus: unreviewed`. Every rating you make: `raterType: llm`, `evidenceLabel: S`. Never write `reviewed`, `panel-retained` or higher yourself.
4. **The Tribal hold is absolute.** Anything touching Tribal governments, Indigenous knowledge or Tribal data is flagged held (section 8) and never released. Do not write as if you speak for any nation.
5. **Run the validator before you hand back.** `python scripts/validate_v2.py` must show no errors in the files you touched.

## 2. Where records live

`<area>` is `core` or `modules/<namespace>` (namespaces: `vocab/modules.yaml`; wave 1 is `water`, `waterq`, `air`, `waste`, `envhealth`, `hazards`, `forest`, `wildlife`, `parks`).

| Entity (`type`) | Path | File name |
|---|---|---|
| Competency | `data/v2/<area>/competencies/` | `<stem>.yaml` |
| Indicator | `data/v2/<area>/indicators/` | `<stem>.yaml` |
| Enactment | `data/v2/<area>/enactments/` | `<stem>.yaml` |
| Task | `data/v2/<area>/tasks/` | `<stem>.yaml` |
| KnowledgeStatement | `data/v2/<area>/knowledge/` | `<stem>.yaml` |
| RoleProfile / RoleVariant / JobFamily / Pathway | `data/v2/<area>/{roles,variants,families,pathways}/` | `<stem>.yaml` |
| LearningResource / Bundle / Source / FrictionRecord / WatchItem | `data/v2/<area>/{learning-resources,bundles,sources,frictions,watch-items}/` | `<stem>.yaml` |
| Credential / SeriesRecord / StateClassRecord | `data/v2/registers/{credentials,opm_series,state_classes}/` | `<stem>.yaml` |
| Tool (L4) | `data/v2/tools/tools.jsonl` | one JSON object per line |
| ExposureAssessment, CraftRating, FunctionRating, RelevanceRating | `data/v2/assessments/<instrument>/<batch>.jsonl` | one per line |
| ChangeSignal | `data/v2/signals/<yyyy>/<source>.jsonl` | one per line |
| Instrument (L5 registry) | `data/v2/instruments/instruments.jsonl` | one per line |
| DriverEvent | `data/v2/events/<yyyy>.jsonl` | one per line |
| ChangeRecord | `data/v2/changes/<release>.jsonl` | one per line |
| Mapping sets | `data/v2/crosswalks/<target>/<target-version>.sssom.tsv` + `.sssom.yml` | SSSOM 1.0 |

**File stem = the id**: `seed:FC-C18` → `seed-FC-C18.yaml` (a `/` in a seed key becomes `--`); a minted `emst:core/CMP-T6N5VE4` → `CMP-T6N5VE4.yaml`. The `module` field must equal the area (`core` or the namespace). **Core records must not depend on module records** (only `replaces`/`replacedBy` may point into a module). Module records must carry `subsectors` (codes from `vocab/subsectors.yaml`).

## 3. Seed keys

Free text after `seed:`, characters `A-Z a-z 0-9 . _ - /`. Use these conventions so the v1 crosswalk (X1) and other agents can find your records:

| Record | Key |
|---|---|
| v1 competency seed (already migrated) | `seed:v1-<code>` e.g. `seed:v1-4.1.1` |
| v1 task seed (already migrated) | `seed:v1-<code>-T<n>` e.g. `seed:v1-4.1.1-T2` |
| Record authored from a candidate (`candidate_disposition.csv`) | `seed:<cand_id>` e.g. `seed:FC-C18`, `seed:DC-CAND-13` |
| A split or free-text target in `v1_disposition.csv` | the key listed in `data/v2/migration/v1_targets.csv` (e.g. `seed:v1-4.4.1-A`) |
| RoleProfile (CR-IA-001) | `seed:<role_key>` with `role_key` from `docs/decisions/mvp_role_set.csv`, e.g. `seed:R02-field-resource-technician` |
| RoleVariant (CR-IA-001) | `seed:<role_key>/<sector_actor>[/<slice>]`, `sector_actor` a `vocab/sector_actors.yaml` notation, e.g. `seed:R02-field-resource-technician/state` (file `seed-R02-field-resource-technician--state.yaml`) |
| Anything else | `seed:<role>-<short-slug>`, e.g. `seed:fc-adapt-protocol-in-place` |

A role or variant key in another form, or a `role_key` not in the MVP role set, is reported as `W-ROLE-KEY` (a warning: later roles may come from elsewhere). Do not use `mvp-role:<role_key>` as a `targetId`; it is a placeholder (`W-MVP-ROLE-TARGET`) and the release gate drops such records.

Look up the planned key for any disposition target in **`data/v2/migration/v1_targets.csv`** (`target_key`, `target_kind`, expected `area`, owning WP). If you author a target under a different key, give it the right `derivedFrom` (section 6) and X1 will still find it.

## 4. Minimal valid examples

Copy, then fill. `<…>` are placeholders. These pass the schema; the authoritative field list is `schema/emst.schema.json` and SPEC §5.

**Competency** (`data/v2/core/competencies/seed-FC-C18.yaml`)

```yaml
id: seed:FC-C18
type: Competency
prefLabel: {en: Assess field site hazards before and during work}
definition: {en: <SKOS definition: what the capability covers and excludes>}
statement: {en: <≤ 60 words; practice and transversal titles are verb + object (+ context); knowledge areas are noun phrases>}
competencyType: practice            # practice | knowledge-area | transversal (+ transversalCluster TX-A…TX-F)
levelSpan: {min: L1, max: L3}
homeModule: core
layer: L1
module: core
status: draft
lifecycleState: established          # proposed/emerging also need reviewBy
useTier: describe                    # declared ceiling; v2.0 content is describe or develop, never select
validationStatus: draft
license: CC0-1.0                     # v1 text is dedicated CC0 (section 7)
sensitivity: public
provenance:
  method: llm-assisted
  agent: ['emstagent:fc-agent@wp-03']
  generatedAt: '2026-10-24T10:00:00Z'
  toolVersion: <model id, frozen>
  promptVersion: <prompt file + version, e.g. wp03-competency@1>
  evidenceLabel: J                   # content text: J with the basis in editorialNote; E needs sources
  reviewStatus: unreviewed
  derivedFrom:                       # required whenever v1 content was used (section 6)
    - {v1Key: 'v1:2.1.3', relation: merged-from}
    - {v1Key: 'v1:4.4.3', relation: merged-from}
  adr: [ADR-0011, ADR-0003]
```

A competency must be supported by at least one Task (`Task.supports`); links live on the task side only.

**Task** (`data/v2/core/tasks/seed-fc-hazard-brief.yaml`)

```yaml
id: seed:fc-hazard-brief
type: Task
prefLabel: {en: Brief a field crew on site hazards and escape routes before work begins}
statement: {en: Brief a field crew on site hazards and escape routes before work begins}
textSha256: <SHA-256 of the normalized statement; see the command below>
supports: [{competency: 'seed:FC-C18', strength: primary}]
workFunction: WF-ASSESS              # one primary function (vocab/work_functions.yaml)
fieldDependency: on-site-required    # on-site-required | on-site-preferred | remote-capable | remote
formationDependency: 'yes'           # quote yes/no
homeModule: core
layer: L2
module: core
status: draft
lifecycleState: established
useTier: describe
validationStatus: draft
license: CC0-1.0
sensitivity: public
provenance: {method: llm-assisted, agent: ['emstagent:fc-agent@wp-03'], generatedAt: '2026-10-24T10:00:00Z', toolVersion: <model>, promptVersion: <prompt>, evidenceLabel: J, reviewStatus: unreviewed}
```

Task text: one imperative verb, 8–30 words, no compound verbs, no product names (a tool *class* is fine when it changes the work condition). `textSha256` must equal the hash of the normalized `statement.en`; compute it with `python -c "import sys; sys.path.insert(0, 'scripts'); import emstlib as L; print(L.text_sha256('YOUR STATEMENT'))"` (the validator's `E-TEXT-HASH` message also prints the expected value).

YAML tip: in a `{en: ...}` flow map, quote any text containing a comma or a colon: `{en: 'Revises the plan, then records it.'}`.

**Indicator** (`data/v2/core/indicators/seed-fc-c18-l2-a.yaml`)

```yaml
id: seed:fc-c18-l2-a
type: Indicator
prefLabel: {en: Revises the job hazard analysis when site conditions change}
competency: seed:FC-C18
level: L2
statement: {en: 'Revises the job hazard analysis when site conditions differ from the plan, and records the change before work resumes.'}
augmentationMode: unaided            # unaided | assisted | supervisory
assessmentMethods: [task-book-observation]
useClass: develop                    # describe | develop (select is not used in v2.0)
obs4: 3                              # develop needs ≥ 2 (+ evidencePlan when 2); 0–1 is never released
jurisdictionVariable: false
servedTasks: ['seed:fc-hazard-brief']
layer: L1
module: core
status: draft
lifecycleState: established
useTier: develop
validationStatus: draft
license: CC0-1.0
sensitivity: public
provenance: {method: llm-assisted, agent: ['emstagent:io-agent@wp-03'], generatedAt: '2026-10-24T10:00:00Z', toolVersion: <model>, promptVersion: <prompt>, evidenceLabel: J, reviewStatus: unreviewed}
```

Then list it on the competency: `levels: [{level: L2, indicators: [seed:fc-c18-l2-a, seed:fc-c18-l2-b]}]` (2–5 per published level). Indicator lint is IO's WP-11 linter (`validation/lint_indicators.py`, rules in `validation/indicator_lint_rules.yaml`: B01–B12 and the publication rules); `validate_v2.py` runs it on every indicator, competency, task and knowledge statement and falls back to `schema/lint/indicator_lint.yaml` only if it is missing. Record the attribute that separates a level from the one below in `distinguishingAttribute` (ATT-AUT … ATT-FOR).

**Enactment** (`data/v2/modules/forest/enactments/seed-ena-fc-c18-forest.yaml`): `type: Enactment`, `competency`, `enactmentKind: actor | module | craft`, `note` (language map); actor enactments also need `actorType`, `authorityBasis`, `principal`, `accountabilityVenue`; module enactments `enactedInModule`; craft enactments `craft`. Plus the common base (`prefLabel`, `layer: L1`, `module`, `status`, `lifecycleState`, `useTier`, `validationStatus`, `license`, `sensitivity`, `provenance`).

**Rating by an agent** (one line in `data/v2/assessments/emst-craft@0.1/wp03-fc-pass1.jsonl`; shown wrapped):

```json
{"id":"seed:asm/wp03-fc-pass1/fc-hazard-brief","type":"CraftRating","prefLabel":{"en":"FC pass 1 craft rating of seed:fc-hazard-brief"},
 "layer":"L5","module":"core","status":"draft","license":"CC0-1.0","sensitivity":"public",
 "task":"seed:fc-hazard-brief","taskTextSha256":"<hash of the exact statement you rated>","scale":"ordinal-0-2","values":{"FC":2,"DC":0,"SC":0},
 "raterType":"llm","raterId":"emstagent:fc-rater-1@wp03","assessedAt":"2026-10-24","method":"blind coding per crafts.yaml rubric",
 "confidence":"med","instrument":"emst-craft@0.1","codebookVersion":"crafts.yaml 1.0.0-draft","evidenceLabel":"S","sources":[],
 "provenance":{"method":"llm-assisted","agent":["emstagent:fc-rater-1@wp03"],"generatedAt":"2026-10-24T10:00:00Z","toolVersion":"<model>","promptVersion":"<prompt>","evidenceLabel":"S","reviewStatus":"unreviewed"}}
```

Three independent passes = three `raterId`s, coded blind to the parent competency and any prior label. Agreement is computed by CI; never type it in.

**L5 and L6 field names that differ from the SPEC text** (CR-DE-001): ChangeSignal uses `signalStatus` (watch | active | retired), SeriesRecord `seriesStatus`, Source `sourceStatus`; their titles go in `prefLabel`. `status` is always the editorial status. Coded values come from `vocab/` exactly (e.g. `crosswalkMinMatchType: skos:closeMatch`, not `close`; `reviewStatus: unreviewed`, not `machine-coded`); periods are `{start, end}` as `YYYY`, `YYYY-MM` or `YYYY-MM-DD` with an optional `note`. The CR-LM-001/002 fields are now in the schema (ADR-0029; see section 12).

**Tool (L4)**: `type: Tool`, `layer: L4`, `toolType`, `vendorNeutral`, `servesTasks` or `servesCompetencies` (L4 points at L1/L2, never the reverse), `lifecycleState: watch | established | declining | withdrawn`, plus the common base. Product names go in `productExamples` (the typing lint learns them automatically).

## 5. Minting IDs (only at `candidate`)

```bash
python scripts/mint_id.py promote seed:FC-C18 --by emstagent:fc-agent@wp-03
```

This draws a CSPRNG ID in the record's namespace, appends it to `data/v2/ids/registry.csv`, sets `status: candidate`, renames the file, rewrites every reference to the seed key under `data/v2/` and logs the pair in `data/v2/ids/seed_map.csv`. It refuses held Tribal records and unauthored v1 seeds (`validationStatus: seed-v1`). In Phase 4, **promotion is done by the CA/DE at integration (WP-16)**; authoring agents leave records as `draft`. Never edit `registry.csv` by hand (CI rejects anything but status transitions). `WatchItem` (`WCH`), `SeriesRecord` (`SER`) and `StateClassRecord` (`SCR`) are mintable like every other type (ADR-0029 §2). A `seed-v1` record is never promoted: rewrite it as a draft first (`E-SEED-CANDIDATE`).

## 6. Working from the v1 seed records

WP-02 migrated every v1 competency and task as a **seed** (`validationStatus: seed-v1`, `license: CC0-1.0` under the lead's dedication, `provenance.method: v1-migration`). Each competency seed carries:

- `editorialNote.en`: its v1 disposition (decision → target, rationale) from `docs/decisions/v1_disposition.csv`;
- `v1Seed`: the restored v1 text, reference only and stripped from every release: original title/description, the four v1 levels mapped to L1–L4 with Knowledge/Application and **all** source indicators (each with its `v1Key`; `origin: restored-from-source-text` marks the 2,104 the v1 database had truncated), and the five sector notes;
- `v1Domain`, `v1SkillArea` legacy facets and `notation: [{scheme: EMSTv1, value: '<code>'}]`.

What the seed's `status` means:

| v1 decision | Seed status | What you do |
|---|---|---|
| carry, rewrite, move-to-module | `draft` (live), in `core/` or `modules/<ns>/` | **Edit the seed in place**: keep its `id`, rewrite the text to v2 rules, fill the required fields, set `validationStatus: draft`, `provenance.method: llm-assisted` (+ versions), change its own `derivedFrom` relation from `carried` to `rewritten` if you change the wording, write new Indicator records from `v1Seed`, then delete `v1Seed` only when every level you publish has v2 indicators. |
| merge | `superseded`, `replacedBy: [<target>]` | Fold the content into the target. If the target is another v1 seed it already carries `derivedFrom {v1Key, relation: merged-from}`; if it is a candidate, add that entry when you author it. The merged item's tasks already point at the target. |
| split | `superseded`, `replacedBy: [<targets>]` | Author each target (keys in `v1_targets.csv`) with `derivedFrom {v1Key: 'v1:<code>', relation: split-from}`; then re-point each of the old tasks (`supports`) to the right successor (the validator warns `W-SUPERSEDED-TARGET` until you do). |
| move-to-tools | `superseded`, `replacedBy: [<durable remainder>, <tool>]` | DC adds the tool family to `tools.jsonl`; the durable remainder (if any) absorbs the content as `merged-from`. |
| retire | `withdrawn` | Nothing; X1 records `sssom:NoTermFound`. |
| hold-for-tribal-review | `superseded`, held, `replacedBy` the held TN successors | Do not author. TN drafts only, inside the hold. |

`derivedFrom` items: `{v1Key, relation, v1Table?, v1Row?, workbookSha256?, sourceTextLine?, note?}`; `relation ∈ carried | rewritten | split-from | merged-from | recovered | prior-evidence | reference-only`. Keys resolve to `data/v1_baseline/` (`v1:4.1.1`, `v1:4.1.1:T2`, `v1:4.1.1:advanced:I7`, `v1:4.1.1:sector:ngos`). Cite indicator keys when you rewrite a v1 indicator. After authoring, DE regenerates X1 with `python scripts/migrate_v1.py --x1-only` (CI fails `E-X1-STALE` otherwise); X1 picks up every live record whose `derivedFrom` names a v1 key.

**v1 tags are prior evidence only** (`data/v2/assessments/emst-v1-*/`; `raterType: v1-analyst`, `raterId: v1-analyst-01`, `confidence: low`). Read them for context; never copy a v1 craft, stage, family, exposure or lens value into a v2 field, and never cite them as v2 findings. These batches, X1 and `data/v2/migration/` are regenerated by `scripts/migrate_v1.py`: do not edit them. The v1 stability tier, modal fields and counts were deliberately not migrated (ADR-0011 rule 5, amended; ADR-0029 §3): never add `stabilityTier`, or `stability_tier`/`tier` inside `v1Values`. The v1 CLD flag, R9 severity and S-trajectory flag are prior evidence only and never feed a computed CLD.

## 7. Licence on each record (ADR-0013)

- EMST-authored records, including everything derived from v1: `license: CC0-1.0`. The project lead dedicated the v1 text to CC0 on 2026-10-23 (`docs/decisions/PROJECT_LEAD_DECISIONS.md`, Q2; recorded in `data/v2/governance/licensing.yaml`), so the v1 seeds and anything rewritten from them ship in the CC0 files. Keep `derivedFrom` lineage anyway: it is provenance, not a licence condition.
- `LicenseRef-EMSTv1-PendingDedication` is the ADR-0013 fallback for a fork without that dedication; do not use it in this repository.
- Third-party text (O*NET, ESCO, accreditors such as the SAF handbook, credential bodies, licensed posting data) is never copied; crosswalks carry IDs only; permitted upstream text lives in `external/` under its own licence.

## 8. Tribal-related content (ADR-0007 §D)

Held: TN-C01…TN-C13, SC-C13, the successors of v1 5.3.2, 6.5.1 and 7.1.1, every v1 ethical-lens L2 value, Tribal role variants, Tribal-flagged signals, government-to-government tasks, Tribal enactments and frictions (`data/v2/governance/tribal_hold.yaml`). A held record carries:

```yaml
indigenousDataFlag: true
approvalStatus: pending-tribal-review
sensitivity: restricted-governed
aiUsePermitted: false          # unless a Tribe has authorized AI use
governedData: tribal           # only for tasks handling confidential Tribal information or Indigenous knowledge
```

Anything that depends on a held record (a task supporting it, an indicator or enactment of it, a rating of it) must be flagged too (`E-TRIBAL-INHERIT`). Unflagged text that mentions Tribes, Indigenous knowledge, treaties or government-to-government relations is reported as `W-TRIBAL-LEAK` for drafts and fails CI (`E-TRIBAL-LEAK`) at `candidate`: rewrite it actor-neutrally or move the Tribal part into a held enactment and tell TN. Never store site locations, consultation content or anything shared in confidence: CI fails on confidential markers and on coordinates next to cultural-site vocabulary anywhere in the repo.

## 9. No personal data (ADR-0012)

No names, e-mail addresses, phone numbers or person-level fields anywhere under `data/v2/`. Raters and agents are pseudonymous: `pid:<pseudonym>`, `panel:<id>`, `emstagent:<agent>@<version>`, `index:<name>`. Examples and fixtures are synthetic and say so.

## 10. Running validation

```bash
python scripts/build_schema.py --check     # schema current with vocab/
python scripts/validate_v2.py               # all data; exit 1 on any error
python scripts/validate_v2.py --json /tmp/report.json   # full list, filter by your ids
python validation/lint_indicators.py data/v2 --tools-lexicon data/v2/tools/tools.jsonl   # IO's full lint report
python -m pytest -q                         # tests, incl. seeded-violation fixtures
```

Issue codes you will meet: `E-SCHEMA` (field missing, wrong value, unknown field), `E-LOCATION` (wrong folder/file name/module), `E-REF-DANGLING` (reference to a record that does not exist; `W-REF-PENDING` if it is a planned disposition target), `E-TEXT-HASH`, `E/W-LINT-TYPING` (product or instrument named in L1/L2 text), `E/W-LINT-INDICATOR` (banned construction B1–B12), `E/W-LINT-LENGTH`, `E-LLM-DRAFT` (agent content claiming review or validation), `E-COMPUTED-FIELD`, `E-TRIBAL-*`, `E-PERSONAL-DATA`, `E-DEPENDENCY-DIRECTION`, `E-LICENSE-V1`, `E-X1-STALE`. Lint on `seed-v1` records is reported as warnings: it is your rewrite worklist. Codes added by ADR-0029 are listed in section 12.

## 11. What not to do

- Do not edit `legacy/`, `data/v1_baseline/`, `vocab/`, `docs/decisions/`, `schema/emst.schema.json` (generated) or `data/v2/ids/registry.csv`.
- Do not type counts or summaries into records or documents; release notes and the README status block are generated.
- Do not set `recommended: true` on any pathway, `useClass: select` on any indicator, or a `validationStatus` above `draft`.
- Do not describe a partner as committed; do not name an L4 product or L5 instrument in L1/L2 text; do not name a competency after a programme (programme labels go in `altLabel`).

## 12. Changes since S0 (ADR-0029, CA rulings of 2026-10-23; SPEC 2.0.0-draft.2)

Schema `2.0.0-draft.2` is generated from the amended `vocab/`. Most S0 records stay valid; the items marked **adapt** need a change in records written before the rulings. Drafts get a warning; the same issue is an error at `candidate` and in `--strict` (release) mode.

| # | Change | What you do |
|---|---|---|
| 1 | **Competencies never list enactments; tasks never list tools.** `Competency.enactments[]` and `Task.tools[]` are computed inverses (`vocab/rules/inverse-links@1.1.0.yaml`): the build derives them from `Enactment.competency` and `Tool.servesTasks` and puts them in bundles and `views/inverse_links.json`. | **Adapt:** delete `enactments:` from competency files (drafts: `W-COMPUTED-FIELD-DEPRECATED`, ignored by the build; candidates: `E-COMPUTED-FIELD` and `E-SCHEMA`). `Task.tools` is `E-COMPUTED-FIELD` at once. Keep the link on the Enactment (`competency`) and the Tool (`servesTasks`). |
| 2 | **Quote `'yes'` and `'no'`** (and `on`/`off`) wherever they are values. The repository loader reads YAML 1.2, but other tools read YAML 1.1 and turn bare `yes` into `true`. | Write `answer: 'yes'`, not `answer: yes`. |
| 3 | **Renamed status fields (ratified):** `ChangeSignal.signalStatus` (watch \| active \| retired), `SeriesRecord.seriesStatus`, `Source.sourceStatus`; titles in `prefLabel`. `status` is always the editorial status. | Nothing if you already followed section 4. |
| 4 | **Seed-v1 records cannot become candidates.** `validationStatus: seed-v1` with `status` candidate, published or deprecated (or a minted ID that is superseded or withdrawn) is `E-SEED-CANDIDATE`; `mint_id.py promote` refuses it. | Rewrite the seed to v2 rules and set `validationStatus: draft` before asking for promotion. Seed-keyed superseded/withdrawn v1 stubs written by the migration are unaffected (CR-DE-004). |
| 5 | **Code lists moved into `vocab/`.** `toolType`, `instrumentType` (adds `agency-order`), `eventType` (adds `submitted-for-review`), DriverEvent `direction`, **`statusAfter` (now an enum of 13 instrument statuses, incl. `under-review`)**, `credentialType`, `closureType`, `pathwayType`, `resourceType`, FrictionRecord `direction`/`severity`/`basis`, `signalStatus`, Indicator `useClass` and RelevanceRating `objectScheme` are generated from vocab; `seriesStatus`/`sourceStatus` patterns too; `StateClassRecord.appointmentRoute` is an array of the listed routes. | Use the vocab notation exactly. A `submitted-for-review` event sets `statusAfter: under-review`, never an in-force status (`E-REVIEW-EVENT-STATUS`). |
| 6 | **New ID prefixes:** WatchItem `WCH`, SeriesRecord `SER`, StateClassRecord `SCR`. | Nothing; keep `seed:` keys until integration mints them. |
| 7 | **ChangeSignal typed fields** replace the interim `EMST-*` notation schemes: `signalFamily` (vocab `change_types.yaml#signal_families`), `independenceKey` (pattern `^[a-z0-9][a-z0-9-]{1,60}$`; active signals must use a key listed in `#independence_keys`), `registeredDeployment` (only with family `deployment`), `impact` (1–3), `scenarioSignposts` (`vocab:scenarios#SP-01` … `SP-12`), `pointsToward` (`SC1`… or `AX-n:<pole>`), `measure.baseline {value, ci95, n, note}` and `measure.sensitivity {weighting, value, baselineValue}`. `signalStatus: active` requires `signalFamily` and `independenceKey`. | **Adapt:** move each `notation: [{scheme: EMST-signalFamily …}]` value into its typed field and drop the notation (`W-NOTATION-INTERIM` on drafts, `E-NOTATION-INTERIM` at candidate). An unlisted key is `W-INDEPENDENCE-KEY-UNLISTED` on watch signals and `E-…` on active ones: ask LM/CA to list it. |
| 8 | **Organization targets:** `targetType: organization` with `targetId` `opm-agency:<code>` or `census-gov:<id>`; never Tribal (`tribalPrograms: false`, no Tribal `sectorActor`; `E-ORG-TARGET-TRIBAL`). Measures with `n < 5` are `W-ORG-SMALL-N` and suppressed in releases. | Use aggregates by sector actor for NGOs and firms; never name one. |
| 9 | **Signpost SP-12** (Tribal co-stewardship) is quarantined like `careFlag`: `I-SP12-QUARANTINE`, excluded from releases, never counted. | Route SP-12 readings through TN only. |
| 10 | **Evidence rule.** `scripts/rules/change_indicator.py` (change-indicator@1.0.0) counts **active** signals only; watch signals appear in the "what's coming" view. | Leave agent-seeded signals at `watch`; a named human reviewer sets `active`. |
| 11 | **Occupation-grain external-index exposure** (CR-LM-002): `raterType: external-index` with `externalSource.unit: occupation` targets a role: required `targetType` (RoleProfile \| RoleVariant), `targetId`, `crosswalkPath`, `crosswalkMinMatchType`; no `task`. Every other ExposureAssessment keeps `task` + `taskTextSha256`. `externalSource` needs `unit` (`onet-task` \| `dwa` \| `iwa` \| `occupation`), may carry `values` and `dispersion`; `matchedOnetTasks` (≥ 1) is required unless `unit: occupation`. External-index records may give `externalSource.values` instead of `technicalExposure`, and a partial `assessedAt` (`YYYY` or `YYYY-MM`); other raters use a full date. | Records licensed `LicenseRef-EMST-third-party-index-derived` stay in `data/v2/assessments/external/<index>/` and are excluded from every release output (counted in the notes). |
| 12 | **Exposure level distributions:** a `technicalExposure[]` item is either `{vector, level}` or `{vector, levelDistribution: {E0..E3}, basis}`; shares sum to 1 ± 0.01 (`E-LEVEL-DISTRIBUTION`). E-levels sort `E0, E2, E1, E3` (`vocab/exposure_instrument_v2.yaml#…ordinal_order`), never by code. | |
| 13 | **Publication-rule checks:** `pass` on `existence` or `consensus` needs `evidence` (≥ 1). IO's PUB-14 also rejects `pass` without human evidence. **PR-2:** an Indicator at `candidate` or later, above the lowest level of its competency that has indicators (from the competency's `levels[]`), needs `distinguishingAttribute` (`E-PR2-ATTRIBUTE`). | Leave checks `pending` unless a human study supports `pass`. |
| 14 | **Lint waivers** live in `data/v2/governance/lint_waivers.csv` (`record_id, rule_id, text_sha256, waiver_class, reviewer, second_reviewer, decided_on, rationale`). A waiver applies only while the record id, rule id and normalized-text SHA-256 all match (`I-WAIVER-VOID` after an edit). Signers must be `pid:` humans (`E-WAIVER-SIGNER`); `false-positive` needs two different reviewers. Release notes count waivers by rule. | Agents never write waivers. Ask a named human reviewer. |
| 15 | **Role keys:** see section 3 (`W-ROLE-KEY`). | Key new RoleProfile/RoleVariant drafts that way. |
| 16 | **SSSOM:** `semapv:LLMBasedMatching` (SSSOM 1.1-only) is accepted as a declared extension and counted per set (`I-SSSOM-1_1-EXTENSION`). A reviewed agent-drafted row becomes `semapv:MappingReview` with `reviewer_id` and keeps `original_justification=semapv:LLMBasedMatching` in `other` (`W-SSSOM-REVIEW-PROVENANCE`). A row marked for selection use (`use=selection` in `other`) may never carry `LLMBasedMatching` (`E-SSSOM-SELECTION-1_1`). The build also writes a generated `sssom/strict-1.0/` rendering. | |
| 17 | **Computed views** are stamped from `vocab/rules/<ruleId>@<version>.yaml` (active version): counts, inverse links, effective use tier (caps: lifecycle, evidence, level rule, indicator lint, pathway), assessment staleness (task and competency hashes), change indicators, display gate (via IO's `decide()`), agreement results. | Never type their outputs into records. |

