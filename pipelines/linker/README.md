# emst_linker — competency-level linker (DP-18; ADR-0019)

Maps text describing work demands (plan requirements, postings, PDs, curricula) to EMST v2 **competencies**, using
the full competency document (label, statement, definition, supporting tasks, indicators), and records the
best-supported task as `evidencesTask` evidence. It is a **candidate generator for human review**, not a coder.

```bash
cd pipelines/linker
python -m emst_linker info                       # version stamp: linker, index and corpus hashes, semantic backend
python -m emst_linker link --input items.csv --k 10 --out links.jsonl   # items.csv: item_id,text[,employer_type]
python -m pytest -q tests                         # synthetic tests (no network)
```

| Module | Role |
|---|---|
| `corpus.py` | builds competency documents from `data/v2` (core + modules); drops superseded, withdrawn and **held** records |
| `index.py` | hybrid retrieval: TF-IDF + BM25 + optional WordLlama static embeddings, fused per query (Phase 2 weights) |
| `safety.py` | PII stripping, Tribal quarantine, evidence-span check for any later LLM stage (ADR-0019 §4, §7) |
| `link.py` | ranks competencies, attaches `evidencesTask`, confidence band from ranker agreement, coverage-gap flag |
| `quality.py` | evaluation with bootstrap CIs; `linker_quality`; `aggregate` = misclassification-corrected shares only |
| `config.py` | every tunable; `TASK_TARGET_FAMILIES` stays empty until DP-18a fires with a change record |

## Rules enforced in code

- **No uncorrected top-1 counts** (ADR-0019 §5, P-IA-11): `quality.aggregate` raises `UncorrectedCountError`
  without a held-out confusion matrix and `linkerQuality`; the CLI never prints per-competency counts.
- **Held content never indexed or linked:** held records are excluded from the corpus; Tribal-flagged input
  items are quarantined before linking and only counted.
- **Untrusted input:** text is data; the only LLM hook planned (IReRa-style rerank) must verify evidence spans as
  substrings (`safety.verify_span`) and pass the ADR-0019 §4 acceptance rule on GS-LINK.
- **Version stamp on every row:** linker version, index SHA-256, corpus SHA-256, semantic backend.

## Status and known limits

- Engineering baseline carried from the Phase 2 prototype (`docs/research/interop-skills-intelligence/prototype/`),
  now indexing v2 records. Phase 2 numbers (P@1 0.51, Hit@5 0.85 on 72 AI-labelled items) were measured on **v1**
  competencies and an engineering-only gold set; **no v2 evaluation exists yet**. GS-LINK (`GOLD_SET_DESIGN.md`)
  must be built with human SMEs before any linked signal is published.
- Lexical matching shows homonym failures (e.g. "channel", "credit", "load", "scenic") — seen again in the X7 ESCO
  re-run; the rerank stage and a requirement/noise classifier are the planned upgrades (pipeline_design §3).
- Licence: Apache-2.0 (code); CC0-1.0 (documents).
