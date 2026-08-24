# Dependent Origination — Filtered Categorical Cofinal Semantics v1.4

## Scope

This layer generalizes the non-quantum dependent-origination refinement spine
from preorder-indexed directed nets to arbitrary indexing categories with an
explicit filteredness certificate.

It does not redefine dependent origination as a filtered category.  The parent
notion remains the v0.1 contextual state-valued functor and composable
transport.  Filtered indexing is an additional refinement architecture.

## Parent orientation

The contextual direction remains covariant:

```text
root context -> conditioned context -> further conditioned context.
```

A `FilteredRefinementDiagram` consists of:

- one root context;
- a functor from an indexing category into contextual presentations;
- one root-to-diagram-object arrow for every index;
- exact compatibility of those root arrows with all indexing morphisms.

Thus an indexing morphism represents an admissible further conditioning, not an
isomorphism requirement.

## Explicit filteredness

`FilteredIndexing` records:

1. an inhabited indexing category;
2. a common future object for every pair of objects;
3. eventual coequalization of every pair of parallel arrows.

The third condition matters because a general category can retain distinct
refinement paths.  The structure therefore goes beyond the preorder-directed
carrier of v1.3 without silently forcing those paths to be equal immediately.

No categorical colimit is assumed.

## Coherent state family

`FilteredStateFamily D R` assigns

```text
state j : D.state.obj (R.chart.obj j)
```

to every indexing object and requires exact transport coherence along every
indexing arrow.

A single root state induces such a family by functorial transport, but the
converse remains a separate predicate:

```text
StateDescendsOnFilteredDiagram D R s
```

means that one root state actually produces all diagram states.

This is not derived from filteredness.

## Semantic descent

For an invariant readout `Q`, coherence along one indexing arrow gives equality
of semantic values at its source and target.

The common-future part of filteredness then compares any two indexing objects.
Hence every coherent filtered family has one unique invariant semantic value:

```text
filteredSemanticDescends_of_coherent
```

proves `FilteredSemanticDescends Q R s`.

The semantic theorem does not require a root-state witness.

## Cofinal change of indexing category

`CofinalIndexingFunctor J K` consists of a functor

```text
F : K ⥤ J
```

such that every `j : J` admits an arrow

```text
j -> F.obj k
```

for some `k : K`.

This is the exact objectwise cofinal condition needed by the current semantic
proof.  The file deliberately does not identify this structure with the full
Mathlib final-functor API and does not claim a general colimit-preservation
theorem.

For every candidate semantic value `v`, the theorem

```text
filteredSemanticStabilizesAt_iff_cofinal
```

proves that stabilization on the whole filtered diagram is equivalent to
stabilization on the selected cofinal subsystem.

Lifting this pointwise statement to `ExistsUnique` gives the main semantic
result:

```text
filteredSemanticDescends_iff_cofinal
```

or mathematically,

```text
unique invariant meaning on J
<->
unique invariant meaning on any objectwise cofinal K -> J.
```

Thus invariant meaning does not depend on which sufficiently far-reaching
conditioning lens is used.

## State boundary

Cofinality does not by itself recover the root state.

A root state may agree with the target family after transport to all selected
future objects even though distinct local states have already collapsed under
those transports.

The explicit predicate

```text
CofinalFunctorSeparatesLocalStates D R F
```

therefore requires the cofinal lens to separate states at every original
context.

Only under this additional condition does

```text
stateDescends_iff_cofinalStateWitness_of_separates
```

prove

```text
full root-state descent
<->
root-state agreement on the cofinal subsystem.
```

This preserves the structural asymmetry established in v1.1-v1.3:

```text
semantic invariance is robust under refinement,
state/substance recovery needs additional separation.
```

## Boundary theorem

`semantic_persists_without_cofinal_root_carrier` combines both sides.

Under local-state separation, if no global root-state witness exists, then no
cofinal root-state witness exists either.  Nevertheless the invariant semantic
value still descends uniquely on the cofinal subsystem.

So the formal architecture allows:

```text
no global root carrier
+ no cofinal root carrier
+ one unique invariant meaning.
```

This is the intended dependent-origination reading: increasingly refined
conditions can stabilize meaning without forcing one underlying substance-like
state to exist.

## Relation to v1.3

v1.3 used a preorder and a chosen refinement arrow whenever `i <= j`.

v1.4 permits:

- multiple refinement arrows between the same contexts;
- nontrivial path data;
- eventual rather than immediate coequalization of parallel paths;
- categorical reindexing by a functor rather than only a monotone map.

The preorder-directed system remains a special, simpler refinement language.
This PR does not remove or weaken it.

## Non-goals

This layer does not assert:

- a categorical colimit object;
- a universal cocone theorem;
- Mathlib final-functor equivalence;
- a Grothendieck topology;
- sheaf or stack descent;
- groupoid-only dependent origination;
- quantum/process-tensor structure;
- Hamiltonian or spectral-gap claims;
- physical Yang--Mills authority.

Those are possible specializations or stronger structures, not the parent
meaning of dependent origination.

## Current non-quantum spine

```text
contextual functorial transport
-> transport-compatible system maps
-> reversible presentation equivalence as extra structure
-> finite history / memory-lifted history
-> local covers and overlap compatibility
-> optional state descent
-> invariant semantic descent
-> refinement transitivity
-> directed refinement nets
-> order-cofinal semantics
-> filtered categorical refinement
-> categorical cofinal semantics
```

The central invariant remains:

```text
meaning can be stable across conditioning and refinement
without promoting one global carrier to an ontological primitive.
```
