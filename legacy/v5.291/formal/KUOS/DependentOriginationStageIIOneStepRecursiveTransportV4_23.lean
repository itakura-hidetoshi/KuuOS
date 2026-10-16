import KUOS.DependentOriginationStageIIIntegralOrientationLiftV4_22
import KUOS.DependentOriginationTruncatedIcosahedralRecursiveRefinementV3_90
import Mathlib

namespace KUOS.DependentOriginationStageIIOneStepRecursiveTransportV4_23

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
open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationHexagramInnerHexagonV3_88
open KUOS.DependentOriginationPentagramInnerPentagonV3_89
open KUOS.DependentOriginationTruncatedIcosahedralRecursiveRefinementV3_90

set_option autoImplicit false

noncomputable section

/-!
# One-step recursive transport of the Stage-II carrier v4.23

v4.18 proves that all eight Stage-II labels cannot be injected into one local
pentagram or hexagram crossing set.  The v4.19--v4.22 carrier is instead
global: eight distinct source labels occupy eight distinct seed faces.

v3.90 already provides the authority-bearing recursive combinatorics for each
individual face:

* pentagon -> pentagram -> inner pentagon;
* hexagon  -> hexagram  -> inner hexagon.

One refinement step preserves both face kind and boundary arity.

This file combines those two facts without compressing the eight labels into a
single star.  Each placed seed face is refined independently to its own central
inner cell.  The resulting child carrier retains its parent face explicitly,
so the eight-way global support remains injective.

For the scalar layer we use the minimal parent-projection pullback: the integer
representative on a refined central cell is obtained from the already-certified
v4.22 representative on its parent face, with orientation recomputed from the
inner face kind.  Since v3.90 proves that the inner face kind equals the parent
kind, this one-step pullback is exactly the original v4.22 representative.

Consequently the eight-term integer total, its mod-two reduction, and the
nonzero Stage-II mismatch all survive one recursive refinement step.

This is a theorem about central-cell pullback transport.  It does not claim
that arbitrary redistributions onto the five or six crossing vertices preserve
the obstruction.
-/

/-- One recursively refined central cell attached to an incidence-selected
seed face.  The parent is retained so different global faces are never
identified merely because their inner cells have the same polygonal kind. -/
structure StageIIIncidenceRecursiveChild where
  parent : OctahedralStageIIIncidenceSeedFace
  innerKind : TruncatedIcosahedralFaceKind
  innerBoundaryLength : Nat
  innerKind_eq :
    innerKind =
      truncatedIcosahedralRecursiveInnerFaceKind
        (truncatedIcosahedralSeedFaceKind parent.1)
  innerBoundaryLength_eq :
    innerBoundaryLength =
      truncatedIcosahedralRecursiveInnerBoundaryLength
        (truncatedIcosahedralSeedFaceKind parent.1)

/-- The canonical central child supplied by the v3.90 recursive-star operator. -/
def stageIIIncidenceRecursiveChild
    (g : OctahedralStageIIIncidenceSeedFace) :
    StageIIIncidenceRecursiveChild where
  parent := g
  innerKind :=
    truncatedIcosahedralRecursiveInnerFaceKind
      (truncatedIcosahedralSeedFaceKind g.1)
  innerBoundaryLength :=
    truncatedIcosahedralRecursiveInnerBoundaryLength
      (truncatedIcosahedralSeedFaceKind g.1)
  innerKind_eq := rfl
  innerBoundaryLength_eq := rfl

@[simp] theorem stageIIIncidenceRecursiveChild_parent
    (g : OctahedralStageIIIncidenceSeedFace) :
    (stageIIIncidenceRecursiveChild g).parent = g := by
  rfl

@[simp] theorem stageIIIncidenceRecursiveChild_innerKind
    (g : OctahedralStageIIIncidenceSeedFace) :
    (stageIIIncidenceRecursiveChild g).innerKind =
      truncatedIcosahedralSeedFaceKind g.1 := by
  exact
    truncatedIcosahedralRecursiveInnerFaceKind_eq
      (truncatedIcosahedralSeedFaceKind g.1)

@[simp] theorem stageIIIncidenceRecursiveChild_innerBoundaryLength
    (g : OctahedralStageIIIncidenceSeedFace) :
    (stageIIIncidenceRecursiveChild g).innerBoundaryLength =
      truncatedIcosahedralFaceSides
        (truncatedIcosahedralSeedFaceKind g.1) := by
  exact
    truncatedIcosahedralRecursiveInnerBoundaryLength_eq
      (truncatedIcosahedralSeedFaceKind g.1)

/-- Distinct parent faces remain distinct after one recursive central-cell
refinement step. -/
theorem stageIIIncidenceRecursiveChild_injective :
    Function.Injective stageIIIncidenceRecursiveChild := by
  intro g h hEq
  exact congrArg (fun c : StageIIIncidenceRecursiveChild => c.parent) hEq

/-- Refine each of the eight v4.19/v4.20 placed faces independently. -/
def octahedralStageIIRecursiveChildPlacement
    (f : OctahedralStageIIParityFace) :
    StageIIIncidenceRecursiveChild :=
  stageIIIncidenceRecursiveChild
    (octahedralStageIIIncidenceSeedEquiv f)

/-- The global eight-label support remains injective after refinement. -/
theorem octahedralStageIIRecursiveChildPlacement_injective :
    Function.Injective octahedralStageIIRecursiveChildPlacement := by
  intro f g hEq
  apply octahedralStageIIIncidenceSeedEquiv.injective
  exact congrArg
    (fun c : StageIIIncidenceRecursiveChild => c.parent) hEq

/-- Middle-switch mates still have opposite inner face kinds after refinement. -/
theorem octahedralStageIIRecursiveChildPlacement_mates_opposite_innerKinds
    (f : OctahedralStageIIParityFace) :
    (octahedralStageIIRecursiveChildPlacement f).innerKind ≠
      (octahedralStageIIRecursiveChildPlacement
        (octahedralStageIIMiddleSwitchMate f)).innerKind := by
  simpa [octahedralStageIIRecursiveChildPlacement] using
    octahedralStageIIIncidenceSeedEquiv_mates_opposite_kinds f

/-- Orientation of a refined central child is determined by its inner face
kind, not by a sign multiplication in `ZMod 2`. -/
def stageIIIncidenceRecursiveChildOrientation
    (c : StageIIIncidenceRecursiveChild) :
    StageIIIncidenceOrientation :=
  stageIIIncidenceFaceKindOrientation c.innerKind

/-- For the canonical child, recursive orientation equals the parent
seed-face orientation because v3.90 preserves face kind. -/
@[simp] theorem stageIIIncidenceRecursiveChildOrientation_eq_parent
    (g : OctahedralStageIIIncidenceSeedFace) :
    stageIIIncidenceRecursiveChildOrientation
        (stageIIIncidenceRecursiveChild g) =
      stageIIIncidenceSeedFaceOrientation g := by
  simp [stageIIIncidenceRecursiveChildOrientation,
    stageIIIncidenceSeedFaceOrientation]

/-- Hence refined middle-switch mates still have flipped orientations. -/
theorem octahedralStageIIRecursiveChildPlacement_mates_orientation_flip
    (f : OctahedralStageIIParityFace) :
    stageIIIncidenceRecursiveChildOrientation
        (octahedralStageIIRecursiveChildPlacement
          (octahedralStageIIMiddleSwitchMate f)) =
      stageIIIncidenceOrientationFlip
        (stageIIIncidenceRecursiveChildOrientation
          (octahedralStageIIRecursiveChildPlacement f)) := by
  rw [octahedralStageIIRecursiveChildPlacement,
    octahedralStageIIRecursiveChildPlacement,
    stageIIIncidenceRecursiveChildOrientation_eq_parent,
    stageIIIncidenceRecursiveChildOrientation_eq_parent]
  exact stageIIIncidenceSeedFaceOrientation_mates_flip f

/-- Integer representative on one refined central child.

The scalar is pulled back along the retained parent projection; orientation is
recomputed from the actual recursive inner face kind. -/
def counterTransportRecursiveChildIntRepresentative
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (c : StageIIIncidenceRecursiveChild) : ℤ :=
  stageIIIncidenceOrientationIntCoeff
      (stageIIIncidenceRecursiveChildOrientation c) *
    counterTransportIncidenceSeedFaceIntRepresentative T c.parent

/-- On a canonical recursive child, the pullback representative is exactly the
v4.22 oriented integer representative on the parent. -/
@[simp] theorem counterTransportRecursiveChildIntRepresentative_eq_parent
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (g : OctahedralStageIIIncidenceSeedFace) :
    counterTransportRecursiveChildIntRepresentative T
        (stageIIIncidenceRecursiveChild g) =
      counterTransportOrientedIncidenceSeedFaceIntRepresentative T
        (stageIIIncidenceSeedFaceOrientation g) g := by
  simp [counterTransportRecursiveChildIntRepresentative,
    counterTransportOrientedIncidenceSeedFaceIntRepresentative]

/-- Therefore every canonical refined child reduces modulo two to the same
validated pushed Stage-II scalar on its parent face. -/
@[simp] theorem counterTransportRecursiveChildIntRepresentative_modTwo
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (g : OctahedralStageIIIncidenceSeedFace) :
    ((counterTransportRecursiveChildIntRepresentative T
        (stageIIIncidenceRecursiveChild g) : ℤ) : ZMod 2) =
      counterTransportIncidenceSeedFaceAdd T g := by
  rw [counterTransportRecursiveChildIntRepresentative_eq_parent]
  exact
    counterTransportOrientedIncidenceSeedFaceIntRepresentative_modTwo
      T (stageIIIncidenceSeedFaceOrientation g) g

/-- Eight-term integer total after one independent recursive refinement of each
placed seed face. -/
def counterTransportOneStepRecursiveCarrierIntTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ℤ :=
  counterTransportRecursiveChildIntRepresentative T
      (octahedralStageIIRecursiveChildPlacement .a00b00) +
    counterTransportRecursiveChildIntRepresentative T
      (octahedralStageIIRecursiveChildPlacement .a01b10) +
    counterTransportRecursiveChildIntRepresentative T
      (octahedralStageIIRecursiveChildPlacement .a00b01) +
    counterTransportRecursiveChildIntRepresentative T
      (octahedralStageIIRecursiveChildPlacement .a01b11) +
    counterTransportRecursiveChildIntRepresentative T
      (octahedralStageIIRecursiveChildPlacement .a10b00) +
    counterTransportRecursiveChildIntRepresentative T
      (octahedralStageIIRecursiveChildPlacement .a11b10) +
    counterTransportRecursiveChildIntRepresentative T
      (octahedralStageIIRecursiveChildPlacement .a10b01) +
    counterTransportRecursiveChildIntRepresentative T
      (octahedralStageIIRecursiveChildPlacement .a11b11)

/-- One-step central-cell refinement preserves the full integer-oriented carrier
total exactly. -/
theorem counterTransportOneStepRecursiveCarrierIntTotal_eq_parent
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterTransportOneStepRecursiveCarrierIntTotal T =
      counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal T := by
  simp [counterTransportOneStepRecursiveCarrierIntTotal,
    octahedralStageIIRecursiveChildPlacement,
    counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal]

/-- Stage-II mismatch after one recursive central-cell refinement step. -/
def counterStageIIOneStepRecursiveCarrierIntMismatch
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ℤ :=
  1 + counterTransportOneStepRecursiveCarrierIntTotal T

/-- The one-step recursive integer mismatch is exactly the v4.22 parent
mismatch. -/
theorem counterStageIIOneStepRecursiveCarrierIntMismatch_eq_parent
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIOneStepRecursiveCarrierIntMismatch T =
      counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch T := by
  rw [counterStageIIOneStepRecursiveCarrierIntMismatch,
    counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch,
    counterTransportOneStepRecursiveCarrierIntTotal_eq_parent]

/-- Reducing after one recursive refinement still gives the certified v4.12
Stage-II obstruction class. -/
theorem counterStageIIOneStepRecursiveCarrierIntMismatch_modTwo_eq_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    ((counterStageIIOneStepRecursiveCarrierIntMismatch T : ℤ) : ZMod 2) =
      counterStageIIObstructionAdd T := by
  rw [counterStageIIOneStepRecursiveCarrierIntMismatch_eq_parent]
  exact
    counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch_modTwo_eq_obstruction
      T

/-- In particular, the one-step recursively transported integral mismatch
cannot vanish. -/
theorem counterStageIIOneStepRecursiveCarrierIntMismatch_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIOneStepRecursiveCarrierIntMismatch T ≠ 0 := by
  rw [counterStageIIOneStepRecursiveCarrierIntMismatch_eq_parent]
  exact
    counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch_ne_zero T

/-!
## Boundary after v4.23

A genuine one-step recursive carrier theorem is now available.

Carrier layer:
* every one of the eight globally placed Stage-II labels refines independently;
* the child retains its parent, so the eight-way placement remains injective;
* v3.90 forces each inner central face to have the same kind and arity as its
  parent;
* middle-switch mate pairs therefore remain opposite-kind and opposite-
  orientation after refinement.

Scalar layer:
* the refined central-cell representative is the parent representative pulled
  back along the child-to-parent projection;
* because inner face kind is preserved, its integer orientation coefficient is
  unchanged;
* the full integer total is therefore identical before and after one step;
* modulo two, the refined mismatch is still the nonzero v4.12 Stage-II class.

This closes one-step preservation for the central-cell pullback semantics.

It does not prove preservation for arbitrary redistribution onto the five
pentagram or six hexagram crossing vertices.  Such a rule would require
additional coherence/descent data.

The next legitimate unit is finite-depth induction for this same central-cell
pullback transport.  Because v3.90 already proves face-kind stability at every
finite depth, no metric or infinite-limit claim is needed.
-/

end

end KUOS.DependentOriginationStageIIOneStepRecursiveTransportV4_23
