# ADR-0027: v2.0 product scope, display policy for uncertain values, claims hygiene and the sector-facing package

- **Decision point:** DP-26 (new; CA) — CP's MVP views; display of v1 values (CP open Q3); PD builder timing (CP open Q5); ACR ownership (CP open Q6); claims hygiene; the sector-facing package
- **Status:** accepted; **publication of any v1-derived figure** in sector-facing material is the project lead's decision (`questions_for_project_lead.md` Q7)
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** CP, AS, IO, LM, CM, FS, FH, SL, LC, DE, TN
- **Related:** ADR-0012 (tiers), ADR-0015 (use tiers), ADR-0023 (exploratory pathways), ADR-0024 (α gate)

## Context

The first user is a training or programme lead in an NGO pilot organization whose job "contains the state training officer's job, with different role variants" (CP §10). v1's Flourish story made claims ahead of evidence ("validated against OPM and O*NET classification systems"; "38% of competencies remain Human-Essential" against 21% of tasks; CLD counts stale) [E: CA-020, CP-004, CP-007]. IO: tags with α < .667 are not shown to users (ADR-0024). CP: show v1 exposure values at task level, labelled, never aggregated, with a "challenge this" route. Verification corrected a set of facts the team had been repeating (V1–V4).

## Decision

### 1. v2.0 product = the **Role Change & Development Planner** (P-CP-12) plus kits first

- **View 1 — "How is this role changing?"** (the Forester PD prototype, generated from data): role variant summary (≤ 60 words), task bundle with time share, work function and craft, attributed exposure assessments with tier, agreement and date, change signals with interval or n and coverage note, emerging items with lifecycle state, a descriptive (not normative) "stays human" rationale.
- **View 2 — "Where are the gaps?"** (local-first gap check): role–competency targets with criticality and served task IDs; CLOs at the target level; ratings live only in a client-side file (ADR-0012).
- **View 3 — "Where can this role lead?"** (**exploratory** until M-03 passes): computed pathway edges, directional coverage, friction records, dated crosswalk destinations; observed transitions only as aggregates (n ≥ 5).
- **View 4 — "What's coming"** (P-FS-13): watch items, proposed and emerging roles and competencies, signposts, the no-regret moves NR-1…NR-8 and contingent moves with triggers (answers FS open Q3 and Q8: published, clearly labelled, in v2.0).
- **Generated HR views:** Federal Series Profile and State Class View (ADR-0006).
- **Kits first when effort competes** (AS): downloadable version-pinned data; the 0400 Kit; the Job-Analysis Starter Pack; skills-gap template; state class-spec crosswalk; fire crosswalk; NGO templates; workforce-board sector kit; curriculum map; change notices.
- **PD skeleton export ships in v2.0; the full PD builder in v2.1** (answers CP open Q5); any redesigned PD is labelled "subject to classification review" and follows FES format (P-FH-09).
- Users enter by role and see 10–20 relevant competencies with depth one click down; the full model is downloadable (CP §10).

### 2. Display policy for uncertain values (answers CP open Q3)

- **v1 analyst exposure values are not shown in the default views.** They appear only in a task-level **evidence drawer** labelled "v1 single-analyst prior, LLM-assisted, unvalidated — not for decisions", with contested markers and a "challenge this" route, never aggregated, never in a headline number, and hidden entirely if comprehension testing fails. (This reconciles CP's proposal with IO's α rule: the drawer is evidence, not a tag shown as a value.)
- Until v2 multi-rater assessments exist for a task, View 1 shows "assessment pending" plus external capability exposure (aggregated Eloundou/AEI/Microsoft/BLS categories) labelled as external context with dispersion.
- Every number on screen traces to stored, attributed records in a tagged release and is computed at build time; every chart has a table, its message in text, no hover-only information and no colour-only encoding (CP uncertainty standard; USWDS).

### 3. Claims hygiene (P-CP-09, P-AS-14)

- Retire now: "validated against OPM and O*NET classification systems", "SAF-accredited competency standards", "38% Human-Essential", "68% in transition", and every stale v1 count (215, 222, 292 competencies; "9 S calls"; "FC/DC structural property").
- **Every public number carries its evidence tier and denominator** (v1 analyst / panel-validated / externally benchmarked; n; date).
- No claim of O*NET, ESCO, OPM or state alignment until a reviewed SSSOM set exists (ADR-0022).
- **Corrected facts to use (V1–V4, 2026-10-23):** OPM's Apr 24 2026 series list is *proposed* for realignment; Natural Resources Management is Chance-to-Compete Tier 2 with no Tier 2 date (FY2028 is the governmentwide target); ~317k 2025 federal departures is OPM's tally (PPS counts 386,826 separations Jan 2025–Jan 2026; net workforce drop ~278k, 12%); AmeriCorps' ~$400M terminations were largely reinstated in plaintiff jurisdictions and the Sep 2026 settlement covers FY2026 only; the −29.4% conservation-postings figure is one job board; EPA's 30.3-year median service applies to ~2,000 year-end-2025 departures; ABC is now Water Professionals International; no active environment-sector-wide workforce/AI coalition exists; Jan 2027 fire standards align USWFS and USFS qualifications (NWCG not a party); Workforce Pell programmes are approved by governors with state boards, and H.R. 8210 has only cleared committee; GBCI (not USGBC) issues LEED AP and ISSP credentials; IEMA is now ISEP; ISO 14001:2026 superseded 2015; ESCO is v1.2.1 (the "27 languages" figure is outdated; the portal lists 28 — recheck before publishing); M-26-04 is dated Dec 11 2025; CEQ's NEPA regulations were removed effective Jan 8 2026; the SPEED Act passed the House and is pending in Senate EPW; PNNL's "1–5 hours saved per EIS subsection" is not confirmed and must not be published; BLS 2025–35 projections (Aug 27 2026) are current.

### 4. Accessibility and security as release gates

WCAG 2.2 AA (a superset of Section 508's WCAG 2.0 AA and the WCAG 2.1 AA required by ADA Title II, whose deadlines moved to Apr 26 2027 / Apr 26 2028 [E: V2-11]); an ACR per major release, **signed by CP during Phase 4 and by the Steward thereafter** (answers CP open Q6); security packet with every release (applicability statement, SBOM, SSDF mapping, Scorecard ≥ 7, SHA-pinned Actions, signed releases).

### 5. The sector-facing package (Phase 4 deliverables)

- **Flagship report "How environmental jobs are changing" (CC BY 4.0):** built from verified external evidence (LM, FS, FC, DC, SC, DB, PS, SL, TN syntheses), v2 structural findings and pre-registered pilot plans; every figure tier-labelled; v1 single-analyst statistics appear only as methodology history unless the project lead decides otherwise; the career-ladder finding is presented as a hypothesis with its mechanism and evidence status, co-published with a nonpartisan partner only after IO and LM validation (P-AS-14).
- **Briefing deck** for federal, state and NGO audiences (mandate-framed: merit, skills-based hiring, mission readiness, knowledge retention).
- **Interactive explorer** = CP's Tier 1 static site with Views 1–4 for the P1 corridor roles.
- **Role-change briefs** (two pages each) for the 13 corridor roles and the Forester PD regenerated in FES format.

## Dissent and trade-offs

- **CP** wanted v1 values visible at task level by default; moved into an evidence drawer to satisfy IO's rule and avoid repeating Flourish's mistake. Trade-off: less "insight" on day one, more credibility with federal adopters.
- **AS vs CP:** kits before interactive views when they compete — adopted (AS disagreement 5).
- **FS:** publishing the "what's coming" view risks speculation in front of HR users; contained by labelling and use-tier filtering.
