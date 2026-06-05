# Qi Circulation Closed-Loop Runner v3.0

Closed-loop runner for Qi autonomous circulation workflows.

## Principle

Qi becomes stable by circulating. The closed-loop runner repeatedly composes routing and feedback so the process tensor can keep moving toward healthier circulation.

## Inputs

- qi_circulation_closed_loop_packet.json

## Outputs

- qi_circulation_closed_loop_receipt.json
- qi_circulation_closed_loop_audit.jsonl
- cycle_N/circulation_change_route_packet.json
- cycle_N/qi_circulation_feedback_packet.json

## Composed layers

```text
Qi circulation change router v2.8
  -> Qi circulation feedback controller v2.9
  -> next Qi process tensor packet
  -> next cycle
```

## Stop / convergence semantics

- continue while cycles remain and concrete blockers are absent
- converge when the next Qi packet delta is below threshold
- block only when router or feedback produces a concrete blocker

## Validation

```bash
python scripts/check_qi_circulation_closed_loop_runner_v3_0.py
```
