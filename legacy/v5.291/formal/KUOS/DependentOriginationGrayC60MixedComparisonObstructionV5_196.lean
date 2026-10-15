import KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
import KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167
import KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174

namespace KUOS.DependentOriginationGrayC60MixedComparisonObstructionV5_196

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F48 / v5.196 — two-face target transport vs. original C60 obstruction

From an ACTUAL all-90-edge original C60/F55 mixed SOURCE frame
construct a genuine edge-indexed field of full native Gray
3-cells: C60 face interchanger, NEW typed comparison 3-cell,
and ORIGINAL F55 source rotation-square arrow.

Prove their EXACT pointwise calibration on both physically
incident original surface faces. The two face choices transport
consistently in the FULL Gray target. This does not identify
different F42 source face-boundary paths or produce a global
higher source functor.

Crucially, local calibration does NOT imply physical flatness:
the original F55 signed north-pentagon curvature remains nonzero.
The independent calibration field Δ=(0,1;0) ITSELF has exact
oriented north-pentagon second integer charge -5, phase ZERO.
Its total signed 32-face curvature still vanishes, making
the distinction between global H² cancellation and local
vertex-gauge H¹ descent explicit. No obstacle is erased by
falsely equating unrelated C60/F55 source 2-cells.
-/

/-- The native value of a genuinely typed ORIGINAL C60 face
interchanger, separately attached on each of the true 90
edges and at either of its two original adjacent faces. -/
def c60F48FaceInterchangerField (side : Bool) :
    TruncatedIcosahedralEdge → GradedThreeCell 0 0 :=
  fun edge => (c60F48AdjacentFaceInterchanger edge side).toNative

theorem c60F48FaceInterchangerField_independentOfSide
    (edge : TruncatedIcosahedralEdge) :
    c60F48FaceInterchangerField false edge =
      c60F48FaceInterchangerField true edge :=
  c60F48TwoFaceInterchangers_sameTarget edge

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section MixedField
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

/-- Field of NEW MIXED comparison arrows, mapped from the
F47 full four-boundary Mathlib source category and retaining
the full original Int×Int and ZMod2 target information. -/
def c60F48MixedComparisonField (side : Bool) :
    TruncatedIcosahedralEdge → GradedThreeCell 0 0 :=
  fun edge =>
    (c60F47MixedGrayFunctor
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)).map
        (c60F47CompareAfter
          (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side))

/-- TRUE original F55 rotation-square 3-arrow from the
physically selected F47 source frame, NOT a new arbitrary
target generator masquerading as an original source arrow. -/
def c60F48OriginalRotationField (side : Bool) :
    TruncatedIcosahedralEdge → GradedThreeCell 0 0 :=
  fun edge =>
    c60F44OriginalF55Eval
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side).rotationStep

/-- Both true adjacent-face choices induce exactly the same
native receiver Δ, with its two integer charges and phase
UNCHANGED. This is target-level face-choice transport. -/
theorem c60F48MixedComparisonField_isCalibration
    (side : Bool) :
    c60F48MixedComparisonField t₁ t₂ left right side =
      fun _ => c60F46FaceF55ComparisonCalibration := by
  funext edge
  exact c60F48EveryRealEdgeComparison_fullNative
    t₁ t₂ left right edge side

theorem c60F48MixedComparisonField_twoFaces_sameTarget :
    c60F48MixedComparisonField t₁ t₂ left right false =
      c60F48MixedComparisonField t₁ t₂ left right true := by
  rw [c60F48MixedComparisonField_isCalibration,
    c60F48MixedComparisonField_isCalibration]

/-- The truly typed F55 original source values at every real
edge match the original genuine ninety-edge field from F46. -/
theorem c60F48OriginalRotationField_isAuthentic
    (side : Bool) :
    c60F48OriginalRotationField t₁ t₂ left right side =
      fun edge =>
        c60F46AllNinetyAuthenticSourceFlagField
          t₁ t₂ left right (.edge edge) := by
  funext edge
  change c60F44OriginalF55GrayFunctor.map
      (c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right edge) =
    c60F46AllNinetyAuthenticSourceFlagField
      t₁ t₂ left right (.edge edge)
  rw [c60F46PhysicalFlagOriginalF55Arrow_fullNative,
    c60F46AllNinetyAuthenticSourceFlagField_edge]

/-- Both face-choice presentations of ALL physical source
rotation 3-arrows have EXACTLY the original F55 square native
labels. No chosen source face boundary is erased or equated. -/
theorem c60F48OriginalRotationField_uniformF55
    (side : Bool) :
    c60F48OriginalRotationField t₁ t₂ left right side =
      c60F19UniformF55EdgeLabels := by
  funext edge
  change c60F44OriginalF55GrayFunctor.map
      (c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right edge) =
    originalF55BraidedSquareGenerator
  rw [c60F46PhysicalFlagOriginalF55Arrow_fullNative,
    c60AllNinetyGrayCell_eq]

/-- EXACT pointwise mixed calibration in the full original
native Gray target at each of the 90 actual C60 physical
edges, simultaneously for either adjacent original face. -/
theorem c60F48MixedField_sitewiseCalibration
    (side : Bool) (edge : TruncatedIcosahedralEdge) :
    c60F48FaceInterchangerField side edge +
      c60F48MixedComparisonField t₁ t₂ left right side edge =
        c60F48OriginalRotationField t₁ t₂ left right side edge := by
  change c60F44FaceThreeEval
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side).faceStep +
    c60F46FaceF55ComparisonCalibration =
      c60F44OriginalF55Eval
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side).rotationStep
  exact (c60F48EveryRealEdgeMixedFrame
    t₁ t₂ left right edge side).calibrated

/-- The target comparisons do glue between the two incident
face choices, although a source-level 2-cell transport between
the distinct ORIGINAL polygonal paths is not yet provided. -/
theorem c60F48BothSides_fullNativeTransport
    (edge : TruncatedIcosahedralEdge) :
    c60F48FaceInterchangerField false edge +
      c60F48MixedComparisonField t₁ t₂ left right false edge =
    c60F48FaceInterchangerField true edge +
      c60F48MixedComparisonField t₁ t₂ left right true edge := by
  rw [c60F48FaceInterchangerField_independentOfSide,
    c60F48MixedComparisonField_twoFaces_sameTarget]

/-- A calibration field can glue over every real geometric
edge and STILL fail to be a flat original C60 vertex gauge.
The original source-interpreted F55 field remains NONFLAT on
the actual north pentagon, with its full integer charge. -/
theorem c60F48MixedOriginalF55_northNonflat
    (side : Bool) :
    c60WangBiSignedGrayFace
      (c60F48OriginalRotationField t₁ t₂ left right side)
      (.aroundVertex .north) ≠ 0 := by
  rw [c60F48OriginalRotationField_uniformF55]
  exact c60WangBiOriginalF55NorthFace_nonflat

/-- The correct original 90-edge field therefore CANNOT be
an exact vertex gauge, despite the valid two-sided mixed
comparison squares. This is a genuine obstruction to descent. -/
theorem c60F48MixedOriginalF55_noVertexGauge
    (side : Bool) :
    ¬ ∃ φ : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F18GrayEdgeCochain
        (c60F48OriginalRotationField t₁ t₂ left right side) =
          φ.comp c60IntegralBoundaryOne := by
  rw [c60F48OriginalRotationField_uniformF55]
  exact c60F19OriginalF55EdgeCochain_no_vertexGauge

/-- EXACT signed curvature of the NEW mixed comparison Δ
field. The actual oriented C60 integer incidence cycle,
rather than any synthetic square face, determines the
integer coefficient on each 5- or 6-sided physical face. -/
theorem c60F48ComparisonField_signedCurvature
    (side : Bool) (face : TruncatedIcosahedralSeedFace) :
    c60WangBiSignedGrayFace
      (c60F48MixedComparisonField t₁ t₂ left right side) face =
        c60F19SignedBoundaryDegree face •
          c60F46FaceF55ComparisonCalibration := by
  rw [c60F48MixedComparisonField_isCalibration]
  exact c60F19SignedScalarList_sum
    (c60IntegerOrientedFaceBoundary face)
    c60F46FaceF55ComparisonCalibration

/-- A pure (0,1;0) integer mixed comparison field has signed
second integer charge n after n real oriented boundary steps. -/
theorem c60F48CalibrationZsmul_secondCharge (n : ℤ) :
    (n • c60F46FaceF55ComparisonCalibration).charge.2 = n := by
  calc
    (n • c60F46FaceF55ComparisonCalibration).charge.2 =
        (n • c60F46FaceF55ComparisonCalibration.charge).2 := by
          exact congrArg Prod.snd
            (grayNeutralChargeHom.map_zsmul
              c60F46FaceF55ComparisonCalibration n)
    _ = n := by
      rw [c60F46FaceF55ComparisonCalibration_components.1]
      simp

/-- Crucial original C60 obstruction: even though Δ's
independent Gray exchange PHASE is zero, its native second
integer charge around the ACTUAL north pentagon is -5.
It cannot be erased by a phase-only comparison. -/
theorem c60F48MixedCalibration_northSecondCharge
    (side : Bool) :
    (c60WangBiSignedGrayFace
      (c60F48MixedComparisonField t₁ t₂ left right side)
      (.aroundVertex .north)).charge.2 = (-5 : ℤ) := by
  rw [c60F48ComparisonField_signedCurvature,
    c60F19SignedBoundaryDegree_complete]
  exact c60F48CalibrationZsmul_secondCharge (-5)

/-- The same genuine original north face has ZERO exchange
phase for the mixed calibration, despite NONZERO integer
square charge. The two independent Gray coordinates must
never be conflated. -/
theorem c60F48MixedCalibration_northPhaseZero
    (side : Bool) :
    (c60WangBiSignedGrayFace
      (c60F48MixedComparisonField t₁ t₂ left right side)
      (.aroundVertex .north)).phase = (0 : ZMod 2) := by
  rw [c60F48ComparisonField_signedCurvature]
  calc
    (c60F19SignedBoundaryDegree (.aroundVertex .north) •
      c60F46FaceF55ComparisonCalibration).phase =
      c60F19SignedBoundaryDegree (.aroundVertex .north) •
        c60F46FaceF55ComparisonCalibration.phase :=
      grayNeutralPhaseHom.map_zsmul
        c60F46FaceF55ComparisonCalibration _
    _ = 0 := by
      rw [c60F46FaceF55ComparisonCalibration_components.2]
      simp

theorem c60F48MixedCalibration_northNonflat
    (side : Bool) :
    c60WangBiSignedGrayFace
      (c60F48MixedComparisonField t₁ t₂ left right side)
      (.aroundVertex .north) ≠ 0 := by
  intro h
  have hh :
      (c60WangBiSignedGrayFace
        (c60F48MixedComparisonField t₁ t₂ left right side)
        (.aroundVertex .north)).charge.2 = (0 : ℤ) :=
    congrArg (fun g : GradedThreeCell 0 0 => g.charge.2) h
  rw [c60F48MixedCalibration_northSecondCharge] at hh
  norm_num at hh

/-- Signed total curvature vanishes on all 32 original
C60 polygonal faces even for this nonflat local receiver.
Global H² cancellation does not entail local H¹ descent. -/
theorem c60F48MixedCalibration_globalSurfaceZero
    (side : Bool) :
    c60WangBiSignedGraySurface
      (c60F48MixedComparisonField t₁ t₂ left right side) = 0 :=
  c60WangBiSignedGraySurface_zero _

#print axioms c60F48MixedComparisonField_isCalibration
#print axioms c60F48MixedComparisonField_twoFaces_sameTarget
#print axioms c60F48OriginalRotationField_uniformF55
#print axioms c60F48MixedField_sitewiseCalibration
#print axioms c60F48BothSides_fullNativeTransport
#print axioms c60F48MixedOriginalF55_northNonflat
#print axioms c60F48MixedOriginalF55_noVertexGauge
#print axioms c60F48ComparisonField_signedCurvature
#print axioms c60F48MixedCalibration_northSecondCharge
#print axioms c60F48MixedCalibration_northPhaseZero
#print axioms c60F48MixedCalibration_northNonflat
#print axioms c60F48MixedCalibration_globalSurfaceZero

end MixedField

end
end KUOS.DependentOriginationGrayC60MixedComparisonObstructionV5_196
