import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AJTernaryPhysicalFiber
import Mathlib.Tactic

/-!
F112-P94D3GK4AJ — exact invariant classification INSIDE each
genuine attained forgetful K_AI -> K_AG fiber. The second GK4AH
integer matrix observation is injective on every fixed old-K_AG
fiber: two new K_AI classes with the same old image are identical
if and only if their new matrices agree.

This is an exact FIRST ISOMORPHISM statement on the attained image,
not a global S->K_AI faithfulness assertion and not a claim of all
integer matrices being attainable. It is valid for arbitrary original
dependent F45 source/target trees and any underlying D/E categories.

A genuine original F54 LocalRotation gives three distinct K_AI
classes within ONE fixed old K_AG fiber. Their new integer matrices
are different, and the physical C60 north supplies an unconditional
specialization. No new axiom, sorry, original Q category laws, Gray,
historical full typed equivalence or hyperdescent.
Append-only, same-root107, strict 空 central; independent Kuu one
presentation; protect PR #1558 Draft/open/unmerged.
Pinned Lean v4.30.0-rc2/mathlib
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

section ExactAttainedFiber
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- The ACTUAL second GK4AH matrix component on original
P92B second-kernel K_AI classes, not a raw F54 word map. -/
def nativeGK4AJSecondMatrixValue
    (z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) first last) :
    NativeGK4AHMatrix :=
  (nativeGK4AIKernelValue first last z).2

/-- Exact pair of tests for equality in the new genuine K_AI:
old K_AG class equality AND new GK4AH matrix equality. -/
theorem nativeGK4AJKernel_eq_iff_two_components
    (u v : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) first last) :
    u = v ↔
      nativeGK4AIForgetMatrix first last u =
        nativeGK4AIForgetMatrix first last v ∧
      nativeGK4AJSecondMatrixValue first last u =
        nativeGK4AJSecondMatrixValue first last v := by
  constructor
  · intro h
    exact ⟨congrArg (nativeGK4AIForgetMatrix first last) h,
      congrArg (nativeGK4AJSecondMatrixValue first last) h⟩
  · rintro ⟨hold, hmatrix⟩
    apply nativeGK4AIKernelValue_injective first last
    apply Prod.ext
    · have hvalue := congrArg (nativeGK4AGKernelValue first last) hold
      simpa only [nativeGK4AIForgetMatrix_value] using hvalue
    · exact hmatrix

/-- All ACTUAL joint classes lying above a fixed previously
attained old K_AG class. No unjustified ambient surjectivity. -/
def nativeGK4AJOldFiber
    (target : NativeGK4SKernelClasses
        (nativeGK4AGP92Family p D E) first last) : Type _ :=
  {z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) first last //
    nativeGK4AIForgetMatrix first last z = target}

/-- The second matrix observation restricted to the specific
typed, already-attained old K_AG fiber. -/
def nativeGK4AJFiberMatrix
    (target : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) first last)
    (z : nativeGK4AJOldFiber first last target) : NativeGK4AHMatrix :=
  nativeGK4AJSecondMatrixValue first last z.1

/-- The second GK4AH matrix is EXACTLY injective WITHIN each
fixed old observational fiber; it need not be globally injective. -/
theorem nativeGK4AJFiberMatrix_injective
    (target : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) first last) :
    Function.Injective (nativeGK4AJFiberMatrix first last target) := by
  intro x y hmatrix
  apply Subtype.ext
  exact (nativeGK4AJKernel_eq_iff_two_components first last x.1 y.1).mpr
    ⟨x.2.trans y.2.symm, hmatrix⟩

/-- FIRST-ISOMORPHISM-type equivalence of the original typed
forgotten-fiber and the ACTUALLY ATTAINED new-matrix image there.
No arbitrary integer matrix or ghost Type-valued 3-cell appears. -/
def nativeGK4AJFiberMatrixImageEquiv
    (target : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ≃
      {m : NativeGK4AHMatrix //
        ∃ z : nativeGK4AJOldFiber first last target,
          nativeGK4AJFiberMatrix first last target z = m} :=
  Equiv.ofBijective
    (fun z => ⟨nativeGK4AJFiberMatrix first last target z, ⟨z, rfl⟩⟩)
    ⟨(by
       intro x y h
       apply nativeGK4AJFiberMatrix_injective first last target
       exact congrArg Subtype.val h),
     (by
       rintro ⟨m, ⟨z, hz⟩⟩
       refine ⟨z, ?_⟩
       apply Subtype.ext
       exact hz)⟩

end ExactAttainedFiber

section GenuineThreePointFiber
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- The old K_AG class already ATTAINED by the three true F54
histories, fixed once for the entire ternary fiber. -/
def nativeGK4AJCommonOldTarget :
    NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) before before :=
  nativeGK4AIForgetMatrix before before (nativeGK4AJClass0 rot)

/-- Three distinct elements of the SAME dependent TYPE fiber. -/
def nativeGK4AJFiberPoint0 :
    nativeGK4AJOldFiber before before (nativeGK4AJCommonOldTarget rot) :=
  ⟨nativeGK4AJClass0 rot, rfl⟩

def nativeGK4AJFiberPoint1 :
    nativeGK4AJOldFiber before before (nativeGK4AJCommonOldTarget rot) :=
  ⟨nativeGK4AJClass1 rot, (nativeGK4AJClass0_forget_eq_1 rot).symm⟩

def nativeGK4AJFiberPoint2 :
    nativeGK4AJOldFiber before before (nativeGK4AJCommonOldTarget rot) :=
  ⟨nativeGK4AJClass2 rot, (nativeGK4AJClass0_forget_eq_2 rot).symm⟩

/-- ONE old attained fiber contains THREE distinct new source
classes. This is stronger than merely proving the forgetful map
noninjective with a pair of witnesses. -/
theorem nativeGK4AJ_three_distinct_in_exact_fiber :
    nativeGK4AJFiberPoint0 rot ≠ nativeGK4AJFiberPoint1 rot ∧
    nativeGK4AJFiberPoint0 rot ≠ nativeGK4AJFiberPoint2 rot ∧
    nativeGK4AJFiberPoint1 rot ≠ nativeGK4AJFiberPoint2 rot := by
  constructor
  · intro h
    exact nativeGK4AJClass0_ne_1 rot (congrArg Subtype.val h)
  constructor
  · intro h
    exact nativeGK4AJClass0_ne_2 rot (congrArg Subtype.val h)
  · intro h
    exact nativeGK4AJClass1_ne_2 rot (congrArg Subtype.val h)

/-- The three distinct points are separated by the SECOND matrix
inside the same old image, illustrating exact fiber-image injectivity. -/
theorem nativeGK4AJ_three_matrix_values_pairwise_ne :
    nativeGK4AJFiberMatrix before before (nativeGK4AJCommonOldTarget rot)
        (nativeGK4AJFiberPoint0 rot) ≠
      nativeGK4AJFiberMatrix before before (nativeGK4AJCommonOldTarget rot)
        (nativeGK4AJFiberPoint1 rot) ∧
    nativeGK4AJFiberMatrix before before (nativeGK4AJCommonOldTarget rot)
        (nativeGK4AJFiberPoint0 rot) ≠
      nativeGK4AJFiberMatrix before before (nativeGK4AJCommonOldTarget rot)
        (nativeGK4AJFiberPoint2 rot) ∧
    nativeGK4AJFiberMatrix before before (nativeGK4AJCommonOldTarget rot)
        (nativeGK4AJFiberPoint1 rot) ≠
      nativeGK4AJFiberMatrix before before (nativeGK4AJCommonOldTarget rot)
        (nativeGK4AJFiberPoint2 rot) := by
  rcases nativeGK4AJ_three_distinct_in_exact_fiber rot with ⟨h01, h02, h12⟩
  constructor
  · intro h
    exact h01 (nativeGK4AJFiberMatrix_injective before before
      (nativeGK4AJCommonOldTarget rot) h)
  constructor
  · intro h
    exact h02 (nativeGK4AJFiberMatrix_injective before before
      (nativeGK4AJCommonOldTarget rot) h)
  · intro h
    exact h12 (nativeGK4AJFiberMatrix_injective before before
      (nativeGK4AJCommonOldTarget rot) h)

end GenuineThreePointFiber

/-- True physical C60 north: there exist THREE distinct K_AI
classes in ONE and the SAME K_AG forgetful target on the original
physical north F45 self-Hom. -/
theorem nativeGK4AJPhysicalNorth_three_classes_one_fiber :
    ∃ x y z : NativeGK4SKernelClasses
        (nativeGK4AIP92Family _ _ _)
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      x ≠ y ∧ x ≠ z ∧ y ≠ z ∧
      nativeGK4AIForgetMatrix
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple x =
        nativeGK4AIForgetMatrix
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple y ∧
      nativeGK4AIForgetMatrix
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple x =
        nativeGK4AIForgetMatrix
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple z := by
  exact nativeGK4AJ_three_classes_one_fiber northHexagonNativeLeftRotation

#print axioms nativeGK4AJSecondMatrixValue
#print axioms nativeGK4AJKernel_eq_iff_two_components
#print axioms nativeGK4AJOldFiber
#print axioms nativeGK4AJFiberMatrix
#print axioms nativeGK4AJFiberMatrix_injective
#print axioms nativeGK4AJFiberMatrixImageEquiv
#print axioms nativeGK4AJCommonOldTarget
#print axioms nativeGK4AJFiberPoint0
#print axioms nativeGK4AJFiberPoint1
#print axioms nativeGK4AJFiberPoint2
#print axioms nativeGK4AJ_three_distinct_in_exact_fiber
#print axioms nativeGK4AJ_three_matrix_values_pairwise_ne
#print axioms nativeGK4AJPhysicalNorth_three_classes_one_fiber

end
end Kuu.F112.Physical
