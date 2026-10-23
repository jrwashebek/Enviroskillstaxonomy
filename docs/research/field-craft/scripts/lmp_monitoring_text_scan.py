import csv, glob, re, sys, collections
csv.field_size_limit(10**9)
rows=[]
for f in glob.glob('/home/claude/lmps/plans/**/components.csv', recursive=True):
    with open(f, newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
print('total components', len(rows))
ct=collections.Counter(r['component_type'] for r in rows)
print(ct.most_common(15))
mon=[r for r in rows if r['component_type'] in ('monitoring_requirement','monitoring','monitoring_question','monitoring_indicator') or 'monitor' in (r['component_type'] or '')]
print('monitoring components', len(mon), collections.Counter(r['component_type'] for r in mon))
pats={
 'field_plot_survey': r'\b(plot|plots|transect|field survey|field verif|ground[- ]truth|site visit|on[- ]the[- ]ground|walk-?through|field review|field check|inspect|inspection|reconnaissance|stream survey|survey(s|ed)?)\b',
 'remote_sensing': r'\b(remote sensing|satellite|landsat|aerial photo|imagery|lidar|modis|sentinel|aerial survey|aerial detection|ADS)\b',
 'sensor_continuous': r'\b(sensor|data logger|logger|gauge|gaging|monitoring station|continuous monitor|telemetry|thermograph)\b',
 'genetic_edna': r'\b(edna|environmental dna|genetic sampl|dna)\b',
 'camera_acoustic': r'\b(camera|acoustic|bat detector|audio)\b',
 'water_sampling': r'\b(water quality|turbidity|sediment|temperature|macroinvertebrate|bmp|best management practice)\b',
 'fire_fuels': r'\b(fuel|fire|burn)\b',
 'tribal_cultural': r'\b(tribe|tribal|heritage|cultural resource|archaeolog)\b',
}
cnt=collections.Counter()
for r in mon:
    t=(r['text'] or '').lower()
    for k,p in pats.items():
        if re.search(p,t,re.I): cnt[k]+=1
for k,v in cnt.most_common(): print(f'{k}: {v} ({100*v/len(mon):.1f}%)')
# component text in standards/guidelines that require field verification
fv=[r for r in rows if re.search(r'(field verif|ground[- ]truth|on[- ]site|site[- ]specific (survey|review)|pre-?project survey|survey(s)? (shall|will|should) be (conducted|completed))', (r['text'] or ''), re.I)]
print('components requiring field verification/pre-project survey:', len(fv), collections.Counter(r['component_type'] for r in fv).most_common(6))
import random, statistics
random.seed(3)
print('median monitoring text len', statistics.median(len(r['text'] or '') for r in mon))
for r in random.sample(mon,8): print('-',r['plan_id'],'|',(r['text'] or '')[:220].replace('\n',' '))
print('plan years of monitoring comps', collections.Counter(r['plan_year'][:3] for r in mon))
# 2012-rule plans: how many monitoring comps mention method
new=[r for r in mon if r['framework']=='usfs-2012-rule']
print('2012-rule monitoring comps',len(new))
c2=collections.Counter()
for r in new:
    t=(r['text'] or '').lower()
    for k,p in pats.items():
        if re.search(p,t,re.I): c2[k]+=1
print(c2)
print(collections.Counter(r['framework'] for r in rows))
