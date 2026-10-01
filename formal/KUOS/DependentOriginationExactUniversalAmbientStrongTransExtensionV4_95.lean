import KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95

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
open KUOS.DependentOriginationExactUniversalAmbientRestrictionHomEquivalenceV4_92
open KUOS.DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93
open KUOS.DependentOriginationExactUniversalAmbientRestrictionFullV4_94

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Ambient StrongTrans extension reduction v4.95

v4.94 proves that restriction along the presentation unit is already full and
faithful on modifications.  The only remaining local hom-equivalence obligation
is therefore essential surjectivity on StrongTrans objects.

This file splits that one-cell problem one step further.

Mathlib's constructed localization is literally bijective on objects.  Hence the
object components of a raw StrongTrans after restriction extend canonically to
all localized objects, exactly as modification components did in v4.94.

What remains is not an object-level problem.  It is precisely the extension of

* the StrongTrans naturality isomorphism on every localized arrow;
* naturality with respect to 2-cells;
* identity coherence;
* composition coherence;

with agreement on arrows coming from the original context.

We package exactly those remaining fields.  Any such package produces a genuine
localized StrongTrans whose restriction is isomorphic to the original raw one.
Thus ambient essential surjectivity is reduced to this explicit coherence
extension problem.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Canonical extension of the object components of a raw StrongTrans. -/
noncomputable def higherLocalizedStrongTransExtensionApp
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (Y : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)) :
    F.obj Y ⟶ G.obj Y := by
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
  exact gamma.app (.mk X)

/-- On a presentation object, the canonical extension recovers the raw
StrongTrans component exactly. -/
@[simp] theorem higherLocalizedStrongTransExtensionApp_presentation
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (X : Context) :
    higherLocalizedStrongTransExtensionApp (W := W) gamma
        (.mk ((higherPresentationUnitFunctor W).obj X)) =
      gamma.app (.mk X) := by
  rfl

/-- The genuine remaining data needed to extend a raw StrongTrans once its
object components have been fixed canonically.

The final field stores the exact forward modification-naturality square on
every raw arrow.  This is the shape required directly by
`Pseudofunctor.StrongTrans.isoMk`; keeping that square rather than first
compressing it to an equality of naturality components avoids dependent
coercion and whiskering-normal-form artifacts. -/
structure HigherLocalizedStrongTransCoherenceExtension
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G) where
  naturality
      {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
      (f : a ⟶ b) :
      F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f
  naturality_naturality
      {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
      {f g : a ⟶ b} (eta : f ⟶ g) :
      F.map₂ eta ▷ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≫
          (naturality g).hom =
        (naturality f).hom ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ◁ G.map₂ eta
  naturality_id
      (a : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)) :
      (naturality (𝟙 a)).hom ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ◁
            (G.mapId a).hom =
        (F.mapId a).hom ▷
            higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫
          (λ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)).hom ≫
          (ρ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)).inv
  naturality_comp
      {a b c : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
      (f : a ⟶ b) (g : b ⟶ c) :
      (naturality (f ≫ g)).hom ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ◁
            (G.mapComp f g).hom =
        (F.mapComp f g).hom ▷
            higherLocalizedStrongTransExtensionApp (W := W) gamma c ≫
          (α_ _ _ _).hom ≫
          F.map f ◁ (naturality g).hom ≫
          (α_ _ _ _).inv ≫
          (naturality f).hom ▷ G.map g ≫
          (α_ _ _ _).hom
  restrict_modification_naturality
      {X Y : LocallyDiscrete Context} (f : X ⟶ Y) :
      (restrictHigherLocalizedSystem W F).map f ◁
            𝟙
              (higherLocalizedStrongTransExtensionApp (W := W) gamma
                ((higherPresentationUnitFunctor W).toPseudofunctor.obj Y)) ≫
          (gamma.naturality f).hom =
        (naturality
            ((higherPresentationUnitFunctor W).toPseudofunctor.map f)).hom ≫
          𝟙
              (higherLocalizedStrongTransExtensionApp (W := W) gamma
                ((higherPresentationUnitFunctor W).toPseudofunctor.obj X)) ▷
            (restrictHigherLocalizedSystem W G).map f

/-- Assemble the preceding extension data into a genuine localized StrongTrans. -/
noncomputable def HigherLocalizedStrongTransCoherenceExtension.toStrongTrans
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G}
    (D : HigherLocalizedStrongTransCoherenceExtension (W := W) gamma) :
    F ⟶ G where
  app := higherLocalizedStrongTransExtensionApp (W := W) gamma
  naturality := D.naturality
  naturality_naturality := D.naturality_naturality
  naturality_id := D.naturality_id
  naturality_comp := D.naturality_comp

/-- Restricting a StrongTrans assembled from extension data is isomorphic to the
original raw StrongTrans.  The object components of the modification are
identities; its naturality is exactly the stored image-arrow compatibility. -/
noncomputable def HigherLocalizedStrongTransCoherenceExtension.restrictionIso
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G}
    (D : HigherLocalizedStrongTransCoherenceExtension (W := W) gamma) :
    restrictHigherLocalizedStrongTrans
        (W := W) D.toStrongTrans ≅ gamma := by
  refine Pseudofunctor.StrongTrans.isoMk (fun X => ?_) ?_
  · rcases X with ⟨X⟩
    exact Iso.refl _
  · rintro ⟨X⟩ ⟨Y⟩ ⟨f⟩
    simpa only [restrictHigherLocalizedStrongTrans,
      HigherLocalizedStrongTransCoherenceExtension.toStrongTrans,
      Iso.refl_hom] using
      D.restrict_modification_naturality f.toLoc

/-- Existence of coherent StrongTrans extension data for every raw StrongTrans
between one pair of localized systems. -/
def HigherLocalizedStrongTransExtensionExists
    (F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)) : Prop :=
  ∀ gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G,
    Nonempty (HigherLocalizedStrongTransCoherenceExtension (W := W) gamma)

/-- The explicit StrongTrans coherence-extension condition implies essential
surjectivity of restriction on the corresponding hom category. -/
theorem higherLocalizedRestrictionHomFunctor_essSurj_of_extensionExists
    (F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))
    (hExt : HigherLocalizedStrongTransExtensionExists (W := W) F G) :
    (higherLocalizedRestrictionHomFunctor (W := W) F G).EssSurj where
  mem_essImage gamma := by
    rcases hExt gamma with ⟨D⟩
    exact
      ⟨D.toStrongTrans,
        ⟨D.restrictionIso⟩⟩

/-- Ambient version of the remaining coherence-extension obligation. -/
def ExactUniversalAmbientRestrictionStrongTransExtension
    (A : RefinementAtlas (LocalizedContext W)) : Prop :=
  ∀
    X Y :
      DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A,
    HigherLocalizedStrongTransExtensionExists
      (W := W)
      (higherStackObjectVal (W := W) A X)
      (higherStackObjectVal (W := W) A Y)

/-- The v4.95 extension condition discharges the sole remaining v4.94
essential-surjectivity obligation. -/
theorem exactUniversalAmbientRestrictionHomEssSurj_of_strongTransExtension
    (A : RefinementAtlas (LocalizedContext W))
    (hExt :
      ExactUniversalAmbientRestrictionStrongTransExtension.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientRestrictionHomEssSurj.{u, v, uH, vH}
      (W := W) A := by
  intro X Y
  exact
    higherLocalizedRestrictionHomFunctor_essSurj_of_extensionExists
      (W := W)
      (higherStackObjectVal (W := W) A X)
      (higherStackObjectVal (W := W) A Y)
      (hExt X Y)

/-- Consequently the explicit StrongTrans coherence-extension condition already
implies ambient Whitehead existence through v4.94. -/
theorem exactUniversalAmbientWhiteheadExistence_of_strongTransExtension
    (A : RefinementAtlas (LocalizedContext W))
    (hExt :
      ExactUniversalAmbientRestrictionStrongTransExtension.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientWhiteheadExistence.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientWhiteheadExistence_of_restrictionHomEssSurj
    (W := W) A
    (exactUniversalAmbientRestrictionHomEssSurj_of_strongTransExtension
      (W := W) A hExt)

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransExtensionApp
#print axioms higherLocalizedStrongTransExtensionApp_presentation
#print axioms HigherLocalizedStrongTransCoherenceExtension.toStrongTrans
#print axioms HigherLocalizedStrongTransCoherenceExtension.restrictionIso
#print axioms higherLocalizedRestrictionHomFunctor_essSurj_of_extensionExists
#print axioms exactUniversalAmbientRestrictionHomEssSurj_of_strongTransExtension
#print axioms exactUniversalAmbientWhiteheadExistence_of_strongTransExtension

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
