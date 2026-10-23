# ADR-0020: Disposition of the v1 task sequence (v7), the WFIC-1 decision gate, and pending Tasks Pre-15B through 22

- **Decision point:** DP-19 (v1 task-sequence v7 disposition, including the WFIC-1 gate)
- **Status:** accepted
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** FS, FC, DC, FH, LC, AS, IO, DE, SC, TN, CP
- **Related:** ADR-0006 (role tiers), ADR-0009 (governance), ADR-0011, ADR-0018 (MOD-11), ADR-0024 (Delphi), ADR-0027 (publication), ADR-0028 (sentinels)

## Context

`taxonomy_task_sequence_v7.md` (March 2026) says Tasks 1–14 are complete and Pre-15A through 22 remain; it inserts WFIC-1 (mapping test against Wildfire Intelligence Center requirements) with a **decision gate**: proceed to WFIC-2/3 (draft competencies, establish profession family F16, integrate with D.SA.N codes) if 3+ functional areas have no coverage or the gaps are genuinely new professional work; otherwise adjust Task 15.5 only. v7 defers the specifications of Tasks 15, 15.5, 16, 16.5 and 17–22 to v6, which was slated for removal, so the governing text for the remaining work is not in the record [E: CA-007, CA-005]. v7 names `skills_taxonomy_workforce_v1_updated.xlsx` (215 competencies) as the active database, which cannot represent the 222-competency state [E: data-audit §1].

FS recommends resolving fire intelligence as an **L3 role family** rather than a new profession family (FS open Q6); FH notes fire-intelligence work spreads across 0132, 1340, 1560, 2210, 0462 and 0401 (FH §4); AS's v1 verdict: WFIC/F16 → function-defined and NWCG-linked; CA's Phase 1 register: a role cluster within a fire module, used as a pilot for subsector extension.

## Decision

### 1. The task sequence retires as the governance instrument

v7 is archived as v1 history. Remaining work is governed by ADRs, the Phase 4 build plan and repo-native change requests (ADR-0009). Its v1 source-of-truth hierarchy is void; `data/v1_baseline/` (copyB) is the only v1 input.

### 2. WFIC-1 decision gate — resolved: do not run WFIC-2/3; fire intelligence becomes an L3 role family

- **No F16 profession family and no new D.SA.N codes.** Fire intelligence is defined by **function** — fusing multi-source fire, fuels, weather and resource information into operational and planning decision support — not by an institution (v7's own design principle).
- It enters v2.0 as **role profile R08 "Fire intelligence analyst (continuous operations)"** in corridor COR-2, lifecycle `emerging` (ADR-0006), home module **MOD-11** with variants: federal (USWFS/USFS), state fire agencies, private (utility situational-awareness centres), academic/NGO; Tribal variant held (ADR-0007). It is composed from tasks linked to the new candidate **"Fuse multi-source fire intelligence into operational decision support"** (FS-C05), existing v1 4.3.4 and 2.1.2, the core AI-validation transversal (ADR-0025), and decision-support design (DC-CAND-22).
- v7's three-way `fire_context_note` (suppression / prescribed fire / fire intelligence) is replaced by role profiles and the work-function facet (`WF-RESPOND`, `WF-PLAN`, `WF-MONITOR`).
- The WFIC becomes a **named horizon-scanning channel** (fire and fire intelligence), alongside permitting, carried from v1 Task 22 (FS protocol; AS P-AS-12). Its institutional design remains a watch item: the claim that EO 14308 directed a national Fire Intelligence Center is a v1 record not re-verified here; USWFS was established by SO 3448 on 12 Jan 2026 [E: V1-06]; consolidation of USFS fire is only proposed in the FY2027 budget [E: V1-06 note].
- **Gate reasoning:** v7's own "proceed" condition (genuinely new professional work) is met — but the v2 architecture answers it with a role family composed from tasks and a small number of candidate competencies, which is exactly the subsector-extension pattern WFIC was meant to pilot.

### 3. Pending v7 tasks

| v7 task | Disposition | Successor in v2 |
|---|---|---|
| **Pre-15A** D6 Ac retrospective | **Closed as executed** (applied in copyA/copyB, not cleanly: 24/30 exact, 6 hybrids; before/after statistics unreliable) [E: data-audit §1.3] | Its per-task notes migrate as v1 prior-evidence rationale (ADR-0008 §5) |
| **Pre-15B** D3 task-description verification | **Superseded and widened**: D1 (82/120), D3 (98/105) and D2 exposure text misalignment make verification against v1 text moot; exposure is re-derived against v2 task text | Phase 4 WP-02/WP-06 (re-rating against hash-pinned v2 text) |
| **WFIC-1 / WFIC-2 / WFIC-3** | Gate resolved as above; WFIC-2/3 not run | R08 role family in MOD-11; FS-C05 candidate |
| **15** Ethical lens population | **Retired as column population.** Lenses become an indicator-writing rubric, a search facet and a governance review checklist; any tag population must pass IO's α gate after ≤ 2 codebook iterations, else ethics is expressed only through observable indicators (answers IO open Q6); L2 definitions and tags are published only through the Tribal gate | ADR-0024, ADR-0007 |
| **15.5** Context columns (fire, permitting) | **Retired** | Modules, work functions, workflow profiles, instrument registry |
| **16** Stability-tier validation and labor-market enrichment | **Retired** (tier); enrichment **replaced** | Computed robustness class; LM's curated O*NET task crosswalk and role-level SOC/OPM crosswalks (P-LM-02, P-LM-10) |
| **16.5** Project knowledge inventory | **Closed** by Phase 1 (legacy capture with SHA-256 manifest; `data/v1_baseline/`) | `legacy/v1/README.md` + MANIFEST |
| **17** GitBook architecture | **Retired** | CP Tier 1 static explorer (ADR-0012, ADR-0027) |
| **18** Python export + Markdown | **Superseded** | DE build and export pipeline (ADR-0010) |
| **19** GitBook build → "Published V1" | **Retired; v1 is not published as a standard.** v1 remains available as an archived, clearly labelled historical dataset | v2.0 release (Phase 4/5) |
| **20–21** Delphi preparation and execution → V1.1 | **Redesigned** under IO's pre-registered modified Delphi against v2 entities (15–25 per panel; exact Lawshe values; sector-actor caps; field practitioners in proportion; Tribal track on Tribal time) | ADR-0024; Phase 5 |
| **22** Sentinel network design | **Carried** into FS's horizon-scanning protocol and AS's sentinel network (60–90 stratified, compensated) | ADR-0028 |

## Rationale

- Function over institution is the v1 principle and a team design principle; fire-intelligence work is spread across six series [E: FH-040 via FH], so a family tag cannot carry it, while a role family with variants and crosswalks can.
- Fire intelligence has the strongest evidence among FS's emerging roles ("now" horizon; FireSat operational July 2026; FS-011, FS-053, FS-034) [E via FS §7].
- Running v1 tasks against a superseded structure would produce v1 tags that v2 treats only as prior evidence (ADR-0011).

## Consequences

- The v1 project's companion research outputs that cite F16 or WFIC-2/3 plans should be updated (carry-over flag to the Skills Taxonomy research project).
- LC-PW-03 (timber cruiser or field technician → remote-sensing inventory or fire intelligence) becomes the R02/R04 → R08 pathway.

## Dissent and trade-offs

- **None of the roles argued for F16.** The trade-off is continuity with v7 users who expected a 222+n count and an F16 family page.
