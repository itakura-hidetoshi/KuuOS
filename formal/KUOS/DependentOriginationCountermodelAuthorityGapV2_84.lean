import KUOS.DependentOriginationCorrectionAuthorityRefinementV2_83

namespace KUOS.DependentOriginationCountermodelAuthorityGapV2_84

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81
open KUOS.DependentOriginationConcreteCorrectabilitySeparationV2_82
open KUOS.DependentOriginationCorrectionAuthorityRefinementV2_83

/-!
# Concrete correction-authority gap v2.84

The v2.83 layer proves abstract monotonicity under widening of correction
authority.  This file realizes a strict authority gap on the octahedral v2.69
countermodel.

The narrow authority admits only the reflexive automorphism as a correction
parameter.  The wide identity authority admits every automorphism.  Since the
countermodel generated holonomy is nontrivial, it is a hard obstruction for
the narrow authority while remaining explicitly correctable for the wide one.

Thus hard obstruction is not an authority-free label attached to the
holonomy alone; it depends on which corrections are licensed.
-/

/-- Narrow correction authority for the concrete countermodel: only the
reflexive automorphism is admissible. -/
def reflexiveOnlyCounterCorrection
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    CorrectionRealization Unit
      (CounterHolonomyCarrier D) (CounterHolonomyCarrier D) where
  admissible := fun _ d => d = Iso.refl _
  effect := fun _ d => d

/-- The reflexive-only authority refines into the wide identity authority. -/
def reflexiveOnly_refines_identity
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    CorrectionAuthorityRefinement
      (reflexiveOnlyCounterCorrection D)
      (identityCorrectionRealization (CounterHolonomyCarrier D)) where
  admissible_mono := fun _ _ _ => True.intro
  effect_eq := fun _ _ => rfl

/-- The nontrivial octahedral generated holonomy is a hard obstruction for the
reflexive-only correction authority. -/
theorem counterGeneratedLoop_hard_of_reflexiveOnly
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    GeneratedHolonomyHardObstruction
      allMorphisms counterSystem D
      (reflexiveOnlyCounterCorrection D)
      () counterGeneratedLoop := by
  intro hcorrectable
  rcases hcorrectable with ⟨p, hp, heffect⟩
  apply counterGeneratedLoop_holonomy_ne_refl D
  calc
    generatedHolonomy allMorphisms counterSystem D counterGeneratedLoop
        = p := heffect.symm
    _ = Iso.refl _ := hp

/-- The same concrete generated holonomy exhibits a strict correction-authority
gap: it is correctable for the wide identity authority but hard for the narrow
reflexive-only authority. -/
theorem counterGeneratedLoop_authorityGap
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    GeneratedHolonomyAuthorityGap
      allMorphisms counterSystem D
      (reflexiveOnlyCounterCorrection D)
      (identityCorrectionRealization (CounterHolonomyCarrier D))
      () counterGeneratedLoop := by
  constructor
  · exact counterGeneratedLoop_correctable_of_identity D
  · exact counterGeneratedLoop_hard_of_reflexiveOnly D

/-- Widening from the reflexive-only authority to the identity authority
removes the hard obstruction witnessed by the concrete loop. -/
theorem counterGeneratedLoop_not_hard_after_widening
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    ¬ GeneratedHolonomyHardObstruction
      allMorphisms counterSystem D
      (identityCorrectionRealization (CounterHolonomyCarrier D))
      () counterGeneratedLoop := by
  intro hhard
  exact hhard (counterGeneratedLoop_correctable_of_identity D)

/-- Under every filtration separated at the reflexive automorphism, the
authority gap coexists with non-flatness of the very same holonomy. -/
theorem counterGeneratedLoop_nonflat_with_authorityGap
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration
      (CounterHolonomyCarrier D))
    (hsep : F.SeparatedAt (Iso.refl _)) :
    (¬ KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73.FilteredGeneratedHolonomyFlat
        allMorphisms counterSystem D F counterGeneratedLoop) ∧
      GeneratedHolonomyAuthorityGap
        allMorphisms counterSystem D
        (reflexiveOnlyCounterCorrection D)
        (identityCorrectionRealization (CounterHolonomyCarrier D))
        () counterGeneratedLoop := by
  constructor
  · exact counterGeneratedLoop_not_flat_of_separated D F hsep
  · exact counterGeneratedLoop_authorityGap D

end KUOS.DependentOriginationCountermodelAuthorityGapV2_84
