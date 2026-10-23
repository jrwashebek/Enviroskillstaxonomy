# ADR-0009: Governance, phased federation, change process and release cadence

- **Decision point:** DP-9 (part a: governance, stewardship, modules, cadence). Part b (IDs, serialization, versioning) is ADR-0010.
- **Status:** accepted for the governance model, federation phasing and cadence; **needs-project-lead** for the host (EPIC incubation through 2027, open call for a university host) and for constituting bodies with external members
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** AS, DE, IA, CM, TN, IO, FS, CP, DB, SL, LC
- **Related:** ADR-0007 (Tribal Council), ADR-0010, ADR-0013 (licensing), ADR-0015 (lifecycle), ADR-0018 (modules), ADR-0024 (use tiers), ADR-0028 (signals); `docs/research/adoption-stewardship/governance_charter_draft.md`

## Context

v1 governance depended on one person's discipline enforced through chat prompts; the task sequence deferred Tasks 15–22 to a v6 document slated for removal; rule IDs collided; public materials claimed validation that had not happened [E: audit §14]. The Australian Skills Classification is "no longer actively maintained" with data to December 2023 [E: CA-036] — the year-five failure mode AS must design against. No subsector body has yet agreed to steward an EMST module, and societies "will not take on unfunded authoring" [E: AS-042, AS-056; AS §10 AS-1].

## Decision

1. **Adopt AS's draft charter (`governance_charter_draft.md`, Articles 1–11) as the basis of EMST governance** (P-AS-05), with these bodies: Steward (host; holds marks in trust; no editorial veto); Editorial Board (7–9; ≤ 1 member per organization; ≥ 3 sector actors; includes a voting Tribal Council liaison); Technical Steering Committee (schema, IDs, release engineering, crosswalk method); Advisory Council (17–21 with sector-actor seats; funders non-voting); **Tribal Council with consent authority over Tribal-related content** (pending real consultation; ADR-0007); Module Stewards; Validation Panels (IO protocols); Sentinel Network (paid, stratified).
2. **Workforce Voice Panel** (CM P-CM-09) is added as a standing body with a **binding usefulness veto at gate G1**, which the CA (Phases 3–4) or Editorial Board (thereafter) may override only by a written answer, a second panel vote and escalation to the Advisory Council executive group (CM disagreement 5).
3. **Phased federation (P-AS-06):**
   - **v2.0–v2.1 (2027–2028): modules are editorial sections** — namespaced, on the shared schema, **authored centrally and paid for by the core**, each with a named module advisory partner.
   - **v2.2+:** a section becomes a **stewarded module** only after its partner signs a Module Stewardship Agreement (core schema, namespaced IDs, core vocabularies, ≥ 1 review cycle a year on core cadence, core evidence standard, SME pool, conformance checks, no separate licence) and completes **two review cycles on time**.
   - **Orphan clause:** a module returns to the core if its steward misses two cycles or withdraws.
   - The architecture is designed for Option C from day one (namespaces, boundaries, CODEOWNERS); staffing is for central authoring through 2028 (~1 extra editorial FTE).
4. **Change process (charter Art. 5):** pull-request–based change requests typed E (errata), C (crosswalk), S (substantive), D (deprecate), X (structural), T (Tribal-related, routed to the Tribal Council first). S and X require **two independent sources including at least one demand signal** (posting, PD, plan requirement, staffing plan) or SME panel data. Stages with service levels: triage ≤ 30 days; candidate comment 30 days (minor) / 60 days (major or X); adjudication ≤ 30 days with NICE-style dispositions (Noted / Accepted / Accepted with modification / Deferred / Rejected). Bots open PRs; humans merge (P-DE-09).
5. **Release cadence (charter Art. 6, adopted):**

   | Release | Contents | Cadence | Notice |
   |---|---|---|---|
   | PATCH | errata; crosswalk re-pins (O*NET, ESCO, OPM register); fast-layer snapshots | as needed; crosswalks ≥ quarterly | release notes |
   | MINOR | additive content, new role variants, deprecations with successors, lifecycle promotions | **once a year in April** (after the sentinel cycle, before federal budget formulation) | candidate ≥ 60 days before |
   | MAJOR | breaking change (withdrawal without successor; change to the meaning of an L0 term or the level scale; schema removal) | **≤ once every 3 years**, announced ≥ 12 months ahead | migration guide + crosswalk |

   Prior MAJOR supported ≥ 24 months; assessment users may pin a version until their next job-analysis refresh. Every release ships a "does this affect me?" notice, machine-readable delta, DOI, signed artifacts, SBOM and an accessibility conformance report.
6. **Decision records:** ADRs in `docs/decisions/`, published within 14 days; the CA resolves disputes through Phase 4 (charter Art. 4.5), after which the Editorial Board decides with appeal to the Advisory Council executive group.
7. **Anti-ASC succession (Art. 11):** five-year Host Agreement with ≥ 12 months' notice; ≥ 2 pre-qualified successors incl. a fiscal sponsor or open-standards foundation; mirrors and Zenodo DOIs; reproducible build; credentials held by two people at two organizations; **published maintenance floor (~3 FTE, ~$0.62M/yr)** and a degradation ladder with 6 months' notice; five-year public review.
8. **Host (recommendation to the project lead):** EPIC incubates through December 2027 and remains founding partner; an open call (Q2 2027) selects a **university-based EMST Stewardship Center** to operate the program from January 2028; an independent EMST Consortium governs (P-AS-08). Until a host exists, the project lead (or EPIC, if confirmed) signs pilot MOUs and data agreements.
9. **Commitment register** in the repo (P-AS-15): every adopter, partner and funder commitment with rung, artifact, date, contact and a **year-five owner** field; it feeds CM metrics M-10 and M-29.
10. **Ecosystem Atlas** (`_merged/ecosystem.csv`, 626 rows) becomes a maintained dataset with owners and review dates, re-verified in Phase 4 (P-AS-13, P-AS-16). V3 found **no active environment-sector-wide workforce/AI coalition** [E: V3-11] — EMST's convening role is open; the four-society joint-statement group (AFS, SAF, SRM, TWS) is a partner prospect, not an existing coalition.

## Rationale and evidence

- NICE caps majors at once every three years with a year's notice and minors at once a year; federal HR artifacts (PDs, classification standards, validated assessments) are expensive to change and can trigger bargaining [E: AS-026, AS-007, AS-009]. AS's hypothesis — adopters accept an annual content cadence only with change notices and a supported prior version — is tested in the design-partner track (ADR-0014).
- Federation works where the extension steward has its own mandate and staff (NICE → DoD DCWF) [E: AS-027; CA-033]; SFIA 10 attendees asked for "stable core plus plug-ins" but SFIA has not adopted it [E: CA-034]. Hence phased, evidence-gated federation.
- The year-five floor and succession clauses answer the ASC precedent and v1's dependence on accounts it did not control (an EPIC Airtable subscription; a suspended GitBook account) [E: AS sustainability model; CP §12].

## Consequences

- Wave-1 module content (ADR-0018) is commissioned centrally in Phase 4 with steward co-authorship where available; credential-body exam blueprints need data agreements, not scraping (DB issue 2).
- The CA's dispute-resolution role ends at the close of Phase 4; ADR-0007's Tribal carve-out applies from the start.

## Dissent and trade-offs

- **AS vs IO:** recruiting Delphi panels through adopters builds commitment but risks bias; IO sets composition rules (≥ 50% independent panelists; sector-actor caps ≤ 30%) (AS disagreement 4; P-IO-09).
- **University host vs society consortium:** neutrality and CESU access versus credential leverage; societies keep strong governance seats either way (AS disagreement 3).
- **Fee-for-service vs neutrality:** services fund the core; the Art. 7.5 firewall manages influence (AS disagreement 7).
- **Trade-off named:** governance friction (veto, consent, panels) in exchange for legitimacy with the people the tool serves and for durability beyond any one organization.
