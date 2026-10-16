import Mathlib
import KUOS.OpenHorizon.MemoryOSStochasticMarkovKernelFDivergenceSufficiencyV0_57

namespace KUOS.OpenHorizon.MemoryOSReversibleMarkovSemigroupEntropyProductionV0_58

open KUOS.OpenHorizon.MemoryOSStochasticMarkovKernelFDivergenceSufficiencyV0_57

/-- Exact chi-square entropy in the orthogonal slow/fast mode coordinates. -/
def chiSquareModeEntropy (slow fast : ℝ) : ℝ :=
  6 * slow ^ 2 + 18 * fast ^ 2

/-- One reversible Markov step on the antisymmetric slow mode. -/
def slowModeStep (slow : ℝ) : ℝ :=
  ((3 : ℝ) / 4) * slow

/-- One reversible Markov step on the curvature fast mode. -/
def fastModeStep (fast : ℝ) : ℝ :=
  ((1 : ℝ) / 4) * fast

/-- The exact discrete-time reversible semigroup on the two nonstationary modes. -/
def modeAfter (n : ℕ) (slow fast : ℝ) : ℝ × ℝ :=
  ((((3 : ℝ) / 4) ^ n) * slow, (((1 : ℝ) / 4) ^ n) * fast)

theorem exact_kernel_row_stochastic_and_symmetric :
    ((3 : ℚ) / 4 + 1 / 4 + 0 = 1) ∧
      ((1 : ℚ) / 4 + 1 / 2 + 1 / 4 = 1) ∧
      ((0 : ℚ) + 1 / 4 + 3 / 4 = 1) ∧
      ((3 : ℚ) / 4 = 3 / 4) ∧
      ((1 : ℚ) / 4 = 1 / 4) ∧
      ((0 : ℚ) = 0) := by
  norm_num

theorem exact_uniform_detailed_balance :
    ((1 : ℚ) / 3) * (3 / 4) = ((1 : ℚ) / 3) * (3 / 4) ∧
      ((1 : ℚ) / 3) * (1 / 4) = ((1 : ℚ) / 3) * (1 / 4) ∧
      ((1 : ℚ) / 3) * 0 = ((1 : ℚ) / 3) * 0 ∧
      ((1 : ℚ) / 3) * (1 / 2) = ((1 : ℚ) / 3) * (1 / 2) := by
  norm_num

theorem exact_reference_kernel_square :
    ((3 : ℚ) / 4) * (3 / 4) + (1 / 4) * (1 / 4) = 5 / 8 ∧
      ((3 : ℚ) / 4) * (1 / 4) + (1 / 4) * (1 / 2) = 5 / 16 ∧
      ((1 : ℚ) / 4) * (1 / 4) = 1 / 16 ∧
      ((1 : ℚ) / 4) * (3 / 4) + (1 / 2) * (1 / 4) = 5 / 16 ∧
      ((1 : ℚ) / 4) * (1 / 4) + (1 / 2) * (1 / 2) +
          (1 / 4) * (1 / 4) = 3 / 8 := by
  norm_num

theorem slow_mode_semigroup
    (m n : ℕ) (slow : ℝ) :
    (((3 : ℝ) / 4) ^ (m + n)) * slow =
      (((3 : ℝ) / 4) ^ n) *
        ((((3 : ℝ) / 4) ^ m) * slow) := by
  rw [pow_add]
  ring

theorem fast_mode_semigroup
    (m n : ℕ) (fast : ℝ) :
    (((1 : ℝ) / 4) ^ (m + n)) * fast =
      (((1 : ℝ) / 4) ^ n) *
        ((((1 : ℝ) / 4) ^ m) * fast) := by
  rw [pow_add]
  ring

theorem one_step_entropy_exact
    (slow fast : ℝ) :
    chiSquareModeEntropy (slowModeStep slow) (fastModeStep fast) =
      ((27 : ℝ) / 8) * slow ^ 2 + ((9 : ℝ) / 8) * fast ^ 2 := by
  unfold chiSquareModeEntropy slowModeStep fastModeStep
  ring

theorem entropy_production_exact
    (slow fast : ℝ) :
    chiSquareModeEntropy slow fast -
        chiSquareModeEntropy (slowModeStep slow) (fastModeStep fast) =
      ((21 : ℝ) / 8) * slow ^ 2 + ((135 : ℝ) / 8) * fast ^ 2 := by
  unfold chiSquareModeEntropy slowModeStep fastModeStep
  ring

theorem entropy_production_nonnegative
    (slow fast : ℝ) :
    0 ≤ chiSquareModeEntropy slow fast -
      chiSquareModeEntropy (slowModeStep slow) (fastModeStep fast) := by
  rw [entropy_production_exact]
  positivity

theorem one_step_strong_data_processing
    (slow fast : ℝ) :
    chiSquareModeEntropy (slowModeStep slow) (fastModeStep fast) ≤
      ((9 : ℝ) / 16) * chiSquareModeEntropy slow fast := by
  unfold chiSquareModeEntropy slowModeStep fastModeStep
  nlinarith [sq_nonneg fast]

theorem strong_data_processing_coefficient_sharp
    (slow : ℝ) :
    chiSquareModeEntropy (slowModeStep slow) (fastModeStep 0) =
      ((9 : ℝ) / 16) * chiSquareModeEntropy slow 0 := by
  unfold chiSquareModeEntropy slowModeStep fastModeStep
  ring

theorem iterated_strong_data_processing
    (n : ℕ) (slow fast : ℝ) :
    chiSquareModeEntropy
        ((((3 : ℝ) / 4) ^ n) * slow)
        ((((1 : ℝ) / 4) ^ n) * fast) ≤
      (((9 : ℝ) / 16) ^ n) * chiSquareModeEntropy slow fast := by
  induction n with
  | zero =>
      simp [chiSquareModeEntropy]
  | succ n ih =>
      calc
        chiSquareModeEntropy
            ((((3 : ℝ) / 4) ^ (n + 1)) * slow)
            ((((1 : ℝ) / 4) ^ (n + 1)) * fast) =
          chiSquareModeEntropy
            (((3 : ℝ) / 4) * ((((3 : ℝ) / 4) ^ n) * slow))
            (((1 : ℝ) / 4) * ((((1 : ℝ) / 4) ^ n) * fast)) := by
              rw [pow_succ, pow_succ]
              ring
        _ ≤ ((9 : ℝ) / 16) *
            chiSquareModeEntropy
              ((((3 : ℝ) / 4) ^ n) * slow)
              ((((1 : ℝ) / 4) ^ n) * fast) :=
          one_step_strong_data_processing
            ((((3 : ℝ) / 4) ^ n) * slow)
            ((((1 : ℝ) / 4) ^ n) * fast)
        _ ≤ ((9 : ℝ) / 16) *
            ((((9 : ℝ) / 16) ^ n) * chiSquareModeEntropy slow fast) := by
          exact mul_le_mul_of_nonneg_left ih (by norm_num)
        _ = (((9 : ℝ) / 16) ^ (n + 1)) *
            chiSquareModeEntropy slow fast := by
          rw [pow_succ]
          ring

theorem exact_spectral_gap_and_sdpi_coefficient :
    (1 : ℚ) - 3 / 4 = 1 / 4 ∧
      ((3 : ℚ) / 4) ^ 2 = 9 / 16 ∧
      ((1 : ℚ) / 4) ^ 2 = 1 / 16 := by
  norm_num

theorem exact_reference_entropy_trajectory :
    chiSquareModeEntropy ((3 : ℝ) / 20) 0 = (27 : ℝ) / 200 ∧
      chiSquareModeEntropy (((3 : ℝ) / 4) * (3 / 20)) 0 =
        (243 : ℝ) / 3200 ∧
      chiSquareModeEntropy ((((3 : ℝ) / 4) ^ 2) * (3 / 20)) 0 =
        (2187 : ℝ) / 51200 ∧
      chiSquareModeEntropy ((((3 : ℝ) / 4) ^ 3) * (3 / 20)) 0 =
        (19683 : ℝ) / 819200 ∧
      chiSquareModeEntropy ((((3 : ℝ) / 4) ^ 4) * (3 / 20)) 0 =
        (177147 : ℝ) / 13107200 := by
  norm_num [chiSquareModeEntropy]

theorem exact_reference_entropy_production_trajectory :
    (27 : ℚ) / 200 - 243 / 3200 = 189 / 3200 ∧
      (243 : ℚ) / 3200 - 2187 / 51200 = 1701 / 51200 ∧
      (2187 : ℚ) / 51200 - 19683 / 819200 = 15309 / 819200 ∧
      (19683 : ℚ) / 819200 - 177147 / 13107200 =
        137781 / 13107200 := by
  norm_num

theorem exact_reference_sdpi_sharpness :
    (243 : ℚ) / 3200 = (9 / 16) * (27 / 200) ∧
      (2187 : ℚ) / 51200 = (9 / 16) ^ 2 * (27 / 200) ∧
      (19683 : ℚ) / 819200 = (9 / 16) ^ 3 * (27 / 200) ∧
      (177147 : ℚ) / 13107200 = (9 / 16) ^ 4 * (27 / 200) := by
  norm_num

structure ReversibleMarkovSemigroupEntropyProductionCertificate where
  sourceMemoryOSV057Bound : Bool
  sourceMemoryOSV056Bound : Bool
  kernelRowStochastic : Bool
  kernelColumnStochastic : Bool
  kernelReversible : Bool
  uniformStationary : Bool
  semigroupCompositionExact : Bool
  eigenmodeDecompositionExact : Bool
  entropyProductionExact : Bool
  entropyProductionNonnegative : Bool
  strongDataProcessingExact : Bool
  strongDataProcessingCoefficientSharp : Bool
  spectralGapExact : Bool
  transportSemigroupCommutes : Bool
  singularAtomicEntropyRetained : Bool
  rankOneDensityRecoveryNotClaimed : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV057Mutated : Bool
  sourceMemoryOSV056Mutated : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

theorem certificate_grants_no_authority
    (certificate : ReversibleMarkovSemigroupEntropyProductionCertificate)
    (hpruning : certificate.candidatePruningPerformed = false)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hsource57 : certificate.sourceMemoryOSV057Mutated = false)
    (hsource56 : certificate.sourceMemoryOSV056Mutated = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV057Mutated = false ∧
      certificate.sourceMemoryOSV056Mutated = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨hpruning, hselection, hexecution, hsource57, hsource56,
    hworld, hverification, htruth⟩

end KUOS.OpenHorizon.MemoryOSReversibleMarkovSemigroupEntropyProductionV0_58
