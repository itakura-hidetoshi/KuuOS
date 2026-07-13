import Mathlib
import KUOS.OpenHorizon.MemoryOSCandidateTripleGramDeterminantJointCoherenceCompatibilityV0_47

namespace KUOS.OpenHorizon.MemoryOSTwoHistoryCandidateGramFactorizationReconstructionV0_48

open KUOS.OpenHorizon.MemoryOSCandidateGramLiftDecisionOSRelationalCoherenceKernelV0_45
open KUOS.OpenHorizon.MemoryOSCandidateTripleGramDeterminantJointCoherenceCompatibilityV0_47

/-- Exact two-history bilinear factorization used by the runtime certificate. -/
def twoHistoryFactorizedEntry2
    (k00 k01 k10 k11 leftA leftB rightA rightB : ℤ) : ℤ :=
  leftA * k00 * rightA +
    leftA * k01 * rightB +
    leftB * k10 * rightA +
    leftB * k11 * rightB

/-- The v0.45 reference candidate entry is exactly the explicit two-history
    factorization with source metric `[[2,cross],[cross,2]]`. -/
theorem candidateGramEntry2_eq_twoHistoryFactorization
    (cross leftA leftB rightA rightB : ℤ) :
    candidateGramEntry2 cross leftA leftB rightA rightB =
      twoHistoryFactorizedEntry2
        2 cross cross 2 leftA leftB rightA rightB := by
  simp [candidateGramEntry2, twoHistoryFactorizedEntry2]
  ring

/-- The `continue = reobserve + terminate_candidate` factor row reconstructs
    every candidate-kernel row. -/
theorem continue_row_reconstructed_from_history_anchors
    (cross rightA rightB : ℤ) :
    candidateGramEntry2 cross 1 1 rightA rightB =
      candidateGramEntry2 cross 1 0 rightA rightB +
        candidateGramEntry2 cross 0 1 rightA rightB := by
  simp [candidateGramEntry2]
  ring

/-- The `hold = reobserve - terminate_candidate` factor row reconstructs every
    candidate-kernel row, including the sign-sensitive partial-dephasing row. -/
theorem hold_row_reconstructed_from_history_anchors
    (cross rightA rightB : ℤ) :
    candidateGramEntry2 cross 1 (-1) rightA rightB =
      candidateGramEntry2 cross 1 0 rightA rightB -
        candidateGramEntry2 cross 0 1 rightA rightB := by
  simp [candidateGramEntry2]
  ring

/-- The same exact factor relations reconstruct every candidate-kernel column. -/
theorem continue_column_reconstructed_from_history_anchors
    (cross leftA leftB : ℤ) :
    candidateGramEntry2 cross leftA leftB 1 1 =
      candidateGramEntry2 cross leftA leftB 1 0 +
        candidateGramEntry2 cross leftA leftB 0 1 := by
  simp [candidateGramEntry2]
  ring

/-- The signed `hold` column is the difference of the two history-anchor
    columns. -/
theorem hold_column_reconstructed_from_history_anchors
    (cross leftA leftB : ℤ) :
    candidateGramEntry2 cross leftA leftB 1 (-1) =
      candidateGramEntry2 cross leftA leftB 1 0 -
        candidateGramEntry2 cross leftA leftB 0 1 := by
  simp [candidateGramEntry2]
  ring

/-- Row-major Leibniz determinant for a `4 × 4` integer matrix. -/
def determinant4
    (a00 a01 a02 a03
      a10 a11 a12 a13
      a20 a21 a22 a23
      a30 a31 a32 a33 : ℤ) : ℤ :=
  a00 * a11 * a22 * a33
    - a00 * a11 * a23 * a32
    - a00 * a12 * a21 * a33
    + a00 * a12 * a23 * a31
    + a00 * a13 * a21 * a32
    - a00 * a13 * a22 * a31
    - a01 * a10 * a22 * a33
    + a01 * a10 * a23 * a32
    + a01 * a12 * a20 * a33
    - a01 * a12 * a23 * a30
    - a01 * a13 * a20 * a32
    + a01 * a13 * a22 * a30
    + a02 * a10 * a21 * a33
    - a02 * a10 * a23 * a31
    - a02 * a11 * a20 * a33
    + a02 * a11 * a23 * a30
    + a02 * a13 * a20 * a31
    - a02 * a13 * a21 * a30
    - a03 * a10 * a21 * a32
    + a03 * a10 * a22 * a31
    + a03 * a11 * a20 * a32
    - a03 * a11 * a22 * a30
    - a03 * a12 * a20 * a31
    + a03 * a12 * a21 * a30

/-- Full four-candidate determinant in candidate order
    `continue, hold, reobserve, terminate_candidate`. -/
def referenceCandidateGramDeterminant4 (cross : ℤ) : ℤ :=
  determinant4
    (candidateGramEntry2 cross 1 1 1 1)
    (candidateGramEntry2 cross 1 1 1 (-1))
    (candidateGramEntry2 cross 1 1 1 0)
    (candidateGramEntry2 cross 1 1 0 1)
    (candidateGramEntry2 cross 1 (-1) 1 1)
    (candidateGramEntry2 cross 1 (-1) 1 (-1))
    (candidateGramEntry2 cross 1 (-1) 1 0)
    (candidateGramEntry2 cross 1 (-1) 0 1)
    (candidateGramEntry2 cross 1 0 1 1)
    (candidateGramEntry2 cross 1 0 1 (-1))
    (candidateGramEntry2 cross 1 0 1 0)
    (candidateGramEntry2 cross 1 0 0 1)
    (candidateGramEntry2 cross 0 1 1 1)
    (candidateGramEntry2 cross 0 1 1 (-1))
    (candidateGramEntry2 cross 0 1 1 0)
    (candidateGramEntry2 cross 0 1 0 1)

/-- The complete four-candidate Gram determinant vanishes for every source
    cross term because all four factor rows live in the same two-history space. -/
theorem referenceCandidateGramDeterminant4_eq_zero (cross : ℤ) :
    referenceCandidateGramDeterminant4 cross = 0 := by
  simp [referenceCandidateGramDeterminant4, determinant4, candidateGramEntry2]
  ring

/-- The source metric recovered from the history-anchor principal block follows
    the exact full-, partial-, and zero-coherence trajectory. -/
theorem reference_history_metric_anchor_trajectory :
    candidateGramEntry2 2 1 0 1 0 = 2 ∧
      candidateGramEntry2 2 1 0 0 1 = 2 ∧
      candidateGramEntry2 2 0 1 1 0 = 2 ∧
      candidateGramEntry2 2 0 1 0 1 = 2 ∧
      candidateGramEntry2 1 1 0 1 0 = 2 ∧
      candidateGramEntry2 1 1 0 0 1 = 1 ∧
      candidateGramEntry2 1 0 1 1 0 = 1 ∧
      candidateGramEntry2 1 0 1 0 1 = 2 ∧
      candidateGramEntry2 0 1 0 1 0 = 2 ∧
      candidateGramEntry2 0 1 0 0 1 = 0 ∧
      candidateGramEntry2 0 0 1 1 0 = 0 ∧
      candidateGramEntry2 0 0 1 0 1 = 2 := by
  norm_num [candidateGramEntry2]

/-- Bounded MemoryOS v0.48 certificate surface. -/
structure TwoHistoryCandidateGramFactorizationReconstructionCertificate where
  sourceMemoryOSV047Bound : Bool
  sourceMemoryOSV045Bound : Bool
  fixedCandidateHistoryFactorRowsExact : Bool
  allCandidateKernelEntriesReconstructed : Bool
  allCandidateRowRelationsExact : Bool
  allCandidateColumnRelationsExact : Bool
  allCandidateFourByFourDeterminantsZero : Bool
  allV047TripleRecordsBoundToFactorization : Bool
  candidateGramRankAtMostTwoByExplicitFactorization : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  relationalFrontierPreserved : Bool
  requiredReviewSetPreserved : Bool
  dissentVisibilityPreserved : Bool
  minorityVisibilityPreserved : Bool
  factorizationWitnessAdvisoryOnly : Bool
  historyCoordinateAnchorsUsedAsCandidatePriority : Bool
  rankFactorizationUsedAsCandidateConsensus : Bool
  candidateRankingPerformed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  decisionReceiptIssued : Bool
  planSynthesisPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV047Mutated : Bool
  sourceMemoryOSV045Mutated : Bool
  sourceDecisionOSV06Mutated : Bool
  persistentWorldStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

/-- v0.48 replaces determinant-only rank observation with a complete explicit
    two-history factorization and preserves every candidate and review surface. -/
theorem factorization_reconstruction_preserves_complete_support
    (certificate : TwoHistoryCandidateGramFactorizationReconstructionCertificate)
    (hv047 : certificate.sourceMemoryOSV047Bound = true)
    (hv045 : certificate.sourceMemoryOSV045Bound = true)
    (hfactors : certificate.fixedCandidateHistoryFactorRowsExact = true)
    (hentries : certificate.allCandidateKernelEntriesReconstructed = true)
    (hrows : certificate.allCandidateRowRelationsExact = true)
    (hcolumns : certificate.allCandidateColumnRelationsExact = true)
    (hdet : certificate.allCandidateFourByFourDeterminantsZero = true)
    (htriples : certificate.allV047TripleRecordsBoundToFactorization = true)
    (hrank : certificate.candidateGramRankAtMostTwoByExplicitFactorization = true)
    (hcandidates : certificate.allDecisionCandidatesRetained = true)
    (hhistories : certificate.allPlanOSHistoriesRetained = true)
    (hfrontier : certificate.relationalFrontierPreserved = true)
    (hreview : certificate.requiredReviewSetPreserved = true)
    (hdissent : certificate.dissentVisibilityPreserved = true)
    (hminority : certificate.minorityVisibilityPreserved = true) :
    certificate.sourceMemoryOSV047Bound = true ∧
      certificate.sourceMemoryOSV045Bound = true ∧
      certificate.fixedCandidateHistoryFactorRowsExact = true ∧
      certificate.allCandidateKernelEntriesReconstructed = true ∧
      certificate.allCandidateRowRelationsExact = true ∧
      certificate.allCandidateColumnRelationsExact = true ∧
      certificate.allCandidateFourByFourDeterminantsZero = true ∧
      certificate.allV047TripleRecordsBoundToFactorization = true ∧
      certificate.candidateGramRankAtMostTwoByExplicitFactorization = true ∧
      certificate.allDecisionCandidatesRetained = true ∧
      certificate.allPlanOSHistoriesRetained = true ∧
      certificate.relationalFrontierPreserved = true ∧
      certificate.requiredReviewSetPreserved = true ∧
      certificate.dissentVisibilityPreserved = true ∧
      certificate.minorityVisibilityPreserved = true := by
  exact ⟨hv047, hv045, hfactors, hentries, hrows, hcolumns, hdet, htriples,
    hrank, hcandidates, hhistories, hfrontier, hreview, hdissent, hminority⟩

/-- Explicit history coordinates are algebraic witnesses only. They grant no
    ranking, selection, decision, synthesis, activation, execution, mutation,
    verification, or truth authority. -/
theorem factorization_reconstruction_grants_no_authority
    (certificate : TwoHistoryCandidateGramFactorizationReconstructionCertificate)
    (hadvisory : certificate.factorizationWitnessAdvisoryOnly = true)
    (hpriority : certificate.historyCoordinateAnchorsUsedAsCandidatePriority = false)
    (hconsensus : certificate.rankFactorizationUsedAsCandidateConsensus = false)
    (hranking : certificate.candidateRankingPerformed = false)
    (hpruning : certificate.candidatePruningPerformed = false)
    (hselection : certificate.candidateSelectionPerformed = false)
    (hcommit : certificate.decisionCommitPerformed = false)
    (hreceipt : certificate.decisionReceiptIssued = false)
    (hsynthesis : certificate.planSynthesisPerformed = false)
    (hactivation : certificate.activationPerformed = false)
    (hexecution : certificate.executionPermission = false)
    (hv047 : certificate.sourceMemoryOSV047Mutated = false)
    (hv045 : certificate.sourceMemoryOSV045Mutated = false)
    (hdecision : certificate.sourceDecisionOSV06Mutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hverification : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false)
    (hfuture : certificate.futureOnly = true)
    (hreadonly : certificate.readOnly = true) :
    certificate.factorizationWitnessAdvisoryOnly = true ∧
      certificate.historyCoordinateAnchorsUsedAsCandidatePriority = false ∧
      certificate.rankFactorizationUsedAsCandidateConsensus = false ∧
      certificate.candidateRankingPerformed = false ∧
      certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.decisionReceiptIssued = false ∧
      certificate.planSynthesisPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV047Mutated = false ∧
      certificate.sourceMemoryOSV045Mutated = false ∧
      certificate.sourceDecisionOSV06Mutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false ∧
      certificate.futureOnly = true ∧
      certificate.readOnly = true := by
  exact ⟨hadvisory, hpriority, hconsensus, hranking, hpruning, hselection,
    hcommit, hreceipt, hsynthesis, hactivation, hexecution, hv047, hv045,
    hdecision, hworld, hverification, htruth, hfuture, hreadonly⟩

end KUOS.OpenHorizon.MemoryOSTwoHistoryCandidateGramFactorizationReconstructionV0_48
