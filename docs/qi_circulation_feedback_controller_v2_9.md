# Qi Circulation Feedback Controller v2.9

Closed-loop feedback controller for Qi circulation in autonomous change workflows.

## Principle

The Qi process tensor should not only route a cycle forward. It should learn from the cycle result and produce the next Qi process tensor packet.

## Inputs

- qi_circulation_feedback_packet.json

## Outputs

- next_qi_process_tensor_packet.json
- qi_circulation_feedback_receipt.json
- qi_circulation_feedback_audit.jsonl

## Feedback actions

- maintain_circulation
- rebalance_circulation
- reopen_circulation
- hold_for_concrete_reason

## Controlled terms

- qi_flow
- coherence_score
- circulation_pressure
- friction
- recovery_witness_present

## Flow

```text
router/action receipt
  -> feedback controller
  -> next_qi_process_tensor_packet
  -> next circulation cycle
```

## Validation

```bash
python scripts/check_qi_circulation_feedback_controller_v2_9.py
```
