# Qi Local Flow v0.3

This addendum advances the local execution path after v0.2.

## Position

```text
queue.jsonl
  -> applied.jsonl
  -> state.json
```

## Local files

```text
queue.jsonl: input rows
applied.jsonl: applied rows
state.json: accumulated local state
```

## Status

```text
QI_LOCAL_FLOW_APPLIED
QI_LOCAL_FLOW_REPLAYED
QI_LOCAL_FLOW_IDLE
QI_LOCAL_FLOW_BLOCKED
```

## Behavior

Rows from `queue.jsonl` are converted into records in `applied.jsonl`.
The local `state.json` file is updated with `applied_total` and recent item keys.
Repeated rows are recognized by idempotency and are not duplicated.

## Validation

```bash
python scripts/check_qi_local_flow_v0_3.py
```

Expected:

```text
PASS: Qi local flow v0.3 check
```
