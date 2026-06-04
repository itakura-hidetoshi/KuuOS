# Qi Work Graph v0.8

This addendum turns single local work into dependency-ordered graph work.

## Graph file

```text
work_graph.json
```

## Node kinds

```text
metric_rollup
report
checkpoint
index
state_patch
append_note
ready_seed
```

## Local outputs

```text
work_graph_log.jsonl
rollups/*.json
reports/*.md
checkpoints/*.json
index.json
graph_notes.md
queue.ready.jsonl
state.json
```

## PT-shaped budget

The process tensor gain values determine how many ready graph nodes can run in one pass.

## Validation

```bash
python scripts/check_qi_work_graph_v0_8.py
```
