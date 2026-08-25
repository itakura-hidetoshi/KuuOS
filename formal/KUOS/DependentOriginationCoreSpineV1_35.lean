import KUOS.DependentOriginationCoreSpineV1_34
import KUOS.DependentOriginationStrongTransformationDuskinCylinderV1_35

namespace KUOS.DependentOriginationCoreSpineV1_35

/-!
# Dependent-origination core spine v1.35

The parent contextual-transport definition remains unchanged.

Version 1.35 lowers the remaining global-prism construction to the correct
bicategorical level:

```text
native strong quasi-inverse GF ==> id_B, FG ==> id_C
  -> pseudofunctor strong transformations
  -> normal-lax cylinders B × [1] -> B and C × [1] -> C
  -> degreewise mixed Duskin simplices
  -> one native SSet.Homotopy in each direction
  -> global Duskin prism
  -> all hornwise round-trip homotopies.
```

The cylinder-to-prism part is now theorem-level and independent of horns.  The
remaining bicategorical construction is precisely uncurrying the native strong
transformations into their normal-lax cylinders.

The v1.33 homotopy-to-strict rectification property remains an explicit extra
lifting hypothesis; simplicial homotopy by itself is not used to claim strict
scaled-horn fibrancy.
-/

end KUOS.DependentOriginationCoreSpineV1_35
