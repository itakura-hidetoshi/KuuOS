# KuuOS Git Admission and Post-Commit Coherence v7.28

## Purpose

v7.27 ends at:

```text
repair_locally_verified_git_admission_ready
```

That is deliberately not the same thing as:

```text
local commit exists
```

and it is also not:

```text
remote publish ready
```

v7.28 adds the missing local Git admission and post-commit re-observation layer.

The chain is:

```text
v7.27 verified post-edit bytes
-> workspace Git authority
-> local Git admission receipt
-> commit
-> post-commit Git observation
-> post-commit Filesystem observation
-> post-commit Lean-LSP observation
-> fresh GitHub remote-base observation
-> remote publish candidate
-> separate GitHub write authority
-> remote publish ready
```

This layer does not itself perform a remote publish.

## Commit preimage

The local commit must be derived from the exact bytes validated by v7.27.

v7.28 requires:

```text
commit.pre_commit_target_content_digest
=
v7.27.post_edit_content_digest
```

and:

```text
commit.committed_target_content_digest
=
v7.27.git_diff_target_post_content_digest
```

If these do not match, the result is:

```text
git_commit_lineage_obstruction
```

This is a true lineage obstruction because the committed object is no longer the candidate that was semantically verified.

## Workspace authority

A v7.27 candidate may be semantically ready while local Git write authority is absent.

In that case v7.28 records:

```text
git_admission_workspace_authority_required
```

The candidate is retained.

Thus:

```text
missing workspace authority
!=
candidate rejection
```

## Commit receipt

With workspace authority present, an actual local Git admission still needs an explicit receipt.

If no commit receipt exists:

```text
git_commit_receipt_required
```

The evidence layer does not pretend that semantic readiness created a commit.

## Post-commit Git coherence

After commit:

```text
post_commit_git_head_sha
=
commit_sha
```

must hold.

The commit is therefore observed as the actual current local revision rather than inferred from a prior intent.

## Post-commit Filesystem coherence

The target file currently visible through Filesystem must equal the committed target content:

```text
Filesystem(target)
=
committed_target
```

This catches edits made after commit but before publication.

## Post-commit Lean coherence

Lean-LSP must analyze exactly the post-commit Filesystem bytes:

```text
Lean.source_digest
=
Filesystem.content_digest
=
committed_target_digest
```

If the Lean observation is stale, v7.28 records:

```text
post_commit_cross_surface_reobservation_required
```

and retains the local commit.

If fresh post-commit Lean semantics unexpectedly contain errors, the state is:

```text
post_commit_lean_semantic_regression
```

The commit is still retained as an observed local fact, but it is not a remote publish candidate.

## Remote base freshness

A local repair commit is normally created from a previously observed GitHub remote head.

Before publication v7.28 checks:

```text
current_github_remote_head_sha
=
commit_parent_sha
```

If the remote branch moved while local repair was occurring:

```text
remote_revision_reconciliation_required_after_local_commit
```

The local commit is not erased or rejected.

It simply cannot yet become a publish candidate against the stale base.

## GitHub authority

When all local/post-commit surfaces are coherent and the remote base is still current, v7.28 forms:

```text
remote_publish_candidate = true
```

If GitHub write authority is absent:

```text
remote_publish_candidate_github_authority_required
```

The candidate remains valid.

Only when the separate GitHub authority is present does the state become:

```text
remote_publish_candidate_ready
```

Even this state does not execute the remote mutation.

## Dirty elsewhere

The local worktree may contain unrelated edits after the repair commit.

That does not automatically invalidate the committed target.

If the committed target, Filesystem target, and Lean target remain coherent, v7.28 emits a warning:

```text
post_commit_worktree_dirty_elsewhere_does_not_invalidate_committed_target
```

rather than a blanket failure.

Similarly, supporting files in the same commit are reviewable:

```text
supporting_committed_paths_present_review_before_remote_publish
```

## Authority separation

The following remain distinct:

```text
semantic repair success
!=
local Git write authority

local commit
!=
remote publish

post-commit Lean success
!=
GitHub write authority

remote publish candidate
!=
remote publish execution
```

This continues the KuuOS pattern of retaining useful action candidates while keeping authority explicit.

## Validation

Focused tests verify:

1. coherent commit plus GitHub authority reaches `remote_publish_candidate_ready`;
2. missing GitHub authority retains a valid publish candidate;
3. missing workspace authority retains the Git-admission candidate;
4. authorized but uncommitted state requests a commit receipt;
5. commit preimage mismatch is a true lineage obstruction;
6. stale post-commit Lean semantics request re-observation;
7. post-commit Lean regression retains the local commit but blocks publication;
8. remote-head movement retains the local commit for reconciliation;
9. dirty elsewhere and supporting committed files are reviewable rather than blanket failures;
10. non-ready v7.27 candidates return to the bounded repair loop.

## Next

The next stage should consume `remote_publish_candidate_ready`, perform an explicitly authorized GitHub MCP branch/ref mutation, bind the mutation receipt to the local commit SHA, and then require fresh remote exact-head plus CI re-observation before merge candidacy.
