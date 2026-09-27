# KuuOS Bounded Lean Repair Loop v7.27

## Purpose

v7.26 says when a Lean repair is locally ready to begin.

v7.27 validates what happens after an authorized local edit.

The loop is evidence-oriented:

```text
repair-ready preimage
-> local edit
-> full-file audit
-> Filesystem re-observation
-> Lean-LSP re-observation
-> Git diff re-observation
-> Git admission candidate
```

The layer does not perform the edit and does not publish remotely.

## Exact preimage

The edit must begin from the bytes that v7.26 declared repair-ready.

```text
pre_edit_content_digest
=
v7.26 filesystem_content_digest
```

If not, the repair lineage is no longer exact and must be re-established from current bytes.

## Full-file audit

The original CI line remains only a locator.

Every repair iteration carries a digest proving that the entire target Lean file was audited.

```text
repair_scope = entire_target_file
ci_error_line_is_locator_not_scope = true
```

## Post-edit semantic freshness

After an edit:

```text
post_edit_content_digest
=
Lean-LSP source_content_digest
```

must hold before Lean diagnostics can be used to judge the repair.

If the file changed after the Lean observation, the candidate is retained and routed to semantic re-observation.

## Lean errors may remain

Remaining errors are not automatic rejection.

If the iteration budget remains:

`post_edit_lean_errors_remain`

routes back to the current post-edit bytes for another bounded repair iteration.

If the operational iteration bound is reached:

`bounded_repair_budget_reached`

the candidate is still retained. A later explicit continuation or replan is required.

The budget is runtime policy, not semantic truth.

## Git diff freshness

Error-free Lean semantics are not enough.

Git must re-observe a diff whose target post-content digest equals the same post-edit Filesystem/Lean digest.

Only then can the state become:

`repair_locally_verified_git_admission_ready`

## Supporting file changes

A full-file audit may reveal that a supporting file also needs change.

Supporting changed paths are therefore not a blanket failure. They are recorded and must be reviewed before Git admission.

## No-op edits

If an edit receipt exists but the target bytes did not actually change, the state is:

`no_effective_edit_observed`

The candidate is retained rather than falsely claiming repair progress.

## Remote publication

v7.27 never sets remote publish ready.

```text
git_admission_ready
!=
remote_publish_ready
```

A later stage must bind local Git admission/commit plus post-commit Filesystem, Lean, and Git coherence before GitHub publication can be considered.

## Relation to CodeAI

KuuOS already contains CodeAI bounded repair orchestration. v7.27 does not replace that generator/verification machinery.

It provides a development-MCP evidence boundary around the actual current repository bytes, Lean semantic observation, and Git diff.

## Validation

Focused tests verify successful local repair, remaining Lean errors, budget exhaustion, stale semantics, stale Git diff, preimage mismatch, supporting-file changes, no-op edits, and not-yet-ready repair candidates.

The central law is:

> **A repair is locally verified only when the whole target file has been audited and Filesystem, Lean-LSP, and Git diff all refer to the same post-edit bytes.**
