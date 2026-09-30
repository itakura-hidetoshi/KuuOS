import KUOS.DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93
import Mathlib.CategoryTheory.Localization.Construction

namespace KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94

open CategoryTheory
open Opposite
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalAmbientRestrictionHomEquivalenceV4_92
open KUOS.DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Ambient restriction fullness v4.94

This theorem unit attacks the first remaining v4.93 obligation: fullness of
restriction on StrongTrans hom categories.

The first step is canonical and unconditional. Mathlib's constructed
localization has a literal object equivalence
`Context ≃ W.Localization`. Therefore every component of a raw modification
between restricted StrongTrans determines a canonical component at every
localized object. The remaining proof obligation is precisely naturality of
this component family along every localized morphism.

The latter will be discharged using
`Localization.Construction.morphismProperty_eq_top'`: it is enough to prove
the modification square on raw image arrows, composition, and inverses.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Canonical extension of the object components of a modification defined after
restriction. The chosen source object is Mathlib's canonical inverse of
`Localization.Construction.objEquiv`, not an arbitrary choice. -/
noncomputable def higherLocalizedModificationExtensionApp
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta)
    (Y : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)) :
    alpha.app Y ⟶ beta.app Y := by
  let Z : LocalizedContext W := unop (unop Y.as)
  let X : Context := (Localization.Construction.objEquiv W).symm Z
  have hX : W.Q.obj X = Z := by
    simpa [X] using
      (Localization.Construction.objEquiv W).apply_symm_apply Z
  have hY :
      (LocallyDiscrete.mk ((higherPresentationUnitFunctor W).obj X) :
        LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)) = Y := by
    apply LocallyDiscrete.ext
    change op (op (W.Q.obj X)) = Y.as
    rw [hX]
  rw [← hY]
  exact Gamma.as.app (.mk X)

/-- On an object coming from the original context, the canonical extended
component is definitionally the original raw component. -/
@[simp] theorem higherLocalizedModificationExtensionApp_presentation
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta)
    (X : Context) :
    higherLocalizedModificationExtensionApp (W := W) Gamma
        (.mk ((higherPresentationUnitFunctor W).obj X)) =
      Gamma.as.app (.mk X) := by
  rfl

#print axioms higherLocalizedModificationExtensionApp
#print axioms higherLocalizedModificationExtensionApp_presentation

end

end KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94
