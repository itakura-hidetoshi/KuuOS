import Mathlib
import KUOS.OpenHorizon.MemoryOSBakryEmeryConcentrationV0_61

namespace KUOS.OpenHorizon.MemoryOSWassersteinMartonTransportV0_62

open KUOS.OpenHorizon.MemoryOSLogSobolevHypercontractiveMixingV0_59
open KUOS.OpenHorizon.MemoryOSBakryEmeryConcentrationV0_61

def pathWassersteinThree
    (p₀ p₁ q₀ q₁ : ℝ) : ℝ :=
  |p₀ - q₀| + |(p₀ + p₁) - (q₀ + q₁)|

def modePathWasserstein (slow fast : ℝ) : ℝ :=
  |slow + fast| + |slow - fast|

def modePathWassersteinAt (slow fast : ℝ) (n : ℕ) : ℝ :=
  modePathWasserstein (slowModeAt slow n) (fastModeAt fast n)

def referenceWassersteinToStationary (n : ℕ) : ℚ :=
  ((3 : ℚ) / 10) * (((3 : ℚ) / 4) ^ n)

def referencePairWasserstein (n : ℕ) : ℚ :=
  ((3 : ℚ) / 5) * (((3 : ℚ) / 4) ^ n)

def martonStatePairWasserstein (distance : ℚ) (n : ℕ) : ℚ :=
  distance * (((3 : ℚ) / 4) ^ n)

def martonInfluenceSum : ℕ → ℚ
  | 0 => 0
  | n + 1 => 1 + ((3 : ℚ) / 4) * martonInfluenceSum n

theorem kernel_row_wasserstein_exact :
    pathWassersteinThree
        ((3 : ℝ) / 4) ((1 : ℝ) / 4)
        ((1 : ℝ) / 4) ((1 : ℝ) / 2) = (3 : ℝ) / 4 ∧
    pathWassersteinThree
        ((1 : ℝ) / 4) ((1 : ℝ) / 2)
        0 ((1 : ℝ) / 4) = (3 : ℝ) / 4 ∧
    pathWassersteinThree
        ((3 : ℝ) / 4) ((1 : ℝ) / 4)
        0 ((1 : ℝ) / 4) = (3 : ℝ) / 2 := by
  norm_num [pathWassersteinThree, abs_of_nonneg, abs_of_nonpos]

theorem kernel_coarse_ricci_curvature_exact :
    (1 : ℝ) - ((3 : ℝ) / 4) = (1 : ℝ) / 4 := by
  norm_num

theorem two_abs_sum_square_le_two_squares (x y : ℝ) :
    (|x| + |y|) ^ 2 ≤ 2 * (x ^ 2 + y ^ 2) := by
  have hgap : 0 ≤ (|x| - |y|) ^ 2 := sq_nonneg _
  nlinarith [sq_abs x, sq_abs y]

theorem mode_pearson_transport_information (slow fast : ℝ) :
    modePathWasserstein slow fast ^ 2 ≤
      ((2 : ℝ) / 3) * modeChiSquare slow fast := by
  have h := two_abs_sum_square_le_two_squares
    (slow + fast) (slow - fast)
  unfold modePathWasserstein modeChiSquare
  nlinarith [sq_nonneg fast]

theorem mode_pearson_transport_information_sharp_on_slow
    (slow : ℝ) :
    modePathWasserstein slow 0 ^ 2 =
      ((2 : ℝ) / 3) * modeChiSquare slow 0 := by
  unfold modePathWasserstein modeChiSquare
  rw [sub_zero, add_zero]
  nlinarith [sq_abs slow]

theorem mode_wasserstein_one_step_contraction
    (slow fast : ℝ) :
    modePathWasserstein
        (((3 : ℝ) / 4) * slow)
        (((1 : ℝ) / 4) * fast) ≤
      ((3 : ℝ) / 4) * modePathWasserstein slow fast := by
  have h₁ :
      |((3 : ℝ) / 4) * slow + ((1 : ℝ) / 4) * fast| ≤
        ((1 : ℝ) / 2) * |slow + fast| +
          ((1 : ℝ) / 4) * |slow - fast| := by
    calc
      |((3 : ℝ) / 4) * slow + ((1 : ℝ) / 4) * fast| =
          |((1 : ℝ) / 2) * (slow + fast) +
            ((1 : ℝ) / 4) * (slow - fast)| := by
              congr 1
              ring
      _ ≤ |((1 : ℝ) / 2) * (slow + fast)| +
          |((1 : ℝ) / 4) * (slow - fast)| := abs_add _ _
      _ = ((1 : ℝ) / 2) * |slow + fast| +
          ((1 : ℝ) / 4) * |slow - fast| := by
            rw [abs_mul, abs_mul]
            norm_num
  have h₂ :
      |((3 : ℝ) / 4) * slow - ((1 : ℝ) / 4) * fast| ≤
        ((1 : ℝ) / 4) * |slow + fast| +
          ((1 : ℝ) / 2) * |slow - fast| := by
    calc
      |((3 : ℝ) / 4) * slow - ((1 : ℝ) / 4) * fast| =
          |((1 : ℝ) / 4) * (slow + fast) +
            ((1 : ℝ) / 2) * (slow - fast)| := by
              congr 1
              ring
      _ ≤ |((1 : ℝ) / 4) * (slow + fast)| +
          |((1 : ℝ) / 2) * (slow - fast)| := abs_add _ _
      _ = ((1 : ℝ) / 4) * |slow + fast| +
          ((1 : ℝ) / 2) * |slow - fast| := by
            rw [abs_mul, abs_mul]
            norm_num
  unfold modePathWasserstein
  nlinarith

theorem mode_wasserstein_iterated_contraction (slow fast : ℝ) :
    ∀ n, modePathWassersteinAt slow fast n ≤
      (((3 : ℝ) / 4) ^ n) * modePathWasserstein slow fast := by
  intro n
  induction n with
  | zero =>
      simp [modePathWassersteinAt, slowModeAt, fastModeAt]
  | succ n ih =>
      have hstep := mode_wasserstein_one_step_contraction
        (slowModeAt slow n) (fastModeAt fast n)
      calc
        modePathWassersteinAt slow fast (n + 1) =
            modePathWasserstein
              (((3 : ℝ) / 4) * slowModeAt slow n)
              (((1 : ℝ) / 4) * fastModeAt fast n) := by
                simp [modePathWassersteinAt, slowModeAt, fastModeAt]
        _ ≤ ((3 : ℝ) / 4) *
            modePathWassersteinAt slow fast n := by
              simpa [modePathWassersteinAt] using hstep
        _ ≤ ((3 : ℝ) / 4) *
            ((((3 : ℝ) / 4) ^ n) *
              modePathWasserstein slow fast) := by
                exact mul_le_mul_of_nonneg_left ih (by norm_num)
        _ = (((3 : ℝ) / 4) ^ (n + 1)) *
            modePathWasserstein slow fast := by
              rw [pow_succ]
              ring

theorem reference_wasserstein_one_step_exact (n : ℕ) :
    referenceWassersteinToStationary (n + 1) =
      ((3 : ℚ) / 4) * referenceWassersteinToStationary n := by
  unfold referenceWassersteinToStationary
  rw [pow_succ]
  ring

theorem reference_pair_wasserstein_one_step_exact (n : ℕ) :
    referencePairWasserstein (n + 1) =
      ((3 : ℚ) / 4) * referencePairWasserstein n := by
  unfold referencePairWasserstein
  rw [pow_succ]
  ring

theorem marton_state_pair_one_step_exact
    (distance : ℚ) (n : ℕ) :
    martonStatePairWasserstein distance (n + 1) =
      ((3 : ℚ) / 4) *
        martonStatePairWasserstein distance n := by
  unfold martonStatePairWasserstein
  rw [pow_succ]
  ring

theorem iterated_marton_transport_contraction
    (transport : ℕ → ℝ)
    (hstep :
      ∀ n, transport (n + 1) ≤
        ((3 : ℝ) / 4) * transport n) :
    ∀ n, transport n ≤
      (((3 : ℝ) / 4) ^ n) * transport 0 := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
      calc
        transport (n + 1) ≤
            ((3 : ℝ) / 4) * transport n := hstep n
        _ ≤ ((3 : ℝ) / 4) *
            ((((3 : ℝ) / 4) ^ n) * transport 0) := by
              exact mul_le_mul_of_nonneg_left ih (by norm_num)
        _ = (((3 : ℝ) / 4) ^ (n + 1)) * transport 0 := by
              rw [pow_succ]
              ring

theorem marton_mismatch_concentration
    (transport mismatch : ℕ → ℝ)
    (hstep :
      ∀ n, transport (n + 1) ≤
        ((3 : ℝ) / 4) * transport n)
    (hmismatch : ∀ n, mismatch n ≤ transport n) :
    ∀ n, mismatch n ≤
      (((3 : ℝ) / 4) ^ n) * transport 0 := by
  intro n
  exact (hmismatch n).trans
    (iterated_marton_transport_contraction transport hstep n)

theorem marton_observable_gap_concentration
    (transport observableGap : ℕ → ℝ)
    (hstep :
      ∀ n, transport (n + 1) ≤
        ((3 : ℝ) / 4) * transport n)
    (hgap : ∀ n, observableGap n ≤ transport n) :
    ∀ n, observableGap n ≤
      (((3 : ℝ) / 4) ^ n) * transport 0 := by
  intro n
  exact (hgap n).trans
    (iterated_marton_transport_contraction transport hstep n)

theorem marton_influence_closed_form :
    ∀ n, martonInfluenceSum n =
      4 * (1 - (((3 : ℚ) / 4) ^ n)) := by
  intro n
  induction n with
  | zero => norm_num [martonInfluenceSum]
  | succ n ih =>
      simp only [martonInfluenceSum]
      rw [ih, pow_succ]
      ring

theorem marton_influence_strictly_below_four (n : ℕ) :
    martonInfluenceSum n < 4 := by
  rw [marton_influence_closed_form]
  have hpow : 0 < (((3 : ℚ) / 4) ^ n) := by
    positivity
  nlinarith

theorem exact_reference_wasserstein_tenth_threshold :
    referenceWassersteinToStationary 3 > (1 : ℚ) / 10 ∧
      referenceWassersteinToStationary 4 ≤ (1 : ℚ) / 10 := by
  norm_num [referenceWassersteinToStationary]

theorem exact_reference_wasserstein_twentieth_threshold :
    referenceWassersteinToStationary 6 > (1 : ℚ) / 20 ∧
      referenceWassersteinToStationary 7 ≤ (1 : ℚ) / 20 := by
  norm_num [referenceWassersteinToStationary]

theorem exact_reference_pair_wasserstein_tenth_threshold :
    referencePairWasserstein 6 > (1 : ℚ) / 10 ∧
      referencePairWasserstein 7 ≤ (1 : ℚ) / 10 := by
  norm_num [referencePairWasserstein]

theorem exact_reference_pair_wasserstein_twentieth_threshold :
    referencePairWasserstein 8 > (1 : ℚ) / 20 ∧
      referencePairWasserstein 9 ≤ (1 : ℚ) / 20 := by
  norm_num [referencePairWasserstein]

theorem exact_adjacent_marton_quarter_threshold :
    martonStatePairWasserstein 1 4 > (1 : ℚ) / 4 ∧
      martonStatePairWasserstein 1 5 ≤ (1 : ℚ) / 4 := by
  norm_num [martonStatePairWasserstein]

theorem exact_endpoint_marton_quarter_threshold :
    martonStatePairWasserstein 2 7 > (1 : ℚ) / 4 ∧
      martonStatePairWasserstein 2 8 ≤ (1 : ℚ) / 4 := by
  norm_num [martonStatePairWasserstein]

theorem full_rank_wasserstein_marton_transport_commutes
    (sourceW sourceChi sourceMarton
      targetW targetChi targetMarton : ℝ)
    (hW : targetW = sourceW)
    (hChi : targetChi = sourceChi)
    (hMarton : targetMarton = sourceMarton)
    (hsource : sourceW ^ 2 ≤ ((2 : ℝ) / 3) * sourceChi) :
    targetW ^ 2 ≤ ((2 : ℝ) / 3) * targetChi ∧
      targetMarton = sourceMarton := by
  subst targetW
  subst targetChi
  exact ⟨hsource, hMarton⟩

structure WassersteinMartonTransportCertificate where
  sourceMemoryOSV061Bound : Bool
  pathMetricWassersteinExact : Bool
  kernelOptimalCouplingsExact : Bool
  dobrushinCoefficientThreeQuartersExact : Bool
  coarseRicciCurvatureQuarterExact : Bool
  pearsonTransportInformationExact : Bool
  martonCouplingProfilesExact : Bool
  martonInfluenceProfilesExact : Bool
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
    (certificate : WassersteinMartonTransportCertificate)
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

end KUOS.OpenHorizon.MemoryOSWassersteinMartonTransportV0_62
