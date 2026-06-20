# Qi–WORLD Licensed Blocker Discharge v1.6

## Purpose

v1.5 proves that an unlicensed cross-cycle transition is blocked. v1.6 closes
the complementary path: a strictly later-cycle ActOS handoff may proceed only
when an external authority packet, human approval, host license, exact PlanOS
binding, and single-use scope all agree.

The source blocker certificate is never deleted or rewritten.

```text
v1.5 all-active blocker certificate
→ external authority packet
→ native PlanOS activation receipt
→ native ActOS step authorization
→ licensed single invocation
→ effect receipt
→ observation and verification debt
```

## Partial discharge, not global removal

Only two blockers are releasable for the target cycle:

```text
present_activation_blocker
execution_authority_blocker
```

The following remain invariant:

```text
memory_overwrite_blocker
world_identity_blocker
truth_authority_blocker
same_cycle_self_loop_blocker
multi_world_collapse_blocker
```

The v1.5 source vector remains all-active as historical proof. v1.6 emits a
separate discharge certificate describing the narrowly licensed transition.

## Required bindings

The external authority packet binds:

- source blocker receipt and certificate digests;
- source PlanOS state, basis, and committed-plan digests;
- host-license digest;
- human-approval receipt and approver;
- exact operation and selected step;
- one invocation and one effectful step;
- issue and expiry times.

The same external-authority digest is inserted into the native ActOS step
authorization as its `act_phase_receipt_digest`. The validator rejects a packet
that is merely attached but not bound into ActOS.

## Single-use consumption

```text
single_use = true
maximum_invocations = 1
maximum_effectful_steps = 1
release_consumption_count = 1
```

Replay, scope widening, additional blocker release, and authorization
substitution are rejected.

## Evidence debt

A successful target-cycle effect does not close the loop:

```text
effect_recorded = true
observation_required = true
verification_required = true
automatic_truth_promotion = false
automatic_plan_completion = false
automatic_rollback = false
```

The result must return through ObserveOS and VerifyOS.

## Fixed invariants

```text
memory_overwritten = false
exact_world_updated = false
truth_promoted = false
same_cycle_recursive_invocation = false
multi_world_collapsed = false
source_cycle_immutable = true
source_blocker_certificate_immutable = true
```

## Boundary

```text
blocker discharge ≠ blocker deletion
external authority ≠ self-issued authority
Plan activation ≠ execution authority
host license ≠ truth authority
one licensed ActOS invocation ≠ automatic continuation
recorded effect → observation debt → verification debt
```
