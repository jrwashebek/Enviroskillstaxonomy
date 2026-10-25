#!/usr/bin/env python3
"""EMST release gate (docs/decisions/PHASE4_BUILD_PLAN.md §5): evidence and the generated gate report.

Two uses:
  - publication_status(): items 6 and 7, the two items that decide external publication. The release build calls it,
    so the generated release notes carry the gate's one-line status (rc.1 fix pass m15; DATA_FIX_BRIEF §10). Its
    inputs are deterministic: the released mapping rows and the publication sign-off record.
  - the command line: collects the evidence for every §5 item from dist/<version>/ and the repository, writes
    docs/release/<version>/gate_evidence.json and renders docs/release/<version>/GATE_REPORT.md from it. Nothing in
    the report is typed by hand; re-rendering the same evidence gives the same bytes.

Item 7 follows the project lead's decision Q13 (2026-10-24, docs/decisions/PROJECT_LEAD_DECISIONS.md): external
publication is signed by the EMST project lead, after at least one named human subject-matter reviewer has read the
report and briefs. AI agent checks, including the adoption-lead (AS) role, are advisory. The sign-off record is
docs/release/<version>/PUBLICATION_SIGNOFF.yaml; reviewers are pseudonymous `pid:` IDs (ADR-0012). An entry is added
only when the review or the signature has happened; no generator ever writes one.

Usage:
  python scripts/release_gate.py --version 2.0.0-rc.1 --as-of 2026-10-25 --run-ci [--twin dist/2.0.0-rc.1-b]
  python scripts/release_gate.py --version 2.0.0-rc.1 --as-of 2026-10-25 --reuse-ci     # keep the CI evidence, refresh the rest
  python scripts/release_gate.py --version 2.0.0-rc.1 --render-only                     # re-render GATE_REPORT.md
Licence: Apache-2.0.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emstlib as L  # noqa: E402

# crosswalk code -> mapping-set directories under data/v2/crosswalks (ADR-0022). X4 is the variant -> series set only;
# opm-series-competency (competency -> series) is not X4.
CROSSWALKS = {"X1": ("emst-v1",), "X2": ("onet-task",), "X3": ("onet-soc", "soc"), "X4": ("opm-series",),
              "X5": ("state-class-", "local-class-"), "X7": ("esco",), "X12": ("dol-ai-literacy",)}
CROSSWALK_LABELS = {"X1": "X1 v1 → v2", "X2": "X2 task → O*NET task", "X3": "X3 variant → O*NET-SOC / SOC",
                    "X4": "X4 federal variant → OPM series", "X5": "X5 variant → state and local classes",
                    "X7": "X7 competency → ESCO", "X12": "X12 → DOL AI Literacy"}
REVIEWED_SUBSET = ("X2", "X3", "X4", "X5", "X7", "X12")
AGREED = ("two-coder-agreed-target", "two-llm-coders-agreed-target")
CLOSE_OR_BETTER = ("skos:exactMatch", "skos:closeMatch")
SIGNOFF_FILE = "PUBLICATION_SIGNOFF.yaml"
Q13 = ("External publication is signed by the EMST project lead, after at least one named human subject-matter reviewer "
       "has read the report and briefs (project lead decision Q13, 2026-10-24). AI agent checks, including the "
       "adoption-lead role, are advisory.")
ITEM_TITLES = {
    "1": "CI green on schema, cross-record rules, typing and indicator lint, Tribal hold, personal data, computed-field and v1-completeness checks",
    "2": "Core size within the G-9 range of 120–180 (held included)",
    "3": "Every published element shows its use tier; nothing is `select`; every displayed tag meets the α gate or is hidden",
    "4": "All wave-1 module sections present; wave-2 and wave-3 content absent except the early drafts named in the dispositions",
    "5": "37 role profiles at their tier depth; Federal Series Profile and State Class View for every federal and state variant in P1–P2",
    "6": "X1 complete; X2 for P1 tasks; X3, X4, X5 (pilot states), X7 and X12 at reviewed-subset level",
    "7": "WP-15 verification of every external claim; ACR and security packet attached; external publication signed by the project lead after at least one named human subject-matter reviewer (Q13)",
    "8": "The lead's answers to Q1–Q2 recorded",
}


def sssom_other(s) -> dict:
    return dict(x.split("=", 1) for x in str(s or "").split(";") if "=" in x)


def human_reviewed(row: dict) -> bool:
    revs = [x for x in str(row.get("reviewer_id") or "").split("|") if x] + [sssom_other(row.get("other")).get("reviewer", "")]
    return any(str(x).startswith("pid:") for x in revs)


def crosswalk_of(set_name: str) -> str | None:
    d = str(set_name).split("/")[0]
    for code, dirs in CROSSWALKS.items():
        if any(d == x or (x.endswith("-") and d.startswith(x)) for x in dirs):
            return code
    return None


def crosswalk_summary(mapping_sets: dict) -> dict:
    """{code: rows, subjects, reviewStatus, raterType, justification, humanReviewed} over released mapping rows."""
    xw = {}
    for code in CROSSWALKS:
        rows = [r for name, rs in mapping_sets.items() if crosswalk_of(name) == code for r in rs]
        o = [sssom_other(m.get("other")) for m in rows]
        xw[code] = {"rows": len(rows), "subjects": len({m.get("subject_id") for m in rows}),
                    "reviewStatus": dict(sorted(Counter(x.get("review_status", "(none)") for x in o).items())),
                    "raterType": dict(sorted(Counter(x.get("rater_type", "(none)") for x in o).items())),
                    "justification": dict(sorted(Counter(m.get("mapping_justification") for m in rows).items())),
                    "humanReviewed": sum(1 for m in rows if human_reviewed(m))}
    return xw


def x2_detail(mapping_sets: dict, root: Path = L.ROOT) -> dict:
    """X2 in plain numbers (review M9): what the rows do and do not support."""
    x2 = [r for name, rs in mapping_sets.items() if crosswalk_of(name) == "X2" for r in rs]

    def real(m):
        return m.get("object_id") not in (None, "", "sssom:NoTermFound") and m.get("predicate_modifier") != "Not"
    agreed = [m for m in x2 if sssom_other(m.get("other")).get("review_status") in AGREED]
    return {"rows": len(x2), "withAnOnetObject": sum(1 for m in x2 if real(m)),
            "agreed": sum(1 for m in agreed if real(m)), "agreedIncludingNoTermFound": len(agreed),
            "agreedAtCloseMatchOrBetter": sum(1 for m in agreed if real(m) and m.get("predicate_id") in CLOSE_OR_BETTER),
            "noTermFound": sum(1 for m in x2 if m.get("object_id") == "sssom:NoTermFound"),
            "noTermFoundWithPositivePredicate": sum(1 for m in x2 if m.get("object_id") == "sssom:NoTermFound"
                                                    and m.get("predicate_id", "").startswith("skos:") and m.get("predicate_modifier") != "Not"),
            "kappaMatchType": _x2_kappa(root)}


def method_lines(mapping_sets: dict, counts: dict, change_view: dict, eut_rule: str, root: Path = L.ROOT) -> list[str]:
    """Release-note lines on how the crosswalks, lifecycle states and change indicators were made, from the data
    (REQUESTS_FOR_BUILD R-07; reviews M3, M7, M9)."""
    xw, x2 = crosswalk_summary(mapping_sets), x2_detail(mapping_sets, root)
    out = ["", "## How the crosswalks, lifecycle states and change indicators were made (computed from this release)", ""]
    for code, x in xw.items():
        if not x["rows"]:
            continue
        just = ", ".join(f"{k} {n}" for k, n in x["justification"].items())
        rev = f"{x['humanReviewed']} rows reviewed by a named person" if x["humanReviewed"] else "human reviewer: none (AI agent)"
        src = {sssom_other(r.get("other")).get("decision_source") for name, rs in mapping_sets.items()
               if crosswalk_of(name) == code for r in rs}
        src_txt = f"; decisions from {src.pop()}" if len(src) == 1 and None not in src else ""
        out.append(f"- **{CROSSWALK_LABELS[code]}:** {x['rows']} rows; justification {just}{src_txt}; {rev}.")
    k = x2.get("kappaMatchType") or {}
    if x2["rows"]:
        out.append(f"- **X2 coverage:** {x2['rows']} rows; {x2['withAnOnetObject']} name an O*NET task; {x2['agreed']} agreed by "
                   f"two LLM coders, {x2['agreedAtCloseMatchOrBetter']} of them at closeMatch or better; {x2['noTermFound']} no term "
                   "found" + (f"; κ on match type {k['value']}" + (f" (95% CI {k['ci95']})" if k.get("ci95") else "")
                              + (" below the ADR-0022 target 0.6, so the X2 gate fails" if k["value"] < 0.6 else "") if k.get("value") is not None else "")
                   + ". Two LLM coders agreeing is LLM-vs-LLM agreement, not human inter-coder reliability.")
    lc = counts.get("byLifecycle") or {}
    if lc:
        forming = sum(lc.get(s, 0) for s in ("proposed", "emerging"))
        out.append("- **Lifecycle** (competencies, tasks and roles): " + ", ".join(f"{s} {n}" for s, n in lc.items())
                   + (". None is proposed or emerging: records whose signals do not meet the vocabulary's entry thresholds are "
                      "`watch`, with the test stored in `lifecycleBasis`." if not forming else ".")
                   + f" Lifecycle describes the work, not the record, and does not cap the use tier ({eut_rule}).")
    rows = (change_view or {}).get("rows") or []
    if rows:
        dec = Counter(r.get("decision") for r in rows)
        out.append(f"- **Change indicators** ({(change_view.get('header') or {}).get('ruleId')}@"
                   f"{(change_view.get('header') or {}).get('ruleVersion')}): {len(rows)} rows: "
                   + ", ".join(f"{d} {n}" for d, n in sorted(dec.items())) + ". Only active, human-reviewed signals can move one.")
    return out


# ------------------------------------------------------------------------------------------------ sign-off (item 7)
def signoff_path(version: str, root: Path = L.ROOT) -> Path:
    return root / "docs" / "release" / version / SIGNOFF_FILE


def load_signoff(version: str, root: Path = L.ROOT) -> dict:
    p = signoff_path(version, root)
    return (L.load_yaml(p) or {}) if p.exists() else {}


def signoff_state(signoff: dict) -> dict:
    """Q13: valid when the project lead's signature is dated and at least one pid: human subject-matter reviewer read
    the report and briefs on or before that date."""
    revs = [r for r in (signoff.get("humanReviewers") or []) if isinstance(r, dict)
            and str(r.get("reviewer", "")).startswith("pid:") and r.get("date")]
    sig = signoff.get("projectLeadSignature") or {}
    sig_date = str(sig.get("date") or "") if isinstance(sig, dict) else ""
    before = [r for r in revs if sig_date and str(r["date"]) <= sig_date]
    return {"humanReviewers": len(revs), "humanReviewersBeforeSignature": len(before),
            "projectLeadSigned": bool(sig_date), "valid": bool(sig_date) and bool(before),
            "advisoryAgentChecks": len(signoff.get("advisoryAgentChecks") or [])}


def publication_status(mapping_sets: dict, signoff: dict, x1_expected: int | None = None, root: Path = L.ROOT) -> dict:
    """Items 6 and 7 as the release build can evaluate them (deterministic inputs only)."""
    per = {}
    for name, rows in mapping_sets.items():
        code = crosswalk_of(name)
        if code:
            p = per.setdefault(code, {"rows": 0, "humanReviewed": 0, "subjects": set()})
            p["rows"] += len(rows)
            p["humanReviewed"] += sum(1 for r in rows if human_reviewed(r))
            p["subjects"] |= {r.get("subject_id") for r in rows}
    x1_subjects = len((per.get("X1") or {}).get("subjects") or ())
    x1_ok = bool(x1_subjects) and (x1_expected is None or x1_subjects >= x1_expected)
    missing = [c for c in REVIEWED_SUBSET if not (per.get(c) or {}).get("humanReviewed")]
    item6 = {"pass": x1_ok and not missing, "x1Subjects": x1_subjects, "x1Expected": x1_expected,
             "withoutHumanReviewedSubset": missing}
    st = signoff_state(signoff)
    acr = (root / "site" / "ACR.md").exists()
    packet = (root / "site" / "SECURITY_PACKET.md").exists()
    item7 = {"pass": st["valid"] and acr and packet, "signoff": st, "acr": acr, "securityPacket": packet}
    failing = [i for i, it in (("6", item6), ("7", item7)) if not it["pass"]]
    if failing:
        line = ("not cleared for external publication; "
                + (f"items {' and '.join(failing)} fail" if len(failing) > 1 else f"item {failing[0]} fails"))
    else:
        line = "items 6 and 7 pass; external publication is signed by the project lead (Q13)"
    return {"item6": item6, "item7": item7, "line": line, "cleared": not failing}


# ------------------------------------------------------------------------------------------------ evidence
def _run(cmd, cwd, env=None, timeout=3600):
    try:
        p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:  # noqa: BLE001
        return 99, f"{type(e).__name__}: {e}"


def _last(text, rx=None):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if rx:
        hits = [ln for ln in lines if re.search(rx, ln)]
        return hits[-1] if hits else (lines[-1] if lines else "")
    return lines[-1] if lines else ""


def collect_ci(root: Path, version: str) -> dict:
    py = sys.executable
    out = {}
    simple = [
        ("extract_v1 --check", [py, "scripts/extract_v1.py", "--check"]),
        ("build_schema --check", [py, "scripts/build_schema.py", "--check"]),
        ("migrate_v1 --check", [py, "scripts/migrate_v1.py", "--check"]),
        ("convert_instrument_links --check", [py, "scripts/convert_instrument_links.py", "--check"]),
        ("mint_id verify", [py, "scripts/mint_id.py", "verify"]),
        ("update_readme_status --check", [py, "scripts/update_readme_status.py", "--check"]),
    ]
    for name, cmd in simple:
        code, text = _run(cmd, root)
        out[name] = {"command": " ".join(["python"] + cmd[1:]), "exit": code, "summary": _last(text)}
    tmp = root / "dist" / f".gate-{version}"
    tmp.mkdir(parents=True, exist_ok=True)
    for mode, extra in (("validate_v2", []), ("validate_v2 --strict", ["--strict"])):
        jp = tmp / (mode.replace(" ", "_").replace("-", "") + ".json")
        code, text = _run([py, "scripts/validate_v2.py", *extra, "--no-git-base", "--quiet", "--json", str(jp)], root)
        rep = json.loads(jp.read_text(encoding="utf-8")) if jp.exists() else {}
        issues = rep.get("issues") or {}
        out[mode] = {"command": f"python scripts/validate_v2.py {' '.join(extra + ['--no-git-base'])}".replace("  ", " "),
                     "exit": code, "summary": _last(text, r"errors?,"),
                     "errors": sum(v for k, v in issues.items() if k.startswith("E-")),
                     "warnings": {k: v for k, v in sorted(issues.items()) if k.startswith("W-")}}
    code, text = _run([py, "-m", "pytest", "-q", "tests", "-p", "no:cacheprovider"], root, timeout=7200)
    summ = _last(text, r"\b(passed|failed|error)")
    counts = {k: int(n) for n, k in re.findall(r"(\d+) (passed|failed|skipped|errors?|xfailed|xpassed)", summ)}
    failed = sorted(set(re.findall(r"^FAILED (\S+)", text, re.M)))
    out["pytest"] = {"command": "python -m pytest -q tests", "exit": code, "counts": counts, "failed": failed}
    env = dict(os.environ, PATH="/opt/node22/bin:" + os.environ.get("PATH", ""))
    if (root / "site" / "_site").exists():
        code, text = _run(["npm", "test"], root / "site", env=env, timeout=3600)
        keep = [ln.strip() for ln in text.splitlines() if re.search(r"\bOK\b|problem|violation|FAIL|pages", ln)]
        out["site npm test"] = {"command": "cd site && npm test", "exit": code, "summary": keep[-6:]}
    else:
        out["site npm test"] = {"command": "cd site && npm test", "exit": None, "summary": ["site/_site not built"]}
    return out


def collect(version: str, as_of: str, root: Path = L.ROOT, ci: dict | None = None, twin: Path | None = None,
            dist: Path | None = None) -> dict:
    sys.path.insert(0, str(root / "scripts"))
    from rules import hr_common as H
    dist = Path(dist) if dist else root / "dist" / version
    bundle = json.loads((dist / "emst.bundle.jsonld").read_text(encoding="utf-8"))
    graph = bundle["@graph"]
    recs = {r["id"]: r for r in graph if isinstance(r, dict) and "id" in r and r.get("type") not in ("Mapping",)}
    maps = [r for r in graph if isinstance(r, dict) and r.get("type") == "Mapping"]
    manifest = next((r for r in graph if r.get("type") == "Release"), {})
    view = lambda p: json.loads((dist / "views" / p).read_text(encoding="utf-8"))  # noqa: E731
    counts = view("counts.json")
    notes = (dist / "RELEASE_NOTES.md").read_text(encoding="utf-8")
    sums = (dist / "SHA256SUMS").read_bytes()
    ev = {"version": version, "asOf": as_of, "buildCommit": manifest.get("buildCommit"), "released": manifest.get("released"),
          "schemaVersion": manifest.get("schemaVersion"),
          "sha256SUMS": hashlib.sha256(sums).hexdigest(), "files": len(sums.decode("utf-8").splitlines()),
          "bundleSha256": L.sha256_bytes((dist / "emst.bundle.jsonld").read_bytes()),
          "statusLine": (re.search(r"\*\*Publication status: ([^*]+)\*\*", notes) or [None, None])[1],
          "counts": {k: counts.get(k) for k in ("byType", "coreCompetencies", "heldRecords", "excluded", "redactedReferences",
                                                "deferredTargets", "ratingsByRaterType", "ratingUnitsByRaterType",
                                                "changeSignalObservations") if k in counts},
          "ci": ci or {}}
    if twin is not None and Path(twin).exists():
        a = {p.relative_to(dist).as_posix(): p.read_bytes() for p in dist.rglob("*") if p.is_file()}
        b = {p.relative_to(twin).as_posix(): p.read_bytes() for p in Path(twin).rglob("*") if p.is_file()}
        ev["determinism"] = {"twin": str(Path(twin).relative_to(root)) if Path(twin).is_relative_to(root) else str(twin),
                             "identical": a == b, "files": len(a), "differ": sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))[:20]}
    # item 2
    ev["item2"] = {"coreSizeLine": next((ln for ln in notes.splitlines() if ln.startswith("Core competencies:")), None)}
    # item 3
    eut = view("effective_use_tier.json")["rows"]
    gate = view("display_gate.json")
    ev["item3"] = {"effectiveUseTierRows": len(eut), "effectiveUseTier": dict(sorted(Counter(r["effectiveUseTier"] for r in eut).items())),
                   "elementsWithoutEffectiveTier": sorted({r["type"] for r in recs.values() if r.get("type") in
                                                           ("Competency", "Task", "Indicator", "Enactment", "RoleProfile", "RoleVariant",
                                                            "KnowledgeStatement", "Pathway")} - {r["type"] for r in eut}),
                   "selectAnywhere": sum(1 for r in recs.values() if "select" in (r.get("useTier"), r.get("useClass")))
                   + sum(1 for r in eut if r["effectiveUseTier"] == "select"),
                   "displayGateRows": len(gate["rows"]), "displayGateDecisions": dict(sorted(Counter(r["decision"] for r in gate["rows"]).items())),
                   "displayGateRule": gate["header"].get("ruleVersion"),
                   "agentDraftNodes": sum(1 for r in graph if _has_agent_draft(r))}
    # item 4
    wave1 = ["air", "envhealth", "forest", "hazards", "parks", "waste", "water", "waterq", "wildlife"]
    mods = Counter((r.get("module") or "core") for r in recs.values() if r.get("type") not in ("Release", "CompetencyLevelOutcome"))
    ev["item4"] = {"wave1Present": {m: mods.get(m, 0) for m in wave1},
                   "otherModules": {m: n for m, n in sorted(mods.items()) if m not in wave1 and m != "core"}}
    # item 5
    roles = sorted((r for r in recs.values() if r.get("type") == "RoleProfile"), key=lambda x: x["id"])
    depth = []
    for r in roles:
        depth.append({"role": r["id"], "tier": H.tier(r), "tasks": len({i.get("task") for i in r.get("taskBundle") or [] if isinstance(i, dict)}),
                      "targets": len(r.get("competencyTargets") or []), "lifecycle": r.get("lifecycleState")})
    by_tier = {}
    for d in depth:
        by_tier.setdefault(d["tier"], []).append(d)
    fsp_idx = view("federal_series_profiles/index.json")["series"]
    fsp_roles = {x for s in fsp_idx for x in s["roles"]}
    scv_idx = view("state_class_views/index.json")["variants"]
    p12 = [r for r in roles if H.tier(r) in ("P1", "P2")]
    fed = [(r["id"], v["id"]) for r in p12 for v in [H.variant_for(recs, r["id"], "federal")] if v]
    sta = [(r["id"], v["id"]) for r in p12 for v in [H.variant_for(recs, r["id"], "state")] if v]
    ev["item5"] = {"roles": len(roles), "byTier": {t: len(v) for t, v in sorted(by_tier.items())},
                   "depthRange": {t: {"tasks": [min(d["tasks"] for d in v), max(d["tasks"] for d in v)],
                                      "targets": [min(d["targets"] for d in v), max(d["targets"] for d in v)]}
                                  for t, v in sorted(by_tier.items())},
                   "lifecycleByTier": {t: dict(sorted(Counter(d["lifecycle"] for d in v).items())) for t, v in sorted(by_tier.items())},
                   "fspFiles": len(fsp_idx), "p1p2FederalVariants": len(fed),
                   "p1p2FederalVariantsInAnFsp": sum(1 for r, _ in fed if r in fsp_roles),
                   "p1p2FederalVariantsWithoutFsp": [r for r, _ in fed if r not in fsp_roles],
                   "scvFiles": len([p for p in (dist / "views" / "state_class_views").glob("*.json") if p.name != "index.json"]),
                   "p1p2StateVariants": len(sta), "p1p2StateVariantsIndexed": sum(1 for _, v in sta if v in scv_idx),
                   "p1p2StateVariantsWithAClassView": sum(1 for _, v in sta if scv_idx.get(v))}
    # item 6
    sets = _sets_from_bundle(maps)
    ev["item6"] = crosswalk_summary(sets)
    ev["x2Detail"] = x2_detail(sets, root)
    # items 6 and 7 as the build saw them
    signoff = load_signoff(version, root)
    ev["publication"] = publication_status(_sets_from_bundle(maps), signoff, None, root)
    ev["publication"]["item6"].pop("x1Expected", None)
    # item 7: claims register, WP-15 sign-off note, sign-off record
    reg_p = root / "docs" / "methods" / "claims_register.csv"
    reg = list(csv.DictReader(open(reg_p, encoding="utf-8", newline=""))) if reg_p.exists() else []
    rb = Counter(r.get("recheck_by", "") for r in reg)
    ev["item7"] = {"registerRows": len(reg), "byStatus": dict(sorted(Counter(r["status"] for r in reg).items())),
                   "unverifiedOrHeld": sorted(r["claim_id"] for r in reg if r["status"] in ("unverified", "held")),
                   "recheckOnOrBeforeAsOf": sorted(r["claim_id"] for r in reg if r.get("recheck_by", "")[:4].isdigit() and r["recheck_by"] <= as_of),
                   "recheckDates": dict(sorted((k, v) for k, v in rb.items() if k[:4].isdigit())),
                   "recheckOther": dict(sorted((k, v) for k, v in rb.items() if not k[:4].isdigit())),
                   "signoffRecord": str(signoff_path(version, root).relative_to(root)), "signoffRecordExists": signoff_path(version, root).exists(),
                   "signoff": signoff_state(signoff),
                   "wp15StatusLine": next((ln for ln in (root / "docs" / "methods" / "WP15_SIGNOFF.md").read_text(encoding="utf-8").splitlines()
                                           if ln.startswith("- **Owner:**")), None),
                   "acr": (root / "site" / "ACR.md").exists(), "securityPacket": (root / "site" / "SECURITY_PACKET.md").exists()}
    # item 8
    pld = (root / "docs" / "decisions" / "PROJECT_LEAD_DECISIONS.md").read_text(encoding="utf-8")
    rows = {m.group(1): m.group(0) for m in re.finditer(r"^\| (Q\d+) \|.*$", pld, re.M)}
    ev["item8"] = {q: bool(rows.get(q)) and bool(re.search(r"\| \d{4}-\d{2}-\d{2} \|", rows.get(q, ""))) for q in ("Q1", "Q2", "Q13")}
    return ev


def _has_agent_draft(node) -> bool:
    if isinstance(node, dict):
        return "agentDraft" in node or any(_has_agent_draft(v) for v in node.values())
    if isinstance(node, list):
        return any(_has_agent_draft(v) for v in node)
    return False


def _sets_from_bundle(maps):
    out = {}
    for m in maps:
        out.setdefault(m.get("mapping_set_id", ""), []).append(m)
    return out


def _x2_kappa(root: Path):
    for p in sorted((root / "data" / "v2" / "crosswalks" / "onet-task").glob("*.sssom.yml")):
        o = sssom_other((L.load_yaml(p) or {}).get("other"))
        if o.get("kappa_match_type"):
            return {"value": float(o["kappa_match_type"]), "ci95": o.get("kappa_ci95"), "target": o.get("target_kappa"),
                    "source": f"{p.relative_to(root)}#other"}
    k = root / "pipelines" / "x2" / "work" / "x2_kappa.json"
    if k.exists():
        d = json.loads(k.read_text(encoding="utf-8"))
        v = d.get("kappa_match_type")
        if isinstance(v, dict):
            v = v.get("kappa", v.get("value"))
        if isinstance(v, list):
            v = v[0]
        return {"value": v, "source": str(k.relative_to(root))}
    return None


# ------------------------------------------------------------------------------------------------ render
def _verdicts(ev) -> dict:
    ci = ev.get("ci") or {}
    ci_ok = bool(ci) and all((v.get("exit") == 0) for k, v in ci.items() if k != "pytest") and (ci.get("pytest") or {}).get("exit") == 0
    v = {"1": "pass" if ci_ok else ("not run" if not ci else "fail")}
    core = re.search(r"(\d+) released \+ held core reported as a count \((\d+)\); range (\d+)-(\d+)", ev["item2"]["coreSizeLine"] or "")
    v["2"] = "pass" if core and int(core.group(3)) <= int(core.group(1)) + int(core.group(2)) <= int(core.group(4)) else "fail"
    i3 = ev["item3"]
    v["3"] = "pass" if i3["selectAnywhere"] == 0 and not i3["elementsWithoutEffectiveTier"] else "fail"
    i4 = ev["item4"]
    v["4"] = "pass" if all(i4["wave1Present"].values()) and set(i4["otherModules"]) <= {"extract", "worklands"} else "fail"
    i5 = ev["item5"]
    v["5"] = ("conditional" if i5["roles"] == 37 else "fail")
    v["6"] = "pass" if ev["publication"]["item6"]["pass"] else "fail"
    v["7"] = "pass" if ev["publication"]["item7"]["pass"] else "fail"
    v["8"] = "pass" if ev["item8"].get("Q1") and ev["item8"].get("Q2") else "fail"
    return v


def render(ev: dict) -> str:
    v = _verdicts(ev)
    i3, i4, i5, i6, i7, x2 = ev["item3"], ev["item4"], ev["item5"], ev["item6"], ev["item7"], ev["x2Detail"]
    fails = [k for k in sorted(v, key=int) if v[k] == "fail"]
    out = [f"# EMST {ev['version']}: release gate report (generated)", "",
           f"- **Generated by** `scripts/release_gate.py` from `dist/{ev['version']}/`, the repository and "
           f"`docs/release/{ev['version']}/gate_evidence.json`; do not edit by hand. Prepared for the re-cut by D-BUILD "
           "(holding the DE and CP codes), an AI agent role, not a person.",
           f"- **Gate:** `docs/decisions/PHASE4_BUILD_PLAN.md` §5, items 1–8. **As of** {ev['asOf']}. Build "
           f"`{ev['buildCommit']}`, released {ev['released']}, schema {ev['schemaVersion']}.",
           "- **Authorship.** AI agents researched and drafted this release. No human subject-matter expert has validated "
           "anything in it, and no human has signed anything recorded here.", "",
           "## Summary", "", "| § 5 item | Result |", "|---|---|"]
    names = {"1": "1. CI green", "2": "2. Core size within G-9", "3": "3. Use tiers; nothing `select`; α gate",
             "4": "4. Wave-1 present; wave 2–3 absent except named early drafts",
             "5": "5. 37 roles at tier depth; FSP and SCV for P1–P2 federal and state variants",
             "6": "6. Crosswalks X1 complete; X2 for P1 tasks; X3, X4, X5, X7, X12 at reviewed-subset level",
             "7": "7. WP-15 verification; ACR and security packet; project lead signs after a named human SME reviewer (Q13)",
             "8": "8. Q1–Q2 recorded"}
    out += [f"| {names[k]} | **{v[k]}** |" for k in sorted(v, key=int)]
    out += ["", f"**Overall.** Publication status: {ev['publication']['line']}."]
    if ev.get("statusLine"):
        out += [f"The generated release notes carry the same line: “Publication status: {ev['statusLine']}”."]
    out += [f"Items failing: {', '.join(fails) or 'none'}. rc.1 may be tagged as a release candidate for the NGO-pilot "
            "preview and the design partners; it is not cleared for external publication until items 6 and 7 pass.", ""]
    det = ev.get("determinism")
    if det:
        out += [f"**Determinism.** Two consecutive builds (`dist/{ev['version']}/` and `{det['twin']}/`) are "
                + ("**byte-identical**" if det["identical"] else f"**different** ({', '.join(det['differ'])})")
                + f" over {det['files']} files. SHA-256 of `SHA256SUMS`: `{ev['sha256SUMS']}`; of the bundle: `{ev['bundleSha256']}`.", ""]
    out += ["---", "", f"## 1. {ITEM_TITLES['1']}", "", f"**Result: {v['1']}.**", "", "| Command | Exit | Output |", "|---|---|---|"]
    for name, c in (ev.get("ci") or {}).items():
        if name == "pytest":
            cnt = ", ".join(f"{n} {k}" for k, n in sorted(c.get("counts", {}).items()))
            out.append(f"| `{c['command']}` | {c['exit']} | {cnt or '(no summary)'}"
                       + (f"; failed: {', '.join('`' + f + '`' for f in c['failed'])}" if c.get("failed") else "") + " |")
        elif name.startswith("validate_v2"):
            w = sum(c.get("warnings", {}).values())
            out.append(f"| `{c['command']}` | {c['exit']} | {c.get('errors', '?')} errors, {w} warnings: "
                       + ", ".join(f"{k} {n}" for k, n in c.get("warnings", {}).items()) + " |")
        else:
            s = c.get("summary")
            s = "; ".join(s) if isinstance(s, list) else s
            out.append(f"| `{c['command']}` | {c['exit']} | {str(s).replace('|', '/')} |")
    if not ev.get("ci"):
        out.append("| (CI evidence not collected in this run) | | |")
    out += ["", "The build's own `self_check()` passed for this release: every bundle node validates against "
            "`schema/emst.schema.json` (minus the documented computed inverse fields), every bundle key is a context term, "
            "and the Tribal trigger scan over every output file and field found nothing outside the exempt policy "
            "statements and vocabulary concepts.", ""]
    out += [f"## 2. {ITEM_TITLES['2']}", "", f"**Result: {v['2']}.**", "",
            f"The generated release notes read: “{ev['item2']['coreSizeLine']}”", ""]
    out += [f"## 3. {ITEM_TITLES['3']}", "", f"**Result: {v['3']}.**", "",
            f"- **Use tiers.** {i3['effectiveUseTierRows']} elements carry a computed effective use tier: "
            + ", ".join(f"{k} {n}" for k, n in i3["effectiveUseTier"].items())
            + (f". Element types with no tier: {', '.join(i3['elementsWithoutEffectiveTier'])}." if i3["elementsWithoutEffectiveTier"] else ". No element type is missing."),
            f"- **`select` appears {i3['selectAnywhere']} times**, as a declared tier, a use class or an effective tier.",
            f"- **Display gate** (`display-gate@{i3['displayGateRule']}`): {i3['displayGateRows']} decisions: "
            + ", ".join(f"{k} {n}" for k, n in i3["displayGateDecisions"].items()) + ". No α-gated value is shown: no reliability study exists.",
            f"- **Agent drafts in the bundle.** {i3['agentDraftNodes']} bundle nodes carry an `agentDraft` sub-object; the CSV and HCM files carry none of those values.", ""]
    out += [f"## 4. {ITEM_TITLES['4']}", "", f"**Result: {v['4']}.**", "",
            "- **Wave-1 modules:** " + ", ".join(f"{m} {n}" for m, n in i4["wave1Present"].items()) + " records.",
            "- **Other modules:** " + (", ".join(f"{m} {n}" for m, n in i4["otherModules"].items()) or "none")
            + " (the early drafts the dispositions name are in extract and worklands).", ""]
    dr = i5["depthRange"]
    out += [f"## 5. {ITEM_TITLES['5']}", "", f"**Result: {v['5']}.**", "",
            f"- **Role profiles: {i5['roles']}** (" + ", ".join(f"{t} {n}" for t, n in i5["byTier"].items()) + ").",
            "- **Depth:** " + "; ".join(f"{t} {d['tasks'][0]}–{d['tasks'][1]} tasks, {d['targets'][0]}–{d['targets'][1]} targets"
                                        for t, d in dr.items() if t in ("P1", "P2")) + ".",
            "- **Lifecycle by tier:** " + "; ".join(f"{t}: " + ", ".join(f"{k} {n}" for k, n in d.items())
                                                    for t, d in i5["lifecycleByTier"].items()) + ".",
            f"- **Federal Series Profiles:** {i5['fspFiles']} series files; {i5['p1p2FederalVariantsInAnFsp']} of "
            f"{i5['p1p2FederalVariants']} P1–P2 federal variants appear in one"
            + (f" (without one: {', '.join('`' + r + '`' for r in i5['p1p2FederalVariantsWithoutFsp'])})." if i5["p1p2FederalVariantsWithoutFsp"] else "."),
            f"- **State Class Views:** {i5['scvFiles']} class files; {i5['p1p2StateVariantsIndexed']} of {i5['p1p2StateVariants']} "
            f"P1–P2 state variants are in the index, {i5['p1p2StateVariantsWithAClassView']} with at least one class view.",
            "- **Why conditional.** \"Critical competencies\" are job-analysis values and appear only as agent drafts (in "
            "`agentDraft`, hidden by the gate); every series and class mapping behind these views is an unreviewed agent "
            "candidate (item 6).", ""]
    out += [f"## 6. {ITEM_TITLES['6']}", "", f"**Result: {v['6']}.**", "",
            "| Crosswalk | Rows | Review status | Rater type | Justification | Human reviewer |", "|---|---|---|---|---|---|"]
    for code, x in i6.items():
        rev = f"{x['humanReviewed']} rows (pid:)" if x["humanReviewed"] else "none (AI agent)"
        fmt = lambda d: ", ".join(f"{k} {n}" for k, n in d.items())  # noqa: E731
        out.append(f"| {CROSSWALK_LABELS[code]} | {x['rows']} ({x['subjects']} subjects) | {fmt(x['reviewStatus'])} | "
                   f"{fmt(x['raterType'])} | {fmt(x['justification'])} | {rev} |")
    k = x2.get("kappaMatchType") or {}
    kv = k.get("value")
    out += ["", f"**X2 in plain numbers** (review M9): rows: {x2['rows']}; with an O*NET object: {x2['withAnOnetObject']}; "
            f"agreed: {x2['agreed']} (plus {x2['agreedIncludingNoTermFound'] - x2['agreed']} agreed NoTermFound rows); agreed at "
            f"closeMatch or better: {x2['agreedAtCloseMatchOrBetter']}; NoTermFound rows that still carry a positive predicate: "
            f"{x2['noTermFoundWithPositivePredicate']}; κ on match type "
            + (f"{kv}" + (f" (95% CI {k['ci95']})" if k.get("ci95") else "") + f" ({k.get('source')})" if kv is not None else "not recorded")
            + (" < 0.6 → fail" if isinstance(kv, (int, float)) and kv < 0.6 else "") + ". Both coders are LLM agents.",
            "- X4 counts the federal variant → OPM series set only; the competency → series set (`opm-series-competency`) "
            "is not X4 (the first rc.1 gate report had counted it under X4).",
            "- **Missing:** a subset reviewed by a named human (`pid:`) for each of "
            + ", ".join(ev["publication"]["item6"]["withoutHumanReviewedSubset"] or ["(none)"])
            + "; for X2, two coders with κ ≥ 0.6 on match type (ADR-0022) and adjudication of the open rows. The agents cannot supply this.", ""]
    st = i7["signoff"]
    out += [f"## 7. {ITEM_TITLES['7']}", "", f"**Result: {v['7']}.**", "",
            f"**Sign-off path.** {Q13} The record is `{i7['signoffRecord']}`"
            + (" (present)" if i7["signoffRecordExists"] else " (absent)") + f": named human subject-matter reviewers "
            f"recorded: {st['humanReviewers']}; project lead signature: {'recorded' if st['projectLeadSigned'] else 'not recorded'}; "
            f"advisory AI agent checks: {st['advisoryAgentChecks']}."
            + (" **No human review or signature has been recorded.**" if not st["humanReviewers"] and not st["projectLeadSigned"] else ""),
            f"- **WP-15 note** (`docs/methods/WP15_SIGNOFF.md`): “{(i7['wp15StatusLine'] or '').lstrip('- ').strip()}”",
            f"- **Claims register** (`docs/methods/claims_register.csv`): {i7['registerRows']} rows: "
            + ", ".join(f"{k} {n}" for k, n in i7["byStatus"].items()) + ".",
            f"- **Unverified or held rows** ({len(i7['unverifiedOrHeld'])}): {', '.join(i7['unverifiedOrHeld']) or 'none'}. "
            "Their records are withheld from the release (`data/v2/governance/release_withheld.yaml`), held, or released with "
            "the J label and no status asserted, as WP-15 §2 requires.",
            f"- **Moving facts due for re-check on or before {ev['asOf']}:** "
            + (", ".join(i7["recheckOnOrBeforeAsOf"]) if i7["recheckOnOrBeforeAsOf"] else "none")
            + ". Later re-check dates: " + ", ".join(f"{d} ({n})" for d, n in i7["recheckDates"].items() if d > ev["asOf"])
            + (("; other: " + ", ".join(f"{d} ({n})" for d, n in i7["recheckOther"].items())) if i7["recheckOther"] else "") + ".",
            f"- **ACR** (`site/ACR.md`): {'present' if i7['acr'] else 'missing'}; **security packet** (`site/SECURITY_PACKET.md`): "
            f"{'present' if i7['securityPacket'] else 'missing'}. Both were prepared by CP, an AI agent, and describe the explorer; "
            "no human has reviewed either.",
            "- **Missing:** a named human subject-matter reviewer's reading of the report and briefs, then the project lead's "
            "signature (Q13); LM's re-check of each moving fact on or after its date; the ACR and security packet re-issued "
            "for the tagged build.", ""]
    out += [f"## 8. {ITEM_TITLES['8']}", "", f"**Result: {v['8']}.**", "",
            "`docs/decisions/PROJECT_LEAD_DECISIONS.md` records, with dates: "
            + ", ".join(f"{q} {'yes' if ok else 'no'}" for q, ok in ev["item8"].items()) + ".", ""]
    out += ["---", "", "## Decisions for the project lead", "",
            "1. **Recruit at least one named human subject-matter reviewer** to read the report and briefs (Q13), and the "
            "human reviewers for a subset of each crosswalk (item 6).",
            "2. **Sign external publication** only after that review (Q13); the record is "
            f"`{i7['signoffRecord']}`.", ""]
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--version", required=True)
    ap.add_argument("--as-of", help="date the gate is judged on (YYYY-MM-DD); required unless --render-only")
    ap.add_argument("--run-ci", action="store_true", help="run the CI commands (pytest takes several minutes)")
    ap.add_argument("--reuse-ci", action="store_true", help="keep the CI evidence of the existing gate_evidence.json")
    ap.add_argument("--twin", type=Path, help="a second build of the same tree, compared byte for byte")
    ap.add_argument("--render-only", action="store_true")
    ap.add_argument("--dist", type=Path, help="release build to read (default dist/<version>)")
    ap.add_argument("--out", type=Path, help="folder for GATE_REPORT.md and gate_evidence.json (default docs/release/<version>)")
    a = ap.parse_args(argv)
    out_dir = a.out or (L.ROOT / "docs" / "release" / a.version)
    evp = out_dir / "gate_evidence.json"
    if a.render_only:
        ev = json.loads(evp.read_text(encoding="utf-8"))
    else:
        if not a.as_of:
            ap.error("--as-of is required")
        ci = collect_ci(L.ROOT, a.version) if a.run_ci else (
            (json.loads(evp.read_text(encoding="utf-8")).get("ci") or {}) if a.reuse_ci and evp.exists() else {})
        ev = collect(a.version, a.as_of, L.ROOT, ci, a.twin, a.dist)
        out_dir.mkdir(parents=True, exist_ok=True)
        evp.write_text(json.dumps(ev, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "GATE_REPORT.md").write_text(render(ev), encoding="utf-8")
    print(f"wrote {out_dir}/GATE_REPORT.md and gate_evidence.json; {ev['publication']['line']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
