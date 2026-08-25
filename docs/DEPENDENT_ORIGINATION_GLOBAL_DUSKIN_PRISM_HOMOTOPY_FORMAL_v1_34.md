# Dependent Origination global Duskin prism homotopy — formal v1.34

Version 1.34 removes the horn-by-horn homotopy choice left in v1.33.

The key object is

```text
GlobalDuskinRoundTripPrismRealization K
```

for normalized coherent quasi-inverse data `K`.  It records one simplicial homotopy in each direction:

```text
normalizedDuskinNerveMap F ; normalizedDuskinNerveMap G ~ id
normalizedDuskinNerveMap G ; normalizedDuskinNerveMap F ~ id.
```

Simplicial homotopy is stable under precomposition.  Therefore each global prism restricts along an arbitrary horn map and automatically gives the `ScaledHornRoundTripBoundaryHomotopy` required by v1.33.

Hence the presentation-independent fibrancy spine now factors as

```text
native strong quasi-inverse
  -> global Duskin prism realization
  -> hornwise round-trip homotopy
  + homotopy-to-strict rectification
  -> ScaledHornRoundTripDescent
  -> ScaledHornPresentationEquivalence
  -> global scaled-fibrancy invariance.
```

This is a genuine reduction of coherence data: there is no longer an independent homotopy witness for every horn.

The remaining boundary is global and nerve-theoretic.  One must construct the two `SSet.Homotopy` values directly from the native Mathlib `Oplax.StrongTrans` values implementing `G F ==> id_B` and `F G ==> id_C`.  This is the Duskin prism construction.  Homotopy rectification remains a separate lifting theorem for the chosen standard scaled-horn presentation and is not conflated with the prism construction.
