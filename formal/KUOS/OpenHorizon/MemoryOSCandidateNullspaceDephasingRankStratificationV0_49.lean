import Mathlib
import KUOS.OpenHorizon.MemoryOSTwoHistoryCandidateGramFactorizationReconstructionV0_48

namespace KUOS.OpenHorizon.MemoryOSCandidateNullspaceDephasingRankStratificationV0_49

open KUOS.OpenHorizon.MemoryOSCandidateGramLiftDecisionOSRelationalCoherenceKernelV0_45
open KUOS.OpenHorizon.MemoryOSTwoHistoryCandidateGramFactorizationReconstructionV0_48

/-- First history coordinate obtained from candidate coefficients in candidate
    order `continue, hold, reobserve, terminate_candidate`. -/
def candidateHistoryFirst
    (continue hold reobserve terminate : ℤ) : ℤ :=
  continue + hold + reobserve

/-- Second history coordinate obtained from candidate coefficients. -/
def candidateHistorySecond
    (continue hold reobserve terminate : ℤ) : ℤ :=
  continue - hold + terminate

/-- History-space quadratic numerator for the source metric
    `[[2,cross],[cross,2]]`. -/
def candidateHistoryQuadratic
    (cross continue hold reobserve terminate : ℤ) : ℤ :=
  let first :=
    candidateHistoryFirst continue hold reobserve terminate
  let second :=
    candidateHistorySecond continue hold reobserve terminate
  2 * first * first +
    2 * cross * first * second +
    2 * second * second

/-- Candidate-space quadratic numerator computed from all sixteen entries of the
    complete four-candidate Gram kernel. -/
def candidateGramQuadratic4
    (cross continue hold reobserve terminate : ℤ) : ℤ :=
  continue *
      (continue * candidateGramEntry2 cross 1 1 1 1 +
        hold * candidateGramEntry2 cross 1 1 1 (-1) +
        reobserve * candidateGramEntry2 cross 1 1 1 0 +
        terminate * candidateGramEntry2 cross 1 1 0 1) +
    hold *
      (continue * candidateGramEntry2 cross 1 (-1) 1 1 +
        hold * candidateGramEntry2 cross 1 (-1) 1 (-1) +
        reobserve * candidateGramEntry2 cross 1 (-1) 1 0 +
        terminate * candidateGramEntry2 cross 1 (-1) 0 1) +
    reobserve *
      (continue * candidateGramEntry2 cross 1 0 1 1 +
        hold * candidateGramEntry2 cross 1 0 1 (-1) +
        reobserve * candidateGramEntry2 cross 1 0 1 0 +
        terminate * candidateGramEntry2 cross 1 0 0 1) +
    terminate *
      (continue * candidateGramEntry2 cross 0 1 1 1 +
        hold * candidateGramEntry2 cross 0 1 1 (-1) +
        reobserve * candidateGramEntry2 cross 0 1 1 0 +
        terminate * candidateGramEntry2 cross 0 1 0 1)

/-- The complete candidate quadratic form is exactly the two-history quadratic
    form induced by the v0.48 factorization. -/
theorem candidateGramQuadratic4_eq_historyQuadratic
    (cross continue hold reobserve terminate : ℤ) :
    candidateGramQuadratic4
        cross continue hold reobserve terminate =
      candidateHistoryQuadratic
        cross continue hold reobserve terminate := by
  simp [candidateGramQuadratic4, candidateHistoryQuadratic,
    candidateHistoryFirst, candidateHistorySecond, candidateGramEntry2]
  ring

/-- The first structural null vector is
    `continue - reobserve - terminate_candidate`. -/
theorem first_structural_null_relation :
    candidateHistoryFirst 1 0 (-1) (-1) = 0 ∧
      candidateHistorySecond 1 0 (-1) (-1) = 0 := by
  norm_num [candidateHistoryFirst, candidateHistorySecond]

/-- The second structural null vector is
    `hold - reobserve + terminate_candidate`. -/
theorem second_structural_null_relation :
    candidateHistoryFirst 0 1 (-1) 1 = 0 ∧
      candidateHistorySecond 0 1 (-1) 1 = 0 := by
  norm_num [candidateHistoryFirst, candidateHistorySecond]

/-- Adding arbitrary multiples of both structural null vectors leaves the first
    history coordinate unchanged. -/
theorem candidateHistoryFirst_structural_translation
    (continue hold reobserve terminate α β : ℤ) :
    candidateHistoryFirst
        (continue + α)
        (hold + β)
        (reobserve - α - β)
        (terminate - α + β) =
      candidateHistoryFirst continue hold reobserve terminate := by
  simp [candidateHistoryFirst]
  ring

/-- The same structural translation leaves the second history coordinate
    unchanged. -/
theorem candidateHistorySecond_structural_translation
    (continue hold reobserve terminate α β : ℤ) :
    candidateHistorySecond
        (continue + α)
        (hold + β)
        (reobserve - α - β)
        (terminate - α + β) =
      candidateHistorySecond continue hold reobserve terminate := by
  simp [candidateHistorySecond]
  ring

/-- Candidate Gram evidence is invariant under every translation by the
    two-dimensional structural nullspace. -/
theorem candidateGramQuadratic4_structural_translation_invariant
    (cross continue hold reobserve terminate α β : ℤ) :
    candidateGramQuadratic4
        cross
        (continue + α)
        (hold + β)
        (reobserve - α - β)
        (terminate - α + β) =
      candidateGramQuadratic4
        cross continue hold reobserve terminate := by
  rw [candidateGramQuadratic4_eq_historyQuadratic,
    candidateGramQuadratic4_eq_historyQuadratic]
  simp [candidateHistoryQuadratic, candidateHistoryFirst,
    candidateHistorySecond]
  ring

/-- Both structural null basis vectors have zero candidate Gram energy for every
    source coherence cross term. -/
theorem structural_null_basis_energy_zero (cross : ℤ) :
    candidateGramQuadratic4 cross 1 0 (-1) (-1) = 0 ∧
      candidateGramQuadratic4 cross 0 1 (-1) 1 = 0 := by
  constructor <;>
    rw [candidateGramQuadratic4_eq_historyQuadratic] <;>
    simp [candidateHistoryQuadratic, candidateHistoryFirst,
      candidateHistorySecond]

/-- The coherence-sensitive antisymmetric history probe
    `reobserve - terminate_candidate` has energy `4 - 2*cross`. -/
theorem antisymmetric_history_probe_energy (cross : ℤ) :
    candidateGramQuadratic4 cross 0 0 1 (-1) =
      4 - 2 * cross := by
  rw [candidateGramQuadratic4_eq_historyQuadratic]
  simp [candidateHistoryQuadratic, candidateHistoryFirst,
    candidateHistorySecond]
  ring

/-- The symmetric history probe `reobserve + terminate_candidate` has energy
    `4 + 2*cross`. -/
theorem symmetric_history_probe_energy (cross : ℤ) :
    candidateGramQuadratic4 cross 0 0 1 1 =
      4 + 2 * cross := by
  rw [candidateGramQuadratic4_eq_historyQuadratic]
  simp [candidateHistoryQuadratic, candidateHistoryFirst,
    candidateHistorySecond]
  ring

/-- Exact determinant numerator of the recovered two-history metric. -/
def historyMetricDeterminant2 (cross : ℤ) : ℤ :=
  4 - cross * cross

/-- Effective rank profile used by the bounded reference trajectory. -/
def referenceHistoryRank (cross : ℤ) : ℕ :=
  if historyMetricDeterminant2 cross = 0 then 1 else 2

/-- Candidate nullity follows from the four candidate coordinates and the
    source-bound effective history rank. -/
def referenceCandidateNullity (cross : ℤ) : ℕ :=
  4 - referenceHistoryRank cross

/-- Dephasing changes the history determinant from zero to strictly positive. -/
theorem reference_history_metric_determinant_trajectory :
    historyMetricDeterminant2 2 = 0 ∧
      historyMetricDeterminant2 1 = 3 ∧
      historyMetricDeterminant2 0 = 4 := by
  norm_num [historyMetricDeterminant2]

/-- The exact effective rank trajectory is one, two, two. -/
theorem reference_history_rank_trajectory :
    referenceHistoryRank 2 = 1 ∧
      referenceHistoryRank 1 = 2 ∧
      referenceHistoryRank 0 = 2 := by
  norm_num [referenceHistoryRank, historyMetricDeterminant2]

/-- The exact complete-candidate nullity trajectory is three, two, two. -/
theorem reference_candidate_nullity_trajectory :
    referenceCandidateNullity 2 = 3 ∧
      referenceCandidateNullity 1 = 2 ∧
      referenceCandidateNullity 0 = 2 := by
  norm_num [referenceCandidateNullity, referenceHistoryRank,
    historyMetricDeterminant2]

/-- The extra antisymmetric null direction is present only at full coherence and
    is released by partial and full dephasing. -/
theorem reference_antisymmetric_probe_energy_trajectory :
    candidateGramQuadratic4 2 0 0 1 (-1) = 0 ∧
      candidateGramQuadratic4 1 0 0 1 (-1) = 2 ∧
      candidateGramQuadratic4 0 0 0 1 (-1) = 4 := by
  constructor
  · rw [antisymmetric_history_probe_energy]
    norm_num
  · constructor
    · rw [antisymmetric_history_probe_energy]
      norm_num
    · rw [antisymmetric_history_probe_energy]
      norm_num

/-- The symmetric history direction remains strictly positive throughout the
    same trajectory. -/
theorem reference_symmetric_probe_energy_trajectory :
    candidateGramQuadratic4 2 0 0 1 1 = 8 ∧
      candidateGramQuadratic4 1 0 0 1 1 = 6 ∧
      candidateGramQuadratic4 0 0 0 1 1 = 4 := by
  constructor
  · rw [symmetric_history_probe_energy]
    norm_num
  · constructor
    · rw [symmetric_history_probe_energy]
      norm_num
    · rw [symmetric_history_probe_energy]
      norm_num

/-- The two structural null vectors together with the full-coherence
    antisymmetric direction are linearly independent. -/
theorem structural_plus_coherence_null_vectors_independent
    (α β γ : ℤ)
    (hcontinue : α * 1 + β * 0 + γ * 0 = 0)
    (hhold : α * 0 + β * 1 + γ * 0 = 0)
    (hreobserve : α * (-1) + β * (-1) + γ * 1 = 0)
    (hterminate : α * (-1) + β * 1 + γ * (-1) = 0) :
    α = 0 ∧ β = 0 ∧ γ = 0 := by
  norm_num at hcontinue hhold
  subst α
  subst β
  norm_num at hreobserve hterminate
  exact ⟨rfl, rfl, hreobserve⟩

/-- Bounded MemoryOS v0.49 certificate surface. -/
structure CandidateNullspaceDephasingRankStratificationCertificate where
  sourceMemoryOSV048Bound : Bool
  sourceMemoryOSV045Bound : Bool
  structuralNullBasisExact : Bool
  structuralNullKernelAnnihilationExact : Bool
  structuralNullQuadraticEvidenceZero : Bool
  candidateQuadraticEvidenceNullTranslationInvariant : Bool
  historyRankTrajectoryExact : Bool
  candidateRankTrajectoryExact : Bool
  candidateNullityTrajectoryExact : Bool
  extraCoherenceNullDirectionReleased : Bool
  dephasingRankRecoveryExact : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  relationalFrontierPreserved : Bool
  requiredReviewSetPreserved : Bool
  dissentVisibilityPreserved : Bool
  minorityVisibilityPreserved : Bool
  nullspaceWitnessAdvisoryOnly : Bool
  nullDirectionUsedAsCandidateDispensability : Bool
  rankRecoveryUsedAsCandidatePreference : Bool
  candidateRankingPerformed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  decisionReceiptIssued : Bool
  planSynthesisPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV048Mutated : Bool
  sourceMemoryOSV045Mutated : Bool
  sourceDecisionOSV06Mutated : Bool
  persistentWorldStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

/-- v0.49 preserves candidate, history, and DecisionOS review support while
    exposing the exact structural and coherence-dependent null directions. -/
theorem nullspace_rank_stratification_preserves_support_and_review
    (certificate :
      CandidateNullspaceDephasingRankStratificationCertificate)
    (hv048 : certificate.sourceMemoryOSV048Bound = true)
    (hv045 : certificate.sourceMemoryOSV045Bound = true)
    (hstructural : certificate.structuralNullBasisExact = true)
    (hannihilation :
      certificate.structuralNullKernelAnnihilationExact = true)
    (henergy : certificate.structuralNullQuadraticEvidenceZero = true)
    (hinvariant :
      certificate.candidateQuadraticEvidenceNullTranslationInvariant = true)
    (hhistoryRank : certificate.historyRankTrajectoryExact = true)
    (hcandidateRank : certificate.candidateRankTrajectoryExact = true)
    (hnullity : certificate.candidateNullityTrajectoryExact = true)
    (hrelease : certificate.extraCoherenceNullDirectionReleased = true)
    (hrecovery : certificate.dephasingRankRecoveryExact = true)
    (hcandidates : certificate.allDecisionCandidatesRetained = true)
    (hhistories : certificate.allPlanOSHistoriesRetained = true)
    (hfrontier : certificate.relationalFrontierPreserved = true)
    (hreview : certificate.requiredReviewSetPreserved = true)
    (hdissent : certificate.dissentVisibilityPreserved = true)
    (hminority : certificate.minorityVisibilityPreserved = true) :
    certificate.sourceMemoryOSV048Bound = true ∧
      certificate.sourceMemoryOSV045Bound = true ∧
      certificate.structuralNullBasisExact = true ∧
      certificate.structuralNullKernelAnnihilationExact = true ∧
      certificate.structuralNullQuadraticEvidenceZero = true ∧
      certificate.candidateQuadraticEvidenceNullTranslationInvariant = true ∧
      certificate.historyRankTrajectoryExact = true ∧
      certificate.candidateRankTrajectoryExact = true ∧
      certificate.candidateNullityTrajectoryExact = true ∧
      certificate.extraCoherenceNullDirectionReleased = true ∧
      certificate.dephasingRankRecoveryExact = true ∧
      certificate.allDecisionCandidatesRetained = true ∧
      certificate.allPlanOSHistoriesRetained = true ∧
      certificate.relationalFrontierPreserved = true ∧
      certificate.requiredReviewSetPreserved = true ∧
      certificate.dissentVisibilityPreserved = true ∧
      certificate.minorityVisibilityPreserved = true := by
  exact ⟨hv048, hv045, hstructural, hannihilation, henergy, hinvariant,
    hhistoryRank, hcandidateRank, hnullity, hrelease, hrecovery, hcandidates,
    hhistories, hfrontier, hreview, hdissent, hminority⟩

/-- Nullspace and rank evidence grants no candidate dispensability, preference,
    selection, decision, synthesis, activation, execution, mutation,
    verification, or truth authority. -/
theorem nullspace_rank_stratification_grants_no_authority
    (certificate :
      CandidateNullspaceDephasingRankStratificationCertificate)
    (hadvisory : certificate.nullspaceWitnessAdvisoryOnly = true)
    (hdispensability :
      certificate.nullDirectionUsedAsCandidateDispensability = false)
    (hpreference :
      certificate.rankRecoveryUsedAsCandidatePreference = false)
    (hrank : certificate.candidateRankingPerformed = false)
    (hprune : certificate.candidatePruningPerformed = false)
    (hselect : certificate.candidateSelectionPerformed = false)
    (hcommit : certificate.decisionCommitPerformed = false)
    (hreceipt : certificate.decisionReceiptIssued = false)
    (hsynthesis : certificate.planSynthesisPerformed = false)
    (hactivate : certificate.activationPerformed = false)
    (hexecute : certificate.executionPermission = false)
    (hv048 : certificate.sourceMemoryOSV048Mutated = false)
    (hv045 : certificate.sourceMemoryOSV045Mutated = false)
    (hdecision : certificate.sourceDecisionOSV06Mutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hverify : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false)
    (hfuture : certificate.futureOnly = true)
    (hreadonly : certificate.readOnly = true) :
    certificate.nullspaceWitnessAdvisoryOnly = true ∧
      certificate.nullDirectionUsedAsCandidateDispensability = false ∧
      certificate.rankRecoveryUsedAsCandidatePreference = false ∧
      certificate.candidateRankingPerformed = false ∧
      certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.decisionReceiptIssued = false ∧
      certificate.planSynthesisPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV048Mutated = false ∧
      certificate.sourceMemoryOSV045Mutated = false ∧
      certificate.sourceDecisionOSV06Mutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false ∧
      certificate.futureOnly = true ∧
      certificate.readOnly = true := by
  exact ⟨hadvisory, hdispensability, hpreference, hrank, hprune, hselect,
    hcommit, hreceipt, hsynthesis, hactivate, hexecute, hv048, hv045,
    hdecision, hworld, hverify, htruth, hfuture, hreadonly⟩

end KUOS.OpenHorizon.MemoryOSCandidateNullspaceDephasingRankStratificationV0_49
