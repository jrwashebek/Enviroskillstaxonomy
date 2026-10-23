#!/usr/bin/env python3
"""DC (A4) data move for S2 close-out builder B (row 39; CR-DC-001 #4; authoring aid, CI never runs it).

  python3 docs/build/S2-closeout-B/moves_dc.py dryrun    # case-sensitive lint dry run per candidate name
  python3 docs/build/S2-closeout-B/moves_dc.py apply     # move the names with a clean dry run

A product name kept in a Tool's scopeNote ("Further product names (kept out of productExamples because they are also
ordinary words; CR-DC-001): A, B.") moves into productExamples only when a case-sensitive match (the same pattern
validate_v2 now compiles for productExamples, CR-DC-001 #1) over the current L1/L2 corpus (Competency prefLabel,
statement, definition; Task statement, prefLabel; Indicator and KnowledgeStatement statement; every status, core and
modules) finds no hit at all. A hit is reported with its record so a human can tell a false positive from a true
product mention; in both cases the name stays in scopeNote (moving it would turn a true mention in another lane's
draft into an error without that lane's review). Output: generated/product_name_dryrun.csv.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import s2b_lib as S  # noqa: E402
L = S.L

TOOLS = S.DATA / "tools" / "tools.jsonl"
GEN = HERE / "generated"
SN_RX = re.compile(r"Further product names \(kept out of productExamples because they are also ordinary words; CR-DC-001\): ([^.]*)\.")
# Kept in scopeNote although the dry run is clean: names shorter than the 3-character minimum both linters apply
# (a move adds no check), and technology classes that are not products.
NOT_PRODUCT = {"blockchain": "technology class, not a product (ADR-0003 T-1: a tool class may be named)"}
MIN_LEN = 3
FIELDS = {"Competency": ["prefLabel", "statement", "definition"], "Task": ["statement", "prefLabel"],
          "Indicator": ["statement"], "KnowledgeStatement": ["statement"]}


def term_rx(term):   # identical to Validator._term_rx with cs=True
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])")


def _strings(v):
    if isinstance(v, dict):
        for x in v.values():
            yield from _strings(x)
    elif isinstance(v, list):
        for x in v:
            yield from _strings(x)
    elif isinstance(v, str):
        yield v


def corpus():
    out = []
    for base in (S.DATA / "core", S.DATA / "modules"):
        for p in base.rglob("*.yaml"):
            rec = L.load_yaml(p)
            if not isinstance(rec, dict):
                continue
            for f in FIELDS.get(rec.get("type"), []):
                for s in _strings(rec.get(f)):
                    out.append((rec["id"], rec.get("validationStatus"), f, s))
    return out


def candidates():
    rows = []
    for line in TOOLS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        m = SN_RX.search((r.get("scopeNote") or {}).get("en", ""))
        if m:
            for name in [x.strip() for x in m.group(1).split(",") if x.strip()]:
                base = re.sub(r"\s*\(.*\)$", "", name)
                rows.append((r["id"], name, base))
    return rows


def dryrun(write=True):
    texts = corpus()
    res = []
    for tid, name, base in candidates():
        rx = term_rx(base)
        hits = [(rid, vs, f, s) for rid, vs, f, s in texts if rx.search(s)]
        res.append({"tool": tid, "name": name, "match_term": base, "hits": len(hits),
                    "hit_records": "; ".join(sorted({f"{rid} ({vs}, {f})" for rid, vs, f, _ in hits}))[:600],
                    "example": (hits[0][3][:160] if hits else ""),
                    "decision": ("keep in scopeNote (shorter than the linters' 3-character minimum)" if len(base) < MIN_LEN
                                 else f"keep in scopeNote ({NOT_PRODUCT[base]})" if base in NOT_PRODUCT
                                 else "move" if not hits else "keep in scopeNote (lint hit)")})
    if write:
        GEN.mkdir(exist_ok=True)
        (GEN / "product_name_dryrun.csv").write_text(
            L.csv_text(["tool", "name", "match_term", "hits", "decision", "hit_records", "example"], res), encoding="utf-8")
    for r in res:
        print(f"{r['match_term']:>12}  hits={r['hits']:<3} {r['decision']:<18} {r['hit_records'][:150]}")
    return res


def apply():
    res = dryrun()
    move = {}
    for r in res:
        if r["decision"] == "move":
            move.setdefault(r["tool"], []).append((r["name"], r["match_term"]))
    lines = TOOLS.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        if not line.strip():
            continue
        r = json.loads(line)
        if r["id"] in move:
            m = SN_RX.search(r["scopeNote"]["en"])
            names = [x.strip() for x in m.group(1).split(",") if x.strip()]
            moved = [n for n, _ in move[r["id"]]]
            pe = list(r.get("productExamples") or [])
            for n, term in move[r["id"]]:
                if term not in pe:
                    pe.append(term)
            r["productExamples"] = pe
            rest = [n for n in names if n not in moved]
            sn = r["scopeNote"]["en"]
            if rest:
                sn = sn[:m.start()] + f"Further product names (kept out of productExamples because they are also ordinary words; CR-DC-001): {', '.join(rest)}." + sn[m.end():]
            else:
                sn = (sn[:m.start()] + sn[m.end():]).strip()
            sn = (sn + " " if sn else "") + f"Moved to productExamples after a clean case-sensitive dry run (CR-DC-001 #4, S2): {', '.join(moved)}."
            r["scopeNote"] = {"en": sn.strip()}
            ag = r["provenance"].setdefault("agent", [])
            if S.AG["DC"] not in ag:
                ag.append(S.AG["DC"])
            S.log(r["id"], "Tool", TOOLS, "move-product-names", "39")
        out.append(L.jsonl_line(r))
    TOOLS.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"moved names on {len(move)} tools: {sorted((t, [n for n, _ in v]) for t, v in move.items())}")


if __name__ == "__main__":
    {"dryrun": dryrun, "apply": apply}[sys.argv[1]]()
