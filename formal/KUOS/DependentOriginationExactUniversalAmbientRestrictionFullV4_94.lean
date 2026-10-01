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
open KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90
open KUOS.DependentOriginationExactUniversalAmbientRestrictionUniversalityV4_91
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
  simp [Pseudofunctor.StrongTrans.naturality_comp_hom, hf, hg]

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
  simp [Pseudofunctor.StrongTrans.naturality_id_hom]

/-- A Cat-valued localized pseudofunctor sends every isomorphism of the
underlying localized category to an equivalence of categories.

Pinned mathlib already provides `Functor.IsEquivalence.mk'`, so we only need
the image of the inverse arrow together with the pseudofunctor unit/composition
isomorphisms. This avoids the ambiguous `≌` notation between categorical and
bicategorical equivalences. -/
theorem higherLocalizedMap_isEquivalence_of_iso
    (H : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))
    {X Y : LocalizedContext W}
    (e : X ≅ Y) :
    (H.map (((opOp (LocalizedContext W)).map e.hom).toLoc).toFunctor).IsEquivalence := by
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
    Functor.IsEquivalence.mk'
      (H.map q).toFunctor
      (by
        simpa only [Cat.Hom.id_toFunctor, Cat.Hom.comp_toFunctor] using
          Cat.Hom.toNatIso etaCat)
      (by
        simpa only [Cat.Hom.id_toFunctor, Cat.Hom.comp_toFunctor] using
          Cat.Hom.toNatIso epsCat)

/-- Naturality is stable under inversion of an isomorphism in the localized
base. The proof cancels left whiskering by the image of the forward arrow; that
whiskering is faithful because the forward arrow is sent to an equivalence of
categories. The remaining equation is the composition coherence for the
StrongTrans, together with the already-known square for the forward arrow. -/
theorem higherLocalizedModificationNaturalityProperty_inv
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta)
    {X Y : LocalizedContext W}
    (e : X ≅ Y)
    (h :
      higherLocalizedModificationNaturalityProperty (W := W) Gamma e.hom) :
    higherLocalizedModificationNaturalityProperty (W := W) Gamma e.inv := by
  let p :=
    ((opOp (LocalizedContext W)).map e.hom).toLoc
  let q :=
    ((opOp (LocalizedContext W)).map e.inv).toLoc
  let mX :=
    higherLocalizedModificationExtensionApp (W := W) Gamma
      (.mk ((opOp (LocalizedContext W)).obj X))
  let mY :=
    higherLocalizedModificationExtensionApp (W := W) Gamma
      (.mk ((opOp (LocalizedContext W)).obj Y))
  have hComp :
      higherLocalizedModificationNaturalityProperty (W := W) Gamma
        (e.hom ≫ e.inv) := by
    rw [e.hom_inv_id]
    exact
      higherLocalizedModificationNaturalityProperty_id
        (W := W) Gamma X
  have hp :
      F.map p ◁ mY ≫ (beta.naturality p).hom =
        (alpha.naturality p).hom ≫ mX ▷ G.map p := by
    simpa only
      [higherLocalizedModificationNaturalityProperty, p, mX, mY] using h
  have hpq :
      F.map (p ≫ q) ◁ mX ≫ (beta.naturality (p ≫ q)).hom =
        (alpha.naturality (p ≫ q)).hom ≫
          mX ▷ G.map (p ≫ q) := by
    simpa only
      [higherLocalizedModificationNaturalityProperty, Functor.map_comp,
        Quiver.Hom.comp_toLoc, p, q, mX] using hComp
  change
    F.map q ◁ mX ≫ (beta.naturality q).hom =
      (alpha.naturality q).hom ≫ mY ▷ G.map q
  letI : (F.map p).toFunctor.IsEquivalence := by
    simpa only [p] using
      higherLocalizedMap_isEquivalence_of_iso (W := W) F e
  have hWhisker :
      F.map p ◁
          (F.map q ◁ mX ≫ (beta.naturality q).hom) =
        F.map p ◁
          ((alpha.naturality q).hom ≫ mY ▷ G.map q) := by
    simp only [Pseudofunctor.StrongTrans.naturality_comp_hom] at hpq
    simpa [hp] using hpq
  apply Cat.Hom₂.ext
  apply
    ((Functor.whiskeringLeft _ _ _).obj (F.map p).toFunctor).map_injective
  exact congrArg Cat.Hom₂.toNatTrans hWhisker

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

/-! ## Localization generation and fullness -/

/-- The modification-naturality property is stable under composition, packaged
in the typeclass form required by Mathlib's localization generator theorem. -/
instance higherLocalizedModificationNaturalityProperty_isStableUnderComposition
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta) :
    MorphismProperty.IsStableUnderComposition
      (higherLocalizedModificationNaturalityProperty (W := W) Gamma) where
  comp_mem f g hf hg :=
    higherLocalizedModificationNaturalityProperty_comp
      (W := W) Gamma f g hf hg

/-- The modification square holds for every morphism of the constructed
localization. Mathlib's generator theorem reduces this to the raw image-arrow
case and stability under inversion of isomorphisms. -/
theorem higherLocalizedModificationNaturalityProperty_eq_top
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta) :
    higherLocalizedModificationNaturalityProperty (W := W) Gamma = ⊤ := by
  exact
    Localization.Construction.morphismProperty_eq_top'
      (W := W)
      (higherLocalizedModificationNaturalityProperty (W := W) Gamma)
      (fun {_ _} f =>
        higherLocalizedModificationNaturalityProperty_map
          (W := W) Gamma f)
      (fun {_ _} e he =>
        higherLocalizedModificationNaturalityProperty_inv
          (W := W) Gamma e he)

/-- Pointwise form of the preceding top-property theorem. -/
theorem higherLocalizedModificationNaturalityProperty_all
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta)
    {X Y : LocalizedContext W}
    (f : X ⟶ Y) :
    higherLocalizedModificationNaturalityProperty (W := W) Gamma f := by
  rw [higherLocalizedModificationNaturalityProperty_eq_top
    (W := W) Gamma]
  exact MorphismProperty.top_apply f

/-- Extend an arbitrary raw modification uniquely at the object-component level
to a modification between the localized StrongTrans. Naturality for an
arbitrary locally-discrete 1-cell is the all-morphisms result above, transported
through the double-opposite equivalence. -/
noncomputable def higherLocalizedModificationExtension
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta) :
    alpha ⟶ beta := by
  refine ⟨{
    app := higherLocalizedModificationExtensionApp (W := W) Gamma
    naturality := ?_
  }⟩
  intro X Y f
  let g := f.as.unop.unop
  have hg :=
    higherLocalizedModificationNaturalityProperty_all
      (W := W) Gamma g
  simpa [higherLocalizedModificationNaturalityProperty, g] using hg

/-- Restricting the canonical localized extension recovers the original raw
modification exactly. -/
@[simp] theorem restrictHigherLocalizedModification_extension
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma :
      restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
        restrictHigherLocalizedStrongTrans (W := W) beta) :
    restrictHigherLocalizedModification
        (W := W)
        (higherLocalizedModificationExtension (W := W) Gamma) =
      Gamma := by
  apply Pseudofunctor.StrongTrans.homCategory.ext
  rintro ⟨X⟩
  exact
    higherLocalizedModificationExtensionApp_presentation
      (W := W) Gamma X

/-- Restriction along the presentation unit is full on every StrongTrans hom
category. Together with v4.93 faithfulness, all modification-level extension
obligations are now unconditional. -/
theorem higherLocalizedRestrictionHomFunctor_full
    (F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)) :
    (higherLocalizedRestrictionHomFunctor (W := W) F G).Full where
  map_surjective {alpha beta} Gamma := by
    refine
      ⟨higherLocalizedModificationExtension (W := W) Gamma, ?_⟩
    change
      restrictHigherLocalizedModification
          (W := W)
          (higherLocalizedModificationExtension (W := W) Gamma) =
        Gamma
    exact
      restrictHigherLocalizedModification_extension
        (W := W) Gamma

/-- The v4.93 global ambient Full obligation is therefore theorem-level
unconditional. -/
theorem exactUniversalAmbientRestrictionHomFull
    (A : RefinementAtlas (LocalizedContext W)) :
    ExactUniversalAmbientRestrictionHomFull.{u, v, uH, vH}
      (W := W) A := by
  intro X Y
  exact
    higherLocalizedRestrictionHomFunctor_full
      (W := W)
      (higherStackObjectVal (W := W) A X)
      (higherStackObjectVal (W := W) A Y)

/-- With Faithful from v4.93 and Full from v4.94 both unconditional, local
restriction hom-equivalence is now equivalent to essential surjectivity alone. -/
theorem exactUniversalAmbientRestrictionHomEquivalence_iff_essSurj
    (A : RefinementAtlas (LocalizedContext W)) :
    ExactUniversalAmbientRestrictionHomEquivalence.{u, v, uH, vH}
        (W := W) A ↔
      ExactUniversalAmbientRestrictionHomEssSurj.{u, v, uH, vH}
        (W := W) A := by
  constructor
  · intro h
    exact
      ((exactUniversalAmbientRestrictionHomEquivalence_iff_full_essSurj
        (W := W) A).1 h).2
  · intro hEssSurj
    exact
      (exactUniversalAmbientRestrictionHomEquivalence_iff_full_essSurj
        (W := W) A).2
        ⟨exactUniversalAmbientRestrictionHomFull (W := W) A,
          hEssSurj⟩

/-- Essential surjectivity alone now suffices for canonical restriction
universality. -/
theorem exactUniversalAmbientRestrictionUniversality_of_homEssSurj
    (A : RefinementAtlas (LocalizedContext W))
    (hEssSurj :
      ExactUniversalAmbientRestrictionHomEssSurj.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientRestrictionUniversality.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientRestrictionUniversality_of_homFull_essSurj
    (W := W) A
    (exactUniversalAmbientRestrictionHomFull (W := W) A)
    hEssSurj

/-- Essential surjectivity alone now implies ambient object coverage. -/
theorem exactUniversalAmbientObjectCoverage_of_restrictionHomEssSurj
    (A : RefinementAtlas (LocalizedContext W))
    (hEssSurj :
      ExactUniversalAmbientRestrictionHomEssSurj.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientObjectCoverage.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientObjectCoverage_of_restrictionHomFull_essSurj
    (W := W) A
    (exactUniversalAmbientRestrictionHomFull (W := W) A)
    hEssSurj

/-- The current ambient Whitehead route is reduced to the single remaining
StrongTrans essential-surjectivity extension problem. -/
theorem exactUniversalAmbientWhiteheadExistence_of_restrictionHomEssSurj
    (A : RefinementAtlas (LocalizedContext W))
    (hEssSurj :
      ExactUniversalAmbientRestrictionHomEssSurj.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientWhiteheadExistence.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientWhiteheadExistence_of_restrictionHomFull_essSurj
    (W := W) A
    (exactUniversalAmbientRestrictionHomFull (W := W) A)
    hEssSurj

/-! ## Regression checks -/

variable
  (F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))

example :
    (higherLocalizedRestrictionHomFunctor (W := W) F G).Full :=
  higherLocalizedRestrictionHomFunctor_full (W := W) F G

#print axioms higherLocalizedModificationExtensionApp
#print axioms higherLocalizedModificationExtensionApp_presentation
#print axioms higherLocalizedModificationNaturalityProperty_comp
#print axioms higherLocalizedModificationNaturalityProperty_id
#print axioms higherLocalizedMap_isEquivalence_of_iso
#print axioms higherLocalizedModificationNaturalityProperty_inv
#print axioms higherLocalizedModificationNaturalityProperty_map
#print axioms higherLocalizedModificationNaturalityProperty_eq_top
#print axioms higherLocalizedModificationNaturalityProperty_all
#print axioms higherLocalizedModificationExtension
#print axioms restrictHigherLocalizedModification_extension
#print axioms higherLocalizedRestrictionHomFunctor_full
#print axioms exactUniversalAmbientRestrictionHomFull
#print axioms exactUniversalAmbientRestrictionHomEquivalence_iff_essSurj
#print axioms exactUniversalAmbientRestrictionUniversality_of_homEssSurj
#print axioms exactUniversalAmbientObjectCoverage_of_restrictionHomEssSurj
#print axioms exactUniversalAmbientWhiteheadExistence_of_restrictionHomEssSurj

end

end KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94
