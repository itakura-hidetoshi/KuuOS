# PlanOS v0.75 subsequent-cycle admission grant

PlanOS v0.75 consumes the completed v0.74 subsequent-cycle admission request and records a bounded admission grant.

The grant preserves the selected candidate identity, candidate-set digest, evaluation-set digest, review-set digest, admission scope, and admission-constraints digest.

It binds both the outer request receipt digest and the concrete admission-request digest.

The boundary is:

```text
subsequent_cycle_admission_requested = true
subsequent_cycle_admission_granted = true
subsequent_cycle_started = false
```

The grant does not start the subsequent cycle.
