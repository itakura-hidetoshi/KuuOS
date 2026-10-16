import Mathlib
import KUOS.DependentOriginationLocalizedSheafUniversalityV2_6

namespace KUOS.DependentOriginationWJCategoryEquivalenceV2_7

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationContextualDescentV1_1
open KUOS.DependentOriginationEffectiveDescentComparisonV2_1
open KUOS.DependentOriginationPresentationUniversalityV2_0
open KUOS.DependentOriginationOppositeSiteVarianceBridgeV2_3
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationBaseChangeDescentV2_5
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6

universe u v w

/-!
# Category-level W + J universality for dependent origination v2.7

The v2.6 layer constructed the objectwise completion

```text
C --localize W--> C[W⁻¹]
                   |
                   | opposite-site sheafification for J_A
                   v
          Sh_{J_A}((C[W⁻¹])ᵒᵖ, Type).
```

This file upgrades that statement from objects to categories.

There are two exact categorical equivalences already available in Mathlib:

1. double-opposite equivalence induces

```text
(C[W⁻¹] ⥤ Type) ≌ (((C[W⁻¹])ᵒᵖ)ᵒᵖ ⥤ Type),
```

2. presentation localization induces

```text
(C[W⁻¹] ⥤ Type) ≌ W.FunctorsInverting Type.
```

Because `Sheaf J A` is literally the full subcategory cut out by
`Presheaf.IsSheaf J`, the first equivalence restricts to an equivalence between
localized covariant functors satisfying descent and the sheaf category.  Pulling
that object property back through the second equivalence then gives a canonical
full subcategory of raw `W`-inverting functors, and this raw admissible category
is equivalent to the same sheaf carrier.

This is the category-level `W + J` theorem.  It still does not add the
higher-coherence axis `H`, and it does not identify arbitrary concrete physical,
medical, or cognitive models with this admissible category without separate
realization theorems.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

section LocalizedCategory

/-- Double-opposite variance correction promoted from objects to the whole
functor category. -/
noncomputable def localizedFunctorPresheafEquivalence :
    (LocalizedContext W ⥤ Type w) ≌
      (((LocalizedContext W)ᵒᵖ)ᵒᵖ ⥤ Type w) :=
  Equivalence.congrLeft (opOpEquivalence (LocalizedContext W)).symm

/-- The ordinary Mathlib sheaf property is invariant under natural isomorphism,
so it can be used as the target object property of `congrFullSubcategory`. -/
instance sheafProperty_isClosedUnderIsomorphisms
    (A : RefinementAtlas (LocalizedContext W)) :
    ObjectProperty.IsClosedUnderIsomorphisms
      (Presheaf.IsSheaf A.generatedTopology (A := Type w)) where
  of_iso e h :=
    (Presheaf.isSheaf_of_iso_iff e).1 h

/-- The property of a localized covariant Type-valued functor whose
variance-correct opposite-site presheaf is a sheaf for the atlas topology.

It is intentionally defined as the inverse image of the ordinary Mathlib sheaf
property along the double-opposite functor-category equivalence. -/
def LocalizedDescentFunctorProperty
    (A : RefinementAtlas (LocalizedContext W)) :
    ObjectProperty (LocalizedContext W ⥤ Type w) :=
  ObjectProperty.inverseImage
    (Presheaf.IsSheaf A.generatedTopology (A := Type w))
    (localizedFunctorPresheafEquivalence W).functor

/-- The pulled-back localized descent property inherits invariance under natural
isomorphism from the ordinary sheaf property. -/
instance localizedDescentFunctorProperty_isClosedUnderIsomorphisms
    (A : RefinementAtlas (LocalizedContext W)) :
    (LocalizedDescentFunctorProperty (W := W) A).IsClosedUnderIsomorphisms := by
  unfold LocalizedDescentFunctorProperty
  infer_instance

/-- The full category of localized covariant contextual functors satisfying the
generated Grothendieck descent condition. -/
abbrev LocalizedDescentFunctorCategory
    (A : RefinementAtlas (LocalizedContext W)) :=
  (LocalizedDescentFunctorProperty (W := W) A).FullSubcategory

/-- The category-level variance/descent theorem: localized covariant contextual
functors satisfying `J_A`-descent are equivalent to the Type-valued sheaf
carrier `DO₁(C,W,A)` from v2.6. -/
noncomputable def localizedDescentFunctorEquivalenceCompletion
    (A : RefinementAtlas (LocalizedContext W)) :
    LocalizedDescentFunctorCategory (W := W) A ≌
      DependentOriginationCompletion1 (W := W) A :=
  (localizedFunctorPresheafEquivalence W).congrFullSubcategory
    (Q := Presheaf.IsSheaf A.generatedTopology (A := Type w)) rfl

/-- Package an ordinary localized functor as the existing KuuOS contextual
transport-system interface. -/
def transportSystemOfLocalizedFunctor
    (F : LocalizedContext W ⥤ Type w) :
    FunctorialTransportSystem (LocalizedContext W) where
  state := F

/-- The full-subcategory predicate is exactly the v2.3 Grothendieck-descent
predicate on the same localized contextual transport. -/
theorem localizedDescentFunctorProperty_iff_grothendieckDescent
    (A : RefinementAtlas (LocalizedContext W))
    (F : LocalizedContext W ⥤ Type w) :
    LocalizedDescentFunctorProperty (W := W) A F ↔
      IsGrothendieckDescentComplete A.generatedTopology
        (transportSystemOfLocalizedFunctor W F) := by
  rfl

/-- Under the geometric hypotheses from v2.5, membership in the localized
category is equivalently effective KuuOS descent at every localized context. -/
theorem localizedDescentFunctorProperty_iff_allEffectiveStateDescent
    (A : RefinementAtlas (LocalizedContext W))
    (hbc : A.IsBaseChangeClosed)
    (O : A.PushoutOverlapAtlas)
    (F : LocalizedContext W ⥤ Type w) :
    LocalizedDescentFunctorProperty (W := W) A F ↔
      ∀ X : LocalizedContext W,
        HasEffectiveStateDescent
          (transportSystemOfLocalizedFunctor W F)
          (A.coverAt X)
          (O.overlap X) := by
  rw [localizedDescentFunctorProperty_iff_grothendieckDescent W A F]
  exact
    isGrothendieckDescentComplete_iff_allEffectiveStateDescent
      A hbc O (transportSystemOfLocalizedFunctor W F)

end LocalizedCategory

section RawCategory

/-- Presentation localization, oriented from raw `W`-inverting functors back to
localized functors. -/
noncomputable def rawWInvertingLocalizedEquivalence :
    W.FunctorsInverting (Type w) ≌ (LocalizedContext W ⥤ Type w) :=
  (presentationFunctorEquivalence W (Type w)).symm

/-- The raw `W + J` admissibility property on already bundled `W`-inverting
functors.  It is the inverse image of localized Grothendieck descent along the
localization equivalence. -/
def RawWJFunctorProperty
    (A : RefinementAtlas (LocalizedContext W)) :
    ObjectProperty (W.FunctorsInverting (Type w)) :=
  ObjectProperty.inverseImage
    (LocalizedDescentFunctorProperty (W := W) A)
    (rawWInvertingLocalizedEquivalence W).functor

/-- The category of raw Type-valued contextual functors which invert `W` and
whose presentation-independent representative satisfies `J_A` descent. -/
abbrev RawWJFunctorCategory
    (A : RefinementAtlas (LocalizedContext W)) :=
  (RawWJFunctorProperty (W := W) A).FullSubcategory

/-- The localization equivalence restricts exactly to the two admissible full
subcategories. -/
noncomputable def rawWJFunctorEquivalenceLocalized
    (A : RefinementAtlas (LocalizedContext W)) :
    RawWJFunctorCategory (W := W) A ≌
      LocalizedDescentFunctorCategory (W := W) A :=
  (rawWInvertingLocalizedEquivalence W).congrFullSubcategory
    (Q := LocalizedDescentFunctorProperty (W := W) A) rfl

/-- Category-level `W + J` universal classification.

Raw contextual Type-valued functors which invert all presentation changes in
`W` and satisfy the pulled-back localized `J_A` descent condition form a category
equivalent to the sheaf carrier `DO₁(C,W,A)`. -/
noncomputable def rawWJFunctorEquivalenceCompletion
    (A : RefinementAtlas (LocalizedContext W)) :
    RawWJFunctorCategory (W := W) A ≌
      DependentOriginationCompletion1 (W := W) A :=
  (rawWJFunctorEquivalenceLocalized W A).trans
    (localizedDescentFunctorEquivalenceCompletion W A)

end RawCategory

/-!
The 1-categorical universality spine is now categorical rather than merely
objectwise:

```text
RawWJFunctorCategory(C,W,A)
          ≌
LocalizedDescentFunctorCategory(C[W⁻¹],A)
          ≌
Sh_{J_A}((C[W⁻¹])ᵒᵖ, Type)
          =
DO₁(C,W,A).
```

The first equivalence is presentation localization restricted to the pulled-back
descent property.  The second is the double-opposite variance equivalence
restricted to the Mathlib sheaf property.  Both are equivalences of full
categories, hence include morphisms and their compositions, not only object
classification.

The next genuinely new axis is higher coherence `H`.  Before claiming the final
`DO(C,W,J,H)`, a later unit must specify the higher-admissible morphisms and show
that the existing bicategorical/scaled-simplicial coherence spine realizes the
required higher completion universal property.
-/

end KUOS.DependentOriginationWJCategoryEquivalenceV2_7
