#!/usr/bin/env node
// EMST public-interface prototype: data build (owner: data engineer; contract: DATA_CONTRACT.md; docs: docs/DATA.md).
//
// Projects the explorer's view model (site/lib/model.mjs, buildModel) into plain-JS data files under app/data/, each
// registering one JSON value on window.EMSTDATA. The view model already applies the display gate, the claims
// register, the Tribal hold, credential-gate withholding, withheld signals and use tiers, so this script only
// projects what it exposes, explicitly, field by field. It never serialises a model object wholesale (the graph is
// cyclic) and never copies a field the model gates. Values the model does not expose are read from the release only
// where the contract allows it (views/*.json, sssom/**, vocab/*.yaml, labels on SeriesRecord, StateClassRecord and
// JobFamily records), and only ungated descriptive fields.
//
// Run from the repository root:  node prototype/public-ui/tools/build-data.mjs
// Licence: Apache-2.0 (code); generated data CC0-1.0, as the release.
import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, rmSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";
import { gzipSync } from "node:zlib";

const HERE = dirname(fileURLToPath(import.meta.url));
const UI = resolve(HERE, "..");
const ROOT = resolve(UI, "..", "..");
const OUT = process.env.EMST_DATA_OUT ? resolve(process.env.EMST_DATA_OUT) : join(UI, "app", "data"); // EMST_DATA_OUT: build somewhere else for a dry run
const require = createRequire(join(ROOT, "site", "package.json"));
const yaml = require("js-yaml");
const { buildModel, slugOf } = await import(pathToFileURL(join(ROOT, "site", "lib", "model.mjs")).href);

const meta = JSON.parse(readFileSync(join(ROOT, "site", ".cache", "release-meta.json"), "utf-8"));
const REL = meta.releaseDir;
const m = buildModel({ root: ROOT, releaseDir: REL, meta });
const readJson = (p) => JSON.parse(readFileSync(p, "utf-8"));
const loadYaml = (p) => yaml.load(readFileSync(p, "utf-8"));

// ---------------------------------------------------------------- governed-content guard (same regexes as lib/model.mjs)
const gc = loadYaml(join(ROOT, "schema", "lint", "governed_content.yaml"));
const triggers = gc.tribal_hold.triggers.map((p) => (typeof p === "string" ? new RegExp(p, "i") : new RegExp(p.pattern, p.cs ? "" : "i")));
const releasable = (s) => !triggers.some((rx) => rx.test(String(s || "")));
const dropped = [];          // [{where, why}] counted into the build report and docs/DATA.md

// ---------------------------------------------------------------- compact helpers
// Keys whose value is null, undefined, "", false, [] or {} are omitted from every output object (absent = not set or false).
const isEmpty = (v) => v == null || v === "" || v === false || (Array.isArray(v) && v.length === 0) || (typeof v === "object" && !Array.isArray(v) && Object.keys(v).length === 0);
function prune(v) {
  if (Array.isArray(v)) return v.map(prune);
  if (v && typeof v === "object") {
    const o = {};
    for (const [k, x] of Object.entries(v)) { const p = prune(x); if (!isEmpty(p)) o[k] = p; }
    return o;
  }
  return v;
}
const clip = (s, n) => {
  s = String(s || "");
  if (s.length <= n) return s;
  const cut = s.slice(0, n - 1);
  const sp = cut.lastIndexOf(" ");
  return (sp > n * 0.6 ? cut.slice(0, sp) : cut).replace(/[\s,;:.]+$/, "") + "…";
};
const stripRefs = (t) => (t == null ? t : String(t).replace(/\s*\((?:ADR-\d|SPEC §|CR-[A-Z]+-\d)[^)]*\)/g, ""));

const tierC = (t) => (t ? { t: t.tier, cap: t.bindingCap, dec: t.declared, src: t.source === "computed" ? "" : t.source } : undefined);
const evC = (e) => (e ? { l: e.label, m: e.method, r: e.reviewStatus, d: e.generatedAt, v: e.validationStatus, src: e.sources, ai: e.isAgentDraft, v1: e.isV1Seed, by: e.agents } : undefined);
// Fail closed: a gated value that now renders has no agreed shape in this contract, so the build stops.
function gated(g, what) {
  if (!g) return { p: 1, txt: m.gateLabels.assessment_pending };
  if (g.renders) throw new Error(`display gate now renders ${what}; extend build-data.mjs before exporting it`);
  return { p: 1, txt: g.text || m.gateLabels.assessment_pending };
}

// ---------------------------------------------------------------- labels for crosswalk objects (never invented)
const objLabel = new Map();
for (const s of m.series) objLabel.set(`OPMseries:${s.code}`, s.title);                     // SeriesRecord titles
for (const c of m.stateClasses) {                                                         // StateClassRecord titles
  for (const r of c.rows) if (!r.noTerm) objLabel.set(r.object, c.title);
}
for (const v of m.variants) objLabel.set(v.id, v.title);
for (const r of m.roles) objLabel.set(r.id, r.title);
for (const c of m.competencies) objLabel.set(c.id, c.title);
// SSSOM object_label wherever a TSV carries it (rc.1: only the X10 evidence-equivalence set), and predicate_modifier,
// which the view model's crosswalk rows leave out: a "Not" row is a negative mapping and must not read as a match.
const notRows = new Set();
{
  const walk = (d) => readdirSync(d, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? (e.name === "strict-1.0" ? [] : walk(join(d, e.name))) : e.name.endsWith(".sssom.tsv") ? [join(d, e.name)] : []));
  for (const f of walk(join(REL, "sssom"))) {
    const lines = readFileSync(f, "utf-8").split("\n").filter((l) => l && !l.startsWith("#"));
    const head = lines.shift().split("\t");
    const ix = (k) => head.indexOf(k);
    const set = f.slice(join(REL, "sssom").length + 1).replace(/\.sssom\.tsv$/, "");
    for (const l of lines) {
      const c = l.split("\t");
      const obj = c[ix("object_id")], lab = ix("object_label") >= 0 ? c[ix("object_label")] : "";
      if (lab && obj && !objLabel.has(obj) && releasable(lab)) objLabel.set(obj, lab);
      if (ix("predicate_modifier") >= 0 && c[ix("predicate_modifier")] === "Not") notRows.add(`${set}|${c[ix("subject_id")]}|${c[ix("predicate_id")]}|${obj}`);
    }
  }
}
const labelOf = (obj) => objLabel.get(obj) || "";
const unlabelled = new Map();   // prefix -> Set of exported object IDs without a label
let notExported = 0;
// Selected `other` keys the explorer displays (applies_to on series pages, role_level on class pages, the federal
// variant flag, the series status, fh_relationship on series competency lists).
const OTHER_KEEP = { applies_to: "to", role_level: "rl", variant: "var", target_series_status: "ss", fh_relationship: "rel" };
function xw(r, subject) {
  const o = {};
  for (const [k, s] of Object.entries(OTHER_KEEP)) if (r.other?.[k]) o[s] = r.other[k];
  const fr = { posture: r.other?.friction_posture_change, licensure: r.other?.friction_licensure_gap, pay: r.other?.friction_pay_direction };
  const lab = r.noTerm ? "" : labelOf(r.object);
  if (!r.noTerm && !lab) { const p = String(r.object).split(":")[0]; if (!unlabelled.has(p)) unlabelled.set(p, new Set()); unlabelled.get(p).add(r.object); }
  const not = !r.noTerm && !!subject && notRows.has(`${r.set}|${subject}|${r.predicate}|${r.object}`);
  if (not && !r.noTerm) notExported++;
  return { set: r.set, pred: r.predicate, not, obj: r.noTerm ? "" : r.object, lab, conf: r.confidence === "" ? null : r.confidence,
    close: r.closeOrBetter, none: r.noTerm, rev: r.reviewed, st: r.reviewStatus, rater: r.raterType, ev: r.evidence,
    note: r.comment, ver: r.objectSourceVersion, o, fr };
}
const codeOf = (obj) => String(obj || "").replace(/^[A-Za-z]+:/, "").replace(/^(\d{2}-\d{4}(?:\.\d{2})?)$/, "$1");

// ---------------------------------------------------------------- shared lookups
const roleById = new Map(m.roles.map((r) => [r.id, r]));
const variantById = new Map(m.variants.map((v) => [v.id, v]));
const compById = new Map(m.competencies.map((c) => [c.id, c]));
const taskById = new Map();
for (const c of m.competencies) for (const t of c.tasks) taskById.set(t.id, t);
for (const r of m.roles) for (const b of r.taskBundle) taskById.set(b.task.id, b.task);
for (const v of m.variants) for (const b of v.bundle) taskById.set(b.task.id, b.task);
const rolesMain = m.rolesMain;
const roleRef = (r) => (r ? { slug: r.slug, title: r.title, wc: r.whatsComingOnly } : null);
const compRef = (c) => ({ slug: c.slug, title: c.title });

const signalC = (s) => ({
  id: slugOf(s.id), title: s.title, family: s.family, status: s.status, about: s.targetLabel,
  target: roleById.get(s.target)?.slug || variantById.get(s.target)?.slug || "",
  sg: s.sourceGrade, sgTxt: s.sourceGradeText,
  m: s.measure ? { v: s.measure.value, u: s.measure.unit, n: s.measure.n, den: s.measure.denominator, few: s.measure.n != null && s.measure.n < 10 } : null,
  per: s.period ? { start: s.period.start, end: s.period.end } : null,
  src: s.sourceRelease || s.source, reviewBy: s.reviewBy, sp: s.signposts, ev: evC(s.evidence), unv: s.unverified,
});
const eventC = (e) => ({ d: e.date, sup: e.dateSuppressed, claim: e.claimId, type: e.type, after: e.statusAfter, fut: e.future });
const instC = (i) => ({
  id: slugOf(i.id), title: i.title, type: i.type, jur: i.jurisdiction, cit: i.citation,
  st: i.unverified.length ? "" : i.status, stTxt: i.unverified.length ? "" : i.statusText,
  unv: i.unverified, noEv: i.noEvents, noEvRow: i.noEventRow, ev: i.unverified.length ? [] : i.events.map(eventC),
  next: i.nextReview, e: evC(i.evidence),
});
const venueC = (v) => (v ? { actor: v.actor, val: v.value, asOf: v.asOf, linked: v.basisLinked, verified: v.basisVerified, withheld: v.basisWithheld } : null);
const gatesC = (gs) => (gs || []).map((g) => ({ kind: g.kind, title: g.title }));

// Explorer wording that must travel with the data (from site/src templates and macros; reused verbatim).
const TEXT = {
  useNotice: "For development and planning only; not a selection instrument.",
  authorship: "This explorer and its records were researched and drafted by a team of AI agents (Anthropic's Claude), each given a specialist role, working to a charter set by the EMST project lead. AI agents checked the facts against sources in October 2026. No independent human expert has reviewed it yet. Role names such as \"Chief Taxonomy Architect\", or \"EMST's federal HR agent\" on these pages, are AI agent roles, not people.",
  credit: "EMST project lead",
  callToAction: "To comment, correct an error or ask about the pilot, open an issue on the project's GitHub Issues page.",
  issuesUrl: "https://github.com/jrwashebek/Enviroskillstaxonomy/issues",
  hrDisclaimer: ["Not a classification basis. Not a job analysis. Not for RIF, adverse action or performance-rating decisions.",
    "This view describes work for development and planning. Any position description built from it is a draft that must be reviewed, revised and adopted by the responsible official, and is subject to classification review."],
  crosswalkNote: "Draft mappings are navigation aids, not alignment claims. No alignment with O*NET, ESCO, OPM or any state system is claimed until a human-reviewed mapping set exists.",
  negativeMapping: "Negative mapping: the drafting agent recorded that this is not a match (kept for disambiguation).",
  agentConfidence: "agent confidence (uncalibrated): the drafting model's own number, not calibrated",
  unverified: "Unverified — not for citation",
  jaPending: "Assessment pending (job analysis)",
  jaNote: "Which tasks the role bundles, at which levels, and which are formation tasks are editorial draft design values (agent-drafted, unreviewed). Importance, time share and the critical and needed-at-entry flags are job-analysis values: they read \"Assessment pending (job analysis)\" until a named person reviews them.",
  targetsNote: "Target levels by role level: design statements drafted by AI agents, not findings. Not yet reviewed by practitioners.",
  pctTimeNote: "% time: set by the supervisor; EMST supplies none before job analysis.",
  credentialMayBeInvolved: "Credentials that may be involved (agent-drafted link, not a requirement; the credential's issuer was checked against a cited source)",
  credentialPending: "credential gate(s) not shown until the issuer is verified",
  signOffPending: "Not shown until a verified credential or legal basis is attached.",
  gradeNote: "judgment by EMST's federal HR agent, an AI agent; not reviewed by a classifier",
  editorialAttr: "Editorial draft attribute set by the author, not a rated value.",
  moduleTag: "editorial section (not a stewarded module)",
  v1DrawerTitle: "Evidence drawer: v1 prior evidence",
  v1DrawerBody: "These codes were assigned in EMST v1 by one analyst working with an AI assistant. They are prior evidence only: not a v2 assessment, never counted or averaged, and not shown anywhere else in the explorer.",
  v1DrawerChange: "What would change this: blind ratings by practitioners in at least two settings under the v2 exposure codebook, with agreement above the publication threshold.",
  watchSignal: "Not counted as a change indicator: watch signals do not meet the two-family, human-reviewed evidence rule.",
  sourceGrade: "a grade of the source, not a statistic; set by the AI agent that entered the signal and not yet re-graded from the underlying source",
  tooFew: "too few to say",
  noSignal: "\"No signal yet\" is a finding, not a reassurance.",
  stayHuman: "A descriptive \"stays human\" rationale is shown only when it comes from a v2 assessment that passes the display gate.",
  externalContext: "External context: not in this build. Occupation-level external exposure indices are third-party licensed and excluded from release files; task-level external values need a human-reviewed O*NET task crosswalk first. Values are never averaged across indices.",
  countsNotShares: "Counts, not time shares: time shares are job-analysis values and stay hidden until a job analysis confirms them.",
  pathwaysNotice: "Exploratory, never a recommendation. Destinations are computed from draft role profiles: roles named as next steps in this role's profile, roles with a drafted learning pathway, and other roles that share at least half of their target competencies with this one. Not yet observed in real career moves.",
  whatsComingNotice: "Exploratory content. Everything on this page is for foresight and curriculum exploration. None of it is a basis for decisions about jobs or people. Each watch item names what would show it is not forming, and lapses if no new evidence appears by its review date.",
  realignment: "Realignment proposed, not final.",
  venue: "\"Required basis\" means an instrument linked as requiring this work is in force; \"permitted\" means no in-force instrument requires it and it remains lawful; \"no current basis\" means every instrument that required it is inactive. Instruments that only enable or constrain the work never decide the value. \"Indeterminate\" means a linked instrument is withheld from this release, so no value is computed. Values that rest on an instrument record the verification pass has not re-checked are not shown. Shown with no exclusions (the EMST project lead's default).",
  indicatorPlacement: "Indicator placement at a level is a draft until a pre-registered Delphi panel places it (70% modal, IQR at most 1). No indicator here is approved for selection use.",
  scenarioSensitivity: "Demand by scenario (agent-drafted hypothesis, S; not a finding)",
  noRegret: "Moves that EMST's foresight analysis, drafted by an AI agent, judges worthwhile in every scenario. This is an agent-assessed judgment from a desk exercise, not a finding; no practitioner workshop has reviewed it (exploratory).",
};
const TIER_TEXT = { exploratory: "Exploratory: foresight and curriculum exploration; not for decisions", describe: "Describe: workforce analytics, planning, curriculum mapping", develop: "Develop: training, task books, IDPs, self-assessment", select: "Select: hiring and promotion input" };
const CAP_TEXT = { levelRule: "limited by the level rule: indicator levels not yet placed by a panel", evidence: "limited by validation evidence not yet met", declaredCeiling: "limited by the author's declared ceiling", lifecycle: "limited by its lifecycle state", lint: "limited by indicator lint", pathway: "limited by the pathway rule" };
const MATCH_TEXT = { exactMatch: "exact fit", closeMatch: "close fit", broadMatch: "broader {noun}", narrowMatch: "more specific {noun}", relatedMatch: "partial fit" };
const DEPTH_TEXT = { P1: "full profile (corridor role)", P2: "earlier draft at lower depth", P4: "earlier draft at lower depth", P3: "emerging role (What's coming only)" };

// ---------------------------------------------------------------- shard plan
const compsSorted = m.competencies;                                  // A to Z, as the explorer lists them
const COMP_SHARD = 20, TASK_SHARD = 100;
const compShard = new Map(compsSorted.map((c, i) => [c.slug, Math.floor(i / COMP_SHARD)]));
const tasksSorted = [...taskById.values()].sort((a, b) => a.slug.localeCompare(b.slug));
const taskShard = new Map(tasksSorted.map((t, i) => [t.slug, Math.floor(i / TASK_SHARD)]));
const pad = (n) => String(n).padStart(2, "0");

// ---------------------------------------------------------------- role membership of tasks and competencies
const taskRoles = new Map();     // task id -> Map(role slug -> {slug, title, formation})
const addTaskRole = (tid, role, formation) => {
  if (!taskRoles.has(tid)) taskRoles.set(tid, new Map());
  const mm = taskRoles.get(tid);
  const cur = mm.get(role.slug);
  mm.set(role.slug, { slug: role.slug, title: role.title, formation: !!(formation || cur?.formation) });
};
for (const r of rolesMain) for (const b of r.taskBundle) addTaskRole(b.task.id, r, b.formationTask);
for (const v of m.variants) for (const b of v.bundle) addTaskRole(b.task.id, v.role, b.formationTask);
const compRoles = new Map();
for (const r of rolesMain) for (const t of r.competencyTargets) {
  if (!compRoles.has(t.id)) compRoles.set(t.id, []);
  compRoles.get(t.id).push({ slug: r.slug, title: r.title, levels: t.targetLevels });
}

// ---------------------------------------------------------------- task projections
function taskDetail(t) {     // full task record (task shards)
  const v1 = t.v1Prior.length ? {
    lab: m.gateLabels.v1_prior,
    prior: t.v1Prior.map((a) => ({ id: slugOf(a.id), d: a.assessedAt, src: a.source, conf: a.confidence, flags: a.flags, stale: a.stale, vals: a.values })),
    contested: t.v1Contested, reasons: t.v1ContestedReasons,
  } : null;
  return {
    id: t.id, slug: t.slug, stmt: t.statement,
    comps: t.supports.map((s) => ({ slug: compById.get(s.competency)?.slug || slugOf(s.competency), title: s.title, strength: s.strength })),
    roles: [...(taskRoles.get(t.id)?.values() || [])].sort((a, b) => a.title.localeCompare(b.title)),
    wf: gated(t.workFunction, "Task.workFunction"), craft: gated(t.craft, "craft"), exp: gated(t.exposure, "exposure"),
    fieldDependency: t.fieldDependency, formationDependency: t.formationDependency,
    credentialGates: gatesC(t.credentialGates), credentialGatesPending: t.credentialGatesPending,
    signOff: t.signOff, signOffPending: t.signOffPending,
    lc: t.lifecycleState, tier: tierC(t.tier), ev: evC(t.evidence), module: t.module, isModule: t.isModule,
    tools: t.tools.map((x) => ({ id: slugOf(x.id), title: x.title, lc: x.lifecycleState })),
    x2: t.x2.map((r) => xw(r, t.id)), v1,
  };
}
function taskInRole(b) {     // a bundle entry in a role file (contract §2 tasks[])
  const t = b.task;
  return {
    slug: t.slug, stmt: t.statement, formation: b.formationTask, roleLevels: b.roleLevels,
    comps: t.supports.map((s) => ({ slug: compById.get(s.competency)?.slug || slugOf(s.competency), title: s.title, strength: s.strength })),
    wf: gated(t.workFunction, "Task.workFunction"), craft: gated(t.craft, "craft"), exp: gated(t.exposure, "exposure"),
    ja: b.ja.renders ? (() => { throw new Error("job-analysis values now render; extend build-data.mjs"); })() : { p: 1, txt: b.ja.text },
    lc: t.lifecycleState, tier: tierC(t.tier), ev: evC(t.evidence), module: t.module, x2: t.x2.map((r) => xw(r, t.id)),
  };
}

// ---------------------------------------------------------------- HR membership per role
const roleSeries = new Map(), roleClasses = new Map();
const pushTo = (map, k, v) => { if (!map.has(k)) map.set(k, new Map()); map.get(k).set(v.key, { ...map.get(k).get(v.key), ...v }); };
for (const s of m.series) {
  for (const r of s.roleRows) {
    const role = r.role || r.variant?.role;
    if (role && r.closeOrBetter) pushTo(roleSeries, role.id, { key: s.code, code: s.code, title: s.title, close: true });
  }
  for (const pr of s.profile?.roles || []) if (pr.role) pushTo(roleSeries, pr.role.id, { key: s.code, code: s.code, title: s.title, profile: true });
}
for (const c of m.stateClasses) {
  for (const r of c.rows) if (r.variant && r.closeOrBetter) pushTo(roleClasses, r.variant.role.id, { key: c.slug, slug: c.slug, title: c.title, jur: c.jurisdiction, close: true });
  for (const mp of c.view?.mappings || []) if (mp.variant) pushTo(roleClasses, mp.variant.role.id, { key: c.slug, slug: c.slug, title: c.title, jur: c.jurisdiction, view: true });
}
const hrList = (map, id) => [...(map.get(id)?.values() || [])].map(({ key, ...x }) => x);

// ---------------------------------------------------------------- role files
const ref = (id) => {           // role or variant ID -> {slug, title, v?, actor?, wc?}
  if (roleById.has(id)) return roleRef(roleById.get(id));
  const v = variantById.get(id);
  if (v) return { slug: v.role.slug, title: v.role.title, v: v.slug, actor: v.actor, actorLabel: v.actorLabel };
  const p3 = m.roles.find((r) => r.variants.some((x) => x.id === id));
  if (p3) return { slug: p3.slug, title: p3.title, wc: true, actor: p3.variants.find((x) => x.id === id).actor };
  return null;
};
const refs = (ids, where) => {
  const out = [], miss = (ids || []).filter((id) => { const r = ref(id); if (r) out.push(r); return !r; });
  if (miss.length) dropped.push({ where, why: `${miss.length} reference(s) to records not in the view model (held, withheld or not released)` });
  return out;
};
const sameBundle = (v) => {
  const a = v.role.taskBundle, b = v.bundle;
  return a.length === b.length && a.every((x, i) => x.task.id === b[i].task.id && x.formationTask === b[i].formationTask && JSON.stringify(x.roleLevels) === JSON.stringify(b[i].roleLevels));
};
const roleIndex = [];
const roleFiles = [];
for (const r of m.roles) {
  const base = {
    id: r.id, slug: r.slug, title: r.title, alt: r.altLabels, def: r.definition, fn: r.functionStatement,
    wf: r.primaryWorkFunction, wfLabel: r.primaryWorkFunctionLabel, depth: r.depthTier, depthLabel: r.depthLabel,
    lc: r.lifecycleState, tier: tierC(r.tier), ev: evC(r.evidence), module: r.homeModule, isModule: r.isModule,
    whatsComingOnly: r.whatsComingOnly, reviewBy: r.reviewBy, counterSignal: r.counterSignal, horizon: r.horizon,
    scen: r.scenarioSensitivityList.map((x) => ({ code: x.scenario, label: x.label, dir: x.direction })),
  };
  const actors = [...new Set(r.variants.map((v) => v.actorLabel))];
  if (r.whatsComingOnly) {
    // P3 roles appear only in What's coming: exactly the fields that page shows; no bundle, targets or crosswalks.
    const file = { ...base, actors, sectors: r.variants.map((v) => ({ actor: v.actor, actorLabel: v.actorLabel })),
      feeders: (r.feeders || []).map(roleRef), nSignals: r.evidenceSignalIds.length };
    roleFiles.push(file);
    roleIndex.push({ ...base, def: clip(r.definition, 280), actors, nVariants: r.variants.length, scen: undefined, counterSignal: undefined });
    continue;
  }
  const roleTaskIds = new Set(r.taskBundle.map((b) => b.task.id));
  const added = new Map();
  for (const v of r.variants) for (const b of v.bundle) if (!roleTaskIds.has(b.task.id) && !added.has(b.task.id)) added.set(b.task.id, b);
  const signals = new Map();
  const variants = r.variants.map((v) => {
    for (const s of v.change.drivers) signals.set(s.id, s);
    const same = sameBundle(v);
    return {
      id: v.id, slug: v.slug, actor: v.actor, actorLabel: v.actorLabel, subtype: v.subtype, subtypeLabel: v.subtypeLabel,
      authority: v.authorityPosition, authorityLabel: v.authorityPositionLabel, industry: v.industry, ownership: v.ownership,
      delivery: v.deliveryModel, def: v.definition, title: v.title, lc: v.lifecycleState, hr: v.actor === "federal" || v.actor === "state",
      ja: v.bundle[0]?.ja?.renders ? (() => { throw new Error("job-analysis values now render"); })() : { p: 1, txt: TEXT.jaPending },
      credentialGates: gatesC(v.credentialGates), credentialGatesPending: v.credentialGatesPending,
      instruments: [...v.instrumentLinks.typed.map((x) => ({ ...instC(x.i), via: x.via, typed: true })), ...v.instrumentLinks.viaMech.map((x) => ({ ...instC(x.i), via: x.via }))],
      instrumentsMore: v.instrumentLinks.viaMechTotal - v.instrumentLinks.viaMech.length,
      tools: v.tools.map((x) => ({ id: slugOf(x.id), title: x.title, lc: x.lifecycleState })),
      signOff: v.signOff, signOffPending: v.signOffPending, disclaimers: v.disclaimers, jurisdiction: v.jurisdictionalContext,
      grade: v.grade ? { scheme: v.grade.scheme, label: v.grade.label, bands: v.grade.bands } : null,
      tier: tierC(v.tier), ev: evC(v.evidence), crosswalks: v.crosswalks.map((x) => xw(x, v.id)),
      sameTasks: same, tasks: same ? [] : v.bundle.map((b) => ({ slug: b.task.slug, formation: b.formationTask, roleLevels: b.roleLevels })),
      chg: {
        levels: v.levelCounts.map((l) => ({ key: l.key, band: l.band, total: l.total, assessed: l.assessed, pending: l.pending })),
        nTasks: v.change.nTasks, nAssessed: v.change.nAssessed, nFormation: v.change.formation.length,
        emerging: v.change.emerging.map((c) => c.slug), signals: v.change.drivers.map((s) => slugOf(s.id)),
        actorWide: v.change.actorWide, withheld: v.change.withheld, rule: "role-change@0.1.0 (interim; reference implementation in the explorer build)",
      },
      emergingNext: v.emergingNext.map((x) => ({ slug: x.slug, title: x.title, lc: x.lifecycleState })),
      nDest: v.pathways.length,
    };
  });
  const file = {
    ...base, actors, nTasks: r.taskBundle.length, nComps: r.competencyTargets.length, nVariants: r.variants.length,
    levels: r.roleLevels.map((l) => ({ key: l.key, band: l.band })),
    ja: r.ja.renders ? (() => { throw new Error("job-analysis values now render"); })() : { p: 1, txt: r.ja.text },
    crosswalks: r.crosswalks.map((x) => xw(x, r.id)),
    feeders: refs(r.feederRoleIds, `role ${r.slug} feeders`), progressesTo: refs(r.progressesTo, `role ${r.slug} progressesTo`), entryFrom: refs(r.entryFrom, `role ${r.slug} entryFrom`),
    tasks: r.taskBundle.map(taskInRole),
    addedTasks: [...added.values()].map(taskInRole),
    targets: r.competencyTargets.map((t) => ({
      slug: t.competency.slug, title: t.competency.title, type: t.competency.type, levels: t.targetLevels, tier: tierC(t.competency.tier),
      lc: t.competency.lifecycleState, module: t.competency.module, isModule: t.competency.isModule, moduleLabel: t.competency.isModule ? t.competency.moduleLabel : "",
      isDefault: t.competency.lifecycleState === "established" && (!t.competency.isModule || t.competency.module === r.homeModule),
      fed: venueC(t.competency.federal),
    })),
    variants, signals: [...signals.values()].map(signalC),
    hrSeries: hrList(roleSeries, r.id), hrClasses: hrList(roleClasses, r.id),
  };
  roleFiles.push(file);
  roleIndex.push({ id: r.id, slug: r.slug, title: r.title, alt: r.altLabels, def: clip(r.definition, 280), fn: r.functionStatement,
    wf: r.primaryWorkFunction, wfLabel: r.primaryWorkFunctionLabel, depth: r.depthTier, depthLabel: r.depthLabel, lc: r.lifecycleState,
    tier: tierC(r.tier), module: r.homeModule, isModule: r.isModule, actors, variants: r.variants.map((v) => ({ slug: v.slug, actor: v.actor, actorLabel: v.actorLabel })),
    nTasks: r.taskBundle.length, nComps: r.competencyTargets.length, nVariants: r.variants.length, whatsComingOnly: false });
}

// ---------------------------------------------------------------- competency shards
const compDetail = (c) => ({
  id: c.id, slug: c.slug, title: c.title, alt: c.altLabels, def: c.definition, stmt: c.statement, type: c.type, typeLabel: c.typeLabel,
  typeNote: c.gateType.renders ? "" : c.gateType.text, transversalCluster: c.transversalCluster, module: c.module, isModule: c.isModule,
  moduleLabel: c.moduleLabel, subsectors: c.subsectors, span: c.levelSpan ? [c.levelSpan.min, c.levelSpan.max] : null,
  lc: c.lifecycleState, reviewBy: c.reviewBy, status: c.status, tier: tierC(c.tier), ev: evC(c.evidence), protect: c.protect,
  crosswalks: c.crosswalks.map((x) => xw(x, c.id)), tools: c.tools.map((x) => ({ id: slugOf(x.id), title: x.title, lc: x.lifecycleState, halfLife: x.halfLife })),
  venue: c.venue.map(venueC),
  levels: c.levels.map((l) => ({ level: l.level, label: l.label, indicators: l.indicators.map((i) => ({
    id: slugOf(i.id), stmt: i.statement, mode: i.augmentationMode, attr: i.distinguishingAttribute, useClass: i.useClass, methods: i.assessmentMethods,
    tier: tierC(i.tier), ev: evC(i.evidence) })) })),
  ks: c.knowledge.map((k) => ({ id: slugOf(k.id), stmt: k.statement, low: k.lowestLevel, tier: tierC(k.tier), ev: evC(k.evidence) })),
  tasks: c.tasks.map((t) => ({ slug: t.slug, stmt: t.statement, strength: t.supports.find((s) => s.competency === c.id)?.strength || "" })),
  roles: compRoles.get(c.id) || [],
  enactments: c.enactments.map((e) => ({ id: slugOf(e.id), title: e.title, kind: e.kind, actorType: e.actorType, module: e.module, ck: e.craft,
    authorityPosition: e.authorityPosition, note: e.note, basis: e.authorityBasis, principal: e.principal, tier: tierC(e.tier), ev: evC(e.evidence) })),
  v1Codes: c.v1Codes, v1From: c.derivedFrom,
});

// ---------------------------------------------------------------- core indexes
const eutRows = readJson(join(REL, "views", "effective_use_tier.json")).rows;
const eutById = new Map(eutRows.map((r) => [r.id, r]));
const useTierTotals = {};
for (const r of eutRows) useTierTotals[r.effectiveUseTier] = (useTierTotals[r.effectiveUseTier] || 0) + 1;

const bundleGraph = readJson(join(REL, "emst.bundle.jsonld"))["@graph"];
const jfRecs = new Map(bundleGraph.filter((r) => r.type === "JobFamily").map((r) => [r.id, r]));
const jfView = readJson(join(REL, "views", "job_families.json"));
const jobFamilies = jfView.families.map((f) => {
  const rec = jfRecs.get(f.family) || {};
  const title = rec.prefLabel?.en || "", def = rec.definition?.en || "";
  const members = f.members.filter((x) => !x.whatsComing && roleById.has(x.role) && !roleById.get(x.role).whatsComingOnly);
  const wc = f.members.length - members.length;
  if (wc) dropped.push({ where: `job family ${slugOf(f.family)}`, why: `${wc} What's-coming-only (P3) member(s) left out` });
  if (!releasable(title + def)) { dropped.push({ where: `job family ${slugOf(f.family)}`, why: "text matches a Tribal-hold trigger" }); return null; }
  const e = eutById.get(f.family);
  return { id: f.family, slug: slugOf(f.family), title, def, roles: members.map((x) => ({ slug: roleById.get(x.role).slug, basis: x.basis })),
    tier: e ? { t: e.effectiveUseTier, cap: e.bindingCap, dec: e.declaredCeiling } : null, rule: `${f.ruleId}@${f.ruleVersion}` };
}).filter(Boolean);

const saVocab = loadYaml(join(ROOT, "vocab", "sector_actors.yaml"));
const sectorActors = saVocab.terms.filter((t) => m.labels.sectorActor[t.notation]).map((t) => ({
  code: t.notation, label: m.labels.sectorActor[t.notation],
  subtypes: (t.subtypes || []).filter((x) => m.labels.sectorActorSubtype[x.notation] && releasable(x.prefLabel)).map((x) => ({ code: x.notation, label: x.prefLabel })),
  nVariants: m.variants.filter((v) => v.actor === t.notation).length,
}));

const crafts = loadYaml(join(ROOT, "vocab", "crafts.yaml"));
const craftLabel = Object.fromEntries((crafts.terms || []).filter((t) => t.notation && t.prefLabel && releasable(t.prefLabel)).map((t) => [t.notation, t.prefLabel]));

// release gate status (docs/release/<id>/GATE_REPORT.md; read-only)
let gate = null;
{
  const p = join(ROOT, "docs", "release", m.release.id, "GATE_REPORT.md");
  if (existsSync(p)) {
    const md = readFileSync(p, "utf-8");
    const items = [...md.matchAll(/^\|\s*(\d+)\.\s*([^|]+?)\s*\|\s*\*\*([a-z]+)\*\*\s*\|$/gm)].map((x) => ({ n: Number(x[1]), item: x[2].trim(), result: x[3] }));
    const overall = (md.match(/\*\*Overall\.\*\*\s*([^\n]+)/) || [])[1] || "";
    const asOf = (md.match(/\*\*As of\*\*\s*([0-9-]+)/) || [])[1] || "";
    gate = { source: `docs/release/${m.release.id}/GATE_REPORT.md`, asOf, items, overall: overall.trim() };
  }
}
// held count: views/counts.json heldRecords (the release notes state the same count)
const heldN = m.counts.heldRecords;
const notesHeld = (readFileSync(join(REL, "RELEASE_NOTES.md"), "utf-8").match(/reported only as a count:\s*(\d+)/) || [])[1];
if (notesHeld && Number(notesHeld) !== heldN) throw new Error(`held count mismatch: counts.json ${heldN}, RELEASE_NOTES ${notesHeld}`);

const labelsOut = {
  workFunction: m.labels.workFunction, workFunctionDef: m.labels.workFunctionDef, sectorActor: m.labels.sectorActor,
  sectorActorSubtype: m.labels.sectorActorSubtype, authorityPosition: m.labels.authorityPosition, module: m.labels.module,
  competencyType: m.labels.competencyType, level: m.labels.level, levelDescriptors: m.labels.levelDescriptors, attribute: m.labels.attribute,
  useTier: m.labels.useTier, useTierText: TIER_TEXT, capText: CAP_TEXT, lifecycle: m.labels.lifecycle, evidence: m.labels.evidence,
  evidenceDef: m.labels.evidenceDef, reviewStatus: m.labels.reviewStatus, raterType: m.labels.raterType, signalFamily: m.labels.signalFamily,
  reliability: m.labels.reliability, instrumentStatus: m.labels.instrumentStatus, subsector: m.labels.subsector, craft: craftLabel,
  match: MATCH_TEXT, depth: DEPTH_TEXT,
};
// Vocabulary text is guarded like the model guards vocab-sourced text: entries matching a Tribal-hold trigger are left out.
for (const [k, map] of Object.entries(labelsOut)) for (const [code, t] of Object.entries(map)) {
  if (!releasable(code + " " + (typeof t === "string" ? t : JSON.stringify(t)))) { delete map[code]; dropped.push({ where: `labels.${k}.${code}`, why: "text matches a Tribal-hold trigger" }); }
}

const countsOut = { ...m.counts };
// Rating counts by rater type are left out: the explorer does not show them and they describe hidden agent ratings.
for (const k of ["ruleId", "ruleVersion", "buildCommit", "release", "ratingsByRaterType", "ratingUnitsByRaterType"]) delete countsOut[k];
// The `excluded` map names the Tribal hold in a key; that count is carried once, as status.held, with its policy text.
countsOut.excluded = Object.entries(m.counts.excluded || {}).filter(([k]) => releasable(k)).map(([reason, n]) => ({ reason: stripRefs(reason), n }));

const core = {
  release: {
    id: m.release.id, date: m.release.date, commit: m.release.buildCommit, profile: m.release.profile, schemaVersion: m.release.schemaVersion,
    notice: m.release.notice, indigenousStatement: m.release.indigenousStatement, license: m.release.license,
    displayGateRule: m.release.displayGateRule, gatesVersion: m.release.gatesVersion, eutRule: m.release.eutRule, changeRule: m.release.changeRule,
    agreementStudies: m.release.agreementStudies, venueRule: m.venue.rule, venueAsOf: m.venue.asOf, hrStamp: m.hr.stamp,
  },
  status: {
    held: { n: heldN, source: "views/counts.json heldRecords; RELEASE_NOTES.md (Held and deferred)",
      policy: "Content under the project's Tribal content hold is excluded from every build until a Tribal Advisory Council approves it. These pages neither show nor describe it; the release notes give only a count of held records." },
    gate,
  },
  text: TEXT, counts: countsOut, stats: m.stats, useTierTotals,
  figs: Object.fromEntries(Object.entries(m.figures).map(([k, f]) => [k, { tier: tierC(f.tier), ev: { l: f.ev.label, ai: f.ev.isAgentDraft, r: f.ev.reviewStatus } }])),
  labels: labelsOut, gateLabels: m.gateLabels,
  roles: roleIndex,
  comps: compsSorted.map((c) => ({ id: c.id, slug: c.slug, title: c.title, stmt: clip(c.statement || c.definition, 200), type: c.type, typeLabel: c.typeLabel,
    module: c.module, isModule: c.isModule, span: c.levelSpan ? [c.levelSpan.min, c.levelSpan.max] : null, tier: tierC(c.tier), lc: c.lifecycleState,
    ev: { l: c.evidence.label, ai: c.evidence.isAgentDraft, v1: c.evidence.isV1Seed, r: c.evidence.reviewStatus }, v1Codes: c.v1Codes,
    nTasks: c.tasks.length, nRoles: (compRoles.get(c.id) || []).length, gap: m.gapCompetencies.some((g) => g.id === c.id), shard: compShard.get(c.slug) })),
  modules: [{ ns: "core", label: m.labels.module.core || "EMST core", n: m.coreCompetencies.length, core: true },
    ...m.moduleList.map((x) => ({ ns: x.ns, label: x.label, code: x.code, wave: x.wave, n: x.competencies.length }))],
  workFunctions: Object.keys(m.labels.workFunctionDef).map((code) => ({ code, label: m.labels.workFunction[code], def: m.labels.workFunctionDef[code], nRoles: rolesMain.filter((r) => r.primaryWorkFunction === code).length })),
  jobFamilies, sectorActors,
  series: m.series.map((s) => ({ code: s.code, slug: s.slug, title: s.title, status: s.seriesStatus, realignment: s.realignment, group: s.group.replace("Occupational group: ", ""),
    nRows: s.roleRows.length, nClose: s.roleRows.filter((r) => r.closeOrBetter).length,
    nRoles: new Set(s.roleRows.map((r) => (r.role || r.variant?.role)?.id).filter(Boolean)).size, nFed: s.fedVariants.length, generated: !!s.profile })),
  stateClasses: m.stateClasses.map((c) => ({ slug: c.slug, title: c.title, state: c.jurisdiction, jurCode: c.jurisdictionCode, code: c.code,
    nRoles: new Set([...c.rows.map((r) => r.variant?.role.id), ...(c.view?.mappings || []).map((x) => x.variant?.role.id)].filter(Boolean)).size, generated: !!c.view })),
  shards: { comp: Object.fromEntries(compShard), task: Object.fromEntries(taskShard), compSize: COMP_SHARD, taskSize: TASK_SHARD,
    nComp: Math.ceil(compsSorted.length / COMP_SHARD), nTask: Math.ceil(tasksSorted.length / TASK_SHARD) },
};

// ---------------------------------------------------------------- change.js
const usedInstrumentIds = new Set(m.instruments.map((i) => i.id));
const change = {
  notice: TEXT.whatsComingNotice,
  signals: m.signals.map(signalC),
  withheld: { n: m.signalsWithheld.n, rows: m.signalsWithheld.rows, reason: "a signal's headline is itself the claim, so it is not shown until the verification pass re-checks it (claims register)" },
  watchItems: m.watchItems.map((w) => ({ id: w.id, slug: w.slug, title: w.title, lc: w.lifecycleState, reviewBy: w.reviewBy, outcome: w.outcome,
    counter: w.counterSignal, hyp: w.hypothesized ? { type: w.hypothesized.type, label: w.hypothesized.label, stmt: w.hypothesized.statement } : null,
    signals: w.signals.map((s) => slugOf(s.id)), signalsWithheld: w.signalsWithheld, tier: tierC(w.tier), ev: evC(w.evidence) })),
  emergingRoles: m.emergingRoles.map((r) => ({ slug: r.slug, title: r.title, lc: r.lifecycleState, wc: r.whatsComingOnly, fn: r.functionStatement,
    horizon: r.horizon, reviewBy: r.reviewBy, counter: r.counterSignal,
    sectors: r.variants.map((v) => ({ actor: v.actor, actorLabel: v.actorLabel, v: v.whatsComingOnly ? "" : v.slug })),
    feeders: (r.feeders || []).map(roleRef), scen: r.scenarioSensitivityList.map((x) => ({ code: x.scenario, label: x.label, dir: x.direction })),
    nSignals: r.evidenceSignalIds.length, tier: tierC(r.tier), ev: evC(r.evidence) })),
  emergingComps: m.emergingCompetencies.map((c) => ({ slug: c.slug, title: c.title, lc: c.lifecycleState, reviewBy: c.reviewBy, module: c.module, isModule: c.isModule,
    moduleLabel: c.moduleLabel, tier: tierC(c.tier), ev: { l: c.evidence.label, ai: c.evidence.isAgentDraft, r: c.evidence.reviewStatus } })),
  instruments: m.instruments.map(instC),
  instrumentsWithheld: { n: m.instrumentsWithheld.n, rows: m.instrumentsWithheld.rows, reason: "an instrument's name and dated events can carry the claim itself, so this release leaves them out until the verification pass re-checks them" },
  drivers: m.instruments.filter((i) => !i.unverified.length).flatMap((i) => i.events.map((e) => ({ inst: slugOf(i.id), ...eventC(e) })))
    .sort((a, b) => String(a.d || "9999").localeCompare(String(b.d || "9999"))),
  scenarios: {
    axes: m.scenarios.axes.map((a) => ({ code: a.code, label: a.label, poles: a.poles.map((p) => ({ code: p.code, def: p.definition })) })),
    terms: m.scenarios.terms.map((t) => ({ code: t.code, label: t.label, summary: t.summary, risk: t.keyRisk })),
    signposts: m.scenarios.signposts.map((s) => ({ code: s.code, text: s.text, source: s.source, cadence: s.cadence, toward: s.pointsToward,
      signals: s.signals.map((x) => slugOf(x.id)), withheld: s.signalsWithheld })),
    noRegret: m.scenarios.noRegret.map((n) => ({ code: n.code, text: n.text })), noRegretNote: TEXT.noRegret,
    wildcards: m.scenarios.wildcards.map((w) => ({ code: w.code, text: w.text, effect: w.effect })),
  },
  changeIndicators: (() => {
    const rows = [];
    for (const r of m.changeIndicators) {
      if (!releasable(r.targetLabel)) { dropped.push({ where: "change.changeIndicators", why: "a row whose target label matches a Tribal-hold trigger" }); continue; }
      // direction and driver are agent-drafted signal tags and are never shown (site/README.md, "Claims register")
      rows.push({ target: r.targetLabel, role: roleById.get(r.targetId)?.slug || "", kind: r.kind, decision: r.decision, reasons: r.reasons,
        nCounted: (r.counted || []).length, nWatch: (r.watchSignals || []).length });
    }
    return { rule: m.release.changeRule, n: rows.length, moved: rows.filter((r) => r.decision !== "watch").length, rows,
      reasonText: { "ER-0-NOT-ACTIVE": "no signal is active yet (agent-seeded signals stay at watch until a named human reviewer activates them)",
        "ER-1-ONE-FAMILY": "evidence comes from one signal family only; two independent families must point the same way",
        "ER-2-NO-PERSISTENCE": "no second observation period yet", "ER-3-MATCH-TYPE": "crosswalk match too broad", "ER-5-NO-NAMED-REVIEW": "no named human review" } };
  })(),
  figures: { signals: core.figs.signals, watchItems: core.figs.watchItems, instruments: core.figs.instruments, emergingCompetencies: core.figs.emergingCompetencies },
};

// ---------------------------------------------------------------- hr.js
const rowRef = (r) => ({ role: (r.role || r.variant?.role)?.slug || "", v: r.variant?.slug || "", sub: r.subjectLabel, ...xw(r, r.subject) });
const hr = {
  disclaimer: TEXT.hrDisclaimer, pctTimeNote: TEXT.pctTimeNote,
  notes: { series: "A crosswalk row says the role's work is found in positions of this series. It is not a classification determination and claims no alignment with OPM standards. Only rows at closeMatch or stronger are listed by default; the agent confidence is the drafting model's own number and is not calibrated.",
    candidates: "Unreviewed agent candidates (not an alignment): related, broader or narrower matches an AI agent drafted.",
    defaultView: "Only established core competencies (and, in role-scoped views, the role's home-module content) appear in default HR views; module editorial sections and emerging content are left out and counted.",
    credentials: "Credential gates appear only when the credential's issuer has been verified; others are counted, not shown." },
  series: m.series.map((s) => ({
    id: s.id, code: s.code, slug: s.slug, title: s.title, status: s.seriesStatus, realignment: s.realignment, successor: s.realignment ? s.raw.successorSeries || "" : "",
    group: s.group.replace("Occupational group: ", ""), qualStd: s.qualStd, qualVerify: /verify/.test(s.qualStd),
    ped: s.raw.positiveEducationRequirement == null ? "" : s.raw.positiveEducationRequirement ? "yes" : "no",
    pedNote: s.raw.positiveEducationRequirement == null ? "" : "judgment by EMST's federal HR agent, an AI agent; not yet checked against the OPM qualification standard",
    reviewBy: s.reviewBy, notes: s.notes, tier: tierC(s.tier), ev: evC(s.evidence),
    rows: s.roleRows.map(rowRef),
    coreComps: s.coreComps.map((r) => ({ slug: r.competency.slug, title: r.competency.title, rel: r.other.fh_relationship || "", pred: r.predicate, st: r.reviewStatus, fed: venueC(r.competency.federal) })),
    omittedModule: s.omittedModule, omittedNotEstablished: s.omittedNotEstablished,
    fedVariants: s.fedVariants.map((v) => ({ v: v.slug, role: v.role.slug, title: v.role.title, hrTargets: v.hrTargets.map((t) => t.competency.slug) })),
    generated: !!s.profile,
  })),
  generated: m.series.filter((s) => s.profile).map((s) => ({
    code: s.code, stamp: s.profile.stamp, notice: s.profile.evidenceNotice, general: s.profile.generalCompetencies,
    roles: s.profile.roles.map((r) => ({
      role: r.role?.slug || "", v: r.variant?.slug || "", title: r.role?.title || "", depth: r.depth, fn: r.functionStatement,
      x4: r.x4 ? { pred: r.x4.predicate, conf: r.x4.agentConfidence, to: r.x4.appliesTo, st: r.x4.reviewStatus, ev: r.x4.evidence } : null,
      credentialGates: gatesC(r.credentialGates.shown), credentialGatesPending: r.credentialGates.pending,
      instruments: r.instruments.map((i) => ({ id: slugOf(i.id), title: i.title, link: i.linkRoleText, st: i.unverified.length ? "" : i.status, unv: i.unverified, noEv: i.noEvents })),
      home: r.homeModule, homeLabel: r.homeModuleLabel, tier: tierC(r.variant?.tier),
      bands: r.bands.map((b) => ({ group: b.group, band: b.band, roleLevels: b.roleLevels,
        duties: b.duties.map((d) => ({ comp: d.competency.slug, duty: d.duty, isDefault: d.isDefault, isModule: d.competency.isModule,
          moduleLabel: d.competency.isModule ? d.competency.moduleLabel : "", lc: d.competency.lifecycleState, tasks: d.tasks.map((t) => t.task.slug) })),
        // the explorer shows factor-1 knowledge for default (established core or home-module) content only
        factor1: b.factor1.filter((k) => k.isDefault).map((k) => ({ comp: k.competency.slug, stmt: k.statement, knowledge: k.knowledge })),
        factor1NotDefault: b.factor1.filter((k) => !k.isDefault).length })),
    })),
    withoutFed: s.profile.withoutFed.map(roleRef), feeders: s.profile.feeders.map(roleRef),
  })),
  classes: m.stateClasses.map((c) => ({
    id: c.id, slug: c.slug, title: c.title, jur: c.jurisdiction, jurCode: c.jurisdictionCode, code: c.code, scheme: c.scheme, seriesName: c.seriesName,
    agency: c.agency, employerType: c.employerType, level: c.level, supervisory: c.supervisory, specUrl: c.specUrl, specRetrieved: c.specRetrieved,
    specEffective: c.specEffective, mq: c.mq, degreeRule: c.degreeRule, licenses: c.licenses, pay: c.pay, payEffective: c.payEffective,
    appointment: c.appointmentRoute, reviewBy: c.reviewBy, tier: tierC(c.tier), ev: evC(c.evidence),
    rows: c.rows.map(rowRef),
    pending: c.rows.length ? [] : c.pending.map((p) => ({ v: p.variant?.slug || "", title: p.variant?.title || "", key: p.variant ? "" : p.key, level: p.level, match: p.match, conf: p.confidence, close: p.closeOrBetter })),
    view: c.view ? { stamp: c.view.stamp, notice: c.view.evidenceNotice, mappings: c.view.mappings.map((mp) => ({
      v: mp.variant?.slug || "", role: mp.variant?.role.slug || "", roleTitle: mp.roleTitle, actorLabel: mp.variant?.actorLabel || "", depth: mp.depth,
      roleLevels: mp.roleLevels, match: mp.matchType, conf: mp.confidence, review: mp.review, authority: mp.authorityPosition, homeLabel: mp.homeModuleLabel,
      tier: tierC(mp.variant?.tier),
      targets: mp.targets.map((t) => ({ comp: t.competency.slug, title: t.competency.title, levels: t.targetLevels, isDefault: t.isDefault,
        moduleLabel: t.competency.isModule ? t.competency.moduleLabel : "", lc: t.competency.lifecycleState })),
      tasks: mp.tasks.map((t) => t.task.slug), credentialGates: gatesC(mp.credentialGates.shown), credentialGatesPending: mp.credentialGates.pending })) } : null,
  })),
};

// ---------------------------------------------------------------- paths.js
const pe = readJson(join(REL, "views", "pathway_edges.json"));
const shownEdge = new Set();
for (const v of m.variants) for (const g of v.pathways) for (const x of g.variants) shownEdge.add(`${v.id}>${x.v.id}`);
let edgesOut = 0;
const edges = pe.edges.filter((e) => {
  const ok = variantById.has(e.from) && variantById.has(e.to);
  if (!ok) edgesOut++;
  return ok;
}).map((e) => ({
  from: variantById.get(e.from).slug, to: variantById.get(e.to).slug, fromLevel: e.fromLevel, toLevel: e.toLevel,
  shared: { N: e.shared.N, M: e.shared.M }, statement: e.statement, named: e.named, shown: shownEdge.has(`${e.from}>${e.to}`),
  gap: e.gap.filter((g) => compById.has(g.competency)).map((g) => ({ slug: compById.get(g.competency).slug, fromLevel: g.fromLevel, toLevel: g.toLevel })),
  fric: (e.frictions || []).map((f) => ({ type: f.frictionType || f.type, severity: f.severity, direction: f.direction, asOf: f.asOf })),
}));
if (edgesOut) dropped.push({ where: "paths.edges", why: `${edgesOut} release-view edges touch a variant the view model does not show (What's-coming-only P3 roles)` });
const learning = new Map();
for (const v of m.variants) for (const g of v.pathways) for (const l of g.learning) if (!learning.has(l.id)) learning.set(l.id, { id: slugOf(l.id), type: l.type, steps: l.steps, from: v.slug, to: g.toRole.slug });
const paths = {
  notice: "Exploratory, never a recommendation. Pathways are computed from draft role profiles and draft crosswalks. None has been checked against real career moves; observed moves will appear only as counts of at least 5 people from partner data. No pathway is labelled recommended until it passes the project's validation gate.",
  rule: `${pe.ruleId}@${pe.ruleVersion}`, edgeNote: "Compares the origin role's targets at its highest role level with the destination's targets at its first role level. Target levels are editorial drafts (agent-drafted, unreviewed). shown = listed by the explorer (its display rule keeps the top six destination roles per variant).",
  variants: Object.fromEntries(m.variants.map((v) => [v.slug, { role: v.role.slug, title: v.role.title, actor: v.actor, actorLabel: v.actorLabel }])),
  edges,
  translations: m.translations.map((t) => ({ from: t.subjectVariant?.slug || "", fromLabel: t.subjectLabel, to: t.objectVariant?.slug || "", toLabel: t.objectKeyLabel,
    id: t.translationId, ...xw(t, t.subject), obj: undefined, lab: undefined })),
  pathways: [...learning.values()], nPathwayRecords: m.pathwayRecords,
  pathwaysNote: "Exploratory learning pathways drafted by AI agents for some destinations; type and step count only.",
};

// ---------------------------------------------------------------- search.js
const syn = new Map();
const addSyn = (term, exps, src) => {
  const k = String(term || "").trim().toLowerCase();
  if (!k) return;
  const list = (exps || []).map((x) => String(x).trim()).filter((x) => x && x.toLowerCase() !== k);
  if (!list.length) return;
  if (!syn.has(k)) syn.set(k, new Set());
  for (const x of list) syn.get(k).add(x);
};
// automatic: alt labels -> preferred title
for (const r of m.roles) for (const a of r.altLabels) addSyn(a, [r.title]);
for (const c of m.competencies) for (const a of c.altLabels) addSyn(a, [c.title]);
// automatic: crosswalk object labels (OPM series titles, state and local class titles) -> roles crosswalked at closeMatch or better
for (const s of m.series) for (const r of s.roleRows) { const role = r.role || r.variant?.role; if (role && r.closeOrBetter && !role.whatsComingOnly) addSyn(s.title, [role.title]); }
for (const c of m.stateClasses) for (const r of c.rows) if (r.variant && r.closeOrBetter) addSyn(c.title, [r.variant.role.title]);
const autoSyn = syn.size;
// curated
const cur = loadYaml(join(HERE, "synonyms.yaml"));
const seriesTitle = new Map(m.series.map((s) => [s.code, s.title]));
let curated = 0;
for (const row of cur.rows || []) {
  if (row.source !== "editorial (prototype)") throw new Error(`synonyms.yaml: row "${row.term}" lacks source: editorial (prototype)`);
  const exps = [...(row.expansions || [])];
  if (row.kind === "opm-series-nickname") {
    if (!seriesTitle.has(String(row.series))) throw new Error(`synonyms.yaml: series ${row.series} is not in the OPM series register`);
    exps.push(seriesTitle.get(String(row.series)));
  }
  addSyn(row.term, exps); curated++;
}

const docs = [];
const DW = { P1: 1, P2: 0.9, P4: 0.85, P3: 0.6 };
for (const r of m.roles) {
  const codes = new Set();
  if (!r.whatsComingOnly) {
    for (const x of r.crosswalks) if (x.closeOrBetter && !x.noTerm) codes.add(codeOf(x.object));
    for (const v of r.variants) for (const x of v.crosswalks) if (x.closeOrBetter && !x.noTerm && /class|pos:/i.test(x.set + x.object)) { codes.add(codeOf(x.object)); if (labelOf(x.object)) codes.add(labelOf(x.object)); }
  }
  docs.push({ k: "role", s: r.slug, t: r.title, a: r.altLabels, c: [...codes],
    x: clip(r.whatsComingOnly ? `Emerging role (What's coming only). ${r.functionStatement}` : `${r.depthLabel}. ${r.functionStatement}`, 120), w: DW[r.depthTier] || 0.8 });
}
for (const c of m.competencies) docs.push({ k: "comp", s: c.slug, t: c.title, a: c.altLabels, c: c.v1Codes, x: clip(c.isModule ? `${c.typeLabel} · ${c.moduleLabel} editorial section` : c.typeLabel, 120), w: c.isModule ? 0.65 : 0.75 });
// Task documents go to their own file (search-tasks.js, key search:tasks) so each file stays within the size budget.
const taskDocs = tasksSorted.map((t) => ({ k: "task", s: t.slug, t: t.statement, x: clip(t.supports[0]?.title ? `Task · ${t.supports[0].title}` : "Task", 120), w: 0.4 }));
for (const s of m.series) docs.push({ k: "series", s: s.slug, t: `${s.code} ${s.title}`, c: [s.code, `GS-${s.code}`], x: clip(`Federal series · ${s.realignment ? TEXT.realignment : s.seriesStatus}`, 120), w: 0.7 });
for (const c of m.stateClasses) docs.push({ k: "class", s: c.slug, t: c.title, c: [c.code], a: c.seriesName ? [c.seriesName] : [], x: clip(`${c.jurisdiction} · ${c.agency}`, 120), w: 0.6 });
for (const s of m.signals) docs.push({ k: "signal", s: slugOf(s.id), t: s.title, x: clip(`Watch signal · ${s.family} · ${s.targetLabel}`, 120), w: 0.3 });
for (const md of m.moduleList) docs.push({ k: "module", s: md.ns, t: md.label, c: md.code ? [md.code] : [], x: clip(`Module editorial section · ${md.competencies.length} competencies`, 120), w: 0.6 });
// tools and credentials the view model shows (credentials only where the issuer is verified, as "may be involved")
const toolRefs = new Map();
const addTool = (x, kind, slug) => {
  const id = slugOf(x.id);
  if (!toolRefs.has(id)) toolRefs.set(id, { title: x.title, lc: x.lifecycleState, cat: x.category, comps: new Set(), tasks: new Set(), variants: new Set() });
  toolRefs.get(id)[kind].add(slug);
};
for (const c of m.competencies) for (const x of c.tools) addTool(x, "comps", c.slug);
for (const t of tasksSorted) for (const x of t.tools) addTool(x, "tasks", t.slug);
for (const v of m.variants) for (const x of v.tools) addTool(x, "variants", v.slug);
const credRefs = new Map();
const addCred = (g, kind, slug) => {
  const id = "cred-" + slugOf(g.title);
  if (!credRefs.has(id)) credRefs.set(id, { title: g.title, kinds: new Set(), tasks: new Set(), variants: new Set() });
  credRefs.get(id).kinds.add(g.kind); credRefs.get(id)[kind].add(slug);
};
for (const t of tasksSorted) for (const g of t.credentialGates) addCred(g, "tasks", t.slug);
for (const v of m.variants) for (const g of v.credentialGates) addCred(g, "variants", v.slug);
for (const [id, x] of toolRefs) docs.push({ k: "tool", s: id, t: x.title, x: clip(`Tool (dated layer) · ${x.lc}${x.cat ? ` · ${x.cat}` : ""}`, 120), w: 0.4 });
for (const [id, x] of credRefs) docs.push({ k: "credential", s: id, t: x.title, x: clip(`Credential that may be involved (agent-drafted link, not a requirement) · ${x.tasks.size + x.variants.size} places`, 120), w: 0.4 });
const search = {
  docs, taskDocs: "search-tasks.js (key search:tasks) holds the task documents",
  syn: Object.fromEntries([...syn].sort((a, b) => a[0].localeCompare(b[0])).map(([k, s]) => [k, [...s]])),
  synNote: "Expansions are one-way and lower-case-keyed. Automatic entries come from alt labels and from OPM series and state or local class titles linked at closeMatch or better; curated entries are editorial (prototype) vocabulary from tools/synonyms.yaml, not EMST release data.",
  tools: Object.fromEntries([...toolRefs].map(([id, x]) => [id, { title: x.title, lc: x.lc, cat: x.cat, comps: [...x.comps], tasks: [...x.tasks], variants: [...x.variants] }])),
  credentials: Object.fromEntries([...credRefs].map(([id, x]) => [id, { title: x.title, kinds: [...x.kinds], tasks: [...x.tasks], variants: [...x.variants] }])),
};

function parseCsvText(text) {
  const rows = []; let row = []; let cur = ""; let q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; continue; }
    if (c === '"') q = true; else if (c === ",") { row.push(cur); cur = ""; } else if (c === "\n") { row.push(cur); rows.push(row); row = []; cur = ""; } else if (c !== "\r") cur += c;
  }
  if (cur || row.length) { row.push(cur); rows.push(row); }
  const [hd, ...rest] = rows;
  return rest.filter((r) => r.length > 1).map((r) => Object.fromEntries(hd.map((k, i) => [k, r[i] ?? ""])));
}
// ---------------------------------------------------------------- display sanitizer (added by the HCD lead after evaluation round 1)
// Policy texts pass through untouched. Everything else: no sentence may describe held content (the policy says pages
// "neither show nor describe it"), and internal decision or work-package references are removed from free text.
const POLICY = new Set([m.release.indigenousStatement, core?.status?.held?.policy].filter(Boolean));
const HELD_CLAUSE = /[;,]?\s*(?:consultation content held under ADR-0007[^.;]*|agreement types covered by the ADR-0007 hold[^.;]*)/gi;
const sourceIdsUsed = new Set();
const AGENT_CODE = /\b(?:SL|FH|LM|DC|FS|CM|CP|PS|IO|LC|SC|WP|ADR|REG|DISC|TR|V\d)-(?:CAND-)?\d[\w/-]*/g;
// Drafting-agent competency codes in prose ("see PS-C18", "mirror of SL-C03") name a competency the reader can't look up.
// data/v2/ids/seed_map.csv maps each code to its published ID; show the competency's title instead. A code that does
// not resolve to a published competency (merged, retired or not public) becomes "a related competency".
const compTitleById = new Map(m.competencies.map((c) => [c.id, c.title]));
const WORK_CODE_TITLE = new Map();
{
  const seedPath = join(ROOT, "data", "v2", "ids", "seed_map.csv");
  if (existsSync(seedPath)) for (const line of readFileSync(seedPath, "utf-8").split(/\r?\n/).slice(1)) {
    const [key, id] = line.split(",");
    const mm = /^seed:([A-Z]{2}-C\d{2,3}[a-z]?)$/.exec(key || "");
    if (mm && compTitleById.has(id)) WORK_CODE_TITLE.set(mm[1], compTitleById.get(id));
  }
}
const workCodeTitles = (t) => t.replace(/\b([A-Z]{2}-C\d{2,3}[a-z]?)\b/g, (code) => (WORK_CODE_TITLE.has(code) ? `\u201c${WORK_CODE_TITLE.get(code)}\u201d` : "a related competency"));
// Vocabulary labels cut at a comma (release data bug, reported to the data owner): in vocab/*.yaml, an unquoted label
// inside a YAML flow mapping such as {notation: x, prefLabel: City, town or municipality} parses as "City", and the
// rest of the label becomes keys with null values. Rebuild the full label from those keys for display.
const LABEL_FULL = new Map(); // short label -> full label
const LABEL_FULL_BY_NOTATION = new Map(); // notation -> [short, full]
{
  const walk = (o) => {
    if (Array.isArray(o)) return o.forEach(walk);
    if (!o || typeof o !== "object") return;
    const tail = Object.entries(o).filter(([, v]) => v === null).map(([k]) => k);
    if (typeof o.prefLabel === "string" && tail.length) {
      const full = [o.prefLabel, ...tail].join(", ");
      LABEL_FULL.set(o.prefLabel, full);
      if (o.notation) LABEL_FULL_BY_NOTATION.set(String(o.notation), [o.prefLabel, full]);
    }
    Object.values(o).forEach(walk);
  };
  const vdir = join(ROOT, "vocab");
  if (existsSync(vdir)) for (const f of readdirSync(vdir).filter((x) => x.endsWith(".yaml"))) walk(loadYaml(join(vdir, f)));
}
const fullLabel = (str, key) => {
  if ((key === "label" || key === "subtypeLabel" || key === "actorLabel") && LABEL_FULL.has(str)) return LABEL_FULL.get(str);
  const byN = LABEL_FULL_BY_NOTATION.get(key);
  return byN && byN[0] === str ? byN[1] : str;
};
const CODE_KEYS = new Set(["c", "code", "codes", "s", "src", "u", "id", "slug", "ns", "jur", "actor", "k"]);
function scrub(str, key = "") {
  if (POLICY.has(str)) return str;
  str = fullLabel(str, key);
  let t = str.replace(HELD_CLAUSE, "");
  // The explorer's HR disclaimer says "for development and planning", but no record reaches the develop use tier in rc.1.
  // Display override (reported to the explorer's owner): keep the meaning, drop the development claim.
  t = t.replace("This view describes work for development and planning.", "This view describes work. It is not ready for training or development plans.");
  t = t.replace(/\s*\[(?:[^\]]*\b(?:ADR-\d{4}|CR-[A-Z]+-\d+)\b[^\]]*)\]/g, "");
  t = t.replace(/\s*\((?:[^()]*\b(?:ADR-\d{4}|IA-CC-\d+|CR-[A-Z]+-[A-Z0-9-]+)\b[^()]*)\)/g, "");
  // Internal work-item codes of the drafting agents, e.g. "(DB-C49)", "(SL-056)", "core SL-C08".
  t = t.replace(/\s*\((?:core\s+)?(?:CA|DE|LM|FS|FC|DC|SC|DB|FH|SL|PS|IO|LC|CM|IA|CP|AS)-C?\d{2,3}[a-z]?(?:[;,]\s*(?:core\s+)?(?:CA|DE|LM|FS|FC|DC|SC|DB|FH|SL|PS|IO|LC|CM|IA|CP|AS)-C?\d{2,3}[a-z]?)*\)/g, "");
  t = t.replace(/\(core (?:CA|DE|LM|FS|FC|DC|SC|DB|FH|SL|PS|IO|LC|CM|IA|CP|AS)-C\d{2,3}\)/g, "");
  // Lineage pointers inside definitions, e.g. "(v1 1.4.5, DB-C49)", and work-package or translation IDs in brackets.
  t = t.replace(/\s*\(v1 [\d.]+(?:,\s*[A-Z]{2}-C?\d{2,3}[a-z]?)*\)/g, "").replace(/,\s*(?:CA|DE|LM|FS|FC|DC|SC|DB|FH|SL|PS|IO|LC|CM|IA|CP|AS)-C\d{2,3}[a-z]?\b/g, "");
  t = t.replace(/\s*\((?:WP-\d{2}|TR-\d{2})\)/g, "");
  t = t.replace(/\bAbsorbs (?:[A-Z]{2}-C\d{2,3}[a-z]?(?:\s*\([^)]*\))?(?:,\s*|\s+and\s+)?)+\.\s*/g, "");
  t = t.replace(/^ADR-\d{4}:\s*/, "").replace(/\bWP-\d+ derivation\b/g, "derived").replace(/\bdevelopment_stage=(\w+)/g, "development stage: $1");
  // Round 2 (patterns found by developer C): evidence tags such as "[E: SC-009]", agent-team prefixes such as
  // "SL review:", review notes such as "(LC to review; WP-07 record)", "per V2-17" and "(DC Phase 2 extract)".
  t = t.replace(/\s*\(DC Phase \d+ extract\)/g, "").replace(/\s*\([A-Z]{2,3} to review\b[^)]*\)/g, "")
    // Evidence brackets: drop the codes; keep any remaining remark of five words or more, in parentheses.
    .replace(/\s*\[[EJS](?=[;:\]])([^\]]*)\]/g, (_, body = "") => {
      const rest = body.replace(/^\s*;\s*[EJS](?=[:\s]|$)/, "").replace(/^\s*:/, "").replace(AGENT_CODE, "").replace(/\b[A-Z]{2}-C\d{2,3}[a-z]?\b/g, "")
        .replace(/\bWP\d{2}-\d+\b/g, "").replace(/\b[EJS]\b(?=\s*(?:for|;|$))/g, "")
        .replace(/^[\s;,]+|[\s;,]+$/g, "").replace(/\s*[;,]\s*[;,]\s*/g, "; ").replace(/\s{2,}/g, " ");
      return rest.split(/\s+/).filter(Boolean).length >= 5 ? ` (${rest})` : "";
    })
    
    .replace(/^As TR-\d+ for /, "Adapted for ").replace(/\(TR-\d+ names /g, "(its translation rows name ")
    .replace(/\bthe PS reference job architecture\b/g, "the private-sector reference job architecture").replace(/\bRequires PS confirmation\./g, "Requires private-sector review.")
    .replace(/\bcomposed from (?:[A-Z]{2}-(?:CAND-)?C?\d+[a-z]?\s*)+\)/g, "composed from several existing competencies)")
    .replace(/\bmvp_role_set(?: example)?\b/g, "").replace(/\bX9 USA Hire\b/g, "USA Hire").replace(/;\s*WP-\d+ open item \d+/g, "")
    .replace(/(^|\.\s+)(?:SL|FH|SC|PS|LM|FS|CM|CP|IO|LC|IA|DC|FC) review:\s*(\w)/g, (_, pre, c) => pre + c.toUpperCase())
    .replace(/\s*\bper\s+V\d+-\d+\b/g, "");
  // Bare agent work-item codes ("SL-053") in prose only: never in code fields, and never in a value without a space
  // (a state class code could look like one).
  if (/\s/.test(t) && !CODE_KEYS.has(key)) t = workCodeTitles(t).replace(new RegExp("\\s*" + AGENT_CODE.source, "g"), "");
  t = t.replace(/\(\s*[;,]\s*/g, "(").replace(/\s*[;,]\s*\)/g, ")").replace(/\s*\(\s*\)/g, "");
  t = t.replace(/\s+([.;,])/g, "$1").replace(/^[;,]\s*/, "").replace(/\s{2,}/g, " ").trim();
  if (t && !/[.!?)]$/.test(t) && /[.!?]$/.test(str)) t += ".";
  return t;
}
function sanitize(v, k = "") {
  if (typeof v === "string") return k === "id" || k === "slug" ? v : scrub(v, k);
  if (Array.isArray(v)) { if (k === "src") v.forEach((x) => typeof x === "string" && sourceIdsUsed.add(x)); return v.map((x) => sanitize(x, k)); }
  if (v && typeof v === "object") { const o = {}; for (const [kk, vv] of Object.entries(v)) o[kk] = sanitize(vv, kk); return o; }
  return v;
}

// ---------------------------------------------------------------- write
const toJs = (key, value) => {
  const json = JSON.stringify(prune(sanitize(value))).replace(/</g, "\\u003c");
  return `(window.EMSTDATA = window.EMSTDATA || {})[${JSON.stringify(key)}] = ${json};\n`;
};
mkdirSync(OUT, { recursive: true });
// Remove only files this script generates; app/data holds nothing else.
for (const f of readdirSync(OUT)) if (/^(core|search|search-tasks|change|hr|paths|sources|role-.+|comp-\d+|task-\d+)\.js$/.test(f) || f === "manifest.json") rmSync(join(OUT, f));
const written = [];
const write = (name, key, value) => {
  const body = toJs(key, value);
  writeFileSync(join(OUT, name), body, "utf-8");
  written.push({ name, key, raw: Buffer.byteLength(body), gz: gzipSync(body, { level: 9 }).length });
};
write("core.js", "core", core);
for (const f of roleFiles) write(`role-${f.slug}.js`, `role:${f.slug}`, f);
for (let i = 0; i * COMP_SHARD < compsSorted.length; i++) write(`comp-${pad(i)}.js`, `comp:${pad(i)}`, { shard: i, comps: compsSorted.slice(i * COMP_SHARD, (i + 1) * COMP_SHARD).map(compDetail) });
for (let i = 0; i * TASK_SHARD < tasksSorted.length; i++) write(`task-${pad(i)}.js`, `task:${pad(i)}`, { shard: i, tasks: tasksSorted.slice(i * TASK_SHARD, (i + 1) * TASK_SHARD).map(taskDetail) });
write("search.js", "search", search);
write("search-tasks.js", "search:tasks", { docs: taskDocs });
write("change.js", "change", change);
write("hr.js", "hr", hr);
write("paths.js", "paths", paths);
// Source titles for every source ID cited in the exported records, so "About this record" can name and link sources.
{
  const srcRows = new Map();
  const readCsv = (p) => (existsSync(p) ? parseCsvText(readFileSync(p, "utf-8")) : []);
  for (const dir of readdirSync(join(ROOT, "docs", "research"))) for (const r of readCsv(join(ROOT, "docs", "research", dir, "sources.csv"))) if (r.source_id && !srcRows.has(r.source_id)) srcRows.set(r.source_id, { t: r.title, p: r.author_or_publisher, d: r.date_published, u: r.url });
  for (const r of readCsv(join(ROOT, "docs", "research", "_verification", "ALL_key_facts.csv"))) if (r.fact_id) srcRows.set(r.fact_id, { t: r.source_title, p: r.source_publisher, d: r.source_date, u: r.source_url, v: r.verification_status });
  const status = new Map(readCsv(join(ROOT, "docs", "research", "_verification", "ALL_queue_results.csv")).map((r) => [r.item_id, r.verification_status]));
  const claimsLib = await import(pathToFileURL(join(ROOT, "site", "lib", "claims.mjs")).href);
  const rules = claimsLib.parseRegister(claimsLib.parseCsv(readFileSync(join(ROOT, "docs", "methods", "claims_register.csv"), "utf-8")));
  // Same claim rules the verifier applies: withheld phrases of unverified or held register rows, do-not-publish patterns, wrong forms.
  const regRows = claimsLib.parseCsv(readFileSync(join(ROOT, "docs", "methods", "claims_register.csv"), "utf-8"));
  const regMap = yaml.load(readFileSync(join(ROOT, "site", "claims", "register_map.yaml"), "utf-8")).rows || {};
  const withheldPh = regRows.filter((r) => ["unverified", "held"].includes(r.status)).flatMap((r) => (regMap[r.claim_id]?.withheld_phrases || []).map((x) => String(x).toLowerCase()));
  const dnpRx = (yaml.load(readFileSync(join(ROOT, "site", "claims", "do_not_publish.yaml"), "utf-8")).patterns || []).filter((d) => !d.unless_before).map((d) => new RegExp(d.rx, "i"));
  const strictRx = rules.strict.map((w) => new RegExp(claimsLib.phraseRx(w.phrase).source, "i"));
  const out = {};
  for (const id of [...sourceIdsUsed].sort()) {
    const r = srcRows.get(id);
    if (!r) { out[id] = {}; continue; }
    const text = [r.t, r.p].join(" ");
    if (!releasable(text)) { out[id] = { held: 1 }; continue; } // never print a title that trips the content hold
    const all = [r.t, r.p, r.u].join(" ");
    const low = all.toLowerCase();
    if (claimsLib.textViolates(all, rules) || withheldPh.some((w) => low.includes(w)) || dnpRx.some((rx) => rx.test(all)) || strictRx.some((rx) => rx.test(all))) { out[id] = { withheld: 1 }; continue; }
    out[id] = { t: r.t, p: r.p, d: r.d, u: /^https:\/\/[^\s?]+$/.test(r.u || "") ? r.u : undefined, v: r.v || status.get(id) };
  }
  write("sources.js", "sources", { note: "Titles from the repository's research source registers; verification status from the V-pass files where present.", src: out });
}
// The manifest lists the files, keys and sizes in bytes (raw and gzip -9); the verifier reads it; pages do not load it.
writeFileSync(join(OUT, "manifest.json"), JSON.stringify({ release: m.release.id, builtFrom: "site/lib/model.mjs buildModel", files: written.map(({ name, key, raw, gz }) => ({ name, key, raw, gz })) }, null, 1) + "\n");

const tot = written.reduce((s, f) => ({ raw: s.raw + f.raw, gz: s.gz + f.gz }), { raw: 0, gz: 0 });
const report = {
  release: m.release.id, files: written.length, totalRaw: tot.raw, totalGz: tot.gz,
  roles: roleFiles.length, comps: compsSorted.length, tasks: tasksSorted.length, edges: edges.length, searchDocs: docs.length + taskDocs.length,
  synonyms: { total: syn.size, automaticTerms: autoSyn, curatedRows: curated },
  unlabelledObjects: Object.fromEntries([...unlabelled].map(([k, v]) => [k, v.size])), negativeMappingsInSssom: notRows.size, negativeMappingRowsExported: notExported, dropped,
};
writeFileSync(join(UI, "tools", ".build-report.json"), JSON.stringify(report, null, 1) + "\n");
console.log(`[build-data] ${written.length} files, ${(tot.raw / 1024).toFixed(1)} KB raw, ${(tot.gz / 1024).toFixed(1)} KB gzipped; ${roleFiles.length} roles, ${compsSorted.length} competencies, ${tasksSorted.length} tasks, ${edges.length} pathway edges, ${docs.length + taskDocs.length} search docs, ${syn.size} synonym terms`);
for (const d of dropped) console.log(`[build-data] left out: ${d.where}: ${d.why}`);
