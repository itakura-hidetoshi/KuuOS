# KuuOS Current Resolved Status Artifact v0.72

This stage follows KuuOS Current Status Resolver v0.71.

It commits the resolved current status payload as a repository artifact.

The artifact must match the output of the stable current status resolver.

## Concrete repository effect

- `status/current.resolved.json` stores the resolved current status payload.
- `runtime/kuuos_current_resolved_status_artifact_v0_72.py` validates the committed artifact against the v0.71 resolver output.
- `tests/test_kuuos_current_resolved_status_artifact_v0_72.py` verifies the artifact path, payload equality, JSON round trip, and authority boundary.
- `runtime/kuuos_current_root_sequence_v0_72.py` adds the artifact test to the current root sequence.
- `runtime/kuuos_current_check.py` now routes through `kuuos_current_root_sequence_v0_72`.

## Stable artifact path

```text
status/current.resolved.json
```

## Focused checks

```bash
python3 runtime/kuuos_current_check.py
python3 runtime/kuuos_current_resolved_status_artifact_v0_72.py
python3 -m unittest tests.test_kuuos_current_resolved_status_artifact_v0_72
python3 -m unittest tests.test_kuuos_current_root_sequence_v0_72
```

## Boundary

The resolved artifact reports repository status.

It does not grant unbounded repository mutation authority.

It does not deploy a production runtime.
