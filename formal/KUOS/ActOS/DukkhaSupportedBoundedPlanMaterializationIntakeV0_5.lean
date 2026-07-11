import Mathlib
import KUOS.VerifyOS.DukkhaReductionClaimVerificationV0_6

namespace KUOS.ActOS.DukkhaSupportedBoundedPlanMaterializationIntakeV0_5

open KUOS.VerifyOS.DukkhaReductionClaimVerificationV0_6

inductive MaterializationCandidateState where
  | preparedNotActivated
  deriving DecidableEq, Repr

structure BoundedPlanMaterializationCandidate where
  candidateId : String
  sourceStepId : String
  sequenceIndex : Nat
  sourceActionClass : String
  materializationClass : String
  sourceActionSpecDigest : String
  materializationPayloadDigest : String
  candidateDigest : String
  reversible : Bool
  irreversible : Bool
  checkpointStepId : String
  stopConditionDigests : Finset String
  evidenceLineageDigests : Finset String
  state : MaterializationCandidateState
  adapterBindingDigest : String
  toolInvocationRequested : Bool
  externalSideEffectRequested : Bool
  executionPermissionRequested : Bool
  activeNowRequested : Bool

structure DukkhaSupportedBoundedPlanMaterializationIntakeReceipt where
  sourceCertificate : DukkhaReductionClaimVerificationCertificate
  sourcePlanReceiptDigest : String
  sourceConcretePlanDigest : String
  sourceWorldBindingDigest : String
  sourceWorldStateDigest : String
  sourceWorldRevision : Nat
  sourceWorldLineageDigest : String
  selectedCandidateId : String
  selectedCandidatePlanIntentDigest : String
  dukkhaAssessmentDigest : String
  referencePlanDigest : String
  materializationCandidates : List BoundedPlanMaterializationCandidate
  materializationCandidateCount : Nat
  materializationIntakePerformed : Bool
  materializationCandidatesIssued : Bool
  allPlanStepsMaterialized : Bool
  oneToOneStepMappingPreserved : Bool
  stepSequencePreserved : Bool
  checkpointGuardsPreserved : Bool
  stopConditionsPreserved : Bool
  evidenceLineagePreserved : Bool
  alternativeCandidatesPreserved : Bool
  dissentPreserved : Bool
  minorityPreserved : Bool
  dukkhaReductionSupportPreserved : Bool
  protectedGroupNonexternalizationPreserved : Bool
  futureNonexternalizationPreserved : Bool
  revisionCapacityPreserved : Bool
  persistentLoopReductionPreserved : Bool
  sourceLineage : Finset String
  resultingLineage : Finset String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  selectionRemainsDecisionOSOwned : Bool
  selectionAuthorityGrantedToActOS : Bool
  planRevisionAuthorityGrantedToActOS : Bool
  dukkhaMinimizationAuthorityGrantedToActOS : Bool
  planActivated : Bool
  adapterBindingPerformed : Bool
  adapterInvocationPerformed : Bool
  toolInvocationPerformed : Bool
  externalSideEffectPerformed : Bool
  executionAuthorityGranted : Bool
  executionPermission : Bool
  persistentWorldStateChanged : Bool
  activeNow : Bool
  sourceClaimSupported :
    sourceCertificate.claimStatus = .supported
  candidateCountMatches :
    materializationCandidateCount = materializationCandidates.length
  candidatesNonempty : materializationCandidates ≠ []
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility

structure DukkhaSupportedBoundedPlanMaterializationIntakeReceiptValid
    (receipt : DukkhaSupportedBoundedPlanMaterializationIntakeReceipt) : Prop where
  source_valid :
    DukkhaReductionClaimVerificationCertificateValid receipt.sourceCertificate
  materialization_intake_performed :
    receipt.materializationIntakePerformed = true
  materialization_candidates_issued :
    receipt.materializationCandidatesIssued = true
  all_plan_steps_materialized :
    receipt.allPlanStepsMaterialized = true
  one_to_one_step_mapping_preserved :
    receipt.oneToOneStepMappingPreserved = true
  step_sequence_preserved : receipt.stepSequencePreserved = true
  checkpoint_guards_preserved : receipt.checkpointGuardsPreserved = true
  stop_conditions_preserved : receipt.stopConditionsPreserved = true
  evidence_lineage_preserved : receipt.evidenceLineagePreserved = true
  alternative_candidates_preserved :
    receipt.alternativeCandidatesPreserved = true
  dissent_preserved : receipt.dissentPreserved = true
  minority_preserved : receipt.minorityPreserved = true
  dukkha_reduction_support_preserved :
    receipt.dukkhaReductionSupportPreserved = true
  protected_group_nonexternalization_preserved :
    receipt.protectedGroupNonexternalizationPreserved = true
  future_nonexternalization_preserved :
    receipt.futureNonexternalizationPreserved = true
  revision_capacity_preserved : receipt.revisionCapacityPreserved = true
  persistent_loop_reduction_preserved :
    receipt.persistentLoopReductionPreserved = true
  selection_remains_decisionos_owned :
    receipt.selectionRemainsDecisionOSOwned = true
  selection_authority_not_granted :
    receipt.selectionAuthorityGrantedToActOS = false
  plan_revision_authority_not_granted :
    receipt.planRevisionAuthorityGrantedToActOS = false
  dukkha_minimization_authority_not_granted :
    receipt.dukkhaMinimizationAuthorityGrantedToActOS = false
  plan_not_activated : receipt.planActivated = false
  adapter_binding_not_performed : receipt.adapterBindingPerformed = false
  adapter_invocation_not_performed : receipt.adapterInvocationPerformed = false
  tool_invocation_not_performed : receipt.toolInvocationPerformed = false
  external_side_effect_not_performed :
    receipt.externalSideEffectPerformed = false
  execution_authority_not_granted :
    receipt.executionAuthorityGranted = false
  execution_permission_false : receipt.executionPermission = false
  persistent_world_state_unchanged :
    receipt.persistentWorldStateChanged = false
  active_now_false : receipt.activeNow = false

theorem supported_claim_is_required_for_materialization_intake
    (receipt : DukkhaSupportedBoundedPlanMaterializationIntakeReceipt)
    (valid : DukkhaSupportedBoundedPlanMaterializationIntakeReceiptValid receipt) :
    receipt.sourceCertificate.claimStatus = .supported ∧
      receipt.materializationIntakePerformed = true ∧
      receipt.materializationCandidatesIssued = true := by
  exact ⟨receipt.sourceClaimSupported,
    valid.materialization_intake_performed,
    valid.materialization_candidates_issued⟩

theorem materialization_intake_preserves_step_bijection_and_sequence
    (receipt : DukkhaSupportedBoundedPlanMaterializationIntakeReceipt)
    (valid : DukkhaSupportedBoundedPlanMaterializationIntakeReceiptValid receipt) :
    receipt.allPlanStepsMaterialized = true ∧
      receipt.oneToOneStepMappingPreserved = true ∧
      receipt.stepSequencePreserved = true := by
  exact ⟨valid.all_plan_steps_materialized,
    valid.one_to_one_step_mapping_preserved,
    valid.step_sequence_preserved⟩

theorem materialization_intake_preserves_checkpoint_stop_and_evidence
    (receipt : DukkhaSupportedBoundedPlanMaterializationIntakeReceipt)
    (valid : DukkhaSupportedBoundedPlanMaterializationIntakeReceiptValid receipt) :
    receipt.checkpointGuardsPreserved = true ∧
      receipt.stopConditionsPreserved = true ∧
      receipt.evidenceLineagePreserved = true := by
  exact ⟨valid.checkpoint_guards_preserved,
    valid.stop_conditions_preserved,
    valid.evidence_lineage_preserved⟩

theorem materialization_intake_preserves_alternatives_dissent_and_minority
    (receipt : DukkhaSupportedBoundedPlanMaterializationIntakeReceipt)
    (valid : DukkhaSupportedBoundedPlanMaterializationIntakeReceiptValid receipt) :
    receipt.alternativeCandidatesPreserved = true ∧
      receipt.dissentPreserved = true ∧
      receipt.minorityPreserved = true := by
  exact ⟨valid.alternative_candidates_preserved,
    valid.dissent_preserved,
    valid.minority_preserved⟩

theorem materialization_intake_preserves_dukkha_nonexternalization
    (receipt : DukkhaSupportedBoundedPlanMaterializationIntakeReceipt)
    (valid : DukkhaSupportedBoundedPlanMaterializationIntakeReceiptValid receipt) :
    receipt.dukkhaReductionSupportPreserved = true ∧
      receipt.protectedGroupNonexternalizationPreserved = true ∧
      receipt.futureNonexternalizationPreserved = true ∧
      receipt.revisionCapacityPreserved = true ∧
      receipt.persistentLoopReductionPreserved = true := by
  exact ⟨valid.dukkha_reduction_support_preserved,
    valid.protected_group_nonexternalization_preserved,
    valid.future_nonexternalization_preserved,
    valid.revision_capacity_preserved,
    valid.persistent_loop_reduction_preserved⟩

theorem materialization_intake_preserves_lineage_and_responsibility
    (receipt : DukkhaSupportedBoundedPlanMaterializationIntakeReceipt) :
    receipt.sourceLineage ⊆ receipt.resultingLineage ∧
      receipt.sourceResponsibility ⊆ receipt.resultingResponsibility := by
  exact ⟨receipt.lineageMonotone, receipt.responsibilityMonotone⟩

theorem materialization_intake_grants_no_selection_revision_or_minimization_authority
    (receipt : DukkhaSupportedBoundedPlanMaterializationIntakeReceipt)
    (valid : DukkhaSupportedBoundedPlanMaterializationIntakeReceiptValid receipt) :
    receipt.selectionRemainsDecisionOSOwned = true ∧
      receipt.selectionAuthorityGrantedToActOS = false ∧
      receipt.planRevisionAuthorityGrantedToActOS = false ∧
      receipt.dukkhaMinimizationAuthorityGrantedToActOS = false := by
  exact ⟨valid.selection_remains_decisionos_owned,
    valid.selection_authority_not_granted,
    valid.plan_revision_authority_not_granted,
    valid.dukkha_minimization_authority_not_granted⟩

theorem materialization_intake_is_not_activation_adapter_invocation_or_execution
    (receipt : DukkhaSupportedBoundedPlanMaterializationIntakeReceipt)
    (valid : DukkhaSupportedBoundedPlanMaterializationIntakeReceiptValid receipt) :
    receipt.planActivated = false ∧
      receipt.adapterBindingPerformed = false ∧
      receipt.adapterInvocationPerformed = false ∧
      receipt.toolInvocationPerformed = false ∧
      receipt.externalSideEffectPerformed = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.executionPermission = false ∧
      receipt.persistentWorldStateChanged = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.plan_not_activated,
    valid.adapter_binding_not_performed,
    valid.adapter_invocation_not_performed,
    valid.tool_invocation_not_performed,
    valid.external_side_effect_not_performed,
    valid.execution_authority_not_granted,
    valid.execution_permission_false,
    valid.persistent_world_state_unchanged,
    valid.active_now_false⟩

end KUOS.ActOS.DukkhaSupportedBoundedPlanMaterializationIntakeV0_5
