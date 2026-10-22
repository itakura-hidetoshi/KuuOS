import Kuu.F112.PolygonNativeF55P92OriginalUnitNaturalityNoGo
import Mathlib.Tactic

/-!
# F112-P92B — separately declared original-F55 associator-naturality extension

P92A proved that original nine-constructor F55 witnesses CANNOT
satisfy associator naturality even for three genuine F54 zero-edge
routes, using their complete ordered left/right-context words.

We do NOT rewrite that original source or present the forbidden
witness as if it came from old F55, nor discard the original
odd C60 phase. Instead, a DIFFERENT genuine Type-valued 3-cell
PRESENTATION is explicitly declared with TWO primitive inclusions:
(1) a faithful embedding of the entire original F55 source witness
and (2) a NEW, honestly labeled three-route associator naturality
GENERATOR, between precisely the original P90 typed source routes.
The standard 3-proof invertible pasting and F54 binary contexts and
route whiskering recursively close these primitive constructors.

On this separately selected presentation, the new naturality
generator is assigned zero chosen full F55 shadow. This is a
consistent choice since P91A shows its genuine F54 rotation defect
is exactly zero, and the original signed square charge/odd phase
remain faithfully preserved by original generators.
We prove all new constructor shadow parity and defect constraints.

A separate exact Type-evidence route-object quotient will equate
the two original P90 source routes BY THE EXPLICIT NEW GENERATOR,
and old original-F55 witnesses map into it. P92A's original source
no-go remains true: the noncommutative empty-route-context word
observer does NOT descend to this new extended comparison.

This does NOT prove a globally strict 3/n-category, all 4-cell
coherences, uniqueness of this presentation, or hyperdescent.
No Gray, sorry, admits or new logical axioms. C60 is a testbed.
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

/-- NEW and DISTINCT source proof presentation with an EXPLICIT
associator-naturality primitive. This new constructor is not a
consequence of original nine-constructor F55, as P92A proves. -/
inductive NativeF55P92AssocComparison (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb},
      KuuNativeF45Tree.DepthRotationRoute p first last →
      KuuNativeF45Tree.DepthRotationRoute p first last →
      Type (max (max uD uE) (max vD vE)) where
  | original
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
      NativeF55P92AssocComparison p r s
  | assocNaturality
      {a b : D} {x y : E}
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (u : KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter)
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :
      NativeF55P92AssocComparison p
        (nativeF54P90AssocNaturalityLeftRoute u v w)
        (nativeF54P90AssocNaturalityRightRoute u v w)
  | refl
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
      NativeF55P92AssocComparison p route route
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (cell : NativeF55P92AssocComparison p r s) : NativeF55P92AssocComparison p s r
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (left : NativeF55P92AssocComparison p r s)
      (right : NativeF55P92AssocComparison p s t) :
      NativeF55P92AssocComparison p r t
  | leftContext
      {a b : D} {x y : E} {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (cell : NativeF55P92AssocComparison p r s)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P92AssocComparison p
        (KuuNativeF45Tree.DepthRotationRoute.leftContext r later)
        (KuuNativeF45Tree.DepthRotationRoute.leftContext s later)
  | rightContext
      {a b : D} {x y : E} {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (cell : NativeF55P92AssocComparison p r s) :
      NativeF55P92AssocComparison p
        (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier r)
        (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier s)
  | precompose
      {a b : D} {x y : E}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      (priorRoute : KuuNativeF45Tree.DepthRotationRoute p first middle)
      {r s : KuuNativeF45Tree.DepthRotationRoute p middle last}
      (cell : NativeF55P92AssocComparison p r s) :
      NativeF55P92AssocComparison p
        (KuuNativeF45Tree.DepthRotationRoute.trans priorRoute r)
        (KuuNativeF45Tree.DepthRotationRoute.trans priorRoute s)
  | postcompose
      {a b : D} {x y : E}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first middle}
      (cell : NativeF55P92AssocComparison p r s)
      (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
      NativeF55P92AssocComparison p
        (KuuNativeF45Tree.DepthRotationRoute.trans r suffix)
        (KuuNativeF45Tree.DepthRotationRoute.trans s suffix)


/-- This selected extension retains the complete original signed
pentagon and square charges and the genuine odd ZMod2 phase. Only
the NEW explicitly adjoined naturality generator has chosen zero
shadow, consistent with P91A's necessary zero pentagon defect. -/
def NativeF55P92AssocComparison.nativeShadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    KuuNativeF55Shadow := by
  induction cell with
  | original old => exact old.nativeShadow
  | assocNaturality u v w => exact 0
  | refl route => exact 0
  | symm cell ih => exact -ih
  | trans f g ihf ihg => exact ihf + ihg
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih => exact ih
  | postcompose cell suffix ih => exact ih

/-- The original nine-constructor source retains its exact chosen
full signed shadow, including genuine odd C60 exchange phase. -/
theorem nativeF55P92_original_shadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (old : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (NativeF55P92AssocComparison.original old).nativeShadow =
      old.nativeShadow := rfl

/-- The honest NEW primitive has precisely the selected zero
full-shadow grade; we do not pretend the choice was forced. -/
theorem nativeF55P92_assocNaturality_shadow

    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (u : KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter)
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :
    (NativeF55P92AssocComparison.assocNaturality u v w).nativeShadow =
      (0 : KuuNativeF55Shadow) := rfl

/-- The original odd-square parity relation survives every new
Type-valued generator and all recursive closure operations. -/
theorem NativeF55P92AssocComparison.phase_squareParity
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    ((cell.nativeShadow.1.2 : Int) : ZMod 2) =
      cell.nativeShadow.2 := by
  induction cell with
  | original old => exact old.phase_squareParity
  | assocNaturality u v w => rfl
  | refl route => rfl
  | symm cell ih =>
      change ((-cell.nativeShadow.1.2 : Int) : ZMod 2) =
        -cell.nativeShadow.2
      simpa using congrArg (fun z : ZMod 2 => -z) ih
  | trans f g ihf ihg =>
      change ((f.nativeShadow.1.2 + g.nativeShadow.1.2 : Int) :
        ZMod 2) = f.nativeShadow.2 + g.nativeShadow.2
      simpa using congrArg₂ (fun z w : ZMod 2 => z + w) ihf ihg
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih => exact ih
  | postcompose cell suffix ih => exact ih

/-- Every NEW genuine Type-valued generator remains compatible
with the exact ORIGINAL F54 rotation-count signed pentagon defect.
The zero shadow on the NEW naturality generator is consistent with
P90's two equal-rotation-count endpoints, not a new logical axiom. -/
theorem NativeF55P92AssocComparison.pentagonCharge_eq_countDefect
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    (r.rotationCount : Int) - (s.rotationCount : Int) =
      cell.nativeShadow.1.1 := by
  induction cell with
  | original old => exact old.p91_pentagonCharge_eq_countDefect
  | assocNaturality u v w =>
      have hcount := nativeF54P90AssocNaturality_rotationCount_eq u v w
      change ((nativeF54P90AssocNaturalityLeftRoute u v w).rotationCount : Int) -
        ((nativeF54P90AssocNaturalityRightRoute u v w).rotationCount : Int) = 0
      rw [hcount, sub_self]
  | refl route =>
      change (route.rotationCount : Int) - (route.rotationCount : Int) = 0
      omega
  | symm cell ih =>
      change _ = -cell.nativeShadow.1.1
      omega
  | trans f g ihf ihg =>
      change _ = f.nativeShadow.1.1 + g.nativeShadow.1.1
      omega
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      change ((prior.rotationCount + _ : Nat) : Int) -
        ((prior.rotationCount + _ : Nat) : Int) = cell.nativeShadow.1.1
      simp only [Nat.cast_add]
      dsimp only [KuuNativeF45Tree.DepthRotationRoute.rotationCount] at *
      omega
  | postcompose cell suffix ih =>
      change ((_ + suffix.rotationCount : Nat) : Int) -
        ((_ + suffix.rotationCount : Nat) : Int) = cell.nativeShadow.1.1
      simp only [Nat.cast_add]
      dsimp only [KuuNativeF45Tree.DepthRotationRoute.rotationCount] at *
      omega

/-- This explicit Type-valued NEW source presentation induces a
DIFFERENT F54 route-object quotient, by actual witness existence. -/
def nativeF55P92AssocRouteSetoid
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Setoid (KuuNativeF45Tree.DepthRotationRoute p first last) where
  r := fun u v => Nonempty (NativeF55P92AssocComparison p u v)
  iseqv := ⟨
    (fun route => ⟨.refl route⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun z => ⟨.trans w z⟩)))⟩

abbrev NativeF55P92AssocRouteClasses
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :=
  _root_.Quotient (nativeF55P92AssocRouteSetoid first last)

def nativeF55P92AssocRouteClass
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P92AssocRouteClasses first last :=
  _root_.Quotient.mk _ r

theorem nativeF55P92AssocRouteClass_eq_iff
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeF55P92AssocRouteClass first last u =
      nativeF55P92AssocRouteClass first last v ↔
      Nonempty (NativeF55P92AssocComparison p u v) := by
  constructor
  · intro h
    exact _root_.Quotient.exact h
  · intro h
    exact _root_.Quotient.sound h

theorem nativeF55P92AssocRouteClass_eq_of_cell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p u v) :
    nativeF55P92AssocRouteClass first last u =
      nativeF55P92AssocRouteClass first last v :=
  _root_.Quotient.sound ⟨cell⟩

/-- THIS selected new presentation truly supplies the previously
UNFILLED triple-route comparison, BY NEW CONSTRUCTOR, not by proof
inside old F55. Source Type boundaries are unchanged. -/
theorem nativeF55P92_assocNaturality_new_class_eq

    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (u : KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter)
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :
    nativeF55P92AssocRouteClass
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore)
      (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter))
      (nativeF54P90AssocNaturalityLeftRoute u v w) =
    nativeF55P92AssocRouteClass
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore)
      (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter))
      (nativeF54P90AssocNaturalityRightRoute u v w) :=
  nativeF55P92AssocRouteClass_eq_of_cell _ _
    (.assocNaturality u v w)

/-- The selected NEW 3-cell COMPARES the original P92 unit routes,
while P92A still proves the ORIGINAL F55 source has NO such cell.
This identifies exactly which additional evidence was adjoined. -/
theorem nativeF55P92_unit_old_no_filler_but_new_certificate
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (¬ Nonempty
      (NativeF55P90AssocNaturalityCell
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃))) ∧
    Nonempty (NativeF55P92AssocComparison p
      (nativeF54P90AssocNaturalityLeftRoute
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃))
      (nativeF54P90AssocNaturalityRightRoute
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃))) := by
  constructor
  · exact nativeF55P92_original_unit_naturality_no_filler t₁ t₂ t₃
  · exact ⟨.assocNaturality
      (nativeF54P92UnitRoute t₁)
      (nativeF54P92UnitRoute t₂)
      (nativeF54P92UnitRoute t₃)⟩

#print axioms NativeF55P92AssocComparison.nativeShadow
#print axioms nativeF55P92_original_shadow
#print axioms nativeF55P92_assocNaturality_shadow
#print axioms NativeF55P92AssocComparison.phase_squareParity
#print axioms NativeF55P92AssocComparison.pentagonCharge_eq_countDefect
#print axioms nativeF55P92AssocRouteSetoid
#print axioms NativeF55P92AssocRouteClasses
#print axioms nativeF55P92AssocRouteClass_eq_iff
#print axioms nativeF55P92AssocRouteClass_eq_of_cell
#print axioms nativeF55P92_assocNaturality_new_class_eq
#print axioms nativeF55P92_unit_old_no_filler_but_new_certificate

end
end Kuu.F112.Physical
