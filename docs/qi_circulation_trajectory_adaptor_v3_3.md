# Qi Circulation Trajectory Adaptor v3.3

Adaptor for Qi circulation scheduler packets.

## Inputs

- qi_circulation_trajectory_packet.json

## Outputs

- next_qi_circulation_scheduler_packet.json
- qi_circulation_trajectory_receipt.json
- qi_circulation_trajectory_audit.jsonl

## Adaptation classes

- stable_lighten
- blocked_recovery
- needs_more_reopen
- long_cycle_rebalance
- continue_adapt
- no_trajectory

## Flow

```text
trajectory result
  -> adaptor
  -> next scheduler packet
  -> next scheduled closed-loop run
```

## Validation

```bash
python scripts/check_qi_circulation_trajectory_adaptor_v3_3.py
```
