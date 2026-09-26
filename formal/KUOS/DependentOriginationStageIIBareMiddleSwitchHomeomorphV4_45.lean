import KUOS.DependentOriginationStageIIBareGeometricMiddleSwitchV4_44
import Mathlib.Topology.MetricSpace.Pseudo.Constructions
import Mathlib.Topology.Constructions
import Mathlib

namespace KUOS.DependentOriginationStageIIBareMiddleSwitchHomeomorphV4_45

open Filter
open MeasureTheory
open KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26
open KUOS.DependentOriginationStageIIInverseLimitMiddleSwitchV4_27
open KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29
open KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30
open KUOS.DependentOriginationStageIIGeometricMiddleSwitchV4_43
open KUOS.DependentOriginationStageIIBareGeometricMiddleSwitchV4_44

set_option autoImplicit false

noncomputable section

/-!
# The descended Stage-II middle-switch is a homeomorphism v4.45

v4.44 proves that branch provenance is uniquely recoverable from a bare real
point of the geometric Cantor carrier and therefore descends the tagged
middle-switch to an involution

  stageIIGeometricCarrierMiddleSwitch :
    StageIIGeometricCantorCarrier → StageIIGeometricCantorCarrier.

The remaining topological issue is continuity.

The key quantitative observation is stronger than mere disjointness:
points belonging to different branch fibers are separated by distance at
least one.  Indeed branch offsets differ by at least two, while the two Cantor
coordinates each lie in [0,1].

Consequently, inside every metric ball of radius one in the bare carrier, the
canonical branch selector is constant.  On such a neighborhood the descended
middle-switch is exactly one fixed real translation from v4.43.  Since that
translation is an isometry, it is continuous.

This gives continuity pointwise without hiding the piecewise geometry inside a
large simplifier call.  Because the map is involutive, the same continuous map
is its inverse, yielding a genuine self-homeomorphism of the bare geometric
Cantor carrier.
-/

/-- Distinct branch fibers are quantitatively separated: any point in one
fiber is at real distance at least one from any point in another fiber. -/
theorem stageIIGeometricCantorFiber_dist_ge_one
    {x y : StageIIFiniteDepthInverseLimit}
    (hxy : x ≠ y)
    {p q : ℝ}
    (hp : p ∈ stageIIGeometricCantorFiber x)
    (hq : q ∈ stageIIGeometricCantorFiber y) :
    (1 : ℝ) ≤ dist p q := by
  unfold stageIIGeometricCantorFiber at hp hq
  rcases hp with ⟨tp, htpC, hpEq⟩
  rcases hq with ⟨tq, htqC, hqEq⟩
  have htpI : tp ∈ Set.Icc (0 : ℝ) 1 :=
    cantorSet_subset_unitInterval htpC
  have htqI : tq ∈ Set.Icc (0 : ℝ) 1 :=
    cantorSet_subset_unitInterval htqC
  have hcoord :
      |tp - tq| ≤ (1 : ℝ) := by
    rw [abs_le]
    constructor <;>
      linarith [htpI.1, htpI.2, htqI.1, htqI.2]
  have hoff :
      (2 : ℝ) ≤
        |stageIICurrentBranchOffset x -
          stageIICurrentBranchOffset y| :=
    stageIICurrentBranchOffset_separated hxy
  have halgebra :
      stageIICurrentBranchOffset x -
          stageIICurrentBranchOffset y =
        (p - q) - (tp - tq) := by
    unfold stageIICantorTranslate at hpEq hqEq
    linarith
  have htriangle :
      |stageIICurrentBranchOffset x -
          stageIICurrentBranchOffset y| ≤
        |p - q| + |tp - tq| := by
    rw [halgebra]
    exact abs_sub _ _
  rw [Real.dist_eq]
  linarith

/-- On the bare carrier, different selected branches force distance at least
one. -/
theorem stageIIGeometricCarrier_dist_ge_one_of_branch_ne
    {p q : StageIIGeometricCantorCarrier}
    (hpq :
      stageIIGeometricBranch p ≠
        stageIIGeometricBranch q) :
    (1 : ℝ) ≤ dist p q := by
  rw [Subtype.dist_eq]
  exact
    stageIIGeometricCantorFiber_dist_ge_one
      hpq
      (stageIIGeometricBranch_mem p)
      (stageIIGeometricBranch_mem q)

/-- Two bare geometric points at distance less than one necessarily have the
same recovered branch. -/
theorem stageIIGeometricBranch_eq_of_dist_lt_one
    (p q : StageIIGeometricCantorCarrier)
    (hqp : dist q p < (1 : ℝ)) :
    stageIIGeometricBranch q =
      stageIIGeometricBranch p := by
  by_contra hne
  have hge :
      (1 : ℝ) ≤ dist q p :=
    stageIIGeometricCarrier_dist_ge_one_of_branch_ne hne
  linarith

/-- The canonical branch selector is locally constant: near each bare
geometric point it equals the branch selected at that point. -/
theorem eventually_stageIIGeometricBranch_eq
    (p : StageIIGeometricCantorCarrier) :
    ∀ᶠ q in nhds p,
      stageIIGeometricBranch q =
        stageIIGeometricBranch p := by
  rw [Metric.eventually_nhds_iff]
  refine ⟨1, by norm_num, ?_⟩
  intro q hqp
  exact stageIIGeometricBranch_eq_of_dist_lt_one p q hqp

/-- The branch component selected by a fixed inverse-limit index. -/
def stageIIGeometricCarrierBranchComponent
    (x : StageIIFiniteDepthInverseLimit) :
    Set StageIIGeometricCantorCarrier :=
  {p | stageIIGeometricBranch p = x}

/-- Each branch component is open in the bare geometric carrier. -/
theorem isOpen_stageIIGeometricCarrierBranchComponent
    (x : StageIIFiniteDepthInverseLimit) :
    IsOpen (stageIIGeometricCarrierBranchComponent x) := by
  rw [Metric.isOpen_iff]
  intro p hp
  refine ⟨1, by norm_num, ?_⟩
  intro q hq
  have hqp : dist q p < (1 : ℝ) := by
    simpa [Metric.mem_ball, dist_comm] using hq
  have hbranch :=
    stageIIGeometricBranch_eq_of_dist_lt_one p q hqp
  exact hbranch.trans hp

/-- Each branch component is also closed; equivalently, the bare carrier is
the finite separated union of clopen Cantor branches. -/
theorem isClosed_stageIIGeometricCarrierBranchComponent
    (x : StageIIFiniteDepthInverseLimit) :
    IsClosed (stageIIGeometricCarrierBranchComponent x) := by
  rw [← isOpen_compl_iff]
  rw [Metric.isOpen_iff]
  intro p hp
  refine ⟨1, by norm_num, ?_⟩
  intro q hq
  have hqp : dist q p < (1 : ℝ) := by
    simpa [Metric.mem_ball, dist_comm] using hq
  have hbranch :=
    stageIIGeometricBranch_eq_of_dist_lt_one p q hqp
  change stageIIGeometricBranch q ≠ x
  change stageIIGeometricBranch p ≠ x at hp
  intro hqx
  exact hp (hbranch.symm.trans hqx)

/-- Real-valued realization of the descended bare middle-switch. -/
noncomputable def stageIIGeometricCarrierMiddleSwitchReal
    (p : StageIIGeometricCantorCarrier) : ℝ :=
  (stageIIGeometricCarrierMiddleSwitch p).1

/-- Near a point p, the descended real-valued map is exactly the single fixed
translation associated to the branch selected at p. -/
theorem stageIIGeometricCarrierMiddleSwitchReal_eventuallyEq
    (p : StageIIGeometricCantorCarrier) :
    (fun q : StageIIGeometricCantorCarrier =>
      stageIIGeometricCarrierMiddleSwitchReal q)
      =ᶠ[nhds p]
    (fun q : StageIIGeometricCantorCarrier =>
      stageIIGeometricMiddleSwitchTranslate
        (stageIIGeometricBranch p) q.1) := by
  filter_upwards [eventually_stageIIGeometricBranch_eq p] with q hbranch
  change
    stageIIGeometricMiddleSwitchTranslate
        (stageIIGeometricBranch q) q.1 =
      stageIIGeometricMiddleSwitchTranslate
        (stageIIGeometricBranch p) q.1
  rw [hbranch]

/-- The real-valued realization of the descended middle-switch is continuous
at every point. -/
theorem continuousAt_stageIIGeometricCarrierMiddleSwitchReal
    (p : StageIIGeometricCantorCarrier) :
    ContinuousAt stageIIGeometricCarrierMiddleSwitchReal p := by
  have hfixed :
      Continuous
        (fun q : StageIIGeometricCantorCarrier =>
          stageIIGeometricMiddleSwitchTranslate
            (stageIIGeometricBranch p) q.1) := by
    exact
      (continuous_stageIIGeometricMiddleSwitchTranslate
        (stageIIGeometricBranch p)).comp continuous_subtype_val
  exact
    hfixed.continuousAt.congr
      (stageIIGeometricCarrierMiddleSwitchReal_eventuallyEq p).symm

/-- The real-valued descended map always lands back in the global geometric
Cantor carrier. -/
theorem stageIIGeometricCarrierMiddleSwitchReal_mem
    (p : StageIIGeometricCantorCarrier) :
    stageIIGeometricCarrierMiddleSwitchReal p ∈
      XInfinityGeometricFractal :=
  (stageIIGeometricCarrierMiddleSwitch p).property

/-- The subtype-valued descended middle-switch is continuous at every point. -/
theorem continuousAt_stageIIGeometricCarrierMiddleSwitch
    (p : StageIIGeometricCantorCarrier) :
    ContinuousAt stageIIGeometricCarrierMiddleSwitch p := by
  have hcod :
      ContinuousAt
        (Set.codRestrict
          stageIIGeometricCarrierMiddleSwitchReal
          XInfinityGeometricFractal
          stageIIGeometricCarrierMiddleSwitchReal_mem)
        p :=
    (continuousAt_stageIIGeometricCarrierMiddleSwitchReal p).codRestrict
      stageIIGeometricCarrierMiddleSwitchReal_mem
  simpa [stageIIGeometricCarrierMiddleSwitchReal,
    stageIIGeometricCarrierMiddleSwitch] using hcod

/-- The descended middle-switch is globally continuous. -/
theorem continuous_stageIIGeometricCarrierMiddleSwitch :
    Continuous stageIIGeometricCarrierMiddleSwitch := by
  rw [continuous_iff_continuousAt]
  exact continuousAt_stageIIGeometricCarrierMiddleSwitch

/-- The algebraic self-equivalence from v4.44 is in fact a self-homeomorphism
of the bare geometric Cantor carrier. -/
noncomputable def stageIIGeometricCarrierMiddleSwitchHomeomorph :
    StageIIGeometricCantorCarrier ≃ₜ
      StageIIGeometricCantorCarrier where
  toEquiv := stageIIGeometricCarrierMiddleSwitchEquiv
  continuous_toFun := by
    simpa [stageIIGeometricCarrierMiddleSwitchEquiv] using
      continuous_stageIIGeometricCarrierMiddleSwitch
  continuous_invFun := by
    simpa [stageIIGeometricCarrierMiddleSwitchEquiv] using
      continuous_stageIIGeometricCarrierMiddleSwitch

/-- The homeomorphism has no fixed point. -/
theorem stageIIGeometricCarrierMiddleSwitchHomeomorph_ne_self
    (p : StageIIGeometricCantorCarrier) :
    stageIIGeometricCarrierMiddleSwitchHomeomorph p ≠ p :=
  stageIIGeometricCarrierMiddleSwitch_ne_self p

/-- The homeomorphism remains exactly involutive. -/
theorem stageIIGeometricCarrierMiddleSwitchHomeomorph_involutive :
    Function.Involutive
      stageIIGeometricCarrierMiddleSwitchHomeomorph := by
  intro p
  exact stageIIGeometricCarrierMiddleSwitch_involutive p

/-!
## Boundary after v4.45

The descended middle-switch is now topological, not merely set-theoretic.

The key new quantitative theorem is:

  different branch provenance
    -> distance >= 1.

Therefore the canonical branch selector is locally constant on radius-one
neighborhoods.  The eight branch components of the bare geometric carrier are
clopen.

Locally, the descended middle-switch is exactly one fixed v4.43 translation.
Since each such translation is an isometry, the descended map is continuous.
Together with the already-proved involution law, this yields the genuine
fixed-point-free self-homeomorphism

  stageIIGeometricCarrierMiddleSwitchHomeomorph.

No continuity is obtained by assertion or by choosing an arbitrary topology:
it follows from the explicit two-unit branch separation and the inherited
subspace metric on the geometric Cantor carrier.

A subsequent theorem unit can transport the finite-depth orientation flip and
Stage-II obstruction semantics through this homeomorphism, or study the
quotient by the free Z/2 middle-switch action.
-/

end

end KUOS.DependentOriginationStageIIBareMiddleSwitchHomeomorphV4_45
