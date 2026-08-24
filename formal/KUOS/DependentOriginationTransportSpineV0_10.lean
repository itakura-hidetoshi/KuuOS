import KUOS.DependentOriginationTransportSpineV0_9
import KUOS.DependentOriginationChoiCompletelyPositiveEquivalenceV0_10

/-!
# Dependent-origination transport spine v0.10

The finite-dimensional quantum branch now reaches Mathlib's native complete
positivity interface:

```text
memory-lifted non-Markov transport
  -> operational process tensor
  -> finite-dimensional complex quantum lift
  -> exact Choi encode/decode
  -> deterministic quantum-comb normalization
  -> Choi PSD iff Mathlib CompletelyPositiveMap
  -> CP + trace preservation quantum-channel certificate
```

The new equivalence is proved constructively.  Complete positivity implies Choi
positivity by the maximally-entangled amplification probe.  Choi positivity
implies complete positivity by Choi square-factorization, explicit Kraus
operators, and positivity of every finite matrix amplification.

No infinite-dimensional or Yang--Mills physical process claim is introduced.
-/

namespace KUOS.DependentOriginationTransportSpineV0_10

end KUOS.DependentOriginationTransportSpineV0_10
