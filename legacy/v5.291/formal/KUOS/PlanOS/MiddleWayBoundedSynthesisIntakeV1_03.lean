import Mathlib
import KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4

namespace KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03

open KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4

inductive IntakeDisposition where
  | boundedSynthesisIntakeReady
  | awaitConditionChange
  | returnToDecisionOSRevision
  | successorLineageReverificationRequired
  | closeWithoutSynthesis
  | terminateWithoutSynthesis
  deriving DecidableEq, Repr


def dispositionForStatus : ConditionalValidityStatus → IntakeDisposition
  | .valid => .boundedSynthesisIntakeReady
  | .suspended => .awaitConditionChange
  | .revisionRequired => .returnToDecisionOSRevision
  | .superseded => .successorLineageReverificationRequired
  | .completed => .closeWithoutSynthesis
  | .terminated => .terminateWithoutSynthesis


def admittedForStatus : ConditionalValidityStatus → Bool
  | .valid => true
  | .suspended => false
  | .revisionRequired => false
  | .superseded => false
  | .completed => false
  | .terminated => false


structure MiddleWayBoundedSynthesisIntakeCertificate where
  sourceTransitionKind : TransitionKind
  sourceConditionalValidityStatus : ConditionalValidityStatus
  intakeDisposition : IntakeDisposition
  sourceLineage : Finset String
  resultingLineage : Finset String
  predecessorReference : String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  sourceDissent : Finset String
  resultingDissent : Finset String
  sourceMinorityEvidence : Finset String
  resultingMinorityEvidence : Finset String
  transitionStatusMatches :
    sourceConditionalValidityStatus = statusForTransition sourceTransitionKind
  dispositionMatches :
    intakeDisposition = dispositionForStatus sourceConditionalValidityStatus
  lineageMonotone : sourceLineage ⊆ resultingLineage
  predecessorPreserved : predecessorReference ∈ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility
  dissentMonotone : sourceDissent ⊆ resultingDissent
  minorityEvidenceMonotone :
    sourceMinorityEvidence ⊆ resultingMinorityEvidence
  boundedSynthesisRequestAdmitted : Bool
  admissionExact :
    boundedSynthesisRequestAdmitted = admittedForStatus sourceConditionalValidityStatus
  selectionAuthorityGrantedToPlanOS : Bool
  planSynthesisPerformed : Bool
  concretePlanIssued : Bool
  executionAuthorityGranted : Bool
  executionPermission : Bool
  persistentWorldStateChanged : Bool
  activeNow : Bool


structure MiddleWayBoundedSynthesisIntakeCertificateValid
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate) : Prop where
  selection_authority_not_granted :
    certificate.selectionAuthorityGrantedToPlanOS = false
  plan_synthesis_not_performed : certificate.planSynthesisPerformed = false
  concrete_plan_not_issued : certificate.concretePlanIssued = false
  execution_authority_not_granted :
    certificate.executionAuthorityGranted = false
  execution_permission_false : certificate.executionPermission = false
  persistent_world_state_unchanged :
    certificate.persistentWorldStateChanged = false
  active_now_false : certificate.activeNow = false


theorem valid_status_admits_bounded_synthesis_intake
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate)
    (status : certificate.sourceConditionalValidityStatus = .valid) :
    certificate.intakeDisposition = .boundedSynthesisIntakeReady ∧
      certificate.boundedSynthesisRequestAdmitted = true := by
  constructor
  · calc
      certificate.intakeDisposition =
          dispositionForStatus certificate.sourceConditionalValidityStatus :=
        certificate.dispositionMatches
      _ = .boundedSynthesisIntakeReady := by
        simp [status, dispositionForStatus]
  · calc
      certificate.boundedSynthesisRequestAdmitted =
          admittedForStatus certificate.sourceConditionalValidityStatus :=
        certificate.admissionExact
      _ = true := by
        simp [status, admittedForStatus]


theorem suspended_status_routes_without_synthesis
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate)
    (status : certificate.sourceConditionalValidityStatus = .suspended) :
    certificate.intakeDisposition = .awaitConditionChange ∧
      certificate.boundedSynthesisRequestAdmitted = false := by
  constructor
  · calc
      certificate.intakeDisposition =
          dispositionForStatus certificate.sourceConditionalValidityStatus :=
        certificate.dispositionMatches
      _ = .awaitConditionChange := by
        simp [status, dispositionForStatus]
  · calc
      certificate.boundedSynthesisRequestAdmitted =
          admittedForStatus certificate.sourceConditionalValidityStatus :=
        certificate.admissionExact
      _ = false := by
        simp [status, admittedForStatus]


theorem revision_required_routes_to_decisionos
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate)
    (status : certificate.sourceConditionalValidityStatus = .revisionRequired) :
    certificate.intakeDisposition = .returnToDecisionOSRevision ∧
      certificate.boundedSynthesisRequestAdmitted = false := by
  constructor
  · calc
      certificate.intakeDisposition =
          dispositionForStatus certificate.sourceConditionalValidityStatus :=
        certificate.dispositionMatches
      _ = .returnToDecisionOSRevision := by
        simp [status, dispositionForStatus]
  · calc
      certificate.boundedSynthesisRequestAdmitted =
          admittedForStatus certificate.sourceConditionalValidityStatus :=
        certificate.admissionExact
      _ = false := by
        simp [status, admittedForStatus]


theorem superseded_status_requires_successor_reverification
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate)
    (status : certificate.sourceConditionalValidityStatus = .superseded) :
    certificate.intakeDisposition = .successorLineageReverificationRequired ∧
      certificate.boundedSynthesisRequestAdmitted = false := by
  constructor
  · calc
      certificate.intakeDisposition =
          dispositionForStatus certificate.sourceConditionalValidityStatus :=
        certificate.dispositionMatches
      _ = .successorLineageReverificationRequired := by
        simp [status, dispositionForStatus]
  · calc
      certificate.boundedSynthesisRequestAdmitted =
          admittedForStatus certificate.sourceConditionalValidityStatus :=
        certificate.admissionExact
      _ = false := by
        simp [status, admittedForStatus]


theorem completed_status_closes_without_synthesis
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate)
    (status : certificate.sourceConditionalValidityStatus = .completed) :
    certificate.intakeDisposition = .closeWithoutSynthesis ∧
      certificate.boundedSynthesisRequestAdmitted = false := by
  constructor
  · calc
      certificate.intakeDisposition =
          dispositionForStatus certificate.sourceConditionalValidityStatus :=
        certificate.dispositionMatches
      _ = .closeWithoutSynthesis := by
        simp [status, dispositionForStatus]
  · calc
      certificate.boundedSynthesisRequestAdmitted =
          admittedForStatus certificate.sourceConditionalValidityStatus :=
        certificate.admissionExact
      _ = false := by
        simp [status, admittedForStatus]


theorem terminated_status_terminates_without_synthesis
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate)
    (status : certificate.sourceConditionalValidityStatus = .terminated) :
    certificate.intakeDisposition = .terminateWithoutSynthesis ∧
      certificate.boundedSynthesisRequestAdmitted = false := by
  constructor
  · calc
      certificate.intakeDisposition =
          dispositionForStatus certificate.sourceConditionalValidityStatus :=
        certificate.dispositionMatches
      _ = .terminateWithoutSynthesis := by
        simp [status, dispositionForStatus]
  · calc
      certificate.boundedSynthesisRequestAdmitted =
          admittedForStatus certificate.sourceConditionalValidityStatus :=
        certificate.admissionExact
      _ = false := by
        simp [status, admittedForStatus]


theorem intake_preserves_source_lineage
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate)
    (digest : String)
    (sourceMember : digest ∈ certificate.sourceLineage) :
    digest ∈ certificate.resultingLineage := by
  exact certificate.lineageMonotone sourceMember


theorem intake_preserves_predecessor
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate) :
    certificate.predecessorReference ∈ certificate.resultingLineage := by
  exact certificate.predecessorPreserved


theorem intake_preserves_responsibility_dissent_and_minority_evidence
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate)
    (responsibility : String)
    (dissent : String)
    (minorityEvidence : String)
    (responsibilityMember : responsibility ∈ certificate.sourceResponsibility)
    (dissentMember : dissent ∈ certificate.sourceDissent)
    (minorityMember : minorityEvidence ∈ certificate.sourceMinorityEvidence) :
    responsibility ∈ certificate.resultingResponsibility ∧
      dissent ∈ certificate.resultingDissent ∧
      minorityEvidence ∈ certificate.resultingMinorityEvidence := by
  exact ⟨certificate.responsibilityMonotone responsibilityMember,
    certificate.dissentMonotone dissentMember,
    certificate.minorityEvidenceMonotone minorityMember⟩


theorem intake_grants_no_selection_or_execution_authority
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid certificate) :
    certificate.selectionAuthorityGrantedToPlanOS = false ∧
      certificate.executionAuthorityGranted = false ∧
      certificate.executionPermission = false := by
  exact ⟨valid.selection_authority_not_granted,
    valid.execution_authority_not_granted,
    valid.execution_permission_false⟩


theorem intake_is_not_plan_synthesis_or_world_mutation
    (certificate : MiddleWayBoundedSynthesisIntakeCertificate)
    (valid : MiddleWayBoundedSynthesisIntakeCertificateValid certificate) :
    certificate.planSynthesisPerformed = false ∧
      certificate.concretePlanIssued = false ∧
      certificate.persistentWorldStateChanged = false ∧
      certificate.activeNow = false := by
  exact ⟨valid.plan_synthesis_not_performed,
    valid.concrete_plan_not_issued,
    valid.persistent_world_state_unchanged,
    valid.active_now_false⟩

end KUOS.PlanOS.MiddleWayBoundedSynthesisIntakeV1_03
