# Dependent Origination Two-Yoneda `(∞,2)` Realization — Formal v1.18

## Status

v1.18 starts from the genuine Mathlib bicategory used by the v1.6 dependent-
origination carrier.

The repository-pinned Mathlib revision provides:

- native bicategories;
- hom-categories of 1- and 2-morphisms;
- associators, unitors, whiskering, pentagon and triangle laws;
- a native `Cat`-valued bicategorical 2-Yoneda pseudofunctor;
- simplicial nerves of categories;
- strict Segal simplicial sets;
- native quasicategories and inner-horn filling.

It does not expose a single completed `InfinityTwoCategory` target typeclass, a
scaled-simplicial-set `(∞,2)` model, or a complete-Segal-object model that KuuOS
can honestly instantiate directly.

Accordingly v1.18 constructs the strongest native realization interface that is
actually available.

## Mapping quasicategories

For a bicategory `B` and objects `X,Y`, define

```text
mappingNerve X Y := nerve (X ⟶ Y).
```

The objects of the hom-category `X ⟶ Y` are the bicategorical 1-morphisms, and
its morphisms are the bicategorical 2-morphisms.  Therefore this nerve retains
the source 2-dimensional information rather than set-truncating it.

The theorem

```text
mappingNerve_segal
```

proves that every spine map is bijective.

The theorem

```text
mappingNerve_quasicategory
```

proves

```text
SSet.Quasicategory (mappingNerve X Y).
```

The theorem

```text
mappingNerve_innerHornFilling
```

then gives an actual filler for every inner horn in every mapping object.

Thus each bicategorical hom-category becomes a mapping quasicategory.

## Composition action

v1.18 also defines

```text
precompositionNerveMap
postcompositionNerveMap
```

by applying the ordinary nerve functor to Mathlib's native bicategorical
precomposition and postcomposition functors.

Therefore 1-morphisms of `B` act functorially on the mapping quasicategories.

## Native 2-Yoneda coherence

Mathlib provides

```text
Bicategory.yoneda : B ⥤ᵖ (Bᵒᵖ ⥤ᵖ Cat).
```

v1.18 re-exports this as

```text
twoYoneda
```

and as

```text
BicategoricalTransportSystem.toTwoYoneda.
```

This pseudofunctor is not a mere object assignment.  Its identity and
composition comparison isomorphisms are built from the bicategorical unitors
and associators, so the weak composition coherence of the v1.6 source is
retained.

## Exact proved chain

```text
v1.6 native bicategory B
  -> native 2-Yoneda pseudofunctor B -> [Bᵒᵖ, Cat]
  -> hom-categories B(X,Y)
  -> nerves N(B(X,Y))
  -> strict Segal mapping objects
  -> native mapping quasicategories
  -> inner horn filling.
```

This is the natural locally-quasicategorical realization of the bicategory
using the APIs available in the pinned library.

## Relation to `(∞,2)` terminology

Mathematically, an `(∞,2)`-category has mapping `(∞,1)`-categories.  The v1.18
mapping objects are genuine Mathlib quasicategories, and the bicategorical
2-Yoneda pseudofunctor retains weak composition coherence.

For this reason v1.18 is called an `(∞,2)`-realization interface.

It is deliberately not declared to instantiate a nonexistent pinned-Mathlib
`InfinityTwoCategory` class.  A future stronger layer may choose and formalize a
specific standard model, for example:

- scaled simplicial sets;
- complete Segal objects in quasicategories;
- a suitable enriched/Segal model.

Only after the corresponding model-specific axioms are formalized should the
stronger target name be used as a theorem conclusion.

## Non-claims

v1.18 does not claim:

- arbitrary bicategories are strict `Cat`-enriched categories;
- a strictification theorem absent from the pinned library;
- a scaled simplicial set construction;
- complete Segal completeness;
- that the v1.15 arbitrary globular tower equals this realization;
- an `(∞,2)` comparison equivalence not yet constructed.

The new theorem layer keeps the existing v1.6 bicategorical source intact and
adds a faithful higher-realization route without collapsing its 2-morphisms.
