import Mathlib
import KuuOSFormal.WaNormalizedScoreV0_23

/-!
# KuuOS Lean→Python v0.24 — observed upper-Wa clipping bridge

The original Wa evaluator performs an upper-score floating-point
multiplication and then takes `min(1.0, rawUpper)`. We prove only
a conditional rational/Real *clipping inequality*, with an explicit
observational identity for that native result. This is not a model
of CPython min(), floating-point implementations or source authenticity.

No existing Lean declarations or original Wa runtime are modified.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS
namespace DecisionOS
namespace WaUpperClipV0_24

open WaRationalBridgeV0_19 WaNormalizationV0_22 WaNormalizedScoreV0_23

/-- An exact rational normalized Wa ideal is inside the unit interval
    when its four scalar inputs have their declared unit constraints. -/
theorem rational_normalized_wa_ideal_in_unit
    (beta normalized weakest alert : ℚ)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hNorm0 : 0 ≤ normalized) (hNorm1 : normalized ≤ 1)
    (hWeak0 : 0 ≤ weakest) (hWeak1 : weakest ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1) :
    0 ≤ rationalIdeal beta normalized weakest alert ∧
      rationalIdeal beta normalized weakest alert ≤ 1 := by
  have hMixLeft : 0 ≤ 1 - beta := by linarith
  have hAlertFactor : 0 ≤ 1 - alert := by linarith
  have hL0 : 0 ≤ (1 - beta) * normalized :=
    mul_nonneg hMixLeft hNorm0
  have hR0 : 0 ≤ beta * weakest := mul_nonneg hBeta0 hWeak0
  have hL1 : (1 - beta) * normalized ≤ 1 - beta := by
    calc
      _ ≤ (1 - beta) * 1 := mul_le_mul_of_nonneg_left hNorm1 hMixLeft
      _ = 1 - beta := mul_one _
  have hR1 : beta * weakest ≤ beta := by
    calc
      _ ≤ beta * 1 := mul_le_mul_of_nonneg_left hWeak1 hBeta0
      _ = beta := mul_one _
  have hMix0 : 0 ≤ (1 - beta) * normalized + beta * weakest :=
    add_nonneg hL0 hR0
  have hMix1 : (1 - beta) * normalized + beta * weakest ≤ 1 := by
    linarith
  unfold rationalIdeal
  constructor
  · exact mul_nonneg hMix0 hAlertFactor
  · calc
      ((1 - beta) * normalized + beta * weakest) * (1 - alert) ≤
        1 * (1 - alert) := mul_le_mul_of_nonneg_right hMix1 hAlertFactor
      _ ≤ 1 := by simp only [one_mul]; linarith

/-- Mathematical clamping to one cannot increase the deviation from
    a comparison scalar known to be no greater than one. -/
theorem rational_min_one_error_nonexpansive
    (raw ideal : ℚ) (hIdeal : ideal ≤ 1) :
    |min (1 : ℚ) raw - ideal| ≤ |raw - ideal| := by
  by_cases hRaw : raw ≤ 1
  · simp only [min_eq_right hRaw, le_refl]
  · have hOne : (1 : ℚ) ≤ raw := le_of_lt (lt_of_not_ge hRaw)
    rw [min_eq_left hOne]
    rw [abs_of_nonneg (sub_nonneg.mpr hIdeal)]
    rw [abs_of_nonneg (sub_nonneg.mpr (le_trans hIdeal hOne))]
    linarith

/-- The measured, explicitly identified native upper clipping is
    nonexpansive relative to an ideal normalized Wa score. -/
theorem observed_upper_clip_normalized_error
    (beta observedWeighted normalized weakest alert rawUpper clippedUpper
      waError normalizedError : ℚ)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hNorm0 : 0 ≤ normalized) (hNorm1 : normalized ≤ 1)
    (hWeak0 : 0 ≤ weakest) (hWeak1 : weakest ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1)
    (hClip : clippedUpper = min (1 : ℚ) rawUpper)
    (hWa : |rawUpper -
      rationalIdeal beta observedWeighted weakest alert| ≤ waError)
    (hWeight : |observedWeighted - normalized| ≤ normalizedError) :
    |clippedUpper - rationalIdeal beta normalized weakest alert| ≤
      waError + normalizedError := by
  have hUnit := rational_normalized_wa_ideal_in_unit
    beta normalized weakest alert hBeta0 hBeta1
    hNorm0 hNorm1 hWeak0 hWeak1 hAlert0 hAlert1
  have hRaw := observed_wa_from_normalized_weight
    beta observedWeighted normalized weakest alert rawUpper
    waError normalizedError hBeta0 hBeta1 hAlert0 hAlert1 hWa hWeight
  simpa only [hClip] using
    (le_trans
      (rational_min_one_error_nonexpansive rawUpper
        (rationalIdeal beta normalized weakest alert) hUnit.2) hRaw)

/-- v0.22 normalization evidence and the observed native *unclipped*
    upper arithmetic error compose through the original upper clipping. -/
theorem native_clipped_upper_final_wa_error {n : ℕ}
    (w x : Fin n → ℚ)
    (beta weakest alert observedWeighted rawUpper clippedUpper nativeSum
      weightError waError tolerance builtinWeightSumError : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hWeak0 : 0 ≤ weakest) (hWeak1 : weakest ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1)
    (hWeighted : |observedWeighted - rationalWeighted w x| ≤ weightError)
    (hNative : |nativeSum - 1| ≤ tolerance)
    (hSum : |nativeSum - rationalWeightTotal w| ≤ builtinWeightSumError)
    (hClip : clippedUpper = min (1 : ℚ) rawUpper)
    (hWa : |rawUpper -
      rationalIdeal beta observedWeighted weakest alert| ≤ waError) :
    |clippedUpper -
      rationalIdeal beta (rationalNormalized w x) weakest alert| ≤
      waError + (weightError + (tolerance + builtinWeightSumError)) := by
  have hUnit := rational_normalized_in_unit w x hw hx0 hx1 hTotal
  have hBound := observed_native_tolerance_to_normalized_error
    w x observedWeighted nativeSum weightError tolerance
    builtinWeightSumError hw hx0 hx1 hTotal hWeighted hNative hSum
  exact observed_upper_clip_normalized_error
    beta observedWeighted (rationalNormalized w x) weakest alert
    rawUpper clippedUpper waError
    (weightError + (tolerance + builtinWeightSumError))
    hBeta0 hBeta1 hUnit.1 hUnit.2 hWeak0 hWeak1
    hAlert0 hAlert1 hClip hWa hBound

/-- The conditional observed upper clipping and normalization estimate
    transfers to the existing Real-valued mathematical Wa ideal. -/
theorem native_clipped_upper_final_wa_real {n : ℕ}
    (w x : Fin n → ℚ)
    (beta weakest alert observedWeighted rawUpper clippedUpper nativeSum
      weightError waError tolerance builtinWeightSumError : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hWeak0 : 0 ≤ weakest) (hWeak1 : weakest ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1)
    (hWeighted : |observedWeighted - rationalWeighted w x| ≤ weightError)
    (hNative : |nativeSum - 1| ≤ tolerance)
    (hSum : |nativeSum - rationalWeightTotal w| ≤ builtinWeightSumError)
    (hClip : clippedUpper = min (1 : ℚ) rawUpper)
    (hWa : |rawUpper -
      rationalIdeal beta observedWeighted weakest alert| ≤ waError) :
    |(clippedUpper : ℝ) -
      realIdeal (beta : ℝ) (rationalNormalized w x : ℝ)
        (weakest : ℝ) (alert : ℝ)| ≤
      ((waError + (weightError + (tolerance + builtinWeightSumError)) : ℚ) : ℝ) := by
  have hFinal := native_clipped_upper_final_wa_error
    w x beta weakest alert observedWeighted rawUpper clippedUpper nativeSum
    weightError waError tolerance builtinWeightSumError
    hw hx0 hx1 hTotal hBeta0 hBeta1 hWeak0 hWeak1 hAlert0 hAlert1
    hWeighted hNative hSum hClip hWa
  exact certified_rational_error_is_real_error beta
    (rationalNormalized w x) weakest alert clippedUpper
    (waError + (weightError + (tolerance + builtinWeightSumError))) hFinal

#print axioms rational_normalized_wa_ideal_in_unit
#print axioms rational_min_one_error_nonexpansive
#print axioms observed_upper_clip_normalized_error
#print axioms native_clipped_upper_final_wa_error
#print axioms native_clipped_upper_final_wa_real

end WaUpperClipV0_24
end DecisionOS
end KUOS
