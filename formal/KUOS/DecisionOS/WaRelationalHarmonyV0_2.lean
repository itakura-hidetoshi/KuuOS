import Mathlib
import KUOS.DecisionOS.RelationalDeliberationKernelV0_1

namespace KUOS
namespace DecisionOS

inductive WaPhase where
  | bind
  | profile
  | evaluate
  | falseHarmonyCheck
  | pluralityCheck
  | gate
  | commit
  deriving DecidableEq, Repr


def WaPhase.next : WaPhase → Option WaPhase
  | .bind => some .profile
  | .profile => some .evaluate
  | .evaluate => some .falseHarmonyCheck
  | .falseHarmonyCheck => some .pluralityCheck
  | .pluralityCheck => some .gate
  | .gate => some .commit
  | .commit => none


theorem waPhase_next_deterministic
    (phase left right : WaPhase)
    (hleft : phase.next = some left)
    (hright : phase.next = some right) :
    left = right := by
  rw [hleft] at hright
  exact Option.some.inj hright


theorem waPhase_no_bind_skip :
    WaPhase.bind.next = some WaPhase.profile := by
  rfl


theorem waPhase_no_gate_skip :
    WaPhase.gate.next = some WaPhase.commit := by
  rfl


structure WaEventIndex where
  current : ℕ


def WaEventIndex.append (index : WaEventIndex) : WaEventIndex where
  current := index.current + 1


theorem waEventIndex_strict
    (index : WaEventIndex) :
    index.current < index.append.current := by
  simp [WaEventIndex.append]


structure UnitInterval where
  lower : ℝ
  upper : ℝ
  lowerNonnegative : 0 ≤ lower
  ordered : lower ≤ upper
  upperAtMostOne : upper ≤ 1


theorem UnitInterval.upperNonnegative
    (interval : UnitInterval) :
    0 ≤ interval.upper := by
  exact le_trans interval.lowerNonnegative interval.ordered


theorem UnitInterval.lowerAtMostOne
    (interval : UnitInterval) :
    interval.lower ≤ 1 := by
  exact le_trans interval.ordered interval.upperAtMostOne


structure ConvexWeight where
  value : ℝ
  nonnegative : 0 ≤ value
  atMostOne : value ≤ 1


def mixedLower
    (beta : ConvexWeight)
    (weighted weakest : UnitInterval) : ℝ :=
  (1 - beta.value) * weighted.lower + beta.value * weakest.lower


def mixedUpper
    (beta : ConvexWeight)
    (weighted weakest : UnitInterval) : ℝ :=
  (1 - beta.value) * weighted.upper + beta.value * weakest.upper


theorem mixedLower_nonnegative
    (beta : ConvexWeight)
    (weighted weakest : UnitInterval) :
    0 ≤ mixedLower beta weighted weakest := by
  unfold mixedLower
  have hleft : 0 ≤ 1 - beta.value := by linarith [beta.atMostOne]
  exact add_nonneg
    (mul_nonneg hleft weighted.lowerNonnegative)
    (mul_nonneg beta.nonnegative weakest.lowerNonnegative)


theorem mixed_ordered
    (beta : ConvexWeight)
    (weighted weakest : UnitInterval) :
    mixedLower beta weighted weakest ≤ mixedUpper beta weighted weakest := by
  unfold mixedLower mixedUpper
  have hleft : 0 ≤ 1 - beta.value := by linarith [beta.atMostOne]
  have hweighted := mul_le_mul_of_nonneg_left weighted.ordered hleft
  have hweakest := mul_le_mul_of_nonneg_left weakest.ordered beta.nonnegative
  linarith


theorem mixedUpper_atMostOne
    (beta : ConvexWeight)
    (weighted weakest : UnitInterval) :
    mixedUpper beta weighted weakest ≤ 1 := by
  unfold mixedUpper
  have hleft : 0 ≤ 1 - beta.value := by linarith [beta.atMostOne]
  have hweighted :=
    mul_le_mul_of_nonneg_left weighted.upperAtMostOne hleft
  have hweakest :=
    mul_le_mul_of_nonneg_left weakest.upperAtMostOne beta.nonnegative
  linarith


def relationalInterval
    (beta : ConvexWeight)
    (weighted weakest : UnitInterval) : UnitInterval where
  lower := mixedLower beta weighted weakest
  upper := mixedUpper beta weighted weakest
  lowerNonnegative := mixedLower_nonnegative beta weighted weakest
  ordered := mixed_ordered beta weighted weakest
  upperAtMostOne := mixedUpper_atMostOne beta weighted weakest


theorem fullBottleneck_exposes_weakestLower
    (weighted weakest : UnitInterval) :
    mixedLower ⟨1, by norm_num, by norm_num⟩ weighted weakest = weakest.lower := by
  simp [mixedLower]



def waLower
    (relational alert : UnitInterval) : ℝ :=
  relational.lower * (1 - alert.upper)


def waUpper
    (relational alert : UnitInterval) : ℝ :=
  relational.upper * (1 - alert.lower)


theorem waLower_nonnegative
    (relational alert : UnitInterval) :
    0 ≤ waLower relational alert := by
  unfold waLower
  exact mul_nonneg relational.lowerNonnegative (by linarith [alert.upperAtMostOne])


theorem wa_interval_ordered
    (relational alert : UnitInterval) :
    waLower relational alert ≤ waUpper relational alert := by
  unfold waLower waUpper
  have hUpperFactor : 0 ≤ 1 - alert.upper := by
    linarith [alert.upperAtMostOne]
  have hRelational :=
    mul_le_mul_of_nonneg_right relational.ordered hUpperFactor
  have hAlertFactor : 1 - alert.upper ≤ 1 - alert.lower := by
    linarith [alert.ordered]
  have hSecond :=
    mul_le_mul_of_nonneg_left hAlertFactor relational.upperNonnegative
  exact le_trans hRelational hSecond


theorem waUpper_atMostOne
    (relational alert : UnitInterval) :
    waUpper relational alert ≤ 1 := by
  unfold waUpper
  have hFactorNonnegative : 0 ≤ 1 - alert.lower := by
    linarith [alert.lowerAtMostOne]
  have hFactorAtMostOne : 1 - alert.lower ≤ 1 := by
    linarith [alert.lowerNonnegative]
  have hProduct :=
    mul_le_mul relational.upperAtMostOne hFactorAtMostOne
      relational.upperNonnegative hFactorNonnegative
  nlinarith


def waInterval
    (relational alert : UnitInterval) : UnitInterval where
  lower := waLower relational alert
  upper := waUpper relational alert
  lowerNonnegative := waLower_nonnegative relational alert
  ordered := wa_interval_ordered relational alert
  upperAtMostOne := waUpper_atMostOne relational alert


theorem strongerAlert_does_not_raise_waLower
    (relational alertLow alertHigh : UnitInterval)
    (upperMonotone : alertLow.upper ≤ alertHigh.upper) :
    waLower relational alertHigh ≤ waLower relational alertLow := by
  unfold waLower
  have factor : 1 - alertHigh.upper ≤ 1 - alertLow.upper := by
    linarith
  exact mul_le_mul_of_nonneg_left factor relational.lowerNonnegative


theorem strongerAlert_does_not_raise_waUpper
    (relational alertLow alertHigh : UnitInterval)
    (lowerMonotone : alertLow.lower ≤ alertHigh.lower) :
    waUpper relational alertHigh ≤ waUpper relational alertLow := by
  unfold waUpper
  have factor : 1 - alertHigh.lower ≤ 1 - alertLow.lower := by
    linarith
  exact mul_le_mul_of_nonneg_left factor relational.upperNonnegative


theorem fullAlert_collapses_wa
    (relational : UnitInterval) :
    waLower relational ⟨1, 1, by norm_num, by norm_num, by norm_num⟩ = 0 ∧
      waUpper relational ⟨1, 1, by norm_num, by norm_num, by norm_num⟩ = 0 := by
  constructor <;> simp [waLower, waUpper]


structure FalseHarmonyBoundary where
  confirmedFalseHarmony : Bool
  suspectedFalseHarmony : Bool
  minorityPreserved : Bool
  dissentConsidered : Bool


structure WaEndorsementGate where
  falseHarmony : FalseHarmonyBoundary
  minimumWaPassed : Bool
  weakestDimensionPassed : Bool
  sourceIdentityPreserved : Bool
  confirmedForbidden : falseHarmony.confirmedFalseHarmony = false
  minorityRequired : falseHarmony.minorityPreserved = true
  dissentRequired : falseHarmony.dissentConsidered = true
  waFloorRequired : minimumWaPassed = true
  weakestRequired : weakestDimensionPassed = true
  identityRequired : sourceIdentityPreserved = true


theorem endorsedWa_has_no_confirmed_false_harmony
    (gate : WaEndorsementGate) :
    gate.falseHarmony.confirmedFalseHarmony = false := by
  exact gate.confirmedForbidden


theorem endorsedWa_preserves_minority
    (gate : WaEndorsementGate) :
    gate.falseHarmony.minorityPreserved = true := by
  exact gate.minorityRequired


theorem endorsedWa_considers_dissent
    (gate : WaEndorsementGate) :
    gate.falseHarmony.dissentConsidered = true := by
  exact gate.dissentRequired


theorem endorsedWa_preserves_source_identity
    (gate : WaEndorsementGate) :
    gate.sourceIdentityPreserved = true := by
  exact gate.identityRequired


structure WaPluralityBoundary where
  sourceOptionCount : ℕ
  profiledOptionCount : ℕ
  retainedAlternativeCount : ℕ
  allProfiled : profiledOptionCount = sourceOptionCount
  retainedWithinSource : retainedAlternativeCount ≤ sourceOptionCount
  silentSubstitution : Bool
  substitutionForbidden : silentSubstitution = false


theorem waPlurality_profiles_all_source_options
    (boundary : WaPluralityBoundary) :
    boundary.profiledOptionCount = boundary.sourceOptionCount := by
  exact boundary.allProfiled


theorem waPlurality_retains_bounded_alternatives
    (boundary : WaPluralityBoundary) :
    boundary.retainedAlternativeCount ≤ boundary.sourceOptionCount := by
  exact boundary.retainedWithinSource


theorem waPlurality_forbids_silent_substitution
    (boundary : WaPluralityBoundary) :
    boundary.silentSubstitution = false := by
  exact boundary.substitutionForbidden


structure WaAuthorityBoundary where
  grantsTruthAuthority : Bool
  grantsExecutionAuthority : Bool
  grantsMoralVeto : Bool
  grantsClinicalAuthority : Bool
  grantsHostLicense : Bool
  truthForbidden : grantsTruthAuthority = false
  executionForbidden : grantsExecutionAuthority = false
  vetoForbidden : grantsMoralVeto = false
  clinicalForbidden : grantsClinicalAuthority = false
  hostLicenseForbidden : grantsHostLicense = false


theorem wa_does_not_grant_truth
    (boundary : WaAuthorityBoundary) :
    boundary.grantsTruthAuthority = false := by
  exact boundary.truthForbidden


theorem wa_does_not_execute
    (boundary : WaAuthorityBoundary) :
    boundary.grantsExecutionAuthority = false := by
  exact boundary.executionForbidden


theorem wa_does_not_grant_moral_veto
    (boundary : WaAuthorityBoundary) :
    boundary.grantsMoralVeto = false := by
  exact boundary.vetoForbidden


theorem wa_does_not_grant_host_license
    (boundary : WaAuthorityBoundary) :
    boundary.grantsHostLicense = false := by
  exact boundary.hostLicenseForbidden


structure WaCommitBoundary where
  futureOnly : Bool
  memoryOverwrite : Bool
  waNotTruth : Bool
  waNotExecution : Bool
  waNotMoralVeto : Bool
  futureRequired : futureOnly = true
  overwriteForbidden : memoryOverwrite = false
  truthSeparationRequired : waNotTruth = true
  nonExecutionRequired : waNotExecution = true
  nonVetoRequired : waNotMoralVeto = true


theorem waCommit_is_future_only
    (boundary : WaCommitBoundary) :
    boundary.futureOnly = true := by
  exact boundary.futureRequired


theorem waCommit_does_not_overwrite
    (boundary : WaCommitBoundary) :
    boundary.memoryOverwrite = false := by
  exact boundary.overwriteForbidden


theorem waCommit_is_not_execution
    (boundary : WaCommitBoundary) :
    boundary.waNotExecution = true := by
  exact boundary.nonExecutionRequired


structure ReplanWaActivation where
  missionPhaseIsReplan : Bool
  futureOnly : Bool
  memoryOverwrite : Bool
  hostLicenseGranted : Bool
  replanRequired : missionPhaseIsReplan = true
  futureRequired : futureOnly = true
  overwriteForbidden : memoryOverwrite = false
  hostLicenseForbidden : hostLicenseGranted = false


theorem waActivation_requires_replan
    (receipt : ReplanWaActivation) :
    receipt.missionPhaseIsReplan = true := by
  exact receipt.replanRequired


theorem waActivation_is_future_only
    (receipt : ReplanWaActivation) :
    receipt.futureOnly = true := by
  exact receipt.futureRequired


theorem waActivation_does_not_overwrite
    (receipt : ReplanWaActivation) :
    receipt.memoryOverwrite = false := by
  exact receipt.overwriteForbidden


theorem waActivation_does_not_grant_host_license
    (receipt : ReplanWaActivation) :
    receipt.hostLicenseGranted = false := by
  exact receipt.hostLicenseForbidden

end DecisionOS
end KUOS
