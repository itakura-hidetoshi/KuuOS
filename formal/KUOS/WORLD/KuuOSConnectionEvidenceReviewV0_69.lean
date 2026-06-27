import KUOS.WORLD.KuuOSConnectionEvidenceV0_68

namespace KUOS.WORLD.KuuOSConnectionEvidenceReviewV0_69

structure ExternalEvidenceReview where
  evidenceCapsuleBinding : Prop
  sourceBinding : Prop
  rollbackBinding : Prop
  candidateBinding : Prop
  reviewerIdentityBinding : Prop
  reviewerClassBinding : Prop
  decisionBinding : Prop
  withinValidity : Prop
  scopeExact : Prop
  immutableRecord : Prop
  reviewOnly : Prop
  approved : Prop
  governedAdmissionCandidate : Prop
  approvalCandidateOnly : approved → governedAdmissionCandidate
  liveEffectDenied : Prop
  stateWriteDenied : Prop
  authorityWideningDenied : Prop
  rollbackReplacementDenied : Prop

structure ExternalEvidenceReview.Valid
    (review : ExternalEvidenceReview) : Prop where
  evidenceCapsuleBinding : review.evidenceCapsuleBinding
  sourceBinding : review.sourceBinding
  rollbackBinding : review.rollbackBinding
  candidateBinding : review.candidateBinding
  reviewerIdentityBinding : review.reviewerIdentityBinding
  reviewerClassBinding : review.reviewerClassBinding
  decisionBinding : review.decisionBinding
  withinValidity : review.withinValidity
  scopeExact : review.scopeExact
  immutableRecord : review.immutableRecord
  reviewOnly : review.reviewOnly
  approvalCandidateOnly : review.approved → review.governedAdmissionCandidate
  liveEffectDenied : review.liveEffectDenied
  stateWriteDenied : review.stateWriteDenied
  authorityWideningDenied : review.authorityWideningDenied
  rollbackReplacementDenied : review.rollbackReplacementDenied

theorem valid_review_preserves_evidence_chain
    (review : ExternalEvidenceReview)
    (h : review.Valid) :
    review.evidenceCapsuleBinding ∧
      review.sourceBinding ∧
      review.rollbackBinding ∧
      review.candidateBinding ∧
      review.reviewerIdentityBinding ∧
      review.reviewerClassBinding ∧
      review.decisionBinding := by
  exact ⟨h.evidenceCapsuleBinding, h.sourceBinding, h.rollbackBinding,
    h.candidateBinding, h.reviewerIdentityBinding,
    h.reviewerClassBinding, h.decisionBinding⟩

theorem valid_review_remains_review_only
    (review : ExternalEvidenceReview)
    (h : review.Valid) :
    review.withinValidity ∧
      review.scopeExact ∧
      review.immutableRecord ∧
      review.reviewOnly ∧
      review.liveEffectDenied ∧
      review.stateWriteDenied ∧
      review.authorityWideningDenied ∧
      review.rollbackReplacementDenied := by
  exact ⟨h.withinValidity, h.scopeExact, h.immutableRecord,
    h.reviewOnly, h.liveEffectDenied, h.stateWriteDenied,
    h.authorityWideningDenied, h.rollbackReplacementDenied⟩

theorem valid_approval_is_candidate_only
    (review : ExternalEvidenceReview)
    (h : review.Valid)
    (ha : review.approved) :
    review.governedAdmissionCandidate ∧
      review.liveEffectDenied ∧
      review.stateWriteDenied ∧
      review.authorityWideningDenied := by
  exact ⟨h.approvalCandidateOnly ha, h.liveEffectDenied,
    h.stateWriteDenied, h.authorityWideningDenied⟩

end KUOS.WORLD.KuuOSConnectionEvidenceReviewV0_69
