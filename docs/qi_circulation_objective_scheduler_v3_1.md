# Qi Circulation Objective Scheduler v3.1

Scheduler for Qi circulation closed-loop workflows.

## Inputs

- qi_circulation_scheduler_packet.json

## Outputs

- qi_circulation_closed_loop_packet.json
- qi_circulation_scheduler_receipt.json
- qi_circulation_scheduler_audit.jsonl

## Objective classes

- maintain
- rebalance
- reopen
- hold

## Schedule policy

```text
maintain  -> max_cycles=2, convergence_threshold=0.015
rebalance -> max_cycles=4, convergence_threshold=0.025
reopen    -> max_cycles=6, convergence_threshold=0.04
```

## Flow

```text
Qi packet
  -> scheduler
  -> closed-loop packet
  -> closed-loop runner v3.0
```

## Validation

```bash
python scripts/check_qi_circulation_objective_scheduler_v3_1.py
```
