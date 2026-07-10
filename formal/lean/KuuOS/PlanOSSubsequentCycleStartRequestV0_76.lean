namespace KuuOS

structure PlanOSSubsequentCycleStartRequestV0_76 where
  selectedCandidateEvidencePreserved : Prop
  admissionRequestPreserved : Prop
  admissionGrantPreserved : Prop
  startRequestRecorded : Prop
  subsequentCycleStarted : Prop
  historyAppendCount : Nat

structure PlanOSSubsequentCycleStartRequestAssumptionsV0_76
    (s : PlanOSSubsequentCycleStartRequestV0_76) : Prop where
  selectedCandidateEvidencePreserved : s.selectedCandidateEvidencePreserved
  admissionRequestPreserved : s.admissionRequestPreserved
  admissionGrantPreserved : s.admissionGrantPreserved
  startRequestRecorded : s.startRequestRecorded
  subsequentCycleNotStarted : ¬ s.subsequentCycleStarted
  historyAppendExactlyOne : s.historyAppendCount = 1

theorem planos_v0_76_preserves_selected_candidate_evidence
    (s : PlanOSSubsequentCycleStartRequestV0_76)
    (h : PlanOSSubsequentCycleStartRequestAssumptionsV0_76 s) :
    s.selectedCandidateEvidencePreserved := h.selectedCandidateEvidencePreserved

theorem planos_v0_76_requires_admission_grant
    (s : PlanOSSubsequentCycleStartRequestV0_76)
    (h : PlanOSSubsequentCycleStartRequestAssumptionsV0_76 s) :
    s.admissionRequestPreserved ∧ s.admissionGrantPreserved :=
  ⟨h.admissionRequestPreserved, h.admissionGrantPreserved⟩

theorem planos_v0_76_records_bounded_start_request
    (s : PlanOSSubsequentCycleStartRequestV0_76)
    (h : PlanOSSubsequentCycleStartRequestAssumptionsV0_76 s) :
    s.startRequestRecorded ∧ s.historyAppendCount = 1 :=
  ⟨h.startRequestRecorded, h.historyAppendExactlyOne⟩

theorem planos_v0_76_does_not_start_cycle
    (s : PlanOSSubsequentCycleStartRequestV0_76)
    (h : PlanOSSubsequentCycleStartRequestAssumptionsV0_76 s) :
    ¬ s.subsequentCycleStarted := h.subsequentCycleNotStarted

end KuuOS
