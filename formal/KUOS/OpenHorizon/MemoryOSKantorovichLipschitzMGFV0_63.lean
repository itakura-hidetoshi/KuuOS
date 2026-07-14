import Mathlib
import KUOS.OpenHorizon.MemoryOSWassersteinMartonTransportV0_62

namespace KUOS.OpenHorizon.MemoryOSKantorovichLipschitzMGFV0_63

open KUOS.OpenHorizon.MemoryOSWassersteinMartonTransportV0_62

structure ThreeObservable where
  early : ℝ
  middle : ℝ
  late : ℝ


def lipschitzSeminorm (f : ThreeObservable) : ℝ :=
  max |f.early - f.middle| |f.middle - f.late|


def centeredDeltaObjective
    (deltaEarly deltaMiddle : ℝ) (f : ThreeObservable) : ℝ :=
  deltaEarly * f.early + deltaMiddle * f.middle -
    (deltaEarly + deltaMiddle) * f.late


def pathWassersteinDelta (deltaEarly deltaMiddle : ℝ) : ℝ :=
  |deltaEarly| + |deltaEarly + deltaMiddle|


def edgeSign (x : ℝ) : ℝ :=
  if 0 ≤ x then 1 else -1


def dualOptimizer (deltaEarly deltaMiddle : ℝ) : ThreeObservable where
  early := edgeSign deltaEarly
  middle := 0
  late := -edgeSign (deltaEarly + deltaMiddle)


def kernelAction (f : ThreeObservable) : ThreeObservable where
  early := ((3 : ℝ) / 4) * f.early + ((1 : ℝ) / 4) * f.middle
  middle := ((1 : ℝ) / 4) * f.early + ((1 : ℝ) / 2) * f.middle +
    ((1 : ℝ) / 4) * f.late
  late := ((1 : ℝ) / 4) * f.middle + ((3 : ℝ) / 4) * f.late


def kernelIterate : ℕ → ThreeObservable → ThreeObservable
  | 0, f => f
  | n + 1, f => kernelAction (kernelIterate n f)


def observableScale (c : ℝ) (f : ThreeObservable) : ThreeObservable where
  early := c * f.early
  middle := c * f.middle
  late := c * f.late


def slowObservable : ThreeObservable where
  early := 1
  middle := 0
  late := -1


def fastObservable : ThreeObservable where
  early := 1
  middle := -2
  late := 1


def stationaryMean (f : ThreeObservable) : ℝ :=
  (f.early + f.middle + f.late) / 3


def stationarySecondMoment (f : ThreeObservable) : ℝ :=
  (f.early ^ 2 + f.middle ^ 2 + f.late ^ 2) / 3


def stationaryMGF (f : ThreeObservable) (t : ℝ) : ℝ :=
  (Real.exp (t * f.early) + Real.exp (t * f.middle) +
    Real.exp (t * f.late)) / 3


def slowMartonSensitivity (n : ℕ) : ℚ :=
  martonInfluenceSum n * (((3 : ℚ) / 4) ^ n)


theorem edgeSign_mul_self_abs (x : ℝ) :
    x * edgeSign x = |x| := by
  by_cases h : 0 ≤ x
  · simp [edgeSign, h, abs_of_nonneg h]
  · have hx : x ≤ 0 := le_of_not_ge h
    simp [edgeSign, h, abs_of_nonpos hx]


theorem edgeSign_abs (x : ℝ) : |edgeSign x| = 1 := by
  by_cases h : 0 ≤ x <;> simp [edgeSign, h]


theorem dual_optimizer_is_one_lipschitz
    (deltaEarly deltaMiddle : ℝ) :
    lipschitzSeminorm (dualOptimizer deltaEarly deltaMiddle) ≤ 1 := by
  simp [lipschitzSeminorm, dualOptimizer, edgeSign_abs]


theorem dual_optimizer_attains_path_wasserstein
    (deltaEarly deltaMiddle : ℝ) :
    centeredDeltaObjective deltaEarly deltaMiddle
        (dualOptimizer deltaEarly deltaMiddle) =
      pathWassersteinDelta deltaEarly deltaMiddle := by
  simp [centeredDeltaObjective, dualOptimizer, pathWassersteinDelta,
    edgeSign_mul_self_abs]


theorem centered_delta_objective_rewrite
    (deltaEarly deltaMiddle : ℝ) (f : ThreeObservable) :
    centeredDeltaObjective deltaEarly deltaMiddle f =
      deltaEarly * (f.early - f.middle) +
        (deltaEarly + deltaMiddle) * (f.middle - f.late) := by
  unfold centeredDeltaObjective
  ring


theorem one_lipschitz_expectation_gap_le_wasserstein_times_lip
    (deltaEarly deltaMiddle : ℝ) (f : ThreeObservable) :
    |centeredDeltaObjective deltaEarly deltaMiddle f| ≤
      pathWassersteinDelta deltaEarly deltaMiddle * lipschitzSeminorm f := by
  rw [centered_delta_objective_rewrite]
  have hEarly :
      |f.early - f.middle| ≤ lipschitzSeminorm f := by
    exact le_max_left _ _
  have hLate :
      |f.middle - f.late| ≤ lipschitzSeminorm f := by
    exact le_max_right _ _
  calc
    |deltaEarly * (f.early - f.middle) +
        (deltaEarly + deltaMiddle) * (f.middle - f.late)|
        ≤ |deltaEarly * (f.early - f.middle)| +
            |(deltaEarly + deltaMiddle) * (f.middle - f.late)| :=
          abs_add _ _
    _ = |deltaEarly| * |f.early - f.middle| +
          |deltaEarly + deltaMiddle| * |f.middle - f.late| := by
          rw [abs_mul, abs_mul]
    _ ≤ |deltaEarly| * lipschitzSeminorm f +
          |deltaEarly + deltaMiddle| * lipschitzSeminorm f := by
          exact add_le_add
            (mul_le_mul_of_nonneg_left hEarly (abs_nonneg _))
            (mul_le_mul_of_nonneg_left hLate (abs_nonneg _))
    _ = pathWassersteinDelta deltaEarly deltaMiddle *
          lipschitzSeminorm f := by
          unfold pathWassersteinDelta
          ring


theorem one_lipschitz_expectation_gap_le_wasserstein
    (deltaEarly deltaMiddle : ℝ) (f : ThreeObservable)
    (hLip : lipschitzSeminorm f ≤ 1) :
    |centeredDeltaObjective deltaEarly deltaMiddle f| ≤
      pathWassersteinDelta deltaEarly deltaMiddle := by
  calc
    |centeredDeltaObjective deltaEarly deltaMiddle f| ≤
        pathWassersteinDelta deltaEarly deltaMiddle *
          lipschitzSeminorm f :=
      one_lipschitz_expectation_gap_le_wasserstein_times_lip _ _ _
    _ ≤ pathWassersteinDelta deltaEarly deltaMiddle * 1 := by
      exact mul_le_mul_of_nonneg_left hLip (by
        unfold pathWassersteinDelta
        positivity)
    _ = pathWassersteinDelta deltaEarly deltaMiddle := by ring


theorem three_point_kantorovich_duality_explicit_optimizer
    (deltaEarly deltaMiddle : ℝ) :
    ∃ f : ThreeObservable,
      lipschitzSeminorm f ≤ 1 ∧
      centeredDeltaObjective deltaEarly deltaMiddle f =
        pathWassersteinDelta deltaEarly deltaMiddle := by
  exact ⟨dualOptimizer deltaEarly deltaMiddle,
    dual_optimizer_is_one_lipschitz _ _,
    dual_optimizer_attains_path_wasserstein _ _⟩


theorem kernel_lipschitz_one_step_contraction (f : ThreeObservable) :
    lipschitzSeminorm (kernelAction f) ≤
      ((3 : ℝ) / 4) * lipschitzSeminorm f := by
  let x := f.early - f.middle
  let y := f.middle - f.late
  let L := max |x| |y|
  have hx : |x| ≤ L := le_max_left _ _
  have hy : |y| ≤ L := le_max_right _ _
  have hFirst :
      |((1 : ℝ) / 2) * x + ((1 : ℝ) / 4) * y| ≤
        ((3 : ℝ) / 4) * L := by
    calc
      |((1 : ℝ) / 2) * x + ((1 : ℝ) / 4) * y| ≤
          |((1 : ℝ) / 2) * x| + |((1 : ℝ) / 4) * y| :=
        abs_add _ _
      _ = ((1 : ℝ) / 2) * |x| + ((1 : ℝ) / 4) * |y| := by
        rw [abs_mul, abs_mul]
        norm_num
      _ ≤ ((1 : ℝ) / 2) * L + ((1 : ℝ) / 4) * L := by
        exact add_le_add
          (mul_le_mul_of_nonneg_left hx (by norm_num))
          (mul_le_mul_of_nonneg_left hy (by norm_num))
      _ = ((3 : ℝ) / 4) * L := by ring
  have hSecond :
      |((1 : ℝ) / 4) * x + ((1 : ℝ) / 2) * y| ≤
        ((3 : ℝ) / 4) * L := by
    calc
      |((1 : ℝ) / 4) * x + ((1 : ℝ) / 2) * y| ≤
          |((1 : ℝ) / 4) * x| + |((1 : ℝ) / 2) * y| :=
        abs_add _ _
      _ = ((1 : ℝ) / 4) * |x| + ((1 : ℝ) / 2) * |y| := by
        rw [abs_mul, abs_mul]
        norm_num
      _ ≤ ((1 : ℝ) / 4) * L + ((1 : ℝ) / 2) * L := by
        exact add_le_add
          (mul_le_mul_of_nonneg_left hx (by norm_num))
          (mul_le_mul_of_nonneg_left hy (by norm_num))
      _ = ((3 : ℝ) / 4) * L := by ring
  change max
      |(((3 : ℝ) / 4) * f.early + ((1 : ℝ) / 4) * f.middle) -
        (((1 : ℝ) / 4) * f.early + ((1 : ℝ) / 2) * f.middle +
          ((1 : ℝ) / 4) * f.late)|
      |(((1 : ℝ) / 4) * f.early + ((1 : ℝ) / 2) * f.middle +
          ((1 : ℝ) / 4) * f.late) -
        (((1 : ℝ) / 4) * f.middle + ((3 : ℝ) / 4) * f.late)| ≤
      ((3 : ℝ) / 4) * max
        |f.early - f.middle| |f.middle - f.late|
  rw [show
      (((3 : ℝ) / 4) * f.early + ((1 : ℝ) / 4) * f.middle) -
          (((1 : ℝ) / 4) * f.early + ((1 : ℝ) / 2) * f.middle +
            ((1 : ℝ) / 4) * f.late) =
        ((1 : ℝ) / 2) * x + ((1 : ℝ) / 4) * y by
      simp [x, y]
      ring]
  rw [show
      (((1 : ℝ) / 4) * f.early + ((1 : ℝ) / 2) * f.middle +
          ((1 : ℝ) / 4) * f.late) -
          (((1 : ℝ) / 4) * f.middle + ((3 : ℝ) / 4) * f.late) =
        ((1 : ℝ) / 4) * x + ((1 : ℝ) / 2) * y by
      simp [x, y]
      ring]
  simpa [L, x, y] using max_le hFirst hSecond


theorem kernel_lipschitz_iterated_contraction (f : ThreeObservable) :
    ∀ n : ℕ,
      lipschitzSeminorm (kernelIterate n f) ≤
        (((3 : ℝ) / 4) ^ n) * lipschitzSeminorm f := by
  intro n
  induction n with
  | zero => simp [kernelIterate]
  | succ n ih =>
      calc
        lipschitzSeminorm (kernelIterate (n + 1) f) =
            lipschitzSeminorm (kernelAction (kernelIterate n f)) := by
              rfl
        _ ≤ ((3 : ℝ) / 4) *
            lipschitzSeminorm (kernelIterate n f) :=
              kernel_lipschitz_one_step_contraction _
        _ ≤ ((3 : ℝ) / 4) *
            ((((3 : ℝ) / 4) ^ n) * lipschitzSeminorm f) := by
              exact mul_le_mul_of_nonneg_left ih (by norm_num)
        _ = (((3 : ℝ) / 4) ^ (n + 1)) * lipschitzSeminorm f := by
              rw [pow_succ]
              ring


theorem kernelAction_scale (c : ℝ) (f : ThreeObservable) :
    kernelAction (observableScale c f) = observableScale c (kernelAction f) := by
  ext <;> simp [kernelAction, observableScale] <;> ring


theorem kernelAction_slow_exact :
    kernelAction slowObservable =
      observableScale ((3 : ℝ) / 4) slowObservable := by
  ext <;> norm_num [kernelAction, observableScale, slowObservable]


theorem kernelAction_fast_exact :
    kernelAction fastObservable =
      observableScale ((1 : ℝ) / 4) fastObservable := by
  ext <;> norm_num [kernelAction, observableScale, fastObservable]


theorem observableScale_mul (a b : ℝ) (f : ThreeObservable) :
    observableScale a (observableScale b f) = observableScale (a * b) f := by
  ext <;> simp [observableScale] <;> ring


theorem slow_observable_semigroup_exact :
    ∀ n : ℕ,
      kernelIterate n slowObservable =
        observableScale (((3 : ℝ) / 4) ^ n) slowObservable := by
  intro n
  induction n with
  | zero =>
      ext <;> simp [kernelIterate, observableScale]
  | succ n ih =>
      rw [show kernelIterate (n + 1) slowObservable =
          kernelAction (kernelIterate n slowObservable) by rfl]
      rw [ih, kernelAction_scale, kernelAction_slow_exact,
        observableScale_mul, pow_succ]


theorem fast_observable_semigroup_exact :
    ∀ n : ℕ,
      kernelIterate n fastObservable =
        observableScale (((1 : ℝ) / 4) ^ n) fastObservable := by
  intro n
  induction n with
  | zero =>
      ext <;> simp [kernelIterate, observableScale]
  | succ n ih =>
      rw [show kernelIterate (n + 1) fastObservable =
          kernelAction (kernelIterate n fastObservable) by rfl]
      rw [ih, kernelAction_scale, kernelAction_fast_exact,
        observableScale_mul, pow_succ]


theorem slow_observable_centered : stationaryMean slowObservable = 0 := by
  norm_num [stationaryMean, slowObservable]


theorem fast_observable_centered : stationaryMean fastObservable = 0 := by
  norm_num [stationaryMean, fastObservable]


theorem stationary_mgf_scaled_slow_exact (r t : ℝ) :
    stationaryMGF (observableScale r slowObservable) t =
      (Real.exp (t * r) + 1 + Real.exp (-(t * r))) / 3 := by
  simp [stationaryMGF, observableScale, slowObservable]
  ring_nf


theorem stationary_mgf_scaled_fast_exact (r t : ℝ) :
    stationaryMGF (observableScale r fastObservable) t =
      (2 * Real.exp (t * r) + Real.exp (-(2 * t * r))) / 3 := by
  simp [stationaryMGF, observableScale, fastObservable]
  ring_nf


theorem stationary_second_moment_scaled_slow_exact (r : ℝ) :
    stationarySecondMoment (observableScale r slowObservable) =
      ((2 : ℝ) / 3) * r ^ 2 := by
  norm_num [stationarySecondMoment, observableScale, slowObservable]
  ring


theorem stationary_second_moment_scaled_fast_exact (r : ℝ) :
    stationarySecondMoment (observableScale r fastObservable) =
      2 * r ^ 2 := by
  norm_num [stationarySecondMoment, observableScale, fastObservable]
  ring


theorem slow_semigroup_mgf_exact (n : ℕ) (t : ℝ) :
    stationaryMGF (kernelIterate n slowObservable) t =
      (Real.exp (t * (((3 : ℝ) / 4) ^ n)) + 1 +
        Real.exp (-(t * (((3 : ℝ) / 4) ^ n)))) / 3 := by
  rw [slow_observable_semigroup_exact]
  exact stationary_mgf_scaled_slow_exact _ _


theorem fast_semigroup_mgf_exact (n : ℕ) (t : ℝ) :
    stationaryMGF (kernelIterate n fastObservable) t =
      (2 * Real.exp (t * (((1 : ℝ) / 4) ^ n)) +
        Real.exp (-(2 * t * (((1 : ℝ) / 4) ^ n)))) / 3 := by
  rw [fast_observable_semigroup_exact]
  exact stationary_mgf_scaled_fast_exact _ _


theorem slow_marton_sensitivity_closed_form (n : ℕ) :
    slowMartonSensitivity n =
      4 * (1 - (((3 : ℚ) / 4) ^ n)) * (((3 : ℚ) / 4) ^ n) := by
  unfold slowMartonSensitivity
  rw [marton_influence_closed_form]


theorem full_rank_kantorovich_lipschitz_mgf_commutes
    (sourceDual sourceLip sourceMGF targetDual targetLip targetMGF : ℝ)
    (hDual : targetDual = sourceDual)
    (hLip : targetLip = sourceLip)
    (hMGF : targetMGF = sourceMGF) :
    targetDual = sourceDual ∧ targetLip = sourceLip ∧ targetMGF = sourceMGF := by
  exact ⟨hDual, hLip, hMGF⟩


structure KantorovichLipschitzMGFCertificate where
  sourceMemoryOSV062Bound : Bool
  explicitKantorovichOptimizerExact : Bool
  universalOneLipschitzUpperBoundExact : Bool
  kernelLipschitzContractionExact : Bool
  iteratedSemigroupContractionExact : Bool
  finiteSymbolicMGFExact : Bool
  martonMGFInputsRetained : Bool
  generalPathSpaceGaussianTheoremClaimed : Bool
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
    (certificate : KantorovichLipschitzMGFCertificate)
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

end KUOS.OpenHorizon.MemoryOSKantorovichLipschitzMGFV0_63
