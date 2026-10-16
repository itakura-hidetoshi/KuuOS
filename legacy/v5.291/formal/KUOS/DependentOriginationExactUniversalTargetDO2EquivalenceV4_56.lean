import KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
import KUOS.DependentOriginationExactUniversalTargetMutualUniquenessV4_54
import KUOS.DependentOriginationHigherStackCarrierV2_9
import Mathlib.CategoryTheory.Bicategory.Adjunction.Basic
import Mathlib.CategoryTheory.Bicategory.InducedBicategory
import Mathlib

namespace KUOS.DependentOriginationExactUniversalTargetDO2EquivalenceV4_56

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactPresentationComparisonV4_52
open KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
open KUOS.DependentOriginationExactUniversalTargetMutualUniquenessV4_54
open KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Exact universal targets are equivalent in DO₂ v4.56

v4.54 proves fixed-raw-system mutual coherent uniqueness:

  Q₁ --> Q₂,
  Q₂ --> Q₁,

with both composites isomorphic by invertible modification to the corresponding
coherent identity comparison.

v4.55 then proves the required naturality layer under coherent equivalences of
raw higher contextual systems.

The roadmap boundary is therefore satisfied.  This file now promotes the v4.54
mutual coherent uniqueness datum to an actual Mathlib bicategorical adjoint
equivalence in the full induced bicategory DO₂.

No equivalence is asserted for arbitrary exact presentations.  Both objects
must be exact coherent universal targets.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Mutual coherent uniqueness data canonically determine an actual adjoint
equivalence of the corresponding DO₂ carriers.

The underlying 1-cells are the DO₂ lifts of the coherent comparisons.  The unit
is the inverse of the left composite-to-identity modification, and the counit is
the right composite-to-identity modification.  Mathlib then adjointifies the
counit so that the triangle law holds. -/
noncomputable def completion2EquivalenceOfMutualCoherentUniqueness
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {Q₁ Q₂ : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (M : ExactUniversalTargetMutualCoherentUniqueness
      (W := W) A Q₁ Q₂) :
    Bicategory.Equivalence Q₁.carrier Q₂.carrier := by
  have hleft := M.left_identity
  change
    M.forward.hom ≫ M.backward.hom ≅
      𝟙 (higherStackObjectVal (W := W) A Q₁.carrier) at hleft

  have hright := M.right_identity
  change
    M.backward.hom ≫ M.forward.hom ≅
      𝟙 (higherStackObjectVal (W := W) A Q₂.carrier) at hright

  have unit :
      𝟙 Q₁.carrier ≅
        exactPresentationCoherentComparisonToCompletion2Hom
            (W := W) A M.forward ≫
          exactPresentationCoherentComparisonToCompletion2Hom
            (W := W) A M.backward := by
    apply CategoryTheory.Bicategory.InducedBicategory.isoMk
    change
      𝟙 (higherStackObjectVal (W := W) A Q₁.carrier) ≅
        M.forward.hom ≫ M.backward.hom
    exact hleft.symm

  have counit :
      exactPresentationCoherentComparisonToCompletion2Hom
          (W := W) A M.backward ≫
        exactPresentationCoherentComparisonToCompletion2Hom
          (W := W) A M.forward ≅
      𝟙 Q₂.carrier := by
    apply CategoryTheory.Bicategory.InducedBicategory.isoMk
    change
      M.backward.hom ≫ M.forward.hom ≅
        𝟙 (higherStackObjectVal (W := W) A Q₂.carrier)
    exact hright

  exact Bicategory.Equivalence.mkOfAdjointifyCounit unit counit

/-- Any two exact coherent universal targets for the same raw system are
adjoint-equivalent objects of DO₂. -/
theorem hasCompletion2Equivalence_of_universalTargets
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {Q₁ Q₂ : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (T₁ : ExactPresentationCoherentUniversalTarget
      (W := W) A Q₁)
    (T₂ : ExactPresentationCoherentUniversalTarget
      (W := W) A Q₂) :
    Nonempty (Bicategory.Equivalence Q₁.carrier Q₂.carrier) := by
  rcases
      hasMutualCoherentUniqueness_of_universalTargets
        (W := W) A T₁ T₂ with
    ⟨M⟩
  exact
    ⟨completion2EquivalenceOfMutualCoherentUniqueness
      (W := W) A M⟩

/-- Exact presentations obtained from any two coherent weak localization
universal properties with stack-complete chosen lifts are equivalent in DO₂. -/
theorem coherentUniversalPresentations_areCompletion2Equivalent
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (U₁ U₂ : CoherentWeakHigherLocalizationUniversalProperty
      (W := W) R)
    (hStack₁ :
      IsHigherGrothendieckDescentComplete W A U₁.chosen.lift)
    (hStack₂ :
      IsHigherGrothendieckDescentComplete W A U₂.chosen.lift) :
    Nonempty
      (Bicategory.Equivalence
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U₁ hStack₁).carrier
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U₂ hStack₂).carrier) := by
  exact
    hasCompletion2Equivalence_of_universalTargets
      (W := W) A
      (exactPresentationCoherentUniversalTargetOfCoherentUniversalProperty
        (W := W) A U₁ hStack₁)
      (exactPresentationCoherentUniversalTargetOfCoherentUniversalProperty
        (W := W) A U₂ hStack₂)

/-- Naturality plus universal-target uniqueness: transporting an R-universal
target along a coherent raw equivalence gives a DO₂ object equivalent to every
independently chosen S-universal target. -/
theorem transportedUniversalTarget_isCompletion2EquivalentToAnyTarget
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (TQ : ExactPresentationCoherentUniversalTarget
      (W := W) A Q)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A S)
    (TP : ExactPresentationCoherentUniversalTarget
      (W := W) A P) :
    Nonempty (Bicategory.Equivalence Q.carrier P.carrier) := by
  change
    Nonempty
      (Bicategory.Equivalence
        (transportExactPresentation (W := W) A E Q).carrier
        P.carrier)
  exact
    hasCompletion2Equivalence_of_universalTargets
      (W := W) A
      (transportExactUniversalTarget
        (W := W) A E Q TQ)
      TP

/-!
## Boundary after v4.56

The object-level exact universality spine now has all three layers:

1. fixed-R coherent essential uniqueness;
2. naturality under coherent raw equivalence;
3. actual bicategorical equivalence of universal targets inside DO₂.

The next frontier is no longer object uniqueness.  It is the mapping-property
layer:

* define the admissible source higher category/bicategory;
* construct the universal realization on general admissible morphisms;
* prove identity/composition coherence;
* assemble the final dependent-origination classification/mapping equivalence.

No claim about that final mapping property is made in this file.
-/

end

end KUOS.DependentOriginationExactUniversalTargetDO2EquivalenceV4_56
