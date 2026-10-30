// Boot: site chrome (release strip, header with search, navigation, footer) and routes. Licence: Apache-2.0.
import { h, icon, clear, $ } from "./lib/dom.js";
import { route, start, configure, refresh } from "./lib/router.js";
import * as data from "./lib/data.js";
import { baseIndex, fullIndex, KIND_LABEL, KIND_ORDER, hrefFor } from "./lib/searchsvc.js";
import { segments } from "./lib/search.js";
import { state } from "./lib/state.js";
import { COPY } from "./content.js";
import { emptyState, REPO_URL, ISSUES_URL } from "./ui.js";
import { dateLong } from "./lib/format.js";

import * as home from "./views/home.js";
import * as searchView from "./views/search.js";
import * as roles from "./views/roles.js";
import * as competencies from "./views/competencies.js";
import * as about from "./views/about.js";
import * as role from "./views/role.js";
import * as competency from "./views/competency.js";
import * as task from "./views/task.js";
import * as compare from "./views/compare.js";
import * as changing from "./views/changing.js";
import * as hr from "./views/hr.js";
import * as misc from "./views/misc.js";

const NAV = [
  ["#/roles", "Roles", ["/roles", "/role/"]],
  ["#/competencies", "Competencies", ["/competencies", "/competency/", "/task/"]],
  ["#/compare", "Compare roles", ["/compare"]],
  ["#/changing", "What's changing", ["/changing"]],
  ["#/hr", "For HR and classifiers", ["/hr", "/series", "/class"]],
  ["#/about", "About the data", ["/about"]],
];

// ------------------------------------------------------------------ chrome
function releaseStrip(core) {
  const r = COPY.site?.ribbon || {};
  return h("div", { class: "release-strip" }, h("div", { class: "container release-strip__inner" }, icon("draft", null),
    h("p", h("strong", COPY.site?.independent || "Independent open project, not a government website."), " ", (r.release || "Draft release {id}").replace("{id}", core.release.id), ". ", r.ai || "Drafted by AI agents and not yet reviewed by people. Not for hiring, classification or performance decisions.", ". ",
      h("a", { href: "#/about/read" }, r.link || "What this means"))));
}

function header() {
  const input = h("input", { class: "search__input", id: "q", type: "search", role: "combobox", "aria-expanded": "false", "aria-controls": "q-list", "aria-autocomplete": "list", "aria-describedby": "q-help", autocomplete: "off", spellcheck: "false", placeholder: COPY.site?.searchPlaceholder || "Try: forestry technician, Rx burn, 0460" });
  const list = h("ul", { class: "listbox", id: "q-list", role: "listbox", "aria-label": "Search suggestions", hidden: true });
  const status = h("p", { class: "vh", role: "status", "aria-live": "polite", id: "q-status" });
  const form = h("form", { class: "search", role: "search", id: "site-search", novalidate: true },
    h("label", { class: "search__label", for: "q" }, COPY.site?.searchLabel || "Search job titles, tasks, competencies and codes"),
    h("div", { class: "search__row" }, h("div", { class: "combobox" }, input, list),
      h("button", { class: "search__btn", type: "submit" }, icon("search"), h("span", "Search"))),
    h("p", { class: "vh", id: "q-help" }, "Suggestions appear as you type. Use the up and down arrow keys to move through them and Enter to open one."),
    status);
  const allLink = h("a", { href: "#/search", class: "vh", tabindex: "-1", "aria-hidden": "true" }, "Search results");
  combobox({ input, list, status, form, allLink });
  return h("header", { class: "site-header" }, h("div", { class: "container site-header__bar" },
    h("a", { class: "brand", href: "#/" }, icon("emst-mark"), h("span", h("span", { class: "brand__name" }, "EMST"), h("span", { class: "brand__full" }, "Environmental Management Skills Taxonomy"))),
    form, allLink));
}

function nav() {
  const toggle = h("button", { class: "site-nav__toggle", type: "button", "aria-expanded": "false", "aria-controls": "nav-list" }, icon("menu"), "Menu");
  const list = h("ul", { class: "site-nav__list", id: "nav-list" }, NAV.map(([href, label]) => h("li", h("a", { class: "site-nav__link", href }, label))));
  toggle.addEventListener("click", () => { const open = list.classList.toggle("is-open"); toggle.setAttribute("aria-expanded", String(open)); });
  list.addEventListener("click", (e) => { if (e.target.closest("a")) { list.classList.remove("is-open"); toggle.setAttribute("aria-expanded", "false"); } });
  return h("nav", { class: "site-nav", "aria-label": "Main" }, h("div", { class: "container site-nav__inner" }, toggle, list));
}

function markNav(path) {
  for (const a of document.querySelectorAll(".site-nav__link")) {
    const item = NAV.find(([href]) => href === a.getAttribute("href"));
    const on = item && item[2].some((p) => path === p || path.startsWith(p));
    if (on) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
  }
}

function footer(core) {
  const f = COPY.site?.footer || {};
  return h("footer", { class: "site-footer" }, h("div", { class: "container site-footer__grid" },
    h("div", { class: "site-footer__about" },
      h("p", { class: "site-footer__brand" }, icon("emst-mark"), "EMST"),
      h("p", COPY.site?.notGov || "The Environmental Management Skills Taxonomy is an independent, open project. It is not a government website, and no agency has endorsed it."),
      h("p", `Release ${core.release.id}, ${dateLong(core.release.date)}. `, f.licence || "Data: CC0 1.0. Code: Apache-2.0. Credit: EMST project lead.", " ", h("span", { class: "id" }, `Build ${String(core.release.commit || "").slice(0, 7)}`)),
      f.authorship ? h("p", f.authorship) : null),
    h("nav", { "aria-labelledby": "ft-project" }, h("h2", { class: "site-footer__h", id: "ft-project" }, "Project"),
      h("ul", h("li", h("a", { href: "#/about/made" }, "How EMST was made")), h("li", h("a", { href: "#/about/status" }, "Release status")), h("li", h("a", { href: "#/about/data" }, "Data and downloads")),
        h("li", h("a", { href: REPO_URL, rel: "noopener" }, "Source on GitHub")), h("li", h("a", { href: ISSUES_URL, rel: "noopener" }, "Report a problem (GitHub)")))),
    h("nav", { "aria-labelledby": "ft-policy" }, h("h2", { class: "site-footer__h", id: "ft-policy" }, "Use and policy"),
      h("ul", h("li", h("a", { href: "#/about/read" }, "How to read EMST")), h("li", h("a", { href: "#/about/corrections" }, "Corrections")), h("li", h("a", { href: "#/about/held" }, "Held records")),
        h("li", h("a", { href: "#/about/accessibility" }, "Accessibility")), h("li", h("a", { href: "#/about/privacy" }, "Privacy"))))));
}

// ------------------------------------------------------------------ search combobox (ARIA 1.2 combobox with listbox popup)
function combobox({ input, list, status, form, allLink }) {
  let opts = [], active = -1, timer = null, announce = null, lastQ = "";
  const close = () => { list.hidden = true; input.setAttribute("aria-expanded", "false"); input.removeAttribute("aria-activedescendant"); active = -1; };
  const setActive = (i) => {
    opts.forEach((o, j) => o.setAttribute("aria-selected", j === i ? "true" : "false"));
    active = i;
    if (i >= 0) { input.setAttribute("aria-activedescendant", opts[i].id); opts[i].scrollIntoView({ block: "nearest" }); } else input.removeAttribute("aria-activedescendant");
  };
  const goAll = () => {
    state.query = input.value.trim(); close();
    allLink.setAttribute("href", "#/search");
    if (location.hash === "#/search") refresh(); else allLink.click();
  };
  const activate = (i) => {
    const o = opts[i];
    if (!o) return goAll();
    if (o.dataset.all) return goAll();
    state.query = input.value.trim();
    close();
    const href = o.querySelector("a")?.getAttribute("href");
    if (href) { allLink.setAttribute("href", href); allLink.click(); allLink.setAttribute("href", "#/search"); }
  };
  const mark = (text, q) => segments(text, q).map((s) => (s.mark ? h("mark", s.text) : s.text));
  async function suggest() {
    const q = input.value.trim();
    if (q === lastQ) return;
    lastQ = q;
    if (q.length < 2) { close(); clear(list); status.textContent = ""; return; }
    const ix = await baseIndex();
    const res = ix.search(q, { limit: 8 });
    clear(list); opts = [];
    if (res.held) res.results = [{ doc: { k: "policy", s: "held", t: "Held records", x: "The project's statement on records it does not publish", held: true } }];
    if (!res.results.length) {
      close();
      status.textContent = `No suggestions for "${q}". Press Enter to search tasks too.`;
      return;
    }
    const groups = new Map();
    for (const r of res.results) { if (!groups.has(r.doc.k)) groups.set(r.doc.k, []); groups.get(r.doc.k).push(r); }
    let n = 0;
    for (const k of KIND_ORDER) {
      const g = groups.get(k);
      if (!g) continue;
      const gid = `q-g-${k}`;
      const ul = h("ul", { role: "group", "aria-labelledby": gid }, h("li", { role: "none", class: "listbox__group-label", id: gid }, KIND_LABEL[k]));
      for (const r of g) {
        const li = h("li", { class: "listbox__option", id: `q-opt-${n++}`, role: "option", "aria-selected": "false" },
          h("a", { href: r.doc.held ? "#/about/held" : hrefFor(r.doc), tabindex: "-1", class: "listbox__title" }, mark(r.doc.t, q)),
          r.doc.x ? h("span", { class: "listbox__ctx" }, r.doc.x) : null);
        li.addEventListener("mousedown", (e) => e.preventDefault());
        li.addEventListener("click", (e) => { e.preventDefault(); activate(opts.indexOf(li)); });
        ul.appendChild(li); opts.push(li);
      }
      list.appendChild(h("li", { role: "none" }, ul));
    }
    const all = h("li", { class: "listbox__option listbox__all", id: "q-opt-all", role: "option", "aria-selected": "false", "data-all": "1" }, `See all results for "${q}"`);
    all.addEventListener("mousedown", (e) => e.preventDefault());
    all.addEventListener("click", () => goAll());
    list.appendChild(all); opts.push(all);
    list.hidden = false; input.setAttribute("aria-expanded", "true"); active = -1;
    clearTimeout(announce);
    announce = setTimeout(() => { status.textContent = `${opts.length - 1} suggestions. Press Enter for all results.`; }, 500);
  }
  input.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(suggest, 120); });
  input.addEventListener("focus", () => { baseIndex(); fullIndex(); }, { once: true });
  input.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") { e.preventDefault(); if (list.hidden) { lastQ = ""; suggest(); } else setActive(Math.min(active + 1, opts.length - 1)); }
    else if (e.key === "ArrowUp") { e.preventDefault(); if (!list.hidden) setActive(Math.max(active - 1, 0)); }
    else if (e.key === "Enter") { e.preventDefault(); if (!list.hidden && active >= 0) activate(active); else if (input.value.trim()) goAll(); }
    else if (e.key === "Escape") { if (!list.hidden) { e.preventDefault(); close(); } else if (input.value) { e.preventDefault(); input.value = ""; lastQ = ""; } }
    else if (e.key === "Tab") close();
  });
  input.addEventListener("blur", () => setTimeout(close, 150));
  form.addEventListener("submit", (e) => { e.preventDefault(); if (input.value.trim()) goAll(); });
}

// ------------------------------------------------------------------ routes
function notFound(_, path) {
  return {
    title: "Page not found",
    node: h("div", { class: "page-head" }, h("h1", { tabindex: "-1" }, "We could not find that page"),
      emptyState({ title: "It may have moved, or the address may be mistyped.", body: `Address: ${path}`, iconName: "search", actions: [h("a", { class: "btn btn--secondary", href: "#/" }, "Go to the home page"), h("a", { class: "btn btn--tertiary", href: "#/roles" }, "Browse roles")] })),
  };
}
function errorView(err) {
  return {
    title: "Something went wrong",
    node: h("div", { class: "page-head" }, h("h1", { tabindex: "-1" }, "This page did not load"),
      emptyState({ title: "Part of the data could not be loaded.", body: String(err && err.message || err), iconName: "alert", actions: [h("a", { class: "btn btn--secondary", href: "#/" }, "Go to the home page")] })),
  };
}

async function boot() {
  const core = await data.core();
  $("#site-top").replaceChildren(releaseStrip(core), header(), nav());
  $("#site-bottom").replaceChildren(footer(core));
  const r = (pattern, mod, fn = "render") => route(pattern, (ctx) => mod[fn](ctx));
  r("/", home); r("/search", searchView);
  r("/roles", roles); r("/role/:slug", role); r("/role/:slug/:actor", role);
  r("/competencies", competencies); r("/competencies/:module", competencies); r("/competency/:slug", competency);
  r("/task/:slug", task);
  r("/compare", compare); r("/compare/:a", compare); r("/compare/:a/:b", compare);
  r("/changing", changing);
  r("/hr", hr, "renderHub"); r("/series", hr, "renderSeriesIndex"); r("/series/:code", hr, "renderSeries"); r("/classes", hr, "renderClassIndex"); r("/class/:slug", hr, "renderClass");
  r("/tool/:slug", misc, "renderTool"); r("/credential/:slug", misc, "renderCredential");
  r("/about", about); r("/about/:page", about);
  configure({ notFound, error: errorView, afterRender: ({ path }) => markNav(path) });
  window.addEventListener("beforeprint", () => document.querySelectorAll("details:not([open])").forEach((d) => { d.dataset.printOpened = "1"; d.open = true; }));
  window.addEventListener("afterprint", () => document.querySelectorAll("details[data-print-opened]").forEach((d) => { d.open = false; delete d.dataset.printOpened; }));
  await start();
}

boot().catch((e) => {
  console.error(e);
  const main = $("#main");
  main.replaceChildren(h("div", { class: "container" }, errorView(e).node));
});
