import Kuu.F112.PolygonNativeF55P93AssocFourCellCoherence
import Mathlib.Tactic

/-!
# F112-P93D — full Type-valued P92B 3-proof four-quotient strict interchange

P93C adjoined clearly named genuine NEW 4-cell generators, preserving
full signed F55 charge and true odd ZMod2 phase through all constructors.
Here those exact Type-evidence witnesses, NOT numerical shadow equality,
supply the quotient congruence needed for strict 3-proof vertical Mathlib
Category and real binary horizontal P92B four-class pasting.
We prove strict horizontal/vertical interchange for FOUR ARBITRARY
new P92B 4-cell quotient classes, including associator-naturality
certificates adjoined in P92B.

We also exhibit exactly why the old original-F55 P89 four-proof slot
is EMPTY for three true original unit routes while P93C's new
P92B-3-proof-indexed quotient has an actual element. This is NOT a
retraction of P92A's no-go.

The new 4-generators are stated, audited presentation choices, NOT
old P89 derivations. The horizontal identity, full 4-dimensional
associator pentagonator/pasting coherence and global strict 3/n
remain separate obligations. No Gray, sorry, new logical axioms or
alteration to 107 public roots.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55P92AssocComparison p u v}

def nativeF55P93VerticalComp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P93AssocFourClasses first last u v)
    (g : NativeF55P93AssocFourClasses first last v w) :
    NativeF55P93AssocFourClasses first last u w :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P93AssocFourClass first last (.trans left right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨witness⟩
      exact ⟨NativeF55P93AssocFourCell.leftWhisker left witness⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨witness⟩
      exact ⟨NativeF55P93AssocFourCell.rightWhisker witness right⟩)

/-- True local strict vertical Mathlib Category on ORIGINAL F54
route objects with P92B proof-relevant 3-homs modulo P93C 4-cells.
The unit/associator laws are witnesses in the NEW four-cell source. -/
@[reducible] def nativeF55P93VerticalCategory
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Category (KuuNativeF45Tree.DepthRotationRoute p first last) where
  Hom := NativeF55P93AssocFourClasses first last
  id route := nativeF55P93AssocFourClass first last (.refl route)
  comp f g := nativeF55P93VerticalComp first last f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P93AssocFourClass first last (.trans (.refl X) raw) =
      nativeF55P93AssocFourClass first last raw
    exact Quot.sound ⟨NativeF55P93AssocFourCell.verticalLeftUnit raw⟩
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P93AssocFourClass first last (.trans raw (.refl Y)) =
      nativeF55P93AssocFourClass first last raw
    exact Quot.sound ⟨NativeF55P93AssocFourCell.verticalRightUnit raw⟩
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun a => ?_)
    refine Quot.inductionOn g (fun b => ?_)
    refine Quot.inductionOn h (fun c => ?_)
    change nativeF55P93AssocFourClass first last
        (.trans (.trans a b) c) =
      nativeF55P93AssocFourClass first last
        (.trans a (.trans b c))
    exact Quot.sound ⟨NativeF55P93AssocFourCell.verticalAssoc a b c⟩

/-- The new full shadow remains vertically additive on arbitrary
true P92B 4-class representatives. -/
theorem nativeF55P93VerticalShadow_comp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P93AssocFourClasses first last r s)
    (g : NativeF55P93AssocFourClasses first last s t) :
    nativeF55P93AssocFourToShadow first last r t
      (nativeF55P93VerticalComp first last f g) =
    nativeF55P93AssocFourToShadow first last r s f +
      nativeF55P93AssocFourToShadow first last s t g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

def nativeF55P93Horizontal
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P93AssocFourClasses leftBefore leftAfter r r')
    (g : NativeF55P93AssocFourClasses rightBefore rightAfter s s') :
    NativeF55P93AssocFourClasses
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (.trans (.leftContext r rightBefore) (.rightContext leftAfter s))
      (.trans (.leftContext r' rightBefore) (.rightContext leftAfter s')) :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P93AssocFourClass _ _ (left.horizontal right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨w⟩
      exact ⟨NativeF55P93AssocFourCell.horizontalRight left w⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨w⟩
      exact ⟨NativeF55P93AssocFourCell.horizontalLeft w right⟩)

/-- P92B×P92B→P93C binary operation computes on the SAME original
F54 route-typed NEW P92B 3-proofs, not a shadow replacement. -/
@[simp] theorem nativeF55P93Horizontal_raw
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P92AssocComparison p r r')
    (g : NativeF55P92AssocComparison p s s') :
    nativeF55P93Horizontal
      (nativeF55P93AssocFourClass leftBefore leftAfter f)
      (nativeF55P93AssocFourClass rightBefore rightAfter g) =
    nativeF55P93AssocFourClass _ _ (f.horizontal g) := rfl



/-- The complete signed F55 shadow of a two-sided horizontal
pasting computes additively on arbitrary NEW P93C quotient classes.
This is a preservation theorem, not proof of interchange. -/
theorem nativeF55P93Horizontal_shadow
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P93AssocFourClasses leftBefore leftAfter r r')
    (g : NativeF55P93AssocFourClasses rightBefore rightAfter s s') :
    nativeF55P93AssocFourToShadow _ _ _ _
      (nativeF55P93Horizontal f g) =
      nativeF55P93AssocFourToShadow _ _ _ _ f +
        nativeF55P93AssocFourToShadow _ _ _ _ g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- Strict interchange for FOUR ARBITRARY typed P93C quotient classes:
horizontal preserves vertical pasting as equality in the SAME P93C
quotient. This is the strict bifunctoriality part of the local
higher structure, not yet the entire globular strict 3-category. -/
theorem nativeF55P93_interchange
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : NativeF55P93AssocFourClasses leftBefore leftAfter u₀ u₁)
    (f₂ : NativeF55P93AssocFourClasses leftBefore leftAfter u₁ u₂)
    (g₁ : NativeF55P93AssocFourClasses rightBefore rightAfter v₀ v₁)
    (g₂ : NativeF55P93AssocFourClasses rightBefore rightAfter v₁ v₂) :
    nativeF55P93Horizontal
      (nativeF55P93VerticalComp leftBefore leftAfter f₁ f₂)
      (nativeF55P93VerticalComp rightBefore rightAfter g₁ g₂) =
    nativeF55P93VerticalComp
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (nativeF55P93Horizontal f₁ g₁)
      (nativeF55P93Horizontal f₂ g₂) := by
  refine Quot.inductionOn f₁ (fun a => ?_)
  refine Quot.inductionOn f₂ (fun b => ?_)
  refine Quot.inductionOn g₁ (fun c => ?_)
  refine Quot.inductionOn g₂ (fun d => ?_)
  change nativeF55P93AssocFourClass _ _
      ((NativeF55P92AssocComparison.trans a b).horizontal
        (NativeF55P92AssocComparison.trans c d)) =
    nativeF55P93AssocFourClass _ _
      (NativeF55P92AssocComparison.trans
        (a.horizontal c) (b.horizontal d))
  exact Quot.sound ⟨NativeF55P93AssocFourCell.interchange a b c d⟩

/-- The genuine P89 original-four-class quotient maps into
P93C FOUR-class space only when its OLD raw 3-proof exists.
This is not asserted to be surjective: new P92B 3-cells have
newly populated hom slots absent from original F55. -/
def nativeF55P93OldP89FourToAssoc
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (q : NativeF55P89FourClasses first last r s) :
    NativeF55P93AssocFourClasses first last r s :=
  Quot.liftOn q
    (fun raw =>
      nativeF55P93AssocFourClass first last
        (NativeF55P92AssocComparison.original raw))
    (by
      intro raw₁ raw₂ h
      rcases h with ⟨old⟩
      exact Quot.sound ⟨NativeF55P93AssocFourCell.old old⟩)

/-- Original 4-class inclusion preserves exact original pentagon,
square and odd ZMod2 phase for every source original F55 3-proof. -/
theorem nativeF55P93OldP89FourToAssoc_shadow
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (q : NativeF55P89FourClasses first last r s) :
    nativeF55P93AssocFourToShadow first last r s
      (nativeF55P93OldP89FourToAssoc first last q) =
    nativeF55P89FourToShadow first last r s q := by
  refine Quot.inductionOn q (fun raw => ?_)
  rfl

/-- For any three authentic original F45 unit histories the original
P89 FOUR-proof quotient has NO element: there is not even an
original P92A F55 3-proof between the mixed-bracketing paths.
The distinct P93C quotient HAS an element through the explicitly
NEW P92B associator-naturality 3-cell, without imposing false
equality in old F55 or P89. -/
theorem nativeF55P93AssocFour_new_not_old_unit
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (¬ Nonempty (NativeF55P89FourClasses
      (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
      (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃))
      (nativeF54P90AssocNaturalityLeftRoute
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃))
      (nativeF54P90AssocNaturalityRightRoute
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃)))) ∧
    Nonempty (NativeF55P93AssocFourClasses
      (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
      (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃))
      (nativeF54P90AssocNaturalityLeftRoute
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃))
      (nativeF54P90AssocNaturalityRightRoute
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃))) := by
  constructor
  · rintro ⟨oldClass⟩
    refine Quot.inductionOn oldClass (fun raw => ?_)
    exact (nativeF55P92_original_unit_naturality_no_filler t₁ t₂ t₃) ⟨raw⟩
  · exact ⟨nativeF55P93AssocFourClass _ _
      (NativeF55P92AssocComparison.assocNaturality
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃))⟩

/-- The genuine north C60 stages specifically witness that P93C
has a nonempty new-four-class slot while old P89 is empty. -/
theorem northNativeF55P93AssocFour_new_not_old_unit :
    (¬ Nonempty (NativeF55P89FourClasses
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node
          northNativeF45FirstStage northNativeF45SecondStage)
        northNativeF45ThirdStage)
      (KuuNativeF45Tree.node northNativeF45FirstStage
        (KuuNativeF45Tree.node
          northNativeF45SecondStage northNativeF45ThirdStage))
      (nativeF54P90AssocNaturalityLeftRoute
        (nativeF54P92UnitRoute northNativeF45FirstStage)
        (nativeF54P92UnitRoute northNativeF45SecondStage)
        (nativeF54P92UnitRoute northNativeF45ThirdStage))
      (nativeF54P90AssocNaturalityRightRoute
        (nativeF54P92UnitRoute northNativeF45FirstStage)
        (nativeF54P92UnitRoute northNativeF45SecondStage)
        (nativeF54P92UnitRoute northNativeF45ThirdStage)))) ∧
    Nonempty (NativeF55P93AssocFourClasses
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node
          northNativeF45FirstStage northNativeF45SecondStage)
        northNativeF45ThirdStage)
      (KuuNativeF45Tree.node northNativeF45FirstStage
        (KuuNativeF45Tree.node
          northNativeF45SecondStage northNativeF45ThirdStage))
      (nativeF54P90AssocNaturalityLeftRoute
        (nativeF54P92UnitRoute northNativeF45FirstStage)
        (nativeF54P92UnitRoute northNativeF45SecondStage)
        (nativeF54P92UnitRoute northNativeF45ThirdStage))
      (nativeF54P90AssocNaturalityRightRoute
        (nativeF54P92UnitRoute northNativeF45FirstStage)
        (nativeF54P92UnitRoute northNativeF45SecondStage)
        (nativeF54P92UnitRoute northNativeF45ThirdStage))) :=
  nativeF55P93AssocFour_new_not_old_unit
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage

#print axioms nativeF55P93VerticalComp
#print axioms nativeF55P93VerticalCategory
#print axioms nativeF55P93VerticalShadow_comp
#print axioms nativeF55P93Horizontal
#print axioms nativeF55P93Horizontal_raw
#print axioms nativeF55P93Horizontal_shadow
#print axioms nativeF55P93_interchange
#print axioms nativeF55P93OldP89FourToAssoc
#print axioms nativeF55P93OldP89FourToAssoc_shadow
#print axioms nativeF55P93AssocFour_new_not_old_unit
#print axioms northNativeF55P93AssocFour_new_not_old_unit

end
end Kuu.F112.Physical
