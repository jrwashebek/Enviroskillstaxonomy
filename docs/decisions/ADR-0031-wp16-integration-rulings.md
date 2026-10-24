# ADR-0031: WP-16 integration rulings, publication scope and the 2.0.0-rc.1 build

- **Decision point:** DP-30 (new; CA as WP-16 integrator, holding the DE code for the build)
- **Status:** accepted
- **Date:** 2026-10-23 · **Decider:** CA (an AI agent role, not a person)
- **Rules on:** pending items P-01, P-02 and P-03; change requests CR-FIX-A-001, -002, -003, CR-FIX-B-001, -002, -003 and CR-FIX-C-001; the orchestrator's package re-check items N1, N2, N12 and N13 (`docs/review/package_recheck.md` §5) and its two claims-register edits; the open items of the S2 close-outs.
- **Inputs:** `docs/decisions/integration/WP16_BRIEF.md`; build plan §1, WP-16 and §5; SPEC §10.5, §12, §16, §18; ADR-0003, -0007, -0010, -0013, -0024, -0027, -0029, -0030; `DECISION_LOG.csv`; `PROJECT_LEAD_DECISIONS.md`; the S2 close-out worklogs; fix logs A, B and C.
- **Amends:** ADR-0014 (WF-10 wording, recorded below), ADR-0027 (CR-FIX-A-001), the computed-view rules (`vocab/rules/`), `candidate_disposition.csv` (three rows), `docs/methods/claims_register.csv` (four rows), `vocab/scenarios.yaml` (three strings).
- **Implementation:** `docs/build/WP-16/` (worklog, data-edit scripts and their generated tables); `scripts/` (validator, release build, minting, migration, view rules); `pipelines/views/`; `site/` (only what minting and N2 needed).
- **Decision rule applied throughout (brief):** where the evidence or the rules do not settle a question, hide rather than show, and defer rather than invent.

## Context

S1 and S2 authoring and three package fix passes are finished. Every record in `data/v2` was still `status: draft` with a `seed:` key, so the `release` profile of `scripts/build_release.py` would publish nothing. WP-16 must decide the open items, mint persistent IDs for what rc.1 publishes, build `2.0.0-rc.1` twice byte for byte, and report the §5 release gate honestly. All counts below were produced by the build or by the scripts named; none is typed from memory.

## Decision

### 1. P-01: activate display-gate 1.1.0 (IO's implementation, CR-CP-001 B4)

- **Accepted with one change.** `display-gate@1.1.0` is `active`; `display-gate@1.0.0` is `superseded` (kept for reproducibility).
- IO's judgment calls:
  - **(a) accepted.** A job-analysis value that a person has reviewed renders with the `editorial` marker and its review status in the label. No new decision value is added.
  - **(b) narrowed.** IO's parameters let editorial design values (bundle membership, role levels, formation flags, target levels) show in *develop* views once a `pid:` reviewer has reviewed them. ADR-0024 §3 requires Delphi level placement for develop use, and the rule's own `editorial_rule` says "at describe tier only". So the CA does **not** ratify the develop branch: editorial design values render at describe tier until they are `panel-retained`. This has no effect at rc.1, because no record has a `pid:` reviewer. IO must align `validation/display_gates.yaml#role_profile_values.editorial_design_values.reviewed.view_tiers` before the first human review is recorded. That file is outside the WP-16 lane.
  - **(c) accepted.** View 2 (gap check) shows unreviewed target levels only in describe-tier views.
- **DE follow-up, done.** `scripts/rules/gated_values.py#role_profile_rows` calls `decide()` for every released RoleProfile field in five contexts (role, gap-check, federal-series-profile, state-class-view, select). The release view `views/display_gate.json` is now stamped 1.1.0. Fix-C's footer note about the 1.0.0 stamp (CR-FIX-C-001 item 4) is resolved.

### 2. P-02: activate the six HR and mobility view rules

- **Accepted with changes.** `federal-series-profile`, `state-class-view`, `job-family-membership`, `role-change`, `mirror-links` and `pathway-edges` (all 0.1.0) are `active`. Each `implementation` now names its module in `scripts/rules/`.
- Changes needed by minting:
  - the FSP and SCV ports find variants by `variantOf` and `sectorActor` (`hr_common.variant_for`), never by a seed-key suffix;
  - role-change view files are named by ID stem;
  - the job-family rule's family and anchor keys are re-pointed to minted IDs (changeNote in the rule file).
- The release ports read released records only (ADR-0030 rule 6). The WP-08 generators in `pipelines/views/` stay authoring previews.

### 3. P-03: test-fixture duplication

- **Decided: keep both, with one canonical copy.** `tests/` (and `pipelines/views/tests/`) are canonical, because CI runs them.
- The copies under `docs/build/` stay as frozen build history (ADR-0030 §5). CI never reads them, and fixture changes go to `tests/` only.
- Nothing is deleted, the conservative choice.

### 4. Change requests

| CR | Ruling | Effect |
|---|---|---|
| CR-FIX-A-001 | **accept** | ADR-0027 is amended, as the amendment below records. The career-ladder hypothesis may be published as a finding only after **named human reviewers** have validated it, in addition to the IO and LM agent reviews: a qualified industrial-organizational psychologist and a labor economist. It is then co-published with a nonpartisan partner. The report's §5 sentence must change; that is a package edit for the orchestrator. |
| CR-FIX-A-002 | **accept with change** | The eight Fix-A sources are registered under their placeholder IDs FIXA-01…08 in a CA-lane list, `docs/decisions/integration/sources.csv`. The validator reads every `docs/**/sources.csv`, so the register rows and the two new events resolve now. LM may re-home them in `docs/methods/sources.csv` with LM IDs at the WP-15 re-check. |
| CR-FIX-A-003 | **accept with changes** | (1) The OpenLMP monitoring signal is renamed "Components typed as monitoring …". Its method and note give the document-type sensitivity (plans only: intervals overlap), and `directionConfidence` is now low. (2) Every OpenLMP signal's `ci95` is the plan-level percentile bootstrap from Fix-A's seeded build (10,000 resamples, seed 20261023; F05 and F06). LM must port both fixes to `docs/methods/scripts/wp10_*.py` (LM lane) before any re-run. (3) The OMB method string now reads "eleven environmental units (nine agencies and bureaus and two USDA mission areas …)". (4) Two DriverEvents were added: the AmeriCorps reinstatement-eligibility notices (July 2025) and the NJ Supreme Court certification (July 2026). The day of each event is not recorded, so both carry evidence label J; views suppress J dates (REG-08). The orchestrator should remove the two hard-coded F09 rows from `build_figures.py`. (5) BLS signals now cite LM-132, and the Colorado events and instruments cite LM-117 and LM-155. (6) The field-craft research text is FC's lane and goes to the orchestrator. |
| CR-FIX-B-001 / **N1** | **accept** | The WP-08 FSP and SCV generators (and the change views) route every bundle value through `decide_role_value`. They print the gate labels in place of % time, importance, critical, needed-at-entry and distinguishing values, and they order by record order. The PD test now asserts the display rule. A new test asserts that no generated FSP or SCV file shows a % value or a critical or needed-at-entry flag. The generated files do **not** ship in the release bundle: the bundle carries the release-port views `views/federal_series_profiles/` and `views/state_class_views/`, which already applied the gate. Package README:36–37 must say so (orchestrator). The British spelling "modelled" in data labels is deferred to an rc.2 style pass, because rewording task text stales every text-hash-pinned rating. |
| CR-FIX-B-002 | **accept with changes; project-lead decision** | (1) The commitment is about 0.1 FTE over the ten months from kickoff (March 2027) to the end of embedding (December 2027). January and February 2028 are close-out only: an interview and the evidence pack, as the timeline in design §8 already shows. (2) "What participating organizations receive" lists only what design §6 and MOU Article 3 already provide: the release and kits free of charge, a coordinator, office hours, kickoff travel for small organizations, cohort calls, peer pairs, a request-a-role route, a stipend if funded, aggregate findings shared before publication, and ownership of their own artifacts. The review's suggestion of role profiles fitted to each organization is **not** added: it is a new service commitment with cost and selection-misuse risk, so it is for the project lead. AS applies the text in `docs/adoption/`, and the WP-14 owner updates deck slides 17–18. |
| CR-FIX-B-003 | **defer** | Register rows for the 0460 education requirement, the EXPLORE Act amendment citation, the Public Lands Corps authority and SME-QA / USA Hire need primary-source reading (LM with FH) at the WP-15 rc.1 re-check. Until then the softened package text stands and nothing is invented. N12 is handled separately (§8). |
| CR-FIX-C-001 | **item by item** | (1a) Re-grading reliability from the underlying sources is **deferred** to LM at the WP-15 re-check, and the explorer keeps its "not yet re-graded" label. (1b) An agency or series scope field is **deferred** to a schema MINOR in rc.2. (2) **Accepted and applied:** role-attached signal titles use the role's title; `weak_signals.csv` source paths become the source's own title; signpost titles name the axis or scenarios; X11 comments use plain words (TSV and generator). The series-register note is now plain in the WP-08 view; the data note is an editorialNote, which the build strips. (3) **Accepted and applied** (also N13): "informed buyers" and "informed-buyer capacity". (4) **Done** under §1. (5) **Decided: strict enforcement.** PLAN-01 is single-quoted, as the orchestrator asked. The two unrelated uses (the SL-C02 permit statement and its indicator; the DC-19 model-tier task) were reworded to "monitoring terms" and "the monitoring the tier requires", with no change of meaning, so the phrase renders nowhere. The context-pattern alternative is rejected: it would leave the wrong form free to re-enter elsewhere. (6) **RPT-05 stays the enforcing row**; WF-02 is not quoted, because quoting '16%' would pair it with WF-02's own percentages and raise false positives. (7) **Accepted with change:** the schema requires a numeric `measure.value`, so the NPS and USFS headcount values stay −0.25. They are relabelled as a bound (`headcount_change_share_bound`; unit "share, as a bound: the loss is more than a quarter (PPS gives no exact figure)"). |

**Orchestrator register edits (applied).** RPT-27 status changes from `verified` to `derived`. In OMB-02 and RPT-04, "(nine bureaus and two USDA mission areas" becomes "(nine agencies and bureaus and two USDA mission areas". PLAN-01 and OMB-02 `do_not_say` now single-quote 'monitoring requirements' and 'nine environmental bureaus'. Their notes no longer say they are deferred.

### 5. Open items from the S2 close-outs

1. **WF-10, "NWCG is not a party".** The credential record `wildland-fire-position-qualification` already carries the WF-10 wording (fixed by S2 close-out B). Its frozen builder `docs/build/WP-07/scripts/build_wp07_credentials.py` still has the wrong form. That file is outside the WP-16 lane and must never be re-run (ADR-0030 §5), so it goes to the orchestrator. The wrong form also remains in `docs/adoption/stage1b_design_partner_packages.md`, `docs/adoption/ecosystem_atlas.csv` and its builder (AS lane), and in ADR-0014's corrected-facts table. The ADR-0014 table is amended below.
2. **Instruments to register.** Only what existing verified records support was registered:
   - `seed:ins/ada-title-ii`, with its 2026-04-20 interim-final-rule event (key fact V2-11 and register CMP-01, verified; CP-012), linked as `requires` on the local enactment of v1 5.3.4-A;
   - `seed:ins/chance-to-compete-act` (FH-001, FH-017; key facts V1-09 and V1-17), with no event, so its status is "not recorded", linked as `requires` on FH-C13's federal enactment.
   - Sections 504 and 508 of the Rehabilitation Act, the ABA standards and EO 13166 with its revocation stay **watch items**: no verified record supports them, and CMP-03's Section 508 point is J. v1 5.3.4-A's federal value therefore stays "basis not yet linked".
3. **Role targets (R13, R26 and the rest of the work orders' `needed_by`).** 47 competency targets were added from `s2_work_orders.csv`, including nine on R13 and SL-C03 on R26. The rule is mechanical and editorial: the target level is the role level's band minimum, clamped to the competency's span. Only target levels were added. No importance, task-bundle or selection value was invented, because those are job-analysis values. Every target renders "editorial draft". The list is in `docs/build/WP-16/generated/role_target_additions.csv`.
4. **`docs/build/WP-07/PATHWAYS.md` is stale.** It is in a frozen builder's lane. rc.1 ships a generated listing of the released pathways at `docs/release/2.0.0-rc.1/PATHWAYS.md`, and the orchestrator should add a one-line pointer to it in the stale file.
5. **`validate_v2.py --strict`: 31 dangling-reference errors.**
   - All 31 named planned targets that are held (TN-C01/02/07/10/11), deferred to wave 2 or 3 (PS-C06, PS-C08, PS-C21, v1 4.5.3-B) or unauthored (FC-C13).
   - Every reference came from records no release can carry: seed-keyed superseded stubs, seed-v1 module tasks and X1 rows.
   - **Ruling:** in release mode, a planned target is an error only when a releasable record names it, meaning a minted ID with a release status. Otherwise the validator reports `W-REF-DEFERRED`, or `W-X1-DEFERRED` for X1, which the build renders as `sssom:NoTermFound`. The release notes count the deferred targets by area.
   - Result: strict validation reports 0 errors.
6. **Disposition amendments assigned to "CA with DE, WP-16".** Applied in `candidate_disposition.csv`: DB-C56 (new module-v2.0 row for MOD-12, wave 1) and the DB-C53 and PS-C06 rationale extensions. `MIGRATION_INFO.json` was regenerated for the new input hash.
7. **Review debt (recorded, not self-reviewed).** The following reviews are owed by the named agent codes or by humans. None was done by the WP-16 agent.
   - **FC** field anchors: DB-C42, DB-C19, DB-C13, DB-C56.
   - **SC:** DB-C05; the FC content added to SL-C03.
   - **DC:** FS-C09; the laboratory-data review task in v1 2.2.3; the PS-C07 and PS-C09 requests, including the PS-C07 → SC-C15 mirror.
   - **DB:** PS-C15 module enactments (forest, water, parks), not yet written.
   - **Self-reviews to redo:** PS-C15's SC review was a self-review.
   - **Independent IO double-coding:** OBS-4 on every new indicator (all are self-coded 3).
   - **LM:** confirmation of the five role-attached watch signals; the unlisted independence keys `fs-fiscal` and `nifc-imsr`.
   - **TN:** the held parts of v1 5.3.1, 5.3.5 and 5.6.5.
8. **CA spot-check of federal venue values (S2 close-out A list), done on the rc.1 view.** No rescission is read as a basis, and there are 0 untyped links.
   - DB-C52 and v1 5.3.5 federal: `no-current-basis`. The rescinded EJ orders are their only federal basis. Their state values are `required-basis` from the New York and New Jersey laws.
   - SL-C02 and FH-C01 federal: `permitted`, basis linked but not yet verified.
   - SL-C08 and SC-C03 federal: `required-basis`. This rests on the DOI and USDA NEPA procedures (E events), together with the NEPA amendment, whose enactment day is J.
   - v1 5.3.4-A: federal "basis not yet linked"; local `required-basis` (ADA Title II).
   - v1 5.3.4-B federal: `required-basis` (OPM Merit Hiring Plan).
   - These values follow `venue-applicability@1.0.0`. The CA is checking that the rule was applied as written; this is not a content review.

### 6. Publication scope and minting (ADR-0010; SPEC §12.2)

- **What rc.1 publishes.** A record is promoted to `candidate` when every one of the following holds:
  - it is a draft with a seed key and is not an unauthored v1 seed;
  - it is not held under the Tribal hold;
  - no other gate rule excludes it (third-party index licence, quarantined or placeholder signal, organization measure with n < 5, withheld under §8);
  - it is in core, a register or a wave-1 module, or it is one of the early drafts the dispositions name for wave 2 (FH-C03 and role R19 in worklands; IA-CC-05 in extract);
  - every record it depends on is itself promoted.
- Ratings on records that are not released stay drafts. Agent ratings ship as data with `raterType: llm`, never as agreement; v1 values ship with `raterType: v1-analyst` as prior evidence only. The views gate both (SPEC §10.5 rule 7; display-gate `data_download`).
- **Minting.** `scripts/mint_id.py promote-batch` is the single writer. It ran once over `docs/build/WP-16/generated/promote_keys.txt` (generated by `select_promotions.py`; the summary is in `promotion_summary.csv`).
  - All IDs were drawn under one registry lock.
  - All references in `data/v2` were rewritten in one pass.
  - Every pair is in `data/v2/ids/seed_map.csv`.
  - Result: 10,472 records promoted and 10,472 registry rows; `mint_id.py verify` reports OK.
  - Held content was not promoted, so it got no public ID (ADR-0007 §D). Neither did withheld records.
  - `migrate_v1.py` now treats promoted seeds as authored and applies the recorded promotions to its generated outputs, so `--check` stays deterministic.
- **Release closure.** The build drops, and counts, every reference in a released record whose target is not in the release (held, withheld or not released). Its self-check fails on any whole-string `seed:` reference in the bundle or on any withheld key.
- **Judgment edges.** 29 J-labelled sensitivity edges had no `reviewBy`, which is an error at `candidate`. They now carry `reviewBy: 2027-01-31`, the date SC used for its reviewed task edges, so each is re-checked before 2.0.0.

### 7. Wrong forms in data (brief Step 1.4)

- "Monitoring requirements" (PLAN-01) was removed from the OpenLMP signal and from the two unrelated records (§4, CR-FIX-C-001 item 5). "Nine environmental bureaus" (OMB-02) was removed from the nine OMB signals.
- Both `do_not_say` entries are now single-quoted.
- The explorer check enforces them on the rc.1 build: 0 problems, and no page carries either phrase.

### 8. Package re-check items N1, N2, N12, N13 and the withheld list

- **N1:** §4, CR-FIX-B-001.
- **N2: withhold, at the source.** WP-15 §2.1 forbids publishing unverified claims, and the WP-15 acceptance requires zero unverified claims in released artifacts. The CA therefore withholds from every release artifact the records whose claim rests on an `unverified` register row whose record carries the claim in its name or its dated events:
  - NEPA-09; ESA-02; ESA-03; CWA-02; DISC-03; REG-01 to REG-07, including the REG-06 instrument and its two signals.
  - That is 13 instruments, their events and 2 signals, listed in `data/v2/governance/release_withheld.yaml`.
  - These records stay drafts with seed keys. Links to them are removed from released enactments and variants. Some were `requires` links (the DOT and EPA NEPA procedures, the SEC rules, Texas HB 3923), so no venue value now rests on an unverified event.
  - REG-08 (J-dated days) and REG-09 (base instruments without events) are **not** withheld: the bundle states the J label, and no status is asserted.
  - The explorer counts the withheld instruments with their register rows. Its checker fails if a withheld record enters the release (E1w) or if any of a row's `withheld_phrases` renders (E2w).
  - `grep -rl "IRA conservation" site/_site` returns no files.
  - A row returns to the release when LM re-verifies it and the CA removes it from the file.
- **N12:** the instrument's label is now "Good Neighbor Authority" and its citation 16 U.S.C. 2113a. The EXPLORE Act event keeps its J-labelled day, which views suppress. The PD's `plain_instrument()` treatment is now unnecessary but harmless.
- **N13:** §4, CR-FIX-C-001 item 3.

### 9. The release build

- **Version** `2.0.0-rc.1`, profile `release`. The **date** comes from the records (latest `generatedAt`, 2026-10-23). No wall clock is used.
- **Counts.** The counts come from `counts@1.1.0`, a new rule version that supersedes 1.0.0 and adds:
  - competencies by module × kind and by lifecycle;
  - roles by tier and variants by sector actor;
  - held records as a count;
  - removed references and deferred targets.
- **Release notes** are generated by the build, and `scripts/release_docs.py` copies them into `docs/release/2.0.0-rc.1/`. They open with the authorship statement from `FIX_PASS_BRIEF.md` §1, adapted to the release, and say plainly that nothing has been validated by human subject-matter experts.
- **Delta.** `delta.json` is computed against no previous release, so every ID is added. `delta_v1.json` is computed against the v1 baseline. v1 had no persistent IDs, so every ID is added; for each v1 competency and task it gives the X1 decision and the rc.1 successors. Successors not in the release (held, deferred or withheld) are counted, never named.
- **Determinism.** Two consecutive builds must be byte-identical. The gate report gives the result.
- **Human-readable copies.** `scripts/release_docs.py` copies the notes, counts and v1 delta into `docs/release/2.0.0-rc.1/`. It also generates `PATHWAYS.md` and `BUILD.md` there. `--check` fails when they are stale.
- **Faults found while gating, and fixed.**
  - **SCV file names.** The release-port State Class View files were named `unknown--<code>`. The jurisdiction now comes from the `class-<JUR>` notation scheme, which gives the same stems as WP-08, and a test asserts it.
  - **Browser-check sample.** The sample's fixed pages were named by seed-key slugs, so after minting the run silently checked 52 pages instead of 71. They now resolve through the seed map, and the run is back to 71 pages.
  - **Tests.** Four tests encoded pre-mint state, and three acceptance tests had started skipping. All were updated to resolve through the seed map and to assert the post-mint rules.
- **Indicator lint (for IO; `validation/` is outside the WP-16 lane).** The standalone whole-tree report reads every CSV row and every typeless YAML document under `data/v2` as an Indicator, so it reports thousands of "required metadata missing" hits on non-indicator files. Those files are `ids/`, `migration/`, crosswalks and governance. The migration, crosswalk and governance hits pre-date WP-16; minting added the `ids/` files. On released records the linter reports 0 failing in release mode. IO should make the loader skip `ids/` and `migration/` and require `type`.

### 10. Gate posture and decisions for the project lead

The gate report (`docs/release/2.0.0-rc.1/GATE_REPORT.md`) gives each §5 item with its evidence. The CA's posture:
- rc.1 may be built and tagged as an honest **release candidate for the NGO-pilot preview and the design partners**;
- it is **not cleared for external publication**. Item 7 fails today: AS has not co-signed WP-15, and the moving facts have re-check dates after today.

Decisions only the project lead can make:
- the CR-FIX-A-001 publication rule (adopted here as CA governance text, but it binds the lead's publications);
- whether fitted role profiles are part of the pilot offer (CR-FIX-B-002), together with a reply-by date and eligibility;
- the AS co-signature path for WP-15 (§5 item 7), plus Q3, Q4, Q6 and Q8–Q11, which are still open with their defaults;
- whether the CTA should move to an organization account (package re-check NH11).

## Rationale

- **Mint what is authored and closed, nothing else.** IDs are permanent: a minted ID is never reused or re-pointed. Minting unauthored seeds, held drafts or records with unverified claims would publish identities the project might have to withdraw. Promoting only authored records whose dependencies are also promoted makes rc.1 referentially closed by construction.
- **Withhold at the source, not in the page (N2).** The explorer's label does not stop a CC0 bundle from carrying the claim. Withholding the record keeps every consumer correct: bundle, CSV, SKOS, views and explorer. It also stops an unverified event from deciding a venue value.
- **Deferred references are warnings only where no release can carry them.** Strict mode exists to protect what is released. Treating a seed-keyed stub's pointer to a held successor as a release error would force either authoring held content, which ADR-0007 forbids, or deleting lineage, which the SPEC forbids.
- **Editorial target levels by a published rule.** The work orders said which roles each new competency was written for. Adding only target levels, by a transparent rule and labelled as editorial drafts, completes those orders without inventing a job-analysis value.

## Consequences

- SPEC, schema and vocabularies are unchanged in meaning. The rule files are updated (display-gate 1.1.0 active; six HR rules active; counts 1.1.0). `vocab/scenarios.yaml` has three wording changes.
- 10,472 records are now `candidate` with persistent IDs. From here on, authoring agents edit minted records and may not create new `seed:` references to them; the seed map resolves old keys.
- Before any re-run, the authoring builders that still write seed keys need porting through `data/v2/ids/seed_map.csv`. They are LM's WP-10 builder, the frozen S1 builders, the crosswalk pipelines (`pipelines/crosswalks/`, `pipelines/x2/`) and the WP-08 change-atom inputs. This is an rc.2 item; the WP-08 view generators already resolve seed keys.
- The explorer now builds from the rc.1 release bundle. It still reads HR views from the WP-08 generators (now gated), not from the release-port views; switching it is an rc.2 item (ADR-0030 §6).

## Dissent and trade-offs

- **IO (simulated):** narrowing call (b) means a reviewed target level cannot reach a develop view without a Delphi. The cost is accepted: develop use needs placement evidence (ADR-0024 §3).
- **LM:** withholding 13 instruments thins the What's coming view and some venue links until the WP-15 re-check. The alternative, labelled but published, would ship unverified claims in CC0 data.
- **SC:** "monitoring terms" is less idiomatic than the permit term of art "monitoring requirements". Accepted in exchange for a wrong form the checker can enforce everywhere.
- **FH:** job families now weight targets equally, so R13 and R35 fall out of every family until importance is confirmed by job analysis. That is the gate's `rollups` rule, applied.
- **Trade-off named:** a smaller, closed release, with some records withheld and some deferred, against a fuller release with more caveats. The smaller release is chosen.

## Amendments made by this ADR to earlier ADRs

- **ADR-0027 (CR-FIX-A-001).** The "Flagship report" bullet on the career-ladder hypothesis now reads: "the career-ladder finding is presented as a hypothesis with its mechanism and evidence status. It is published as a finding only after named human reviewers (a qualified industrial-organizational psychologist and a labor economist) validate it, in addition to the IO and LM agent reviews, and it is then co-published with a nonpartisan partner (P-AS-14)."
- **ADR-0014 (WF-10).** In the corrected-facts table, "NWCG is not a party" is replaced by "the alignment is between USWFS and USFS standards (the plan does not name NWCG)" (claims register WF-10).
