# Dependent Origination Directed Cofinal Semantics v1.3

## Purpose

v1.1 introduced contextual covers, common refinements, overlap compatibility,
and the distinction between state descent and semantic descent.

v1.2 then proved exact transitivity through refinement-of-refinement.

v1.3 moves from finite-depth refinement diagrams to a potentially unbounded
directed refinement net while keeping the same non-quantum parent notion of
dependent origination.

The orientation remains covariant:

```text
root -> X_i -> X_j      when i <= j.
```

No categorical colimit is assumed.  No sheaf, stack, site, groupoid, quantum,
or Hamiltonian structure is added to the parent layer.

## 1. Directed refinement system

A `DirectedRefinementSystem Context Index` contains:

- one root context;
- a context `chart i` for every preorder index;
- a root-to-chart morphism;
- a chosen refinement morphism whenever `i <= j`;
- exact identity and composition coherence;
- exact agreement between direct root-to-chart transport and transport through
  an earlier stage;
- a common upper refinement for every pair of indices.

Thus the context diagram can continue to finer and finer conditions without
requiring a final or terminal context.

## 2. Coherent state family

A `DirectedStateFamily D R` chooses

```text
s_i : D(X_i)
```

at every stage and requires

```text
D(i -> j)(s_i) = s_j
```

whenever `i <= j`.

A root state always generates such a family by functorial transport.

The converse is deliberately not automatic.  `StateDescendsOnNet` is the
explicit predicate saying that all `s_i` arise from one root state.

## 3. Invariant semantics on a directed net

For an invariant readout `Q`, coherence immediately gives equality of semantic
values along every refinement arrow.

Directedness then gives equality at arbitrary two stages by sending both to a
common upper refinement.

For a nonempty index type, the theorem

```text
netSemanticDescends_of_coherent
```

proves one unique semantic value for the whole coherent net.

This requires no root-state witness.

## 4. Order-cofinal refinement lens

A `CofinalRefinementLens R SubIndex` consists of a monotone map

```text
F : SubIndex -> Index
```

such that every original stage lies below some selected stage:

```text
forall i, exists j, i <= F(j).
```

This is specifically an order-theoretic notion of cofinality.  v1.3 does not
claim that `F` is a categorical final functor and does not invoke a colimit
universal property.

## 5. Exact semantic cofinality

For a proposed semantic value `v`, v1.3 proves

```text
semantic value is v on every stage
<->
semantic value is v on every stage selected by F.
```

The reverse implication uses cofinality: an arbitrary stage can be refined into
a selected one, and invariant semantics is unchanged along that refinement.

The `ExistsUnique` upgrade is

```text
netSemanticDescends_iff_cofinal
```

so full-net semantic descent is exactly equivalent to semantic descent on any
cofinal refinement lens.

This is stronger than merely saying that one preferred sequence of refinements
has a stable value.

## 6. Why cofinality alone does not recover a root state

Suppose a root state matches the coherent family on all selected cofinal
stages.  That still does not imply equality at every earlier stage.

Two distinct local states can in principle become equal after further
refinement.

Therefore v1.3 does not assert

```text
cofinal root witness => full root witness.
```

Instead it introduces the explicit condition

```text
CofinalLensSeparatesLocalStates.
```

At each stage `i`, if two local states become equal after transport to every
selected later cofinal stage, then they were already equal at `i`.

Only under this separation condition is state descent equivalent to existence
of a cofinal root witness.

## 7. Semantic/state asymmetry

The resulting hierarchy is:

```text
coherent directed family
        |
        +--> invariant semantic descent
        |       |
        |       +--> exact cofinal criterion
        |             no state separation required
        |
        +--> root-state descent
                |
                +--> cofinal criterion only with
                     local-state separation.
```

Thus the semantic layer is structurally more robust under contextual
refinement than the state-carrier layer.

## 8. No manufactured carrier

If the full directed family has no root-state witness and the cofinal lens
separates local states, then no root-state witness can appear merely by looking
only at the cofinal stages.

At the same time, the invariant semantic value still descends uniquely on that
same cofinal lens.

The theorem

```text
semantic_persists_without_cofinal_root_carrier
```

records both statements together.

## 9. Relation to dependent origination

The structural interpretation is now:

```text
context
  -> conditioned state
  -> refinement
  -> coherent refinement net
  -> invariant meaning stable under further conditioning
  -> cofinal choice of observational/refinement lens does not change meaning.
```

The key point is not that one hidden global object is reconstructed by taking
an infinitely fine limit.

Rather, stable meaning can be invariant across an indefinitely refinable
network of conditioned presentations even when root-state reconstruction is
not justified.

## 10. Relation to previous specializations

The following remain downstream specializations rather than the parent
definition:

- reversible action groupoids and Cech-style gauge changes;
- finite event histories;
- memory-lifted history;
- semigroup transport;
- process tensors;
- Choi channels and quantum combs;
- Hamiltonian or spectral-gap realizations.

v1.3 does not change their theorems.  It only strengthens the non-quantum
contextual spine above them.

## 11. Scope boundary

This file does not claim:

- existence of categorical colimits;
- a Grothendieck topology;
- sheaf or stack descent;
- that every contextual family has a root-state witness;
- that cofinality alone reflects state equality;
- any physical Yang--Mills result.

The formal result is narrower and exact:

```text
invariant semantics of a coherent directed refinement family
is uniquely determined on every order-cofinal refinement lens,
while state reconstruction requires additional separation.
```
