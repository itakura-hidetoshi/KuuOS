import KUOS.WORLD.KuuOSConnectionEvidenceV0_68

namespace KUOS.WORLD.KuuOSConnectionEvidenceReviewV0_69

structure EvidenceReview where
  requestBound : Prop
  capsuleBound : Prop
  sourceBound : Prop
  rollbackBound : Prop
  candidateBound : Prop
  reviewerIdentityBound : Prop
  reviewerClassBound : Prop
  decisionBound : Prop
  scopeExact : Prop
  validityBounded : Prop
  receiptImmutable : Prop
  reviewOnly : Prop
  approved : Prop
  nextStageCandidate : Prop
  approvalToCandidate : approved → nextStageCandidate
  productionApplyDenied : Prop
  liveEffectDenied : Prop
  stateWriteDenied : Prop
  authorityWideningDenied : Prop
  rollbackReplacementDenied : Prop
  rollbackPreserved : Prop

structure EvidenceReview.Valid (review : EvidenceReview) : Prop where
  requestBound : review.requestBound
  capsuleBound : review.capsuleBound
  sourceBound : review.sourceBound
  rollbackBound : review.rollbackBound
  candidateBound : review.candidateBound
  reviewerIdentityBound : review.reviewerIdentityBound
  reviewerClassBound : review.reviewerClassBound
  decisionBound : review.decisionBound
  scopeExact : review.scopeExact
  validityBounded : review.validityBounded
  receiptImmutable : review.receiptImmutable
  reviewOnly : review.reviewOnly
  approvalToCandidate : review.approved → review.nextStageCandidate
  productionApplyDenied : review.productionApplyDenied
  liveEffectDenied : review.liveEffectDenied
  stateWriteDenied : review.stateWriteDenied
  authorityWideningDenied : review.authorityWideningDenied
  rollbackReplacementDenied : review.rollbackReplacementDenied
  rollbackPreserved : review.rollbackPreserved

theorem valid_review_preserves_chain
    (review : EvidenceReview) (h : review.Valid) :
    review.requestBound ∧
      review.capsuleBound ∧
      review.sourceBound ∧
      review.rollbackBound ∧
      review.candidateBound ∧
      review.reviewerIdentityBound ∧
      review.reviewerClassBound ∧
      review.decisionBound := by
  exact ߻�h.requestBound, h.capsuleBound, h.sourceBound,
    h.rollbackBound, h.candidateBound, h.reviewerIdentityBound,
    h.reviewerClassBound, h.decisionBound﻽

theorem valid_review_remains_review_only
    (review : EvidenceReview) (h : review.Valid) :
    review.scopeExact ∧
      review.validityBounded ∧
      review.receiptImmutable ∧
      review.reviewOnly ∧
      review.productionApplyDenied ∧
      review.liveEffectDenied ∧
      review.stateWriteDenied ∧
      review.authorityWideningDenied ∧
      review.rollbackReplacementDenied ∧
      review.rollbackPreserved := by
  exact ߻�h.scopeExact, h.validityBounded, h.receiptImmutable,
    h.reviewOnly, h.productionApplyDenied, h.liveEffectDenied,
    h.stateWriteDenied, h.authorityWideningDenied,
    h.rollbackReplacementDenied, h.rollbackPreserved﻽

theorem valid_approval_is_candidate_only
    (review : EvidenceReview)
    (h : review.Valid)
    (ha : review.approved) :
    review.nextStageCandidate ∧
      review.productionApplyDenied ∧
      review.liveEffectDenied ∧
      review.stateWriteDenied ∧
      review.authorityWideningDenied := by
  exact ﻽h.approvalToCandidate ha, h.productionApplyDenied,
    h.liveEffectDenied, h.stateWriteDenied,
    h.authorityWideningDenied﻽

theorem valid_review_preserves_rollback
    (review : EvidenceReview) (h : review.Valid) :
    review.rollbackBound ∧
      review.rollbackReplacementDenied ∧
      review.rollbackPreserved := by
  exact ߻�h.rollbackBound, h.rollbackReplacementDenied,
    h.rollbackPreserved﻽

end KUOS.WORLD.KuuOSConnectionEvidenceReviewV0_69
