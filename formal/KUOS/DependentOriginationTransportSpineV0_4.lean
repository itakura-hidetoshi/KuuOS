import KUOS.DependentOriginationTransportSpineV0_3
import KUOS.DependentOriginationFiniteTransferWordV0_4

/-!
# Dependent-origination transport spine v0.4

This aggregate module exposes the current KuuOS mathematical transport spine:

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
                                +-- vacuum-subtracted connected readout
                                      |
                                      +-- finite transfer-word history
                                            |
                                            +-- word = total-time semantics
                                            +-- product gap weight
                                            +-- finite-word connected decay
```

The v0.4 word layer distinguishes syntax from semantics.  A word retains its
ordered finite transfer history, while the present one-parameter additive
semigroup makes its denotation factor through the sum of the word's positive
times.  This factorization is a theorem of the semigroup specialization, not a
definition of dependent origination in general.

Consequently, future non-Markovian/process-tensor realizations may preserve
history-sensitive word semantics by replacing the total-time factorization,
without changing the upper functorial dependent-origination layer.

As before, no KuuOS theorem in this aggregate asserts a Yang--Mills Hamiltonian,
spectral measure, physical vacuum-orthogonal sector, or physical mass gap.
Those physical obligations remain in the authoritative physical proof
repository.
-/

namespace KUOS.DependentOriginationTransportSpineV0_4

open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationExponentialGapTransportV0_2
open KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3
open KUOS.DependentOriginationFiniteTransferWordV0_4

end KUOS.DependentOriginationTransportSpineV0_4
