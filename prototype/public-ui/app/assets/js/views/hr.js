// HR hub, OPM series and state or local class pages (#/hr, #/series, #/series/:code, #/classes, #/class/:slug).
// DESIGN_SPEC §2.10. The HR disclaimer comes first on every series and class page. Developer C. Licence: Apache-2.0.
import { h, frag, icon } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { NotFound } from "../lib/data.js";
import * as ui from "../ui.js";
import { COPY } from "../content.js";
import { fmt, dateLong } from "../lib/format.js";
import { hrNotice, plain, plural, p3Slugs, variantHref, credSlug, humanize, cap, timingWords, ROLE_LEVELS, roleLevelLabel } from "./misc.js";

const HR_CRUMB = { href: "#/hr", text: "For HR and classifiers" };
const JA_WHAT = ["importance", "timeShare", "critical", "neededAtEntry"];
const DEGREE = { "not-required": "Not required", required: "The specification asks for a degree", substitutable: "Experience can take the place of a degree", "agency-set": "Set by the hiring agency" };
const LINK_MEANS = "A link means AI agents found this role's work in jobs of this kind. It is not a classification decision, and EMST claims no match with OPM or state standards. Close links are shown first; other suggestions are in a list you can open.";

const disclaimer = (hr) => hrNotice(hr.disclaimer);

/** Crosswalk rows to roles, split into close links (shown) and other suggestions (in a disclosure). P3 roles are left out. */
function roleLinks(rows, core, noun) {
  const p3 = p3Slugs(core);
  const kept = rows.filter((r) => !p3.has(r.role));
  const nP3 = rows.length - kept.length;
  const title = (r) => core.roles.find((x) => x.slug === r.role)?.title || r.sub || "Role";
  const linkFn = (r) => ({ href: r.v ? variantHref(r.v) : ui.link.role(r.role), text: `${plain(r.sub || title(r))}${r.o?.to && r.o.to !== "all" ? `, for ${plain(r.o.to)}` : ""}` });
  const list = (rs) => ui.crosswalkList(rs.map((r) => ({ ...r, note: r.note ? plain(r.note) : r.note, ver: undefined })), { noun, linkFn }).querySelector(".xw-list");
  const vers = [...new Set(kept.map((r) => r.ver).filter(Boolean))];
  const close = kept.filter((r) => r.close && !r.not);
  const other = kept.filter((r) => !(r.close && !r.not));
  return [
    h("p", LINK_MEANS),
    close.length ? list(close) : h("p", { class: "meta" }, "No role has a close link yet."),
    other.length ? ui.disclosure(`Other suggested links (${fmt(other.length)})`, [h("p", { class: "meta" }, "Links an AI agent drafted that are broader, narrower or related only in part. They are not reviewed."), list(other)]) : null,
    nP3 ? h("p", { class: "meta" }, `${plural(nP3, "more suggested link")} ${nP3 === 1 ? "points" : "point"} to roles that may be forming. Those roles appear only on `, h("a", { href: "#/changing@emerging-roles" }, "What's changing"), ".") : null,
    vers.length ? h("p", { class: "meta" }, `Reference version: ${vers.join("; ")}.`) : null,
    h("p", { class: "meta" }, COPY.match.note),
  ];
}

const closeRoleCount = (rows, p3) => new Set((rows || []).filter((r) => r.close && !r.not && !p3.has(r.role)).map((r) => r.role)).size;

function credList(gates) {
  return h("ul", { class: "task-list" }, gates.map((g) => h("li", h("a", { href: `#/credential/${credSlug(g.title)}` }, g.title), h("p", { class: "task-list__meta" }, "May be involved (AI-drafted link)"))));
}

// ------------------------------------------------------------------ hub
export async function renderHub() {
  const [core, hr] = await Promise.all([data.core(), data.hr()]);
  const d = COPY.use.describe, sel = COPY.use.select;
  const noSelect = !core.useTierTotals?.select;
  const nRealign = core.series.filter((s) => s.realignment).length;
  const node = frag(
    ui.printMeta(core, "For HR and classification staff"),
    ui.pageHeader({
      crumbs: [{ href: "#/", text: "Home" }, { text: HR_CRUMB.text }],
      kind: "Guide for HR staff",
      title: "For HR and classification staff",
      lede: "EMST describes environmental work in plain task language. This page says what HR staff can and can't use it for, then takes you to federal job series and state job classes.",
      meta: disclaimer(hr),
    }),
    h("div", { class: "page-body c-single" },
      ui.section("use", "What you can use EMST for", [
        h("div", { class: "grid-2" },
          h("div", { class: "c-can" }, h("h3", { class: "h4" }, icon("check"), "You can"), h("ul", d.youCan.map((x) => h("li", x)))),
          h("div", { class: "c-cant" }, h("h3", { class: "h4" }, icon("close"), "You can't"), h("ul", d.youCant.map((x) => h("li", x))))),
        h("p", d.why),
        h("p", h("a", { href: ui.link.key("use-tiers") }, "How EMST labels what each record may be used for")),
      ]),
      ui.section("hiring", "AI-drafted content and hiring", [
        h("p", sel.why),
        noSelect ? h("p", sel.notReached) : null,
      ]),
      ui.section("usa-class", "Where EMST fits beside USA Class", [
        h("p", "USA Class is OPM's own tool for drafting federal position descriptions. EMST is not a position description tool, and it does not set series or grade."),
        h("p", "EMST offers reference wording: tasks, competencies and levels, each with its source, date and release. You can copy or print that wording into your own tools. Your HR office must then review it and change it to fit the real job."),
      ]),
      ui.section("browse", "Federal series and state classes", [
        h("ul", { class: "card-list" },
          h("li", ui.card({ kind: "Federal", title: "OPM job series", href: "#/series", summary: "Federal job series that AI agents linked to EMST roles, with any proposed changes flagged.",
            meta: [["Series", fmt(core.series.length)], ["Realignment proposed", fmt(nRealign)], ["With a generated profile", fmt(core.series.filter((s) => s.generated).length)]] })),
          h("li", ui.card({ kind: "State and local", title: "State and local job classes", href: "#/classes", summary: "Job classes from state and local civil-service plans, with links to their official specifications.",
            meta: [["Classes", fmt(core.stateClasses.length)], ["With a class view", fmt(core.stateClasses.filter((c) => c.generated).length)]] }))),
      ])));
  return { title: "For HR and classification staff", node };
}

// ------------------------------------------------------------------ series index
export async function renderSeriesIndex() {
  const [core, hr] = await Promise.all([data.core(), data.hr()]);
  const p3 = p3Slugs(core);
  const rows = hr.series.map((s) => ({ ...s, nCloseRoles: closeRoleCount(s.rows, p3) }));
  const table = ui.table({
    caption: "OPM job series in EMST",
    hint: "Links are AI-suggested and not reviewed.",
    sortBy: "series",
    columns: [
      { key: "series", label: "Series", sort: (r) => r.code, render: (r) => h("a", { href: ui.link.series(r.code) }, `${r.code} ${r.title}`) },
      { key: "status", label: "Status", sort: (r) => (r.realignment ? 1 : 0), render: (r) => (r.realignment ? core.text.realignment : "Active") },
      { key: "close", label: "Roles with a close link", num: true, sort: (r) => r.nCloseRoles, render: (r) => fmt(r.nCloseRoles) },
      { key: "gen", label: "Generated profile", sort: (r) => (r.generated ? 1 : 0), render: (r) => (r.generated ? "Yes" : "No") },
    ],
    rows,
  });
  const node = frag(
    ui.printMeta(core, "OPM job series"),
    ui.pageHeader({
      crumbs: [{ href: "#/", text: "Home" }, HR_CRUMB, { text: "OPM job series" }],
      kind: "Federal job series",
      title: "OPM job series",
      lede: "Federal job series that EMST roles may relate to. A generated profile groups a role's duties by grade band.",
      meta: disclaimer(hr),
    }),
    h("div", { class: "page-body c-single stack-lg" }, h("p", { class: "prose" }, LINK_MEANS), table,
      h("p", { class: "meta" }, `These pages do not come from OPM. A realignment flag means OPM has proposed a change that is not final.`)));
  return { title: "OPM job series", node };
}

// ------------------------------------------------------------------ series page
function profileBlock(g, core, pctNote) {
  const out = [
    h("p", `EMST generated this profile on ${dateLong(g.stamp?.asOf)} from draft role profiles. It lists duties by grade band to help describe the work. It is not a position description.`),
    h("div", { class: "c-pending" }, ui.pendingSummary({ what: JA_WHAT })),
    h("p", { class: "meta" }, pctNote),
    h("p", { class: "meta" }, "Target levels are editorial design drafts by AI agents."),
  ];
  for (const r of g.roles || []) {
    out.push(h("h3", { class: "h3 c-profile__role" }, h("a", { href: variantHref(r.v) }, r.title), h("span", { class: "meta" }, " (federal)")));
    if (r.fn) out.push(h("p", plain(r.fn)));
    out.push(h("dl", { class: "facts" },
      r.x4 ? [h("dt", "Link to this series"), h("dd", `${ui.matchWords({ pred: r.x4.pred }, "series")} · ${COPY.match.unreviewed}`)] : null,
      r.homeLabel ? [h("dt", "Home area"), h("dd", r.homeLabel)] : null,
      r.instruments?.length ? [h("dt", "Policies linked"), h("dd", h("ul", { class: "c-plain" }, r.instruments.map((i) => h("li", plain(i.title), i.unv ? [" ", h("span", { class: "meta" }, core.text.unverified)] : i.link ? h("span", { class: "meta" }, ` (${plain(i.link)})`) : null))))] : null));
    if (r.credentialGates?.length) out.push(h("h4", { class: "h4" }, "Credentials that may be involved"), credList(r.credentialGates));
    if (r.credentialGatesPending) out.push(h("p", { class: "meta" }, "Some credentials are not shown until their issuer is checked against a source."));
    for (const b of r.bands || []) {
      out.push(h("div", { class: "c-band" },
        h("h4", { class: "c-band__title" }, `${cap(b.group || "Grade band")}: ${b.band}`),
        b.roleLevels?.length ? h("p", { class: "meta" }, `EMST role levels: ${b.roleLevels.map((k) => roleLevelLabel(k).toLowerCase()).join(", ")}`) : null,
        h("h5", { class: "c-band__h" }, `Duties (${fmt((b.duties || []).length)})`),
        r.homeLabel ? h("p", { class: "meta" }, `Duties come from EMST core and from ${r.homeLabel.toLowerCase()} unless marked.`) : null,
        h("ul", { class: "task-list" }, (b.duties || []).map((du) => h("li", h("a", { href: ui.link.comp(du.comp) }, plain(du.duty)),
          (du.isModule && du.moduleLabel !== r.homeLabel) || (du.lc && du.lc !== "established") ? h("p", { class: "task-list__meta" }, du.isModule && du.moduleLabel !== r.homeLabel ? du.moduleLabel : null, du.lc && du.lc !== "established" ? [" ", ui.badgeLifecycle(du.lc, { compact: true })] : null) : null))),
        b.factor1?.length ? ui.disclosure(`Knowledge the work needs (factor 1): ${plural(b.factor1.length, "statement")}`, [
          h("ul", { class: "task-list" }, b.factor1.map((f) => h("li", plain(f.stmt)))),
          b.factor1NotDefault ? h("p", { class: "meta" }, `${plural(b.factor1NotDefault, "more statement")} from module or emerging content ${b.factor1NotDefault === 1 ? "is" : "are"} left out of this default view.`) : null,
        ]) : null));
    }
  }
  return out;
}
export async function renderSeries({ params }) {
  const [core, hr] = await Promise.all([data.core(), data.hr()]);
  const code = String(params.code || "").replace(/^gs-?/i, "");
  const s = hr.series.find((x) => x.code === code || x.slug === code);
  if (!s) throw new NotFound(`No series "${params.code}"`);
  const g = s.generated ? (hr.generated || []).find((x) => x.code === s.code) : null;
  const name = `OPM series ${s.code} ${s.title}`;

  const facts = h("dl", { class: "facts" },
    s.group ? [h("dt", "Occupational group"), h("dd", String(s.group).replace(/\.$/, ""))] : null,
    h("dt", "Status"), h("dd", s.realignment ? core.text.realignment : "Active"),
    s.qualStd ? [h("dt", "Qualification standard"), h("dd", s.qualStd, s.qualVerify ? h("span", { class: "meta" }, " (to be checked against OPM's current standard)") : null)] : null,
    s.ped ? [h("dt", "Positive education requirement"), h("dd", s.ped === "yes" ? "Yes" : s.ped === "no" ? "No" : s.ped, s.pedNote ? h("span", { class: "meta" }, ` (${s.pedNote})`) : null)] : null,
    s.reviewBy ? [h("dt", "Review by"), h("dd", dateLong(s.reviewBy))] : null);

  const sections = [
    ui.section("facts", "About this series", [
      s.realignment ? ui.notice("caution", core.text.realignment, `OPM has proposed changes to some federal job series, including this one. The proposal is not final.${s.successor ? ` It names series ${s.successor} for this work.` : ""}`) : null,
      facts,
    ]),
    ui.section("roles", "Roles linked to this series", roleLinks(s.rows || [], core, "series")),
    s.coreComps?.length ? ui.section("competencies", "Competencies AI agents linked to this series", [
      h("ul", { class: "task-list" }, s.coreComps.map((c) => h("li", h("a", { href: ui.link.comp(c.slug) }, c.title),
        h("p", { class: "task-list__meta" }, `${c.rel === "core" ? "Core to this series" : c.rel === "supporting" ? "Supporting in this series" : humanize(c.rel)} · ${COPY.match.unreviewed}`)))),
      h("p", { class: "meta" }, hr.notes?.defaultView || "", s.omittedModule || s.omittedNotEstablished ? ` Left out here: ${plural(s.omittedModule || 0, "module competency", "module competencies")} and ${plural(s.omittedNotEstablished || 0, "emerging competency", "emerging competencies")}.` : ""),
    ], { meta: plural(s.coreComps.length, "competency", "competencies") }) : null,
    g ? ui.section("profile", "Generated series profile", profileBlock(g, core, hr.pctTimeNote)) : ui.section("profile", "Generated series profile", h("p", "EMST has not generated a profile for this series in this release.")),
    ui.section("about", "About this record", ui.aboutRecord(s, core, { title: name, kind: "OPM series record" })),
  ].filter(Boolean);

  const node = frag(
    ui.printMeta(core, name),
    ui.pageHeader({
      crumbs: [{ href: "#/", text: "Home" }, HR_CRUMB, { href: "#/series", text: "OPM job series" }, { text: `${s.code} ${s.title}` }],
      kind: "OPM job series", id: s.id, title: name,
      meta: disclaimer(hr),
      status: ui.statusLine(s, { aboutHref: "#about" }),
    }),
    h("div", { class: "page-body c-single" }, sections));
  return { title: name, node };
}

// ------------------------------------------------------------------ class index
export async function renderClassIndex() {
  const [core, hr] = await Promise.all([data.core(), data.hr()]);
  const p3 = p3Slugs(core);
  const rows = hr.classes.map((c) => ({ ...c, state: core.stateClasses.find((x) => x.slug === c.slug)?.state || c.jur, nCloseRoles: closeRoleCount(c.rows, p3) }));
  const table = ui.table({
    caption: "State and local job classes in EMST",
    hint: "Links are AI-suggested and not reviewed.",
    sortBy: "jur",
    columns: [
      { key: "title", label: "Class", sort: (r) => r.title, render: (r) => h("a", { href: ui.link.cls(r.slug) }, r.title) },
      { key: "jur", label: "Jurisdiction", sort: (r) => `${r.state} ${r.code}`, render: (r) => r.state },
      { key: "code", label: "Class code", sort: (r) => r.code, render: (r) => h("span", { class: "id" }, r.code) },
      { key: "close", label: "Roles with a close link", num: true, sort: (r) => r.nCloseRoles, render: (r) => fmt(r.nCloseRoles) },
      { key: "view", label: "Class view", sort: (r) => (r.view ? 1 : 0), render: (r) => (r.view ? "Yes" : "No") },
    ],
    rows,
  });
  const node = frag(
    ui.printMeta(core, "State and local job classes"),
    ui.pageHeader({
      crumbs: [{ href: "#/", text: "Home" }, HR_CRUMB, { text: "State and local job classes" }],
      kind: "State and local job classes",
      title: "State and local job classes",
      lede: "Job classes from state and local civil-service plans that EMST roles may relate to. Each page links to the official specification.",
      meta: disclaimer(hr),
    }),
    h("div", { class: "page-body c-single stack-lg" }, h("p", { class: "prose" }, LINK_MEANS), table,
      h("p", { class: "meta" }, "These pages do not come from any state or city. Always check the official specification.")));
  return { title: "State and local job classes", node };
}

// ------------------------------------------------------------------ class page
function classView(view, core, titles) {
  const out = [
    h("p", `EMST generated this view on ${dateLong(view.stamp?.asOf)}. It shows how draft EMST roles might relate to this class.`),
    h("div", { class: "c-pending" }, ui.pendingSummary({ what: JA_WHAT })),
    h("p", { class: "meta" }, "Target levels are editorial design drafts by AI agents."),
  ];
  for (const m of view.mappings || []) {
    out.push(h("h3", { class: "h3 c-profile__role" }, h("a", { href: variantHref(m.v) }, m.roleTitle), h("span", { class: "meta" }, ` (${m.actorLabel})`)));
    out.push(h("dl", { class: "facts" },
      h("dt", "Link to this class"), h("dd", `${ui.matchWords({ pred: m.match }, "class")} · ${COPY.match.unreviewed}`),
      m.roleLevels?.length ? [h("dt", "EMST role levels"), h("dd", m.roleLevels.map((k) => roleLevelLabel(k)).join(", "))] : null,
      m.authority ? [h("dt", "Authority position"), h("dd", m.authority)] : null,
      m.homeLabel ? [h("dt", "Home area"), h("dd", m.homeLabel)] : null));
    if (m.credentialGates?.length) out.push(h("h4", { class: "h4" }, "Credentials that may be involved"), credList(m.credentialGates));
    if (m.credentialGatesPending) out.push(h("p", { class: "meta" }, "Some credentials are not shown until their issuer is checked against a source."));
    if (m.targets?.length) out.push(h("h4", { class: "h4" }, `Competencies and target levels (${fmt(m.targets.length)})`),
      h("ul", { class: "c-rolelist" }, m.targets.map((t) => h("li", { class: "c-rolelist__item" },
        h("p", { class: "c-rolelist__title" }, h("a", { href: ui.link.comp(t.comp) }, t.title), t.lc && t.lc !== "established" ? [" ", ui.badgeLifecycle(t.lc, { compact: true })] : null),
        h("ul", { class: "c-bylevel", "aria-label": `Target levels for ${t.title}` }, ROLE_LEVELS.filter((k) => t.levels?.[k]).map((k) => h("li", h("span", { class: "c-bylevel__k" }, `${roleLevelLabel(k)} `), ui.levelChip(t.levels[k], core))))))));
    if (m.tasks?.length) out.push(ui.disclosure(`Tasks in this view (${fmt(m.tasks.length)})`,
      h("ul", { class: "task-list" }, m.tasks.map((slug) => h("li", h("a", { href: ui.link.task(slug) }, titles.get(slug) || "Task"))))));
  }
  return out;
}

export async function renderClass({ params }) {
  const [core, hr] = await Promise.all([data.core(), data.hr()]);
  const c = hr.classes.find((x) => x.slug === params.slug);
  if (!c) throw new NotFound(`No class "${params.slug}"`);
  let titles = new Map();
  const taskSlugs = (c.view?.mappings || []).flatMap((m) => m.tasks || []);
  if (taskSlugs.length) {
    const t = await data.searchTasks();
    const want = new Set(taskSlugs);
    titles = new Map(t.docs.filter((d) => want.has(d.s)).map((d) => [d.s, d.t]));
  }
  const level = String(c.level || "").replace(/\s*\(ordinal \d+\)/, "");
  const sections = [
    ui.section("facts", "About this class", [
      h("dl", { class: "facts" },
        h("dt", "Jurisdiction"), h("dd", c.jur),
        c.agency ? [h("dt", "Agency"), h("dd", c.agency)] : null,
        c.code ? [h("dt", "Class code"), h("dd", h("span", { class: "id" }, c.code))] : null,
        c.seriesName ? [h("dt", "Class series"), h("dd", c.seriesName)] : null,
        c.employerType ? [h("dt", "Employer type"), h("dd", humanize(c.employerType))] : null,
        level ? [h("dt", "Level in the series"), h("dd", level)] : null,
        c.supervisory ? [h("dt", "Supervision"), h("dd", humanize(c.supervisory))] : null,
        c.specUrl ? [h("dt", "Official specification"), h("dd", ui.a(c.specUrl, `${c.title} specification`),
          h("span", { class: "meta" }, [c.specRetrieved ? ` Retrieved ${dateLong(c.specRetrieved)}.` : null, c.specEffective ? ` Effective ${dateLong(c.specEffective)}.` : null].filter(Boolean).join("")))] : null),
    ]),
    ui.section("quals", "Qualifications and pay", [
      h("p", { class: "meta" }, "AI agents summarized these from the official specification. Always check the specification itself."),
      h("dl", { class: "facts" },
        c.mq ? [h("dt", "Minimum qualifications (paraphrase)"), h("dd", plain(c.mq))] : null,
        c.degreeRule ? [h("dt", "Degree"), h("dd", DEGREE[c.degreeRule] || humanize(c.degreeRule))] : null,
        c.licenses?.length ? [h("dt", "Licenses named in the specification"), h("dd", h("ul", { class: "c-plain" }, c.licenses.map((l) => h("li", `${plain(l.credential)}${l.issuer ? ` (${plain(l.issuer)})` : ""}${l.timing ? `, ${timingWords(l.timing)}` : ""}`))))] : null,
        c.pay ? [h("dt", "Pay"), h("dd", c.pay, c.payEffective ? h("span", { class: "meta" }, ` (effective ${dateLong(c.payEffective)})`) : null)] : null),
    ]),
    ui.section("roles", "Roles linked to this class", roleLinks(c.rows || [], core, "class")),
    c.view ? ui.section("view", "State class view", classView(c.view, core, titles)) : null,
    ui.section("about", "About this record", ui.aboutRecord(c, core, { title: c.title, kind: "State or local class record" })),
  ].filter(Boolean);

  const node = frag(
    ui.printMeta(core, `${c.title} (${c.jur})`),
    ui.pageHeader({
      crumbs: [{ href: "#/", text: "Home" }, HR_CRUMB, { href: "#/classes", text: "State and local job classes" }, { text: c.title }],
      kind: "State or local job class", id: c.id, title: c.title,
      lede: `${c.jur}${c.code ? `, class ${c.code}` : ""}`,
      meta: disclaimer(hr),
      status: ui.statusLine(c, { aboutHref: "#about" }),
    }),
    h("div", { class: "page-body c-single" }, sections));
  return { title: c.title, node };
}
