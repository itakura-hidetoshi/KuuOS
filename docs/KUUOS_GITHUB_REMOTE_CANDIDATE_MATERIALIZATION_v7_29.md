# KuuOS GitHub Remote Candidate Materialization v7.29

## Purpose

v7.28 proves that one local repair commit is coherent across local Git, Filesystem, Lean-LSP, and the still-current GitHub base.

It ends at:

```text
remote_publish_candidate_ready
```

v7.29 connects that state to the remote Git object database.

The crucial point is that a local-only commit SHA cannot simply be passed to GitHub branch creation.

GitHub can only create a ref to a commit object already present in its repository object database.

Therefore the correct remote publication sequence is:

```text
verified local candidate
-> remote blobs
-> remote tree
-> remote commit
-> remote candidate branch
-> fresh remote observation
```

## Why local and remote commit SHA may differ

The current GitHub connector exposes:

```text
create_blob
create_tree
create_commit
create_branch / update_ref
```

but the `create_commit` surface accepts:

- message;
- tree SHA;
- parent SHA(s).

It does not expose all author/committer metadata and timestamps required to guarantee reproduction of an arbitrary pre-existing local Git commit object.

Therefore v7.29 does not assert:

```text
local_commit_sha = remote_commit_sha
```

as a universal requirement.

Instead it distinguishes:

```text
Git commit identity
```

from:

```text
publish-candidate invariant
```

The remote commit may be admitted as an equivalent presentation only when the bounded invariant agrees:

```text
changed-path content digests
+
tree content digest
+
parent SHA
+
commit message digest
```

If the SHA happens to match exactly, v7.29 records:

```text
exact_git_commit_identity
```

Otherwise the accepted relation is:

```text
content_parent_message_equivalent_distinct_git_commit_identity
```

This is not a claim that arbitrary different Git SHAs are interchangeable.

## Relation to v0.94-v0.97

KuuOS already separates local repository mutation into:

```text
v0.94 object materialization authorization
v0.95 object materialization receipt
v0.96 reference update authorization
v0.97 atomic modeled reference transition
```

v7.29 mirrors that separation on the GitHub remote surface.

Objects are materialized first.

The visible branch reference is created only after object equivalence is established.

## Why a new candidate branch is preferred

Updating `main` directly would combine candidate publication with base-branch mutation.

v7.29 instead requires:

```text
candidate_branch != base_branch
```

and prefers a fresh candidate branch.

This gives:

```text
main remains unchanged
candidate commit becomes reachable
CI can run on the candidate branch/PR
merge remains a later authority domain
```

## Branch name collision

A pre-existing branch with a different SHA does not invalidate the already materialized commit objects.

The state becomes:

```text
remote_candidate_branch_reselection_required
```

The candidate is retained and a fresh branch name can be selected.

If the pre-existing branch already points to the exact remote materialized commit, publication is treated idempotently.

## Base movement

The base branch may move while remote object materialization is occurring.

If the candidate branch was successfully published but:

```text
base_after != local_commit_parent
```

v7.29 records:

```text
remote_candidate_published_base_reconciliation_required
```

The published candidate is retained.

It is not silently merged against a stale base.

## Partial object materialization

Git blobs, trees, and commits are immutable objects.

A failed sequence may therefore leave unreachable objects in the remote object database even when no branch ref was created.

v7.29 explicitly records:

```text
partial_remote_objects_may_exist
```

and does not describe such a case as “no effect”.

This follows the same effect-boundary discipline as v0.95.

## MCP and REST boundary

The official GitHub MCP server currently used by KuuOS does not expose the low-level Git Data object tools needed for arbitrary commit materialization.

The KuuOS GitHub MCP Server Bridge v0.2 already defines Git-object mutation as an exact-SHA delegated domain rather than unrestricted direct MCP mutation.

v7.29 stays inside that architecture.

MCP write authority remains the outer authority boundary; low-level object materialization is performed by the bounded Git Data executor/delegate.

## Publication is not CI success

A successful candidate-branch publication yields:

```text
remote_candidate_published_ci_reobservation_required
```

and:

```text
merge_candidate = false
```

The next stage must freshly observe:

- the exact remote candidate head;
- the current base;
- required GitHub Actions / CI receipts.

Only then may merge candidacy be considered.

## Validation

Focused tests verify:

1. a remote commit with a different SHA can represent the same bounded publish candidate when content/tree/parent/message invariants match;
2. exact local/remote commit SHA equality is accepted when it genuinely occurs;
3. missing GitHub authority retains the local candidate;
4. authorized but not yet materialized candidates request a materialization receipt;
5. remote blob-content mismatch is a true materialization obstruction and acknowledges possible partial remote objects;
6. materialized objects may wait for later branch publication;
7. branch-name conflict retains the materialized commit and requests branch reselection;
8. a branch already at the remote commit is idempotently accepted;
9. base movement after publication retains the candidate for reconciliation;
10. a non-ready v7.28 packet returns to v7.28.

## Next

The next stage is fresh remote exact-head and CI re-observation bound to the remote materialized commit SHA. Only successful current-head CI evidence may form merge candidacy.
