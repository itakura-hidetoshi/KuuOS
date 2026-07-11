# PlanOS v0.89 subsequent-cycle next iteration request

PlanOS v0.89 records a bounded request to begin the next iteration after the v0.88 learning update has been applied.

The package preserves the selected-candidate identity, candidate, evaluation, and review set digests, closeout evidence, post-closeout review evidence, and learning-update evidence.

The request binds the source learning-update receipt digest, concrete learning-update record digest, next-iteration scope, next-iteration constraints digest, and deterministic next-iteration request digest.

The fail-closed checker blocks invalid or incomplete learning-update receipts, missing source digests, absent learning-update application, pre-requested next iteration, selected-candidate or evidence mismatch, missing next-iteration scope, and missing next-iteration constraints.

The transition is bounded to:

```text
subsequent_cycle_learning_update_applied = true
subsequent_cycle_next_iteration_requested = true
subsequent_cycle_next_iteration_started = false
```

Actual next-iteration start remains a separate later transition.
