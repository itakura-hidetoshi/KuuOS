# Qi GitHub Actuator v2.2

A bounded GitHub actuator layer for KuuOS autonomous-change workflows.

## Inputs

- github_actuator_plan.json

## Planned action kinds

- create_branch
- file_patch
- create_pr
- merge_pr

## Outputs

- github_actuator_receipt.json
- github_actuator_audit.jsonl
- pr_merge_gate_packet.json
- pr_merge_receipt.json
- pr_merge_gate_audit.jsonl

## Merge semantics

The merge step is not direct by default. The actuator writes a PR merge gate packet and evaluates it through Qi PR Merge Gate v2.1.

A merge is allowed only when the gate passes and the plan explicitly sets merge_allowed.

## Status

- QI_GITHUB_ACTUATOR_READY
- QI_GITHUB_ACTUATOR_MERGE_BLOCKED
- QI_GITHUB_ACTUATOR_BLOCKED

## Position

Objective
 -> GitHub action plan
 -> branch/file/PR action records
 -> PR merge gate
 -> receipt
 -> audit

## Validation

```bash
python scripts/check_qi_github_actuator_v2_2.py
```
