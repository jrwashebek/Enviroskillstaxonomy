// Competencies index (#/competencies, #/competencies/:module). Owner: developer A. Spec: docs/DESIGN_SPEC.md §1, §7 (IA).
// Filters (module, type, level, used in a role, words in the title) live in module memory, never in the URL.
import { h } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { state } from "../lib/state.js";
import { pageHeader, chipGroup, liveCount, badgeTier, badgeDraft, badgeLifecycle, shortId, fmt, notice } from "../ui.js";
import { normalize } from "../lib/search.js";
import { truncate } from "../lib/format.js";
import { filterPanel, activeChips, noMatches } from "./roles.js";

const LEVELS = ["L1", "L2", "L3", "L4", "L5"];
const PAGE = 40;
// "A" (Awareness) is a knowledge bundle below L1, not a level (vocab/proficiency_levels.yaml). It is not in core.labels.level.
const lvlIndex = (code) => (code === "A" ? -1 : LEVELS.indexOf(code));
const covers = (c, lvl) => lvlIndex(c.span[0]) <= LEVELS.indexOf(lvl) && LEVELS.indexOf(lvl) <= lvlIndex(c.span[1]);
const lvlText = (code) => (code === "A" ? "Awareness" : code);

let F = { modules: new Set(), types: new Set(), level: "any", used: false, words: "" };
let limit = PAGE;

/** Level span: five cells (L1 to L5) with the covered ones filled, plus words. */
export function spanNode(span) {
  const lo = Math.max(0, lvlIndex(span[0])), hi = lvlIndex(span[1]);
  return h("span", { class: "span" },
    h("span", { class: "span__cells", "aria-hidden": "true" }, LEVELS.map((_, i) => h("i", { class: i >= lo && i <= hi ? "on" : null }))),
    `${lvlText(span[0])} to ${lvlText(span[1])}`);
}

function compCard(c, core) {
  const mod = c.module && c.module !== "core" ? core.labels.module?.[c.module] : null;
  return h("article", { class: "card card--comp" },
    h("p", { class: "card__kind" }, h("span", c.typeLabel || core.labels.competencyType?.[c.type] || "Competency"), h("span", { class: "id" }, shortId(c.id))),
    h("h3", { class: "card__title h4" }, h("a", { class: "card__link", href: `#/competency/${c.slug}` }, c.title)),
    mod ? h("p", { class: "card__alt meta" }, `Module: ${mod}`) : null,
    c.stmt ? h("p", { class: "card__summary" }, truncate(c.stmt, 150)) : null,
    h("dl", { class: "card__meta" },
      h("div", h("dt", "Levels"), h("dd", spanNode(c.span))),
      h("div", h("dt", "Tasks"), h("dd", fmt(c.nTasks || 0))),
      h("div", h("dt", "Used in roles"), h("dd", fmt(c.nRoles || 0)))),
    h("div", { class: "card__badges cluster" }, badgeTier(c.tier?.t || "exploratory", { compact: true }), badgeDraft({ compact: true, v1: !!c.ev?.v1 }),
      c.lc && c.lc !== "established" ? badgeLifecycle(c.lc, { compact: true }) : null));
}

export async function render({ params = {} } = {}) {
  const core = await data.core();
  const modules = core.modules.slice().sort((a, b) => (b.core ? 1 : 0) - (a.core ? 1 : 0) || a.label.localeCompare(b.label));
  const known = new Set(modules.map((m) => m.ns));
  let unknownModule = null;
  if (state.compFilters) {
    const cf = state.compFilters;
    F = { modules: new Set(cf.modules || []), types: new Set(cf.types || []), level: cf.level || "any", used: !!cf.used, words: cf.words || "" };
    state.compFilters = null;
  }
  if (params.module) {
    if (known.has(params.module)) F.modules = new Set([params.module]);
    else unknownModule = params.module;
  }
  limit = PAGE;

  const comps = core.comps.slice().sort((a, b) => a.title.localeCompare(b.title));
  const typeCodes = Object.keys(core.labels.competencyType || {}).filter((t) => comps.some((c) => c.type === t));
  const opts = {
    modules: modules.map((m) => ({ value: m.ns, label: m.core ? "Core (all kinds of work)" : m.label })),
    types: typeCodes.map((t) => ({ value: t, label: core.labels.competencyType[t] })),
    level: [{ value: "any", label: "Any level" }, ...LEVELS.map((l) => ({ value: l, label: `${l} ${core.labels.level?.[l] || ""}`.trim() }))],
    used: [{ value: "yes", label: "Used in at least one role" }],
  };
  const qWords = () => normalize(F.words).split(/\s+/).filter(Boolean);
  const has = {
    modules: (c, v) => c.module === v,
    types: (c, v) => c.type === v,
    level: (c, v) => v === "any" || covers(c, v),
    used: (c) => (c.nRoles || 0) > 0,
  };
  const active = (k) => (k === "level" ? F.level !== "any" : k === "used" ? F.used : F[k].size > 0);
  const passWords = (c) => { const ws = qWords(); if (!ws.length) return true; const t = normalize(c.title); return ws.every((w) => t.includes(w)); };
  const pass = (c, skip) => passWords(c) && ["modules", "types", "level", "used"].every((k) => k === skip || !active(k) ||
    (k === "level" ? has.level(c, F.level) : k === "used" ? has.used(c) : [...F[k]].some((v) => has[k](c, v))));
  const countsFor = (k) => Object.fromEntries(opts[k].map((o) => [o.value, comps.filter((c) => pass(c, k) && (k === "used" ? has.used(c) : has[k](c, o.value))).length]));

  const groups = {
    modules: chipGroup({ legend: "Module", name: "comp-mod", options: opts.modules.map((o) => ({ ...o, count: 0 })), checked: [...F.modules], onChange: (v) => { F.modules = v; changed(); } }),
    types: chipGroup({ legend: "Type", name: "comp-type", options: opts.types.map((o) => ({ ...o, count: 0 })), checked: [...F.types], onChange: (v) => { F.types = v; changed(); } }),
    level: chipGroup({ legend: "Described at level", name: "comp-level", multi: false, options: opts.level.map((o) => ({ ...o, count: 0 })), checked: [F.level], onChange: (v) => { F.level = [...v][0] || "any"; changed(); } }),
    used: chipGroup({ legend: "Roles", name: "comp-used", options: opts.used.map((o) => ({ ...o, count: 0 })), checked: F.used ? ["yes"] : [], onChange: (v) => { F.used = v.has("yes"); changed(); } }),
  };
  groups.modules.node.appendChild(h("p", { class: "meta facet__help" }, "Core competencies apply across environmental work. Modules add competencies for one kind of work."));
  groups.level.node.appendChild(h("p", { class: "meta facet__help" }, "Shows competencies described at that level. Levels run from L1 (works under direction) to L5 (sets strategy)."));
  const filterTitle = h("span");
  const panel = filterPanel(filterTitle, [groups.modules.node, groups.types.node, groups.level.node, groups.used.node]);

  const words = h("input", { class: "text-input", id: "comp-words", type: "search", autocomplete: "off", spellcheck: "false", value: F.words, "aria-describedby": "comp-words-help" });
  let wt;
  words.addEventListener("input", () => { clearTimeout(wt); wt = setTimeout(() => { F.words = words.value; changed(); }, 150); });
  const wordBox = h("div", { class: "word-filter" }, h("label", { for: "comp-words" }, "Filter by words in the title"),
    h("p", { class: "meta", id: "comp-words-help" }, "The list updates as you type."), words);

  const count = liveCount();
  count.node.setAttribute("tabindex", "-1");
  const chipsSlot = h("div");
  const list = h("ul", { class: "card-list" });
  const moreRow = h("div", { class: "more-row" });
  const results = h("div", { class: "stack" });

  function clearAll() {
    F = { modules: new Set(), types: new Set(), level: "any", used: false, words: "" };
    groups.modules.set(new Set()); groups.types.set(new Set()); groups.level.set(new Set(["any"])); groups.used.set(new Set());
    words.value = "";
    changed();
  }
  function changed() { limit = PAGE; update(); }
  function update() {
    for (const k of Object.keys(groups)) groups[k].counts(countsFor(k));
    const n = F.modules.size + F.types.size + (F.level !== "any" ? 1 : 0) + (F.used ? 1 : 0);
    filterTitle.textContent = n ? `Filter competencies (${fmt(n)} selected)` : "Filter competencies";
    const chips = [];
    const modLabel = Object.fromEntries(opts.modules.map((o) => [o.value, o.label]));
    for (const v of F.modules) chips.push({ label: `Module: ${modLabel[v]}`, remove: () => { F.modules.delete(v); groups.modules.set(F.modules); changed(); } });
    for (const v of F.types) chips.push({ label: core.labels.competencyType[v], remove: () => { F.types.delete(v); groups.types.set(F.types); changed(); } });
    if (F.level !== "any") chips.push({ label: `Level ${F.level}`, remove: () => { F.level = "any"; groups.level.set(new Set(["any"])); changed(); } });
    if (F.used) chips.push({ label: "Used in a role", remove: () => { F.used = false; groups.used.set(new Set()); changed(); } });
    chipsSlot.replaceChildren(activeChips(chips, { onClear: clearAll, focusFallback: () => count.node }));
    draw();
  }
  function draw(focusFrom = -1) {
    const shown = comps.filter((c) => pass(c));
    count.set(`${fmt(shown.length)} of ${fmt(comps.length)} competencies match`);
    if (!shown.length) {
      results.replaceChildren(noMatches("No competencies match these filters", "Remove a filter, or use fewer words.", () => { clearAll(); count.node.focus(); }));
      return;
    }
    const page = shown.slice(0, limit);
    list.replaceChildren(...page.map((c) => h("li", compCard(c, core))));
    const rest = shown.length - page.length;
    moreRow.replaceChildren(h("p", { class: "meta" }, `Showing ${fmt(page.length)} of ${fmt(shown.length)}`),
      rest > 0 ? h("button", { class: "btn btn--secondary", type: "button", on: { click: () => { const from = limit; limit += PAGE; draw(from); } } },
        `Show ${fmt(Math.min(PAGE, rest))} more`) : null);
    if (results.firstChild !== list) results.replaceChildren(list, moreRow);
    if (focusFrom >= 0) list.children[focusFrom]?.querySelector("a")?.focus();
  }

  update();
  count.node.textContent = `${fmt(comps.filter((c) => pass(c)).length)} of ${fmt(comps.length)} competencies match`;

  const node = h("div",
    pageHeader({ crumbs: [{ href: "#/", text: "Home" }, { text: "Competencies" }], title: "Competencies",
      lede: "A competency is an area of skill that a role needs. Each one is described at up to five levels. Use the filters to find competencies for a course or a training plan." }),
    h("div", { class: "page-body stack filter-page" },
      unknownModule ? notice("info", null, "This release has no module with that name, so all modules are shown.") : null,
      h("p", { class: "meta" }, "AI agents drafted these competencies and their levels. No person has reviewed them yet. ",
        h("a", { href: "#/about/read@ai-drafted" }, "What this means")),
      h("div", { class: "filter-box" }, panel, wordBox),
      h("div", { class: "result-bar" }, count.node, chipsSlot),
      h("h2", { class: "vh" }, "Matching competencies"),
      results));
  return { title: "Competencies", node };
}
