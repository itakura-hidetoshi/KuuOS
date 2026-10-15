import KuuOS.PlanOSV083

namespace KuuOS.PlanOS

structure SubsequentCycleCloseoutReceiptV084 where
  sourceCloseoutRequestPreserved : Prop
  selectedCandidateEvidencePreserved : Prop
  executionCompletionEvidencePreserved : Prop
  closeoutScopePreserved : Prop
  closeoutConstraintsPreserved : Prop
  closeoutRequested : Prop
  cycleClosed : Prop
  postCloseoutReviewRequested : Prop

structure SubsequentCycleCloseoutReceiptV084Valid
    (r : SubsequentCycleCloseoutReceiptV084) : Prop where
  source_closeout_request_preserved : r.sourceCloseoutRequestPreserved
  selected_candidate_evidence_preserved : r.selectedCandidateEvidencePreserved
  execution_completion_evidence_preserved : r.executionCompletionEvidencePreserved
  closeout_scope_preserved : r.closeoutScopePreserved
  closeout_constraints_preserved : r.closeoutConstraintsPreserved
  closeout_requested : r.closeoutRequested
  cycle_closed : r.cycleClosed
  post_closeout_review_not_requested : ¬ r.postCloseoutReviewRequested

theorem subsequentCycleCloseoutReceiptV084_preservesEvidence
    (r : SubsequentCycleCloseoutReceiptV084)
    (h : SubsequentCycleCloseoutReceiptV084Valid r) :
    r.sourceCloseoutRequestPreserved ∧
    r.selectedCandidateEvidencePreserved ∧
    r.executionCompletionEvidencePreserved := by
  exact ⟨h.source_closeout_request_preserved,
    h.selected_candidate_evidence_preserved,
    h.execution_completion_evidence_preserved⟩

theorem subsequentCycleCloseoutReceiptV084_closesCycle
    (r : SubsequentCycleCloseoutReceiptV084)
    (h : SubsequentCycleCloseoutReceiptV084Valid r) :
    r.closeoutRequested ∧ r.cycleClosed := by
  exact ⟨h.closeout_requested, h.cycle_closed⟩

theorem subsequentCycleCloseoutReceiptV084_keepsReviewSeparate
    (r : SubsequentCycleCloseoutReceiptV084)
    (h : SubsequentCycleCloseoutReceiptV084Valid r) :
    ¬ r.postCloseoutReviewRequested := by
  exact h.post_closeout_review_not_requested

end KuuOS.PlanOS
