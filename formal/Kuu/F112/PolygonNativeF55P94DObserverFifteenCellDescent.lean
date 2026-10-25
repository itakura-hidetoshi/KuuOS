import Kuu.F112.PolygonNativeF55P94DConservativeTowerDescent
import Mathlib.Tactic

/-!
# F112-P94D3AO — dimension-polymorphic conservative 15-cell descent

For any EXACT dependent fiber of raw fourteen-cell proofs, construct a
Type-valued FIFTEEN-cell observer-conservative presentation preserving
both a selected nonabelian history and a signed integer charge.

The core presentation is explicitly the MAXIMAL history-and-charge
preserving comparison grammar: its atom is a pair of exact observer
equalities; this is NOT claimed to represent every original geometric
fifteen-cell constructor. The extended grammar independently adjoins
an exchange on one specifically named pair of original witnesses.
No raw proof equality or global high-dimensional coherence is assumed.

Its quotient has charge descent and an iff criterion for arbitrary
observers; the free-group history fails to descend at a separated pair.
The finite-closure no-go reuses F112-P94D3AL verbatim.

Specializing the carrier to the ORIGINAL source-dependent fourteen-cell
fiber (rather than an untyped graph) is the separate physical bridge.
-/

namespace Kuu.F112.Physical

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v w

/-- Explicitly named MAXIMAL observer-conservative Type-valued 15D grammar.
No independent exchange is hidden in its constructors. -/
inductive NativeObserverCoreFifteenCell {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ) :
    A → A → Type (max u v) where
  | refl (x : A) : NativeObserverCoreFifteenCell history charge x x
  | atom {x y : A}
      (hword : history x = history y)
      (hcharge : charge x = charge y) :
      NativeObserverCoreFifteenCell history charge x y
  | symm {x y : A}
      (h : NativeObserverCoreFifteenCell history charge x y) :
      NativeObserverCoreFifteenCell history charge y x
  | trans {x y z : A}
      (h : NativeObserverCoreFifteenCell history charge x y)
      (k : NativeObserverCoreFifteenCell history charge y z) :
      NativeObserverCoreFifteenCell history charge x z

/-- EVERY conservative 15D witness preserves its exact free-word history. -/
theorem NativeObserverCoreFifteenCell.history_sound
    {A : Type u} {W : Type v}
    {history : A → W} {charge : A → ℤ}
    {x y : A}
    (h : NativeObserverCoreFifteenCell history charge x y) :
    history x = history y := by
  induction h with
  | refl _ => rfl
  | atom hword _ => exact hword
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2

/-- EVERY conservative 15D witness also preserves integer charge. -/
theorem NativeObserverCoreFifteenCell.charge_sound
    {A : Type u} {W : Type v}
    {history : A → W} {charge : A → ℤ}
    {x y : A}
    (h : NativeObserverCoreFifteenCell history charge x y) :
    charge x = charge y := by
  induction h with
  | refl _ => rfl
  | atom _ hcharge => exact hcharge
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2

/-- The exact strength of this maximal conservative grammar:
filler existence is EQUIVALENT to joint observer compatibility.
It does not identify raw proof terms. -/
theorem nativeObserverCoreFifteen_filler_iff
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (x y : A) :
    Nonempty (NativeObserverCoreFifteenCell history charge x y) ↔
      history x = history y ∧ charge x = charge y := by
  constructor
  · rintro ⟨h⟩
    exact ⟨h.history_sound, h.charge_sound⟩
  · rintro ⟨hword, hcharge⟩
    exact ⟨.atom hword hcharge⟩

/-- Type-valued 15D comparison grammar with exactly ONE independent
source-typed exchange pair. The charge equality is explicit evidence
supplied to that generator, not an axiom or raw equality. -/
inductive NativeObserverExtendedFifteenCell {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (left right : A) :
    A → A → Type (max u v) where
  | core {x y : A}
      (h : NativeObserverCoreFifteenCell history charge x y) :
      NativeObserverExtendedFifteenCell history charge left right x y
  | squareExchange (hcharge : charge left = charge right) :
      NativeObserverExtendedFifteenCell history charge left right left right
  | symm {x y : A}
      (h : NativeObserverExtendedFifteenCell history charge left right x y) :
      NativeObserverExtendedFifteenCell history charge left right y x
  | trans {x y z : A}
      (h : NativeObserverExtendedFifteenCell history charge left right x y)
      (k : NativeObserverExtendedFifteenCell history charge left right y z) :
      NativeObserverExtendedFifteenCell history charge left right x z

/-- The independently extended 15D grammar still respects signed charge. -/
theorem NativeObserverExtendedFifteenCell.charge_sound
    {A : Type u} {W : Type v}
    {history : A → W} {charge : A → ℤ}
    {left right x y : A}
    (h : NativeObserverExtendedFifteenCell history charge left right x y) :
    charge x = charge y := by
  induction h with
  | core h => exact h.charge_sound
  | squareExchange hcharge => exact hcharge
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2

/-- Nonempty ACTUAL Type-valued 15D witness defines an equivalence
relation on the original raw 14D fiber, with no proof erasure
before the quotient is formed. -/
def NativeObserverExtendedFifteenCell.setoid
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (left right : A) : Setoid A where
  r := fun x y => Nonempty
    (NativeObserverExtendedFifteenCell history charge left right x y)
  iseqv := ⟨
    (fun x => ⟨.core (.refl x)⟩),
    (fun h => h.elim (fun witness => ⟨.symm witness⟩)),
    (fun first second =>
      first.elim (fun f => second.elim (fun s => ⟨.trans f s⟩)))⟩

abbrev NativeObserverFifteenClasses
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (left right : A) :=
  Quotient (NativeObserverExtendedFifteenCell.setoid
    history charge left right)

/-- The canonical integer observer on genuine fifteen-cell classes. -/
def nativeObserverFifteenCharge
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (left right : A) :
    NativeObserverFifteenClasses history charge left right → ℤ :=
  Quotient.lift charge (by
    intro x y related
    rcases related with ⟨h⟩
    exact h.charge_sound)

/-- An actual Type-valued independent 15-cell implies equality of
the ORIGINAL raw 14-cell witnesses only AFTER the 15D quotient. -/
theorem nativeObserverFifteen_square_quotient_eq
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (left right : A)
    (hcharge : charge left = charge right) :
    (Quotient.mk
       (NativeObserverExtendedFifteenCell.setoid history charge left right)
       left) =
    (Quotient.mk
       (NativeObserverExtendedFifteenCell.setoid history charge left right)
       right) :=
  Quot.sound ⟨NativeObserverExtendedFifteenCell.squareExchange hcharge⟩

/-- A general observer descends exactly when it respects EVERY
independent fifteen-cell comparison in the actual named quotient. -/
theorem nativeObserverFifteen_factors_iff
    {A : Type u} {W : Type v} {B : Type w}
    (history : A → W) (charge : A → ℤ)
    (left right : A) (obs : A → B) :
    (∃ F : NativeObserverFifteenClasses history charge left right → B,
      ∀ x, F (Quotient.mk
        (NativeObserverExtendedFifteenCell.setoid history charge left right) x) =
        obs x) ↔
    (∀ x y : A,
      Nonempty (NativeObserverExtendedFifteenCell
        history charge left right x y) → obs x = obs y) :=
  nativeHigherObserver_factors_iff
    (NativeObserverExtendedFifteenCell.setoid history charge left right) obs

/-- The chosen order-sensitive free-word history does NOT descend
when an adjoined fifteen-cell witnesses a history-separated pair. -/
theorem nativeObserverFifteen_history_noDescent
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (left right : A)
    (hcharge : charge left = charge right)
    (hword : history left ≠ history right) :
    ¬ ∃ F : NativeObserverFifteenClasses history charge left right → W,
      ∀ x, F (Quotient.mk
        (NativeObserverExtendedFifteenCell.setoid history charge left right) x) =
        history x := by
  exact nativeHigherObserver_no_descent
    (NativeObserverExtendedFifteenCell.setoid history charge left right)
    history
    ⟨NativeObserverExtendedFifteenCell.squareExchange hcharge⟩ hword

/-- No comparison in even the MAXIMAL observer-conservative
15D grammar can bridge a history-separated source-dependent pair. -/
theorem nativeObserverFifteen_noConservativeFiller
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    {x y : A} (hword : history x ≠ history y) :
    ¬ Nonempty (NativeObserverCoreFifteenCell history charge x y) := by
  rintro ⟨h⟩
  exact hword h.history_sound

/-- Reuse the dimension-polymorphic finite closure: NONE of its
arbitrarily many finite conservative stages fill this exact pair. -/
theorem nativeObserverFifteen_noFiniteCoreFiller
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    {x y : A} (hword : history x ≠ history y)
    (n : Nat) :
    ¬ Nonempty (NativeConservativeTower
      (NativeObserverCoreFifteenCell history charge) n x y) := by
  exact NativeConservativeTower.no_finite_filler
    history
    (fun {x y} (h : NativeObserverCoreFifteenCell history charge x y) =>
      h.history_sound)
    hword n

/-- In particular an adjoined 15D exchange cannot retract back into
any finite stage of the named conservative observer grammar. -/
theorem nativeObserverFifteen_noFiniteCoreRetraction
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (left right : A)
    (hcharge : charge left = charge right)
    (hword : history left ≠ history right)
    (n : Nat) :
    ¬ Nonempty
      (NativeObserverExtendedFifteenCell history charge left right left right →
        NativeConservativeTower
          (NativeObserverCoreFifteenCell history charge)
          n left right) := by
  exact NativeConservativeTower.no_finite_retraction
    history
    (fun {x y} (h : NativeObserverCoreFifteenCell history charge x y) =>
      h.history_sound)
    (NativeObserverExtendedFifteenCell.squareExchange hcharge)
    hword n

#print axioms NativeObserverCoreFifteenCell
#print axioms NativeObserverCoreFifteenCell.history_sound
#print axioms NativeObserverCoreFifteenCell.charge_sound
#print axioms nativeObserverCoreFifteen_filler_iff
#print axioms NativeObserverExtendedFifteenCell
#print axioms NativeObserverExtendedFifteenCell.charge_sound
#print axioms NativeObserverExtendedFifteenCell.setoid
#print axioms nativeObserverFifteenCharge
#print axioms nativeObserverFifteen_square_quotient_eq
#print axioms nativeObserverFifteen_factors_iff
#print axioms nativeObserverFifteen_history_noDescent
#print axioms nativeObserverFifteen_noConservativeFiller
#print axioms nativeObserverFifteen_noFiniteCoreFiller
#print axioms nativeObserverFifteen_noFiniteCoreRetraction

end
end Kuu.F112.Physical
