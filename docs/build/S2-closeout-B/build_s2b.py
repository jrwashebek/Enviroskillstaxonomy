#!/usr/bin/env python3
"""S2 close-out builder B: write the records for the content work orders (authoring aid; CI never runs it).

  python3 docs/build/S2-closeout-B/build_s2b.py <module> [<module> ...]     # e.g. content_db content_lc
  python3 docs/build/S2-closeout-B/build_s2b.py --check <module>            # local word/count checks only

Each content module defines SPECS (competency specs, see s2b_lib.build) and may define ENACTMENTS and PATCHES
(callables run after SPECS). Writes are guarded by s2b_lib.put / patch (never overwrites another lane's authored
record). After a run: scripts/migrate_v1.py --x1-only, then scripts/validate_v2.py.
"""
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import s2b_lib as S  # noqa: E402


def run(modname, check_only=False):
    m = importlib.import_module(modname)
    errs = []
    for c in getattr(m, "SPECS", []):
        errs += S.check_words(c)
    if errs:
        print("\n".join(errs))
        raise SystemExit(f"{modname}: {len(errs)} local check failures")
    if check_only:
        print(f"{modname}: local checks pass")
        return
    for c in getattr(m, "SPECS", []):
        S.build(c, c["row"])
        for e in c.get("enactments", []):
            rec = S.enactment(e["id"], c["id"], e["module"], e["label"], e["note"], e.get("roles", c["roles"]),
                              e["subsectors"], position=e.get("position"), tasks=e.get("tasks"),
                              variants=e.get("variants"), instruments=e.get("instruments"), editorial=e.get("editorial"))
            S.put(rec, e["module"], c["row"])
        print(f"{c['id']}: written")
    for fn in getattr(m, "PATCHES", []):
        fn()
        print(f"patch {fn.__name__}: done")


if __name__ == "__main__":
    args = sys.argv[1:]
    chk = "--check" in args
    for a in [x for x in args if x != "--check"]:
        run(a, chk)
