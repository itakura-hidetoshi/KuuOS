# KuuOS README Surface Exposure v0.78

This stage follows KuuOS Current Surface Stable CLI v0.77.

It updates README.md so the human entrypoint exposes the machine-readable current surface.

## Concrete repository effect

- `README.md` now points to `runtime/kuuos_current_surface.py`.
- `README.md` now points to `status/current.surface.index.json`.
- `README.md` now points to `status/current.surface.json`.
- `tests/test_kuuos_readme_surface_status_v0_78.py` verifies the README surface exposure and non-authority boundaries.
- `runtime/kuuos_current_root_sequence_v0_78.py` adds the README surface exposure test to the current root sequence.
- `runtime/kuuos_current_check.py` now routes through `kuuos_current_root_sequence_v0_78`.

## Stable human and machine entrypoints

```text
README.md
runtime/kuuos_current_surface.py
status/current.surface.index.json
status/current.surface.json
```

## Focused checks

```bash
python3 runtime/kuuos_current_check.py
python3 -m unittest tests.test_kuuos_readme_surface_status_v0_78
python3 -m unittest tests.test_kuuos_current_root_sequence_v0_78
```

## Boundary

README surface exposure is a discovery layer.

It does not grant unbounded repository mutation authority.
