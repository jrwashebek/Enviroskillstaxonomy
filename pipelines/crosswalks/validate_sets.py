#!/usr/bin/env python3
"""Validate EMST mapping sets against SSSOM 1.0 (sssom-py) and the EMST crosswalk profile (sssomlib.check_rows).

Usage:
  python pipelines/crosswalks/validate_sets.py [--sssom-bin PATH] [--profile-only] [TSV ...]

Without TSV arguments every `data/v2/crosswalks/**/*.sssom.tsv` except X1 (DE-owned, different profile) is checked.
For the SSSOM check the external `.sssom.yml` is embedded as a commented header in a temporary copy (SSSOM/TSV
embedded mode) and `sssom validate -V JsonSchema -V PrefixMapCompleteness -V StrictCurieFormat` is run. sssom-py
pins SSSOM 1.0 through `sssom-schema 1.0.0`; the 1.1 slots `record_id` and `reviewer_agreement` are declared under
`extension_definitions` (V4-13). Exit status 1 on any error. Licence: Apache-2.0.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sssomlib as S  # noqa: E402


# semapv justification values that SSSOM 1.1 adds and the SSSOM 1.0 schema pattern rejects: accepted as a declared
# extension until 1.1 is final (CR-IA-002 ruling; vocab/mapping_predicates.yaml#justifications_sssom_1_1_only).
V11_JUSTIFICATIONS = tuple(S.L.load_yaml(S.L.VOCAB / "mapping_predicates.yaml").get(
    "justifications_sssom_1_1_only", ["semapv:LLMBasedMatching"]))


def sssom_check(tsv: Path, sssom_bin: str, allow_11_values: bool) -> tuple[bool, str]:
    """Run sssom-py validation. With allow_11_values, rows using a 1.1-only justification value are checked with
    that one value replaced by semapv:UnspecifiedMatching in a temporary copy, so every other slot is still tested
    against the 1.0 schema; the substitution count is reported, never hidden."""
    yml = tsv.with_name(tsv.name[: -len(".sssom.tsv")] + ".sssom.yml")
    with tempfile.TemporaryDirectory() as td:
        emb = Path(td) / tsv.name
        head = "".join("#" + ln + "\n" for ln in yml.read_text(encoding="utf-8").splitlines())
        body = tsv.read_text(encoding="utf-8")
        nsub = 0
        if allow_11_values:
            for v in V11_JUSTIFICATIONS:
                nsub += body.count("\t" + v + "\t")
                body = body.replace("\t" + v + "\t", "\tsemapv:UnspecifiedMatching\t")
        emb.write_text(head + body, encoding="utf-8")
        p = subprocess.run([sssom_bin, "validate", str(emb), "-V", "JsonSchema", "-V", "PrefixMapCompleteness",
                            "-V", "StrictCurieFormat"], capture_output=True, text=True, timeout=600, cwd=td)
        out = (p.stdout + p.stderr).strip()
        bad = p.returncode != 0 or any(w in out.lower() for w in ("error", "traceback", "invalid", "missing prefix"))
        if allow_11_values:
            out = f"[{nsub} rows use a SSSOM 1.1 justification value]" + ("\n" + out if out else "")
        return (not bad), out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tsv", nargs="*")
    ap.add_argument("--sssom-bin", default=os.environ.get("SSSOM_BIN") or shutil.which("sssom") or "")
    ap.add_argument("--profile-only", action="store_true")
    a = ap.parse_args()
    files = [Path(t).resolve() for t in a.tsv] or sorted(p for p in S.XW.rglob("*.sssom.tsv") if p.parent.name != "emst-v1")
    preds, justs = S.vocab_terms()
    failed = False
    for tsv in files:
        rows = S.read_set(tsv)
        errs = S.check_rows(rows, preds, justs)
        status = "ok" if not errs else f"{len(errs)} profile errors"
        line = f"{tsv.relative_to(S.ROOT)}: rows={len(rows)} profile={status}"
        if errs:
            failed = True
            line += "\n  " + "\n  ".join(errs[:10])
        if not a.profile_only:
            if not a.sssom_bin:
                line += " sssom=SKIPPED (sssom-py not installed; pip install sssom==0.4.15)"
            else:
                ok_strict, out_strict = sssom_check(tsv, a.sssom_bin, allow_11_values=False)
                ok, out = sssom_check(tsv, a.sssom_bin, allow_11_values=True)
                line += (f" sssom-1.0-strict={'ok' if ok_strict else 'FAIL (1.1 justification values; CR-IA-002)'}"
                         f" sssom-1.0+1.1-values={'ok' if ok else 'FAIL'}")
                if out:
                    line += "\n  " + out.replace("\n", "\n  ")[:1500]
                failed |= not ok
        print(line)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
