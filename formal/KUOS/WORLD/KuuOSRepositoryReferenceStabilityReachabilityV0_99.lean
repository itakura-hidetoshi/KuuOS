import KUOS.WORLD.KuuOSRepositoryReferenceUpdateReceiptV0_98

namespace KUOS.WORLD.KuuOSRepositoryReferenceStabilityReachabilityV0_99

structure ReferenceStabilityWitness where
  referenceUpdateReceiptValid : Prop
  referenceUpdateReceiptCommitted : Prop
  repositoryBound : Prop
  referenceBound : Prop
  candidateCommitBound : Prop
  transactionBound : Prop
  delayedObservationBound : Prop
  stabilityIntervalBounded : Prop
  directLocalBranch : Prop
  objectDatabaseReachabilityBound : Prop
  reachabilityPathComplete : Prop
  reachabilityDepthBounded : Prop
  candidateCommitPresent : Prop
  delayedTipPresent : Prop
  candidateReachableFromDelayedTip : Prop
  candidateIsDelayedTip : Bool
  delayedTipAdvanced : Bool
  workingTreeEvidenceUsed : Bool
  reflogEvidenceUsed : Bool
  remoteEvidenceUsed : Bool
  certificateCommitted : Bool
  forceUpdateAuthorized : Bool
  referenceDeleteAuthorized : Bool
  pushAuthorized : Bool
  referenceMutationPerformed : Bool
  objectDatabaseWritePerformed : Bool
  workingTreeWritePerformed : Bool
  indexWritePerformed : Bool
  reflogWritePerformed : Bool
  remoteReferenceUpdated : Bool
  pushPerformed : Bool
  signingPerformed : Bool

structure ReferenceStabilityWitness.ValidCommitted
    (w : ReferenceStabilityWitness) : Prop where
  referenceUpdateReceiptValid : w.referenceUpdateReceiptValid
  referenceUpdateReceiptCommitted : w.referenceUpdateReceiptCommitted
  repositoryBound : w.repositoryBound
  referenceBound : w.referenceBound
  candidateCommitBound : w.candidateCommitBound
  transactionBound : w.transactionBound
  delayedObservationBound : w.delayedObservationBound
  stabilityIntervalBounded : w.stabilityIntervalBounded
  directLocalBranch : w.directLocalBranch
  objectDatabaseReachabilityBound : w.objectDatabaseReachabilityBound
  reachabilityPathComplete : w.reachabilityPathComplete
  reachabilityDepthBounded : w.reachabilityDepthBounded
  candidateCommitPresent : w.candidateCommitPresent
  delayedTipPresent : w.delayedTipPresent
  candidateReachableFromDelayedTip : w.candidateReachableFromDelayedTip
  tipRelation :
    w.candidateIsDelayedTip = true ∨ w.delayedTipAdvanced = true
  workingTreeEvidenceUsed : w.workingTreeEvidenceUsed = false
  reflogEvidenceUsed : w.reflogEvidenceUsed = false
  remoteEvidenceUsed : w.remoteEvidenceUsed = false
  certificateCommitted : w.certificateCommitted = true
  forceUpdateAuthorized : w.forceUpdateAuthorized = false
  referenceDeleteAuthorized : w.referenceDeleteAuthorized = false
  pushAuthorized : w.pushAuthorized = false
  referenceMutationPerformed : w.referenceMutationPerformed = false
  objectDatabaseWritePerformed : w.objectDatabaseWritePerformed = false
  workingTreeWritePerformed : w.workingTreeWritePerformed = false
  indexWritePerformed : w.indexWritePerformed = false
  reflogWritePerformed : w.reflogWritePerformed = false
  remoteReferenceUpdated : w.remoteReferenceUpdated = false
  pushPerformed : w.pushPerformed = false
  signingPerformed : w.signingPerformed = false


theorem valid_stability_certificate_binds_receipt_repository_and_reference
    (w : ReferenceStabilityWitness)
    (h : w.ValidCommitted) :
    w.referenceUpdateReceiptValid ∧ w.referenceUpdateReceiptCommitted ∧
      w.repositoryBound ∧ w.referenceBound ∧
      w.candidateCommitBound ∧ w.transactionBound := by
  exact ⟨h.referenceUpdateReceiptValid, h.referenceUpdateReceiptCommitted,
    h.repositoryBound, h.referenceBound, h.candidateCommitBound,
    h.transactionBound⟩


theorem valid_stability_certificate_uses_bounded_delayed_evidence
    (w : ReferenceStabilityWitness)
    (h : w.ValidCommitted) :
    w.delayedObservationBound ∧ w.stabilityIntervalBounded ∧
      w.directLocalBranch ∧ w.objectDatabaseReachabilityBound ∧
      w.reachabilityPathComplete ∧ w.reachabilityDepthBounded := by
  exact ⟨h.delayedObservationBound, h.stabilityIntervalBounded,
    h.directLocalBranch, h.objectDatabaseReachabilityBound,
    h.reachabilityPathComplete, h.reachabilityDepthBounded⟩


theorem valid_stability_certificate_preserves_candidate_reachability
    (w : ReferenceStabilityWitness)
    (h : w.ValidCommitted) :
    w.candidateCommitPresent ∧ w.delayedTipPresent ∧
      w.candidateReachableFromDelayedTip := by
  exact ⟨h.candidateCommitPresent, h.delayedTipPresent,
    h.candidateReachableFromDelayedTip⟩


theorem valid_stability_certificate_accepts_exact_or_advanced_tip
    (w : ReferenceStabilityWitness)
    (h : w.ValidCommitted) :
    w.candidateIsDelayedTip = true ∨ w.delayedTipAdvanced = true := by
  exact h.tipRelation


theorem valid_stability_certificate_uses_no_worktree_reflog_or_remote_evidence
    (w : ReferenceStabilityWitness)
    (h : w.ValidCommitted) :
    w.workingTreeEvidenceUsed = false ∧
      w.reflogEvidenceUsed = false ∧
      w.remoteEvidenceUsed = false := by
  exact ⟨h.workingTreeEvidenceUsed, h.reflogEvidenceUsed,
    h.remoteEvidenceUsed⟩


theorem valid_stability_certificate_grants_no_mutation_authority
    (w : ReferenceStabilityWitness)
    (h : w.ValidCommitted) :
    w.forceUpdateAuthorized = false ∧
      w.referenceDeleteAuthorized = false ∧
      w.pushAuthorized = false := by
  exact ⟨h.forceUpdateAuthorized, h.referenceDeleteAuthorized,
    h.pushAuthorized⟩


theorem stability_certificate_performs_no_repository_effect
    (w : ReferenceStabilityWitness)
    (h : w.ValidCommitted) :
    w.referenceMutationPerformed = false ∧
      w.objectDatabaseWritePerformed = false ∧
      w.workingTreeWritePerformed = false ∧
      w.indexWritePerformed = false ∧
      w.reflogWritePerformed = false ∧
      w.remoteReferenceUpdated = false ∧
      w.pushPerformed = false ∧ w.signingPerformed = false := by
  exact ⟨h.referenceMutationPerformed, h.objectDatabaseWritePerformed,
    h.workingTreeWritePerformed, h.indexWritePerformed,
    h.reflogWritePerformed, h.remoteReferenceUpdated,
    h.pushPerformed, h.signingPerformed⟩


structure ReferenceStabilityDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_reference_stability_certificate
    {Input Output : Type}
    (derivation : ReferenceStabilityDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryReferenceStabilityReachabilityV0_99
