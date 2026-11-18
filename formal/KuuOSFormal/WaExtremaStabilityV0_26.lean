import Mathlib
import KuuOSFormal.WaFiniteExtremaV0_25

/-!
# KuuOS Lean→Python v0.26 — conditional extrema-to-final-score stability

v0.25 conditionally identifies the original finite seven-axis positive
minimum and seven-axis alert maximum with exact rational list extrema.
This module propagates *explicitly supplied* weakest-axis and alert-axis
reference discrepancies through the original Wa ideal and through the
v0.22/v0.23 normalized weighted score error budget.

No arbitrary Python/IEEE 754 min/max/sum behavior, source authenticity,
or full Lean↔Python refinement is asserted. The original Wa evaluator,
stored weights/scores and all existing Lean sources remain untouched.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS
namespace DecisionOS
namespace WaExtremaStabilityV0_26

open WaRationalBridgeV0_19 WaNormalizationV0_22
open WaNormalizedScoreV0_23 WaFiniteExtremaV0_25

/-- With mixing and alert coefficients in [0,1], changing only the
    weakest-positive input cannot enlarge its absolute difference. -/
theorem rational_ideal_weakest_nonexpansive
    (beta weighted weakest targetWeakest alert : ℚ)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1) :
    |rationalIdeal beta weighted weakest alert -
      rationalIdeal beta weighted targetWeakest alert| ≤
      |weakest - targetWeakest| := by
  have hFactor0 : 0 ≤ 1 - alert := by linarith
  have hFactor1 : 1 - alert ≤ 1 := by linarith
  have hCoeff0 : 0 ≤ beta * (1 - alert) :=
    mul_nonneg hBeta0 hFactor0
  have hCoeff1 : beta * (1 - alert) ≤ 1 := by
    calc
      _ ≤ 1 * (1 - alert) :=
        mul_le_mul_of_nonneg_right hBeta1 hFactor0
      _ = 1 - alert := one_mul _
      _ ≤ 1 := hFactor1
  have hDiff :
      rationalIdeal beta weighted weakest alert -
          rationalIdeal beta weighted targetWeakest alert =
        (beta * (1 - alert)) * (weakest - targetWeakest) := by
    unfold rationalIdeal
    ring
  rw [hDiff, abs_mul, abs_of_nonneg hCoeff0]
  calc
    beta * (1 - alert) * |weakest - targetWeakest| ≤
        1 * |weakest - targetWeakest| :=
      mul_le_mul_of_nonneg_right hCoeff1 (abs_nonneg _)
    _ = |weakest - targetWeakest| := one_mul _

/-- With a normalized unit weighted score and unit weakest axis,
    changing only the alert factor cannot enlarge the alert difference. -/
theorem rational_ideal_alert_nonexpansive
    (beta normalized weakest alert targetAlert : ℚ)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hNorm0 : 0 ≤ normalized) (hNorm1 : normalized ≤ 1)
    (hWeak0 : 0 ≤ weakest) (hWeak1 : weakest ≤ 1) :
    |rationalIdeal beta normalized weakest alert -
      rationalIdeal beta normalized weakest targetAlert| ≤
      |alert - targetAlert| := by
  have hFactor0 : 0 ≤ 1 - beta := by linarith
  have hLeft0 : 0 ≤ (1 - beta) * normalized :=
    mul_nonneg hFactor0 hNorm0
  have hRight0 : 0 ≤ beta * weakest :=
    mul_nonneg hBeta0 hWeak0
  have hLeft1 : (1 - beta) * normalized ≤ 1 - beta := by
    calc
      _ ≤ (1 - beta) * 1 :=
        mul_le_mul_of_nonneg_left hNorm1 hFactor0
      _ = 1 - beta := mul_one _
  have hRight1 : beta * weakest ≤ beta := by
    calc
      _ ≤ beta * 1 := mul_le_mul_of_nonneg_left hWeak1 hBeta0
      _ = beta := mul_one _
  have hMix0 :
      0 ≤ (1 - beta) * normalized + beta * weakest :=
    add_nonneg hLeft0 hRight0
  have hMix1 :
      (1 - beta) * normalized + beta * weakest ≤ 1 := by
    linarith
  have hDiff :
      rationalIdeal beta normalized weakest alert -
          rationalIdeal beta normalized weakest targetAlert =
        ((1 - beta) * normalized + beta * weakest) *
          (targetAlert - alert) := by
    unfold rationalIdeal
    ring
  rw [hDiff, abs_mul, abs_of_nonneg hMix0]
  calc
    ((1 - beta) * normalized + beta * weakest) *
          |targetAlert - alert| ≤
        1 * |targetAlert - alert| :=
      mul_le_mul_of_nonneg_right hMix1 (abs_nonneg _)
    _ = |targetAlert - alert| := one_mul _
    _ = |alert - targetAlert| := abs_sub_comm _ _

/-- Separate weakest-positive and alert discrepancies compose into
    a final Wa ideal discrepancy once the normalized comparison is unit. -/
theorem rational_ideal_two_extrema_stability
    (beta normalized weakest targetWeakest alert targetAlert : ℚ)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hNorm0 : 0 ≤ normalized) (hNorm1 : normalized ≤ 1)
    (hTargetWeak0 : 0 ≤ targetWeakest)
    (hTargetWeak1 : targetWeakest ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1) :
    |rationalIdeal beta normalized weakest alert -
      rationalIdeal beta normalized targetWeakest targetAlert| ≤
      |weakest - targetWeakest| + |alert - targetAlert| := by
  have hWeak := rational_ideal_weakest_nonexpansive
    beta normalized weakest targetWeakest alert
    hBeta0 hBeta1 hAlert0 hAlert1
  have hAlert := rational_ideal_alert_nonexpansive
    beta normalized targetWeakest alert targetAlert
    hBeta0 hBeta1 hNorm0 hNorm1 hTargetWeak0 hTargetWeak1
  have hIdentity :
      rationalIdeal beta normalized weakest alert -
          rationalIdeal beta normalized targetWeakest targetAlert =
        (rationalIdeal beta normalized weakest alert -
          rationalIdeal beta normalized targetWeakest alert) +
        (rationalIdeal beta normalized targetWeakest alert -
          rationalIdeal beta normalized targetWeakest targetAlert) := by ring
  calc
    |rationalIdeal beta normalized weakest alert -
        rationalIdeal beta normalized targetWeakest targetAlert| =
      |(rationalIdeal beta normalized weakest alert -
          rationalIdeal beta normalized targetWeakest alert) +
        (rationalIdeal beta normalized targetWeakest alert -
          rationalIdeal beta normalized targetWeakest targetAlert)| := by
            rw [hIdentity]
    _ ≤ |rationalIdeal beta normalized weakest alert -
          rationalIdeal beta normalized targetWeakest alert| +
        |rationalIdeal beta normalized targetWeakest alert -
          rationalIdeal beta normalized targetWeakest targetAlert| :=
      abs_add_le _ _
    _ ≤ |weakest - targetWeakest| + |alert - targetAlert| :=
      add_le_add hWeak hAlert

/-- An observed raw Wa score, a certified normalized weighted input,
    and two explicitly bounded source-associated extrema discrepancies
    compose without claiming general native Python semantics. -/
theorem observed_wa_with_extrema_error
    (beta observedWeighted normalized observedWeakest targetWeakest
      observedAlert targetAlert observedWa waError normalizedWeightError
      weakestError alertError : ℚ)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hNorm0 : 0 ≤ normalized) (hNorm1 : normalized ≤ 1)
    (hTargetWeak0 : 0 ≤ targetWeakest)
    (hTargetWeak1 : targetWeakest ≤ 1)
    (hAlert0 : 0 ≤ observedAlert) (hAlert1 : observedAlert ≤ 1)
    (hWa : |observedWa -
      rationalIdeal beta observedWeighted observedWeakest observedAlert| ≤ waError)
    (hWeight : |observedWeighted - normalized| ≤ normalizedWeightError)
    (hWeak : |observedWeakest - targetWeakest| ≤ weakestError)
    (hAlert : |observedAlert - targetAlert| ≤ alertError) :
    |observedWa -
      rationalIdeal beta normalized targetWeakest targetAlert| ≤
      (waError + normalizedWeightError) + (weakestError + alertError) := by
  have hWeighted := observed_wa_from_normalized_weight
    beta observedWeighted normalized observedWeakest observedAlert
    observedWa waError normalizedWeightError
    hBeta0 hBeta1 hAlert0 hAlert1 hWa hWeight
  have hExtrema := rational_ideal_two_extrema_stability
    beta normalized observedWeakest targetWeakest observedAlert targetAlert
    hBeta0 hBeta1 hNorm0 hNorm1 hTargetWeak0 hTargetWeak1 hAlert0 hAlert1
  have hTarget :
      |rationalIdeal beta normalized observedWeakest observedAlert -
        rationalIdeal beta normalized targetWeakest targetAlert| ≤
          weakestError + alertError :=
    le_trans hExtrema (add_le_add hWeak hAlert)
  have hIdentity :
      observedWa - rationalIdeal beta normalized targetWeakest targetAlert =
        (observedWa -
          rationalIdeal beta normalized observedWeakest observedAlert) +
        (rationalIdeal beta normalized observedWeakest observedAlert -
          rationalIdeal beta normalized targetWeakest targetAlert) := by ring
  calc
    |observedWa -
      rationalIdeal beta normalized targetWeakest targetAlert| =
      |(observedWa -
        rationalIdeal beta normalized observedWeakest observedAlert) +
        (rationalIdeal beta normalized observedWeakest observedAlert -
          rationalIdeal beta normalized targetWeakest targetAlert)| := by
            rw [hIdentity]
    _ ≤ |observedWa -
          rationalIdeal beta normalized observedWeakest observedAlert| +
        |rationalIdeal beta normalized observedWeakest observedAlert -
          rationalIdeal beta normalized targetWeakest targetAlert| :=
      abs_add_le _ _
    _ ≤ (waError + normalizedWeightError) +
          (weakestError + alertError) :=
      add_le_add hWeighted hTarget

/-- The exact v0.22 native weight-total error witness and v0.26
    weakest/alert reference discrepancies give a composed final score
    bound in the original rational Wa ideal. -/
theorem native_normalized_wa_with_extrema_error {n : ℕ}
    (w x : Fin n → ℚ)
    (beta observedWeighted observedWeakest targetWeakest
      observedAlert targetAlert observedWa nativeWeightSum
      weightError waError tolerance builtinWeightSumError
      weakestError alertError : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hTargetWeak0 : 0 ≤ targetWeakest)
    (hTargetWeak1 : targetWeakest ≤ 1)
    (hAlert0 : 0 ≤ observedAlert) (hAlert1 : observedAlert ≤ 1)
    (hWeighted : |observedWeighted - rationalWeighted w x| ≤ weightError)
    (hNative : |nativeWeightSum - 1| ≤ tolerance)
    (hSum : |nativeWeightSum - rationalWeightTotal w| ≤ builtinWeightSumError)
    (hWa : |observedWa -
      rationalIdeal beta observedWeighted observedWeakest observedAlert| ≤ waError)
    (hWeak : |observedWeakest - targetWeakest| ≤ weakestError)
    (hAlert : |observedAlert - targetAlert| ≤ alertError) :
    |observedWa -
      rationalIdeal beta (rationalNormalized w x)
        targetWeakest targetAlert| ≤
      (waError + (weightError + (tolerance + builtinWeightSumError))) +
        (weakestError + alertError) := by
  have hUnit := rational_normalized_in_unit w x hw hx0 hx1 hTotal
  have hWeightBound := observed_native_tolerance_to_normalized_error
    w x observedWeighted nativeWeightSum weightError tolerance
    builtinWeightSumError hw hx0 hx1 hTotal hWeighted hNative hSum
  exact observed_wa_with_extrema_error
    beta observedWeighted (rationalNormalized w x)
    observedWeakest targetWeakest observedAlert targetAlert observedWa
    waError (weightError + (tolerance + builtinWeightSumError))
    weakestError alertError
    hBeta0 hBeta1 hUnit.1 hUnit.2
    hTargetWeak0 hTargetWeak1 hAlert0 hAlert1
    hWa hWeightBound hWeak hAlert

/-- Conditional rational-to-Real transfer of the full observed finite
    extrema and normalized weighted score error budget. -/
theorem native_normalized_wa_with_extrema_real {n : ℕ}
    (w x : Fin n → ℚ)
    (beta observedWeighted observedWeakest targetWeakest
      observedAlert targetAlert observedWa nativeWeightSum
      weightError waError tolerance builtinWeightSumError
      weakestError alertError : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hTargetWeak0 : 0 ≤ targetWeakest)
    (hTargetWeak1 : targetWeakest ≤ 1)
    (hAlert0 : 0 ≤ observedAlert) (hAlert1 : observedAlert ≤ 1)
    (hWeighted : |observedWeighted - rationalWeighted w x| ≤ weightError)
    (hNative : |nativeWeightSum - 1| ≤ tolerance)
    (hSum : |nativeWeightSum - rationalWeightTotal w| ≤ builtinWeightSumError)
    (hWa : |observedWa -
      rationalIdeal beta observedWeighted observedWeakest observedAlert| ≤ waError)
    (hWeak : |observedWeakest - targetWeakest| ≤ weakestError)
    (hAlert : |observedAlert - targetAlert| ≤ alertError) :
    |(observedWa : ℝ) -
      realIdeal (beta : ℝ) (rationalNormalized w x : ℝ)
        (targetWeakest : ℝ) (targetAlert : ℝ)| ≤
      (((waError + (weightError + (tolerance + builtinWeightSumError))) +
          (weakestError + alertError) : ℚ) : ℝ) := by
  have hBound := native_normalized_wa_with_extrema_error
    w x beta observedWeighted observedWeakest targetWeakest
    observedAlert targetAlert observedWa nativeWeightSum
    weightError waError tolerance builtinWeightSumError
    weakestError alertError
    hw hx0 hx1 hTotal hBeta0 hBeta1 hTargetWeak0 hTargetWeak1
    hAlert0 hAlert1 hWeighted hNative hSum hWa hWeak hAlert
  exact certified_rational_error_is_real_error beta
    (rationalNormalized w x) targetWeakest targetAlert observedWa
    ((waError + (weightError + (tolerance + builtinWeightSumError))) +
      (weakestError + alertError)) hBound

#print axioms rational_ideal_weakest_nonexpansive
#print axioms rational_ideal_alert_nonexpansive
#print axioms rational_ideal_two_extrema_stability
#print axioms observed_wa_with_extrema_error
#print axioms native_normalized_wa_with_extrema_error
#print axioms native_normalized_wa_with_extrema_real

end WaExtremaStabilityV0_26
end DecisionOS
end KUOS
