# Package fix pass — shared brief (2026-10-23)

Two independent reviews of the sector-facing package are in:

- `docs/review/package_review.md`: a cold read of the whole package. It found 39 issues, 12 of them must-fix.
- `docs/review/evidence_review.md`: a red team on the flagship report. It checked 99 claims, found 23 problems and gives a 16-item must-fix list in §7.

`docs/methods/WP15_report_corrections.md` also lists the corrections the WP-15 sign-off already required. This pass applies all of them. You are an editor: fix what the reviews say, and do not add new claims. Where a review gives the corrected fact and its source, use that and cite it. Where it does not, soften the claim or remove it rather than inventing a fact.

## Read first

1. `CHARTER.md` and `TEAM_BRIEF.md`, for the evidence labels and the simulated-voice rule.
2. The two reviews, in full, and `docs/methods/WP15_report_corrections.md`.
3. `docs/methods/claims_register.csv`. Its `do_not_say` column is binding.
4. `docs/research/_verification/CORRECTIONS_REGISTER.csv` and `ALL_key_facts.csv`. Use only the corrected facts.
5. `validation/display_gates.yaml` (rule 1.1.0) and `validation/display_gate.py`.

## Decisions that bind every file

These are orchestrator decisions and apply to every file in the package.

### 1. Authorship (package must-fix 3)

Use this statement, or a faithful shortening of it, in every document's front matter or colophon:

> This package was researched and drafted by a team of AI agents (Anthropic's Claude), each given a specialist role,
> working to a charter set by the EMST project lead. AI agents checked the facts against sources in October 2026. No
> independent human expert has reviewed the package yet. Role names such as "Chief Taxonomy Architect" are AI agent
> roles, not people.

Never write as if a human panel, SME or practitioner agreed. Never attribute a view to a Tribal nation, a practitioner or an organization.

### 2. Status line (package must-fix 2; evidence must-fix 1)

Replace every "verified" or "cleared" status line with this, adapted per file:

> **Status: draft for NGO-pilot preview (2026-10-23).** AI agents checked facts against sources; 13 references were
> read but not re-verified, and some claims await register rows. Not yet reviewed by independent human experts.
> Date-sensitive statements will be re-checked before external release.

Do not use the words "verified", "validated" or "cleared" for the package as a whole.

### 3. The display rule (package must-fix 1)

Under display-gate 1.1.0, the following never appear in sector-facing text:

- agent-drafted time shares;
- importance or critical/needed-at-entry flags;
- target proficiency levels presented as findings;
- LLM craft ratings;
- any value with α < .667.

You may describe a role's work in words and say which crafts it draws on, using the craft definitions. You may not give numbers or flags.

### 4. Agent drafts are not findings (package must-fix 4; evidence §4.3)

Use hypothesis or judgment verbs, such as "we expect", "the evidence suggests" or "an agent-assessed judgment", wherever the claim rests on agent work. Keep the E/J/S labels where the file already uses them.

### 5. No implied participants (package must-fix 11)

Do not present organizations, jurisdictions or programmes as participating, partnering, piloting or committed. They may appear as examples, as context or as "potential" partners. The commitment register is empty.

### 6. Readable to outsiders (package must-fix 6)

Remove internal IDs and acronyms from reader-facing text. This covers seed IDs, R01/COR-1, WP-nn, CA/DE/IO role codes and L1–L5 without explanation. Either spell things out or move them to a short technical note at the end. Keep numbered citations.

### 7. Call to action (package must-fix 8)

Wherever a contact or next step is needed, use the literal placeholder `{{EMST_CONTACT}}`. Write it once per document, in a sentence such as: "To comment, correct an error or ask about the pilot: {{EMST_CONTACT}}." The orchestrator will fill it in. Every CTA must lead to that placeholder. Never invent an email address or URL.

### 8. Facts the reviews corrected

Use these in every file where the topic appears:

- **AmeriCorps.** Add the July 2025 reinstatement-eligibility notices to non-plaintiff grantees. Remove "terminations persisted elsewhere" and "reinstated only in plaintiff states". Keep the settlement nuance from package must-fix 12.
- **Self-assessment questionnaire rule.** Always give its exceptions (seasonal work, GS-4 and below) and the FY2028 target (package must-fix 7; evidence item 10).
- **New Jersey EJ rules.** The NJ Supreme Court granted certification in July 2026, and the rules stay in effect pending its decision.
- **Pennsylvania equivalency.** Follow register row STATE-PA-02; do not state it as a general rule.
- **"Budgets."** Do not name budgets as a cause of the contraction (package must-fix 5). FY2026 appropriations were near flat.
- **Drones.** Follow the corrected field-craft drone wording in the claims register.
- **Scope.** Write "federal", not "public", where the evidence is federal. Scope entry-job and field-craft claims to federal land agencies, and plan-monitoring claims to western national forests.

## Lanes

| Agent | Files it may edit |
|---|---|
| Fix-A (report) | `docs/package/report/**` (report, `figures/build_figures.py` and its outputs, `claims_used.csv`) and `docs/methods/claims_register.csv` |
| Fix-B (briefs) | `docs/package/briefs/**`, `docs/package/deck/**`, `docs/package/README.md` and `pipelines/views/forester_pd_fes.py` (then regenerate `docs/package/forester_pd_fes_draft.md` with `pipelines/views/build_views.sh` and keep `pipelines/views/tests` passing) |
| Fix-C (explorer) | `site/**` only |

Nobody edits `data/v2`, `vocab`, `schema`, `scripts`, `legacy`, ADRs or SPEC. If a fix needs a change outside your lane, write `docs/decisions/change_requests/CR-FIX-<A|B|C>-NNN.md`.

Never `git commit`; the orchestrator commits. If the harness refuses a write, do not rename the file or work around the refusal. Put the full text in your final reply after `# FULL TEXT OF <path>`.

## Worklog and final reply

Keep a worklog at `docs/review/fixlog_<A|B|C>.md`. It is a table: issue ID (PKG-n / EVD-n / WP15-Cnnn), file, what changed, and status (fixed / softened / deferred + reason).

Your final reply is at most 250 words. Give counts of issues fixed, softened and deferred (generated from your worklog), anything deferred, any CRs, and anything the orchestrator must decide.
