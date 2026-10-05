import KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31
import KUOS.DependentOriginationExactClassificationFactorExistenceV5_19
import KUOS.DependentOriginationExactLiftabilityCriterionV5_18
import Mathlib

namespace KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftabilityCriterionV5_18
open KUOS.DependentOriginationExactClassificationFactorExistenceV5_19

set_option autoImplicit false

noncomputable section

/-!
# Aligned exact-liftability collapse v5.32

v5.19 already specializes the refinement atlas to
`RefinementAtlas.{u, max u v, uH}`, while the raw system takes values in
`Cat.{vH, uH}`.  Under exactly that aligned specialization, the v5.18
stack-factorization criterion has the same universe parameters as the v5.19
ambient-aligned criterion.

This theorem unit proves only that specialized collapse.  It does not assert
that an arbitrary atlas with a different index universe can be reindexed.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

theorem exactLiftabilityCriterion_implies_ambientAligned_of_alignedAtlas
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context))
    (hExact :
      ExactLiftabilityCriterion
        (W := W) A R) :
    AmbientAlignedExactLiftabilityCriterion.{u, v, uH, vH}
      (W := W) A R := by
  have hStack :
      HasHigherStackLocalizationFactorization
        (W := W) A R :=
    (exactLiftabilityCriterion_iff_stackFactorization
      (W := W) A R).1 hExact
  change
    Nonempty
      (HigherStackLocalizationFactorization.{u, v, uH, uH, vH}
        (W := W) A R)
  exact hStack

theorem exactLiftabilityCriterion_iff_ambientAligned_of_alignedAtlas
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) :
    ExactLiftabilityCriterion
        (W := W) A R ↔
      AmbientAlignedExactLiftabilityCriterion.{u, v, uH, vH}
        (W := W) A R := by
  constructor
  · exact
      exactLiftabilityCriterion_implies_ambientAligned_of_alignedAtlas
        (W := W) A R
  · exact
      ambientAlignedExactLiftabilityCriterion_implies_exactLiftabilityCriterion
        (W := W) A R

theorem ExactLiftableClassificationObject.exists_labelPreserving_exactUniversalSource
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ∃ Y :
        ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel,
      Y.label = X.label ∧
        Nonempty
          (HigherPointwiseEquivalenceComparison
            Y.source.raw X.raw) := by
  have hExact :
      ExactLiftabilityCriterion (W := W) A X.raw :=
    KUOS.DependentOriginationExactLiftabilityCriterionV5_18.
      ExactLiftableClassificationObject.satisfiesExactLiftabilityCriterion
        (W := W) A X
  have hAligned :
      AmbientAlignedExactLiftabilityCriterion.{u, v, uH, vH}
        (W := W) A X.raw :=
    exactLiftabilityCriterion_implies_ambientAligned_of_alignedAtlas
      (W := W) A X.raw hExact
  exact
    KUOS.DependentOriginationExactClassificationFactorExistenceV5_19.
      ExactLiftableClassificationObject.exists_labelPreserving_exactUniversalSource_of_ambientAligned
        (W := W) A X hAligned

theorem WeakSemanticClassificationObject.exists_labelPreserving_exactUniversalSource_of_exactCriterion
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) WorldLabel PresentationLabel)
    (hExact :
      ExactLiftabilityCriterion
        (W := W) A X.raw) :
    ∃ Y :
        ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel,
      Y.label = X.label ∧
        Nonempty
          (HigherPointwiseEquivalenceComparison
            Y.source.raw X.raw) := by
  have hAligned :
      AmbientAlignedExactLiftabilityCriterion.{u, v, uH, vH}
        (W := W) A X.raw :=
    exactLiftabilityCriterion_implies_ambientAligned_of_alignedAtlas
      (W := W) A X.raw hExact
  exact
    KUOS.DependentOriginationExactClassificationFactorExistenceV5_19.
      WeakSemanticClassificationObject.exists_labelPreserving_exactUniversalSource_of_ambientAligned
        (W := W) A X hAligned

/-!
The weak-semantic boundary is unchanged: v5.18 already proves by the octahedral
counterSystem that weak admissibility alone does not imply exact liftability.
Only the extra aligned witness from v5.19 has been removed under the atlas
universe specialization already assumed there.
-/

#print axioms exactLiftabilityCriterion_implies_ambientAligned_of_alignedAtlas
#print axioms exactLiftabilityCriterion_iff_ambientAligned_of_alignedAtlas
#print axioms ExactLiftableClassificationObject.exists_labelPreserving_exactUniversalSource
#print axioms WeakSemanticClassificationObject.exists_labelPreserving_exactUniversalSource_of_exactCriterion

end

end KUOS.DependentOriginationAlignedExactLiftabilityCollapseV5_32
