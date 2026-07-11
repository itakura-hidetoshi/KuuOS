import KuuOS.PlanOSV088

namespace KuuOS.PlanOS

structure SubsequentCycleNextIterationRequestV089 where
  sourceLearningUpdateReceiptPreserved : Prop
  selectedCandidateEvidencePreserved : Prop
  closeoutEvidencePreserved : Prop
  learningUpdateEvidencePreserved : Prop
  nextIterationScopePreserved : Prop
  nextIterationConstraintsPreserved : Prop
  nextIterationRequested : Prop
  nextIterationStarted : Prop

structure SubsequentCycleNextIterationRequestV089Valid
    (r : SubsequentCycleNextIterationRequestV089) : Prop where
  source_learning_update_receipt_preserved : r.sourceLearningUpdateReceiptPreserved
  selected_candidate_evidence_preserved : r.selectedCandidateEvidencePreserved
  closeout_evidence_preserved : r.closeoutEvidencePreserved
  learning_update_evidence_preserved : r.learningUpdateEvidencePreserved
  next_iteration_scope_preserved : r.nextIterationScopePreserved
  next_iteration_constraints_preserved : r.nextIterationConstraintsPreserved
  next_iteration_requested : r.nextIterationRequested
  next_iteration_not_started : ¬ r.nextIterationStarted

theorem subsequentCycleNextIterationRequestV089_preservesEvidence
    (r : SubsequentCycleNextIterationRequestV089)
    (h : SubsequentCycleNextIterationRequestV089Valid r) :
    r.sourceLearningUpdateReceiptPreserved ∧
    r.selectedCandidateEvidencePreserved ∧
    r.learningUpdateEvidencePreserved := by
  exact ⟨h.source_learning_update_receipt_preserved,
    h.selected_candidate_evidence_preserved,
    h.learning_update_evidence_preserved⟩

theorem subsequentCycleNextIterationRequestV089_requestsNextIteration
    (r : SubsequentCycleNextIterationRequestV089)
    (h : SubsequentCycleNextIterationRequestV089Valid r) :
    r.nextIterationRequested := by
  exact h.next_iteration_requested

theorem subsequentCycleNextIterationRequestV089_keepsStartSeparate
    (r : SubsequentCycleNextIterationRequestV089)
    (h : SubsequentCycleNextIterationRequestV089Valid r) :
    ¬ r.nextIterationStarted := by
  exact h.next_iteration_not_started

end KuuOS.PlanOS
