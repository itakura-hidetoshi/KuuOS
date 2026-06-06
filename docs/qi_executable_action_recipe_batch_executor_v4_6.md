# Qi Executable Action Recipe Batch Executor v4.6

Bounded batch executor for high-level Qi executable recipes.

This layer increases execution coverage by running more than one v4.5 recipe executor call in a declared finite batch.

## Input

- `qi_executable_action_recipe_batch_packet.json`

## Outputs

- `qi_executable_action_recipe_packet.json`
- `qi_executable_action_recipe_batch_executor_receipt.json`
- `qi_executable_action_recipe_batch_executor_audit.jsonl`

## Behavior

The batch executor writes one temporary `qi_executable_action_recipe_packet.json` per recipe and delegates execution to v4.5.

It stops when:

- the batch is complete
- a delegated recipe executor is blocked
- the batch exceeds the configured cap
- a recipe is not allowlisted
- the batch packet or license is not ready

## Boundary

This does not create arbitrary execution. It only runs bounded v4.5 recipe executor calls in a finite declared batch.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_action_recipe_batch_executor_v4_6.py
```
