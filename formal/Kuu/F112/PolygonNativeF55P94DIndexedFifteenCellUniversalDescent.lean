import Kuu.F112.PolygonNativeF55P94DObserverFifteenCellDescent

/-!
# F112-P94D3AP — indexed independent fifteen-cell comparisons

The *original* raw fourteen-cell fiber is kept as a Type.  An arbitrary
index type can name many independently ADJOINED Type-valued fifteen-cell
exchanges.  Each named exchange requires explicit charge compatibility;
none follows merely from equality of scalar observations.

The extended closure is initial among equivalence relations containing
both the maximal conservative (history, charge) kernel and all named
independent exchanges.  Its quotient has an exact observer descent iff:
- the observer respects EVERY conservative kernel pair, and
- it respects EVERY separately named independent exchange.

The signed charge descends; a history-separated named exchange prevents
free-group history descent, and has no finite conservative filler or
retraction.  The singleton family is proven equivalent to P94D3AO's
actual independent fifteen-cell syntax, not silently equated by fiat.

This is a *presentation-relative* statement, not a full geometric
15-cell grammar, global strict n-category, or hyperdescent theorem.
-/

namespace Kuu.F112.Physical

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v w z

/-- Type-valued fifteen-cell closure under a FAMILY of independent,
source-indexed exchanges.  The charge equality is externally supplied
evidence; `exchange` is a genuinely independent new constructor. -/
inductive NativeFifteenFamilyCell {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    {I : Type w} (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i)) :
    A → A → Type (max (max u v) w) where
  | conservative {x y : A}
      (h : NativeObserverCoreFifteenCell history charge x y) :
      NativeFifteenFamilyCell history charge left right chargeEq x y
  | exchange (i : I) :
      NativeFifteenFamilyCell history charge left right chargeEq
        (left i) (right i)
  | symm {x y : A}
      (h : NativeFifteenFamilyCell history charge left right chargeEq x y) :
      NativeFifteenFamilyCell history charge left right chargeEq y x
  | trans {x y z : A}
      (h : NativeFifteenFamilyCell history charge left right chargeEq x y)
      (k : NativeFifteenFamilyCell history charge left right chargeEq y z) :
      NativeFifteenFamilyCell history charge left right chargeEq x z

/-- Every actual comparison in the indexed syntax preserves charge. -/
theorem NativeFifteenFamilyCell.charge_sound
    {A : Type u} {W : Type v} {I : Type w}
    {history : A → W} {charge : A → ℤ}
    {left right : I → A}
    {chargeEq : ∀ i : I, charge (left i) = charge (right i)}
    {x y : A}
    (h : NativeFifteenFamilyCell history charge left right chargeEq x y) :
    charge x = charge y := by
  induction h with
  | conservative base => exact base.charge_sound
  | exchange i => exact chargeEq i
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2

/-- The induction principle for ALL compatible observers, including
observers other than the two used to choose the conservative grammar. -/
theorem NativeFifteenFamilyCell.observer_sound
    {A : Type u} {W : Type v} {I : Type w} {B : Type z}
    {history : A → W} {charge : A → ℤ}
    {left right : I → A}
    {chargeEq : ∀ i : I, charge (left i) = charge (right i)}
    (obs : A → B)
    (coreSound : ∀ x y : A,
      history x = history y → charge x = charge y → obs x = obs y)
    (exchangeSound : ∀ i : I, obs (left i) = obs (right i))
    {x y : A}
    (h : NativeFifteenFamilyCell history charge left right chargeEq x y) :
    obs x = obs y := by
  induction h with
  | conservative base =>
      exact coreSound _ _ base.history_sound base.charge_sound
  | exchange i => exact exchangeSound i
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2

/-- GENUINE Type-valued comparisons induce an equivalence on raw
fourteen-cell proof terms, only AFTER which classes are formed. -/
def NativeFifteenFamilyCell.setoid
    {A : Type u} {W : Type v} {I : Type w}
    (history : A → W) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i)) :
    Setoid A where
  r := fun x y => Nonempty
    (NativeFifteenFamilyCell history charge left right chargeEq x y)
  iseqv := ⟨
    (fun x => ⟨.conservative (.refl x)⟩),
    (fun h => h.elim (fun witness => ⟨.symm witness⟩)),
    (fun h k =>
      h.elim (fun f => k.elim (fun g => ⟨.trans f g⟩)))⟩

abbrev NativeFifteenFamilyClasses
    {A : Type u} {W : Type v} {I : Type w}
    (history : A → W) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i)) :=
  Quotient (NativeFifteenFamilyCell.setoid
    history charge left right chargeEq)

/-- EXACT universal descent criterion: preserving charge alone is
insufficient for an arbitrary observer, and every exchange must be
checked separately. -/
theorem nativeFifteenFamily_factors_iff
    {A : Type u} {W : Type v} {I : Type w} {B : Type z}
    (history : A → W) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    (obs : A → B) :
    (∃ F : NativeFifteenFamilyClasses history charge left right chargeEq → B,
      ∀ x : A,
        F (Quotient.mk (NativeFifteenFamilyCell.setoid
          history charge left right chargeEq) x) = obs x) ↔
    (∀ x y : A,
      history x = history y → charge x = charge y → obs x = obs y) ∧
    (∀ i : I, obs (left i) = obs (right i)) := by
  constructor
  · intro h
    have hrespects : ∀ x y : A,
        Nonempty (NativeFifteenFamilyCell
          history charge left right chargeEq x y) → obs x = obs y :=
      (nativeHigherObserver_factors_iff
        (NativeFifteenFamilyCell.setoid history charge left right chargeEq)
        obs).mp h
    constructor
    · intro x y hword hcharge
      exact hrespects x y
        ⟨NativeFifteenFamilyCell.conservative (.atom hword hcharge)⟩
    · intro i
      exact hrespects (left i) (right i)
        ⟨NativeFifteenFamilyCell.exchange i⟩
  · rintro ⟨hcore, hexchange⟩
    apply (nativeHigherObserver_factors_iff
      (NativeFifteenFamilyCell.setoid history charge left right chargeEq)
      obs).mpr
    intro x y related
    rcases related with ⟨h⟩
    exact h.observer_sound obs hcore hexchange

/-- Among compatible setoids, this generated relation is the LEAST:
all observations and contexts preserving its generators automatically
preserve every pasting of those generators. -/
theorem nativeFifteenFamily_setoid_minimal
    {A : Type u} {W : Type v} {I : Type w}
    (history : A → W) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    (s : Setoid A)
    (coreRel : ∀ x y : A,
      history x = history y → charge x = charge y → s.r x y)
    (exchangeRel : ∀ i : I, s.r (left i) (right i))
    {x y : A}
    (related : (NativeFifteenFamilyCell.setoid
      history charge left right chargeEq).r x y) :
    s.r x y := by
  rcases related with ⟨h⟩
  induction h with
  | conservative base =>
      exact coreRel _ _ base.history_sound base.charge_sound
  | exchange i => exact exchangeRel i
  | symm _ ih => exact s.iseqv.symm ih
  | trans _ _ ih1 ih2 => exact s.iseqv.trans ih1 ih2

/-- Canonical comparison of quotient presentations into ANY coarser
compatible quotient.  No arbitrary raw proof identification is made. -/
def nativeFifteenFamily_toCoarser
    {A : Type u} {W : Type v} {I : Type w}
    (history : A → W) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    (s : Setoid A)
    (coreRel : ∀ x y : A,
      history x = history y → charge x = charge y → s.r x y)
    (exchangeRel : ∀ i : I, s.r (left i) (right i)) :
    NativeFifteenFamilyClasses history charge left right chargeEq →
      Quotient s :=
  Quotient.lift (fun x => Quotient.mk s x) (by
    intro x y related
    exact Quot.sound
      (nativeFifteenFamily_setoid_minimal
        history charge left right chargeEq
        s coreRel exchangeRel related))

/-- The comparison commutes EXACTLY with all original witnesses. -/
theorem nativeFifteenFamily_toCoarser_mk
    {A : Type u} {W : Type v} {I : Type w}
    (history : A → W) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    (s : Setoid A)
    (coreRel : ∀ x y : A,
      history x = history y → charge x = charge y → s.r x y)
    (exchangeRel : ∀ i : I, s.r (left i) (right i))
    (x : A) :
    nativeFifteenFamily_toCoarser
      history charge left right chargeEq s coreRel exchangeRel
      (Quotient.mk
        (NativeFifteenFamilyCell.setoid history charge left right chargeEq)
        x) = Quotient.mk s x := rfl

/-- Signed integer charge factors on ALL original raw witnesses. -/
def nativeFifteenFamilyCharge
    {A : Type u} {W : Type v} {I : Type w}
    (history : A → W) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i)) :
    NativeFifteenFamilyClasses history charge left right chargeEq → ℤ :=
  Quotient.lift charge (by
    intro x y related
    rcases related with ⟨h⟩
    exact h.charge_sound)

/-- No representative choice is needed for this all-raw charge factor. -/
theorem nativeFifteenFamily_charge_mk
    {A : Type u} {W : Type v} {I : Type w}
    (history : A → W) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    (x : A) :
    nativeFifteenFamilyCharge history charge left right chargeEq
      (Quotient.mk
        (NativeFifteenFamilyCell.setoid history charge left right chargeEq)
        x) = charge x := rfl

/-- A single named history-separated independent exchange obstructs
global descent of the ordered word, even if all charges agree. -/
theorem nativeFifteenFamily_history_noDescent
    {A : Type u} {W : Type v} {I : Type w}
    (history : A → W) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    (i : I)
    (hword : history (left i) ≠ history (right i)) :
    ¬ ∃ F : NativeFifteenFamilyClasses
        history charge left right chargeEq → W,
      ∀ x : A,
        F (Quotient.mk
          (NativeFifteenFamilyCell.setoid history charge left right chargeEq)
          x) = history x :=
  nativeHigherObserver_no_descent
    (NativeFifteenFamilyCell.setoid history charge left right chargeEq)
    history ⟨NativeFifteenFamilyCell.exchange i⟩ hword

/-- An arbitrary number of OTHER generators cannot produce a filler
inside the named observer-conservative grammar for this separated pair. -/
theorem nativeFifteenFamily_noFiniteCoreFiller
    {A : Type u} {W : Type v} {I : Type w}
    (history : A → W) (charge : A → ℤ)
    (left right : I → A)
    (_chargeEq : ∀ i : I, charge (left i) = charge (right i))
    (i : I)
    (hword : history (left i) ≠ history (right i))
    (n : Nat) :
    ¬ Nonempty (NativeConservativeTower
      (NativeObserverCoreFifteenCell history charge)
      n (left i) (right i)) :=
  NativeConservativeTower.no_finite_filler
    history
    (fun {x y} (h : NativeObserverCoreFifteenCell history charge x y) =>
      h.history_sound)
    hword n

/-- The independently adjoined indexed exchange cannot retract to
any finite conservative stage at a history-separated raw boundary. -/
theorem nativeFifteenFamily_noFiniteCoreRetraction
    {A : Type u} {W : Type v} {I : Type w}
    (history : A → W) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    (i : I)
    (hword : history (left i) ≠ history (right i))
    (n : Nat) :
    ¬ Nonempty
      (NativeFifteenFamilyCell history charge left right chargeEq
          (left i) (right i) →
        NativeConservativeTower
          (NativeObserverCoreFifteenCell history charge)
          n (left i) (right i)) :=
  NativeConservativeTower.no_finite_retraction
    history
    (fun {x y} (h : NativeObserverCoreFifteenCell history charge x y) =>
      h.history_sound)
    (NativeFifteenFamilyCell.exchange i) hword n

/-- Singleton families recover AO's single independent exchange,
including the Type-valued witnesses, by structural recursion. -/
theorem nativeFifteenSingleton_toAO
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (left right : A) (hcharge : charge left = charge right)
    {x y : A}
    (h : NativeFifteenFamilyCell history charge
      (fun _ : Unit => left) (fun _ : Unit => right)
      (fun _ : Unit => hcharge) x y) :
    NativeObserverExtendedFifteenCell history charge left right x y := by
  induction h with
  | conservative base => exact .core base
  | exchange _ => exact .squareExchange hcharge
  | symm _ ih => exact .symm ih
  | trans _ _ ih1 ih2 => exact .trans ih1 ih2

/-- Conversely AO's original independent comparison is represented
by the singleton indexed family, without identifying raw 14D terms. -/
theorem nativeFifteenSingleton_fromAO
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (left right : A) (hcharge : charge left = charge right)
    {x y : A}
    (h : NativeObserverExtendedFifteenCell
      history charge left right x y) :
    NativeFifteenFamilyCell history charge
      (fun _ : Unit => left) (fun _ : Unit => right)
      (fun _ : Unit => hcharge) x y := by
  induction h with
  | core base => exact .conservative base
  | squareExchange _ => exact .exchange ()
  | symm _ ih => exact .symm ih
  | trans _ _ ih1 ih2 => exact .trans ih1 ih2

/-- The TWO typed presentations induce precisely the SAME equivalence
relation on raw witnesses for the singleton family. -/
theorem nativeFifteenSingleton_related_iff
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (left right : A) (hcharge : charge left = charge right)
    (x y : A) :
    (NativeFifteenFamilyCell.setoid history charge
      (fun _ : Unit => left) (fun _ : Unit => right)
      (fun _ : Unit => hcharge)).r x y ↔
    (NativeObserverExtendedFifteenCell.setoid
      history charge left right).r x y := by
  constructor
  · rintro ⟨h⟩
    exact ⟨nativeFifteenSingleton_toAO
      history charge left right hcharge h⟩
  · rintro ⟨h⟩
    exact ⟨nativeFifteenSingleton_fromAO
      history charge left right hcharge h⟩

/-- Explicit presentation-transport EQUIVALENCE (not just a bijection
of scalar observations), between independently generated 15D quotients. -/
def nativeFifteenSingleton_quotientEquiv
    {A : Type u} {W : Type v}
    (history : A → W) (charge : A → ℤ)
    (left right : A) (hcharge : charge left = charge right) :
    NativeFifteenFamilyClasses history charge
      (fun _ : Unit => left) (fun _ : Unit => right)
      (fun _ : Unit => hcharge) ≃
    NativeObserverFifteenClasses history charge left right where
  toFun := Quotient.lift
    (fun x => Quotient.mk
      (NativeObserverExtendedFifteenCell.setoid history charge left right) x)
    (by
      intro x y h
      exact Quot.sound
        ((nativeFifteenSingleton_related_iff
          history charge left right hcharge x y).mp h))
  invFun := Quotient.lift
    (fun x => Quotient.mk
      (NativeFifteenFamilyCell.setoid history charge
        (fun _ : Unit => left) (fun _ : Unit => right)
        (fun _ : Unit => hcharge)) x)
    (by
      intro x y h
      exact Quot.sound
        ((nativeFifteenSingleton_related_iff
          history charge left right hcharge x y).mpr h))
  left_inv := by
    intro q
    refine Quotient.inductionOn q ?_
    intro x
    rfl
  right_inv := by
    intro q
    refine Quotient.inductionOn q ?_
    intro x
    rfl

#print axioms NativeFifteenFamilyCell
#print axioms NativeFifteenFamilyCell.charge_sound
#print axioms NativeFifteenFamilyCell.observer_sound
#print axioms NativeFifteenFamilyCell.setoid
#print axioms NativeFifteenFamilyClasses
#print axioms nativeFifteenFamily_factors_iff
#print axioms nativeFifteenFamily_setoid_minimal
#print axioms nativeFifteenFamily_toCoarser
#print axioms nativeFifteenFamily_toCoarser_mk
#print axioms nativeFifteenFamilyCharge
#print axioms nativeFifteenFamily_charge_mk
#print axioms nativeFifteenFamily_history_noDescent
#print axioms nativeFifteenFamily_noFiniteCoreFiller
#print axioms nativeFifteenFamily_noFiniteCoreRetraction
#print axioms nativeFifteenSingleton_toAO
#print axioms nativeFifteenSingleton_fromAO
#print axioms nativeFifteenSingleton_related_iff
#print axioms nativeFifteenSingleton_quotientEquiv

end
end Kuu.F112.Physical
