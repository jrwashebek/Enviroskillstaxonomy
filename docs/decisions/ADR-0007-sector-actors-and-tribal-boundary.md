# ADR-0007: Sector actors, structured enactments, and the Tribal boundary

- **Decision point:** DP-7 (sector-actor representation and the Tribal protocol boundary)
- **Status:** accepted for the model, the five vetoes and the content hold. The binding Tribal Advisory Council (TAC) authority, the charter carve-out and reviewer compensation were **accepted by the project lead (Q1, 2026-10-23)**. **Needs-project-lead** for any invitation to help form the TAC (Q11). **Needs-real-consultation** for every item of Tribal-related content.
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** TN, SC, SL, PS, DB, FH, CM, CP, DE, IA, LM, AS, FC
- **Related:** ADR-0006, ADR-0012 (no personal data), ADR-0013 (licensing carve-out), ADR-0016 (DEI/EJ containers), ADR-0017 (authority position), `vocab/sector_actors.yaml`

## Context

v1's five free-text sector notes (Public Agencies, Private Sector, NGOs, Consulting, Academia) merge federal, state, local and Tribal into one column, treat consulting as an actor, omit Tribal nations, and are illustrative settings rather than statements of how work is enacted differently [E: audit §7; SL-087: of 222 "Public Agencies" notes, 13 match state terms, 10 local, 167 none]. TN holds a design veto over knowledge or data that is not the project's to include (charter). TN is a **simulated voice**; nothing it drafted speaks for any nation.

## Decision

### A. Sector actors (L0)

1. **Seven sector actors** — `federal | state | local | tribal | ngo | private | academic` — with subtypes in `vocab/sector_actors.yaml`. Tribal subtypes follow P-TN-01: federally recognized Tribe; inter-Tribal organization or consortium; Tribal college or university; Tribal enterprise; ANCSA corporation (distinct legal category); Native Hawaiian organization (distinct status); state-recognized Tribe (distinct status). Local subtypes: county, municipality, special district, regional authority, conservation district, local health department.
2. **Industry, ownership and delivery model are facets orthogonal to sector actor** (P-PS-01). "Utility" and "consulting" are *not* sector-actor subtypes (correcting CA audit §7): a utility may be municipal, a special district, investor-owned, cooperative or Tribal; consultants work for every actor. Ownership ∈ {public, investor-owned, cooperative, nonprofit, tribal}; delivery model ∈ {in-house, contracted, independent-third-party}.
3. **Sector actor attaches to employment context** — role variants, enactment records, friction records, signals — never to a competency as a tag.

### B. Enactments and actor-specific competencies

4. **Default: one competency, structured enactments by actor** (P-SC-04). An `Enactment` record carries `actor_type`, `authority_basis`, `principal`, `accountability_venue`, `characteristic_instruments[]` (L5 instrument IDs), `typical_frictions[]`, optional extra tasks or indicator variants, and provenance. Enactments are written only where the actor changes the performance.
5. **Actor-specific competencies only when the deliverable differs in kind** (a different legal duty or source of authority). Four such competencies are authorized: (1) exercising Tribal sovereignty in a Tribal government's own programs — **TN-owned, written or approved only by Tribal authority**; (2) the duty-holder side of government-to-government consultation (federal and state); (3) operating or overseeing delegated and assumed regulatory programs (state and Tribal); (4) regulated-entity compliance across divergent regimes (private).
6. **Obligations owed to Tribal nations are core Statecraft content for every actor, not enactment notes** (TN §8 Q1 point 3; P-TN-05). TN-C01–TN-C12 (trust responsibility and treaty rights, G2G consultation, confidential information, agreements, Tribal jurisdiction, partner conduct in Tribally led fire, Tribal data governance, funding that respects self-governance, Indian preference, engaging Indigenous knowledge only on holders' terms, THPO coordination, sustaining obligations when procedures change) enter the core candidate pool **under the content hold below**.
7. **Jurisdictional-context facet** (categorical only): trust or Tribal lands; treaty-reserved-rights areas; co-managed areas. It must never become a geographic layer of Tribal places. **Tribal law and compact standards are representable as an authority that overrides EMST default qualification statements on Tribal lands** (TN §8 Q1 point 1).

### C. The Tribal boundary — five architecture invariants (TN's vetoes, adopted)

| # | EMST must not… | Enforcement |
|---|---|---|
| V1 | define, describe, rank or credential Indigenous knowledge (no competency, level, indicator, task or exposure score may describe the content of a nation's knowledge or grade "expertise in TEK") | content review gate; lint list; retires v1 5.3.2 ladder and the v1 fire report's recommendation to credential Indigenous fire stewardship |
| V2 | hold confidential Tribal information (site locations, consultation content, material shared in confidence) — even under access control | CI fails on confidential records anywhere in the repo and on coordinates co-occurring with cultural-site vocabulary (P-TN-02) |
| V3 | publish characterizations of named Tribes without consent (rankings, capacity, readiness or maturity scores, Tribe-level change indicators) | schema forbids Tribe-identified computed indicators |
| V4 | ingest Tribal employers' documents or postings by default, including in LLM pipelines | IA pipeline quarantine; `tribal_programs` flag; no training on Tribal documents (P-TN-10) |
| V5 | create a "Tribal Natural Resource Management" profession family | Tribal differences live in sector actor, jurisdiction and variants |

The taxonomy states on its face that Indigenous knowledge is a distinct body of environmental expertise held and governed by Indigenous nations and is **out of scope by design**, and it points to Tribally controlled resources where Tribes provide them (TN disagreement 8 mitigation).

### D. The content hold (interim rule)

8. **Until a Tribal Advisory Council constituted by Tribal governments and inter-Tribal organizations exists and approves, nothing Tribal-related is published.** This covers: the successor to v1 7.1.1 (TN-C07); every L2 ethical-lens definition and tag; TN-C01–TN-C13; SC-C13; Tribal role variants (drafts may exist internally, marked `approval_status = pending-tribal-review`, never released); Tribal-flagged change signals; TN's role signals; the Tribal engagement protocol and Indigenous data governance policy (both AI-drafted). Internal multi-rater analytical tagging is allowed (it is analysis, not taking Indigenous content).
9. **Schema fields from day one:** `indigenous_data_flag`, `sensitivity`, `approval_status`, `ai_use_permitted`, `governed_data` (P-TN-02, P-TN-09); a reserved **Tribally stewarded namespace** (`emst:tribal-<steward>/…`) with contributor-chosen licence and withdrawal right (P-TN-11).
10. **Recommendation to the project lead:** constitute the TAC with **binding consent authority** over inclusion, wording and release of Tribal-related content, and amend the charter so the CA's dispute-resolution authority does not override the TAC in that category (default = withhold) (P-TN-03; AS governance charter). Budget compensation for Tribal reviewers before first contact; if it cannot be funded, the pilot proceeds with the gate closed and no Tribal outreach (TN open Q5).

## Rationale and evidence

- Interior policy says Indigenous knowledge must be "generally considered authoritative by the Indigenous Peoples who possess it" and that agencies should rely on Indigenous Peoples to interpret it [E: TN-018 §7.5, §7.6.A(5)]; staff are warned not to overstate what FOIA lets agencies protect [E: TN-018 §7.6.A(1)(b)]. An open, forkable, agency-hosted taxonomy cannot protect what it holds; not holding it is the only protection that works (V2).
- Tribal status is political, not demographic; placing Tribal relations beside DEI exposed Tribal programs to anti-DEI cuts agency by agency in 2025–26 [E: TN-029, TN-032] — hence ADR-0016's container rule.
- Statecraft transfer evidence: negotiation, engagement design, record integrity, drafting and durability judgment transfer across actors; authority basis, principals, sovereignty and delegated-program constraints do not (SC §3.2) — the enactment fields carry exactly the non-transferable parts so frictions can be computed.
- PS: consulting plus architectural/engineering services employ ~34% of environmental scientists, more than state government [E: PS-014]; private context must attach to every function, not to two families.

## Consequences

- The Tribal workforce will be under-measured; v1 already notes it is invisible in federal series data [E: TN-050]. The response is analyses Tribes commission and control, not quiet ingestion; every sector-wide statistic EMST publishes carries that caveat.
- TN-C13 and Tribal-employer role variants (Tribal environmental director, Tribal forester, Tribal FMO, THPO) exist only as pending internal drafts from public program documents (P-TN-14).
- Alaska Native and Native Hawaiian contexts get separate subtypes, enactment notes and reviewers (P-TN-17).

## Dissent and trade-offs

- **CA's own hypothesis** ("sector actor is context, not content") is amended: for obligations owed to Tribal nations it is content. **Trade-off:** a larger core versus HR and training views that actually show trust and treaty obligations (TN disagreement 2).
- **LM and IA completeness goals** lose Tribal postings; TN accepts the measurement gap and so does the CA.
- **IO and CM timelines:** Tribal research approvals slow any Delphi including Tribal professionals; run the federal/state Delphi on schedule and the Tribal track on Tribal time (TN disagreement 6).
- **Simulated-voice limit:** this ADR adopts TN's vetoes as invariants because they reduce harm in every case; it does not and cannot ratify any Tribal content.

## Amendments

- **2026-10-23 — Project lead decision Q1 (recorded by CA).** The project lead accepted §D.10 in full:
  - (a) binding consent authority for the TAC over the inclusion, wording and release of Tribal-related content;
  - (b) a charter carve-out so the CA (later the Editorial Board) cannot override the TAC in that category, with "withhold" as the default;
  - (c) Tribal reviewer compensation budgeted before first contact.

  The §D content hold stays in force until a Council constituted by Tribal governments and inter-Tribal organizations exists and approves (`PROJECT_LEAD_DECISIONS.md`).
- **2026-10-23 — Forming the Council is not EMST's to do; inviting help is the project lead's question (CA; Q11).** Under Q1 the Council is constituted by Tribal governments and inter-Tribal organizations, not by EMST. A **lead-signed invitation to inter-Tribal organizations to help *form* a Tribal Advisory Council** would be the project's first contact with organizations of sovereign governments. It would also commit the Q1(c) compensation budget. It is therefore a question for the project lead (`questions_for_project_lead.md` Q11), not a build task.
  - **Default until answered:** no invitation is drafted for sending and no contact is made.
  - **WP-13:** it may describe a formation procedure only as an internal document marked "for the project lead; not for distribution".
  - **Agents:** no agent, including the TN role, drafts outreach as if it spoke for or to any nation.
- **2026-10-23 — CR-LM-001 / ADR-0029 §8 (CA).** Two applications of V3:
  - Change signals may target a government organization by official code, but never a Tribal government, Tribal organization or Tribal enterprise; CI rejects it.
  - The Tribal co-stewardship signpost (SP-12) is readable only through the Tribal Council.
