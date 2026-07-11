import KuuOS.PlanOSV085

namespace KuuOS.PlanOS

structure SubsequentCyclePostCloseoutReviewReceiptV086 where
  sourceReviewRequestPreserved : Prop
  selectedCandidateEvidencePreserved : Prop
  closeoutEvidencePreserved : Prop
  reviewScopePreserved : Prop
  reviewCriteriaPreserved : Prop
  reviewRequested : Prop
  reviewCompleted : Prop
  learningUpdateRequested : Prop

structure SubsequentCyclePostCloseoutReviewReceiptV086Valid
    (r : SubsequentCyclePostCloseoutReviewReceiptV086) : Prop where
  source_review_request_preserved : r.sourceReviewRequestPreserved
  selected_candidate_evidence_preserved : r.selectedCandidateEvidencePreserved
  closeout_evidence_preserved : r.closeoutEvidencePreserved
  review_scope_preserved : r.reviewScopePreserved
  review_criteria_preserved : r.reviewCriteriaPreserved
  review_requested : r.reviewRequested
  review_completed : r.reviewCompleted
  learning_update_not_requested : ¬ r.learningUpdateRequested

theorem subsequentCyclePostCloseoutReviewReceiptV086_preservesEvidence
    (r : SubsequentCyclePostCloseoutReviewReceiptV086)
    (h : SubsequentCyclePostCloseoutReviewReceiptV086Valid r) :
    r.sourceReviewRequestPreserved ∧
    r.selectedCandidateEvidencePreserved ∧
    r.closeoutEvidencePreserved := by
  exact ⟨h.source_review_request_preserved,
    h.selected_candidate_evidence_preserved,
    h.closeout_evidence_preserved⟩

theorem subsequentCyclePostCloseoutReviewReceiptV086_completesReview
    (r : SubsequentCyclePostCloseoutReviewReceiptV086)
    (h : SubsequentCyclePostCloseoutReviewReceiptV086Valid r) :
    r.reviewRequested ∧ r.reviewCompleted := by
  exact ⟨h.review_requested, h.review_completed⟩

theorem subsequentCyclePostCloseoutReviewReceiptV086_keepsLearningSeparate
    (r : SubsequentCyclePostCloseoutReviewReceiptV086)
    (h : SubsequentCyclePostCloseoutReviewReceiptV086Valid r) :
    ¬ r.learningUpdateRequested := by
  exact h.learning_update_not_requested

end KuuOS.PlanOS
