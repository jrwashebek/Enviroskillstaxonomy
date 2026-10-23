# Mini gold set — annotation guidelines (IA, v0.1)

**Status: single-annotator AI judgment.** Every label in `gold_set.csv` (dev, 60 items) and `gold_heldout.csv`
(held-out, 30 items) was assigned by one AI agent (the IA role, Claude) working from the component text and the
list of 222 v1 competencies. No human SME has reviewed them. Treat the set as a *development* reference that
makes the prototype's behaviour measurable, not as validation evidence (IO owns validation).

## Unit and question

Unit: one OpenLMP plan component (verbatim `text`). Question: *which v1 EMST competencies would a professional
need to exercise, as a substantial part of the work, to implement, comply with, or monitor this plan direction?*

## Fields

| Field | Rule |
|---|---|
| `item_status` | `requirement` (plan direction); `generic` (direction too general to imply a specific competency, e.g. a monitoring-category header); `noise` (extraction artefact: table fragment, header, legend, narrative, glossary, public comment). Noise items are excluded from P@k and used to test abstention. |
| `primary_code` | The single most specific v1 competency. Blank only when nothing applies. |
| `acceptable_codes` | Every v1 competency that is defensible (pipe-separated). Includes the primary. |
| `fit` | `good` if at least one v1 competency covers the requirement well; `weak` if the best one only partly covers it (a coverage-gap signal); `none` for noise with no content. |
| `gap_theme` | For weak fits, the missing function in plain words. |

## Procedure

1. Items were drawn by `emst_link/sample.py` (stratified by state × component type, with a state-agency floor)
   **before** any ranking was produced, and labelled from text only (`annotation_mode = blind`).
2. After the first evaluation run, the system's top-5 for the dev set was inspected and five defensible
   competencies the annotator had missed were added to `gold_pooled_additions.csv` (`pooled-post-hoc`). Metrics
   are reported both strict (blind labels only) and pooled. Pooling inflates scores; strict numbers are the headline.
3. Changes to the linker designed after inspecting dev-set errors (acronym glossary, proper-name masking,
   agreement confidence) were scored only on the held-out set, which was drawn and labelled blind afterwards.

## Known biases

- One annotator, who also built the linker: no inter-rater reliability is available. A second, human annotator
  on at least the 90 items (Cohen's kappa on primary code; Jaccard on acceptable sets) is the next step.
- The annotator knows the v1 competency list well, which may make acceptable sets broader than a field
  practitioner would draw them (inflating P@1) or narrower where field vocabulary is unfamiliar.
- 95% of the corpus is USFS plans in western states; results do not transfer to water, air, waste or ESG text.
