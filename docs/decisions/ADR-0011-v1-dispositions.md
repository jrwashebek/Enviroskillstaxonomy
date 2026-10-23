# ADR-0011: v1 dispositions — carry the ideas, re-derive the structure, migrate the content as seed with provenance

- **Decision point:** DP-10 (disposition of each v1 element and competency)
- **Status:** accepted (per-competency dispositions in `docs/decisions/v1_disposition.csv`; those touching Tribal content are `hold-for-tribal-review`; those resting on DB [J] subsector claims are subject to the Phase 4 verification pass)
- **Date:** 2026-10-23 · **Decider:** CA
- **Roles consulted:** all 15 research roles (614 v1 verdicts in `_merged/v1_assessment.csv`), DE (data audit)
- **Related:** ADR-0003, ADR-0004, ADR-0005, ADR-0008, ADR-0018, ADR-0020

## Context

The v1 database is a single linear lineage (V1 → v1u → V3 → reconciled copyA → copyB) whose competency text is identical across versions; versions differ only in analytical layers [E: data-audit §1]. The import from the source text lost or corrupted a third of the assessment content (2,104 of 6,484 indicators; all 30 D5 Knowledge/Application statements) [E: data-audit §6]. Every v1 tag was assigned by one analyst with an LLM; the only redundancy (re-classification of D2 and D6) disagrees substantially [E: data-audit §14].

## Decision

### Migration rules (apply to every v1 record)

1. **Baseline = copyB** (`20260223_SkillsTaxonomy_Core_V3_reconciled__copyB_aaf34c8c.xlsx`), via the frozen, hash-pinned `data/v1_baseline/` (P-DE-01).
2. **For content, the source text outranks the database** (`data/v1_baseline/source_text/`): restore D5 Knowledge/Application and indicators, the 2,104 truncated indicators and the 19 title/description splits before any rewriting (P-DE-02, P-DE-12, P-IO-15).
3. **All 222 competencies and 666 tasks migrate as seed records** with `derivedFrom` lineage and a row in the v1→v2 SSSOM crosswalk; CI fails if any v1 key is unaccounted for (P-DE-08).
4. **Every v1 tag migrates as prior evidence only** — rater `v1-analyst-01`, low confidence, misalignment flags — never as a v2 value (P-DE-03, P-IO-14; ADR-0008 §5). This covers craft primary/secondary, workflow stages (incl. the five recovered dual-primary second stages), reform flags, families, exposure, CLD, stability tier and the 20 populated lens cells plus the D7.2 lens values recovered from the D7 record.
5. **Stored summaries are not migrated** (modal exposure, counts, Zero-Core, FPP, tier, reform count); they become computed views or retire (P-DE-04, P-DE-13).

### Disposition vocabulary (per competency, `v1_disposition.csv`)

| Decision | Meaning |
|---|---|
| `carry` | Concept and scope carry into v2 with editorial normalization (verb-led title, description repair, IO-standard indicators rewritten from seeds) |
| `rewrite` | Concept kept but scope or framing changes materially (regime-agnostic, function-based, actor-neutral, tool-free); usually absorbs a candidate |
| `split` | One v1 competency becomes two or more v2 entities (e.g. practice + knowledge area; field risk vs safety programme) |
| `merge` | Folded into another v1 competency or a candidate as the surviving target (duplicates by domain, e.g. 1.2.4/4.1.3, 2.3.2/4.5.4, 4.2.3/4.3.2, 6.6.5/6.8.2) |
| `retire` | Withdrawn without successor (ID never minted; v1 code maps to `sssom:NoTermFound` with rationale) |
| `move-to-tools` | Content is tool fluency; the durable remainder (if any) goes to a named target and the tool family to L4 |
| `move-to-module` | Valid but subsector-specific under the three-module rule; homed in a module, not the core |
| `hold-for-tribal-review` | Touches Tribal governments, Indigenous knowledge or Tribal data; drafted internally only, under ADR-0007's content hold |

### Element-level dispositions (finalizing `docs/audit/v1_carry_forward_register.csv`)

| v1 element | Final disposition | Decided in |
|---|---|---|
| Seven domains, 45 skill areas, 5-per-area rule, D.SA.N codes | Retire as structure; keep as legacy alias facet and aliases | ADR-0002, ADR-0010 |
| Competency as untyped entity; noun-phrase titles | Typed entities; verb-led titles for practices | ADR-0003 |
| Task text (666) | Carry as seed; verify against v2 text (supersedes Pre-15B); strip tools; split compound and level-graded tasks | ADR-0003, ADR-0020 |
| Four tenure levels; Knowledge/Application stems; indicators | Retire levels and stems; indicators carried as draft seeds only | ADR-0004 |
| Five sector-application notes | Retire as structure; keep text as seed illustrations for variants and enactments | ADR-0007 |
| Example positions, career pathway tables, cross-cutting blocks in source text | Add: seed role inventory, progression links and transversal layer (re-resolve stale SA numbering by hand) | ADR-0006, ADR-0025 |
| Craft definitions, irreducibility test, integration points | Carry, re-worded as v2 definitions and rater rubric | ADR-0005 |
| Craft primary/secondary; predicted distribution | Retire as stored values (prior evidence); retire the circular calibration | ADR-0005 |
| Crafts as reproduction regimes (Structural Conditions) | Add as reproduction-regime attributes | ADR-0005 |
| Five Functional Positions | Carry as Data Craft's five functions and as LC bundle anchors | ADR-0005, ADR-0026 |
| 15 profession families; Core/Supporting matrix; family→SOC crosswalk | Families → computed job families of role profiles (F4, F13 split); matrix retired; crosswalk retired as anchor after fixing verified errors (19-1012, 33-1021; 25-4031 and 29-9021 misdirected; add 19-2041) | ADR-0006, ADR-0022 |
| Workflow stages S1–S6, caps, dual-primary | S1–S6 kept as the *project-authorization lifecycle* workflow profile mapped onto work functions; stages move to tasks; caps retired | ADR-0017 |
| Six reform flags; reform count; stability tier | Retire as columns; seed dated instruments and driver events; tier replaced by computed robustness class | ADR-0008, ADR-0028 |
| Exposure instrument, Ac, A/V rule, vectors, CLD + R9 rubric | Carry the concepts; re-issue as codebook v2; v1 values prior evidence | ADR-0008 |
| Tacit density, career position, horizon | Change: tacit assessed independently; career position derived from role profiles; horizon replaced by dated assessments | ADR-0008 |
| Standing rules R1–R12; FC/DC structural finding | Re-issue with unique IDs (XR-NN); R1's expectation clause dropped; finding retired | ADR-0008 |
| Ethical lenses L1–L5 | Carry definitions; use as indicator-writing rubric, search facet and review checklist; L2 fixed per TN and gated; R10 retired; any tag population must pass IO's α gate | ADR-0024, ADR-0007 |
| Domain 7 as a "domain" | Change into the transversal practice layer; 7.2 content carried; 7.1.1 held | ADR-0025 |
| Task sequence v7, source-of-truth hierarchy, Airtable/GitBook pipeline, Workforce Signals sheet | Retire; repo-native governance; generated dashboards | ADR-0009, ADR-0020 |
| Change log CL-001…CL-014 | Carry as v1 history | — |
| Delphi plan; sentinel network | Redesign under IO; carry sentinel concept into FS horizon scanning | ADR-0024, ADR-0028 |
| Forester PD prototype | Carry as flagship view, regenerated from data in FES format and labelled "subject to classification review" | ADR-0027 |
| Public validation claims (Flourish slides 1 and 3) | Retire now | ADR-0027 |

### Counts (from `v1_disposition.csv`, generated)

The CSV records one decision per v1 competency. Counts are generated by the build and reported in release notes; they are not hand-typed here (P-DE-13, AS claims hygiene).

## Rationale and evidence

The structural verdicts rest on the audit's direct inspection of v1 and DE's reproducible baseline (65 passing tests). Per-competency decisions weigh: role verdicts (FC on 49 FC-primary competencies; DC on all 35 D2; SC on D3/D5/D6/D7; TN on Tribal content; DB on subsector items; PS, IO, LC, FH, SL, FS), DC's durable-vs-tool classification, DE's near-duplicate screen, candidate competencies that absorb v1 items (`related_v1_codes`), and FS's stress-test protect suggestions [E/J as cited in each row's `role_verdicts_considered`].

## Consequences

- Phase 4 WP-02 implements `scripts/migrate_v1.py` reading `v1_disposition.csv` as machine-readable decisions (DE M2).
- Protect suggestions (59 v1 competencies from FS's heuristic stress test) are recorded as candidate governance decisions, not applied automatically (ADR-0015).

## Dissent and trade-offs

- **FC** retires none of the 49 FC competencies (carry 21, change 27); **DC** retires 7 of 35 D2. The CA follows both, with merges where duplicates exist across their lanes.
- **Trade-off named:** migration effort and a smaller, honest v2.0 versus continuity of v1's counts and published narratives (which must not be cited without re-derivation; ADR-0027).
