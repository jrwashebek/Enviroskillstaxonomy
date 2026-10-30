// Search results (#/search). Owner: developer A. Spec: docs/DESIGN_SPEC.md §2.3. Licence: Apache-2.0.
// The query lives only in memory (state.query); it never enters the URL. Results are grouped by kind and each one
// says why it matched. Zero and near-zero answers are honest and offer next steps.
import { h, icon } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { state } from "../lib/state.js";
import { refresh } from "../lib/router.js";
import { fullIndex, KIND_LABEL, KIND_ORDER, hrefFor } from "../lib/searchsvc.js";
import { normalize, stem, segments } from "../lib/search.js";
import { COPY, fill } from "../content.js";
import { pageHeader, notice, onThisPage, jargon, clean, fmt } from "../ui.js";
import { truncate, cap } from "../lib/format.js";

const EXAMPLES = ["forestry technician", "Rx burn", "0460"];
// Same stop words and tokenizer as lib/search.js, so "why this matched" agrees with the ranking.
const STOP = new Set("a an and are as at be by for from in into is it its my of on or our that the their this to with we you your i me what how do does job jobs work".split(" "));
const words = (s) => normalize(s).split(/\s+/).flatMap((w) => (/^[a-z]+-[a-z]+$/.test(w) ? [w, ...w.split("-")] : [w])).filter((w) => w && !STOP.has(w));
const codeKey = (s) => String(s || "").toLowerCase().replace(/^gs[\s-]*/, "").replace(/[^a-z0-9]/g, "");
// Record text is generated; the shared clean() rewrites internal words that must not appear on screen.
const plain = (s) => clean(s);

const ONE = { role: "Role", series: "OPM series", class: "State or local job class", comp: "Competency", task: "Task", module: "Module", tool: "Tool", credential: "Credential that may be involved", signal: "Change signal, on watch", emerging: "Emerging role" };
const MANY = { role: "roles", series: "OPM series", class: "state and local classes", comp: "competencies", task: "tasks", module: "modules", tool: "tools", credential: "credentials", signal: "change signals", emerging: "emerging roles" };
const GROUP_ORDER = [...KIND_ORDER, "emerging"];
const GROUP_LABEL = { ...KIND_LABEL, emerging: "Emerging roles (in What's changing)" };
const LIMIT = { role: 8 };

// ------------------------------------------------------------------ running a search (memory only)
async function runSearch(q) {
  state.query = q;
  const header = document.getElementById("q");
  if (header) header.value = q;
  await refresh();
  // refresh() re-renders without moving focus; put it on the result summary so the new count is read out.
  document.getElementById("search-summary")?.focus();
}
const searchButton = (term, cls = "chip-btn") => h("button", { class: cls, type: "button", on: { click: () => runSearch(term) } }, icon("search"), term);

function pageSearch(q) {
  const input = h("input", { class: "search__input", id: "q-page", type: "search", value: q, autocomplete: "off", spellcheck: "false" });
  const form = h("form", { class: "search search--page", role: "search", "aria-label": "Search again", novalidate: true },
    h("label", { class: "search__label", for: "q-page" }, "Search job titles, tasks, skills and codes"),
    h("div", { class: "search__row" }, h("div", { class: "combobox" }, input), h("button", { class: "search__btn", type: "submit" }, icon("search"), h("span", "Search"))));
  form.addEventListener("submit", (e) => { e.preventDefault(); const v = input.value.trim(); if (v) runSearch(v); else input.focus(); });
  return form;
}

// ------------------------------------------------------------------ why this matched
/** Words of `term` found in `text` (exact, same stem, or as the start of a word of 3+ letters). Returns the text's words or null. */
function termIn(term, text) {
  const ws = words(term);
  if (!ws.length || !text) return null;
  const toks = words(text);
  const got = [];
  for (const w of ws) {
    const sw = stem(w);
    const t = toks.find((x) => x === w || stem(x) === sw || (w.length >= 3 && (x.startsWith(w) || x.startsWith(sw))));
    if (!t) return null;
    got.push(t);
  }
  return got;
}
/** Unique words, dropping the parts of a hyphenated word that is also listed ("ai-assisted", not also "ai", "assisted"). */
const tidy = (list) => { const u = [...new Set(list)]; return u.filter((x) => !u.some((y) => y !== x && y.includes("-") && y.split("-").includes(x))); };
const hasToken = (text, tok) => words(text).some((x) => x === tok || stem(x) === tok);

function codeReason(d, code) {
  if (d.k === "series") return `OPM series code ${code}`;
  if (d.k === "class") return `Class code ${code}`;
  if (d.k === "comp") return `Code from EMST version 1: ${code}`;
  if (d.k === "module") return `Module code ${code}`;
  if (d.k === "role") {
    const what = /^\d{4}$/.test(code) ? `OPM series ${code}` : /^\d{2}-\d{4}\.\d{2}$/.test(code) ? `O*NET code ${code}` : /^SOC/.test(code) ? `SOC code ${code.replace(/^SOC\d*:/, "")}` : `class code ${code}`;
    return `Linked to ${what} (AI-suggested link, not reviewed)`;
  }
  return `Code ${code}`;
}

/** Reasons a document matched, and the title words to mark. */
function whyMatched(r, q, plan, spelling) {
  const d = r.doc, reasons = [], marks = [], titleWords = [], ctxWords = [];
  const where = d.k === "task" ? "its competency" : "the summary";
  const add = (s) => { if (s && !reasons.includes(s)) reasons.push(s); };
  const qk = codeKey(q);
  const code = qk.length >= 3 && /\d/.test(qk) ? (d.c || []).find((c) => codeKey(c) === qk) : null;
  if (code) add(codeReason(d, code));
  let matchedGroups = 0;
  for (const g of plan.groups) {
    let hit = false;
    g.terms.forEach((term, i) => {
      if (hit) return;
      const syn = i > 0 ? `Synonym: ${g.label} → ${plain(term)}` : null;
      const tw = termIn(term, d.t);
      if (tw) { hit = true; marks.push(...tw); if (syn) add(syn); else titleWords.push(...tw); return; }
      const alt = (d.a || []).find((a) => termIn(term, a));
      if (alt) { hit = true; add(`Also called: ${plain(alt)}`); add(syn); return; }
      const tk = codeKey(term);
      const cd = (d.c || []).find((c) => (tk && /\d/.test(tk) && codeKey(c) === tk) || termIn(term, c));
      if (cd) { hit = true; add(codeReason(d, cd)); add(syn); return; }
      const xw = termIn(term, d.x);
      if (xw) { hit = true; if (syn) add(`${syn} (in ${where})`); else ctxWords.push(...xw); return; }
      // The index matches a phrase across fields (one word in the title, another in the summary).
      const all = termIn(term, [d.t, ...(d.a || []), d.x].join(" "));
      if (all) {
        hit = true;
        const inTitle = all.filter((t) => hasToken(d.t, t) || words(d.t).includes(t));
        marks.push(...inTitle);
        add(syn ? `${syn} (in the title and ${where})` : `Words in the title and ${where}: ${tidy(all).join(", ")}`);
      }
    });
    if (!hit) {
      const from = words(g.terms[0]);
      // Every close spelling the index used, not only the one named in the note.
      for (const s of spelling.filter((x) => from.includes(x.from))) {
        for (const to of s.all || [s.to]) {
          if (hit) break;
          if ([d.t, ...(d.a || []), d.x].some((t) => hasToken(t, to))) { hit = true; add(`Spelling: ${to}`); if (hasToken(d.t, to)) marks.push(to); }
        }
      }
    }
    if (hit) matchedGroups++;
  }
  const tw = tidy(titleWords).filter((w) => !(code && codeKey(w) === qk));
  if (tw.length) add(`Words in the title: ${tw.join(", ")}`);
  if (ctxWords.length) add(`Words in ${where}: ${tidy(ctxWords).join(", ")}`);
  if (!r.complete && !code) reasons.unshift(matchedGroups ? "Matches only some of your words" : "Close to your words");
  if (!reasons.length) reasons.push("Close to your words");
  const spell = (x) => clean(x).replace(/\bllms?\b/gi, "AI");
  return { reasons: reasons.map(spell), marks: marks.map(spell) };
}

// ------------------------------------------------------------------ result rows
function context(kind, d, core, roleBy, compBy) {
  const x = plain(d.x || "");
  switch (kind) {
    case "role": { const r = roleBy.get(d.s); return r ? `${r.depth === "P1" ? "Full profile" : "Starter profile"}. ${truncate(plain(r.fn), 150)}` : x; }
    case "emerging": { const r = roleBy.get(d.s); return `Shown only in What's changing, because the work is not yet shown to exist. ${truncate(plain(r?.fn || ""), 110)}`; }
    case "comp": {
      const c = compBy.get(d.s);
      if (!c) return x;
      const mod = c.module && c.module !== "core" ? `${core.labels.module?.[c.module] || c.module} module` : "Core";
      const lv = (s) => (s === "A" ? "Awareness" : s);
      return `${mod} · Levels ${lv(c.span[0])} to ${lv(c.span[1])} · ${truncate(plain(c.stmt || ""), 110)}`;
    }
    case "task": return `Competency: ${x.replace(/^Task\s*·\s*/, "")}`;
    case "series": return cap(x.replace(/^Federal series\s*·\s*/, ""));
    case "tool": return x.replace(/^Tool \([^)]*\)\s*·\s*/, "");
    case "credential": return x.replace(/^Credential that may be involved\s*/, "").replace(/^\((.*?)\)\s*·?\s*/, (m, a) => `${cap(a)}. `);
    case "signal": return x.replace(/^Watch signal\s*·\s*/, "");
    case "module": return x.replace(/^Module editorial section\s*·\s*/, "");
    default: return x;
  }
}

function resultItem(kind, r, ctx) {
  const d = r.doc;
  const href = kind === "emerging" ? `#/changing@${d.s}` : hrefFor(d);
  const { reasons, marks } = whyMatched(r, ctx.q, ctx.plan, ctx.spelling);
  const title = plain(d.t);
  const segs = marks.length ? segments(title, marks.join(" ")) : [{ text: title, mark: false }];
  return h("li", { class: "result" },
    h("p", { class: "result__title" }, h("a", { href }, segs.map((s) => (s.mark ? h("mark", s.text) : s.text)))),
    h("p", { class: "result__ctx" }, h("span", { class: "result__kind" }, ONE[kind]), " · ", context(kind, d, ctx.core, ctx.roleBy, ctx.compBy)),
    h("p", { class: "result__why" }, h("span", { class: "result__why-label" }, "Why it matched: "), reasons.slice(0, 2).join(" · ")));
}

function groupNode(kind, items, ctx, prefix = "") {
  const id = `res-${prefix}${kind}`, n = items.length, lim = LIMIT[kind] || 5;
  const ul = h("ul", { class: "result-list" });
  const addRange = (from, to) => items.slice(from, to).forEach((r) => ul.appendChild(resultItem(kind, r, ctx)));
  addRange(0, lim);
  const meta = h("p", { class: "meta" }, n > lim ? `${fmt(lim)} of ${fmt(n)} shown` : `${fmt(n)} ${n === 1 ? "result" : "results"}`);
  let more = null;
  if (n > lim) {
    more = h("button", { class: "btn btn--secondary btn--small", type: "button", on: { click: () => {
      const first = ul.children.length;
      addRange(lim, n);
      meta.textContent = `${fmt(n)} results`;
      more.remove();
      ul.children[first]?.querySelector("a")?.focus();
    } } }, `Show all ${fmt(n)} ${MANY[kind]}`);
  }
  return h("section", { class: "result-group", id, "aria-labelledby": `h-${id}`, tabindex: "-1" },
    h("div", { class: "section__head" }, h(prefix ? "h3" : "h2", { class: "h3", id: `h-${id}` }, GROUP_LABEL[kind]), meta), ul, more);
}

// ------------------------------------------------------------------ notes, zero results
function notesNode(notes, spelling) {
  const items = [];
  let syn = false;
  const quoteList = (xs) => { const q = xs.map((x) => `“${x}”`); return q.length > 1 ? `${q.slice(0, -1).join(", ")} and ${q[q.length - 1]}` : q[0]; };
  for (const s of spelling) {
    const all = (s.all || [s.to]).slice(0, 4);
    items.push(`Spelling: also searched for ${quoteList(all)}, ${all.length > 1 ? "close spellings" : "a close spelling"} of “${s.from}”.`);
  }
  for (const n of notes || []) {
    if (n.type === "synonym") {
      syn = true;
      items.push(`Other words: also searched for ${quoteList((n.to || []).map(plain))}, for “${n.from}”.`);
    }
  }
  if (!items.length) return null;
  return notice("info", null, h("ul", { class: "search-notes__list" }, items.map((t) => h("li", t))),
    syn ? h("p", { class: "meta" }, "The list of other words is a draft made for this prototype. No practitioner has checked it.") : null);
}

/** Related searches for a query with no (or only partial) results: single words that work, close spellings and prefixes. */
function related(ix, q) {
  const ws = [...new Set(words(q))].filter((w) => w.length >= 3);
  const cand = new Map();
  const df = (t) => ix.post.get(t)?.size || 0;
  const put = (t, score) => { if (/^[a-z][a-z-]{2,}$/.test(t) && score > (cand.get(t) || 0)) cand.set(t, score); };
  for (const w of ws) {
    if (ws.length > 1) put(w, 3000 + Math.min(df(w), 99));
    for (const [v, d] of ix.fuzzy(w)) if (v !== w) put(v, 2000 - d * 100 + Math.min(df(v), 99));
    for (let n = Math.min(w.length - 1, 8); n >= Math.max(4, Math.ceil(w.length * 0.75)); n--) {
      const toks = ix.prefixed(w.slice(0, n), 400).filter((t) => t !== w && t.length >= 4 && stem(t) === t);
      if (toks.length) { toks.forEach((t) => put(t, n * 10 + Math.min(df(t), 9))); break; }
    }
  }
  const out = [], stems = new Set();
  for (const [t] of [...cand].sort((a, b) => b[1] - a[1])) {
    if (out.length >= 5) break;
    if (stems.has(stem(t)) || normalize(q) === t) continue;
    if (!ix.search(t, { limit: 3 }).results.some((r) => r.complete)) continue;
    stems.add(stem(t)); out.push(t);
  }
  return out;
}

function zeroNode(q, ix, partial) {
  const z = COPY.zero;
  const sugg = related(ix, q);
  const browse = [["#/roles", "All roles"], ["#/competencies", "All competencies"], ["#/series", "Federal job series"], ["#/classes", "State and local job classes"], ["#/changing", "What's changing"]];
  return h("div", { class: "empty zero" },
    h("span", { class: "empty__icon", "aria-hidden": "true" }, icon("search")),
    h("h2", { class: "empty__title h3", id: "search-summary", tabindex: "-1" }, partial ? `No results match all the words in “${q}”` : fill(z.title, { q })),
    h("p", partial ? `The ${fmt(partial)} ${partial === 1 ? "result" : "results"} below match only some of your words. ${z.body}` : z.body),
    h("h3", { class: "h4" }, sugg.length ? z.tryTitle : "Try an example"),
    h("ul", { class: "example-chips" }, (sugg.length ? sugg : EXAMPLES).map((t) => h("li", searchButton(t)))),
    h("h3", { class: "h4" }, z.browseTitle),
    h("ul", { class: "zero__browse" }, browse.map(([href, label]) => h("li", h("a", { href }, label)))),
    h("p", h("a", { class: "arrow-link", href: "#/about/corrections@corr-missing" }, icon("flag"), z.suggest, icon("arrow-right"))),
    h("p", { class: "meta" }, "That page shows your search words so you can copy them into your suggestion."));
}

// ------------------------------------------------------------------ view
export async function render() {
  const [core, ix] = await Promise.all([data.core(), fullIndex()]);
  const q = String(state.query || "").trim();
  const header = document.getElementById("q");
  if (header && document.activeElement !== header && header.value.trim() !== q) header.value = q;
  const head = pageHeader({ crumbs: [{ href: "#/", text: "Home" }, { text: "Search results" }], title: "Search results" });

  if (!q) {
    return { title: "Search results", node: h("div", head, h("div", { class: "page-body stack search-page" }, pageSearch(""),
      h("p", "Type a job title, a task, a skill or a code such as 0460. What you type stays on your device and is never added to the page address."),
      h("p", { class: "meta", id: "ex-label" }, "Or try an example:"),
      h("ul", { class: "example-chips", "aria-labelledby": "ex-label" }, EXAMPLES.map((t) => h("li", searchButton(t)))))) };
  }

  const res = ix.search(q, { limit: 10000 });
  const plan = ix.plan(q);
  const spelling = (res.notes || []).filter((n) => n.type === "spelling").flatMap((n) => n.items || [])
    .map((s) => ({ ...s, all: [s.to, ...ix.fuzzy(s.from).map(([v]) => v).filter((v) => v !== s.to)] }));
  const roleBy = new Map(core.roles.map((r) => [r.slug, r]));
  const compBy = new Map(core.comps.map((c) => [c.slug, c]));
  const ctx = { q, plan, spelling, core, roleBy, compBy };

  // Results that match every word come first, grouped by kind. Results that match only some words follow in their
  // own section, so a partial match never sits above a full one.
  const kindOf = (r) => (r.doc.k === "role" && roleBy.get(r.doc.s)?.whatsComingOnly ? "emerging" : r.doc.k);
  const groupBy = (rs) => { const m = new Map(); for (const r of rs) { const k = kindOf(r); if (!m.has(k)) m.set(k, []); m.get(k).push(r); } return m; };
  const full = groupBy(res.results.filter((r) => r.complete));
  const part = groupBy(res.results.filter((r) => !r.complete));
  const fullKinds = GROUP_ORDER.filter((k) => full.has(k)), partKinds = GROUP_ORDER.filter((k) => part.has(k));
  const nFull = res.results.filter((r) => r.complete).length, nPart = res.results.length - nFull;

  let hrShown = false;
  const hrNotice = (k) => {
    if ((k !== "series" && k !== "class") || hrShown) return null;
    hrShown = true;
    const seen = new Set();
    return notice("hr", "About federal series and state classes", (core.text.hrDisclaimer || []).map((t) => h("p", jargon(t, seen))));
  };
  const groupsOf = (map, kinds, prefix) => kinds.flatMap((k) => [hrNotice(k), groupNode(k, map.get(k), ctx, prefix)]);

  // The summary takes focus after a new search. With no full matches, the zero-results heading is the summary.
  const summary = nFull ? h("p", { class: "search-summary", id: "search-summary", tabindex: "-1" },
    `${fmt(nFull)} ${nFull === 1 ? "result" : "results"} for “${q}”`,
    fullKinds.length > 1 ? h("span", { class: "meta" }, ` (${fullKinds.map((k) => `${MANY[k]} ${fmt(full.get(k).length)}`).join(", ")})`) : null) : null;

  const partSection = nPart ? h("section", { class: "result-part", id: "res-part", "aria-labelledby": "h-res-part", tabindex: "-1" },
    nFull ? h("div", { class: "section__head" }, h("h2", { id: "h-res-part" }, "Matching only some of your words"), h("p", { class: "meta" }, `${fmt(nPart)} ${nPart === 1 ? "result" : "results"}`))
      : h("h2", { class: "vh", id: "h-res-part" }, "Results that match some of your words"),
    h("div", { class: "result-groups" }, groupsOf(part, partKinds, "part-"))) : null;

  const main = h("div", { class: "stack-lg search-page" },
    pageSearch(q),
    notesNode(res.notes, spelling),
    summary,
    !res.total ? zeroNode(q, ix, 0) : !nFull ? zeroNode(q, ix, nPart) : null,
    nFull ? h("div", { class: "result-groups" }, groupsOf(full, fullKinds, "")) : null,
    partSection);

  const toc = [...fullKinds.map((k) => ({ id: `res-${k}`, title: `${GROUP_LABEL[k]} (${fmt(full.get(k).length)})` })),
    ...(nPart && nFull ? [{ id: "res-part", title: `Matching only some of your words (${fmt(nPart)})` }] : !nFull ? partKinds.map((k) => ({ id: `res-part-${k}`, title: `${GROUP_LABEL[k]} (${fmt(part.get(k).length)})` })) : [])];
  const body = toc.length > 1 ? h("div", { class: "with-margin page-body" },
    h("aside", { class: "with-margin__side" }, onThisPage(toc)), h("div", { class: "with-margin__main" }, main))
    : h("div", { class: "page-body" }, main);
  return { title: "Search results", node: h("div", head, body) };
}
