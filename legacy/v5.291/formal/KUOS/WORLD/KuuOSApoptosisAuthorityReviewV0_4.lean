import KUOS.WORLD.KuuOSApoptosisDependencyReviewV0_3

namespace KUOS.WORLD.KuuOSApoptosisAuthorityReviewV0_4

inductive AuthorityReviewStatus where
  | clearForQuiescenceReview
  | blocked
  | rejected
  deriving DecidableEq, Repr

structure ApoptosisAuthorityReviewWitness where
  sourceDependencyRecomputedValid : Bool
  sourceDependencyClear : Bool
  sourceBindingValid : Bool
  reviewerAllowed : Bool
  reviewerIndependent : Bool
  evidenceValid : Bool
  evidenceFresh : Bool
  authorityClosureComplete : Bool
  responsibleAuthorityPresent : Bool
  responsibilityAcknowledged : Bool
  delegationChainComplete : Bool
  subjectControlsResponsibleAuthority : Bool
  institutionalHoldPresent : Bool
  constitutionalProtectionPresent : Bool
  protectedAuthorityPresent : Bool
  unresolvedAuthorityPresent : Bool
  authorityCyclePresent : Bool
  emergencyOverrideActive : Bool
  status : AuthorityReviewStatus
  authorityReviewRecordIssued : Bool
  authorityClearForQuiescenceReview : Bool
  quiescenceReviewRequiredNext : Bool
  externalReviewRequiredNext : Bool
  independentAuthorizationRequiredNext : Bool
  authorityRevocationPerformed : Bool
  quiescenceTransitionPerformed : Bool
  terminalTransitionPerformed : Bool
  tombstoneWritePerformed : Bool
  physicalDeletionPerformed : Bool
  liveGitExecutionPerformed : Bool
  repositoryMutationPerformed : Bool

structure ApoptosisAuthorityReviewWitness.ValidClear
    (w : ApoptosisAuthorityReviewWitness) : Prop where
  sourceDependencyRecomputedValid :
    w.sourceDependencyRecomputedValid = true
  sourceDependencyClear : w.sourceDependencyClear = true
  sourceBindingValid : w.sourceBindingValid = true
  reviewerAllowed : w.reviewerAllowed = true
  reviewerIndependent : w.reviewerIndependent = true
  evidenceValid : w.evidenceValid = true
  evidenceFresh : w.evidenceFresh = true
  authorityClosureComplete : w.authorityClosureComplete = true
  responsibleAuthorityPresent : w.responsibleAuthorityPresent = true
  responsibilityAcknowledged : w.responsibilityAcknowledged = true
  delegationChainComplete : w.delegationChainComplete = true
  subjectDoesNotControlResponsibleAuthority :
    w.subjectControlsResponsibleAuthority = false
  institutionalHoldAbsent : w.institutionalHoldPresent = false
  constitutionalProtectionAbsent :
    w.constitutionalProtectionPresent = false
  protectedAuthorityAbsent : w.protectedAuthorityPresent = false
  unresolvedAuthorityAbsent : w.unresolvedAuthorityPresent = false
  authorityCycleAbsent : w.authorityCyclePresent = false
  emergencyOverrideAbsent : w.emergencyOverrideActive = false
  statusClear : w.status = AuthorityReviewStatus.clearForQuiescenceReview
  authorityReviewRecordIssued : w.authorityReviewRecordIssued = true
  authorityClearForQuiescenceReview :
    w.authorityClearForQuiescenceReview = true
  quiescenceReviewRequiredNext : w.quiescenceReviewRequiredNext = true
  externalReviewRequiredNext : w.externalReviewRequiredNext = true
  independentAuthorizationRequiredNext :
    w.independentAuthorizationRequiredNext = true
  authorityRevocationNotPerformed : w.authorityRevocationPerformed = false
  quiescenceTransitionNotPerformed : w.quiescenceTransitionPerformed = false
  terminalTransitionNotPerformed : w.terminalTransitionPerformed = false
  tombstoneWriteNotPerformed : w.tombstoneWritePerformed = false
  physicalDeletionNotPerformed : w.physicalDeletionPerformed = false
  liveGitExecutionNotPerformed : w.liveGitExecutionPerformed = false
  repositoryMutationNotPerformed : w.repositoryMutationPerformed = false

structure ApoptosisAuthorityReviewWitness.ValidBlocked
    (w : ApoptosisAuthorityReviewWitness) : Prop where
  statusBlocked : w.status = AuthorityReviewStatus.blocked
  authorityReviewRecordIssued : w.authorityReviewRecordIssued = true
  authorityNotClear : w.authorityClearForQuiescenceReview = false
  quiescenceReviewNotRequiredNext : w.quiescenceReviewRequiredNext = false
  externalReviewNotRequiredNext : w.externalReviewRequiredNext = false
  independentAuthorizationNotRequiredNext :
    w.independentAuthorizationRequiredNext = false
  authorityRevocationNotPerformed : w.authorityRevocationPerformed = false
  quiescenceTransitionNotPerformed : w.quiescenceTransitionPerformed = false
  terminalTransitionNotPerformed : w.terminalTransitionPerformed = false
  tombstoneWriteNotPerformed : w.tombstoneWritePerformed = false
  physicalDeletionNotPerformed : w.physicalDeletionPerformed = false
  liveGitExecutionNotPerformed : w.liveGitExecutionPerformed = false
  repositoryMutationNotPerformed : w.repositoryMutationPerformed = false

structure ApoptosisAuthorityReviewWitness.ValidRejected
    (w : ApoptosisAuthorityReviewWitness) : Prop where
  statusRejected : w.status = AuthorityReviewStatus.rejected
  authorityReviewRecordNotIssued : w.authorityReviewRecordIssued = false
  authorityNotClear : w.authorityClearForQuiescenceReview = false
  quiescenceReviewNotRequiredNext : w.quiescenceReviewRequiredNext = false
  externalReviewNotRequiredNext : w.externalReviewRequiredNext = false
  independentAuthorizationNotRequiredNext :
    w.independentAuthorizationRequiredNext = false
  authorityRevocationNotPerformed : w.authorityRevocationPerformed = false
  quiescenceTransitionNotPerformed : w.quiescenceTransitionPerformed = false
  terminalTransitionNotPerformed : w.terminalTransitionPerformed = false
  tombstoneWriteNotPerformed : w.tombstoneWritePerformed = false
  physicalDeletionNotPerformed : w.physicalDeletionPerformed = false
  liveGitExecutionNotPerformed : w.liveGitExecutionPerformed = false
  repositoryMutationNotPerformed : w.repositoryMutationPerformed = false


theorem clear_authority_review_requires_later_gates
    (w : ApoptosisAuthorityReviewWitness)
    (h : w.ValidClear) :
    w.quiescenceReviewRequiredNext = true ∧
      w.externalReviewRequiredNext = true ∧
      w.independentAuthorizationRequiredNext = true := by
  exact ⟨h.quiescenceReviewRequiredNext,
    h.externalReviewRequiredNext,
    h.independentAuthorizationRequiredNext⟩


theorem clear_authority_review_is_independent
    (w : ApoptosisAuthorityReviewWitness)
    (h : w.ValidClear) :
    w.reviewerAllowed = true ∧ w.reviewerIndependent = true := by
  exact ⟨h.reviewerAllowed, h.reviewerIndependent⟩


theorem blocked_authority_review_does_not_advance
    (w : ApoptosisAuthorityReviewWitness)
    (h : w.ValidBlocked) :
    w.authorityClearForQuiescenceReview = false ∧
      w.quiescenceReviewRequiredNext = false ∧
      w.externalReviewRequiredNext = false ∧
      w.independentAuthorizationRequiredNext = false := by
  exact ⟨h.authorityNotClear,
    h.quiescenceReviewNotRequiredNext,
    h.externalReviewNotRequiredNext,
    h.independentAuthorizationNotRequiredNext⟩


theorem valid_authority_review_performs_no_lifecycle_effect
    (w : ApoptosisAuthorityReviewWitness)
    (h : w.ValidClear ∨ w.ValidBlocked ∨ w.ValidRejected) :
    w.authorityRevocationPerformed = false ∧
      w.quiescenceTransitionPerformed = false ∧
      w.terminalTransitionPerformed = false ∧
      w.tombstoneWritePerformed = false ∧
      w.physicalDeletionPerformed = false ∧
      w.liveGitExecutionPerformed = false ∧
      w.repositoryMutationPerformed = false := by
  rcases h with h | h | h
  · exact ⟨h.authorityRevocationNotPerformed,
      h.quiescenceTransitionNotPerformed,
      h.terminalTransitionNotPerformed,
      h.tombstoneWriteNotPerformed,
      h.physicalDeletionNotPerformed,
      h.liveGitExecutionNotPerformed,
      h.repositoryMutationNotPerformed⟩
  · exact ⟨h.authorityRevocationNotPerformed,
      h.quiescenceTransitionNotPerformed,
      h.terminalTransitionNotPerformed,
      h.tombstoneWriteNotPerformed,
      h.physicalDeletionNotPerformed,
      h.liveGitExecutionNotPerformed,
      h.repositoryMutationNotPerformed⟩
  · exact ⟨h.authorityRevocationNotPerformed,
      h.quiescenceTransitionNotPerformed,
      h.terminalTransitionNotPerformed,
      h.tombstoneWriteNotPerformed,
      h.physicalDeletionNotPerformed,
      h.liveGitExecutionNotPerformed,
      h.repositoryMutationNotPerformed⟩

structure ApoptosisAuthorityReviewDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_authority_review
    {Input Output : Type}
    (derivation : ApoptosisAuthorityReviewDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSApoptosisAuthorityReviewV0_4
