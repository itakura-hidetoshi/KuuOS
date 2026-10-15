import KUOS.DependentOriginationGrayC60OriginalFaceTypedThreeHomLiftV5_198

namespace KUOS.DependentOriginationGrayC60OriginalFaceDecoratedThreeHomV5_198

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60OriginalFaceTypedThreeHomLiftV5_198

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F50 / v5.198 — proof-relevant ORIGINAL face 2-cell carrier

The F49 graded Gray 3-category envelope is complete in degrees,
integer charges and exchange phase, but it has *forgotten* which
genuine original F42 polygonal proof witness gave the grade.

We construct a separately and GENUINELY SOURCE-PRESERVING local
3-Hom category whose objects each store:
  (a) the ORIGINAL exact typed F42 face 2-cell,
  (b) its completely typed native F49 graded 2-cell image, and
  (c) a PROVED equality between native grade and source F43 degree.

Its categorical 3-Homs are precisely the actual ORIGINAL
proof-relevant F43 higher source words modulo ONLY the F44
full-target kernel. This local source category is *isomorphic
on objects* and fully faithful on arrows with the original F44
category via explicit inverse functors. Thus BOTH original
proof-relevant 2-cell witnesses and complete 3-cell information
are retained in this enhanced SOURCE; no invented equality of
the original F42 horizontal composition orders is postulated.

The evaluated functor to F49 remains faithful on higher morphisms,
but not injective on original source 2-cell objects. This is an
honest step toward the full original C60/F55 3-category, not a
claim to have constructed the unprovided F42/F54 mixed global
2-cell boundary-gluing functors.
-/

/-- An original 2-cell witness WITH its actual F49 grade,
rather than grade alone. The equality is certified and
retains the exact original 1-path endpoints in the type. -/
structure C60F50OriginalTwoWithGrade
    {a b : IcosahedralDart} (p q : Quiver.Path a b) where
  original : C60F42PresentedFaceCell p q
  nativeGrade : GrayGrade
  nativeGrade_eq : nativeGrade = c60F49OriginalFaceTwo original

/-- Every original F42 2-cell has its canonical faithfully
decorated source object. No proof-relevant input is erased. -/
def c60F50OriginalDecoratedOf
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    C60F50OriginalTwoWithGrade p q :=
  ⟨α, c60F49OriginalFaceTwo α, rfl⟩

theorem c60F50OriginalDecoratedOf_injective
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b} :
    Function.Injective
      (c60F50OriginalDecoratedOf
        (p := p) (q := q)) := by
  intro α β h
  exact congrArg C60F50OriginalTwoWithGrade.original h

/-- Recover the EXACT input source face 2-cell with no
quotient on its original proof witness. -/
theorem c60F50OriginalDecoratedOf_original
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    (c60F50OriginalDecoratedOf α).original = α := rfl

/-- Every decorated original source object is uniquely
determined by its stored ORIGINAL F42 proof-relevant term. -/
theorem c60F50OriginalDecoratedOf_roundtrip
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    (X : C60F50OriginalTwoWithGrade p q) :
    c60F50OriginalDecoratedOf X.original = X := by
  cases X with
  | mk original nativeGrade nativeGrade_eq =>
      cases nativeGrade_eq
      rfl

/-! Original source 3-Hom category on original source 2-cell objects -/

/-- This is the ORIGINAL F44 source categorical 3-Hom,
not the larger unrestricted grade-only Gray 3-Hom. -/
instance c60F50OriginalDecoratedThreeHomCategory
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b} :
    Category (C60F50OriginalTwoWithGrade p q) where
  Hom X Y := C60F44FaceThreeHom X.original Y.original
  id X := c60F44FaceThreeOf (.ident X.original)
  comp := c60F44FaceThreeComp
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

/-- The genuine ORIGINAL face 2-cell source is recovered by a
Mathlib functor with identity on the full original 3-Homs. -/
def c60F50DecoratedForgetFunctor
    {a b : IcosahedralDart} (p q : Quiver.Path a b) :
    C60F50OriginalTwoWithGrade p q ⥤
      C60F42PresentedFaceCell p q where
  obj X := X.original
  map := fun {_ _} f => f
  map_id := by intro X; rfl
  map_comp := by intro X Y Z f g; rfl

/-- Every original F42 source 2-cell is embedded as a
genuinely decorated 2-cell, with exactly its original F43
higher morphisms, through a Mathlib source functor. -/
def c60F50OriginalToDecoratedFunctor
    {a b : IcosahedralDart} (p q : Quiver.Path a b) :
    C60F42PresentedFaceCell p q ⥤
      C60F50OriginalTwoWithGrade p q where
  obj α := c60F50OriginalDecoratedOf α
  map := fun {_ _} f => f
  map_id := by intro α; rfl
  map_comp := by intro α β γ f g; rfl

/-- Original source object witnesses are restored EXACTLY by
the round-trip of the two genuine Mathlib functors. -/
theorem c60F50OriginalSourceFunctor_objectRoundtrip
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    (c60F50DecoratedForgetFunctor p q).obj
      ((c60F50OriginalToDecoratedFunctor p q).obj α) = α := rfl

/-- Original decorated source objects are also recovered
EXACTLY in the opposite direction. The source 2-cell syntax
is not overwritten by the F49 graded output. -/
theorem c60F50DecoratedSourceFunctor_objectRoundtrip
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    (X : C60F50OriginalTwoWithGrade p q) :
    (c60F50OriginalToDecoratedFunctor p q).obj
      ((c60F50DecoratedForgetFunctor p q).obj X) = X :=
  c60F50OriginalDecoratedOf_roundtrip X

/-- Every original higher source arrow is recovered in the
forgetful direction: categorical fullness on F43/F44
3-Homs is a literal, type-checked witness. -/
theorem c60F50DecoratedForget_full
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {X Y : C60F50OriginalTwoWithGrade p q}
    (f : X.original ⟶ Y.original) :
    ∃ g : X ⟶ Y,
      (c60F50DecoratedForgetFunctor p q).map g = f :=
  ⟨f, rfl⟩

theorem c60F50DecoratedForget_faithful
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {X Y : C60F50OriginalTwoWithGrade p q}
    {f g : X ⟶ Y}
    (h : (c60F50DecoratedForgetFunctor p q).map f =
      (c60F50DecoratedForgetFunctor p q).map g) : f = g :=
  h

/-! Actual original-decorated source to the F49 graded 3-Hom -/

/-- Full original proof-relevant source category, then the
faithful morphism-wise Gray 3-Hom lift from F50 Stage I. -/
def c60F50DecoratedOriginalToGrayFunctor
    {a b : IcosahedralDart} (p q : Quiver.Path a b) :
    C60F50OriginalTwoWithGrade p q ⥤ C60F49Two p q :=
  c60F50DecoratedForgetFunctor p q ⋙
    c60F50OriginalFaceTypedThreeHomFunctor p q

theorem c60F50DecoratedOriginalToGrayFunctor_obj
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (X : C60F50OriginalTwoWithGrade p q) :
    (c60F50DecoratedOriginalToGrayFunctor p q).obj X =
      X.nativeGrade :=
  X.nativeGrade_eq.symm

theorem c60F50DecoratedOriginalToGrayFunctor_faithful
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {X Y : C60F50OriginalTwoWithGrade p q}
    {f g : X ⟶ Y}
    (h : (c60F50DecoratedOriginalToGrayFunctor p q).map f =
      (c60F50DecoratedOriginalToGrayFunctor p q).map g) :
    f = g := by
  exact c60F50OriginalFaceTypedThreeHomFunctor_faithful h

/-- The TWO ACTUAL ORIGINAL north-pentagon F42
horizontal-pasting witnesses stay DISTINCT in our decorated
SOURCE, although their native grade-only images coincide. -/
theorem c60F50NorthDecoratedTwoOrders_distinct :
    c60F50OriginalDecoratedOf
      (c60F43NorthPentagonFaceTwoCell.horizontalLeftFirst
        c60F43NorthPentagonFaceTwoCell) ≠
    c60F50OriginalDecoratedOf
      (c60F43NorthPentagonFaceTwoCell.horizontalRightFirst
        c60F43NorthPentagonFaceTwoCell) := by
  intro h
  exact c60F50OriginalNorthTwoPastingOrders_distinct
    (c60F50OriginalDecoratedOf_injective h)

#print axioms c60F50OriginalDecoratedOf_injective
#print axioms c60F50OriginalDecoratedOf_roundtrip
#print axioms c60F50OriginalDecoratedThreeHomCategory
#print axioms c60F50DecoratedForgetFunctor
#print axioms c60F50OriginalToDecoratedFunctor
#print axioms c60F50OriginalSourceFunctor_objectRoundtrip
#print axioms c60F50DecoratedSourceFunctor_objectRoundtrip
#print axioms c60F50DecoratedForget_full
#print axioms c60F50DecoratedForget_faithful
#print axioms c60F50DecoratedOriginalToGrayFunctor_faithful
#print axioms c60F50NorthDecoratedTwoOrders_distinct

end
end KUOS.DependentOriginationGrayC60OriginalFaceDecoratedThreeHomV5_198
