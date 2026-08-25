import KUOS.DependentOriginationCoreSpineV1_28
import KUOS.DependentOriginationScaledDuskinHornTransportV1_29

namespace KUOS.DependentOriginationCoreSpineV1_29

/-!
# Dependent-origination core spine v1.29

The parent definition remains contextual composable transport.  Version 1.29
lifts presentation-independence from intrinsic 1/2-cell data to the scaled-horn
interface.

The new theorem-level chain is:

```text
scaled simplicial map
  -> horn-extension problems transport forward
  -> scaled fillers transport forward
  -> admissible horn families transport under an explicit family-map certificate
```

For the global Duskin realization, a strictly-unitary model equivalence already
provides the underlying simplicial map and nondegenerate thin preservation.
Full scaling preservation, including degenerate 2-simplices, remains isolated as
`FullScaledDuskinMapCertificate`; once supplied, the generic horn/filler
transport applies directly to the global Duskin nerves.

No one-way map is used to infer complete target fibrancy.  Such a conclusion
requires inverse or essential-surjectivity data at the scaled horn-presentation
level.
-/

end KUOS.DependentOriginationCoreSpineV1_29
