# KuuOS Expected-Head Merge Closure v7.31

## Purpose

v7.30 ends at:

```text
merge_candidate = true
merge_authority_granted = false
```

v7.31 closes the remaining development cycle.

The chain is:

```text
v7.30 exact merge candidate
-> independently supplied merge authority
-> fresh pre-merge head/base check
-> existing GitHub MCP Bridge v0.2 exact_git_action
-> expected-head merge
-> fresh merged-PR observation
-> fresh main-head observation
-> fresh post-merge CI re-observation
-> development lineage closed
```

The central rule is that none of the earlier evidence is silently promoted into merge authority.

## Independent merge authority

v7.31 consumes a separate authority packet:

```text
kuuos_expected_head_merge_authority_v7_31
```

It must bind exactly:

- repository;
- pull request number;
- v7.30 candidate head SHA;
- v7.30 base SHA;
- merge method;
- source v7.30 packet digest;
- authority scope digest.

Therefore:

```text
all CI green
!= merge authority

merge_candidate = true
!= merge authority
```

If authority is simply absent, the candidate remains:

```text
merge_authority_required
```

This is partial state, not rejection.

If an authority packet exists but is bound to another PR/head/base, the state is:

```text
merge_authority_binding_obstruction
```

because that is contradictory authority evidence rather than ordinary absence.

## Pre-merge re-observation

Even valid authority is not enough if the repository moved.

Immediately before merge, v7.31 requires:

```text
fresh PR head = v7.30 expected head
fresh base head = v7.30 expected base
```

If either changed:

```text
pre_merge_revision_reconciliation_required
```

The candidate is retained.

The system returns to fresh v7.30 candidacy rather than merging stale revisions.

## Existing expected-head merge path

v7.31 does not create a new GitHub mutation mechanism.

It reuses:

```text
KuuOS GitHub MCP Server Bridge v0.2
```

through:

```text
exact_git_action
  -> merge_pr
```

The existing bridge performs the important split:

```text
GitHub MCP capability discovery
!=
unbounded Git mutation
```

For merge, v0.2 delegates to the bounded exact-SHA GitHub path with:

```text
PR number
expected head SHA
expected base SHA checked before delegation
merge method
```

The v7.31 checker actually runs this existing bridge in mock mode and requires one exact delegated merge receipt.

## Merge receipt

A merge attempt is accepted only when the bridge evidence says:

```text
KUUOS_GITHUB_MCP_WRITE_BRIDGE_APPLIED
delegated_applied_count = 1
action kind = merge_pr
expected head = v7.30 candidate head
expected base = v7.30 base
merge result merged = true
merge result SHA present
```

A wrong expected head/base is not a normal merge failure. It is a receipt-binding obstruction.

A bridge that simply does not apply the merge yields:

```text
expected_head_merge_not_applied_reobservation_required
```

and remains partial.

## Merge success does not close the lineage

After GitHub reports a successful merge, v7.31 still does not declare completion.

It requires fresh observation of both:

```text
main HEAD
merged PR
```

and both must identify the same merge commit.

If the PR/main observations are absent:

```text
post_merge_main_pr_reobservation_required
```

If main has already advanced beyond the successful merge commit:

```text
post_merge_main_advanced_reconciliation_required
```

The successful merge fact is retained; later movement of main does not erase history.

## Post-merge CI

The merge commit then receives the same bounded CI truth discipline already used elsewhere in KuuOS:

```text
workflow event
!= verified CI evidence
```

Each required post-merge workflow must have a fresh:

```text
kuuos_github_ci_completion_reentry_v1_1
```

packet whose head SHA is exactly the merge commit.

Missing post-merge CI gives:

```text
post_merge_ci_reobservation_required
```

A real verified CI failure gives:

```text
post_merge_ci_non_success_followup_required
```

The merge fact is retained and repair continues on the merged repository state.

There is no automatic rollback:

```text
post-merge CI failure
!= automatic rollback
```

Malformed or stale-head CI evidence gives the stronger:

```text
post_merge_ci_binding_obstruction
```

## Closure

Only the full conjunction:

```text
exact v7.30 candidacy
+
independent exact merge authority
+
fresh pre-merge head/base
+
applied expected-head merge receipt
+
fresh merged PR
+
fresh main head at merge commit
+
all required post-merge CI freshly verified successful
```

produces:

```text
development_lineage_closed
```

This is a durable completion fact for that development lineage.

It is not authority for a future repository mutation.

## Validation

The focused checker verifies:

1. complete expected-head merge + fresh post-merge CI closes the lineage;
2. absent merge authority retains the candidate;
3. mismatched explicit authority is a true binding obstruction;
4. pre-merge head movement requests reconciliation;
5. authority without merge execution requests a merge receipt;
6. non-applied bridge merge remains partial;
7. wrong expected head in merge receipt is obstructed;
8. successful merge without fresh PR/main observation remains open;
9. main advancing after merge preserves the successful merge fact;
10. missing post-merge CI requests re-observation;
11. post-merge CI failure does not auto-rollback;
12. stale-head post-merge CI is an evidence obstruction;
13. the real existing GitHub MCP write bridge mock path produces an exact merge receipt compatible with v7.31 closure.

## Next

Once a development lineage is closed, future edits should begin a new lineage rooted in the newly observed main state.

The closure receipt is historical evidence, not a reusable write license.
