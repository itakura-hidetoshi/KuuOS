import KUOS.PlanOS.SubsequentCycleAdmissionRequestV0_74

namespace KUOS.PlanOS

structure SubsequentCycleAdmissionGrantV0_75 where
  selectedCandidatePreserved : Prop
  admissionRequestPreserved : Prop
  admissionGranted : Prop
  subsequentCycleStarted : Prop
  hSelectedCandidatePreserved : selectedCandidatePreserved
  hAdmissionRequestPreserved : admissionRequestPreserved
  hAdmissionGranted : admissionGranted
  hSubsequentCycleNotStarted : ¬ subsequentCycleStarted

 theorem subsequentCycleAdmissionGrantV0_75_is_bounded
    (g : SubsequentCycleAdmissionGrantV0_75) :
    g.selectedCandidatePreserved ∧
    g.admissionRequestPreserved ∧
    g.admissionGranted ∧
    ¬ g.subsequentCycleStarted := by
  exact ⟨g.hSelectedCandidatePreserved,
    g.hAdmissionRequestPreserved,
    g.hAdmissionGranted,
    g.hSubsequentCycleNotStarted⟩

end KUOS.PlanOS
