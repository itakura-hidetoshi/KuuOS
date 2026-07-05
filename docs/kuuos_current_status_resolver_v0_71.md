# KuuOS Current Status Resolver v0.71

This stage follows KuuOS Current Status Pointer v0.70.

It adds a stable resolver for the machine-readable KuuOS status surface.

The resolver starts from `status/current.json`, follows the current status index, follows the current self-organization snapshot, and emits one resolved JSON payload.

## Concrete repository effect

- `runtime/kuuos_current_status_resolver_v0_71.py` resolves the current pointer, status index, and snapshot.
- `runtime/kuuos_current_status.py` provides a stable unversioned CLI entrypoint.
- `tests/test_kuuos_current_status_resolver_v0_71.py` verifies the resolved payload and JSON round trip.
- `tests/test_kuuos_current_status_cli_v0_71.py` verifies the stable CLI surface.
- `runtime/kuuos_current_root_sequence_v0_71.py` adds the resolver and CLI tests to the current root sequence.
- `runtime/kuuos_current_check.py` now routes through `kuuos_current_root_sequence_v0_71`.

## Stable CLI

```bash
PYTHONPATH=. python3 runtime/kuuos_current_status.py
```

## Focused checks

```bash
python3 runtime/kuuos_current_check.py
python3 runtime/kuuos_current_status.py
python3 runtime/kuuos_current_status_resolver_v0_71.py
python3 -m unittest tests.test_kuuos_current_status_resolver_v0_71
python3 -m unittest tests.test_kuuos_current_status_cli_v0_71
python3 -m unittest tests.test_kuuos_current_root_sequence_v0_71
```

## Boundary

The resolver reports repository status.

It does not grant unbounded repository mutation authority.

It does not deploy a production runtime.
