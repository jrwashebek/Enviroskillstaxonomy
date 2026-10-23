"""Parse the per-task AI/robotics exposure working records (Task 12/13/14) from legacy/v1/docs/.

These records are the only place where most per-task exposure *rationale* lives. Formats:
- markdown tables  | Code | Competency | Task | Task Description | Auto | Tacit | Career | Vector | Horizon | Notes |
  (domain1/3/5_task13_exposure_classification.md, domain4_task12_working_record.md)
- fixed-width text with a confidence code [C]/[R]/[I] (d2_sa*.txt)
- per-competency prose blocks "- T1 (...): H / Hi / P / — / N" (domain7_task14_tagging_record.txt)
Used by scripts/extract_v1.py; returns plain dict rows.
"""
from __future__ import annotations

import re
from pathlib import Path

MD_FILES = {
    "domain1_task13_exposure_classification.md": "d1_record",
    "domain3_task13_exposure_classification.md": "d3_record",
    "domain4_task12_working_record.md": "d4_record",
    "domain5_task13_exposure_classification.md": "d5_record",
}
D2_GLOB = "d2_sa*.txt"
D7_FILE = "domain7_task14_tagging_record.txt"

MD_ROW = re.compile(r"^\|\s*\**([1-7]\.\d{1,2}\.\d{1,2})\**\s*\|")
D2_ROW = re.compile(r"^([1-7]\.\d{1,2}\.\d{1,2})\s+(T[123])\s+(.+?)\s{2,}(Ac|A|H|V|S)\s+(Hi|Med|Lo)\s+(P|C|X)\s+"
                    r"(AI|Ro|Cv|—|-)\s+([123N])\s+(\S+)\s+(\S+)\s+\[(C|R|I)\]\s*(.*)$")
D7_HEAD = re.compile(r"^###\s+([1-7]\.\d\.\d)\s+—")
D7_TEXT = re.compile(r"^-\s+T([123]):\s+(.*)$")
D7_CLASS = re.compile(r"^-\s+T([123])\s+\((.*?)\):\s*(\S+)\s*/\s*(\S+)\s*/\s*(\S+)\s*/\s*(\S+)\s*/\s*(\S+)")


def _cell(s):
    s = re.sub(r"\*\*", "", s or "").strip()
    return s or None


def parse_md(path: Path, source: str):
    rows = []
    for i, ln in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if not MD_ROW.match(ln):
            continue
        cells = [_cell(c) for c in ln.strip().strip("|").split("|")]
        if len(cells) < 10 or not re.match(r"^T[123]$", cells[2] or ""):
            continue
        desc = cells[3] or ""
        inferred = "[source-inferred]" in desc.lower()
        desc = re.sub(r"\s*\[source-inferred\]\s*", " ", desc, flags=re.I).strip()
        rows.append(dict(source=source, source_file=path.name, source_row=i, code=cells[0], task=cells[2],
                         source_task_text=desc, auto_type=cells[4], tacit_density=cells[5], career_ladder=cells[6],
                         vector=cells[7], horizon=cells[8], rationale=" | ".join(c for c in cells[9:] if c) or None,
                         confidence=None, source_inferred=inferred))
    return rows


def parse_d2(path: Path):
    rows = []
    for i, ln in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        m = D2_ROW.match(ln.rstrip())
        if not m:
            continue
        g = m.groups()
        rows.append(dict(source="d2_record", source_file=path.name, source_row=i, code=g[0], task=g[1],
                         source_task_text=g[2].strip(), auto_type=g[3], tacit_density=g[4], career_ladder=g[5],
                         vector=g[6], horizon=g[7], rationale=g[11] or None, confidence=g[10],
                         source_inferred=None, cld_marker=g[8], s_traj_marker=g[9]))
    return rows


D2_COMP = re.compile(r"^COMPETENCY\s+([1-7]\.\d{1,2}\.\d{1,2})\s+—")
D2_TASK = re.compile(r"^Task\s+([123]):\s+(.*)$")
D2_DIM = {"Auto Type": "auto_type", "Tacit Density": "tacit_density", "Career Ladder": "career_ladder",
          "Vector": "vector", "Time Horizon": "horizon"}


def parse_d2_blocks(path: Path):
    """SA 2.4-2.7 files: 'COMPETENCY 2.4.1 — ...' blocks with a vertical dimension table."""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    rows = []
    prov, conf = None, "R"
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("PROVENANCE:"):
            buf = [ln]
            j = i + 1
            while j < len(lines) and lines[j].strip():
                buf.append(lines[j].strip())
                j += 1
            prov = " ".join(buf)
            conf = "C-auto/R-other" if "Auto Type sequences CONFIRMED" in prov else "R"
        m = D2_COMP.match(ln)
        if m:
            code = m.group(1)
            texts, dims, notes = {}, {}, []
            start = i
            j = i + 1
            while j < len(lines) and not D2_COMP.match(lines[j]) and not lines[j].startswith("====="):
                l2 = lines[j]
                mt = D2_TASK.match(l2)
                if mt:
                    texts[mt.group(1)] = mt.group(2).strip()
                elif "|" in l2 and l2.split("|")[0].strip() in D2_DIM:
                    parts = [x.strip() for x in l2.split("|")]
                    dims[D2_DIM[parts[0]]] = parts[1:4]
                elif l2.strip() and not l2.startswith("---") and not l2.startswith("Dimension") and dims:
                    notes.append(l2.strip())
                j += 1
            for k in range(3):
                if all(d in dims and len(dims[d]) > k for d in D2_DIM.values()):
                    rows.append(dict(source="d2_record", source_file=path.name, source_row=start + 1, code=code,
                                     task=f"T{k + 1}", source_task_text=texts.get(str(k + 1)),
                                     **{d: dims[d][k] for d in D2_DIM.values()},
                                     rationale=" ".join(notes)[:2000] or None, confidence=conf,
                                     source_inferred=None))
            i = j
            continue
        i += 1
    return rows


def parse_d7(path: Path):
    rows, texts = [], {}
    code = None
    for i, ln in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        m = D7_HEAD.match(ln)
        if m:
            code = m.group(1)
            continue
        if code is None:
            continue
        m = D7_CLASS.match(ln)
        if m:
            t, short, a, ta, c, v, h = m.groups()
            rows.append(dict(source="d7_record", source_file=path.name, source_row=i, code=code, task=f"T{t}",
                             source_task_text=texts.get((code, t)) or short, auto_type=a, tacit_density=ta,
                             career_ladder=c, vector=v, horizon=h, rationale=None, confidence=None,
                             source_inferred=None))
            continue
        m = D7_TEXT.match(ln)
        if m and (code, m.group(1)) not in texts:
            texts[(code, m.group(1))] = m.group(2).strip()
    return rows


TOKEN = re.compile(r"^(Ac|A|H|V|S|Hi|Med|Lo|P|C|X|AI|Ro|Cv|—|-|1|2|3|N)(?![A-Za-z])")


def _normalize(r):
    """Reduce cells like 'Ac ★ confirmed' to the code; remember a star as a confirmation marker."""
    star = False
    for d in ("auto_type", "tacit_density", "career_ladder", "vector", "horizon"):
        v = (r.get(d) or "").strip()
        star = star or "★" in v
        m = TOKEN.match(v)
        r[d] = ("none" if m.group(1) in ("—", "-") else m.group(1)) if m else (v or None)
    if star and r.get("confidence") in (None, "R"):
        r["confidence"] = "C-star"
    return r


def parse_all(docs: Path):
    out, missing = [], []
    for fname, src in MD_FILES.items():
        p = docs / fname
        if p.exists():
            out += parse_md(p, src)
        else:
            missing.append(fname)
    d2 = sorted(docs.glob(D2_GLOB))
    if not d2:
        missing.append(D2_GLOB)
    for p in d2:
        out += parse_d2(p) + parse_d2_blocks(p)
    p = docs / D7_FILE
    if p.exists():
        out += parse_d7(p)
    else:
        missing.append(D7_FILE)
    return [_normalize(r) for r in out], missing
