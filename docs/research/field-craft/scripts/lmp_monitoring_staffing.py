import csv, glob, re, collections
csv.field_size_limit(10**9)
spec=collections.Counter(); days=collections.Counter(); n=0; plans=collections.Counter()
for f in glob.glob('/home/claude/lmps/plans/**/components.csv', recursive=True):
    for r in csv.DictReader(open(f, newline='', encoding='utf-8')):
        t=r['text'] or ''
        m=re.search(r'Primary Specialist\(s\) Needed:\s*([^|]+)', t)
        if m:
            n+=1; plans[r['plan_id']]+=1
            d=re.search(r'Estimated Days[^:]*:\s*([\d.]+)', t)
            for s in re.split(r',|;| and |/', m.group(1)):
                s=s.strip().rstrip('.')
                if s:
                    spec[s]+=1
                    if d: days[s]+=float(d.group(1))
print('rows',n, plans)
for s,c in spec.most_common(40): print(f'{c:4d}  {days[s]:6.1f}d  {s}')
