import KUOS.DependentOriginationGrayC60GrayThreeCategoryCoherenceV5_197

namespace KUOS.DependentOriginationGrayC60GrayThreeCategoryPhysicalF55V5_197

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60GrayThreeCategoryCoherenceV5_197
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F49 / v5.197 — ALL 90 original F55 mixed squares at TRUE 3-category HOMs

F49's genuine ORIGINAL-C60-0/1-path Gray 3-category envelope has
a complete braided Mathlib 3-Hom category at EVERY original pair
of 1-paths. F48 proved genuine mixed C60/F55 comparison squares
for EACH of the 90 physical edges and BOTH of its actual adjacent
physical polygonal faces, with exact original F42/F54/F55 boundaries.

For each chosen real polygonal face, its physical original
five- or six-edge boundary path is doubled to obtain the ACTUAL
1-path boundary of the F48 left/right face 2-cell pasting.
At the corresponding nontrivial C60 1-path HOM, place F48's
full Mathlib mixed-square category through its existing
FAITHFUL 3-Hom Gray functor. Both independent F58 integer
charges and F59 exchange phase are preserved. The new
comparison Δ=(0,1;0) remains NOT an original F55 source.

Scope: this is an explicit LOCAL, exact physical C60 1-path
3-Hom realisation of F48's separately adjoined mixed generators,
NOT an equivalence between the distinct original global F42
surface computad and original F54 tree-rotation source.
-/

/-- Double the ORIGINAL boundary path of an ACTUAL five- or six-sided
original C60 polygon. Exactly this path is the 1-source of
the two copies of its F42 face-2-cell horizontally pasted. -/
def c60F49PhysicalFaceDoubleLoop
    (face : TruncatedIcosahedralSeedFace) :
    C60F49One
      (c60F41PhysicalFaceBoundaryLoop face).1
      (c60F41PhysicalFaceBoundaryLoop face).1 :=
  (c60F41PhysicalFaceBoundaryLoop face).2.comp
    (c60F41PhysicalFaceBoundaryLoop face).2

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section EveryRealEdge
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

/-- A REAL Mathlib functor from the original 90-edge
proof-relevant adjoined mixed source 3-Hom category into
the specific 3-Hom sitting over the ACTUAL physical
doubled polygonal C60 1-path, not an unrelated singleton. -/
def c60F49AllRealFaceMixedThreeHomFunctor
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) ⥤
    C60F49Two
      (c60F49PhysicalFaceDoubleLoop
        (c60F48AdjacentRealFace edge side))
      (Quiver.Path.nil : C60F49One
        (c60F41PhysicalFaceBoundaryLoop
          (c60F48AdjacentRealFace edge side)).1
        (c60F41PhysicalFaceBoundaryLoop
          (c60F48AdjacentRealFace edge side)).1) :=
  c60F47MixedGrayFunctor
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)

/-- Exact FULL native comparison at all 90 physical C60
edges and EITHER original polygonal surface face, now
inside a genuine path-indexed three-level Mathlib 3-Hom. -/
theorem c60F49AllRealFaceMixedComparison_fullNative
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (c60F49AllRealFaceMixedThreeHomFunctor
      t₁ t₂ left right edge side).map
        (c60F47CompareAfter
          (c60F48EveryRealEdgeMixedFrame
            t₁ t₂ left right edge side)) =
      c60F46FaceF55ComparisonCalibration := rfl

/-- The actual four-boundary mixed F47 source square still
COMMUTES as an honest categorical arrow equality INSIDE
the C60 physical doubled face 1-path three-dimensional HOM. -/
theorem c60F49AllRealFaceMixedSquare_preserved
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (c60F49AllRealFaceMixedThreeHomFunctor
      t₁ t₂ left right edge side).map
        (c60F47FaceArrow
          (c60F48EveryRealEdgeMixedFrame
            t₁ t₂ left right edge side) ≫
         c60F47CompareAfter
          (c60F48EveryRealEdgeMixedFrame
            t₁ t₂ left right edge side)) =
    (c60F49AllRealFaceMixedThreeHomFunctor
      t₁ t₂ left right edge side).map
        (c60F47CompareBefore
          (c60F48EveryRealEdgeMixedFrame
            t₁ t₂ left right edge side) ≫
         c60F47OriginalF55Arrow
          (c60F48EveryRealEdgeMixedFrame
            t₁ t₂ left right edge side)) := by
  exact congrArg
    (fun h => (c60F49AllRealFaceMixedThreeHomFunctor
      t₁ t₂ left right edge side).map h)
    (c60F48AllNinetyBothFaces_mixedSquare
      t₁ t₂ left right edge side)

/-- The original ALL-NINETY typed F55 square generator retains
its exact two integers (0,1) and independent nontrivial
exchange phase one when embedded in the original C60
physical face 3-Hom, not just a parity projection. -/
theorem c60F49AllRealFace_originalF55_fullComponents
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    ((c60F49AllRealFaceMixedThreeHomFunctor
      t₁ t₂ left right edge side).map
        (c60F47OriginalF55Arrow
          (c60F48EveryRealEdgeMixedFrame
            t₁ t₂ left right edge side))).charge =
      ((0 : Int), (1 : Int)) ∧
    ((c60F49AllRealFaceMixedThreeHomFunctor
      t₁ t₂ left right edge side).map
        (c60F47OriginalF55Arrow
          (c60F48EveryRealEdgeMixedFrame
            t₁ t₂ left right edge side))).phase =
      (1 : ZMod 2) := by
  change (c60AllNinetyGrayCell t₁ t₂ left right edge).charge =
      ((0 : Int), (1 : Int)) ∧
    (c60AllNinetyGrayCell t₁ t₂ left right edge).phase =
      (1 : ZMod 2)
  rw [c60AllNinetyGrayCell_eq]
  exact originalF55BraidedSquareGenerator_complete

/-- Even inside the complete new Gray three-category envelope,
the truly mixed comparison (0,1;0) cannot be disguised as
any original all-nine-constructor F55 3-cell. One really
must adjoin the F47 mixed comparison with its OWN source. -/
theorem c60F49AllRealFace_mixedNotOriginalF55Locked
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (c60F49AllRealFaceMixedThreeHomFunctor
      t₁ t₂ left right edge side).map
        (c60F47CompareAfter
          (c60F48EveryRealEdgeMixedFrame
            t₁ t₂ left right edge side)) ∉ c60F55PhaseLocked := by
  change c60F46FaceF55ComparisonCalibration ∉ c60F55PhaseLocked
  exact c60F46FaceF55ComparisonCalibration_notOriginalF55Locked

#print axioms c60F49AllRealFaceMixedThreeHomFunctor
#print axioms c60F49AllRealFaceMixedComparison_fullNative
#print axioms c60F49AllRealFaceMixedSquare_preserved
#print axioms c60F49AllRealFace_originalF55_fullComponents
#print axioms c60F49AllRealFace_mixedNotOriginalF55Locked

end EveryRealEdge

end
end KUOS.DependentOriginationGrayC60GrayThreeCategoryPhysicalF55V5_197
