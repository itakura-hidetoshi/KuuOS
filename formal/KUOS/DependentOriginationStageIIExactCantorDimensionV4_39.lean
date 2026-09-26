import KUOS.DependentOriginationCantorExactDimensionV4_38
import KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30
import Mathlib.Topology.MetricSpace.HausdorffDimension
import Mathlib.Analysis.Normed.Group.AddTorsor
import Mathlib

namespace KUOS.DependentOriginationStageIIExactCantorDimensionV4_39

open MeasureTheory
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26
open KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29
open KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30
open KUOS.DependentOriginationCantorCriticalExponentV4_34
open KUOS.DependentOriginationCantorExactDimensionV4_38

set_option autoImplicit false

noncomputable section

/-!
# Exact Stage-II geometric Cantor dimension v4.39

v4.38 proves the exact Hausdorff dimension of the classical ternary Cantor set:

  dimH cantorSet = logb 3 2 = log 2 / log 3.

v4.30 realizes the Stage-II geometric fractal as the finite union of eight
translated copies of that Cantor set:

  XInfinityGeometricFractal
    = ⋃ x, stageIIGeometricCantorFiber x.

Translation by a fixed real offset is an isometry.  Therefore every branch
fiber has exactly the same Hausdorff dimension as the classical Cantor set.
Since the branch index type is finite, the global carrier has the supremum of
eight identical dimensions, hence the same exact value.

This unit upgrades the earlier v4.32 bound
  dimH XInfinityGeometricFractal <= 1
to the sharp equality
  dimH XInfinityGeometricFractal = log 2 / log 3.
-/

/-- Translation by one fixed Stage-II branch offset is an isometry of ℝ. -/
theorem isometry_stageIICantorTranslate
    (x : StageIIFiniteDepthInverseLimit) :
    Isometry (stageIICantorTranslate x) := by
  have h :
      Isometry
        (fun t : ℝ =>
          t + stageIICurrentBranchOffset x) :=
    (IsometryEquiv.vaddConst
      (stageIICurrentBranchOffset x) : ℝ ≃ᵢ ℝ).isometry
  simpa [stageIICantorTranslate, add_comm] using h

/-- Every translated Stage-II Cantor fiber has the exact classical Cantor
Hausdorff dimension. -/
theorem dimH_stageIIGeometricCantorFiber_eq_cantorCriticalExponent
    (x : StageIIFiniteDepthInverseLimit) :
    dimH (stageIIGeometricCantorFiber x) =
      (cantorCriticalExponent : ENNReal) := by
  unfold stageIIGeometricCantorFiber
  calc
    dimH (stageIICantorTranslate x '' cantorSet) =
        dimH cantorSet :=
      (isometry_stageIICantorTranslate x).dimH_image cantorSet
    _ = (cantorCriticalExponent : ENNReal) :=
      dimH_cantorSet_eq_cantorCriticalExponent

/-- Every translated Stage-II Cantor fiber has exact real Hausdorff dimension
log 2 / log 3. -/
theorem toReal_dimH_stageIIGeometricCantorFiber_eq_log_div_log
    (x : StageIIFiniteDepthInverseLimit) :
    (dimH (stageIIGeometricCantorFiber x)).toReal =
      Real.log 2 / Real.log 3 := by
  rw [dimH_stageIIGeometricCantorFiber_eq_cantorCriticalExponent]
  rw [ENNReal.coe_toReal]
  exact
    cantorCriticalExponentReal_eq_log_div_log.trans'
      cantorCriticalExponent_coe

/-- The full eight-branch Stage-II geometric fractal has the exact Cantor
Hausdorff dimension. -/
theorem dimH_XInfinityGeometricFractal_eq_cantorCriticalExponent :
    dimH XInfinityGeometricFractal =
      (cantorCriticalExponent : ENNReal) := by
  unfold XInfinityGeometricFractal
  rw [dimH_iUnion]
  apply le_antisymm
  · refine iSup_le ?_
    intro x
    exact
      le_of_eq
        (dimH_stageIIGeometricCantorFiber_eq_cantorCriticalExponent x)
  · let x0 : StageIIFiniteDepthInverseLimit :=
      octahedralStageIIParityFaceEquivFiniteDepthInverseLimit .a00b00
    calc
      (cantorCriticalExponent : ENNReal) =
          dimH (stageIIGeometricCantorFiber x0) :=
        (dimH_stageIIGeometricCantorFiber_eq_cantorCriticalExponent x0).symm
      _ ≤
          ⨆ x : StageIIFiniteDepthInverseLimit,
            dimH (stageIIGeometricCantorFiber x) :=
        le_iSup
          (fun x : StageIIFiniteDepthInverseLimit =>
            dimH (stageIIGeometricCantorFiber x))
          x0

/-- ENNReal form of the exact global dimension as log 2 / log 3. -/
theorem dimH_XInfinityGeometricFractal_eq_ofReal_log_div_log :
    dimH XInfinityGeometricFractal =
      ENNReal.ofReal (Real.log 2 / Real.log 3) := by
  rw [dimH_XInfinityGeometricFractal_eq_cantorCriticalExponent]
  calc
    (cantorCriticalExponent : ENNReal) =
        dimH cantorSet :=
      dimH_cantorSet_eq_cantorCriticalExponent.symm
    _ = ENNReal.ofReal (Real.log 2 / Real.log 3) :=
      dimH_cantorSet_eq_ofReal_log_div_log

/-- Requested real-valued exact dimension of the full Stage-II geometric
fractal carrier. -/
theorem toReal_dimH_XInfinityGeometricFractal_eq_log_div_log :
    (dimH XInfinityGeometricFractal).toReal =
      Real.log 2 / Real.log 3 := by
  rw [dimH_XInfinityGeometricFractal_eq_cantorCriticalExponent]
  rw [ENNReal.coe_toReal]
  calc
    (cantorCriticalExponent : ℝ) =
        cantorCriticalExponentReal :=
      cantorCriticalExponent_coe
    _ = Real.log 2 / Real.log 3 :=
      cantorCriticalExponentReal_eq_log_div_log

/-- The geometric Cantor carrier is strictly lower-dimensional than its
dimension-one ambient branch carrier. -/
theorem dimH_XInfinityGeometricFractal_lt_branch :
    dimH XInfinityGeometricFractal <
      dimH XInfinityBranch := by
  rw [dimH_XInfinityGeometricFractal_eq_cantorCriticalExponent,
    dimH_XInfinityBranch_eq_one]
  exact_mod_cast cantorCriticalExponent_lt_one

/-!
## Boundary after v4.39

The Stage-II geometric carrier now has the sharp certified dimension:

  dimH XInfinityGeometricFractal
    = logb 3 2
    = log 2 / log 3.

Moreover, every one of the eight translated fibers has the same exact value,
and the full geometric carrier is strictly lower-dimensional than the
dimension-one ambient branch carrier.

The next theorem unit can upgrade the v4.32 bundled geometric-fractal
certificate itself so that its dimension field records this exact Cantor value
while preserving the existing compactness, closedness, nonemptiness,
self-similarity, inclusion, Hausdorff-rate, and convergence fields.
-/

end

end KUOS.DependentOriginationStageIIExactCantorDimensionV4_39
