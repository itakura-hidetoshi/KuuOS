import KUOS.DependentOriginationCoherentBiadjunctionExchangeNormalFormNaturalityV5_143

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid

set_option autoImplicit false
noncomputable section

/-!
# F47-A / v5.144 — genuine F19-first realization of the F46 exchange normal form

F46 constructs a F28-first canonical representative. Here we construct
the opposite native F19-first route directly from the TWO full original
Type-valued histories, without ever identifying the F19 modification
category with the genuine F28 compression-kernel quotient category.

Every F19-first path retains its original intermediate Blocks and
OneStep constructors. The F44 generating adjacent exchanges, and
NOT equality of evaluated Hom composites, identify the two actual
orderings in the quotient. We prove complete original-history recovery
before connecting to the unchanged actual source η / target ε mates.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A genuine pure F19 primitive trace realizes EXACTLY its original
Type-level intermediate block history, not merely a F42 Prop trace. -/
theorem AxisTrace.toModificationInterleaving_modificationTrace
    {a b : D} {x y : E} {n : Nat}
    {ma mb : Blocks a b}
    (hm : AxisTrace n ma mb) (pa : Blocks x y) :
    (AxisTrace.toModificationInterleaving hm pa).modificationTrace = hm := by
  induction hm with
  | refl p => rfl
  | snoc hm step ih =>
      exact congrArg (fun t => AxisTrace.snoc t step) ih

/-- The same pure F19 trace leaves the independently typed F28 axis
as its original zero-step identity witness. -/
theorem AxisTrace.toModificationInterleaving_comparisonTrace
    {a b : D} {x y : E} {n : Nat}
    {ma mb : Blocks a b}
    (hm : AxisTrace n ma mb) (pa : Blocks x y) :
    (AxisTrace.toModificationInterleaving hm pa).comparisonTrace =
      AxisTrace.refl pa := by
  induction hm with
  | refl p => rfl
  | snoc hm step ih => exact ih

/-- Realize the opposite, F19-FIRST actual ordered path by first
carrying out ALL original F19 refinement moves, then every independent
original F28 refinement move. The exact natural-number depths remain. -/
def AxisTrace.modificationNormal
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    OrderedInterleaving n m ma pa mb pb := by
  induction hc with
  | refl p =>
      exact AxisTrace.toModificationInterleaving hm p
  | snoc hc step ih =>
      exact OrderedInterleaving.comparison ih step

/-- F19-first normalization preserves every ORIGINAL F19 operation
and its intermediate F40 block presentation in Type. -/
theorem AxisTrace.modificationNormal_modificationTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.modificationNormal hm hc).modificationTrace = hm := by
  induction hc with
  | refl p =>
      exact AxisTrace.toModificationInterleaving_modificationTrace hm p
  | snoc hc step ih =>
      exact ih

/-- F19-first normalization independently preserves every F28
operation and all its original intermediate quotient-category blocks. -/
theorem AxisTrace.modificationNormal_comparisonTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.modificationNormal hm hc).comparisonTrace = hc := by
  induction hc with
  | refl p =>
      exact AxisTrace.toModificationInterleaving_comparisonTrace hm p
  | snoc hc step ih =>
      exact congrArg (fun t => AxisTrace.snoc t step) ih

/-- The two ORIGINAL ordered routes are related by the precise
reflexive/symmetric/transitive closure of F44's primitive F19/F28
ADJACENT swaps. No same-axis interchange is added. -/
theorem AxisTrace.modificationNormal_exchangeEqv_comparisonNormal
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    ExchangeEqv (AxisTrace.modificationNormal hm hc)
      (AxisTrace.comparisonNormal hm hc) := by
  apply (exchangeEqv_iff_axisHistories_eq _ _).2
  exact ⟨(AxisTrace.modificationNormal_modificationTrace hm hc).trans
      (AxisTrace.comparisonNormal_modificationTrace hm hc).symm,
    (AxisTrace.modificationNormal_comparisonTrace hm hc).trans
      (AxisTrace.comparisonNormal_comparisonTrace hm hc).symm⟩

/-- F19-first and F28-first concrete original paths represent the SAME
F44 generated exchange class, with unchanged complete per-axis history. -/
theorem AxisTrace.modificationNormal_class_eq_comparisonNormal
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.modificationNormal hm hc).toClass =
      (AxisTrace.comparisonNormal hm hc).toClass :=
  (exchangeEqv_iff_class_eq _ _).1
    (AxisTrace.modificationNormal_exchangeEqv_comparisonNormal hm hc)

/-- Canonical F19-FIRST realization of any original F44 exchange class
using exactly its F45 proof-relevant F19/F28 histories. -/
def ExchangeClass.modificationNormal
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    OrderedInterleaving n m ma pa mb pb :=
  AxisTrace.modificationNormal c.axisTraces.1 c.axisTraces.2

/-- COMPLETE F47 order-independence: constructing the canonical
F19-first route from ANY genuine F44 exchange class recovers that
SAME class, because the F19-first and F28-first original routes are
related by the F44 generated primitive swaps. -/
theorem ExchangeClass.modificationNormal_toClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    c.modificationNormal.toClass = c := by
  calc
    c.modificationNormal.toClass =
        c.comparisonNormal.toClass :=
      AxisTrace.modificationNormal_class_eq_comparisonNormal
        c.axisTraces.1 c.axisTraces.2
    _ = c := ExchangeClass.comparisonNormal_toClass c

/-- Strongest equality criterion for concrete F19-first and F28-first
normal paths: their complete F19/F28 histories agree, by construction. -/
theorem ExchangeClass.modificationNormal_axisTraces
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    c.modificationNormal.modificationTrace = c.axisTraces.1 ∧
      c.modificationNormal.comparisonTrace = c.axisTraces.2 :=
  ⟨AxisTrace.modificationNormal_modificationTrace _ _,
    AxisTrace.modificationNormal_comparisonTrace _ _⟩

#print axioms AxisTrace.toModificationInterleaving_modificationTrace
#print axioms AxisTrace.toModificationInterleaving_comparisonTrace
#print axioms AxisTrace.modificationNormal
#print axioms AxisTrace.modificationNormal_modificationTrace
#print axioms AxisTrace.modificationNormal_comparisonTrace
#print axioms AxisTrace.modificationNormal_exchangeEqv_comparisonNormal
#print axioms AxisTrace.modificationNormal_class_eq_comparisonNormal
#print axioms ExchangeClass.modificationNormal
#print axioms ExchangeClass.modificationNormal_toClass
#print axioms ExchangeClass.modificationNormal_axisTraces

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
