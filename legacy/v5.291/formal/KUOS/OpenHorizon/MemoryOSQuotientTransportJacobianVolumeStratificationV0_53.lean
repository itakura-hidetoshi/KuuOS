import Mathlib
import KUOS.OpenHorizon.MemoryOSQuotientMetricCovectorTransportV0_52

namespace KUOS.OpenHorizon.MemoryOSQuotientTransportJacobianVolumeStratificationV0_53

open KUOS.OpenHorizon.MemoryOSCandidateQuotientModeDiagonalizationInverseV0_51
open KUOS.OpenHorizon.MemoryOSQuotientMetricCovectorTransportV0_52

def transportSymmetricEigenNumerator
    (sourceCross targetCross : ℤ) : ℤ :=
  quotientSymmetricWeight targetCross *
    quotientAntisymmetricWeight sourceCross

def transportAntisymmetricEigenNumerator
    (sourceCross targetCross : ℤ) : ℤ :=
  quotientAntisymmetricWeight targetCross *
    quotientSymmetricWeight sourceCross

def transportDeterminantNumerator
    (sourceCross targetCross : ℤ) : ℤ :=
  transportSymmetricEigenNumerator sourceCross targetCross *
    transportAntisymmetricEigenNumerator sourceCross targetCross

 theorem transport_symmetric_mode_eigenvector
    (sourceCross targetCross amplitude : ℤ) :
    quotientCovectorTransportFirst
        sourceCross targetCross amplitude amplitude =
        transportSymmetricEigenNumerator sourceCross targetCross * amplitude ∧
      quotientCovectorTransportSecond
        sourceCross targetCross amplitude amplitude =
        transportSymmetricEigenNumerator sourceCross targetCross * amplitude := by
  constructor <;>
    simp [quotientCovectorTransportFirst, quotientCovectorTransportSecond,
      quotientMetricActionFirst, quotientMetricActionSecond,
      quotientAdjugateActionFirst, quotientAdjugateActionSecond,
      transportSymmetricEigenNumerator, quotientSymmetricWeight,
      quotientAntisymmetricWeight] <;>
    ring

theorem transport_antisymmetric_mode_eigenvector
    (sourceCross targetCross amplitude : ℤ) :
    quotientCovectorTransportFirst
        sourceCross targetCross amplitude (-amplitude) =
        transportAntisymmetricEigenNumerator sourceCross targetCross * amplitude ∧
      quotientCovectorTransportSecond
        sourceCross targetCross amplitude (-amplitude) =
        -(transportAntisymmetricEigenNumerator sourceCross targetCross * amplitude) := by
  constructor <;>
    simp [quotientCovectorTransportFirst, quotientCovectorTransportSecond,
      quotientMetricActionFirst, quotientMetricActionSecond,
      quotientAdjugateActionFirst, quotientAdjugateActionSecond,
      transportAntisymmetricEigenNumerator, quotientSymmetricWeight,
      quotientAntisymmetricWeight] <;>
    ring

theorem transport_symmetric_multiplier_scaled
    (sourceCross targetCross : ℤ) :
    quotientSymmetricWeight sourceCross *
        transportSymmetricEigenNumerator sourceCross targetCross =
      quotientMetricDeterminant sourceCross *
        quotientSymmetricWeight targetCross := by
  simp [transportSymmetricEigenNumerator, quotientSymmetricWeight,
    quotientAntisymmetricWeight, quotientMetricDeterminant]
  ring

theorem transport_antisymmetric_multiplier_scaled
    (sourceCross targetCross : ℤ) :
    quotientAntisymmetricWeight sourceCross *
        transportAntisymmetricEigenNumerator sourceCross targetCross =
      quotientMetricDeterminant sourceCross *
        quotientAntisymmetricWeight targetCross := by
  simp [transportAntisymmetricEigenNumerator, quotientSymmetricWeight,
    quotientAntisymmetricWeight, quotientMetricDeterminant]
  ring

theorem transport_determinant_factorization
    (sourceCross targetCross : ℤ) :
    transportDeterminantNumerator sourceCross targetCross =
      quotientMetricDeterminant sourceCross *
        quotientMetricDeterminant targetCross := by
  simp [transportDeterminantNumerator, transportSymmetricEigenNumerator,
    transportAntisymmetricEigenNumerator, quotientSymmetricWeight,
    quotientAntisymmetricWeight, quotientMetricDeterminant]
  ring

theorem transport_symmetric_mode_composition
    (sourceCross middleCross targetCross : ℤ) :
    transportSymmetricEigenNumerator middleCross targetCross *
        transportSymmetricEigenNumerator sourceCross middleCross =
      quotientMetricDeterminant middleCross *
        transportSymmetricEigenNumerator sourceCross targetCross := by
  simp [transportSymmetricEigenNumerator, quotientSymmetricWeight,
    quotientAntisymmetricWeight, quotientMetricDeterminant]
  ring

theorem transport_antisymmetric_mode_composition
    (sourceCross middleCross targetCross : ℤ) :
    transportAntisymmetricEigenNumerator middleCross targetCross *
        transportAntisymmetricEigenNumerator sourceCross middleCross =
      quotientMetricDeterminant middleCross *
        transportAntisymmetricEigenNumerator sourceCross targetCross := by
  simp [transportAntisymmetricEigenNumerator, quotientSymmetricWeight,
    quotientAntisymmetricWeight, quotientMetricDeterminant]
  ring

theorem transport_determinant_composition
    (sourceCross middleCross targetCross : ℤ) :
    transportDeterminantNumerator middleCross targetCross *
        transportDeterminantNumerator sourceCross middleCross =
      quotientMetricDeterminant middleCross *
        quotientMetricDeterminant middleCross *
        transportDeterminantNumerator sourceCross targetCross := by
  simp [transportDeterminantNumerator, transportSymmetricEigenNumerator,
    transportAntisymmetricEigenNumerator, quotientSymmetricWeight,
    quotientAntisymmetricWeight, quotientMetricDeterminant]
  ring

theorem reference_one_to_zero_mode_jacobian :
    transportSymmetricEigenNumerator 1 0 = 2 ∧
      transportAntisymmetricEigenNumerator 1 0 = 6 ∧
      quotientMetricDeterminant 1 = 3 ∧
      transportDeterminantNumerator 1 0 = 12 ∧
      3 * 4 = 12 := by
  norm_num [transportSymmetricEigenNumerator,
    transportAntisymmetricEigenNumerator, transportDeterminantNumerator,
    quotientSymmetricWeight, quotientAntisymmetricWeight,
    quotientMetricDeterminant]

theorem reference_zero_to_one_mode_jacobian :
    transportSymmetricEigenNumerator 0 1 = 6 ∧
      transportAntisymmetricEigenNumerator 0 1 = 2 ∧
      quotientMetricDeterminant 0 = 4 ∧
      transportDeterminantNumerator 0 1 = 12 ∧
      4 * 3 = 12 := by
  norm_num [transportSymmetricEigenNumerator,
    transportAntisymmetricEigenNumerator, transportDeterminantNumerator,
    quotientSymmetricWeight, quotientAntisymmetricWeight,
    quotientMetricDeterminant]

theorem reference_full_rank_round_trip_mode_scaling :
    transportSymmetricEigenNumerator 1 0 *
        transportSymmetricEigenNumerator 0 1 = 12 ∧
      transportAntisymmetricEigenNumerator 1 0 *
        transportAntisymmetricEigenNumerator 0 1 = 12 ∧
      quotientMetricDeterminant 1 * quotientMetricDeterminant 0 = 12 := by
  norm_num [transportSymmetricEigenNumerator,
    transportAntisymmetricEigenNumerator, quotientSymmetricWeight,
    quotientAntisymmetricWeight, quotientMetricDeterminant]

theorem full_coherence_source_has_no_two_dimensional_jacobian
    (targetCross : ℤ) :
    quotientMetricDeterminant 2 = 0 ∧
      transportSymmetricEigenNumerator 2 targetCross = 0 ∧
      transportDeterminantNumerator 2 targetCross = 0 := by
  simp [quotientMetricDeterminant, transportSymmetricEigenNumerator,
    transportDeterminantNumerator, transportAntisymmetricEigenNumerator,
    quotientSymmetricWeight, quotientAntisymmetricWeight]

theorem full_coherence_antisymmetric_information_not_recoverable
    (leftAntisymmetric rightAntisymmetric : ℤ) :
    quotientAntisymmetricDual 2 leftAntisymmetric =
        quotientAntisymmetricDual 2 rightAntisymmetric := by
  simp [quotientAntisymmetricDual, quotientAntisymmetricWeight]

structure QuotientTransportJacobianVolumeStratificationCertificate where
  sourceMemoryOSV052Bound : Bool
  sourceMemoryOSV051Bound : Bool
  allModeEigenvaluesExact : Bool
  allTransportDeterminantsExact : Bool
  allFullRankJacobiansExact : Bool
  allModeCompositionIdentitiesExact : Bool
  rankOneBoundaryHasNoVolumeJacobian : Bool
  antisymmetricRecoveryNotClaimed : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV052Mutated : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

theorem certificate_grants_no_authority
    (certificate : QuotientTransportJacobianVolumeStratificationCertificate)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hsource : certificate.sourceMemoryOSV052Mutated = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidateSelectionPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV052Mutated = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hselection, hexecution, hsource, hworld, hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSQuotientTransportJacobianVolumeStratificationV0_53
