# Contributing to EMST

- **Work package:** WP-13 · **Author:** A10b (AS) · **Date:** 2026-10-23 · **Status:** draft for adoption with the governance charter v0.9
- **Builds:** governance charter Art. 6 (ADR-0009 §4), ADR-0003 (typing and naming), ADR-0007 (Tribal hold), ADR-0010 (IDs), ADR-0012 (no personal data), ADR-0013 (licensing), ADR-0015 (lifecycle), ADR-0021 (stored vs computed), ADR-0024 (evidence by use), ADR-0028 (signals); SPEC §4, §12, §13, §15, §18.4.
- **Licence of this guide:** CC BY 4.0. Contributions themselves are licensed as set out in §8.

Thank you for helping keep EMST accurate. EMST is an open standard: anyone can propose a change. Because federal, state and other employers build position descriptions, class specifications, training plans and assessments on it, changes follow a predictable process with published service levels. This guide tells you how.

> **Before Phase 4 closes** (expected with `2.0.0-rc.1`, Q1 2027), the Chief Taxonomy Architect (CA) decides change requests and disputes. After that the Editorial Board (EB) decides, with appeal to the Advisory Council Executive Group. Until those bodies are constituted, the project lead acts for them. <!-- PENDING Q8 -->
>
> **Task sequence v7 is retired** as the governance instrument. The ADRs in `docs/decisions/`, the decision log and this guide replace it. <!-- PENDING Q10: confirm retirement; default — the repo follows the ADRs and the companion project's descriptions are treated as v1 history. -->

---

## 1. Ways to contribute

| You want to… | Do this |
|---|---|
| Report a typo, broken link or wrong code | Open an issue with the **Errata (E)** template, or a pull request |
| Say a mapping to O*NET, SOC, ESCO, OPM series, a state class or CIP is wrong or missing | **Crosswalk (C)** template |
| Add or change a task, competency, indicator, knowledge statement, role profile or variant | **Substantive (S)** template |
| Propose retiring something | **Deprecate (D)** template |
| Change the schema, an L0 vocabulary, the level scale, ID rules or a computed-view rule | **Structural (X)** template |
| Anything touching Tribal governments, Tribal law or jurisdiction, consultation, Indigenous knowledge, cultural resources or Tribal data | **Tribal-related (T)** template — read §6 first |
| Report a change you see in your work (a new duty, tool, mandate, a role disappearing) | **Signal** template; it goes to the quarterly triage panel, not straight into content (§5) |
| Request a role EMST lacks | **Request a role** template (pilot and design-partner users have this in the explorer) |
| Report misuse of EMST (ranking, screening, RIF or adverse-action use) | **Misuse report** — routed to the Workforce Voice Panel channel and the Steward; it can pause expansion (CM metric M-11) |

## 2. What every change request must contain

1. **The problem and the proposed change**, in plain words.
2. **Affected IDs** (EMST IDs, or `seed:` keys for drafts) and related content. A new task must name its competencies and the role profiles it belongs to.
3. **Evidence, labelled** **[E]** (a source you read, with its ID or URL), **[J]** (your judgment and what it rests on) or **[S]** (speculation, with what would confirm or refute it).
4. **For S and X:** at least **two independent sources, including at least one demand signal** — a job posting, a position description, a plan requirement, a staffing plan — **or SME panel data**. Two indices built on the same data count as one source.
5. **Effect on adopters:** breaking or not; which use tier it affects (exploratory, describe, develop, select).
6. **Sector-actor variants or enactments** it implies, if the work is performed differently by federal, state, local, NGO, private or academic employers. (Tribal variants: see §6.)
7. **Conflict-of-interest disclosure** if you or your organization would gain directly (a vendor's mapping, a client's role profile, a society's credential crosswalk).

**Do not include** personal data (names of workers, applicants or raters; ratings of individuals), confidential documents, Tribal-confidential information, or third-party text you have no right to share (accreditor or credential-body text, licensed posting data, O*NET or ESCO text in CC0 files). Paraphrase and cite instead.

## 3. Writing rules your text must pass

These are checked by CI lint and by editors (SPEC §18.4; ADR-0003; ADR-0004; ADR-0016):

- **Name the work, not a programme or ideology.** Titles follow verb + object + context ("Analyze cumulative burdens and distributional effects of environmental decisions"). Programme names go in `altLabel` as search aliases.
- **No products or instruments in core text.** No named software, platform, model or vendor product (those live in L4 Tools), and no named statute, rule, order or programme (those live in the L5 instrument registry) in L1/L2 titles, descriptions or indicators.
- **Observable indicators.** Each indicator names an observable behaviour with a condition and a standard; years of experience are never a level; the indicator lint bans twelve constructions (e.g. "shapes understanding of…").
- **Descriptions ≤ 60 words.**
- **Store atoms, never summaries.** Do not type counts, modal values, blends, tiers, roll-ups or percentages into records or documents; CI computes them (ADR-0021).
- **No validation claims ahead of evidence.** Do not write "validated", "SME-agreed", "Delphi-retained" or "aligned with O*NET/OPM/ESCO" unless a recorded study or reviewed SSSOM mapping set supports it (ADR-0027 §3).
- **Corrected facts only.** Date-sensitive claims in kits and publications must match the corrected-facts list in ADR-0027 §3 and pass the WP-15 claims register.
- **Agent-assisted text** is labelled `method = llm-assisted` with tool and prompt versions, `validationStatus = draft` and evidence label S until a named human reviews it.

## 4. Stages and service levels

| Stage | What happens | Who | Time limit |
|---|---|---|---|
| **Proposal** | Issue or PR opened with a template; automated checks run (schema, lint, Tribal hold, personal data, third-party text) | proposer; CI | — |
| **Triage** | An editor assigns type, owner and priority; may reject as out of scope with written reasons (appealable to the EB) | Managing Editor or delegate | ≤ 30 days |
| **Candidate** | The drafted change is published for comment | EB (or module steward, v2.2+) | 30 days (minor) / 60 days (major or X) |
| **Adjudication** | Every comment is marked **Noted / Accepted / Accepted with modification / Deferred / Rejected**, with a reason | owner editor | ≤ 30 days after comment closes |
| **Decision** | EB (S, D), TSC (C, technical E), EB + TSC jointly (X); TAC consent first for T | per charter Art. 5 | next scheduled meeting |
| **Release** | Bundled into the next PATCH or April MINOR, or a MAJOR (charter Art. 7) | TSC and Steward | per cadence |

**Fast track:** E and C changes may go straight to the next PATCH after editor review. **T changes pause** until the TAC decides; while no TAC exists they are held (§6).

**Merging:** bots may open pull requests (e.g. upstream re-pins, signal digests); **only humans merge**. Every merged change gets a change record (`data/v2/changes/<release>.jsonl`) declaring its `semverImpact`; CI fails a release tag smaller than the largest declared impact (SPEC §12.5).

## 5. Signals are not changes

Sentinel reports, NLP drift reports, upstream releases (O*NET, ESCO, OPM issuances, SOC 2028) and policy events enter L5 as **signal records**, not as content edits. A signal moves a computed change indicator only under the evidence rule — two independent signal families, persistence, a close crosswalk match, a driver tag and named human review; otherwise it stays `watch` and appears in the "what's coming" view (ADR-0028 §2). The quarterly triage panel turns qualifying signals into change requests.

## 6. Tribal-related contributions

- **Nothing Tribal-related is published** until a Tribal Advisory Council constituted by Tribal governments and inter-Tribal organizations exists and approves it (ADR-0007 §D). T requests are logged at triage and held; they are not opened for public comment.
- **Never submit:** Indigenous knowledge content, sacred or cultural site locations, consultation records, material shared in confidence, characterizations or scores of named Tribes, Tribal employers' documents or postings, or person-level Tribal data. CI rejects some of these automatically; editors reject the rest.
- If you are a Tribal government, inter-Tribal organization or Tribal professional and wish to raise something with EMST, you will be able to do so through the Tribal Liaison once a TAC exists. Until then, please know that the project will not use anything you send in any release. See `tribal_gate_procedures.md`. <!-- PENDING Q1 -->

## 7. Decisions, records and appeals

- Decisions and rationale are published in `docs/decisions/` within 14 days.
- You may appeal a triage rejection to the EB, and an EB decision to the AC Executive Group within 30 days, on grounds of process, evidence, conflict of interest or new evidence (charter Art. 8). TAC decisions on Tribal-related content are not appealable.

## 8. Licensing of contributions

- **Inbound = outbound.** You license your contribution under the licence of the files you change (`LICENSING.md`): **CC0 1.0** for data, vocabularies, schema and the standard; **CC BY 4.0** for narrative publications; **Apache-2.0** for code. No copyright assignment.
- **Developer Certificate of Origin (DCO).** Sign off each commit (`Signed-off-by: Your Name <email>`), certifying you have the right to submit it under those terms. Federal employees' contributions made in their official capacity are U.S. government works.
- **Third-party material** keeps its own terms and goes, if at all, into `external/` with attribution; crosswalks carry external **IDs only**.
- **Tribal-contributed content** is never relicensed by EMST; it lives in a Tribally stewarded namespace under the contributor's chosen licence, with a withdrawal right, and only after TAC approval (ADR-0013 §6).

## 9. Conduct

Be accurate, cite what you read, label what you judge, and disagree in writing with reasons. Do not use EMST, or ask it to be used, to rank, screen or remove people. Respect participants' anonymity: no one is named in the repository without their explicit, revocable consent.
