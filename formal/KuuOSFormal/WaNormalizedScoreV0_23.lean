import Mathlib
import KuuOSFormal.WaNormalizationV0_22

/-!
# KuuOS Lean→Python v0.23 — normalized Wa final-score error gluing

The existing v0.19 exact rational Wa ideal score uses a weighted input,
a weakest positive axis, an alert and a mixing coefficient.
The v0.20 native-float observation certificates bound local arithmetic.
The v0.21 typed finite products bound the *raw* weighted sum, and the
v0.22 rational normalization comparison bounds the difference between
the observed raw weighted sum and a mathematically normalized witness.

This module proves the conditional composition through the FINAL Wa
scalar score, with explicit coefficient intervals, input identity, and
observed error hypotheses. No total native Python/IEEE-754 semantics
or end-to-end source/execution authenticity is asserted.
No original Wa code, stores, proof declarations, CI or pins change.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS
namespace DecisionOS
namespace WaNormalizedScoreV0_23

open WaRationalBridgeV0_19 WaGridRoundingV0_20
open WaWeightedSumV0_21 WaNormalizationV0_22

/-- The exact rational original Wa score is nonexpansive in its
    weighted input when both mixing and alert coefficients lie in [0,1].
    This concerns arithmetic only, not an arbitrary Python execution. -/
theorem rational_ideal_weighted_contraction
    (beta weighted normalized weakest alert : ℚ)
    (hBeta0 : 0 ≤ beta)
    (hBeta1 : beta ≤ 1)
    (hAlert0 : 0 ≤ alert)
    (hAlert1 : alert ≤ 1) :
    |rationalIdeal beta weighted weakest alert -
      rationalIdeal beta normalized weakest alert| ≤
      |weighted - normalized| := by
  have hLeft0 : 0 ≤ 1 - beta := by linarith
  have hLeft1 : 1 - beta ≤ 1 := by linarith
  have hRight0 : 0 ≤ 1 - alert := by linarith
  have hRight1 : 1 - alert ≤ 1 := by linarith
  have hDifference :
      rationalIdeal beta weighted weakest alert -
          rationalIdeal beta normalized weakest alert =
        ((1 - beta) * (weighted - normalized)) * (1 - alert) := by
    unfold rationalIdeal
    ring
  rw [hDifference]
  calc
    |((1 - beta) * (weighted - normalized)) * (1 - alert)| =
        |(1 - beta) * (weighted - normalized)| * (1 - alert) := by
          rw [abs_mul, abs_of_nonneg hRight0]
    _ ≤ |(1 - beta) * (weighted - normalized)| := by
      calc
        _ ≤ |(1 - beta) * (weighted - normalized)| * 1 :=
          mul_le_mul_of_nonneg_left hRight1 (abs_nonneg _)
        _ = _ := mul_one _
    _ = (1 - beta) * |weighted - normalized| := by
      rw [abs_mul, abs_of_nonneg hLeft0]
    _ ≤ |weighted - normalized| := by
      calc
        _ ≤ 1 * |weighted - normalized| :=
          mul_le_mul_of_nonneg_right hLeft1 (abs_nonneg _)
        _ = _ := one_mul _

/-- A measured native Wa output error relative to the observed raw
    weighted input composes with a separately certified normalized
    weighted-input error. -/
theorem observed_wa_from_normalized_weight
    (beta observedWeighted normalized weakest alert observedWa
      waError normalizedWeightError : ℚ)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1)
    (hWa : |observedWa -
        rationalIdeal beta observedWeighted weakest alert| ≤ waError)
    (hWeight : |observedWeighted - normalized| ≤ normalizedWeightError) :
    |observedWa - rationalIdeal beta normalized weakest alert| ≤
      waError + normalizedWeightError := by
  have hIdentity :
      observedWa - rationalIdeal beta normalized weakest alert =
        (observedWa - rationalIdeal beta observedWeighted weakest alert) +
        (rationalIdeal beta observedWeighted weakest alert -
          rationalIdeal beta normalized weakest alert) := by ring
  calc
    |observedWa - rationalIdeal beta normalized weakest alert| =
        |(observedWa - rationalIdeal beta observedWeighted weakest alert) +
          (rationalIdeal beta observedWeighted weakest alert -
            rationalIdeal beta normalized weakest alert)| := by
          rw [hIdentity]
    _ ≤ |observedWa - rationalIdeal beta observedWeighted weakest alert| +
        |rationalIdeal beta observedWeighted weakest alert -
          rationalIdeal beta normalized weakest alert| := abs_add_le _ _
    _ ≤ waError + normalizedWeightError :=
      add_le_add hWa
        (le_trans
          (rational_ideal_weighted_contraction beta observedWeighted
            normalized weakest alert hBeta0 hBeta1 hAlert0 hAlert1)
          hWeight)

/-- The existing v0.22 conditional normalized-weight error estimate
    composes with a separately measured FINAL native Wa score error.
    Exact rational native evidence, not Python semantics, supplies
    the hypotheses. -/
theorem native_normalized_final_wa_error {n : ℕ}
    (w x : Fin n → ℚ)
    (beta weakest alert observedWeighted observedWa nativeWeightSum
      weightError waError tolerance builtinWeightSumError : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1)
    (hWeighted : |observedWeighted - rationalWeighted w x| ≤ weightError)
    (hNative : |nativeWeightSum - 1| ≤ tolerance)
    (hSum : |nativeWeightSum - rationalWeightTotal w| ≤ builtinWeightSumError)
    (hWa : |observedWa -
      rationalIdeal beta observedWeighted weakest alert| ≤ waError) :
    |observedWa -
      rationalIdeal beta (rationalNormalized w x) weakest alert| ≤
      waError + (weightError + (tolerance + builtinWeightSumError)) := by
  have hNormalized := observed_native_tolerance_to_normalized_error
    w x observedWeighted nativeWeightSum weightError tolerance
    builtinWeightSumError hw hx0 hx1 hTotal hWeighted hNative hSum
  exact observed_wa_from_normalized_weight
    beta observedWeighted (rationalNormalized w x) weakest alert
    observedWa waError (weightError + (tolerance + builtinWeightSumError))
    hBeta0 hBeta1 hAlert0 hAlert1 hWa hNormalized

/-- The final exact rational score bound transports into the original
    real-valued Wa ideal, conditional on all supplied observations. -/
theorem native_normalized_final_wa_real {n : ℕ}
    (w x : Fin n → ℚ)
    (beta weakest alert observedWeighted observedWa nativeWeightSum
      weightError waError tolerance builtinWeightSumError : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1)
    (hWeighted : |observedWeighted - rationalWeighted w x| ≤ weightError)
    (hNative : |nativeWeightSum - 1| ≤ tolerance)
    (hSum : |nativeWeightSum - rationalWeightTotal w| ≤ builtinWeightSumError)
    (hWa : |observedWa -
      rationalIdeal beta observedWeighted weakest alert| ≤ waError) :
    |(observedWa : ℝ) -
      realIdeal (beta : ℝ) (rationalNormalized w x : ℝ)
        (weakest : ℝ) (alert : ℝ)| ≤
      ((waError + (weightError + (tolerance + builtinWeightSumError)) : ℚ) : ℝ) := by
  have hFinal := native_normalized_final_wa_error
    w x beta weakest alert observedWeighted observedWa nativeWeightSum
    weightError waError tolerance builtinWeightSumError
    hw hx0 hx1 hTotal hBeta0 hBeta1 hAlert0 hAlert1
    hWeighted hNative hSum hWa
  exact certified_rational_error_is_real_error beta
    (rationalNormalized w x) weakest alert observedWa
    (waError + (weightError + (tolerance + builtinWeightSumError))) hFinal

/-- The two independently measured native Wa stages of v0.20 (relational
    mixing and alert multiplication) compose with normalized weights.
    Their local bounds do not come from a general IEEE-754 theorem. -/
theorem normalized_native_two_stage_wa_error {n : ℕ}
    (w x : Fin n → ℚ)
    (beta weakest alert observedWeighted relational observedWa
      nativeWeightSum weightError tolerance builtinWeightSumError
      epsRel epsOut : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1)
    (hWeighted : |observedWeighted - rationalWeighted w x| ≤ weightError)
    (hNative : |nativeWeightSum - 1| ≤ tolerance)
    (hSum : |nativeWeightSum - rationalWeightTotal w| ≤ builtinWeightSumError)
    (hRel :
      |relational - ((1 - beta) * observedWeighted + beta * weakest)| ≤ epsRel)
    (hOut : |observedWa - relational * (1 - alert)| ≤ epsOut)
    (hRelBudget : 0 ≤ epsRel) :
    |observedWa -
      rationalIdeal beta (rationalNormalized w x) weakest alert| ≤
      (epsOut + epsRel) +
        (weightError + (tolerance + builtinWeightSumError)) := by
  have hWa := rational_two_stage_score_error
    beta observedWeighted weakest alert relational observedWa epsRel epsOut
    hAlert0 hAlert1 hRel hOut hRelBudget
  exact native_normalized_final_wa_error w x beta weakest alert
    observedWeighted observedWa nativeWeightSum weightError
    (epsOut + epsRel) tolerance builtinWeightSumError
    hw hx0 hx1 hTotal hBeta0 hBeta1 hAlert0 hAlert1
    hWeighted hNative hSum hWa

/-- v0.21 measured finite product list can provide the raw native
    weighted-input error for v0.22 and thus the final normalized Wa
    score, provided the seven-axis list is *explicitly identified*
    with the original finite-index vector. -/
theorem certified_products_normalized_final_wa_error {n : ℕ}
    (products : List CertifiedProduct) (w x : Fin n → ℚ)
    (beta weakest alert observedWeighted observedWa nativeWeightSum
      builtinScoreSumError waError tolerance builtinWeightSumError : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1)
    (hList : exactWeighted products = rationalWeighted w x)
    (hProductSum :
      |observedWeighted - roundedWeighted products| ≤ builtinScoreSumError)
    (hNative : |nativeWeightSum - 1| ≤ tolerance)
    (hSum : |nativeWeightSum - rationalWeightTotal w| ≤ builtinWeightSumError)
    (hWa : |observedWa -
      rationalIdeal beta observedWeighted weakest alert| ≤ waError) :
    |observedWa -
      rationalIdeal beta (rationalNormalized w x) weakest alert| ≤
      waError +
        ((builtinScoreSumError +
          (products.map (fun p => p.quantum / 2)).sum) +
          (tolerance + builtinWeightSumError)) := by
  have hProducts := weighted_sum_observed_error
    products observedWeighted builtinScoreSumError hProductSum
  have hWeighted :
      |observedWeighted - rationalWeighted w x| ≤
        builtinScoreSumError +
          (products.map (fun p => p.quantum / 2)).sum := by
    rw [← hList]
    exact hProducts
  exact native_normalized_final_wa_error w x beta weakest alert
    observedWeighted observedWa nativeWeightSum
    (builtinScoreSumError + (products.map (fun p => p.quantum / 2)).sum)
    waError tolerance builtinWeightSumError
    hw hx0 hx1 hTotal hBeta0 hBeta1 hAlert0 hAlert1
    hWeighted hNative hSum hWa

/-- Explicitly certified seven-axis product list, weight normalization,
    and the actual observed final Wa score compose in the real model
    without adding a Python-implementation axiom. -/
theorem certified_products_normalized_final_wa_real {n : ℕ}
    (products : List CertifiedProduct) (w x : Fin n → ℚ)
    (beta weakest alert observedWeighted observedWa nativeWeightSum
      builtinScoreSumError waError tolerance builtinWeightSumError : ℚ)
    (hw : ∀ i, 0 ≤ w i)
    (hx0 : ∀ i, 0 ≤ x i)
    (hx1 : ∀ i, x i ≤ 1)
    (hTotal : 0 < rationalWeightTotal w)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hAlert0 : 0 ≤ alert) (hAlert1 : alert ≤ 1)
    (hList : exactWeighted products = rationalWeighted w x)
    (hProductSum :
      |observedWeighted - roundedWeighted products| ≤ builtinScoreSumError)
    (hNative : |nativeWeightSum - 1| ≤ tolerance)
    (hSum : |nativeWeightSum - rationalWeightTotal w| ≤ builtinWeightSumError)
    (hWa : |observedWa -
      rationalIdeal beta observedWeighted weakest alert| ≤ waError) :
    |(observedWa : ℝ) -
      realIdeal (beta : ℝ) (rationalNormalized w x : ℝ)
        (weakest : ℝ) (alert : ℝ)| ≤
      ((waError +
        ((builtinScoreSumError +
            (products.map (fun p => p.quantum / 2)).sum) +
          (tolerance + builtinWeightSumError)) : ℚ) : ℝ) := by
  have hBound := certified_products_normalized_final_wa_error
    products w x beta weakest alert observedWeighted observedWa
    nativeWeightSum builtinScoreSumError waError tolerance builtinWeightSumError
    hw hx0 hx1 hTotal hBeta0 hBeta1 hAlert0 hAlert1
    hList hProductSum hNative hSum hWa
  exact certified_rational_error_is_real_error beta
    (rationalNormalized w x) weakest alert observedWa
    (waError +
      ((builtinScoreSumError + (products.map (fun p => p.quantum / 2)).sum) +
        (tolerance + builtinWeightSumError))) hBound

#print axioms rational_ideal_weighted_contraction
#print axioms observed_wa_from_normalized_weight
#print axioms native_normalized_final_wa_error
#print axioms native_normalized_final_wa_real
#print axioms normalized_native_two_stage_wa_error
#print axioms certified_products_normalized_final_wa_error
#print axioms certified_products_normalized_final_wa_real

end WaNormalizedScoreV0_23
end DecisionOS
end KUOS
