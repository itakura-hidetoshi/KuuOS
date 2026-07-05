# KuuOS Repository Structure Map v0.38

This stage follows repository self-organization index v0.37.

It does not move files.

It defines the target map used before future cleanup.

## Directory zones

| Path | Responsibility |
|---|---|
| `runtime/` | Executable runtime modules and deterministic checks. |
| `tests/` | Unit and integration tests. |
| `formal/` | Lean proof-facing declarations and aggregate imports. |
| `docs/` | Human-readable design, roadmap, and status documents. |
| `manifests/` | Small machine-readable stage metadata. |
| `ci/check_registry.d/` | Registry snippets and check notes. |
| `scripts/` | Operator compatibility entrypoints and wrappers. |

## Cleanup principles

Prefer an index or alias before moving files.

Every active line should be reachable from a declared root or explicitly marked as legacy.

Unmerged proposal material should not be promoted into current roots.

Closed repository mutation and lifecycle completion remain separate lines.

Manifest files should stay small.

Design prose belongs in docs.

Runtime enforcement belongs in runtime and tests.

## Focused check

```bash
python3 -m unittest tests.test_kuuos_repository_structure_map_v0_38
```

## Current root follow-up

The current runtime root should include this structure map test after the v0.37 repository index check.
