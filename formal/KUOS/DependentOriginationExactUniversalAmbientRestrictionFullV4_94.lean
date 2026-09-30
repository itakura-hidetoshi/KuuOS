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

Mathlib's constructed localization has a literal object equivalence
`Context ≃ W.Localization`. Hence a raw modification after restriction already
determines the component at every localized object. The genuine remaining
obligation is morphism naturality.

We package that equation as a `MorphismProperty` on the constructed
localization. The image-arrow case is exactly the naturality equation of the
given raw modification. The next step is to close composition and inverse
stability and then apply
`Localization.Construction.morphismProperty_eq_top'`.
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
component is the original raw component. -/
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

/-- The modification-naturality equation, viewed as a property of a morphism in
the constructed localization. The double-opposite functor only restores the
variance used by the KuuOS higher-localized site. -/
def higherLocalizedModificationNaturalityProperty
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta) :
    MorphismProperty (LocalizedContext W) :=
  fun X Y f =>
    let p :=
      ((opOp (LocalizedContext W)).map f).toLoc
    F.map p ◁
          higherLocalizedModificationExtensionApp (W := W) Gamma
            (.mk ((opOp (LocalizedContext W)).obj Y)) ≫
        (beta.naturality p).hom =
      (alpha.naturality p).hom ≫
        higherLocalizedModificationExtensionApp (W := W) Gamma
            (.mk ((opOp (LocalizedContext W)).obj X)) ▷
          G.map p

/-- The modification-naturality property is stable under composition of
localized morphisms. This is the bicategorical pasting law for the two
modification squares, with the StrongTrans composition coherences supplying the
necessary reassociations. -/
theorem higherLocalizedModificationNaturalityProperty_comp
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta)
    {X Y Z : LocalizedContext W}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf :
      higherLocalizedModificationNaturalityProperty (W := W) Gamma f)
    (hg :
      higherLocalizedModificationNaturalityProperty (W := W) Gamma g) :
    higherLocalizedModificationNaturalityProperty (W := W) Gamma (f ≫ g) := by
  dsimp [higherLocalizedModificationNaturalityProperty] at hf hg ⊢
  simp only [Functor.map_comp, Quiver.Hom.comp_toLoc]
  simp only [Pseudofunctor.StrongTrans.naturality_comp_hom]
  simp [hf, hg]

/-- The naturality property holds on every raw image arrow. This is exactly the
naturality field of the supplied restricted modification. -/
theorem higherLocalizedModificationNaturalityProperty_map
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta)
    {X Y : Context} (f : X ⟶ Y) :
    higherLocalizedModificationNaturalityProperty (W := W) Gamma
      (W.Q.map f) := by
  simpa only
    [higherLocalizedModificationNaturalityProperty,
      higherLocalizedModificationExtensionApp_presentation,
      higherPresentationUnitFunctor,
      restrictHigherLocalizedStrongTrans]
    using Gamma.as.naturality f.toLoc

#print axioms higherLocalizedModificationExtensionApp
#print axioms higherLocalizedModificationExtensionApp_presentation
#print axioms higherLocalizedModificationNaturalityProperty_comp
#print axioms higherLocalizedModificationNaturalityProperty_map

end

end KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94
