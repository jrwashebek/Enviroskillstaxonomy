# ADR-0014: Rollout sequencing — NGO pilot for the tool, federal/state design-partner track for the artifacts, in parallel

- **Decision point:** DP-13 (rollout sequencing)
- **Status:** provisional-pending-verification — the timing windows rest on facts that verification corrected (see Context); the decision holds under the corrected facts, but dates are re-checked at each stage gate. The charter-sequence interpretation is flagged to the project lead (`questions_for_project_lead.md` Q5).
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** AS, CM, CP, FH, SL, IO, LC, FS, TN
- **Related:** ADR-0006 (role tiers), ADR-0009 (cadence), ADR-0023 (expansion gates G1/G2), ADR-0024 (use tiers), ADR-0027 (product); `PHASE4_BUILD_PLAN.md`

## Context

The charter says: "Rollout runs NGO pilot group, then federal and state agencies, then the whole sector including academia." AS proposes a federal and state **design-partner track in parallel** with the NGO pilot because three federal windows were reported to close on fixed dates (P-AS-01); CM's logic model independently requires federal and state "shadow users" in the pilot (CM A10). Verification corrected the windows:

| Claim as reported | Verified status (2026-10-23) |
|---|---|
| OPM consolidates 115 series, standards and PD templates through Sep 2027 | The Apr 24 2026 Phase One list is **proposed**; agency feedback was due May 11 2026; no final decision memo found [E: V1-10] |
| Natural Resources Management is a Tier 2 Chance-to-Compete group with full implementation by FY2028 | NRM is **Tier 2 with no Tier 2 date**; FY2028 is the governmentwide full-implementation target [E: V1-17] |
| Aligned wildland fire qualifications take effect Jan 2027 (NWCG and USWFS) | **USWFS–USFS** aligned federal qualification standards effective Jan 2027; **NWCG is not a party**; NWCG updated PMS 310-1 on Jan 23 2026 [E: V3-13] |
| Workforce Pell programs approved by state boards | Approved by **governors working with state workforce boards**, then ED review [E: V3-03] |
| AmeriCorps cuts of ~$400M | Largely reinstated in plaintiff jurisdictions by injunction; Sep 11 2026 settlement covers **FY2026 only**; stay to Feb 1 2027 [E: V1-05] |

## Decision

1. **Two tracks run in parallel from Stage 1 (2027):**
   - **Stage 1a — NGO pilot of the tool** (Mar 2027 – Feb 2028; G1 decision Mar 2028): 12 organizations (range 10–14) in two or three states matched to state design partners; the three corridors (ADR-0006); The Corps Network as anchor; describe/develop use only; AS pilot design and CM gate G1 verbatim (P-AS-11, P-CM-11).
   - **Stage 1b — federal and state design-partner track for artifacts** (Jan – Dec 2027): co-production, not deployment. Deliverables: the **0400 Kit** (competency models and PD language for 0401 and 0404 first, then 0460, 0408, 0486, 0028, with a task-level crosswalk from series *proposed* for realignment) offered to OPM; a **Job-Analysis Starter Pack** for one natural-resources series run by one agency talent team on 3–5 vacancies (P-AS-02, P-AS-03, P-FH-06); a **federal-to-state environmental crosswalk** validated with Pennsylvania (P-SL-08); state class-spec crosswalks with three contrasting state models (PA, TX, WA) plus one county environmental health department and one municipal utility (P-SL-09); a fire crosswalk keyed to the USWFS–USFS standards.
2. **The charter's sequence is interpreted, not overturned:** the *tool* is piloted with NGOs first; federal and state partners **co-produce artifacts** and act as shadow users. Nothing federal or state uses in selection is released before IO's selection-grade evidence for that function cluster (ADR-0024).
3. **Stage 2 (2028–29)** federal and state adoption follows gate G1; **Stage 3 (2029–31)** sector-wide including academia follows G2 (CM).
4. **First commitments to seek** (P-AS-04), re-dated against verified facts: a federal design-partner letter (USFS or DOI/USWFS, with OPM reviewing) by Feb 2027; three state forestry or environmental agencies via NASF/ECOS plus one workforce board by Apr 2027; The Corps Network as pilot anchor plus 11 pilot MOUs by Mar 2027; SAF plus two to four societies as founding consortium in parallel.
5. **Fast track limited to translation and crediting** (CM disagreement 6): the federal-to-state crosswalk and translation views may ship before any pathway *recommendation*, because they need no prediction.

## Rationale and evidence

- Federal HR is moving toward what EMST supplies whatever the exact dates: the Chance to Compete Act requires position-specific, job-analysis-based technical assessments; self-assessments may not rank candidates since 30 Sep 2025; in FY2025 91% of delegated-examining announcements relied only on self-report questionnaires; only 15% of agencies employ I-O psychologists [E: FH-023, FH-002, FH-017; V1-09]. Agencies will need technical job analyses for natural-resources series by the FY2028 target.
- OPM is building series-level competency models (FWCI) and issued its first competency-based standards for 2210 on 13 Apr 2026 [E: V1-11]; EMST can feed, not compete with, FWCI (P-FH-03).
- States are hiring displaced federal staff now: Pennsylvania counts federal experience as equivalent and reports 1,350 hires with federal experience by Aug 2026 [E: SL-031, SL-080].
- IO: the NGO pilot can calibrate instruments and support describe/develop uses; it cannot support selection or generalize to federal or state jobs (IO §6) — federal and state partners are needed in parallel for any validity evidence.

## Consequences

- Phase 4 must deliver a v2.0-beta and the 0400 Kit draft by Q1 2027 (`PHASE4_BUILD_PLAN.md`); if it slips, the NGO pilot start (Mar 2027) holds and the 0400 Kit slips, not the reverse (AS open Q7).
- CP's security packet and state readiness briefs must be ready before Stage 1b (AS issue).
- Collective-bargaining obligations on PD changes are anticipated: AFGE, NFFE, NTEU and PEER consulted on non-punitive use before pilots (FH issue).

## Dissent and trade-offs

- **Strict sequence** (literal charter) gives cleaner learning and less reputational risk with federal partners; **parallel** catches the policy windows and gets incumbent validation data (AS disagreement 1). Parallel chosen, framed as artifact co-production.
- **IO:** adopter-recruited panels risk bias; IO's composition rules apply (ADR-0009).
- **Condition:** if OPM finalizes a different consolidation, or NRM is re-tiered, the 0400 Kit contents are re-sequenced but the track continues.
