# KuuOS Repository Checkpoint Evolution Workspace v1.04

v1.04 turns a confirmed repository checkpoint into an isolated, deterministic evolution workspace.

The layer is functional rather than observational:

```text
confirmed checkpoint
→ immutable workspace seed
→ isolated mutable workspace
→ candidate-bound atomic file plan
→ transformed workspace tree
→ optional filesystem materialization
```

It does not add another delayed receipt or stability certificate.

## Core capability

A committed and confirmed v1.03 checkpoint can seed one or more independent workspaces.

Each workspace contains an explicit file tree, checkpoint OID, checkpoint reference, repository identity, and deterministic tree digest.

A candidate plan can atomically perform:

- add text file
- replace text file with expected-content compare-and-swap
- delete text file with expected-content compare-and-swap
- move text file with expected-content compare-and-swap

A successful plan produces a new workspace tree and increments its sequence number once.

A failed plan returns the exact source workspace without partial edits or sequence advance.

## Candidate binding

The plan is bound to a v0.87 repository evolution candidate.

The candidate source frontier commit must equal the checkpoint OID.

The candidate proposal digest must equal the deterministic workspace-plan proposal digest.

The candidate changed paths must equal the paths affected by the plan.

## Filesystem materialization

A validated workspace can be written to a new destination directory through a staging directory and atomic directory rename.

The adapter rejects an existing destination and path traversal.

It does not invoke Git and does not write into the source repository.

## Reset and fork

A workspace may be reset to its checkpoint seed.

Multiple workspaces may be initialized from the same seed and evolved independently.

## Validation

Focused:

```bash
python3 -m unittest -v tests.test_kuuos_repository_checkpoint_evolution_workspace_v1_04
```

Cumulative:

```bash
python3 runtime/kuuos_v104_check.py
```
