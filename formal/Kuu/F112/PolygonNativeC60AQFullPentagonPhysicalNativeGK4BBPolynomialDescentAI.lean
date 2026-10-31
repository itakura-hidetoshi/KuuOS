import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAOnePointDeterminacy
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AIKernelCategory
import Mathlib.Tactic

/-!
F112-P94D3GK4BB — the genuinely original GK4AV full-polynomial
matrix family descends to the EXISTING second kernel K_AI.

GK4BA proves that the old t=4 AH matrix alone determines the
ENTIRE genuine original F54 polynomial P_r(X), with no bound on
backwardCount. Existing K_AI's observer carries AH as an actual
component. Consequently the P92B original polynomial map is
constant on K_AI's kernel fibers and admits an explicit Quotient.lift.

We prove: exact lift on all original P92B classes, recovery of the
old t=4 AH matrix from the new polynomial lift, equality iff equal
AH components on K_AI, unique descent, and the separate true
S -> K_AI comparison triangle for the independent original
structural quotient. No source Type-valued comparison cell is
inferred, and no original P92B Q category laws are assumed.

This is a theorem about existing K_AI, NOT a new quotient nor
equivalence of genuine F54 Type-valued source histories.
Append-only; maintain public root107, strict 空 center, independent
Kuu one presentation, no Gray, protected PR #1558 unmerged.
Lean v4.30.0-rc2; pinned mathlib
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

section GenuineKAIOriginalPolynomialDescent

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Actual full polynomial-matrix value on the EXISTING K_AI
kernel quotient. The proof required by Quotient.lift is exactly
GK4BA's independently certified original P92B t=4 determinacy. -/
def nativeGK4BBPolynomialOnAI
    (z : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last) :
    NativeGK4AVValue :=
  _root_.Quotient.lift
    (nativeGK4AVP92Value first last)
    (by
      intro q r h
      have hAI : nativeGK4AIP92 first last q =
          nativeGK4AIP92 first last r := h
      have hAH : nativeGK4AHP92Value first last q =
          nativeGK4AHP92Value first last r :=
        congrArg (fun v : NativeGK4AIValue => v.2) hAI
      exact nativeGK4BAP92_AH_determines first last q r hAH)
    z

/-- Exact computation on each TRUE original P92B representative;
no fabricated F54 route or Type-valued 3-cell is selected. -/
@[simp] theorem nativeGK4BBPolynomialOnAI_class
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4BBPolynomialOnAI first last
      (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) first last q) =
      nativeGK4AVP92Value first last q := rfl

/-- The entire polynomial matrix's t=4 evaluation is EXACTLY the
old actual AH component carried by the K_AI observation. -/
theorem nativeGK4BBPolynomialOnAI_eval_four
    (z : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last) :
    nativeGK4AVPolyEval 4 (nativeGK4BBPolynomialOnAI first last z) =
      (nativeGK4AIKernelValue first last z).2 := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  change nativeGK4AVPolyEval 4
      (nativeGK4AVP92Value first last q) =
      nativeGK4AHP92Value first last q
  exact (nativeGK4AVP92_recover first last q).2

/-- Existing K_AI polynomial equality is EXACTLY AH equality,
not equality of raw source Type-valued evidence. -/
theorem nativeGK4BBPolynomialOnAI_eq_iff_AH
    (u v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last) :
    nativeGK4BBPolynomialOnAI first last u =
        nativeGK4BBPolynomialOnAI first last v ↔
      (nativeGK4AIKernelValue first last u).2 =
        (nativeGK4AIKernelValue first last v).2 := by
  constructor
  · intro hp
    have h4 := congrArg (nativeGK4AVPolyEval 4) hp
    simpa only [nativeGK4BBPolynomialOnAI_eval_four] using h4
  · intro hAH
    revert hAH
    refine _root_.Quotient.inductionOn₂ u v ?_
    intro q r hAH
    change nativeGK4AHP92Value first last q =
      nativeGK4AHP92Value first last r at hAH
    change nativeGK4AVP92Value first last q =
      nativeGK4AVP92Value first last r
    exact nativeGK4BAP92_AH_determines first last q r hAH

/-- A quotient-descended polynomial map satisfying the original Q
representative equations is UNIQUE, not merely a choice of section. -/
theorem nativeGK4BBPolynomialOnAI_unique
    (f : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last → NativeGK4AVValue)
    (hf : ∀ q : NativeF55P92AssocRouteClasses first last,
      f (nativeGK4SKernelClass (nativeGK4AIP92Family p D E)
        first last q) = nativeGK4AVP92Value first last q) :
    f = nativeGK4BBPolynomialOnAI first last := by
  funext z
  refine _root_.Quotient.inductionOn z ?_
  intro q
  simpa only [nativeGK4BBPolynomialOnAI_class] using hf q

/-- Independent original structural quotient S commutes with the
same EXISTING K_AI comparison, using the original full S descent.
We do not identify S with Q or manufacture their Type-valued cells. -/
theorem nativeGK4BBPolynomialOnAI_structural
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4BBPolynomialOnAI first last
      (nativeGK4AIComparison first last s) =
      nativeGK4AVStructuralValue first last s := by
  obtain ⟨q, rfl⟩ :=
    nativeGK4EP92ToStructural_surjective first last s
  have hcomp :
      nativeGK4AIComparison first last
        (nativeGK4EP92ToStructural first last q) =
        nativeGK4SKernelClass
          (nativeGK4AIP92Family p D E) first last q := by
    exact nativeGK4TComparison_class
      (nativeGK4AIP92Family p D E) first last
      (nativeGK4AISeamInvariant first last) q
  rw [hcomp, nativeGK4BBPolynomialOnAI_class]
  exact (nativeGK4AV_commutes first last q).symm

end GenuineKAIOriginalPolynomialDescent

#print axioms nativeGK4BBPolynomialOnAI
#print axioms nativeGK4BBPolynomialOnAI_class
#print axioms nativeGK4BBPolynomialOnAI_eval_four
#print axioms nativeGK4BBPolynomialOnAI_eq_iff_AH
#print axioms nativeGK4BBPolynomialOnAI_unique
#print axioms nativeGK4BBPolynomialOnAI_structural

end
end Kuu.F112.Physical
