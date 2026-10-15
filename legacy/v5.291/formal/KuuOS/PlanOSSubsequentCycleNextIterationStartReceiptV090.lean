import KuuOS.PlanOSV089

namespace KuuOS.PlanOS

structure SubsequentCycleNextIterationStartReceiptV090 where
  sourceNextIterationRequestPreserved : Prop
  selectedCandidateEvidencePreserved : Prop
  learningUpdateEvidencePreserved : Prop
  nextIterationScopePreserved : Prop
  nextIterationConstraintsPreserved : Prop
  nextIterationRequested : Prop
  nextIterationStarted : Prop
  nextIterationPlanningRequested : Prop

structure SubsequentCycleNextIterationStartReceiptV090Valid
    (r : SubsequentCycleNextIterationStartReceiptV090) : Prop where
  source_next_iteration_request_preserved : r.sourceNextIterationRequestPreserved
  selected_candidate_evidence_preserved : r.selectedCandidateEvidencePreserved
  learning_update_evidence_preserved : r.learningUpdateEvidencePreserved
  next_iteration_scope_preserved : r.nextIterationScopePreserved
  next_iteration_constraints_preserved : r.nextIterationConstraintsPreserved
  next_iteration_requested : r.nextIterationRequested
  next_iteration_started : r.nextIterationStarted
  next_iteration_planning_not_requested : ¬ r.nextIterationPlanningRequested

theorem subsequentCycleNextIterationStartReceiptV090_preservesEvidence
    (r : SubsequentCycleNextIterationStartReceiptV090)
    (h : SubsequentCycleNextIterationStartReceiptV090Valid r) :
    r.sourceNextIterationRequestPreserved ∧
    r.selectedCandidateEvidencePreserved ∧
    r.learningUpdateEvidencePreserved := by
  exact ⟨h.source_next_iteration_request_preserved,
    h.selected_candidate_evidence_preserved,
    h.learning_update_evidence_preserved⟩

theorem subsequentCycleNextIterationStartReceiptV090_startsIteration
    (r : SubsequentCycleNextIterationStartReceiptV090)
    (h : SubsequentCycleNextIterationStartReceiptV090Valid r) :
    r.nextIterationRequested ∧ r.nextIterationStarted := by
  exact ⟨h.next_iteration_requested, h.next_iteration_started⟩

theorem subsequentCycleNextIterationStartReceiptV090_keepsPlanningSeparate
    (r : SubsequentCycleNextIterationStartReceiptV090)
    (h : SubsequentCycleNextIterationStartReceiptV090Valid r) :
    ¬ r.nextIterationPlanningRequested := by
  exact h.next_iteration_planning_not_requested

end KuuOS.PlanOS
