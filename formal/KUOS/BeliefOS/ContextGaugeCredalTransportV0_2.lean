import Mathlib
import KUOS.BeliefOS.RelationalConditionalKernelV0_1

namespace KUOS
namespace BeliefOS

structure TransportReliability where
  value : ℝ
  nonnegative : 0 ≤ value
  atMostOne : value ≤ 1


def transportedLower
    (reliability : TransportReliability)
    (interval : CredalInterval) : ℝ :=
  reliability.value * interval.lower


def transportedUpper
    (reliability : TransportReliability)
    (interval : CredalInterval) : ℝ :=
  reliability.value * interval.upper + (1 - reliability.value)


theorem transportedLower_nonnegative
    (reliability : TransportReliability)
    (interval : CredalInterval) :
    0 ≤ transportedLower reliability interval := by
  exact mul_nonneg reliability.nonnegative interval.lowerNonnegative


theorem transportedLower_le_source
    (reliability : TransportReliability)
    (interval : CredalInterval) :
    transportedLower reliability interval ≤ interval.lower := by
  unfold transportedLower
  have h := mul_le_mul_of_nonneg_right reliability.atMostOne interval.lowerNonnegative
  simpa using h


theorem source_le_transportedUpper
    (reliability : TransportReliability)
    (interval : CredalInterval) :
    interval.upper ≤ transportedUpper reliability interval := by
  unfold transportedUpper
  have hnonneg : 0 ≤ 1 - reliability.value := sub_nonneg.mpr reliability.atMostOne
  have hmul := mul_le_mul_of_nonneg_left interval.upperAtMostOne hnonneg
  nlinarith


theorem transportedUpper_le_one
    (reliability : TransportReliability)
    (interval : CredalInterval) :
    transportedUpper reliability interval ≤ 1 := by
  unfold transportedUpper
  have hmul := mul_le_mul_of_nonneg_left interval.upperAtMostOne reliability.nonnegative
  nlinarith


theorem transported_interval_ordered
    (reliability : TransportReliability)
    (interval : CredalInterval) :
    transportedLower reliability interval ≤ transportedUpper reliability interval := by
  exact le_trans
    (transportedLower_le_source reliability interval)
    (le_trans interval.ordered (source_le_transportedUpper reliability interval))


def transportCredalInterval
    (reliability : TransportReliability)
    (interval : CredalInterval) : CredalInterval where
  lower := transportedLower reliability interval
  upper := transportedUpper reliability interval
  lowerNonnegative := transportedLower_nonnegative reliability interval
  ordered := transported_interval_ordered reliability interval
  upperAtMostOne := transportedUpper_le_one reliability interval


theorem transportCredalInterval_is_conservative_lower
    (reliability : TransportReliability)
    (interval : CredalInterval) :
    (transportCredalInterval reliability interval).lower ≤ interval.lower := by
  exact transportedLower_le_source reliability interval


theorem transportCredalInterval_is_conservative_upper
    (reliability : TransportReliability)
    (interval : CredalInterval) :
    interval.upper ≤ (transportCredalInterval reliability interval).upper := by
  exact source_le_transportedUpper reliability interval


def credalHull (left right : CredalInterval) : CredalInterval where
  lower := min left.lower right.lower
  upper := max left.upper right.upper
  lowerNonnegative := by
    exact le_min left.lowerNonnegative right.lowerNonnegative
  ordered := by
    calc
      min left.lower right.lower ≤ left.lower := min_le_left _ _
      _ ≤ left.upper := left.ordered
      _ ≤ max left.upper right.upper := le_max_left _ _
  upperAtMostOne := by
    exact max_le left.upperAtMostOne right.upperAtMostOne


theorem credalHull_contains_left_lower
    (left right : CredalInterval) :
    (credalHull left right).lower ≤ left.lower := by
  exact min_le_left _ _


theorem credalHull_contains_left_upper
    (left right : CredalInterval) :
    left.upper ≤ (credalHull left right).upper := by
  exact le_max_left _ _


theorem credalHull_contains_right_lower
    (left right : CredalInterval) :
    (credalHull left right).lower ≤ right.lower := by
  exact min_le_right _ _


theorem credalHull_contains_right_upper
    (left right : CredalInterval) :
    right.upper ≤ (credalHull left right).upper := by
  exact le_max_right _ _


structure ContextGaugeBeliefBoundary where
  localityPreserved : Bool
  pluralityPreserved : Bool
  pathSearchUsed : Bool
  globalWinnerSelected : Bool
  globalTruthGranted : Bool
  localityRequired : localityPreserved = true
  pluralityRequired : pluralityPreserved = true
  pathSearchForbidden : pathSearchUsed = false
  globalWinnerForbidden : globalWinnerSelected = false
  globalTruthForbidden : globalTruthGranted = false


theorem contextGaugeBelief_preserves_locality
    (boundary : ContextGaugeBeliefBoundary) :
    boundary.localityPreserved = true := by
  exact boundary.localityRequired


theorem contextGaugeBelief_preserves_plurality
    (boundary : ContextGaugeBeliefBoundary) :
    boundary.pluralityPreserved = true := by
  exact boundary.pluralityRequired


theorem contextGaugeBelief_does_not_search_global_path
    (boundary : ContextGaugeBeliefBoundary) :
    boundary.pathSearchUsed = false := by
  exact boundary.pathSearchForbidden


theorem contextGaugeBelief_does_not_grant_global_truth
    (boundary : ContextGaugeBeliefBoundary) :
    boundary.globalTruthGranted = false := by
  exact boundary.globalTruthForbidden


structure TransportResidualBoundary where
  curvatureVisible : Bool
  cocycleDefectVisible : Bool
  holonomyVisible : Bool
  qiHistoryResidualVisible : Bool
  residualGrantsAuthority : Bool
  curvatureRequired : curvatureVisible = true
  cocycleRequired : cocycleDefectVisible = true
  holonomyRequired : holonomyVisible = true
  qiHistoryRequired : qiHistoryResidualVisible = true
  authorityForbidden : residualGrantsAuthority = false


theorem transportResidual_does_not_grant_authority
    (boundary : TransportResidualBoundary) :
    boundary.residualGrantsAuthority = false := by
  exact boundary.authorityForbidden


structure TransportCounterevidence where
  sourceCount : ℕ
  transportedCount : ℕ
  preserved : sourceCount ≤ transportedCount


theorem transportCounterevidence_is_append_only
    (counterevidence : TransportCounterevidence) :
    counterevidence.sourceCount ≤ counterevidence.transportedCount := by
  exact counterevidence.preserved


structure BeliefTransportHistory where
  commits : ℕ
  holonomyRecords : ℕ
  aligned : holonomyRecords = commits


def appendBeliefTransport
    (history : BeliefTransportHistory) : BeliefTransportHistory where
  commits := history.commits + 1
  holonomyRecords := history.holonomyRecords + 1
  aligned := by simp [history.aligned]


theorem beliefTransportHolonomy_strict
    (history : BeliefTransportHistory) :
    history.holonomyRecords <
      (appendBeliefTransport history).holonomyRecords := by
  simp [appendBeliefTransport]


structure ReplanTransportActivation where
  candidateRoute : Bool
  missionPhaseIsReplan : Bool
  futureOnly : Bool
  memoryOverwrite : Bool
  grantsExecutionAuthority : Bool
  candidateRequired : candidateRoute = true
  replanRequired : missionPhaseIsReplan = true
  futureBounded : futureOnly = true
  overwriteForbidden : memoryOverwrite = false
  executionAuthorityForbidden : grantsExecutionAuthority = false


theorem transportActivation_requires_replan
    (receipt : ReplanTransportActivation) :
    receipt.missionPhaseIsReplan = true := by
  exact receipt.replanRequired


theorem transportActivation_is_future_only
    (receipt : ReplanTransportActivation) :
    receipt.futureOnly = true := by
  exact receipt.futureBounded


theorem transportActivation_does_not_overwrite
    (receipt : ReplanTransportActivation) :
    receipt.memoryOverwrite = false := by
  exact receipt.overwriteForbidden


theorem transportActivation_does_not_grant_execution
    (receipt : ReplanTransportActivation) :
    receipt.grantsExecutionAuthority = false := by
  exact receipt.executionAuthorityForbidden

end BeliefOS
end KUOS
