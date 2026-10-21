import Kuu.F112.PolygonNativeF44ExchangeComposition

/-!
# F112-E7Q5-F4-M3 — complete native F44 exchange-class classification

The independent F44 raw constructor grammar retains BOTH distinct
independently typed primitive proofs as Type-valued histories.  The
ONLY quotient generator is adjacent swapping an F19 operation with
an independent F28 operation, in actual ordered contexts.

We prove every raw F44 word is exchange equivalent to the explicit
F19-first / F28-second normal form of its own COMPLETE history pair.
Thus equality in the generated quotient is equivalent (both ways)
to equality of those two Type-valued histories.  The quotient is
equivalent to their dependent typed product — not to a Prop existence
pair, scalar grade or categorical-Hom shadow.

No historical frozen F19/F28/F44 equivalence is asserted: historical
primitive OneStep is Prop while this independently built source's
primitive evidence remains in Type. No Gray/F51/F77 imports.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]

/-- Bubble a final actual F19 primitive across EVERY F28 operation
in an F19-first then F28-second word, via repeated genuine adjacent
squares; no same-axis operations are rearranged or collapsed. -/
theorem KuuNativeF44Ordered.firstThenSecond_snocFirst_class
    {a b : A} {x y : B} {n m : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb)
    (f : KuuNativeOneStep mb mc) :
    (KuuNativeF44Ordered.first
      (KuuNativeF44Ordered.firstThenSecond h₁ h₂) f).toExchangeClass =
    (KuuNativeF44Ordered.firstThenSecond
      (KuuNativeAxisTrace.snoc h₁ f) h₂).toExchangeClass := by
  induction h₂ with
  | refl pa =>
      rfl
  | snoc h₂ s ih =>
      have hs :
        (KuuNativeF44Ordered.second
          (KuuNativeF44Ordered.first
            (KuuNativeF44Ordered.firstThenSecond h₁ h₂) f) s).toExchangeClass =
        (KuuNativeF44Ordered.first
          (KuuNativeF44Ordered.second
            (KuuNativeF44Ordered.firstThenSecond h₁ h₂) s) f).toExchangeClass :=
        Quot.sound (KuuNativeF44AdjacentSwap.square
          (KuuNativeF44Ordered.firstThenSecond h₁ h₂) f s)
      change
        (KuuNativeF44Ordered.first
          (KuuNativeF44Ordered.second
            (KuuNativeF44Ordered.firstThenSecond h₁ h₂) s) f).toExchangeClass =
        (KuuNativeF44Ordered.second
          (KuuNativeF44Ordered.firstThenSecond
            (KuuNativeAxisTrace.snoc h₁ f) h₂) s).toExchangeClass
      exact hs.symm.trans
        (congrArg (fun c => c.afterSecond s) ih)

/-- Full F44 word normalization: only actual adjacent swaps can
reach the canonical F19-then-F28 execution of precisely the
original two proof-relevant, uncollapsed axis histories. -/
theorem KuuNativeF44Ordered.toExchangeClass_eq_normal
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (p : KuuNativeF44Ordered n m ma pa mb pb) :
    p.toExchangeClass =
      (KuuNativeF44Ordered.firstThenSecond
        p.firstHistory p.secondHistory).toExchangeClass := by
  induction p with
  | refl ma pa =>
      rfl
  | first p f ih =>
      change (KuuNativeF44Ordered.first p f).toExchangeClass =
        (KuuNativeF44Ordered.firstThenSecond
          (KuuNativeAxisTrace.snoc p.firstHistory f)
          p.secondHistory).toExchangeClass
      exact
        (congrArg (fun c => c.afterFirst f) ih).trans
          (KuuNativeF44Ordered.firstThenSecond_snocFirst_class
            p.firstHistory p.secondHistory f)
  | second p s ih =>
      change (KuuNativeF44Ordered.second p s).toExchangeClass =
        (KuuNativeF44Ordered.second
          (KuuNativeF44Ordered.firstThenSecond
            p.firstHistory p.secondHistory) s).toExchangeClass
      exact congrArg (fun c => c.afterSecond s) ih

/-- COMPLETE faithfulness of the actual generated exchange quotient
to the PAIR of Type-valued axes, in both directions: this does not
say raw F44 paths or old Prop-valued primitive proofs are equal. -/
theorem kuuNativeF44Class_eq_iff_histories_eq
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (p q : KuuNativeF44Ordered n m ma pa mb pb) :
    p.toExchangeClass = q.toExchangeClass ↔
      p.histories = q.histories := by
  constructor
  · intro h
    exact (p.histories_toExchangeClass).symm.trans
      ((congrArg KuuNativeF44ExchangeClass.histories h).trans
        q.histories_toExchangeClass)
  · intro h
    calc
      p.toExchangeClass =
          (KuuNativeF44Ordered.firstThenSecond
            p.firstHistory p.secondHistory).toExchangeClass :=
        p.toExchangeClass_eq_normal
      _ = (KuuNativeF44Ordered.firstThenSecond
            q.firstHistory q.secondHistory).toExchangeClass :=
        congrArg
          (fun t : KuuNativeAxisTrace n ma mb ×
              KuuNativeAxisTrace m pa pb =>
            (KuuNativeF44Ordered.firstThenSecond t.1 t.2).toExchangeClass) h
      _ = q.toExchangeClass :=
        q.toExchangeClass_eq_normal.symm

/-- The independently constructed source exchange Quot has an
actual Mathlib equivalence with the full product of the two
proof-relevant native histories; no additional Gray law is used. -/
def KuuNativeF44ExchangeClass.historyEquiv
    {a b : A} {x y : B} {n m : Nat}
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    KuuNativeF44ExchangeClass n m ma mb pa pb ≃
      (KuuNativeAxisTrace n ma mb ×
        KuuNativeAxisTrace m pa pb) where
  toFun := KuuNativeF44ExchangeClass.histories
  invFun := fun h =>
    (KuuNativeF44Ordered.firstThenSecond h.1 h.2).toExchangeClass
  left_inv := by
    intro c
    refine Quot.inductionOn c ?_
    intro p
    exact (KuuNativeF44Ordered.toExchangeClass_eq_normal p).symm
  right_inv := by
    intro h
    cases h with
    | mk h₁ h₂ =>
        exact KuuNativeF44Ordered.fromF45Order_histories
          .firstAxisFirst h₁ h₂

/-- Any two original-shaped F45 execution orders give the SAME
generated exchange class for arbitrary complete independent Nat
histories, not just the unit example.  The two raw orders generally
remain distinct before this quotient. -/
theorem KuuNativeF44Ordered.fromF45Order_class_independent
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (o₁ o₂ : KuuNativeF45Order)
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    (KuuNativeF44Ordered.fromF45Order o₁ h₁ h₂).toExchangeClass =
      (KuuNativeF44Ordered.fromF45Order o₂ h₁ h₂).toExchangeClass := by
  apply (kuuNativeF44Class_eq_iff_histories_eq _ _).2
  exact (KuuNativeF44Ordered.fromF45Order_histories o₁ h₁ h₂).trans
    (KuuNativeF44Ordered.fromF45Order_histories o₂ h₁ h₂).symm

/-- Two arbitrary F45 original-shaped binary trees whose ENTIRE
Type-valued two-axis histories agree have equal F44 exchange-class
components, without forcing their genuine physical C60 bracket
components to be equal. -/
theorem KuuNativeF45Tree.exchangePacket_class_eq_of_histories_eq
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first second : KuuNativeF45Tree p n m ma pa mb pb)
    (h : first.axisHistories = second.axisHistories) :
    first.exchangePacket.2 = second.exchangePacket.2 := by
  apply (KuuNativeF44ExchangeClass.historyEquiv ma mb pa pb).injective
  calc
    first.exchangePacket.2.histories = first.axisHistories :=
      first.exchangePacket_histories
    _ = second.axisHistories := h
    _ = second.exchangePacket.2.histories :=
      second.exchangePacket_histories.symm

#print axioms KuuNativeF44Ordered.firstThenSecond_snocFirst_class
#print axioms KuuNativeF44Ordered.toExchangeClass_eq_normal
#print axioms kuuNativeF44Class_eq_iff_histories_eq
#print axioms KuuNativeF44ExchangeClass.historyEquiv
#print axioms KuuNativeF44Ordered.fromF45Order_class_independent
#print axioms KuuNativeF45Tree.exchangePacket_class_eq_of_histories_eq
end
end Kuu.F112.Physical
