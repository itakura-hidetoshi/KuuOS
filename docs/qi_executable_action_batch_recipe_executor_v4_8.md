# Qi Executable Action Batch Recipe Executor v4.8

End-to-end executor for high-level Qi executable batch recipes.

This layer reads a batch recipe compiler packet, compiles it with v4.7, then runs the resulting batch with v4.6.

## Input

- `qi_executable_action_recipe_batch_compiler_packet.json`

## Outputs

- `qi_executable_action_recipe_batch_packet.json`
- `qi_executable_action_batch_recipe_executor_receipt.json`
- `qi_executable_action_batch_recipe_executor_audit.jsonl`

## Flow

```text
batch recipe compiler packet
  -> v4.7 batch compiler
  -> v4.6 batch executor
```

## Boundary

This executor does not create arbitrary execution. It only compiles allowlisted batch recipes and runs the bounded v4.6 batch executor.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_action_batch_recipe_executor_v4_8.py
```
