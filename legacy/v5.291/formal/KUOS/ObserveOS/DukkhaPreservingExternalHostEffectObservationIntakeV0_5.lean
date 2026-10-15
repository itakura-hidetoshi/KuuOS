import Mathlib
import KUOS.ActOS.DukkhaPreservingAtomicExternalHostEffectIntakeV0_11

namespace KUOS.ObserveOS.DukkhaPreservingExternalHostEffectObservationIntakeV0_5

open KUOS.ActOS.DukkhaPreservingAtomicExternalHostEffectIntakeV0_11

inductive ExternalHostEffectObservationState where
  | hostEffectRecordedUnobserved
  | hostEffectObservedUnverified
  deriving DecidableEq, Repr

structure DukkhaPreservingExternalHostEffectObservationReceipt where
  sourceReceipt : DukkhaPreservingAtomicExternalHostEffectReceipt
  sourceHostEffectReceiptDigest : String
  sourceExternalHostEffectRecordDigest : String
  sourceObservationHandoffEnvelopeDigest : String
  independentObservationEvidencePacketDigest : String
  observationIntakeContextDigest : String
  observationRecordDigest : String
  observationDebtConsumptionRecordDigest : String
  verificationHandoffEnvelopeDigest : String
  invokedFrontierCandidateId : String
  invokedFrontierAdapterId : String
  invokedFrontierBindingDigest : String
  collectorId : String
  evidenceSourceId : String
  observationStateBefore : ExternalHostEffectObservationState
  observationStateAfter : ExternalHostEffectObservationState
  sourceHostEffectReceiptSupplied : Bool
  sourceHostEffectReceiptFullyRevalidated : Bool
  independentObservationEvidenceBound : Bool
  collectorIdentityBound : Bool
  evidenceSourceIdentityBound : Bool
  collectionEpochFreshnessConfirmed : Bool
  rawArtifactDigestBound : Bool
  observedValueDigestBound : Bool
  uncertaintyDigestBound : Bool
  calibrationDigestBound : Bool
  contextDigestBound : Bool
  tamperEvidenceDigestBound : Bool
  provenanceChainPreserved : Bool
  hostEffectObservationIdentityExact : Bool
  exactlyOneObservationReceiptIssued : Bool
  observationPerformed : Bool
  independentWorldEvidencePresent : Bool
  observationDebtConsumed : Bool
  observationDebtReplayClosed : Bool
  observationDoubleConsumed : Bool
  observationEvidencePacketReplayClosed : Bool
  observationIntakeNonceConsumed : Bool
  observationIntakeNonceReplayClosed : Bool
  sourceHostEffectReceiptReplayClosed : Bool
  sessionFreshBeforeIntake : Bool
  evidenceFreshBeforeIntake : Bool
  nonceFreshBeforeIntake : Bool
  sourceReceiptFreshBeforeObservation : Bool
  worldConditionsCurrent : Bool
  observationCollectionDurationCurrent : Bool
  observationIntakeDelayCurrent : Bool
  collectorIndependentFromHostDriver : Bool
  evidenceSourceIndependentFromHostReceipt : Bool
  hostReceiptUsedAsIndependentEvidence : Bool
  hostOperationReexecuted : Bool
  toolInvocationPerformed : Bool
  externalSideEffectPerformed : Bool
  persistentHostStateChangedByObservation : Bool
  persistentWorldModelStateUnchanged : Bool
  worldFactConfirmed : Bool
  causalAttributionConfirmed : Bool
  verificationIntakeRequired : Bool
  verificationIntakeAdmitted : Bool
  verificationReceiptRequired : Bool
  verificationCompleted : Bool
  verificationDebtOpen : Bool
  compensationRouteReady : Bool
  compensationPerformed : Bool
  automaticTruthPromotion : Bool
  automaticPlanCompletion : Bool
  automaticRollback : Bool
  automaticCompensation : Bool
  effectScopePreserved : Bool
  effectCeilingPreserved : Bool
  checkpointGuardsPreserved : Bool
  stopConditionsPreserved : Bool
  evidenceLineagePreserved : Bool
  responsibilityLineagePreserved : Bool
  alternativeCandidatesPreserved : Bool
  dissentPreserved : Bool
  minorityPreserved : Bool
  dukkhaReductionSupportPreserved : Bool
  protectedGroupNonexternalizationPreserved : Bool
  futureNonexternalizationPreserved : Bool
  revisionCapacityPreserved : Bool
  persistentLoopReductionPreserved : Bool
  singleScalarUtilityNotIntroduced : Bool
  selectionRemainsDecisionOSOwned : Bool
  selectionAuthorityGrantedToObserveOS : Bool
  planRevisionAuthorityGrantedToObserveOS : Bool
  dukkhaMinimizationAuthorityGrantedToObserveOS : Bool
  generalExecutionAuthorityGranted : Bool
  executionPermission : Bool
  worldMutationAuthorityGranted : Bool
  activeNow : Bool
  sourceLineage : Finset String
  resultingLineage : Finset String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  sourceHostEffectRecorded :
    sourceReceipt.hostEffectStateAfter =
      AtomicExternalHostEffectState.hostEffectRecordedUnobserved
  transitionExact :
    observationStateBefore = .hostEffectRecordedUnobserved ∧
      observationStateAfter = .hostEffectObservedUnverified
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility

structure DukkhaPreservingExternalHostEffectObservationReceiptValid
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt) : Prop where
  source_valid : DukkhaPreservingAtomicExternalHostEffectReceiptValid receipt.sourceReceipt
  source_supplied : receipt.sourceHostEffectReceiptSupplied = true
  source_revalidated : receipt.sourceHostEffectReceiptFullyRevalidated = true
  independent_evidence_bound : receipt.independentObservationEvidenceBound = true
  collector_identity_bound : receipt.collectorIdentityBound = true
  evidence_source_identity_bound : receipt.evidenceSourceIdentityBound = true
  collection_fresh : receipt.collectionEpochFreshnessConfirmed = true
  raw_artifact_bound : receipt.rawArtifactDigestBound = true
  observed_value_bound : receipt.observedValueDigestBound = true
  uncertainty_bound : receipt.uncertaintyDigestBound = true
  calibration_bound : receipt.calibrationDigestBound = true
  context_bound : receipt.contextDigestBound = true
  tamper_evidence_bound : receipt.tamperEvidenceDigestBound = true
  provenance_preserved : receipt.provenanceChainPreserved = true
  observation_identity_exact : receipt.hostEffectObservationIdentityExact = true
  exactly_one_observation_receipt : receipt.exactlyOneObservationReceiptIssued = true
  observation_performed : receipt.observationPerformed = true
  independent_world_evidence_present : receipt.independentWorldEvidencePresent = true
  observation_debt_consumed : receipt.observationDebtConsumed = true
  observation_debt_replay_closed : receipt.observationDebtReplayClosed = true
  observation_not_double_consumed : receipt.observationDoubleConsumed = false
  evidence_packet_replay_closed : receipt.observationEvidencePacketReplayClosed = true
  nonce_consumed : receipt.observationIntakeNonceConsumed = true
  nonce_replay_closed : receipt.observationIntakeNonceReplayClosed = true
  source_replay_closed : receipt.sourceHostEffectReceiptReplayClosed = true
  session_fresh : receipt.sessionFreshBeforeIntake = true
  evidence_fresh : receipt.evidenceFreshBeforeIntake = true
  nonce_fresh : receipt.nonceFreshBeforeIntake = true
  source_receipt_fresh : receipt.sourceReceiptFreshBeforeObservation = true
  world_current : receipt.worldConditionsCurrent = true
  collection_duration_current : receipt.observationCollectionDurationCurrent = true
  intake_delay_current : receipt.observationIntakeDelayCurrent = true
  collector_independent : receipt.collectorIndependentFromHostDriver = true
  evidence_source_independent : receipt.evidenceSourceIndependentFromHostReceipt = true
  host_receipt_not_evidence : receipt.hostReceiptUsedAsIndependentEvidence = false
  host_operation_not_reexecuted : receipt.hostOperationReexecuted = false
  tool_not_invoked : receipt.toolInvocationPerformed = false
  side_effect_not_performed : receipt.externalSideEffectPerformed = false
  host_state_not_changed : receipt.persistentHostStateChangedByObservation = false
  world_model_unchanged : receipt.persistentWorldModelStateUnchanged = true
  world_fact_not_confirmed : receipt.worldFactConfirmed = false
  causality_not_confirmed : receipt.causalAttributionConfirmed = false
  verification_required : receipt.verificationIntakeRequired = true
  verification_admitted : receipt.verificationIntakeAdmitted = true
  verification_receipt_required : receipt.verificationReceiptRequired = true
  verification_not_completed : receipt.verificationCompleted = false
  verification_debt_open : receipt.verificationDebtOpen = true
  compensation_ready : receipt.compensationRouteReady = true
  compensation_not_performed : receipt.compensationPerformed = false
  automatic_truth_forbidden : receipt.automaticTruthPromotion = false
  automatic_completion_forbidden : receipt.automaticPlanCompletion = false
  automatic_rollback_forbidden : receipt.automaticRollback = false
  automatic_compensation_forbidden : receipt.automaticCompensation = false
  scope_preserved : receipt.effectScopePreserved = true
  ceiling_preserved : receipt.effectCeilingPreserved = true
  checkpoint_guards_preserved : receipt.checkpointGuardsPreserved = true
  stop_conditions_preserved : receipt.stopConditionsPreserved = true
  evidence_lineage_preserved : receipt.evidenceLineagePreserved = true
  responsibility_lineage_preserved : receipt.responsibilityLineagePreserved = true
  alternatives_preserved : receipt.alternativeCandidatesPreserved = true
  dissent_preserved : receipt.dissentPreserved = true
  minority_preserved : receipt.minorityPreserved = true
  dukkha_support_preserved : receipt.dukkhaReductionSupportPreserved = true
  protected_group_preserved : receipt.protectedGroupNonexternalizationPreserved = true
  future_nonexternalization_preserved : receipt.futureNonexternalizationPreserved = true
  revision_capacity_preserved : receipt.revisionCapacityPreserved = true
  persistent_loop_reduction_preserved : receipt.persistentLoopReductionPreserved = true
  scalar_utility_not_introduced : receipt.singleScalarUtilityNotIntroduced = true
  selection_owned_by_decisionos : receipt.selectionRemainsDecisionOSOwned = true
  selection_authority_not_granted : receipt.selectionAuthorityGrantedToObserveOS = false
  revision_authority_not_granted : receipt.planRevisionAuthorityGrantedToObserveOS = false
  minimization_authority_not_granted :
    receipt.dukkhaMinimizationAuthorityGrantedToObserveOS = false
  general_execution_not_granted : receipt.generalExecutionAuthorityGranted = false
  execution_permission_false : receipt.executionPermission = false
  world_mutation_not_granted : receipt.worldMutationAuthorityGranted = false
  active_now_false : receipt.activeNow = false

theorem host_effect_receipt_is_required_for_observation_intake
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt) :
    receipt.sourceReceipt.hostEffectStateAfter =
        AtomicExternalHostEffectState.hostEffectRecordedUnobserved ∧
      receipt.observationStateBefore = .hostEffectRecordedUnobserved := by
  exact ⟨receipt.sourceHostEffectRecorded, receipt.transitionExact.1⟩

theorem observation_has_exact_unverified_transition
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt) :
    receipt.observationStateBefore = .hostEffectRecordedUnobserved ∧
      receipt.observationStateAfter = .hostEffectObservedUnverified := by
  exact receipt.transitionExact

theorem observation_binds_independent_evidence_and_provenance
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt)
    (valid : DukkhaPreservingExternalHostEffectObservationReceiptValid receipt) :
    receipt.independentObservationEvidenceBound = true ∧
      receipt.collectorIdentityBound = true ∧
      receipt.evidenceSourceIdentityBound = true ∧
      receipt.rawArtifactDigestBound = true ∧
      receipt.observedValueDigestBound = true ∧
      receipt.uncertaintyDigestBound = true ∧
      receipt.calibrationDigestBound = true ∧
      receipt.contextDigestBound = true ∧
      receipt.tamperEvidenceDigestBound = true ∧
      receipt.provenanceChainPreserved = true := by
  exact ⟨valid.independent_evidence_bound,
    valid.collector_identity_bound,
    valid.evidence_source_identity_bound,
    valid.raw_artifact_bound,
    valid.observed_value_bound,
    valid.uncertainty_bound,
    valid.calibration_bound,
    valid.context_bound,
    valid.tamper_evidence_bound,
    valid.provenance_preserved⟩

theorem observation_records_exactly_one_receipt
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt)
    (valid : DukkhaPreservingExternalHostEffectObservationReceiptValid receipt) :
    receipt.hostEffectObservationIdentityExact = true ∧
      receipt.exactlyOneObservationReceiptIssued = true ∧
      receipt.observationPerformed = true ∧
      receipt.independentWorldEvidencePresent = true := by
  exact ⟨valid.observation_identity_exact,
    valid.exactly_one_observation_receipt,
    valid.observation_performed,
    valid.independent_world_evidence_present⟩

theorem observation_closes_nonce_source_and_debt_replay
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt)
    (valid : DukkhaPreservingExternalHostEffectObservationReceiptValid receipt) :
    receipt.observationDebtConsumed = true ∧
      receipt.observationDebtReplayClosed = true ∧
      receipt.observationDoubleConsumed = false ∧
      receipt.observationEvidencePacketReplayClosed = true ∧
      receipt.observationIntakeNonceConsumed = true ∧
      receipt.observationIntakeNonceReplayClosed = true ∧
      receipt.sourceHostEffectReceiptReplayClosed = true := by
  exact ⟨valid.observation_debt_consumed,
    valid.observation_debt_replay_closed,
    valid.observation_not_double_consumed,
    valid.evidence_packet_replay_closed,
    valid.nonce_consumed,
    valid.nonce_replay_closed,
    valid.source_replay_closed⟩

theorem observation_distinguishes_collector_from_host_driver_and_kernel
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt)
    (valid : DukkhaPreservingExternalHostEffectObservationReceiptValid receipt) :
    receipt.collectorIndependentFromHostDriver = true ∧
      receipt.evidenceSourceIndependentFromHostReceipt = true ∧
      receipt.hostReceiptUsedAsIndependentEvidence = false ∧
      receipt.hostOperationReexecuted = false ∧
      receipt.toolInvocationPerformed = false ∧
      receipt.externalSideEffectPerformed = false := by
  exact ⟨valid.collector_independent,
    valid.evidence_source_independent,
    valid.host_receipt_not_evidence,
    valid.host_operation_not_reexecuted,
    valid.tool_not_invoked,
    valid.side_effect_not_performed⟩

theorem observation_preserves_world_model_nontruth_boundary
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt)
    (valid : DukkhaPreservingExternalHostEffectObservationReceiptValid receipt) :
    receipt.persistentHostStateChangedByObservation = false ∧
      receipt.persistentWorldModelStateUnchanged = true ∧
      receipt.worldFactConfirmed = false ∧
      receipt.causalAttributionConfirmed = false := by
  exact ⟨valid.host_state_not_changed,
    valid.world_model_unchanged,
    valid.world_fact_not_confirmed,
    valid.causality_not_confirmed⟩

theorem observation_admits_verification_and_preserves_verification_debt
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt)
    (valid : DukkhaPreservingExternalHostEffectObservationReceiptValid receipt) :
    receipt.verificationIntakeRequired = true ∧
      receipt.verificationIntakeAdmitted = true ∧
      receipt.verificationReceiptRequired = true ∧
      receipt.verificationCompleted = false ∧
      receipt.verificationDebtOpen = true := by
  exact ⟨valid.verification_required,
    valid.verification_admitted,
    valid.verification_receipt_required,
    valid.verification_not_completed,
    valid.verification_debt_open⟩

theorem observation_forbids_automatic_truth_completion_rollback_or_compensation
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt)
    (valid : DukkhaPreservingExternalHostEffectObservationReceiptValid receipt) :
    receipt.automaticTruthPromotion = false ∧
      receipt.automaticPlanCompletion = false ∧
      receipt.automaticRollback = false ∧
      receipt.automaticCompensation = false ∧
      receipt.compensationRouteReady = true ∧
      receipt.compensationPerformed = false := by
  exact ⟨valid.automatic_truth_forbidden,
    valid.automatic_completion_forbidden,
    valid.automatic_rollback_forbidden,
    valid.automatic_compensation_forbidden,
    valid.compensation_ready,
    valid.compensation_not_performed⟩

theorem observation_preserves_dukkha_and_nonexternalization
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt)
    (valid : DukkhaPreservingExternalHostEffectObservationReceiptValid receipt) :
    receipt.dukkhaReductionSupportPreserved = true ∧
      receipt.protectedGroupNonexternalizationPreserved = true ∧
      receipt.futureNonexternalizationPreserved = true ∧
      receipt.revisionCapacityPreserved = true ∧
      receipt.persistentLoopReductionPreserved = true ∧
      receipt.singleScalarUtilityNotIntroduced = true := by
  exact ⟨valid.dukkha_support_preserved,
    valid.protected_group_preserved,
    valid.future_nonexternalization_preserved,
    valid.revision_capacity_preserved,
    valid.persistent_loop_reduction_preserved,
    valid.scalar_utility_not_introduced⟩

theorem observation_preserves_alternatives_dissent_and_minority
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt)
    (valid : DukkhaPreservingExternalHostEffectObservationReceiptValid receipt) :
    receipt.alternativeCandidatesPreserved = true ∧
      receipt.dissentPreserved = true ∧
      receipt.minorityPreserved = true := by
  exact ⟨valid.alternatives_preserved,
    valid.dissent_preserved,
    valid.minority_preserved⟩

theorem observation_preserves_lineage_and_responsibility
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt) :
    receipt.sourceLineage ⊆ receipt.resultingLineage ∧
      receipt.sourceResponsibility ⊆ receipt.resultingResponsibility := by
  exact ⟨receipt.lineageMonotone, receipt.responsibilityMonotone⟩

theorem observation_grants_no_selection_revision_minimization_or_execution_authority
    (receipt : DukkhaPreservingExternalHostEffectObservationReceipt)
    (valid : DukkhaPreservingExternalHostEffectObservationReceiptValid receipt) :
    receipt.selectionRemainsDecisionOSOwned = true ∧
      receipt.selectionAuthorityGrantedToObserveOS = false ∧
      receipt.planRevisionAuthorityGrantedToObserveOS = false ∧
      receipt.dukkhaMinimizationAuthorityGrantedToObserveOS = false ∧
      receipt.generalExecutionAuthorityGranted = false ∧
      receipt.executionPermission = false ∧
      receipt.worldMutationAuthorityGranted = false ∧
      receipt.activeNow = false := by
  exact ⟨valid.selection_owned_by_decisionos,
    valid.selection_authority_not_granted,
    valid.revision_authority_not_granted,
    valid.minimization_authority_not_granted,
    valid.general_execution_not_granted,
    valid.execution_permission_false,
    valid.world_mutation_not_granted,
    valid.active_now_false⟩

end KUOS.ObserveOS.DukkhaPreservingExternalHostEffectObservationIntakeV0_5
