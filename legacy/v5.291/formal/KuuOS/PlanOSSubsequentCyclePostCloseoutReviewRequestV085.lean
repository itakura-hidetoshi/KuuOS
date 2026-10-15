import KuuOS.PlanOSV084

namespace KuuOS.PlanOS

structure SubsequentCyclePostCloseoutReviewRequestV085 where
  sourceCloseoutReceiptPreserved : Prop
  selectedCandidateEvidencePreserved : Prop
  executionCompletionEvidencePreserved : Prop
  closeoutEvidencePreserved : Prop
  reviewScopePreserved : Prop
  reviewCriteriaPreserved : Prop
  cycleClosed : Prop
  postCloseoutReviewRequested : Prop
  postCloseoutReviewCompleted : Prop

structure SubsequentCyclePostCloseoutReviewRequestV085Valid
    (r : SubsequentCyclePostCloseoutReviewRequestV085) : Prop where
  source_closeout_receipt_preserved : r.sourceCloseoutReceiptPreserved
  selected_candidate_evidence_preserved : r.selectedCandidateEvidencePreserved
  execution_completion_evidence_preserved : r.executionCompletionEvidencePreserved
  closeout_evidence_preserved : r.closeoutEvidencePreserved
  review_scope_preserved : r.reviewScopePreserved
  review_criteria_preserved : r.reviewCriteriaPreserved
  cycle_closed : r.cycleClosed
  post_closeout_review_requested : r.postCloseoutReviewRequested
  post_closeout_review_not_completed : ¬ r.postCloseoutReviewCompleted

theorem subsequentCyclePostCloseoutReviewRequestV085_preservesEvidence
    (r : SubsequentCyclePostCloseoutReviewRequestV085)
    (h : SubsequentCyclePostCloseoutReviewRequestV085Valid r) :
    r.sourceCloseoutReceiptPreserved ∧
    r.selectedCandidateEvidencePreserved ∧
    r.executionCompletionEvidencePreserved ∧
    r.closeoutEvidencePreserved := by
  exact ⟨h.source_closeout_receipt_preserved,
    h.selected_candidate_evidence_preserved,
    h.execution_completion_evidence_preserved,
    h.closeout_evidence_preserved⟩

theorem subsequentCyclePostCloseoutReviewRequestV085_requestsBoundedReview
    (r : SubsequentCyclePostCloseoutReviewRequestV085)
    (h : SubsequentCyclePostCloseoutReviewRequestV085Valid r) :
    r.cycleClosed ∧ r.postCloseoutReviewRequested := by
  exact ⟨h.cycle_closed, h.post_closeout_review_requested⟩

theorem subsequentCyclePostCloseoutReviewRequestV085_keepsCompletionSeparate
    (r : SubsequentCyclePostCloseoutReviewRequestV085)
    (h : SubsequentCyclePostCloseoutReviewRequestV085Valid r) :
    ¬ r.postCloseoutReviewCompleted := by
  exact h.post_closeout_review_not_completed

end KuuOS.PlanOS
