# PlanOS Subsequent-Cycle Candidate Selection Request v0.72

PlanOS v0.72 converts the bounded selection authority granted by v0.71 into an explicit candidate selection request.

This layer requests selection only.

It does not select a candidate and does not request admission.

## Inputs

The source is `kuuos_planos_subsequent_cycle_candidate_selection_authorization_grant_v0_71`.

The request preserves:

- candidate-set digest
- evaluation-set digest
- review-set digest
- exact selection-eligible candidate identities
- authorization scope
- authorization-constraints digest
- source authorization-grant receipt digest
- source authorization-grant digest

## Output

The runtime emits `PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_REQUEST_READY` when the authorization grant is ready, internally consistent, and non-promoted beyond its boundary.

The request binds a selection scope and selection-criteria digest.

## Fail-closed conditions

The runtime blocks:

- invalid or incomplete authorization grants
- missing grant records or grant digests
- missing or duplicate eligible candidate identities
- eligible-count mismatch
- grant-record mismatch
- missing selection scope
- missing selection criteria
- pre-requested selection
- preselected candidates
- premature admission

## Boundary

- candidate-selection authorization requested = true
- selection authority granted = true
- candidate selection requested = true
- candidate selected = false
- admission requested = false

Review order and total score remain evidence rather than automatic selection authority.
