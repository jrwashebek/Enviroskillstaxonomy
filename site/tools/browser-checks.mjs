#!/usr/bin/env node
// Browser checks for the built explorer (WP-12 acceptance). Uses a local Chromium through playwright-core and axe-core;
// both are dev-only tools, never shipped. Licence: Apache-2.0.
//
//  1. Network: on every sampled page, every request goes to the local origin; scripts make no request after load.
//  2. Accessibility: axe-core with WCAG 2.0/2.1/2.2 A and AA rules, run twice per page (as loaded, and with every
//     <details> opened); best-practice rules reported but not gating.
//  3. Reflow at 320 CSS px: no horizontal page scroll (WCAG 1.4.10). Focus is visible on the first 12 Tab stops.
//  4. Gap check privacy: rate, type a sentinel note, summarise, save, clear, reopen the saved file. No request is
//     made, the address bar never changes, no cookie or storage is written, and the sentinel appears only in the
//     downloaded file. Team grid: shows nothing with 4 files, counts with 5.
//  5. Search: results appear with no request.
// Writes reports/browser-checks.json. Exit 1 on any gating failure.
import { chromium } from "playwright-core";
import { existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { startServer } from "./serve.mjs";

const SITE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const OUT = join(SITE, "_site");
const SCRATCH = join(SITE, ".cache", "browser-checks");
mkdirSync(SCRATCH, { recursive: true });
if (!process.env.PLAYWRIGHT_BROWSERS_PATH && existsSync("/opt/pw-browsers")) process.env.PLAYWRIGHT_BROWSERS_PATH = "/opt/pw-browsers";
const AXE = readFileSync(join(SITE, "node_modules", "axe-core", "axe.min.js"), "utf-8");
const AXE_VERSION = JSON.parse(readFileSync(join(SITE, "node_modules", "axe-core", "package.json"), "utf-8")).version;
const TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];

function firstDir(p) { try { return readdirSync(join(OUT, p), { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name).sort(); } catch { return []; } }
function sample() {
  const s = ["/", "/roles/", "/gap-check/", "/gap-check/competencies/", "/gap-check/team/", "/pathways/", "/whats-coming/",
    "/federal-series/", "/state-classes/", "/competencies/", "/modules/", "/evidence/", "/challenge/", "/about/privacy/",
    "/about/accessibility/", "/about/security/", "/download/", "/search/", "/404.html"];
  const roles = firstDir("roles");
  for (const r of roles.slice(0, 3)) {
    s.push(`/roles/${r}/`);
    for (const v of firstDir(`roles/${r}`).slice(0, 2)) { s.push(`/roles/${r}/${v}/`); s.push(`/gap-check/${r}/${v}/`); s.push(`/pathways/${r}/${v}/`); }
  }
  const fed = firstDir("roles").flatMap((r) => firstDir(`roles/${r}`).filter((v) => v === "federal").map((v) => `/roles/${r}/${v}/`));
  if (fed[0]) s.push(fed[0]);
  const series = firstDir("federal-series"); s.push(...["0401", "0029", "0460"].filter((x) => series.includes(x)).map((x) => `/federal-series/${x}/`));
  const classes = firstDir("state-classes"); s.push(...classes.slice(0, 2).map((x) => `/state-classes/${x}/`));
  const comps = firstDir("competencies"); s.push(...["db-c09", "v1-3-2-5", "dc-cand-13", "sc-c02"].filter((x) => comps.includes(x)).map((x) => `/competencies/${x}/`));
  const mods = firstDir("modules"); if (mods[0]) s.push(`/modules/${mods[0]}/`);
  return [...new Set(s)];
}

const report = { axeVersion: AXE_VERSION, tags: TAGS, pages: [], gapCheck: null, teamGrid: null, search: null, failures: [] };
const server = await startServer({ port: 0, root: OUT });
const ORIGIN = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch();
const fail = (where, msg) => report.failures.push({ where, msg });

async function axe(page) {
  await page.evaluate(AXE);
  return page.evaluate(async (tags) => {
    const r = await window.axe.run(document, { runOnly: { type: "tag", values: tags }, resultTypes: ["violations", "incomplete"] });
    const bp = await window.axe.run(document, { runOnly: { type: "tag", values: ["best-practice"] }, resultTypes: ["violations"] });
    const slim = (v) => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length, targets: v.nodes.slice(0, 3).map((n) => n.target.join(" ")) });
    return { violations: r.violations.map(slim), incomplete: r.incomplete.map(slim), bestPractice: bp.violations.map(slim) };
  }, TAGS);
}

try {
  const ctx = await browser.newContext({ acceptDownloads: true });
  for (const url of sample()) {
    const page = await ctx.newPage();
    const external = [], csp = [];
    page.on("request", (r) => { const u = r.url(); if (!u.startsWith(ORIGIN) && !u.startsWith("data:") && !u.startsWith("blob:")) external.push(u); });
    page.on("console", (m) => { if (/Content Security Policy|Refused to/i.test(m.text())) csp.push(m.text()); });
    const resp = await page.goto(ORIGIN + url, { waitUntil: "load" });
    const entry = { url, status: resp ? resp.status() : null };
    const a1 = await axe(page);
    await page.evaluate(() => document.querySelectorAll("details").forEach((d) => { d.open = true; }));
    const a2 = await axe(page);
    const merge = (k) => { const m = new Map(); for (const v of [...a1[k], ...a2[k]]) if (!m.has(v.id) || m.get(v.id).nodes < v.nodes) m.set(v.id, v); return [...m.values()]; };
    entry.violations = merge("violations"); entry.incomplete = merge("incomplete").map((v) => v.id); entry.bestPractice = merge("bestPractice").map((v) => v.id);
    await page.setViewportSize({ width: 320, height: 800 });
    await page.evaluate(() => document.querySelectorAll("details").forEach((d) => { d.open = false; }));
    entry.reflow = await page.evaluate(() => ({ scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth }));
    await page.setViewportSize({ width: 1280, height: 900 });
    entry.focus = [];
    await page.keyboard.press("Tab");
    for (let i = 0; i < 12; i++) {
      const f = await page.evaluate(() => {
        const e = document.activeElement; if (!e || e === document.body) return null;
        const s = getComputedStyle(e);
        return { tag: e.tagName.toLowerCase(), text: (e.textContent || e.getAttribute("aria-label") || "").trim().slice(0, 40), outline: s.outlineStyle !== "none" && parseFloat(s.outlineWidth) >= 2, shadow: s.boxShadow !== "none" };
      });
      if (f) entry.focus.push(f);
      await page.keyboard.press("Tab");
    }
    entry.external = external; entry.csp = csp;
    if (entry.status !== 200 && url !== "/404.html") fail(url, `HTTP ${entry.status}`);
    if (external.length) fail(url, `external requests: ${external.join(", ")}`);
    if (csp.length) fail(url, `CSP violations: ${csp.join(" | ")}`);
    if (entry.violations.length) fail(url, `axe violations: ${entry.violations.map((v) => `${v.id} (${v.nodes})`).join(", ")}`);
    if (entry.reflow.scrollWidth > entry.reflow.clientWidth + 1) fail(url, `horizontal scroll at 320 px (${entry.reflow.scrollWidth}px)`);
    const nofocus = entry.focus.filter((f) => !f.outline && !f.shadow);
    if (nofocus.length) fail(url, `focus not visible on ${nofocus.map((f) => f.tag + ":" + f.text).join("; ")}`);
    report.pages.push(entry);
    await page.close();
  }

  // ---------------------------------------------------------------- gap check privacy
  const SENTINEL = "SENTINEL-NOTE-7f3a";
  const gapUrl = (() => { const r = firstDir("gap-check").filter((d) => !["competencies", "team"].includes(d))[0]; const v = r ? firstDir(`gap-check/${r}`)[0] : null; return r && v ? `/gap-check/${r}/${v}/` : "/gap-check/competencies/"; })();
  {
    const page = await ctx.newPage();
    const reqs = [];
    page.on("request", (r) => reqs.push({ url: r.url(), post: r.postData() || "" }));
    await page.goto(ORIGIN + gapUrl, { waitUntil: "load" });
    const atLoad = reqs.length;
    const startUrl = page.url();
    const fs = page.locator("fieldset.emst-rate[data-competency]");
    const n = Math.min(await fs.count(), 4);
    for (let i = 0; i < n; i++) {
      const f = fs.nth(i);
      const det = f.locator("xpath=ancestor::details[1]");
      if (await det.count()) await det.evaluate((d) => { d.open = true; });
      const radios = f.locator('[data-role="self"] input[type=radio]');
      await radios.nth(i % 2 === 0 ? 0 : 1).check();
      const aim = f.locator('[data-role="aim"]');
      if (await aim.count()) await aim.selectOption({ index: (await aim.locator("option").count()) - 1 });
    }
    await fs.nth(0).locator('[data-role="note"]').fill(SENTINEL);
    await page.click('[data-action="summary"]');
    const summaryText = await page.locator("[data-summary]").innerText();
    const dl = page.waitForEvent("download");
    await page.click('[data-action="save"]');
    const d = await dl;
    const savedPath = join(SCRATCH, "saved.emst.json");
    await d.saveAs(savedPath);
    const saved = JSON.parse(readFileSync(savedPath, "utf-8"));
    await page.click('[data-action="clear"]');
    const clearedChecked = await page.locator('input[type=radio][name^="self-"]:checked').count();
    await page.setInputFiles("#emst-open-file", savedPath);
    await page.waitForTimeout(300);
    const restored = await page.locator('input[type=radio][name^="self-"]:checked').count();
    const noteBack = await fs.nth(0).locator('[data-role="note"]').inputValue();
    const storage = await page.evaluate(() => ({ cookie: document.cookie, local: (() => { try { return localStorage.length; } catch { return -1; } })(), session: (() => { try { return sessionStorage.length; } catch { return -1; } })() }));
    const after = reqs.slice(atLoad).filter((r) => !r.url.startsWith("blob:") && !r.url.startsWith("data:"));
    const leaked = reqs.filter((r) => r.url.includes(SENTINEL) || r.post.includes(SENTINEL));
    report.gapCheck = {
      page: gapUrl, rated: n, requestsAtLoad: atLoad, requestsAfterLoad: after.map((r) => r.url), sentinelInRequests: leaked.length,
      urlUnchanged: page.url() === startUrl, savedSchema: saved.schema_version, savedRatings: saved.ratings.length,
      savedKeys: Object.keys(saved), sentinelInFile: JSON.stringify(saved).includes(SENTINEL), clearedChecked, restored, noteRestored: noteBack === SENTINEL,
      storage, summaryShown: /development priorities/i.test(summaryText),
    };
    const g = report.gapCheck;
    if (after.length) fail("gap-check", `requests after load: ${after.map((r) => r.url).join(", ")}`);
    if (leaked.length) fail("gap-check", "sentinel note appeared in a request");
    if (!g.urlUnchanged) fail("gap-check", "address bar changed");
    if (g.savedSchema !== "emst-gap-check@1" || !g.sentinelInFile || g.savedRatings !== n) fail("gap-check", "saved file incomplete");
    if (JSON.stringify(g.savedKeys) !== JSON.stringify(["schema_version", "release_id", "role_variant_id", "level", "mode", "ratings"])) fail("gap-check", `unexpected saved fields ${g.savedKeys}`);
    if (g.clearedChecked !== 0 || g.restored !== n || !g.noteRestored) fail("gap-check", "clear/reopen did not round-trip");
    if (storage.cookie || storage.local > 0 || storage.session > 0) fail("gap-check", "cookie or browser storage written");
    if (!g.summaryShown) fail("gap-check", "summary not shown");

    // Team grid from the saved file
    const team = await ctx.newPage();
    const treqs = [];
    team.on("request", (r) => treqs.push(r.url()));
    await team.goto(ORIGIN + "/gap-check/team/", { waitUntil: "load" });
    const tload = treqs.length;
    const mk = (k) => { const p = join(SCRATCH, `team-${k}.emst.json`); const x = JSON.parse(JSON.stringify(saved)); x.ratings = x.ratings.map((r, i) => ({ ...r, self: ["none", "L1", "L2", "L1", "unsure"][(i + k) % 5], note: SENTINEL })); writeFileSync(p, JSON.stringify(x)); return p; };
    const four = [0, 1, 2, 3].map(mk), five = [...four, mk(4)];
    await team.setInputFiles("#emst-team-files", four); await team.waitForTimeout(300);
    const gridWith4 = await team.locator("[data-grid] table").count();
    await team.setInputFiles("#emst-team-files", five); await team.waitForTimeout(300);
    const gridWith5 = await team.locator("[data-grid] table").count();
    const gridText = await team.locator("[data-grid]").innerText();
    report.teamGrid = { gridWith4, gridWith5, sentinelShown: gridText.includes(SENTINEL), requestsAfterLoad: treqs.slice(tload).filter((u) => !u.startsWith("blob:")) };
    if (gridWith4 !== 0 || gridWith5 !== 1) fail("team-grid", `minimum cell rule not applied (4 files: ${gridWith4}, 5 files: ${gridWith5})`);
    if (report.teamGrid.sentinelShown) fail("team-grid", "notes shown in team grid");
    if (report.teamGrid.requestsAfterLoad.length) fail("team-grid", "requests after load");
    await team.close(); await page.close();
  }

  // ---------------------------------------------------------------- search
  {
    const page = await ctx.newPage();
    const reqs = [];
    page.on("request", (r) => reqs.push(r.url()));
    await page.goto(ORIGIN + "/search/", { waitUntil: "load" });
    const atLoad = reqs.length;
    await page.fill("#emst-q", "stormwater inspect");
    await page.waitForTimeout(400);
    const results = await page.locator("[data-results] li").count();
    report.search = { results, requestsAfterTyping: reqs.slice(atLoad) };
    if (!results) fail("search", "no results for a known term");
    if (reqs.length > atLoad) fail("search", `requests after typing: ${reqs.slice(atLoad).join(", ")}`);
    await page.close();
  }
} finally {
  await browser.close();
  server.close();
}

const summary = {
  pages: report.pages.length,
  pagesWithAxeViolations: report.pages.filter((p) => p.violations.length).length,
  axeViolationIds: [...new Set(report.pages.flatMap((p) => p.violations.map((v) => v.id)))],
  axeIncompleteIds: [...new Set(report.pages.flatMap((p) => p.incomplete))],
  bestPracticeIds: [...new Set(report.pages.flatMap((p) => p.bestPractice))],
  externalRequests: report.pages.reduce((s, p) => s + p.external.length, 0),
  reflowFailures: report.pages.filter((p) => p.reflow.scrollWidth > p.reflow.clientWidth + 1).map((p) => p.url),
  failures: report.failures.length,
};
report.summary = summary;
mkdirSync(join(SITE, "reports"), { recursive: true });
writeFileSync(join(SITE, "reports", "browser-checks.json"), JSON.stringify(report, null, 1));
console.log(`[browser] ${summary.pages} pages; axe (WCAG 2.2 A/AA, axe-core ${AXE_VERSION}) violations on ${summary.pagesWithAxeViolations} pages ${JSON.stringify(summary.axeViolationIds)}; needs-review ${JSON.stringify(summary.axeIncompleteIds)}; external requests ${summary.externalRequests}; reflow failures ${summary.reflowFailures.length}`);
console.log(`[browser] gap check: ${JSON.stringify(report.gapCheck)}`);
console.log(`[browser] team grid: ${JSON.stringify(report.teamGrid)}; search: ${JSON.stringify(report.search)}`);
if (report.failures.length) {
  console.error(`[browser] FAILED (${report.failures.length}):`);
  for (const f of report.failures.slice(0, 40)) console.error(`  ${f.where}: ${f.msg}`);
  process.exit(1);
}
console.log("[browser] OK");
