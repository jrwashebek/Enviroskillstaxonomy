// About the data (#/about, #/about/:page). Owner: developer A. Spec: docs/DESIGN_SPEC.md §2.11. Licence: Apache-2.0.
// Page text comes from content.js (COPY.about); every count is filled from core data with aboutVars().
import { h, icon } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { NotFound } from "../lib/data.js";
import { state } from "../lib/state.js";
import { COPY, fill, fillBlocks, aboutVars } from "../content.js";
import { pageHeader, blocks, withMargin, table, evidenceLadder, ISSUES_URL } from "../ui.js";
import { copyText } from "../export.js";

const PAGES = [
  ["read", "How to read EMST", "What every label means, and what you can and can't use EMST for."],
  ["made", "How EMST was made", "Who drafted EMST, the checks that ran, and what has not happened yet."],
  ["status", "Release status", "How this release did on its release checks."],
  ["data", "Data and downloads", "How to get the data, cite it and reuse it with its caveats."],
  ["corrections", "Corrections and contributing", "How to report an error, or suggest work that is missing."],
  ["held", COPY.held?.heading || "Held records", "The statement on held records, and how many there are."],
  ["accessibility", "Accessibility", "The accessibility target and the known limits of this prototype."],
  ["privacy", "Privacy", "What this site does not collect."],
];
const TITLE = Object.fromEntries(PAGES.map(([k, t]) => [k, t]));
const crumbs = (title) => [{ href: "#/", text: "Home" }, { href: "#/about", text: "About the data" }, { text: title }];

function copyRow(label, getText, done) {
  const status = h("span", { class: "meta", role: "status", "aria-live": "polite" });
  const lab = h("span", label);
  const btn = h("button", { class: "btn btn--secondary btn--small", type: "button", on: { click: async () => {
    const ok = await copyText(getText());
    lab.textContent = ok ? "Copied" : label;
    status.textContent = ok ? done : COPY.errors?.copy || "Copy did not work. Select the text and copy it yourself.";
    setTimeout(() => { lab.textContent = label; status.textContent = ""; }, 2500);
  } } }, icon("copy"), lab);
  return h("div", { class: "btn-row" }, btn, status);
}

// ------------------------------------------------------------------ page-specific additions
/** Release status: the gate items from core data as a table, worded with the content designer's plain names. */
function gateTable(core, vars, dlBlock) {
  const plainName = {}, plainWhat = {};
  for (const [k, v] of dlBlock?.items || []) {
    const m = /^(\d+)\.\s*(.*?)(?::\s*\{gate\d+\})?$/.exec(k);
    if (m) { plainName[m[1]] = m[2]; plainWhat[m[1]] = v; }
  }
  const RES = { pass: ["badge--ok", "check"], conditional: ["badge--info", "info"], fail: ["badge--warn", "alert"] };
  const gate = core.status.gate;
  return table({
    caption: `Release checks for ${core.release.id}`,
    hint: `Results as of ${vars.gateAsOf}. Scripts and AI agents ran the checks; no person has signed them.`,
    sticky: false,
    columns: [
      { key: "n", label: "Check", render: (it) => `${it.n}. ${plainName[it.n] || `Check ${it.n}`}` },
      { key: "result", label: "Result", render: (it) => { const [cls, ic] = RES[it.result] || ["", "info"]; return h("span", { class: ["badge", "badge--compact", cls] }, icon(ic), cap(vars[`gate${it.n}`] || it.result)); } },
      { key: "what", label: "What it checks", render: (it) => plainWhat[it.n] || "" },
    ],
    rows: gate.items,
  });
}
const cap = (s) => (s ? s[0].toUpperCase() + s.slice(1) : "");

function heldPage(core) {
  const r = core.release, held = core.status.held;
  const title = COPY.held?.heading || "Held records";
  const body = h("div", { class: "notice notice--hold", role: "note", "data-emst-policy": "indigenous-statement" },
    h("div", { class: "notice__body" },
      h("p", held.policy),
      h("p", fill((COPY.about.held || []).find((b) => /\{heldN\}/.test(b.text || ""))?.text || "{heldN}", aboutVars(core))),
      r.indigenousStatement ? h("p", r.indigenousStatement) : null));
  return { title, node: h("div", pageHeader({ crumbs: crumbs(title), title }), h("div", { class: "page-body about-body" }, body)) };
}

// ------------------------------------------------------------------ view
export async function render({ params = {} } = {}) {
  const core = await data.core();
  const page = params.page;

  if (!page) {
    const node = h("div",
      pageHeader({ crumbs: [{ href: "#/", text: "Home" }, { text: "About the data" }], title: "About the data",
        lede: "How EMST was made, what it may be used for, and how to reuse it or correct it." }),
      h("div", { class: "page-body" }, h("ul", { class: "card-list" }, PAGES.map(([k, t, d]) => h("li",
        h("article", { class: "card card--about" },
          h("h2", { class: "card__title h4" }, h("a", { class: "card__link", href: `#/about/${k}` }, t)),
          h("p", { class: "card__summary" }, d)))))));
    return { title: "About the data", node };
  }
  if (!COPY.about?.[page] || !TITLE[page]) throw new NotFound(`No about page "${page}"`);
  if (page === "held") return heldPage(core);

  const vars = aboutVars(core);
  const raw = COPY.about[page];
  const filled = fillBlocks(raw, vars);
  const nodes = [];
  filled.forEach((b, i) => {
    // Release status: the eight checks as a table built from core.status.gate (same words as the list in COPY).
    if (page === "status" && b.t === "dl") { nodes.push(gateTable(core, vars, raw[i])); return; }
    // How it was made: the review path drawn as the evidence ladder (same steps and words as COPY.ladder).
    if (page === "made" && b.t === "ul" && filled[i - 2]?.id === "made-path") {
      const allUnreviewed = Object.values(core.figs || {}).every((f) => (f.ev?.r || "unreviewed") === "unreviewed");
      nodes.push(allUnreviewed ? evidenceLadder({ ev: { r: "unreviewed" } }) : blocks([b])[0]);
      return;
    }
    nodes.push(blocks([b])[0]);
    // Data: no download links yet (dist/ is not published), so say how to get the files and point to role exports.
    if (page === "data" && b.t === "p" && /Copy tasks as text/.test(b.text)) {
      nodes.push(blocks([
        { t: "p", text: "[Browse roles](#/roles) to find a role page." },
        { t: "p", text: `You can also ask for the release files on [GitHub Issues](${ISSUES_URL.replace(/\/new\/choose$/, "")}). You need a free GitHub account.` },
      ]));
    }
    if (page === "data" && b.t === "example") {
      nodes.push(copyRow("Copy citation", () => b.text, COPY.actions?.citeDone || "Citation copied"));
      // Next to the citation, because people cite record IDs: they can still change before version 2.0.0.
      nodes.push(h("p", { class: "about-note" }, icon("info"), h("span", "Record IDs are candidates until version 2.0.0, so they may still change. Always cite the release with the ID.")));
    }
    // Corrections: show the words from the last search so people can copy them into a suggestion.
    if (page === "corrections" && b.t === "p" && filled[i - 1]?.id === "corr-missing" && String(state.query || "").trim()) {
      const q = String(state.query).trim();
      nodes.push(h("div", { class: "panel search-words" }, h("p", { class: "meta", id: "your-words" }, "Your search words"),
        h("p", { class: "search-words__q", "aria-labelledby": "your-words" }, q), copyRow("Copy search words", () => q, "Search words copied")));
    }
  });

  const sections = filled.filter((b) => b.t === "h2" && b.id).map((b) => ({ id: b.id, title: b.text }));
  const prose = h("div", { class: "prose about-body" }, nodes.flat());
  const body = sections.length >= 2 ? withMargin(sections, prose) : h("div", { class: "page-body" }, prose);
  return { title: TITLE[page], node: h("div", pageHeader({ crumbs: crumbs(TITLE[page]), title: TITLE[page] }), body) };
}
