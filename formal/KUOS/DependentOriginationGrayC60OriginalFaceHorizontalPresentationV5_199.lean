import KUOS.DependentOriginationGrayC60OriginalAllNinetyF55FaceLiftV5_198

namespace KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
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
# v5.199 / F59-F51-A — honest horizontal original-face 3-cell presentation

The original F42 2-cell objects are proof-relevant and indexed by
ACTUAL C60 source and target 1-paths. Original F43 3-cell
generators provide identities, interchangers, inverses, vertical
pasting and two 1-path whiskerings, but not a constructor for
HORIZONTAL composition of arbitrary *3-morphism pairs*.

We therefore ADJOIN a genuinely NEW proof-relevant horizontal
3-cell constructor, and separately a vertical 2-context constructor.
Both have exact F42 source/target 2-cell boundaries. Original
F43 3-cell witnesses are included as distinct tagged generators.
The raw syntax also contains typed 3-cell identity, composition,
inversion and actual C60 1-path left/right whiskering.

The complete native F59 evaluation is recursively assigned to all
new generators, retaining BOTH Int integer charges and separate
ZMod2 exchange phase. Degree preservation is proved by structural
induction on ALL constructors using existing F43 source theorems.
These are additions to the ORIGINAL presentation, not a false
claim that the old F43 grammar already had horizontal 3-composition.

The source 2-cell wrapper makes the new category's object type
DIFFERENT from the existing F44/F50 categories, so independent
category structures do not conflict in Lean's typeclass inference.
-/

/-- A fresh wrapper around a genuine ORIGINAL F42 face 2-cell:
the exact dependent C60 1-path indices and raw 2-cell witness
are retained, not reduced to its ZMod2 grade. -/
structure C60F51OriginalTwo {a b : IcosahedralDart}
    (p q : Quiver.Path a b) where
  original : C60F42PresentedFaceCell p q

def c60F51OriginalTwoOf
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    C60F51OriginalTwo p q := ⟨α⟩

theorem c60F51OriginalTwoOf_injective
    {a b : IcosahedralDart} {p q : Quiver.Path a b} :
    Function.Injective
      (c60F51OriginalTwoOf (p := p) (q := q)) := by
  intro α β h
  exact congrArg C60F51OriginalTwo.original h

/-- The original face 2-cell vertical composite preserves the
original p→q→r C60 path boundaries, with NO free-source collapse. -/
def c60F51OriginalTwoVertical
    {a b : IcosahedralDart} {p q r : Quiver.Path a b}
    (α : C60F51OriginalTwo p q) (β : C60F51OriginalTwo q r) :
    C60F51OriginalTwo p r :=
  ⟨.trans α.original β.original⟩

/-- The actual F42 left-first original horizontal two-cell
pasting, with its *original* two C60 1-path boundaries. -/
def c60F51OriginalTwoHorizontal
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F51OriginalTwo p q)
    (β : C60F51OriginalTwo r s) :
    C60F51OriginalTwo (p.comp r) (q.comp s) :=
  ⟨α.original.horizontalLeftFirst β.original⟩

/-- The independent right-first original horizontal 2-cell
term is retained, not identified with left-first raw syntax. -/
def c60F51OriginalTwoHorizontalRight
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F51OriginalTwo p q)
    (β : C60F51OriginalTwo r s) :
    C60F51OriginalTwo (p.comp r) (q.comp s) :=
  ⟨α.original.horizontalRightFirst β.original⟩

/-- New ORIGINAL-source-aware horizontal three-cell words.
Every constructor is indexed by ACTUAL original F42 face
2-cell boundary witnesses, not just by their parity degree. -/
inductive C60F51PresentedThreeCell :
    {a b : IcosahedralDart} →
    {p q : Quiver.Path a b} →
    C60F42PresentedFaceCell p q →
    C60F42PresentedFaceCell p q → Type where
  | ident {a b : IcosahedralDart} {p q : Quiver.Path a b}
      (α : C60F42PresentedFaceCell p q) :
      C60F51PresentedThreeCell α α
  | original {a b : IcosahedralDart} {p q : Quiver.Path a b}
      {α β : C60F42PresentedFaceCell p q}
      (f : C60F43PresentedThreeCell α β) :
      C60F51PresentedThreeCell α β
  | symm {a b : IcosahedralDart} {p q : Quiver.Path a b}
      {α β : C60F42PresentedFaceCell p q}
      (f : C60F51PresentedThreeCell α β) :
      C60F51PresentedThreeCell β α
  | trans {a b : IcosahedralDart} {p q : Quiver.Path a b}
      {α β γ : C60F42PresentedFaceCell p q}
      (f : C60F51PresentedThreeCell α β)
      (g : C60F51PresentedThreeCell β γ) :
      C60F51PresentedThreeCell α γ
  | horizontal {a b c : IcosahedralDart}
      {p q : Quiver.Path a b} {r s : Quiver.Path b c}
      {α α' : C60F42PresentedFaceCell p q}
      {β β' : C60F42PresentedFaceCell r s}
      (f : C60F51PresentedThreeCell α α')
      (g : C60F51PresentedThreeCell β β') :
      C60F51PresentedThreeCell
        (α.horizontalLeftFirst β)
        (α'.horizontalLeftFirst β')
  | vertical {a b : IcosahedralDart}
      {p q r : Quiver.Path a b}
      {α α' : C60F42PresentedFaceCell p q}
      {β β' : C60F42PresentedFaceCell q r}
      (f : C60F51PresentedThreeCell α α')
      (g : C60F51PresentedThreeCell β β') :
      C60F51PresentedThreeCell
        (.trans α β) (.trans α' β')
  | whiskerLeft {a b c : IcosahedralDart}
      (prior : Quiver.Path a b)
      {p q : Quiver.Path b c}
      {α β : C60F42PresentedFaceCell p q}
      (f : C60F51PresentedThreeCell α β) :
      C60F51PresentedThreeCell
        (.whiskerLeft prior α) (.whiskerLeft prior β)
  | whiskerRight {a b c : IcosahedralDart}
      {p q : Quiver.Path a b}
      {α β : C60F42PresentedFaceCell p q}
      (f : C60F51PresentedThreeCell α β)
      (suffix : Quiver.Path b c) :
      C60F51PresentedThreeCell
        (.whiskerRight α suffix) (.whiskerRight β suffix)

/-- Complete recursive native realization of EVERY original
and adjoined 3-cell constructor. New 2-context/horizontal
composites add BOTH original Int charges and the genuine
independent exchange phase in the existing F59 target. -/
def C60F51PresentedThreeCell.toNative
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : C60F51PresentedThreeCell α β) :
    GradedThreeCell 0 0 := by
  induction f with
  | ident _ => exact 0
  | original f => exact f.toNative
  | symm f ih => exact -ih
  | trans f g ihf ihg => exact ihf + ihg
  | horizontal f g ihf ihg => exact ihf + ihg
  | vertical f g ihf ihg => exact ihf + ihg
  | whiskerLeft prior f ih => exact ih
  | whiskerRight f suffix ih => exact ih

/-- Genuine source grade invariant over ALL horizontal,
vertical, inverse and 1-path contextual 3-cell generators.
This supplies exact source/target grades for the F49 lift. -/
theorem C60F51PresentedThreeCell.preservesFaceDegree
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : C60F51PresentedThreeCell α β) :
    c60F43FaceDegree α = c60F43FaceDegree β := by
  induction f with
  | ident _ => rfl
  | original f => exact f.preservesFaceDegree
  | symm f ih => exact ih.symm
  | trans f g ihf ihg => exact ihf.trans ihg
  | horizontal f g ihf ihg =>
      rw [c60F43FaceDegree_horizontalLeftFirst,
        c60F43FaceDegree_horizontalLeftFirst, ihf, ihg]
  | vertical f g ihf ihg =>
      rw [c60F43FaceDegree_trans, c60F43FaceDegree_trans, ihf, ihg]
  | whiskerLeft prior f ih => exact ih
  | whiskerRight f suffix ih => exact ih

/-- Every new horizontal original-source 3-cell constructor
has the exact target sum of the original F59 Int×Int charge
and independent ZMod2 braided Gray phase. -/
theorem C60F51PresentedThreeCell.horizontal_toNative
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {α α' : C60F42PresentedFaceCell p q}
    {β β' : C60F42PresentedFaceCell r s}
    (f : C60F51PresentedThreeCell α α')
    (g : C60F51PresentedThreeCell β β') :
    (C60F51PresentedThreeCell.horizontal f g).toNative =
      f.toNative + g.toNative := rfl

theorem C60F51PresentedThreeCell.vertical_toNative
    {a b : IcosahedralDart} {p q r : Quiver.Path a b}
    {α α' : C60F42PresentedFaceCell p q}
    {β β' : C60F42PresentedFaceCell q r}
    (f : C60F51PresentedThreeCell α α')
    (g : C60F51PresentedThreeCell β β') :
    (C60F51PresentedThreeCell.vertical f g).toNative =
      f.toNative + g.toNative := rfl

#print axioms C60F51PresentedThreeCell.preservesFaceDegree
#print axioms C60F51PresentedThreeCell.horizontal_toNative
#print axioms C60F51PresentedThreeCell.vertical_toNative
#print axioms c60F51OriginalTwoOf_injective

end
end KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
