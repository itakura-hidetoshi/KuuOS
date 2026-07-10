# PlanOS Subsequent-Cycle Candidate Evaluation Receipt v0.67

PlanOS v0.67 evaluates every candidate materialized by v0.66 and records a bounded evaluation receipt.

This layer does not request review, select a candidate, or request subsequent-cycle admission.

## Input

The source input is `kuuos_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66`.

The source must be ready.

The source candidate set must be nonempty, digest-valid, count-consistent, and unique by candidate id and candidate digest.

Evaluation specifications must cover every materialized candidate exactly once and must not contain unknown candidates.

Each evaluation specification contains:

- candidate id
- continuity score
- constraint score
- reversibility score
- uncertainty penalty
- rationale digest

Each score component is an integer from zero through one hundred.

The total score is calculated as:

`continuity + constraint + reversibility - uncertainty penalty`

The evaluation order follows the materialized candidate order.

The evaluation order is not a selection or ranking authority.

## Output

The runtime emits `PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_EVALUATION_RECEIPT_READY` when all source and evaluation checks pass.

Each candidate evaluation contains:

- candidate id
- candidate digest
- four score components
- total score
- rationale digest
- evaluation ordinal
- evaluation digest

The output also contains:

- candidate-set digest
- candidate count
- evaluation-set digest
- evaluation count
- candidate-evaluation receipt record
- receipt digest

## Fail-closed conditions

The runtime blocks when:

- the source candidate-set digest is invalid
- source candidate count and candidate-set length differ
- source candidate ids or digests are not unique
- an evaluation is missing
- an evaluation refers to an unknown candidate
- a candidate is evaluated more than once
- an evaluation component is not an integer
- an evaluation component is outside zero through one hundred
- a rationale digest is missing
- the source has already promoted candidate selection or admission

## Required boundary

- source candidate-set materialization receipt preserved = true
- selected-candidate provenance preserved = true
- candidate-set digest preserved = true
- candidate-set nonempty and unique properties preserved = true
- prior memory, truth-authority, blocker-release, closeout, replan, generation, and materialization chain preserved = true
- subsequent-cycle candidate-evaluation receipt only = true
- all materialized candidates evaluated = true
- evaluation count exact = true
- evaluation score bounds valid = true
- candidate evaluations recorded = true
- evaluation order is not selection = true

## Closed boundary

- subsequent-cycle candidate review requested = false
- subsequent-cycle candidate selected = false
- subsequent-cycle admission requested = false

## Formal guarantees

The Lean bridge requires:

- candidate count is positive
- evaluation input count equals candidate count
- evaluation output count equals candidate count
- evaluation-set digest is bound
- every materialized candidate is evaluated
- all score bounds are valid
- review, selection, and admission remain closed

## Authority boundary

This layer records evaluation evidence only.

The evaluation recorder itself remains non-authoritative.
