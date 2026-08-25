# Dependent Origination Native Infinity-Two / Scaled Formalization v1.19

## Scope

This layer bundles the already proved bicategorical 2-Yoneda and hom-category
nerve construction into repository-native higher-categorical classes without
claiming stronger models than have actually been formalized.

## Native `InfinityTwoCategory`

For a Mathlib bicategory `B`, every hom-category `B(X,Y)` has a simplicial nerve

```text
mappingNerve X Y = nerve (X ⟶ Y).
```

The v1.18 theorems prove each such nerve is strict Segal, a native Mathlib
quasicategory, and has every inner horn filler.  v1.19 packages this as

```text
class InfinityTwoCategory B
```

and proves an instance for every Mathlib bicategory.

The meaning is deliberately exact: this is the canonical 2-truncated embedding
of a bicategory into a locally quasicategorical `(infinity,2)` model.  Mapping
`(infinity,1)`-categories are nerves of ordinary hom-categories, so no new
higher cells above the original 2-morphisms are fabricated.

## Native scaled simplicial-set class

`ScaledSimplicialSet X` consists of

```text
thin : X_2 -> Prop
```

plus proofs that both degenerate 2-simplices obtained from every 1-simplex are
thin.  This is the standard minimum scaling axiom.

`ScaledSimplicialSet.maximal X` marks every 2-simplex thin and therefore gives a
canonical scaling on every simplicial set.

`LocallyScaledInfinityTwoCategory B` equips each mapping quasicategory with a
scaling.  Every bicategory receives an automatic instance via maximal mapping
scalings.

## Boundary

The automatic scaling is local to the mapping quasicategories.  It is not called
a global Duskin nerve or a global scaled nerve of the bicategory.  Constructing
that stronger object requires a separate simplicial realization of objects,
1-morphisms, 2-morphisms, and bicategorical coherence.
