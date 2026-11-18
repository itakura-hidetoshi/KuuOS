import Mathlib
import KuuOSFormal.WaWeightedSumV0_21

/-!
# KuuOS Lean→Python v0.22 — exact-rational normalization tolerance bridge

The native Python Wa validator checks an observed binary64 sum of seven
weights with tolerance 1e-9. This is *not* the exact rational constraint
that a convex weight vector sums to one.

This source proves a conditional, quantitatively bounded bridge:
  * each rational represented weight is nonnegative;
  * each represented sample belongs to [0,1];
  * their exact rational weight total is strictly positive;
  * the difference between native observed built-in sum and exact
    represented-rational weight sum is separately observed/bounded;
  * an observed weighted sum has an explicit bounded rational error.

No theorem assumes that Python's sum() is exact or has universal bounded
error; no new IEEE-754 operational semantics is asserted. The original
Wa UnitInterval / ConvexWeight model, Python kernel and ledgers are
unmodified. A rational normalized witness is a comparison construct,
not authorization to overwrite native scores.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS
namespace DecisionOS
namespace WaNormalizationV0_22

/-- Exact total of represented rational weights. -/
def rationalWeightTotal {n : ℕ} (w : Fin n → ℚ) : ℚ :=
  ∑ i, w i

/-- Exact rational weighted score of represented rational endpoints. -/
def rationalWeighted {n : ℕ} (w x : Fin n → ℚ) : ℚ :=
  ∑ i, w i * x i

/-- A mathematical normalization for comparison only, not a Python update. -/
def rationalNormalized {n : ℕ} (w x : Fin n → ℚ) : ℚ :=
  rationalWeighted w x / rationalWeightTotal w

/-- Nonnegative represented weights and endpoints yield nonnegative score. -/
theorem rational_weighted_nonnegative {n : ℕ} (w x : Fin n → ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx : ∀ i, 0 ≤ x i) :
    0 ≤ rationalWeighted w x := by
  unfold rationalWeighted
  exact Finset.sum_nonneg (fun i _ => mul_nonneg (hw i) (hx i))

/-- Endpoint values at most one bound the exact weighted score by
    the exact (not merely native-observed) total of represented weights. -/
theorem rational_weighted_le_total {n : ℕ} (w x : Fin n → ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx : ∀ i, x i ≤ 1) :
    rationalWeighted w x ≤ rationalWeightTotal w := by
  unfold rationalWeighted rationalWeightTotal
  apply Finset.sum_le_sum
  intro i _
  calc
    w i * x i ≤ w i * 1 := mul_le_mul_of_nonneg_left (hx i) (hw i)
    _ = w i := mul_one _

/-- Under an explicitly positive exact total, the mathematical
    normalized weighted score lies in [0,1]. -/
theorem rational_normalized_in_unit {n : ℕ} (w x : Fin n → ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w) :
    0 ≤ rationalNormalized w x ∧ rationalNormalized w x ≤ 1 := by
  constructor
  · unfold rationalNormalized
    exact div_nonneg (rational_weighted_nonnegative w x hw hx0)
      (le_of_lt hTotal)
  · unfold rationalNormalized
    apply (div_le_iff₀ hTotal).2
    simpa using rational_weighted_le_total w x hw hx1

/-- Exact normalization cannot change a nonnegative [0,1] weighted
    score by more than the exact represented weight-total defect. -/
theorem rational_normalization_shift_bound {n : ℕ} (w x : Fin n → ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w) :
    |rationalWeighted w x - rationalNormalized w x| ≤
      |rationalWeightTotal w - 1| := by
  have hUnit := rational_normalized_in_unit w x hw hx0 hx1 hTotal
  have hNormAbs : |rationalNormalized w x| ≤ 1 := by
    simpa [abs_of_nonneg hUnit.1] using hUnit.2
  have hIdentity :
      rationalWeighted w x - rationalNormalized w x =
        rationalNormalized w x * (rationalWeightTotal w - 1) := by
    unfold rationalNormalized
    field_simp [ne_of_gt hTotal]
  calc
    |rationalWeighted w x - rationalNormalized w x| =
      |rationalNormalized w x| * |rationalWeightTotal w - 1| := by
        rw [hIdentity, abs_mul]
    _ ≤ 1 * |rationalWeightTotal w - 1| :=
      mul_le_mul_of_nonneg_right hNormAbs (abs_nonneg _)
    _ = |rationalWeightTotal w - 1| := one_mul _

/-- Observed Python built-in sum acceptance plus independently measured
    built-in sum deviation bounds the *exact rational* weight-total defect.
    Neither hypothesis follows automatically from a Python source signature. -/
theorem native_sum_to_exact_weight_defect {n : ℕ}
    (w : Fin n → ℚ) (nativeSum tolerance sumError : ℚ)
    (hNative : |nativeSum - 1| ≤ tolerance)
    (hSum : |nativeSum - rationalWeightTotal w| ≤ sumError) :
    |rationalWeightTotal w - 1| ≤ tolerance + sumError := by
  have hIdentity :
      rationalWeightTotal w - 1 =
        (rationalWeightTotal w - nativeSum) + (nativeSum - 1) := by ring
  calc
    |rationalWeightTotal w - 1| =
        |(rationalWeightTotal w - nativeSum) + (nativeSum - 1)| := by
          rw [hIdentity]
    _ ≤ |rationalWeightTotal w - nativeSum| + |nativeSum - 1| :=
      abs_add_le _ _
    _ ≤ sumError + tolerance := by
      exact add_le_add (by simpa only [abs_sub_comm] using hSum) hNative
    _ = tolerance + sumError := add_comm _ _

/-- An explicitly bounded actual weighted observation is close to the
    exact mathematically normalized rational witness. -/
theorem observed_to_normalized_error {n : ℕ}
    (w x : Fin n → ℚ)
    (observed weightedError exactWeightDefect : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hWeighted : |observed - rationalWeighted w x| ≤ weightedError)
    (hDefect : |rationalWeightTotal w - 1| ≤ exactWeightDefect) :
    |observed - rationalNormalized w x| ≤
      weightedError + exactWeightDefect := by
  have hIdentity :
      observed - rationalNormalized w x =
        (observed - rationalWeighted w x) +
          (rationalWeighted w x - rationalNormalized w x) := by ring
  calc
    |observed - rationalNormalized w x| =
        |(observed - rationalWeighted w x) +
          (rationalWeighted w x - rationalNormalized w x)| := by
            rw [hIdentity]
    _ ≤ |observed - rationalWeighted w x| +
        |rationalWeighted w x - rationalNormalized w x| := abs_add_le _ _
    _ ≤ weightedError + exactWeightDefect :=
      add_le_add hWeighted
        (le_trans (rational_normalization_shift_bound w x hw hx0 hx1 hTotal)
          hDefect)

/-- The native tolerance and measured weight-sum error are distinct
    contributions, not an assumption of exact convex normalization. -/
theorem observed_native_tolerance_to_normalized_error {n : ℕ}
    (w x : Fin n → ℚ)
    (observedWeighted nativeSum weightedError tolerance sumError : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hWeighted : |observedWeighted - rationalWeighted w x| ≤ weightedError)
    (hNative : |nativeSum - 1| ≤ tolerance)
    (hSum : |nativeSum - rationalWeightTotal w| ≤ sumError) :
    |observedWeighted - rationalNormalized w x| ≤
      weightedError + (tolerance + sumError) := by
  exact observed_to_normalized_error w x observedWeighted weightedError
    (tolerance + sumError) hw hx0 hx1 hTotal hWeighted
    (native_sum_to_exact_weight_defect w nativeSum tolerance sumError hNative hSum)

/-- Conditional rational-to-Real transport of the observed normalization
    bound. This is not a Python interpreter semantics theorem. -/
theorem observed_native_tolerance_to_normalized_real {n : ℕ}
    (w x : Fin n → ℚ)
    (observedWeighted nativeSum weightedError tolerance sumError : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hWeighted : |observedWeighted - rationalWeighted w x| ≤ weightedError)
    (hNative : |nativeSum - 1| ≤ tolerance)
    (hSum : |nativeSum - rationalWeightTotal w| ≤ sumError) :
    |(observedWeighted : ℝ) - (rationalNormalized w x : ℝ)| ≤
      ((weightedError + (tolerance + sumError) : ℚ) : ℝ) := by
  exact_mod_cast observed_native_tolerance_to_normalized_error
    w x observedWeighted nativeSum weightedError tolerance sumError
    hw hx0 hx1 hTotal hWeighted hNative hSum

#print axioms rational_weighted_nonnegative
#print axioms rational_weighted_le_total
#print axioms rational_normalized_in_unit
#print axioms rational_normalization_shift_bound
#print axioms native_sum_to_exact_weight_defect
#print axioms observed_to_normalized_error
#print axioms observed_native_tolerance_to_normalized_error
#print axioms observed_native_tolerance_to_normalized_real

end WaNormalizationV0_22
end DecisionOS
end KUOS
