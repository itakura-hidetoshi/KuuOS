import KUOS.DependentOriginationGrayC60MixedComparisonObstructionV5_196

namespace KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60MixedComparisonObstructionV5_196
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F48 / v5.196 — categorical transport between mixed face choices

The two actual adjacent polygonal C60 faces at one physical edge
have genuinely DISTINCT original F42 dependent path boundaries.
F48 constructs separate local four-boundary MIXED SOURCE 3-Hom
categories for both choices, each with the SAME original F54/F55
rotation routes. Their original C60 face steps have EQUAL FULL
native Gray images, and their genuine original F55 source steps
have the same target.

Here we construct an ACTUAL Mathlib FUNCTOR between these
SEPARATELY TYPED MIXED 3-Hom categories. It relabels the four
mixed boundary slots, maps each proof-relevant raw original-face,
original-F55, comparison-before, comparison-after and composite
constructor, and descends through the complete native Gray kernel.
The functor is faithful and transports the entire commuting mixed
source square, not just an equality of integer/phase values.

IMPORTANT: this is an honest comparison functor between the
NEWLY ADJOINED F47 mixed four-boundary presentations; it is
NOT a functor between the pre-existing raw F42 polygonal
2-cell source categories or a global nondegenerate Gray 3-functor.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GeneralMixedFrameTransport
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w v' w' : IcosahedralDart}
variable {p q : Quiver.Path v w} {p' q' : Quiver.Path v' w'}
variable {α β : C60F42PresentedFaceCell p q}
variable {α' β' : C60F42PresentedFaceCell p' q'}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

variable (B₀ : C60F47SquareFrame α β r s)
  (B₁ : C60F47SquareFrame α' β' r s)

/-- An explicit typed change-of-presentation of the four
boundary positions. The original F42 face paths in the
two different mixed frames remain distinct source data. -/
def c60F48ChangeMixedBoundaryPoint :
    C60F47BoundaryPoint B₀ → C60F47BoundaryPoint B₁
  | .faceBefore => .faceBefore
  | .faceAfter => .faceAfter
  | .rotationBefore => .rotationBefore
  | .rotationAfter => .rotationAfter

/-- Transport ALL five primitive / composite raw mixed 3-cell
constructors, with matching genuinely typed boundaries. -/
def c60F48ChangeMixedRaw
    {X Y : C60F47BoundaryPoint B₀}
    (f : C60F47PresentedMixedThreeCell B₀ X Y) :
    C60F47PresentedMixedThreeCell B₁
      (c60F48ChangeMixedBoundaryPoint B₀ B₁ X)
      (c60F48ChangeMixedBoundaryPoint B₀ B₁ Y) := by
  induction f with
  | ident X => exact .ident _
  | originalFace => exact .originalFace
  | originalF55 => exact .originalF55
  | compareBefore => exact .compareBefore
  | compareAfter => exact .compareAfter
  | trans f g ihf ihg => exact .trans ihf ihg

/-- Every raw constructor's FULL Int×Int and ZMod2 Gray
value is preserved by boundary relabeling, provided the
two ORIGINAL source face and F55 arrows have matching
full target images. No bare parity projection is allowed. -/
theorem c60F48ChangeMixedRaw_native
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀}
    (f : C60F47PresentedMixedThreeCell B₀ X Y) :
    (c60F48ChangeMixedRaw B₀ B₁ f).toNative = f.toNative := by
  induction f with
  | ident X => rfl
  | originalFace =>
      change c60F44FaceThreeEval B₁.faceStep =
        c60F44FaceThreeEval B₀.faceStep
      exact hface.symm
  | originalF55 =>
      change c60F44OriginalF55Eval B₁.rotationStep =
        c60F44OriginalF55Eval B₀.rotationStep
      exact hrotation.symm
  | compareBefore => rfl
  | compareAfter => rfl
  | trans f g ihf ihg =>
      change (c60F48ChangeMixedRaw B₀ B₁ f).toNative +
          (c60F48ChangeMixedRaw B₀ B₁ g).toNative =
        f.toNative + g.toNative
      rw [ihf, ihg]

/-- Genuine Mathlib FUNCTOR between different locally mixed
source 3-Hom categories, constructed from the complete original
Gray image equalities of their two real source arrows. -/
def c60F48MixedBoundaryTransportFunctor
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep) :
    C60F47BoundaryPoint B₀ ⥤ C60F47BoundaryPoint B₁ where
  obj := c60F48ChangeMixedBoundaryPoint B₀ B₁
  map := fun {_ _} f =>
    Quot.liftOn f
      (fun raw => c60F47MixedOf
        (c60F48ChangeMixedRaw B₀ B₁ raw))
      (by
        intro f g h
        apply Quot.sound
        calc
          (c60F48ChangeMixedRaw B₀ B₁ f).toNative =
              f.toNative :=
            c60F48ChangeMixedRaw_native B₀ B₁ hface hrotation f
          _ = g.toNative := h
          _ = (c60F48ChangeMixedRaw B₀ B₁ g).toNative :=
            (c60F48ChangeMixedRaw_native B₀ B₁ hface hrotation g).symm)
  map_id := by
    intro X
    apply Quot.sound
    rfl
  map_comp := by
    intro X Y Z f g
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    apply Quot.sound
    rfl

/-- This categorical transport preserves EVERY original and
newly mixed 3-arrow's full native value, for all typed endpoints. -/
theorem c60F48MixedBoundaryTransportFunctor_fullNative
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀} (f : X ⟶ Y) :
    c60F47MixedEval
      ((c60F48MixedBoundaryTransportFunctor
        B₀ B₁ hface hrotation).map f) =
      c60F47MixedEval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact c60F48ChangeMixedRaw_native B₀ B₁ hface hrotation raw

theorem c60F48MixedBoundaryTransportFunctor_faithful
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀} {f g : X ⟶ Y}
    (heq : (c60F48MixedBoundaryTransportFunctor
        B₀ B₁ hface hrotation).map f =
      (c60F48MixedBoundaryTransportFunctor
        B₀ B₁ hface hrotation).map g) : f = g := by
  have hh :
      c60F47MixedEval
        ((c60F48MixedBoundaryTransportFunctor
          B₀ B₁ hface hrotation).map f) =
      c60F47MixedEval
        ((c60F48MixedBoundaryTransportFunctor
          B₀ B₁ hface hrotation).map g) :=
    congrArg (fun h => c60F47MixedEval h) heq
  rw [c60F48MixedBoundaryTransportFunctor_fullNative,
    c60F48MixedBoundaryTransportFunctor_fullNative] at hh
  exact c60F47MixedGrayFunctor_faithful B₀ hh

/-- The ENTIRE type-correct mixed source square is transported
as a composite arrow, not only pointwise as a Gray equality. -/
theorem c60F48MixedBoundaryTransport_square
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep) :
    (c60F48MixedBoundaryTransportFunctor B₀ B₁ hface hrotation).map
      (c60F47FaceArrow B₀ ≫ c60F47CompareAfter B₀) =
      c60F47FaceArrow B₁ ≫ c60F47CompareAfter B₁ := by
  apply Quot.sound
  rfl

end GeneralMixedFrameTransport

/-! ## The genuine pair of incident surface faces on each real edge -/

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

/-- A true categorical change-of-face functor for any of the 90
physical edges: first incident original polygon → second incident
ORIGINAL polygon, while preserving the same actual original F55
rotation-square 2/3-cell and all integer/phase coordinates. -/
def c60F48ActualEdgeFaceChoiceFunctor (edge : TruncatedIcosahedralEdge) :
    C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false) ⥤
    C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true) :=
  c60F48MixedBoundaryTransportFunctor
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)
    (by
      rw [c60F48EveryRealEdgeFaceStep_native,
        c60F48EveryRealEdgeFaceStep_native])
    (by rfl)

/-- Both genuine separately typed face mixed source categories
are related by a full native-faithful categorical transporter. -/
theorem c60F48ActualEdgeFaceChoiceFunctor_faithful
    (edge : TruncatedIcosahedralEdge)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)}
    {f g : X ⟶ Y}
    (h : (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge).map f =
      (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge).map g) :
    f = g := by
  exact c60F48MixedBoundaryTransportFunctor_faithful
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)
    (by rw [c60F48EveryRealEdgeFaceStep_native,
      c60F48EveryRealEdgeFaceStep_native])
    (by rfl) h

/-- The actual original 90-edge face-choice change transports
the SOURCE comparison square into the second physical face's
separately typed mixed source category. -/
theorem c60F48ActualEdgeFaceChoiceFunctor_square
    (edge : TruncatedIcosahedralEdge) :
    (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge).map
      (c60F47FaceArrow
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false) ≫
       c60F47CompareAfter
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)) =
      c60F47FaceArrow
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true) ≫
      c60F47CompareAfter
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true) := by
  apply Quot.sound
  rfl

#print axioms c60F48ActualEdgeFaceChoiceFunctor
#print axioms c60F48ActualEdgeFaceChoiceFunctor_faithful
#print axioms c60F48ActualEdgeFaceChoiceFunctor_square

end EveryRealEdge

#print axioms c60F48MixedBoundaryTransportFunctor
#print axioms c60F48MixedBoundaryTransportFunctor_faithful
#print axioms c60F48MixedBoundaryTransport_square

end
end KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196
