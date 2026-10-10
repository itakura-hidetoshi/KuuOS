import KUOS.DependentOriginationCoherentBiadjunctionExchangeNormalFormCompletenessV5_143

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid

set_option autoImplicit false
noncomputable section

/-!
# F46-C / v5.143 — exact and reversible two-axis history classification

F45 constructed a map from the F44 generated exchange quotient
to the pair of Type-valued original F19/F28 histories. F46-B proves
every quotient class has the canonical F28-first representative.

We now prove both inverse laws and provide an actual Lean Equiv.
This is *not* a comparison of endpoint composite Hom values: equality
in the generated path quotient is equivalent to equality of BOTH
complete proof-relevant same-axis histories, and nothing weaker.
In particular no distinct histories on the same axis are identified.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A pair of original Type-valued F19/F28 derivations produces the
canonical genuine F28-first F44 primitive-exchange quotient class. -/
def AxisTrace.pairToClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (histories : AxisTrace n ma mb × AxisTrace m pa pb) :
    ExchangeClass n m ma mb pa pb :=
  (AxisTrace.comparisonNormal histories.1 histories.2).toClass

/-- FIRST inverse law: both original complete histories survive
constructing and extracting the canonical quotient representative. -/
theorem AxisTrace.pairToClass_axisTraces
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (histories : AxisTrace n ma mb × AxisTrace m pa pb) :
    (AxisTrace.pairToClass histories).axisTraces = histories := by
  rcases histories with ⟨hm, hc⟩
  exact Prod.ext
    (AxisTrace.comparisonNormal_modificationTrace hm hc)
    (AxisTrace.comparisonNormal_comparisonTrace hm hc)

/-- SECOND inverse law: the F28-first representative built from
the actual extracted histories equals the ORIGINAL generated
exchange class by the F46-B genuine normalization theorem. -/
theorem ExchangeClass.axisTraces_pairToClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    AxisTrace.pairToClass c.axisTraces = c :=
  ExchangeClass.comparisonNormal_toClass c

/-- Main F46 classification: the quotient by F19/F28 *adjacent
independent-axis* exchanges is exactly equivalent to the product
of their two separately typed and genuinely proof-relevant finite
primitive histories, with unchanged natural-number depths. -/
def ExchangeClass.axisTraceEquiv
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y} :
    ExchangeClass n m ma mb pa pb ≃
      (AxisTrace n ma mb × AxisTrace m pa pb) where
  toFun := ExchangeClass.axisTraces
  invFun := AxisTrace.pairToClass
  left_inv := ExchangeClass.axisTraces_pairToClass
  right_inv := AxisTrace.pairToClass_axisTraces

/-- Complete equality criterion on original genuine F44 classes:
they are equal precisely when BOTH original Type-valued same-axis
histories match, not merely their endpoints or categorical Hom. -/
theorem ExchangeClass.eq_iff_axisTraces_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (p q : ExchangeClass n m ma mb pa pb) :
    p = q ↔ p.axisTraces = q.axisTraces := by
  constructor
  · intro h
    exact congrArg ExchangeClass.axisTraces h
  · intro h
    exact (ExchangeClass.axisTraceEquiv
      (ma := ma) (mb := mb) (pa := pa) (pb := pb)
      (n := n) (m := m)).injective h

/-- F46 is also an EXACT presentation theorem for the **generated**
primitive exchange relation itself. Two original ordered shuffles
are exchange-equivalent iff the two complete independent Type-level
histories agree, with all internal same-axis order retained. -/
theorem exchangeEqv_iff_axisHistories_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (p q : OrderedInterleaving n m ma pa mb pb) :
    ExchangeEqv p q ↔
      p.modificationTrace = q.modificationTrace ∧
        p.comparisonTrace = q.comparisonTrace := by
  rw [exchangeEqv_iff_class_eq p q,
    ExchangeClass.eq_iff_axisTraces_eq p.toClass q.toClass]
  constructor
  · intro h
    exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩
  · rintro ⟨h₁, h₂⟩
    exact Prod.ext h₁ h₂

/-- The canonical normal forms are UNIQUE AS EXCHANGE CLASSES: a
normal representative contains exactly a pair of original histories.
This is not an assertion that arbitrary syntactic OrderedInterleaving
proof trees are definitionally equal. -/
theorem AxisTrace.comparisonNormal_class_injective
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (p q : AxisTrace n ma mb × AxisTrace m pa pb)
    (h : AxisTrace.pairToClass p = AxisTrace.pairToClass q) :
    p = q := by
  have hh := congrArg ExchangeClass.axisTraces h
  simpa only [AxisTrace.pairToClass_axisTraces] using hh

#print axioms AxisTrace.pairToClass
#print axioms AxisTrace.pairToClass_axisTraces
#print axioms ExchangeClass.axisTraces_pairToClass
#print axioms ExchangeClass.axisTraceEquiv
#print axioms ExchangeClass.eq_iff_axisTraces_eq
#print axioms exchangeEqv_iff_axisHistories_eq
#print axioms AxisTrace.comparisonNormal_class_injective

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
