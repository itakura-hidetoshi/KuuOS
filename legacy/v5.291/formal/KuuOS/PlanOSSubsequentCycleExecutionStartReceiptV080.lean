import KuuOS.PlanOSV079

namespace KuuOS.PlanOS

structure SubsequentCycleExecutionStartReceiptV080 where
  sourceExecutionAuthorizationGrantPreserved : Prop
  selectedCandidateEvidencePreserved : Prop
  admissionEvidencePreserved : Prop
  startEvidencePreserved : Prop
  executionEvidencePreserved : Prop
  executionRequested : Prop
  executionAuthorityGranted : Prop
  executionStarted : Prop
  executionCompleted : Prop

structure SubsequentCycleExecutionStartReceiptV080Valid
    (r : SubsequentCycleExecutionStartReceiptV080) : Prop where
  source_execution_authorization_grant_preserved :
    r.sourceExecutionAuthorizationGrantPreserved
  selected_candidate_evidence_preserved : r.selectedCandidateEvidencePreserved
  admission_evidence_preserved : r.admissionEvidencePreserved
  start_evidence_preserved : r.startEvidencePreserved
  execution_evidence_preserved : r.executionEvidencePreserved
  execution_requested : r.executionRequested
  execution_authority_granted : r.executionAuthorityGranted
  execution_started : r.executionStarted
  execution_not_completed : ¬ r.executionCompleted

theorem subsequentCycleExecutionStartReceiptV080_preservesEvidence
    (r : SubsequentCycleExecutionStartReceiptV080)
    (h : SubsequentCycleExecutionStartReceiptV080Valid r) :
    r.sourceExecutionAuthorizationGrantPreserved ∧
    r.selectedCandidateEvidencePreserved ∧
    r.admissionEvidencePreserved ∧
    r.startEvidencePreserved ∧
    r.executionEvidencePreserved := by
  exact ⟨h.source_execution_authorization_grant_preserved,
    h.selected_candidate_evidence_preserved,
    h.admission_evidence_preserved,
    h.start_evidence_preserved,
    h.execution_evidence_preserved⟩

theorem subsequentCycleExecutionStartReceiptV080_startsExecution
    (r : SubsequentCycleExecutionStartReceiptV080)
    (h : SubsequentCycleExecutionStartReceiptV080Valid r) :
    r.executionRequested ∧ r.executionAuthorityGranted ∧ r.executionStarted := by
  exact ⟨h.execution_requested, h.execution_authority_granted, h.execution_started⟩

theorem subsequentCycleExecutionStartReceiptV080_doesNotCompleteExecution
    (r : SubsequentCycleExecutionStartReceiptV080)
    (h : SubsequentCycleExecutionStartReceiptV080Valid r) :
    ¬ r.executionCompleted := by
  exact h.execution_not_completed

end KuuOS.PlanOS
