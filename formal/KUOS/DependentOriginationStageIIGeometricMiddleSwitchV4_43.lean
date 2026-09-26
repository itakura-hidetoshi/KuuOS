import KUOS.DependentOriginationStageIIHausdorffDimensionJumpV4_42
import KUOS.DependentOriginationStageIIInverseLimitMiddleSwitchV4_27
import KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30
import Mathlib.Analysis.Normed.Group.AddTorsor
import Mathlib

namespace KUOS.DependentOriginationStageIIGeometricMiddleSwitchV4_43

open MeasureTheory
open KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19
open KUOS.DependentOriginationStageIIOrientationMod2CollapseV4_21
open KUOS.DependentOriginationStageIIFiniteDepthRecursiveTransportV4_24
open KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26
open KUOS.DependentOriginationStageIIInverseLimitMiddleSwitchV4_27
open KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29
open KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30

set_option autoImplicit false

noncomputable section

/-!
# Geometric middle-switch symmetry on the Stage-II Cantor carrier v4.43

v4.27 transports the fixed-point-free middle-switch involution from the
eight-label Stage-II source carrier to the set-theoretic inverse-limit branch
index.

v4.30 places one translated copy of the classical Cantor set over each branch
index.  This unit now lifts the middle-switch into that geometric layer without
forgetting branch provenance.

For a branch x, define the ambient translation

  y ↦ y + (offset(mate x) - offset x).

It sends the entire Cantor fiber over x exactly onto the Cantor fiber over
mate x.  Because it is a translation of the real line, it is an isometry and
continuous.  Applying the corresponding mate translation a second time is the
identity.

To make this a genuine global involution without silently identifying branch
provenance, we also introduce a tagged geometric carrier whose points remember

  branch index + real Cantor point + membership certificate.

The middle-switch acts on that tagged carrier by switching the branch and
applying the canonical fiber translation.  The resulting map is involutive,
fixed-point-free, preserves the global geometric Cantor carrier under
realization, and retains the v4.27 orientation-flip provenance at every finite
depth.
-/

/-- The branch offset changes under the fixed-point-free middle-switch mate. -/
theorem stageIICurrentBranchOffset_mate_ne
    (x : StageIIFiniteDepthInverseLimit) :
    stageIICurrentBranchOffset (stageIIInverseLimitMate x) ≠
      stageIICurrentBranchOffset x := by
  unfold stageIICurrentBranchOffset
  rw [stageIIInverseLimitSource_mate]
  cases h : stageIIInverseLimitSource x <;>
    norm_num [h, stageIISourceBranchOffset,
      octahedralStageIIMiddleSwitchMate]

/-- Canonical ambient translation carrying the Cantor fiber over x to the
Cantor fiber over its middle-switch mate. -/
noncomputable def stageIIGeometricMiddleSwitchTranslate
    (x : StageIIFiniteDepthInverseLimit)
    (y : ℝ) : ℝ :=
  y +
    (stageIICurrentBranchOffset (stageIIInverseLimitMate x) -
      stageIICurrentBranchOffset x)

/-- The geometric middle-switch translation sends a branch realization with
Cantor coordinate t to the mate branch with the same Cantor coordinate. -/
theorem stageIIGeometricMiddleSwitchTranslate_translate
    (x : StageIIFiniteDepthInverseLimit)
    (t : ℝ) :
    stageIIGeometricMiddleSwitchTranslate x
        (stageIICantorTranslate x t) =
      stageIICantorTranslate (stageIIInverseLimitMate x) t := by
  unfold stageIIGeometricMiddleSwitchTranslate stageIICantorTranslate
  ring

/-- Each branchwise geometric middle-switch is an isometry of the real line. -/
theorem isometry_stageIIGeometricMiddleSwitchTranslate
    (x : StageIIFiniteDepthInverseLimit) :
    Isometry (stageIIGeometricMiddleSwitchTranslate x) := by
  have hfun :
      stageIIGeometricMiddleSwitchTranslate x =
        (fun y : ℝ =>
          y +
            (stageIICurrentBranchOffset (stageIIInverseLimitMate x) -
              stageIICurrentBranchOffset x)) := by
    rfl
  rw [hfun]
  exact
    (IsometryEquiv.vaddConst
      (stageIICurrentBranchOffset (stageIIInverseLimitMate x) -
        stageIICurrentBranchOffset x) : ℝ ≃ᵢ ℝ).isometry

/-- Hence every branchwise geometric middle-switch is continuous. -/
theorem continuous_stageIIGeometricMiddleSwitchTranslate
    (x : StageIIFiniteDepthInverseLimit) :
    Continuous (stageIIGeometricMiddleSwitchTranslate x) :=
  (isometry_stageIIGeometricMiddleSwitchTranslate x).continuous

/-- The branchwise translation carries one full Cantor fiber exactly to its
middle-switch mate fiber. -/
theorem stageIIGeometricMiddleSwitchTranslate_image_fiber
    (x : StageIIFiniteDepthInverseLimit) :
    stageIIGeometricMiddleSwitchTranslate x ''
        stageIIGeometricCantorFiber x =
      stageIIGeometricCantorFiber (stageIIInverseLimitMate x) := by
  apply Set.Subset.antisymm
  · rintro y ⟨z, hz, rfl⟩
    rcases hz with ⟨t, ht, rfl⟩
    refine ⟨t, ht, ?_⟩
    exact
      (stageIIGeometricMiddleSwitchTranslate_translate x t).symm
  · rintro y ⟨t, ht, rfl⟩
    refine ⟨stageIICantorTranslate x t, ?_, ?_⟩
    · exact ⟨t, ht, rfl⟩
    · exact stageIIGeometricMiddleSwitchTranslate_translate x t

/-- Applying the mate branch translation after the original branch translation
returns every real point exactly. -/
theorem stageIIGeometricMiddleSwitchTranslate_involutive
    (x : StageIIFiniteDepthInverseLimit)
    (y : ℝ) :
    stageIIGeometricMiddleSwitchTranslate
        (stageIIInverseLimitMate x)
        (stageIIGeometricMiddleSwitchTranslate x y) =
      y := by
  unfold stageIIGeometricMiddleSwitchTranslate
  rw [stageIIInverseLimitMate_involutive x]
  ring

/-- The branchwise middle-switch translation has no fixed real point because
the mate branch has a distinct geometric offset. -/
theorem stageIIGeometricMiddleSwitchTranslate_ne_self
    (x : StageIIFiniteDepthInverseLimit)
    (y : ℝ) :
    stageIIGeometricMiddleSwitchTranslate x y ≠ y := by
  intro h
  apply stageIICurrentBranchOffset_mate_ne x
  unfold stageIIGeometricMiddleSwitchTranslate at h
  linarith

/-- A tagged point of the geometric Cantor carrier.  The branch tag is retained
explicitly, so branch provenance is never reconstructed from a bare real
coordinate. -/
structure StageIIGeometricCantorTaggedPoint where
  branch : StageIIFiniteDepthInverseLimit
  point : ℝ
  point_mem : point ∈ stageIIGeometricCantorFiber branch

/-- Two tagged points are equal once their branch tags and real points agree. -/
@[ext] theorem StageIIGeometricCantorTaggedPoint.ext
    {p q : StageIIGeometricCantorTaggedPoint}
    (hbranch : p.branch = q.branch)
    (hpoint : p.point = q.point) :
    p = q := by
  cases p with
  | mk pb pp ph =>
    cases q with
    | mk qb qp qh =>
      simp only at hbranch hpoint
      cases hbranch
      cases hpoint
      rfl

/-- Realization of a tagged geometric point into the ambient real line. -/
def StageIIGeometricCantorTaggedPoint.realize
    (p : StageIIGeometricCantorTaggedPoint) : ℝ :=
  p.point

/-- Every tagged point realizes into the global Stage-II geometric fractal. -/
theorem StageIIGeometricCantorTaggedPoint.realize_mem
    (p : StageIIGeometricCantorTaggedPoint) :
    p.realize ∈ XInfinityGeometricFractal := by
  unfold StageIIGeometricCantorTaggedPoint.realize
  unfold XInfinityGeometricFractal
  rw [Set.mem_iUnion]
  exact ⟨p.branch, p.point_mem⟩

/-- Global geometric middle-switch on the tagged Cantor carrier. -/
noncomputable def stageIIGeometricMiddleSwitch
    (p : StageIIGeometricCantorTaggedPoint) :
    StageIIGeometricCantorTaggedPoint where
  branch := stageIIInverseLimitMate p.branch
  point := stageIIGeometricMiddleSwitchTranslate p.branch p.point
  point_mem := by
    rw [← stageIIGeometricMiddleSwitchTranslate_image_fiber p.branch]
    exact ⟨p.point, p.point_mem, rfl⟩

/-- The geometric middle-switch preserves the branch-level middle-switch
provenance exactly. -/
@[simp] theorem stageIIGeometricMiddleSwitch_branch
    (p : StageIIGeometricCantorTaggedPoint) :
    (stageIIGeometricMiddleSwitch p).branch =
      stageIIInverseLimitMate p.branch := by
  rfl

/-- The real component is exactly the canonical mate-fiber translation. -/
@[simp] theorem stageIIGeometricMiddleSwitch_point
    (p : StageIIGeometricCantorTaggedPoint) :
    (stageIIGeometricMiddleSwitch p).point =
      stageIIGeometricMiddleSwitchTranslate p.branch p.point := by
  rfl

/-- The lifted geometric middle-switch is involutive on the tagged carrier. -/
theorem stageIIGeometricMiddleSwitch_involutive :
    Function.Involutive stageIIGeometricMiddleSwitch := by
  intro p
  apply StageIIGeometricCantorTaggedPoint.ext
  · exact stageIIInverseLimitMate_involutive p.branch
  · exact
      stageIIGeometricMiddleSwitchTranslate_involutive
        p.branch p.point

/-- The lifted geometric middle-switch is therefore injective. -/
theorem stageIIGeometricMiddleSwitch_injective :
    Function.Injective stageIIGeometricMiddleSwitch :=
  stageIIGeometricMiddleSwitch_involutive.injective

/-- The lifted geometric middle-switch has no fixed tagged points. -/
theorem stageIIGeometricMiddleSwitch_ne_self
    (p : StageIIGeometricCantorTaggedPoint) :
    stageIIGeometricMiddleSwitch p ≠ p := by
  intro h
  have hbranch :=
    congrArg StageIIGeometricCantorTaggedPoint.branch h
  exact stageIIInverseLimitMate_ne_self p.branch hbranch

/-- The switched tagged point still realizes into the same global geometric
fractal carrier. -/
theorem stageIIGeometricMiddleSwitch_realize_mem
    (p : StageIIGeometricCantorTaggedPoint) :
    (stageIIGeometricMiddleSwitch p).realize ∈
      XInfinityGeometricFractal :=
  StageIIGeometricCantorTaggedPoint.realize_mem
    (stageIIGeometricMiddleSwitch p)

/-- At every finite depth, the geometric middle-switch retains the exact
orientation-flip provenance proved for the inverse-limit middle-switch. -/
theorem stageIIGeometricMiddleSwitch_orientation_flip
    (p : StageIIGeometricCantorTaggedPoint)
    (depth : Nat) :
    stageIIIncidenceRecursiveDepthCellOrientation
        ((stageIIGeometricMiddleSwitch p).branch.1 depth) =
      stageIIIncidenceOrientationFlip
        (stageIIIncidenceRecursiveDepthCellOrientation
          (p.branch.1 depth)) := by
  exact stageIIInverseLimitMate_orientation_flip p.branch depth

/-- At every finite depth, the switched branch remains on the opposite
recursive inner-face kind. -/
theorem stageIIGeometricMiddleSwitch_opposite_innerKinds
    (p : StageIIGeometricCantorTaggedPoint)
    (depth : Nat) :
    (p.branch.1 depth).innerKind ≠
      ((stageIIGeometricMiddleSwitch p).branch.1 depth).innerKind := by
  exact stageIIInverseLimitMate_opposite_innerKinds p.branch depth

/-!
## Boundary after v4.43

The v4.27 middle-switch now acts canonically on the Stage-II Cantor geometry.

For every branch x:

* the geometric action is an explicit real translation;
* it is an isometry and therefore continuous;
* it sends the complete Cantor fiber over x exactly onto the mate fiber;
* composing the mate translation with the original translation is the identity;
* the translation is fixed-point-free because mate offsets are distinct.

On the provenance-preserving tagged geometric carrier:

* the middle-switch is a global explicit map;
* it is involutive and injective;
* it is fixed-point-free;
* both original and switched points realize into XInfinityGeometricFractal;
* finite-depth orientation flip and opposite-inner-kind semantics are retained.

No quotienting of branch provenance is used.  A later unit may descend this
tagged symmetry to a single piecewise self-homeomorphism of the bare real
carrier, or use the tagged involution to transport orientation/obstruction
data into the metric limit.
-/

end

end KUOS.DependentOriginationStageIIGeometricMiddleSwitchV4_43
