import Mathlib
import KUOS.VerifyOS.IndependentEvidenceVerificationV0_14

namespace KUOS.VerifyOS.OutcomeDispositionHandoffV0_15

open KUOS.VerifyOS.IndependentEvidenceVerificationV0_14

inductive OutcomeDispositionCandidate where
  | adopt
  | reject
  | defer
  | reobserve
  deriving DecidableEq, Repr

inductive OutcomeDispositionHandoffDisposition where
  | adoptCandidatePrepared
  | rejectCandidatePrepared
  | deferCandidatePrepared
  | reobservationCandidatePrepared
  | sourceVerificationReceiptRepairRequired
  | verificationOutcomeCorrespondenceRepairRequired
  | dispositionAuthorityReviewRepairRequired
  | evidencePreservationRepairRequired
  | appealRouteRepairRequired
  | verificationDebtPreservationRepairRequired
  | dispositionWindowRepairRequired
  | dispositionReplayConflictRejected
  | currentStateMutationRejected
  | authorityEscalationRejected
  deriving DecidableEq, Repr

inductive OutcomeDispositionHandoffState where
  | independentEvidenceVerificationReceiptRecorded
  | independentEvidenceVerificationReceiptRecordedDispositionHandoffPrepared
  deriving DecidableEq, Repr

structure OutcomeDispositionHandoffReceipt where
  sourceReceipt : IndependentEvidenceVerificationReceipt
  sourceVerificationReceiptDigest : String
  outcomeDispositionRequestDigest : String
  outcomeDispositionReviewDigest : String
  outcomeDispositionContextDigest : String
  dispositionPolicyDigest : String
  verifyOSResponsibilityDigest : String
  dispositionHandoffId : String
  dispositionBundleDigest : String
  requesterId : String
  reviewerId : String
  sourceWorldRevision : Nat
  resultingWorldRevision : Nat
  handoffDisposition : OutcomeDispositionHandoffDisposition
  sourceVerificationOutcome : Option IndependentEvidenceVerificationOutcome
  outcomeDispositionCandidate : Option OutcomeDispositionCandidate
  handoffStateBefore : OutcomeDispositionHandoffState
  handoffStateAfter : OutcomeDispositionHandoffState
  outcomeDispositionHandoffPrepared : Bool
  worldDispositionCandidateGenerated : Bool
  adoptCandidateGenerated : Bool
  rejectCandidateGenerated : Bool
  deferCandidateGenerated : Bool
  reobservationCandidateGenerated : Bool
  governanceReviewRequired : Bool
  freshWorldAuthorizationRequired : Bool
  appealReviewRequired : Bool
  evidencePreserved : Bool
  verificationDebtOpen : Bool
  reobservationRequired : Bool
  worldDispositionCompleted : Bool
  worldCommitReady : Bool
  persistentWorldStateChangedByHandoff : Bool
  worldModelRevisionIncrementedByHandoff : Bool
  currentPlanRevisedByHandoff : Bool
  currentPolicyActivatedByHandoff : Bool
  learningDeltaActivatedByHandoff : Bool
  observationRecollectionPerformedByKernel : Bool
  toolInvocationPerformedByKernel : Bool
  externalSideEffectPerformedByKernel : Bool
  generalizedTruthClaimed : Bool
  causalAttributionClaimed : Bool
  worldAdoptionAuthorityGranted : Bool
  worldRejectionAuthorityGranted : Bool
  worldMutationAuthorityGranted : Bool
  policyActivationAuthorityGranted : Bool
  executionAuthorityGranted : Bool
  observationExecutionAuthorityGranted : Bool
  historyReadOnly : Bool
  futureOnly : Bool
  activeNow : Bool
  sourceLineage : Finset String
  resultingLineage : Finset String
  sourceResponsibility : Finset String
  resultingResponsibility : Finset String
  sourceOutcomeBound : sourceVerificationOutcome = sourceReceipt.verificationOutcome
  sourceAccepted :
    sourceReceipt.verificationReceiptRecorded = true ∧
      sourceReceipt.independentEvidenceVerificationExecuted = true ∧
      sourceReceipt.verificationCompleted = true ∧
      ((sourceReceipt.verificationDisposition = .verificationPassed ∧
          sourceReceipt.verificationOutcome = some .passed) ∨
        (sourceReceipt.verificationDisposition = .verificationFailed ∧
          sourceReceipt.verificationOutcome = some .failed) ∨
        (sourceReceipt.verificationDisposition = .verificationIndeterminate ∧
          sourceReceipt.verificationOutcome = some .indeterminate))
  adoptResult :
    handoffDisposition = .adoptCandidatePrepared →
      sourceVerificationOutcome = some .passed ∧
        outcomeDispositionCandidate = some .adopt ∧
        handoffStateBefore = .independentEvidenceVerificationReceiptRecorded ∧
        handoffStateAfter =
          .independentEvidenceVerificationReceiptRecordedDispositionHandoffPrepared ∧
        outcomeDispositionHandoffPrepared = true ∧
        worldDispositionCandidateGenerated = true ∧
        adoptCandidateGenerated = true ∧
        governanceReviewRequired = true ∧
        freshWorldAuthorizationRequired = true ∧
        verificationDebtOpen = false ∧
        reobservationRequired = false ∧
        worldDispositionCompleted = false ∧
        worldCommitReady = false
  rejectResult :
    handoffDisposition = .rejectCandidatePrepared →
      sourceVerificationOutcome = some .failed ∧
        outcomeDispositionCandidate = some .reject ∧
        handoffStateBefore = .independentEvidenceVerificationReceiptRecorded ∧
        handoffStateAfter =
          .independentEvidenceVerificationReceiptRecordedDispositionHandoffPrepared ∧
        outcomeDispositionHandoffPrepared = true ∧
        worldDispositionCandidateGenerated = true ∧
        rejectCandidateGenerated = true ∧
        governanceReviewRequired = true ∧
        freshWorldAuthorizationRequired = true ∧
        appealReviewRequired = true ∧
        evidencePreserved = true ∧
        verificationDebtOpen = false ∧
        reobservationRequired = false ∧
        worldDispositionCompleted = false ∧
        worldCommitReady = false
  deferResult :
    handoffDisposition = .deferCandidatePrepared →
      sourceVerificationOutcome = some .indeterminate ∧
        outcomeDispositionCandidate = some .defer ∧
        handoffStateBefore = .independentEvidenceVerificationReceiptRecorded ∧
        handoffStateAfter =
          .independentEvidenceVerificationReceiptRecordedDispositionHandoffPrepared ∧
        outcomeDispositionHandoffPrepared = true ∧
        worldDispositionCandidateGenerated = true ∧
        deferCandidateGenerated = true ∧
        governanceReviewRequired = true ∧
        freshWorldAuthorizationRequired = true ∧
        verificationDebtOpen = true ∧
        reobservationRequired = true ∧
        worldDispositionCompleted = false ∧
        worldCommitReady = false
  reobservationResult :
    handoffDisposition = .reobservationCandidatePrepared →
      sourceVerificationOutcome = some .indeterminate ∧
        outcomeDispositionCandidate = some .reobserve ∧
        handoffStateBefore = .independentEvidenceVerificationReceiptRecorded ∧
        handoffStateAfter =
          .independentEvidenceVerificationReceiptRecordedDispositionHandoffPrepared ∧
        outcomeDispositionHandoffPrepared = true ∧
        worldDispositionCandidateGenerated = true ∧
        reobservationCandidateGenerated = true ∧
        governanceReviewRequired = true ∧
        freshWorldAuthorizationRequired = true ∧
        verificationDebtOpen = true ∧
        reobservationRequired = true ∧
        worldDispositionCompleted = false ∧
        worldCommitReady = false
  routedResult :
    handoffDisposition ≠ .adoptCandidatePrepared →
      handoffDisposition ≠ .rejectCandidatePrepared →
        handoffDisposition ≠ .deferCandidatePrepared →
          handoffDisposition ≠ .reobservationCandidatePrepared →
            outcomeDispositionCandidate = none ∧
              handoffStateBefore = .independentEvidenceVerificationReceiptRecorded ∧
              handoffStateAfter = .independentEvidenceVerificationReceiptRecorded ∧
              outcomeDispositionHandoffPrepared = false ∧
              worldDispositionCandidateGenerated = false ∧
              worldDispositionCompleted = false ∧
              worldCommitReady = false
  debtPreserved : verificationDebtOpen = sourceReceipt.verificationDebtOpen
  reobservationPreserved : reobservationRequired = sourceReceipt.reobservationRequired
  revisionUnchanged : resultingWorldRevision = sourceWorldRevision
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility

structure OutcomeDispositionHandoffReceiptValid
    (receipt : OutcomeDispositionHandoffReceipt) : Prop where
  worldNotChanged : receipt.persistentWorldStateChangedByHandoff = false
  revisionNotIncremented :
    receipt.worldModelRevisionIncrementedByHandoff = false
  planNotRevised : receipt.currentPlanRevisedByHandoff = false
  policyNotActivated : receipt.currentPolicyActivatedByHandoff = false
  learningNotActivated : receipt.learningDeltaActivatedByHandoff = false
  observationNotRecollected :
    receipt.observationRecollectionPerformedByKernel = false
  toolNotInvoked : receipt.toolInvocationPerformedByKernel = false
  externalEffectNotPerformed :
    receipt.externalSideEffectPerformedByKernel = false
  noGeneralizedTruth : receipt.generalizedTruthClaimed = false
  noCausalAttribution : receipt.causalAttributionClaimed = false
  noWorldAdoptionAuthority : receipt.worldAdoptionAuthorityGranted = false
  noWorldRejectionAuthority : receipt.worldRejectionAuthorityGranted = false
  noWorldMutationAuthority : receipt.worldMutationAuthorityGranted = false
  noPolicyActivationAuthority :
    receipt.policyActivationAuthorityGranted = false
  noExecutionAuthority : receipt.executionAuthorityGranted = false
  noObservationExecutionAuthority :
    receipt.observationExecutionAuthorityGranted = false
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

theorem passed_maps_to_adopt_candidate_not_world_adoption
    (receipt : OutcomeDispositionHandoffReceipt)
    (h : receipt.handoffDisposition = .adoptCandidatePrepared) :
    receipt.sourceVerificationOutcome = some .passed ∧
      receipt.outcomeDispositionCandidate = some .adopt ∧
      receipt.worldDispositionCandidateGenerated = true ∧
      receipt.worldDispositionCompleted = false ∧
      receipt.worldCommitReady = false := by
  rcases receipt.adoptResult h with
    ⟨ho, hc, _, _, _, hg, _, _, _, _, _, hd, hw⟩
  exact ⟨ho, hc, hg, hd, hw⟩

theorem failed_maps_to_reject_candidate_with_evidence_and_appeal
    (receipt : OutcomeDispositionHandoffReceipt)
    (h : receipt.handoffDisposition = .rejectCandidatePrepared) :
    receipt.sourceVerificationOutcome = some .failed ∧
      receipt.outcomeDispositionCandidate = some .reject ∧
      receipt.appealReviewRequired = true ∧
      receipt.evidencePreserved = true ∧
      receipt.worldDispositionCompleted = false := by
  rcases receipt.rejectResult h with
    ⟨ho, hc, _, _, _, _, _, _, _, ha, he, _, _, hd, _⟩
  exact ⟨ho, hc, ha, he, hd⟩

theorem indeterminate_maps_to_defer_or_reobserve_with_open_debt
    (receipt : OutcomeDispositionHandoffReceipt)
    (h : receipt.handoffDisposition = .deferCandidatePrepared ∨
      receipt.handoffDisposition = .reobservationCandidatePrepared) :
    receipt.sourceVerificationOutcome = some .indeterminate ∧
      (receipt.outcomeDispositionCandidate = some .defer ∨
        receipt.outcomeDispositionCandidate = some .reobserve) ∧
      receipt.verificationDebtOpen = true ∧
      receipt.reobservationRequired = true ∧
      receipt.worldDispositionCompleted = false := by
  rcases h with hd | hr
  · rcases receipt.deferResult hd with
      ⟨ho, hc, _, _, _, _, _, _, _, hv, hrq, hw, _⟩
    exact ⟨ho, Or.inl hc, hv, hrq, hw⟩
  · rcases receipt.reobservationResult hr with
      ⟨ho, hc, _, _, _, _, _, _, _, hv, hrq, hw, _⟩
    exact ⟨ho, Or.inr hc, hv, hrq, hw⟩

theorem disposition_handoff_has_no_current_effect
    (receipt : OutcomeDispositionHandoffReceipt)
    (valid : OutcomeDispositionHandoffReceiptValid receipt) :
    receipt.persistentWorldStateChangedByHandoff = false ∧
      receipt.worldModelRevisionIncrementedByHandoff = false ∧
      receipt.currentPlanRevisedByHandoff = false ∧
      receipt.currentPolicyActivatedByHandoff = false ∧
      receipt.learningDeltaActivatedByHandoff = false ∧
      receipt.observationRecollectionPerformedByKernel = false ∧
      receipt.toolInvocationPerformedByKernel = false ∧
      receipt.externalSideEffectPerformedByKernel = false := by
  exact ⟨valid.worldNotChanged, valid.revisionNotIncremented,
    valid.planNotRevised, valid.policyNotActivated, valid.learningNotActivated,
    valid.observationNotRecollected, valid.toolNotInvoked,
    valid.externalEffectNotPerformed⟩

theorem disposition_handoff_grants_no_authority
    (receipt : OutcomeDispositionHandoffReceipt)
    (valid : OutcomeDispositionHandoffReceiptValid receipt) :
    receipt.worldAdoptionAuthorityGranted = false ∧
      receipt.worldRejectionAuthorityGranted = false ∧
      receipt.worldMutationAuthorityGranted = false ∧
      receipt.policyActivationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false ∧
      receipt.observationExecutionAuthorityGranted = false := by
  exact ⟨valid.noWorldAdoptionAuthority, valid.noWorldRejectionAuthority,
    valid.noWorldMutationAuthority, valid.noPolicyActivationAuthority,
    valid.noExecutionAuthority, valid.noObservationExecutionAuthority⟩

theorem disposition_handoff_does_not_claim_truth_or_causality
    (receipt : OutcomeDispositionHandoffReceipt)
    (valid : OutcomeDispositionHandoffReceiptValid receipt) :
    receipt.generalizedTruthClaimed = false ∧
      receipt.causalAttributionClaimed = false := by
  exact ⟨valid.noGeneralizedTruth, valid.noCausalAttribution⟩

theorem debt_and_reobservation_are_preserved
    (receipt : OutcomeDispositionHandoffReceipt) :
    receipt.verificationDebtOpen = receipt.sourceReceipt.verificationDebtOpen ∧
      receipt.reobservationRequired = receipt.sourceReceipt.reobservationRequired := by
  exact ⟨receipt.debtPreserved, receipt.reobservationPreserved⟩

theorem revision_and_lineages_are_preserved
    (receipt : OutcomeDispositionHandoffReceipt) :
    receipt.resultingWorldRevision = receipt.sourceWorldRevision ∧
      receipt.sourceLineage ⊆ receipt.resultingLineage ∧
      receipt.sourceResponsibility ⊆ receipt.resultingResponsibility := by
  exact ⟨receipt.revisionUnchanged, receipt.lineageMonotone,
    receipt.responsibilityMonotone⟩

end KUOS.VerifyOS.OutcomeDispositionHandoffV0_15
