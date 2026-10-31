#!/usr/bin/env node
// EMST public-interface prototype: data verification (contract: DATA_CONTRACT.md, "Verification"; docs: docs/DATA.md).
//
// Checks every generated file in app/data/ against the contract and the explorer's governance rules:
//   1. each file is UTF-8 plain JS that registers exactly one JSON value under its key (no functions, `<` escaped);
//   2. sizes against the budget (core.js <= 150 KB gzipped and <= 600 KB raw; any other file <= 120 KB gzipped);
//   3. counts match the view model (roles, competencies, every task it holds);
//   4. every slug a file references resolves to a record in some file;
//   5. a forbidden-content scan over all output (gated values, agentDraft, numeric craft or exposure scores, Tribal-hold
//      trigger terms outside the two policy texts, held seed keys and held v1 codes, e-mail addresses and phone
//      numbers, retired claims, register wrong forms, withheld phrases, judgment-dated event days, unverified records
//      without their flag, recommendation language on pathways);
//   6. a short report to stdout and into docs/DATA.md under "Verification".
// The scan reuses the explorer's own rule sources: schema/lint/governed_content.yaml (Tribal triggers, as
// lib/model.mjs compiles them), site/lib/claims.mjs with docs/methods/claims_register.csv (do_not_say), site/claims/
// do_not_publish.yaml and site/claims/register_map.yaml. The retired-claim regexes (ADR-0027 §3) are copied from
// site/tools/check-output.mjs, which is a script, not a module.
// Exit code 1 on any failure. Run from the repository root:  node prototype/public-ui/tools/verify-data.mjs
// Licence: Apache-2.0.
import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";
import { gzipSync } from "node:zlib";
import vm from "node:vm";

const HERE = dirname(fileURLToPath(import.meta.url));
const UI = resolve(HERE, "..");
const ROOT = resolve(UI, "..", "..");
// `--data <dir>` checks another copy (used to test the checker on seeded violations); the report then goes to stdout only.
const argData = process.argv.indexOf("--data") > 0 ? resolve(process.argv[process.argv.indexOf("--data") + 1]) : null;
const DATA = argData || join(UI, "app", "data");
const DOC = argData ? join(argData, "__no_doc__.md") : join(UI, "docs", "DATA.md");
const require = createRequire(join(ROOT, "site", "package.json"));
const yaml = require("js-yaml");
const { buildModel, slugOf } = await import(pathToFileURL(join(ROOT, "site", "lib", "model.mjs")).href);
const { parseRegister, sentencesOf, conflates, phraseRx, parseCsv } = await import(pathToFileURL(join(ROOT, "site", "lib", "claims.mjs")).href);

const problems = [];
const fail = (rule, where, msg) => problems.push({ rule, where, msg });
const notes = [];

// ---------------------------------------------------------------- 1. parse and register
const manifest = JSON.parse(readFileSync(join(DATA, "manifest.json"), "utf-8"));
const onDisk = readdirSync(DATA).filter((f) => f.endsWith(".js")).sort();
const listed = new Set(manifest.files.map((f) => f.name));
for (const f of onDisk) if (!listed.has(f)) fail("1", f, "file in app/data is not in manifest.json");
const FORMAT = /^\(window\.EMSTDATA = window\.EMSTDATA \|\| \{\}\)\[("(?:[^"\\]|\\.)*")\] = ([\s\S]*);\n$/;
const D = {};             // key -> value
const sizes = [];
for (const { name, key } of manifest.files) {
  const p = join(DATA, name);
  if (!existsSync(p)) { fail("1", name, "listed in manifest.json but missing"); continue; }
  const buf = readFileSync(p);
  const text = buf.toString("utf-8");
  if (!Buffer.from(text, "utf-8").equals(buf)) fail("1", name, "not valid UTF-8");
  if (text.includes("<")) fail("1", name, "raw '<' in file (must be escaped as \\u003c)");
  const mt = text.match(FORMAT);
  if (!mt) { fail("1", name, "does not match the registration format"); continue; }
  let k, value;
  try { k = JSON.parse(mt[1]); value = JSON.parse(mt[2]); } catch (e) { fail("1", name, `payload is not pure JSON: ${e.message}`); continue; }
  if (k !== key) fail("1", name, `registers "${k}", manifest says "${key}"`);
  // Execute it as a page would (script tag): exactly one key, equal to the parsed JSON.
  const sandbox = { window: {} };
  try { vm.runInNewContext(text, sandbox, { timeout: 5000 }); } catch (e) { fail("1", name, `throws when run: ${e.message}`); continue; }
  const keys = Object.keys(sandbox.window.EMSTDATA || {});
  if (keys.length !== 1 || keys[0] !== key) fail("1", name, `registers ${JSON.stringify(keys)}`);
  else if (JSON.stringify(sandbox.window.EMSTDATA[key]) !== JSON.stringify(value)) fail("1", name, "executed value differs from its JSON");
  D[key] = value;
  sizes.push({ name, key, raw: buf.length, gz: gzipSync(buf, { level: 9 }).length });
}

// ---------------------------------------------------------------- 2. sizes
const KB = 1024;
for (const s of sizes) {
  if (s.name === "core.js") {
    if (s.gz > 150 * KB) fail("2", s.name, `gzipped ${(s.gz / KB).toFixed(1)} KB > 150 KB`);
    if (s.raw > 600 * KB) fail("2", s.name, `raw ${(s.raw / KB).toFixed(1)} KB > 600 KB`);
  } else if (s.gz > 120 * KB) fail("2", s.name, `gzipped ${(s.gz / KB).toFixed(1)} KB > 120 KB`);
}
const total = sizes.reduce((a, s) => ({ raw: a.raw + s.raw, gz: a.gz + s.gz }), { raw: 0, gz: 0 });

// ---------------------------------------------------------------- 3. counts against the view model
const meta = JSON.parse(readFileSync(join(ROOT, "site", ".cache", "release-meta.json"), "utf-8"));
const m = buildModel({ root: ROOT, releaseDir: meta.releaseDir, meta });
const core = D.core || {};
const roleFiles = Object.entries(D).filter(([k]) => k.startsWith("role:")).map(([, v]) => v);
const compAll = Object.entries(D).filter(([k]) => k.startsWith("comp:")).flatMap(([k, v]) => v.comps.map((c) => ({ ...c, _shard: Number(k.slice(5)) })));
const taskAll = Object.entries(D).filter(([k]) => k.startsWith("task:") ).flatMap(([k, v]) => v.tasks.map((t) => ({ ...t, _shard: Number(k.slice(5)) })));
const vmTasks = new Set();
for (const c of m.competencies) for (const t of c.tasks) vmTasks.add(t.slug);
for (const r of m.roles) for (const b of r.taskBundle) vmTasks.add(b.task.slug);
for (const v of m.variants) for (const b of v.bundle) vmTasks.add(b.task.slug);
const eqSet = (a, b) => a.size === b.size && [...a].every((x) => b.has(x));
const counts = {
  roles: { files: roleFiles.length, index: (core.roles || []).length, model: m.roles.length },
  comps: { files: compAll.length, index: (core.comps || []).length, model: m.competencies.length },
  tasks: { files: taskAll.length, model: m.stats.tasks, modelProjected: vmTasks.size },
  variants: { files: roleFiles.flatMap((r) => (r.whatsComingOnly ? [] : r.variants || [])).length, model: m.variants.length },
  series: { files: (D.hr?.series || []).length, model: m.series.length, generated: (D.hr?.generated || []).length },
  classes: { files: (D.hr?.classes || []).length, model: m.stateClasses.length, generated: (D.hr?.classes || []).filter((c) => c.view).length },
  signals: { files: (D.change?.signals || []).length, model: m.signals.length, withheld: D.change?.withheld?.n ?? null },
};
if (roleFiles.length !== m.roles.length || counts.roles.index !== m.roles.length) fail("3", "roles", JSON.stringify(counts.roles));
if (!eqSet(new Set(roleFiles.map((r) => r.slug)), new Set(m.roles.map((r) => r.slug)))) fail("3", "roles", "role files differ from the model's roles");
for (const r of roleFiles) if (!D[`role:${r.slug}`]) fail("3", r.slug, "role file key mismatch");
if (compAll.length !== m.competencies.length || counts.comps.index !== m.competencies.length) fail("3", "comps", JSON.stringify(counts.comps));
if (!eqSet(new Set(compAll.map((c) => c.slug)), new Set(m.competencies.map((c) => c.slug)))) fail("3", "comps", "competency shards differ from the model");
if (taskAll.length !== m.stats.tasks || !eqSet(new Set(taskAll.map((t) => t.slug)), vmTasks)) fail("3", "tasks", JSON.stringify(counts.tasks));
if (counts.variants.files !== m.variants.length) fail("3", "variants", JSON.stringify(counts.variants));
if (counts.series.files !== m.series.length || counts.classes.files !== m.stateClasses.length) fail("3", "hr", JSON.stringify({ series: counts.series, classes: counts.classes }));
if (counts.signals.files !== m.signals.length) fail("3", "signals", JSON.stringify(counts.signals));
if (core.status?.held?.n !== m.counts.heldRecords) fail("3", "core.status.held", `held count ${core.status?.held?.n} != ${m.counts.heldRecords}`);

// ---------------------------------------------------------------- 4. references resolve
const R = new Set(roleFiles.map((r) => r.slug));
const V = new Set(roleFiles.flatMap((r) => (r.whatsComingOnly ? [] : (r.variants || []).map((v) => v.slug))));
const C = new Set(compAll.map((c) => c.slug));
const T = new Set(taskAll.map((t) => t.slug));
const S = new Set((D.hr?.series || []).map((s) => s.code));
const K = new Set((D.hr?.classes || []).map((c) => c.slug));
const G = new Set((D.change?.signals || []).map((s) => s.id));
const I = new Set((D.change?.instruments || []).map((i) => i.id));
const M = new Set((core.modules || []).map((x) => x.ns));
const TL = new Set(Object.keys(D.search?.tools || {}));
const CR = new Set(Object.keys(D.search?.credentials || {}));
let refsChecked = 0;
const need = (set, slug, where, what) => { refsChecked++; if (!set.has(slug)) fail("4", where, `${what} "${slug}" does not resolve`); };
const each = (arr, fn) => (arr || []).forEach(fn);
// core
each(core.roles, (r) => { need(R, r.slug, "core.roles", "role"); each(r.variants, (v) => need(V, v.slug, "core.roles", "variant")); });
each(core.comps, (c) => { need(C, c.slug, "core.comps", "competency"); const cc = compAll.find((x) => x.slug === c.slug); if (cc && cc._shard !== c.shard) fail("4", "core.comps", `${c.slug} shard ${c.shard} but found in ${cc._shard}`); });
for (const [s, n] of Object.entries(core.shards?.comp || {})) { need(C, s, "core.shards.comp", "competency"); if (compAll.find((x) => x.slug === s)?._shard !== n) fail("4", "core.shards.comp", `${s} not in comp:${n}`); }
for (const [s, n] of Object.entries(core.shards?.task || {})) { need(T, s, "core.shards.task", "task"); if (taskAll.find((x) => x.slug === s)?._shard !== n) fail("4", "core.shards.task", `${s} not in task:${n}`); }
if (Object.keys(core.shards?.task || {}).length !== T.size) fail("4", "core.shards.task", "does not list every task");
each(core.series, (s) => need(S, s.code, "core.series", "series"));
each(core.stateClasses, (c) => need(K, c.slug, "core.stateClasses", "class"));
each(core.jobFamilies, (f) => each(f.roles, (r) => need(R, r.slug, `core.jobFamilies ${f.slug}`, "role")));
// roles
for (const r of roleFiles) {
  const w = `role:${r.slug}`;
  const own = new Set([...(r.tasks || []), ...(r.addedTasks || [])].map((t) => t.slug));
  for (const k of ["feeders", "progressesTo", "entryFrom"]) each(r[k], (x) => { need(R, x.slug, w, k); if (x.v) need(V, x.v, w, `${k} variant`); });
  for (const t of [...(r.tasks || []), ...(r.addedTasks || [])]) { need(T, t.slug, w, "task"); each(t.comps, (c) => need(C, c.slug, w, "task competency")); }
  each(r.targets, (t) => need(C, t.slug, w, "target"));
  each(r.signals, (s) => need(G, s.id, w, "signal"));
  each(r.hrSeries, (s) => need(S, s.code, w, "hrSeries"));
  each(r.hrClasses, (c) => need(K, c.slug, w, "hrClasses"));
  each(r.variants, (v) => {
    if (!r.whatsComingOnly) need(V, v.slug, w, "variant");
    each(v.tasks, (t) => { need(T, t.slug, w, "variant task"); if (!own.has(t.slug)) fail("4", w, `variant task ${t.slug} has no detail in the role file`); });
    if (!v.sameTasks && !(v.tasks || []).length && !r.whatsComingOnly) fail("4", w, `variant ${v.slug} has neither sameTasks nor tasks`);
    each(v.chg?.emerging, (c) => need(C, c, w, "emerging competency"));
    each(v.chg?.signals, (s) => need(G, s, w, "variant signal"));
    each(v.emergingNext, (x) => need(R, x.slug, w, "emergingNext"));
    each(v.tools, (x) => need(TL, x.id, w, "tool"));
    each(v.instruments, (x) => need(I, x.id, w, "instrument"));
  });
}
// competency and task shards
for (const c of compAll) { each(c.tasks, (t) => need(T, t.slug, `comp ${c.slug}`, "task")); each(c.roles, (x) => need(R, x.slug, `comp ${c.slug}`, "role")); each(c.tools, (x) => need(TL, x.id, `comp ${c.slug}`, "tool")); }
for (const t of taskAll) { each(t.comps, (c) => need(C, c.slug, `task ${t.slug}`, "competency")); each(t.roles, (x) => need(R, x.slug, `task ${t.slug}`, "role")); each(t.tools, (x) => need(TL, x.id, `task ${t.slug}`, "tool")); }
// search
const KIND = { role: R, comp: C, task: T, series: S, class: K, signal: G, tool: TL, credential: CR, module: M };
for (const d of [...(D.search?.docs || []), ...(D["search:tasks"]?.docs || [])]) { if (!KIND[d.k]) fail("4", "search", `unknown kind ${d.k}`); else need(KIND[d.k], d.s, "search.docs", d.k); }
for (const x of Object.values(D.search?.tools || {})) { each(x.comps, (s) => need(C, s, "search.tools", "competency")); each(x.tasks, (s) => need(T, s, "search.tools", "task")); each(x.variants, (s) => need(V, s, "search.tools", "variant")); }
for (const x of Object.values(D.search?.credentials || {})) { each(x.tasks, (s) => need(T, s, "search.credentials", "task")); each(x.variants, (s) => need(V, s, "search.credentials", "variant")); }
// change
const ch = D.change || {};
each(ch.signals, (s) => { if (s.target && !R.has(s.target) && !V.has(s.target)) fail("4", "change.signals", `target ${s.target} does not resolve`); });
each(ch.watchItems, (x) => each(x.signals, (s) => need(G, s, "change.watchItems", "signal")));
each(ch.emergingRoles, (x) => { need(R, x.slug, "change.emergingRoles", "role"); each(x.sectors, (v) => v.v && need(V, v.v, "change.emergingRoles", "variant")); each(x.feeders, (f) => need(R, f.slug, "change.emergingRoles", "feeder")); });
each(ch.emergingComps, (x) => need(C, x.slug, "change.emergingComps", "competency"));
each(ch.scenarios?.signposts, (x) => each(x.signals, (s) => need(G, s, "change.signposts", "signal")));
each(ch.drivers, (x) => need(I, x.inst, "change.drivers", "instrument"));
each(ch.changeIndicators?.rows, (x) => x.role && need(R, x.role, "change.changeIndicators", "role"));
// hr
const hr = D.hr || {};
const rowRefs = (rows, w) => each(rows, (x) => { if (x.role) need(R, x.role, w, "role"); if (x.v) need(V, x.v, w, "variant"); });
each(hr.series, (s) => { rowRefs(s.rows, `hr.series ${s.code}`); each(s.coreComps, (c) => need(C, c.slug, `hr.series ${s.code}`, "competency"));
  each(s.fedVariants, (v) => { need(V, v.v, `hr.series ${s.code}`, "variant"); need(R, v.role, `hr.series ${s.code}`, "role"); each(v.hrTargets, (c) => need(C, c, `hr.series ${s.code}`, "target")); }); });
each(hr.generated, (g) => { need(S, g.code, "hr.generated", "series");
  each(g.roles, (r) => { if (r.role) need(R, r.role, `hr.generated ${g.code}`, "role"); if (r.v) need(V, r.v, `hr.generated ${g.code}`, "variant");
    each(r.bands, (b) => { each(b.duties, (d) => { need(C, d.comp, `hr.generated ${g.code}`, "duty competency"); each(d.tasks, (t) => need(T, t, `hr.generated ${g.code}`, "duty task")); });
      each(b.factor1, (k) => need(C, k.comp, `hr.generated ${g.code}`, "factor-1 competency")); }); });
  each(g.withoutFed, (r) => need(R, r.slug, `hr.generated ${g.code}`, "role")); each(g.feeders, (r) => need(R, r.slug, `hr.generated ${g.code}`, "role")); });
each(hr.classes, (c) => { const w = `hr.classes ${c.slug}`; rowRefs(c.rows, w); each(c.pending, (p) => p.v && need(V, p.v, w, "variant"));
  each(c.view?.mappings, (mp) => { if (mp.v) need(V, mp.v, w, "variant"); if (mp.role) need(R, mp.role, w, "role"); each(mp.targets, (t) => need(C, t.comp, w, "target")); each(mp.tasks, (t) => need(T, t, w, "task")); }); });
// paths
const pa = D.paths || {};
for (const [vs, x] of Object.entries(pa.variants || {})) { need(V, vs, "paths.variants", "variant"); need(R, x.role, "paths.variants", "role"); }
each(pa.edges, (e) => { need(V, e.from, "paths.edges", "from"); need(V, e.to, "paths.edges", "to"); each(e.gap, (g) => need(C, g.slug, "paths.edges", "gap competency")); });
each(pa.translations, (t) => { if (t.from) need(V, t.from, "paths.translations", "from"); if (t.to) need(V, t.to, "paths.translations", "to"); });
each(pa.pathways, (p) => { need(V, p.from, "paths.pathways", "from"); need(R, p.to, "paths.pathways", "to"); });

// ---------------------------------------------------------------- 5. forbidden content
const gc = yaml.load(readFileSync(join(ROOT, "schema", "lint", "governed_content.yaml"), "utf-8"));
const tribal = gc.tribal_hold.triggers.map((p) => (typeof p === "string" ? new RegExp(p, "i") : new RegExp(p.pattern, p.cs ? "" : "i")));
const hold = yaml.load(readFileSync(join(ROOT, "data", "v2", "governance", "tribal_hold.yaml"), "utf-8")) || {};
const heldKeys = hold.heldSeedKeys || [];
const heldRx = heldKeys.length ? new RegExp(`(?<![A-Za-z0-9._/:-])(?:${heldKeys.map((k) => k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})(?![A-Za-z0-9._/-])`) : null;
const heldV1 = new Set((hold.heldV1Codes || []).map(String));
const POLICY_PATHS = new Set(["core.release.indigenousStatement", "core.status.held.policy"]);
const register = parseCsv(readFileSync(join(ROOT, "docs", "methods", "claims_register.csv"), "utf-8"));
const regMap = yaml.load(readFileSync(join(ROOT, "site", "claims", "register_map.yaml"), "utf-8")).rows || {};
const dnp = yaml.load(readFileSync(join(ROOT, "site", "claims", "do_not_publish.yaml"), "utf-8")).patterns || [];
const dns = parseRegister(register);
const wrongForms = [...dns.strict.map((w) => ({ claim: w.claim, rx: new RegExp(phraseRx(w.phrase).source, "i"), strict: true })),
  ...dnp.map((d) => ({ claim: d.claim, rx: new RegExp(d.rx, "i"), unlessBefore: !!d.unless_before }))];
const bundle = JSON.parse(readFileSync(join(meta.releaseDir, "emst.bundle.jsonld"), "utf-8"))["@graph"];
const recTitle = new Map(bundle.filter((r) => r.prefLabel).map((r) => [r.id, r.prefLabel.en || ""]));
const withheldPhrases = [], mappedInstrumentTitles = [], mappedSignalTitles = [], judged = new Set(), judgedStrings = [];
for (const r of register) {
  if (!["unverified", "held"].includes(r.status)) continue;
  const mm = regMap[r.claim_id];
  if (!mm) continue;
  for (const ph of mm.withheld_phrases || []) withheldPhrases.push({ claim: r.claim_id, phrase: ph });
  for (const id of mm.instruments || []) if (recTitle.get(id)) mappedInstrumentTitles.push({ claim: r.claim_id, title: recTitle.get(id) });
  for (const id of mm.signals || []) if (recTitle.get(id)) mappedSignalTitles.push({ claim: r.claim_id, title: recTitle.get(id) });
  for (const lab of mm.events_with_evidence_label || []) for (const e of bundle) if (e.type === "DriverEvent" && (e.evidenceLabel || "S") === lab) {
    judged.add(`${slugOf(e.instrument)}|${e.eventDate}|${e.eventType}`); judgedStrings.push({ claim: r.claim_id, s: `${e.eventDate} ${e.eventType}` });
  }
}
const NEG = /\b(never|not|no|nor|nothing|none|without|until|unless|before|isn't|aren't|cannot|neither)\b/i;
const negated = (text, idx, win = 80) => {
  let before = text.slice(Math.max(0, idx - win), idx);
  const cut = Math.max(before.lastIndexOf(". "), before.lastIndexOf("? "), before.lastIndexOf("! "), before.lastIndexOf("; "), before.lastIndexOf(": "), before.lastIndexOf("\n"));
  if (cut >= 0) before = before.slice(cut + 1);
  return NEG.test(before);
};
// Retired claims (ADR-0027 §3), as in site/tools/check-output.mjs (C06b applies to pathways output only).
const CLAIMS = [
  { id: "C01", rx: /validated against (?:the )?(?:OPM|O\*NET)/gi, msg: "retired claim: validated against OPM/O*NET" },
  { id: "C02", rx: /SAF[- ]accredited/gi, msg: "retired claim: SAF-accredited" },
  { id: "C03", rx: /\b38\s?%[^.]{0,60}human[- ]essential|\bhuman[- ]essential[^.]{0,40}\b38\s?%|\b68\s?%[^.]{0,40}transition|\b77\s?%[^.]{0,80}(?:automat|API)|\b21\s?%[^.]{0,30}of tasks/gi, msg: "retired v1/AEI headline percentage" },
  { id: "C04", rx: /\b(?:215|222|292)\s+competencies\b/gi, msg: "stale v1 competency count" },
  { id: "C05", rx: /\b9 S calls\b|structural property/gi, msg: "retired v1 claim" },
  { id: "C06", rx: /\brecommended (?:pathways?|routes?|moves?|destinations?|careers?|next steps?)\b|\b(?:pathways?|routes?|moves?|destinations?) (?:is|are|was|were) recommended\b/gi, msg: "pathway described as recommended", neg: true },
  { id: "C06b", rx: /\brecommend(?:ed|s|ation)?\b/gi, msg: "recommendation language in pathways data", neg: true, only: "paths" },
  { id: "C07", rx: /UGESP[- ]complian(?:t|ce)/gi, msg: "never describe validation as UGESP compliance" },
  { id: "C08", rx: /SB\s?24-205/gi, msg: "Colorado SB 24-205 cited (never took effect as written)", allowNear: /never took effect|repealed/i },
  { id: "C09", rx: /\brealigned\b|\bconsolidated into\b/gi, msg: "series shown as realigned (only proposed)", neg: true },
  { id: "C10", rx: /usindigenousdata/gi, msg: "domain must never be linked" },
  { id: "C11", rx: /1\s?[–-]\s?5 hours/gi, msg: "unconfirmed PNNL figure" },
  { id: "C12", rx: /\bvalidated (?:competenc\w*|taxonom\w*|indicators?|roles?|role profiles?|pathways?|framework|content|tasks?|profiles?|standards?)\b|\b(?:EMST|taxonomy|competencies|indicators|role profiles|pathways|this release|content)\b[^.]{0,30}\b(?:has|have|is|are|was|were) (?:been )?validated\b|\bvalidated by (?:practitioners|SMEs?|experts|(?:a )?panels?|(?:a )?Delphi)\b/gi, msg: "validation claimed for EMST content", neg: true },
  { id: "C13", rx: /\b(?:aligned|alignment|conforms?) (?:with|to) (?:the )?(?:O\*NET|ESCO|OPM)/gi, msg: "alignment claim without a reviewed set", neg: true },
  { id: "C14", rx: /\bselection[- ]grade\b|\bfor (?:hiring|selection) decisions\b/gi, msg: "selection use claimed", neg: true },
  { id: "C15", rx: /\bPolitical Savvy\b|\bInfluencing\/Negotiating\b/g, msg: "retired ECQ competency named as current", allowNear: /removed|no longer|retired|rewritten|replaced/i },
];
const PERSONAL = [
  { id: "P01", rx: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b/g, msg: "e-mail address" },
  { id: "P02", rx: /\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b/g, msg: "phone number" },
];
const FORBIDDEN_KEYS = new Set(["importance", "timeShare", "critical", "neededAtEntry", "distinguishing", "criticalForSelection", "pctTime", "agentDraft", "obs4", "recommended"]);
// Signals: direction, direction confidence, driver tags and impact are agent drafts and never shown (site/README.md).
const SIGNAL_KEYS = new Set(["id", "title", "family", "status", "about", "target", "sg", "sgTxt", "m", "per", "src", "reviewBy", "sp", "ev", "unv"]);
const hasNumber = (x) => (typeof x === "number" ? true : Array.isArray(x) ? x.some(hasNumber) : x && typeof x === "object" ? Object.entries(x).some(([k, y]) => k !== "p" && hasNumber(y)) : false);
const GATED_KEYS = new Set(["craft", "exp", "exposure", "ja"]);
const V1_KEYS = ["v1 automation type", "v1 career-ladder position", "v1 tacit knowledge density", "v1 horizon", "v1 vector"];
const deferredHits = new Map(dns.deferred.map((d) => [`${d.claim}|${d.phrase}`, { claim: d.claim, phrase: d.phrase, n: 0, example: "" }]));

const seenText = new Map();      // text -> first path (scan each distinct text once per file group)
let stringsScanned = 0, objectsScanned = 0;
function scanText(text, path, fileKey, { blockRules = true } = {}) {
  const ctx = (i, n = 60) => text.slice(Math.max(0, i - n), i + n).replace(/\s+/g, " ");
  const isPaths = fileKey === "paths";
  for (const c of CLAIMS) {
    if (c.only === "paths" && !isPaths) continue;
    if (c.allowNear && !blockRules) { /* object-level pass below */ }
    else if (c.allowNear) continue;           // needs the record's other fields as context: see allowNearCheck
    for (const mt of text.matchAll(c.rx)) {
      if (c.neg && negated(text, mt.index)) continue;
      if (c.allowNear && c.allowNear.test(text.slice(Math.max(0, mt.index - 80), mt.index + 320))) continue;
      fail(`5-${c.id}`, path, `${c.msg}: "…${ctx(mt.index)}…"`);
    }
  }
  for (const w of wrongForms) {
    for (const mt of text.matchAll(new RegExp(w.rx.source, "gi"))) {
      if (w.unlessBefore && NEG.test(text.slice(Math.max(0, mt.index - 20), mt.index))) continue;
      fail("5-wrong-form", path, `${w.claim} wrong form: "…${ctx(mt.index)}…"`);
    }
  }
  if (!blockRules) return;
  const low = text.toLowerCase();
  // Shorter register phrases ('final', 'maintain') are not matched on their own, as in the explorer's checker: the
  // curated patterns in site/claims/do_not_publish.yaml cover them in context.
  for (const s of sentencesOf(text)) for (const c of dns.conflations) if (conflates(s, c)) fail("5-conflation", path, `${c.claim}: "${s.slice(0, 160)}"`);
  for (const w of withheldPhrases) if (low.includes(w.phrase.toLowerCase())) fail("5-withheld", path, `${w.claim} withheld phrase "${w.phrase}"`);
  for (const j of judgedStrings) if (text.includes(j.s)) fail("5-judged-date", path, `${j.claim}: judgment-dated event "${j.s}"`);
  for (const u of mappedSignalTitles) if (u.title && text.includes(u.title)) fail("5-withheld-signal", path, `${u.claim}: withheld signal title appears`);
  for (const p of PERSONAL) for (const mt of text.matchAll(p.rx)) fail(`5-${p.id}`, path, `${p.msg}: ${mt[0]}`);
  if (heldRx && heldRx.test(text)) fail("5-held-key", path, "held seed key present");
  for (const d of deferredHits.values()) if (new RegExp(phraseRx(d.phrase).source, "i").test(text)) { d.n++; d.example ||= path; }
}
// Rules with an allowNear context (C08, C15) are judged against the whole record, as a page renders it with its status.
function allowNearCheck(text, path, context) {
  for (const c of CLAIMS.filter((x) => x.allowNear)) for (const mt of text.matchAll(c.rx)) {
    if (c.allowNear.test(text.slice(Math.max(0, mt.index - 80), mt.index + 320)) || c.allowNear.test(context)) continue;
    fail(`5-${c.id}`, path, `${c.msg}: "…${text.slice(Math.max(0, mt.index - 60), mt.index + 60)}…"`);
  }
}
function tribalCheck(text, path) {
  if (POLICY_PATHS.has(path)) return;
  if (/^search\.hold\[\d+\]\.p$/.test(path)) return; // the trigger patterns themselves, so search can answer them with the held-records statement
  for (const rx of tribal) { const mt = text.match(rx); if (mt) { fail("5-tribal", path, `Tribal-hold trigger "${mt[0]}": "…${text.slice(Math.max(0, mt.index - 50), mt.index + 50)}…"`); return; } }
  // Sentences that describe held content without a trigger word (round 1 T1: "content held under …", "agreement types
  // covered by the … hold route through held competencies"). The policy says pages neither show nor describe it.
  const hd = HELD_DESCRIPTION.exec(text);
  if (hd) fail("5-held-description", path, `Describes held content: "…${text.slice(Math.max(0, hd.index - 50), hd.index + 70)}…"`);
}
const HELD_DESCRIPTION = /\b(?:held (?:competenc\w*|content|enactments?|tasks?|roles?|records? (?:on|about|for|cover))|content (?:is )?held under|hold (?:routes?|covers?|applies to)|(?:routed?|route) through (?:the )?held|covered by the [^.]{0,30}\bhold\b)/i;
const v1Label = D.core?.gateLabels?.v1_prior;
function walk(v, path, fileKey, inV1, context = "") {
  if (typeof v === "string") {
    allowNearCheck(v, path, context);
    stringsScanned++;
    tribalCheck(v, path);
    if (!inV1) for (const k of V1_KEYS) if (v.includes(`${k}`) && !POLICY_PATHS.has(path) && !/^core\.text\./.test(path)) fail("5-v1", path, `v1 code "${k}" outside a task's v1 drawer`);
    const key = `${fileKey === "paths" ? "P" : "A"}|${v}`;
    if (!seenText.has(key)) { seenText.set(key, path); scanText(v, path, fileKey); }
    return;
  }
  if (Array.isArray(v)) { v.forEach((x, i) => walk(x, `${path}[${i}]`, fileKey, inV1, context)); return; }
  if (!v || typeof v !== "object") return;
  objectsScanned++;
  // Object-level text, as a page would render the object's fields together (claims regexes span fields).
  const flat = Object.values(v).filter((x) => typeof x === "string" || typeof x === "number").join(" · ");
  if (flat && !seenText.has(`O|${flat}`) && Object.keys(v).length > 1) { seenText.set(`O|${flat}`, path); scanText(flat, `${path}{…}`, fileKey, { blockRules: false }); }
  for (const [k, x] of Object.entries(v)) {
    const p = `${path}.${k}`;
    tribalCheck(k, `${p} (key)`);
    if (FORBIDDEN_KEYS.has(k)) fail("5-forbidden-key", p, `key "${k}" must never be exported`);
    if (GATED_KEYS.has(k) && !(path.startsWith("core.labels") || path.startsWith("core.text"))) {
      const ok = x && typeof x === "object" && !Array.isArray(x) && x.p === 1 && typeof x.txt === "string" && Object.keys(x).length === 2;
      if (!ok) fail("5-gate", p, `gated value must be {p:1, txt} (got ${JSON.stringify(x).slice(0, 80)})`);
    }
    if (k === "wf" && typeof x === "object" && x && !(x.p === 1 && typeof x.txt === "string" && Object.keys(x).length === 2)) fail("5-gate", p, "work-function value must be gated");
    if (k === "wf" && typeof x === "string" && !/^(WF|MODE)-[A-Z]+$/.test(x)) fail("5-gate", p, `unexpected work-function value ${x}`);
    if (/craft|exposure|^exp$/i.test(k) && !path.startsWith("core.labels") && path !== "core.counts.byType" && hasNumber(x)) fail("5-score", p, "numeric craft or exposure value");
    if (k === "v1") {
      if (!fileKey.startsWith("task:")) fail("5-v1", p, "v1 drawer outside a task shard");
      if (x.lab !== v1Label) fail("5-v1", p, "v1 drawer without the v1_prior label text");
    }
    if ((k === "v1Codes" || k === "v1From") && JSON.stringify(x).match(new RegExp(`(?:^|[^0-9.])(?:${[...heldV1].map((c) => c.replace(/\./g, "\\.")).join("|") || "$^"})(?![0-9])`))) fail("5-held-v1", p, "held v1 code present");
    walk(x, p, fileKey, inV1 || k === "v1", flat);
  }
}
for (const [key, value] of Object.entries(D)) walk(value, key === "core" ? "core" : key, key, false);
// agentDraft may appear only inside the release notice text (it describes where gated drafts live in the bundle).
for (const [key, value] of Object.entries(D)) {
  const s = JSON.stringify(key === "core" ? { ...value, release: { ...value.release, notice: "" } } : value);
  if (s.includes("agentDraft")) fail("5-agentDraft", key, "agentDraft appears outside the release notice");
}
// Unverified instruments render only with their flag; judgment-dated event days never appear as dates.
const unvTitles = mappedInstrumentTitles.map((u) => u.title).filter(Boolean);
let eventsChecked = 0;
function walkObjs(v, path, fn) { if (Array.isArray(v)) v.forEach((x, i) => walkObjs(x, `${path}[${i}]`, fn)); else if (v && typeof v === "object") { fn(v, path); for (const [k, x] of Object.entries(v)) walkObjs(x, `${path}.${k}`, fn); } }
for (const [key, value] of Object.entries(D)) walkObjs(value, key, (o, path) => {
  if (typeof o.title === "string" && unvTitles.some((t) => o.title.includes(t)) && !(o.unv || []).length) fail("5-unverified", path, `"${o.title.slice(0, 60)}" without its unverified flag`);
  if (Array.isArray(o.unv) && o.unv.length && (o.st || (o.ev || []).length)) fail("5-unverified", path, "unverified instrument shows a status or events");
  const inst = o.inst || (Array.isArray(o.ev) && o.id) || null;
  const evs = o.inst ? [o] : Array.isArray(o.ev) ? o.ev.filter((e) => e && typeof e === "object" && "type" in e) : [];
  for (const e of evs) { eventsChecked++; if (e.d && judged.has(`${inst}|${e.d}|${e.type}`)) fail("5-judged-date", path, `judgment-dated event day ${e.d} ${e.type}`); if (e.sup && e.d) fail("5-judged-date", path, "suppressed event carries a date"); }
});
for (const s of [...(D.change?.signals || []), ...roleFiles.flatMap((r) => r.signals || [])]) for (const k of Object.keys(s)) if (!SIGNAL_KEYS.has(k)) fail("5-signal", `signal ${s.id}`, `field "${k}" is not shown by the explorer`);
for (const r of D.change?.changeIndicators?.rows || []) for (const k of ["direction", "driver"]) if (k in r) fail("5-signal", "change.changeIndicators", `field "${k}" is an agent-drafted tag`);
// Pathways: never recommended; the notice must say so.
if (!/never a recommendation/i.test(D.paths?.notice || "")) fail("5-paths", "paths.notice", "notice must say 'never a recommendation'");
// HR disclaimer: the three parts travel with the HR data.
const hrd = (D.hr?.disclaimer || []).join(" ");
if (!(/Not a classification basis/.test(hrd) && /Not a job analysis/.test(hrd) && /Not for RIF/.test(hrd))) fail("5-hr", "hr.disclaimer", "three-part HR disclaimer missing");
// Use tiers: nothing is select (ADR-0015); every role, competency and task carries a tier and an evidence label.
walkObjs(D, "", (o, path) => { if (o.t === "select" && o.cap !== undefined) fail("5-tier", path, "select tier exported"); });
for (const t of taskAll) if (!t.tier?.t || !t.ev?.l) fail("5-badge", `task ${t.slug}`, "missing tier or evidence");
for (const c of compAll) if (!c.tier?.t || !c.ev?.l) fail("5-badge", `comp ${c.slug}`, "missing tier or evidence");
for (const r of roleFiles) if (!r.tier?.t || !r.ev?.l) fail("5-badge", `role ${r.slug}`, "missing tier or evidence");

// ---------------------------------------------------------------- 6. report
const fmt = (n) => (n / KB).toFixed(1);
const byRule = {};
for (const p of problems) byRule[p.rule] = (byRule[p.rule] || 0) + 1;
const ok = problems.length === 0;
const groups = [["core.js", (s) => s.name === "core.js"], ["role-*.js", (s) => s.name.startsWith("role-")], ["comp-NN.js", (s) => s.name.startsWith("comp-")],
  ["task-NN.js", (s) => s.name.startsWith("task-")], ["search.js", (s) => s.name === "search.js"], ["search-tasks.js", (s) => s.name === "search-tasks.js"],
  ["change.js", (s) => s.name === "change.js"], ["hr.js", (s) => s.name === "hr.js"], ["paths.js", (s) => s.name === "paths.js"]];
const lines = [];
lines.push(`Result: **${ok ? "PASS" : "FAIL"}** (${problems.length} problem${problems.length === 1 ? "" : "s"}${ok ? "" : ": " + JSON.stringify(byRule)}). Release ${m.release.id}; verified ${new Date().toISOString().slice(0, 10)} by \`tools/verify-data.mjs\`.`);
lines.push("");
lines.push("| Check | Result |");
lines.push("|---|---|");
lines.push(`| 1. Parse and register | ${sizes.length} files; each registers exactly one key; pure JSON; \`<\` escaped |`);
lines.push(`| 2. Size budget | core.js ${fmt(sizes.find((s) => s.name === "core.js")?.gz || 0)} KB gz / ${fmt(sizes.find((s) => s.name === "core.js")?.raw || 0)} KB raw (≤ 150 / 600); largest other file ${fmt(Math.max(...sizes.filter((s) => s.name !== "core.js").map((s) => s.gz)))} KB gz (≤ 120) |`);
lines.push(`| 3. Counts | roles ${counts.roles.files}/${counts.roles.model}; competencies ${counts.comps.files}/${counts.comps.model}; tasks ${counts.tasks.files}/${counts.tasks.model}; variants ${counts.variants.files}/${counts.variants.model}; series ${counts.series.files}/${counts.series.model} (${counts.series.generated} generated profiles); classes ${counts.classes.files}/${counts.classes.model} (${counts.classes.generated} generated views); signals ${counts.signals.files}/${counts.signals.model} (${counts.signals.withheld} withheld); held records ${core.status?.held?.n} |`);
lines.push(`| 4. References resolve | ${refsChecked} references checked |`);
lines.push(`| 5. Forbidden content | ${stringsScanned} strings and ${objectsScanned} objects scanned (${seenText.size} distinct texts); ${eventsChecked} dated events checked; rules: gated keys, agentDraft, craft/exposure scores, ${tribal.length} Tribal-hold triggers, ${heldKeys.length} held seed keys, ${heldV1.size} held v1 codes, e-mail/phone, ${CLAIMS.length} retired-claim rules, ${wrongForms.length} register and do-not-publish wrong forms, ${dns.conflations.length} conflation rules, ${withheldPhrases.length} withheld phrases, ${judged.size} judgment-dated events, ${unvTitles.length} unverified instrument titles |`);
lines.push("");
lines.push("| File | Raw KB | Gzipped KB |");
lines.push("|---|---:|---:|");
for (const [label, f] of groups) {
  const xs = sizes.filter(f);
  if (!xs.length) continue;
  const raw = xs.reduce((a, s) => a + s.raw, 0), gz = xs.reduce((a, s) => a + s.gz, 0);
  const extra = xs.length > 1 ? ` (${xs.length} files; largest ${fmt(Math.max(...xs.map((s) => s.gz)))} KB gz)` : "";
  lines.push(`| ${label}${extra} | ${fmt(raw)} | ${fmt(gz)} |`);
}
lines.push(`| **Total (${sizes.length} files)** | **${fmt(total.raw)}** | **${fmt(total.gz)}** |`);
const deferred = [...deferredHits.values()].filter((d) => d.n);
if (deferred.length) { lines.push(""); lines.push(`Deferred register phrases (double-quoted in the register; reported, not enforced, as in the explorer): ${deferred.map((d) => `${d.claim} "${d.phrase}" in ${d.n} text(s), e.g. ${d.example}`).join("; ")}.`); }
if (!ok) { lines.push(""); lines.push("Problems (first 40):"); lines.push(""); for (const p of problems.slice(0, 40)) lines.push(`- \`${p.rule}\` ${p.where}: ${p.msg}`); }
const reportMd = lines.join("\n");
console.log(reportMd.replace(/\*\*/g, ""));
if (existsSync(DOC)) {
  const doc = readFileSync(DOC, "utf-8");
  const START = "<!-- verification:start -->", END = "<!-- verification:end -->";
  if (doc.includes(START) && doc.includes(END)) writeFileSync(DOC, doc.slice(0, doc.indexOf(START) + START.length) + "\n" + reportMd + "\n" + doc.slice(doc.indexOf(END)));
  else console.log("[verify-data] note: docs/DATA.md has no verification markers; report not written there");
}
process.exit(ok ? 0 : 1);
