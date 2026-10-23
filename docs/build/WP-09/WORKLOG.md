# WP-09 Crosswalks X1–X12 — worklog (A2 IA)

Owner: A2 IA (Workforce Systems Interoperability Architect / Skills Intelligence Engineer).
Co-owners for named sets: FH (X3–X5, X9), SL (X5), LC (X6, X10, X12 with DC), PS (X8, X11), DC (X12).
Binding inputs: ADR-0022, ADR-0019, ADR-0013, `vocab/mapping_predicates.yaml`, SPEC §15, AUTHORING_GUIDE.
Labels: [E] evidence, [J] judgment, [S] speculation.

All rows in every set written here are **agent drafts**: `raterType`-equivalent is the author ID
`emstagent:ia-wp09@phase4` (model `claude-opus-5-5`, prompt `wp09-crosswalk@1`), `review_status=candidate`
in `other`, no human reviewer, evidence label S unless the row cites an external code check (E). Nothing here is
a reviewed or selection-grade mapping (ADR-0022 §4). **No public alignment claim may rest on these sets.**

## Conventions adopted (pending WP-08 / CA confirmation — see CR-IA-001)

- Role keys: `seed:<role_key>` from `docs/decisions/mvp_role_set.csv` (e.g. `seed:R11-environmental-permit-writer`).
  Variant keys: `seed:<role_key>/<sector_actor>` (e.g. `seed:R11-environmental-permit-writer/state`).
  When WP-08 mints different keys, rows are re-keyed by `pipelines/crosswalks/rekey.py` (no hand edits).
- Register records (CR-DE-002, no TYPE prefix yet): `seed:opm-series/<code>`, `seed:state-class/<jur>/<code>`.
- External code namespaces: see each `.sssom.yml` `curie_map`. IDs only in CC0 files (ADR-0013 §5).
- Every row carries in `other`: `weakest_match_type=…;review_status=…;evidence=…` plus set-specific keys; the
  rationale is in `comment` (EMST-authored text, never upstream text).

## Session log

- 2026-10-23: read brief, build plan, ADR-0013/0019/0022, SPEC §15, mapping vocab, validator SSSOM rules,
  Phase 2 crosswalk method and prototype, FH/SL/LC/PS inputs, V1–V4 verification.
- Network: shell reaches PyPI and raw GitHub only; onetcenter.org, esco.ec.europa.eu, bls.gov and
  huggingface.co return proxy 403 (not retried). O*NET 31.0 and ESCO v1.2.1 bulk files could not be
  downloaded this session; see version-gap notes in X2 prep and X7.
- X3 built: `pipelines/crosswalks/x3_soc.py` + `curation/x3_role_soc.csv` → `data/v2/crosswalks/onet-soc/2019` and
  `soc/2018`. All 37 MVP roles covered; verified v1 errors recorded as `predicate_modifier: Not` rows (F10→19-1012,
  F12→33-2021, F8→23-1011, F11→25-4031, F13→29-9021) plus ADR-0022 §5 additions. Codes checked offline against
  O*NET 27.2 data-level occupations (O*NET-SOC 2019) and BLS OEWS May 2021 (SOC 2018) — `reference/*.txt`.
  Finding: mvp_role_set R19 cited stale O*NET-SOC 2010 code 19-1031.01 (CR-IA-001, accepted).
- CR-IA-001 (role/variant seed keys; series and SOC errata) and CR-IA-002 (`semapv:LLMBasedMatching` is not valid
  in the SSSOM 1.0 schema) opened and **ruled by CA the same day** (both accepted). `validate_sets.py` reports
  strict-1.0 and 1.0+1.1-values results with the affected-row count, reading
  `vocab/mapping_predicates.yaml#justifications_sssom_1_1_only`.
- X4 built: `x4_opm_series.py` → SeriesRecords in `data/v2/registers/opm_series/` (FH's 73 + 6 added for MVP
  coverage: 0201, 0601, 1712, 1801, 5408, 5409 — titles IA judgment, FH to verify); 15 series
  `proposed-realignment` per the CHCO memo re-read 2026-10-23 (0408/0482/0486 are NOT proposed);
  `crosswalks/opm-series/2026-10-23` (role→series) and `opm-series-competency/2026-10-23` (FH core/supporting
  judgments chained through X1; rows on held v1 codes omitted).
- X5 built: `x5_state_classes.py` + `curation/x5_classes.yaml`, `x5_variant_class.csv` → StateClassRecords in
  `data/v2/registers/state_classes/` (TX, WA, Lewis County WA EH, Philadelphia Water Department) and five sets
  (`state-class-tx|wa|pa`, `local-class-wa-lewis-county`, `local-class-pa-philadelphia-water`). PA class codes are
  not exposed in postings: PA rows are position overrides (allowed for pilots) with `register_record=pending`.
  Spec text stored as URL + null hash (hash-and-URL rule). Records name variants as `roleVariantKey` until WP-08
  authors the variants (re-run the script to link them; validator would otherwise report dangling refs).
- Open for SL: verify Lewis County grade 122 mapping to the 2026 schedule; retrieve PA OA job specifications (class
  codes) and current TX Park Ranger / Hydrologist pay (2019 values recorded as dated); mvp_role_set R37's PA example
  is a regulator-side class (mirror only), mapped to R12 instead.
- X7 built: `x7_esco.py` (candidates from `pipelines/linker` hybrid index, IDs only, to `work/`) + LLM review
  decisions `curation/x7_esco_review.csv` → `crosswalks/esco/1.2.0`. VERSION GAP: v1.2.1 unreachable; pinned to the
  v1.2.0 skill URIs bundled in esco-skill-extractor 0.1.18 (sha256 in the set yml). Many lexical homonym candidates
  rejected as `Not` rows so they do not resurface. Navigation-grade at most; no ESCO alignment claim.
- X9 built: `x9_ecq.py` + `curation/x9_ecq.csv` → `crosswalks/opm-ecq/2025-10-01`. Five current ECQs and their
  15 competencies re-verified on OPM's page 2026-10-23 (`reference/opm_ecq_2025-10-01.csv`); retired names never
  targets. FWCI / USA Hire / OPM general competency parts of X9 not built (scope given: five-ECQ only).
- X8 / X11 seeds: `x8_x11_private.py` → `crosswalks/emst-private-ja/0.1.0` (PS reference job architecture) and
  `emst-public-private/0.1.0` (PS translation rows with friction fields; `emst:mirrorRole` for inverted authority
  pairs). TR-14 (cultural resources / government-to-government) not seeded — Tribal hold, left for TN.
- Linker (DP-18): `pipelines/linker/emst_linker` 0.2.0 (TF-IDF + BM25 + optional WordLlama, min-max fusion,
  ranker-agreement confidence; PII strip and Tribal quarantine before linking; `aggregate()` refuses to count
  without gold-set quality — `UncorrectedCountError`). Gold-set design `GOLD_SET_DESIGN.md` (GS-LINK, 600 units).
  No gold set exists yet, so no linkerQuality is published.
- X2 prep and run: `pipelines/onet/fetch_onet.py` (31.0 fetch 403; 27.2 = Eloundou base cached in scratch),
  `pipelines/x2/` protocol, provisional P1 frame, candidates, coder A (agent) on 273 units, merge →
  `crosswalks/onet-task/27.2`. Kappa: not computable (one coder); `coder_prompt.md` ready for a blind coder B in a
  fresh context. Coder A NoTermFound share 56% (ADR-0022 expected ≈30%): v2 P1 tasks are dominated by
  specification, review and AI-output validation work with no O*NET task counterpart — a finding, not a defect.
- X2 re-run on WP-08's P1 frame (frame `0.2.0-wp08-bundles`, 316 tasks): `build_candidates.py` now reads
  `taskToP1Roles` only (roles per task; refuses older frames); `--k 6` as in v0.1.0. O*NET 31.0 re-tried
  2026-10-23: onetcenter.org still refused by the egress proxy (403), no mirror found, so the set stays on 27.2
  (version gap recorded in the set) and DWAs remain pending. Coder A: 92 v0.1.0 decisions carried (text, pool and
  candidate list unchanged; carry rule in CODING_PROTOCOL.md v0.2.0 §1), 224 coded afresh. Coder B: four fresh
  `claude -p` sessions (`run_coder_b.py`, model claude-opus-5-5, tools off, no MCP, no session persistence, empty
  scratch dir, env stripped of session/project links after a probe showed the claude.ai project context leaking in);
  each saw only `coder_prompt.md` (v2, self-contained) and the shuffled sheet under pass keys, plus the pool. Prompts
  and raw answers stay in scratch (O*NET text). Agreement (`work/x2_kappa.json`, generated) is **LLM-vs-LLM
  agreement, not human inter-coder reliability**; it is below the 0.6 target. Main split: coder A NoTermFound vs
  coder B relatedMatch on review/validation/AI-oversight tasks (B reads rule 3 more leniently). `merge_x2.py`
  keeps coder A's object on disagreements, marks them `needs-adjudication`, and records the weaker of both codes.
- Tooling: `report_counts.py` (counts → `crosswalk_counts.json`), `build_all.sh`, `tests/test_sssomlib.py`.

## Open items (end of session 2026-10-23)

1. X2: adjudicate the `needs-adjudication` rows (human third coder for any selection or published use) and decide
   with IO whether rule 3 (AI-validation / formation tasks → NoTermFound) needs sharper wording before a re-code;
   LLM-vs-LLM κ is below 0.6 and does not open the DP-18a(a) gate.
2. Re-pins: O*NET 31.0 (X2, X3 O*NET-SOC check), ESCO v1.2.1 (X7) via the upstream-diff pipeline; DWAs for X2.
3. P1 frame: re-run `build_candidates.py` and both coders on changed units whenever WP-08 regenerates
   `p1_frame.yaml` (carry rule applies).
4. WP-08: once variants exist, re-run `x5_state_classes.py` (links `roleVariant`) and `rekey.py` if keys differ.
5. FH: verify the 6 added OPM series titles/groups; SL: items above; PA class codes (OA job specs).
6. X9 FWCI / USA Hire parts; X10 is LC/IO's (fails the WP-09 profile — not mine, not changed).
7. Human review of every set: all rows are agent drafts (`raterType llm`, evidence S unless cited).
