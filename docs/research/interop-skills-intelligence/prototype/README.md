# EMST linking prototype (IA role, Phase 2)

A transparent baseline that maps text describing work demands (here: land management plan components from
OpenLMP, plus one illustrative position description) onto the 222 EMST v1 competencies, reports top-k candidates
with a confidence band, measures itself against a hand-labelled gold set, and demonstrates the two outputs the
v2 change-signal layer needs: change over time and candidate coverage gaps.

## Run

```bash
pip install -r requirements.txt
python run.py                 # ~1 minute: sample, link, evaluate, bands, era drift, gap clusters, postings
python run.py --skip-drift    # ~10 s
python run.py --no-semantic   # lexical only (no wordllama)
python crosswalk_esco.py      # EMST -> ESCO v1.2.0 SSSOM candidates + reviewed file (downloads a pinned PyPI wheel once)
python crosswalk_family_soc.py  # v1 family -> SOC 2018 crosswalk as SSSOM with verification flags
```

Inputs are read-only: `EMST_ROOT/data/v1_baseline/` (DE's normalized v1 extract) and `LMPS_ROOT/plans/*/*/*/components.csv`
(override with env vars `EMST_ROOT`, `LMPS_ROOT`). SHA-256 of every input file is written to
`data/sample_manifest.json` and `outputs/eval_report.json`. No network is used except by `crosswalk_esco.py`
(PyPI + GitHub raw, both hash-checked).

## What it does

| Step | Module | Output |
|---|---|---|
| Sample 300 components (monitoring/standard/guideline; MT ID CA WA OR CO UT WY; floor of 30 state-agency components) and a blind 60-item dev + 30-item held-out gold subset | `emst_link/sample.py` | `data/sample_components.csv`, `gold/gold_items_*_blind.csv` |
| Build competency documents (title ×3, description ×2, tasks ×2, proficiency, indicators) and index with TF-IDF (1–2-grams, crude stemming, plan and competency stop-lists), BM25 and WordLlama static embeddings; fuse min-max-normalised scores 0.35/0.35/0.30 | `emst_link/index.py`, `link.py` | `outputs/candidates_sample300.csv` (top-10 per component) |
| Confidence: (a) tercile bands fixed from the unlabelled 300 (raw TF-IDF top-1 + margin); (b) agreement of base rankers with the fused top-1 | `link.py`, `run.py` | `confidence_band` column; `bands` in `eval_report.json` |
| Evaluate variants (lexical/semantic/fused; title+description only; task-level index rolled up by max; RRF hybrid; query preprocessing) — P@1, P@3, Hit@k, MRR, Recall@5 with bootstrap CIs | `evaluate.py` | `outputs/eval_report.json`, `outputs/gold_eval_detail_{dev,heldout}.csv` |
| Review queue: every non-high-confidence item with its top-5 | `run.py` | `outputs/review_queue.csv` |
| Era drift: link 17,982 usable USFS monitoring/standard/guideline components; compare competency shares in binding direction between 1982-rule and 2012-rule plans with a plan-level cluster bootstrap | `drift.py` | `outputs/era_shift_by_competency.csv`, `outputs/all_components_top1.csv` |
| Coverage gaps: NMF topics over bottom-tercile-similarity components | `gaps.py` | `outputs/coverage_gap_clusters.csv` |
| Postings/PDs: link each paragraph of any `data/job_postings/*.txt` | `run.py` | `outputs/postings_links.json` |

## Results (2026-10-23 run; single-annotator AI gold — read the caveats)

| System | Dev P@1 (95% CI) | Dev Hit@5 | Held-out P@1 (95% CI) | Held-out Hit@5 |
|---|---|---|---|---|
| **Fused full-document (headline)** | **0.53 (0.39–0.67)** | **0.88** | **0.48 (0.26–0.65)** | **0.78** |
| TF-IDF only | 0.53 | 0.82 | 0.48 | 0.83 |
| BM25 only | 0.41 | 0.78 | 0.39 | 0.74 |
| WordLlama only | 0.39 | 0.63 | 0.43 | 0.74 |
| Title + description only (fused) | 0.45 | 0.80 | 0.43 | 0.65 |
| Task-level index, max roll-up | 0.43 | 0.61 | 0.39 | 0.70 |
| Fused + acronym glossary + name masking | 0.47 | 0.84 | 0.39 | 0.78 |

Dev n = 49 and held-out n = 23 non-noise items. Pooled dev P@1 for the headline is 0.59. Combined (n = 72): P@1 0.51
(Wilson 0.40–0.63), Hit@5 0.85 (0.75–0.91). Agreement-based confidence, combined: high 0.91 (n = 11), medium 0.53
(n = 34), low 0.33 (n = 27). 18 of 90 gold items (20%) were extraction noise; neither confidence signal reliably
flags them.

**Use:** as a candidate generator for human review (top-5 contains an acceptable competency about 85% of the
time), not as an automatic coder. Do not publish demand counts from top-1 labels without carrying the precision
and its interval along with them.

## Files you will want

- `gold/GUIDELINES.md` — how the gold labels were made and why they are weak evidence.
- `outputs/eval_report.json` — all metrics, input hashes, band cut-points, drift and gap summaries.
- `outputs/gold_eval_detail_*.csv` — per-item gold vs system for failure analysis.
