// What EMST covers (#/coverage). Brief: DEV_COVERAGE (HCD lead). Licence: Apache-2.0.
// The heading and opening come from core.js and show at once. The rest of the page (the scope map, statuses and counts) is
// composed from the data by tools/build-data.mjs into data/coverage.js, loaded only here, so the app bundle carries only
// this renderer. Status is always written in words; colour and icon repeat it.
import { h, icon } from "../lib/dom.js";
import * as data from "../lib/data.js";
import { focusSection, parseHash } from "../lib/router.js";
import { COPY, fill } from "../content.js";
import { pageHeader, section, withMargin, table, blocks, rich, emptyState, fmt, disclosure } from "../ui.js";

const T = COPY.coverage;
const BADGE = { roles: ["badge--ok", "check"], comps: ["badge--info", "layers"], compsOnly: ["badge--info", "layers"], none: ["cov-badge-none"] };

export async function render() {
  const core = await data.core();
  const mods = Object.keys(core.labels?.module || {}).filter((ns) => ns !== "core");
  const withRoles = new Set(core.roles.filter((r) => !r.whatsComingOnly).map((r) => r.module).filter((ns) => mods.includes(ns)));
  const slot = h("div", { class: "loading", role: "status" }, h("span", { class: "spinner", "aria-hidden": "true" }), T.loading);
  const node = h("div",
    pageHeader({ crumbs: [{ href: "#/", text: "Home" }, { href: "#/about", text: "About the data" }, { text: T.title }], title: T.title, lede: T.lede,
      meta: h("div", { class: "cov-intro" }, h("p", fill(T.modules, { n: fmt(withRoles.size), total: fmt(mods.length) })), h("p", T.purpose)) }),
    slot);
  data.coverage().then((cov) => {
    if (!slot.isConnected) return;
    slot.replaceWith(body(cov));
    const { section: target } = parseHash(); // a deep link to a part of the page, once that part exists
    if (target && document.getElementById(target) && [document.body, node.querySelector("h1")].includes(document.activeElement)) focusSection(target);
  }).catch(() => { if (slot.isConnected) slot.replaceWith(emptyState({ title: COPY.errors.load.title, body: COPY.errors.load.body, iconName: "alert" })); });
  return { title: T.title, node };
}

function body(cov) {
  const C = cov.cols;
  const badge = (st) => h("span", { class: ["badge", "badge--compact", BADGE[st]?.[0]] }, BADGE[st]?.[1] ? icon(BADGE[st][1]) : null, cov.status[st]);
  const sub = (r) => (r.shared ? h("span", { class: "cov-sub" }, r.shared) : null);
  const cell = {
    module: (r) => [r.module, r.wave ? h("span", { class: "cov-sub" }, r.wave) : null],
    comps: (r) => [r.comps, sub(r), r.links ? h("ul", { class: "cov-comps" }, r.links.map((x) => h("li", rich(x)))) : null],
    tasks: (r) => [r.tasks, sub(r)],
    st: (r) => badge(r.st),
  };
  // Subsectors as a table from 40rem up, and as stacked cards on phones (as the role page's competency table).
  const asTable = (b) => table({ caption: b.caption, hint: cov.tableHint, sticky: false, rows: b.rows, columns: [
    { key: "label", label: C.sub }, { key: "module", label: C.module, render: cell.module }, { key: "roles", label: b.rolesHead },
    { key: "comps", label: C.comps, render: cell.comps }, { key: "tasks", label: C.tasks, num: true, render: cell.tasks }, { key: "st", label: C.status, render: cell.st }] });
  const asCards = (b) => h("ul", { class: "cov-cards", "aria-label": b.caption }, b.rows.map((r) => h("li", { class: "cov-card" },
    h("h4", { class: "cov-card__title" }, r.label), h("p", h("span", { class: "vh" }, `${C.status}: `), badge(r.st)),
    h("dl", { class: "facts" }, [["module", C.module], ["roles", b.rolesHead], ["comps", C.comps], ["tasks", C.tasks]]
      .flatMap(([k, label]) => [h("dt", label), h("dd", cell[k] ? cell[k](r) : r[k])])))));
  const wraps = [];
  const area = (b) => {
    const wrap = h("div", { class: "cov-wrap" });
    wraps.push([wrap, b]);
    // Each area's heading and one-line summary stay visible; its subsector table and role list sit in a closed
    // disclosure, so the whole scope map can be scanned on one screen (the open page was over 13,000 px at 1280).
    const n = b.rows?.length || 0;
    return h("div", { class: "cov-area", id: b.id, tabindex: "-1" }, h("h3", b.label), h("p", { class: "meta" }, b.summary),
      disclosure(`Show ${n === 1 ? "its subsector" : `its ${n} subsectors`} and roles`, [wrap,
        b.roles ? h("div", { class: "cov-mods" }, h("h4", cov.rolesBy), h("dl", b.roles.map(([m, items]) => [h("dt", m),
          h("dd", h("ul", { class: "cov-rolelist" }, items.map((x) => h("li", rich(x)))))]))) : h("p", { class: "meta" }, b.noRoles)], { small: true }));
  };
  const block = (b) => (b.t === "area" ? area(b)
    : b.t === "totals" ? h("ul", { class: "cov-totals" }, b.items.map(([st, x]) => h("li", badge(st), h("span", x))))
    : b.t === "key" ? h("dl", { class: "cov-key" }, b.items.map(([st, x]) => [h("dt", badge(st)), h("dd", x)]))
    : b.t === "draft" ? h("p", { class: "cov-draft" }, icon("draft"), h("span", b.text))
    : b.t === "suggest" ? h("p", h("a", { class: "arrow-link", href: b.href }, icon("flag"), b.text, icon("arrow-right")))
    : blocks([b])[0]);
  const parts = cov.sections.map((s) => section(s.id, s.title, s.blocks.map(block)));
  const mq = window.matchMedia("(min-width: 40rem)");
  let wide = null;
  const draw = () => { if (wide === mq.matches) return; wide = mq.matches; for (const [w, b] of wraps) w.replaceChildren(wide ? asTable(b) : asCards(b)); };
  const onMq = () => { if (!wraps[0]?.[0].isConnected) { mq.removeEventListener("change", onMq); return; } draw(); };
  mq.addEventListener("change", onMq);
  draw();
  return withMargin(cov.sections.map((s) => ({ id: s.id, title: s.title })), h("div", { class: "cov-body" }, parts));
}
