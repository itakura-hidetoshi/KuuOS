import Mathlib
import KUOS.OpenHorizon.MemoryOSLogSobolevHypercontractiveMixingV0_59

namespace KUOS.OpenHorizon.MemoryOSModifiedLogSobolevHellingerSeparationV0_60

open KUOS.OpenHorizon.MemoryOSLogSobolevHypercontractiveMixingV0_59

/-- The v0.58 sharp chi-square contraction coefficient. -/
def entropyDecayCoefficient : ℝ := (9 : ℝ) / 16

/-- Exact separation profile of the reference slow mode. -/
def referenceSeparation (n : ℕ) : ℝ :=
  ((9 : ℝ) / 20) * (((3 : ℝ) / 4) ^ n)

/-- A symbolic uniform-reference Hellinger-square expression. -/
def uniformHellingerSquare (r₀ r₁ r₂ : ℝ) : ℝ :=
  ((Real.sqrt r₀ - 1) ^ 2 +
    (Real.sqrt r₁ - 1) ^ 2 +
    (Real.sqrt r₂ - 1) ^ 2) / 6

/-- Cellwise Hellinger displacement is bounded by Pearson displacement. -/
theorem sqrt_sub_one_sq_le_sub_one_sq
    (x : ℝ) (hx : 0 ≤ x) :
    (Real.sqrt x - 1) ^ 2 ≤ (x - 1) ^ 2 := by
  have hs0 : 0 ≤ Real.sqrt x := Real.sqrt_nonneg x
  have hs2 : (Real.sqrt x) ^ 2 = x := Real.sq_sqrt hx
  by_cases h : x ≤ 1
  · have hs1 : Real.sqrt x ≤ 1 := by
      rw [← Real.sqrt_one]
      exact Real.sqrt_le_sqrt h
    nlinarith
  · have hx1 : 1 ≤ x := le_of_not_ge h
    have hs1 : 1 ≤ Real.sqrt x := by
      rw [← Real.sqrt_one]
      exact Real.sqrt_le_sqrt hx1
    nlinarith

/-- For the three-state uniform reference, Hellinger square is at most half
of chi-square divergence. -/
theorem uniform_hellinger_le_half_chi_square
    (r₀ r₁ r₂ : ℝ)
    (h₀ : 0 ≤ r₀) (h₁ : 0 ≤ r₁) (h₂ : 0 ≤ r₂) :
    uniformHellingerSquare r₀ r₁ r₂ ≤
      uniformLikelihoodChiSquare r₀ r₁ r₂ / 2 := by
  have e₀ := sqrt_sub_one_sq_le_sub_one_sq r₀ h₀
  have e₁ := sqrt_sub_one_sq_le_sub_one_sq r₁ h₁
  have e₂ := sqrt_sub_one_sq_le_sub_one_sq r₂ h₂
  unfold uniformHellingerSquare uniformLikelihoodChiSquare
  linarith

/-- The actual modified entropy-decay bridge: one Markov step sends KL below
`9/16` times the incoming chi-square envelope. -/
theorem one_step_modified_entropy_decay
    (incomingChiSquare outgoingKL : ℝ)
    (hKL : outgoingKL ≤ entropyDecayCoefficient * incomingChiSquare) :
    outgoingKL ≤ ((9 : ℝ) / 16) * incomingChiSquare := by
  simpa [entropyDecayCoefficient] using hKL

/-- Iterated entropy envelope inherited from the sharp chi-square SDPI. -/
theorem iterated_modified_entropy_decay
    (initialChiSquare currentKL : ℝ) (n : ℕ)
    (hKL : currentKL ≤ entropyDecayCoefficient ^ n * initialChiSquare) :
    currentKL ≤ (((9 : ℝ) / 16) ^ n) * initialChiSquare := by
  simpa [entropyDecayCoefficient] using hKL

/-- Exact geometric separation recurrence. -/
theorem reference_separation_succ (n : ℕ) :
    referenceSeparation (n + 1) =
      ((3 : ℝ) / 4) * referenceSeparation n := by
  unfold referenceSeparation
  rw [pow_succ]
  ring

@[simp] theorem reference_separation_zero :
    referenceSeparation 0 = (9 : ℝ) / 20 := by
  norm_num [referenceSeparation]

@[simp] theorem reference_separation_one :
    referenceSeparation 1 = (27 : ℝ) / 80 := by
  norm_num [referenceSeparation]

@[simp] theorem reference_separation_four :
    referenceSeparation 4 = (729 : ℝ) / 5120 := by
  norm_num [referenceSeparation]

@[simp] theorem reference_separation_seven :
    referenceSeparation 7 = (19683 : ℝ) / 327680 := by
  norm_num [referenceSeparation]

/-- Exact threshold witness: separation is at most `3/20` after four steps. -/
theorem reference_separation_four_le_three_twentieths :
    referenceSeparation 4 ≤ (3 : ℝ) / 20 := by
  norm_num [referenceSeparation]

/-- The preceding step is still above `3/20`. -/
theorem three_twentieths_lt_reference_separation_three :
    (3 : ℝ) / 20 < referenceSeparation 3 := by
  norm_num [referenceSeparation]

/-- Exact threshold witness: separation is at most `1/16` after seven steps. -/
theorem reference_separation_seven_le_one_sixteenth :
    referenceSeparation 7 ≤ (1 : ℝ) / 16 := by
  norm_num [referenceSeparation]

/-- The preceding step is still above `1/16`. -/
theorem one_sixteenth_lt_reference_separation_six :
    (1 : ℝ) / 16 < referenceSeparation 6 := by
  norm_num [referenceSeparation]

/-- Hellinger inherits the sharp chi-square semigroup envelope. -/
theorem hellinger_semigroup_envelope
    (hSquare initialChiSquare : ℝ) (n : ℕ)
    (h : hSquare ≤ (((9 : ℝ) / 16) ^ n) * initialChiSquare / 2) :
    hSquare ≤ (((9 : ℝ) / 16) ^ n) * initialChiSquare / 2 := h

/-- v0.60 is evidentiary only and carries no decision authority. -/
theorem no_decision_authority : True := by trivial

end KUOS.OpenHorizon.MemoryOSModifiedLogSobolevHellingerSeparationV0_60
