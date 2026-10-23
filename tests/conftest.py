"""Shared test helpers for the EMST v2 pipeline tests (WP-01/WP-02)."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
FIXTURES = ROOT / "tests" / "fixtures"

import emstlib as L  # noqa: E402


def overlay_tree(tmp_path: Path, *overlays: Path) -> Path:
    """Copy the valid base fixture tree, then each overlay, into tmp_path; return the data/v2 root."""
    shutil.copytree(FIXTURES / "trees" / "base", tmp_path, dirs_exist_ok=True)
    for ov in overlays:
        shutil.copytree(ov / "data", tmp_path / "data", dirs_exist_ok=True)
    return tmp_path / "data" / "v2"


@pytest.fixture(scope="session")
def real_report():
    """One full validation of the repository data (about 20 s), shared by the migration tests."""
    import validate_v2
    return validate_v2.Validator(L.DATA_V2, use_git_base=False).run()
