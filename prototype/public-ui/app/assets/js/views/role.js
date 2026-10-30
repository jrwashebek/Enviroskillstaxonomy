// Role page: #/role/:slug and #/role/:slug/:actor. Owner: developer B. Spec: docs/DESIGN_SPEC.md §2.5.
// Leads with the work. Each status is said once per context: one status line, one pending summary per section.
// Filter, grouping and employer choice live in memory; tab clicks never change the URL. Licence: Apache-2.0.
import { h, icon, nextId, frag } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { state } from "../lib/state.js";
import * as ui from "../ui.js";
import { COPY, GLOSSARY } from "../content.js";
import { fmt, dateLong, cap } from "../lib/format.js";
import { exportFrame, copyText, toCsv, download, safeName } from "../export.js";

// ------------------------------------------------------------------ words used only on this page (CONTENT_GUIDE.md rules)
const ORDER = ["federal", "state", "local", "ngo", "private", "academic"];
const SHORT = { federal: "Federal", state: "State", local: "Local", ngo: "Nonprofit", private: "Private", academic: "Academic" };
const ADJ = { federal: "federal", state: "state", local: "local government", ngo: "nonprofit", private: "private-sector", academic: "academic" };
const FIRST = 8; // tasks shown before "Show all"
const MAX_DEST = 6;
const T = {
  s: { tasks: "The work", competencies: "Competencies", employers: "With other employers", connections: "Connections", paths: "Where it can lead", changing: "How it's changing", about: "About this record" },
  more: "More about this role",
  depth: { P1: "Full profile", P2: "Starter profile", P4: "Starter profile" },
  employers: "Employers",
  level: "Role level", group: "Group by", all: "All", byComp: "Competency", flat: "List",
  showFewer: "Show fewer tasks",
  showFewerComps: "Show fewer competencies",
  compHidden: (n) => `The other ${fmt(n)} come from subject modules, or are new or on watch.`,
  noTasks: "No tasks at this role level for this employer type.",
  otherComps: "Tasks under other competencies",
  alsoUses: "Also uses",
  compLabel: "Competency",
  compIntro: "The level this role aims for in each competency, at each role level.",
  compCaption: "Target level in each competency, by role level",
  compPending: "Not shown yet: how important each competency is, and whether it is critical.",
  noTarget: "No target at this level",
  employersIntro: "The task list above follows the type you pick.",
  linkView: "Link to this view",
  noActor: "EMST does not describe this role for the employer type in the link. Showing another employer type instead.",
  kindOf: "Kind of employer", empRole: "Employer's role", signOff: "Sign-off", where: "Where it applies", grade: "Grade range",
  signOffWords: { "position-qualification": "May involve a position qualification", licensure: "May involve a license" },
  diffTitle: "Tasks that differ from the main list",
  same: "Same tasks as the main list for this role.",
  addedHere: "Added for this employer type", leftOut: "Left out for this employer type",
  credMore: (n, any) => any ? `${fmt(n)} more ${n === 1 ? "is" : "are"} not shown until the issuer is checked.` : `${fmt(n)} ${n === 1 ? "credential is" : "credentials are"} not shown until the issuer is checked.`,
  instTitle: (n) => `Laws, rules and policies linked to this work (${fmt(n)})`,
  instMore: (n) => `${fmt(n)} more ${n === 1 ? "law, rule or policy that may affect this work is" : "laws, rules and policies that may affect this work are"} listed under `,
  statusAsOf: (d) => `Status on ${d}`,
  noStatus: "Status not recorded",
  xwTitle: "Related job classes and roles",
  hrTitle: "Federal series and state or local classes",
  seriesTitle: "Federal job series (OPM)",
  classesTitle: "State and local job classes",
  occTitle: "Occupation codes (O*NET-SOC and SOC)",
  profile: "A draft federal series profile exists for this series.",
  allUnreviewed: "All AI-suggested, not reviewed.",
  aboutMore: "Review path, who drafted it, and what it may be used for",
  grows: "Roles before and after this one", growsFrom: "Grows from", growsInto: "Can grow into",
  wcNote: (n) => `${fmt(n)} emerging ${n === 1 ? "role is" : "roles are"} also named as a next step. Emerging roles are listed only under `,
  noConnections: "No links to other systems or roles are drafted for this role yet.",
  named: "Named as a next step in this role's profile",
  sharing: "Other roles that share many competencies",
  shares: (n, m) => `Shares ${fmt(n)} of the ${fmt(m)} competencies that role needs, at the level it needs them.`,
  pathway: (n) => `A learning pathway is drafted for this move (${fmt(n)} steps).`,
  compare: "Compare",
  noDest: "No destinations are worked out for this role yet. That says nothing about which moves are possible.",
  pathsFail: "This part of the page did not load. Reload the page to try again.",
  loading: "Loading…",
  allWatch: (n) => `No change indicator has moved for this role. All ${fmt(n)} ${n === 1 ? "signal" : "signals"} about it ${n === 1 ? "is" : "are"} on watch.`,
  notAllWatch: "Some signals about this role are not on watch. See What's changing for what that means.",
  watchWhy: "A signal starts to count only after a person reviews it and a second, independent kind of evidence points the same way.",
  signalsTitle: (n) => `The ${fmt(n)} ${n === 1 ? "signal" : "signals"} about this role`,
  emergingTitle: (n) => `${fmt(n)} ${n === 1 ? "competency" : "competencies"} in this role that ${n === 1 ? "is" : "are"} new or on watch`,
  seeChanging: "See what's changing across environmental work",
  roleWatch: "This role is itself on watch.",
  reviewBy: "Review by", counter: "What would show it is not forming",
  copied: "Tasks copied. Paste them into your document.",
  copyFail: "Could not copy. Use Download CSV instead, or select the text and copy it.",
  saved: "CSV file saved to your device.",
  notes: "Drafted by AI agents; not yet reviewed by people; describes work only",
  // P3 ("What's coming only") page
  wcKind: "Emerging role",
  wcTitle: "This role is on watch",
  wcBody: "It is a hypothesis about work that may be forming. It does not describe jobs that exist today, so it has no tasks or competency levels. EMST lists it under What's changing.",
  wcLink: "Go to What's changing",
  horizon: "Time frame", sectors: "Employer types it may appear in", signals: "Signals pointing to it", feeders: "Roles it may grow from",
};
const PRED_WORDS = { exactMatch: "exact fit", closeMatch: "close fit", broadMatch: "broader", narrowMatch: "more specific", relatedMatch: "related in part", mirrorRole: "mirror role" };

// ------------------------------------------------------------------ small helpers
const keyOf = (v) => (v.slug.split("--")[1] || v.actor);
const joinAnd = (xs) => (xs.length < 2 ? xs.join("") : `${xs.slice(0, -1).join(", ")} and ${xs[xs.length - 1]}`);
const cleanLabel = (s) => String(s || "").replace(/\s*\([^)]*$/, "").trim(); // vocabulary labels cut at a comma, e.g. "Special district (water"
const primaryOf = (t) => (t.comps || []).find((c) => c.strength === "primary") || (t.comps || [])[0] || null;
const recordId = (module, slug) => `emst:${module || "core"}/${String(slug).toUpperCase()}`;
const splitParen = (s) => { const m = /^(.*?)\s*\((.*)\)\s*$/.exec(String(s || "")); return m ? [m[1], m[2]] : [String(s || ""), ""]; };
const sentence = (s) => { const t = cap(String(s || "").trim()); return t && !/[.!?]$/.test(t) ? `${t}.` : t; };
/** Plain words for data text shown on this page: no SKOS terms, prefixes or model acronyms (brief: forbidden strings). */
function clean(s) {
  return String(s || "")
    .replace(/(?:skos|emst):(\w+)/g, (_, p) => PRED_WORDS[p] || p.replace(/Match$/, ""))
    .replace(/\bONETSOC:/g, "O*NET-SOC ").replace(/\bSOC2018:/g, "SOC ").replace(/\bOPMseries:/g, "OPM series ")
    .replace(/\bLLM-vs-LLM\b/g, "AI against AI").replace(/\bLLMs?\b/g, "AI")
    .replace(/\bSMEs\b/g, "subject-matter experts").replace(/\bSME\b/g, "subject-matter expert")
    .replace(/\bPS\b/g, "private-sector agent").replace(/\(FH\)/g, "(federal HR agent)");
}
function via(text) {
  const s = String(text || "");
  let m = /^(.*?) \(typed link on this variant\)$/.exec(s);
  if (m) return sentence(m[1]);
  m = /^sensitivity to DM-\d+ \((.*)\)$/.exec(s);
  if (m) return `Sensitive to changes in ${m[1].replace(/\b(esa|nepa|cwa|caa)\b/gi, (x) => x.toUpperCase())}.`;
  return sentence(s.replace(/\bDM-\d+\s*/g, ""));
}
const horizonWords = (hz) => { const m = /^(\d+)\s*-\s*(\d+)\s*y$/.exec(String(hz || "")); return m ? `Within ${m[1]} to ${m[2]} years` : String(hz || ""); };
function levelsText(rl, all) {
  if (!rl || !rl.length || rl.length >= all.length) return null;
  return rl.length === 1 ? `${cap(rl[0])} level only` : `${cap(joinAnd(rl))} levels`;
}
function tabLabel(v, dup) {
  const base = SHORT[v.actor] || cleanLabel(v.actorLabel);
  return dup ? `${base}: ${String(v.authorityLabel || keyOf(v)).toLowerCase()}` : base;
}
function variantName(v, dup) {
  return dup && v.authorityLabel ? `${v.actorLabel} (${v.authorityLabel.toLowerCase()})` : v.actorLabel;
}
/** crosswalkList appends the crosswalk note to every list; this page says it once per section instead. */
function xwList(rows, opts) {
  const f = ui.crosswalkList(rows, opts);
  if (f && f.lastChild && COPY.match?.note && f.lastChild.textContent === COPY.match.note) f.removeChild(f.lastChild);
  return f;
}
const xwNote = () => h("p", { class: "meta" }, COPY.match?.note || "");
function cleanRows(rows, { keepVer = true } = {}) {
  return (rows || []).map((r) => ({ ...r, note: r.note ? clean(r.note) : undefined, ver: keepVer ? r.ver : undefined }));
}
/** Borrowed references are dated once per list, not once per row. Rows with a different version keep their own. */
function refVersion(rows) {
  const vs = [...new Set((rows || []).map((r) => r.ver).filter(Boolean))];
  return vs.length === 1 ? h("p", { class: "meta" }, `${COPY.match?.asOf || "Reference version"}: ${vs[0]}`) : null;
}
function stripVer(rows) {
  const vs = new Set((rows || []).map((r) => r.ver).filter(Boolean));
  return vs.size === 1 ? rows.map((r) => ({ ...r, ver: undefined })) : rows;
}
/** "About this record" in layers (CONTENT_GUIDE §5): one plain paragraph on what AI did and what people have not done yet,
 *  then the review path, the use ladder and the provenance facts from ui.aboutRecord in one disclosure. Citation,
 *  corrections and exports stay open. */
function aboutParts(fr) {
  const kids = [...fr.childNodes];
  const ladders = kids.filter((n) => n.classList?.contains("ev-ladder"));
  const facts = kids.find((n) => n.matches?.("dl.facts"));
  if (ladders.length < 2 || !facts) return fr;
  const moved = [...ladders, facts];
  return frag(h("p", { class: "b-ai" }, COPY.ai?.detail || ""), ui.disclosure(T.aboutMore, moved), kids.filter((n) => !moved.includes(n)));
}
/** Below 64rem "On this page" sits above the content, so it folds into a closed disclosure there: one tab stop
 *  instead of seven before the first task (spec §2.5 AC). From 64rem it stays open in the margin. */
function compactToc(layout) {
  const side = layout.querySelector(".with-margin__side"), nav = side?.querySelector(".toc");
  if (!nav) return;
  const drawer = ui.disclosure(COPY.site?.onThisPage || "On this page", null);
  drawer.classList.add("b-toc-drawer");
  const body = drawer.querySelector(".drawer__body");
  const mq = window.matchMedia("(max-width: 63.99rem)");
  const place = () => {
    if (!layout.isConnected && drawer.dataset.placed) { mq.removeEventListener("change", place); return; }
    drawer.dataset.placed = "1";
    if (mq.matches) { body.appendChild(nav); side.appendChild(drawer); } else { side.appendChild(nav); drawer.remove(); }
  };
  mq.addEventListener("change", place);
  place();
}
function sortVariants(list) {
  return list.slice().sort((a, b) => (ORDER.indexOf(a.actor) - ORDER.indexOf(b.actor)) || String(a.authorityLabel || "").localeCompare(String(b.authorityLabel || "")));
}

// ------------------------------------------------------------------ entry point
export async function render({ params }) {
  const core = await data.core();
  const role = await data.role(params.slug);
  if (role.whatsComingOnly) return watchPage(core, role);
  return rolePage(core, role, params.actor || null);
}

// ------------------------------------------------------------------ full role page (P1, P2, P4)
function rolePage(core, role, actorParam) {
  const pathsP = data.paths(); // loads beside the page; "Where it can lead" fills in when it arrives
  pathsP.catch(() => {});
  const variants = sortVariants(role.variants || []);
  const dupActor = new Set(variants.map((v) => v.actor).filter((a, i, all) => all.indexOf(a) !== i));
  const isDup = (v) => dupActor.has(v.actor);
  const chosen = actorParam ? (variants.find((v) => keyOf(v) === actorParam) || variants.find((v) => v.actor === actorParam)) : null;
  const st = { variant: chosen || variants[0] || null, level: "all", group: "comp", expanded: false, ordered: [] };
  const levels = role.levels || [];
  const levelKeys = levels.map((l) => l.key);
  const bundle = role.tasks || [];
  const bundleSet = new Set(bundle.map((t) => t.slug));
  const taskBy = new Map([...bundle, ...(role.addedTasks || [])].map((t) => [t.slug, t]));
  const compBy = new Map(core.comps.map((c) => [c.slug, c]));
  const targets = role.targets || [];
  const targetOrder = new Map(targets.map((t, i) => [t.slug, i]));
  const seen = new Set();

  function itemsFor(v) {
    if (!v || v.sameTasks || !v.tasks) return bundle.map((t) => ({ t, formation: !!t.formation, roleLevels: t.roleLevels || [], added: false }));
    return v.tasks.map((x) => ({ t: taskBy.get(x.slug), formation: !!x.formation, roleLevels: x.roleLevels || [], added: !bundleSet.has(x.slug) })).filter((x) => x.t);
  }
  function diffFor(v) {
    if (!v || v.sameTasks || !v.tasks) return { added: [], removed: [] };
    const vs = new Set(v.tasks.map((x) => x.slug));
    return { added: v.tasks.filter((x) => !bundleSet.has(x.slug)).map((x) => taskBy.get(x.slug)).filter(Boolean), removed: bundle.filter((t) => !vs.has(t.slug)) };
  }
  const variantUrl = (v) => `${location.href.split("#")[0]}#/role/${role.slug}${v ? "/" + keyOf(v) : ""}`;

  // ---------------------------------------------------------------- header
  const fam = (core.jobFamilies || []).find((f) => (f.roles || []).some((r) => r.slug === role.slug));
  const crumbs = [{ href: "#/roles", text: "Roles" }];
  if (fam) crumbs.push({ href: "#/roles", text: fam.title });
  crumbs.push({ text: role.title });
  const lede = ui.jargon(role.fn || "", seen);
  const defNode = role.def ? (role.def.length > 280 ? ui.disclosure(T.more, h("p", ui.jargon(role.def, seen))) : h("p", ui.jargon(role.def, seen))) : null;
  const actorsShown = variants.map((v) => tabLabel(v, isDup(v)));
  const metaRow = h("div", { class: "b-head-extra" }, defNode,
    h("ul", { class: "cluster b-meta", "aria-label": "About this role" },
      h("li", { class: "b-meta__depth" }, T.depth[role.depth] || role.depthLabel || ""),
      actorsShown.length ? h("li", { class: "b-meta__emp" }, h("span", { class: "vh" }, `${T.employers}: `),
        h("ul", { class: "cluster" }, actorsShown.map((a) => h("li", h("span", { class: "badge badge--compact" }, a))))) : null));
  const head = ui.pageHeader({ crumbs, kind: "Role profile", id: role.id, title: role.title, alt: role.alt, lede, meta: metaRow, status: ui.statusLine(role, { aboutHref: "#about" }) });
  if (fam) {
    const famLink = head.querySelectorAll(".breadcrumb a")[1];
    famLink?.addEventListener("click", () => { state.roleFilters = { families: new Set([fam.slug]), actors: new Set(), depth: new Set() }; });
  }
  const headSeen = new Set(seen);

  // ---------------------------------------------------------------- the work
  const work = (() => {
    const listId = nextId("b-tasks");
    const note = h("p", { class: "b-variant-note", hidden: true });
    const levelGroup = levels.length > 1 ? ui.chipGroup({ legend: T.level, name: nextId("b-lvl"), multi: false, checked: ["all"],
      options: [{ value: "all", label: T.all, count: 0 }, ...levels.map((l) => ({ value: l.key, label: cap(l.key), count: 0 }))],
      onChange: (vals) => { st.level = [...vals][0] || "all"; draw(); } }) : null;
    const groupGroup = ui.chipGroup({ legend: T.group, name: nextId("b-grp"), multi: false, checked: ["comp"],
      options: [{ value: "comp", label: T.byComp }, { value: "list", label: T.flat }],
      onChange: (vals) => { st.group = [...vals][0] || "comp"; draw(); } });
    const def = h("p", { class: "meta b-def" }, h("span", { class: "badge badge--compact b-tag" }, icon("user-group"), COPY.formation?.tag || "Formation task"), " ", COPY.formation?.explain || "");
    const count = ui.liveCount();
    count.node.classList.add("b-count", "no-print");
    const list = h("div", { class: "b-tasks", id: listId });
    const moreLab = h("span");
    const more = h("button", { class: "btn btn--secondary b-more", type: "button", "aria-controls": listId, "aria-expanded": "false" }, moreLab);
    more.addEventListener("click", () => {
      st.expanded = !st.expanded;
      list.classList.toggle("is-expanded", st.expanded);
      more.setAttribute("aria-expanded", String(st.expanded));
      setMoreLabel(); setCount(true);
    });
    const pend = h("div", { class: "b-pending" });
    let filtered = [];
    function setMoreLabel() { moreLab.textContent = st.expanded ? T.showFewer : `Show all ${fmt(filtered.length)} tasks`; more.hidden = filtered.length <= FIRST; }
    function setCount(live) {
      const lv = st.level === "all" ? "" : ` at ${st.level} level`;
      const n = filtered.length;
      const text = !n ? T.noTasks : n <= FIRST || st.expanded ? `Showing all ${fmt(n)} tasks${lv}.` : `Showing ${fmt(FIRST)} of ${fmt(n)} tasks${lv}.`;
      if (live) count.set(text); else count.node.textContent = text;
    }
    function taskItem(x, idx, s) {
      const t = x.t, p = primaryOf(t);
      const tags = [];
      if (x.formation) tags.push(h("span", { class: "badge badge--compact b-tag" }, icon("user-group"), COPY.formation?.tag || "Formation task"));
      if (x.added) tags.push(h("span", { class: "badge badge--compact b-tag" }, icon("plus"), `Added for ${ADJ[st.variant.actor] || st.variant.actor} roles`));
      const bits = [];
      const lv = levelsText(x.roleLevels, levelKeys);
      if (lv) bits.push(h("span", lv));
      if (st.group === "list" && p) bits.push(h("span", `${T.compLabel}: `, h("a", { href: ui.link.comp(p.slug) }, p.title)));
      const contrib = (t.comps || []).filter((c) => c !== p);
      if (contrib.length) bits.push(h("span", `${T.alsoUses}: `, contrib.map((c, i) => [i ? "; " : "", h("a", { href: ui.link.comp(c.slug) }, c.title)])));
      return h("li", { class: ["b-task", idx >= FIRST && "is-extra"] },
        h("a", { class: "b-task__link", href: ui.link.task(t.slug) }, ui.jargon(t.stmt, s)),
        tags.map((g) => [" ", g]),
        bits.length ? h("p", { class: "task-list__meta b-task__meta" }, bits) : null);
    }
    function draw(live = true) {
      const v = st.variant;
      const items = itemsFor(v);
      filtered = st.level === "all" ? items : items.filter((x) => x.roleLevels.includes(st.level));
      const s = new Set(headSeen);
      let nodes;
      if (st.group === "comp") {
        const groups = new Map();
        for (const x of filtered) { const p = primaryOf(x.t); const k = p ? p.slug : ""; if (!groups.has(k)) groups.set(k, { comp: p, items: [] }); groups.get(k).items.push(x); }
        const ordered = [...groups.values()].sort((a, b) => (targetOrder.get(a.comp?.slug) ?? 1e6) - (targetOrder.get(b.comp?.slug) ?? 1e6));
        st.ordered = ordered.flatMap((g) => g.items);
        let i = 0;
        nodes = ordered.map((g) => {
          const start = i; i += g.items.length;
          return h("div", { class: ["task-group", "b-group", start >= FIRST && "is-extra"] },
            h("h3", { class: "b-group__title" }, g.comp ? h("a", { href: ui.link.comp(g.comp.slug) }, g.comp.title) : T.otherComps),
            h("ul", { class: "task-list" }, g.items.map((x, j) => taskItem(x, start + j, s))));
        });
      } else {
        st.ordered = filtered;
        nodes = [h("ul", { class: "task-list" }, filtered.map((x, j) => taskItem(x, j, s)))];
      }
      list.replaceChildren(...(filtered.length ? nodes : [ui.emptyState({ title: T.noTasks, body: null })]));
      if (!laterSeen) laterSeen = s;
      def.hidden = !items.some((x) => x.formation);
      if (levelGroup) {
        const counts = { all: items.length };
        for (const l of levelKeys) counts[l] = items.filter((x) => x.roleLevels.includes(l)).length;
        levelGroup.counts(counts);
      }
      const d = diffFor(v);
      if (v && (d.added.length || d.removed.length)) {
        const parts = [d.added.length ? `adds ${fmt(d.added.length)} ${d.added.length === 1 ? "task" : "tasks"}` : null, d.removed.length ? `leaves out ${fmt(d.removed.length)} ${d.removed.length === 1 ? "task" : "tasks"} from the main list` : null].filter(Boolean);
        note.textContent = `This list follows the ${variantName(v, isDup(v)).toLowerCase()} version of the role, which ${joinAnd(parts)}.`;
        note.hidden = false;
      } else note.hidden = true;
      const chg = v?.chg;
      pend.replaceChildren(ui.pendingSummary(chg ? { total: chg.nTasks, assessed: chg.nAssessed, unit: "tasks" } : { unit: "tasks" }));
      setMoreLabel(); setCount(live);
    }
    let laterSeen = null;
    draw(false);
    const node = ui.section("tasks", T.s.tasks, [
      note,
      h("div", { class: "b-controls no-print" }, levelGroup?.node, groupGroup.node),
      def, count.node, list, more, pend]);
    return { node, draw, seen: () => laterSeen || new Set(headSeen) };
  })();
  const rest = work.seen(); // glossary terms already expanded at the top of the page

  // ---------------------------------------------------------------- competencies
  const comps = (() => {
    const defaults = targets.filter((t) => t.isDefault), extras = targets.filter((t) => !t.isDefault);
    const rows = [...defaults, ...extras];
    const wrapId = nextId("b-comps");
    const wrap = h("div", { class: "b-comps", id: wrapId });
    const moreClass = (i) => (i >= defaults.length ? "is-more2" : i >= FIRST ? "is-more1" : null);
    const extraMeta = (t) => {
      if (t.isDefault) return null;
      const bits = [t.isModule && t.moduleLabel ? t.moduleLabel : null, t.lc && t.lc !== "established" ? (COPY.lifecycle?.[t.lc]?.label || t.lc) : null].filter(Boolean);
      return bits.length ? h("span", { class: "meta b-comp__extra" }, bits.join(" · ")) : null;
    };
    const chip = (code) => { const c = ui.levelChip(code, core); c.classList.add("badge--compact"); return c; };
    const cell = (t, key) => (t.levels?.[key] ? chip(t.levels[key]) : h("span", { class: "meta" }, h("span", { "aria-hidden": "true" }, "—"), h("span", { class: "vh" }, T.noTarget)));
    const compLink = (t) => h("a", { href: ui.link.comp(t.slug) }, t.title);
    function asTable() {
      const tbl = ui.table({ caption: T.compCaption, sticky: true, rows,
        columns: [{ key: "title", label: T.compLabel, render: (t) => [compLink(t), extraMeta(t) ? [h("br"), extraMeta(t)] : null] },
          ...levels.map((l) => ({ key: l.key, label: cap(l.key), rowHeader: false, render: (t) => cell(t, l.key) }))] });
      tbl.querySelectorAll("tbody tr").forEach((tr, i) => { const c = moreClass(i); if (c) tr.classList.add(c); });
      return tbl;
    }
    function asCards() {
      return h("ul", { class: "b-comp-cards", "aria-label": T.compCaption }, rows.map((t, i) => h("li", { class: ["b-comp-card", moreClass(i)] },
        h("p", { class: "b-comp-card__title" }, compLink(t)), extraMeta(t),
        h("dl", { class: "b-comp-card__levels" }, levels.map((l) => h("div", h("dt", cap(l.key)), h("dd", cell(t, l.key))))))));
    }
    const mq = window.matchMedia("(min-width: 40rem)");
    let wide = null;
    const draw = () => { if (wide === mq.matches) return; wide = mq.matches; wrap.replaceChildren(wide ? asTable() : asCards()); };
    const onMq = () => { if (!wrap.isConnected) { mq.removeEventListener("change", onMq); return; } draw(); };
    mq.addEventListener("change", onMq);
    draw();
    // Like the task list: the first 8, then the rest of the main set, then modules and emerging content.
    const has1 = defaults.length > FIRST, has2 = extras.length > 0, start = has1 ? 0 : 1;
    let step = start;
    const lab = h("span");
    const more = has1 || has2 ? h("button", { class: "btn btn--secondary b-more", type: "button", "aria-controls": wrapId }, lab) : null;
    const count = ui.liveCount();
    count.node.classList.add("b-count", "no-print");
    const setStep = (n, live = true) => {
      step = n; wrap.dataset.step = String(n);
      const shown = n === 0 ? FIRST : n === 1 ? defaults.length : rows.length;
      const text = shown >= rows.length ? `Showing all ${fmt(rows.length)} competencies.` : `Showing ${fmt(shown)} of ${fmt(rows.length)} competencies.${n === 1 ? ` ${T.compHidden(extras.length)}` : ""}`;
      if (live) count.set(text); else count.node.textContent = text;
      if (!more) return;
      lab.textContent = n === 0 ? `Show ${fmt(defaults.length - FIRST)} more competencies` : n === 1 && has2 ? `Show ${fmt(extras.length)} more (modules and emerging)` : T.showFewerComps;
      more.setAttribute("aria-expanded", String(n === 2 || (n === 1 && !has2)));
    };
    more?.addEventListener("click", () => setStep(step === 0 ? 1 : step === 1 && has2 ? 2 : start));
    setStep(start, false);
    if (!rows.length) return ui.section("competencies", T.s.competencies, [h("p", T.noTarget)]);
    return ui.section("competencies", T.s.competencies, [
      h("p", { class: "meta" }, core.text.targetsNote),
      count.node, wrap, more,
      h("p", { class: "b-pend-line" }, ui.pendingInline(COPY.pending?.title), " ", T.compPending)]);
  })();

  // ---------------------------------------------------------------- with other employers
  const linkView = h("a", { class: "b-viewlink__a" }, T.linkView);
  const linkViewWhich = h("span", { class: "meta" });
  function variantPanel(v) {
    const s = rest;
    const facts = [];
    const fact = (k, val) => { if (val) facts.push(h("dt", k), h("dd", val)); };
    fact(T.kindOf, cleanLabel(v.subtypeLabel));
    fact(T.empRole, v.authorityLabel);
    fact(T.signOff, v.signOff ? (T.signOffWords[v.signOff] || cap(String(v.signOff).replace(/-/g, " "))) : v.signOffPending ? core.text.signOffPending : null);
    fact(T.where, (v.jurisdiction || []).length ? v.jurisdiction.map((j) => cap(String(j).replace(/-/g, " "))).join("; ") : null);
    if (v.grade?.bands?.length) {
      const g = GLOSSARY[v.grade.scheme];
      fact(T.grade, [v.grade.bands.map((b) => h("span", { class: "b-band" }, `${cap(b.level)}: ${b.band}`)),
        h("span", { class: "meta b-grade-note" }, g?.exp ? `${v.grade.scheme} is the ${g.exp} pay system. ` : "", sentence(core.text.gradeNote), " ", sentence(v.grade.label))]);
    }
    const d = diffFor(v);
    const taskLinks = (ts) => h("ul", { class: "b-plain" }, ts.map((t) => h("li", h("a", { href: ui.link.task(t.slug) }, t.stmt))));
    const diff = v.sameTasks || !v.tasks || !(d.added.length + d.removed.length) ? h("p", T.same) : ui.disclosure(`${T.diffTitle} (${fmt(d.added.length + d.removed.length)})`, [
      d.added.length ? frag(h("p", { class: "b-sub" }, `${T.addedHere} (${fmt(d.added.length)})`), taskLinks(d.added)) : null,
      d.removed.length ? frag(h("p", { class: "b-sub" }, `${T.leftOut} (${fmt(d.removed.length)})`), taskLinks(d.removed)) : null]);
    const gates = v.credentialGates || [], gPend = v.credentialGatesPending || 0;
    const [credHead, credNote] = splitParen(core.text.credentialMayBeInvolved);
    const creds = gates.length || gPend ? frag(h("h4", credHead),
      gates.length ? h("ul", { class: "b-plain" }, gates.map((g) => h("li", ui.jargon(g.title, s)))) : null,
      gates.length && credNote ? h("p", { class: "meta" }, sentence(credNote)) : null,
      gPend ? h("p", { class: "meta" }, T.credMore(gPend, gates.length > 0)) : null) : null;
    const inst = v.instruments || [];
    const asOf = dateLong(core.release.date);
    const insts = inst.length ? ui.disclosure(T.instTitle(inst.length), h("ul", { class: "b-plain b-inst" }, inst.map((i) => h("li",
      h("p", { class: "b-inst__title" }, ui.jargon(i.title, s)),
      i.unv ? h("p", { class: "meta" }, core.text.unverified)
        : h("p", { class: "meta" }, `${T.statusAsOf(asOf)}: ${i.noEv || !i.stTxt ? T.noStatus : i.stTxt.replace(/\.$/, "")}.`, i.via ? ` ${via(i.via)}` : ""))))) : null;
    const instMore = v.instrumentsMore ? h("p", { class: "meta" }, T.instMore(v.instrumentsMore), h("a", { href: "#/changing" }, "What's changing"), ".") : null;
    const rows = cleanRows(v.crosswalks, { keepVer: false });
    const classLink = (r) => {
      if (r.none) return { text: T.xwTitle };
      const obj = String(r.obj || "");
      if (/^(state|local)-class/.test(r.set)) {
        const raw = obj.split(":").slice(1).join(":");
        const code = raw.toLowerCase();
        const jk = (/class-([a-z]+)/.exec(r.set) || [])[1] || "";
        const cands = (core.stateClasses || []).filter((c) => String(c.code).toLowerCase() === code);
        const c = cands.length > 1 ? cands.find((x) => String(x.jurCode).toLowerCase().startsWith(jk)) || cands[0] : cands[0];
        if (c) return { href: ui.link.cls(c.slug), text: `${r.lab || c.title} (${c.state})` };
        const j = (core.stateClasses || []).find((x) => String(x.jurCode).toLowerCase().split("-")[0] === jk);
        const jur = j ? String(j.state).split(", ").pop() : jk.toUpperCase();
        const what = /^title-/.test(raw) ? cap(raw.slice(6).replace(/-/g, " ")) : /^pos-/.test(raw) ? `position ${raw.slice(4)}` : `class ${raw}`;
        return { text: r.lab ? `${r.lab} (${jur})` : `${jur}: ${what}` };
      }
      const same = variants.find((x) => x.id === obj);
      if (same) return { href: ui.link.role(role.slug, keyOf(same)), text: r.lab || same.title };
      if (/^EMSTpja:/.test(obj)) return { text: `Private-sector job framework entry ${obj.split(":")[1]}` };
      return { text: r.lab || obj };
    };
    const xw = rows.length ? ui.disclosure(`${T.xwTitle} (${fmt(rows.length)})`, [xwList(rows, { noun: "class", linkFn: classLink }), xwNote()]) : null;
    return h("div", { class: "stack b-panel" },
      v.hr ? ui.notice("hr", null, core.text.hrDisclaimer.map((p) => h("p", ui.jargon(p, s)))) : null,
      h("h3", { class: "h4" }, variantName(v, isDup(v))),
      v.def ? h("p", ui.jargon(v.def, s)) : null,
      facts.length ? h("dl", { class: "facts" }, facts) : null,
      diff, creds, insts, instMore, xw);
  }
  function selectVariant(key) {
    const v = variants.find((x) => keyOf(x) === key);
    if (!v) return;
    linkView.setAttribute("href", ui.link.role(role.slug, keyOf(v)));
    linkViewWhich.textContent = ` · ${variantName(v, isDup(v))}`;
    if (v === st.variant) return;
    st.variant = v;
    work.draw(true);
  }
  const employers = variants.length ? ui.section("employers", T.s.employers, [
    actorParam && !chosen ? ui.notice("info", null, T.noActor) : null,
    h("p", { class: "meta" }, T.employersIntro),
    ui.tabs(variants.map((v) => ({ key: keyOf(v), label: tabLabel(v, isDup(v)), render: () => variantPanel(v) })), { labelledBy: "h-employers", selected: st.variant ? keyOf(st.variant) : null, onSelect: selectVariant }),
    h("p", { class: "b-viewlink no-print" }, linkView, linkViewWhich)]) : null;
  if (st.variant) selectVariant(keyOf(st.variant));

  // ---------------------------------------------------------------- connections
  const connections = (() => {
    const xws = cleanRows(role.crosswalks);
    const opm = xws.filter((x) => /^opm-series/.test(x.set));
    const onet = xws.filter((x) => /^onet-soc/.test(x.set));
    const soc = xws.filter((x) => /^soc\//.test(x.set));
    const seriesBy = new Map((core.series || []).map((s) => [s.code, s]));
    const hrSeries = role.hrSeries || [];
    const extraSeries = hrSeries.filter((s) => !opm.some((x) => x.obj === `OPMseries:${s.code}`));
    const classes = role.hrClasses || [];
    const parts = [];
    if (opm.length || extraSeries.length || classes.length) {
      parts.push(h("h3", T.hrTitle), ui.notice("hr", null, core.text.hrDisclaimer.map((p) => h("p", ui.jargon(p, rest)))));
      // One line per series: the link, its code, the plain match type, and flags. "AI-suggested" is said once for the list;
      // the agents' reasons are on each series page.
      const seriesItem = (code, title, words, profile) => {
        const rec = seriesBy.get(code);
        return h("li", { class: "b-xw" },
          h("p", { class: "b-xw__name" }, rec ? h("a", { href: ui.link.series(code) }, title || rec.title) : title, " ", h("span", { class: "id" }, code)),
          words ? h("p", { class: "meta" }, words) : null,
          rec?.realignment ? h("p", { class: "b-flag" }, icon("alert"), core.text.realignment) : null,
          profile ? h("p", { class: "meta" }, T.profile) : null);
      };
      const seriesRows = [...opm.map((r) => {
        const code = String(r.obj || "").replace(/^OPMseries:/, "");
        return r.none || !r.obj ? h("li", { class: "b-xw" }, h("p", { class: "meta" }, ui.matchWords(r, "series")))
          : seriesItem(code, r.lab, ui.matchWords(r, "series"), hrSeries.some((s) => s.code === code && s.profile));
      }), ...extraSeries.map((s) => seriesItem(s.code, s.title, null, s.profile))];
      if (seriesRows.length) parts.push(h("h4", T.seriesTitle), h("p", { class: "meta" }, [T.allUnreviewed, refVersion(opm)?.textContent].filter(Boolean).join(" ")),
        h("ul", { class: "b-xws" }, seriesRows));
      if (classes.length) parts.push(h("h4", T.classesTitle), h("ul", { class: "b-xws" }, classes.map((c) => h("li", { class: "b-xw" },
        h("p", { class: "b-xw__name" }, h("a", { href: ui.link.cls(c.slug) }, c.title), c.jur ? ` (${c.jur})` : ""),
        h("p", { class: "meta" }, [c.close ? COPY.match?.closeMatch : null, COPY.match?.unreviewed || "AI-suggested, not reviewed"].filter(Boolean).join(" · "))))));
    }
    if (onet.length || soc.length) {
      const socCode = (r) => (r.none || !r.obj ? "SOC" : `SOC ${String(r.obj).replace(/^SOC\d*:/, "")}`);
      parts.push(ui.disclosure(`${T.occTitle}: ${fmt(onet.length + soc.length)}`, [
        refVersion(onet),
        xwList(stripVer(onet), { noun: "occupation", linkFn: (r) => {
          if (r.none || !r.obj) return { text: "O*NET-SOC" };
          const code = String(r.obj).replace(/^ONETSOC:/, "");
          return /^\d{2}-\d{4}\.\d{2}$/.test(code) ? { href: `https://www.onetonline.org/link/summary/${code}`, text: `O*NET-SOC ${code}`, code } : { text: `O*NET-SOC ${code}` };
        } }),
        soc.length ? [h("h4", "SOC"), refVersion(soc), h("ul", { class: "b-plain b-soc" }, soc.map((r) => h("li", h("span", { class: "id" }, socCode(r)), " · ", ui.matchWords(r, "occupation"), r.rev ? "" : ` · ${COPY.match?.unreviewed || "AI-suggested, not reviewed"}`)))] : null]));
    }
    if (parts.length) parts.push(xwNote());
    // roles it grows from and into (emerging roles appear only under What's changing)
    const roleList = (list) => {
      const by = new Map();
      for (const r of list || []) { if (r.wc) continue; if (!by.has(r.slug)) by.set(r.slug, { r, vs: [] }); if (r.v) by.get(r.slug).vs.push(r); }
      return [...by.values()].map(({ r, vs }) => h("li",
        vs.length === 1 ? h("a", { href: ui.link.role(r.slug, String(vs[0].v).split("--")[1]) }, r.title) : h("a", { href: ui.link.role(r.slug) }, r.title),
        vs.length ? h("span", { class: "meta" }, ` · ${joinAnd(vs.map((x) => cleanLabel(x.actorLabel).toLowerCase()))}`) : null));
    };
    const from = roleList([...(role.entryFrom || []), ...(role.feeders || [])]);
    const into = roleList(role.progressesTo);
    const wc = (role.progressesTo || []).filter((r) => r.wc).length;
    if (from.length || into.length || wc) parts.push(h("h3", T.grows), h("dl", { class: "b-grows" },
      from.length ? [h("dt", T.growsFrom), h("dd", h("ul", { class: "b-plain" }, from))] : null,
      into.length || wc ? [h("dt", T.growsInto), h("dd", into.length ? h("ul", { class: "b-plain" }, into) : null,
        wc ? h("p", { class: "meta" }, T.wcNote(wc), h("a", { href: "#/changing" }, "What's changing"), ".") : null)] : null));
    return ui.section("connections", T.s.connections, parts.length ? parts : [h("p", T.noConnections)]);
  })();

  // ---------------------------------------------------------------- where it can lead (exploratory; data loads beside the page)
  const pathsBody = h("div", { class: "stack", "aria-busy": "true" }, h("p", { class: "meta" }, T.loading));
  pathsP.then((paths) => { pathsBody.removeAttribute("aria-busy"); pathsBody.replaceChildren(...pathsContent(paths)); })
    .catch(() => { pathsBody.removeAttribute("aria-busy"); pathsBody.replaceChildren(h("p", T.pathsFail)); });
  function pathsContent(paths) {
    const mine = new Set(variants.map((v) => v.slug));
    const best = new Map();
    for (const e of paths.edges || []) {
      if (!e.shown || !mine.has(e.from)) continue;
      const d = paths.variants?.[e.to];
      if (!d || d.role === role.slug) continue;
      const cur = best.get(d.role);
      const named = !!e.named || !!cur?.named;
      if (!cur || e.shared.N > cur.e.shared.N) best.set(d.role, { e, d, named });
      else cur.named = named;
    }
    const chosenDest = [...best.values()].sort((a, b) => (b.named - a.named) || (b.e.shared.N - a.e.shared.N) || a.d.title.localeCompare(b.d.title)).slice(0, MAX_DEST);
    const item = ({ e, d, named }) => {
      const pw = (paths.pathways || []).find((p) => mine.has(p.from) && p.to === d.role);
      const fric = (e.fric || []).filter((f) => typeof f === "string");
      return h("li", { class: "b-dest" },
        h("p", { class: "b-dest__title" }, h("a", { href: ui.link.role(d.role) }, d.title)),
        h("p", { class: "meta" }, named ? h("strong", { class: "b-dest__named" }, `${T.named}. `) : null, T.shares(e.shared.N, e.shared.M), pw ? ` ${T.pathway(pw.steps)}` : "", fric.length ? ` ${sentence(clean(fric.join("; ")))}` : "", " ",
          h("a", { class: "b-dest__compare", href: ui.link.compare(role.slug, d.role) }, T.compare, h("span", { class: "vh" }, ` ${role.title} with ${d.title}`))));
    };
    const byTitle = (a, b) => (b.named - a.named) || a.d.title.localeCompare(b.d.title);
    return [ui.notice("exploratory", null, paths.notice || core.text.pathwaysNotice),
      chosenDest.length ? h("ul", { class: "b-dests" }, chosenDest.slice().sort(byTitle).map(item)) : h("p", T.noDest)];
  }
  const pathsSection = ui.section("paths", T.s.paths, [pathsBody]);

  // ---------------------------------------------------------------- how it's changing
  const changing = (() => {
    const sigs = role.signals || [];
    const parts = [];
    if (sigs.length) {
      const allWatch = sigs.every((x) => x.status === "watch");
      parts.push(h("p", allWatch ? T.allWatch(sigs.length) : T.notAllWatch));
      const fam = (f) => String(core.labels?.signalFamily?.[f] || f).split(/ \(|;|\. /)[0].replace(/\.$/, "");
      parts.push(ui.disclosure(T.signalsTitle(sigs.length), [h("p", { class: "meta" }, T.watchWhy), h("ul", { class: "b-plain b-signals" }, sigs.map((x) => h("li",
        h("p", { class: "b-signal__title" }, ui.jargon(clean(x.title), rest)),
        h("p", { class: "meta" }, fam(x.family), x.sg ? ` · Source grade ${x.sg}: ${(COPY.sourceGrade?.[x.sg] || x.sgTxt || "").replace(/\.$/, "")}` : "",
          x.reviewBy ? ` · ${T.reviewBy} ${dateLong(x.reviewBy)}` : ""))))]));
    } else parts.push(h("p", "No signal yet. ", sentence(String(core.text.noSignal || "").replace(/^"No signal yet" is /, "That is "))));
    const emerg = [...new Set(variants.flatMap((v) => v.chg?.emerging || []))].map((s) => compBy.get(s)).filter(Boolean);
    if (emerg.length) {
      const byLc = new Map();
      for (const c of emerg) { const k = c.lc || "watch"; if (!byLc.has(k)) byLc.set(k, []); byLc.get(k).push(c); }
      parts.push(ui.disclosure(T.emergingTitle(emerg.length), [...byLc].map(([lc, cs]) => frag(
        h("p", { class: "b-sub" }, COPY.lifecycle?.[lc]?.label || cap(lc)),
        h("ul", { class: "b-plain" }, cs.map((c) => h("li", h("a", { href: ui.link.comp(c.slug) }, c.title))))))));
    }
    if (role.lc && role.lc !== "established" && (role.reviewBy || role.counterSignal)) {
      parts.push(h("h3", { class: "h4" }, T.roleWatch), h("dl", { class: "facts" },
        role.reviewBy ? [h("dt", T.reviewBy), h("dd", dateLong(role.reviewBy))] : null,
        role.counterSignal ? [h("dt", T.counter), h("dd", ui.jargon(role.counterSignal, rest))] : null));
    }
    parts.push(h("p", h("a", { href: "#/changing" }, T.seeChanging)));
    return ui.section("changing", T.s.changing, parts);
  })();

  // ---------------------------------------------------------------- about this record, exports
  const exportStatus = h("p", { class: "meta b-export-status", role: "status", "aria-live": "polite" });
  function tasksText() {
    const v = st.variant;
    const list = st.ordered;
    const { head: top, foot } = exportFrame(core, `${role.title}: tasks`);
    const lines = [...top, "", `Role: ${role.title}`];
    if (v) lines.push(`Employer type: ${variantName(v, isDup(v))}`, `Link to this version: ${variantUrl(v)}`);
    if (st.level !== "all") lines.push(`Role level: ${cap(st.level)}`);
    lines.push("", `Tasks (${list.length}):`);
    list.forEach((x, i) => {
      const p = primaryOf(x.t);
      const tags = [x.formation ? (COPY.formation?.tag || "Formation task").toLowerCase() : null, x.added ? `added for ${ADJ[v.actor] || v.actor} roles` : null].filter(Boolean);
      lines.push(`${i + 1}. ${x.t.stmt}${tags.length ? ` (${tags.join("; ")})` : ""}`);
      if (p) lines.push(`   Competency: ${p.title}`);
    });
    if (list.some((x) => x.formation)) lines.push("", `${COPY.formation?.tag || "Formation task"}: ${COPY.formation?.explain || ""}`);
    const chg = v?.chg;
    if (chg) lines.push("", `${COPY.pending?.title || "Assessment pending"}: ${fmt(chg.nAssessed)} of ${fmt(chg.nTasks)} tasks assessed. ${COPY.pending?.why || ""}`);
    if (v?.hr) lines.push("", ...core.text.hrDisclaimer);
    lines.push("", ...foot);
    return lines.join("\n");
  }
  function csvText() {
    const v = st.variant;
    const src = variantUrl(v);
    const useCell = (t) => { const u = COPY.use?.[t] || {}; return u.short ? `${u.label}: ${u.short}` : t; };
    const reviewCell = (r) => `Drafted by AI agents; ${String(COPY.review?.[r || "unreviewed"]?.label || "not yet reviewed by people").toLowerCase()}`;
    const evCell = (l) => (l ? `${l}: ${COPY.evidence?.[l]?.label || ""}` : "");
    const rows = [["record_id", "kind", "text", "competency", "role_levels", "formation", "use_tier", "evidence_label", "review_status", "release", "source_page", "notes"]];
    for (const x of itemsFor(v)) {
      const t = x.t, p = primaryOf(t);
      rows.push([recordId(t.module, t.slug), "task", t.stmt, p ? p.title : "", x.roleLevels, x.formation ? "yes" : "no", useCell(t.tier?.t || role.tier?.t), evCell(t.ev?.l), reviewCell(t.ev?.r), core.release.id, src, T.notes]);
    }
    for (const t of targets) {
      const c = compBy.get(t.slug);
      rows.push([c?.id || recordId(t.module, t.slug), "competency_target", t.title, t.title, levels.filter((l) => t.levels?.[l.key]).map((l) => `${l.key}: ${t.levels[l.key]}`), "", useCell(t.tier?.t), evCell(c?.ev?.l), reviewCell(c?.ev?.r), core.release.id, src, T.notes]);
    }
    return toCsv(rows);
  }
  async function onCopy() { const ok = await copyText(tasksText()); exportStatus.textContent = ok ? T.copied : T.copyFail; setTimeout(() => { exportStatus.textContent = ""; }, 4000); }
  function onCsv() {
    download(`emst-${safeName(role.title)}-${st.variant ? keyOf(st.variant) : "role"}-${core.release.id}.csv`, csvText(), "text/csv");
    exportStatus.textContent = T.saved; setTimeout(() => { exportStatus.textContent = ""; }, 4000);
  }
  const about = ui.section("about", T.s.about, [
    aboutParts(ui.aboutRecord(role, core, { title: role.title, kind: "Role profile", exports: [
      { label: COPY.actions?.copyTasks || "Copy tasks as text", icon: "copy", onClick: onCopy },
      { label: COPY.actions?.csv || "Download CSV", icon: "download", onClick: onCsv }] })),
    exportStatus]);

  // ---------------------------------------------------------------- assemble
  const sections = [
    { id: "tasks", title: T.s.tasks }, { id: "competencies", title: T.s.competencies },
    employers ? { id: "employers", title: T.s.employers } : null,
    { id: "connections", title: T.s.connections }, { id: "paths", title: T.s.paths },
    { id: "changing", title: T.s.changing }, { id: "about", title: T.s.about }].filter(Boolean);
  const title = actorParam && chosen ? `${role.title} (${variantName(chosen, isDup(chosen))})` : role.title;
  const layout = ui.withMargin(sections, [work.node, comps, employers, connections, pathsSection, changing, about]);
  compactToc(layout);
  const node = h("div", { class: "b-role" },
    h("div", { id: "overview", class: "b-overview" }, head),
    ui.printMeta(core, role.title),
    layout);
  return { title, node };
}

// ------------------------------------------------------------------ P3: on watch, shown in full only under What's changing
function watchPage(core, role) {
  const seen = new Set();
  const crumbs = [{ href: "#/changing", text: "What's changing" }, { text: role.title }];
  const head = ui.pageHeader({ crumbs, kind: T.wcKind, id: role.id, title: role.title, alt: role.alt, lede: ui.jargon(role.fn || "", seen),
    status: ui.statusLine(role, { aboutHref: "#about" }) });
  const facts = [];
  const fact = (k, v) => { if (v) facts.push(h("dt", k), h("dd", v)); };
  fact(T.horizon, role.horizon ? horizonWords(role.horizon) : null);
  fact(T.reviewBy, role.reviewBy ? dateLong(role.reviewBy) : null);
  fact(T.counter, role.counterSignal ? ui.jargon(role.counterSignal, seen) : null);
  fact(T.sectors, (role.sectors || []).length ? cap(joinAnd(role.sectors.map((s) => cleanLabel(s.actorLabel).toLowerCase()))) : null);
  fact(T.signals, role.nSignals !== undefined ? `${fmt(role.nSignals)} (all listed under What's changing)` : null);
  fact(T.feeders, (role.feeders || []).filter((f) => !f.wc).length ? role.feeders.filter((f) => !f.wc).map((f, i) => [i ? "; " : "", h("a", { href: ui.link.role(f.slug) }, f.title)]) : null);
  const body = h("div", { class: "b-watch stack-lg" },
    ui.notice("caution", T.wcTitle, h("p", T.wcBody), h("p", h("a", { class: "btn btn--primary", href: "#/changing" }, icon("signal"), T.wcLink))),
    role.def && role.def !== role.fn ? h("p", ui.jargon(role.def, seen)) : null,
    facts.length ? h("dl", { class: "facts" }, facts) : null,
    ui.section("about", T.s.about, [aboutParts(ui.aboutRecord(role, core, { title: role.title, kind: "Emerging role (on watch)" }))]));
  return { title: role.title, node: h("div", { class: "b-role" }, head, ui.printMeta(core, role.title), h("div", { class: "page-body" }, body)) };
}
