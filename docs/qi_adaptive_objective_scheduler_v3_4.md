# Qi Adaptive Objective Scheduler v3.4

Governance-bounded adaptive packet layer for Qi circulation workflows.

This component does not perform direct runtime control and does not bypass the circulation scheduler. It reads trajectory adaptor hints and converts them into scheduler-mediated packet parameters.

## Inputs

- qi_adaptive_scheduler_packet.json

## Outputs

- qi_circulation_scheduler_packet.json
- qi_circulation_closed_loop_packet.json
- qi_adaptive_scheduler_receipt.json
- qi_adaptive_scheduler_audit.jsonl

## Hint fields

- objective_hint
- max_cycles_delta
- convergence_threshold_delta

## Governance boundary

- hint-only: true
- scheduler-mediated: true
- packet-only: true
- direct_runtime_control: false
- direct_scheduler_bypass: false
- direct_execution_authority: false
- memoryos_write_authority: false
- world_update_authority: false
- probe_execution_authority: false

## Flow

```text
trajectory adaptor output
  -> adaptive packet hint layer
  -> circulation scheduler mediated packet
  -> closed-loop packet candidate
```

## Validation

```bash
python scripts/check_qi_adaptive_objective_scheduler_v3_4.py
```
