# Qi Autonomous Change Loop v2.5

Top-level autonomous change loop for KuuOS GitHub workflows.

## Inputs

- autonomous_change_loop_packet.json

## Outputs

- github_tool_bridge_plan.json
- automerge_packet.json
- autonomous_change_loop_receipt.json
- autonomous_change_loop_audit.jsonl

## Stages

```text
autonomous_change_loop_packet
  -> GitHub tool bridge v2.3
  -> automerge executor v2.4
  -> autonomous change receipt/audit
```

## Modes

- mock: full loop simulation for CI/local validation
- real: requires execute_external_actions=true and downstream real-mode gates

## Required packet fields

- repository_full_name
- branch
- base_branch
- expected_head_sha
- actual_head_sha
- explicit_change_loop_license
- explicit_automerge_license
- merge_allowed
- required_checks

## Validation

```bash
python scripts/check_qi_autonomous_change_loop_v2_5.py
```
