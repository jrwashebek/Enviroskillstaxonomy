// What's changing (#/changing). DESIGN_SPEC §2.9. Developer C. Everything here is exploratory. Licence: Apache-2.0.
import { h, frag } from "../lib/dom.js";
import * as data from "../lib/data.js";
import * as ui from "../ui.js";
import { COPY } from "../content.js";
import { fmt, dateLong } from "../lib/format.js";
import { plain, humanize, plural, p3Slugs, variantHref } from "./misc.js";

// Short plain names for signal families (core.labels.signalFamily holds the long definitions).
const FAMILY = {
  capability: "What technology can do", "observed-use": "Observed use of technology", deployment: "Deployments of technology",
  "postings-pds": "Job postings and position descriptions", headcount: "Workforce counts", "plan-requirements": "Plan and permit requirements",
  "worker-report": "Reports from practitioners", policy: "Policy and HR events", projection: "Projections", workload: "Workload",
};
const INST_TYPE = {
  statute: "Laws", regulation: "Regulations", "court-decision": "Court decisions", "disclosure-regime": "Disclosure rules",
  guidance: "Guidance", "standard-with-legal-force": "Standards with legal force", "permit-programme": "Permit programs",
  "executive-order": "Executive orders", "agreement-authority": "Agreement authorities", memo: "Memos",
};
const HORIZON = { "0-1y": "within a year", "1-3y": "in 1 to 3 years", "3-5y": "in 3 to 5 years", "5-10y": "in 5 to 10 years", "5y+": "in more than 5 years" };
const DIR = { up: "more demand", down: "less demand", flat: "about the same" };

// Filter state lives in memory (brief: never storage, never the URL).
let familyFilter = null;

const famName = (code) => FAMILY[code] || humanize(code);

function period(per) {
  if (!per) return null;
  return per.start && per.end && per.start !== per.end ? `${dateLong(per.start)} to ${dateLong(per.end)}` : dateLong(per.start || per.end);
}

function measure(m, core) {
  if (!m || m.v === undefined) return null;
  const base = m.n !== undefined ? ` (out of ${fmt(m.n)}${m.den ? ` ${plain(m.den)}` : ""})` : "";
  return [`${fmt(m.v)} ${plain(m.u || "")}`.trim() + base, m.few ? h("strong", `; ${core.text.tooFew}`) : null];
}

function aboutLink(s, core, p3) {
  const about = plain(s.about || "");
  if (!s.target) return about;
  const role = String(s.target).split("--")[0];
  if (p3.has(role) || !core.roles.some((r) => r.slug === role)) return about;
  return h("a", { href: s.target.includes("--") ? variantHref(s.target) : ui.link.role(role) }, about);
}

function signalCard(s, core, p3) {
  if (s.unv) return h("article", { class: "c-card", id: s.id, tabindex: "-1" }, h("h3", { class: "h4 c-card__title" }, plain(s.title)), h("p", core.text.unverified));
  const grade = COPY.sourceGrade[s.sg];
  return h("article", { class: "c-card", id: s.id, tabindex: "-1", "aria-labelledby": `${s.id}-t` },
    h("p", { class: "c-card__kind" }, famName(s.family)),
    h("h3", { class: "h4 c-card__title", id: `${s.id}-t` }, plain(s.title)),
    h("p", { class: "cluster" }, ui.badgeLifecycle(s.status || "watch", { compact: true })),
    h("dl", { class: "facts" },
      s.m ? [h("dt", "Measure"), h("dd", measure(s.m, core))] : null,
      s.per ? [h("dt", "Period"), h("dd", period(s.per))] : null,
      s.sg ? [h("dt", "Source grade"), h("dd", `${s.sg}: ${grade || s.sgTxt || ""}`)] : null,
      s.src ? [h("dt", "Source"), h("dd", plain(s.src))] : null,
      s.about ? [h("dt", "About"), h("dd", aboutLink(s, core, p3))] : null,
      s.reviewBy ? [h("dt", "Review by"), h("dd", dateLong(s.reviewBy))] : null));
}

function signalsSection(ch, core) {
  const p3 = p3Slugs(core);
  const counts = {};
  for (const s of ch.signals) counts[s.family] = (counts[s.family] || 0) + 1;
  const fams = Object.keys(counts).sort((x, y) => counts[y] - counts[x] || famName(x).localeCompare(famName(y)));
  const items = ch.signals.map((s) => ({ s, li: h("li", signalCard(s, core, p3)) }));
  const list = h("ul", { class: "c-cards", id: "signal-list" }, items.map((x) => x.li));
  const live = ui.liveCount();
  const apply = (vals) => {
    familyFilter = vals.size ? vals : null;
    let n = 0;
    for (const { s, li } of items) { const on = !familyFilter || familyFilter.has(s.family); li.hidden = !on; if (on) n++; }
    live.set(`Showing ${fmt(n)} of ${fmt(items.length)} signals`);
    return n;
  };
  const chips = ui.chipGroup({ legend: "Show signals from", name: "family", options: fams.map((f) => ({ value: f, label: famName(f), count: counts[f] })),
    checked: familyFilter ? [...familyFilter] : [], onChange: apply });
  const clear = h("button", { class: "btn btn--tertiary btn--small", type: "button", on: { click: () => { chips.set(new Set()); apply(new Set()); } } }, "Show all families");
  const n = apply(familyFilter || new Set());
  live.node.textContent = `Showing ${fmt(n)} of ${fmt(items.length)} signals`;
  return [
    h("p", "A signal is one piece of evidence that some work may be changing. Each one stays “on watch” until people review it and a second, independent kind of evidence points the same way."),
    chips.node,
    h("div", { class: "result-bar" }, live.node, clear),
    list,
  ];
}

function rolesSection(ch, core) {
  return [
    h("p", "These roles may be forming. They are not described in full yet, so they appear only on this page."),
    h("ul", { class: "c-cards" }, ch.emergingRoles.map((r) => h("li", h("article", { class: "c-card", id: r.slug, tabindex: "-1", "aria-labelledby": `${r.slug}-t` },
      h("p", { class: "c-card__kind" }, "Possible new role"),
      h("h3", { class: "h4 c-card__title", id: `${r.slug}-t` }, r.title),
      h("p", { class: "cluster" }, ui.badgeLifecycle(r.lc, { compact: true })),
      r.fn ? h("p", plain(r.fn)) : null,
      h("dl", { class: "facts" },
        r.horizon ? [h("dt", "Might form"), h("dd", HORIZON[r.horizon] || r.horizon)] : null,
        r.sectors?.length ? [h("dt", "Employers"), h("dd", r.sectors.map((x) => x.actorLabel).join(", "))] : null,
        r.feeders?.length ? [h("dt", "Might grow from"), h("dd", r.feeders.map((f, i) => [i ? ", " : null, h("a", { href: ui.link.role(f.slug) }, f.title)]))] : null,
        r.reviewBy ? [h("dt", "Review by"), h("dd", dateLong(r.reviewBy))] : null,
        r.counter ? [h("dt", "What would show this isn't happening"), h("dd", plain(r.counter))] : null),
      r.scen?.length ? h("p", { class: "meta" }, `${core.text.scenarioSensitivity}: `, r.scen.map((s) => `${s.label}, ${DIR[s.dir] || s.dir}`).join("; "), ".") : null)))),
  ];
}

function compsSection(ch, core) {
  const out = [
    h("p", "Competencies that may be emerging. Each has a date by which it is reviewed again, and is dropped if no new evidence comes in."),
    h("ul", { class: "task-list" }, ch.emergingComps.map((c) => h("li", h("a", { href: ui.link.comp(c.slug) }, c.title), " ", ui.badgeLifecycle(c.lc, { compact: true }),
      h("p", { class: "task-list__meta" }, [c.isModule ? c.moduleLabel : null, c.reviewBy ? `Review by ${dateLong(c.reviewBy)}` : null].filter(Boolean).join(" · "))))),
  ];
  if (ch.watchItems?.length) {
    out.push(h("h3", { class: "h4" }, "Ideas on watch"));
    out.push(h("ul", { class: "c-cards" }, ch.watchItems.map((w) => h("li", h("article", { class: "c-card", id: w.slug, tabindex: "-1" },
      h("p", { class: "c-card__kind" }, w.hyp?.type ? `Possible new ${w.hyp.type.toLowerCase()}` : "Watch item"),
      h("h4", { class: "c-card__title" }, w.title),
      w.hyp?.stmt ? h("p", plain(w.hyp.stmt)) : null,
      h("dl", { class: "facts" },
        w.reviewBy ? [h("dt", "Review by"), h("dd", dateLong(w.reviewBy))] : null,
        w.counter ? [h("dt", "What would show this isn't happening"), h("dd", plain(w.counter))] : null))))));
  }
  return out;
}

function instrumentItem(i, core) {
  if (i.unv) return h("li", { class: "c-inst" }, h("p", { class: "c-inst__title" }, plain(i.title)), h("p", { class: "meta" }, core.text.unverified));
  const evs = (i.ev || []).map((e) => h("li", e.sup ? `${humanize(e.type)} (date not shown)` : `${dateLong(e.d)}: ${humanize(e.type)}${e.fut ? " (scheduled)" : ""}`));
  return h("li", { class: "c-inst" },
    h("p", { class: "c-inst__title" }, plain(i.title)),
    h("p", { class: "meta" }, [i.jur, i.cit ? plain(i.cit) : null].filter(Boolean).join(" · ")),
    h("dl", { class: "facts" },
      h("dt", `Status on ${dateLong(core.release.date)}`), h("dd", i.noEv ? "Status not recorded" : (i.stTxt || core.labels.instrumentStatus?.[i.st] || humanize(i.st))),
      evs.length ? [h("dt", "Dated events"), h("dd", h("ul", { class: "c-inst__events" }, evs))] : null,
      i.next ? [h("dt", "Next review"), h("dd", dateLong(i.next))] : null));
}

function instrumentsSection(ch, core) {
  const groups = new Map();
  for (const i of ch.instruments) { if (!groups.has(i.type)) groups.set(i.type, []); groups.get(i.type).push(i); }
  const order = [...groups.keys()].sort((x, y) => groups.get(y).length - groups.get(x).length);
  const w = ch.instrumentsWithheld;
  return [
    h("p", "Laws, rules, court decisions and guidance that can change environmental work. Status is as of the release date. AI agents recorded these, and no person has checked them."),
    ...order.map((t) => ui.disclosure(`${INST_TYPE[t] || humanize(t)} (${fmt(groups.get(t).length)})`,
      h("ul", { class: "c-insts" }, groups.get(t).sort((a, b) => String(a.title).localeCompare(String(b.title))).map((i) => instrumentItem(i, core))))),
    w?.n ? h("p", { class: "meta" }, `${plural(w.n, "more instrument")} ${w.n === 1 ? "is" : "are"} left out of this release: ${w.reason}.`) : null,
  ];
}

function scenariosSection(ch, core) {
  const sc = ch.scenarios || {};
  return [
    h("p", "Scenarios are possible futures, not forecasts. AI agents built them in a desk exercise around two big uncertainties. No practitioner workshop has reviewed them."),
    sc.axes?.length ? [h("h3", { class: "h4" }, "The two uncertainties"),
      h("dl", { class: "facts" }, sc.axes.map((a) => [h("dt", a.label), h("dd", (a.poles || []).map((p) => h("p", plain(p.def))))]))] : null,
    sc.terms?.length ? [h("h3", { class: "h4" }, "Four possible futures"),
      h("ul", { class: "c-cards c-cards--2" }, sc.terms.map((t) => h("li", h("article", { class: "c-card" },
        h("h4", { class: "c-card__title" }, t.label),
        t.summary ? h("p", plain(t.summary)) : h("p", { class: "meta" }, "No summary in this release."),
        t.risk ? h("p", h("strong", "Main risk: "), plain(t.risk)) : null))))] : null,
    sc.noRegret?.length ? [h("h3", { class: "h4" }, "Moves judged worthwhile in every scenario"),
      h("ul", { class: "c-noregret" }, sc.noRegret.map((n) => h("li", plain(n.text)))),
      h("p", { class: "meta" }, core.text.noRegret)] : null,
    sc.signposts?.length ? ui.disclosure(`Signposts we watch (${fmt(sc.signposts.length)})`, [
      h("p", "A signpost is something we keep measuring that would show which future is unfolding."),
      h("ul", { class: "task-list" }, sc.signposts.map((s) => h("li", plain(s.text), h("p", { class: "task-list__meta" }, [s.source, s.cadence ? `checked ${s.cadence}` : null].filter(Boolean).map(plain).join(" · ")))))]) : null,
    sc.wildcards?.length ? ui.disclosure(`Wild cards (${fmt(sc.wildcards.length)})`, [
      h("p", "Rare events that could change things quickly."),
      h("ul", { class: "task-list" }, sc.wildcards.map((w) => h("li", plain(w.text))))]) : null,
  ];
}

function howToRead(core) {
  return ui.disclosure("How to read this page", [
    h("h3", { class: "h4" }, "On watch"),
    h("p", COPY.lifecycle.watch.plain),
    h("p", { class: "meta" }, core.text.watchSignal),
    h("h3", { class: "h4" }, "Source grades"),
    h("p", `Each signal has a grade for its source, from A to D: ${core.text.sourceGrade}.`),
    h("dl", { class: "facts" }, Object.entries(COPY.sourceGrade).map(([k, v]) => [h("dt", k), h("dd", v)])),
    h("h3", { class: "h4" }, "Signposts"),
    h("p", "A signpost is something we keep measuring, such as hiring in a job series. If signposts move, we look again at which future is unfolding."),
    h("p", h("a", { href: ui.link.key("source-grades") }, "More about these labels")),
  ]);
}

export async function render({ section } = {}) {
  const [core, ch] = await Promise.all([data.core(), data.change()]);
  // A deep link to a signal must work even if the in-memory filter would hide that signal.
  const target = section ? ch.signals.find((s) => s.id === section) : null;
  if (target && familyFilter && !familyFilter.has(target.family)) familyFilter = null;
  const ci = ch.changeIndicators || {};
  const allWatch = ch.signals.every((s) => s.status === "watch");
  const fig = ch.figures?.signals;
  const sections = [
    { id: "signals", title: "Signals" },
    ch.emergingRoles?.length ? { id: "emerging-roles", title: "Roles that may be forming" } : null,
    ch.emergingComps?.length ? { id: "emerging-competencies", title: "Competencies that may be emerging" } : null,
    ch.instruments?.length ? { id: "instruments", title: "Laws, rules and policies" } : null,
    ch.scenarios ? { id: "scenarios", title: "Scenarios" } : null,
  ].filter(Boolean);
  const t = (id) => sections.find((s) => s.id === id)?.title;

  const summary = h("div", { class: "c-summaryline" },
    h("p", h("strong", plural(ch.signals.length, "signal")), allWatch ? ", all on watch. " : ". ",
      ci.moved === 0 ? `No change indicator has moved: ${fmt(ci.n)} were checked, and none has enough evidence yet.` : `${plural(ci.moved, "change indicator")} of ${fmt(ci.n)} moved.`),
    fig ? h("p", { class: "cluster" }, ui.badgeTier(fig.tier?.t || "exploratory", { compact: true }), fig.ev?.l ? ui.badgeEvidence(fig.ev.l, { compact: true }) : null) : null);

  const main = [
    ui.section("signals", t("signals"), signalsSection(ch, core), { meta: plural(ch.signals.length, "signal") }),
    ch.emergingRoles?.length ? ui.section("emerging-roles", t("emerging-roles"), rolesSection(ch, core), { meta: plural(ch.emergingRoles.length, "role") }) : null,
    ch.emergingComps?.length ? ui.section("emerging-competencies", t("emerging-competencies"), compsSection(ch, core), { meta: plural(ch.emergingComps.length, "competency", "competencies") }) : null,
    ch.instruments?.length ? ui.section("instruments", t("instruments"), instrumentsSection(ch, core), { meta: plural(ch.instruments.length, "instrument") }) : null,
    ch.scenarios ? ui.section("scenarios", t("scenarios"), scenariosSection(ch, core)) : null,
  ];

  const node = frag(
    ui.printMeta(core, "What's changing"),
    ui.pageHeader({
      crumbs: [{ href: "#/", text: "Home" }, { text: "What's changing" }],
      kind: "Foresight, for exploring only",
      title: "What's changing",
      lede: "Early signs of how environmental work may change: new tools, rules, roles and skills. Nothing here is a forecast.",
      meta: frag(ui.notice("exploratory", "Exploratory", ch.notice), howToRead(core), summary),
    }),
    ui.withMargin(sections, main));
  return { title: "What's changing", node };
}
