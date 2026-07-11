import Mathlib
import KUOS.VerifyOS.VacuumExpectationCommitVerificationReceiptV0_3

namespace KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4

inductive TransitionKind where
  | retain
  | suspend
  | requestRevision
  | supersedeWithLineage
  | complete
  | terminate
  deriving DecidableEq, Repr

inductive ConditionalValidityStatus where
  | valid
  | suspended
  | revisionRequired
  | superseded
  | completed
  | terminated
  deriving DecidableEq, Repr

def statusForTransition : TransitionKind → ConditionalValidityStatus
  | .retain => .valid
  | .suspend => .suspended
  | .requestRevision => .revisionRequired
  | .supersedeWithLineage => .superseded
  | .complete => .completed
  | .terminate => .terminated

structure MiddleWayContinuityCertificate where
  transitionKind : TransitionKind
  conditionalValidityStatus : ConditionalValidityStatus
  sourceLineage : Finset String
  resultingLineage : Finset String
  predecessorReference : String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  sourceDissent : Finset String
  resultingDissent : Finset String
  sourceMinorityEvidence : Finset String
  resultingMinorityEvidence : Finset String
  transitionStatusMatches : conditionalValidityStatus = statusForTransition transitionKind
  predecessorPreserved : predecessorReference ∈ resultingLineage
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityPreserved : sourceResponsibility ⊆ resultingResponsibility
  dissentPreserved : sourceDissent ⊆ resultingDissent
  minorityEvidencePreserved : sourceMinorityEvidence ⊆ resultingMinorityEvidence
  objectNotReified : Prop
  objectNotErased : Prop
  commitmentNotAbsolutized : Prop
  terminationDoesNotEraseHistory : Prop
  authorityUnchanged : Prop
  executionPermissionNotGranted : Prop
  persistentWorldStateUnchanged : Prop
  selectionRemainsDecisionOSOwned : Prop
  planSynthesisPerformed : Bool
  concretePlanIssued : Bool
  activeNow : Bool
  executionPermission : Bool

structure MiddleWayContinuityCertificateValid
    (certificate : MiddleWayContinuityCertificate) : Prop where
  object_not_reified : certificate.objectNotReified
  object_not_erased : certificate.objectNotErased
  commitment_not_absolutized : certificate.commitmentNotAbsolutized
  termination_preserves_history : certificate.terminationDoesNotEraseHistory
  authority_unchanged : certificate.authorityUnchanged
  execution_permission_not_granted : certificate.executionPermissionNotGranted
  persistent_world_state_unchanged : certificate.persistentWorldStateUnchanged
  selection_remains_decisionos_owned : certificate.selectionRemainsDecisionOSOwned
  plan_synthesis_not_performed : certificate.planSynthesisPerformed = false
  concrete_plan_not_issued : certificate.concretePlanIssued = false
  active_now_false : certificate.activeNow = false
  execution_permission_false : certificate.executionPermission = false

theorem transition_status_is_conditioned
    (certificate : MiddleWayContinuityCertificate) :
    certificate.conditionalValidityStatus =
      statusForTransition certificate.transitionKind := by
  exact certificate.transitionStatusMatches

theorem lineage_monotone_preserves_source
    (certificate : MiddleWayContinuityCertificate)
    (digest : String)
    (sourceMember : digest ∈ certificate.sourceLineage) :
    digest ∈ certificate.resultingLineage := by
  exact certificate.lineageMonotone sourceMember

theorem predecessor_is_not_erased
    (certificate : MiddleWayContinuityCertificate) :
    certificate.predecessorReference ∈ certificate.resultingLineage := by
  exact certificate.predecessorPreserved

theorem revision_preserves_responsibility
    (certificate : MiddleWayContinuityCertificate)
    (digest : String)
    (sourceMember : digest ∈ certificate.sourceResponsibility) :
    digest ∈ certificate.resultingResponsibility := by
  exact certificate.responsibilityPreserved sourceMember

theorem dissent_is_not_erased
    (certificate : MiddleWayContinuityCertificate)
    (digest : String)
    (sourceMember : digest ∈ certificate.sourceDissent) :
    digest ∈ certificate.resultingDissent := by
  exact certificate.dissentPreserved sourceMember

theorem minority_evidence_is_not_erased
    (certificate : MiddleWayContinuityCertificate)
    (digest : String)
    (sourceMember : digest ∈ certificate.sourceMinorityEvidence) :
    digest ∈ certificate.resultingMinorityEvidence := by
  exact certificate.minorityEvidencePreserved sourceMember

theorem supersession_preserves_predecessor
    (certificate : MiddleWayContinuityCertificate)
    (kind : certificate.transitionKind = .supersedeWithLineage) :
    certificate.predecessorReference ∈ certificate.resultingLineage := by
  exact certificate.predecessorPreserved

theorem termination_does_not_deny_lineage
    (certificate : MiddleWayContinuityCertificate)
    (valid : MiddleWayContinuityCertificateValid certificate)
    (kind : certificate.transitionKind = .terminate) :
    certificate.terminationDoesNotEraseHistory := by
  exact valid.termination_preserves_history

theorem middle_way_rejects_reification_and_erasure
    (certificate : MiddleWayContinuityCertificate)
    (valid : MiddleWayContinuityCertificateValid certificate) :
    certificate.objectNotReified ∧ certificate.objectNotErased ∧
      certificate.commitmentNotAbsolutized := by
  exact ⟨valid.object_not_reified, valid.object_not_erased,
    valid.commitment_not_absolutized⟩

theorem middle_way_preserves_authority_boundary
    (certificate : MiddleWayContinuityCertificate)
    (valid : MiddleWayContinuityCertificateValid certificate) :
    certificate.authorityUnchanged ∧
      certificate.executionPermissionNotGranted ∧
      certificate.selectionRemainsDecisionOSOwned := by
  exact ⟨valid.authority_unchanged,
    valid.execution_permission_not_granted,
    valid.selection_remains_decisionos_owned⟩

theorem middle_way_verification_is_not_plan_or_execution
    (certificate : MiddleWayContinuityCertificate)
    (valid : MiddleWayContinuityCertificateValid certificate) :
    certificate.planSynthesisPerformed = false ∧
      certificate.concretePlanIssued = false ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨valid.plan_synthesis_not_performed,
    valid.concrete_plan_not_issued,
    valid.active_now_false,
    valid.execution_permission_false⟩

end KUOS.VerifyOS.MiddleWayConditionalContinuityVerificationV0_4
