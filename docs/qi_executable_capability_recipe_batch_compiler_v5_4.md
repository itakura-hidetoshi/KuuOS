# Qi Executable Capability Recipe Batch Compiler v5.4

Batch compiler for high-level Qi executable capability recipe batches.

This layer translates named safe capability recipe batch plans into v5.3 capability recipe batch packets.

## Input

- `qi_executable_capability_recipe_batch_compiler_packet.json`

## Output

- `qi_executable_capability_recipe_batch_packet.json`
- `qi_executable_capability_recipe_batch_compiler_receipt.json`
- `qi_executable_capability_recipe_batch_compiler_audit.jsonl`

## Batch recipes

- `compile_surface_twice`
- `compile_then_execute_surface`
- `batch_compile_then_execute_surface`
- `observe_compile_batch_surface`
- `safe_full_capability_batch_surface`

## Boundary

This compiler does not execute capability recipes. It only emits a bounded v5.3 capability recipe batch packet from a named allowlisted capability recipe batch.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_capability_recipe_batch_compiler_v5_4.py
```
