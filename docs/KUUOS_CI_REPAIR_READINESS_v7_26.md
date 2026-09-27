# KuuOS CI Repair Readiness v7.26

## Purpose

v7.25 can identify a Lean CI failure and select the right MCP planes.

v7.26 decides whether the current local workspace is actually ready for repair.

The key distinction is:

```text
CI failure observed
!=
current workspace ready to edit
```

A repair becomes locally ready only when the full target file has been observed and Lean-LSP semantics are fresh for those exact bytes.

## Three readiness levels

### Analysis ready

`analysis_ready` requires:

- the CI exact head still matches the fresh remote head;
- the full target file currently exists;
- Filesystem and Lean-LSP content digests agree;
- Lean semantics are fresh;
- the v7.19 federation allows local semantic work.

### Local repair ready

`local_repair_ready` adds workspace write authority.

If workspace authority is missing, the candidate is retained and the status is partial. It is not rejected.

### Remote publish ready

`remote_publish_ready` is stricter. It additionally requires an aligned committed workspace, remote/local revision alignment, remote-mutation eligibility, and separate GitHub write authority.

Thus:

```text
local repair ready
does not imply
remote publish ready
```

## Dirty worktree

A dirty but semantically fresh target file remains valid for local repair.

That is the normal development state after an edit:

```text
Filesystem bytes changed
-> Lean-LSP re-observed those exact bytes
-> local repair may continue
-> Git diff reviewed later
```

## Remote/local divergence

If the local Git head differs from the remote head, v7.26 does not globally block repair.

If the current bytes and Lean semantics are fresh, local repair can continue. Remote publish remains unavailable until revision reconciliation.

## Stale CI head

If the CI failure belongs to an older remote head than the current federation observation, v7.26 does not auto-patch the current workspace.

It returns:

`reobserve_ci_on_current_remote_head`

This preserves exact-head meaning.

## Stale Lean semantics

If the file changed after Lean-LSP observed it, the repair candidate is held at:

`reobserve_lean_semantics_on_current_bytes`

The current edit is not discarded.

## Full-file scope

The repair evidence always records:

```text
repair_scope = entire_target_file
ci_error_line_is_locator_not_scope = true
full_target_file_audit_required = true
```

The readiness layer stores digests and bindings, not raw file contents or raw CI logs.

## Authority

Workspace authority and GitHub authority remain distinct.

Workspace write authority permits local edit candidates. It does not grant remote GitHub mutation authority.

Likewise, Lean semantic freshness does not itself authorize Git operations.

## Validation

Focused tests verify aligned fresh readiness, dirty fresh local repair, remote/local divergence, stale Lean semantics, stale CI heads, missing workspace authority, target-binding obstruction, and non-Lean routes.

The central law is:

> **Repair the full current file only after its bytes and semantic state are fresh; reconcile remote publication separately.**
