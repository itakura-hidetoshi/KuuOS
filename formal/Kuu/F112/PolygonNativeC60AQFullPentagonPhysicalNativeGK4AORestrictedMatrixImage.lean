import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AOIntegralCongruence
import Mathlib.Tactic

/-!
F112-P94D3GK4AO — genuinely STRICT arithmetic image obstruction:
the integer matrix [[1,0],[1,1]] has determinant 1, but fails the
lower-left 4-divisibility of every original F54 GK4AH matrix.
Consequently it is not attained on ANY original dependent F54 Hom,
original P92B Q, independently constructed S, actual K_AI, or ANY
of the real K_AI -> K_AG forgotten fibers. Thus determinant 1 is
necessary but not sufficient for attainability. We exhibit a
proper arithmetic ambient domain without asserting every member
of Gamma_1(4) is reachable. A faithful subtype embedding into the
congruence monoid strengthens the GK4AL original fiber matrix code.
No original Q category axioms, new Type-cell, fixed infinite fiber,
global S->K_AI faithfulness, Gray or hyperdescent is asserted.
Append-only/tighten-only/same-root107. Strict 空 central.
Protected PR #1558 remains Draft/open/unmerged. Lean v4.30.0-rc2
and mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6 pinned.
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

/-- An explicit unit-determinant integer matrix forbidden by the
actual original F54 Type-valued history congruence. -/
def nativeGK4AOExcludedSLMatrix : NativeGK4AHMatrix :=
  (((1 : Int), (0 : Int)), ((1 : Int), (1 : Int)))

theorem nativeGK4AOExcludedSLMatrix_det :
    nativeGK4AODet nativeGK4AOExcludedSLMatrix = 1 := by decide

/-- The obstruction is strictly stronger than determinant one:
the bottom-left entry 1 is NOT divisible by 4. -/
theorem nativeGK4AOExcludedSLMatrix_not_congruence :
    ¬ nativeGK4AOIntegralCongruence nativeGK4AOExcludedSLMatrix := by
  intro h
  rcases h with ⟨_, _, ⟨c, hc⟩, _⟩
  change (1 : Int) = 4 * c at hc
  omega

section ExactUnattainability
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- No element of the ORIGINAL P92B proof-existence quotient has
the excluded determinant-one matrix as its genuine second value. -/
theorem nativeGK4AOExcludedSLMatrix_not_P92
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4AHP92Value first last q ≠ nativeGK4AOExcludedSLMatrix := by
  intro h
  have hq := nativeGK4AOP92_sound first last q
  rw [h] at hq
  exact nativeGK4AOExcludedSLMatrix_not_congruence hq

/-- The independently presented structural S cannot attain it,
without any appeal to the original Q category axioms. -/
theorem nativeGK4AOExcludedSLMatrix_not_structural
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AHStructuralValue first last s ≠ nativeGK4AOExcludedSLMatrix := by
  intro h
  have hs := nativeGK4AOStructural_sound first last s
  rw [h] at hs
  exact nativeGK4AOExcludedSLMatrix_not_congruence hs

/-- No element of the actual attained second quotient K_AI can
attain the excluded 2x2 matrix on ANY fully dependent F45 Hom. -/
theorem nativeGK4AOExcludedSLMatrix_not_kernel
    (z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) first last) :
    (nativeGK4AIKernelValue first last z).2 ≠ nativeGK4AOExcludedSLMatrix := by
  intro h
  have hz := nativeGK4AOKernel_sound first last z
  rw [h] at hz
  exact nativeGK4AOExcludedSLMatrix_not_congruence hz

/-- Strictness of the Gamma_1(4) obstruction at EVERY genuinely
attained old target: determinant 1 alone is insufficient. -/
theorem nativeGK4AOExcludedSLMatrix_not_fiber
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AOExcludedSLMatrix ∉
      nativeGK4ALAttainedMatrixSet first last target := by
  exact nativeGK4AOUnattainable_of_not_congruence first last target
    nativeGK4AOExcludedSLMatrix
    nativeGK4AOExcludedSLMatrix_not_congruence

theorem nativeGK4AOProperDetOneAmbient
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    ∃ M : NativeGK4AHMatrix,
      nativeGK4AODet M = 1 ∧
        M ∉ nativeGK4ALAttainedMatrixSet first last target := by
  exact ⟨nativeGK4AOExcludedSLMatrix,
    nativeGK4AOExcludedSLMatrix_det,
    nativeGK4AOExcludedSLMatrix_not_fiber first last target⟩

/-- The actual dependent fiber embeds into the *arithmetically
admissible* integer matrices, not just all (Z^4) matrices. -/
def nativeGK4AORestrictedFiberMatrixEmbedding
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ↪
      {M : NativeGK4AHMatrix // nativeGK4AOIntegralCongruence M} where
  toFun z :=
    ⟨nativeGK4AJFiberMatrix first last target z,
      nativeGK4AOFiber_sound first last target z⟩
  inj' := by
    intro x y h
    apply nativeGK4AJFiberMatrix_injective first last target
    exact congrArg Subtype.val h

/-- EXACT relative normal form in the ACTUALLY ATTAINED portion
of Gamma_1(4). Surjectivity onto the entire subgroup is NOT claimed. -/
def nativeGK4AORestrictedAttainedFiberEquiv
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4AJOldFiber first last target ≃
      {M : {N : NativeGK4AHMatrix // nativeGK4AOIntegralCongruence N} //
        M ∈ Set.range (nativeGK4AORestrictedFiberMatrixEmbedding first last target)} :=
  Equiv.ofBijective
    (fun z => ⟨nativeGK4AORestrictedFiberMatrixEmbedding first last target z,
      ⟨z, rfl⟩⟩)
    ⟨(by
       intro x y h
       apply (nativeGK4AORestrictedFiberMatrixEmbedding first last target).injective
       exact congrArg Subtype.val h),
     (by
       rintro ⟨M, ⟨z, hz⟩⟩
       refine ⟨z, ?_⟩
       exact Subtype.ext hz)⟩

end ExactUnattainability

#print axioms nativeGK4AOExcludedSLMatrix
#print axioms nativeGK4AOExcludedSLMatrix_det
#print axioms nativeGK4AOExcludedSLMatrix_not_congruence
#print axioms nativeGK4AOExcludedSLMatrix_not_P92
#print axioms nativeGK4AOExcludedSLMatrix_not_structural
#print axioms nativeGK4AOExcludedSLMatrix_not_kernel
#print axioms nativeGK4AOExcludedSLMatrix_not_fiber
#print axioms nativeGK4AOProperDetOneAmbient
#print axioms nativeGK4AORestrictedFiberMatrixEmbedding
#print axioms nativeGK4AORestrictedAttainedFiberEquiv

end
end Kuu.F112.Physical
