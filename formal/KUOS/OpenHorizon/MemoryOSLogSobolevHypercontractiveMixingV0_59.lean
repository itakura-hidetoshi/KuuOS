import Mathlib
import KUOS.OpenHorizon.MemoryOSReversibleMarkovSemigroupEntropyProductionV0_58

namespace KUOS.OpenHorizon.MemoryOSLogSobolevHypercontractiveMixingV0_59

open KUOS.OpenHorizon.MemoryOSReversibleMarkovSemigroupEntropyProductionV0_58

def uniformLikelihoodKLEntropy (r₀ r₁ r₂ : ℝ) : ℝ :=
  (r₀ * Real.log r₀ + r₁ * Real.log r₁ + r₂ * Real.log r₂) / 3

def uniformLikelihoodChiSquare (r₀ r₁ r₂ : ℝ) : ℝ :=
  ((r₀ - 1) ^ 2 + (r₁ - 1) ^ 2 + (r₂ - 1) ^ 2) / 3

def modeLikelihoodEarly (slow fast : ℝ) : ℝ := 1 + 3 * (slow + fast)
def modeLikelihoodMiddle (_slow fast : ℝ) : ℝ := 1 - 6 * fast
def modeLikelihoodLate (slow fast : ℝ) : ℝ := 1 + 3 * (-slow + fast)

def dirichletModeEnergy (slow fast : ℝ) : ℝ :=
  ((3 : ℝ) / 2) * slow ^ 2 + ((27 : ℝ) / 2) * fast ^ 2

def centeredMeanSquare (slow fast : ℝ) : ℝ :=
  ((2 : ℝ) / 3) * slow ^ 2 + 2 * fast ^ 2

def centeredMeanFourth (slow fast : ℝ) : ℝ :=
  ((2 : ℝ) / 3) * (slow ^ 2 + 3 * fast ^ 2) ^ 2

def twoStepEarly (slow fast : ℝ) : ℝ := (9 * slow + fast) / 16
def twoStepMiddle (_slow fast : ℝ) : ℝ := -fast / 8
def twoStepLate (slow fast : ℝ) : ℝ := (-9 * slow + fast) / 16

theorem x_mul_log_le_x_mul_sub_one
    (x : ℝ) (hx : 0 < x) :
    x * Real.log x ≤ x * (x - 1) := by
  exact mul_le_mul_of_nonneg_left
    (Real.log_le_sub_one_of_pos hx) hx.le

theorem uniform_kl_le_chi_square
    (r₀ r₁ r₂ : ℝ)
    (h₀ : 0 < r₀) (h₁ : 0 < r₁) (h₂ : 0 < r₂)
    (hmass : r₀ + r₁ + r₂ = 3) :
    uniformLikelihoodKLEntropy r₀ r₁ r₂ ≤
      uniformLikelihoodChiSquare r₀ r₁ r₂ := by
  have hlog₀ := x_mul_log_le_x_mul_sub_one r₀ h₀
  have hlog₁ := x_mul_log_le_x_mul_sub_one r₁ h₁
  have hlog₂ := x_mul_log_le_x_mul_sub_one r₂ h₂
  unfold uniformLikelihoodKLEntropy uniformLikelihoodChiSquare
  nlinarith

theorem mode_likelihood_mass_exact (slow fast : ℝ) :
    modeLikelihoodEarly slow fast +
        modeLikelihoodMiddle slow fast +
        modeLikelihoodLate slow fast = 3 := by
  ring

theorem mode_uniform_chi_square_exact (slow fast : ℝ) :
    uniformLikelihoodChiSquare
        (modeLikelihoodEarly slow fast)
        (modeLikelihoodMiddle slow fast)
        (modeLikelihoodLate slow fast) =
      chiSquareModeEntropy slow fast := by
  unfold uniformLikelihoodChiSquare
    modeLikelihoodEarly modeLikelihoodMiddle modeLikelihoodLate
    chiSquareModeEntropy
  ring

theorem mode_chi_square_le_four_dirichlet (slow fast : ℝ) :
    chiSquareModeEntropy slow fast ≤ 4 * dirichletModeEnergy slow fast := by
  unfold chiSquareModeEntropy dirichletModeEnergy
  nlinarith [sq_nonneg fast]

theorem mode_log_sobolev_bound
    (slow fast : ℝ)
    (hearly : 0 < modeLikelihoodEarly slow fast)
    (hmiddle : 0 < modeLikelihoodMiddle slow fast)
    (hlate : 0 < modeLikelihoodLate slow fast) :
    uniformLikelihoodKLEntropy
        (modeLikelihoodEarly slow fast)
        (modeLikelihoodMiddle slow fast)
        (modeLikelihoodLate slow fast) ≤
      4 * dirichletModeEnergy slow fast := by
  have hkl := uniform_kl_le_chi_square
    (modeLikelihoodEarly slow fast)
    (modeLikelihoodMiddle slow fast)
    (modeLikelihoodLate slow fast)
    hearly hmiddle hlate
    (mode_likelihood_mass_exact slow fast)
  rw [mode_uniform_chi_square_exact] at hkl
  exact hkl.trans (mode_chi_square_le_four_dirichlet slow fast)

theorem one_step_l2_to_l4_hypercontractive (slow fast : ℝ) :
    centeredMeanFourth (((3 : ℝ) / 4) * slow) (((1 : ℝ) / 4) * fast) ≤
      centeredMeanSquare slow fast ^ 2 := by
  unfold centeredMeanFourth centeredMeanSquare
  nlinarith [
    sq_nonneg (slow ^ 2),
    sq_nonneg (slow * fast),
    sq_nonneg (fast ^ 2)
  ]

theorem two_step_early_l2_to_linf (slow fast : ℝ) :
    twoStepEarly slow fast ^ 2 ≤ centeredMeanSquare slow fast := by
  unfold twoStepEarly centeredMeanSquare
  nlinarith [
    sq_nonneg (269 * slow - 27 * fast),
    sq_nonneg fast
  ]

theorem two_step_middle_l2_to_linf (slow fast : ℝ) :
    twoStepMiddle slow fast ^ 2 ≤ centeredMeanSquare slow fast := by
  unfold twoStepMiddle centeredMeanSquare
  nlinarith [sq_nonneg slow, sq_nonneg fast]

theorem two_step_late_l2_to_linf (slow fast : ℝ) :
    twoStepLate slow fast ^ 2 ≤ centeredMeanSquare slow fast := by
  unfold twoStepLate centeredMeanSquare
  nlinarith [
    sq_nonneg (269 * slow + 27 * fast),
    sq_nonneg fast
  ]

theorem two_step_l2_to_linf_hypercontractive (slow fast : ℝ) :
    twoStepEarly slow fast ^ 2 ≤ centeredMeanSquare slow fast ∧
      twoStepMiddle slow fast ^ 2 ≤ centeredMeanSquare slow fast ∧
      twoStepLate slow fast ^ 2 ≤ centeredMeanSquare slow fast := by
  exact ⟨
    two_step_early_l2_to_linf slow fast,
    two_step_middle_l2_to_linf slow fast,
    two_step_late_l2_to_linf slow fast
  ⟩

theorem three_term_cauchy_absolute
    (x y z : ℝ) :
    (|x| + |y| + |z|) ^ 2 ≤
      3 * (x ^ 2 + y ^ 2 + z ^ 2) := by
  have h :
      (|x| - |y|) ^ 2 + (|y| - |z|) ^ 2 + (|z| - |x|) ^ 2 ≥ 0 := by
    positivity
  nlinarith [sq_abs x, sq_abs y, sq_abs z]

theorem total_variation_squared_le_chi_square_quarter
    (x y z : ℝ) :
    ((|x| + |y| + |z|) / 2) ^ 2 ≤
      (3 * (x ^ 2 + y ^ 2 + z ^ 2)) / 4 := by
  have h := three_term_cauchy_absolute x y z
  nlinarith

theorem three_probability_chi_square_le_two
    (p₀ p₁ p₂ : ℝ)
    (hp₀ : 0 ≤ p₀) (hp₁ : 0 ≤ p₁) (hp₂ : 0 ≤ p₂)
    (hmass : p₀ + p₁ + p₂ = 1) :
    3 * ((p₀ - (1 : ℝ) / 3) ^ 2 +
      (p₁ - (1 : ℝ) / 3) ^ 2 +
      (p₂ - (1 : ℝ) / 3) ^ 2) ≤ 2 := by
  nlinarith [
    mul_nonneg hp₀ hp₁,
    mul_nonneg hp₀ hp₂,
    mul_nonneg hp₁ hp₂
  ]

theorem exact_quarter_mixing_time_bound :
    ((1 : ℚ) / 2) * (((9 : ℚ) / 16) ^ 4) ≤ ((1 : ℚ) / 4) ^ 2 ∧
      ((1 : ℚ) / 2) * (((9 : ℚ) / 16) ^ 3) > ((1 : ℚ) / 4) ^ 2 := by
  norm_num

theorem exact_eighth_mixing_time_bound :
    ((1 : ℚ) / 2) * (((9 : ℚ) / 16) ^ 7) ≤ ((1 : ℚ) / 8) ^ 2 ∧
      ((1 : ℚ) / 2) * (((9 : ℚ) / 16) ^ 6) > ((1 : ℚ) / 8) ^ 2 := by
  norm_num

theorem exact_reference_twentieth_mixing_time :
    ((3 : ℚ) / 20) * (((3 : ℚ) / 4) ^ 4) ≤ (1 : ℚ) / 20 ∧
      ((3 : ℚ) / 20) * (((3 : ℚ) / 4) ^ 3) > (1 : ℚ) / 20 := by
  norm_num

theorem full_rank_log_sobolev_transport_commutes
    (sourceKL sourceDirichlet targetKL targetDirichlet : ℝ)
    (hKL : targetKL = sourceKL)
    (hDirichlet : targetDirichlet = sourceDirichlet)
    (hsource : sourceKL ≤ 4 * sourceDirichlet) :
    targetKL ≤ 4 * targetDirichlet := by
  linarith

structure LogSobolevHypercontractiveMixingCertificate where
  sourceMemoryOSV058Bound : Bool
  sourceMemoryOSV057Bound : Bool
  logarithmicEntropyBridgeExact : Bool
  logSobolevConstantFourExact : Bool
  oneStepL2ToL4Hypercontractive : Bool
  twoStepL2ToLInfinityHypercontractive : Bool
  totalVariationMixingBoundExact : Bool
  fullRankTransportCommutes : Bool
  singularAtomicMixingLedgerRetained : Bool
  rankOneDensityRecoveryNotClaimed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

theorem certificate_grants_no_authority
    (certificate : LogSobolevHypercontractiveMixingCertificate)
    (hpruning : certificate.candidatePruningPerformed = false)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hpruning, hselection, hexecution, hworld, hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSLogSobolevHypercontractiveMixingV0_59
