# Qi Executable Action Recipe Batch Compiler v4.7

Batch compiler for high-level Qi executable recipe suites.

This layer translates named safe batch recipes into v4.6 batch packets.

## Input

- `qi_executable_action_recipe_batch_compiler_packet.json`

## Output

- `qi_executable_action_recipe_batch_packet.json`
- `qi_executable_action_recipe_batch_compiler_receipt.json`
- `qi_executable_action_recipe_batch_compiler_audit.jsonl`

## Batch recipes

- `observe_adapt_twice`
- `observe_supervise_adapt`
- `cycle_observe_adapt`
- `return_cycle_observe`
- `safe_full_observe_adapt_run`

## Boundary

This compiler does not execute recipes. It only emits a bounded v4.6 batch packet from a named allowlisted batch recipe.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_action_recipe_batch_compiler_v4_7.py
```
