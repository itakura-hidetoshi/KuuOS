import Kuu.F112.PolygonNativeF55P88InterchangeObstruction

/-!
# F112-P89A — an explicit alternate Type-valued interchange presentation

The old P87 witness syntax is unchanged. This is a DIFFERENT,
source-typed 4-cell presentation: its new interchange constructor
witnesses the genuine original F55 interchange pair, subject to the
actual F54 route typing. The old twelve constructor operations are
recursively retained as operations on new P89 certificates.

Adding a generator is not an axiom asserting P87 equality, and not
yet a construction of all local strict 3-category coherence laws.
Original full F55 shadow is proved sound for every constructor.
P88 noncommutative word is explicitly NOT invariant here when the
two middle original histories are nonunit. All original F54 route
objects and physical odd exchange phases remain unchanged.
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

/-- Distinct, proof-relevant P89 4-cell presentation. Original P87
certificates embed, but P88 interchange obstruction is deliberately
not a law of this NEW presentation. The added genuine Type constructor
records exactly which comparison becomes admissible. -/
inductive NativeF55P89InterchangeFourCell
    {p : Polygon} {a b : D} {x y : E} :
    ∀ {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last},
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v →
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v →
      Type (max (max uD uE) (max vD vE)) where
  | old

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (witness : NativeF55P87ClosedFourCell f g) :
      NativeF55P89InterchangeFourCell f g
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
      (f₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₀ u₁)
      (f₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₁ u₂)
      (g₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₀ v₁)
      (g₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₁ v₂) :
      NativeF55P89InterchangeFourCell
        ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂))
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
          (f₁.horizontal g₁) (f₂.horizontal g₂))
  | refl

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
      NativeF55P89InterchangeFourCell f f
  | symm

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P89InterchangeFourCell f g) :
      NativeF55P89InterchangeFourCell g f
  | trans

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (fg : NativeF55P89InterchangeFourCell f g)
      (gh : NativeF55P89InterchangeFourCell g h) :
      NativeF55P89InterchangeFourCell f h
  | leftWhisker

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w}
      (h : NativeF55P89InterchangeFourCell f g) :
      NativeF55P89InterchangeFourCell (.trans prior f) (.trans prior g)
  | rightWhisker

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P89InterchangeFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w) :
      NativeF55P89InterchangeFourCell (.trans f suffix) (.trans g suffix)
  | leftContext

      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P89InterchangeFourCell f g)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P89InterchangeFourCell
        (.leftContext f later) (.leftContext g later)
  | rightContext

      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P89InterchangeFourCell f g) :
      NativeF55P89InterchangeFourCell
        (.rightContext earlier f) (.rightContext earlier g)
  | precompose

      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      (prior : KuuNativeF45Tree.DepthRotationRoute p first middle)
      {r s : KuuNativeF45Tree.DepthRotationRoute p middle last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (h : NativeF55P89InterchangeFourCell f g) :
      NativeF55P89InterchangeFourCell
        (.precompose prior f) (.precompose prior g)
  | postcompose

      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first middle}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (h : NativeF55P89InterchangeFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
      NativeF55P89InterchangeFourCell
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
      {f f' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u'}
      (h : NativeF55P89InterchangeFourCell f f')
      (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
      NativeF55P89InterchangeFourCell
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
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u')
      {g g' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v'}
      (h : NativeF55P89InterchangeFourCell g g') :
      NativeF55P89InterchangeFourCell
        (f.horizontal g) (f.horizontal g')


variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}

/-- Direct independent proof of all thirteen P89 source 4-cell
constructors preserving the ORIGINAL full F55 charge/phase shadow.
The interchange constructor uses the OLD raw P87 commutative-shadow
calculation only for shadow soundness, never as a 4-cell witness. -/
theorem NativeF55P89InterchangeFourCell.shadow_sound
    (h : NativeF55P89InterchangeFourCell f g) :
    f.nativeShadow = g.nativeShadow := by
  induction h with
  | old witness => exact witness.shadow_sound
  | interchange f₁ f₂ g₁ g₂ =>
      exact nativeF55P87_interchange_shadow f₁ f₂ g₁ g₂
  | refl raw => rfl
  | symm witness ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior witness ih =>
      change prior.nativeShadow + _ = prior.nativeShadow + _
      rw [ih]
  | rightWhisker witness suffix ih =>
      change _ + suffix.nativeShadow = _ + suffix.nativeShadow
      rw [ih]
  | leftContext witness later ih => exact ih
  | rightContext earlier witness ih => exact ih
  | precompose prior witness ih => exact ih
  | postcompose witness suffix ih => exact ih
  | horizontalLeft witness g ih =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => z + g.nativeShadow) ih
  | horizontalRight f witness ih =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => f.nativeShadow + z) ih

/-- The exact quotient kernel is the existence of an actual P89 Type
certificate, not equality of full shadows or numeric observations. -/
def nativeF55P89FourSetoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Setoid (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) where
  r := fun f g => Nonempty (NativeF55P89InterchangeFourCell f g)
  iseqv := ⟨
    (fun raw => ⟨.refl raw⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun v => ⟨.trans w v⟩)))⟩

abbrev NativeF55P89FourClasses
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :=
  _root_.Quotient (nativeF55P89FourSetoid first last u v)

def nativeF55P89FourClass
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    NativeF55P89FourClasses first last u v :=
  _root_.Quotient.mk _ raw

theorem nativeF55P89FourClass_eq_iff
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55P89FourClass first last f =
      nativeF55P89FourClass first last g ↔
      Nonempty (NativeF55P89InterchangeFourCell f g) := by
  constructor
  · intro heq
    exact _root_.Quotient.exact heq
  · intro hw
    exact _root_.Quotient.sound hw

/-- All full original F55 signed-charge / odd-phase coordinates
descend through this new quotient. No exchange phase is erased. -/
def nativeF55P89FourToShadow
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P89FourClasses first last u v → KuuNativeF55Shadow :=
  _root_.Quotient.lift
    (fun raw => raw.nativeShadow)
    (by
      intro a b h
      rcases h with ⟨w⟩
      exact w.shadow_sound)

/-- The old P87 quotient maps naturally onto this DIFFERENT,
strictly coarser possible presentation. -/
def nativeF55P87ToP89
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (q : NativeF55P87FourClasses first last u v) :
    NativeF55P89FourClasses first last u v :=
  _root_.Quotient.liftOn q
    (fun raw => nativeF55P89FourClass first last raw)
    (by
      intro a b h
      rcases h with ⟨w⟩
      exact _root_.Quotient.sound ⟨NativeF55P89InterchangeFourCell.old w⟩)

theorem nativeF55P87ToP89_surjective
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last} :
    Function.Surjective (nativeF55P87ToP89 first last (u := u) (v := v)) := by
  intro q
  refine _root_.Quotient.inductionOn q (fun raw => ?_)
  exact ⟨nativeF55P87FourClass first last raw, rfl⟩

/-- P89 makes the ORIGINAL typed raw interchange strictly equal
in the NEW quotient, by a genuine explicit P89 Type four-cell.
It does not reinterpret this as an old P87 equality. -/
theorem nativeF55P89_interchange_quotient_eq
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₀ u₁)
    (f₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₁ u₂)
    (g₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₀ v₁)
    (g₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₁ v₂) :
    nativeF55P89FourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂)) =
    nativeF55P89FourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (f₁.horizontal g₁) (f₂.horizontal g₂)) := by
  exact _root_.Quotient.sound
    ⟨NativeF55P89InterchangeFourCell.interchange f₁ f₂ g₁ g₂⟩

/-- Old P88 exact word conservation cannot extend as-is to a
sound invariant for ALL P89 certificates. In the nonunit-middle
case we expose BOTH genuine new evidence and the precise old word
inequality. This is explicit information loss, not concealment. -/
theorem nativeF55P89_interchange_word_not_preserved
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₀ u₁)
    (f₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₁ u₂)
    (g₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₀ v₁)
    (g₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₁ v₂)
    (hf : f₂.p88InterchangeWord ≠ [])
    (hg : g₁.p88InterchangeWord ≠ []) :
    Nonempty (NativeF55P89InterchangeFourCell
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂))
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (f₁.horizontal g₁) (f₂.horizontal g₂))) ∧
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂)).p88InterchangeWord ≠
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (f₁.horizontal g₁) (f₂.horizontal g₂)).p88InterchangeWord := by
  exact ⟨⟨NativeF55P89InterchangeFourCell.interchange f₁ f₂ g₁ g₂⟩,
    nativeF55P88_raw_interchange_word_ne f₁ f₂ g₁ g₂ hf hg⟩

#print axioms NativeF55P89InterchangeFourCell
#print axioms NativeF55P89InterchangeFourCell.shadow_sound
#print axioms nativeF55P89FourSetoid
#print axioms NativeF55P89FourClasses
#print axioms nativeF55P89FourClass_eq_iff
#print axioms nativeF55P89FourToShadow
#print axioms nativeF55P87ToP89
#print axioms nativeF55P87ToP89_surjective
#print axioms nativeF55P89_interchange_quotient_eq
#print axioms nativeF55P89_interchange_word_not_preserved

end
end Kuu.F112.Physical
