// Roles index (#/roles). Owner: developer A. Spec: docs/DESIGN_SPEC.md §2.4. Licence: Apache-2.0.
// Filters (job family, employer type, depth) and grouping live in module memory, never in the URL.
// What's-coming-only (P3) roles are not listed here; they appear only in What's changing.
import { h, icon } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { state } from "../lib/state.js";
import { COPY } from "../content.js";
import { pageHeader, chipGroup, liveCount, badgeTier, badgeDraft, badgeLifecycle, shortId, fmt, disclosure } from "../ui.js";

export const ACTOR_ORDER = ["federal", "state", "local", "ngo", "private", "academic"];
export const ACTOR_SHORT = { federal: "Federal", state: "State", local: "Local", ngo: "Nonprofit", private: "Private", academic: "Academic" };
const DEPTH = { full: "Full profile", starter: "Starter profile" };
const depthKey = (r) => (r.depth === "P1" ? "full" : "starter");

/** Roles shown in role lists: every role except What's-coming-only (P3) roles. */
export const listedRoles = (core) => core.roles.filter((r) => !r.whatsComingOnly);
const actorsOf = (r) => new Set((r.variants || []).map((v) => v.actor));
/** Number of listed roles with a variant for each employer type. */
export function rolesByActor(core) {
  const out = {};
  for (const r of listedRoles(core)) for (const a of actorsOf(r)) out[a] = (out[a] || 0) + 1;
  return out;
}

// ------------------------------------------------------------------ shared filter helpers (also used by competencies.js)
/** Filters shown in a disclosure: open on wide screens, closed on phones so results stay near the top. */
export function filterPanel(title, facets) {
  const wide = typeof matchMedia === "function" && matchMedia("(min-width: 64rem)").matches;
  const d = disclosure(title, facets, { open: wide });
  d.classList.add("filters");
  return d;
}
/** Active filters as removable chips plus "Clear filters". items: [{label, remove()}]. */
export function activeChips(items, { onClear, focusFallback }) {
  const wrap = h("div", { class: "active-filters" });
  items.forEach((it, i) => {
    const b = h("button", { class: "chip-remove", type: "button" }, h("span", { class: "vh" }, "Remove filter: "), it.label, icon("close"));
    b.addEventListener("click", () => {
      it.remove();
      requestAnimationFrame(() => {
        const left = [...document.querySelectorAll(".active-filters .chip-remove")];
        (left[Math.min(i, left.length - 1)] || focusFallback?.())?.focus();
      });
    });
    wrap.appendChild(b);
  });
  if (items.length) wrap.appendChild(h("button", { class: "btn btn--tertiary btn--small", type: "button", on: { click: () => { onClear(); requestAnimationFrame(() => focusFallback?.()?.focus()); } } }, COPY.empty?.filters?.action || "Clear filters"));
  return wrap;
}
/** Empty state for filters that leave nothing. */
export function noMatches(title, body, onClear) {
  return h("div", { class: "empty" }, h("span", { class: "empty__icon", "aria-hidden": "true" }, icon("filter")),
    h("h2", { class: "empty__title h4" }, title), h("p", body),
    h("div", { class: "btn-row" }, h("button", { class: "btn btn--secondary", type: "button", on: { click: onClear } }, COPY.empty?.filters?.action || "Clear filters")));
}

// ------------------------------------------------------------------ view state (memory only)
let F = { families: new Set(), actors: new Set(), depth: new Set() };
let groupBy = "family";
const openGroups = new Map(); // family groups the person opened or closed, kept in memory

function roleCard(r, headingLevel = 3) {
  const actors = ACTOR_ORDER.filter((a) => actorsOf(r).has(a));
  return h("article", { class: "card" },
    h("p", { class: "card__kind" }, h("span", `Role · ${DEPTH[depthKey(r)]}`), h("span", { class: "id" }, shortId(r.id))),
    h(`h${headingLevel}`, { class: "card__title h4" }, h("a", { class: "card__link", href: `#/role/${r.slug}` }, r.title)),
    r.alt && r.alt.length ? h("p", { class: "card__alt meta" }, `${COPY.site?.alsoCalled || "Also called"}: ${r.alt.slice(0, 2).join("; ")}`) : null,
    r.fn ? h("p", { class: "card__summary" }, r.fn) : null,
    actors.length ? h("p", { class: "card__emp" }, h("span", { class: "card__emp-label" }, "Employers: "), actors.map((a) => ACTOR_SHORT[a]).join(" · ")) : null,
    h("dl", { class: "card__meta" }, h("div", h("dt", "Tasks"), h("dd", fmt(r.nTasks))), h("div", h("dt", "Competencies"), h("dd", fmt(r.nComps)))),
    h("div", { class: "card__badges cluster" }, badgeTier(r.tier?.t || "exploratory", { compact: true }), badgeDraft({ compact: true }),
      r.lc && r.lc !== "established" ? badgeLifecycle(r.lc, { compact: true }) : null));
}

export async function render({ section } = {}) {
  const core = await data.core();
  if (state.roleFilters) {
    const rf = state.roleFilters;
    F = { families: new Set(rf.families || []), actors: new Set(rf.actors || []), depth: new Set(rf.depth || []) };
    state.roleFilters = null;
  }
  const roles = listedRoles(core).slice().sort((a, b) => a.title.localeCompare(b.title));
  const p3 = core.roles.filter((r) => r.whatsComingOnly).length;
  const famOf = new Map(roles.map((r) => [r.slug, new Set()]));
  for (const f of core.jobFamilies) for (const m of f.roles || []) famOf.get(m.slug)?.add(f.slug);
  const families = core.jobFamilies.filter((f) => roles.some((r) => famOf.get(r.slug).has(f.slug))).sort((a, b) => a.title.localeCompare(b.title));
  const famTitle = Object.fromEntries(core.jobFamilies.map((f) => [f.slug, f.title]));
  // A link to one family's group (#/roles@<family>, used by the home page's cards when opened in a new tab): show
  // roles by family with that group open. The router then moves focus to it. No filter is set from the address.
  const famSection = section && families.some((f) => f.slug === section) ? section : null;
  if (famSection) { groupBy = "family"; openGroups.set(famSection, true); }

  const has = {
    families: (r, v) => famOf.get(r.slug).has(v),
    actors: (r, v) => actorsOf(r).has(v),
    depth: (r, v) => depthKey(r) === v,
  };
  const pass = (r, skip) => Object.keys(F).every((k) => k === skip || !F[k].size || [...F[k]].some((v) => has[k](r, v)));
  const countsFor = (k, values) => Object.fromEntries(values.map((v) => [v, roles.filter((r) => pass(r, k) && has[k](r, v)).length]));

  const opts = {
    families: families.map((f) => ({ value: f.slug, label: f.title })),
    actors: ACTOR_ORDER.map((a) => ({ value: a, label: ACTOR_SHORT[a] })),
    depth: ["full", "starter"].map((d) => ({ value: d, label: DEPTH[d] })),
  };
  const groups = {};
  const mk = (k, legend) => (groups[k] = chipGroup({ legend, name: `roles-${k}`, options: opts[k].map((o) => ({ ...o, count: 0 })), checked: [...F[k]], onChange: (vals) => { F[k] = vals; update(); } }));
  mk("families", "Job family");
  mk("actors", "Employer type");
  mk("depth", "Depth of profile");
  const depthHelp = h("p", { class: "meta facet__help" }, "Full profiles have the most detail. Starter profiles are shorter, earlier drafts.");
  groups.depth.node.appendChild(depthHelp);
  const filterTitle = h("span");
  const panel = filterPanel(filterTitle, [groups.families.node, groups.actors.node, groups.depth.node]);

  const count = liveCount();
  count.node.setAttribute("tabindex", "-1");
  const sort = chipGroup({ legend: "Show roles", name: "roles-group", multi: false, checked: [groupBy],
    options: [{ value: "family", label: "By job family" }, { value: "az", label: "A to Z" }], onChange: (v) => { groupBy = [...v][0] || "family"; draw(); } });
  sort.node.classList.add("facet--inline");
  const chipsSlot = h("div");
  const results = h("div", { class: "role-results" });

  function clearAll() { F = { families: new Set(), actors: new Set(), depth: new Set() }; for (const k of Object.keys(groups)) groups[k].set(new Set()); update(); }
  function update() {
    for (const k of Object.keys(groups)) groups[k].counts(countsFor(k, opts[k].map((o) => o.value)));
    const n = Object.values(F).reduce((s, v) => s + v.size, 0);
    filterTitle.textContent = n ? `Filter roles (${fmt(n)} selected)` : "Filter roles";
    const active = [];
    for (const k of Object.keys(F)) for (const v of F[k]) active.push({ label: k === "families" ? famTitle[v] : k === "actors" ? ACTOR_SHORT[v] : DEPTH[v], remove: () => { F[k].delete(v); groups[k].set(F[k]); update(); } });
    chipsSlot.replaceChildren(activeChips(active, { onClear: clearAll, focusFallback: () => count.node }));
    draw();
  }
  function draw() {
    const shown = roles.filter((r) => pass(r));
    count.set(`Showing ${fmt(shown.length)} of ${fmt(roles.length)} roles`);
    if (!shown.length) {
      results.replaceChildren(noMatches(COPY.empty.filters.title, `${COPY.empty.filters.body} Some roles are described for only a few employer types.`, () => { clearAll(); count.node.focus(); }));
      return;
    }
    if (groupBy === "az") {
      results.replaceChildren(h("h2", { class: "vh" }, "Roles A to Z"), h("ul", { class: "card-list" }, shown.map((r) => h("li", roleCard(r)))));
      return;
    }
    // Each family is a disclosure (a heading that holds a button), so phones get a short, scannable list of families.
    const fams = (F.families.size ? families.filter((f) => F.families.has(f.slug)) : families)
      .map((f) => ({ id: f.slug, title: f.title, rs: shown.filter((r) => famOf.get(r.slug).has(f.slug)) })).filter((g) => g.rs.length);
    const other = F.families.size ? [] : shown.filter((r) => !famOf.get(r.slug).size);
    if (other.length) fams.push({ id: "fam-none", title: "Not yet in a job family", rs: other });
    const wide = typeof matchMedia === "function" && matchMedia("(min-width: 64rem)").matches;
    const openByDefault = wide || fams.length === 1 || shown.length <= 6;
    results.replaceChildren(
      h("p", { class: "meta" }, "A role can be in more than one job family, so it may appear more than once."),
      ...fams.map((g) => group(g.id, g.title, g.rs, openGroups.has(g.id) ? openGroups.get(g.id) : openByDefault)));
  }
  function group(id, title, rs, open) {
    const panel = h("div", { class: "role-group__panel", id: `p-${id}`, hidden: !open }, h("ul", { class: "card-list" }, rs.map((r) => h("li", roleCard(r)))));
    const btn = h("button", { class: "group-toggle", type: "button", "aria-expanded": String(open), "aria-controls": `p-${id}` },
      icon("chevron-down"), h("span", { class: "group-toggle__title" }, title), h("span", { class: "group-toggle__count" }, `${fmt(rs.length)} ${rs.length === 1 ? "role" : "roles"}`));
    btn.addEventListener("click", () => {
      const o = btn.getAttribute("aria-expanded") !== "true";
      btn.setAttribute("aria-expanded", String(o));
      panel.hidden = !o;
      openGroups.set(id, o);
    });
    return h("section", { class: "role-group", id, "aria-labelledby": `h-${id}` }, h("h2", { class: "role-group__h h3", id: `h-${id}` }, btn), panel);
  }

  update();
  count.node.textContent = `Showing ${fmt(roles.filter((r) => pass(r)).length)} of ${fmt(roles.length)} roles`;

  const node = h("div",
    pageHeader({ crumbs: [{ href: "#/", text: "Home" }, { text: "Roles" }], title: "Roles",
      lede: "A role describes a kind of job: its tasks, the competencies it needs, and how it differs from one employer to another. Choose a role to see its work." }),
    h("div", { class: "page-body stack filter-page" },
      h("div", { class: "filter-box" }, panel),
      h("div", { class: "result-bar" }, count.node, chipsSlot),
      sort.node,
      results,
      h("p", { class: "p3-note" }, icon("eye"), h("span", `${fmt(p3)} emerging roles are not listed here, because the work is not yet shown to exist. `,
        h("a", { href: "#/changing" }, "See them in What's changing")))));
  return { title: "Roles", node };
}
