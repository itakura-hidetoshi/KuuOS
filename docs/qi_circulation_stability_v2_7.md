# Qi Circulation Stability v2.7

Qi process-tensor stability layer for autonomous change workflows.

## Principle

Qi is primarily a circulation process. When there is no concrete stop reason, a circulating state is treated as more stable than a stagnant state.

## Inputs

- qi_circulation_packet.json

## Outputs

- qi_circulation_receipt.json
- qi_circulation_audit.jsonl

## Scores

- circulation_index
- stagnation_index

## Recommended actions

- continue_cycle
- rebalance_and_continue
- reopen_flow
- concrete_stop

## Concrete stop reasons

The layer stops only for concrete reasons such as scope mismatch, head SHA mismatch, or critical blocker presence.

## Validation

```bash
python scripts/check_qi_circulation_stability_v2_7.py
```
