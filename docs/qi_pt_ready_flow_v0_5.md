# Qi PT Ready Flow v0.5

This addendum applies PT-ready rows and records feedback.

## Position

```text
queue.ready.jsonl
  -> applied.jsonl
  -> state.json
  -> pt_feedback.jsonl
```

## Files

```text
queue.ready.jsonl
applied.jsonl
state.json
pt_feedback.jsonl
```

## Status

```text
QI_PT_READY_FLOW_APPLIED
QI_PT_READY_FLOW_REPLAYED
QI_PT_READY_FLOW_IDLE
QI_PT_READY_FLOW_BLOCKED
```

## Validation

```bash
python scripts/check_qi_pt_ready_flow_v0_5.py
```
