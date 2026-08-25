import KUOS.DependentOriginationCoreSpineV1_15
import KUOS.DependentOriginationQuasicategoryNerveV1_16

namespace KUOS.DependentOriginationCoreSpineV1_16

/-!
# Dependent-origination non-quantum core spine v1.16

The parent frontier now has one concrete quasicategorical realization in
addition to the independent higher-coherence interface:

```text
D : Context ⥤ Type
  -> category of elements ∫ D
  -> simplicial nerve N(∫ D)
  -> strict Segal
  -> inner horn filling
  -> native Mathlib Quasicategory.
```

This closes the previously explicit v1.15 obligations for a specific and
canonical realization of the original one-categorical parent transport.

The distinction remains important:

```text
N(∫ D) is a proved quasicategory,

but

the independent v1.15 globular tower
  != yet proved equivalent to N(∫ D),

and the v1.6 bicategorical source
  != thereby promoted to an (∞,2)-category.
```

Thus the quasicategorical theorem is strong but exactly scoped.
-/

end KUOS.DependentOriginationCoreSpineV1_16
