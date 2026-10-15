import KUOS.WORLD.KuuOSRepositoryAtomicCheckpointCreationV1_02

namespace KUOS.WORLD.KuuOSRepositoryCheckpointCreationReceiptV1_03

structure CheckpointCreationReceiptWitness where
  v102ResultValid : Prop
  v102ResultBindingExact : Prop
  executionReportBindingExact : Prop
  referenceObservationExact : Prop
  nonceObservationExact : Prop
  repositoryIdentityStable : Prop
  gitDirFingerprintStable : Prop
  observationSequenceOrdered : Prop
  noFutureEvidence : Prop
  noForbiddenExecutionEffect : Prop
  committedReportConsistent : Bool
  abortedReportConsistent : Bool
  committedReceiptConfirmed : Bool
  abortedReceiptConfirmed : Bool
  suppliedExternalReportConsistent : Bool
  externalReportIndependentlyTrusted : Bool
  liveExecutionProven : Bool
  receiptPerformedCheckpointMutation : Bool
  receiptPerformedNonceConsumption : Bool
  receiptInvokedLiveGitCommand : Bool
  receiptMutatedLiveRepository : Bool

structure CheckpointCreationReceiptWitness.ValidCommitted
    (w : CheckpointCreationReceiptWitness) : Prop where
  v102ResultValid : w.v102ResultValid
  v102ResultBindingExact : w.v102ResultBindingExact
  executionReportBindingExact : w.executionReportBindingExact
  referenceObservationExact : w.referenceObservationExact
  nonceObservationExact : w.nonceObservationExact
  repositoryIdentityStable : w.repositoryIdentityStable
  gitDirFingerprintStable : w.gitDirFingerprintStable
  observationSequenceOrdered : w.observationSequenceOrdered
  noFutureEvidence : w.noFutureEvidence
  noForbiddenExecutionEffect : w.noForbiddenExecutionEffect
  committedReportConsistent : w.committedReportConsistent = true
  committedReceiptConfirmed : w.committedReceiptConfirmed = true
  suppliedExternalReportConsistent :
    w.suppliedExternalReportConsistent = true
  externalReportIndependentlyTrusted :
    w.externalReportIndependentlyTrusted = false
  liveExecutionProven : w.liveExecutionProven = false
  receiptPerformedCheckpointMutation :
    w.receiptPerformedCheckpointMutation = false
  receiptPerformedNonceConsumption :
    w.receiptPerformedNonceConsumption = false
  receiptInvokedLiveGitCommand : w.receiptInvokedLiveGitCommand = false
  receiptMutatedLiveRepository : w.receiptMutatedLiveRepository = false

structure CheckpointCreationReceiptWitness.ValidAborted
    (w : CheckpointCreationReceiptWitness) : Prop where
  v102ResultValid : w.v102ResultValid
  v102ResultBindingExact : w.v102ResultBindingExact
  executionReportBindingExact : w.executionReportBindingExact
  referenceObservationExact : w.referenceObservationExact
  nonceObservationExact : w.nonceObservationExact
  repositoryIdentityStable : w.repositoryIdentityStable
  gitDirFingerprintStable : w.gitDirFingerprintStable
  observationSequenceOrdered : w.observationSequenceOrdered
  noFutureEvidence : w.noFutureEvidence
  noForbiddenExecutionEffect : w.noForbiddenExecutionEffect
  abortedReportConsistent : w.abortedReportConsistent = true
  abortedReceiptConfirmed : w.abortedReceiptConfirmed = true
  suppliedExternalReportConsistent :
    w.suppliedExternalReportConsistent = true
  externalReportIndependentlyTrusted :
    w.externalReportIndependentlyTrusted = false
  liveExecutionProven : w.liveExecutionProven = false
  receiptPerformedCheckpointMutation :
    w.receiptPerformedCheckpointMutation = false
  receiptPerformedNonceConsumption :
    w.receiptPerformedNonceConsumption = false
  receiptInvokedLiveGitCommand : w.receiptInvokedLiveGitCommand = false
  receiptMutatedLiveRepository : w.receiptMutatedLiveRepository = false


theorem confirmed_committed_receipt_requires_revalidated_v102_and_exact_evidence
    (w : CheckpointCreationReceiptWitness)
    (h : w.ValidCommitted) :
    w.v102ResultValid ∧
      w.v102ResultBindingExact ∧
      w.executionReportBindingExact ∧
      w.referenceObservationExact ∧
      w.nonceObservationExact ∧
      w.repositoryIdentityStable ∧
      w.gitDirFingerprintStable := by
  exact ⟨h.v102ResultValid, h.v102ResultBindingExact,
    h.executionReportBindingExact, h.referenceObservationExact,
    h.nonceObservationExact, h.repositoryIdentityStable,
    h.gitDirFingerprintStable⟩


theorem confirmed_aborted_receipt_requires_preserved_observations
    (w : CheckpointCreationReceiptWitness)
    (h : w.ValidAborted) :
    w.v102ResultValid ∧
      w.referenceObservationExact ∧
      w.nonceObservationExact ∧
      w.abortedReportConsistent = true ∧
      w.abortedReceiptConfirmed = true := by
  exact ⟨h.v102ResultValid, h.referenceObservationExact,
    h.nonceObservationExact, h.abortedReportConsistent,
    h.abortedReceiptConfirmed⟩


theorem receipt_confirmation_has_bounded_ordered_evidence
    (w : CheckpointCreationReceiptWitness)
    (h : w.ValidCommitted) :
    w.observationSequenceOrdered ∧
      w.noFutureEvidence ∧
      w.noForbiddenExecutionEffect := by
  exact ⟨h.observationSequenceOrdered, h.noFutureEvidence,
    h.noForbiddenExecutionEffect⟩


theorem receipt_does_not_independently_trust_external_report
    (w : CheckpointCreationReceiptWitness)
    (h : w.ValidCommitted) :
    w.externalReportIndependentlyTrusted = false ∧
      w.liveExecutionProven = false := by
  exact ⟨h.externalReportIndependentlyTrusted, h.liveExecutionProven⟩


theorem receipt_verification_performs_no_state_mutation
    (w : CheckpointCreationReceiptWitness)
    (h : w.ValidAborted) :
    w.receiptPerformedCheckpointMutation = false ∧
      w.receiptPerformedNonceConsumption = false ∧
      w.receiptInvokedLiveGitCommand = false ∧
      w.receiptMutatedLiveRepository = false := by
  exact ⟨h.receiptPerformedCheckpointMutation,
    h.receiptPerformedNonceConsumption,
    h.receiptInvokedLiveGitCommand,
    h.receiptMutatedLiveRepository⟩


structure CheckpointCreationReceiptDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_checkpoint_creation_receipt
    {Input Output : Type}
    (derivation : CheckpointCreationReceiptDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointCreationReceiptV1_03
