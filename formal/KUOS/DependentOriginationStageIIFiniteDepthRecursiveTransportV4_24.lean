import KUOS.DependentOriginationStageIIOneStepRecursiveTransportV4_23
import KUOS.DependentOriginationTruncatedIcosahedralRecursiveRefinementV3_90
import Mathlib

namespace KUOS.DependentOriginationStageIIFiniteDepthRecursiveTransportV4_24

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationStageIIObstructionClassV4_12
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19
open KUOS.DependentOriginationStageIIIncidencePushforwardV4_20
open KUOS.DependentOriginationStageIIOrientationMod2CollapseV4_21
open KUOS.DependentOriginationStageIIIntegralOrientationLiftV4_22
open KUOS.DependentOriginationStageIIOneStepRecursiveTransportV4_23
open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationTruncatedIcosahedralRecursiveRefinementV3_90

set_option autoImplicit false

noncomputable section

/-!
# Finite-depth recursive transport of the Stage-II carrier v4.24

v4.23 proves one-step preservation for the central-cell pullback semantics.
The present file extends that theorem to every finite recursive depth.

The key existing input is v3.90:

  truncatedIcosahedralRecursiveFaceKind depth k = k

for every natural-number depth and every pentagon/hexagon face kind.

Accordingly, each of the eight globally placed Stage-II faces is transported
along its own central-cell tower.  The original incidence-selected seed face is
retained as provenance at every depth, so the eight supports never collapse
into one local five- or six-crossing star.

At depth n:

* the recursive inner face kind is the v3.90 n-fold face-kind iterate;
* the inner boundary arity is the corresponding polygonal arity;
* orientation is recomputed from that inner face kind;
* the integer scalar representative is pulled back from the retained parent.

Because the recursive face kind is stable at every finite depth, every
depth-indexed integer representative equals its v4.22 parent representative.
Hence the full eight-term integer total and mismatch are depth-invariant, and
their mod-two reduction is always the same nonzero v4.12 Stage-II obstruction.

No infinite-depth limit, metric contraction, Euclidean similarity, or
Hausdorff-dimension assertion is made.
-/

/-- Central recursive cell at a specified finite depth above one
incidence-selected seed face.  The original parent face is retained explicitly
as global provenance. -/
structure StageIIIncidenceRecursiveDepthCell where
  parent : OctahedralStageIIIncidenceSeedFace
  depth : Nat
  innerKind : TruncatedIcosahedralFaceKind
  innerBoundaryLength : Nat
  innerKind_eq :
    innerKind =
      truncatedIcosahedralRecursiveFaceKind depth
        (truncatedIcosahedralSeedFaceKind parent.1)
  innerBoundaryLength_eq :
    innerBoundaryLength =
      truncatedIcosahedralFaceSides innerKind

/-- Canonical finite-depth central cell supplied by the v3.90 recursive
face-kind operator. -/
def stageIIIncidenceRecursiveDepthCell
    (depth : Nat)
    (g : OctahedralStageIIIncidenceSeedFace) :
    StageIIIncidenceRecursiveDepthCell where
  parent := g
  depth := depth
  innerKind :=
    truncatedIcosahedralRecursiveFaceKind depth
      (truncatedIcosahedralSeedFaceKind g.1)
  innerBoundaryLength :=
    truncatedIcosahedralFaceSides
      (truncatedIcosahedralRecursiveFaceKind depth
        (truncatedIcosahedralSeedFaceKind g.1))
  innerKind_eq := rfl
  innerBoundaryLength_eq := rfl

@[simp] theorem stageIIIncidenceRecursiveDepthCell_parent
    (depth : Nat)
    (g : OctahedralStageIIIncidenceSeedFace) :
    (stageIIIncidenceRecursiveDepthCell depth g).parent = g := by
  rfl

@[simp] theorem stageIIIncidenceRecursiveDepthCell_depth
    (depth : Nat)
    (g : OctahedralStageIIIncidenceSeedFace) :
    (stageIIIncidenceRecursiveDepthCell depth g).depth = depth := by
  rfl

/-- Every finite recursive depth preserves the parent polygonal face kind. -/
@[simp] theorem stageIIIncidenceRecursiveDepthCell_innerKind
    (depth : Nat)
    (g : OctahedralStageIIIncidenceSeedFace) :
    (stageIIIncidenceRecursiveDepthCell depth g).innerKind =
      truncatedIcosahedralSeedFaceKind g.1 := by
  exact
    truncatedIcosahedralRecursiveFaceKind_eq depth
      (truncatedIcosahedralSeedFaceKind g.1)

/-- Consequently every finite recursive depth preserves the parent boundary
arity. -/
@[simp] theorem stageIIIncidenceRecursiveDepthCell_innerBoundaryLength
    (depth : Nat)
    (g : OctahedralStageIIIncidenceSeedFace) :
    (stageIIIncidenceRecursiveDepthCell depth g).innerBoundaryLength =
      truncatedIcosahedralFaceSides
        (truncatedIcosahedralSeedFaceKind g.1) := by
  simp [stageIIIncidenceRecursiveDepthCell]

/-- At every fixed depth, retaining the parent projection makes the central-cell
transport injective on the global face support. -/
theorem stageIIIncidenceRecursiveDepthCell_injective
    (depth : Nat) :
    Function.Injective (stageIIIncidenceRecursiveDepthCell depth) := by
  intro g h hEq
  exact congrArg
    (fun c : StageIIIncidenceRecursiveDepthCell => c.parent) hEq

/-- Place each Stage-II source label on its own finite-depth central recursive
cell. -/
def octahedralStageIIFiniteDepthChildPlacement
    (depth : Nat)
    (f : OctahedralStageIIParityFace) :
    StageIIIncidenceRecursiveDepthCell :=
  stageIIIncidenceRecursiveDepthCell depth
    (octahedralStageIIIncidenceSeedEquiv f)

/-- The full eight-label global support remains injective at every finite
depth. -/
theorem octahedralStageIIFiniteDepthChildPlacement_injective
    (depth : Nat) :
    Function.Injective
      (octahedralStageIIFiniteDepthChildPlacement depth) := by
  intro f g hEq
  apply octahedralStageIIIncidenceSeedEquiv.injective
  exact congrArg
    (fun c : StageIIIncidenceRecursiveDepthCell => c.parent) hEq

/-- Middle-switch mates retain opposite recursive inner face kinds at every
finite depth. -/
theorem octahedralStageIIFiniteDepthChildPlacement_mates_opposite_innerKinds
    (depth : Nat)
    (f : OctahedralStageIIParityFace) :
    (octahedralStageIIFiniteDepthChildPlacement depth f).innerKind ≠
      (octahedralStageIIFiniteDepthChildPlacement depth
        (octahedralStageIIMiddleSwitchMate f)).innerKind := by
  simpa [octahedralStageIIFiniteDepthChildPlacement] using
    octahedralStageIIIncidenceSeedEquiv_mates_opposite_kinds f

/-- Orientation at finite depth is determined by the actual recursive inner
face kind. -/
def stageIIIncidenceRecursiveDepthCellOrientation
    (c : StageIIIncidenceRecursiveDepthCell) :
    StageIIIncidenceOrientation :=
  stageIIIncidenceFaceKindOrientation c.innerKind

/-- Since v3.90 preserves face kind at all finite depths, the recursive
orientation is exactly the original parent orientation. -/
@[simp] theorem stageIIIncidenceRecursiveDepthCellOrientation_eq_parent
    (depth : Nat)
    (g : OctahedralStageIIIncidenceSeedFace) :
    stageIIIncidenceRecursiveDepthCellOrientation
        (stageIIIncidenceRecursiveDepthCell depth g) =
      stageIIIncidenceSeedFaceOrientation g := by
  simp [stageIIIncidenceRecursiveDepthCellOrientation,
    stageIIIncidenceSeedFaceOrientation]

/-- Middle-switch mates therefore retain opposite orientations at every finite
depth. -/
theorem octahedralStageIIFiniteDepthChildPlacement_mates_orientation_flip
    (depth : Nat)
    (f : OctahedralStageIIParityFace) :
    stageIIIncidenceRecursiveDepthCellOrientation
        (octahedralStageIIFiniteDepthChildPlacement depth
          (octahedralStageIIMiddleSwitchMate f)) =
      stageIIIncidenceOrientationFlip
        (stageIIIncidenceRecursiveDepthCellOrientation
          (octahedralStageIIFiniteDepthChildPlacement depth f)) := by
  rw [octahedralStageIIFiniteDepthChildPlacement,
    octahedralStageIIFiniteDepthChildPlacement,
    stageIIIncidenceRecursiveDepthCellOrientation_eq_parent,
    stageIIIncidenceRecursiveDepthCellOrientation_eq_parent]
  exact stageIIIncidenceSeedFaceOrientation_mates_flip f

/-- Integer representative on a finite-depth central recursive cell.

As in v4.23, the scalar is pulled back from the retained parent, while
orientation is recomputed from the recursive inner face kind. -/
def counterTransportRecursiveDepthCellIntRepresentative
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (c : StageIIIncidenceRecursiveDepthCell) : ℤ :=
  stageIIIncidenceOrientationIntCoeff
      (stageIIIncidenceRecursiveDepthCellOrientation c) *
    counterTransportIncidenceSeedFaceIntRepresentative T c.parent

/-- At every finite depth the integer representative is exactly the v4.22
oriented representative on the original parent. -/
@[simp] theorem counterTransportRecursiveDepthCellIntRepresentative_eq_parent
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat)
    (g : OctahedralStageIIIncidenceSeedFace) :
    counterTransportRecursiveDepthCellIntRepresentative T
        (stageIIIncidenceRecursiveDepthCell depth g) =
      counterTransportOrientedIncidenceSeedFaceIntRepresentative T
        (stageIIIncidenceSeedFaceOrientation g) g := by
  simp [counterTransportRecursiveDepthCellIntRepresentative,
    counterTransportOrientedIncidenceSeedFaceIntRepresentative]

/-- Successive recursive depths carry the same integer representative. -/
theorem counterTransportRecursiveDepthCellIntRepresentative_succ_eq
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat)
    (g : OctahedralStageIIIncidenceSeedFace) :
    counterTransportRecursiveDepthCellIntRepresentative T
        (stageIIIncidenceRecursiveDepthCell (Nat.succ depth) g) =
      counterTransportRecursiveDepthCellIntRepresentative T
        (stageIIIncidenceRecursiveDepthCell depth g) := by
  rw [counterTransportRecursiveDepthCellIntRepresentative_eq_parent,
    counterTransportRecursiveDepthCellIntRepresentative_eq_parent]

/-- The depth-one construction agrees at the scalar level with the v4.23
one-step recursive child. -/
theorem counterTransportRecursiveDepthCellIntRepresentative_one_eq_v4_23
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (g : OctahedralStageIIIncidenceSeedFace) :
    counterTransportRecursiveDepthCellIntRepresentative T
        (stageIIIncidenceRecursiveDepthCell 1 g) =
      counterTransportRecursiveChildIntRepresentative T
        (stageIIIncidenceRecursiveChild g) := by
  rw [counterTransportRecursiveDepthCellIntRepresentative_eq_parent,
    counterTransportRecursiveChildIntRepresentative_eq_parent]

/-- Every finite-depth central-cell representative reduces modulo two to the
same validated pushed Stage-II scalar on its original parent. -/
@[simp] theorem counterTransportRecursiveDepthCellIntRepresentative_modTwo
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat)
    (g : OctahedralStageIIIncidenceSeedFace) :
    ((counterTransportRecursiveDepthCellIntRepresentative T
        (stageIIIncidenceRecursiveDepthCell depth g) : ℤ) : ZMod 2) =
      counterTransportIncidenceSeedFaceAdd T g := by
  rw [counterTransportRecursiveDepthCellIntRepresentative_eq_parent]
  exact
    counterTransportOrientedIncidenceSeedFaceIntRepresentative_modTwo
      T (stageIIIncidenceSeedFaceOrientation g) g

/-- Eight-term integer total at an arbitrary finite recursive depth. -/
def counterTransportFiniteDepthRecursiveCarrierIntTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) : ℤ :=
  counterTransportRecursiveDepthCellIntRepresentative T
      (octahedralStageIIFiniteDepthChildPlacement depth .a00b00) +
    counterTransportRecursiveDepthCellIntRepresentative T
      (octahedralStageIIFiniteDepthChildPlacement depth .a01b10) +
    counterTransportRecursiveDepthCellIntRepresentative T
      (octahedralStageIIFiniteDepthChildPlacement depth .a00b01) +
    counterTransportRecursiveDepthCellIntRepresentative T
      (octahedralStageIIFiniteDepthChildPlacement depth .a01b11) +
    counterTransportRecursiveDepthCellIntRepresentative T
      (octahedralStageIIFiniteDepthChildPlacement depth .a10b00) +
    counterTransportRecursiveDepthCellIntRepresentative T
      (octahedralStageIIFiniteDepthChildPlacement depth .a11b10) +
    counterTransportRecursiveDepthCellIntRepresentative T
      (octahedralStageIIFiniteDepthChildPlacement depth .a10b01) +
    counterTransportRecursiveDepthCellIntRepresentative T
      (octahedralStageIIFiniteDepthChildPlacement depth .a11b11)

/-- At every finite depth, the complete integer-oriented total is exactly the
v4.22 parent total. -/
theorem counterTransportFiniteDepthRecursiveCarrierIntTotal_eq_parent
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    counterTransportFiniteDepthRecursiveCarrierIntTotal T depth =
      counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal T := by
  simp [counterTransportFiniteDepthRecursiveCarrierIntTotal,
    octahedralStageIIFiniteDepthChildPlacement,
    counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal]

/-- The total is invariant under one more recursive depth. -/
theorem counterTransportFiniteDepthRecursiveCarrierIntTotal_succ_eq
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    counterTransportFiniteDepthRecursiveCarrierIntTotal T (Nat.succ depth) =
      counterTransportFiniteDepthRecursiveCarrierIntTotal T depth := by
  rw [counterTransportFiniteDepthRecursiveCarrierIntTotal_eq_parent,
    counterTransportFiniteDepthRecursiveCarrierIntTotal_eq_parent]

/-- Depth one recovers the v4.23 one-step total. -/
theorem counterTransportFiniteDepthRecursiveCarrierIntTotal_one_eq_v4_23
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterTransportFiniteDepthRecursiveCarrierIntTotal T 1 =
      counterTransportOneStepRecursiveCarrierIntTotal T := by
  rw [counterTransportFiniteDepthRecursiveCarrierIntTotal_eq_parent,
    counterTransportOneStepRecursiveCarrierIntTotal_eq_parent]

/-- Integer Stage-II mismatch at arbitrary finite recursive depth. -/
def counterStageIIFiniteDepthRecursiveCarrierIntMismatch
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) : ℤ :=
  1 + counterTransportFiniteDepthRecursiveCarrierIntTotal T depth

/-- Every finite-depth mismatch is exactly the v4.22 parent mismatch. -/
theorem counterStageIIFiniteDepthRecursiveCarrierIntMismatch_eq_parent
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch T depth =
      counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch T := by
  change 1 + counterTransportFiniteDepthRecursiveCarrierIntTotal T depth =
    1 + counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal T
  rw [counterTransportFiniteDepthRecursiveCarrierIntTotal_eq_parent]

/-- Successive recursive depths have identical integer mismatch. -/
theorem counterStageIIFiniteDepthRecursiveCarrierIntMismatch_succ_eq
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch T
        (Nat.succ depth) =
      counterStageIIFiniteDepthRecursiveCarrierIntMismatch T depth := by
  rw [counterStageIIFiniteDepthRecursiveCarrierIntMismatch_eq_parent,
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch_eq_parent]

/-- Explicit finite-depth induction: every natural-number depth has the same
integer mismatch as depth zero. -/
theorem counterStageIIFiniteDepthRecursiveCarrierIntMismatch_eq_zeroDepth
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch T depth =
      counterStageIIFiniteDepthRecursiveCarrierIntMismatch T 0 := by
  induction depth with
  | zero =>
      rfl
  | succ depth ih =>
      rw [counterStageIIFiniteDepthRecursiveCarrierIntMismatch_succ_eq]
      exact ih

/-- Depth one agrees exactly with the already-validated v4.23 one-step
mismatch. -/
theorem counterStageIIFiniteDepthRecursiveCarrierIntMismatch_one_eq_v4_23
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch T 1 =
      counterStageIIOneStepRecursiveCarrierIntMismatch T := by
  rw [counterStageIIFiniteDepthRecursiveCarrierIntMismatch_eq_parent,
    counterStageIIOneStepRecursiveCarrierIntMismatch_eq_parent]

/-- At every finite depth, mod-two reduction is exactly the certified v4.12
Stage-II obstruction. -/
theorem counterStageIIFiniteDepthRecursiveCarrierIntMismatch_modTwo_eq_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    ((counterStageIIFiniteDepthRecursiveCarrierIntMismatch T depth : ℤ) :
        ZMod 2) =
      counterStageIIObstructionAdd T := by
  rw [counterStageIIFiniteDepthRecursiveCarrierIntMismatch_eq_parent]
  exact
    counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch_modTwo_eq_obstruction
      T

/-- Since the Stage-II obstruction equals one, every finite-depth mismatch has
mod-two value one. -/
theorem counterStageIIFiniteDepthRecursiveCarrierIntMismatch_modTwo_eq_one
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    ((counterStageIIFiniteDepthRecursiveCarrierIntMismatch T depth : ℤ) :
        ZMod 2) = 1 := by
  rw [counterStageIIFiniteDepthRecursiveCarrierIntMismatch_modTwo_eq_obstruction,
    counterStageIIObstructionAdd_eq_one]

/-- Therefore the integer mismatch is nonzero at every finite recursive
depth. -/
theorem counterStageIIFiniteDepthRecursiveCarrierIntMismatch_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch T depth ≠ 0 := by
  rw [counterStageIIFiniteDepthRecursiveCarrierIntMismatch_eq_parent]
  exact
    counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch_ne_zero T

/-- Although the chosen integer representative can depend on the coherent
transport, its certified mod-two obstruction class remains transport-independent
at every finite depth. -/
theorem counterStageIIFiniteDepthRecursiveCarrierIntMismatch_modTwo_transport_independent
    (T U : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (depth : Nat) :
    ((counterStageIIFiniteDepthRecursiveCarrierIntMismatch T depth : ℤ) :
        ZMod 2) =
      ((counterStageIIFiniteDepthRecursiveCarrierIntMismatch U depth : ℤ) :
        ZMod 2) := by
  rw [counterStageIIFiniteDepthRecursiveCarrierIntMismatch_modTwo_eq_obstruction,
    counterStageIIFiniteDepthRecursiveCarrierIntMismatch_modTwo_eq_obstruction]
  exact counterStageIIObstructionAdd_transport_independent T U

/-!
## Boundary after v4.24

The central-cell pullback semantics now extends from one refinement step to
every finite natural-number depth.

For every depth n:

* all eight source labels remain globally distinct because their original
  parent faces are retained;
* the recursive inner pentagon/hexagon kind and arity equal the parent kind and
  arity by v3.90;
* middle-switch mates remain opposite-kind and opposite-orientation;
* every integer representative equals its v4.22 parent representative;
* the complete integer total and mismatch are invariant under n -> n + 1;
* explicit induction identifies every finite-depth mismatch with depth zero;
* reduction modulo two is always omega(T) = 1, hence nonzero and
  transport-independent.

This establishes finite-depth recursive survival of the Stage-II obstruction
for the authority-bounded central-cell pullback rule.

It still does not imply an infinite recursive limit or a metric fractal.
Neither does it prove preservation under arbitrary redistribution of scalar
data among local pentagram/hexagram crossings.  Those require additional
topological, analytic, or descent data beyond the present finite incidence
formalization.
-/

end

end KUOS.DependentOriginationStageIIFiniteDepthRecursiveTransportV4_24
