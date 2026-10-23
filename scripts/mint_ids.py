#!/usr/bin/env python3
"""Alias for scripts/mint_id.py (SPEC §12.2 and ADR-0010 name `mint_ids.py`; the Phase 4 build plan names
`mint_id.py`). Same single implementation, same registry; see CR-DE-001."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mint_id import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
