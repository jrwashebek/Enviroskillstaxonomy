"""EMST competency-level linker (DP-18; ADR-0019).

A transparent candidate generator that maps text describing work demands (postings, position descriptions, plan
requirements, curricula) onto EMST v2 competencies, using the full competency document, and records the
best-supported task as `emst:evidencesTask` evidence. It is a candidate generator for human review, not a coder.

Rules carried from ADR-0019 and enforced in code:
- link to competencies now; tasks only when DP-18a fires for a family (``config.TASK_TARGET_FAMILIES`` is empty);
- never publish uncorrected top-1 counts: ``quality.aggregate`` refuses to run without a held-out gold-set
  evaluation and returns misclassification-corrected shares with bootstrap intervals;
- PII stripping and Tribal quarantine run before linking (``safety``);
- input text is untrusted data, never instructions;
- every output row carries the linker version, index hash and corpus release.

Phase 2 prototype lineage: docs/research/interop-skills-intelligence/prototype/ (v1 competencies). This package
indexes v2 records under data/v2. Licence: Apache-2.0.
"""
__version__ = "0.2.0"
