# PlanOS Subsequent-Cycle Candidate Selection Authorization Grant v0.71

PlanOS v0.71 grants bounded authority to request selection from the candidate set authorized by v0.70.

It preserves the candidate-set, evaluation-set, and review-set digests, the reviewed eligible candidate identities, the authorization scope, and the authorization-constraints digest.

This layer grants selection authority only.

It does not request candidate selection, select a candidate, or request admission.

## Input

The source is `kuuos_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70`.

The source must be ready, contain a nonempty eligible candidate set, and remain ungranted and unselected.

## Output

The runtime emits `PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_GRANT_READY` when all checks pass.

The grant binds:

- source authorization-request receipt digest
- source authorization-request digest
- candidate-set digest
- evaluation-set digest
- review-set digest
- eligible candidate ids and digests
- authorization scope
- authorization-constraints digest
- grant-rationale digest
- authorization-grant digest

## Fail-closed conditions

The runtime blocks an invalid or incomplete source request, missing or duplicate eligible candidate identities, count mismatch, request-record mismatch, missing authorization scope or constraints digest, pre-granted authority, pre-requested selection, preselected candidates, premature admission, or missing grant rationale.

## Boundary

- subsequent-cycle candidate-selection authorization requested = true
- subsequent-cycle selection authority granted = true
- subsequent-cycle candidate selection requested = false
- subsequent-cycle candidate selected = false
- subsequent-cycle admission requested = false

Review evidence and eligibility do not themselves select a candidate.

The next layer may request candidate selection only from the preserved eligible candidate set and within the preserved authorization constraints.
