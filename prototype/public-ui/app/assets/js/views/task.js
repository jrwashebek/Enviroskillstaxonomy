// Task page (#/task/:slug). DESIGN_SPEC §2.7. Developer C. Licence: Apache-2.0.
import { h, frag, icon } from "../lib/dom.js";
import * as data from "../lib/data.js";
import * as ui from "../ui.js";
import { COPY, fill } from "../content.js";
import { fmt, dateLong } from "../lib/format.js";
import { plain, plural, credSlug, humanize, draftNote } from "./misc.js";

const NOUN = "O*NET task";

/** "ONET:19-4042.00:1553" → {occ: "19-4042.00", id: "1553"} */
function onetId(obj) {
  const parts = String(obj || "").replace(/^ONET:/, "").split(":");
  return parts.length >= 2 ? { occ: parts[0], id: parts.slice(1).join(":") } : { occ: null, id: parts[0] };
}

function onetRows(rows) {
  const sorted = rows.slice().sort((a, b) => (a.none ? 1 : 0) - (b.none ? 1 : 0));
  const list = h("ul", { class: "xw-list stack" }, sorted.map((r) => {
    const id = r.none ? null : onetId(r.obj);
    const reason = r.none && r.note ? (/no-term reason:\s*([^.(]+)/i.exec(r.note) || [])[1] : null;
    const coders = /adjudication/.test(r.st || "") ? COPY.match.disagree : /two-llm/.test(r.st || "") ? COPY.match.twoCoders : null;
    return h("li", { class: "xw" },
      h("p", { class: "xw__name" }, r.none ? fill(COPY.match.none, { noun: NOUN })
        : [`${NOUN} `, h("span", { class: "id" }, id.id), id.occ ? [" in occupation ", h("span", { class: "id" }, id.occ)] : null]),
      h("p", { class: "cluster xw__badges" }, r.none ? null : ui.badgeMatch(r, NOUN),
        h("span", { class: "badge badge--draft" }, icon("unreviewed"), COPY.match.unreviewed)),
      coders ? h("p", { class: ["meta", /adjudication/.test(r.st || "") && "c-disagree"] }, coders, ".") : null,
      reason ? h("p", { class: "meta" }, `Reason the AI agents gave: ${plain(reason.trim())}.`) : null);
  }));
  const ver = [...new Set(rows.map((r) => String(r.ver || "").replace(/\s*\(.*$/, "")).filter(Boolean))];
  return [list, ver.length ? h("p", { class: "meta" }, `Compared with: ${ver.join("; ")}.`) : null, h("p", { class: "meta" }, COPY.match.note)];
}

function v1Drawer(task, core) {
  const v1 = task.v1;
  if (!v1) return null;
  const body = [
    h("p", core.text.v1DrawerBody),
    (v1.prior || []).map((p) => h("div", { class: "c-prior" },
      h("h4", { class: "c-prior__title" }, p.d ? `Coded on ${dateLong(p.d)}` : "Earlier coding"),
      h("dl", { class: "facts" }, (p.vals || []).flatMap(([k, v]) => [h("dt", k), h("dd", v)])),
      h("p", { class: "meta" }, [
        p.conf ? `Analyst's own confidence: ${p.conf}.` : null,
        p.flags?.length ? `Flags: ${p.flags.map(humanize).join(", ").toLowerCase()}.` : null,
        p.stale ? "Marked as out of date." : null,
      ].filter(Boolean).join(" ")),
      p.src ? h("p", { class: "meta" }, `Source: ${plain(p.src)}`) : null)),
    v1.contested ? h("p", h("strong", "Contested. "), (v1.reasons || []).map((r) => plain(r).replace(/_/g, " ")).join("; "), ".") : null,
    core.text.v1DrawerChange ? h("p", { class: "meta" }, core.text.v1DrawerChange) : null,
  ];
  return ui.disclosure(plain(v1.lab), body, { badge: ui.badgeNfd() });
}

export async function render({ params }) {
  const [core, task] = await Promise.all([data.core(), data.task(params.slug)]);
  const comps = (task.comps || []).slice().sort((a, b) => (a.strength === "primary" ? 0 : 1) - (b.strength === "primary" ? 0 : 1));
  const roles = task.roles || [];
  const primary = comps.find((c) => c.strength === "primary") || comps[0];
  const words = String(task.stmt || "").split(/\s+/);
  const short = words.slice(0, 8).join(" ") + (words.length > 8 ? "…" : "");
  const anyFormation = roles.some((r) => r.formation);

  const what = ["workFunction", "craft", "exposure"];
  if (task.ja) what.unshift("importance", "timeShare", "critical", "neededAtEntry");

  const sections = [];
  sections.push(ui.section("competencies", "Competencies it uses", comps.length ? h("ul", { class: "task-list" }, comps.map((c) => h("li",
    h("a", { href: ui.link.comp(c.slug) }, c.title),
    h("p", { class: "task-list__meta" }, c.strength === "primary" ? "Main competency for this task" : "Also uses this competency")))) : h("p", "No competency is linked yet."),
  { meta: plural(comps.length, "competency", "competencies") }));

  sections.push(ui.section("roles", "Roles it appears in", roles.length ? [
    h("ul", { class: "task-list" }, roles.map((r) => h("li", h("a", { href: ui.link.role(r.slug) }, r.title),
      r.formation ? [" ", h("span", { class: "badge badge--compact" }, COPY.formation.tag)] : null))),
    anyFormation ? h("p", { class: "meta" }, h("strong", `${COPY.formation.tag}: `), COPY.formation.explain, " ", h("a", { href: ui.link.key("formation") }, "More about formation tasks")) : null,
  ] : h("p", "No role profile includes this task yet. It is linked only through its competencies."), { meta: plural(roles.length, "role") }));

  sections.push(ui.section("assessment", "Assessment status", [
    h("div", { class: "c-pending" }, ui.pendingSummary({ what })),
    task.ja ? h("p", { class: "meta" }, core.text.jaNote) : null,
    v1Drawer(task, core),
  ]));

  if (task.x2?.length) sections.push(ui.section("onet", "Matching O*NET tasks", [
    h("p", "AI agents looked for tasks in O*NET, the US Department of Labor's database of occupations, that describe the same work."),
    ...onetRows(task.x2),
  ]));

  if (task.tools?.length) sections.push(ui.section("tools", "Tools", [
    h("ul", { class: "task-list" }, task.tools.map((t) => h("li", h("a", { href: `#/tool/${t.id}` }, t.title),
      t.lc && t.lc !== "established" ? [" ", ui.badgeLifecycle(t.lc, { compact: true })] : null))),
    draftNote("AI agents drafted these links."),
  ]));

  const creds = task.credentialGates || [];
  if (creds.length || task.credentialGatesPending || task.signOffPending) sections.push(ui.section("credentials", "Credentials that may be involved", [
    h("p", "Some employers may look for these credentials for this work. They are AI-drafted links, not requirements. Each employer decides what its jobs need."),
    creds.length ? h("ul", { class: "task-list" }, creds.map((c) => h("li", h("a", { href: `#/credential/${credSlug(c.title)}` }, c.title), h("p", { class: "task-list__meta" }, "May be involved (AI-drafted link)")))) : null,
    task.credentialGatesPending ? h("p", { class: "meta" }, `${plural(task.credentialGatesPending, "more credential")} not shown until the issuer is checked against a source.`) : null,
    task.signOffPending ? h("dl", { class: "facts" }, h("dt", "Who signs off"), h("dd", core.text.signOffPending)) : null,
  ]));

  sections.push(ui.section("about", "About this record", ui.aboutRecord(task, core, { title: task.stmt, kind: "Task" })));

  const header = ui.pageHeader({
    crumbs: [{ href: "#/", text: "Home" }, { href: "#/competencies", text: "Competencies" },
      primary ? { href: ui.link.comp(primary.slug), text: primary.title } : null, { text: "Task" }].filter(Boolean),
    kind: "Task", id: task.id, title: task.stmt,
    status: ui.statusLine(task, { aboutHref: "#about" }),
  });
  header.querySelector("h1")?.classList.add("c-task-h1");

  const node = frag(ui.printMeta(core, `Task: ${short}`), header, h("div", { class: "page-body c-single" }, sections));
  return { title: `Task: ${short}`, node };
}
