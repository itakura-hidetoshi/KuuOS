import Mathlib

/-!
A minimal Mathlib-only calculus kernel for the bounded-generator Araki Hessian.

This module isolates the actual derivative argument from the larger WORLD stack.
It proves that the negative derivative of the Araki first variation is the
Bogoliubov-Kubo-Mori pairing whenever the exponential-arc expectation response
has the stated derivative at the faithful reference state.
-/

namespace KUOS
namespace WORLD

noncomputable section

structure ArakiBoundedExponentialArcCalculus where
  Generator : Type
  referenceExpectation : Generator → ℝ
  expectationAlong : Generator → Generator → ℝ → ℝ
  bkmPairing : Generator → Generator → ℝ
  expectationDerivativeAtReference : ∀ k h,
    HasDerivAt (expectationAlong k h) (bkmPairing k h) 0
  bkmSymmetric : ∀ k h, bkmPairing k h = bkmPairing h k
  bkmNonnegative : ∀ h, 0 ≤ bkmPairing h h

namespace ArakiBoundedExponentialArcCalculus

variable (A : ArakiBoundedExponentialArcCalculus)

def firstVariation (k h : A.Generator) (s : ℝ) : ℝ :=
  A.referenceExpectation h - A.expectationAlong k h s

def mixedHessian (k h : A.Generator) : ℝ :=
  -deriv (A.firstVariation k h) 0

theorem firstVariation_hasDerivAt (k h : A.Generator) :
    HasDerivAt (A.firstVariation k h) (-A.bkmPairing k h) 0 := by
  simpa [firstVariation] using
    (A.expectationDerivativeAtReference k h).const_sub
      (A.referenceExpectation h)

theorem mixedHessian_eq_bkm (k h : A.Generator) :
    A.mixedHessian k h = A.bkmPairing k h := by
  have hderiv := A.firstVariation_hasDerivAt k h
  unfold mixedHessian
  rw [hderiv.deriv]
  simp

theorem mixedHessian_symmetric (k h : A.Generator) :
    A.mixedHessian k h = A.mixedHessian h k := by
  rw [A.mixedHessian_eq_bkm, A.mixedHessian_eq_bkm]
  exact A.bkmSymmetric k h

theorem mixedHessian_nonnegative (h : A.Generator) :
    0 ≤ A.mixedHessian h h := by
  rw [A.mixedHessian_eq_bkm]
  exact A.bkmNonnegative h

end ArakiBoundedExponentialArcCalculus
end
end WORLD
end KUOS
