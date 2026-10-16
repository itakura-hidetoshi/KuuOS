import KUOS.DependentOriginationTransportSpineV0_4
import KUOS.DependentOriginationHistorySensitiveTransportV0_5

/-!
# Dependent-origination transport spine v0.5

The KuuOS transport spine now separates finite-history syntax from the
one-parameter semigroup specialization:

```text
functorial dependent origination
  |
  +-- reversible action-groupoid / Čech transport
  |
  +-- finite composable history transport
        |
        +-- genuinely history-sensitive semantics permitted
        |
        +-- total-time factorization certificate
              |
              +-- additive positive-time semigroup
                    |
                    +-- linear transfer realization
                    +-- vacuum-centered connected readout
                    +-- exponential gap/readout decay
```

The key architectural change is directionality: total-time collapse is no longer
part of the parent history semantics.  It is an additional theorem/certificate
for the current positive-time semigroup specialization.

Thus a future non-Markov/process-tensor realization may distinguish two finite
histories with equal total elapsed time without changing the definition of
dependent-origination transport.

No physical Yang--Mills theorem authority is imported by this aggregate module.
-/

namespace KUOS.DependentOriginationTransportSpineV0_5

end KUOS.DependentOriginationTransportSpineV0_5
