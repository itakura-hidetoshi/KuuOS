import Mathlib
import KUOS.DecisionOS.WaRelationalHarmonyV0_3

/-!
# Wa rational shadow of finite Python float observations (v0.19)

Theorems concern the real interpretation of exact rational operands and
explicit error certificates. They do NOT implement IEEE-754 rounding, certify
an arbitrary Python interpreter, authenticate local observations, or establish
full Lean-to-Python refinement. The original Wa kernel is not modified.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS
namespace DecisionOS
namespace WaRationalBridgeV0_19

/-- The rational, exact-operation shadow of one endpoint of the Wa formula. -/
def rationalIdeal (beta weighted weakest alert : ℚ) : ℚ :=
  ((1 - beta) * weighted + beta * weakest) * (1 - alert)

/-- The same algebraic formula interpreted in the original real-valued model. -/
def realIdeal (beta weighted weakest alert : ℝ) : ℝ :=
  ((1 - beta) * weighted + beta * weakest) * (1 - alert)

/-- Exact rational operations commute with the rational-to-real interpretation. -/
theorem rationalIdeal_cast
    (beta weighted weakest alert : ℚ) :
    (rationalIdeal beta weighted weakest alert : ℝ) =
      realIdeal (beta : ℝ) (weighted : ℝ) (weakest : ℝ) (alert : ℝ) := by
  simp [rationalIdeal, realIdeal]

/-- A verified rational error certificate transports to a real-number bound.
    This is a conditional bridge, NOT a proof that native floats always pass. -/
theorem certified_rational_error_is_real_error
    (beta weighted weakest alert observed budget : ℚ)
    (hcert : |observed - rationalIdeal beta weighted weakest alert| ≤ budget) :
    |(observed : ℝ) -
      realIdeal (beta : ℝ) (weighted : ℝ) (weakest : ℝ) (alert : ℝ)| ≤
      (budget : ℝ) := by
  have hcast :
      |(observed : ℝ) - (rationalIdeal beta weighted weakest alert : ℝ)| ≤
        (budget : ℝ) := by
    exact_mod_cast hcert
  simpa only [rationalIdeal_cast] using hcast

/-- Two explicitly bounded, nonnegative-error stages compose without
    replacing a measured bound with an unsupported IEEE-754 assertion. -/
theorem two_stage_score_error_bound
    (beta weighted weakest alert relational observed epsRel epsOut : ℝ)
    (hAlertNonnegative : 0 ≤ alert)
    (hAlertAtMostOne : alert ≤ 1)
    (hRel : |relational - ((1 - beta) * weighted + beta * weakest)| ≤ epsRel)
    (hOut : |observed - relational * (1 - alert)| ≤ epsOut)
    (hRelBudget : 0 ≤ epsRel) :
    |observed - realIdeal beta weighted weakest alert| ≤ epsOut + epsRel := by
  have hFactor : 0 ≤ 1 - alert := by linarith
  have hSecond :
      |(relational - ((1 - beta) * weighted + beta * weakest)) *
        (1 - alert)| ≤ epsRel := by
    calc
      |(relational - ((1 - beta) * weighted + beta * weakest)) *
          (1 - alert)| =
          |relational - ((1 - beta) * weighted + beta * weakest)| *
            (1 - alert) := by rw [abs_mul, abs_of_nonneg hFactor]
      _ ≤ epsRel * (1 - alert) :=
        mul_le_mul_of_nonneg_right hRel hFactor
      _ ≤ epsRel := by nlinarith [mul_nonneg hRelBudget hAlertNonnegative]
  have hIdentity :
      observed - realIdeal beta weighted weakest alert =
        (observed - relational * (1 - alert)) +
          (relational - ((1 - beta) * weighted + beta * weakest)) *
            (1 - alert) := by
    unfold realIdeal
    ring
  calc
    |observed - realIdeal beta weighted weakest alert| =
      |(observed - relational * (1 - alert)) +
        (relational - ((1 - beta) * weighted + beta * weakest)) *
          (1 - alert)| := by rw [hIdentity]
    _ ≤ |observed - relational * (1 - alert)| +
        |(relational - ((1 - beta) * weighted + beta * weakest)) *
          (1 - alert)| := abs_add_le _ _
    _ ≤ epsOut + epsRel := add_le_add hOut hSecond

/-- The IEEE-754 binary64 values corresponding to native Python's
    0.1, 0.2 and native 0.1+0.2 witness an actual rounding obstruction.
    Numerators/denominators were obtained by Python as_integer_ratio. -/
theorem binary64_addition_is_not_exact_rational_addition :
    ((1351079888211149 : ℚ) / 4503599627370496) ≠
      ((3602879701896397 : ℚ) / 36028797018963968) +
        ((3602879701896397 : ℚ) / 18014398509481984) := by
  norm_num

/-- When the original Wa input fields are exactly rational shadows, its
    real-valued waLower coincides with their real interpretation. -/
theorem rational_product_matches_original_waLower
    (relational alert : UnitInterval) (qRel qAlert : ℚ)
    (hRel : (qRel : ℝ) = relational.lower)
    (hAlert : (qAlert : ℝ) = alert.upper) :
    ((qRel * (1 - qAlert) : ℚ) : ℝ) = waLower relational alert := by
  simp [waLower, hRel, hAlert]

end WaRationalBridgeV0_19
end DecisionOS
end KUOS
