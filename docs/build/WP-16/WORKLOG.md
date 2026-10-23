# WP-16 worklog: integration and 2.0.0-rc.1

Agent: WP-16 integration agent, holding CA (decision authority) and DE (build).
Date: 2026-10-23. Brief: `docs/decisions/integration/WP16_BRIEF.md`.
Rules: no commits or tags; Tribal hold in force; no personal data; agent ratings stay raterType llm.

## Status

- [ ] Read-first set
- [ ] Step 1: decide and apply open items (ADR-0031, DECISION_LOG rows)
- [ ] Step 2: mint IDs, keep consumers in step, build rc.1 (byte-identical x2)
- [ ] Step 3: gate report

## Log

- Start. No prior WP-16 worklog; git tree clean at b7415c1 (Fix pass C).
- Read-first set done: CHARTER, TEAM_BRIEF, build plan (§1, WP-16, §5), SPEC §10.5/§12/§16/§18/§19, ADR-0003/0007/0010/0013/0024/0029/0030, DECISION_LOG, PROJECT_LEAD_DECISIONS (Q1, Q2 recorded), pending_for_CA_integration (P-01..03), all CR-FIX-* CRs, S2 close-out A/B worklogs, fix logs A/B/C, FIX_PASS_BRIEF, WP15_SIGNOFF. Note: the brief names `docs/decisions/integration/s1_integration_review.md`; only `s1_integration_review.py` and its outputs exist (ADR-0030 §3 is the review text).
- **Baseline (before any WP-16 change):** `validate_v2.py` 0 errors, 156 warnings; `--strict` 31 errors (all E-REF-DANGLING: held successors TN-C01/C02/C07/C10/C11, FC-C13, wave-3 PS-C06/C08/C21, wave-2 v1-4.5.3-B; referenced only from seed-keyed superseded stubs, seed-v1 module tasks and X1 rows); `build_schema --check` current; `extract_v1 --check` current; `migrate_v1 --check` OK; README status block stale; registry empty (0 IDs minted); 12,224 records, 122 held.
- Census: every record is `status: draft` (or superseded/withdrawn seed-v1 stubs). The release profile excludes drafts and unminted records, so rc.1 needs promotion to `candidate` with minted IDs.
- **Orchestrator additions (package re-check, docs/review/package_recheck.md §5), added to WP-16 scope, each to be ruled in ADR-0031:**
  - N1 (must-fix; = CR-FIX-B-001): gate time shares and critical/entry flags in the WP-08 FSP/SCV generators (md + json), regenerate, test asserts absence. Fallback: exclude from rc.1 and tell the orchestrator (package README:36-37).
  - N2 (must-fix): explorer renders the unverified REG-06 headline "Rescission of unobligated IRA conservation and staffing funds (P.L. 119-21)" as an instrument title on 6 pages. Withhold instruments tied to unverified register rows (like signals) or fix the record; rebuild; `grep -rl "IRA conservation" site/_site` must be empty.
  - N12: "Good Neighbor Authority incl. EXPLORE Act amendments" on 16 explorer pages: apply plain_instrument() treatment or register the citation.
  - N13: vocab/scenarios.yaml "intelligent customers"/"intelligent-customer capacity" -> "informed buyers"/"informed-buyer capacity".
  - Do not touch docs/package.
- **Orchestrator addition (register edits, to avoid collision):** RPT-27 status verified -> derived; OMB-02 and RPT-04 "(nine bureaus and two USDA mission areas" -> "(nine agencies and bureaus and two USDA mission areas". Data text for the OMB method string will use the same wording.
