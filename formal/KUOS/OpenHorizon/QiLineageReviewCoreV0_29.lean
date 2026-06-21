import Mathlib

namespace KUOS.OpenHorizon

structure QiLineageReviewCoreV029 where
  holdVisible : Bool
  reobserveVisible : Bool
  reviewVisible : Bool
  nonExecuting : Bool
  noActivation : Bool
  holdRequired : holdVisible = true
  reobserveRequired : reobserveVisible = true
  reviewRequired : reviewVisible = true
  boundedRequired : nonExecuting = true
  activationRequired : noActivation = true

namespace QiCandidateLineageBinding

theorem review_core_is_bounded (r : QiLineageReviewCoreV029) :
    r.holdVisible = true ∧
      r.reobserveVisible = true ∧
      r.reviewVisible = true ∧
      r.nonExecuting = true ∧
      r.noActivation = true := by
  exact ⟨r.holdRequired, r.reobserveRequired,
    r.reviewRequired, r.boundedRequired,
    r.activationRequired⟩

end QiCandidateLineageBinding

end KUOS.OpenHorizon
