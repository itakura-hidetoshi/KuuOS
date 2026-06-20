# Qi–WORLD Licensed Blocker Discharge v1.7

## Position

v1.5 blocks an unlicensed cross-cycle transition. v1.6 emits a read-only Indra
transport request and explicitly leaves analytic transport unrealized. v1.7
closes a different edge: a strictly later-cycle ActOS handoff may proceed only
when a separate external execution-authority packet, human approval, host
license, exact PlanOS binding, and single-use scope all agree.

```text
v1.5 all-active blocker certificate
→ v1.6 read-only Indra transport request
→ separate external execution authority
→ native PlanOS activation receipt
→ native ActOS step authorization
→ one licensed invocation
→ effect receipt
→ observation and verification debt
```

## Transport request and execution authority remain distinct

The v1.6 request remains:

```text
request_only = true
runtime_transport_realized = false
exact_world_updated = false
disposition = EXTERNAL_ANALYTIC_TRANSPORT_RECEIPTS_REQUIRED
```

The v1.7 execution-authority packet is not an analytic transport receipt and
cannot satisfy, forge, or bypass the v1.6 normal-star-isomorphism,
pseudofunctor, stack-descent, branch-transport, coherence, history-phase, or
continuum non-Markov receipt requirements.

## Partial discharge, not blocker deletion

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

The v1.5 source blocker vector remains all-active as historical proof. v1.7
emits a separate discharge certificate describing one narrowly licensed
transition.

## Required bindings

The external authority packet binds:

- the v1.5 blocker receipt and certificate digests carried by v1.6;
- the source PlanOS state, basis, and committed-plan digests;
- host-license digest;
- human-approval receipt and approver;
- exact operation and selected step;
- one invocation and one effectful step;
- issue and expiry times.

The same external-authority digest is inserted into native ActOS
`step_authorization.act_phase_receipt_digest`. A packet that is merely attached
but not bound into ActOS is rejected.

## Single-use consumption

```text
single_use = true
maximum_invocations = 1
maximum_effectful_steps = 1
release_consumption_count = 1
```

Replay, scope widening, additional blocker release, Indra request substitution,
transport-realization forgery, human-approval substitution, and authority
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
source_cycle_immutable = true
source_blocker_certificate_immutable = true
indra_transport_still_unrealized = true
memory_overwritten = false
exact_world_updated = false
truth_promoted = false
same_cycle_recursive_invocation = false
multi_world_collapsed = false
```

## Boundary

```text
blocker discharge ≠ blocker deletion
Indra transport request ≠ execution authority
external execution authority ≠ analytic transport receipt
Plan activation ≠ execution authority
host license ≠ truth authority
one licensed ActOS invocation ≠ automatic continuation
recorded effect → observation debt → verification debt
```
