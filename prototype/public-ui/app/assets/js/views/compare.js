// Compare two roles (#/compare, #/compare/:a, #/compare/:a/:b). DESIGN_SPEC §2.8, DESIGN_SYSTEM §7.18. Developer C.
// Never a percentage, a score or "you qualify". Licence: Apache-2.0.
import { h, frag, icon, nextId } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { NotFound } from "../lib/data.js";
import * as ui from "../ui.js";
import { COPY, fill } from "../content.js";
import { fmt } from "../lib/format.js";
import { plain, levelRank, roleLevelLabel, ROLE_LEVELS, credSlug, svg, plural, draftNote, hrNotice } from "./misc.js";

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
        h("p", { class: "meta", id: "cmp-b-hint" }, "The summary counts the competencies in this role's draft profile."), selB)),
    h("div", { class: "btn-row" }, go, swap),
    status,
    h("p", { class: "meta" }, "Roles are grouped by job family. A role can appear in more than one family. Only roles with a full or starter profile are listed; emerging roles are on What's changing."));
}

/** The colour key for a role. Role B's key carries the same SVG hatch as its bar segment, so A and B differ by
 *  pattern as well as colour (accessibility review, round 2). */
function key(which, hatchId) {
  if (which !== "b") return h("span", { class: ["key", which === "shared" && "key--shared"], "aria-hidden": "true" });
  return svg("svg", { class: "key key--b c-key", viewBox: "0 0 14 14", "aria-hidden": "true", focusable: "false" },
    svg("rect", { class: "c-hatch-over", width: 14, height: 14, fill: `url(#${hatchId})` }));
}
function hatchDefs(id) {
  return svg("svg", { class: "c-defs", width: 0, height: 0, "aria-hidden": "true", focusable: "false" },
    svg("defs", {}, svg("pattern", { id, patternUnits: "userSpaceOnUse", width: 6, height: 6, patternTransform: "rotate(45)" },
      svg("rect", { class: "c-hatch__line", x: 0, y: 0, width: 2, height: 6 }))));
}

function roleCard(role, which, hatchId) {
  return h("div", { class: ["compare__role", which === "b" && "compare__role--b"] },
    key(which, hatchId),
    h("div", h("p", { class: "meta" }, which === "a" ? "First role" : "Second role"),
      h("h3", { class: "h4" }, h("a", { href: ui.link.role(role.slug) }, role.title)),
      h("p", { class: "meta" }, `${plural(role.targets.length, "competency", "competencies")} · ${plural(role.tasks.length, "task")}`)));
}

function overlapFigure(A, B, onlyA, shared, onlyB, hatchId) {
  const union = Math.max(onlyA + shared + onlyB, 1);
  const pc = (n) => `${(n / union) * 100}%`;
  // Percentages keep the drawing in screen pixels, so the hatch is not stretched (no preserveAspectRatio="none").
  const seg = (cls, x, w) => (w > 0 ? svg("rect", { class: `overlap__seg ${cls}`, x: pc(x), y: 0, width: pc(w), height: "100%" }) : null);
  const bar = svg("svg", { class: "overlap__bar", "aria-hidden": "true", focusable: "false" },
    seg("overlap__seg--a", 0, onlyA), seg("overlap__seg--shared", onlyA, shared), seg("overlap__seg--b", onlyA + shared, onlyB),
    onlyB > 0 ? svg("rect", { class: "c-hatch-over", x: pc(onlyA + shared), y: 0, width: pc(onlyB), height: "100%", fill: `url(#${hatchId})` }) : null);
  const are = (n) => (n === 1 ? "is" : "are");
  return h("figure", { class: "overlap" },
    h("figcaption", { class: "overlap__caption" }, "How their competencies overlap"),
    bar,
    h("ul", { class: "overlap__legend" },
      h("li", key("a"), h("span", `Only ${A.title}: `, h("strong", { class: "num" }, fmt(onlyA)))),
      h("li", key("shared"), h("span", "Shared: ", h("strong", { class: "num" }, fmt(shared)))),
      h("li", key("b", hatchId), h("span", `Only ${B.title} (hatched): `, h("strong", { class: "num" }, fmt(onlyB))))),
    h("p", { class: "overlap__text" }, `${fmt(shared)} of the ${fmt(onlyA + shared + onlyB)} competencies across both roles ${are(shared)} shared. ${fmt(onlyA)} ${are(onlyA)} only in ${A.title}, and ${fmt(onlyB)} ${are(onlyB)} only in ${B.title}.`));
}

function compLists(A, B, mapA, mapB, core, hatchId) {
  const sharedRows = [...mapB.keys()].filter((k) => mapA.has(k)).map((k) => ({ t: mapB.get(k), la: topLevel(mapA.get(k)), lb: topLevel(mapB.get(k)) }))
    .sort((x, y) => (levelRank(y.lb) - levelRank(y.la)) - (levelRank(x.lb) - levelRank(x.la)) || byTitle(x.t, y.t));
  const onlyA = [...mapA.values()].filter((t) => !mapB.has(t.slug)).sort(byTitle);
  const onlyB = [...mapB.values()].filter((t) => !mapA.has(t.slug)).sort(byTitle);
  const item = (t, ...rest) => h("li", h("a", { href: ui.link.comp(t.slug) }, t.title), h("p", { class: "c-lv" }, ...rest));
  // Column headings are h3 under the section's h2 (accessibility review: never h4 straight after h2).
  const col = (id, which, label, rows) => h("section", { class: "compare__col", "aria-labelledby": id },
    h("h3", { class: "h4 c-col__h", id }, key(which, hatchId), label, h("span", { class: "count" }, fmt(rows.length))),
    rows.length ? h("ul", rows) : h("p", { class: "meta" }, "None."));
  return h("div", { class: "compare__lists" },
    col("cmp-only-a", "a", fill(COPY.compare.onlyA, { a: A.title }), onlyA.map((t) => item(t, ui.levelChip(topLevel(t), core)))),
    col("cmp-shared", "shared", COPY.compare.shared, sharedRows.map((r) => item(r.t,
      h("span", { class: "vh" }, `${A.title}: `), ui.levelChip(r.la, core),
      h("span", { class: "c-lv__arrow", "aria-hidden": "true" }, "→"),
      h("span", { class: "vh" }, `; ${B.title}: `), ui.levelChip(r.lb, core),
      levelRank(r.lb) > levelRank(r.la) ? h("span", { class: "c-lv__note" }, `Higher in ${B.title}`) : null))),
    col("cmp-only-b", "b", fill(COPY.compare.onlyB, { b: B.title }), onlyB.map((t) => item(t, ui.levelChip(topLevel(t), core)))));
}

/** Friction text sits under "may be involved", so it must not also say "required" (trust review O8). Display only:
 *  "none required, CEP valued" → "no license named; CEP valued"; "licence where required" → "licence in some places";
 *  "design work requires PE licensure" → "PE licensure for design work". */
function mayBeInvolved(text) {
  return plain(text)
    .replace(/^none required\b,?\s*/i, "no license named; ")
    .replace(/\bwhere required\b/gi, "in some places")
    .replace(/^([a-z][\w\s-]*?) requires ([^,(;]+)/i, (_, who, what) => `${what.trim()} for ${who.trim()}${/\s$/.test(what) ? " " : ""}`)
    .replace(/\s*\brequired\b/gi, "")
    .replace(/\s+([,;.])/g, "$1").replace(/;\s*$/, "").trim();
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
        return h("li", h("a", { href: ui.link.series(s.code) }, `Federal job series ${s.code} ${s.title}`),
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
        t.fr.licensure ? [h("dt", "Licenses or credentials that may be involved"), h("dd", mayBeInvolved(t.fr.licensure))] : null,
        t.fr.pay ? [h("dt", "Pay"), h("dd", plain(t.fr.pay))] : null)))));
    out.push(draftNote(COPY.match.unreviewed + "."));
  }
  return out;
}

const ORD = ROLE_LEVELS;
const lvl = (k) => roleLevelLabel(k).toLowerCase();
const topLevelOf = (role) => (role.levels || []).map((l) => l.key).sort((x, y) => ORD.indexOf(y) - ORD.indexOf(x))[0];

function edgeBlock(A, B, paths, mapA, mapB, core, summary) {
  const vA = new Set((A.variants || []).map((v) => v.slug)), vB = new Set((B.variants || []).map((v) => v.slug));
  const edges = (paths.edges || []).filter((e) => vA.has(e.from) && vB.has(e.to));
  const actor = (slug) => paths.variants?.[slug]?.actorLabel || slug;
  if (!edges.length) {
    const back = (paths.edges || []).some((e) => vB.has(e.from) && vA.has(e.to));
    return [h("p", COPY.compare.noEdge),
      back ? h("p", "EMST has worked out a path the other way, from ", B.title, " to ", A.title, ". ", h("a", { href: ui.link.compare(B.slug, A.slug) }, "Compare them in that order")) : null];
  }
  // Group variant pairs that give the same count and gap list. The largest count comes first, as on the role page.
  const groups = new Map();
  for (const e of edges) {
    const key = `${e.shared?.N}|${e.shared?.M}|${e.fromLevel}|${e.toLevel}|${(e.gap || []).map((g) => `${g.slug}:${g.fromLevel || ""}:${g.toLevel}`).join(",")}`;
    if (!groups.has(key)) groups.set(key, { e, from: new Set(), to: new Set() });
    groups.get(key).from.add(e.from); groups.get(key).to.add(e.to);
  }
  const list = [...groups.values()].sort((x, y) => (y.e.shared?.N || 0) - (x.e.shared?.N || 0));
  const titleOf = (slug) => mapB.get(slug)?.title || mapA.get(slug)?.title || core.comps.find((c) => c.slug === slug)?.title || "Competency";
  const ORDER = ["federal", "state", "local", "ngo", "private", "academic"];
  const who = (set, role) => {
    if (set.size >= (role.variants || []).length) return "any employer type";
    return [...set].sort((x, y) => ORDER.indexOf(paths.variants?.[x]?.actor) - ORDER.indexOf(paths.variants?.[y]?.actor)).map(actor).join(", ");
  };
  // Destinations whose profile tops out below the origin's top level are moves down, not up (trust review O5).
  const bTop = topLevelOf(B);
  const tag = (e) => {
    if (!bTop || ORD.indexOf(bTop) >= ORD.indexOf(e.fromLevel)) return null;
    return h("p", { class: "c-edge__tag" }, h("span", { class: "badge" }, bTop === "entry" ? "Entry-level role" : "Lower-level role"), " ",
      bTop === "entry" ? `${B.title}'s draft profile covers entry level only, below ${A.title}'s ${lvl(e.fromLevel)} level.`
        : `${B.title}'s draft profile stops at ${lvl(bTop)} level, below ${A.title}'s ${lvl(e.fromLevel)} level.`);
  };
  return list.map(({ e, from, to }, i) => {
    const N = e.shared?.N, M = e.shared?.M;
    return h("div", { class: "c-edge" },
      h("h3", { class: "h4 c-edge__title" }, `From ${A.title} (${who(from, A)}) to ${B.title} (${who(to, B)})`),
      tag(e),
      N !== undefined ? h("p", { class: "c-edge__stmt" }, `At ${lvl(e.fromLevel)} level, ${A.title} has ${fmt(N)} of the ${fmt(M)} competencies ${B.title}'s draft profile lists for ${lvl(e.toLevel)} level.`)
        : h("p", `${A.title} ${plain(e.statement)}.`),
      i === 0 && N !== undefined ? h("p", { class: "meta" }, `Why this differs from the ${summary.shared} of ${summary.total} above: that count includes every competency in ${B.title}'s profile at any level. This one uses only the competencies listed for ${B.title}'s ${lvl(e.toLevel)} level, and counts one only if ${A.title}'s ${lvl(e.fromLevel)}-level target is as high or higher.`) : null,
      e.gap?.length ? [h("h4", { class: "c-edge__h" }, `Not yet at that level (${fmt(e.gap.length)})`),
        h("p", { class: "meta" }, `Competencies ${B.title}'s profile lists at a higher level than ${A.title} targets, or that ${A.title} does not target.`),
        h("ul", { class: "task-list" }, e.gap.map((g) => h("li", h("a", { href: ui.link.comp(g.slug) }, titleOf(g.slug)),
          h("p", { class: "c-lv" }, g.fromLevel ? [h("span", { class: "vh" }, "From "), ui.levelChip(g.fromLevel, core), h("span", { class: "c-lv__arrow", "aria-hidden": "true" }, "→"), h("span", { class: "vh" }, " to ")]
            : h("span", { class: "meta" }, `Not targeted in ${A.title}; listed at `), ui.levelChip(g.toLevel, core)))))] : null);
  });
}

export async function render({ params }) {
  const core = await data.core();
  const roles = core.roles.filter((r) => !r.whatsComingOnly);
  const ok = new Set(roles.map((r) => r.slug));
  for (const s of [params.a, params.b]) if (s && !ok.has(s)) throw new NotFound(`No role "${s}" to compare`);
  const a = params.a || "", b = params.b || "";
  if (a) chosen.a = a;
  if (b) chosen.b = b;
  const crumbs = [{ href: "#/", text: "Home" }, { text: "Compare roles" }];
  const lede = "See which competencies and tasks two roles share, how their target levels differ, and what to check with an employer.";
  const choose = ui.section("choose", "Choose two roles", chooser(core, roles, a, b));

  if (!a || !b || a === b) {
    const header = ui.pageHeader({ crumbs, kind: "Exploratory comparison", title: "Compare roles", lede });
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
  const hatchId = nextId("cmp-hatch");
  const title = `Compare ${A.title} and ${B.title}`;

  const header = ui.pageHeader({
    crumbs: [{ href: "#/", text: "Home" }, { href: "#/compare", text: "Compare roles" }, { text: `${A.title} and ${B.title}` }],
    kind: "Exploratory comparison", title, lede,
    // The caveat comes first, before any number (spec §2.8; usability and trust reviews kept it as a strength).
    meta: ui.notice("exploratory", COPY.compare.caveat, paths.notice),
  });
  const results = [
    ui.section("overview", "Overview", [
      // Say what is counted, so the number can be checked against the role page (trust review O5).
      h("p", { class: "lede c-summary" }, `${A.title} and ${B.title} share ${fmt(shared)} of the ${fmt(mapB.size)} competencies in ${B.title}'s draft profile (at any level). Tasks in common: ${fmt(sharedTasks.length)}.`),
      h("div", { class: "compare" },
        hatchDefs(hatchId),
        h("div", { class: "compare__roles" }, roleCard(A, "a", hatchId), roleCard(B, "b", hatchId)),
        overlapFigure(A, B, onlyA, shared, onlyB, hatchId)),
    ]),
    ui.section("competencies", "Competencies", [
      h("p", { class: "meta" }, "Each level shown is the highest target level that role's profile sets for the competency, across all its role levels (for example entry to lead). ", core.text.targetsNote),
      compLists(A, B, mapA, mapB, core, hatchId),
    ]),
    ui.section("tasks", "Tasks in both roles", [
      h("p", `${A.title} has ${plural(tasksA.size, "task")}. ${B.title} has ${plural((B.tasks || []).length, "task")}. They share ${plural(sharedTasks.length, "task")}.`),
      sharedTasks.length ? h("ul", { class: "task-list" }, sharedTasks.map((t) => h("li", h("a", { href: ui.link.task(t.slug) }, t.stmt)))) : null,
    ], { meta: plural(sharedTasks.length, "task") }),
    ui.section("check", COPY.compare.check, whatToCheck(A, B, paths, core)),
    ui.section("path", "Computed path between these roles", [
      h("p", { class: "meta" }, "Exploratory. A computed path compares draft target levels. It is not a career path anyone has taken, and it is not advice to take it."),
      ...edgeBlock(A, B, paths, mapA, mapB, core, { shared: fmt(shared), total: fmt(mapB.size) }),
    ]),
  ];

  const node = frag(
    ui.printMeta(core, title),
    header,
    h("div", { class: "page-body c-single" }, choose, results));
  return { title, node, announce: `Comparing ${A.title} with ${B.title}` };
}
