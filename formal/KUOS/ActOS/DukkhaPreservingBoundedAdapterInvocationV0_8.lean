import Mathlib
import KUOS.ActOS.DukkhaPreservingFrontierPlanActivationReceiptV0_7

namespace KUOS.ActOS.DukkhaPreservingBoundedAdapterInvocationV0_8

open KUOS.ActOS.DukkhaPreservingFrontierPlanActivationReceiptV0_7

inductive BoundedAdapterInvocationState where
  | activatedNotInvoked
  | invokedEffectNotCommitted
  deriving DecidableEq, Repr

structure DukkhaPreservingBoundedAdapterInvocationReceipt where
  sourceReceipt : DukkhaPreservingFrontierPlanActivationReceipt
  sourceActivationReceiptDigest : String
  sourceAuthorizationReceiptDigest : String
  invocationContextDigest : String
  invokedFrontierCandidateId : String
  invokedFrontierAdapterId : String
  invokedFrontierBindingDigest : String
  invokedFrontierLeaseId : String
  leaseReservationDigest : String
  invocationStateBefore : BoundedAdapterInvocationState
  invocationStateAfter : BoundedAdapterInvocationState
  adapterInvocationPerformed : Bool
  adapterHostInvocationPerformed : Bool
  exactlyOneAdapterInvoked : Bool
  boundedScopePreserved : Bool
  effectCeilingPreserved : Bool
  activationFrontierSequencePreserved : Bool
  completedPrefixPreserved : Bool
  laterCandidatesRemainUninvoked : Bool
  adapterLeaseReservationConsumed : Bool
  adapterLeaseUseConsumed : Bool
  adapterLeaseDoubleDecremented : Bool
  leaseConsumptionRecordIssued : Bool
  invocationNonceConsumed : Bool
  invocationNonceReplayClosed : Bool
  frontierInvocationReplayClosed : Bool
  invocationResultEnvelopeIssued : Bool
  effectProposalRecorded : Bool
  effectCommitRequired : Bool
  effectCommitPerformed : Bool
  observationIntakeRequired : Bool
  verificationDebtOpen : Bool
  adapterRegistrySnapshotUnchanged : Bool
  worldConditionsCurrent : Bool
  invocationDelayCurrent : Bool
  leaseReservationReplayFreshBeforeConsumption : Bool
  invocationNonceReplayFreshBeforeConsumption : Bool
  frontierReplayFreshBeforeInvocation : Bool
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
  toolInvocationPerformed : Bool
  externalSideEffectPerformed : Bool
  executionAuthorityGranted : Bool
  executionPermission : Bool
  persistentWorldStateChanged : Bool
  activeNow : Bool
  sourceFrontierActivated :
    sourceReceipt.activationStateAfter = .activatedNotInvoked
  invocationTransitionExact :
    invocationStateBefore = .activatedNotInvoked ∧
      invocationStateAfter = .invokedEffectNotCommitted
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility

structure DukkhaPreservingBoundedAdapterInvocationReceiptValid
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt) : Prop where
  source_valid :
    DukkhaPreservingFrontierPlanActivationReceiptValid receipt.sourceReceipt
  source_frontier_activated :
    receipt.sourceReceipt.activationStateAfter = .activatedNotInvoked
  adapter_invocation_performed : receipt.adapterInvocationPerformed = true
  adapter_host_invocation_performed :
    receipt.adapterHostInvocationPerformed = true
  exactly_one_adapter_invoked : receipt.exactlyOneAdapterInvoked = true
  bounded_scope_preserved : receipt.boundedScopePreserved = true
  effect_ceiling_preserved : receipt.effectCeilingPreserved = true
  frontier_sequence_preserved :
    receipt.activationFrontierSequencePreserved = true
  completed_prefix_preserved : receipt.completedPrefixPreserved = true
  later_candidates_uninvoked :
    receipt.laterCandidatesRemainUninvoked = true
  lease_reservation_consumed :
    receipt.adapterLeaseReservationConsumed = true
  lease_use_consumed : receipt.adapterLeaseUseConsumed = true
  lease_not_double_decremented :
    receipt.adapterLeaseDoubleDecremented = false
  lease_consumption_record_issued :
    receipt.leaseConsumptionRecordIssued = true
  invocation_nonce_consumed : receipt.invocationNonceConsumed = true
  invocation_nonce_replay_closed :
    receipt.invocationNonceReplayClosed = true
  frontier_invocation_replay_closed :
    receipt.frontierInvocationReplayClosed = true
  invocation_result_envelope_issued :
    receipt.invocationResultEnvelopeIssued = true
  effect_proposal_recorded : receipt.effectProposalRecorded = true
  effect_commit_required : receipt.effectCommitRequired = true
  effect_commit_not_performed : receipt.effectCommitPerformed = false
  observation_intake_required : receipt.observationIntakeRequired = true
  verification_debt_open : receipt.verificationDebtOpen = true
  registry_snapshot_unchanged :
    receipt.adapterRegistrySnapshotUnchanged = true
  world_conditions_current : receipt.worldConditionsCurrent = true
  invocation_delay_current : receipt.invocationDelayCurrent = true
  lease_reservation_fresh :
    receipt.leaseReservationReplayFreshBeforeConsumption = true
  invocation_nonce_fresh :
    receipt.invocationNonceReplayFreshBeforeConsumption = true
  frontier_fresh : receipt.frontierReplayFreshBeforeInvocation = true
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
  tool_not_invoked : receipt.toolInvocationPerformed = false
  external_side_effect_not_performed :
    receipt.externalSideEffectPerformed = false
  execution_authority_not_granted :
    receipt.executionAuthorityGranted = false
  execution_permission_false : receipt.executionPermission = false
  persistent_world_state_unchanged :
    receipt.persistentWorldStateChanged = false
  active_now_false : receipt.activeNow = false

theorem activated_frontier_is_required_for_bounded_adapter_invocation
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt)
    (valid : DukkhaPreservingBoundedAdapterInvocationReceiptValid receipt) :
    receipt.sourceReceipt.activationStateAfter = .activatedNotInvoked ∧
      receipt.adapterInvocationPerformed = true := by
  exact ⟨valid.source_frontier_activated,
    valid.adapter_invocation_performed⟩

theorem bounded_adapter_invocation_has_exact_uncommitted_transition
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt) :
    receipt.invocationStateBefore = .activatedNotInvoked ∧
      receipt.invocationStateAfter = .invokedEffectNotCommitted := by
  exact receipt.invocationTransitionExact

theorem bounded_adapter_invocation_preserves_frontier_order
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt)
    (valid : DukkhaPreservingBoundedAdapterInvocationReceiptValid receipt) :
    receipt.exactlyOneAdapterInvoked = true ∧
      receipt.activationFrontierSequencePreserved = true ∧
      receipt.completedPrefixPreserved = true ∧
      receipt.laterCandidatesRemainUninvoked = true := by
  exact ⟨valid.exactly_one_adapter_invoked,
    valid.frontier_sequence_preserved,
    valid.completed_prefix_preserved,
    valid.later_candidates_uninvoked⟩

theorem adapter_invocation_consumes_reserved_lease_once
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt)
    (valid : DukkhaPreservingBoundedAdapterInvocationReceiptValid receipt) :
    receipt.adapterLeaseReservationConsumed = true ∧
      receipt.adapterLeaseUseConsumed = true ∧
      receipt.adapterLeaseDoubleDecremented = false ∧
      receipt.leaseConsumptionRecordIssued = true := by
  exact ⟨valid.lease_reservation_consumed,
    valid.lease_use_consumed,
    valid.lease_not_double_decremented,
    valid.lease_consumption_record_issued⟩

theorem adapter_invocation_closes_nonce_and_frontier_replay
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt)
    (valid : DukkhaPreservingBoundedAdapterInvocationReceiptValid receipt) :
    receipt.invocationNonceConsumed = true ∧
      receipt.invocationNonceReplayClosed = true ∧
      receipt.frontierInvocationReplayClosed = true := by
  exact ⟨valid.invocation_nonce_consumed,
    valid.invocation_nonce_replay_closed,
    valid.frontier_invocation_replay_closed⟩

theorem adapter_invocation_records_effect_without_commit
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt)
    (valid : DukkhaPreservingBoundedAdapterInvocationReceiptValid receipt) :
    receipt.invocationResultEnvelopeIssued = true ∧
      receipt.effectProposalRecorded = true ∧
      receipt.effectCommitRequired = true ∧
      receipt.effectCommitPerformed = false ∧
      receipt.observationIntakeRequired = true ∧
      receipt.verificationDebtOpen = true := by
  exact ⟨valid.invocation_result_envelope_issued,
    valid.effect_proposal_recorded,
    valid.effect_commit_required,
    valid.effect_commit_not_performed,
    valid.observation_intake_required,
    valid.verification_debt_open⟩

theorem adapter_invocation_preserves_dukkha_and_nonexternalization
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt)
    (valid : DukkhaPreservingBoundedAdapterInvocationReceiptValid receipt) :
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

theorem adapter_invocation_preserves_alternatives_dissent_and_minority
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt)
    (valid : DukkhaPreservingBoundedAdapterInvocationReceiptValid receipt) :
    receipt.alternativeCandidatesPreserved = true ∧
      receipt.dissentPreserved = true ∧
      receipt.minorityPreserved = true := by
  exact ⟨valid.alternative_candidates_preserved,
    valid.dissent_preserved,
    valid.minority_preserved⟩

theorem adapter_invocation_preserves_lineage_and_responsibility
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt) :
    receipt.sourceLineage ⊆ receipt.resultingLineage ∧
      receipt.sourceResponsibility ⊆ receipt.resultingResponsibility := by
  exact ⟨receipt.lineageMonotone, receipt.responsibilityMonotone⟩

theorem adapter_invocation_grants_no_selection_revision_or_minimization_authority
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt)
    (valid : DukkhaPreservingBoundedAdapterInvocationReceiptValid receipt) :
    receipt.selectionRemainsDecisionOSOwned = true ∧
      receipt.selectionAuthorityGrantedToActOS = false ∧
      receipt.planRevisionAuthorityGrantedToActOS = false ∧
      receipt.dukkhaMinimizationAuthorityGrantedToActOS = false := by
  exact ⟨valid.selection_remains_decisionos_owned,
    valid.selection_authority_not_granted,
    valid.plan_revision_authority_not_granted,
    valid.dukkha_minimization_authority_not_granted⟩

theorem adapter_invocation_is_not_tool_external_effect_or_world_commit
    (receipt : DukkhaPreservingBoundedAdapterInvocationReceipt)
    (valid : DukkhaPreservingBoundedAdapterInvocationReceiptValid receipt) :
    receipt.toolInvocationPerformed = false ∧
      receipt.externalSideEffectPerformed = false ∧
      receipt.effectCommitPerformed = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.executionPermission = false ∧
      receipt.persistentWorldStateChanged = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.tool_not_invoked,
    valid.external_side_effect_not_performed,
    valid.effect_commit_not_performed,
    valid.execution_authority_not_granted,
    valid.execution_permission_false,
    valid.persistent_world_state_unchanged,
    valid.active_now_false⟩

end KUOS.ActOS.DukkhaPreservingBoundedAdapterInvocationV0_8
