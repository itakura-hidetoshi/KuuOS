import Mathlib
import KUOS.BeliefOS.ContextGaugeCredalTransportV0_2

namespace KUOS
namespace BeliefOS

structure CoherenceDefect where
  value : ℝ
  nonnegative : 0 ≤ value
  atMostOne : value ≤ 1


def coherentLower
    (defect : CoherenceDefect)
    (interval : CredalInterval) : ℝ :=
  max 0 (interval.lower - defect.value)


def coherentUpper
    (defect : CoherenceDefect)
    (interval : CredalInterval) : ℝ :=
  min 1 (interval.upper + defect.value)


theorem coherentLower_nonnegative
    (defect : CoherenceDefect)
    (interval : CredalInterval) :
    0 ≤ coherentLower defect interval := by
  exact le_max_left _ _


theorem coherentLower_le_source
    (defect : CoherenceDefect)
    (interval : CredalInterval) :
    coherentLower defect interval ≤ interval.lower := by
  unfold coherentLower
  apply max_le
  · exact interval.lowerNonnegative
  · exact sub_le_self interval.lower defect.nonnegative


theorem source_le_coherentUpper
    (defect : CoherenceDefect)
    (interval : CredalInterval) :
    interval.upper ≤ coherentUpper defect interval := by
  unfold coherentUpper
  apply le_min
  · exact interval.upperAtMostOne
  · linarith [defect.nonnegative]


theorem coherentUpper_le_one
    (defect : CoherenceDefect)
    (interval : CredalInterval) :
    coherentUpper defect interval ≤ 1 := by
  exact min_le_left _ _


theorem coherent_interval_ordered
    (defect : CoherenceDefect)
    (interval : CredalInterval) :
    coherentLower defect interval ≤ coherentUpper defect interval := by
  exact le_trans
    (coherentLower_le_source defect interval)
    (le_trans interval.ordered (source_le_coherentUpper defect interval))


def coherenceWiden
    (defect : CoherenceDefect)
    (interval : CredalInterval) : CredalInterval where
  lower := coherentLower defect interval
  upper := coherentUpper defect interval
  lowerNonnegative := coherentLower_nonnegative defect interval
  ordered := coherent_interval_ordered defect interval
  upperAtMostOne := coherentUpper_le_one defect interval


theorem coherenceWiden_is_conservative_lower
    (defect : CoherenceDefect)
    (interval : CredalInterval) :
    (coherenceWiden defect interval).lower ≤ interval.lower := by
  exact coherentLower_le_source defect interval


theorem coherenceWiden_is_conservative_upper
    (defect : CoherenceDefect)
    (interval : CredalInterval) :
    interval.upper ≤ (coherenceWiden defect interval).upper := by
  exact source_le_coherentUpper defect interval


theorem coherenceWiden_contains_left_hull
    (defect : CoherenceDefect)
    (left right : CredalInterval) :
    (coherenceWiden defect (credalHull left right)).lower ≤ left.lower ∧
      left.upper ≤ (coherenceWiden defect (credalHull left right)).upper := by
  constructor
  · exact le_trans
      (coherenceWiden_is_conservative_lower defect (credalHull left right))
      (credalHull_contains_left_lower left right)
  · exact le_trans
      (credalHull_contains_left_upper left right)
      (coherenceWiden_is_conservative_upper defect (credalHull left right))


theorem coherenceWiden_contains_right_hull
    (defect : CoherenceDefect)
    (left right : CredalInterval) :
    (coherenceWiden defect (credalHull left right)).lower ≤ right.lower ∧
      right.upper ≤ (coherenceWiden defect (credalHull left right)).upper := by
  constructor
  · exact le_trans
      (coherenceWiden_is_conservative_lower defect (credalHull left right))
      (credalHull_contains_right_lower left right)
  · exact le_trans
      (credalHull_contains_right_upper left right)
      (coherenceWiden_is_conservative_upper defect (credalHull left right))


structure TwoCellBeliefBoundary where
  residue : CoherenceDefect
  localizedOnTripleOverlap : Bool
  sourcePathsPreserved : Bool
  residueGrantsVeto : Bool
  residueGrantsAuthority : Bool
  localizedRequired : localizedOnTripleOverlap = true
  sourcePathsRequired : sourcePathsPreserved = true
  vetoForbidden : residueGrantsVeto = false
  authorityForbidden : residueGrantsAuthority = false


theorem twoCell_residue_does_not_veto
    (boundary : TwoCellBeliefBoundary) :
    boundary.residueGrantsVeto = false := by
  exact boundary.vetoForbidden


theorem twoCell_residue_does_not_grant_authority
    (boundary : TwoCellBeliefBoundary) :
    boundary.residueGrantsAuthority = false := by
  exact boundary.authorityForbidden


structure HigherBeliefWitnessBoundary where
  defect : CoherenceDefect
  localizedOnQuadrupleOverlap : Bool
  globalTrivializationUsed : Bool
  higherDefectGrantsProhibition : Bool
  higherDefectGrantsAuthority : Bool
  localizedRequired : localizedOnQuadrupleOverlap = true
  trivializationForbidden : globalTrivializationUsed = false
  prohibitionForbidden : higherDefectGrantsProhibition = false
  authorityForbidden : higherDefectGrantsAuthority = false


theorem higherWitness_does_not_trivialize
    (boundary : HigherBeliefWitnessBoundary) :
    boundary.globalTrivializationUsed = false := by
  exact boundary.trivializationForbidden


theorem higherWitness_does_not_prohibit
    (boundary : HigherBeliefWitnessBoundary) :
    boundary.higherDefectGrantsProhibition = false := by
  exact boundary.prohibitionForbidden


theorem higherWitness_does_not_grant_authority
    (boundary : HigherBeliefWitnessBoundary) :
    boundary.higherDefectGrantsAuthority = false := by
  exact boundary.authorityForbidden


structure GerbeBeliefBoundary where
  localityPreserved : Bool
  pluralityPreserved : Bool
  twoTruthsSeparated : Bool
  paramarthaNonReified : Bool
  pathSearchUsed : Bool
  globalWinnerSelected : Bool
  globalTrivializationUsed : Bool
  localityRequired : localityPreserved = true
  pluralityRequired : pluralityPreserved = true
  twoTruthsRequired : twoTruthsSeparated = true
  nonReificationRequired : paramarthaNonReified = true
  pathSearchForbidden : pathSearchUsed = false
  globalWinnerForbidden : globalWinnerSelected = false
  trivializationForbidden : globalTrivializationUsed = false


theorem gerbeBelief_preserves_locality
    (boundary : GerbeBeliefBoundary) :
    boundary.localityPreserved = true := by
  exact boundary.localityRequired


theorem gerbeBelief_preserves_plurality
    (boundary : GerbeBeliefBoundary) :
    boundary.pluralityPreserved = true := by
  exact boundary.pluralityRequired


theorem gerbeBelief_preserves_two_truths
    (boundary : GerbeBeliefBoundary) :
    boundary.twoTruthsSeparated = true := by
  exact boundary.twoTruthsRequired


theorem gerbeBelief_is_non_reified
    (boundary : GerbeBeliefBoundary) :
    boundary.paramarthaNonReified = true := by
  exact boundary.nonReificationRequired


theorem gerbeBelief_does_not_search_paths
    (boundary : GerbeBeliefBoundary) :
    boundary.pathSearchUsed = false := by
  exact boundary.pathSearchForbidden


theorem gerbeBelief_does_not_select_global_winner
    (boundary : GerbeBeliefBoundary) :
    boundary.globalWinnerSelected = false := by
  exact boundary.globalWinnerForbidden


theorem gerbeBelief_does_not_globally_trivialize
    (boundary : GerbeBeliefBoundary) :
    boundary.globalTrivializationUsed = false := by
  exact boundary.trivializationForbidden


structure GerbeCounterevidence where
  sourceCount : ℕ
  coherentCount : ℕ
  preserved : sourceCount ≤ coherentCount


theorem gerbeCounterevidence_is_append_only
    (counterevidence : GerbeCounterevidence) :
    counterevidence.sourceCount ≤ counterevidence.coherentCount := by
  exact counterevidence.preserved


structure SurfaceHolonomyHistory where
  coherenceCommits : ℕ
  surfaceHolonomyRecords : ℕ
  aligned : surfaceHolonomyRecords = coherenceCommits


def appendSurfaceHolonomy
    (history : SurfaceHolonomyHistory) : SurfaceHolonomyHistory where
  coherenceCommits := history.coherenceCommits + 1
  surfaceHolonomyRecords := history.surfaceHolonomyRecords + 1
  aligned := by simp [history.aligned]


theorem surfaceHolonomy_strict
    (history : SurfaceHolonomyHistory) :
    history.surfaceHolonomyRecords <
      (appendSurfaceHolonomy history).surfaceHolonomyRecords := by
  simp [appendSurfaceHolonomy]


structure ReplanGerbeActivation where
  candidateRoute : Bool
  missionPhaseIsReplan : Bool
  futureOnly : Bool
  memoryOverwrite : Bool
  grantsTruthAuthority : Bool
  grantsExecutionAuthority : Bool
  candidateRequired : candidateRoute = true
  replanRequired : missionPhaseIsReplan = true
  futureBounded : futureOnly = true
  overwriteForbidden : memoryOverwrite = false
  truthAuthorityForbidden : grantsTruthAuthority = false
  executionAuthorityForbidden : grantsExecutionAuthority = false


theorem gerbeActivation_requires_replan
    (receipt : ReplanGerbeActivation) :
    receipt.missionPhaseIsReplan = true := by
  exact receipt.replanRequired


theorem gerbeActivation_is_future_only
    (receipt : ReplanGerbeActivation) :
    receipt.futureOnly = true := by
  exact receipt.futureBounded


theorem gerbeActivation_does_not_overwrite
    (receipt : ReplanGerbeActivation) :
    receipt.memoryOverwrite = false := by
  exact receipt.overwriteForbidden


theorem gerbeActivation_does_not_grant_truth
    (receipt : ReplanGerbeActivation) :
    receipt.grantsTruthAuthority = false := by
  exact receipt.truthAuthorityForbidden


theorem gerbeActivation_does_not_grant_execution
    (receipt : ReplanGerbeActivation) :
    receipt.grantsExecutionAuthority = false := by
  exact receipt.executionAuthorityForbidden

end BeliefOS
end KUOS
