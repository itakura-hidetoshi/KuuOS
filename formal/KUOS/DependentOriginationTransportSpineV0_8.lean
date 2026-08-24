import KUOS.DependentOriginationTransportSpineV0_7
import KUOS.DependentOriginationProcessTensorMemoryBridgeV0_8

/-!
# Dependent-origination transport spine v0.8

This aggregate extends the v0.7 memory-lifted history spine by an explicit
operational process-tensor realization.

```text
functorial dependent origination
  |
  +-- free finite-history transport
        |
        +-- explicit enlarged state Visible × Memory
              |
              +-- strict full-state causal composition
              |
              +-- real-linear event realization
                    |
                    +-- finite intervention-word operator
                    +-- operational linear process tensor
                    |     |
                    |     +-- causal append composition
                    |     +-- slotwise linearity
                    |
                    +-- exact visible response = visibleEval
                    +-- exact memory response  = memoryEval
                    |
                    +-- equal-summary process-tensor distinction
                          iff
                        visible non-Markov history sensitivity
                          |
                          +-- obstructs total-time factorization
```

The process-tensor layer is structural.  It does not assert complete positivity,
trace preservation, a Choi state, a quantum comb theorem, a Yang--Mills process
tensor, or a physical mass gap.  Those require additional explicit structures
and proofs.
-/

namespace KUOS.DependentOriginationTransportSpineV0_8

open KUOS.DependentOriginationHistorySensitiveTransportV0_5
open KUOS.DependentOriginationMemoryLiftedHistoryTransportV0_7
open KUOS.DependentOriginationProcessTensorMemoryBridgeV0_8

end KUOS.DependentOriginationTransportSpineV0_8
