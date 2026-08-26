import KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46

namespace KUOS.DependentOriginationCoreSpineV1_46

open CategoryTheory
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43
open KUOS.DependentOriginationScaledColimitsPresentabilityV1_45
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46

/-!
# Dependent-origination core spine v1.46

The internal canonical scaled small-object/WFS route is closed in v1.45.
Version 1.46 isolates the external comparison boundary at generator level.

For an external generator family `E`, it is enough to prove

```text
T ≤ E.rlp.llp
E ≤ T.rlp.llp
```

where `T` is the canonical KuuOS horn-cylinder generator family.  These two
mutual closure-generation statements imply

```text
E.rlp.llp = T.rlp.llp
E.rlp     = T.rlp.
```

Hence the external family inherits the already-proved canonical weak
factorization system without a second small-object argument, and external
terminal fibrancy is exactly canonical attachment fibrancy.

The higher dependent-origination spine therefore reaches

```text
bicategorical model equivalence
  -> canonical global Duskin prism
  -> homotopy-class horn invariance
  -> strictification via relative cylinders
  -> canonical attachment RLP
  -> canonical generator family T
  -> explicit scaled colimits and finite presentability
  -> small-object argument
  -> canonical WFS (T.rlp.llp, T.rlp)
  -> external generator comparison
  -> external WFS and external-fibrancy equivalence.
```

No external/Lurie scaled-anodyne class is asserted to exist in pinned Mathlib.
A future standard implementation only has to discharge the two generator-level
closure inclusions above.
-/

end KUOS.DependentOriginationCoreSpineV1_46
