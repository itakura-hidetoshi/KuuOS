import KUOS.DependentOriginationCoreSpineV1_17
import KUOS.DependentOriginationInfinityTwoYonedaV1_18

namespace KUOS.DependentOriginationCoreSpineV1_18

/-!
# Dependent-origination non-quantum core spine v1.18

The bicategorical higher-realization frontier now contains:

```text
native bicategory
  -> native 2-Yoneda pseudofunctor into Cat-valued pseudofunctors
  -> hom-categories B(X,Y)
  -> mapping nerves N(B(X,Y))
  -> strict Segal
  -> native quasicategories
  -> inner horn filling.
```

This is the strongest `(∞,2)`-realization interface currently justified by the
repository-pinned Mathlib APIs.  It preserves the bicategorical 2-morphisms and
weak associator/unitor coherence without pretending that Mathlib already
provides a completed scaled-simplicial or complete-Segal
`InfinityTwoCategory` target typeclass.
-/

end KUOS.DependentOriginationCoreSpineV1_18
