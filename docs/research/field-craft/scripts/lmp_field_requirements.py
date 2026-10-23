import csv, glob, re, collections, random
csv.field_size_limit(10**9)
rows=[]
for f in glob.glob('/home/claude/lmps/plans/**/components.csv', recursive=True):
    rows += list(csv.DictReader(open(f, newline='', encoding='utf-8')))
norm=[r for r in rows if r['component_type'] in ('standard','guideline','standard_or_guideline')]
pat=re.compile(r'(field[- ]verif|ground[- ]truth|on[- ]site (review|inspection|evaluation|survey)|site[- ]specific (survey|review|evaluation|analysis|assessment)|pre-?project (survey|field)|survey(s)? (shall|will|should|must) be (conducted|completed|performed)|(conduct|complete|perform)(ed)? (pre-?\w+ )?surveys?|field (review|survey|inspection|reconnaissance)s?|surveyed (for|prior)|inspect(ed|ions?)? (by|prior|before|during))', re.I)
hits=[r for r in norm if pat.search(r['text'] or '')]
print('normative components', len(norm), 'with explicit field survey/verification/inspection requirement', len(hits), f'{100*len(hits)/len(norm):.1f}%')
print('plans with >=1 hit', len({r['plan_id'] for r in hits}), 'of', len({r['plan_id'] for r in norm}))
th=collections.Counter()
for r in hits:
    for t in (r['themes'] or '').split('|'):
        if t: th[t]+=1
print(th.most_common(15))
random.seed(7)
for r in random.sample(hits,8): print('-', r['plan_id'], '|', (r['text'] or '')[:230].replace('\n',' '))
