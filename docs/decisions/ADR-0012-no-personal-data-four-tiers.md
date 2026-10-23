# ADR-0012: "EMST holds no personal data" — a binding architectural invariant, and the four-tier delivery architecture

- **Decision point:** DP-11 (CP's invariant and four-tier architecture)
- **Status:** accepted (binding on all roles and Phase 4 work packages, including IA's skills-intelligence pipeline, LM's signals, CM's validation data and IO's panels)
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** CP, IA, CM, IO, FH, SL, TN, DE, LM, FS, AS
- **Related:** ADR-0007 (Tribal data), ADR-0023 (mobility validation), ADR-0024 (panels), ADR-0027 (product)

## Context

The heavy compliance regimes turn on two triggers: a service that collects or maintains Federal information on behalf of an agency (FedRAMP, FISMA ATO), and records about individuals retrieved by an identifier (Privacy Act SORN, PIA, state public-employee data law) [E: CP-015, CP-016; J: CP-040, CP-077]. FedRAMP's Consolidated Rules for 2026 replace "authorization" with "certification" (Classes A–D), available from 4 July 2026 as optional early adoption and mandatory from 1 January 2027 [E: V2-10]. Competency ratings retrieved by employee name are likely a Privacy Act system of records (FH issue). In a RIF and accountability-reform environment, skills data can be turned against workers (CM issue).

## Decision

### Invariant (I-1): the EMST steward holds no personal data

No EMST repository, build, release, website, API or steward-operated service receives, stores or processes person-level data about workers, applicants, raters, panelists or pilot participants. Specifically:

1. **No person entity in the schema.** Person-level structures exist only as versioned client-side file formats (`{release_id, role_variant_id, level, ratings[], schema_version}`) or as Tier 2 kit schemas instantiated in adopters' own authorized systems (CP §11 Q2).
2. **Signals describe work, not workers.** Postings, PDs and plans are **de-identified at ingestion**; only derived signals and source hashes are stored (P-CP-19). Small-cell headcounts (series × grade × age at small units) are suppressed below a minimum cell of 5 (LM issue).
3. **Raters and panelists are pseudonymous.** Gold-set and assessment records carry pseudonymous rater IDs; the identity map is held by the research partner outside the repo. Delphi and SME responses enter the repo **only as aggregates** (answers DE open Q7).
4. **Observed career transitions** (CM's validation table) enter EMST only as aggregate edges (from-variant, to-variant, year, region bucket) with n ≥ 5. Consented person-level research records, if collected, are held by an IRB-governed research partner, never by the steward (answers CM open Q6).
5. **Tribal data** follows ADR-0007's vetoes in addition: no person-level Tribal data, no citizenship or preference status, ever.

### Invariant (I-2): development use only

EMST never ranks, scores, screens or selects people. Exports carry "not a selection instrument / not a classification basis / not for RIF, adverse action or performance ratings" (P-CP-06, P-FH-10, P-CM-10). AI-assisted builders produce drafts that a human adopts, and exports record the AI assistance and release used — the pattern OPM's 27 Aug 2026 memo treats as generally not high-impact when the responsible official independently reviews, revises and adopts the draft [E: V1-13].

### Four tiers (P-CP-01)

| Tier | What | Personal data | Owner |
|---|---|---|---|
| **0 Open core** | Repo as source of truth; signed, versioned releases with DOI, SBOM, provenance attestation and delta file | never | DE, IA |
| **1 Public explorer** | Static, local-first, pre-rendered site; no server, accounts, cookies, query logs or third-party requests; gap check runs in the browser; save/load as a file; USWDS 3; WCAG 2.2 AA; rehostable on .gov | never leaves the device | CP |
| **2 Run-it-yourself kits** | Skills-library import files for HCM/LMS; team gap workbook (min cell 5); PD drafting kit; later a skills-inference pipeline with person confirmation — each with PTA/PIA starter, SORN data-element inventory, AI system card, impact-assessment inputs, ACR, SBOM | only inside the adopter's authorized system | IA (+CP docs) |
| **3 Hosted personnel-data service** | **Not on the roadmap.** If ever needed, partner with a certified platform | — | — |

Standing rules: no user input in URLs; no runtime third-party requests (the OpenLMP dashboard's Google Fonts call is the pattern to avoid); every judgment shown carries tier, rater type, date and method (P-CP-02). Skills inference from documents about an individual is deferred; if built, Tier 2 only, with person confirmation, visible evidence spans, no default storage and published error rates (P-CP-20). An "Ask EMST" assistant is out of the MVP because it would collect and log queries (CP §3).

## Rationale and evidence

- With no personal data and no Federal information collected, the public explorer is an information provider: no FedRAMP, no new ATO, PTA only when rehosted on .gov [E: CP-015, CP-016; J: CP §3]. Any hosted personnel-data design triggers FedRAMP, agency ATOs, SORNs, PIAs, GovRAMP for states and M-25-21 high-impact review [E: CP-016, CP-023].
- Local-first delivers most of the user value at almost none of the compliance cost, and removes a permanent barrier for federal and state staff who would otherwise need an agency determination before entering their own data (CP §4).
- State public-records law can expose stored individual ratings (CP-077 [J]); default aggregates protect workers and adopters.

## Consequences

- IA's pipeline design (`pipeline_design.md`) is amended: PII stripping is stage 2 and mandatory; Tribal-employer postings are quarantined (ADR-0007).
- CM's pathway validation depends on partner-computed aggregates and an OPM EHRI research agreement (P-CM-12), which is slower to build than telemetry.
- IO's assessments and BARS are delivered as Tier 2 kit content; validation data flow back only as aggregates.

## Dissent and trade-offs

- **CM:** validation needs real career histories; minimum-grain, consented, separately stored records are the compromise, held by a research partner rather than none at all (CM disagreement 7).
- **CP vs CM/AS (anticipated):** no telemetry and file sharing instead of shared workspaces slow causal evidence and add friction (CP disagreements 2, 4). Accepted.
- **IA vs CP:** inference vs self-rating — inference deferred; self- and supervisor rating against anchored indicators is slower but transparent (CP disagreement 3).
- **Trade-off named:** analytic power and convenience traded for a tool federal and state staff can use without procurement review.
