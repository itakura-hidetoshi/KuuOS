import KUOS.DependentOriginationGrayC60OriginalF43RightHorizontalV5_203
import KUOS.DependentOriginationGrayC60MixedComparisonObstructionV5_196

namespace KUOS.DependentOriginationGrayC60OriginalF43F55MixedBridgeV5_203

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorThreeHomV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorNaturalityV5_200
open KUOS.DependentOriginationGrayC60OriginalF43RightHorizontalV5_203
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60MixedComparisonObstructionV5_196
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.203 / F59-F54-B: source-preserving F43/F52 to ORIGINAL F54/F55 mixed bridge

Connect the *newly proved F52 source-typed natural F43 interchanger*
to the PREEXISTING actual C60 90-edge, both-incident-face F47 mixed
four-boundary category. Do not identify F42 face 2-cell witnesses with
the independently typed F54 rotation routes. At each of all 180 sites:
  - the F52 arrow is exactly the genuinely original F43 generator;
  - its FULL native image matches the old actual F47 FACE side;
  - unique calibration Δ=(0,1;0) recovers the ORIGINAL F55 arrow;
  - the four-boundary source categorical comparison square commutes.
The phase 1 exchange remains nonidentity, the calibration remains
outside the original nine-generator F55 phase-locked image, and the
true signed north pentagon has nonzero original F55 curvature.

These are local source-compatible cospans and verified calibrations,
NOT a newly invented original F55 Δ-arrow, source-term identity, or
unconditional descent/global fully faithful Gray 3-category.
-/

/-- The truly ORIGINAL proof-relevant physical polygon face at a
genuine physical edge and one of its TWO incident C60 faces. -/
def c60F54AdjacentF52OriginalFace
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    C60F52OriginalTwo
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace edge side)).2 Quiver.Path.nil :=
  ⟨c60F48AdjacentFaceTwoCell edge side⟩

/-- An F52 arrow whose proof term is EXACTLY the old ORIGINAL F43
face interchange, at all physical edge/face choices. This is not
a new F55 square, nor an untyped identification of sources. -/
def c60F54AdjacentF52OriginalInterchanger
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F52OriginalTwoHorizontal
      (c60F54AdjacentF52OriginalFace edge side)
      (c60F54AdjacentF52OriginalFace edge side) ⟶
    c60F52OriginalTwoHorizontalRight
      (c60F54AdjacentF52OriginalFace edge side)
      (c60F54AdjacentF52OriginalFace edge side) :=
  c60F52OriginalInterchanger
    (c60F54AdjacentF52OriginalFace edge side)
    (c60F54AdjacentF52OriginalFace edge side)

theorem c60F54AdjacentF52Interchanger_isOriginalF43
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F54AdjacentF52OriginalInterchanger edge side =
      c60F52Of (.ofF51 (.original
        (c60F48AdjacentFaceInterchanger edge side))) := rfl

/-- Complete native F59 image: both independent integer charges
and the odd original Gray exchange phase are retained. -/
theorem c60F54AdjacentF52Interchanger_native
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F52Eval (c60F54AdjacentF52OriginalInterchanger edge side) =
      (c60F48AdjacentFaceInterchanger edge side).toNative := rfl

theorem c60F54AdjacentF52Interchanger_phaseOne
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (c60F52Eval
      (c60F54AdjacentF52OriginalInterchanger edge side)).phase =
        (1 : ZMod 2) := by
  rw [c60F54AdjacentF52Interchanger_native,
    c60F48AdjacentFaceInterchanger_native]
  exact c60F43NorthPentagonInterchange_components.2

theorem c60F54AdjacentF52Interchanger_nontrivial
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F52Eval (c60F54AdjacentF52OriginalInterchanger edge side) ≠
      (0 : GradedThreeCell 0 0) := by
  intro h
  have hp := congrArg GradedThreeCell.phase h
  rw [c60F54AdjacentF52Interchanger_phaseOne] at hp
  exact (by decide : (1 : ZMod 2) ≠ 0) hp

/-- The true two incident faces are distinct. Their F42
source-dependent path types are NEVER silently identified. -/
theorem c60F54AdjacentOriginalFaces_distinct
    (edge : TruncatedIcosahedralEdge) :
    c60F48AdjacentRealFace edge false ≠
      c60F48AdjacentRealFace edge true :=
  c60F48BothRealFaces_distinct edge

/-- Both distinct original F42 face sources have the SAME
complete native exchange image, without an unprovided SOURCE
transport between their different physical boundary paths. -/
theorem c60F54BothFacesOriginalF43_sameNative
    (edge : TruncatedIcosahedralEdge) :
    c60F52Eval (c60F54AdjacentF52OriginalInterchanger edge false) =
      c60F52Eval (c60F54AdjacentF52OriginalInterchanger edge true) := by
  rw [c60F54AdjacentF52Interchanger_native,
    c60F54AdjacentF52Interchanger_native]
  exact c60F48TwoFaceInterchangers_sameTarget edge

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalRotationSources
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- At each of ALL 90 physical edges and BOTH adjacent original
faces, the new F52 categorical arrow agrees with the actual
face side of the existing four-boundary F47 mixed source frame,
in FULL native 3-cell data (not just parity). -/
theorem c60F54F52Face_matchesActualF47
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F52Eval (c60F54AdjacentF52OriginalInterchanger edge side) =
      c60F44FaceThreeEval
        (c60F48EveryRealEdgeMixedFrame
          t₁ t₂ left right edge side).faceStep := by
  change (c60F48AdjacentFaceInterchanger edge side).toNative =
    (c60F48AdjacentFaceInterchanger edge side).toNative
  rfl

/-- Genuine correctly typed ORIGINAL F54/F55 square arrow
is obtained from the original F43/F52 face arrow by the UNIQUE
full-native calibration. This does not create an old F55 Δ. -/
theorem c60F54ActualOriginalF43F55_calibrated
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F52Eval (c60F54AdjacentF52OriginalInterchanger edge side) +
      c60F46FaceF55ComparisonCalibration =
      c60F44OriginalF55Eval
        (c60F48EveryRealEdgeMixedFrame
          t₁ t₂ left right edge side).rotationStep := by
  rw [c60F54F52Face_matchesActualF47]
  exact (c60F48EveryRealEdgeMixedFrame
    t₁ t₂ left right edge side).calibrated

/-- Every C60 edge/face site has exactly one possible complete
Gray calibration receiver; this proves a constraint on comparison
data, NOT the existence of an original F55 source generator. -/
theorem c60F54ActualOriginalF43F55_uniqueReceiver
    (edge : TruncatedIcosahedralEdge) (side : Bool)
    (receiver : GradedThreeCell 0 0) :
    (c60F52Eval
        (c60F54AdjacentF52OriginalInterchanger edge side) +
          receiver =
      c60F44OriginalF55Eval
        (c60F48EveryRealEdgeMixedFrame
          t₁ t₂ left right edge side).rotationStep) ↔
      receiver = c60F46FaceF55ComparisonCalibration := by
  constructor
  · intro h
    have hc := c60F54ActualOriginalF43F55_calibrated
      t₁ t₂ left right edge side
    exact add_left_cancel (h.trans hc.symm)
  · rintro rfl
    exact c60F54ActualOriginalF43F55_calibrated
      t₁ t₂ left right edge side

/-- This really is a COMMUTING SQUARE in the local FOUR-boundary
Mathlib source category with independently typed original F42
face and F54/F55 rotation source 2-cell endpoints. -/
theorem c60F54ActualOriginalF43F55_mixedSquare
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F47FaceArrow
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) ≫
    c60F47CompareAfter
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) =
    c60F47CompareBefore
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) ≫
    c60F47OriginalF55Arrow
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) :=
  c60F48AllNinetyBothFaces_mixedSquare t₁ t₂ left right edge side

/-- No original F55 nine-constructor PresentedCell can produce the
new source mixed receiver: its phase 0 and square charge 1
violate the already proved original F55 source phase lock. -/
theorem c60F54ActualCalibration_notOriginalF55 :
    c60F46FaceF55ComparisonCalibration ∉ c60F55PhaseLocked :=
  c60F46FaceF55ComparisonCalibration_notOriginalF55Locked

/-- The genuine old F55 edge field retains NONZERO signed
curvature on the actual north pentagon after our new F43-F52 bridge.
Global surface cancellation must not be mistaken for descent. -/
theorem c60F54ActualOriginalF55_northNonflat
    (side : Bool) :
    c60WangBiSignedGrayFace
      (c60F48OriginalRotationField t₁ t₂ left right side)
      (.aroundVertex .north) ≠ 0 :=
  c60F48MixedOriginalF55_northNonflat t₁ t₂ left right side

/-- Independent calibration-field obstruction:
the actual north pentagon has second integer charge -5. -/
theorem c60F54ActualCalibration_northSecondCharge
    (side : Bool) :
    (c60WangBiSignedGrayFace
      (c60F48MixedComparisonField t₁ t₂ left right side)
      (.aroundVertex .north)).charge.2 = (-5 : ℤ) :=
  c60F48MixedCalibration_northSecondCharge t₁ t₂ left right side

theorem c60F54ActualCalibration_northPhaseZero
    (side : Bool) :
    (c60WangBiSignedGrayFace
      (c60F48MixedComparisonField t₁ t₂ left right side)
      (.aroundVertex .north)).phase = (0 : ZMod 2) :=
  c60F48MixedCalibration_northPhaseZero t₁ t₂ left right side

#print axioms c60F54AdjacentF52Interchanger_isOriginalF43
#print axioms c60F54AdjacentF52Interchanger_native
#print axioms c60F54AdjacentF52Interchanger_phaseOne
#print axioms c60F54AdjacentF52Interchanger_nontrivial
#print axioms c60F54BothFacesOriginalF43_sameNative
#print axioms c60F54F52Face_matchesActualF47
#print axioms c60F54ActualOriginalF43F55_calibrated
#print axioms c60F54ActualOriginalF43F55_uniqueReceiver
#print axioms c60F54ActualOriginalF43F55_mixedSquare
#print axioms c60F54ActualCalibration_notOriginalF55
#print axioms c60F54ActualOriginalF55_northNonflat
#print axioms c60F54ActualCalibration_northSecondCharge
#print axioms c60F54ActualCalibration_northPhaseZero

end OriginalRotationSources
end
end KUOS.DependentOriginationGrayC60OriginalF43F55MixedBridgeV5_203
