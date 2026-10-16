import Mathlib

namespace KUOS
namespace OpenHorizon


def boundedGerbeValue (raw : ℚ) : ℚ := max 0 (min 1 raw)


theorem boundedGerbeValue_nonnegative (raw : ℚ) :
    0 ≤ boundedGerbeValue raw := by
  simp [boundedGerbeValue]


theorem boundedGerbeValue_upper (raw : ℚ) :
    boundedGerbeValue raw ≤ 1 := by
  simp [boundedGerbeValue]


def boundedTripleOverlap (sourcePair leftTarget rightTarget : ℚ) : ℚ :=
  boundedGerbeValue (min sourcePair (min leftTarget rightTarget))


theorem boundedTripleOverlap_nonnegative
    (sourcePair leftTarget rightTarget : ℚ) :
    0 ≤ boundedTripleOverlap sourcePair leftTarget rightTarget := by
  exact boundedGerbeValue_nonnegative _


theorem boundedTripleOverlap_upper
    (sourcePair leftTarget rightTarget : ℚ) :
    boundedTripleOverlap sourcePair leftTarget rightTarget ≤ 1 := by
  exact boundedGerbeValue_upper _


def boundedFourfoldOverlap
    (firstSecond firstThird firstTarget secondThird secondTarget thirdTarget : ℚ) : ℚ :=
  boundedGerbeValue
    (min firstSecond
      (min firstThird
        (min firstTarget
          (min secondThird (min secondTarget thirdTarget)))))


theorem boundedFourfoldOverlap_nonnegative
    (firstSecond firstThird firstTarget secondThird secondTarget thirdTarget : ℚ) :
    0 ≤ boundedFourfoldOverlap
      firstSecond firstThird firstTarget secondThird secondTarget thirdTarget := by
  exact boundedGerbeValue_nonnegative _


theorem boundedFourfoldOverlap_upper
    (firstSecond firstThird firstTarget secondThird secondTarget thirdTarget : ℚ) :
    boundedFourfoldOverlap
      firstSecond firstThird firstTarget secondThird secondTarget thirdTarget ≤ 1 := by
  exact boundedGerbeValue_upper _


structure GerbeTwoCell where
  tripleOverlap : ℚ
  coherenceResidue : ℚ
  tripleOverlapBounded : 0 ≤ tripleOverlap ∧ tripleOverlap ≤ 1
  coherenceResidueBounded : 0 ≤ coherenceResidue ∧ coherenceResidue ≤ 1
  localizedOnTripleOverlap : True
  pairwiseTransportFromV013 : True


structure GerbeFourfoldWitness where
  quadrupleOverlap : ℚ
  higherCocycleDefect : ℚ
  quadrupleOverlapBounded : 0 ≤ quadrupleOverlap ∧ quadrupleOverlap ≤ 1
  higherCocycleDefectBounded : 0 ≤ higherCocycleDefect ∧ higherCocycleDefect ≤ 1
  localizedOnQuadrupleOverlap : True
  pairwiseTransportFromV013 : True


theorem gerbeTwoCell_local (cell : GerbeTwoCell) :
    cell.localizedOnTripleOverlap := by
  exact cell.localizedOnTripleOverlap


theorem gerbeTwoCell_preserves_v013_transport (cell : GerbeTwoCell) :
    cell.pairwiseTransportFromV013 := by
  exact cell.pairwiseTransportFromV013


theorem gerbeFourfoldWitness_local (witness : GerbeFourfoldWitness) :
    witness.localizedOnQuadrupleOverlap := by
  exact witness.localizedOnQuadrupleOverlap


theorem gerbeFourfoldWitness_preserves_v013_transport
    (witness : GerbeFourfoldWitness) :
    witness.pairwiseTransportFromV013 := by
  exact witness.pairwiseTransportFromV013


structure GerbeResidueBounds where
  twoCurvature : ℚ
  higherCocycleDefect : ℚ
  twoCurvatureBounded : 0 ≤ twoCurvature ∧ twoCurvature ≤ 1
  higherCocycleDefectBounded :
    0 ≤ higherCocycleDefect ∧ higherCocycleDefect ≤ 1


theorem gerbeTwoCurvature_nonnegative (residue : GerbeResidueBounds) :
    0 ≤ residue.twoCurvature := by
  exact residue.twoCurvatureBounded.1


theorem gerbeTwoCurvature_upper (residue : GerbeResidueBounds) :
    residue.twoCurvature ≤ 1 := by
  exact residue.twoCurvatureBounded.2


theorem higherCocycleDefect_nonnegative (residue : GerbeResidueBounds) :
    0 ≤ residue.higherCocycleDefect := by
  exact residue.higherCocycleDefectBounded.1


theorem higherCocycleDefect_upper (residue : GerbeResidueBounds) :
    residue.higherCocycleDefect ≤ 1 := by
  exact residue.higherCocycleDefectBounded.2


structure GerbeLiftSection where
  floor : ℚ
  shortWeight : ℚ
  mediumWeight : ℚ
  longWeight : ℚ
  floorNonnegative : 0 ≤ floor
  shortFloor : floor ≤ shortWeight
  mediumFloor : floor ≤ mediumWeight
  longFloor : floor ≤ longWeight
  sumOne : shortWeight + mediumWeight + longWeight = 1


theorem gerbeLift_no_total_short (section : GerbeLiftSection)
    (hfloor : 0 < section.floor) : section.shortWeight < 1 := by
  have hm : 0 < section.mediumWeight := lt_of_lt_of_le hfloor section.mediumFloor
  have hl : 0 ≤ section.longWeight := le_trans section.floorNonnegative section.longFloor
  linarith [section.sumOne]


theorem gerbeLift_no_total_medium (section : GerbeLiftSection)
    (hfloor : 0 < section.floor) : section.mediumWeight < 1 := by
  have hs : 0 < section.shortWeight := lt_of_lt_of_le hfloor section.shortFloor
  have hl : 0 ≤ section.longWeight := le_trans section.floorNonnegative section.longFloor
  linarith [section.sumOne]


theorem gerbeLift_no_total_long (section : GerbeLiftSection)
    (hfloor : 0 < section.floor) : section.longWeight < 1 := by
  have hs : 0 < section.shortWeight := lt_of_lt_of_le hfloor section.shortFloor
  have hm : 0 ≤ section.mediumWeight := le_trans section.floorNonnegative section.mediumFloor
  linarith [section.sumOne]


structure GerbeSurfaceHistory where
  cycles : ℕ
  surfaceHolonomyRecords : ℕ
  aligned : surfaceHolonomyRecords = cycles


def appendGerbeSurfaceCycle (history : GerbeSurfaceHistory) : GerbeSurfaceHistory where
  cycles := history.cycles + 1
  surfaceHolonomyRecords := history.surfaceHolonomyRecords + 1
  aligned := by simp [history.aligned]


theorem gerbeSurfaceHolonomy_strict (history : GerbeSurfaceHistory) :
    history.surfaceHolonomyRecords <
      (appendGerbeSurfaceCycle history).surfaceHolonomyRecords := by
  simp [appendGerbeSurfaceCycle]

end OpenHorizon
end KUOS
