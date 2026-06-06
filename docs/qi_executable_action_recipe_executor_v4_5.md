# Qi Executable Action Recipe Executor v4.5

End-to-end recipe executor for bounded Qi executable actions.

This layer reads a high-level recipe packet, compiles it with v4.4, then runs the resulting sequence with v4.3.

## Input

- `qi_executable_action_recipe_packet.json`

## Outputs

- `qi_executable_action_sequence_packet.json`
- `qi_executable_action_recipe_executor_receipt.json`
- `qi_executable_action_recipe_executor_audit.jsonl`

## Flow

```text
recipe packet
  -> v4.4 recipe compiler
  -> v4.3 sequence runner
```

## Boundary

This executor does not create arbitrary execution. It only compiles allowlisted recipes and runs the bounded v4.3 sequence runner.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_action_recipe_executor_v4_5.py
```
