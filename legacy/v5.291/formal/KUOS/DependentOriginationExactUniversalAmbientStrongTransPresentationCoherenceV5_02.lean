import KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationCoherenceV5_02

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Presentation StrongTrans identity/composition coherence v5.02

v4.97 fixes the canonical naturality isomorphism on every arrow in the image
of the presentation pseudofunctor.  v5.01 fixes the canonical localized
identity formula, while v4.99 fixes the canonical localized composition
formula.

Before comparing those localized formulas through the coherence of
`Pseudofunctor.comp`, we first record a cast-free boundary on the raw
presentation side:

* presentation naturality on an identity is exactly Mathlib's
  `StrongTrans.naturality_id_iso` formula for the restricted systems;
* presentation naturality on a composite is exactly Mathlib's
  `StrongTrans.naturality_comp_iso` formula for the restricted systems.

The corresponding hom equalities are stated in the exact shape of the
v4.96 `naturality_id` and `naturality_comp` fields, but at the restricted
presentation level.

These are the two relation cores corresponding to
`Localization.Construction.relations.id` and `.comp`.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- On a raw identity arrow, the v4.97 canonical presentation naturality is
exactly the standard StrongTrans identity formula for the restricted
pseudofunctors. -/
theorem higherLocalizedStrongTransPresentationNaturality_id_iso
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (X : LocallyDiscrete Context) :
    higherLocalizedStrongTransPresentationNaturality
        (W := W) gamma (𝟙 X) =
      Bicategory.whiskerRightIso
          ((restrictHigherLocalizedSystem W F).mapId X)
          (higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj X)) ≪≫
        (λ_
          (higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj X))) ≪≫
        (ρ_
          (higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj X))).symm ≪≫
        Bicategory.whiskerLeftIso
          (higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj X))
          ((restrictHigherLocalizedSystem W G).mapId X).symm := by
  rcases X with ⟨X⟩
  change gamma.naturality (𝟙 (.mk X)) = _
  simpa only [higherLocalizedStrongTransExtensionApp_presentation] using
    Pseudofunctor.StrongTrans.naturality_id_iso gamma (.mk X)

/-- Hom-form identity coherence for the canonical presentation choice. -/
theorem higherLocalizedStrongTransPresentationNaturality_id_coherence
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (X : LocallyDiscrete Context) :
    (higherLocalizedStrongTransPresentationNaturality
        (W := W) gamma (𝟙 X)).hom ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma
              ((higherPresentationUnitFunctor W).toPseudofunctor.obj X) ◁
            ((restrictHigherLocalizedSystem W G).mapId X).hom =
      ((restrictHigherLocalizedSystem W F).mapId X).hom ▷
          higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj X) ≫
        (λ_
          (higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj X))).hom ≫
        (ρ_
          (higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj X))).inv := by
  rcases X with ⟨X⟩
  change
    (gamma.naturality (𝟙 (.mk X))).hom ≫
          gamma.app (.mk X) ◁
            ((restrictHigherLocalizedSystem W G).mapId (.mk X)).hom =
      ((restrictHigherLocalizedSystem W F).mapId (.mk X)).hom ▷
          gamma.app (.mk X) ≫
        (λ_ (gamma.app (.mk X))).hom ≫
        (ρ_ (gamma.app (.mk X))).inv
  exact gamma.naturality_id (.mk X)

/-- On raw composable arrows, the v4.97 canonical presentation naturality of
their composite is exactly Mathlib's standard StrongTrans composition formula
for the restricted pseudofunctors. -/
theorem higherLocalizedStrongTransPresentationNaturality_comp_iso
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y Z : LocallyDiscrete Context}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    higherLocalizedStrongTransPresentationNaturality
        (W := W) gamma (f ≫ g) =
      Bicategory.whiskerRightIso
          ((restrictHigherLocalizedSystem W F).mapComp f g)
          (higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj Z)) ≪≫
        (α_ _ _ _) ≪≫
        Bicategory.whiskerLeftIso
          ((restrictHigherLocalizedSystem W F).map f)
          (higherLocalizedStrongTransPresentationNaturality
            (W := W) gamma g) ≪≫
        (α_ _ _ _).symm ≪≫
        Bicategory.whiskerRightIso
          (higherLocalizedStrongTransPresentationNaturality
            (W := W) gamma f)
          ((restrictHigherLocalizedSystem W G).map g) ≪≫
        (α_ _ _ _) ≪≫
        Bicategory.whiskerLeftIso
          (higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj X))
          ((restrictHigherLocalizedSystem W G).mapComp f g).symm := by
  rcases X with ⟨X⟩
  rcases Y with ⟨Y⟩
  rcases Z with ⟨Z⟩
  change gamma.naturality (f ≫ g) = _
  simpa only
      [higherLocalizedStrongTransExtensionApp_presentation,
        higherLocalizedStrongTransPresentationNaturality] using
    Pseudofunctor.StrongTrans.naturality_comp_iso gamma f g

/-- Hom-form composition coherence for the canonical presentation choice. -/
theorem higherLocalizedStrongTransPresentationNaturality_comp_coherence
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y Z : LocallyDiscrete Context}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (higherLocalizedStrongTransPresentationNaturality
        (W := W) gamma (f ≫ g)).hom ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma
              ((higherPresentationUnitFunctor W).toPseudofunctor.obj X) ◁
            ((restrictHigherLocalizedSystem W G).mapComp f g).hom =
      ((restrictHigherLocalizedSystem W F).mapComp f g).hom ▷
          higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj Z) ≫
        (α_ _ _ _).hom ≫
        (restrictHigherLocalizedSystem W F).map f ◁
          (higherLocalizedStrongTransPresentationNaturality
            (W := W) gamma g).hom ≫
        (α_ _ _ _).inv ≫
        (higherLocalizedStrongTransPresentationNaturality
            (W := W) gamma f).hom ▷
          (restrictHigherLocalizedSystem W G).map g ≫
        (α_ _ _ _).hom := by
  rcases X with ⟨X⟩
  rcases Y with ⟨Y⟩
  rcases Z with ⟨Z⟩
  change
    (gamma.naturality (f ≫ g)).hom ≫
          gamma.app (.mk X) ◁
            ((restrictHigherLocalizedSystem W G).mapComp f g).hom =
      ((restrictHigherLocalizedSystem W F).mapComp f g).hom ▷
          gamma.app (.mk Z) ≫
        (α_ _ _ _).hom ≫
        (restrictHigherLocalizedSystem W F).map f ◁
          (gamma.naturality g).hom ≫
        (α_ _ _ _).inv ≫
        (gamma.naturality f).hom ▷
          (restrictHigherLocalizedSystem W G).map g ≫
        (α_ _ _ _).hom
  exact gamma.naturality_comp f g

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransPresentationNaturality_id_iso
#print axioms higherLocalizedStrongTransPresentationNaturality_id_coherence
#print axioms higherLocalizedStrongTransPresentationNaturality_comp_iso
#print axioms higherLocalizedStrongTransPresentationNaturality_comp_coherence

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationCoherenceV5_02
