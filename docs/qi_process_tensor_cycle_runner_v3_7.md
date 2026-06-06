# Qi Process Tensor Cycle Runner v3.7

One-cycle runner for the Qi process tensor circulation loop.

This layer runs:

```text
Qi process tensor return loop orchestrator v3.6
  -> Qi scheduled closed-loop runner v3.2
  -> append scheduled result back into qi_circulation_trajectory_packet.json
```

## Inputs

- `qi_circulation_trajectory_packet.json`
- `qi_process_tensor_packet.json`

## Outputs

- `qi_scheduled_closed_loop_packet.json`
- updated `qi_circulation_trajectory_packet.json`
- `qi_process_tensor_cycle_runner_receipt.json`
- `qi_process_tensor_cycle_runner_audit.jsonl`

## Status values

- `QI_PROCESS_TENSOR_CYCLE_RUNNER_READY`
- `QI_PROCESS_TENSOR_CYCLE_RUNNER_BLOCKED`

## Boundary

This is a bounded cycle runner. It does not create clinical authority, intervention authority, theorem authority, institutional authority, final commitment authority, or autonomous execution authority.

## Validation

```bash
python scripts/check_qi_process_tensor_cycle_runner_v3_7.py
```
