# KuuOS Repository Self-Organization v0.37

This layer adds a machine-readable map of the current KuuOS repository surface.

The goal is not to move or delete existing files.

The goal is to make the current structure easier to understand and safer to extend.

## What is organized

The index separates these surfaces.

- current runtime root
- closed repository mutation root
- legacy compatibility root
- Lean aggregate root
- lifecycle completion test
- repository index test

## Current root

```text
runtime/kuuos_current_check.py
```

The current root should run the closed mutation root and the current lifecycle completion test.

This v0.37 layer also adds a repository index check to that root.

## Closed mutation line

```text
runtime/kuuos_v124_check.py
```

The repository mutation research line remains closed at v1.24.

This line does not create v1.25 authority.

## Lifecycle line

```text
tests.test_kuuos_lifecycle_completion_v0_36
```

The lifecycle line is treated as completed at v0.36.

Completion does not create a following lifecycle route.

## New index check

```bash
python3 -m unittest tests.test_kuuos_repo_index_v0_37
```

The check verifies that the main lines and roots are listed once, that the current root includes the right active checks, and that closed mutation and lifecycle completion remain separate.

## Safety

This layer is read-only as a repository map.

It does not move files.

It does not delete files.

It does not perform live repository mutation.

It creates a stable index that later cleanup work can follow.
