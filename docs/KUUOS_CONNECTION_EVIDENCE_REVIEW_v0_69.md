# KuuOS External Post-Shadow Evidence Review v0.69

## Purpose

v0.69 reviews the exact v0.68 evidence capsule under an externally bound reviewer identity, reviewer class, digest chain, and finite validity window.

The review decision and application authority are not separated.

`APPROVE_EVIDENCE` carries application authority.

`REJECT_EVIDENCE` and `REQUEST_MORE_EVIDENCE` do not.

## Flow

```text
v0.68 evidence capsule
  -> external review request
  -> reviewer identity and class binding
  -> exact request, capsule, source, rollback, and candidate bindings
  -> finite validity window
  -> explicit decision
  -> immutable review record
```

## Decision semantics

```text
APPROVE_EVIDENCE
  <-> production_apply_allowed = true

REJECT_EVIDENCE
  -> production_apply_allowed = false

REQUEST_MORE_EVIDENCE
  -> production_apply_allowed = false
```

A decision and permission mismatch is rejected fail closed.

## Execution record

Application authority does not assert that the review function already performed an application.

The review record independently states whether a live effect or state write occurred.

At v0.69 review construction:

```text
live_effect_performed = false
state_write_performed = false
authority_widened = false
rollback_target_replaced = false
```

A later governed executor may consume an approved record without requiring a second, conceptually separate grant of production authority.

## Exact bindings

The request and attestation bind:

- evidence capsule digest
- source bundle digest
- rollback bundle digest
- candidate connection digest
- reviewer identity
- reviewer class
- exact review scope
- finite validity window
- explicit decision
- application authority flag

The rollback digest remains identical to the source bundle digest.

## Fail-closed conditions

Review is blocked for:

- expired or not-yet-valid evidence
- invalid request, attestation, capsule, or record digest
- source, rollback, candidate, or capsule binding mismatch
- reviewer identity or class mismatch
- scope widening
- decision and permission mismatch
- unrecorded live effect or state write
- authority widening
- rollback-target replacement

Finite evidence remains validity-bounded and does not establish truth for all future contexts.

## Formal statements

The Lean surface proves:

- `valid_review_preserves_exact_chain`
- `valid_approval_iff_application_authorized`
- `valid_approval_grants_application_authority`
- `valid_application_authority_requires_approval`
- `valid_review_records_no_unperformed_effect`
