import csv, re, collections, sys
B='/home/claude/emst/data/v1_baseline/'
prof=list(csv.DictReader(open(B+'proficiency.csv')))
ind=list(csv.DictReader(open(B+'indicators.csv')))
tasks=list(csv.DictReader(open(B+'tasks.csv')))
sec=list(csv.DictReader(open(B+'sector_applications.csv')))
NONOBS={'understands','understand','knows','aware','appreciates','familiar','recognizes','expert','shapes','advances','is','has','demonstrates understanding','values','grasps','comprehends','learns','pioneers','thought','influences','transforms','sets','champions','redefines','visionary','leads transformative'}
# Bloom-ish verb bands
REMEMBER={'identifies','lists','names','defines','describes','recalls','recognizes','labels','locates','states'}
UNDERSTAND={'explains','summarizes','interprets','classifies','distinguishes','compares','understands','discusses','illustrates'}
APPLY={'applies','uses','conducts','collects','performs','operates','implements','follows','completes','records','measures','deploys','maintains','prepares','calculates','executes','installs','administers','processes','enters','documents','maps','runs','samples','tests','monitors','tracks','supports','assists','participates','coordinates','facilitates','communicates','writes','presents','manages','drafts'}
ANALYZE={'analyzes','evaluates','assesses','diagnoses','interprets','validates','critiques','reviews','audits','troubleshoots','compares','models','quantifies','tests','verifies','determines'}
CREATE={'designs','develops','creates','builds','leads','establishes','integrates','synthesizes','formulates','plans','directs','architects','authors','publishes','innovates','mentors','trains','negotiates','advises','oversees','pioneers','shapes','advances','sets','influences'}
def first(s):
    s=(s or '').strip()
    m=re.match(r"([A-Za-z\-]+)",s)
    return m.group(1).lower() if m else ''
def band(v):
    for n,S in [('remember',REMEMBER),('understand',UNDERSTAND),('apply',APPLY),('analyze',ANALYZE),('create',CREATE)]:
        if v in S: return n
    return 'other'
res={}
for field in ['knowledge','application']:
    c=collections.Counter(); byl=collections.defaultdict(collections.Counter)
    for p in prof:
        v=first(p[field]); c[v]+=1; byl[p['level']][v]+=1
    res[field]=c
    print(f'== {field}: top first words'); print(c.most_common(15))
    for lv in ['foundational','intermediate','advanced','expert']:
        print(' ',lv, byl[lv].most_common(6))
# non-observable rate
def nonobs(s):
    s=(s or '').lower().strip()
    return bool(re.match(r"(understands|knows|is aware|aware of|appreciates|familiar|expert in|expert|shapes|advances|recognized|thought leader|deep understanding|comprehensive understanding|demonstrates understanding|has )",s))
for field in ['knowledge','application']:
    n=sum(nonobs(p[field]) for p in prof); print(field,'non-observable lead:',n,'/',len(prof),round(100*n/len(prof),1),'%')
    for lv in ['foundational','intermediate','advanced','expert']:
        L=[p for p in prof if p['level']==lv]; n=sum(nonobs(p[field]) for p in L); print('  ',lv,n,'/',len(L))
# expert-level application statements that are about 'leads'/'shapes' field-level influence
ex=[p for p in prof if p['level']=='expert']
inf=sum(1 for p in ex if re.match(r"(shapes|advances|leads|pioneers|sets|influences|transforms|defines|redefines|establishes)",(p['knowledge']+' ').lower()) or re.match(r"(shapes|advances|leads|pioneers|sets|influences|transforms|defines|redefines|establishes)",(p['application']+' ').lower()))
print('expert rows with field-influence verbs (shapes/advances/leads...):',inf,'/',len(ex))
# indicators
print('indicators total',len(ind))
iv=collections.Counter(first(i['text']) for i in ind)
print('indicator top verbs',iv.most_common(25))
bands=collections.Counter(band(first(i['text'])) for i in ind)
print('indicator bloom bands',bands)
bl=collections.defaultdict(collections.Counter)
for i in ind: bl[i['level']][band(first(i['text']))]+=1
for lv in ['foundational','intermediate','advanced','expert']:
    t=sum(bl[lv].values()); print(' ',lv,t,{k:round(100*v/t) for k,v in bl[lv].most_common()})
nonobs_ind=sum(nonobs(i['text']) for i in ind); print('indicators non-observable lead',nonobs_ind, round(100*nonobs_ind/len(ind),1))
# autonomy / condition cues
cues={'with guidance|under supervision|with supervision|with assistance|with support':'supervised','independently|without supervision':'independent','mentors|trains others|teaches|coaches':'develops_others','publishes|peer-reviewed|journal':'publishes','national|international|global|regional':'scale'}
for pat,name in cues.items():
    n=sum(1 for i in ind if re.search(pat,i['text'],re.I)); print('cue',name,n)
# criteria/standard cues
n=sum(1 for i in ind if re.search(r"(accurate|accuracy|within|according to|per |protocol|standard|to specification|meets|compliant|correctly|%|percent)",i['text'],re.I)); print('indicators with criterion/standard cue',n,round(100*n/len(ind),1))
# tool-name cues
n=sum(1 for i in ind if re.search(r"(ArcGIS|QGIS|Python|\bR\b|Excel|Survey123|Collector|ENVI|Google Earth|Tableau|Power BI|SQL|MATLAB|ChatGPT|LiDAR software|eCognition)",i['text'])); print('indicators naming specific tools',n)
# duplicates across levels within a competency
dup=0; tot=0
byc=collections.defaultdict(lambda: collections.defaultdict(set))
for i in ind: byc[i['code']][i['level']].add(i['text'].strip().lower())
for c,d in byc.items():
    allt=collections.Counter(t for lv in d for t in d[lv])
    dup+=sum(1 for t,k in allt.items() if k>1); tot+=len(allt)
print('indicator texts repeated across levels within same competency',dup,'of',tot)
# indicators count per level
print('mean indicators/prof row', round(len(ind)/len(prof),2))
# sector applications length
L=[len(s['text'].split()) for s in sec if s['text']]; print('sector app texts',len(L),'mean words',round(sum(L)/len(L),1),'empty',sum(1 for s in sec if not s['text']))
# tasks first verb
tv=collections.Counter(first(t['text']) for t in tasks); print('task verbs',tv.most_common(12))
