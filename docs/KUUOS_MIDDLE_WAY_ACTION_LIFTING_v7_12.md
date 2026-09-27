# KuuOS Middle-Way Action Lifting v7.12

## Purpose

v7.12 connects the Two Truths non-collapse layer to action without introducing a new blanket-blocking rule.

The naive version would say:

```text
paramartha-only basis -> block
world mismatch -> block
direct execution request -> block
```

v7.12 explicitly rejects that design.

These facts are not sufficient reasons to reject an action.

Instead, the action is evaluated through the concrete conditions that make an effect appropriate:

- samvrti dependence;
- cross-world invariance;
- transfer evidence;
- fresh lower execution authority;
- evidence completeness;
- reversibility;
- recoverability;
- impact radius;
- risk;
- compensation mode;
- required human review.

## Request is not authority — but request is not a fault

A direct-execution request is a legitimate candidate signal.

```text
direct_execution_requested = true
```

does not create authority, but it also does not count as a rejection reason.

The runtime therefore fixes both:

```text
request != authority
request != prohibition
```

If a fresh ActOS/capability authority is already supplied and the other conditions hold, the direct request can become:

```text
licensed_execution_candidate_...
```

If authority is absent, the action remains alive as:

```text
fresh_authority_required
```

rather than becoming semantically rejected.

## Paramartha-only actions

A missing or held samvrti binding is not by itself a reason to reject an action.

Some actions are genuinely independent of the local world presentation.

For example, a bounded read-only metadata operation may have:

```text
world_dependence = none
```

If fresh lower authority covers the world-independent effect surface, v7.12 permits:

```text
licensed_execution_candidate_world_independent
```

Thus:

```text
paramartha-only
!=
automatically non-actionable
```

The important question is whether the action actually depends on a samvrti distinction.

## Exact-world execution

When:

```text
target world = bound samvrti world
fresh authority covers action + world
required evidence is present
risk/reversibility/recoverability/impact are admissible
```

the route is:

```text
licensed_execution_candidate_exact_world
```

This runtime only assesses eligibility. It does not execute the effect itself.

## Cross-world lifting

A world mismatch is a structured condition, not a failure bit.

Suppose:

```text
source world = A
target world = B
```

The action may still lift if either:

1. an explicit transfer witness certifies the cross-world transport; or
2. the action itself is invariant across the relevant samvrti presentations.

With fresh authority covering the target world, the route becomes:

```text
licensed_execution_candidate_transferred_world
```

This preserves the v7.11 distinction between worlds while still allowing justified action transport.

## Bounded probe instead of forced hold

Some world mismatches cannot yet be certified.

If the proposed effect is:

- low risk;
- low impact;
- highly reversible;
- highly recoverable;
- separately probe-authorized;

v7.12 can route it as:

```text
bounded_probe_candidate
```

The purpose of the probe is not to pretend the worlds are equal.

It is to gather effect-grounded evidence under a bounded, recoverable action so that the world binding can be resolved empirically.

This implements a middle path between:

```text
execute as if worlds were identical
```

and:

```text
refuse all action until perfect world identity is known
```

## Concrete reasons replace blanket blocking

v7.12 holds or replans only for specific operational reasons, such as:

- execution risk above the configured ceiling;
- insufficient reversibility;
- insufficient recoverability;
- excessive impact radius;
- high-impact noncompensable effect;
- explicit human-review requirement;
- missing required evidence;
- expired or revoked lower authority.

A direct execution request does not appear in that list.

A world mismatch does not appear in that list by itself.

A paramartha-only basis does not appear in that list by itself.

## Relationship to DecisionOS

The existing DecisionOS already reasons over:

- estimated risk;
- recoverability;
- reversibility;
- evidence;
- human review;
- external license requirement;
- experiment information gain;
- middle-way repairability.

v7.12 does not replace those dimensions.

It adds a two-truths-aware lifting layer that determines how an action candidate relates to:

```text
paramartha meaning
samvrti world
target world
cross-world transport
fresh effect authority
```

## Relationship to ActOS and transactional effects

KuuOS v0.24 already uses the sequence:

```text
bounded plan proposal
-> exact ActOS authorization
-> prepare
-> licensed host invocation
-> canonical effect receipt
-> independent world observation
-> reconciliation
-> verification
```

v7.12 preserves that architecture.

A v7.12 execution candidate means:

> the semantic/two-truths/action conditions are sufficient to present this action to the lower authorized effect path.

It does not mean that v7.12 itself has executed anything.

After a real effect, ObserveOS and VerifyOS remain necessary because:

```text
licensed execution
!= confirmed intended world state
!= mission success
```

## Route summary

### Exact world

```text
licensed_execution_candidate_exact_world
```

### Certified/invariant transfer

```text
licensed_execution_candidate_transferred_world
```

### World-independent action

```text
licensed_execution_candidate_world_independent
```

### Mismatch with safe exploratory path

```text
bounded_probe_candidate
```

### Missing authority

```text
fresh_authority_required
```

The action is retained.

### Stale authority

```text
authority_renewal_or_replan_required
```

The old authority is not silently reused.

### Concrete operational insufficiency

```text
review_or_replan_required
```

with typed reasons.

## Why this is a KuuOS middle-way layer

The two failure modes are:

### Over-permissive collapse

```text
same paramartha
-> ignore world
-> execute anywhere
```

### Over-restrictive collapse

```text
world not exactly bound
-> reject every action
```

v7.12 does neither.

Instead:

```text
semantic basis
+
samvrti dependence
+
world transport
+
authority
+
evidence
+
effect properties
->
contextual action route
```

This is closer to dependent origination than a binary gate.

## Validation

The focused checker verifies:

1. a direct execution request in its exact world becomes a licensed execution candidate;
2. a certified cross-world transfer can become a licensed execution candidate;
3. an unresolved world mismatch can become a bounded reversible probe;
4. a paramartha-only but genuinely world-independent action can become executable;
5. a direct execution request without authority becomes `fresh_authority_required`, not rejection;
6. a high-impact irreversible action is replanned for concrete risk reasons, not because it requested execution;
7. an action-invariance witness can support cross-world lifting.

The central law is:

> **Action is neither authorized nor forbidden by one semantic flag. It emerges from the conjunction of world relevance, transferability, authority, evidence, reversibility, recoverability and impact.**
