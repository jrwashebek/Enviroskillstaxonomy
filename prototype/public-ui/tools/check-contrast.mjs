#!/usr/bin/env node
// EMST design tokens: WCAG 2.x contrast check for every text/background and UI/background token pair,
// in the light theme and the dark theme. Exits 1 on any failure.
//
// Usage: node tools/check-contrast.mjs [path/to/tokens.css] [--verbose]
//
// Pairing rules (from the token names in tokens.css):
//   1. every global text token  --fg*         on every global surface --bg* and every status surface --st-*-bg   >= 4.5
//   2. every global UI token    --ui-*        on every global surface --bg*                                      >= 3.0
//   3. every group G with --G-fg* / --G-bg* / --G-ui*: each G-fg on each G-bg >= 4.5, each G-ui on each G-bg >= 3.0
//   4. every status text token  --st-*-fg     also on every global surface --bg*                                 >= 4.5
//   5. the explicit pairs in EXTRA below (inverted marks)
// Exempt: --deco-* (decorative, never carries meaning) and --cat-* (chart slots, validated with validate_palette.js).
// It also fails if the two dark-theme blocks differ, if a theme is missing a token the other has, or if
// base.css / components.css / print.css reference a custom property that tokens.css does not define.

import { readFileSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const verbose = args.includes("--verbose");
const tokensPath = resolve(args.find((a) => !a.startsWith("--")) ?? join(here, "../app/assets/css/tokens.css"));
const cssDir = dirname(tokensPath);
const css = readFileSync(tokensPath, "utf-8").replace(/\/\*[\s\S]*?\*\//g, "");

const EXTRA = [
  ["--bg-surface", "--ui-strong", 4.5, "letter in the E evidence mark and the check in a done ladder step"],
];
const EXEMPT = /^--(deco|cat)-/;

// ---- parse ------------------------------------------------------------------------------------
function blockAfter(src, selectorRe) {
  const m = selectorRe.exec(src);
  if (!m) return null;
  let i = src.indexOf("{", m.index + m[0].length - 1), depth = 0, start = i + 1;
  for (; i < src.length; i++) {
    if (src[i] === "{") depth++;
    else if (src[i] === "}" && --depth === 0) return src.slice(start, i);
  }
  return null;
}
function decls(body) {
  const out = new Map();
  for (const m of body.matchAll(/(--[a-z0-9-]+)\s*:\s*([^;]+);/gi)) out.set(m[1], m[2].trim());
  return out;
}
const lightBody = blockAfter(css, /(^|\})\s*:root\s*\{/m);
const mediaBody = blockAfter(css, /@media\s*\(prefers-color-scheme:\s*dark\)\s*\{/);
const darkMediaBody = mediaBody && blockAfter(mediaBody, /:root:not\(\[data-theme="light"\]\)\s*\{/);
const darkAttrBody = blockAfter(css, /:root\[data-theme="dark"\]\s*\{/);

const problems = [];
if (!lightBody) problems.push("no light :root block found");
if (!darkMediaBody) problems.push('no @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { ... } } block found');
if (!darkAttrBody) problems.push('no :root[data-theme="dark"] block found');
if (problems.length) { console.error(problems.join("\n")); process.exit(1); }

const light = decls(lightBody);
const darkOnly = decls(darkAttrBody);
const darkMedia = decls(darkMediaBody);
const dark = new Map([...light, ...darkOnly]); // dark inherits non-colour tokens from :root

// The two dark blocks must be identical
for (const [k, v] of darkOnly) if (darkMedia.get(k) !== v) problems.push(`dark blocks differ: ${k} is "${v}" under data-theme but "${darkMedia.get(k)}" under prefers-color-scheme`);
for (const k of darkMedia.keys()) if (!darkOnly.has(k)) problems.push(`dark blocks differ: ${k} only under prefers-color-scheme`);

// ---- colour maths --------------------------------------------------------------------------------
const HEX = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i;
// A token is a colour if its value is one, or if its name follows the colour naming scheme
// (so a mistyped colour value is reported rather than silently skipped).
const isColourToken = (name, value) => HEX.test(value) || /^(rgb|hsl|oklch|color)\(/i.test(value) || /^--(bg|fg)(-|$)|^--(ui|st)-|-(fg|bg)(-|$)/.test(name);
function resolveVal(map, v, seen = new Set()) {
  const m = /^var\((--[a-z0-9-]+)\)$/i.exec(v);
  if (!m) return v;
  if (seen.has(m[1])) return null;
  seen.add(m[1]);
  return map.has(m[1]) ? resolveVal(map, map.get(m[1]), seen) : null;
}
function rgb(hex) {
  let h = hex.slice(1);
  if (h.length === 3) h = [...h].map((c) => c + c).join("");
  return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) / 255);
}
const lum = (hex) => { const [r, g, b] = rgb(hex).map((c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4)); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };

// ---- build pairs ---------------------------------------------------------------------------------
function colourTokens(map, theme) {
  const out = new Map();
  for (const [k, raw] of map) {
    if (!isColourToken(k, raw)) continue;
    const v = resolveVal(map, raw);
    if (EXEMPT.test(k)) continue;
    if (!v || !HEX.test(v)) { problems.push(`${theme}: ${k} must resolve to a hex colour (got "${raw}")`); continue; }
    out.set(k, v);
  }
  return out;
}
function pairsFor(tokens) {
  const names = [...tokens.keys()];
  const gBg = names.filter((n) => /^--bg(-|$)/.test(n));
  const gFg = names.filter((n) => /^--fg(-|$)/.test(n));
  const gUi = names.filter((n) => /^--ui-/.test(n));
  const groups = new Map();
  for (const n of names) {
    const m = /^--([a-z0-9-]+?)-(fg|bg|ui)(?:-([a-z0-9-]+))?$/.exec(n);
    if (!m || ["bg", "fg", "ui"].includes(m[1])) continue;
    if (!groups.has(m[1])) groups.set(m[1], { fg: [], bg: [], ui: [] });
    groups.get(m[1])[m[2]].push(n);
  }
  const stBg = [...groups].filter(([g]) => g.startsWith("st-")).flatMap(([, v]) => v.bg);
  const pairs = [];
  const add = (fg, bg, min, why) => pairs.push({ fg, bg, min, why });
  for (const f of gFg) for (const b of [...gBg, ...stBg]) add(f, b, 4.5, "text on surface");
  for (const u of gUi) for (const b of gBg) add(u, b, 3, "UI mark on surface");
  for (const [g, v] of groups) {
    if (!v.bg.length) problems.push(`group "${g}" has no --${g}-bg token`);
    for (const f of v.fg) for (const b of v.bg) add(f, b, 4.5, `${g} text`);
    for (const u of v.ui) for (const b of v.bg) add(u, b, 3, `${g} UI mark`);
    if (g.startsWith("st-")) for (const f of v.fg) for (const b of gBg) add(f, b, 4.5, `${g} text on surface`);
  }
  for (const [f, b, min, why] of EXTRA) add(f, b, min, why);
  return pairs;
}

const themes = { light: colourTokens(light, "light"), dark: colourTokens(dark, "dark") };
for (const k of themes.light.keys()) if (!themes.dark.has(k)) problems.push(`dark theme is missing ${k}`);
for (const k of themes.dark.keys()) if (!themes.light.has(k)) problems.push(`light theme is missing ${k}`);

// ---- run -------------------------------------------------------------------------------------------
let total = 0, failed = 0;
for (const [theme, tokens] of Object.entries(themes)) {
  const pairs = pairsFor(tokens);
  let worst = null;
  console.log(`\n${theme.toUpperCase()} theme: ${tokens.size} colour tokens, ${pairs.length} pairs`);
  for (const p of pairs) {
    const a = tokens.get(p.fg), b = tokens.get(p.bg);
    if (!a || !b) { problems.push(`${theme}: pair ${p.fg} on ${p.bg} refers to an undefined token`); continue; }
    const r = ratio(a, b);
    total++;
    const ok = r >= p.min;
    if (!ok) failed++;
    if (!worst || r / p.min < worst.r / worst.min) worst = { ...p, r };
    if (!ok || verbose) console.log(`  ${ok ? "pass" : "FAIL"}  ${r.toFixed(2).padStart(5)}:1  (min ${p.min})  ${p.fg} ${a}  on  ${p.bg} ${b}  [${p.why}]`);
  }
  if (worst) console.log(`  closest to its limit: ${worst.fg} on ${worst.bg} at ${worst.r.toFixed(2)}:1 (min ${worst.min})`);
}

// ---- every custom property used in the stylesheets must be defined ---------------------------------
const defined = new Set([...light.keys(), ...darkOnly.keys()]);
for (const f of ["base.css", "components.css", "print.css"]) {
  const p = join(cssDir, f);
  if (!existsSync(p)) continue;
  const src = readFileSync(p, "utf-8").replace(/\/\*[\s\S]*?\*\//g, "");
  const local = new Set([...src.matchAll(/(--[a-z0-9-]+)\s*:/gi)].map((m) => m[1]));
  for (const m of src.matchAll(/var\((--[a-z0-9-]+)/gi)) if (!defined.has(m[1]) && !local.has(m[1])) problems.push(`${f} uses ${m[1]}, which tokens.css does not define`);
}

console.log(`\n${total} pairs checked, ${failed} below the minimum.`);
const uniq = [...new Set(problems)];
if (uniq.length) console.log(`${uniq.length} structural problem(s):\n  ` + uniq.join("\n  "));
console.log(`Exempt from this check: --deco-* (decorative) and --cat-* (validate with the dataviz palette validator).`);
if (failed || uniq.length) { console.log("RESULT: FAIL"); process.exit(1); }
console.log("RESULT: PASS");
