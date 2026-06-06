# Qi Process Tensor Return Loop Orchestrator v3.6

One-pass orchestrator for the Qi circulation return loop.

This layer runs the existing return path in order:

```text
Qi circulation trajectory adaptor v3.3
  -> Qi circulation scheduler packet v3.4
  -> Qi process tensor scheduler overlay v3.5
```

It turns a prior trajectory packet and a Qi process tensor packet into the next scheduled closed-loop packet.

## Inputs

- `qi_circulation_trajectory_packet.json`
- `qi_process_tensor_packet.json`

## Intermediate files

- `next_qi_circulation_scheduler_packet.json`
- `qi_scheduled_closed_loop_packet.json`

## Outputs

- `qi_scheduled_closed_loop_packet.json`
- `qi_process_tensor_return_loop_receipt.json`
- `qi_process_tensor_return_loop_audit.jsonl`

## Stage order

1. v3.3 adapts trajectory history into the next scheduler packet.
2. v3.4 materializes that packet into the scheduled closed-loop input.
3. v3.5 overlays process tensor memory, non-Markov, and recovery context.

## Boundary

This orchestrator is a bounded return-loop runner. It does not create intervention authority, clinical authority, theorem authority, institutional authority, final commitment authority, or autonomous execution authority.

## Validation

```bash
python scripts/check_qi_process_tensor_return_loop_orchestrator_v3_6.py
```
