# ADR-0013: Licensing — CC0 for everything adopters embed, CC BY 4.0 for narrative publications, Apache-2.0 for code, a Tribal carve-out

- **Decision point:** DP-12 (licensing)
- **Status:** accepted — **conditional on the project lead's written CC0 dedication of the v1-derived content** (the v1 text is the lead's own work; DE §12 caveat 3). See `questions_for_project_lead.md` Q2.
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** DE, CP, AS, IA, TN, LC, FH, PS, LM
- **Related:** ADR-0007 (Tribal carve-out), ADR-0009 (marks and conformance), ADR-0010 (releases, DOI)

## Context — the conflict

- **DE (P-DE-11) and CP (P-CP-08):** CC0-1.0 for schema, vocabularies, documentation and EMST-authored data; Apache-2.0 for code; upstream text out of CC0 files; matches OpenLMP and the CEQ permitting data standard.
- **AS (P-AS-07; charter Art. 8):** **CC BY 4.0 for content** (competency, task, indicator and role-profile text and documentation), **CC0 for schema, IDs, vocabularies and crosswalk tables**, Apache-2.0 for code, Tribal carve-out. Reasons: attribution with version supports provenance and legal defensibility ("which version did this PD use?"), adoption measurement and funder visibility.
- **IA (P-IA-06):** pick one, with AS/CP. **TN (P-TN-11):** CC0 is right for project-authored content and wrong for Tribal-contributed content.
- **v1** asserted both licences at once (CC0 in the GitHub dropdown, CC BY 4.0 in the README) [E: CP-005, AS-048]. Two licences on one dataset "invite counsel to say no" (CP §9).

## Decision

1. **CC0 1.0** for all EMST-authored **data and standard text**: L0 vocabularies, schema and JSON-LD context, identifiers and the ID registry, competency/knowledge/task/indicator/role/variant/enactment text, crosswalk mapping sets, computed views, release bundles and exports, and `docs/standard/SPEC.md`.
2. **CC BY 4.0** for EMST **narrative publications**: the flagship report, briefing decks, role-change briefs, research papers, explorer prose and other documentation that is authored as a publication rather than embedded as data.
3. **Apache-2.0** for code. Contributions under the Developer Certificate of Origin; inbound = outbound; no copyright assignment; federal employees' contributions are U.S. government works.
4. **Provenance and version citation are secured by marks and release engineering, not by licence:** every export and page is stamped with release ID and DOI (P-CP-17); CITATION.cff and a non-binding citation request; the "EMST" name and marks are held in trust by the Steward; "EMST-conformant" and "EMST-mapped" claims require a conformance check; modified versions may not be called EMST (charter Art. 9).
5. **Third-party material keeps its own terms and stays out of CC0 files:** crosswalks store external **IDs only** (O*NET-SOC/task IDs, ESCO URIs, CIP, SOC, OPM series); upstream text (O*NET CC BY 4.0; ESCO; AEI data CC BY [E: V4-01]) lives, if at all, in separately licensed and attributed files under `external/`; licensed posting data (e.g. Lightcast) is used only as permitted aggregates; accreditor and credential-body text is paraphrased and cited, never copied (SAF handbook precedent). A third-party licence register ships with each release.
6. **Tribal carve-out:** Tribal-contributed content lives in its own namespace with the contributor's chosen licence, labels (e.g. Local Contexts Notices if the Tribal Council chooses) and withdrawal right, and is **excluded from the bulk CC0 release unless the contributor opts in** (P-TN-11; ADR-0007).
7. **Resolve v1's contradiction** in the first commit of the v2 repository: one `LICENSE` (Apache-2.0), one `LICENSE-DATA` (CC0 1.0), one `LICENSE-PUBLICATIONS` (CC BY 4.0) with a path map, and the lead's dedication statement.

## Rationale

- **The adoption route is embedding.** AS's own analysis says adoption comes "through artifacts, not endorsements": competency models and PDs for OPM's consolidated series, Chance-to-Compete job analyses, state class specifications, Workforce Pell program approvals, vendor skills libraries (AS §0.1). Under CC BY, attribution obligations travel into every derived PD, class spec and vendor database (AS concedes "attribution stacking in large derived databases" and slower legal review). CC0 removes that friction exactly where adoption is decided.
- **CC BY does not deliver version citation.** It requires attribution, which is routinely satisfied by naming the source; it does not compel a release ID. The release stamp, DOI and conformance mark do that directly and are enforceable through the mark, not the copyright.
- **One licence per record.** AS's layered split would put a CC0 ID and a CC BY label in the same record and export row — recreating the v1 two-licence confusion inside every row.
- **Public-domain inputs.** Federal contributions are U.S. government works; OPM text is public domain; CEQ's data standard and OpenLMP are CC0 [E: AS-046, AS-047; J: CP-055]. Mixed CC BY + public-domain provenance complicates counsel review.
- **AS's legitimate concerns are kept** where attribution matters for visibility and funding — the narrative publications — and the trademark-in-trust convention protects against altered copies circulating as "EMST".

## Consequences

- DE adds licence fields per file family and a CI check that no CC0 file contains third-party text (upstream text detector against O*NET and ESCO label lists).
- AS's funder narrative uses publication citations, DOIs and the commitment register (P-AS-15) as visibility evidence.

## Dissent and trade-offs

- **AS** dissents for content: CC BY would make provenance and fundability stronger. **Trade-off named:** less adoption friction and one licence per record (chosen) versus enforceable attribution of content. The CA judges that the mark-and-DOI convention captures most of AS's benefit at little of the cost.
- **TN's** carve-out adds schema complexity (namespace and licence separation from day one), accepted.
