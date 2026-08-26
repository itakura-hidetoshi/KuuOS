import KUOS.DependentOriginationScaledSmallObjectArgumentV1_44

namespace KUOS.DependentOriginationCoreSpineV1_44

open CategoryTheory
open KUOS.DependentOriginationScaledSmallObjectArgumentV1_44

/-!
# Dependent-origination core spine v1.44

The higher scaled-Duskin specialization now reaches Mathlib's native
small-object argument.

The parent dependent-origination structure remains context-dependent
establishment plus composable transport.  The scaled simplicial and
bicategorical constructions remain higher specializations/completions rather
than a redefinition of the parent.

The strict-fibrancy / weak-factorization route is now:

```text
canonical horn-cylinder attachment generators T
  -> small morphism property
  -> explicit regular-cardinal small-object data
  -> HasSmallObjectArgument T
  -> functorial factorization T.rlp.llp ; T.rlp
  -> native weak factorization system

and simultaneously

T.rlp.llp
  = retracts
      (transfinite compositions
        (pushouts
          (coproducts T))).
```

All earlier presentation-independent homotopy-class and strict-fibrancy
results remain upstream.  The remaining constructive problem has been moved
entirely to the categorical/presentability properties of `ScaledSSet` needed
to instantiate `CanonicalScaledSmallObjectCardinalData`.
-/

end KUOS.DependentOriginationCoreSpineV1_44
