# CR-FC-002: Field content for module survivors of merged FC candidates (FC-C05, FC-C17, FC-C29) and module task moves

- **From:** FC (A3), WP-03 · **To:** DB (A6), WP-06, owner of the module records; CA for information · **Date:** 2026-10-23 · **Type:** content handoff for cross-lane merges (S1 brief, Lanes) · **SemVer impact:** none (draft content)
- **Affects:** `modules/waste/…/seed-DB-C19`, `modules/air/…/seed-DB-C13`, later `modules/markets/…/seed-PS-C06` (wave 3), and three v1 task seeds still in `core/tasks/`. WP-03 has not edited module records.
- **Evidence label:** J (FC Phase 2 report §2.3, §4; candidates FC-C05, FC-C17, FC-C29).

## 1. FC-C05 → DB-C19 (site assessment and characterization, MOD-04)

DB-C19 already covers core logging, interval selection, well-installation oversight and custody. Field-craft gaps:

| Kind | Proposed text |
|---|---|
| Task (adaptation in place) | Stop drilling or sampling and upgrade protection when field-screening readings exceed the site health and safety plan's action level, recording the reading and the change |
| Task | Collect soil-gas samples to the sampling plan, checking probe seals and leak-test results before each sample is accepted |
| Indicator L2 (unaided; task-book-observation) | Halts intrusive work when screening readings exceed the plan's action level, upgrading protection before work resumes and recording each reading. |

Suggested link: let DB-C19's field tasks support the core `seed:v1-4.4.4-A` (work safely on hazardous, industrial and energized sites) and `seed:FC-C24` (custody and field QC) as `contributing` (module to core is the permitted direction).

## 2. FC-C17 → DB-C13 (ambient air monitoring networks, MOD-03)

DB-C13 already covers audits, collocation, siting and validation. Gaps:
- a station-condition task: *Document changes in conditions around a monitoring station, such as new obstructions, construction or vandalism, that affect siting criteria* (FC-a, FC-f);
- a community-network task, linking the core `seed:FC-C21` (work alongside landowners, volunteers and communities): *Support community hosts of low-cost sensors on site, checking placement and power and explaining what the data can and cannot show*.

## 3. FC-C29 → PS-C06 (digital MRV, MOD-10 markets, wave 3)

Out of scope for wave 1. When PS-C06 is authored, its field-calibration anchors should reuse the core `seed:FC-C31` (observer calibration and blind re-measurement) and `seed:FS-C04` (reference data) instead of restating them.

## 4. v1 task seeds that must move into a module (dependency direction)

These tasks still support superseded v1 seeds. Their successors live in `worklands` (MOD-14), so the files must move to `modules/worklands/tasks/` when WP-06 authors those successors. WP-03 cannot re-point them in `core/` without creating `E-DEPENDENCY-DIRECTION`:
- `seed:v1-4.5.3-T1` (tractors, excavators, skid steers) → `seed:v1-4.5.3-B`;
- `seed:v1-4.6.2-T2` and `seed:v1-4.6.2-T3` (site-specific management; variable-rate prescriptions) → `seed:v1-4.6.1`.

## Request

WP-06 decides on items 1–2 and schedules item 4 with the worklands early drafts. No CA ruling needed.

## CA ruling

- **Ruling:** **accept 1–2 for S2 (DB, inside WP-08); 3 deferred to wave 3; 4 mechanical moves by DE in S2** · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** ADR-0030 §4, `RULINGS_FOR_DE.md` §18.3, DECISION_LOG `CR-FC-002`
- **Why the CA rules:** WP-06 finished S1. DB (A6) remains active in S2 as WP-08 contributor for the module roles R24–R30.

1. **FC-C05 → DB-C19 (R27, P2): accepted.** DB (A6) adds the stop-and-upgrade adaptation task, the soil-gas sampling task and the L2 halt indicator in S2, writing in the records (the S1 builders are frozen, ADR-0030 §5; if DB re-runs `build_wp06.py` it must first port these edits into `docs/build/WP-06/src/`). It also adds the `contributing` links to core `seed:v1-4.4.4-A` and `seed:FC-C24`, which run module → core, the permitted direction. FC (A3) reviews.
2. **FC-C17 → DB-C13 (R28, P2): accepted.** DB adds both tasks. The community-sensor task supports core `seed:FC-C21` as `contributing` and states what low-cost sensor data can and cannot show. It names no product.
3. **FC-C29 → PS-C06: deferred to wave 3** with MOD-10. When PS-C06 is authored, its field-calibration anchors reuse `seed:FC-C31` and `seed:FS-C04`, not restated text. This is recorded in `docs/decisions/integration/disposition_amendments.csv`.
4. **Task moves: DE in S2, mechanically.** No text changes; FC and DB review the result. They are listed with the other S1 residue moves in `RULINGS_FOR_DE.md` §18.3:
   - `seed:v1-4.6.2-T2` and `-T3` move to `modules/worklands/tasks/` and support `seed:v1-4.6.1`, which exists;
   - `seed:v1-4.5.3-T1` moves there and supports the planned `seed:v1-4.5.3-B`, so `W-REF-PENDING` is expected until MOD-14 is authored (wave 2).
