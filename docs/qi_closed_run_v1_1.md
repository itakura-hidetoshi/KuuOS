# Qi Closed Run v1.1

This addendum combines the v0.9 loop and v1.0 adaptation into one local run.

## Stages

```text
loop
adapt
```

## Inputs

```text
queue.ready.jsonl
work_graph.json
pt_packet
runtime_context
closed_run_license_packet
```

## Outputs

```text
loop.jsonl
loop_feedback.jsonl
run_summary.json
pt_next.json
next_loop_context.json
adapt_log.jsonl
closed_run_chain.jsonl
closed_run_final.json
```

## Behavior

A single call runs the loop stage, then runs the adaptation stage from the loop outputs.
The run writes a chain file and final packet for the whole closed run.

## Validation

```bash
python scripts/check_qi_closed_run_v1_1.py
```
