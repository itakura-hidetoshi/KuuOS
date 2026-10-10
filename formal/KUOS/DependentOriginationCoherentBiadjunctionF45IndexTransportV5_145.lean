import KUOS.DependentOriginationCoherentBiadjunctionF45OrderCompatibilityV5_144

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F48-A / v5.145 — explicit Nat.zero_add transport on original F45 paths

The original F45 functions AxisTrace.modificationFirst/comparisonFirst
are actual genuine finite F19/F28 ordered paths, defined via F44
append and simplification of independent exact natural-number depths.

F47 proved canonical native F19-first/F28-first paths but deliberately
did not identify them with the older F45 implementations: the latter
elaborate to dependent Eq.mp casts along Nat.zero_add.

We isolate the two **specific** index transports, prove that they
preserve the unaffected Type-valued original F19/F28 history on the
nose, and relate them to the exact F45 implementation. No generic
higher interchange, same-axis permutation or strictness is assumed.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Reindex ONLY the genuine F28 primitive count along an equality
of finite depths; the F19 count, original categories, Blocks, and
intermediate primitive moves remain unchanged. -/
def OrderedInterleaving.castComparisonDepth
    {a b : D} {x y : E} {n m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (depthEq : m = m')
    (route : OrderedInterleaving n m ma pa mb pb) :
    OrderedInterleaving n m' ma pa mb pb := by
  cases depthEq
  exact route

/-- Reindex ONLY the genuine F19 primitive count. F28's independent
actual quotient-category refinement history remains unmodified. -/
def OrderedInterleaving.castModificationDepth
    {a b : D} {x y : E} {n n' m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (depthEq : n = n')
    (route : OrderedInterleaving n m ma pa mb pb) :
    OrderedInterleaving n' m ma pa mb pb := by
  cases depthEq
  exact route

/-- The comparison-depth Eq.mp index transport keeps the complete
proof-relevant F19 modification trace unchanged, not just a Prop
existence witness or its categorical composite. -/
theorem OrderedInterleaving.castComparisonDepth_modificationTrace
    {a b : D} {x y : E} {n m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (depthEq : m = m') (route : OrderedInterleaving n m ma pa mb pb) :
    (OrderedInterleaving.castComparisonDepth depthEq route).modificationTrace =
      route.modificationTrace := by
  cases depthEq
  rfl

/-- The modification-depth Eq.mp index transport keeps the complete
proof-relevant original F28 comparison trace unchanged. -/
theorem OrderedInterleaving.castModificationDepth_comparisonTrace
    {a b : D} {x y : E} {n n' m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (depthEq : n = n') (route : OrderedInterleaving n m ma pa mb pb) :
    (OrderedInterleaving.castModificationDepth depthEq route).comparisonTrace =
      route.comparisonTrace := by
  cases depthEq
  rfl

/-- Type-valued depth transports commute with the native F44 exchange
quotient projection; the transported path is still a genuine quotient
representative at its exact new natural-number depth. -/
theorem OrderedInterleaving.castComparisonDepth_toClass
    {a b : D} {x y : E} {n m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (depthEq : m = m') (route : OrderedInterleaving n m ma pa mb pb) :
    (OrderedInterleaving.castComparisonDepth depthEq route).toClass =
      depthEq ▸ route.toClass := by
  cases depthEq
  rfl

/-- The other independent axis similarly descends to the genuine
F44 generated quotient under a natural-number index transport. -/
theorem OrderedInterleaving.castModificationDepth_toClass
    {a b : D} {x y : E} {n n' m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (depthEq : n = n') (route : OrderedInterleaving n m ma pa mb pb) :
    (OrderedInterleaving.castModificationDepth depthEq route).toClass =
      depthEq ▸ route.toClass := by
  cases depthEq
  rfl

/-- The ORIGINAL F45 F19-first path is the F44 ordered append with
its exact F28 Nat.zero_add index transport made explicit. This is
an equality of actual Type-valued proof-relevant ordered paths. -/
theorem AxisTrace.modificationFirst_eq_castComparisonDepth
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    AxisTrace.modificationFirst hm hc =
      OrderedInterleaving.castComparisonDepth (Nat.zero_add m)
        (OrderedInterleaving.append
          (AxisTrace.toModificationInterleaving hm pa)
          (AxisTrace.toComparisonInterleaving mb hc)) := by
  rfl

/-- The ORIGINAL F45 F28-first path is the F44 ordered append with
its exact F19 Nat.zero_add index transport made explicit. -/
theorem AxisTrace.comparisonFirst_eq_castModificationDepth
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hm : AxisTrace n ma mb) (hc : AxisTrace m pa pb) :
    AxisTrace.comparisonFirst hm hc =
      OrderedInterleaving.castModificationDepth (Nat.zero_add n)
        (OrderedInterleaving.append
          (AxisTrace.toComparisonInterleaving ma hc)
          (AxisTrace.toModificationInterleaving hm pb)) := by
  rfl

#print axioms OrderedInterleaving.castComparisonDepth
#print axioms OrderedInterleaving.castModificationDepth
#print axioms OrderedInterleaving.castComparisonDepth_modificationTrace
#print axioms OrderedInterleaving.castModificationDepth_comparisonTrace
#print axioms OrderedInterleaving.castComparisonDepth_toClass
#print axioms OrderedInterleaving.castModificationDepth_toClass
#print axioms AxisTrace.modificationFirst_eq_castComparisonDepth
#print axioms AxisTrace.comparisonFirst_eq_castModificationDepth

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
