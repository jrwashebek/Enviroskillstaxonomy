// Check the generated GitBook guidebook (gitbook/site) before it is synced to GitBook. Decision Q17 sets the rule:
// nothing syncs unless these checks pass. Exit code 1 on any failure; warnings are reported and do not fail.
//
// Usage (from the repository root):  node prototype/public-ui/tools/check-gitbook.mjs
// Writes prototype/public-ui/docs/qa/gitbook-check.json (set GB_OUT_DIR to write it somewhere else).
//
// Checks
//   build      gitbook/site is exactly what tools/build-gitbook.mjs makes (no hand edits, no stale pages)
//   structure  .gitbook.yaml; SUMMARY.md lists every page once and only pages that exist; README first
//   page       front-matter description; one h1, first; no skipped heading levels; balanced hint blocks; the
//              release ribbon and the report-a-problem footer; no unfilled tokens or unresolved links
//   links      relative links reach a page (and its heading, for #anchors); external links are https with no query
//              string; link text says where it goes; images have alt text; tables are well formed
//   content    the same honesty rules as the explorer's check-rendered.mjs (claims register, Tribal hold triggers,
//              held-content wording, never recommend, never "you qualify", jargon, personal data), plus: change is
//              never stated as fact, EMST makes no forecast, and no private or build-machine path appears
//   figures    the home page's counts equal the release's counts.json
//   reading    Flesch-Kincaid grade per page (target 8 or lower: warning above 8, failure above 10)
// Licence: Apache-2.0.
import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, resolve, dirname, posix } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";
import { spawnSync } from "node:child_process";
import vm from "node:vm";

const HERE = dirname(fileURLToPath(import.meta.url));
const UI = resolve(HERE, "..");
const ROOT = resolve(UI, "..", "..");
const SITE = join(UI, "gitbook", "site");
const require = createRequire(import.meta.url);
const yaml = require(join(ROOT, "site", "node_modules", "js-yaml"));
const { parseRegister, sentencesOf, conflates, phraseRx, parseCsv } = await import(pathToFileURL(join(ROOT, "site", "lib", "claims.mjs")).href);
globalThis.window = {};
vm.runInThisContext(readFileSync(join(UI, "app", "data", "core.js"), "utf8"));
const core = window.EMSTDATA.core;

const fails = [], warns = [], info = {};
const fail = (page, rule, detail = "") => fails.push({ page, rule, detail: String(detail).slice(0, 240) });
const warn = (page, rule, detail = "") => warns.push({ page, rule, detail: String(detail).slice(0, 240) });

// ---------------------------------------------------------------- build
const b = spawnSync(process.execPath, [join(HERE, "build-gitbook.mjs"), "--check"], { encoding: "utf8" });
if (b.status !== 0) fail("(site)", "build-drift", (b.stderr || b.stdout).trim());

// ---------------------------------------------------------------- structure
const walk = (d, base = d) => (existsSync(d) ? readdirSync(d).flatMap((f) => { const full = join(d, f); return statSync(full).isDirectory() ? walk(full, base) : [full.slice(base.length + 1).split(/[\\/]/).join("/")]; }) : []);
const all = walk(SITE);
const mdFiles = all.filter((f) => f.endsWith(".md") && f !== "SUMMARY.md");
for (const f of all.filter((f) => !f.endsWith(".md") && f !== ".gitbook.yaml")) fail(f, "unexpected-file", "only Markdown pages and .gitbook.yaml belong in gitbook/site");
let gb = {};
try { gb = yaml.load(readFileSync(join(SITE, ".gitbook.yaml"), "utf8")) || {}; } catch (e) { fail(".gitbook.yaml", "missing-or-invalid", e.message); }
if (gb.root !== "./" || gb.structure?.readme !== "README.md" || gb.structure?.summary !== "SUMMARY.md") fail(".gitbook.yaml", "config", JSON.stringify(gb));
const summary = existsSync(join(SITE, "SUMMARY.md")) ? readFileSync(join(SITE, "SUMMARY.md"), "utf8") : "";
const navLinks = [...summary.matchAll(/^\s*\* \[([^\]]+)\]\(([^)]+)\)\s*$/gm)].map((m) => m[2]);
if (!summary) fail("SUMMARY.md", "missing");
if (navLinks[0] !== "README.md") fail("SUMMARY.md", "readme-first", navLinks[0]);
const seen = new Set();
for (const l of navLinks) { if (seen.has(l)) fail("SUMMARY.md", "listed-twice", l); seen.add(l); if (!mdFiles.includes(l)) fail("SUMMARY.md", "missing-page", l); }
for (const f of mdFiles) if (!seen.has(f)) fail(f, "not-in-summary");
const firstGroup = summary.search(/^## /m), lastUngrouped = summary.slice(0, firstGroup < 0 ? summary.length : firstGroup);
if (firstGroup >= 0 && /^\* \[/m.test(summary.slice(firstGroup)) === false) fail("SUMMARY.md", "empty-groups");
info.pages = mdFiles.length; info.ungroupedPages = (lastUngrouped.match(/^\* \[/gm) || []).length;

// ---------------------------------------------------------------- page parsing
const slug = (s) => String(s).toLowerCase().replace(/[’'"“”]/g, "").replace(/[^a-z0-9\s-]/g, " ").trim().replace(/\s+/g, "-").replace(/-+/g, "-");
const unescapeMd = (s) => s.replace(/\\([\\*`<>[\]|_])/g, "$1");
const pages = new Map();
for (const f of mdFiles) {
  const raw = readFileSync(join(SITE, f), "utf8");
  const fm = raw.match(/^---\n([\s\S]*?)\n---\n/);
  const body = fm ? raw.slice(fm[0].length) : raw;
  const headings = [...body.matchAll(/^(#{1,6}) (.+)$/gm)].map((m) => ({ level: m[1].length, text: unescapeMd(m[2].trim()) }));
  pages.set(f, { raw, body, fm: fm ? yaml.load(fm[1]) : null, headings, anchors: new Set(headings.map((h) => slug(h.text))) });
}

// Plain text of a page, one rendered line per line (list items and table cells are separate lines).
function textOf(body) {
  return body
    .replace(/\{% hint style="\w+" %\}|\{% endhint %\}/g, "")
    .replace(/^\|?\s*-{3,}.*$/gm, "")
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[((?:\\\]|[^\]])+)\]\([^)]*\)/g, "$1")
    .split("\n").flatMap((l) => (l.trim().startsWith("|") ? l.split(/(?<!\\)\|/).map((c) => c.trim()) : [l]))
    .map((l) => unescapeMd(l.replace(/^#{1,6} |^\s*(?:[-*]|\d+\.) |^> /, "").replace(/\*\*/g, "")))
    .filter((l) => l.trim() && l.trim() !== "---")
    .join("\n");
}

// ---------------------------------------------------------------- rules shared with check-rendered.mjs
const JARGON = /effective-use-tier@|closeMatch|relatedMatch|broadMatch|narrowMatch|exactMatch|agentDraft|raterType|OBS-4|SSSOM|skos:|semapv:|\bLLM\b(?! \[large language model\])|\bundefined\b(?! terms?\b)|\[object Object\]|\bNaN\b/;
const gc = yaml.load(readFileSync(join(ROOT, "schema", "lint", "governed_content.yaml"), "utf8"));
const TRIBAL = gc.tribal_hold.triggers.map((p) => (typeof p === "string" ? new RegExp(p, "i") : new RegExp(p.pattern, p.cs ? "" : "i")));
const CONFIDENTIAL = (gc.confidential_markers || []).map((p) => new RegExp(p, "i"));
const HELD_POLICY = core.status.held.policy, INDIGENOUS = core.release.indigenousStatement;
const allowedHeld = [HELD_POLICY, INDIGENOUS].filter(Boolean);
const HELD_CLAUSE = /consultation content held under ADR-0007|agreement types covered by the ADR-0007 hold|\bADR-0007\b/i;
const register = parseRegister(parseCsv(readFileSync(join(ROOT, "docs", "methods", "claims_register.csv"), "utf8")));
// Stating change as a fact, or forecasting, unless the same sentence negates or conditions it.
const CHANGE_FACT = /\b(?:is|are|will be) (?:now |already |rapidly )?(?:changing|shrinking|growing|disappearing|declining|being (?:automated|replaced|transformed))\b|\bwill (?:replace|eliminate|automate|transform)\b|\b(?:compresses|automates|eliminates) (?:the )?(?:work|production|jobs?|tasks?)\b/i;
const FORECAST = /\b(?:forecasts?|forecasted|predicts?|projected to)\b/i;
const NEGATED = /\b(?:not|no|never|none|nothing|only when|whether|until|unless|any role is)\b/i;
const PRIVATE = /\/home\/|\/tmp\/|\/root\/|\/mnt\/|scratchpad|claude\.ai\/(?:code|chat)|session_[0-9A-Za-z]{6,}|C:\\Users\\/i;
const EMAIL = /[\w.+-]+@[\w-]+\.[a-z]{2,}/i, PHONE = /(?<!\d)(?:\(\d{3}\)\s?|\d{3}[-.])\d{3}[-.]\d{4}(?!\d)/;

function contentRules(page, text) {
  const lines = text.split("\n");
  const sents = lines.flatMap((l) => sentencesOf(l));
  const m = text.match(JARGON);
  if (m) fail(page, "jargon", m[0]);
  let stripped = text.replace(/\n/g, " ");
  for (const a of allowedHeld) stripped = stripped.split(a).join(" ");
  for (const rx of TRIBAL) { const t = stripped.match(rx); if (t) fail(page, "tribal-trigger", stripped.slice(Math.max(0, t.index - 80), t.index + 80)); }
  for (const rx of CONFIDENTIAL) { const t = text.match(rx); if (t) fail(page, "confidential-marker", t[0]); }
  const hc = text.match(HELD_CLAUSE);
  if (hc) fail(page, "held-description", hc[0]);
  if (/content hold/i.test(stripped)) fail(page, "held-policy-paraphrased", "a mention of the content hold outside the verbatim policy");
  for (const rule of register.strict) { const t = new RegExp(phraseRx(rule.phrase).source, "i").exec(text); if (t) fail(page, "retired-claim", `${rule.claim}: ${t[0]}`); }
  for (const s of sents) for (const rule of register.conflations) if (conflates(s, rule)) fail(page, "conflation", s.slice(0, 160));
  for (const s of sents) {
    if (/\brecommend(ed|s|ation)?\b/i.test(s) && /\b(pathways?|paths?|next (role|step|move)|career|move to|you should|moves?)\b/i.test(s)
      && !/\b(never|not|no|none)\b[^.]{0,60}\brecommend/i.test(s) && !/successional pathway|consultation findings/i.test(s)) fail(page, "recommend", s);
    if (CHANGE_FACT.test(s) && !NEGATED.test(s)) fail(page, "change-as-fact", s);
    if (FORECAST.test(s) && !NEGATED.test(s) && !/other bodies' projections/i.test(s)) fail(page, "forecast", s);
  }
  for (const q of text.matchAll(/\byou (qualify|are qualified|are eligible)\b/gi)) {
    if (!/(?:doesn.t|does not|never|not) (?:mean|say)[^.]{0,20}$|\bwhether $/i.test(text.slice(Math.max(0, q.index - 40), q.index))) fail(page, "qualify", text.slice(Math.max(0, q.index - 60), q.index + 60));
  }
  if (EMAIL.test(text)) fail(page, "email", text.match(EMAIL)[0]);
  if (PHONE.test(text)) fail(page, "phone", text.match(PHONE)[0]);
  for (const t of text.matchAll(/(\d+(?:\.\d+)?)\s?%/g)) warn(page, "percent (review)", text.slice(Math.max(0, t.index - 60), t.index + 40));
}

// ---------------------------------------------------------------- reading level (Flesch-Kincaid grade)
function syllables(w) {
  w = w.toLowerCase().replace(/[^a-z]/g, "");
  if (!w) return 0;
  if (w.length <= 3) return 1;
  w = w.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/, "").replace(/^y/, "");
  const n = (w.match(/[aeiouy]{1,2}/g) || []).length;
  return Math.max(1, n);
}
function fkGrade(text) {
  const sentences = text.split(/\n+/).flatMap((l) => l.split(/(?<=[.!?])\s+/)).map((s) => s.trim()).filter((s) => /[A-Za-z]/.test(s));
  const words = sentences.flatMap((s) => s.split(/\s+/).filter((w) => /[A-Za-z]/.test(w)));
  if (!words.length) return { grade: 0, words: 0 };
  const syl = words.reduce((n, w) => n + syllables(w), 0);
  return { grade: 0.39 * (words.length / sentences.length) + 11.8 * (syl / words.length) - 15.59, words: words.length, sentences: sentences.length };
}

// ---------------------------------------------------------------- per page
const BAD_LINK_TEXT = /^(here|click here|link|this|this link|this page|more|read more|learn more)$/i;
const ribbonStart = "Draft release ";
const reading = [];
for (const [f, pg] of pages) {
  const { body, fm, headings } = pg;
  if (!fm?.description || String(fm.description).length > 220) fail(f, "description", fm?.description || "missing");
  const h1 = headings.filter((h) => h.level === 1);
  if (h1.length !== 1 || headings[0]?.level !== 1) fail(f, "h1", `${h1.length} h1; first heading level ${headings[0]?.level}`);
  for (let i = 1; i < headings.length; i++) if (headings[i].level > headings[i - 1].level + 1) fail(f, "heading-skip", `${headings[i - 1].text} → ${headings[i].text}`);
  const dupe = headings.map((h) => slug(h.text)).filter((s, i, a) => a.indexOf(s) !== i);
  if (dupe.length) fail(f, "duplicate-heading-anchor", dupe.join(", "));
  const opens = (body.match(/\{% hint style="(\w+)" %\}/g) || []), closes = (body.match(/\{% endhint %\}/g) || []);
  if (opens.length !== closes.length) fail(f, "hint-unbalanced", `${opens.length} open, ${closes.length} close`);
  for (const o of opens) if (!/"(info|warning|danger|success)"/.test(o)) fail(f, "hint-style", o);
  const firstHint = body.indexOf('{% hint style="info" %}\n' + ribbonStart);
  if (firstHint < 0 || firstHint > body.indexOf("\n# ") + 200) fail(f, "release-ribbon");
  if (!body.includes("[Report a problem with this page](") || !body.includes(`release ${core.release.id}`)) fail(f, "footer");
  const priv = pg.raw.match(PRIVATE);
  if (priv) fail(f, "private-path", priv[0]);
  const leftovers = body.replace(/\{% (?:hint style="\w+"|endhint) %\}/g, "").match(/\{\{|\}\}|\{%|%\}|\]\((?:page|explorer(?:-cta)?):|\]\(#\//);
  if (leftovers) fail(f, "unresolved", leftovers[0]);

  // links and images
  for (const m of body.matchAll(/(!?)\[((?:\\\]|[^\]\n])*)\]\(([^)\s]*)\)/g)) {
    const [, bang, rawText, href] = m, text = unescapeMd(rawText).trim();
    if (bang) { if (!text) fail(f, "image-alt", href); continue; }
    if (!text) fail(f, "empty-link-text", href);
    if (BAD_LINK_TEXT.test(text)) fail(f, "vague-link-text", text);
    if (/^https?:/.test(href)) {
      if (!href.startsWith("https://")) fail(f, "not-https", href);
      if (href.includes("?")) fail(f, "query-string", href);
      (info.hosts ||= {})[new URL(href).host] = ((info.hosts ||= {})[new URL(href).host] || 0) + 1;
      continue;
    }
    if (/^[a-z]+:/i.test(href)) { fail(f, "link-scheme", href); continue; }
    const [p, anchor] = href.split("#");
    const target = p ? posix.normalize(posix.join(posix.dirname(f), p)) : f;
    if (!pages.has(target)) { fail(f, "broken-link", href); continue; }
    if (anchor && !pages.get(target).anchors.has(anchor)) fail(f, "broken-anchor", href);
  }
  // tables
  const lines = body.split("\n");
  for (let i = 0; i < lines.length; i++) {
    if (!lines[i].startsWith("|") || (i > 0 && lines[i - 1].startsWith("|"))) continue;
    const cols = (l) => l.replace(/\\\|/g, "").split("|").length - 2;
    const head = lines[i], sep = lines[i + 1] || "";
    if (!/^\|(?:\s*:?-{3,}:?\s*\|)+$/.test(sep)) { fail(f, "table-no-header", head.slice(0, 80)); continue; }
    if (head.replace(/\\\|/g, "").split("|").slice(1, -1).some((c) => !c.trim())) fail(f, "table-empty-header", head.slice(0, 80));
    for (let j = i + 1; j < lines.length && lines[j].startsWith("|"); j++) if (cols(lines[j]) !== cols(head)) fail(f, "table-columns", lines[j].slice(0, 80));
  }
  // content and reading level (the ribbon, the footer and the glossary table are shared or reference text)
  const text = textOf(body);
  contentRules(f, text);
  const prose = textOf(body.replace(/\{% hint style="info" %\}\nDraft release[\s\S]*?\{% endhint %\}/, "").replace(/\n---\n[\s\S]*$/, "").replace(/^\|.*$/gm, ""));
  // Sentences only: lines of names (roles, modules, competencies) carry no end punctuation and are not prose.
  const r = fkGrade(prose.split("\n").filter((l) => /[.!?”]$/.test(l.trim())).join("\n").replace(/O\*NET/g, "ONET"));
  reading.push({ page: f, grade: Math.round(r.grade * 10) / 10, words: r.words });
  if (f !== "how-to-read/glossary.md" && r.words >= 60) {
    if (r.grade > 10) fail(f, "reading-level", `FK grade ${r.grade.toFixed(1)}`);
    else if (r.grade > 8) warn(f, "reading-level", `FK grade ${r.grade.toFixed(1)}`);
  }
}
const held = pages.get("how-to-read/held-records.md");
if (!held || !textOf(held.body).replace(/\n/g, " ").includes(HELD_POLICY)) fail("how-to-read/held-records.md", "held-policy-verbatim");

// ---------------------------------------------------------------- figures on the home page
const counts = JSON.parse(readFileSync(join(ROOT, "docs", "release", core.release.id, "counts.json"), "utf8"));
const home = pages.get("README.md")?.body || "";
const rowN = (label) => { const m = home.match(new RegExp(`^\\| ${label} \\| ([\\d,]+) \\|`, "m")); return m ? Number(m[1].replace(/,/g, "")) : null; };
for (const [label, want] of [["Roles", counts.byType.RoleProfile], ["Competencies", counts.byType.Competency], ["Tasks", counts.byType.Task]]) {
  const got = rowN(label);
  if (got !== want) fail("README.md", "figure", `${label}: page ${got}, counts.json ${want}`);
}

// ---------------------------------------------------------------- report
reading.sort((a, b) => b.grade - a.grade);
const medianGrade = reading.map((r) => r.grade).sort((a, b) => a - b)[Math.floor(reading.length / 2)];
const outDir = process.env.GB_OUT_DIR ? resolve(process.env.GB_OUT_DIR) : join(UI, "docs", "qa");
mkdirSync(outDir, { recursive: true });
const byRule = (xs) => xs.reduce((o, x) => ((o[x.rule] = (o[x.rule] || 0) + 1), o), {});
const report = { release: core.release.id, pages: info.pages, failures: fails.length, warnings: warns.length, failuresByRule: byRule(fails), warningsByRule: byRule(warns),
  readingLevel: { medianGrade, highest: reading.slice(0, 5) }, externalHosts: info.hosts || {}, fails, warns };
writeFileSync(join(outDir, "gitbook-check.json"), `${JSON.stringify(report, null, 1)}\n`);
console.log(`[check-gitbook] ${info.pages} pages: ${fails.length} failure(s), ${warns.length} warning(s); median reading grade ${medianGrade}`);
for (const x of fails.slice(0, 40)) console.log(`  FAIL ${x.page} | ${x.rule} | ${x.detail}`);
for (const x of warns.slice(0, 20)) console.log(`  warn ${x.page} | ${x.rule} | ${x.detail}`);
process.exit(fails.length ? 1 : 0);
