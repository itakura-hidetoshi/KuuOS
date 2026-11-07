import KuuOSFormal.HistoricalNativeF54F47SupportLEC13
import KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
import Kuu.F112.PolygonPhysicalF47SourcePacket

/-!
# LEC-14 — inhabited original F47 / independent native C60 hexagon square

This module compares ACTUAL ORIGINAL F54/F55 two-depth raw rotation
routes and the ORIGINAL physical F47 mixed four-boundary frame against
the independently constructed north C60 hexagon F54/F55 source and
physical F42 fan/disk. The TWO original proof sources stay in different
Type-valued families. The equality is only the exactly calculated full
(Int × Int) × ZMod 2 shadow, supplemented by a genuine common C60
physical edge and polygon face at the selected north-hexagon side.

For every supplied pair of genuinely typed old local rotations, ALL
90 original physical edges and both incident faces have an inhabited
old/native square comparison packet. On the true north hexagon first
physical side, the old/new C60 edge and adjacent polygon face coincide
via the already proved physical equivalences. The old F47 mixed square
and the independent native four-boundary square retain DIFFERENT
comparison generators, and each is independently calibrated.

No source-level old-to-native F54 functor, all-nine-constructor raw
equivalence, old F42-to-native F42 typed face-cell equivalence, universal
P77/GK5CG descent, higher-stack descent or external authority is claimed.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.LivingEngiHexagonBridge

open CategoryTheory
open Kuu.F112.Physical
open KUOS.LivingEngiHistoricalBridge
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.F112ActualHistoricalF36F40BridgeP4.GenuineOriginalC60Geometry
open KUOS.F112ActualHistoricalF36F40BridgeP4.GenuineOriginalC60Geometry.ActualF47

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section TypedComparison
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- A truly inhabited comparison when supplied the concrete historical
square construction: the historical F55 raw Type, its exact categorical
arrow, the separately typed independent native six-sector F55 raw
source inside its genuine physical F42 fan/disk, and the true edge.
No field asserts equality of the distinct F54/F42 source Types. -/
structure ActualOriginalNativeHexagonSquare
    (B : C60F47SquareFrame α β r s) where
  historicalRaw : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s
  independentFrame : NativeHexagonPhysicalF47Frame
  historicalArrowExact : c60F44OriginalF55Of historicalRaw = B.rotationStep
  commonShadowExact :
    historicalF55CommonReadout historicalRaw =
      (independentFrame.higher.raw).nativeShadow
  nativeComparisonCalibrated : independentFrame.Calibrated
  physicalEdge : Edge
  physicalEdgeExact : frameKuuEdge B = physicalEdge

/-- The original raw evidence is read from its stored field and satisfies
the ORIGINAL F54-route-indexed categorical arrow, not an invented
numeric reconstruction. -/
theorem ActualOriginalNativeHexagonSquare.old_arrow_exact
    {B : C60F47SquareFrame α β r s}
    (P : ActualOriginalNativeHexagonSquare B) :
    c60F44OriginalF55Of P.historicalRaw = B.rotationStep :=
  P.historicalArrowExact

/-- Both sides have exact typed source traces, but common shadow is a
proof of observation equality, not equality of these source traces. -/
theorem ActualOriginalNativeHexagonSquare.readout_exact
    {B : C60F47SquareFrame α β r s}
    (P : ActualOriginalNativeHexagonSquare B) :
    historicalF55CommonReadout P.historicalRaw =
      (P.independentFrame.higher.raw).nativeShadow :=
  P.commonShadowExact

theorem ActualOriginalNativeHexagonSquare.native_source_exact
    {B : C60F47SquareFrame α β r s}
    (P : ActualOriginalNativeHexagonSquare B) :
    P.independentFrame.higher.raw = northHexagonNativeF55SquareCell :=
  P.independentFrame.exactRaw

theorem ActualOriginalNativeHexagonSquare.native_calibrated
    {B : C60F47SquareFrame α β r s}
    (P : ActualOriginalNativeHexagonSquare B) :
    P.independentFrame.Calibrated :=
  P.nativeComparisonCalibrated

end TypedComparison

section GenuineRealEdges

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

/-- The ORIGINAL physical square at every real edge has (0,1;1).
The old F55 raw cell is an actual constructor at actual F54 endpoints;
the proof reads its old source interpreter rather than postulating a
new arbitrary element with the desired numerical coordinates. -/
theorem original_physical_square_full_shadow
    (edge : TruncatedIcosahedralEdge) :
    historicalF55CommonReadout
        (c60F46PhysicalFlagOriginalF55Cell t₁ t₂ left right edge) =
      (((0 : Int), (1 : Int)), (1 : ZMod 2)) := by
  cases edge with
  | around a =>
      change (originalF55BraidedSquareGenerator.charge,
        originalF55BraidedSquareGenerator.phase) =
          (((0 : Int), (1 : Int)), (1 : ZMod 2))
      exact Prod.ext originalF55BraidedSquareGenerator_complete.1
        originalF55BraidedSquareGenerator_complete.2
  | cross e =>
      change (originalF55BraidedSquareGenerator.charge,
        originalF55BraidedSquareGenerator.phase) =
          (((0 : Int), (1 : Int)), (1 : ZMod 2))
      exact Prod.ext originalF55BraidedSquareGenerator_complete.1
        originalF55BraidedSquareGenerator_complete.2

/-- The independently constructed real six-sector north C60 physical
F42 fan/disk retains its exact native raw square, not just a charge. -/
theorem independent_physical_hexagon_full_shadow :
    (northHexagonPhysicalF47Frame.higher.raw).nativeShadow =
      (((0 : Int), (1 : Int)), (1 : ZMod 2)) := by
  change northHexagonNativeF55SquareCell.nativeShadow =
    (((0 : Int), (1 : Int)), (1 : ZMod 2))
  exact northHexagonNativeF55SquareCell_shadow

/-- Explicit existentially inhabited typed original/native comparison
on any REAL C60 edge and on EITHER of its two actual incident faces.
The only caller-supplied data are the genuinely typed old F54 local
rotations. No old/native numerical calibration hypothesis is supplied. -/
def actual_square_comparison
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    ActualOriginalNativeHexagonSquare
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) where
  historicalRaw := c60F46PhysicalFlagOriginalF55Cell t₁ t₂ left right edge
  independentFrame := northHexagonPhysicalF47Frame
  historicalArrowExact := rfl
  commonShadowExact := by
    calc
      historicalF55CommonReadout
          (c60F46PhysicalFlagOriginalF55Cell t₁ t₂ left right edge) =
        (((0 : Int), (1 : Int)), (1 : ZMod 2)) :=
        original_physical_square_full_shadow t₁ t₂ left right edge
      _ = (northHexagonPhysicalF47Frame.higher.raw).nativeShadow :=
        independent_physical_hexagon_full_shadow.symm
  nativeComparisonCalibrated := northHexagonPhysicalF47Frame_calibrated
  physicalEdge := edgeEquiv.symm edge
  physicalEdgeExact := rfl

theorem actual_square_comparison_exists
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    Nonempty (ActualOriginalNativeHexagonSquare
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)) :=
  ⟨actual_square_comparison t₁ t₂ left right edge side⟩

/-- This is the actual 90-edge × two-face family, not a fabricated
finite index set or an abstract uninhabited alignment requirement. -/
theorem all_real_edges_both_faces_compared :
    ∀ edge : TruncatedIcosahedralEdge, ∀ side : Bool,
      Nonempty (ActualOriginalNativeHexagonSquare
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)) := by
  intro edge side
  exact actual_square_comparison_exists t₁ t₂ left right edge side

/-- The constructed historical proof and genuine native F55 source
have precisely the same complete signed/phase observation. -/
theorem actual_square_comparison_shadow
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    historicalF55CommonReadout
      (actual_square_comparison t₁ t₂ left right edge side).historicalRaw =
      ((actual_square_comparison t₁ t₂ left right edge side).independentFrame.higher.raw).nativeShadow :=
  (actual_square_comparison t₁ t₂ left right edge side).commonShadowExact

/-- The old physical four-boundary square commutes in the actual old
Mathlib 3-Hom, independently of the native calibrated comparison. -/
theorem actual_square_comparison_original_boundary
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60F47FaceArrow (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) ≫
      c60F47CompareAfter (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) =
    c60F47CompareBefore (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) ≫
      c60F47OriginalF55Arrow
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) :=
  c60F48AllNinetyBothFaces_mixedSquare t₁ t₂ left right edge side

end GenuineRealEdges

/-! A concrete physical identification of the old selected original
hexagon face and the independent north hexagon FIRST boundary side. -/

/-- The fixed actual top hexagon first side in BOTH physical C60
presentations, transported by the pre-existing real C60 equivalence. -/
def topHexagonActualOldEdge : TruncatedIcosahedralEdge :=
  edgeEquiv (Edge.cross (.northSpoke 0))

theorem topHexagon_actual_original_face :
    c60F48AdjacentRealFace topHexagonActualOldEdge false =
      polygonEquiv (.hexagon (.top 0)) := rfl

theorem topHexagon_same_physical_first_edge :
    edgeEquiv.symm topHexagonActualOldEdge =
      cyclicBoundaryEdge (.hexagon (.top 0)) 0 := by
  calc
    edgeEquiv.symm topHexagonActualOldEdge =
        Edge.cross (.northSpoke 0) := edgeEquiv.symm_apply_apply _
    _ = cyclicBoundaryEdge (.hexagon (.top 0)) 0 :=
      northHexagonPhysical_first_edge.symm

/-- The common edge lies on the true top hexagon six-side physical
boundary. This is a geometric incidence proof, not a raw-F42
2-cell-transport identification. -/
theorem topHexagon_actual_native_incidence :
    Site.edge (cyclicBoundaryEdge (.hexagon (.top 0)) 0) ≤
      Site.face (.hexagon (.top 0)) :=
  (northHexagonPhysical_original_flag 0).2.1

section TopHexagonConcreteComparison
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

/-- The actual old F47 first face is this exact independent north
hexagon, and the retained C60 edge matches the real first native
hexagon side, while both typed F54/F55 proof terms remain separate. -/
theorem top_hexagon_paired_physical_support :
    (actual_square_comparison t₁ t₂ left right
      topHexagonActualOldEdge false).physicalEdge =
        cyclicBoundaryEdge (.hexagon (.top 0)) 0 ∧
    c60F48AdjacentRealFace topHexagonActualOldEdge false =
        polygonEquiv (.hexagon (.top 0)) := by
  constructor
  · exact topHexagon_same_physical_first_edge
  · exact topHexagon_actual_original_face

/-- A single constructed packet retains BOTH fully typed real-source
F55 square witnesses and the correct physical first edge. -/
theorem top_hexagon_inhabited_exact_source_and_support :
    ∃ P : ActualOriginalNativeHexagonSquare
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right
          topHexagonActualOldEdge false),
      P.physicalEdge = cyclicBoundaryEdge (.hexagon (.top 0)) 0 ∧
      P.independentFrame.higher.raw = northHexagonNativeF55SquareCell ∧
      historicalF55CommonReadout P.historicalRaw =
        (P.independentFrame.higher.raw).nativeShadow := by
  refine ⟨actual_square_comparison t₁ t₂ left right
    topHexagonActualOldEdge false, ?_, ?_, ?_⟩
  · exact (top_hexagon_paired_physical_support t₁ t₂ left right).1
  · exact (actual_square_comparison t₁ t₂ left right
      topHexagonActualOldEdge false).native_source_exact
  · exact (actual_square_comparison t₁ t₂ left right
      topHexagonActualOldEdge false).commonShadowExact

end TopHexagonConcreteComparison

#print axioms ActualOriginalNativeHexagonSquare.old_arrow_exact
#print axioms ActualOriginalNativeHexagonSquare.readout_exact
#print axioms ActualOriginalNativeHexagonSquare.native_source_exact
#print axioms ActualOriginalNativeHexagonSquare.native_calibrated
#print axioms original_physical_square_full_shadow
#print axioms independent_physical_hexagon_full_shadow
#print axioms actual_square_comparison
#print axioms actual_square_comparison_exists
#print axioms all_real_edges_both_faces_compared
#print axioms actual_square_comparison_shadow
#print axioms actual_square_comparison_original_boundary
#print axioms topHexagon_actual_original_face
#print axioms topHexagon_same_physical_first_edge
#print axioms topHexagon_actual_native_incidence
#print axioms top_hexagon_paired_physical_support
#print axioms top_hexagon_inhabited_exact_source_and_support

end
end KUOS.LivingEngiHexagonBridge
