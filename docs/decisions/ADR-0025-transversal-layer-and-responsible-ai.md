# ADR-0025: The transversal practice layer, Domain 7, and the three-layer split of responsible-AI content

- **Decision point:** DP-24 (new; CA) — what is transversal; ownership of AI validation and supervision (SC open Q5, DC open Q6); Domain 7
- **Status:** accepted (7.1.1 successor held under ADR-0007)
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** DC, SC, FC, IO, LC, PS, SL, FS, FH, CM, TN, LM
- **Related:** ADR-0003 (transversal type), ADR-0004 (augmented practice attribute), ADR-0024 (IO candidates)

## Context

Domain 7 was created to hold capacities that apply across all subject domains; putting cross-cutting practice into a "domain" is a category error [E: audit §13]. The source text holds domain-level cross-cutting competencies the database dropped (safety consciousness, systems thinking, stakeholder engagement…) [E: CA-006]. DC: responsible AI is **both** transversal and Datacraft, in three layers (DC §10.2). SC: DC owns general AI-output validation; SC owns legal adequacy and provenance in the record — or one transversal competency with enactments, provided the legal-adequacy anchors survive (SC disagreement 5). LC: D7.2 is the best v1 content for learning and should be the writing model (LC §1.2). CM: D7 transversal competencies are the strongest cross-family bridges, though partly built in by tagging (CM).

## Decision

### 1. The transversal practice layer (core; type `transversal`; required of roles by function, with enactments)

| Cluster | Competencies (successors; candidate merges) | Floor |
|---|---|---|
| **TX-A Data and AI practice (universal floor)** | Interpret and question environmental data products (DC-CAND-01); Use AI tools responsibly in everyday work (DC-CAND-02); **Validate AI-generated work products before professional use** (DC-CAND-13 + FS-C01 + v1 7.2.1 + FH-C15) with **FC, DC and SC enactments**; Calibrate trust in AI and automation (v1 7.2.3); Record provenance and AI involvement in work products (DC-CAND-05 at L1) | **every role profile carries L1** on DC-CAND-01 and -02 and on AI-output validation (P-DC-05) |
| **TX-B Professional integrity and accountability** | Authorize interventions with legitimate standing (v1 7.1.2); Maintain regulatory and scientific integrity (v1 7.1.3); Maintain independence and manage conflicts across the regulator–regulated boundary (PS-C18); Practise within licensure scope and responsible charge, incl. certifying AI-drafted deliverables under professional liability (SL-C16 + PS-C20) | by role |
| **TX-C Safety culture** | Apply safety practices and stop-work authority across field, facility and incident settings (split from v1 4.4.1; field risk management stays an FC practice competency) | field and facility roles |
| **TX-D Formation of others and knowledge continuity** | Design developmental experiences that preserve the learning substrate, incl. AI-augmented apprenticeships (v1 7.2.2 + FH-C06 + FS-C13 + LC-C-01); Evaluate and certify others' task performance against position standards (IO-C01 + LC-C-02); Elicit, document and transfer tacit and institutional knowledge before people leave (IO-C03 + FH-C07 + FS-C12 + CC-CM-01 + C-LM-05) | supervisors and senior levels (ADR-0004 formation attribute) |
| **TX-E Systems and collaboration** | Systems thinking across ecological, institutional and technical systems (v1 D6 cross-cutting); Communicate environmental risk under uncertainty (DB-C29) | by role |
| **TX-F Professional services and funding practice** | Manage client and partner scope; Develop proposals and grant applications; Deliver projects to budget, schedule and quality (PS-C01–C03 merged to three, with public enactments: COR, grants, cost recovery) (ADR-0003 G-8) | by role |

### 2. Responsible-AI content in three layers (DC §10.2, adopted)

1. **Transversal floor** — TX-A above.
2. **Data Craft specialist competencies** (where the methods live): design human-in-the-loop review (DC-CAND-14); build task-specific evaluation sets and benchmark AI tools (DC-CAND-15, merged with FS-C17); analyze regulatory, plan and comment text with LLMs with traceable citations (DC-CAND-16); supervise agentic AI workflows (DC-CAND-17, lifecycle `proposed`, [S]); assess and manage model risk for consequential decisions (DC-CAND-19 + FS-C02); specify, evaluate and accept AI and analytics services in procurement, protecting public data rights (DC-CAND-20 + FS-C10); govern enterprise data and AI portfolios (DC-CAND-21).
3. **Craft enactments** on the floor: **FC** = ecological plausibility and field ground truth; **DC** = sampling design and error estimation for validation at volume; **SC** = legal sufficiency, uniqueness and response sufficiency, AI provenance in the administrative record, authorization of the oversight design (v1 7.1.4's authorization part).

**Ownership (answers SC open Q5 and DC open Q6):** SC-C05 ("supervise AI-assisted drafting and public-comment analysis for legal defensibility") merges into the SC enactment of the validation floor **and** into SC-C02 (defensible administrative record, absorbing FS-C03's AI-provenance content); its **legal-adequacy anchors survive** as SC-enactment indicators. DC is steward of record for the technical content of responsible-AI anchors; SC co-owns authorization; IO validates.

### 3. Domain 7 dispositions

7.1.1 Indigenous data sovereignty → successor TN-C07, **hold-for-tribal-review**; 7.1.2, 7.1.3 → TX-B; 7.1.4 AI governance → split (authorization → SC; risk tiering → DC-CAND-19; oversight design → DC-CAND-14) with DC secondary (P-DC-15); 7.2.1 → TX-A validation; 7.2.2 → TX-D; 7.2.3 → TX-A. D7 exposure is re-assessed descriptively (its all-H calls were normative).

### 4. Not transversal

Horizon scanning (FS-C15) is a core **practice** competency in a strategy cluster (span L3–L5), not a floor requirement (answers FS open Q4). Negotiation, engagement design and drafting are core Statecraft practice competencies with actor enactments (ADR-0007), not transversal, because their performance standards are craft-specific.

## Rationale

- The people verifying deployed environmental AI are comment analysts, planners and permit staff, not data scientists (FWS DocketScope "verified by analysts"; USDA permitting AI "only recommendations for authorized staff to review") [E: DC-001]; DOL frames AI literacy for the whole public workforce [E: DC-015] — hence a floor. Whether human review is substantive is the hinge of federal AI compliance (M-25-21 "principal basis") [E: DC-001, DC-007] — hence DC specialist content.
- SAF's integrative components (C4-5 to C4-9) and ABET outcomes 3, 4, 5 and 7 are transversal and developed across a curriculum [E: LC-001, LC-002]: a typed transversal layer lets a programme map them once.

## Dissent and trade-offs

- **DC vs CA hypothesis:** if "human-AI practice is transversal" meant *all* responsible-AI content, methods would lose an expert owner and anchors would drift generic — hence the three layers.
- **SC:** accepts merging SC-C05 only because the legal-adequacy anchors survive.
- **CM:** D7 bridging should not be cited as evidence of portability until re-derived; agreed.
- **Trade-off named:** a universal floor adds three L1 requirements to every role (assessment load) in exchange for the competency the 2025–26 evidence most consistently demands.
