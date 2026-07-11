import KuuOS.PlanOSV081

namespace KuuOS.PlanOS

structure SubsequentCycleExecutionCompletionReceiptV082 where
  sourceCompletionRequestPreserved : Prop
  selectedCandidateEvidencePreserved : Prop
  admissionEvidencePreserved : Prop
  cycleStartEvidencePreserved : Prop
  executionEvidencePreserved : Prop
  completionScopePreserved : Prop
  completionConstraintsPreserved : Prop
  completionRequested : Prop
  executionCompleted : Prop
  closeoutRequested : Prop

structure SubsequentCycleExecutionCompletionReceiptV082Valid
    (r : SubsequentCycleExecutionCompletionReceiptV082) : Prop where
  source_completion_request_preserved : r.sourceCompletionRequestPreserved
  selected_candidate_evidence_preserved : r.selectedCandidateEvidencePreserved
  admission_evidence_preserved : r.admissionEvidencePreserved
  cycle_start_evidence_preserved : r.cycleStartEvidencePreserved
  execution_evidence_preserved : r.executionEvidencePreserved
  completion_scope_preserved : r.completionScopePreserved
  completion_constraints_preserved : r.completionConstraintsPreserved
  completion_requested : r.completionRequested
  execution_completed : r.executionCompleted
  closeout_not_requested : ¬ r.closeoutRequested

theorem subsequentCycleExecutionCompletionReceiptV082_preservesEvidence
    (r : SubsequentCycleExecutionCompletionReceiptV082)
    (h : SubsequentCycleExecutionCompletionReceiptV082Valid r) :
    r.sourceCompletionRequestPreserved ∧
    r.selectedCandidateEvidencePreserved ∧
    r.admissionEvidencePreserved ∧
    r.cycleStartEvidencePreserved ∧
    r.executionEvidencePreserved := by
  exact ⟨h.source_completion_request_preserved,
    h.selected_candidate_evidence_preserved,
    h.admission_evidence_preserved,
    h.cycle_start_evidence_preserved,
    h.execution_evidence_preserved⟩

theorem subsequentCycleExecutionCompletionReceiptV082_completesExecution
    (r : SubsequentCycleExecutionCompletionReceiptV082)
    (h : SubsequentCycleExecutionCompletionReceiptV082Valid r) :
    r.completionRequested ∧ r.executionCompleted := by
  exact ⟨h.completion_requested, h.execution_completed⟩

theorem subsequentCycleExecutionCompletionReceiptV082_doesNotRequestCloseout
    (r : SubsequentCycleExecutionCompletionReceiptV082)
    (h : SubsequentCycleExecutionCompletionReceiptV082Valid r) :
    ¬ r.closeoutRequested := by
  exact h.closeout_not_requested

end KuuOS.PlanOS
