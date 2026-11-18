// Render the generated guidebook (gitbook/site) as one self-contained HTML page that reads like a GitBook site, so the
// project lead can review it before anything is connected to GitBook. It is an approximation: GitBook's own layout,
// search and page actions will differ. Optionally runs axe-core on every page of the preview.
//
// Usage (from the repository root):
//   node prototype/public-ui/tools/preview-gitbook.mjs <out.html> [--axe]
// Licence: Apache-2.0.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { join, resolve, dirname, posix } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const HERE = dirname(fileURLToPath(import.meta.url));
const UI = resolve(HERE, "..");
const ROOT = resolve(UI, "..", "..");
const SITE = join(UI, "gitbook", "site");
const OUT = resolve(process.argv[2] || "gitbook-preview.html");
const AXE = process.argv.includes("--axe");
const require = createRequire(import.meta.url);
const MarkdownIt = require(join(ROOT, "site", "node_modules", "markdown-it"));
const yaml = require(join(ROOT, "site", "node_modules", "js-yaml"));

// ---------------------------------------------------------------- read the site in SUMMARY order
const summary = readFileSync(join(SITE, "SUMMARY.md"), "utf8");
const nav = []; let group = null;
for (const line of summary.split("\n")) {
  const g = line.match(/^## (.+)$/); if (g) { group = { title: g[1], items: [] }; nav.push(group); continue; }
  const m = line.match(/^(\s*)\* \[(.+)\]\((.+)\)$/); if (!m) continue;
  const item = { path: m[3], title: m[2].replace(/\\(.)/g, "$1"), depth: m[1].length / 2 };
  if (!group) { group = { title: null, items: [] }; nav.push(group); }
  group.items.push(item);
}
const order = nav.flatMap((g) => g.items.map((i) => i.path));
const pid = (p) => p.replace(/\.md$/, "").replace(/(^|\/)README$/, "$1index").replace(/[^a-z0-9]+/gi, "-").replace(/^-|-$/g, "").toLowerCase();
const slug = (s) => String(s).toLowerCase().replace(/[’'"“”]/g, "").replace(/[^a-z0-9\s-]/g, " ").trim().replace(/\s+/g, "-").replace(/-+/g, "-");
const escHtml = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

const md = new MarkdownIt({ html: false, linkify: false, typographer: false });
const defaultLink = md.renderer.rules.link_open || ((t, i, o, e, s) => s.renderToken(t, i, o));
md.renderer.rules.link_open = (tokens, idx, opts, env, self) => {
  const t = tokens[idx]; const href = t.attrGet("href") || "";
  if (/^https?:/.test(href)) { t.attrSet("target", "_blank"); t.attrSet("rel", "noopener"); t.attrJoin("class", "ext"); }
  else {
    const [p, a] = href.split("#");
    const target = p ? posix.normalize(posix.join(posix.dirname(env.path), p)) : env.path;
    t.attrSet("href", `#${pid(target)}${a ? `--${a}` : ""}`);
  }
  return defaultLink(tokens, idx, opts, env, self);
};
md.renderer.rules.heading_open = (tokens, idx, opts, env, self) => {
  const t = tokens[idx]; const text = tokens[idx + 1].children.map((c) => c.content).join("");
  if (t.tag !== "h1") { t.attrSet("id", `${env.id}--${slug(text)}`); env.lastHeading = text; }
  return self.renderToken(tokens, idx, opts);
};
// Each scrollable table is a labelled region (keyboard users can scroll it); labels are unique on a page.
md.renderer.rules.table_open = (tokens, idx, opts, env) => {
  const base = `${env.lastHeading || env.title} (table)`; env.tables = env.tables || {};
  const n = (env.tables[base] = (env.tables[base] || 0) + 1);
  return `<div class="table-wrap" tabindex="0" role="region" aria-label="${escHtml(n > 1 ? `${base.slice(0, -1)} ${n})` : base)}"><table>`;
};
md.renderer.rules.table_close = () => "</table></div>";

const LABEL = { info: "Note", warning: "Warning", danger: "Important", success: "Tip" };
const pages = order.map((path) => {
  const raw = readFileSync(join(SITE, path), "utf8");
  const fm = raw.match(/^---\n([\s\S]*?)\n---\n/);
  const meta = fm ? yaml.load(fm[1]) : {};
  let body = fm ? raw.slice(fm[0].length) : raw;
  const title = (body.match(/^# (.+)$/m) || [, path])[1].replace(/\\(.)/g, "$1");
  body = body.replace(/^# .+\n/m, "");
  const env = { path, id: pid(path), title };
  // GitBook hint blocks become notes with a written label, so the kind of note never rests on colour alone.
  const parts = body.split(/\{% hint style="(\w+)" %\}\n([\s\S]*?)\n\{% endhint %\}/);
  let html = "";
  for (let i = 0; i < parts.length; i++) {
    if (i % 3 === 0) html += md.render(parts[i], env);
    else if (i % 3 === 1) { const style = parts[i], inner = md.render(parts[i + 1], env); html += `<div class="hint hint--${style}" role="note"><span class="hint__label">${LABEL[style] || "Note"}</span><div class="hint__body">${inner}</div></div>`; i++; }
  }
  const [main, foot] = html.split(/<hr>\n?/);
  const toc = [...(main || "").matchAll(/<h2 id="([^"]+)">([\s\S]*?)<\/h2>/g)].map((m) => [m[1], m[2]]);
  return { path, id: env.id, title, description: meta.description || "", main, foot: foot || "", toc, text: `${title} ${meta.description || ""} ${(main || "").replace(/<[^>]+>/g, " ")}`.replace(/\s+/g, " ") };
});
const byId = Object.fromEntries(pages.map((p) => [p.id, p]));

// ---------------------------------------------------------------- page HTML
const navHtml = nav.map((g) => `${g.title ? `<p class="nav__group">${escHtml(g.title)}</p>` : ""}<ul class="nav__list">${g.items.map((i) =>
  `<li class="nav__item nav__item--d${i.depth}"><a href="#${pid(i.path)}" data-page="${pid(i.path)}">${escHtml(i.title)}</a></li>`).join("")}</ul>`).join("");
const articles = pages.map((p, n) => {
  const prev = pages[n - 1], next = pages[n + 1];
  const crumbs = nav.find((g) => g.items.some((i) => i.path === p.path))?.title;
  return `<article class="page" id="pg-${p.id}" data-page="${p.id}" data-title="${escHtml(p.title)}" hidden>
<header class="page__head">${crumbs ? `<p class="page__group">${escHtml(crumbs)}</p>` : ""}<h1 tabindex="-1">${escHtml(p.title)}</h1>${p.description ? `<p class="page__desc">${escHtml(p.description)}</p>` : ""}</header>
<div class="prose">${p.main}</div>
<nav class="pager" aria-label="Previous and next page">${prev ? `<a class="pager__link" href="#${prev.id}"><span class="pager__dir">Previous</span><span class="pager__title">${escHtml(prev.title)}</span></a>` : "<span></span>"}${next ? `<a class="pager__link pager__link--next" href="#${next.id}"><span class="pager__dir">Next</span><span class="pager__title">${escHtml(next.title)}</span></a>` : ""}</nav>
<footer class="page__foot">${p.foot}</footer>
${p.toc.length ? `<template class="toc">${p.toc.map(([id, t]) => `<li><a href="#${id}">${t}</a></li>`).join("")}</template>` : ""}
</article>`;
}).join("\n");
const searchIndex = JSON.stringify(pages.map((p) => ({ id: p.id, t: p.title, x: p.text.slice(0, 4000) })));
const release = (pages[0].foot.match(/release ([\w.-]+), ([^.]+)\./) || [])[1] || "";

const html = `<title>EMST Guidebook Preview</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: a GitBook-style reading room (header, grouped sidebar, one page, "On this page"), in the Ground Truth palette.
   GitBook allows one primary font and one code font, so the preview uses only Source Serif 4 and IBM Plex Mono. */
:root {
  --paper: #f6f5f0; --surface: #ffffff; --mist: #e2e8e0; --haze: #ece6d6;
  --ink: #1b221e; --ink-2: #4d5a52; --rule: #c3ccc0;
  --pine: #23392f; --moss: #4f6b56; --wash: #456a7e; --signal: #8f3f14;
  --info-bg: #e7efe9; --info-edge: #4f6b56; --warn-bg: #f7eadf; --warn-edge: #b4521f;
  --focus: #456a7e;
  --serif: "Source Serif 4", Georgia, "Times New Roman", serif;
  --mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper: #141916; --surface: #1b211d; --mist: #233029; --haze: #2a2a22;
  --ink: #e6ebe5; --ink-2: #b2bdb4; --rule: #34423a;
  --pine: #a9cdb8; --moss: #8fb59c; --wash: #9cc1d4; --signal: #f0a070;
  --info-bg: #1f2c25; --info-edge: #8fb59c; --warn-bg: #33251b; --warn-edge: #f0a070; --focus: #9cc1d4; color-scheme: dark; } }
:root[data-theme="dark"] {
  --paper: #141916; --surface: #1b211d; --mist: #233029; --haze: #2a2a22;
  --ink: #e6ebe5; --ink-2: #b2bdb4; --rule: #34423a;
  --pine: #a9cdb8; --moss: #8fb59c; --wash: #9cc1d4; --signal: #f0a070;
  --info-bg: #1f2c25; --info-edge: #8fb59c; --warn-bg: #33251b; --warn-edge: #f0a070; --focus: #9cc1d4; color-scheme: dark; }
* { box-sizing: border-box; }
body { background: var(--paper); color: var(--ink); font: 400 1.0625rem/1.6 var(--serif); }
a { color: var(--pine); text-underline-offset: 0.18em; text-decoration-thickness: 1px; }
a:hover { text-decoration-thickness: 2px; }
:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; border-radius: 2px; }
[tabindex="-1"]:focus { outline: none; } /* headings and the main area take focus only from page changes */
.skip { position: absolute; left: -999px; top: 0; }
.skip:focus { left: max(16px, env(safe-area-inset-left, 0px)); top: calc(8px + env(safe-area-inset-top, 0px)); z-index: 30; background: var(--surface); padding: 0.5rem 0.75rem; }
.vh { position: absolute !important; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }

.preview-note { background: var(--haze); border-bottom: 1px solid var(--rule); font: 400 0.8125rem/1.45 var(--mono);
  padding-block: 0.5rem; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.preview-note strong { font-weight: 500; }
.preview-note p { margin: 0; max-width: 84rem; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--surface); }
.top { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--surface); border-bottom: 1px solid var(--rule);
  display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; padding-block: 0.625rem;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.brand { display: flex; align-items: baseline; gap: 0.5rem; text-decoration: none; color: var(--ink); margin-right: auto; }
.brand__mark { font: 700 1.125rem/1 var(--serif); letter-spacing: 0.02em; color: var(--pine); }
.brand__name { font: 400 0.9375rem/1.2 var(--serif); color: var(--ink-2); }
.search { position: relative; flex: 1 1 14rem; max-width: 22rem; }
.search input { width: 100%; font: 400 0.9375rem/1.2 var(--serif); padding: 0.5rem 0.75rem; border: 1px solid var(--rule); border-radius: 6px; background: var(--paper); color: var(--ink); }
.results { position: absolute; top: calc(100% + 4px); left: 0; right: 0; background: var(--surface); border: 1px solid var(--rule); border-radius: 6px; margin: 0; padding: 0.25rem 0; list-style: none; max-height: 60vh; overflow: auto; box-shadow: 0 8px 24px rgb(0 0 0 / 0.12); }
.results a { display: block; padding: 0.5rem 0.75rem; text-decoration: none; }
.results a:hover, .results a:focus-visible { background: var(--mist); }
.results small { display: block; color: var(--ink-2); font-size: 0.8125rem; }
.top__link { font: 400 0.875rem/1 var(--mono); }
.menu-btn { display: none; font: 500 0.875rem/1 var(--mono); background: none; border: 1px solid var(--rule); border-radius: 6px; padding: 0.5rem 0.75rem; color: var(--ink); }

.shell { display: grid; grid-template-columns: 17rem minmax(0, 1fr) 13rem; gap: 2.5rem; max-width: 84rem; margin: 0 auto;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.nav { position: sticky; top: 3.75rem; align-self: start; max-height: calc(100vh - 4.5rem); overflow: auto; padding-block: 1.5rem 3rem; font-size: 0.9375rem; }
.nav__group { font: 500 0.75rem/1.2 var(--mono); text-transform: uppercase; letter-spacing: 0.08em; color: var(--moss); margin: 1.5rem 0 0.375rem; }
.nav__list { list-style: none; margin: 0; padding: 0; }
.nav__item a { display: block; padding: 0.3rem 0.625rem; border-radius: 6px; text-decoration: none; color: var(--ink-2); line-height: 1.35; }
.nav__item--d1 a { padding-left: 1.5rem; font-size: 0.875rem; }
.nav__item a:hover { background: var(--mist); color: var(--ink); }
.nav__item a[aria-current="page"] { background: var(--mist); color: var(--pine); font-weight: 600; }
main { min-width: 0; padding-block: 2rem 4rem; }
.page { max-width: 46rem; }
.page__group { font: 500 0.75rem/1.2 var(--mono); text-transform: uppercase; letter-spacing: 0.08em; color: var(--moss); margin: 0 0 0.5rem; }
h1 { font: 700 clamp(1.875rem, 1.5rem + 1.4vw, 2.5rem)/1.15 var(--serif); margin: 0; text-wrap: balance; }
.page__desc { color: var(--ink-2); font-size: 1.125rem; margin: 0.625rem 0 1.75rem; max-width: 40rem; }
.prose { max-width: 42rem; }
.prose h2 { font: 700 1.5rem/1.25 var(--serif); margin: 2.25rem 0 0.75rem; text-wrap: balance; scroll-margin-top: 4.5rem; }
.prose h3 { font: 600 1.1875rem/1.3 var(--serif); margin: 1.75rem 0 0.5rem; scroll-margin-top: 4.5rem; }
.prose p, .prose ul, .prose ol { margin: 0 0 1rem; }
.prose p, .prose li, .prose blockquote, .page__foot p, td { overflow-wrap: anywhere; }
.prose li + li { margin-top: 0.35rem; }
.prose blockquote { margin: 0 0 1rem; padding: 0.75rem 1rem; border-left: 3px solid var(--wash); background: var(--surface); }
.prose blockquote p { margin: 0; }
.prose code { font: 0.9em var(--mono); }
.hint { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 0.25rem 0.75rem; align-items: baseline; margin: 0 0 1.25rem; padding: 0.875rem 1rem; border-radius: 6px; border: 1px solid; }
.hint--info { background: var(--info-bg); border-color: var(--info-edge); }
.hint--warning, .hint--danger { background: var(--warn-bg); border-color: var(--warn-edge); }
.hint__label { font: 500 0.75rem/1.6 var(--mono); text-transform: uppercase; letter-spacing: 0.08em; color: var(--moss); }
.hint--warning .hint__label, .hint--danger .hint__label { color: var(--signal); }
.hint__body > :last-child { margin-bottom: 0; }
.hint__body p { margin: 0 0 0.5rem; }
.page > .prose > .hint:first-child { font-size: 0.9375rem; }
.table-wrap { overflow-x: auto; margin: 0 0 1.25rem; border: 1px solid var(--rule); border-radius: 6px; background: var(--surface); }
table { border-collapse: collapse; width: 100%; font-size: 0.9375rem; }
th, td { text-align: left; vertical-align: top; padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--rule); }
th { font: 500 0.8125rem/1.3 var(--mono); color: var(--ink-2); background: var(--mist); }
tr:last-child td { border-bottom: 0; }
td[style*="right"], th[style*="right"] { font-variant-numeric: tabular-nums; }
.pager { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 3rem 0 1.5rem; }
.pager__link { display: flex; flex-direction: column; gap: 0.25rem; padding: 0.875rem 1rem; border: 1px solid var(--rule); border-radius: 6px; text-decoration: none; background: var(--surface); }
.pager__link--next { text-align: right; grid-column: 2; }
.pager__dir { font: 500 0.75rem/1.2 var(--mono); text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-2); }
.pager__title { font-weight: 600; }
.page__foot { border-top: 1px solid var(--rule); padding-top: 1rem; font-size: 0.875rem; color: var(--ink-2); max-width: 42rem; }
.page__foot p { margin: 0 0 0.625rem; }
.aside { position: sticky; top: 3.75rem; align-self: start; padding-block: 2rem; font-size: 0.875rem; }
.aside h2 { font: 500 0.75rem/1.2 var(--mono); text-transform: uppercase; letter-spacing: 0.08em; color: var(--moss); margin: 0 0 0.5rem; }
.aside ul { list-style: none; margin: 0; padding: 0 0 0 0.75rem; border-left: 1px solid var(--rule); }
.aside li { margin: 0 0 0.375rem; }
.aside a { text-decoration: none; color: var(--ink-2); }
.aside a:hover { color: var(--pine); }
@media (max-width: 72rem) { .shell { grid-template-columns: 15rem minmax(0, 1fr); } .aside { display: none; } }
@media (max-width: 52rem) {
  .shell { grid-template-columns: minmax(0, 1fr); gap: 0; }
  .menu-btn { display: inline-block; }
  .nav { position: static; max-height: none; padding-block: 0.5rem 1rem; border-bottom: 1px solid var(--rule); }
  .nav:not(.is-open) { display: none; }
  .search { order: 3; flex-basis: 100%; max-width: none; }
  .top { position: static; }
  .nav, .aside, .prose h2, .prose h3 { scroll-margin-top: 1rem; }
}
@media (prefers-reduced-motion: no-preference) { .nav__item a, .results a { transition: background-color 120ms ease; } }
</style>
<script>document.documentElement.lang = "en";</script>
<a class="skip" href="#main">Skip to the page</a>
<aside class="preview-note" aria-label="About this preview"><p><strong>Preview, not yet on GitBook.</strong> This is how the EMST guidebook's pages read, built from release ${escHtml(release)}. GitBook's own layout, search and page actions will differ.</p></aside>
<header class="top">
  <a class="brand" href="#index"><span class="brand__mark">EMST</span><span class="brand__name">Environmental Management Skills Taxonomy</span></a>
  <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  <div class="search" role="search">
    <label class="vh" for="q">Search the guidebook</label>
    <input id="q" type="search" placeholder="Search the guidebook" autocomplete="off" aria-controls="results" aria-describedby="q-status">
    <ul class="results" id="results" hidden></ul>
    <p class="vh" id="q-status" role="status" aria-live="polite"></p>
  </div>
  <a class="top__link ext" href="https://github.com/jrwashebek/Enviroskillstaxonomy" target="_blank" rel="noopener">GitHub</a>
</header>
<div class="shell">
  <nav class="nav" id="nav" aria-label="Guidebook">${navHtml}</nav>
  <main id="main" tabindex="-1">${articles}</main>
  <aside class="aside" aria-label="On this page"><h2>On this page</h2><ul id="toc"></ul></aside>
</div>
<script>
(() => {
  const pages = [...document.querySelectorAll("article.page")];
  const links = [...document.querySelectorAll(".nav a[data-page]")];
  const toc = document.getElementById("toc"), aside = document.querySelector(".aside");
  const nav = document.getElementById("nav"), menu = document.getElementById("menu-btn");
  const INDEX = ${searchIndex};
  let current = null;
  function show(hash, focus) {
    const [id, anchor] = (hash || "").replace(/^#/, "").split("--");
    // Articles carry a "pg-" prefix so the browser never jumps to one on its own; headings keep page--anchor ids.
    const page = document.getElementById("pg-" + id) || pages[0];
    if (page !== current) {
      pages.forEach((p) => { p.hidden = p !== page; });
      links.forEach((a) => (a.dataset.page === page.dataset.page ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current")));
      const tpl = page.querySelector("template.toc");
      toc.replaceChildren(...(tpl ? tpl.content.cloneNode(true).childNodes : []));
      aside.hidden = !tpl;
      document.title = page.dataset.title + " · EMST Guidebook Preview";
      current = page;
    }
    const target = anchor && document.getElementById(page.dataset.page + "--" + anchor);
    if (target) { target.setAttribute("tabindex", "-1"); target.scrollIntoView(); if (focus) target.focus({ preventScroll: true }); }
    else { window.scrollTo(0, 0); if (focus) page.querySelector("h1").focus({ preventScroll: true }); }
    if (window.matchMedia("(max-width: 52rem)").matches) { nav.classList.remove("is-open"); menu.setAttribute("aria-expanded", "false"); }
  }
  window.addEventListener("hashchange", () => show(location.hash, true));
  show(location.hash, false);
  menu.addEventListener("click", () => { const open = nav.classList.toggle("is-open"); menu.setAttribute("aria-expanded", String(open)); });
  const q = document.getElementById("q"), results = document.getElementById("results"), status = document.getElementById("q-status");
  q.addEventListener("input", () => {
    const words = q.value.toLowerCase().split(/\\s+/).filter(Boolean);
    if (!words.length) { results.hidden = true; status.textContent = ""; return; }
    const hits = INDEX.map((p) => ({ p, s: words.reduce((n, w) => n + (p.t.toLowerCase().includes(w) ? 5 : 0) + (p.x.toLowerCase().includes(w) ? 1 : 0), 0), all: words.every((w) => (p.t + " " + p.x).toLowerCase().includes(w)) }))
      .filter((h) => h.all).sort((a, b) => b.s - a.s).slice(0, 8);
    results.replaceChildren(...hits.map(({ p }) => {
      const li = document.createElement("li"), a = document.createElement("a"), small = document.createElement("small");
      const at = p.x.toLowerCase().indexOf(words[0]);
      a.href = "#" + p.id; a.textContent = p.t;
      small.textContent = at > -1 ? "…" + p.x.slice(Math.max(0, at - 40), at + 80) + "…" : "";
      a.append(small); li.append(a); return li;
    }));
    results.hidden = !hits.length;
    status.textContent = hits.length ? hits.length + " pages found" : "No pages found";
  });
  results.addEventListener("click", () => { results.hidden = true; q.value = ""; status.textContent = ""; });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !results.hidden) { results.hidden = true; q.focus(); } });
})();
</script>
`;
writeFileSync(OUT, html);
console.log(`[preview-gitbook] wrote ${pages.length} pages to ${OUT} (${Math.round(html.length / 1024)} KB)`);

// ---------------------------------------------------------------- axe, page by page
if (AXE) {
  const { chromium } = require("playwright");
  const axeSrc = readFileSync(join(ROOT, "site", "node_modules", "axe-core", "axe.min.js"), "utf8");
  const browser = await chromium.launch();
  const results = [];
  for (const scheme of ["light", "dark"]) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: scheme, bypassCSP: true });
    const page = await ctx.newPage();
    await page.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.abort());
    await page.goto(`file://${OUT}`);
    await page.addScriptTag({ content: axeSrc });
    for (const p of pages) {
      await page.evaluate((id) => { location.hash = id; }, p.id);
      await page.waitForFunction((id) => !document.getElementById("pg-" + id).hidden, p.id);
      const r = await page.evaluate(async () => { const out = await window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"] } }); return out.violations.map((v) => ({ id: v.id, impact: v.impact, n: v.nodes.length, sample: v.nodes[0]?.target?.join(" ") })); });
      for (const v of r) results.push({ scheme, page: p.path, ...v });
    }
    const sw = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    if (sw > 1) results.push({ scheme, page: "(layout)", id: "horizontal-scroll", n: sw });
    await ctx.close();
  }
  // phone width: no sideways scroll on any page
  const ctx = await browser.newContext({ viewport: { width: 375, height: 800 } });
  const page = await ctx.newPage();
  await page.route(/fonts\.(googleapis|gstatic)\.com/, (r) => r.abort());
  await page.goto(`file://${OUT}`);
  for (const p of pages) {
    await page.evaluate((id) => { location.hash = id; }, p.id);
    const sw = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    if (sw > 1) results.push({ scheme: "phone", page: p.path, id: "horizontal-scroll", n: sw });
  }
  await browser.close();
  console.log(`[preview-gitbook --axe] ${pages.length} pages × light and dark: ${results.length} finding(s)`);
  for (const r of results.slice(0, 30)) console.log("  ", JSON.stringify(r));
  writeFileSync(join(UI, "docs", "qa", "gitbook-preview-axe.json"), `${JSON.stringify({ pages: pages.length, schemes: ["light", "dark", "phone 375"], axe: "4.14.0", findings: results }, null, 1)}\n`);
  process.exit(results.length ? 1 : 0);
}
