// Shared interface components for the EMST prototype. Markup follows docs/DESIGN_SYSTEM.md; words come from content.js.
// Every function returns DOM nodes built with h() (no innerHTML). Licence: Apache-2.0.
import { h, icon, nextId, frag } from "./lib/dom.js";
import { focusSection } from "./lib/router.js";
import { COPY, GLOSSARY, fill } from "./content.js";
import { fmt, dateLong, plural } from "./lib/format.js";
import { copyText, citation, correctionTemplate, pageUrl, restrictedHost } from "./export.js";

export const ISSUES_URL = "https://github.com/jrwashebek/Enviroskillstaxonomy/issues/new/choose";
export const REPO_URL = "https://github.com/jrwashebek/Enviroskillstaxonomy";
const KEY = (anchor) => `#/about/read@${anchor}`;

// ------------------------------------------------------------------ routes
export const link = {
  role: (slug, actor) => `#/role/${slug}${actor ? "/" + actor : ""}`,
  comp: (slug) => `#/competency/${slug}`,
  task: (slug) => `#/task/${slug}`,
  series: (code) => `#/series/${code}`,
  cls: (slug) => `#/class/${slug}`,
  compare: (a, b) => `#/compare${a ? "/" + a : ""}${b ? "/" + b : ""}`,
  about: (page, anchor) => `#/about/${page}${anchor ? "@" + anchor : ""}`,
  key: KEY,
};
export function a(href, ...children) {
  const external = /^https?:/.test(href);
  return h("a", { href, rel: external ? "noopener" : null }, ...children, external ? [h("span", { class: "vh" }, " (opens another site)"), icon("external")] : null);
}

// ------------------------------------------------------------------ badges
const TIER_STEPS = { exploratory: 1, describe: 2, develop: 3, select: 4 };
export function badgeTier(t, { compact = false, linked = false } = {}) {
  const c = COPY.use?.[t] || { label: t };
  const reached = t === "exploratory" || t === "describe";
  const el = reached
    ? h("span", { class: ["badge", "tier", `tier--${t}`, compact && "badge--compact"] },
      h("span", { class: "tier__steps", "aria-hidden": "true" }, [1, 2, 3, 4].map((i) => h("i", { class: i <= TIER_STEPS[t] ? "on" : null }))),
      h("span", h("span", { class: "badge__pre" }, "Use tier "), c.label))
    : h("span", { class: ["badge", "tier", "tier--locked", compact && "badge--compact"] }, icon("lock"), h("span", `${c.label}: not yet available`));
  return linked ? h("a", { href: KEY(`use-${t}`), class: "badge-link" }, el) : el;
}
export function badgeEvidence(l, { compact = false } = {}) {
  const c = COPY.evidence?.[l] || { label: l };
  return h("span", { class: ["badge", "ev", `ev--${String(l).toLowerCase()}`, compact && "badge--compact"] },
    h("span", { class: "ev__mark", "aria-hidden": "true" }, l),
    h("span", h("span", { class: "vh" }, `Evidence label ${l}: `), c.label));
}
const LC = { established: ["badge--ok", "established"], watch: ["badge--warn", "eye"], emerging: ["badge--info", "emerging"], proposed: ["badge--info", "emerging"] };
export function badgeLifecycle(lc, { compact = false } = {}) {
  if (!lc) return null;
  const [cls, ic] = LC[lc] || ["badge--info", "info"];
  const label = COPY.lifecycle?.[lc]?.label || COPY.lifecycle?.[lc] || lc;
  return h("span", { class: ["badge", cls, compact && "badge--compact"] }, icon(ic), typeof label === "string" ? label : lc);
}
export function badgeDraft({ compact = false, v1 = false } = {}) {
  return h("span", { class: ["badge", "badge--draft", compact && "badge--compact"] }, icon("draft"), v1 ? (COPY.ai?.v1Short || "Carried over from v1, AI-assisted") : (COPY.ai?.badge || "AI-drafted, not yet reviewed"));
}
export const badgeNfd = () => h("span", { class: "badge badge--nfd" }, icon("scales"), COPY.ai?.nfd || "Not for decisions");

// ------------------------------------------------------------------ crosswalk match types
const MATCH_ICON = { exactMatch: "match-close", closeMatch: "match-close", broadMatch: "match-nested", narrowMatch: "match-nested", relatedMatch: "match-related" };
export function matchWords(row, noun = "term") {
  const m = COPY.match || {};
  if (row.none) return fill(m.none || "No matching {noun} found", { noun });
  if (row.not) return m.not || "Not a match (noted by an AI agent)";
  const p = String(row.pred || "").replace(/^.*:/, "");
  return fill(m[p] || p.replace(/Match$/, " match"), { noun });
}
export function badgeMatch(row, noun) {
  const p = String(row.pred || "").replace(/^.*:/, "");
  const ic = row.none || row.not ? "match-none" : MATCH_ICON[p] || "match-related";
  return h("span", { class: "badge match" }, icon(ic), matchWords(row, noun));
}
export function badgeUnreviewed(row) {
  const st = row?.st || "";
  const text = /two-llm/.test(st) ? `${COPY.match?.twoCoders || "Two AI coders agreed"}; not reviewed by a person`
    : /adjudication/.test(st) ? (COPY.match?.disagree || "AI coders disagreed; a person needs to decide") : (COPY.match?.unreviewed || "AI-suggested, not reviewed");
  return h("span", { class: "badge badge--draft" }, icon("unreviewed"), text);
}

/** Crosswalk rows as a plain list. linkFn(row) may return {href, text} for the external object. */
export function crosswalkList(rows, { linkFn, label, empty, noun = "term", note = true } = {}) {
  if (!rows || !rows.length) return empty ? h("p", { class: "meta" }, empty) : null;
  const ul = h("ul", { class: "xw-list stack" });
  const versions = [...new Set(rows.map((r) => r.ver).filter(Boolean))];
  for (const r of rows) {
    const target = linkFn ? linkFn(r) : null;
    const name = target ? (target.href ? a(target.href, target.text) : target.text) : (r.lab || r.obj || "");
    ul.appendChild(h("li", { class: "xw" },
      h("p", { class: "xw__name" }, name, r.lab && target && target.code ? h("span", { class: "id" }, " ", target.code) : null),
      h("p", { class: "cluster xw__badges" }, badgeMatch(r, noun), r.rev ? null : badgeUnreviewed(r)),
      r.note ? disclosure(COPY.match?.why || "Why the AI agents suggested this", h("p", clean(r.note)), { small: true }) : null));
  }
  return frag(label ? h("h3", { class: "h4" }, label) : null, ul,
    versions.length ? h("p", { class: "meta" }, `${COPY.match?.asOf || "Version of the other list"}: ${versions.map(clean).join("; ")}`) : null,
    note && COPY.match?.note ? h("p", { class: "meta" }, COPY.match.note) : null);
}

// ------------------------------------------------------------------ status line
export function statusLine(rec, { compact = false, aboutHref = null } = {}) {
  const t = rec?.tier?.t || rec?.tier || "exploratory";
  const ev = rec?.ev || {};
  const use = COPY.use?.[t] || {};
  const kids = [compact ? badgeTier(t, { linked: true }) : badgeTier(t), compact ? null : h("p", { class: "status-line__use" }, use.short || "",
    " ", h("a", { href: KEY(`use-${t}`) }, COPY.use?.examples || "What this allows")),
  h("a", { href: KEY("ai-drafted"), class: "badge-link" }, badgeDraft({ v1: !!ev.v1 })),
  rec?.lc && rec.lc !== "established" ? h("a", { href: KEY("lifecycle"), class: "badge-link" }, badgeLifecycle(rec.lc)) : null,
  aboutHref ? h("a", { href: aboutHref, class: "status-line__more", on: { click: sectionClick } }, COPY.actions?.aboutRecord || "About this record") : null];
  return h("div", { class: "status-line" }, kids);
}

// ------------------------------------------------------------------ page structure
/** crumbs: [{href, text}], last crumb without href is current */
export function pageHeader({ crumbs = [], kind, id, title, alt, lede, status, meta }) {
  return h("div", { class: "page-head" },
    crumbs.length ? h("nav", { class: "breadcrumb", "aria-label": "Breadcrumb" },
      h("ol", crumbs.map((c, i) => h("li", i === crumbs.length - 1 && !c.href ? h("span", { "aria-current": "page" }, c.text) : h("a", { href: c.href }, c.text))))) : null,
    kind || id ? h("p", { class: "page-head__kind" }, kind ? h("span", kind) : null, id ? h("span", { class: "id" }, shortId(id)) : null) : null,
    h("h1", { tabindex: "-1" }, title),
    alt && alt.length ? h("p", { class: "page-head__alt meta" }, `${COPY.site?.alsoCalled || "Also called"}: `, alt.join("; ")) : null,
    lede ? h("p", { class: "lede" }, lede) : null,
    meta || null,
    status ? h("div", { class: "page-head__status" }, status) : null);
}
export const shortId = (id) => String(id || "").replace(/^emst:[a-z]+\//, "");

export function section(id, title, children, { meta, level = 2, cls } = {}) {
  const hid = `h-${id}`;
  return h("section", { class: ["section", cls], id, "aria-labelledby": hid, tabindex: "-1" },
    h("div", { class: "section__head" }, h(`h${level}`, { id: hid }, title), meta ? h("p", { class: "meta" }, meta) : null),
    children);
}

/** Two-column page body with "On this page" in the margin. sections: [{id, title}] */
export function withMargin(sections, main) {
  return h("div", { class: "with-margin page-body" },
    h("aside", { class: "with-margin__side" }, onThisPage(sections)),
    h("div", { class: "with-margin__main" }, main));
}

function sectionClick(e) {
  const href = e.currentTarget.getAttribute("href") || "";
  const at = href.indexOf("@");
  const id = at >= 0 ? href.slice(at + 1) : href.replace(/^#/, "");
  if (document.getElementById(id)) { e.preventDefault(); focusSection(id); }
}
export function onThisPage(sections) {
  const tid = nextId("toc");
  const links = sections.filter(Boolean).map((s) => h("li", h("a", { class: "toc__link", href: `#${s.id}`, on: { click: sectionClick } }, s.title)));
  const nav = h("nav", { class: "toc", "aria-labelledby": tid }, h("h2", { class: "toc__title", id: tid }, COPY.site?.onThisPage || "On this page"), h("ol", { class: "toc__list" }, links));
  // mark the section in view; observer is created after the node is attached
  requestAnimationFrame(() => {
    if (!("IntersectionObserver" in window)) return;
    const anchors = [...nav.querySelectorAll("a")];
    const io = new IntersectionObserver((entries) => {
      for (const en of entries) if (en.isIntersecting) {
        anchors.forEach((x) => x.removeAttribute("aria-current"));
        const hit = anchors.find((x) => x.getAttribute("href") === `#${en.target.id}`);
        if (hit) hit.setAttribute("aria-current", "true");
      }
    }, { rootMargin: "-20% 0px -70% 0px" });
    sections.filter(Boolean).forEach((s) => { const el = document.getElementById(s.id); if (el) io.observe(el); });
  });
  return nav;
}

// ------------------------------------------------------------------ pending
const PENDING_WHAT = ["importance", "timeShare", "critical", "neededAtEntry", "craft", "exposure", "workFunction"];
export function pendingSummary({ what = PENDING_WHAT, assessed = 0, total, unit = "tasks" } = {}) {
  const p = COPY.pending || {};
  const names = what.map((k) => p.what?.[k] || k);
  const list = names.length > 1 ? names.slice(0, -1).join(", ") + " and " + names[names.length - 1] : names[0];
  const lead = total !== undefined ? fill(p.body || "{assessed} of {total} {unit} assessed so far. Not shown yet:", { assessed: fmt(assessed), total: fmt(total), unit }) : (p.notShown || "Not shown yet:");
  return h("div", { class: "pending pending--block" },
    h("div", { class: "pending__label" }, icon("hourglass"),
      h("div", { class: "pending__content stack-sm" },
        h("p", { class: "pending__title" }, p.title || "Assessment pending"),
        h("p", { class: "pending__text" }, `${lead} ${list}.`),
        p.why ? h("p", { class: "pending__text" }, p.why) : null,
        p.next ? h("p", { class: "pending__text" }, p.next) : null,
        h("a", { href: KEY("pending") }, p.link || "Why some values are held back"))));
}
export function pendingInline(text) {
  return h("span", { class: "pending" }, icon("hourglass"), text || COPY.pending?.inline || "Assessment pending");
}

// ------------------------------------------------------------------ evidence ladder, use-tier path, provenance
export function evidenceLadder(rec) {
  const lad = COPY.ladder || {};
  const steps = lad.steps || [
    { key: "drafted", label: "Drafted by AI agents" }, { key: "checked", label: "Automated checks passed" },
    { key: "reviewed", label: "Reviewed by practitioners" }, { key: "tested", label: "Reliability-tested" }, { key: "validated", label: "Validated for use" }];
  const ev = rec?.ev || {};
  const reviewed = ev.r && ev.r !== "unreviewed";
  const validated = ev.v === "validated";
  const doneUpTo = validated ? 4 : reviewed ? 2 : 1; // index of last done step
  const id = nextId("evl");
  return h("div", { class: "ev-ladder" },
    h("h3", { class: "ev-ladder__title", id }, lad.title || "Review path for this record"),
    h("ol", { class: "ev-ladder__steps", "aria-labelledby": id }, steps.map((s, i) => {
      const done = i <= doneUpTo, cur = i === doneUpTo + 1;
      return h("li", { class: ["ev-ladder__step", done && "is-done", cur && "is-current"], "aria-current": cur ? "step" : null },
        h("span", { class: "ev-ladder__node", "aria-hidden": "true" }, done ? icon("check") : null),
        h("span", { class: "ev-ladder__label" }, s.label, done ? h("span", { class: "vh" }, ": done") : cur ? null : h("span", { class: "vh" }, ": not yet")),
        cur ? h("span", { class: "ev-ladder__here" }, lad.nextLabel || "Next step") : null,
        s.plain ? h("span", { class: "ev-ladder__desc" }, s.plain) : null);
    })),
    lad.next ? h("p", { class: "ev-ladder__note meta" }, lad.next) : null);
}

export function useTierPath(t) {
  const id = nextId("tiers");
  const order = ["exploratory", "describe", "develop", "select"];
  const at = order.indexOf(t);
  return h("div", { class: "ev-ladder" },
    h("h3", { class: "ev-ladder__title", id }, COPY.use?.pathTitle || "What this record may be used for"),
    h("ol", { class: "ev-ladder__steps", "aria-labelledby": id }, order.map((k, i) => {
      const c = COPY.use?.[k] || { label: k };
      const locked = k === "develop" || k === "select";
      const done = !locked && i < at, cur = i === at;
      return h("li", { class: ["ev-ladder__step", done && "is-done", cur && "is-current", locked && "is-locked"], "aria-current": cur ? "step" : null },
        h("span", { class: "ev-ladder__node", "aria-hidden": "true" }, done ? icon("check") : locked ? icon("lock") : null),
        h("span", { class: "ev-ladder__label" }, c.label, done ? h("span", { class: "vh" }, ": allowed") : null),
        cur ? h("span", { class: "ev-ladder__here" }, COPY.use?.thisRecord || "This record") : null,
        h("span", { class: "ev-ladder__desc" }, c.short || "", locked ? [" ", h("b", COPY.use?.notInRelease || "Not yet available in this release.")] : null));
    })));
}

const AGENT = { ca: "chief architect", de: "data engineering", lm: "labour market", fs: "foresight", fc: "field craft", dc: "data craft", sc: "statecraft", db: "domain bench", fh: "federal human capital", sl: "state and local", ps: "private sector", io: "job analysis and validation", lc: "learning and curriculum", cm: "career mobility", ia: "interoperability", cp: "product and compliance", as: "adoption", tn: "Tribal advisory (simulated)", d: "data", wp10: "change signals" };
export function agentNames(by) {
  const ids = (Array.isArray(by) ? by : String(by || "").split(/[,;\s]+/)).filter(Boolean);
  const names = new Set();
  for (const raw of ids) {
    const parts = String(raw).toLowerCase().replace(/^emstagent:/, "").replace(/@.*/, "").split(/[-_]/);
    const hit = parts.find((x) => AGENT[x]);
    names.add(hit ? AGENT[hit] : null);
  }
  const known = [...names].filter(Boolean);
  return known.length ? `AI agents (${known.join(", ")})` : "AI agents";
}
/** Display-only cleanup of internal words that leak through free-text notes in the data. */
export function clean(text) {
  return String(text ?? "")
    .replace(/\bLLM-vs-LLM\b/g, "AI-to-AI").replace(/\bLLM[- ]assisted\b/gi, "AI-assisted").replace(/\bLLMs?\b/g, "AI")
    .replace(/\bskos:(exact|close|broad|narrow|related)Match\b/g, (_, m) => ({ exact: "exact match", close: "close match", broad: "broader match", narrow: "narrower match", related: "related match" })[m])
    .replace(/\b(close|broad|narrow|related|exact)Match\b/g, "$1 match").replace(/\braterType\b/g, "rater type").replace(/\bagentDraft\b/g, "AI draft")
    .replace(/\bsemapv:\w+/g, "").replace(/\bsssom:NoTermFound\b/g, "no matching term")
    .replace(/\bONETSOC:/g, "O*NET-SOC ").replace(/\bONETtask:/gi, "O*NET task ").replace(/\bOPMseries:/g, "OPM series ").replace(/\bESCO:/g, "ESCO ");
}
export function provenance(rec, core) {
  const ev = rec?.ev || {};
  const rows = [
    [COPY.prov?.drafted || "Drafted by", agentNames(ev.by)],
    [COPY.prov?.date || "Drafted on", ev.d ? dateLong(ev.d) : "—"],
    [COPY.prov?.evidence || "Evidence label", h("span", badgeEvidence(ev.l || "S"), " ", COPY.evidence?.[ev.l || "S"]?.plain || "")],
    [COPY.prov?.review || "Review", COPY.review?.[ev.r || "unreviewed"]?.label || "Not yet reviewed by people"],
    [COPY.prov?.sources || "Sources", ev.src && ev.src.length ? clean(ev.src.join(", ")) : (COPY.prov?.noSources || "No source cited; this is the drafting agents' judgment")],
    [COPY.prov?.id || "Record ID", h("span", { class: "id" }, rec?.id || "—")],
    [COPY.prov?.release || "Release", `${core.release.id} (${dateLong(core.release.date)})`],
  ];
  return h("dl", { class: "facts" }, rows.flatMap(([k, v]) => [h("dt", k), h("dd", v)]));
}

/** "About this record" section body: ladder, use path, provenance, actions. */
export function aboutRecord(rec, core, { title, kind, exports = [] } = {}) {
  return frag(evidenceLadder(rec), useTierPath(rec?.tier?.t || "exploratory"), provenance(rec, core), recordActions(core, { title, kind, id: rec?.id, exports }));
}

// ------------------------------------------------------------------ actions
function copyButton(label, getText, doneLabel) {
  const status = h("span", { class: "meta", role: "status", "aria-live": "polite" });
  const lab = h("span", label);
  const btn = h("button", { class: "btn btn--secondary btn--small", type: "button", on: { click: async () => {
    const ok = await copyText(getText());
    lab.textContent = ok ? (COPY.actions?.copied || "Copied") : label;
    status.textContent = ok ? doneLabel : (COPY.actions?.copyFailed || "Could not copy. Select the text and copy it yourself.");
    setTimeout(() => { lab.textContent = label; status.textContent = ""; }, 2500);
  } } }, icon("copy"), lab);
  return [btn, status];
}
/** exports: [{label, icon, onClick}] extra buttons such as "Copy tasks as text" or "Download CSV". */
export function recordActions(core, { title, kind, id, exports = [] }) {
  const citeText = citation(core, { title, kind, id });
  const citeId = nextId("cite");
  const corrText = correctionTemplate(core, { title, kind, id });
  const [citeBtn, citeStatus] = copyButton(COPY.actions?.cite || "Copy citation", () => citeText, COPY.actions?.citeDone || "Citation copied");
  const [corrBtn, corrStatus] = copyButton(COPY.actions?.copyRef || "Copy a report template", () => corrText, COPY.actions?.copyRefDone || "Report template copied. Paste it into the GitHub issue.");
  const steps = COPY.actions?.correctSteps || ["Copy the report template.", "Open GitHub Issues and choose a new issue.", "Paste the template and say what is wrong."];
  return h("div", { class: "stack record-actions" },
    h("h3", { class: "h4" }, COPY.actions?.citeTitle || "Cite this record"),
    h("figure", { class: "citation" }, h("blockquote", { class: "citation__text", id: citeId }, citeText), h("figcaption", { class: "btn-row" }, citeBtn, citeStatus)),
    h("h3", { class: "h4" }, COPY.actions?.correctTitle || "Something wrong or missing?"),
    h("ol", { class: "steps" }, steps.map((s) => h("li", s))),
    h("div", { class: "btn-row" }, corrBtn,
      h("a", { class: "btn btn--secondary btn--small", href: ISSUES_URL, rel: "noopener" }, icon("flag"), COPY.actions?.correct || "Suggest a correction", h("span", { class: "vh" }, " (opens GitHub Issues)"), icon("external")), corrStatus),
    h("p", { class: "meta" }, COPY.actions?.githubNote || "Opens GitHub Issues. You need a free GitHub account. Please do not include personal information."),
    h("div", { class: "btn-row no-print" },
      restrictedHost() ? null : h("button", { class: "btn btn--secondary btn--small", type: "button", on: { click: () => window.print() } }, icon("print"), COPY.actions?.print || "Print"),
      exports.map((x) => {
        const blocked = restrictedHost() && (x.icon || "download") === "download";
        const label = blocked ? String(x.label).replace(/^Download\s+/i, "Copy ") + " to the clipboard" : x.label;
        const st = h("span", { class: "meta", role: "status", "aria-live": "polite" });
        const btn = h("button", { class: "btn btn--secondary btn--small", type: "button", on: { click: async (ev) => {
          const r = await x.onClick(ev);
          if (blocked) st.textContent = r === "failed" ? (COPY.actions?.copyFailed || "Could not copy.") : (COPY.actions?.copied || "Copied") + ". Paste it into a spreadsheet or text file.";
        } } }, icon(blocked ? "copy" : (x.icon || "download")), label);
        return [btn, st];
      })),
    restrictedHost() ? h("p", { class: "meta" }, "In this preview, files and printing are turned off by the host, so exports copy to your clipboard.") : null);
}

// ------------------------------------------------------------------ levels
export function levelChip(code, core) {
  if (!code) return null;
  const name = core?.labels?.level?.[code] || (code === "A" ? "Awareness" : "");
  return h("span", { class: "badge level-chip" }, h("span", { class: "level-chip__code" }, code), name);
}
/** levels: [{level, label, indicators[]}]; span: [min,max]; target: {level, text} */
export function levelLadder(levels, { span, target, core, titleId } = {}) {
  const all = ["L1", "L2", "L3", "L4", "L5"];
  const lo = span ? all.indexOf(span[0]) : 0, hi = span ? all.indexOf(span[1]) : 4;
  const by = Object.fromEntries((levels || []).map((l) => [l.level, l]));
  const desc = core?.labels?.levelDescriptors || {};
  return h("ol", { class: "levels", "aria-labelledby": titleId || null }, all.map((code, i) => {
    const l = by[code];
    const name = l?.label || core?.labels?.level?.[code] || code;
    const inSpan = i >= lo && i <= hi;
    const isTarget = target && target.level === code;
    const d = desc[code];
    const dtext = Array.isArray(d) ? d.join(" ") : typeof d === "object" && d ? Object.values(d).join(" ") : d;
    return h("li", { class: ["level", isTarget && "is-target", !inSpan && "is-undefined"] },
      h("div", { class: "level__rung", "aria-hidden": "true" }, code),
      h("div", { class: "level__body" },
        isTarget ? h("p", { class: "level__target" }, icon("target"), target.text) : null,
        h("h4", { class: "level__name" }, h("span", { class: "vh" }, `Level ${i + 1}: `), name),
        inSpan && dtext ? h("p", { class: "level__desc" }, dtext) : null,
        !inSpan ? h("p", { class: "level__none" }, COPY.levels?.none || "Not defined for this competency.") :
          l && l.indicators?.length ? h("ul", { class: "level__indicators" }, l.indicators.map((ind) => h("li", ind.stmt, ind.attr ? h("span", { class: "meta" }, ` (${COPY.levels?.distinguished || "distinguished by"} ${ind.attr})`) : null))) : null));
  }));
}

// ------------------------------------------------------------------ notices, disclosure, tabs
const NOTICE = { info: ["notice--info", "info"], caution: ["notice--warn", "alert"], hr: ["notice--use", "scales"], use: ["notice--use", "scales"], exploratory: ["notice--draft", "route"], draft: ["notice--draft", "draft"], held: ["notice--hold", null] };
export function notice(kind, title, ...body) {
  const [cls, ic] = NOTICE[kind] || NOTICE.info;
  return h("div", { class: ["notice", cls], role: "note" }, ic ? h("span", { class: "notice__icon" }, icon(ic)) : null,
    h("div", { class: "notice__body" }, title ? h("h3", { class: "notice__title" }, title) : null,
      body.flat().map((b) => (typeof b === "string" ? h("p", b) : b))));
}
export function disclosure(summary, body, { open = false, badge = null, small = false } = {}) {
  return h("details", { class: ["drawer", small && "drawer--small"], open },
    h("summary", { class: "drawer__summary" }, icon("chevron-down"), h("span", { class: "drawer__title" }, summary), badge),
    h("div", { class: "drawer__body" }, body));
}

/** items: [{key, label, count, render: () => Node}] — panels render lazily on first selection. */
export function tabs(items, { label, labelledBy, selected, onSelect } = {}) {
  const base = nextId("tabs");
  let current = Math.max(0, items.findIndex((x) => x.key === selected));
  const list = h("div", { class: "tabs__list", role: "tablist", "aria-label": labelledBy ? null : label, "aria-labelledby": labelledBy || null });
  const panels = [], btns = [];
  items.forEach((it, i) => {
    const tid = `${base}-t${i}`, pid = `${base}-p${i}`;
    const b = h("button", { class: "tabs__tab", type: "button", role: "tab", id: tid, "aria-controls": pid, "aria-selected": "false", tabindex: "-1" },
      it.label, it.count !== undefined ? h("span", { class: "tabs__count" }, String(it.count)) : null);
    const p = h("section", { class: "tabs__panel", role: "tabpanel", id: pid, "aria-labelledby": tid, tabindex: "0", hidden: true });
    b.addEventListener("click", () => select(i, false));
    b.addEventListener("keydown", (e) => {
      const n = items.length;
      const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
      if (k) { e.preventDefault(); select((current + k + n) % n, true); }
      else if (e.key === "Home") { e.preventDefault(); select(0, true); }
      else if (e.key === "End") { e.preventDefault(); select(n - 1, true); }
    });
    btns.push(b); panels.push(p); list.appendChild(b);
  });
  function select(i, focus) {
    current = i;
    btns.forEach((b, j) => { b.setAttribute("aria-selected", j === i ? "true" : "false"); b.setAttribute("tabindex", j === i ? "0" : "-1"); });
    panels.forEach((p, j) => { p.hidden = j !== i; });
    if (!panels[i].dataset.rendered) { panels[i].appendChild(items[i].render()); panels[i].dataset.rendered = "1"; }
    if (focus) btns[i].focus();
    onSelect?.(items[i].key);
  }
  const root = h("div", { class: "tabs" }, list, panels);
  if (items.length) select(current, false);
  return root;
}

// ------------------------------------------------------------------ filters
/** options: [{value, label, count}]; returns {node, values():Set, set(values)} */
export function chipGroup({ legend, name, options, multi = true, checked = [], onChange }) {
  const fs = h("fieldset", { class: "facet" }, h("legend", { class: "facet__legend" }, legend));
  const wrap = h("div", { class: "chips" });
  const inputs = [];
  for (const o of options) {
    const inp = h("input", { class: "chip__input", type: multi ? "checkbox" : "radio", name, value: o.value, checked: checked.includes(o.value) });
    inp.addEventListener("change", () => onChange?.(values()));
    inputs.push(inp);
    wrap.appendChild(h("label", { class: "chip" }, inp, h("span", { class: "chip__face" }, icon("check"), o.label, o.count !== undefined ? h("span", { class: "chip__count" }, fmt(o.count)) : null)));
  }
  fs.appendChild(wrap);
  const values = () => new Set(inputs.filter((i) => i.checked).map((i) => i.value));
  const set = (vals) => { inputs.forEach((i) => { i.checked = vals.has(i.value); }); };
  const counts = (map) => { inputs.forEach((i) => { const c = i.parentElement.querySelector(".chip__count"); if (c && map[i.value] !== undefined) c.textContent = fmt(map[i.value]); }); };
  return { node: fs, values, set, counts };
}
export function liveCount() {
  const el = h("p", { class: "result-bar__count", role: "status", "aria-live": "polite" });
  let t;
  return { node: el, set: (text) => { clearTimeout(t); t = setTimeout(() => { el.textContent = text; }, 250); } };
}

// ------------------------------------------------------------------ cards, empty, figures
export function card({ kind, id, title, href, summary, meta = [], badges = [], comp = false, headingLevel = 3 }) {
  return h("article", { class: ["card", comp && "card--comp"] },
    h("p", { class: "card__kind" }, h("span", kind), id ? h("span", { class: "id" }, shortId(id)) : null),
    h(`h${headingLevel}`, { class: "card__title h4" }, h("a", { class: "card__link", href }, title)),
    summary ? h("p", { class: "card__summary" }, summary) : null,
    meta.length ? h("dl", { class: "card__meta" }, meta.filter(Boolean).map(([k, v]) => h("div", h("dt", k), h("dd", v)))) : null,
    badges.filter(Boolean).length ? h("div", { class: "card__badges cluster" }, badges) : null);
}
export function emptyState({ title, body, actions = [], iconName = "filter" }) {
  return h("div", { class: "empty" }, h("span", { class: "empty__icon", "aria-hidden": "true" }, icon(iconName)),
    h("h3", { class: "empty__title h4" }, title), body ? (typeof body === "string" ? h("p", body) : body) : null,
    actions.length ? h("div", { class: "btn-row" }, actions) : null);
}
/** A headline number with its compact tier and evidence badges (spec: every figure carries badges). */
export function figure(n, label, fig) {
  return h("li", { class: "panel fig" }, h("p", { class: "fig__n num" }, fmt(n)), h("p", { class: "fig__label" }, label),
    fig ? h("p", { class: "cluster" }, fig.tier ? badgeTier(fig.tier.t || fig.tier.tier || fig.tier, { compact: true }) : null, fig.ev?.l ? badgeEvidence(fig.ev.l, { compact: true }) : null) : null);
}

// ------------------------------------------------------------------ sortable table
/** columns: [{key, label, num, sort: (row)=>value, render: (row)=>Node|string, rowHeader}] */
export function table({ caption, hint, columns, rows, sticky = true, sortBy = null, dir = 1, limit = null, moreLabel }) {
  const capId = nextId("cap");
  const tbody = h("tbody");
  const thead = h("thead");
  const headRow = h("tr");
  let sortKey = sortBy, sortDir = dir, showAll = !limit;
  const hintEl = h("span", { class: "data-table__hint" });
  const ths = columns.map((c) => {
    if (!c.sort) return h("th", { scope: "col", class: c.num ? "num" : null }, c.label);
    const ic = icon("sort");
    const btn = h("button", { class: "sort", type: "button" }, c.label, ic);
    const th = h("th", { scope: "col", class: ["is-sortable", c.num && "num"] }, btn);
    btn.addEventListener("click", () => { if (sortKey === c.key) sortDir = -sortDir; else { sortKey = c.key; sortDir = c.num ? -1 : 1; } draw(); });
    th._col = c; th._ic = ic;
    return th;
  });
  ths.forEach((t) => headRow.appendChild(t));
  thead.appendChild(headRow);
  const more = limit ? h("button", { class: "btn btn--tertiary btn--small", type: "button", on: { click: () => { showAll = !showAll; draw(); } } }) : null;
  function draw() {
    let data = rows.slice();
    const col = columns.find((c) => c.key === sortKey);
    if (col?.sort) data.sort((x, y) => { const p = col.sort(x), q = col.sort(y); return (p < q ? -1 : p > q ? 1 : 0) * sortDir; });
    ths.forEach((th) => {
      if (!th._col) return;
      const on = th._col.key === sortKey;
      if (on) th.setAttribute("aria-sort", sortDir === 1 ? "ascending" : "descending"); else th.removeAttribute("aria-sort");
      th._ic.querySelector("use").setAttribute("href", `assets/icons.svg#${on ? (sortDir === 1 ? "sort-asc" : "sort-desc") : "sort"}`);
    });
    const shown = showAll || !limit ? data : data.slice(0, limit);
    tbody.replaceChildren(...shown.map((r) => h("tr", columns.map((c, i) => {
      const v = c.render ? c.render(r) : r[c.key];
      return c.rowHeader || (i === 0 && c.rowHeader !== false) ? h("th", { scope: "row", class: c.num ? "num" : null }, v) : h("td", { class: c.num ? "num" : null }, v);
    }))));
    hintEl.textContent = [hint, limit && !showAll ? `First ${fmt(limit)} of ${fmt(rows.length)}.` : null, col ? `Sorted by ${col.label.toLowerCase()}.` : (columns.some((c) => c.sort) ? "Select a column heading to sort." : null)].filter(Boolean).join(" ");
    if (more) { more.textContent = showAll ? (COPY.actions?.showFewer || "Show fewer") : `${COPY.actions?.showAll || "Show all"} ${fmt(rows.length)}`; more.hidden = rows.length <= limit; }
  }
  draw();
  return h("div", { class: "stack" },
    h("div", { class: "table-scroll", role: "region", "aria-labelledby": capId, tabindex: "0" },
      h("table", { class: ["data-table", sticky && "data-table--sticky"] }, h("caption", { id: capId }, caption, hintEl), thead, tbody)),
    more);
}

// ------------------------------------------------------------------ jargon
/** Expand known acronyms on first use per page: returns nodes with <abbr title> plus the expansion in text the first time. */
export function jargon(text, seen = new Set()) {
  const terms = Object.keys(GLOSSARY || {});
  if (!terms.length) return [text];
  const rx = new RegExp(`\\b(${terms.map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).sort((x, y) => y.length - x.length).join("|")})\\b`, "g");
  const out = [];
  let last = 0, m;
  while ((m = rx.exec(text))) {
    const t = m[1], g = GLOSSARY[t];
    out.push(text.slice(last, m.index));
    if (!seen.has(t) && g?.exp) { seen.add(t); out.push(h("abbr", { title: g.exp }, t), ` (${g.exp})`); }
    else out.push(g?.exp ? h("abbr", { title: g.exp }, t) : t);
    last = m.index + t.length;
  }
  out.push(text.slice(last));
  return out;
}

// ------------------------------------------------------------------ about-page blocks
/** Text with [label](href) links turned into anchors; everything else stays text. */
export function rich(text) {
  const out = [];
  const rx = /\[([^\]]+)\]\(([^)\s]+)\)/g;
  let last = 0, m;
  const s = String(text ?? "");
  while ((m = rx.exec(s))) {
    out.push(s.slice(last, m.index));
    const href = m[2];
    out.push(/^(#|https:\/\/)/.test(href) ? a(href, m[1]) : m[1]);
    last = m.index + m[0].length;
  }
  out.push(s.slice(last));
  return out;
}
export function blocks(list = []) {
  return list.map((b) => {
    switch (b.t) {
      case "h2": return h("h2", { id: b.id || null, tabindex: b.id ? "-1" : null }, b.text);
      case "h3": return h("h3", { id: b.id || null }, b.text);
      case "p": return h("p", rich(b.text));
      case "ul": return h("ul", (b.items || []).map((x) => h("li", rich(x))));
      case "ol": return h("ol", (b.items || []).map((x) => h("li", rich(x))));
      case "dl": return h("dl", { class: "facts" }, (b.items || []).flatMap(([k, v]) => [h("dt", k), h("dd", rich(v))]));
      case "notice": return notice(b.kind || "info", b.title, h("p", rich(b.text)));
      case "example": return h("p", { class: "example" }, h("strong", `${b.label}: `), rich(b.text));
      case "link": return h("p", a(b.href, b.text));
      default: return b.text ? h("p", rich(b.text)) : null;
    }
  });
}

// ------------------------------------------------------------------ print block
export function printMeta(core, title) {
  return h("div", { class: "print-only print-meta" },
    h("p", `EMST release ${core.release.id} (${dateLong(core.release.date)}). Printed from ${title}: ${pageUrl()}`),
    h("p", COPY.site?.printNote || "Drafted by AI agents and not yet reviewed by a person. Not for selection, classification or performance decisions."));
}

export { plural, fmt, dateLong };
