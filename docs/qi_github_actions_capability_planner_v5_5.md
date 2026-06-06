# Qi GitHub Actions Capability Planner v5.5

GitHub Actions-aware planner for the Qi executable capability stack.

This layer reads a bounded GitHub Actions status packet and emits a v5.3 capability recipe batch packet for the next safe executable path.

## Inputs

- `qi_github_actions_status_packet.json`

## Outputs

- `qi_executable_capability_recipe_batch_packet.json`
- `qi_github_actions_capability_planner_receipt.json`
- `qi_github_actions_capability_planner_audit.jsonl`

## Observed GitHub Actions surface

The current repository uses pull-request checks including:

- `Qi Process Tensor Review Checks`
- `KuuOS Runtime Full Check`
- `All Governance Validation`
- `Core Governance Validation`
- `Emptiness Two Truths Runtime Audit Validation`
- `Emptiness Superposition Non-Collapse Validation`

The Qi process tensor review workflow and KuuOS runtime full check workflow both expose `workflow_dispatch`, so they are explicit GitHub Actions execution surfaces. This planner does not dispatch workflows directly; it consumes their observed status and plans the next bounded capability recipe batch.

## Planning classes

- `github_actions_all_green_batch`
- `github_actions_pending_observe_batch`
- `github_actions_qi_repair_batch`
- `github_actions_runtime_repair_batch`
- `github_actions_governance_repair_batch`
- `github_actions_mixed_repair_batch`
- `github_actions_missing_required_blocked`

## Boundary

This planner does not call GitHub APIs, rerun workflows, merge PRs, or execute shell commands. It only converts observed GitHub Actions status into a bounded v5.3 capability recipe batch packet.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, repository write authority, workflow dispatch authority, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_github_actions_capability_planner_v5_5.py
```
