import KUOS.WORLD.KuuOSRepositoryCheckpointStabilityV1_05

namespace KUOS.WORLD.KuuOSRepositoryCheckpointDiscrepancyReviewV1_06

inductive CheckpointReviewDisposition where
  | clean
  | reviewRequired
  | rejected
  deriving DecidableEq, Repr

inductive CheckpointDiscrepancy where
  | none
  | lost
  | substituted
  | other
  | evidenceInvalid
  deriving DecidableEq, Repr

structure CheckpointReviewWitness where
  stabilityCertificateValid : Prop
  evidenceBindingExact : Prop
  directLocalEvidence : Prop
  observationFresh : Prop
  currentStateRecheckStable : Prop
  targetCommitPresent : Prop
  dispositionMatchesCurrentState : Prop
  disposition : CheckpointReviewDisposition
  discrepancy : CheckpointDiscrepancy
  humanReviewRequired : Bool
  repositoryChangeAuthorityGranted : Bool
  referenceMutationPerformed : Bool
  objectWritePerformed : Bool
  liveGitCommandInvoked : Bool
  liveRepositoryMutated : Bool
  nonceConsumed : Bool

structure CheckpointReviewWitness.ValidClean
    (w : CheckpointReviewWitness) : Prop where
  stabilityCertificateValid : w.stabilityCertificateValid
  evidenceBindingExact : w.evidenceBindingExact
  directLocalEvidence : w.directLocalEvidence
  observationFresh : w.observationFresh
  currentStateRecheckStable : w.currentStateRecheckStable
  targetCommitPresent : w.targetCommitPresent
  dispositionMatchesCurrentState : w.dispositionMatchesCurrentState
  dispositionClean : w.disposition = CheckpointReviewDisposition.clean
  discrepancyNone : w.discrepancy = CheckpointDiscrepancy.none
  humanReviewRequired : w.humanReviewRequired = false
  repositoryChangeAuthorityGranted : w.repositoryChangeAuthorityGranted = false
  referenceMutationPerformed : w.referenceMutationPerformed = false
  objectWritePerformed : w.objectWritePerformed = false
  liveGitCommandInvoked : w.liveGitCommandInvoked = false
  liveRepositoryMutated : w.liveRepositoryMutated = false
  nonceConsumed : w.nonceConsumed = false

structure CheckpointReviewWitness.ValidReviewRequired
    (w : CheckpointReviewWitness) : Prop where
  stabilityCertificateValid : w.stabilityCertificateValid
  evidenceBindingExact : w.evidenceBindingExact
  directLocalEvidence : w.directLocalEvidence
  observationFresh : w.observationFresh
  currentStateRecheckStable : w.currentStateRecheckStable
  targetCommitPresent : w.targetCommitPresent
  dispositionMatchesCurrentState : w.dispositionMatchesCurrentState
  dispositionReviewRequired :
    w.disposition = CheckpointReviewDisposition.reviewRequired
  discrepancyEligible :
    w.discrepancy = CheckpointDiscrepancy.lost ∨
      w.discrepancy = CheckpointDiscrepancy.substituted
  humanReviewRequired : w.humanReviewRequired = true
  repositoryChangeAuthorityGranted : w.repositoryChangeAuthorityGranted = false
  referenceMutationPerformed : w.referenceMutationPerformed = false
  objectWritePerformed : w.objectWritePerformed = false
  liveGitCommandInvoked : w.liveGitCommandInvoked = false
  liveRepositoryMutated : w.liveRepositoryMutated = false
  nonceConsumed : w.nonceConsumed = false

structure CheckpointReviewWitness.ValidRejected
    (w : CheckpointReviewWitness) : Prop where
  dispositionRejected : w.disposition = CheckpointReviewDisposition.rejected
  humanReviewRequired : w.humanReviewRequired = false
  repositoryChangeAuthorityGranted : w.repositoryChangeAuthorityGranted = false
  referenceMutationPerformed : w.referenceMutationPerformed = false
  objectWritePerformed : w.objectWritePerformed = false
  liveGitCommandInvoked : w.liveGitCommandInvoked = false
  liveRepositoryMutated : w.liveRepositoryMutated = false
  nonceConsumed : w.nonceConsumed = false


theorem clean_checkpoint_requires_no_human_review
    (w : CheckpointReviewWitness)
    (h : w.ValidClean) :
    w.discrepancy = CheckpointDiscrepancy.none ∧
      w.humanReviewRequired = false := by
  exact ⟨h.discrepancyNone, h.humanReviewRequired⟩


theorem human_review_is_limited_to_confirmed_loss_or_substitution
    (w : CheckpointReviewWitness)
    (h : w.ValidReviewRequired) :
    (w.discrepancy = CheckpointDiscrepancy.lost ∨
      w.discrepancy = CheckpointDiscrepancy.substituted) ∧
      w.humanReviewRequired = true := by
  exact ⟨h.discrepancyEligible, h.humanReviewRequired⟩


theorem rejected_evidence_does_not_request_human_review
    (w : CheckpointReviewWitness)
    (h : w.ValidRejected) :
    w.disposition = CheckpointReviewDisposition.rejected ∧
      w.humanReviewRequired = false := by
  exact ⟨h.dispositionRejected, h.humanReviewRequired⟩


theorem review_record_grants_no_repository_change_authority
    (w : CheckpointReviewWitness)
    (h : w.ValidReviewRequired) :
    w.repositoryChangeAuthorityGranted = false ∧
      w.referenceMutationPerformed = false ∧
      w.objectWritePerformed = false ∧
      w.liveGitCommandInvoked = false ∧
      w.liveRepositoryMutated = false ∧
      w.nonceConsumed = false := by
  exact ⟨h.repositoryChangeAuthorityGranted, h.referenceMutationPerformed,
    h.objectWritePerformed, h.liveGitCommandInvoked,
    h.liveRepositoryMutated, h.nonceConsumed⟩


structure CheckpointReviewDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_checkpoint_review_record
    {Input Output : Type}
    (derivation : CheckpointReviewDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointDiscrepancyReviewV1_06
