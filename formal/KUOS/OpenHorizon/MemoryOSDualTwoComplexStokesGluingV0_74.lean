import Mathlib
import KUOS.OpenHorizon.MemoryOSTetrahedralBianchiCurvatureV0_73

namespace KUOS.OpenHorizon.MemoryOSDualTwoComplexStokesGluingV0_74

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSTetrahedralBianchiCurvatureV0_73

/--
Two tetrahedral memory cells glued across one shared primal face. The seam
transport is the dual 1-cell connecting the two primal 3-cells.
-/
structure GluedTetrahedra (G : Type*) [Group G] where
  left : TetrahedronConnection G
  right : TetrahedronConnection G
  seamTransport : G

/-- Product of the three outer faces of one oriented tetrahedral cell. -/
def cellOuterBoundary {G : Type*} [Group G]
    (connection : TetrahedronConnection G) : G :=
  face012 connection * face023 connection * face031 connection

/-- The fourth face, transported to the cell basepoint. -/
def cellSharedFace {G : Type*} [Group G]
    (connection : TetrahedronConnection G) : G :=
  transportFace123ToZero connection

theorem cell_outer_boundary_eq_shared_face {G : Type*} [Group G]
    (connection : TetrahedronConnection G) :
    cellOuterBoundary connection = cellSharedFace connection := by
  unfold cellOuterBoundary cellSharedFace
  exact tetrahedral_discrete_bianchi connection

/-- Right-cell outer boundary transported through the dual edge to the left basepoint. -/
def transportedRightOuter {G : Type*} [Group G]
    (pair : GluedTetrahedra G) : G :=
  pair.seamTransport * cellOuterBoundary pair.right * pair.seamTransport⁻¹

/-- Right shared face transported through the dual edge to the left basepoint. -/
def transportedRightShared {G : Type*} [Group G]
    (pair : GluedTetrahedra G) : G :=
  pair.seamTransport * cellSharedFace pair.right * pair.seamTransport⁻¹

/-- Opposite-orientation shared-face gluing condition. -/
def SharedFaceCompatible {G : Type*} [Group G]
    (pair : GluedTetrahedra G) : Prop :=
  transportedRightShared pair = (cellSharedFace pair.left)⁻¹

/-- Residual seam defect after the two shared faces are composed. -/
def seamGluingDefect {G : Type*} [Group G]
    (pair : GluedTetrahedra G) : G :=
  cellSharedFace pair.left * transportedRightShared pair

/-- Ordered outer boundary of the glued two-cell complex. -/
def gluedOuterBoundary {G : Type*} [Group G]
    (pair : GluedTetrahedra G) : G :=
  cellOuterBoundary pair.left * transportedRightOuter pair

/--
Cellwise Bianchi identities propagate the seam defect exactly to the outer
boundary of the glued complex.
-/
theorem glued_outer_boundary_eq_seam_defect {G : Type*} [Group G]
    (pair : GluedTetrahedra G) :
    gluedOuterBoundary pair = seamGluingDefect pair := by
  unfold gluedOuterBoundary seamGluingDefect transportedRightOuter
    transportedRightShared
  rw [cell_outer_boundary_eq_shared_face pair.left,
    cell_outer_boundary_eq_shared_face pair.right]

theorem seam_gluing_defect_identity_of_compatible {G : Type*} [Group G]
    (pair : GluedTetrahedra G) (h : SharedFaceCompatible pair) :
    seamGluingDefect pair = 1 := by
  unfold seamGluingDefect
  rw [h]
  simp

/-- Finite lattice Stokes closure after opposite-orientation seam cancellation. -/
theorem glued_lattice_stokes {G : Type*} [Group G]
    (pair : GluedTetrahedra G) (h : SharedFaceCompatible pair) :
    gluedOuterBoundary pair = 1 := by
  rw [glued_outer_boundary_eq_seam_defect]
  exact seam_gluing_defect_identity_of_compatible pair h

/-- Independent local gauge frames on the two cells. -/
structure GluedGaugeFrame (G : Type*) [Group G] where
  leftFrame : TetrahedronGaugeFrame G
  rightFrame : TetrahedronGaugeFrame G

/--
The dual-edge seam transforms by the left and right cell basepoint frames.
-/
def gaugeTransformGluedPair {G : Type*} [Group G]
    (pair : GluedTetrahedra G) (frame : GluedGaugeFrame G) :
    GluedTetrahedra G :=
  {
    left := gaugeTransform pair.left frame.leftFrame
    right := gaugeTransform pair.right frame.rightFrame
    seamTransport :=
      frame.leftFrame.g0⁻¹ * pair.seamTransport * frame.rightFrame.g0
  }

theorem cell_shared_face_gauge_covariant {G : Type*} [Group G]
    (connection : TetrahedronConnection G)
    (frame : TetrahedronGaugeFrame G) :
    cellSharedFace (gaugeTransform connection frame) =
      frame.g0⁻¹ * cellSharedFace connection * frame.g0 := by
  unfold cellSharedFace
  exact transported_face123_gauge_covariant connection frame

theorem transported_right_shared_gauge_covariant {G : Type*} [Group G]
    (pair : GluedTetrahedra G) (frame : GluedGaugeFrame G) :
    transportedRightShared (gaugeTransformGluedPair pair frame) =
      frame.leftFrame.g0⁻¹ * transportedRightShared pair *
        frame.leftFrame.g0 := by
  change
    (frame.leftFrame.g0⁻¹ * pair.seamTransport * frame.rightFrame.g0) *
        cellSharedFace (gaugeTransform pair.right frame.rightFrame) *
        (frame.leftFrame.g0⁻¹ * pair.seamTransport *
          frame.rightFrame.g0)⁻¹ =
      frame.leftFrame.g0⁻¹ *
        (pair.seamTransport * cellSharedFace pair.right *
          pair.seamTransport⁻¹) *
        frame.leftFrame.g0
  rw [cell_shared_face_gauge_covariant]
  group

theorem seam_gluing_defect_gauge_covariant {G : Type*} [Group G]
    (pair : GluedTetrahedra G) (frame : GluedGaugeFrame G) :
    seamGluingDefect (gaugeTransformGluedPair pair frame) =
      frame.leftFrame.g0⁻¹ * seamGluingDefect pair *
        frame.leftFrame.g0 := by
  change
    cellSharedFace (gaugeTransform pair.left frame.leftFrame) *
        transportedRightShared (gaugeTransformGluedPair pair frame) =
      frame.leftFrame.g0⁻¹ *
        (cellSharedFace pair.left * transportedRightShared pair) *
        frame.leftFrame.g0
  rw [cell_shared_face_gauge_covariant,
    transported_right_shared_gauge_covariant]
  group

theorem glued_outer_boundary_gauge_covariant {G : Type*} [Group G]
    (pair : GluedTetrahedra G) (frame : GluedGaugeFrame G) :
    gluedOuterBoundary (gaugeTransformGluedPair pair frame) =
      frame.leftFrame.g0⁻¹ * gluedOuterBoundary pair *
        frame.leftFrame.g0 := by
  rw [glued_outer_boundary_eq_seam_defect,
    glued_outer_boundary_eq_seam_defect,
    seam_gluing_defect_gauge_covariant]

/-- Class-function Wilson observable on the glued outer boundary. -/
def dualBoundaryWilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (pair : GluedTetrahedra G) : R :=
  χ.toFun (gluedOuterBoundary pair)

theorem dual_boundary_wilson_gauge_invariant {G : Type*} [Group G]
    {R : Type*} (χ : ClassFunction G R)
    (pair : GluedTetrahedra G) (frame : GluedGaugeFrame G) :
    dualBoundaryWilson χ (gaugeTransformGluedPair pair frame) =
      dualBoundaryWilson χ pair := by
  unfold dualBoundaryWilson
  rw [glued_outer_boundary_gauge_covariant]
  simpa using
    χ.conjugationInvariant frame.leftFrame.g0 (gluedOuterBoundary pair)

/-- Bounded class-function penalty for residual shared-face mismatch. -/
def dualComplexGluingPenalty {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale : ℚ)
    (pair : GluedTetrahedra G) : ℚ :=
  (maxValue - dualBoundaryWilson χ pair) / scale

theorem dual_complex_gluing_penalty_gauge_invariant {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale : ℚ)
    (pair : GluedTetrahedra G) (frame : GluedGaugeFrame G) :
    dualComplexGluingPenalty χ maxValue scale
        (gaugeTransformGluedPair pair frame) =
      dualComplexGluingPenalty χ maxValue scale pair := by
  unfold dualComplexGluingPenalty
  rw [dual_boundary_wilson_gauge_invariant]

/-- Confidence remains advisory and depends only on the gauge-invariant defect class. -/
def dualComplexAdjustedConfidence {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (pair : GluedTetrahedra G) : ℚ :=
  base - dualComplexGluingPenalty χ maxValue scale pair

theorem dual_complex_adjusted_confidence_gauge_invariant
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (pair : GluedTetrahedra G) (frame : GluedGaugeFrame G) :
    dualComplexAdjustedConfidence χ maxValue scale base
        (gaugeTransformGluedPair pair frame) =
      dualComplexAdjustedConfidence χ maxValue scale base pair := by
  unfold dualComplexAdjustedConfidence
  rw [dual_complex_gluing_penalty_gauge_invariant]

theorem dual_complex_adjusted_confidence_mem_unit_interval
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (pair : GluedTetrahedra G)
    (hbase0 : 0 ≤ base) (hbase1 : base ≤ 1)
    (hpenalty0 : 0 ≤ dualComplexGluingPenalty χ maxValue scale pair)
    (hpenalty :
      dualComplexGluingPenalty χ maxValue scale pair ≤ base) :
    dualComplexAdjustedConfidence χ maxValue scale base pair ∈
      Set.Icc (0 : ℚ) 1 := by
  unfold dualComplexAdjustedConfidence
  constructor <;> linarith

def compatibleCurvedPair : GluedTetrahedra S3 :=
  {
    left := curvedS3Tetrahedron
    right := curvedS3Tetrahedron
    seamTransport := swap01
  }

def mismatchedCurvedPair : GluedTetrahedra S3 :=
  {
    left := curvedS3Tetrahedron
    right := curvedS3Tetrahedron
    seamTransport := 1
  }

theorem canonical_compatible_shared_face :
    SharedFaceCompatible compatibleCurvedPair := by
  native_decide

theorem canonical_compatible_lattice_stokes :
    gluedOuterBoundary compatibleCurvedPair = 1 := by
  exact glued_lattice_stokes compatibleCurvedPair
    canonical_compatible_shared_face

theorem canonical_mismatched_seam_defect :
    seamGluingDefect mismatchedCurvedPair = swap12 * swap01 := by
  native_decide

theorem canonical_mismatched_outer_boundary :
    gluedOuterBoundary mismatchedCurvedPair = swap12 * swap01 := by
  native_decide

theorem canonical_compatible_boundary_wilson :
    dualBoundaryWilson (identityWilsonClass S3) compatibleCurvedPair = 3 := by
  native_decide

theorem canonical_mismatched_boundary_wilson :
    dualBoundaryWilson (identityWilsonClass S3) mismatchedCurvedPair = 0 := by
  native_decide

theorem canonical_compatible_gluing_penalty :
    dualComplexGluingPenalty (identityWilsonClass S3) 3 18
      compatibleCurvedPair = 0 := by
  native_decide

theorem canonical_mismatched_gluing_penalty :
    dualComplexGluingPenalty (identityWilsonClass S3) 3 18
      mismatchedCurvedPair = 1 / 6 := by
  native_decide

theorem canonical_compatible_adjusted_confidence :
    dualComplexAdjustedConfidence (identityWilsonClass S3) 3 18 (1 / 3)
      compatibleCurvedPair = 1 / 3 := by
  native_decide

theorem canonical_mismatched_adjusted_confidence :
    dualComplexAdjustedConfidence (identityWilsonClass S3) 3 18 (1 / 3)
      mismatchedCurvedPair = 1 / 6 := by
  native_decide

structure DualTwoComplexStokesCertificate where
  sourceMemoryOSV073Bound : Bool
  dualTwoComplexExact : Bool
  oppositeOrientationGluingExact : Bool
  latticeStokesCompositionExact : Bool
  bianchiDefectPropagationExact : Bool
  boundaryWilsonGaugeInvariant : Bool
  continuumDualComplexClaimed : Bool
  physicalNonAbelianStokesActionClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSDualTwoComplexStokesGluingV0_74
