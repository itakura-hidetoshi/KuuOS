# PlanOS v0.83 subsequent-cycle closeout request

PlanOS v0.83 consumes the ready v0.82 execution-completion receipt and records a bounded closeout request.

The request preserves the selected candidate identity, candidate-set digest, evaluation-set digest, review-set digest, admission evidence, cycle-start evidence, execution evidence, and completion evidence.

It additionally binds a closeout scope and closeout-constraints digest to the source completion receipt and concrete completion-record digest.

The transition boundary is:

```text
subsequent_cycle_execution_completed = true
subsequent_cycle_closeout_requested = true
subsequent_cycle_closed = false
```

The request therefore does not close the cycle.

The checker fails closed on an invalid source version or status, missing source receipt or record digests, absent execution completion, pre-requested closeout, selected-candidate mismatch, evidence mismatch, missing closeout scope, and missing closeout constraints.
