#!/usr/bin/env node
// Static checks on the built explorer (_site/). Fails the build (exit 1) on any violation. Licence: Apache-2.0.
//
//  A. No runtime third-party fetches: no absolute or protocol-relative URL in any src/srcset/poster/data/<link href>/
//     <form action>/<base>/<meta refresh>/<iframe>/<embed>/<object>, CSS url()/@import, or JS import; <a href> to
//     other sites is a navigation the user chooses and is allowed (counted, must not carry query strings).
//  B. No network, storage or address-bar APIs in shipped JavaScript; no inline executable script; CSP meta with
//     connect-src 'none' and form-action 'none' on every page.
//  C. Release ID and the use notice on every page.
//  D. Claims hygiene (ADR-0027 §3; P-CP-09): banned claims; every [data-figure] carries a use-tier and an evidence badge;
//     v1 codes only inside the v1 evidence drawer; HR disclaimers on series, class and federal/state variant pages;
//     "assessment pending" on role-change pages; pathways never "recommended"; no Tribal variant pages; Tribal-hold
//     trigger terms only inside marked policy statements; no held seed key; no e-mail address or phone number.
// Writes reports/check-output.json and, when everything passes, _site/download/security/SITE_SHA256SUMS.
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, readdirSync, statSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join, relative, resolve, extname } from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const SITE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const ROOT = resolve(SITE, "..");
const OUT = resolve(process.argv[2] || join(SITE, "_site"));
const problems = [];
const stats = { pages: 0, files: 0, externalLinks: 0, figures: 0, v1Drawers: 0 };
const fail = (file, rule, msg) => problems.push({ file: relative(OUT, file), rule, msg: String(msg).slice(0, 300) });

function walk(d) { return readdirSync(d, { withFileTypes: true }).flatMap((e) => e.isDirectory() ? walk(join(d, e.name)) : [join(d, e.name)]); }
const files = walk(OUT).filter((f) => !f.endsWith("SITE_SHA256SUMS"));
stats.files = files.length;

const ABS = /^\s*(?:[a-z][a-z0-9+.-]*:)?\/\//i;           // http://, https://, //host, any scheme://
const NONLOCAL_SCHEME = /^\s*(?:https?|ftp|ws|wss):/i;
const isRemote = (u) => ABS.test(u) || NONLOCAL_SCHEME.test(u);

// ---------------------------------------------------------------- helpers
function stripScriptsAndStyles(html) { return html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ").replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " "); }
function decode(s) { return s.replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#x27;/g, "'").replace(/&#(\d+);/g, (m, n) => String.fromCharCode(Number(n))); }
function textOf(html) { return decode(stripScriptsAndStyles(html).replace(/<[^>]+>/g, " ")).replace(/\s+/g, " "); }
// Remove every element that carries `attr` (balanced on its own tag name).
function removeElementsWith(html, attrRx) {
  let out = html, guard = 0;
  for (;;) {
    const m = out.match(new RegExp(`<([a-z0-9]+)\\b[^>]*\\b${attrRx}[^>]*>`, "i"));
    if (!m || guard++ > 5000) return out;
    const start = m.index, tag = m[1].toLowerCase();
    const end = findClose(out, start, tag);
    out = out.slice(0, start) + out.slice(end);
  }
}
function findClose(html, start, tag) {
  const rx = new RegExp(`<(/?)${tag}\\b[^>]*>`, "gi");
  rx.lastIndex = start;
  let depth = 0, m;
  while ((m = rx.exec(html))) {
    if (/\/>$/.test(m[0]) && !m[1]) continue;
    depth += m[1] ? -1 : 1;
    if (depth === 0) return rx.lastIndex;
  }
  return html.length;
}
function elementsWith(html, attrRx) {
  const res = [];
  const rx = new RegExp(`<([a-z0-9]+)\\b([^>]*\\b${attrRx}(?:[\\s=>][^>]*)?)>`, "gi");
  let m;
  while ((m = rx.exec(html))) {
    const end = findClose(html, m.index, m[1].toLowerCase());
    res.push({ open: m[0], body: html.slice(m.index, end) });
  }
  return res;
}

// ---------------------------------------------------------------- inputs for content rules
const gc = yaml.load(readFileSync(join(ROOT, "schema", "lint", "governed_content.yaml"), "utf-8"));
const tribal = gc.tribal_hold.triggers.map((p) => typeof p === "string" ? new RegExp(p, "i") : new RegExp(p.pattern, p.cs ? "" : "i"));
const holdFile = join(ROOT, "data", "v2", "governance", "tribal_hold.yaml");
const heldKeys = existsSync(holdFile) ? (yaml.load(readFileSync(holdFile, "utf-8")).heldSeedKeys || []) : [];
const heldRx = heldKeys.length ? new RegExp(`(?<![A-Za-z0-9._/:-])(?:${heldKeys.map((k) => k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})(?![A-Za-z0-9._/-])`) : null;
const meta = JSON.parse(readFileSync(join(SITE, ".cache", "release-meta.json"), "utf-8"));
const releaseId = meta.version;

const NEG = /\b(never|not|no|nor|nothing|none|without|until|unless|before|isn't|aren't|cannot|neither)\b/i;
// A claim is negated only by a negation word earlier in the same sentence (at most `win` characters back).
const negated = (text, idx, win = 80) => {
  let before = text.slice(Math.max(0, idx - win), idx);
  const cut = Math.max(before.lastIndexOf(". "), before.lastIndexOf("? "), before.lastIndexOf("! "), before.lastIndexOf("; "), before.lastIndexOf(": "));
  if (cut >= 0) before = before.slice(cut + 2);
  return NEG.test(before);
};
const CLAIMS = [
  { id: "C01", rx: /validated against (?:the )?(?:OPM|O\*NET)/gi, msg: "retired claim: validated against OPM/O*NET" },
  { id: "C02", rx: /SAF[- ]accredited/gi, msg: "retired claim: SAF-accredited" },
  { id: "C03", rx: /\b38\s?%[^.]{0,60}human[- ]essential|\bhuman[- ]essential[^.]{0,40}\b38\s?%|\b68\s?%[^.]{0,40}transition|\b77\s?%[^.]{0,80}(?:automat|API)|\b21\s?%[^.]{0,30}of tasks/gi, msg: "retired v1/AEI headline percentage" },
  { id: "C04", rx: /\b(?:215|222|292)\s+competencies\b/gi, msg: "stale v1 competency count" },
  { id: "C05", rx: /\b9 S calls\b|structural property/gi, msg: "retired v1 claim" },
  { id: "C06", rx: /\brecommended (?:pathways?|routes?|moves?|destinations?|careers?|next steps?)\b|\b(?:pathways?|routes?|moves?|destinations?) (?:is|are|was|were) recommended\b/gi, msg: "pathway described as recommended", neg: true },
  { id: "C06b", rx: /\brecommend(?:ed|s|ation)?\b/gi, msg: "recommendation language on a pathways page", neg: true, onlyUrl: /^\/pathways\// },
  { id: "C07", rx: /UGESP[- ]complian(?:t|ce)/gi, msg: "never describe validation as UGESP compliance" },
  { id: "C08", rx: /SB\s?24-205/gi, msg: "Colorado SB 24-205 cited (never took effect as written)", allowNear: /never took effect|repealed/i },
  { id: "C09", rx: /\brealigned\b|\bconsolidated into\b/gi, msg: "series shown as realigned (only proposed)", neg: true },
  { id: "C10", rx: /usindigenousdata/gi, msg: "domain must never be linked" },
  { id: "C11", rx: /1\s?[–-]\s?5 hours/gi, msg: "unconfirmed PNNL figure" },
  { id: "C12", rx: /\bvalidated (?:competenc\w*|taxonom\w*|indicators?|roles?|role profiles?|pathways?|framework|content|tasks?|profiles?|standards?)\b|\b(?:EMST|taxonomy|competencies|indicators|role profiles|pathways|this release|content)\b[^.]{0,30}\b(?:has|have|is|are|was|were) (?:been )?validated\b|\bvalidated by (?:practitioners|SMEs?|experts|(?:a )?panels?|(?:a )?Delphi)\b/gi, msg: "validation claimed for EMST content", neg: true },
  { id: "C13", rx: /\b(?:aligned|alignment|conforms?) (?:with|to) (?:the )?(?:O\*NET|ESCO|OPM)/gi, msg: "alignment claim without a reviewed set", neg: true },
  { id: "C14", rx: /\bselection[- ]grade\b|\bfor (?:hiring|selection) decisions\b/gi, msg: "selection use claimed", neg: true },
  { id: "C15", rx: /\bPolitical Savvy\b|\bInfluencing\/Negotiating\b/g, msg: "retired ECQ competency named as current", allowNear: /removed|no longer|retired|rewritten|replaced/i },
];
const PERSONAL = [
  { id: "P01", rx: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b/g, msg: "e-mail address" },
  { id: "P02", rx: /\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b/g, msg: "phone number" },
];

// ---------------------------------------------------------------- per-file checks
for (const f of files) {
  const ext = extname(f).toLowerCase();
  if (ext === ".html") {
    stats.pages++;
    const html = readFileSync(f, "utf-8");
    const url = "/" + relative(OUT, f).replace(/index\.html$/, "").split("\\").join("/");
    // A. fetches
    for (const m of html.matchAll(/<([a-z0-9]+)\b([^>]*)>/gi)) {
      const tag = m[1].toLowerCase(), attrs = m[2];
      const attr = (n) => { const a = attrs.match(new RegExp(`\\s${n}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s>]+))`, "i")); return a ? (a[2] ?? a[3] ?? a[4] ?? "") : null; };
      for (const n of ["src", "poster", "data", "action", "formaction", "background", "ping", "manifest", "icon"]) {
        const v = attr(n); if (v != null && isRemote(v)) fail(f, "A1", `<${tag} ${n}="${v}">`);
      }
      const ss = attr("srcset"); if (ss && ss.split(",").some((x) => isRemote(x.trim().split(/\s+/)[0]))) fail(f, "A1", `<${tag} srcset>`);
      if (tag === "link") { const v = attr("href"); if (v && isRemote(v)) fail(f, "A2", `<link href="${v}">`); }
      if (["iframe", "embed", "object", "frame", "portal", "base"].includes(tag)) fail(f, "A3", `<${tag}> element not allowed`);
      if (tag === "meta" && /http-equiv\s*=\s*["']?refresh/i.test(attrs)) fail(f, "A3", "meta refresh not allowed");
      if (tag === "a") {
        const v = attr("href");
        if (v && isRemote(v)) { stats.externalLinks++; if (/[?]/.test(v)) fail(f, "A4", `external link carries a query string: ${v}`); }
      }
      if (/\son[a-z]+\s*=/i.test(attrs)) fail(f, "B3", `inline event handler on <${tag}>`);
      if (/\sstyle\s*=/i.test(attrs) && tag !== "svg") fail(f, "B4", `inline style attribute on <${tag}> (blocked by CSP)`);
    }
    for (const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
      const a = m[1];
      if (/\bsrc\s*=/.test(a)) continue;
      if (!/type\s*=\s*["']application\/json["']/i.test(a)) fail(f, "B2", "inline executable <script>");
    }
    // B. CSP
    const csp = decode((html.match(/<meta http-equiv="Content-Security-Policy" content="([^"]+)"/i) || [])[1] || "");
    if (!csp) fail(f, "B1", "no CSP meta");
    else for (const d of ["default-src 'self'", "connect-src 'none'", "form-action 'none'", "object-src 'none'", "base-uri 'none'"]) if (!csp.includes(d)) fail(f, "B1", `CSP lacks ${d}`);
    if (!/<meta name="referrer" content="no-referrer">/.test(html)) fail(f, "B1", "no referrer policy meta");
    // C. release ID + notice
    if (!html.includes(`<meta name="emst-release" content="${releaseId}">`) || !html.includes(`Release ${releaseId}`)) fail(f, "C1", "release ID missing");
    if (!/not a selection instrument/i.test(html)) fail(f, "C2", "use notice missing");
    // D. content
    for (const fig of elementsWith(html, "data-figure")) {
      stats.figures++;
      if (!/data-badge="tier"/.test(fig.body) || !/data-badge="evidence"/.test(fig.body)) fail(f, "D1", `figure without use-tier and evidence badges: ${textOf(fig.open + fig.body).slice(0, 120)}`);
      if (!/data-use-tier="[a-z]+"/.test(fig.open) || !/data-evidence="[^"]+"/.test(fig.open)) fail(f, "D1", "figure lacks data-use-tier/data-evidence");
    }
    stats.v1Drawers += (html.match(/data-v1-drawer/g) || []).length;
    const outsideDrawers = textOf(removeElementsWith(html, "data-v1-drawer"));
    for (const k of ["v1 automation type:", "v1 career-ladder position:", "v1 tacit knowledge density:", "v1 horizon:", "v1 vector:"]) if (outsideDrawers.includes(k)) fail(f, "D2", `v1 code "${k}" outside the evidence drawer`);
    for (const d of elementsWith(html, "data-v1-drawer")) if (!d.body.includes("v1 single-analyst prior, LLM-assisted, unvalidated")) fail(f, "D2", "v1 drawer without the v1_prior label");
    const visible = textOf(html);
    const policyFree = textOf(removeElementsWith(html, "data-emst-policy"));
    for (const c of CLAIMS) {
      if (c.onlyUrl && !c.onlyUrl.test(url)) continue;
      for (const m of visible.matchAll(c.rx)) {
        if (c.neg && negated(visible, m.index)) continue;
        if (c.allowNear && c.allowNear.test(visible.slice(Math.max(0, m.index - 80), m.index + 320))) continue;
        fail(f, `D3-${c.id}`, `${c.msg}: "…${visible.slice(Math.max(0, m.index - 60), m.index + 60)}…"`);
      }
    }
    for (const rx of tribal) { const m = policyFree.match(rx); if (m) fail(f, "D4", `Tribal-hold trigger outside a policy statement: "…${policyFree.slice(Math.max(0, m.index - 60), m.index + 60)}…"`); }
    if (heldRx && heldRx.test(html)) fail(f, "D5", "held seed key present");
    for (const p of PERSONAL) for (const m of visible.matchAll(p.rx)) fail(f, `D6-${p.id}`, `${p.msg}: ${m[0]}`);
    const isVariant = /^\/roles\/[^/]+\/[^/]+\/$/.test(url);
    if (isVariant && !/assessment pending/i.test(visible)) fail(f, "D7", "role-change page without 'assessment pending'");
    const hr = /^\/(federal-series|state-classes)\/[^/]+\/$/.test(url) || (isVariant && /· (Federal government|State government)<\/span><\/h1>/.test(html));
    if (hr && !(/Not a classification basis/.test(visible) && /Not a job analysis/.test(visible) && /Not for RIF/.test(visible))) fail(f, "D8", "HR view without the classification/job-analysis/RIF disclaimer");
    if (/^\/pathways\//.test(url) && !/never a recommendation/i.test(visible)) fail(f, "D9", "pathways page without the exploratory notice");
    if (/\/tribal\/?$/.test(url) || /--tribal/.test(url)) fail(f, "D10", "Tribal variant page generated");
  } else if (ext === ".css") {
    const css = readFileSync(f, "utf-8");
    for (const m of css.matchAll(/url\(\s*['"]?([^'")]+)['"]?\s*\)/g)) if (isRemote(m[1])) fail(f, "A5", `css url(${m[1]})`);
    for (const m of css.matchAll(/@import\s+(?:url\()?['"]?([^'");]+)/g)) fail(f, "A5", `css @import ${m[1]}`);
  } else if (ext === ".js" || ext === ".mjs") {
    const js = readFileSync(f, "utf-8").replace(/\/\/[^\n]*/g, "").replace(/\/\*[\s\S]*?\*\//g, "");
    const banned = [
      [/\bfetch\s*\(/, "fetch()"], [/XMLHttpRequest/, "XMLHttpRequest"], [/sendBeacon/, "navigator.sendBeacon"], [/\bWebSocket\b/, "WebSocket"],
      [/\bEventSource\b/, "EventSource"], [/\bimport\s*\(/, "dynamic import()"], [/importScripts/, "importScripts"], [/serviceWorker/, "service worker"],
      [/localStorage|sessionStorage|indexedDB/, "browser storage"], [/document\.cookie/, "cookies"], [/history\.(?:push|replace)State/, "address-bar writes"],
      [/location\.(?:hash|search|href)\s*=(?!=)/, "address-bar writes"], [/new\s+Image\s*\(/, "image beacon"], [/RTCPeerConnection/, "WebRTC"],
    ];
    for (const [rx, name] of banned) if (rx.test(js)) fail(f, "B5", `shipped JavaScript uses ${name}`);
    for (const m of js.matchAll(/["'`]((?:https?:)?\/\/[^"'`\s]+)["'`]/g)) fail(f, "A6", `absolute URL literal in JS: ${m[1]}`);
  }
}

// Search index and gap data are JSON inside pages; they were covered by the HTML text and fetch checks above.
const report = { ok: problems.length === 0, release: releaseId, outDir: relative(SITE, OUT), stats, problems };
mkdirSync(join(SITE, "reports"), { recursive: true });
writeFileSync(join(SITE, "reports", "check-output.json"), JSON.stringify(report, null, 1));
if (problems.length) {
  const byRule = {};
  for (const p of problems) byRule[p.rule] = (byRule[p.rule] || 0) + 1;
  console.error(`[check] FAILED: ${problems.length} problems ${JSON.stringify(byRule)}`);
  for (const p of problems.slice(0, 40)) console.error(`  ${p.rule} ${p.file}: ${p.msg}`);
  process.exit(1);
}
// Checksums of every published file (security packet: integrity of what was reviewed).
const sums = files.map((f) => `${createHash("sha256").update(readFileSync(f)).digest("hex")}  ${relative(OUT, f).split("\\").join("/")}`).sort((a, b) => a.slice(66).localeCompare(b.slice(66)));
mkdirSync(join(OUT, "download", "security"), { recursive: true });
writeFileSync(join(OUT, "download", "security", "SITE_SHA256SUMS"), sums.join("\n") + "\n");
console.log(`[check] OK: ${stats.pages} pages, ${stats.files} files, ${stats.figures} figures with badges, ${stats.v1Drawers} v1 drawers, ${stats.externalLinks} outbound links (navigation only), 0 problems`);
