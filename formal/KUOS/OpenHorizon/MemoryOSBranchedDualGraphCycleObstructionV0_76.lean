import Mathlib
import KUOS.OpenHorizon.MemoryOSDualCellChainDefectLocalizationV0_75

namespace KUOS.OpenHorizon.MemoryOSBranchedDualGraphCycleObstructionV0_76

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSDualCellChainDefectLocalizationV0_75

structure DualDiamond (G : Type*) [Group G] where
  j01 : G
  j13 : G
  j02 : G
  j23 : G

def upperPath {G : Type*} [Group G] (diamond : DualDiamond G) : G :=
  diamond.j01 * diamond.j13

def lowerPath {G : Type*} [Group G] (diamond : DualDiamond G) : G :=
  diamond.j02 * diamond.j23

def cycleObstruction {G : Type*} [Group G] (diamond : DualDiamond G) : G :=
  upperPath diamond * (lowerPath diamond)⁻¹

def PathsAgree {G : Type*} [Group G] (diamond : DualDiamond G) : Prop :=
  upperPath diamond = lowerPath diamond

theorem paths_agree_iff_cycle_obstruction_identity
    {G : Type*} [Group G] (diamond : DualDiamond G) :
    PathsAgree diamond ↔ cycleObstruction diamond = 1 := by
  unfold PathsAgree cycleObstruction
  constructor
  · intro h
    rw [h]
    simp
  · intro h
    have h' := congrArg (fun value => value * lowerPath diamond) h
    simpa [mul_assoc] using h'

def upperLocalizedDefect {G : Type*} [Group G]
    (diamond : DualDiamond G) (defect : G) : G :=
  upperPath diamond * defect * (upperPath diamond)⁻¹

def lowerLocalizedDefect {G : Type*} [Group G]
    (diamond : DualDiamond G) (defect : G) : G :=
  lowerPath diamond * defect * (lowerPath diamond)⁻¹

theorem upper_lower_localizations_related
    {G : Type*} [Group G] (diamond : DualDiamond G) (defect : G) :
    upperLocalizedDefect diamond defect =
      cycleObstruction diamond * lowerLocalizedDefect diamond defect *
        (cycleObstruction diamond)⁻¹ := by
  unfold upperLocalizedDefect lowerLocalizedDefect cycleObstruction
  group

theorem path_agreement_implies_localization_agreement
    {G : Type*} [Group G] (diamond : DualDiamond G) (defect : G)
    (h : PathsAgree diamond) :
    upperLocalizedDefect diamond defect =
      lowerLocalizedDefect diamond defect := by
  unfold PathsAgree at h
  unfold upperLocalizedDefect lowerLocalizedDefect
  rw [h]

structure DiamondGaugeFrame (G : Type*) [Group G] where
  g0 : G
  g1 : G
  g2 : G
  g3 : G

def gaugeTransformDiamond {G : Type*} [Group G]
    (diamond : DualDiamond G) (frame : DiamondGaugeFrame G) :
    DualDiamond G :=
  {
    j01 := frame.g0⁻¹ * diamond.j01 * frame.g1
    j13 := frame.g1⁻¹ * diamond.j13 * frame.g3
    j02 := frame.g0⁻¹ * diamond.j02 * frame.g2
    j23 := frame.g2⁻¹ * diamond.j23 * frame.g3
  }

theorem upper_path_gauge_covariant
    {G : Type*} [Group G]
    (diamond : DualDiamond G) (frame : DiamondGaugeFrame G) :
    upperPath (gaugeTransformDiamond diamond frame) =
      frame.g0⁻¹ * upperPath diamond * frame.g3 := by
  unfold upperPath gaugeTransformDiamond
  group

theorem lower_path_gauge_covariant
    {G : Type*} [Group G]
    (diamond : DualDiamond G) (frame : DiamondGaugeFrame G) :
    lowerPath (gaugeTransformDiamond diamond frame) =
      frame.g0⁻¹ * lowerPath diamond * frame.g3 := by
  unfold lowerPath gaugeTransformDiamond
  group

theorem cycle_obstruction_gauge_covariant
    {G : Type*} [Group G]
    (diamond : DualDiamond G) (frame : DiamondGaugeFrame G) :
    cycleObstruction (gaugeTransformDiamond diamond frame) =
      frame.g0⁻¹ * cycleObstruction diamond * frame.g0 := by
  unfold cycleObstruction
  rw [upper_path_gauge_covariant, lower_path_gauge_covariant]
  group

def gaugeTransformTargetDefect {G : Type*} [Group G]
    (defect : G) (frame : DiamondGaugeFrame G) : G :=
  frame.g3⁻¹ * defect * frame.g3

theorem upper_localized_defect_gauge_covariant
    {G : Type*} [Group G]
    (diamond : DualDiamond G) (defect : G) (frame : DiamondGaugeFrame G) :
    upperLocalizedDefect (gaugeTransformDiamond diamond frame)
        (gaugeTransformTargetDefect defect frame) =
      frame.g0⁻¹ * upperLocalizedDefect diamond defect * frame.g0 := by
  unfold upperLocalizedDefect gaugeTransformTargetDefect
  rw [upper_path_gauge_covariant]
  group

theorem lower_localized_defect_gauge_covariant
    {G : Type*} [Group G]
    (diamond : DualDiamond G) (defect : G) (frame : DiamondGaugeFrame G) :
    lowerLocalizedDefect (gaugeTransformDiamond diamond frame)
        (gaugeTransformTargetDefect defect frame) =
      frame.g0⁻¹ * lowerLocalizedDefect diamond defect * frame.g0 := by
  unfold lowerLocalizedDefect gaugeTransformTargetDefect
  rw [lower_path_gauge_covariant]
  group

def cycleObstructionWilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (diamond : DualDiamond G) : R :=
  χ.toFun (cycleObstruction diamond)

theorem cycle_obstruction_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (diamond : DualDiamond G) (frame : DiamondGaugeFrame G) :
    cycleObstructionWilson χ (gaugeTransformDiamond diamond frame) =
      cycleObstructionWilson χ diamond := by
  unfold cycleObstructionWilson
  rw [cycle_obstruction_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (cycleObstruction diamond)

def upperRouteWilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (diamond : DualDiamond G) (defect : G) : R :=
  χ.toFun (upperLocalizedDefect diamond defect)

def lowerRouteWilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (diamond : DualDiamond G) (defect : G) : R :=
  χ.toFun (lowerLocalizedDefect diamond defect)

theorem route_wilson_signature_equal
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (diamond : DualDiamond G) (defect : G) :
    upperRouteWilson χ diamond defect =
      lowerRouteWilson χ diamond defect := by
  unfold upperRouteWilson lowerRouteWilson
  rw [upper_lower_localizations_related]
  simpa using
    χ.conjugationInvariant (cycleObstruction diamond)⁻¹
      (lowerLocalizedDefect diamond defect)

theorem upper_route_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (diamond : DualDiamond G) (defect : G) (frame : DiamondGaugeFrame G) :
    upperRouteWilson χ (gaugeTransformDiamond diamond frame)
        (gaugeTransformTargetDefect defect frame) =
      upperRouteWilson χ diamond defect := by
  unfold upperRouteWilson
  rw [upper_localized_defect_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0
    (upperLocalizedDefect diamond defect)

def routeObstructionPenalty {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale : ℚ)
    (diamond : DualDiamond G) : ℚ :=
  (maxValue - cycleObstructionWilson χ diamond) / scale

theorem route_obstruction_penalty_gauge_invariant
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale : ℚ)
    (diamond : DualDiamond G) (frame : DiamondGaugeFrame G) :
    routeObstructionPenalty χ maxValue scale
        (gaugeTransformDiamond diamond frame) =
      routeObstructionPenalty χ maxValue scale diamond := by
  unfold routeObstructionPenalty
  rw [cycle_obstruction_wilson_gauge_invariant]

def branchedGraphAdjustedConfidence {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (diamond : DualDiamond G) : ℚ :=
  base - routeObstructionPenalty χ maxValue scale diamond

theorem branched_graph_adjusted_confidence_gauge_invariant
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (diamond : DualDiamond G) (frame : DiamondGaugeFrame G) :
    branchedGraphAdjustedConfidence χ maxValue scale base
        (gaugeTransformDiamond diamond frame) =
      branchedGraphAdjustedConfidence χ maxValue scale base diamond := by
  unfold branchedGraphAdjustedConfidence
  rw [route_obstruction_penalty_gauge_invariant]

theorem branched_graph_adjusted_confidence_mem_unit_interval
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (diamond : DualDiamond G)
    (hbase0 : 0 ≤ base) (hbase1 : base ≤ 1)
    (hpenalty0 : 0 ≤ routeObstructionPenalty χ maxValue scale diamond)
    (hpenalty :
      routeObstructionPenalty χ maxValue scale diamond ≤ base) :
    branchedGraphAdjustedConfidence χ maxValue scale base diamond ∈
      Set.Icc (0 : ℚ) 1 := by
  unfold branchedGraphAdjustedConfidence
  constructor <;> linarith

def flatDiamond : DualDiamond S3 :=
  {
    j01 := swap01
    j13 := swap12
    j02 := 1
    j23 := swap01 * swap12
  }

def obstructedDiamond : DualDiamond S3 :=
  {
    j01 := 1
    j13 := 1
    j02 := swap01
    j23 := 1
  }

def canonicalTargetDefect : S3 :=
  swap12 * swap01

def canonicalConjugateTargetDefect : S3 :=
  swap01 * canonicalTargetDefect * swap01

theorem canonical_flat_paths_agree :
    PathsAgree flatDiamond := by
  native_decide

theorem canonical_flat_cycle_obstruction :
    cycleObstruction flatDiamond = 1 := by
  native_decide

theorem canonical_obstructed_paths_disagree :
    ¬ PathsAgree obstructedDiamond := by
  native_decide

theorem canonical_obstructed_cycle_obstruction :
    cycleObstruction obstructedDiamond = swap01 := by
  native_decide

theorem canonical_obstructed_upper_localization :
    upperLocalizedDefect obstructedDiamond canonicalTargetDefect =
      canonicalTargetDefect := by
  native_decide

theorem canonical_obstructed_lower_localization :
    lowerLocalizedDefect obstructedDiamond canonicalTargetDefect =
      canonicalConjugateTargetDefect := by
  native_decide

theorem canonical_obstructed_route_representatives_differ :
    upperLocalizedDefect obstructedDiamond canonicalTargetDefect ≠
      lowerLocalizedDefect obstructedDiamond canonicalTargetDefect := by
  native_decide

theorem canonical_obstructed_route_wilson_limitation :
    upperRouteWilson (identityWilsonClass S3) obstructedDiamond
        canonicalTargetDefect =
      lowerRouteWilson (identityWilsonClass S3) obstructedDiamond
        canonicalTargetDefect := by
  exact route_wilson_signature_equal
    (identityWilsonClass S3) obstructedDiamond canonicalTargetDefect

theorem canonical_flat_cycle_wilson :
    cycleObstructionWilson (identityWilsonClass S3) flatDiamond = 3 := by
  native_decide

theorem canonical_obstructed_cycle_wilson :
    cycleObstructionWilson (identityWilsonClass S3) obstructedDiamond = 1 := by
  native_decide

theorem canonical_flat_route_penalty :
    routeObstructionPenalty (identityWilsonClass S3) 3 18 flatDiamond = 0 := by
  native_decide

theorem canonical_obstructed_route_penalty :
    routeObstructionPenalty (identityWilsonClass S3) 3 18
      obstructedDiamond = 1 / 9 := by
  native_decide

theorem canonical_flat_adjusted_confidence :
    branchedGraphAdjustedConfidence (identityWilsonClass S3) 3 18 (1 / 3)
      flatDiamond = 1 / 3 := by
  native_decide

theorem canonical_obstructed_adjusted_confidence :
    branchedGraphAdjustedConfidence (identityWilsonClass S3) 3 18 (1 / 3)
      obstructedDiamond = 2 / 9 := by
  native_decide

structure BranchedDualGraphCycleObstructionCertificate where
  sourceMemoryOSV075Bound : Bool
  finiteDiamondExact : Bool
  spanningTreeTransportExact : Bool
  pathAgreementCycleCriterionExact : Bool
  routeObstructionGaugeCovariant : Bool
  routedDefectConjugacyExact : Bool
  routeWilsonLimitationRecorded : Bool
  continuumDualGraphClaimed : Bool
  physicalGaugeFieldInferenceClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSBranchedDualGraphCycleObstructionV0_76
