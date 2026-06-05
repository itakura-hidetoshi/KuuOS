# Qi Forward Change Runner v2.6

Forward-biased wrapper for the Qi autonomous change loop.

## Inputs

- forward_change_packet.json

## Outputs

- autonomous_change_loop_packet.json
- forward_change_receipt.json
- forward_change_audit.jsonl

## Posture

The runner begins from forward intent. It normalizes missing forward fields and then calls the autonomous change loop.

It stops on concrete stop reasons from the downstream loop, such as failed checks, SHA mismatch, scope mismatch, or failed bridge result.

## Flow

```text
forward_change_packet
  -> normalize forward intent
  -> autonomous_change_loop_packet
  -> Qi autonomous change loop v2.5
  -> forward receipt/audit
```

## Validation

```bash
python scripts/check_qi_forward_change_runner_v2_6.py
```
