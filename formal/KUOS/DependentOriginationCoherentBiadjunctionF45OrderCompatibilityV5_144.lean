import KUOS.DependentOriginationCoherentBiadjunctionModificationNormalFormV5_144

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F47-B / v5.144 — F45's two actual finite execution orders are coherent

F45 constructed both \`AxisTrace.modificationFirst\` and
\`AxisTrace.comparisonFirst\` as full F44 ordered Type-valued paths.
F46 produced a canonical F28-first quotient representative and F47-A
produced an independently defined F19-first representative.

This file checks that the ORIGINAL two F45 concrete execution routes
contain exactly the two input Type-level histories, even when F45
uses full finite path concatenation. We prove projection/concatenation
compatibility and use F46's *complete generated-exchange criterion*
to identify those precise F45 paths with the F47 normal forms.
No arbitrary same-axis operation is ever commuted.
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

/-- A genuine zero-step prefix does not alter the appended native
same-axis refinement history, at the full Type-level. -/
theorem AxisTrace.append_refl_left
    {a b : D} {n : Nat} {ma mb : Blocks a b}
    (hm : AxisTrace n ma mb) :
    AxisTrace.append (AxisTrace.refl ma) hm = hm := by
  induction hm with
  | refl p => rfl
  | snoc hm step ih =>
      exact congrArg (fun t => AxisTrace.snoc t step) ih

/-- A genuine zero-step suffix likewise leaves the original
same-axis intermediate block history exactly unchanged. -/
theorem AxisTrace.append_refl_right
    {a b : D} {n : Nat} {ma mb : Blocks a b}
    (hm : AxisTrace n ma mb) :
    AxisTrace.append hm (AxisTrace.refl mb) = hm :=
  rfl

/-- F45's ORIGINAL F19-FIRST full ordered construction retains every
individual F19 step and typed intermediate refinement presentation. -/
theorem AxisTrace.modificationFirst_modificationTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.modificationFirst hm hc).modificationTrace = hm := by
  change (OrderedInterleaving.append
      (AxisTrace.toModificationInterleaving hm pa)
      (AxisTrace.toComparisonInterleaving mb hc)).modificationTrace = hm
  rw [OrderedInterleaving.modificationTrace_append,
    AxisTrace.toModificationInterleaving_modificationTrace,
    AxisTrace.toComparisonInterleaving_modificationTrace,
    AxisTrace.append_refl_right]

/-- F45's original F19-first ordered route also preserves all
independent F28 quotient-category primitive history in Type. -/
theorem AxisTrace.modificationFirst_comparisonTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.modificationFirst hm hc).comparisonTrace = hc := by
  change (OrderedInterleaving.append
      (AxisTrace.toModificationInterleaving hm pa)
      (AxisTrace.toComparisonInterleaving mb hc)).comparisonTrace = hc
  rw [OrderedInterleaving.comparisonTrace_append,
    AxisTrace.toModificationInterleaving_comparisonTrace,
    AxisTrace.toComparisonInterleaving_comparisonTrace,
    AxisTrace.append_refl_left]

/-- F45's ORIGINAL F28-first full ordered construction preserves
the entire native F19 Type-level step history without permutation. -/
theorem AxisTrace.comparisonFirst_modificationTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.comparisonFirst hm hc).modificationTrace = hm := by
  change (OrderedInterleaving.append
      (AxisTrace.toComparisonInterleaving ma hc)
      (AxisTrace.toModificationInterleaving hm pb)).modificationTrace = hm
  rw [OrderedInterleaving.modificationTrace_append,
    AxisTrace.toComparisonInterleaving_modificationTrace,
    AxisTrace.toModificationInterleaving_modificationTrace,
    AxisTrace.append_refl_left]

/-- F45's original F28-first route likewise preserves its genuine
separate F28 Type-level quotient primitive history. -/
theorem AxisTrace.comparisonFirst_comparisonTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.comparisonFirst hm hc).comparisonTrace = hc := by
  change (OrderedInterleaving.append
      (AxisTrace.toComparisonInterleaving ma hc)
      (AxisTrace.toModificationInterleaving hm pb)).comparisonTrace = hc
  rw [OrderedInterleaving.comparisonTrace_append,
    AxisTrace.toComparisonInterleaving_comparisonTrace,
    AxisTrace.toModificationInterleaving_comparisonTrace,
    AxisTrace.append_refl_right]

/-- The two ACTUAL original F45 finite concatenation paths are related
by F44's generated primitive exchanges, not only by a Hom equality. -/
theorem AxisTrace.modificationFirst_exchangeEqv_comparisonFirst
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    ExchangeEqv (AxisTrace.modificationFirst hm hc)
      (AxisTrace.comparisonFirst hm hc) := by
  apply (exchangeEqv_iff_axisHistories_eq _ _).2
  exact ⟨(AxisTrace.modificationFirst_modificationTrace hm hc).trans
        (AxisTrace.comparisonFirst_modificationTrace hm hc).symm,
      (AxisTrace.modificationFirst_comparisonTrace hm hc).trans
        (AxisTrace.comparisonFirst_comparisonTrace hm hc).symm⟩

/-- The originally constructed F45 F19-first and F28-first ordered
routes represent the very SAME original F44 generated exchange class. -/
theorem AxisTrace.modificationFirst_class_eq_comparisonFirst
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.modificationFirst hm hc).toClass =
      (AxisTrace.comparisonFirst hm hc).toClass :=
  (exchangeEqv_iff_class_eq _ _).1
    (AxisTrace.modificationFirst_exchangeEqv_comparisonFirst hm hc)

/-- F45's F19-first actual route and F47-A's independently constructed
F19-first normal route coincide in the generated F44 quotient. -/
theorem AxisTrace.modificationFirst_class_eq_modificationNormal
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.modificationFirst hm hc).toClass =
      (AxisTrace.modificationNormal hm hc).toClass := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  exact Prod.ext
    ((AxisTrace.modificationFirst_modificationTrace hm hc).trans
      (AxisTrace.modificationNormal_modificationTrace hm hc).symm)
    ((AxisTrace.modificationFirst_comparisonTrace hm hc).trans
      (AxisTrace.modificationNormal_comparisonTrace hm hc).symm)

/-- F45's F28-first actual route and F46's canonical F28-first normal
path likewise coincide as full generated exchange classes. -/
theorem AxisTrace.comparisonFirst_class_eq_comparisonNormal
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.comparisonFirst hm hc).toClass =
      (AxisTrace.comparisonNormal hm hc).toClass := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  exact Prod.ext
    ((AxisTrace.comparisonFirst_modificationTrace hm hc).trans
      (AxisTrace.comparisonNormal_modificationTrace hm hc).symm)
    ((AxisTrace.comparisonFirst_comparisonTrace hm hc).trans
      (AxisTrace.comparisonNormal_comparisonTrace hm hc).symm)

#print axioms AxisTrace.append
#print axioms OrderedInterleaving.modificationTrace_append
#print axioms OrderedInterleaving.comparisonTrace_append
#print axioms AxisTrace.append_refl_left
#print axioms AxisTrace.append_refl_right
#print axioms AxisTrace.modificationFirst_modificationTrace
#print axioms AxisTrace.modificationFirst_comparisonTrace
#print axioms AxisTrace.comparisonFirst_modificationTrace
#print axioms AxisTrace.comparisonFirst_comparisonTrace
#print axioms AxisTrace.modificationFirst_exchangeEqv_comparisonFirst
#print axioms AxisTrace.modificationFirst_class_eq_comparisonFirst
#print axioms AxisTrace.modificationFirst_class_eq_modificationNormal
#print axioms AxisTrace.comparisonFirst_class_eq_comparisonNormal

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
