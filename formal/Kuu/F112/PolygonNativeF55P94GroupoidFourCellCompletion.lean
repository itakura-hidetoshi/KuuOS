import Kuu.F112.PolygonNativeF55P94UnitFourQuotientHorizontalCategory
import Mathlib.CategoryTheory.Groupoid
import Mathlib.Tactic

/-!
# F112-P94C2 — genuine nonabelian groupoid completion of typed P92B 3-proofs

P94B proves a strict local Category and interchange for typed P92B
3-proof classes but does NOT supply the inverse cancellation four-cells
needed to make the declared formal `symm` into group-theoretic
inversion. Those are missing relations, not consequences of zero
numerical F55 charge.

This DISTINCT 4-cell presentation embeds every genuine P94A Type
witness, closes its dependent whiskers and horizontal contexts, and
adds TWO explicitly named reversible-3-proof relations:
  inverseLeft : symm(f);f => refl
  inverseRight: f;symm(f) => refl
The inverseCongr comparison is then DERIVED using group cancellation and
existing four-dimensional whiskering/associativity; it is NOT adjoined.

Prove every constructor preserves the entire signed F55 shadow,
take the proof-relevant quotient, construct a genuine Mathlib Groupoid
on original F54 route objects, and preserve the P94A category and
the actual C60 odd phase through the canonical surjection.

This is a selected nonabelian groupoid PRESENTATION, not a proof that
old P94A had inverse cancellation or that the missing four-dimensional
pentagonator coherence has been resolved. No Gray or new logical axioms.
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

inductive NativeF55P94GroupFourCell
    {p : Polygon} {a b : D} {x y : E} :
    ∀ {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last},
      NativeF55P92AssocComparison p r s →
      NativeF55P92AssocComparison p r s →
      Type (max (max uD uE) (max vD vE)) where
  | old
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94UnitFourCell f g) :
      NativeF55P94GroupFourCell f g
  | refl
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P94GroupFourCell f f
  | symm
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94GroupFourCell f g) :
      NativeF55P94GroupFourCell g f
  | trans
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : NativeF55P92AssocComparison p r s}
      (fg : NativeF55P94GroupFourCell f g)
      (gh : NativeF55P94GroupFourCell g h) :
      NativeF55P94GroupFourCell f h
  | verticalLeftUnit
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P94GroupFourCell (.trans (.refl r) f) f
  | verticalRightUnit
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P94GroupFourCell (.trans f (.refl s)) f
  | verticalAssoc
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t z : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s)
      (g : NativeF55P92AssocComparison p s t)
      (h : NativeF55P92AssocComparison p t z) :
      NativeF55P94GroupFourCell
        (.trans (.trans f g) h)
        (.trans f (.trans g h))
  | leftWhisker
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : NativeF55P92AssocComparison p r s)
      {f g : NativeF55P92AssocComparison p s t}
      (w : NativeF55P94GroupFourCell f g) :
      NativeF55P94GroupFourCell (.trans prior f) (.trans prior g)
  | rightWhisker
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94GroupFourCell f g)
      (suffix : NativeF55P92AssocComparison p s t) :
      NativeF55P94GroupFourCell (.trans f suffix) (.trans g suffix)
  | leftContext
      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94GroupFourCell f g)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P94GroupFourCell (.leftContext f later) (.leftContext g later)
  | rightContext
      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94GroupFourCell f g) :
      NativeF55P94GroupFourCell (.rightContext earlier f) (.rightContext earlier g)
  | precompose
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      (prior : KuuNativeF45Tree.DepthRotationRoute p first middle)
      {r s : KuuNativeF45Tree.DepthRotationRoute p middle last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94GroupFourCell f g) :
      NativeF55P94GroupFourCell
        (.precompose prior f) (.precompose prior g)
  | postcompose
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first middle}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94GroupFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
      NativeF55P94GroupFourCell
        (.postcompose f suffix) (.postcompose g suffix)
  | horizontalLeft
      {n n' m m' k k' l l' : Nat}
      {p₀ p₁ p₂ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ : KuuNativeBlocks x y}
      {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
      {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
      {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
      {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
      {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
      {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
      {f f' : NativeF55P92AssocComparison p u u'}
      (w : NativeF55P94GroupFourCell f f')
      (g : NativeF55P92AssocComparison p v v') :
      NativeF55P94GroupFourCell
        (f.horizontal g) (f'.horizontal g)
  | horizontalRight
      {n n' m m' k k' l l' : Nat}
      {p₀ p₁ p₂ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ : KuuNativeBlocks x y}
      {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
      {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
      {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
      {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
      {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
      {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
      (f : NativeF55P92AssocComparison p u u')
      {g g' : NativeF55P92AssocComparison p v v'}
      (w : NativeF55P94GroupFourCell g g') :
      NativeF55P94GroupFourCell
        (f.horizontal g) (f.horizontal g')
  | interchange
      {n n' m m' k k' l l' : Nat}
      {p₀ p₁ p₂ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ : KuuNativeBlocks x y}
      {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
      {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
      {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
      {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
      {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
      {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
      (f₁ : NativeF55P92AssocComparison p u₀ u₁)
      (f₂ : NativeF55P92AssocComparison p u₁ u₂)
      (g₁ : NativeF55P92AssocComparison p v₀ v₁)
      (g₂ : NativeF55P92AssocComparison p v₁ v₂) :
      NativeF55P94GroupFourCell
        ((NativeF55P92AssocComparison.trans f₁ f₂).horizontal
          (NativeF55P92AssocComparison.trans g₁ g₂))
        (NativeF55P92AssocComparison.trans
          (f₁.horizontal g₁) (f₂.horizontal g₂))



  | inverseLeft
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P94GroupFourCell (.trans (.symm f) f) (.refl s)
  | inverseRight
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P94GroupFourCell (.trans f (.symm f)) (.refl r)
/-- The nonabelian groupoid completion does NOT forget pentagon
integer, exchange square integer, or genuine C60 odd ZMod2 phase. -/
theorem NativeF55P94GroupFourCell.shadow_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94GroupFourCell f g) :
    f.nativeShadow = g.nativeShadow := by
  induction w with
  | old witness => exact witness.shadow_sound
  | refl cell => rfl
  | symm witness ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f => simp [NativeF55P92AssocComparison.nativeShadow]
  | verticalRightUnit f => simp [NativeF55P92AssocComparison.nativeShadow]
  | verticalAssoc f g h =>
      change (f.nativeShadow + g.nativeShadow) + h.nativeShadow =
        f.nativeShadow + (g.nativeShadow + h.nativeShadow)
      exact add_assoc _ _ _
  | leftWhisker prior witness ih =>
      exact congrArg
        (fun z : KuuNativeF55Shadow => prior.nativeShadow + z) ih
  | rightWhisker witness suffix ih =>
      exact congrArg
        (fun z : KuuNativeF55Shadow => z + suffix.nativeShadow) ih
  | leftContext witness later ih => exact ih
  | rightContext earlier witness ih => exact ih
  | precompose prior witness ih => exact ih
  | postcompose witness suffix ih => exact ih
  | horizontalLeft witness g ih =>
      simpa only [NativeF55P92AssocComparison.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => z + g.nativeShadow) ih
  | horizontalRight f witness ih =>
      simpa only [NativeF55P92AssocComparison.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => f.nativeShadow + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      change (f₁.nativeShadow + f₂.nativeShadow) +
          (g₁.nativeShadow + g₂.nativeShadow) =
        (f₁.nativeShadow + g₁.nativeShadow) +
          (f₂.nativeShadow + g₂.nativeShadow)
      abel
  | inverseLeft f =>
      change -f.nativeShadow + f.nativeShadow = 0
      exact neg_add_cancel _
  | inverseRight f =>
      change f.nativeShadow + (-f.nativeShadow) = 0
      exact add_neg_cancel _

/-- Inversion preserves equality of 3-proofs by a CONSTRUCTED
group-theoretic 4-pasting: its source compares
f⁻¹ → f⁻¹;(g;g⁻¹) → (f⁻¹;g);g⁻¹
→ (f⁻¹;f);g⁻¹ → id;g⁻¹ → g⁻¹.
No new inverse-congruence generator or Lean axiom is needed. -/
def NativeF55P94GroupFourCell.inverseCongr
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94GroupFourCell f g) :
    NativeF55P94GroupFourCell (.symm f) (.symm g) :=
  .trans
    (.symm
      (.trans
        (.leftWhisker (.symm f) (.inverseRight g))
        (.verticalRightUnit (.symm f))))
    (.trans
      (.symm (.verticalAssoc (.symm f) g (.symm g)))
      (.trans
        (.rightWhisker (.leftWhisker (.symm f) (.symm w)) (.symm g))
        (.trans
          (.rightWhisker (.inverseLeft f) (.symm g))
          (.verticalLeftUnit (.symm g)))))

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}

/-- Exact quotient of genuine 3-proofs by genuine new 4-proof existence. -/
def nativeF55P94GroupFourSetoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Setoid (NativeF55P92AssocComparison p r s) where
  r := fun f g => Nonempty (NativeF55P94GroupFourCell f g)
  iseqv := ⟨
    (fun f => ⟨.refl f⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun z => ⟨.trans w z⟩)))⟩

abbrev NativeF55P94GroupFourClasses
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :=
  _root_.Quotient (nativeF55P94GroupFourSetoid first last r s)

def nativeF55P94GroupFourClass
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    NativeF55P94GroupFourClasses first last r s :=
  _root_.Quotient.mk _ cell

/-- Exact Type-valued 4-cell kernel, not a charge equality shortcut. -/
theorem nativeF55P94GroupFourClass_eq_iff
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : NativeF55P92AssocComparison p r s) :
    nativeF55P94GroupFourClass first last f =
      nativeF55P94GroupFourClass first last g ↔
        Nonempty (NativeF55P94GroupFourCell f g) := by
  constructor
  · intro h
    exact _root_.Quotient.exact h
  · intro h
    exact _root_.Quotient.sound h

def nativeF55P94GroupFourToShadow
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P94GroupFourClasses first last r s → KuuNativeF55Shadow :=
  _root_.Quotient.lift
    (fun raw => raw.nativeShadow)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.shadow_sound)

/-- P94A embeds by terms; the new quotient is a documented
separate, potentially coarser groupoid-completion presentation. -/
def nativeF55P94UnitToGroupFour
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (q : NativeF55P94UnitFourClasses first last r s) :
    NativeF55P94GroupFourClasses first last r s :=
  Quot.liftOn q
    (fun raw => nativeF55P94GroupFourClass first last raw)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact Quot.sound ⟨NativeF55P94GroupFourCell.old w⟩)

theorem nativeF55P94UnitToGroupFour_surjective
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last} :
    Function.Surjective (nativeF55P94UnitToGroupFour first last
       (r := r) (s := s)) := by
  intro q
  refine Quot.inductionOn q (fun raw => ?_)
  exact ⟨nativeF55P94UnitFourClass first last raw, rfl⟩

/-- The new inversion operation on classes is well-defined by an
ACTUAL inverseCongr Type-valued four-cell. -/
def nativeF55P94GroupInverse
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P94GroupFourClasses first last r s) :
    NativeF55P94GroupFourClasses first last s r :=
  Quot.liftOn f
    (fun raw => nativeF55P94GroupFourClass first last (.symm raw))
    (by
      intro a b h
      rcases h with ⟨w⟩
      exact Quot.sound ⟨NativeF55P94GroupFourCell.inverseCongr w⟩)

def nativeF55P94GroupVerticalComp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P94GroupFourClasses first last u v)
    (g : NativeF55P94GroupFourClasses first last v w) :
    NativeF55P94GroupFourClasses first last u w :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P94GroupFourClass first last (.trans left right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨witness⟩
      exact ⟨NativeF55P94GroupFourCell.leftWhisker left witness⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨witness⟩
      exact ⟨NativeF55P94GroupFourCell.rightWhisker witness right⟩)

/-- True local strict vertical Mathlib Category on ORIGINAL F54
route objects with P92B proof-relevant 3-homs modulo P93C 4-cells.
The unit/associator laws are witnesses in the NEW four-cell source. -/
@[reducible] def nativeF55P94GroupVerticalCategory
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Category (KuuNativeF45Tree.DepthRotationRoute p first last) where
  Hom := NativeF55P94GroupFourClasses first last
  id route := nativeF55P94GroupFourClass first last (.refl route)
  comp f g := nativeF55P94GroupVerticalComp first last f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P94GroupFourClass first last (.trans (.refl X) raw) =
      nativeF55P94GroupFourClass first last raw
    exact Quot.sound ⟨NativeF55P94GroupFourCell.verticalLeftUnit raw⟩
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P94GroupFourClass first last (.trans raw (.refl Y)) =
      nativeF55P94GroupFourClass first last raw
    exact Quot.sound ⟨NativeF55P94GroupFourCell.verticalRightUnit raw⟩
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun a => ?_)
    refine Quot.inductionOn g (fun b => ?_)
    refine Quot.inductionOn h (fun c => ?_)
    change nativeF55P94GroupFourClass first last
        (.trans (.trans a b) c) =
      nativeF55P94GroupFourClass first last
        (.trans a (.trans b c))
    exact Quot.sound ⟨NativeF55P94GroupFourCell.verticalAssoc a b c⟩



/-- The inverse-cancellation 4-generators are sufficient to promote
the true proof-relevant P92B 3-cell category to a Mathlib Groupoid. -/
@[reducible] def nativeF55P94GroupoidCategory
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Groupoid (KuuNativeF45Tree.DepthRotationRoute p first last) where
  toCategory := nativeF55P94GroupVerticalCategory first last
  inv := by
    intro X Y f
    exact nativeF55P94GroupInverse first last f
  inv_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P94GroupFourClass first last
      (.trans (.symm raw) raw) =
        nativeF55P94GroupFourClass first last (.refl Y)
    exact Quot.sound ⟨NativeF55P94GroupFourCell.inverseLeft raw⟩
  comp_inv := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P94GroupFourClass first last
      (.trans raw (.symm raw)) =
        nativeF55P94GroupFourClass first last (.refl X)
    exact Quot.sound ⟨NativeF55P94GroupFourCell.inverseRight raw⟩

/-- Explicit nonabelian reverse/pasting cancellation on genuine typed
P92B original-route witnesses: a source-level 4-cell, not a shadow. -/
def nativeF55P94Group_original_pentagon_inverse_cancel
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    NativeF55P94GroupFourCell
      (.trans
        (NativeF55P92AssocComparison.original (.pentagon t₁ t₂ t₃ t₄))
        (.symm (NativeF55P92AssocComparison.original (.pentagon t₁ t₂ t₃ t₄))))
      (.refl (KuuNativeF45Tree.DepthRotationRoute.pentagonLong
          t₁ t₂ t₃ t₄)) :=
  .inverseRight _

/-- The groupoid completion cannot contract a genuine closed
P92B 3-proof carrying nonzero odd C60 phase to the identity:
the obstruction follows from the actual FOUR-witness shadow theorem. -/
theorem nativeF55P94Group_odd_phase_no_null_fourCell
    {r : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r r)
    (hodd : f.nativeShadow.2 ≠ (0 : ZMod 2)) :
    ¬ Nonempty (NativeF55P94GroupFourCell f (.refl r)) := by
  rintro ⟨w⟩
  have hs := congrArg (fun sh : KuuNativeF55Shadow => sh.2) w.shadow_sound
  change f.nativeShadow.2 = (0 : ZMod 2) at hs
  exact hodd hs

/-- Three cyclically composable odd-phase 3-proofs leave one unit of
odd phase, even in the newly established genuine groupoid. This is
a conditional typed obstruction relevant to the THREE square faces
of K5; it does NOT assume those global K5 face whiskers are constructed. -/
theorem nativeF55P94Group_three_odd_square_phase_obstruction
    {r₀ r₁ r₂ : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r₀ r₁)
    (g : NativeF55P92AssocComparison p r₁ r₂)
    (h : NativeF55P92AssocComparison p r₂ r₀)
    (hf : f.nativeShadow.2 = (1 : ZMod 2))
    (hg : g.nativeShadow.2 = (1 : ZMod 2))
    (hh : h.nativeShadow.2 = (1 : ZMod 2)) :
    ¬ Nonempty (NativeF55P94GroupFourCell (.trans (.trans f g) h) (.refl r₀)) := by
  rintro ⟨w⟩
  have hs := congrArg (fun sh : KuuNativeF55Shadow => sh.2) w.shadow_sound
  change (f.nativeShadow.2 + g.nativeShadow.2) + h.nativeShadow.2 =
    (0 : ZMod 2) at hs
  rw [hf, hg, hh] at hs
  exact (by decide : ((1 : ZMod 2) + 1) + 1 ≠ 0) hs

/-- The physically genuine C60 source disjoint-square cell used in
the preceding obstruction retains its original odd phase. -/
theorem northHexagonNativeF55P94Group_original_square_odd_phase :
    (NativeF55P92AssocComparison.original
       northHexagonNativeF55SquareCell).nativeShadow.2 ≠ (0 : ZMod 2) := by
  change northHexagonNativeF55SquareCell.nativeShadow.2 ≠ (0 : ZMod 2)
  exact northHexagonNativeF55SquareCell_phase_nonzero

#print axioms NativeF55P94GroupFourCell
#print axioms NativeF55P94GroupFourCell.shadow_sound
#print axioms NativeF55P94GroupFourCell.inverseCongr
#print axioms nativeF55P94GroupFourSetoid
#print axioms NativeF55P94GroupFourClasses
#print axioms nativeF55P94GroupFourClass_eq_iff
#print axioms nativeF55P94GroupFourToShadow
#print axioms nativeF55P94UnitToGroupFour
#print axioms nativeF55P94UnitToGroupFour_surjective
#print axioms nativeF55P94GroupInverse
#print axioms nativeF55P94GroupVerticalComp
#print axioms nativeF55P94GroupVerticalCategory
#print axioms nativeF55P94GroupoidCategory
#print axioms nativeF55P94Group_original_pentagon_inverse_cancel
#print axioms nativeF55P94Group_odd_phase_no_null_fourCell
#print axioms nativeF55P94Group_three_odd_square_phase_obstruction
#print axioms northHexagonNativeF55P94Group_original_square_odd_phase

end
end Kuu.F112.Physical
