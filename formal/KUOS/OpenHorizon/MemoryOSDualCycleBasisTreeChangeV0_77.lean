import Mathlib
import KUOS.OpenHorizon.MemoryOSBranchedDualGraphCycleObstructionV0_76

namespace KUOS.OpenHorizon.MemoryOSDualCycleBasisTreeChangeV0_77

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSDualCellChainDefectLocalizationV0_75
open KUOS.OpenHorizon.MemoryOSBranchedDualGraphCycleObstructionV0_76

/-- A finite theta-shaped dual graph with three root-to-target routes. -/
structure DualTheta (G : Type*) [Group G] where
  j01 : G
  j14 : G
  j02 : G
  j24 : G
  j03 : G
  j34 : G

def path0 {G : Type*} [Group G] (theta : DualTheta G) : G :=
  theta.j01 * theta.j14

def path1 {G : Type*} [Group G] (theta : DualTheta G) : G :=
  theta.j02 * theta.j24

def path2 {G : Type*} [Group G] (theta : DualTheta G) : G :=
  theta.j03 * theta.j34

/-- Fundamental cycle based on route 0 versus route 1. -/
def cycle01 {G : Type*} [Group G] (theta : DualTheta G) : G :=
  path0 theta * (path1 theta)⁻¹

/-- Fundamental cycle based on route 0 versus route 2. -/
def cycle02 {G : Type*} [Group G] (theta : DualTheta G) : G :=
  path0 theta * (path2 theta)⁻¹

/-- Pairwise cycle comparing route 1 versus route 2. -/
def cycle12 {G : Type*} [Group G] (theta : DualTheta G) : G :=
  path1 theta * (path2 theta)⁻¹

theorem cycle12_eq_cycle01_inv_mul_cycle02
    {G : Type*} [Group G] (theta : DualTheta G) :
    cycle12 theta = (cycle01 theta)⁻¹ * cycle02 theta := by
  unfold cycle12 cycle01 cycle02
  group

theorem cycle02_eq_cycle01_mul_cycle12
    {G : Type*} [Group G] (theta : DualTheta G) :
    cycle02 theta = cycle01 theta * cycle12 theta := by
  unfold cycle12 cycle01 cycle02
  group

def AllPathsAgree {G : Type*} [Group G] (theta : DualTheta G) : Prop :=
  path0 theta = path1 theta ∧ path0 theta = path2 theta

theorem all_paths_agree_iff_fundamental_cycles_identity
    {G : Type*} [Group G] (theta : DualTheta G) :
    AllPathsAgree theta ↔ cycle01 theta = 1 ∧ cycle02 theta = 1 := by
  constructor
  · rintro ⟨h01, h02⟩
    constructor
    · unfold cycle01
      rw [h01]
      simp
    · unfold cycle02
      rw [h02]
      simp
  · rintro ⟨h01, h02⟩
    constructor
    · unfold cycle01 at h01
      have h := congrArg (fun value => value * path1 theta) h01
      simpa [mul_assoc] using h
    · unfold cycle02 at h02
      have h := congrArg (fun value => value * path2 theta) h02
      simpa [mul_assoc] using h

/-- Cycle basis selected when route 0 is the spanning-tree route. -/
def tree0Basis {G : Type*} [Group G] (theta : DualTheta G) : G × G :=
  (cycle01 theta, cycle02 theta)

/-- Cycle basis selected when route 1 is the spanning-tree route. -/
def tree1Basis {G : Type*} [Group G] (theta : DualTheta G) : G × G :=
  ((cycle01 theta)⁻¹, cycle12 theta)

/-- Exact Nielsen-type basis change between route-0 and route-1 trees. -/
theorem tree1_basis_exact_change
    {G : Type*} [Group G] (theta : DualTheta G) :
    tree1Basis theta =
      ((tree0Basis theta).1⁻¹,
        (tree0Basis theta).1⁻¹ * (tree0Basis theta).2) := by
  unfold tree0Basis tree1Basis
  rw [cycle12_eq_cycle01_inv_mul_cycle02]

theorem tree0_basis_reconstructs_cycle12
    {G : Type*} [Group G] (theta : DualTheta G) :
    cycle12 theta =
      (tree0Basis theta).1⁻¹ * (tree0Basis theta).2 := by
  exact cycle12_eq_cycle01_inv_mul_cycle02 theta

theorem tree1_basis_reconstructs_cycle02
    {G : Type*} [Group G] (theta : DualTheta G) :
    cycle02 theta =
      (tree1Basis theta).1⁻¹ * (tree1Basis theta).2 := by
  unfold tree1Basis
  rw [cycle02_eq_cycle01_mul_cycle12]
  simp

def localizedDefect0 {G : Type*} [Group G]
    (theta : DualTheta G) (defect : G) : G :=
  path0 theta * defect * (path0 theta)⁻¹

def localizedDefect1 {G : Type*} [Group G]
    (theta : DualTheta G) (defect : G) : G :=
  path1 theta * defect * (path1 theta)⁻¹

def localizedDefect2 {G : Type*} [Group G]
    (theta : DualTheta G) (defect : G) : G :=
  path2 theta * defect * (path2 theta)⁻¹

theorem localization0_eq_cycle01_conjugate_localization1
    {G : Type*} [Group G] (theta : DualTheta G) (defect : G) :
    localizedDefect0 theta defect =
      cycle01 theta * localizedDefect1 theta defect * (cycle01 theta)⁻¹ := by
  unfold localizedDefect0 localizedDefect1 cycle01
  group

theorem localization0_eq_cycle02_conjugate_localization2
    {G : Type*} [Group G] (theta : DualTheta G) (defect : G) :
    localizedDefect0 theta defect =
      cycle02 theta * localizedDefect2 theta defect * (cycle02 theta)⁻¹ := by
  unfold localizedDefect0 localizedDefect2 cycle02
  group

theorem localization1_eq_cycle12_conjugate_localization2
    {G : Type*} [Group G] (theta : DualTheta G) (defect : G) :
    localizedDefect1 theta defect =
      cycle12 theta * localizedDefect2 theta defect * (cycle12 theta)⁻¹ := by
  unfold localizedDefect1 localizedDefect2 cycle12
  group

structure ThetaGaugeFrame (G : Type*) [Group G] where
  g0 : G
  g1 : G
  g2 : G
  g3 : G
  g4 : G

def gaugeTransformTheta {G : Type*} [Group G]
    (theta : DualTheta G) (frame : ThetaGaugeFrame G) : DualTheta G :=
  {
    j01 := frame.g0⁻¹ * theta.j01 * frame.g1
    j14 := frame.g1⁻¹ * theta.j14 * frame.g4
    j02 := frame.g0⁻¹ * theta.j02 * frame.g2
    j24 := frame.g2⁻¹ * theta.j24 * frame.g4
    j03 := frame.g0⁻¹ * theta.j03 * frame.g3
    j34 := frame.g3⁻¹ * theta.j34 * frame.g4
  }

theorem path0_gauge_covariant
    {G : Type*} [Group G]
    (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    path0 (gaugeTransformTheta theta frame) =
      frame.g0⁻¹ * path0 theta * frame.g4 := by
  unfold path0 gaugeTransformTheta
  group

theorem path1_gauge_covariant
    {G : Type*} [Group G]
    (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    path1 (gaugeTransformTheta theta frame) =
      frame.g0⁻¹ * path1 theta * frame.g4 := by
  unfold path1 gaugeTransformTheta
  group

theorem path2_gauge_covariant
    {G : Type*} [Group G]
    (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    path2 (gaugeTransformTheta theta frame) =
      frame.g0⁻¹ * path2 theta * frame.g4 := by
  unfold path2 gaugeTransformTheta
  group

theorem cycle01_gauge_covariant
    {G : Type*} [Group G]
    (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    cycle01 (gaugeTransformTheta theta frame) =
      frame.g0⁻¹ * cycle01 theta * frame.g0 := by
  unfold cycle01
  rw [path0_gauge_covariant, path1_gauge_covariant]
  group

theorem cycle02_gauge_covariant
    {G : Type*} [Group G]
    (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    cycle02 (gaugeTransformTheta theta frame) =
      frame.g0⁻¹ * cycle02 theta * frame.g0 := by
  unfold cycle02
  rw [path0_gauge_covariant, path2_gauge_covariant]
  group

theorem cycle12_gauge_covariant
    {G : Type*} [Group G]
    (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    cycle12 (gaugeTransformTheta theta frame) =
      frame.g0⁻¹ * cycle12 theta * frame.g0 := by
  unfold cycle12
  rw [path1_gauge_covariant, path2_gauge_covariant]
  group

def gaugeTransformThetaTargetDefect {G : Type*} [Group G]
    (defect : G) (frame : ThetaGaugeFrame G) : G :=
  frame.g4⁻¹ * defect * frame.g4

theorem localized_defect0_gauge_covariant
    {G : Type*} [Group G]
    (theta : DualTheta G) (defect : G) (frame : ThetaGaugeFrame G) :
    localizedDefect0 (gaugeTransformTheta theta frame)
        (gaugeTransformThetaTargetDefect defect frame) =
      frame.g0⁻¹ * localizedDefect0 theta defect * frame.g0 := by
  unfold localizedDefect0 gaugeTransformThetaTargetDefect
  rw [path0_gauge_covariant]
  group

def cycle01Wilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) : R :=
  χ.toFun (cycle01 theta)

def cycle02Wilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) : R :=
  χ.toFun (cycle02 theta)

def cycle12Wilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) : R :=
  χ.toFun (cycle12 theta)

theorem cycle01_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    cycle01Wilson χ (gaugeTransformTheta theta frame) =
      cycle01Wilson χ theta := by
  unfold cycle01Wilson
  rw [cycle01_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (cycle01 theta)

theorem cycle02_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    cycle02Wilson χ (gaugeTransformTheta theta frame) =
      cycle02Wilson χ theta := by
  unfold cycle02Wilson
  rw [cycle02_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (cycle02 theta)

theorem cycle12_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    cycle12Wilson χ (gaugeTransformTheta theta frame) =
      cycle12Wilson χ theta := by
  unfold cycle12Wilson
  rw [cycle12_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (cycle12 theta)

/-- Complete pairwise cycle signature; no spanning-tree route is privileged. -/
def completePairwiseCycleSignature {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) : R × R × R :=
  (cycle01Wilson χ theta, cycle02Wilson χ theta, cycle12Wilson χ theta)

theorem complete_pairwise_cycle_signature_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    completePairwiseCycleSignature χ (gaugeTransformTheta theta frame) =
      completePairwiseCycleSignature χ theta := by
  unfold completePairwiseCycleSignature
  rw [cycle01_wilson_gauge_invariant, cycle02_wilson_gauge_invariant,
    cycle12_wilson_gauge_invariant]

def thetaRouteWilson0 {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) (defect : G) : R :=
  χ.toFun (localizedDefect0 theta defect)

def thetaRouteWilson1 {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) (defect : G) : R :=
  χ.toFun (localizedDefect1 theta defect)

def thetaRouteWilson2 {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) (defect : G) : R :=
  χ.toFun (localizedDefect2 theta defect)

theorem theta_route_wilson0_eq_target
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) (defect : G) :
    thetaRouteWilson0 χ theta defect = χ.toFun defect := by
  unfold thetaRouteWilson0 localizedDefect0
  simpa using χ.conjugationInvariant (path0 theta)⁻¹ defect

theorem theta_route_wilson1_eq_target
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) (defect : G) :
    thetaRouteWilson1 χ theta defect = χ.toFun defect := by
  unfold thetaRouteWilson1 localizedDefect1
  simpa using χ.conjugationInvariant (path1 theta)⁻¹ defect

theorem theta_route_wilson2_eq_target
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (theta : DualTheta G) (defect : G) :
    thetaRouteWilson2 χ theta defect = χ.toFun defect := by
  unfold thetaRouteWilson2 localizedDefect2
  simpa using χ.conjugationInvariant (path2 theta)⁻¹ defect

def pairwiseCycleWilsonSum {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (theta : DualTheta G) : ℚ :=
  cycle01Wilson χ theta + cycle02Wilson χ theta + cycle12Wilson χ theta

theorem pairwise_cycle_wilson_sum_gauge_invariant
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    pairwiseCycleWilsonSum χ (gaugeTransformTheta theta frame) =
      pairwiseCycleWilsonSum χ theta := by
  unfold pairwiseCycleWilsonSum
  rw [cycle01_wilson_gauge_invariant, cycle02_wilson_gauge_invariant,
    cycle12_wilson_gauge_invariant]

/-- Symmetric advisory penalty over all three pairwise cycles. -/
def thetaCyclePenalty {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale : ℚ)
    (theta : DualTheta G) : ℚ :=
  (3 * maxValue - pairwiseCycleWilsonSum χ theta) / scale

def thetaAdjustedConfidence {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (theta : DualTheta G) : ℚ :=
  base - thetaCyclePenalty χ maxValue scale theta

theorem theta_adjusted_confidence_gauge_invariant
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (theta : DualTheta G) (frame : ThetaGaugeFrame G) :
    thetaAdjustedConfidence χ maxValue scale base
        (gaugeTransformTheta theta frame) =
      thetaAdjustedConfidence χ maxValue scale base theta := by
  unfold thetaAdjustedConfidence thetaCyclePenalty
  rw [pairwise_cycle_wilson_sum_gauge_invariant]

theorem theta_adjusted_confidence_mem_unit_interval
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (theta : DualTheta G)
    (hbase0 : 0 ≤ base) (hbase1 : base ≤ 1)
    (hpenalty0 : 0 ≤ thetaCyclePenalty χ maxValue scale theta)
    (hpenalty : thetaCyclePenalty χ maxValue scale theta ≤ base) :
    thetaAdjustedConfidence χ maxValue scale base theta ∈ Set.Icc (0 : ℚ) 1 := by
  unfold thetaAdjustedConfidence
  constructor <;> linarith

def flatTheta : DualTheta S3 :=
  {
    j01 := swap01
    j14 := swap12
    j02 := swap01
    j24 := swap12
    j03 := swap01
    j34 := swap12
  }

def rankOneTheta : DualTheta S3 :=
  {
    j01 := 1
    j14 := 1
    j02 := swap01
    j24 := 1
    j03 := 1
    j34 := 1
  }

def rankTwoTheta : DualTheta S3 :=
  {
    j01 := 1
    j14 := 1
    j02 := swap01
    j24 := 1
    j03 := swap12
    j34 := 1
  }

def thetaTargetDefect : S3 := canonicalTargetDefect

theorem canonical_flat_all_paths_agree :
    AllPathsAgree flatTheta := by
  native_decide

theorem canonical_flat_cycle_basis :
    tree0Basis flatTheta = (1, 1) := by
  native_decide

theorem canonical_rank_one_cycles :
    cycle01 rankOneTheta = swap01 ∧
      cycle02 rankOneTheta = 1 ∧
      cycle12 rankOneTheta = swap01 := by
  native_decide

theorem canonical_rank_two_cycles :
    cycle01 rankTwoTheta = swap01 ∧
      cycle02 rankTwoTheta = swap12 ∧
      cycle12 rankTwoTheta = swap01 * swap12 := by
  native_decide

theorem canonical_rank_two_tree_change :
    tree1Basis rankTwoTheta =
      (swap01, swap01 * swap12) := by
  native_decide

theorem canonical_rank_two_basis_noncommutative :
    cycle01 rankTwoTheta * cycle02 rankTwoTheta ≠
      cycle02 rankTwoTheta * cycle01 rankTwoTheta := by
  native_decide

theorem canonical_rank_two_route0_localization :
    localizedDefect0 rankTwoTheta thetaTargetDefect = thetaTargetDefect := by
  native_decide

theorem canonical_rank_two_route1_localization :
    localizedDefect1 rankTwoTheta thetaTargetDefect =
      swap01 * thetaTargetDefect * swap01 := by
  native_decide

theorem canonical_rank_two_route2_localization :
    localizedDefect2 rankTwoTheta thetaTargetDefect =
      swap12 * thetaTargetDefect * swap12 := by
  native_decide

theorem canonical_rank_two_route_wilson_equal :
    thetaRouteWilson0 (identityWilsonClass S3) rankTwoTheta thetaTargetDefect =
      thetaRouteWilson1 (identityWilsonClass S3) rankTwoTheta thetaTargetDefect ∧
    thetaRouteWilson1 (identityWilsonClass S3) rankTwoTheta thetaTargetDefect =
      thetaRouteWilson2 (identityWilsonClass S3) rankTwoTheta thetaTargetDefect := by
  constructor
  · rw [theta_route_wilson0_eq_target, theta_route_wilson1_eq_target]
  · rw [theta_route_wilson1_eq_target, theta_route_wilson2_eq_target]

theorem canonical_flat_theta_penalty :
    thetaCyclePenalty (identityWilsonClass S3) 3 54 flatTheta = 0 := by
  native_decide

theorem canonical_rank_one_theta_penalty :
    thetaCyclePenalty (identityWilsonClass S3) 3 54 rankOneTheta = 2 / 27 := by
  native_decide

theorem canonical_rank_two_theta_penalty :
    thetaCyclePenalty (identityWilsonClass S3) 3 54 rankTwoTheta = 7 / 54 := by
  native_decide

theorem canonical_flat_theta_confidence :
    thetaAdjustedConfidence (identityWilsonClass S3) 3 54 (1 / 3)
      flatTheta = 1 / 3 := by
  native_decide

theorem canonical_rank_one_theta_confidence :
    thetaAdjustedConfidence (identityWilsonClass S3) 3 54 (1 / 3)
      rankOneTheta = 7 / 27 := by
  native_decide

theorem canonical_rank_two_theta_confidence :
    thetaAdjustedConfidence (identityWilsonClass S3) 3 54 (1 / 3)
      rankTwoTheta = 11 / 54 := by
  native_decide

end KUOS.OpenHorizon.MemoryOSDualCycleBasisTreeChangeV0_77
