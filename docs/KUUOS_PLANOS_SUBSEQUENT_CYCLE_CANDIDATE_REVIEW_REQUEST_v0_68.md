# PlanOS Subsequent-Cycle Candidate Review Request v0.68

PlanOS v0.68 converts the v0.67 candidate-evaluation receipt into a bounded review request.

This layer requests review of the complete evaluation set.

It does not complete review, grant selection authority, select a candidate, or request subsequent-cycle admission.

## Input

The source input is `kuuos_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67`.

The source must be ready.

The source evaluation set must satisfy:

- nonempty candidate count
- evaluation count equal to candidate count
- evaluation-set digest validity
- unique candidate ids, candidate digests, and evaluation digests
- every materialized candidate evaluated
- bounded evaluation components
- evaluation order explicitly non-selective
- review, selection, and admission still unopened

The request also requires:

- review scope equal to `subsequent_cycle_candidate_evaluation_set`
- a nonempty review-criteria digest

## Output

The runtime emits `PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_REQUEST_READY` when all checks pass.

The output contains:

- selected-candidate provenance
- candidate-set digest and count
- evaluation-set digest and count
- review scope
- review-criteria digest
- candidate-review request record
- receipt digest

## Fail-closed conditions

The request is blocked when:

- the source candidate-evaluation receipt is not ready
- candidate and evaluation counts differ
- the evaluation list count differs from the recorded count
- candidate ids, candidate digests, or evaluation digests are duplicated
- evaluation ordinals are not exact
- the evaluation-set digest is invalid
- source record counts or digests do not match
- review has already been requested
- candidate selection or admission has already been promoted
- the review scope is invalid
- the review-criteria digest is missing
- selected-candidate provenance does not match the source record

## Required boundary

- request owned by PlanOS = true
- source candidate-evaluation receipt preserved = true
- selected-candidate provenance preserved = true
- candidate-set digest preserved = true
- evaluation-set digest preserved = true
- evaluation count exact preserved = true
- all materialized candidates evaluated preserved = true
- evaluation score bounds valid preserved = true
- evaluation order nonselection preserved = true
- prior memory, truth-authority, blocker-release, closeout, replan, generation, materialization, and evaluation chain preserved = true
- subsequent-cycle candidate-review request only = true
- subsequent-cycle candidate review requested = true
- subsequent-cycle review scope bound = true
- subsequent-cycle review-criteria digest bound = true

## Closed boundary

- subsequent-cycle selection authority granted = false
- subsequent-cycle candidate review completed = false
- subsequent-cycle candidate selected = false
- subsequent-cycle admission requested = false

## Formal guarantees

The Lean bridge requires:

- candidate count is positive
- evaluation count equals candidate count
- review scope and review-criteria digest are bound
- review request is opened without selection authority
- review completion remains closed
- candidate selection remains closed
- admission remains closed

## Authority boundary

This layer creates a review request only.

The requester remains non-authoritative and cannot convert evaluation order or scores into selection authority.
