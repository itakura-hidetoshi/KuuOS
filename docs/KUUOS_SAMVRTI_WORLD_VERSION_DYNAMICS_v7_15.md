# KuuOS Samvrti World-Version Dynamics v7.15

## Purpose

v7.14 created append-only conventional world versions from verified effects.

v7.15 asks what a sequence of those versions means:

```text
W0 -> W1 -> W2 -> ...
```

The answer must not be reduced to:

```text
digest changed -> structural change
```

because every genuine world transition changes its world-state digest.

Instead, v7.15 classifies the history inside one paramartha fiber using:

- exact history composition;
- local change diagnostics;
- reversibility;
- recoverability;
- impact radius;
- repeated direction of change;
- world-binding signatures;
- structural-context signatures;
- explicit binding-revalidation evidence.

## One paramartha fiber, changing conventional world

The basic object is:

```text
Paramartha P
  |
  +-- W0
  +-- W1
  +-- W2
  +-- ...
```

Every v7.14 world version must satisfy:

```text
paramartha_before = paramartha_after = P
```

v7.15 does not infer a new paramartha class from conventional drift.

Thus:

```text
samvrti structural drift
!=
paramartha reclassification
```

## Exact history composition

For successive versions:

```text
W0 -> W1
W1 -> W2
```

the second transition must begin exactly where the first ended:

```text
second.prior_world_state_digest
=
first.observed_world_state_digest
```

If instead:

```text
W0 -> W1
OTHER -> W2
```

v7.15 records:

```text
samvrti_world_history_disconnected
```

It does not fabricate the missing transition.

This mirrors the finite-history composition emphasis in the existing dependent-origination formal spine.

## Reversible local dynamics

A continuous history is classified as:

```text
reversible_local_samvrti_dynamics
```

when:

- world binding remains stable;
- structural context remains stable;
- each transition is locally bounded;
- reversibility remains high;
- recoverability remains high;
- impact remains bounded;
- no cumulative drift signal dominates.

This is ordinary conditioned change.

It should normally flow back into context without forcing a global rebind.

## Cumulative samvrti drift

Several individually small changes can accumulate.

For example:

```text
W0 --a--> W1 --a--> W2 --a--> W3
```

may remain locally reversible at every step while exhibiting a persistent directional trend.

v7.15 records:

```text
cumulative_samvrti_drift
```

when configured operational policy detects:

- sufficient accumulated local change; or
- a sufficiently long repeated drift-axis run.

This still preserves the same paramartha fiber.

The normal response is:

```text
fresh observation
+
consider replan
```

rather than automatic action cancellation.

## Structural world drift

A stronger class appears when the conventional structure itself changes, for example:

- the world-binding signature changes;
- the structural-context signature changes;
- an explicit binding-revalidation receipt requests reconsideration.

Then v7.15 records:

```text
structural_world_drift_rebind_required
```

The consequence is deliberately scoped:

```text
recheck world-dependent bindings
```

not:

```text
block everything
```

In particular:

```text
world_independent_action_reuse_allowed = true
paramartha_reclassification_required = false
```

This continues the v7.12 principle that one unresolved world condition must not become a blanket prohibition.

## World-state digest change is not enough

A confirmed transition necessarily changes:

```text
prior_world_state_digest
->
observed_world_state_digest
```

That alone says only that the conventional world changed.

It does not say whether the change is:

- local;
- reversible;
- cumulative;
- structural.

v7.15 therefore fixes:

```text
world_digest_change_alone_is_structural_drift = false
```

## Runtime thresholds are policy, not truth

The runtime uses bounded operational diagnostics such as:

- local change score;
- reversibility;
- recoverability;
- impact;
- cumulative score;
- repeated-axis count.

These support routing and resource decisions.

They are not promoted to theorem-level semantics.

The manifest explicitly fixes:

```text
policy_thresholds_are_semantic_truth = false
```

This follows the existing formal Relational Feedback Semantics, where predicates such as high uncertainty and reversibility remain abstract rather than being identified with one arbitrary scalar threshold.

## Relation to formal feedback semantics

The formal reference is:

```text
DependentOriginationRelationalFeedbackSemanticsV0_1.lean
```

Its structural pattern is:

```text
context
-> present-state readout
-> observation
-> evidence
-> unresolved difference
-> gate
-> action
-> feedback
-> next context
```

and repeated encounters form an exact finite-history transport.

v7.15 is a runtime structural mirror on the verified-world side:

```text
verified W0
-> verified W1
-> verified W2
-> dynamics classification
-> future context/planning feedback
```

It does not claim to instantiate the formal theorem objects directly.

## Action consequences

### Reversible local dynamics

```text
binding reuse eligible
ordinary feedback update
```

### Cumulative drift

```text
binding provisionally reusable
fresh observation recommended
consider replan
```

### Structural drift

```text
world-dependent binding recheck required
world-independent action remains usable
paramartha class unchanged
```

### Disconnected history

```text
repair history or binding
do not invent missing transition
```

## Why this is dependent origination rather than a graph-drift score

A graph-drift system could compare snapshots by distance.

v7.15 instead asks whether the later world is connected to the earlier world by a valid sequence of verified conditioned transitions.

So the relevant object is not merely:

```text
distance(W0, Wn)
```

but:

```text
W0
 --effect/evidence-->
W1
 --effect/evidence-->
W2
 ...
```

with explicit reversibility, context, binding and lineage.

The path matters because the conditions that produced the world matter.

## Validation

The focused checker verifies:

1. a continuous small reversible history is local dynamics;
2. repeated same-direction small transitions become cumulative samvrti drift;
3. changed binding/context signatures become structural world drift;
4. world-state digest changes alone do not imply structural drift;
5. disconnected history is an obstruction and is never silently filled;
6. structural drift requires rechecking world-dependent bindings but does not block world-independent action;
7. runtime numeric thresholds cannot be promoted to semantic truth.

The central law is:

> **A changing conventional world remains intelligible through its verified history of conditions; structural drift changes which worldly bindings need re-evaluation, not the paramartha class by default.**
