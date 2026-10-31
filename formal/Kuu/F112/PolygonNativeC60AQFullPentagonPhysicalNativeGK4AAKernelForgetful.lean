import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AAKernelCategory
import Mathlib.Tactic

/-!
F112-P94D3GK4AA — the GENUINE second quotient functor
  K_AA (Bool × Int × Nat) -> K_X (Bool × Int)
induced by forgetting actual backward physical rotations.

This is a true Mathlib functor between SEPARATE second quotients of
original P92B proof-existence classes. It is surjective on each Hom.
Every genuine GK4Z balanced original F54 route has a different
K_AA image but maps to the SAME K_X image. For every witnessed
Type-valued local rotation, the true fixed-value K_AA->K_X fiber
has exactly aleph0 members. The result uses COUNTABILITY of the
new attained triple observation, not an unproved original F54
unconditional 14D Countable statement.

Append-only, same-root 107, no Gray, no original P92B category laws,
no global S->K_AA faithfulness, no 19D filler or hyperdescent.
Pinned Lean 4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected PR #1558 remains Draft/open/unmerged.
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

section OriginalSecondKernelFactor
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- The true triple-kernel unit maps to the old enhanced unit. -/
@[simp] theorem nativeGK4AAForgetBackward_unit :
    nativeGK4AAForgetBackward t₁ t₁
      (nativeGK4AAEnhancedKernelUnit t₁) =
        nativeGK4YEnhancedKernelUnit t₁ := rfl

/-- True K_AA -> K_X quotient map preserves transported
composition, by original Q class representatives ONLY. -/
theorem nativeGK4AAForgetBackward_compose
    (u : NativeGK4SKernelClasses (nativeGK4AATripleP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AATripleP92Family p D E) t₂ t₃) :
    nativeGK4AAForgetBackward t₁ t₃
      (nativeGK4AAEnhancedKernelCompose t₁ t₂ t₃ u v) =
    nativeGK4YEnhancedKernelCompose t₁ t₂ t₃
      (nativeGK4AAForgetBackward t₁ t₂ u)
      (nativeGK4AAForgetBackward t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r
  change nativeGK4AAForgetBackward t₁ t₃
      (nativeGK4AAEnhancedKernelCompose t₁ t₂ t₃
        (nativeGK4SKernelClass (nativeGK4AATripleP92Family p D E) t₁ t₂ q)
        (nativeGK4SKernelClass (nativeGK4AATripleP92Family p D E) t₂ t₃ r)) =
    nativeGK4YEnhancedKernelCompose t₁ t₂ t₃
      (nativeGK4AAForgetBackward t₁ t₂
        (nativeGK4SKernelClass (nativeGK4AATripleP92Family p D E) t₁ t₂ q))
      (nativeGK4AAForgetBackward t₂ t₃
        (nativeGK4SKernelClass (nativeGK4AATripleP92Family p D E) t₂ t₃ r))
  rw [nativeGK4AAEnhancedKernelCompose_class,
    nativeGK4AAForgetBackward_class,
    nativeGK4AAForgetBackward_class,
    nativeGK4AAForgetBackward_class,
    nativeGK4YEnhancedKernelCompose_class]

end OriginalSecondKernelFactor

/-- A genuine functor between two separately proved quotient
categories; the underlying Q remains only a source proof set. -/
def nativeGK4AAForgetBackwardFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4AAEnhancedKernelStage p ma mb pa pb ⥤
      NativeGK4YEnhancedKernelStage p ma mb pa pb where
  obj X := ⟨X.original⟩
  map := fun {X Y} f =>
    nativeGK4AAForgetBackward X.original.2.2 Y.original.2.2 f
  map_id := by
    intro X
    exact nativeGK4AAForgetBackward_unit X.original.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4AAForgetBackward_compose
      X.original.2.2 Y.original.2.2 Z.original.2.2 f g

/-- Every original enhanced-kernel class admits a triple-kernel
preimage; the forgetting functor is full per actual Hom. -/
theorem nativeGK4AAForgetFunctor_surjective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AAEnhancedKernelStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4AAForgetBackwardFunctor p ma mb pa pb).map f) := by
  exact nativeGK4AAForgetBackward_surjective
    X.original.2.2 Y.original.2.2

/-- Exact factorization of the old TRUE S->K_X comparison through
the newly constructed TRUE S->K_AA and K_AA->K_X functors. -/
theorem nativeGK4AAForgetFunctor_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4AAForgetBackwardFunctor p ma mb pa pb).map
      ((nativeGK4AAEnhancedKernelComparisonFunctor p ma mb pa pb).map f) =
    (nativeGK4YEnhancedKernelComparisonFunctor p ma mb pa pb).map f := by
  exact nativeGK4AAForgetBackward_comparison X.2.2 Y.2.2 f

theorem nativeGK4AAForgetFunctor_factor_obj
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X : NativeGK4IStage p ma mb pa pb) :
    (nativeGK4AAForgetBackwardFunctor p ma mb pa pb).obj
        ((nativeGK4AAEnhancedKernelComparisonFunctor p ma mb pa pb).obj X) =
      (nativeGK4YEnhancedKernelComparisonFunctor p ma mb pa pb).obj X := rfl

section TrueInfiniteFiber
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- The forgetful map K_AA->K_X is non-injective on any witnessed
genuine original F54 local-rotation self-Hom. -/
theorem nativeGK4AAForgetBackward_not_injective :
    ¬ Function.Injective (nativeGK4AAForgetBackward before before) := by
  intro hinj
  have hsame := nativeGK4AABalancedTower_forget_constant rot 0 1
  have hclasses := hinj hsame
  have hidx := nativeGK4AABalancedTower_comparison_injective rot hclasses
  omega

/-- Genuine NEW kernel fiber over the single old enhanced
K_X observation class represented by the actual original R_0. -/
abbrev NativeGK4AAForgetFiber :=
  {z : NativeGK4SKernelClasses
      (nativeGK4AATripleP92Family p D E) before before //
    nativeGK4AAForgetBackward before before z =
      nativeGK4XEnhancedComparison before before
        (nativeGK4EStructuralRouteClass before before
          (nativeGK4ZBalancedTower rot 0))}

/-- Every real F54 balanced Type-valued route R_k lies in this exact
fiber, not merely in an invented ambient countable set. -/
def nativeGK4AABalancedTowerForgetFiber (k : Nat) :
    NativeGK4AAForgetFiber rot :=
  ⟨nativeGK4AATripleComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ZBalancedTower rot k)),
    by
      rw [nativeGK4AAForgetBackward_comparison]
      exact nativeGK4ZBalancedTower_comparison_constant rot k 0⟩

theorem nativeGK4AABalancedTowerForgetFiber_injective :
    Function.Injective (nativeGK4AABalancedTowerForgetFiber rot) := by
  intro i j hij
  exact nativeGK4AABalancedTower_comparison_injective rot
    (congrArg Subtype.val hij)

/-- The precise K_AA->K_X fiber has cardinality aleph0 whenever
an actual F54 local rotation is witnessed. This needs no arbitrary
source D/E countability hypothesis: K_AA itself injects into the
COUNTABLE observed triple-value type (Bool×Int)×Nat. -/
theorem nativeGK4AAForgetFiber_aleph0 :
    Cardinal.mk (NativeGK4AAForgetFiber rot) = Cardinal.aleph0 := by
  letI : Countable (NativeGK4SKernelClasses
      (nativeGK4AATripleP92Family p D E) before before) :=
    (nativeGK4AAEnhancedKernelValue_injective before before).countable
  letI : Countable (NativeGK4AAForgetFiber rot) := inferInstance
  letI : Infinite (NativeGK4AAForgetFiber rot) :=
    Infinite.of_injective (nativeGK4AABalancedTowerForgetFiber rot)
      (nativeGK4AABalancedTowerForgetFiber_injective rot)
  exact Cardinal.mk_eq_aleph0 _

end TrueInfiniteFiber

section PhysicalNorth
theorem nativeGK4AA_physical_north_forgetful_fiber_aleph0 :
    Cardinal.mk (NativeGK4AAForgetFiber
      northHexagonNativeLeftRotation) = Cardinal.aleph0 ∧
    ¬ Function.Injective (nativeGK4AAForgetBackward
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact ⟨nativeGK4AAForgetFiber_aleph0 northHexagonNativeLeftRotation,
    nativeGK4AAForgetBackward_not_injective northHexagonNativeLeftRotation⟩
end PhysicalNorth

#print axioms nativeGK4AAForgetBackward_unit
#print axioms nativeGK4AAForgetBackward_compose
#print axioms nativeGK4AAForgetBackwardFunctor
#print axioms nativeGK4AAForgetFunctor_surjective_hom
#print axioms nativeGK4AAForgetFunctor_factor_map
#print axioms nativeGK4AAForgetFunctor_factor_obj
#print axioms nativeGK4AAForgetBackward_not_injective
#print axioms NativeGK4AAForgetFiber
#print axioms nativeGK4AABalancedTowerForgetFiber
#print axioms nativeGK4AABalancedTowerForgetFiber_injective
#print axioms nativeGK4AAForgetFiber_aleph0
#print axioms nativeGK4AA_physical_north_forgetful_fiber_aleph0

end
end Kuu.F112.Physical
