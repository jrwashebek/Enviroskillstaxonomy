# EMST crosswalk method (L6) — draft (IA)

**Purpose.** Connect EMST to the systems agencies, employers and educators already use (O*NET, ESCO, OPM series
and qualification standards, state class specs, CIP, credential registries, NICE-like frameworks, vendor skills
libraries). Every connection is recorded as a reviewable, versioned mapping record, never as a hard-coded field
on a concept.

Labels: [E] evidence (IDs in `sources.csv`), [J] judgment, [S] speculation.

## 1. Record format: SSSOM

All crosswalks are **SSSOM/TSV** files: a YAML header holding the curie map, mapping set id and version,
licence, both sources and their versions, tool and extension definitions, followed by one row per mapping
[E: IA-014]. SSSOM is chosen over CASE associations, CTDL alignments or ad-hoc CSV for four reasons:

- It records the relation **and** the justification (`semapv:` vocabulary). That vocabulary now includes
  `LLMBasedMatching`, `LexicalSimilarityThresholdMatching`, `ManualMappingCuration` and `MappingReview`
  [E: IA-014].
- It has author, reviewer, confidence and source versions per row.
- It has negation (`predicate_modifier: Not`) and an explicit "no equivalent" object (`sssom:NoTermFound`)
  [E: IA-014]. Recording *that a match was looked for and does not exist* is how EMST documents what other
  frameworks miss.
- It is a plain TSV that HR analysts can open, with tooling (sssom-py) that CI can run [J].

Exports derive from it: SKOS `*Match` triples, CTDL-ASN `*Alignment` properties, CASE associations (lossy),
RSD `alignments` and `occupations` (lossy).

### 1.1 Required and recommended slots (EMST profile of SSSOM)

| Slot | EMST rule |
|---|---|
| `record_id` | Required. Stable per row, e.g. `emst-v1-esco:2.1.1:1` (SSSOM 1.1 slot; used now as an extension) |
| `subject_id` / `object_id` | CURIEs from the header map; EMST side always a persistent EMST IRI (v1 aliases only in migration files) |
| `predicate_id` | One of `skos:exactMatch`, `skos:closeMatch`, `skos:broadMatch`, `skos:narrowMatch`, `skos:relatedMatch`; or an EMST relation for cross-type links (`emst:requiresCompetency` role→competency; `emst:evidencesTask` posting/plan text→task) |
| `predicate_modifier` | `Not` for reviewed rejections (kept to stop the same bad candidate resurfacing) |
| `mapping_justification` | `semapv:LexicalSimilarityThresholdMatching` / `EmbeddingBasedMatching` for machine candidates; `semapv:LLMBasedMatching` for LLM judgments (including in-session AI review); `semapv:ManualMappingCuration` only for human SMEs; `semapv:MappingReview` when a human confirms a machine row |
| `confidence` | Creator's probability that the row is correct (0–1). For machine rows: calibrated score from the gold set, never a raw cosine |
| `similarity_score` / `similarity_measure` | Raw machine score and how it was computed (kept separate from confidence) |
| `author_id` / `reviewer_id` | ORCID for people; `emstagent:<tool>-<version>` for software and models |
| `reviewer_agreement` | SSSOM 1.1 slot: reviewer confidence that the row is right (−1…1); κ across reviewers goes in the set header |
| `subject_source_version` / `object_source_version` | Required. EMST release; upstream release (e.g. `O*NET 31.0`, `ESCO v1.2.1`, `OPM series list 2026-04-24`) |
| `review_status` (EMST extension) | `candidate`, `accepted`, `rejected`, `needs-review`, `deprecated` |
| `mapping_date` / `review_date` | ISO dates |
| `comment` | Free-text rationale; LLM rows must say "requires human SME confirmation" until reviewed |

### 1.2 Choosing a predicate (decision rules)

| If… | Predicate |
|---|---|
| Interchangeable for hiring, training and analytics; same scope, same type of thing | `skos:exactMatch` (rare across frameworks) |
| Same capability, minor scope or wording difference; interchangeable for most uses | `skos:closeMatch` |
| The other concept is broader (EMST is a specialisation, e.g. NEPA implementation → ESCO "assess environmental impact") | `skos:broadMatch` |
| The other concept is narrower (EMST GIS operation → ESCO "create GIS reports") | `skos:narrowMatch` |
| Associated but different kind of thing (competency vs knowledge concept; task vs occupation) or partial overlap | `skos:relatedMatch` |
| Different types where the relation has a meaning (role requires competency; text evidences task) | EMST relation |
| Looked for; nothing fits | object `sssom:NoTermFound` |

SKOS direction: `A skos:broadMatch B` means B is broader [E: IA-052]. The official ESCO–O*NET occupation
crosswalk uses the same four predicates. Its distribution is broadMatch 2,053, closeMatch 1,432, exactMatch 498,
narrowMatch 227 (plus 43 ISCO-level fallbacks) [E: IA-022]. Exact matches are a minority even between two
occupational classifications. Expect fewer between EMST competencies and ESCO skills [J].

## 2. Target-by-target design

| Target | EMST side | Grain | Version tracking | Owner of review |
|---|---|---|---|---|
| **O*NET tasks** (task statements; DWAs) | L2 tasks | task ↔ task (closeMatch / narrowMatch); task ↔ DWA (broadMatch) | O*NET release (quarterly; 31.0 Aug 2026; next Nov 2026) [E: IA-017, IA-018, IA-020] | IA + LM (LM ingests AEI/exposure measures through these links) |
| **O*NET-SOC occupations** | L3 roles | role ↔ occupation (close/broad/narrow); `emst:requiresCompetency` occupation → competency (from O*NET importance data, optional) | O*NET-SOC 2019 now; re-base at SOC 2028 [E: IA-019] | FH, SL, PS |
| **ESCO skills / knowledge** | L1 competencies, L2 knowledge statements | competency ↔ skill (all predicates); knowledge statement ↔ ESCO knowledge (close) | ESCO version (v1.2.1 Dec 2025 per CA-030; prototype used v1.2.0) | IA + DB |
| **ESCO occupations** | L3 roles | via chaining: EMST role → O*NET-SOC → ESCO using the official crosswalk (`semapv:MappingChaining`, `derived_from` = both source rows) | crosswalk v1 (Sep 2022) [E: IA-022] | IA |
| **OPM series / qualification standards** | L3 role variants (federal) | role ↔ series (close/broad); role ↔ qualification standard (related) | Series list date. The April 2026 consolidation runs to Sep 2027 [E: CA-044]. A consolidated series makes old mapping rows `deprecated` with a successor row, not an ID change | FH |
| **State class specs** | L3 role variants (state/local) | role ↔ class (close/broad); per state file | Class plan revision date per state | SL |
| **CIP 2020** | learning resources/programs; L1 via programs | program ↔ CIP (exact/close); competency ↔ CIP (related, through program evidence) | CIP edition | LC |
| **NICE-like frameworks** (NICE, DCWF, SFIA where licensed) | L2/L3 | statement ↔ statement; work role ↔ role | Component version (NICE v2.2.0 per CA-032) | IA + DC |
| **Credentials** (CTDL, OB3) | L1 | credential `covers` competency: published *by issuers* as alignments; harvested into SSSOM rows with issuer as author | Registry snapshot date | LC |
| **Vendor libraries** (Lightcast, HCM skills clouds) | L4 tools; L1 | vendor skill ↔ EMST (related/close); vendor-supplied rows accepted only with author = vendor | Vendor release (Lightcast: 4-week releases, 120-day support window per CA-041) | PS, CP (licence) |

### 2.1 Version tracking against upstream releases

1. **Pin.** Every mapping set states `object_source_version`. There is one mapping set per upstream version
   (`emst-onet-task/31.0/…`).
2. **Diff on release.** When O*NET or ESCO publishes, a CI job loads the new release, diffs concept IDs and
   labels against the pinned one, and classifies each EMST mapping row:
   - (a) object unchanged → carry the row forward automatically, re-stamping `object_source_version` and noting
     "carried";
   - (b) object label or description changed → `needs-review`;
   - (c) object deprecated or replaced → `deprecated`, with the upstream successor proposed as a `candidate`;
   - (d) new upstream concepts near EMST concepts (by the linker) → new `candidate` rows.
3. **Release.** The new mapping set version is published with a change summary. Consumers can always fall back
   to the previous pinned set.

O*NET's 30.3 content-model modernization (Worker/Job/Market) shipped a migration crosswalk [E: CA-028 via
IA-038]. That is exactly the kind of upstream change this process absorbs: apply O*NET's own crosswalk as
`semapv:MappingChaining`. ESCO v1.2.1 "improved structure without adding or removing content" and shipped a
delta [E: CA-030 via IA-038]. That is case (a)/(b) only.

## 3. Workflow (who does what)

```
candidate generation (linker; lexical + embedding; later LLM rerank)  -> review_status=candidate, confidence=calibrated
   -> triage queue sorted by expected value (high-use EMST concepts first; low-confidence last)
   -> reviewer 1 (domain SME)  -> accept with predicate / reject (Not) / NoTermFound
   -> reviewer 2 on a 20% sample + all exactMatch rows -> reviewer_agreement; Cohen's kappa on predicate per set
   -> CA/steward sign-off for exactMatch and for any role↔OPM/state-class row used in hiring
   -> publish mapping set version
```

- A mapping used for **selection** (hiring) needs two human reviewers and IO's validity evidence. A mapping used
  for **analytics** or **navigation** needs one human reviewer plus the sampled second review [J; IO to set the
  thresholds].
- Machine and LLM rows **never** become `accepted` without a human reviewer, except in clearly labelled
  research files like the prototype's (justification `semapv:LLMBasedMatching`, reviewer
  `emstagent:claude-in-session-IA`).

## 4. What the prototype showed (EMST v1 → ESCO v1.2.0)

`prototype/crosswalk_esco.py` generated **666 candidates** (top 3 lexical matches for each of 222 competencies)
from 13,939 ESCO skill URIs [E: IA-024]. It then merged 39 reviewed rows plus 4 additions into
`crosswalks/emst_v1_to_esco_skill.reviewed.sssom.tsv`.

- **Accepted:** 23 of 39 reviewed candidates (59%). Of those, 6 closeMatch, 6 narrowMatch, 2 broadMatch and
  9 relatedMatch. **Rejected:** 16 (41%).
- Acceptance did not fall with rank (rank 1: 62%, rank 2: 54%, rank 3: 62%). The lexical score does not order
  good candidates well [E: prototype output].
- **Failure mode 1, homonyms:** "prescribed" (fire vs medication), "invasive" (species vs cardiovascular
  procedure), "inventory" (forest vs warehouse).
- **Failure mode 2, recall:** the lexical matcher missed ESCO "manage forest fires", which a targeted search
  found. It was added as a reviewed row.
- **Failure mode 3, true gaps:** the bundled ESCO v1.2.0 skills contain no "tribal" or "Indigenous" string, no
  "wildfire" or "wildland fire", and no concept for validating AI outputs. EMST 6.5.1 and 7.2.1 are therefore
  recorded as `sssom:NoTermFound` [E: string search of IA-024].

This finding matters for adoption. **ESCO cannot stand in for EMST on US statecraft or wildland fire**, and
EMST's value is partly in exactly those gaps [J].

Role-level verification of v1's family→SOC sheet, using O*NET-SOC 2019 descriptions carried in the official
crosswalk [E: IA-022]:

- Two code/title pairs are wrong: **19-1012** is Food Scientists and Technologists, not farm and home management
  educators; **33-1021** is First-Line Supervisors of Firefighting and Prevention Workers, not fire inspectors.
- Three targets look wrong for their families: F8 → Lawyers, F11 → Library Technicians, F13 → Health
  Information Technologists.

All are flagged in `crosswalks/emst_v1_family_to_soc2018.sssom.tsv` for FH to adjudicate.

## 5. Quality metrics per mapping set (published in the header comment and release notes)

- Coverage: share of EMST concepts with ≥1 accepted non-negated mapping; share with `NoTermFound`.
- Predicate distribution (compare with the ESCO–O*NET reference distribution).
- Reviewer agreement: κ on predicate over the double-reviewed sample; % of machine candidates accepted.
- Staleness: share of rows whose `object_source_version` is not the current upstream release.

## 6. Limits

- The ESCO version of the bundle is inferred, not stated. Its 3,658 occupations equal ESCO v1.2.0 in the MELO
  standardized files [E: IA-023, IA-024]. Re-run against the official ESCO download when the portal is reachable.
- Preferred labels for some ESCO skills could not be split from alt labels (5% "(label not derived)").
  Cosmetic only; URIs are exact.
- No O*NET task-level mapping was produced: the task file was not obtainable offline. Methods are specified
  above. The v1 task layer (3 tasks per competency) is too thin for a meaningful task↔task crosswalk anyway (see
  report §5).
