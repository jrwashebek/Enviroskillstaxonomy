# CR-FC-001: Field-performance content for SL-C03 from merged candidate FC-C04

- **From:** FC (A3), WP-03 · **To:** SC (A5), WP-05, owner of `seed:SL-C03`; CA for information · **Date:** 2026-10-23 · **Type:** content handoff for a cross-lane merge (S1 brief, Lanes) · **SemVer impact:** none (draft content)
- **Affects:** `data/v2/core/competencies/seed-SL-C03.yaml` and its tasks and indicators (WP-05 lane). WP-03 has not edited them.
- **Evidence label:** J (FC Phase 2 report §1.5 and anchors; codebook E4).

## Why

`candidate_disposition.csv` merges FC-C04 (Conduct on-site environmental compliance inspections) into SL-C03 "as its field-performance anchors". SL-C03 as drafted by WP-05 already carries most of it: checklist inspection, compliance sampling under custody, and on-site resolution of ambiguity (L3). Three field-craft elements of FC-C04 are not yet explicit:

1. **Perceptual detection beyond the checklist** (FC-a): recognizing violations and risk from site conditions the checklist does not ask about.
2. **Adaptation in place** (G-2 split): extending or changing the inspection on site when conditions differ from the records.
3. **Measurement integrity of the inspector's own field measurements** (FC-b), which an enforcement case relies on.

## Proposed additions (for WP-05 to accept, edit or reject)

| Kind | Proposed text | Notes |
|---|---|---|
| Task (adaptation in place) | Extend an inspection beyond the planned checklist when site conditions show an unpermitted activity, discharge or control failure, documenting the observation | WF-ENFORCE; on-site-required; formation yes; mentorship H |
| Indicator L2 (unaided; task-book-observation, seeded-error-work-sample; obs4 3) | Recognizes evidence of an unpermitted discharge, control failure or unreported activity outside the checklist, documenting it with photos, measurements and location. | distinguishingAttribute ATT-CPX |
| Indicator L1 (unaided; record-audit; obs4 3) | Measures field parameters during an inspection with meters calibrated that day, recording the calibration so that each measurement can be used as evidence. | links FC-C24 custody and QC |
| Indicator L2 (assisted; record-audit; obs4 3) | Checks drone or remote imagery used to target an inspection against conditions observed on site, recording where the imagery was wrong. | optional; links FC-C02 |

Suggested cross-links (task `supports` with strength `contributing`; core to core, so no dependency issue): the sampling task to `seed:FC-C24` and `seed:FC-C16`; the site-entry task to `seed:v1-4.4.4-A` (hazardous, industrial and energized sites).

## Request

WP-05 decides whether to add these to SL-C03. If accepted, WP-03 asks to be listed as a contributor in the record's provenance agents; nothing else changes in WP-03's lane. No CA ruling is needed unless WP-05 disagrees with the merge itself.
