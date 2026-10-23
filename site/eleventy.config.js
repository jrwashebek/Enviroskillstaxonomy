// Eleventy 3 configuration for the EMST Tier 1 explorer (WP-12). Licence: Apache-2.0.
// Pages are generated from one release build (see tools/prepare-release.mjs); nothing is hand-typed into a page.
import { readFileSync, existsSync } from "node:fs";
import { join, resolve, dirname, relative, posix } from "node:path";
import { fileURLToPath } from "node:url";
import { buildModel, en, slugOf, figureOf } from "./lib/model.mjs";

const SITE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(SITE, "..");

export default async function (cfg) {
  const metaPath = join(SITE, ".cache", "release-meta.json");
  if (!existsSync(metaPath)) throw new Error("No release prepared: run `npm run build` (or `npm run release`) first.");
  const meta = JSON.parse(readFileSync(metaPath, "utf-8"));
  const model = buildModel({ root: ROOT, releaseDir: meta.releaseDir, meta });
  cfg.addGlobalData("emst", model);
  cfg.addGlobalData("site", {
    title: "EMST Explorer",
    portable: process.env.EMST_PORTABLE === "1",
    csp: "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; media-src 'none'; object-src 'none'; frame-src 'none'; worker-src 'none'; manifest-src 'none'; base-uri 'none'; form-action 'none'",
  });

  cfg.addPassthroughCopy({ "src/assets": "assets" });
  cfg.addPassthroughCopy({ "security/sbom-runtime.cdx.json": "download/security/sbom-runtime.cdx.json", "security/sbom-build.cdx.json": "download/security/sbom-build.cdx.json" });
  const rel = meta.releaseDir;
  for (const f of ["RELEASE_NOTES.md", "SHA256SUMS", "csv/competencies.csv", "csv/tasks.csv", "csv/indicators.csv", "csv/task_competency_links.csv", "csv/hcm_skills_library.csv", "csv/mappings.csv", "csv/datapackage.json"]) {
    if (existsSync(join(rel, f))) cfg.addPassthroughCopy({ [relative(SITE, join(rel, f))]: `download/release/${f}` });
  }

  // ------------------------------------------------------------------ filters
  cfg.addFilter("en", en);
  cfg.addFilter("fig", figureOf);
  cfg.addFilter("slug", slugOf);
  cfg.addFilter("json", (v) => JSON.stringify(v).replace(/</g, "\\u003c"));
  cfg.addFilter("pct", (v) => (v == null || Number.isNaN(v) ? "not set" : `${Math.round(v * 100)}%`));
  cfg.addFilter("label", (code, map) => (map && map[code]) || code || "");
  cfg.addFilter("where", (arr, k, v) => (arr || []).filter((x) => x && x[k] === v));
  cfg.addFilter("whereNot", (arr, k, v) => (arr || []).filter((x) => x && x[k] !== v));
  cfg.addFilter("take", (arr, n) => (arr || []).slice(0, n));
  cfg.addFilter("sumBy", (arr, k) => (arr || []).reduce((s, x) => s + (Number(x?.[k]) || 0), 0));
  cfg.addFilter("groupBy", (arr, k) => {
    const m = new Map();
    for (const x of arr || []) { const key = x?.[k] ?? ""; if (!m.has(key)) m.set(key, []); m.get(key).push(x); }
    return [...m.entries()].map(([key, items]) => ({ key, items }));
  });
  cfg.addFilter("uniq", (arr) => [...new Set(arr || [])]);
  cfg.addFilter("titlecase", (s) => String(s || "").replace(/(^|[-\s])([a-z])/g, (m, p, c) => p.replace("-", " ") + c.toUpperCase()));
  cfg.addFilter("barWidth", (share, total, width) => (total > 0 ? Math.max(0, Math.round((share / total) * width)) : 0));
  cfg.addFilter("sharedText", (e) => `Shares ${e.shared} of ${e.destCount} destination competencies at the destination's target level`);
  cfg.addFilter("external", (u) => /^https?:\/\//.test(String(u || "")));
  cfg.addFilter("levelsFor", (comp) => (comp?.levels || []).map((l) => l.level));
  cfg.addFilter("tierText", (t) => ({ exploratory: "Exploratory: foresight and curriculum exploration; not for decisions", describe: "Describe: workforce analytics, planning, curriculum mapping", develop: "Develop: training, task books, IDPs, self-assessment", select: "Select: hiring and promotion input" })[t] || t);
  cfg.addFilter("capText", (c) => ({ levelRule: "limited by the level rule: indicator levels not yet placed by a panel", evidence: "limited by validation evidence not yet met", declaredCeiling: "limited by the author's declared ceiling", lifecycle: "limited by its lifecycle state", lint: "limited by indicator lint", pathway: "limited by the pathway rule" })[c] || (c ? `limited by ${c}` : ""));
  cfg.addFilter("sentence", (s) => { s = String(s || ""); return s.charAt(0).toUpperCase() + s.slice(1); });
  cfg.addFilter("dateOnly", (s) => String(s || "").slice(0, 10));
  // SKOS match predicates in plain words (package review issue 6): "A broadMatch B" means B is broader than A.
  cfg.addFilter("match", (p, noun = "term") => {
    const k = String(p || "").replace(/^skos:/, "");
    return ({ exactMatch: "exact fit", closeMatch: "close fit", broadMatch: `broader ${noun}`, narrowMatch: `more specific ${noun}`, relatedMatch: "partial fit" })[k]
      || k.replace(/([a-z])([A-Z])/g, "$1 $2").toLowerCase();
  });

  // Optional portable build: every link becomes relative so the folder works from disk (file://) or any sub-path.
  if (process.env.EMST_PORTABLE === "1") {
    cfg.addTransform("portable-links", function (content) {
      const out = this.page.outputPath;
      if (!out || !out.endsWith(".html")) return content;
      const fromDir = posix.dirname("/" + posix.relative(posix.join(SITE, "_site"), out.split("\\").join("/")));
      return content.replace(/(\s(?:href|src))="(\/[^"#?]*)([#?][^"]*)?"/g, (m, attr, p, tail = "") => {
        let target = p.endsWith("/") ? p + "index.html" : p;
        let r = posix.relative(fromDir, target) || "index.html";
        return `${attr}="${r}${tail}"`;
      });
    });
  }

  return {
    dir: { input: "src", output: "_site", includes: "_includes", data: "_data" },
    templateFormats: ["njk"],
    htmlTemplateEngine: "njk",
    pathPrefix: process.env.EMST_PATH_PREFIX || "/",
  };
}
