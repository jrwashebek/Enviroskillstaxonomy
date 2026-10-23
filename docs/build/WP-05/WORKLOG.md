# WP-05 worklog: Statecraft and the regulatory core (A5 SC; SL reviews state enactments)

Started 2026-10-23T13:44Z. Agent `emstagent:a5-sc@wp-05` (model claude-opus-5-5); SL review pass recorded as `emstagent:a5-sl-review@wp-05` (A5 carries SL as its junior review code, build plan §2). Prompt version `wp05-sc-authoring@1`.

All counts are generated in `generated/wp05_counts.json` and `generated/wp05_written.json`. Run `gen_counts.py`; never type counts by hand.

## What was authored (all `status: draft`, `validationStatus: draft`, `reviewStatus: unreviewed`, CC0-1.0)

**WP-05 list, complete**
- **Review:** SL-C08, SC-C03, SC-C04, SC-C09, DB-C50, DB-C52, FH-C01.
- **Authorization:** SL-C02 (enactments for the regulator variant at state, federal and local level, and for the resource-manager variant at federal and state level), SC-C01, SC-C14, v1 5.5.2.
- **Inspection and enforcement:** SL-C03, SL-C04, SL-C10, DB-C25 (lifecycle emerging, reviewBy 2027-10-23), DB-C26.
- **Rules and resources:** SC-C10, SC-C11, SC-C12, SC-C16, SC-C17, SC-C18, v1 6.4.5. v1 6.4.3 is delivered through its merge target v1 6.3.4, which WP-05 rewrote; WP-04 (DC) is asked to co-review because DC is the defining craft of most of its tasks.
- **Agreements:** SC-C08, v1 3.1.4 (absorbs 3.3.4).
- **TX-B:** v1 7.1.2, v1 7.1.3, PS-C18, SL-C16.

**Further SC-lane core rows needed by COR-3 P1 roles, or targeted by other lanes' tasks**
- SC-C02 (receives the record half of v1 6.4.4; SC-C05's legal-adequacy anchors are indicators here).
- SC-C07, SC-C06, SC-C15 (absorbs v1 3.6.2).
- v1 6.1.1 (absorbs 6.4.1), v1 6.2.3, SL-C12.
- v1 5.2.1 (absorbs 3.6.3), 5.2.2, 5.2.3, 5.2.4 (absorbs 5.5.3), 5.2.5.

**Every competency has:**
- 2–5 indicators at each published level, carrying `augmentationMode`, `assessmentMethods`, `useClass: develop`, `obs4` and `distinguishingAttribute` above the lowest level. An evidence plan is attached wherever obs4 = 2.
- At least 4 primary tasks.
- Mechanism sensitivity edges (`instrumentSensitivity`).
- Structured actor enactments where the actor changes the performance. These record authority basis, principal and accountability venue; delegated constraints are written inside `authorityBasis`; enactments carry `authorityPosition` and registered L5 instrument IDs.

**Other changes to v1 seeds**
- v1 seeds were edited in place: ids, facets and lineage kept, `carried` switched to `rewritten`, and `v1Seed` dropped.
- Split-source tasks were re-pointed: 6.1.2 to SL-C03 and DB-C26; 6.1.3 to SC-C01; 6.1.4 to SL-C08; 6.5.2 to SC-C09; 6.4.4 T3 to SC-C02.
- **For CA:** 6.4.4 T1 (design the input process) was re-pointed to **SC-C06**, which is not one of the 6.4.4 split targets listed in the disposition. CA to confirm or move it to SC-C02.
- X1 was regenerated with `scripts/migrate_v1.py --x1-only`; there was no diff.

**Craft ratings:** three LLM passes (`data/v2/assessments/emst-craft@0.1/wp05-sc-pass{1,2,3}.jsonl`), coded from task text only, each in its own random order.
- Same model and session as the author, so the passes are not blind to the authoring context.
- `raterType: llm`, `evidenceLabel: S`, IO LLM-coder gate level G0.
- Run-to-run consistency is in `generated/craft_run_consistency.json`. It is not reliability.
- Split units are in `generated/craft_split_units.csv`. SC splits cluster on advice, pathway-mapping and coordination tasks, where the codebook's commitment test is hard to apply. IO may want a decision rule for these.

## Sensitivity edges, instruments, venue applicability, mirror links
- **Task-level edges:** the schema has no Task field for them, so they are generated in `generated/task_sensitivity_edges.csv` (`gen_edges.py`) as inherited drafts with a review-by date. See CR-SC-001.
- **Instruments:** registered `seed:ins/*` IDs are linked from enactments. Instruments the registry still lacks are listed with citation hints and proposed IDs in `instruments_to_register.csv` (for LM). Five rows were verified this session: the EJ executive orders and their 2025 revocations, NJ EJ law and rules, NY ECL 70-0118, and EO 14303 (`sources.csv` WP05-001..004).
- **Venue applicability (ADR-0016):** prototype in `ci/venue_applicability.py`, with synthetic fixtures that pass `validate_v2.py --data-root` and 6 passing tests in `ci/test_venue_applicability.py`. Live output is in `generated/venue_applicability.csv` and `generated/federal_applicability.json`.
  - These are computed fields, never stored in records.
  - DB-C52's federal and state values read `permitted` with `basisLinked = false` until LM registers the instruments above.
  - Known defect: removal or enabling instruments read as "required basis". CR-SC-001 item 2 fixes this.
- **Mirror links:** `mirror_links.csv`. Regulator and regulated-party pairs within one competency are actor enactments with opposite `authorityPosition`. Pairs across competencies (SL-C03/SL-C04/SL-C10/DB-C25 to DB-C26; SL-C02 to SC-C01; SC-C04 to the SL-C08 preparer enactment) have no schema field yet (CR-SC-001 item 3).

## SL review (junior-code pass on state and local enactments)
- Checked every state and local enactment against SL's 70-class sample and sources (SL-038 … SL-088). The citations match the claimed postings.
- Local-government enactments rest on SL's thin local sample (2 classes) and are labelled [J].
- Regions are under-covered: no Mountain West specs, and the Southeast is represented by Florida only.
- Water and wastewater operators and REHS are module content (WP-06) and are not authored here.
- SL-C12 (state revolving funds) is [J]: no source was retrieved this session.

## Holds and rules respected
- **SC-C13** is not authored. It is held and merged into TN-C02.
- **No Tribal enactment authored.** Reserved for TN under the hold:
  - SL-C08 and SC-C03 (Tribal environmental review codes);
  - DB-C50 (THPO coordination, TN-C11);
  - SL-C02 and SC-C14 (treatment-as-state programmes);
  - SC-C08 (agreements, TN-C04);
  - v1 7.1.2 (authority with standing);
  - v1 6.4.5 (Tribal council processes);
  - SC-C10 (self-governance funding, TN-C08);
  - SC-C18 (briefing Tribal councils);
  - v1 5.2.1 and 5.2.3 (G2G framing).
- `tribalRecordsAuthored` = 0 (generated).
- v1 task quotes that name held content are withheld from editorial notes.
- **No L1/L2 text names an L5 instrument.** Instruments appear only in enactments and in L5. Programme labels appear as `altLabel` only.
- **OPM ECQ (five-ECQ framework, Oct 2025):** no WP-05 competency uses or depends on the withdrawn names (political savvy, partnering, influencing/negotiating). X9 (WP-09) must map to the current five ECQs only.
- **Q4 default:** the mechanism is built and nothing is excluded.

## Open issues and CRs
- **CR-SC-001** (`docs/decisions/change_requests/CR-SC-001.md`):
  1. `Task.instrumentSensitivity`;
  2. instrument roles on `characteristicInstruments`;
  3. competency mirror links;
  4. port the venue rule to `vocab/rules/` and `build_release.py`;
  5. a `delegatedConstraints` field, or ratify the text convention.
- **LM (WP-10):** register the instruments in `instruments_to_register.csv`. Once IDs exist, WP-05 links them from the DB-C52, v1 7.1.3 and SL-C02 enactments.
- **WP-06:** the v1 6.7.5 tasks (air monitoring, planning, health) still point at the superseded 6.7.5 seed in core. Their successors are module competencies (DB-C13, DB-C14). The SL-C02 air-permitting part is covered by the SL-C02 local and state regulator enactments.
- **WP-04:** owns the SC enactment of AI-output validation (seed:v1-7.1.4-A). SC-C05's legal-adequacy anchors are also carried as SC-C02 indicators.
- **Not authored (rest of the SC lane by v1 craft):**
  - v1 3.1.5, 3.2.4, 3.2.5, 3.3.1, 3.3.5, 5.1.1, 5.1.3, 5.3.1, 5.3.5, 5.4.1, 5.4.3, 5.5.4, 5.6.1, 5.6.4, 5.6.5, 6.2.5;
  - candidates DB-C05, DB-C42, FH-C13, FH-C14, CC-CM-02, PS-C15, FS-C09, FS-C15.
  - Several of these are general management or communication, which P-SC-07 says should not be Statecraft. CA to reassign or confirm.
- **Not WP-05's:** repository tests failing at hand-back (`tests/test_migration.py`, `test_schema_build.py`, `test_build_release.py`) come from other lanes' in-progress edits and the pending DE schema regeneration (RULINGS_FOR_DE). `validate_v2.py` shows 0 errors in WP-05 files.

## For WP-08 (role profiles) and WP-12 (explorer)
- **COR-3 P1 roles:**
  - R10: SL-C08, SC-C03, SC-C04, SC-C09, SC-C02, SC-C17, DB-C50, DB-C52, FH-C01, SC-C06.
  - R11: SL-C02, SC-C01, SC-C16, SC-C07, SC-C14.
  - R12: SL-C03, SL-C04, SL-C10, DB-C25.
  - R13: SC-C10, SC-C11, SC-C12, SC-C18, v1 6.4.5, SC-C08, v1 6.2.3, v1 3.1.4.
  - TX-B applies to all roles.
- **Variants:** `authorityPosition` on the actor enactments matches the variants WP-08 needs. SL-C02 has regulator enactments (state, federal, local) and resource-manager enactments (federal and state land; useful for R18).
- **Mirror pair R11/R12 to R37:** see `mirror_links.csv`.
- **Explorer:**
  - `federalApplicability` must be read from the computed view, never from records.
  - Show "basis not yet linked" when `basisLinked = false`.
  - Never render the LLM craft passes (G0).
  - 9 indicators have obs4 = 2 with evidence plans.
