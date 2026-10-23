#!/usr/bin/env python3
"""One-off repair (S2 close-out B, 2026-10-23 ~17:55): restore the v1 lineage that a re-run of build_s2b.py dropped
from in-place seed rewrites (coordinator note; DE Batch 2). For every Competency and Task in manifest.csv whose last
`validationStatus: seed-v1` version exists in git (or, failing that, in the session's pre-edit index), the seed's
derivedFrom entries (with their v1 keys, table, sheet, row, fields and workbook SHA; `carried` -> `rewritten`),
notation and v1 facets are merged back into the current record. Entries added since are kept. Idempotent.

  python3 docs/build/S2-closeout-B/repair_lineage.py [--dry]
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import s2b_lib as S  # noqa: E402
L = S.L


def git_seed_version(rel):
    try:
        hashes = subprocess.run(["git", "-C", str(S.REPO), "log", "--format=%h", "--", rel], capture_output=True,
                                text=True, check=True).stdout.split()
    except subprocess.CalledProcessError:
        return None
    for h in hashes:
        r = subprocess.run(["git", "-C", str(S.REPO), "show", f"{h}:{rel}"], capture_output=True, text=True)
        if r.returncode != 0:
            continue
        rec = L.load_yaml_text(r.stdout)
        if isinstance(rec, dict) and rec.get("validationStatus") == "seed-v1":
            return rec
    return None


def converted(seed, typ):
    own = None
    for n in seed.get("notation") or []:
        if n.get("scheme") == "EMSTv1":
            own = f"v1:{n['value']}"
    out = []
    for d in (seed.get("provenance") or {}).get("derivedFrom") or []:
        d = dict(d)
        if d.get("relation") == "carried" and (typ == "Task" or d.get("v1Key") == own):
            d["relation"] = "rewritten"
        out.append(d)
    return out


def main(dry=False):
    rows = [r for r in L.read_csv(HERE / "manifest.csv") if r["type"] in ("Competency", "Task")
            and r["action"] in ("rewrite-seed", "rewrite-own")]   # records I rewrote, never ones I only patched
    fixed = []
    for r in rows:
        p = S.REPO / r["path"]
        if not p.exists():
            continue
        cur = L.load_yaml(p)
        if cur.get("validationStatus") == "seed-v1":
            continue
        seed = git_seed_version(r["path"])
        if seed is None:
            continue
        lineage = converted(seed, cur["type"])
        prov = cur["provenance"]
        have = prov.get("derivedFrom") or []
        key = lambda x: (x.get("v1Key"), x.get("relation"), x.get("v1Table"))  # noqa: E731
        seed_keys = {key(x) for x in lineage}
        # drop bare duplicates of seed entries (same v1Key and relation, fewer fields), keep everything else
        rest = [x for x in have if key(x) not in seed_keys and
                not any(x.get("v1Key") == y.get("v1Key") and x.get("relation") == y.get("relation") and set(x) < set(y) for y in lineage)]
        new = lineage + rest
        changed = new != have
        if changed:
            # rebuild provenance with derivedFrom in its canonical place
            np_ = {}
            for k, v in prov.items():
                if k == "derivedFrom":
                    continue
                np_[k] = v
                if k == "promptVersion":
                    np_["derivedFrom"] = new
            if "derivedFrom" not in np_:
                np_["derivedFrom"] = new
            cur["provenance"] = np_
        for k in (["notation", "v1Domain", "v1SkillArea"] + (["v1Tier"] if cur["type"] == "Task" else [])):
            if seed.get(k) and not cur.get(k):
                cur[k] = seed[k]
                changed = True
        if changed:
            fixed.append((cur["id"], len(have), len(new)))
            if not dry:
                L.write_yaml(p, cur)
    for f in fixed:
        print(f"{f[0]}: derivedFrom {f[1]} -> {f[2]}")
    print(f"{len(fixed)} records repaired{' (dry run)' if dry else ''}")


if __name__ == "__main__":
    main("--dry" in sys.argv)
