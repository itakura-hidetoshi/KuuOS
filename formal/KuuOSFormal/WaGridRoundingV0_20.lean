import Mathlib
import KuuOSFormal.WaRationalBridgeV0_19

/-!
# Wa rational uniform-grid rounding bridge (v0.20 candidate A)

A constructive exact-rational *grid* rounding operation is defined below.
For every positive rational quantum, rounding to the selected integer grid
has absolute error at most half a quantum. The proof is valid for rational
arithmetic, including negative inputs.

This is NOT the operational semantics of Python float or IEEE-754 binary64:
the grid is unbounded, its quantum is supplied externally, and midpoint
ties round toward positive infinity rather than ties-to-even. In particular,
a Python result cannot be identified with gridRound without an additional
equality/rounding certificate. Overflow, underflow, subnormal transitions,
binade changes, signed zero and NaN are not modeled.

The conditional two-operation Wa theorem uses *explicit* grid equality
witnesses. The original DecisionOS Wa kernel and v0.19 source are unchanged.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS
namespace DecisionOS
namespace WaGridRoundingV0_20

open WaRationalBridgeV0_19

/-- Quantize an exact rational to an unbounded uniform rational grid.
    The tie convention is half-up, not IEEE-754 ties-to-even. -/
def gridRound (x quantum : ℚ) : ℚ :=
  quantum * (((x / quantum + (1 / 2 : ℚ)).floor : ℤ) : ℚ)

/-- The exact rational grid constructor is within half a positive quantum. -/
theorem gridRound_half_quantum
    (x quantum : ℚ) (hquantum : 0 < quantum) :
    |gridRound x quantum - x| ≤ quantum / 2 := by
  let scaled : ℚ := x / quantum + 1 / 2
  let k : ℤ := scaled.floor
  have hfloor : (k : ℚ) ≤ scaled := by
    simpa [k] using Rat.floor_le scaled
  have hnext : scaled < (k : ℚ) + 1 := by
    simpa [k, Int.cast_add, Int.cast_one] using Rat.lt_floor_add_one scaled
  have hpositive : 0 ≤ quantum := le_of_lt hquantum
  have hlow := mul_le_mul_of_nonneg_left hfloor hpositive
  have hhigh := mul_lt_mul_of_pos_left hnext hquantum
  have hnotzero : quantum ≠ 0 := ne_of_gt hquantum
  have hcancel : (x / quantum) * quantum = x := by
    field_simp
  have hleft : -(quantum / 2) ≤ quantum * (k : ℚ) - x := by
    dsimp [scaled] at hhigh
    nlinarith [hhigh, hcancel]
  have hright : quantum * (k : ℚ) - x ≤ quantum / 2 := by
    dsimp [scaled] at hlow
    nlinarith [hlow, hcancel]
  change |quantum * (k : ℚ) - x| ≤ quantum / 2
  exact abs_le.mpr ⟨hleft, hright⟩

/-- One *modelled* rounded addition, not the Python interpreter operation. -/
theorem grid_add_error
    (x y quantum : ℚ) (hquantum : 0 < quantum) :
    |gridRound (x + y) quantum - (x + y)| ≤ quantum / 2 := by
  exact gridRound_half_quantum (x + y) quantum hquantum

/-- One *modelled* rounded multiplication, not the Python interpreter operation. -/
theorem grid_mul_error
    (x y quantum : ℚ) (hquantum : 0 < quantum) :
    |gridRound (x * y) quantum - (x * y)| ≤ quantum / 2 := by
  exact gridRound_half_quantum (x * y) quantum hquantum

/-- The v0.19 two-stage Wa inequality expressed on exact rationals.
    The errors are assumptions about the operands actually supplied. -/
theorem rational_two_stage_score_error
    (beta weighted weakest alert relational observed epsRel epsOut : ℚ)
    (hAlertNonnegative : 0 ≤ alert)
    (hAlertAtMostOne : alert ≤ 1)
    (hRel :
      |relational - ((1 - beta) * weighted + beta * weakest)| ≤ epsRel)
    (hOut : |observed - relational * (1 - alert)| ≤ epsOut)
    (hRelBudget : 0 ≤ epsRel) :
    |observed - rationalIdeal beta weighted weakest alert| ≤ epsOut + epsRel := by
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
      observed - rationalIdeal beta weighted weakest alert =
        (observed - relational * (1 - alert)) +
          (relational - ((1 - beta) * weighted + beta * weakest)) *
            (1 - alert) := by
    unfold rationalIdeal
    ring
  calc
    |observed - rationalIdeal beta weighted weakest alert| =
      |(observed - relational * (1 - alert)) +
        (relational - ((1 - beta) * weighted + beta * weakest)) *
          (1 - alert)| := by rw [hIdentity]
    _ ≤ |observed - relational * (1 - alert)| +
        |(relational - ((1 - beta) * weighted + beta * weakest)) *
          (1 - alert)| := abs_add_le _ _
    _ ≤ epsOut + epsRel := add_le_add hOut hSecond

/-- Two witnessed grid-round steps have an explicit combined Wa error.
    This theorem does not establish that any Python float output is a gridRound. -/
theorem wa_two_grid_rounds_error
    (beta weighted weakest alert relational observed relQuantum outQuantum : ℚ)
    (hAlertNonnegative : 0 ≤ alert)
    (hAlertAtMostOne : alert ≤ 1)
    (hRelQuantum : 0 < relQuantum)
    (hOutQuantum : 0 < outQuantum)
    (hRel : relational =
      gridRound ((1 - beta) * weighted + beta * weakest) relQuantum)
    (hOut : observed = gridRound (relational * (1 - alert)) outQuantum) :
    |observed - rationalIdeal beta weighted weakest alert| ≤
      outQuantum / 2 + relQuantum / 2 := by
  have hRelError :
      |relational - ((1 - beta) * weighted + beta * weakest)| ≤
        relQuantum / 2 := by
    rw [hRel]
    exact gridRound_half_quantum _ _ hRelQuantum
  have hOutError :
      |observed - relational * (1 - alert)| ≤ outQuantum / 2 := by
    rw [hOut]
    exact gridRound_half_quantum _ _ hOutQuantum
  have hRelBudget : 0 ≤ relQuantum / 2 := by
    positivity
  exact rational_two_stage_score_error
    beta weighted weakest alert relational observed
    (relQuantum / 2) (outQuantum / 2)
    hAlertNonnegative hAlertAtMostOne hRelError hOutError hRelBudget

/-- The same conditional *grid* error estimate in the real Wa formula.
    The v0.19 rational-to-real bridge is reused, not re-proven. -/
theorem wa_two_grid_rounds_real_error
    (beta weighted weakest alert relational observed relQuantum outQuantum : ℚ)
    (hAlertNonnegative : 0 ≤ alert)
    (hAlertAtMostOne : alert ≤ 1)
    (hRelQuantum : 0 < relQuantum)
    (hOutQuantum : 0 < outQuantum)
    (hRel : relational =
      gridRound ((1 - beta) * weighted + beta * weakest) relQuantum)
    (hOut : observed = gridRound (relational * (1 - alert)) outQuantum) :
    |(observed : ℝ) -
      realIdeal (beta : ℝ) (weighted : ℝ) (weakest : ℝ) (alert : ℝ)| ≤
      (((outQuantum + relQuantum) / 2 : ℚ) : ℝ) := by
  have hq := wa_two_grid_rounds_error beta weighted weakest alert
    relational observed relQuantum outQuantum
    hAlertNonnegative hAlertAtMostOne
    hRelQuantum hOutQuantum hRel hOut
  have hcert :
      |observed - rationalIdeal beta weighted weakest alert| ≤
        (outQuantum + relQuantum) / 2 := by
    linarith
  exact certified_rational_error_is_real_error
    beta weighted weakest alert observed
    ((outQuantum + relQuantum) / 2) hcert

#print axioms gridRound_half_quantum
#print axioms grid_add_error
#print axioms grid_mul_error
#print axioms rational_two_stage_score_error
#print axioms wa_two_grid_rounds_error
#print axioms wa_two_grid_rounds_real_error

end WaGridRoundingV0_20
end DecisionOS
end KUOS
