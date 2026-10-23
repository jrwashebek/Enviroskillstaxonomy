# EMST Tribal Gate Procedures (draft 0.9)

> **AI-drafted. Requires review and revision by Tribal representatives before use.**
> An AI agent (A10b, AS role) wrote these procedures from ADR-0007, SPEC §16.1, the build plan and the TN role's Phase 2 drafts (`docs/research/tribal-sovereignty/tribal_engagement_protocol.md` and `indigenous_data_governance_policy.md`, both themselves AI-drafted and unreviewed). **No Tribal nation, inter-Tribal organization or Tribal professional has reviewed this document.** It does not speak for any Tribe and it authorizes no outreach. Its purpose is the opposite: to keep the project's gates **closed** until the conditions in §2 are met, and to stop Tribal-related content leaking into anything EMST publishes.

- **Work package:** WP-13 (owner A10b AS; TN is gate reviewer under G-TN) · **Date:** 2026-10-23 · **Licence:** CC BY 4.0
- **Builds:** ADR-0007 §C–§D, ADR-0012 I-1 §5, ADR-0013 §6, ADR-0015 §3, ADR-0023 §4, ADR-0028 §5; SPEC §4, §16.1; `PHASE4_BUILD_PLAN.md` §1 rule 4; `questions_for_project_lead.md` Q1, Q9.
- **Status:** draft; the gates it describes are **in force now** as build invariants, because ADR-0007 is accepted for the vetoes and the content hold.

---

## 1. Two gates

| Gate | What it controls | State today | Opens when |
|---|---|---|---|
| **Gate C — content gate** (G-TN in the build plan) | Whether any Tribal-related record, text, signal, variant, example or claim can reach a release, kit, view, publication or communication | **Closed.** Everything Tribal-related is an internal draft, `approvalStatus = pending-tribal-review`, excluded by CI | Item by item, only on a recorded TAC approval (§5). Never opens in bulk. |
| **Gate O — outreach gate** | Whether anyone acting for EMST contacts a Tribal nation, an inter-Tribal organization or a Tribal professional about EMST | **Closed.** No outreach has occurred or is authorized | Only when every precondition in §2 is met |

Under the default to Q1 (no answer from the project lead), **both gates stay closed indefinitely**. <!-- PENDING Q1 -->

## 2. Preconditions for any Tribal outreach (Gate O)

No outreach of any kind — content review, research participation, Delphi or job-analysis panels, Workforce Voice seats (stratum S-H), sentinel channels, pilot recruitment, data requests, event attendance, publicity or "partner" listings — takes place until **all** of the following are true and recorded in `docs/decisions/`:

1. **The project lead has answered Q1** — accepting (a) binding TAC consent authority, (b) the charter carve-out so no body overrides the TAC on Tribal-related content, and (c) compensation budgeted before first contact. <!-- PENDING Q1 -->
2. **Reviewer compensation is funded**, not merely planned: a budget line exists in an executed grant or host budget for honoraria at professional rates, travel and the 0.5 FTE Tribal Liaison, with a mechanism to pay the party a Tribe directs (an individual, or the Tribal government by agreement). If it cannot be funded, the gate stays closed and the pilot proceeds without Tribal outreach (ADR-0007 §10; TN open Q5). <!-- PENDING Q9 -->
3. **A Tribal Advisory Council exists**, constituted by Tribal governments and inter-Tribal organizations, and has adopted its own terms of reference, protocol and data policy.
4. **The project lead has adopted the engagement protocol and data governance policy as working drafts**, labelled AI-drafted, for Tribal reviewers to revise or discard.

**The one exception, and why it is flagged.** Condition 3 cannot be met without some contact, because a TAC must be constituted by Tribal governments and inter-Tribal organizations themselves. The only contact these procedures contemplate before a TAC exists is the **TAC-formation step** in TN's protocol (§14 phase 1): a letter **signed by the project lead (never by an agent)** to a small number of inter-Tribal organizations, asking whether they wish to advise on whether and how a TAC should be formed, accepting "no", and offering compensation already funded. That step requires conditions 1, 2 and 4 and the project lead's explicit, separate approval recorded in the decision log. Under the Q1 default it does not happen. **[J]** This exception is an interpretation of WP-13's rule ("no outreach until reviewer compensation is funded and a TAC exists"); the CA and the project lead should confirm or strike it. <!-- PENDING Q1 -->

**Never, whatever the gate state:**

- AI agents do not contact Tribes, Tribal organizations or Tribal professionals, and do not draft anything presented as a Tribal perspective (protocol §12).
- Nobody scrapes directories or job boards for contacts, cold-emails Tribal employees about their employer's programmes, or treats a federal liaison or non-Tribal intermediary as a substitute for a Tribe (protocol §4).
- No Tribe's or Tribal organization's name, seal or logo is used, and no Tribe is listed as a partner, prospect, invitee or "engaged", without written permission (protocol §4, §8).
- EMST outreach is never called "consultation" and never implied to satisfy any agency's consultation duty (protocol §1).
- Silence is not consent; a Tribe that does not respond has declined, and is not listed as having been asked (protocol §2, §8).

## 3. What the content gate covers (Gate C)

Tribal-related content is held under ADR-0007 §D. The held set includes at least:

| Held item | Where it may exist now | Marker |
|---|---|---|
| Successor to v1 7.1.1 (TN-C07) and the v1 5.3.2 and 6.5.1 successors | internal draft records | `approvalStatus = pending-tribal-review` |
| Every L2 ethical-lens definition and every L2 tag | internal drafts | same |
| TN-C01 … TN-C13; SC-C13 | internal candidate pool | same |
| Tribal role variants (Tribal environmental director, Tribal forester, Tribal FMO, THPO, and Tribal variants marked `tribal(held)` in `mvp_role_set.csv`) | internal drafts only | same |
| Tribal-flagged change signals (`tribalPrograms`/`careFlag`) and TN's role signals | L5 quarantine | same; never released |
| Tribal frictions (CM does not define them; the TAC decides what, if anything, is recorded) | none | — |
| The Tribal engagement protocol and Indigenous data governance policy | `docs/research/tribal-sovereignty/` as AI-drafted research | "AI-drafted; requires Tribal review" label |
| Tribal-related rows of the Ecosystem Atlas (inter-Tribal organizations, Indigenous data-governance standards and tools, Tribal programmes) | `docs/adoption/ecosystem_atlas.csv` with `tribal_related = true` | `release_status = held-pending-tribal-review` |
| Tribal-related protect decisions | none until the TAC decides | — |

Internal multi-rater analytical tagging is allowed (it is analysis, not taking Indigenous content) (ADR-0007 §D 8).

**Never held, because never collected (veto items, ADR-0007 §C):** content describing, ranking or credentialing Indigenous knowledge (V1); confidential Tribal information, even under access control (V2); characterizations of named Tribes (V3); Tribal employers' documents or postings by default, including in LLM pipelines (V4); a Tribal profession family (V5); person-level Tribal data, citizenship or preference status (ADR-0012 I-1 §5).

## 4. Build-time procedure (every merge)

1. **Flag at creation.** Any record that touches Tribal governments, Indigenous knowledge or Tribal data carries `indigenousDataFlag = true`, `approvalStatus = pending-tribal-review`, `sensitivity = restricted-governed`, `aiUsePermitted = false` and, where applicable, `governedData = tribal` (SPEC §4, §16.1). When in doubt, flag.
2. **CI blocks release builds** on any unapproved Tribal-related record, any confidential record anywhere in the repository, coordinates co-occurring with cultural-site vocabulary, a quarantined Tribal-employer document in pipeline outputs, or a `tribalPrograms` signal without a TAC review ID (SPEC §16.1; IDG policy §15). These checks may be tightened by the TSC; they may be relaxed only with TAC consent.
3. **G-TN review.** The TN gate reviewer checks every work package's output for leaks before the CA merges it: Tribal content in enactments, examples, signals, crosswalk rows, kit text, atlas rows or prose. A leak blocks the merge (`PHASE4_BUILD_PLAN.md` §1 rule 4).
4. **Pipeline quarantine.** IA's pipeline keeps a list of Tribal employers (Tribal governments and departments, inter-Tribal organizations, TCUs, Tribal enterprises); their postings and documents are quarantined before any LLM processing and are never used for training, retrieval, prompting or evaluation (ADR-0007 V4; IDG policy §6.1, §13).
5. **Statement on the face of every release.** "Indigenous knowledge is a distinct body of environmental expertise held and governed by Indigenous nations and is out of scope by design" (ADR-0007 §C; SPEC §16.1).
6. **Sector-wide statistics carry the caveat** that the Tribal workforce is under-measured by design (ADR-0007 consequences).

## 5. How an item would pass the content gate (once a TAC exists)

Proposed sequence, for the TAC to replace with its own:

1. The EB (or CA) prepares the item with its provenance, the public sources it rests on and a plain statement of what it is for; AI-drafted text is labelled as such.
2. The Tribal Liaison submits it to the TAC on the TAC's schedule (draft windows: 90–120 days where a Tribal government decision is needed; 30–45 days for staff-level review; extensions on request).
3. The TAC approves, approves with changes or conditions (labels, attribution, licence, `aiUsePermitted`), defers, or declines. **No decision means not approved.**
4. Only a recorded TAC approval ID changes `approvalStatus` to `approved`; CI checks for the ID.
5. The TAC may withdraw approval at any time; the item is removed at the next release or sooner if the TAC asks; the changelog says "withdrawn at the contributor's request" without reproducing it; known downstream users are notified.

Tribal-contributed content, if any is ever offered, goes into a reserved Tribally stewarded namespace (`emst:tribal-<steward>/…`) under the contributor's chosen licence, with a withdrawal right, excluded from the bulk CC0 release unless the contributor opts in (ADR-0007 §D 9; ADR-0013 §6).

## 6. Incidents

If Tribal-related or confidential material is found in a release, kit, view, publication or the public repository:

1. Take it down within 24 hours of discovery and freeze further releases containing it.
2. If a TAC exists, notify the TAC and any affected Tribe through the channel the TAC sets; if none exists, the project lead decides how to notify, and the incident is recorded.
3. Purge it from history where feasible (it may persist in forks; say so).
4. Record root cause and fix in `docs/decisions/` and report it to the TAC when one exists (IDG policy §14).

## 7. What EMST documents may and may not say meanwhile

| May say | May not say |
|---|---|
| Tribal nations are sovereign governments and employers; obligations owed to Tribal nations are core Statecraft content for every actor, under a content hold | that any Tribe, Tribal organization or Tribal professional was consulted, engaged, reviewed or approved anything |
| Tribal-related content is withheld until a Tribal Advisory Council constituted by Tribal governments and inter-Tribal organizations approves it | that EMST includes, describes or credentials Indigenous knowledge |
| The Tribal workforce is under-measured by design | Tribe-level statistics, rankings, capacity or readiness characterizations |
| EMST follows the CARE Principles for any Indigenous data matter (cite the GIDA publication, not a link to the former USIDSN domain) | any link to the domain formerly used by USIDSN, which now serves unrelated content [E: V2 verification, items TN-062 and TN-E03; ADR-0027 §3] |

## 8. Owners and review

- **Gate C reviewer:** TN role during Phase 4; the Tribal Liaison (reporting to the TAC) thereafter.
- **Gate O:** the project lead alone may open it, and only on the conditions in §2.
- **Review:** these procedures are replaced by the TAC's own once a TAC exists; until then the project lead reviews them annually with the charter (charter Art. 14).
