import KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29
import Mathlib.Topology.Instances.CantorSet
import Mathlib.Topology.Compactness.Compact
import Mathlib

namespace KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30

open MeasureTheory
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26
open KUOS.DependentOriginationStageIIInverseLimitMiddleSwitchV4_27
open KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29

set_option autoImplicit false

noncomputable section

/-!
# Geometric Cantor topology over the Stage-II branch carrier v4.30

v4.29 proves that the branch carrier has Hausdorff dimension one by retaining
one real segment over each of the eight current inverse-limit points.

The present unit introduces a genuine recursive geometric skeleton inside those
branches: each branch index carries a translated copy of the classical ternary
Cantor set.

For a branch index x with offset a_x, define

  C_x = a_x + CantorSet.

The global geometric carrier is the finite union of these eight translated
Cantor copies.

This file proves the topological layer:

* each branch fiber is compact;
* the global carrier is compact and therefore closed in ℝ;
* the global carrier is nonempty;
* each fiber satisfies the exact two-child similarity equation inherited from
  the classical Cantor set.

No Hausdorff-dimension formula for the Cantor skeleton is asserted here.
The already-certified v4.29 branch carrier remains the dimension-one ambient
branch carrier.
-/

/-- Translation used to place the classical Cantor set inside one Stage-II
branch. -/
noncomputable def stageIICantorTranslate
    (x : StageIIFiniteDepthInverseLimit)
    (t : ℝ) : ℝ :=
  stageIICurrentBranchOffset x + t

/-- One geometric fractal fiber over a current inverse-limit branch index. -/
noncomputable def stageIIGeometricCantorFiber
    (x : StageIIFiniteDepthInverseLimit) : Set ℝ :=
  stageIICantorTranslate x '' cantorSet

/-- The global geometric fractal carrier is the union of the eight translated
Cantor fibers. -/
noncomputable def XInfinityGeometricFractal : Set ℝ :=
  ⋃ x : StageIIFiniteDepthInverseLimit, stageIIGeometricCantorFiber x

/-- Translation by a fixed branch offset is continuous. -/
theorem continuous_stageIICantorTranslate
    (x : StageIIFiniteDepthInverseLimit) :
    Continuous (stageIICantorTranslate x) := by
  simpa [stageIICantorTranslate] using
    (continuous_const.add continuous_id)

/-- Each translated Cantor fiber is compact. -/
theorem isCompact_stageIIGeometricCantorFiber
    (x : StageIIFiniteDepthInverseLimit) :
    IsCompact (stageIIGeometricCantorFiber x) := by
  exact isCompact_cantorSet.image (continuous_stageIICantorTranslate x)

/-- Since there are only eight branch indices, their union is compact. -/
theorem isCompact_XInfinityGeometricFractal :
    IsCompact XInfinityGeometricFractal := by
  unfold XInfinityGeometricFractal
  exact isCompact_iUnion isCompact_stageIIGeometricCantorFiber

/-- The geometric fractal carrier is closed in the real line. -/
theorem isClosed_XInfinityGeometricFractal :
    IsClosed XInfinityGeometricFractal :=
  isCompact_XInfinityGeometricFractal.isClosed

/-- The geometric fractal carrier is nonempty. -/
theorem XInfinityGeometricFractal_nonempty :
    XInfinityGeometricFractal.Nonempty := by
  let x0 : StageIIFiniteDepthInverseLimit :=
    octahedralStageIIParityFaceEquivFiniteDepthInverseLimit .a00b00
  refine ⟨stageIICurrentBranchOffset x0, ?_⟩
  unfold XInfinityGeometricFractal
  rw [Set.mem_iUnion]
  refine ⟨x0, ?_⟩
  unfold stageIIGeometricCantorFiber
  refine ⟨0, zero_mem_cantorSet, ?_⟩
  simp [stageIICantorTranslate]

/-- Each branch fiber satisfies the exact two-child ternary self-similarity
equation. -/
theorem stageIIGeometricCantorFiber_self_similar
    (x : StageIIFiniteDepthInverseLimit) :
    stageIIGeometricCantorFiber x =
      (fun t : ℝ => stageIICurrentBranchOffset x + t / 3) '' cantorSet ∪
      (fun t : ℝ => stageIICurrentBranchOffset x + (2 + t) / 3) '' cantorSet := by
  unfold stageIIGeometricCantorFiber
  calc
    stageIICantorTranslate x '' cantorSet =
        stageIICantorTranslate x ''
          ((fun t : ℝ => t / 3) '' cantorSet ∪
            (fun t : ℝ => (2 + t) / 3) '' cantorSet) := by
      rw [cantorSet_eq_union_halves]
    _ =
        stageIICantorTranslate x '' ((fun t : ℝ => t / 3) '' cantorSet) ∪
          stageIICantorTranslate x ''
            ((fun t : ℝ => (2 + t) / 3) '' cantorSet) := by
      rw [Set.image_union]
    _ =
        (fun t : ℝ => stageIICurrentBranchOffset x + t / 3) '' cantorSet ∪
          (fun t : ℝ => stageIICurrentBranchOffset x + (2 + t) / 3) ''
            cantorSet := by
      rw [Set.image_image, Set.image_image]
      rfl

/-- The geometric fractal carrier is contained in the v4.29 ambient branching
carrier, because the Cantor set lies in the unit interval of each branch. -/
theorem XInfinityGeometricFractal_subset_branch :
    XInfinityGeometricFractal ⊆ XInfinityBranch := by
  intro y hy
  rcases Set.mem_iUnion.mp hy with ⟨x, hx⟩
  rcases hx with ⟨t, htC, rfl⟩
  unfold XInfinityBranch
  rw [Set.mem_iUnion]
  refine ⟨x, ?_⟩
  unfold stageIIBranchFiber stageIICantorTranslate
  rw [segment_eq_Icc (by linarith :
      stageIICurrentBranchOffset x ≤ stageIICurrentBranchOffset x + 1)]
  have ht : t ∈ Set.Icc (0 : ℝ) 1 :=
    cantorSet_subset_unitInterval htC
  exact ⟨by linarith [ht.1], by linarith [ht.2]⟩

/-!
## Boundary after v4.30

The branching program now has a genuine recursive geometric skeleton:

  X_{infinity,geometric}
    = ⋃_x (a_x + CantorSet).

It is compact, closed, nonempty, and each branch fiber satisfies an exact
two-child 1/3-similarity equation.

The carrier remains inside the previously certified dimension-one ambient
branch carrier.

The next unit should formalize finite binary-code approximants and prove metric
convergence to this geometric carrier.  The classical Cantor API in mathlib
already supplies both the digit coding and the exact infinite limit set.
-/

end

end KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30
