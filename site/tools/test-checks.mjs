#!/usr/bin/env node
// Seeded-violation test for tools/check-output.mjs: each fixture page breaks one rule, and the checker must report
// that rule. A checker that passes everything would otherwise look like a clean site. Licence: Apache-2.0.
import { spawnSync } from "node:child_process";
import { mkdirSync, readFileSync, rmSync, writeFileSync, copyFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const SITE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const FIX = join(SITE, ".cache", "check-fixtures");
const good = readFileSync(join(SITE, "_site", "evidence", "index.html"), "utf-8");
const seeds = {
  A1: (h) => h.replace("</main>", '<img src="https://example.org/pixel.gif" alt=""></main>'),
  A2: (h) => h.replace("</head>", '<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=X"></head>'),
  A3: (h) => h.replace("</main>", '<iframe title="x" src="/x"></iframe></main>'),
  A4: (h) => h.replace("</main>", '<a href="https://example.org/?q=user">x</a></main>'),
  B1: (h) => h.replace(/<meta http-equiv="Content-Security-Policy"[^>]*>/, ""),
  B2: (h) => h.replace("</main>", "<script>console.log(1)</script></main>"),
  B3: (h) => h.replace("<main ", '<main onclick="x()" '),
  C1: (h) => h.replace(/<meta name="emst-release"[^>]*>/, ""),
  D1: (h) => h.replace("</main>", '<figure data-figure data-use-tier="describe" data-evidence="S"><figcaption>42 tasks</figcaption></figure></main>'),
  D2: (h) => h.replace("</main>", "<p>v1 automation type: A (Augmentation)</p></main>"),
  "D3-C01": (h) => h.replace("</main>", "<p>The taxonomy was validated against OPM classification systems.</p></main>"),
  "D3-C06": (h) => h.replace("</main>", "<p>This is the recommended pathway for technicians.</p></main>"),
  "D3-C09": (h) => h.replace("</main>", "<p>Series 0029 was realigned to 0303.</p></main>"),
  "D3-C12": (h) => h.replace("</main>", "<p>These competencies are validated by practitioners.</p></main>"),
  D4: (h) => h.replace("</main>", "<p>Tribal consultation tasks are listed here.</p></main>"),
  "D6-P01": (h) => h.replace("</main>", "<p>Contact jane.doe@example.org</p></main>"),
  E2: (h) => h.replace("</main>", "<p>Fix Our Forests Act (H.R. 471 / S. 1462): in force since 2026.</p></main>"),
  E3: (h) => h.replace("</main>", "<p>FAST-41: 2015-12-04 enacted.</p></main>"),
  E4: (h) => h.replace("</main>", "<p>The aligned standards take effect in 2027; NWCG is not a party.</p><p>AEI shows 77% of tasks are automated.</p></main>"),
};
let failed = 0;
for (const [rule, f] of Object.entries(seeds)) {
  rmSync(FIX, { recursive: true, force: true });
  mkdirSync(join(FIX, "evidence"), { recursive: true });
  writeFileSync(join(FIX, "evidence", "index.html"), f(good));
  const r = spawnSync(process.execPath, [join(SITE, "tools", "check-output.mjs"), FIX], { encoding: "utf-8" });
  const rep = JSON.parse(readFileSync(join(SITE, "reports", "check-output.json"), "utf-8"));
  const hit = rep.problems.some((p) => p.rule === rule || p.rule.startsWith(rule));
  if (r.status === 0 || !hit) { failed++; console.error(`[test-checks] seeded ${rule} NOT detected`); }
}
// The unmodified page must pass.
rmSync(FIX, { recursive: true, force: true });
mkdirSync(join(FIX, "evidence"), { recursive: true });
writeFileSync(join(FIX, "evidence", "index.html"), good);
const ok = spawnSync(process.execPath, [join(SITE, "tools", "check-output.mjs"), FIX], { encoding: "utf-8" });
if (ok.status !== 0) { failed++; console.error("[test-checks] clean fixture failed:", ok.stderr.slice(0, 400)); }
rmSync(FIX, { recursive: true, force: true });
if (failed) { console.error(`[test-checks] ${failed} seeded cases failed`); process.exit(1); }
console.log(`[test-checks] OK: ${Object.keys(seeds).length} seeded violations detected; clean page passes`);
