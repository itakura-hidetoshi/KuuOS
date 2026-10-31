import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AFMatrixInvariant
import Mathlib.Tactic

/-!
F112-P94D3GK4AF — proven residual NONFAITHFULNESS of the actual
independent structural S -> FOUR-component K_AE quotient comparison.

The genuine physical F54 self-loop B has original forward and backward
RotationEdge witnesses. C is the original double-Nat castDepths rfl rfl
self-route. The original fully dependent F54 words
  u = C ; B ; B ; C
  v = B ; C ; C ; B
have the SAME actual four-component observer
 (Boolean grade=false, castCharge=-2, backwardCount=2,
  orderedMoment=-2).
Thus K_AE identifies their genuine original S images.

But the separately descended true 2-by-2 integer-matrix evaluator
assigns distinct matrices to u and v. Since this fifth original
history invariant is preserved by all actual original F55/P92B cells
and independent 14 structural seams, [u]_S != [v]_S, with
no extra 3-cell or injected quotient equality.

This refutes local S -> K_AE faithfulness on any witnessed genuinely
typed F54 LocalRotation, including the real C60 north physical witness.
It does NOT refute GK4AC's different K_AA -> K_X exact Nat fiber,
nor imply source Q is a category or a historical typed equivalence.
Strict 空 central, independent Kuu one presentation; append-only,
tighten-only, same-root root 107, no Gray; protect #1558.
Lean pinned v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

section OriginalTypedMatrixWitness
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- The original actual two-Nat cast BEFORE two full physically
witnessed forward/backward F54 backtracks, and then cast AGAIN. -/
def nativeGK4AFWordCBBC :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4WCastRoute before)
    (.trans (nativeGK4FBacktrack rot)
      (.trans (nativeGK4FBacktrack rot)
        (nativeGK4WCastRoute before)))

/-- The same actual two backtracks but now casts lie between them.
Each original F54 proof constructor and dependent endpoint is retained. -/
def nativeGK4AFWordBCCB :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4FBacktrack rot)
    (.trans (nativeGK4WCastRoute before)
      (.trans (nativeGK4WCastRoute before)
        (nativeGK4FBacktrack rot)))

/-- The FULL original four-coordinate observation agrees exactly,
not only a Boolean grade or a synthetic numerical shadow. -/
theorem nativeGK4AFWord_sameFour :
    nativeGK4AEQuadStructural before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AFWordCBBC rot)) =
    nativeGK4AEQuadStructural before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AFWordBCCB rot)) := by
  rfl

theorem nativeGK4AFWordCBBC_quad :
    (nativeGK4AEQuadStructural before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AFWordCBBC rot))) =
      (false, (((-2 : Int), (2 : Nat)), (-2 : Int))) := by
  rfl

theorem nativeGK4AFWordBCCB_quad :
    (nativeGK4AEQuadStructural before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AFWordBCCB rot))) =
      (false, (((-2 : Int), (2 : Nat)), (-2 : Int))) := by
  rfl

/-- True higher-order matrix evaluation distinguishes the words:
C*B*B*C = [[0,-1],[1,1]]. -/
theorem nativeGK4AFWordCBBC_matrix :
    (nativeGK4AFWordCBBC rot).gk4afMatrix =
      (((0 : Int), (-1 : Int)), ((1 : Int), (1 : Int))) := by
  rfl

/-- B*C*C*B = [[-1,-1],[3,2]] differs in two actual matrix entries. -/
theorem nativeGK4AFWordBCCB_matrix :
    (nativeGK4AFWordBCCB rot).gk4afMatrix =
      (((-1 : Int), (-1 : Int)), ((3 : Int), (2 : Int))) := by
  rfl

/-- Even ORIGINAL P92B witness-existence Q does not identify the two
fully typed F54 terms. It is not necessary to assert Q category laws. -/
theorem nativeGK4AFP92Classes_ne :
    nativeF55P92AssocRouteClass before before
        (nativeGK4AFWordCBBC rot) ≠
      nativeF55P92AssocRouteClass before before
        (nativeGK4AFWordBCCB rot) := by
  intro heq
  have hv := congrArg (nativeGK4AFP92Value before before) heq
  change (nativeGK4AFWordCBBC rot).gk4afMatrix =
    (nativeGK4AFWordBCCB rot).gk4afMatrix at hv
  rw [nativeGK4AFWordCBBC_matrix, nativeGK4AFWordBCCB_matrix] at hv
  have hentry := congrArg (fun m : NativeGK4AFMatrix => m.1.1) hv
  change (0 : Int) = (-1 : Int) at hentry
  omega

/-- In the independently larger structural proof-existence quotient
S the different integer-matrix evaluations STILL certify distinct
classes after all original 14 F54 seams have been adjoined. -/
theorem nativeGK4AFStructuralClasses_ne :
    nativeGK4EStructuralRouteClass before before
        (nativeGK4AFWordCBBC rot) ≠
      nativeGK4EStructuralRouteClass before before
        (nativeGK4AFWordBCCB rot) := by
  intro heq
  have hv := congrArg (nativeGK4AFStructuralValue before before) heq
  change (nativeGK4AFWordCBBC rot).gk4afMatrix =
    (nativeGK4AFWordBCCB rot).gk4afMatrix at hv
  rw [nativeGK4AFWordCBBC_matrix, nativeGK4AFWordBCCB_matrix] at hv
  have hentry := congrArg (fun m : NativeGK4AFMatrix => m.1.1) hv
  change (0 : Int) = (-1 : Int) at hentry
  omega

/-- The genuine P92B second observational K_AE DOES identify them,
because the four-component source observations coincide. -/
theorem nativeGK4AFFourKernel_equal :
    nativeGK4AEComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AFWordCBBC rot)) =
    nativeGK4AEComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AFWordBCCB rot)) := by
  exact (nativeGK4AEComparison_eq_iff before before _ _).mpr
    (nativeGK4AFWord_sameFour rot)

/-- Main exact-source residual obstruction:
S -> K_AE is NOT INJECTIVE on the SELF-HOM of every genuine
native F54 local rotation, despite new ordered moment. -/
theorem nativeGK4AFComparison_not_injective
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    ¬ Function.Injective (nativeGK4AEComparison before before) := by
  intro hinj
  exact nativeGK4AFStructuralClasses_ne rot
    (hinj (nativeGK4AFFourKernel_equal rot))

end OriginalTypedMatrixWitness

section ActualC60North

/-- At the TRUE north C60 physical hexagon F45 witness,
the four-component S -> K_AE observer comparison is nonfaithful. -/
theorem nativeGK4AFPhysicalNorth_four_nonfaithful :
    ¬ Function.Injective
      (nativeGK4AEComparison
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact nativeGK4AFComparison_not_injective northHexagonNativeLeftRotation

end ActualC60North

#print axioms nativeGK4AFWordCBBC
#print axioms nativeGK4AFWordBCCB
#print axioms nativeGK4AFWord_sameFour
#print axioms nativeGK4AFWordCBBC_quad
#print axioms nativeGK4AFWordBCCB_quad
#print axioms nativeGK4AFWordCBBC_matrix
#print axioms nativeGK4AFWordBCCB_matrix
#print axioms nativeGK4AFP92Classes_ne
#print axioms nativeGK4AFStructuralClasses_ne
#print axioms nativeGK4AFFourKernel_equal
#print axioms nativeGK4AFComparison_not_injective
#print axioms nativeGK4AFPhysicalNorth_four_nonfaithful

end
end Kuu.F112.Physical
