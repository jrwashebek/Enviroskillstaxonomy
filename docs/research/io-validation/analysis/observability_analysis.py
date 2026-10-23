#!/usr/bin/env python3
"""IO role (EMST v2) -- reproducible appraisal of v1 measurement design.

Run from the repo root:  python3 docs/research/io-validation/analysis/observability_analysis.py

Inputs (read-only):
  legacy/v1/data/20260223_SkillsTaxonomy_Core_V3_reconciled__copyB_aaf34c8c.xlsx
  data/v1_baseline/{tasks,exposure_sources,source_text/indicators}.csv
  docs/research/io-validation/analysis/ratings/*.txt   (manual OBS-4 codes, see indicator_writing_rules.md s.2)
Outputs (written next to this script):
  ../v1_observability_ratings.csv          statement-level manual codes (sample + holdout) with rule-coder codes
  ../v1_observability_population_rulecoded.csv   all 6,268 v1 statements coded by the frozen rule coder
  observability_summary.json               every number quoted in report.md s.3

Method notes
- Manual codes were assigned blind (no rule-coder output visible) by one rater (the IO agent, an LLM).
  This is a single-rater measurement and is itself subject to the reliability critique in report.md;
  it should be re-coded by >=2 trained human raters before any v1 figure is used in a publication.
- The rule coder (rule_code) was written AFTER the 43-competency sample was rated and then FROZEN;
  the 6-competency holdout was rated afterwards, so holdout agreement is the honest estimate.
"""
import json, re, glob, math, os
from collections import Counter
import numpy as np
import pandas as pd
from scipy.stats import binom

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
XLSX = os.path.join(ROOT, 'legacy/v1/data/20260223_SkillsTaxonomy_Core_V3_reconciled__copyB_aaf34c8c.xlsx')
BASE = os.path.join(ROOT, 'data/v1_baseline')
LV = {'FOUNDATIONAL': 'F', 'INTERMEDIATE': 'I', 'ADVANCED': 'A', 'EXPERT': 'E'}
ORDER = ['F', 'I', 'A', 'E']

# ---------------------------------------------------------------- statements
def load_statements():
    pi = pd.read_excel(XLSX, sheet_name='Proficiency Indicators', dtype=str)
    rows = []
    for _, r in pi.iterrows():
        code, lv = r['Competency Code'], LV[r['Proficiency Level']]
        K, A = r['Knowledge'], r['Application']
        inds = [r[f'Indicator {i}'] for i in range(1, 7)]
        if pd.isna(K):  # Domain 5 parse defect: K/A sit in Indicator 1/2, Indicator 3 = 'Indicators*:'
            K = re.sub(r'^Knowledge\*:\s*', '', str(inds[0]))
            A = re.sub(r'^Application\*:\s*', '', str(inds[1]))
            inds = []
        rows.append((f'{code}|{lv}|K', code, r['Domain #'], lv, 'Knowledge', K))
        rows.append((f'{code}|{lv}|A', code, r['Domain #'], lv, 'Application', A))
        for i, x in enumerate(inds, 1):
            if isinstance(x, str) and x.strip() and not x.startswith('Indicators*'):
                rows.append((f'{code}|{lv}|I{i}', code, r['Domain #'], lv, 'Indicator', x))
    return pd.DataFrame(rows, columns=['sid', 'code', 'domain', 'lvl', 'stype', 'text'])

# ---------------------------------------------------------------- frozen rule coder
R0 = (r'^(shapes|influences|advances|transforms|recognized|is recognized|achieves recognition|provides (strategic )?(\w+ )?leadership|'
      r'leads (transformative|sector|industry)|defines .* transformative|demonstrates significant)|adopted (widely|sector-wide)|field-wide|'
      r'thought leader|influential|recognized (expert|authority|leader)|nationally or internationally|at systemic level|^ensures .*(inspiring|relevan|drives|advances)')
R1 = (r'^(understands|knows|familiar|awareness|aware|appreciates|values|expert in|deep understanding|comprehensive (cultural )?expertise|proficient in|'
      r'has knowledge|considers whether|balances)|^recognizes (that|the importance|arguments|limits|variation|food|water|survey biases|tool limitations)|^recognizes when mission')
R3V = (r'^(collects|records|calculates|measures|identifies|explains|describes|diagrams|maps|operates|follows|completes|performs|prepares|drafts|writes|'
       r'documents|compiles|downloads|installs|plants|removes|piles|creates (basic|simple)|enters|inspects|samples|tests|classifies|maintains (accurate|records)|'
       r'locates|summarizes|reads|sets|displays|accesses|edits|shares|organizes|tracks|calibrates|troubleshoots|conducts (point|t-tests|basic|routine|systematic|'
       r'thorough|power|occupancy|value|dynamic|food|comprehensive (material|stakeholder))|uses (handheld|binoculars|yield|safety|hazmat|comments|mark|distance|'
       r'regression|r or|statistical)|reconstructs|assesses (severity|fuels)|interprets (population|landscape|dashboard|decision|imagery|drone)|develops (site-specific|'
       r'variable|compliance protocols|corrective|mission-based|simple decision|automated alerts|monitoring plans|biodiversity credit or|climate risk disclosure|'
       r'air quality improvement)|designs (statistically|data sharing|validation|quality assurance|intervention decision|deliberate|team-level|oversight)|applies '
       r'(a structured|reversibility|accountability)|negotiates|evacuates|contains|establishes isolation|selects appropriate ppe|implements (erosion|mechanical)|'
       r'creates (defensible|materiality|user)|drafts|facilitates mission|translates|handles routine|distinguishes|quantifies|produces|evaluates emission|models '
       r'(air|pollutant)|conducts retrospective|conducts systematic)')

def rule_code(t):
    s = str(t).strip().lower()
    if s.startswith('publishes') or ('completes' in s and 'training' in s):
        return 3 if 'influential' not in s else 0
    if re.search(R0, s): return 0
    if re.search(R1, s): return 1
    if re.search(R3V, s): return 3
    return 2

def kappa(a, b, quadratic=False):
    O = np.zeros((4, 4))
    for x, y in zip(a, b): O[int(x), int(y)] += 1
    E = np.outer(O.sum(1), O.sum(0)) / O.sum()
    W = np.array([[((i - j) ** 2) / 9 if quadratic else float(i != j) for j in range(4)] for i in range(4)])
    return float(1 - (W * O).sum() / (W * E).sum())

def read_ratings(files):
    rat = {}
    for f in files:
        for line in open(f):
            line = line.strip()
            if line and not line.startswith('#'):
                k, v = line.split(':', 1)
                rat[k.strip()] = v.split()
    return rat

def attach(st, rat, set_name):
    out = []
    st = st.copy(); st['key'] = st.sid.str.rsplit('|', n=1).str[0]
    for k, g in st.groupby('key', sort=False):
        if k not in rat: continue
        codes = rat[k]
        assert len(codes) == len(g), (k, len(codes), len(g))
        for (_, r), c in zip(g.iterrows(), codes):
            d = r.to_dict(); d.update(score=int(c[0]), flags=c[1:], set=set_name); out.append(d)
    return pd.DataFrame(out)

def main():
    summ = {}
    st = load_statements()
    summ['population_statements'] = int(len(st))
    rdir = os.path.join(HERE, 'ratings')
    sample = attach(st, read_ratings(sorted(glob.glob(os.path.join(rdir, 'ratings_b*.txt')))), 'sample')
    hold = attach(st, read_ratings([os.path.join(rdir, 'ratings_holdout.txt')]), 'holdout')
    m = pd.concat([sample, hold], ignore_index=True)
    for fl in 'PCOT': m[fl] = m['flags'].str.contains(fl)
    m['rule_code'] = m.text.map(rule_code)
    sc = pd.read_csv(os.path.join(rdir, 'sample_competencies.csv'), dtype=str)
    craft = pd.read_excel(XLSX, sheet_name='Dimension Tags', dtype=str).set_index('Competency Code')['Craft Primary']
    m['craft'] = m.code.map(craft)
    m['usable'] = (m.score >= 2) & (~m.P)
    s = m[m.set == 'sample']
    summ['sample'] = {'competencies': int(s.code.nunique()), 'statements': int(len(s)),
                      'domains': sorted(s.domain.unique().tolist()), 'skill_areas': int(s.code.str.rsplit('.', n=1).str[0].nunique())}
    summ['sample_score_pct'] = {int(k): round(v * 100, 1) for k, v in s.score.value_counts(normalize=True).sort_index().items()}
    summ['sample_by_level_pct'] = {lv: {int(k): round(v * 100, 1) for k, v in s[s.lvl == lv].score.value_counts(normalize=True).sort_index().items()} for lv in ORDER}
    summ['sample_by_type_pct'] = {t: {int(k): round(v * 100, 1) for k, v in s[s.stype == t].score.value_counts(normalize=True).sort_index().items()} for t in ['Knowledge', 'Application', 'Indicator']}
    summ['sample_flags_pct'] = {f: round(float(s[f].mean() * 100), 1) for f in 'PCOT'}
    summ['sample_flags_by_level_pct'] = {lv: {f: round(float(s[s.lvl == lv][f].mean() * 100), 1) for f in 'PCOT'} for lv in ORDER}
    summ['sample_usable_by_level_pct'] = {lv: round(float(s[s.lvl == lv].usable.mean() * 100), 1) for lv in ORDER}
    summ['sample_by_domain'] = {d: {'n': int(len(g)), 'mean': round(float(g.score.mean()), 2), 'pct3': round(float((g.score == 3).mean() * 100), 1),
                                    'pct0': round(float((g.score == 0).mean() * 100), 1), 'usable_pct': round(float(g.usable.mean() * 100), 1)} for d, g in s.groupby('domain')}
    summ['sample_by_craft'] = {c: {'n': int(len(g)), 'mean': round(float(g.score.mean()), 2), 'pct3': round(float((g.score == 3).mean() * 100), 1),
                                   'pct0': round(float((g.score == 0).mean() * 100), 1), 'usable_pct': round(float(g.usable.mean() * 100), 1)} for c, g in s.groupby('craft')}
    lvl_ok = s.groupby(['code', 'lvl']).apply(lambda g: bool(((g.score == 3) & (~g.P)).any())).unstack()
    summ['share_competency_levels_with_direct_nonproxy_statement_pct'] = {lv: round(float(lvl_ok[lv].mean() * 100), 1) for lv in ORDER}
    summ['knowledge_statements_coded_0_or_1_pct'] = round(float((s[s.stype == 'Knowledge'].score <= 1).mean() * 100), 1)
    # agreement manual vs rule coder
    for name, g in [('in_sample', s), ('holdout', m[m.set == 'holdout'])]:
        summ[f'rule_vs_manual_{name}'] = {'n': int(len(g)), 'exact': round(float((g.score == g.rule_code).mean()), 3),
                                         'kappa': round(kappa(g.score, g.rule_code), 3), 'quadratic_weighted_kappa': round(kappa(g.score, g.rule_code, True), 3)}
    # population estimates with frozen coder
    st['rule_code'] = st.text.map(rule_code)
    summ['population_rulecoded_by_level_pct'] = {lv: {int(k): round(v * 100, 1) for k, v in st[st.lvl == lv].rule_code.value_counts(normalize=True).sort_index().items()} for lv in ORDER}
    low = lambda lv, typ, pat: int(st[(st.lvl == lv) & (st.stype == typ)].text.str.lower().str.match(pat).sum())
    summ['template_counts_of_222'] = {'expert_K_starts_Shapes': low('E', 'Knowledge', r'^shapes'),
                                      'advanced_K_starts_Expert_in': low('A', 'Knowledge', r'^expert in'),
                                      'foundational_K_starts_Understands_Familiar_Aware': low('F', 'Knowledge', r'^(understands|familiar|aware)')}
    e = st[st.lvl == 'E']
    bp = r'^(shapes|advances|transforms)|influence|^publishes|recogni|^provides .*leadership|^develops (innovative|novel|new)|consult|^advises|^leads (major|transformative)'
    summ['expert_level_mean_share_boilerplate_per_competency'] = round(float(e.assign(b=e.text.str.lower().str.contains(bp)).groupby('code').b.mean().mean()), 3)
    # data-integrity checks
    pi = pd.read_excel(XLSX, sheet_name='Proficiency Indicators', dtype=str)
    summ['domain5_levels_without_valid_indicators'] = int((pi[pi['Domain #'] == '5'][['Indicator 4']].isna().all(axis=1)).sum())
    src = pd.read_csv(os.path.join(BASE, 'source_text/indicators.csv'), dtype=str)
    summ['source_text_indicators'] = int(len(src)); summ['source_indicators_absent_from_db'] = int((src.in_db_any_position != 'true').sum())
    tasks = pd.read_csv(os.path.join(BASE, 'tasks.csv'), dtype=str)
    summ['career_ladder_by_task_position'] = {str(k): v for k, v in pd.crosstab(tasks.task_n, tasks.career_ladder).to_dict(orient='index').items()}
    t = tasks.text.fillna('')
    summ['task_quality_pct'] = {'has_standard_marker': round(float(t.str.contains(r'according to|following|per |in accordance|compliant|meeting|standard|protocol', case=False).mean() * 100), 1),
                                'compound_and_or': round(float(t.str.contains(r'\b(?:and|or)\b [a-z]+(?:s|e)\b', case=False).mean() * 100), 1),
                                'names_AI_or_specific_technology': round(float(t.str.contains(r'\bAI\b|machine learning|artificial intelligence|AI-|automat|algorithm|drone|UAV|LiDAR|GPS|sensor|software|GIS|blockchain|crypto|VR|AR\b|digital twin|app\b|platform|dashboard|robot', case=False).mean() * 100), 1),
                                'leading_verb_use': round(float(t.str.match(r'^Use\b').mean() * 100), 1)}
    dt = pd.read_excel(XLSX, sheet_name='Dimension Tags', dtype=str)
    B = lambda x: str(x).strip().lower() in ('true', 'yes', 'y')
    viol = []
    for _, r in dt.iterrows():
        tk = [(r[f'T13: {x} Career'], r[f'T13: {x} Auto Type']) for x in ('T1', 'T2', 'T3')]
        exp = any(c == 'P' and a in ('Ac', 'S', 'V') for c, a in tk)
        if exp != B(r['T13: CLD Flag']): viol.append(r['Competency Code'])
    summ['cld_rule_violations'] = viol
    summ['out_of_vocabulary_values'] = {'CLD Flag': sorted(set(dt['T13: CLD Flag'].dropna()) - {'True', 'False'}),
                                        'Modal Contested': sorted(set(dt['T13: Modal Contested'].dropna()) - {'True', 'False'}),
                                        'CLD Severity': sorted(set(dt['T13: CLD Severity'].dropna()) - {'High', 'Moderate', 'Low'})}
    summ['ethical_lens_populated_competencies'] = int(dt['L1 Equity & Justice'].notna().sum())
    ex = pd.read_csv(os.path.join(BASE, 'exposure_sources.csv'), dtype=str)
    tk = tasks.set_index('key')
    agr = {}
    for srcn in ['d6', 'pre15a']:
        g = ex[ex.source == srcn]
        agr[srcn] = {f: round(float((g[f].fillna('none').values == tk.loc[g.task_key, f].fillna('none').values).mean()), 3)
                     for f in ['auto_type', 'tacit_density', 'career_ladder', 'vector', 'horizon']}
    summ['same_rater_version_agreement_vs_db'] = agr
    summ['lawshe_cvr_critical_exact_one_tailed_05'] = {}
    for n in [3, 5, 8, 10, 12, 15, 20, 25, 30, 40]:
        crit = next((ne for ne in range(n + 1) if binom.sf(ne - 1, n, .5) < .05), None)
        summ['lawshe_cvr_critical_exact_one_tailed_05'][n] = None if crit is None else {'min_essential': crit, 'cvr': round((crit - n / 2) / (n / 2), 3)}
    # write outputs
    keep = ['set', 'sid', 'code', 'domain', 'craft', 'lvl', 'stype', 'text', 'score', 'flags', 'rule_code']
    m[keep].to_csv(os.path.join(HERE, '..', 'v1_observability_ratings.csv'), index=False)
    st[['sid', 'code', 'domain', 'lvl', 'stype', 'text', 'rule_code']].to_csv(os.path.join(HERE, '..', 'v1_observability_population_rulecoded.csv'), index=False)
    with open(os.path.join(HERE, 'observability_summary.json'), 'w') as f:
        json.dump(summ, f, indent=1, default=str)
    print(json.dumps(summ, indent=1, default=str))

if __name__ == '__main__':
    main()
