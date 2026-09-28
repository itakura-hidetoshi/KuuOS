# KuuOS Development Lineage Re-rooting v7.32

## Purpose

v7.31 closes one complete repository-development lineage:

```text
candidate
-> authority
-> expected-head merge
-> merged main
-> post-merge CI
-> closed lineage
```

v7.32 does not reopen that lineage.

Instead it uses the closed receipt as immutable predecessor evidence and creates a fresh root for the next development lineage.

```text
closed lineage
+
fresh current main
->
new lineage root
```

No authority crosses that boundary.

## Closed receipt is history, not authority

The v7.31 closure proves what happened. It does not authorize what happens next.

```text
closed receipt != successor authority
old merge authority != new merge authority
old write authority != new write authority
```

If an observation claims that predecessor authority is being reused, v7.32 records:

```text
predecessor_authority_carryover_obstruction
```

The new root always has:

```text
successor_write_authority_granted = false
successor_merge_authority_granted = false
```

Any later mutation must acquire authority again.

## Exact current main

The simplest case is:

```text
current main HEAD
=
v7.31 merge commit
```

A fresh main observation is enough to create:

```text
new_lineage_root_ready_exact_closed_merge
```

No ancestry comparison is required because identity itself proves the relation.

## Main may advance

The next lineage must not be blocked merely because another valid change reached main after the previous lineage closed.

Suppose:

```text
closed merge = M
current main = N
M != N
```

v7.32 accepts N as the new root when a fresh compare observation proves:

```text
base = M
head = N
status = ahead
ahead_by > 0
behind_by = 0
```

Then:

```text
new_lineage_root_ready_descendant_main
```

This preserves the historical lineage while starting from the real current repository state.

The old post-merge CI receipt does not certify N. It certifies only the old merge commit.

## Missing ancestry is not rejection

If main advanced but no fresh ancestry comparison is available:

```text
closed_merge_ancestry_reobservation_required
```

The prior closed lineage remains valid. The system simply cannot yet bind the next root.

## Diverged history

If fresh comparison says the old merge is not an ancestor of current main, for example `diverged`, or current main is behind the closed merge, v7.32 records:

```text
closed_merge_not_ancestor_of_current_main_obstruction
```

This is a real history-binding problem rather than ordinary repository movement.

## Local Git is a separate surface

A remote new root can be known even when the local worktree is stale.

If:

```text
fresh remote main = N
local Git HEAD = L
L != N
```

the root is still formed:

```text
new_lineage_root_ready_local_revision_reconciliation_required
```

with:

```text
local_reconciliation_required = true
```

The next remote-bound action must reconcile the local revision first, but read/analysis work does not require pretending that the remote root is unknown.

If local Git has not been observed at all, remote re-rooting is still allowed; local observation remains a follow-up requirement.

## Root identity

The new lineage root is identified from:

- repository;
- predecessor closure packet digest;
- predecessor merge commit;
- fresh current main SHA;
- fresh current main observation digest.

Authority is deliberately excluded from the root identity.

Changing the current main changes the root identity.

## Validation

Focused tests verify:

1. exact closed merge becomes the next root;
2. descendant current main becomes the next root with fresh ancestry evidence;
3. advanced main without ancestry evidence remains partial;
4. diverged history is obstructed;
5. stale local Git does not reject a valid remote root;
6. missing local observation does not reject a valid remote root;
7. predecessor merge/write authority cannot be reused;
8. a closure receipt cannot issue successor authority;
9. missing current-main observation requests re-observation;
10. a nonclosed source is not applicable;
11. root identity changes when fresh main changes.

> **Closure is a durable predecessor fact, not a reusable capability; the next development lineage begins from freshly observed current reality.**
