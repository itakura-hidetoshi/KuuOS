import Kuu.F112.PolygonNativeF55P94CPentagonPastingBoundary
import Mathlib.CategoryTheory.Groupoid
import Mathlib.Tactic

/-!
# F112-P94C2 — genuinely noncommutative groupoid of P92B 3-proofs

P94A proves a CATEGORY but does NOT provide inverse cancellation of
arbitrary P92B 3-cell histories. P94C1 has a true original F55 pentagon
generator of nonzero signed charge, at exact four-stage F54 boundaries.

Choose an explicitly DISTINCT Type-valued four-cell presentation:
* inclusion of every prior P94A witness, unchanged;
* left/right P92B 3-proof inverse cancellation 4-cells;
* preservation of 3-proof inversion under arbitrary 4-comparisons;
* all source whiskering, context, and horizontal congruence closures.

From genuine certificates (NEVER from equality of shadows) construct
the local GROUPoid on actual original F54 routes, preserving the entire
signed pentagon / signed square / odd C60 ZMod2 physical observation.
This is a group-theoretic strengthening needed before evaluating
the five-stage associahedron's nonabelian pentagonator relator.

No claim the new inverse relations held in P94A. No complete higher
pentagonator, strict global 3/n, Gray or extra logical axioms.
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

/-- Distinct source 4-proof grammar: GROUP-theoretic 3-cell inverse
coherence, retaining all P94A generators as real proof terms. -/
inductive NativeF55P94CGroupFourCell
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
      NativeF55P94CGroupFourCell f g
  | refl
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P94CGroupFourCell f f
  | symm
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94CGroupFourCell f g) :
      NativeF55P94CGroupFourCell g f
  | trans
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : NativeF55P92AssocComparison p r s}
      (fg : NativeF55P94CGroupFourCell f g)
      (gh : NativeF55P94CGroupFourCell g h) :
      NativeF55P94CGroupFourCell f h
  | inverseLeft
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P94CGroupFourCell (.trans f (.symm f)) (.refl r)
  | inverseRight
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55P92AssocComparison p r s) :
      NativeF55P94CGroupFourCell (.trans (.symm f) f) (.refl s)
  | inverseRespect
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94CGroupFourCell f g) :
      NativeF55P94CGroupFourCell (.symm f) (.symm g)
  | leftWhisker
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : NativeF55P92AssocComparison p r s)
      {f g : NativeF55P92AssocComparison p s t}
      (w : NativeF55P94CGroupFourCell f g) :
      NativeF55P94CGroupFourCell (.trans prior f) (.trans prior g)
  | rightWhisker
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94CGroupFourCell f g)
      (suffix : NativeF55P92AssocComparison p s t) :
      NativeF55P94CGroupFourCell (.trans f suffix) (.trans g suffix)
  | leftContext
      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94CGroupFourCell f g)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P94CGroupFourCell (.leftContext f later) (.leftContext g later)
  | rightContext
      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94CGroupFourCell f g) :
      NativeF55P94CGroupFourCell (.rightContext earlier f) (.rightContext earlier g)
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
      (w : NativeF55P94CGroupFourCell f g) :
      NativeF55P94CGroupFourCell
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
      (w : NativeF55P94CGroupFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
      NativeF55P94CGroupFourCell
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
      (w : NativeF55P94CGroupFourCell f f')
      (g : NativeF55P92AssocComparison p v v') :
      NativeF55P94CGroupFourCell
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
      (w : NativeF55P94CGroupFourCell g g') :
      NativeF55P94CGroupFourCell
        (f.horizontal g) (f.horizontal g')

/-- Every chosen groupoid 4-cell generator is compatible with ALL
three original F55 shadow coordinates; the odd ZMod2 is never erased. -/
theorem NativeF55P94CGroupFourCell.shadow_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94CGroupFourCell f g) :
    f.nativeShadow = g.nativeShadow := by
  induction w with
  | old witness => exact witness.shadow_sound
  | refl cell => rfl
  | symm witness ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | inverseLeft f =>
      change f.nativeShadow + -f.nativeShadow = (0 : KuuNativeF55Shadow)
      exact add_neg_cancel _
  | inverseRight f =>
      change -f.nativeShadow + f.nativeShadow = (0 : KuuNativeF55Shadow)
      exact neg_add_cancel _
  | inverseRespect witness ih =>
      exact congrArg (fun z : KuuNativeF55Shadow => -z) ih
  | leftWhisker prior witness ih =>
      exact congrArg (fun z : KuuNativeF55Shadow => prior.nativeShadow + z) ih
  | rightWhisker witness suffix ih =>
      exact congrArg (fun z : KuuNativeF55Shadow => z + suffix.nativeShadow) ih
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

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- This NEW groupoid quotient has exact proof-term witness kernel. -/
def nativeF55P94CGroupFourSetoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Setoid (NativeF55P92AssocComparison p r s) where
  r := fun f g => Nonempty (NativeF55P94CGroupFourCell f g)
  iseqv := ⟨
    (fun f => ⟨.refl f⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun z => ⟨.trans w z⟩)))⟩

abbrev NativeF55P94CGroupFourClasses
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :=
  _root_.Quotient (nativeF55P94CGroupFourSetoid first last r s)

def nativeF55P94CGroupFourClass
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    NativeF55P94CGroupFourClasses first last r s :=
  _root_.Quotient.mk _ cell

/-- Selected OLD P94A witnesses embed as actual NEW Type evidence;
in no way are the new inverse relations attributed to P94A. -/
def nativeF55P94COldToGroup
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (q : NativeF55P94UnitFourClasses first last r s) :
    NativeF55P94CGroupFourClasses first last r s :=
  Quot.liftOn q (fun raw => nativeF55P94CGroupFourClass first last raw)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact Quot.sound ⟨NativeF55P94CGroupFourCell.old w⟩)

/-- Full signed pentagon, exchange square and genuinely odd C60 phase
descend along exactly the new Type-valued groupoid 4-relations. -/
def nativeF55P94CGroupToShadow
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P94CGroupFourClasses first last r s → KuuNativeF55Shadow :=
  Quot.lift (fun raw => raw.nativeShadow)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.shadow_sound)

/-- 3-cell vertical composition is well-defined on genuinely typed
new GROUPoid quotient representatives. -/
def nativeF55P94CGroupVerticalComp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P94CGroupFourClasses first last r s)
    (g : NativeF55P94CGroupFourClasses first last s t) :
    NativeF55P94CGroupFourClasses first last r t :=
  Quot.liftOn₂ f g
    (fun left right => nativeF55P94CGroupFourClass first last (.trans left right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨w⟩
      exact ⟨NativeF55P94CGroupFourCell.leftWhisker left w⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨w⟩
      exact ⟨NativeF55P94CGroupFourCell.rightWhisker w right⟩)

/-- Actual groupoid inverse, using raw P92B 3-cell reversal and NEW
inversion-respect four-cell evidence. -/
def nativeF55P94CGroupInverse
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P94CGroupFourClasses first last r s) :
    NativeF55P94CGroupFourClasses first last s r :=
  Quot.liftOn f (fun raw => nativeF55P94CGroupFourClass first last (.symm raw))
    (by
      intro left right h
      rcases h with ⟨w⟩
      exact Quot.sound ⟨NativeF55P94CGroupFourCell.inverseRespect w⟩)

/-- A locally STRICT noncommutative Mathlib Groupoid of ACTUAL original
F54 route objects and original P92B 3-proof source morphisms.
The 3-proof inverse identities are certified by the explicitly NEW
Type-valued four-cell generators. -/
@[reducible] def nativeF55P94CGroupoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Groupoid (KuuNativeF45Tree.DepthRotationRoute p first last) where
  Hom := NativeF55P94CGroupFourClasses first last
  id route := nativeF55P94CGroupFourClass first last (.refl route)
  comp f g := nativeF55P94CGroupVerticalComp first last f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P94CGroupFourClass first last (.trans (.refl X) raw) =
      nativeF55P94CGroupFourClass first last raw
    exact Quot.sound ⟨NativeF55P94CGroupFourCell.old
      (.verticalLeftUnit raw)⟩
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P94CGroupFourClass first last (.trans raw (.refl Y)) =
      nativeF55P94CGroupFourClass first last raw
    exact Quot.sound ⟨NativeF55P94CGroupFourCell.old
      (.verticalRightUnit raw)⟩
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun a => ?_)
    refine Quot.inductionOn g (fun b => ?_)
    refine Quot.inductionOn h (fun c => ?_)
    change nativeF55P94CGroupFourClass first last (.trans (.trans a b) c) =
      nativeF55P94CGroupFourClass first last (.trans a (.trans b c))
    exact Quot.sound ⟨NativeF55P94CGroupFourCell.old
      (.verticalAssoc a b c)⟩
  inv := fun {X Y} f => nativeF55P94CGroupInverse first last f
  inv_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P94CGroupFourClass first last (.trans (.symm raw) raw) =
      nativeF55P94CGroupFourClass first last (.refl Y)
    exact Quot.sound ⟨NativeF55P94CGroupFourCell.inverseRight raw⟩
  comp_inv := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P94CGroupFourClass first last (.trans raw (.symm raw)) =
      nativeF55P94CGroupFourClass first last (.refl X)
    exact Quot.sound ⟨NativeF55P94CGroupFourCell.inverseLeft raw⟩

/-- The chosen GROUPoid presentation cancels the genuine original F55
four-stage pentagon 3-cell against its P92B reversal by explicit 4-evidence. -/
def nativeF55P94CGroupPentagon_cancel
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    NativeF55P94CGroupFourCell
      (.trans (nativeF55P94CPentagonThreeCell t₁ t₂ t₃ t₄)
        (.symm (nativeF55P94CPentagonThreeCell t₁ t₂ t₃ t₄)))
      (.refl (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄)) :=
  .inverseLeft (nativeF55P94CPentagonThreeCell t₁ t₂ t₃ t₄)

/-- Genuine four-sector north C60 instance of the new inverse 4-law,
without erasing C60 sectors, prior odd square phase, or old P79 no-go. -/
def northNativeF55P94CGroupPentagon_cancel :
    NativeF55P94CGroupFourCell
      (.trans
        (nativeF55P94CPentagonThreeCell
          northNativeF45FirstStage northNativeF45SecondStage
          northNativeF45ThirdStage northNativeF45FourthStage)
        (.symm (nativeF55P94CPentagonThreeCell
          northNativeF45FirstStage northNativeF45SecondStage
          northNativeF45ThirdStage northNativeF45FourthStage)))
      (.refl northNativeF45PentagonLong) :=
  nativeF55P94CGroupPentagon_cancel _ _ _ _

#print axioms NativeF55P94CGroupFourCell
#print axioms NativeF55P94CGroupFourCell.shadow_sound
#print axioms nativeF55P94CGroupFourSetoid
#print axioms NativeF55P94CGroupFourClasses
#print axioms nativeF55P94COldToGroup
#print axioms nativeF55P94CGroupToShadow
#print axioms nativeF55P94CGroupVerticalComp
#print axioms nativeF55P94CGroupInverse
#print axioms nativeF55P94CGroupoid
#print axioms nativeF55P94CGroupPentagon_cancel
#print axioms northNativeF55P94CGroupPentagon_cancel

end
end Kuu.F112.Physical
