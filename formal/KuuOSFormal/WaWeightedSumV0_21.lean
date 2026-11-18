import Mathlib
import KuuOSFormal.WaNeighborMidpointV0_20

/-!
# KuuOS Lean→Python v0.21: finite seven-axis weighted-sum error

This additive rational theorem concerns a FINITE list of individually
certified product observations and a separately bounded final sum.
It formalizes error propagation without replacing the original Python
built-in sum with an unverified naive-addition algorithm.

Certificate hypotheses are per-observation midpoint and neighbor-gap
inequalities from the already-certified v0.20 source. The last sum error
is measured against the exact sum of the *rounded* product observations.

This is NOT a proof of CPython built-in sum, IEEE-754 semantics,
tie-breaking, subnormal behavior, or all-input Lean/Python refinement.
No original Lean kernel, store, manifest or runtime is modified.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS
namespace DecisionOS
namespace WaWeightedSumV0_21

open WaNeighborMidpointV0_20

/-- An exact-rational record of a local product and its neighbor certificate.
    It makes required inequalities explicit instead of inferring them from
    the fact that a native floating-point operation was requested. -/
structure CertifiedProduct where
  weight : ℚ
  sample : ℚ
  rounded : ℚ
  previous : ℚ
  following : ℚ
  quantum : ℚ
  lowerMidpoint :
    (previous + rounded) / 2 ≤ weight * sample
  upperMidpoint :
    weight * sample ≤ (rounded + following) / 2
  previousGap : rounded - previous ≤ quantum
  followingGap : following - rounded ≤ quantum

/-- Ideal weighted products from the represented rational inputs. -/
def exactWeighted (xs : List CertifiedProduct) : ℚ :=
  (xs.map (fun x => x.weight * x.sample)).sum

/-- Exact rational sum of individually observed rounded products. -/
def roundedWeighted (xs : List CertifiedProduct) : ℚ :=
  (xs.map (fun x => x.rounded)).sum

/-- Signed local product errors, not a model of Python's sum algorithm. -/
def productErrors (xs : List CertifiedProduct) : List ℚ :=
  xs.map (fun x => x.rounded - x.weight * x.sample)

/-- The already-certified neighboring-midpoint inequalities supply a
    local half-quantum bound, for this specific certified product. -/
theorem certified_product_error (x : CertifiedProduct) :
    |x.rounded - x.weight * x.sample| ≤ x.quantum / 2 := by
  exact observed_neighbor_midpoint_error
    (x.weight * x.sample) x.rounded x.previous x.following x.quantum
    x.lowerMidpoint x.upperMidpoint x.previousGap x.followingGap

/-- Exact finite sums obey the triangle inequality for any rational list. -/
theorem list_abs_sum_le_sum_abs (errors : List ℚ) :
    |errors.sum| ≤ (errors.map abs).sum := by
  induction errors with
  | nil => simp
  | cons x xs ih =>
    simpa only [List.sum_cons, List.map_cons] using
      (abs_add_le x xs.sum).trans (add_le_add (le_refl |x|) ih)

/-- Difference of the two finite sums is exactly the sum of signed
    product errors: no rounding model for the final sum is used. -/
theorem rounded_minus_exact_is_sum_errors (xs : List CertifiedProduct) :
    roundedWeighted xs - exactWeighted xs = (productErrors xs).sum := by
  induction xs with
  | nil => simp [roundedWeighted, exactWeighted, productErrors]
  | cons x xs ih =>
    simp only [roundedWeighted, exactWeighted, productErrors,
      List.map_cons, List.sum_cons] at ih ⊢
    linarith

/-- Summed local absolute product errors are bounded by the sum of
    the individual certified half-quantum budgets. -/
theorem sum_product_errors_le_half_quantums (xs : List CertifiedProduct) :
    ((productErrors xs).map abs).sum ≤
      (xs.map (fun x => x.quantum / 2)).sum := by
  induction xs with
  | nil => simp [productErrors]
  | cons x xs ih =>
    simp only [productErrors, List.map_cons, List.sum_cons] at ih ⊢
    exact add_le_add (certified_product_error x) ih

/-- The sum of the rounded products differs from the exact weighted
    input sum by at most the accumulated local half-quantum budgets. -/
theorem rounded_products_sum_error (xs : List CertifiedProduct) :
    |roundedWeighted xs - exactWeighted xs| ≤
      (xs.map (fun x => x.quantum / 2)).sum := by
  calc
    |roundedWeighted xs - exactWeighted xs| =
        |(productErrors xs).sum| := by
          rw [rounded_minus_exact_is_sum_errors]
    _ ≤ ((productErrors xs).map abs).sum :=
      list_abs_sum_le_sum_abs (productErrors xs)
    _ ≤ (xs.map (fun x => x.quantum / 2)).sum :=
      sum_product_errors_le_half_quantums xs

/-- The final Python built-in sum is treated as a separate observation.
    Given a *verified* error of this sum relative to the exact rational
    sum of rounded products, the total weighted-score error is bounded. -/
theorem weighted_sum_observed_error
    (xs : List CertifiedProduct) (observed builtinError : ℚ)
    (hBuiltin : |observed - roundedWeighted xs| ≤ builtinError) :
    |observed - exactWeighted xs| ≤
      builtinError + (xs.map (fun x => x.quantum / 2)).sum := by
  have hIdentity :
      observed - exactWeighted xs =
        (observed - roundedWeighted xs) +
          (roundedWeighted xs - exactWeighted xs) := by ring
  calc
    |observed - exactWeighted xs| =
        |(observed - roundedWeighted xs) +
          (roundedWeighted xs - exactWeighted xs)| := by rw [hIdentity]
    _ ≤ |observed - roundedWeighted xs| +
        |roundedWeighted xs - exactWeighted xs| := abs_add_le _ _
    _ ≤ builtinError + (xs.map (fun x => x.quantum / 2)).sum :=
      add_le_add hBuiltin (rounded_products_sum_error xs)

/-- Transport the exact finite rational certificate to the Real
    interpretation, without equating native float evaluation to real
    arithmetic unconditionally. -/
theorem weighted_sum_observed_real_error
    (xs : List CertifiedProduct) (observed builtinError : ℚ)
    (hBuiltin : |observed - roundedWeighted xs| ≤ builtinError) :
    |(observed : ℝ) - (exactWeighted xs : ℝ)| ≤
      ((builtinError + (xs.map (fun x => x.quantum / 2)).sum : ℚ) : ℝ) := by
  exact_mod_cast weighted_sum_observed_error xs observed builtinError hBuiltin

#print axioms certified_product_error
#print axioms list_abs_sum_le_sum_abs
#print axioms rounded_minus_exact_is_sum_errors
#print axioms sum_product_errors_le_half_quantums
#print axioms rounded_products_sum_error
#print axioms weighted_sum_observed_error
#print axioms weighted_sum_observed_real_error

end WaWeightedSumV0_21
end DecisionOS
end KUOS
