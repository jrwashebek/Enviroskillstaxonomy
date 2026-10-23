# ADR-0003: Entity typing rules and grain — what is a competency, a task, knowledge, a tool, an instrument or a credential

- **Decision point:** DP-3 (typing rules and target grain)
- **Status:** accepted
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** DC, FC, SC, IO, LC, DB, PS, FH, SL, FS, IA, DE
- **Related:** ADR-0001, ADR-0004, ADR-0016 (naming), ADR-0021 (entity catalogue), ADR-0022 (credentials), ADR-0025 (transversal layer)

## Context

v1's "competency" was five different kinds of thing: a body of knowledge (1.1.1), tool fluency (2.1.1, 2.5.3 naming Trello and Asana), a practice bound to named reporting standards (3.6.2), a qualification-gated practice close to a role (4.3.2 burn boss), an administrative function (5.5.2) and a professional disposition (D7) [E: audit §4.1]. Each kind changes at a different speed and is assessed differently. DC supplied a rule set (DC-R1–R5) rather than examples (P-DC-02); FC supplied a tools-versus-task-bundle test (FC §8 Q2); SC asked whether a competency may have no defining craft (P-SC-07); PS asked whether business practice belongs in the core (PS open Q1).

## Decision

### 1. Entity kinds (each a distinct record type with its own fields, cadence and assessment)

| Kind | Layer | What it is | Title form | Assessed by |
|---|---|---|---|---|
| **Practice competency** | L1 | A performed capability whose work product can be judged without knowing which tool produced it | verb + object (+ context) | indicators at levels (ADR-0004) |
| **Knowledge area** | L1 | A body of disciplinary knowledge several crafts draw on (most v1 D1 science items) | noun phrase | knowledge tests; linked knowledge statements |
| **Transversal practice** | L1 | Professional practice required across work functions and modules (ethics and integrity, human-AI practice, safety culture, formation of others…) with craft/actor/module **enactments** | verb + object | indicators; enactment-specific anchors |
| **Task** | L2 | Smallest unit of work with a meaningful outcome and clear start/end (DACUM) | imperative verb + object + condition/purpose | job-analysis ratings; task-book observation |
| **Knowledge statement** | L2 | A testable proposition a performance depends on; may be tagged Awareness (A) | declarative | knowledge checks |
| **Tool, method or technical standard** | L4 | Named product, platform, model, instrument class, protocol, technical standard or reporting framework | noun | practical check; never a proficiency level |
| **Instrument** (law, rule, policy, memo, court decision) | L5 registry | Dated legal or policy instrument with status; changes by public process | citation | n/a (referenced by sensitivity edges) |
| **Credential / qualification / licence** | reference entity linked from L2/L3, crosswalked in L6 | A gate conferred by an external body | issuer's name | record check; never stands in for proficiency |

### 2. Typing rules (apply to all three crafts)

- **T-1 = DC-R1 Substitution invariance.** A statement belongs in L1/L2 only if it stays true, performable and assessable when every named product, platform, model, library, format, vendor service and instrument is replaced by a functional equivalent. Otherwise the named thing goes to L4 or L5 and the statement is rewritten to the function.
- **T-2 = DC-R2 Judgment-bearing evidence.** L1 content is evidenced by a judgment-bearing work product. Content evidenced only by operating an interface is L4 fluency, however difficult.
- **T-3 = DC-R3 Half-life threshold.** Content with an expected useful life under two L1 review cycles (< 2 years) is L4/L5.
- **T-4 = DC-R4 Reference direction.** L4 and L5 point to L1/L2; L1/L2 text never names an L4 product or an L5 instrument. A task may name a **tool class** when the class changes the work condition itself ("validate AI detections", "supervise an automated aircraft").
- **T-5 = DC-R5 Promotion.** A tool class becomes an L1 competency only when its adoption creates a new judgment-bearing work product evidenced in ≥ 2 sector actors or ≥ 3 organizations; until then the candidate enters with lifecycle `proposed` (ADR-0015).
- **T-6 (FC test) Tools-layer vs task-bundle change.** A technology change is tools-layer if a proficient practitioner meets the *same anchors* after brief familiarization; it is a task-bundle change if the anchors change (FC §8 Q2). UAS flight near crews is a durable FC practice; the aircraft and photogrammetry software are L4.
- **T-7 Instrument vs tool.** If it has legal or policy force and changes by public process (statute, rule, EO, OMB memo, court decision, permit program) it is an **Instrument** in the L5 registry with dated driver events (ADR-0028). If practitioners choose it as a method or technical standard (ISO 19115, GHG Protocol, a reporting framework's technical standard) it is **L4**. This resolves DC (all policy instruments in L4) vs SC (instrument registry) by kind, not by preference.
- **T-8 Credentials are gates, not competencies.** HAZWOPER, red cards, PE/PG seals, operator grades, REHS registration and NWCG position qualifications are Credential records attached as `credential_gate` to tasks and role variants (ADR-0022). "Prescribed fire planning and execution" is a practice competency; "burn boss" is a qualification on a role.

### 3. Grain rules

- **G-1 Competency.** One assessable capability; links to ≥ 1 L2 task (≥ 3 recommended; ≥ 1 *critical* task for `use_class = select`); anchorable with 2–5 indicators at each level in its span; description ≤ 60 words; no fixed number per area.
- **G-2 Task.** One verb (no compound "develop and maintain"); object; condition or purpose; 8–30 words; no level grade (v1's T1/T2/T3 order becomes a legacy attribute only). Split **production** from **specification, review and defence** (P-FS-11) and **execution to protocol** from **adaptation in place** (FC §8 Q1) where both exist. Variable count per competency and role.
- **G-3 No fixed counts.** Retire "5 competencies per skill area" and "3 tasks per competency".
- **G-4 Core vs module (three-module rule).** A competency is **core** if the same task core is enacted in ≥ 3 modules and differs only in knowledge base or regulatory regime; otherwise it lives in the module that is its home, with enactments elsewhere (P-DB-09; boundary disputes resolved by ADR-0018's home-module rule). IO tests rater agreement on the rule in Phase 4.
- **G-5 Technology-neutral titles.** No competency title names a technology family (P-DC-03).
- **G-6 Actor-specific competencies only when the deliverable differs in kind** (a different legal duty or source of authority), not merely procedure (SC §8 Q1; ADR-0007).
- **G-7 "No defining craft" is allowed.** A task may carry no craft at weight 2; such tasks roll up as *general professional practice* in blends. General management and supervision stop inflating Statecraft (P-SC-07); the SC-primary test is the four-property deliverable test (ADR-0005).
- **G-8 Business and funding practice.** Add a small transversal cluster in the core — client and partner scope management, proposals and grant development, project delivery to budget/schedule/quality — written with environmental tasks and public enactments (COR, grants, cost recovery). Generic remainder is referenced from O*NET/ESCO, not authored (P-PS-03; resolves PS open Q1).
- **G-9 Size discipline.** Core target at v2.0: **120–180 competencies** (within the 100–250 range of hypotheses §2), with depth in modules; role profiles carry 15–40 tasks and 6–12 critical competencies (FH §9 Q1).

## Rationale and evidence

- DC-R1–R5 were tested against all 35 D2 competencies and tool-laden D3/D6 tasks; they separate content with 1–3-year half-lives (EO foundation models, domain AI tools, policy memos) from functions cited in plans for decades (ROS, NRV, FIA) [E: DC-001, DC-023, DC-025, DC-028, DC-031, DC-035].
- Comparable frameworks type the same way: ESCO (knowledge / skills / transversal), SFIA ("not a catalogue of tools"), ASC (core competencies / specialist tasks / technology tools), Singapore (TSC / CCS) [E: CA-016, CA-034, CA-036, CA-037].
- IO's four-layer proficiency architecture (indicators / knowledge elements / qualification gates / tools) requires exactly these kinds (P-IO-03).
- Licensed subsectors separate the ability to do a task from the right to do it (operator in responsible charge, PE seal, LSP opinion, SOI qualification) [J: DB-020, DB-031, DB-058]; PS: sign-off authority is "the hardest private hiring screen" (P-PS-02).

## Consequences

- 26 v1 D1 DC-primary science competencies become knowledge areas without a craft-primary tag (P-DC-12); their tasks keep craft weights.
- Seven v1 D2 tool competencies retire or move to L4 (P-DC-03; `v1_disposition.csv`).
- DE implements a lint for T-1/T-4 (product names in L1/L2 text, using DC's 53-entry L4 seed as a lexicon) and for IO's twelve banned indicator constructions (P-IO-04).

## Dissent and trade-offs

- **PS:** private postings *do* screen on named tools (EQuIS, HEC-RAS, AERMOD); role profiles must be able to query L4 (PS disagreement 4). Accepted: role variants carry `tools_commonly_required[]` links into L4, versioned separately.
- **DC vs SC on instruments:** resolved by T-7 (kind-based split). DC said either was acceptable "as long as L1 never cites an instrument by name".
- **FH:** hiring benchmarks need Section 7, Section 106 and NEPA specificity; statute-neutral titles with federal-specific tasks and anchors in the federal variant (FH disagreement 3) — adopted.
- **Trade-off named:** more L1 competencies for genuine durable practices (e.g. UAS operations near crews) versus understating real change; and more record kinds versus v1's single row.
