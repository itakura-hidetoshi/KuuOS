import Kuu.F112.PolygonSource
import Kuu.F112.PolygonNativeFourBoundaryChargeForgetNonfaithful

/-!
# F112-P31 — physical C60 F42 face source and native F55 typed bridge packet

This is a genuinely source-bearing comparison packet on the ACTUAL top
hexagon of the truncated icosahedron. Its first part is the authentic
Type-valued physical six-sector fan and disk, with original 90-edge
incidence and two original endpoint darts. Its second part is the
independent Type-valued F54/F55 disjoint-rotation 3-cell already
proved in P29/P30, with four strictly tagged receiver boundaries.

A frame keeps BOTH source presentations. The native raw F55 generator
must be exactly the six-sector C60 square; it cannot be invented from
a charge or from a coincidental evaluated equality.

For every real boundary sector we prove actual dart -> edge -> face
globularity, its raw/localized F69 face rewrite, the complete disk
boundary equality, and preservation of distinct raw native two-step
and diagonal blocks. Its four-boundary higher square commutes IFF an
explicit full charge/phase calibration certificate is supplied.

The canonical frame is calibrated. A second frame has the SAME
complete physical fan/disk and the SAME original F55 raw 3-cell but
zero higher calibration and a NONCOMMUTATIVE square. Therefore
calibration does NOT descend from the common Type-valued physical
and raw source evidence alone.

This is NOT a comparison or equivalence to frozen historical F47
physical face and original F55 3-Hom. The missing type-faithful
historical source functor/Beck-Chevalley transport remains an honest
obligation. No imported KUOS.*, Gray, additional axioms or sorry.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- A typed physical-face/F55 comparison source on the ACTUAL
six-sided C60 hexagon. The first field retains all six Type-valued
physical F42 fan witnesses AND the entire physical disk. The higher
field retains its native F54 routes, raw F55 3-cell, and full chosen
even/odd target values; the final certificate pins the same real C60
raw square, not a numerical-grade proxy. -/
structure NativeHexagonPhysicalF47Frame where
  physical : PolygonSourcePresentation (.hexagon (.top 0))
  higher : NativeHexagonFourBoundaryData
  exactRaw :
    higher.raw = northHexagonNativeF55SquareCell

/-- A separate full-shadow calibration is an obligation, not an
automatic consequence of having a real polygon, its F42 face or a
correctly typed native F55 source 3-cell. -/
def NativeHexagonPhysicalF47Frame.Calibrated
    (F : NativeHexagonPhysicalF47Frame) : Prop :=
  F.higher.Calibrated

/-- The REAL hexagon north-side physical fan and full source disk,
paired with the genuinely constructed independent raw F55 square
and its explicitly calibrated even/odd higher receiver comparison. -/
def northHexagonPhysicalF47Frame : NativeHexagonPhysicalF47Frame where
  physical := canonicalPolygonSource (.hexagon (.top 0))
  higher := northHexagonFourData
  exactRaw := rfl

/-- The SAME physically valid face fan/disk and SAME native raw
F55 source, now considered with an uncorrected higher comparison. -/
def northHexagonPhysicalF47ZeroFrame :
    NativeHexagonPhysicalF47Frame where
  physical := canonicalPolygonSource (.hexagon (.top 0))
  higher := northHexagonFourZeroData
  exactRaw := rfl

/-- Each of the six actual C60 boundary sectors retains its
independent native F45 source leaf (not a Bool-labelled surrogate).
The same sector can be read from that leaf without losing its site. -/
theorem northHexagonNativeUnit_exact_physical_sector
    (i : Fin 6) :
    (northHexagonNativeUnit i).sectors = [northHexagonNativeSector i] := rfl

/-- A genuine six-leaf C60 native F45 tree. These six physical leaf
labels are EXACTLY the ones that occur in the independently
constructed disjoint F54 associator generators of the F55 raw
hexagon square, including the original order 0,...,5. -/
def northHexagonSixPhysicalUnitTree :=
  KuuNativeF45Tree.node
    (KuuNativeF45Tree.node
      (KuuNativeF45Tree.node
        (northHexagonNativeUnit 0) (northHexagonNativeUnit 1))
      (northHexagonNativeUnit 2))
    (KuuNativeF45Tree.node
      (KuuNativeF45Tree.node
        (northHexagonNativeUnit 3) (northHexagonNativeUnit 4))
      (northHexagonNativeUnit 5))

theorem northHexagonSixPhysicalUnitTree_sectors :
    northHexagonSixPhysicalUnitTree.sectors =
      [northHexagonNativeSector 0, northHexagonNativeSector 1,
       northHexagonNativeSector 2, northHexagonNativeSector 3,
       northHexagonNativeSector 4, northHexagonNativeSector 5] := rfl

/-- For EVERY one of six actual hexagon sides the original C60
dart-to-edge-to-face incidence legs and both end darts are
simultaneously present. The middle site is one of the TRUE 90 edges,
not a direct invented vertex-to-vertex morphism. -/
theorem northHexagonPhysical_original_flag (i : Fin 6) :
    Site.vertex
        (cyclicBoundaryDart (.hexagon (.top 0)) i.val) ≤
      Site.edge (cyclicBoundaryEdge (.hexagon (.top 0)) i.val) ∧
    Site.edge (cyclicBoundaryEdge (.hexagon (.top 0)) i.val) ≤
      Site.face (.hexagon (.top 0)) ∧
    Site.vertex
        (cyclicBoundaryDart (.hexagon (.top 0)) (i.val + 1)) ≤
      Site.edge (cyclicBoundaryEdge (.hexagon (.top 0)) i.val) := by
  have h := cyclicBoundarySide_real
    (.hexagon (.top 0)) i (northHexagonNativeSector i).2
  exact ⟨edgeJoins_start _ _ _ h.1, h.2.1,
    edgeJoins_finish _ _ _ h.1⟩

/-- The intermediate original physical edge is truly ON the exact
hexagonal face boundary selected by the F55 raw source. -/
theorem northHexagonPhysical_original_side_member (i : Fin 6) :
    cyclicBoundaryEdge (.hexagon (.top 0)) i.val ∈
      polygonBoundaryEdges (.hexagon (.top 0)) :=
  (cyclicBoundarySide_real (.hexagon (.top 0)) i
    (northHexagonNativeSector i).2).2.2

/-- The physical first side is the genuine original north-spoke
cross-dart edge, not a manufactured F47 bridge generator. -/
theorem northHexagonPhysical_first_edge :
    cyclicBoundaryEdge (.hexagon (.top 0)) 0 =
      Edge.cross (.northSpoke 0) := rfl

/-- A genuinely Type-valued primitive physical F42 face source
from the stored polygon atlas at ANY of the six original sides. -/
def NativeHexagonPhysicalF47Frame.physicalSide
    (F : NativeHexagonPhysicalF47Frame) (i : Fin 6) :
    PolygonFanRewrite
      (polygonRawSide (.hexagon (.top 0)) i
        (northHexagonNativeSector i).2)
      (polygonConeRawSide (.hexagon (.top 0)) i
        (northHexagonNativeSector i).2) :=
  F.physical.sector i (northHexagonNativeSector i).2

/-- Every physical face source primitive is sound in the ACTUAL
F69 localization, independently of even/odd receiver calibration. -/
theorem NativeHexagonPhysicalF47Frame.physicalSide_localized
    (F : NativeHexagonPhysicalF47Frame) (i : Fin 6) :
    zigzagToLocalization
        (polygonRawSide (.hexagon (.top 0)) i
          (northHexagonNativeSector i).2) =
      zigzagToLocalization
        (polygonConeRawSide (.hexagon (.top 0)) i
          (northHexagonNativeSector i).2) :=
  (F.physicalSide i).localized_sound

/-- This equality also descends to the precisely specified
original C60 zigzag-localization kernel, but no raw proofs are
identified or silently erased beforehand. -/
theorem NativeHexagonPhysicalF47Frame.physicalSide_kernel
    (F : NativeHexagonPhysicalF47Frame) (i : Fin 6) :
    zigzagKernelQ.map
        (polygonRawSide (.hexagon (.top 0)) i
          (northHexagonNativeSector i).2) =
      zigzagKernelQ.map
        (polygonConeRawSide (.hexagon (.top 0)) i
          (northHexagonNativeSector i).2) :=
  (F.physicalSide i).kernel_sound

/-- The whole REAL six-sided physical face loop is certified by
a Type-valued disk witness from the SAME stored physical source. -/
theorem NativeHexagonPhysicalF47Frame.physicalDisk_kernel
    (F : NativeHexagonPhysicalF47Frame) :
    zigzagKernelQ.map (polygonRawLoop (.hexagon (.top 0))) =
      zigzagKernelQ.map
        (Zigzag.nil
          (Site.vertex (cyclicBoundaryDart (.hexagon (.top 0)) 0))) :=
  F.physical.disk.kernel_sound

/-- The two native polygon-sector paths have literally different
original free length (two original incidences versus their actual
diagonal) yet evaluate to the SAME real site morphism. This property
holds for every one of the physical source's six sectors. -/
theorem northHexagonPhysical_twoLeg_and_diagonal (i : Fin 6) :
    polygonSectorNativeTwoStep (.hexagon (.top 0))
        (northHexagonNativeSector i) ≠
      polygonSectorNativeDiagonal (.hexagon (.top 0))
        (northHexagonNativeSector i) ∧
    (polygonSectorNativeTwoStep (.hexagon (.top 0))
        (northHexagonNativeSector i)).composite =
      (polygonSectorNativeDiagonal (.hexagon (.top 0))
        (northHexagonNativeSector i)).composite :=
  ⟨polygonSectorTwoStep_ne_diagonal _ _, polygonSectorNative_composite_eq _ _⟩

/-- The original two-block physical path and one-block diagonal
are also NOT identified as raw F40 histories. -/
theorem northHexagonPhysical_twoBlocks_ne_one (i : Fin 6) :
    polygonSectorTwoBlocks (.hexagon (.top 0))
        (northHexagonNativeSector i) ≠
      polygonSectorOneBlock (.hexagon (.top 0))
        (northHexagonNativeSector i) :=
  polygonSectorTwoBlocks_ne_oneBlock _ _

/-- The F55 side of every frame remains EXACTLY the correctly
typed C60 six-sector proof witness and the two genuinely different
F54 source routes; no phase number creates a nonexistent 3-cell. -/
theorem NativeHexagonPhysicalF47Frame.exact_native_raw
    (F : NativeHexagonPhysicalF47Frame) :
    F.higher.raw =
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell.disjointSquare
        northHexagonNativeLeftRotation northHexagonNativeRightRotation := by
  simpa only [northHexagonNativeF55SquareCell] using F.exactRaw

/-- The same frame also retains the full source's genuinely
different left-first and right-first native F54 paths. -/
theorem NativeHexagonPhysicalF47Frame.native_routes_distinct
    (_F : NativeHexagonPhysicalF47Frame) :
    northHexagonNativeSquareLeft ≠ northHexagonNativeSquareRight :=
  northHexagonNativeSquare_ne

/-- The joint **physical AND higher** compatibility condition
separates two different sorts of proofs: ALL six independent
physical F42 face incidences are automatically kernel-sound, but
the higher four-boundary square commutes EXACTLY when the separately
supplied full target calibration matches. -/
theorem NativeHexagonPhysicalF47Frame.joint_descent_iff_calibrated
    (F : NativeHexagonPhysicalF47Frame) :
    ((∀ i : Fin 6,
      zigzagKernelQ.map
          (polygonRawSide (.hexagon (.top 0)) i
            (northHexagonNativeSector i).2) =
        zigzagKernelQ.map
          (polygonConeRawSide (.hexagon (.top 0)) i
            (northHexagonNativeSector i).2)) ∧
      (nativeHexagonFourEvenArrow F.higher ≫
          nativeHexagonFourCompareAfter F.higher =
        nativeHexagonFourCompareBefore F.higher ≫
          nativeHexagonFourOddArrow F.higher)) ↔
      F.Calibrated := by
  constructor
  · exact fun h => (nativeHexagonFourSquare_iff_calibrated F.higher).1 h.2
  · intro h
    exact ⟨F.physicalSide_kernel,
      (nativeHexagonFourSquare_iff_calibrated F.higher).2 h⟩

/-- The true C60 top hexagon has a separate calibrated comparison
packet with both physically sound fan/disk and native 3-witness. -/
theorem northHexagonPhysicalF47Frame_calibrated :
    northHexagonPhysicalF47Frame.Calibrated :=
  northHexagonFourData_calibrated

/-- The exact SAME original physical F42 face data and SAME native
raw F55 square admit another valid frame with ZERO correction. -/
theorem northHexagonPhysicalF47Frame_same_sources :
    northHexagonPhysicalF47Frame.physical =
      northHexagonPhysicalF47ZeroFrame.physical ∧
    northHexagonPhysicalF47Frame.higher.raw =
      northHexagonPhysicalF47ZeroFrame.higher.raw := by
  exact ⟨rfl, rfl⟩

/-- The zero-calibration packet still retains all six real C60 F42
physical proof terms and the same typed F55 source but FAILS the
independently required four-boundary coherence obligation. -/
theorem northHexagonPhysicalF47ZeroFrame_not_calibrated :
    ¬ northHexagonPhysicalF47ZeroFrame.Calibrated := by
  intro h
  exact northHexagonFourZeroSquare_not_commutative
    ((nativeHexagonFourSquare_iff_calibrated
      northHexagonFourZeroData).2 h)

/-- The exact Type-valued physical F42 fan/disk plus full typed RAW
F55 source proof is retained together, as an explicit observation
that does not erase any of these source proof objects. -/
def NativeHexagonPhysicalF47Frame.sourceObservation
    (F : NativeHexagonPhysicalF47Frame) :=
  (F.physical, F.higher.raw)

/-- Physical and raw evidence are IDENTICAL for the two actual
C60 comparison frames, before any physical-path localization or
shadow quotient. The calibration choice remains separate data. -/
theorem northHexagonPhysicalF47_sourceObservation_eq :
    northHexagonPhysicalF47Frame.sourceObservation =
      northHexagonPhysicalF47ZeroFrame.sourceObservation := rfl

/-- The rigorous F47-style calibration obstruction: there exists
NO predicate on even the FULL Type-valued physical six-sector
fan/disk AND raw F55 proof evidence that can decide whether EVERY
receiver-relative four-boundary frame is calibrated. The two
constructed packets share that source observation and disagree in
the higher square. This does not assert a global historical F47
descent or original F68/F77 curvature identification. -/
theorem northHexagonPhysicalF47_calibration_no_source_descent :
    ¬ ∃ Q :
        (PolygonSourcePresentation (.hexagon (.top 0)) ×
          KuuNativeF45Tree.DepthRotationRoute.PresentedCell
            (.hexagon (.top 0))
            northHexagonNativeSquareLeft northHexagonNativeSquareRight) → Prop,
        ∀ F : NativeHexagonPhysicalF47Frame,
          (Q F.sourceObservation ↔ F.Calibrated) := by
  rintro ⟨Q, hQ⟩
  have hyes :
      Q northHexagonPhysicalF47Frame.sourceObservation :=
    (hQ northHexagonPhysicalF47Frame).2
      northHexagonPhysicalF47Frame_calibrated
  have hzero :
      Q northHexagonPhysicalF47ZeroFrame.sourceObservation := by
    rw [← northHexagonPhysicalF47_sourceObservation_eq]
    exact hyes
  exact northHexagonPhysicalF47ZeroFrame_not_calibrated
    ((hQ northHexagonPhysicalF47ZeroFrame).1 hzero)

#print axioms NativeHexagonPhysicalF47Frame
#print axioms northHexagonNativeUnit_exact_physical_sector
#print axioms northHexagonSixPhysicalUnitTree_sectors
#print axioms northHexagonPhysical_original_flag
#print axioms northHexagonPhysical_original_side_member
#print axioms NativeHexagonPhysicalF47Frame.physicalSide
#print axioms NativeHexagonPhysicalF47Frame.physicalSide_localized
#print axioms NativeHexagonPhysicalF47Frame.physicalSide_kernel
#print axioms NativeHexagonPhysicalF47Frame.physicalDisk_kernel
#print axioms northHexagonPhysical_twoLeg_and_diagonal
#print axioms northHexagonPhysical_twoBlocks_ne_one
#print axioms NativeHexagonPhysicalF47Frame.exact_native_raw
#print axioms NativeHexagonPhysicalF47Frame.native_routes_distinct
#print axioms NativeHexagonPhysicalF47Frame.joint_descent_iff_calibrated
#print axioms northHexagonPhysicalF47Frame_calibrated
#print axioms northHexagonPhysicalF47Frame_same_sources
#print axioms northHexagonPhysicalF47ZeroFrame_not_calibrated
#print axioms northHexagonPhysicalF47_sourceObservation_eq
#print axioms northHexagonPhysicalF47_calibration_no_source_descent

end
end Kuu.F112.Physical
