import KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194

namespace KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F47 / v5.195 — correctly typed mixed C60-face / original F55 boundary 3-Hom

The original C60 face 2-cells and original F54 bracket rotation 2-cells
belong to different 2-dimensional source systems. F46 constructed
the unique full native Gray receiver Δ=(0,1;0), but explicitly proved
that Δ is NOT represented by an original nine-constructor F55 3-cell.

This file ADJOINS two genuinely NEW mixed boundary-comparison
generators between four *tagged*, original, typed 2-cell boundaries:
the source boundary comparison has native image 0; the target
boundary comparison has native image Δ. The true original C60 face
3-arrow and true original F55 rotation-square 3-arrow remain separate
primitive generators. A mixed square is admitted only if its complete
Gray calibration is actually proved, with original C60 physical edge
data and BOTH independently typed source arrows retained.

The resulting proof-relevant mixed free-category quotient has a
genuine Mathlib Category instance, a faithful native Gray functor,
and an exactly commuting mixed comparison square. The native kernel
quotient retains both independent integer charges and the separate
ZMod2 phase. No equation between unrelated raw original source
2-cells, nor a nonexistent original F55 Δ-arrow, is asserted.

The source is a LOCAL, explicitly ADJOINED four-boundary comparison
category. It is not yet the globally nondegenerate Gray 3-category
on all original C60 0/1/2/3 cells.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section MixedBoundary
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- Each mixed source square retains the EXACT two original
face-2-cell endpoints, the EXACT two original F54 rotation
2-cell endpoints, its real C60 physical edge, and the TWO
genuine original categorical 3-arrows. The calibration is a
proved property, not an axiom or an implicit identification. -/
structure C60F47SquareFrame
    (α β : C60F42PresentedFaceCell p q)
    (r s : OriginalF45BracketTree.DepthRotationRoute first last) where
  edge : TruncatedIcosahedralEdge
  faceStep : α ⟶ β
  rotationStep : r ⟶ s
  calibrated :
    c60F44FaceThreeEval faceStep +
      c60F46FaceF55ComparisonCalibration =
        c60F44OriginalF55Eval rotationStep

/-- Four different 2-cell boundary POSITIONS. Their original,
different type-indexed source 2-cells are stored in the frame.
The tags prevent any Lean definitional equality from
silently identifying a polygonal face with an F54 route. -/
inductive C60F47BoundaryPoint
    (B : C60F47SquareFrame α β r s) where
  | faceBefore | faceAfter | rotationBefore | rotationAfter

/-- Proof-relevant RAW mixed 3-cells. The two new bridge
constructors are NOT smuggled into the original F55 syntax.
Every composite has literally matching boundary positions. -/
inductive C60F47PresentedMixedThreeCell
    (B : C60F47SquareFrame α β r s) :
      C60F47BoundaryPoint B → C60F47BoundaryPoint B → Type _ where
  | ident (X : C60F47BoundaryPoint B) :
      C60F47PresentedMixedThreeCell B X X
  | originalFace :
      C60F47PresentedMixedThreeCell B .faceBefore .faceAfter
  | originalF55 :
      C60F47PresentedMixedThreeCell B .rotationBefore .rotationAfter
  | compareBefore :
      C60F47PresentedMixedThreeCell B .faceBefore .rotationBefore
  | compareAfter :
      C60F47PresentedMixedThreeCell B .faceAfter .rotationAfter
  | trans {X Y Z : C60F47BoundaryPoint B}
      (f : C60F47PresentedMixedThreeCell B X Y)
      (g : C60F47PresentedMixedThreeCell B Y Z) :
      C60F47PresentedMixedThreeCell B X Z

/-- Complete native target evaluation, retaining Int×Int and
independent phase, for EVERY original and mixed constructor. -/
def C60F47PresentedMixedThreeCell.toNative
    {B : C60F47SquareFrame α β r s}
    {X Y : C60F47BoundaryPoint B}
    (f : C60F47PresentedMixedThreeCell B X Y) :
      GradedThreeCell 0 0 :=
  match f with
  | .ident _ => 0
  | .originalFace => c60F44FaceThreeEval B.faceStep
  | .originalF55 => c60F44OriginalF55Eval B.rotationStep
  | .compareBefore => 0
  | .compareAfter => c60F46FaceF55ComparisonCalibration
  | .trans f g => f.toNative + g.toNative

/-- Only the genuine complete Gray evaluation is quotiented.
Original raw witnesses and all four boundary TYPES remain
available and separate before the quotient. -/
abbrev C60F47MixedHom
    (B : C60F47SquareFrame α β r s)
    (X Y : C60F47BoundaryPoint B) :=
  Quot (fun f g : C60F47PresentedMixedThreeCell B X Y =>
    f.toNative = g.toNative)

def c60F47MixedOf
    {B : C60F47SquareFrame α β r s}
    {X Y : C60F47BoundaryPoint B}
    (f : C60F47PresentedMixedThreeCell B X Y) :
    C60F47MixedHom B X Y :=
  Quot.mk _ f

def c60F47MixedEval
    {B : C60F47SquareFrame α β r s}
    {X Y : C60F47BoundaryPoint B}
    (f : C60F47MixedHom B X Y) : GradedThreeCell 0 0 :=
  Quot.liftOn f (fun raw => raw.toNative) (by
    intro f g h
    exact h)

@[simp] theorem c60F47MixedEval_of
    {B : C60F47SquareFrame α β r s}
    {X Y : C60F47BoundaryPoint B}
    (f : C60F47PresentedMixedThreeCell B X Y) :
    c60F47MixedEval (c60F47MixedOf f) = f.toNative := rfl

def c60F47MixedComp
    {B : C60F47SquareFrame α β r s}
    {X Y Z : C60F47BoundaryPoint B}
    (f : C60F47MixedHom B X Y)
    (g : C60F47MixedHom B Y Z) :
    C60F47MixedHom B X Z :=
  Quot.liftOn₂ f g
    (fun left right => c60F47MixedOf (.trans left right))
    (by
      intro left right₁ right₂ heq
      apply Quot.sound
      change left.toNative + right₁.toNative =
        left.toNative + right₂.toNative
      rw [heq])
    (by
      intro left₁ left₂ right heq
      apply Quot.sound
      change left₁.toNative + right.toNative =
        left₂.toNative + right.toNative
      rw [heq])

theorem c60F47MixedEval_comp
    {B : C60F47SquareFrame α β r s}
    {X Y Z : C60F47BoundaryPoint B}
    (f : C60F47MixedHom B X Y)
    (g : C60F47MixedHom B Y Z) :
    c60F47MixedEval (c60F47MixedComp f g) =
      c60F47MixedEval f + c60F47MixedEval g := by
  refine Quot.inductionOn f (fun f => ?_)
  refine Quot.inductionOn g (fun g => ?_)
  rfl

/-- New genuinely TYPED Mathlib 3-Hom category over the four
original boundary slots. Associativity and identities hold
after the *specified* exact native kernel quotient. -/
instance c60F47MixedCategory
    (B : C60F47SquareFrame α β r s) :
    Category (C60F47BoundaryPoint B) where
  Hom := C60F47MixedHom B
  id X := c60F47MixedOf (.ident X)
  comp := c60F47MixedComp
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change (0 : GradedThreeCell 0 0) + raw.toNative = raw.toNative
    exact zero_add _
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change raw.toNative + (0 : GradedThreeCell 0 0) = raw.toNative
    exact add_zero _
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    refine Quot.inductionOn h (fun h => ?_)
    apply Quot.sound
    change (f.toNative + g.toNative) + h.toNative =
      f.toNative + (g.toNative + h.toNative)
    exact add_assoc _ _ _

/-- A real Mathlib functor, faithful on the chosen complete
native-kernel quotient: BOTH integer charges and phase survive. -/
def c60F47MixedGrayFunctor
    (B : C60F47SquareFrame α β r s) :
    C60F47BoundaryPoint B ⥤ GrayGrade where
  obj _ := GrayGrade.unit
  map := fun {_ _} f => c60F47MixedEval f
  map_id := by
    intro X
    apply GradedThreeCell.ext <;> rfl
  map_comp := by
    intro X Y Z f g
    change c60F47MixedEval (c60F47MixedComp f g) =
      (c60F47MixedEval f ≫ c60F47MixedEval g :
        GrayGrade.unit ⟶ GrayGrade.unit)
    rw [c60F47MixedEval_comp]
    exact grayNeutral_add_eq_native_comp
      (c60F47MixedEval f) (c60F47MixedEval g)

theorem c60F47MixedGrayFunctor_faithful
    (B : C60F47SquareFrame α β r s)
    {X Y : C60F47BoundaryPoint B}
    {f g : X ⟶ Y}
    (h : (c60F47MixedGrayFunctor B).map f =
      (c60F47MixedGrayFunctor B).map g) : f = g := by
  change c60F47MixedEval f = c60F47MixedEval g at h
  revert h
  refine Quot.inductionOn f (fun f => ?_)
  refine Quot.inductionOn g (fun g hh => ?_)
  exact Quot.sound hh

/-! ## The four EXACT source/mixed boundary arrows -/

def c60F47FaceArrow (B : C60F47SquareFrame α β r s) :
    (C60F47BoundaryPoint.faceBefore : C60F47BoundaryPoint B) ⟶
      .faceAfter :=
  c60F47MixedOf .originalFace

def c60F47OriginalF55Arrow (B : C60F47SquareFrame α β r s) :
    (C60F47BoundaryPoint.rotationBefore : C60F47BoundaryPoint B) ⟶
      .rotationAfter :=
  c60F47MixedOf .originalF55

def c60F47CompareBefore (B : C60F47SquareFrame α β r s) :
    (C60F47BoundaryPoint.faceBefore : C60F47BoundaryPoint B) ⟶
      .rotationBefore :=
  c60F47MixedOf .compareBefore

def c60F47CompareAfter (B : C60F47SquareFrame α β r s) :
    (C60F47BoundaryPoint.faceAfter : C60F47BoundaryPoint B) ⟶
      .rotationAfter :=
  c60F47MixedOf .compareAfter

/-- A genuinely COMMUTING square of four correctly typed source
2-cell boundaries. The two original source 3-arrows occupy
different sides. The two NEW mixed comparison 3-arrows connect
them, without falsely identifying their original source types. -/
theorem c60F47MixedOriginalBoundarySquare
    (B : C60F47SquareFrame α β r s) :
    c60F47FaceArrow B ≫ c60F47CompareAfter B =
      c60F47CompareBefore B ≫ c60F47OriginalF55Arrow B := by
  apply Quot.sound
  change c60F44FaceThreeEval B.faceStep +
    c60F46FaceF55ComparisonCalibration =
    (0 : GradedThreeCell 0 0) + c60F44OriginalF55Eval B.rotationStep
  simpa only [zero_add] using B.calibrated

/-- The TARGET comparison is genuinely new and nonidentity:
it has square integer charge one and exchange phase zero. -/
theorem c60F47CompareAfter_native_components
    (B : C60F47SquareFrame α β r s) :
    ((c60F47MixedGrayFunctor B).map
      (c60F47CompareAfter B)).charge = ((0 : Int), (1 : Int)) ∧
    ((c60F47MixedGrayFunctor B).map
      (c60F47CompareAfter B)).phase = (0 : ZMod 2) := by
  exact ⟨rfl, rfl⟩

/-- The SOURCE comparison is a distinct typed mixed arrow
although its entire target Gray charge and phase vanish. -/
theorem c60F47CompareBefore_native_zero
    (B : C60F47SquareFrame α β r s) :
    (c60F47MixedGrayFunctor B).map
      (c60F47CompareBefore B) = (0 : GradedThreeCell 0 0) := rfl

/-- The calibrated comparison respects horizontal/tensor
composition with ANY independent genuinely typed Gray 3-cell.
This is the existing F59 interchange-compatible tensor law
applied to the NEW original mixed source boundary square. -/
theorem c60F47MixedSquare_tensor_naturality
    (B : C60F47SquareFrame α β r s)
    {i j : ZMod 2} (h : GradedThreeCell i j) :
    ((c60F44FaceThreeEval B.faceStep).tensor h).comp
        (c60F46FaceF55ComparisonCalibration.tensor
          (GradedThreeCell.ident j)) =
      ((GradedThreeCell.ident 0).tensor h).comp
        ((c60F44OriginalF55Eval B.rotationStep).tensor
          (GradedThreeCell.ident j)) := by
  have hframe :
      (c60F44FaceThreeEval B.faceStep).comp
        c60F46FaceF55ComparisonCalibration =
      (GradedThreeCell.ident 0).comp
        (c60F44OriginalF55Eval B.rotationStep) := by
    change c60F44FaceThreeEval B.faceStep +
      c60F46FaceF55ComparisonCalibration =
        (0 : GradedThreeCell 0 0) +
          c60F44OriginalF55Eval B.rotationStep
    simpa only [zero_add] using B.calibrated
  calc
    _ = ((c60F44FaceThreeEval B.faceStep).comp
          c60F46FaceF55ComparisonCalibration).tensor
        (h.comp (GradedThreeCell.ident j)) :=
      GradedThreeCell.tensor_comp _ _ _ _
    _ = ((GradedThreeCell.ident 0).comp
          (c60F44OriginalF55Eval B.rotationStep)).tensor
        (h.comp (GradedThreeCell.ident j)) := by rw [hframe]
    _ = _ := (GradedThreeCell.tensor_comp _ _ _ _).symm

/-- The ACTUAL Gray exchange is natural for the newly
adjoined mixed comparison generator, including both full
integer charges and the independent exchange phase. -/
theorem c60F47MixedComparison_GrayExchange
    {i j : ZMod 2} (h : GradedThreeCell i j) :
    (c60F46FaceF55ComparisonCalibration.tensor h).comp
        (GradedThreeCell.exchange 0 j) =
      (GradedThreeCell.exchange 0 i).comp
        (h.tensor c60F46FaceF55ComparisonCalibration) :=
  GradedThreeCell.exchange_naturality
    c60F46FaceF55ComparisonCalibration h

end MixedBoundary

#print axioms c60F47MixedGrayFunctor
#print axioms c60F47MixedGrayFunctor_faithful
#print axioms c60F47MixedOriginalBoundarySquare
#print axioms c60F47CompareAfter_native_components
#print axioms c60F47MixedSquare_tensor_naturality
#print axioms c60F47MixedComparison_GrayExchange

end
end KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
