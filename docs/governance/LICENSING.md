# EMST Licensing Notices

- **Work package:** WP-13 · **Author:** A10b (AS) · **Date:** 2026-10-23
- **Builds:** ADR-0013 (accepted; its condition — the project lead's CC0 dedication of v1-derived content — was **met on 2026-10-23**, Q2, recorded in `docs/decisions/PROJECT_LEAD_DECISIONS.md`), ADR-0007 §D 9 (Tribal namespace), ADR-0010 (releases, DOI), SPEC §16.3, governance charter Art. 10–11.
- **Status:** draft text for the three licence files and the third-party licence register that ship with each release. The CI checks it relies on are DE's (ADR-0013 consequences). This page is not legal advice; counsel for the Steward should review it before 2.0.0.

> **AS dissent, recorded and not reopened here.** AS argued for CC BY 4.0 on content text (provenance, adoption measurement, funder visibility). The CA chose CC0 for everything adopters embed, securing version citation through marks, DOIs and release stamps instead (ADR-0013, dissent). This notice implements the decision as made.

---

## 1. The licensing set

| What | Licence | Why |
|---|---|---|
| **EMST-authored data and standard text**: L0 vocabularies, schema and JSON-LD context, identifiers and the ID registry, competency / knowledge / task / indicator / role / variant / enactment text, crosswalk mapping sets (IDs only for external systems), computed views, release bundles and exports, `docs/standard/SPEC.md` | **CC0 1.0 Universal** (public-domain dedication) | Adoption happens by embedding EMST in PDs, class specs, assessments, HR systems and grant curricula; CC0 removes attribution chains exactly there (ADR-0013 §1, rationale). |
| **Narrative publications**: the flagship report, briefing decks, role-change briefs, research papers, explorer prose, governance and adoption documents authored as publications | **CC BY 4.0** | Attribution matters for visibility and funding where content is read rather than embedded (ADR-0013 §2). |
| **Code**: scripts, build, CI, tests, the explorer's source | **Apache-2.0** | Permissive with a patent grant; matches OpenLMP (ADR-0013 §3). |
| **Third-party material** | **Its own terms** (register in §5) | Never relicensed; kept out of CC0 files; IDs only in crosswalks (ADR-0013 §5). |
| **Tribal-contributed content** (none exists; none may be accepted until a TAC exists and approves) | **The contributor's chosen licence**, with labels and a withdrawal right; excluded from the bulk CC0 release unless the contributor opts in | CARE authority to control; open releases cannot be recalled (ADR-0013 §6; ADR-0007 §D 9). |

**Provenance and version citation are secured by marks and release engineering, not by licence:** every export and page carries the release ID and DOI; `CITATION.cff` carries a non-binding citation request; "EMST", "EMST-conformant" and "EMST-mapped" are marks held in trust by the Steward and require a conformance check; modified versions may not be called EMST (ADR-0013 §4; charter Art. 11).

## 2. Repository path map

| Path | Licence | Notes |
|---|---|---|
| `data/v2/**` (except Tribal namespaces), `vocab/**`, `schema/**` | CC0 1.0 | One licence per record; `license` field = `CC0-1.0` unless governed (SPEC §4) |
| `data/v2/**/tribal-*/**` (reserved; empty) | contributor's licence | excluded from bulk CC0 bundles unless opted in |
| `data/v2/registers/commitments.csv` | CC0 1.0 | organization-level facts only; no personal data (commitment register schema) |
| `docs/standard/**` | CC0 1.0 | standard text |
| `docs/decisions/**` | CC0 1.0 **[J]** | decision records are the standard's provenance and are cited from CC0 records; CA to confirm |
| `docs/research/**`, `docs/governance/**` and `docs/adoption/**` narrative documents | CC BY 4.0 | narrative publications |
| `docs/adoption/*_template.md`, `docs/governance/module_stewardship_agreement_template.md`, the commitment register schema, `docs/adoption/ecosystem_atlas.csv` | CC0 1.0 **[J]** | templates are copied into adopters' own agreements and the atlas is data; treating them as data removes attribution friction. CA to confirm this reading of ADR-0013 §1. |
| `scripts/**`, `tests/**`, `.github/**`, explorer source | Apache-2.0 | DCO sign-off on contributions |
| `external/**` | each file's own licence | attribution file per source; never merged into CC0 bundles |
| `legacy/**` and `data/v1_baseline/**` (v1 content authored by the project lead) | **CC0 1.0** | The project lead dedicated the v1 text (competency titles, descriptions, tasks, indicators, source text) to CC0 on 2026-10-23, resolving v1's CC0 / CC BY 4.0 contradiction [E: CP-005, AS-048]; v2 records derived from it ship in the CC0 data files. Third-party material in `legacy/` is **not** covered (next row). <!-- DECIDED Q2 (2026-10-23, PROJECT_LEAD_DECISIONS.md): CC0 dedication of the v1 text accepted --> |
| `legacy/v1/reference_only/` | third-party, git-ignored | read and cite, never copy (SAF handbook) |

## 3. Licence files (text to place at the repository root in the first v2 commit)

### `LICENSE`

```
Copyright 2026 the EMST contributors.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
the code in this repository except in compliance with the License. You may obtain
a copy of the License at https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

Scope: code only (scripts/, tests/, .github/, explorer source). Data, the
standard and publications are licensed separately: see LICENSE-DATA and
LICENSE-PUBLICATIONS. Contributions are accepted under the Developer
Certificate of Origin; inbound terms equal outbound terms.
```

### `LICENSE-DATA`

```
EMST data and standard — CC0 1.0 Universal (public-domain dedication)
https://creativecommons.org/publicdomain/zero/1.0/

To the extent possible under law, the EMST contributors have waived all
copyright and related or neighboring rights to the EMST-authored data, vocabularies,
schema, identifiers, crosswalk mapping sets, computed views, release bundles and
the EMST specification, as listed in docs/governance/LICENSING.md §2.

Exclusions (not covered by this dedication):
  - third-party material, which keeps its own terms (see the third-party licence
    register shipped with each release); crosswalks contain external identifiers only;
  - Tribally stewarded namespaces (emst:tribal-<steward>/...), which carry the
    contributor's chosen licence and are excluded from bulk releases unless the
    contributor has opted in;
  - third-party material held with the v1 files (e.g. the SAF Accreditation
    Handbook), which is never redistributed.

The EMST v1 text authored by the project lead (legacy/v1/ and data/v1_baseline/)
is dedicated to the public domain under CC0 1.0 by its author (decision recorded
in docs/decisions/PROJECT_LEAD_DECISIONS.md, 2026-10-23); v2 records derived
from it are covered by this dedication.

Citation request (not a condition): please cite the release ID and DOI, e.g.
"EMST <release>, doi:<doi>". "EMST", "EMST-conformant" and "EMST-mapped" are marks
held in trust by the EMST Steward; modified versions may not be called EMST.

Use notice: EMST is not a selection instrument, not a classification basis and
not for reductions in force, adverse action or performance ratings. An employer's
selection use is defensible only after its own job analysis confirms the content.
Indigenous knowledge is a distinct body of environmental expertise held and
governed by Indigenous nations and is out of scope by design.
```

### `LICENSE-PUBLICATIONS`

```
EMST narrative publications — Creative Commons Attribution 4.0 International
https://creativecommons.org/licenses/by/4.0/

Applies to the narrative documents listed in docs/governance/LICENSING.md §2
(reports, briefs, decks, research and governance documents authored as
publications). Attribution: "Environmental Management Skills Taxonomy (EMST)
contributors, <title>, <release or date>, <DOI or URL>, CC BY 4.0."
Third-party figures, quotations and data inside publications keep their own
terms and are credited where they appear.
```

## 4. Dedication statement

The project lead **accepted** the CC0 dedication on 2026-10-23 (Q2; `docs/decisions/PROJECT_LEAD_DECISIONS.md`). The decision covers the v1 content in `legacy/v1/` and `data/v1_baseline/` authored by the project lead and excludes third-party material. The statement below is the optional signed form the lead may add to that file for downstream counsel. <!-- DECIDED Q2 (2026-10-23, PROJECT_LEAD_DECISIONS.md): CC0 dedication of the v1 text accepted -->

> I, the author of the EMST v1 content (competency titles, descriptions, tasks, proficiency statements, indicators and the v1 source text), dedicate that content to the public domain under CC0 1.0 Universal, so that EMST v2 records derived from it may be released under CC0. Dated and signed: ____________.

The decision applies now; the signature is a convenience for counsel, not a condition.

## 5. Third-party licence register (seed)

Each release ships this register, regenerated from `data/v2/` and `external/` by CI. "IDs only" means a CC0 file may hold the external identifier but not the external text. Rows marked **verify** must be checked by DE before any text from that source is bundled; until then only identifiers are used.

| Source | Owner | Version pinned | Terms (as recorded) | Verification | How EMST uses it | Where it may live |
|---|---|---|---|---|---|---|
| O*NET database (tasks, DWAs, O*NET-SOC 2019) | National Center for O*NET Development (USDOL/ETA) | 31.0 (Aug 2026) [E: V3-01, V4-08] | CC BY 4.0 (ADR-0013 §5) | licence named in ADR; text not re-read this pass — **verify attribution wording** | X2/X3 crosswalks; external exposure joins | IDs in CC0 files; any text in `external/onet/` with attribution |
| SOC 2018 | U.S. BLS / SOC Policy Committee | 2018; SOC 2028 final planned 2027 [E: V3-02] | U.S. government work [J] | verify | X3 codes | IDs in CC0 files |
| CIP 2020 and CIP–SOC crosswalk | NCES (IES) | CIP 2020 [E: V3-09] | U.S. government work [J] | verify | X6 | IDs in CC0 files |
| ESCO | European Commission | v1.2.1 (Dec 2025) [E: V4-09] | Commission reuse terms with attribution [J] | **verify** | X7 | URIs in CC0 files; labels in `external/esco/` only if terms permit |
| OPM classification and qualification standards, FWCI frameworks, series list | U.S. OPM | dated per issuance (OPM series register) | public domain (U.S. government work) [J: ADR-0013 rationale] | per issuance | X4, X9 | IDs and short quotations with citation |
| DOL AI Literacy Framework (TEN 07-25) | USDOL/ETA | Feb 13 2026 (SPEC §15) | U.S. government work [J] | verify | X12 area names | official names as identifiers |
| BLS Employment Projections incl. AI exposure categories | U.S. BLS | 2025–35 (Aug 27 2026) [E: V4-07] | U.S. government work [J] | verify | L5 external signals | values with citation |
| Anthropic Economic Index datasets | Anthropic | releases through 2026-06-26 [E: V4-01] | CC BY (ADR-0013 §5, citing V4-01) | recorded by V4 | external-index assessments keyed to O*NET tasks | aggregated values in L5 with attribution; raw data in `external/` |
| Microsoft "Working with AI" results files | Microsoft Research | arXiv v6 (2025-12-22) [E: V4-02] | repository licence not recorded | **verify** | external-index assessments | `external/` only until verified |
| Eloundou et al. "GPTs are GPTs" labels | OpenAI (GitHub) | O*NET 27.x task labels | repository licence not recorded | **verify** | external-index assessments | `external/` only until verified |
| Lightcast data (postings, skills taxonomy) | Lightcast | per contract | **licensed by contract, not open** [E: V4; ADR-0013 §5] | recorded by V4 | only permitted aggregates under contract | never in CC0 files; aggregates only as contract permits |
| USAJOBS API and historic announcements | U.S. OPM | snapshot dates | API terms of service [J] | verify | de-identified derived signals and hashes only (ADR-0012 I-1 §2) | derived signals |
| OpenLMP plan components | OpenLMP maintainers | release pinned per build | CC0 data; Apache-2.0 code [E: AS-046] | sister repo | L5 demand signals | CC0 |
| CEQ NEPA and Permitting Data and Technology Standard | CEQ / GSA TTS | v1.2 (Aug 18 2025) [E: V2-08] | CC0 (ADR-0013 rationale) [J] | verify | alignment reference | CC0 |
| Federal AI Use Case Inventory | OMB (GitHub) | 2025 inventory (summary as of Apr 13 2026) [E: V4-15] | U.S. government work [J] | verify | deployment-stage signals | values with citation |
| SAF Accreditation Handbook 2024 and other accreditor criteria (ABET, EHAC, NAAEE, NASPAA) | each accreditor | as cited | copyrighted | — | X6 alignment | **paraphrase and cite; never copy** (SAF handbook rule) |
| Credential-body exam blueprints and job-task analyses | each credential body | as cited | proprietary | — | X10 evidence equivalence | only under a data agreement; never scraped (DB issue 2) |
| NWCG PMS 310-1; USWFS–USFS Federal Wildland Fire Qualifications Supplement | NWCG; DOI/USFS | PMS 310-1 (Jan 23 2026); aligned federal standards effective Jan 2027 [E: V3-13] | U.S. government publications [J] | verify | fire crosswalk IDs | IDs and citations |
| CARE Principles for Indigenous Data Governance | Global Indigenous Data Alliance (publication in *Data Science Journal*) | 2020 | CC BY (journal article) [J] | verify | cited as governing principle | citation only |
| Local Contexts Notices and Labels | Local Contexts | — | Labels are applied **only by communities**; Notices by institutions | — | only as a TAC directs | — |

**Owner:** DE maintains this register; TSC reviews it each release; WP-15 re-checks every row marked *verify* before 2.0.0.
