import KUOS.DependentOriginationCoreSpineV1_25
import KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26

namespace KUOS.DependentOriginationCoreSpineV1_26

/-!
# Dependent-origination core spine v1.26

The v1.26 spine advances presentation independence from

```text
same bicategory / different higher presentations
```

to

```text
different bicategorical models related by Whitehead-style biequivalence data.
```

The parent dependent-origination definition remains unchanged.  The new layer
uses a native Mathlib pseudofunctor together with categorical equivalences on
every hom-category and essential surjectivity on objects up to bicategorical
adjoint equivalence.

The invariant route is

```text
source local/global presentation
        ↓
source intrinsic hom-category
        ↓  categorical equivalence induced by the pseudofunctor
target intrinsic hom-category
        ↓
target local mapping presentation.
```

The one-cell and two-cell squares commute exactly.  Consequently every
observable or predicate that factors through the transported intrinsic carrier
is independent both of the higher presentation and of the chosen
biequivalent bicategorical model at the present two-skeleton frontier.

A direct target global Duskin simplex is intentionally not required here.
The present global Duskin nerve uses strictly unitary normal-lax simplices,
whereas a general pseudofunctor need not be strictly unitary.  The remaining
problem is therefore a normalization/presentation theorem, not a defect in the
intrinsic invariant.
-/

end KUOS.DependentOriginationCoreSpineV1_26
