# Dependent Origination Global Duskin / Scaled Nerve — Formal v1.21

## Exact baseline

This layer is additive over the canonical parent after v1.20.

The previous higher-categorical layer supplied:

- a native bicategory;
- mapping quasicategories `N(B(X,Y))`;
- local mapping-object scalings;
- a conditional complete-Segal/univalence certificate.

Those data were not yet one global scaled simplicial set.

## Global Duskin carrier

For a Mathlib bicategory `B`, v1.21 defines

```text
DuskinSimplex B n :=
  StrictlyUnitaryLaxFunctor (LocallyDiscrete (Fin (n+1))) B.
```

Thus

```text
N_Duskin(B)_n = NormalLax([n], B).
```

This is the standard normal-lax definition of the Duskin nerve.

The repository-pinned Mathlib file

```text
Mathlib/CategoryTheory/Bicategory/Functor/StrictlyUnitary.lean
```

already defines normal lax functors and proves strict unit/associativity for their composition, but explicitly lists construction of the Duskin nerve as a TODO. v1.21 supplies that missing global construction in KuuOS.

## Simplicial operators

For a simplex-category arrow, the induced monotone functor between finite ordinals is promoted to a normal lax functor between locally discrete bicategories.

A Duskin simplex is reindexed by normal-lax precomposition.

The theorems

```text
duskinReindex_id
duskinReindex_comp
```

plus Mathlib's strict laws

```text
StrictlyUnitaryLaxFunctor.id_comp
StrictlyUnitaryLaxFunctor.comp_assoc
```

prove the functor laws of

```text
duskinNerve B : SSet.
```

Therefore all face and degeneracy identities belong to one genuine simplicial-set structure rather than being a family of low-dimensional certificates.

## Global scaled structure

A Duskin 2-simplex carries the lax comparison cell

```text
sigma(0->1) >> sigma(1->2) ==> sigma(0->2).
```

v1.21 exposes it as

```text
duskinComparison.
```

The global thin predicate declares a 2-simplex thin when either:

1. its comparison 2-cell is invertible; or
2. it is one of the simplicial degeneracies of a 1-simplex.

The second clause records explicitly the mandatory degenerate scaling. For a normal lax simplex these degenerate triangles are precisely the unit triangles; the presentation keeps the scaled-simplicial-set obligation explicit rather than hiding it behind elaboration of the normality laws.

This yields

```text
duskinScaling B : ScaledSimplicialSet (duskinNerve B)
```

and the bundle

```text
globalScaledDuskinNerve B.
```

## Local versus global

v1.19:

```text
for each X,Y:
  N(B(X,Y)) + a scaling.
```

v1.21:

```text
one SSet N_Duskin(B)
  + one global thin predicate on its 2-simplices.
```

These are different structures. v1.21 is the first global Duskin/scaled carrier in the parent dependent-origination spine.

## Scope boundary

v1.21 does not assert that the underlying Duskin simplicial set of an arbitrary bicategory is an `(infinity,1)` quasicategory. Noninvertible 2-morphisms are precisely the higher information that should not be collapsed into an `(infinity,1)` model.

It also does not yet prove model-equivalence with a global scaled nerve in another formalism such as a complete Segal object, nor a scaled-anodyne horn theorem. Those are stronger comparison/model-structure results.

No quantum, Hamiltonian, spectral-gap, or Yang--Mills authority is introduced.
