# Qi Executable Capability Recipe Compiler v5.1

Recipe compiler for the Qi executable capability sequence runner.

This layer translates named safe capability recipes into v5.0 capability sequence packets.

## Input

- `qi_executable_capability_recipe_packet.json`

## Output

- `qi_executable_capability_sequence_packet.json`
- `qi_executable_capability_recipe_compiler_receipt.json`
- `qi_executable_capability_recipe_compiler_audit.jsonl`

## Capability recipes

- `compile_recipe_and_batch`
- `compile_then_execute_recipe`
- `compile_batch_then_execute_batch`
- `route_observe_then_compile`
- `safe_compile_full_surface`

## Boundary

This compiler does not execute capabilities. It only emits a bounded v5.0 capability sequence packet from a named allowlisted capability recipe.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_capability_recipe_compiler_v5_1.py
```
