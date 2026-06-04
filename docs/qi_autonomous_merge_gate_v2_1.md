# Qi Autonomous Merge Gate v2.1

This document defines the merge gate for autonomous KuuOS changes.

## Goal

Allow a Qi-driven actuator to carry a change from proposal to merge only when all merge gates are satisfied.

## Required gates

```text
explicit_automerge_license = true
allowed_repository = true
allowed_base_branch = true
pull_request_created = true
pull_request_not_draft = true
head_sha_pinned = true
mergeable = true
required_checks_success = true
no_unresolved_blockers = true
receipt_written = true
audit_written = true
```

## Forbidden conditions

```text
force_push_required
unchecked_head_sha
failing_checks
pending_required_checks
draft_pull_request
unknown_base_branch
unbounded_repository_scope
missing_receipt
missing_audit
```

## Merge method

The default merge method is repository default merge. A caller may specify `merge`, `squash`, or `rebase` only when the repository allows it.

## Receipt fields

```text
merge_gate_packet_id
repository_full_name
pull_request_number
base_branch
head_branch
head_sha
mergeable
checks_summary
merge_method
merged
merge_commit_sha
gate_reasons
created_at_epoch
```

## Semantics

The autonomous merge gate is not an authority bypass. It is an execution gate that can merge only a bounded pull request with pinned head SHA and successful checks.

## Position

```text
Qi objective / PT
  -> actuator change
  -> pull request
  -> CI checks
  -> autonomous merge gate
  -> merge receipt
  -> audit log
```
