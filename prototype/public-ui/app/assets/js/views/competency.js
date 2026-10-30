// Competency page (#/competency/:slug). DESIGN_SPEC §2.6. Developer C. Licence: Apache-2.0.
import { h, frag } from "../lib/dom.js";
import * as data from "../lib/data.js";
import * as ui from "../ui.js";
import { COPY } from "../content.js";
import { fmt } from "../lib/format.js";
import { plain, ROLE_LEVELS, roleLevelLabel, levelRank, levelTag, humanize, jump, moreList, plural, draftNote } from "./misc.js";

const V1_RELATION = {
  "merged-from": "Merged into this competency",
  "split-from": "Split out of this earlier item",
  rewritten: "Rewritten from this earlier item",
  recovered: "Recovered from this earlier item",
  "reference-only": "Kept for reference only",
};

// Crosswalk sets, in display order. name(row) gives the shown name; ESCO objects have no label in the release.
const XW_SETS = [
  { rx: /^esco/, title: "ESCO skills (European Union)", noun: "skill",
    name: (r) => ({ text: r.lab || (r.obj ? `ESCO skill ${String(r.obj).replace(/^ESCO:/, "").slice(0, 8)}` : "ESCO") }) },
  { rx: /^opm-series/, title: "OPM job series", noun: "series", name: null },
  { rx: /^opm-ecq/, title: "OPM Executive Core Qualifications (senior executive leadership skills)", noun: "term",
    name: (r) => ({ text: r.lab || (r.obj ? `Executive Core Qualification item ${String(r.obj).replace(/^[A-Z]+:/, "")}` : "Executive Core Qualifications") }) },
  { rx: /^dol-ai/, title: "Department of Labor AI literacy framework", noun: "term",
    name: (r) => ({ text: r.lab || (r.obj ? `AI literacy framework item ${String(r.obj).replace(/^[A-Z]+:/, "")}` : "AI literacy framework") }) },
];
const xwRank = (r) => (r.not ? 4 : r.none ? 3 : r.close ? 0 : 1);

function seriesName(core) {
  return (r) => {
    if (!r.obj) return { text: "OPM job series" };
    const code = String(r.obj).replace(/^[A-Za-z]+:/, "");
    const rec = core.series.find((s) => s.code === code);
    const rel = r.o?.rel ? `, ${r.o.rel} competency in this series` : "";
    const realign = rec?.realignment ? `. ${core.text.realignment}` : "";
    return rec ? { href: ui.link.series(code), text: `${code} ${rec.title}${rel}${realign}` } : { text: `${code} ${r.lab || ""}${rel}`.trim() };
  };
}

function crosswalks(comp, core) {
  // Reference versions are shown once per system instead of on every row.
  const rows = (comp.crosswalks || []).map((r) => ({ ...r, note: r.note ? plain(r.note) : r.note, ver: undefined, _ver: r.ver }));
  if (!rows.length) return null;
  const parts = [];
  const used = new Set();
  for (const set of XW_SETS) {
    const mine = rows.filter((r) => set.rx.test(r.set || "")).sort((x, y) => xwRank(x) - xwRank(y));
    mine.forEach((r) => used.add(r));
    if (!mine.length) continue;
    const f = ui.crosswalkList(mine, { noun: set.noun, linkFn: set.name || seriesName(core) });
    const vers = [...new Set(mine.map((r) => r._ver).filter(Boolean))];
    parts.push(h("h3", { class: "h4" }, set.title), f.querySelector(".xw-list"),
      vers.length ? h("p", { class: "meta" }, `Reference version: ${vers.join("; ")}.`) : null);
  }
  const rest = rows.filter((r) => !used.has(r));
  if (rest.length) parts.push(h("h3", { class: "h4" }, "Other systems"), ui.crosswalkList(rest, { noun: "term" }).querySelector(".xw-list"));
  parts.push(h("p", { class: "meta" }, COPY.match.note));
  return parts;
}

function rolesUsing(comp, core) {
  const roles = comp.roles || [];
  if (!roles.length) return [h("p", "No role profile targets this competency yet.")];
  const list = h("ul", { class: "c-rolelist" }, roles.map((r) => h("li", { class: "c-rolelist__item" },
    h("h3", { class: "h4 c-rolelist__title" }, h("a", { href: ui.link.role(r.slug) }, r.title)),
    h("ul", { class: "c-bylevel", "aria-label": `Target levels for ${r.title}` },
      ROLE_LEVELS.filter((k) => r.levels?.[k]).map((k) => h("li", h("span", { class: "c-bylevel__k" }, `${roleLevelLabel(k)} `), ui.levelChip(r.levels[k], core)))))));
  return [
    h("p", "Each role profile sets a target level for this competency at each of its role levels."),
    moreList(list, 10, { more: `Show all ${fmt(roles.length)} roles`, less: "Show fewer roles" }),
    h("p", { class: "meta" }, core.text.targetsNote),
  ];
}

function taskList(comp) {
  const tasks = (comp.tasks || []).slice().sort((a, b) => (a.strength === "primary" ? 0 : 1) - (b.strength === "primary" ? 0 : 1));
  const primary = tasks.filter((t) => t.strength === "primary");
  const other = tasks.filter((t) => t.strength !== "primary");
  const out = [];
  const one = (t) => h("li", h("a", { href: ui.link.task(t.slug) }, t.stmt));
  if (primary.length) out.push(h("h3", { class: "h4" }, `Main competency for these tasks (${fmt(primary.length)})`),
    moreList(h("ul", { class: "task-list" }, primary.map(one)), 8, { more: `Show all ${fmt(primary.length)} tasks`, less: "Show fewer tasks" }));
  if (other.length) out.push(h("h3", { class: "h4" }, `Also used in these tasks (${fmt(other.length)})`),
    moreList(h("ul", { class: "task-list" }, other.map(one)), 8, { more: `Show all ${fmt(other.length)} tasks`, less: "Show fewer tasks" }));
  return out;
}

function knowledge(comp, core) {
  const ks = (comp.ks || []).slice().sort((a, b) => levelRank(a.low) - levelRank(b.low));
  const seen = new Set(["AI"]);
  return [
    h("p", "Each statement shows the lowest level at which people are expected to know it. “Awareness” means knowing the issue exists, when it applies and whom to involve. It is not a level of practice."),
    h("ul", { class: "task-list" }, ks.map((k) => h("li", { class: "c-ks" }, h("span", ui.jargon(k.stmt, seen)), h("span", { class: "c-ks__level" }, h("span", { class: "vh" }, "Lowest level: "), levelTag(k.low, core))))),
  ];
}

function enactments(comp, core) {
  const L = core.labels;
  const groups = new Map();
  for (const e of comp.enactments || []) {
    const key = e.authorityPosition ? (L.authorityPosition?.[e.authorityPosition] || humanize(e.authorityPosition))
      : e.ck ? (L.craft?.[e.ck] || humanize(e.ck)) : "Other settings";
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(e);
  }
  const seen = new Set(["AI"]);
  const out = [h("p", "The same competency can look different depending on who does it and under what authority. These notes are grouped by the position of the person doing the work, such as regulator or service provider. AI agents drafted them.")];
  for (const [key, list] of groups) {
    out.push(h("h3", { class: "h4" }, key));
    out.push(h("ul", { class: "c-enact" }, list.map((e) => {
      const who = [e.actorType ? `Employer: ${L.sectorActor?.[e.actorType] || humanize(e.actorType)}` : null,
        e.module && e.module !== "core" ? `Area: ${L.module?.[e.module] || humanize(e.module)}` : null,
        e.ck ? `Craft: ${L.craft?.[e.ck] || e.ck}` : null].filter(Boolean).join(" · ");
      return h("li", { class: "c-enact__item" },
        h("p", { class: "c-enact__title" }, plain(e.title)),
        who ? h("p", { class: "meta" }, who) : null,
        e.note ? h("p", ui.jargon(plain(e.note), seen)) : null,
        e.basis || e.principal ? h("dl", { class: "facts" },
          e.basis ? [h("dt", "Basis for the work"), h("dd", plain(e.basis))] : null,
          e.principal ? [h("dt", "Answers to"), h("dd", plain(e.principal))] : null) : null);
    })));
  }
  return out;
}

function tools(comp, core) {
  return [h("ul", { class: "task-list" }, comp.tools.map((t) => h("li", { class: "c-tool" },
    h("a", { href: `#/tool/${t.id}` }, t.title), t.lc && t.lc !== "established" ? [" ", ui.badgeLifecycle(t.lc, { compact: true })] : null))),
  draftNote("AI agents drafted these links. Tools change faster than the work, so they sit in a separate, dated layer.")];
}

function v1Lineage(comp) {
  const codes = comp.v1Codes || [];
  const from = comp.v1From || [];
  if (!codes.length && !from.length) return null;
  return ui.disclosure("Earlier version (v1)", [
    h("p", "EMST version 1 used different codes. These show where this competency came from, for tracing history only. They are not ratings."),
    codes.length ? h("dl", { class: "facts" }, h("dt", "v1 codes"), h("dd", h("span", { class: "id" }, codes.join(", ")))) : null,
    from.length ? h("ul", { class: "c-v1from" }, from.map((x) => h("li", h("span", { class: "id" }, String(x.key).replace(/^v1:/, "v1 item ")), ": ", V1_RELATION[x.relation] || humanize(x.relation)))) : null,
  ]);
}

function spanText(span, core) {
  if (!span) return null;
  const nm = (c) => (c === "A" ? "Awareness" : `${c} ${core.labels.level?.[c] || ""}`.trim());
  return `${nm(span[0])} to ${nm(span[1])}`;
}

export async function render({ params }) {
  const [core, comp] = await Promise.all([data.core(), data.comp(params.slug)]);
  const nRoles = (comp.roles || []).length, nTasks = (comp.tasks || []).length;
  const hasLevels = (comp.levels || []).length > 0;
  const seen = new Set(["AI"]);

  const meta = h("div", { class: "c-headmeta" },
    h("p", { class: "meta" }, [
      comp.moduleLabel ? `Area: ${comp.moduleLabel}${comp.isModule ? ` (${core.text.moduleTag})` : ""}` : null,
      comp.span ? `Levels: ${spanText(comp.span, core)}` : null,
    ].filter(Boolean).join(" · ")),
    nRoles || nTasks ? h("p", { class: "c-headmeta__jump" },
      nRoles ? jump("roles", `Used in ${plural(nRoles, "role")}`) : null, nRoles && nTasks ? " · " : null,
      nTasks ? jump("tasks", `Serves ${plural(nTasks, "task")}`) : null) : null);

  const sections = [
    { id: "levels", title: hasLevels ? "Levels" : "Knowledge area" },
    { id: "roles", title: "Used in roles" },
    nTasks ? { id: "tasks", title: "Tasks" } : null,
    comp.ks?.length ? { id: "knowledge", title: "Knowledge" } : null,
    comp.enactments?.length ? { id: "enactments", title: "How employers differ" } : null,
    comp.tools?.length ? { id: "tools", title: "Tools" } : null,
    comp.crosswalks?.length ? { id: "crosswalks", title: "Related elsewhere" } : null,
    { id: "about", title: "About this record" },
  ].filter(Boolean);
  const title = (id) => sections.find((s) => s.id === id)?.title;

  const levelsBody = hasLevels ? [
    ui.notice("draft", "Draft indicators, not assessment criteria", "AI agents drafted these indicators to show what each level can look like. They are for exploring and planning. They are not assessment criteria yet, so do not rate people against them."),
    ui.levelLadder(comp.levels, { span: comp.span?.[0] === "A" ? ["L1", comp.span[1]] : comp.span, core, titleId: "h-levels" }),
    h("p", { class: "meta" }, ui.jargon(core.text.indicatorPlacement, seen)),
  ] : [
    h("p", "This is a knowledge area. It is described by knowledge statements, each with the lowest level where it applies, not by levels of practice."),
    comp.ks?.length ? h("p", jump("knowledge", "Go to the knowledge statements")) : null,
  ];

  const main = [
    ui.section("levels", title("levels"), levelsBody),
    ui.section("roles", title("roles"), rolesUsing(comp, core), { meta: plural(nRoles, "role") }),
    nTasks ? ui.section("tasks", title("tasks"), taskList(comp), { meta: plural(nTasks, "task") }) : null,
    comp.ks?.length ? ui.section("knowledge", title("knowledge"), knowledge(comp, core), { meta: plural(comp.ks.length, "statement") }) : null,
    comp.enactments?.length ? ui.section("enactments", title("enactments"), enactments(comp, core)) : null,
    comp.tools?.length ? ui.section("tools", title("tools"), tools(comp, core)) : null,
    comp.crosswalks?.length ? ui.section("crosswalks", title("crosswalks"), crosswalks(comp, core)) : null,
    ui.section("about", title("about"), [ui.aboutRecord(comp, core, { title: comp.title, kind: "Competency" }), v1Lineage(comp)]),
  ];

  const node = frag(
    ui.printMeta(core, comp.title),
    ui.pageHeader({
      crumbs: [{ href: "#/", text: "Home" }, { href: "#/competencies", text: "Competencies" },
        comp.module ? { href: `#/competencies/${comp.module}`, text: comp.moduleLabel || humanize(comp.module) } : null, { text: comp.title }].filter(Boolean),
      kind: comp.typeLabel || "Competency", id: comp.id, title: comp.title,
      alt: (comp.alt || []).map(plain),
      lede: comp.stmt ? ui.jargon(comp.stmt, seen) : null,
      meta: frag(meta, comp.def && comp.def !== comp.stmt ? ui.disclosure("Full definition", h("p", { class: "prose" }, ui.jargon(plain(comp.def), seen)), { small: true }) : null),
      status: ui.statusLine(comp, { aboutHref: "#about" }),
    }),
    ui.withMargin(sections, main));
  return { title: comp.title, node };
}
