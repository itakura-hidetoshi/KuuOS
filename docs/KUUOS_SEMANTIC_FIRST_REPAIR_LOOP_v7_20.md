# KuuOS Semantic-First Repair Loop v7.20

## Purpose

v7.19 established four distinct development surfaces:

```text
GitHub remote
local Git
Filesystem current bytes
Lean-LSP semantic state
```

v7.20 turns those observations into a bounded repair loop while reusing the existing CodeAI candidate and repair contracts.

The loop is:

```text
current filesystem bytes
-> fresh Lean diagnostics / goal state
-> repair candidate proposal
-> CodeAI static preflight
-> shadow Lean re-observation
-> local application candidate
-> current-byte Lean re-observation
-> Git diff review
-> remote/local revision reconciliation
-> remote submission candidate
-> separate existing GitHub authority
```

v7.20 itself applies no patch and performs no Git or GitHub mutation.

## Semantic evidence is byte-bound

A Lean observation is accepted only when:

```text
Lean source_content_digest
=
Filesystem current_content_digest
```

If the file changes after the Lean observation, v7.20 returns:

```text
lean_semantic_reobservation_required
```

The local edit is preserved.

This follows v7.19:

```text
stale semantics -> reobserve
not
stale semantics -> discard worktree
```

## Candidate provenance and current bytes remain separate

The existing CodeAI Candidate Patch receipt proves proposal provenance and policy admission.

It does not prove that the candidate is based on the current dirty working bytes.

v7.20 therefore requires an additional:

```text
before_content_digest
```

and later:

```text
result_content_digest
```

This preserves:

```text
CodeAI candidate receipt
!=
current-byte binding
```

The candidate may be relevant when the current workspace contains either the candidate's source bytes or its result bytes. Any third state is stale and requires reconciliation rather than silent application.

## Existing CodeAI contracts are reused

v7.20 consumes rather than replaces:

- Candidate Patch Envelope v0.1;
- Typed Structured Edit IR v0.1;
- Candidate Static Admissibility Preflight v0.1;
- Verification-Guided Candidate Repair and Regeneration v0.1;
- Bounded Repair Cycle Orchestration v0.1.

Candidate Patch and Static Preflight receipt digests are rechecked canonically.

Their effect and authority fields must remain false.

Thus:

```text
candidate != selected
candidate != applied
static preflight != correctness proof
repair feedback != authority
```

remain intact.

## No candidate yet

If the current Lean observation is fresh and has errors but no candidate is bound:

```text
repair_candidate_generation_ready
```

This means the existing CodeAI generation path may be invoked.

It does not mean a model must be called or that any proposed edit is correct.

## Static preflight

A supported Candidate Patch receipt without Static Preflight evidence becomes:

```text
candidate_static_preflight_ready
```

Static Preflight outcomes stay distinct:

```text
REPAIRABLE -> candidate_repair_feedback_ready
HOLD       -> candidate_hold_preserved
REJECT     -> candidate_rejected_preserved
ADMISSIBLE -> shadow semantic evaluation
```

Hold and reject are not collapsed into generic failure.

## Shadow Lean semantics

An admissible candidate must have a fresh Lean observation bound to:

```text
candidate result_content_digest
```

before v7.20 compares it with the source diagnostic state.

A lower error count is recorded as semantic improvement.

A higher error count is:

```text
candidate_semantic_regression
```

An equal nonzero error count is:

```text
candidate_no_semantic_improvement
```

These are diagnostic facts, not correctness judgments.

## Semantic improvement does not write

Even a candidate that removes all current Lean errors becomes only:

```text
local_application_candidate
```

v7.20 fixes:

```text
semantic_improvement_grants_local_write_authority = false
semantic_improvement_grants_remote_write_authority = false
```

Local application remains a separate governed workspace effect.

## After local application

When v7.19 re-observes the candidate result as the current Filesystem bytes and Lean-LSP confirms fresh semantics, v7.20 advances to:

```text
git_diff_review_ready
```

The shadow semantic result does not substitute for re-observing the actual current bytes.

## Git admission and remote reconciliation

A reviewed diff may still need local Git admission, for example for a new untracked file:

```text
local_git_admission_required
```

A local revision that no longer matches the remote GitHub head becomes:

```text
remote_revision_reconciliation_required
```

but local semantic repair may continue.

Only after:

```text
fresh current semantics
+
reviewed Git diff
+
local Git eligibility
+
remote/local revision alignment
```

does v7.20 emit:

```text
remote_submission_candidate
```

That is still not GitHub write authority.

## Why this changes the Lean workflow

The old practical loop often looked like:

```text
edit
-> push
-> CI RED
-> inspect Lean error
-> repair
```

With v7.17-v7.20, the intended loop becomes:

```text
edit
-> Lean-LSP diagnostics / goal
-> bounded candidate
-> static preflight
-> shadow Lean check
-> local application
-> Lean-LSP reobserve
-> Git diff review
-> push / PR under existing authority
-> exact-head CI
```

CI remains the final repository-head receipt. Semantic feedback simply moves earlier.

## Validation

The focused checker verifies:

1. fresh errors without a candidate route to generation;
2. stale Lean diagnostics route to re-observation;
3. candidate receipts without preflight route to Static Preflight;
4. repairable preflight routes into the existing repair path;
5. hold and reject remain distinct;
6. an admissible candidate with fewer Lean errors becomes only a local application candidate;
7. regression and no-improvement are typed separately;
8. an applied candidate requires Git diff review;
9. remote revision divergence requires reconciliation but does not block local semantic work;
10. reviewed/aligned candidates become remote submission candidates without authority;
11. untracked/unadmitted candidates require local Git admission;
12. corrupt CodeAI lineage is obstructed;
13. a clean zero-error workspace needs no semantic repair.

The central law is:

> **Semantic evidence may guide repair earlier and more precisely, but every observation remains bound to the bytes that produced it and every mutation keeps its own authority boundary.**
