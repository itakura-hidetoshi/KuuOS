import Mathlib
import KUOS.ActOS.DukkhaPreservingAdapterBindingAuthorizationIntakeV0_6

namespace KUOS.ActOS.DukkhaPreservingFrontierPlanActivationReceiptV0_7

open KUOS.ActOS.DukkhaPreservingAdapterBindingAuthorizationIntakeV0_6

inductive FrontierActivationState where
  | boundNotInvoked
  | activatedNotInvoked
  deriving DecidableEq, Repr

structure DukkhaPreservingFrontierPlanActivationReceipt where
  sourceReceipt : DukkhaPreservingAdapterBindingAuthorizationIntakeReceipt
  sourceAuthorizationReceiptDigest : String
  activationAuthorizationTokenDigest : String
  activationContextDigest : String
  activatedFrontierCandidateId : String
  activatedFrontierAdapterId : String
  activatedFrontierBindingDigest : String
  activatedFrontierLeaseId : String
  activationStateBefore : FrontierActivationState
  activationStateAfter : FrontierActivationState
  activationAuthorizationConsumed : Bool
  activationAuthorizationTokenMarkedConsumed : Bool
  singleUseAuthorizationReplayClosed : Bool
  planActivationPerformed : Bool
  frontierCandidateActivated : Bool
  exactlyOneFrontierActivated : Bool
  activationFrontierSequencePreserved : Bool
  completedPrefixPreserved : Bool
  laterCandidatesRemainInactive : Bool
  adapterBindingPreserved : Bool
  adapterInvocationIntakeAdmitted : Bool
  adapterLeaseUseConsumed : Bool
  adapterRegistrySnapshotUnchanged : Bool
  worldConditionsCurrent : Bool
  authorizationDelayCurrent : Bool
  tokenReplayFreshBeforeConsumption : Bool
  frontierReplayFreshBeforeActivation : Bool
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
  singleScalarUtilityNotIntroduced : Bool
  sourceLineage : Finset String
  resultingLineage : Finset String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  selectionRemainsDecisionOSOwned : Bool
  selectionAuthorityGrantedToActOS : Bool
  planRevisionAuthorityGrantedToActOS : Bool
  dukkhaMinimizationAuthorityGrantedToActOS : Bool
  adapterInvocationPerformed : Bool
  toolInvocationPerformed : Bool
  externalSideEffectPerformed : Bool
  executionAuthorityGranted : Bool
  executionPermission : Bool
  persistentWorldStateChanged : Bool
  activeNow : Bool
  sourceAuthorizationReady :
    sourceReceipt.authorizationDisposition =
      .activationAuthorizationReady
  activationTransitionExact :
    activationStateBefore = .boundNotInvoked ∧
      activationStateAfter = .activatedNotInvoked
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility

structure DukkhaPreservingFrontierPlanActivationReceiptValid
    (receipt : DukkhaPreservingFrontierPlanActivationReceipt) : Prop where
  source_valid :
    DukkhaPreservingAdapterBindingAuthorizationIntakeReceiptValid
      receipt.sourceReceipt
  source_authorization_ready :
    receipt.sourceReceipt.authorizationDisposition =
      .activationAuthorizationReady
  authorization_consumed :
    receipt.activationAuthorizationConsumed = true
  authorization_token_marked_consumed :
    receipt.activationAuthorizationTokenMarkedConsumed = true
  single_use_replay_closed :
    receipt.singleUseAuthorizationReplayClosed = true
  plan_activation_performed : receipt.planActivationPerformed = true
  frontier_candidate_activated : receipt.frontierCandidateActivated = true
  exactly_one_frontier_activated :
    receipt.exactlyOneFrontierActivated = true
  frontier_sequence_preserved :
    receipt.activationFrontierSequencePreserved = true
  completed_prefix_preserved : receipt.completedPrefixPreserved = true
  later_candidates_inactive : receipt.laterCandidatesRemainInactive = true
  adapter_binding_preserved : receipt.adapterBindingPreserved = true
  invocation_intake_admitted : receipt.adapterInvocationIntakeAdmitted = true
  adapter_lease_not_consumed : receipt.adapterLeaseUseConsumed = false
  registry_snapshot_unchanged :
    receipt.adapterRegistrySnapshotUnchanged = true
  world_conditions_current : receipt.worldConditionsCurrent = true
  authorization_delay_current : receipt.authorizationDelayCurrent = true
  token_fresh_before_consumption :
    receipt.tokenReplayFreshBeforeConsumption = true
  frontier_fresh_before_activation :
    receipt.frontierReplayFreshBeforeActivation = true
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
  single_scalar_utility_not_introduced :
    receipt.singleScalarUtilityNotIntroduced = true
  selection_remains_decisionos_owned :
    receipt.selectionRemainsDecisionOSOwned = true
  selection_authority_not_granted :
    receipt.selectionAuthorityGrantedToActOS = false
  plan_revision_authority_not_granted :
    receipt.planRevisionAuthorityGrantedToActOS = false
  dukkha_minimization_authority_not_granted :
    receipt.dukkhaMinimizationAuthorityGrantedToActOS = false
  adapter_not_invoked : receipt.adapterInvocationPerformed = false
  tool_not_invoked : receipt.toolInvocationPerformed = false
  external_side_effect_not_performed :
    receipt.externalSideEffectPerformed = false
  execution_authority_not_granted :
    receipt.executionAuthorityGranted = false
  execution_permission_false : receipt.executionPermission = false
  persistent_world_state_unchanged :
    receipt.persistentWorldStateChanged = false
  active_now_false : receipt.activeNow = false

theorem ready_authorization_is_required_for_frontier_activation
    (receipt : DukkhaPreservingFrontierPlanActivationReceipt)
    (valid : DukkhaPreservingFrontierPlanActivationReceiptValid receipt) :
    receipt.sourceReceipt.authorizationDisposition =
        .activationAuthorizationReady ∧
      receipt.planActivationPerformed = true := by
  exact ⟨valid.source_authorization_ready,
    valid.plan_activation_performed⟩

theorem frontier_activation_consumes_single_use_authorization
    (receipt : DukkhaPreservingFrontierPlanActivationReceipt)
    (valid : DukkhaPreservingFrontierPlanActivationReceiptValid receipt) :
    receipt.activationAuthorizationConsumed = true ∧
      receipt.activationAuthorizationTokenMarkedConsumed = true ∧
      receipt.singleUseAuthorizationReplayClosed = true := by
  exact ⟨valid.authorization_consumed,
    valid.authorization_token_marked_consumed,
    valid.single_use_replay_closed⟩

theorem frontier_activation_has_exact_noninvoked_transition
    (receipt : DukkhaPreservingFrontierPlanActivationReceipt) :
    receipt.activationStateBefore = .boundNotInvoked ∧
      receipt.activationStateAfter = .activatedNotInvoked := by
  exact receipt.activationTransitionExact

theorem frontier_activation_preserves_sequence_and_later_inactivity
    (receipt : DukkhaPreservingFrontierPlanActivationReceipt)
    (valid : DukkhaPreservingFrontierPlanActivationReceiptValid receipt) :
    receipt.frontierCandidateActivated = true ∧
      receipt.exactlyOneFrontierActivated = true ∧
      receipt.activationFrontierSequencePreserved = true ∧
      receipt.completedPrefixPreserved = true ∧
      receipt.laterCandidatesRemainInactive = true := by
  exact ⟨valid.frontier_candidate_activated,
    valid.exactly_one_frontier_activated,
    valid.frontier_sequence_preserved,
    valid.completed_prefix_preserved,
    valid.later_candidates_inactive⟩

theorem frontier_activation_preserves_dukkha_and_nonexternalization
    (receipt : DukkhaPreservingFrontierPlanActivationReceipt)
    (valid : DukkhaPreservingFrontierPlanActivationReceiptValid receipt) :
    receipt.dukkhaReductionSupportPreserved = true ∧
      receipt.protectedGroupNonexternalizationPreserved = true ∧
      receipt.futureNonexternalizationPreserved = true ∧
      receipt.revisionCapacityPreserved = true ∧
      receipt.persistentLoopReductionPreserved = true ∧
      receipt.singleScalarUtilityNotIntroduced = true := by
  exact ⟨valid.dukkha_reduction_support_preserved,
    valid.protected_group_nonexternalization_preserved,
    valid.future_nonexternalization_preserved,
    valid.revision_capacity_preserved,
    valid.persistent_loop_reduction_preserved,
    valid.single_scalar_utility_not_introduced⟩

theorem frontier_activation_preserves_alternatives_dissent_and_minority
    (receipt : DukkhaPreservingFrontierPlanActivationReceipt)
    (valid : DukkhaPreservingFrontierPlanActivationReceiptValid receipt) :
    receipt.alternativeCandidatesPreserved = true ∧
      receipt.dissentPreserved = true ∧
      receipt.minorityPreserved = true := by
  exact ⟨valid.alternative_candidates_preserved,
    valid.dissent_preserved,
    valid.minority_preserved⟩

theorem frontier_activation_preserves_lineage_and_responsibility
    (receipt : DukkhaPreservingFrontierPlanActivationReceipt) :
    receipt.sourceLineage ⊆ receipt.resultingLineage ∧
      receipt.sourceResponsibility ⊆ receipt.resultingResponsibility := by
  exact ⟨receipt.lineageMonotone, receipt.responsibilityMonotone⟩

theorem frontier_activation_grants_no_selection_revision_or_minimization_authority
    (receipt : DukkhaPreservingFrontierPlanActivationReceipt)
    (valid : DukkhaPreservingFrontierPlanActivationReceiptValid receipt) :
    receipt.selectionRemainsDecisionOSOwned = true ∧
      receipt.selectionAuthorityGrantedToActOS = false ∧
      receipt.planRevisionAuthorityGrantedToActOS = false ∧
      receipt.dukkhaMinimizationAuthorityGrantedToActOS = false := by
  exact ⟨valid.selection_remains_decisionos_owned,
    valid.selection_authority_not_granted,
    valid.plan_revision_authority_not_granted,
    valid.dukkha_minimization_authority_not_granted⟩

theorem activation_does_not_consume_adapter_lease
    (receipt : DukkhaPreservingFrontierPlanActivationReceipt)
    (valid : DukkhaPreservingFrontierPlanActivationReceiptValid receipt) :
    receipt.adapterBindingPreserved = true ∧
      receipt.adapterInvocationIntakeAdmitted = true ∧
      receipt.adapterLeaseUseConsumed = false ∧
      receipt.adapterRegistrySnapshotUnchanged = true := by
  exact ⟨valid.adapter_binding_preserved,
    valid.invocation_intake_admitted,
    valid.adapter_lease_not_consumed,
    valid.registry_snapshot_unchanged⟩

theorem plan_activation_is_not_adapter_invocation_or_execution
    (receipt : DukkhaPreservingFrontierPlanActivationReceipt)
    (valid : DukkhaPreservingFrontierPlanActivationReceiptValid receipt) :
    receipt.adapterInvocationPerformed = false ∧
      receipt.toolInvocationPerformed = false ∧
      receipt.externalSideEffectPerformed = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.executionPermission = false ∧
      receipt.persistentWorldStateChanged = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.adapter_not_invoked,
    valid.tool_not_invoked,
    valid.external_side_effect_not_performed,
    valid.execution_authority_not_granted,
    valid.execution_permission_false,
    valid.persistent_world_state_unchanged,
    valid.active_now_false⟩

end KUOS.ActOS.DukkhaPreservingFrontierPlanActivationReceiptV0_7
