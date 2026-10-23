# GS-LINK — gold-set design for the EMST competency linker (DP-18; ADR-0019 §6)

**Owner:** IA (tooling) with IO (labelling rules, `validation/spec_gold_sets.md` §6) and DE (storage, splits,
SCORES.md) · **Status:** design, Phase 4 (run with people in Stage 1) · **Licence:** CC0-1.0 (this document)
**Labels:** [E] evidence, [J] judgment, [S] speculation.

This document specifies GS-LINK, the 600-item gold set that gates every linker method change (ADR-0019 §4) and
supplies the `linkerQuality` attached to every ChangeSignal derived from linking (ADR-0019 §5). It follows IO's
gold-set specification and does not restate its general rules (coders, adjudication, splits, contamination,
rotation, CI enforcement); where this document and IO's specification differ, IO's governs.

## 1. What is labelled

A **unit** is one text segment that may express a work demand: a plan component (OpenLMP), a job-posting duties
or qualifications sentence group, a position-description major duty, or a curriculum learning outcome. Each unit
is labelled, independently and blind to system output, with:

| Field | Values | Notes |
|---|---|---|
| `item_status` | `requirement` · `generic` · `noise` | `noise` = extraction residue or non-demand text (headers, legal boilerplate, benefits). The Phase 2 set found 20% noise (Wilson 13–29%) [E: IA §5] |
| `acceptable` | set of EMST v2 competency IDs | every competency a qualified reviewer would accept as a correct link (the "acceptable set"); may be empty when `fit = none` |
| `primary` | one competency ID or empty | the single best link |
| `fit` | `good` · `partial` · `none` | `none` marks a coverage gap (no adequate EMST competency) — these feed emergence detection and abstention metrics |
| `evidencesTask` | task ID or empty | best-supported task of the primary competency (secondary label; enables the DP-18a comparison) |
| `subsector`, `sectorActor`, `sourceType` | codes from `vocab/` | stratification and per-stratum reporting |

Competency IDs are pinned to an EMST release; when a labelled competency is superseded, the unit is re-labelled by
the change record's successor map, or retired if the split is ambiguous (IO §3 "a unit whose text later changes
is retired").

## 2. Size and strata (600 units)

| Stratum | Target units | Rationale |
|---|---|---|
| Public lands plan components (OpenLMP; USFS, BLM) | 160 | Largest open corpus; Phase 2 baseline lives here |
| Federal postings and PDs (USAJOBS public text; agency PD libraries via FH agreements) | 120 | Federal design partners |
| State and local postings and class specs (pilot states PA, TX, WA first; SL) | 140 | State design partners; X5 overlap |
| Private postings (permitted public postings only; no licensed text) and consulting job architecture text | 80 | Private variants (X8) |
| Curricula and credential outcomes (CTDL harvest; LC) | 60 | Supply-side coverage |
| Deliberately sampled `noise` and `none` items | 40 | So abstention recall can be estimated (≥ 0.7 target) |

- **≥ 40% outside public lands and forestry** (ADR-0019 §6; P-DB-17): water, air, waste, environmental health,
  hazards, energy and ESG corpora. The allocation above gives 62% outside public-lands plan text [J].
- Within each stratum, sample proportionally to module (core + nine wave-1 modules), with ≥ 15 units per wave-1
  module across the whole set.
- **Exclusions (hard):** Tribal employers' documents, Tribal-flagged plan components, and any text whose subject is
  government-to-government consultation or Indigenous knowledge are never sampled (ADR-0007 §D; IO §3.7). The
  linker's quarantine stage (`emst_linker/safety.py`) is applied to the frame before sampling, and the quarantine
  count is reported.
- **PII:** all units pass `safety.strip_pii` before coders see them; residual names found by coders are redacted
  and the unit kept.

## 3. Layout (MELO-compatible)

Files follow the MELO layout so results are comparable with published entity-linking benchmarks [E: IA-023]:

```
validation/gold/gs-link/<release>/
  corpus_elements.tsv      # EMST competency IDs + document text (EMST text only; CC0)
  queries_dev.tsv          # unit_id, text (development split, 25%)
  queries_heldout.tsv      # held-out split (75%) — stored outside the public repo until each evaluation has run
  annotations_dev.tsv      # unit_id, acceptable IDs, primary, fit, item_status, evidencesTask, coder IDs (pseudonymous)
  annotations_heldout.tsv
  manifest.yaml            # frame snapshot hash, sampling seed, strata, coder pool, codebook version, canaries
  SCORES.md                # generated per release (IO §7): P@1, Hit@5, MRR, abstention recall, calibration, per stratum
```

Held-out files carry canary strings and a contamination probe runs before any LLM-stage evaluation
(IO §5; `validation/protocol_llm_coder_gate.md` §6.3). Third-party text in units (postings, PDs) keeps its source
licence; units from sources whose terms forbid redistribution are stored as hash + URL with text held privately
(the hash-and-URL rule used for X5).

## 4. Labelling

- Two qualified human SME coders per unit, blind and independent; a third senior SME adjudicates disagreements on
  `primary` and `fit` (IO §4). Coders see the competency documents (`emst_linker.corpus`) and a keyword search over
  them, never the linker's ranking.
- Agreement reported: Cohen's κ on `primary` (with "none" as a category), Krippendorff's α on `fit`, Jaccard on
  `acceptable` sets; bootstrap CIs.
- The Phase 2 72-item single-annotator AI set is **engineering data only** (ADR-0019 Context; IO §6): it may seed
  development examples and coder training, never evaluation.

## 5. Metrics and gates computed from GS-LINK

| Use | Metric | Gate |
|---|---|---|
| Method change (e.g. LLM rerank, P-IA-10) | held-out P@1 and its 95% CI | improvement ≥ 0.10 with non-overlapping CIs and noise-abstention recall ≥ 0.7 (ADR-0019 §4) |
| DP-18a task switch for a family | task-level vs competency-level P@1 on ≥ 100 held-out items of that family | ≥ 0.10 better, non-overlapping CIs, abstention ≥ 0.7, plus the X2 condition (ADR-0019 §2) |
| Published aggregates | confusion matrix (predicted top-1 × gold primary, incl. `none`) on held-out items | `quality.aggregate` refuses to run without it; corrected shares with bootstrap intervals only (ADR-0019 §5) |
| Confidence bands | calibration (reliability diagram; ECE) of the band | bands are relabelled from held-out calibration, never from dev |

`emst_linker.quality.evaluate` implements P@1, Hit@5, MRR and abstention recall with bootstrap CIs;
`quality.linker_quality` produces the `linkerQuality{goldSet, precisionAt1, ci95}` object.

## 6. Pre-registration fields

All `validation/preregistration_core.yaml#core_required` fields, plus IO §9 fields, plus: corpus frame snapshot
hashes per source; the linker version and index hash under evaluation (`python -m emst_linker info`); the
competency release; the list of quarantined frame items (count only).

## 7. Cost and schedule (order of magnitude) [J]

600 units × 2 coders × ~2 min ≈ 40 coder-hours, adjudication ~8 h, set-up ~16 h (IA pipeline_design §9). Stage 1,
after the CA approves the codebook and the coder pool is funded. Refresh ≥ 20% of held-out units per MINOR release
(IO §5).
