import csv, re, collections
B='/home/claude/emst/data/v1_baseline/'
tasks=list(csv.DictReader(open(B+'tasks.csv',encoding='utf-8')))
cs={r['code']:r for r in csv.DictReader(open(B+'craft_stage_reform.csv',encoding='utf-8'))}
for t in tasks: t['cp']=cs.get(t['code'],{}).get('craft_primary','?')
print('tasks',len(tasks))
ct=collections.Counter((t['cp'],t['auto_type']) for t in tasks)
for cp in ['FC','DC','SC']:
    tot=sum(v for (c,a),v in ct.items() if c==cp)
    print(cp, tot, {a:ct[(cp,a)] for a in ['A','Ac','H','S','V']}, 'H%%=%.1f'%(100*ct[(cp,'H')]/tot))
# SC H by domain (D7 normative)
sch=collections.Counter(t['code'].split('.')[0] for t in tasks if t['cp']=='SC' and t['auto_type']=='H')
print('SC H by domain', dict(sch))
# Field-type tasks by verb/phrase, regardless of parent craft
field=re.compile(r'\b(collect|measure|install|deploy|conduct field|field[- ]based|in the field|field surveys?|survey|sample|sampling|electrofish|netting|trap|plant|construct|operate|navigate|monitor .* in the field|inspect|ground[- ]truth|calibrat|troubleshoot|maintain)\b',re.I)
desk=re.compile(r'\b(model|analy[sz]e|software|database|gis|statistic|report|develop .*plan|policy|draft|review documents?)\b',re.I)
ft=[t for t in tasks if field.search(t['text']) and not desk.search(t['text'])]
print('field-type tasks (field verb, no desk verb):',len(ft))
c2=collections.Counter((t['cp'],t['auto_type']) for t in ft)
for cp in ['FC','DC','SC']:
    tot=sum(v for (c,a),v in c2.items() if c==cp)
    if tot: print('  ',cp,tot,{a:c2[(cp,a)] for a in ['A','Ac','H','S','V']},'H%%=%.1f'%(100*c2[(cp,'H')]/tot))
print('DC-parent field-type tasks:')
for t in ft:
    if t['cp']=='DC': print('   ',t['code'],'T'+t['task_n'],t['auto_type'],t['tacit_density'],'|',t['text'][:95])
print('FC-parent field-type tasks coded H (sample):')
for t in [x for x in ft if x['cp']=='FC' and x['auto_type']=='H'][:12]: print('   ',t['code'],'T'+t['task_n'],t['tacit_density'],'|',t['text'][:95])
# Hi tacit DC tasks: how many A vs H
hi=collections.Counter((t['cp'],t['auto_type']) for t in tasks if t['tacit_density']=='Hi')
print('Hi-tacit tasks by craft:',{cp:{a:hi[(cp,a)] for a in ['A','H']} for cp in ['FC','DC','SC']})
