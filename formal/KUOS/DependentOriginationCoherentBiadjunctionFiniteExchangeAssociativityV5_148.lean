import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45SequentialCoherenceV5_147

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F51-A / v5.148 — actual finite F19/F28 exchange-path associativity and units

The F44 generated quotient carries an actual path concatenation;
F50 proves a two-stage sequential law on the ORIGINAL F45 routes.
The exact Nat-valued F19 and F28 primitive depths do not associate
definitionally for general symbolic depths, so the correct native
associativity uses their *explicit dependent index transport*.

We prove associativity of the ORIGINAL Type-valued per-axis histories,
the independent two-depth cast of the genuine generated quotient,
and its associativity and left/right units. These are equalities of
genuine generated F44 exchange classes, NOT equality of endpoint
Hom composites or new permutations of same-axis steps.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Genuine Type-valued single-axis refinement history concatenation
is associative UP TO THE REQUIRED Nat.add_assoc dependent cast,
without rearranging any same-axis OneStep operations. -/
theorem AxisTrace.append_assoc
    {a b : D} {n n' n'' : Nat}
    {ma mb mc md : Blocks a b}
    (h : AxisTrace n ma mb)
    (k : AxisTrace n' mb mc)
    (l : AxisTrace n'' mc md) :
    AxisTrace.castDepth (Nat.add_assoc n n' n'')
      (AxisTrace.append (AxisTrace.append h k) l) =
    AxisTrace.append h (AxisTrace.append k l) := by
  induction l with
  | refl =>
      rfl
  | snoc l step ih =>
      have hcast :=
        AxisTrace.castDepth_snoc
          (Nat.add_assoc n n' _) (AxisTrace.append (AxisTrace.append h k) l) step
      have hnext :=
        congrArg (fun t => AxisTrace.snoc t step) (ih k)
      simpa only [AxisTrace.append, Nat.add_succ] using hcast.trans hnext

/-- The reflexive genuine F44 path is the unit of the generated
exchange quotient at the SAME independently typed source blocks. -/
def ExchangeClass.reflClass
    {a b : D} {x y : E}
    (ma : Blocks a b) (pa : Blocks x y) :
    ExchangeClass 0 0 ma ma pa pa :=
  (OrderedInterleaving.refl ma pa).toClass

/-- Explicit pair of native dependent index transports for the TWO
independent original F19/F28 finite depths in the generated quotient. -/
def ExchangeClass.castDepths
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hn : n = n') (hm : m = m')
    (c : ExchangeClass n m ma mb pa pb) :
    ExchangeClass n' m' ma mb pa pb := by
  cases hn
  cases hm
  exact c

/-- BOTH complete original Type-valued axis histories are transported
independently along the same two natural-number depth equalities. -/
theorem ExchangeClass.castDepths_axisTraces
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hn : n = n') (hm : m = m')
    (c : ExchangeClass n m ma mb pa pb) :
    (ExchangeClass.castDepths hn hm c).axisTraces =
      (AxisTrace.castDepth hn c.axisTraces.1,
       AxisTrace.castDepth hm c.axisTraces.2) := by
  cases hn
  cases hm
  rfl

/-- The two independently typed native history projections of the
actual F44 reflexive class are the exact zero-step witnesses. -/
theorem ExchangeClass.reflClass_axisTraces
    {a b : D} {x y : E}
    (ma : Blocks a b) (pa : Blocks x y) :
    (ExchangeClass.reflClass ma pa).axisTraces =
      (AxisTrace.refl ma, AxisTrace.refl pa) :=
  rfl

/-- Genuine F44 generated exchange quotient concatenation is
ASSOCIATIVE, with its two Nat.add_assoc dependent index casts made
explicit and no extra identifications between same-axis histories. -/
theorem ExchangeClass.append_assoc
    {a b : D} {x y : E}
    {n n' n'' m m' m'' : Nat}
    {ma mb mc md : Blocks a b}
    {pa pb pc pd : Blocks x y}
    (h : ExchangeClass n m ma mb pa pb)
    (k : ExchangeClass n' m' mb mc pb pc)
    (l : ExchangeClass n'' m'' mc md pc pd) :
    ExchangeClass.castDepths
        (Nat.add_assoc n n' n'') (Nat.add_assoc m m' m'')
        (ExchangeClass.append (ExchangeClass.append h k) l) =
      ExchangeClass.append h (ExchangeClass.append k l) := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  simpa only [ExchangeClass.castDepths_axisTraces,
    ExchangeClass.axisTraces_append] using
    (Prod.ext
      (AxisTrace.append_assoc h.axisTraces.1 k.axisTraces.1 l.axisTraces.1)
      (AxisTrace.append_assoc h.axisTraces.2 k.axisTraces.2 l.axisTraces.2))

/-- Genuine right unit: after any original finite F19/F28 exchange
path, appending the native zero-step reflexive class changes NOTHING. -/
theorem ExchangeClass.append_refl_right
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (h : ExchangeClass n m ma mb pa pb) :
    ExchangeClass.append h (ExchangeClass.reflClass mb pb) = h := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  simp only [ExchangeClass.axisTraces_append,
    ExchangeClass.reflClass_axisTraces,
    AxisTrace.append_refl_right, Nat.add_zero]

/-- Genuine left unit: the original zero-step class concatenated with
an arbitrary F19/F28 exchange path is EXACTLY the same class after
the two required Nat.zero_add dependent index transports. -/
theorem ExchangeClass.append_refl_left
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (h : ExchangeClass n m ma mb pa pb) :
    ExchangeClass.castDepths (Nat.zero_add n) (Nat.zero_add m)
      (ExchangeClass.append (ExchangeClass.reflClass ma pa) h) = h := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  simp only [ExchangeClass.castDepths_axisTraces,
    ExchangeClass.axisTraces_append,
    ExchangeClass.reflClass_axisTraces,
    AxisTrace.append_refl_left_cast]

#print axioms AxisTrace.append_assoc
#print axioms ExchangeClass.reflClass
#print axioms ExchangeClass.castDepths
#print axioms ExchangeClass.castDepths_axisTraces
#print axioms ExchangeClass.reflClass_axisTraces
#print axioms ExchangeClass.append_assoc
#print axioms ExchangeClass.append_refl_right
#print axioms ExchangeClass.append_refl_left

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
