# KuuOS Current Surface Stable CLI v0.77

This stage follows KuuOS Current Status Surface Index v0.76.

It adds a stable CLI for reading the current status surface.

## Concrete repository effect

- `runtime/kuuos_current_surface_entrypoint_v0_77.py` validates the surface index and returns the current surface artifact.
- `runtime/kuuos_current_surface.py` is the stable CLI for the current surface.
- `tests/test_kuuos_current_surface_entrypoint_v0_77.py` verifies the versioned entrypoint.
- `tests/test_kuuos_current_surface_cli_v0_77.py` verifies the stable CLI.
- `runtime/kuuos_current_root_sequence_v0_77.py` adds the entrypoint and CLI tests to the current root sequence.
- `runtime/kuuos_current_check.py` now routes through `kuuos_current_root_sequence_v0_77`.

## Stable CLI

```bash
PYTHONPATH=. python3 runtime/kuuos_current_surface.py
```

## Focused checks

```bash
python3 runtime/kuuos_current_check.py
python3 runtime/kuuos_current_surface_entrypoint_v0_77.py
python3 runtime/kuuos_current_surface.py
python3 -m unittest tests.test_kuuos_current_surface_entrypoint_v0_77
python3 -m unittest tests.test_kuuos_current_surface_cli_v0_77
python3 -m unittest tests.test_kuuos_current_root_sequence_v0_77
```

## Boundary

The current surface CLI reports repository status.

It does not grant unbounded repository mutation authority.
