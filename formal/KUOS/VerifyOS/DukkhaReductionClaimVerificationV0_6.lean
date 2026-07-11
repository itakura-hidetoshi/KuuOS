import Mathlib
import KUOS.VerifyOS.BoundedPlanMiddleWayVerificationV0_5

namespace KUOS.VerifyOS.DukkhaReductionClaimVerificationV0_6

open KUOS.VerifyOS.BoundedPlanMiddleWayVerificationV0_5

inductive DukkhaDimension where
  | misfit
  | updateLag
  | attachmentRigidity
  | relationalCurvature
  | structuralConstraint
  | uncertaintyBurden
  deriving DecidableEq, Repr

inductive DukkhaReductionClaimStatus where
  | supported
  | indeterminate
  | contradicted
  deriving DecidableEq, Repr

inductive DukkhaVerificationDisposition where
  | supportedForMaterializationIntake
  | additionalEvidenceRequired
  | returnToPlanOSRevision
  deriving DecidableEq, Repr


def dispositionForClaim
    (status : DukkhaReductionClaimStatus) : DukkhaVerificationDisposition :=
  match status with
  | .supported => .supportedForMaterializationIntake
  | .indeterminate => .additionalEvidenceRequired
  | .contradicted => .returnToPlanOSRevision


def admittedForClaim (status : DukkhaReductionClaimStatus) : Bool :=
  status = .supported


structure DukkhaReductionClaimVerificationCertificate where
  sourceCertificate : BoundedPlanMiddleWayVerificationCertificate
  claimStatus : DukkhaReductionClaimStatus
  verificationDisposition : DukkhaVerificationDisposition
  materializationIntakeAdmitted : Bool
  dukkhaVectorPreserved : Bool
  singleScalarUtilityForbidden : Bool
  observationIntegrityPreserved : Bool
  adverseEvidenceRetained : Bool
  precisionCollapseNotUsed : Bool
  modelFamilyNarrowingNotUsed : Bool
  uncertaintyDisclosed : Bool
  structuralSufferingAcknowledged : Bool
  agencyPreserved : Bool
  dissentPreserved : Bool
  minorityPreserved : Bool
  futureBurdenAssessed : Bool
  causalModelNotTruth : Bool
  avoidableDukkhaNonworseningSupported : Bool
  atLeastOneAvoidableDimensionImproved : Bool
  attachmentRigidityNotIncreased : Bool
  relationalCurvatureNotHidden : Bool
  persistentLoopGainReduced : Bool
  modelRevisionCapacityPreserved : Bool
  protectedGroupSufferingNotExternalized : Bool
  futureSufferingNotExternalized : Bool
  sourcePlanPreserved : Bool
  sourceLineage : Finset String
  resultingLineage : Finset String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  selectionRemainsDecisionOSOwned : Bool
  selectionAuthorityGrantedToVerifyOS : Bool
  planRevisionAuthorityGrantedToVerifyOS : Bool
  dukkhaMinimizationAuthorityGrantedToVerifyOS : Bool
  planActivated : Bool
  materializationPerformed : Bool
  executionAuthorityGranted : Bool
  executionPermission : Bool
  persistentWorldStateChanged : Bool
  activeNow : Bool
  dispositionMatches :
    verificationDisposition = dispositionForClaim claimStatus
  admissionMatches :
    materializationIntakeAdmitted = admittedForClaim claimStatus
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility


structure DukkhaReductionClaimVerificationCertificateValid
    (certificate : DukkhaReductionClaimVerificationCertificate) : Prop where
  source_valid :
    BoundedPlanMiddleWayVerificationCertificateValid certificate.sourceCertificate
  dukkha_vector_preserved : certificate.dukkhaVectorPreserved = true
  single_scalar_utility_forbidden :
    certificate.singleScalarUtilityForbidden = true
  observation_integrity_preserved :
    certificate.observationIntegrityPreserved = true
  adverse_evidence_retained : certificate.adverseEvidenceRetained = true
  precision_collapse_not_used : certificate.precisionCollapseNotUsed = true
  model_family_narrowing_not_used :
    certificate.modelFamilyNarrowingNotUsed = true
  uncertainty_disclosed : certificate.uncertaintyDisclosed = true
  structural_suffering_acknowledged :
    certificate.structuralSufferingAcknowledged = true
  agency_preserved : certificate.agencyPreserved = true
  dissent_preserved : certificate.dissentPreserved = true
  minority_preserved : certificate.minorityPreserved = true
  future_burden_assessed : certificate.futureBurdenAssessed = true
  causal_model_not_truth : certificate.causalModelNotTruth = true
  source_plan_preserved : certificate.sourcePlanPreserved = true
  selection_remains_decisionos_owned :
    certificate.selectionRemainsDecisionOSOwned = true
  selection_authority_not_granted :
    certificate.selectionAuthorityGrantedToVerifyOS = false
  plan_revision_authority_not_granted :
    certificate.planRevisionAuthorityGrantedToVerifyOS = false
  dukkha_minimization_authority_not_granted :
    certificate.dukkhaMinimizationAuthorityGrantedToVerifyOS = false
  plan_not_activated : certificate.planActivated = false
  materialization_not_performed : certificate.materializationPerformed = false
  execution_authority_not_granted :
    certificate.executionAuthorityGranted = false
  execution_permission_false : certificate.executionPermission = false
  persistent_world_state_unchanged :
    certificate.persistentWorldStateChanged = false
  active_now_false : certificate.activeNow = false


theorem supported_claim_admits_materialization_intake
    (certificate : DukkhaReductionClaimVerificationCertificate)
    (supported : certificate.claimStatus = .supported) :
    certificate.verificationDisposition = .supportedForMaterializationIntake ∧
      certificate.materializationIntakeAdmitted = true := by
  constructor
  · calc
      certificate.verificationDisposition =
          dispositionForClaim certificate.claimStatus :=
        certificate.dispositionMatches
      _ = .supportedForMaterializationIntake := by
        simp [dispositionForClaim, supported]
  · calc
      certificate.materializationIntakeAdmitted =
          admittedForClaim certificate.claimStatus :=
        certificate.admissionMatches
      _ = true := by simp [admittedForClaim, supported]


theorem indeterminate_claim_requires_additional_evidence
    (certificate : DukkhaReductionClaimVerificationCertificate)
    (indeterminate : certificate.claimStatus = .indeterminate) :
    certificate.verificationDisposition = .additionalEvidenceRequired ∧
      certificate.materializationIntakeAdmitted = false := by
  constructor
  · calc
      certificate.verificationDisposition =
          dispositionForClaim certificate.claimStatus :=
        certificate.dispositionMatches
      _ = .additionalEvidenceRequired := by
        simp [dispositionForClaim, indeterminate]
  · calc
      certificate.materializationIntakeAdmitted =
          admittedForClaim certificate.claimStatus :=
        certificate.admissionMatches
      _ = false := by simp [admittedForClaim, indeterminate]


theorem contradicted_claim_returns_to_planos_revision
    (certificate : DukkhaReductionClaimVerificationCertificate)
    (contradicted : certificate.claimStatus = .contradicted) :
    certificate.verificationDisposition = .returnToPlanOSRevision ∧
      certificate.materializationIntakeAdmitted = false := by
  constructor
  · calc
      certificate.verificationDisposition =
          dispositionForClaim certificate.claimStatus :=
        certificate.dispositionMatches
      _ = .returnToPlanOSRevision := by
        simp [dispositionForClaim, contradicted]
  · calc
      certificate.materializationIntakeAdmitted =
          admittedForClaim certificate.claimStatus :=
        certificate.admissionMatches
      _ = false := by simp [admittedForClaim, contradicted]


theorem verification_preserves_vector_without_scalar_collapse
    (certificate : DukkhaReductionClaimVerificationCertificate)
    (valid : DukkhaReductionClaimVerificationCertificateValid certificate) :
    certificate.dukkhaVectorPreserved = true ∧
      certificate.singleScalarUtilityForbidden = true := by
  exact ⟨valid.dukkha_vector_preserved,
    valid.single_scalar_utility_forbidden⟩


theorem observation_and_uncertainty_integrity_are_preserved
    (certificate : DukkhaReductionClaimVerificationCertificate)
    (valid : DukkhaReductionClaimVerificationCertificateValid certificate) :
    certificate.observationIntegrityPreserved = true ∧
      certificate.adverseEvidenceRetained = true ∧
      certificate.precisionCollapseNotUsed = true ∧
      certificate.modelFamilyNarrowingNotUsed = true ∧
      certificate.uncertaintyDisclosed = true := by
  exact ⟨valid.observation_integrity_preserved,
    valid.adverse_evidence_retained,
    valid.precision_collapse_not_used,
    valid.model_family_narrowing_not_used,
    valid.uncertainty_disclosed⟩


theorem structural_suffering_is_acknowledged_without_reification
    (certificate : DukkhaReductionClaimVerificationCertificate)
    (valid : DukkhaReductionClaimVerificationCertificateValid certificate) :
    certificate.structuralSufferingAcknowledged = true ∧
      certificate.causalModelNotTruth = true := by
  exact ⟨valid.structural_suffering_acknowledged,
    valid.causal_model_not_truth⟩


theorem agency_dissent_minority_and_future_are_preserved
    (certificate : DukkhaReductionClaimVerificationCertificate)
    (valid : DukkhaReductionClaimVerificationCertificateValid certificate) :
    certificate.agencyPreserved = true ∧
      certificate.dissentPreserved = true ∧
      certificate.minorityPreserved = true ∧
      certificate.futureBurdenAssessed = true := by
  exact ⟨valid.agency_preserved,
    valid.dissent_preserved,
    valid.minority_preserved,
    valid.future_burden_assessed⟩


theorem verification_preserves_lineage_and_responsibility
    (certificate : DukkhaReductionClaimVerificationCertificate) :
    certificate.sourceLineage ⊆ certificate.resultingLineage ∧
      certificate.sourceResponsibility ⊆ certificate.resultingResponsibility := by
  exact ⟨certificate.lineageMonotone, certificate.responsibilityMonotone⟩


theorem verification_grants_no_selection_revision_or_minimization_authority
    (certificate : DukkhaReductionClaimVerificationCertificate)
    (valid : DukkhaReductionClaimVerificationCertificateValid certificate) :
    certificate.selectionRemainsDecisionOSOwned = true ∧
      certificate.selectionAuthorityGrantedToVerifyOS = false ∧
      certificate.planRevisionAuthorityGrantedToVerifyOS = false ∧
      certificate.dukkhaMinimizationAuthorityGrantedToVerifyOS = false := by
  exact ⟨valid.selection_remains_decisionos_owned,
    valid.selection_authority_not_granted,
    valid.plan_revision_authority_not_granted,
    valid.dukkha_minimization_authority_not_granted⟩


theorem verification_is_not_activation_materialization_or_execution
    (certificate : DukkhaReductionClaimVerificationCertificate)
    (valid : DukkhaReductionClaimVerificationCertificateValid certificate) :
    certificate.planActivated = false ∧
      certificate.materializationPerformed = false ∧
      certificate.executionAuthorityGranted = false ∧
      certificate.executionPermission = false ∧
      certificate.persistentWorldStateChanged = false ∧
      certificate.activeNow = false := by
  exact ⟨valid.plan_not_activated,
    valid.materialization_not_performed,
    valid.execution_authority_not_granted,
    valid.execution_permission_false,
    valid.persistent_world_state_unchanged,
    valid.active_now_false⟩

end KUOS.VerifyOS.DukkhaReductionClaimVerificationV0_6
