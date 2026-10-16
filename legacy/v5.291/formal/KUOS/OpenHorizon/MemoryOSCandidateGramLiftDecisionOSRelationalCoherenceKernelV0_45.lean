import Mathlib
import KUOS.OpenHorizon.MemoryOSObserverRelativeCoherenceQuadraticEvidenceDecisionOSHandoffV0_44

namespace KUOS.OpenHorizon.MemoryOSCandidateGramLiftDecisionOSRelationalCoherenceKernelV0_45

open scoped BigOperators ComplexConjugate
open KUOS.OpenHorizon.MemoryOSObserverRelativeNonMarkovInfluenceConditionedPlanOSCoherenceKernelV0_42

/-- Push a DecisionOS candidate-space vector through the complete candidate to
    PlanOS-history coupling field. -/
def liftCandidateVector
    {δ ι : Type} [Fintype δ]
    (coupling : δ → ι → ℂ)
    (vector : δ → ℂ) : ι → ℂ :=
  fun history => ∑ candidate, coupling candidate history * vector candidate

/-- Candidate-space Gram lift `C K C*` written in the row-vector convention
    used by the runtime certificate. -/
def candidateGramLift
    {δ ι : Type} [Fintype ι]
    (coupling : δ → ι → ℂ)
    (kernel : Matrix ι ι ℂ) : Matrix δ δ ℂ :=
  fun left right => ∑ row, ∑ column,
    star (coupling left row) * kernel row column * coupling right column

/-- Every diagonal entry of the candidate Gram lift is exactly the v0.44
    quadratic evidence of that candidate coupling vector. -/
theorem candidateGramLift_diagonal_eq_quadraticForm
    {δ ι : Type} [Fintype ι]
    (coupling : δ → ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (candidate : δ) :
    candidateGramLift coupling kernel candidate candidate =
      quadraticForm kernel (coupling candidate) := by
  rfl

/-- Candidate-space quadratic evaluation is source-kernel evaluation after the
    candidate vector is pushed through the complete coupling field. -/
theorem candidateGramLift_quadraticForm
    {δ ι : Type} [Fintype δ] [Fintype ι]
    (coupling : δ → ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (vector : δ → ℂ) :
    quadraticForm (candidateGramLift coupling kernel) vector =
      quadraticForm kernel (liftCandidateVector coupling vector) := by
  classical
  simp [quadraticForm, candidateGramLift, liftCandidateVector,
    Finset.mul_sum, Finset.sum_mul, mul_comm, mul_left_comm, mul_assoc,
    Finset.sum_comm]

/-- The complete candidate Gram lift of a PSD history kernel remains PSD. -/
theorem candidateGramLift_preserves_positiveSemidefinite
    {δ ι : Type} [Fintype δ] [Fintype ι]
    (coupling : δ → ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (hpsd : IsPositiveSemidefiniteKernel kernel) :
    IsPositiveSemidefiniteKernel (candidateGramLift coupling kernel) := by
  intro vector
  rw [candidateGramLift_quadraticForm]
  exact hpsd _

/-- In particular every candidate-kernel diagonal is nonnegative. -/
theorem candidateGramLift_diagonal_nonnegative
    {δ ι : Type} [Fintype ι]
    (coupling : δ → ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (hpsd : IsPositiveSemidefiniteKernel kernel)
    (candidate : δ) :
    0 ≤ (candidateGramLift coupling kernel candidate candidate).re := by
  rw [candidateGramLift_diagonal_eq_quadraticForm]
  exact hpsd _

/-- Exact two-history candidate-pair Gram entry for the reference kernel
    `[[2,cross],[cross,2]]`. -/
def candidateGramEntry2
    (cross leftA leftB rightA rightB : ℤ) : ℤ :=
  2 * leftA * rightA +
    cross * leftA * rightB +
    cross * leftB * rightA +
    2 * leftB * rightB

/-- The `continue = [1,1]` row of the candidate Gram kernel is exact at full
    coherence, partial dephasing, and full dephasing. -/
theorem reference_continue_candidate_gram_row :
    candidateGramEntry2 2 1 1 1 1 = 8 ∧
      candidateGramEntry2 2 1 1 1 (-1) = 0 ∧
      candidateGramEntry2 2 1 1 1 0 = 4 ∧
      candidateGramEntry2 2 1 1 0 1 = 4 ∧
      candidateGramEntry2 1 1 1 1 1 = 6 ∧
      candidateGramEntry2 1 1 1 1 (-1) = 0 ∧
      candidateGramEntry2 1 1 1 1 0 = 3 ∧
      candidateGramEntry2 1 1 1 0 1 = 3 ∧
      candidateGramEntry2 0 1 1 1 1 = 4 ∧
      candidateGramEntry2 0 1 1 1 (-1) = 0 ∧
      candidateGramEntry2 0 1 1 1 0 = 2 ∧
      candidateGramEntry2 0 1 1 0 1 = 2 := by
  norm_num [candidateGramEntry2]

/-- The `hold = [1,-1]` row contains both positive and negative pairwise
    coherence while its diagonal remains nonnegative. -/
theorem reference_hold_candidate_gram_row :
    candidateGramEntry2 2 1 (-1) 1 1 = 0 ∧
      candidateGramEntry2 2 1 (-1) 1 (-1) = 0 ∧
      candidateGramEntry2 2 1 (-1) 1 0 = 0 ∧
      candidateGramEntry2 2 1 (-1) 0 1 = 0 ∧
      candidateGramEntry2 1 1 (-1) 1 1 = 0 ∧
      candidateGramEntry2 1 1 (-1) 1 (-1) = 2 ∧
      candidateGramEntry2 1 1 (-1) 1 0 = 1 ∧
      candidateGramEntry2 1 1 (-1) 0 1 = -1 ∧
      candidateGramEntry2 0 1 (-1) 1 1 = 0 ∧
      candidateGramEntry2 0 1 (-1) 1 (-1) = 4 ∧
      candidateGramEntry2 0 1 (-1) 1 0 = 2 ∧
      candidateGramEntry2 0 1 (-1) 0 1 = -2 := by
  norm_num [candidateGramEntry2]

/-- The remaining pair trajectories expose the exact relational coherence
    values `[2,1,0]` without converting them into a candidate order. -/
theorem reference_reobserve_terminate_pair :
    candidateGramEntry2 2 1 0 0 1 = 2 ∧
      candidateGramEntry2 1 1 0 0 1 = 1 ∧
      candidateGramEntry2 0 1 0 0 1 = 0 := by
  norm_num [candidateGramEntry2]

/-- Bounded MemoryOS v0.45 certificate surface. -/
structure CandidateGramLiftDecisionOSRelationalCoherenceKernelCertificate where
  sourceMemoryOSV043Bound : Bool
  sourceMemoryOSV044Bound : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  allCandidatePairSupportRetained : Bool
  candidateKernelHermitian : Bool
  candidateKernelPositiveSemidefinite : Bool
  candidateDiagonalsMatchV044Evidence : Bool
  relationalFrontierPreserved : Bool
  requiredReviewSetPreserved : Bool
  dissentVisibilityPreserved : Bool
  minorityVisibilityPreserved : Bool
  candidatePairCoherenceAdvisoryOnly : Bool
  candidateGramKernelUsedAsRelationalOrder : Bool
  candidateRankingPerformed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  decisionReceiptIssued : Bool
  planSynthesisPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV043Mutated : Bool
  sourceMemoryOSV044Mutated : Bool
  sourceDecisionOSV06Mutated : Bool
  persistentWorldStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

/-- v0.45 preserves complete history, candidate, candidate-pair, and DecisionOS
    review support while lifting the source PSD kernel. -/
theorem candidate_gram_lift_preserves_support_and_review
    (certificate : CandidateGramLiftDecisionOSRelationalCoherenceKernelCertificate)
    (hv043 : certificate.sourceMemoryOSV043Bound = true)
    (hv044 : certificate.sourceMemoryOSV044Bound = true)
    (hcandidates : certificate.allDecisionCandidatesRetained = true)
    (hhistories : certificate.allPlanOSHistoriesRetained = true)
    (hpairs : certificate.allCandidatePairSupportRetained = true)
    (hhermitian : certificate.candidateKernelHermitian = true)
    (hpsd : certificate.candidateKernelPositiveSemidefinite = true)
    (hdiagonal : certificate.candidateDiagonalsMatchV044Evidence = true)
    (hfrontier : certificate.relationalFrontierPreserved = true)
    (hreview : certificate.requiredReviewSetPreserved = true)
    (hdissent : certificate.dissentVisibilityPreserved = true)
    (hminority : certificate.minorityVisibilityPreserved = true) :
    certificate.sourceMemoryOSV043Bound = true ∧
      certificate.sourceMemoryOSV044Bound = true ∧
      certificate.allDecisionCandidatesRetained = true ∧
      certificate.allPlanOSHistoriesRetained = true ∧
      certificate.allCandidatePairSupportRetained = true ∧
      certificate.candidateKernelHermitian = true ∧
      certificate.candidateKernelPositiveSemidefinite = true ∧
      certificate.candidateDiagonalsMatchV044Evidence = true ∧
      certificate.relationalFrontierPreserved = true ∧
      certificate.requiredReviewSetPreserved = true ∧
      certificate.dissentVisibilityPreserved = true ∧
      certificate.minorityVisibilityPreserved = true := by
  exact ⟨hv043, hv044, hcandidates, hhistories, hpairs, hhermitian, hpsd,
    hdiagonal, hfrontier, hreview, hdissent, hminority⟩

/-- Candidate relational coherence grants no ordering, ranking, selection,
    decision, synthesis, activation, execution, mutation, verification, or
    truth authority. -/
theorem candidate_gram_lift_grants_no_authority
    (certificate : CandidateGramLiftDecisionOSRelationalCoherenceKernelCertificate)
    (hadvisory : certificate.candidatePairCoherenceAdvisoryOnly = true)
    (horder : certificate.candidateGramKernelUsedAsRelationalOrder = false)
    (hrank : certificate.candidateRankingPerformed = false)
    (hprune : certificate.candidatePruningPerformed = false)
    (hselect : certificate.candidateSelectionPerformed = false)
    (hcommit : certificate.decisionCommitPerformed = false)
    (hreceipt : certificate.decisionReceiptIssued = false)
    (hsynthesis : certificate.planSynthesisPerformed = false)
    (hactivate : certificate.activationPerformed = false)
    (hexecute : certificate.executionPermission = false)
    (hv043 : certificate.sourceMemoryOSV043Mutated = false)
    (hv044 : certificate.sourceMemoryOSV044Mutated = false)
    (hdecision : certificate.sourceDecisionOSV06Mutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hverify : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false)
    (hfuture : certificate.futureOnly = true)
    (hreadonly : certificate.readOnly = true) :
    certificate.candidatePairCoherenceAdvisoryOnly = true ∧
      certificate.candidateGramKernelUsedAsRelationalOrder = false ∧
      certificate.candidateRankingPerformed = false ∧
      certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.decisionReceiptIssued = false ∧
      certificate.planSynthesisPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV043Mutated = false ∧
      certificate.sourceMemoryOSV044Mutated = false ∧
      certificate.sourceDecisionOSV06Mutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false ∧
      certificate.futureOnly = true ∧
      certificate.readOnly = true := by
  exact ⟨hadvisory, horder, hrank, hprune, hselect, hcommit, hreceipt,
    hsynthesis, hactivate, hexecute, hv043, hv044, hdecision, hworld, hverify,
    htruth, hfuture, hreadonly⟩

end KUOS.OpenHorizon.MemoryOSCandidateGramLiftDecisionOSRelationalCoherenceKernelV0_45
