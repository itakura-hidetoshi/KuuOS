# Qi GitHub Actions Direct Executor v5.6

Direct GitHub Actions / PR execution layer for the Qi executable stack.

This layer intentionally removes the v5.5 limitation that the GitHub Actions layer is observation-only.

## Input

- `qi_github_actions_direct_execution_packet.json`

## Outputs

- `qi_github_actions_direct_executor_receipt.json`
- `qi_github_actions_direct_executor_audit.jsonl`

## Direct actions

- `workflow_dispatch`
- `rerun_failed_workflow_run_jobs`
- `rerun_workflow_job`
- `merge_pull_request`

## Transport modes

- `dry_run`: validate and emit the target GitHub REST request without sending it
- `github_rest`: send the request to GitHub REST using `GITHUB_TOKEN` or `GH_TOKEN`

## Required guards

Direct execution requires all of the following:

- runtime context enabled
- execution packet `direct_execution_allowed: true`
- license status ready
- action-specific license flag, such as `allow_workflow_dispatch_action: true`
- `transport_mode` set to `github_rest` or `dry_run`
- token available for `github_rest`

## REST targets

- `POST /repos/{owner}/{repo}/actions/workflows/{workflow_id_or_file}/dispatches`
- `POST /repos/{owner}/{repo}/actions/runs/{run_id}/rerun-failed-jobs`
- `POST /repos/{owner}/{repo}/actions/jobs/{job_id}/rerun`
- `PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge`

## Boundary

This executor can directly call GitHub REST when explicitly configured. It still does not grant clinical authority, theorem authority, institutional authority, shell access, arbitrary network access beyond GitHub REST, arbitrary repository write authority, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_github_actions_direct_executor_v5_6.py
```
