import Mathlib
import KUOS.PlanOS.BoundedSynthesisReceiptV1_04

namespace KUOS.VerifyOS.BoundedPlanMiddleWayVerificationV0_5

open KUOS.PlanOS.BoundedSynthesisReceiptV1_04

inductive PlanConditionalValidityStatus where
  | valid
  | revisionRequired
  deriving DecidableEq, Repr

inductive PlanVerificationDisposition where
  | boundedPlanVerifiedForMaterializationIntake
  | returnToPlanOSRevision
  deriving DecidableEq, Repr


def dispositionForWorldCurrency (worldConditionsCurrent : Bool) :
    PlanVerificationDisposition :=
  if worldConditionsCurrent then
    .boundedPlanVerifiedForMaterializationIntake
  else
    .returnToPlanOSRevision


def statusForWorldCurrency (worldConditionsCurrent : Bool) :
    PlanConditionalValidityStatus :=
  if worldConditionsCurrent then .valid else .revisionRequired


def admittedForWorldCurrency (worldConditionsCurrent : Bool) : Bool :=
  worldConditionsCurrent


structure BoundedPlanMiddleWayVerificationCertificate where
  sourcePlanReceiptDigest : String
  sourcePlanDigest : String
  sourceConstraintDigest : String
  sourceWorldBindingDigest : String
  sourceWorldStateDigest : String
  sourceWorldRevision : Nat
  sourceWorldLineageDigest : String
  currentWorldBindingDigest : String
  currentWorldStateDigest : String
  currentWorldRevision : Nat
  currentWorldLineageDigest : String
  worldConditionsCurrent : Bool
  conditionalValidityStatus : PlanConditionalValidityStatus
  verificationDisposition : PlanVerificationDisposition
  materializationIntakeAdmitted : Bool
  finitePlanVerified : Bool
  stepSequenceVerified : Bool
  stepBoundVerified : Bool
  branchBoundVerified : Bool
  revisionBoundVerified : Bool
  checkpointOrderVerified : Bool
  stopConditionsVerified : Bool
  forbiddenEffectsAbsent : Bool
  selectedCandidatePreserved : Bool
  planIntentPreserved : Bool
  worldDependencyExplicit : Bool
  alternativeCandidatesPreserved : Bool
  dissentEvidencePreserved : Bool
  minorityEvidencePreserved : Bool
  sourceLineage : Finset String
  resultingLineage : Finset String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  planRemainsConditionallyBinding : Bool
  planNotReified : Bool
  planNotErased : Bool
  conditionChangeRoutesToRevision : Bool
  selectionRemainsDecisionOSOwned : Bool
  selectionAuthorityGrantedToVerifyOS : Bool
  planRevisionAuthorityGrantedToVerifyOS : Bool
  planActivated : Bool
  materializationPerformed : Bool
  executionAuthorityGranted : Bool
  executionPermission : Bool
  persistentWorldStateChanged : Bool
  activeNow : Bool
  statusMatches :
    conditionalValidityStatus = statusForWorldCurrency worldConditionsCurrent
  dispositionMatches :
    verificationDisposition = dispositionForWorldCurrency worldConditionsCurrent
  admissionMatches :
    materializationIntakeAdmitted = admittedForWorldCurrency worldConditionsCurrent
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility


structure BoundedPlanMiddleWayVerificationCertificateValid
    (certificate : BoundedPlanMiddleWayVerificationCertificate) : Prop where
  finite_plan_verified : certificate.finitePlanVerified = true
  step_sequence_verified : certificate.stepSequenceVerified = true
  step_bound_verified : certificate.stepBoundVerified = true
  branch_bound_verified : certificate.branchBoundVerified = true
  revision_bound_verified : certificate.revisionBoundVerified = true
  checkpoint_order_verified : certificate.checkpointOrderVerified = true
  stop_conditions_verified : certificate.stopConditionsVerified = true
  forbidden_effects_absent : certificate.forbiddenEffectsAbsent = true
  selected_candidate_preserved : certificate.selectedCandidatePreserved = true
  plan_intent_preserved : certificate.planIntentPreserved = true
  world_dependency_explicit : certificate.worldDependencyExplicit = true
  alternative_candidates_preserved :
    certificate.alternativeCandidatesPreserved = true
  dissent_evidence_preserved : certificate.dissentEvidencePreserved = true
  minority_evidence_preserved : certificate.minorityEvidencePreserved = true
  plan_remains_conditionally_binding :
    certificate.planRemainsConditionallyBinding = true
  plan_not_reified : certificate.planNotReified = true
  plan_not_erased : certificate.planNotErased = true
  condition_change_routes_to_revision :
    certificate.conditionChangeRoutesToRevision = true
  selection_remains_decisionos_owned :
    certificate.selectionRemainsDecisionOSOwned = true
  selection_authority_not_granted :
    certificate.selectionAuthorityGrantedToVerifyOS = false
  plan_revision_authority_not_granted :
    certificate.planRevisionAuthorityGrantedToVerifyOS = false
  plan_not_activated : certificate.planActivated = false
  materialization_not_performed : certificate.materializationPerformed = false
  execution_authority_not_granted :
    certificate.executionAuthorityGranted = false
  execution_permission_false : certificate.executionPermission = false
  persistent_world_state_unchanged :
    certificate.persistentWorldStateChanged = false
  active_now_false : certificate.activeNow = false


theorem current_world_conditions_admit_materialization_intake
    (certificate : BoundedPlanMiddleWayVerificationCertificate)
    (current : certificate.worldConditionsCurrent = true) :
    certificate.conditionalValidityStatus = .valid ∧
      certificate.verificationDisposition =
        .boundedPlanVerifiedForMaterializationIntake ∧
      certificate.materializationIntakeAdmitted = true := by
  constructor
  · calc
      certificate.conditionalValidityStatus =
          statusForWorldCurrency certificate.worldConditionsCurrent :=
        certificate.statusMatches
      _ = .valid := by simp [statusForWorldCurrency, current]
  constructor
  · calc
      certificate.verificationDisposition =
          dispositionForWorldCurrency certificate.worldConditionsCurrent :=
        certificate.dispositionMatches
      _ = .boundedPlanVerifiedForMaterializationIntake := by
        simp [dispositionForWorldCurrency, current]
  · calc
      certificate.materializationIntakeAdmitted =
          admittedForWorldCurrency certificate.worldConditionsCurrent :=
        certificate.admissionMatches
      _ = true := by simp [admittedForWorldCurrency, current]


theorem changed_world_conditions_require_plan_revision
    (certificate : BoundedPlanMiddleWayVerificationCertificate)
    (changed : certificate.worldConditionsCurrent = false) :
    certificate.conditionalValidityStatus = .revisionRequired ∧
      certificate.verificationDisposition = .returnToPlanOSRevision ∧
      certificate.materializationIntakeAdmitted = false := by
  constructor
  · calc
      certificate.conditionalValidityStatus =
          statusForWorldCurrency certificate.worldConditionsCurrent :=
        certificate.statusMatches
      _ = .revisionRequired := by simp [statusForWorldCurrency, changed]
  constructor
  · calc
      certificate.verificationDisposition =
          dispositionForWorldCurrency certificate.worldConditionsCurrent :=
        certificate.dispositionMatches
      _ = .returnToPlanOSRevision := by
        simp [dispositionForWorldCurrency, changed]
  · calc
      certificate.materializationIntakeAdmitted =
          admittedForWorldCurrency certificate.worldConditionsCurrent :=
        certificate.admissionMatches
      _ = false := by simp [admittedForWorldCurrency, changed]


theorem bounded_plan_structure_is_reverified
    (certificate : BoundedPlanMiddleWayVerificationCertificate)
    (valid : BoundedPlanMiddleWayVerificationCertificateValid certificate) :
    certificate.finitePlanVerified = true ∧
      certificate.stepSequenceVerified = true ∧
      certificate.stepBoundVerified = true ∧
      certificate.branchBoundVerified = true ∧
      certificate.revisionBoundVerified = true := by
  exact ⟨valid.finite_plan_verified,
    valid.step_sequence_verified,
    valid.step_bound_verified,
    valid.branch_bound_verified,
    valid.revision_bound_verified⟩


theorem checkpoint_stop_and_effect_boundaries_are_reverified
    (certificate : BoundedPlanMiddleWayVerificationCertificate)
    (valid : BoundedPlanMiddleWayVerificationCertificateValid certificate) :
    certificate.checkpointOrderVerified = true ∧
      certificate.stopConditionsVerified = true ∧
      certificate.forbiddenEffectsAbsent = true := by
  exact ⟨valid.checkpoint_order_verified,
    valid.stop_conditions_verified,
    valid.forbidden_effects_absent⟩


theorem verification_preserves_selection_plan_intent_and_world_dependency
    (certificate : BoundedPlanMiddleWayVerificationCertificate)
    (valid : BoundedPlanMiddleWayVerificationCertificateValid certificate) :
    certificate.selectedCandidatePreserved = true ∧
      certificate.planIntentPreserved = true ∧
      certificate.worldDependencyExplicit = true := by
  exact ⟨valid.selected_candidate_preserved,
    valid.plan_intent_preserved,
    valid.world_dependency_explicit⟩


theorem verification_preserves_alternatives_dissent_and_minority
    (certificate : BoundedPlanMiddleWayVerificationCertificate)
    (valid : BoundedPlanMiddleWayVerificationCertificateValid certificate) :
    certificate.alternativeCandidatesPreserved = true ∧
      certificate.dissentEvidencePreserved = true ∧
      certificate.minorityEvidencePreserved = true := by
  exact ⟨valid.alternative_candidates_preserved,
    valid.dissent_evidence_preserved,
    valid.minority_evidence_preserved⟩


theorem verification_preserves_lineage_and_responsibility
    (certificate : BoundedPlanMiddleWayVerificationCertificate) :
    certificate.sourceLineage ⊆ certificate.resultingLineage ∧
      certificate.sourceResponsibility ⊆ certificate.resultingResponsibility := by
  exact ⟨certificate.lineageMonotone, certificate.responsibilityMonotone⟩


theorem verified_plan_remains_middle_way_conditioned
    (certificate : BoundedPlanMiddleWayVerificationCertificate)
    (valid : BoundedPlanMiddleWayVerificationCertificateValid certificate) :
    certificate.planRemainsConditionallyBinding = true ∧
      certificate.planNotReified = true ∧
      certificate.planNotErased = true ∧
      certificate.conditionChangeRoutesToRevision = true := by
  exact ⟨valid.plan_remains_conditionally_binding,
    valid.plan_not_reified,
    valid.plan_not_erased,
    valid.condition_change_routes_to_revision⟩


theorem verification_grants_no_selection_or_revision_authority
    (certificate : BoundedPlanMiddleWayVerificationCertificate)
    (valid : BoundedPlanMiddleWayVerificationCertificateValid certificate) :
    certificate.selectionRemainsDecisionOSOwned = true ∧
      certificate.selectionAuthorityGrantedToVerifyOS = false ∧
      certificate.planRevisionAuthorityGrantedToVerifyOS = false := by
  exact ⟨valid.selection_remains_decisionos_owned,
    valid.selection_authority_not_granted,
    valid.plan_revision_authority_not_granted⟩


theorem verification_is_not_activation_materialization_or_execution
    (certificate : BoundedPlanMiddleWayVerificationCertificate)
    (valid : BoundedPlanMiddleWayVerificationCertificateValid certificate) :
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

end KUOS.VerifyOS.BoundedPlanMiddleWayVerificationV0_5
