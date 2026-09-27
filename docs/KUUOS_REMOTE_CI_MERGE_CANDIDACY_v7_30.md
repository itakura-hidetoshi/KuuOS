# KuuOS Remote CI Merge Candidacy v7.30

## Purpose

v7.29 ends after one verified local candidate has been materialized into GitHub and made reachable through a remote candidate branch.

That is still not merge candidacy.

v7.30 requires the remote collaboration and CI surfaces to agree on the exact published candidate.

The chain is:

```text
v7.29 published candidate branch
-> fresh candidate-branch head observation
-> fresh base-branch head observation
-> exact pull-request binding
-> completed CI event
-> fresh GitHub MCP CI re-observation
-> exact required workflow success
-> merge candidate
```

The final result still does not grant merge authority.

## Candidate head

The currently observed candidate branch head must equal the remote commit SHA certified by v7.29:

```text
candidate_branch_head
=
v7.29.remote_commit_sha
```

If the branch moved:

```text
remote_candidate_head_reconciliation_required
```

The published candidate is retained.

## Base head

The base branch must still equal the base re-observed at the end of v7.29.

If it moved:

```text
remote_base_reconciliation_required
```

Again, the candidate is retained rather than rejected.

This prevents stale-base merge candidacy while preserving useful repair work.

## Pull request binding

A merge candidate requires one currently observed open pull request whose:

```text
head branch = candidate branch
head SHA    = candidate head
base branch = expected base branch
base SHA    = current base head
```

No PR gives:

```text
pull_request_required
```

A mismatched PR gives:

```text
pull_request_binding_reconciliation_required
```

A draft PR remains a valid published candidate, but not yet a merge candidate:

```text
pull_request_review_state_required
```

v7.30 does not automatically change draft/review state.

## Reusing CI Completion Reentry v1.1

v7.30 does not invent another CI truth layer.

It consumes the existing:

```text
kuuos_github_ci_completion_reentry_v1_1
```

verification packet.

That layer already enforces:

```text
event observed != CI verified

event success != success evidence

fresh MCP observation
+
exact repository
+
run ID
+
workflow name
+
head SHA
+
completed jobs/required steps
=
verified CI re-entry
```

v7.30 adds the requirement that every required workflow packet binds the exact remote candidate head.

## Missing CI

If some required workflow has not yet been freshly re-observed:

```text
candidate_ci_reobservation_required
```

This is a partial state, not candidate rejection.

## Verified non-success

A completed workflow may be freshly verified and still conclude failure.

That routes to:

```text
candidate_ci_non_success_repair_reentry
```

The remote candidate remains available for diagnosis and repair.

This connects naturally back to the v7.25-v7.27 CI repair path.

## CI binding obstruction

Malformed CI evidence, stale-head CI evidence, or a CI packet that claims merge/write authority is a true evidence obstruction:

```text
candidate_ci_binding_obstruction
```

The key distinction is:

```text
CI failure
!=
CI evidence corruption
```

A real failing test is useful information.

A packet bound to the wrong head is invalid evidence.

## Merge candidacy

Only when all conditions agree does v7.30 emit:

```text
merge_candidate_ready_explicit_merge_authority_required
```

with:

```text
merge_candidate = true
merge_authority_granted = false
```

The next route is:

```text
acquire_explicit_merge_authority_then_expected_head_merge
```

## Why CI never grants merge authority

The existing CI Completion Reentry formal boundary proves that verified CI re-entry does not grant merge or write authority.

v7.30 preserves that boundary.

Therefore:

```text
all CI green
!=
merge authority
```

and:

```text
merge candidate
!=
merged
```

## Validation

The focused checker builds real v1.1 completion/re-observation packets and verifies:

1. exact PR + exact candidate/base + all fresh successful required CI forms a merge candidate;
2. candidate-head movement retains the candidate for reconciliation;
3. base movement retains the candidate for reconciliation;
4. missing PR retains the published candidate;
5. PR-head mismatch requests PR rebinding;
6. draft PR is not rejected but is not merge-candidate ready;
7. missing required CI requests re-observation;
8. verified CI failure routes back to repair without discarding the remote candidate;
9. stale-head CI is a true evidence binding obstruction;
10. CI evidence can never grant merge authority.

## Next

The next layer may consume `merge_candidate=true` together with an independently supplied merge authority, invoke the existing expected-head GitHub merge path, and require a fresh post-merge main-head/CI observation before declaring the development lineage closed.
