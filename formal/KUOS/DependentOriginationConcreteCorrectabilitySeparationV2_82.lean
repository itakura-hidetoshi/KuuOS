import KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81

namespace KUOS.DependentOriginationConcreteCorrectabilitySeparationV2_82

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81

universe u

/-!
# Concrete correctability separation v2.82

The v2.81 bridge kept the distinction between non-flatness and hard
obstruction conditional on an externally supplied robust correction witness.
This layer closes that logical gap with an explicit correction realization.

For any defect carrier, the identity realization uses the defect itself as the
correction parameter and admits every parameter.  Applied to the octahedral
v2.69 countermodel, this gives a concrete generated loop which is simultaneously

* non-flat for every filtration separated at the reflexive automorphism,
* explicitly correctable, and therefore
* not a hard obstruction for this supplied correction mechanism.

The theorem is deliberately existential in the correction mechanism.  It does
not assert that every physically or semantically meaningful correction system
admits the defect.
-/

/-- The identity correction realization: a defect is realized by selecting
that defect itself as an admissible correction parameter. -/
def identityCorrectionRealization (D : Type u) :
    CorrectionRealization Unit D D where
  admissible := fun _ _ => True
  effect := fun _ d => d

/-- Every defect is explicitly correctable for the identity realization. -/
theorem identityCorrectionRealization_correctable
    (D : Type u) (d : D) :
    (identityCorrectionRealization D).CorrectableAt () d := by
  exact ⟨d, True.intro, rfl⟩

/-- The concrete octahedral generated holonomy is correctable for the identity
realization, with no flatness assumption. -/
theorem counterGeneratedLoop_correctable_of_identity
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    GeneratedHolonomyCorrectable
      allMorphisms counterSystem D
      (identityCorrectionRealization (CounterHolonomyCarrier D))
      () counterGeneratedLoop := by
  exact identityCorrectionRealization_correctable
    (CounterHolonomyCarrier D)
    (generatedHolonomy allMorphisms counterSystem D counterGeneratedLoop)

/-- Concrete separation theorem: the same generated loop is non-flat and
correctable, hence it is not a hard obstruction for the explicit identity
correction realization. -/
theorem counterGeneratedLoop_nonflat_correctable_not_hard
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : ObstructionFiltration (CounterHolonomyCarrier D))
    (hsep : F.SeparatedAt (Iso.refl _)) :
    (¬ FilteredGeneratedHolonomyFlat
        allMorphisms counterSystem D F counterGeneratedLoop) ∧
      GeneratedHolonomyCorrectable
        allMorphisms counterSystem D
        (identityCorrectionRealization (CounterHolonomyCarrier D))
        () counterGeneratedLoop ∧
      ¬ GeneratedHolonomyHardObstruction
        allMorphisms counterSystem D
        (identityCorrectionRealization (CounterHolonomyCarrier D))
        () counterGeneratedLoop := by
  have hnonflat :
      ¬ FilteredGeneratedHolonomyFlat
        allMorphisms counterSystem D F counterGeneratedLoop :=
    counterGeneratedLoop_not_flat_of_separated D F hsep
  have hcorrectable :
      GeneratedHolonomyCorrectable
        allMorphisms counterSystem D
        (identityCorrectionRealization (CounterHolonomyCarrier D))
        () counterGeneratedLoop :=
    counterGeneratedLoop_correctable_of_identity D
  refine ⟨hnonflat, hcorrectable, ?_⟩
  intro hhard
  exact hhard hcorrectable

/-- In the concrete octahedral model, non-flatness does not force hard
obstruction for the explicit identity correction realization. -/
theorem counterGeneratedLoop_nonflat_not_imply_hard
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : ObstructionFiltration (CounterHolonomyCarrier D))
    (hsep : F.SeparatedAt (Iso.refl _)) :
    ¬ ((¬ FilteredGeneratedHolonomyFlat
          allMorphisms counterSystem D F counterGeneratedLoop) →
        GeneratedHolonomyHardObstruction
          allMorphisms counterSystem D
          (identityCorrectionRealization (CounterHolonomyCarrier D))
          () counterGeneratedLoop) := by
  intro hforce
  have hnonflat :
      ¬ FilteredGeneratedHolonomyFlat
        allMorphisms counterSystem D F counterGeneratedLoop :=
    counterGeneratedLoop_not_flat_of_separated D F hsep
  have hhard := hforce hnonflat
  exact hhard (counterGeneratedLoop_correctable_of_identity D)

end KUOS.DependentOriginationConcreteCorrectabilitySeparationV2_82
