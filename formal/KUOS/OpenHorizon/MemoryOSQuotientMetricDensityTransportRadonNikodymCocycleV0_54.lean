import Mathlib
import KUOS.OpenHorizon.MemoryOSQuotientTransportJacobianVolumeStratificationV0_53

namespace KUOS.OpenHorizon.MemoryOSQuotientMetricDensityTransportRadonNikodymCocycleV0_54

open KUOS.OpenHorizon.MemoryOSCandidateQuotientModeDiagonalizationInverseV0_51
open KUOS.OpenHorizon.MemoryOSQuotientTransportJacobianVolumeStratificationV0_53

def quotientTransportJacobian
    (sourceCross targetCross : ℤ) : ℚ :=
  (quotientMetricDeterminant targetCross : ℚ) /
    (quotientMetricDeterminant sourceCross : ℚ)

def quotientMetricDensityMultiplier
    (sourceCross targetCross : ℤ) : ℚ :=
  (quotientMetricDeterminant sourceCross : ℚ) /
    (quotientMetricDeterminant targetCross : ℚ)

def quotientSymmetricDensityMultiplier
    (sourceCross targetCross : ℤ) : ℚ :=
  (quotientSymmetricWeight sourceCross : ℚ) /
    (quotientSymmetricWeight targetCross : ℚ)

def quotientAntisymmetricDensityMultiplier
    (sourceCross targetCross : ℤ) : ℚ :=
  (quotientAntisymmetricWeight sourceCross : ℚ) /
    (quotientAntisymmetricWeight targetCross : ℚ)

theorem quotient_metric_determinant_mode_factorization
    (cross : ℤ) :
    quotientMetricDeterminant cross =
      quotientSymmetricWeight cross * quotientAntisymmetricWeight cross := by
  simp [quotientMetricDeterminant, quotientSymmetricWeight,
    quotientAntisymmetricWeight]
  ring

theorem density_multiplier_is_jacobian_reciprocal
    (sourceCross targetCross : ℤ)
    (hsource : quotientMetricDeterminant sourceCross ≠ 0)
    (htarget : quotientMetricDeterminant targetCross ≠ 0) :
    quotientMetricDensityMultiplier sourceCross targetCross *
        quotientTransportJacobian sourceCross targetCross = 1 := by
  have hsourceQ : (quotientMetricDeterminant sourceCross : ℚ) ≠ 0 := by
    exact_mod_cast hsource
  have htargetQ : (quotientMetricDeterminant targetCross : ℚ) ≠ 0 := by
    exact_mod_cast htarget
  unfold quotientMetricDensityMultiplier quotientTransportJacobian
  field_simp [hsourceQ, htargetQ]
  ring

theorem mode_density_product_is_radon_nikodym
    (sourceCross targetCross : ℤ)
    (hsourceSymmetric : quotientSymmetricWeight sourceCross ≠ 0)
    (hsourceAntisymmetric : quotientAntisymmetricWeight sourceCross ≠ 0)
    (htargetSymmetric : quotientSymmetricWeight targetCross ≠ 0)
    (htargetAntisymmetric : quotientAntisymmetricWeight targetCross ≠ 0) :
    quotientSymmetricDensityMultiplier sourceCross targetCross *
        quotientAntisymmetricDensityMultiplier sourceCross targetCross =
      quotientMetricDensityMultiplier sourceCross targetCross := by
  have hsourceSymmetricQ : (quotientSymmetricWeight sourceCross : ℚ) ≠ 0 := by
    exact_mod_cast hsourceSymmetric
  have hsourceAntisymmetricQ :
      (quotientAntisymmetricWeight sourceCross : ℚ) ≠ 0 := by
    exact_mod_cast hsourceAntisymmetric
  have htargetSymmetricQ : (quotientSymmetricWeight targetCross : ℚ) ≠ 0 := by
    exact_mod_cast htargetSymmetric
  have htargetAntisymmetricQ :
      (quotientAntisymmetricWeight targetCross : ℚ) ≠ 0 := by
    exact_mod_cast htargetAntisymmetric
  unfold quotientSymmetricDensityMultiplier
    quotientAntisymmetricDensityMultiplier quotientMetricDensityMultiplier
  rw [quotient_metric_determinant_mode_factorization sourceCross,
    quotient_metric_determinant_mode_factorization targetCross]
  field_simp [hsourceSymmetricQ, hsourceAntisymmetricQ,
    htargetSymmetricQ, htargetAntisymmetricQ]
  ring

theorem radon_nikodym_density_cocycle
    (sourceCross middleCross targetCross : ℤ)
    (hsource : quotientMetricDeterminant sourceCross ≠ 0)
    (hmiddle : quotientMetricDeterminant middleCross ≠ 0)
    (htarget : quotientMetricDeterminant targetCross ≠ 0) :
    quotientMetricDensityMultiplier sourceCross middleCross *
        quotientMetricDensityMultiplier middleCross targetCross =
      quotientMetricDensityMultiplier sourceCross targetCross := by
  have hsourceQ : (quotientMetricDeterminant sourceCross : ℚ) ≠ 0 := by
    exact_mod_cast hsource
  have hmiddleQ : (quotientMetricDeterminant middleCross : ℚ) ≠ 0 := by
    exact_mod_cast hmiddle
  have htargetQ : (quotientMetricDeterminant targetCross : ℚ) ≠ 0 := by
    exact_mod_cast htarget
  unfold quotientMetricDensityMultiplier
  field_simp [hsourceQ, hmiddleQ, htargetQ]
  ring

theorem finite_support_pushforward_pullback_mass_preserved
    (sourceCross targetCross : ℤ)
    (sourceDensity sourceCellVolume : ℚ)
    (hsource : quotientMetricDeterminant sourceCross ≠ 0)
    (htarget : quotientMetricDeterminant targetCross ≠ 0) :
    (sourceDensity *
        quotientMetricDensityMultiplier sourceCross targetCross) *
      (sourceCellVolume *
        quotientTransportJacobian sourceCross targetCross) =
      sourceDensity * sourceCellVolume := by
  have hsourceQ : (quotientMetricDeterminant sourceCross : ℚ) ≠ 0 := by
    exact_mod_cast hsource
  have htargetQ : (quotientMetricDeterminant targetCross : ℚ) ≠ 0 := by
    exact_mod_cast htarget
  unfold quotientMetricDensityMultiplier quotientTransportJacobian
  field_simp [hsourceQ, htargetQ]
  ring

theorem reference_one_to_zero_density_transport :
    quotientSymmetricDensityMultiplier 1 0 = (3 : ℚ) / 2 ∧
      quotientAntisymmetricDensityMultiplier 1 0 = (1 : ℚ) / 2 ∧
      quotientMetricDensityMultiplier 1 0 = (3 : ℚ) / 4 ∧
      quotientTransportJacobian 1 0 = (4 : ℚ) / 3 := by
  norm_num [quotientSymmetricDensityMultiplier,
    quotientAntisymmetricDensityMultiplier,
    quotientMetricDensityMultiplier, quotientTransportJacobian,
    quotientSymmetricWeight, quotientAntisymmetricWeight,
    quotientMetricDeterminant]

theorem reference_zero_to_one_density_transport :
    quotientSymmetricDensityMultiplier 0 1 = (2 : ℚ) / 3 ∧
      quotientAntisymmetricDensityMultiplier 0 1 = (2 : ℚ) ∧
      quotientMetricDensityMultiplier 0 1 = (4 : ℚ) / 3 ∧
      quotientTransportJacobian 0 1 = (3 : ℚ) / 4 := by
  norm_num [quotientSymmetricDensityMultiplier,
    quotientAntisymmetricDensityMultiplier,
    quotientMetricDensityMultiplier, quotientTransportJacobian,
    quotientSymmetricWeight, quotientAntisymmetricWeight,
    quotientMetricDeterminant]

theorem reference_full_rank_round_trip_density_preserved :
    quotientMetricDensityMultiplier 1 0 *
        quotientMetricDensityMultiplier 0 1 = 1 ∧
      quotientMetricDensityMultiplier 0 1 *
        quotientMetricDensityMultiplier 1 0 = 1 := by
  norm_num [quotientMetricDensityMultiplier, quotientMetricDeterminant]

theorem full_rank_to_full_coherence_is_singular_measure_boundary
    (sourceCross : ℤ)
    (hsource : quotientMetricDeterminant sourceCross ≠ 0) :
    quotientMetricDeterminant 2 = 0 ∧
      quotientTransportJacobian sourceCross 2 = 0 := by
  constructor
  · norm_num [quotientMetricDeterminant]
  · have hsourceQ : (quotientMetricDeterminant sourceCross : ℚ) ≠ 0 := by
      exact_mod_cast hsource
    simp [quotientTransportJacobian, quotientMetricDeterminant, hsourceQ]

theorem full_coherence_source_has_no_two_dimensional_density
    (targetCross : ℤ) :
    quotientMetricDeterminant 2 = 0 ∧
      transportDeterminantNumerator 2 targetCross = 0 := by
  constructor
  · exact (full_coherence_source_has_no_two_dimensional_jacobian targetCross).1
  · exact (full_coherence_source_has_no_two_dimensional_jacobian targetCross).2.2

structure QuotientMetricDensityTransportRadonNikodymCocycleCertificate where
  sourceMemoryOSV053Bound : Bool
  sourceMemoryOSV052TransportBound : Bool
  allDensityMultipliersExact : Bool
  allModeDensityProductsExact : Bool
  allFiniteSupportPushforwardPullbackWitnessesExact : Bool
  allRadonNikodymCocyclesExact : Bool
  fullRankRoundTripDensityPreserved : Bool
  singularMeasureBoundarySeparated : Bool
  rankOneDensityRecoveryNotClaimed : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV053Mutated : Bool
  sourceMemoryOSV052Mutated : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

theorem certificate_grants_no_authority
    (certificate : QuotientMetricDensityTransportRadonNikodymCocycleCertificate)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hsource53 : certificate.sourceMemoryOSV053Mutated = false)
    (hsource52 : certificate.sourceMemoryOSV052Mutated = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidateSelectionPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV053Mutated = false ∧
      certificate.sourceMemoryOSV052Mutated = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hselection, hexecution, hsource53, hsource52, hworld,
    hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSQuotientMetricDensityTransportRadonNikodymCocycleV0_54
