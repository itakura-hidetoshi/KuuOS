import KuuOS.PlanOSV087

namespace KuuOS.PlanOS

structure SubsequentCycleLearningUpdateReceiptV088 where
  sourceLearningUpdateRequestPreserved : Prop
  selectedCandidateEvidencePreserved : Prop
  closeoutEvidencePreserved : Prop
  reviewCompletionEvidencePreserved : Prop
  learningUpdateScopePreserved : Prop
  learningUpdateConstraintsPreserved : Prop
  learningUpdateRequested : Prop
  learningUpdateApplied : Prop
  nextIterationRequested : Prop

structure SubsequentCycleLearningUpdateReceiptV088Valid
    (r : SubsequentCycleLearningUpdateReceiptV088) : Prop where
  source_learning_update_request_preserved : r.sourceLearningUpdateRequestPreserved
  selected_candidate_evidence_preserved : r.selectedCandidateEvidencePreserved
  closeout_evidence_preserved : r.closeoutEvidencePreserved
  review_completion_evidence_preserved : r.reviewCompletionEvidencePreserved
  learning_update_scope_preserved : r.learningUpdateScopePreserved
  learning_update_constraints_preserved : r.learningUpdateConstraintsPreserved
  learning_update_requested : r.learningUpdateRequested
  learning_update_applied : r.learningUpdateApplied
  next_iteration_not_requested : ¬ r.nextIterationRequested

theorem subsequentCycleLearningUpdateReceiptV088_preservesEvidence
    (r : SubsequentCycleLearningUpdateReceiptV088)
    (h : SubsequentCycleLearningUpdateReceiptV088Valid r) :
    r.sourceLearningUpdateRequestPreserved ∧
    r.selectedCandidateEvidencePreserved ∧
    r.closeoutEvidencePreserved ∧
    r.reviewCompletionEvidencePreserved := by
  exact ⟨h.source_learning_update_request_preserved,
    h.selected_candidate_evidence_preserved,
    h.closeout_evidence_preserved,
    h.review_completion_evidence_preserved⟩

theorem subsequentCycleLearningUpdateReceiptV088_appliesLearning
    (r : SubsequentCycleLearningUpdateReceiptV088)
    (h : SubsequentCycleLearningUpdateReceiptV088Valid r) :
    r.learningUpdateRequested ∧ r.learningUpdateApplied := by
  exact ⟨h.learning_update_requested, h.learning_update_applied⟩

theorem subsequentCycleLearningUpdateReceiptV088_keepsNextIterationSeparate
    (r : SubsequentCycleLearningUpdateReceiptV088)
    (h : SubsequentCycleLearningUpdateReceiptV088Valid r) :
    ¬ r.nextIterationRequested := by
  exact h.next_iteration_not_requested

end KuuOS.PlanOS
