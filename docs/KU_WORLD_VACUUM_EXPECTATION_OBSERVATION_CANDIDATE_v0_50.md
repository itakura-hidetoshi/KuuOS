# WORLD Vacuum Expectation Observation Candidate Bridge v0.50

v0.50 extends the WORLD v0.49 read-only vacuum layer with a typed observation-candidate bridge.

```text
v0.49 analytic vacuum state
  → admissible observable
  → exact vacuum expectation value
  → immutable observation identifier
  → exact context binding
  → exact evidence-receipt binding
  → read-only observation candidate
```

The bridge does not convert a vacuum expectation into a fact, a truth authority, a belief update, a planning trigger, an execution license, or a WORLD mutation.

## Candidate construction

For every admissible observable `a`, v0.50 constructs a candidate carrying:

```text
observation id
context
source evidence receipt
observable a
admissibility proof
value ω_Kū(a)
exact equality value = ω_Kū(a)
```

The candidate value is not independently supplied.

It is definitionally generated from the v0.49 vacuum state.

This prevents substitution of an unrelated scalar after source binding.

## Lean-derived consequences

Lean directly derives three core consequences from v0.49.

### Normalization

The candidate generated from the identity observable satisfies

```text
value([1]) = ω_Kū(1) = 1.
```

### Positivity

For every observable `a`, the candidate generated from `a* a` satisfies

```text
Re value([a* a]) >= 0.
```

### Gauge equivalence

For every supplied gauge action `g`, the candidate values satisfy

```text
value([g · a]) = value([a]).
```

This is equality of analytic candidate values.

It is not a declaration that two WORLD contexts, evidence histories, or operational states have collapsed into one.

## Source exactness

Every candidate preserves exact equalities for:

```text
candidate observation id = observationIdOf(observable)
candidate context = registered observation context
candidate receipt = registered evidence receipt
```

The source packet is immutable at this layer.

A later consumer may reject or retain the candidate, but may not replace its source while presenting it as the same candidate.

## Runtime boundary

The runtime flags are fixed to false for:

```text
candidate → fact promotion
candidate → belief promotion
candidate → PlanOS activation
candidate → ActOS authority
physical-time execution
WORLD update
```

The bridge remains a read-only mathematical sidecar.

No WORLD formal result directly activates PlanOS or ActOS.

## Fixed boundary

```text
vacuum expectation != fact
vacuum expectation != truth authority
observation candidate != belief promotion
observation candidate != PlanOS activation
observation candidate != ActOS authority
WORLD sidecar != control objective
modular time != physical time
candidate equality != WORLD collapse
validation != truth
runtime remains read-only
```

v0.50 does not construct new physical observables, execute physical time, infer empirical truth, or replace clinical, institutional, scientific, or mathematical review.
