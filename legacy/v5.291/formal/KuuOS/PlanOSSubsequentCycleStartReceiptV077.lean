import KuuOS.PlanOSV076

namespace KuuOS.PlanOS

structure SubsequentCycleStartReceiptV077 where
  sourceStartRequestPreserved : Prop
  selectedCandidateEvidencePreserved : Prop
  admissionEvidencePreserved : Prop
  startScopePreserved : Prop
  startConstraintsPreserved : Prop
  startRequested : Prop
  cycleStarted : Prop
  executionRequested : Prop

structure SubsequentCycleStartReceiptV077Valid
    (r : SubsequentCycleStartReceiptV077) : Prop where
  source_start_request_preserved : r.sourceStartRequestPreserved
  selected_candidate_evidence_preserved : r.selectedCandidateEvidencePreserved
  admission_evidence_preserved : r.admissionEvidencePreserved
  start_scope_preserved : r.startScopePreserved
  start_constraints_preserved : r.startConstraintsPreserved
  start_requested : r.startRequested
  cycle_started : r.cycleStarted
  execution_not_requested : ¬ r.executionRequested

 theorem subsequentCycleStartReceiptV077_preservesEvidence
    (r : SubsequentCycleStartReceiptV077)
    (h : SubsequentCycleStartReceiptV077Valid r) :
    r.sourceStartRequestPreserved ∧
    r.selectedCandidateEvidencePreserved ∧
    r.admissionEvidencePreserved := by
  exact ⟨h.source_start_request_preserved,
    h.selected_candidate_evidence_preserved,
    h.admission_evidence_preserved⟩

 theorem subsequentCycleStartReceiptV077_startsCycle
    (r : SubsequentCycleStartReceiptV077)
    (h : SubsequentCycleStartReceiptV077Valid r) :
    r.startRequested ∧ r.cycleStarted := by
  exact ⟨h.start_requested, h.cycle_started⟩

 theorem subsequentCycleStartReceiptV077_doesNotRequestExecution
    (r : SubsequentCycleStartReceiptV077)
    (h : SubsequentCycleStartReceiptV077Valid r) :
    ¬ r.executionRequested := by
  exact h.execution_not_requested

end KuuOS.PlanOS
