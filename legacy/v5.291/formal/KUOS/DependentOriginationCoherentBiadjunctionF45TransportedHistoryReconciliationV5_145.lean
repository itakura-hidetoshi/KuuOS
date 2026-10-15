import KUOS.DependentOriginationCoherentBiadjunctionF45IndexTransportV5_145

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F48-B / v5.145 — full original F45 history recovery through Eq.mp

F48-A identifies the actual original F45 proof-relevant ordered paths
with the F44 path concatenations reindexed by precisely Nat.zero_add
on the independent axis. Here dependent transport is performed
at the Type-valued AxisTrace level, without erasing original
intermediate F19/F28 Blocks or treating their Hom types as equal.

The finite left-identity result explicitly transports
  AxisTrace (0+n) p q  →  AxisTrace n p q
instead of incorrectly assuming 0+n is definitional equality.
All four actual old F45 history projections are proved, closing the
distinction between original F45 routes and F47 native normal forms
*in the genuine F44 generated exchange quotient*.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Native proof-relevant F19 or F28 exact-depth reindexing using a
single equality of dependent Type families, not Prop proof erasure. -/
def AxisTrace.castDepth
    {a b : D} {n n' : Nat} {pa pb : Blocks a b}
    (depthEq : n = n') (t : AxisTrace n pa pb) :
    AxisTrace n' pa pb :=
  cast (congrArg (fun k => AxisTrace k pa pb) depthEq) t

/-- Transport respects the actual F42 primitive snoc constructor,
including its intermediate block presentation. -/
theorem AxisTrace.castDepth_snoc
    {a b : D} {n n' : Nat} {pa pb pc : Blocks a b}
    (depthEq : n = n') (t : AxisTrace n pa pb)
    (step : OneStep pb pc) :
    AxisTrace.castDepth (congrArg Nat.succ depthEq) (AxisTrace.snoc t step) =
      AxisTrace.snoc (AxisTrace.castDepth depthEq t) step := by
  cases depthEq
  rfl

/-- Casts in the original F45 modification-first construction leave
its complete genuine F28 axis history transported along Nat.zero_add. -/
theorem OrderedInterleaving.castComparisonDepth_comparisonTrace
    {a b : D} {x y : E} {n m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (depthEq : m = m') (route : OrderedInterleaving n m ma pa mb pb) :
    (OrderedInterleaving.castComparisonDepth depthEq route).comparisonTrace =
      AxisTrace.castDepth depthEq route.comparisonTrace := by
  cases depthEq
  rfl

/-- Casts in original F45 comparison-first construction retain the
complete genuine F19 history transported along its own Nat.zero_add. -/
theorem OrderedInterleaving.castModificationDepth_modificationTrace
    {a b : D} {x y : E} {n n' m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (depthEq : n = n') (route : OrderedInterleaving n m ma pa mb pb) :
    (OrderedInterleaving.castModificationDepth depthEq route).modificationTrace =
      AxisTrace.castDepth depthEq route.modificationTrace := by
  cases depthEq
  rfl

/-- The left identity for native F19/F28 Type-valued primitive traces
is an ACTUAL dependent transport, not a false definitional reduction
of Nat.zero_add for an arbitrary natural number n. -/
theorem AxisTrace.append_refl_left_cast
    {a b : D} {n : Nat} {pa pb : Blocks a b}
    (t : AxisTrace n pa pb) :
    AxisTrace.castDepth (Nat.zero_add n)
      (AxisTrace.append (AxisTrace.refl pa) t) = t := by
  induction t with
  | refl p =>
      rfl
  | snoc t step ih =>
      calc
        _ = AxisTrace.snoc
              (AxisTrace.castDepth (Nat.zero_add _)
                (AxisTrace.append (AxisTrace.refl _) t)) step := by
          exact AxisTrace.castDepth_snoc (Nat.zero_add _) _ step
        _ = AxisTrace.snoc t step :=
          congrArg (fun h => AxisTrace.snoc h step) ih

/-- ORIGINAL F45 F19-FIRST path: exact F19 Type-valued history,
including every genuine intermediate F40 block and OneStep. -/
theorem AxisTrace.modificationFirst_originalModificationTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.modificationFirst hm hc).modificationTrace = hm := by
  rw [AxisTrace.modificationFirst_eq_castComparisonDepth,
    OrderedInterleaving.castComparisonDepth_modificationTrace,
    OrderedInterleaving.modificationTrace_append,
    AxisTrace.toModificationInterleaving_modificationTrace,
    AxisTrace.toComparisonInterleaving_modificationTrace,
    AxisTrace.append_refl_right]

/-- ORIGINAL F45 F19-FIRST path: the independent F28 history is
retained exactly by the Nat.zero_add transported left identity. -/
theorem AxisTrace.modificationFirst_originalComparisonTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.modificationFirst hm hc).comparisonTrace = hc := by
  rw [AxisTrace.modificationFirst_eq_castComparisonDepth,
    OrderedInterleaving.castComparisonDepth_comparisonTrace,
    OrderedInterleaving.comparisonTrace_append,
    AxisTrace.toModificationInterleaving_comparisonTrace,
    AxisTrace.toComparisonInterleaving_comparisonTrace,
    AxisTrace.append_refl_left_cast]

/-- ORIGINAL F45 F28-FIRST path: F19's Type-level history is
retained exactly by the transported left-identity theorem. -/
theorem AxisTrace.comparisonFirst_originalModificationTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.comparisonFirst hm hc).modificationTrace = hm := by
  rw [AxisTrace.comparisonFirst_eq_castModificationDepth,
    OrderedInterleaving.castModificationDepth_modificationTrace,
    OrderedInterleaving.modificationTrace_append,
    AxisTrace.toComparisonInterleaving_modificationTrace,
    AxisTrace.toModificationInterleaving_modificationTrace,
    AxisTrace.append_refl_left_cast]

/-- ORIGINAL F45 F28-FIRST path: the native F28 Type-valued history
is unaffected by the independent F19 index transport. -/
theorem AxisTrace.comparisonFirst_originalComparisonTrace
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.comparisonFirst hm hc).comparisonTrace = hc := by
  rw [AxisTrace.comparisonFirst_eq_castModificationDepth,
    OrderedInterleaving.castModificationDepth_comparisonTrace,
    OrderedInterleaving.comparisonTrace_append,
    AxisTrace.toComparisonInterleaving_comparisonTrace,
    AxisTrace.toModificationInterleaving_comparisonTrace,
    AxisTrace.append_refl_right]

/-- Full F48 exact original F45 history statement in BOTH axes,
not merely F42 Prop reachability or equality of endpoint arrows. -/
theorem AxisTrace.originalF45Orders_preserve_histories
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    ((AxisTrace.modificationFirst hm hc).modificationTrace = hm ∧
      (AxisTrace.modificationFirst hm hc).comparisonTrace = hc) ∧
    ((AxisTrace.comparisonFirst hm hc).modificationTrace = hm ∧
      (AxisTrace.comparisonFirst hm hc).comparisonTrace = hc) :=
  ⟨⟨AxisTrace.modificationFirst_originalModificationTrace hm hc,
     AxisTrace.modificationFirst_originalComparisonTrace hm hc⟩,
   ⟨AxisTrace.comparisonFirst_originalModificationTrace hm hc,
     AxisTrace.comparisonFirst_originalComparisonTrace hm hc⟩⟩

/-- Both ORIGINAL F45 Type-valued routes represent the SAME generated
F44 exchange class, certified by its COMPLETE F46 exchange relation
rather than by equality of evaluated categorical Hom composites. -/
theorem AxisTrace.originalF45Orders_exchangeEqv
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    ExchangeEqv (AxisTrace.modificationFirst hm hc)
      (AxisTrace.comparisonFirst hm hc) := by
  apply (exchangeEqv_iff_axisHistories_eq _ _).2
  exact ⟨(AxisTrace.modificationFirst_originalModificationTrace hm hc).trans
      (AxisTrace.comparisonFirst_originalModificationTrace hm hc).symm,
    (AxisTrace.modificationFirst_originalComparisonTrace hm hc).trans
      (AxisTrace.comparisonFirst_originalComparisonTrace hm hc).symm⟩

/-- ORIGINAL F45 F19-FIRST path now coincides in the exact generated
exchange quotient with F47's independently constructed F19 normal path. -/
theorem AxisTrace.originalF45_modificationFirst_eq_normalClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.modificationFirst hm hc).toClass =
      (AxisTrace.modificationNormal hm hc).toClass := by
  apply (exchangeEqv_iff_class_eq _ _).1
  apply (exchangeEqv_iff_axisHistories_eq _ _).2
  exact ⟨(AxisTrace.modificationFirst_originalModificationTrace hm hc).trans
      (AxisTrace.modificationNormal_modificationTrace hm hc).symm,
    (AxisTrace.modificationFirst_originalComparisonTrace hm hc).trans
      (AxisTrace.modificationNormal_comparisonTrace hm hc).symm⟩

/-- ORIGINAL F45 F28-FIRST path now coincides with F46's F28 normal
path in the SAME genuine F44 generated adjacent-exchange quotient. -/
theorem AxisTrace.originalF45_comparisonFirst_eq_normalClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.comparisonFirst hm hc).toClass =
      (AxisTrace.comparisonNormal hm hc).toClass := by
  apply (exchangeEqv_iff_class_eq _ _).1
  apply (exchangeEqv_iff_axisHistories_eq _ _).2
  exact ⟨(AxisTrace.comparisonFirst_originalModificationTrace hm hc).trans
      (AxisTrace.comparisonNormal_modificationTrace hm hc).symm,
    (AxisTrace.comparisonFirst_originalComparisonTrace hm hc).trans
      (AxisTrace.comparisonNormal_comparisonTrace hm hc).symm⟩

/-- The original two F45 constructions have the exact same quotient
class, with every F19/F28 same-axis operation history retained. -/
theorem AxisTrace.originalF45Orders_class_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    (AxisTrace.modificationFirst hm hc).toClass =
      (AxisTrace.comparisonFirst hm hc).toClass :=
  (exchangeEqv_iff_class_eq _ _).1
    (AxisTrace.originalF45Orders_exchangeEqv hm hc)

#print axioms AxisTrace.castDepth
#print axioms AxisTrace.castDepth_snoc
#print axioms OrderedInterleaving.castComparisonDepth_comparisonTrace
#print axioms OrderedInterleaving.castModificationDepth_modificationTrace
#print axioms AxisTrace.append_refl_left_cast
#print axioms AxisTrace.modificationFirst_originalModificationTrace
#print axioms AxisTrace.modificationFirst_originalComparisonTrace
#print axioms AxisTrace.comparisonFirst_originalModificationTrace
#print axioms AxisTrace.comparisonFirst_originalComparisonTrace
#print axioms AxisTrace.originalF45Orders_preserve_histories
#print axioms AxisTrace.originalF45Orders_exchangeEqv
#print axioms AxisTrace.originalF45_modificationFirst_eq_normalClass
#print axioms AxisTrace.originalF45_comparisonFirst_eq_normalClass
#print axioms AxisTrace.originalF45Orders_class_eq

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
