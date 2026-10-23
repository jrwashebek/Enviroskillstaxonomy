#!/usr/bin/env node
// Generate the explorer's SBOMs with npm's built-in CycloneDX writer (no extra dependency):
//   security/sbom-runtime.cdx.json  production dependency tree (what the shipped assets come from)
//   security/sbom-build.cdx.json    full tree including build and test tooling (never shipped)
// Licence: Apache-2.0.
import { spawnSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
const SITE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
mkdirSync(join(SITE, "security"), { recursive: true });
for (const [name, extra] of [["sbom-runtime.cdx.json", ["--omit", "dev"]], ["sbom-build.cdx.json", []]]) {
  const r = spawnSync("npm", ["sbom", "--sbom-format", "cyclonedx", ...extra], { cwd: SITE, encoding: "utf-8", maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) { console.error(`[sbom] npm sbom failed: ${r.stderr}`); process.exit(1); }
  const doc = JSON.parse(r.stdout);
  writeFileSync(join(SITE, "security", name), JSON.stringify(doc, null, 1));
  console.log(`[sbom] ${name}: ${(doc.components || []).length} components`);
}
