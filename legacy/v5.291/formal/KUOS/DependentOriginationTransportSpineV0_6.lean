import KUOS.DependentOriginationFunctorialTransportV0_1
import KUOS.GaugeInvariantDependentOriginationFunctorialTransportBridgeV0_1
import KUOS.DependentOriginationExponentialGapTransportV0_2
import KUOS.DependentOriginationLinearTransferConnectedReadoutV0_3
import KUOS.DependentOriginationFiniteTransferWordV0_4
import KUOS.DependentOriginationHistorySensitiveTransportV0_5
import KUOS.DependentOriginationFreeHistoryFunctorV0_6

/-!
# Dependent-origination transport spine v0.6

The current KuuOS transport architecture is now organized as

```text
functorial dependent origination
  |
  +-- reversible action-groupoid / Čech descent
  |
  +-- free finite-history category
        |
        +-- HistoryTransport
        |     |
        |     +-- generated uniquely by single-event transports
        |     +-- may distinguish ordered histories
        |
        +-- optional total-time factorization
              |
              +-- additive positive-time semigroup
                    |
                    +-- linear transfer realization
                    +-- vacuum subtraction
                    +-- abstract exponential gap
                    +-- connected-readout decay
```

The categorical parent law is compositional transport.  The free-history
specialization uses `SingleObj (List Event)`: finite words are morphisms and
history evaluation is the corresponding state-valued functor.

A total-time factorization is additional structure, not the definition of
history semantics.  Conversely, the strict `HistoryTransport.eval_append` law
means that v0.5/v0.6 history semantics is exactly a free-monoid action on the
chosen state carrier.  A genuinely higher-order process tensor must therefore
enter through an explicit richer carrier/event/category bridge rather than by
terminology alone.

No physical Yang--Mills theorem authority is imported by this aggregate.
-/

namespace KUOS.DependentOriginationTransportSpineV0_6

open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationHistorySensitiveTransportV0_5
open KUOS.DependentOriginationFreeHistoryFunctorV0_6

end KUOS.DependentOriginationTransportSpineV0_6
