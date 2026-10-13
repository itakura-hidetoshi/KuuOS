import KUOS.DependentOriginationC60OriginalStrictThreeArrowsV5_227

namespace KUOS.DependentOriginationC60OriginalSourceInterchangerNaturalityV5_228

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199
open KUOS.DependentOriginationC60OriginalStrictThreeArrowsV5_227

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.228 / F74 — original source F43 interchange as a genuine NATURAL ISOMORPHISM

F73 established STRICT VERTICAL three-arrow Hom categories for actual
F42/F43 original 2-cell witnesses and independent mixed F54/F55 original
rotation boundaries. We now construct a new ORIGINAL-SOURCE THREE-ARROW
coherence result, with no Gray replacement of source arrows:

* An explicitly presented INVERSE of every original F43 interchange
  in the F51 correctly typed complete-native-kernel quotient.
* A true source-level original horizontal interchange Iso between the
  two DIFFERENT original F42 horizontal 2-cell pasting orders.
* A new ORIGINAL right-first horizontal three-arrow FUNCTOR, obtained
  by transporting the already original left-first horizontal functor
  across those correctly typed source F43 isomorphisms.
* An authentic Mathlib NatIso between the two source horizontal
  functors; its naturality is a three-arrow equality in the ORIGINAL
  F51 source quotient, not an equality of Gray charges.
* A physical north C60 pentagon specialization whose ORIGINAL F43
  interchange has INDEPENDENT nonzero ZMod2 phase.

The interchange is NONIDENTITY at the north pentagon; its inverse is
NOT constructed by setting the original two different F42 source
words definitionally equal. The right-first horizontal functor here
is the explicitly specified INTERCHANGER-CONJUGATED extension, not a
claim of independently primitive right-first source raw syntax.

Strict category laws hold INSIDE each correctly indexed 3-Hom
source category. Nontrivial Gray exchange is retained one dimension
higher, so no unsupported fully strict 3-category is asserted.
-/

/-! ## 1. A truly typed inverse to each ORIGINAL F43 source interchange -/

/-- Genuine original F43 inverse source THREE-ARROW with EXACT
right-first and left-first F42 2-cell endpoints. -/
def c60F74OriginalInterchangerInverse
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F51OriginalTwo p q)
    (Y : C60F51OriginalTwo r s) :
    c60F51OriginalTwoHorizontalRight X Y ⟶
      c60F51OriginalTwoHorizontal X Y :=
  c60F51Of
    (.symm (.original
      (.interchange X.original Y.original)))

/-- The original F43 source interchange followed by the
original reverse F43 three-arrow equals the genuine source
identity IN THE TYPED F51 QUOTIENT, without erasing source types. -/
theorem c60F74OriginalInterchanger_hom_inv_id
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F51OriginalTwo p q)
    (Y : C60F51OriginalTwo r s) :
    c60F51OriginalInterchanger X Y ≫
      c60F74OriginalInterchangerInverse X Y =
    𝟙 (c60F51OriginalTwoHorizontal X Y) := by
  apply Quot.sound
  change
    c60F43PhysicalInterchangerNative X.original Y.original +
      -(c60F43PhysicalInterchangerNative X.original Y.original) =
        (0 : GradedThreeCell 0 0)
  exact add_neg_cancel _

/-- The inverse-FIRST original source exchange is also exactly
the identity on the independent RIGHT-first F42 source word. -/
theorem c60F74OriginalInterchanger_inv_hom_id
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F51OriginalTwo p q)
    (Y : C60F51OriginalTwo r s) :
    c60F74OriginalInterchangerInverse X Y ≫
      c60F51OriginalInterchanger X Y =
    𝟙 (c60F51OriginalTwoHorizontalRight X Y) := by
  apply Quot.sound
  change
    -(c60F43PhysicalInterchangerNative X.original Y.original) +
      c60F43PhysicalInterchangerNative X.original Y.original =
        (0 : GradedThreeCell 0 0)
  exact neg_add_cancel _

/-- A genuine Mathlib source-three-Hom ISO from one
original F42 horizontal pasting order to the other. -/
def c60F74OriginalInterchangerIso
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F51OriginalTwo p q)
    (Y : C60F51OriginalTwo r s) :
    c60F51OriginalTwoHorizontal X Y ≅
      c60F51OriginalTwoHorizontalRight X Y where
  hom := c60F51OriginalInterchanger X Y
  inv := c60F74OriginalInterchangerInverse X Y
  hom_inv_id := c60F74OriginalInterchanger_hom_inv_id X Y
  inv_hom_id := c60F74OriginalInterchanger_inv_hom_id X Y

/-! ## 2. Strict original RIGHT-first source horizontal three-arrow functor -/

/-- Transport a real ORIGINAL horizontal source three-arrow
to RIGHT-first F42 pasting via ACTUAL ORIGINAL F43 source
interchanger arrows. This creates a TYPED source 3-arrow,
NOT a Gray-grade computation or invented C60 physical square. -/
def c60F74OriginalRightHorizontalMap
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F51OriginalTwoHorizontalRight X Y ⟶
      c60F51OriginalTwoHorizontalRight X' Y' :=
  (c60F74OriginalInterchangerIso X Y).inv ≫
    c60F51HorizontalMap f g ≫
    (c60F74OriginalInterchangerIso X' Y').hom

/-- A genuinely constructed Mathlib FUNCTOR for the
RIGHT-first ORIGINAL F42 source 2-cell pasting order.
The source retains both ORIGINAL F42 witness objects and
the actual F43 plus horizontal 3-arrow words. -/
def c60F74OriginalRightHorizontalThreeHomFunctor
    {a b c : IcosahedralDart}
    (p q : Quiver.Path a b)
    (r s : Quiver.Path b c) :
    (C60F51OriginalTwo p q × C60F51OriginalTwo r s) ⥤
      C60F51OriginalTwo (p.comp r) (q.comp s) where
  obj Z := c60F51OriginalTwoHorizontalRight Z.1 Z.2
  map := fun {X Y} f => c60F74OriginalRightHorizontalMap f.1 f.2
  map_id := by
    intro X
    change
      (c60F74OriginalInterchangerIso X.1 X.2).inv ≫
        c60F51HorizontalMap (𝟙 X.1) (𝟙 X.2) ≫
        (c60F74OriginalInterchangerIso X.1 X.2).hom =
      𝟙 (c60F51OriginalTwoHorizontalRight X.1 X.2)
    have hm :=
      (c60F51HorizontalThreeHomFunctor p q r s).map_id X
    change
      c60F51HorizontalMap (𝟙 X.1) (𝟙 X.2) =
        𝟙 (c60F51OriginalTwoHorizontal X.1 X.2) at hm
    rw [hm]
    simp
  map_comp := by
    intro X Y Z f g
    change
      (c60F74OriginalInterchangerIso X.1 X.2).inv ≫
        c60F51HorizontalMap (f.1 ≫ g.1) (f.2 ≫ g.2) ≫
        (c60F74OriginalInterchangerIso Z.1 Z.2).hom =
      ((c60F74OriginalInterchangerIso X.1 X.2).inv ≫
          c60F51HorizontalMap f.1 f.2 ≫
          (c60F74OriginalInterchangerIso Y.1 Y.2).hom) ≫
        ((c60F74OriginalInterchangerIso Y.1 Y.2).inv ≫
          c60F51HorizontalMap g.1 g.2 ≫
          (c60F74OriginalInterchangerIso Z.1 Z.2).hom)
    have hm :=
      (c60F51HorizontalThreeHomFunctor p q r s).map_comp f g
    change
      c60F51HorizontalMap (f.1 ≫ g.1) (f.2 ≫ g.2) =
        c60F51HorizontalMap f.1 f.2 ≫
          c60F51HorizontalMap g.1 g.2 at hm
    rw [hm]
    simp [Category.assoc]

/-! ## 3. True ORIGINAL-SOURCE F43 interchange NATURALITY -/

/-- The ORIGINAL F43 source interchanger is natural with respect
to EVERY pair of properly typed ORIGINAL F51 source three-arrows.
It is a native Mathlib NATURAL ISOMORPHISM between two genuine
original source 3-Hom horizontal composition functors. -/
def c60F74OriginalInterchangerNatIso
    {a b c : IcosahedralDart}
    (p q : Quiver.Path a b)
    (r s : Quiver.Path b c) :
    c60F51HorizontalThreeHomFunctor p q r s ≅
      c60F74OriginalRightHorizontalThreeHomFunctor p q r s :=
  NatIso.ofComponents
    (fun Z => c60F74OriginalInterchangerIso Z.1 Z.2)
    (by
      intro X Y f
      change
        c60F51HorizontalMap f.1 f.2 ≫
          (c60F74OriginalInterchangerIso Y.1 Y.2).hom =
        (c60F74OriginalInterchangerIso X.1 X.2).hom ≫
          ((c60F74OriginalInterchangerIso X.1 X.2).inv ≫
            c60F51HorizontalMap f.1 f.2 ≫
            (c60F74OriginalInterchangerIso Y.1 Y.2).hom)
      simp)

/-- The source NATURALITY SQUARE explicitly written as an
equality between two different PASTINGS of genuine original
F43 and original horizontal F51 source three-arrows. -/
theorem c60F74OriginalInterchanger_sourceNaturality
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F51HorizontalMap f g ≫
      c60F51OriginalInterchanger X' Y' =
    c60F51OriginalInterchanger X Y ≫
      c60F74OriginalRightHorizontalMap f g := by
  exact
    (c60F74OriginalInterchangerNatIso p q r s).hom.naturality
      ((f, g) : (X, Y) ⟶ (X', Y'))

/-- A direct specialization to ACTUAL original F42/F43
source words (rather than arbitrary native-grade arrows).
The source inclusion on each side is the original F43/F44
faithful original-source injection. -/
theorem c60F74OriginalF43Interchanger_sourceNaturality
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {α α' : C60F42PresentedFaceCell p q}
    {β β' : C60F42PresentedFaceCell r s}
    (f : α ⟶ α') (g : β ⟶ β') :
    c60F51HorizontalMap
        ((c60F51OriginalInclusion p q).map f)
        ((c60F51OriginalInclusion r s).map g) ≫
      c60F51OriginalInterchanger ⟨α'⟩ ⟨β'⟩ =
    c60F51OriginalInterchanger ⟨α⟩ ⟨β⟩ ≫
      c60F74OriginalRightHorizontalMap
        ((c60F51OriginalInclusion p q).map f)
        ((c60F51OriginalInclusion r s).map g) :=
  c60F74OriginalInterchanger_sourceNaturality
    ((c60F51OriginalInclusion p q).map f)
    ((c60F51OriginalInclusion r s).map g)

/-! ## 4. The ACTUAL north C60 pentagon has nonzero SOURCE exchange -/

/-- On the original north pentagon the HOM of the above
genuine original F43 source interchange ISO is EXACTLY the
old original F43 three-arrow, not a new Gray proxy. -/
theorem c60F74NorthOriginalInterchangerIso_isOriginalF43 :
    (c60F74OriginalInterchangerIso
      c60F51NorthFaceSourceTwo
      c60F51NorthFaceSourceTwo).hom =
        c60F73NorthOriginalStrictThreeInterchanger := rfl

/-- The genuinely typed original north C60 SOURCE ISO retains
the FULL nonzero independent exchange phase one. -/
theorem c60F74NorthOriginalInterchangerIso_phase_one :
    (c60F51Eval
      (c60F74OriginalInterchangerIso
        c60F51NorthFaceSourceTwo
        c60F51NorthFaceSourceTwo).hom).phase = (1 : ZMod 2) :=
  c60F73NorthOriginalStrictThree_phase_one

/-- The original interchange iso cannot be collapsed into
an identity Gray arrow (the two raw pasting endpoints are distinct
F42 source terms), even though it is an invertible source
three-arrow and enjoys genuine source naturality. -/
theorem c60F74NorthOriginalInterchangerIso_notNeutral :
    c60F51Eval
      (c60F74OriginalInterchangerIso
        c60F51NorthFaceSourceTwo
        c60F51NorthFaceSourceTwo).hom ≠
      (0 : GradedThreeCell 0 0) :=
  c60F73NorthOriginalStrictThree_noIdentityInterchange

#print axioms c60F74OriginalInterchangerInverse
#print axioms c60F74OriginalInterchanger_hom_inv_id
#print axioms c60F74OriginalInterchanger_inv_hom_id
#print axioms c60F74OriginalInterchangerIso
#print axioms c60F74OriginalRightHorizontalMap
#print axioms c60F74OriginalRightHorizontalThreeHomFunctor
#print axioms c60F74OriginalInterchangerNatIso
#print axioms c60F74OriginalInterchanger_sourceNaturality
#print axioms c60F74OriginalF43Interchanger_sourceNaturality
#print axioms c60F74NorthOriginalInterchangerIso_isOriginalF43
#print axioms c60F74NorthOriginalInterchangerIso_phase_one
#print axioms c60F74NorthOriginalInterchangerIso_notNeutral

end
end KUOS.DependentOriginationC60OriginalSourceInterchangerNaturalityV5_228
