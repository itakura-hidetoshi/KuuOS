import KuuOS.PlanOSV086

namespace KuuOS.PlanOS

structure SubsequentCycleLearningUpdateRequestV087 where
  sourceReviewReceiptPreserved : Prop
  selectedCandidateEvidencePreserved : Prop
  closeoutEvidencePreserved : Prop
  reviewCompletionEvidencePreserved : Prop
  learningUpdateScopePreserved : Prop
  learningUpdateConstraintsPreserved : Prop
  learningUpdateRequested : Prop
  learningUpdateApplied : Prop

structure SubsequentCycleLearningUpdateRequestV087Valid
    (r : SubsequentCycleLearningUpdateRequestV087) : Prop where
  source_review_receipt_preserved : r.sourceReviewReceiptPreserved
  selected_candidate_evidence_preserved : r.selectedCandidateEvidencePreserved
  closeout_evidence_preserved : r.closeoutEvidencePreserved
  review_completion_evidence_preserved : r.reviewCompletionEvidencePreserved
  learning_update_scope_preserved : r.learningUpdateScopePreserved
  learning_update_constraints_preserved : r.learningUpdateConstraintsPreserved
  learning_update_requested : r.learningUpdateRequested
  learning_update_not_applied : ¬ r.learningUpdateApplied

theorem subsequentCycleLearningUpdateRequestV087_preservesEvidence
    (r : SubsequentCycleLearningUpdateRequestV087)
    (h : SubsequentCycleLearningUpdateRequestV087Valid r) :
    r.sourceReviewReceiptPreserved ∧
    r.selectedCandidateEvidencePreserved ∧
    r.closeoutEvidencePreserved ∧
    r.reviewCompletionEvidencePreserved := by
  exact ⟨h.source_review_receipt_preserved,
    h.selected_candidate_evidence_preserved,
    h.closeout_evidence_preserved,
    h.review_completion_evidence_preserved⟩

theorem subsequentCycleLearningUpdateRequestV087_requestsBoundedUpdate
    (r : SubsequentCycleLearningUpdateRequestV087)
    (h : SubsequentCycleLearningUpdateRequestV087Valid r) :
    r.learningUpdateScopePreserved ∧
    r.learningUpdateConstraintsPreserved ∧
    r.learningUpdateRequested := by
  exact ⟨h.learning_update_scope_preserved,
    h.learning_update_constraints_preserved,
    h.learning_update_requested⟩

theorem subsequentCycleLearningUpdateRequestV087_keepsApplicationSeparate
    (r : SubsequentCycleLearningUpdateRequestV087)
    (h : SubsequentCycleLearningUpdateRequestV087Valid r) :
    ¬ r.learningUpdateApplied := by
  exact h.learning_update_not_applied

end KuuOS.PlanOS