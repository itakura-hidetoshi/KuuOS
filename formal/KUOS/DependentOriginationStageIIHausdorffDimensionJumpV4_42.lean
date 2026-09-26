import KUOS.DependentOriginationStageIIFiniteApproxDimensionV4_41
import Mathlib.Topology.MetricSpace.HausdorffDimension
import Mathlib.Topology.MetricSpace.HausdorffDistance
import Mathlib.Topology.Instances.ENNReal
import Mathlib

namespace KUOS.DependentOriginationStageIIHausdorffDimensionJumpV4_42

open Filter
open MeasureTheory
open KUOS.DependentOriginationStageIICantorMetricConvergenceV4_31
open KUOS.DependentOriginationCantorCriticalExponentV4_34
open KUOS.DependentOriginationStageIIExactCantorDimensionV4_39
open KUOS.DependentOriginationStageIIFiniteApproxDimensionV4_41

set_option autoImplicit false

noncomputable section

/-!
# Hausdorff-limit dimension jump for the Stage-II geometric carrier v4.42

v4.31 proves that the finite-depth geometric approximants converge to the
Stage-II geometric Cantor carrier in Hausdorff distance, with the explicit
rate

  d_H(X_n, X_infinity) <= 3^{-n}.

v4.39 proves the exact positive dimension of the limit:

  dimH X_infinity = logb 3 2 = log 2 / log 3.

v4.41 proves that every finite-depth approximant is finite and therefore has

  dimH X_n = 0.

This unit packages these already-validated facts into one dimension-jump
certificate and records the stronger sequential consequence:

  the Hausdorff distances tend to zero,
  but the Hausdorff dimensions do not tend to the Hausdorff dimension of the
  limit.

Indeed the dimension sequence is identically zero, while the limit dimension
is strictly positive.

This is a concrete theorem internal to the Stage-II construction; no general
continuity or semicontinuity principle for Hausdorff dimension is assumed.
-/

/-- The exact Cantor limit dimension is strictly positive. -/
theorem dimH_XInfinityGeometricFractal_pos :
    0 < dimH XInfinityGeometricFractal := by
  rw [dimH_XInfinityGeometricFractal_eq_cantorCriticalExponent]
  exact_mod_cast cantorCriticalExponent_pos

/-- Every finite-depth approximant has strictly smaller Hausdorff dimension
than the geometric limit. -/
theorem dimH_XInfinityGeometricApprox_lt_limit
    (n : Nat) :
    dimH (XInfinityGeometricApprox n) <
      dimH XInfinityGeometricFractal := by
  rw [dimH_XInfinityGeometricApprox_eq_zero]
  exact dimH_XInfinityGeometricFractal_pos

/-- The Hausdorff-dimension sequence of the finite approximants converges to
zero, because it is identically zero. -/
theorem dimH_XInfinityGeometricApprox_tendsto_zero :
    Tendsto
      (fun n : Nat => dimH (XInfinityGeometricApprox n))
      atTop
      (nhds 0) := by
  have hconst :
      Tendsto
        (fun _ : Nat => (0 : ENNReal))
        atTop
        (nhds 0) :=
    tendsto_const_nhds
  simpa only [dimH_XInfinityGeometricApprox_eq_zero] using hconst

/-- Although the sets converge in Hausdorff distance, their Hausdorff
dimensions do not converge to the Hausdorff dimension of the limit. -/
theorem dimH_XInfinityGeometricApprox_not_tendsto_limit :
    ¬ Tendsto
        (fun n : Nat => dimH (XInfinityGeometricApprox n))
        atTop
        (nhds (dimH XInfinityGeometricFractal)) := by
  intro hlimit
  have heq :
      dimH XInfinityGeometricFractal = 0 :=
    tendsto_nhds_unique
      hlimit
      dimH_XInfinityGeometricApprox_tendsto_zero
  exact (ne_of_gt dimH_XInfinityGeometricFractal_pos) heq

/-- Bundled certificate for the concrete Hausdorff-limit dimension jump. -/
structure StageIIHausdorffDimensionJumpCertificate where
  approximantFinite :
    ∀ n, (XInfinityGeometricApprox n).Finite
  approximantDimensionZero :
    ∀ n, dimH (XInfinityGeometricApprox n) = 0
  hausdorffRate :
    ∀ n,
      Metric.hausdorffDist
          (XInfinityGeometricApprox n)
          XInfinityGeometricFractal ≤
        (3 : ℝ)⁻¹ ^ n
  hausdorffConvergence :
    Tendsto
      (fun n : Nat =>
        Metric.hausdorffDist
          (XInfinityGeometricApprox n)
          XInfinityGeometricFractal)
      atTop
      (nhds 0)
  limitExactDimension :
    dimH XInfinityGeometricFractal =
      (cantorCriticalExponent : ENNReal)
  limitExactDimensionReal :
    (dimH XInfinityGeometricFractal).toReal =
      Real.log 2 / Real.log 3
  limitDimensionPositive :
    0 < dimH XInfinityGeometricFractal
  pointwiseDimensionGap :
    ∀ n,
      dimH (XInfinityGeometricApprox n) <
        dimH XInfinityGeometricFractal
  approximantDimensionsTendToZero :
    Tendsto
      (fun n : Nat => dimH (XInfinityGeometricApprox n))
      atTop
      (nhds 0)
  approximantDimensionsDoNotTendToLimit :
    ¬ Tendsto
        (fun n : Nat => dimH (XInfinityGeometricApprox n))
        atTop
        (nhds (dimH XInfinityGeometricFractal))

/-- Canonical v4.42 certificate assembled from v4.31, v4.39, and v4.41. -/
noncomputable def stageIIHausdorffDimensionJumpCertificate :
    StageIIHausdorffDimensionJumpCertificate where
  approximantFinite :=
    XInfinityGeometricApprox_finite
  approximantDimensionZero :=
    dimH_XInfinityGeometricApprox_eq_zero
  hausdorffRate :=
    hausdorffDist_XInfinityGeometricApprox_le
  hausdorffConvergence :=
    hausdorffDist_XInfinityGeometricApprox_tendsto_zero
  limitExactDimension :=
    dimH_XInfinityGeometricFractal_eq_cantorCriticalExponent
  limitExactDimensionReal :=
    toReal_dimH_XInfinityGeometricFractal_eq_log_div_log
  limitDimensionPositive :=
    dimH_XInfinityGeometricFractal_pos
  pointwiseDimensionGap :=
    dimH_XInfinityGeometricApprox_lt_limit
  approximantDimensionsTendToZero :=
    dimH_XInfinityGeometricApprox_tendsto_zero
  approximantDimensionsDoNotTendToLimit :=
    dimH_XInfinityGeometricApprox_not_tendsto_limit

/-- Final v4.42 synthesis theorem.

The finite approximants have dimension zero and converge in Hausdorff distance
to a positive-dimensional Cantor limit, while the dimension sequence itself
does not converge to the dimension of that limit. -/
theorem stageII_hausdorff_limit_dimension_jump :
    (∀ n, (XInfinityGeometricApprox n).Finite) ∧
      (∀ n, dimH (XInfinityGeometricApprox n) = 0) ∧
      (∀ n,
        Metric.hausdorffDist
            (XInfinityGeometricApprox n)
            XInfinityGeometricFractal ≤
          (3 : ℝ)⁻¹ ^ n) ∧
      Tendsto
        (fun n : Nat =>
          Metric.hausdorffDist
            (XInfinityGeometricApprox n)
            XInfinityGeometricFractal)
        atTop
        (nhds 0) ∧
      dimH XInfinityGeometricFractal =
        (cantorCriticalExponent : ENNReal) ∧
      (dimH XInfinityGeometricFractal).toReal =
        Real.log 2 / Real.log 3 ∧
      0 < dimH XInfinityGeometricFractal ∧
      (∀ n,
        dimH (XInfinityGeometricApprox n) <
          dimH XInfinityGeometricFractal) ∧
      Tendsto
        (fun n : Nat => dimH (XInfinityGeometricApprox n))
        atTop
        (nhds 0) ∧
      ¬ Tendsto
          (fun n : Nat => dimH (XInfinityGeometricApprox n))
          atTop
          (nhds (dimH XInfinityGeometricFractal)) := by
  exact
    ⟨stageIIHausdorffDimensionJumpCertificate.approximantFinite,
      stageIIHausdorffDimensionJumpCertificate.approximantDimensionZero,
      stageIIHausdorffDimensionJumpCertificate.hausdorffRate,
      stageIIHausdorffDimensionJumpCertificate.hausdorffConvergence,
      stageIIHausdorffDimensionJumpCertificate.limitExactDimension,
      stageIIHausdorffDimensionJumpCertificate.limitExactDimensionReal,
      stageIIHausdorffDimensionJumpCertificate.limitDimensionPositive,
      stageIIHausdorffDimensionJumpCertificate.pointwiseDimensionGap,
      stageIIHausdorffDimensionJumpCertificate.approximantDimensionsTendToZero,
      stageIIHausdorffDimensionJumpCertificate.approximantDimensionsDoNotTendToLimit⟩

/-!
## Boundary after v4.42

The finite-depth/limit dimension contrast is now completely formalized:

  for every n,
    X_n is finite,
    dimH X_n = 0;

  d_H(X_n, X_infinity) <= 3^{-n};
  d_H(X_n, X_infinity) -> 0;

  dimH X_infinity
    = logb 3 2
    = log 2 / log 3
    > 0.

Moreover,

  dimH X_n -> 0

and therefore

  dimH X_n does not tend to dimH X_infinity.

Thus this specific Stage-II sequence gives an explicit internal witness that
Hausdorff convergence of compact geometric approximants does not force
continuity of Hausdorff dimension.

The exact Cantor-dimension and finite-approximant programs are now both closed.
A later theorem unit can move to critical Hausdorff measure, quantitative
covering content, or a higher structural interpretation.
-/

end

end KUOS.DependentOriginationStageIIHausdorffDimensionJumpV4_42
