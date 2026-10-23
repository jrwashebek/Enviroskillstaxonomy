# Pending items for the CA at WP-16 integration

Items that a build agent prepared but could not apply because the target is outside its lane. Each needs a CA
decision (accept / change / reject) and, if accepted, application by the lane owner.

## P-01 Activate display-gate rule 1.1.0 (from IO, S2 work order; CR-CP-001 B4)
- IO implemented `validation/display_gates.yaml` 1.1.0 (`role_profile_values`) and `validation/display_gate.py#decide_role_value`, with tests.
- Proposed change in `vocab/rules/` (CA lane): `display-gate@1.0.0.yaml` → `status: superseded`, `supersededBy: display-gate@1.1.0`; `display-gate@1.1.0.yaml` → `status: active`, append an activation note to `changeNote`.
- IO's judgment calls for CA to confirm: (a) reviewed job-analysis values display with marker `editorial` and the review status in the label, rather than a new "reviewed" decision value; (b) editorial design values may show in develop views only after a `pid:` reviewer has reviewed them; (c) View 2 shows unreviewed target levels only in describe-tier views.
- DE follow-up if accepted: `scripts/rules/gated_values.py` must call `decide()` for role rows with `field`, `validationStatus`, `reviewers`, `context`.
