# Qi PT Flow v0.4

This addendum makes local flow use PT signals before local application.

## Position

```text
queue.jsonl
  -> PT policy
  -> queue.ready.jsonl / queue.deferred.jsonl
  -> v0.3 local flow
```

## Signals

```text
process_tensor_ok
execution_pressure
coherence_score
memory_depth
recovery_witness_present
recovery_witness_missing
non_markov_unresolved
preferred_actions
blocked_actions
```

## Files

```text
queue.jsonl
queue.ready.jsonl
queue.deferred.jsonl
pt_policy_state.json
pt_policy_log.jsonl
```

## Validation

```bash
python scripts/check_qi_process_tensor_flow_policy_v0_4.py
```
