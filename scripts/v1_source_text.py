"""Parse the v1 source competency text (20251202_SkillsTaxonomy_Core_V2 (1).txt) into records.

The text is the document the v1 Excel database was imported from. It mixes several house styles (plain,
inline, markdown-ish `*Knowledge*:` and `#Job Tasks:`, bulleted `* Knowledge:`), so the parser is tolerant
and reports what it could not find rather than guessing. Used by scripts/extract_v1.py to cross-check the
database against its source.
"""
from __future__ import annotations

import re
from pathlib import Path

LEVEL_NAMES = ["FOUNDATIONAL", "INTERMEDIATE", "ADVANCED", "EXPERT"]
SECTOR_LABELS = ["Public Agencies", "Private Sector", "NGOs", "Consulting", "Academia"]

HDR = re.compile(r"^[\s#*]*([1-6])\.(\d{1,2})\.(\d{1,2})[\s:.*]+(\S.*)$")
SA_HDR = re.compile(r"^[\s#*]*([1-6])\.(\d{1,2})\s+([A-Z][A-Z&,/()\- ]+?)\s*(\(NEW\))?\s*$")
DOM_HDR = re.compile(r"^DOMAIN ([1-6]):")
LEVEL_RE = re.compile(r"^[\s#*]*(FOUNDATIONAL|INTERMEDIATE|ADVANCED|EXPERT)\b\s*(\([^)]*\))?[\s:*]*(.*)$")
TASKS_RE = re.compile(r"^[\s#*]*Job Tasks\s*:?\**\s*(.*)$", re.I)
PROF_RE = re.compile(r"^[\s#*]*Proficiency Levels", re.I)
SECTOR_HDR = re.compile(r"^[\s#*]*Sector[- ]Specific Applications", re.I)
SECTOR_LINE = re.compile(r"^[\s#*\-]*(" + "|".join(re.escape(s) for s in SECTOR_LABELS) + r")\**\s*:\s*\**\s*(.*)$")
BREAK = re.compile(r"^\s*(---+|_{5,})\s*$")


def _clean(s: str | None) -> str | None:
    if s is None:
        return None
    s = re.sub(r"\*([A-Za-z]+)\*", r"\1", s)        # *Knowledge* -> Knowledge
    s = re.sub(r"^[\s*#•\-–]+", "", s)               # leading bullets / markdown
    s = re.sub(r"[\s*]+$", "", s)                    # trailing bullet of the next line
    s = re.sub(r"\s+", " ", s).strip()
    return s or None


def _split_kai(text: str):
    """Split 'Knowledge: .. Application: .. Indicators: ..' (any subset) into parts."""
    t = re.sub(r"\*(Knowledge|Application|Indicators)\*", r"\1", text)
    parts = {}
    for m in re.finditer(r"(Knowledge|Application|Indicators)\s*\**\s*:\s*(.*?)(?=(?:\*\s*)?(?:Knowledge|Application|Indicators)\s*\**\s*:|$)",
                         t, re.S):
        parts[m.group(1).lower()] = _clean(m.group(2))
    return parts


def parse(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    # 1) locate competency headers: first header per code that is followed by "Job Tasks" within 20 lines
    heads = []
    seen = set()
    for i, ln in enumerate(lines):
        m = HDR.match(ln)
        if not m:
            continue
        code = f"{m.group(1)}.{int(m.group(2))}.{int(m.group(3))}"
        if code in seen:
            continue
        window = "\n".join(lines[i:i + 20])
        if not re.search(r"Job Tasks", window, re.I):
            continue
        seen.add(code)
        heads.append((i, code, m.group(4)))
    sa_heads = []
    for i, ln in enumerate(lines):
        m = SA_HDR.match(ln)
        if m and int(m.group(2)) < 20:
            sa_heads.append((i, f"{m.group(1)}.{int(m.group(2))}", m.group(3).strip(), bool(m.group(4))))
    dom_lines = [i for i, ln in enumerate(lines) if DOM_HDR.match(ln)]
    stops = sorted({h[0] for h in heads} | {s[0] for s in sa_heads} | set(dom_lines) | {len(lines)})

    comps, tasks, profs, inds, sectors, problems = [], [], [], [], [], []
    for i, code, rest in heads:
        end = next(s for s in stops if s > i)
        block = lines[i:end]
        rec = dict(code=code, source_line=i + 1, header_text=_clean(rest), title=None, description=None)
        # title / description: header line, then non-empty lines until Job Tasks
        pre = []
        j = 1
        while j < len(block) and not TASKS_RE.match(block[j]):
            if block[j].strip() and not BREAK.match(block[j]):
                pre.append(block[j])
            j += 1
        rec["description_lines"] = " ".join(_clean(p) or "" for p in pre).strip() or None
        # tasks
        tlist = []
        k = j + 1
        if j < len(block):
            inline = TASKS_RE.match(block[j]).group(1)
            if inline:
                for m in re.finditer(r"(\d)\.\s+(.*?)(?=\s\d\.\s|$)", inline):
                    tlist.append(_clean(m.group(2)))
        while k < len(block) and len(tlist) < 3 and not PROF_RE.match(block[k]) and not LEVEL_RE.match(block[k]):
            m = re.match(r"^[\s#*]*(\d)[.)]\s+(.*)$", block[k])
            if m:
                tlist.append(_clean(m.group(2)))
            k += 1
        for n, t in enumerate(tlist, start=1):
            tasks.append(dict(code=code, task_n=n, text=t))
        rec["n_tasks"] = len(tlist)
        # proficiency levels
        lv_idx = [(x, LEVEL_RE.match(block[x])) for x in range(len(block)) if LEVEL_RE.match(block[x])]
        sec_idx = next((x for x in range(len(block)) if SECTOR_HDR.match(block[x])), None)
        found_levels = []
        for n, (x, m) in enumerate(lv_idx):
            lname = m.group(1)
            if lname in found_levels:
                continue
            found_levels.append(lname)
            nxt = [y for y, _ in lv_idx if y > x]
            stop = min(nxt[0] if nxt else len(block), sec_idx if (sec_idx and sec_idx > x) else len(block))
            seg = [m.group(3)] + block[x + 1:stop]
            # Knowledge / Application may be inline or on their own lines; indicators follow "Indicators:"
            text_before_ind, ind_lines, in_ind = [], [], False
            for s in seg:
                if in_ind:
                    if BREAK.match(s):
                        break
                    if s.strip():
                        ind_lines.append(s)
                    continue
                mi = re.search(r"\*?Indicators\*?\s*:\s*(.*)$", s)
                if mi:
                    text_before_ind.append(s[:mi.start()])
                    in_ind = True
                    if mi.group(1).strip():
                        ind_lines.append(mi.group(1))
                else:
                    text_before_ind.append(s)
            parts = _split_kai(" ".join(text_before_ind))
            indicators = [c for c in (_clean(x) for x in ind_lines) if c and not SECTOR_LINE.match(c)]
            profs.append(dict(code=code, level=lname.lower(), level_label=_clean(m.group(2)),
                              knowledge=parts.get("knowledge"), application=parts.get("application"),
                              n_indicators=len(indicators)))
            for q, t in enumerate(indicators, start=1):
                inds.append(dict(code=code, level=lname.lower(), indicator_n=q, text=t))
        rec["levels_found"] = "|".join(l.lower() for l in found_levels)
        # sectors
        lab = "|".join(re.escape(x) for x in SECTOR_LABELS)
        for s in block:
            if SECTOR_LINE.match(s):
                for m in re.finditer(r"(" + lab + r")\**\s*:\s*(.*?)(?=\s*(?:" + lab + r")\**\s*:|$)", s):
                    sectors.append(dict(code=code, sector_label=m.group(1), text=_clean(m.group(2))))
        if len(tlist) != 3:
            problems.append(dict(code=code, problem=f"found {len(tlist)} tasks"))
        if len(found_levels) != 4:
            problems.append(dict(code=code, problem=f"found levels {found_levels}"))
        comps.append(rec)
    skill_areas = [dict(skill_area_code=c, name=n, marked_new=new, source_line=i + 1) for i, c, n, new in sa_heads]
    return dict(competencies=comps, tasks=tasks, proficiency=profs, indicators=inds, sectors=sectors,
                skill_areas=skill_areas, problems=problems, n_lines=len(lines))
