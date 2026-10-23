# EMST skills-intelligence pipeline — design (IA)

**Goal.** Keep EMST current by continuously mapping job postings, position descriptions (PDs), curricula and
plan requirements onto EMST tasks, competencies and roles. Publish change-over-time indicators (L5
ChangeSignals) that carry their own uncertainty.

**Non-goal.** The pipeline does not edit the taxonomy. It proposes candidates (new tasks, wording shifts,
coverage gaps) to a human review process.

Labels: [E] evidence (IDs in `sources.csv`), [J] judgment, [S] speculation.

---

## 1. Sources

| Source | What it tells us | Access (status this session) | Cadence | Main risks |
|---|---|---|---|---|
| **USAJOBS** (Search API + Historic JOA) | Federal demand by series, grade, agency and location; duties and qualifications text | Public API with key [IA-046, not verified this session] | Daily pull, quarterly indicators | Announcements reuse boilerplate; one JOA can cover many hires; grade inflation of text |
| **State job boards** (state portals; NEOGOV/governmentjobs-type platforms) | State and local demand; class titles | Terms vary by state; prefer data-sharing agreements over scraping [J] | Weekly | 50 formats; class specs drive text (SL to map) |
| **NGO and professional-society boards** (conservation, wildlife, water associations) | NGO pilot cohort's labour market | Partnership or permission (pilot members) [J] | Weekly | Small n; duplicates across boards |
| **Private postings via licensed data** (aggregators) | Private-sector demand at scale | Commercial licence; redistribution usually barred [S] | Monthly | Licence can be withdrawn. Nesta's skills-taxonomy-v2 can no longer be rerun because its licensed TextKernel data was withdrawn [E: IA-041]. Store only derived aggregates and EMST IDs |
| **Position descriptions** (agency PD libraries; classification files) | What jobs officially are; PD rewrites signal transformation | Through FH/SL agreements; may contain incumbent names [J] | On change | PII; PDs lag practice (v1 forester page argues this) [E: IA-037] |
| **Curricula / course catalogs; credentials** | Supply-side coverage of competencies | CTDL Credential Registry (open linked data) [E: IA-012]; college catalogs | Term / annual | Marketing language; course titles ≠ outcomes |
| **Land management plan requirements** (OpenLMP) | What binding plan direction demands of the workforce | Local, open, provenance on every record [E: IA-030, IA-033] | As plans are revised | 95% USFS, western states; extraction noise (rule-based precision 0.785 [E: IA-032]) |
| **O*NET Emerging Tasks; O*NET releases** | Externally curated new or revised task statements | CC BY 4.0 downloads [E: IA-017] | Quarterly | US-generic, not environment-specific |

## 2. Stages

```
 ingest ──► normalize & segment ──► (extract) ──► link ──► score & calibrate ──► review queue ──► aggregate ──► detect drift/emergence ──► publish L5
   │              │                     │            │              │                  │               │                 │                       │
 raw snapshot   sections:            requirement   candidates   confidence band;    human accept /  indicators with   change, novelty,       ChangeSignal records
 + SHA-256      duties/quals/        sentences;    top-k EMST   abstain;            reject; gold    CIs + linker      gap clusters           + linkerQuality
 + licence      specialized exp.;    skill spans   tasks/comps  upstream conf.      growth          error correction
```

1. **Ingest.** Fetch, snapshot the raw document, store SHA-256, URL, retrieval time and licence. This is the
   OpenLMP `source.json` pattern [E: IA-030]. Strip PII at ingest (§8). Deduplicate near-identical postings
   with MinHash on normalized text, and keep a duplicate count so aggregates can be weighted by announcement or
   by opening [J].
2. **Normalize and segment.** Split into sections (USAJOBS: duties, qualifications, specialized experience,
   education; plans: already segmented by OpenLMP). Classify each segment as *requirement* or *non-requirement*.
   In the IA gold set, 18 of 90 plan components (20%, Wilson 13–29%) were extraction noise. Neither confidence
   signal flagged them reliably. A cheap deontic-language rule caught 10 of 18 at a 10% false-positive rate
   (exploratory) [E: prototype]. A small classifier trained on that label is the first upgrade [J].
3. **Extract (optional).** For long texts, extract requirement sentences or skill spans before linking (the
   SkillSpan / Nesta NER pattern). Nesta's open NER reaches F1 0.59 on UK adverts [E: IA-029], so span
   extraction adds error. Use it only where whole-sentence linking fails [J].
4. **Link.** Generate candidates over EMST concepts with hybrid retrieval: TF-IDF + BM25 + embedding, fused
   (prototype). Then **rerank with an LLM** (§3). The target is the task layer wherever L2 is rich, with roll-up
   to competencies; until then, competencies (§3.3).
5. **Score and calibrate** (§4).
6. **Review queue.** Route every item below "high" confidence, plus a random 5% of "high", to reviewers in
   priority order: frequency × uncertainty × policy salience [J]. Reviewer decisions feed the gold set
   (with dates), and the gold set gates every model change.
7. **Aggregate.** Compute indicators (§6) per period × competency/task/role × sector actor × jurisdiction ×
   subsector. Report misclassification-corrected estimates with intervals (§4.3).
8. **Detect drift and emergence** (§5).
9. **Publish** L5 `ChangeSignal` records (schema in `emst-v2.schema.json`). Each one carries `linkerQuality`
   (gold-set precision and its CI), corpus version and hash, caveats, and evidence label (usually S until a
   human reviews the signal).

## 3. State of the art and the LLM stage

### 3.1 What the literature and open tools show (2022–2026)

| Method | What it is | Evidence | Appraisal for EMST |
|---|---|---|---|
| Span extraction (SkillSpan; Nesta NER) | Tag skill spans, then link | SkillSpan: 14.5K sentences, 12.5K spans, domain-adapted models best [E: IA-027]. Nesta NER F1 0.59 on 500 labelled UK ads [E: IA-029] | Annotation guidelines are reusable. Accuracy is mediocre and the extra step compounds error. Low priority [J] |
| Embedding similarity with thresholds and hierarchical fallback (Nesta mapper) | Cosine to taxonomy concepts (MiniLM); 0.7 threshold; fall back to higher levels | Model card lists failure modes: metaphors, acronyms, non-skills [E: IA-029] | The same failure classes appeared in the IA prototype (acronyms, non-requirements) [E: prototype]. Thresholds need per-taxonomy tuning [E: IA-029] |
| Taxonomy-driven pretraining (ESCOXLM-R) | XLM-R-large further pretrained on ESCO relations; 27 languages | State of the art on 6 of 9 job-market benchmarks; better on short spans [E: IA-028] | Strong once a fine-tuning set exists. Weights on HuggingFace were not reachable here. A later-stage option [J] |
| LLM synthetic training data for extreme multi-label linking (Decorte et al. 2023) | LLM generates sentences per ESCO skill to train a bi-encoder | Benchmarks TECH/HOUSE/TECHWOLF released [E: IA-025] | Attractive for EMST: about 1,000 concepts × synthetic sentences is cheap. Must be validated on real text [J] |
| Infer–Retrieve–Rank (IReRa, 2024) | LLM proposes labels → retriever maps to taxonomy → LLM reranks; optimized with ~50 labelled examples | Released program and prompts for ESCO [E: IA-026] (paper body not read; arXiv blocked) | **Best fit for the EMST LLM stage**: small gold set, large label space, modular, auditable prompts [J] |
| Zero-shot LLM matching and LLM extraction (Clavié & Soulié 2023; Nguyen et al. 2024; Senger et al. 2024 survey) | Prompted LLMs as matchers or extractors | Not read this session [IA-042–IA-044, unverified] | Background only. Do not cite numbers until verified |
| Entity-linking benchmarks (MELO 2024) | Standardized query/corpus/annotation layout; lexical and encoder baselines | 48 datasets, 21 languages [E: IA-023] | Copy its layout for EMST gold sets so results are comparable and reusable [J] |
| Official human crosswalk (ESCO–O*NET 2022) | Expert SKOS-typed mapping | 4,269 rows; exactMatch only 12% [E: IA-022] | Reference distribution for what "good" crosswalks look like [J] |

**Thin evidence, stated plainly:** I found no published benchmark of skill extraction or linking on
*environmental* job text. Every number above comes from tech, hospitality or generic UK adverts. The EMST gold
set would be the first environmental one [J]. Drift and emergence detection is mostly vendor practice: Lightcast
releases its taxonomy every 4 weeks with a 120-day support window [E: CA-041]; O*NET publishes Emerging Tasks
[E: IA-017]. Peer-reviewed evaluation of emergence detectors is scarce [J].

### 3.2 LLM stage design

1. **Retrieve** the top 20 EMST candidates with the hybrid baseline. In the prototype, Hit@10 for the fused
   baseline was 0.90 on dev and 0.83 on held-out [E: eval_report.json]. Retrieving 20 rather than 10 is meant to
   push recall higher still, so the reranker is rarely missing the right answer [J].
2. **Prompt:** the requirement text (as untrusted data inside delimiters); 20 candidates, each with ID, label,
   statement, 2 tasks and 1 indicator; and an explicit **"none of these fits"** option. Ask for strict JSON:
   up to 3 IDs, relation (`evidencesTask` / `requiresCompetency`), the **verbatim evidence span**, and a
   one-sentence rationale.
3. **Self-consistency:** sample 5 times at moderate temperature. Confidence is the share of samples agreeing on
   each ID. Abstain when no ID reaches 3/5.
4. **Guardrails:**
   - reject outputs whose evidence span is not a substring of the input;
   - treat any instruction inside the posting text as content, never as an instruction;
   - pin the model version and prompt version (both recorded in `provenance.toolVersion` / `promptVersion`).
5. **Optimize, IReRa-style:** tune few-shot demonstrations on the dev gold only; never on held-out [E: IA-026
   design; J].

### 3.3 Mapping target: tasks or competencies?

Tasks, eventually; competencies now.

- Task statements are the unit that external exposure measures attach to. CA's lean makes them the spine
  [E: IA-038].
- But linking plan text to v1's 3-task-per-competency inventory did worse than linking to whole competency
  documents: dev P@1 0.43 vs 0.53, held-out 0.39 vs 0.48; Hit@5 0.61 vs 0.88 dev [E: prototype].
- v1 tasks are too few and too generic to be retrieval targets. The pipeline should therefore link to
  competencies (using all their text), record the best-matching task as secondary evidence, and switch to
  task-first linking once L2 has O*NET-style coverage (15–30 tasks per role) [J].
- Re-test the switch on the gold set before making it [J].

### 3.4 Evaluating the LLM stage

- **Gold:** 600 items stratified by source (postings, PDs, plans, curricula) × sector actor × subsector, double
  annotated by two human SMEs blind to system output. Measure Cohen's κ on the primary code and Jaccard on
  acceptable sets. Adjudicate disagreements. Split into dev (200) and held-out (400). This follows the OpenLMP
  pattern of independent annotators, IAA and published SCORES [E: IA-032].
- **Metrics:**
  - P@1, Hit@5, MRR;
  - abstention precision/recall (does it abstain on noise and on true gaps?);
  - expected calibration error of the confidence;
  - per-subsector and per-sector-actor breakdowns, with CIs.
- **Acceptance rule:** the LLM stage replaces the baseline only if held-out P@1 improves by at least 0.10 with
  non-overlapping 95% CIs, and abstention on noise reaches ≥0.7 recall [J; thresholds for CA/IO].
- **Regression:** re-run the full gold set on every model, prompt or taxonomy release, and publish SCORES.md
  [E: IA-032 pattern].

## 4. Confidence

### 4.1 Signals
- Retrieval margin and score.
- Base-ranker agreement.
- LLM self-consistency.
- Upstream extraction confidence (OpenLMP `confidence`, `method`, `enriched_by`).
- Source quality (structured vs scraped).

### 4.2 Calibration
- Fit isotonic regression from signals to P(correct) on the dev gold. Report reliability diagrams on held-out.
- Bands are defined on calibrated probability (high ≥ 0.8, medium 0.5–0.8, low < 0.5) [J].
- **Prototype evidence:** a priori tercile bands were not monotonic on dev (high 0.69, medium 0.43, low 0.50).
  Ranker-agreement bands were monotonic on both sets. Combined n = 72: high 0.91 (n = 11, Wilson 0.62–0.98),
  medium 0.53 (n = 34), low 0.33 (n = 27) [E: prototype]. The high band is small, so most items will need
  review until the LLM stage exists.

### 4.3 Propagating into aggregates
A share computed from top-1 labels is biased when precision is about 0.5. Correct prevalence with the gold-set
confusion matrix (misclassification-corrected estimation) and bootstrap over both plans/postings and gold items,
so intervals include linker uncertainty [J; standard measurement-error practice]. Never publish a demand count
without `linkerQuality` attached.

## 5. Drift and emergence

| Signal | Method | Prototype demonstration |
|---|---|---|
| **Demand drift** (share of requirements linked to a competency) | Period-over-period difference in corrected shares. Cluster bootstrap by employer/plan. Benjamini–Hochberg FDR across ~1,000 concepts | 1982-rule (76 plans) vs 2012-rule (16 plans) USFS binding direction: 72 of 222 competencies had CIs excluding zero (no FDR applied). Largest increases: fuels management +2.7 pts, trail construction +3.3, restoration +1.9, invasive species +1.7, Tribal consultation +0.6. Decreases: silviculture −1.6, NEPA implementation −0.9. Also "urban habitat restoration" +1.5, almost certainly a linker artefact (restoration language in 2012 plans pulled toward an urban competency): exactly why `linkerQuality` must travel with signals [E: prototype; interpretation J] |
| **Content drift** (same competency, different language) | Track the centroid of evidence spans linked to each concept per period; flag cosine shifts beyond the bootstrap null | Not run (needs dated postings) |
| **Emergence** (requirements the taxonomy does not cover) | Cluster low-similarity or abstained items (NMF/HDBSCAN). Promote a cluster to a candidate when it persists across ≥2 periods and ≥5 employers/plans. Corroborate with O*NET Emerging Tasks and vendor new-skill releases | 5,994 bottom-tercile USFS components gave 12 clusters. Range/livestock (641), motorized recreation/ROS (533), scenic/wild & scenic rivers (482), roads (419), minerals (391) and oil & gas stipulations (159) match the blind gold set's weak-fit themes exactly. Habitat-specific (1,031), snag (722) and riparian (611) clusters are vocabulary gaps inside covered competencies, not missing competencies [E: prototype] |
| **Model drift** | Monitor score distributions, abstention rate and review-overturn rate per source and month | — |

## 6. Output indicators (L5)

Each indicator is computed per period × concept (task / competency / role) × sector actor × jurisdiction ×
subsector, with CI and linker quality:

- **Demand share:** share of postings or requirements evidencing the concept.
- **Growth:** change in demand share between periods.
- **Entry-level exposure:** share of entry-grade postings (e.g. GS-5/7, or state equivalents via SL) requiring
  the concept. This is the observable counterpart of v1's career-ladder concerns, which LM can test.
- **AI-tool co-mention rate:** postings that mention AI or automation tools alongside the concept (L4 linkage).
- **Coverage gap index:** share of requirements in a subsector with no adequate EMST concept.
- **Supply–demand gap:** demand share vs share of credentials and courses covering the concept (CTDL harvest).
- **Novelty rate:** emerging-cluster volume per subsector.

## 7. Governance

- **Linker releases** carry a model card (Nesta's model card is a good template [E: IA-029]) and a SCORES.md.
  A linker or prompt change is a release with a version number.
- **Human authority:** only reviewed signals move a role's change indicator. Unreviewed signals are visible as
  "provisional" (S). LM sets the evidence threshold for a signal to count (CA question LM-3).
- **Tribal programs:**
  - postings by Tribal governments and plan components tagged `tribal` are processed only under TN's protocol
    (CARE principles);
  - aggregate indicators for Tribal employers are not published without that protocol;
  - Indigenous knowledge is never extracted into EMST content from public text [J; hard rule in TEAM_BRIEF].
- **Appeals:** any agency, employer or steward can contest a published signal through the repo issue process.
  The signal record links to its inputs.

## 8. Privacy and security (with CP)

- Postings and PDs can contain names, emails, phone numbers and incumbent names. Strip them with regex plus NER
  at ingest. Store only redacted text and hashes. Never ingest resumes, applications or person-level HR data in
  this pipeline (that would be a separate, CP-governed system).
- Licensed private data stays in its licence boundary. Publish only aggregates and EMST IDs.
- LLM calls on agency-provided PDs require an approved processing environment (FedRAMP or state equivalent;
  CP lane). Public postings and plans can run on any provider.
- Treat all ingested text as untrusted input to LLMs (prompt-injection guard in §3.2).

## 9. Cost (order of magnitude; to be priced by AS/CP)

Assumed annual volume [S]: 50,000 public-sector and NGO postings, 60,000 plan components (full OpenLMP plus
growth), 5,000 PDs and 20,000 course or credential descriptions, about 135,000 items in all.

| Item | Estimate | Basis |
|---|---|---|
| Hybrid retrieval (baseline) | Negligible: the prototype links 17,982 components to 222 competencies in under a minute on one CPU | [E: prototype runtime] |
| LLM rerank | ≈1.7k tokens per item × 5 samples ≈ 1.1 B tokens per year at full self-consistency, or ≈ 0.23 B with 1 sample plus 5 samples only on uncertain items | Item text ~300 tokens + 20 candidates × ~50 tokens + output [S]. Multiply by the current per-token price of the chosen model |
| Human review | ~2,000 queue items per year at ~1 min ≈ 35 h; gold set 600 items × 2 SMEs × ~2 min ≈ 40 h, then ~10 h per quarter to refresh | [J] |
| Infrastructure | GitHub Actions + object storage for snapshots (tens of GB per year) | [J] |
| Licensed private postings | The dominant and most uncertain cost; often tens of thousands of dollars per year with redistribution limits | [S]: price with vendors; prefer partnerships (NLx-type public exchanges) where available |

## 10. Phasing

1. **Now:**
   - lexical/hybrid baseline (prototype) on OpenLMP and USAJOBS;
   - double-annotated 600-item gold set with IO;
   - requirement/noise classifier;
   - replace LM's hand-written keyword → competency map in `lmp_demand_signals.py` with the evaluated linker,
     or at least attach its error bounds to LM's counts.
2. **Next:**
   - LLM rerank (IReRa-style) behind the acceptance rule;
   - state boards for 3–5 pilot states (SL);
   - NGO pilot boards;
   - agency PD library through FH.
3. **Later:**
   - task-first linking once L2 is rich;
   - licensed private data;
   - fine-tuned encoder (ESCOXLM-R-type) trained on accumulated reviews;
   - multilingual labels.
