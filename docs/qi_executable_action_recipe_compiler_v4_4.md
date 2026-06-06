# Qi Executable Action Recipe Compiler v4.4

Recipe compiler for the Qi executable action sequence runner.

This layer increases execution coverage by translating named safe recipes into v4.3 sequence packets.

## Input

- `qi_executable_action_recipe_packet.json`

## Output

- `qi_executable_action_sequence_packet.json`
- `qi_executable_action_recipe_compiler_receipt.json`
- `qi_executable_action_recipe_compiler_audit.jsonl`

## Recipes

- `observe_and_adapt`
- `observe_adapt_and_run`
- `supervise_then_summarize`
- `single_cycle_then_summarize`
- `return_loop_then_cycle`

## Boundary

This compiler does not execute actions. It only emits a bounded v4.3 sequence packet from a named allowlisted recipe.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_action_recipe_compiler_v4_4.py
```
