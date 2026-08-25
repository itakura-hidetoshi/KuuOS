# Dependent Origination: Strictly-Unitary Duskin Model Transport v1.27

## Purpose

Version 1.26 established that the dependent-origination higher-categorical
invariant is independent of the selected bicategorical model at the intrinsic
1/2-cell level.  A general model equivalence was represented by a native
Mathlib pseudofunctor together with equivalences on every hom-category and
essential surjectivity on objects.

The global Duskin presentation has one additional requirement: its simplices
are `StrictlyUnitaryLaxFunctor`s.  A general pseudofunctor is not definitionally
strictly unitary, and the pinned Mathlib revision does not expose a constructor
that automatically normalizes every pseudofunctor.

Version 1.27 therefore separates the mathematics correctly.  It introduces an
explicit strictly-unitary model-equivalence certificate and proves all global
transport consequences from that certificate.  It does **not** disguise the
remaining normalization theorem as an axiom or silently identify arbitrary
pseudofunctors with normal ones.

## Strictly-unitary model equivalence

The new structure is

```lean
StrictlyUnitaryBicategoricalModelEquivalence B C
```

with data:

- `forward : StrictlyUnitaryPseudofunctor B C`;
- for every `X,Y : B`, a categorical equivalence
  `B(X,Y) ≌ C(FX,FY)`;
- exact identification of its forward functor with the native hom functor of
  `forward`;
- essential surjectivity on objects up to native bicategorical adjoint
  equivalence.

There is an automatic forgetting map

```text
StrictlyUnitaryBicategoricalModelEquivalence B C
        -> BicategoricalModelEquivalence B C.
```

Hence every v1.26 presentation-independent theorem remains available.

## Direct global Duskin transport

For every degree `n` and every global Duskin simplex

```text
σ : [n] -> B,
```

postcomposition with the normalized forward map gives

```text
[n] -> B -> C.
```

Because both factors are strictly unitary lax functors, Mathlib's native
`StrictlyUnitaryLaxFunctor.comp` produces another valid Duskin simplex.

The definition is

```lean
transportDuskinSimplex E σ
```

and satisfies exact object, 1-cell, and 2-cell formulas:

```text
obj  -> F(obj)
map  -> F(map)
map₂ -> F₂(map₂).
```

## Simplicial naturality

Postcomposition commutes with every Duskin reindexing by strict associativity
of `StrictlyUnitaryLaxFunctor.comp`:

```text
transport ((reindex f) ; σ)
  = (reindex f) ; transport(σ).
```

Therefore v1.27 constructs an actual simplicial map

```text
N_Duskin(B) -> N_Duskin(C)
```

in every simplicial degree, not only a low-dimensional correspondence.

## Exact comparison-cell formula

For a source Duskin triangle with principal arrows `f`, `g` and comparison
cell

```text
κ : f ≫ g -> h,
```

the transported global triangle has comparison

```text
F(f) ≫ F(g)
  --(F.mapComp f g)^-1--> F(f ≫ g)
  --F₂(κ)--------------> F(h).
```

Formally,

```text
duskinComparison (transport σ)
  = (F.mapComp f g).inv ≫ F.map₂ (duskinComparison σ).
```

This is the crucial coherence statement.  The target global comparison is not
identified naively with `F.map₂ κ`; the canonical pseudofunctor composition
constraint is inserted exactly where bicategorical weak composition requires
it.

## Compatibility with the presentation-independent invariant

At the one-skeleton, direct global transport equals the intrinsic v1.26
transport exactly:

```text
duskinEdgeArrow (transport σ)
  = transportIntrinsicOneCell (duskinEdgeArrow σ).
```

At the two-cell level, the direct global comparison factors through the v1.26
intrinsic two-cell transport with only the canonical composition constraint in
front:

```text
target global comparison
  = canonical composition coherence
      ; transported intrinsic comparison.
```

Thus the new global presentation does not modify the invariant.  It realizes
the same invariant in a normalized global encoding.

## Scaling

If a source comparison cell is invertible, then:

1. its image under `map₂` is invertible;
2. the pseudofunctor composition constraint is an isomorphism;
3. their composite, the target global comparison, is invertible.

Consequently every nondegenerate source-thin Duskin triangle is sent to a
thin target triangle.

This is currently stated at theorem level.  The remaining upgrade to a bundled
`IsScaledMap` should additionally package preservation of degenerate thin
triangles through the simplicial map.

## Mathematical frontier

Proved in v1.27:

```text
strictly-unitary model equivalence
  -> direct global Duskin transport in all degrees
  -> simplicial global-to-global map
  -> exact 1-cell invariant transport
  -> exact 2-cell coherence factorization
  -> preservation of invertible comparisons
  -> preservation of nondegenerate thinness.
```

Still open, intentionally and explicitly:

1. construct a strictly-unitary normalization for sufficiently general
   pseudofunctorial biequivalence data;
2. prove that different choices of normalization induce equivalent global
   transport and the same intrinsic invariant;
3. package the simplicial map as a fully scaled map, including degeneracies;
4. transport the chosen scaled-horn families and their fillers;
5. use those results toward a presentation-independent global
   `(infinity,2)`-model equivalence theorem.

The important conceptual point is that the presentation-independent invariant
was already established before this normalization problem.  Normalization now
controls only how the same invariant is represented globally.
