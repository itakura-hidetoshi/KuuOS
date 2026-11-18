import Mathlib
import KuuOSFormal.WaGridRoundingV0_20

/-!
# Exact rational adjacent-float midpoint certificates (v0.20 candidate B)

The Python observation layer can interpret a finite float result, its finite
neighbors (nextafter), and the represented input operands as exact rationals.
When its exact rational operation result lies between the two neighboring
midpoints, these *observed* midpoint relations imply a half-quantum error
bound. No IEEE-754 operational semantics, completeness of adjacent floats,
ties-to-even, overflow or subnormal semantics are proved here.

The local checker must supply all hypotheses: neither this theorem nor
successful examples assert that arbitrary Python float operations satisfy
them. The original Wa Lean model and historical v0.19 theorem are unchanged.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS
namespace DecisionOS
namespace WaNeighborMidpointV0_20

open WaRationalBridgeV0_19 WaGridRoundingV0_20

/-- A verifiable exact-rational adjacent-neighbor midpoint certificate.
    No global property of float or nextafter is assumed or concluded. -/
theorem observed_neighbor_midpoint_error
    (exact observed previous next quantum : ℚ)
    (hLowerMidpoint : (previous + observed) / 2 ≤ exact)
    (hUpperMidpoint : exact ≤ (observed + next) / 2)
    (hLowerGap : observed - previous ≤ quantum)
    (hUpperGap : next - observed ≤ quantum) :
    |observed - exact| ≤ quantum / 2 := by
  apply abs_le.mpr
  constructor <;> linarith

/-- Two independently supplied midpoint certificates imply the Wa
    real-score error bound through the previously proven v0.19 bridge.
    This is *conditional* refinement of rational observations, not a
    Python-interpreter semantics theorem. -/
theorem wa_observed_neighbor_two_stage_real_error
    (beta weighted weakest alert rel out : ℚ)
    (relPrev relNext outPrev outNext relQuantum outQuantum : ℚ)
    (hAlertNonnegative : 0 ≤ alert)
    (hAlertAtMostOne : alert ≤ 1)
    (hRelLow :
      (relPrev + rel) / 2 ≤ (1 - beta) * weighted + beta * weakest)
    (hRelHigh :
      (1 - beta) * weighted + beta * weakest ≤ (rel + relNext) / 2)
    (hRelGapLow : rel - relPrev ≤ relQuantum)
    (hRelGapHigh : relNext - rel ≤ relQuantum)
    (hOutLow : (outPrev + out) / 2 ≤ rel * (1 - alert))
    (hOutHigh : rel * (1 - alert) ≤ (out + outNext) / 2)
    (hOutGapLow : out - outPrev ≤ outQuantum)
    (hOutGapHigh : outNext - out ≤ outQuantum) :
    |(out : ℝ) -
      realIdeal (beta : ℝ) (weighted : ℝ) (weakest : ℝ) (alert : ℝ)| ≤
      (((outQuantum + relQuantum) / 2 : ℚ) : ℝ) := by
  have hRelError :
      |rel - ((1 - beta) * weighted + beta * weakest)| ≤
        relQuantum / 2 :=
    observed_neighbor_midpoint_error _ _ _ _ _
      hRelLow hRelHigh hRelGapLow hRelGapHigh
  have hOutError :
      |out - rel * (1 - alert)| ≤ outQuantum / 2 :=
    observed_neighbor_midpoint_error _ _ _ _ _
      hOutLow hOutHigh hOutGapLow hOutGapHigh
  have hRelNonnegative : 0 ≤ relQuantum / 2 := by
    have hl : 0 ≤ relQuantum := by
      have hNonneg := abs_nonneg
        (rel - ((1 - beta) * weighted + beta * weakest))
      linarith [hRelError]
    exact div_nonneg hl (by norm_num)
  have hScore := rational_two_stage_score_error
    beta weighted weakest alert rel out
    (relQuantum / 2) (outQuantum / 2)
    hAlertNonnegative hAlertAtMostOne hRelError hOutError hRelNonnegative
  have hCert :
      |out - rationalIdeal beta weighted weakest alert| ≤
        (outQuantum + relQuantum) / 2 := by
    linarith
  exact certified_rational_error_is_real_error
    beta weighted weakest alert out
    ((outQuantum + relQuantum) / 2) hCert

#print axioms observed_neighbor_midpoint_error
#print axioms wa_observed_neighbor_two_stage_real_error

end WaNeighborMidpointV0_20
end DecisionOS
end KUOS
