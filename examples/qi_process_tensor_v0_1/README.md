# KuuOS Qi Process Tensor Example v0.1

This example shows process-level Qi flowing into the KuuOS closed loop through `process_history`.

The raw state does **not** need to manually set `process_tensor_visible`. Instead, the process tensor evaluator derives:

- `process_tensor_visible`
- `transition_continuity_visible`
- `memory_continuity_visible`
- `nonmarkov_memory_visible`

from the `process_history` entries.

## Check

```bash
python3 scripts/check_kuuos_qi_process_tensor_example_v0_1.py
```

## Boundary

This is non-authoritative. Process tensor support helps candidate flow, but it does not grant execution authority, truth authority, clinical authority, theorem authority, memory overwrite authority, or final commitment authority. Boundary failure still blocks process tensor support.
