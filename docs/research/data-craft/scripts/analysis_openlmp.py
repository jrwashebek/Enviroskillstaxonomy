"""Reproduce the DC demand-signal counts from OpenLMP plan components (report section 5.7; source DC-035).

Usage: python3 -I analysis_openlmp.py [/home/claude/lmps]   (read-only; commit b3e55df used)

Counts components mentioning data-craft terms (case-insensitive regex on `text`) and tallies the
`authoritative_data` field. Note the naive case-sensitive '\\bAI\\b' pattern returns 16 components and none
concerns artificial intelligence (9 'MON-AI-xx' American Indian Rights and Interests monitoring codes; the rest
are management-area codes, an 'A1' soil horizon and an OCR split of 'Although'); the AI/ML count therefore uses
explicit phrases only.
"""
import collections, csv, glob, os, re, sys

csv.field_size_limit(10**9)
ROOT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/lmps"
PATS = {
    "ai_ml (explicit phrases)": r"artificial intelligence|machine learning|deep learning|neural network",
    "naive \\bAI\\b (false-positive check)": r"\bAI\b",
    "remote sensing/satellite/imagery/lidar": r"remote sens|satellite|imagery|lidar|landsat|sentinel",
    "model(ing)": r"\bmodel(s|ing|ed)?\b",
    "uncertainty": r"uncertaint",
    "best available scientific information": r"best available scienti",
}


def main():
    files = glob.glob(os.path.join(ROOT, "plans", "*", "*", "*", "components.csv"))
    n, mon = 0, 0
    plans = set()
    hits = collections.Counter()
    ad = collections.Counter()
    n_ad = 0
    for f in files:
        with open(f, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                n += 1
                plans.add(row["plan_id"])
                if row["component_type"] == "monitoring":
                    mon += 1
                t = row["text"]
                for k, p in PATS.items():
                    flags = 0 if k.startswith("naive") else re.I
                    if re.search(p, t, flags):
                        hits[k] += 1
                a = row["authoritative_data"].strip()
                if a:
                    n_ad += 1
                    for x in a.split("|"):
                        ad[x.strip()] += 1
    print(f"plans={len(plans)} components={n} monitoring={mon} with_authoritative_data={n_ad}")
    for k in PATS:
        print(f"  {k}: {hits[k]}")
    print("Top authoritative data references:")
    for k, v in ad.most_common(12):
        print(f"  {v:5d}  {k}")


if __name__ == "__main__":
    main()
