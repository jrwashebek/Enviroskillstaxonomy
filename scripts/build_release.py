#!/usr/bin/env python3
"""Build EMST release artifacts deterministically from the source records (WP-01; SPEC §17.2; ADR-0010 §1).

Outputs in --out (default dist/<version>/):
  emst.bundle.jsonld          normative JSON-LD bundle (records sorted by id; context inlined)
  csv/*.csv + datapackage.json  CSV + Frictionless data package: competencies, tasks, indicators, task links,
                              HCM skills-library import file, mappings (flattened), release delta feed
  emst.skos.ttl               SKOS: every vocab/ concept scheme + released competencies/tasks; mapping triples only for
                              rows a pid: human reviewed (none in rc.1). Agent-drafted mappings and their provenance
                              (rater_type, review_status in `other`) are in the bundle and SSSOM only (M11)
  sssom/<set>.sssom.tsv (+.yml)  mapping sets as released (held rows redacted; unreleased successors -> NoTermFound)
  sssom/strict-1.0/<set>.sssom.tsv  generated SSSOM 1.0-strict rendering (1.1-only justifications -> UnspecifiedMatching)
  views/*.json                computed views, each row stamped ruleId/ruleVersion/buildCommit from the active rule file
                              in vocab/rules/ (ADR-0021; ADR-0029 §4): counts, inverse_links, effective_use_tier,
                              assessment_staleness, change_indicators, display_gate, venue_applicability;
                              views/agreement/<study>.json (ADR-0030 adds the CLO nodes and the HR views)
  RELEASE_NOTES.md            generated counts; held items reported only as a count
  delta.json                  added/changed/superseded/withdrawn IDs vs --previous bundle
  delta_v1.json               delta against the v1 baseline: every ID added; per v1 key, decision and rc.1 successors (X1)
  SHA256SUMS                  checksums of every file

Release gate (always on): held Tribal-related records, and records attached to a held target, are excluded
(ADR-0007 §D); records carrying LicenseRef-EMSTv1-PendingDedication are excluded from the CC0 files while the lead's
Q2 dedication is pending (ADR-0013); records licensed LicenseRef-EMST-third-party-index-derived are excluded from every
output and counted (ADR-0029 §9.6); quarantined signals (careFlag, SP-12), placeholder `mvp-role:` targets and
organization measures with n < 5 are excluded (ADR-0029 §8.2); v1Seed, editorialNote and stored inverse links are
stripped (inverses are recomputed by inverse-links@1.1.0); drafts are excluded (profile `release`). The build refuses to
run if scripts/validate_v2.py --strict reports errors (skip only with --no-validate, e.g. in tests), and it
re-checks its own output for leaks before writing SHA256SUMS.

Release closure and conformance (rc.1 fix pass B1, M1, M11, m4, m14; docs/review/DATA_FIX_BRIEF.md §1, §9, §12):
  - references to records not in the release are removed; a record whose required field that removal would empty is
    held back from the release and counted, never shipped broken; an actor enactment that loses a requires, enables
    or constrains link makes its venue value `indeterminate (basis withheld)`;
  - Text-typed fields only (per schema/emst.schema.json) become language maps; nested strings stay strings;
  - display-gated values the gate does not render move into `agentDraft` (scripts/agent_draft.py) in the bundle and
    are left out of every CSV and HCM file;
  - self_check() validates every bundle node against the schema (minus the documented computed inverse fields),
    checks that every bundle key is a context term, and runs the Tribal trigger scan over every output file and field.
Build stamp (m1): under --profile release the build refuses a commit stamp that ends in `+uncommitted` or claims a clean
commit the tree does not have; a pre-commit candidate passes `--build-commit "<HEAD sha>+recut-pending-commit"` (see
docs/release/<version>/BUILD.md). The release date is --date, else the latest record generatedAt (SOURCE_DATE_EPOCH is
honoured by the preview profile only, so CI and a local re-cut agree).

Usage:
  python scripts/build_release.py --version 2.0.0-rc.1 [--date 2027-01-15] [--previous dist/2.0.0-rc.0/emst.bundle.jsonld]
  python scripts/build_release.py --profile preview --version 2.0.0-dev     # internal: includes drafts (never held)
Determinism: no wall-clock time is used; --date defaults to SOURCE_DATE_EPOCH, else the latest generatedAt among
included records. Two consecutive builds from the same inputs are byte-identical (tests/test_build_release.py).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import uuid
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emstlib as L  # noqa: E402
import agent_draft  # noqa: E402
import release_gate  # noqa: E402
from rules import (agreement, assessment_staleness, change_indicator, effective_use_tier, gated_values,  # noqa: E402
                   inverse_links, io_bridge, registry, venue_applicability)
from rules import (federal_series_profile, job_family_membership, mirror_links, pathway_edges,  # noqa: E402
                   role_change, state_class_view)

V1_LICENSE = "LicenseRef-EMSTv1-PendingDedication"
CC0_IRI = "https://creativecommons.org/publicdomain/zero/1.0/"
UUID_NS = uuid.uuid5(uuid.NAMESPACE_URL, L.IRI_BASE)
_DROP = object()
STRIP_FIELDS = {"v1Seed", "editorialNote"}
RELEASE_STATUSES = {"candidate", "published", "deprecated", "superseded", "withdrawn"}
NOTICE = ("EMST describes work; it is not a selection instrument, not a classification basis, not a job analysis "
          "and not for RIF, adverse action or performance-rating decisions (ADR-0012 I-2; ADR-0024).")
INDIGENOUS_STATEMENT = ("Indigenous knowledge is a distinct body of environmental expertise held and governed by Indigenous "
                        "nations. It is out of scope of EMST by design (ADR-0007; SPEC §16.1).")
TEXT_FIELDS_TO_LANG = {"rationale", "assessmentContext", "authorityBasis", "principal", "accountabilityVenue", "counterSignal",
                       "evidencePlan", "shouldRemainHumanReason", "mitigation", "scopeOfPractice", "assessmentPlan", "note",
                       "description", "costNote"}
THIRD_PARTY_LICENSE = "LicenseRef-EMST-third-party-index-derived"
EXCLUDE_THIRD_PARTY = "third-party index-derived licence (ADR-0013; ADR-0029 §9.6)"
EXCLUDE_HELD = "held (Tribal content hold, ADR-0007 §D)"
EXCLUDE_WITHHELD = "withheld: claim rests on an unverified claims-register row (WP-15 §2.1; ADR-0031 §8)"
AUTHORSHIP = ("This release was researched and drafted by a team of AI agents (Anthropic's Claude), each given a specialist "
              "role, working to a charter set by the EMST project lead. AI agents checked the facts against sources in October "
              "2026. No independent human expert has reviewed the release yet. Role names such as \"Chief Taxonomy Architect\" "
              "are AI agent roles, not people.")
NOT_VALIDATED = ("Nothing in this release has been validated by human subject-matter experts. No Delphi panel, reliability "
                 "study or job analysis has been run. Every rating and tag is an AI agent's draft (raterType llm, label S; or "
                 "v1-analyst, LLM-assisted, prior evidence). Repeated passes of one model are one rater: their agreement is "
                 "run-to-run consistency, not reliability. The display gate shows none of them as findings, and every published "
                 "element is at describe or develop tier at most, never select.")
AGENT_DRAFT_NOTICE = ("Agent-drafted values that the display gate does not show sit only in an `agentDraft` sub-object, with "
                      "their raterType, validationStatus and display-gate label: role task-bundle importance, time share, "
                      "critical and needed-at-entry flags; competency-target importance, distinguishing and "
                      "critical-for-selection flags; task work function, field and formation dependency, work modes, "
                      "relationship types and reproduction-regime codes; indicator OBS-4. They are AI drafts, not job-analysis "
                      "results. The CSV and HCM files leave them out (csv/tasks.csv gives only their gate status in *_status "
                      "columns; csv/indicators.csv names the agents' declared use class use_class_declared).")
ID_NOTICE = "IDs are candidate; they become stable from 2.0.0 (SPEC §10.1: IDs are stable from `published`)."
MANIFEST_NOTICE = f"{NOTICE} {AGENT_DRAFT_NOTICE} {ID_NOTICE}"
CSV_NOTICE = f"{NOTICE} {ID_NOTICE}"
EXCLUDE_REDACTION = "held back: removing references to records not in this release would empty a required field (B1)"
VENUE_ROLES = ("requires", "enables", "constrains")
VENUE_WITHHELD = "indeterminate (basis withheld)"
X1_NOT_RELEASED = "successor not in this release"
SUCCESSOR_RELATIONS = {"emst:replacedBy", "emst:splitInto", "emst:mergedInto", "emst:movedToTools"}
# m3: release artifacts SPEC §12.5 and §17.2 promise that this build does not produce
OMITTED_ARTIFACTS = [
    ("SPEC §12.5", "\"does this affect me?\" notice"), ("SPEC §12.5", "DOI"), ("SPEC §12.5", "SBOM of the data release"),
    ("SPEC §12.5", "signed artifacts"), ("SPEC §12.5", "accessibility conformance report for the data release (the explorer's is site/ACR.md)"),
    ("SPEC §17.2", "CTDL-ASN (the primary public linked-data channel; nothing is registered in the Credential Registry, so the "
                   "`ctid` values in csv/hcm_skills_library.csv are derived UUIDv5 values, SPEC §12.3, registered nowhere)"),
    ("SPEC §17.2", "CASE 1.1"), ("SPEC §17.2", "RSD"), ("SPEC §17.2", "Open Badges 3.0 alignment targets"),
]
SHIPPED_ARTIFACTS = "JSON-LD bundle, CSV + Frictionless data package (with the HCM skills-library file and the delta feed), SKOS Turtle, SSSOM (with SSSOM 1.0-strict renderings), computed views, delta files and SHA256SUMS"
# m14: build-owned statements of the hold rule that name no record; the full-output trigger scan exempts these exact
# strings, and the SKOS triples about vocabulary concepts (SPEC §9.1: the vocabulary carries the actor subtypes)
HOLD_COUNT_LINE = "Held Tribal-related records (ADR-0007 §D), reported only as a count"
HOLD_POLICY_LINE = ("Held Tribal-related items are reported only as a count (ADR-0007 §D); nothing Tribal-related is published "
                    "before a Tribal Advisory Council approves.")
DEPENDENT_FIELDS = ("task", "competency", "subject", "targetId", "variantOf")
G9_RANGE = (120, 180)          # counts@1.0.0 coreCompetencies incl. held core (ADR-0030 §3.4; G-9)
X1_HELD_COMMENT = "decision={decision}; ADR-0011; one or more successors not in this release"
WAIVER_COLUMNS = ["record_id", "rule_id", "text_sha256", "waiver_class", "reviewer", "second_reviewer", "decided_on", "rationale"]
# Inputs the build reads: a commit stamp is clean only when none of these differs from HEAD (m1).
BUILD_INPUTS = ["data", "vocab", "schema", "scripts", "validation", "docs/decisions/candidate_disposition.csv",
                "docs/release/*/PUBLICATION_SIGNOFF.yaml", "pyproject.toml"]
PENDING_COMMIT_SUFFIX = "+recut-pending-commit"


def git_state(root: Path) -> tuple[str | None, bool]:
    """(HEAD sha or None, whether any build input differs from HEAD)."""
    try:
        out = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=10)
        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--", *BUILD_INPUTS],
                               capture_output=True, text=True, timeout=30)
        if out.returncode == 0:
            return out.stdout.strip(), bool(dirty.stdout.strip())
    except Exception:  # noqa: BLE001
        pass
    return None, True


def git_commit(root: Path) -> str:
    head, dirty = git_state(root)
    if head is None:
        return "uncommitted"
    return head + ("+uncommitted" if dirty else "")


def check_build_commit(commit: str, profile: str, root: Path = L.ROOT) -> str | None:
    """m1: under the release profile, a build stamp must identify its inputs. Returns a refusal message or None.
    Refused: '+uncommitted' (or 'uncommitted'); a bare 40-hex sha that is not HEAD, or is HEAD while the build inputs
    differ from it. Allowed: HEAD on a clean tree, or '<HEAD>+recut-pending-commit' for a pre-commit candidate that the
    orchestrator rebuilds from the clean commit before tagging."""
    if profile != "release":
        return None
    if commit == "uncommitted" or commit.endswith("+uncommitted"):
        return (f"refusing a release build stamped {commit!r}: commit the inputs first, or pass "
                f"--build-commit \"<HEAD sha>{PENDING_COMMIT_SUFFIX}\" for a pre-commit candidate (BUILD.md)")
    if re.fullmatch(r"[0-9a-f]{40}", commit):
        head, dirty = git_state(root)
        if head is not None and (commit != head or dirty):
            return (f"refusing a release build stamped {commit[:12]}: it claims a clean commit, but "
                    + ("HEAD is " + head[:12] if commit != head else "the build inputs differ from HEAD"))
    return None


def case_uuid(rid: str) -> str:
    return str(uuid.uuid5(UUID_NS, L.iri(rid)))


TEXT_DEFS = ("Text", "LangMap", "LangMapMulti")


def sssom_other(s) -> dict:
    return dict(x.split("=", 1) for x in str(s or "").split(";") if "=" in x)


def human_reviewed(row: dict) -> bool:
    """A mapping row a pseudonymous human (pid:) reviewed: reviewer_id, or reviewer= in `other`."""
    revs = [x for x in str(row.get("reviewer_id") or "").split("|") if x] + [sssom_other(row.get("other")).get("reviewer", "")]
    return any(x.startswith("pid:") for x in revs)


def _semver(v) -> tuple:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)", str(v or ""))
    return tuple(int(x) for x in m.groups()) if m else (0, 0, 0)


def schema_text_paths(schema: dict) -> dict[str, list[tuple]]:
    """{entity type: [path]} where the schema types the value as Text/LangMap ('[]' array item, '*' map value)."""
    defs = schema.get("$defs") or {}
    types = (defs.get("v_entityType") or {}).get("enum") or []

    def walk(node, path, out, stack, depth=0):
        if depth > 40 or not isinstance(node, dict):
            return
        ref = node.get("$ref", "")
        if ref.startswith("#/$defs/"):
            name = ref.split("/")[-1]
            if name in TEXT_DEFS:
                out.add(path)
                return
            if name not in stack:
                walk(defs.get(name, {}), path, out, stack | {name}, depth + 1)
        for k, sub in (node.get("properties") or {}).items():
            walk(sub, path + (k,), out, stack, depth + 1)
        if isinstance(node.get("items"), dict):
            walk(node["items"], path + ("[]",), out, stack, depth + 1)
        if isinstance(node.get("additionalProperties"), dict):
            walk(node["additionalProperties"], path + ("*",), out, stack, depth + 1)
        for key in ("allOf", "anyOf", "oneOf"):
            for sub in node.get(key) or []:
                walk(sub, path, out, stack, depth + 1)
        for key in ("then", "else"):
            if isinstance(node.get(key), dict):
                walk(node[key], path, out, stack, depth + 1)

    out = {}
    for t in types:
        acc: set = set()
        walk(defs.get(t, {}), (), acc, {t})
        out[t] = sorted(acc)
    return out


class Builder:
    def __init__(self, data_root=L.DATA_V2, profile="release", version="2.0.0-dev", date=None, previous=None,
                 include_pending_license=False, build_commit=None):
        self.data = Path(data_root)
        self.profile = profile
        self.version = version
        self.previous = previous
        self.include_pending = include_pending_license and profile == "preview"
        gov = self.data / "governance"
        self.hold = L.load_yaml(gov / "tribal_hold.yaml") if (gov / "tribal_hold.yaml").exists() else {}
        self.licensing = L.load_yaml(gov / "licensing.yaml") if (gov / "licensing.yaml").exists() else {"v1Dedication": "pending"}
        self.held_keys = set(self.hold.get("heldSeedKeys") or [])
        self.held_v1 = set(self.hold.get("heldV1Codes") or [])
        self.tac = bool(self.hold.get("tacConstituted"))
        wh = L.load_yaml(gov / "release_withheld.yaml") if (gov / "release_withheld.yaml").exists() else {}
        self.withheld = {k for row in (wh.get("withheld") or []) for k in row.get("records") or []}
        self.included = None                       # ids that pass the gate; set by build() before records are cleaned
        self.redacted = Counter()
        self.commit = build_commit or git_commit(L.ROOT)
        refusal = check_build_commit(self.commit, profile)
        if refusal:
            raise SystemExit(refusal)
        self.basis_withheld: set = set()          # actor enactments that lost a venue-deciding link to redaction (m4)
        self.held_back: list = []                 # records held back because redaction would empty a required field (B1)
        self.agent_draft_moved = 0
        self.records = {}
        for loc, rec in L.iter_records(self.data):
            if isinstance(rec, dict) and isinstance(rec.get("id"), str):
                self.records.setdefault(rec["id"], rec)
        self.excluded = Counter()
        self.date = date or self._default_date()
        self.rules = registry.active_rules()
        self.stamped: set = set()
        cf = L.load_yaml(L.LINT_DIR / "computed_fields.yaml")
        self.inverse_fields = {t: set(v) for t, v in (cf.get("inverse_fields_by_type") or {}).items()}
        self.waivers = self._load_waivers()
        gc = L.load_yaml(L.LINT_DIR / "governed_content.yaml")
        self.triggers = [re.compile(p["pattern"], 0 if p.get("cs") else re.I) if isinstance(p, dict) else re.compile(p, re.I)
                         for p in gc["tribal_hold"]["triggers"]]

    def _load_waivers(self):
        """data/v2/governance/lint_waivers.csv rows signed by pseudonymous humans only (validate_v2 reports the rest)."""
        p = self.data / "governance" / "lint_waivers.csv"
        if not p.exists():
            return []
        out = []
        for w in L.read_csv(p):
            if list(w) != WAIVER_COLUMNS:
                return []
            signers = [w["reviewer"]] + ([w["second_reviewer"]] if w["second_reviewer"] else [])
            if all(x.startswith("pid:") for x in signers) and w["reviewer"] != w["second_reviewer"]:
                out.append(dict(w))
        return out

    def _default_date(self):
        sde = os.environ.get("SOURCE_DATE_EPOCH")
        if sde and self.profile != "release":       # m1: a release date comes from the records, or from --date
            return dt.datetime.fromtimestamp(int(sde), dt.timezone.utc).date().isoformat()
        if sde:
            print("I-RELEASE-DATE SOURCE_DATE_EPOCH ignored under --profile release; the date comes from the records (or --date)")
        dates = sorted(str((r.get("provenance") or {}).get("generatedAt", ""))[:10] for r in self.records.values())
        return dates[-1] if dates and dates[-1] else "1970-01-01"

    # ---------------------------------------------------------------- gate
    def is_held(self, rid, rec):
        if rid in self.held_keys:
            return True
        if rec.get("indigenousDataFlag") is True and not (self.tac and rec.get("approvalStatus") == "approved"):
            return True
        for d in (rec.get("provenance") or {}).get("derivedFrom") or []:
            m = re.match(r"^v1:([1-7]\.\d{1,2}\.\d{1,2})", d.get("v1Key", ""))
            if m and m.group(1) in self.held_v1 and d.get("relation") != "reference-only":
                return True
        return False

    def depends_on_held(self, rec):
        """Records attached to a held target inherit the hold (ADR-0007 §D; ADR-0029 §9.6)."""
        refs = [rec.get(f) for f in DEPENDENT_FIELDS]
        refs += [s.get("competency") for s in rec.get("supports") or [] if isinstance(s, dict)]
        return any(self._held_ref(x) for x in refs if isinstance(x, str))

    @staticmethod
    def quarantined(rec):
        if rec.get("type") != "ChangeSignal":
            return False
        sps = set(rec.get("scenarioSignposts") or []) | {n.get("value") for n in rec.get("notation") or []
                                                         if isinstance(n, dict) and n.get("scheme") == "EMST-signpost"}
        return bool(rec.get("careFlag")) or bool(sps & {"vocab:scenarios#SP-12", "SP-12"})

    def include(self, rid, rec):
        if rec.get("type") == "VocabularyTerm":
            return False
        if self.is_held(rid, rec) or self.depends_on_held(rec):
            self.excluded[EXCLUDE_HELD] += 1
            return False
        if rec.get("license") == THIRD_PARTY_LICENSE:
            self.excluded[EXCLUDE_THIRD_PARTY] += 1
            return False
        if rid in self.withheld or (rec.get("type") == "DriverEvent" and rec.get("instrument") in self.withheld):
            self.excluded[EXCLUDE_WITHHELD] += 1
            return False
        if self.quarantined(rec):
            self.excluded["quarantined signal: careFlag or signpost SP-12 (ADR-0028 ER-0; ADR-0029 §8.2)"] += 1
            return False
        if str(rec.get("targetId", "")).startswith("mvp-role:"):
            self.excluded["placeholder mvp-role: target, not yet re-keyed (ADR-0029 §8.2)"] += 1
            return False
        if rec.get("type") == "ChangeSignal" and rec.get("targetType") == "organization" \
                and isinstance((rec.get("measure") or {}).get("n"), int) and rec["measure"]["n"] < 5:
            self.excluded["organization measure with n < 5, suppressed (ADR-0012)"] += 1
            return False
        if rec.get("license") == V1_LICENSE and self.licensing.get("v1Dedication") != "granted" and not self.include_pending:
            self.excluded["v1-derived text pending CC0 dedication (ADR-0013, Q2)"] += 1
            return False
        if self.profile == "release" and rec.get("status") not in RELEASE_STATUSES:
            self.excluded["draft (not in a release)"] += 1
            return False
        if self.profile == "release" and not L.is_emst_id(rid):
            self.excluded["no minted ID"] += 1
            return False
        if rec.get("type") == "Pathway" and rec.get("recommended") is True:
            raise SystemExit(f"release gate: pathway {rid} is labelled recommended (ADR-0023)")
        return True

    def clean(self, rec, redact=True):
        """Strip build-only fields, remove references to records not in the release (redact=False skips that, for
        the B1 hold-back test) and turn Text-typed strings into language maps."""
        out = {}
        t = rec.get("type")
        inverse = self.inverse_fields.get(t, set())
        for k, v in rec.items():
            if k in STRIP_FIELDS or k in inverse:
                continue
            if redact:
                before = v
                v = self._redact(v)
                if t == "Enactment" and k == "characteristicInstruments":
                    self._note_basis_withheld(rec, before, v)
                if v is _DROP:
                    continue
            out[k] = self._lang(t, (k,), v)
        return out

    def _note_basis_withheld(self, rec, before, after):
        """m4: an actor enactment whose requires, enables or constrains link was removed has a withheld basis."""
        def n(links):
            return sum(1 for x in (links if isinstance(links, list) else []) if isinstance(x, dict) and x.get("role") in VENUE_ROLES)
        if n(before) > (0 if after is _DROP else n(after)):
            self.basis_withheld.add(rec.get("id"))

    def _held_ref(self, s):
        if not isinstance(s, str) or not L.is_record_ref(s):
            return False
        if s in self.held_keys:
            return True
        r = self.records.get(s)
        return r is not None and self.is_held(s, r)

    def _gone(self, s):
        """Why a record reference may not appear in a released record: held, withheld or not in this release
        (draft, unminted, excluded or unauthored). None for anything that is not a record reference or is released."""
        if not isinstance(s, str) or not L.is_record_ref(s):
            return None
        if self._held_ref(s):
            return "held"
        if s in self.withheld:
            return "withheld"
        if self.included is not None and s not in self.included:
            return "not in this release"
        return None

    def _redact(self, v):
        """Remove references to held records (ADR-0007 §D: held keys never leave the repo) and to any record that is
        not in this release (ADR-0031 §6: a release is referentially closed; withheld and unminted records are never
        named). An object that names such a record is dropped whole (a supports link, a typed instrument link, a bundle
        item). Each removal is counted for the release notes."""
        if isinstance(v, str):
            why = self._gone(v)
            if why:
                self.redacted[why] += 1
                return _DROP
            return v
        if isinstance(v, list):
            items = [self._redact(x) for x in v]
            return [x for x in items if x is not _DROP]
        if isinstance(v, dict):
            whys = [w for w in (self._gone(x) for x in v.values() if isinstance(x, str)) if w]
            if whys:
                self.redacted[whys[0]] += 1
                return _DROP          # an object that names held or unreleased content is dropped whole
            out = {}
            for k, x in v.items():
                y = self._redact(x)
                if y is not _DROP:
                    out[k] = y
            return out
        return v

    def _lang(self, rtype, path, v):
        """B1: a string becomes {"en": ...} only at a path the schema types as Text (or a language map) and whose field
        name is in TEXT_FIELDS_TO_LANG. Nested `note` fields that the schema types as plain strings stay strings."""
        if isinstance(v, dict):
            return {k: self._lang(rtype, path + (k,), x) for k, x in v.items()}
        if isinstance(v, list):
            return [self._lang(rtype, path + ("[]",), x) for x in v]
        if isinstance(v, str):
            name = next((p for p in reversed(path) if p != "[]"), None)
            if name in TEXT_FIELDS_TO_LANG and self._text_typed(rtype, path):
                return {"en": v}
        return v

    def _text_typed(self, rtype, path):
        pats = self.text_paths().get(rtype, ())
        return any(len(p) == len(path) and all(a == b or a == "*" for a, b in zip(p, path)) for p in pats)

    def text_paths(self):
        """{type: [path tuple]} of every field the schema types as Text, LangMap or LangMapMulti ('[]' = array item,
        '*' = map value). Computed from schema/emst.schema.json, so it follows the schema without a hand list."""
        if not hasattr(self, "_text_paths"):
            self._text_paths = schema_text_paths(self.schema())
        return self._text_paths

    def schema(self):
        if not hasattr(self, "_schema"):
            self._schema = json.loads(L.SCHEMA_OUT.read_text(encoding="utf-8"))
        return self._schema

    def validator(self, def_name=None):
        """jsonschema validator for the whole schema (dispatch on `type`) or for one $def."""
        import jsonschema
        cache = self.__dict__.setdefault("_validators", {})
        if def_name not in cache:
            s = self.schema()
            doc = s if def_name is None else {"$schema": s.get("$schema"), "$defs": s["$defs"], "$ref": f"#/$defs/{def_name}"}
            cache[def_name] = jsonschema.Draft202012Validator(doc, format_checker=jsonschema.FormatChecker())
        return cache[def_name]

    def schema_errors(self, node):
        """Leaf validation errors of a node, most specific first (an 'Unevaluated properties' error at the root only
        echoes a failed branch, so it sorts last)."""
        t = node.get("type") if isinstance(node, dict) else None
        v = self.validator(t if t in ("Release", "CompetencyLevelOutcome") else None)

        def leaves(e):
            if e.context:
                for c in e.context:
                    yield from leaves(c)
            else:
                yield e
        errs = [x for e in v.iter_errors(node) for x in leaves(e)]
        return sorted(errs, key=lambda e: (e.message.startswith("Unevaluated"), -len(e.absolute_path),
                                           list(map(str, e.absolute_path)), e.message))

    # ---------------------------------------------------------------- build
    def close(self, included: set) -> dict:
        """Clean every included record, then hold back (B1) any record whose cleaned form fails the schema only because
        references were removed (for example a tool left with `servesCompetencies: []`), and repeat until nothing
        more is held back: holding one record back can remove references from others. Returns the released records."""
        included = set(included)
        while True:
            self.included = included
            self.redacted = Counter()
            self.basis_withheld = set()
            released, back = {}, []
            for rid in sorted(included):
                rec = self.records[rid]
                before = sum(self.redacted.values())
                cleaned = self.clean(rec)
                if sum(self.redacted.values()) != before and self.schema_errors(cleaned) \
                        and not self.schema_errors(self.clean(rec, redact=False)):
                    back.append(rid)
                released[rid] = cleaned
            if not back:
                return released
            for rid in back:
                included.discard(rid)
                self.held_back.append(rid)
                self.excluded[EXCLUDE_REDACTION] += 1

    def build(self, out: Path):
        out = Path(out)
        included = {rid for rid, rec in sorted(self.records.items()) if self.include(rid, rec)}
        released = self.close(included)
        self.released = released
        self.inverse = inverse_links.compute(released)
        files: dict[str, bytes] = {}
        files.update(self.views(released))          # first: the bundle's agentDraft labels and the CSV tiers read views
        files["emst.bundle.jsonld"] = self.bundle(released).encode("utf-8")
        files.update(self.csvs(released))
        files["emst.skos.ttl"] = self.skos(released).encode("utf-8")
        files.update(self.sssom(released))
        delta = self.delta(released)
        files["delta.json"] = L.dump_json(delta).encode("utf-8")
        self.v1delta = self.delta_v1(released)
        files["delta_v1.json"] = L.dump_json(self.v1delta).encode("utf-8")
        files["csv/delta.csv"] = L.csv_text(["id", "change"], [{"id": i, "change": c} for c in ("added", "changed", "superseded", "withdrawn") for i in delta[c]]).encode()
        files["csv/datapackage.json"] = self.datapackage(files).encode("utf-8")
        files["RELEASE_NOTES.md"] = self.notes(released, delta).encode("utf-8")
        self.self_check(files)
        sums = "".join(f"{L.sha256_bytes(files[name])}  {name}\n" for name in sorted(files))
        files["SHA256SUMS"] = sums.encode()
        out.mkdir(parents=True, exist_ok=True)
        for name, data in files.items():
            p = out / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        return files

    def bundle(self, released):
        ctx = json.loads(L.CONTEXT_OUT.read_text(encoding="utf-8"))["@context"]
        extra = inverse_links.bundle_fields(self.inverse)            # inverse-links@1.1.0 bundle_fields
        if extra:
            self.stamped.add(("inverse-links", str(self.rules["inverse-links"]["version"])))
        # M1: display-gated values the gate does not render move into agentDraft (labels from views/display_gate.json)
        env = agent_draft.Envelope.from_display_gate((getattr(self, "view_docs", {}) or {}).get("views/display_gate.json"))
        stale = getattr(self, "stale_ids", set())
        graph = [dict(env.apply(r), **extra.get(rid, {}), **({"stale": True} if rid in stale else {}))
                 for rid, r in released.items()]
        self.agent_draft_moved = env.moved
        graph += self.clo_nodes(released)
        mappings = self._mapping_rows(released)
        for set_name, rows in sorted(mappings.items()):
            for r in rows:
                graph.append(self.mapping_node(r, set_name))
        manifest = {"id": f"https://w3id.org/emst/release/{self.version}", "type": "Release",
                    "emstRelease": self.version, "schemaVersion": L.SCHEMA_VERSION, "released": self.date,
                    "license": CC0_IRI, "notice": MANIFEST_NOTICE, "indigenousKnowledgeStatement": INDIGENOUS_STATEMENT,
                    "buildCommit": self.commit}
        # everything in the default graph: release manifest first, then records sorted by id, then mappings
        return L.dump_json({"@context": ctx, "@graph": [manifest] + graph})

    @staticmethod
    def mapping_node(r, set_name):
        """One SSSOM row as a bundle node typed as the schema's Mapping def: numeric slots as numbers, multivalued
        slots as lists ('|'-separated in TSV), every other column (including `other` and `mapping_tool`) kept."""
        import build_schema
        m = {"type": "Mapping"}
        for k, v in r.items():
            if v in ("", None):
                continue
            if k in build_schema.SSSOM_NUMERIC:
                try:
                    v = float(v)
                except ValueError:
                    pass
            elif k in build_schema.SSSOM_MULTIVALUED:
                v = [x for x in str(v).split("|") if x]
            m[k] = v
        m["mapping_set_id"] = m.get("mapping_set_id", set_name)
        return m

    @staticmethod
    def clo_nodes(released):
        """Computed CompetencyLevelOutcome nodes (CR-LC-001 #3; vocab/identifiers.yaml#form.clo_iri). Never source
        records: one per released competency level, with that level's indicators only, and one per enactment level
        with indicator variants (generic indicators plus the enactment's variants at that level)."""
        nodes = []
        levels_of = {}
        for rid, r in released.items():
            if r.get("type") != "Competency":
                continue
            for lv in r.get("levels") or []:
                if not isinstance(lv, dict) or not lv.get("level"):
                    continue
                inds = [i for i in lv.get("indicators") or [] if i in released]
                levels_of.setdefault(rid, {})[lv["level"]] = inds
                cid = f"{rid}/levels/{lv['level']}"
                nodes.append({"id": cid, "type": "CompetencyLevelOutcome", "competency": rid, "level": lv["level"],
                              "indicators": inds, "caseUuid": case_uuid(cid)})        # SPEC §12.3 derived UUIDv5
        for rid, e in released.items():
            if e.get("type") != "Enactment" or not e.get("indicatorVariants"):
                continue
            variants = [released[i] for i in e["indicatorVariants"] if i in released]
            generic = levels_of.get(e.get("competency"), {})
            for lv in sorted({v.get("level") for v in variants if v.get("level")} | set(generic)):
                vids = sorted(v["id"] for v in variants if v.get("level") == lv)
                if not vids:
                    continue
                cid = f"{rid}/levels/{lv}"
                nodes.append({"id": cid, "type": "CompetencyLevelOutcome", "competency": e.get("competency"),
                              "enactment": rid, "level": lv, "indicators": generic.get(lv, []) + vids, "caseUuid": case_uuid(cid)})
        return sorted(nodes, key=lambda n: n["id"])

    # ---------------------------------------------------------------- CSV + datapackage
    TABLES = {
        "competencies": ["id", "uri", "case_uuid", "v1_codes", "pref_label_en", "statement_en", "competency_type", "transversal_cluster",
                         "home_module", "module", "status", "lifecycle_state", "use_tier_ceiling", "effective_use_tier",
                         "validation_status", "level_min", "level_max", "replaced_by", "license"],
        # M1: gated task values are never exported; the *_status columns hold only the display-gate label
        "tasks": ["id", "uri", "pref_label_en", "statement_en", "text_sha256", "work_function_status", "field_dependency_status",
                  "formation_dependency_status", "home_module", "module", "status", "lifecycle_state", "effective_use_tier",
                  "validation_status", "license"],
        "task_competency_links": ["task_id", "competency_id", "strength"],
        # M1/m8: use_class is the authoring agents' declared class; obs4 stays empty until humans double-code it
        "indicators": ["id", "competency_id", "level", "statement_en", "augmentation_mode", "use_class_declared", "obs4",
                       "effective_use_tier", "assessment_methods", "jurisdiction_variable", "validation_status"],
        "hcm_skills_library": ["skill_id", "uri", "case_uuid", "ctid", "skill_name", "skill_statement", "category", "module",
                               "status", "replaced_by", "emst_release", "notice"],
        "mappings": ["mapping_set", "subject_id", "predicate_id", "predicate_modifier", "object_id", "mapping_justification",
                     "confidence", "author_id", "mapping_date", "mapping_tool", "other", "comment"],
    }
    TASK_STATUS_COLUMNS = {"work_function_status": "workFunction", "field_dependency_status": "fieldDependency",
                           "formation_dependency_status": "formationDependency"}

    def _csv_gate(self, rid, rec, field):
        """Display-gate label for a gated value in a CSV (never the value). '' when the record has no value; the
        value itself only if the gate renders it (then the column says so)."""
        if rec.get(field) in (None, "", []):
            return ""
        env = getattr(self, "_csv_env", None)
        if env is None:
            env = self._csv_env = agent_draft.Envelope.from_display_gate(self.view_docs.get("views/display_gate.json"))
        gate_field = {"workFunction": "Task.workFunction"}.get(field)
        decision, label = env.decisions.get((rid, gate_field), (None, None)) if gate_field else (None, None)
        if decision in agent_draft.RENDERED:
            return f"shown ({decision})"
        return env.labels.get(label or "assessment_pending", env.labels.get("assessment_pending", "assessment pending"))

    def _eut(self):
        if not hasattr(self, "_eut_by_id"):
            rows = (self.view_docs.get("views/effective_use_tier.json") or {}).get("rows") or []
            self._eut_by_id = {r.get("id"): r.get("effectiveUseTier", "") for r in rows}
        return self._eut_by_id

    def csvs(self, released):
        rows = defaultdict(list)
        for rid, r in released.items():
            t = r.get("type")
            en = lambda f: (r.get(f) or {}).get("en", "") if isinstance(r.get(f), dict) else (r.get(f) or "")  # noqa: E731
            if t == "Competency":
                rows["competencies"].append({
                    "id": rid, "uri": L.iri(rid), "case_uuid": case_uuid(rid),
                    "v1_codes": "|".join(n["value"] for n in r.get("notation", []) if n.get("scheme") == "EMSTv1"),
                    "pref_label_en": en("prefLabel"), "statement_en": en("statement"), "competency_type": r.get("competencyType", ""),
                    "transversal_cluster": r.get("transversalCluster", ""), "home_module": r.get("homeModule", ""),
                    "module": r.get("module"), "status": r.get("status"), "lifecycle_state": r.get("lifecycleState", ""),
                    "use_tier_ceiling": r.get("useTier", ""), "effective_use_tier": self._eut().get(rid, ""),
                    "validation_status": r.get("validationStatus", ""),
                    "level_min": (r.get("levelSpan") or {}).get("min", ""), "level_max": (r.get("levelSpan") or {}).get("max", ""),
                    "replaced_by": "|".join(r.get("replacedBy", [])), "license": r.get("license")})
                rows["hcm_skills_library"].append({
                    "skill_id": rid, "uri": L.iri(rid), "case_uuid": case_uuid(rid), "ctid": "ce-" + case_uuid(rid),
                    "skill_name": en("prefLabel"), "skill_statement": en("statement"), "category": r.get("competencyType", ""),
                    "module": r.get("module"), "status": r.get("status"), "replaced_by": "|".join(r.get("replacedBy", [])),
                    "emst_release": self.version, "notice": CSV_NOTICE})
            elif t == "Task":
                rows["tasks"].append({
                    "id": rid, "uri": L.iri(rid), "pref_label_en": en("prefLabel"), "statement_en": en("statement"),
                    "text_sha256": r.get("textSha256"),
                    **{col: self._csv_gate(rid, r, f) for col, f in self.TASK_STATUS_COLUMNS.items()},
                    "home_module": r.get("homeModule", ""), "module": r.get("module"), "status": r.get("status"),
                    "lifecycle_state": r.get("lifecycleState", ""), "effective_use_tier": self._eut().get(rid, ""),
                    "validation_status": r.get("validationStatus", ""), "license": r.get("license")})
                for s in r.get("supports", []):
                    if s["competency"] in released:
                        rows["task_competency_links"].append({"task_id": rid, "competency_id": s["competency"], "strength": s["strength"]})
            elif t == "Indicator":
                rows["indicators"].append({
                    "id": rid, "competency_id": r.get("competency"), "level": r.get("level"), "statement_en": en("statement"),
                    "augmentation_mode": r.get("augmentationMode", ""), "use_class_declared": r.get("useClass", ""),
                    "obs4": "",                       # gated (indicator.obs4) and self-coded: never exported (M1, m8)
                    "effective_use_tier": self._eut().get(rid, ""),
                    "assessment_methods": "|".join(r.get("assessmentMethods", [])),
                    "jurisdiction_variable": str(r.get("jurisdictionVariable", "")).lower(), "validation_status": r.get("validationStatus", "")})
        for set_name, mrows in sorted(self._mapping_rows(released).items()):
            for m in mrows:
                rows["mappings"].append({"mapping_set": set_name, **{k: m.get(k, "") for k in self.TABLES["mappings"] if k != "mapping_set"}})
        return {f"csv/{name}.csv": L.csv_text(cols, rows[name]).encode("utf-8") for name, cols in self.TABLES.items()}

    def datapackage(self, files):
        resources = []
        keys = {"competencies": ["id"], "tasks": ["id"], "indicators": ["id"], "hcm_skills_library": ["skill_id"]}
        fks = {"task_competency_links": [{"fields": "task_id", "reference": {"resource": "tasks", "fields": "id"}},
                                         {"fields": "competency_id", "reference": {"resource": "competencies", "fields": "id"}}],
               "indicators": [{"fields": "competency_id", "reference": {"resource": "competencies", "fields": "id"}}]}
        cols = dict(self.TABLES)
        cols["delta"] = ["id", "change"]
        for name in sorted(cols):
            path = f"{name}.csv"
            schema = {"fields": [{"name": c, "type": "integer" if c == "obs4" else "string"} for c in cols[name]],
                      "missingValues": [""]}
            if name in keys:
                schema["primaryKey"] = keys[name]
            if name in fks:
                schema["foreignKeys"] = fks[name]
            resources.append({"name": name.replace("_", "-"), "path": path, "profile": "tabular-data-resource",
                              "format": "csv", "mediatype": "text/csv", "encoding": "utf-8",
                              "hash": "sha256:" + L.sha256_bytes(files[f"csv/{name}.csv"]), "schema": schema})
        pkg = {"profile": "tabular-data-package", "name": "emst", "title": "Environmental Management Skills Taxonomy",
               "version": self.version, "created": f"{self.date}T00:00:00Z",          # m2: Frictionless datetime
               "licenses": [{"name": "CC0-1.0", "path": CC0_IRI}], "description": CSV_NOTICE, "resources": resources}
        return L.dump_json(pkg)

    # ---------------------------------------------------------------- SKOS
    @staticmethod
    def _lit(s, lang=None):
        esc = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
        return f'"{esc}"' + (f"@{lang}" if lang else "")

    def skos(self, released):
        lines = ["@prefix skos: <http://www.w3.org/2004/02/skos/core#> .", "@prefix dct: <http://purl.org/dc/terms/> .",
                 "@prefix owl: <http://www.w3.org/2002/07/owl#> .", ""]
        triples = []
        main = f"{L.IRI_BASE}scheme/emst-v2"
        triples.append((main, "a", "skos:ConceptScheme"))
        triples.append((main, "dct:title", self._lit("Environmental Management Skills Taxonomy", "en")))
        triples.append((main, "owl:versionInfo", self._lit(self.version)))
        triples.append((main, "dct:license", f"<{CC0_IRI}>"))
        for vf in sorted(L.VOCAB.glob("*.yaml")):
            v = L.load_yaml(vf)
            scheme = f"{L.IRI_BASE}vocab/{v.get('scheme', vf.stem)}"
            triples.append((scheme, "a", "skos:ConceptScheme"))
            triples.append((scheme, "dct:title", self._lit(str(v.get("title", vf.stem)), "en")))
            if v.get("schemeVersion"):
                triples.append((scheme, "owl:versionInfo", self._lit(str(v["schemeVersion"]))))
            for term in self._vocab_terms(v):
                iri = f"{scheme}/{term['notation']}"
                triples.append((iri, "a", "skos:Concept"))
                triples.append((iri, "skos:inScheme", f"<{scheme}>"))
                triples.append((iri, "skos:notation", self._lit(str(term["notation"]))))
                if term.get("prefLabel"):
                    triples.append((iri, "skos:prefLabel", self._lit(str(term["prefLabel"]), "en")))
                if term.get("definition"):
                    triples.append((iri, "skos:definition", self._lit(L.normalize_text(str(term["definition"])), "en")))
                if term.get("broader"):
                    triples.append((iri, "skos:broader", f"<{scheme}/{term['broader']}>"))
        for rid, r in released.items():
            if r.get("type") not in ("Competency", "Task", "KnowledgeStatement", "RoleProfile"):
                continue
            iri = L.iri(rid)
            triples.append((iri, "a", "skos:Concept"))
            triples.append((iri, "skos:inScheme", f"<{main}>"))
            for lang, txt in (r.get("prefLabel") or {}).items():
                triples.append((iri, "skos:prefLabel", self._lit(txt, lang)))
            for f in ("definition", "statement"):
                for lang, txt in (r.get(f) or {}).items() if isinstance(r.get(f), dict) else []:
                    triples.append((iri, "skos:definition" if f == "definition" else "skos:scopeNote", self._lit(txt, lang)))
            for n in r.get("notation", []):
                triples.append((iri, "skos:notation", self._lit(f"{n['scheme']}:{n['value']}")))
            for rb in r.get("replacedBy", []):
                if rb in released:
                    triples.append((iri, "dct:isReplacedBy", f"<{L.iri(rb)}>"))
        for set_name, rows in sorted(self._mapping_rows(released).items()):
            for m in rows:
                p = m.get("predicate_id", "")
                if not human_reviewed(m):
                    continue               # M11: an agent-drafted mapping is never asserted as a bare SKOS triple
                if p.startswith("skos:") and not m.get("predicate_modifier") and m.get("object_id") != "sssom:NoTermFound":
                    s, o = m.get("subject_id", ""), m.get("object_id", "")
                    if L.is_record_ref(s) and (L.is_record_ref(o) or o.startswith("http")):
                        triples.append((L.iri(s), p, f"<{L.iri(o) if L.is_record_ref(o) else o}>"))
        body = []
        for s, p, o in sorted(set(triples)):
            obj = o if (o.startswith('"') or o.startswith("<") or o.startswith("skos:")) else o
            body.append(f"<{s}> {p} {obj} .")
        return "\n".join(lines + body) + "\n"

    @staticmethod
    def _vocab_terms(v):
        out = []

        def add(t, broader=None):
            if isinstance(t, dict) and t.get("notation") is not None:
                out.append({"notation": t["notation"], "prefLabel": t.get("prefLabel"), "definition": t.get("definition"), "broader": broader})
                for sub in ("subtypes", "subfunctions", "components", "clusters"):
                    for c in t.get(sub, []) or []:
                        add(c, t["notation"])
        for t in v.get("terms", []) or []:
            add(t)
        return [t for t in out if re.fullmatch(r"[A-Za-z0-9._-]+", str(t["notation"]))]

    # ---------------------------------------------------------------- SSSOM
    def _mapping_rows(self, released):
        if hasattr(self, "_mcache"):
            return self._mcache
        sets = {}
        cw = self.data / "crosswalks"
        for tsv in sorted(cw.rglob("*.sssom.tsv")) if cw.exists() else []:
            lines = [ln for ln in tsv.read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")]
            if not lines:
                continue
            header = lines[0].split("\t")
            rows = [dict(zip(header, ln.split("\t"))) for ln in lines[1:]]
            name = str(tsv.relative_to(cw))[: -len(".sssom.tsv")]
            if name.startswith("emst-v1/"):
                self._x1_source_subjects = len({r.get("subject_id") for r in rows})
            out_rows, by_subject = [], defaultdict(list)
            for r in rows:
                obj = r.get("object_id", "")
                subj = r.get("subject_id", "")
                orec = self.records.get(obj)
                if orec is not None and self.is_held(obj, orec) or obj in self.held_keys:
                    by_subject[subj].append(None)
                    continue
                if L.is_record_ref(subj) and subj not in released:
                    continue              # subject not in this release (unreleased, unminted or unauthored; ADR-0031 §6)
                r = dict(r)
                if L.is_record_ref(obj) and obj not in released:
                    if r.get("predicate_id") not in SUCCESSOR_RELATIONS:
                        self.redacted["not in this release"] += 1
                        continue          # a non-successor mapping to unreleased content is not in this release
                    r["object_id"] = "sssom:NoTermFound"
                    r["predicate_id"] = "emst:successorNotReleased"      # never a positive NoTermFound (M9, m5)
                    r["comment"] = (r.get("comment", "") + "; " + X1_NOT_RELEASED).strip("; ")
                by_subject[subj].append(r)
            for subj, items in by_subject.items():
                kept = [x for x in items if x is not None]
                if kept:
                    out_rows.extend(kept)
                else:
                    # every successor is held: the row says only what any unreleased successor says (m14)
                    template = next(r for r in rows if r.get("subject_id") == subj)
                    out_rows.append({**template, "object_id": "sssom:NoTermFound", "comment": X1_NOT_RELEASED,
                                     "predicate_id": "emst:successorNotReleased"})
            dec_rx = re.compile(r"^(decision=[a-z-]+)")
            for r in out_rows:
                m = dec_rx.match(r.get("comment", "") or "")
                if m and "withheld" in r.get("comment", ""):
                    r["comment"] = m.group(1) + "; " + r["comment"].split("; ", 1)[-1]
                if name.startswith("emst-v1/") and self._names_held(r.get("comment", "")):
                    decision = m.group(1).split("=", 1)[1] if m else ""
                    r["comment"] = (X1_HELD_COMMENT.format(decision=decision)
                                    if decision and not any(rx.search(decision) for rx in self.triggers) else X1_NOT_RELEASED)
                if "held_variants=" in (r.get("other") or ""):      # m14: no per-row marker of held variants
                    r["other"] = ";".join(x for x in r["other"].split(";") if not x.startswith("held_variants="))
            sets[name] = out_rows
        self._mcache = sets
        return sets

    def _held_bare(self):
        """Held seed keys and their bare candidate IDs (seed:TN-C11 -> TN-C11), as boundary-anchored patterns."""
        if not hasattr(self, "_held_rx"):
            keys = set(self.held_keys)
            bare = {k[len("seed:"):] for k in keys if k.startswith("seed:")}
            self._held_rx = [(k, re.compile(r"(?<![A-Za-z0-9._/:-])" + re.escape(k) + r"(?![A-Za-z0-9._/-])")) for k in sorted(keys)]
            self._bare_rx = [(b, re.compile(r"(?<![A-Za-z0-9-])" + re.escape(b) + r"(?![0-9A-Za-z])")) for b in sorted(bare)]
        return self._held_rx, self._bare_rx

    def _names_held(self, text: str) -> bool:
        held_rx, bare_rx = self._held_bare()
        return any(rx.search(text or "") for _, rx in held_rx + bare_rx)

    def sssom(self, released):
        files = {}
        cw = self.data / "crosswalks"
        for name, rows in sorted(self._mapping_rows(released).items()):
            src = cw / f"{name}.sssom.tsv"
            header = [ln for ln in src.read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")][0].split("\t")
            files[f"sssom/{name}.sssom.tsv"] = L.csv_text(header, [{k: r.get(k, "") for k in header} for r in rows], delimiter="\t").encode()
            meta = cw / f"{name}.sssom.yml"
            if meta.exists():
                m = L.load_yaml(meta)
                m["mapping_set_version"] = f"{m.get('mapping_set_version', '0')}+emst.{self.version}"
                files[f"sssom/{name}.sssom.yml"] = L.dump_yaml(m).encode()
            strict = self._strict_rows(rows)
            if strict is not None:                      # CR-IA-002 #4: generated SSSOM 1.0-strict rendering, never a source
                hdr = header + ([] if "other" in header else ["other"])
                files[f"sssom/strict-1.0/{name}.sssom.tsv"] = L.csv_text(hdr, [{k: r.get(k, "") for k in hdr} for r in strict], delimiter="\t").encode()
        return files

    def _strict_rows(self, rows):
        only = set(L.load_yaml(L.VOCAB / "mapping_predicates.yaml").get("justifications_sssom_1_1_only") or [])
        if not any(r.get("mapping_justification") in only for r in rows):
            return None
        out = []
        for r in rows:
            r = dict(r)
            j = r.get("mapping_justification")
            if j in only:
                r["mapping_justification"] = "semapv:UnspecifiedMatching"
                other = r.get("other") or ""
                if "original_justification=" not in other:
                    r["other"] = ";".join(x for x in (other, f"original_justification={j}") if x)
            out.append(r)
        return out

    # ---------------------------------------------------------------- computed views (ADR-0021; ADR-0029 §4)
    def _stamp(self, rule):
        st = registry.stamp(self.rules, rule, self.commit)
        self.stamped.add((rule, st["ruleVersion"]))
        return st

    def _tool_names(self, released):
        names = []
        for r in released.values():
            if r.get("type") == "Tool" and r.get("toolType") in ("software-product", "platform", "model", "dataset-product", "instrument-model"):
                names += [v for v in (r.get("prefLabel") or {}).values() if isinstance(v, str)] + list(r.get("productExamples") or [])
        return names

    @staticmethod
    def three_module_recurrence(released):
        """Core practice competencies -> distinct modules where they recur (module enactments, supporting tasks'
        home modules, role profiles that target them) (CR-DB-001 #1; reported, never stored)."""
        rec = {cid: set() for cid, c in released.items() if c.get("type") == "Competency" and c.get("module") == "core"
               and c.get("competencyType") == "practice" and c.get("status") not in ("superseded", "withdrawn")}
        for r in released.values():
            t = r.get("type")
            if t == "Enactment" and r.get("enactmentKind") == "module" and r.get("competency") in rec:
                rec[r["competency"]].add(r.get("enactedInModule"))
            elif t == "Task" and r.get("status") not in ("superseded", "withdrawn"):
                for s in r.get("supports") or []:
                    if isinstance(s, dict) and s.get("competency") in rec:
                        rec[s["competency"]].add(r.get("homeModule") or r.get("module"))
            elif t == "RoleProfile":
                for ct in r.get("competencyTargets") or []:
                    if isinstance(ct, dict) and ct.get("competency") in rec:
                        rec[ct["competency"]].add(r.get("homeModule") or r.get("module"))
        return {c: sorted(m - {None, "core"}) for c, m in rec.items()}

    def views(self, released):
        st = self._stamp
        files = {}
        self.rating_breakdown = self.ratings_by_rater_type(released)
        counts = {**st("counts"), "release": self.version,
                  "byType": dict(sorted(Counter(r["type"] for r in released.values()).items())),
                  "competenciesByKind": dict(sorted(Counter(r.get("competencyType", "unset") for r in released.values() if r["type"] == "Competency").items())),
                  "competenciesByModule": dict(sorted(Counter(r.get("module") for r in released.values() if r["type"] == "Competency").items())),
                  "byLifecycle": dict(sorted(Counter(r.get("lifecycleState", "unset") for r in released.values() if r["type"] in ("Competency", "Task", "RoleProfile")).items())),
                  "coreCompetencies": sum(1 for r in released.values() if r["type"] == "Competency" and r.get("module") == "core" and r.get("status") not in ("superseded", "withdrawn")),
                  "excluded": dict(sorted(self.excluded.items()))}
        if counts["ruleVersion"] != "1.0.0":                    # counts@1.1.0 (ADR-0031 §9)
            comps = [r for r in released.values() if r["type"] == "Competency"]
            counts.update({
                "competenciesByModuleAndKind": {m: dict(sorted(Counter(r.get("competencyType", "unset") for r in comps if r.get("module") == m).items()))
                                                for m in sorted({r.get("module") for r in comps})},
                "competenciesByLifecycle": dict(sorted(Counter(r.get("lifecycleState", "unset") for r in comps).items())),
                "rolesByTier": dict(sorted(Counter(self._tier(r) for r in released.values() if r["type"] == "RoleProfile").items())),
                "variantsBySectorActor": dict(sorted(Counter(r.get("sectorActor", "unset") for r in released.values() if r["type"] == "RoleVariant").items())),
                "heldRecords": self.excluded.get(EXCLUDE_HELD, 0),
                "redactedReferences": dict(sorted(self.redacted.items())),
                "deferredTargets": self.deferred_targets(released)})
            keys = ["ruleId", "ruleVersion", "buildCommit", "release", "byType", "competenciesByKind",
                    "competenciesByModule", "competenciesByModuleAndKind", "competenciesByLifecycle",
                    "byLifecycle", "rolesByTier", "variantsBySectorActor", "coreCompetencies",
                    "heldRecords", "excluded", "redactedReferences", "deferredTargets"]
            if _semver(counts["ruleVersion"]) >= (1, 2, 0):          # counts@1.2.0 (m12; REQUESTS_FOR_DATA R4)
                counts.update(self.rating_breakdown)
                keys += ["ratingsByRaterType", "ratingUnitsByRaterType", "changeSignalObservations"]
            counts = {k: counts[k] for k in keys}
        self.counts = counts
        files["views/counts.json"] = counts
        files["views/inverse_links.json"] = inverse_links.view_rows(self.inverse, st("inverse-links"))
        # effective-use-tier@1.0.0: header pins IO's tier requirements; lint caps from IO's linter with our waivers
        req_file = "validation/indicator_lint_rules.yaml"
        req_doc = L.load_yaml(L.ROOT / req_file) if (L.ROOT / req_file).exists() else {}
        tier_req = ((req_doc.get("publication_rules") or {}).get("tier_requirements")) or {}
        lint, self.waived = io_bridge.lint(released, self.waivers, self._tool_names(released))
        eut_stamp = st("effective-use-tier")
        files["views/effective_use_tier.json"] = {
            "header": {**eut_stamp, "tierRequirements": f"{req_file}#publication_rules.tier_requirements",
                       "tierRequirementsSha256": io_bridge.file_sha256(req_file),
                       "lintEngine": "validation/lint_indicators.py" if lint is not None else "unavailable (every Indicator capped at develop)",
                       "waivers": len(self.waivers)},
            "rows": effective_use_tier.compute(released, tier_req, lint, eut_stamp)}
        files["views/assessment_staleness.json"] = assessment_staleness.compute(released, st("assessment-staleness"))
        # M8 (REQUESTS_FOR_BUILD R-03): the bundle marks every stale rating where it is read; computed, never stored
        self.stale_ids = assessment_staleness.stale_ids(released) if hasattr(assessment_staleness, "stale_ids") else set()
        # change-indicator@1.0.0 over released signals and external-index assessments
        ci_stamp = st("change-indicator")
        inputs = [r for r in released.values() if r["type"] == "ChangeSignal"
                  or (r["type"] == "ExposureAssessment" and r.get("raterType") == "external-index")]
        files["views/change_indicators.json"] = {
            "header": {**ci_stamp, "inputs": len(inputs), "note": "Only signalStatus active counts; watch signals feed the 'what's coming' view (ifWatchCounted)."},
            "rows": change_indicator.view_rows(inputs, stamp=ci_stamp)}
        # display-gate@1.0.0 with agreement results emitted from declared studies (none before the S2 studies)
        dg_stamp = st("display-gate")
        ratings = [r for r in released.values() if r["type"] in L.RATING_TYPES]
        results = agreement.emit(ratings, agreement.load_studies(self.data), dg_stamp)
        for sid, res in results.items():
            files[f"views/agreement/{sid}.json"] = res
        files["views/agreement/index.json"] = {**dg_stamp, "schema": "validation/display_gates.yaml#agreement_result_schema",
                                               "studies": sorted(results)}
        files["views/display_gate.json"] = gated_values.compute(released, self.rules["display-gate"], results, dg_stamp)
        files["views/venue_applicability.json"] = self.venue_overlay(
            venue_applicability.compute(released, self.date, st("venue-applicability")))
        # HR and mobility views (RULINGS_FOR_DE §19; CR-FH-001, CR-CP-001): released records and released mappings only
        mappings = self._mapping_rows(released)
        files.update(federal_series_profile.compute(released, mappings, st("federal-series-profile"), self.date))
        files.update(state_class_view.compute(released, st("state-class-view")))
        files["views/job_families.json"] = job_family_membership.compute(released, self.rules["job-family-membership"], st("job-family-membership"))
        files.update(role_change.compute(released, files["views/display_gate.json"], self.date, st("role-change")))
        files["views/mirror_links.json"] = mirror_links.compute(released, mappings, st("mirror-links"))
        files["views/pathway_edges.json"] = pathway_edges.compute(released, st("pathway-edges"))
        self.recurrence = self.three_module_recurrence(released)
        self.view_docs = files
        return {k: L.dump_json(v).encode() for k, v in files.items()}

    def venue_overlay(self, view: dict) -> dict:
        """m4: a venue value must not be an artifact of withholding. Where any of a row's actor enactments lost a
        requires, enables or constrains link to redaction, the value is `indeterminate (basis withheld)`."""
        hit = 0
        for r in view.get("rows") or []:
            if set(r.get("enactments") or []) & self.basis_withheld:
                r["venueApplicability"] = VENUE_WITHHELD
                r["basisWithheld"] = True
                hit += 1
                if r.get("sectorActor") == "federal" and r.get("competency") in (view.get("federal") or {}):
                    f = view["federal"][r["competency"]]
                    f["federalApplicability"] = VENUE_WITHHELD
                    f["note"] = (f.get("note", "") + " A basis link was withheld from this release, so the value is "
                                 "indeterminate.").strip()
        view.setdefault("header", {})["basisWithheldOverlay"] = (
            f"{hit} rows set to '{VENUE_WITHHELD}': an actor enactment lost a requires, enables or constrains link "
            "because its instrument is not in this release (scripts/build_release.py#venue_overlay; review m4)")
        return view

    @staticmethod
    def ratings_by_rater_type(released):
        """m12 (counts@1.2.0): ratings by type and raterType, with distinct rated units and distinct raterIds, and
        ChangeSignal records against distinct observations."""
        from rules.agreement import unit
        recs, units, raters = defaultdict(Counter), defaultdict(lambda: defaultdict(set)), defaultdict(lambda: defaultdict(set))
        for r in released.values():
            t = r.get("type")
            if t not in L.RATING_TYPES:
                continue
            rt = r.get("raterType") or "unset"
            recs[t][rt] += 1
            units[t][rt].add(f"{unit(r)}|{r.get('object') or ''}")      # a RelevanceRating unit is subject x object
            raters[t][rt].add(str(r.get("raterId")))
        sig = [r for r in released.values() if r.get("type") == "ChangeSignal"]
        obs = {r.get("observationId") or r["id"] for r in sig}
        return {"ratingsByRaterType": {t: dict(sorted(c.items())) for t, c in sorted(recs.items())},
                "ratingUnitsByRaterType": {t: {rt: {"units": len(units[t][rt]), "raterIds": len(raters[t][rt])}
                                               for rt in sorted(units[t])} for t in sorted(units)},
                "changeSignalObservations": {"records": len(sig), "distinctObservations": len(obs),
                                             "observationIdRecorded": sum(1 for r in sig if r.get("observationId"))}}

    # ---------------------------------------------------------------- delta, notes, self-check
    def delta(self, released):
        prev = {}
        if self.previous and Path(self.previous).exists():
            doc = json.loads(Path(self.previous).read_text(encoding="utf-8"))
            prev = {r["id"]: r for r in doc.get("@graph", []) if isinstance(r, dict) and r.get("id") and r.get("type") not in ("Mapping", "Release")}
        cur = {rid: r for rid, r in released.items()}
        out = {"from": str(self.previous or ""), "to": self.version, "added": [], "changed": [], "superseded": [], "withdrawn": []}
        for rid, r in cur.items():
            if rid not in prev:
                out["added"].append(rid)
            elif json.dumps(prev[rid], sort_keys=True) != json.dumps(r, sort_keys=True):
                status = r.get("status")
                key = status if status in ("superseded", "withdrawn") and prev[rid].get("status") != status else "changed"
                out[key].append(rid)
        return out

    @staticmethod
    def _tier(role):
        for n in role.get("notation") or []:
            if isinstance(n, dict) and n.get("scheme") == "MVPtier":
                return str(n.get("value"))
        return "unset"

    def seed_map(self):
        p = self.data / "ids" / "seed_map.csv"
        return {r["seed_key"]: r["id"] for r in L.read_csv(p)} if p.exists() else {}

    def deferred_targets(self, released):
        """Planned v2.0 targets (v1 disposition targets and candidates decided core-v2.0/module-v2.0) that are neither
        released nor held nor merged away, counted by area (counts@1.1.0). Keys are never listed (held keys could be)."""
        planned = {}
        t = self.data / "migration" / "v1_targets.csv"
        for r in (L.read_csv(t) if t.exists() else []):
            if r.get("target_key") and r.get("target_kind") in ("v1-seed", "candidate", "split-new", "enactment"):
                planned[r["target_key"]] = (r.get("area") or "core", r.get("held") == "true")
        cands = L.ROOT / "docs" / "decisions" / "candidate_disposition.csv"
        for r in (L.read_csv(cands) if cands.exists() else []):
            if r.get("decision") in ("core-v2.0", "module-v2.0"):
                tgt = r.get("target", "")
                m = re.match(r"^MOD-\w+\s+([a-z]+)", tgt)
                planned.setdefault(f"seed:{r['cand_id']}", ("core" if tgt.startswith("core") or not m else m.group(1), False))
        smap = self.seed_map()
        out = Counter()
        for key, (area, held_flag) in planned.items():
            rid = smap.get(key, key)
            rec = self.records.get(rid)
            if rid in released or held_flag or key in self.held_keys or (rec is not None and self.is_held(rid, rec)):
                continue
            if rec is not None and rec.get("status") in ("superseded", "withdrawn"):
                continue
            out[area] += 1
        return dict(sorted(out.items()))

    def delta_v1(self, released):
        """Delta against the v1 baseline (SPEC §12.5): v1 had no persistent IDs, so every rc.1 ID is new. For each v1
        competency and task, the X1 decision and the rc.1 successor IDs from the released X1 set (held successors appear
        only as a count; unreleased successors as NoTermFound)."""
        rows = (self._mapping_rows(released).get("emst-v1/emst-v1_to_v2") or [])
        by = defaultdict(lambda: {"decision": None, "successors": [], "notInRelease": 0})
        for r in rows:
            subj = r.get("subject_id", "")
            m = re.match(r"^decision=([a-z-]+)", r.get("comment", "") or "")
            e = by[subj]
            e["decision"] = e["decision"] or (m.group(1) if m else None)
            obj = r.get("object_id", "")
            if obj in released:
                e["successors"].append(obj)
            elif obj == "sssom:NoTermFound":
                e["notInRelease"] += 0 if r.get("predicate_id") == "emst:retiredWithoutReplacement" else 1
        items = [{"v1": k, "decision": v["decision"], "successors": sorted(set(v["successors"])), "successorsNotInRelease": v["notInRelease"]}
                 for k, v in sorted(by.items())]
        summary = Counter()
        for it in items:
            kind = "task" if re.search(r":T[1-3]$", it["v1"]) else "competency"
            state = "successor in this release" if it["successors"] else ("retired" if it["decision"] == "retire" else "no successor in this release")
            summary[f"{kind}: {state}"] += 1
        return {"from": "EMST v1 (copyB baseline; data/v1_baseline)", "to": self.version,
                "note": "v1 had no persistent IDs; every EMST ID in this release is added relative to v1. Per-key successors "
                        "come from the released X1 mapping set (ADR-0022). A decision is null where the released X1 rows "
                        "say only 'successor not in this release' (ADR-0007 §D: no per-key marker of held content).",
                "added": sorted(rid for rid in released if L.is_emst_id(rid)),
                "summary": dict(sorted(summary.items())), "v1Keys": items}

    def notes(self, released, delta):
        c = Counter(r["type"] for r in released.values())
        counts = getattr(self, "counts", {}) or {}
        pub = self.publication = release_gate.publication_status(
            self._mapping_rows(released), release_gate.load_signoff(self.version), getattr(self, "_x1_source_subjects", None))
        lines = [f"# EMST {self.version} — release notes (generated)", "",
                 f"- Released: {self.date} · schema {L.SCHEMA_VERSION} · build {self.commit} · profile `{self.profile}`",
                 f"- **Publication status: {pub['line']}** (release gate, `docs/decisions/PHASE4_BUILD_PLAN.md` §5; "
                 f"`docs/release/{self.version}/GATE_REPORT.md`). {release_gate.Q13}",
                 f"- **Authorship.** {AUTHORSHIP}",
                 f"- **Not validated.** {NOT_VALIDATED}",
                 f"- **IDs.** {ID_NOTICE} The registry rows are `candidate`; an adopter that imports them into an HCM system "
                 "should expect them to be confirmed, or deprecated with a successor (ADR-0010), at 2.0.0.",
                 f"- **Agent drafts.** {AGENT_DRAFT_NOTICE} Values moved into `agentDraft` in this bundle: {self.agent_draft_moved}.",
                 f"- Licence: CC0-1.0 for data and standard text (ADR-0013). {NOTICE}",
                 f"- {INDIGENOUS_STATEMENT}", "", "## Contents (counted by the build)", "", "| Entity | Records |", "|---|---|"]
        lines += [f"| {t} | {n} |" for t, n in sorted(c.items())] or ["| (none) | 0 |"]
        rb = getattr(self, "rating_breakdown", None) or {}
        if rb:
            src = (f"counts@{counts.get('ruleVersion')}" if "ratingsByRaterType" in counts
                   else "computed by the build; counts@1.2.0 adds it to views/counts.json")
            lines += ["", f"### Ratings by rater type and distinct units ({src})", "",
                      "Several passes of one model with one prompt family are one rater (one `raterId`); their agreement is "
                      "run-to-run consistency, not reliability.", "",
                      "| Rating type | Rater type | Records | Distinct units rated | Distinct raterIds |", "|---|---|---|---|---|"]
            for t, by in rb["ratingsByRaterType"].items():
                for rt, n in by.items():
                    u = rb["ratingUnitsByRaterType"].get(t, {}).get(rt, {})
                    lines.append(f"| {t} | {rt} | {n} | {u.get('units', '')} | {u.get('raterIds', '')} |")
            so = rb["changeSignalObservations"]
            lines += ["", f"ChangeSignal: {so['records']} records, {so['distinctObservations']} distinct observations "
                      + ("(by `observationId`)." if so["observationIdRecorded"] == so["records"] and so["records"]
                         else f"(`observationId` recorded on {so['observationIdRecorded']} of {so['records']}; a record without one counts as its own observation).")]
        if counts.get("ruleVersion", "1.0.0") != "1.0.0":
            def table(title, head, d):
                return ["", f"### {title}", "", f"| {head} | Records |", "|---|---|"] + ([f"| {k} | {v} |" for k, v in d.items()] or ["| (none) | 0 |"])
            lines += table("Competencies by kind", "Kind", counts.get("competenciesByKind", {}))
            lines += table("Competencies by module", "Module", counts.get("competenciesByModule", {}))
            mk = counts.get("competenciesByModuleAndKind", {})
            kinds = sorted({k for d in mk.values() for k in d})
            lines += ["", "### Competencies by module and kind", "", "| Module | " + " | ".join(kinds) + " |", "|---" * (len(kinds) + 1) + "|"]
            lines += [f"| {m} | " + " | ".join(str(d.get(k, 0)) for k in kinds) + " |" for m, d in mk.items()]
            lines += table("Competencies by lifecycle state", "Lifecycle state", counts.get("competenciesByLifecycle", {}))
            lines += table("Roles by tier (MVP role set)", "Tier", counts.get("rolesByTier", {}))
            lines += table("Role variants by sector actor", "Sector actor", counts.get("variantsBySectorActor", {}))
            lines += ["", "### Held and deferred", "",
                      f"- {HOLD_COUNT_LINE}: {counts.get('heldRecords', 0)}.",
                      f"- Planned v2.0 targets not in this release (deferred to rc.2 or a later wave), by area: "
                      + (", ".join(f"{k} {v}" for k, v in counts.get("deferredTargets", {}).items()) or "none") + "."]
        lines += ["", "## Excluded by the release gate", "", "| Reason | Records |", "|---|---|"]
        lines += [f"| {k} | {v} |" for k, v in sorted(self.excluded.items())] or ["| (none) | 0 |"]
        if self.redacted:
            lines += ["", "References removed from released records because their target is not released (by reason): "
                      + ", ".join(f"{k} {v}" for k, v in sorted(self.redacted.items())) + "."]
        if self.held_back:
            lines += ["", f"Records held back because removing those references would leave a required field empty: "
                      f"{len(self.held_back)} (never shipped with an emptied required field; review B1)."]
        if self.basis_withheld:
            lines += ["", f"Actor enactments that lost a requires, enables or constrains link to an instrument not in this "
                      f"release: {len(self.basis_withheld)}; their venue values read “{VENUE_WITHHELD}” (review m4)."]
        lines += release_gate.method_lines(
            self._mapping_rows(released), counts, (getattr(self, "view_docs", {}) or {}).get("views/change_indicators.json") or {},
            f"effective-use-tier@{self.rules['effective-use-tier']['version']}", self.data.parents[1] if self.data.name == "v2" else L.ROOT)
        lines += ["", "## Not in this release (SPEC §12.5, §17.2)", "",
                  f"rc.1 ships: {SHIPPED_ARTIFACTS}. It does not ship these artifacts that the SPEC says each release "
                  "carries:", ""] + [f"- {s}: {a}." for s, a in OMITTED_ARTIFACTS]
        waived = Counter(h.rule_id for h in getattr(self, "waived", []))
        lines += ["", "## Lint waivers applied (data/v2/governance/lint_waivers.csv)", "", "| Rule | Waived hits |", "|---|---|"]
        lines += [f"| {k} | {v} |" for k, v in sorted(waived.items())] or ["| (none) | 0 |"]
        low = sum(1 for m in getattr(self, "recurrence", {}).values() if len(m) < 3)
        lines += ["", "## Three-module recurrence (CR-DB-001; for the Editorial Board, not a gate)", "",
                  f"Core practice competencies recurring in fewer than three modules: {low} of {len(getattr(self, 'recurrence', {}))}."]
        core, held_core = self.core_size(released)
        lines += ["", "## Core size (G-9)", "", f"Core competencies: {core} released + held core reported as a count ({held_core}); "
                  f"range {G9_RANGE[0]}-{G9_RANGE[1]} (counts@{self.rules['counts']['version']})."]
        lines += ["", "## Computed-view rules", "", "| Rule | Version |", "|---|---|"]
        lines += [f"| {r} | {v} |" for r, v in sorted(self.stamped)]
        lines += ["", HOLD_POLICY_LINE, "", "## Delta", "",
                  f"Against the previous release ({delta['from'] or 'none given'}): added {len(delta['added'])} · changed {len(delta['changed'])} · superseded {len(delta['superseded'])} · withdrawn {len(delta['withdrawn'])} (delta.json).", ""]
        v1d = getattr(self, "v1delta", None)
        if v1d:
            lines += ["Against the v1 baseline (delta_v1.json; v1 had no persistent IDs, so every ID is added):", "",
                      "| v1 key kind and outcome | v1 keys |", "|---|---|"]
            lines += [f"| {k} | {v} |" for k, v in v1d["summary"].items()]
            lines += [""]
        return "\n".join(lines)

    def core_size(self, released):
        core = sum(1 for r in released.values() if r.get("type") == "Competency" and r.get("module") == "core"
                   and r.get("status") not in ("superseded", "withdrawn"))
        held_core = {rid for rid, r in self.records.items() if r.get("type") == "Competency" and r.get("module") == "core"
                     and r.get("status") not in ("superseded", "withdrawn") and self.is_held(rid, r)}
        # held candidates decided core-v2.0 count toward G-9 even before they are authored ("held items included")
        cands = L.ROOT / "docs" / "decisions" / "candidate_disposition.csv"
        if cands.exists():
            core_cands = {f"seed:{r['cand_id']}" for r in L.read_csv(cands) if r.get("decision") == "core-v2.0"}
            held_core |= {k for k in self.held_keys & core_cands if k not in self.records}
        return core, len(held_core)

    def g9_applies(self):
        """The G-9 gate applies to release builds of 2.0.0-rc.1 or later (not -dev, not the rc.0 test fixtures)."""
        m = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-(rc)\.(\d+))?$", self.version)
        if self.profile != "release" or not m:
            return False
        major, minor, patch, rc, n = m.groups()
        return (int(major), int(minor), int(patch)) > (2, 0, 0) or rc is None or int(n) >= 1

    def self_check(self, files):
        """Release gate re-applied to the output: no held key, no v1Seed, no pending-licence record, no Tribal text."""
        problems = []
        doc = json.loads(files["emst.bundle.jsonld"].decode("utf-8"))
        graph_text = json.dumps(doc["@graph"], ensure_ascii=False)
        others = "".join(v.decode("utf-8", "replace") for k, v in files.items() if k != "emst.bundle.jsonld")
        held_ids = {rid for rid, r in self.records.items() if self.is_held(rid, r)} | self.held_keys
        for k in sorted(held_ids):
            pat = re.compile(r"(?<![A-Za-z0-9._/:-])" + re.escape(k) + r"(?![A-Za-z0-9._/-])")
            if pat.search(graph_text) or pat.search(others):
                problems.append(f"held key {k} present in release output")
        if any('"v1Seed"' in json.dumps(r) for r in doc["@graph"]):
            problems.append("v1Seed present in bundle")
        _, bare_rx = self._held_bare()                    # bare candidate IDs of held keys (ADR-0030 §3.3; RULINGS §18.1)
        for b, rx in bare_rx:
            for name, blob in sorted(files.items()):
                if rx.search(blob.decode("utf-8", "replace")):
                    problems.append(f"held candidate ID {b} present in {name}")
                    break
        core, held_core = self.core_size(self.released)
        total = core + held_core
        if self.g9_applies() and not (G9_RANGE[0] <= total <= G9_RANGE[1]):
            problems.append(f"G-9: {total} core competencies (incl. held) outside {G9_RANGE[0]}-{G9_RANGE[1]}")
        elif not self.g9_applies():
            print(f"I-CORE-SIZE core competencies {core} + held {held_core} = {total} (G-9 range {G9_RANGE[0]}-{G9_RANGE[1]})")
        if THIRD_PARTY_LICENSE in graph_text or THIRD_PARTY_LICENSE in others:
            problems.append(f"{THIRD_PARTY_LICENSE} record present in release output (ADR-0029 §9.6)")
        for k in sorted(self.withheld):                    # ADR-0031 §8: withheld records are never named in a release
            pat = re.compile(r"(?<![A-Za-z0-9._/:-])" + re.escape(k) + r"(?![A-Za-z0-9._/-])")
            if pat.search(graph_text) or pat.search(others):
                problems.append(f"withheld key {k} present in release output")
        if self.profile == "release":                      # ADR-0031 §6: a release names minted IDs only
            unminted = sorted({s for r in doc["@graph"] for _, s in L.iter_strings(r) if L.is_seed(s)})
            if unminted:
                problems.append(f"{len(unminted)} unminted seed: references in the release bundle, e.g. {unminted[:3]}")
        for r in doc["@graph"]:
            for f in self.inverse_fields.get(r.get("type"), set()) - {"tools", "enactments", "tasks", "mirroredBy"}:
                if f in r:
                    problems.append(f"stored inverse {f} on {r.get('id')}")
        if self.licensing.get("v1Dedication") != "granted" and not self.include_pending and V1_LICENSE in graph_text:
            problems.append("v1-derived (pending dedication) record present in CC0 bundle")
        problems += self.trigger_scan(files)                # m14: every output file and every field
        problems += self.schema_check(doc)                  # B1: every bundle node conforms (SPEC §18.1)
        problems += self.context_check(doc)                 # M11: no bundle key is dropped by JSON-LD expansion
        if problems:
            raise SystemExit("release gate failed:\n  " + "\n  ".join(problems[:20])
                             + (f"\n  ... and {len(problems) - 20} more" if len(problems) > 20 else ""))

    # documented computed fields the bundle adds to records (inverse-links bundle_fields); stripped before validation
    BUNDLE_COMPUTED = {"tools", "enactments", "mirroredBy"}

    def schema_check(self, doc) -> list[str]:
        out, by_type = [], Counter()
        for node in doc["@graph"]:
            t = node.get("type")
            n = {k: v for k, v in node.items() if not (k in self.BUNDLE_COMPUTED and k in self.inverse_fields.get(t, set()))}
            errs = self.schema_errors(n)
            if errs:
                by_type[t] += 1
                if by_type[t] <= 3:
                    e = errs[0]
                    out.append(f"schema: {t} {node.get('id') or node.get('subject_id')} at /{'/'.join(map(str, e.absolute_path))}: {e.message[:160]}")
        if by_type:
            out.insert(0, f"schema: {sum(by_type.values())} bundle nodes fail schema/emst.schema.json: {dict(sorted(by_type.items()))}")
        return out

    def context_check(self, doc) -> list[str]:
        """Every key of every bundle node is a term of the shipped context (no @vocab, so an undefined key would be
        dropped on expansion), except inside @json literals and language maps."""
        ctx = doc["@context"]
        missing = Counter()

        def walk(o, path):
            if isinstance(o, list):
                for x in o:
                    walk(x, path)
                return
            if not isinstance(o, dict):
                return
            for k, v in o.items():
                if k.startswith("@"):
                    continue
                term = ctx.get(k)
                if term is None:
                    missing["/".join(path + (k,))] += 1
                    continue
                if isinstance(term, dict) and (term.get("@type") == "@json" or term.get("@container") == "@language"):
                    continue
                walk(v, path + (k,))
        for node in doc["@graph"]:
            walk(node, (str(node.get("type")),))
        return [f"context: {n} keys at {p} have no JSON-LD term (dropped on expansion)" for p, n in sorted(missing.items())]

    def trigger_scan(self, files) -> list[str]:
        """m14: the Tribal-hold triggers over every output file and every field: bundle (records, Mapping rows,
        provenance, the manifest), CSV, SSSOM TSV and YAML, SKOS, views, notes. Exempt only the build's own statements of
        the hold rule (which name no record) and SKOS triples about vocabulary concepts (SPEC §9.1)."""
        exempt = sorted({INDIGENOUS_STATEMENT, HOLD_COUNT_LINE, HOLD_POLICY_LINE, EXCLUDE_HELD}, key=len, reverse=True)
        vocab_subject = f"<{L.IRI_BASE}vocab/"
        out = []

        def hits(s):
            for e in exempt:
                s = s.replace(e, " ")
            return [rx.pattern for rx in self.triggers if rx.search(s)]

        def walk(o, path):
            if isinstance(o, str):
                yield path, o
            elif isinstance(o, dict):
                for k, v in o.items():
                    yield path + (f"<key {k}>",), k
                    yield from walk(v, path + (k,))
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    yield from walk(v, path + (i,))
        for name in sorted(files):
            text = files[name].decode("utf-8", "replace")
            if name.endswith((".json", ".jsonld")):
                doc = json.loads(text)
                nodes = doc["@graph"] if isinstance(doc, dict) and "@graph" in doc else [doc]
                for node in nodes:
                    rid = node.get("id") or node.get("subject_id") or node.get("recordId") if isinstance(node, dict) else None
                    for path, s in walk(node, ()):
                        h = hits(s)
                        if h:
                            out.append(f"Tribal-related text in {name} {rid or ''} at {'/'.join(map(str, path))} ({h[0]})")
                            break
            else:
                for i, line in enumerate(text.splitlines(), 1):
                    if name.endswith(".ttl") and line.startswith(vocab_subject):
                        continue
                    h = hits(line)
                    if h:
                        out.append(f"Tribal-related text in {name} line {i} ({h[0]})")
        return out


Release = Builder      # name used by vocab/rules/*.yaml#implementation ("scripts/build_release.py#Release.views")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", default="2.0.0-dev")
    ap.add_argument("--date")
    ap.add_argument("--profile", choices=["release", "preview"], default="release")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--data-root", type=Path, default=L.DATA_V2)
    ap.add_argument("--previous", type=Path)
    ap.add_argument("--include-pending-license", action="store_true", help="preview only; output is NOT for distribution")
    ap.add_argument("--no-validate", action="store_true")
    ap.add_argument("--build-commit")
    args = ap.parse_args(argv)
    if not args.no_validate:
        import validate_v2
        rep = validate_v2.Validator(args.data_root, strict=args.profile == "release", use_git_base=False).run()
        if rep.errors:
            for i in rep.errors[:30]:
                print(f"{i.code} {i.where} {i.message}")
            print(f"refusing to build: {len(rep.errors)} validation errors (run scripts/validate_v2.py{' --strict' if args.profile == 'release' else ''})")
            return 1
    b = Builder(args.data_root, args.profile, args.version, args.date, args.previous, args.include_pending_license, args.build_commit)
    out = args.out or (L.ROOT / "dist" / args.version)
    files = b.build(out)
    print(f"built {len(files)} files in {out} ({len(b.released)} records; excluded {dict(b.excluded)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
