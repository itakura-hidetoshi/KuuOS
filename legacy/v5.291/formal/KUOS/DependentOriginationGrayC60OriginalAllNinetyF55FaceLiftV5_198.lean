import KUOS.DependentOriginationGrayC60OriginalFaceWhiskeringNaturalityV5_198
import KUOS.DependentOriginationGrayC60GrayThreeCategoryPhysicalF55V5_197

namespace KUOS.DependentOriginationGrayC60OriginalAllNinetyF55FaceLiftV5_198

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60GrayThreeCategoryPhysicalF55V5_197
open KUOS.DependentOriginationGrayC60OriginalFaceTypedThreeHomLiftV5_198
open KUOS.DependentOriginationGrayC60OriginalFaceDecoratedThreeHomV5_198
open KUOS.DependentOriginationGrayC60OriginalFaceWhiskeringNaturalityV5_198
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.198 / F59-F50 — original physical F42/F43 3-cell source at all flags

F48 proved a genuine original F42 face 2-cell source with F43
interchanger at each of the 90 physical C60 edges and either
one of the two ACTUAL incident polygonal surface faces. F47
attached the genuine original F54/F55 local rotation-square
source, but required a distinct NEW mixed comparison receiver.

This file transports the ACTUAL F43 categorical source
3-arrow from each true F48 source frame through the NEW F50
faithful original 3-Hom functor into F49's 60-object graded
Gray 3-category envelope, at the EXACT original doubled
physical polygonal face 1-path. BOTH original F42 boundary
2-cell witnesses survive in the functor DOMAIN.

We prove their full native integer/phase components and the
precise original F55 square calibration in both independent
integer charge and exchange phase coordinates at every one
of the 180 actual edge-by-adjacent-face placements.

No unsupported original F54-to-F42 2-cell identification,
faithfulness on raw F42 objects into grade-only GrayGrade,
global original F55 3-functor, or fake flatness is asserted.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section EveryRealOriginalFace
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

/-- Original F48 physical FACE source 3-morphism, from the
original F42 proof-relevant categorical 3-Hom, now lifted
by a faithful higher-source functor to the actual physical
1-path Gray 3-Hom, NOT an invented neutral target constant. -/
def c60F50AllRealFlagsOriginalFaceTypedThree
    (edge : TruncatedIcosahedralEdge) (side : Bool) :=
  (c60F50OriginalFaceTypedThreeHomFunctor
    (c60F49PhysicalFaceDoubleLoop
      (c60F48AdjacentRealFace edge side))
    (Quiver.Path.nil)).map
      (c60F48EveryRealEdgeMixedFrame
        t₁ t₂ left right edge side).faceStep

/-- The exact actual source F43 original interchange witness
is preserved, with both actual horizontal-pasting F42
2-cell boundary terms retained in the input category. -/
theorem c60F50AllRealFlagsOriginalFaceTypedThree_eqRaw
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F50AllRealFlagsOriginalFaceTypedThree
      t₁ t₂ left right edge side =
      c60F49OriginalFaceThree
        (c60F48AdjacentFaceInterchanger edge side) := by
  exact c60F50OriginalRawThreeCell_map
    (c60F48AdjacentFaceInterchanger edge side)

/-- Every original physical pentagon or hexagon face F43
interchanger still has the exact charge (0,0) and exchange
phase 1 after ORIGINAL source-aware categorical transport. -/
theorem c60F50AllRealFlagsOriginalFaceTypedThree_components
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (c60F50AllRealFlagsOriginalFaceTypedThree
      t₁ t₂ left right edge side).charge =
        ((0 : Int), (0 : Int)) ∧
    (c60F50AllRealFlagsOriginalFaceTypedThree
      t₁ t₂ left right edge side).phase =
        (1 : ZMod 2) := by
  rw [c60F50AllRealFlagsOriginalFaceTypedThree_eqRaw]
  constructor
  · change (c60F48AdjacentFaceInterchanger edge side).toNative.charge =
        ((0 : Int), (0 : Int))
    rw [c60F48AdjacentFaceInterchanger_native]
    exact c60F43NorthPentagonInterchange_components.1
  · change (c60F48AdjacentFaceInterchanger edge side).toNative.phase =
        (1 : ZMod 2)
    rw [c60F48AdjacentFaceInterchanger_native]
    exact c60F43NorthPentagonInterchange_components.2

/-- Original F43 face/source typed 3-cell and the NEW genuine
mixed calibration have exactly the original true F55 square
generator's two integer charges and the independent phase,
without falsely creating an original F55 source for Δ. -/
theorem c60F50AllRealFlagsOriginalF55_calibrationComponents
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (c60F50AllRealFlagsOriginalFaceTypedThree
      t₁ t₂ left right edge side).charge +
        c60F46FaceF55ComparisonCalibration.charge =
      originalF55BraidedSquareGenerator.charge ∧
    (c60F50AllRealFlagsOriginalFaceTypedThree
      t₁ t₂ left right edge side).phase +
        c60F46FaceF55ComparisonCalibration.phase =
      originalF55BraidedSquareGenerator.phase := by
  rw [c60F50AllRealFlagsOriginalFaceTypedThree_eqRaw]
  have hcal := c60F46NativeNorthFaceF55_calibrated
  constructor
  · change
      (c60F48AdjacentFaceInterchanger edge side).toNative.charge +
        c60F46FaceF55ComparisonCalibration.charge =
      originalF55BraidedSquareGenerator.charge
    rw [c60F48AdjacentFaceInterchanger_native]
    have hcharge := congrArg GradedThreeCell.charge hcal
    rw [grayNeutral_add_charge] at hcharge
    exact hcharge
  · change
      (c60F48AdjacentFaceInterchanger edge side).toNative.phase +
        c60F46FaceF55ComparisonCalibration.phase =
      originalF55BraidedSquareGenerator.phase
    rw [c60F48AdjacentFaceInterchanger_native]
    have hphase := congrArg GradedThreeCell.phase hcal
    rw [grayNeutral_add_phase] at hphase
    exact hphase

#print axioms c60F50AllRealFlagsOriginalFaceTypedThree
#print axioms c60F50AllRealFlagsOriginalFaceTypedThree_eqRaw
#print axioms c60F50AllRealFlagsOriginalFaceTypedThree_components
#print axioms c60F50AllRealFlagsOriginalF55_calibrationComponents

end EveryRealOriginalFace

end
end KUOS.DependentOriginationGrayC60OriginalAllNinetyF55FaceLiftV5_198
