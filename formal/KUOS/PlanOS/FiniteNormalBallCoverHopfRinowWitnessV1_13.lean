import Mathlib
import KUOS.PlanOS.ExponentialMapNormalCoordinateBallV1_12

namespace KUOS.PlanOS.FiniteNormalBallCoverHopfRinowWitnessV1_13

structure FiniteNormalBallCoverHopfRinowWitnessCertificate where
  finiteNormalBallCoverCertified : Bool
  allRetainedSamplesCovered : Bool
  normalBallOverlapChainCertified : Bool
  localGeodesicExtensionChainCertified : Bool
  finiteWindowFullyExtended : Bool
  finiteCoverCoordinateBoundCertified : Bool
  boundedHopfRinowFiniteWindowWitness : Bool
  classicalHopfRinowEquivalenceNotClaimed : Bool
  globalGeodesicCompletenessNotClaimed : Bool
  globalMetricCompletenessNotClaimed : Bool
  globalCompactnessNotClaimed : Bool
  globalMinimizingGeodesicNotClaimed : Bool
  localFiniteWitnessOnly : Bool
  sourceExponentialMapCertificateNotMutated : Bool
  sourceAtlasCertificateNotMutated : Bool
  persistentWorldStateUnchanged : Bool
  candidateIdentityRetained : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  finiteCoverGrantsNoAuthority : Bool
  geodesicExtensionGrantsNoAuthority : Bool
  hopfRinowWitnessGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- One normal ball retained strictly inside a source injectivity-radius lower bound. -/
structure NormalBallWitness where
  radius : ℝ
  injectivityRadiusLowerBound : ℝ
  radiusPositive : 0 < radius
  insideInjectivityBound : radius < injectivityRadiusLowerBound

/-- One finite-window local extension step. -/
structure LocalExtensionStep where
  startParameter : ℝ
  endParameter : ℝ
  length : ℝ
  normalBallRadius : ℝ
  parameterOrder : startParameter < endParameter
  lengthIdentity : length = endParameter - startParameter
  lengthPositive : 0 < length
  lengthWithinNormalBall : length < normalBallRadius

/-- Two local extension steps whose parameter intervals are contiguous. -/
structure TwoStepExtensionChain where
  first : LocalExtensionStep
  second : LocalExtensionStep
  contiguous : first.endParameter = second.startParameter

/-- A finite indexed family of retained samples is covered by finite indexed balls. -/
def FiniteIndexedCover {ballCount sampleCount : ℕ}
    (coveredBy : Fin ballCount → Fin sampleCount → Prop) : Prop :=
  ∀ sample, ∃ ball, coveredBy ball sample

/-- A finite-window Hopf--Rinow witness is only a bounded extension-and-cover package. -/
structure BoundedHopfRinowFiniteWindowWitness where
  windowStart : ℝ
  windowEnd : ℝ
  positiveWindow : windowStart < windowEnd
  finiteCoverRetained : Prop
  extensionChainRetained : Prop
  coordinateBoundRetained : Prop

/-- A strict normal-ball witness gives a positive source injectivity bound. -/
theorem injectivityRadiusLowerBound_positive
    (ball : NormalBallWitness) :
    0 < ball.injectivityRadiusLowerBound := by
  exact lt_trans ball.radiusPositive ball.insideInjectivityBound

/-- Shrinking a retained positive normal ball preserves inclusion in the same injectivity bound. -/
theorem normalBallWitness_shrink
    (ball : NormalBallWitness)
    (smaller : ℝ)
    (hpositive : 0 < smaller)
    (hle : smaller ≤ ball.radius) :
    NormalBallWitness := by
  exact {
    radius := smaller
    injectivityRadiusLowerBound := ball.injectivityRadiusLowerBound
    radiusPositive := hpositive
    insideInjectivityBound := lt_of_le_of_lt hle ball.insideInjectivityBound
  }

/-- An explicit finite assignment produces a finite indexed cover. -/
theorem finiteIndexedCover_of_assignment
    {ballCount sampleCount : ℕ}
    (coveredBy : Fin ballCount → Fin sampleCount → Prop)
    (assignment : Fin sampleCount → Fin ballCount)
    (hcovered : ∀ sample, coveredBy (assignment sample) sample) :
    FiniteIndexedCover coveredBy := by
  intro sample
  exact ⟨assignment sample, hcovered sample⟩

/-- Every valid local extension step has the stated positive parameter increment. -/
theorem localExtensionStep_parameter_increment
    (step : LocalExtensionStep) :
    0 < step.endParameter - step.startParameter := by
  linarith [step.parameterOrder]

/-- Every valid local extension step stays below its retained normal-ball radius. -/
theorem localExtensionStep_within_normal_ball
    (step : LocalExtensionStep) :
    step.endParameter - step.startParameter < step.normalBallRadius := by
  rw [← step.lengthIdentity]
  exact step.lengthWithinNormalBall

/-- Two contiguous extension steps telescope to the sum of their certified lengths. -/
theorem twoStepExtensionChain_total_length
    (chain : TwoStepExtensionChain) :
    chain.second.endParameter - chain.first.startParameter =
      chain.first.length + chain.second.length := by
  rw [chain.first.lengthIdentity, chain.second.lengthIdentity]
  rw [← chain.contiguous]
  ring

/-- A two-step contiguous extension reaches a strictly later parameter. -/
theorem twoStepExtensionChain_reaches_later_parameter
    (chain : TwoStepExtensionChain) :
    chain.first.startParameter < chain.second.endParameter := by
  have hsecond : chain.first.endParameter < chain.second.endParameter := by
    rw [chain.contiguous]
    exact chain.second.parameterOrder
  exact lt_trans chain.first.parameterOrder hsecond

/-- The total certified length of a two-step chain is positive. -/
theorem twoStepExtensionChain_total_length_positive
    (chain : TwoStepExtensionChain) :
    0 < chain.first.length + chain.second.length := by
  exact add_pos chain.first.lengthPositive chain.second.lengthPositive

/-- A bounded finite-window witness has positive window length. -/
theorem boundedHopfRinowWitness_window_length_positive
    (witness : BoundedHopfRinowFiniteWindowWitness) :
    0 < witness.windowEnd - witness.windowStart := by
  linarith [witness.positiveWindow]

/-- Cover, extension, and boundedness evidence remain explicit conjuncts. -/
theorem boundedHopfRinowWitness_components
    (witness : BoundedHopfRinowFiniteWindowWitness) :
    witness.finiteCoverRetained ∧
      witness.extensionChainRetained ∧
      witness.coordinateBoundRetained := by
  exact ⟨witness.finiteCoverRetained,
    witness.extensionChainRetained,
    witness.coordinateBoundRetained⟩

/-- Finite cover, local extension, and bounded Hopf--Rinow evidence grant no authority. -/
theorem finite_hopf_rinow_geometry_grants_no_authority
    (certificate : FiniteNormalBallCoverHopfRinowWitnessCertificate)
    (hcover : certificate.finiteCoverGrantsNoAuthority = true)
    (hextension : certificate.geodesicExtensionGrantsNoAuthority = true)
    (hhopf : certificate.hopfRinowWitnessGrantsNoAuthority = true)
    (hselection : certificate.decisionSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.finiteCoverGrantsNoAuthority = true ∧
      certificate.geodesicExtensionGrantsNoAuthority = true ∧
      certificate.hopfRinowWitnessGrantsNoAuthority = true ∧
      certificate.decisionSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hcover, hextension, hhopf, hselection, hexecution⟩

/-- The v1.13 witness remains local, finite, read-only, future-only, and inactive. -/
theorem finite_hopf_rinow_certificate_is_local_future_only
    (certificate : FiniteNormalBallCoverHopfRinowWitnessCertificate)
    (hlocal : certificate.localFiniteWitnessOnly = true)
    (hclassical : certificate.classicalHopfRinowEquivalenceNotClaimed = true)
    (hcomplete : certificate.globalGeodesicCompletenessNotClaimed = true)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.localFiniteWitnessOnly = true ∧
      certificate.classicalHopfRinowEquivalenceNotClaimed = true ∧
      certificate.globalGeodesicCompletenessNotClaimed = true ∧
      certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hlocal, hclassical, hcomplete, hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.FiniteNormalBallCoverHopfRinowWitnessV1_13
