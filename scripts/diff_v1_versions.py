#!/usr/bin/env python3
"""Cell-by-cell diff of the five v1 database workbooks along their lineage.

    python scripts/diff_v1_versions.py

Lineage (by content, see docs/audit/data-audit.md section 1):
    v1  skills_taxonomy_workforce_v1.xlsx                         215 competencies, no exposure columns
    v1u skills_taxonomy_workforce_v1_updated.xlsx                 + Task 13 exposure columns (25)
    v3  20260223_SkillsTaxonomy_Core_V3.xlsx                      + Domain 7 (7 comps), CLD Severity, tier rule
    v3rA 20260223_..._reconciled (copyA)                          + D6 exposure reconciled, Pre-Task 15A
    v3rB 20260223_..._reconciled (copyB, latest upload)           + Data Dictionary lens-status notes

Writes data/v1_baseline/version_diffs.csv (one row per differing cell / added row / added column) and
data/v1_baseline/version_summary.csv (counts per step, sheet, column, change type).
Keys: Competency Code for competency sheets; Competency Code + Proficiency Level for Proficiency Indicators;
Skill Area Code for Structure Summary; row number for free-form sheets (Workforce Signals, Labor Market
Crosswalk, Data Dictionary). Values are compared after light normalization (strip, int-valued floats -> int,
TRUE/FALSE case) so that type noise is not reported as change.
"""
from __future__ import annotations

import csv
import io
from collections import Counter, OrderedDict
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "legacy" / "v1" / "data"
OUT = ROOT / "data" / "v1_baseline"
VERSIONS = OrderedDict([
    ("v1", "skills_taxonomy_workforce_v1.xlsx"),
    ("v1u", "skills_taxonomy_workforce_v1_updated.xlsx"),
    ("v3", "20260223_SkillsTaxonomy_Core_V3.xlsx"),
    ("v3rA", "20260223_SkillsTaxonomy_Core_V3_reconciled__copyA_995a86e4.xlsx"),
    ("v3rB", "20260223_SkillsTaxonomy_Core_V3_reconciled__copyB_aaf34c8c.xlsx"),
])
KEYED = OrderedDict([("Competencies", ["Competency Code"]), ("Dimension Tags", ["Competency Code"]),
                     ("Profession Family View", ["Competency Code"]),
                     ("Proficiency Indicators", ["Competency Code", "Proficiency Level"]),
                     ("Structure Summary", ["Skill Area Code"])])
FREEFORM = ["Workforce Signals", "Labor Market Crosswalk", "Data Dictionary"]


def norm(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    s = str(v).strip()
    if not s:
        return None
    return s.capitalize() if s.upper() in ("TRUE", "FALSE") else s


def load(fname):
    wb = openpyxl.load_workbook(LEGACY / fname, read_only=True, data_only=True)
    return {ws.title: [[norm(c) for c in r] for r in ws.iter_rows(values_only=True)] for ws in wb.worksheets}


def keyed(rows, keycols):
    hdr = rows[0]
    idx = [hdr.index(k) for k in keycols]
    out = OrderedDict()
    for r in rows[1:]:
        if all(c is None for c in r):
            continue
        out[" / ".join(r[i] or "" for i in idx)] = {h: (r[j] if j < len(r) else None) for j, h in enumerate(hdr) if h}
    return [h for h in hdr if h], out


def diff_pair(a, b, A, B):
    rows = []
    for sheet, kc in KEYED.items():
        ha, da = keyed(A[sheet], kc)
        hb, db = keyed(B[sheet], kc)
        for col in hb:
            if col not in ha:
                n = sum(1 for r in db.values() if r.get(col) is not None)
                rows.append(dict(step=f"{a}->{b}", sheet=sheet, key="*", column=col, change_type="column_added",
                                 from_value=None, to_value=f"{n} non-empty values"))
        for col in ha:
            if col not in hb:
                rows.append(dict(step=f"{a}->{b}", sheet=sheet, key="*", column=col, change_type="column_removed",
                                 from_value=None, to_value=None))
        for k in db:
            if k not in da:
                rows.append(dict(step=f"{a}->{b}", sheet=sheet, key=k, column="*", change_type="row_added",
                                 from_value=None, to_value=db[k].get("Competency Title") or db[k].get("Skill Area Name")))
        for k in da:
            if k not in db:
                rows.append(dict(step=f"{a}->{b}", sheet=sheet, key=k, column="*", change_type="row_removed",
                                 from_value=da[k].get("Competency Title"), to_value=None))
        common = [c for c in ha if c in hb]
        for k in da:
            if k not in db:
                continue
            for c in common:
                va, vb = da[k].get(c), db[k].get(c)
                if va == vb:
                    continue
                ct = "filled" if va is None else "cleared" if vb is None else "changed"
                rows.append(dict(step=f"{a}->{b}", sheet=sheet, key=k, column=c, change_type=ct,
                                 from_value=va, to_value=vb))
    for sheet in FREEFORM:
        ra, rb = A[sheet], B[sheet]
        for i in range(max(len(ra), len(rb))):
            x = [c for c in (ra[i] if i < len(ra) else []) if c is not None]
            y = [c for c in (rb[i] if i < len(rb) else []) if c is not None]
            if x != y:
                rows.append(dict(step=f"{a}->{b}", sheet=sheet, key=f"row {i + 1}", column="*",
                                 change_type="row_changed" if x and y else ("row_added" if y else "row_removed"),
                                 from_value=" | ".join(x) or None, to_value=" | ".join(y) or None))
    return rows


def write(path, rows, cols):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in cols})
    path.write_text(buf.getvalue(), encoding="utf-8")


def main():
    data = {v: load(f) for v, f in VERSIONS.items()}
    names = list(VERSIONS)
    rows = []
    for a, b in zip(names, names[1:]):
        rows += diff_pair(a, b, data[a], data[b])
    rows += diff_pair("v1u", "v3rB", data["v1u"], data["v3rB"])   # authoritative-per-change-log vs baseline
    for r in rows:
        if r["step"] == "v1u->v3rB":
            r["step"] = "v1u->v3rB (direct)"
    write(OUT / "version_diffs.csv", rows, ["step", "sheet", "key", "column", "change_type", "from_value", "to_value"])
    summ = Counter((r["step"], r["sheet"], r["column"], r["change_type"]) for r in rows)
    srows = [dict(step=s, sheet=sh, column=c, change_type=ct, n=n) for (s, sh, c, ct), n in summ.items()]
    write(OUT / "version_summary.csv", srows, ["step", "sheet", "column", "change_type", "n"])
    per_step = Counter(r["step"] for r in rows)
    for s, n in per_step.items():
        print(f"{s:22s} {n:6d} differences")


if __name__ == "__main__":
    main()
