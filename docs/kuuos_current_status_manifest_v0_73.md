# KuuOS Current Status Manifest v0.73

This stage follows KuuOS Current Resolved Status Artifact v0.72.

It adds a stable manifest for the machine-readable KuuOS status surface.

The manifest points to the stable pointer, status index, self-organization snapshot, resolved status artifact, stable CLI, and current root check.

## Concrete repository effect

- `status/current.manifest.json` records the current status surface paths.
- `runtime/kuuos_current_status_manifest_v0_73.py` validates the manifest and the referenced artifacts.
- `tests/test_kuuos_current_status_manifest_v0_73.py` verifies the manifest path, payload equality, JSON round trip, and authority boundary.
- `runtime/kuuos_current_root_sequence_v0_73.py` adds the manifest test to the current root sequence.
- `runtime/kuuos_current_check.py` now routes through `kuuos_current_root_sequence_v0_73`.

## Stable manifest path

```text
status/current.manifest.json
```

## Focused checks

```bash
python3 runtime/kuuos_current_check.py
python3 runtime/kuuos_current_status_manifest_v0_73.py
python3 -m unittest tests.test_kuuos_current_status_manifest_v0_73
python3 -m unittest tests.test_kuuos_current_root_sequence_v0_73
```

## Boundary

The current status manifest is a discovery artifact.

It does not grant unbounded repository mutation authority.

It does not deploy a production runtime.
