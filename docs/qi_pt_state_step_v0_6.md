# Qi PT State Step v0.6

This addendum makes PT signals shape the local state step itself.

## Position

```text
queue.ready.jsonl
  -> PT gains
  -> state.json
  -> pt_step_log.jsonl
  -> pt_feedback.jsonl
```

## PT-derived gains

```text
qi_gain
qi_drag
recovery_gain
memory_gain
```

## State fields changed

```text
tick
qi_energy
qi_stability
qi_recovery
```

## Validation

```bash
python scripts/check_qi_pt_state_step_v0_6.py
```
