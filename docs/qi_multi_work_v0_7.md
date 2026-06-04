# Qi Multi Work v0.7

This addendum increases the local work kinds available to the Qi runtime.

## Work kinds

```text
metric
note
record
state_patch
counter
snapshot
pull_deferred
```

## Local files

```text
metrics.jsonl
notes.md
records/*.json
snapshots/*.json
state.json
queue.ready.jsonl
multi_work_log.jsonl
```

## PT-shaped values

```text
qi_gain
qi_drag
recovery_gain
memory_gain
```

## Validation

```bash
python scripts/check_qi_multi_work_v0_7.py
```
