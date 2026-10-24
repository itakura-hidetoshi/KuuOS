import Mathlib.Tactic

/-!
# F112-P94D3AL — finite conservative coherence closure and descent

This layer is dimension-polymorphic: for ANY original dependent
boundary fiber of raw Type-valued higher cells, the conservative
comparison constructors preserve a chosen observer even after
arbitrarily many FINITE closure stages.

It does NOT flatten source-dependent witnesses into a graph.
Instantiate the abstract carrier with an exact original typed
boundary fiber and the primitive relation with its genuine
conservative cell grammar. The closure adds only identity, inverse,
transitivity, and finite inclusion; no independently adjoined
square-exchange is smuggled into the conservative tower.

The companion generic theorem characterizes observer descent
through an arbitrary genuine quotient and isolates its obstruction.
No global strict n-category or hyperdescent is inferred.
-/

namespace Kuu.F112.Physical

universe u v w

/-- Iterated finite conservative equality grammar. Stage zero already
contains every original conservative comparison. Further stages
permit only identity, inversion, composition and weakening.
The Nat index refers to formal closure stages, NOT geometric cell
dimension or an arbitrary new higher-cell operation. -/
inductive NativeConservativeTower {A : Type u}
    (Core : A → A → Type v) : Nat → A → A → Type (max u v) where
  | atom {x y : A} (h : Core x y) : NativeConservativeTower Core 0 x y
  | weaken {n : Nat} {x y : A}
      (h : NativeConservativeTower Core n x y) :
      NativeConservativeTower Core (n + 1) x y
  | refl {n : Nat} (x : A) : NativeConservativeTower Core n x x
  | symm {n : Nat} {x y : A}
      (h : NativeConservativeTower Core n x y) :
      NativeConservativeTower Core n y x
  | trans {n : Nat} {x y z : A}
      (h : NativeConservativeTower Core n x y)
      (k : NativeConservativeTower Core n y z) :
      NativeConservativeTower Core n x z

/-- Any observer conserved by each actual core generator is
conserved by EVERY finite conservative closure stage. -/
theorem NativeConservativeTower.observer_sound
    {A : Type u} {B : Type w} {Core : A → A → Type v}
    (obs : A → B)
    (coreSound : ∀ {x y : A}, Core x y → obs x = obs y)
    {n : Nat} {x y : A}
    (h : NativeConservativeTower Core n x y) :
    obs x = obs y := by
  induction h with
  | atom h => exact coreSound h
  | weaken _ ih => exact ih
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2

/-- A measured critical pair with unequal observed values has no
filler in ANY finite conservative closure stage. The obstruction
is relative to this exact named grammar and chosen observer. -/
theorem NativeConservativeTower.no_finite_filler
    {A : Type u} {B : Type w} {Core : A → A → Type v}
    (obs : A → B)
    (coreSound : ∀ {x y : A}, Core x y → obs x = obs y)
    {x y : A} (separated : obs x ≠ obs y) :
    ∀ n : Nat, ¬ Nonempty (NativeConservativeTower Core n x y) := by
  intro n
  rintro ⟨h⟩
  exact separated (h.observer_sound obs coreSound)

/-- At a genuine new comparison critical pair, a retraction of the
independently extended witness to any finite conservative stage is
impossible. This is NOT a no-go for richer grammars. -/
theorem NativeConservativeTower.no_finite_retraction
    {A : Type u} {B : Type w} {Core Extended : A → A → Type v}
    (obs : A → B)
    (coreSound : ∀ {x y : A}, Core x y → obs x = obs y)
    {x y : A}
    (newWitness : Extended x y)
    (separated : obs x ≠ obs y) :
    ∀ n : Nat, ¬ Nonempty
      (Extended x y → NativeConservativeTower Core n x y) := by
  intro n
  rintro ⟨retract⟩
  exact (NativeConservativeTower.no_finite_filler obs coreSound separated n)
    ⟨retract newWitness⟩

/-- Generic iff theorem for descent of an observer along an actual
quotient. No geometry, frame, or coherence is assumed implicitly. -/
theorem nativeHigherObserver_factors_iff
    {A : Type u} {B : Type w}
    (s : Setoid A) (obs : A → B) :
    (∃ F : Quotient s → B, ∀ x, F (Quotient.mk s x) = obs x) ↔
    (∀ x y : A, s.r x y → obs x = obs y) := by
  constructor
  · rintro ⟨F, hF⟩ x y related
    calc
      obs x = F (Quotient.mk s x) := (hF x).symm
      _ = F (Quotient.mk s y) := congrArg F (Quot.sound related)
      _ = obs y := hF y
  · intro compatible
    refine ⟨Quotient.lift obs (by
      intro x y related
      exact compatible x y related), ?_⟩
    intro x
    rfl

/-- A genuine quotient identifies two raw terms but an order-sensitive
observer distinguishes them; therefore the observer does not descend. -/
theorem nativeHigherObserver_no_descent
    {A : Type u} {B : Type w}
    (s : Setoid A) (obs : A → B)
    {x y : A} (related : s.r x y) (separated : obs x ≠ obs y) :
    ¬ ∃ F : Quotient s → B,
      ∀ z, F (Quotient.mk s z) = obs z := by
  intro h
  exact separated
    ((nativeHigherObserver_factors_iff s obs).mp h x y related)

/-- Exact independence of observers: a scalar can factor through the
same genuine quotient for which another observer fails to descend. -/
theorem nativeHigherObservers_independent
    {A : Type u} {B : Type w} {C : Type v}
    (s : Setoid A) (coarse : A → B) (fine : A → C)
    (coarseSound : ∀ x y : A, s.r x y → coarse x = coarse y)
    {x y : A} (related : s.r x y) (fineSeparated : fine x ≠ fine y) :
    (∃ F : Quotient s → B,
      ∀ z, F (Quotient.mk s z) = coarse z) ∧
    ¬ ∃ G : Quotient s → C,
      ∀ z, G (Quotient.mk s z) = fine z := by
  constructor
  · exact (nativeHigherObserver_factors_iff s coarse).mpr coarseSound
  · exact nativeHigherObserver_no_descent s fine related fineSeparated

#print axioms NativeConservativeTower
#print axioms NativeConservativeTower.observer_sound
#print axioms NativeConservativeTower.no_finite_filler
#print axioms NativeConservativeTower.no_finite_retraction
#print axioms nativeHigherObserver_factors_iff
#print axioms nativeHigherObserver_no_descent
#print axioms nativeHigherObservers_independent

end Kuu.F112.Physical
