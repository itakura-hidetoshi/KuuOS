import Kuu.F112.PolygonNativeF45PhysicalExecution

/-!
# F112-E7Q5-F4-O9-A — lossless splitting of complete native AxisTraces

A genuine Type-valued F41 history of depth n+m can be split at
exactly n primitive steps. The intermediate Blocks, the two
original source traces and their literal recomposition equality
are constructed together as a dependent Sigma packet.

Induction proceeds from the rightmost primitive snoc constructor.
No Prop replacement, classical representative choice, scalar grade
or historical KUOS/Gray dependency is used. All original arrows,
their ordered block refinements and the actual witness terms survive.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe u v
variable {C : Type u} [Category.{v} C]

/-- The actual dependent intermediate Blocks, both complete native
Type-valued evidence histories, and their exact unquotiented
recomposition. The witness equality includes every constructor. -/
def KuuNativeAxisTrace.splitAppend
    {x y : C} (n m : Nat)
    {source target : KuuNativeBlocks x y}
    (whole : KuuNativeAxisTrace (n + m) source target) :
    Σ middle : KuuNativeBlocks x y,
      Σ first : KuuNativeAxisTrace n source middle,
        Σ second : KuuNativeAxisTrace m middle target,
          first.append second = whole := by
  induction m generalizing target with
  | zero =>
      exact ⟨target, whole, .refl target, rfl⟩
  | succ m ih =>
      cases whole with
      | snoc preceding step =>
          rcases ih preceding with ⟨middle, first, second, hjoin⟩
          refine ⟨middle, first, .snoc second step, ?_⟩
          exact congrArg (fun t => KuuNativeAxisTrace.snoc t step) hjoin

/-- Erasing only the Sigma wrappers recovers the ORIGINAL entire
history, not just equal primitive counts or category composites. -/
theorem KuuNativeAxisTrace.splitAppend_recompose
    {x y : C} (n m : Nat)
    {source target : KuuNativeBlocks x y}
    (whole : KuuNativeAxisTrace (n + m) source target) :
    ((KuuNativeAxisTrace.splitAppend n m whole).2.1).append
        ((KuuNativeAxisTrace.splitAppend n m whole).2.2.1) = whole :=
  (KuuNativeAxisTrace.splitAppend n m whole).2.2.2

/-- At an empty right-hand depth the chosen intermediate Blocks
are the actual final Blocks and the whole evidence is unchanged. -/
theorem KuuNativeAxisTrace.splitAppend_zero
    {x y : C} (n : Nat)
    {source target : KuuNativeBlocks x y}
    (whole : KuuNativeAxisTrace (n + 0) source target) :
    (KuuNativeAxisTrace.splitAppend n 0 whole).1 = target := rfl

#print axioms KuuNativeAxisTrace.splitAppend
#print axioms KuuNativeAxisTrace.splitAppend_recompose
#print axioms KuuNativeAxisTrace.splitAppend_zero
end
end Kuu.F112.Physical
