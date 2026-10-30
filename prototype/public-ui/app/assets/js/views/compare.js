// Compare two roles (#/compare, #/compare/:a, #/compare/:a/:b). DESIGN_SPEC §2.8, DESIGN_SYSTEM §7.18. Developer C.
// Never a percentage, a score or "you qualify". Licence: Apache-2.0.
import { h, frag, icon } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { NotFound } from "../lib/data.js";
import * as ui from "../ui.js";
import { COPY, fill } from "../content.js";
import { fmt } from "../lib/format.js";
import { plain, levelRank, roleLevelLabel, credSlug, svg, plural, draftNote, hrNotice } from "./misc.js";

// Choices made in the selects before the user follows the link. In memory only (never storage, never the URL).
const chosen = { a: "", b: "" };

const byTitle = (x, y) => String(x.title).localeCompare(String(y.title));

/** Highest target level a role profile sets for a competency, across all its role levels. */
function topLevel(t) {
  let best = null;
  for (const v of Object.values(t.levels || {})) if (levelRank(v) > levelRank(best)) best = v;
  return best;
}

function chooser(core, roles, a, b) {
  const bySlug = new Map(roles.map((r) => [r.slug, r]));
  const fams = core.jobFamilies.map((f) => ({ title: f.title, roles: (f.roles || []).map((m) => bySlug.get(m.slug)).filter(Boolean).sort(byTitle) }))
    .filter((f) => f.roles.length).sort(byTitle);
  const inFam = new Set(fams.flatMap((f) => f.roles.map((r) => r.slug)));
  const other = roles.filter((r) => !inFam.has(r.slug)).sort(byTitle);

  const makeSelect = (id) => {
    const sel = h("select", { id, class: "c-select", "aria-describedby": `${id}-hint` }, h("option", { value: "" }, "Choose a role"),
      fams.map((f) => h("optgroup", { label: f.title }, f.roles.map((r) => h("option", { value: r.slug }, r.title)))),
      other.length ? h("optgroup", { label: "Other roles" }, other.map((r) => h("option", { value: r.slug }, r.title))) : null);
    return sel;
  };
  const selA = makeSelect("cmp-a"), selB = makeSelect("cmp-b");
  selA.value = a || chosen.a || "";
  selB.value = b || chosen.b || "";
  const go = h("a", { class: "btn btn--primary", href: "#/compare" }, icon("compare"), "Compare these roles");
  const swap = h("a", { class: "btn btn--tertiary", href: "#/compare" }, "Swap the two roles");
  const status = h("p", { class: "meta c-choose__status", role: "status", "aria-live": "polite" });

  const update = (announce) => {
    chosen.a = selA.value; chosen.b = selB.value;
    const A = bySlug.get(selA.value), B = bySlug.get(selB.value);
    go.setAttribute("href", A && B ? ui.link.compare(A.slug, B.slug) : A ? ui.link.compare(A.slug) : "#/compare");
    swap.hidden = !(A && B);
    if (A && B) swap.setAttribute("href", ui.link.compare(B.slug, A.slug));
    const msg = A && B ? (A.slug === B.slug ? "You chose the same role twice. Choose two different roles." : `Ready to compare ${A.title} with ${B.title}. Select “Compare these roles”.`)
      : A || B ? "Choose the other role too." : "Choose two roles, then select “Compare these roles”.";
    if (announce) status.textContent = msg;
  };
  selA.addEventListener("change", () => update(true));
  selB.addEventListener("change", () => update(true));
  update(false);

  return h("div", { class: "panel c-choose" },
    h("div", { class: "c-choose__fields" },
      h("div", { class: "c-field" }, h("label", { class: "c-field__label", for: "cmp-a" }, "First role"),
        h("p", { class: "meta", id: "cmp-a-hint" }, "For example, the role you have now."), selA),
      h("div", { class: "c-field" }, h("label", { class: "c-field__label", for: "cmp-b" }, "Second role"),
        h("p", { class: "meta", id: "cmp-b-hint" }, "The summary counts what this role needs."), selB)),
    h("div", { class: "btn-row" }, go, swap),
    status,
    h("p", { class: "meta" }, "Roles are grouped by job family. A role can appear in more than one family. Only roles with a full or starter profile are listed; emerging roles are on What's changing."));
}

function roleCard(role, which) {
  return h("div", { class: ["compare__role", which === "b" && "compare__role--b"] },
    h("span", { class: ["key", which === "b" && "key--b"], "aria-hidden": "true" }),
    h("div", h("p", { class: "meta" }, which === "a" ? "First role" : "Second role"),
      h("h3", { class: "h4" }, h("a", { href: ui.link.role(role.slug) }, role.title)),
      h("p", { class: "meta" }, `${plural(role.targets.length, "competency", "competencies")} · ${plural(role.tasks.length, "task")}`)));
}

function overlapFigure(A, B, onlyA, shared, onlyB) {
  const union = onlyA + shared + onlyB;
  const seg = (cls, x, w) => (w > 0 ? svg("rect", { class: `overlap__seg ${cls}`, x, y: 0, width: w, height: 1 }) : null);
  const bar = svg("svg", { class: "overlap__bar", viewBox: `0 0 ${Math.max(union, 1)} 1`, preserveAspectRatio: "none", "aria-hidden": "true", focusable: "false" },
    seg("overlap__seg--a", 0, onlyA), seg("overlap__seg--shared", onlyA, shared), seg("overlap__seg--b", onlyA + shared, onlyB));
  const are = (n) => (n === 1 ? "is" : "are");
  return h("figure", { class: "overlap" },
    h("figcaption", { class: "overlap__caption" }, "How their competencies overlap"),
    bar,
    h("ul", { class: "overlap__legend" },
      h("li", h("span", { class: "key", "aria-hidden": "true" }), h("span", `Only ${A.title}: `, h("strong", { class: "num" }, fmt(onlyA)))),
      h("li", h("span", { class: "key key--shared", "aria-hidden": "true" }), h("span", "Shared: ", h("strong", { class: "num" }, fmt(shared)))),
      h("li", h("span", { class: "key key--b", "aria-hidden": "true" }), h("span", `Only ${B.title}: `, h("strong", { class: "num" }, fmt(onlyB))))),
    h("p", { class: "overlap__text" }, `${fmt(shared)} of the ${fmt(union)} competencies across both roles ${are(shared)} shared. ${fmt(onlyA)} ${are(onlyA)} only in ${A.title}, and ${fmt(onlyB)} ${are(onlyB)} only in ${B.title}.`));
}

function compLists(A, B, mapA, mapB, core) {
  const sharedRows = [...mapB.keys()].filter((k) => mapA.has(k)).map((k) => ({ t: mapB.get(k), la: topLevel(mapA.get(k)), lb: topLevel(mapB.get(k)) }))
    .sort((x, y) => (levelRank(y.lb) - levelRank(y.la)) - (levelRank(x.lb) - levelRank(x.la)) || byTitle(x.t, y.t));
  const onlyA = [...mapA.values()].filter((t) => !mapB.has(t.slug)).sort(byTitle);
  const onlyB = [...mapB.values()].filter((t) => !mapA.has(t.slug)).sort(byTitle);
  const item = (t, ...rest) => h("li", h("a", { href: ui.link.comp(t.slug) }, t.title), h("p", { class: "c-lv" }, ...rest));
  const col = (id, keyCls, label, rows) => h("section", { class: "compare__col", "aria-labelledby": id },
    h("h4", { id }, h("span", { class: ["key", keyCls], "aria-hidden": "true" }), label, h("span", { class: "count" }, fmt(rows.length))),
    rows.length ? h("ul", rows) : h("p", { class: "meta" }, "None."));
  return h("div", { class: "compare__lists" },
    col("cmp-only-a", null, fill(COPY.compare.onlyA, { a: A.title }), onlyA.map((t) => item(t, ui.levelChip(topLevel(t), core)))),
    col("cmp-shared", "key--shared", COPY.compare.shared, sharedRows.map((r) => item(r.t,
      h("span", { class: "vh" }, `${A.title}: `), ui.levelChip(r.la, core),
      h("span", { class: "c-lv__arrow", "aria-hidden": "true" }, "→"),
      h("span", { class: "vh" }, `; ${B.title}: `), ui.levelChip(r.lb, core),
      levelRank(r.lb) > levelRank(r.la) ? h("span", { class: "c-lv__note" }, `Higher in ${B.title}`) : null))),
    col("cmp-only-b", "key--b", fill(COPY.compare.onlyB, { b: B.title }), onlyB.map((t) => item(t, ui.levelChip(topLevel(t), core)))));
}

function whatToCheck(A, B, paths, core) {
  const out = [];
  const vB = new Set((B.variants || []).map((v) => v.slug));
  const showHr = (B.hrSeries || []).length || (B.hrClasses || []).length || (B.variants || []).some((v) => v.hr);
  if (showHr) out.push(hrNotice(core.text.hrDisclaimer));

  // Credentials that may be involved, from role B's employer variants.
  const creds = new Map();
  for (const v of B.variants || []) for (const g of v.credentialGates || []) {
    if (!creds.has(g.title)) creds.set(g.title, []);
    creds.get(g.title).push(v.actorLabel);
  }
  const pending = (B.variants || []).some((v) => v.credentialGatesPending);
  out.push(h("h3", { class: "h4" }, "Credentials that may be involved"));
  if (creds.size) out.push(h("p", `Some employers may look for these for ${B.title}. They are AI-drafted links, not requirements.`),
    h("ul", { class: "task-list" }, [...creds].map(([title, actors]) => h("li", h("a", { href: `#/credential/${credSlug(title)}` }, title),
      h("p", { class: "task-list__meta" }, `May be involved (AI-drafted link) · ${actors.join(", ")}`)))));
  else out.push(h("p", `No credential is shown for ${B.title} yet.`));
  if (pending) out.push(h("p", { class: "meta" }, "Some credentials linked to this role are not shown until their issuer is checked against a source."));

  // OPM series and state or local classes linked to role B.
  const series = B.hrSeries || [], classes = B.hrClasses || [];
  out.push(h("h3", { class: "h4" }, "Federal job series and state or local job classes"));
  if (series.length || classes.length) {
    out.push(h("ul", { class: "task-list" },
      series.map((s) => {
        const rec = core.series.find((x) => x.code === s.code);
        return h("li", h("a", { href: ui.link.series(s.code) }, `OPM series ${s.code} ${s.title}`),
          h("p", { class: "task-list__meta" }, [s.close ? COPY.match.closeMatch : "Covered by a generated series profile", COPY.match.unreviewed, rec?.realignment ? core.text.realignment : null].filter(Boolean).join(" · ")));
      }),
      classes.map((c) => h("li", h("a", { href: ui.link.cls(c.slug) }, `${c.title} (${c.jur})`),
        h("p", { class: "task-list__meta" }, [c.close ? COPY.match.closeMatch : "Related in part", COPY.match.unreviewed].join(" · "))))));
  } else out.push(h("p", `EMST has no federal series or state class linked to ${B.title} yet.`));

  // Friction notes for moves between employer types, where either end is a variant of role B.
  const label = (slug, fallback) => { const v = paths.variants?.[slug]; return v ? `${v.title} (${v.actorLabel})` : fallback; };
  const tr = (paths.translations || []).filter((t) => t.fr && (vB.has(t.from) || vB.has(t.to)));
  if (tr.length) {
    out.push(h("h3", { class: "h4" }, "Moving between employers"));
    out.push(h("p", `AI agents noted what tends to change when people move between kinds of employer in or near ${B.title}.`));
    out.push(h("ul", { class: "c-fric" }, tr.map((t) => h("li",
      h("p", { class: "c-fric__title" }, `${label(t.from, plain(t.fromLabel || "Another role"))} to ${label(t.to, "a related job outside EMST's role list")}`),
      h("dl", { class: "facts" },
        t.fr.posture ? [h("dt", "What changes"), h("dd", plain(t.fr.posture))] : null,
        t.fr.licensure ? [h("dt", "Licenses or certificates mentioned"), h("dd", plain(t.fr.licensure), h("span", { class: "meta" }, " (may be involved)"))] : null,
        t.fr.pay ? [h("dt", "Pay"), h("dd", plain(t.fr.pay))] : null)))));
    out.push(draftNote(COPY.match.unreviewed + "."));
  }
  return out;
}

function edgeBlock(A, B, paths, mapA, mapB, core) {
  const vA = new Set((A.variants || []).map((v) => v.slug)), vB = new Set((B.variants || []).map((v) => v.slug));
  const edges = (paths.edges || []).filter((e) => vA.has(e.from) && vB.has(e.to));
  const actor = (slug) => paths.variants?.[slug]?.actorLabel || slug;
  if (!edges.length) {
    const back = (paths.edges || []).some((e) => vB.has(e.from) && vA.has(e.to));
    return [h("p", COPY.compare.noEdge),
      back ? h("p", "EMST has worked out a path the other way, from ", B.title, " to ", A.title, ". ", h("a", { href: ui.link.compare(B.slug, A.slug) }, "Compare them in that order")) : null];
  }
  // Group variant pairs that give the same statement and gap list.
  const groups = new Map();
  for (const e of edges) {
    const key = `${e.statement}|${e.fromLevel}|${e.toLevel}|${(e.gap || []).map((g) => `${g.slug}:${g.fromLevel || ""}:${g.toLevel}`).join(",")}`;
    if (!groups.has(key)) groups.set(key, { e, from: new Set(), to: new Set() });
    groups.get(key).from.add(e.from); groups.get(key).to.add(e.to);
  }
  const titleOf = (slug) => mapB.get(slug)?.title || mapA.get(slug)?.title || core.comps.find((c) => c.slug === slug)?.title || "Competency";
  const ORDER = ["federal", "state", "local", "ngo", "private", "academic"];
  const who = (set, role) => {
    if (set.size >= (role.variants || []).length) return "all its employer types";
    return [...set].sort((x, y) => ORDER.indexOf(paths.variants?.[x]?.actor) - ORDER.indexOf(paths.variants?.[y]?.actor)).map(actor).join(", ");
  };
  return [...groups.values()].map(({ e, from, to }) => h("div", { class: "c-edge" },
    h("p", h("strong", `From ${A.title} (${who(from, A)}) to ${B.title} (${who(to, B)})`)),
    h("p", `${A.title} ${plain(e.statement)}.`),
    h("p", { class: "meta" }, `This compares ${A.title} at its ${roleLevelLabel(e.fromLevel).toLowerCase()} level with ${B.title} at its ${roleLevelLabel(e.toLevel).toLowerCase()} level.`),
    e.gap?.length ? [h("h4", { class: "c-edge__h" }, `Gaps (${fmt(e.gap.length)})`),
      h("p", { class: "meta" }, `Competencies ${B.title} needs at a higher level than ${A.title} targets, or that ${A.title} does not target.`),
      h("ul", { class: "task-list" }, e.gap.map((g) => h("li", h("a", { href: ui.link.comp(g.slug) }, titleOf(g.slug)),
        h("p", { class: "c-lv" }, g.fromLevel ? [h("span", { class: "vh" }, "From "), ui.levelChip(g.fromLevel, core), h("span", { class: "c-lv__arrow", "aria-hidden": "true" }, "→"), h("span", { class: "vh" }, " to ")]
          : h("span", { class: "meta" }, "Not targeted in the first role, needed at "), ui.levelChip(g.toLevel, core)))))] : null));
}

export async function render({ params }) {
  const core = await data.core();
  const roles = core.roles.filter((r) => !r.whatsComingOnly);
  const ok = new Set(roles.map((r) => r.slug));
  for (const s of [params.a, params.b]) if (s && !ok.has(s)) throw new NotFound(`No role "${s}" to compare`);
  const a = params.a || "", b = params.b || "";
  if (a) chosen.a = a;
  if (b) chosen.b = b;

  const header = ui.pageHeader({
    crumbs: [{ href: "#/", text: "Home" }, { text: "Compare roles" }],
    kind: "Exploratory comparison",
    title: "Compare roles",
    lede: "See which competencies and tasks two roles share, how their target levels differ, and what to check with an employer.",
  });
  const choose = ui.section("choose", "Choose two roles", chooser(core, roles, a, b));

  if (!a || !b || a === b) {
    const hint = a && b ? ui.notice("info", "Choose two different roles", "You chose the same role twice.") : null;
    return { title: "Compare roles", node: frag(header, h("div", { class: "page-body c-single" }, hint, choose)) };
  }

  const [A, B, paths] = await Promise.all([data.role(a), data.role(b), data.paths()]);
  const mapA = new Map((A.targets || []).map((t) => [t.slug, t]));
  const mapB = new Map((B.targets || []).map((t) => [t.slug, t]));
  const shared = [...mapB.keys()].filter((k) => mapA.has(k)).length;
  const onlyA = mapA.size - shared, onlyB = mapB.size - shared;
  const tasksA = new Set((A.tasks || []).map((t) => t.slug));
  const sharedTasks = (B.tasks || []).filter((t) => tasksA.has(t.slug));

  const results = [
    ui.notice("exploratory", COPY.compare.caveat, paths.notice),
    ui.section("overview", "Overview", [
      h("p", { class: "lede c-summary" }, fill(COPY.compare.summary, { a: A.title, b: B.title, shared: fmt(shared), total: fmt(mapB.size), tasks: fmt(sharedTasks.length) })),
      h("div", { class: "compare" },
        h("div", { class: "compare__roles" }, roleCard(A, "a"), roleCard(B, "b")),
        overlapFigure(A, B, onlyA, shared, onlyB)),
    ]),
    ui.section("competencies", "Competencies", [
      h("p", { class: "meta" }, "Each level shown is the highest target level that role's profile sets for the competency, across all its role levels (for example entry to lead). ", core.text.targetsNote),
      compLists(A, B, mapA, mapB, core),
    ]),
    ui.section("tasks", "Tasks in both roles", [
      h("p", `${A.title} has ${plural(tasksA.size, "task")}. ${B.title} has ${plural((B.tasks || []).length, "task")}. They share ${plural(sharedTasks.length, "task")}.`),
      sharedTasks.length ? h("ul", { class: "task-list" }, sharedTasks.map((t) => h("li", h("a", { href: ui.link.task(t.slug) }, t.stmt)))) : null,
    ], { meta: plural(sharedTasks.length, "task") }),
    ui.section("check", COPY.compare.check, whatToCheck(A, B, paths, core)),
    ui.section("path", "Computed path between these roles", [
      h("p", { class: "meta" }, "Exploratory. A computed path compares draft target levels. It is not a career path anyone has taken, and it is not advice to take it."),
      ...edgeBlock(A, B, paths, mapA, mapB, core),
    ]),
  ];

  const node = frag(
    ui.printMeta(core, `Compare ${A.title} and ${B.title}`),
    header,
    h("div", { class: "page-body c-single" }, choose, results));
  return { title: "Compare roles", node };
}
