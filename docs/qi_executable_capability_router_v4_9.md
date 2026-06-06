# Qi Executable Capability Router v4.9

Unified bounded capability router for the Qi executable stack.

This layer increases executable usability by providing one safe entry point that can delegate to the existing bounded execution surfaces.

## Input

- `qi_executable_capability_packet.json`

## Outputs

- one delegated input packet, depending on capability kind
- `qi_executable_capability_router_receipt.json`
- `qi_executable_capability_router_audit.jsonl`

## Capability kinds

- `action_dispatch` -> v4.2 dispatcher
- `action_sequence` -> v4.3 sequence runner
- `recipe_compile` -> v4.4 recipe compiler
- `recipe_execute` -> v4.5 recipe executor
- `recipe_batch_execute` -> v4.6 recipe batch executor
- `batch_recipe_compile` -> v4.7 batch recipe compiler
- `batch_recipe_execute` -> v4.8 batch recipe executor

## Boundary

This router does not create arbitrary execution. It only delegates to existing bounded surfaces when the capability packet and router license both allow the selected capability.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_capability_router_v4_9.py
```
