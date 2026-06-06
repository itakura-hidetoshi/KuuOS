# Qi Process Tensor Cycle Supervisor v3.8

Bounded multi-cycle supervisor for the Qi process tensor circulation loop.

This layer runs the v3.7 cycle runner repeatedly with a hard upper bound, records each cycle, and stops on convergence, block, hold, or the configured cycle cap.

## Inputs

- `qi_circulation_trajectory_packet.json`
- `qi_process_tensor_packet.json`

## Outputs

- updated `qi_circulation_trajectory_packet.json`
- `qi_process_tensor_cycle_supervisor_state.json`
- `qi_process_tensor_cycle_supervisor_receipt.json`
- `qi_process_tensor_cycle_supervisor_audit.jsonl`

## Stop reasons

- `converged`
- `blocked`
- `hold_overlay`
- `cycle_cap_reached`
- `no_progress`

## Boundary

This is a bounded supervisor. It does not create clinical authority, intervention authority, theorem authority, institutional authority, final commitment authority, or autonomous execution authority.

## Validation

```bash
python scripts/check_qi_process_tensor_cycle_supervisor_v3_8.py
```
