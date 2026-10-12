import KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195

namespace KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
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
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.196 / F59-F48 — ORIGINAL 90-edge × two-adjacent-face mixed squares

All 90 genuine C60 edges carry two distinct, incident, original
five- or six-sided physical faces. For EACH of the 180 face choices
we construct the original Type-valued F42 physical face 2-cell,
its ORIGINAL F43 interchanger with itself, the genuine original
F54/F55 left-first/right-first rotation route 2-cells and 3-arrow,
and the F47 four-boundary mixed comparison category.

The previously proven native Δ=(0,1;0) calibrates the ORIGINAL
C60 face interchange (0,0;1) to the ORIGINAL F55 square (0,1;1)
at EVERY actual physical edge and either physically incident face.
The mixed square COMMUTES in a genuine typed local Mathlib category,
not merely as an untyped target value.

The two face choices are truly DISTINCT polygonal faces and have
different original source path/2-cell boundary types. Only their
FULL target Gray images agree: no unprovided source transport,
new fictitious quadrilateral C60 face, or global nondegenerate
Gray 3-functor is silently postulated.
-/

/-- An actual polygonal C60 surface face incident to the given
edge, selected among the two different original incident faces. -/
def c60F48AdjacentRealFace
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    TruncatedIcosahedralSeedFace :=
  (c60F46PhysicalFourFlagSquare edge).face side

theorem c60F48AdjacentRealFace_incident
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    truncatedEdgeOnSeedFace edge (c60F48AdjacentRealFace edge side) := by
  cases side with
  | false =>
      exact (c60F46PhysicalFourFlagSquare edge).firstIncident
  | true =>
      exact (c60F46PhysicalFourFlagSquare edge).secondIncident

/-- The two polygonal faces on every REAL edge are unequal.
The K₂,₂ four-flag carrier is not a quadrilateral C60 face. -/
theorem c60F48BothRealFaces_distinct
    (edge : TruncatedIcosahedralEdge) :
    c60F48AdjacentRealFace edge false ≠
      c60F48AdjacentRealFace edge true :=
  (c60F46PhysicalFourFlagSquare edge).faces_ne

theorem c60F48EveryFlagCorner_isIncident
    (edge : TruncatedIcosahedralEdge) (endpoint side : Bool) :
    truncatedDartOnSeedFace
      ((c60F46PhysicalFourFlagSquare edge).vertex endpoint)
      (c60F48AdjacentRealFace edge side) :=
  c60F46PhysicalFourFlagSquare_allFourIncidences edge endpoint side

/-- The unchanged original exact FIVE- or SIX-edge physical-face
source 2-cell, with its original (non-erased) dependent 1-path
endpoints. The shape is determined by actual adjacency. -/
def c60F48AdjacentFaceTwoCell
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    C60F42PresentedFaceCell
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace edge side)).2
      Quiver.Path.nil :=
  .physicalFace (c60F48AdjacentRealFace edge side)

/-- The two original source horizontal composition orders of
that very same original polygonal face 2-cell are compared by
a true Type-valued ORIGINAL C60 F43 interchange 3-cell. -/
def c60F48AdjacentFaceInterchanger
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    C60F43PresentedThreeCell
      ((c60F48AdjacentFaceTwoCell edge side).horizontalLeftFirst
        (c60F48AdjacentFaceTwoCell edge side))
      ((c60F48AdjacentFaceTwoCell edge side).horizontalRightFirst
        (c60F48AdjacentFaceTwoCell edge side)) :=
  .interchange (c60F48AdjacentFaceTwoCell edge side)
    (c60F48AdjacentFaceTwoCell edge side)

/-- For EVERY pentagon and hexagon on EVERY real edge, the
complete native C60 source interchanger is (0,0;1), identical
as a Gray target 3-cell to the true north pentagon generator.
This does NOT equate their differently typed SOURCE 2-cells. -/
theorem c60F48AdjacentFaceInterchanger_native
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (c60F48AdjacentFaceInterchanger edge side).toNative =
      c60F43NorthPentagonInterchange.toNative := by
  apply GradedThreeCell.ext
  · rfl
  · rfl

/-- Both TRUE incident faces carry matching FULL target
Int×Int charge and independent exchange phase, despite
distinct source polygon boundary paths. -/
theorem c60F48TwoFaceInterchangers_sameTarget
    (edge : TruncatedIcosahedralEdge) :
    (c60F48AdjacentFaceInterchanger edge false).toNative =
      (c60F48AdjacentFaceInterchanger edge true).toNative := by
  rw [c60F48AdjacentFaceInterchanger_native,
    c60F48AdjacentFaceInterchanger_native]

/-- The original first adjacent face is always a REAL pentagon
on around-edges, and a REAL hexagon on cross-edges. -/
theorem c60F48AroundFirst_isPentagon
    (a : TruncatedIcosahedralAroundEdge) :
    c60F48AdjacentRealFace (.around a) false =
      .aroundVertex a.center :=
  c60F46AroundFlag_firstRealPentagon a

theorem c60F48CrossFirst_isHexagon
    (e : IcosahedralEdge) :
    c60F48AdjacentRealFace (.cross e) false =
      .fromTriangle (icosahedralEdgeIncidentFaces e).1 :=
  c60F46CrossFlag_firstHexagon e

theorem c60F48CrossSecond_isHexagon
    (e : IcosahedralEdge) :
    c60F48AdjacentRealFace (.cross e) true =
      .fromTriangle (icosahedralEdgeIncidentFaces e).2 :=
  c60F46CrossFlag_secondHexagon e

/-! ## All 90 × 2 genuinely typed F47 source squares -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section RealSourceAllEdges
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

/-- A full four-boundary MIXED source frame at any of the
90 real physical C60 edges and EITHER of its two actual faces.
Both original source 3-arrows retain their original independent
dependent source 2-cell boundaries and proof-relevant witnesses. -/
def c60F48EveryRealEdgeMixedFrame
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    C60F47SquareFrame
      ((c60F48AdjacentFaceTwoCell edge side).horizontalLeftFirst
        (c60F48AdjacentFaceTwoCell edge side))
      ((c60F48AdjacentFaceTwoCell edge side).horizontalRightFirst
        (c60F48AdjacentFaceTwoCell edge side))
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right) where
  edge := edge
  faceStep :=
    c60F44FaceThreeOf (c60F48AdjacentFaceInterchanger edge side)
  rotationStep := c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right edge
  calibrated := by
    change (c60F48AdjacentFaceInterchanger edge side).toNative +
        c60F46FaceF55ComparisonCalibration =
      c60F44OriginalF55GrayFunctor.map
        (c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right edge)
    rw [c60F48AdjacentFaceInterchanger_native,
      c60F46PhysicalFlagOriginalF55Arrow_fullNative,
      c60AllNinetyGrayCell_eq]
    exact c60F46NativeNorthFaceF55_calibrated

theorem c60F48EveryRealEdgeMixedFrame_edge
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side).edge =
      edge := rfl

/-- A genuine Mathlib 3-Hom SOURCE equality for ALL physical
edge/face choices. No untyped or phase-only identification:
the new boundary-comparison generators are exactly the
separately typed F47 mixed source arrows. -/
theorem c60F48AllNinetyBothFaces_mixedSquare
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F47FaceArrow
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) ≫
        c60F47CompareAfter
          (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) =
    c60F47CompareBefore
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) ≫
        c60F47OriginalF55Arrow
          (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) :=
  c60F47MixedOriginalBoundarySquare
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)

/-- The two ORIGINAL source 3-arrows have the exact Gray
target comparison at every real edge, without projecting
away the independent integer square charge. -/
theorem c60F48EveryRealEdgeMixedFrame_calibrated
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F44FaceThreeEval
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side).faceStep +
      c60F46FaceF55ComparisonCalibration =
    c60F44OriginalF55Eval
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side).rotationStep :=
  (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side).calibrated

theorem c60F48EveryRealEdgeFaceStep_native
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F44FaceThreeEval
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side).faceStep =
      c60F43NorthPentagonInterchange.toNative := by
  change (c60F48AdjacentFaceInterchanger edge side).toNative = _
  exact c60F48AdjacentFaceInterchanger_native edge side

/-- Source and target mixed comparison are themselves original
typed arrows in the ADJOINED F47 category, evaluated in its
FAITHFUL complete Gray target. The new non-phase-locked
calibration is NOT asserted to be an original F55 source. -/
theorem c60F48EveryRealEdgeComparison_fullNative
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (c60F47MixedGrayFunctor
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)).map
        (c60F47CompareAfter
          (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)) =
            c60F46FaceF55ComparisonCalibration := rfl

/-- Every original physical four-flag incidence carrier
contributes exactly TWO independent actual polygon face choices
to the typed comparison; no new face has been manufactured. -/
theorem c60F48PhysicalEdgeCount :
    Fintype.card TruncatedIcosahedralEdge = 90 :=
  truncatedIcosahedralEdge_card

#print axioms c60F48AdjacentRealFace_incident
#print axioms c60F48BothRealFaces_distinct
#print axioms c60F48EveryFlagCorner_isIncident
#print axioms c60F48AdjacentFaceInterchanger_native
#print axioms c60F48TwoFaceInterchangers_sameTarget
#print axioms c60F48EveryRealEdgeMixedFrame
#print axioms c60F48AllNinetyBothFaces_mixedSquare
#print axioms c60F48EveryRealEdgeMixedFrame_calibrated
#print axioms c60F48EveryRealEdgeComparison_fullNative

end RealSourceAllEdges

end
end KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
