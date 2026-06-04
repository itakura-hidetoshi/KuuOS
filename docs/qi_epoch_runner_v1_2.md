# Qi Epoch Runner v1.2

This addendum runs multiple closed-run epochs in one call.

## Inputs

```text
epoch_tasks.jsonl
pt_packet
runtime_context
epoch_license_packet
```

## Outputs

```text
epoch_injections.jsonl
epoch_chain.jsonl
epoch_final.json
pt_next.json
next_loop_context.json
queue.ready.jsonl
closed_run_chain.jsonl
closed_run_final.json
```

## Behavior

Each epoch injects due tasks from `epoch_tasks.jsonl` into `queue.ready.jsonl`, runs the v1.1 closed run, then carries `pt_next.json` and `next_loop_context.json` into the next epoch.

## Validation

```bash
python scripts/check_qi_epoch_runner_v1_2.py
```
