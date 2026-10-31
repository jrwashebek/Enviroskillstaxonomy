// Crawl every route of the prototype in Chromium and check the rendered text against the project's honesty rules.
// Usage (from the repository root, with the app served):  node prototype/public-ui/tools/check-rendered.mjs http://127.0.0.1:8811
// Exit code 1 on any failure. Licence: Apache-2.0.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";
import vm from "node:vm";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, "..", "..", "..");
const BASE = process.argv[2] || "http://127.0.0.1:8811";
const LIMIT = Number(process.env.LIMIT || 0);
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const yaml = require(join(ROOT, "site", "node_modules", "js-yaml"));
const { parseRegister, sentencesOf, conflates, phraseRx, parseCsv } = await import(pathToFileURL(join(ROOT, "site", "lib", "claims.mjs")).href);

// ---------------------------------------------------------------- data (to list routes)
globalThis.window = {};
for (const f of ["core", "search", "hr"]) vm.runInThisContext(readFileSync(join(HERE, "..", "app", "data", `${f}.js`), "utf8"));
const core = window.EMSTDATA.core, search = window.EMSTDATA.search, hr = window.EMSTDATA.hr;

const routes = ["/", "/roles", "/competencies", "/compare", "/changing", "/hr", "/series", "/classes", "/about",
  ...["read", "made", "status", "data", "corrections", "held", "accessibility", "privacy"].map((p) => `/about/${p}`)];
for (const r of core.roles) {
  routes.push(`/role/${r.slug}`);
  for (const v of r.variants || []) routes.push(`/role/${r.slug}/${v.actor}`);
}
for (const c of core.comps) routes.push(`/competency/${c.slug}`);
for (const m of core.modules) routes.push(`/competencies/${m.ns}`);
vm.runInThisContext(readFileSync(join(HERE, "..", "app", "data", "search-tasks.js"), "utf8"));
for (const d of window.EMSTDATA["search:tasks"].docs) if (d.k === "task") routes.push(`/task/${d.s}`);
for (const s of hr.series) routes.push(`/series/${s.slug || s.code}`);
for (const c of hr.classes) routes.push(`/class/${c.slug}`);
for (const d of search.docs.filter((d) => d.k === "tool" || d.k === "credential")) routes.push(`/${d.k}/${d.s}`);
const p1 = core.roles.filter((r) => !r.whatsComingOnly);
for (let i = 0; i + 1 < p1.length; i += 3) routes.push(`/compare/${p1[i].slug}/${p1[i + 1].slug}`);
const list = LIMIT ? routes.slice(0, LIMIT) : routes;

// ---------------------------------------------------------------- rules
const JARGON = /effective-use-tier@|closeMatch|relatedMatch|broadMatch|narrowMatch|exactMatch|agentDraft|raterType|OBS-4|SSSOM|skos:|semapv:|\bLLM\b(?! \[large language model\])|\bundefined\b(?! terms?\b)|\[object Object\]|\bNaN\b/;
const gc = yaml.load(readFileSync(join(ROOT, "schema", "lint", "governed_content.yaml"), "utf8"));
const TRIBAL = gc.tribal_hold.triggers.map((p) => (typeof p === "string" ? new RegExp(p, "i") : new RegExp(p.pattern, p.cs ? "" : "i")));
const allowedHeld = [core.status?.held?.policy, core.release?.indigenousStatement].filter(Boolean);
const regRows = parseCsv(readFileSync(join(ROOT, "docs", "methods", "claims_register.csv"), "utf8"));
const register = parseRegister(regRows);
const hrFirst = String(hr.disclaimer || core.text?.hrDisclaimer || "").split(/\n+/)[0].slice(0, 60);
const pathsNotice = String(core.text?.pathwaysNotice || "").slice(0, 50);

function checkText(route, text, lines = text) {
  // Sentence-level rules run per rendered line: list items and table cells have no full stop between them.
  const sents = lines.split(/\n+/).flatMap((l) => sentencesOf(l));
  const out = [];
  const m = text.match(JARGON);
  if (m) out.push(["jargon", m[0], text.slice(Math.max(0, m.index - 60), m.index + 60)]);
  let stripped = text;
  for (const a of allowedHeld) stripped = stripped.split(a).join(" ");
  for (const rx of TRIBAL) { const t = stripped.match(rx); if (t && route !== "/about/held") out.push(["tribal-trigger", t[0], stripped.slice(Math.max(0, t.index - 80), t.index + 80)]); }
  for (const rule of register.strict) { const t = new RegExp(phraseRx(rule.phrase).source, "i").exec(text); if (t) out.push(["retired-claim", `${rule.claim}: ${t[0]}`, text.slice(Math.max(0, t.index - 60), t.index + 60)]); }
  for (const s of sents) for (const rule of register.conflations) if (conflates(s, rule)) out.push(["conflation", rule.claim || "", s.slice(0, 160)]);
  // EMST must never recommend a pathway, role or move. Task statements may describe recommending as part of the work.
  for (const sent of sents) {
    if (!/\brecommend(ed|s|ation)?\b/i.test(sent) || !/\b(pathways?|paths?|next (role|step|move)|career|move to|you should)\b/i.test(sent)) continue;
    if (/\b(never|not|no|none)\b[^.]{0,60}\brecommend/i.test(sent) || /successional pathway|consultation findings/i.test(sent)) continue;
    out.push(["recommend", "", sent.slice(0, 200)]);
  }
  const q = /\byou (qualify|are qualified|are eligible)\b/i.exec(text);
  if (q && !/(doesn.t|does not|never|not) (mean|say)[^.]{0,20}$/i.test(text.slice(Math.max(0, q.index - 40), q.index))) out.push(["qualify", q[0], text.slice(Math.max(0, q.index - 60), q.index + 60)]);
  for (const t of text.matchAll(/(\d+(?:\.\d+)?)\s?%/g)) out.push(["percent (review)", t[0], text.slice(Math.max(0, t.index - 60), t.index + 40)]);
  if (/@|mailto:/.test(text) && /[\w.]+@[\w-]+\.[a-z]{2,}/i.test(text)) out.push(["email", "", ""]);
  return out;
}

// ---------------------------------------------------------------- crawl
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
const errors = [], external = [];
page.on("pageerror", (e) => errors.push([page.url(), e.message]));
page.on("console", (m) => { if (m.type() === "error") errors.push([page.url(), m.text()]); });
page.on("request", (r) => { if (!r.url().startsWith(BASE) && !r.url().startsWith("blob:") && !r.url().startsWith("data:")) external.push(r.url()); });
await page.goto(`${BASE}/index.html#/`);
await page.waitForSelector("#main h1");

const findings = [], metrics = [];
let n = 0;
for (const r of list) {
  await page.evaluate((h) => { location.hash = h; }, `#${r}`); // test harness only; the app itself never writes location
  try {
    await page.waitForFunction(() => !document.querySelector("#main[aria-busy]") && document.querySelector("#main h1"), null, { timeout: 8000 });
  } catch { findings.push([r, "timeout", "", ""]); continue; }
  await page.waitForTimeout(30);
  const info = await page.evaluate(() => {
    const main = document.querySelector("#main");
    const raw = main.innerText;
    const text = raw.replace(/\s+/g, " ").trim();
    const lines = raw.replace(/[ \t]+/g, " ");
    const focusables = [...main.querySelectorAll("a[href], button:not([disabled]), input, select, textarea, summary, [tabindex]:not([tabindex='-1'])")].filter((e) => e.offsetParent !== null && !(e.closest("details:not([open])") && !e.matches("details > summary")));
    return { text, lines, h1: (main.querySelector("h1") || {}).innerText || "", words: text.split(" ").length, tabStops: focusables.length, height: document.documentElement.scrollHeight, title: document.title, sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth };
  });
  if (/could not find|did not load/i.test(info.h1)) findings.push([r, "error-page", info.h1, ""]);
  if (info.sw > info.cw + 1) findings.push([r, "horizontal-scroll", `${info.sw} > ${info.cw}`, ""]);
  for (const f of checkText(r, info.text, info.lines)) findings.push([r, ...f]);
  if ((r.startsWith("/series/") || r.startsWith("/class/")) && hrFirst && !info.text.includes(hrFirst.slice(0, 40))) findings.push([r, "hr-disclaimer-missing", "", ""]);
  if (r.startsWith("/compare/") && pathsNotice && !info.text.includes(pathsNotice.slice(0, 30))) findings.push([r, "paths-notice-missing", "", ""]);
  metrics.push({ r, words: info.words, tabStops: info.tabStops, height: info.height, title: info.title });
  if (++n % 200 === 0) console.error(`[check-rendered] ${n}/${list.length}`);
}
await browser.close();

// ---------------------------------------------------------------- report
const byRule = {};
for (const f of findings) byRule[f[1]] = (byRule[f[1]] || 0) + 1;
const hard = findings.filter((f) => !/percent \(review\)/.test(f[1]));
const kind = (r) => r.split("/")[1] || "home";
const agg = {};
for (const m of metrics) { const k = kind(m.r); (agg[k] = agg[k] || []).push(m); }
const med = (xs) => { const s = xs.slice().sort((a, b) => a - b); return s[Math.floor(s.length / 2)]; };
const summary = Object.fromEntries(Object.entries(agg).map(([k, ms]) => [k, { pages: ms.length, medianWords: med(ms.map((m) => m.words)), medianTabStops: med(ms.map((m) => m.tabStops)), medianHeight390: med(ms.map((m) => m.height)), maxHeight390: Math.max(...ms.map((m) => m.height)) }]));
const outDir = process.env.RC_OUT_DIR ? resolve(process.env.RC_OUT_DIR) : join(HERE, "..", "docs", "qa"); // RC_OUT_DIR lets a developer keep the lead's report
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "rendered-check.json"), JSON.stringify({ base: BASE, routes: list.length, byRule, errors, external: [...new Set(external)], summary, findings: findings.slice(0, 400) }, null, 1));
console.log(JSON.stringify({ routes: list.length, byRule, errors: errors.length, external: [...new Set(external)].length, summary }, null, 1));
for (const f of hard.slice(0, 25)) console.log("  ", f.join(" | ").slice(0, 260));
process.exit(hard.length || errors.length || external.length ? 1 : 0);
