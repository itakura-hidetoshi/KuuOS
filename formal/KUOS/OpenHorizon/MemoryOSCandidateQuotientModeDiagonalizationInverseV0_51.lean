import Mathlib
import KUOS.OpenHorizon.MemoryOSCandidateQuotientCoordinateCanonicalizationV0_50

namespace KUOS.OpenHorizon.MemoryOSCandidateQuotientModeDiagonalizationInverseV0_51

open KUOS.OpenHorizon.MemoryOSCandidateQuotientCoordinateCanonicalizationV0_50

def quotientSymmetricMode (first second : ℤ) : ℤ :=
  first + second

def quotientAntisymmetricMode (first second : ℤ) : ℤ :=
  first - second

def quotientSymmetricWeight (cross : ℤ) : ℤ :=
  2 + cross

def quotientAntisymmetricWeight (cross : ℤ) : ℤ :=
  2 - cross

def quotientMetricDeterminant (cross : ℤ) : ℤ :=
  4 - cross * cross

def quotientMetricActionFirst
    (cross first second : ℤ) : ℤ :=
  2 * first + cross * second

def quotientMetricActionSecond
    (cross first second : ℤ) : ℤ :=
  cross * first + 2 * second

def quotientAdjugateActionFirst
    (cross first second : ℤ) : ℤ :=
  2 * first - cross * second

def quotientAdjugateActionSecond
    (cross first second : ℤ) : ℤ :=
  -cross * first + 2 * second

def quotientModeQuadraticNumerator
    (cross first second : ℤ) : ℤ :=
  quotientSymmetricWeight cross *
      quotientSymmetricMode first second *
      quotientSymmetricMode first second +
    quotientAntisymmetricWeight cross *
      quotientAntisymmetricMode first second *
      quotientAntisymmetricMode first second

def quotientModeBilinearNumerator
    (cross leftFirst leftSecond rightFirst rightSecond : ℤ) : ℤ :=
  quotientSymmetricWeight cross *
      quotientSymmetricMode leftFirst leftSecond *
      quotientSymmetricMode rightFirst rightSecond +
    quotientAntisymmetricWeight cross *
      quotientAntisymmetricMode leftFirst leftSecond *
      quotientAntisymmetricMode rightFirst rightSecond

theorem quotient_metric_quadratic_mode_diagonalization
    (cross first second : ℤ) :
    2 * candidateHistoryBilinear
          cross first second first second =
      quotientModeQuadraticNumerator cross first second := by
  simp [candidateHistoryBilinear, quotientModeQuadraticNumerator,
    quotientSymmetricWeight, quotientAntisymmetricWeight,
    quotientSymmetricMode, quotientAntisymmetricMode]
  ring

theorem quotient_metric_bilinear_mode_diagonalization
    (cross leftFirst leftSecond rightFirst rightSecond : ℤ) :
    2 * candidateHistoryBilinear
          cross leftFirst leftSecond rightFirst rightSecond =
      quotientModeBilinearNumerator
        cross leftFirst leftSecond rightFirst rightSecond := by
  simp [candidateHistoryBilinear, quotientModeBilinearNumerator,
    quotientSymmetricWeight, quotientAntisymmetricWeight,
    quotientSymmetricMode, quotientAntisymmetricMode]
  ring

theorem symmetric_mode_eigenvector
    (cross amplitude : ℤ) :
    quotientMetricActionFirst cross amplitude amplitude =
        quotientSymmetricWeight cross * amplitude ∧
      quotientMetricActionSecond cross amplitude amplitude =
        quotientSymmetricWeight cross * amplitude := by
  simp [quotientMetricActionFirst, quotientMetricActionSecond,
    quotientSymmetricWeight]
  constructor <;> ring

theorem antisymmetric_mode_eigenvector
    (cross amplitude : ℤ) :
    quotientMetricActionFirst cross amplitude (-amplitude) =
        quotientAntisymmetricWeight cross * amplitude ∧
      quotientMetricActionSecond cross amplitude (-amplitude) =
        -(quotientAntisymmetricWeight cross * amplitude) := by
  simp [quotientMetricActionFirst, quotientMetricActionSecond,
    quotientAntisymmetricWeight]
  constructor <;> ring

theorem quotient_metric_determinant_factorization
    (cross : ℤ) :
    quotientMetricDeterminant cross =
      quotientSymmetricWeight cross * quotientAntisymmetricWeight cross := by
  simp [quotientMetricDeterminant, quotientSymmetricWeight,
    quotientAntisymmetricWeight]
  ring

theorem quotient_metric_adjugate_inverse_witness
    (cross first second : ℤ) :
    quotientMetricActionFirst
        cross
        (quotientAdjugateActionFirst cross first second)
        (quotientAdjugateActionSecond cross first second) =
        quotientMetricDeterminant cross * first ∧
      quotientMetricActionSecond
        cross
        (quotientAdjugateActionFirst cross first second)
        (quotientAdjugateActionSecond cross first second) =
        quotientMetricDeterminant cross * second := by
  simp [quotientMetricActionFirst, quotientMetricActionSecond,
    quotientAdjugateActionFirst, quotientAdjugateActionSecond,
    quotientMetricDeterminant]
  constructor <;> ring

theorem quotient_adjugate_metric_inverse_witness
    (cross first second : ℤ) :
    quotientAdjugateActionFirst
        cross
        (quotientMetricActionFirst cross first second)
        (quotientMetricActionSecond cross first second) =
        quotientMetricDeterminant cross * first ∧
      quotientAdjugateActionSecond
        cross
        (quotientMetricActionFirst cross first second)
        (quotientMetricActionSecond cross first second) =
        quotientMetricDeterminant cross * second := by
  simp [quotientMetricActionFirst, quotientMetricActionSecond,
    quotientAdjugateActionFirst, quotientAdjugateActionSecond,
    quotientMetricDeterminant]
  constructor <;> ring

theorem full_coherence_pairing_rank_one
    (leftFirst leftSecond rightFirst rightSecond : ℤ) :
    candidateHistoryBilinear
        2 leftFirst leftSecond rightFirst rightSecond =
      2 * quotientSymmetricMode leftFirst leftSecond *
        quotientSymmetricMode rightFirst rightSecond := by
  simp [candidateHistoryBilinear, quotientSymmetricMode]
  ring

theorem full_coherence_antisymmetric_mode_null
    (amplitude : ℤ) :
    quotientMetricActionFirst 2 amplitude (-amplitude) = 0 ∧
      quotientMetricActionSecond 2 amplitude (-amplitude) = 0 := by
  norm_num [quotientMetricActionFirst, quotientMetricActionSecond]

theorem partial_dephasing_one_inverse_witness
    (first second : ℤ) :
    quotientMetricActionFirst
        1
        (quotientAdjugateActionFirst 1 first second)
        (quotientAdjugateActionSecond 1 first second) =
        3 * first ∧
      quotientMetricActionSecond
        1
        (quotientAdjugateActionFirst 1 first second)
        (quotientAdjugateActionSecond 1 first second) =
        3 * second := by
  simpa [quotientMetricDeterminant] using
    quotient_metric_adjugate_inverse_witness 1 first second

theorem full_dephasing_zero_inverse_witness
    (first second : ℤ) :
    quotientMetricActionFirst
        0
        (quotientAdjugateActionFirst 0 first second)
        (quotientAdjugateActionSecond 0 first second) =
        4 * first ∧
      quotientMetricActionSecond
        0
        (quotientAdjugateActionFirst 0 first second)
        (quotientAdjugateActionSecond 0 first second) =
        4 * second := by
  simpa [quotientMetricDeterminant] using
    quotient_metric_adjugate_inverse_witness 0 first second

theorem reference_mode_weight_trajectory :
    quotientSymmetricWeight 2 = 4 ∧
      quotientAntisymmetricWeight 2 = 0 ∧
      quotientMetricDeterminant 2 = 0 ∧
      quotientSymmetricWeight 1 = 3 ∧
      quotientAntisymmetricWeight 1 = 1 ∧
      quotientMetricDeterminant 1 = 3 ∧
      quotientSymmetricWeight 0 = 2 ∧
      quotientAntisymmetricWeight 0 = 2 ∧
      quotientMetricDeterminant 0 = 4 := by
  norm_num [quotientSymmetricWeight, quotientAntisymmetricWeight,
    quotientMetricDeterminant]

theorem reference_mixed_probe_modes :
    quotientSymmetricMode 4 7 = 11 ∧
      quotientAntisymmetricMode 4 7 = -3 := by
  norm_num [quotientSymmetricMode, quotientAntisymmetricMode]

structure CandidateQuotientModeDiagonalizationInverseCertificate where
  sourceMemoryOSV050Bound : Bool
  sourceMemoryOSV048Bound : Bool
  symmetricModeEigenvectorExact : Bool
  antisymmetricModeEigenvectorExact : Bool
  allQuadraticEvidenceModeDiagonalized : Bool
  allBilinearPairingsModeDiagonalized : Bool
  determinantFactorizationExact : Bool
  fullCoherenceRankOneExact : Bool
  postDephasingInverseWitnessExact : Bool
  quotientRankTrajectoryPreserved : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV050Mutated : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

theorem certificate_grants_no_authority
    (certificate : CandidateQuotientModeDiagonalizationInverseCertificate)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hsource : certificate.sourceMemoryOSV050Mutated = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidateSelectionPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV050Mutated = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hselection, hexecution, hsource, hworld, hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSCandidateQuotientModeDiagonalizationInverseV0_51
