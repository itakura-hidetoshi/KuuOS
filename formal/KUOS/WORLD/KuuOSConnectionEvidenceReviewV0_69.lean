import KUOS.WORLD.KuuOSConnectionEvidenceV0_68

namespace KUOS.WORLD.KuuOSConnectionEvidenceReviewV0_69

structure ExternalEvidenceReview where
  requestBinding : Prop
  capsuleBinding : Prop
  sourceBinding : Prop
  rollbackBinding : Prop
  candidateBinding : Prop
  reviewerIdentityBinding : Prop
  reviewerClassBinding : Prop
  decisionBinding : Prop
  withinValidity : Prop
  exactScope : Prop
  immutableRecord : Prop
  approved : Prop
  applicationAuthorized : Prop
  authorizationSound : approved ↔ applicationAuthorized
  noLiveEffectPerformed : Prop
  noStateWritePerformed : Prop
  noAuthorityWidening : Prop
  rollbackPreserved : Prop

structure ExternalEvidenceReview.Valid
    (review : ExternalEvidenceReview) : Prop where
  requestBinding : review.requestBinding
  capsuleBinding : review.capsuleBinding
  sourceBinding : review.sourceBinding
  rollbackBinding : review.rollbackBinding
  candidateBinding : review.candidateBinding
  reviewerIdentityBinding : review.reviewerIdentityBinding
  reviewerClassBinding : review.reviewerClassBinding
  decisionBinding : review.decisionBinding
  withinValidity : review.withinValidity
  exactScope : review.exactScope
  immutableRecord : review.immutableRecord
  authorizationSound : review.approved ↔ review.applicationAuthorized
  noLiveEffectPerformed : review.noLiveEffectPerformed
  noStateWritePerformed : review.noStateWritePerformed
  noAuthorityWidening : review.noAuthorityWidening
  rollbackPreserved : review.rollbackPreserved

theorem valid_review_preserves_exact_chain
    (review : ExternalEvidenceReview)
    (h : review.Valid) :
    review.requestBinding ∧
      review.capsuleBinding ∧
      review.sourceBinding ∧
      review.rollbackBinding ∧
      review.candidateBinding ∧
      review.reviewerIdentityBinding ∧
      review.reviewerClassBinding ∧
      review.decisionBinding := by
  exact ⟨h.requestBinding, h.capsuleBinding, h.sourceBinding,
    h.rollbackBinding, h.candidateBinding, h.reviewerIdentityBinding,
    h.reviewerClassBinding, h.decisionBinding⟩

theorem valid_approval_iff_application_authorized
    (review : ExternalEvidenceReview)
    (h : review.Valid) :
    review.approved ↔ review.applicationAuthorized := by
  exact h.authorizationSound

theorem valid_approval_grants_application_authority
    (review : ExternalEvidenceReview)
    (h : review.Valid)
    (ha : review.approved) : review.applicationAuthorized := by
  exact h.authorizationSound.mp ha

theorem valid_application_authority_requires_approval
    (review : ExternalEvidenceReview)
    (h : review.Valid)
    (ha : review.applicationAuthorized) : review.approved := by
  exact h.authorizationSound.mpr ha

theorem valid_review_records_no_unperformed_effect
    (review : ExternalEvidenceReview)
    (h : review.Valid) :
    review.withinValidity ∧
      review.exactScope ∧
      review.immutableRecord ∧
      review.noLiveEffectPerformed ∧
      review.noStateWritePerformed ∧
      review.noAuthorityWidening ∧
      review.rollbackPreserved := by
  exact ⟨h.withinValidity, h.exactScope, h.immutableRecord,
    h.noLiveEffectPerformed, h.noStateWritePerformed,
    h.noAuthorityWidening, h.rollbackPreserved⟩

end KUOS.WORLD.KuuOSConnectionEvidenceReviewV0_69
