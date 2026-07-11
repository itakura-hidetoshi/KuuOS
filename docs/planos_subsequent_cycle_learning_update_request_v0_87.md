# PlanOS v0.87 subsequent-cycle learning update request

PlanOS v0.87 records a bounded learning-update request sourced from the completed post-closeout review receipt produced by v0.86.

The package preserves selected-candidate identity, candidate, evaluation, and review set digests, closeout evidence, and post-closeout review-completion evidence.

The request binds the source review-receipt digest, concrete post-closeout review-record digest, learning-update scope, learning-update constraints digest, and deterministic learning-update request digest.

The fail-closed checker blocks invalid or incomplete review receipts, missing source digests, absent review completion, pre-requested learning update, selected-candidate or evidence mismatch, missing update scope, and missing update constraints.

The transition is bounded to:

```text
subsequent_cycle_post_closeout_review_completed = true
subsequent_cycle_learning_update_requested = true
subsequent_cycle_learning_update_applied = false
```

Application of the learning update remains a separate later transition.