# PlanOS Subsequent-Cycle Candidate Selection Authorization Request v0.70

PlanOS v0.70 converts the completed v0.69 candidate review into a bounded request for candidate-selection authority.

This layer requests authority only.

It does not grant authority, request execution of selection, select a candidate, or request subsequent-cycle admission.

## Input

The source is `kuuos_planos_subsequent_cycle_candidate_review_receipt_v0_69`.

The source must preserve the complete materialization, evaluation, review-request, and review-receipt chain.

The source must establish:

- candidate count is positive
- evaluation count equals candidate count
- review count equals evaluation count
- review-set digest is valid
- all evaluated candidates were reviewed
- candidate review is complete
- selection eligibility is recorded
- at least one candidate is selection eligible
- selection authority, selection request, candidate selection, and admission remain unopened

## Eligible candidate set

The runtime projects only review outcomes with `selection_eligible = true`.

Each projected entry preserves:

- candidate id
- candidate digest
- evaluation digest
- review digest
- total score
- review disposition

The projected list is bound by `selection_eligible_set_digest`.

The eligible set remains evidence and does not itself select a candidate.

## Request parameters

The selection scope must equal `subsequent_cycle_selection_eligible_candidates`.

A nonempty selection-policy digest is required.

## Output

The runtime emits `PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_REQUEST_READY` when all checks pass.

The output records:

- source review-receipt digest
- candidate, evaluation, and review-set digests
- exact candidate, evaluation, and review counts
- eligible candidate count and eligible-set digest
- selection scope
- selection-policy digest
- authorization-request digest
- receipt digest

## Fail-closed conditions

The request is blocked when:

- the source review receipt is not ready
- a required source boundary is absent or pre-promoted
- source counts are invalid or not exact
- the review-set digest is invalid
- review candidate ids or review digests are duplicated
- selection eligibility count disagrees with the review outcomes
- the eligible candidate set is empty
- source record digests or counts disagree with the receipt
- the selection scope is invalid
- the selection-policy digest is missing

## Required boundary

- source candidate-review receipt preserved = true
- candidate, evaluation, and review-set digests preserved = true
- review count exact preserved = true
- candidate review completed preserved = true
- selection eligibility preserved = true
- selection-eligible set nonempty = true
- prior memory, truth-authority, blocker-release, closeout, replan, generation, materialization, evaluation, and review chain preserved = true
- candidate-selection authorization request only = true
- candidate-selection authorization requested = true
- selection scope bound = true
- selection-policy digest bound = true

## Closed boundary

- selection authority granted = false
- candidate selection requested = false
- candidate selected = false
- admission requested = false

## Formal guarantees

The Lean bridge requires positive and bounded eligible count, exact candidate-evaluation-review counts, bound eligible-set digest, bound scope and policy digest, and non-promotion of selection authority, selection request, candidate selection, or admission.

The requester remains non-authoritative.
