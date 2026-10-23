# EMST Explorer: security packet (Tier 1)

- **Prepared by:** CP (Security, Privacy & Government Compliance Lead), WP-12. Phase 4 draft, 2026-10-23.
- **Release covered:** whatever release the explorer was built from. The current build uses `2.0.0-dev` with the internal preview profile. The release ID is stamped on every page.
- **Status:** draft for the security reviews of pilot states and federal units. CP signs during Phase 4; the Steward signs thereafter (ADR-0027 §4).
- **Evidence labels:** [E] means a source I read, with IDs from `docs/research/compliance-product/sources.csv`. [J] means my judgment. [S] means speculation.

This packet covers the static explorer in `site/`. It does not cover Tier 2 kits, which adopters run in their own authorized systems, or any hosted personnel-data service. Tier 3 is not on the roadmap (ADR-0012).

## 1. Applicability statement

**What the explorer is.** A set of static HTML, CSS, JavaScript, font and image files generated from a public, versioned EMST release.

- **No server-side code.** There is nothing on the server that processes input.
- **Nothing to log in to.** There are no accounts or sign-in.
- **No collection or storage.** It collects, receives, stores and processes no information from or about its users.
- **Gap check runs on the device.** Ratings stay in page memory until the user saves them, and then only to the user's own disk.

| Regime | Does it apply to the Tier 1 explorer? | Basis |
|---|---|---|
| FedRAMP (FedRAMP Authorization Act; OMB M-24-15 §III; Consolidated Rules for 2026, mandatory 1 Jan 2027) | **No.** The explorer is not a cloud service that creates, collects, processes, stores or maintains Federal information on behalf of an agency. It is a widely available information resource that provides public information and collects no Federal information. That is the out-of-scope case M-24-15 describes. Each agency makes its own determination. | [E: CP-015, CP-016, CP-018; J] |
| FISMA / agency ATO (NIST SP 800-37) | **No new ATO for reading the public site or downloading releases.** Ordinary web-use policy applies. If an agency **rehosts** the static files on a .gov platform, the files fall under that platform's existing ATO. That is usually a light assessment, because there is no code that runs on the server. | [E: CP-031; J] |
| Privacy Act of 1974 (SORN), E-Government Act §208 (PIA/PTA) | **No system of records:** nothing about an individual is collected or retrieved. A rehosting agency can document this with a PTA showing no PII. | [E: CP-030; J] |
| Paperwork Reduction Act | **No information collection:** the explorer asks the public nothing and receives nothing. | [E: CP-029, CP-033] |
| Federal web analytics and cookies (OMB M-10-22; DAP) | No cookies or analytics in the shipped site. A .gov mirror may add DAP through its own include; DAP sees page views only. Role selections and ratings are never sent to any analytics endpoint. | [E: CP-032; J] |
| OMB M-25-21 (high-impact AI), OPM AI-in-hiring memo (27 Aug 2026) | **Not an AI system and not used in hiring.** The explorer runs no model. EMST content was drafted with AI assistance; the explorer labels every agent draft, and EMST is "not a selection instrument". | [E: CP-022, CP-023; J] |
| Secure software (OMB M-26-05, which rescinds M-22-18 and M-23-16) | Agencies set risk-based policy. The CISA attestation is optional and an SBOM can be required on request. This packet supplies the SBOM, the SSDF mapping (§5) and checksums. | [E: CP-014] |
| State cloud verification (GovRAMP, TX-RAMP and similar) | Same reasoning as FedRAMP: no state information is collected or hosted. State CISOs reviewing third-party web content will find no third-party scripts, embeds or trackers (§4). | [J] |
| Section 508, WCAG 2.2 AA, ADA Title II | See `site/ACR.md`. | [E: CP-025, CP-026, CP-012] |

**Conditions that would change this statement.** Any of the following would bring the full regime into play: FedRAMP, ATO, SORN, PIA, GovRAMP and an M-25-21 review.

- accounts;
- server-side processing of input;
- uploads to a server;
- telemetry;
- an "Ask EMST" assistant;
- storing ratings anywhere other than the user's own file.

These are design-excluded (ADR-0012), and the output checks in `tools/check-output.mjs` fail the build if a network API appears in shipped code.

## 2. System description and boundary

```
  EMST repository (Tier 0)                    Build machine (CI or a maintainer laptop)
  data/v2, vocab/, validation/   ──────────▶  scripts/build_release.py  (release gate: Tribal hold,
  docs/build/WP-05, WP-08 (stop-gap views)     third-party licence, quarantine, personal-data checks)
                                                │  emst.bundle.jsonld + views/*.json
                                                ▼
                                              site/: Eleventy 3 → _site/ (static files)
                                              tools/check-output.mjs (fails the build on violations)
                                                │  _site/ + SITE_SHA256SUMS + SBOMs
                                                ▼
  Static host (GitHub Pages, or an agency .gov mirror)  ── HTTPS GET of static files ──▶  User's browser
                                                                                         │
                                         (nothing travels back)                          │ in memory only
                                                                                         ▼
                                                                    user-chosen file: *.emst.json, *.csv
```

**Data flow (complete list).**

| Flow | Direction | Content | Personal data |
|---|---|---|---|
| Page and asset requests | browser → host | `GET` of fixed paths: pages, `/assets/...` fonts, CSS, JS and images. The path carries only role, competency or register IDs that the user navigated to. | None from the explorer. The host's own access log records network addresses (§6). |
| Search | none | The whole index is embedded in the search page and loaded before the user types. No request depends on the query. | None |
| Gap-check ratings and notes | none (memory only) | Saved only when the user clicks "Save to file". The file holds `schema_version, release_id, role_variant_id, level, mode, ratings[]` (ADR-0012 I-1 §1). | Only what the user types in notes; the page warns against names. |
| Opening a saved file / team grid | local file → browser memory | `FileReader`, files of at most 2 MB, parsed as JSON. Notes and supervisor views are ignored in the team grid. Nothing is shown below 5 files. | Stays on the device |
| CSV and print exports | browser → user's disk | Priorities or counts, with the release ID and the use notice | As above |

**Pagefind was not used.** My Phase 2 spec named Pagefind (P-CP-11). Pagefind fetches index chunks and result fragments chosen by the query, so a static host's access log would see requests derived from what users search. The explorer therefore embeds a single index file instead. [J]

## 3. Software bill of materials

| File | Scope | Components |
|---|---|---|
| `security/sbom-runtime.cdx.json`, published at `/download/security/` | The production dependency tree: `@uswds/uswds` 3.14.0 and its declared dependencies (lit and its parts) | 7 |
| `security/sbom-build.cdx.json` | Full tree including build and test tools (Eleventy 3.1.6, axe-core 4.14.0, playwright-core 1.63.0, js-yaml 4.3.2). None of these is shipped. | 141 |
| `src/assets/vendor/uswds/VENDORED.json` | The USWDS files actually shipped: one stylesheet and 50 fonts and icons it references | — |
| `_site/download/security/SITE_SHA256SUMS` | SHA-256 of every published file | — |

- **Generator.** `npm sbom --sbom-format cyclonedx` (npm 10.9.4, CycloneDX 1.5). No extra tool is needed.
- **What ships versus what the SBOM lists.** The site ships no USWDS JavaScript and no lit code. The runtime SBOM lists them because npm declares them; `VENDORED.json` is the exact shipped list.
- **First-party code.** About 20 KB of first-party JavaScript, under 8 KB compressed: `emst.js`, `gap-check.js`, `team-grid.js` and `search.js`. No framework.
- **Vulnerability status at this build.** `npm audit` reports 0 vulnerabilities. js-yaml was raised from 4.1.1 to 4.3.2 to clear GHSA-h67p-54hq-rp68 and related merge-key DoS advisories. js-yaml parses only repository YAML at build time, so exposure was low. [E: npm audit output 2026-10-23]

## 4. Security controls in the shipped site

| Control | Implementation | Verified by |
|---|---|---|
| Content Security Policy | Set as a `<meta>` on every page: `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; media-src 'none'; object-src 'none'; frame-src 'none'; worker-src 'none'; manifest-src 'none'; base-uri 'none'; form-action 'none'`. With `connect-src 'none'`, scripts **cannot make any network connection**, even if an author mistake introduced one. | `check-output.mjs` B1; browser checks record no CSP violations |
| No third parties | All fonts, CSS, images and scripts are self-hosted. The vendoring step refuses a stylesheet that references external URLs. No embeds, iframes or external forms. | `check-output.mjs` A1–A6 |
| No storage, cookies or address-bar writes | Shipped JS is scanned for storage, cookie, history and location APIs. The browser test confirms that `document.cookie` is empty and storage is empty after a full gap-check session. | B5; `browser-checks.mjs` |
| XSS resistance | Templates are autoescaped (Nunjucks). JSON in `<script type="application/json">` escapes `<`. Client scripts build the DOM with `textContent` and never use `innerHTML`. No inline scripts or handlers; CSP blocks them anyway. | B2, B3, code review |
| File input | Only JSON files the user picks. Size capped at 2 MB. Schema and version checked. Unknown competencies are ignored and counted. Notes are truncated to 500 characters. | browser round-trip test |
| Referrer | `<meta name="referrer" content="no-referrer">`. Outbound links carry no query strings. | B1, A4 |
| Supply chain | Exact version pins and a committed `package-lock.json`. `npm ci --ignore-scripts`, so no lifecycle scripts run. A 14-day cooldown on new versions (Eleventy 3.1.6 chosen over 3.1.7, released 15 Oct 2026). | `package.json`; this packet |

**Response headers for a header-capable host.** GitHub Pages cannot set headers, so the CSP is delivered as a `<meta>` element [E: CP-080]. A host that can set headers should send the following (`tools/serve.mjs` sends the same set):

- `Content-Security-Policy`: as above, plus `frame-ancestors 'none'`;
- `Referrer-Policy: no-referrer`;
- `X-Content-Type-Options: nosniff`;
- `Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=(), browsing-topics=()`;
- `Cross-Origin-Opener-Policy: same-origin`;
- `Cross-Origin-Resource-Policy: same-origin`;
- HSTS.

## 5. SSDF mapping (NIST SP 800-218 v1.1)

| Practice | What the explorer does | Evidence |
|---|---|---|
| PO.1 Define security requirements | ADR-0012 (no personal data, four tiers, standing rules); ADR-0027 §4 (accessibility and security as release gates); CP compliance matrix CR-01…CR-39 | `docs/decisions/`, `docs/research/compliance-product/compliance_matrix.csv` |
| PO.3 Supporting toolchains | Pinned Node 22 toolchain; build and test tools are dev-only and never shipped | `package.json`, `package-lock.json`, SBOMs |
| PO.4 Criteria for security checks | Build fails on any `check-output.mjs` rule. `npm test` adds the browser checks: 0 axe violations, 0 external requests, 0 user-data requests. | `reports/check-output.json`, `reports/browser-checks.json` |
| PO.5 Secure environments | Builds read only repository files. `build_release.py` re-validates its inputs and refuses on errors. No secrets are needed. | `tools/prepare-release.mjs` |
| PS.1 Protect code | Git is the source of truth; the CA integrates changes (Phase 4 rules) | repository |
| PS.2 Integrity verification | `SITE_SHA256SUMS` for every published file; release `SHA256SUMS` for the data | `_site/download/security/`, `/download/release/` |
| PS.3 Archive and protect releases | Releases are versioned, with a DOI planned (ADR-0010). The explorer prints the release ID and build commit on every page. | footer of every page |
| PW.1 Design to meet requirements | Static, local-first design that removes the server attack surface (ADR-0012 Tier 1) | §1–§2 |
| PW.4 Reuse well-secured software | USWDS 3 from GSA; minimal dependency tree; 14-day cooldown; no runtime third-party code | §3 |
| PW.5 Secure coding | Autoescaping, no `innerHTML`, CSP, no inline scripts, input size limits | §4 |
| PW.6 Build configuration | Deterministic data build (`build_release.py` byte-identical builds); Eleventy configuration in the repository | `eleventy.config.js` |
| PW.7 / PW.8 Review and test | Seeded-violation test of the checker (16 cases); static output checks; browser tests of privacy behaviour; axe-core | `tools/test-checks.mjs`, `tools/check-output.mjs`, `tools/browser-checks.mjs` |
| PW.9 Secure defaults | No telemetry; nothing is saved without a user action; a warning before leaving the page with unsaved ratings | `gap-check.js` |
| RV.1 Identify vulnerabilities | `npm audit` at build; SBOMs published so adopters can scan | §3 |
| RV.2 / RV.3 Respond and analyse root cause | Private vulnerability reporting via the repository security policy (the Steward's route; not yet published) | open item |

## 6. Residual risks and open items

1. **Host logs.** Any web host can log network addresses and the paths requested. Paths reveal which role or competency pages someone viewed, never what they rated or searched. On GitHub Pages this sits with GitHub. A .gov mirror follows its agency's logging policy. The privacy page says so. [J]
2. **Shared or managed devices.** Saved gap-check files are personal development records on the user's disk. Agency device policy governs them. The team grid guidance asks leads to collect files only with consent and to delete them after use. [J]
3. **Notes may contain personal data that users type.** The UI warns against it, and the team grid never reads notes. [J]
4. **Not yet in place.** Each is owned by DE/WP-16 or the Steward.
   - Signed releases with provenance attestations (for example GitHub artifact attestations or Sigstore).
   - An OpenSSF Scorecard run of at least 7, which needs the public repository [E: CP-034].
   - SHA-pinned GitHub Actions for a site build workflow. No workflow for the site exists yet.
   - A published SECURITY.md disclosure route.
   - The voluntary CISA attestation form.
5. **Stop-gap inputs** (CR-CP-001). Two computed views come from scripts outside the release build:
   - federal applicability (DE's registered rule `scripts/rules/venue_applicability.py`, run by `site/tools/venue_view.py` over the release bundle; the WP-05 prototype is only a fallback);
   - the HR views (WP-08 generators).

   The explorer re-checks every ID against the release bundle, so held or excluded records cannot appear. The data still bypass `build_release.py`'s own gate until those views are emitted by the release. The CA accepted CR-CP-001 A1–A3, and DE ports these views into the release; the explorer switches automatically when `views/venue_applicability.json` and `views/federal-series/` appear.
7. **Unverified external claims.** The WP-15 sign-off clears the explorer for internal drafts and the NGO-pilot preview only. Records tied to unverified register rows render as "Unverified — not for citation". `check-output.mjs` section E fails the build on any `do_not_say` wrong form.
6. **Preview profile.** The current build includes draft records, by design for the pilot preview, and every page says so. A distribution build should use a tagged release (`EMST_RELEASE_DIR`).
