import Mathlib
import KUOS.OpenHorizon.MemoryOSRelativeEntropyTransportLebesgueDecompositionV0_55

namespace KUOS.OpenHorizon.MemoryOSFDivergenceTransportDataProcessingV0_56

open KUOS.OpenHorizon.MemoryOSCandidateQuotientModeDiagonalizationInverseV0_51
open KUOS.OpenHorizon.MemoryOSQuotientMetricDensityTransportRadonNikodymCocycleV0_54
open KUOS.OpenHorizon.MemoryOSRelativeEntropyTransportLebesgueDecompositionV0_55

def fDivergenceDensityContribution
    (f : ℝ → ℝ) (pDensity qDensity cellVolume : ℝ) : ℝ :=
  (qDensity * f (pDensity / qDensity)) * cellVolume

theorem f_divergence_density_transport_invariant
    (f : ℝ → ℝ)
    (pDensity qDensity cellVolume rho jacobian : ℝ)
    (hq : qDensity ≠ 0)
    (hrho : rho ≠ 0)
    (hreciprocal : rho * jacobian = 1) :
    fDivergenceDensityContribution f
        (pDensity * rho) (qDensity * rho) (cellVolume * jacobian) =
      fDivergenceDensityContribution f pDensity qDensity cellVolume := by
  unfold fDivergenceDensityContribution
  rw [likelihood_ratio_invariant_under_common_density_scaling
    pDensity qDensity rho hq hrho]
  calc
    ((qDensity * rho) * f (pDensity / qDensity)) *
          (cellVolume * jacobian) =
        (qDensity * f (pDensity / qDensity) * cellVolume) *
          (rho * jacobian) := by ring
    _ = qDensity * f (pDensity / qDensity) * cellVolume := by
      rw [hreciprocal]
      ring

theorem finite_support_f_divergence_transport_invariant
    {ι : Type*}
    (support : Finset ι)
    (f : ℝ → ℝ)
    (pDensity qDensity cellVolume : ι → ℝ)
    (rho jacobian : ℝ)
    (hq : ∀ i ∈ support, qDensity i ≠ 0)
    (hrho : rho ≠ 0)
    (hreciprocal : rho * jacobian = 1) :
    ∑ i ∈ support,
        fDivergenceDensityContribution f
          (pDensity i * rho) (qDensity i * rho)
          (cellVolume i * jacobian) =
      ∑ i ∈ support,
        fDivergenceDensityContribution f
          (pDensity i) (qDensity i) (cellVolume i) := by
  apply Finset.sum_congr rfl
  intro i hi
  exact f_divergence_density_transport_invariant
    f (pDensity i) (qDensity i) (cellVolume i)
    rho jacobian (hq i hi) hrho hreciprocal

def pearsonFGenerator (ratio : ℝ) : ℝ :=
  (ratio - 1) ^ 2

def pearsonDivergenceContribution (pMass qMass : ℝ) : ℝ :=
  (pMass - qMass) ^ 2 / qMass

theorem pearson_generator_contribution_eq
    (pMass qMass : ℝ)
    (hq : qMass ≠ 0) :
    fDivergenceDensityContribution pearsonFGenerator
        pMass qMass 1 =
      pearsonDivergenceContribution pMass qMass := by
  unfold fDivergenceDensityContribution pearsonFGenerator
    pearsonDivergenceContribution
  field_simp [hq]
  ring

theorem pearson_pairwise_merge_gap_identity
    (p₁ p₂ q₁ q₂ : ℝ)
    (hq₁ : q₁ ≠ 0)
    (hq₂ : q₂ ≠ 0)
    (hqsum : q₁ + q₂ ≠ 0) :
    pearsonDivergenceContribution p₁ q₁ +
        pearsonDivergenceContribution p₂ q₂ -
        pearsonDivergenceContribution (p₁ + p₂) (q₁ + q₂) =
      (q₂ * (p₁ - q₁) - q₁ * (p₂ - q₂)) ^ 2 /
        (q₁ * q₂ * (q₁ + q₂)) := by
  unfold pearsonDivergenceContribution
  field_simp [hq₁, hq₂, hqsum]
  ring

theorem pearson_pairwise_merge_data_processing
    (p₁ p₂ q₁ q₂ : ℝ)
    (hq₁ : 0 < q₁)
    (hq₂ : 0 < q₂) :
    pearsonDivergenceContribution (p₁ + p₂) (q₁ + q₂) ≤
      pearsonDivergenceContribution p₁ q₁ +
        pearsonDivergenceContribution p₂ q₂ := by
  have hidentity := pearson_pairwise_merge_gap_identity
    p₁ p₂ q₁ q₂ (ne_of_gt hq₁) (ne_of_gt hq₂)
      (ne_of_gt (add_pos hq₁ hq₂))
  have hdenominator :
      0 < q₁ * q₂ * (q₁ + q₂) :=
    mul_pos (mul_pos hq₁ hq₂) (add_pos hq₁ hq₂)
  have hgap :
      0 ≤
        (q₂ * (p₁ - q₁) - q₁ * (p₂ - q₂)) ^ 2 /
          (q₁ * q₂ * (q₁ + q₂)) :=
    div_nonneg (sq_nonneg _) (le_of_lt hdenominator)
  linarith

theorem pearson_three_way_coarse_graining_contracts
    (p₁ p₂ p₃ q₁ q₂ q₃ : ℝ)
    (hq₁ : 0 < q₁)
    (hq₂ : 0 < q₂)
    (hq₃ : 0 < q₃) :
    pearsonDivergenceContribution (p₁ + p₂ + p₃) (q₁ + q₂ + q₃) ≤
      pearsonDivergenceContribution p₁ q₁ +
        pearsonDivergenceContribution p₂ q₂ +
        pearsonDivergenceContribution p₃ q₃ := by
  have hfirst := pearson_pairwise_merge_data_processing
    p₁ p₂ q₁ q₂ hq₁ hq₂
  have hsecond := pearson_pairwise_merge_data_processing
    (p₁ + p₂) p₃ (q₁ + q₂) q₃ (add_pos hq₁ hq₂) hq₃
  linarith

def pearsonRationalContribution (pMass qMass : ℚ) : ℚ :=
  (pMass - qMass) ^ 2 / qMass

theorem exact_reference_coarse_channel_masses :
    ((1 : ℚ) + 2 + 3) / 45 = (2 : ℚ) / 15 ∧
      ((4 : ℚ) + 5 + 6) / 45 = (1 : ℚ) / 3 ∧
      ((7 : ℚ) + 8 + 9) / 45 = (8 : ℚ) / 15 ∧
      ((9 : ℚ) + 8 + 7) / 45 = (8 : ℚ) / 15 ∧
      ((6 : ℚ) + 5 + 4) / 45 = (1 : ℚ) / 3 ∧
      ((3 : ℚ) + 2 + 1) / 45 = (2 : ℚ) / 15 := by
  norm_num

theorem exact_reference_pearson_data_processing :
    let fine :=
      pearsonRationalContribution ((1 : ℚ) / 45) ((9 : ℚ) / 45) +
      pearsonRationalContribution ((2 : ℚ) / 45) ((8 : ℚ) / 45) +
      pearsonRationalContribution ((3 : ℚ) / 45) ((7 : ℚ) / 45) +
      pearsonRationalContribution ((4 : ℚ) / 45) ((6 : ℚ) / 45) +
      pearsonRationalContribution ((5 : ℚ) / 45) ((5 : ℚ) / 45) +
      pearsonRationalContribution ((6 : ℚ) / 45) ((4 : ℚ) / 45) +
      pearsonRationalContribution ((7 : ℚ) / 45) ((3 : ℚ) / 45) +
      pearsonRationalContribution ((8 : ℚ) / 45) ((2 : ℚ) / 45) +
      pearsonRationalContribution ((9 : ℚ) / 45) ((1 : ℚ) / 45)
    let coarse :=
      pearsonRationalContribution ((2 : ℚ) / 15) ((8 : ℚ) / 15) +
      pearsonRationalContribution ((1 : ℚ) / 3) ((1 : ℚ) / 3) +
      pearsonRationalContribution ((8 : ℚ) / 15) ((2 : ℚ) / 15)
    fine = (2593 : ℚ) / 1134 ∧
      coarse = (3 : ℚ) / 2 ∧
      fine - coarse = (446 : ℚ) / 567 ∧
      coarse ≤ fine := by
  norm_num [pearsonRationalContribution]

theorem full_rank_density_transport_gives_exact_f_divergence_invariance
    (f : ℝ → ℝ)
    (sourceCross targetCross : ℤ)
    (pDensity qDensity cellVolume : ℝ)
    (hsource : quotientMetricDeterminant sourceCross ≠ 0)
    (htarget : quotientMetricDeterminant targetCross ≠ 0)
    (hq : qDensity ≠ 0) :
    fDivergenceDensityContribution f
        (pDensity *
          ((quotientMetricDensityMultiplier sourceCross targetCross : ℚ) : ℝ))
        (qDensity *
          ((quotientMetricDensityMultiplier sourceCross targetCross : ℚ) : ℝ))
        (cellVolume *
          ((quotientTransportJacobian sourceCross targetCross : ℚ) : ℝ)) =
      fDivergenceDensityContribution f pDensity qDensity cellVolume := by
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
  exact f_divergence_density_transport_invariant
    f pDensity qDensity cellVolume
    ((quotientMetricDensityMultiplier sourceCross targetCross : ℚ) : ℝ)
    ((quotientTransportJacobian sourceCross targetCross : ℚ) : ℝ)
    hq hrhoR hreciprocalR

theorem rank_one_source_has_no_two_dimensional_f_divergence_density
    (targetCross : ℤ) :
    quotientMetricDeterminant 2 = 0 ∧
      transportDeterminantNumerator 2 targetCross = 0 := by
  exact full_coherence_source_has_no_two_dimensional_density targetCross

structure FDivergenceTransportDataProcessingCertificate where
  sourceMemoryOSV055Bound : Bool
  sourceMemoryOSV054Bound : Bool
  generatorCatalogExact : Bool
  allFullRankFDivergenceTermsInvariant : Bool
  allDataProcessingContractionsExact : Bool
  allPearsonMergeGapsExact : Bool
  allFDivergenceCocyclesExact : Bool
  singularAtomicFDivergenceRetained : Bool
  rankOneDensityRecoveryNotClaimed : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV055Mutated : Bool
  sourceMemoryOSV054Mutated : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

theorem certificate_grants_no_authority
    (certificate : FDivergenceTransportDataProcessingCertificate)
    (hpruning : certificate.candidatePruningPerformed = false)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hsource55 : certificate.sourceMemoryOSV055Mutated = false)
    (hsource54 : certificate.sourceMemoryOSV054Mutated = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV055Mutated = false ∧
      certificate.sourceMemoryOSV054Mutated = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hpruning, hselection, hexecution, hsource55, hsource54,
    hworld, hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSFDivergenceTransportDataProcessingV0_56
