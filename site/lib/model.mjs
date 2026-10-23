// EMST explorer view model (WP-12). Turns one EMST release build (bundle + computed views) into the data the page
// templates render. Rules this file enforces, so templates cannot get them wrong:
//
//  * Only records in the release bundle exist here; the release gate has already removed held, third-party-licensed,
//    quarantined and placeholder records. A second Tribal-trigger filter guards text taken from vocab/.
//  * Gated values render only when views/display_gate.json says production or tentative (fail closed). Everything
//    else shows IO's fallback label (validation/display_gates.yaml#labels), never the value. LLM craft ratings and
//    agent work-function values therefore never render.
//  * v1 analyst values (raterType v1-analyst) are exposed only as `v1Prior` on tasks, for the evidence drawer.
//  * Effective use tier comes from views/effective_use_tier.json; never from the record's declared ceiling alone.
//  * Federal applicability comes from the computed venue view, never from records (ADR-0016 §4; WP-05 note).
//  * Module records are flagged `isModule` so HR views (Federal Series Profile, State Class View, default lists)
//    can leave them out (ADR-0018).
// Licence: Apache-2.0.
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import yaml from "js-yaml";
import { parseRegister, textViolates } from "./claims.mjs";

export const USE_TIERS = ["exploratory", "describe", "develop", "select"];
const TIER_RANK = Object.fromEntries(USE_TIERS.map((t, i) => [t, i]));
export const minTier = (...ts) => ts.filter(Boolean).sort((a, b) => TIER_RANK[a] - TIER_RANK[b])[0] || "exploratory";

const EV_ORDER = { S: 0, J: 1, E: 2 };
const EV_TEXT = { S: "Speculation", J: "Expert judgment", E: "Evidence" };
// Badge data for a figure computed over records: lowest effective use tier and weakest evidence label among them.
export function figureOf(items) {
  const xs = (items || []).filter(Boolean);
  const tier = minTier(...xs.map((i) => i.tier?.tier));
  const worst = xs.map((i) => i.evidence?.label || "S").sort((a, b) => EV_ORDER[a] - EV_ORDER[b])[0] || "S";
  return {
    tier: { tier, source: "lowest tier among the records counted" },
    ev: { label: worst, labelText: EV_TEXT[worst] || worst, isAgentDraft: xs.some((i) => i.evidence?.isAgentDraft),
      isV1Seed: false, reviewStatus: xs.length && xs.every((i) => (i.evidence?.reviewStatus || "unreviewed") === "unreviewed") ? "unreviewed" : "mixed review status" },
  };
}

export function en(v) {
  if (v == null) return "";
  if (typeof v === "string") return v;
  if (Array.isArray(v)) return v.map(en).join("; ");
  if (typeof v === "object") return v.en ?? Object.values(v)[0] ?? "";
  return String(v);
}
export function enList(v) {
  if (!v) return [];
  if (Array.isArray(v)) return v.map(en);
  if (typeof v === "object") { const x = v.en ?? Object.values(v)[0]; return Array.isArray(x) ? x : x ? [x] : []; }
  return [String(v)];
}
export function slugOf(id) {
  return String(id).replace(/^seed:/, "").replace(/^emst:[a-z0-9-]+\//, "").replace(/^https?:\/\/[^/]+\//, "")
    .toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}
const parseOther = (s) => Object.fromEntries(String(s || "").split(";").filter((x) => x.includes("=")).map((x) => {
  const i = x.indexOf("="); return [x.slice(0, i).trim(), x.slice(i + 1).trim()];
}));

function loadYaml(p) { return yaml.load(readFileSync(p, "utf-8")); }
function loadJson(p, fallback = null) { return existsSync(p) ? JSON.parse(readFileSync(p, "utf-8")) : fallback; }
function parseCsv(text) {
  const rows = []; let row = []; let cur = ""; let q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; continue; }
    if (c === '"') q = true; else if (c === ",") { row.push(cur); cur = ""; } else if (c === "\n") { row.push(cur); rows.push(row); row = []; cur = ""; } else if (c !== "\r") cur += c;
  }
  if (cur || row.length) { row.push(cur); rows.push(row); }
  const [h, ...rest] = rows;
  return rest.filter((r) => r.length > 1).map((r) => Object.fromEntries(h.map((k, i) => [k, r[i] ?? ""])));
}

export function buildModel({ root, releaseDir, meta }) {
  const bundle = loadJson(join(releaseDir, "emst.bundle.jsonld"));
  const graph = bundle["@graph"];
  const manifest = graph.find((r) => r.type === "Release") || {};
  const records = new Map();
  const mappings = [];
  for (const r of graph) {
    if (r.type === "Release") continue;
    if (r.type === "Mapping") mappings.push(r); else if (r.id) records.set(r.id, r);
  }
  const byType = (t) => [...records.values()].filter((r) => r.type === t);
  const views = join(releaseDir, "views");

  // ---------------------------------------------------------------- governed-content guard for vocab-sourced text
  const gc = loadYaml(join(root, "schema", "lint", "governed_content.yaml"));
  const triggers = gc.tribal_hold.triggers.map((p) => typeof p === "string" ? new RegExp(p, "i") : new RegExp(p.pattern, p.cs ? "" : "i"));
  const releasable = (s) => !triggers.some((rx) => rx.test(String(s || "")));

  // ---------------------------------------------------------------- vocab labels
  const V = (f) => loadYaml(join(root, "vocab", f));
  const wf = V("work_functions.yaml"), sa = V("sector_actors.yaml"), ap = V("authority_positions.yaml"), mods = V("modules.yaml");
  const ct = V("change_types.yaml"), lc = V("lifecycle_states.yaml"), ev = V("evidence_labels.yaml"), sc = V("scenarios.yaml");
  const pl = V("proficiency_levels.yaml"), dm = V("driver_mechanisms.yaml"), cty = V("competency_types.yaml"), subs = V("subsectors.yaml");
  const labels = {
    workFunction: Object.fromEntries([...wf.terms, ...(wf.modes?.terms || [])].map((t) => [t.notation, t.prefLabel])),
    workFunctionDef: Object.fromEntries(wf.terms.map((t) => [t.notation, t.definition])),
    sectorActor: Object.fromEntries(sa.terms.filter((t) => t.notation !== "tribal").map((t) => [t.notation, t.prefLabel])),
    sectorActorSubtype: Object.fromEntries(sa.terms.filter((t) => t.notation !== "tribal").flatMap((t) => (t.subtypes || []).map((x) => [x.notation, x.prefLabel]))),
    authorityPosition: Object.fromEntries(ap.terms.map((t) => [t.notation, t.prefLabel])),
    module: Object.fromEntries([[mods.core.namespace, mods.core.prefLabel], ...mods.terms.map((t) => [t.namespace, t.prefLabel])]),
    moduleWave: Object.fromEntries(mods.terms.map((t) => [t.namespace, t.wave])),
    moduleCode: Object.fromEntries(mods.terms.map((t) => [t.namespace, t.notation])),
    competencyType: Object.fromEntries(cty.terms.map((t) => [t.notation, t.prefLabel])),
    level: Object.fromEntries(pl.terms.filter((t) => t.isLevel !== false).map((t) => [t.notation, t.prefLabel])),
    levelDescriptors: Object.fromEntries(pl.terms.filter((t) => t.descriptors).map((t) => [t.notation, t.descriptors])),
    attribute: Object.fromEntries(pl.attributes.map((a) => [a.notation, a.prefLabel])),
    roleLevelBand: Object.fromEntries(pl.role_level_bands.map((b) => [b.key, b.band])),
    useTier: Object.fromEntries(lc.use_tiers.values.map((t) => [t.notation, t.definition])),
    lifecycle: Object.fromEntries((lc.lifecycle_states || []).map((t) => [t.notation, t.meaning || t.prefLabel])),
    evidence: Object.fromEntries(ev.evidence_labels.map((t) => [t.notation, t.prefLabel])),
    evidenceDef: Object.fromEntries(ev.evidence_labels.map((t) => [t.notation, t.definition])),
    reviewStatus: Object.fromEntries(ev.review_statuses.map((t) => [t.notation, t.definition])),
    raterType: Object.fromEntries(ev.rater_types.map((t) => [t.notation, t.definition])),
    signalFamily: Object.fromEntries(ct.signal_families.values.map((t) => [t.notation, t.definition])),
    reliability: Object.fromEntries(ct.signal_reliability.values.map((t) => [t.notation, t.definition])),
    instrumentStatus: Object.fromEntries(dm.instrument_statuses.values.map((t) => [t.notation, t.definition])),
    mechanism: Object.fromEntries(dm.terms.map((t) => [t.notation, t.definition])),
    mechanismName: Object.fromEntries(dm.terms.map((t) => [t.notation, String(t.prefLabel || t.notation).replace(/-/g, " ")])),
    instrumentLinkRole: Object.fromEntries((dm.instrument_link_roles?.values || []).map((t) => [t.notation, t.definition])),
    subsector: Object.fromEntries(flattenSubsectors(subs).map((t) => [t.notation, t.prefLabel])),
  };
  function flattenSubsectors(d) {
    const out = [];
    const walk = (xs) => { for (const t of xs || []) { if (t && t.notation) out.push(t); walk(t.subsectors); walk(t.terms); } };
    walk(d.terms); walk(d.clusters);
    return out;
  }
  const gates = loadYaml(join(root, "validation", "display_gates.yaml"));
  // WP-15 claims register (docs/methods/claims_register.csv) and CP's map to records (site/claims/register_map.yaml):
  // records tied to unverified rows render as "Unverified — not for citation"; held rows never render.
  const claims = { rows: new Map(), byInstrument: new Map(), bySignal: new Map(), suppressEventLabels: new Set(), noEventRow: null, signoff: null };
  {
    const regPath = join(root, "docs", "methods", "claims_register.csv");
    const mapPath = join(root, "site", "claims", "register_map.yaml");
    if (existsSync(regPath)) for (const r of parseCsv(readFileSync(regPath, "utf-8"))) claims.rows.set(r.claim_id, r);
    const map = existsSync(mapPath) ? loadYaml(mapPath) : { rows: {} };
    for (const [id, m] of Object.entries(map.rows || {})) {
      const row = claims.rows.get(id);
      if (!row || !["unverified", "held"].includes(row.status)) continue;      // re-verified rows stop suppressing
      for (const i of m.instruments || []) { if (!claims.byInstrument.has(i)) claims.byInstrument.set(i, []); claims.byInstrument.get(i).push(id); }
      for (const g of m.signals || []) { if (!claims.bySignal.has(g)) claims.bySignal.set(g, []); claims.bySignal.get(g).push(id); }
      for (const l of m.events_with_evidence_label || []) claims.suppressEventLabels.add(l);
      if (m.events_with_evidence_label) claims.eventRow = id;
      if (m.instruments_without_events) claims.noEventRow = id;
    }
    claims.signoff = existsSync(join(root, "docs", "methods", "WP15_SIGNOFF.md")) ? "docs/methods/WP15_SIGNOFF.md" : null;
  }
  // Register wrong forms (lib/claims.mjs, shared with tools/check-output.mjs): strict phrases and "mixing ..." items.
  const dnsRules = parseRegister([...claims.rows.values()]);
  const gateLabels = gates.labels;

  // ---------------------------------------------------------------- computed views
  const dgv = loadJson(join(views, "display_gate.json"), { header: {}, rows: [] });
  const gate = new Map();                              // recordId -> field -> row
  for (const r of dgv.rows) {
    if (!gate.has(r.recordId)) gate.set(r.recordId, {});
    gate.get(r.recordId)[r.field] = r;
  }
  const eutv = loadJson(join(views, "effective_use_tier.json"), { header: {}, rows: [] });
  const eut = new Map(eutv.rows.map((r) => [r.id, r]));
  const stale = new Map((loadJson(join(views, "assessment_staleness.json"), []) || []).map((r) => [r.assessment, r.stale]));
  const civ = loadJson(join(views, "change_indicators.json"), { header: {}, rows: [] });
  const inv = new Map((loadJson(join(views, "inverse_links.json"), []) || []).filter((r) => r.competency).map((r) => [r.competency, r]));
  const counts = loadJson(join(views, "counts.json"), {});
  const agreementIndex = loadJson(join(views, "agreement", "index.json"), { studies: [] });

  // ---------------------------------------------------------------- venue / federal applicability (computed view)
  const venue = { source: meta?.venue?.source || "unavailable", asOf: meta?.venue?.asOf || null, rows: [], rule: null };
  if (venue.source === "release-view" || venue.source === "rule-over-release") {
    const v = loadJson(meta.venue.path, []);
    venue.rule = Array.isArray(v) ? null : `${v.header?.ruleId}@${v.header?.ruleVersion}`;
    if (!venue.asOf && !Array.isArray(v)) venue.asOf = v.header?.asOf || null;
    venue.rows = (Array.isArray(v) ? v : (v.rows || [])).map((r) => {
      const insts = (r.deciding || []).map((x) => x.instrument);
      if (insts.some((i) => claims.byInstrument.has(i))) return { ...r, venueApplicability: "not-shown-unverified", basisLinked: false, withheld: true };
      return r;
    });
  } else if (venue.source === "wp05-prototype" && existsSync(meta.venue.path)) {
    // CR-CP-001 ruling A1: the prototype over-reads rescissions, so it may not show "required-basis"; it shows
    // "basis not yet linked" instead until venue-applicability@1.0.0 ships in the release.
    venue.rows = parseCsv(readFileSync(meta.venue.path, "utf-8")).map((r) => {
      const linked = r.basisLinked === "True" || r.basisLinked === "true";
      // WP-15 sign-off: a value that rests on an instrument whose register row is unverified is not shown.
      const insts = String(r.instruments || "").split("|").map((x) => x.split("=")[0]).filter(Boolean);
      if (insts.some((i) => claims.byInstrument.has(i))) return { ...r, venueApplicability: "not-shown-unverified", basisLinked: false, withheld: true };
      return r.venueApplicability === "required-basis" ? { ...r, venueApplicability: "basis-not-yet-linked", basisLinked: false, withheld: true } : { ...r, basisLinked: linked };
    });
  }
  const venueBy = new Map();
  for (const r of venue.rows) {
    if (r.sectorActor === "tribal" || !records.has(r.competency)) continue;   // held content never enters a view
    if (!venueBy.has(r.competency)) venueBy.set(r.competency, []);
    venueBy.get(r.competency).push({ actor: r.sectorActor, value: r.venueApplicability, asOf: r.asOf, basisLinked: !!r.basisLinked,
      basisVerified: r.basisVerified !== false, requires: (r.deciding || []).map((x) => x.instrument) });
  }

  // ---------------------------------------------------------------- shared helpers
  const stripRefs = (t) => (t == null ? t : String(t).replace(/\s*\((?:ADR-\d|SPEC §|CR-[A-Z]+-\d)[^)]*\)/g, ""));
  const release = {
    id: manifest.emstRelease || meta?.version || "unknown",
    profile: meta?.profile || "release",
    isPreview: (meta?.profile || "release") !== "release",
    schemaVersion: manifest.schemaVersion, date: manifest.released, buildCommit: manifest.buildCommit,
    // Reader-facing text: internal decision references such as "(ADR-0012 I-2; ADR-0024)" are left out (package review
    // issue 6); the release notes in the download keep them.
    notice: stripRefs(manifest.notice), indigenousStatement: stripRefs(manifest.indigenousKnowledgeStatement),
    license: manifest.license, buildOk: meta?.buildOk !== false, warning: meta?.warning || null,
    displayGateRule: `${dgv.header.ruleId}@${dgv.header.ruleVersion}`, gatesSha256: dgv.header.gatesSha256, gatesVersion: gates.version || "",
    agreementStudies: agreementIndex.studies || [], eutRule: `${eutv.header.ruleId}@${eutv.header.ruleVersion}`,
    changeRule: `${civ.header.ruleId}@${civ.header.ruleVersion}`,
  };

  function evidenceOf(r) {
    const p = r.provenance || {};
    const label = r.evidenceLabel || p.evidenceLabel || "S";
    return {
      label, labelText: labels.evidence[label] || label, method: p.method || "unknown",
      reviewStatus: p.reviewStatus || r.reviewStatus || "unreviewed", generatedAt: (p.generatedAt || "").slice(0, 10),
      agents: (p.agent || []).join(", "), sources: [...new Set([...(p.sources || []), ...(r.sources || [])].filter((s) => typeof s === "string"))],
      validationStatus: r.validationStatus || null,
      isAgentDraft: ["llm-assisted", "lexical-linker"].includes(p.method),
      isV1Seed: r.validationStatus === "seed-v1",
    };
  }
  function tierOf(r) {
    const e = eut.get(r.id);
    if (e) return { tier: e.effectiveUseTier, source: "computed", bindingCap: e.bindingCap, declared: e.declaredCeiling, rule: release.eutRule };
    const lifecycleCap = { watch: "exploratory", proposed: "exploratory", emerging: "develop" }[r.lifecycleState];
    return { tier: minTier(r.useTier || "exploratory", lifecycleCap || r.useTier || "exploratory"), source: "declared", bindingCap: lifecycleCap ? "lifecycle" : "declaredCeiling", declared: r.useTier || null, rule: null };
  }
  function gateFor(id, field) {
    const g = gate.get(id)?.[field];
    if (!g) return { decision: "hidden", label: "assessment_pending", text: gateLabels.assessment_pending, renders: false };
    const renders = g.decision === "production" || g.decision === "tentative";
    const text = g.decision === "editorial" ? "Editorial classification (not a rated value)" : (gateLabels[g.label] || gateLabels.assessment_pending);
    return { decision: g.decision, label: g.label, text, renders, reason: g.reason || "" };
  }
  const mappingsBySubject = new Map();
  for (const m of mappings) {
    if (!mappingsBySubject.has(m.subject_id)) mappingsBySubject.set(m.subject_id, []);
    mappingsBySubject.get(m.subject_id).push(m);
  }
  function crosswalkRow(m) {
    const o = parseOther(m.other);
    return {
      set: m.mapping_set_id, predicate: m.predicate_id, object: m.object_id, objectLabel: m.object_label || "",
      justification: m.mapping_justification, confidence: m.confidence || "", date: m.mapping_date || "",
      reviewStatus: o.review_status || o.review || "unreviewed", raterType: o.rater_type || (String(m.mapping_justification).includes("LLM") ? "llm" : ""),
      evidence: o.evidence || o.evidence_label || "", comment: m.comment || "", noTerm: m.object_id === "sssom:NoTermFound",
      reviewed: /MappingReview|ManualMappingCuration/.test(m.mapping_justification || "") && !/candidate|unreviewed/.test(o.review_status || ""),
      other: o, objectSourceVersion: m.object_source_version || "",
    };
  }

  // Link role of a typed instrument link (vocab/driver_mechanisms.yaml#instrument_link_roles), in plain words.
  const LINK_ROLE_TEXT = { requires: "requires this work", enables: "enables this work", constrains: "constrains this work", "removed-requirement": "removed an earlier requirement for this work" };
  const linkRoleText = (r) => LINK_ROLE_TEXT[r] || `linked as "${String(r).replace(/-/g, " ")}"`;

  // "R10-environmental-review-specialist/private" -> "Environmental review specialist (private)"
  function keyLabel(k) {
    const [role, actor] = String(k || "").split("/");
    const t = role.replace(/^R\d+-/, "").replace(/-/g, " ");
    return t ? t.charAt(0).toUpperCase() + t.slice(1) + (actor ? ` (${labels.sectorActor[actor] || actor})` : "") : "";
  }

  // ---------------------------------------------------------------- tools, credentials, instruments
  const tools = byType("Tool");
  const toolsByCompetency = new Map(), toolsByTask = new Map();
  for (const t of tools) {
    for (const c of t.servesCompetencies || []) { if (!toolsByCompetency.has(c)) toolsByCompetency.set(c, []); toolsByCompetency.get(c).push(t); }
    for (const c of t.servesTasks || []) { if (!toolsByTask.has(c)) toolsByTask.set(c, []); toolsByTask.get(c).push(t); }
  }
  const toolVM = (t) => ({ id: t.id, title: en(t.prefLabel), lifecycleState: t.lifecycleState, category: t.category || t.toolType || "", reviewBy: t.reviewBy || "", halfLife: t.expectedHalfLifeYears ?? null });
  const credTitle = (id) => en(records.get(id)?.prefLabel) || id;
  // SPEC §10.5 rule 8: credential gates and sign-off authority are verified facts; without a verified source they are not shown.
  const credVerified = (id) => { const iv = records.get(id)?.issuerVerified; return iv?.verified === true && Array.isArray(iv.sources) && iv.sources.length > 0; };
  const gatesOf = (gs) => {
    const all = (gs || []).filter((g) => g && g.credential);
    // Even when the issuer is verified, the link between this work and the credential is an agent draft: shown as a
    // "may be involved" note, never as a requirement (coordinator ruling; SPEC §10.5 rule 8).
    const shown = all.filter((g) => credVerified(g.credential)).map((g) => ({ kind: g.kind, title: credTitle(g.credential) }));
    return { shown, pending: all.length - shown.length };
  };
  const signOffOf = (so) => {
    if (!so || !so.kind) return { shown: null, pending: false };
    const creds = so.credentials || [];
    return creds.length && creds.every(credVerified) ? { shown: so.kind, pending: false } : { shown: null, pending: true };
  };

  // ---------------------------------------------------------------- v1 prior evidence (drawer only)
  const V1_AUTO = { A: "Augmentation", Ac: "Compressive augmentation", H: "Human-essential", S: "Substitution", V: "Supervision" };
  const V1_CAREER = { P: "Primary learning (0–5 yr)", C: "Contributing (3–8 yr)", X: "Peripheral or specialist (8+ yr)" };
  const V1_VECTOR = { AI: "Artificial intelligence", Ro: "Physical robotics", Cv: "Convergent (both)", "—": "None recorded" };
  const V1_HORIZON = { 1: "Deployed now", 2: "3–5 years", 3: "5–10+ years", N: "No automation trajectory" };
  const v1ByTask = new Map();
  for (const a of byType("ExposureAssessment")) {
    if (a.raterType !== "v1-analyst" || !a.task) continue;
    const vals = a.v1Values || {};
    const row = {
      id: a.id, assessedAt: a.assessedAt || "", source: a.method || "", confidence: a.confidence || "low",
      flags: a.v1Flags || [], stale: stale.get(a.id) === true,
      values: [
        vals.auto_type && ["v1 automation type", `${vals.auto_type} (${V1_AUTO[vals.auto_type] || "?"})`],
        vals.tacit_density && ["v1 tacit knowledge density", vals.tacit_density],
        vals.career_ladder && ["v1 career-ladder position", `${vals.career_ladder} (${V1_CAREER[vals.career_ladder] || "?"})`],
        vals.vector && ["v1 vector", `${vals.vector} (${V1_VECTOR[vals.vector] || "?"})`],
        vals.horizon && ["v1 horizon", `${vals.horizon} (${V1_HORIZON[vals.horizon] || "?"})`],
      ].filter(Boolean),
      autoType: vals.auto_type || null,
    };
    if (!v1ByTask.has(a.task)) v1ByTask.set(a.task, []);
    v1ByTask.get(a.task).push(row);
  }
  for (const rows of v1ByTask.values()) rows.sort((a, b) => a.source.localeCompare(b.source));

  // ---------------------------------------------------------------- indicators, tasks, competencies
  const indicators = new Map(byType("Indicator").map((i) => [i.id, i]));
  const indicatorVM = (i) => ({
    id: i.id, level: i.level, statement: en(i.statement), augmentationMode: i.augmentationMode || "", useClass: i.useClass || "",
    obs4: i.obs4 ?? null, assessmentMethods: i.assessmentMethods || [], tier: tierOf(i), evidence: evidenceOf(i),
    distinguishingAttribute: i.distinguishingAttribute ? (labels.attribute[i.distinguishingAttribute] || i.distinguishingAttribute) : "",
  });

  const taskVMs = new Map();
  function taskVM(id) {
    if (taskVMs.has(id)) return taskVMs.get(id);
    const t = records.get(id);
    if (!t || t.type !== "Task") return null;
    const v1 = v1ByTask.get(id) || [];
    const autoTypes = new Set(v1.map((x) => x.autoType).filter(Boolean));
    const contestedFlags = new Set(v1.flatMap((x) => x.flags).filter((f) => ["text_misaligned", "d2_divergent", "normative_h", "pre15a_hybrid"].includes(f)));
    const vm = {
      id, slug: slugOf(id), anchor: `task-${slugOf(id)}`, statement: en(t.statement) || en(t.prefLabel),
      supports: (t.supports || []).map((s) => ({ competency: s.competency, strength: s.strength })),
      workFunction: gateFor(id, "Task.workFunction"),
      craft: gateFor(id, "craft.FC").renders || gateFor(id, "craft.DC").renders || gateFor(id, "craft.SC").renders
        ? { renders: true } : { renders: false, text: gateLabels.assessment_pending },
      exposure: { renders: false, text: gateLabels.assessment_pending },          // no v2 multi-rater exposure study yet
      fieldDependency: t.fieldDependency || "", formationDependency: t.formationDependency || "",
      credentialGates: gatesOf(t.credentialGates).shown, credentialGatesPending: gatesOf(t.credentialGates).pending,
      signOff: signOffOf(t.signOffAuthority).shown || "", signOffPending: signOffOf(t.signOffAuthority).pending,
      lifecycleState: t.lifecycleState || "", status: t.status,
      tier: tierOf(t), evidence: evidenceOf(t), module: t.module, isModule: t.module !== "core",
      tools: (toolsByTask.get(id) || []).map(toolVM),
      v1Prior: v1, v1Contested: autoTypes.size > 1 || contestedFlags.size > 0,
      v1ContestedReasons: [...(autoTypes.size > 1 ? ["v1 records disagree on automation type"] : []), ...[...contestedFlags].map((f) => `v1 flag: ${f}`)],
      x2: (mappingsBySubject.get(id) || []).filter((m) => m.mapping_set_id.startsWith("onet-task")).map(crosswalkRow),
    };
    // Exposure: a v2 value renders only if some exposure dimension passes the gate (none before the S2 studies).
    const g = gate.get(id) || {};
    const passing = Object.values(g).filter((r) => r.field.startsWith("exposure.") && (r.decision === "production" || r.decision === "tentative"));
    if (passing.length) vm.exposure = { renders: true, rows: passing };
    taskVMs.set(id, vm);
    return vm;
  }

  const ksBy = new Map();
  for (const k of byType("KnowledgeStatement")) {
    for (const c of k.supports || []) { if (!ksBy.has(c)) ksBy.set(c, []); ksBy.get(c).push({ id: k.id, statement: en(k.statement), lowestLevel: k.lowestLevel || "", tier: tierOf(k), evidence: evidenceOf(k) }); }
  }
  const LIVE = new Set(["draft", "candidate", "published", "deprecated"]);
  const compRecs = byType("Competency").filter((c) => LIVE.has(c.status));
  const competencies = [];
  const compById = new Map();
  for (const c of compRecs) {
    const il = inv.get(c.id) || { tasks: [], enactments: [] };
    const levels = (c.levels || []).map((l) => ({
      level: l.level, label: labels.level[l.level] || l.level,
      indicators: (l.indicators || []).map((iid) => indicators.get(iid)).filter(Boolean).map(indicatorVM),
    }));
    const enactments = (il.enactments || []).map((e) => records.get(typeof e === "string" ? e : e.enactment || e.id)).filter(Boolean).map((e) => ({
      id: e.id, title: en(e.prefLabel), kind: e.enactmentKind, actorType: e.actorType || "", module: e.enactedInModule || e.module,
      craft: e.craft || "", authorityPosition: e.authorityPosition || "", note: en(e.note), evidence: evidenceOf(e), tier: tierOf(e),
      authorityBasis: en(e.authorityBasis), principal: en(e.principal),
    }));
    const tasks = (il.tasks || []).map((x) => taskVM(typeof x === "string" ? x : x.task)).filter(Boolean);
    const cw = (mappingsBySubject.get(c.id) || []).filter((m) => !m.mapping_set_id.startsWith("emst-v1")).map(crosswalkRow);
    const vm = {
      id: c.id, slug: slugOf(c.id), url: `/competencies/${slugOf(c.id)}/`, title: en(c.prefLabel), altLabels: enList(c.altLabel),
      definition: en(c.definition), statement: en(c.statement), type: c.competencyType || "", typeLabel: labels.competencyType[c.competencyType] || "Not yet typed",
      transversalCluster: c.transversalCluster || "", module: c.module, homeModule: c.homeModule || c.module, isModule: c.module !== "core",
      moduleLabel: labels.module[c.module] || c.module, subsectors: (c.subsectors || []).map((s) => ({ code: s, label: labels.subsector[s] || s })),
      levelSpan: c.levelSpan || null, levels, tasks, enactments, lifecycleState: c.lifecycleState || "", reviewBy: c.reviewBy || "",
      status: c.status, tier: tierOf(c), evidence: evidenceOf(c), protect: c.protect || null,
      v1Codes: (c.notation || []).filter((n) => n.scheme === "EMSTv1").map((n) => n.value),
      derivedFrom: ((c.provenance || {}).derivedFrom || []).map((d) => ({ key: d.v1Key, relation: d.relation })),
      crosswalks: cw, tools: (toolsByCompetency.get(c.id) || []).map(toolVM), knowledge: ksBy.get(c.id) || [],
      venue: (venueBy.get(c.id) || []).sort((a, b) => a.actor.localeCompare(b.actor)),
      federal: (venueBy.get(c.id) || []).find((v) => v.actor === "federal") || null,
      gateType: gateFor(c.id, "Competency.competencyType"),
    };
    competencies.push(vm);
    compById.set(c.id, vm);
  }
  competencies.sort((a, b) => a.title.localeCompare(b.title));
  for (const t of taskVMs.values()) t.supports = t.supports.map((s) => ({ ...s, title: compById.get(s.competency)?.title || "", url: compById.get(s.competency)?.url || "" }));

  // ---------------------------------------------------------------- roles (WP-08), variants, pathways, frictions
  const roleRecs = byType("RoleProfile").filter((r) => LIVE.has(r.status));
  const variantRecs = byType("RoleVariant").filter((r) => LIVE.has(r.status) && r.sectorActor !== "tribal");
  const pathwayRecs = byType("Pathway").filter((r) => LIVE.has(r.status));
  const frictionRecs = byType("FrictionRecord");
  const signals = byType("ChangeSignal");
  const sigField = (s, f) => s[f] ?? (s.notation || []).find((n) => n.scheme === `EMST-${f}`)?.value ?? null;

  // display-gate@1.1.0 (CR-CP-001 B4): importance, timeShare, critical and neededAtEntry (bundle) and importance,
  // distinguishing, criticalForSelection (targets) are job-analysis values. They render only from validationStatus
  // >= reviewed with a pid: reviewer; in the Federal Series Profile and State Class View, timeShare and importance only
  // from job-analysis-confirmed. Bundle membership, role levels, formationTask and target levels are editorial design
  // values: shown, labelled "editorial draft (agent-drafted, unreviewed)".
  const VS_ORDER = ["seed-v1", "draft", "reviewed", "panel-retained", "job-analysis-confirmed", "criterion-supported"];
  function jaGate(rec) {
    const vs = rec?.validationStatus || "draft";
    const reviewer = rec?.provenance?.reviewer || rec?.provenance?.reviewedBy || rec?.reviewer || "";
    const human = /^pid:/.test(String(Array.isArray(reviewer) ? reviewer[0] : reviewer));
    const i = VS_ORDER.indexOf(vs);
    return { renders: human && i >= VS_ORDER.indexOf("reviewed"), hrRenders: human && i >= VS_ORDER.indexOf("job-analysis-confirmed"), status: vs,
      text: "Assessment pending (job analysis)" };
  }
  let currentJa = { renders: false, hrRenders: false, status: "draft", text: "Assessment pending (job analysis)" };
  function bundleItem(b) {
    const t = taskVM(b.task);
    if (!t) return null;
    const ja = currentJa;
    return { task: t, formationTask: !!b.formationTask, roleLevels: b.roleLevels || [], ja,
      importance: ja.renders ? b.importance ?? null : null, timeShare: ja.renders ? b.timeShare ?? null : null,
      critical: ja.renders ? !!b.critical : null, neededAtEntry: ja.renders ? !!b.neededAtEntry : null };
  }
  // Profile depth (RoleProfile notation MVPtier), in plain words for readers.
  const DEPTH_TEXT = { P1: "full profile (corridor role)", P2: "earlier draft at lower depth", P4: "earlier draft at lower depth", P3: "emerging role (What's coming only)" };
  const roles = [];
  const roleById = new Map();
  for (const r of roleRecs) {
    currentJa = jaGate(r);
    const vm = {
      id: r.id, slug: slugOf(r.id), url: `/roles/${slugOf(r.id)}/`, title: en(r.prefLabel), altLabels: enList(r.altLabel),
      functionStatement: en(r.functionStatement), definition: en(r.definition),
      primaryWorkFunction: r.primaryWorkFunction || "", primaryWorkFunctionLabel: labels.workFunction[r.primaryWorkFunction] || r.primaryWorkFunction || "",
      roleLevels: (r.roleLevels || []).map((l) => ({ key: l.key, band: l.levelBand })),
      taskBundle: (r.taskBundle || []).map(bundleItem).filter(Boolean),
      competencyTargets: (r.competencyTargets || []).map((t) => ({ competency: compById.get(t.competency) || null, id: t.competency, targetLevels: t.targetLevels || {},
        importance: currentJa.renders ? t.importance ?? null : null, distinguishing: currentJa.renders ? !!t.distinguishing : null })).filter((t) => t.competency),
      ja: currentJa,
      lifecycleState: r.lifecycleState || "", reviewBy: r.reviewBy || "", counterSignal: en(r.counterSignal), horizon: r.horizon || "",
      scenarioSensitivity: r.scenarioSensitivity || null, evidenceSignals: r.evidenceSignals || [], feederRoles: (r.feederRoles || []).map((f) => f.role),
      entryFrom: r.entryFrom || [], progressesTo: r.progressesTo || [], homeModule: r.homeModule || "core", isModule: (r.homeModule || "core") !== "core",
      status: r.status, tier: tierOf(r), evidence: evidenceOf(r), variants: [],
      depthTier: (r.notation || []).find((n) => n.scheme === "MVPtier")?.value || "",
      horizonLabel: r.horizon || "", scenarioSensitivityList: Object.entries(r.scenarioSensitivity || {}).map(([k, v]) => ({ scenario: k, label: (sc.terms || []).find((t) => t.notation === k)?.prefLabel || "", direction: v })),
      feederRoleIds: (r.feederRoles || []).map((f) => f.role), evidenceSignalIds: r.evidenceSignals || [],
      crosswalks: (mappingsBySubject.get(r.id) || []).map(crosswalkRow),
    };
    vm.depthLabel = DEPTH_TEXT[vm.depthTier] || "depth not recorded";
    vm.whatsComingOnly = vm.depthTier === "P3";            // coordinator ruling: P3 roles appear only in "What's coming"
    if (vm.whatsComingOnly) vm.url = `/whats-coming/#${vm.slug}`;
    roles.push(vm);
    roleById.set(r.id, vm);
  }
  // RoleVariant.indicativeGradeOrBand: {scheme, byRoleLevel: {entry: "GS-3 to GS-5", ...}, label} (current), or
  // {scheme, band, label} / a plain string (older shapes). Bands are listed in the role's level order.
  function gradeOf(g, role) {
    if (!g) return null;
    if (typeof g === "string") return { scheme: "", label: "", bands: [{ level: "", band: g }] };
    const order = (role?.roleLevels || []).map((l) => l.key);
    const rank = (k) => (order.indexOf(k) < 0 ? 99 : order.indexOf(k));
    const bands = g.byRoleLevel && typeof g.byRoleLevel === "object"
      ? Object.entries(g.byRoleLevel).filter(([, b]) => b).sort((a, b) => rank(a[0]) - rank(b[0])).map(([level, band]) => ({ level, band: String(band) }))
      : g.band ? [{ level: "", band: String(g.band) }] : [];
    return bands.length ? { scheme: g.scheme || "", label: g.label || "", bands } : null;
  }
  const variants = [];
  for (const v of variantRecs) {
    const role = roleById.get(v.variantOf);
    if (!role) continue;
    if (role.whatsComingOnly) { role.variants.push({ id: v.id, actor: v.sectorActor, actorLabel: labels.sectorActor[v.sectorActor] || v.sectorActor, whatsComingOnly: true }); continue; }
    currentJa = jaGate(v);
    const drops = new Set(v.taskDrops || []);
    const overrides = new Map((v.taskOverrides || []).map((b) => [b.task, b]));
    const bundle = [
      ...role.taskBundle.filter((b) => !drops.has(b.task.id)).map((b) => overrides.has(b.task.id) ? (bundleItem({ ...overrides.get(b.task.id) }) || b) : b),
      ...(v.taskAdds || []).map(bundleItem).filter(Boolean),
    ];
    const actor = v.sectorActor;
    const slice = v.id.split("/").slice(2).join("/");          // e.g. seed:R37-.../private/applicant-preparer
    const vm = {
      id: v.id, slug: `${role.slug}--${slugOf(v.id.split("/").slice(1).join("-") || actor)}`, role, actor, actorLabel: (labels.sectorActor[actor] || actor) + (slice ? ` (${slice.replace(/[-/]/g, " ")})` : ""),
      subtype: v.sectorActorSubtype || "", subtypeLabel: labels.sectorActorSubtype[v.sectorActorSubtype] || v.sectorActorSubtype || "", authorityPosition: v.authorityPosition || "", authorityPositionLabel: labels.authorityPosition[v.authorityPosition] || v.authorityPosition || "",
      industry: v.industry || "", ownership: v.ownership || "", deliveryModel: v.deliveryModel || "", definition: en(v.definition), title: en(v.prefLabel) || `${role.title} (${labels.sectorActor[actor] || actor})`,
      // Typed instrument links ({instrument, role, note}; ADR-0030); a bare ID string is the pre-typing shape.
      bundle, instruments: (v.instruments || []).map((x) => {
        const id = typeof x === "string" ? x : x?.instrument || x?.id || null;
        if (!id) return null;
        return { id, role: typeof x === "object" ? x.role || "" : "", note: typeof x === "object" ? en(x.note) : "", title: en(records.get(id)?.prefLabel) || id };
      }).filter(Boolean),
      credentialGates: gatesOf(v.credentialGates).shown, credentialGatesPending: gatesOf(v.credentialGates).pending,
      signOff: signOffOf(v.signOffAuthority).shown || "", signOffPending: signOffOf(v.signOffAuthority).pending,
      tools: (v.toolsCommonlyRequired || []).map((t) => records.get(t)).filter(Boolean).map(toolVM),
      grade: gradeOf(v.indicativeGradeOrBand, role), jurisdictionalContext: v.jurisdictionalContext || [], disclaimers: v.disclaimers || [],
      lifecycleState: v.lifecycleState || role.lifecycleState, status: v.status, tier: tierOf(v), evidence: evidenceOf(v),
      crosswalks: (mappingsBySubject.get(v.id) || []).map(crosswalkRow),
    };
    vm.hrTargets = role.competencyTargets.filter((t) => t.competency.lifecycleState === "established" && (!t.competency.isModule || t.competency.module === role.homeModule));
    vm.url = `/roles/${role.slug}/${slugOf(v.id.split("/").slice(1).join("-") || actor)}/`;
    vm.gapUrl = `/gap-check/${role.slug}/${slugOf(v.id.split("/").slice(1).join("-") || actor)}/`;
    vm.pathwaysUrl = `/pathways/${role.slug}/${slugOf(v.id.split("/").slice(1).join("-") || actor)}/`;
    vm.emergingNext = [...(role.progressesTo || [])].map((id) => roleById.get(id)).filter((r) => r && r.whatsComingOnly);
    role.variants.push(vm);
    variants.push(vm);
  }
  for (const r of roles) r.variants.sort((a, b) => a.actor.localeCompare(b.actor));
  for (const r of roles) if (r.whatsComingOnly) {
    r.feeders = r.feederRoleIds.map((id) => roleById.get(id)).filter(Boolean);
  }
  roles.sort((a, b) => a.title.localeCompare(b.title));
  const variantById = new Map(variants.map((v) => [v.id, v]));

  // Role change summary per variant (computed at build time from release records; ADR-0027 §1 View 1)
  for (const v of variants) {
    // role-change@0.1.0 summary: per role level, bundle tasks by assessment status (N of M). No time shares
    // (display-gate@1.1.0 job_analysis_rule; CR-CP-001 B4).
    v.levelCounts = v.role.roleLevels.map((l) => {
      const at = v.bundle.filter((b) => !b.roleLevels.length || b.roleLevels.includes(l.key));
      const assessed = at.filter((b) => b.task.exposure.renders).length;
      return { key: l.key, band: l.band, total: at.length, assessed, pending: at.length - assessed };
    });
    const totalShare = v.bundle.reduce((s, b) => s + (b.timeShare || 0), 0);
    const assessed = v.bundle.filter((b) => b.task.exposure.renders);
    v.change = {
      nTasks: v.bundle.length, nAssessed: assessed.length, totalShare,
      shareAssessed: assessed.reduce((s, b) => s + (b.timeShare || 0), 0),
      shareByAssessment: [
        { key: "pending", label: "Assessment pending (no v2 multi-rater assessment)", share: v.bundle.filter((b) => !b.task.exposure.renders).reduce((s, b) => s + (b.timeShare || 0), 0), n: v.bundle.length - assessed.length },
        { key: "assessed", label: "Assessed by a v2 multi-rater study", share: assessed.reduce((s, b) => s + (b.timeShare || 0), 0), n: assessed.length },
      ],
      emerging: v.role.competencyTargets.filter((t) => ["emerging", "proposed"].includes(t.competency.lifecycleState)).map((t) => t.competency),
      formation: v.bundle.filter((b) => b.formationTask || b.task.formationDependency === "yes"),
      // Signals about this role, this variant or the role's primary work function. Signals about a whole employer
      // type (e.g. every federal headcount figure) are not specific to the role: they are counted here and listed in
      // What's coming. Signals tied to an unverified claims-register row are withheld everywhere, only counted.
      drivers: signals.filter((s) => s.targetId === `vocab:work_functions#${v.role.primaryWorkFunction}` || s.targetId === v.id || s.targetId === v.role.id)
        .map((s) => signalVM(s)).filter((s) => !s.unverified.length),
      actorWide: signals.filter((s) => s.targetId === `vocab:sector_actors#${v.actor}` && !(claims.bySignal.get(s.id) || []).length).length,
      withheld: signals.filter((s) => [`vocab:work_functions#${v.role.primaryWorkFunction}`, `vocab:sector_actors#${v.actor}`, v.id, v.role.id].includes(s.targetId) && (claims.bySignal.get(s.id) || []).length).length,
    };
  }

  // Pathway edges between variants (computed; exploratory; ADR-0023 — never "recommended")
  // pathway-edges@0.1.0: compare the origin's targets at its highest role level with the destination's targets at its
  // first role level (where a person moving across would enter). Target levels are editorial design values.
  function targetMap(role) { return new Map(role.competencyTargets.map((t) => [t.id, t])); }
  const levelOrd = (l) => ({ A: 0, L1: 1, L2: 2, L3: 3, L4: 4, L5: 5 })[l] ?? 0;
  const ROLE_LEVEL_ORDER = ["entry", "journey", "senior", "lead", "strategic"];
  const levelsOf = (role) => role.roleLevels.map((l) => l.key).sort((a, b) => ROLE_LEVEL_ORDER.indexOf(a) - ROLE_LEVEL_ORDER.indexOf(b));
  const pathwaysFrom = new Map();
  for (const v of variants) {
    const o = targetMap(v.role);
    const named = new Set([...(v.role.progressesTo || [])]);
    const edges = [];
    for (const w of variants) {
      if (w.role.id === v.role.id && w.actor === v.actor) continue;
      if (w.role.id === v.role.id) continue;                  // same role, other actor: shown as a variant switch, not a pathway
      const fromLevel = levelsOf(v.role).slice(-1)[0], toLevel = levelsOf(w.role)[0];
      const d = new Map([...targetMap(w.role)].filter(([, t]) => t.targetLevels[toLevel]));
      if (!d.size) continue;
      let shared = 0; const gaps = [];
      for (const [cid, t] of d) {
        const s = o.get(cid);
        const have = s ? s.targetLevels[fromLevel] || "" : "";
        if (have && levelOrd(have) >= levelOrd(t.targetLevels[toLevel])) shared++;
        else gaps.push({ competency: t.competency, level: t.targetLevels[toLevel], fromLevel: have, partial: !!have });
      }
      const isNamed = named.has(w.role.id) || named.has(w.id);
      const lp = pathwayRecs.filter((p) => (p.fromVariant === v.id || p.fromVariant === v.role.id) && (p.toVariant === w.id || p.toVariant === w.role.id));
      if (!isNamed && !lp.length && shared * 2 < d.size) continue;
      edges.push({
        to: w, shared, destCount: d.size, gaps: gaps.slice(0, 12), gapCount: gaps.length, named: isNamed, fromLevel, toLevel,
        learning: lp.map((p) => ({ id: p.id, type: p.pathwayType || "", steps: (p.sequence || []).length, recommended: p.recommended === true })),
        frictions: frictionRecs.filter((f) => (f.fromVariant === v.id && f.toVariant === w.id) || (!f.fromVariant && f.fromActor === v.actor && f.toActor === w.actor))
          .map((f) => ({ type: f.frictionType, severity: f.severity, direction: f.direction, asOf: f.asOf, basis: f.basis, mitigation: en(f.mitigation), evidence: f.evidenceLabel })),
        crosswalks: w.crosswalks.filter((c) => /opm-series|state-class|local-class|soc/.test(c.set) && !c.noTerm),
        basis: "computed",
      });
    }
    // One entry per destination role; its variants are listed, the same-actor variant first (cross-sector moves visible).
    const byRole = new Map();
    for (const e of edges) {
      if (!byRole.has(e.to.role.id)) byRole.set(e.to.role.id, { ...e, toRole: e.to.role, variants: [] });
      const g = byRole.get(e.to.role.id);
      g.variants.push({ v: e.to, frictions: e.frictions, crosswalks: e.crosswalks, sameActor: e.to.actor === v.actor });
      g.named = g.named || e.named;
      if (e.learning.length && !g.learning.length) g.learning = e.learning;
    }
    const grouped = [...byRole.values()].map((g) => {
      g.variants.sort((a, b) => (b.sameActor - a.sameActor) || a.v.actor.localeCompare(b.v.actor));
      g.to = g.variants[0].v;
      return g;
    });
    grouped.sort((a, b) => (b.named - a.named) || (b.learning.length - a.learning.length) || (b.shared / b.destCount - a.shared / a.destCount) || a.toRole.title.localeCompare(b.toRole.title));
    pathwaysFrom.set(v.id, grouped.slice(0, 6));
    v.pathways = pathwaysFrom.get(v.id);
  }

  // Cross-sector translation rows (X11 seed, PS): available before role records exist
  const translations = mappings.filter((m) => m.mapping_set_id.startsWith("emst-public-private")).map((m) => {
    const c = crosswalkRow(m);
    const objectId = c.noTerm ? null : m.object_id;
    return {
      ...c, subject: m.subject_id, subjectLabel: m.subject_label || m.subject_id, subjectVariant: variantById.get(m.subject_id) || null,
      objectVariant: objectId ? variantById.get(objectId) || null : null, objectKey: (m.record_id || "").split(":").slice(-1)[0],
      translationId: c.other.translation_id || "", frictionChange: c.other.friction_posture_change || "",
      licensureGap: c.other.friction_licensure_gap || "", payDirection: c.other.friction_pay_direction || "",
      objectKeyLabel: keyLabel((m.record_id || "").split(":").slice(-1)[0]),
    };
  });

  // ---------------------------------------------------------------- signals, watch items, instruments, events
  function signalVM(s) {
    const fam = s.signalFamily || sigField(s, "signalFamily");
    const sps = (s.scenarioSignposts || []).concat((s.notation || []).filter((n) => n.scheme === "EMST-signpost").map((n) => n.value))
      .map((x) => String(x).replace(/^vocab:scenarios#/, "")).filter((x) => x !== "SP-12");
    const target = s.targetId || "";
    let targetLabel = target;
    const m = target.match(/^vocab:(work_functions|sector_actors|scenarios)#(.+)$/);
    if (m) targetLabel = m[1] === "work_functions" ? `Work function: ${labels.workFunction[m[2]] || m[2]}` : m[1] === "sector_actors" ? `Employer type: ${labels.sectorActor[m[2]] || m[2]}` : `Signpost ${m[2]}`;
    else if (records.has(target)) targetLabel = en(records.get(target).prefLabel);
    const unv = claims.bySignal.get(s.id) || [];
    return {
      id: s.id, title: unv.length ? "" : en(s.prefLabel), family: fam || "unknown", status: s.signalStatus || "watch", direction: s.direction || "", directionConfidence: s.directionConfidence || "",
      drivers: s.drivers || [], reliability: s.reliability || "", reliabilityText: labels.reliability[s.reliability] || "",
      measure: s.measure || null, period: s.observedPeriod || null, sourceRelease: s.sourceRelease || "", source: s.source || "",
      sectorActor: s.sectorActor || "", geography: s.geography || "", method: s.method || "", reviewBy: s.reviewBy || "",
      target, targetLabel, signposts: sps, evidence: evidenceOf(s), steep: s.steepCategory || "",
      impact: s.impact ?? sigField(s, "impact"), independenceKey: s.independenceKey || sigField(s, "independenceKey") || "",
      unverified: claims.bySignal.get(s.id) || [],
    };
  }
  // WP-15 sign-off, package review issue 2: a signal tied to an unverified register row is withheld entirely (its
  // headline is the claim), and only counted with the register row.
  const signalAll = signals.map(signalVM);
  const signalVMs = signalAll.filter((s) => !s.unverified.length).sort((a, b) => a.family.localeCompare(b.family) || a.title.localeCompare(b.title));
  const signalsWithheld = { n: signalAll.length - signalVMs.length, rows: [...new Set(signalAll.flatMap((s) => s.unverified))].sort() };
  const signalById = new Map(signalVMs.map((s) => [s.id, s]));
  const watchItems = byType("WatchItem").map((w) => ({
    id: w.id, slug: slugOf(w.id), title: en(w.prefLabel), lifecycleState: w.lifecycleState || "watch", reviewBy: w.reviewBy || "", outcome: w.outcome || "open",
    counterSignal: en(w.scopeNote).replace(/^Counter-signal \(what would show it is not forming\):\s*/i, ""),
    hypothesized: w.hypothesizedEntity ? { type: w.hypothesizedEntity.type, label: en(w.hypothesizedEntity.label), statement: en(w.hypothesizedEntity.functionStatement) } : null,
    signals: (w.signals || []).map((id) => signalById.get(id)).filter(Boolean),
    signalsWithheld: (w.signals || []).filter((id) => (claims.bySignal.get(id) || []).length).length, evidence: evidenceOf(w), tier: { tier: "exploratory", source: "lifecycle cap (watch)" },
  })).filter((w) => releasable(w.title + w.counterSignal));
  const instruments = byType("Instrument");
  const events = byType("DriverEvent");
  const eventsBy = new Map();
  for (const e of events) { if (!eventsBy.has(e.instrument)) eventsBy.set(e.instrument, []); eventsBy.get(e.instrument).push(e); }
  const asOf = release.date || "9999-12-31";
  const instrumentVMs = instruments.map((i) => {
    const evs = (eventsBy.get(i.id) || []).slice().sort((a, b) => a.eventDate.localeCompare(b.eventDate));
    const past = evs.filter((e) => e.eventDate <= asOf);
    const status = past.length ? past[past.length - 1].statusAfter : "no-event";
    const unverified = claims.byInstrument.get(i.id) || [];
    const noEvents = evs.length === 0;
    return {
      id: i.id, title: en(i.prefLabel), type: i.instrumentType || "", jurisdiction: i.jurisdiction || "", citation: i.citation || "",
      mechanisms: (i.mechanisms || []).map((m) => ({ code: m, label: releasable(labels.mechanism[m]) ? labels.mechanism[m] || m : labels.mechanismName[m] || m })), status, statusText: labels.instrumentStatus[status] || "",
      unverified, noEvents, noEventRow: noEvents ? claims.noEventRow : null,
      events: unverified.length ? [] : evs.map((e) => {
        const judged = claims.suppressEventLabels.has(e.evidenceLabel || "S");
        return { date: judged ? null : e.eventDate, dateSuppressed: judged, claimId: judged ? claims.eventRow : null, type: e.eventType, statusAfter: e.statusAfter, direction: e.direction || "", reviewBy: e.reviewBy || "", future: e.eventDate > asOf, evidence: e.evidenceLabel || "" };
      }),
      nextReview: evs.map((e) => e.reviewBy).filter(Boolean).sort()[0] || "", evidence: evidenceOf(i),
    };
  }).filter((i) => releasable(i.title + i.citation)).sort((a, b) => a.title.localeCompare(b.title));
  // role-change@0.1.0 instruments: the variant's typed links, plus instruments reached through the sensitivity edges
  // (mechanisms) of the role's target competencies. Each with its dated status as of the release date.
  {
    const instById = new Map(instrumentVMs.map((i) => [i.id, i]));
    const byMech = new Map();
    for (const i of instrumentVMs) for (const m of i.mechanisms) { if (!byMech.has(m.code)) byMech.set(m.code, []); byMech.get(m.code).push(i); }
    for (const v of variants) {
      const typed = v.instruments.map((x) => (instById.has(x.id) ? { i: instById.get(x.id), role: x.role,
        via: x.role ? `${linkRoleText(x.role)} (typed link on this variant)` : "typed link on this variant (role not recorded)" } : null)).filter(Boolean);
      const seen = new Set(typed.map((x) => x.i.id));
      const mechs = new Map();
      for (const t of v.role.competencyTargets) for (const e of records.get(t.id)?.instrumentSensitivity || []) if (e.mechanism) mechs.set(e.mechanism, (mechs.get(e.mechanism) || 0) + 1);
      const viaMech = [];
      for (const [m] of [...mechs].sort((a, b) => b[1] - a[1])) for (const i of byMech.get(m) || []) {
        if (seen.has(i.id) || i.jurisdiction !== "US") continue;        // state instruments only through typed links
        seen.add(i.id); viaMech.push({ i, via: `sensitivity to ${m} (${labels.mechanismName[m] || m})` });
      }
      v.instrumentLinks = { typed, viaMech: viaMech.slice(0, 8), viaMechTotal: viaMech.length };
    }
  }
  const changeIndicators = civ.rows.map((r) => ({
    ...r, targetLabel: (() => { const m = String(r.targetId).match(/^vocab:(work_functions|sector_actors|scenarios)#(.+)$/); if (m) return m[1] === "work_functions" ? `Work function: ${labels.workFunction[m[2]] || m[2]}` : m[1] === "sector_actors" ? `Employer type: ${labels.sectorActor[m[2]] || m[2]}` : `Signpost ${m[2]}`; return en(records.get(r.targetId)?.prefLabel) || r.targetId; })(),
  })).filter((r) => !String(r.targetId).endsWith("SP-12"));

  const scenarios = {
    axes: sc.axes.map((a) => ({ code: a.notation, label: a.prefLabel, poles: a.poles.filter((p) => releasable(p.definition)).map((p) => ({ code: p.notation, definition: p.definition })) })),
    terms: sc.terms.map((t) => ({ code: t.notation, label: t.prefLabel, summary: releasable(t.summary) ? t.summary : null, keyRisk: releasable(t.key_risk) ? t.key_risk : null })),
    signposts: sc.signposts.filter((s) => s.notation !== "SP-12" && s.access !== "tribal-council-only" && releasable(s.signpost)).map((s) => ({
      code: s.notation, text: s.signpost, source: s.source, cadence: s.cadence, pointsToward: s.points_toward,
      signals: signalVMs.filter((x) => x.signposts.includes(s.notation) || x.target === `vocab:scenarios#${s.notation}`),
      signalsWithheld: signalAll.filter((x) => x.unverified.length && (x.signposts.includes(s.notation) || x.target === `vocab:scenarios#${s.notation}`)).length,
    })),
    noRegret: sc.no_regret_moves_2026_2029.filter((m) => releasable(m.move)).map((m) => ({ code: m.id, text: m.move })),
    // Wildcards whose wording matches a register wrong form (e.g. WF-07) are left out (WP-15 sign-off §2.3).
    wildcards: sc.wildcards.filter((w) => releasable(w.wildcard + w.effect) && !textViolates(`${w.wildcard}: ${w.effect}`, dnsRules)).map((w) => ({ code: w.id, text: w.wildcard, effect: w.effect })),
  };

  // ---------------------------------------------------------------- HR registers: OPM series and state classes
  const seriesRecs = byType("SeriesRecord");
  const x4 = mappings.filter((m) => m.mapping_set_id.startsWith("opm-series/"));
  const x4c = mappings.filter((m) => m.mapping_set_id.startsWith("opm-series-competency"));
  const series = seriesRecs.map((s) => {
    const code = s.seriesCode || (s.notation || [])[0]?.value;
    const obj = `OPMseries:${code}`;
    const roleRows = x4.filter((m) => m.object_id === obj).map((m) => ({ ...crosswalkRow(m), subject: m.subject_id, subjectLabel: m.subject_label || m.subject_id, role: roleById.get(m.subject_id) || variantById.get(m.subject_id)?.role || null, variant: variantById.get(m.subject_id) || null }));
    const compRows = x4c.filter((m) => m.object_id === obj).map((m) => ({ ...crosswalkRow(m), competency: compById.get(m.subject_id) || null })).filter((r) => r.competency);
    const fedVariants = variants.filter((v) => v.actor === "federal" && (roleRows.some((r) => r.variant?.id === v.id) || roleRows.some((r) => !r.variant && r.role?.id === v.role.id && (r.other.variant || "federal") === "federal")));
    return {
      id: s.id, code, slug: code, url: `/federal-series/${code}/`, title: en(s.prefLabel), seriesStatus: s.seriesStatus || "", group: en(s.scopeNote),
      qualStd: s.qualificationStandardVersion || "", reviewBy: s.reviewBy || "", evidence: evidenceOf(s), tier: tierOf(s),
      realignment: /proposed/.test(s.seriesStatus || ""), notes: en(s.editorialNote || ""),
      roleRows, fedVariants,
      coreComps: compRows.filter((r) => !r.competency.isModule && r.competency.lifecycleState === "established"),
      omittedModule: compRows.filter((r) => r.competency.isModule).length,
      omittedNotEstablished: compRows.filter((r) => !r.competency.isModule && r.competency.lifecycleState !== "established").length,
      raw: s,
    };
  }).sort((a, b) => a.code.localeCompare(b.code));

  const classSets = mappings.filter((m) => /^(state-class|local-class)/.test(m.mapping_set_id));
  const stateClasses = byType("StateClassRecord").map((s) => {
    const scheme = (s.notation || [])[0]?.scheme || "";
    const code = s.classCode || (s.notation || [])[0]?.value || "";
    const jur = s.id.replace(/^seed:class\//, "").split("/")[0];
    const rows = classSets.filter((m) => String(m.object_id).endsWith(`:${code}`) && m.mapping_set_id.includes(jur.toLowerCase().split("-")[0])).map((m) => ({ ...crosswalkRow(m), subject: m.subject_id, subjectLabel: m.subject_label, variant: variantById.get(m.subject_id) || null }));
    const pending = (s.emstMapping || []).map((x) => ({ key: x.roleVariantKey || x.roleVariant || "", level: x.roleLevel || "", match: x.matchType || "", confidence: x.confidence ?? "", pending: x.pending || "", variant: variantById.get(`seed:${x.roleVariantKey}`) || variantById.get(x.roleVariant) || null }));
    return {
      id: s.id, slug: slugOf(s.id.replace(/^seed:class\//, "")), url: `/state-classes/${slugOf(s.id.replace(/^seed:class\//, ""))}/`, jurisdiction: s.jurisdictionId?.label || jur, jurisdictionCode: jur,
      code, scheme, title: s.classTitle || en(s.prefLabel), agency: s.agency || "", employerType: s.employerType || "", seriesName: s.seriesId || "",
      level: s.levelIndex ? `${s.levelIndex.label || ""} (ordinal ${s.levelIndex.ordinal ?? "?"})` : "", supervisory: s.supervisoryStatus || "",
      specEffective: s.specEffectiveDate || "", specUrl: s.workDescriptionText?.url || "", specRetrieved: s.workDescriptionText?.retrieved || "",
      mq: s.mqText?.paraphrase || "", degreeRule: s.degreeRule || "", licenses: (s.licensesRequired || []).map((l) => ({ credential: l.credential, issuer: l.issuer || "", timing: l.timing || "" })),
      pay: [s.payGradeLabel || s.payMinMax?.rangeLabel || "", (s.payMinMax && s.payMinMax.min != null && s.payMinMax.max != null) ? `${s.payMinMax.currency || "USD"} ${s.payMinMax.min.toLocaleString("en-US")}–${s.payMinMax.max.toLocaleString("en-US")} ${s.payBasis || ""}`.trim() : ""].filter(Boolean).join(", "), payEffective: s.payEffectiveDate || "", appointmentRoute: s.appointmentRoute || [],
      reviewBy: s.reviewBy || "", evidence: evidenceOf(s), tier: tierOf(s), rows, pending,
    };
  }).sort((a, b) => a.jurisdiction.localeCompare(b.jurisdiction) || a.code.localeCompare(b.code));

  // ---------------------------------------------------------------- generated HR views (WP-08 generators; CR-FH-001)
  // Every ID the generated views name is re-checked against the release bundle; anything absent (held, excluded,
  // superseded) is dropped and counted. Credential gates follow SPEC §10.5 rule 8 (verified issuer only). Default HR
  // content = core and established; module or non-established content is kept for a collapsed, labelled section.
  const hrSrc = meta?.hrViews || { source: "unavailable" };
  const hr = { source: hrSrc.source, dropped: 0, stamp: null };
  const readHr = (rel) => { const p = hrSrc.dir ? join(hrSrc.dir, rel) : null; return p && existsSync(p) ? loadJson(p) : null; };
  // The generators stamp a rule status written before the rule was registered ("proposed (...; not yet in
  // vocab/rules/)"). Read the status from the registered rule file when it exists, so the page is not stale.
  const ruleStamp = (st) => {
    if (!st) return st;
    const f = join(root, "vocab", "rules", `${st.ruleId}@${st.ruleVersion}.yaml`);
    if (!existsSync(f)) return { ...st, ruleStatus: String(st.ruleStatus || "not registered").replace(/\s*\(.*\)\s*$/, "") + " (not yet registered)" };
    let status = "registered";
    try { status = loadYaml(f)?.status || status; } catch { /* keep "registered" */ }
    return { ...st, ruleStatus: `registered rule, status ${status}` };
  };
  const inRelease = (id) => { const ok = !!id && records.has(id); if (id && !ok) hr.dropped++; return ok; };
  const instrumentById = new Map(instrumentVMs.map((i) => [i.id, i]));
  // CR-CP-001 B5: in role-scoped HR views the role's home module renders in the main section; other modules and
  // non-established items go to the collapsed section. B4: job-analysis values only from job-analysis-confirmed (hr).
  const inDefault = (c, home) => c.lifecycleState === "established" && (!c.isModule || c.module === home);
  let hrJa = { hrRenders: false }, hrHome = "core";
  function hrTarget(t) {
    const c = compById.get(t.competency);
    if (!c) { hr.dropped++; return null; }
    return { competency: c, targetLevels: t.targetLevels || {}, statement: t.statement || "",
      importance: hrJa.hrRenders ? t.importance ?? null : null, distinguishing: hrJa.hrRenders ? !!t.distinguishing : null,
      isDefault: inDefault(c, hrHome) };
  }
  function hrTask(t) {
    const tv = taskVMs.get(t.task) || (records.has(t.task) ? taskVM(t.task) : null);
    if (!tv) { hr.dropped++; return null; }
    const ok = hrJa.hrRenders;
    return { task: tv, pctTime: ok ? t.pctTime ?? null : null, importance: ok ? t.importance ?? null : null, critical: ok ? !!t.critical : null, neededAtEntry: ok ? !!t.neededAtEntry : null, formationTask: !!t.formationTask };
  }
  const setHrContext = (roleId) => { const r = records.get(roleId); hrJa = jaGate(r); hrHome = r?.homeModule || "core"; return hrJa; };
  // WP-08 views now carry credential gates as {shown: [...], notShownUntilIssuerVerified: n}; older views carried an
  // array. Either way each shown gate is re-checked against the release bundle (a gate whose issuer is not verified
  // there joins the withheld count), and the generator's withheld count is added, so nothing unverified is shown.
  const hrGates = (gs) => {
    const list = Array.isArray(gs) ? gs : Array.isArray(gs?.shown) ? gs.shown : [];
    const withheld = Array.isArray(gs) ? 0 : Math.max(0, Number(gs?.notShownUntilIssuerVerified) || 0);
    const g = gatesOf(list.filter((x) => x && x.credential).map((x) => ({ credential: x.credential, kind: x.kind })));
    return { shown: g.shown, pending: g.pending + withheld };
  };
  function fedProfile(code) {
    const d = readHr(`federal-series/${code}.json`);
    if (!d) return null;
    hr.stamp = hr.stamp || ruleStamp(d.stamp);
    const roles = (d.roles || []).filter((r) => inRelease(r.role) && (!r.variant || inRelease(r.variant)) && !roleById.get(r.role)?.whatsComingOnly).map((r) => (setHrContext(r.role), {
      role: roleById.get(r.role) || null, variant: variantById.get(r.variant) || null, depth: DEPTH_TEXT[r.tier] || "depth not recorded", functionStatement: r.functionStatement || "",
      x4: r.x4 || null, credentialGates: hrGates(r.credentialGates),
      instruments: (r.instruments || []).map((i) => (typeof i === "string" ? { id: i } : i || {})).filter((i) => instrumentById.has(i.id))
        .map((i) => ({ ...instrumentById.get(i.id), linkRole: i.role || "", linkRoleText: i.role ? linkRoleText(i.role) : "" })),
      ja: hrJa, homeModule: hrHome, homeModuleLabel: labels.module[hrHome] || hrHome,
      bands: (r.bands || []).map((b) => {
        const duties = (b.majorDuties || []).map((m) => {
          const c = compById.get(m.competency);
          if (!c) { hr.dropped++; return null; }
          return { competency: c, duty: m.duty, pctTime: hrJa.hrRenders ? m.pctTime ?? null : null, tasks: (m.tasks || []).map(hrTask).filter(Boolean), isDefault: inDefault(c, hrHome) };
        }).filter(Boolean);
        const k1 = (b.factor1Knowledge || []).map((f) => { const c = compById.get(f.competency); if (!c) { hr.dropped++; return null; } return { competency: c, statement: f.statement, knowledge: (f.knowledgeStatements || []).map(en), importance: hrJa.hrRenders ? f.importance ?? null : null, distinguishing: hrJa.hrRenders ? !!f.distinguishing : null, isDefault: inDefault(c, hrHome) }; }).filter(Boolean);
        return { group: b.group || "", band: b.indicativeBand || "", roleLevels: b.roleLevels || [], duties, factor1: k1,
          neededAtEntry: hrJa.hrRenders ? (b.neededAtEntryTasks || []).map((t) => taskVMs.get(t)).filter(Boolean) : [],
          critical: hrJa.hrRenders ? (b.criticalTasks || []).map((t) => taskVMs.get(t)).filter(Boolean) : [],
          distinguishing: hrJa.hrRenders ? (b.distinguishingCompetencies || []).map((c) => compById.get(c)).filter(Boolean) : [] };
      }),
    }));
    const withoutFed = (d.rolesWithoutFederalVariant || []).filter(inRelease).map((id) => roleById.get(id)).filter(Boolean);
    const feeders = (d.feederOrDestinationRoles || []).map((x) => (typeof x === "string" ? x : x.role)).filter(inRelease).map((id) => roleById.get(id)).filter(Boolean);
    return { stamp: ruleStamp(d.stamp), evidenceNotice: d.evidenceNotice || "", generalCompetencies: d.generalCompetencies || "", roles, withoutFed, feeders };
  }
  function classView(recordId) {
    const stem = String(recordId).replace(/^seed:class\//, "").replace(/\//g, "--");
    const d = readHr(`state-class/${stem}.json`);
    if (!d) return null;
    hr.stamp = hr.stamp || ruleStamp(d.stamp);
    return {
      stamp: ruleStamp(d.stamp), evidenceNotice: d.evidenceNotice || "",
      mappings: (d.mappings || []).filter((m) => inRelease(m.roleVariant) && !roleById.get(m.role)?.whatsComingOnly).map((m) => (setHrContext(m.role), {
        variant: variantById.get(m.roleVariant) || null, roleTitle: m.roleTitle || "", depth: DEPTH_TEXT[m.tier] || "depth not recorded", roleLevels: m.roleLevels || [],
        matchType: m.matchType || "", confidence: m.confidence ?? "", review: m.review || "", authorityPosition: labels.authorityPosition[m.authorityPosition] || m.authorityPosition || "",
        targets: (m.competencyTargets || []).map(hrTarget).filter(Boolean), tasks: (m.topTasks || []).map(hrTask).filter(Boolean), credentialGates: hrGates(m.credentialGates),
        ja: hrJa, homeModuleLabel: labels.module[hrHome] || hrHome,
      })),
    };
  }
  for (const s of series) s.profile = fedProfile(s.code);
  for (const c of stateClasses) c.view = classView(c.id);

  // ---------------------------------------------------------------- modules (editorial sections; never default HR views)
  const moduleList = [...new Set(competencies.filter((c) => c.isModule).map((c) => c.module))].sort().map((ns) => ({
    ns, label: labels.module[ns] || ns, code: labels.moduleCode[ns] || "", wave: labels.moduleWave[ns] ?? null,
    competencies: competencies.filter((c) => c.module === ns),
  }));

  // ---------------------------------------------------------------- what's coming
  const emergingCompetencies = competencies.filter((c) => ["emerging", "proposed"].includes(c.lifecycleState));
  const emergingRoles = roles.filter((r) => ["emerging", "proposed"].includes(r.lifecycleState));

  // ---------------------------------------------------------------- search index (one file, loaded before typing)
  const search = [
    ...roles.map((r) => ({ t: r.title, k: r.whatsComingOnly ? "Emerging role (What's coming)" : "Role", u: r.url, a: r.altLabels.join(" ") })),
    ...variants.map((v) => ({ t: v.title, k: "Role variant", u: v.url, a: "" })),
    ...competencies.map((c) => ({ t: c.title, k: c.isModule ? `Competency (${c.moduleLabel} editorial section)` : "Competency", u: c.url, a: c.altLabels.join(" ") + " " + c.v1Codes.join(" ") })),
    ...series.map((s) => ({ t: `${s.code} ${s.title}`, k: "Federal series profile", u: s.url, a: "" })),
    ...stateClasses.map((s) => ({ t: `${s.title} (${s.jurisdiction} ${s.code})`, k: "State or local class view", u: s.url, a: s.agency })),
    ...watchItems.map((w) => ({ t: w.title, k: "Watch item", u: `/whats-coming/#${w.slug}`, a: "" })),
    ...[...taskVMs.values()].filter((t) => t.supports[0]?.url).map((t) => ({ t: t.statement, k: "Task", u: `${t.supports[0].url}#${t.anchor}`, a: "" })),
  ];

  // ---------------------------------------------------------------- gap-check data (role-independent mode)
  const gapCompetencies = competencies.filter((c) => !c.isModule && c.levels.some((l) => l.indicators.length)).map((c) => ({
    id: c.id, t: c.title, u: c.url, type: c.typeLabel, tier: c.tier.tier, ev: c.evidence.label,
    levels: c.levels.filter((l) => l.indicators.length).map((l) => ({ l: l.level, n: l.label, i: l.indicators.map((i) => i.statement) })),
  }));

  const figures = {
    coreCompetencies: figureOf(competencies.filter((c) => !c.isModule)), moduleCompetencies: figureOf(competencies.filter((c) => c.isModule)),
    tasks: figureOf([...taskVMs.values()]), roles: figureOf(roles), variants: figureOf(variants), series: figureOf(series),
    stateClasses: figureOf(stateClasses), signals: { ...figureOf(signalVMs), tier: { tier: "exploratory", source: "watch signals" } },
    watchItems: { ...figureOf(watchItems), tier: { tier: "exploratory", source: "lifecycle cap (watch)" } }, instruments: figureOf(instrumentVMs),
    emergingCompetencies: figureOf(emergingCompetencies),
    gate: { tier: { tier: "exploratory", source: "display gate" }, ev: { label: "S", labelText: "Speculation", isAgentDraft: true, isV1Seed: false, reviewStatus: "unreviewed" } },
  };

  return {
    release, labels, gateLabels, counts, figures, venue: { source: venue.source, asOf: venue.asOf, n: venueBy.size, rule: venue.rule }, hr,
    claims: { signoff: claims.signoff, unverifiedInstruments: [...claims.byInstrument.keys()].length },
    competencies, coreCompetencies: competencies.filter((c) => !c.isModule), moduleList,
    roles, rolesMain: roles.filter((r) => !r.whatsComingOnly), variants, pathwaysFrom, translations, pathwayRecords: pathwayRecs.length,
    signals: signalVMs, signalsWithheld, watchItems, instruments: instrumentVMs, changeIndicators, scenarios,
    series, stateClasses, emergingCompetencies, emergingRoles, search, gapCompetencies,
    titleIndex: Object.fromEntries(competencies.map((c) => [c.id, c.title])),
    stats: {
      tasks: taskVMs.size, indicators: indicators.size, mappings: mappings.length, tools: tools.length,
      v1Assessments: [...v1ByTask.values()].reduce((s, x) => s + x.length, 0), gatedRendering: dgv.rows.filter((r) => r.decision === "production" || r.decision === "tentative").length,
      gatedRows: dgv.rows.length,
      depth: { full: roles.filter((r) => !r.whatsComingOnly && r.depthTier === "P1").length,
        lower: roles.filter((r) => !r.whatsComingOnly && r.depthTier !== "P1").length, emerging: roles.filter((r) => r.whatsComingOnly).length },
    },
  };
}
