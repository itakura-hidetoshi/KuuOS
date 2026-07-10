# PlanOS v0.77 subsequent-cycle start receipt

PlanOS v0.77 consumes the ready v0.76 subsequent-cycle start request and records the bounded start of the selected subsequent-cycle candidate.

The package preserves the selected candidate identity, candidate-set digest, evaluation-set digest, review-set digest, admission scope, admission-constraints digest, start scope, and start-constraints digest.

The receipt binds the source start-request receipt digest, the concrete start-request digest, a start-rationale digest, and a deterministic subsequent-cycle start receipt digest.

The boundary is:

```text
subsequent_cycle_start_requested = true
subsequent_cycle_started = true
subsequent_cycle_execution_requested = false
```

The start receipt does not itself request candidate execution. Execution remains a separate downstream transition.

The checker fails closed on an invalid source version or status, missing source receipt or request digest, absent admission grant, absent start request, a pre-started source, evidence mismatch, missing scope or constraints, and missing start rationale.
