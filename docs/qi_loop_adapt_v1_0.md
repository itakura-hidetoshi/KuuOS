# Qi Loop Adapt v1.0

This addendum closes the loop after v0.9.

## Inputs

```text
state.json
run_summary.json
loop_feedback.jsonl
pt_packet
```

## Outputs

```text
pt_next.json
next_loop_context.json
adapt_log.jsonl
```

## Behavior

The adapter reads loop feedback and run summary, then updates next PT values and the next loop context.

Updated values include:

```text
execution_pressure
coherence_score
memory_depth
recovery_witness_present
cycles
base_cycle_budget
```

## Validation

```bash
python scripts/check_qi_loop_adapt_v1_0.py
```
