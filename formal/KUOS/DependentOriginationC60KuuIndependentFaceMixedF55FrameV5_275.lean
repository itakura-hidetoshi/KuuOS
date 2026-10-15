import KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
import KUOS.DependentOriginationGrayC60OriginalF43F55MixedBridgeV5_203

namespace KUOS.DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalF43F55MixedBridgeV5_203
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuPhaseReconstructionObstructionV5_269
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.275 / F112 third stage — an ACTUAL independent-face F42/F54/F55 mixed source square

F112/v5.274 constructs independent ORIGINAL F42 face cells at the
two genuine distinct polygonal C60 face sites of a real edge, and
a correctly path-typed ORIGINAL F51 exchange (charge (0,0),
independent Gray phase 1) from those chosen cells. The F77 quotient
collapses this phase but does not change the original source cells.

Now construct the strictly STRONGER source-level F47 comparison:
  * lift those SAME independently chosen F42 cells and genuine C60
    connecting paths to an ORIGINAL F43 raw typed interchanger,
    and hence a genuine F44 categorical 3-Hom between the actual
    independently constructed F42 horizontal pasting endpoints;
  * combine this old original FACE 3-Hom with the independently
    typed original F54 rotation routes and actual original F55
    physical flag-square 3-Hom as an ACTUAL C60F47SquareFrame.
  * prove its source-level four-boundary square COMMUTES in the
    mixed F47 categorical quotient; calibration is a PROVED
    complete native (Int×Int, ZMod 2) equality, not a hypothesis.
  * classify the UNIQUE target receiver and prove that NO original
    nine-constructor F55 raw cell on the exact original rotation
    boundary routes can implement it. The added mixed F47
    comparison generator is mathematically indispensable.
  * connect this non-lift with the real F112 F77-observed finite
    refinements, independent original phase and signed curvature.

This is a concrete original-boundary-preserving LOCAL mixed F47
source square for ANY two source face cells with their original
C60 physical-loop boundaries and odd degrees, including all
90 original physical edges. It is NOT an identification of F42
and F54 boundary types, not a new ORIGINAL F55 constructor, and
not effective global original F42/F54/F55 three-descent.
-/

/-- The same independent original two-polygon source F42
comparison as v5.274, but in the ACTUAL original F43 raw
grammar, before adjoining any F51 horizontal generators.
Both distinct face bases are connected by a TRUE C60 path. -/
def c60F112IndependentFaceOriginalF43
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    C60F43PresentedThreeCell
      (c60F112IndependentPairLeft C i P)
      (c60F112IndependentPairRight C i P) :=
  .whiskerRight
    (.whiskerLeft (C.prior i)
      (.interchange P.first (c60F112SecondFaceBridged C i P)))
    (C.suffix i)

/-- Source F43's full native image is the genuine original
odd/odd physical exchange, for EVERY odd face-site pair,
not only the canonical original face generators. -/
theorem c60F112IndependentFaceOriginalF43_native
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    (c60F112IndependentFaceOriginalF43 C i P).toNative =
      c60F43NorthPentagonInterchange.toNative := by
  apply GradedThreeCell.ext
  · rfl
  · change
      c60F43FaceDegree P.first * c60F43FaceDegree P.second =
        (1 : ZMod 2)
    rw [P.first_odd, P.second_odd]
    simp

/-- Source-extension compatibility: the F43 original categorical
arrow and the v5.274 independently typed F51 categorical arrow
have exactly the SAME full native image, without identifying
their different source presentations or their raw proof terms. -/
theorem c60F112IndependentF43_F51_native
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    c60F44FaceThreeEval
        (c60F44FaceThreeOf
          (c60F112IndependentFaceOriginalF43 C i P)) =
      c60F51Eval (c60F112IndependentPairExchangeHom C i P) := by
  rfl

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section ActualIndependentMixedSource
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

/-- CONSTRUCTED (not postulated) original mixed F47 source
four-boundary frame: original F42 independent source face
pasting endpoints + the separately typed ORIGINAL F54 rotation
route boundaries. Actual old original F43 AND F55 3-arrows
supply the two sides, and full native calibration is PROVED. -/
def c60F112IndependentFaceOriginalMixedFrame
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    C60F47SquareFrame
      (c60F112IndependentPairLeft C i P)
      (c60F112IndependentPairRight C i P)
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right) where
  edge := C.edge i
  faceStep := c60F44FaceThreeOf
    (c60F112IndependentFaceOriginalF43 C i P)
  rotationStep :=
    c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right (C.edge i)
  calibrated := by
    change
      (c60F112IndependentFaceOriginalF43 C i P).toNative +
        c60F46FaceF55ComparisonCalibration =
      c60F44OriginalF55GrayFunctor.map
        (c60F46PhysicalFlagOriginalF55Arrow
          t₁ t₂ left right (C.edge i))
    rw [c60F112IndependentFaceOriginalF43_native,
      c60F46PhysicalFlagOriginalF55Arrow_fullNative,
      c60AllNinetyGrayCell_eq]
    exact c60F46NativeNorthFaceF55_calibrated

/-- This original F47 mixed source frame is genuinely LOCALIZED
on the physical edge of both originally distinct C60 face sites. -/
theorem c60F112IndependentFaceMixedFrame_edge
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P).edge =
      C.edge i := rfl

/-- Its actual F47 ORIGINAL F43 source edge literally evaluates
to the independently chosen original F51 interchange from F112.
No phase or integer-charge projection occurs in this equality. -/
theorem c60F112IndependentFaceMixedFrame_face_native
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    c60F44FaceThreeEval
      (c60F112IndependentFaceOriginalMixedFrame
        t₁ t₂ left right C i P).faceStep =
    c60F51Eval
      (c60F112IndependentPairExchangeHom C i P) :=
  c60F112IndependentF43_F51_native C i P

/-- The rotation leg is the AUTHENTIC original F54/F55 typed
physical flag source arrow on exactly the SAME real C60 edge. -/
theorem c60F112IndependentFaceMixedFrame_rotation
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    (c60F112IndependentFaceOriginalMixedFrame
      t₁ t₂ left right C i P).rotationStep =
        c60F46PhysicalFlagOriginalF55Arrow
          t₁ t₂ left right (C.edge i) := rfl

/-- Source-level 4-BOUNDARY categorical commuting square
for ANY independently selected original odd F42 face pair.
The new F47 mixed comparisons remain distinct tagged arrows,
not falsely invented original F55 grammar constructors. -/
theorem c60F112IndependentFaceOriginalMixedSquare
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    c60F47FaceArrow
      (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P) ≫
    c60F47CompareAfter
      (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P) =
    c60F47CompareBefore
      (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P) ≫
    c60F47OriginalF55Arrow
      (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P) :=
  c60F47MixedOriginalBoundarySquare
    (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P)

/-- The source-construction's complete native comparison receiver
is UNIQUE: it cannot depend on a choice of new auxiliary gauge. -/
theorem c60F112IndependentFaceOriginalMixedReceiver_unique
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i)
    (receiver : GradedThreeCell 0 0) :
    (c60F44FaceThreeEval
      (c60F112IndependentFaceOriginalMixedFrame
        t₁ t₂ left right C i P).faceStep + receiver =
      c60F44OriginalF55Eval
        (c60F112IndependentFaceOriginalMixedFrame
          t₁ t₂ left right C i P).rotationStep) ↔
      receiver = c60F46FaceF55ComparisonCalibration := by
  have hcal :=
    (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P).calibrated
  constructor
  · intro h
    exact add_left_cancel (h.trans hcal.symm)
  · intro h
    subst receiver
    exact hcal

/-- A PRECISE SOURCE NO-GO: between exactly the true old
original F54 square-left and square-right rotation routes,
there exists NO original nine-constructor F55 raw cell that
can replace the new calibrated F47 mixed comparison.
This follows from the independently retained F55 phase lock,
not merely nonzero north physical curvature. -/
theorem c60F112IndependentFaceOriginalMixed_noF55Lift
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    ¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112IndependentFaceOriginalMixedFrame
          t₁ t₂ left right C i P).faceStep +
        c60F55SourceNative cell =
      c60F44OriginalF55Eval
        (c60F112IndependentFaceOriginalMixedFrame
          t₁ t₂ left right C i P).rotationStep := by
  rintro ⟨cell, heq⟩
  have hcal :=
    (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P).calibrated
  have hreceiver :
      c60F55SourceNative cell =
        c60F46FaceF55ComparisonCalibration :=
    add_left_cancel (heq.trans hcal.symm)
  have hmem := c60F55SourceNative_mem cell
  rw [hreceiver] at hmem
  exact c60F46FaceF55ComparisonCalibration_notOriginalF55Locked hmem

/-- Complete, independently source-TYPED boundary certificate:
F47 four-boundary mixed source square genuinely COMMUTES,
its F43 face arrow is the full original F51 odd interchange,
and no original F55 source cell can replace Delta.
This does not equate F42 and F54 boundary types. -/
theorem c60F112IndependentFaceMixed_observedSourceBoundary
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i : Fin n) (P : C60F112IndependentOddFacePair C i) :
    (c60F51Eval (c60F112IndependentPairExchangeHom C i P)).phase =
      (1 : ZMod 2) ∧
    c60F77Projection.map
      (c60F51Eval (c60F112IndependentPairExchangeHom C i P)) =
        𝟙 (c60F77Projection.obj GrayGrade.unit) ∧
    (c60F47FaceArrow
      (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P) ≫
      c60F47CompareAfter
        (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P) =
      c60F47CompareBefore
        (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P) ≫
      c60F47OriginalF55Arrow
        (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P)) ∧
    (¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112IndependentFaceOriginalMixedFrame
          t₁ t₂ left right C i P).faceStep +
        c60F55SourceNative cell =
      c60F44OriginalF55Eval
        (c60F112IndependentFaceOriginalMixedFrame
          t₁ t₂ left right C i P).rotationStep) := by
  exact ⟨(c60F112IndependentPairExchange_components C i P).2,
    c60F112IndependentPair_F77_identity C i P,
    c60F112IndependentFaceOriginalMixedSquare t₁ t₂ left right C i P,
    c60F112IndependentFaceOriginalMixed_noF55Lift t₁ t₂ left right C i P⟩

/-- This true four-boundary mixed source square is already
constructed for the full NINETY real C60 edge atlas and each
edge's TWO genuinely distinct original polygon faces.
No synthetic extra physical face is added. -/
theorem c60F112AllNinetyIndependentMixedSquare
    (i : Fin (Fintype.card TruncatedIcosahedralEdge)) (side : Bool) :
    c60F47FaceArrow
      (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right
        c60F108AllNinetyBothFaces i
        (c60F112CanonicalOddFacePair c60F108AllNinetyBothFaces i)) ≫
      c60F47CompareAfter
        (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right
          c60F108AllNinetyBothFaces i
          (c60F112CanonicalOddFacePair c60F108AllNinetyBothFaces i)) =
    c60F47CompareBefore
      (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right
        c60F108AllNinetyBothFaces i
        (c60F112CanonicalOddFacePair c60F108AllNinetyBothFaces i)) ≫
      c60F47OriginalF55Arrow
        (c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right
          c60F108AllNinetyBothFaces i
          (c60F112CanonicalOddFacePair c60F108AllNinetyBothFaces i)) :=
  c60F112IndependentFaceOriginalMixedSquare
    t₁ t₂ left right c60F108AllNinetyBothFaces i
      (c60F112CanonicalOddFacePair c60F108AllNinetyBothFaces i)

#print axioms c60F112IndependentFaceOriginalF43_native
#print axioms c60F112IndependentF43_F51_native
#print axioms c60F112IndependentFaceOriginalMixedFrame
#print axioms c60F112IndependentFaceMixedFrame_edge
#print axioms c60F112IndependentFaceMixedFrame_face_native
#print axioms c60F112IndependentFaceMixedFrame_rotation
#print axioms c60F112IndependentFaceOriginalMixedSquare
#print axioms c60F112IndependentFaceOriginalMixedReceiver_unique
#print axioms c60F112IndependentFaceOriginalMixed_noF55Lift
#print axioms c60F112IndependentFaceMixed_observedSourceBoundary
#print axioms c60F112AllNinetyIndependentMixedSquare

end ActualIndependentMixedSource
end
end KUOS.DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275
