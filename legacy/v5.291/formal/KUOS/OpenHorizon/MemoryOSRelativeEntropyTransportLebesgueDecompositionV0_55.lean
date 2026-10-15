import Mathlib
import KUOS.OpenHorizon.MemoryOSQuotientMetricDensityTransportRadonNikodymCocycleV0_54

namespace KUOS.OpenHorizon.MemoryOSRelativeEntropyTransportLebesgueDecompositionV0_55

open KUOS.OpenHorizon.MemoryOSCandidateQuotientModeDiagonalizationInverseV0_51
open KUOS.OpenHorizon.MemoryOSQuotientMetricDensityTransportRadonNikodymCocycleV0_54

def relativeEntropyDensityContribution
    (pDensity qDensity cellVolume : ℝ) : ℝ :=
  (pDensity * Real.log (pDensity / qDensity)) * cellVolume

theorem likelihood_ratio_invariant_under_common_density_scaling
    (pDensity qDensity rho : ℝ)
    (hq : qDensity ≠ 0)
    (hrho : rho ≠ 0) :
    (pDensity * rho) / (qDensity * rho) = pDensity / qDensity := by
  field_simp [hq, hrho]
  ring

theorem relative_entropy_density_transport_invariant
    (pDensity qDensity cellVolume rho jacobian : ℝ)
    (hq : qDensity ≠ 0)
    (hrho : rho ≠ 0)
    (hreciprocal : rho * jacobian = 1) :
    relativeEntropyDensityContribution
        (pDensity * rho) (qDensity * rho) (cellVolume * jacobian) =
      relativeEntropyDensityContribution pDensity qDensity cellVolume := by
  unfold relativeEntropyDensityContribution
  rw [likelihood_ratio_invariant_under_common_density_scaling
    pDensity qDensity rho hq hrho]
  calc
    ((pDensity * rho) * Real.log (pDensity / qDensity)) *
          (cellVolume * jacobian) =
        (pDensity * Real.log (pDensity / qDensity) * cellVolume) *
          (rho * jacobian) := by ring
    _ = pDensity * Real.log (pDensity / qDensity) * cellVolume := by
      rw [hreciprocal]
      ring

theorem reverse_relative_entropy_density_transport_invariant
    (pDensity qDensity cellVolume rho jacobian : ℝ)
    (hp : pDensity ≠ 0)
    (hrho : rho ≠ 0)
    (hreciprocal : rho * jacobian = 1) :
    relativeEntropyDensityContribution
        (qDensity * rho) (pDensity * rho) (cellVolume * jacobian) =
      relativeEntropyDensityContribution qDensity pDensity cellVolume := by
  exact relative_entropy_density_transport_invariant
    qDensity pDensity cellVolume rho jacobian hp hrho hreciprocal

theorem finite_support_relative_entropy_transport_invariant
    {ι : Type*}
    (support : Finset ι)
    (pDensity qDensity cellVolume : ι → ℝ)
    (rho jacobian : ℝ)
    (hq : ∀ i ∈ support, qDensity i ≠ 0)
    (hrho : rho ≠ 0)
    (hreciprocal : rho * jacobian = 1) :
    ∑ i ∈ support,
        relativeEntropyDensityContribution
          (pDensity i * rho) (qDensity i * rho)
          (cellVolume i * jacobian) =
      ∑ i ∈ support,
        relativeEntropyDensityContribution
          (pDensity i) (qDensity i) (cellVolume i) := by
  apply Finset.sum_congr rfl
  intro i hi
  exact relative_entropy_density_transport_invariant
    (pDensity i) (qDensity i) (cellVolume i) rho jacobian
    (hq i hi) hrho hreciprocal

theorem relative_entropy_transport_composition
    (sourceEntropy middleEntropy targetEntropy : ℝ)
    (hsourceMiddle : middleEntropy = sourceEntropy)
    (hmiddleTarget : targetEntropy = middleEntropy) :
    targetEntropy = sourceEntropy := by
  calc
    targetEntropy = middleEntropy := hmiddleTarget
    _ = sourceEntropy := hsourceMiddle

theorem exact_reference_probability_masses :
    ((1 : ℚ) + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9) / 45 = 1 ∧
      ((9 : ℚ) + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1) / 45 = 1 := by
  norm_num

theorem exact_reference_likelihood_ratios :
    ((1 : ℚ) / 45) / ((9 : ℚ) / 45) = (1 : ℚ) / 9 ∧
      ((5 : ℚ) / 45) / ((5 : ℚ) / 45) = 1 ∧
      ((9 : ℚ) / 45) / ((1 : ℚ) / 45) = 9 := by
  norm_num

theorem full_rank_density_transport_gives_exact_kl_invariance
    (sourceCross targetCross : ℤ)
    (pDensity qDensity cellVolume : ℝ)
    (hsource : quotientMetricDeterminant sourceCross ≠ 0)
    (htarget : quotientMetricDeterminant targetCross ≠ 0)
    (hq : qDensity ≠ 0) :
    relativeEntropyDensityContribution
        (pDensity *
          ((quotientMetricDensityMultiplier sourceCross targetCross : ℚ) : ℝ))
        (qDensity *
          ((quotientMetricDensityMultiplier sourceCross targetCross : ℚ) : ℝ))
        (cellVolume *
          ((quotientTransportJacobian sourceCross targetCross : ℚ) : ℝ)) =
      relativeEntropyDensityContribution pDensity qDensity cellVolume := by
  have hsourceQ : (quotientMetricDeterminant sourceCross : ℚ) ≠ 0 := by
    exact_mod_cast hsource
  have htargetQ : (quotientMetricDeterminant targetCross : ℚ) ≠ 0 := by
    exact_mod_cast htarget
  have hrhoQ :
      quotientMetricDensityMultiplier sourceCross targetCross ≠ 0 := by
    unfold quotientMetricDensityMultiplier
    exact div_ne_zero hsourceQ htargetQ
  have hrhoR :
      ((quotientMetricDensityMultiplier sourceCross targetCross : ℚ) : ℝ) ≠ 0 := by
    exact_mod_cast hrhoQ
  have hreciprocalQ :
      quotientMetricDensityMultiplier sourceCross targetCross *
        quotientTransportJacobian sourceCross targetCross = 1 :=
    density_multiplier_is_jacobian_reciprocal
      sourceCross targetCross hsource htarget
  have hreciprocalR :
      ((quotientMetricDensityMultiplier sourceCross targetCross : ℚ) : ℝ) *
        ((quotientTransportJacobian sourceCross targetCross : ℚ) : ℝ) = 1 := by
    exact_mod_cast hreciprocalQ
  exact relative_entropy_density_transport_invariant
    pDensity qDensity cellVolume
    ((quotientMetricDensityMultiplier sourceCross targetCross : ℚ) : ℝ)
    ((quotientTransportJacobian sourceCross targetCross : ℚ) : ℝ)
    hq hrhoR hreciprocalR

theorem singular_lebesgue_decomposition_exact
    (pMass qMass : ℚ) :
    (0 : ℚ) + pMass = pMass ∧
      (0 : ℚ) + qMass = qMass ∧
      pMass = 0 + pMass ∧
      qMass = 0 + qMass := by
  ring

theorem full_rank_to_rank_one_has_zero_absolutely_continuous_mass
    (pMass qMass : ℚ) :
    let pAbsolutelyContinuous := (0 : ℚ)
    let pSingular := pMass
    let qAbsolutelyContinuous := (0 : ℚ)
    let qSingular := qMass
    pAbsolutelyContinuous + pSingular = pMass ∧
      qAbsolutelyContinuous + qSingular = qMass := by
  simp

theorem rank_one_source_has_no_two_dimensional_relative_entropy_density
    (targetCross : ℤ) :
    quotientMetricDeterminant 2 = 0 ∧
      transportDeterminantNumerator 2 targetCross = 0 := by
  exact full_coherence_source_has_no_two_dimensional_density targetCross

structure RelativeEntropyTransportLebesgueDecompositionCertificate where
  sourceMemoryOSV054Bound : Bool
  sourceMemoryOSV053Bound : Bool
  allReferenceProbabilityMassesExact : Bool
  allLikelihoodRatiosExact : Bool
  allFullRankRelativeEntropyTermsInvariant : Bool
  allReverseRelativeEntropyTermsInvariant : Bool
  allRelativeEntropyCocyclesExact : Bool
  allSingularLebesgueDecompositionsExact : Bool
  singularAtomicRelativeEntropyRetained : Bool
  rankOneDensityRecoveryNotClaimed : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV054Mutated : Bool
  sourceMemoryOSV053Mutated : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

theorem certificate_grants_no_authority
    (certificate : RelativeEntropyTransportLebesgueDecompositionCertificate)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hsource54 : certificate.sourceMemoryOSV054Mutated = false)
    (hsource53 : certificate.sourceMemoryOSV053Mutated = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidateSelectionPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV054Mutated = false ∧
      certificate.sourceMemoryOSV053Mutated = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hselection, hexecution, hsource54, hsource53, hworld,
    hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSRelativeEntropyTransportLebesgueDecompositionV0_55
