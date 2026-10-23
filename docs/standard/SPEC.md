# EMST v2 Architecture Specification

**Environmental Management Skills Taxonomy, version 2 — normative specification**

- **Specification version:** 2.0.0-draft.2 · **Date:** 2026-10-23 · **Status:** Draft for Phase 4 implementation
- **Editor:** Chief Taxonomy Architect (CA) · **Decision basis:** ADR-0001 … ADR-0029 in `docs/decisions/`
- **draft.2 changes:** the CA rulings on change requests CR-DE-001…003, CR-IO-001…003, CR-LM-001…003 and CR-IA-001…002 (ADR-0029). The changed sections are §4, §5.1–§5.5, §5.12–§5.17, §5.19–§5.20, §5.24, §8.2, §10.5, §11.3–§11.4, §12.1–§12.2, §14.3, §15 and §17.1.
- **Licence:** CC0 1.0 (ADR-0013)
- **Implementers:** Data Engineer & Repository Steward (DE) and Interoperability Architect / Skills Intelligence (IA) build to this document; every other role authors content to it.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are used as in RFC 2119. Where this specification and an ADR disagree, the ADR governs until this document is corrected by a change record.

---

## Contents

1. Purpose, scope and users
2. Design principles
3. Architecture overview: layers L0–L6 and modules
4. Common record model
5. Entity types and required fields
6. Facets
7. Crafts
8. Proficiency model
9. Sector actors, variants, enactments and frictions
10. Lifecycle, editorial status, protect and use tiers
11. Exposure and change model
12. Identifiers, versioning and supersession
13. Provenance and evidence
14. Stored versus computed
15. Crosswalks
16. Governed content: Tribal, personal and third-party data
17. Serialization, repository layout and exports
18. Conformance
19. What v2.0 contains, and what comes later
20. Glossary

---

## 1. Purpose, scope and users

### 1.1 Purpose

EMST v2 is an open, versioned, machine-readable taxonomy of the work, capabilities and roles of the environmental sector. It exists so that the sector can **see how its jobs are changing** and so that **people, skills and knowledge can move** between federal, state, local, Tribal, NGO, private and academic institutions (charter vision and theory of change).

### 1.2 What EMST describes

- **Work:** tasks people perform (L2), grouped into function-defined **role profiles** with sector-actor **variants** (L3).
- **Capabilities:** typed **competencies** with anchored proficiency **indicators** at the levels where each is practised (L1), and **knowledge statements** (L2).
- **Craft blends:** how much each task draws on **Field craft**, **Data craft** and **Statecraft** (§7).
- **Context:** sector actor, authority position, subsector and module, jurisdiction, credentials and frictions.
- **Change:** dated, attributed assessments and signals about tasks and roles, and the policy instruments that drive change (L5).
- **Connections:** versioned crosswalks to O*NET, SOC, ESCO, OPM series, state classes, CIP, credentials and private job architectures (L6).

### 1.3 What EMST does not do

EMST MUST NOT rank, score, screen or select people; MUST NOT hold person-level data (§16.2); MUST NOT define, describe, rank or credential Indigenous knowledge (§16.1); and is not a classification basis, a job analysis, or an input to RIF, adverse action or performance rating decisions. An employer's selection use is defensible only after its own job analysis confirms the content (ADR-0024).

### 1.4 Users and the views they get

| User | First job | Entry point (generated view) |
|---|---|---|
| Federal HR specialist / classifier | job analysis, SME-QA benchmarks, PD language | Federal Series Profile (by OPM series and indicative grade band) |
| State HR / classification analyst | class specs, MQs, federal-equivalency hiring | State Class View; federal-to-state crosswalk |
| Training officer / NGO programme lead (pilot U1) | development plans, onboarding, reskilling | Role Change view; local-first Gap check; Pathways (exploratory) |
| Curriculum lead / accreditor | programme mapping, outcomes | Competency-level outcomes (CLOs); accreditation crosswalks; credential bundles |
| Early-career worker / career mover | "where can this lead?" | Role Change and Pathways views with frictions |
| Workforce strategist / researcher | planning, forecasting | "What's coming" view; computed indicators; full data download |
| Systems integrator (HCM, LMS, registries) | import, alignment | CSV skills library + delta feed; JSON-LD; CTDL-ASN; CASE; RSD |

Users enter by **role** and see 10–20 relevant competencies with depth one click down; the full faceted graph is downloadable, not the navigation (ADR-0027).

### 1.5 Audience order

Federal and state first (training, curriculum, workforce strategy); an NGO pilot kit; nobody shut out — the sector-actor vocabulary, subsector modules and Tribal protocol exist from v2.0 so later actors join without restructuring.

---

## 2. Design principles

1. **Type every entity by what kind of thing it is** — work, worker capability, context, event, mapping (ADR-0003).
2. **The spine is the task-and-role graph; competencies are first-class packages linked to tasks** (ADR-0001).
3. **Store observations and decisions; compute summaries** (ADR-0021).
4. **Every judgment is a dated, attributed assessment with a rater, method, confidence and the hash of the text rated** (ADR-0008).
5. **Durable over trendy:** named tools, products, models and instruments live in fast layers; core text names functions (ADR-0003 T-1…T-7).
6. **Observable and assessable:** indicators name observable behaviour with a condition and a standard; years are never a level (ADR-0004).
7. **Portable across sector actors:** function over institution; sector actor is context on variants, except obligations owed to Tribal nations, which are core content (ADR-0007).
8. **Different layers change at different speeds,** pinned together in each release (ADR-0009, ADR-0010).
9. **No public claim ahead of evidence:** every published number carries its evidence tier and denominator (ADR-0027).
10. **Depth in modules, simplicity in the core** (ADR-0018).

---

## 3. Architecture overview

### 3.1 Layers

| Layer | Contents | Cadence | Section |
|---|---|---|---|
| **L0 Reference vocabularies** | crafts; proficiency levels and attributes; sector actors and subtypes; industry; ownership; delivery model; authority positions; sign-off types; work functions, modes and workflow profiles; subsectors, clusters and modules; competency types; reusability levels; lifecycle states; editorial statuses; use tiers; evidence labels; validation statuses; exposure instrument codebook; scenario set; change types; mapping predicates; driver mechanisms; jurisdictional context; friction types | annual or slower; a change of meaning is MAJOR | §6–§11 |
| **L1 Competencies** | practice competencies, knowledge areas, transversal practice; indicators by level; enactments | annual MINOR | §5.2–§5.4 |
| **L2 Tasks and knowledge** | task statements; knowledge statements (incl. Awareness bundles) | within the annual MINOR | §5.5–§5.6 |
| **L3 Roles** | role profiles; role variants; job families; pathways | within the annual MINOR | §5.7–§5.10 |
| **L4 Tools, methods and technical standards** | software, platforms, models, instrument classes, protocols, technical standards, reporting frameworks | dated snapshots; quarterly review for short half-life entries | §5.11 |
| **L5 Change and evidence** | exposure assessments; craft, function and relevance ratings; change signals; watch items; instrument registry and driver events; scenario-conditioned rows; friction records | continuous with review; snapshots pinned per release | §5.12–§5.18, §11 |
| **L6 Crosswalks and registers** | SSSOM mapping sets; credential register; OPM series register; state class records | track upstream; ≥ quarterly | §5.19–§5.21, §15 |
| **Learning (cross-layer)** | learning resources; credential bundles (computed views with stable IDs) | MINOR | §5.22–§5.23 |
| **Provenance** | sources; change records; decision records; ID registry | every change | §12–§13 |

### 3.2 Core and modules

- The **core** holds L0, transversal practice, cross-subsector competencies and tasks, the cross-cutting practice areas (environmental review; compliance inspection and enforcement; community programmes; education and communication; research; environmental data and geospatial), and core role profiles.
- A **module** is a namespaced bundle of subsectors with a steward (or, until v2.2, an advisory partner) and its own review cycle. Modules use the core schema and core vocabularies; module records MAY reference core records; **core records MUST NOT depend on module records**.
- **Core vs module (three-module rule):** a competency is core if the same task core is enacted in three or more modules and differs only in knowledge base or regulatory regime; otherwise it has exactly one **home module** — the module whose regulatory regime governs the legal sufficiency of its deliverable — with enactments elsewhere (ADR-0003 G-4, ADR-0018).
- The 19 modules and their namespaces are listed in `vocab/modules.yaml`. Wave 1 (v2.0): `water`, `waterq`, `air`, `waste`, `envhealth`, `hazards`, `forest`, `wildlife`, `parks`.

---

## 4. Common record model

Every stored record (except mapping rows, which follow SSSOM, §15) MUST carry the common base:

| Field | Type | Req. | Notes |
|---|---|---|---|
| `id` | EMST ID (§12) or `seed:` key before `candidate` | MUST | |
| `type` | entity type name (§5) | MUST | fixed at minting |
| `prefLabel` | language map; `en` required | MUST | title |
| `altLabel` | language map of arrays | MAY | search aliases (incl. programme names, ADR-0016) |
| `definition` | language map | SHOULD; MUST on VocabularyTerm and on authored Competency, RoleProfile, RoleVariant, JobFamily and Pathway | Indicator `statement` and Enactment `note` serve as their definitions (CR-DE-001 #6) |
| `scopeNote`, `editorialNote` | language map | MAY | |
| `notation` | array of `{scheme, value}` | MAY | v1 aliases: `{scheme: "EMSTv1", value: "2.1.1"}` |
| `layer` | `L0`…`L6`, `learning` | MUST | |
| `module` | module namespace or `core` | MUST | where the record currently lives (distinct from the ID's minting namespace) |
| `status` | editorial status (§10.1) | MUST | |
| `lifecycleState` | lifecycle state (§10.2) | MUST for L1–L4 | |
| `useTier` | use tier (§10.4) | MUST for L1–L3 | stored as the *declared ceiling*; the effective tier is computed |
| `validationStatus` | validation status (§10.5) | MUST for L1–L3 | |
| `versionIntroduced`, `lastChangedIn` | taxonomy SemVer | MUST once published | |
| `replaces`, `replacedBy` | arrays of IDs | MUST when superseded | `status = superseded` requires `replacedBy` |
| `changeNote` | array of `{release, note}` | SHOULD | |
| `license` | SPDX ID | MUST | `CC0-1.0` unless governed (§16) |
| `sensitivity` | `public | restricted-governed` | MUST | governed content cannot be `public` without approval |
| `indigenousDataFlag`, `approvalStatus`, `aiUsePermitted`, `governedData` | see §16.1 | MUST when applicable | |
| `reviewBy` | ISO date | MUST when `lifecycleState ∈ {watch, proposed, emerging}` (§10.2) | |
| `v1Domain`, `v1SkillArea` | `{code, label}` | MAY | legacy facets (§6.8) |
| `provenance` | object (§13) | MUST | |

Records MUST be closed objects: unknown fields are rejected. **Computed fields (§14) MUST NOT appear in source records**; they appear only in release bundles and views.

**Seed records.** A record with `validationStatus = seed-v1` must carry the common base, but the type-specific MUST fields of §5 apply only when `validationStatus ≠ seed-v1`: seeds cannot honestly supply v2 judgments. The validator lists each seed's gaps. Seed-v1 records are never released, and a record cannot move to `candidate` while it is `seed-v1` (CR-DE-001 #7).

**Field names.** No type-specific field reuses a common-base name: a type's own status is named for its type (`signalStatus`, `seriesStatus`, `sourceStatus`), and no type has a `title` field, because `prefLabel` is the label (CR-DE-001 #1–#2).

---

## 5. Entity types and required fields

Field names are the terms of `schema/emst.context.jsonld`. "Req." gives MUST (M), SHOULD (S) or MAY (O) beyond the common base.

### 5.1 `VocabularyTerm` (L0)

`inScheme` (M; one of the vocabularies in `vocab/`), `notation` (M; the common-base array with at least one entry `{scheme: <the vocabulary's scheme>, value: <short code>}`, e.g. `[{scheme: work_functions, value: WF-OPERATE}]`; vocabulary files write the short code as a string and the build converts it; CR-DE-001 #3), `definition` (M), `broader` (O), `ordinal` (O; for ordered scales), `examples` (S), scheme-specific attributes (e.g. crafts carry `components[]` and `test`). Each scheme file carries `schemeVersion` and `lastReviewed`.

### 5.2 `Competency` (L1)

| Field | Req. | Content |
|---|---|---|
| `competencyType` | M | `practice | knowledge-area | transversal` (`vocab/competency_types.yaml`) |
| `statement` | M | ≤ 60 words; practice/transversal titles are verb + object (+ context); knowledge areas are noun phrases |
| `levelSpan` | M | `{min, max}` in L1–L5 (and `A` for an Awareness bundle) |
| `levels[]` | M for each level in span that is published | `{level, indicators[] (2–5 Indicator IDs), publicationRuleChecks{existence, distinctness, assessability, consensus}}`; each check is `{result ∈ pass \| fail \| pending \| not-applicable, evidence[], checkedOn}`, with `evidence[]` M when `existence` or `consensus` is `pass` (§8.2; CR-IO-001) |
| `transversalCluster` | M when `competencyType = transversal` | `TX-A`…`TX-F` (`vocab/competency_types.yaml`) |
| `awarenessBundle` | O | KnowledgeStatement IDs tagged `A` |
| `knowledge[]` | S | KnowledgeStatement IDs |
| `enactments[]` | — (computed) | **not stored**: each Enactment's `competency` is the one stored link; bundles carry the inverse (`inverse-links@1.1.0`; CR-DE-001 #9) |
| `v1Seed` | O | reference-only v1 text (four v1 levels mapped to L1–L4 with Knowledge/Application, source indicators with `v1Key`, sector notes); **stripped from every release**, never counted, displayed or used by a computed view (CR-DE-001) |
| `homeModule` | M | `core` or a module namespace |
| `subsectors[]` | O | only where the competency is subsector-specific; otherwise computed from tasks |
| `reusability` | S | reviewed value of the computed suggestion (§6.4) |
| `protect` | O | `{decision: true, decidedBy, decidedOn, criteria[], rationale}` (§10.3) |
| `learningDesign` | S | `{assessmentContext, recommendedModes[], typicalHoursPerLevelStep, prerequisites[]}` |
| `typicalTimeToLevel[]` | O | descriptive only, from job-analysis data; never a criterion |
| `instrumentSensitivity[]` | O | Mechanism IDs (L0) with evidence (§11.6) |

Constraints: a competency MUST be linked from at least one Task (`Task.supports`); `useTier = select` requires at least one linked task with `critical = true` in a validated role variant (ADR-0001, ADR-0024). Titles MUST NOT name an L4 product or an L5 instrument (§5.11, T-4). There is no fixed number of competencies per area.

### 5.3 `Indicator` (L1; own ID for credential alignment)

| Field | Req. | Content |
|---|---|---|
| `competency`, `level` | M | parent and level |
| `statement` | M | one sentence: observable verb + specific object + condition + standard; ≤ 30 words (IO `indicator_writing_rules.md`) |
| `augmentationMode` | M | `unaided | assisted | supervisory` |
| `assessmentMethods[]` | M | from `vocab/friction_types.yaml#assessment_methods` (work sample, seeded-error work sample, structured interview with BARS, simulation, task-book observation, check ride, blind re-measurement, portfolio, knowledge test, record audit, 360 counterpart input) |
| `useClass` | M | `describe`, `develop` or `select` (`vocab/lifecycle_states.yaml#use_tiers.indicator_use_classes`) |
| `obs4` | M | 0–3 observability code; release thresholds: select requires 3 with no lint flags; develop requires ≥ 2 with an evidence plan; 0–1 never released as indicators |
| `evidenceTypes[]` | S | work products an assessor examines |
| `jurisdictionVariable` | M | boolean; if true, the standard is supplied by an enactment |
| `servedTasks[]` | S | Task IDs this indicator evidences |
| `distinguishingAttribute` | M once `candidate`, for indicators at any level above the competency's lowest level with indicators | the `vocab/proficiency_levels.yaml#attributes` term (`ATT-AUT`…`ATT-FOR`) on which it differs from the adjacent lower level (PR-2; CR-IO-001) |
| `evidencePlan` | M when `useClass = develop` and `obs4 = 2` | how the missing observability evidence will be obtained |
| `obs4Flags[]`, `safetyOrLegalCritical` | O | IO metadata (`obs4Flags` ⊂ {P, C, O, T}; `useClass = select` requires none) |
| `validationStatus` | M | §10.5 |

Indicators MUST NOT use the twelve banned constructions (internal-state verbs; level labels as content; reputation and influence; proxies; outcome guarantees; empty verbs; compound performances; adjective-only gradation; vendor names; hard-coded jurisdiction rules; traits; non-job-related access requirements). Adjacent levels MUST differ on a named attribute (§8.2). The set of indicators at one level is the **competency-level outcome (CLO)**.

### 5.4 `Enactment` (L1)

`competency` (M); `actorType` (M; sector actor or subtype); `authorityPosition` (O); `jurisdiction` (O); `authorityBasis` (M), `principal` (M), `accountabilityVenue` (M), `characteristicInstruments[]` (S; Instrument IDs), `typicalFrictions[]` (O; FrictionRecord IDs); `additionalTasks[]`, `indicatorVariants[]` (O); `note` (M). Enactments exist only where the actor, module or craft changes the performance. Module enactments and craft enactments (FC/DC/SC) use the same type with `enactmentKind ∈ {actor, module, craft}`.

### 5.5 `Task` (L2)

| Field | Req. | Content |
|---|---|---|
| `statement` | M | one imperative verb + object + condition or purpose; 8–30 words; no compound verbs; no product names (a tool *class* MAY be named when it changes the work condition) |
| `textSha256` | M (computed by build, stored for pinning) | SHA-256 of the normalized statement |
| `supports[]` | M | `{competency, strength ∈ {primary, contributing}}` |
| `workFunction` | M | one primary work function (§6.1); `modes[]` O |
| `workflowProfiles[]` | O | §6.1 |
| `knowledge[]` | O | KnowledgeStatement IDs |
| `tools[]` | — (computed) | **not stored**: L4 points to tasks (`Tool.servesTasks`); bundles carry the inverse (`inverse-links@1.1.0`; CR-DE-001 #8) |
| `fieldDependency` | M | `on-site-required | on-site-preferred | remote-capable | remote` |
| `formationDependency` | M | `yes | partial | no` |
| `reproductionRegime` | S | `{mentorshipDependence, cycleDependence, placeBoundness, credentialGate, currencyDecay}` (§7.4) |
| `credentialGates[]` | O | `{credential, kind ∈ {required, preferred, entry}}` |
| `signOffAuthority` | O | §6.6 |
| `accountabilityConstraint` | O | boolean + basis (human in responsible charge required by law) |
| `governedData` | O | `tribal` etc. (§16.1) |
| `homeModule`, `subsectors[]` | M, S | |
| `v1Tier` | O | legacy T1/T2/T3 position, provenance only |

Production tasks SHOULD be split from specification, review and defence tasks, and execution-to-protocol from adaptation in place, where both exist. Craft, exposure, function and relevance *judgments* are not fields on Task; they are L5 assessment records (§5.12–§5.13).

### 5.6 `KnowledgeStatement` (L2)

`statement` (M; testable proposition), `lowestLevel` (S; L1–L5 or `A`), `supports[]` (S; competencies), `assessmentMethods[]` (S; knowledge test, oral exam, explanation component).

### 5.7 `RoleProfile` (L3)

| Field | Req. | Content |
|---|---|---|
| `functionStatement` | M | independent of organization and tool |
| `primaryWorkFunction` | M | §6.1 |
| `roleLevels[]` | M | `{key ∈ {entry, journey, senior, lead, strategic}, levelBand: [Lmin, Lmax]}` |
| `taskBundle[]` | M | `{task, importance (1–5), timeShare (0–1), critical (bool), neededAtEntry (bool), formationTask (bool, reviewed value of the computed flag), roleLevels[]}` |
| `competencyTargets[]` | M | `{competency, targetLevel per roleLevel, importance, distinguishing (bool), criticalForSelection (bool)}` |
| `entryFrom[]`, `progressesTo[]` | S | RoleProfile or RoleVariant IDs |
| `homeModule` | M | |
| `jobFamily` | O | JobFamily ID (membership is computed; this field records an editorial override) |
| `lifecycleState` | M | `proposed`/`emerging` roles additionally MUST carry `evidenceSignals[]` (SIG IDs), `feederRoles[]` with competency deltas, `horizon`, `scenarioSensitivity`, `reviewBy`, `counterSignal` (FS §7) |
| `v1Seeds` | O | v1 example-position text with provenance |

### 5.8 `RoleVariant` (L3)

| Field | Req. | Content |
|---|---|---|
| `variantOf` | M | RoleProfile ID |
| `sectorActor`, `sectorActorSubtype` | M, S | §9 |
| `authorityPosition` | M | §6.5 |
| `industry`, `ownership`, `deliveryModel` | S (M for private variants) | §9.2 |
| `taskAdds[]`, `taskDrops[]`, `taskOverrides[]` | O | relative to the role's bundle |
| `instruments[]` | O | Instrument IDs that characterize the variant |
| `credentialGates[]`, `signOffAuthority` | O | |
| `toolsCommonlyRequired[]` | O | L4 IDs (private screens on named tools, ADR-0003) |
| `indicativeGradeOrBand` | O | `{scheme (GS, FWS, state range), band, label: "not a classification criterion"}` |
| `jurisdictionalContext[]` | O | §6.7 |
| `approvalStatus` | M for Tribal variants | `pending-tribal-review` until approved |
| `disclaimers[]` | M for federal and state variants | "not a classification basis / not a job analysis / not for RIF or rating decisions" |

**Separate role vs variant:** a separate RoleProfile MUST be created when a licence or certification defines a legal scope of practice that changes which tasks may be performed, or when importance-weighted core-task overlap with the nearest role is below 0.60 (ADR-0006).

### 5.9 `JobFamily` (L3)

`definition` (M), `boundaryCriteria` (S; carried from v1 family definitions where valid), `memberRule` (M; rule ID). Membership is computed; families are navigation only.

### 5.10 `Pathway` (L3/learning)

`fromVariant`, `toVariant` (M); `pathwayType ∈ {new-hire, upskill, reskill, cross-sector, baseline}` (M; `vocab/friction_types.yaml#pathway_types`); `gap[]` (computed in bundles); `outcomes[]` (Indicator/CLO IDs); `modes[]`; `assessmentPlan`; `sequence`; `recognitionOfPriorLearning[]`; `durationAndCost`; `formationCoverage` (computed); `alternativeFormationRoutes[]`; `frictions[]`; `validationStatus`; `recommended` (MUST be false until the pathway passes the M-03 validation gate, ADR-0023).

### 5.11 `Tool` (L4)

`toolType ∈ {software-category, software-product, platform, model, dataset-product, instrument-class, instrument-model, protocol, technical-standard, reporting-framework, credential-bound-standard}` (M; `vocab/competency_types.yaml#tool_types`); `vendorNeutral` (M); `productExamples[]` (O); `servesTasks[]`/`servesCompetencies[]` (M; **L4 points to L1/L2, never the reverse**); `maturity` (S); `expectedHalfLifeYears` (S); `replacementRisk` (S); `lifecycleState` (M; `watch | established | declining | withdrawn`, mapped from DC's `watch → active → legacy → retired`); `reviewTriggers[]` (S); `successor` (O).

Typing rules T-1…T-7 (ADR-0003) decide L1/L2 vs L4: substitution invariance; judgment-bearing evidence; half-life under two review cycles; reference direction; promotion only when a tool class creates a new judgment-bearing work product evidenced in ≥ 2 sector actors or ≥ 3 organizations; tools-layer change if a proficient practitioner meets the same anchors after brief familiarization; legal and policy instruments are L5 Instruments, not tools.

### 5.12 `ExposureAssessment` (L5)

| Field | Req. | Content |
|---|---|---|
| `task` | M, except occupation-grain external-index records | Task ID |
| `taskTextSha256` | M with `task` | hash of the exact statement rated; mismatch with the task's current hash marks the assessment **stale** |
| `targetType`, `targetId`, `crosswalkPath[]`, `crosswalkMinMatchType` | M for occupation-grain external-index records, otherwise forbidden | `targetType ∈ {RoleProfile, RoleVariant}`; a record has either a task or a role target, never both (CR-LM-002) |
| `roleVariant`, `sectorActor` | O | context |
| `instrument`, `codebookVersion` | M | e.g. `emst-exposure@2.0` |
| `raterType` | M | `expert-panel | sme | analyst | llm | external-index | v1-analyst` |
| `raterId` | M | pseudonymous |
| `assessedAt`, `method`, `confidence` | M | `assessedAt` MAY be a partial date (year or year-month) only for `external-index`, where it is the date of the index release; EMST's ingestion date is `provenance.generatedAt` |
| `technicalExposure[]` | M (construct a), except external-index records whose index has no E-level construct | `{vector ∈ {llm-cognitive, robotics, sensing, convergent}, level ∈ {E0, E1, E2, E3}}`; external-index records MAY give `levelDistribution {E0, E1, E2, E3}` (shares summing to 1 ± 0.01) with `basis` (how the index's labels map to EMST levels) instead of `level` |
| `sWatch` | O | XR-04: true when a supervises-system or system-executes claim lacks deployment evidence and is coded compressive |
| `tacitExperienceRequirement` | O | `Hi`, `Med` or `Lo` (codebook supporting attribute) |
| `deploymentMode` | S (construct b) | `human-executes | assisted | compressive | supervises-system | system-executes`; `deploymentStage ∈ {none, pilot, deployed-limited, deployed-scaled}`; `deploymentEvidence[]` (M if mode is `supervises-system` or `system-executes`) |
| `strategy` | O | `substitution | augmentation | augmentation-for-formation` |
| `noDeployedToolPerformsCore` | O | descriptive boolean |
| `shouldRemainHumanReason` | O | normative field, kept separate |
| `scenario`, `demandDirection`, `reproductionRisk` | O (construct c) | only for tasks above the exposure threshold or flagged formation tasks |
| `rationale` | S | |
| `externalSource` | M when `raterType = external-index` | `{index, release, unit ∈ {onet-task, dwa, iwa, occupation}, matchedOnetTasks[] (may be empty only when unit = occupation), aggregation, values{} (the index's own published numbers), dispersion (number or object), noExternalAnalogue}`; an external-index record carries `technicalExposure` or `externalSource.values`, or both |
| `v1Flags[]` | M when `raterType = v1-analyst` | e.g. `text_misaligned`, `reconstructed_d2`, `d2_divergent`, `reconciled_d6_2026_03`, `normative_h` |
| `v1Values`, `mappingRule` | M (`v1Values`), O (`mappingRule`) when `raterType = v1-analyst` | v1 codes verbatim (snake_case); the codebook rule that mapped them |
| `evidenceLabel`, `sources[]` | M | |

Codebook rules XR-01…XR-07 apply (§11.3). External-index values derived from datasets whose licence is unverified carry `license: LicenseRef-EMST-third-party-index-derived` and are excluded from the CC0 files and from every release bundle until the index's terms are entered in the third-party licence register (ADR-0013; CR-LM-002).

### 5.13 `CraftRating`, `FunctionRating`, `RelevanceRating` (L5)

Per-rater atomic ratings of a task (craft; work function; authority-relevant attributes) or of a competency–role relation (relevance), with the same rater, date, method, confidence and text-hash fields as §5.12. `CraftRating.scale ∈ {ordinal-0-2, constant-sum-100, nominal-defining}`; values `{FC, DC, SC}`. The representation is swappable without migration (ADR-0005). `RelevanceRating.objectScheme` comes from `vocab/evidence_labels.yaml#rating_object_schemes`. **v1 competency-level tags** (craft, workflow stage, family, reform flags, lenses, CLD) use `competency` + `competencyTextSha256` (and `subject` + `subjectTextSha256` on RelevanceRating), with the legacy `objectScheme` values `v1-family | v1-reform-flags | v1-ethical-lens | v1-cld`, **only when `raterType = v1-analyst`**. They are prior evidence, never v2 values (ADR-0008 §5; CR-DE-001).

### 5.14 `ChangeSignal` (L5)

Required: `targetType`, `targetId`, `measure{name, value, unit, ci95, n, denominator, baseline{value, ci95, n, note} (O), sensitivity{weighting, value, baselineValue} (O)}`, `observedPeriod`, `comparisonPeriod` (S), `geography`, `sectorActor` (S), `source`, `sourceRelease`, `corpus{version, sha256, license}`, `method`, `toolVersion`, `promptVersion` (if LLM), `crosswalkPath`, `crosswalkMinMatchType`, `linkerQuality{goldSet, precisionAt1, ci95}` (M if derived from automated linking), `direction`, `directionConfidence`, `drivers[]`, `steepCategory`, `novelty`, `reliability (A–D)`, `corroboration`, `priorityScore` (computed), `careFlag`, `tribalPrograms`, `personalData` (MUST be false), `evidenceLabel` (S until reviewed), `reviewStatus`, `reviewer`, `reviewBy`, `signalStatus ∈ {watch, active, retired}` (`vocab/change_types.yaml#signal_statuses`; renamed from `status`).

Evidence-rule fields (CR-LM-001):
- `signalFamily`: from `vocab/change_types.yaml#signal_families`.
- `independenceKey`: a slug naming the upstream dataset; its providers are listed in `vocab/change_types.yaml#independence_keys`.
- Both are M when `signalStatus = active`, and an active signal's key MUST be listed.
- `registeredDeployment`: boolean; only when `signalFamily = deployment`.
- `impact`: integer 1–3, the input to `priorityScore`.
- `scenarioSignposts[]`: `vocab:scenarios#SP-NN`.
- `pointsToward[]`: a scenario notation `SC1`…`SC4`, or an axis pole written `AX-n:<pole>`.
- `notation` MUST NOT carry the interim `EMST-*` schemes once a signal is `candidate`.

`targetType` is an entity type or `organization` (`vocab/change_types.yaml#signal_external_targets`):
- An organization `targetId` is `opm-agency:<code>` or `census-gov:<id>`.
- An organization target is never a Tribal government, Tribal organization or Tribal enterprise, and never a named NGO or private firm. Measures with n < 5 are suppressed.
- Organization signals never move a role change indicator directly.
- Occupation-grain signals attach to RoleProfile or RoleVariant through the X3 path, not as an occupation target.

`mvp-role:` ExternalRef targets are interim. The release gate excludes them.

### 5.15 `WatchItem` (L5)

`signals[]` (M; ≥ 2, or 1 high-priority), `hypothesizedEntity{type, label, functionStatement}` (M), `reviewBy` (M; +12 months), `outcome ∈ {open, promoted-to:<ID>, lapsed}`.

### 5.16 `Instrument` and `DriverEvent` (L5)

`Instrument`: `citation` (M), `instrumentType` (M; `vocab/driver_mechanisms.yaml#instrument_types`: statute, regulation, executive-order, agency-order, memo, guidance, court-decision, permit-programme, agreement-authority, disclosure-regime, state-hr-order, standard-with-legal-force), `jurisdiction` (M), `currentStatus` (computed from events), `mechanisms[]` (M; L0 driver-mechanism terms).
`DriverEvent`: `instrument` (M), `eventType` (M; `#event_types`: introduced | passed-chamber | enacted | proposed | submitted-for-review | interim | final | effective | enjoined | stayed | vacated | remanded | rescinded | decided | expired | sunset), `eventDate` (M), `jurisdiction` (M), `direction` (M; `#event_directions`: expands, contracts, reshapes), `statusAfter` (M; `#instrument_statuses`), `sources[]` (M), `evidenceLabel` (M), `recordedBy` (M), `reviewBy` (M). A `submitted-for-review` event never makes an instrument in force (CR-LM-001 #5–#7).

Tasks and competencies link to **mechanisms** (L0) through `instrumentSensitivity` edges with evidence; instruments link to mechanisms; sensitivity and venue applicability are computed (§11.6, ADR-0016).

### 5.17 `FrictionRecord` (L5)

`fromActor`, `toActor` (M), `fromVariant`, `toVariant` (S), `frictionType` (M; `vocab/friction_types.yaml`), `direction` (M; `#friction_directions`: from-to, to-from, both), `severity ∈ {blocking, costly, minor}` (M; `#friction_severities`), `basis ∈ {statute, regulation, policy, practice}` (M; `#friction_bases`), `movableBy[]` (S), `mitigation` (S), `asOf` (M), `jurisdiction` (O), evidence label and sources (M). Tribal frictions are recorded only as the Tribal Council decides.

### 5.18 Scenario-conditioned rows

Stored as `ExposureAssessment` construct (c) fields with `scenario` set to an L0 scenario term (`SC1`–`SC4`) and optional `strategy`.

### 5.19 `Credential` (L6 register)

`credentialType ∈ {licence, certification, certificate, position-qualification, mandated-training-record}` (M; `vocab/authority_positions.yaml#credential_types`); `issuer` (M); `issuingJurisdiction` (S); `legalBasis` (S); `scopeOfPractice` (S); `closureType ∈ {legal-licensure, regulation-mandated-training, voluntary}` (M; `#closure_types`); `renewal` (O); `reciprocity` (O); `ctid` (O); `issuerVerified` (M; boolean with date). Credentials are gates, never proficiency.

### 5.20 `SeriesRecord` (L6; OPM series register)

`seriesCode` (M; the series title is `prefLabel`); `seriesStatus ∈ {active, proposed-realignment, realigned-to:<code>, cancelled}` (M; `vocab/mapping_predicates.yaml#series_statuses`; renamed from `status`); `effectiveDate`, `successorSeries`, `qualificationStandardVersion`, `positiveEducationRequirement` (S); `events[]` (DriverEvent IDs). Old codes are kept as aliases; nothing is overwritten.

### 5.21 `StateClassRecord` (L6)

SL's minimal common fields (`vocab/state_class_fields.yaml`): MUST — jurisdiction and employer type; agency; class code, title and series; level index and supervisory status; spec effective date; work-description text (or a hash and URL where reuse is restricted); MQ text and MQ location; degree rule; licences with issuer and timing; pay basis, range and effective date; provenance; and the EMST mapping record (role variant, competency targets with level, match type, confidence, reviewer, review date). SHOULD — SOC code, EEO-4 category, bargaining unit, appointment route, substitution formula, residency, exam type, broad-class flag, position overrides, native crosswalk references. Records are dated and re-run each 1 July or on state-plan revision.

### 5.22 `LearningResource` (learning)

`resourceType` (M; `vocab/friction_types.yaml#learning_resource_types`), `provider` (M), `cip` (O), `teaches[]` (M; CLO/Indicator IDs with I/R/E level), `modes[]`, `hours`, `credentialOffered` (O), `currencyReviewBy` (S). Third-party text is summarized, not copied.

### 5.23 `Bundle` (learning; computed view with stable ID)

`workFunction` (M), `clos[]` (computed; 3–8), `emstRelease` (M), `currencyInterval` (computed from lifecycle and change velocity), `alignmentTargets` (OB 3.0 / CLR 2.0 rendering).

### 5.24 `Source`, `ChangeRecord`, ID registry

`Source`: `sourceId` (team schema 5.1 IDs or EMST SRC IDs), `prefLabel` (the title), publisher, date, URL, `sha256` (S), `rights` (M), quality, `sourceStatus` (M; `vocab/evidence_labels.yaml#source_statuses`; renamed from `status`). `ChangeRecord`: `changeType ∈ {E, C, S, D, X, T}` (M), affected IDs (M), `semverImpact` (M), ADR or decision reference (M), evidence (M for S and X: two independent sources incl. a demand signal or SME panel data), reviewer attestation (M for `editorial` meaning-preserving changes). The ID registry is append-only (§12).

---

## 6. Facets

All facets are L0 vocabularies. Facets are applied to **tasks** unless stated, and rolled up by computation.

### 6.1 Work functions, modes and workflow profiles (`vocab/work_functions.yaml`, `vocab/workflow_profiles.yaml`)

Thirteen work functions: `WF-ASSESS` Assess & sense; `WF-PLAN` Plan & design; `WF-REVIEW` Review consequences; `WF-RULE` Make rules & policy; `WF-AUTHORIZE` Authorize (sub-function `.delegated`); `WF-RESOURCE` Resource & finance; `WF-BUILD` Build & implement; `WF-OPERATE` Operate & maintain; `WF-MONITOR` Monitor & verify (sub-function `.attest` Report & attest); `WF-ENFORCE` Inspect, enforce & assure (sub-functions `.assist`, `.assure`); `WF-RESPOND` Respond & recover; `WF-LEARN` Learn & adapt; `WF-MANAGE` Lead & manage organizations.
Two cross-cutting modes: `MODE-ENGAGE` (with `relationshipType ∈ {public, stakeholder, client, intergovernmental, government-to-government}`; government-to-government relations are never public participation) and `MODE-RESOLVE`.
Ten workflow profiles; `WP-PROJECT` maps v1 S1–S6 (S1→PLAN, S2→REVIEW, S3→AUTHORIZE, S4→BUILD/OPERATE, S5→MONITOR, S6→LEARN).

### 6.2 Subsectors and modules (`vocab/subsectors.yaml`, `vocab/modules.yaml`)

44 subsectors in 9 clusters (W, P, H, E, C, M, L, U, X), polyhierarchical. Cluster X is core practice. 19 modules (MOD-01…MOD-18 with MOD-07a/b) with namespaces and waves.

### 6.3 Competency types (`vocab/competency_types.yaml`)

`practice`, `knowledge-area`, `transversal`.

### 6.4 Reusability (`vocab/competency_types.yaml#reusability`)

`transversal | cross-subsector | subsector-specific | role-specific`; computed suggestion from task links across modules, reviewed value stored on the competency.

### 6.5 Authority position (`vocab/authority_positions.yaml`; on role variants)

`regulator | resource-manager | regulated-party | service-provider | independent-verifier | funder | advocate | advisor-researcher`.

### 6.6 Sign-off authority (`vocab/authority_positions.yaml#sign_off_authority`; on tasks and variants)

`licensure | legal-signatory | regulatory-definition | accreditation | position-qualification`, each with Credential references. Missing sign-off is a blocking friction in mobility computations.

### 6.7 Jurisdictional context (`vocab/friction_types.yaml#jurisdictional_context`)

Categorical only: `trust-or-tribal-lands | treaty-reserved-rights-area | co-managed-area | delegated-program-jurisdiction | federal-lands | state-lands | private-lands`. It MUST NOT be implemented as a geographic layer of Tribal places.

### 6.8 Legacy facets

`v1Domain`, `v1SkillArea` on migrated records, for provenance and navigation only.

---

## 7. Crafts

### 7.1 Definitions (`vocab/crafts.yaml`)

- **Field craft (FC):** the capacity to perceive, measure, act and stay safe in a specific place — reading land, water, air, living systems and the engineered systems that hold, treat or move them, and producing the ground truth and physical interventions that other environmental work depends on. Formed through repeated, supervised exposure to real conditions; evidenced by performance in the field. Components FC-a perceptual expertise; FC-b measurement and sampling integrity; FC-c situated judgment and intervention; FC-d physical and operational skill; FC-e risk management in uncontrolled environments; FC-f place knowledge and temporal depth; FC-g working with people on the land.
- **Data craft (DC):** the disciplined capacity to turn observations of environmental systems into warranted evidence, models and decision support — designing what gets measured, stewarding data so it stays fit for use and properly governed, analysing and modelling with honest uncertainty, and putting results before decision-makers in a form they can act on — including specifying, validating, supervising and answering for AI-generated analysis. Irreducible contribution: **warrant**. Functions DC-ACQ Acquire; DC-STW Steward; DC-ANL Analyze & model; DC-INT Integrate & communicate; DC-ASR Assure & govern.
- **Statecraft (SC):** the learnable capacity to turn knowledge and public purpose into decisions that are authorized, legitimate, resourced and durable, working through law and administrative procedure, institutions, budgets and relationships across jurisdictions and sectors. Defining deliverable: **a commitment that holds**. Components SC1 legal-procedural fluency; SC2 institutional navigation and intergovernmental coordination; SC3 coalition, partnership and agreement building; SC4 negotiation and conflict resolution; SC5 public engagement and legitimacy; SC6 fiscal and appropriations craft; SC7 political judgment and timing; SC8 accountability and integrity; SC9 instrument design and drafting.

### 7.2 Rating rubric

Each task is rated per craft **0 (none) / 1 (supporting) / 2 (defining)**:
- **FC = 2** if *presence* holds and at least one of *physical consequence* or *ground-truth authority*; FC = 1 where field knowledge catches errors but intermediate performance is possible without it.
- **DC = 2** if the deliverable is an evidence product judged by its warrant and requires choosing or checking methods, not operating a tool.
- **SC = 2** if the deliverable is a commitment needing authority, legitimacy or agreement from another institution or the public that must hold over time.
- Several crafts may be 2; a task may have none at 2 (general professional practice).

Raters MUST code blind to parent competency, domain and any prior craft label; production values require ≥ 3 raters; agreement is Krippendorff's ordinal α with bootstrap CI (§10.5). The scale is provisional until the IO pilot reports; the schema accepts `ordinal-0-2`, `constant-sum-100` and `nominal-defining`.

### 7.3 Field and formation dependency

`fieldDependency` (must the work happen in place?) and `formationDependency` (must the expertise have been formed through field or institutional exposure, even if the task is now remote?) are task attributes separate from craft ratings.

### 7.4 Reproduction-regime attributes

`mentorshipDependence (L/M/H)`, `cycleDependence (none / seasonal / multi-year-or-rare-event)`, `placeBoundness (general / ecosystem-type / site-specific / system-specific)`, `credentialGate (none / internal-qualification / external-certificate / licence)`, `currencyDecay (L/M/H)`; `entryPathDependence` is computed from role profiles.

### 7.5 Blends

Competency blend = linked task ratings weighted by link strength; role blend = task ratings weighted by importance × time share; dominant craft is a display field only. Blends **describe** roles and **design** pathways; they are not the mobility similarity measure and are not shown about individuals until reliability thresholds are met (ADR-0005, ADR-0023).

---

## 8. Proficiency model

### 8.1 Scale (`vocab/proficiency_levels.yaml`)

Five levels — **L1 Supervised, L2 Independent, L3 Senior, L4 Lead/Expert, L5 Strategic** — defined once on seven attributes: autonomy; guidelines and judgment; complexity; scope and influence; knowledge application; augmented practice (tools and AI); formation of others. **Awareness (A)** is a knowledge bundle, not a level.

### 8.2 Rules

1. Each competency declares a level span. The four publication rules are: PR-1 existence in job-analysis data (≥ 20% of incumbents at that level rate it important or above); PR-2 distinctness on a named attribute (`Indicator.distinguishingAttribute`); PR-3 assessability (≥ 2 indicators at OBS-4 = 3 for the use class); PR-4 consensus (Delphi placement ≥ 70% modal, IQR ≤ 1). Each result is recorded as `pass | fail | pending | not-applicable` (§5.2). **Anchored indicators are published at a level when the rules that the record's use tier requires pass** (ratified tier mapping, `validation/indicator_lint_rules.yaml#publication_rules.tier_requirements`; CR-IO-001):

   | Tier | PR-1 | PR-2 | PR-3 | PR-4 | OBS-4 minimum |
   |---|---|---|---|---|---|
   | describe | pass or pending | pass | pass or pending | pass or pending | ≥ 2 |
   | develop | pass or pending | pass | pass (≥ 2 at OBS-4 = 3) | pass | ≥ 2, with evidence plan |
   | select | pass | pass | pass | pass | 3, double-coded by humans, no lint flags |

   `pass` on PR-1 requires an indicator at that level with `validationStatus ≥ job-analysis-confirmed`, and `pass` on PR-4 requires `≥ panel-retained`; both cite `evidence[]` (lint PUB-14). Views show "level placement pending validation" wherever PR-1 or PR-4 is `pending`. Until a Delphi has run, no level is develop-grade. An empty level is information, not a gap.
2. L5 is defined only where SME panels confirm strategic demand.
3. Indicators carry `augmentationMode`; where career-ladder formation is at risk, unaided indicators are retained at L1–L2 and dual-condition (AI-off/AI-on) assessment is used.
4. Three anchoring resolutions: generic descriptors (position classification); BARS (selection and promotion); entrustment-supervision 1–5 on task-book tasks (training and qualification).
5. Years are descriptive only (`typicalTimeToLevel`).
6. Role levels (entry, journey, senior, lead, strategic) are bands of L1–L5.

### 8.3 Crosswalks of scales (L6 only)

OPM five-point scales starting at Awareness: A→1, L1→2, L2→3, L3→4, L4/L5→5. Grades and pay bands appear only as `indicativeGradeOrBand` on variants with the label "not a classification criterion"; no grade-equivalence table is published. Licensure grades and NWCG/NIMS position qualifications map through module-specific anchors; the credential itself is a gate. Four-level drafts from v1 and craft leads map L1–L4 and are re-sorted between L4 and L5 by the attribute test.

---

## 9. Sector actors, variants, enactments and frictions

### 9.1 Sector actors (`vocab/sector_actors.yaml`)

`federal | state | local | tribal | ngo | private | academic` with subtypes. Tribal subtypes: federally recognized Tribe; inter-Tribal organization or consortium; Tribal college or university; Tribal enterprise; ANCSA corporation; Native Hawaiian organization; state-recognized Tribe. Sector actor attaches to employment context (variants, enactments, frictions, signals), never to a competency as a tag.

### 9.2 Industry, ownership and delivery model

Orthogonal to sector actor (`vocab/sector_actors.yaml#industry`, `vocab/sector_actors.yaml#ownership`, `vocab/sector_actors.yaml#delivery_model`). Utilities and consultancies are industries and delivery models, not sector actors.

### 9.3 Variants and enactments

A role variant shares its role's function and core task bundle (§5.8). A competency is performed differently by actor only where an `Enactment` says so (§5.4). Actor-specific competencies exist only when the deliverable differs in kind; four are authorized (ADR-0007): exercising Tribal sovereignty (Tribal authority only); the duty-holder side of government-to-government consultation; operating or overseeing delegated and assumed programmes; regulated-entity compliance across divergent regimes. **Obligations owed to Tribal nations are core Statecraft competencies for every actor**, under the content hold (§16.1).

### 9.4 Frictions

First-class `FrictionRecord`s (§5.17) on actor pairs and variant pairs; minimum types in `vocab/friction_types.yaml`.

---

## 10. Lifecycle, editorial status, protect and use tiers

### 10.1 Editorial status (`vocab/lifecycle_states.yaml#editorial_statuses`)

`draft → candidate → published → deprecated | superseded | withdrawn`. Persistent IDs are minted at `candidate`; IDs are stable from `published`.

### 10.2 Lifecycle state (`vocab/lifecycle_states.yaml`)

`watch` (L5 only) → `proposed` → `emerging` → `established` → `declining` → `withdrawn`; plus `lapsed` (watch expired) and `merged`. Entry thresholds and review-by intervals are defined in the vocabulary (ADR-0015). Every `proposed` or `emerging` record MUST carry `reviewBy`.

### 10.3 Protect overlay

A stored governance decision on L1–L3 records (and L2 where useful), made when at least two criteria hold: severe failure consequence (life safety, legal duty, irreversible ecological harm, broken trust); reproduction takes ≥ 5 years; supply fragile in ≥ 2 scenarios. A protected record cannot move to `withdrawn` without Editorial Board approval and sector consultation. Tribal-related protect decisions require Tribal Council consent.

### 10.4 Use tiers (`vocab/lifecycle_states.yaml#use_tiers`)

`exploratory | describe | develop | select`. **Effective use tier** (computed) = the minimum of the lifecycle cap (watch/proposed → exploratory; emerging → develop; established → select), the evidence met under ADR-0024, and the reliability gate for any tag shown.

### 10.5 Validation status and reliability gates (`vocab/lifecycle_states.yaml#validation_statuses`)

`seed-v1 | draft | reviewed | panel-retained | job-analysis-confirmed | criterion-supported`. Tags shown to users require Krippendorff's α lower bound ≥ .667 (shown as tentative below .80); values below .667 are not shown.

**Display gate** (`vocab/rules/display-gate@1.0.0.yaml`; parameters in `validation/display_gates.yaml`; CR-IO-002). Views render gated values only through it.

1. **Unmeasured is not shown.** With no admissible study the view shows "Assessment pending".
2. **Admissible study.** All of the following:
   - human rater types only;
   - ≥ 120 units;
   - ≥ 3 distinct raters (the design target stays 120–200 units × 6 raters);
   - ≥ 2 pairable values per unit;
   - unit bootstrap of ≥ 10,000 resamples, decided on the 2.5th percentile;
   - pre-registered and blind;
   - same codebook version as the values;
   - lapses after 36 months.

   Any `llm`, `external-index` or `v1-analyst` rater in the counted set makes the study inadmissible. An LLM coder becomes admissible only by passing IO's LLM-coder gate **and** a reviewed change record, and never for `select` values.
3. **Strata.** A module or sector-actor stratum with ≥ 30 study units needs its own lower bound ≥ .667.
4. **Weak categories.** A category with one-vs-rest point α < .50 (on ≥ 10 units) is capped at tentative.
5. **Production and tentative.** Production values need a consensus of ≥ 3 human raters. Tentative values need ≥ 2 agreeing human codes or an adjudication. Select views admit production values only.
6. **Editorial fields** are labelled "editorial" and not α-gated: RoleProfile.primaryWorkFunction, RoleVariant.sectorActor, RoleVariant.sectorActorSubtype, RoleVariant.authorityPosition, Enactment.actorType, Competency.homeModule, Competency.competencyType, Competency.transversalCluster and Task.supports.
7. **Gated values:** every task-level rating, **including Task.workFunction**, and the assignment of external units (postings, PDs, state classes) to authority positions. Until a study reports, views navigate by the editorial RoleProfile.primaryWorkFunction. Gated values stay in the source records and the release bundle with their `validationStatus`.
8. **Verified facts** (credential gates, sign-off authority, accountability constraint) need E-labelled sources, not α. Without a source they are not shown.

---

## 11. Exposure and change model

### 11.1 Constructs

(a) **Technical exposure** by vector (llm-cognitive, robotics, sensing, convergent), E0–E3, scenario-invariant, dated; (b) **deployment mode** by sector actor (human-executes, assisted, compressive, supervises-system, system-executes) with deployment stage and an adoption **strategy** tag; (c) **outcome** — staffing outcome at role or organization level, and scenario-conditioned demand direction and reproduction risk only for tasks above an exposure threshold or flagged as formation tasks.

### 11.2 Scenario set (`vocab/scenarios.yaml`)

SC1 Assured Augmentation; SC2 Human Premium; SC3 Platform Stewardship; SC4 Patchwork Retreat (capacity rebuilt/coordinated vs thin/fragmented × AI trusted/assured vs brittle/contested); versioned, refreshed every 3 years.

### 11.3 Codebook v2 (`vocab/exposure_instrument_v2.yaml`)

XR-01 blind coding; XR-02 descriptive and normative fields separate; XR-03 Ac is time compression, never headcount; XR-04 system-executes and supervises-system claims require deployment evidence, else compressive with `sWatch`; XR-05 governed-data conditionality; XR-06 aggregate external matches and show dispersion; XR-07 module tasks assessed before sector-wide conclusions.

E-level codes are labels, not ranks. Their intensity order is `ordinal_order: [E0, E2, E1, E3]`, used for ordinal α (with nominal α reported alongside) and for every sorted display. Scenario rows apply to tasks with any vector at E1, E2 or E3, or with deployment mode compressive or higher, or to flagged formation tasks (CR-IO-003).

### 11.4 External measures

Ingested as `ExposureAssessment` with `raterType = external-index`, keyed to O*NET tasks and releases: Eloundou et al. E-labels and T-rubric; Anthropic Economic Index usage and collaboration shares (six numbered releases through 2026-06-26), labor-market-impacts and robot-exposure datasets; Microsoft "Working with AI" applicability; BLS AI exposure categories (2025–35 projections); OMB AI inventory deployment stage on functions. Context only: AIOE, Webb, ILO WP 140, WEF. Benchmarks only: Canaries, Humlum–Vestergaard. No change indicator may rest on a single vendor's data. Upstream providers are recorded per `independenceKey` (`vocab/change_types.yaml#independence_keys`).

Until X2 task matches exist, occupation-level index values attach to RoleProfile or RoleVariant through the X3 path, as occupation-grain records (§5.12; CR-LM-002). In views they appear only as context labelled "Occupation-level external index; not specific to this role's tasks", with dispersion, the index release and the match type. Values matched more broadly than `skos:closeMatch` appear only in the evidence drawer. They are never averaged across indices and never appear in select views.

### 11.5 v1 values

Migrated as `raterType = v1-analyst`, `raterId = v1-analyst-01`, low confidence, with misalignment flags; prior evidence only; never displayed as v2 values or aggregated into public numbers.

### 11.6 Signals, instruments and the evidence rule

Change signals (§5.14) move a computed change indicator only under the two-family, two-period, close-match, driver-tagged, human-reviewed rule (ADR-0028); otherwise they remain `watch`. Instruments and dated driver events, joined to L0 mechanisms through sensitivity edges, replace v1's reform flags; competency and role sensitivity and **venue applicability** (incl. `federalApplicability ∈ {required-basis, permitted, no-current-basis}` with `asOf`) are computed.

### 11.7 Computed indicators

Exposure distributions; CLD at task, role and pathway level with driver attribution and top-of-ladder loss; entry-path health; robustness class (robust / contingent / fragile) and scenario-sensitivity profile; robustness replaces v1's stability tier, which is a stored summary and is not migrated (ADR-0011 rule 5, as amended; CR-DE-003).

---

## 12. Identifiers, versioning and supersession

### 12.1 ID form

```
compact: emst:<namespace>/<TYPE>-<6 Crockford base32><1 Luhn mod-32 check>
IRI:     https://w3id.org/emst/<namespace>/<TYPE>-<code>
```

- **Crockford base32** alphabet `0-9 A-H J K M N P-T V-Z` (no I, L, O, U); the check symbol is Luhn mod-32 over the same alphabet.
- **TYPE:** VOC, CMP, KNW, IND, TSK, ROL, VAR, ENA, FAM, TL, INS, EVT, CRD, LRN, PTH, BND, SIG, ASM, FRC, SRC, MAP, CHG, WCH (WatchItem), SER (SeriesRecord), SCR (StateClassRecord) (CR-DE-002 #1).
- **Namespace = minting authority:** `core`; registered module namespaces (`water`, `waterq`, `air`, `waste`, `ehs`, `envhealth`, `extract`, `energy`, `climate`, `hazards`, `markets`, `forest`, `wildlife`, `marine`, `worklands`, `parks`, `culture`, `built`, `lab`); reserved `tribal-<steward>`.
- Validation regex (`vocab/identifiers.yaml#form.regex`): `^emst:(core|[a-z][a-z0-9-]{1,30})/(VOC|CMP|KNW|IND|TSK|ROL|VAR|ENA|FAM|TL|INS|EVT|CRD|LRN|PTH|BND|SIG|ASM|FRC|SRC|MAP|CHG|WCH|SER|SCR)-[0-9A-HJKMNP-TV-Z]{7}$` plus check-symbol verification.

### 12.2 Minting

One writer (`scripts/mint_id.py`; `scripts/mint_ids.py` is an alias only) mints random 30-bit bodies from a CSPRNG into the append-only `data/v2/ids/registry.csv` (`id, type, namespace, minted_on, minted_by, status, superseded_by, first_release`) when a record reaches `candidate`; collisions are rejected and re-minted. Draft records use `seed:<free text>` keys, which may contain `/` (written `--` in file names). IDs are never reused and never re-pointed. CI rejects registry edits other than status transitions.

### 12.3 Derived identifiers

CASE identifiers, CTIDs (`ce-<uuid>`) and RSD UUIDs are UUIDv5 of the EMST IRI under the namespace UUIDv5(URL, `https://w3id.org/emst/`).

### 12.4 Supersession

Clarifying wording without changing meaning keeps the ID (PATCH with reviewer attestation, or MINOR). A change of meaning, split or merge mints new IDs; the old record becomes `superseded` with `replacedBy` and remains resolvable. Removal sets `withdrawn` with a change note; records are never deleted. Promotion of a module record to core keeps its ID and changes `module`.

### 12.5 Versioning

- **Taxonomy release:** SemVer. MAJOR — a published ID withdrawn without successor; a change to the meaning of an L0 term or the level scale; removal or rename of a schema field. MINOR — new entities, modules or terms; deprecations or supersessions with successors; new optional fields. PATCH — attested meaning-preserving edits; provenance or metadata fixes. Each change record declares `semverImpact`; CI fails a tag smaller than the largest declared impact.
- **Cadence:** PATCH as needed (crosswalks ≥ quarterly); MINOR annually in April; MAJOR ≤ once every 3 years with ≥ 12 months' notice; prior MAJOR supported ≥ 24 months.
- **Schema:** its own SemVer. **Fast layers** (L4, L5 signals and events): dated snapshots pinned per release. **Mapping sets:** `mapping_set_version` + pinned `object_source_version`. **Stewarded modules** (v2.2+): MINOR.PATCH inside a core MAJOR. No per-concept SemVer.
- Each release ships a **delta file** (added, changed, superseded, withdrawn IDs), a "does this affect me?" notice, DOI, SHA256SUMS, SBOM, signed artifacts and an accessibility conformance report.

---

## 13. Provenance and evidence

### 13.1 Provenance object (required on every record)

| Field | Req. | Values |
|---|---|---|
| `method` | M | `v1-migration | source-text-recovery | human-authoring | sme-panel | delphi | job-analysis | llm-assisted | rule | lexical-linker | import | computed` |
| `agent[]` | M | pseudonymous person IDs or `emstagent:` software agents with versions |
| `generatedAt` | M | ISO 8601 |
| `derivedFrom[]` | M when `method = v1-migration` | `{v1Key, v1Code, v1Table, v1Sheet, v1Row, v1Fields, workbookSha256, v1ProvenanceCode, sourceTextLine, relation ∈ {carried, rewritten, split-from, merged-from, recovered, prior-evidence, reference-only}}` |
| `sources[]` | M when `evidenceLabel = E` | source IDs resolving to a `sources.csv` or Source record |
| `evidenceLabel` | M | `E | J | S` (`vocab/evidence_labels.yaml`) |
| `confidence` | S | 0–1 or ordinal |
| `reviewStatus` | M | `unreviewed | spot-checked | reviewed | validated | gold` |
| `reviewers[]`, `reviewedAt` | S | |
| `interRaterAgreement` | S | `{statistic, value, ci95, nRaters, nUnits}` |
| `toolVersion`, `promptVersion` | M when LLM-assisted | |
| `adr` | S | decision record reference |

### 13.2 Evidence standard

Every substantive claim is labelled **E** (supported by a cited source actually read), **J** (expert judgment with its basis), or **S** (speculation with what would confirm or refute it). An `E` label without a resolvable source is invalid. LLM-assisted content is labelled as such and passes IO's gate before it can carry a selection-relevant value.

---

## 14. Stored versus computed

### 14.1 Stored (source records)

Authored text; per-rater atomic ratings with instrument version, date, rationale, text hash and confidence; links (task → competency, role → task bundle, role → competency targets, task → tool, task → mechanism, enactments); dated events and signals; mappings; credentials and registers; change records, decisions, the ID registry; protect and lifecycle decisions.

### 14.2 Computed (build only; never in source)

Per-task consensus values; competency and role exposure distributions; craft blends and dominant craft; competency roll-ups of work function and subsector; reusability suggestions; family relevance, breadth and job-family membership; CLD (task, role, pathway) with driver attribution; entry-path health; robustness class and scenario sensitivity; instrument sensitivity and venue/federal applicability; Federal Series Profiles and State Class Views; pathway edges, directional coverage, pathway scores and formation coverage; bundle contents and currency; effective use tier; agreement statistics; priority scores; inverse links; all dashboard, README, release-note and documentation counts; the data dictionary.

### 14.3 Rules

Each computed view is produced by a versioned rule (`vocab/rules/<rule-id>@<version>.yaml`) and every view row records `ruleId`, `ruleVersion` and `buildCommit`. CI recomputes and compares. Release CSVs include all computed views. A rule change is a reviewed change record whose effects are reported in release notes.

**Rule files (CR-DE-003; ADR-0029 §4).**
- `vocab/rules/` is the only home for computed-view rules. Each file carries `ruleId`, `version`, `status`, `steward`, `decidedIn`, `computes`, `inputs`, `definition`, `outputs`, `parameters` and `implementation`.
- The rule file is the normative definition; the code lives in `scripts/` (or `validation/` for IO's display gate).
- A rule may delegate thresholds to a stewarded parameter file pinned by path and SHA-256.
- CI fails when a view stamps a `ruleId`/`ruleVersion` with no rule file, or when a rule file names an `implementation` that does not exist.
- Superseded rule versions are kept, so past builds stay reproducible.

---

## 15. Crosswalks

- **Format:** SSSOM 1.0 mapping sets (1.1 slots, and the 1.1 justification `semapv:LLMBasedMatching` for unreviewed agent-drafted rows, as declared extensions; a human-reviewed row takes `semapv:MappingReview` and keeps `original_justification` in `other`; CR-IA-002), one per upstream version, TSV plus YAML metadata, with SKOS predicates, `predicate_modifier: Not`, `sssom:NoTermFound`, `semapv` justifications, calibrated `confidence` separate from raw `similarity_score`, author and reviewer IDs, and `object_source_version`. A flattened CSV is shipped for HR users.
- **EMST relation predicates** (`vocab/mapping_predicates.yaml`): `emst:replacedBy`, `emst:retiredWithoutReplacement`, `emst:splitInto`, `emst:mergedInto`, `emst:evidencesTask`, `emst:variantOf`, `emst:equivalentEvidence` (credential ↔ CLO).
- **Required sets** (ADR-0022): X1 v1 → v2 (complete; CI-enforced); X2 task → O*NET 31.0 task/DWA (+ 27.x for Eloundou); X3 role variant → O*NET-SOC 2019/SOC 2018; X4 OPM series register; X5 state class records; X6 CIP and accreditation; X7 ESCO v1.2.1; X8 private reference job architecture; X9 OPM FWCI and USA Hire; X10 credential ↔ CLO equivalence; X11 public ↔ private translation; X12 TX-A floor and AI practice → DOL AI Literacy Framework (TEN 07-25, Feb 13 2026; official area names such as "Direct AI Effectively").
- **Upstream tracking:** on each upstream release (O*NET, ESCO, OPM issuances, SOC 2028, CIP), a CI job sorts rows into carry / needs-review / deprecated / new-candidate.
- **Thresholds by use:** selection contexts — two independent human reviewers and ≥ `closeMatch`; analytics — published coverage, predicate mix, κ and staleness; navigation — single-reviewed candidates labelled as such.
- **IDs only** for third-party systems in CC0 files; no alignment claim before a reviewed set exists.

---

## 16. Governed content: Tribal, personal and third-party data

### 16.1 Tribal content (ADR-0007)

Invariants: EMST MUST NOT (V1) define, describe, rank or credential Indigenous knowledge; (V2) hold confidential Tribal information, even under access control; (V3) publish characterizations of named Tribes without consent; (V4) ingest Tribal employers' documents or postings by default, including in LLM pipelines; (V5) create a Tribal profession family. Records touching Tribal governments, Indigenous knowledge or Tribal data carry `indigenousDataFlag = true`, `approvalStatus ∈ {pending-tribal-review, approved, withdrawn}`, `aiUsePermitted`, and `sensitivity = restricted-governed` until approved. **Until a Tribal Advisory Council exists and approves, nothing Tribal-related is published.** CI MUST fail release builds on unapproved Tribal-related records, on any confidential record, and on coordinates co-occurring with cultural-site vocabulary. Tribally stewarded namespaces carry the contributor's licence, labels and withdrawal right and are excluded from bulk CC0 unless opted in. The release states on its face that Indigenous knowledge is a distinct body of expertise held and governed by Indigenous nations and is out of scope by design.

### 16.2 Personal data (ADR-0012)

The EMST steward holds no person-level data. The schema has no person entity; person-level structures exist only as client-side file formats or Tier 2 kit schemas in adopters' authorized systems. Signals are de-identified at ingestion; rater identities are pseudonymous with maps held outside the repo; panel and Delphi data enter only as aggregates; observed transitions enter only as aggregates with n ≥ 5; small cells are suppressed.

### 16.3 Third-party content (ADR-0013)

Third-party text (O*NET, ESCO, AEI, accreditors, credential bodies, licensed posting data) is excluded from CC0 files; crosswalks store IDs only; any permitted third-party text lives in `external/` with its own licence and attribution; a third-party licence register ships with each release.

---

## 17. Serialization, repository layout and exports

### 17.1 Canonical source (ADR-0010)

```
vocab/                         L0 concept schemes (YAML; SKOS-exportable); vocab/rules/ for computed-view rules
schema/emst.schema.json        single JSON Schema 2020-12; enums generated from vocab/
schema/emst.context.jsonld     JSON-LD 1.1 context (field names = context terms)
data/v1_baseline/              frozen v1 (hash-pinned; never edited)
data/v2/core/<type>/<ID>.yaml  one authored record per file
data/v2/modules/<ns>/<type>/<ID>.yaml
data/v2/core/watch-items/<ID>.yaml   L5 watch items (one per file)
data/v2/tools/tools.jsonl
data/v2/assessments/<instrument>/<batch>.jsonl
data/v2/assessments/external/<index>/<batch>.jsonl   external-index assessments (CR-LM-002)
data/v2/signals/<yyyy>/<source>.jsonl
data/v2/instruments/instruments.jsonl   L5 instrument registry (CR-DE-001 #5, CR-LM-003)
data/v2/events/<yyyy>.jsonl
data/v2/crosswalks/<target>/<target-version>.sssom.tsv (+ .yml)
data/v2/registers/{credentials,opm_series,state_classes}/…
data/v2/governance/           CI-read governance state: licensing.yaml, tribal_hold.yaml, lint_waivers.csv (CR-IO-001)
data/v2/ids/registry.csv       append-only
data/v2/changes/<release>.jsonl
external/                      third-party material under its own licences
```

A seed key's `/` is written `--` in its file name. Authoring tools that write records, such as WP-10's builder in `docs/methods/scripts/`, stay in their owner's lane, must be deterministic, write only inside the lane, and are never invoked by CI or the release build. Code that CI or the build runs lives in `scripts/` with tests in `tests/` (CR-LM-003).

Source records are YAML using the JSON-LD context terms (YAML-LD); every record validates against the single schema; cross-record rules (referential integrity; registry append-only; text-hash staleness; sources resolve; v1 completeness; no module redefines a core ID; Tribal and personal-data checks) run in `scripts/validate_v2.py` in CI.

### 17.2 Generated exports (never hand-edited)

JSON-LD bundle (normative release serialization); CSV + Frictionless datapackage (incl. an HCM skills-library import file and a release delta feed); SKOS Turtle; SSSOM; CTDL-ASN (primary public linked-data channel; Credential Registry); CASE 1.1 (claimed only after validation against 1EdTech's schema); RSD; Open Badges 3.0 alignment targets (IRIs). Platforms that infer skills are asked to export their mappings to EMST IDs as SSSOM; no vendor ID is ever an EMST key.

---

## 18. Conformance

### 18.1 Data conformance (a release, a module or a fork)

A conforming dataset MUST: validate against `schema/emst.schema.json` at its declared schema version; use only L0 terms from the pinned vocabulary snapshot; carry provenance on every record; contain no computed fields in source records; mint IDs only in its own registered namespace; publish crosswalks as SSSOM; pass the Tribal and personal-data CI checks; and ship a delta file. Modified versions MUST NOT be called "EMST".

### 18.2 Module conformance

A module release MUST additionally: use the core schema, namespaced IDs and core vocabularies; reference core records only in the permitted direction; apply the three-module and home-module rules; run at least one review cycle per year on the core cadence; meet the core evidence standard; name an SME pool and contact; and carry no separate licence.

### 18.3 Adopter claims

- Anyone MAY say they "use" or "map to" EMST with a release ID.
- "EMST-mapped" (an adopter artifact whose items carry EMST IDs and release) and "EMST-conformant" (a dataset or tool meeting §18.1) claims require a published conformance check.
- An adopter using EMST content in selection MUST cite the release and the use tier, and MUST rely on its own job analysis.

### 18.4 Content-authoring conformance

L1/L2 text passes the typing lint (no L4 products or L5 instruments named), the indicator lint (twelve banned constructions), the naming rule (function-based titles; programme labels as aliases), and IO's publication rules for each published level.

---

## 19. What v2.0 contains, and what comes later

### 19.1 v2.0 (target: 2.0.0-rc.1 for the NGO pilot and design partners, Q1 2027; 2.0.0 after the first comment window)

- All L0 vocabularies in `vocab/` at version 1.0.
- **Core:** ~120–180 competencies (practice, knowledge areas, transversal), migrated from v1 per `docs/decisions/v1_disposition.csv` and from the core candidates in `docs/decisions/candidate_disposition.csv`, with task links and anchored indicators at `develop` tier where IO's develop-use evidence is met, otherwise `describe`.
- **Wave-1 module editorial sections:** `water`, `waterq`, `air`, `waste`, `envhealth`, `hazards`, `forest`, `wildlife`, `parks` — centrally authored with advisory partners.
- **Roles:** 37 role profiles (`docs/decisions/mvp_role_set.csv`): 13 corridor roles at full depth; 17 federal/state design-partner roles at starter-kit depth; 6 emerging roles in the "what's coming" view; 1 sector-extension role.
- **L4** seed (~53 entries from DC plus FC field instruments and PS reporting tools) and **L5** seeds (instrument registry and driver events; v1 prior-evidence assessments; external-index assessments where X2 matches exist; signals from OpenLMP, the OMB inventory and OPM FWD).
- **L6:** X1 complete; X3, X4, X5 (pilot states) and X7 at reviewed-subset level; X2 for the P1 corridor tasks; credential register seeded and partly verified.
- **Views:** Role Change, Gap check (local-first), Pathways (exploratory), What's coming; Federal Series Profile; State Class View; kits (0400 Kit, Job-Analysis Starter Pack, federal-to-state crosswalk).
- **No selection-grade content**, no Tribal-related content (held), no person-level data, no pathway labelled "recommended".

### 19.2 v2.1 (April 2028 MINOR)

Selection-grade content for the first function clusters after job analysis and linkage; craft-scale decision from the IO pilot applied; full PD builder; first annual Signals Review; wave-2 module sections begin (`ehs`, `extract`, `energy`, `climate`, `worklands`, `culture`, `built`, `lab`); SAF EPRC recognition sought.

### 19.3 v2.2+ (2029 onward)

Stewarded modules for partners that have signed agreements and completed two on-time cycles; wave-3 modules (`markets`, `marine`); Tribal content only as the Tribal Council approves; pathway recommendation for pathways passing validation; task-level NLP linking per family when DP-18a fires; SOC 2028 re-map; scenario refresh (2029).

---

## 20. Glossary

- **Authority position:** which side of a regulatory or resource relationship a role variant sits on (§6.5).
- **CLO (competency-level outcome):** the set of anchored indicators for one competency at one level.
- **CLD (career-ladder destruction):** loss of the entry-level formation tasks through which juniors build judgment; computed at role and pathway level.
- **Enactment:** a structured record of how a competency is performed differently by a sector actor, module or craft.
- **Formation task:** a task at entry level with a high or medium tacit or experience requirement — the work through which judgment is learned.
- **Home module:** the single module that owns a module-level competency.
- **Mechanism:** a durable L0 driver code (e.g. review scope, delegation, disclosure) that instruments act through.
- **Protect:** a governance decision preventing the withdrawal of a capability whose loss would be irreversible or dangerous.
- **Role variant:** a sector-actor-specific form of a function-defined role profile.
- **Use tier:** the uses a record may support — exploratory, describe, develop, select.
- **Watch item:** a cluster of signals and a hypothesized entity in L5, before any content exists.
