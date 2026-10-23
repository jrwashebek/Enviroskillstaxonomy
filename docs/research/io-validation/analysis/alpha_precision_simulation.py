#!/usr/bin/env python3
"""IO role: Monte Carlo of Krippendorff alpha sampling precision for the craft-weight pilot (validation_protocol.md s.7.3).
Generating model: latent task score + independent rater noise with given single-rater reliability; ordinal3 = latent cut at -0.5/0.7.
Run: python3 alpha_precision_simulation.py  (seeded; 300 reps per cell)."""
import numpy as np
rng=np.random.default_rng(1)
def kalpha(M, metric='interval'):
    # M: units x raters, complete data
    vals=M.flatten(); n=vals.size
    if metric=='interval': d=lambda a,b:(a-b)**2
    elif metric=='nominal': d=lambda a,b:(a!=b).astype(float)
    # observed disagreement: within-unit pairs
    m=M.shape[1]
    Do=0.0
    for u in M:
        diff=d(u[:,None],u[None,:]); Do+=diff.sum()/(m-1)
    Do/=n
    De=d(vals[:,None],vals[None,:]).sum()/(n*(n-1))
    return 1-Do/De
def sim(units,raters,rel,metric,reps=300):
    out=[]
    for _ in range(reps):
        true=rng.normal(size=units)
        noise_sd=np.sqrt((1-rel)/rel)
        X=true[:,None]+rng.normal(scale=noise_sd,size=(units,raters))
        if metric=='ordinal3':
            X=np.digitize(X,[-0.5,0.7]).astype(float); out.append(kalpha(X,'interval'))  # interval on 0/1/2 approximates ordinal
        elif metric=='nominal3':
            X=np.digitize(X,[-0.5,0.7]); out.append(kalpha(X,'nominal'))
        else: out.append(kalpha(X,'interval'))
    a=np.array(out); return a.mean(),np.percentile(a,2.5),np.percentile(a,97.5)
for metric in ['interval','ordinal3']:
    for rel in [0.6,0.8]:
        for units in [40,120,200]:
            for raters in [3,6]:
                m,lo,hi=sim(units,raters,rel,metric)
                print(f'{metric:9s} true_single_rater_rel={rel} units={units:3d} raters={raters}  alpha mean={m:.3f}  95% sampling range=[{lo:.3f},{hi:.3f}] width={hi-lo:.3f}')
