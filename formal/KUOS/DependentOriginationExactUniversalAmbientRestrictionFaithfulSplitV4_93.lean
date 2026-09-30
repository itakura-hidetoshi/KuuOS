import KUOS.DependentOriginationExactUniversalAmbientRestrictionHomEquivalenceV4_92

namespace KUOS.DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93

open CategoryTheory
open Opposite
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90
open KUOS.DependentOriginationExactUniversalAmbientRestrictionHomEquivalenceV4_92

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Ambient restriction faithfulness split v4.93

v4.92 reduces ambient object coverage to local equivalence of the restriction
functor on StrongTrans hom categories.

An equivalence of categories has three pieces:

* faithfulness;
* fullness;
* essential surjectivity.

The first piece is not an additional higher-localization hypothesis here.
Mathlib's constructed localization has a literal bijection on objects

  Context ≃ W.Localization,

and the KuuOS presentation unit is this localization object map followed by the
double-opposite functor. Hence every object of the localized locally-discrete
domain is literally in the image of the presentation unit.

A modification between StrongTrans is determined by its object components.
Therefore, if two localized modifications have the same restriction, they agree
on every localized object and are equal.

This file proves that restriction on each StrongTrans hom category is faithful
without assumptions. Consequently the v4.92 local-equivalence condition is
equivalent to only the two remaining obligations:

* Full: every raw modification between restricted StrongTrans extends;
* EssSurj: every raw StrongTrans is isomorphic to a restricted localized one.

This separates 2-cell extension from 1-cell extension and removes faithfulness
from the genuine P4 frontier.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The presentation-unit functor is surjective on objects for Mathlib's
constructed localization. The double-opposite variance does not change this. -/
theorem higherPresentationUnitFunctor_obj_surjective :
    Function.Surjective (higherPresentationUnitFunctor W).obj := by
  intro Y
  let Z : LocalizedContext W := unop (unop Y)
  let X : Context := (Localization.Construction.objEquiv W).symm Z
  refine ⟨X, ?_⟩
  change op (op (W.Q.obj X)) = Y
  have hX : W.Q.obj X = Z := by
    simpa [X] using
      (Localization.Construction.objEquiv W).apply_symm_apply Z
  rw [hX]
  rfl

/-- The same object-surjectivity after wrapping source and target categories as
locally discrete bicategories. -/
theorem higherPresentationUnitLocallyDiscrete_obj_surjective :
    Function.Surjective
      (fun X : Context =>
        (LocallyDiscrete.mk ((higherPresentationUnitFunctor W).obj X) :
          LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ))) := by
  intro Y
  rcases higherPresentationUnitFunctor_obj_surjective (W := W) Y.as with
    ⟨X, hX⟩
  refine ⟨X, ?_⟩
  apply LocallyDiscrete.ext
  exact hX

/-- Restriction along the presentation unit is faithful on every StrongTrans hom
category. No stack, exactness, or universal-property hypothesis is needed. -/
theorem higherLocalizedRestrictionHomFunctor_faithful
    (F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)) :
    (higherLocalizedRestrictionHomFunctor (W := W) F G).Faithful where
  map_injective {alpha beta} h := by
    apply Pseudofunctor.StrongTrans.homCategory.ext
    intro Y
    rcases
      higherPresentationUnitLocallyDiscrete_obj_surjective
        (W := W) Y with
      ⟨X, rfl⟩
    have hX :=
      congrArg
        (fun Gamma => Gamma.as.app (.mk X))
        h
    simpa only
      [higherLocalizedRestrictionHomFunctor_map,
        restrictHigherLocalizedModification_app] using hX

/-- The remaining modification-level obligation after unconditional
faithfulness: restriction must be full on every ambient StrongTrans hom
category. -/
def ExactUniversalAmbientRestrictionHomFull : Prop :=
  ∀
    X Y :
      DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A,
    (higherLocalizedRestrictionHomFunctor
      (W := W)
      (higherStackObjectVal (W := W) A X)
      (higherStackObjectVal (W := W) A Y)).Full

/-- The remaining one-cell-level obligation: every raw StrongTrans between the
restricted ambient pseudofunctors is isomorphic to the restriction of a
localized StrongTrans. -/
def ExactUniversalAmbientRestrictionHomEssSurj : Prop :=
  ∀
    X Y :
      DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A,
    (higherLocalizedRestrictionHomFunctor
      (W := W)
      (higherStackObjectVal (W := W) A X)
      (higherStackObjectVal (W := W) A Y)).EssSurj

/-- Because restriction is already faithful, the v4.92 local hom-equivalence
condition is exactly fullness plus essential surjectivity. -/
theorem exactUniversalAmbientRestrictionHomEquivalence_iff_full_essSurj :
    ExactUniversalAmbientRestrictionHomEquivalence.{u, v, uH, vH}
        (W := W) A ↔
      ExactUniversalAmbientRestrictionHomFull.{u, v, uH, vH}
          (W := W) A ∧
        ExactUniversalAmbientRestrictionHomEssSurj.{u, v, uH, vH}
          (W := W) A := by
  constructor
  · intro hLocal
    constructor
    · intro X Y
      exact (hLocal X Y).full
    · intro X Y
      exact (hLocal X Y).essSurj
  · rintro ⟨hFull, hEssSurj⟩ X Y
    exact
      { faithful :=
          higherLocalizedRestrictionHomFunctor_faithful
            (W := W)
            (higherStackObjectVal (W := W) A X)
            (higherStackObjectVal (W := W) A Y)
        full := hFull X Y
        essSurj := hEssSurj X Y }

/-- The split remaining obligations already imply the v4.91 canonical
restriction-universality condition. -/
theorem exactUniversalAmbientRestrictionUniversality_of_homFull_essSurj
    (hFull :
      ExactUniversalAmbientRestrictionHomFull.{u, v, uH, vH}
        (W := W) A)
    (hEssSurj :
      ExactUniversalAmbientRestrictionHomEssSurj.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientRestrictionUniversality.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientRestrictionUniversality_of_homEquivalence
    (W := W) A
    ((exactUniversalAmbientRestrictionHomEquivalence_iff_full_essSurj
      (W := W) A).2 ⟨hFull, hEssSurj⟩)

/-- The same split obligations discharge ambient object coverage. -/
theorem exactUniversalAmbientObjectCoverage_of_restrictionHomFull_essSurj
    (hFull :
      ExactUniversalAmbientRestrictionHomFull.{u, v, uH, vH}
        (W := W) A)
    (hEssSurj :
      ExactUniversalAmbientRestrictionHomEssSurj.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientObjectCoverage.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientObjectCoverage_of_restrictionHomEquivalence
    (W := W) A
    ((exactUniversalAmbientRestrictionHomEquivalence_iff_full_essSurj
      (W := W) A).2 ⟨hFull, hEssSurj⟩)

/-- Whitehead existence now depends only on the two genuine extension
obligations; faithfulness is theorem-level infrastructure. -/
theorem exactUniversalAmbientWhiteheadExistence_of_restrictionHomFull_essSurj
    (hFull :
      ExactUniversalAmbientRestrictionHomFull.{u, v, uH, vH}
        (W := W) A)
    (hEssSurj :
      ExactUniversalAmbientRestrictionHomEssSurj.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientWhiteheadExistence.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientWhiteheadExistence_of_restrictionHomEquivalence
    (W := W) A
    ((exactUniversalAmbientRestrictionHomEquivalence_iff_full_essSurj
      (W := W) A).2 ⟨hFull, hEssSurj⟩)

/-! ## Regression checks -/

variable
  (F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W))

example :
    (higherLocalizedRestrictionHomFunctor (W := W) F G).Faithful :=
  higherLocalizedRestrictionHomFunctor_faithful (W := W) F G

example
    (hFull :
      ExactUniversalAmbientRestrictionHomFull.{u, v, uH, vH}
        (W := W) A)
    (hEssSurj :
      ExactUniversalAmbientRestrictionHomEssSurj.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientRestrictionHomEquivalence.{u, v, uH, vH}
      (W := W) A :=
  (exactUniversalAmbientRestrictionHomEquivalence_iff_full_essSurj
    (W := W) A).2 ⟨hFull, hEssSurj⟩

#print axioms higherPresentationUnitFunctor_obj_surjective
#print axioms higherPresentationUnitLocallyDiscrete_obj_surjective
#print axioms higherLocalizedRestrictionHomFunctor_faithful
#print axioms exactUniversalAmbientRestrictionHomEquivalence_iff_full_essSurj
#print axioms exactUniversalAmbientRestrictionUniversality_of_homFull_essSurj
#print axioms exactUniversalAmbientObjectCoverage_of_restrictionHomFull_essSurj
#print axioms exactUniversalAmbientWhiteheadExistence_of_restrictionHomFull_essSurj

end

end KUOS.DependentOriginationExactUniversalAmbientRestrictionFaithfulSplitV4_93
