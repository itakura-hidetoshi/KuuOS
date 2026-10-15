import Mathlib
import KUOS.VerifyOS.SequentialEpistemicObservationVerificationHandoffV0_13

namespace KUOS.VerifyOS.IndependentEvidenceVerificationV0_14

open KUOS.VerifyOS.SequentialEpistemicObservationVerificationHandoffV0_13

inductive IndependentEvidenceVerificationOutcome where
  | passed
  | failed
  | indeterminate
  deriving DecidableEq, Repr

inductive IndependentEvidenceVerificationDisposition where
  | verificationPassed
  | verificationFailed
  | verificationIndeterminate
  | sourceVerificationHandoffRepairRequired
  | verificationCorrespondenceRepairRequired
  | verifierIndependenceRepairRequired
  | independentEvidenceIntegrityRepairRequired
  | verificationProtocolExecutionRepairRequired
  | reproductionExecutionRepairRequired
  | acceptanceAdjudicationRepairRequired
  | verificationResultReviewRepairRequired
  | verificationReplayConflictRejected
  | currentStateMutationRejected
  | authorityEscalationRejected
  deriving DecidableEq, Repr

inductive IndependentEvidenceVerificationState where
  | independentVerificationHandoffPrepared
  | independentVerificationHandoffPreparedVerificationReceiptRecorded
  deriving DecidableEq, Repr

structure IndependentEvidenceVerificationReceipt where
  sourceReceipt : SequentialEpistemicObservationVerificationHandoffReceipt
  sourceVerificationHandoffReceiptDigest : String
  independentEvidenceBundleDigest : String
  independentVerificationExecutionDigest : String
  independentVerificationResultReviewDigest : String
  independentVerificationContextDigest : String
  verificationPolicyDigest : String
  verifyOSResponsibilityDigest : String
  verificationId : String
  verificationBundleDigest : String
  verifierId : String
  reviewerId : String
  sourceWorldRevision : Nat
  resultingWorldRevision : Nat
  verificationDisposition : IndependentEvidenceVerificationDisposition
  verificationOutcome : Option IndependentEvidenceVerificationOutcome
  verificationStateBefore : IndependentEvidenceVerificationState
  verificationStateAfter : IndependentEvidenceVerificationState
  sourceVerificationHandoffPrepared : Bool
  independentEvidenceBundleBound : Bool
  verificationProtocolExecuted : Bool
  reproductionPlanExecuted : Bool
  falsificationChallengeExecuted : Bool
  verificationResultReviewed : Bool
  verificationReceiptRecorded : Bool
  independentEvidenceVerificationExecuted : Bool
  verificationCompleted : Bool
  verificationDebtOpen : Bool
  reobservationRequired : Bool
  worldDispositionCandidateGenerated : Bool
  persistentWorldStateChangedByVerification : Bool
  worldModelRevisionIncrementedByVerification : Bool
  currentPlanRevisedByVerification : Bool
  currentPolicyActivatedByVerification : Bool
  learningDeltaActivatedByVerification : Bool
  toolInvocationPerformedByKernel : Bool
  externalSideEffectPerformedByKernel : Bool
  generalizedTruthClaimed : Bool
  causalAttributionClaimed : Bool
  worldAdoptionAuthorityGranted : Bool
  worldRejectionAuthorityGranted : Bool
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
  sourceAccepted :
    sourceReceipt.handoffDisposition =
        .independentVerificationHandoffSupported ∧
      sourceReceipt.handoffStateAfter =
        .observabilityEnvelopeRecordedIndependentVerificationHandoffPrepared ∧
      sourceReceipt.verificationRequestRecorded = true ∧
      sourceReceipt.independentVerificationHandoffPrepared = true ∧
      sourceReceipt.verificationCompleted = false ∧
      sourceReceipt.verificationDebtOpen = true
  passedResult :
    verificationDisposition = .verificationPassed →
      verificationOutcome = some .passed ∧
        verificationStateBefore = .independentVerificationHandoffPrepared ∧
        verificationStateAfter =
          .independentVerificationHandoffPreparedVerificationReceiptRecorded ∧
        independentEvidenceBundleBound = true ∧
        verificationProtocolExecuted = true ∧
        reproductionPlanExecuted = true ∧
        falsificationChallengeExecuted = true ∧
        verificationResultReviewed = true ∧
        verificationReceiptRecorded = true ∧
        independentEvidenceVerificationExecuted = true ∧
        verificationCompleted = true ∧
        verificationDebtOpen = false ∧
        reobservationRequired = false
  failedResult :
    verificationDisposition = .verificationFailed →
      verificationOutcome = some .failed ∧
        verificationStateBefore = .independentVerificationHandoffPrepared ∧
        verificationStateAfter =
          .independentVerificationHandoffPreparedVerificationReceiptRecorded ∧
        independentEvidenceBundleBound = true ∧
        verificationProtocolExecuted = true ∧
        reproductionPlanExecuted = true ∧
        falsificationChallengeExecuted = true ∧
        verificationResultReviewed = true ∧
        verificationReceiptRecorded = true ∧
        independentEvidenceVerificationExecuted = true ∧
        verificationCompleted = true ∧
        verificationDebtOpen = false ∧
        reobservationRequired = false
  indeterminateResult :
    verificationDisposition = .verificationIndeterminate →
      verificationOutcome = some .indeterminate ∧
        verificationStateBefore = .independentVerificationHandoffPrepared ∧
        verificationStateAfter =
          .independentVerificationHandoffPreparedVerificationReceiptRecorded ∧
        independentEvidenceBundleBound = true ∧
        verificationProtocolExecuted = true ∧
        reproductionPlanExecuted = true ∧
        falsificationChallengeExecuted = true ∧
        verificationResultReviewed = true ∧
        verificationReceiptRecorded = true ∧
        independentEvidenceVerificationExecuted = true ∧
        verificationCompleted = true ∧
        verificationDebtOpen = true ∧
        reobservationRequired = true
  routedResult :
    verificationDisposition ≠ .verificationPassed →
      verificationDisposition ≠ .verificationFailed →
        verificationDisposition ≠ .verificationIndeterminate →
          verificationOutcome = none ∧
            verificationStateBefore = .independentVerificationHandoffPrepared ∧
            verificationStateAfter = .independentVerificationHandoffPrepared ∧
            verificationReceiptRecorded = false ∧
            independentEvidenceVerificationExecuted = false ∧
            verificationCompleted = false ∧
            verificationDebtOpen = true ∧
            reobservationRequired = false
  revisionUnchanged : resultingWorldRevision = sourceWorldRevision
  lineageMonotone : sourceLineage ⊆ resultingLineage
  responsibilityMonotone : sourceResponsibility ⊆ resultingResponsibility

structure IndependentEvidenceVerificationReceiptValid
    (receipt : IndependentEvidenceVerificationReceipt) : Prop where
  noWorldDispositionCandidate :
    receipt.worldDispositionCandidateGenerated = false
  worldNotChanged :
    receipt.persistentWorldStateChangedByVerification = false
  revisionNotIncremented :
    receipt.worldModelRevisionIncrementedByVerification = false
  planNotRevised : receipt.currentPlanRevisedByVerification = false
  policyNotActivated : receipt.currentPolicyActivatedByVerification = false
  learningNotActivated : receipt.learningDeltaActivatedByVerification = false
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
  historyReadOnly : receipt.historyReadOnly = true
  futureOnly : receipt.futureOnly = true
  inactiveNow : receipt.activeNow = false

theorem passed_verification_closes_debt
    (receipt : IndependentEvidenceVerificationReceipt)
    (h : receipt.verificationDisposition = .verificationPassed) :
    receipt.verificationOutcome = some .passed ∧
      receipt.verificationCompleted = true ∧
      receipt.verificationDebtOpen = false ∧
      receipt.reobservationRequired = false := by
  rcases receipt.passedResult h with
    ⟨ho, _, _, _, _, _, _, _, _, _, hc, hd, hr⟩
  exact ⟨ho, hc, hd, hr⟩

theorem failed_verification_closes_debt
    (receipt : IndependentEvidenceVerificationReceipt)
    (h : receipt.verificationDisposition = .verificationFailed) :
    receipt.verificationOutcome = some .failed ∧
      receipt.verificationCompleted = true ∧
      receipt.verificationDebtOpen = false ∧
      receipt.reobservationRequired = false := by
  rcases receipt.failedResult h with
    ⟨ho, _, _, _, _, _, _, _, _, _, hc, hd, hr⟩
  exact ⟨ho, hc, hd, hr⟩

theorem indeterminate_verification_preserves_debt
    (receipt : IndependentEvidenceVerificationReceipt)
    (h : receipt.verificationDisposition = .verificationIndeterminate) :
    receipt.verificationOutcome = some .indeterminate ∧
      receipt.verificationCompleted = true ∧
      receipt.verificationDebtOpen = true ∧
      receipt.reobservationRequired = true := by
  rcases receipt.indeterminateResult h with
    ⟨ho, _, _, _, _, _, _, _, _, _, hc, hd, hr⟩
  exact ⟨ho, hc, hd, hr⟩

theorem verification_has_no_current_effect
    (receipt : IndependentEvidenceVerificationReceipt)
    (valid : IndependentEvidenceVerificationReceiptValid receipt) :
    receipt.worldDispositionCandidateGenerated = false ∧
      receipt.persistentWorldStateChangedByVerification = false ∧
      receipt.worldModelRevisionIncrementedByVerification = false ∧
      receipt.currentPlanRevisedByVerification = false ∧
      receipt.currentPolicyActivatedByVerification = false ∧
      receipt.learningDeltaActivatedByVerification = false ∧
      receipt.toolInvocationPerformedByKernel = false ∧
      receipt.externalSideEffectPerformedByKernel = false := by
  exact ⟨valid.noWorldDispositionCandidate, valid.worldNotChanged,
    valid.revisionNotIncremented, valid.planNotRevised,
    valid.policyNotActivated, valid.learningNotActivated,
    valid.toolNotInvoked, valid.externalEffectNotPerformed⟩

theorem verification_grants_no_authority
    (receipt : IndependentEvidenceVerificationReceipt)
    (valid : IndependentEvidenceVerificationReceiptValid receipt) :
    receipt.worldAdoptionAuthorityGranted = false ∧
      receipt.worldRejectionAuthorityGranted = false ∧
      receipt.worldMutationAuthorityGranted = false ∧
      receipt.policyActivationAuthorityGranted = false ∧
      receipt.executionAuthorityGranted = false := by
  exact ⟨valid.noWorldAdoptionAuthority, valid.noWorldRejectionAuthority,
    valid.noWorldMutationAuthority, valid.noPolicyActivationAuthority,
    valid.noExecutionAuthority⟩

theorem verification_does_not_claim_truth_or_causality
    (receipt : IndependentEvidenceVerificationReceipt)
    (valid : IndependentEvidenceVerificationReceiptValid receipt) :
    receipt.generalizedTruthClaimed = false ∧
      receipt.causalAttributionClaimed = false := by
  exact ⟨valid.noGeneralizedTruth, valid.noCausalAttribution⟩

theorem revision_and_lineages_are_preserved
    (receipt : IndependentEvidenceVerificationReceipt) :
    receipt.resultingWorldRevision = receipt.sourceWorldRevision ∧
      receipt.sourceLineage ⊆ receipt.resultingLineage ∧
      receipt.sourceResponsibility ⊆ receipt.resultingResponsibility := by
  exact ⟨receipt.revisionUnchanged, receipt.lineageMonotone,
    receipt.responsibilityMonotone⟩

end KUOS.VerifyOS.IndependentEvidenceVerificationV0_14
