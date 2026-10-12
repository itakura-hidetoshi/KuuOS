import KUOS.DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199

namespace KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.200 / F59-F52-A: source-relevant associator and unit comparisons

The original F42 proof witnesses are NOT identified under reassociation.
Every rebracketing of actual C60 source and target paths is mediated by
the proved Quiver.Path.comp_assoc, nil_comp and comp_nil equalities.
We explicitly ADJOIN typed, zero-native-charge associator and unitor
3-morphism generators; these are not incorrectly attributed to F43.
All F51 original and horizontally/vertically adjoined 3-words remain
embedded in the expanded F52 source syntax. The complete F59 native
integer-pair charge and independent ZMod2 phase are retained.
-/

/-- Change both genuine original source 1-path indices by proved
equalities, without identifying two distinct F42 2-cell terms. -/
def c60F52ReindexFace
    {a b : IcosahedralDart}
    {p q p' q' : Quiver.Path a b}
    (hp : p = p') (hq : q = q')
    (α : C60F42PresentedFaceCell p q) :
    C60F42PresentedFaceCell p' q' := by
  cases hp
  cases hq
  exact α

theorem c60F52ReindexFace_degree
    {a b : IcosahedralDart}
    {p q p' q' : Quiver.Path a b}
    (hp : p = p') (hq : q = q')
    (α : C60F42PresentedFaceCell p q) :
    c60F43FaceDegree (c60F52ReindexFace hp hq α) =
      c60F43FaceDegree α := by
  cases hp
  cases hq
  rfl

/-- Right-associated, original F42 horizontal 2-cell witness, now
reindexed to the LEFT-associated physical C60 path boundaries.
The raw proof term remains the right-associated proof witness. -/
def c60F52AssocRight
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b}
    {r s : Quiver.Path b c}
    {t u : Quiver.Path c d}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u) :
    C60F42PresentedFaceCell
      ((p.comp r).comp t) ((q.comp s).comp u) :=
  c60F52ReindexFace
    (Quiver.Path.comp_assoc p r t).symm
    (Quiver.Path.comp_assoc q s u).symm
    (α.horizontalLeftFirst (β.horizontalLeftFirst γ))

theorem c60F52AssocRight_degree
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b}
    {r s : Quiver.Path b c}
    {t u : Quiver.Path c d}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u) :
    c60F43FaceDegree (c60F52AssocRight α β γ) =
      c60F43FaceDegree α +
        (c60F43FaceDegree β + c60F43FaceDegree γ) := by
  simp only [c60F52AssocRight, c60F52ReindexFace_degree,
    c60F43FaceDegree_horizontalLeftFirst]

/-- The LEFT unit comparison begins at a genuine original F42
left-first horizontal proof with the empty C60 path, reindexed
via Quiver.Path.nil_comp rather than a fake definitional cast. -/
def c60F52LeftUnitSource
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    C60F42PresentedFaceCell p q :=
  c60F52ReindexFace
    (Quiver.Path.nil_comp p) (Quiver.Path.nil_comp q)
    ((C60F42PresentedFaceCell.ident
      (Quiver.Path.nil : Quiver.Path a a)).horizontalLeftFirst α)

def c60F52RightUnitSource
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    C60F42PresentedFaceCell p q :=
  c60F52ReindexFace
    (Quiver.Path.comp_nil p) (Quiver.Path.comp_nil q)
    (α.horizontalLeftFirst
      (C60F42PresentedFaceCell.ident
        (Quiver.Path.nil : Quiver.Path b b)))

theorem c60F52LeftUnitSource_degree
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    c60F43FaceDegree (c60F52LeftUnitSource α) =
      c60F43FaceDegree α := by
  simp only [c60F52LeftUnitSource, c60F52ReindexFace_degree,
    c60F43FaceDegree_horizontalLeftFirst,
    c60F43FaceDegree_ident, zero_add]

theorem c60F52RightUnitSource_degree
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    c60F43FaceDegree (c60F52RightUnitSource α) =
      c60F43FaceDegree α := by
  simp only [c60F52RightUnitSource, c60F52ReindexFace_degree,
    c60F43FaceDegree_horizontalLeftFirst,
    c60F43FaceDegree_ident, add_zero]

/-- F52 extends F51 syntax by THREE expressly ADJOINED comparison
families. Neither associator nor either unitor is claimed to be
an original F43 or F55 primitive. Their exact F42 endpoints
are retained, including two independent path reassociations. -/
inductive C60F52PresentedThreeCell :
    {a b : IcosahedralDart} →
    {p q : Quiver.Path a b} →
    C60F42PresentedFaceCell p q →
    C60F42PresentedFaceCell p q → Type where
  | ofF51 {a b : IcosahedralDart} {p q : Quiver.Path a b}
      {α β : C60F42PresentedFaceCell p q}
      (f : C60F51PresentedThreeCell α β) :
      C60F52PresentedThreeCell α β
  | ident {a b : IcosahedralDart} {p q : Quiver.Path a b}
      (α : C60F42PresentedFaceCell p q) :
      C60F52PresentedThreeCell α α
  | symm {a b : IcosahedralDart} {p q : Quiver.Path a b}
      {α β : C60F42PresentedFaceCell p q}
      (f : C60F52PresentedThreeCell α β) :
      C60F52PresentedThreeCell β α
  | trans {a b : IcosahedralDart} {p q : Quiver.Path a b}
      {α β γ : C60F42PresentedFaceCell p q}
      (f : C60F52PresentedThreeCell α β)
      (g : C60F52PresentedThreeCell β γ) :
      C60F52PresentedThreeCell α γ
  | horizontal {a b c : IcosahedralDart}
      {p q : Quiver.Path a b} {r s : Quiver.Path b c}
      {α α' : C60F42PresentedFaceCell p q}
      {β β' : C60F42PresentedFaceCell r s}
      (f : C60F52PresentedThreeCell α α')
      (g : C60F52PresentedThreeCell β β') :
      C60F52PresentedThreeCell
        (α.horizontalLeftFirst β)
        (α'.horizontalLeftFirst β')
  | vertical {a b : IcosahedralDart}
      {p q r : Quiver.Path a b}
      {α α' : C60F42PresentedFaceCell p q}
      {β β' : C60F42PresentedFaceCell q r}
      (f : C60F52PresentedThreeCell α α')
      (g : C60F52PresentedThreeCell β β') :
      C60F52PresentedThreeCell
        (.trans α β) (.trans α' β')
  | whiskerLeft {a b c : IcosahedralDart}
      (prior : Quiver.Path a b)
      {p q : Quiver.Path b c}
      {α β : C60F42PresentedFaceCell p q}
      (f : C60F52PresentedThreeCell α β) :
      C60F52PresentedThreeCell
        (.whiskerLeft prior α) (.whiskerLeft prior β)
  | whiskerRight {a b c : IcosahedralDart}
      {p q : Quiver.Path a b}
      {α β : C60F42PresentedFaceCell p q}
      (f : C60F52PresentedThreeCell α β)
      (suffix : Quiver.Path b c) :
      C60F52PresentedThreeCell
        (.whiskerRight α suffix) (.whiskerRight β suffix)
  | reindex {a b : IcosahedralDart}
      {p q p' q' : Quiver.Path a b}
      (hp : p = p') (hq : q = q')
      {α β : C60F42PresentedFaceCell p q}
      (f : C60F52PresentedThreeCell α β) :
      C60F52PresentedThreeCell
        (c60F52ReindexFace hp hq α)
        (c60F52ReindexFace hp hq β)
  | associator {a b c d : IcosahedralDart}
      {p q : Quiver.Path a b} {r s : Quiver.Path b c}
      {t u : Quiver.Path c d}
      (α : C60F42PresentedFaceCell p q)
      (β : C60F42PresentedFaceCell r s)
      (γ : C60F42PresentedFaceCell t u) :
      C60F52PresentedThreeCell
        ((α.horizontalLeftFirst β).horizontalLeftFirst γ)
        (c60F52AssocRight α β γ)
  | leftUnitor {a b : IcosahedralDart}
      {p q : Quiver.Path a b}
      (α : C60F42PresentedFaceCell p q) :
      C60F52PresentedThreeCell (c60F52LeftUnitSource α) α
  | rightUnitor {a b : IcosahedralDart}
      {p q : Quiver.Path a b}
      (α : C60F42PresentedFaceCell p q) :
      C60F52PresentedThreeCell (c60F52RightUnitSource α) α

/-- Complete new source-word evaluation, with no loss of either
integer charge or the independent braided exchange phase. -/
def C60F52PresentedThreeCell.toNative
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : C60F52PresentedThreeCell α β) :
    GradedThreeCell 0 0 := by
  induction f with
  | ofF51 f => exact f.toNative
  | ident _ => exact 0
  | symm f ih => exact -ih
  | trans f g ihf ihg => exact ihf + ihg
  | horizontal f g ihf ihg => exact ihf + ihg
  | vertical f g ihf ihg => exact ihf + ihg
  | whiskerLeft prior f ih => exact ih
  | whiskerRight f suffix ih => exact ih
  | reindex hp hq f ih => exact ih
  | associator α β γ => exact 0
  | leftUnitor α => exact 0
  | rightUnitor α => exact 0

theorem C60F52PresentedThreeCell.preservesFaceDegree
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : C60F52PresentedThreeCell α β) :
    c60F43FaceDegree α = c60F43FaceDegree β := by
  induction f with
  | ofF51 f => exact f.preservesFaceDegree
  | ident _ => rfl
  | symm f ih => exact ih.symm
  | trans f g ihf ihg => exact ihf.trans ihg
  | horizontal f g ihf ihg =>
      rw [c60F43FaceDegree_horizontalLeftFirst,
        c60F43FaceDegree_horizontalLeftFirst, ihf, ihg]
  | vertical f g ihf ihg =>
      rw [c60F43FaceDegree_trans, c60F43FaceDegree_trans, ihf, ihg]
  | whiskerLeft prior f ih => exact ih
  | whiskerRight f suffix ih => exact ih
  | reindex hp hq f ih =>
      simpa only [c60F52ReindexFace_degree] using ih
  | associator α β γ =>
      simp only [c60F43FaceDegree_horizontalLeftFirst,
        c60F52AssocRight_degree, add_assoc]
  | leftUnitor α => exact c60F52LeftUnitSource_degree α
  | rightUnitor α => exact c60F52RightUnitSource_degree α

theorem c60F52Associator_native
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u) :
    (C60F52PresentedThreeCell.associator α β γ).toNative =
      (0 : GradedThreeCell 0 0) := rfl

theorem c60F52LeftUnitor_native
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    (C60F52PresentedThreeCell.leftUnitor α).toNative =
      (0 : GradedThreeCell 0 0) := rfl

theorem c60F52RightUnitor_native
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    (C60F52PresentedThreeCell.rightUnitor α).toNative =
      (0 : GradedThreeCell 0 0) := rfl

#print axioms c60F52ReindexFace_degree
#print axioms c60F52AssocRight_degree
#print axioms c60F52LeftUnitSource_degree
#print axioms c60F52RightUnitSource_degree
#print axioms C60F52PresentedThreeCell.preservesFaceDegree
#print axioms c60F52Associator_native
#print axioms c60F52LeftUnitor_native
#print axioms c60F52RightUnitor_native

end
end KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200
