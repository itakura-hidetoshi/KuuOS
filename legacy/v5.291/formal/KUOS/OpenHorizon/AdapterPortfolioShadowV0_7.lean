import Mathlib

/-!
Finite formal surface for the v0.7 live-plus-shadow adapter portfolio.
Shadow projections are non-actuating estimates. Only a later realized live outcome
may resolve a prediction error and update the separate portfolio bias.
-/

namespace KUOS
namespace OpenHorizon

structure ShadowPrediction where
  predictedUtility : ℚ
  predictionConfidence : ℚ
  shadowActuationCount : ℕ := 0


def realizationError (prediction : ShadowPrediction) (realizedUtility : ℚ) : ℚ :=
  realizedUtility - prediction.predictedUtility


def resolveBias
    (α oldBias : ℚ) (prediction : ShadowPrediction) (realizedUtility : ℚ) : ℚ :=
  oldBias + α * (realizationError prediction realizedUtility - oldBias)


theorem resolveBias_zero_rate
    (oldBias : ℚ) (prediction : ShadowPrediction) (realizedUtility : ℚ) :
    resolveBias 0 oldBias prediction realizedUtility = oldBias := by
  simp [resolveBias]


theorem resolveBias_full_rate
    (oldBias : ℚ) (prediction : ShadowPrediction) (realizedUtility : ℚ) :
    resolveBias 1 oldBias prediction realizedUtility =
      realizationError prediction realizedUtility := by
  simp [resolveBias]
  ring


theorem realizationError_zero_when_exact
    (prediction : ShadowPrediction) :
    realizationError prediction prediction.predictedUtility = 0 := by
  simp [realizationError]


theorem shadow_non_actuation (prediction : ShadowPrediction) :
    prediction.shadowActuationCount = 0 := by
  rfl


def boundedPortfolioAdjustment (bound reliability bias : ℚ) : ℚ :=
  max (-bound) (min bound (reliability * bias))


theorem boundedPortfolioAdjustment_le
    (bound reliability bias : ℚ) :
    boundedPortfolioAdjustment bound reliability bias ≤ bound := by
  simp [boundedPortfolioAdjustment]


theorem neg_bound_le_boundedPortfolioAdjustment
    (bound reliability bias : ℚ) :
    -bound ≤ boundedPortfolioAdjustment bound reliability bias := by
  simp [boundedPortfolioAdjustment]


structure PortfolioSelection where
  liveAdapterCount : ℕ
  oneLiveAdapter : liveAdapterCount ≤ 1
  shadowActuationCount : ℕ := 0


theorem oneLiveAdapter (selection : PortfolioSelection) :
    selection.liveAdapterCount = 0 ∨ selection.liveAdapterCount = 1 := by
  omega


theorem portfolio_shadow_non_actuation (selection : PortfolioSelection) :
    selection.shadowActuationCount = 0 := by
  rfl


structure PortfolioHistory where
  liveCycles : ℕ
  shadowProjections : ℕ
  resolvedPredictions : ℕ
  resolutionBound : resolvedPredictions ≤ shadowProjections


def appendLiveCycle
    (history : PortfolioHistory) (newShadowProjections : ℕ)
    (resolvedNow : Bool) : PortfolioHistory where
  liveCycles := history.liveCycles + 1
  shadowProjections := history.shadowProjections + newShadowProjections
  resolvedPredictions := history.resolvedPredictions + if resolvedNow then 1 else 0
  resolutionBound := by
    by_cases h : resolvedNow
    · simp [h]
      omega
    · simp [h]
      omega


theorem appendLiveCycle_live_strict
    (history : PortfolioHistory) (newShadowProjections : ℕ) (resolvedNow : Bool) :
    history.liveCycles <
      (appendLiveCycle history newShadowProjections resolvedNow).liveCycles := by
  simp [appendLiveCycle]

end OpenHorizon
end KUOS
