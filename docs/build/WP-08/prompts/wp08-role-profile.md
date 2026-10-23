# Prompt and method: WP-08 role profiles (`wp08-role-profile@1`)

Frozen 2026-10-23 for `emstagent:fh-agent@wp-08` (model `claude-opus-5-5`). Every value produced under this prompt is an
agent draft: `raterType llm`, `validationStatus draft`, evidence label **S**. Nothing produced here is a job analysis,
an SME rating or a classification. LLM-coder gate level **G0** (`validation/protocol_llm_coder_gate.md`): values are
stored as draft evidence and pre-fills only; task criticality and needed-at-entry flags can never reach G2.

## Inputs read (binding)
ADR-0006, -0016, -0017, -0024, -0025, -0027, -0029; SPEC §5.7–5.9, §10; `mvp_role_set.csv`; WP-03 task-bundle handoff
(`[S]` suggestions); WP-04/05/06/07 role→competency maps and TX suggestions; WP-07 formation provisions; X3/X4/X5/X11.

## Instructions (as applied)
1. **Grain.** One RoleProfile per `mvp_role_set.csv` row, keyed `seed:<role_key>`; levels exactly as listed there.
   A RoleProfile lives in the area of its home module; a core profile may reference only core records.
2. **Competency targets.** For P1: 6–12 role-specific critical targets (importance ≥ 4), plus supporting targets
   (importance 2–3). For P2: 6–10 critical targets. The TX-A floor (DC-CAND-01, -02, -13, -05) is added to every role
   at L1 at least (WP-04). Target levels are read against `vocab/proficiency_levels.yaml#role_level_bands` and
   clamped to the levels at which the competency publishes indicators. `criticalForSelection` is always false.
   `distinguishing` marks competencies that separate the role from its nearest neighbours.
3. **Task bundle (P1).** 15–40 live, non-held, authored (`validationStatus: draft`) tasks chosen by FH from the
   competencies' task pools. Per task: importance 1–5 (consequence for the role's function), a relative time
   weight normalized to `timeShare` across the whole role (shares sum to 1.000), `critical` (error has severe,
   irreversible or legal consequence), `neededAtEntry` (needed on the first day at the role's lowest level),
   `formationTask` (WP-07 provision or WP-03 suggestion that FH agrees with), and the role levels that perform it.
   Every critical target must be served by at least one bundled task.
4. **Task bundle (P2–P4 auto rule, starter-kit depth).** For each targeted competency with importance ≥ 3, in
   descending importance: its primary tasks (live, authored, in an allowed area), up to 3 (4 for importance-5
   competencies), at most 40 tasks overall. Defaults: importance = the competency's importance; time weight = the
   same; levels by the statement's first verb (Set/Establish/Charter/Govern → top two levels; Design/Plan/Lead/Train/
   Evaluate/Decide/Direct/Supervise/Negotiate/Recommend/Advise/Certify/Resolve/Testify/Defend/Brief/Specify → senior
   upward, else from the second level); `critical` = importance-5 competency and performed at every level;
   `neededAtEntry` = performed at the lowest level and competency importance ≥ 4; `formationTask` = WP-07 provision
   or WP-03 suggestion performed at the lowest level. FH did not review each auto-selected task.
5. **Variants.** One per sector actor listed for the role, plus named slices (`/applicant-preparer` on R37). Tribal
   variants are held stubs only (ADR-0007 §D): no tasks, instruments, credentials or crosswalks. Federal, state and
   local variants carry the disclaimer "Not a classification basis / not a job analysis / not for RIF or rating
   decisions." Federal variants carry an `indicativeGradeOrBand` read from FH's Phase 2 proficiency proposal
   (report §6.2), labelled "not a classification criterion", with the role level each band is read against in
   brackets. Credential gates and sign-off are drafts until an E-labelled source is attached (SPEC §10 rule 8).
6. **Change-view atoms (P1).** For each P1 role, name the tasks being reshaped (`content_change_types`) and role-level
   signals (`role_signal_types`), each with driver tags (`vocab/change_types.yaml#driver_tags`) and, where known,
   registered instrument and signal IDs. Fiscal and policy drivers are tagged as such so they are never read as AI
   effects. v1 values are never used as inputs; they appear only as prior evidence pointers computed by the view.
7. **Mirror and mobility.** `entryFrom`/`progressesTo` carry pre-registered pathways (ADR-0006 §7). Mirror pairs
   (ADR-0017 §4) are X11 rows (`emst:mirrorRole`). Core profiles never link to module profiles (dependency direction).
8. **Never**: personal data; Tribal-related content outside held stubs; L4 product or L5 instrument names in role
   text; claims of validation, retention or job-analysis confirmation.
