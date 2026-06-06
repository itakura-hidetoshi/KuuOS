# Qi Trend Adaptive Supervisor Run v4.1

Adaptive supervisor execution layer for the Qi process tensor circulation loop.

This layer reads the bounded supervisor packet created by v4.0 and runs the v3.8 supervisor with the requested context patch.

## Inputs

- `next_qi_process_tensor_cycle_supervisor_packet.json`
- `qi_circulation_trajectory_packet.json`
- `qi_process_tensor_packet.json`

## Outputs

- updated `qi_circulation_trajectory_packet.json`
- `qi_process_tensor_cycle_supervisor_state.json`
- `qi_trend_adaptive_supervisor_run_receipt.json`
- `qi_trend_adaptive_supervisor_run_audit.jsonl`

## Flow

```text
v3.9 trend summary
  -> v4.0 next supervisor packet
  -> v4.1 adaptive supervisor run
  -> v3.8 cycle supervisor
```

## Boundary

This layer only runs the already-bounded v3.8 supervisor using a v4.0 packet. It does not grant clinical authority, intervention authority, theorem authority, institutional authority, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_trend_adaptive_supervisor_run_v4_1.py
```
