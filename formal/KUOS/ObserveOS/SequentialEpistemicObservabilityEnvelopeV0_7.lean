import Mathlib
import KUOS.ObserveOS.DukkhaPreservingFutureOnlyMaintenanceMonitoringObservationIntakeV0_6

namespace KUOS.ObserveOS.SequentialEpistemicObservabilityEnvelopeV0_7

inductive SequentialEpistemicObservabilityDisposition where
  | sequentialEpistemicObservabilitySupported
  | sourceObservationReceiptRepairRequired
  | traceContextRepairRequired
  | signalCoverageRepairRequired
  | provenanceRepairRequired
  | sampleAccountingRepairRequired
  | missingnessReviewRequired
  | distributionShiftReviewRequired
  | sequentialUncertaintyRepairRequired
  | conformalCalibrationRepairRequired
  | observationWindowRepairRequired
  | replayConflictRejected
  | currentStateMutationRejected
  | authorityEscalationRejected
  deriving DecidableEq, Repr

inductive SequentialEpistemicObservabilityState where
  | boundedMaintenanceMonitoringObservationRecorded
  | boundedMaintenanceMonitoringObservationRecordedObservabilityEnvelopeRecorded
  deriving DecidableEq, Repr

structure SequentialEpistemicObservabilityEnvelopeReceipt where
  sourceObservationReceiptDigest : String
  observabilityPacketDigest : String
  observabilityPolicyDigest : String
  traceId : String
  spanId : String
  provenanceBundleDigest : String
  sequentialUncertaintyDigest : String
  conformalCalibrationDigest : String
  distributionShiftEvidenceDigest : String
  sourceWorldRevision : Nat
  resultingWorldRevision : Nat
  totalSamples : Nat
  observedSamples : Nat
  missingSamples : Nat
  missingFractionPpm : Nat
  maximumMissingFractionPpm : Nat
  conformalCoverageGapPpm : Nat
  maximumConformalCoverageGapPpm : Nat
  disposition : SequentialEpistemicObservabilityDisposition
  stateBefore : SequentialEpistemicObservabilityState
  stateAfter : SequentialEpistemicObservabilityState
  traceContextValid : Bool
  signalCoverageComplete : Bool
  provenanceBound : Bool
  sampleAccountingConfirmed : Bool
  missingnessWithinPolicy : Bool
  distributionShiftDetected : Bool
  sequentialUncertaintyBound : Bool
  conformalCalibrationBound : Bool
  observationWindowValid : Bool
  replayClosed : Bool
  observabilityEnvelopeRecorded : Bool
  verificationCompleted : Bool
  verificationDebtOpen : Bool
  persistentWorldStateChanged : Bool
  worldModelRevisionIncremented : Bool
  currentPlanRevised : Bool
  currentPolicyActivated : Bool
  learningDeltaActivated : Bool
  toolInvocationPerformed : Bool
  externalSideEffectPerformed : Bool
  generalizedTruthClaimed : Bool
  causalVerificationClaimed : Bool
  selectionAuthorityGrantedToObserveOS : Bool
  verificationAuthorityGrantedToObserveOS : Bool
  worldMutationAuthorityGranted : Bool
  policyActivationAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  sourceLineage : Finset String
  resultingLineage : Finset String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  sampleAccounting : observedSamples + missingSamples = totalSamples
  supportedEnvelope :
    disposition = .sequentialEpistemicObservabilitySupported →
      stateBefore = .boundedMaintenanceMonitoringObservationRecorded ∧
        stateAfter =
          .boundedMaintenanceMonitoringObservationRecordedObservabilityEnvelopeRecorded ∧
        traceContextValid = true ∧
        signalCoverageComplete = true ∧
        provenanceBound = true ∧
        sampleAccountingConfirmed = true ∧
        missingnessWithinPolicy = true ∧
        distributionShiftDetected = false ∧
        sequentialUncertaintyBound = true ∧
        conformalCalibrationBound = true ∧
        observationWindowValid = true ∧
        replayClosed = true ∧
        observabilityEnvelopeRecorded = true ∧
        missingFractionPpm ≤ maximumMissingFractionPpm ∧
        conformalCoverageGapPpm ≤ maximumConformalCoverageGapPpm ∧
        verificationCompleted = false ∧
        verificationDebtOpen = true
  routedEnvelope :
    disposition ≠ .sequentialEpistemicObservabilitySupported →
      stateBefore = .boundedMaintenanceMonitoringObservationRecorded ∧
        stateAfter = .boundedMaintenanceMonitoringObservationRecorded ∧
        observabilityEnvelopeRecorded = false
  revisionUnchanged : resultingWorldRevision = sourceWorldRevision
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility

structure SequentialEpistemicObservabilityEnvelopeReceiptValid
    (receipt : SequentialEpistemicObservabilityEnvelopeReceipt) : Prop where
  verificationNotCompleted : receipt.verificationCompleted = false
  verificationDebtPreserved : receipt.verificationDebtOpen = true
  worldNotChanged : receipt.persistentWorldStateChanged = false
  revisionNotIncremented : receipt.worldModelRevisionIncremented = false
  planNotRevised : receipt.currentPlanRevised = false
  policyNotActivated : receipt.currentPolicyActivated = false
  learningNotActivated : receipt.learningDeltaActivated = false
  toolNotInvoked : receipt.toolInvocationPerformed = false
  externalEffectNotPerformed : receipt.externalSideEffectPerformed = false
  noGeneralizedTruth : receipt.generalizedTruthClaimed = false
  noCausalVerification : receipt.causalVerificationClaimed = false
  noSelectionAuthority : receipt.selectionAuthorityGrantedToObserveOS = false
  noVerificationAuthority : receipt.verificationAuthorityGrantedToObserveOS = false
  noWorldMutationAuthority : receipt.worldMutationAuthorityGranted = false
  noPolicyActivationAuthority : receipt.policyActivationAuthorityGranted = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

theorem observed_samples_le_total
    (receipt : SequentialEpistemicObservabilityEnvelopeReceipt) :
    receipt.observedSamples ≤ receipt.totalSamples := by
  have h := receipt.sampleAccounting
  omega

theorem missing_samples_le_total
    (receipt : SequentialEpistemicObservabilityEnvelopeReceipt) :
    receipt.missingSamples ≤ receipt.totalSamples := by
  have h := receipt.sampleAccounting
  omega

theorem sample_partition_is_exact_and_bounded
    (receipt : SequentialEpistemicObservabilityEnvelopeReceipt) :
    receipt.observedSamples + receipt.missingSamples = receipt.totalSamples ∧
      receipt.observedSamples ≤ receipt.totalSamples ∧
      receipt.missingSamples ≤ receipt.totalSamples := by
  exact ⟨receipt.sampleAccounting, observed_samples_le_total receipt,
    missing_samples_le_total receipt⟩

theorem supported_records_observability_without_verification
    (receipt : SequentialEpistemicObservabilityEnvelopeReceipt)
    (h : receipt.disposition =
      .sequentialEpistemicObservabilitySupported) :
    receipt.traceContextValid = true ∧
      receipt.signalCoverageComplete = true ∧
      receipt.provenanceBound = true ∧
      receipt.sampleAccountingConfirmed = true ∧
      receipt.missingnessWithinPolicy = true ∧
      receipt.distributionShiftDetected = false ∧
      receipt.sequentialUncertaintyBound = true ∧
      receipt.conformalCalibrationBound = true ∧
      receipt.observabilityEnvelopeRecorded = true ∧
      receipt.verificationCompleted = false ∧
      receipt.verificationDebtOpen = true := by
  rcases receipt.supportedEnvelope h with
    ⟨_, _, ht, hs, hp, ha, hm, hd, hu, hc, _, _, he, _, _, hv, hvd⟩
  exact ⟨ht, hs, hp, ha, hm, hd, hu, hc, he, hv, hvd⟩

theorem supported_respects_missingness_and_calibration_budgets
    (receipt : SequentialEpistemicObservabilityEnvelopeReceipt)
    (h : receipt.disposition =
      .sequentialEpistemicObservabilitySupported) :
    receipt.missingFractionPpm ≤ receipt.maximumMissingFractionPpm ∧
      receipt.conformalCoverageGapPpm ≤
        receipt.maximumConformalCoverageGapPpm := by
  rcases receipt.supportedEnvelope h with
    ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, hm, hc, _, _⟩
  exact ⟨hm, hc⟩

theorem routed_path_preserves_source_state
    (receipt : SequentialEpistemicObservabilityEnvelopeReceipt)
    (h : receipt.disposition ≠
      .sequentialEpistemicObservabilitySupported) :
    receipt.stateAfter =
        .boundedMaintenanceMonitoringObservationRecorded ∧
      receipt.observabilityEnvelopeRecorded = false := by
  rcases receipt.routedEnvelope h with ⟨_, hs, he⟩
  exact ⟨hs, he⟩

theorem observability_is_not_verification_or_activation
    (receipt : SequentialEpistemicObservabilityEnvelopeReceipt)
    (valid : SequentialEpistemicObservabilityEnvelopeReceiptValid receipt) :
    receipt.verificationCompleted = false ∧
      receipt.verificationDebtOpen = true ∧
      receipt.currentPolicyActivated = false ∧
      receipt.learningDeltaActivated = false := by
  exact ⟨valid.verificationNotCompleted, valid.verificationDebtPreserved,
    valid.policyNotActivated, valid.learningNotActivated⟩

theorem observability_has_no_current_effect
    (receipt : SequentialEpistemicObservabilityEnvelopeReceipt)
    (valid : SequentialEpistemicObservabilityEnvelopeReceiptValid receipt) :
    receipt.persistentWorldStateChanged = false ∧
      receipt.worldModelRevisionIncremented = false ∧
      receipt.currentPlanRevised = false ∧
      receipt.currentPolicyActivated = false ∧
      receipt.learningDeltaActivated = false ∧
      receipt.toolInvocationPerformed = false ∧
      receipt.externalSideEffectPerformed = false := by
  exact ⟨valid.worldNotChanged, valid.revisionNotIncremented,
    valid.planNotRevised, valid.policyNotActivated, valid.learningNotActivated,
    valid.toolNotInvoked, valid.externalEffectNotPerformed⟩

theorem observability_grants_no_authority
    (receipt : SequentialEpistemicObservabilityEnvelopeReceipt)
    (valid : SequentialEpistemicObservabilityEnvelopeReceiptValid receipt) :
    receipt.selectionAuthorityGrantedToObserveOS = false ∧
      receipt.verificationAuthorityGrantedToObserveOS = false ∧
      receipt.worldMutationAuthorityGranted = false ∧
      receipt.policyActivationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false := by
  exact ⟨valid.noSelectionAuthority, valid.noVerificationAuthority,
    valid.noWorldMutationAuthority, valid.noPolicyActivationAuthority,
    valid.noExecutionAuthority⟩

theorem revision_and_lineages_are_preserved
    (receipt : SequentialEpistemicObservabilityEnvelopeReceipt) :
    receipt.resultingWorldRevision = receipt.sourceWorldRevision ∧
      receipt.sourceLineage ⊆ receipt.resultingLineage ∧
      receipt.sourceResponsibility ⊆ receipt.resultingResponsibility := by
  exact ⟨receipt.revisionUnchanged, receipt.lineageMonotone,
    receipt.responsibilityMonotone⟩

end KUOS.ObserveOS.SequentialEpistemicObservabilityEnvelopeV0_7
