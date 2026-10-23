"""Reproduce TN counts of Tribal-related demand signals in the OpenLMP corpus (read-only).

Usage: python3 -I lmp_tribal_counts.py [/path/to/lmps]
Outputs counts only (no component text is written), so no Tribal or confidential text is copied into EMST.
"""
import csv, glob, re, sys, collections, os, json

root = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/lmps"
csv.field_size_limit(10**9)
files = glob.glob(os.path.join(root, "plans/*/*/*/components.csv"))

pats = {
    "tribal_or_indigenous_text": re.compile(r"\btrib(e|es|al)\b|indigenous|native american|alaska native|treaty", re.I),
    "ik_tek": re.compile(r"traditional ecological knowledge|indigenous knowledge|traditional knowledge|\bTEK\b|\bITEK\b", re.I),
    "confidential_cultural_or_tribal": re.compile(r"(confidential|sensitive)[^.]{0,120}(tribal|tribe|cultural|sacred)|(tribal|tribe|cultural|sacred)[^.]{0,120}(confidential)", re.I),
    "treaty_or_reserved_right": re.compile(r"treaty|reserved right", re.I),
    "cultural_burning": re.compile(r"cultural (burn|fire)|indigenous fire|tribal (burn|fire)", re.I),
    "first_foods": re.compile(r"first foods|traditional foods|culturally significant (plant|species|food)", re.I),
}
n = 0
coord = collections.Counter()
cnt = collections.Counter()
plans = collections.defaultdict(set)
mod = collections.Counter()
for f in files:
    with open(f, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            n += 1
            c = r.get("coordination") or ""
            for s in c.split(";"):
                if s:
                    coord[s] += 1
            if "tribal" in c.split(";"):
                cnt["coordination=tribal"] += 1
                plans["coordination=tribal"].add(r["plan_id"])
                mod[r.get("modality") or "(blank)"] += 1
            t = r.get("text") or ""
            for k, p in pats.items():
                if p.search(t):
                    cnt[k] += 1
                    plans[k].add(r["plan_id"])
out = {
    "component_files": len(files),
    "components": n,
    "counts": {k: {"components": cnt[k], "plans": len(plans[k])} for k in sorted(cnt)},
    "tribal_coordination_modality": dict(mod),
    "nhpa_section_106_components": coord.get("nhpa_section_106", 0),
}
print(json.dumps(out, indent=1))
