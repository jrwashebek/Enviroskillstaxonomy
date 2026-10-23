# Interoperability and skills intelligence for EMST v2 — IA report (Phase 2)

**Role:** IA (Workforce Systems Interoperability Architect + Skills Intelligence/NLP Engineer). **Date:** 2026-10-23. **Labels:** [E] evidence (source IDs resolve to `sources.csv`; CA-/FH- IDs resolve to those roles' files), [J] expert judgment, [S] speculation.

## 0. Summary

1. **Keep the repo as the only editable copy and generate every other format from it** [J]. The canonical store is a JSON-LD bundle (SKOS semantics, PROV provenance, a published context), validated by JSON Schema 2020-12, with crosswalks kept as separate SSSOM files. CTDL-ASN (main public linked-data channel), CASE 1.1, RSD, SKOS Turtle, a CSV bundle and Open Badges 3.0 alignment targets are all generated exports. This is the main guard against vendor lock-in. v1 had it backwards: a proprietary SaaS base was its only editable source [E: IA-035].
2. **Persistent IDs:**
   - Form: `emst:<namespace>/<TYPE>-<6 base32 + check>`, behind w3id.org IRIs.
   - The namespace names who minted the ID (core or a module steward).
   - v1 codes survive only as aliases.
   - Supersession follows NICE's Retained/New/Withdrawn pattern [E: CA-033].
   - CASE, CTDL and RSD identifiers are derived from the IRI, always the same way.
   - Worked examples for v1 2.1.1 and 6.1.2 in every format validate end to end.
3. **Standards stack.**
   - **Adopt:** SKOS, JSON-LD 1.1, JSON Schema, SSSOM 1.0 (1.1 slots as extensions), PROV, w3id, the OpenLMP provenance pattern, CTDL-ASN.
   - **Map to:** CASE 1.1, IEEE 1484.20.3-2022, RSD, OB 3.0, JDX JobSchema+, ESCO, O*NET-SOC 2019 / O*NET 31.0, SOC 2018, OPM series, CIP, Lightcast (licence permitting).
   - **Watch:** VC 2.0, LER/HR Open, JEDx, CASE Network, SOC 2028, NICE (as a design precedent), and the enterprise HCM skills engines.
   - Several items could not be verified this session (§1.2).
4. **Standing changes that matter:**
   - RSD and OSMT moved from WGU's Open Skills Network to Credential Engine (Feb 2025) [E: IA-007].
   - CASE 1.1 is final and public (Apr 2025) [E: IA-004].
   - VC 2.0 became a W3C Recommendation (May 2025) [E: IA-016].
   - O*NET is at 31.0 (Aug 2026), next update Nov 2026 [E: IA-017, IA-018, IA-020].
   - O*NET Web Services 2.0 supersedes 1.9 [E: IA-021].
   - SSSOM 1.1 is in pre-release; it adds an LLM-matching justification and reviewer agreement [E: IA-014].
5. **v1's only crosswalk has verifiable errors.** Two family→SOC code/title pairs are wrong (19-1012 is Food Scientists; 33-1021 is fire supervisors, not inspectors) and three targets look misdirected [E: IA-022]. There is no competency-, task- or role-level crosswalk at all.
6. **Prototype (runnable, one command).** A transparent fused lexical/semantic baseline links land-management-plan requirements to v1 competencies. On a 90-item gold set I labelled myself, blind to system output but as a single annotator, it reaches P@1 0.51 (95% CI 0.40–0.63) and Hit@5 0.85 (0.75–0.91) over 72 non-noise items. Held-out alone: P@1 0.48 (0.26–0.65). It is a **candidate generator for human review**, not an automatic coder.
7. **Uncertainty, reported plainly:**
   - Fixes I designed from dev-set errors (acronym glossary, masking of place and agency names) **lowered** held-out P@1 from 0.48 to 0.39.
   - The confidence bands I set in advance were not monotonic on dev.
   - A ranker-agreement signal was monotonic on both sets, but its high band is small (11 of 72).
   - 20% of sampled plan components were extraction noise. Neither confidence signal catches them reliably.
8. **What to link to: competencies now, tasks later.** Linking to v1's three-tasks-per-competency layer did worse than linking to whole competency documents (dev P@1 0.43 vs 0.53; Hit@5 0.61 vs 0.88). CA's task spine needs a much richer L2, crosswalked to O*NET tasks, first.
9. **Plan requirements reveal seven missing functions:** range/grazing, recreation and visitor management (recreation opportunity spectrum, travel), scenery, transportation/roads, minerals and energy authorizations, lands and realty, wilderness stewardship. My blind gold labels and unsupervised clustering of 5,994 low-similarity plan components agree on all seven.
10. **ESCO cannot stand in for EMST on US statecraft or wildland fire.** I reviewed 39 of 666 EMST→ESCO v1.2.0 candidates. 41% were rejected, many for homonyms ("prescribed", "invasive", "inventory"). ESCO has no Tribal-consultation, wildland-fire or AI-validation concept; these are recorded as `sssom:NoTermFound`.

## 1. Scope, method and evidence limits

### 1.1 What I did
- **Read:** the charter, team brief, CA's architecture hypotheses and audit; OpenLMP's SPEC, schema, context, data dictionary and evaluation; DE's v1 baseline; and three v1 documents (infrastructure guide, architecture/methodology export, forester PD page).
- **Researched:** 4 web searches and about 20 web fetches. Through the shell I read 15 GitHub repositories and 2 PyPI packages:
  - specification sources: SSSOM, Open Badges, VC 2.0, CTDL vocabularies, OSMT;
  - official code: O*NET Web Services samples;
  - paper repositories: SkillSpan, ESCOXLM-R, IReRa, Decorte benchmarks, MELO, Nesta.
- **Built:**
  - the data model, schema, context and worked examples;
  - a hash-pinned EMST→ESCO candidate crosswalk with a reviewed subset;
  - the v1 family→SOC sheet re-expressed as SSSOM with verification flags;
  - a reproducible linking prototype with a 60-item dev and 30-item held-out gold set;
  - a validation suite (all checks pass).

### 1.2 What I could not verify
- **Blocked access.** The shared web-search budget ran out after four searches. After that, fetches of URLs not already surfaced were permission-gated and declined. arXiv, ACL Anthology, the ESCO portal, Lightcast, USAJOBS, NIST and vendor documentation were unreachable.
- **Vendor ingestion paths** (Workday Skills Cloud, SAP SuccessFactors Talent Intelligence Hub, Oracle HCM, Eightfold) are unverified [IA-051]. CP hit the same limit (CP-066). Everything I say about them is [J]/[S] and must be tested in the pilot.
- **Other unverified standards:** HR Open/LER-RS versions, JEDx status, Lightcast Open Skills licence [IA-045, IA-049, IA-050].
- **ESCO current version:** I rely on CA (v1.2.1, Dec 2025 [CA-030]). My data is v1.2.0, inferred from an exact occupation-count match [E: IA-023, IA-024].
- **Papers:** IReRa, SkillSpan, ESCOXLM-R and Decorte were read through their repositories, not full text. Three widely cited LLM papers are background only (unverified) [IA-042–044].
- **No real job postings** could be obtained, and no other role had saved any. The PD path is shown on the v1-authored illustrative Forester PD, labelled as such [IA-037]. The USAJOBS adapter is specified (§6) but not run.

## 2. Standards and platforms: appraisal and recommended stack

The full table is `standards_appraisal.csv` (34 rows). The reasoning, by function:

**2.1 Semantics and serialization: adopt SKOS, JSON-LD and JSON Schema.**
- **SKOS.** ESCO's model is RDF/SKOS, and CTDL and the official ESCO–O*NET crosswalk use SKOS match predicates [E: IA-022, IA-012]. SKOS is the common denominator every target reads.
- **JSON-LD 1.1.** One file serves both as JSON for developers and as an RDF graph. Language maps give multilingual labels. The context expands the example bundle to 1,424 triples with no undefined terms.
- **JSON Schema.** Enforces what SKOS cannot: the ID pattern with check symbol, provenance on every record, and `superseded` requiring `replacedBy`. This is the OpenLMP approach [E: IA-031].
- **SKOS-XL** is held in reserve [J].

**2.2 Crosswalk records: adopt SSSOM.**
- Each mapping records the relation, its justification (`semapv:` terms, including `LLMBasedMatching`), confidence, author and reviewer, versions of both sides, negation, and "no term found."
- Versions: v1.0.0 (Aug 2024); v1.1 pre-releases (May 2026) add `record_id`, `reviewer_agreement`, `review_date` and `derived_from` [E: IA-014]. Adopt the 1.0 slots and carry the 1.1 slots as declared extensions.
- HR users may find SSSOM unfamiliar [J], so the CSV bundle also gives plain mapping columns.

**2.3 Competency exchange: CTDL-ASN first; CASE and RSD as exports; IEEE as a reference to map to.**
- **CTDL-ASN:**
  - It links competencies to credentials, jobs, occupations, work roles and tasks.
  - Its steward recommends publishing in CTDL, not only CASE, when frameworks must link to credentials [E: IA-011].
  - It had a significant update in Jan 2025 (versioned frameworks, competency facets, cross-framework mappings) [E: IA-010], and its SHACL was edited Jul 2026 [E: IA-012].
  - The repository already shows the shapes EMST needs: `ceasn:Competency`, `ceterms:Task`, `ceterms:WorkRole`, and `ceterms:occupationType` alignment objects [E: IA-012].
  - **Adopt** as the primary public channel: the Credential Registry, with CTIDs.
- **CASE 1.1:**
  - Final; public 2025-04-02. It is a system-to-system exchange format for K-12 and higher education [E: IA-003, IA-004, IA-006].
  - 1.1 adds framework types, multilingual support, `isTranslationOf`, `targetType` on association endpoints, and extensions [E: IA-003].
  - Its association types are coarser than SKOS (no close/broad/narrow), so match precision is lost on export.
  - **Map.** The 1.1 information model itself was blocked. Example field names follow CASE 1.0 plus the 1.1 change list; validate against 1EdTech's schema before claiming conformance.
- **RSD:**
  - Open Skills Network says it is "not a Standards Development Organization" and offers "no conformance testing" [E: IA-008]. Credential Engine has stewarded RSD since Feb 2025 [E: IA-007].
  - It is a recipe over CTDL-ASN. **Map** as an export for OSMT users. Field names come from the OSMT API v2 fixture [E: IA-013].
- **IEEE 1484.20.3-2022:**
  - Active; published 2023-07-27. An amendment PAR (2025-06-19) would put it in IEEE SA Open and enable application profiles [E: IA-001, IA-002].
  - I found no evidence of HR or registry tooling built on it, and the text is paywalled.
  - **Map** in documentation; contribute an application profile once 20.3a lands. Do not make it the serialization [J].

**2.4 Credentials.**
- OB 3.0 `Alignment.targetType` lists `ceasn:Competency`, `CFItem` and CASE rubric types [E: IA-015]. Resolvable EMST IRIs are all issuers need [J].
- VC 2.0 is a W3C Recommendation (2025-05-15) [E: IA-016]. Credential Engine has CTDL-in-VC samples [E: IA-012].
- LER-RS and HR Open versions are unverified. **Watch.**

**2.5 HR and job data exchange.**
- **JDX** (the `jdx:` vocabulary) types job requirements as competencies, e.g. `jdx:ability` is a subproperty of `jdx:competency` [E: IA-012]. **Map:** use it as the role-profile export shape and as a structured-posting input.
- **HR Open and JEDx** are unverified. **Watch.**
- **schema.org JobPosting** markup should be read where job boards embed it [J].

**2.6 Occupational and skills frameworks (map, pinned to versions).**
- **O*NET:**
  - 31.0 (Aug 2026), quarterly updates, next one Nov 2026, CC BY 4.0 [E: IA-017, IA-018, IA-020].
  - O*NET-SOC 2019 has 1,016 titles, 923 of them data-level [E: IA-019]. Web Services 2.0 is current [E: IA-021].
  - 30.3 modernized the content model and shipped a migration crosswalk [E: CA-028].
  - This is EMST's main US anchor at task and role level.
- **ESCO:**
  - v1.2.1 (Dec 2025) [E: CA-030]; 27 languages [E: IA-028].
  - The official ESCO–O*NET occupation crosswalk (v1, Sep 2022) offers a ready bridge for chaining. Only 12% of its rows are exactMatch [E: IA-022].
- **SOC:** map to SOC 2018. SOC 2028 status is unverified; a revision would re-base all role crosswalks [J].
- **OPM:** map at role level. The Apr 2026 series consolidation (running to Sep 2027) [E: CA-044] should appear as dated mapping deprecations, not ID changes.
- **CIP:** map via learning resources (LC's lane).
- **NICE:** a design precedent, not a mapping target. It gives statement IDs Retained/New/Withdrawn status and separates its component catalog [E: CA-032, CA-033, IA-036].
- **Lightcast:** releases every 4 weeks with a 120-day support window [E: CA-041]; licence unverified. Use only as a mapping object for the L4 tools layer, never as EMST's spine.

**2.7 Enterprise platforms.**
- I could not read vendor docs [IA-051], so the design depends on no vendor feature.
- EMST ships what any platform can take in: (1) a CSV skills library with stable IDs, versions and status; (2) a release delta feed; (3) resolvable IRIs.
- In return, EMST asks vendors to export their inferred mappings to EMST IDs as SSSOM [J].
- USA Hire competencies run through FH (FH-026).

**2.8 Outdated or superseded:**
- Open Skills Network stewardship of RSD → now Credential Engine [IA-007].
- O*NET Web Services 1.9 → 2.0 [IA-021].
- The 2019 O*NET frameworks in CTDL-ASN predate the 30.3 content model [IA-054].
- skills-ml is unmaintained [IA-040].
- Nesta's skills-taxonomy-v2 cannot be rerun: its licensed data was withdrawn [IA-041].
- v1's Airtable→GitHub→GitBook plan is superseded by the lead's decision [IA-035].

## 3. The v2 data model in brief

See `data_model_v2.md`, `emst-v2.schema.json`, `emst.context.jsonld` and `examples/`.

- **Layers (CA's L0–L6):**
  - VocabularyTerm (L0);
  - Competency, with embedded ProficiencyAnchors and Indicators (L1);
  - Task and KnowledgeStatement (L2);
  - RoleProfile and ProfessionFamily (L3);
  - Tool (L4);
  - ChangeSignal, ExposureAssessment and DriverEvent (L5);
  - Mapping (L6, SSSOM);
  - plus Credential, LearningResource and Source.
- **Links are stored once, on the spine side.** Tasks hold `supports → competency`; roles hold their task bundle and competency targets. Inverse links, craft blends, exposure summaries and counts are computed at build time. The v1 Workforce Signals drift (a 59-flag discrepancy) shows why stored counts go wrong [E: IA-034].
- **IDs:** e.g. `emst:core/CMP-T6N5VE4` → `https://w3id.org/emst/core/CMP-T6N5VE4`.
  - Six Crockford base32 symbols plus a Luhn mod-32 check symbol. I replaced Crockford's mod-37 check, which emitted `$` and other characters that break IRIs.
  - Migration IDs are minted deterministically once, then frozen in a registry with collision checks.
  - CASE identifiers, CTIDs and RSD UUIDs are all UUIDv5 of the IRI.
- **Provenance:** OpenLMP's extraction block, generalized [E: IA-030, IA-031]. Fields: `method`, `agent`, `generatedAt`, `derivedFrom` (v1 key, sheet, row, workbook SHA-256, v1 provenance code), `sources`, `evidenceLabel`, `confidence`, `reviewStatus`, `reviewers`, `interRaterAgreement`, `toolVersion`, `promptVersion`.
- **Versioning:** SemVer for the release, each layer, each module, the schema and each concept. A change of meaning mints a new ID with `replacedBy`. Every release ships a delta file.
- **Modules:**
  - Module namespaces name who minted an ID.
  - Modules may reference core; core never depends on modules.
  - Promotion to core keeps the ID.
- **Labels:** every text field is a language map.
- **Exports:** each is shown for 2.1.1, with what it loses: native JSON-LD, CSV + Frictionless datapackage, SKOS Turtle, CASE 1.1, CTDL-ASN, RSD, OB 3.0 alignment.

## 4. Crosswalk method and what the first crosswalks show

**Method** (`crosswalk_method.md`):
- SSSOM rows using SKOS predicates, EMST relations for cross-type links, and `NoTermFound`.
- Calibrated `confidence` is kept separate from the raw `similarity_score`.
- Authors and reviewers are identified, whether person or software/model agent.
- One mapping set per upstream version.
- On each upstream release, a CI diff sorts every row into carry / needs-review / deprecated / new-candidate.
- Two human reviewers for any mapping used in selection.

**EMST v1 → ESCO v1.2.0** [E: IA-024, prototype]:
- 666 lexical candidates (top 3 for each of 222 competencies).
- 39 candidates reviewed across 13 competencies:
  - 23 accepted: 6 closeMatch, 6 narrowMatch, 2 broadMatch, 9 relatedMatch;
  - 16 rejected, kept with `Not`;
  - acceptance did not fall with rank (62% / 54% / 62%).
- 4 additions, including "manage forest fires". The lexical matcher missed it because "prescribed" pulled toward medical skills.
- The bundled ESCO skills contain no "tribal", "Indigenous", "wildfire" or "wildland fire". So 6.5.1 and 7.2.1 are recorded as `sssom:NoTermFound`.
- [J] ESCO bridges generic data-craft and management competencies. It cannot replace EMST for US statecraft, Tribal relations or wildland fire, and that is where EMST adds distinct value.
- These are AI-reviewed (`semapv:LLMBasedMatching`) and labelled as needing SME confirmation.

**v1 family → SOC** [E: IA-022, IA-019]:
- 29 rows, 8 flagged.
- F10 uses 19-1012, which is Food Scientists and Technologists. F12 uses 33-1021, which is First-Line Supervisors of Firefighting and Prevention Workers (inspectors are 33-2021 and 33-2022).
- For FH: F8 → Lawyers, F11 → Library Technicians, F13 → Health Information Technologists look misdirected. Verified alternatives exist: 13-1199.05, 19-2041.02, 19-2099.01.
- This backs CA's warning about v1's public "validated against O*NET" claim [E: IA-038].

## 5. Skills intelligence: state of the art, prototype, results

**5.1 State of the art, appraised** (see `pipeline_design.md` §3.1).
- **Span-first extraction:**
  - SkillSpan's guidelines are reusable [E: IA-027].
  - Accuracy is modest: Nesta's open NER reaches F1 0.59 [E: IA-029].
- **Embedding plus threshold:**
  - Nesta maps with MiniLM at a 0.7 threshold, falling back up the hierarchy.
  - Its documented failures (acronyms, metaphors, non-skills) are the ones I hit [E: IA-029].
- **Taxonomy-driven pretraining:**
  - ESCOXLM-R is state of the art on 6 of 9 tasks [E: IA-028].
  - A later option, once EMST has data to fine-tune on.
- **LLM-generated synthetic training data:**
  - Decorte et al. [E: IA-025].
  - Cheap for a taxonomy of about 10³ concepts [J].
- **Infer–Retrieve–Rank (IReRa):**
  - Works with about 50 labelled examples [E: IA-026].
  - **This is the LLM pattern I recommend** [J].
- **Benchmark layout:** MELO offers a reusable one [E: IA-023].
- **Thin evidence, stated plainly:**
  - no environmental-sector skills benchmark exists;
  - drift and emergence detection is mostly vendor practice [E: CA-041, IA-017];
  - there is no standard for calibrating confidence [J].

**5.2 Prototype** (`prototype/`, `python run.py`).
- **Data:** 300 OpenLMP components (monitoring, standard and guideline) across 8 states. A floor of 30 state-agency components is enforced, since state plans are about 5% of the corpus. All 222 v1 competencies come from DE's baseline. Inputs are pinned by SHA-256.
- **Index:** competency documents weight the title ×3, description ×2 and tasks ×2, plus proficiency statements and indicators. Rankers: TF-IDF (1–2-grams, crude stemming, plan and competency stop-lists), BM25, and WordLlama static embeddings (bundled weights; HuggingFace is unreachable). Scores are min-max normalized and fused 0.35/0.35/0.30.
- **Variants tested:** each ranker alone; title+description only; task-level index (666 tasks, max roll-up); RRF hybrid; query preprocessing.
- **Confidence:** (a) tercile bands fixed in advance from the unlabelled 300; (b) agreement among the base rankers, specified after (a) failed on dev, so it is validated only on held-out.
- **Gold set:** 60 dev + 30 held-out items, labelled blind before any ranking existed. Each item records status, primary code, acceptable set, and fit/gap theme. Five pooled additions on dev are kept separate. Annotator: a single AI, which is not SME evidence. Runtime is about 55 s.

**5.3 Results.** Strict scores use the blind labels; pooled dev scores in parentheses.

| System | Dev P@1 [95% CI] n=49 | Dev Hit@5 | Held-out P@1 [95% CI] n=23 | Held-out Hit@5 |
|---|---|---|---|---|
| **Fused full document** | **0.53 [0.39, 0.67]** (0.59) | **0.88** | **0.48 [0.26, 0.65]** | **0.78** |
| TF-IDF | 0.53 | 0.82 | 0.48 | 0.83 |
| BM25 | 0.41 | 0.78 | 0.39 | 0.74 |
| WordLlama | 0.39 | 0.63 | 0.43 | 0.74 |
| Title+description only | 0.45 | 0.80 | 0.43 | 0.65 |
| Task-level (v1 tasks) | 0.43 | 0.61 | 0.39 | 0.70 |
| Fused + glossary + masking | 0.47 | 0.84 | 0.39 | 0.78 |

- **Combined (n=72):** P@1 0.51 [0.40, 0.63]; Hit@5 0.85 [0.75, 0.91].
- **Most specific competency at rank 1:** dev 0.31, held-out 0.35.
- **Breakdowns:**
  - good-fit items 0.55 vs weak-fit items 0.36;
  - standards 0.58, guidelines 0.52, monitoring 0.40;
  - state plans 0.54 vs USFS 0.51.
- [J] What the numbers mean:
  - The top 5 contains an acceptable competency about 85% of the time, which is useful for review today.
  - Counts built from top-1 labels carry roughly ±0.1–0.15 precision uncertainty and must be corrected for error.
  - The richer v1 text earns its keep.
  - With n=23, held-out differences under about 0.15 cannot be told apart.
- **Confidence** (combined, non-noise items):
  - Tercile bands: high 0.71 (n=24), medium 0.45, low 0.37. Not monotonic on dev alone.
  - Ranker agreement: high 0.91 (n=11, Wilson 0.62–0.98), medium 0.53 (n=34), low 0.33 (n=27). Monotonic on both sets.
  - Use agreement for now. Only about 15% of items land in high.
- **Noise:**
  - 18 of 90 items (20%, Wilson 13–29%) were extraction artefacts, consistent with OpenLMP's rule-based component precision of 0.785 [E: IA-032].
  - Neither signal isolates them. A deontic-language rule flags 10 of 18 at about 10% false positives (exploratory).

**5.4 Failure modes:**
1. **Homonyms.** "ownership"/"rights" pulled toward 7.1.1 (S017, S227); "accurate…evidence" toward 7.2.1 (S107); "supply" toward 1.8.5 (S173).
2. **Proper names as false anchors.** "Game and *Fish* Department" (S273) and "Garden *Creek*" (S082) pulled toward fisheries. But masking names also removed real signal ("Idaho Fish and Game", "Federal Highway Administration").
3. **v1 near-duplicates.** 4.2.3/4.3.2 and 1.3.5/1.3.1 push the right answer to rank 2–3 (S130, S293, S141).
4. **Missing vocabulary.** "reclaim" (S214), "obliterate roads" (S197); forestry BMPs matched to stormwater (S241, S028).
5. **Abstract intent.** Compliance currency (S023); a training manual matched to facilities (S121). An LLM should help most here [J].
6. **True coverage gaps.** Scenery, range, roads, minerals, lands, wilderness, recreation.
7. **Confident noise.** 7 noise items landed in the high tercile band (e.g. S166).

**5.5 Negative result.**
- After studying dev errors I added an acronym glossary and name masking. On blind held-out data they cut P@1 from 0.48 to 0.39.
- [J] Hand rules fitted to a few dozen errors over-fit, and names carry signal as well as noise here.
- Improvements must come from methods that generalize and must be scored on held-out data.

**5.6 Tasks vs competencies.**
- v1's task layer (3 per competency, generic wording) underperforms as a target [E: IA-034].
- This does not refute a task spine. It says v1's tasks cannot be that spine for NLP yet.

**5.7 Change over time, gaps and the PD demo.**
- **Era drift:** USFS binding direction, 76 1982-rule plans vs 16 2012-rule plans, with a plan-level bootstrap.
  - Increases: trail construction +3.3 pts, fuels +2.7, restoration +1.9, invasive species +1.7, Tribal consultation +0.6.
  - Decreases: silviculture −1.6, NEPA −0.9.
  - 72 of 222 competencies have CIs excluding zero (no FDR correction applied).
  - "Urban habitat restoration" +1.5 is almost certainly a linker artefact.
  - [S] The direction is plausible, but plan format, extraction and linker error are all confounded with real change. Treat this as a demonstration of the record shape, not a demand finding (that is LM's lane).
- **Gap clusters:** NMF over 5,994 low-similarity components gave 12 clusters. These match the blind gold gap themes:

  | Cluster | Components |
  |---|---|
  | Range/livestock | 641 |
  | Motorized recreation/ROS | 533 |
  | Scenic/wild and scenic rivers | 482 |
  | Roads | 419 |
  | Minerals | 391 |
  | Oil and gas stipulations | 159 |

  Habitat (1,031), snag (722) and riparian (611) clusters are vocabulary gaps inside covered competencies. These feed `candidate_competencies.csv` (IA-CC-01…07), which I suggest go to a public-lands module rather than core [J].
- **PD demo** (v1 illustrative Forester PD):
  - Duties linked plausibly: 1.3.1, 1.3.2, 1.3.4, 1.3.5 + 3.1.4, 4.1.1.
  - A short GIS mention inside a KSA paragraph was missed, which argues for linking sentence by sentence.
  - Forestry is the easy case for a forestry-heavy v1.

## 6. Pipeline design in brief (`pipeline_design.md`)

- **Sources:**
  - USAJOBS;
  - state boards (through agreements);
  - NGO pilot boards;
  - licensed private data (keep only derived aggregates);
  - PDs (through FH/SL);
  - CTDL credentials and course catalogs;
  - OpenLMP;
  - O*NET Emerging Tasks.
- **Stages:**
  1. Ingest with a hash and licence record.
  2. Strip PII.
  3. Segment the text and classify what is a real requirement.
  4. Retrieve candidates with the hybrid baseline.
  5. Rerank with an LLM, IReRa-style.
  6. Calibrate confidence.
  7. Route to the review queue.
  8. Aggregate with correction for misclassification.
  9. Detect drift and emergence.
  10. Publish L5 ChangeSignals, each with `linkerQuality`.
- **LLM stage:**
  - 20 candidates with definitions, plus "none fits";
  - verbatim evidence spans, checked against the source text;
  - confidence from 5-sample self-consistency;
  - pinned model and prompt versions;
  - posting text treated as untrusted data.
- **Acceptance rule:** held-out P@1 improves by ≥0.10 with CIs that don't overlap, and abstention on noise reaches ≥0.7 recall.
- **Evaluation:** a 600-item gold set annotated twice, with IO; per-release SCORES.md.
- **Cost:** retrieval is negligible; LLM reranking is about 0.23–1.1 billion tokens a year for about 135k items; human review about 75 hours in year 1. Licensed private data is the dominant, uncertain cost [S].
- **Governance:** model cards; humans decide which signals count; TN protocol for Tribal data; an appeals route.

## 7. Answers to CA architecture questions

**IA-1. Standards per layer; ID scheme; modules (DP-9).**

| Layer | Canonical form | Exports and mappings |
|---|---|---|
| L0 | SKOS ConceptSchemes | CTDL concept schemes |
| L1 | JSON-LD Competency | CTDL-ASN `ceasn:Competency` (primary), CASE CFItem, RSD, OB3 target; IEEE 1484.20.3 alignment in docs |
| L2 | Task, KnowledgeStatement | `ceterms:Task`; SSSOM to O*NET tasks/DWAs |
| L3 | RoleProfile with sector-actor variants | `ceterms:WorkRole`/Occupation, JDX Job; SSSOM to O*NET-SOC, OPM series, state classes |
| L4 | Tool (vendor-neutral categories) | SSSOM to O*NET Technology Skills and Lightcast |
| L5 | ChangeSignal / ExposureAssessment / DriverEvent with PROV | none (no external standard fits) |
| L6 | SSSOM | SKOS/CTDL/CASE renderings |

- HR Open and JEDx are watched; EMST meets them through IRIs and the CSV library.
- **IDs:** as §3.
- **Modules:**
  - Each module has a namespace (minting authority), a steward and its own release line.
  - Module concepts may reference core, never the reverse.
  - Conformance means the same schema, provenance on every record, and SSSOM crosswalks.
  - Promotion to core keeps the ID. Forks mint in their own namespace, so they stay visible.

**IA-2. What to link text to; how confidence and drift are recorded in L5.**
- **Link to competencies now, using their full text,** and record the best task as `emst:evidencesTask` evidence.
- **Switch to tasks** when L2 has 15–30 statements per role crosswalked to O*NET, and task-level linking beats competency-level linking on held-out data.
- Evidence for waiting: with v1's tasks, P@1 is 0.43 vs 0.53 and Hit@5 0.61 vs 0.88 [E].
- On CA's "change my mind": the external task measures LM is assessing are anchored to O*NET tasks and DWAs [J; LM to confirm]. So L2 should be designed crosswalk-first to O*NET. That supports the task spine.
- **Each ChangeSignal records:**
  - `measure{value, ci95, n, denominator}`, corrected for linker error;
  - `linkerQuality{goldSet, precisionAt1, ci95}`;
  - `corpus{version, sha256, license}`;
  - `provenance{method, toolVersion, promptVersion, evidenceLabel S until reviewed, reviewStatus}`;
  - `caveats`.
- **Item-level links** are SSSOM rows, with calibrated confidence kept separate from raw similarity.
- **Drift:** signals compare `observedPeriod` with `comparisonPeriod`. **Emergence:** `emergence-candidate` signals.

**IA-3. Crosswalk artifacts.**
- SSSOM with SKOS predicates, `Not` and `NoTermFound`.
- Calibrated confidence plus raw similarity; `semapv` justifications; reviewer IDs and agreement.
- One mapping set per upstream version, with a CI diff on every O*NET quarterly and ESCO release.
- O*NET 30.3 migration applied as `MappingChaining`.
- OPM consolidation recorded as dated deprecations with successors.

## 8. Proposals

- **P-IA-01** Make the JSON-LD bundle canonical (SKOS + PROV; `emst.context.jsonld`), validated by `emst-v2.schema.json` in DE's CI. Generate CTDL-ASN, CASE, RSD, SKOS and CSV from it; never hand-edit them.
- **P-IA-02** Adopt the persistent ID scheme:
  - opaque `TYPE-code` with a check symbol;
  - namespace = minting authority;
  - w3id IRIs;
  - deterministic migration minting into `registry/ids.csv`;
  - UUIDv5 for CASE, CTDL and RSD;
  - never reuse an ID.

  Register `w3id.org/emst/` (AS to own the namespace).
- **P-IA-03** Make provenance mandatory on every record and every machine-derived value, including `evidenceLabel`, `interRaterAgreement` and full v1 lineage.
- **P-IA-04** Run crosswalks as a program of SSSOM sets: v1→v2 identity map; EMST↔ESCO; roles↔O*NET-SOC; roles↔OPM (FH) and state classes (SL); tasks↔O*NET tasks/DWAs. Publish coverage, predicate mix, κ and staleness for each.
- **P-IA-05** Fix F10 and F12 now. Have FH adjudicate F8, F11 and F13. Retire the family-level crosswalk as an anchor in favour of role-level crosswalks.
- **P-IA-06** Retire Airtable as editing master; editors submit pull requests. Pick one licence (CC BY 4.0 or CC0) with AS/CP.
- **P-IA-07** Adopt a vendor-neutral delivery contract and procurement clause:
  - CSV library, delta feed and IRIs;
  - vendors export their mappings to EMST as SSSOM;
  - no vendor IDs as keys.
- **P-IA-08** Link to competencies now and switch to tasks by the gold-set criterion; design L2 crosswalk-first to O*NET.
- **P-IA-09** Build a 600-item environmental gold set with IO: annotated twice, MELO layout, dev/held-out split, SCORES.md each release.
- **P-IA-10** Add an LLM rerank stage (IReRa-style) behind the acceptance rule.
- **P-IA-11** Never publish uncorrected top-1 counts. Every ChangeSignal carries `linkerQuality` and corrected CIs; offer the same to LM.
- **P-IA-12** Add a requirement/noise classifier upstream and propagate OpenLMP extraction confidence.
- **P-IA-13** Route the seven gap functions to DB/FC/SC as public-lands module candidates.
- **P-IA-14** Resolve v1 near-duplicates (prescribed fire, drones, green bonds, carbon, conservation finance, participatory research) before linking at scale.
- **P-IA-15** Publish the core framework in CTDL-ASN in the Credential Registry during the NGO pilot, so issuers can align to EMST from day one.

## 9. Disagreements and trade-offs

- **With v1:** Airtable as master; codes used as IDs; a family-level crosswalk; two licences asserted at once.
- **With CA's task spine:** I agree on the destination but not the timing for NLP. Linking to tasks gives exposure joins; linking to competencies is more accurate now.
- **CTDL-ASN vs CASE first:**
  - I pick CTDL-ASN for linked data [E: IA-011]; LC may prefer CASE for academic systems.
  - Both are generated exports, so the choice is where to publish first, not lock-in.
- **SSSOM vs a simple table:**
  - SSSOM is heavier and less familiar to HR users.
  - It is the only open format with per-row provenance, negation and "no term."
  - The flattened CSV offsets the usability cost.
- **Opaque vs sequential IDs:**
  - Opaque IDs are harder to remember.
  - Sequential IDs invite people to read meaning into them, which is how v1's codes became structural.
- **The LLM stage:**
  - Accuracy gains are expected but unproven here [S].
  - Costs: run cost, dependence on one provider, reproducibility.
  - For CP: agency PDs may require an approved environment.
- **With LM:** our work is complementary. I only ask that counts carry error bounds, and I offer the evaluated linker.
- **With PS and vendors:** I accept that vendors will map EMST into their own graphs, but require SSSOM exports so those mappings can be checked.

## 10. Issues outside my area

- **Tribal data (TN):** components tagged `tribal` and Tribal postings need TN's protocol (CARE principles). Hold aggregates until it exists.
- **Claims hygiene (CP/AS):** claim no O*NET, ESCO or OPM alignment until a reviewed SSSOM set exists.
- **Coverage skew (DB/LM):** the demand corpus is about 95% USFS in western states. Water, air, waste, energy and ESG need their own requirement sources.
- **Licences (CP/AS):** O*NET is CC BY 4.0, so crosswalk files need attribution. ESCO terms are unverified. The licence lineage of the WordLlama weights is unverified, which is why a lexical-only mode exists.
- **Stewardship (AS):** someone must own the w3id namespace, the Credential Registry account and the ID registry in year five. skills-ml and Nesta are lapse cases.
- **Validation (IO):** my gold set is single-annotator AI judgment, fit only for engineering.

## 11. Open questions for CA

1. Is the bundle canonical, and does the schema go into DE's CI?
2. Do IDs follow namespace = minting authority, or should only core mint?
3. Which licence: CC BY 4.0 or CC0?
4. What mapping acceptance thresholds apply for each use (selection, analytics, navigation), set with IO and FH?
5. Should the task-first switch criterion become a named decision point under DP-1?
6. Do the public-lands gap functions go into a module or into core?
7. Should the pilot publish CTDL-ASN first (my recommendation) or CASE?

## 12. Files written

All under `/home/claude/emst/docs/research/interop-skills-intelligence/` (report.md itself was refused by the harness; its text is above).

**Tables:**
- `sources.csv` (55)
- `standards_appraisal.csv` (34)
- `ecosystem.csv` (26)
- `v1_assessment.csv` (22)
- `candidate_competencies.csv` (7)

**Data model:**
- `data_model_v2.md`
- `emst-v2.schema.json`
- `emst.context.jsonld`
- `examples/`: bundle, csv_bundle, SKOS, CASE, CTDL-ASN, RSD, OB3

**Methods:**
- `crosswalk_method.md`
- `pipeline_design.md`

**Crosswalks** (`crosswalks/`):
- `emst_v1_to_esco_skill.candidates.sssom.tsv`
- `emst_v1_to_esco_skill.reviewed.sssom.tsv`
- `review_emst_esco*.csv`
- `emst_v1_family_to_soc2018.sssom.tsv`

**Prototype** (`prototype/`):
- `run.py`, `crosswalk_esco.py`, `crosswalk_family_soc.py`
- `emst_link/`
- `README.md`, `requirements.txt`
- `data/`, `gold/`, `outputs/`

**Scripts:**
- `scripts/build_examples.py`
- `scripts/validate_outputs.py`
