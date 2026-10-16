import KUOS.DependentOriginationBinaryCantorHausdorffDimensionV4_33
import Mathlib.Analysis.SpecialFunctions.Log.Base
import Mathlib

namespace KUOS.DependentOriginationCantorCriticalExponentV4_34

set_option autoImplicit false

noncomputable section

/-!
# Critical Cantor exponent v4.34

The ternary Cantor critical exponent is

  s = log_3 2 = log 2 / log 3.

This file isolates the real-number algebra needed by the later Hölder
transport, independently of the metric coding argument.

This unit is validated against canonical merged v4.33.

We prove:

* 0 < s < 1;
* 3^s = 2;
* s * log_2 3 = 1;
* (log_2 3)^(-1) = s.

These are exactly the scale identities relating binary cylinders of diameter
2^(-n) to ternary cylinders of diameter 3^(-n).
-/

/-- The real critical exponent of the classical ternary Cantor set. -/
noncomputable def cantorCriticalExponentReal : ℝ :=
  Real.logb 3 2

/-- The same exponent bundled as a nonnegative real for Hölder APIs. -/
noncomputable def cantorCriticalExponent : NNReal :=
  ⟨cantorCriticalExponentReal,
    (Real.logb_pos (by norm_num : (1 : ℝ) < 3)
      (by norm_num : (1 : ℝ) < 2)).le⟩

@[simp] theorem cantorCriticalExponent_coe :
    (cantorCriticalExponent : ℝ) = cantorCriticalExponentReal := by
  rfl

/-- The critical exponent is the familiar quotient log 2 / log 3. -/
theorem cantorCriticalExponentReal_eq_log_div_log :
    cantorCriticalExponentReal =
      Real.log 2 / Real.log 3 := by
  exact (Real.log_div_log (b := 3) (x := 2)).symm

/-- Positivity of the critical exponent. -/
theorem cantorCriticalExponentReal_pos :
    0 < cantorCriticalExponentReal := by
  exact
    Real.logb_pos
      (by norm_num : (1 : ℝ) < 3)
      (by norm_num : (1 : ℝ) < 2)

/-- The critical exponent is strictly less than one. -/
theorem cantorCriticalExponentReal_lt_one :
    cantorCriticalExponentReal < 1 := by
  calc
    cantorCriticalExponentReal = Real.logb 3 2 := rfl
    _ < Real.logb 3 3 := by
      exact Real.logb_lt_logb
        (by norm_num : (1 : ℝ) < 3)
        (by norm_num : (0 : ℝ) < 2)
        (by norm_num : (2 : ℝ) < 3)
    _ = 1 := Real.logb_self_eq_one (by norm_num)

/-- Bundled positivity for Hölder-dimension theorems. -/
theorem cantorCriticalExponent_pos :
    0 < cantorCriticalExponent := by
  change 0 < cantorCriticalExponentReal
  exact cantorCriticalExponentReal_pos

/-- Bundled upper bound. -/
theorem cantorCriticalExponent_lt_one :
    cantorCriticalExponent < 1 := by
  change cantorCriticalExponentReal < 1
  exact cantorCriticalExponentReal_lt_one

/-- Ternary scaling to the critical exponent equals binary scaling. -/
theorem three_rpow_cantorCriticalExponent :
    (3 : ℝ) ^ cantorCriticalExponentReal = 2 := by
  simpa [cantorCriticalExponentReal] using
    (Real.rpow_logb (b := 3) (x := 2)
      (by norm_num : (0 : ℝ) < 3)
      (by norm_num : (3 : ℝ) ≠ 1)
      (by norm_num : (0 : ℝ) < 2))

/-- The reciprocal exponent for binary-to-ternary transport. -/
theorem inv_logb_two_three_eq_cantorCriticalExponent :
    (Real.logb 2 3)⁻¹ = cantorCriticalExponentReal := by
  simpa [cantorCriticalExponentReal] using
    (Real.inv_logb 2 3)

/-- The two reciprocal logarithmic exponents multiply to one. -/
theorem cantorCriticalExponent_mul_logb_two_three :
    cantorCriticalExponentReal * Real.logb 2 3 = 1 := by
  calc
    cantorCriticalExponentReal * Real.logb 2 3 =
        Real.logb 3 2 * Real.logb 2 3 := rfl
    _ = Real.logb 3 3 := by
      exact
        Real.mul_logb (a := 3) (b := 2) (c := 3)
          (by norm_num : (2 : ℝ) ≠ 0)
          (by norm_num : (2 : ℝ) ≠ 1)
          (by norm_num : (2 : ℝ) ≠ -1)
    _ = 1 := Real.logb_self_eq_one (by norm_num)

/-- The reciprocal binary-to-ternary exponent is greater than one. -/
theorem one_lt_logb_two_three :
    (1 : ℝ) < Real.logb 2 3 := by
  simpa using
    (Real.logb_lt_logb (b := 2) (x := 2) (y := 3)
      (by norm_num : (1 : ℝ) < 2)
      (by norm_num : (0 : ℝ) < 2)
      (by norm_num : (2 : ℝ) < 3))

/-- A useful restatement of the exact requested real value. -/
theorem cantorCriticalExponentReal_eq_requested :
    cantorCriticalExponentReal =
      Real.log 2 / Real.log 3 :=
  cantorCriticalExponentReal_eq_log_div_log

/-!
## Boundary after v4.34

The critical exponent algebra is now independent of the geometric proof.

The next unit must prove the quantitative coding bounds:

* binary -> ternary is Hölder with exponent log_2 3;
* ternary Cantor -> binary is Hölder with exponent log_3 2.

Together with v4.33, the Hausdorff-dimension transport theorems then force

  dim_H(CantorSet) = log_3 2 = log 2 / log 3.
-/

end

end KUOS.DependentOriginationCantorCriticalExponentV4_34
