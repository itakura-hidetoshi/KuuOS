import KUOS.DependentOriginationGrayC60F55MixedCocycleV5_205
import KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195

namespace KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205

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
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60MixedComparisonObstructionV5_196
open KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196
open KUOS.DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204
open KUOS.DependentOriginationGrayC60F55MixedCocycleV5_205
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.205 / F59-F56-B: genuine original-F42 and original-F54/F55
# contextual whiskering functors for independently typed F47 mixed squares

F48's old face-choice functor required both local frames to have
the EXACT SAME original F54 rotation-route types. Thus it CANNOT
be used directly when the independent original F55 bracket-tree
context changes those types.

Here construct a NEW fully typed FOUR-BOUNDARY SOURCE functor
between two F47 mixed square frames having arbitrary, separately
typed original F42 physical path indices and separately typed
original F54/F55 bracket-tree rotation-route indices. The two
actual original face/F55 morphism images must agree in the full
Int×Int/phase native target, and the physical C60 edge MUST match.

Then instantiate this genuinely new source functor on:
  (1) the original F42 LEFT 1-path whisker and original F54/F55
      LEFT bracket-tree context simultaneously;
  (2) the original F42 RIGHT 1-path whisker and original F54/F55
      RIGHT bracket-tree context simultaneously.
Both contexts preserve each original physical edge and the
ENTIRE source mixed comparison square, with distinct original
2-cell proof witnesses and independently typed source routes.

The new mixed comparison Delta remains ADJOINED, not a tenth
original F55 constructor. Complete native target equality does
NOT identify raw original F42 or F54 source witness terms.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section AcrossIndependentOriginalRotations
variable {a b : D} {x y : E}
variable {n₀ n₀' m₀ m₀' n₁ n₁' m₁ m₁' : Nat}
variable {ma₀ mb₀ ma₁ mb₁ : Blocks a b}
variable {pa₀ pb₀ pa₁ pb₁ : Blocks x y}
variable {first₀ : OriginalF45BracketTree n₀ m₀ ma₀ pa₀ mb₀ pb₀}
variable {last₀ : OriginalF45BracketTree n₀' m₀' ma₀ pa₀ mb₀ pb₀}
variable {first₁ : OriginalF45BracketTree n₁ m₁ ma₁ pa₁ mb₁ pb₁}
variable {last₁ : OriginalF45BracketTree n₁' m₁' ma₁ pa₁ mb₁ pb₁}
variable {r₀ s₀ : OriginalF45BracketTree.DepthRotationRoute first₀ last₀}
variable {r₁ s₁ : OriginalF45BracketTree.DepthRotationRoute first₁ last₁}
variable {v₀ w₀ v₁ w₁ : IcosahedralDart}
variable {p₀ q₀ : Quiver.Path v₀ w₀}
variable {p₁ q₁ : Quiver.Path v₁ w₁}
variable {α₀ β₀ : C60F42PresentedFaceCell p₀ q₀}
variable {α₁ β₁ : C60F42PresentedFaceCell p₁ q₁}
variable (B₀ : C60F47SquareFrame α₀ β₀ r₀ s₀)
variable (B₁ : C60F47SquareFrame α₁ β₁ r₁ s₁)

/-- Object change PRESERVES the four independently typed mixed
boundary TAGS even when BOTH original F42 source 1-paths and
original F54 rotation trees have different types. -/
def c60F56ContextMixedPoint :
    C60F47BoundaryPoint B₀ → C60F47BoundaryPoint B₁
  | .faceBefore => .faceBefore
  | .faceAfter => .faceAfter
  | .rotationBefore => .rotationBefore
  | .rotationAfter => .rotationAfter

/-- Every genuine original FACE and ORIGINAL F55 generator,
plus NEW compare-before/after, identity and trans, has a
corresponding RAW source F47 arrow under mixed contextuality. -/
def c60F56ContextMixedRaw
    {X Y : C60F47BoundaryPoint B₀}
    (f : C60F47PresentedMixedThreeCell B₀ X Y) :
    C60F47PresentedMixedThreeCell B₁
      (c60F56ContextMixedPoint B₀ B₁ X)
      (c60F56ContextMixedPoint B₀ B₁ Y) := by
  induction f with
  | ident X => exact .ident _
  | originalFace => exact .originalFace
  | originalF55 => exact .originalF55
  | compareBefore => exact .compareBefore
  | compareAfter => exact .compareAfter
  | trans f g ihf ihg => exact .trans ihf ihg

/-- This does NOT project away the exchange phase or either
integer generator charge. Full source-Gray preservation follows
on ALL raw mixed F47 constructors from the two independent
original face/F55 evaluator equalities. -/
theorem c60F56ContextMixedRaw_native
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀}
    (f : C60F47PresentedMixedThreeCell B₀ X Y) :
    (c60F56ContextMixedRaw B₀ B₁ f).toNative = f.toNative := by
  induction f with
  | ident X => rfl
  | originalFace => exact hface.symm
  | originalF55 => exact hrotation.symm
  | compareBefore => rfl
  | compareAfter => rfl
  | trans f g ihf ihg =>
      change (c60F56ContextMixedRaw B₀ B₁ f).toNative +
          (c60F56ContextMixedRaw B₀ B₁ g).toNative =
        f.toNative + g.toNative
      rw [ihf, ihg]

/-- A NEW Mathlib source functor over two genuinely DIFFERENT
F42/F54 original boundary systems. The authentic physical C60
edge must remain the same; only proved full Gray equality of
the original two old 3-arrows admits this change of context. -/
def c60F56ContextMixedFunctor
    (_hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep) :
    C60F47BoundaryPoint B₀ ⥤ C60F47BoundaryPoint B₁ where
  obj := c60F56ContextMixedPoint B₀ B₁
  map := fun {_ _} f =>
    Quot.liftOn f
      (fun raw => c60F47MixedOf
        (c60F56ContextMixedRaw B₀ B₁ raw))
      (by
        intro f g h
        apply Quot.sound
        calc
          (c60F56ContextMixedRaw B₀ B₁ f).toNative = f.toNative :=
            c60F56ContextMixedRaw_native B₀ B₁ hface hrotation f
          _ = g.toNative := h
          _ = (c60F56ContextMixedRaw B₀ B₁ g).toNative :=
            (c60F56ContextMixedRaw_native B₀ B₁ hface hrotation g).symm)
  map_id := by
    intro X
    apply Quot.sound
    rfl
  map_comp := by
    intro X Y Z f g
    refine Quot.inductionOn f (fun rawf => ?_)
    refine Quot.inductionOn g (fun rawg => ?_)
    apply Quot.sound
    rfl

/-- The restriction to actual original physical edges and
independent typed contexts does not change any full native
original F43/F55 or NEW F47 mixed 3-morphism evaluation. -/
theorem c60F56ContextMixedFunctor_fullNative
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀} (f : X ⟶ Y) :
    c60F47MixedEval
      ((c60F56ContextMixedFunctor
        B₀ B₁ hedge hface hrotation).map f) =
      c60F47MixedEval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact c60F56ContextMixedRaw_native B₀ B₁ hface hrotation raw

/-- The cross-original-F42/F54 contextual functor remains
faithful on all F47 mixed 3-Hom quotients. Original 2-cell
objects themselves are NOT asserted equal across contexts. -/
theorem c60F56ContextMixedFunctor_faithful
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀}
    {f g : X ⟶ Y}
    (h : (c60F56ContextMixedFunctor
      B₀ B₁ hedge hface hrotation).map f =
      (c60F56ContextMixedFunctor
        B₀ B₁ hedge hface hrotation).map g) : f = g := by
  have hh := congrArg (fun z => c60F47MixedEval z) h
  change c60F47MixedEval
        ((c60F56ContextMixedFunctor
          B₀ B₁ hedge hface hrotation).map f) =
      c60F47MixedEval
        ((c60F56ContextMixedFunctor
          B₀ B₁ hedge hface hrotation).map g) at hh
  rw [c60F56ContextMixedFunctor_fullNative,
    c60F56ContextMixedFunctor_fullNative] at hh
  exact c60F47MixedGrayFunctor_faithful B₀ hh

/-- The entire independently typed F47 comparison square is
preserved as a category arrow; no original F42 term is
mistaken for an F54 rotation term. -/
theorem c60F56ContextMixedFunctor_square
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep) :
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrotation).map
      (c60F47FaceArrow B₀ ≫ c60F47CompareAfter B₀) =
      c60F47FaceArrow B₁ ≫ c60F47CompareAfter B₁ := by
  apply Quot.sound
  rfl

end AcrossIndependentOriginalRotations

/-! ## Actual original F42 C60 and original F54/F55 contexts -/

section IndependentLeftAndRightWhiskering
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart}
variable {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}
variable (B : C60F47SquareFrame α β r s)

/-- Simultaneously context BOTH independent original source
systems: an actual physical C60 PRIOR path left-whiskers the
F42 face and the independently typed original F54 LATER tree
left-contexts both F54 routes and their F55 3-arrows. -/
def c60F56OriginalLeftMixedContextFunctor
    {u : IcosahedralDart} (prior : Quiver.Path u v)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    C60F47BoundaryPoint B ⥤
      C60F47BoundaryPoint (c60F47WhiskerLeft B prior later) :=
  c60F56ContextMixedFunctor B (c60F47WhiskerLeft B prior later)
    rfl
    (c60F45LeftWhiskerGrayMap prior B.faceStep).symm
    (c60F45F55LeftContextGrayMap later B.rotationStep).symm

/-- The actual F42 right suffix and original F54 earlier
tree right-context are independent operations; here both
produce a correctly typed source F47 functor on the
four original boundary positions. -/
def c60F56OriginalRightMixedContextFunctor
    {u : IcosahedralDart} (suffix : Quiver.Path w u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa) :
    C60F47BoundaryPoint B ⥤
      C60F47BoundaryPoint (c60F47WhiskerRight B suffix earlier) :=
  c60F56ContextMixedFunctor B (c60F47WhiskerRight B suffix earlier)
    rfl
    (c60F45RightWhiskerGrayMap suffix B.faceStep).symm
    (c60F45F55RightContextGrayMap earlier B.rotationStep).symm

/-- An HONEST categorical preservation of the source mixed
comparison square after actual left F42 path context PLUS
original F54/F55 bracket-tree context. Source arrows are
not identified across their different original 2-cell types. -/
theorem c60F56OriginalLeftMixedContext_square
    {u : IcosahedralDart} (prior : Quiver.Path u v)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    (c60F56OriginalLeftMixedContextFunctor
      B prior later).map
      (c60F47FaceArrow B ≫ c60F47CompareAfter B) =
    c60F47FaceArrow (c60F47WhiskerLeft B prior later) ≫
      c60F47CompareAfter (c60F47WhiskerLeft B prior later) := by
  apply Quot.sound
  rfl

theorem c60F56OriginalRightMixedContext_square
    {u : IcosahedralDart} (suffix : Quiver.Path w u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa) :
    (c60F56OriginalRightMixedContextFunctor
      B suffix earlier).map
      (c60F47FaceArrow B ≫ c60F47CompareAfter B) =
    c60F47FaceArrow (c60F47WhiskerRight B suffix earlier) ≫
      c60F47CompareAfter (c60F47WhiskerRight B suffix earlier) := by
  apply Quot.sound
  rfl

/-- Both INDEPENDENT source left contexts leave the actual
C60 original physical four-flag edge unchanged. -/
theorem c60F56OriginalLeftMixedContext_edge
    {u : IcosahedralDart} (prior : Quiver.Path u v)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    (c60F47WhiskerLeft B prior later).edge = B.edge :=
  c60F47WhiskerLeft_edge B prior later

/-- The right C60 path and old F54/F55 bracket tree
contexts likewise preserve the exact same physical edge. -/
theorem c60F56OriginalRightMixedContext_edge
    {u : IcosahedralDart} (suffix : Quiver.Path w u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa) :
    (c60F47WhiskerRight B suffix earlier).edge = B.edge :=
  c60F47WhiskerRight_edge B suffix earlier

end IndependentLeftAndRightWhiskering

#print axioms c60F56ContextMixedFunctor
#print axioms c60F56ContextMixedFunctor_fullNative
#print axioms c60F56ContextMixedFunctor_faithful
#print axioms c60F56ContextMixedFunctor_square
#print axioms c60F56OriginalLeftMixedContextFunctor
#print axioms c60F56OriginalRightMixedContextFunctor
#print axioms c60F56OriginalLeftMixedContext_square
#print axioms c60F56OriginalRightMixedContext_square
#print axioms c60F56OriginalLeftMixedContext_edge
#print axioms c60F56OriginalRightMixedContext_edge

end
end KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
