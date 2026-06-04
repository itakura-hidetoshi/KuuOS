# Qi PR Merge Gate v2.1

A bounded merge gate for autonomous pull-request workflows.

## Inputs

- pr_merge_gate_packet.json

## Required conditions

- explicit_automerge_license
- allowed_repository
- allowed_base_branch
- pull_request_created
- pull_request_not_draft
- mergeable
- expected_head_sha == actual_head_sha
- all required checks successful
- no unresolved blockers
- receipt_written
- audit_written

## Outputs

- pr_merge_receipt.json
- pr_merge_gate_audit.jsonl

## Status

- QI_PR_MERGE_GATE_PASSED
- QI_PR_MERGE_GATE_BLOCKED

## Position

Objective
 -> actuator change
 -> pull request
 -> CI checks
 -> PR merge gate
 -> merge receipt
 -> audit
