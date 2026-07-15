import Mathlib
import KUOS.OpenHorizon.MemoryOSDualCycleBasisTreeChangeV0_77

namespace KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSDualCellChainDefectLocalizationV0_75
open KUOS.OpenHorizon.MemoryOSDualCycleBasisTreeChangeV0_77

/-- A finite four-route dual atlas with a common root and target. -/
structure DualFourRouteAtlas (G : Type*) [Group G] where
  j01 : G
  j15 : G
  j02 : G
  j25 : G
  j03 : G
  j35 : G
  j04 : G
  j45 : G

def path0 {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) : G :=
  atlas.j01 * atlas.j15

def path1 {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) : G :=
  atlas.j02 * atlas.j25

def path2 {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) : G :=
  atlas.j03 * atlas.j35

def path3 {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) : G :=
  atlas.j04 * atlas.j45

/-- Route comparison holonomy. -/
def routeCycle {G : Type*} [Group G] (left right : G) : G :=
  left * right⁻¹

theorem route_cycle_refl {G : Type*} [Group G] (path : G) :
    routeCycle path path = 1 := by
  simp [routeCycle]

theorem route_cycle_symm {G : Type*} [Group G] (left right : G) :
    routeCycle right left = (routeCycle left right)⁻¹ := by
  unfold routeCycle
  group

theorem route_cycle_cocycle {G : Type*} [Group G] (first second third : G) :
    routeCycle first third =
      routeCycle first second * routeCycle second third := by
  unfold routeCycle
  group

theorem route_cycle_eq_one_iff {G : Type*} [Group G] (left right : G) :
    routeCycle left right = 1 ↔ left = right := by
  constructor
  · intro h
    have h' := congrArg (fun value => value * right) h
    simpa [routeCycle, mul_assoc] using h'
  · intro h
    rw [h]
    simp [routeCycle]

def cycle01 {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) : G :=
  routeCycle (path0 atlas) (path1 atlas)

def cycle02 {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) : G :=
  routeCycle (path0 atlas) (path2 atlas)

def cycle03 {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) : G :=
  routeCycle (path0 atlas) (path3 atlas)

def cycle12 {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) : G :=
  routeCycle (path1 atlas) (path2 atlas)

def cycle13 {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) : G :=
  routeCycle (path1 atlas) (path3 atlas)

def cycle23 {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) : G :=
  routeCycle (path2 atlas) (path3 atlas)

theorem cycle12_eq_cycle01_inv_mul_cycle02
    {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) :
    cycle12 atlas = (cycle01 atlas)⁻¹ * cycle02 atlas := by
  unfold cycle12 cycle01 cycle02 routeCycle
  group

theorem cycle13_eq_cycle01_inv_mul_cycle03
    {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) :
    cycle13 atlas = (cycle01 atlas)⁻¹ * cycle03 atlas := by
  unfold cycle13 cycle01 cycle03 routeCycle
  group

theorem cycle23_eq_cycle02_inv_mul_cycle03
    {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) :
    cycle23 atlas = (cycle02 atlas)⁻¹ * cycle03 atlas := by
  unfold cycle23 cycle02 cycle03 routeCycle
  group

structure RootedCoordinates (G : Type*) where
  toFirst : G
  toSecond : G
  toThird : G
deriving DecidableEq

/-- Coordinates based at route 0. -/
def root0Coordinates {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) : RootedCoordinates G :=
  {
    toFirst := cycle01 atlas
    toSecond := cycle02 atlas
    toThird := cycle03 atlas
  }

/-- Coordinates based at route 1, ordered toward routes 0, 2, and 3. -/
def root1Coordinates {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) : RootedCoordinates G :=
  {
    toFirst := (cycle01 atlas)⁻¹
    toSecond := cycle12 atlas
    toThird := cycle13 atlas
  }

/-- Nielsen-type change of rooted coordinates from route 0 to route 1. -/
def rebaseAtFirst {G : Type*} [Group G]
    (coordinates : RootedCoordinates G) : RootedCoordinates G :=
  {
    toFirst := coordinates.toFirst⁻¹
    toSecond := coordinates.toFirst⁻¹ * coordinates.toSecond
    toThird := coordinates.toFirst⁻¹ * coordinates.toThird
  }

theorem root1_coordinates_exact_change
    {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) :
    root1Coordinates atlas = rebaseAtFirst (root0Coordinates atlas) := by
  ext
  · rfl
  · exact cycle12_eq_cycle01_inv_mul_cycle02 atlas
  · exact cycle13_eq_cycle01_inv_mul_cycle03 atlas

theorem rebase_at_first_involutive
    {G : Type*} [Group G] (coordinates : RootedCoordinates G) :
    rebaseAtFirst (rebaseAtFirst coordinates) = coordinates := by
  cases coordinates with
  | mk a b c =>
      ext <;> simp [rebaseAtFirst, mul_assoc]

def AllFourPathsAgree {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) : Prop :=
  path0 atlas = path1 atlas ∧
    path0 atlas = path2 atlas ∧
    path0 atlas = path3 atlas

theorem all_four_paths_agree_iff_root0_coordinates_identity
    {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) :
    AllFourPathsAgree atlas ↔
      cycle01 atlas = 1 ∧ cycle02 atlas = 1 ∧ cycle03 atlas = 1 := by
  unfold AllFourPathsAgree cycle01 cycle02 cycle03
  rw [route_cycle_eq_one_iff, route_cycle_eq_one_iff, route_cycle_eq_one_iff]

theorem four_route_cycle_rank :
    (8 : Nat) - 6 + 1 = 3 := by
  norm_num

def localizedDefect {G : Type*} [Group G] (path defect : G) : G :=
  path * defect * path⁻¹

def localizedDefect0 {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G) : G :=
  localizedDefect (path0 atlas) defect

def localizedDefect1 {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G) : G :=
  localizedDefect (path1 atlas) defect

def localizedDefect2 {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G) : G :=
  localizedDefect (path2 atlas) defect

def localizedDefect3 {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G) : G :=
  localizedDefect (path3 atlas) defect

theorem localized_defect_relation
    {G : Type*} [Group G] (left right defect : G) :
    localizedDefect left defect =
      routeCycle left right * localizedDefect right defect *
        (routeCycle left right)⁻¹ := by
  unfold localizedDefect routeCycle
  group

theorem localization0_eq_cycle01_conjugate_localization1
    {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) (defect : G) :
    localizedDefect0 atlas defect =
      cycle01 atlas * localizedDefect1 atlas defect * (cycle01 atlas)⁻¹ := by
  exact localized_defect_relation (path0 atlas) (path1 atlas) defect

theorem localization0_eq_cycle02_conjugate_localization2
    {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) (defect : G) :
    localizedDefect0 atlas defect =
      cycle02 atlas * localizedDefect2 atlas defect * (cycle02 atlas)⁻¹ := by
  exact localized_defect_relation (path0 atlas) (path2 atlas) defect

theorem localization0_eq_cycle03_conjugate_localization3
    {G : Type*} [Group G] (atlas : DualFourRouteAtlas G) (defect : G) :
    localizedDefect0 atlas defect =
      cycle03 atlas * localizedDefect3 atlas defect * (cycle03 atlas)⁻¹ := by
  exact localized_defect_relation (path0 atlas) (path3 atlas) defect

structure FourRouteGaugeFrame (G : Type*) [Group G] where
  g0 : G
  g1 : G
  g2 : G
  g3 : G
  g4 : G
  g5 : G

def gaugeTransformAtlas {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    DualFourRouteAtlas G :=
  {
    j01 := frame.g0⁻¹ * atlas.j01 * frame.g1
    j15 := frame.g1⁻¹ * atlas.j15 * frame.g5
    j02 := frame.g0⁻¹ * atlas.j02 * frame.g2
    j25 := frame.g2⁻¹ * atlas.j25 * frame.g5
    j03 := frame.g0⁻¹ * atlas.j03 * frame.g3
    j35 := frame.g3⁻¹ * atlas.j35 * frame.g5
    j04 := frame.g0⁻¹ * atlas.j04 * frame.g4
    j45 := frame.g4⁻¹ * atlas.j45 * frame.g5
  }

theorem path0_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    path0 (gaugeTransformAtlas atlas frame) =
      frame.g0⁻¹ * path0 atlas * frame.g5 := by
  unfold path0 gaugeTransformAtlas
  group

theorem path1_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    path1 (gaugeTransformAtlas atlas frame) =
      frame.g0⁻¹ * path1 atlas * frame.g5 := by
  unfold path1 gaugeTransformAtlas
  group

theorem path2_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    path2 (gaugeTransformAtlas atlas frame) =
      frame.g0⁻¹ * path2 atlas * frame.g5 := by
  unfold path2 gaugeTransformAtlas
  group

theorem path3_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    path3 (gaugeTransformAtlas atlas frame) =
      frame.g0⁻¹ * path3 atlas * frame.g5 := by
  unfold path3 gaugeTransformAtlas
  group

theorem cycle01_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    cycle01 (gaugeTransformAtlas atlas frame) =
      frame.g0⁻¹ * cycle01 atlas * frame.g0 := by
  unfold cycle01 routeCycle
  rw [path0_gauge_covariant, path1_gauge_covariant]
  group

theorem cycle02_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    cycle02 (gaugeTransformAtlas atlas frame) =
      frame.g0⁻¹ * cycle02 atlas * frame.g0 := by
  unfold cycle02 routeCycle
  rw [path0_gauge_covariant, path2_gauge_covariant]
  group

theorem cycle03_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    cycle03 (gaugeTransformAtlas atlas frame) =
      frame.g0⁻¹ * cycle03 atlas * frame.g0 := by
  unfold cycle03 routeCycle
  rw [path0_gauge_covariant, path3_gauge_covariant]
  group

theorem cycle12_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    cycle12 (gaugeTransformAtlas atlas frame) =
      frame.g0⁻¹ * cycle12 atlas * frame.g0 := by
  unfold cycle12 routeCycle
  rw [path1_gauge_covariant, path2_gauge_covariant]
  group

theorem cycle13_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    cycle13 (gaugeTransformAtlas atlas frame) =
      frame.g0⁻¹ * cycle13 atlas * frame.g0 := by
  unfold cycle13 routeCycle
  rw [path1_gauge_covariant, path3_gauge_covariant]
  group

theorem cycle23_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    cycle23 (gaugeTransformAtlas atlas frame) =
      frame.g0⁻¹ * cycle23 atlas * frame.g0 := by
  unfold cycle23 routeCycle
  rw [path2_gauge_covariant, path3_gauge_covariant]
  group

def gaugeTransformTargetDefect {G : Type*} [Group G]
    (defect : G) (frame : FourRouteGaugeFrame G) : G :=
  frame.g5⁻¹ * defect * frame.g5

theorem localized_defect0_gauge_covariant
    {G : Type*} [Group G]
    (atlas : DualFourRouteAtlas G) (defect : G)
    (frame : FourRouteGaugeFrame G) :
    localizedDefect0 (gaugeTransformAtlas atlas frame)
        (gaugeTransformTargetDefect defect frame) =
      frame.g0⁻¹ * localizedDefect0 atlas defect * frame.g0 := by
  unfold localizedDefect0 localizedDefect gaugeTransformTargetDefect
  rw [path0_gauge_covariant]
  group

def cycle01Wilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G) : R :=
  χ.toFun (cycle01 atlas)

def cycle02Wilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G) : R :=
  χ.toFun (cycle02 atlas)

def cycle03Wilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G) : R :=
  χ.toFun (cycle03 atlas)

def cycle12Wilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G) : R :=
  χ.toFun (cycle12 atlas)

def cycle13Wilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G) : R :=
  χ.toFun (cycle13 atlas)

def cycle23Wilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G) : R :=
  χ.toFun (cycle23 atlas)

theorem cycle01_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G)
    (frame : FourRouteGaugeFrame G) :
    cycle01Wilson χ (gaugeTransformAtlas atlas frame) =
      cycle01Wilson χ atlas := by
  unfold cycle01Wilson
  rw [cycle01_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (cycle01 atlas)

theorem cycle02_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G)
    (frame : FourRouteGaugeFrame G) :
    cycle02Wilson χ (gaugeTransformAtlas atlas frame) =
      cycle02Wilson χ atlas := by
  unfold cycle02Wilson
  rw [cycle02_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (cycle02 atlas)

theorem cycle03_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G)
    (frame : FourRouteGaugeFrame G) :
    cycle03Wilson χ (gaugeTransformAtlas atlas frame) =
      cycle03Wilson χ atlas := by
  unfold cycle03Wilson
  rw [cycle03_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (cycle03 atlas)

theorem cycle12_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G)
    (frame : FourRouteGaugeFrame G) :
    cycle12Wilson χ (gaugeTransformAtlas atlas frame) =
      cycle12Wilson χ atlas := by
  unfold cycle12Wilson
  rw [cycle12_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (cycle12 atlas)

theorem cycle13_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G)
    (frame : FourRouteGaugeFrame G) :
    cycle13Wilson χ (gaugeTransformAtlas atlas frame) =
      cycle13Wilson χ atlas := by
  unfold cycle13Wilson
  rw [cycle13_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (cycle13 atlas)

theorem cycle23_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G)
    (frame : FourRouteGaugeFrame G) :
    cycle23Wilson χ (gaugeTransformAtlas atlas frame) =
      cycle23Wilson χ atlas := by
  unfold cycle23Wilson
  rw [cycle23_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (cycle23 atlas)

structure PairwiseWilsonSignature (R : Type*) where
  s01 : R
  s02 : R
  s03 : R
  s12 : R
  s13 : R
  s23 : R
deriving DecidableEq

def completePairwiseCycleSignature {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G) :
    PairwiseWilsonSignature R :=
  {
    s01 := cycle01Wilson χ atlas
    s02 := cycle02Wilson χ atlas
    s03 := cycle03Wilson χ atlas
    s12 := cycle12Wilson χ atlas
    s13 := cycle13Wilson χ atlas
    s23 := cycle23Wilson χ atlas
  }

theorem complete_pairwise_cycle_signature_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (atlas : DualFourRouteAtlas G)
    (frame : FourRouteGaugeFrame G) :
    completePairwiseCycleSignature χ (gaugeTransformAtlas atlas frame) =
      completePairwiseCycleSignature χ atlas := by
  ext
  · exact cycle01_wilson_gauge_invariant χ atlas frame
  · exact cycle02_wilson_gauge_invariant χ atlas frame
  · exact cycle03_wilson_gauge_invariant χ atlas frame
  · exact cycle12_wilson_gauge_invariant χ atlas frame
  · exact cycle13_wilson_gauge_invariant χ atlas frame
  · exact cycle23_wilson_gauge_invariant χ atlas frame

def routeWilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (path defect : G) : R :=
  χ.toFun (localizedDefect path defect)

theorem route_wilson_eq_target
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (path defect : G) :
    routeWilson χ path defect = χ.toFun defect := by
  unfold routeWilson localizedDefect
  simpa using χ.conjugationInvariant path⁻¹ defect

def sixCycleWilsonSum {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (atlas : DualFourRouteAtlas G) : ℚ :=
  cycle01Wilson χ atlas + cycle02Wilson χ atlas + cycle03Wilson χ atlas +
    cycle12Wilson χ atlas + cycle13Wilson χ atlas + cycle23Wilson χ atlas

theorem six_cycle_wilson_sum_gauge_invariant
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (atlas : DualFourRouteAtlas G)
    (frame : FourRouteGaugeFrame G) :
    sixCycleWilsonSum χ (gaugeTransformAtlas atlas frame) =
      sixCycleWilsonSum χ atlas := by
  unfold sixCycleWilsonSum
  rw [cycle01_wilson_gauge_invariant, cycle02_wilson_gauge_invariant,
    cycle03_wilson_gauge_invariant, cycle12_wilson_gauge_invariant,
    cycle13_wilson_gauge_invariant, cycle23_wilson_gauge_invariant]

def routeAtlasPenalty {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale : ℚ)
    (atlas : DualFourRouteAtlas G) : ℚ :=
  (6 * maxValue - sixCycleWilsonSum χ atlas) / scale

def routeAtlasAdjustedConfidence {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (atlas : DualFourRouteAtlas G) : ℚ :=
  base - routeAtlasPenalty χ maxValue scale atlas

theorem route_atlas_adjusted_confidence_gauge_invariant
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (atlas : DualFourRouteAtlas G) (frame : FourRouteGaugeFrame G) :
    routeAtlasAdjustedConfidence χ maxValue scale base
        (gaugeTransformAtlas atlas frame) =
      routeAtlasAdjustedConfidence χ maxValue scale base atlas := by
  unfold routeAtlasAdjustedConfidence routeAtlasPenalty
  rw [six_cycle_wilson_sum_gauge_invariant]

theorem route_atlas_adjusted_confidence_mem_unit_interval
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (atlas : DualFourRouteAtlas G)
    (hbase0 : 0 ≤ base) (hbase1 : base ≤ 1)
    (hpenalty0 : 0 ≤ routeAtlasPenalty χ maxValue scale atlas)
    (hpenalty : routeAtlasPenalty χ maxValue scale atlas ≤ base) :
    routeAtlasAdjustedConfidence χ maxValue scale base atlas ∈
      Set.Icc (0 : ℚ) 1 := by
  unfold routeAtlasAdjustedConfidence
  constructor <;> linarith

def flatAtlas : DualFourRouteAtlas S3 :=
  {
    j01 := swap01
    j15 := swap12
    j02 := swap01
    j25 := swap12
    j03 := swap01
    j35 := swap12
    j04 := swap01
    j45 := swap12
  }

def singleSupportAtlas : DualFourRouteAtlas S3 :=
  {
    j01 := 1
    j15 := 1
    j02 := swap01
    j25 := 1
    j03 := 1
    j35 := 1
    j04 := 1
    j45 := 1
  }

def orderedABAtlas : DualFourRouteAtlas S3 :=
  {
    j01 := 1
    j15 := 1
    j02 := swap01
    j25 := 1
    j03 := swap12
    j35 := 1
    j04 := swap01 * swap12
    j45 := 1
  }

def orderedBAAtlas : DualFourRouteAtlas S3 :=
  {
    j01 := 1
    j15 := 1
    j02 := swap12
    j25 := 1
    j03 := swap01
    j35 := 1
    j04 := swap12 * swap01
    j45 := 1
  }

def atlasTargetDefect : S3 := thetaTargetDefect

theorem canonical_flat_root_coordinates :
    root0Coordinates flatAtlas =
      { toFirst := 1, toSecond := 1, toThird := 1 } := by
  native_decide

theorem canonical_single_support_root_coordinates :
    root0Coordinates singleSupportAtlas =
      { toFirst := swap01, toSecond := 1, toThird := 1 } := by
  native_decide

theorem canonical_ordered_ab_root_coordinates :
    root0Coordinates orderedABAtlas =
      {
        toFirst := swap01
        toSecond := swap12
        toThird := swap12 * swap01
      } := by
  native_decide

theorem canonical_ordered_ba_root_coordinates :
    root0Coordinates orderedBAAtlas =
      {
        toFirst := swap12
        toSecond := swap01
        toThird := swap01 * swap12
      } := by
  native_decide

theorem canonical_ordered_exact_coordinates_differ :
    root0Coordinates orderedABAtlas ≠ root0Coordinates orderedBAAtlas := by
  native_decide

theorem canonical_ordered_ab_noncommutative :
    (root0Coordinates orderedABAtlas).toFirst *
        (root0Coordinates orderedABAtlas).toSecond ≠
      (root0Coordinates orderedABAtlas).toSecond *
        (root0Coordinates orderedABAtlas).toFirst := by
  native_decide

theorem canonical_ordered_class_signature_limit :
    completePairwiseCycleSignature (identityWilsonClass S3) orderedABAtlas =
      completePairwiseCycleSignature (identityWilsonClass S3) orderedBAAtlas := by
  native_decide

theorem canonical_ordered_route_wilson_equal :
    routeWilson (identityWilsonClass S3) (path0 orderedABAtlas) atlasTargetDefect =
      routeWilson (identityWilsonClass S3) (path3 orderedBAAtlas)
        atlasTargetDefect := by
  rw [route_wilson_eq_target, route_wilson_eq_target]

theorem canonical_flat_penalty :
    routeAtlasPenalty (identityWilsonClass S3) 3 108 flatAtlas = 0 := by
  native_decide

theorem canonical_single_support_penalty :
    routeAtlasPenalty (identityWilsonClass S3) 3 108 singleSupportAtlas =
      1 / 18 := by
  native_decide

theorem canonical_ordered_ab_penalty :
    routeAtlasPenalty (identityWilsonClass S3) 3 108 orderedABAtlas =
      7 / 54 := by
  native_decide

theorem canonical_ordered_ba_penalty :
    routeAtlasPenalty (identityWilsonClass S3) 3 108 orderedBAAtlas =
      7 / 54 := by
  native_decide

theorem canonical_flat_confidence :
    routeAtlasAdjustedConfidence (identityWilsonClass S3) 3 108 (1 / 3)
      flatAtlas = 1 / 3 := by
  native_decide

theorem canonical_single_support_confidence :
    routeAtlasAdjustedConfidence (identityWilsonClass S3) 3 108 (1 / 3)
      singleSupportAtlas = 5 / 18 := by
  native_decide

theorem canonical_ordered_ab_confidence :
    routeAtlasAdjustedConfidence (identityWilsonClass S3) 3 108 (1 / 3)
      orderedABAtlas = 11 / 54 := by
  native_decide

theorem canonical_ordered_ba_confidence :
    routeAtlasAdjustedConfidence (identityWilsonClass S3) 3 108 (1 / 3)
      orderedBAAtlas = 11 / 54 := by
  native_decide

end KUOS.OpenHorizon.MemoryOSRootedRouteAtlasNielsenChangeV0_78
