import KUOS.DependentOriginationCoreSpineV1_13
import KUOS.DependentOriginationStackDescentV1_14

namespace KUOS.DependentOriginationCoreSpineV1_14

/-!
# Dependent-origination non-quantum core spine v1.14

The local/global hierarchy now distinguishes two levels:

```text
weak parent descent:
  local compatibility / semantic descent
  without automatic global state reconstruction

strong optional stack layer:
  Grothendieck topology
  + Cat-valued pseudofunctor
  + native Mathlib IsStack
  -> effective descent.
```

The strong layer is additive and conditional; it does not retroactively turn the
whole parent dependent-origination theory into a sheaf or stack.
-/

end KUOS.DependentOriginationCoreSpineV1_14
