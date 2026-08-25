# Dependent Origination coherent normalized scaled model equivalence — formal v1.32

Version 1.32 separates the remaining existence problem into its true bicategorical and horn-level parts.

The bicategorical quasi-inverse is now represented natively. For normalized strictly-unitary model maps

```text
F : B -> C
G : C -> B
```

KuuOS records strong transformations

```text
G F ==> id_B
F G ==> id_C
```

using Mathlib `Oplax.StrongTrans`, and requires every object component to be an intrinsic equivalence 1-cell.

This yields coherent round-trip isomorphisms on every 1-cell and the corresponding exact naturality squares on every 2-cell. Thus quasi-inverse coherence is no longer hidden inside a horn-level assumption.

The remaining bridge is isolated as `ScaledHornRoundTripDescent`: filler existence for the chosen scaled horn presentation must be invariant under the two coherent normalized Duskin round trips.

The package `CoherentNormalizedScaledModelEquivalence` contains:

- general Whitehead-style model equivalences in both directions;
- chosen strictly-unitary normalization certificates;
- native coherent quasi-inverse data for the normalized representatives;
- full scaled global Duskin maps both ways;
- admissible horn-family preservation both ways;
- the final horn round-trip descent certificate.

From these data KuuOS constructs the v1.31 `BidirectionalScaledDuskinModelEquivalence`, hence a `ScaledHornPresentationEquivalence`, and proves global scaled-Duskin fibrancy invariant.

The next frontier is therefore precise: derive `ScaledHornRoundTripDescent` from a simplicial/horn homotopy comparison induced by the native strong quasi-inverse, rather than supplying it separately.
