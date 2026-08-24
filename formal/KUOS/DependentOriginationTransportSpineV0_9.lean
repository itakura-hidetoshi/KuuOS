import KUOS.DependentOriginationTransportSpineV0_8
import KUOS.DependentOriginationQuantumChoiCombV0_9

/-!
# Dependent-origination transport spine v0.9

The current formal spine is now:

```text
functorial dependent origination
  |
  +-- reversible transport / Čech branch
  |
  +-- positive-time semigroup branch
  |     |
  |     +-- linear transfer / vacuum / gap / readout decay
  |
  +-- free finite-history branch
        |
        +-- history-sensitive semantics
        +-- memory-lifted Markovization
        +-- operational linear process tensor
              |
              +-- explicit finite-dimensional complex quantum lift
                    |
                    +-- exact Choi encode/decode
                    +-- trace-preserving ↔ partial-trace normalization
                    +-- Choi link-product composition
                    +-- finite-word complete Choi response
                    +-- positive recursive deterministic quantum comb
```

The v0.9 layer deliberately does not coerce the v0.8 real-linear process tensor
into a quantum object.  A `QuantumChoiLift` must explicitly provide the complex
matrix-algebra intervention realization, complex operational process, readout
decoding map, and exact response bridge.

Likewise, positivity is stated directly on Choi matrices via
`Matrix.PosSemidef`, while deterministic comb causality is stated by recursive
output partial traces.  No external completely-positive-map theorem is assumed
without a bridge theorem.

No KuuOS theorem in this aggregate asserts a Yang--Mills Hamiltonian, physical
Yang--Mills process tensor, spectral measure, vacuum-orthogonal sector, or
physical mass gap.
-/

namespace KUOS.DependentOriginationTransportSpineV0_9

open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationHistorySensitiveTransportV0_5
open KUOS.DependentOriginationFreeHistoryFunctorV0_6
open KUOS.DependentOriginationMemoryLiftedHistoryTransportV0_7
open KUOS.DependentOriginationProcessTensorMemoryBridgeV0_8
open KUOS.DependentOriginationQuantumChoiCombV0_9

end KUOS.DependentOriginationTransportSpineV0_9
