# Qi Execution Loop v0.9

This addendum combines queue items and work graph nodes into a multi-cycle local execution loop.

## Inputs

```text
queue.ready.jsonl
work_graph.json
state.json
process_tensor_packet
loop_license_packet
```

## Outputs

```text
loop.jsonl
loop_feedback.jsonl
run_summary.json
state.json
loop_reports/*.md
loop_checkpoints/*.json
```

## Behavior

Each cycle uses PT-shaped gains to set a cycle budget.
The loop consumes ready queue rows first, then graph nodes whose dependencies are satisfied.
Each cycle writes feedback and the run writes a final summary.

## Validation

```bash
python scripts/check_qi_execution_loop_v0_9.py
```
