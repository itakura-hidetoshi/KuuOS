# KuuOS Samvrti World Effect Update v7.14

## Purpose

v7.13 connected semantic action to the real ActOS and transactional effect lineage.

v7.14 closes the return path.

The question is now:

> When a real external effect has been independently observed and verified, how should KuuOS reflect that change back into the conventional world without reifying it or changing the paramartha class?

The answer is:

```text
verified confirmed effect
  -> append-only samvrti world transition
```

not:

```text
verified effect
  -> new ultimate truth
```

and not:

```text
verified effect
  -> mission success
```

## Effect return path

The full cycle now becomes:

```text
presentation
-> invariant
-> paramartha carrier
-> samvrti distinction
-> action candidate
-> ActOS authority
-> external effect
-> ObserveOS evidence
-> reconciliation
-> VerifyOS
-> action-effect lineage
-> samvrti world update
```

The final arrow returns a verified conventional effect to the conventional world layer.

It does not climb back into a stronger metaphysical authority.

## Confirmed world transition

A samvrti world version is materialized only when the real v0.24 transaction is committed with:

```text
route = EFFECT_CONFIRMED
reconciliation_verdict = EFFECT_CONFIRMED
verification_route = VERIFICATION_PASSED
```

The transition uses the existing reconciliation receipt:

```text
prior_world_state_digest
observed_world_state_digest
observed_effect_digest
independent_world_evidence_digests
reconciliation_receipt_digest
```

The resulting runtime record contains:

```text
samvrti_world_version_id
samvrti_world_transition_digest
prior_world_state_digest
observed_world_state_digest
observed_effect_digest
```

This is an observed conventional world version.

## Paramartha remains unchanged

The v7.14 transition explicitly records:

```text
paramartha_carrier_element_id_before
paramartha_carrier_element_id_after
paramartha_class_changed = false
```

and requires:

```text
before = after
```

A change in the conventional world therefore does not by itself imply a change in the presentation-independent paramartha carrier.

This is exactly the two-truths non-collapse direction:

```text
samvrti can change
while
paramartha equivalence remains stable
```

## World update is append-only

The prior world state is never overwritten.

The transition records:

```text
prior world
  -> observed world
```

with both digests retained.

Therefore:

```text
world_update_overwrites_history = false
samvrti_world_versions_are_append_only = true
```

A conventional world can evolve without pretending that its prior state never existed.

## Reobservation is not a world update

When the transaction route is:

```text
REOBSERVATION_REQUIRED
```

v7.14 does not choose a new world state.

It records:

```text
samvrti_reobservation_open
```

with a residue digest.

No samvrti world version is materialized.

This preserves:

```text
uncertain world transition
!=
confirmed world transition
```

## Compensation is not rollback

When the route is:

```text
COMPENSATION_PROPOSED
```

the state becomes:

```text
samvrti_compensation_open
```

No prior world state is restored automatically.

The existing v0.24 architecture requires compensation to become a new:

```text
PlanOS
-> DecisionOS
-> ActOS
-> transaction
```

lineage.

Thus:

```text
compensation proposal
!=
world rollback
```

## Handover

When the route is:

```text
HANDOVER_REQUIRED
```

v7.14 records:

```text
samvrti_handover_open
```

Again, no world version is fabricated merely to close the state machine.

## No effect

When:

```text
NO_EFFECT_RECORDED
```

the runtime records:

```text
samvrti_no_effect
```

and materializes no world transition.

This distinguishes:

```text
no external effect occurred
```

from:

```text
an effect occurred but was unsuccessful
```

and from:

```text
the effect occurred but its resulting world state remains uncertain
```

## Effect confirmation is not mission success

The transition explicitly carries:

```text
mission_success = undetermined
mission_success_implied = false
```

A successfully confirmed local effect may still:

- fail to satisfy the mission;
- be only one intermediate step;
- produce an unexpected long-horizon outcome;
- require additional observation;
- alter future planning.

Thus:

```text
effect confirmed
!=
mission success
```

remains invariant.

## Reconciliation is not truth

The observed world version is a conventional operational record.

It is supported by independent observation and verification, but it is not promoted to ultimate truth.

v7.14 fixes:

```text
reconciliation_is_truth = false
world_transition_is_ultimate_truth = false
```

The conventional world is usable precisely because it remains explicit about its conditions and evidence.

## Why this matters for dependent origination

The earlier layers mostly moved from many presentations toward invariant meaning.

v7.14 adds the reverse direction:

```text
invariant meaning
-> conditioned action
-> observed effect
-> changed conventional world
```

So KuuOS is no longer only a quotient/descent architecture.

It now contains a feedback loop:

```text
world
-> presentation
-> invariant
-> action
-> effect
-> world'
```

while retaining:

```text
paramartha(world) = paramartha(world')
```

when the deeper invariant has not changed.

This is much closer to dependent origination than a static graph representation.

## Validation

The focused checker uses the actual v0.24 transaction fixtures and verifies:

1. a real `EFFECT_CONFIRMED` transaction creates exactly one append-only samvrti world version;
2. prior and observed world-state digests are copied exactly from the real reconciliation receipt;
3. the paramartha carrier is identical before and after the samvrti transition;
4. mission success remains undetermined;
5. `REOBSERVATION_REQUIRED` creates a residue but no world version;
6. `COMPENSATION_PROPOSED` and `HANDOVER_REQUIRED` create open residues but no rollback;
7. `NO_EFFECT_RECORDED` produces no world transition;
8. an attempted paramartha-class change is obstructed;
9. a transaction-lineage digest mismatch is obstructed.

The central law is:

> **Verified effect may change the conventional world record, but it does not by itself change the paramartha class, establish ultimate truth, or complete the mission.**
