import KuuOSFormal.HistoricalF36F40BridgeP36
import Mathlib.Tactic.Abel

/-!
# F112-P37 — historically anchored four-boundary additive gauge transport

This is an OLD-SIDE validation module only. It does not enter the
independent Kuu.F112 / KuuOSStrict import closure. Its source is the
ACTUAL historical original F47 C60F47SquareFrame, including the old
F42 physical-face 3-Hom and old original F54/F55 rotation 3-Hom.
P36 already transported its real C60 edge into TWO distinct native
five/six-sector F42 face atlases, and proved the old/new chosen
comparison shadows require a nonzero correction.

P37 proves a stronger and more structurally useful statement:
for ANY genuinely calibrated native four-boundary F42/F55 frame N,
the historical and native complete (Int×Int)×ZMod2 four-arrow
evaluations admit an EXPLICIT object-boundary gauge. The gauge
simultaneously matches the physical-face generator, rotation
generator, before comparison and after comparison — all FOUR.
The latter compatibility is DERIVED using BOTH actual independently
proved original/new mixed-square calibration equations; it is
not postulated as a new coherence axiom.

We also prove that the fourth compatibility is FORCED by the first
three and both calibrated squares. This isolates the exact
square-descent/naturality obligation before any unproved old-to-new
higher-source functor or Beck-Chevalley equivalence is asserted.

The old and new PHYSICAL SOURCE TWO-CELLS are still different types.
This is a shadow-level gauge / boundary-transport theorem, not a
historical F47 ≌ independent source equivalence or F68/F77 nonlift.
No change to the old math corpus or public roots, no new axioms/sorry.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156

set_option autoImplicit false
set_option warningAsError true
noncomputable section

universe uP37 vP37 uDP37 vDP37
variable {C : Type uP37} [Category.{vP37} C]
variable {D : Type uDP37} [Category.{vDP37} D]
variable {a b : C} {x y : D} {n n' m m' : Nat}
variable {ma mb : OldBlocks a b} {pa pb : OldBlocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- The historical actual F47 FACE arrow's complete native shadow,
without pretending its old F42 source 2-cell is an independent native
F54/F55 source 2-cell. -/
def historicalF47FaceCoordinates
    (B : C60F47SquareFrame α β r s) : KuuNativeF55Shadow :=
  (((c60F47MixedGrayFunctor B).map (c60F47FaceArrow B)).charge,
    ((c60F47MixedGrayFunctor B).map (c60F47FaceArrow B)).phase)

/-- The historical original F55 ROTATION arrow has its own
independently typed old F54 route endpoints. -/
def historicalF47RotationCoordinates
    (B : C60F47SquareFrame α β r s) : KuuNativeF55Shadow :=
  (((c60F47MixedGrayFunctor B).map
      (c60F47OriginalF55Arrow B)).charge,
    ((c60F47MixedGrayFunctor B).map
      (c60F47OriginalF55Arrow B)).phase)

/-- The true old calibrated mixed square transfers componentwise
to the complete native comparison CARRIER, although no map between
the original and new source 3-Hom categories has yet been claimed. -/
theorem historicalF47Coordinates_calibrated
    (B : C60F47SquareFrame α β r s) :
    historicalF47FaceCoordinates B +
      historicalF47AfterCoordinates B =
        historicalF47RotationCoordinates B := by
  apply Prod.ext
  · have hc := congrArg GradedThreeCell.charge B.calibrated
    change
      (historicalF47FaceCoordinates B).1 +
        (historicalF47AfterCoordinates B).1 =
          (historicalF47RotationCoordinates B).1 at hc
    exact hc
  · have hp := congrArg GradedThreeCell.phase B.calibrated
    change
      (historicalF47FaceCoordinates B).2 +
        (historicalF47AfterCoordinates B).2 =
          (historicalF47RotationCoordinates B).2 at hp
    exact hp

/-- The old after-arrow is the uniquely required old rotation
value MINUS the original face value, not an unproved new F55 lift. -/
theorem historicalF47After_eq_rotation_sub_face
    (B : C60F47SquareFrame α β r s) :
    historicalF47AfterCoordinates B =
      historicalF47RotationCoordinates B -
        historicalF47FaceCoordinates B := by
  apply add_left_cancel (a := historicalF47FaceCoordinates B)
  calc
    historicalF47FaceCoordinates B +
        historicalF47AfterCoordinates B =
          historicalF47RotationCoordinates B :=
      historicalF47Coordinates_calibrated B
    _ = historicalF47FaceCoordinates B +
          (historicalF47RotationCoordinates B -
            historicalF47FaceCoordinates B) := by abel

/-- The same precise equation for any separately calibrated
independent native physical-face/F55 rotation mixed frame. -/
theorem nativeCalibratedAfter_eq_sub
    (N : NativeC60PhysicalMixedCalibration)
    (hN : N.Calibrated) :
    N.compareAfter = N.compareBefore +
      N.rotationValue - N.faceValue := by
  apply add_left_cancel (a := N.faceValue)
  calc
    N.faceValue + N.compareAfter =
        N.compareBefore + N.rotationValue := hN
    _ = N.faceValue +
        (N.compareBefore + N.rotationValue - N.faceValue) := by abel

/-- A four-object complete-shadow GAUGE, with separate correction
at every genuinely tagged physical/rotation BEFORE and AFTER point.
The laws are a componentwise additive naturality square, but do not
equate original F42 source types with new native F54 route types. -/
structure HistoricalF47FourBoundaryGauge
    (B : C60F47SquareFrame α β r s)
    (N : NativeC60PhysicalMixedCalibration) where
  faceBefore : KuuNativeF55Shadow
  faceAfter : KuuNativeF55Shadow
  rotationBefore : KuuNativeF55Shadow
  rotationAfter : KuuNativeF55Shadow
  face_law :
    historicalF47FaceCoordinates B + faceAfter =
      faceBefore + N.faceValue
  rotation_law :
    historicalF47RotationCoordinates B + rotationAfter =
      rotationBefore + N.rotationValue
  before_law :
    (0 : KuuNativeF55Shadow) + rotationBefore =
      faceBefore + N.compareBefore
  after_law :
    historicalF47AfterCoordinates B + rotationAfter =
      faceAfter + N.compareAfter

/-- The complete normalized four-boundary gauge is CONSTRUCTED for
every old ACTUAL F47 frame and every independently calibrated
native comparison frame. It uses face/rotation endpoint data, not
an arbitrary assertion that the old and new after-arrows agree. -/
def historicalF47FourBoundaryGauge
    (B : C60F47SquareFrame α β r s)
    (N : NativeC60PhysicalMixedCalibration)
    (hN : N.Calibrated) :
    HistoricalF47FourBoundaryGauge B N where
  faceBefore := 0
  faceAfter := N.faceValue - historicalF47FaceCoordinates B
  rotationBefore := N.compareBefore
  rotationAfter := N.compareBefore + N.rotationValue -
    historicalF47RotationCoordinates B
  face_law := by
    change historicalF47FaceCoordinates B +
      (N.faceValue - historicalF47FaceCoordinates B) =
        (0 : KuuNativeF55Shadow) + N.faceValue
    abel
  rotation_law := by
    change historicalF47RotationCoordinates B +
      (N.compareBefore + N.rotationValue -
        historicalF47RotationCoordinates B) =
      N.compareBefore + N.rotationValue
    abel
  before_law := by
    change (0 : KuuNativeF55Shadow) + N.compareBefore =
      (0 : KuuNativeF55Shadow) + N.compareBefore
    rfl
  after_law := by
    change historicalF47AfterCoordinates B +
      (N.compareBefore + N.rotationValue -
        historicalF47RotationCoordinates B) =
        (N.faceValue - historicalF47FaceCoordinates B) +
          N.compareAfter
    rw [historicalF47After_eq_rotation_sub_face B,
      nativeCalibratedAfter_eq_sub N hN]
    abel

/-- The fourth face-to-rotation comparison equality is NOT an
independent choice: both calibrated squares AND the first THREE
boundary generator compatibilities FORCE it. This is the precise
additive coherence condition for all four distinct boundary tags. -/
theorem historicalF47FourthBoundary_forced
    (B : C60F47SquareFrame α β r s)
    (N : NativeC60PhysicalMixedCalibration)
    (hN : N.Calibrated)
    (fBefore fAfter rBefore rAfter : KuuNativeF55Shadow)
    (hFace : historicalF47FaceCoordinates B + fAfter =
      fBefore + N.faceValue)
    (hRotation : historicalF47RotationCoordinates B + rAfter =
      rBefore + N.rotationValue)
    (hBefore : (0 : KuuNativeF55Shadow) + rBefore =
      fBefore + N.compareBefore) :
    historicalF47AfterCoordinates B + rAfter =
      fAfter + N.compareAfter := by
  have hf : fAfter =
      fBefore + N.faceValue - historicalF47FaceCoordinates B := by
    apply add_left_cancel (a := historicalF47FaceCoordinates B)
    calc
      historicalF47FaceCoordinates B + fAfter =
          fBefore + N.faceValue := hFace
      _ = historicalF47FaceCoordinates B +
        (fBefore + N.faceValue - historicalF47FaceCoordinates B) := by abel
  have hr : rAfter =
      rBefore + N.rotationValue -
        historicalF47RotationCoordinates B := by
    apply add_left_cancel (a := historicalF47RotationCoordinates B)
    calc
      historicalF47RotationCoordinates B + rAfter =
          rBefore + N.rotationValue := hRotation
      _ = historicalF47RotationCoordinates B +
        (rBefore + N.rotationValue -
          historicalF47RotationCoordinates B) := by abel
  have hb : rBefore = fBefore + N.compareBefore := by
    simpa only [zero_add] using hBefore
  rw [historicalF47After_eq_rotation_sub_face B,
    nativeCalibratedAfter_eq_sub N hN, hf, hr, hb]
  abel

/-- This gauge does not depend on any arbitrary historical/new
C60 geometry identification: it is a required SHADOW-level
normalization on four independently preserved source positions. -/
theorem historicalF47FourBoundaryGauge_exists
    (B : C60F47SquareFrame α β r s)
    (N : NativeC60PhysicalMixedCalibration)
    (hN : N.Calibrated) :
    Nonempty (HistoricalF47FourBoundaryGauge B N) :=
  ⟨historicalF47FourBoundaryGauge B N hN⟩

/-- The verified north C60 mixed physical face/rotation frame is
one actual native recipient to which every old actual calibrated
F47 frame has this explicit four-boundary coordinate gauge. The
underlying original F42/F55 3-Hom SOURCE correspondence is STILL
an independent, unproved obligation. -/
theorem historicalF47FourBoundaryNorth_exists
    (B : C60F47SquareFrame α β r s) :
    Nonempty (HistoricalF47FourBoundaryGauge B
      northHexagonPhysicalMixedCalibrated) :=
  ⟨historicalF47FourBoundaryGauge B
    northHexagonPhysicalMixedCalibrated
    northHexagonPhysicalMixedCalibrated_valid⟩

#print axioms historicalF47Coordinates_calibrated
#print axioms historicalF47After_eq_rotation_sub_face
#print axioms nativeCalibratedAfter_eq_sub
#print axioms HistoricalF47FourBoundaryGauge
#print axioms historicalF47FourBoundaryGauge
#print axioms historicalF47FourthBoundary_forced
#print axioms historicalF47FourBoundaryGauge_exists
#print axioms historicalF47FourBoundaryNorth_exists

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
