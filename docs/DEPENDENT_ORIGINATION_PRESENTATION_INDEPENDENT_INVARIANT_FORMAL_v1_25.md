# Dependent Origination: Presentation-Independent Invariant Kernel v1.25

## Purpose

v1.25 changes the comparison strategy.

Earlier layers compare two presentations of one bicategory `B`:

- the local mapping presentation `mappingNerve X Y = N(B(X,Y))`;
- the global scaled Duskin presentation.

The invariant itself should be neither of these presentations.  The canonical
presentation-independent carrier is the intrinsic bicategorical data:

- objects: `B`;
- mapping invariant: the hom-category `B(X,Y)`;
- intrinsic object equivalence: native bicategorical adjoint equivalence;
- intrinsic 1-cell equivalence: isomorphism in the hom-category;
- intrinsic 2-cell invertibility: `IsIso`.

The local and global presentations are therefore compared only after projecting
to this common carrier.

## Main formal file

`formal/KUOS/DependentOriginationPresentationIndependentInvariantV1_25.lean`

Aggregate spine:

`formal/KUOS/DependentOriginationCoreSpineV1_25.lean`

## Intrinsic mapping invariant

For every pair `X,Y : B`, define

```text
PresentationIndependentMappingInvariant X Y := B(X,Y).
```

This is the native hom-category of the bicategory and therefore does not depend
on choosing a local nerve or a global Duskin realization.

The local presentation reads a vertex through Mathlib's native nerve
equivalence:

```text
mappingNerve(X,Y)_0 -> B(X,Y).
```

The global presentation reads a fixed-endpoint Duskin edge through its principal
1-morphism:

```text
GlobalDuskinEdgeOver(B,X,Y) -> B(X,Y).
```

v1.25 proves that for every global edge `e`, the local vertex obtained from `e`
and the global edge itself have exactly the same image in `B(X,Y)`.

## Intrinsic 2-cell invariant

A local mapping-nerve edge between parallel 1-morphisms is read through
Mathlib's native `nerve.homEquiv`:

```text
MappingNerveEdge(X,Y,f,g) -> (f -> g).
```

A global Duskin 2-simplex is read through its normal-lax comparison cell:

```text
sigma_01 >> sigma_12 -> sigma_02.
```

v1.25 proves the commuting equality

```text
localTwoCellInvariant(duskinComparisonMappingEdge sigma)
  = globalTwoCellInvariant sigma.
```

Thus local and global data agree after passing to the same intrinsic 2-cell.

## Universal observable theorem

The strongest formulation in v1.25 is not tied to a particular quantity.

For any codomain `Z` and any observable

```text
F : B(X,Y) -> Z,
```

v1.25 proves that evaluating `F` on the local image of a global edge gives the
same result as evaluating `F` on the global edge's intrinsic 1-cell.

Likewise, for any observable on the relevant intrinsic 2-cell space, the local
and global values agree.

Schematically:

```text
presentation -> intrinsic carrier -> observable
```

is independent of whether the starting presentation is local or global.

This is the first theorem-level form of

```text
presentation-independent invariant.
```

## Scaling becomes intrinsic

For a nondegenerate global Duskin triangle `sigma`, v1.25 proves

```text
global thinness
  <-> IsIso(global comparison 2-cell).
```

The right-hand side is an intrinsic statement in the hom-category and no longer
mentions either simplicial presentation.

The same condition can also be expressed through the local mapping edge, and
the two formulations agree by the commuting 2-cell theorem.

## Intrinsic equivalence of parallel 1-morphisms

Define

```text
IntrinsicOneCellsEquivalent f g := Nonempty (f ≅ g)
```

inside the hom-category `B(X,Y)`.

v1.25 proves that the local mapping nerve contains an invertible edge between
`f` and `g` exactly when `f` and `g` are intrinsically isomorphic.

A nondegenerate globally thin Duskin triangle therefore always yields the same
intrinsic 1-cell equivalence and hence an invertible local mapping edge.

The converse for arbitrary local edges is not promoted to a global triangle
without an explicit global triangle representability theorem.

## Object equivalence

Define the intrinsic object-equivalence relation by

```text
IntrinsicObjectEquivalent X Y := Nonempty (X ≌ Y).
```

The local presentation contains an equivalence vertex exactly when this
intrinsic relation holds.

Under `GlobalDuskinEdgeRepresentability B X Y`, the global presentation contains
a fixed-endpoint Duskin equivalence edge exactly when the same intrinsic relation
holds.

Therefore, under global edge representability,

```text
local equivalence vertex
  <-> intrinsic adjoint equivalence
  <-> global Duskin equivalence edge.
```

If `ObjectUnivalence B` is also supplied, then

```text
X = Y
  <-> local equivalence vertex
  <-> intrinsic adjoint equivalence
  <-> global Duskin equivalence edge.
```

This is bundled in `PresentationIndependentCompleteObjectKernel`.

## Automatic kernel

Every bicategory canonically supplies

```text
PresentationIndependentTwoSkeletonKernel B.
```

It records:

1. local/global 1-cell agreement;
2. local/global 2-cell agreement;
3. nondegenerate global scaling equals intrinsic 2-cell invertibility.

No horn-filling or univalence assumption is needed for this automatic
2-skeleton kernel.

## Complete object-level kernel

Given

```text
ObjectUnivalence B
```

and

```text
GlobalDuskinLocalOneSkeletonComparison B,
```

v1.25 constructs

```text
PresentationIndependentCompleteObjectKernel B.
```

It simultaneously records path/local/global agreement for object equivalence.

## Mathematical meaning

The new factorization is

```text
                   intrinsic bicategory B
                          /       \
                         /         \
          local mapping nerve     global scaled Duskin
```

rather than

```text
local presentation <-> global presentation
```

as a primitive claim.

This distinction matters.  A comparison between presentations should be proved
by showing that both represent the same invariant data, not by declaring one
representation to be canonical by fiat.

## What is not yet proved

v1.25 does **not** yet prove:

- reverse representability of every local 2-cell by a controlled global Duskin
  triangle;
- construction of a fixed-endpoint global mapping simplicial object in every
  degree;
- equivalence of that global mapping object with `N(B(X,Y))`;
- compatibility of a full comparison with composition, scaling, and the chosen
  scaled-horn family;
- equivalence of complete local and global `(infinity,2)` models;
- invariance under replacing `B` itself by a biequivalent but different
  bicategory.

## Next frontier

The next mathematically decisive step is to move from

```text
same bicategory, two presentations
```

to

```text
biequivalent bicategories, same invariant.
```

The target chain is:

```text
presentation-independent two-skeleton kernel
  -> controlled global 2-cell representability
  -> full mapping-object comparison
  -> composition/scaling/horn compatibility
  -> local/global model equivalence
  -> invariance under bicategorical equivalence
  -> presentation-independent invariant.
```

The final invariant should therefore be stable not only under changing the
simplicial presentation of one `B`, but also under changing the bicategory model
within its appropriate equivalence class.
