#!/usr/bin/env node
// Generate the explorer's SBOMs with npm's built-in CycloneDX writer (no extra dependency):
//   security/sbom-runtime.cdx.json  production dependency tree (what the shipped assets come from)
//   security/sbom-build.cdx.json    full tree including build and test tooling (never shipped)
// Licence: Apache-2.0.
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
const SITE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
mkdirSync(join(SITE, "security"), { recursive: true });
for (const [name, extra] of [["sbom-runtime.cdx.json", ["--omit", "dev"]], ["sbom-build.cdx.json", []]]) {
  const r = spawnSync("npm", ["sbom", "--sbom-format", "cyclonedx", ...extra], { cwd: SITE, encoding: "utf-8", maxBuffer: 64 * 1024 * 1024 });
  if (r.status !== 0) { console.error(`[sbom] npm sbom failed: ${r.stderr}`); process.exit(1); }
  const doc = JSON.parse(r.stdout);
  // npm writes a fresh random serialNumber and a wall-clock timestamp each run. Keep the committed file when nothing
  // else changed, so rebuilding the same tree leaves the tree clean (the release re-cut is one command; BUILD.md).
  const out = join(SITE, "security", name);
  const stable = (d) => JSON.stringify({ ...d, serialNumber: null, metadata: { ...(d.metadata || {}), timestamp: null } });
  let same = false;
  if (existsSync(out)) { try { same = stable(JSON.parse(readFileSync(out, "utf-8"))) === stable(doc); } catch { same = false; } }
  if (!same) writeFileSync(out, JSON.stringify(doc, null, 1));
  console.log(`[sbom] ${name}: ${(doc.components || []).length} components${same ? " (unchanged)" : ""}`);
}
