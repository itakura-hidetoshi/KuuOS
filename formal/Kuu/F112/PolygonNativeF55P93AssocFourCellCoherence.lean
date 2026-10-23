import Kuu.F112.PolygonNativeF55P93OriginalToAssocNonfaithfulness
import Kuu.F112.PolygonNativeF55P89InterchangeFourCell
import Mathlib.Tactic

/-!
# F112-P93C — independently declared proof-relevant P92B 4-cell coherence

The P92B Type-valued 3-cell presentation genuinely contains the explicit
associator-naturality generator, NOT derivable in original F55 (P92A).
The P89 4-cell was indexed by ORIGINAL F55 3-cell witnesses and hence does
not automatically apply to new P92B 3-cell histories.

Define a DISTINCT 4-cell source indexed by pairs of actual P92B 3-proofs.
Old P89 comparisons are retained through the honest original inclusion.
New explicitly named 4-cell generators control vertical source 3-proof
units/associativity and horizontal-vertical interchange for arbitrary
P92B 3-proofs, INCLUDING the newly adjoined associator naturality.
Close recursively under 3-proof vertical whiskering, both true F45
binary contexts, true F54 route pre/post, and both horizontal whiskers.

This is NOT a deduction that the original 4-cell syntax already contained
the missing coherence. These genuinely new generators are CHOICES of
presentation; full signed pentagon/square charge and odd C60 phase must
be shown invariant through *every* constructor.

The genuine witness-existence quotient will have an exact Type kernel
and a full-shadow projection. It does not declare all 4-dimensional
pentagonators/associator naturality pasting constraints automatically.
No Gray, no new Lean axioms or changes to historical proof sources.
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

/-- True P92B-3-proof-indexed FOUR cell; the new generators below
are explicit, and old P89 4-cells embed only via original F55. -/
inductive NativeF55P93AssocFourCell
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
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (w : NativeF55P89InterchangeFourCell f g) :
      NativeF55P93AssocFourCell (.original f) (.original g)
  | refl
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P93AssocFourCell f f
  | symm
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P93AssocFourCell f g) :
      NativeF55P93AssocFourCell g f
  | trans
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : NativeF55P92AssocComparison p r s}
      (fg : NativeF55P93AssocFourCell f g)
      (gh : NativeF55P93AssocFourCell g h) :
      NativeF55P93AssocFourCell f h
  | verticalLeftUnit
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P93AssocFourCell (.trans (.refl r) f) f
  | verticalRightUnit
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P93AssocFourCell (.trans f (.refl s)) f
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
      NativeF55P93AssocFourCell
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
      (w : NativeF55P93AssocFourCell f g) :
      NativeF55P93AssocFourCell (.trans prior f) (.trans prior g)
  | rightWhisker
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P93AssocFourCell f g)
      (suffix : NativeF55P92AssocComparison p s t) :
      NativeF55P93AssocFourCell (.trans f suffix) (.trans g suffix)
  | leftContext
      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P93AssocFourCell f g)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P93AssocFourCell (.leftContext f later) (.leftContext g later)
  | rightContext
      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P93AssocFourCell f g) :
      NativeF55P93AssocFourCell (.rightContext earlier f) (.rightContext earlier g)
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
      (w : NativeF55P93AssocFourCell f g) :
      NativeF55P93AssocFourCell
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
      (w : NativeF55P93AssocFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
      NativeF55P93AssocFourCell
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
      (w : NativeF55P93AssocFourCell f f')
      (g : NativeF55P92AssocComparison p v v') :
      NativeF55P93AssocFourCell
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
      (w : NativeF55P93AssocFourCell g g') :
      NativeF55P93AssocFourCell
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
      NativeF55P93AssocFourCell
        ((NativeF55P92AssocComparison.trans f₁ f₂).horizontal
          (NativeF55P92AssocComparison.trans g₁ g₂))
        (NativeF55P92AssocComparison.trans
          (f₁.horizontal g₁) (f₂.horizontal g₂))

/-- Every P93C 4-cell comparison preserves *all three* signed
shadow coordinates (pentagon, square, odd ZMod2), inductively. -/
theorem NativeF55P93AssocFourCell.shadow_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) :
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
      -- Native shadow is compiled to a dependent recursor; use
      -- congrArg, not rw on syntactically reduced recursive terms.
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

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55P92AssocComparison p r s}

/-- New proof-relevant four-cell witness-existence relation. -/
def nativeF55P93AssocFourSetoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Setoid (NativeF55P92AssocComparison p r s) where
  r := fun f g => Nonempty (NativeF55P93AssocFourCell f g)
  iseqv := ⟨
    (fun f => ⟨.refl f⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun z => ⟨.trans w z⟩)))⟩

abbrev NativeF55P93AssocFourClasses
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :=
  _root_.Quotient (nativeF55P93AssocFourSetoid first last r s)

def nativeF55P93AssocFourClass
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    NativeF55P93AssocFourClasses first last r s :=
  _root_.Quotient.mk _ cell

/-- Exact source Type kernel, not shadow equality or route-object equality. -/
theorem nativeF55P93AssocFourClass_eq_iff
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : NativeF55P92AssocComparison p r s) :
    nativeF55P93AssocFourClass first last f =
      nativeF55P93AssocFourClass first last g ↔
        Nonempty (NativeF55P93AssocFourCell f g) := by
  constructor
  · intro h
    exact _root_.Quotient.exact h
  · intro h
    exact _root_.Quotient.sound h

/-- Full signed pentagon/square/odd-phase shadow descends through
the P93C 4-cell quotient by actual proof-relevant soundness. -/
def nativeF55P93AssocFourToShadow
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P93AssocFourClasses first last r s → KuuNativeF55Shadow :=
  _root_.Quotient.lift
    (fun raw => raw.nativeShadow)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.shadow_sound)

/-- Every original P89 4-cell remains genuinely present after both
inclusions; no new equality is attributed to the original source. -/
theorem nativeF55P93_oldFourCell_lifts
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55P89InterchangeFourCell f g) :
    Nonempty (NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) :=
  ⟨.old w⟩

/-- Source 4-cell exists for arbitrary NEW associator-naturality
proof histories mixed into a true F54 horizontal interchange.
This is a NEW, clearly chosen 4-generator, not a P89 consequence. -/
theorem nativeF55P93Assoc_interchange_witness
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    {r₀ r₁ r₂ : KuuNativeF45Tree.DepthRotationRoute p first last}
    {s₀ s₁ s₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : NativeF55P92AssocComparison p r₀ r₁)
    (f₂ : NativeF55P92AssocComparison p r₁ r₂)
    (g₁ : NativeF55P92AssocComparison p s₀ s₁)
    (g₂ : NativeF55P92AssocComparison p s₁ s₂) :
    Nonempty (NativeF55P93AssocFourCell
      ((NativeF55P92AssocComparison.trans f₁ f₂).horizontal
        (NativeF55P92AssocComparison.trans g₁ g₂))
      (NativeF55P92AssocComparison.trans
        (f₁.horizontal g₁) (f₂.horizontal g₂))) :=
  ⟨.interchange f₁ f₂ g₁ g₂⟩

#print axioms NativeF55P93AssocFourCell
#print axioms NativeF55P93AssocFourCell.shadow_sound
#print axioms nativeF55P93AssocFourSetoid
#print axioms NativeF55P93AssocFourClasses
#print axioms nativeF55P93AssocFourClass_eq_iff
#print axioms nativeF55P93AssocFourToShadow
#print axioms nativeF55P93_oldFourCell_lifts
#print axioms nativeF55P93Assoc_interchange_witness

end
end Kuu.F112.Physical
