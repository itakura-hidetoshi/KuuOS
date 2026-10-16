import KUOS.DependentOriginationCorrectionReachabilityProfileV2_89

namespace KUOS.DependentOriginationStrictCorrectionPowerV2_90

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationCountermodelCorrectabilityBridgeV2_81
open KUOS.DependentOriginationConcreteCorrectabilitySeparationV2_82
open KUOS.DependentOriginationCorrectionAuthorityRefinementV2_83
open KUOS.DependentOriginationReflexiveAuthorityGapV2_85
open KUOS.DependentOriginationHeterogeneousCorrectionAuthorityV2_86
open KUOS.DependentOriginationCorrectionPowerSemanticsV2_88
open KUOS.DependentOriginationCorrectionReachabilityProfileV2_89
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69

universe u v₁ v₂ w uC vC uH vH

/-!
# Strict correction power v2.90

The v2.88-v2.89 semantics turns correction authority into a preorder of
reachable defect profiles.  A genuine authority gap should therefore witness
a strict increase of correction power whenever the source power is already
known to embed into the target power.

This layer makes that statement explicit.  It then applies it to the
octahedral countermodel:

* the reflexive-only authority embeds into the unrestricted identity authority;
* the concrete generated holonomy is correctable in the identity authority;
* the same holonomy is hard in the reflexive-only authority.

Hence the identity authority has strictly greater correction power.  Under a
separated filtration, this strict authority difference coexists with the
non-flatness of the same generated holonomy.
-/

/-- Strict inclusion of extensional correction power. -/
def CorrectionPowerLT
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) : Prop :=
  CorrectionPowerLE C₁ C₂ ∧ ¬ CorrectionPowerLE C₂ C₁

/-- A reachable defect in the target which is hard in the source witnesses
strict correction-power inclusion, provided source power already embeds into
target power. -/
theorem correctionPowerLT_of_le_of_witness
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    {C₁ : CorrectionRealization State Param₁ D}
    {C₂ : CorrectionRealization State Param₂ D}
    (hle : CorrectionPowerLE C₁ C₂)
    {x : State} {d : D}
    (htarget : C₂.CorrectableAt x d)
    (hsource : C₁.HardObstructionAt x d) :
    CorrectionPowerLT C₁ C₂ := by
  refine ⟨hle, ?_⟩
  intro hreverse
  exact hsource (hreverse x d htarget)

/-- A generated-holonomy authority gap witnesses strict correction power when
the source authority is already included in the target authority. -/
theorem generatedHolonomy_correctionPowerLT_of_le_of_gap
    {Context : Type uC} [Category.{vC} Context]
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (P : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    {State : Type u}
    {Param₁ : Type v₁} {Param₂ : Type v₂}
    (Source : CorrectionRealization State Param₁
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (Target : CorrectionRealization State Param₂
      ((freePathEvaluator W R P).map p ≅
        (freePathEvaluator W R P).map p))
    (hle : CorrectionPowerLE Source Target)
    (x : State)
    (gamma : GeneratedLocalizationLoop W p)
    (hgap : GeneratedHolonomyHeterogeneousAuthorityGap
      W R P Source Target x gamma) :
    CorrectionPowerLT Source Target := by
  exact correctionPowerLT_of_le_of_witness
    hle hgap.1 hgap.2

/-- The reflexive-only octahedral correction authority is extensionally
included in the unrestricted identity authority. -/
theorem counter_reflexive_powerLE_identity
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    CorrectionPowerLE
      (reflexiveOnlyCounterCorrection D)
      (identityCorrectionRealization (CounterHolonomyCarrier D)) := by
  exact CorrectionPowerLE.ofAuthorityHom
    (CorrectionAuthorityHom.ofRefinement
      (reflexiveOnly_refines_identity D))

/-- The octahedral countermodel witnesses a strict correction-power increase
from reflexive-only authority to unrestricted identity authority. -/
theorem counter_reflexive_powerLT_identity
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    CorrectionPowerLT
      (reflexiveOnlyCounterCorrection D)
      (identityCorrectionRealization (CounterHolonomyCarrier D)) := by
  have hgap := counterGeneratedLoop_reflexive_authorityGap D
  exact correctionPowerLT_of_le_of_witness
    (counter_reflexive_powerLE_identity D)
    hgap.1 hgap.2

/-- The strict authority-power difference is witnessed at the concrete
generated holonomy itself. -/
theorem counterGeneratedLoop_strictPower_witness
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem) :
    CorrectionReachabilityProfile
        (identityCorrectionRealization (CounterHolonomyCarrier D))
        ()
        (generatedHolonomy
          allMorphisms counterSystem D counterGeneratedLoop) ∧
      ¬ CorrectionReachabilityProfile
        (reflexiveOnlyCounterCorrection D)
        ()
        (generatedHolonomy
          allMorphisms counterSystem D counterGeneratedLoop) := by
  have hgap := counterGeneratedLoop_reflexive_authorityGap D
  exact ⟨hgap.1, hgap.2⟩

/-- Under separated filtration, non-flatness and strict correction-power
inequality coexist for the same octahedral generated holonomy. -/
theorem counterGeneratedLoop_nonflat_and_strictPower
    (D : PointwiseWAdjointEquivalenceData
      (W := allMorphisms) counterSystem)
    (F : ObstructionFiltration (CounterHolonomyCarrier D))
    (hsep : F.SeparatedAt (Iso.refl _)) :
    (¬ FilteredGeneratedHolonomyFlat
        allMorphisms counterSystem D F counterGeneratedLoop) ∧
      CorrectionPowerLT
        (reflexiveOnlyCounterCorrection D)
        (identityCorrectionRealization (CounterHolonomyCarrier D)) := by
  exact ⟨
    counterGeneratedLoop_not_flat_of_separated D F hsep,
    counter_reflexive_powerLT_identity D
  ⟩

end KUOS.DependentOriginationStrictCorrectionPowerV2_90
