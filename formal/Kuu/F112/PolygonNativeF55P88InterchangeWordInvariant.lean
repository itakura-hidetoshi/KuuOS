import Kuu.F112.PolygonNativeF55P87ClosedHorizontalCategory

/-!
# F112-P88A — independent noncommutative source-word invariant

P87 proves that original F55 horizontal composition is a total
self-closed P87×P87→P87 binary operation, using its recursively
closed genuine Type-valued 4-cell presentation. It has NOT shown
strict interchange with source vertical pasting.

To decide genuine interchange, we introduce an ORIGINAL raw F55
source-SYNTACTIC invariant into the NONCOMMUTATIVE free word monoid
(List Bool, append). Each actual non-unit pentagon/disjoint-square
atom contributes one letter. Vertical F55 composition concatenates
words; original left F45 binary context uniformly marks letters
FALSE and original right binary context uniformly marks letters
TRUE. F54 pre/postcompose preserve source word, as does raw
symmetry. An original horizontal pasting therefore produces left
letters THEN right letters.

This is not the old commutative (Int × Int) × ZMod 2 numerical
observer, and we do NOT define new source equality by word equality.
Instead we PROVE that all eight original P77 vertical four-cell
constructors, all nine P80, all eight P85, all twelve P86 and all
twelve recursive P87 Type-valued FOUR-CELL constructors conserve
the independent word. Hence any P87 class equation preserves
this source-order witness.

The law for raw interchange can move a right-context block past
a left-context block. In a noncommutative free word this is in
general a new relation, not a consequence of vertical units,
associators, context closure or horizontal whiskering.
The exact no-go and strict-interchange obligations follow in
P88B, using source witnesses rather than numeric shadows.

No Gray, no new axioms, no sorry/admit and no discarded previous
public roots. Earlier C60 and pre-C60 dependent-origination theory
remain mathematical context rather than being replaced by C60.
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

/-- Genuine source-order word in the FREE noncommutative monoid
on two context-orientation markers. The actual source constructors
and dependent F54 type bounds remain unchanged. Ident, pentagon and
square are distinguished by being empty versus nonempty; left/right
contexts mark the orientation on every source primitive letter.
Raw F55 symm is retained as an ORIGINAL constructor (not a claim
about the strict 3-inverse law). -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88InterchangeWord
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb} :
    ∀ {u v : KuuNativeF45Tree.DepthRotationRoute p first last},
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v → List Bool
  | _, _, .ident _ => []
  | _, _, .pentagon _ _ _ _ => [false]
  | _, _, .disjointSquare _ _ => [false]
  | _, _, .symm c => c.p88InterchangeWord
  | _, _, .trans c d => c.p88InterchangeWord ++ d.p88InterchangeWord
  | _, _, .leftContext c _ => c.p88InterchangeWord.map (fun _ => false)
  | _, _, .rightContext _ c => c.p88InterchangeWord.map (fun _ => true)
  | _, _, .precompose _ c => c.p88InterchangeWord
  | _, _, .postcompose c _ => c.p88InterchangeWord

/-- Explicit source horizontal word formula: ORIGINAL horizontal
syntax is a vertical paste of F54-left-context and right-context
source cells, so the order is FALSE letters followed by TRUE letters. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word
    {p : Polygon} {a b : D} {x y : E}
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
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
    (f.horizontal g).p88InterchangeWord =
      f.p88InterchangeWord.map (fun _ => false) ++
        g.p88InterchangeWord.map (fun _ => true) := rfl

/-- The P77 ORIGINAL proof-relevant vertical units, associator,
whiskerings and all Type-valued proof transitivity preserve order.
This source proof is independent of numerical shadow invariants. -/
theorem NativeF55RawVerticalFourCell.p88_word_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
    (h : NativeF55RawVerticalFourCell first last f g) :
    f.p88InterchangeWord = g.p88InterchangeWord := by
  induction h with
  | refl raw => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior h ih =>
      change prior.p88InterchangeWord ++ _ =
        prior.p88InterchangeWord ++ _
      rw [ih]
  | rightWhisker h suffix ih =>
      change _ ++ suffix.p88InterchangeWord =
        _ ++ suffix.p88InterchangeWord
      rw [ih]
  | leftUnit raw =>
      change ([] : List Bool) ++ raw.p88InterchangeWord =
        raw.p88InterchangeWord
      rfl
  | rightUnit raw =>
      change raw.p88InterchangeWord ++ ([] : List Bool) =
        raw.p88InterchangeWord
      simp
  | assoc a b c =>
      change (a.p88InterchangeWord ++ b.p88InterchangeWord) ++
          c.p88InterchangeWord =
        a.p88InterchangeWord ++
          (b.p88InterchangeWord ++ c.p88InterchangeWord)
      exact List.append_assoc _ _ _

/-- P80 adds exactly three Type-valued unit comparison constructors.
Their original source words are both EMPTY; all old P77 witnesses
preserve the word by independent source induction. -/
theorem NativeF55P80UnitFourCell.p88_word_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
    (h : NativeF55P80UnitFourCell f g) :
    f.p88InterchangeWord = g.p88InterchangeWord := by
  induction h with
  | old w => exact w.p88_word_sound
  | refl raw => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior h ih =>
      change prior.p88InterchangeWord ++ _ =
        prior.p88InterchangeWord ++ _
      rw [ih]
  | rightWhisker h suffix ih =>
      change _ ++ suffix.p88InterchangeWord =
        _ ++ suffix.p88InterchangeWord
      rw [ih]
  | horizontalUnit u v => rfl
  | leftContextUnit u later => rfl
  | rightContextUnit earlier u => rfl

/-- P85's two ORIGINAL horizontal whiskers respect source order:
the genuine P80 certificate changes precisely one word argument
of the original left-word/right-word concatenation. -/
theorem NativeF55P85HorizontalFourCell.p88_word_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
    (h : NativeF55P85HorizontalFourCell f g) :
    f.p88InterchangeWord = g.p88InterchangeWord := by
  induction h with
  | old w => exact w.p88_word_sound
  | refl raw => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior h ih =>
      change prior.p88InterchangeWord ++ _ =
        prior.p88InterchangeWord ++ _
      rw [ih]
  | rightWhisker h suffix ih =>
      change _ ++ suffix.p88InterchangeWord =
        _ ++ suffix.p88InterchangeWord
      rw [ih]
  | horizontalLeft witness g =>
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word,
        witness.p88_word_sound]
  | horizontalRight f witness =>
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word,
        witness.p88_word_sound]

/-- P86's six new source context/route/horizontal generators are
also word-sound, with genuinely typed old P85 witness arguments. -/
theorem NativeF55P86ContextFourCell.p88_word_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
    (h : NativeF55P86ContextFourCell f g) :
    f.p88InterchangeWord = g.p88InterchangeWord := by
  induction h with
  | old w => exact w.p88_word_sound
  | refl raw => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior h ih =>
      change prior.p88InterchangeWord ++ _ =
        prior.p88InterchangeWord ++ _
      rw [ih]
  | rightWhisker h suffix ih =>
      change _ ++ suffix.p88InterchangeWord =
        _ ++ suffix.p88InterchangeWord
      rw [ih]
  | leftContext witness later =>
      change (List.map (fun _ : Bool => false) _) =
        List.map (fun _ : Bool => false) _
      rw [witness.p88_word_sound]
  | rightContext earlier witness =>
      change (List.map (fun _ : Bool => true) _) =
        List.map (fun _ : Bool => true) _
      rw [witness.p88_word_sound]
  | precompose prior witness => exact witness.p88_word_sound
  | postcompose witness suffix => exact witness.p88_word_sound
  | horizontalLeft witness g =>
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word,
        witness.p88_word_sound]
  | horizontalRight f witness =>
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word,
        witness.p88_word_sound]

/-- P87 recursively transports P87 four-cell witnesses through
each context and horizontal whisker, so the induction genuinely
checks every one of its TWELVE source constructors. A numerical
shadow equality is not used at any point. -/
theorem NativeF55P87ClosedFourCell.p88_word_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
    (h : NativeF55P87ClosedFourCell f g) :
    f.p88InterchangeWord = g.p88InterchangeWord := by
  induction h with
  | old w => exact w.p88_word_sound
  | refl raw => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior h ih =>
      change prior.p88InterchangeWord ++ _ =
        prior.p88InterchangeWord ++ _
      rw [ih]
  | rightWhisker h suffix ih =>
      change _ ++ suffix.p88InterchangeWord =
        _ ++ suffix.p88InterchangeWord
      rw [ih]
  | leftContext witness later ih =>
      change (List.map (fun _ : Bool => false) _) =
        List.map (fun _ : Bool => false) _
      rw [ih]
  | rightContext earlier witness ih =>
      change (List.map (fun _ : Bool => true) _) =
        List.map (fun _ : Bool => true) _
      rw [ih]
  | precompose prior witness ih => exact ih
  | postcompose witness suffix ih => exact ih
  | horizontalLeft witness g ih =>
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word, ih]
  | horizontalRight f witness ih =>
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word, ih]

/-- This source grammar has a word-conserving exact quotient
boundary: equality of P87 classes forces equality of source
noncommutative words by a REAL 4-cell witness, not by shadow. -/
theorem nativeF55P87FourClass_eq_implies_p88_word
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (h : nativeF55P87FourClass first last f =
      nativeF55P87FourClass first last g) :
    f.p88InterchangeWord = g.p88InterchangeWord := by
  obtain ⟨certificate⟩ := (nativeF55P87FourClass_eq_iff first last f g).mp h
  exact certificate.p88_word_sound

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88InterchangeWord
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word
#print axioms NativeF55RawVerticalFourCell.p88_word_sound
#print axioms NativeF55P80UnitFourCell.p88_word_sound
#print axioms NativeF55P85HorizontalFourCell.p88_word_sound
#print axioms NativeF55P86ContextFourCell.p88_word_sound
#print axioms NativeF55P87ClosedFourCell.p88_word_sound
#print axioms nativeF55P87FourClass_eq_implies_p88_word

end
end Kuu.F112.Physical
