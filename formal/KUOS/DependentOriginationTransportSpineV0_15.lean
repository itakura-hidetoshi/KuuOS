import KUOS.DependentOriginationTransportSpineV0_14
import KUOS.DependentOriginationQuantumTesterBornV0_15

namespace KUOS.DependentOriginationTransportSpineV0_15

/-!
# Dependent-origination transport spine v0.15

The quantum branch now separates two different Choi objects that must not be
identified merely because both use the same finite history index.

```text
open deterministic quantum comb
  |
  +-- arbitrary complex-linear all-leg response
  +-- history sensitivity / sequential-factorization obstruction

closed quantum process tester
  |
  +-- positive tester Choi matrix
  +-- deterministic tester normalization on all CPTP slot words
  +-- positive CP-history weights
  +-- finite quantum-instrument outcome tensor
  +-- total Born probability = 1
```

The distinction is structural.  v0.14 `QuantumCombChoi.tensorLinkScalar` is a
response and is not automatically a normalized probability.  v0.15 adds the
separate `QuantumProcessTesterChoi` carrier whose positivity and deterministic
normalization are exactly the hypotheses needed to obtain a Born law.

No theorem from v0.1-v0.14 is weakened or reinterpreted.
-/

end KUOS.DependentOriginationTransportSpineV0_15
