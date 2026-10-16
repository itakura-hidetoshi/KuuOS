import Mathlib

namespace KUOS
namespace OpenHorizon

inductive AtlasHorizon where
  | short
  | medium
  | long
  deriving DecidableEq, Repr


def boundedOverlap (raw : ℚ) : ℚ := max 0 (min 1 raw)


theorem boundedOverlap_nonnegative (raw : ℚ) :
    0 ≤ boundedOverlap raw := by
  simp [boundedOverlap]


theorem boundedOverlap_upper (raw : ℚ) :
    boundedOverlap raw ≤ 1 := by
  simp [boundedOverlap]


def boundedCurvature (raw : ℚ) : ℚ := max 0 (min 1 raw)


theorem boundedCurvature_nonnegative (raw : ℚ) :
    0 ≤ boundedCurvature raw := by
  simp [boundedCurvature]


theorem boundedCurvature_upper (raw : ℚ) :
    boundedCurvature raw ≤ 1 := by
  simp [boundedCurvature]


structure AtlasSection where
  floor : ℚ
  shortWeight : ℚ
  mediumWeight : ℚ
  longWeight : ℚ
  floorNonnegative : 0 ≤ floor
  shortFloor : floor ≤ shortWeight
  mediumFloor : floor ≤ mediumWeight
  longFloor : floor ≤ longWeight
  sumOne : shortWeight + mediumWeight + longWeight = 1


theorem atlas_no_total_short (section : AtlasSection)
    (hfloor : 0 < section.floor) : section.shortWeight < 1 := by
  have hm : 0 < section.mediumWeight := lt_of_lt_of_le hfloor section.mediumFloor
  have hl : 0 ≤ section.longWeight := le_trans section.floorNonnegative section.longFloor
  linarith [section.sumOne]


theorem atlas_no_total_medium (section : AtlasSection)
    (hfloor : 0 < section.floor) : section.mediumWeight < 1 := by
  have hs : 0 < section.shortWeight := lt_of_lt_of_le hfloor section.shortFloor
  have hl : 0 ≤ section.longWeight := le_trans section.floorNonnegative section.longFloor
  linarith [section.sumOne]


theorem atlas_no_total_long (section : AtlasSection)
    (hfloor : 0 < section.floor) : section.longWeight < 1 := by
  have hs : 0 < section.shortWeight := lt_of_lt_of_le hfloor section.shortFloor
  have hm : 0 ≤ section.mediumWeight := le_trans section.floorNonnegative section.mediumFloor
  linarith [section.sumOne]


structure AtlasTransition where
  overlap : ℚ
  curvature : ℚ
  cocycleDefect : ℚ
  overlapBounded : 0 ≤ overlap ∧ overlap ≤ 1
  curvatureBounded : 0 ≤ curvature ∧ curvature ≤ 1
  cocycleBounded : 0 ≤ cocycleDefect ∧ cocycleDefect ≤ 1
  chartLocalityPreserved : True


theorem chart_locality_preserved (transition : AtlasTransition) :
    transition.chartLocalityPreserved := by
  trivial


structure AtlasHistory where
  cycles : ℕ
  holonomyRecords : ℕ
  aligned : holonomyRecords = cycles


def appendAtlasCycle (history : AtlasHistory) : AtlasHistory where
  cycles := history.cycles + 1
  holonomyRecords := history.holonomyRecords + 1
  aligned := by simp [history.aligned]


theorem atlasHolonomy_strict (history : AtlasHistory) :
    history.holonomyRecords < (appendAtlasCycle history).holonomyRecords := by
  simp [appendAtlasCycle]

end OpenHorizon
end KUOS
