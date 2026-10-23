#!/usr/bin/env node
// Vendor the USWDS 3 assets the explorer uses into src/assets/vendor/uswds/ so the built site makes no runtime
// third-party requests (ADR-0012 standing rules; mvp_spec §2.4 rule 4). Only the compiled stylesheet and the files it
// references are copied; USWDS JavaScript is not used (native <details> and a small first-party script instead).
// Refuses to vendor a stylesheet that references an absolute or protocol-relative URL. Licence: Apache-2.0.
import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const SITE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PKG = join(SITE, "node_modules", "@uswds", "uswds");
const DIST = join(PKG, "dist");
const OUT = join(SITE, "src", "assets", "vendor", "uswds");

if (!existsSync(DIST)) {
  console.error("USWDS is not installed; run `npm ci --ignore-scripts` first.");
  process.exit(1);
}
const version = JSON.parse(readFileSync(join(PKG, "package.json"), "utf-8")).version;
const css = readFileSync(join(DIST, "css", "uswds.min.css"), "utf-8");
const refs = [...css.matchAll(/url\(\s*['"]?([^'")]*)['"]?\s*\)/g)].map((m) => m[1]).filter((u) => u && !u.startsWith("data:"));
const external = refs.filter((u) => /^(https?:)?\/\//i.test(u));
if (external.length) {
  console.error("USWDS stylesheet references external URLs; refusing to vendor:", external);
  process.exit(1);
}
const copied = [];
function copy(rel) {
  const src = normalize(join(DIST, "css", rel.split(/[?#]/)[0]));
  if (!src.startsWith(DIST)) throw new Error(`path escapes dist: ${rel}`);
  const dst = join(OUT, src.slice(DIST.length + 1));
  if (!existsSync(src)) { console.warn(`[vendor] referenced file missing in package: ${rel}`); return; }
  mkdirSync(dirname(dst), { recursive: true });
  copyFileSync(src, dst);
  copied.push(src.slice(DIST.length + 1));
}
mkdirSync(join(OUT, "css"), { recursive: true });
writeFileSync(join(OUT, "css", "uswds.min.css"), css.replace(/\/\*# sourceMappingURL=.*?\*\//g, ""));
for (const r of new Set(refs)) copy(r);
for (const f of ["LICENSE.md", "README.md"]) {
  if (existsSync(join(PKG, f))) copyFileSync(join(PKG, f), join(OUT, f === "README.md" ? "USWDS-README.md" : f));
}
// Font licences travel with the fonts (SIL OFL).
for (const fam of readdirSync(join(DIST, "fonts"))) {
  const d = join(DIST, "fonts", fam);
  for (const f of readdirSync(d)) {
    if (/licen[cs]e|ofl/i.test(f)) { mkdirSync(join(OUT, "fonts", fam), { recursive: true }); copyFileSync(join(d, f), join(OUT, "fonts", fam, f)); }
  }
}
writeFileSync(join(OUT, "VENDORED.json"), JSON.stringify({ package: "@uswds/uswds", version, files: ["css/uswds.min.css", ...copied.sort()] }, null, 1));
console.log(`[vendor] USWDS ${version}: stylesheet + ${copied.length} referenced files -> ${OUT}`);
