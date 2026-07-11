# PlanOS v0.90 subsequent-cycle next iteration start receipt

PlanOS v0.90 records the bounded start of the next iteration requested by v0.89.

The package preserves selected-candidate identity, candidate, evaluation, and review set digests, closeout evidence, post-closeout review evidence, learning-update evidence, next-iteration scope, and next-iteration constraints.

The receipt binds the source next-iteration request receipt digest, concrete next-iteration request digest, start-rationale digest, and deterministic next-iteration start-receipt digest.

The fail-closed checker blocks invalid or incomplete next-iteration requests, missing source digests, absent request, pre-started iteration, selected-candidate or evidence mismatch, missing scope or constraints, and missing start rationale.

The transition is bounded to:

```text
subsequent_cycle_next_iteration_requested = true
subsequent_cycle_next_iteration_started = true
subsequent_cycle_next_iteration_planning_requested = false
```

Planning for the started iteration remains a separate later transition.
