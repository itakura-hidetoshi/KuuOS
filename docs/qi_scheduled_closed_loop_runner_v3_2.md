# Qi Scheduled Closed-Loop Runner v3.2

Scheduled runner for Qi circulation workflows.

## Inputs

- qi_scheduled_closed_loop_packet.json

## Outputs

- qi_circulation_scheduler_packet.json
- qi_circulation_closed_loop_packet.json
- qi_scheduled_closed_loop_receipt.json
- qi_scheduled_closed_loop_audit.jsonl

## Stages

```text
scheduled packet
  -> scheduler v3.1
  -> closed-loop runner v3.0
  -> receipt and audit
```

## Validation

```bash
python scripts/check_qi_scheduled_closed_loop_runner_v3_2.py
```
