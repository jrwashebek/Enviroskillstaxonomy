// Build the EMST GitBook guidebook (project-lead decision Q17, phase 1) from the same release build as the explorer.
//
// Reads
//   app/data/core.js, coverage.js, change.js   the explorer's data, written by build-data.mjs from the release
//   app/assets/js/content.js                    the explorer's copy (the about pages are reused word for word)
//   gitbook/src/pages/**/*.md                   pages written for the guidebook, with {{tokens}} for every count
//   gitbook/src/config.json                     addresses (explorer, repository, issues)
// Writes
//   gitbook/site/   the folder GitBook's Git Sync reads: .gitbook.yaml, README.md, SUMMARY.md and the pages
//
// Usage (from the repository root):
//   node prototype/public-ui/tools/build-gitbook.mjs           build gitbook/site
//   node prototype/public-ui/tools/build-gitbook.mjs --check   exit 1 if gitbook/site differs from a fresh build
// Then run tools/check-gitbook.mjs before anything is synced. Licence: Apache-2.0.
import { readFileSync, writeFileSync, mkdirSync, rmSync, readdirSync, statSync, existsSync, mkdtempSync } from "node:fs";
import { join, resolve, dirname, posix } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import vm from "node:vm";

const HERE = dirname(fileURLToPath(import.meta.url));
const UI = resolve(HERE, "..");
const ROOT = resolve(UI, "..", "..");
const SRC = join(UI, "gitbook", "src");
const SITE = join(UI, "gitbook", "site");
const CHECK = process.argv.includes("--check");
const require = createRequire(import.meta.url);
const yaml = require(join(ROOT, "site", "node_modules", "js-yaml"));

const { COPY, GLOSSARY, aboutVars, fillBlocks, fill } = await import(pathToFileURL(join(UI, "app", "assets", "js", "content.js")).href);
globalThis.window = {};
for (const f of ["core", "coverage", "change"]) vm.runInThisContext(readFileSync(join(UI, "app", "data", `${f}.js`), "utf8"));
const { core, coverage: cov, change } = window.EMSTDATA;
const CFG = JSON.parse(readFileSync(join(SRC, "config.json"), "utf8"));
const problems = [];

// ---------------------------------------------------------------- figures (every count comes from the release build)
const nf = (n) => (typeof n === "number" ? n.toLocaleString("en-US") : String(n ?? ""));
const lcFirst = (s) => (/^[A-Z][a-z]/.test(s) ? s[0].toLowerCase() + s.slice(1) : s);
const C = core.counts, T = C.byType;
const tierOf = (r) => r.tier?.t || "exploratory";
const modNs = Object.keys(core.labels?.module || {}).filter((ns) => ns !== "core");
const withRoles = new Set(core.roles.filter((r) => !r.whatsComingOnly).map((r) => r.module).filter((ns) => modNs.includes(ns)));
const csvRows = (f) => readFileSync(join(ROOT, "data", "v1_baseline", f), "utf8").trim().split(/\r?\n/).slice(1);
const v1Struct = csvRows("structure.csv").map((l) => l.split(",")[1]);
const vars = aboutVars(core);
const R = core.release;
const EMPLOYER_PHRASE = { private: "the private sector" };
const actors = core.sectorActors.map((a) => EMPLOYER_PHRASE[a.code] || lcFirst(a.label));
const emerging = core.roles.filter((r) => r.whatsComingOnly);
const moved = change.changeIndicators.moved;
const block = (page, id) => { // the blocks of one about-page section, tokens filled
  const bs = fillBlocks(COPY.about[page], vars); const i = bs.findIndex((b) => b.t === "h2" && b.id === id); const out = [];
  for (let j = i + 1; j < bs.length && bs[j].t !== "h2"; j++) out.push(bs[j]);
  return out;
};
const notForPeopleNotice = fillBlocks(COPY.about.read, vars).find((b) => b.t === "notice" && b.kind === "caution").text;
const V = {
  ...vars,
  lede: COPY.site.lede, repo: CFG.repo, issues: CFG.issues, markdownCopy: CFG.markdownCopy, gitbookCookies: CFG.gitbookCookies,
  decisionsUrl: `${CFG.repo}/tree/main/docs/decisions`, governanceUrl: `${CFG.repo}/tree/main/docs/governance`, v1Url: `${CFG.repo}/tree/main/legacy/v1`,
  roles: nf(core.roles.length), rolesDescribe: nf(core.roles.filter((r) => tierOf(r) === "describe").length),
  rolesEmerging: nf(core.stats.depth.emerging), rolesFull: nf(core.stats.depth.full), rolesLower: nf(core.stats.depth.lower),
  comps: nf(T.Competency), compsCore: nf(C.coreCompetencies), compsModule: nf(T.Competency - C.coreCompetencies),
  compsPractice: nf(C.competenciesByKind.practice), compsTransversal: nf(C.competenciesByKind.transversal), compsKnowledge: nf(C.competenciesByKind["knowledge-area"]),
  compsWatch: nf(C.competenciesByLifecycle.watch), tasks: nf(T.Task), indicators: nf(T.Indicator), variants: nf(T.RoleVariant),
  families: nf(core.jobFamilies.length), modules: nf(modNs.length), modulesWithRoles: nf(withRoles.size), subsectors: nf(cov.subsectors.length),
  series: nf(T.SeriesRecord), stateClasses: nf(T.StateClassRecord), tools: nf(T.Tool), credentials: nf(T.Credential),
  signals: nf(change.signals.length), instruments: nf(change.instruments.length), instrumentsWithheld: nf(change.instrumentsWithheld.n),
  changeTargets: nf(change.changeIndicators.n), changeMovedSentence: moved ? `${nf(moved)} met it.` : "None met it.",
  emergingExample: lcFirst(emerging[0]?.title || ""), scenarioAxes: change.scenarios.axes.map((a) => lcFirst(a.label)).join(", and "),
  actorList: `${actors.slice(0, -1).join("; ")}; and ${actors.at(-1)}`,
  v1Domains: nf(v1Struct.filter((l) => l === "domain").length), v1SkillAreas: nf(v1Struct.filter((l) => l === "skill_area").length),
  v1Comps: nf(csvRows("competencies.csv").length), v1Tasks: nf(csvRows("tasks.csv").length),
  notForPeopleNotice, pathwaysNotice: core.text.pathwaysNotice, whatsComingNotice: change.notice || core.text.whatsComingNotice,
  compareCaveat: COPY.compare.caveat, describeWhy: COPY.use.describe.why, developWhy: COPY.use.develop.why, developNotReached: COPY.use.develop.notReached,
  hrDraftRule: core.text.hrDisclaimer[1].replace(/^This view describes work\. It is not ready for training or development plans\. /, ""),
  dataCaveats: block("data", "data-caveats").map((b) => b.text).join(" "),
  lifecycleWatch: COPY.lifecycle.watch.plain, heldPolicy: core.status.held.policy, indigenousStatement: R.indigenousStatement,
  craftField: GLOSSARY["field craft"].def, craftData: GLOSSARY["data craft"].def, craftState: GLOSSARY.statecraft.def,
};
const LISTS = { notForPeople: COPY.use.describe.youCant, exploratoryCant: COPY.use.exploratory.youCant };
if (V.hrDraftRule === core.text.hrDisclaimer[1]) problems.push("hrDisclaimer[1] changed: re-check the HR draft rule on 'Describe the work'");

// ---------------------------------------------------------------- Markdown helpers
const slug = (s) => String(s).toLowerCase().replace(/[’'"“”]/g, "").replace(/[^a-z0-9\s-]/g, " ").trim().replace(/\s+/g, "-").replace(/-+/g, "-");
const esc = (s) => String(s ?? "").replace(/([\\*`<>[\]])/g, "\\$1");
const cell = (s) => String(s ?? "").replace(/\|/g, "\\|").replace(/\n+/g, " ");
const rel = (from, to) => { const r = posix.relative(posix.dirname(from), to); return r || posix.basename(to); };

// Explorer routes inside the explorer's copy, mapped to guidebook pages. Anything else under "#/" is an explorer page.
const READ_SPLIT = {
  "use-tiers": "how-to-read/uses.md", "use-describe": "how-to-read/uses.md", "use-exploratory": "how-to-read/uses.md", "use-develop": "how-to-read/uses.md", "use-select": "how-to-read/uses.md",
  "ai-drafted": "how-to-read/drafted-by-ai-agents.md", review: "how-to-read/review-status.md", evidence: "how-to-read/evidence-labels.md",
  pending: "how-to-read/assessment-pending.md", lifecycle: "how-to-read/how-established.md", matches: "how-to-read/links-to-other-systems.md",
  "source-grades": "how-to-read/source-grades.md", formation: "how-to-read/formation-tasks.md", held: "how-to-read/held-records.md", "not-gov": "how-to-read/not-a-government-website.md",
};
const ABOUT_PAGE = { read: "how-to-read/README.md", made: "start-here/how-emst-was-made.md", status: "release/status.md", data: "release/data-and-downloads.md",
  corrections: "contribute/corrections-and-contributing.md", held: "how-to-read/held-records.md", accessibility: "release/accessibility.md", privacy: "release/privacy.md" };
const COV_DIR = "start-here/what-emst-covers";
const areaBlocks = cov.sections.find((s) => s.id === "cov-map").blocks.filter((b) => b.t === "area");
const AREA_PAGE = Object.fromEntries(areaBlocks.map((b) => [b.id, `${COV_DIR}/${slug(b.label)}.md`]));

function mapHref(href) {
  if (/^https:\/\//.test(href)) return href;
  let m = href.match(/^#\/about(?:\/(\w+))?(?:@([\w-]+))?$/);
  if (m) {
    const pg = m[1] || "read", a = m[2];
    if (pg === "read" && a) return `page:${READ_SPLIT[a] || ABOUT_PAGE.read}`;
    const h2 = a && (COPY.about[pg] || []).find((b) => b.t === "h2" && b.id === a);
    return `page:${ABOUT_PAGE[pg] || ABOUT_PAGE.read}${h2 ? `#${slug(h2.text)}` : ""}`;
  }
  m = href.match(/^#(?:\/coverage)?@?(cov-[\w-]+)?$/) || href.match(/^#\/coverage@([\w-]+)$/);
  if (m || href === "#/coverage") {
    const id = m?.[1];
    if (id && AREA_PAGE[id]) return `page:${AREA_PAGE[id]}`;
    const sec = id && cov.sections.find((s) => s.id === id);
    return `page:${COV_DIR}/README.md${sec ? `#${slug(sec.title)}` : ""}`;
  }
  if (href.startsWith("#/")) return `explorer:${href.slice(1)}`;
  problems.push(`unmapped link ${href}`);
  return href;
}
/** Plain text with inline [text](href) links: escape the text, map the links. */
function inline(text) {
  const out = []; let last = 0;
  for (const m of String(text ?? "").matchAll(/\[([^\]\n]+)\]\(([^)\s]+)\)/g)) {
    out.push(esc(text.slice(last, m.index)), `[${esc(m[1])}](${mapHref(m[2])})`);
    last = m.index + m[0].length;
  }
  out.push(esc(String(text ?? "").slice(last)));
  return out.join("");
}
const hint = (style, body) => `{% hint style="${style}" %}\n${body}\n{% endhint %}`;
const tableMd = (head, rows) => [`| ${head.map(cell).join(" | ")} |`, `|${head.map(() => "---").join("|")}|`, ...rows.map((r) => `| ${r.map(cell).join(" | ")} |`)].join("\n");
const DL_HEAD = {
  review: ["Status", "What it means"], evidence: ["Label", "What it means"], lifecycle: ["Label", "What it means"], matches: ["Match type", "What it means"],
  "source-grades": ["Grade", "What it means"], "status-checks": ["Check and result", "What it covers"], "data-files": ["File", "What it holds"], "cov-kinds": ["Kind of profile", "What it means"],
};
function blocksMd(blocks, ctx = "") {
  const out = [];
  for (const b of blocks) {
    if (b.t === "h2") { ctx = b.id; out.push(`## ${esc(b.text)}`); }
    else if (b.t === "h3") out.push(`### ${esc(b.text)}`);
    else if (b.t === "p") out.push(inline(b.text));
    else if (b.t === "ul") out.push(b.items.map((x) => `- ${inline(x)}`).join("\n"));
    else if (b.t === "notice") out.push(hint(b.kind === "caution" ? "warning" : "info", `${b.title ? `**${esc(b.title)}.** ` : ""}${inline(b.text)}`));
    else if (b.t === "example") out.push(`> **${esc(b.label)}:** ${inline(b.text)}`);
    else if (b.t === "dl") out.push(tableMd(DL_HEAD[ctx] || ["Term", "What it means"], b.items.map(([k, v]) => [inline(k), inline(v)])));
    else if (b.t === "draft") out.push(hint("info", inline(b.text)));
    else if (b.t === "totals") out.push(b.items.map(([st, x]) => `- ${esc(cov.status[st])}: ${inline(x)}`).join("\n"));
    else if (b.t === "key") out.push(tableMd(["Status", "What it means"], b.items.map(([st, x]) => [esc(cov.status[st]), inline(x)])));
    else if (b.t === "suggest") out.push(`[${esc(b.text)}](${mapHref(b.href)})`);
    else if (b.t === "area") out.push(`- [${esc(b.label)}](page:${AREA_PAGE[b.id]}): ${inline(b.summary)}`);
    else problems.push(`unknown block type ${b.t}`);
  }
  return out.join("\n\n");
}
function sectionsOf(page) { // {id: {title, blocks}} for one about page, tokens filled; intro blocks under ""
  const out = { "": { title: "", blocks: [] } }; let cur = out[""];
  for (const b of fillBlocks(COPY.about[page], vars)) {
    if (b.t === "h2") { cur = { title: b.text, blocks: [] }; out[b.id] = cur; } else cur.blocks.push(b);
  }
  return out;
}

// ---------------------------------------------------------------- pages
const PAGES = new Map(); // path -> {title, description, body}
const add = (path, title, description, body) => {
  if (PAGES.has(path)) problems.push(`duplicate page ${path}`);
  PAGES.set(path, { title, description, body: body.trim() });
};

// Pages written for the guidebook
const missing = new Set();
const walk = (d) => readdirSync(d).flatMap((f) => (statSync(join(d, f)).isDirectory() ? walk(join(d, f)) : f.endsWith(".md") ? [join(d, f)] : []));
for (const file of walk(join(SRC, "pages"))) {
  const raw = readFileSync(file, "utf8");
  const m = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!m) { problems.push(`no front matter: ${file}`); continue; }
  const fm = yaml.load(m[1]);
  let body = m[2].replace(/^\{\{list:(\w+)\}\}$/gm, (t, k) => (LISTS[k] ? LISTS[k].map((x) => `- ${esc(x)}`).join("\n") : t));
  body = body.replace(/\{\{(\w+)\}\}/g, (t, k) => (Object.prototype.hasOwnProperty.call(V, k) ? String(V[k]) : (missing.add(`${fm.path}: {{${k}}}`), t)));
  add(fm.path, fm.title, fm.description, body);
}

// How to read EMST: the explorer's "How to read EMST" page, one guidebook page per label
const read = sectionsOf("read");
const READ_PAGES = [
  ["how-to-read/uses.md", ["use-tiers", "use-describe", "use-exploratory", "use-develop", "use-select"], "What each use label allows, from explore only to job analysis input, and which uses no record reaches yet."],
  ["how-to-read/drafted-by-ai-agents.md", ["ai-drafted"], "Who drafted EMST's records, what AI agents and people did, and what has not been done yet."],
  ["how-to-read/review-status.md", ["review"], "The review statuses a record can have, and where release records stand."],
  ["how-to-read/evidence-labels.md", ["evidence"], "The E, J and S labels that say what each record rests on."],
  ["how-to-read/assessment-pending.md", ["pending"], "Why some values show “Assessment pending” instead of a number, and what that does and doesn't mean."],
  ["how-to-read/how-established.md", ["lifecycle"], "Labels that say how established a kind of work is, from on watch to withdrawn."],
  ["how-to-read/links-to-other-systems.md", ["matches"], "How EMST records link to O*NET, ESCO, OPM job series and state job classes, and what the match types mean."],
  ["how-to-read/source-grades.md", ["source-grades"], "The A to D grades given to the sources of signals about change."],
  ["how-to-read/formation-tasks.md", ["formation"], "Tasks that are learned through supervised practice on the job, not from a course alone."],
  ["how-to-read/not-a-government-website.md", ["not-gov"], "EMST is an independent, open project. No government agency runs it or has endorsed it."],
];
for (const [path, ids, desc] of READ_PAGES) {
  const [first, ...rest] = ids;
  const body = [blocksMd(read[first].blocks, first), ...rest.map((id) => blocksMd([{ t: "h2", id, text: read[id].title }, ...read[id].blocks], id))].join("\n\n");
  add(path, read[first].title, desc, body);
}
add("how-to-read/held-records.md", COPY.held.heading, "The statement on held records, and how many there are.",
  blocksMd(fillBlocks(COPY.about.held, vars)));
const glossRows = Object.entries(GLOSSARY).sort(([a], [b]) => a.localeCompare(b, "en", { sensitivity: "base" }))
  .map(([k, g]) => [esc(k), esc(g.exp || ""), esc(g.def)]);
add("how-to-read/glossary.md", "Glossary", "Plain-language meanings of the abbreviations and specialist words used across EMST.",
  `Plain meanings of the abbreviations and specialist words you will see on EMST. Where a term is an abbreviation, the second column spells it out.\n\n${tableMd(["Term", "Stands for", "Meaning"], glossRows)}`);
add("how-to-read/README.md", "How to read EMST", "What every label on an EMST record means, and what you can and can't use EMST for.",
  ["This section explains every label you will see on EMST. In the explorer, each label on a record links to its explanation.", "",
    ...[...READ_PAGES.map(([p, ids, d]) => [p, read[ids[0]].title, d]), ["how-to-read/held-records.md", COPY.held.heading, PAGES.get("how-to-read/held-records.md").description],
      ["how-to-read/glossary.md", "Glossary", PAGES.get("how-to-read/glossary.md").description]]
      .map(([p, t, d]) => `- **[${esc(t)}](page:${p}).** ${esc(d)}`)].join("\n"));

// The explorer's other about pages, word for word
const aboutPage = (page, path, title, desc, drop = []) => {
  const s = sectionsOf(page);
  const body = Object.entries(s).filter(([id]) => !drop.includes(id))
    .map(([id, sec]) => (id ? blocksMd([{ t: "h2", id, text: sec.title }, ...sec.blocks], id) : blocksMd(sec.blocks))).join("\n\n");
  add(path, title, desc, body);
};
aboutPage("made", "start-here/how-emst-was-made.md", "How EMST was made", "Who drafted EMST, the checks that ran, and what has not happened yet.");
aboutPage("status", "release/status.md", "Release status", `How release ${R.id} did on the eight checks a release must pass before anyone outside the project may rely on it.`);
// "data-wording" describes how the explorer's record pages tidy notes; the guidebook has no record pages yet (phase 2 adds it back).
aboutPage("data", "release/data-and-downloads.md", "Data and downloads", "What a release contains, how to get it and cite it, and the caveats to keep with it.", ["data-wording"]);
aboutPage("corrections", "contribute/corrections-and-contributing.md", "Corrections and contributing", "How to report an error, report misuse, or suggest a role or task that EMST is missing.");

// What EMST covers: the explorer's scope map, one page per area
const covSec = Object.fromEntries(cov.sections.map((s) => [s.id, s]));
const draftText = covSec["cov-map"].blocks.find((b) => b.t === "draft")?.text || "";
const covBody = [
  `${esc(COPY.coverage.lede)} ${esc(fill(COPY.coverage.modules, { n: V.modulesWithRoles, total: V.modules }))}`, esc(COPY.coverage.purpose),
  ...cov.sections.map((s) => blocksMd([{ t: "h2", id: s.id, text: s.title }, ...s.blocks.filter((b) => b.t !== "area")], s.id)
    + (s.id === "cov-map" ? `\n\n### ${esc("Each area's page")}\n\n${s.blocks.filter((b) => b.t === "area").map((b) => blocksMd([b])).join("\n")}` : "")),
].join("\n\n");
add(`${COV_DIR}/README.md`, COPY.coverage.title, "Where EMST has roles, where it has only competencies and tasks, and where it has nothing yet.", covBody);
for (const b of areaBlocks) {
  const Cc = cov.cols;
  const rows = (b.rows || []).map((r) => [esc(r.label), `${esc(r.module)}${r.wave ? ` (${esc(r.wave)})` : ""}`, esc(r.roles),
    `${esc(r.comps)}${r.shared ? ` (${esc(r.shared)})` : ""}${r.links?.length ? `: ${r.links.map(inline).join("; ")}` : ""}`,
    `${esc(r.tasks)}${r.shared ? ` (${esc(r.shared)})` : ""}`, esc(cov.status[r.st])]);
  const roles = b.roles?.length
    ? b.roles.map(([m, items]) => `### ${esc(m)}\n\n${items.map((x) => `- ${inline(x)}`).join("\n")}`).join("\n\n")
    : inline(b.noRoles || "");
  add(AREA_PAGE[b.id], b.label, `${b.label}: the subsectors in this area of EMST's scope map, their subject modules, and the roles EMST has for them.`, [
    inline(b.summary), hint("info", inline(draftText)),
    `## Subsectors\n\n${tableMd([Cc.sub, Cc.module, b.rolesHead, Cc.comps, Cc.tasks, Cc.status], rows)}\n\n${esc(cov.tableHint)} [How to read the counts](page:${COV_DIR}/README.md#${slug("How to read the counts")})`,
    `## ${esc(cov.rolesBy)}\n\n${roles}`,
  ].join("\n\n"));
}

// ---------------------------------------------------------------- navigation
const NAV = [
  [null, ["README.md"]],
  ["Start here", ["start-here/what-emst-is.md", [`${COV_DIR}/README.md`, areaBlocks.map((b) => AREA_PAGE[b.id])], "start-here/how-emst-was-made.md"]],
  ["By what you need", ["by-need/describe-the-work.md", "by-need/develop-people-and-programs.md", "by-need/find-my-next-move.md", "by-need/anticipate-change.md", "by-need/use-check-and-improve-the-data.md"]],
  ["How to read EMST", ["how-to-read/README.md", ...READ_PAGES.map(([p]) => p), "how-to-read/held-records.md", "how-to-read/glossary.md"]],
  ["How EMST works", ["how-emst-works/README.md", "how-emst-works/the-three-crafts.md", "how-emst-works/how-change-is-tracked.md", "how-emst-works/who-decides.md", "how-emst-works/version-1.md"]],
  ["About this release", ["release/status.md", "release/data-and-downloads.md", "release/about-this-guidebook.md", "release/accessibility.md", "release/privacy.md"]],
  ["Contribute", ["contribute/corrections-and-contributing.md"]],
];
const navLine = (p, depth) => { const pg = PAGES.get(p); if (!pg) { problems.push(`navigation names a missing page ${p}`); return ""; } return `${"  ".repeat(depth)}* [${esc(pg.title)}](${p})`; };
const summary = ["# Table of contents", ""];
for (const [group, items] of NAV) {
  if (group) summary.push("", `## ${group}`, "");
  for (const it of items) {
    if (Array.isArray(it)) { summary.push(navLine(it[0], 0)); for (const c of it[1]) summary.push(navLine(c, 1)); } else summary.push(navLine(it, 0));
  }
}
const inNav = new Set(NAV.flatMap(([, items]) => items.flatMap((x) => (Array.isArray(x) ? [x[0], ...x[1]] : [x]))));
for (const p of PAGES.keys()) if (!inNav.has(p)) problems.push(`page not in navigation: ${p}`);

// ---------------------------------------------------------------- render
const explorerOffline = new Set();
// While the explorer is offline, a link that is a whole sentence on its own ("Browse the roles", "See them in What's
// changing") would read as a stray phrase, so it is dropped; a link inside a sentence keeps its words as plain text.
const LONE_EXPLORER = /(^|(?<=[.!?”)]) )\[(?:\\\]|[^\]\n])+\]\(explorer(?:-cta)?:[^)\s]*\)\.?(?=[ \t]*(?:$|\|))/gm;
function resolveLinks(md, from) {
  if (!CFG.explorerUrl) {
    const before = md;
    md = md.replace(LONE_EXPLORER, "").replace(/[ \t]+$/gm, "").replace(/\n{3,}/g, "\n\n");
    if (md !== before) explorerOffline.add(from);
  }
  return md.replace(/\[((?:\\\]|[^\]\n])+)\]\(((?:page|explorer(?:-cta)?):[^)\s]*)\)/g, (all, text, href) => {
    if (href.startsWith("page:")) {
      const [p, a] = href.slice(5).split("#");
      if (!PAGES.has(p)) problems.push(`${from}: link to a missing page ${p}`);
      return `[${text}](${rel(from, p)}${a ? `#${a}` : ""})`;
    }
    const route = href.replace(/^explorer(?:-cta)?:/, "") || "/";
    if (CFG.explorerUrl) return `[${text}](${CFG.explorerUrl.replace(/\/$/, "")}/#${route})`;
    explorerOffline.add(from);
    return text;
  });
}
const yamlStr = (s) => `"${String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"')}"`;
function render(path, pg) {
  const ai = "how-to-read/drafted-by-ai-agents.md";
  const ribbon = `${fill(COPY.site.ribbon.release, { id: R.id })}. ${COPY.site.ribbon.ai}.${path === ai ? "" : ` [${COPY.site.ribbon.link}](page:${ai})`}`;
  let body = resolveLinks(pg.body, path);
  const foot = [];
  if (explorerOffline.has(path)) foot.push(`The EMST explorer is not online yet. Names of explorer pages and records on this page will become links when it is. Until then, the records are in the release files on [GitHub](${CFG.repo}).`);
  foot.push(`Built from EMST release ${R.id}, ${vars.releaseDate}. [Report a problem with this page](${CFG.issues}) on GitHub (free account needed). ${COPY.site.notGov} Text: CC BY 4.0. Data: CC0 1.0.`);
  body = `${hint("info", resolveLinks(ribbon, path))}\n\n${body}\n\n---\n\n${foot.join("\n\n")}`;
  return `---\ndescription: ${yamlStr(pg.description)}\n---\n\n# ${esc(pg.title)}\n\n${body}\n`;
}
const files = new Map();
files.set(".gitbook.yaml", "# GitBook Git Sync configuration for the EMST guidebook. Generated by tools/build-gitbook.mjs; do not edit.\nroot: ./\n\nstructure:\n  readme: README.md\n  summary: SUMMARY.md\n");
for (const [p, pg] of PAGES) files.set(p, render(p, pg));
files.set("SUMMARY.md", `${summary.join("\n").replace(/\n{3,}/g, "\n\n")}\n`);

if (missing.size) problems.push(...[...missing].map((m) => `unknown token ${m}`));
if (problems.length) { console.error(`[build-gitbook] ${problems.length} problem(s):\n  ${problems.join("\n  ")}`); process.exit(1); }

// ---------------------------------------------------------------- write, or compare
const writeAll = (dir) => { for (const [p, text] of files) { mkdirSync(dirname(join(dir, p)), { recursive: true }); writeFileSync(join(dir, p), text); } };
const listAll = (dir, base = dir) => (existsSync(dir) ? readdirSync(dir).flatMap((f) => { const full = join(dir, f); return statSync(full).isDirectory() ? listAll(full, base) : [posix.join(...full.slice(base.length + 1).split(/[\\/]/))]; }) : []);
if (CHECK) {
  const tmp = mkdtempSync(join(tmpdir(), "emst-gitbook-"));
  writeAll(tmp);
  const a = new Set(listAll(SITE)), b = new Set(listAll(tmp));
  const diff = [...new Set([...a, ...b])].filter((f) => !a.has(f) || !b.has(f) || readFileSync(join(SITE, f), "utf8") !== readFileSync(join(tmp, f), "utf8"));
  rmSync(tmp, { recursive: true, force: true });
  if (diff.length) { console.error(`[build-gitbook --check] gitbook/site differs from a fresh build in ${diff.length} file(s):\n  ${diff.slice(0, 30).join("\n  ")}\nRebuild it, and make any fix in gitbook/src or the release data, not in gitbook/site.`); process.exit(1); }
  console.log(`[build-gitbook --check] gitbook/site matches a fresh build (${files.size} files).`);
} else {
  rmSync(SITE, { recursive: true, force: true });
  writeAll(SITE);
  console.log(`[build-gitbook] wrote ${PAGES.size} pages, SUMMARY.md and .gitbook.yaml to ${posix.relative(ROOT.split("\\").join("/"), SITE.split("\\").join("/"))}${explorerOffline.size ? `; explorer links written as plain text on ${explorerOffline.size} pages (config explorerUrl is not set)` : ""}`);
}
