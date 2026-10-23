# X2 coding protocol — EMST task → O*NET task (and DWA) · v0.2.0

**Owner:** IA (WP-09) with LM (exposure joins) and IO (gold-set rules, `validation/spec_gold_sets.md` §6 GS-X2)
**Decision basis:** ADR-0022 X2 (two coders, κ ≥ 0.6 on match type; candidates restricted to the role family's
O*NET-SOC pool; expect ~30% none and mostly partial); ADR-0019 §2 DP-18a(a); ADR-0013 (IDs only).
**Licence:** CC0-1.0. **Labels:** [E] evidence, [J] judgment, [S] speculation.

## 1. Units and frame

- **Unit:** one live, non-held EMST v2 task in the P1 frame (`p1_frame.yaml`), pinned by `textSha256`. A unit
  whose text changes after coding is re-coded, never carried.
- **Frame (v0.2.0, 2026-10-23):** exactly the tasks in `p1_frame.yaml#taskToP1Roles` (frame ≥ 0.2.0), which WP-08
  generates from the P1 RoleProfile task bundles; each unit's roles come from that entry. v0.1.0 used the
  provisional competency superset (`competencyToP1Roles`), which the builder no longer reads.
- **Carry rule:** a coder's v0.1.0 decision is carried to v0.2.0 only when the unit's `textSha256`, O*NET-SOC pool
  and candidate list are all unchanged; every other unit is coded afresh.
- **Exclusions:** held Tribal content; government-to-government tasks (ADR-0007 §D).

## 2. Candidate pool

- O*NET-SOC codes mapped to the unit's P1 roles in X3 (`data/v2/crosswalks/onet-soc/2019`, positive rows).
- All O*NET task statements (core and supplemental) of those occupations, from the pinned release.
- Coders see six machine candidates (`build_candidates.py --k 6`) **in random order, without scores**, and may search the whole pool
  (record `found_by = pool search`). Searching outside the pool is not allowed in v0.1; a coder who believes the
  best target lies outside the pool records `NoTermFound` and notes "outside pool" (this measures X3's recall).
- **Release:** the target is O*NET 31.0 (Aug 2026). Until 31.0 is downloadable (`pipelines/onet/fetch_onet.py`),
  coding runs on the O*NET 27.2 task set that carries the Eloundou et al. labels, which ADR-0022 requires anyway;
  the 31.0 set is produced by the upstream diff (carry / needs-review / deprecated / new-candidate).
- **DWAs:** the Tasks-to-DWAs file is not available offline; DWA coding is added when 31.0 is fetched (each chosen
  task's DWAs are then attached mechanically, and coders confirm the DWA-level predicate).

## 3. What a coder records (per unit)

| Field | Values |
|---|---|
| `object_id` | `ONET:<O*NET-SOC>:<Task ID>` of the single best O*NET task, or `NoTermFound` |
| `predicate` | `skos:closeMatch` — same work, interchangeable for exposure joins; `skos:broadMatch` — the O*NET task is broader (the EMST task is one specialised part of it); `skos:narrowMatch` — the O*NET task is one part of the EMST task; `skos:relatedMatch` — associated or partial overlap; with `NoTermFound`, always `skos:closeMatch` (nothing close exists) |
| `confidence` | coder's probability that the row is right (0–1) |
| `found_by` | `candidate list` · `pool search` · `no adequate match among the shown candidates` |
| `note` | optional; required for `outside pool` |

`skos:exactMatch` is not used in X2 (different authors; wording never identical) [J].

**Decision rules [J]:** code the *work performed*, not the subject domain (a weather-forecast model task is
`relatedMatch` to an ecosystem forecast task, not `closeMatch`). Specification, review, validation and defence
tasks (G-2 split) match O*NET production tasks at most as `relatedMatch` unless the O*NET task itself is a review
task. AI-validation and formation tasks usually have no O*NET counterpart: code `NoTermFound`.

## 4. Independence, adjudication and agreement

1. Two coders per unit, **blind to each other and to the ranker's order and scores**, using this protocol and the
   prompt in `coder_prompt.md` (LLM passes) or the same sheet (human coders). A coder never codes units they
   authored. LLM coder B runs through `run_coder_b.py`: each batch is a fresh `claude -p` session with tools off,
   no MCP servers, no session persistence and an environment stripped of project and session links, in an empty
   scratch directory; it sees only `coder_prompt.md` and the shuffled sheet (pass-specific keys and order, no EMST
   IDs, competencies, roles or coder A answers), plus the POOL of the batch's occupations so that it can search the
   pool as coder A can.
2. Agreement (`kappa.py`): Cohen's κ on the 5-category match type {close, broad, narrow, related, none}, with
   bootstrap 95% CI; also exact agreement on `object_id`, and κ on the binary "any match vs none". Target
   κ ≥ 0.6 (ADR-0022). When both coders are LLMs, κ is reported as **LLM-vs-LLM agreement**, never as human
   inter-coder reliability; like agent craft ratings (CR-IO-002) it is draft evidence that does not by itself open
   the DP-18a(a) gate (IO/CA to rule otherwise).
3. Disagreements are adjudicated by a third coder (human for any selection or published-analytics use); the final
   row keeps both codes in `other` (`coder_a=…;coder_b=…`), `mapping_justification` = `semapv:MappingReview`
   after human adjudication (else `semapv:LLMBasedMatching`), and the **weakest** of the two match types as
   `weakest_match_type` (IO §6 GS-X2).
4. Gate for use: exposure joins (WP-10) may use rows at ≥ `relatedMatch` only as partial evidence, aggregated, never
   single-match (ADR-0028; WP-10 acceptance); DP-18a(a) requires ≥ `closeMatch` by two coders with κ ≥ 0.6.

## 5. Outputs

- `coding/coder-a.csv`, `coding/coder-b.csv` (IDs only).
- `data/v2/crosswalks/onet-task/<release>.sssom.tsv` via `merge_x2.py` (one row per unit; `NoTermFound` rows kept).
- `work/x2_kappa.json` (generated statistics; never typed into documents).

## 6. Pre-registration fields

`validation/preregistration_core.yaml#core_required` plus: frame version and hash; O*NET release and file hash;
pool construction (X3 set version); candidate generator version (`emst_linker` index hash); coder identities
(pseudonymous) and type (human / llm with model and prompt version); random seed for candidate order.
