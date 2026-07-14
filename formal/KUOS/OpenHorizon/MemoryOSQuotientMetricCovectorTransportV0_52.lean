import Mathlib
import KUOS.OpenHorizon.MemoryOSCandidateQuotientModeDiagonalizationInverseV0_51

namespace KUOS.OpenHorizon.MemoryOSQuotientMetricCovectorTransportV0_52

open KUOS.OpenHorizon.MemoryOSCandidateQuotientModeDiagonalizationInverseV0_51

def quotientCovectorTransportFirst
    (sourceCross targetCross first second : ℤ) : ℤ :=
  quotientMetricActionFirst
    targetCross
    (quotientAdjugateActionFirst sourceCross first second)
    (quotientAdjugateActionSecond sourceCross first second)

def quotientCovectorTransportSecond
    (sourceCross targetCross first second : ℤ) : ℤ :=
  quotientMetricActionSecond
    targetCross
    (quotientAdjugateActionFirst sourceCross first second)
    (quotientAdjugateActionSecond sourceCross first second)

def quotientSymmetricDual (cross symmetricCoordinate : ℤ) : ℤ :=
  quotientSymmetricWeight cross * symmetricCoordinate

def quotientAntisymmetricDual (cross antisymmetricCoordinate : ℤ) : ℤ :=
  quotientAntisymmetricWeight cross * antisymmetricCoordinate

theorem quotient_covector_transport_scaled
    (sourceCross targetCross first second : ℤ) :
    quotientCovectorTransportFirst
        sourceCross targetCross
        (quotientMetricActionFirst sourceCross first second)
        (quotientMetricActionSecond sourceCross first second) =
        quotientMetricDeterminant sourceCross *
          quotientMetricActionFirst targetCross first second ∧
      quotientCovectorTransportSecond
        sourceCross targetCross
        (quotientMetricActionFirst sourceCross first second)
        (quotientMetricActionSecond sourceCross first second) =
        quotientMetricDeterminant sourceCross *
          quotientMetricActionSecond targetCross first second := by
  simp [quotientCovectorTransportFirst, quotientCovectorTransportSecond,
    quotientMetricActionFirst, quotientMetricActionSecond,
    quotientAdjugateActionFirst, quotientAdjugateActionSecond,
    quotientMetricDeterminant]
  constructor <;> ring

theorem quotient_covector_transport_composition
    (sourceCross middleCross targetCross first second : ℤ) :
    quotientCovectorTransportFirst
        middleCross targetCross
        (quotientCovectorTransportFirst
          sourceCross middleCross first second)
        (quotientCovectorTransportSecond
          sourceCross middleCross first second) =
        quotientMetricDeterminant middleCross *
          quotientCovectorTransportFirst
            sourceCross targetCross first second ∧
      quotientCovectorTransportSecond
        middleCross targetCross
        (quotientCovectorTransportFirst
          sourceCross middleCross first second)
        (quotientCovectorTransportSecond
          sourceCross middleCross first second) =
        quotientMetricDeterminant middleCross *
          quotientCovectorTransportSecond
            sourceCross targetCross first second := by
  simp [quotientCovectorTransportFirst, quotientCovectorTransportSecond,
    quotientMetricActionFirst, quotientMetricActionSecond,
    quotientAdjugateActionFirst, quotientAdjugateActionSecond,
    quotientMetricDeterminant]
  constructor <;> ring

theorem quotient_covector_transport_identity_scaled
    (cross first second : ℤ) :
    quotientCovectorTransportFirst cross cross first second =
        quotientMetricDeterminant cross * first ∧
      quotientCovectorTransportSecond cross cross first second =
        quotientMetricDeterminant cross * second := by
  simp [quotientCovectorTransportFirst, quotientCovectorTransportSecond,
    quotientMetricActionFirst, quotientMetricActionSecond,
    quotientAdjugateActionFirst, quotientAdjugateActionSecond,
    quotientMetricDeterminant]
  constructor <;> ring

theorem full_rank_one_to_zero_transport_matrix
    (first second : ℤ) :
    quotientCovectorTransportFirst 1 0 first second =
        4 * first - 2 * second ∧
      quotientCovectorTransportSecond 1 0 first second =
        -2 * first + 4 * second := by
  norm_num [quotientCovectorTransportFirst, quotientCovectorTransportSecond,
    quotientMetricActionFirst, quotientMetricActionSecond,
    quotientAdjugateActionFirst, quotientAdjugateActionSecond]
  constructor <;> ring

theorem full_rank_zero_to_one_transport_matrix
    (first second : ℤ) :
    quotientCovectorTransportFirst 0 1 first second =
        4 * first + 2 * second ∧
      quotientCovectorTransportSecond 0 1 first second =
        2 * first + 4 * second := by
  norm_num [quotientCovectorTransportFirst, quotientCovectorTransportSecond,
    quotientMetricActionFirst, quotientMetricActionSecond,
    quotientAdjugateActionFirst, quotientAdjugateActionSecond]
  constructor <;> ring

theorem full_rank_one_zero_round_trip
    (first second : ℤ) :
    quotientCovectorTransportFirst
        0 1
        (quotientCovectorTransportFirst 1 0 first second)
        (quotientCovectorTransportSecond 1 0 first second) =
        12 * first ∧
      quotientCovectorTransportSecond
        0 1
        (quotientCovectorTransportFirst 1 0 first second)
        (quotientCovectorTransportSecond 1 0 first second) =
        12 * second := by
  norm_num [quotientCovectorTransportFirst, quotientCovectorTransportSecond,
    quotientMetricActionFirst, quotientMetricActionSecond,
    quotientAdjugateActionFirst, quotientAdjugateActionSecond]
  constructor <;> ring

theorem full_coherence_symmetric_partial_transport
    (targetCross symmetricCoordinate : ℤ) :
    4 * quotientSymmetricDual targetCross symmetricCoordinate =
      quotientSymmetricWeight targetCross *
        quotientSymmetricDual 2 symmetricCoordinate := by
  simp [quotientSymmetricDual, quotientSymmetricWeight]
  ring

theorem full_coherence_antisymmetric_dual_erased
    (antisymmetricCoordinate : ℤ) :
    quotientAntisymmetricDual 2 antisymmetricCoordinate = 0 := by
  simp [quotientAntisymmetricDual, quotientAntisymmetricWeight]

theorem full_coherence_dual_independent_of_antisymmetric
    (symmetricCoordinate leftAntisymmetric rightAntisymmetric : ℤ) :
    quotientSymmetricDual 2 symmetricCoordinate =
        quotientSymmetricDual 2 symmetricCoordinate ∧
      quotientAntisymmetricDual 2 leftAntisymmetric =
        quotientAntisymmetricDual 2 rightAntisymmetric := by
  simp [quotientSymmetricDual, quotientAntisymmetricDual,
    quotientSymmetricWeight, quotientAntisymmetricWeight]

theorem partial_dephasing_one_recovers_antisymmetric_dual
    (antisymmetricCoordinate : ℤ) :
    quotientAntisymmetricDual 1 antisymmetricCoordinate =
      antisymmetricCoordinate := by
  simp [quotientAntisymmetricDual, quotientAntisymmetricWeight]

structure QuotientMetricCovectorTransportCertificate where
  sourceMemoryOSV051Bound : Bool
  sourceMemoryOSV050Bound : Bool
  allScaledTransportIdentitiesExact : Bool
  allCompositionIdentitiesExact : Bool
  fullRankRationalTransportExact : Bool
  rankOneBoundaryPartialTransportExact : Bool
  antisymmetricRecoveryNotClaimedAtBoundary : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV051Mutated : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

theorem certificate_grants_no_authority
    (certificate : QuotientMetricCovectorTransportCertificate)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hsource : certificate.sourceMemoryOSV051Mutated = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidateSelectionPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV051Mutated = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hselection, hexecution, hsource, hworld, hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSQuotientMetricCovectorTransportV0_52
