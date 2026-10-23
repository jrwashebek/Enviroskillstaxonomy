# EMST Indigenous Data Governance Policy (DRAFT 0.1)

> **AI-drafted. Requires review and revision by Tribal representatives before use.**
>
> This draft was written by an AI agent playing the Tribal Nations Workforce & Sovereignty Advisor (TN). It does not speak for any Tribal nation. It applies the CARE Principles alongside FAIR. However, the CARE source text (TN-060) and the Local Contexts materials (TN-061) could not be re-read this session. Their wording must be checked against the sources before adoption. Until the Tribal Advisory Council (TAC; see `tribal_engagement_protocol.md` §5) adopts a version, **sections 4 and 6 apply as interim hard rules** and everything else is a proposal. Evidence labels: [E] evidence (source IDs in `sources.csv`), [J] judgment, [S] speculation.

---

## 1. Scope

This policy applies to:
- the EMST GitHub repository (all branches and history);
- the data pipelines, including LLM-based extraction of skills from postings, position descriptions, curricula and plans;
- the EMST tool and any dashboards;
- every release;
- any agency, NGO or vendor that hosts or redistributes EMST;
- every team member, including AI agents.

## 2. Definitions (draft)

- **Indigenous data.** Data about Indigenous peoples, nations, lands, waters, resources, knowledge and cultures, at the individual or collective level, whoever collected it. [J; consistent with USIDSN usage, TN-062, not re-read]
- **Indigenous knowledge (IK).** Uses DOI's definition: "a body of observations, oral and written knowledge, innovations, technologies, practices, and beliefs" developed by Indigenous Peoples through interaction with the environment. IK is distinct from local or individual knowledge that has not been validated within an Indigenous culture. [E: TN-018 §7.4–7.5]
- **Confidential Tribal information.** Information shared by a Tribe in confidence, consultation records, culturally sensitive information, and the locations of cultural, sacred, burial, gathering or archaeological sites.
- **Tribal-contributed content.** Any text, data or review that a Tribe, inter-Tribal organization or Tribal professional provides to EMST.
- **Tribal workforce data.** Data about the jobs, positions, staffing, pay or postings of Tribal employers.
- **Tribal-related content.** Any EMST content that describes working with Tribal nations, Tribal programs or Tribal employers, or that carries an L2 (Cultural Rights & Self-Determination) tag.

## 3. Principles

1. **CARE alongside FAIR.** The FAIR principles (findable, accessible, interoperable, reusable) govern how data are engineered. The CARE principles (collective benefit, authority to control, responsibility, ethics) govern whether and on what terms Indigenous data are used at all. Where they conflict, CARE prevails for Indigenous data. [J; TN-060]
2. **Not ours to hold.** The project describes the work that non-Tribal professionals do with Tribal nations. It does **not** describe Tribal nations' knowledge, and it does not hold their confidential information.
3. **Minimize.** If Tribal data are not needed for a stated, approved purpose, the project does not collect them.
4. **Public is not permission.** That something is publicly available (on a website, in a book, in a federal record) does not make it the project's to republish or analyze when it is Indigenous knowledge or confidential Tribal information. [J]
5. **Assume disclosure.** Anything EMST holds may be disclosed. That can happen through open release, forks, or public-records law if a government adopter hosts it. DOI's own policy warns staff not to overstate how well an agency can protect IK under FOIA. [E: TN-018 §7.6.A(1)(b)] The safest protection is not holding the material at all.

## 4. Never collected, stored or published (interim hard rules)

1. **Indigenous knowledge content.** This covers descriptions of ecological knowledge, cultural fire methods or objectives, plant or animal uses, harvest practices, place names, oral histories, stories, and ceremonial or religious information. It applies even when the content is publicly available elsewhere.
2. **Location or description of sensitive places.** This covers sacred sites, traditional cultural properties, burial sites, cultural gathering areas and archaeological sites. Plans already hold these back. For example, the Mt. Baker-Snoqualmie 1990 standard maintains site confidentiality under NHPA §304. The OpenLMP pipeline withholds them. [E: TN-044, TN-054]
3. **Consultation content.** This covers records, minutes, comment letters shared in confidence, and confidential appendices.
4. **Characterizations of named Tribes.** No rankings, "capacity," "readiness," "maturity," compliance or performance scores, and no change indicators for a named Tribe's programs, unless that Tribe has agreed.
5. **Person-level data about Tribal employees or citizens.** This includes Tribal citizenship or enrollment, Indian-preference status, and any identifier.
6. **AI-exposure or automation scores attached to named Tribal programs or Tribal-specific role variants.** Exception: the TAC approves and the relevant Tribal professionals have validated the scores.
7. **Tribal documents.** This covers plans, codes, ordinances, internal policies and workplans, unless a Tribe asks for inclusion and agrees to the terms. This mirrors OpenLMP's rule. [E: TN-054]
8. **Machine-inferred Tribal content.** No LLM or NLP outputs that infer Tribal-specific skills, practices or knowledge from Tribal documents.
9. **Names, seals or logos** of Tribes or inter-Tribal organizations used to imply endorsement or partnership without written permission.

**The veto applies here.** TN's position is that items 1–3 are never the project's to include, whatever the purpose. A TAC may decide otherwise for content its own nations contribute and control. The project cannot.

## 5. What EMST may hold, and on what conditions

| Content | Allowed? | Conditions |
|---|---|---|
| Competencies for **non-Tribal** professionals working with Tribal nations (TN-C01 to TN-C12; rewritten 6.5.1, 7.1.1) | Yes | Authored by the project from public law and policy; reviewed and approved by the TAC before publication; L2-tagged; no description of IK content |
| Public federal and state law, policy and plan requirements about Tribes (EO 13175, 301 DM 7, Section 106 rules, treaty-rights plan components) | Yes | Cite by ID; quote only non-confidential public text; date-stamp, because policy status changes [E: TN-014] |
| Aggregate demand signals from **federal and state** documents (e.g., OpenLMP Tribal coordination touchpoints) | Yes | Counts and component IDs; no reproduction of confidential appendices; no Tribe-level indicators |
| Federal positions serving Indian Country (BIA, USWFS, IHS environmental health) | Yes | Federal public records; strip any Tribe-specific confidential detail |
| **Tribal-employer role variants** (e.g., TN-C13) | Only with approval | Function-level description; validated by Tribal professionals; TAC approval; opt-in naming only |
| **Tribal-contributed content** | Only under agreement | Written contribution agreement (§7); separate namespace; license chosen by the contributor (§12); labels (§7); withdrawal right (§9) |
| **Tribal employer job postings** | Not by default | See §6 |

## 6. Tribal workforce data and change signals (interim hard rules)

**6.1 Tribal employer job postings.** Tribal postings are public recruitment announcements by sovereign employers. Analyzing them is a secondary use the employer did not ask for. [J]

- **Default: excluded from ingestion.** The pipeline maintains a list of Tribal employers (Tribal governments, Tribal departments, inter-Tribal organizations, TCUs, Tribal enterprises). Postings from those employers are quarantined and not processed.
- **Release from quarantine requires a TAC decision.** If the TAC allows any use, the following conditions apply as minimums unless the TAC sets stricter ones:
  - derived signals only, with no stored full text;
  - no model training or fine-tuning on Tribal postings;
  - results reported only in aggregates that cannot identify a Tribe, with a suppression threshold the TAC sets;
  - no Tribe-identified counts, pay or trends without that Tribe's consent;
  - a per-Tribe opt-out list that is always honored.

**6.2 Change signals that touch Tribal programs.** This covers, for example, "Tribal forestry staffing declining" or "Tribal fire roles moving to USWFS".

- **Source.** Signals must come from public, non-confidential sources and carry date and attribution, like every L5 record.
- **Flag.** Each such signal carries the flag `tribal_programs: true`.
- **Review gate.** Flagged signals are **held from release until the TAC has reviewed them**. Where Tribes or inter-Tribal organizations have published their own interpretation, the signal links to it, and the Tribal sources are preferred. [J] This report's `role_signals.csv` rows TN-S01 to TN-S16 are themselves subject to this gate.
- **Named Tribes.** No signal names a specific Tribe unless the source is that Tribe's own public statement (e.g., congressional testimony; TN-006) **and** the use is approved by the TAC.

**6.3 Exposure assessments.** Tasks that require handling confidential Tribal information are tagged `governed_data: tribal`. Their AI-exposure classification must be conditional: AI assistance is permissible only where the Tribe has authorized it. v1 coded 6.5.1 T3 and 5.3.3 T2 as AI-augmentable without this condition [E: TN-052, TN-046]. The instrument needs a standing rule (proposal P-TN-09 in `report.md`).

## 7. Labeling, consent records and metadata (proposal for DE/IA)

Every EMST record that may involve Indigenous data carries:

| Field | Values | Notes |
|---|---|---|
| `indigenous_data_flag` | true / false | Set at ingestion; default true for anything from or about a Tribal source |
| `tribal_authority` | name of the governing Tribe or organization, or "none" | Who decides about this record |
| `consent_record_id` | ID | Links to the consent log (protocol §7) |
| `approval_status` | pending / approved / withdrawn | Release builds include only `approved` |
| `local_contexts_ids` | Notice or Label IDs | **Labels are applied only by Tribes.** The project may apply Notices (e.g., a TK or BC Notice) to signal that Indigenous rights or interests may attach. [J; TN-061, confirm terms] |
| `license` | as chosen by the contributor | Never inherited from the project default (§12) |
| `ai_use_permitted` | false (default) / true | Only an explicit grant sets true |
| `sensitivity` | public / restricted / confidential | Confidential records are never stored in the repository (§4) |
| `attribution` | as specified by the contributor | May be "none" |

## 8. Storage

- **Pre-approval storage.** Tribal-contributed content is **not committed to the public repository before approval**. Git history is hard to purge and forks are permanent.
- **Working copies.** These are held either by the contributing Tribe, with EMST linking or referencing, or in an access-controlled location that the Tribe agrees to.
- **AI tools and cloud services.** Nothing covered by this policy is placed in third-party AI tools or cloud AI APIs unless `ai_use_permitted` is true for that record.
- **Agency hosting.** If an agency hosts EMST, Tribal-contributed content stays under the contributor's terms. Hosting agreements must say so, and contributors must be told about any records-law exposure first. [J; TN-018]

## 9. Withdrawal

- **Receipt.** A withdrawal request from a contributor or the TAC is logged on receipt.
- **Removal.** The content is removed from working branches within 10 business days and excluded from the next release. Sooner if the TAC asks.
- **Changelog.** The entry reads "withdrawn at the contributor's request" without reproducing the content.
- **Downstream notice.** Known downstream users and hosts are notified and asked to delete.
- **Open releases.** The contributor is told plainly that copies of openly licensed releases cannot be recalled. This is why §12 keeps contributed content out of open-licensed releases unless the contributor chooses otherwise.

## 10. Attribution

- **Contributor's terms.** Attribution follows the contributor's instructions, which may be Tribe, department, individual, or none.
- **Individual or Tribal government.** A position of a Tribal government is never attributed to an individual. An individual's view is never presented as a Tribal position.
- **No implied endorsement.** "Reviewed by the TAC" means only what the TAC agrees it means. It never means "endorsed by Tribes."
- **AI-drafted labels.** AI-drafted material is labeled as AI-drafted, including this policy.

## 11. CARE alongside FAIR: how each principle shows up in EMST

| Principle | EMST practice |
|---|---|
| **F**indable | Persistent IDs for all records, but metadata for restricted Tribal content is itself restricted. Findability does not override §4. |
| **A**ccessible | "As open as Tribal authority permits." Access conditions travel with the record (`license`, `local_contexts_ids`). |
| **I**nteroperable | Label and Notice identifiers and consent IDs are carried in exports (JSON-LD/CTDL), so downstream systems inherit the conditions. Coordinate with IA. |
| **R**eusable | Reuse conditions are explicit and machine-readable. No reuse beyond the stated purpose. |
| **C**ollective benefit | Outputs that Tribes request (protocol §11); Tribal-controlled workforce analyses |
| **A**uthority to control | TAC binding authority; per-contribution consent; withdrawal; Tribal law prevails |
| **R**esponsibility | Report back to the TAC annually; disclose limits (records law, open-release permanence); build no dependency on Tribal unpaid labor |
| **E**thics | Minimize; assess harms before release; never characterize named Tribes without consent; no AI processing without consent |

## 12. Licensing (flag for DE and AS)

The OpenLMP pattern licenses project data as CC0 [E: TN-054]. CC0 is appropriate for the project's own competency text, including content about working with Tribes once the TAC approves it.

**CC0 must not attach to Tribal-contributed content.** That content:
- lives in a separate namespace (for example `emst:tribal/<steward>/…`);
- carries the license the contributor chooses, which may be non-open;
- is excluded from the CC0 bulk release unless the contributor opts in.

This needs a schema-level separation, not a README note.

## 13. AI and the NLP pipeline (rules for IA)

1. **Excluded inputs.** No Tribal-contributed, Tribal-confidential or IK content goes into prompts, retrieval indexes, fine-tuning sets or evaluation sets.
2. **Quarantine at ingestion.** Use the Tribal employer list (§6.1). Documents from Tribal sources are quarantined before any LLM processing.
3. **Machine inference.** Model outputs that mention Tribal roles or programs are labeled "machine-inferred" and routed to the `tribal_programs` review gate.
4. **Gold sets.** Gold-standard reference sets for evaluation must not contain Tribal documents unless the TAC approves.

## 14. Governance and incidents

- **Ownership.** The TAC owns this policy once constituted. Until then, the project lead holds it on the interim rules in §4 and §6.
- **Changes.** Changes require TAC approval.
- **Incident.** If covered material is published in error, the project:
  1. takes it down within 24 hours of discovery;
  2. notifies the affected Tribe and the TAC;
  3. purges it from history where feasible;
  4. reports the root cause and the fix to the TAC.

## 15. Automated checks (proposal for DE)

CI should fail a release build when any of these occur:
- a record with `indigenous_data_flag=true` lacks `approval_status=approved`;
- a record with `sensitivity=confidential` exists anywhere in the repository;
- coordinates co-occur with cultural-site vocabulary;
- a document from a quarantined Tribal employer appears in pipeline outputs;
- a `tribal_programs=true` signal lacks a TAC review ID.

## 16. Questions for Tribal reviewers

1. Is the list in §4 complete, and is anything on it over-broad?
2. Should EMST ever analyze Tribal employers' public postings? If so, under what conditions?
3. Which Notices or Labels should EMST use, and who should apply them?
4. What licensing defaults should apply to Tribal-contributed content?
5. Do Tribes want Tribal-specific role variants in EMST at all, or only competencies for their non-Tribal partners?
