# WP-04 worklog — Data Craft and the responsible-AI layer (A4, DC)

Started 2026-10-23T13:46Z. Agent `emstagent:A4-DC@wp-04` (model claude-opus-5-5; prompt `wp04-dc-authoring@1`).
All content is draft evidence: `status: draft`, `validationStatus: draft`, `reviewStatus: unreviewed`, ratings `raterType: llm`, evidence `S`.

## Plan (priority order, S1 brief)
1. TX-A floor: DC-CAND-01, DC-CAND-02, DC-CAND-13 (+ FC/DC/SC craft enactments; SC = seed:v1-7.1.4-A), v1 7.2.3, DC-CAND-05.
2. DC specialist responsible-AI: DC-CAND-14, -15, -16, -19, -20, -21. DC-CAND-17 stays L5 watch (seed:watch-DC-CAND-17, WP-10).
3. L4 tools seed `data/v2/tools/tools.jsonl`; X12 DOL AI Literacy crosswalk.
4. Core DC practice for P1 roles (R03, R04, R05, R08, R10–R13; R31): v1 2.1.2, 2.1.4, 2.1.5, 2.2.2, 2.2.3, 2.4.1, 2.4.2; DC-CAND-03, -04, -06, -07, -08, -09, -11, -12, -22.
5. Rest of lane: v1 2.2.1, 2.4.4, DC-CAND-18; tasks of superseded D2 seeds; other DC-primary v1 seeds.

## Log
- 14:00–14:50 Builder scripts (agent-side, scratchpad; generated records are what count). Authored and validated (0 errors in WP-04 files):
  - TX-A floor: seed:DC-CAND-01, -02, -13 (+ craft enactments seed:ena-dc-cand-13-fc, seed:ena-dc-cand-13-dc, seed:v1-7.1.4-A = SC enactment), seed:v1-7.2.3 rewritten in place ("Calibrate trust in AI and automation"), seed:DC-CAND-05 (TX-A at L1, DC practice above).
  - Specialist responsible-AI: seed:DC-CAND-14, -15, -16, -19, -20, -21. DC-CAND-17 left as the existing L5 watch item seed:watch-DC-CAND-17 (WP-10); no competency authored.
  - Core DC practice: v1 2.1.2, 2.1.4, 2.1.5, 2.2.1, 2.2.2, 2.2.3, 2.4.1, 2.4.2, 2.4.4 rewritten in place (v1Seed removed once every level had v2 indicators); seed:DC-CAND-03, -04, -06, -07, -08, -09, -11, -12, -18, -22.
  - v1 tasks rewritten/re-pointed: 7.2.1, 7.1.4 (split: T1→DC-CAND-19 + SC enactment, T2→DC-CAND-14, T3→DC-CAND-21), 2.5.5, 3.5.5, 6.4.4-T2 (DC-CAND-16 part only; T1/T3 left for SC-C02), all D2 carry/rewrite/merge-target tasks, 2.3.1 split (T1/T2→FC-C01, T3→DC-CAND-04), move-to-tools residues (2.1.1→2.1.4/2.1.5, 2.3.4→FC-C23, 2.5.1→5.2.2, 2.7.1→2.1.5, 2.7.2→5.4.1, 2.7.4→2.1.5).
  - Coordination: v1 2.5.3-T1/T3 were consolidated by WP-07 into seed:v1-3.1.1-T2; I briefly overwrote them, then restored that consolidation (status superseded, replacedBy seed:v1-3.1.1-T2). 2.5.3-T2 rewritten to PS-C03. Ran `scripts/migrate_v1.py --x1-only`.
  - Left for target owners (merge targets in other lanes): 2.1.3→FC-C18, 2.3.2→FC-C14, 2.3.3→FC-C23, 2.3.5→4.4.5 (FC), 2.5.2→3.3.5 (SC). FC-enactment indicators for DC-CAND-13 are a WP-03 output.
