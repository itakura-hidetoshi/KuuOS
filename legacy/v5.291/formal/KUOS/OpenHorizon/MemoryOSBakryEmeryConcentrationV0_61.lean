import Mathlib
import KUOS.OpenHorizon.MemoryOSModifiedLogSobolevHellingerSeparationV0_60

namespace KUOS.OpenHorizon.MemoryOSBakryEmeryConcentrationV0_61

open KUOS.OpenHorizon.MemoryOSLogSobolevHypercontractiveMixingV0_59
open KUOS.OpenHorizon.MemoryOSModifiedLogSobolevHellingerSeparationV0_60

def modeChiSquare (slow fast : ℝ) : ℝ :=
  6 * slow ^ 2 + 18 * fast ^ 2

def integratedGammaTwo (slow fast : ℝ) : ℝ :=
  ((3 : ℝ) / 8) * slow ^ 2 + ((81 : ℝ) / 8) * fast ^ 2

def likelihoodDeviationEarly (slow fast : ℝ) : ℝ :=
  3 * (slow + fast)

def likelihoodDeviationMiddle (_slow fast : ℝ) : ℝ :=
  -6 * fast

def likelihoodDeviationLate (slow fast : ℝ) : ℝ :=
  3 * (-slow + fast)

def threePointMeanSquare (x y z : ℝ) : ℝ :=
  (x ^ 2 + y ^ 2 + z ^ 2) / 3

def tailIndicator (threshold value : ℝ) : ℝ :=
  if threshold ≤ |value| then 1 else 0

def threePointTailMass (threshold x y z : ℝ) : ℝ :=
  (tailIndicator threshold x +
    tailIndicator threshold y +
    tailIndicator threshold z) / 3

def slowModeAt (slow : ℝ) : ℕ → ℝ
  | 0 => slow
  | n + 1 => ((3 : ℝ) / 4) * slowModeAt slow n

def fastModeAt (fast : ℝ) : ℕ → ℝ
  | 0 => fast
  | n + 1 => ((1 : ℝ) / 4) * fastModeAt fast n

def modeChiSquareAt (slow fast : ℝ) (n : ℕ) : ℝ :=
  modeChiSquare (slowModeAt slow n) (fastModeAt fast n)

def modeTailMassAt (threshold slow fast : ℝ) (n : ℕ) : ℝ :=
  threePointTailMass threshold
    (likelihoodDeviationEarly (slowModeAt slow n) (fastModeAt fast n))
    (likelihoodDeviationMiddle (slowModeAt slow n) (fastModeAt fast n))
    (likelihoodDeviationLate (slowModeAt slow n) (fastModeAt fast n))

def referenceLikelihoodAmplitude (n : ℕ) : ℚ :=
  ((9 : ℚ) / 20) * (((3 : ℚ) / 4) ^ n)

theorem mode_chi_square_source_exact (slow fast : ℝ) :
    modeChiSquare slow fast = chiSquareModeEntropy slow fast := by
  unfold modeChiSquare chiSquareModeEntropy
  ring

theorem mode_uniform_chi_square_exact_v061 (slow fast : ℝ) :
    uniformLikelihoodChiSquare
        (modeLikelihoodEarly slow fast)
        (modeLikelihoodMiddle slow fast)
        (modeLikelihoodLate slow fast) =
      modeChiSquare slow fast := by
  unfold uniformLikelihoodChiSquare
    modeLikelihoodEarly modeLikelihoodMiddle modeLikelihoodLate
    modeChiSquare
  ring

theorem integrated_gamma_two_nonnegative (slow fast : ℝ) :
    0 ≤ integratedGammaTwo slow fast := by
  unfold integratedGammaTwo
  positivity

theorem integrated_gamma_two_curvature (slow fast : ℝ) :
    ((1 : ℝ) / 4) * dirichletModeEnergy slow fast ≤
      integratedGammaTwo slow fast := by
  unfold integratedGammaTwo dirichletModeEnergy
  nlinarith [sq_nonneg fast]

theorem integrated_gamma_two_gap_exact (slow fast : ℝ) :
    integratedGammaTwo slow fast -
        ((1 : ℝ) / 4) * dirichletModeEnergy slow fast =
      ((27 : ℝ) / 4) * fast ^ 2 := by
  unfold integratedGammaTwo dirichletModeEnergy
  ring

theorem integrated_curvature_sharp_on_slow_mode (slow : ℝ) :
    integratedGammaTwo slow 0 =
      ((1 : ℝ) / 4) * dirichletModeEnergy slow 0 := by
  unfold integratedGammaTwo dirichletModeEnergy
  ring

theorem mode_poincare_inequality (slow fast : ℝ) :
    modeChiSquare slow fast ≤ 4 * dirichletModeEnergy slow fast := by
  unfold modeChiSquare dirichletModeEnergy
  nlinarith [sq_nonneg fast]

theorem mode_poincare_gap_exact (slow fast : ℝ) :
    4 * dirichletModeEnergy slow fast - modeChiSquare slow fast =
      36 * fast ^ 2 := by
  unfold modeChiSquare dirichletModeEnergy
  ring

theorem mode_poincare_sharp_on_slow_mode (slow : ℝ) :
    modeChiSquare slow 0 = 4 * dirichletModeEnergy slow 0 := by
  unfold modeChiSquare dirichletModeEnergy
  ring

theorem mode_dirichlet_le_four_gamma_two (slow fast : ℝ) :
    dirichletModeEnergy slow fast ≤ 4 * integratedGammaTwo slow fast := by
  have h := integrated_gamma_two_curvature slow fast
  nlinarith

theorem functional_inequality_hierarchy
    (slow fast : ℝ)
    (hearly : 0 < modeLikelihoodEarly slow fast)
    (hmiddle : 0 < modeLikelihoodMiddle slow fast)
    (hlate : 0 < modeLikelihoodLate slow fast) :
    uniformLikelihoodKLEntropy
        (modeLikelihoodEarly slow fast)
        (modeLikelihoodMiddle slow fast)
        (modeLikelihoodLate slow fast) ≤
      modeChiSquare slow fast ∧
    modeChiSquare slow fast ≤ 4 * dirichletModeEnergy slow fast ∧
    4 * dirichletModeEnergy slow fast ≤
      16 * integratedGammaTwo slow fast := by
  have hkl := uniform_kl_le_chi_square
    (modeLikelihoodEarly slow fast)
    (modeLikelihoodMiddle slow fast)
    (modeLikelihoodLate slow fast)
    hearly hmiddle hlate
    (mode_likelihood_mass_exact slow fast)
  rw [mode_uniform_chi_square_exact_v061] at hkl
  have hpoincare := mode_poincare_inequality slow fast
  have hcurvature := mode_dirichlet_le_four_gamma_two slow fast
  constructor
  · exact hkl
  constructor
  · exact hpoincare
  · nlinarith

theorem likelihood_deviation_mean_square_exact (slow fast : ℝ) :
    threePointMeanSquare
        (likelihoodDeviationEarly slow fast)
        (likelihoodDeviationMiddle slow fast)
        (likelihoodDeviationLate slow fast) =
      modeChiSquare slow fast := by
  unfold threePointMeanSquare likelihoodDeviationEarly
    likelihoodDeviationMiddle likelihoodDeviationLate modeChiSquare
  ring

theorem tail_indicator_square_bound
    (threshold value : ℝ)
    (hthreshold : 0 ≤ threshold) :
    tailIndicator threshold value * threshold ^ 2 ≤ value ^ 2 := by
  by_cases h : threshold ≤ |value|
  · simp [tailIndicator, h]
    nlinarith [sq_abs value, abs_nonneg value]
  · simp [tailIndicator, h]

theorem three_point_quadratic_concentration
    (threshold x y z : ℝ)
    (hthreshold : 0 ≤ threshold) :
    threePointTailMass threshold x y z * threshold ^ 2 ≤
      threePointMeanSquare x y z := by
  have hx := tail_indicator_square_bound threshold x hthreshold
  have hy := tail_indicator_square_bound threshold y hthreshold
  have hz := tail_indicator_square_bound threshold z hthreshold
  unfold threePointTailMass threePointMeanSquare
  nlinarith

theorem mode_chi_square_one_step_decay (slow fast : ℝ) :
    modeChiSquare (((3 : ℝ) / 4) * slow) (((1 : ℝ) / 4) * fast) ≤
      ((9 : ℝ) / 16) * modeChiSquare slow fast := by
  unfold modeChiSquare
  nlinarith [sq_nonneg fast]

theorem mode_chi_square_iterated_decay (slow fast : ℝ) :
    ∀ n, modeChiSquareAt slow fast n ≤
      (((9 : ℝ) / 16) ^ n) * modeChiSquare slow fast := by
  intro n
  induction n with
  | zero =>
      simp [modeChiSquareAt, slowModeAt, fastModeAt]
  | succ n ih =>
      have hstep := mode_chi_square_one_step_decay
        (slowModeAt slow n) (fastModeAt fast n)
      calc
        modeChiSquareAt slow fast (n + 1) =
            modeChiSquare
              (((3 : ℝ) / 4) * slowModeAt slow n)
              (((1 : ℝ) / 4) * fastModeAt fast n) := by
                simp [modeChiSquareAt, slowModeAt, fastModeAt]
        _ ≤ ((9 : ℝ) / 16) *
            modeChiSquareAt slow fast n := by
              simpa [modeChiSquareAt] using hstep
        _ ≤ ((9 : ℝ) / 16) *
            ((((9 : ℝ) / 16) ^ n) * modeChiSquare slow fast) := by
              exact mul_le_mul_of_nonneg_left ih (by norm_num)
        _ = (((9 : ℝ) / 16) ^ (n + 1)) *
            modeChiSquare slow fast := by
              rw [pow_succ]
              ring

theorem finite_three_state_concentration_profile
    (threshold slow fast : ℝ)
    (n : ℕ)
    (hthreshold : 0 ≤ threshold) :
    modeTailMassAt threshold slow fast n * threshold ^ 2 ≤
      (((9 : ℝ) / 16) ^ n) * modeChiSquare slow fast := by
  have htail := three_point_quadratic_concentration
    threshold
    (likelihoodDeviationEarly (slowModeAt slow n) (fastModeAt fast n))
    (likelihoodDeviationMiddle (slowModeAt slow n) (fastModeAt fast n))
    (likelihoodDeviationLate (slowModeAt slow n) (fastModeAt fast n))
    hthreshold
  have hexact := likelihood_deviation_mean_square_exact
    (slowModeAt slow n) (fastModeAt fast n)
  have hdecay := mode_chi_square_iterated_decay slow fast n
  calc
    modeTailMassAt threshold slow fast n * threshold ^ 2 ≤
        modeChiSquareAt slow fast n := by
          unfold modeTailMassAt modeChiSquareAt
          rw [← hexact]
          exact htail
    _ ≤ (((9 : ℝ) / 16) ^ n) * modeChiSquare slow fast := hdecay

theorem reference_slow_mode_chi_square_decay_exact (slow : ℝ) :
    modeChiSquare (((3 : ℝ) / 4) * slow) 0 =
      ((9 : ℝ) / 16) * modeChiSquare slow 0 := by
  unfold modeChiSquare
  ring

theorem exact_reference_quarter_tail_threshold :
    referenceLikelihoodAmplitude 2 ≥ (1 : ℚ) / 4 ∧
      referenceLikelihoodAmplitude 3 < (1 : ℚ) / 4 := by
  norm_num [referenceLikelihoodAmplitude]

theorem exact_reference_eighth_tail_threshold :
    referenceLikelihoodAmplitude 4 ≥ (1 : ℚ) / 8 ∧
      referenceLikelihoodAmplitude 5 < (1 : ℚ) / 8 := by
  norm_num [referenceLikelihoodAmplitude]

theorem full_rank_curvature_hierarchy_transport_commutes
    (sourceKL sourceChi sourceDir sourceGamma
      targetKL targetChi targetDir targetGamma : ℝ)
    (hKL : targetKL = sourceKL)
    (hChi : targetChi = sourceChi)
    (hDir : targetDir = sourceDir)
    (hGamma : targetGamma = sourceGamma)
    (hsource :
      sourceKL ≤ sourceChi ∧
      sourceChi ≤ 4 * sourceDir ∧
      4 * sourceDir ≤ 16 * sourceGamma) :
    targetKL ≤ targetChi ∧
      targetChi ≤ 4 * targetDir ∧
      4 * targetDir ≤ 16 * targetGamma := by
  rcases hsource with ⟨h₁, h₂, h₃⟩
  subst targetKL
  subst targetChi
  subst targetDir
  subst targetGamma
  exact ⟨h₁, h₂, h₃⟩

structure BakryEmeryConcentrationCertificate where
  sourceMemoryOSV060Bound : Bool
  integratedGammaTwoCurvatureExact : Bool
  curvatureLowerBoundQuarterExact : Bool
  poincareConstantFourExact : Bool
  functionalInequalityHierarchyExact : Bool
  finiteThreeStateConcentrationExact : Bool
  fullRankTransportCommutes : Bool
  singularAtomicProfileRetained : Bool
  rankOneDensityRecoveryNotClaimed : Bool
  candidateRankingPerformed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  persistentWORLDStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

theorem certificate_grants_no_authority
    (certificate : BakryEmeryConcentrationCertificate)
    (hranking : certificate.candidateRankingPerformed = false)
    (hpruning : certificate.candidatePruningPerformed = false)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hcommit : certificate.decisionCommitPerformed = false)
    (hactivation : certificate.activationPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hworld : certificate.persistentWORLDStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false) :
    certificate.candidateRankingPerformed = false ∧
      certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.persistentWORLDStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false := by
  exact ⟨
    hranking, hpruning, hselection, hcommit, hactivation,
    hexecution, hworld, hverification, htruth
  ⟩

end KUOS.OpenHorizon.MemoryOSBakryEmeryConcentrationV0_61
