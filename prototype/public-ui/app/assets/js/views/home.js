// Home page (#/). Owner: developer A. Spec: docs/DESIGN_SPEC.md §2.1. Licence: Apache-2.0.
// Gets people to the right role quickly and states the release status honestly, once.
import { h, icon } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { state } from "../lib/state.js";
import { COPY } from "../content.js";
import { figure, fmt, dateLong } from "../ui.js";
import { ACTOR_ORDER, listedRoles, rolesByActor } from "./roles.js";

const EXAMPLES = ["forestry technician", "Rx burn", "0460"];

const TASKS = [
  ["#/roles", "Look up what a role involves", "Tasks, competencies and how the work differs by employer."],
  ["#/compare", "Compare two roles", "What two roles share, and what to check with an employer."],
  ["#/competencies", "Find competencies and levels for a course or training plan", "Skill areas described at up to five levels."],
  ["#/changing", "See what's changing", "Early signals about how the work may change, all still on watch."],
  ["#/about/data", "Download or cite the data", "How to get the data, cite it and keep its caveats."],
];

/** The weakest of several figure badges: lowest use tier, weakest evidence label. */
function weakest(...figs) {
  const tiers = ["exploratory", "describe", "develop", "select"], ev = ["S", "J", "E"];
  const fs = figs.filter(Boolean);
  if (!fs.length) return null;
  const t = fs.map((f) => f.tier?.t).sort((a, b) => tiers.indexOf(a) - tiers.indexOf(b))[0];
  const l = fs.map((f) => f.ev?.l).sort((a, b) => ev.indexOf(a) - ev.indexOf(b))[0];
  return { tier: { t }, ev: { l } };
}

export async function render() {
  const core = await data.core();
  const go = h("a", { href: "#/search", class: "vh", tabindex: "-1", "aria-hidden": "true" }, "Search results");
  const search = (q) => {
    q = String(q || "").trim();
    if (!q) return false;
    state.query = q;
    const header = document.getElementById("q");
    if (header) header.value = q;
    go.click();
    return true;
  };

  // 1–3. Purpose, lede and a large search with example chips
  const input = h("input", { class: "search__input", id: "home-q", type: "search", autocomplete: "off", spellcheck: "false", placeholder: "Try: forestry technician" });
  const form = h("form", { class: "search search--page hero-search", role: "search", "aria-label": "Search EMST from the home page", novalidate: true },
    h("label", { class: "search__label home-search__label", for: "home-q" }, "Search for a job title, task, skill or code"),
    h("div", { class: "search__row" }, h("div", { class: "combobox" }, input),
      h("button", { class: "search__btn", type: "submit" }, icon("search"), h("span", "Search"))));
  form.addEventListener("submit", (e) => { e.preventDefault(); if (!search(input.value)) input.focus(); });
  const chips = h("div", { class: "home-examples" }, h("p", { class: "meta", id: "home-ex" }, "Or try an example:"),
    h("ul", { class: "example-chips", "aria-labelledby": "home-ex" }, EXAMPLES.map((ex) =>
      h("li", h("button", { class: "chip-btn", type: "button", on: { click: () => search(ex) } }, icon("search"), ex)))));

  const head = h("div", { class: "page-head home-head" },
    h("h1", { class: "display", tabindex: "-1" }, COPY.site.tagline),
    h("p", { class: "lede" }, COPY.site.lede),
    form, chips, go);

  // 4. Top tasks, verbs first
  const tasks = sec("home-tasks", "What do you want to do?",
    h("ul", { class: "task-links" }, TASKS.map(([href, label, hint]) => h("li",
      h("a", { class: "task-link", href }, h("span", { class: "task-link__text" }, h("span", { class: "task-link__label" }, label), h("span", { class: "task-link__hint" }, hint)), icon("arrow-right"))))));

  // 5. Browse by job family (filter passed to the roles page in memory, never in the URL)
  const listed = new Set(listedRoles(core).map((r) => r.slug));
  const fams = core.jobFamilies.map((f) => ({ ...f, n: (f.roles || []).filter((r) => listed.has(r.slug)).length }))
    .sort((a, b) => (b.n > 0) - (a.n > 0) || a.title.localeCompare(b.title));
  const famCards = h("ul", { class: "card-list card-list--compact" }, fams.map((f) => h("li", f.n
    ? h("article", { class: "card card--compact" },
      h("h3", { class: "card__title h4" }, h("a", { class: "card__link", href: "#/roles", on: { click: () => { state.roleFilters = { families: new Set([f.slug]) }; } } }, f.title)),
      h("p", { class: "card__count meta" }, `${fmt(f.n)} ${f.n === 1 ? "role" : "roles"}`))
    : h("article", { class: "card card--compact card--none" },
      h("h3", { class: "card__title h4" }, f.title),
      h("p", { class: "card__count meta" }, "No role profiles in this release yet")))));
  const families = sec("home-families", "Browse by job family", [
    h("p", { class: "meta" }, "Job families group roles that do similar work. A role can be in more than one family."), famCards]);

  // 6. Browse by employer type
  const byActor = rolesByActor(core);
  const actors = ACTOR_ORDER.map((code) => core.sectorActors.find((a) => a.code === code)).filter(Boolean);
  const employers = sec("home-employers", "Browse by employer type", [
    h("p", { class: "meta" }, "Each role says how the work differs for each kind of employer that has it."),
    h("ul", { class: "card-list card-list--compact" }, actors.map((a) => {
      const n = byActor[a.code] || 0;
      return h("li", h("article", { class: "card card--compact" },
        h("h3", { class: "card__title h4" }, h("a", { class: "card__link", href: "#/roles", on: { click: () => { state.roleFilters = { actors: new Set([a.code]) }; } } }, a.label)),
        h("p", { class: "card__count meta" }, `${fmt(n)} ${n === 1 ? "role" : "roles"} described for this employer type`)));
    }))]);

  // 7. What you can use EMST for (three lines and a link to the key)
  const use = sec("home-use", "What you can use EMST for", [
    h("dl", { class: "use-lines" },
      h("div", h("dt", icon("check"), "Use it for"), h("dd", "Describing work, planning a workforce, and mapping courses or training to the tasks a role does.")),
      h("div", h("dt", icon("scales"), "Don't use it for"), h("dd", "Decisions about people: hiring, setting grade or pay, rating performance, or choosing who to lay off.")),
      h("div", h("dt", icon("draft"), "How it was made"), h("dd", COPY.ai.line, " ", h("a", { href: "#/about/made" }, "How EMST was made")))),
    h("p", h("a", { class: "arrow-link", href: "#/about/read@use-tiers" }, "How to read EMST: what every label means", icon("arrow-right")))]);

  // 8. Release facts: figures with their badges, release ID and date, publication status, not a government site
  const r = core.release;
  const gate = core.status?.gate || {};
  const notCleared = (gate.items || []).some((i) => i.result === "fail");
  const facts = sec("home-release", "About this release", [
    h("ul", { class: "cluster figs" },
      figure(core.roles.length, "roles", core.figs.roles),
      figure(core.comps.length, "competencies", weakest(core.figs.coreCompetencies, core.figs.moduleCompetencies)),
      figure(core.stats.tasks, "tasks", core.figs.tasks)),
    h("p", { class: "meta" }, "Each number shows what the records it counts may be used for, and the weakest evidence among them. ",
      h("a", { href: "#/about/read@evidence" }, "What these labels mean")),
    h("p", "Draft release ", h("span", { class: "id" }, r.id), `, ${dateLong(r.date)}.`),
    notCleared ? h("p", { class: "home-quiet" }, `Release ${r.id} is a draft for the project team and pilot preview. It is not yet cleared for wider publication. `,
      h("a", { href: "#/about/status" }, "Release status")) : null,
    h("p", h("strong", COPY.site.notGov))]);

  return { title: null, node: h("div", { class: "home" }, head, h("div", { class: "page-body home-body" }, tasks, families, employers, use, facts)) };
}

function sec(id, title, children) {
  return h("section", { class: "section", id, "aria-labelledby": `h-${id}` },
    h("div", { class: "section__head" }, h("h2", { id: `h-${id}` }, title)), children);
}
