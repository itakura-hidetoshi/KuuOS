# Qi GitHub Tool Bridge v2.3

Actual GitHub REST bridge for Qi autonomous change workflows.

## Inputs

- github_tool_bridge_plan.json

## Outputs

- github_tool_bridge_receipt.json
- github_tool_bridge_audit.jsonl

## Modes

- mock: no network mutation; used for CI and local validation
- real: calls GitHub REST API when explicitly enabled

## Supported action kinds

- create_branch
- create_file
- update_file
- file_patch
- create_pr
- merge_pr

## Real mode gates

Real mode is blocked unless all are true:

- runtime context has execute_external_actions=true
- plan has execute_external_actions=true
- token_env resolves to a token, default GITHUB_TOKEN
- license_status is QI_GITHUB_TOOL_BRIDGE_LICENSE_READY
- external_action_allowed=true

## Safety boundary

The bridge does not infer repository or branch authority from the action itself. The plan-level repository and base branch are treated as the bounded authority surface. Every action is checked against that scope before execution.

## Validation

```bash
python scripts/check_qi_github_tool_bridge_v2_3.py
```
