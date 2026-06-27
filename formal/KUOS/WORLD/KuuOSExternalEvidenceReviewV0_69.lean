import KUOS.WORLD.KuuOSConnectionEvidenceV0_68

namespace KUOS.WORLD.KuuOSExternalEvidenceReviewV0_69

structure ExternalEvidenceReviewReceipt where
  requestBinding : Prop
  capsuleBinding : Prop
  sourceBinding : Prop
  rollbackBinding : Prop
  candidateBinding : Prop
  reviewerIdentityBinding : Prop
  reviewerClassBinding : Prop
  decisionBinding : Prop
  validityBinding : Prop
  immutableReceipt : Prop
  approvalDecision : Prop
  nextStageCandidate : Prop
  candidateSound : approvalDecision ↔ nextStageCandidate
  applicationAuthorityDenied : Prop
  noLiveEffect : Prop
  noStateWrite : Prop
  noScopeWidening : Prop
  rollbackPreserved : Prop

structure ExternalEvidenceReviewReceipt.Valid
    (receipt : ExternalEvidenceReviewReceipt) : Prop where
  requestBinding : receipt.requestBinding
  capsuleBinding : receipt.capsuleBinding
  sourceBinding : receipt.sourceBinding
  rollbackBinding : receipt.rollbackBinding
  candidateBinding : receipt.candidateBinding
  reviewerIdentityBinding : receipt.reviewerIdentityBinding
  reviewerClassBinding : receipt.reviewerClassBinding
  decisionBinding : receipt.decisionBinding
  validityBinding : receipt.validityBinding
  immutableReceipt : receipt.immutableReceipt
  candidateSound : receipt.approvalDecision ↔ receipt.nextStageCandidate
  applicationAuthorityDenied : receipt.applicationAuthorityDenied
  noLiveEffect : receipt.noLiveEffect
  noStateWrite : receipt.noStateWrite
  noScopeWidening : receipt.noScopeWidening
  rollbackPreserved : receipt.rollbackPreserved

theorem valid_review_preserves_exact_chain
    (receipt : ExternalEvidenceReviewReceipt)
    (h : receipt.Valid) :
    receipt.requestBinding ∧
      receipt.capsuleBinding ∧
      receipt.sourceBinding ∧
      receipt.rollbackBinding ∧
      receipt.candidateBinding ∧
      receipt.reviewerIdentityBinding ∧
      receipt.reviewerClassBinding ∧
      receipt.decisionBinding ∧
      receipt.validityBinding := by
  exact ⟨h.requestBinding, h.capsuleBinding, h.sourceBinding,
    h.rollbackBinding, h.candidateBinding, h.reviewerIdentityBinding,
    h.reviewerClassBinding, h.decisionBinding, h.validityBinding⟩

theorem valid_review_couples_approval_to_next_stage
    (receipt : ExternalEvidenceReviewReceipt)
    (h : receipt.Valid) :
    receipt.approvalDecision ↔ receipt.nextStageCandidate := by
  exact h.candidateSound

theorem valid_approval_is_candidate_only
    (receipt : ExternalEvidenceReviewReceipt)
    (h : receipt.Valid)
    (ha : receipt.approvalDecision) :
    receipt.nextStageCandidate ∧
      receipt.applicationAuthorityDenied ∧
      receipt.noLiveEffect ∧
      receipt.noStateWrite ∧
      receipt.noScopeWidening := by
  exact ⟨h.candidateSound.mp ha, h.applicationAuthorityDenied,
    h.noLiveEffect, h.noStateWrite, h.noScopeWidening⟩

theorem valid_review_remains_bounded
    (receipt : ExternalEvidenceReviewReceipt)
    (h : receipt.Valid) :
    receipt.immutableReceipt ∧
      receipt.applicationAuthorityDenied ∧
      receipt.noLiveEffect ∧
      receipt.noStateWrite ∧
      receipt.noScopeWidening ∧
      receipt.rollbackPreserved := by
  exact ⟨h.immutableReceipt, h.applicationAuthorityDenied,
    h.noLiveEffect, h.noStateWrite,
    h.noScopeWidening, h.rollbackPreserved⟩

end KUOS.WORLD.KuuOSExternalEvidenceReviewV0_69
