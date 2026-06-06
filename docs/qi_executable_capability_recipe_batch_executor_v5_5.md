# Qi Executable Capability Recipe Batch Executor v5.5

End-to-end executor for high-level Qi executable capability recipe batches.

This layer reads a capability recipe batch compiler packet, compiles it with v5.4, then runs the resulting capability recipe batch with v5.3.

## Input

- `qi_executable_capability_recipe_batch_compiler_packet.json`

## Outputs

- `qi_executable_capability_recipe_batch_packet.json`
- `qi_executable_capability_recipe_batch_executor_v5_5_receipt.json`
- `qi_executable_capability_recipe_batch_executor_v5_5_audit.jsonl`

## Flow

```text
capability recipe batch compiler packet
  -> v5.4 capability recipe batch compiler
  -> v5.3 capability recipe batch executor
```

## Boundary

This executor does not create arbitrary execution. It only compiles allowlisted capability recipe batches and runs the bounded v5.3 capability recipe batch executor.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_capability_recipe_batch_executor_v5_5.py
```
