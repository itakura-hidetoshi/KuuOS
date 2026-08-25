# Dependent Origination Complete-Segal Infinity-Two Formalization v1.20

## Why completeness is extra

A bicategory already supplies objects, 1-morphisms, 2-morphisms, weak
composition, associators, unitors, pentagon, and triangle.  By v1.19 it also
canonically supplies quasicategorical mapping nerves.

Rezk completeness is additional global information.  It is not the statement
that equivalent objects are definitionally equal.  In the present 2-truncated
setting, the correct univalence form is

```text
(X = Y) ≃ (X ≌ Y),
```

where `X ≌ Y` is Mathlib's native `Bicategory.Equivalence`: an adjoint
equivalence with invertible unit and counit satisfying triangle coherence.

## `ObjectUnivalence`

v1.20 defines

```text
structure ObjectUnivalence B where
  pathEquiv : forall X Y : B, (X = Y) ≃ (X ≌ Y)
```

This records the object-completeness data explicitly rather than manufacturing
it from the bicategory axioms.

Equality always maps canonically to an adjoint equivalence via
`equalityToEquivalence`; the nontrivial completeness content is the inverse
identification and its coherence.

## `CompleteSegalInfinityTwoCategory`

The native class extends the locally scaled infinity-two layer with

```text
mapping_strict_segal : forall X Y, IsStrictSegal (mappingNerve X Y)
object_univalence : ObjectUnivalence B
```

and therefore combines:

- native Mathlib bicategory coherence;
- strict-Segal mapping nerves;
- native Mathlib mapping quasicategories and inner horn fillers;
- explicit scaled mapping simplicial sets;
- object-level Rezk/univalence completeness.

The constructor

```text
completeSegalOfObjectUnivalence
```

proves that any bicategory equipped with `ObjectUnivalence` satisfies the full
v1.20 native class.  All Segal/quasicategory obligations are discharged from
the existing hom-category nerve theorems; only the genuine completeness witness
is additional.

## Exact boundary

```text
Bicategory B
  -> InfinityTwoCategory B                       automatic
  -> LocallyScaledInfinityTwoCategory B         automatic

Bicategory B + ObjectUnivalence B
  -> CompleteSegalInfinityTwoCategory B         proved
```

No theorem claims that arbitrary bicategories are Rezk-complete.  No literal
object collapse is substituted for homotopical completeness.  A future global
scaled/Duskin or complete-Segal-object realization may refine this native
2-truncated class while preserving these theorems as a lower truncation.
