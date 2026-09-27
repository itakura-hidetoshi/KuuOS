# KuuOS Development MCP Federation v7.19

## Purpose

v7.16-v7.18 verified the individual development MCP surfaces.

v7.19 connects them without collapsing their meanings.

```text
GitHub MCP
-> remote repository / PR / CI state

Git MCP
-> local revision / diff / worktree state

Filesystem MCP
-> current working bytes

Lean-LSP MCP
-> semantic state of those current bytes
```

The central rule is:

```text
same repository
!=
same observation surface
```

Each plane observes a different conditioned aspect of the development world.

## Dirty worktree is not an error

KuuOS development necessarily passes through states that are not committed.

Therefore:

```text
dirty_worktree_is_error = false
```

If the selected file differs from the Git commit baseline but Lean-LSP has analyzed exactly the current Filesystem bytes, v7.19 records:

```text
dirty_local_candidate_semantically_fresh
```

and permits continued local repair.

This is the normal edit loop:

```text
committed file
-> local edit
-> Filesystem bytes
-> Lean diagnostics
-> further edit
-> Git diff review
```

A dirty worktree is a candidate state, not a failed repository.

## Lean semantic freshness

Lean diagnostics are useful only for the bytes they actually describe.

v7.19 therefore binds:

```text
Lean-LSP source_content_digest
=
Filesystem content_digest
```

If the file changes after a Lean observation, the old diagnostics become:

```text
dirty_local_candidate_semantic_reobservation_required
```

The candidate bytes are preserved.

KuuOS does not discard the edit.

It simply requests a fresh semantic observation.

## Commit baseline

The existing Repository Git Revision Adapter v0.83 deliberately reads commit-tree objects and ignores the dirty working tree.

v7.19 preserves that rule.

The committed baseline comes from:

```text
Git commit tree/blob
```

while the development candidate comes from:

```text
Filesystem MCP current bytes
```

Thus:

```text
commit-tree truth
!=
working-tree candidate
```

but both can participate in one development lineage.

## Clean-tree inconsistency

If Git reports:

```text
worktree_clean = true
```

and the selected tracked file's Filesystem digest differs from the Git blob digest, the surfaces contradict one another.

That becomes:

```text
clean_worktree_filesystem_git_baseline_obstruction
```

This is different from an ordinary dirty candidate.

## Remote/local revision divergence

Suppose:

```text
GitHub remote head != local Git head
```

v7.19 records:

```text
remote_local_revision_reconciliation_required
```

but keeps:

```text
local_semantic_work_allowed = true
```

Local reading, editing, Lean diagnostics and reasoning may continue.

Only remote mutation requires revision reconciliation first.

Therefore:

```text
remote mismatch
!=
global development block
```

## Untracked files

A new local Lean file may not yet exist in the Git commit tree.

If the Filesystem file exists and Lean-LSP has fresh diagnostics for those exact bytes, v7.19 records:

```text
untracked_local_candidate_semantically_fresh
```

The file may continue through local semantic development.

Admission to Git remains a separate decision.

## Dirty elsewhere

A repository can be dirty while the selected target file still exactly matches its committed Git blob.

v7.19 distinguishes this as:

```text
workspace_dirty_elsewhere_selected_file_committed
```

The selected file's semantic observation is not invalidated merely because another file changed.

## Remote mutation

Even when the workspace state is suitable for a future remote operation:

```text
remote_mutation_eligible_before_authority_check = true
```

does not grant authority.

The actual mutation still requires the existing KuuOS GitHub/workspace authorization path.

Thus:

```text
semantic freshness
!=
Git write authority
```

and:

```text
verified MCP compatibility
!=
source authority transfer
```

## Four-plane development loop

The preferred KuuOS development cycle is now:

```text
GitHub exact-head observation
        |
        v
local Git revision observation
        |
        v
Filesystem current bytes
        |
        v
Lean-LSP semantic observation
        |
        v
local repair
        |
        v
Git diff review
        |
        v
remote/local revision reconciliation
        |
        v
explicit authorized GitHub mutation
        |
        v
exact-head CI
```

This moves semantic error detection earlier without weakening the final exact-head repository receipt.

## Relation to dependent origination

The same source file has several valid conditioned presentations:

```text
remote commit identity
local commit identity
working bytes
Lean semantic state
```

No one presentation should be mistaken for all the others.

The development state is therefore relational:

```text
semantic state
depends on current bytes

current bytes
may differ from commit baseline

local commit
may differ from remote commit

remote mutation
depends on explicit authority
```

This is a development-specific instance of the wider KuuOS non-collapse architecture.

## Validation

Focused tests verify:

1. clean exact-head state with fresh Lean semantics;
2. dirty local edits remain valid when Lean semantics are fresh;
3. stale Lean semantics request reobservation without discarding the edit;
4. remote/local head divergence blocks only remote mutation, not local analysis;
5. clean Git state plus differing filesystem bytes is a true cross-surface obstruction;
6. untracked files can receive fresh Lean semantic analysis before Git admission;
7. changes elsewhere do not invalidate a committed selected file;
8. Lean observation for another file cannot be substituted for the target file.

The central law is:

> **KuuOS development may continue through uncommitted and locally divergent states as long as each semantic observation remains bound to the bytes and revision context that actually produced it.**
