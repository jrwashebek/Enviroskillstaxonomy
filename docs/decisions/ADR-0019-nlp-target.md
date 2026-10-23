# ADR-0019: NLP linking target — competencies now, tasks later by a pre-registered criterion (DP-18a)

- **Decision point:** DP-18 (NLP target), with named sub-decision **DP-18a** (the task-switch criterion)
- **Status:** accepted
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** IA, LM, IO, DE, CP, TN, SL, LC
- **Related:** ADR-0001 (task spine), ADR-0008 (signals use linker quality), ADR-0012 (PII), ADR-0022 (O*NET task crosswalk), ADR-0028 (signal layer)

## Context

IA's prototype links land-management-plan requirements to v1 competencies with a fused lexical/semantic baseline: on 72 non-noise gold items, P@1 0.51 (95% CI 0.40–0.63) and Hit@5 0.85 (0.75–0.91); held-out P@1 0.48 (0.26–0.65). Linking to v1's three-tasks-per-competency layer did worse than linking to whole competency documents (dev P@1 0.43 vs 0.53; Hit@5 0.61 vs 0.88). Hand rules fitted to dev errors *lowered* held-out P@1 (0.48 → 0.39). 20% of sampled components were extraction noise, and neither confidence signal isolates them [E: IA §5]. LM: naive lexical matching of v1 tasks to 19,265 O*NET tasks was right about a quarter of the time [E: LM §5.3]. The gold set is single-annotator AI judgement, fit only for engineering (IA §10).

## Decision

1. **Now: link text to competencies**, using the full competency document (title, description, linked tasks, indicators), and record the best-supported task as `evidencesTask` evidence on each link (P-IA-08).
2. **DP-18a — switch to tasks** for a given role family or module when **all** hold: (a) L2 has 15–30 v2 task statements per role profile in that family, crosswalked to O*NET tasks/DWAs at ≥ "close" match by two coders (κ ≥ 0.6); (b) on a held-out gold set of ≥ 100 items for that family, task-level linking beats competency-level linking on P@1 by ≥ 0.10 with non-overlapping 95% CIs; (c) abstention on noise reaches ≥ 0.7 recall. The switch is recorded as a change record citing the evaluation.
3. **Human review is the default.** The linker is a candidate generator; every link used in a published signal is reviewed, except aggregate signals whose published numbers are corrected for measured linker error.
4. **Acceptance rule for any method change** (e.g. IReRa-style LLM rerank, P-IA-10): held-out P@1 improves by ≥ 0.10 with non-overlapping CIs and noise abstention ≥ 0.7 recall; frozen model and prompt versions; verbatim evidence spans checked against the source; posting text treated as untrusted data.
5. **Never publish uncorrected top-1 counts** (P-IA-11). Every ChangeSignal derived from linking carries `linkerQuality{goldSet, precisionAt1, ci95}` and corrected intervals.
6. **Gold sets:** a 600-item environmental gold set, double-annotated by human SMEs with IO, MELO layout, dev/held-out split, SCORES.md per release (P-IA-09, P-DE-10); stratified so ≥ 40% of items come from outside public lands (water, air, waste, EH, energy, ESG corpora; P-DB-17).
7. **Upstream classifier** for requirement vs noise, propagating OpenLMP extraction confidence (P-IA-12). **PII stripping** at ingestion and **Tribal quarantine** are mandatory stages (ADR-0007, ADR-0012).
8. **Thresholds by use** (answers IA open Q4, set with IO and FH): mappings used in **selection** contexts need two human reviewers and ≥ "close" match; **analytics** mappings need linker-quality reporting and error correction; **navigation** mappings may be single-reviewed candidates labelled as such.

## Rationale

- The richer competency documents "earn their keep"; v1 tasks are too generic and too few to be the NLP target yet (IA §5.6) — this does not refute the task spine (ADR-0001), it sequences it.
- The external measures EMST will ingest are anchored to O*NET tasks/DWAs (LM P-LM-02), so L2 must be built crosswalk-first; the switch criterion ties NLP to that build.

## Consequences

- Change signals from postings, PDs and plans are competency-level until DP-18a fires per family; task-level exposure joins come from the curated O*NET crosswalk, not from NLP links.
- IA and LM share one evaluated linker (IA disagreement with LM resolved as complementary).

## Dissent and trade-offs

- **CA's own task-spine lean** wanted tasks sooner; IA's evidence wins on timing.
- **Trade-off named:** accuracy now versus the analytical power of task-level joins later; plus LLM run cost, provider dependence and reproducibility for the rerank stage (IA disagreement 5).
