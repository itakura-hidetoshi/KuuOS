# PlanOS v0.78 subsequent-cycle execution request

PlanOS v0.78 consumes the ready v0.77 subsequent-cycle start receipt and records a bounded execution request.

The request preserves the selected candidate identity, candidate-set digest, evaluation-set digest, review-set digest, admission evidence, and start evidence.

It additionally binds an execution scope and an execution-constraints digest to the source start receipt and concrete start-record digest.

The transition boundary is:

```text
subsequent_cycle_started = true
subsequent_cycle_execution_requested = true
subsequent_cycle_execution_authority_granted = false
subsequent_cycle_execution_started = false
```

The request therefore does not grant execution authority and does not start execution.

The checker fails closed on an invalid source version or status, missing source receipt or record digests, absent cycle start, pre-requested execution, selected-candidate mismatch, evidence mismatch, missing execution scope, and missing execution constraints.
