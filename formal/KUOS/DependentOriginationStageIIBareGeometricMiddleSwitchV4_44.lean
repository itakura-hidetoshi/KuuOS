import KUOS.DependentOriginationStageIIGeometricMiddleSwitchV4_43
import Mathlib.Topology.Instances.CantorSet
import Mathlib

namespace KUOS.DependentOriginationStageIIBareGeometricMiddleSwitchV4_44

open MeasureTheory
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19
open KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26
open KUOS.DependentOriginationStageIIInverseLimitMiddleSwitchV4_27
open KUOS.DependentOriginationStageIIBranchingPositiveHausdorffV4_29
open KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30
open KUOS.DependentOriginationStageIIGeometricMiddleSwitchV4_43

set_option autoImplicit false

noncomputable section

/-!
# Descent of the geometric middle-switch to the bare real Cantor carrier v4.44

v4.43 constructs the geometric middle-switch on a tagged carrier.  The branch
tag is retained explicitly there because a bare real coordinate should not be
asked to remember provenance unless uniqueness has first been proved.

The present unit proves that uniqueness.

The eight Stage-II branch offsets are

  0, 2, 4, 6, 8, 10, 12, 14,

while every Cantor coordinate lies in [0,1].  Hence distinct translated Cantor
fibers are disjoint.  Every point of XInfinityGeometricFractal therefore lies
in one unique branch fiber.

This permits a canonical noncomputable branch selector on the bare real
carrier.  Using that selector we descend the tagged middle-switch to a genuine
fixed-point-free involution of the subtype

  {y : ℝ // y ∈ XInfinityGeometricFractal}.

The final compatibility theorem proves that the square formed by tagged
realization and the two middle-switch maps commutes.  Thus v4.44 is an actual
descent theorem: the tagged symmetry is not merely analogous to a bare-real
symmetry; it induces it.
-/

/-- The explicit eight real branch offsets are injective. -/
theorem stageIISourceBranchOffset_injective :
    Function.Injective stageIISourceBranchOffset := by
  intro f g h
  cases f <;> cases g <;>
    norm_num [stageIISourceBranchOffset] at h ⊢

/-- Distinct source labels have branch offsets separated by at least two. -/
theorem stageIISourceBranchOffset_separated
    {f g : OctahedralStageIIParityFace}
    (hfg : f ≠ g) :
    (2 : ℝ) ≤
      |stageIISourceBranchOffset f - stageIISourceBranchOffset g| := by
  cases f <;> cases g <;>
    norm_num [stageIISourceBranchOffset] at hfg ⊢

/-- The real branch-offset function is injective on inverse-limit branches. -/
theorem stageIICurrentBranchOffset_injective :
    Function.Injective stageIICurrentBranchOffset := by
  intro x y hxy
  apply octahedralStageIIParityFaceEquivFiniteDepthInverseLimit.symm.injective
  apply stageIISourceBranchOffset_injective
  simpa [stageIICurrentBranchOffset, stageIIInverseLimitSource] using hxy

/-- Distinct inverse-limit branches retain the same two-unit offset
separation. -/
theorem stageIICurrentBranchOffset_separated
    {x y : StageIIFiniteDepthInverseLimit}
    (hxy : x ≠ y) :
    (2 : ℝ) ≤
      |stageIICurrentBranchOffset x - stageIICurrentBranchOffset y| := by
  have hsource :
      stageIIInverseLimitSource x ≠ stageIIInverseLimitSource y := by
    intro h
    apply hxy
    exact
      octahedralStageIIParityFaceEquivFiniteDepthInverseLimit.symm.injective
        (by
          simpa [stageIIInverseLimitSource] using h)
  simpa [stageIICurrentBranchOffset] using
    stageIISourceBranchOffset_separated hsource

/-- A real point cannot belong to two different translated Cantor fibers.
Therefore fiber membership determines the branch uniquely. -/
theorem stageIIGeometricCantorFiber_branch_unique
    {x y : StageIIFiniteDepthInverseLimit}
    {z : ℝ}
    (hx : z ∈ stageIIGeometricCantorFiber x)
    (hy : z ∈ stageIIGeometricCantorFiber y) :
    x = y := by
  unfold stageIIGeometricCantorFiber at hx hy
  rcases hx with ⟨tx, htxC, hzx⟩
  rcases hy with ⟨ty, htyC, hzy⟩
  have htxI : tx ∈ Set.Icc (0 : ℝ) 1 :=
    cantorSet_subset_unitInterval htxC
  have htyI : ty ∈ Set.Icc (0 : ℝ) 1 :=
    cantorSet_subset_unitInterval htyC
  have hsame :
      stageIICantorTranslate x tx =
        stageIICantorTranslate y ty :=
    hzx.trans hzy.symm
  by_contra hxy
  have hsep := stageIICurrentBranchOffset_separated hxy
  have hupper :
      |stageIICurrentBranchOffset x -
        stageIICurrentBranchOffset y| ≤ 1 := by
    rw [abs_le]
    unfold stageIICantorTranslate at hsame
    constructor <;>
      linarith [htxI.1, htxI.2, htyI.1, htyI.2]
  linarith

/-- Equivalently, distinct translated Cantor fibers are disjoint. -/
theorem stageIIGeometricCantorFiber_disjoint
    {x y : StageIIFiniteDepthInverseLimit}
    (hxy : x ≠ y) :
    Disjoint
      (stageIIGeometricCantorFiber x)
      (stageIIGeometricCantorFiber y) := by
  rw [Set.disjoint_left]
  intro z hx hy
  exact hxy (stageIIGeometricCantorFiber_branch_unique hx hy)

/-- The bare real geometric carrier, with only global membership retained. -/
def StageIIGeometricCantorCarrier : Type :=
  {z : ℝ // z ∈ XInfinityGeometricFractal}

/-- Every bare geometric point lies in one unique branch fiber. -/
theorem StageIIGeometricCantorCarrier.existsUnique_branch
    (p : StageIIGeometricCantorCarrier) :
    ∃! x : StageIIFiniteDepthInverseLimit,
      p.1 ∈ stageIIGeometricCantorFiber x := by
  have hp := p.property
  unfold XInfinityGeometricFractal at hp
  rcases Set.mem_iUnion.mp hp with ⟨x, hx⟩
  refine ⟨x, hx, ?_⟩
  intro y hy
  exact stageIIGeometricCantorFiber_branch_unique hy hx

/-- Canonical branch selected by the unique-fiber theorem. -/
noncomputable def stageIIGeometricBranch
    (p : StageIIGeometricCantorCarrier) :
    StageIIFiniteDepthInverseLimit :=
  Classical.choose
    (StageIIGeometricCantorCarrier.existsUnique_branch p).exists

/-- The selected branch really contains the bare geometric point. -/
theorem stageIIGeometricBranch_mem
    (p : StageIIGeometricCantorCarrier) :
    p.1 ∈ stageIIGeometricCantorFiber (stageIIGeometricBranch p) := by
  exact
    Classical.choose_spec
      (StageIIGeometricCantorCarrier.existsUnique_branch p).exists

/-- Any certified branch containing the point is the canonical selected
branch. -/
theorem stageIIGeometricBranch_eq_of_mem
    (p : StageIIGeometricCantorCarrier)
    {x : StageIIFiniteDepthInverseLimit}
    (hx : p.1 ∈ stageIIGeometricCantorFiber x) :
    stageIIGeometricBranch p = x := by
  exact
    stageIIGeometricCantorFiber_branch_unique
      (stageIIGeometricBranch_mem p) hx

/-- Forget the explicit branch tag while retaining global geometric
membership. -/
def stageIIGeometricTaggedToCarrier
    (p : StageIIGeometricCantorTaggedPoint) :
    StageIIGeometricCantorCarrier :=
  ⟨p.realize, p.realize_mem⟩

/-- Recover the unique branch tag from a bare geometric point. -/
noncomputable def stageIIGeometricCarrierToTagged
    (p : StageIIGeometricCantorCarrier) :
    StageIIGeometricCantorTaggedPoint where
  branch := stageIIGeometricBranch p
  point := p.1
  point_mem := stageIIGeometricBranch_mem p

/-- Tagged and bare carriers are equivalent because branch provenance is
uniquely recoverable from the real point. -/
noncomputable def stageIIGeometricTaggedEquivCarrier :
    StageIIGeometricCantorTaggedPoint ≃ StageIIGeometricCantorCarrier where
  toFun := stageIIGeometricTaggedToCarrier
  invFun := stageIIGeometricCarrierToTagged
  left_inv := by
    intro p
    apply StageIIGeometricCantorTaggedPoint.ext
    · exact
        stageIIGeometricBranch_eq_of_mem
          (stageIIGeometricTaggedToCarrier p) p.point_mem
    · rfl
  right_inv := by
    intro p
    apply Subtype.ext
    rfl

/-- The descended middle-switch on the bare real geometric carrier. -/
noncomputable def stageIIGeometricCarrierMiddleSwitch
    (p : StageIIGeometricCantorCarrier) :
    StageIIGeometricCantorCarrier where
  val :=
    stageIIGeometricMiddleSwitchTranslate
      (stageIIGeometricBranch p) p.1
  property := by
    unfold XInfinityGeometricFractal
    rw [Set.mem_iUnion]
    refine
      ⟨stageIIInverseLimitMate (stageIIGeometricBranch p), ?_⟩
    rw [← stageIIGeometricMiddleSwitchTranslate_image_fiber
      (stageIIGeometricBranch p)]
    exact
      ⟨p.1, stageIIGeometricBranch_mem p, rfl⟩

/-- The descended point lies specifically in the mate of its selected source
branch. -/
theorem stageIIGeometricCarrierMiddleSwitch_mem_mate
    (p : StageIIGeometricCantorCarrier) :
    (stageIIGeometricCarrierMiddleSwitch p).1 ∈
      stageIIGeometricCantorFiber
        (stageIIInverseLimitMate (stageIIGeometricBranch p)) := by
  rw [← stageIIGeometricMiddleSwitchTranslate_image_fiber
    (stageIIGeometricBranch p)]
  exact
    ⟨p.1, stageIIGeometricBranch_mem p, rfl⟩

/-- The unique branch selected after switching is exactly the middle-switch
mate of the original selected branch. -/
@[simp] theorem stageIIGeometricBranch_middleSwitch
    (p : StageIIGeometricCantorCarrier) :
    stageIIGeometricBranch (stageIIGeometricCarrierMiddleSwitch p) =
      stageIIInverseLimitMate (stageIIGeometricBranch p) := by
  exact
    stageIIGeometricBranch_eq_of_mem
      (stageIIGeometricCarrierMiddleSwitch p)
      (stageIIGeometricCarrierMiddleSwitch_mem_mate p)

/-- The descended middle-switch is involutive on the bare real carrier. -/
theorem stageIIGeometricCarrierMiddleSwitch_involutive :
    Function.Involutive stageIIGeometricCarrierMiddleSwitch := by
  intro p
  apply Subtype.ext
  change
    stageIIGeometricMiddleSwitchTranslate
        (stageIIGeometricBranch
          (stageIIGeometricCarrierMiddleSwitch p))
        (stageIIGeometricMiddleSwitchTranslate
          (stageIIGeometricBranch p) p.1) =
      p.1
  rw [stageIIGeometricBranch_middleSwitch]
  exact
    stageIIGeometricMiddleSwitchTranslate_involutive
      (stageIIGeometricBranch p) p.1

/-- Therefore the bare middle-switch is injective. -/
theorem stageIIGeometricCarrierMiddleSwitch_injective :
    Function.Injective stageIIGeometricCarrierMiddleSwitch :=
  stageIIGeometricCarrierMiddleSwitch_involutive.injective

/-- The bare middle-switch has no fixed geometric point. -/
theorem stageIIGeometricCarrierMiddleSwitch_ne_self
    (p : StageIIGeometricCantorCarrier) :
    stageIIGeometricCarrierMiddleSwitch p ≠ p := by
  intro h
  have hbranch :=
    congrArg stageIIGeometricBranch h
  rw [stageIIGeometricBranch_middleSwitch] at hbranch
  exact
    stageIIInverseLimitMate_ne_self
      (stageIIGeometricBranch p) hbranch

/-- Package the descended involution as an actual self-equivalence of the bare
geometric carrier. -/
noncomputable def stageIIGeometricCarrierMiddleSwitchEquiv :
    StageIIGeometricCantorCarrier ≃ StageIIGeometricCantorCarrier where
  toFun := stageIIGeometricCarrierMiddleSwitch
  invFun := stageIIGeometricCarrierMiddleSwitch
  left_inv := stageIIGeometricCarrierMiddleSwitch_involutive
  right_inv := stageIIGeometricCarrierMiddleSwitch_involutive

/-- The bare map is exactly the realization of the tagged v4.43 map on the
canonical recovered tag. -/
theorem stageIIGeometricCarrierMiddleSwitch_eq_tagged_realization
    (p : StageIIGeometricCantorCarrier) :
    (stageIIGeometricCarrierMiddleSwitch p).1 =
      (stageIIGeometricMiddleSwitch
        (stageIIGeometricCarrierToTagged p)).realize := by
  rfl

/-- Full descent compatibility: realize after the tagged middle-switch equals
bare middle-switch after realization. -/
theorem stageIIGeometricMiddleSwitch_descent
    (p : StageIIGeometricCantorTaggedPoint) :
    stageIIGeometricCarrierMiddleSwitch
        (stageIIGeometricTaggedToCarrier p) =
      stageIIGeometricTaggedToCarrier
        (stageIIGeometricMiddleSwitch p) := by
  apply Subtype.ext
  change
    stageIIGeometricMiddleSwitchTranslate
        (stageIIGeometricBranch
          (stageIIGeometricTaggedToCarrier p))
        p.point =
      stageIIGeometricMiddleSwitchTranslate p.branch p.point
  rw [stageIIGeometricBranch_eq_of_mem
    (stageIIGeometricTaggedToCarrier p) p.point_mem]

/-!
## Boundary after v4.44

The tagged middle-switch of v4.43 has now descended to the bare real geometric
carrier.

The decisive new theorem is branch uniqueness:

* source offsets are injective and separated by at least two;
* Cantor coordinates lie in [0,1];
* therefore distinct translated Cantor fibers are disjoint;
* every point of XInfinityGeometricFractal has one unique branch provenance.

Consequently:

* tagged and bare geometric carriers are equivalent;
* the bare carrier has a canonical middle-switch;
* the bare middle-switch is involutive and injective;
* it is fixed-point-free;
* its selected branch is exactly the mate branch;
* the tagged and bare actions satisfy an exact commuting descent square.

Thus the provenance tag introduced in v4.43 was a safe construction device,
not extra mathematical data.  The branch geometry itself makes provenance
recoverable from the bare real point.

A subsequent unit can add topological structure to the descended involution,
for example proving continuity/homeomorphism from the finite clopen branch
decomposition, or transport the orientation/obstruction semantics through the
tagged-bare equivalence.
-/

end

end KUOS.DependentOriginationStageIIBareGeometricMiddleSwitchV4_44
