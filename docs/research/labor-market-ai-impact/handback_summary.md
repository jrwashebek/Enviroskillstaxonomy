**LM summary.** Writing `report.md` was refused, so its full text follows the marker line below. Everything else is saved in `/home/claude/emst/docs/research/labor-market-ai-impact/`.

**Top findings**
- **[E] Environmental work has two exposure profiles.** On LLM exposure, the analytical and regulatory occupations rank in the 81st–99th percentile of the whole economy (Environmental Scientists 98th, Sustainability Specialists 97th, Planners 90th). Field occupations rank 10th–33rd. The indices agree on ranking (ρ 0.70–0.91) but measure different things.
- **[E] Environmental work shows up little in usage data.** Usage-based scores put 20 of 24 environmental occupations below their theoretical exposure. In the AEI, each environmental task is 0.002–0.02% of conversations. [J] Likely causes are that government is not sampled, plus real adoption lag.
- **[E] Federal environmental agencies show two waves of AI.** 504 use cases, of which 61 of 347 with a reported stage (18%) are deployed, mostly classical ML for science. Generative-AI drafting tools are licensed agency-wide (EPA 10,000–50,000 users). No NEPA or permitting AI is deployed.
- **[E via FH/FS/FC/AS] The 2025–26 workforce shock is fiscal and policy-driven, not AI.** USFS lost 16% to over 25% (sources use different bases), NPS over 25%, EPA staffing is at a 40-year low, and seasonal hiring was halted. This swamps any AI signal. No environment-specific causal evidence of AI job effects exists.
- **[E] Land management plans show where demand is growing.** Monitoring is 22% of components in 2012-rule plans vs 1.8% in 1982-rule plans, and partnership and Tribal touchpoints about tripled. Plans name outcomes, not methods (remote sensing appears in 3 of 1,506 monitoring questions).
- **[E] The v1 pilot (60 tasks matched to O*NET) partly supports v1.**
  - 30% of tasks have no O*NET match, which marks them as candidate new work.
  - v1's Ac and H labels broadly agree with external ratings; S does not.
  - v1's "A" mixes desk tasks with physical tasks.
  - The external labels themselves are unstable: 13 of 21 alternate matches disagree.

**Top proposals:** P-LM-01 (split exposure into three constructs), P-LM-02 (hand-built O*NET crosswalk), P-LM-04 (require deployment evidence for S/V claims), P-LM-06 (career-ladder risk at pathway level, with its driver recorded), P-LM-07 (two independent evidence families before a role indicator moves), P-LM-08 (plan-requirement demand pipeline).

**Biggest trade-off:** usage data understate environmental exposure and theoretical scores overstate it, so both are needed. HR wants one label per role. I want the components shown, and FC will resist the finding that the desk half of environmental work is highly exposed.

**Limits:**
- Hugging Face was blocked, so the AEI join is designed but not run.
- The web-search budget ran out, so most index releases are unverified.
- The primary AEI labor-market study was not read.

**Files written:**
- **Required CSVs:** `sources.csv`, `index_appraisal.csv`, `env_occupations_in_scope.csv`, `ecosystem.csv`, `role_signals.csv`, `v1_assessment.csv`, `candidate_competencies.csv`.
- **Analysis outputs:** `env_occupation_exposure_scores.csv`, `index_agreement_spearman.csv`, `aei_env_rows_seen.csv`, `omb_*.csv`, `lmp_outputs/`, `v1_onet_pilot_*`.
- **Scripts:** all in `scripts/`; re-runs give identical outputs.

# FULL TEXT OF report.md

