import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ALFiniteMatrixNormalForms
import Mathlib.Tactic

/-!
F112-P94D3GK4AM — first UNCONDITIONAL FAILURE of the conditional
GK4AL finite-family coverage property in an ACTUAL original F54 typed
forgetful fiber. The previous GK4AJ genuine middle word
B^3 C B^6 C B^3 is an additional element over exactly GK4AK's
old q_1, but GK4AK's Fin(2) family contains only C B^12 C
and B^6 C^2 B^6. The second matrix decoder distinguishes all
three as -184, -88, 8. Therefore FamilyCovers(1) is FALSE and
a genuinely attained matrix lies outside the proposed finite set.
This does NOT prove a fixed infinite fiber or global faithfulness.
Original P92B comparison evidence is never inferred from equal
observations. Import existing Type-valued F55/P92B/seam soundness.
Append-only/tighten-only/same-root107; strict 空 central, independent
Kuu one presentation, no Gray or hyperdescent, protect #1558.
Pinned Lean v4.30.0-rc2 / mathlib
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

section OriginalTypedNoncoverage
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- Existing GK4AJ genuine middle word lies over the ACTUAL GK4AK
q_1: no invented source cell or untyped free word is used. -/
theorem nativeGK4AMMiddle_forget :
    nativeGK4AIForgetMatrix before before (nativeGK4AJClass1 rot) =
      nativeGK4AKOldTarget rot 1 := by
  calc
    nativeGK4AIForgetMatrix before before (nativeGK4AJClass1 rot) =
        nativeGK4AIForgetMatrix before before (nativeGK4AJClass0 rot) :=
      (nativeGK4AJClass0_forget_eq_1 rot).symm
    _ = nativeGK4AKOldTarget rot 1 := by
      rw [nativeGK4AJClass0, nativeGK4AIForgetMatrix_comparison]
      unfold nativeGK4AKOldTarget
      apply (nativeGK4AGComparison_eq_iff before before _ _).mpr
      rw [nativeGK4AJWord0_oldValue, nativeGK4AKWord_oldValue]
      rfl

/-- A genuine THIRD point in the exact dependent fiber at q_1. -/
def nativeGK4AMMiddleFiberPoint :
    nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot 1) :=
  ⟨nativeGK4AJClass1 rot, nativeGK4AMMiddle_forget rot⟩

/-- Its full sound second matrix has linear decoder -88,
strictly between the two original GK4AK family values -184, 8. -/
theorem nativeGK4AMMiddle_decoder :
    nativeGK4AKDecoder
      (nativeGK4AJFiberMatrix before before
        (nativeGK4AKOldTarget rot 1) (nativeGK4AMMiddleFiberPoint rot)) =
      -88 := by
  change nativeGK4AKDecoder
    (nativeGK4AIKernelValue before before (nativeGK4AJClass1 rot)).2 = -88
  rw [nativeGK4AJClass1_matrix]
  norm_num [nativeGK4AKDecoder]

/-- Exact nonmembership: the new middle point is not either of
the two k=1 extreme members of the GK4AK family. -/
theorem nativeGK4AMMiddle_not_family (i : Fin (1 + 1)) :
    nativeGK4AMMiddleFiberPoint rot ≠ nativeGK4AKFiberPoint rot 1 i := by
  intro h
  have hd := congrArg
    (fun z : nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot 1) =>
      nativeGK4AKDecoder
        (nativeGK4AJFiberMatrix before before (nativeGK4AKOldTarget rot 1) z)) h
  rw [nativeGK4AMMiddle_decoder rot] at hd
  change (-88 : Int) =
    nativeGK4AKDecoder
      (nativeGK4AIKernelValue before before (nativeGK4AKClass rot 1 i)).2 at hd
  rw [nativeGK4AKClass_decoder rot 1 i] at hd
  have hi := i.isLt
  omega

/-- The attained second matrix of the middle element lies OUTSIDE
the finite GK4AL proposed matrix normal form at k=1. -/
theorem nativeGK4AMMiddle_matrix_not_range :
    nativeGK4AJFiberMatrix before before (nativeGK4AKOldTarget rot 1)
        (nativeGK4AMMiddleFiberPoint rot) ∉
      Set.range (nativeGK4ALFiniteFamilyMatrix rot 1) := by
  rintro ⟨i, hi⟩
  apply nativeGK4AMMiddle_not_family rot i
  apply nativeGK4AJFiberMatrix_injective before before
    (nativeGK4AKOldTarget rot 1)
  exact hi.symm

/-- MAIN NEGATIVE THEOREM: original GK4AL FamilyCovers(1) is FALSE
for every genuinely witnessed original LocalRotation. This is not
an assumption and requires NO original Q-category axioms. -/
theorem nativeGK4AMFamilyCovers_one_false :
    ¬ nativeGK4ALFamilyCovers rot 1 := by
  intro h
  obtain ⟨i, hi⟩ := h (nativeGK4AMMiddleFiberPoint rot)
  exact nativeGK4AMMiddle_not_family rot i hi.symm

end OriginalTypedNoncoverage

/-- Unconditional north-hexagon physical F54 counterexample. -/
theorem nativeGK4AMPhysicalNorth_family_not_covers_one :
    ¬ nativeGK4ALFamilyCovers northHexagonNativeLeftRotation 1 := by
  exact nativeGK4AMFamilyCovers_one_false northHexagonNativeLeftRotation

#print axioms nativeGK4AMMiddle_forget
#print axioms nativeGK4AMMiddleFiberPoint
#print axioms nativeGK4AMMiddle_decoder
#print axioms nativeGK4AMMiddle_not_family
#print axioms nativeGK4AMMiddle_matrix_not_range
#print axioms nativeGK4AMFamilyCovers_one_false
#print axioms nativeGK4AMPhysicalNorth_family_not_covers_one

end
end Kuu.F112.Physical
