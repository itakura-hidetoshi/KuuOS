# Qi Adaptive Objective Scheduler v3.4

Adaptive scheduler for Qi circulation workflows.

## Inputs

- qi_adaptive_scheduler_packet.json

## Outputs

- qi_circulation_scheduler_packet.json
- qi_circulation_closed_loop_packet.json
- qi_adaptive_scheduler_receipt.json
- qi_adaptive_scheduler_audit.jsonl

## Adapted fields

- objective_hint
- max_cycles_delta
- convergence_threshold_delta

## Flow

```text
trajectory adaptor output
  -> adaptive scheduler
  -> closed-loop packet
  -> next scheduled run
```

## Validation

```bash
python scripts/check_qi_adaptive_objective_scheduler_v3_4.py
```
