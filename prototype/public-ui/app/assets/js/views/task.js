// Task page (#/task/:slug). DESIGN_SPEC §2.7. Developer C. Licence: Apache-2.0.
import { h, frag, icon } from "../lib/dom.js";
import * as data from "../lib/data.js";
import * as ui from "../ui.js";
import { COPY, fill } from "../content.js";
import { fmt, dateLong } from "../lib/format.js";
import { plain, plural, credSlug, humanize, cap, draftNote } from "./misc.js";

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

// v1 evidence drawer in plain words. File paths, field names and flag codes go into a nested "Technical source"
// disclosure (trust review U5). Meanings of the flags come from scripts/migrate_v1.py in the repository.
const V1_FIELD = {
  "v1 automation type": "Type of automation", "v1 tacit knowledge density": "Know-how that is hard to write down",
  "v1 career-ladder position": "Career stage", "v1 vector": "Kind of technology", "v1 horizon": "When it might happen",
};
const V1_WORD = { Lo: "Low", Med: "Medium", Hi: "High", "none (?)": "None recorded" };
const V1_FLAG = {
  text_misaligned: "the v1 record's task wording differs noticeably from this task",
  reconstructed_d2: "the values were rebuilt from another v1 working record",
  d2_divergent: "another v1 working record gives different values",
  reconciled_d6_2026_03: "the values come from a v1 file that was reconciled in March 2026",
  pre15a_hybrid: "the values come from an earlier v1 reclassification pass",
  normative_h: "“human-essential” here is a judgment about what should stay human, not a finding",
};
/** "C (Contributing (3–8 yr))" → "Contributing (3–8 yr)"; "Med" → "Medium". */
const v1Value = (v) => V1_WORD[v] || String(v ?? "").replace(/^[A-Za-z0-9]{1,4} \((.*)\)$/, "$1");
const v1Source = (src) => (/^v1 database/i.test(src || "") ? "The v1 database" : /^v1 working record/i.test(src || "") ? "A v1 working record" : "A v1 record");
const v1Reason = (r) => { const m = /^v1 flag: (\w+)$/.exec(r); return m ? (V1_FLAG[m[1]] ? `v1 note: ${V1_FLAG[m[1]]}` : "a v1 note on this record") : plain(r); };

function v1Drawer(task, core) {
  const v1 = task.v1;
  if (!v1) return null;
  const prior = v1.prior || [];
  const body = [
    h("p", core.text.v1DrawerBody),
    prior.map((p, i) => h("div", { class: "c-prior" },
      h("h3", { class: "h4 c-prior__title" }, prior.length > 1 ? `Earlier coding ${i + 1} of ${prior.length}` : "Earlier coding", p.d ? h("span", { class: "meta" }, ` (${dateLong(p.d)})`) : null),
      h("dl", { class: "facts" }, (p.vals || []).flatMap(([k, v]) => [h("dt", V1_FIELD[k] || cap(String(k).replace(/^v1\s+/, ""))), h("dd", v1Value(v))])),
      h("p", { class: "meta" }, [
        `${v1Source(p.src)}, coded by one analyst working with an AI assistant.`,
        p.conf ? `The analyst's own confidence: ${p.conf}.` : null,
        p.flags?.length ? `Notes: ${p.flags.map((f) => V1_FLAG[f] || "a v1 note on this record").join("; ")}.` : null,
        p.stale ? "Marked as out of date." : null,
      ].filter(Boolean).join(" ")))),
    v1.contested ? h("p", h("strong", "Contested. "), cap((v1.reasons || []).map(v1Reason).join("; ")), ".") : null,
    core.text.v1DrawerChange ? h("p", { class: "meta" }, core.text.v1DrawerChange) : null,
    ui.disclosure("Technical source", [
      h("p", { class: "meta" }, "Where these values came from, as recorded in the v1 files. For people tracing the data."),
      prior.map((p, i) => h("dl", { class: "facts c-tech" },
        h("dt", "Record"), h("dd", h("span", { class: "id" }, p.id || `v1 record ${i + 1}`)),
        p.src ? [h("dt", "Source as recorded"), h("dd", h("span", { class: "c-path" }, plain(p.src)))] : null,
        (p.vals || []).length ? [h("dt", "Fields and codes"), h("dd", (p.vals || []).map(([k, v]) => `${k}: ${v}`).join("; "))] : null,
        p.flags?.length ? [h("dt", "Flags as recorded"), h("dd", h("span", { class: "c-path" }, p.flags.join(", ")))] : null)),
    ], { small: true }),
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
