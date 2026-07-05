# KuuOS Repository Cleanup Proposals v0.39

This stage follows Repository Structure Map v0.38.

It does not move files.

It does not delete files.

It creates a safe proposal list for later cleanup work.

## Proposal classes

| Proposal | Target | Kind |
|---|---|---|
| docs-status-frontier-summary | `docs/` | Add concise status summary document. |
| runtime-current-root-commentary | `runtime/` | Keep current root small and delegated. |
| manifest-small-metadata-rule | `manifests/` | Keep manifests short and metadata-only. |
| ci-note-to-registry-candidate | `ci/check_registry.d/` | Normalize check notes only when safe. |
| legacy-entrypoint-labeling | `scripts/` | Label legacy wrappers without removing them. |

## Safety rules

The proposals are read-only at this stage.

They do not authorize physical file moves.

They do not authorize deletion.

They do not promote unmerged proposal material.

They do not create a new mutation roadmap successor.

## Focused check

```bash
python3 -m unittest tests.test_kuuos_repository_cleanup_proposals_v0_39
```

## Current root follow-up

The current runtime root should include this proposal check after the v0.38 structure map check.
