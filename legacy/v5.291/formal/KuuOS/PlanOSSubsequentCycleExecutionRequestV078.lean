import KuuOS.PlanOSV077

namespace KuuOS.PlanOS

structure SubsequentCycleExecutionRequestV078 where
  sourceStartReceiptPreserved : Prop
  selectedCandidateEvidencePreserved : Prop
  admissionEvidencePreserved : Prop
  startEvidencePreserved : Prop
  executionScopePreserved : Prop
  executionConstraintsPreserved : Prop
  cycleStarted : Prop
  executionRequested : Prop
  executionAuthorityGranted : Prop
  executionStarted : Prop

structure SubsequentCycleExecutionRequestV078Valid
    (r : SubsequentCycleExecutionRequestV078) : Prop where
  source_start_receipt_preserved : r.sourceStartReceiptPreserved
  selected_candidate_evidence_preserved : r.selectedCandidateEvidencePreserved
  admission_evidence_preserved : r.admissionEvidencePreserved
  start_evidence_preserved : r.startEvidencePreserved
  execution_scope_preserved : r.executionScopePreserved
  execution_constraints_preserved : r.executionConstraintsPreserved
  cycle_started : r.cycleStarted
  execution_requested : r.executionRequested
  execution_authority_not_granted : ¬ r.executionAuthorityGranted
  execution_not_started : ¬ r.executionStarted

theorem subsequentCycleExecutionRequestV078_preservesEvidence
    (r : SubsequentCycleExecutionRequestV078)
    (h : SubsequentCycleExecutionRequestV078Valid r) :
    r.sourceStartReceiptPreserved ∧
    r.selectedCandidateEvidencePreserved ∧
    r.admissionEvidencePreserved ∧
    r.startEvidencePreserved := by
  exact ⟨h.source_start_receipt_preserved,
    h.selected_candidate_evidence_preserved,
    h.admission_evidence_preserved,
    h.start_evidence_preserved⟩

theorem subsequentCycleExecutionRequestV078_requestsExecution
    (r : SubsequentCycleExecutionRequestV078)
    (h : SubsequentCycleExecutionRequestV078Valid r) :
    r.cycleStarted ∧ r.executionRequested := by
  exact ⟨h.cycle_started, h.execution_requested⟩

theorem subsequentCycleExecutionRequestV078_keepsExecutionClosed
    (r : SubsequentCycleExecutionRequestV078)
    (h : SubsequentCycleExecutionRequestV078Valid r) :
    ¬ r.executionAuthorityGranted ∧ ¬ r.executionStarted := by
  exact ⟨h.execution_authority_not_granted, h.execution_not_started⟩

end KuuOS.PlanOS
