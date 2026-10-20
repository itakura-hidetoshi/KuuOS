import KuuOSFormal.HistoricalF36F40BridgeP4
import Kuu.F112.PolygonPhysicalMixedChargeFunctorNonfaithful
import Mathlib.Tactic.Abel
import Mathlib.Tactic.NormNum

/-!
# F112-P36 — actual historical F47 geometry and honest native calibration transport

This is an OLD-SIDE-only theorem carrier in the existing KuuOSFormal
library namespace. It imports the original frozen historical F47/Gray
source THROUGH the already verified P4 old/new geometry bridge.
It must NOT be imported into KuuOSStrict or Kuu.F112.

The ACTUAL original F47 C60F47SquareFrame is indexed by its
independent F42 physical-face 2-cell pair and genuine F54/F55
rotation-route pair, and contains a certified old mixed square.
P4 already reconstructed its exact native physical edge, original
dart endpoints and the two distinct adjacent original polygons.

P36 now constructs TWO complete independently typed native F42
polygon fan/disk atlases from precisely those original F47 adjacent
faces, retaining the REAL old physical edge and the full historical
two-axis witness. Every side/disk is sound in genuine F69
localization; the originally indexed face/rotation 3-arrows and
calibrated old four-boundary square remain in the packet.

The original F47 after-comparison has coordinates ((0,1),0).
The distinct independently presented P33–P35 native north-hexagon
physical-F42/F55 mixed comparison needs ((0,0),nonzero phase).
These are NOT the same shadow! We prove explicit impossibility of
unmodified coordinate identification and the unique additive
correction required by ANY direct coordinate comparison, with
signed charge (0,-1) and NONZERO ZMod2 phase.

The arbitrary historical F47 frame has NO presumed north-hexagon
match: the real first and second polygon atlases are indexed by
the old frame's real physical edge, not by a chosen proxy hexagon.
No historical/new 3-Hom equivalence, Beck-Chevalley or global
F68/F77 curvature result is inferred by fiat. No new axioms/sorry.
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

set_option autoImplicit false
set_option warningAsError true
noncomputable section

universe uP36 vP36 uDP36 vDP36
variable {C : Type uP36} [Category.{vP36} C]
variable {D : Type uDP36} [Category.{vDP36} D]
variable {a b : C} {x y : D} {n n' m m' : Nat}
variable {ma mb : OldBlocks a b} {pa pb : OldBlocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- An actual historical F47 source boundary frame B with its true
old C60 edge, reconstructed constructor-wise as a Kuu 90-edge,
BOTH distinct original adjacent polygon faces, their entire
TYPE-valued five/six-sector F42 face source atlas, and the
previously verified actual F19/F28 original native-axis witness. -/
structure HistoricalF47TwoFaceNativeAtlas
    (B : C60F47SquareFrame α β r s) where
  edge : Edge
  edgeToHistorical : edgeEquiv edge = B.edge
  firstFace : Polygon
  secondFace : Polygon
  firstFace_eq : firstFace = faceAt edge false
  secondFace_eq : secondFace = faceAt edge true
  firstSource : PolygonSourcePresentation firstFace
  secondSource : PolygonSourcePresentation secondFace
  nativeHistories : GenuineOriginalF47.F47NativeBoundaryWitness B

/-- The atlas is built from the ACTUAL historical edge/face frame
and the independently proved Kuu vertex/edge/face equivalences.
There is no artificial north-hexagon match for arbitrary B. -/
def historicalF47TwoFaceNativeAtlas
    (B : C60F47SquareFrame α β r s) :
    HistoricalF47TwoFaceNativeAtlas B where
  edge := frameKuuEdge B
  edgeToHistorical := frameKuuEdge_roundtrip B
  firstFace := (frameKuuFaces B).1
  secondFace := (frameKuuFaces B).2
  firstFace_eq := rfl
  secondFace_eq := rfl
  firstSource := canonicalPolygonSource (frameKuuFaces B).1
  secondSource := canonicalPolygonSource (frameKuuFaces B).2
  nativeHistories := GenuineOriginalF47.F47NativeBoundaryWitness.ofFrame B

/-- The historical original F47 edge lies on its independently
reconstructed FIRST genuine native polygon boundary. -/
theorem HistoricalF47TwoFaceNativeAtlas.firstEdge_onBoundary
    {B : C60F47SquareFrame α β r s}
    (P : HistoricalF47TwoFaceNativeAtlas B) :
    P.edge ∈ polygonBoundaryEdges P.firstFace := by
  apply (originalEdge_polygonBoundary_iff P.edge P.firstFace).2
  exact Or.inl P.firstFace_eq

/-- The same physical old edge lies on the SECOND original polygon
boundary, retaining the real two-face incidence instead of a
fabricated square-face or generic finite-cardinality witness. -/
theorem HistoricalF47TwoFaceNativeAtlas.secondEdge_onBoundary
    {B : C60F47SquareFrame α β r s}
    (P : HistoricalF47TwoFaceNativeAtlas B) :
    P.edge ∈ polygonBoundaryEdges P.secondFace := by
  apply (originalEdge_polygonBoundary_iff P.edge P.secondFace).2
  exact Or.inr P.secondFace_eq

/-- The two original C60 faces incident to this F47 edge really are
DISTINCT. No historical polygonal source faces are identified. -/
theorem HistoricalF47TwoFaceNativeAtlas.faces_ne
    {B : C60F47SquareFrame α β r s}
    (P : HistoricalF47TwoFaceNativeAtlas B) :
    P.firstFace ≠ P.secondFace := by
  rw [P.firstFace_eq, P.secondFace_eq]
  exact everyPhysicalEdge_two_distinct_faces P.edge

/-- The actual old F47 physical edge's original ordered endpoints
are recovered by the verified constructor-wise dart equivalence,
not merely by the equality of edge counts. -/
theorem HistoricalF47TwoFaceNativeAtlas.oldDartEndpoints
    {B : C60F47SquareFrame α β r s}
    (P : HistoricalF47TwoFaceNativeAtlas B) :
    (truncatedIcosahedralEdgeEndpoints B.edge).1 =
      dartEquiv (edgeEndpoints P.edge).1 ∧
    (truncatedIcosahedralEdgeEndpoints B.edge).2 =
      dartEquiv (edgeEndpoints P.edge).2 := by
  rw [← P.edgeToHistorical]
  exact edgeEndpoints_equiv P.edge

/-- Every actual first-face F42 raw sector in the historical
F47 frame has its ORIGINAL F69 localization interpretation;
this is a theorem about a Type-valued proof retained in P. -/
theorem HistoricalF47TwoFaceNativeAtlas.firstSector_localized
    {B : C60F47SquareFrame α β r s}
    (P : HistoricalF47TwoFaceNativeAtlas B)
    (i : PolygonBoundarySector P.firstFace) :
    zigzagToLocalization (polygonRawSide P.firstFace i.1 i.2) =
      zigzagToLocalization (polygonConeRawSide P.firstFace i.1 i.2) :=
  (P.firstSource.sector i.1 i.2).localized_sound

/-- Ditto the genuinely different second-face original F42
source, indexed by its own genuine five/six-sided boundary. -/
theorem HistoricalF47TwoFaceNativeAtlas.secondSector_localized
    {B : C60F47SquareFrame α β r s}
    (P : HistoricalF47TwoFaceNativeAtlas B)
    (i : PolygonBoundarySector P.secondFace) :
    zigzagToLocalization (polygonRawSide P.secondFace i.1 i.2) =
      zigzagToLocalization (polygonConeRawSide P.secondFace i.1 i.2) :=
  (P.secondSource.sector i.1 i.2).localized_sound

/-- The first original F47 adjacent polygon disk closes in the
exact independent C60 F69 kernel, without erasing its raw proof. -/
theorem HistoricalF47TwoFaceNativeAtlas.firstDisk_kernel
    {B : C60F47SquareFrame α β r s}
    (P : HistoricalF47TwoFaceNativeAtlas B) :
    zigzagKernelQ.map (polygonRawLoop P.firstFace) =
      zigzagKernelQ.map
        (Zigzag.nil (Site.vertex (cyclicBoundaryDart P.firstFace 0))) :=
  P.firstSource.disk.kernel_sound

/-- The other ORIGINAL adjacent face disk is independently
kernel-sound; it is not forced equal to the first disk. -/
theorem HistoricalF47TwoFaceNativeAtlas.secondDisk_kernel
    {B : C60F47SquareFrame α β r s}
    (P : HistoricalF47TwoFaceNativeAtlas B) :
    zigzagKernelQ.map (polygonRawLoop P.secondFace) =
      zigzagKernelQ.map
        (Zigzag.nil (Site.vertex (cyclicBoundaryDart P.secondFace 0))) :=
  P.secondSource.disk.kernel_sound

/-- The historical F47 frame still contains the EXACT original,
separately typed F42 face and F55 rotation 3-Hom arrows and its
proved calibrated mixed square. Native sector data do not replace
either historical source arrow. -/
theorem HistoricalF47TwoFaceNativeAtlas.original_square
    {B : C60F47SquareFrame α β r s}
    (_P : HistoricalF47TwoFaceNativeAtlas B) :
    c60F47FaceArrow B ≫ c60F47CompareAfter B =
      c60F47CompareBefore B ≫ c60F47OriginalF55Arrow B :=
  c60F47MixedOriginalBoundarySquare B

/-- Original historical F47 after-comparison, in the independent
native SHADOW CARRIER (Int×Int)×ZMod2. This is a READING of actual
historical source output, NOT a claimed source-level equivalence
of original and new higher 3-Homs. -/
def historicalF47AfterCoordinates
    (B : C60F47SquareFrame α β r s) : KuuNativeF55Shadow :=
  (((c60F47MixedGrayFunctor B).map
      (c60F47CompareAfter B)).charge,
    ((c60F47MixedGrayFunctor B).map
      (c60F47CompareAfter B)).phase)

/-- The original genuinely calibrated F47 compare-after arrow has
square generator charge one and exchange phase ZERO. -/
theorem historicalF47AfterCoordinates_components
    (B : C60F47SquareFrame α β r s) :
    (historicalF47AfterCoordinates B).1 = ((0 : Int), (1 : Int)) ∧
    (historicalF47AfterCoordinates B).2 = (0 : ZMod 2) :=
  c60F47CompareAfter_native_components B

/-- The historical F47 bridge's true signed charge is incompatible
with the NATIVE north-hexagon P33–P35 mixed bridge's zero charge.
This is an explicit source-calibration obstruction; the compared
physical edges are not asserted to be equal without geometric data. -/
theorem historicalF47After_ne_nativeMixedCorrection
    (B : C60F47SquareFrame α β r s) :
    historicalF47AfterCoordinates B ≠
      northHexagonPhysicalMixedCalibrated.compareAfter := by
  intro h
  have hcharge : ((0 : Int), (1 : Int)) =
      ((0 : Int), (0 : Int)) := by
    calc
      ((0 : Int), (1 : Int)) =
          (historicalF47AfterCoordinates B).1 :=
        ((historicalF47AfterCoordinates_components B).1).symm
      _ = northHexagonPhysicalMixedCalibrated.compareAfter.1 :=
        congrArg Prod.fst h
      _ = ((0 : Int), (0 : Int)) :=
        northHexagonPhysicalMixedCorrection_charge_zero
  exact (by decide : ((0 : Int), (1 : Int)) ≠
    ((0 : Int), (0 : Int))) hcharge

/-- A REQUIRED explicit affine change-of-calibration datum between
these two chosen original/new output coordinate presentations.
It is not a claimed canonical source 3-functor or equivalence. -/
def historicalToNativeCorrectionShift
    (B : C60F47SquareFrame α β r s) : KuuNativeF55Shadow :=
  northHexagonPhysicalMixedCalibrated.compareAfter -
    historicalF47AfterCoordinates B

/-- With this EXPLICIT additional transport correction, the
original calibrated after-comparison reaches the exact new mixed
receiver after-comparison at the SHADOW level. -/
theorem historicalToNativeCorrectionShift_sound
    (B : C60F47SquareFrame α β r s) :
    historicalF47AfterCoordinates B +
      historicalToNativeCorrectionShift B =
        northHexagonPhysicalMixedCalibrated.compareAfter := by
  unfold historicalToNativeCorrectionShift
  abel

/-- The additional transport correction is UNIQUE for each
source-original F47 frame if full shadow equality is required. -/
theorem historicalToNativeCorrectionShift_unique
    (B : C60F47SquareFrame α β r s)
    (δ : KuuNativeF55Shadow)
    (hδ : historicalF47AfterCoordinates B + δ =
      northHexagonPhysicalMixedCalibrated.compareAfter) :
    δ = historicalToNativeCorrectionShift B := by
  apply add_left_cancel (a := historicalF47AfterCoordinates B)
  exact hδ.trans (historicalToNativeCorrectionShift_sound B).symm

/-- Any such original/new transport needs a NONZERO extra
correction: the old and new chosen mixed bridge cannot be
identified even at the complete value level. -/
theorem historicalToNativeCorrectionShift_ne_zero
    (B : C60F47SquareFrame α β r s) :
    historicalToNativeCorrectionShift B ≠
      (0 : KuuNativeF55Shadow) := by
  intro hz
  have heq :
      northHexagonPhysicalMixedCalibrated.compareAfter =
        historicalF47AfterCoordinates B := by
    have hh : northHexagonPhysicalMixedCalibrated.compareAfter -
        historicalF47AfterCoordinates B = 0 := hz
    exact sub_eq_zero.mp hh
  exact historicalF47After_ne_nativeMixedCorrection B heq.symm

/-- More strongly: the uniquely forced transport changes the
integer square charge by MINUS ONE, rather than merely adjusting
an untyped phase tag. -/
theorem historicalToNativeCorrectionShift_charge
    (B : C60F47SquareFrame α β r s) :
    (historicalToNativeCorrectionShift B).1 =
      ((0 : Int), (-1 : Int)) := by
  change northHexagonPhysicalMixedCalibrated.compareAfter.1 -
      (historicalF47AfterCoordinates B).1 =
        ((0 : Int), (-1 : Int))
  rw [northHexagonPhysicalMixedCorrection_charge_zero,
    (historicalF47AfterCoordinates_components B).1]
  norm_num

/-- The independently required correction also contains a genuinely
NONZERO ZMod2 phase component: this is NOT a faithful identity
of the historical and native full-shadow observers. -/
theorem historicalToNativeCorrectionShift_phase_ne_zero
    (B : C60F47SquareFrame α β r s) :
    (historicalToNativeCorrectionShift B).2 ≠
      (0 : ZMod 2) := by
  change northHexagonPhysicalMixedCalibrated.compareAfter.2 -
      (historicalF47AfterCoordinates B).2 ≠ (0 : ZMod 2)
  rw [(historicalF47AfterCoordinates_components B).2]
  simpa only [sub_zero] using
    northHexagonPhysicalMixedCorrection_phase_ne_zero

#print axioms HistoricalF47TwoFaceNativeAtlas
#print axioms historicalF47TwoFaceNativeAtlas
#print axioms HistoricalF47TwoFaceNativeAtlas.firstEdge_onBoundary
#print axioms HistoricalF47TwoFaceNativeAtlas.secondEdge_onBoundary
#print axioms HistoricalF47TwoFaceNativeAtlas.faces_ne
#print axioms HistoricalF47TwoFaceNativeAtlas.oldDartEndpoints
#print axioms HistoricalF47TwoFaceNativeAtlas.firstSector_localized
#print axioms HistoricalF47TwoFaceNativeAtlas.secondSector_localized
#print axioms HistoricalF47TwoFaceNativeAtlas.firstDisk_kernel
#print axioms HistoricalF47TwoFaceNativeAtlas.secondDisk_kernel
#print axioms HistoricalF47TwoFaceNativeAtlas.original_square
#print axioms historicalF47AfterCoordinates_components
#print axioms historicalF47After_ne_nativeMixedCorrection
#print axioms historicalToNativeCorrectionShift_sound
#print axioms historicalToNativeCorrectionShift_unique
#print axioms historicalToNativeCorrectionShift_ne_zero
#print axioms historicalToNativeCorrectionShift_charge
#print axioms historicalToNativeCorrectionShift_phase_ne_zero

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
