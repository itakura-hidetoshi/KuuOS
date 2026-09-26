import KUOS.DependentOriginationStageIICurrentHausdorffDimensionZeroV4_28
import Mathlib.Topology.MetricSpace.HausdorffDimension
import Mathlib

namespace KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29

open MeasureTheory
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26
open KUOS.DependentOriginationStageIIInverseLimitMiddleSwitchV4_27
open KUOS.DependentOriginationStageIICurrentHausdorffDimensionZeroV4_28

set_option autoImplicit false

noncomputable section

/-!
# Branching Stage-II carrier has positive Hausdorff dimension v4.29

v4.28 proves that the current inverse-limit carrier is an eight-point set and
therefore has Hausdorff dimension zero for every extended metric structure.

This unit is based on the canonical merged v4.28 zero-dimension theorem.

To obtain positive Hausdorff dimension one must genuinely retain additional
branch data rather than merely re-metrize those same eight points.

This file thickens each current inverse-limit point by one nondegenerate real
segment. The eight current points remain the branch indices. Their source
labels determine separated real offsets, while each branch fiber itself is a
unit segment.

Thus the branching carrier is the union of eight one-dimensional fibers.
Mathlib proves that every nondegenerate real segment has Hausdorff dimension
one, and that Hausdorff dimension of a countable union is the supremum of the
dimensions of the pieces. Therefore the branching carrier has Hausdorff
dimension exactly one, hence strictly positive.

This is a genuine metric-dimensional upgrade, but it is a deliberately simple
branch model. It does not yet encode a binary tree, self-similar contraction
ratio, or a Cantor-type branch metric.
-/

/-- Distinct geometric offsets attached to the eight original Stage-II source
labels. Consecutive branch fibers are separated by a gap of length one. -/
def stageIISourceBranchOffset :
    OctahedralStageIIParityFace → ℝ
  | .a00b00 => 0
  | .a01b10 => 2
  | .a00b01 => 4
  | .a01b11 => 6
  | .a10b00 => 8
  | .a11b10 => 10
  | .a10b01 => 12
  | .a11b11 => 14

/-- Offset of one current inverse-limit point, read through its unique v4.26
source label. -/
noncomputable def stageIICurrentBranchOffset
    (x : StageIIFiniteDepthInverseLimit) : ℝ :=
  stageIISourceBranchOffset (stageIIInverseLimitSource x)

/-- One branch fiber over a current inverse-limit point: a nondegenerate unit
segment in the real line. -/
noncomputable def stageIIBranchFiber
    (x : StageIIFiniteDepthInverseLimit) : Set ℝ :=
  segment ℝ
    (stageIICurrentBranchOffset x)
    (stageIICurrentBranchOffset x + 1)

/-- Every branch fiber is nondegenerate. -/
theorem stageIIBranchFiber_endpoints_ne
    (x : StageIIFiniteDepthInverseLimit) :
    stageIICurrentBranchOffset x ≠
      stageIICurrentBranchOffset x + 1 := by
  linarith

/-- Every branch fiber has Hausdorff dimension exactly one. -/
theorem dimH_stageIIBranchFiber_eq_one
    (x : StageIIFiniteDepthInverseLimit) :
    dimH (stageIIBranchFiber x) = 1 := by
  unfold stageIIBranchFiber
  exact Real.dimH_segment (stageIIBranchFiber_endpoints_ne x)

/-- The branching infinite-depth carrier is the union of the eight real branch
fibers indexed by current inverse-limit points. -/
noncomputable def XInfinityBranch : Set ℝ :=
  ⋃ x : StageIIFiniteDepthInverseLimit, stageIIBranchFiber x

/-- The branching carrier has Hausdorff dimension exactly one. -/
theorem dimH_XInfinityBranch_eq_one :
    dimH XInfinityBranch = 1 := by
  change
    dimH
      (⋃ x : StageIIFiniteDepthInverseLimit, stageIIBranchFiber x) =
      1
  rw [dimH_iUnion]
  apply le_antisymm
  · refine iSup_le ?_
    intro x
    exact le_of_eq (dimH_stageIIBranchFiber_eq_one x)
  · calc
      (1 : ENNReal) =
          dimH
            (stageIIBranchFiber
              (octahedralStageIIParityFaceEquivFiniteDepthInverseLimit
                .a00b00)) :=
        (dimH_stageIIBranchFiber_eq_one
          (octahedralStageIIParityFaceEquivFiniteDepthInverseLimit
            .a00b00)).symm
      _ ≤
          ⨆ x : StageIIFiniteDepthInverseLimit,
            dimH (stageIIBranchFiber x) :=
        le_iSup
          (fun x : StageIIFiniteDepthInverseLimit =>
            dimH (stageIIBranchFiber x))
          (octahedralStageIIParityFaceEquivFiniteDepthInverseLimit
            .a00b00)

/-- In particular, the branching carrier has strictly positive Hausdorff
dimension. -/
theorem dimH_XInfinityBranch_pos :
    0 < dimH XInfinityBranch := by
  rw [dimH_XInfinityBranch_eq_one]
  exact zero_lt_one

/-- Direct contrast with the current carrier:
current compatible sections are zero-dimensional, while the new branch carrier
is one-dimensional. -/
theorem current_zero_branch_positive
    [EMetricSpace StageIIFiniteDepthInverseLimit] :
    dimH XInfinityCurrent = 0 ∧
      0 < dimH XInfinityBranch := by
  exact ⟨dimH_XInfinityCurrent_eq_zero, dimH_XInfinityBranch_pos⟩

/-!
## Boundary after v4.29

The requested dimension contrast is now formalized:

  dim_H(X_{infinity,current}) = 0,
  dim_H(X_{infinity,branch}) = 1 > 0.

The reason for the change is structural.

Current carrier:
* every compatible section is rigidly determined by one of eight source labels;
* hence the whole carrier has eight points.

Branching carrier:
* each of those eight points retains an independent nondegenerate real branch
  fiber;
* each fiber has Hausdorff dimension one;
* the finite/countable union has Hausdorff dimension one.

This branching construction is intentionally minimal. It establishes positive
Hausdorff dimension without claiming metric self-similarity of the earlier
pentagram/hexagram recursion.

A later theorem may replace the real-segment fibers by a recursively branching
ultrametric or Cantor-type carrier and compute its dimension from a proved
branching number and contraction ratio.
-/

end

end KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29
