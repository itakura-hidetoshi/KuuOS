import KUOS.DependentOriginationCoreSpineV1_32
import KUOS.DependentOriginationScaledHornHomotopyDescentV1_33

namespace KUOS.DependentOriginationCoreSpineV1_33

/-!
# Dependent-origination core spine v1.33

The parent contextual-transport definition remains unchanged.

Version 1.33 decomposes the last horn-descent obstruction into its actual
homotopical ingredients:

```text
native strong quasi-inverse
  -> hornwise global Duskin round-trip homotopy       -- realization boundary
round-trip strict filler + hornwise homotopy
  -> homotopy filler                                  -- proved
homotopy filler + homotopy rectification
  -> original strict filler                           -- explicit property
original strict filler
  -> round-trip strict filler                         -- automatic
  -> ScaledHornRoundTripDescent                       -- proved
  -> presentation-independent scaled fibrancy.
```

Thus v1.33 no longer treats horn descent as an opaque primitive.  The remaining
work is split into the nerve/prism realization of the strong quasi-inverse and
homotopy-to-strict rectification for the chosen standard scaled-horn family.
-/

end KUOS.DependentOriginationCoreSpineV1_33
