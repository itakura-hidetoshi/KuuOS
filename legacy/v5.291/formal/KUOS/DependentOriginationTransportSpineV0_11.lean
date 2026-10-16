import KUOS.DependentOriginationTransportSpineV0_10
import KUOS.DependentOriginationCPTPChoiWordV0_11

/-!
# Dependent-origination transport spine v0.11

The quantum branch now closes native CPTP finite-history dynamics:

```text
memory-lifted non-Markov transport
  -> operational process tensor
  -> complex Choi representation
  -> deterministic quantum-comb causality
  -> Choi positivity iff Mathlib complete positivity
  -> native CPTP composition
  -> positive normalized linked Choi words
  -> density-matrix preservation
  -> exact linked-Choi reconstruction of finite CPTP evolution
```

This layer does not yet identify an arbitrary process-tensor readout with a
probability.  Quantum instruments and comb contraction normalization remain a
separate theorem layer.
-/

namespace KUOS.DependentOriginationTransportSpineV0_11

end KUOS.DependentOriginationTransportSpineV0_11
