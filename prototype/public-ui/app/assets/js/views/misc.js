// Tool and credential pages (#/tool/:slug, #/credential/:slug), plus small helpers shared by developer C's views
// (competency, task, compare, changing, hr). Developer C. Licence: Apache-2.0.
import { h, frag, icon } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { NotFound } from "../lib/data.js";
import { focusSection } from "../lib/router.js";
import * as ui from "../ui.js";
import { COPY } from "../content.js";
import { fmt, dateLong } from "../lib/format.js";

// ------------------------------------------------------------------ helpers for developer C's views

/** Plain words for internal terms that sometimes appear inside data text (brief: no visible internal jargon). */
export function plain(s) {
  return String(s ?? "")
    .replace(/\bLLM-vs-LLM\b/g, "AI coder against AI coder")
    .replace(/\bLLM-(assisted|extracted|coded|drafted)\b/gi, "AI-$1")
    .replace(/\bLLMs\b/g, "AI language models")
    .replace(/\bLLM\b/gi, "AI language model")
    .replace(/\bskos:|\bsemapv:/g, "")
    .replace(/\bcloseMatch\b/g, "close fit").replace(/\brelatedMatch\b/g, "partial fit")
    .replace(/\bbroadMatch\b/g, "broader match").replace(/\bnarrowMatch\b/g, "narrower match").replace(/\bexactMatch\b/g, "exact fit");
}

/** plain() plus removal of internal working codes that still sit inside some free-text fields ("SL-053",
 *  "DC-CAND-01/-13", "per V2-17", "mvp_role_set example", "(DC Phase 2 extract)"). Display only; data is untouched. */
export function scrub(s) {
  return plain(s)
    .replace(/\s*\(DC Phase \d+ extract\)/g, "")
    .replace(/\bper\s+V\d+-\d+\b/g, "")
    .replace(/\b(?:SL|FH|LM|DC|FS|CM|CP|PS|IO|LC|IA|SC|WP|WP09|ADR|REG|DISC|TR|V\d)-(?:CAND-)?\d[\w/-]*(?:\s*§\s*[A-Z0-9]+)?/g, "")
    .replace(/\bmvp_role_set(?: example)?\b/g, "")
    .replace(/\(\s*[;,]\s*/g, "(").replace(/\s*[;,]\s*\)/g, ")").replace(/\(\s*\)/g, "")
    .replace(/\s{2,}/g, " ").replace(/\s+([.,;)])/g, "$1").trim();
}

/** Export buttons with a status line, for a toolbar near the content they export (not only at the foot of the page).
 *  items: [{label, icon: "copy"|"download", run: async () => "copied"|"saved"|"failed"|boolean}]. Where the host blocks
 *  downloads, export.download() copies instead, and the label says so. */
export function exportBar(items, { label = "Export" } = {}) {
  const status = h("p", { class: "meta c-export__status", role: "status", "aria-live": "polite" });
  const restricted = document.documentElement.classList.contains("host-artifact");
  const btns = items.map((x) => {
    const dl = (x.icon || "download") === "download";
    const text = restricted && dl ? String(x.label).replace(/^Download\s+/i, "Copy ") + " to the clipboard" : x.label;
    return h("button", { class: "btn btn--secondary btn--small", type: "button", on: { click: async () => {
      const r = await x.run();
      status.textContent = r === "failed" || r === false ? (COPY.actions?.copyFailed || "Could not copy. Select the text and copy it yourself.")
        : r === "copied" || r === true ? `${COPY.actions?.copied || "Copied"}. ${x.done || "Paste it where you need it."}` : x.saved || "File saved to your downloads.";
      setTimeout(() => { status.textContent = ""; }, 5000);
    } } }, icon(restricted && dl ? "copy" : (x.icon || "download")), text);
  });
  return h("div", { class: "c-export no-print", role: "group", "aria-label": label }, h("div", { class: "btn-row" }, btns), status);
}

export const ROLE_LEVELS = ["entry", "journey", "senior", "lead", "strategic"];
const ROLE_LEVEL_LABEL = { entry: "Entry", journey: "Journey", senior: "Senior", lead: "Lead", strategic: "Strategic" };
export const roleLevelLabel = (k) => ROLE_LEVEL_LABEL[k] || cap(String(k || "").replace(/-/g, " "));
export const LEVEL_ORDER = ["A", "L1", "L2", "L3", "L4", "L5"];
export const levelRank = (code) => LEVEL_ORDER.indexOf(code);
export const cap = (s) => (s ? s[0].toUpperCase() + s.slice(1) : "");
/** "court-decision" → "Court decision" */
export const humanize = (code) => cap(String(code || "").replace(/[-_]+/g, " ").trim());

/** A level chip that also understands "A" (Awareness: a knowledge bundle, not a level). */
export function levelTag(code, core) {
  if (code === "A") return h("span", { class: "badge level-chip" }, h("span", { class: "level-chip__code" }, "A"), "Awareness");
  return ui.levelChip(code, core);
}

/** href for a role variant slug such as rol-ja00qmt--private-regulated-party (the part after "--" picks the variant). */
export function variantHref(vslug) {
  const [role, suffix] = String(vslug || "").split("--");
  return ui.link.role(role, suffix || null);
}
export const p3Slugs = (core) => new Set(core.roles.filter((r) => r.whatsComingOnly).map((r) => r.slug));
export const credSlug = (title) => "cred-" + String(title || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
export const plural = (n, one, many = one + "s") => `${fmt(n)} ${n === 1 ? one : many}`;

/** In-page link that moves focus to a section without changing the address (brief: never change the hash). */
export function jump(id, ...children) {
  return h("a", { href: `#${id}`, on: { click: (e) => { if (document.getElementById(id)) { e.preventDefault(); focusSection(id); } } } }, ...children);
}

/** Show the first n items of a list, with a button that reveals the rest. Returns a fragment. */
export function moreList(list, n, { more, less }) {
  const items = [...list.children];
  if (items.length <= n) return list;
  if (!list.id) list.id = `more-${Math.random().toString(36).slice(2, 8)}`;
  let open = false;
  const btn = h("button", { class: "btn btn--tertiary btn--small", type: "button", "aria-expanded": "false", "aria-controls": list.id });
  const draw = () => {
    items.forEach((li, i) => { li.hidden = !open && i >= n; });
    btn.textContent = open ? less : more;
    btn.setAttribute("aria-expanded", String(open));
  };
  btn.addEventListener("click", () => { open = !open; draw(); });
  draw();
  return frag(list, h("p", { class: "c-more no-print" }, btn));
}

/** SVG element builder (h() builds HTML elements only). Attributes only; never style. */
export function svg(tag, attrs = {}, ...kids) {
  const el = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [k, v] of Object.entries(attrs)) if (v !== null && v !== undefined && v !== false) el.setAttribute(k, String(v));
  for (const k of kids.flat()) if (k) el.appendChild(k);
  return el;
}

/** The HR disclaimer as a notice, with acronyms such as RIF spelled out on first use. */
export function hrNotice(paras) {
  const seen = new Set();
  return ui.notice("hr", "Not for decisions about people", [].concat(paras || []).map((t) => h("p", ui.jargon(t, seen))));
}

/** A small "AI-drafted, not reviewed" line for lists that have no record of their own (tools, credentials, links). */
export const draftNote = (text) => h("p", { class: "c-draftline meta" }, icon("draft"), text);

const TIMING = { "at-hire": "at hire", "alternative to the experience requirement": "as an alternative to the experience asked for" };
export const timingWords = (t) => TIMING[t] || String(t || "").replace(/-/g, " ");

// ------------------------------------------------------------------ shared bits for tool and credential pages

function roleLabelMap(core) {
  const m = new Map();
  for (const r of core.roles) for (const v of r.variants || []) m.set(v.slug, { role: r, v });
  return m;
}
async function taskTitles(slugs) {
  if (!slugs?.length) return new Map();
  const t = await data.searchTasks();
  const want = new Set(slugs);
  return new Map(t.docs.filter((d) => want.has(d.s)).map((d) => [d.s, d.t]));
}
function linkList(items, cls = "task-list") {
  return h("ul", { class: cls }, items.map((it) => h("li", h("a", { href: it.href }, it.text), it.meta ? h("p", { class: "task-list__meta" }, it.meta) : null)));
}
function whereSection(id, title, n, body) {
  return ui.section(id, title, body, { meta: plural(n, "link") });
}

// ------------------------------------------------------------------ tool page
export async function renderTool({ params }) {
  const [core, s] = await Promise.all([data.core(), data.search()]);
  const t = s.tools?.[params.slug];
  if (!t) throw new NotFound(`No tool "${params.slug}"`);
  const titles = await taskTitles(t.tasks);
  const comps = (t.comps || []).map((slug) => core.comps.find((c) => c.slug === slug)).filter(Boolean);
  const vmap = roleLabelMap(core);
  const p3 = p3Slugs(core);
  const variants = (t.variants || []).filter((v) => !p3.has(v.split("--")[0])).map((v) => vmap.get(v)).filter(Boolean);

  const sections = [];
  if (comps.length) sections.push(whereSection("comps", "Competencies that use it", comps.length, linkList(comps.map((c) => ({ href: ui.link.comp(c.slug), text: c.title })))));
  if (t.tasks?.length) sections.push(whereSection("tasks", "Tasks that use it", t.tasks.length,
    moreList(linkList(t.tasks.map((slug) => ({ href: ui.link.task(slug), text: titles.get(slug) || "Task" }))), 10, { more: `Show all ${fmt(t.tasks.length)} tasks`, less: "Show fewer tasks" })));
  if (variants.length) sections.push(whereSection("roles", "Roles that use it", variants.length,
    linkList(variants.map(({ role, v }) => ({ href: variantHref(v.slug), text: `${role.title} (${v.actorLabel})` })))));

  const node = frag(
    ui.printMeta(core, t.title),
    ui.pageHeader({
      crumbs: [{ href: "#/", text: "Home" }, { href: "#/competencies", text: "Competencies" }, { text: "Tool" }],
      kind: "Tool or technology", title: t.title,
      lede: "Tools change faster than the work. EMST lists them in a separate, dated layer and links them to the competencies and tasks that use them.",
      meta: h("p", { class: "cluster" }, t.cat ? h("span", { class: "meta" }, `Kind of tool: ${t.cat}`) : null, ui.badgeLifecycle(t.lc)),
    }),
    h("div", { class: "page-body stack-lg" },
      draftNote("AI agents drafted these links. No person has reviewed them yet. A tool listed here is an example, not a product EMST endorses."),
      sections.length ? sections : ui.emptyState({ title: "Not linked to any record yet", body: "AI agents have not linked this tool to a competency, task or role in this release.", iconName: "info" })));
  return { title: t.title, node };
}

// ------------------------------------------------------------------ credential page
export async function renderCredential({ params }) {
  const [core, s] = await Promise.all([data.core(), data.search()]);
  const c = s.credentials?.[params.slug];
  if (!c) throw new NotFound(`No credential "${params.slug}"`);
  const titles = await taskTitles(c.tasks);
  const vmap = roleLabelMap(core);
  const p3 = p3Slugs(core);
  const variants = (c.variants || []).filter((v) => !p3.has(v.split("--")[0])).map((v) => vmap.get(v)).filter(Boolean);
  const hasHr = variants.some(({ v }) => v.actor === "federal" || v.actor === "state");

  const sections = [];
  if (variants.length) sections.push(whereSection("roles", "Roles where it may be involved", variants.length,
    linkList(variants.map(({ role, v }) => ({ href: variantHref(v.slug), text: `${role.title} (${v.actorLabel})` })))));
  if (c.tasks?.length) sections.push(whereSection("tasks", "Tasks where it may be involved", c.tasks.length,
    moreList(linkList(c.tasks.map((slug) => ({ href: ui.link.task(slug), text: titles.get(slug) || "Task" }))), 10, { more: `Show all ${fmt(c.tasks.length)} tasks`, less: "Show fewer tasks" })));

  const node = frag(
    ui.printMeta(core, c.title),
    ui.pageHeader({
      crumbs: [{ href: "#/", text: "Home" }, { href: "#/roles", text: "Roles" }, { text: "Credential" }],
      kind: "Credential", title: c.title,
      lede: "This credential may be involved in some of the work below (AI-drafted link). EMST does not say it is required. Each employer decides what its jobs need.",
    }),
    h("div", { class: "page-body stack-lg" },
      hasHr ? hrNotice(core.text.hrDisclaimer) : null,
      draftNote("AI agents drafted these links and checked the issuer against a cited source. No person has reviewed them yet."),
      sections.length ? sections : ui.emptyState({ title: "Not linked to any record yet", body: "AI agents have not linked this credential to a task or role in this release.", iconName: "info" })));
  return { title: c.title, node };
}
