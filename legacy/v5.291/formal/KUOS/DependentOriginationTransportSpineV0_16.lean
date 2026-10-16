import KUOS.DependentOriginationTransportSpineV0_15
import KUOS.DependentOriginationTesterDualNormalizationV0_16

namespace KUOS.DependentOriginationTransportSpineV0_16

/-!
# Dependent-origination transport spine v0.16

The quantum branch now separates three normalization levels explicitly:

```text
open-comb complex response
  |
  +-- v0.15 weak closed tester normalization
  |     complete TP words have total scalar weight one
  |
  +-- v0.16 conditional causal tester normalization
        every deterministic newest slot leaves one fixed previous residual
        |
        +-- exact dual matrix recursion
              W_(n+1) = I_output ⊗ X_(n+1)
              Tr_input X_(n+1) = W_n
              W_0 = 1
```

The main v0.16 equivalence is

```text
CausalTesterNormalized d n W
  ↔ DualTesterNormalized d n W
```

and either side implies the v0.15 `TesterNormalized W` predicate.  The reverse
implication from the weaker v0.15 predicate is intentionally not asserted.

This remains finite-dimensional structural quantum process-tensor mathematics;
it does not promote any physical Yang--Mills theorem authority into KuuOS.
-/

end KUOS.DependentOriginationTransportSpineV0_16
