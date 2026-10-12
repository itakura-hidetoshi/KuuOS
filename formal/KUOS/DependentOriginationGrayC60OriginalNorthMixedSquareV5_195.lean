import KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195

namespace KUOS.DependentOriginationGrayC60OriginalNorthMixedSquareV5_195

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.195 / F59-F47 — actual north C60 face / F54–F55 mixed square

Instantiates the separately defined mixed FOUR-boundary category on:
  • the genuine north C60 5-edge pentagon face 2-cell repeated twice;
  • the two original F54 left-first/right-first rotation paths;
  • their respective actual original source 3-arrows;
  • the genuine north pentagon/hexagon physical edge and four flags.

The source and target boundary comparisons are NEW mixed 3-cells,
not original F55 PresentedCell constructors. Their native images
are exactly 0 and Δ=(0,1;0), and the comparison square commutes
within the actual typed local mixed Mathlib 3-Hom. This is a local
piece of a potential global Gray presentation, NOT a global one.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section RealNorthOriginalSquare
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

/-- Four *original* 2-cell boundaries and the two actual
original source 3-arrows, tied to the genuine north C60
physical pentagon/hexagon edge. No hypothesis invents a
new F55 cell: its native calibration follows from F46. -/
def c60F47NorthActualMixedFrame :
    C60F47SquareFrame
      (c60F43NorthPentagonFaceTwoCell.horizontalLeftFirst
        c60F43NorthPentagonFaceTwoCell)
      (c60F43NorthPentagonFaceTwoCell.horizontalRightFirst
        c60F43NorthPentagonFaceTwoCell)
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right) where
  edge := .around ⟨.north, .s0⟩
  faceStep := c60F44FaceThreeOf c60F43NorthPentagonInterchange
  rotationStep :=
    c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right
      (.around ⟨.north, .s0⟩)
  calibrated := by
    change c60F43NorthPentagonInterchange.toNative +
        c60F46FaceF55ComparisonCalibration =
      c60F44OriginalF55GrayFunctor.map
        (c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right
          (.around ⟨.north, .s0⟩))
    rw [c60F46PhysicalFlagOriginalF55Arrow_fullNative,
        c60AllNinetyGrayCell_eq]
    exact c60F46NativeNorthFaceF55_calibrated

/-- The MIXED source category's fixed edge is the genuine
north original pentagon/hexagon C60 physical edge. -/
theorem c60F47NorthActualMixedFrame_edge :
    (c60F47NorthActualMixedFrame t₁ t₂ left right).edge =
      (.around ⟨.north, .s0⟩ : TruncatedIcosahedralEdge) := rfl

/-- This mixed square rests on four actual C60 physical
vertex/face incidences, not on a fictitious square face. -/
theorem c60F47NorthMixedAllFourIncidences (i j : Bool) :
    truncatedDartOnSeedFace
      ((c60F46PhysicalFourFlagSquare
        (c60F47NorthActualMixedFrame t₁ t₂ left right).edge).vertex i)
      ((c60F46PhysicalFourFlagSquare
        (c60F47NorthActualMixedFrame t₁ t₂ left right).edge).face j) := by
  exact c60F46PhysicalFourFlagSquare_allFourIncidences
    (c60F47NorthActualMixedFrame t₁ t₂ left right).edge i j

/-- The exact ORIGINAL north pentagon face is the first
face of this physically valid mixed four-flag square. -/
theorem c60F47NorthMixedFirstFacePentagon :
    (c60F46PhysicalFourFlagSquare
      (c60F47NorthActualMixedFrame t₁ t₂ left right).edge).firstFace =
        (.aroundVertex .north) := rfl

/-- Nontrivial result: the actual C60 pentagon interchanger
and actual original F55 square are related by TWO separately
typed mixed 3-arrows in an honest four-boundary source category.
The equality is of SOURCE categorical composite arrows, not
merely an untyped equation of target integers and phases. -/
theorem c60F47NorthActualMixedBoundarySquare :
    c60F47FaceArrow (c60F47NorthActualMixedFrame t₁ t₂ left right) ≫
      c60F47CompareAfter (c60F47NorthActualMixedFrame t₁ t₂ left right) =
    c60F47CompareBefore (c60F47NorthActualMixedFrame t₁ t₂ left right) ≫
      c60F47OriginalF55Arrow
        (c60F47NorthActualMixedFrame t₁ t₂ left right) :=
  c60F47MixedOriginalBoundarySquare
    (c60F47NorthActualMixedFrame t₁ t₂ left right)

/-- The new target boundary comparison is INCOMPATIBLE with the
phase-locked all-nine-constructor original F55 source image:
it must genuinely be added as a mixed generator. -/
theorem c60F47NorthCompareAfter_notOriginalF55PhaseLocked :
    (c60F47MixedGrayFunctor
      (c60F47NorthActualMixedFrame t₁ t₂ left right)).map
        (c60F47CompareAfter
          (c60F47NorthActualMixedFrame t₁ t₂ left right))
      ∉ c60F55PhaseLocked := by
  change c60F46FaceF55ComparisonCalibration ∉ c60F55PhaseLocked
  exact c60F46FaceF55ComparisonCalibration_notOriginalF55Locked

/-- The same genuine mixed source comparison square stays
compatible with arbitrary additional independently typed Gray
horizontal 3-cell tensoring, using the original F59 tensor law. -/
theorem c60F47NorthMixedSquare_tensor
    {i j : ZMod 2} (h : GradedThreeCell i j) :
    ((c60F44FaceThreeEval
       (c60F47NorthActualMixedFrame t₁ t₂ left right).faceStep).tensor h).comp
        (c60F46FaceF55ComparisonCalibration.tensor
          (GradedThreeCell.ident j)) =
      ((GradedThreeCell.ident 0).tensor h).comp
        ((c60F44OriginalF55Eval
          (c60F47NorthActualMixedFrame t₁ t₂ left right).rotationStep).tensor
          (GradedThreeCell.ident j)) :=
  c60F47MixedSquare_tensor_naturality
    (c60F47NorthActualMixedFrame t₁ t₂ left right) h

#print axioms c60F47NorthActualMixedFrame
#print axioms c60F47NorthMixedAllFourIncidences
#print axioms c60F47NorthMixedFirstFacePentagon
#print axioms c60F47NorthActualMixedBoundarySquare
#print axioms c60F47NorthCompareAfter_notOriginalF55PhaseLocked
#print axioms c60F47NorthMixedSquare_tensor

end RealNorthOriginalSquare

end
end KUOS.DependentOriginationGrayC60OriginalNorthMixedSquareV5_195
