import Mathlib
import KUOS.ObserveOS.DukkhaPreservingExternalHostEffectObservationIntakeV0_5

namespace KUOS.VerifyOS.DukkhaPreservingObservedHostEffectVerificationIntakeV0_7

open KUOS.ObserveOS.DukkhaPreservingExternalHostEffectObservationIntakeV0_5

inductive ObservedHostEffectVerificationDisposition where
  | effectVerificationSupported
  | worldRefreshRequired
  | verificationContextRefreshRequired
  | verificationReviewRefreshRequired
  | additionalObservationRequired
  | calibrationRepairRequired
  | provenanceRepairRequired
  | effectContractRepairRequired
  | nonexternalizationReviewRequired
  | dukkhaPreservationContradicted
  | replayConflictRejected
  deriving DecidableEq, Repr

inductive ObservedHostEffectVerificationState where
  | hostEffectObservedUnverified
  | hostEffectVerifiedWorldNotUpdated
  deriving DecidableEq, Repr

structure DukkhaPreservingObservedHostEffectVerificationReceipt where
  sourceReceipt : DukkhaPreservingExternalHostEffectObservationReceipt
  sourceObservationReceiptDigest : String
  sourceObservationRecordDigest : String
  sourceVerificationHandoffEnvelopeDigest : String
  effectVerificationReviewCertificateDigest : String
  verificationIntakeContextDigest : String
  verificationRecordDigest : String
  verificationDebtConsumptionRecordDigest : String
  worldDispositionHandoffEnvelopeDigest : String
  invokedFrontierCandidateId : String
  invokedFrontierAdapterId : String
  invokedFrontierBindingDigest : String
  verifierId : String
  verificationDisposition : ObservedHostEffectVerificationDisposition
  verificationStateBefore : ObservedHostEffectVerificationState
  verificationStateAfter : ObservedHostEffectVerificationState
  sourceObservationReceiptSupplied : Bool
  sourceObservationReceiptFullyRevalidated : Bool
  effectVerificationReviewCertificateBound : Bool
  verifierIdentityBound : Bool
  verificationMethodBound : Bool
  verificationEvidenceBound : Bool
  expectedEffectContractBound : Bool
  observedValueDigestBound : Bool
  uncertaintyDigestBound : Bool
  calibrationDigestBound : Bool
  provenanceChainBound : Bool
  dukkhaImpactAssessmentBound : Bool
  protectedGroupImpactAssessmentBound : Bool
  futureSubjectImpactAssessmentBound : Bool
  exactlyOneVerificationReceiptIssued : Bool
  verificationReviewPerformed : Bool
  verificationCompleted : Bool
  effectConformanceVerified : Bool
  dukkhaPreservationVerified : Bool
  protectedGroupNonexternalizationVerified : Bool
  futureNonexternalizationVerified : Bool
  verificationDebtConsumed : Bool
  verificationDebtReplayClosed : Bool
  verificationDoubleConsumed : Bool
  verificationReviewCertificateReplayClosed : Bool
  verificationIntakeNonceConsumed : Bool
  verificationIntakeNonceReplayClosed : Bool
  sourceObservationReceiptReplayClosed : Bool
  worldConditionsCurrent : Bool
  verificationReviewDurationCurrent : Bool
  verificationIntakeDelayCurrent : Bool
  verificationDebtOpen : Bool
  worldDispositionIntakeAdmitted : Bool
  worldDispositionReceiptRequired : Bool
  worldDispositionCompleted : Bool
  persistentWorldModelStateUnchanged : Bool
  worldFactConfirmed : Bool
  causalAttributionConfirmed : Bool
  dukkhaReductionRealizedConfirmed : Bool
  hostOperationReexecuted : Bool
  observationReperformed : Bool
  toolInvocationPerformed : Bool
  externalSideEffectPerformed : Bool
  persistentHostStateChangedByVerification : Bool
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
  selectionAuthorityGrantedToVerifyOS : Bool
  planRevisionAuthorityGrantedToVerifyOS : Bool
  dukkhaMinimizationAuthorityGrantedToVerifyOS : Bool
  generalExecutionAuthorityGranted : Bool
  executionPermission : Bool
  worldMutationAuthorityGranted : Bool
  activeNow : Bool
  sourceLineage : Finset String
  resultingLineage : Finset String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  sourceObservationRecorded :
    sourceReceipt.observationStateAfter =
      ExternalHostEffectObservationState.hostEffectObservedUnverified
  supportedTransition :
    verificationDisposition = .effectVerificationSupported →
      verificationStateBefore = .hostEffectObservedUnverified ∧
        verificationStateAfter = .hostEffectVerifiedWorldNotUpdated
  routedTransition :
    verificationDisposition ≠ .effectVerificationSupported →
      verificationStateBefore = .hostEffectObservedUnverified ∧
        verificationStateAfter = .hostEffectObservedUnverified
  supportedCompletion :
    verificationDisposition = .effectVerificationSupported →
      verificationCompleted = true ∧
        effectConformanceVerified = true ∧
        dukkhaPreservationVerified = true ∧
        protectedGroupNonexternalizationVerified = true ∧
        futureNonexternalizationVerified = true ∧
        verificationDebtConsumed = true ∧
        verificationDebtReplayClosed = true ∧
        sourceObservationReceiptReplayClosed = true ∧
        verificationDebtOpen = false ∧
        worldDispositionIntakeAdmitted = true ∧
        worldDispositionReceiptRequired = true
  routedDebtPreserved :
    verificationDisposition ≠ .effectVerificationSupported →
      verificationCompleted = false ∧
        verificationDebtConsumed = false ∧
        sourceObservationReceiptReplayClosed = false ∧
        verificationDebtOpen = true ∧
        worldDispositionIntakeAdmitted = false ∧
        worldDispositionReceiptRequired = false
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility

structure DukkhaPreservingObservedHostEffectVerificationReceiptValid
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt) : Prop where
  source_valid :
    DukkhaPreservingExternalHostEffectObservationReceiptValid receipt.sourceReceipt
  source_supplied : receipt.sourceObservationReceiptSupplied = true
  source_revalidated : receipt.sourceObservationReceiptFullyRevalidated = true
  review_certificate_bound : receipt.effectVerificationReviewCertificateBound = true
  verifier_identity_bound : receipt.verifierIdentityBound = true
  verification_method_bound : receipt.verificationMethodBound = true
  verification_evidence_bound : receipt.verificationEvidenceBound = true
  expected_contract_bound : receipt.expectedEffectContractBound = true
  observed_value_bound : receipt.observedValueDigestBound = true
  uncertainty_bound : receipt.uncertaintyDigestBound = true
  calibration_bound : receipt.calibrationDigestBound = true
  provenance_bound : receipt.provenanceChainBound = true
  dukkha_assessment_bound : receipt.dukkhaImpactAssessmentBound = true
  protected_group_assessment_bound :
    receipt.protectedGroupImpactAssessmentBound = true
  future_subject_assessment_bound :
    receipt.futureSubjectImpactAssessmentBound = true
  exactly_one_receipt : receipt.exactlyOneVerificationReceiptIssued = true
  review_performed : receipt.verificationReviewPerformed = true
  verification_not_double_consumed : receipt.verificationDoubleConsumed = false
  review_replay_closed : receipt.verificationReviewCertificateReplayClosed = true
  nonce_consumed : receipt.verificationIntakeNonceConsumed = true
  nonce_replay_closed : receipt.verificationIntakeNonceReplayClosed = true
  world_disposition_not_completed : receipt.worldDispositionCompleted = false
  world_model_unchanged : receipt.persistentWorldModelStateUnchanged = true
  world_fact_not_confirmed : receipt.worldFactConfirmed = false
  causality_not_confirmed : receipt.causalAttributionConfirmed = false
  realized_dukkha_not_confirmed : receipt.dukkhaReductionRealizedConfirmed = false
  host_operation_not_reexecuted : receipt.hostOperationReexecuted = false
  observation_not_reperformed : receipt.observationReperformed = false
  tool_not_invoked : receipt.toolInvocationPerformed = false
  side_effect_not_performed : receipt.externalSideEffectPerformed = false
  host_state_not_changed : receipt.persistentHostStateChangedByVerification = false
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
  protected_group_preserved :
    receipt.protectedGroupNonexternalizationPreserved = true
  future_nonexternalization_preserved :
    receipt.futureNonexternalizationPreserved = true
  revision_capacity_preserved : receipt.revisionCapacityPreserved = true
  persistent_loop_reduction_preserved :
    receipt.persistentLoopReductionPreserved = true
  scalar_utility_not_introduced : receipt.singleScalarUtilityNotIntroduced = true
  selection_owned_by_decisionos : receipt.selectionRemainsDecisionOSOwned = true
  selection_authority_not_granted :
    receipt.selectionAuthorityGrantedToVerifyOS = false
  revision_authority_not_granted :
    receipt.planRevisionAuthorityGrantedToVerifyOS = false
  minimization_authority_not_granted :
    receipt.dukkhaMinimizationAuthorityGrantedToVerifyOS = false
  general_execution_not_granted : receipt.generalExecutionAuthorityGranted = false
  execution_permission_false : receipt.executionPermission = false
  world_mutation_not_granted : receipt.worldMutationAuthorityGranted = false
  active_now_false : receipt.activeNow = false


theorem observation_receipt_is_required_for_verification_intake
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt) :
    receipt.sourceReceipt.observationStateAfter =
        ExternalHostEffectObservationState.hostEffectObservedUnverified := by
  exact receipt.sourceObservationRecorded


theorem supported_verification_has_exact_world_unupdated_transition
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt)
    (h : receipt.verificationDisposition = .effectVerificationSupported) :
    receipt.verificationStateBefore = .hostEffectObservedUnverified ∧
      receipt.verificationStateAfter = .hostEffectVerifiedWorldNotUpdated := by
  exact receipt.supportedTransition h


theorem routed_verification_preserves_observed_unverified_state
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt)
    (h : receipt.verificationDisposition ≠ .effectVerificationSupported) :
    receipt.verificationStateBefore = .hostEffectObservedUnverified ∧
      receipt.verificationStateAfter = .hostEffectObservedUnverified := by
  exact receipt.routedTransition h


theorem verification_binds_review_method_evidence_and_assessments
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt)
    (valid : DukkhaPreservingObservedHostEffectVerificationReceiptValid receipt) :
    receipt.effectVerificationReviewCertificateBound = true ∧
      receipt.verifierIdentityBound = true ∧
      receipt.verificationMethodBound = true ∧
      receipt.verificationEvidenceBound = true ∧
      receipt.expectedEffectContractBound = true ∧
      receipt.observedValueDigestBound = true ∧
      receipt.uncertaintyDigestBound = true ∧
      receipt.calibrationDigestBound = true ∧
      receipt.provenanceChainBound = true ∧
      receipt.dukkhaImpactAssessmentBound = true ∧
      receipt.protectedGroupImpactAssessmentBound = true ∧
      receipt.futureSubjectImpactAssessmentBound = true := by
  exact ⟨valid.review_certificate_bound,
    valid.verifier_identity_bound,
    valid.verification_method_bound,
    valid.verification_evidence_bound,
    valid.expected_contract_bound,
    valid.observed_value_bound,
    valid.uncertainty_bound,
    valid.calibration_bound,
    valid.provenance_bound,
    valid.dukkha_assessment_bound,
    valid.protected_group_assessment_bound,
    valid.future_subject_assessment_bound⟩


theorem supported_verification_consumes_debt_once
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt)
    (h : receipt.verificationDisposition = .effectVerificationSupported) :
    receipt.verificationCompleted = true ∧
      receipt.effectConformanceVerified = true ∧
      receipt.dukkhaPreservationVerified = true ∧
      receipt.protectedGroupNonexternalizationVerified = true ∧
      receipt.futureNonexternalizationVerified = true ∧
      receipt.verificationDebtConsumed = true ∧
      receipt.verificationDebtReplayClosed = true ∧
      receipt.sourceObservationReceiptReplayClosed = true ∧
      receipt.verificationDebtOpen = false ∧
      receipt.worldDispositionIntakeAdmitted = true ∧
      receipt.worldDispositionReceiptRequired = true := by
  exact receipt.supportedCompletion h


theorem routed_verification_keeps_debt_open
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt)
    (h : receipt.verificationDisposition ≠ .effectVerificationSupported) :
    receipt.verificationCompleted = false ∧
      receipt.verificationDebtConsumed = false ∧
      receipt.sourceObservationReceiptReplayClosed = false ∧
      receipt.verificationDebtOpen = true ∧
      receipt.worldDispositionIntakeAdmitted = false ∧
      receipt.worldDispositionReceiptRequired = false := by
  exact receipt.routedDebtPreserved h


theorem verification_receipt_is_not_world_fact_or_causal_attribution
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt)
    (valid : DukkhaPreservingObservedHostEffectVerificationReceiptValid receipt) :
    receipt.persistentWorldModelStateUnchanged = true ∧
      receipt.worldFactConfirmed = false ∧
      receipt.causalAttributionConfirmed = false ∧
      receipt.dukkhaReductionRealizedConfirmed = false ∧
      receipt.worldDispositionCompleted = false := by
  exact ⟨valid.world_model_unchanged,
    valid.world_fact_not_confirmed,
    valid.causality_not_confirmed,
    valid.realized_dukkha_not_confirmed,
    valid.world_disposition_not_completed⟩


theorem verification_reexecutes_no_host_operation_observation_tool_or_effect
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt)
    (valid : DukkhaPreservingObservedHostEffectVerificationReceiptValid receipt) :
    receipt.hostOperationReexecuted = false ∧
      receipt.observationReperformed = false ∧
      receipt.toolInvocationPerformed = false ∧
      receipt.externalSideEffectPerformed = false ∧
      receipt.persistentHostStateChangedByVerification = false := by
  exact ⟨valid.host_operation_not_reexecuted,
    valid.observation_not_reperformed,
    valid.tool_not_invoked,
    valid.side_effect_not_performed,
    valid.host_state_not_changed⟩


theorem verification_forbids_automatic_truth_completion_rollback_or_compensation
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt)
    (valid : DukkhaPreservingObservedHostEffectVerificationReceiptValid receipt) :
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


theorem verification_preserves_dukkha_and_nonexternalization
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt)
    (valid : DukkhaPreservingObservedHostEffectVerificationReceiptValid receipt) :
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


theorem verification_preserves_alternatives_dissent_and_minority
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt)
    (valid : DukkhaPreservingObservedHostEffectVerificationReceiptValid receipt) :
    receipt.alternativeCandidatesPreserved = true ∧
      receipt.dissentPreserved = true ∧
      receipt.minorityPreserved = true := by
  exact ⟨valid.alternatives_preserved,
    valid.dissent_preserved,
    valid.minority_preserved⟩


theorem verification_preserves_lineage_and_responsibility
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt) :
    receipt.sourceLineage ⊆ receipt.resultingLineage ∧
      receipt.sourceResponsibility ⊆ receipt.resultingResponsibility := by
  exact ⟨receipt.lineageMonotone, receipt.responsibilityMonotone⟩


theorem verification_grants_no_selection_revision_minimization_execution_or_world_authority
    (receipt : DukkhaPreservingObservedHostEffectVerificationReceipt)
    (valid : DukkhaPreservingObservedHostEffectVerificationReceiptValid receipt) :
    receipt.selectionRemainsDecisionOSOwned = true ∧
      receipt.selectionAuthorityGrantedToVerifyOS = false ∧
      receipt.planRevisionAuthorityGrantedToVerifyOS = false ∧
      receipt.dukkhaMinimizationAuthorityGrantedToVerifyOS = false ∧
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

end KUOS.VerifyOS.DukkhaPreservingObservedHostEffectVerificationIntakeV0_7
