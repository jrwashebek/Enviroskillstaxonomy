#!/usr/bin/env node
// Prepare the EMST release build the explorer is generated from (WP-12).
//
// The site never reads data/v2/ itself. It reads a release build produced by scripts/build_release.py, so the release
// gate (Tribal hold, third-party licence, quarantined signals, placeholder targets, personal-data checks) has already
// run before any page exists. Until IDs are minted (WP-16) only the `preview` profile contains records, so the explorer
// says on every page that it shows an internal preview of drafts, not a release.
//
//   EMST_RELEASE_DIR=/path/to/dist/2.0.0-rc.1 npm run build   use an existing release build (nothing is rebuilt)
//   npm run release -- --refresh                              force a fresh preview build into site/.cache/release
//
// A preview build is reused while data/, vocab/, validation/display_gates.yaml and scripts/ are older than it.
// If a fresh build fails (for example validation errors while another work package is mid-edit), the previous build is
// kept and the failure is recorded in .cache/release-meta.json, which the site prints on every page.
//
// Federal applicability (ADR-0016 §3-4) is a computed view. build_release.py does not emit it yet (CR-SC-001,
// CR-CP-001), so this step runs the WP-05 prototype computation into .cache/venue/ and the site labels it a prototype.
// Licence: Apache-2.0.
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, statSync, writeFileSync, readFileSync, rmSync, renameSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const SITE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const ROOT = resolve(SITE, "..");
const CACHE = join(SITE, ".cache");
const VERSION = process.env.EMST_VERSION || "2.0.0-dev";
const PROFILE = process.env.EMST_PROFILE || "preview";
const refresh = process.argv.includes("--refresh");
const python = process.env.PYTHON || "python3";

mkdirSync(CACHE, { recursive: true });

function newestMtime(dir, skip = new Set(["__pycache__", ".pytest_cache"])) {
  let t = 0;
  if (!existsSync(dir)) return 0;
  const st = statSync(dir);
  if (st.isFile()) return st.mtimeMs;
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (skip.has(e.name)) continue;
    const p = join(dir, e.name);
    t = Math.max(t, e.isDirectory() ? newestMtime(p, skip) : statSync(p).mtimeMs);
  }
  return t;
}

const meta = { version: VERSION, profile: PROFILE, source: null, builtAt: null, buildOk: true, warning: null, venue: null };
let releaseDir;

if (process.env.EMST_RELEASE_DIR) {
  releaseDir = resolve(process.env.EMST_RELEASE_DIR);
  if (!existsSync(join(releaseDir, "emst.bundle.jsonld"))) {
    console.error(`EMST_RELEASE_DIR has no emst.bundle.jsonld: ${releaseDir}`);
    process.exit(1);
  }
  meta.source = "external";
} else {
  releaseDir = join(CACHE, "release");
  const bundle = join(releaseDir, "emst.bundle.jsonld");
  const inputs = Math.max(
    newestMtime(join(ROOT, "data", "v2")),
    newestMtime(join(ROOT, "vocab")),
    newestMtime(join(ROOT, "scripts")),
    newestMtime(join(ROOT, "validation", "display_gates.yaml")),
  );
  const have = existsSync(bundle);
  const stale = have && statSync(bundle).mtimeMs < inputs;
  if (!have || stale || refresh) {
    console.log(`[release] ${have ? (refresh ? "refresh requested" : "inputs changed") : "no cached build"}: running scripts/build_release.py --profile ${PROFILE} (takes a few minutes)`);
    const tmp = join(CACHE, "release.tmp");
    rmSync(tmp, { recursive: true, force: true });
    const r = spawnSync(python, [join(ROOT, "scripts", "build_release.py"), "--profile", PROFILE, "--version", VERSION, "--out", tmp],
      { cwd: ROOT, stdio: ["ignore", "inherit", "inherit"], env: { ...process.env } });
    if (r.status === 0 && existsSync(join(tmp, "emst.bundle.jsonld"))) {
      rmSync(releaseDir, { recursive: true, force: true });
      renameSync(tmp, releaseDir);
      meta.builtAt = new Date().toISOString();
    } else if (have) {
      meta.buildOk = false;
      meta.warning = "The latest data did not pass scripts/build_release.py; this site shows the previous preview build.";
      console.warn(`[release] build failed (exit ${r.status}); keeping the previous build. ${meta.warning}`);
    } else {
      console.error("[release] build failed and no previous build exists. Run `python scripts/validate_v2.py` in the repo root.");
      process.exit(1);
    }
  } else {
    console.log("[release] cached preview build is current");
  }
  meta.source = "preview-cache";
}

// Computed venue applicability (prototype until CR-SC-001 / CR-CP-001 are ruled).
const venueInRelease = join(releaseDir, "views", "venue_applicability.json");
const venueDir = join(CACHE, "venue");
if (existsSync(venueInRelease)) {
  meta.venue = { source: "release-view", path: venueInRelease };
} else {
  const proto = join(ROOT, "docs", "build", "WP-05", "ci", "venue_applicability.py");
  mkdirSync(venueDir, { recursive: true });
  let asOf = "2026-10-23";
  try {
    const notes = readFileSync(join(releaseDir, "RELEASE_NOTES.md"), "utf-8");
    const m = notes.match(/Released: (\d{4}-\d{2}-\d{2})/);
    if (m) asOf = m[1];
  } catch { /* keep default */ }
  // Preferred: the registered rule venue-applicability@1.0.0 (scripts/rules/venue_applicability.py) applied to the
  // release bundle by site/tools/venue_view.py. Fallback: the WP-05 prototype (never shows "required-basis").
  const viaRule = spawnSync(python, [join(SITE, "tools", "venue_view.py"), releaseDir, join(venueDir, "venue_applicability.json"), "--as-of", asOf],
    { cwd: ROOT, stdio: ["ignore", "inherit", "inherit"] });
  if (viaRule.status === 0) {
    meta.venue = { source: "rule-over-release", path: join(venueDir, "venue_applicability.json"), asOf, rule: "venue-applicability@1.0.0" };
  } else if (existsSync(proto)) {
    mkdirSync(venueDir, { recursive: true });
    const r = spawnSync(python, [proto, "--as-of", asOf, "--out", venueDir], { cwd: ROOT, stdio: ["ignore", "inherit", "inherit"] });
    meta.venue = r.status === 0
      ? { source: "wp05-prototype", path: join(venueDir, "venue_applicability.csv"), asOf, script: "docs/build/WP-05/ci/venue_applicability.py" }
      : { source: "unavailable" };
  } else {
    meta.venue = { source: "unavailable" };
  }
}

// Generated HR views (Federal Series Profile, State Class View). Prefer views shipped in the release build; until
// build_release.py emits them (CR-FH-001, CR-CP-001) read WP-08's generated output read-only. The model drops any
// record those views name that is not in the release bundle, so held or excluded content cannot enter a page.
const hrInRelease = join(releaseDir, "views", "federal-series");
const hrWp08 = process.env.EMST_HR_VIEWS_DIR || join(ROOT, "docs", "build", "WP-08", "generated");
if (existsSync(join(hrInRelease, "index.json"))) meta.hrViews = { source: "release-view", dir: join(releaseDir, "views") };
else if (existsSync(join(hrWp08, "federal-series", "index.json"))) meta.hrViews = { source: "wp08-generated", dir: hrWp08 };
else meta.hrViews = { source: "unavailable" };

meta.releaseDir = releaseDir;
writeFileSync(join(CACHE, "release-meta.json"), JSON.stringify(meta, null, 1));
console.log(`[release] using ${releaseDir} (${meta.source}); venue applicability: ${meta.venue.source}; HR views: ${meta.hrViews.source}`);
