import KUOS.DependentOriginationCoreSpineV1_31
import KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32

namespace KUOS.DependentOriginationCoreSpineV1_32

/-!
# Dependent-origination core spine v1.32

The parent contextual-transport definition remains unchanged.

Version 1.32 resolves the bicategorical quasi-inverse layer of the global
presentation-independent fibrancy spine:

```text
general model equivalences B -> C and C -> B
  + strictly-unitary normalization certificates
  + native strong round-trip coherence GF ==> id_B and FG ==> id_C
  + full scaled global Duskin maps
  + admissible horn-family preservation
  + horn filler descent through coherent round trips
  -> v1.31 BidirectionalScaledDuskinModelEquivalence
  -> ScaledHornPresentationEquivalence
  -> scaled fibrancy invariance.
```

The remaining boundary is now specifically horn-level: prove that scaled horn
filler existence descends through the coherent simplicial round-trip induced by
the native strong quasi-inverse data.
-/

end KUOS.DependentOriginationCoreSpineV1_32
