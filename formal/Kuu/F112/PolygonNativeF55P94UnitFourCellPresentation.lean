import Kuu.F112.PolygonNativeF55P93FourQuotientStrictInterchange
import Mathlib.Tactic

/-!
# F112-P94A — independently declared horizontal and context unit 4-cell presentation

P79 proves the older path-equality-sound source four-cell relation cannot
identify the two genuine horizontal F55 identity proofs. P93D builds
true P92B-3-proof vertical Mathlib Category and strict interchange
on an explicit P93C 4-cell presentation, but does not prove that its
horizontal operation maps a pair of identity 3-cells to the identity
at their genuine original F54 horizontal route.

This NEW Type-valued P94A four-cell presentation includes ALL P93C
evidence via an explicit `old` generator, and adjoins only THREE
clearly declared structural unit generators:
- horizontalUnit: P92B.refl(u) horizontally P92B.refl(v) versus
  P92B.refl(the genuinely composed original F54 route).
- leftContextUnit and rightContextUnit: contextualized P92B.refl
  versus P92B.refl of the original contexted F54 route.

All existing 4-cell operations are recursively reclosed in THIS new
proof-relevant presentation (rather than changing original F55/P93C).
Full signed F55 pentagon/square charges and the C60 odd ZMod2 phase
are conserved for every constructor. This source choice is NOT
a derivation in P77 or the prior P93C syntax, nor a claim of all
pentagonator / global strict 3/n coherence. C60 remains a testbed.
No Gray, sorry/admit or added logical axioms.
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

/-- New four-cell evidence language over genuine P92B 3-proofs;
previous P93C proofs embed faithfully as terms, never identified
with the old P77 path-sound syntax. -/
inductive NativeF55P94UnitFourCell
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
      (w : NativeF55P93AssocFourCell f g) :
      NativeF55P94UnitFourCell f g
  | refl
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P94UnitFourCell f f
  | symm
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94UnitFourCell f g) :
      NativeF55P94UnitFourCell g f
  | trans
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : NativeF55P92AssocComparison p r s}
      (fg : NativeF55P94UnitFourCell f g)
      (gh : NativeF55P94UnitFourCell g h) :
      NativeF55P94UnitFourCell f h
  | verticalLeftUnit
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P94UnitFourCell (.trans (.refl r) f) f
  | verticalRightUnit
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P94UnitFourCell (.trans f (.refl s)) f
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
      NativeF55P94UnitFourCell
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
      (w : NativeF55P94UnitFourCell f g) :
      NativeF55P94UnitFourCell (.trans prior f) (.trans prior g)
  | rightWhisker
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94UnitFourCell f g)
      (suffix : NativeF55P92AssocComparison p s t) :
      NativeF55P94UnitFourCell (.trans f suffix) (.trans g suffix)
  | leftContext
      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94UnitFourCell f g)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P94UnitFourCell (.leftContext f later) (.leftContext g later)
  | rightContext
      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94UnitFourCell f g) :
      NativeF55P94UnitFourCell (.rightContext earlier f) (.rightContext earlier g)
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
      (w : NativeF55P94UnitFourCell f g) :
      NativeF55P94UnitFourCell
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
      (w : NativeF55P94UnitFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
      NativeF55P94UnitFourCell
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
      (w : NativeF55P94UnitFourCell f f')
      (g : NativeF55P92AssocComparison p v v') :
      NativeF55P94UnitFourCell
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
      (w : NativeF55P94UnitFourCell g g') :
      NativeF55P94UnitFourCell
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
      NativeF55P94UnitFourCell
        ((NativeF55P92AssocComparison.trans f₁ f₂).horizontal
          (NativeF55P92AssocComparison.trans g₁ g₂))
        (NativeF55P92AssocComparison.trans
          (f₁.horizontal g₁) (f₂.horizontal g₂))

  | horizontalUnit
      {n n' m m' k k' l l' : Nat}
      {p₀ p₁ p₂ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ : KuuNativeBlocks x y}
      {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
      {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
      {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
      {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
      (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
      (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
      NativeF55P94UnitFourCell
        ((NativeF55P92AssocComparison.refl u).horizontal
          (NativeF55P92AssocComparison.refl v))
        (NativeF55P92AssocComparison.refl
          (nativeF54P90HorizontalRoute u v))
  | leftContextUnit
      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      (route : KuuNativeF45Tree.DepthRotationRoute p first last)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.leftContext (.refl route) later)
        (NativeF55P92AssocComparison.refl (.leftContext route later))
  | rightContextUnit
      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
      NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.rightContext earlier (.refl route))
        (NativeF55P92AssocComparison.refl (.rightContext earlier route))

/-- Every P93C 4-cell comparison preserves *all three* signed
shadow coordinates (pentagon, square, odd ZMod2), inductively. -/
theorem NativeF55P94UnitFourCell.shadow_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) :
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
  | horizontalUnit u v =>
      change (0 : KuuNativeF55Shadow) + 0 = 0
      simp
  | leftContextUnit route later => rfl
  | rightContextUnit earlier route => rfl

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55P92AssocComparison p r s}

/-- New proof-relevant four-cell witness-existence relation. -/
def nativeF55P94UnitFourSetoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Setoid (NativeF55P92AssocComparison p r s) where
  r := fun f g => Nonempty (NativeF55P94UnitFourCell f g)
  iseqv := ⟨
    (fun f => ⟨.refl f⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun z => ⟨.trans w z⟩)))⟩

abbrev NativeF55P94UnitFourClasses
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :=
  _root_.Quotient (nativeF55P94UnitFourSetoid first last r s)

def nativeF55P94UnitFourClass
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    NativeF55P94UnitFourClasses first last r s :=
  _root_.Quotient.mk _ cell

/-- Exact source Type kernel, not shadow equality or route-object equality. -/
theorem nativeF55P94UnitFourClass_eq_iff
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : NativeF55P92AssocComparison p r s) :
    nativeF55P94UnitFourClass first last f =
      nativeF55P94UnitFourClass first last g ↔
        Nonempty (NativeF55P94UnitFourCell f g) := by
  constructor
  · intro h
    exact _root_.Quotient.exact h
  · intro h
    exact _root_.Quotient.sound h

/-- Full signed pentagon/square/odd-phase shadow descends through
the P93C 4-cell quotient by actual proof-relevant soundness. -/
def nativeF55P94UnitFourToShadow
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P94UnitFourClasses first last r s → KuuNativeF55Shadow :=
  _root_.Quotient.lift
    (fun raw => raw.nativeShadow)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.shadow_sound)

/-- Canonical map from the exact P93C 4-proof quotient to
new P94A 4-proof quotient, retaining each ORIGINAL raw P92B proof. -/
def nativeF55P93ToP94UnitFour
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (q : NativeF55P93AssocFourClasses first last r s) :
    NativeF55P94UnitFourClasses first last r s :=
  Quot.liftOn q
    (fun raw => nativeF55P94UnitFourClass first last raw)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact Quot.sound ⟨NativeF55P94UnitFourCell.old w⟩)

/-- The new 4-proof quotient preserves the entire P93C proof-term
image and is surjectively covered by it; no old witness is erased. -/
theorem nativeF55P93ToP94UnitFour_surjective
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last} :
    Function.Surjective (nativeF55P93ToP94UnitFour first last (r := r) (s := s)) := by
  intro q
  refine Quot.inductionOn q (fun raw => ?_)
  exact ⟨nativeF55P93AssocFourClass first last raw, rfl⟩

/-- Genuine horizontal unit equality on original F54 routes,
generated by a visibly NEW Type-valued P94A four-cell witness. -/
theorem nativeF55P94HorizontalUnit_new_class_eq
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    nativeF55P94UnitFourClass
      (KuuNativeF45Tree.node first rightBefore)
      (KuuNativeF45Tree.node last rightAfter)
      ((NativeF55P92AssocComparison.refl u).horizontal
        (NativeF55P92AssocComparison.refl v)) =
    nativeF55P94UnitFourClass
      (KuuNativeF45Tree.node first rightBefore)
      (KuuNativeF45Tree.node last rightAfter)
      (NativeF55P92AssocComparison.refl
        (nativeF54P90HorizontalRoute u v)) :=
  Quot.sound ⟨NativeF55P94UnitFourCell.horizontalUnit u v⟩

/-- The genuine chosen horizontal unit generator has complete
zero shadow; unlike new 4-cell existence, zero charge was already
a necessary condition supplied by the original F55 semantics. -/
theorem nativeF55P94HorizontalUnit_shadow_eq
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    ((NativeF55P92AssocComparison.refl u).horizontal
      (NativeF55P92AssocComparison.refl v)).nativeShadow =
    (NativeF55P92AssocComparison.refl
      (nativeF54P90HorizontalRoute u v)).nativeShadow :=
  (NativeF55P94UnitFourCell.horizontalUnit u v).shadow_sound

/-- Genuine C60 pair of independent physical six-sector F54
associators has an actual new horizontal identity four-certificate.
P79 proves its ORIGINAL P77 analogue is impossible, as retained. -/
theorem northHexagonNativeF55P94HorizontalUnit_new_witness :
    Nonempty (NativeF55P94UnitFourCell
      ((NativeF55P92AssocComparison.refl northHexagonNativeLeftF54UnitRoute).horizontal
        (NativeF55P92AssocComparison.refl northHexagonNativeRightF54UnitRoute))
      (NativeF55P92AssocComparison.refl
        (nativeF54P90HorizontalRoute
          northHexagonNativeLeftF54UnitRoute
          northHexagonNativeRightF54UnitRoute))) :=
  ⟨.horizontalUnit
    northHexagonNativeLeftF54UnitRoute
    northHexagonNativeRightF54UnitRoute⟩

#print axioms NativeF55P94UnitFourCell
#print axioms NativeF55P94UnitFourCell.shadow_sound
#print axioms nativeF55P94UnitFourSetoid
#print axioms NativeF55P94UnitFourClasses
#print axioms nativeF55P94UnitFourClass_eq_iff
#print axioms nativeF55P94UnitFourToShadow
#print axioms nativeF55P93ToP94UnitFour
#print axioms nativeF55P93ToP94UnitFour_surjective
#print axioms nativeF55P94HorizontalUnit_new_class_eq
#print axioms nativeF55P94HorizontalUnit_shadow_eq
#print axioms northHexagonNativeF55P94HorizontalUnit_new_witness

end
end Kuu.F112.Physical
