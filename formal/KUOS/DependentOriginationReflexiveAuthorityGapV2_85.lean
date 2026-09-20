import KUOS.DependentOriginationRestrictedCorrectionAuthorityGapV2_84

namespace KUOS.DependentOriginationReflexiveAuthorityGapV2_85

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
open KUOS.DependentOriginationConcreteCorrectabilitySeparationV2_82
open KUOS.DependentOriginationCorrectionAuthorityRefinementV2_83
open KUOS.DependentOriginationRestrictedCorrectionAuthorityGapV2_84

/-!
# Reflexive-only correction authority gap v2.85

The v2.84 layer gives a generic restricted-identity correction authority.
This file specializes that construction to the smallest natural authority for
the octahedral countermodel: only the reflexive automorphism is licensed.

The v2.69 generated loop is nontrivial, so it is excluded by that narrow
authority.  The generic v2.84 authority-gap theorem therefore gives a concrete
strict separation:

* the loop is hard for the reflexive-only authority;
* the same loop is correctable for the unrestricted identity authority;
* under separated filtration it can simultaneously remain non-flat.

This specialization adds no new obstruction principle; it instantiates the
authority-relative theorem with a canonical explicit predicate.
-/

/-- The narrow predicate licensing only the reflexive automorphism. -/
def ReflexiveAllowed
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    CounterHolonomyCarrier D → Prop :=
  fun d => d = Iso.refl _

/-- The corresponding reflexive-only correction realization. -/
abbrev reflexiveOnlyCounterCorrection
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :=
  restrictedIdentityCorrectionRealization (ReflexiveAllowed D)

/-- The concrete nontrivial holonomy is excluded by the reflexive-only
authority. -/
theorem counterGeneratedLoop_not_reflexiveAllowed
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    ¬ ReflexiveAllowed D
      (generatedHolonomy
        allMorphisms counterSystem D counterGeneratedLoop) := by
  exact counterGeneratedLoop_holonomy_ne_refl D

/-- The reflexive-only correction authority refines into the unrestricted
identity authority. -/
theorem reflexiveOnly_refines_identity
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    CorrectionAuthorityRefinement
      (reflexiveOnlyCounterCorrection D)
      (identityCorrectionRealization (CounterHolonomyCarrier D)) := by
  exact counterRestrictedAuthority_refines_identity D (ReflexiveAllowed D)

/-- The octahedral generated loop exhibits the concrete reflexive-only
authority gap. -/
theorem counterGeneratedLoop_reflexive_authorityGap
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    GeneratedHolonomyAuthorityGap
      allMorphisms counterSystem D
      (reflexiveOnlyCounterCorrection D)
      (identityCorrectionRealization (CounterHolonomyCarrier D))
      () counterGeneratedLoop := by
  exact counterGeneratedLoop_authorityGap_of_not_allowed
    D (ReflexiveAllowed D)
    (counterGeneratedLoop_not_reflexiveAllowed D)

/-- In particular, the generated loop is a hard obstruction for the
reflexive-only authority. -/
theorem counterGeneratedLoop_hard_of_reflexiveOnly
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    GeneratedHolonomyHardObstruction
      allMorphisms counterSystem D
      (reflexiveOnlyCounterCorrection D)
      () counterGeneratedLoop :=
  (counterGeneratedLoop_reflexive_authorityGap D).2

/-- Under separated filtration, non-flatness and the reflexive-only authority
gap coexist for the same generated holonomy. -/
theorem counterGeneratedLoop_nonflat_reflexive_authorityGap
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : ObstructionFiltration (CounterHolonomyCarrier D))
    (hsep : F.SeparatedAt (Iso.refl _)) :
    (¬ FilteredGeneratedHolonomyFlat
        allMorphisms counterSystem D F counterGeneratedLoop) ∧
      GeneratedHolonomyAuthorityGap
        allMorphisms counterSystem D
        (reflexiveOnlyCounterCorrection D)
        (identityCorrectionRealization (CounterHolonomyCarrier D))
        () counterGeneratedLoop := by
  exact counterGeneratedLoop_nonflat_authorityGap_of_not_allowed
    D F hsep (ReflexiveAllowed D)
    (counterGeneratedLoop_not_reflexiveAllowed D)

end KUOS.DependentOriginationReflexiveAuthorityGapV2_85
