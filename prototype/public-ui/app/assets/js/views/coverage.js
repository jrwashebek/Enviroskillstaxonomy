// What EMST covers (#/coverage). Brief: DEV_COVERAGE (HCD lead). Licence: Apache-2.0.
// Where this release has roles, where it has only competencies and tasks, and where it has nothing yet. The scope map is
// data/coverage.js (loaded only by this page); roles, competencies and job families come from core.js. Every number is
// computed here from the data. Roles carry no subsector, so they are counted by module. Status is always in words.
import { h, icon } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { COPY, fill } from "../content.js";
import { focusSection, parseHash } from "../lib/router.js";
import { pageHeader, section, withMargin, table, notice, emptyState, link, fmt, plural } from "../ui.js";

const T = COPY.coverage;
const STATUS = { roles: ["badge--ok", "check"], comps: ["badge--info", "layers"], compsOnly: ["badge--info", "layers"], none: ["cov-badge-none", null] };
const DEPTHS = ["full", "lower", "emerging"];
const depthOf = (r) => (r.whatsComingOnly ? "emerging" : r.depth === "P1" ? "full" : "lower");
const SHORT = { full: ["full profile", "full profiles"], lower: ["earlier draft", "earlier drafts"], emerging: ["emerging", "emerging"] };
const count = (n, [one, many]) => `${fmt(n)} ${n === 1 ? one : many}`;
/** Template with {tokens} filled by strings or nodes. */
const fillN = (tpl, vars) => String(tpl).split(/(\{\w+\})/).map((p) => { const m = /^\{(\w+)\}$/.exec(p); return m && m[1] in vars ? vars[m[1]] : p; });
/** [a, b, c] -> a, b and c (strings or nodes). */
const andList = (xs) => xs.flatMap((x, i) => [i === 0 ? null : i === xs.length - 1 ? " and " : ", ", x]);
const badge = (st) => h("span", { class: ["badge", "badge--compact", STATUS[st][0]] }, STATUS[st][1] ? icon(STATUS[st][1]) : null, T.status[st][0]);

// The heading and opening come from core.js, so they show at once; the scope map fills in when data/coverage.js arrives
// (it is not in the early-data map, so on a slow connection it lands one round trip after the app).
export async function render() {
  const core = await data.core();
  const subjectNs = Object.keys(core.labels?.module || {}).filter((ns) => ns !== "core");
  const withRoles = new Set(core.roles.filter((r) => !r.whatsComingOnly).map((r) => r.module).filter((ns) => subjectNs.includes(ns)));
  const slot = h("div", { class: "loading", role: "status" }, h("span", { class: "spinner", "aria-hidden": "true" }), "Loading the scope map…");
  const node = h("div",
    pageHeader({ crumbs: [{ href: "#/", text: "Home" }, { href: "#/about", text: "About the data" }, { text: T.title }], title: T.title, lede: T.lede,
      meta: h("div", { class: "cov-intro" }, h("p", fill(T.modules, { n: fmt(withRoles.size), total: fmt(subjectNs.length) })), h("p", T.purpose)) }),
    slot);
  data.coverage().then((cov) => {
    if (!slot.isConnected) return;
    slot.replaceWith(body(core, cov));
    const { section: target } = parseHash();
    if (target && document.getElementById(target) && [document.body, node.querySelector("h1")].includes(document.activeElement)) focusSection(target);
  }).catch(() => {
    if (!slot.isConnected) return;
    slot.replaceWith(emptyState({ title: COPY.errors.load.title, body: COPY.errors.load.body, iconName: "alert" }));
  });
  return { title: T.title, node };
}

function body(core, cov) {
  const mod = new Map(cov.modules.map((m) => [m.ns, m]));
  const coreMod = cov.modules.find((m) => m.core) || { nComps: 0, nTasks: 0 };
  const subjectMods = cov.modules.filter((m) => !m.core);
  const subs = cov.subsectors;
  const rolesIn = new Map();
  for (const r of core.roles.slice().sort((a, b) => DEPTHS.indexOf(depthOf(a)) - DEPTHS.indexOf(depthOf(b)) || a.title.localeCompare(b.title))) {
    const ns = mod.has(r.module) ? r.module : coreMod.ns;
    if (!rolesIn.has(ns)) rolesIn.set(ns, []);
    rolesIn.get(ns).push(r);
  }
  const listedIn = (ns) => (rolesIn.get(ns) || []).filter((r) => !r.whatsComingOnly);
  const isCore = (s) => !!mod.get(s.module)?.core;
  const nComps = (s) => (isCore(s) ? coreMod.nComps : (s.comps || []).length);
  const nTasks = (s) => (isCore(s) ? coreMod.nTasks : s.nTasks || 0);
  const statusOf = (s) => (listedIn(s.module).length ? "roles" : nComps(s) ? (nTasks(s) ? "comps" : "compsOnly") : "none");
  const tally = (list) => { const t = {}; for (const s of list) { const st = statusOf(s); t[st] = (t[st] || 0) + 1; } return t; };
  const used = Object.keys(STATUS).filter((st) => subs.some((s) => statusOf(s) === st));
  const compBy = new Map(core.comps.map((c) => [c.slug, c]));
  const cid = (c) => `cov-${c.toLowerCase()}`;
  const coreAreas = subs.filter(isCore).length;

  // ---------------------------------------------------------------- cells (shared by the table and the phone cards)
  const moduleCell = (s) => (isCore(s) ? T.coreModule : [mod.get(s.module)?.label || s.module, h("span", { class: "cov-wave" }, fill(T.wave, { n: mod.get(s.module)?.wave }))]);
  const rolesText = (ns) => {
    const rs = rolesIn.get(ns) || [];
    if (!rs.length) return T.none;
    return DEPTHS.map((d) => [d, rs.filter((r) => depthOf(r) === d).length]).filter(([, n]) => n).map(([d, n]) => count(n, SHORT[d])).join(", ");
  };
  const compLinks = (s) => h("ul", { class: "cov-comps" }, (s.comps || []).map((slug) => h("li", h("a", { href: link.comp(slug) }, compBy.get(slug)?.title || slug))));
  const compsCell = (s) => {
    if (isCore(s)) return [fmt(coreMod.nComps), h("span", { class: "cov-wave" }, T.coreShared)];
    const n = nComps(s);
    if (!n) return T.none;
    return statusOf(s) === "roles" ? fmt(n) : [fmt(n), compLinks(s)];
  };
  const tasksCell = (s) => (isCore(s) ? [fmt(coreMod.nTasks), h("span", { class: "cov-wave" }, T.coreShared)] : nTasks(s) ? fmt(nTasks(s)) : T.none);
  const rolesHead = (list) => (list.every(isCore) ? T.col.rolesCore : T.col.roles);

  function asTable(cl, list) {
    return table({
      caption: `${cl.label}: ${plural(list.length, "subsector")}`, hint: T.tableHint, sticky: false,
      columns: [
        { key: "sub", label: T.col.sub, render: (s) => s.label },
        { key: "module", label: T.col.module, render: moduleCell },
        { key: "roles", label: rolesHead(list), render: (s) => rolesText(s.module) },
        { key: "comps", label: T.col.comps, render: compsCell },
        { key: "tasks", label: T.col.tasks, num: true, render: tasksCell },
        { key: "status", label: T.col.status, render: (s) => badge(statusOf(s)) },
      ],
      rows: list,
    });
  }
  function asCards(cl, list) {
    return h("ul", { class: "cov-cards", "aria-label": `${cl.label}: ${plural(list.length, "subsector")}` }, list.map((s) => h("li", { class: "cov-card" },
      h("h4", { class: "cov-card__title" }, s.label),
      h("p", { class: "cov-card__status" }, h("span", { class: "vh" }, `${T.col.status}: `), badge(statusOf(s))),
      h("dl", { class: "facts" },
        h("dt", T.col.module), h("dd", moduleCell(s)),
        h("dt", isCore(s) ? T.col.rolesCore : T.col.roles), h("dd", rolesText(s.module)),
        h("dt", T.col.comps), h("dd", compsCell(s)),
        h("dt", T.col.tasks), h("dd", tasksCell(s))))));
  }

  // Roles by module, below each area: listed roles by name; emerging roles only as a count, linked to What's changing.
  function rolesByModule(list) {
    const nss = [...new Set(list.map((s) => s.module))].filter((ns) => (rolesIn.get(ns) || []).length);
    if (!nss.length) return h("p", { class: "meta" }, T.noRoles);
    return h("div", { class: "cov-mods" }, h("h4", T.rolesBy), h("dl", nss.map((ns) => {
      const rs = rolesIn.get(ns), em = rs.filter((r) => r.whatsComingOnly);
      return [h("dt", mod.get(ns)?.core ? T.coreModule : mod.get(ns)?.label || ns),
        h("dd", h("ul", { class: "cov-rolelist" },
          rs.filter((r) => !r.whatsComingOnly).map((r) => h("li", h("a", { href: link.role(r.slug) }, r.title), " ", h("span", { class: "meta" }, `(${SHORT[depthOf(r)][0]})`))),
          em.length ? h("li", h("a", { href: em.length === 1 ? `#/changing@${em[0].slug}` : "#/changing@emerging-roles" }, `${fmt(em.length)} ${em.length === 1 ? "emerging role" : "emerging roles"}`), " ", h("span", { class: "meta" }, `(${T.emergingIn})`)) : null))];
    })));
  }

  // One block per area: heading, a summary line, the table (or cards on phones) and the roles by module.
  const wraps = [];
  const statusLine = (t) => used.filter((st) => t[st]).map((st) => `${T.status[st][0]}: ${fmt(t[st])}.`).join(" ");
  const areas = cov.clusters.map((cl) => {
    const list = subs.filter((s) => s.cluster === cl.code);
    if (!list.length) return null;
    const wrap = h("div", { class: "cov-wrap" });
    wraps.push({ wrap, cl, list });
    return h("div", { class: "cov-area", id: cid(cl.code), tabindex: "-1" },
      h("h3", cl.label), h("p", { class: "meta" }, `${plural(list.length, "subsector")}. ${statusLine(tally(list))}`), wrap, rolesByModule(list));
  }).filter(Boolean);
  const mq = window.matchMedia("(min-width: 40rem)");
  let wide = null;
  const draw = () => { if (wide === mq.matches) return; wide = mq.matches; for (const w of wraps) w.wrap.replaceChildren(wide ? asTable(w.cl, w.list) : asCards(w.cl, w.list)); };
  const onMq = () => { if (!wraps[0]?.wrap.isConnected) { mq.removeEventListener("change", onMq); return; } draw(); };
  mq.addEventListener("change", onMq);
  draw();

  // ---------------------------------------------------------------- sections
  const total = tally(subs);
  const summary = section("cov-summary", T.s.summary, [
    h("p", fill(T.scale, { subsectors: fmt(subs.length), clusters: fmt(areas.length) })),
    h("p", fill(T.totals, { subsectors: fmt(subs.length) })),
    h("ul", { class: "cov-totals" }, used.map((st) => h("li", badge(st), h("span", plural(total[st], "subsector"))))),
    h("p", T.byArea),
    h("ul", { class: "cov-areas" }, cov.clusters.filter((cl) => subs.some((s) => s.cluster === cl.code)).map((cl) => {
      const list = subs.filter((s) => s.cluster === cl.code);
      return h("li", h("a", { href: `#${cid(cl.code)}` }, cl.label), h("span", { class: "meta" }, ` ${plural(list.length, "subsector")}. ${statusLine(tally(list))}`));
    })),
  ]);

  const byDepth = Object.fromEntries(DEPTHS.map((d) => [d, core.roles.filter((r) => depthOf(r) === d).length]));
  const kinds = section("cov-kinds", T.s.kinds, [
    h("p", T.kindsIntro),
    h("dl", { class: "cov-kinds" }, DEPTHS.filter((d) => byDepth[d]).map((d) => [h("dt", `${T.kinds[d][0]}: ${fmt(byDepth[d])}`),
      h("dd", T.kinds[d][1], d === "emerging" ? [" ", h("a", { href: "#/changing@emerging-roles" }, "See them in What's changing")] : null)])),
    h("p", h("a", { class: "arrow-link", href: "#/roles" }, T.kindsLink, icon("arrow-right"))),
  ]);

  const map = section("cov-map", T.s.map, [
    h("p", fill(T.mapIntro, { core: fmt(coreAreas) })),
    h("p", { class: "cov-draft" }, icon("draft"), h("span", T.mapDraft)),
    h("h3", T.howTitle), h("ul", T.how.map((x) => h("li", x))),
    h("h3", T.statusTitle), h("dl", { class: "cov-key" }, used.map((st) => [h("dt", badge(st)), h("dd", T.status[st][1])])),
    areas,
  ]);

  // Permitting: the editorial anchor roles (from the data build), their shared job family, and the modules that hold
  // energy, transmission and mine permitting when those modules have no roles.
  const pRoles = (cov.permitting?.roles || []).map((slug) => core.roles.find((r) => r.slug === slug)).filter(Boolean);
  const fam = pRoles.length ? core.jobFamilies.find((f) => pRoles.every((r) => (f.roles || []).some((x) => x.slug === r.slug))) : null;
  const pMods = [...new Set((cov.permitting?.subsectors || []).map((c) => subs.find((s) => s.code === c)?.module).filter(Boolean))]
    .map((ns) => mod.get(ns)).filter((m) => m && !m.core && !listedIn(m.ns).length);
  const pComps = core.comps.filter((c) => pMods.some((m) => m.ns === c.module));
  const permitting = pRoles.length ? section("cov-permitting", T.s.permitting, [notice("info", null, h("p",
    fillN(T.permitting[0], { n: fmt(pRoles.length), roles: andList(pRoles.map((r) => h("a", { href: link.role(r.slug) }, r.title))) }),
    fam ? [" ", fill(T.permitting[1], { family: fam.title })] : null,
    pMods.length ? [" ", fill(T.permitting[2], { modules: andList(pMods.map((m) => `“${m.label}”`)).join("") })] : null,
    pComps.length ? [" ", fillN(T.permittingComps, { n: plural(pComps.length, "competency", "competencies"), comps: andList(pComps.map((c) => h("a", { href: link.comp(c.slug) }, c.title))) })] : null))]) : null;

  const waveNos = [...new Set(subjectMods.map((m) => m.wave).filter((w) => w != null))].sort((a, b) => a - b);
  const waves = section("cov-waves", T.s.waves, [
    h("p", fill(T.wavesIntro[0], { first: waveNos[0] }), waveNos.length > 1 ? [" ", fill(T.wavesIntro[1], { later: andList(waveNos.slice(1).map(String)).join("") })] : null),
    h("ul", waveNos.map((w) => {
      const ms = subjectMods.filter((m) => m.wave === w), wr = ms.filter((m) => listedIn(m.ns).length);
      const n = !wr.length ? "none" : wr.length === ms.length ? `all ${fmt(wr.length)}` : fmt(wr.length);
      return h("li", fill(T.waveLine, { n: w, mods: plural(ms.length, "module"), withRoles: n }).replace(/\.$/, ""),
        wr.length && wr.length < ms.length ? ` (${wr.map((m) => `“${m.label}”`).join(", ")})` : "", ".");
    })),
  ]);

  const o = cov.outside || {};
  const taskList = (ts) => h("ul", ts.map((t) => h("li", h("a", { href: link.task(t.slug) }, t.stmt))));
  const ednaComps = [...new Map((o.edna || []).filter((t) => t.comp?.slug).map((t) => [t.comp.slug, t.comp])).values()];
  const outside = section("cov-outside", T.s.outside, [
    h("p", T.outside[0]),
    o.biotechOnMap ? null : h("p", fill(T.outside[1], { n: fmt(subs.length) }), (o.biotechTasks || []).length ? null : [" ", T.biotechNoTask]),
    (o.bioengineering || []).length ? [h("p", fill(T.bioeng, { n: plural(o.bioengineering.length, "task") })), taskList(o.bioengineering)] : null,
    (o.edna || []).length && ednaComps.length ? h("p", fillN(T.edna, { n: plural(o.edna.length, "task"), comps: andList(ednaComps.map((c) => h("a", { href: link.comp(c.slug) }, c.title))) })) : null,
  ]);

  const missing = section("cov-missing", T.s.missing, [
    ...T.missing.map((x) => h("p", x)),
    h("p", h("a", { class: "arrow-link", href: "#/about/corrections@corr-missing" }, icon("flag"), T.suggest, icon("arrow-right"))),
  ]);

  const parts = [summary, kinds, map, permitting, waves, outside, missing].filter(Boolean);
  const toc = parts.map((p) => ({ id: p.id, title: p.querySelector("h2").textContent }));
  return withMargin(toc, h("div", { class: "cov-body" }, parts));
}
