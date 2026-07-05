# KuuOS Current Root Sequence v0.41

This stage follows repository frontier summary v0.40.

It keeps the current runtime root small.

The current root delegates its run order to a dedicated sequence module.

## Files

```text
runtime/kuuos_current_check.py
runtime/kuuos_current_root_sequence_v0_41.py
tests/test_kuuos_current_root_sequence_v0_41.py
```

## Focused check

```bash
python3 -m unittest tests.test_kuuos_current_root_sequence_v0_41
```

## Full current root

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

The sequence keeps each step explicit and required.

The root remains an entrypoint, not a place for long policy detail.
