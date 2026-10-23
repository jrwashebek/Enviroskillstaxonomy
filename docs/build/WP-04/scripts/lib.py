"""WP-04 (A4, DC) record builder helpers. Writes EMST v2 draft records using the repo's canonical YAML dumper."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

REPO = Path("/home/claude/emst")
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402

DATA = REPO / "data" / "v2"
CORE = DATA / "core"
AGENT = "emstagent:A4-DC@wp-04"
MODEL = "claude-opus-5-5"
PROMPT = "wp04-dc-authoring@1"
GEN_AT = "2026-10-23T14:00:00Z"
REVIEW_BY_EMERGING = "2028-10-23"
WRITTEN: list[str] = []


def prov(evidence="J", sources=None, derived=None, adr=None, confidence=None):
    p = {"method": "llm-assisted", "agent": [AGENT], "generatedAt": GEN_AT, "toolVersion": MODEL,
         "promptVersion": PROMPT, "evidenceLabel": evidence, "reviewStatus": "unreviewed"}
    if derived:
        p["derivedFrom"] = derived
    if sources:
        p["sources"] = sorted(set(sources))
    if confidence:
        p["confidence"] = confidence
    p["adr"] = adr or ["ADR-0003", "ADR-0025"]
    return p


def df(v1key, relation, note=None):
    d = {"v1Key": v1key, "relation": relation}
    if note:
        d["note"] = note
    return d


def path_for(rid: str, kind: str, area: str = "core") -> Path:
    base = CORE if area == "core" else DATA / "modules" / area
    return base / kind / (L.id_to_stem(rid) + ".yaml")


KIND = {"Competency": "competencies", "Task": "tasks", "Indicator": "indicators", "Enactment": "enactments",
        "KnowledgeStatement": "knowledge"}


def write(rec: dict, kind: str | None = None, area: str = "core"):
    p = path_for(rec["id"], kind or KIND[rec["type"]], area)
    L.write_yaml(p, rec)
    WRITTEN.append(str(p.relative_to(REPO)))
    return p


def load(rid: str, kind: str, area: str = "core") -> dict:
    return L.load_yaml(path_for(rid, kind, area))


BASE_COMMIT = "e2bbdd2"   # last commit before WP-04 edits; holds the WP-02 migrated v1 seeds
ORIG = Path(__file__).resolve().parent / "orig"


def load_orig(rid: str, kind: str, area: str = "core") -> dict:
    """The migrated v1 seed as WP-02 wrote it (idempotent re-runs of in-place rewrites)."""
    import subprocess
    p = path_for(rid, kind, area)
    rel = p.relative_to(REPO)
    cache = ORIG / rel
    if not cache.exists():
        txt = subprocess.run(["git", "show", f"{BASE_COMMIT}:{rel}"], cwd=REPO, capture_output=True, text=True, check=True).stdout
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(txt, encoding="utf-8")
    return L.load_yaml(cache)


def lm(s):
    return {"en": s}


# ------------------------------------------------------------------ competency
def competency(cid, title, definition, statement, ctype, span, levels, *, cluster=None, lifecycle="established",
               evidence="J", sources=None, derived=None, alt=None, notation=None, note=None, reusability=None,
               enactments=None, scope=None, adr=None, use_tier="develop"):
    rec = {"id": cid, "type": "Competency", "prefLabel": lm(title)}
    if alt:
        rec["altLabel"] = {"en": alt} if isinstance(alt, list) else {"en": [alt]}
    rec["definition"] = lm(definition)
    rec["statement"] = lm(statement)
    if scope:
        rec["scopeNote"] = lm(scope)
    # ADR-0029 (CR-LM-001 ruling): no EMST-* notation schemes from candidate on -> keep the candidate ID in the note.
    interim = [n for n in (notation or []) if n["scheme"].startswith("EMST-")]
    notation = [n for n in (notation or []) if not n["scheme"].startswith("EMST-")]
    for n in interim:
        tag = f"Candidate ID {n['value']} (candidate_disposition.csv)."
        note = tag + (" " + note if note else "")
    if note:
        rec["editorialNote"] = lm(note)
    if notation:
        rec["notation"] = notation
    rec["competencyType"] = ctype
    if cluster:
        rec["transversalCluster"] = cluster
    rec["levelSpan"] = {"min": span[0], "max": span[1]}
    rec["levels"] = [{"level": lv, "indicators": ids} for lv, ids in levels]
    # Competency.enactments is a computed inverse (ADR-0029 §1.2): never stored; enactments point to the competency.
    rec["homeModule"] = "core"
    if reusability:
        rec["reusability"] = reusability
    rec.update({"layer": "L1", "module": "core", "status": "draft", "lifecycleState": lifecycle, "useTier": use_tier,
                "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public"})
    if lifecycle in ("watch", "proposed", "emerging"):
        rec["reviewBy"] = REVIEW_BY_EMERGING
    rec["provenance"] = prov(evidence, sources, derived, adr)
    return rec


def rewrite_seed_competency(cid, title, definition, statement, ctype, span, levels, *, cluster=None,
                            lifecycle="established", evidence="J", sources=None, extra_derived=None, alt=None,
                            note=None, reusability=None, enactments=None, scope=None, adr=None, keep_v1seed=False):
    """Edit a migrated v1 seed in place (AUTHORING_GUIDE §6)."""
    old = load_orig(cid, "competencies")
    derived = []
    for d in old["provenance"].get("derivedFrom", []):
        d = copy.deepcopy(d)
        if d.get("relation") == "carried":
            d["relation"] = "rewritten"
        elif d.get("relation") == "recovered":
            d["relation"] = "reference-only"
            d.setdefault("note", "v1 text restored from source text was consulted; no v1 wording is carried")
        derived.append(d)
    for d in extra_derived or []:
        if not any(x["v1Key"] == d["v1Key"] for x in derived):
            derived.append(d)
    prev_note = (old.get("editorialNote") or {}).get("en", "")
    rec = competency(cid, title, definition, statement, ctype, span, levels, cluster=cluster, lifecycle=lifecycle,
                     evidence=evidence, sources=sources, derived=derived, alt=alt, notation=old.get("notation"),
                     note=(note + " " if note else "") + prev_note, reusability=reusability, enactments=enactments,
                     scope=scope, adr=(adr or ["ADR-0003", "ADR-0011"]))
    for k in ("v1Domain", "v1SkillArea"):
        if k in old:
            rec[k] = old[k]
    if keep_v1seed and "v1Seed" in old:
        rec["v1Seed"] = old["v1Seed"]
    return rec


# ------------------------------------------------------------------ task
def task(tid, statement, supports, wf, field, formation, *, modes=None, profiles=None, regime=None, lifecycle="established",
         evidence="J", sources=None, derived=None, note=None, accountability=None, adr=None, notation=None,
         v1tier=None, v1domain=None, v1area=None, rel=None):
    n = L.word_count(statement)
    assert 8 <= n <= 30, (tid, n, statement)
    rec = {"id": tid, "type": "Task", "prefLabel": lm(statement), "statement": lm(statement),
           "textSha256": L.text_sha256(statement)}
    if note:
        rec["editorialNote"] = lm(note)
    if notation:
        rec["notation"] = notation
    sup = []
    for s in supports:
        if isinstance(s, str):
            sup.append({"competency": s, "strength": "primary"})
        else:
            sup.append({"competency": s[0], "strength": s[1]})
    rec["supports"] = sup
    rec["workFunction"] = wf
    if modes:
        rec["modes"] = modes
    if rel:
        rec["relationshipTypes"] = rel
    if profiles:
        rec["workflowProfiles"] = profiles
    rec["fieldDependency"] = field
    rec["formationDependency"] = formation
    if regime:
        rec["reproductionRegime"] = regime
    if accountability:
        rec["accountabilityConstraint"] = {"required": True, "basis": accountability}
    rec["homeModule"] = "core"
    rec.update({"layer": "L2", "module": "core", "status": "draft", "lifecycleState": lifecycle, "useTier": "develop",
                "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public"})
    if lifecycle in ("watch", "proposed", "emerging"):
        rec["reviewBy"] = REVIEW_BY_EMERGING
    if v1tier:
        rec["v1Tier"] = v1tier
    if v1domain:
        rec["v1Domain"] = v1domain
    if v1area:
        rec["v1SkillArea"] = v1area
    rec["provenance"] = prov(evidence, sources, derived, adr or ["ADR-0003"])
    return rec


def rewrite_seed_task(tid, statement, supports, wf, field, formation, **kw):
    old = load_orig(tid, "tasks")
    derived = []
    for d in old["provenance"].get("derivedFrom", []):
        d = copy.deepcopy(d)
        if d.get("relation") == "carried":
            d["relation"] = "rewritten"
        derived.append(d)
    note = kw.pop("note", None)
    prev = (old.get("editorialNote") or {}).get("en", "")
    rec = task(tid, statement, supports, wf, field, formation, derived=derived, notation=old.get("notation"),
               v1tier=old.get("v1Tier"), v1domain=old.get("v1Domain"), v1area=old.get("v1SkillArea"),
               note=((note + " ") if note else "") + prev, adr=kw.pop("adr", ["ADR-0003", "ADR-0011"]), **kw)
    return rec


# ------------------------------------------------------------------ indicator
METHODS = {"ws": "work-sample", "sews": "seeded-error-work-sample", "bars": "structured-interview-bars",
           "sjt": "situational-judgment-test", "sim": "simulation-role-play", "tbo": "task-book-observation",
           "brm": "blind-re-measurement", "pt": "prediction-test", "ra": "record-audit", "md": "moot-defense",
           "pr": "portfolio-review", "kt": "knowledge-test"}
MODES = {"u": "unaided", "a": "assisted", "s": "supervisory"}
ATTR = {"aut": "ATT-AUT", "gui": "ATT-GUI", "cpx": "ATT-CPX", "sco": "ATT-SCO", "kno": "ATT-KNO", "aug": "ATT-AUG",
        "for": "ATT-FOR"}


def indicator(iid, comp, level, statement, mode, methods, tasks=None, *, obs4=3, use="develop", attr=None,
              jv=False, evidence_types=None, evidence_plan=None, safety=False, lifecycle="established", label=None):
    n = L.word_count(statement)
    assert n <= 30, (iid, n, statement)
    rec = {"id": iid, "type": "Indicator", "prefLabel": lm(label or _short(statement)), "competency": comp,
           "level": level, "statement": lm(statement), "augmentationMode": MODES[mode],
           "assessmentMethods": [METHODS[m] for m in methods], "useClass": use, "obs4": obs4}
    if evidence_types:
        rec["evidenceTypes"] = evidence_types
    if obs4 == 2 and use == "develop":
        rec["evidencePlan"] = lm(evidence_plan or "Double-code OBS-4 on a work-sample pilot (spec_gold_sets.md) before develop use; the observable product is named in the statement.")
    rec["jurisdictionVariable"] = jv
    if tasks:
        rec["servedTasks"] = tasks
    if attr:
        rec["distinguishingAttribute"] = ATTR[attr]
    if safety:
        rec["safetyOrLegalCritical"] = True
    rec.update({"layer": "L1", "module": "core", "status": "draft", "lifecycleState": lifecycle, "useTier": use,
                "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public"})
    if lifecycle in ("watch", "proposed", "emerging"):
        rec["reviewBy"] = REVIEW_BY_EMERGING
    rec["provenance"] = prov("J", adr=["ADR-0004", "ADR-0025"])
    return rec


def _short(s: str) -> str:
    s = s.rstrip(".")
    words = s.split()
    return " ".join(words[:14]) + ("…" if len(words) > 14 else "")


# ------------------------------------------------------------------ enactment
def craft_enactment(eid, comp, craft, title, note, *, indicator_variants=None, additional_tasks=None,
                    derived=None, lifecycle="emerging", sources=None, evidence="J", editorial=None):
    rec = {"id": eid, "type": "Enactment", "prefLabel": lm(title)}
    if editorial:
        rec["editorialNote"] = lm(editorial)
    rec.update({"competency": comp, "enactmentKind": "craft", "craft": craft})
    if additional_tasks:
        rec["additionalTasks"] = additional_tasks
    if indicator_variants:
        rec["indicatorVariants"] = indicator_variants
    rec["note"] = lm(note)
    rec.update({"layer": "L1", "module": "core", "status": "draft", "lifecycleState": lifecycle, "useTier": "develop",
                "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public"})
    if lifecycle in ("watch", "proposed", "emerging"):
        rec["reviewBy"] = REVIEW_BY_EMERGING
    rec["provenance"] = prov(evidence, sources, derived, ["ADR-0025", "ADR-0005"])
    return rec


# ------------------------------------------------------------------ build helper for a competency bundle
class Bundle:
    """Collects one competency's indicators by level so the competency record lists them."""

    def __init__(self, cid, prefix):
        self.cid, self.prefix, self.inds, self.by_level = cid, prefix, [], {}
        self.counter = {}

    def ind(self, level, statement, mode, methods, tasks=None, **kw):
        n = self.counter.get(level, 0)
        self.counter[level] = n + 1
        iid = f"seed:{self.prefix}-{level.lower()}-{'abcde'[n]}"
        rec = indicator(iid, self.cid, level, statement, mode, methods, tasks, **kw)
        self.inds.append(rec)
        self.by_level.setdefault(level, []).append(iid)
        return iid

    def levels(self):
        return [(lv, self.by_level[lv]) for lv in ("L1", "L2", "L3", "L4", "L5") if lv in self.by_level]

    def write_indicators(self):
        for r in self.inds:
            write(r, "indicators")
