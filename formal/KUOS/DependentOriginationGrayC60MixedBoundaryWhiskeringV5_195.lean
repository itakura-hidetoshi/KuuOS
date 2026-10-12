import KUOS.DependentOriginationGrayC60OriginalNorthMixedSquareV5_195

namespace KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60OriginalNorthMixedSquareV5_195
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.195 F59-F47 — ORIGINAL left/right 1-context whiskerings of mixed squares

A mixed C60/F55 square must be compatible with genuine source
contexts on BOTH different original source sides, not just a bare
target equality. Use the actual F45 original C60 path whiskering
FUNCTORS and original F55 bracket-tree context FUNCTORS together.

In each new typed source, we re-build the entire frame from the
whiskered original arrows; the calibration is derived by the
PREVIOUSLY PROVED F45 full native evaluation invariance, preserving
both independent integer charges AND independent ZMod2 phase.

Both new four-boundary mixed comparison squares therefore commute
in their own correctly indexed categorical 3-Hom. Different C60
path parenthesizations and F54 bracket-tree context source objects
are never falsely declared judgmentally equal. Their common FULL
native Gray receiver remains Δ=(0,1;0).
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalWhiskering
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- Honest simultaneous left-context whiskering:
C60 ORIGINAL path prior acts on each original face 2/3-cell;
F54 ORIGINAL later tree acts on each F54 route and F55 3-cell.
The actual C60 geometric edge is preserved as the site label. -/
def c60F47WhiskerLeft
    (B : C60F47SquareFrame α β r s)
    {u : IcosahedralDart} (prior : Quiver.Path u v)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    C60F47SquareFrame
      ((c60F45LeftWhiskerFunctor prior).obj α)
      ((c60F45LeftWhiskerFunctor prior).obj β)
      ((c60F45F55LeftContextFunctor later).obj r)
      ((c60F45F55LeftContextFunctor later).obj s) where
  edge := B.edge
  faceStep := (c60F45LeftWhiskerFunctor prior).map B.faceStep
  rotationStep := (c60F45F55LeftContextFunctor later).map B.rotationStep
  calibrated := by
    rw [c60F45LeftWhiskerGrayMap, c60F45F55LeftContextGrayMap]
    exact B.calibrated

/-- The original F45 left-whiskered mixed comparison square
is a TRUE categorical square with all FOUR newly typed
whiskered 2-cell boundaries, not a target-only equality. -/
theorem c60F47WhiskerLeft_mixedSquare
    (B : C60F47SquareFrame α β r s)
    {u : IcosahedralDart} (prior : Quiver.Path u v)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    c60F47FaceArrow (c60F47WhiskerLeft B prior later) ≫
        c60F47CompareAfter (c60F47WhiskerLeft B prior later) =
      c60F47CompareBefore (c60F47WhiskerLeft B prior later) ≫
        c60F47OriginalF55Arrow (c60F47WhiskerLeft B prior later) :=
  c60F47MixedOriginalBoundarySquare (c60F47WhiskerLeft B prior later)

/-- Honest simultaneous right-context whiskering:
C60 ORIGINAL suffix acts on the face 2/3-cell and the
original earlier F54 bracket-tree acts on F55 2/3-cells. -/
def c60F47WhiskerRight
    (B : C60F47SquareFrame α β r s)
    {u : IcosahedralDart} (suffix : Quiver.Path w u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa) :
    C60F47SquareFrame
      ((c60F45RightWhiskerFunctor suffix).obj α)
      ((c60F45RightWhiskerFunctor suffix).obj β)
      ((c60F45F55RightContextFunctor earlier).obj r)
      ((c60F45F55RightContextFunctor earlier).obj s) where
  edge := B.edge
  faceStep := (c60F45RightWhiskerFunctor suffix).map B.faceStep
  rotationStep := (c60F45F55RightContextFunctor earlier).map B.rotationStep
  calibrated := by
    rw [c60F45RightWhiskerGrayMap, c60F45F55RightContextGrayMap]
    exact B.calibrated

/-- The original F45 right-whiskered mixed comparison square
commutes as a source CATEGORY equality, after independently
valid original typed whiskering on BOTH source systems. -/
theorem c60F47WhiskerRight_mixedSquare
    (B : C60F47SquareFrame α β r s)
    {u : IcosahedralDart} (suffix : Quiver.Path w u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa) :
    c60F47FaceArrow (c60F47WhiskerRight B suffix earlier) ≫
        c60F47CompareAfter (c60F47WhiskerRight B suffix earlier) =
      c60F47CompareBefore (c60F47WhiskerRight B suffix earlier) ≫
        c60F47OriginalF55Arrow (c60F47WhiskerRight B suffix earlier) :=
  c60F47MixedOriginalBoundarySquare (c60F47WhiskerRight B suffix earlier)

/-- The underlying geometric physical edge is untouched by the
two distinct original kinds of LEFT contextualization. -/
theorem c60F47WhiskerLeft_edge
    (B : C60F47SquareFrame α β r s)
    {u : IcosahedralDart} (prior : Quiver.Path u v)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    (c60F47WhiskerLeft B prior later).edge = B.edge := rfl

/-- Likewise under a right C60 suffix and an original
F54 earlier-bracket context. -/
theorem c60F47WhiskerRight_edge
    (B : C60F47SquareFrame α β r s)
    {u : IcosahedralDart} (suffix : Quiver.Path w u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa) :
    (c60F47WhiskerRight B suffix earlier).edge = B.edge := rfl

/-- In each left-whiskered frame the independent complete Gray
interchanger/naturality still holds after any tensor factor. -/
theorem c60F47WhiskerLeft_tensor
    (B : C60F47SquareFrame α β r s)
    {u : IcosahedralDart} (prior : Quiver.Path u v)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc)
    {i j : ZMod 2} (h : GradedThreeCell i j) :
    ((c60F44FaceThreeEval
        (c60F47WhiskerLeft B prior later).faceStep).tensor h).comp
      (c60F46FaceF55ComparisonCalibration.tensor (GradedThreeCell.ident j)) =
    ((GradedThreeCell.ident 0).tensor h).comp
      ((c60F44OriginalF55Eval
        (c60F47WhiskerLeft B prior later).rotationStep).tensor
          (GradedThreeCell.ident j)) :=
  c60F47MixedSquare_tensor_naturality (c60F47WhiskerLeft B prior later) h

#print axioms c60F47WhiskerLeft
#print axioms c60F47WhiskerLeft_mixedSquare
#print axioms c60F47WhiskerRight
#print axioms c60F47WhiskerRight_mixedSquare
#print axioms c60F47WhiskerLeft_tensor

end OriginalWhiskering

end
end KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
