import KUOS.DependentOriginationCoreSpineV1_33
import KUOS.DependentOriginationGlobalDuskinPrismHomotopyV1_34

namespace KUOS.DependentOriginationCoreSpineV1_34

/-!
# Dependent-origination core spine v1.34

The parent contextual-transport definition remains unchanged.

Version 1.34 globalizes the homotopy bridge introduced in v1.33:

```text
native strong quasi-inverse
  + global Duskin prism homotopies
      N(F) ; N(G) ~ id
      N(G) ; N(F) ~ id
  -> all hornwise round-trip homotopies by precomposition
  + homotopy rectification
  -> strict round-trip horn descent
  -> presentation-independent scaled fibrancy.
```

Thus no independent homotopy choice is required for each horn.  The remaining
nerve-theoretic frontier is the single global prism construction from the native
`Oplax.StrongTrans` quasi-inverse data.
-/

end KUOS.DependentOriginationCoreSpineV1_34
