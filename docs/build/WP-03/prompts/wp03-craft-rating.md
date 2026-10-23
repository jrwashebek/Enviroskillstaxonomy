# WP-03 craft-rating prompt (frozen) — `wp03-craft-rating@1`

Owner: FC (A3) · Model: `claude-opus-5-5` · Frozen: 2026-10-23 · Codebook: `validation/codebook_craft_ratings.md`
(`emst-craft-codebook@1.0.0-draft`), definitions in `vocab/crafts.yaml` 1.0.0-draft · Licence: CC0-1.0

## Frame

Each pass receives a list of units produced by `docs/build/WP-03/rating/make_frames.py`: a random unit code and the
task statement only. The frame never shows the parent competency, domain, module, v1 code, v1 craft label, any
other pass's values or any machine suggestion (codebook §2; XR-01). Each pass uses a different random ordering
(seeded per pass). Tasks whose text matches the Tribal hold are excluded from the frame (codebook E14).

## Instruction (applied to each unit)

1. Name the deliverable in five words or fewer.
2. FC: presence? then physical consequence or ground-truth authority? -> 2 / 1 / 0.
3. DC: evidence product + judged by warrant + method choice or checking? -> 2 / 1 / 0.
4. SC: a commitment needing another institution's or the public's authority, legitimacy or agreement that must
   hold? -> 2 / 1 / 0.
5. No craft at 2 is allowed (general professional practice). Do not raise a 1 to avoid it.
6. Apply the common-error rules E1-E15 of the codebook (notably E3: remote review needing field formation is FC 1).
7. Confidence: low | med | high. Use cannot-code with a reason when the text does not allow a decision.

## Output (one line per unit)

`<unit> <FC> <DC> <SC> <confidence> [cannot-code:<reason>] [note]`

## Status of the output

The three passes are three runs of one model family with different unit orderings in one session. Their agreement
is run-to-run consistency, not inter-rater reliability, SME agreement or Delphi retention
(`validation/protocol_llm_coder_gate.md` §1.1). Every value is `raterType: llm`, evidence label S,
`validationStatus: draft`, gate level G0 (stored as draft evidence; never rendered; never a pre-fill shown to human
raters in a reliability study).
