import KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30
import Mathlib.Topology.MetricSpace.HausdorffDistance
import Mathlib.Topology.MetricSpace.Pseudo.Lemmas
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Topology.Instances.CantorSet
import Mathlib

namespace KUOS.DependentOriginationStageIICantorMetricConvergenceV4_31

open Filter
open MeasureTheory
open KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26
open KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29
open KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30

set_option autoImplicit false

noncomputable section

/-!
# Metric convergence to the geometric Cantor carrier v4.31

v4.30 constructs the compact geometric carrier as eight translated copies of
the classical ternary Cantor set.

For a point t in the Cantor set, mathlib already proves that the finite sum of
the first n ternary digits lies between

  t - (1/3)^n

and t.

We use this exact estimate to define finite-depth geometric approximants.
The bound is uniform in the Cantor point and in the Stage-II branch index.
Consequently:

* every approximating point is within (1/3)^n of its limiting Cantor point;
* every limiting point is within (1/3)^n of the corresponding approximant;
* the global Hausdorff distance is at most (1/3)^n;
* therefore the Hausdorff distance tends to zero.

This is metric convergence of the geometric carrier itself, not merely
pointwise convergence of one selected branch.
-/

/-- The finite ternary partial sum attached to one real point. For points in
the Cantor set, v4.31 uses the canonical 0/2 ternary expansion supplied by
mathlib. -/
noncomputable def stageIICantorPartial
    (n : Nat) (t : ℝ) : ℝ :=
  ∑ i ∈ Finset.range n,
    Real.ofDigitsTerm (cantorToTernary t) i

/-- For a Cantor point, the partial sum never overshoots the limit. -/
theorem stageIICantorPartial_le
    {t : ℝ} (ht : t ∈ cantorSet) (n : Nat) :
    stageIICantorPartial n t ≤ t := by
  exact ofDigits_cantorToTernary_sum_le ht

/-- For a Cantor point, the missing tail is bounded by (1/3)^n. -/
theorem sub_scale_le_stageIICantorPartial
    {t : ℝ} (ht : t ∈ cantorSet) (n : Nat) :
    t - (3 : ℝ)⁻¹ ^ n ≤ stageIICantorPartial n t := by
  exact le_ofDigits_cantorToTernary_sum ht

/-- Quantitative pointwise error bound for one Cantor point. -/
theorem dist_stageIICantorPartial_le
    {t : ℝ} (ht : t ∈ cantorSet) (n : Nat) :
    dist (stageIICantorPartial n t) t ≤ (3 : ℝ)⁻¹ ^ n := by
  rw [Real.dist_eq, abs_sub_comm, abs_of_nonneg]
  · linarith [sub_scale_le_stageIICantorPartial ht n]
  · linarith [stageIICantorPartial_le ht n]

/-- Finite-depth approximating point in one translated Stage-II branch. -/
noncomputable def stageIIGeometricApproxPoint
    (n : Nat)
    (x : StageIIFiniteDepthInverseLimit)
    (t : ℝ) : ℝ :=
  stageIICurrentBranchOffset x + stageIICantorPartial n t

/-- Limiting geometric point in one translated Stage-II branch. -/
noncomputable def stageIIGeometricLimitPoint
    (x : StageIIFiniteDepthInverseLimit)
    (t : ℝ) : ℝ :=
  stageIICurrentBranchOffset x + t

/-- The branch translation does not change the finite-depth error bound. -/
theorem dist_stageIIGeometricApproxPoint_le
    {t : ℝ} (ht : t ∈ cantorSet)
    (n : Nat)
    (x : StageIIFiniteDepthInverseLimit) :
    dist (stageIIGeometricApproxPoint n x t)
      (stageIIGeometricLimitPoint x t) ≤
        (3 : ℝ)⁻¹ ^ n := by
  simpa [stageIIGeometricApproxPoint, stageIIGeometricLimitPoint,
    Real.dist_eq] using dist_stageIICantorPartial_le ht n

/-- The geometric approximation scale tends to zero. -/
theorem stageIIGeometricApproxScale_tendsto_zero :
    Tendsto (fun n : Nat => (3 : ℝ)⁻¹ ^ n) atTop (nhds 0) := by
  exact tendsto_pow_atTop_nhds_zero_of_lt_one
    (by positivity) (by norm_num)

/-- Every coded point converges metrically to its branch Cantor point. -/
theorem stageIIGeometricApproxPoint_tendsto
    {t : ℝ} (ht : t ∈ cantorSet)
    (x : StageIIFiniteDepthInverseLimit) :
    Tendsto
      (fun n : Nat => stageIIGeometricApproxPoint n x t)
      atTop
      (nhds (stageIIGeometricLimitPoint x t)) := by
  apply tendsto_iff_dist_tendsto_zero.2
  apply squeeze_zero
  · intro n
    exact dist_nonneg
  · intro n
    exact dist_stageIIGeometricApproxPoint_le ht n x
  · exact stageIIGeometricApproxScale_tendsto_zero

/-- One finite-depth geometric fiber, obtained by truncating the canonical
ternary expansion of every Cantor point after n digits. -/
noncomputable def stageIIGeometricApproxFiber
    (n : Nat)
    (x : StageIIFiniteDepthInverseLimit) : Set ℝ :=
  stageIIGeometricApproxPoint n x '' cantorSet

/-- The global finite-depth geometric approximant. -/
noncomputable def XInfinityGeometricApprox
    (n : Nat) : Set ℝ :=
  ⋃ x : StageIIFiniteDepthInverseLimit,
    stageIIGeometricApproxFiber n x

/-- The finite-depth approximant and its limiting Cantor fiber are at
Hausdorff distance at most (1/3)^n. -/
theorem hausdorffDist_stageIIGeometricApproxFiber_le
    (n : Nat)
    (x : StageIIFiniteDepthInverseLimit) :
    Metric.hausdorffDist
        (stageIIGeometricApproxFiber n x)
        (stageIIGeometricCantorFiber x) ≤
      (3 : ℝ)⁻¹ ^ n := by
  apply Metric.hausdorffDist_le_of_mem_dist
  · positivity
  · intro y hy
    rcases hy with ⟨t, ht, rfl⟩
    refine ⟨stageIIGeometricLimitPoint x t, ?_, ?_⟩
    · exact ⟨t, ht, rfl⟩
    · exact dist_stageIIGeometricApproxPoint_le ht n x
  · intro y hy
    rcases hy with ⟨t, ht, rfl⟩
    refine ⟨stageIIGeometricApproxPoint n x t, ?_, ?_⟩
    · exact ⟨t, ht, rfl⟩
    · simpa [dist_comm] using
        dist_stageIIGeometricApproxPoint_le ht n x

/-- Uniform global Hausdorff bound across all eight branches. -/
theorem hausdorffDist_XInfinityGeometricApprox_le
    (n : Nat) :
    Metric.hausdorffDist
        (XInfinityGeometricApprox n)
        XInfinityGeometricFractal ≤
      (3 : ℝ)⁻¹ ^ n := by
  apply Metric.hausdorffDist_le_of_mem_dist
  · positivity
  · intro y hy
    rcases Set.mem_iUnion.mp hy with ⟨x, hx⟩
    rcases hx with ⟨t, ht, rfl⟩
    refine ⟨stageIIGeometricLimitPoint x t, ?_, ?_⟩
    · unfold XInfinityGeometricFractal
      rw [Set.mem_iUnion]
      exact ⟨x, ⟨t, ht, rfl⟩⟩
    · exact dist_stageIIGeometricApproxPoint_le ht n x
  · intro y hy
    rcases Set.mem_iUnion.mp hy with ⟨x, hx⟩
    rcases hx with ⟨t, ht, rfl⟩
    refine ⟨stageIIGeometricApproxPoint n x t, ?_, ?_⟩
    · unfold XInfinityGeometricApprox
      rw [Set.mem_iUnion]
      exact ⟨x, ⟨t, ht, rfl⟩⟩
    · simpa [dist_comm] using
        dist_stageIIGeometricApproxPoint_le ht n x

/-- Main metric-convergence theorem: the global finite-depth geometric
approximants converge to the compact Cantor carrier in Hausdorff distance. -/
theorem hausdorffDist_XInfinityGeometricApprox_tendsto_zero :
    Tendsto
      (fun n : Nat =>
        Metric.hausdorffDist
          (XInfinityGeometricApprox n)
          XInfinityGeometricFractal)
      atTop
      (nhds 0) := by
  apply squeeze_zero
  · intro n
    exact Metric.hausdorffDist_nonneg
  · intro n
    exact hausdorffDist_XInfinityGeometricApprox_le n
  · exact stageIIGeometricApproxScale_tendsto_zero

/-!
## Boundary after v4.31

The recursive geometric program now has genuine metric convergence.

For the finite-depth approximants X_n and the geometric Cantor carrier X_inf,

  d_H(X_n, X_inf) ≤ 3^{-n}

and therefore

  d_H(X_n, X_inf) → 0.

The bound is uniform over all eight Stage-II branches.

Together with v4.30, X_inf is compact, closed, nonempty, and exactly
self-similar on each branch.  The next synthesis theorem can therefore package
the Hausdorff-dimension result from v4.29, the topology from v4.30, and the
Hausdorff-metric convergence from v4.31 as one authority-bearing geometric
fractal-limit statement.
-/

end

end KUOS.DependentOriginationStageIICantorMetricConvergenceV4_31
