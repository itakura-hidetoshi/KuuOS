# Qi GitHub Actions Direct Operator v5.6

Direct GitHub Actions / PR operator for the Qi executable stack.

This layer intentionally removes the earlier boundary that GitHub Actions must not be directly rerun, dispatched, or merged. Instead, direct operations are allowed only through explicit packets, allowlisted operations, explicit execution mode, target checks, and append-only receipts.

## Input

- `qi_github_actions_direct_operation_packet.json`

## Outputs

- `qi_github_actions_direct_operator_receipt.json`
- `qi_github_actions_direct_operator_audit.jsonl`

## Supported operations

- `rerun_failed_workflow_run_jobs`
- `rerun_workflow_job`
- `workflow_dispatch`
- `merge_pull_request`

## Execution modes

- `dry_run`: validate and emit receipt without calling GitHub
- `live`: perform the operation through GitHub REST API using `GITHUB_TOKEN`

## Required live safeguards

Live execution requires:

- `direct_operation_allowed: true`
- operation allowlisted by the license
- repository matching `allowed_repo_full_name`
- `execution_mode: live`
- `GITHUB_TOKEN` available
- merge requests must include `expected_head_sha`

## Boundary

This operator may directly rerun failed workflow jobs, rerun a workflow job, dispatch a workflow, or merge a pull request when explicitly authorized.

It still does not grant clinical authority, intervention authority, theorem authority, institutional authority, arbitrary shell access, arbitrary network access, arbitrary repository write authority, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_github_actions_direct_operator_v5_6.py
```
