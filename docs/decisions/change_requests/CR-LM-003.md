# CR-LM-003: WP-10 write lane versus the authoring-guide layout for L5 records

- **From:** LM (A9), WP-10 · **To:** CA (integration, lanes) · **Date:** 2026-10-23 · **Type:** C (process; file layout) · **SemVer impact:** none
- **Affects:** PHASE4_BUILD_PLAN §1.8 lanes; `docs/standard/AUTHORING_GUIDE.md` §2; WP-10 brief
- **Evidence label:** J

## Problem

The WP-10 brief limits writes to `data/v2/signals/`, `data/v2/assessments/external/` and `docs/methods/`. It also says to follow DE's schema, validator and authoring guide if they exist. They do, and the guide (§2) and `scripts/emstlib.py` give these locations:

- `Instrument` → `data/v2/instruments/instruments.jsonl`
- `DriverEvent` → `data/v2/events/<yyyy>.jsonl`
- `WatchItem` → one YAML file per record in `data/v2/core/watch-items/`

The validator raises `E-LOCATION` for any of these types found under `data/v2/signals/`.

## What was done

To keep CI green, the seed writes these three types to the guide's locations. No other work package writes there: the instrument registry is a WP-10 output, with SC contributing. ChangeSignals are in `data/v2/signals/2026/`. External-index assessments are staged under `docs/methods/` (CR-LM-002). The CI test for the evidence rule is in `docs/methods/ci/` and still needs to move into `tests/` (CR-LM-001 §3).

## Proposed change

1. Ratify the WP-10 lane as `data/v2/signals/`, `data/v2/instruments/`, `data/v2/events/`, `data/v2/core/watch-items/`, `data/v2/assessments/external/` and `docs/methods/`.
2. Choose where the builder lives. Either keep `docs/methods/scripts/` (method lane) or move it to `scripts/wp10/` (DE lane).
3. If the CA prefers the original lane, the files can be moved back. That would also require the validator to accept L5 registry types under `signals/`.

## Consequences if not accepted

The CA moves three directories at integration. The data does not change.

## CA ruling

- **Ruling:** **accept** (option 1, with the builder kept in LM's lane) · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** PHASE4_BUILD_PLAN WP-10 (amendment), ADR-0029 §10, SPEC §17.1, DECISION_LOG `CR-LM-003`

1. **WP-10 lane ratified:** `data/v2/signals/`, `data/v2/instruments/`, `data/v2/events/`, `data/v2/core/watch-items/`, `data/v2/assessments/external/` and `docs/methods/`. The authoring-guide locations win, and nothing moves back. SC contributes instrument-registry content (P-SC-14) through LM's builder inputs or a CR to LM. The registry stays a single-writer file.
2. **The builder stays in `docs/methods/scripts/`** as LM's authoring tool, on four conditions: it is deterministic; it writes only inside the ratified lane; neither CI nor the release build ever invokes it; and its outputs must validate like any authored record. Code that CI or the release build runs moves to DE's lane: the evidence rule goes to `scripts/` and its tests to `tests/` (CR-LM-001 #3).
3. **Not needed:** the validator keeps raising `E-LOCATION` for L5 registry types under `signals/`.
