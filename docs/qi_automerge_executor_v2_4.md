# Qi Automerge Executor v2.4

CI-aware automerge executor for Qi autonomous GitHub workflows.

## Inputs

- automerge_packet.json

## Outputs

- automerge_receipt.json
- automerge_audit.jsonl
- pr_merge_gate_packet.json
- github_tool_bridge_plan.json

## Required gates

- explicit_automerge_license=true
- expected_head_sha == actual_head_sha
- pull_request_not_draft=true
- mergeable=true
- all required checks successful
- no unresolved blockers
- receipt_written=true
- audit_written=true
- merge_allowed=true

## Execution stages

```text
automerge_packet
  -> PR merge gate v2.1
  -> GitHub tool bridge v2.3
  -> automerge receipt/audit
```

## Modes

- mock: CI/local verification; merge action is simulated
- real: requires execute_external_actions=true and token-backed GitHub tool bridge

## Validation

```bash
python scripts/check_qi_automerge_executor_v2_4.py
```
