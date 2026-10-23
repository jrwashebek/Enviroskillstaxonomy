# EMST Ecosystem Atlas

- **Work package:** WP-13 (P-AS-13, P-AS-16; ADR-0009 §10) · **Author:** A10b (AS) · **Date:** 2026-10-23
- **Files:** `ecosystem_atlas.csv` (the dataset, CC0 1.0) · `ecosystem_atlas_summary.csv` (counts, **generated**, never typed) · `scripts/build_ecosystem_atlas.py` (Apache-2.0; reproducible build)
- **Rebuild:** from the repository root, `python3 -I docs/adoption/scripts/build_ecosystem_atlas.py`. The build reads only `docs/research/_merged/ecosystem.csv`, `docs/research/_merged/sources.csv` and `docs/research/_verification/*`, and writes only the two CSVs above.
- **Status:** first maintained edition. Every row is dated and owned; rows are re-checked on their `review_by` date and before any claim drawn from them is published (WP-15).

> **The atlas records connections EMST could make, not commitments anyone has made.** `how_emst_connects` and `integration_detail` are proposals written by the Phase 2 roles. Every row carries `commitment_status = none recorded`; no organization in the atlas may be described as a partner, funder, adopter, steward or co-publisher unless the commitment register holds a signed entry (charter Art. 12; `COMMITMENT_REGISTER.md`).

## 1. Why EMST keeps an atlas

The project lead's goal is for EMST to become the asset that **brings together** the indices, research programmes, papers, working groups, organizations, funds, standards and tools that show how AI and other forces are changing environmental work (TEAM_BRIEF §5.5). The atlas is the map of those entities and of how each one connects to EMST records. Verification found **no active environment-sector-wide workforce or AI coalition** [E: V3-11]: the convening role is open, and the atlas is the working list for it.

## 2. How it was built

1. **Input:** the merged ecosystem file from all Phase 2 roles (sizes in the generated summary).
2. **Deduplication.** Rows describing the same entity (for example O*NET and OpenLMP, each recorded by several roles) are merged by an explicit, reviewable cluster map in the build script. Rows that bundle several entities ("Licensure boards: NCEES, ASBOG…") stay as their own rows. A product of an organization is merged into the organization only where the roles were clearly describing the same thing (e.g. SAF and SAF accreditation; NAAEE and its certification programme). Every merged row keeps `contributing_entity_ids`, `contributing_roles` and each role's own integration text, prefixed `[ROLE]`.
3. **Best-verified status and URL.** For each entity the build collects every check that applies — the Phase 2b queue result for each contributing row, the key facts that concern the entity (V1–V4), and source-item checks where an entity was verified through a source (e.g. UGESP through IO-020/IO-022) — and carries the best one (`verified > corrected > superseded > source-read > unreachable > unverified > not-found`). The verification URL and source date of that check are kept. Key-fact corrections that concern other entities are not attributed to an entity (e.g. V3-07's ISSP and IEMA corrections do not mark SAF as corrected).
4. **Corrections applied.** Names, URLs and status text are corrected from the verification findings and ADR-0027 §3: ISEP (formerly IEMA); ISSP credentials offered by GBCI; Water Professionals International (formerly ABC), with operator certification issued by states; Lightcast Skills Taxonomy (formerly Open Skills); OPM's Phase One series list shown as **proposed**; USWFS–USFS aligned federal fire qualifications (NWCG not a party); Workforce Pell programmes approved by governors working with state boards; Colorado SB 26-189 replacing SB 24-205; the five-ECQ framework; UGESP status; BLS 2025–35 projections; the "Coalition of Natural Resource Societies" marked **not found**. The domain formerly used by the U.S. Indigenous Data Sovereignty Network is removed and never linked. `corrections_applied` lists the checks that produced corrections.
5. **Tribal hold.** Rows recorded by TN, or whose subject is a Tribal government, inter-Tribal organization, Tribal programme or Indigenous data governance, carry `tribal_related = true`, `release_status = held-pending-tribal-review`, `atlas_owner_role = TN`, and connection modes reduced to `watch`; the Phase 2 modes are kept in `connection_note` as "suspended under the Tribal gate". No outreach follows from any atlas row (`docs/governance/tribal_gate_procedures.md`). Only a TAC can release these rows; its consent authority is decided (Q1 accepted), but no TAC exists and the outreach gate stays closed until compensation is funded. <!-- DECIDED Q1 (2026-10-23, PROJECT_LEAD_DECISIONS.md): TAC binding consent authority accepted; the content hold continues until a TAC exists --> <!-- PENDING Q9 -->
6. **Owners and review dates.** Each row names an `atlas_owner_role` (the role whose lane the entity sits in) and a `review_by` date: three months for policies, indices, datasets, platforms, tools, funds and every weakly verified row; six months (before the April MINOR) for the rest.

## 3. Columns

| Column | Meaning |
|---|---|
| `atlas_id` | local key `ATL-nnnn`, assigned by sort order in each build — **not an EMST ID** and not stable across rebuilds; cite entities by name and `contributing_entity_ids` |
| `name`, `entity_type`, `entity_type_alternates` | corrected name; type from the TEAM_BRIEF vocabulary; other types contributing roles used |
| `owner_or_host`, `sector_focus`, `what_it_illuminates` | from the representative row, corrected where verification required |
| `latest_release_or_status` | dated status; replaced by the verified or corrected statement where one exists |
| `how_emst_connects` | union of connection modes across contributing rows (§4); `watch` only for Tribal-related rows |
| `join_keys` | the identifier systems through which EMST records join this entity's data (§5) |
| `integration_detail` | each contributing role's proposed integration, prefixed `[ROLE]` |
| `url` | best entity URL (corrected where verification required; blank where the only URL was wrong or unsafe) |
| `verification_status`, `verified_on`, `verification_source_date`, `verification_url`, `verification_refs`, `corrections_applied`, `verification_note` | the best check, when it was run, the date of the evidence, where, which checks apply, which produced corrections, and the findings |
| `evidence_label` | E where a check or a read source supports the row; otherwise J or S |
| `source_ids` | union of contributing roles' source IDs (resolve in `docs/research/_merged/sources.csv`) |
| `contributing_roles`, `contributing_entity_ids`, `n_contributing_rows` | provenance |
| `tribal_related`, `release_status`, `connection_note` | governed-content flags (§6) |
| `commitment_status` | always "none recorded" until the commitment register says otherwise |
| `atlas_owner_role`, `review_by` | maintenance |

**Verification status values.** `verified` — checked against a current primary or authoritative source in the Phase 2b pass; `corrected` — checked and found partly wrong, corrections applied; `superseded` — a newer version or name replaces the one recorded, updated; `source-read` — not re-checked in Phase 2b, but the contributing role cited a source it read (with its access date in `verified_on`); `unreachable` — the check could not reach a source; `unverified` — queued for verification but not reached, or recorded from prior knowledge; `not-found` — the check found no evidence the entity exists or is active as described.

**Release status values.** `usable-with-citation` — may be cited in EMST materials with the verification reference, subject to WP-15 for date-sensitive claims; `verify-before-external-use` — internal planning only until re-checked; `do-not-cite-as-active` — not found; `held-pending-tribal-review` — held under ADR-0007 §D.

## 4. Connection modes

| Mode | What it means | Condition before EMST does it |
|---|---|---|
| `ingest` | EMST takes data from the entity into L5 (signals, external-index assessments) or L6 (registers) | licence recorded in the third-party register (`docs/governance/LICENSING.md` §5); IDs only in CC0 files; values aggregated, never single-match; personal data stripped at ingestion; Tribal-employer material quarantined (ADR-0007 V4, ADR-0012) |
| `crosswalk` | EMST maintains an SSSOM mapping set to the entity's identifiers (X1–X12) | SSSOM 1.0; pinned upstream version; no alignment claim until a reviewed set exists (ADR-0022 §4) |
| `benchmark` | EMST compares its own values or methods against the entity's | comparison reported with dispersion; no change indicator may rest on a single vendor's data (ADR-0008 §4) |
| `partner` | a working relationship (advisory seats, co-production, recruitment channels) | a signed commitment-register entry before any public description as a partner |
| `funder` | a source of money | a signed grant or agreement in the register; editorial-independence clause (charter Art. 9.3) |
| `adopter` | an organization that puts EMST IDs into its own artifacts | a register entry naming the artifact; counted for M-08, M-18, M-25 only when signed |
| `validator` | supplies evidence that confirms or refutes EMST content (SME panels, job analyses, gold sets, credential evidence) | IO protocols and composition rules (ADR-0024); aggregates only |
| `distribution` | a channel through which EMST reaches users (registries, platforms, networks) | conformance check for "EMST-mapped" listings (charter Art. 11.3) |
| `watch` | tracked for change; no exchange of data or commitments | `review_by` date |

## 5. How EMST joins indices: the O*NET task ID as the hinge

Most of the evidence about how AI is changing work is published **by O*NET task or by occupation**, not by environmental competency. EMST therefore joins external indices through its **task layer**, using O*NET task IDs as the hinge key (P-AS-13; ADR-0008; ADR-0022; SPEC §11.4, §15).

```
EMST Task (L2, emst:…/TSK-…)
   │  X2 mapping set (SSSOM 1.0): emst task → O*NET 31.0 task ID / DWA
   │     – two independent coders, κ ≥ 0.6 on match type; weakest match type carried
   │     – candidates restricted to the role family's O*NET-SOC pool; ~30% NoTermFound expected
   │     – a second explicit mapping to O*NET 27.x tasks, where Eloundou labels sit
   ▼
O*NET task ID ──► external index values keyed by task, per pinned release
   │               · Anthropic Economic Index task usage and collaboration shares (six releases through 2026-06-26)
   │               · Eloundou et al. E-labels and T-rubric (O*NET 27.x tasks)
   │               · Microsoft "Working with AI" applicability (task → DWA → IWA)
   │               · AEI labour-market-impacts and robot task-capability datasets
   ▼
ExposureAssessment (L5), raterType = external-index, with source release, match path and weakest match type
   │  aggregation rules: never a single match; top-k weighted by match type; dispersion shown (XR-06)
   ▼
computed views (build only): task and role external context in View 1 "How is this role changing?",
labelled as external context, beside "assessment pending" until v2 multi-rater assessments exist (ADR-0027 §2)
```

**Occupation-grain sources** join one level up, through X3 role variant → **O*NET-SOC 2019 / SOC 2018**: BLS Employment Projections 2025–35 and their AI exposure categories, OEWS, AIOE (context only, SOC 2010 codes handled), and occupation-level AEI observed exposure. **ISCO-08** sources (ILO WP 140) join via ESCO (X7, v1.2.1). Federal headcount sources (OPM Federal Workforce Data) join via **OPM series** (X4, with `proposed-realignment` statuses); state sources via **state class records** (X5); education sources via **CIP 2020** (X6); credentials via **CTDL/CTIDs** (X10, Credential Registry). The `join_keys` column records which of these keys each atlas entity's data uses.

**Rules that keep the join honest.**

1. **Match quality travels with the value.** Every external value carries the crosswalk path and its weakest match type; partial matches can raise only a `watch`, never move a change indicator (ADR-0028 §2).
2. **Two families, not one index.** A change indicator moves only when two independent signal families agree; two indices built on the same data family count as one (ADR-0028 §2).
3. **Say what the index measures.** The AEI's API automation-pattern share describes usage patterns in API traffic, **not job automation** (ADR-0027 §3); capability exposure is not deployment, and deployment is not staffing outcome (ADR-0008).
4. **IDs only in CC0 files.** O*NET task text (CC BY 4.0), AEI data (CC BY) and licensed posting data (Lightcast, by contract) stay out of CC0 files; aggregates are stored with attribution (ADR-0013 §5).
5. **Re-pin on every upstream release.** O*NET is pinned at 31.0 (Aug 2026); on each O*NET, ESCO or SOC release a CI diff sorts mappings into carry / needs-review / deprecated / new-candidate (ADR-0022 §1). The SOC 2028 re-map is planned once the final structure is published (planned 2027) [E: V3-02].
6. **No Tribal joins.** Tribal-employer postings and documents are never joined or ingested by default; the `tribal_programs` quarantine applies to any index row that would describe Tribal programmes (ADR-0007 V4).

This design lets EMST ingest **any** future index published at task or occupation grain without changing its schema — the sustainability model's answer to the risk that O*NET or a vendor publishes its own environmental AI index: EMST's distinct value is mobility across sector actors, crafts and role variants, not one more index.

## 6. Governed content in the atlas

- **Tribal-related rows** are held (§2.5). They include inter-Tribal organizations, Tribal colleges, Tribal programmes, federal Tribal-policy instruments recorded by TN, and Indigenous data-governance standards and tools. Listing them is analysis of public information for internal planning; it implies no engagement, partnership or permission.
- **No personal data.** Rows describe organizations, programmes and products; no individual is named as a contact.
- **Unsafe links** are removed (the former USIDSN domain).

## 7. Maintenance

| Task | Owner | When |
|---|---|---|
| Re-check rows on or before `review_by`; update status, URL, `verified_on` | `atlas_owner_role` | quarterly / semi-annually |
| Automated link check of `url` and `verification_url` in CI | DE | each build (P-AS-16) |
| Re-verify every `unverified`, `unreachable` and `source-read` row before it is cited externally | WP-15 claims register (A9 LM; AS co-signs) | before rc.1 and before 2.0.0 |
| Add new entities through the ordinary change process (type C for crosswalk-relevant entries, otherwise E) | any contributor | continuous |
| Review the cluster map when two rows are found to describe the same entity | AS successor role (Community and Partnerships Manager) | each rebuild |
| Release Tribal-related rows | TAC only | only on TAC approval |

## 8. Known limits

- A large share of rows rest on prior knowledge or on a single role's reading and are marked `unverified` or `source-read`; the generated summary gives the current mix. They are planning aids, not citations.
- Deduplication is a judgment; the cluster map is in the script so anyone can challenge it.
- `join_keys` is derived from the roles' own integration text plus SPEC §11.4; an entity marked `none` may still be joinable once its data are examined.
- Status text is shortened from findings; `verification_note` and the cited checks are the record.
