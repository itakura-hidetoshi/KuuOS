import KUOS.DependentOriginationTransportSpineV0_13
import KUOS.DependentOriginationOpenCombOperationalRealizationV0_14

/-!
# Dependent-origination transport spine v0.14

The quantum branch now distinguishes two mathematically different levels.

```text
closed sequential generalized Born rule (v0.13)
  |
  +-- initial density boundary
  +-- repeated Choi link composition
  +-- final trace closure
  +-- exact joint Born probability

open quantum comb operational semantics (v0.14)
  |
  +-- fixed-length Choi-slot word
  +-- tensor over the full recursive CombIndex history
  +-- direct all-leg open-comb contraction
  +-- explicit external history realization
  |
  +-- optional sequential factorization
        |
        +-- fixed initial matrix
        +-- composed channel only
        +-- fixed final readout
        |
        +-- obstructed whenever equal-composite histories
            have distinct open-comb responses
```

Thus an open process tensor is no longer identified with the v0.13 sequential
state propagation by default.  Sequential propagation is represented by an
explicit factorization certificate and can fail when the comb retains genuine
history information.
-/
