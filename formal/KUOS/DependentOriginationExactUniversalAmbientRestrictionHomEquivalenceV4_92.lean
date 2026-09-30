import KUOS.DependentOriginationExactUniversalAmbientRestrictionUniversalityV4_91

namespace KUOS.DependentOriginationExactUniversalAmbientRestrictionHomEquivalenceV4_92

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactPresentationComparisonV4_52
open KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89
open KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90
open KUOS.DependentOriginationExactUniversalAmbientRestrictionUniversalityV4_91

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Ambient restriction hom-equivalence reduction v4.92

v4.91 shows that ambient object coverage follows if every ambient DO₂ object Z
has a tautological restriction presentation which is a coherent universal
target.

This file resolves that universal-target structure into a local bicategorical
localization condition.

For localized Cat-valued pseudofunctors F and G, restriction along the
presentation-localization unit acts on

* StrongTrans objects by restrictHigherLocalizedStrongTrans;
* modifications by restrictHigherLocalizedModification.

The v4.59 identity and composition laws make this a genuine functor between
StrongTrans hom categories.

If this restriction functor is an equivalence of categories for every pair of
ambient stack carriers, then the tautological restriction presentation of every
ambient Z is universal:

* essential surjectivity lifts the raw comparison of any exact presentation P
  to a localized StrongTrans P.carrier --> Z;
* full faithfulness lifts an isomorphism between the restricted StrongTrans of
  any two such factors back to an isomorphism between the localized factors.

Thus the remaining P4 object-coverage obligation is reduced to the local
hom-equivalence part of a bicategorical presentation-localization theorem.
This is strictly stronger than ordinary 1-categorical localization and is not
asserted unconditionally here.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Restriction along the presentation unit as a functor on one StrongTrans
hom category. -/
noncomputable def higherLocalizedRestrictionHomFunctor
    (F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)) :
    (F ⟶ G) ⥤
      (restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G) where
  obj alpha :=
    restrictHigherLocalizedStrongTrans (W := W) alpha
  map Gamma :=
    restrictHigherLocalizedModification (W := W) Gamma
  map_id alpha :=
    restrictHigherLocalizedModification_id (W := W) alpha
  map_comp eta theta :=
    restrictHigherLocalizedModification_comp (W := W) eta theta

@[simp] theorem higherLocalizedRestrictionHomFunctor_obj
    (F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))
    (alpha : F ⟶ G) :
    (higherLocalizedRestrictionHomFunctor (W := W) F G).obj alpha =
      restrictHigherLocalizedStrongTrans (W := W) alpha :=
  rfl

@[simp] theorem higherLocalizedRestrictionHomFunctor_map
    (F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))
    {alpha beta : F ⟶ G}
    (Gamma : alpha ⟶ beta) :
    (higherLocalizedRestrictionHomFunctor (W := W) F G).map Gamma =
      restrictHigherLocalizedModification (W := W) Gamma :=
  rfl

/-- Local bicategorical localization condition needed by the v4.91 canonical
restriction construction: restriction is an equivalence on every hom category
between ambient stack carriers.

As in v4.91, vH occurs only inside the proposition body, so callers should pin
the universe application explicitly. -/
def ExactUniversalAmbientRestrictionHomEquivalence : Prop :=
  ∀
    X Y :
      DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A,
    (higherLocalizedRestrictionHomFunctor
      (W := W)
      (higherStackObjectVal (W := W) A X)
      (higherStackObjectVal (W := W) A Y)).IsEquivalence

/-- Under local hom-equivalence, the tautological restriction presentation of
one ambient object is a coherent universal target. -/
theorem exactUniversalAmbientRestrictionPresentation_isUniversal_of_homEquivalence
    (hLocal :
      ExactUniversalAmbientRestrictionHomEquivalence.{u, v, uH, vH}
        (W := W) A)
    (Z :
      DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A) :
    ExactPresentationCoherentUniversalTarget
      (W := W) A
      (exactUniversalAmbientRestrictionPresentation
        (W := W) A Z) := by
  refine
    { factor := ?_
      essential_unique := ?_ }
  · intro P
    let F :=
      higherStackObjectVal (W := W) A P.carrier
    let G :=
      higherStackObjectVal (W := W) A Z
    let Rfun :=
      higherLocalizedRestrictionHomFunctor (W := W) F G
    letI : Rfun.IsEquivalence := by
      dsimp [Rfun, F, G]
      exact hLocal P.carrier Z
    let e := Rfun.asEquivalence
    let alphaHom : F ⟶ G :=
      e.inverse.obj P.comparison
    refine
      ⟨{
        hom := alphaHom
        comparison_triangle := ?_
      }⟩
    change
      (restrictHigherLocalizedStrongTrans (W := W) alphaHom ≫
        𝟙 _) ≅ P.comparison
    exact
      Bicategory.rightUnitor
          (restrictHigherLocalizedStrongTrans (W := W) alphaHom) ≪≫
        e.counitIso.app P.comparison
  · intro P alpha beta
    let F :=
      higherStackObjectVal (W := W) A P.carrier
    let G :=
      higherStackObjectVal (W := W) A Z
    let Rfun :=
      higherLocalizedRestrictionHomFunctor (W := W) F G
    letI : Rfun.IsEquivalence := by
      dsimp [Rfun, F, G]
      exact hLocal P.carrier Z
    have hAlpha := alpha.comparison_triangle
    have hBeta := beta.comparison_triangle
    change
      (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
        𝟙 _) ≅ P.comparison at hAlpha
    change
      (restrictHigherLocalizedStrongTrans (W := W) beta.hom ≫
        𝟙 _) ≅ P.comparison at hBeta
    have hRestricted :
        restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≅
          restrictHigherLocalizedStrongTrans (W := W) beta.hom :=
      (Bicategory.rightUnitor
          (restrictHigherLocalizedStrongTrans (W := W) alpha.hom)).symm ≪≫
        hAlpha ≪≫
        hBeta.symm ≪≫
        Bicategory.rightUnitor
          (restrictHigherLocalizedStrongTrans (W := W) beta.hom)
    have hMapped : Rfun.obj alpha.hom ≅ Rfun.obj beta.hom := by
      exact hRestricted
    exact ⟨Rfun.preimageIso hMapped⟩

/-- Local hom-equivalence for ambient stack carriers implies the v4.91 uniform
restriction-universality condition. -/
theorem exactUniversalAmbientRestrictionUniversality_of_homEquivalence
    (hLocal :
      ExactUniversalAmbientRestrictionHomEquivalence.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientRestrictionUniversality.{u, v, uH, vH}
      (W := W) A := by
  intro Z
  exact
    ⟨exactUniversalAmbientRestrictionPresentation_isUniversal_of_homEquivalence
      (W := W) A hLocal Z⟩

/-- Consequently the local hom-equivalence condition discharges ambient object
coverage. -/
theorem exactUniversalAmbientObjectCoverage_of_restrictionHomEquivalence
    (hLocal :
      ExactUniversalAmbientRestrictionHomEquivalence.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientObjectCoverage.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientObjectCoverage_of_restrictionUniversality.{u, v, uH, vH}
    (W := W) A
    (exactUniversalAmbientRestrictionUniversality_of_homEquivalence
      (W := W) A hLocal)

/-- The actual v4.70 realization therefore has ambient Whitehead data whenever
restriction is locally an equivalence on ambient StrongTrans hom categories. -/
def exactUniversalAmbientWhiteheadBiequivalenceOfRestrictionHomEquivalence
    (hLocal :
      ExactUniversalAmbientRestrictionHomEquivalence.{u, v, uH, vH}
        (W := W) A) :
    WhiteheadBiequivalenceData
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      (DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A) :=
  exactUniversalAmbientWhiteheadBiequivalenceOfCoverage.{u, v, uH, vH}
    (W := W) A
    (exactUniversalAmbientObjectCoverage_of_restrictionHomEquivalence
      (W := W) A hLocal)

/-- Existence-shaped endpoint matching the v4.90 ambient reduction. -/
theorem exactUniversalAmbientWhiteheadExistence_of_restrictionHomEquivalence
    (hLocal :
      ExactUniversalAmbientRestrictionHomEquivalence.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientWhiteheadExistence.{u, v, uH, vH}
      (W := W) A :=
  (exactUniversalAmbientWhiteheadExistence_iff_objectCoverage.{u, v, uH, vH}
    (W := W) A).2
    (exactUniversalAmbientObjectCoverage_of_restrictionHomEquivalence
      (W := W) A hLocal)

/-! ## Regression checks -/

variable
  (X Y :
    DependentOriginationCompletion2.{u, v, uH, uH, vH}
      (W := W) A)

example :
    (higherLocalizedRestrictionHomFunctor
      (W := W)
      (higherStackObjectVal (W := W) A X)
      (higherStackObjectVal (W := W) A Y)).obj
        (𝟙 (higherStackObjectVal (W := W) A X)) =
      restrictHigherLocalizedStrongTrans
        (W := W) (𝟙 (higherStackObjectVal (W := W) A X)) := by
  rfl

example
    (hLocal :
      ExactUniversalAmbientRestrictionHomEquivalence.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientRestrictionUniversality.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientRestrictionUniversality_of_homEquivalence
    (W := W) A hLocal

#print axioms higherLocalizedRestrictionHomFunctor
#print axioms exactUniversalAmbientRestrictionPresentation_isUniversal_of_homEquivalence
#print axioms exactUniversalAmbientRestrictionUniversality_of_homEquivalence
#print axioms exactUniversalAmbientObjectCoverage_of_restrictionHomEquivalence
#print axioms exactUniversalAmbientWhiteheadBiequivalenceOfRestrictionHomEquivalence
#print axioms exactUniversalAmbientWhiteheadExistence_of_restrictionHomEquivalence

end

end KUOS.DependentOriginationExactUniversalAmbientRestrictionHomEquivalenceV4_92
