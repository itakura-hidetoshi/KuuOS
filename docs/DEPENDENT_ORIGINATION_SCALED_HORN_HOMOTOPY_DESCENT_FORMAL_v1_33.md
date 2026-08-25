# Dependent Origination scaled horn homotopy descent — formal v1.33

Version 1.33 refines the final horn-level obstruction in the presentation-independent global `(∞,2)` spine.

The key point is that a simplicial homotopy from a normalized round trip back to the identity does **not** by itself turn a filler of the transported horn into a strict filler of the original horn. What it gives canonically is a simplex whose boundary is homotopic to the prescribed horn map.

The formal factorization is therefore:

```text
strict round-trip filler
  + hornwise round-trip homotopy
  -> homotopy filler of the original horn
  + homotopy-to-strict rectification
  -> strict filler of the original horn.
```

The new `HomotopyScaledHornFiller` stores:

- a scaled simplex map `Δ[n] -> X`;
- a native Mathlib `SSet.Homotopy` from its actual horn boundary to the prescribed horn map.

`ScaledHornHomotopyRectification` isolates the extra statement that every such homotopy filler can be strictified.

`ScaledHornRoundTripBoundaryHomotopy` records the hornwise simplicial realization of the normalized round trips. `NormalizedQuasiInverseDuskinHomotopyRealization` ties that data to the native strong quasi-inverse introduced in v1.32.

The theorem

```text
scaledHornRoundTripDescent_of_homotopy_rectification
```

proves that hornwise round-trip homotopy plus source and target rectification imply the exact v1.32 `ScaledHornRoundTripDescent` certificate.

The reverse implication on filler existence is automatic: an original strict filler is postcomposed with the two full scaled Duskin maps.

Consequently the remaining frontier is no longer an opaque "horn descent" assumption. It is split into two concrete constructions:

1. realize the native `Oplax.StrongTrans` comparisons `GF ==> id_B` and `FG ==> id_C` as hornwise simplicial homotopies of the global Duskin nerves;
2. prove homotopy-to-strict rectification for the chosen standard scaled-horn presentation.

No strict equality of equivalent presentations is assumed.
