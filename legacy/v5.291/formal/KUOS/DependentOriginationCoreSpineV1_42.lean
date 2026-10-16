import KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42

namespace KUOS.DependentOriginationCoreSpineV1_42

open CategoryTheory
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42

/-!
# Dependent-origination core spine v1.42

The presentation-independence spine now packages the canonical scaled
horn-cylinder attachments as a Mathlib morphism property and passes to its
lifting-theoretic Galois closure.

The parent dependent-origination structure remains contextual establishment
plus composable transport.  The scaled-Duskin development remains a higher
specialization/completion and does not redefine that parent.

The v1.42 strict-fibrancy route is:

```text
canonical minimally-scaled horn-cylinder inclusions
  -> generator morphism property T
  -> canonical scaled-anodyne closure T.rlp.llp
  -> Mathlib equality (T.rlp.llp).rlp = T.rlp

therefore every compatible presentation
  T <= A <= T.rlp.llp
has the same right class and the same fibrant objects.

attachment-fibrant global Duskin nerve
  -> terminal RLP for every horn problem
  -> terminal RLP for every chosen horn family
  -> v1.40 attachment lifting
  -> v1.39 cylinder extension
  -> homotopy-class strictification
  -> strict scaled horn fibrancy.

coherent normalized bicategorical model equivalence
  + attachment fibrancy of both global Duskin nerves
  -> presentation-independent strict scaled fibrancy.
```

A future standard scaled-anodyne implementation only has to be compared as a
morphism property with this canonical generator/closure sandwich.  No ordinary
anodyne class is silently identified with the scaled class.
-/

end KUOS.DependentOriginationCoreSpineV1_42
