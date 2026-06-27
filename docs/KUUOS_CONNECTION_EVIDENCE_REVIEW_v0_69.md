# KuuOS External Post-Shadow Evidence Review v0.69

## Purpose

v0.69 performs an external, validity-bounded review of the exact v0.68 evidence capsule.

The review operation does not itself mutate the source bundle, committed OS state, ledger, or MemoryOS capsule.

## Flow

```text
v0.68 evidence capsule
  -> external review request
  -> assigned reviewer identity and class
  -> exact capsule, source, rollback, and candidate bindings
  -> finite review validity window
  -> explicit decision
  -> immutable external review record
```

## Decisions

The only decisions are:

- `APPROVE_EVIDENCE`
- `REJECT_EVIDENCE`
- `REQUEST_MORE_EVIDENCE`

`APPROVE_EVIDENCE` binds `production_apply_allowed = true` in the reviewer attestation.

`REJECT_EVIDENCE` and `REQUEST_MORE_EVIDENCE` bind `production_apply_allowed = false`.

The permission is therefore not separated from the approval decision.

The review operation still records no live effect or state write; permission and execution are independently auditable.

## Exact bindings

The review request binds:

- evidence capsule digest
- source bundle digest
- rollback bundle digest
- candidate connection digest
- assigned reviewer identity
- assigned reviewer class
- exact review scope

The reviewer attestation binds the same digest chain and the request digest.

The immutable review record binds the request, attestation, decision, reviewer, capsule, source, rollback target, and candidate.

## Fail-closed conditions

Review is blocked when any of the following occurs:

- evidence is expired or not yet valid
- capsule self-digest is invalid
- source or rollback binding differs
- reviewer identity or class differs
- attestation scope is widened
- validity window exceeds the capsule window
- the decision and production permission disagree
- state write is requested
- authority widening is requested
- rollback replacement is requested

## Recorded execution boundary

Every generated review record has:

```text
review_only = true
live_effect_allowed = false
state_write_performed = false
authority_widened = false
rollback_target_replaced = false
```

These fields describe what the review operation performed, not whether an approved attestation carries production permission.

## Formal statements

The Lean surface proves:

- `valid_review_preserves_evidence_chain`
- `valid_review_remains_review_only`
- `valid_approval_is_candidate_only`

The current formal surface preserves the v0.68 evidence chain and the non-write property of the review operation. It does not claim that finite evidence establishes truth for all future contexts.
