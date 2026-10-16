import Mathlib
import KUOS.OpenHorizon.MemoryOSFiniteLogMGFChernoffTailV0_64

namespace KUOS.OpenHorizon.MemoryOSFiniteLegendreOptimizerV0_65

open KUOS.OpenHorizon.MemoryOSKantorovichLipschitzMGFV0_63
open KUOS.OpenHorizon.MemoryOSFiniteLogMGFChernoffTailV0_64

noncomputable section


def finiteTiltGrid : Finset ℝ :=
  (Finset.range 5).image (fun n : ℕ => (n : ℝ))


theorem finite_tilt_grid_nonempty : finiteTiltGrid.Nonempty := by
  refine ⟨0, ?_⟩
  simp [finiteTiltGrid]


theorem finite_tilt_grid_nonnegative {tilt : ℝ}
    (htilt : tilt ∈ finiteTiltGrid) :
    0 ≤ tilt := by
  classical
  change tilt ∈ (Finset.range 5).image (fun n : ℕ => (n : ℝ)) at htilt
  rcases Finset.mem_image.mp htilt with ⟨n, hn, rfl⟩
  positivity


theorem finite_tilt_grid_le_four {tilt : ℝ}
    (htilt : tilt ∈ finiteTiltGrid) :
    tilt ≤ 4 := by
  classical
  change tilt ∈ (Finset.range 5).image (fun n : ℕ => (n : ℝ)) at htilt
  rcases Finset.mem_image.mp htilt with ⟨n, hn, rfl⟩
  have hnlt : n < 5 := Finset.mem_range.mp hn
  have hnle : n ≤ 4 := by omega
  exact_mod_cast hnle


theorem four_mem_finite_tilt_grid : (4 : ℝ) ∈ finiteTiltGrid := by
  simp [finiteTiltGrid]


def legendreObjective
    (f : ThreeObservable) (threshold tilt : ℝ) : ℝ :=
  tilt * threshold - stationaryLogMGF f tilt


structure FiniteLegendreOptimizer
    (f : ThreeObservable) (threshold : ℝ) where
  tilt : ℝ
  mem_grid : tilt ∈ finiteTiltGrid
  maximal :
    ∀ candidate ∈ finiteTiltGrid,
      legendreObjective f threshold candidate ≤
        legendreObjective f threshold tilt


theorem finite_legendre_optimizer_exists
    (f : ThreeObservable) (threshold : ℝ) :
    Nonempty (FiniteLegendreOptimizer f threshold) := by
  classical
  let values : Finset ℝ :=
    finiteTiltGrid.image
      (fun tilt => legendreObjective f threshold tilt)
  have hvalues : values.Nonempty := by
    rcases finite_tilt_grid_nonempty with ⟨tilt, htilt⟩
    refine ⟨legendreObjective f threshold tilt, ?_⟩
    exact Finset.mem_image.mpr ⟨tilt, htilt, rfl⟩
  have hmaxmem : values.max' hvalues ∈ values :=
    Finset.max'_mem values hvalues
  rcases Finset.mem_image.mp hmaxmem with
    ⟨tilt, htilt, htiltmax⟩
  refine ⟨{
    tilt := tilt
    mem_grid := htilt
    maximal := ?_
  }⟩
  intro candidate hcandidate
  have hcandmem :
      legendreObjective f threshold candidate ∈ values :=
    Finset.mem_image.mpr ⟨candidate, hcandidate, rfl⟩
  have hle :
      legendreObjective f threshold candidate ≤ values.max' hvalues :=
    Finset.le_max' values _ hcandmem
  exact hle.trans_eq htiltmax.symm


noncomputable def chosenFiniteLegendreOptimizer
    (f : ThreeObservable) (threshold : ℝ) :
    FiniteLegendreOptimizer f threshold :=
  Classical.choice (finite_legendre_optimizer_exists f threshold)


noncomputable def finiteLegendreRate
    (f : ThreeObservable) (threshold : ℝ) : ℝ :=
  legendreObjective f threshold
    (chosenFiniteLegendreOptimizer f threshold).tilt


noncomputable def finiteOptimizedEnvelope
    (f : ThreeObservable) (threshold : ℝ) : ℝ :=
  Real.exp (-(finiteLegendreRate f threshold))


theorem chosen_finite_legendre_optimizer_mem
    (f : ThreeObservable) (threshold : ℝ) :
    (chosenFiniteLegendreOptimizer f threshold).tilt ∈ finiteTiltGrid :=
  (chosenFiniteLegendreOptimizer f threshold).mem_grid


theorem finite_legendre_rate_dominates_grid
    (f : ThreeObservable) (threshold candidate : ℝ)
    (hcandidate : candidate ∈ finiteTiltGrid) :
    legendreObjective f threshold candidate ≤
      finiteLegendreRate f threshold := by
  exact
    (chosenFiniteLegendreOptimizer f threshold).maximal
      candidate hcandidate


theorem finite_legendre_rate_nonnegative
    (f : ThreeObservable) (threshold : ℝ) :
    0 ≤ finiteLegendreRate f threshold := by
  have hzero :=
    finite_legendre_rate_dominates_grid
      f threshold 0 (by simp [finiteTiltGrid])
  simpa [finiteLegendreRate, legendreObjective,
    stationary_log_mgf_zero] using hzero


theorem finite_optimized_envelope_eq_chosen
    (f : ThreeObservable) (threshold : ℝ) :
    finiteOptimizedEnvelope f threshold =
      chernoffEnvelope f
        (chosenFiniteLegendreOptimizer f threshold).tilt threshold := by
  rw [← chernoff_transform_exponentiates]
  unfold finiteOptimizedEnvelope finiteLegendreRate legendreObjective
  unfold chernoffTransform
  congr 1
  ring


theorem finite_optimized_envelope_le_candidate
    (f : ThreeObservable) (threshold candidate : ℝ)
    (hcandidate : candidate ∈ finiteTiltGrid) :
    finiteOptimizedEnvelope f threshold ≤
      chernoffEnvelope f candidate threshold := by
  rw [finite_optimized_envelope_eq_chosen]
  rw [← chernoff_transform_exponentiates]
  rw [← chernoff_transform_exponentiates]
  apply Real.exp_le_exp.mpr
  have hmax :=
    (chosenFiniteLegendreOptimizer f threshold).maximal
      candidate hcandidate
  unfold legendreObjective at hmax
  unfold chernoffTransform
  linarith


theorem finite_optimized_envelope_le_one
    (f : ThreeObservable) (threshold : ℝ) :
    finiteOptimizedEnvelope f threshold ≤ 1 := by
  have hrate := finite_legendre_rate_nonnegative f threshold
  unfold finiteOptimizedEnvelope
  have hneg : -(finiteLegendreRate f threshold) ≤ 0 :=
    neg_nonpos.mpr hrate
  have hexp := Real.exp_le_exp.mpr hneg
  simpa using hexp


theorem slow_upper_tail_finite_optimized_bound
    (amplitude threshold : ℝ) :
    slowUpperTailMass amplitude threshold ≤
      finiteOptimizedEnvelope
        (observableScale amplitude slowObservable) threshold := by
  rw [finite_optimized_envelope_eq_chosen]
  exact slow_upper_tail_chernoff_bound
    amplitude threshold
    (chosenFiniteLegendreOptimizer
      (observableScale amplitude slowObservable) threshold).tilt
    (finite_tilt_grid_nonnegative
      (chosenFiniteLegendreOptimizer
        (observableScale amplitude slowObservable) threshold).mem_grid)


theorem fast_upper_tail_finite_optimized_bound
    (amplitude threshold : ℝ) :
    fastUpperTailMass amplitude threshold ≤
      finiteOptimizedEnvelope
        (observableScale amplitude fastObservable) threshold := by
  rw [finite_optimized_envelope_eq_chosen]
  exact fast_upper_tail_chernoff_bound
    amplitude threshold
    (chosenFiniteLegendreOptimizer
      (observableScale amplitude fastObservable) threshold).tilt
    (finite_tilt_grid_nonnegative
      (chosenFiniteLegendreOptimizer
        (observableScale amplitude fastObservable) threshold).mem_grid)


theorem chernoff_envelope_support_expansion
    (f : ThreeObservable) (tilt threshold : ℝ) :
    chernoffEnvelope f tilt threshold =
      (Real.exp (tilt * (f.early - threshold)) +
        Real.exp (tilt * (f.middle - threshold)) +
        Real.exp (tilt * (f.late - threshold))) / 3 := by
  unfold chernoffEnvelope stationaryMGF
  have hEarly :
      Real.exp (-(tilt * threshold)) * Real.exp (tilt * f.early) =
        Real.exp (tilt * (f.early - threshold)) := by
    rw [← Real.exp_add]
    congr 1
    ring
  have hMiddle :
      Real.exp (-(tilt * threshold)) * Real.exp (tilt * f.middle) =
        Real.exp (tilt * (f.middle - threshold)) := by
    rw [← Real.exp_add]
    congr 1
    ring
  have hLate :
      Real.exp (-(tilt * threshold)) * Real.exp (tilt * f.late) =
        Real.exp (tilt * (f.late - threshold)) := by
    rw [← Real.exp_add]
    congr 1
    ring
  calc
    Real.exp (-(tilt * threshold)) *
        ((Real.exp (tilt * f.early) +
          Real.exp (tilt * f.middle) +
          Real.exp (tilt * f.late)) / 3) =
      (Real.exp (-(tilt * threshold)) * Real.exp (tilt * f.early) +
        Real.exp (-(tilt * threshold)) * Real.exp (tilt * f.middle) +
        Real.exp (-(tilt * threshold)) * Real.exp (tilt * f.late)) / 3 := by
          ring
    _ = (Real.exp (tilt * (f.early - threshold)) +
        Real.exp (tilt * (f.middle - threshold)) +
        Real.exp (tilt * (f.late - threshold))) / 3 := by
          rw [hEarly, hMiddle, hLate]


theorem chernoff_envelope_antitone_of_support_below
    (f : ThreeObservable) (threshold smallerTilt largerTilt : ℝ)
    (htilts : smallerTilt ≤ largerTilt)
    (hEarly : f.early ≤ threshold)
    (hMiddle : f.middle ≤ threshold)
    (hLate : f.late ≤ threshold) :
    chernoffEnvelope f largerTilt threshold ≤
      chernoffEnvelope f smallerTilt threshold := by
  rw [chernoff_envelope_support_expansion]
  rw [chernoff_envelope_support_expansion]
  have hEarlyExp :
      Real.exp (largerTilt * (f.early - threshold)) ≤
        Real.exp (smallerTilt * (f.early - threshold)) := by
    apply Real.exp_le_exp.mpr
    exact mul_le_mul_of_nonpos_right htilts (sub_nonpos.mpr hEarly)
  have hMiddleExp :
      Real.exp (largerTilt * (f.middle - threshold)) ≤
        Real.exp (smallerTilt * (f.middle - threshold)) := by
    apply Real.exp_le_exp.mpr
    exact mul_le_mul_of_nonpos_right htilts (sub_nonpos.mpr hMiddle)
  have hLateExp :
      Real.exp (largerTilt * (f.late - threshold)) ≤
        Real.exp (smallerTilt * (f.late - threshold)) := by
    apply Real.exp_le_exp.mpr
    exact mul_le_mul_of_nonpos_right htilts (sub_nonpos.mpr hLate)
  nlinarith


theorem finite_optimized_envelope_eq_tilt_four_of_support_below
    (f : ThreeObservable) (threshold : ℝ)
    (hEarly : f.early ≤ threshold)
    (hMiddle : f.middle ≤ threshold)
    (hLate : f.late ≤ threshold) :
    finiteOptimizedEnvelope f threshold =
      chernoffEnvelope f 4 threshold := by
  apply le_antisymm
  · exact finite_optimized_envelope_le_candidate
      f threshold 4 four_mem_finite_tilt_grid
  · rw [finite_optimized_envelope_eq_chosen]
    exact chernoff_envelope_antitone_of_support_below
      f threshold
      (chosenFiniteLegendreOptimizer f threshold).tilt 4
      (finite_tilt_grid_le_four
        (chosenFiniteLegendreOptimizer f threshold).mem_grid)
      hEarly hMiddle hLate


theorem slow_half_extinct_tilt_four_optimizer :
    finiteOptimizedEnvelope
        (observableScale (((3 : ℝ) / 4) ^ 3) slowObservable)
        ((1 : ℝ) / 2) =
      chernoffEnvelope
        (observableScale (((3 : ℝ) / 4) ^ 3) slowObservable)
        4 ((1 : ℝ) / 2) := by
  apply finite_optimized_envelope_eq_tilt_four_of_support_below
  all_goals norm_num [observableScale, slowObservable]


theorem slow_quarter_extinct_tilt_four_optimizer :
    finiteOptimizedEnvelope
        (observableScale (((3 : ℝ) / 4) ^ 5) slowObservable)
        ((1 : ℝ) / 4) =
      chernoffEnvelope
        (observableScale (((3 : ℝ) / 4) ^ 5) slowObservable)
        4 ((1 : ℝ) / 4) := by
  apply finite_optimized_envelope_eq_tilt_four_of_support_below
  all_goals norm_num [observableScale, slowObservable]


theorem fast_half_extinct_tilt_four_optimizer :
    finiteOptimizedEnvelope
        (observableScale (((1 : ℝ) / 4) ^ 1) fastObservable)
        ((1 : ℝ) / 2) =
      chernoffEnvelope
        (observableScale (((1 : ℝ) / 4) ^ 1) fastObservable)
        4 ((1 : ℝ) / 2) := by
  apply finite_optimized_envelope_eq_tilt_four_of_support_below
  all_goals norm_num [observableScale, fastObservable]


theorem fast_quarter_extinct_tilt_four_optimizer :
    finiteOptimizedEnvelope
        (observableScale (((1 : ℝ) / 4) ^ 2) fastObservable)
        ((1 : ℝ) / 4) =
      chernoffEnvelope
        (observableScale (((1 : ℝ) / 4) ^ 2) fastObservable)
        4 ((1 : ℝ) / 4) := by
  apply finite_optimized_envelope_eq_tilt_four_of_support_below
  all_goals norm_num [observableScale, fastObservable]


theorem full_rank_finite_legendre_optimizer_commutes
    (sourceRate sourceEnvelope targetRate targetEnvelope : ℝ)
    (hRate : targetRate = sourceRate)
    (hEnvelope : targetEnvelope = sourceEnvelope) :
    targetRate = sourceRate ∧ targetEnvelope = sourceEnvelope := by
  exact ⟨hRate, hEnvelope⟩


structure FiniteLegendreOptimizerCertificate where
  sourceMemoryOSV064Bound : Bool
  finiteTiltGridExact : Bool
  finiteArgmaxExistsExact : Bool
  finiteLegendreRateNonnegative : Bool
  optimizedEnvelopeTailBoundExact : Bool
  extinctProfileTiltFourOptimizerExact : Bool
  continuousTiltOptimizerClaimed : Bool
  generalLargeDeviationPrincipleClaimed : Bool
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
    (certificate : FiniteLegendreOptimizerCertificate)
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
  exact ⟨hranking, hpruning, hselection, hcommit, hactivation,
    hexecution, hworld, hverification, htruth⟩


end

end KUOS.OpenHorizon.MemoryOSFiniteLegendreOptimizerV0_65
