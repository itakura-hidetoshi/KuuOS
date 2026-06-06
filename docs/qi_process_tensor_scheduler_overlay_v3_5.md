# Qi Process Tensor Scheduler Overlay v3.5

Process-tensor-aware overlay for the Qi circulation return loop.

This layer reads the `qi_scheduled_closed_loop_packet.json` materialized by v3.4 and a local `qi_process_tensor_packet.json`, evaluates process-level Qi memory support, and writes a bounded overlay back into the scheduled closed-loop packet before the next v3.2 run.

## Inputs

- `qi_scheduled_closed_loop_packet.json`
- `qi_process_tensor_packet.json`

## Outputs

- updated `qi_scheduled_closed_loop_packet.json`
- `qi_process_tensor_scheduler_overlay_receipt.json`
- `qi_process_tensor_scheduler_overlay_audit.jsonl`

## Overlay classes

- `process_tensor_stabilize_overlay`
- `process_tensor_rebalance_overlay`
- `process_tensor_recovery_overlay`
- `process_tensor_hold_overlay`
- `process_tensor_continue_overlay`

## Flow

```text
Qi scheduled closed-loop runner v3.2
  -> Qi circulation trajectory adaptor v3.3
  -> Qi circulation scheduler packet v3.4
  -> Qi process tensor scheduler overlay v3.5
  -> next scheduled closed-loop run
```

## Boundary

This layer preserves the existing non-authority boundary. A process tensor overlay is memory-sensitive scheduling context only. It is not intervention authority, clinical authority, theorem authority, institutional authority, final commitment authority, or autonomous execution authority.

## Validation

```bash
python scripts/check_qi_process_tensor_scheduler_overlay_v3_5.py
```
