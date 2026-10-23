# EMST Commitment Register — schema and rules

- **Work package:** WP-13 · **Author:** A10b (AS) · **Date:** 2026-10-23 · **Licence:** CC0 1.0 (schema)
- **Register file:** `data/v2/registers/commitments.csv` (header only; **no commitments exist yet**)
- **Builds:** ADR-0009 §9 (P-AS-15), governance charter Art. 12, ADR-0012 (no personal data), ADR-0007 (Tribal), CM metrics M-08, M-10, M-18, M-25, M-29 (`docs/adoption/gate_metrics_G1_G2.csv`), `PHASE4_BUILD_PLAN.md` §6 ("the commitment register is the only source of committed status").

## 1. Why it exists

Agencies will not build PDs and assessments on content nobody maintains, and funders will ask who carries each piece of work in year five. The register records every commitment made to or by EMST, with the artifact that proves it and a **year-five owner**. It is the **only** source from which any EMST document may describe an organization as committed, a partner, a pilot member, an adopter, a steward, a funder or a co-publisher (charter Art. 12.2).

## 2. What goes in, and what does not

| In the register | Not in the register |
|---|---|
| Written commitments: letters of intent, MOUs, DUAs, Module Stewardship Agreements, grant awards, Host Agreements, CESU task agreements, contracts, written confirmations of a named use | **Prospects, candidates and conversations** — they live in the Ecosystem Atlas as *candidate*/*prospect* and in the Steward's own pipeline outside the repository |
| Written offers from EMST awaiting signature (`status = offered`) — these do **not** make an organization committed | Organizations that declined (not recorded publicly) |
| Organization-level facts and role titles | **Personal names, personal emails or phone numbers** of signatories or contacts (role titles only), and any person-level data (ADR-0012 I-1) |
| A Tribal government's or Tribal organization's commitment, only with a TAC approval ID | Tribes as prospects, invitees or "asked"; Tribes counted toward any target (charter Art. 12.4) |

## 3. Fields

| # | Field | Type | Required | Values / rule |
|---|---|---|---|---|
| 1 | `commitment_id` | string | always | `CR-<yyyy>-<nnn>`, assigned in order, never reused (a local register key, not an EMST ID) |
| 2 | `organization_name` | string | always | legal or official name as the organization uses it |
| 3 | `sector_actor` | enum | always | `federal | state | local | tribal | ngo | private | academic` (`vocab/sector_actors.yaml`) |
| 4 | `organization_subtype` | string | should | subtype from `vocab/sector_actors.yaml` (e.g. county, special district, conservation corps, land trust, professional society, foundation) |
| 5 | `jurisdiction` | string | should | e.g. `US`, `US-PA`, `US-WA`; region bucket for multi-state |
| 6 | `role_in_emst` | enum | always | `host | incubator | funder | pilot-anchor | pilot-organization | design-partner-federal | design-partner-state | design-partner-local | shadow-user | workforce-board | module-advisory-partner | module-steward | consortium-member | validation-partner | research-partner | data-provider | co-publisher | adopter | vendor-conformance | other` |
| 7 | `stage` | enum | always | `stage-0 | stage-1a | stage-1b | stage-2 | stage-3 | ongoing` (ADR-0014) |
| 8 | `rung` | enum | always | adoption ladder: `1-aware | 2-try | 3-use-in-one-decision | 4-embed-in-system | 5-co-govern` (AS adoption roadmap §4) |
| 9 | `commitment_summary` | string | always | what the organization commits to, in one or two plain sentences (e.g. "draft three to five PDs for realigned positions using the 0400 Kit and send them through normal classification review") |
| 10 | `artifact_type` | enum | always | `letter-of-intent | MOU | DUA | MSA | advisory-partner-letter | grant-agreement | host-agreement | CESU-task-agreement | contract | written-confirmation | public-statement | other` |
| 11 | `artifact_reference` | string | if signed | repository path or document ID of the executed artifact or a redacted copy; never a confidential document itself |
| 12 | `gate_artifact` | pipe list | if applicable | the gate instrument EMST IDs are to appear in: `PD | class-spec | posting | assessment | crediting-plan | staffing-plan | IDP | training-plan | curriculum-map | grant-report | ETPL-review | workforce-pell-program | other` (feeds M-08, M-18) |
| 13 | `emst_release_cited` | string | if applicable | release ID the artifact pins (e.g. `2.0.0-rc.1`) |
| 14 | `status` | enum | always | `offered | signed | active | completed | lapsed | withdrawn | terminated` |
| 15 | `date_offered` | date | if offered | ISO 8601 |
| 16 | `date_signed` | date | if signed or later | ISO 8601; the date that makes the commitment real |
| 17 | `effective_from`, `effective_to` | date | if signed | ISO 8601 |
| 18 | `review_by` | date | always | next review; ≤ 12 months after the last review |
| 19 | `emst_signatory_role` | string | if signed | role title, e.g. "Project lead" <!-- PENDING Q3: until a host exists the project lead signs; EPIC if it confirms incubation and the lead so decides --> |
| 20 | `partner_signatory_role` | string | if signed | role title only |
| 21 | `emst_contact_role` | string | always | e.g. "Pilot coordinator", "Managing Editor" |
| 22 | `partner_contact_role` | string | should | role title or office (e.g. "Human Capital Office, classification branch") |
| 23 | `year_five_owner_org` | string | if signed | the organization that will be accountable in year five for maintaining what this commitment produces (may be the partner, the Steward or a named successor) |
| 24 | `year_five_owner_role` | string | if signed | the accountable role at that organization |
| 25 | `year_five_plan` | enum + text | if signed | `maintained-by-owner | transfers-to-steward | transfers-to-successor | sunsets-by-design | unknown` followed by `; ` and a short note. `unknown` is allowed but is reported as a risk in every quarterly summary |
| 26 | `funding_usd` | number | if funder or paid | committed amount; blank otherwise |
| 27 | `funding_period` | string | if funding | e.g. `2027-01..2029-12` |
| 28 | `data_shared` | enum | always | `none | public-documents | de-identified-artifacts | aggregates-only` — never person-level |
| 29 | `personal_data` | boolean | always | must be `false` |
| 30 | `tribal_related` | boolean | always | `true` only for a Tribal government's or organization's own commitment or Tribal-related terms |
| 31 | `tac_approval_id` | string | if `tribal_related = true` | TAC decision ID; a row with `tribal_related = true` and no ID fails CI |
| 32 | `feeds_metrics` | pipe list | should | e.g. `M-08|M-10|M-18|M-25|M-29|AS-G1a|AS-G1b|AS-G1c|AS-G1d` |
| 33 | `evidence_label` | enum | always | `E` when the artifact is on file; otherwise the row cannot be `signed` |
| 34 | `source` | string | always | where the evidence lives (e.g. "executed MOU, Steward records, redacted copy at …") |
| 35 | `recorded_by_role` | string | always | role title |
| 36 | `recorded_on` | date | always | ISO 8601 |
| 37 | `last_reviewed_on` | date | always | ISO 8601 |
| 38 | `notes` | string | may | no personal data |

A machine-readable version of this table for CI is in `commitment_register.schema.json` (Frictionless Table Schema).

## 4. Validation rules (for DE's CI)

1. `personal_data` is `false` on every row; any email address, phone number or personal-name pattern in any field fails the build.
2. `status ∈ {signed, active, completed}` ⇒ `date_signed`, `artifact_reference`, `year_five_owner_org`, `year_five_owner_role`, `year_five_plan` present and `evidence_label = E`.
3. `tribal_related = true` ⇒ `tac_approval_id` present. While no TAC exists, CI rejects any such row. <!-- PENDING Q1 -->
4. `review_by` is in the future at build time for every row not `completed`, `lapsed`, `withdrawn` or `terminated`; overdue rows are listed in the build report.
5. `commitment_id` values are unique and append-only (edits change status and dates; rows are never deleted).
6. **Claims check:** any organization named in a release artifact, kit or publication with the words *committed, partner, pilot organization, design partner, adopter, steward, funder, co-publisher* must appear in the register with `status ∈ {signed, active}` and a role matching the claim; otherwise the claims-hygiene lint fails (ADR-0027 §3).

## 5. What is computed from it (never typed)

Counts by role, stage, rung and status; M-10 (federal and state agencies with signed agreements naming a use case, an artifact and data terms); M-18 (live gate artifacts carrying EMST IDs, by agency and state); M-25 (adopters by actor type, Tribal never a target); M-29 (years of committed stewardship funding with a named steward); AS-G1a–d; the share of signed commitments with `year_five_plan = unknown`. These appear in the quarterly adopter bulletin and in the gate evidence packs.

## 6. Current state

The register is empty on 2026-10-23. **No organization has committed to EMST v2.** Phase 2 and Phase 4 documents that name organizations (The Corps Network, SAF, NASF, ECOS, PPS, EPIC, USFS, DOI/USWFS, OPM, Pennsylvania and others) name them as **candidates or prospects only**.
