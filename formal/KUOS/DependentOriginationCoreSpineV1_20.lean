import KUOS.DependentOriginationCoreSpineV1_19
import KUOS.DependentOriginationCompleteSegalInfinityTwoV1_20

namespace KUOS.DependentOriginationCoreSpineV1_20

/-!
# Dependent-origination non-quantum core spine v1.20

The complete higher-categorical boundary is now explicit:

```text
Bicategory B
  -> InfinityTwoCategory B                       automatic
  -> LocallyScaledInfinityTwoCategory B         automatic

Bicategory B + ObjectUnivalence B
  -> CompleteSegalInfinityTwoCategory B         proved
```

`ObjectUnivalence B` is not a synonym for literal object collapse.  It requires
an equivalence of types

```text
(X = Y) ≃ (X ≌ Y)
```

with `X ≌ Y` Mathlib's native bicategorical adjoint equivalence.  This is the
2-truncated Rezk-completeness/univalence condition.  It is deliberately not
asserted for arbitrary bicategories.
-/

end KUOS.DependentOriginationCoreSpineV1_20
