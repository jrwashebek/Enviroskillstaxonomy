# Questions for the project lead

- **From:** CA (Chief Taxonomy Architect), Phase 3 · **Date:** 2026-10-23
- **Scope:** only decisions that belong to the project lead: ownership of the v1 work, authority over governance bodies and the charter, commitments made on the project's behalf, money, and public positions. Everything else is decided in ADR-0001 … ADR-0028.
- **How to answer:** a one-line reply per question is enough ("accept", "accept with change …", or "decline"). Each question states the **default** the build follows if no answer arrives by its date, so Phase 4 is never blocked.
- Question numbers are stable because ADRs cite them (Q2 in ADR-0013, Q4 in ADR-0016, Q5 in ADR-0014, Q6 in ADR-0023, Q7 in ADR-0027).

---

## Q1. Tribal Advisory Council: consent authority, the charter carve-out and reviewer compensation

- **Decision needed:** (a) Will the Tribal Advisory Council (TAC), once constituted by Tribal governments and inter-Tribal organizations, hold **binding consent authority** over the inclusion, wording and release of Tribal-related content? (b) Will the charter be amended so the CA's (later the Editorial Board's) dispute-resolution authority **cannot override** the TAC in that category, with "withhold" as the default? (c) Will compensation for Tribal reviewers be budgeted **before** first contact?
- **Why it is yours:** it changes the charter's allocation of authority and commits money and the project's relationship with sovereign governments. No simulated role can decide it, and the TN role cannot speak for any nation.
- **Recommendation:** accept all three. This is the only arrangement consistent with CARE and with Interior's own statement that Indigenous knowledge is authoritative as held by the peoples who possess it (ADR-0007, P-TN-03).
- **Default if unanswered:** the content hold in ADR-0007 §D stays in force indefinitely; no Tribal outreach takes place; TN-C01–C13, SC-C13, the v1 5.3.2, 6.5.1 and 7.1.1 successors, Tribal variants and Tribal signals remain internal drafts excluded from every release.
- **Needed by:** before any Tribal outreach, and before WP-13 finalizes the governance charter (Phase 4 sprint S3).

## Q2. CC0 dedication of the v1-derived content

- **Decision needed:** will you dedicate, in writing, the v1 text you authored (competency titles, descriptions, tasks, indicators and source text) to the public domain under CC0 1.0, so v2 records derived from it can ship in the CC0 data files?
- **Why it is yours:** v1 is your own work; only the rights holder can dedicate it (ADR-0013; DE caveat 3).
- **Recommendation:** accept. CC0 for data and the standard's text, CC BY 4.0 for narrative publications and Apache-2.0 for code is the licensing set that lets agencies, HR systems and platforms adopt EMST without attribution chains in records (ADR-0013). AS's dissent in favour of CC BY for content is recorded there.
- **Default if unanswered:** rc.1 ships with v1-derived text **excluded** from the CC0 data files (IDs, structure and crosswalks only), and v1 wording stays in `legacy/` under its current terms. That makes rc.1 far less usable.
- **Needed by:** before WP-16 builds 2.0.0-rc.1 (sprint S4).

## Q3. Host, incubation and who signs for the project

- **Decision needed:** (a) Does EPIC incubate EMST through December 2027 and remain a founding partner? (b) Do you approve an open call in Q2 2027 for a university-based EMST Stewardship Center to operate the programme from January 2028, governed by an independent EMST Consortium? (c) Until a host exists, who signs pilot MOUs, data agreements and design-partner letters: you or EPIC?
- **Why it is yours:** these are institutional commitments made on the project's behalf (ADR-0009 §8).
- **Recommendation:** (a) yes, if EPIC confirms; (b) yes; (c) EPIC signs if it has confirmed incubation, otherwise you sign as project lead, with every commitment entered in the commitment register (P-AS-15).
- **Default if unanswered:** you are listed as signatory for Stage 1 documents; the host call is drafted but not issued.
- **Needed by:** February 2027 (first federal design-partner letter and pilot MOUs, ADR-0014 §4).

## Q4. Publication stance for DEI- and EJ-labelled content in federal default views

- **Decision needed:** confirm the publication stance in ADR-0016: content stays in the core where it meets the evidence standard; every competency is named by the work performed (programme labels become search aliases); and **federal default views exclude items whose only basis is a rescinded or inactive federal instrument**, computed from the instrument registry, while state, local, NGO and private views keep them where their own instruments apply.
- **Why it is yours:** it is the project's public position on a contested federal policy question, and it determines what federal design partners see first.
- **Recommendation:** accept. It treats every item under one rule, keeps content adoptable by federal partners without deleting it, and reverses automatically if instruments change in either direction.
- **Default if unanswered:** the mechanism is built (it is accepted); federal default views show computed applicability with an explanatory note and no exclusions until you confirm.
- **Needed by:** before WP-12 renders federal default views (sprint S2).

## Q5. Interpreting the charter's rollout sequence

- **Decision needed:** approve running two tracks in parallel from 2027: **Stage 1a**, an NGO pilot of the tool (March 2027 – February 2028, gate G1 in March 2028), and **Stage 1b**, a federal and state design-partner track that co-produces artifacts (0400 Kit, Job-Analysis Starter Pack, federal-to-state crosswalk) and acts as shadow users, with nothing used in selection before IO's selection-grade evidence (ADR-0014).
- **Why it is yours:** the charter sets the sequence; this interprets it, and you own the charter.
- **Recommendation:** accept. Federal and state classification and hiring timelines (OPM's series realignment is still only proposed; Natural Resources Management is Chance to Compete Tier 2 with no Tier 2 date [E: V1]) mean that waiting for an NGO pilot to finish before engaging them would miss the window in which their artifacts are being rewritten.
- **Default if unanswered:** Stage 1b is limited to informal shadow review with no co-produced artifacts until you answer.
- **Needed by:** February 2027.

## Q6. The restated theory of change as the operating version

- **Decision needed:** adopt CM's restated theory of change — mobility follows when skills are embedded **in the instruments that gate movement** (job analyses, crediting plans, class specifications, qualification standards) and frictions are reduced on demand-backed pathways — as the operating version, keeping the charter sentence ("if those blends are visible and portable, mobility follows") as the north star (ADR-0023).
- **Why it is yours:** it changes what the project promises funders and partners and how success is measured (CM gates G1 and G2).
- **Recommendation:** accept. The published evidence shows visibility alone rarely moves hiring (e.g. only 37% of firms announcing skills-based hiring followed through; Colorado rewrote about 80% of classifications yet non-degree hires stayed near 25%) [E: CM-011, CM-012, CM-014, CM-050].
- **Default if unanswered:** the build uses the restated version internally; external documents quote the charter sentence only.
- **Needed by:** before WP-13 and WP-14 publish (sprint S3).

## Q7. Publishing v1-derived figures in sector-facing material

- **Decision needed:** may sector-facing publications (flagship report, briefing deck, explorer) cite v1 statistics, such as v1 exposure, craft or observability distributions?
- **Why it is yours:** the figures are products of your v1 analysis, and publishing them is a public claim on the project's behalf.
- **Recommendation:** cite them **only as methodology history** until they are re-derived under the v2 instrument with multiple raters; v1 observability figures may be cited as findings only after human double-coding with α ≥ .80 (ADR-0024 §11, ADR-0027). v1 values were assigned by a single analyst with LLM assistance, often to different text from the competency they describe (data audit).
- **Default if unanswered:** methodology history only.
- **Needed by:** before WP-14 drafts the flagship report (sprint S3).

## Q8. Constituting the governance bodies at release candidate

- **Decision needed:** which bodies exist at 2.0.0-rc.1, and who sits on them? Proposed: an interim **Editorial Board** and **Technical Steering Committee** named at rc.1, taking over dispute resolution from the CA when Phase 4 ends (charter Art. 4.5); the **Advisory Council** and **Validation Panels** constituted by gate G1; **Module Stewards** only after a signed Module Stewardship Agreement and two on-time review cycles (ADR-0009, ADR-0018).
- **Why it is yours:** appointments and the adoption of the governance charter are yours (ADR-0009 status: needs project lead).
- **Recommendation:** accept, adopting the governance charter as version 0.9 with a one-year review.
- **Default if unanswered:** you act as interim Editorial Board; the CA's decision log continues; no module is described as stewarded.
- **Needed by:** before WP-16 (sprint S4).

## Q9. Funding the floor and the people the evidence depends on

- **Decision needed:** will the project seek funding, before Stage 1 outreach, for (a) the published maintenance floor (about 3 FTE, about $0.62M a year, ADR-0009 §7), (b) compensation for sentinels (60–90, stratified), Delphi and job-analysis panel members, and Tribal reviewers (Q1), and (c) a philanthropic ask for the Stage 1 pilot and the first job-analysis clusters?
- **Why it is yours:** these are financial commitments and fundraising positions.
- **Recommendation:** secure the year-one floor and the compensation lines before inviting people. IO's composition correction depends on removing participation costs for thinned public field and statecraft strata (ADR-0024 §7); unpaid panels would reproduce the contraction bias the design is meant to correct.
- **Default if unanswered:** the degradation ladder applies: the sentinel network starts at the year-five floor of 30, panels are smaller and reported as such, and Tribal outreach does not start.
- **Needed by:** January 2027.

## Q10. Retiring task sequence v7 and updating the companion projects

- **Decision needed:** (a) confirm that task sequence v7 retires as the governance instrument (ADR-0020) and that the decision log, the ADRs and the Phase 4 build plan replace it; (b) update the working instructions you maintain for this work and for the companion research project, which still describe the taxonomy as "222 + n competencies across 7 domains, 45 skill areas" and direct work to "follow the most current Task Sequence document". Under ADR-0002 the domains and skill areas become a legacy facet and counts are generated by work function, module and lifecycle.
- **Why it is yours:** you own those instructions and the companion project; the v2 structure changes how both describe the taxonomy.
- **Recommendation:** accept. Cite v1 counts as "v1 (2026-02-23)" history; point current counts to the generated release notes; carry ADR-0002, ADR-0003, ADR-0011 and the DECISION_LOG into the companion research project so its literature and the build stay consistent.
- **Default if unanswered:** the repo follows the ADRs; the companion project's descriptions are left as v1 history and flagged as out of date.
- **Needed by:** before WP-14 publishes (sprint S3).

## Q11. A lead-signed invitation to inter-Tribal organizations to help form a Tribal Advisory Council

- **Added:** 2026-10-23 by the CA (Phase 4), after Q1 was accepted (ADR-0007 amendments)
- **Decision needed:** will you sign and send an invitation to inter-Tribal organizations, asking whether they wish to help **form** a Tribal Advisory Council? Forming it means deciding for themselves whether a Council should exist, who constitutes it, and its charter and terms. If yes, when, and to which organizations?
- **Why it is yours:**
  - It would be EMST's first contact with organizations of sovereign governments.
  - Under Q1 the Council holds binding consent authority, and Tribal governments and inter-Tribal organizations constitute it, not EMST.
  - Sending it commits the project's relationship and, under Q1(c), money: compensation must be budgeted before first contact.
  - Q3 (who signs) and Q9 (funding) bear on it.
  - No agent and no simulated role, TN included, can decide this, or draft the invitation as if speaking for or to any nation.
- **Recommendation:** yes, but send it only once three conditions hold:
  1. the compensation line for Council members and Tribal reviewers is secured (Q1(c), Q9(b));
  2. the signatory is settled (Q3(c));
  3. a person you choose who has Tribal-relations experience reviews the text before it is sent (not an agent).

  The invitation should:
  - ask for help forming the Council, not for review of EMST drafts;
  - attach no Tribal-related EMST content;
  - state the Q1 commitments: binding consent, the charter carve-out with "withhold" as default, the withdrawal right and Tribally stewarded namespaces;
  - say that whether, when and how to participate is entirely theirs, including declining;
  - set no deadline tied to EMST's release schedule (Tribal time, ADR-0007 dissent);
  - promise nothing about content that only the Council can decide.
- **Default if unanswered:**
  - No invitation is drafted for sending, and no contact is made.
  - The ADR-0007 §D content hold stays in force, and Tribal-related records remain internal drafts excluded from every release.
  - WP-13 may describe a formation procedure only as an internal document marked "for the project lead; not for distribution".
- **Needed by:** before WP-13 finalizes the governance charter (sprint S3), and in any case not before the compensation line is secured.
