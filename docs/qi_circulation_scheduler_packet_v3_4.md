# Qi Circulation Scheduler Packet v3.4

Handoff layer for the next Qi circulation scheduler packet.

It reads the trajectory-adapted packet produced by the v3.3 adaptor and materializes the next scheduled closed-loop input packet used by the v3.2 runner.

## Inputs

- `next_qi_circulation_scheduler_packet.json`

## Outputs

- `qi_scheduled_closed_loop_packet.json`
- `qi_circulation_scheduler_packet_receipt.json`
- `qi_circulation_scheduler_packet_audit.jsonl`

## Handoff classes

- `stable_lighten_handoff`
- `reopen_handoff`
- `rebalance_handoff`
- `continue_handoff`

## Flow

```text
next_qi_circulation_scheduler_packet
  -> scheduler packet handoff
  -> qi_scheduled_closed_loop_packet
  -> scheduled closed-loop runner
```

## Boundary

This layer is a bounded packet handoff. It does not grant intervention authority, medical authority, institutional authority, theorem authority, or autonomous execution authority.

## Validation

```bash
python scripts/check_qi_circulation_scheduler_packet_v3_4.py
```
