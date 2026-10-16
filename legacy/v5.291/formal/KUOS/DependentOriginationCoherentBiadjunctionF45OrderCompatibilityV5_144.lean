import KUOS.DependentOriginationCoherentBiadjunctionModificationNormalFormV5_144

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F47-B / v5.144 — genuine quotient concatenation preserves complete axis histories

F44 supplies genuine concatenation of full Type-valued F19/F28
primitive refinement paths and a sound concatenation on its generated
adjacent-exchange quotient. F45 separately extracts the two complete
native histories, preserving intermediate Blocks and exact depths.

Here we prove that the F44 quotient concatenation corresponds
*exactly* to independent F19/F28 Type-valued history concatenation.
Unlike the original F45 standard-order definitions, this theorem does
not rely on unnormalized Eq.mp transports from Nat.zero_add; it follows
directly by induction on the actual full ordered route and by sound
elimination from the quotient. No same-axis moves are identified.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Concatenate native single-axis histories with the exact n+n'
number of F42 genuine primitive refinement operations. -/
def AxisTrace.append
    {a b : D} {n n' : Nat}
    {ma mb mc : Blocks a b}
    (h : AxisTrace n ma mb) (k : AxisTrace n' mb mc) :
    AxisTrace (n + n') ma mc := by
  induction k with
  | refl =>
      simpa only [Nat.add_zero] using h
  | snoc k step ih =>
      simpa only [Nat.add_succ] using
        (AxisTrace.snoc (ih h) step)

/-- Both F44 ordered path concatenation and native F19 history
concatenation retain exactly the same proof-relevant operation list. -/
theorem OrderedInterleaving.modificationTrace_append
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (h : OrderedInterleaving n m ma pa mb pb)
    (k : OrderedInterleaving n' m' mb pb mc pc) :
    (OrderedInterleaving.append h k).modificationTrace =
      AxisTrace.append h.modificationTrace k.modificationTrace := by
  induction k with
  | refl =>
      rfl
  | modification k step ih =>
      exact congrArg (fun t => AxisTrace.snoc t step) (ih h)
  | comparison k step ih =>
      exact ih h

/-- An independent F28 trace is transported in precisely the same
m+m' manner under a full F44 two-axis concatenation. -/
theorem OrderedInterleaving.comparisonTrace_append
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (h : OrderedInterleaving n m ma pa mb pb)
    (k : OrderedInterleaving n' m' mb pb mc pc) :
    (OrderedInterleaving.append h k).comparisonTrace =
      AxisTrace.append h.comparisonTrace k.comparisonTrace := by
  induction k with
  | refl =>
      rfl
  | modification k step ih =>
      exact ih h
  | comparison k step ih =>
      exact congrArg (fun t => AxisTrace.snoc t step) (ih h)

/-- A genuine zero-step suffix likewise leaves the original
same-axis intermediate block history exactly unchanged. -/
theorem AxisTrace.append_refl_right
    {a b : D} {n : Nat} {ma mb : Blocks a b}
    (hm : AxisTrace n ma mb) :
    AxisTrace.append hm (AxisTrace.refl mb) = hm :=
  rfl

/-- The two native complete Type-valued original histories add
independently when genuine F44 ordered paths are concatenated. -/
theorem OrderedInterleaving.axisTraces_append
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (h : OrderedInterleaving n m ma pa mb pb)
    (k : OrderedInterleaving n' m' mb pb mc pc) :
    (OrderedInterleaving.append h k).modificationTrace =
        AxisTrace.append h.modificationTrace k.modificationTrace ∧
      (OrderedInterleaving.append h k).comparisonTrace =
        AxisTrace.append h.comparisonTrace k.comparisonTrace :=
  ⟨OrderedInterleaving.modificationTrace_append h k,
    OrderedInterleaving.comparisonTrace_append h k⟩

/-- Genuine concatenation ON THE F44 GENERATED EXCHANGE QUOTIENT
corresponds exactly to independent native concatenation of BOTH
complete Type-valued F19/F28 axis histories.

This is not a postulated equation between original categorical
composite arrows: both equalities are proved by the original F44
Quot eliminator and Type-valued path constructors. -/
theorem ExchangeClass.axisTraces_append
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (h : ExchangeClass n m ma mb pa pb)
    (k : ExchangeClass n' m' mb mc pb pc) :
    (ExchangeClass.append h k).axisTraces =
      (AxisTrace.append h.axisTraces.1 k.axisTraces.1,
       AxisTrace.append h.axisTraces.2 k.axisTraces.2) := by
  refine Quot.induction_on h ?_
  intro route₁
  refine Quot.induction_on k ?_
  intro route₂
  exact Prod.ext
    (OrderedInterleaving.modificationTrace_append route₁ route₂)
    (OrderedInterleaving.comparisonTrace_append route₁ route₂)

#print axioms AxisTrace.append
#print axioms OrderedInterleaving.modificationTrace_append
#print axioms OrderedInterleaving.comparisonTrace_append
#print axioms AxisTrace.append_refl_right
#print axioms OrderedInterleaving.axisTraces_append
#print axioms ExchangeClass.axisTraces_append

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
