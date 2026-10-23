#!/usr/bin/env bash
# Rebuild every WP-09 mapping set and register from its curation inputs, then validate and count.
# Requires: python3 with pyyaml, numpy, scikit-learn, rank_bm25 (wordllama optional); for X7 the ESCO skills file
# and labels (ESCO_SKILLS, ESCO_LABELS); for X2 the O*NET cache (EMST_ONET_CACHE; see pipelines/onet/fetch_onet.py);
# sssom-py (SSSOM_BIN) for SSSOM 1.0 validation. Licence: Apache-2.0.
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 pipelines/crosswalks/x3_soc.py
python3 pipelines/crosswalks/x4_opm_series.py
python3 pipelines/crosswalks/x5_state_classes.py
if [[ -n "${ESCO_SKILLS:-}" ]]; then
  python3 pipelines/crosswalks/x7_esco.py --esco-skills "$ESCO_SKILLS" ${ESCO_LABELS:+--esco-labels "$ESCO_LABELS"}
fi
python3 pipelines/crosswalks/x8_x11_private.py
python3 pipelines/crosswalks/x9_ecq.py
if [[ -n "${EMST_ONET_CACHE:-}" ]]; then
  python3 pipelines/x2/build_candidates.py --release "${ONET_RELEASE:-27.2}" --k 6
  # Coder B is a separate blind LLM pass, run by hand (needs the claude CLI; see CODING_PROTOCOL.md §4):
  #   python3 pipelines/x2/run_coder_b.py run|write --release 27.2 --workdir <scratch dir outside the repo>
  python3 pipelines/x2/merge_x2.py --release "${ONET_RELEASE:-27.2}"
  python3 pipelines/x2/kappa.py pipelines/x2/coding/coder-a.csv pipelines/x2/coding/coder-b.csv --out pipelines/x2/work/x2_kappa.json
fi
python3 pipelines/crosswalks/validate_sets.py
python3 pipelines/crosswalks/report_counts.py > /dev/null
python3 scripts/validate_v2.py
