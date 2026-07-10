# PlanOS Subsequent-Cycle Candidate Selection Authorization Request v0.70

PlanOS v0.70 consumes the completed v0.69 candidate review receipt and emits a bounded request for candidate-selection authority.

This layer does not grant authority and does not select a candidate.

## Source

The source must be `kuuos_planos_subsequent_cycle_candidate_review_receipt_v0_69` in ready state.

The candidate, evaluation, and review counts must agree.

The review-set digest must validate against the recorded review outcomes.

At least one reviewed candidate must be selection eligible.

## Output

The request preserves:

- candidate-set digest
- evaluation-set digest
- review-set digest
- exact candidate, evaluation, and review counts
- eligible candidate ids and candidate digests
- selection-eligible count
- authorization scope
- authorization-constraints digest

The request records `subsequent_cycle_candidate_selection_authorization_requested = true`.

## Closed boundary

The following remain false:

- `subsequent_cycle_selection_authority_granted`
- `subsequent_cycle_candidate_selection_requested`
- `subsequent_cycle_candidate_selected`
- `subsequent_cycle_admission_requested`

Review order and total score remain evidence rather than selection authority.

## Fail-closed conditions

The runtime blocks missing or malformed review receipts, incomplete review coverage, count mismatch, review-set tampering, missing eligible candidates, duplicate eligible identities, pre-granted selection authority, pre-requested selection, preselected candidates, and premature admission.

## Formal boundary

The Lean bridge proves that the source review is bound, review completion and eligibility are preserved, at least one eligible candidate exists, authorization is requested, and authority grant, selection request, candidate selection, and admission remain closed.
