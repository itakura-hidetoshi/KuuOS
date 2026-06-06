# Qi Executable Capability Recipe Executor v5.2

End-to-end executor for high-level Qi executable capability recipes.

This layer reads a capability recipe packet, compiles it with v5.1, then runs the resulting capability sequence with v5.0.

## Input

- `qi_executable_capability_recipe_packet.json`

## Outputs

- `qi_executable_capability_sequence_packet.json`
- `qi_executable_capability_recipe_executor_receipt.json`
- `qi_executable_capability_recipe_executor_audit.jsonl`

## Flow

```text
capability recipe packet
  -> v5.1 capability recipe compiler
  -> v5.0 capability sequence runner
```

## Boundary

This executor does not create arbitrary execution. It only compiles allowlisted capability recipes and runs the bounded v5.0 capability sequence runner.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_capability_recipe_executor_v5_2.py
```
