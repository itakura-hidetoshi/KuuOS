import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ANShiftedOddFamily
import Mathlib.Tactic

/-!
F112-P94D3GK4AN — doubled uniform finite lower bounds in TRUE
typed forgetful K_AI -> K_AG fibers over GK4AK's exact q_k.
The k+1 original even W_k(j) witnesses are joined by ALL k
genuinely typed shifted odd half-backtrack witnesses, giving
  Fin (2*k+1) ↪ Fiber(q_k)
for every k, using the pinned mathlib finSumFinEquiv.
All original F55/P92B/seam Type-valued comparison soundness is
inherited. This is neither a fixed infinite fiber nor an exact
description of ALL attained second matrices. No original Q category
axioms, no Gray, global faithfulness or hyperdescent. Append-only,
tighten-only, same-root107; strict 空 central, independent Kuu one
presentation. Validation-only PR #1558 remains Draft/OPEN/unmerged.
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

section CombinedPhysicalFiniteFamily
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- Actual two-parity finite family, still over exactly q_k.
Even side: GK4AK Fin(k+1); odd side: GK4AN Fin(k). -/
def nativeGK4ANEvenOddFiberEmbedding (k : Nat) :
    (Fin (k + 1) ⊕ Fin k) ↪
      nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot k) where
  toFun
    | Sum.inl i => nativeGK4AKFiberPoint rot k i
    | Sum.inr i => nativeGK4ANOddFiberPoint rot k i
  inj' := by
    intro x y h
    cases x with
    | inl i =>
        cases y with
        | inl j =>
            change nativeGK4AKFiberPoint rot k i =
              nativeGK4AKFiberPoint rot k j at h
            exact congrArg Sum.inl ((nativeGK4AKFiberEmbedding rot k).injective h)
        | inr j =>
            change nativeGK4AKFiberPoint rot k i =
              nativeGK4ANOddFiberPoint rot k j at h
            exact False.elim (nativeGK4ANOdd_ne_even rot k j i h.symm)
    | inr i =>
        cases y with
        | inl j =>
            change nativeGK4ANOddFiberPoint rot k i =
              nativeGK4AKFiberPoint rot k j at h
            exact False.elim (nativeGK4ANOdd_ne_even rot k i j h)
        | inr j =>
            change nativeGK4ANOddFiberPoint rot k i =
              nativeGK4ANOddFiberPoint rot k j at h
            exact congrArg Sum.inr (nativeGK4ANOddFiberPoint_injective rot k h)

/-- MAIN theorem-construction: canonical Fin(2k+1) embeds in the
ACTUAL same old q_k dependent fiber for EVERY k>=0. The finite
cardinality is a lower bound, NOT the claimed entire fiber size. -/
def nativeGK4AN2kPlusOneFiberEmbedding (k : Nat) :
    Fin (2 * k + 1) ↪
      nativeGK4AJOldFiber before before (nativeGK4AKOldTarget rot k) where
  toFun i :=
    nativeGK4ANEvenOddFiberEmbedding rot k
      ((finSumFinEquiv (m := k + 1) (n := k)).symm
        (Fin.cast (by omega : 2 * k + 1 = (k + 1) + k) i))
  inj' := by
    intro i j h
    have hs := (nativeGK4ANEvenOddFiberEmbedding rot k).injective h
    have hc := (finSumFinEquiv (m := k + 1) (n := k)).symm.injective hs
    apply Fin.ext
    have hv := congrArg Fin.val hc
    simpa only [Fin.val_cast] using hv

/-- Every finite k has a truly attained q_k with 2k+1 distinct
K_AI classes, while the entire q_k fiber remains Countable. -/
theorem nativeGK4AN_doubled_finite_countable_fiber (k : Nat) :
    ∃ q : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E)
        before before,
      Countable (nativeGK4AJOldFiber before before q) ∧
      Nonempty (Fin (2 * k + 1) ↪ nativeGK4AJOldFiber before before q) := by
  exact ⟨nativeGK4AKOldTarget rot k,
    nativeGK4ALFiberCountable before before (nativeGK4AKOldTarget rot k),
    ⟨nativeGK4AN2kPlusOneFiberEmbedding rot k⟩⟩

end CombinedPhysicalFiniteFamily

/-- Unconditional genuine physical C60 north, not a fabricated
source generator or assumed original P92B Q category. -/
theorem nativeGK4ANPhysicalNorth_doubled_finite_countable_fiber
    (k : Nat) :
    ∃ q : NativeGK4SKernelClasses (nativeGK4AGP92Family _ _ _)
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      Countable (nativeGK4AJOldFiber nativeGK4FPhysicalNorthTriple
        nativeGK4FPhysicalNorthTriple q) ∧
      Nonempty (Fin (2 * k + 1) ↪ nativeGK4AJOldFiber
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q) := by
  exact nativeGK4AN_doubled_finite_countable_fiber
    northHexagonNativeLeftRotation k

#print axioms nativeGK4ANEvenOddFiberEmbedding
#print axioms nativeGK4AN2kPlusOneFiberEmbedding
#print axioms nativeGK4AN_doubled_finite_countable_fiber
#print axioms nativeGK4ANPhysicalNorth_doubled_finite_countable_fiber

end
end Kuu.F112.Physical
