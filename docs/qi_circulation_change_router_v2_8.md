# Qi Circulation Change Router v2.8

Circulation-aware router for Qi autonomous change workflows.

## Principle

Qi process tensor evaluation should not remain a passive score. When circulation is available, it should route the change loop forward.

## Inputs

- circulation_change_route_packet.json

## Outputs

- qi_circulation_packet.json
- forward_change_packet.json
- circulation_change_router_receipt.json
- circulation_change_router_audit.jsonl

## Routing actions

The following circulation actions are routed into the forward change runner:

- continue_cycle
- rebalance_and_continue
- reopen_flow

Only concrete_stop blocks routing.

## Flow

```text
circulation_change_route_packet
  -> Qi circulation stability v2.7
  -> forward_change_packet
  -> Qi forward change runner v2.6
  -> router receipt/audit
```

## Validation

```bash
python scripts/check_qi_circulation_change_router_v2_8.py
```
