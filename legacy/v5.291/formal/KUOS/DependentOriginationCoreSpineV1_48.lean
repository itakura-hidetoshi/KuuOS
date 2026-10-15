import KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48

namespace KUOS.DependentOriginationCoreSpineV1_48

open CategoryTheory
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48

/-!
# Dependent-origination core spine v1.48

The higher scaled-Duskin specialization now separates the canonical KuuOS
horn-cylinder generator into two mathematically different pieces.

For every canonical attachment generator

```text
j_min : A_min -> C
```

there is a literal factorization

```text
A_min
  -- scaling enrichment -->
A_induced
  -- induced attachment inclusion -->
C.
```

Here `A_induced` carries exactly the scaling pulled back from the cylinder.
Consequently the v1.46 comparison condition

```text
T ≤ E.rlp.llp
```

can be proved from the pair

```text
scaledHornAttachmentScalingEnrichments ≤ E.rlp.llp
inducedScaledHornAttachmentGenerators ≤ E.rlp.llp.
```

This distinction is essential when comparing with a standard/Lurie-style
scaled-anodyne presentation.  The inner-horn pushout-product geometry belongs
to the induced-attachment factor; the minimal-to-induced scaling enrichment is
an additional comparison problem and is not silently identified with it.

The parent dependent-origination structure remains context-dependent
establishment plus composable transport.  This is a higher specialization,
not a redefinition of the parent.
-/

end KUOS.DependentOriginationCoreSpineV1_48
