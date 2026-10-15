import KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43

namespace KUOS.DependentOriginationCoreSpineV1_43

open CategoryTheory
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneWFSUniversalityV1_43

/-!
# Dependent-origination core spine v1.43

The higher scaled-Duskin specialization now separates generator choice,
orthogonal saturation, and factorization.

```text
canonical horn-cylinder generators T
  -> right orthogonal T.rlp
  -> canonical left orthogonal closure T.rlp.llp

T.rlp.llp
  = least orthogonally saturated class containing T
  = unique orthogonally saturated compatible v1.42 presentation

left closure laws:
  retracts / cobase change / composition
right closure laws:
  retracts / base change / composition

remaining constructive input:
  HasFactorization (T.rlp.llp) (T.rlp)

then:
  Mathlib IsWeakFactorizationSystem (T.rlp.llp) (T.rlp)
```

Thus the future small-object argument is isolated to factorization.  Lifting,
retract stability, pushout/pullback stability, composition, and presentation
universality are already theorem-level consequences of the orthogonality
construction.

The parent KuuOS dependent-origination definition remains contextual
establishment plus composable transport.  This scaled weak-factorization layer
is a higher specialization/completion and does not redefine that parent.
-/

end KUOS.DependentOriginationCoreSpineV1_43
