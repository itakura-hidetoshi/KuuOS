# KuuOS Action–Effect Lineage Binding v7.13

## Purpose

v7.12 answered:

> Under which semantic, world, authority and effect conditions is an action eligible to be presented to the lower effect machinery?

v7.13 answers the next question:

> Did that exact semantic action become the exact ActOS-authorized operation, and what happened after the real effect path ran?

The layer binds one lineage across:

```text
semantic action candidate
  -> exact ActOS prepared state
  -> step authorization
  -> capability lease
  -> host projection
  -> transaction intent
  -> lower effect receipt
  -> ObserveOS evidence
  -> world reconciliation
  -> VerifyOS adjudication
  -> transaction final receipt
```

It performs no effect itself.

## Why this layer is necessary

A v7.12 route such as:

```text
licensed_execution_candidate_exact_world
```

means that the semantic and operational preconditions are sufficient for lower execution consideration.

It is not execution authority.

Likewise:

```text
fresh_authority_required
```

is not a permanent rejection.

Fresh ActOS authority may arrive later.

v7.13 therefore preserves the old semantic assessment and allows the lineage to evolve when new lower artifacts appear.

## Dynamic resolution

Suppose v7.12 recorded:

```text
fresh_authority_required
```

At time t1 the action has no lower authority.

At time t2 a valid ActOS state exists with:

- exact selected step;
- exact operation;
- fresh single-use authorization;
- valid host capability lease;
- valid host projection.

v7.13 can then record:

```text
authorized_prepared
```

without rewriting the historical v7.12 route.

This is important:

```text
historical semantic assessment
!=
eternal status
```

New conditions can change what is currently possible.

The same rule applies to world mismatch.

A prior:

```text
world_transfer_or_reconciliation_required
```

may later advance when a new world-transfer resolution witness is supplied.

## Exact lower binding

v7.13 validates the actual existing ActOS state using:

```text
validate_act_state
```

and binds:

```text
act_state_digest
step_authorization_digest
host_license_digest
host_projection_digest
operation_id
operation_input_digest
```

The layer does not accept those identifiers merely because they are present.

They must belong to a valid existing ActOS state.

## Semantic-to-lower effect binding

The bridge computes one digest over both semantic and lower identities:

```text
semantic_effect_binding_digest
```

It includes:

- action ID and action digest;
- semantic subject;
- paramartha carrier;
- target samvrti world;
- world relation;
- world-binding evidence;
- any new world-transfer resolution witness;
- mapped lower operation;
- operation input digest;
- intended effect digest;
- ActOS state;
- step authorization;
- capability lease;
- host projection;
- transaction intent.

Thus the lower operation cannot silently detach from the semantic action that justified it.

## World binding

ActOS and the host adapter are lower effect machinery.

They do not by themselves encode the full v7.11 samvrti semantics.

Therefore v7.13 keeps an explicit:

```text
world_binding_evidence_digest
```

for world-dependent actions.

This is provenance, not authority.

It records which evidence binds the semantic target world to the concrete lower host projection.

## Transaction binding

When a v0.24 transaction state is supplied, v7.13 validates it using:

```text
validate_transaction_state
```

and binds the action to:

```text
transaction_intent_digest
transaction_state_digest
transaction_final_receipt_digest
```

The transaction intent must agree with the mapped operation, operation input, intended effect, ActOS authorization, capability lease and host projection.

Any exact mismatch becomes:

```text
binding_obstructed
```

This is a true obstruction because the action and lower effect lineage no longer refer to the same operation.

## Effect-confirmed meaning

A lower host invocation receipt alone is not enough.

v7.13 accepts:

```text
effect_confirmed
```

only from a committed v0.24 transaction whose route is:

```text
EFFECT_CONFIRMED
```

The underlying v0.24 transaction already requires:

```text
ActOS effect record
+
ObserveOS world evidence
+
world-effect reconciliation
+
VerifyOS verification
```

Therefore the action lineage can distinguish:

```text
authorized to try
executed lower invocation
observed world effect
verified effect
committed effect-confirmed transaction
```

instead of collapsing them.

## Non-confirmed real outcomes

Real action does not always end in confirmation.

v7.13 preserves the existing v0.24 outcomes:

```text
REOBSERVATION_REQUIRED
-> reobservation_required

COMPENSATION_PROPOSED
-> compensation_proposed

HANDOVER_REQUIRED
-> handover_required

NO_EFFECT_RECORDED
-> no_effect_recorded
```

These are not converted into generic failure.

Each means something different in the dependent-origination lineage.

## Compensation

A compensation proposal is not an automatic rollback.

The existing v0.24 boundary requires a new:

```text
PlanOS
-> DecisionOS
-> ActOS authorization
-> capability lease
-> transaction
```

for compensation.

v7.13 preserves that distinction.

## Mission success remains separate

Even:

```text
effect_confirmed
```

does not imply:

```text
mission_success
```

The confirmed effect is one world-state fact in a larger mission lineage.

Outcome verification at the mission level remains separate.

## Relation to the previous layers

The chain is now:

```text
presentation independence
-> invariant carrier
-> carrier-model independence
-> invariant-choice independence
-> Two Truths non-collapse
-> middle-way action lifting
-> exact action/effect lineage binding
```

The key new point is that semantic meaning now connects to real effect evidence without becoming effect authority itself.

## Validation

The focused checker uses the repository's existing v0.24 runtime fixtures, not only synthetic dictionaries.

It verifies:

1. a real prepared ActOS project state binds to a v7.12 action;
2. a prior `fresh_authority_required` action advances when real ActOS authority arrives;
3. absence of authority remains `awaiting_lower_authority`, not rejection;
4. a real committed confirmed transaction refines the lineage to `effect_confirmed`;
5. real reobservation and compensation transactions preserve their typed outcomes;
6. an operation mapping mismatch is detected as a true binding obstruction.

The central law is:

> **Semantic eligibility, execution authority, lower execution, observed world effect, verified effect and mission success are distinct stages of one lineage, not interchangeable labels.**
