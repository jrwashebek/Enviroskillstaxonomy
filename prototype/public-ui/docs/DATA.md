# EMST prototype data

**Owner:** data engineer (an AI agent on the HCD team). **Consumers:** front-end developers and designers.
**Release:** `2.0.0-rc.1`. **Contract:** `DATA_CONTRACT.md` (team scratchpad).

The files in `app/data/` are generated. Do not edit them by hand. Rebuild and verify from the repository root:

```bash
node prototype/public-ui/tools/build-data.mjs && node prototype/public-ui/tools/verify-data.mjs
```

`build-data.mjs` projects the explorer's view model (`site/lib/model.mjs`, `buildModel`). The prototype therefore inherits every governance rule that the explorer codes and tests:

- the display gate;
- the claims register;
- the Tribal hold;
- credential-gate withholding;
- withheld signals;
- use tiers.

The script copies fields explicitly, one by one. It never serialises a model object wholesale, and it stops with an error if the display gate ever starts to render a value: this contract has no shape for one yet, so the build fails closed.

`verify-data.mjs` checks the output and writes the "Verification" section at the end of this file.

## Loading

Each file is plain JavaScript that registers one JSON value. There is no fetch, so the files work under the explorer's CSP (`connect-src 'none'`):

```html
<script src="data/core.js"></script>          <!-- every page -->
<script src="data/role-rol-zk41bza.js"></script>
<script>/* in your own file: */ const core = window.EMSTDATA.core; const role = window.EMSTDATA["role:rol-zk41bza"];</script>
```

- **Format.** Minified JSON, UTF-8. `<` inside strings is escaped as `<`. No functions.
- **Manifest.** `app/data/manifest.json` lists every file, its key and its size in bytes (`raw`, and `gz` at gzip -9). Pages do not load it; the verifier and build tools read it.

| File | Key | Load when |
|---|---|---|
| `core.js` | `core` | every page |
| `role-<slug>.js` (37) | `role:<slug>` | a role or variant page (slug from `core.roles`) |
| `comp-NN.js` (12, about 20 competencies each) | `comp:NN` | a competency page (`core.shards.comp[slug]` gives `NN`) |
| `task-NN.js` (14, about 100 tasks each) | `task:NN` | a task detail or evidence drawer (`core.shards.task[slug]`) |
| `search.js` | `search` | search: every kind except tasks, plus synonyms |
| `search-tasks.js` | `search:tasks` | search over task statements (split off to stay within the size budget) |
| `change.js` | `change` | What's coming |
| `hr.js` | `hr` | federal series and state or local class views |
| `paths.js` | `paths` | Where it can lead |

`NN` is two digits (`00`, `01` …), both in file names and in keys. In `core.shards` it is a plain integer.

## Conventions

- **Empty values are left out.** A key whose value is `null`, `""`, `false`, `[]` or `{}` is omitted, so an absent key means "not set" or "false". Numbers are always kept, including `0`.
- **Slugs** are the explorer's URL slugs:
  - roles: `rol-zk41bza`;
  - variants: `rol-zk41bza--federal`;
  - competencies: `cmp-…`;
  - tasks: `tsk-…`;
  - signals: `sig-…`;
  - instruments: `ins-…`;
  - tools: `tol-…`;
  - credentials: `cred-<title slug>`;
  - series: their code (`0460`);
  - classes: `pa-phl-7e45`.
- **Record IDs.** `id` holds the release record ID (`emst:core/ROL-ZK41BZA`) where one exists. IDs are candidate IDs until 2.0.0.
- **Shared sub-objects:**
  - **Tier** `tier: {t, cap, dec, src}`:
    - `t` is the effective use tier (`exploratory`, `describe`, `develop`, `select`; rc.1 has only the first two);
    - `cap` is the binding cap (explain it with `core.labels.capText`);
    - `dec` is the declared ceiling;
    - `src` appears only when the tier is not the computed one (`declared`, or a figure's source text).
  - **Evidence** `ev: {l, m, r, d, v, src, ai, v1, by}`:
    - `l`: evidence label `E`, `J` or `S` (`core.labels.evidence` and `evidenceDef`);
    - `m`: method;
    - `r`: review status;
    - `d`: generated date;
    - `v`: validation status;
    - `src`: source IDs (from the repository's sources registers);
    - `ai`: an AI-agent draft;
    - `v1`: v1 seed text not yet rewritten;
    - `by`: drafting agent IDs (AI agent roles, not people).
  - **Gated value** `{p: 1, txt}`. The value has not passed the display gate. Show `txt`, the gate's own label text, and never a value. This covers:
    - tasks: `wf`, `craft` and `exp`;
    - job-analysis values: `ja`.
  - **Crosswalk row** `{set, pred, not, obj, lab, conf, close, none, rev, st, rater, ev, note, ver, o, fr}`:
    - `set`: mapping set;
    - `pred`: SKOS predicate (plain words in `core.labels.match`);
    - `not`: a negative mapping, meaning the drafting agent recorded that this is **not** a match;
    - `obj`: external object ID (absent when `none`);
    - `lab`: the object's human-readable label, only where the release carries one (see "Labels");
    - `conf`: agent confidence (uncalibrated);
    - `close`: closeMatch or better, not negated, with a real object (the only rows that read as a crosswalk);
    - `none`: no matching term found;
    - `rev`: reviewed by a person (none in rc.1);
    - `st`: review status;
    - `rater`: rater type;
    - `ev`: evidence label;
    - `note`: comment;
    - `ver`: object source version;
    - `o`: selected SSSOM `other` fields: `to` (applies to), `rl` (role level), `var` (variant), `ss` (target series status), `rel` (relationship);
    - `fr`: friction fields `{posture, licensure, pay}` from `friction_*`.
    Show `core.text.crosswalkNote` with every crosswalk table.

## `core` (`core.js`)

- **`release`.** Contains:
  - `id`, `date`, `commit`, `profile`, `schemaVersion`;
  - `notice` (the use notice, with internal decision references removed, as the explorer shows it);
  - `indigenousStatement`, `license`;
  - `displayGateRule`, `gatesVersion`, `eutRule`, `changeRule`;
  - `agreementStudies` (empty in rc.1);
  - `venueRule`, `venueAsOf` (the computed federal-applicability view);
  - `hrStamp` (generator stamp of the HR views).
- **`status.held`.** `{n, source, policy}` is the Tribal hold. `n` is 163, from `views/counts.json` `heldRecords`; the build checks it against `RELEASE_NOTES.md`. `policy` is the explorer's policy sentence. Show only the count and this text.
- **`status.gate`.** `{source, asOf, items: [{n, item, result}], overall}` is the release gate from `docs/release/2.0.0-rc.1/GATE_REPORT.md`, read-only. Items 6 and 7 fail, so rc.1 is not cleared for external publication.
- **`text`.** Explorer wording that must travel with the data, reused verbatim from the templates. Use these strings rather than rewriting them:
  - `useNotice`, `authorship`, `credit`, `callToAction`, `issuesUrl`;
  - `hrDisclaimer` (two paragraphs; the first is the three-part disclaimer);
  - `crosswalkNote`, `negativeMapping`, `agentConfidence`, `unverified`;
  - `jaPending`, `jaNote`, `targetsNote`, `pctTimeNote`;
  - `credentialMayBeInvolved`, `credentialPending`, `signOffPending`;
  - `gradeNote`, `editorialAttr`, `moduleTag`;
  - `v1DrawerTitle`, `v1DrawerBody`, `v1DrawerChange`;
  - `watchSignal`, `sourceGrade`, `tooFew`, `noSignal`, `stayHuman`;
  - `externalContext`, `countsNotShares`;
  - `pathwaysNotice`, `whatsComingNotice`, `realignment`;
  - `venue`, `indicatorPlacement`, `scenarioSensitivity`, `noRegret`.
- **`counts`.** The release counts view:
  - `byType`, `competenciesByKind`, `competenciesByModule`, `competenciesByModuleAndKind`, `competenciesByLifecycle`, `byLifecycle`, `rolesByTier`, `variantsBySectorActor`, `coreCompetencies`, `heldRecords`, `redactedReferences`, `deferredTargets`, `changeSignalObservations`;
  - `excluded: [{reason, n}]`. The Tribal-hold reason is carried only as `status.held`.
- **`stats`.** The explorer's build statistics:
  - `tasks`, `indicators`, `mappings`, `tools`, `v1Assessments`;
  - `gatedRendering` (0) and `gatedRows`;
  - `depth: {full, lower, emerging}`.
- **`useTierTotals`.** Counts by effective use tier, from `views/effective_use_tier.json`: describe 1,789, exploratory 1,949.
- **`figs`.** Badge data for the explorer's headline figures: `{<figure>: {tier, ev: {l, ai, r}}}`. Every number you show needs a tier badge and an evidence badge.
- **`labels`.** Code-to-text maps from `vocab/`, through the view model:
  - `workFunction`, `workFunctionDef`;
  - `sectorActor`, `sectorActorSubtype`, `authorityPosition`;
  - `module`, `competencyType`, `level`, `levelDescriptors`, `attribute`;
  - `useTier` (definition) and `useTierText` (short text), `capText`, `lifecycle`;
  - `evidence`, `evidenceDef`, `reviewStatus`, `raterType`;
  - `signalFamily`, `reliability`, `instrumentStatus`;
  - `subsector`, `craft` (FC, DC and SC enactment kinds);
  - `match` (predicate in plain words; replace `{noun}` with "series", "class" or "term");
  - `depth`.

  `gateLabels` holds the display gate's label texts. `gateLabels.v1_prior` is the required v1 drawer label.
- **`roles[]`.** Role index, with these fields:
  - identity and text: `id`, `slug`, `title`, `alt[]`, `def` (≤ 280 characters), `fn` (function statement);
  - work function: `wf`, `wfLabel` (the editorial primary work function, not a rated value);
  - depth: `depth` (P1 to P4) and `depthLabel`;
  - status: `lc` (lifecycle), `tier`, `module`, `isModule`;
  - employers: `actors[]` (labels) and `variants[{slug, actor, actorLabel}]`;
  - counts: `nTasks`, `nComps`, `nVariants`;
  - `whatsComingOnly`.

  P3 roles carry `whatsComingOnly: true`, `reviewBy`, `horizon` and `ev`, but no task or competency counts. Show them only in What's coming.
- **`comps[]`.** Competency index, with these fields:
  - `id`, `slug`, `title`;
  - `stmt` (≤ 200 characters);
  - `type`, `typeLabel`, `module`, `isModule`;
  - `span: [min, max]`;
  - `tier`, `lc`, `ev: {l, ai, v1, r}`;
  - `v1Codes` (lineage);
  - `nTasks`, `nRoles`;
  - `gap` (usable in the role-independent gap check);
  - `shard`.
- **`modules[]`.** `{ns, label, n, code, wave}`; the `core` row has `core: true`. Module records are editorial sections, not stewarded modules, and stay out of default HR views.
- **`workFunctions[]`.** `{code, label, def, nRoles}`.
- **`jobFamilies[]`.** `{id, slug, title, def, roles: [{slug, basis}], tier, rule}`. Membership comes from `views/job_families.json`; titles and definitions come from the release's JobFamily records. P3 members are left out.
- **`sectorActors[]`.** `{code, label, subtypes: [{code, label}], nVariants}`. The Tribal actor is excluded by the view model.
- **`series[]`.** Contains:
  - `{code, slug, title, status, realignment, group}`;
  - `nRows` (all draft rows), `nClose` (closeMatch or better), `nRoles`, `nFed` (federal variants);
  - `generated` (a Federal Series Profile exists).
- **`stateClasses[]`.** `{slug, title, state, jurCode, code, nRoles, generated}`.
- **`shards`.** `{comp: {slug: n}, task: {slug: n}, compSize, taskSize, nComp, nTask}`.

## `role:<slug>` (`role-<slug>.js`)

### P1, P2 and P4 roles

- **Index fields.** Every field of the role index, with `def` in full.
- **Role-level fields:**
  - `reviewBy`, `counterSignal`, `horizon`;
  - `scen: [{code, label, dir}]`: scenario sensitivity, an agent-drafted hypothesis; show it with `text.scenarioSensitivity`;
  - `ev`;
  - `levels: [{key, band: [L…]}]`;
  - `ja: {p: 1, txt}`: the job-analysis gate for importance, time share, critical and needed-at-entry flags (bundle) and for importance and distinguishing (targets);
  - `crosswalks[]`: O*NET-SOC, SOC and OPM series rows;
  - `feeders[]`, `progressesTo[]`, `entryFrom[]`: `{slug, title, wc, v, actor, actorLabel}`. `v` and `actor` appear when the profile names a variant. `wc` marks a What's-coming-only role.
- **`tasks[]`.** The role's task bundle:
  - `{slug, stmt, formation, roleLevels[], comps: [{slug, title, strength}]}`;
  - `wf`, `craft`, `exp` (gated) and `ja` (gated);
  - `lc`, `tier`, `ev`, `module`;
  - `x2[]`: O*NET task rows.

  Bundle membership, role levels and formation flags are editorial drafts (`text.jaNote`).
- **`addedTasks[]`.** The same shape, for tasks that a variant adds to the role bundle.
- **`targets[]`.** Competency targets:
  - `{slug, title, type, levels: {roleLevel: L…}}`;
  - `tier`, `lc`, `module`, `isModule`, `moduleLabel`;
  - `isDefault`: established core content, or content from the role's home module (the HR default view);
  - `fed`: computed federal applicability `{actor, val, asOf, linked, verified, withheld}`; read it with `text.venue`.
- **`variants[]`.** One entry per employer-type variant:
  - identity: `id`, `slug`, `actor`, `actorLabel`;
  - editorial classification: `subtype`, `subtypeLabel`, `authority`, `authorityLabel`, `industry`, `ownership`, `delivery`;
  - text and status: `def`, `title`, `lc`;
  - `hr`: a federal or state variant; show `text.hrDisclaimer`;
  - `ja`;
  - credentials: `credentialGates: [{kind, title}]` (shown only when the issuer is verified, as "may be involved", never as a requirement) and `credentialGatesPending` (count not shown);
  - instruments: `instruments[]` (as in `change.instruments`, plus `via` (how the instrument is linked) and `typed`) and `instrumentsMore` (the further count, listed in What's coming);
  - sign-off: `signOff` and `signOffPending`;
  - `tools[]`, `disclaimers[]`, `jurisdiction[]`;
  - `grade: {scheme, label, bands: [{level, band}]}`; always show `text.gradeNote` with it;
  - `tier`, `ev`, `crosswalks[]` (state and local classes, private job architecture, public-private translation rows);
  - tasks: `sameTasks` (true when the variant's task list equals the role bundle); otherwise `tasks: [{slug, formation, roleLevels}]`, whose details are in `tasks[]` or `addedTasks[]`;
  - `chg`: the role-change summary per role-change@0.1.0:
    - `levels: [{key, band, total, assessed, pending}]` (task counts, never time shares);
    - `nTasks`, `nAssessed`, `nFormation`;
    - `emerging[]`: competency slugs at watch, emerging or proposed;
    - `signals[]`: signal IDs shown for this variant;
    - `actorWide`: signals about the employer type as a whole, counted here and listed in What's coming;
    - `withheld`;
    - `rule`;
  - `emergingNext: [{slug, title, lc}]`: emerging roles named as next steps (What's coming only);
  - `nDest`: number of destination roles shown on the pathways page.
- **`signals[]`.** Every signal shown on any of the role's variants (shape as in `change.signals`).
- **`hrSeries[]`.** `{code, title, close, profile}`: OPM series crosswalked at closeMatch or better, or covered by a generated profile.
- **`hrClasses[]`.** `{slug, title, jur, close, view}`.

### P3 roles

A P3 file carries only what What's coming shows:

- the index fields;
- `reviewBy`, `counterSignal`, `horizon`, `scen`, `ev`;
- `sectors: [{actor, actorLabel}]`;
- `feeders[]`;
- `nSignals`.

It has no tasks, targets, variants or crosswalks.

## `comp:NN` (`comp-NN.js`)

`{shard, comps: [...]}`. Per competency:

- **Identity and text:** `id`, `slug`, `title`, `alt`, `def`, `stmt`.
- **Type:** `type` and `typeLabel`; `typeNote` ("Editorial classification (not a rated value)"); `transversalCluster`.
- **Module:** `module`, `isModule`, `moduleLabel`, `subsectors: [{code, label}]`.
- **Status:** `span: [min, max]`, `lc`, `reviewBy`, `status`, `tier`, `ev`, `protect`.
- **`crosswalks[]`:** ESCO, OPM series association, OPM ECQ and DOL AI literacy rows.
- **`tools: [{id, title, lc, halfLife}]`.**
- **`venue: [{actor, val, asOf, linked, verified, withheld}]`.**
- **`levels: [{level, label, indicators: [...]}]`.** Each indicator is `{id, stmt, mode, attr, useClass, methods[], tier, ev}`:
  - `mode` is the augmentation mode;
  - `attr` is the distinguishing attribute label that the explorer shows ("distinguished by …"). It is not the gated "distinguishing" flag.
- **`ks: [{id, stmt, low, tier, ev}]`.** Knowledge statements; `low` is the lowest level.
- **`tasks: [{slug, stmt, strength}]`.**
- **`roles: [{slug, title, levels}]`.** P1, P2 and P4 roles that target the competency, with target levels by role level.
- **`enactments: [...]`.** Each enactment is `{id, title, kind, actorType, module, ck, authorityPosition, note, basis, principal, tier, ev}`. `ck` is the craft kind of a craft enactment (`labels.craft`).
- **Lineage:** `v1Codes` and `v1From: [{key, relation}]`.

Show `text.indicatorPlacement` under the levels.

## `task:NN` (`task-NN.js`)

`{shard, tasks: [...]}`. Per task:

- **Identity:** `id`, `slug`, `stmt`.
- **Links:**
  - `comps: [{slug, title, strength}]`;
  - `roles: [{slug, title, formation}]`, from role bundles and variant bundles; P3 roles excluded.
- **Gated:** `wf`, `craft`, `exp`.
- **Editorial attributes:** `fieldDependency` and `formationDependency`, shown with `text.editorialAttr`. Both are empty in rc.1: the release moved them into `agentDraft`.
- **Credentials:** `credentialGates[]` and `credentialGatesPending`.
- **Sign-off:** `signOff` and `signOffPending`.
- **Status:** `lc`, `tier`, `ev`, `module`, `isModule`.
- **`tools: [{id, title, lc}]`.**
- **`x2[]`:** O*NET task rows.
- **`v1`:** the evidence drawer, present only when v1 records exist. Its shape is `{lab, prior: [{id, d, src, conf, flags, stale, vals: [[label, value]]}], contested, reasons[]}`. `lab` is the required label ("v1 single-analyst prior, LLM-assisted, unvalidated — not for decisions."). Show the drawer only inside a closed disclosure with `text.v1DrawerBody`. Never count, average or headline these values.

## `search` and `search:tasks`

- **`search.docs[]` and `search:tasks.docs[]`.** Each document is `{k, s, t, a, c, x, w}`:
  - `k`: kind (`role`, `comp`, `task`, `series`, `class`, `signal`, `tool`, `credential` or `module`);
  - `s`: slug or route ID;
  - `t`: title;
  - `a`: alternative labels;
  - `c`: codes;
  - `x`: context (≤ 120 characters);
  - `w`: weight hint, 0 to 1.
- **Codes on role documents.** Role documents carry the O*NET-SOC, SOC and OPM series codes from the role's crosswalk rows, and the state and local class codes and titles from its variants' rows, at closeMatch or better only.
- **Codes on other documents.** Series documents carry `0460` and `GS-0460`. Competency documents carry v1 codes.
- **`search.syn`.** `{term (lower case): [expansions]}`. Expansions are one-way. Automatic entries:
  - alt label → preferred title;
  - OPM series or class title → titles of roles crosswalked at closeMatch or better.

  Curated entries come from `tools/synonyms.yaml` (see below).
- **`search.tools`.** `{id: {title, lc, cat, comps[], tasks[], variants[]}}`: where each tool appears.
- **`search.credentials`.** `{id: {title, kinds[], tasks[], variants[]}}`: credentials the view model shows, only where the issuer is verified. Always present them as "may be involved (agent-drafted link)".

## `change` (`change.js`)

- **`notice`.** The What's coming notice.
- **`signals[]`.** Shown signals only:
  - `{id, title, family, status, about, target}` (`target` is a role or variant slug when the signal is about one);
  - `sg` and `sgTxt`: the source grade, Admiralty A to D; show it with `text.sourceGrade`;
  - `m: {v, u, n, den, few}`: the measure as reported by the source; `few` means n < 10, so say `text.tooFew`;
  - `per: {start, end}`, `src`, `reviewBy`;
  - `sp[]`: signposts;
  - `ev`, `unv`.
- **`withheld`.** `{n, rows, reason}` for signals withheld under the claims register (0 in rc.1).
- **`watchItems[]`.** `{id, slug, title, lc, reviewBy, outcome, counter, hyp: {type, label, stmt}, signals[], signalsWithheld, tier, ev}`.
- **`emergingRoles[]`.** Contains:
  - `{slug, title, lc, wc, fn, horizon, reviewBy, counter}`;
  - `sectors: [{actor, actorLabel, v}]`, where `v` is empty for What's-coming-only roles;
  - `feeders[]`, `scen[]`, `nSignals`, `tier`, `ev`.
- **`emergingComps[]`.** `{slug, title, lc, reviewBy, module, isModule, moduleLabel, tier, ev}`.
- **`instruments[]`.** Contains:
  - `{id, title, type, jur, cit}`;
  - `st` and `stTxt`: status as of the release date;
  - `unv`: claims-register rows; when set, show only the title and `text.unverified`, with no status or dates;
  - `noEv` and `noEvRow`: no dated event ("status not recorded");
  - `ev: [{d, sup, claim, type, after, fut}]`: dated events. When `sup` is set, the date was judgment-dated and is withheld: show the type and the claim ID, not a date. `fut` marks a scheduled event;
  - `next`: next review;
  - `e`: evidence.
- **`instrumentsWithheld`.** `{n, rows, reason}`. In rc.1, 13 instruments are withheld from the release under 12 register rows.
- **`drivers[]`.** The same events as a flat timeline, with an `inst` slug.
- **`scenarios`:**
  - `axes: [{code, label, poles: [{code, def}]}]`;
  - `terms: [{code, label, summary, risk}]`;
  - `signposts: [{code, text, source, cadence, toward, signals[], withheld}]`;
  - `noRegret[]` and `noRegretNote`;
  - `wildcards[]`.
- **`changeIndicators`.** `{rule, n, moved, rows: [{target, role, kind, decision, reasons[], nCounted, nWatch}], reasonText}`. All 210 rows are at watch.
- **`figures`.** Badge data.

## `hr` (`hr.js`)

- **Top-level text:**
  - `disclaimer`: the three-part HR disclaimer, two paragraphs. It must appear on every series, class and federal or state variant view;
  - `pctTimeNote`;
  - `notes: {series, candidates, defaultView, credentials}`.
- **`series[]`.** All 79 register records:
  - `{id, code, slug, title, status}`;
  - `realignment` and `successor`: if `realignment` is set, say `text.realignment` ("Realignment proposed, not final"); never say the series has moved;
  - `group`, `qualStd`, `qualVerify` (the register marks it for verification);
  - `ped` and `pedNote`: positive education requirement, "yes" or "no", an AI agent's judgment;
  - `reviewBy`, `notes`, `tier`, `ev`;
  - `rows[]`: role crosswalk rows (crosswalk row plus `role`, `v` and `sub` (subject label)). Show rows with `close` by default; put the others under `notes.candidates`;
  - `coreComps: [{slug, title, rel, pred, st, fed}]`;
  - `omittedModule` and `omittedNotEstablished`;
  - `fedVariants: [{v, role, title, hrTargets[]}]`;
  - `generated`.
- **`generated[]`.** The 13 Federal Series Profiles:
  - `{code, stamp, notice, general}`;
  - `roles[]`, each with:
    - `{role, v, title, depth, fn}`;
    - `x4: {pred, conf, to, st, ev}`;
    - `credentialGates` and `credentialGatesPending`;
    - `instruments: [{id, title, link, st, unv, noEv}]`;
    - `home`, `homeLabel`, `tier`;
    - `bands[]`, each with:
      - `{group, band, roleLevels}`;
      - `duties: [{comp, duty, isDefault, isModule, moduleLabel, lc, tasks[]}]`. Duties have no percentages;
      - `factor1: [{comp, stmt, knowledge[]}]`: default content only;
      - `factor1NotDefault`: a count;
  - `withoutFed[]` and `feeders[]`.
- **`classes[]`.** All 38 state and local class records:
  - identity: `{id, slug, title, jur, jurCode, code, scheme, seriesName}`;
  - class facts: `agency`, `employerType`, `level`, `supervisory`;
  - specification: `specUrl` (an outbound link to the official specification), `specRetrieved`, `specEffective`;
  - qualifications: `mq` (a paraphrase), `degreeRule`, `licenses: [{credential, issuer, timing}]`. These are the class specification's own requirements;
  - pay and appointment: `pay`, `payEffective`, `appointment[]`;
  - `reviewBy`, `tier`, `ev`;
  - `rows[]`;
  - `pending[]`: draft mappings in the class record, used only when no crosswalk rows exist;
  - `view`: the 20 State Class Views. `{stamp, notice, mappings: [...]}`, where each mapping is:
    - `{v, role, roleTitle, actorLabel, depth, roleLevels, match, conf, review, authority, homeLabel, tier}`;
    - `targets: [{comp, title, levels, isDefault, moduleLabel, lc}]`;
    - `tasks[]`;
    - `credentialGates` and `credentialGatesPending`.

## `paths` (`paths.js`)

Everything in this file is exploratory and never a recommendation. `notice` says so, and every pathways view must show it.

- **`rule` and `edgeNote`.** The rule ID, and how edges are computed.
- **`variants`.** `{variantSlug: {role, title, actor, actorLabel}}` resolves edge ends to a role slug and an actor.
- **`edges[]`.** From `views/pathway_edges.json`, restricted to variants the view model shows:
  - `{from, to}`: variant slugs;
  - `fromLevel`, `toLevel`;
  - `shared: {N, M}` and `statement`;
  - `named`: named as a next step in the profile;
  - `shown`: listed by the explorer, whose display rule keeps the top six destination roles per variant;
  - `gap: [{slug, fromLevel, toLevel}]`; `fromLevel` is absent when the origin does not target the competency;
  - `fric[]`.
- **`translations[]`.** Cross-sector translation seed rows:
  - `{from, fromLabel, to, toLabel, id}`;
  - the crosswalk row fields without `obj` or `lab` (`to` and `toLabel` name the variant);
  - `fr`: friction fields.
- **`pathways[]`.** Learning pathways the view model exposes on edges: `{id, type, steps, from, to}`. `nPathwayRecords` is the number of pathway records in the release (11).

## Curated synonyms (`tools/synonyms.yaml`)

The file holds 68 rows:

- 36 abbreviation and shorthand rows, including every one the contract names, plus WUI, ICS, T&E, ESA, CWA, NPDES, SWPPP, HAZWOPER, QA/QC, REHS, PD, IDP, KSA, fuels, hotshot, WLFF and enviro;
- 32 OPM series nickname rows, covering every series code the contract names, "0401 fire" and "0462 forestry technician".

Each row has:

- `term` and `expansions`;
- `kind`;
- `source: editorial (prototype)`, which the build enforces;
- optional `confidence: low` and `note`.

The build adds the register title to every series row from the OPM series register, and fails if a series code is not in the register.

Three rows are marked low confidence:

- **"0401 fire".** Professional fire positions are classified differently across agencies.
- **"0462 fire".** Wildland firefighters are moving from 0462 to the 0456 Wildland Fire Management series.
- **"LE ranger".** Law enforcement rangers sit in different series at different agencies.

The rows are vocabulary, not EMST data. No practitioner has reviewed them.

## Labels for external objects

The build never invents a label. When no label exists, it exports the code and leaves `lab` empty.

- **Labels the build uses:**
  - OPM series: `SeriesRecord` titles;
  - state and local classes: `StateClassRecord` class titles;
  - EMST records: view-model titles;
  - SSSOM `object_label` wherever a TSV carries one. In rc.1, only the X10 evidence-equivalence set does, and the prototype does not export that set.
- **Codes with no label anywhere in the release.** None of the SSSOM files, `csv/` or the bundle carries a label for these objects, so they are exported as codes only:
  - O*NET-SOC (36 codes) and SOC 2018 (32);
  - O*NET task (121);
  - ESCO (245; the row `note` often names the skill in passing, but it is a comment and is not used as a label);
  - OPM ECQ (12);
  - DOL AI literacy (20);
  - private job architecture `EMSTpja` (46);
  - 4 PA position records and 2 TX class records without a released class record.

## Not exported

| What | Why |
|---|---|
| Importance, time share, critical, needed-at-entry, distinguishing, critical-for-selection, `pctTime` | Job-analysis values; the view model nulls them (`ja` gate). Only the gate text is exported. |
| Work function, craft and exposure values; agent work-function and craft ratings | Display gate: no value passes. Exported as `{p:1, txt}`. |
| `agentDraft` contents, indicator OBS-4 | Gated agent drafts; never in the view model. |
| Signal `direction`, `directionConfidence`, driver tags, `impact`, STEEP category, method, geography, independence key, measure baseline and CI | Direction and driver tags are agent drafts the explorer never shows; the other fields are not shown by the explorer, so their display status is unclear. |
| Change-indicator `direction`, `driver`, signal ID lists | Agent-drafted signal tags; the explorer shows only counts and reasons. |
| Rating counts by rater type (`ratingsByRaterType`, `ratingUnitsByRaterType`) | Not shown by the explorer; they describe hidden agent ratings. |
| Instrument mechanism lists and mechanism definitions | Not shown on What's coming. One mechanism definition (DM-11) contains a Tribal-hold trigger term. The variant `via` text carries the mechanism code and name the explorer shows. |
| Driver event `direction`, per-event `reviewBy`, event evidence label | Not shown by the explorer. |
| Status and events of instruments with an unverified register row | Claims register: title and flag only. |
| Dates of judgment-dated events (REG-08) | Claims register. The view model nulls them (`sup: true`). |
| Credential gates whose issuer is not verified | View model withholds them; only counts are exported. |
| P3 roles' task bundles, targets, variants (other than actor labels) and crosswalks | P3 roles appear only in What's coming, which shows none of these. P3 roles and variants are also left out of pathway edges (298 release-view edges), job-family membership (9 members) and task and competency role lists. They do appear in HR crosswalk rows, as the explorer shows them there. |
| Job-family `share` (anchor share) | A computed number the explorer does not show; its display status is unclear. |
| Pathway records' `cloOutcomes`, `formationProvisions` and quotas | Not exposed by the view model and not shown by the explorer. Only type and step count are exported. |
| Non-default factor-1 knowledge in Federal Series Profiles | The explorer shows default (established core or home-module) factor-1 content only. A count is kept. |
| SSSOM `other` fields: `via`, `status_as_of`, `proposed_successor` on rows, model, prompt, coder IDs, pools | Not shown by the explorer. `via` can carry v1 lineage codes, and successor codes on rows could read as a realignment. The series record keeps `successor` behind `realignment`. |
| Series `editorialNote` | Empty in rc.1. The release's Tribal scan skips this field, so `notes` is exported only if it passes the verifier's scan. |
| Venue view raw rows (`deciding` instruments) | The view model exposes only the computed value and flags. |
| v1 exposure codes outside the task `v1` drawer | Explorer rule: v1 values only in the drawer. |
| Labels of external objects with no label in the release | Never invented (see "Labels"). |
| The role-change summary as prose text | The view model has none; `chg` carries its task counts. |

## Findings for the team

- **Negative mappings.** 102 ESCO rows (and one OPM series row) carry `predicate_modifier: Not`, meaning the drafting agent recorded that they are **not** matches. The view model's crosswalk rows drop the modifier, so the explorer's competency pages list them as ordinary matches (for example "close fit").
  - The prototype reads the modifier from the SSSOM files and exports `not: true`, with `text.negativeMapping`.
  - Front ends should show these rows as "not a match", or hide them.
  - Worth raising with the explorer's owner.
- **No human-readable labels for most external crosswalk objects.** O*NET, SOC, ESCO, ECQ and DOL objects have no label in the release (see "Labels").
- **Sizes.** Task statements dominate search, so they are split into `search-tasks.js`. Every file is within budget; see "Verification".

## Verification

<!-- verification:start -->
Result: **PASS** (0 problems). Release 2.0.0-rc.1; verified 2026-10-30 by `tools/verify-data.mjs`.

| Check | Result |
|---|---|
| 1. Parse and register | 70 files; each registers exactly one key; pure JSON; `<` escaped |
| 2. Size budget | core.js 59.4 KB gz / 258.7 KB raw (≤ 150 / 600); largest other file 88.6 KB gz (≤ 120) |
| 3. Counts | roles 37/37; competencies 223/223; tasks 1317/1317; variants 121/121; series 79/79 (13 generated profiles); classes 38/38 (20 generated views); signals 107/107 (0 withheld); held records 163 |
| 4. References resolve | 29891 references checked |
| 5. Forbidden content | 220839 strings and 57963 objects scanned (35158 distinct texts); 655 dated events checked; rules: gated keys, agentDraft, craft/exposure scores, 17 Tribal-hold triggers, 17 held seed keys, 3 held v1 codes, e-mail/phone, 16 retired-claim rules, 85 register and do-not-publish wrong forms, 2 conflation rules, 13 withheld phrases, 6 judgment-dated events, 0 unverified instrument titles |

| File | Raw KB | Gzipped KB |
|---|---:|---:|
| core.js | 258.7 | 59.4 |
| role-*.js (37 files; largest 11.7 KB gz) | 2030.7 | 260.6 |
| comp-NN.js (12 files; largest 35.6 KB gz) | 1895.7 | 350.0 |
| task-NN.js (14 files; largest 17.1 KB gz) | 1901.5 | 221.9 |
| search.js | 211.1 | 43.6 |
| search-tasks.js | 338.3 | 88.6 |
| change.js | 179.9 | 22.9 |
| hr.js | 449.0 | 41.7 |
| paths.js | 675.5 | 25.1 |
| **Total (70 files)** | **7992.4** | **1131.1** |
<!-- verification:end -->
