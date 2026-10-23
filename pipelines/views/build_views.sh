#!/usr/bin/env bash
# Regenerate every WP-08 view from data/v2 (deterministic). Run after build_wp08.py and after any X4/X5/X11 re-run.
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 pipelines/views/federal_series_profile.py
python3 pipelines/views/state_class_view.py
python3 pipelines/views/job_families.py
python3 pipelines/views/change_view.py
python3 pipelines/views/mirror_links.py
python3 pipelines/views/forester_pd_fes.py
python3 pipelines/views/x2_frame_from_bundles.py
python3 -m pytest -q pipelines/views/tests
