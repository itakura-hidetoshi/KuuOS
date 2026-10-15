import KUOS.DependentOriginationTransportSpineV0_2
import KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3

/-!
# Dependent-origination transport spine v0.3

This aggregate module extends the v0.2 transport spine by separating the generic
composable-transport principle from the additional linear structure carried by
transfer operators.

```text
functorial dependent origination
  |
  +-- reversible action-groupoid / Čech transport
  |
  +-- non-invertible additive positive-time transport
        |
        +-- contractive vacuum-fixed transport
              |
              +-- abstract exponential excitation gap
                    |
                    +-- bounded-readout exponential decay
                    |
                    +-- linear transfer realization
                          |
                          +-- T_t (x - Ω) = T_t x - Ω
                                |
                                +-- connected readout
                                      |
                                      +-- exponential connected decay
```

The linear-transfer branch does not promote the KuuOS abstraction to a physical
Yang--Mills theorem.  It records the exact extra algebraic structure needed to
interpret an abstract dependent-origination transport as a transfer operator and
to pass its excitation decay to vacuum-subtracted/connected readouts.
-/

namespace KUOS.DependentOriginationTransportSpineV0_3

open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationExponentialGapTransportV0_2
open KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3

end KUOS.DependentOriginationTransportSpineV0_3
