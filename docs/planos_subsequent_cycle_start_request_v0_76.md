# PlanOS v0.76 subsequent-cycle start request

PlanOS v0.76 consumes the completed v0.75 admission grant and records only a bounded request to start the admitted subsequent cycle.

It preserves the selected candidate identity, candidate-set digest, evaluation-set digest, review-set digest, admission scope, and admission-constraints digest.

The request binds the source admission-grant receipt digest, concrete admission-grant digest, start scope, start-constraints digest, and deterministic start-request digest.

The fail-closed checker rejects an invalid admission grant, missing grant record, selected-candidate mismatch, evidence mismatch, missing start scope or constraints, and a pre-started cycle.

The boundary is:

```text
subsequent_cycle_admission_requested = true
subsequent_cycle_admission_granted = true
subsequent_cycle_start_requested = true
subsequent_cycle_started = false
```

The request does not start the subsequent cycle. A later receipt layer must perform and record that transition.
