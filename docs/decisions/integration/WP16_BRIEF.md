# WP-16 Integration and release candidate: brief

**Owner:** the Chief Taxonomy Architect (CA), working with the Data Engineer (DE), as one integration agent that holds both codes.
**Build plan:** `docs/decisions/PHASE4_BUILD_PLAN.md`, WP-16 and the §5 release gate.
**Date:** 2026-10-23.

## Goal

Produce `2.0.0-rc.1`, an honest release candidate. It need not be a perfect one. Every gate item either passes, or is reported as failing with the reason and the fix.

## Read first

- `CHARTER.md` and `TEAM_BRIEF.md`.
- The build plan: §1 ground rules, WP-16, and the §5 release gate.
- `docs/standard/SPEC.md`, in particular §18 on conformance.
- ADR-0003 (core size), ADR-0007 (Tribal hold), ADR-0010 (IDs and minting), ADR-0013 (licensing), ADR-0024 (release criteria), ADR-0029 and ADR-0030 (earlier rulings).
- `docs/decisions/DECISION_LOG.csv`, `docs/decisions/PROJECT_LEAD_DECISIONS.md` and `docs/decisions/integration/s1_integration_review.md`.

## Step 1: decide the open items

Record every decision in a new `docs/decisions/ADR-0031-wp16-integration-rulings.md` and add rows to `DECISION_LOG.csv`. Then apply them; as CA and DE you may edit `vocab/rules/`, `schema/`, `scripts/` and `data/v2/`.

1. **Pending items.** Decide P-01, P-02 and P-03 in `docs/decisions/integration/pending_for_CA_integration.md`.
   - P-01 is display-gate 1.1.0, with IO's three judgment calls and DE's follow-up in `scripts/rules/gated_values.py`.
   - P-02 is the six human-resources view rules.
   - P-03 is the test-fixture duplication.
2. **Open change requests.** Find every request in `docs/decisions/change_requests/` that has no ruling in `DECISION_LOG.csv`. These include CR-FIX-A-001 to 003 and any CR-FIX-B or CR-FIX-C files. Rule on each: accept, accept with changes, defer or reject.
3. **Open items from the S2 close-outs.** These are listed in `docs/build/S2-closeout-A/WORKLOG.md` and `docs/build/S2-closeout-B/WORKLOG.md`.
   - The credential record for the wildland fire position qualification, and its builder, still use the wrong form "NWCG is not a party". Use claims register row WF-10.
   - The instruments in `docs/build/S2-closeout-A/instruments_to_register.csv` need registering in the instrument registry. Register only what you can source from existing verified records. Otherwise leave each one as a watch item.
   - The R13 role bundle needs the new competencies.
   - R26 needs an SL-C03 target.
   - `docs/build/WP-07/PATHWAYS.md` is stale.
   - `validate_v2.py --strict` reports 31 dangling-reference errors.
   - Reviews named in the orders remain open (FC, SC and DC). Record them as open review debt. Do not self-review them.
4. **Wrong forms in data.** CR-FIX-A-003 lists text in `data/v2` that still uses wrong forms such as "nine environmental bureaus" and "monitoring requirements". Fix that text, then change those `do_not_say` entries in `docs/methods/claims_register.csv` from double to single quotes, as Fix-A asked, so the explorer check enforces them.

## Step 2: build rc.1

1. **Mint IDs.** Mint persistent IDs as ADR-0010 and the AUTHORING_GUIDE describe, using the single writer, `scripts/mint_id.py`, and the append-only registry. Mint for everything the release gate publishes. Held Tribal content gets no public ID, per ADR-0007 §D.
2. **Keep the data and its consumers in step.**
   - Update `scripts/update_readme_status.py` output in `README.md`.
   - Regenerate the views with `pipelines/views/build_views.sh`.
   - Make sure the explorer in `site/` still builds and that `site/check-output.mjs` passes.
   - If minting changes what the site or the views need, fix them. You may touch `pipelines/` and `site/` for this, keeping the explorer's existing fixes.
3. **Build the release.** Run `python scripts/build_release.py` with the release profile and version `2.0.0-rc.1`. Two builds must be byte-identical. Generate the release notes and the counts:
   - competencies by kind, module and lifecycle;
   - roles by tier;
   - held items, as a count only.

   Also produce the delta file against the v1 baseline and a comment-window plan.

   Put the human-readable release notes in `docs/release/2.0.0-rc.1/RELEASE_NOTES.md`, generated rather than typed. The release notes must carry the authorship statement from `docs/review/FIX_PASS_BRIEF.md` §1. They must also say plainly that nothing is validated by human subject-matter experts yet.

## Step 3: run the release gate

Write `docs/release/2.0.0-rc.1/GATE_REPORT.md`. For each item in §5 of the build plan, give:

- **Result:** pass, fail or conditional.
- **Evidence:** the command run and its output summary, using generated numbers.
- **What is missing**, if anything.

Item 7 needs WP-15 sign-off on every external claim, plus the accessibility conformance report (ACR) and the security packet. For it:

- Report the state of `docs/methods/WP15_SIGNOFF.md` and the claims register after the fix passes.
- Treat the adoption-steward co-sign as a separate sign-off. You may not provide it yourself.
- List the moving facts and their re-check dates.

CI must be green: run the validator in normal and `--strict` modes, the indicator lint, all tests, and the Tribal-hold, personal-data, computed-field and v1-completeness checks.

## Rules

- **Lanes.** You may edit `vocab/`, `schema/`, `scripts/`, `data/v2/`, `pipelines/`, `site/` (only as Step 2 needs), `docs/decisions/` and `docs/release/`. Do not edit the report, briefs or deck in `docs/package/`. If a package file must change, note it for the orchestrator.
- **Tribal hold and personal data.** The Tribal hold stays in force, and no personal data goes in.
- **Agent ratings.** Agent ratings stay `raterType: llm`. Never present them as agreement among subject-matter experts.
- **Commits.** Never run `git commit` or `git tag`; the orchestrator commits and tags.
- **Restarts.** Write progressively, because container restarts happen. Keep `docs/build/WP-16/WORKLOG.md`.
- **Refused writes.** If the harness refuses a write, do not work around it. Put the text in your final reply.

## Final reply (up to 300 words)

- The gate result for each item.
- The generated headline counts.
- What fails and why.
- Decisions the project lead must make.
- Anything the orchestrator must change in the package.
