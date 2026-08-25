import KUOS.DependentOriginationCoreSpineV1_18
import KUOS.DependentOriginationNativeInfinityTwoScaledV1_19

namespace KUOS.DependentOriginationCoreSpineV1_19

/-!
# Dependent-origination non-quantum core spine v1.19

The higher frontier now includes a repository-native typeclass boundary:

```text
Mathlib bicategory
  -> hom-category nerves
  -> native Mathlib quasicategories
  -> KuuOS.InfinityTwoCategory
  -> KuuOS.LocallyScaledInfinityTwoCategory.
```

`InfinityTwoCategory` is automatic for every bicategory and is explicitly a
2-truncated / locally-quasicategorical realization.  `ScaledSimplicialSet`
uses a genuine thin-2-simplex predicate containing all degenerate 2-simplices.
The automatic mapping scaling is maximal and is intentionally not presented as
a global Duskin/scaled nerve of the entire bicategory.
-/

end KUOS.DependentOriginationCoreSpineV1_19
