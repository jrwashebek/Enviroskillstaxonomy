// What's changing (#/changing). DESIGN_SPEC §2.9, restructured in round 2 as a hub (usability report §5): a short overview
// with four section cards, then four sections that start collapsed. Deep links (#/changing@sig-…, @rol-…, @ins-…, a
// section id) open whatever holds the target before the router focuses it. Everything here is exploratory.
// Developer C. Licence: Apache-2.0.
import { h, frag } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { focusSection, parseHash } from "../lib/router.js";
import * as ui from "../ui.js";
import { COPY } from "../content.js";
import { fmt, dateLong } from "../lib/format.js";
import { plain, scrub, humanize, plural, p3Slugs, variantHref } from "./misc.js";

// Short plain names for signal families, in reading order: technology, work, labour market, plans and policy, then
// other bodies' projections last (core.labels.signalFamily holds the long definitions).
const FAMILY = {
  capability: "What technology can do", "observed-use": "Observed use of technology", deployment: "Technology in use",
  "postings-pds": "Job postings and position descriptions", headcount: "Workforce counts", workload: "Workload",
  "plan-requirements": "Plan and permit requirements", policy: "Policy and HR events", "worker-report": "Reports from practitioners",
  projection: "Other bodies' projections",
};
const FAM_ORDER = Object.keys(FAMILY);
const INST_TYPE = {
  statute: "Laws", regulation: "Regulations", "court-decision": "Court decisions", "disclosure-regime": "Disclosure rules",
  guidance: "Guidance", "standard-with-legal-force": "Standards with legal force", "permit-programme": "Permit programs",
  "executive-order": "Executive orders", "agreement-authority": "Agreement authorities", memo: "Memos",
};
const HORIZON = { "0-1y": "within a year", "1-3y": "in 1 to 3 years", "3-5y": "in 3 to 5 years", "5-10y": "in 5 to 10 years", "5y+": "in more than 5 years" };
const DIR = { up: "more demand", down: "less demand", flat: "about the same" };
const PER_FAMILY = 8;

// UI state lives in memory only (brief: never storage, never the URL). It survives Back within the session.
const st = { families: new Set(), role: "", open: new Set(), allFam: new Set() };
let cur = null; // the page currently on screen: {root, rowsById, revealRow}

const famName = (code) => FAMILY[code] || humanize(code);
const famRank = (code) => { const i = FAM_ORDER.indexOf(code); return i < 0 ? 99 : i; };

// ------------------------------------------------------------------ measures
/** 80.57 → 81, 5.6 → 5.6, 1.44 → 1.4: whole numbers from 10 up, one decimal below. */
const roundShown = (v) => (Math.abs(v) >= 10 ? Math.round(v) : Math.round(v * 10) / 10);
const clean = (v) => Number(Number(v).toPrecision(12));
/** The noun a unit counts: "use cases at development stage: deployed" → "case". */
function headNoun(u) {
  const core = String(u || "").replace(/\(.*?\)/g, "").split(/:|\s(?:at|of|per|in|among|for)\s/)[0].trim();
  return (core.split(/\s+/).pop() || "").toLowerCase().replace(/s$/, "");
}
function measure(m, core) {
  if (!m || m.v === undefined) return null;
  const u = String(m.u || "");
  const share = /^share\b/.test(u);
  const raw = clean(share ? m.v * 100 : m.v);
  const shown = roundShown(raw);
  const rest = share ? u.replace(/^share\b,?\s*/, "") : u;
  let value;
  if (share) value = `${raw < 0 ? "down " : ""}${fmt(Math.abs(shown))}%${rest ? (/^of\s/.test(rest) ? ` ${plain(rest)}` : ` (${plain(rest)})`) : ""}`;
  else if (u === "percent") value = `${shown > 0 ? "+" : ""}${fmt(shown)}%`;
  else value = `${fmt(shown)} ${plain(u)}`.trim();
  let base = "";
  if (m.n !== undefined && m.den) {
    const noun = headNoun(share ? rest.replace(/^of\s+/, "") : u);
    const same = noun && new RegExp(`\\b${noun}s?\\b`, "i").test(m.den);
    base = `, ${same ? "out of" : "from"} ${fmt(m.n)} ${plain(m.den)}`;
  }
  return {
    text: [value + base, m.few ? h("strong", `; ${core.text.tooFew}`) : null],
    exact: shown !== raw ? `${fmt(raw)}${share || u === "percent" ? "%" : ""}` : null,
    context: m.n === undefined && m.den && !/^not (applicable|a census)$/i.test(m.den) ? plain(m.den) : null,
  };
}
function period(per) {
  if (!per) return null;
  return per.start && per.end && per.start !== per.end ? `${dateLong(per.start)} to ${dateLong(per.end)}` : dateLong(per.start || per.end);
}

// ------------------------------------------------------------------ reveal (deep links and in-page links)
/** Open everything that hides the element with this id: section disclosures, "show 8" limits, filters, closed details. */
function reveal(root, id) {
  if (!id || !root) return null;
  if (cur?.rowsById.has(id)) cur.revealRow(id);
  let el = root.querySelector(`#${CSS.escape(id)}`);
  if (!el) return null;
  for (let p = el; p && p !== root; p = p.parentNode) {
    if (p.tagName === "DETAILS" && !(p === el)) p.open = true;
    if (p.hidden && p.parentElement?.id) {
      const btn = root.querySelector(`[aria-controls="${CSS.escape(p.parentElement.id)}"][aria-expanded="false"]`);
      if (btn) btn.click();
    }
  }
  if (el.tagName === "SECTION") { const d = el.querySelector("details.c-secbody"); if (d) d.open = true; }
  return el;
}
/** A link to a place on this page. Its href is the deep link (so "open in new tab" works); a plain click never
 *  changes the address: it opens what holds the target and moves focus there. */
function here(id, ...children) {
  return h("a", { href: `#/changing@${id}`, on: { click: (e) => {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    const root = e.currentTarget.closest(".c-changing");
    if (root && reveal(root, id)) { e.preventDefault(); focusSection(id); }
  } } }, ...children);
}
// Same-page deep links (for example a search result chosen while this page is open) do not re-render, so open the
// target before the router's own hashchange handler focuses it. Capture listeners on the target run first.
let listening = false;
function listen() {
  if (listening) return;
  listening = true;
  window.addEventListener("hashchange", () => {
    const { path, section } = parseHash();
    if (path === "/changing" && section && cur?.root?.isConnected) {
      const el = reveal(cur.root, section);
      if (el) setTimeout(() => { if (document.activeElement !== el) focusSection(section); }, 0);
    }
  }, true);
}

// ------------------------------------------------------------------ signals
/** "… (role: Ecologist)" → "…". The role is shown on its own line. */
function baseTitle(t) {
  const s = String(t || "");
  const i = s.lastIndexOf(" (role: ");
  return i > 0 && s.endsWith(")") ? s.slice(0, i) : s;
}
/** Signals with the same title, measure, period, grade and source are one piece of evidence recorded once per role
 *  (51 BLS projection signals are 21 occupations). Show each once and list what it is about. */
function groupSignals(signals) {
  const groups = new Map();
  for (const s of signals) {
    const base = baseTitle(s.title);
    const key = s.unv ? s.id : JSON.stringify([s.family, base, s.m, s.per, s.sg, s.src]);
    if (!groups.has(key)) groups.set(key, { base, family: s.family, sigs: [], unv: !!s.unv });
    groups.get(key).sigs.push(s);
  }
  return [...groups.values()];
}

function aboutItem(s, ctx) {
  const { core, ch, p3, roleBy } = ctx;
  if (s.target) {
    const slug = String(s.target).split("--")[0];
    const r = roleBy.get(slug);
    if (r && p3.has(slug)) return { role: slug, node: here(slug, r.title), note: "may be forming" };
    if (r) return { role: slug, node: h("a", { href: s.target.includes("--") ? variantHref(s.target) : ui.link.role(slug) }, plain(s.about || r.title)) };
  }
  const about = String(s.about || "");
  const sp = /^Signpost (SP-\d+)$/.exec(about);
  if (sp) {
    const post = (ch.scenarios?.signposts || []).find((x) => x.code === sp[1]);
    return { node: post ? `A scenario signpost: ${scrub(post.text)}` : "A scenario signpost" };
  }
  const inst = (ch.instruments || []).find((i) => i.title === about && !i.unv);
  if (inst) return { node: here(inst.id, plain(about)) };
  return { node: plain(about) };
}

/** ui.jargon, but only the first use of a term on the page is marked up; later uses stay plain text (less noise). */
function jargonOnce(text, seen) {
  const before = new Set(seen);
  return ui.jargon(text, seen).map((n) => (n && n.tagName === "ABBR" && before.has(n.textContent) ? n.textContent : n));
}

function rowNode(g, ctx, seen) {
  const { core } = ctx;
  const s0 = g.sigs[0];
  const tid = `${s0.id}-t`;
  if (g.unv) return h("li", { class: "c-sig", id: s0.id, tabindex: "-1", "aria-labelledby": tid },
    h("p", { class: "c-sig__title", id: tid }, plain(s0.title)), h("p", { class: "meta" }, core.text.unverified));
  const abouts = g.sigs.map((s) => aboutItem(s, ctx));
  // one entry per distinct thing it is about
  const uniq = [];
  const seenAbout = new Set();
  for (const a of abouts) { const k = a.role || (typeof a.node === "string" ? a.node : a.node.textContent); if (!seenAbout.has(k)) { seenAbout.add(k); uniq.push(a); } }
  const nRoles = uniq.filter((a) => a.role).length;
  const aboutLead = uniq.length === 1 ? "About: " : nRoles === uniq.length ? `About ${fmt(nRoles)} roles: ` : "About: ";
  const grade = COPY.sourceGrade?.[s0.sg];
  const ms = measure(s0.m, core);
  const details = ui.disclosure([`Details`, h("span", { class: "vh" }, `: ${scrub(g.base)}`)], [
    h("dl", { class: "facts" },
      ms ? [h("dt", "Measure, as reported"), h("dd", ms.text)] : null,
      ms?.exact ? [h("dt", "Exact figure"), h("dd", ms.exact)] : null,
      ms?.context ? [h("dt", "Context"), h("dd", ms.context)] : null,
      s0.per ? [h("dt", "Period"), h("dd", period(s0.per))] : null,
      s0.sg ? [h("dt", "Source grade"), h("dd", `${s0.sg}: ${grade || s0.sgTxt || ""}`)] : null,
      s0.src ? [h("dt", "Reported in"), h("dd", scrub(s0.src))] : null,
      h("dt", "Status"), h("dd", ui.badgeLifecycle(s0.status || "watch", { compact: true }), s0.reviewBy ? ` Review by ${dateLong(s0.reviewBy)}.` : null)),
    g.sigs.length > 1 ? h("p", { class: "meta" }, `EMST recorded this evidence ${fmt(g.sigs.length)} times, once for each thing it is about. It is shown once here.`) : null,
  ], { small: true });
  return h("li", { class: "c-sig", id: s0.id, tabindex: "-1", "aria-labelledby": tid },
    h("p", { class: "c-sig__title", id: tid }, jargonOnce(scrub(g.base), seen)),
    h("p", { class: "c-sig__meta meta" }, famName(g.family), " · ", s0.sg ? `Source grade ${s0.sg}` : "No source grade"),
    h("p", { class: "c-sig__about" }, h("span", { class: "c-sig__k" }, aboutLead),
      uniq.map((a, i) => [i ? "; " : null, a.node, a.note ? h("span", { class: "meta" }, ` (${a.note})`) : null])),
    details);
}

function signalsBody(ch, ctx) {
  const { core, roleBy, p3 } = ctx;
  const seen = new Set(["AI"]);
  const groups = groupSignals(ch.signals);
  const rows = groups.map((g) => ({ g, li: rowNode(g, ctx, seen), roles: new Set(g.sigs.map((s) => s.target && String(s.target).split("--")[0]).filter(Boolean)) }));
  const rowsById = new Map();
  for (const r of rows) for (const s of r.g.sigs) rowsById.set(s.id, r);

  // family groups, each showing the first PER_FAMILY matching rows
  const fams = [...new Set(rows.map((r) => r.g.family))].sort((a, b) => famRank(a) - famRank(b));
  const sigCount = {};
  for (const s of ch.signals) sigCount[s.family] = (sigCount[s.family] || 0) + 1;
  const famBlocks = new Map();
  for (const f of fams) {
    const list = h("ul", { class: "c-sigs", id: `fam-${f}-list` }, rows.filter((r) => r.g.family === f).map((r) => r.li));
    const count = h("p", { class: "meta c-fam__count" });
    const more = h("button", { class: "btn btn--tertiary btn--small", type: "button", "aria-controls": `fam-${f}-list`, "aria-expanded": "false" });
    const block = h("div", { class: "c-fam" }, h("h3", { class: "h4 c-fam__title", id: `fam-${f}-h` }, famName(f)), count, list, h("p", { class: "c-more no-print" }, more));
    famBlocks.set(f, { block, count, more, list });
    more.addEventListener("click", () => {
      const opening = !st.allFam.has(f);
      if (opening) st.allFam.add(f); else st.allFam.delete(f);
      const firstNew = apply();
      // "Show all" moves focus to the first newly shown item (accessibility review, round 2)
      if (opening && firstNew.get(f)) firstNew.get(f).focus();
    });
  }

  // role filter: a native select (36 roles are too many for chips on a phone)
  const roleCounts = new Map();
  for (const r of rows) for (const slug of r.roles) roleCounts.set(slug, (roleCounts.get(slug) || 0) + r.g.sigs.filter((s) => String(s.target || "").split("--")[0] === slug).length);
  const roleOpt = (slug) => h("option", { value: slug }, `${roleBy.get(slug)?.title || slug} (${fmt(roleCounts.get(slug))})`);
  const bySlugTitle = (a, b) => String(roleBy.get(a)?.title).localeCompare(String(roleBy.get(b)?.title));
  const profiled = [...roleCounts.keys()].filter((s) => !p3.has(s)).sort(bySlugTitle);
  const forming = [...roleCounts.keys()].filter((s) => p3.has(s)).sort(bySlugTitle);
  const sel = h("select", { class: "c-select", id: "sig-role" }, h("option", { value: "" }, "Any role"),
    profiled.length ? h("optgroup", { label: "Roles with a draft profile" }, profiled.map(roleOpt)) : null,
    forming.length ? h("optgroup", { label: "Roles that may be forming" }, forming.map(roleOpt)) : null);
  if (st.role && !roleCounts.has(st.role)) st.role = "";
  sel.value = st.role;

  const chips = ui.chipGroup({ legend: "Kind of evidence", name: "family", options: fams.map((f) => ({ value: f, label: famName(f), count: sigCount[f] })),
    checked: [...st.families], onChange: (vals) => { st.families = vals; apply(); } });
  sel.addEventListener("change", () => { st.role = sel.value; apply(); });
  const live = ui.liveCount();
  const clearBtn = h("button", { class: "btn btn--tertiary btn--small", type: "button", on: { click: () => { st.families = new Set(); st.role = ""; chips.set(new Set()); sel.value = ""; apply(); } } }, "Clear filters");
  const empty = ui.emptyState({ title: "No signals match these filters", body: "Choose another kind of evidence or another role, or clear the filters." });

  function matches(r) { return (!st.families.size || st.families.has(r.g.family)) && (!st.role || r.roles.has(st.role)); }
  function apply() {
    let nSig = 0, nRow = 0;
    const firstNew = new Map();
    for (const f of fams) {
      const fb = famBlocks.get(f);
      const mine = rows.filter((r) => r.g.family === f);
      const on = mine.filter(matches);
      const all = st.allFam.has(f);
      mine.forEach((r) => { r.li.hidden = true; });
      on.forEach((r, i) => { r.li.hidden = !all && i >= PER_FAMILY; if (all && i === PER_FAMILY) firstNew.set(f, r.li); });
      const sigs = on.reduce((n, r) => n + (st.role ? r.g.sigs.filter((s) => String(s.target || "").split("--")[0] === st.role).length : r.g.sigs.length), 0);
      nSig += sigs; nRow += on.length;
      fb.block.hidden = !on.length;
      const merged = sigs !== on.length;
      fb.count.textContent = `${plural(sigs, "signal")}${merged ? ` in ${plural(on.length, "row")}` : ""}${!all && on.length > PER_FAMILY ? `. Showing the first ${fmt(PER_FAMILY)}.` : "."}`;
      fb.more.parentElement.hidden = on.length <= PER_FAMILY;
      fb.more.textContent = all ? `Show fewer in “${famName(f)}”` : `Show all ${fmt(on.length)} in “${famName(f)}”`;
      fb.more.setAttribute("aria-expanded", String(all));
    }
    const filtered = st.families.size || st.role;
    live.set(filtered ? `Showing ${plural(nSig, "signal")} of ${fmt(ch.signals.length)}` : `Showing all ${plural(ch.signals.length, "signal")}`);
    clearBtn.hidden = !filtered;
    empty.hidden = nRow > 0;
    return firstNew;
  }
  apply();

  /** A deep link to one signal: make sure no filter or "show 8" limit hides it, and give its row that id. */
  function revealRow(id) {
    const r = rowsById.get(id);
    if (!r) return;
    if (!matches(r)) { st.families = new Set(); st.role = ""; chips.set(new Set()); sel.value = ""; }
    const on = rows.filter((x) => x.g.family === r.g.family && matches(x));
    if (on.indexOf(r) >= PER_FAMILY) st.allFam.add(r.g.family);
    apply();
    r.li.id = id;
  }

  const nMerged = groups.filter((g) => g.sigs.length > 1);
  const node = [
    h("p", "A signal is one piece of evidence that some work may be changing. Each one stays “on watch” until people review it and a second, independent kind of evidence points the same way."),
    nMerged.length ? h("p", { class: "meta" }, `Some evidence was recorded once for each role it is about. Here it is shown once, with every role listed: ${plural(ch.signals.length, "signal")} in ${plural(groups.length, "row")}.`) : null,
    h("div", { class: "c-filters" }, chips.node,
      h("div", { class: "c-field" }, h("label", { class: "c-field__label", for: "sig-role" }, "About a role"), sel)),
    h("div", { class: "result-bar" }, live.node, clearBtn),
    empty,
    fams.map((f) => famBlocks.get(f).block),
  ];
  return { node, rowsById, revealRow, groups };
}

// ------------------------------------------------------------------ roles and competencies that may be forming
function formingBody(ch, core) {
  const roles = ch.emergingRoles || [];
  const onlyHere = roles.filter((r) => r.wc);
  const profiled = roles.filter((r) => !r.wc);
  const join = (xs) => xs.length > 1 ? [xs.slice(0, -1).map((x, i) => [i ? ", " : null, x]), " and ", xs[xs.length - 1]] : xs;
  const out = [h("p", "Each item here stays on watch until new evidence comes in by its review date. It is dropped if none does.")];
  if (roles.length) {
    out.push(h("h3", { id: "emerging-roles", tabindex: "-1" }, "Roles that may be forming"),
      h("p", onlyHere.length ? `${plural(onlyHere.length, "role")} ${onlyHere.length === 1 ? "is" : "are"} described only on this page, because the work is not yet shown to exist.` : null,
        profiled.length ? [" ", `${profiled.length === 1 ? "One role also has" : `${fmt(profiled.length)} roles also have`} a full draft profile: `,
          join(profiled.map((r) => h("a", { href: ui.link.role(r.slug) }, r.title))), "."] : null),
      h("ul", { class: "c-cards" }, roles.map((r) => h("li", h("article", { class: "c-card", id: r.slug, tabindex: "-1", "aria-labelledby": `${r.slug}-t` },
        h("p", { class: "c-card__kind" }, r.wc ? "Possible new role · described only here" : "Possible new role · has a draft profile"),
        h("h4", { class: "c-card__title", id: `${r.slug}-t` }, r.wc ? r.title : h("a", { href: ui.link.role(r.slug) }, r.title)),
        r.fn ? h("p", scrub(r.fn)) : null,
        h("dl", { class: "facts" },
          r.horizon ? [h("dt", "Might form"), h("dd", HORIZON[r.horizon] || r.horizon)] : null,
          r.sectors?.length ? [h("dt", "Employers"), h("dd", r.sectors.map((x) => x.actorLabel).join(", "))] : null,
          r.feeders?.length ? [h("dt", "Might grow from"), h("dd", r.feeders.map((f, i) => [i ? ", " : null, h("a", { href: ui.link.role(f.slug) }, f.title)]))] : null,
          r.reviewBy ? [h("dt", "Review by"), h("dd", dateLong(r.reviewBy))] : null,
          r.counter ? [h("dt", "What would show this isn't happening"), h("dd", scrub(r.counter))] : null),
        r.scen?.length ? h("p", { class: "meta" }, `${core.text.scenarioSensitivity}: `, r.scen.map((s) => `${s.label}, ${DIR[s.dir] || s.dir}`).join("; "), ".") : null)))));
  }
  if (ch.emergingComps?.length) {
    const list = h("ul", { class: "task-list", id: "emerging-comp-list" }, ch.emergingComps.map((c) => h("li", { id: c.slug, tabindex: "-1" }, h("a", { href: ui.link.comp(c.slug) }, c.title), " ", ui.badgeLifecycle(c.lc, { compact: true }),
      h("p", { class: "task-list__meta" }, [c.isModule ? c.moduleLabel : null, c.reviewBy ? `Review by ${dateLong(c.reviewBy)}` : null].filter(Boolean).join(" · ")))));
    out.push(h("h3", { id: "emerging-competencies", tabindex: "-1" }, "Competencies that may be emerging"),
      h("p", { class: "meta" }, plural(ch.emergingComps.length, "competency", "competencies")),
      showMore(list, 8, (n) => `Show all ${fmt(n)} competencies`, "Show fewer competencies"));
  }
  if (ch.watchItems?.length) {
    out.push(h("h3", { id: "watch-items", tabindex: "-1" }, "Ideas on watch"));
    out.push(h("ul", { class: "c-cards" }, ch.watchItems.map((w) => h("li", h("article", { class: "c-card", id: w.slug, tabindex: "-1", "aria-labelledby": `${w.slug}-t` },
      h("p", { class: "c-card__kind" }, w.hyp?.type ? `Possible new ${w.hyp.type.toLowerCase()}` : "Watch item"),
      h("h4", { class: "c-card__title", id: `${w.slug}-t` }, w.title),
      w.hyp?.stmt ? h("p", scrub(w.hyp.stmt)) : null,
      h("dl", { class: "facts" },
        w.reviewBy ? [h("dt", "Review by"), h("dd", dateLong(w.reviewBy))] : null,
        w.counter ? [h("dt", "What would show this isn't happening"), h("dd", scrub(w.counter))] : null))))));
  }
  return out;
}

/** First n items of a list, then a button for the rest. "Show all" moves focus to the first newly shown item. */
function showMore(list, n, moreLabel, lessLabel) {
  const items = [...list.children];
  if (items.length <= n) return list;
  let open = false;
  const btn = h("button", { class: "btn btn--tertiary btn--small", type: "button", "aria-expanded": "false", "aria-controls": list.id });
  const draw = () => { items.forEach((li, i) => { li.hidden = !open && i >= n; }); btn.textContent = open ? lessLabel : moreLabel(items.length); btn.setAttribute("aria-expanded", String(open)); };
  btn.addEventListener("click", () => { open = !open; draw(); if (open && items[n]) { if (!items[n].hasAttribute("tabindex")) items[n].setAttribute("tabindex", "-1"); items[n].focus(); } });
  draw();
  return frag(list, h("p", { class: "c-more no-print" }, btn));
}

// ------------------------------------------------------------------ laws and policies
function instrumentItem(i, core) {
  if (i.unv) return h("li", { class: "c-inst", id: i.id, tabindex: "-1" }, h("p", { class: "c-inst__title" }, plain(i.title)), h("p", { class: "meta" }, core.text.unverified));
  const evs = (i.ev || []).map((e) => h("li", e.sup ? `${humanize(e.type)} (date not shown)` : `${dateLong(e.d)}: ${humanize(e.type)}${e.fut ? " (scheduled)" : ""}`));
  return h("li", { class: "c-inst", id: i.id, tabindex: "-1" },
    h("p", { class: "c-inst__title" }, plain(i.title)),
    h("p", { class: "meta" }, [i.jur, i.cit ? plain(i.cit) : null].filter(Boolean).join(" · ")),
    h("dl", { class: "facts" },
      h("dt", `Status on ${dateLong(core.release.date)}`), h("dd", i.noEv ? "Status not recorded" : (i.stTxt || core.labels.instrumentStatus?.[i.st] || humanize(i.st))),
      evs.length ? [h("dt", "Dated events"), h("dd", h("ul", { class: "c-inst__events" }, evs))] : null,
      i.next ? [h("dt", "Next review"), h("dd", dateLong(i.next))] : null));
}
function instrumentsBody(ch, core) {
  const groups = new Map();
  for (const i of ch.instruments) { if (!groups.has(i.type)) groups.set(i.type, []); groups.get(i.type).push(i); }
  const order = [...groups.keys()].sort((x, y) => groups.get(y).length - groups.get(x).length);
  const w = ch.instrumentsWithheld;
  return [
    h("p", "Laws, rules, court decisions and guidance that can change environmental work, grouped by kind. Status is as of the release date. AI agents recorded these, and no person has checked them."),
    ...order.map((t) => ui.disclosure(`${INST_TYPE[t] || humanize(t)} (${fmt(groups.get(t).length)})`,
      h("ul", { class: "c-insts" }, groups.get(t).sort((a, b) => String(a.title).localeCompare(String(b.title))).map((i) => instrumentItem(i, core))))),
    w?.n ? h("p", { class: "meta" }, `${plural(w.n, "more law or policy", "more laws and policies")} ${w.n === 1 ? "is" : "are"} left out of this release: ${w.reason}.`) : null,
  ];
}

// ------------------------------------------------------------------ scenarios
function scenariosBody(ch, core) {
  const sc = ch.scenarios || {};
  return [
    h("p", "Scenarios are possible futures, not forecasts. AI agents built them in a desk exercise around two big uncertainties. No practitioner workshop has reviewed them."),
    sc.axes?.length ? [h("h3", "The two uncertainties"),
      h("dl", { class: "facts" }, sc.axes.map((a) => [h("dt", a.label), h("dd", (a.poles || []).map((p) => h("p", scrub(p.def))))]))] : null,
    sc.terms?.length ? [h("h3", `${fmt(sc.terms.length)} possible futures`),
      h("ul", { class: "c-cards c-cards--2" }, sc.terms.map((t) => h("li", h("article", { class: "c-card", "aria-labelledby": `scn-${t.code}` },
        h("h4", { class: "c-card__title", id: `scn-${t.code}` }, t.label),
        t.summary ? h("p", scrub(t.summary)) : h("p", { class: "meta" }, "No summary in this release."),
        t.risk ? h("p", h("strong", "Main risk: "), scrub(t.risk)) : null))))] : null,
    sc.noRegret?.length ? [h("h3", "Moves an AI agent judged worthwhile in every scenario (not reviewed)"),
      ui.notice("exploratory", null, core.text.noRegret),
      h("ul", { class: "c-noregret" }, sc.noRegret.map((n) => h("li", scrub(n.text))))] : null,
    sc.signposts?.length ? ui.disclosure(`Signposts we watch (${fmt(sc.signposts.length)})`, [
      h("p", "A signpost is something we keep measuring that would show which future is unfolding."),
      h("ul", { class: "task-list" }, sc.signposts.map((s) => h("li", scrub(s.text), h("p", { class: "task-list__meta" }, [s.source, s.cadence ? `checked ${s.cadence}` : null].filter(Boolean).map(scrub).join(" · ")))))]) : null,
    sc.wildcards?.length ? ui.disclosure(`Wild cards (${fmt(sc.wildcards.length)})`, [
      h("p", "Rare events that could change things quickly."),
      h("ul", { class: "task-list" }, sc.wildcards.map((w) => h("li", scrub(w.text))))]) : null,
  ];
}

// ------------------------------------------------------------------ hub
function howToRead(core) {
  return [
    h("ul", { class: "c-howto" },
      h("li", h("strong", "On watch. "), COPY.lifecycle.watch.plain),
      h("li", h("strong", "Source grade. "), `Each signal has a grade from A (strong) to D (weak). It is ${core.text.sourceGrade}.`),
      h("li", h("strong", "No forecast. "), "EMST makes no forecast. Some signals report other bodies' projections."),
      h("li", h("strong", "Change indicators. "), core.text.watchSignal)),
    ui.disclosure("What each source grade means", h("dl", { class: "facts" }, Object.entries(COPY.sourceGrade).map(([k, v]) => [h("dt", k), h("dd", v)])), { small: true }),
    h("p", h("a", { href: ui.link.key("source-grades") }, "More about these labels")),
  ];
}

function hubCard({ id, title, summary, meta, fig }) {
  const card = ui.card({ kind: "Section", title, href: `#/changing@${id}`, summary, meta,
    badges: [ui.badgeTier(fig?.tier?.t || "exploratory", { compact: true }), fig?.ev?.l ? ui.badgeEvidence(fig.ev.l, { compact: true }) : null] });
  const a = card.querySelector("a");
  a.addEventListener("click", (e) => {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    const root = a.closest(".c-changing");
    if (root && reveal(root, id)) { e.preventDefault(); st.open.add(id); focusSection(id); }
  });
  return h("li", card);
}

/** A section whose body starts collapsed (a native disclosure); its open state is kept in memory. */
function collapsible(id, title, summary, intro, body, meta) {
  const d = ui.disclosure(summary, body);
  d.classList.add("c-secbody");
  d.open = st.open.has(id);
  d.addEventListener("toggle", () => { if (d.open) st.open.add(id); else st.open.delete(id); });
  return ui.section(id, title, [intro ? h("p", intro) : null, d], { meta });
}

export async function render({ section } = {}) {
  listen();
  const [core, ch] = await Promise.all([data.core(), data.change()]);
  const p3 = p3Slugs(core);
  const roleBy = new Map(core.roles.map((r) => [r.slug, r]));
  const ctx = { core, ch, p3, roleBy };
  const ci = ch.changeIndicators || {};
  const allWatch = ch.signals.every((s) => s.status === "watch");
  const fig = ch.figures || {};

  const sig = signalsBody(ch, ctx);
  const nFam = new Set(ch.signals.map((s) => s.family)).size;
  const roles = ch.emergingRoles || [], comps = ch.emergingComps || [], watch = ch.watchItems || [];
  const sc = ch.scenarios || {};
  const withheld = ch.instrumentsWithheld?.n || 0;

  const headline = h("div", { class: "c-headline" },
    h("p", { class: "c-headline__line" }, `${plural(ch.signals.length, "signal")}${allWatch ? ", all on watch." : "."} `,
      ci.moved === 0 ? "No change indicator has moved." : `${plural(ci.moved, "change indicator")} moved.`),
    ci.n ? h("p", { class: "meta" }, `EMST checked ${plural(ci.n, "change indicator")}. ${ci.moved === 0 ? "None has" : `${fmt(ci.n - ci.moved)} have not`} enough evidence yet.`) : null,
    fig.signals ? h("p", { class: "cluster" }, ui.badgeTier(fig.signals.tier?.t || "exploratory", { compact: true }), fig.signals.ev?.l ? ui.badgeEvidence(fig.signals.ev.l, { compact: true }) : null) : null);

  const cards = h("ul", { class: "card-list c-hub" },
    hubCard({ id: "signals", title: "Signals", summary: "Evidence that some work may be changing: technology in use, staffing, job postings, plans and other bodies' projections.",
      meta: [["Signals", fmt(ch.signals.length)], ["Kinds of evidence", fmt(nFam)]], fig: fig.signals }),
    hubCard({ id: "forming", title: "Roles and competencies that may be forming", summary: "New roles, competencies and ideas that EMST is watching, each with what would show it isn't happening.",
      meta: [["Roles", fmt(roles.length)], ["Competencies", fmt(comps.length)], watch.length ? ["Ideas on watch", fmt(watch.length)] : null], fig: fig.watchItems }),
    hubCard({ id: "instruments", title: "Laws and policies", summary: "Laws, rules, court decisions and guidance that can change the work, with their status on the release date.",
      meta: [["Laws and policies", fmt(ch.instruments.length)], withheld ? ["Left out of this release", fmt(withheld)] : null], fig: fig.instruments }),
    hubCard({ id: "scenarios", title: "Scenarios", summary: "Possible futures built around two big uncertainties, and the signposts that would show which one is unfolding.",
      meta: [["Possible futures", fmt((sc.terms || []).length)], ["Signposts", fmt((sc.signposts || []).length)]] }));

  const main = [
    ui.section("overview", "Overview", [headline, cards]),
    ui.section("how-to-read", "How to read this", howToRead(core)),
    collapsible("signals", "Signals", "Show the signals", null, sig.node, plural(ch.signals.length, "signal")),
    collapsible("forming", "Roles and competencies that may be forming", "Show the roles, competencies and ideas", null, formingBody(ch, core),
      [plural(roles.length, "role"), plural(comps.length, "competency", "competencies")].join(" · ")),
    collapsible("instruments", "Laws and policies", "Show the laws and policies", null, instrumentsBody(ch, core), plural(ch.instruments.length, "item")),
    sc.terms?.length || sc.noRegret?.length ? collapsible("scenarios", "Scenarios", "Show the scenarios", null, scenariosBody(ch, core)) : null,
  ];

  const root = h("div", { class: "c-changing" },
    ui.printMeta(core, "What's changing"),
    ui.pageHeader({
      crumbs: [{ href: "#/", text: "Home" }, { text: "What's changing" }],
      kind: "Foresight, for exploring only",
      title: "What's changing",
      lede: "Early signs of how environmental work may change: new tools, rules, roles and skills. EMST makes no forecast. Some signals report other bodies' projections.",
      meta: ui.notice("exploratory", "Exploratory", ch.notice),
    }),
    h("div", { class: "page-body c-single" }, main));

  cur = { root, rowsById: sig.rowsById, revealRow: sig.revealRow };
  // A deep link opens what holds its target; the router then scrolls to it and focuses it.
  const target = section || (location.hash.includes("@") ? parseHash().section : null);
  if (target) { const el = reveal(root, target); if (el?.tagName === "SECTION") st.open.add(target); }
  return { title: "What's changing", node: root };
}
