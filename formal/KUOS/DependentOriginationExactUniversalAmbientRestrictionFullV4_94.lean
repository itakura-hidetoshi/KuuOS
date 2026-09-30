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

/-- The modification-naturality property holds on identities. Unlike the raw
image-arrow case, this is intrinsic to the StrongTrans identity coherence and
does not require a chosen presentation representative. -/
theorem higherLocalizedModificationNaturalityProperty_id
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta)
    (X : LocalizedContext W) :
    higherLocalizedModificationNaturalityProperty (W := W) Gamma (𝟙 X) := by
  dsimp [higherLocalizedModificationNaturalityProperty]
  simp only [Functor.map_id, Quiver.Hom.id_toLoc]
  simp [Pseudofunctor.StrongTrans.naturality_id_hom]

/-- A Cat-valued localized pseudofunctor sends every isomorphism of the
underlying localized category to an equivalence of categories.

We build the quasi-inverse directly from the image of the inverse arrow. The
unit and counit are the pseudofunctor mapId/mapComp isomorphisms, so this lemma
uses only the pinned pseudofunctor API and does not depend on newer mathlib
adjunction conveniences. -/
noncomputable def higherLocalizedMapEquivalenceOfIso
    (H : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))
    {X Y : LocalizedContext W}
    (e : X ≅ Y) :
    H.obj (.mk ((opOp (LocalizedContext W)).obj X)) ≌
      H.obj (.mk ((opOp (LocalizedContext W)).obj Y)) := by
  let p :=
    ((opOp (LocalizedContext W)).map e.hom).toLoc
  let q :=
    ((opOp (LocalizedContext W)).map e.inv).toLoc
  have hpq : p ≫ q = 𝟙 _ := by
    apply Discrete.ext
    dsimp [p, q]
    simp
  have hqp : q ≫ p = 𝟙 _ := by
    apply Discrete.ext
    dsimp [p, q]
    simp
  let etaCat :
      𝟙 (H.obj (.mk ((opOp (LocalizedContext W)).obj X))) ≅
        H.map p ≫ H.map q :=
    (H.mapId _).symm ≪≫
      H.mapComp' p q (𝟙 _) hpq
  let epsCat :
      H.map q ≫ H.map p ≅
        𝟙 (H.obj (.mk ((opOp (LocalizedContext W)).obj Y))) :=
    (H.mapComp' q p (𝟙 _) hqp).symm ≪≫
      H.mapId _
  exact
    CategoryTheory.Equivalence.mk
      (H.map p).toFunctor
      (H.map q).toFunctor
      (by
        simpa only [Cat.Hom.id_toFunctor, Cat.Hom.comp_toFunctor] using
          Cat.Hom.toNatIso etaCat)
      (by
        simpa only [Cat.Hom.id_toFunctor, Cat.Hom.comp_toFunctor] using
          Cat.Hom.toNatIso epsCat)

/-- In particular, the image functor of an isomorphism is an equivalence. -/
theorem higherLocalizedMap_isEquivalence_of_iso
    (H : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))
    {X Y : LocalizedContext W}
    (e : X ≅ Y) :
    ((H.map (((opOp (LocalizedContext W)).map e.hom).toLoc).toFunctor)
      .IsEquivalence := by
  exact
    (higherLocalizedMapEquivalenceOfIso (W := W) H e).isEquivalence_functor

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
#print axioms higherLocalizedModificationNaturalityProperty_id
#print axioms higherLocalizedMapEquivalenceOfIso
#print axioms higherLocalizedMap_isEquivalence_of_iso
#print axioms higherLocalizedModificationNaturalityProperty_map

end

end KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94
