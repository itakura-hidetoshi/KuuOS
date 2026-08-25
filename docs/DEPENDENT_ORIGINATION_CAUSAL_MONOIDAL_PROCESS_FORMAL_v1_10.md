# Dependent Origination Causal Monoidal Process — Formal v1.10

## Purpose

v1.9 added a native monoidal process layer:

```text
sequential composition = categorical composition
parallel composition   = monoidal tensor
```

v1.10 adds a causal axis without reducing dependent origination to a graph of efficient causes.

The formal layer separates two notions that are often conflated:

1. **causal orientation** — which contextual process arrows are allowed to point from one interface to another;
2. **causal normalization** — whether a process preserves categorical discarding.

## Causal orientation

`CausalOrder Context` contains a relation

```text
precedes : Context -> Context -> Prop
```

with reflexivity, transitivity, compatibility with every admitted process arrow, and compatibility with monoidal tensor.

Thus every process

```text
f : X -> Y
```

implies

```text
X precedes Y.
```

The theorem `CausalOrder.no_process_against_order` makes the contrapositive boundary explicit: if the declared causal orientation forbids `X precedes Y`, there can be no admitted morphism `X -> Y`.

This is an orientation constraint, not a claim that every dependence relation is temporal causation.

## Categorical discarding

`CausalMonoidalProcessStructure` supplies

```text
discard X : X -> I
```

where `I` is the monoidal unit.

Discarding satisfies a tensor compatibility law:

```text
discard (X tensor Y)
=
(discard X tensor discard Y)
  followed by the native unitor I tensor I -> I.
```

A process is then defined to be causal when

```text
f >> discard Y = discard X.
```

This is the standard process-theoretic normalization reading: applying a causal process and then forgetting its output is indistinguishable from forgetting the input directly.

## Closure of causal interventions

The formal theorems prove:

```text
identity causal
causal f + causal g -> causal (f >> g)
causal f + causal g -> causal (f tensor g)
```

`CausalIntervention C X Y` packages a process together with its causality certificate.

Consequently interventions are closed under both:

```text
sequential intervention composition
parallel independent intervention composition.
```

This is the first explicit causal-process subtheory in the restored parent dependent-origination spine.

## Normalized states

Given the v1.9 state-level monoidal realization `P`, a state is normalized when

```text
D.transport (discard X) x = P.unitState.
```

This is packaged by `NormalizedState`.

Two important closure statements are formalized:

1. `CausalIntervention.mapNormalized`
   - every causal intervention maps normalized states to normalized states;
2. `tensorNormalized`
   - independent tensor composition of normalized states is normalized.

The second theorem uses the v1.9 tensor-state naturality together with the native monoidal unitor.

## Relation to non-Markov structure

Causal direction is **not** identified with Markovianity.

A process may retain explicit memory/history while still respecting a causal orientation and discard normalization.  Thus the earlier WORLD / process-tensor memory architecture can remain downstream without contradiction.

## No-signalling boundary

v1.10 deliberately does **not** claim general no-signalling for arbitrary joint multi-condition operations.

The distinction is:

```text
causal normalization
!=
no-signalling factorization.
```

Independent tensor products already behave independently by the v1.9 monoidal law.  For a genuinely joint process

```text
(X1 tensor X2) -> (Y1 tensor Y2)
```

no-signalling requires explicit marginal/factorization equations.  Those should be added as a separate stronger layer rather than inferred from causality alone.

## Current parent hierarchy

```text
contextual transport
  -> descent / cofinal semantics
  -> bicategorical path coherence
  -> operadic multi-condition structure
  -> higher multicategorical coherence
  -> monoidal process theory
  -> causal orientation + discarding
  -> causal interventions + normalized-state preservation
```

## Scope boundary

v1.10 does not claim:

- that dependent origination is identical to causal structure;
- that causality implies Markovianity;
- general no-signalling for arbitrary joint operations;
- symmetric or braided monoidal process theory;
- compact closure or traced feedback;
- sheaf/stack descent;
- enriched hom objects;
- infinity-categorical completion;
- quantum authority in the parent core;
- physical Yang--Mills authority.

The parent reading remains:

> dependent origination is composable contextual establishment before object-substance specialization; causal structure is an additional directional/process-normalization axis.
