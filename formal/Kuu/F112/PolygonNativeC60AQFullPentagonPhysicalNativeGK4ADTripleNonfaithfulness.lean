import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ADOrderedHistoryInvariant
import Mathlib.Tactic

/-!
F112-P94D3GK4AD — residual nonfaithfulness of the TRUE structural
S -> original P92B-based TRIPLE observation-kernel K_AA comparison.

Take an actual original F54 forward/backward physical backtrack B
from a genuinely witnessed LocalRotation, and an actual original
double-Nat castDepths rfl rfl self-route C. The two ORIGINAL fully
typed F54 self-routes (C;B) and (B;C) retain the same raw endpoints,
Boolean grade=false, signed cast-minus-rotation charge=-1 and exact
backwardCount=1, hence the same genuine triple observation.

The ordered noncommutative original F54 Heisenberg value from the
companion file is (((-1,1),0)) on C;B and (((-1,1),-1)) on B;C.
Because that ordered invariant is separately descended through ALL
actual original P92B cells and structural seams to S, the two genuine
independent structural quotient classes are PROVABLY DISTINCT.
Yet the true GK4AA S->K_AA comparison identifies them. This
settles the previously open global faithfulness question NEGATIVELY
at every witnessed native F54 local rotation, including physical
C60 north. The result does NOT identify Q, S and K_AA or derive
an original Type-valued P92B 3-cell from numeric equality.

No original P92B Q category axioms, no historical complete typed
equivalence, old 14D unconditional Countable, 19D filler, global
strict n or hyperdescent. Strict 空 central, independent Kuu one
presentation, Gray excluded; append-only, same-root 107.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected #1558 Draft/open/unmerged.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section OriginalTypedPhysicalWitnesses
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- TWO genuinely distinct original F54 proof histories: cast
BEFORE the full original forward/backward physical backtrack. -/
def nativeGK4ADCastBeforeBacktrack :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4WCastRoute before) (nativeGK4FBacktrack rot)

/-- The same actual cast and actual physical backtrack in the other
order. No freely created 3-cell is assumed between these histories. -/
def nativeGK4ADCastAfterBacktrack :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4FBacktrack rot) (nativeGK4WCastRoute before)

/-- Their FULL original-triple (Boolean,charge,backwardCount) is
identical on ACTUAL structural quotient representatives. -/
theorem nativeGK4ADTwoOrders_sameTriple :
    nativeGK4AATripleStructural before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ADCastBeforeBacktrack rot)) =
    nativeGK4AATripleStructural before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ADCastAfterBacktrack rot)) := by
  rfl

/-- Genuine cast preceding backtrack has moment zero: the cast
neutralizes the immediate forward step before the backward step. -/
theorem nativeGK4ADCastBefore_value :
    (nativeGK4ADCastBeforeBacktrack rot).gk4adValue =
      (((-1 : Int), (1 : Nat)), (0 : Int)) := by
  rfl

/-- Cast AFTER the same real backtrack leaves a residual -1
noncommutative moment. This is a Type-valued history invariant. -/
theorem nativeGK4ADCastAfter_value :
    (nativeGK4ADCastAfterBacktrack rot).gk4adValue =
      (((-1 : Int), (1 : Nat)), (-1 : Int)) := by
  rfl

/-- The two raw histories are separated already in the original
P92B quotient Q, via its independently descended ordered invariant.
This does not assert original P92B associativity/unit laws. -/
theorem nativeGK4ADOriginalP92Orders_ne :
    nativeF55P92AssocRouteClass before before
        (nativeGK4ADCastBeforeBacktrack rot) ≠
      nativeF55P92AssocRouteClass before before
        (nativeGK4ADCastAfterBacktrack rot) := by
  intro heq
  have hv := congrArg (nativeGK4ADP92Value before before) heq
  change
    (((-1 : Int), (1 : Nat)), (0 : Int)) =
      (((-1 : Int), (1 : Nat)), (-1 : Int)) at hv
  have hmoment := congrArg Prod.snd hv
  omega

/-- Crucial theorem: the separately stronger TRUE structural quotient
S does NOT identify the two original Type-valued histories, even
after adding all fourteen original F54 structural seams. -/
theorem nativeGK4ADStructuralOrders_ne :
    nativeGK4EStructuralRouteClass before before
        (nativeGK4ADCastBeforeBacktrack rot) ≠
      nativeGK4EStructuralRouteClass before before
        (nativeGK4ADCastAfterBacktrack rot) := by
  intro heq
  have hv := congrArg (nativeGK4ADStructuralValue before before) heq
  change
    (((-1 : Int), (1 : Nat)), (0 : Int)) =
      (((-1 : Int), (1 : Nat)), (-1 : Int)) at hv
  have hmoment := congrArg Prod.snd hv
  omega

/-- The true second P92B triple observation-kernel K_AA nevertheless
IDENTIFIES those two different independent structural S classes. -/
theorem nativeGK4ADTwoOrders_sameKernel :
    nativeGK4AATripleComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ADCastBeforeBacktrack rot)) =
    nativeGK4AATripleComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ADCastAfterBacktrack rot)) := by
  apply (nativeGK4AATripleComparison_eq_iff before before _ _).mpr
  exact nativeGK4ADTwoOrders_sameTriple rot

/-- MAIN RESIDUAL OBSTRUCTION: any actually witnessed physical F54
LocalRotation implies S->K_AA is NOT injective on that original
fully dependent F45 self-Hom. The three numerical components are
not a faithful complete invariant of the original structural S. -/
theorem nativeGK4ADTripleComparison_not_injective
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    ¬ Function.Injective
      (nativeGK4AATripleComparison before before) := by
  intro hinj
  exact nativeGK4ADStructuralOrders_ne rot
    (hinj (nativeGK4ADTwoOrders_sameKernel rot))

end OriginalTypedPhysicalWitnesses

section RealC60North

/-- The genuine physical C60 north local rotation witnesses the
new nonfaithfulness of the REAL structural->triple-kernel functor.
This is different from GK4AC's COMPLETE K_AA->K_X fiber theorem. -/
theorem nativeGK4AD_physical_north_triple_nonfaithful :
    ¬ Function.Injective
      (nativeGK4AATripleComparison
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact nativeGK4ADTripleComparison_not_injective
    northHexagonNativeLeftRotation

end RealC60North

#print axioms nativeGK4ADCastBeforeBacktrack
#print axioms nativeGK4ADCastAfterBacktrack
#print axioms nativeGK4ADTwoOrders_sameTriple
#print axioms nativeGK4ADCastBefore_value
#print axioms nativeGK4ADCastAfter_value
#print axioms nativeGK4ADOriginalP92Orders_ne
#print axioms nativeGK4ADStructuralOrders_ne
#print axioms nativeGK4ADTwoOrders_sameKernel
#print axioms nativeGK4ADTripleComparison_not_injective
#print axioms nativeGK4AD_physical_north_triple_nonfaithful

end
end Kuu.F112.Physical
