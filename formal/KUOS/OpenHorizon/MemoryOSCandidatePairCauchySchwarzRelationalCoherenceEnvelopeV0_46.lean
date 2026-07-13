import Mathlib
import KUOS.OpenHorizon.MemoryOSCandidateGramLiftDecisionOSRelationalCoherenceKernelV0_45

namespace KUOS.OpenHorizon.MemoryOSCandidatePairCauchySchwarzRelationalCoherenceEnvelopeV0_46

open KUOS.OpenHorizon.MemoryOSCandidateGramLiftDecisionOSRelationalCoherenceKernelV0_45

/-- Real two-history candidate-pair Gram entry for the kernel
    `[[2, cross], [cross, 2]]`. -/
def candidateGramEntry2Real
    (cross leftA leftB rightA rightB : ℝ) : ℝ :=
  2 * leftA * rightA +
    cross * leftA * rightB +
    cross * leftB * rightA +
    2 * leftB * rightB

/-- Diagonal candidate energy induced by the two-history Gram kernel. -/
def candidateEnergy2Real (cross coefficientA coefficientB : ℝ) : ℝ :=
  candidateGramEntry2Real cross coefficientA coefficientB coefficientA coefficientB

/-- The exact two-dimensional Gram determinant identity. -/
theorem candidateGramDeterminantIdentity
    (cross leftA leftB rightA rightB : ℝ) :
    candidateEnergy2Real cross leftA leftB *
        candidateEnergy2Real cross rightA rightB -
      candidateGramEntry2Real cross leftA leftB rightA rightB ^ 2 =
      (4 - cross ^ 2) * (leftA * rightB - leftB * rightA) ^ 2 := by
  ring_nf
  rfl

/-- For every positive-semidefinite reference kernel (`-2 ≤ cross ≤ 2`), the
    candidate-pair Gram entry obeys the Cauchy-Schwarz bound. -/
theorem candidateGramEntry2Real_cauchySchwarz
    (cross leftA leftB rightA rightB : ℝ)
    (hlower : -2 ≤ cross)
    (hupper : cross ≤ 2) :
    candidateGramEntry2Real cross leftA leftB rightA rightB ^ 2 ≤
      candidateEnergy2Real cross leftA leftB *
        candidateEnergy2Real cross rightA rightB := by
  have hminus : 0 ≤ 2 - cross := by linarith
  have hplus : 0 ≤ 2 + cross := by linarith
  have hdet : 0 ≤ 4 - cross ^ 2 := by
    nlinarith [mul_nonneg hminus hplus]
  have hsquare : 0 ≤ (leftA * rightB - leftB * rightA) ^ 2 :=
    sq_nonneg _
  have hidentity :=
    candidateGramDeterminantIdentity cross leftA leftB rightA rightB
  nlinarith [mul_nonneg hdet hsquare]

/-- A zero diagonal energy forces every coherence entry incident to that
    candidate to vanish. -/
theorem zeroEnergy_forces_zeroCoherence
    (cross leftA leftB rightA rightB : ℝ)
    (hlower : -2 ≤ cross)
    (hupper : cross ≤ 2)
    (hzero : candidateEnergy2Real cross leftA leftB = 0) :
    candidateGramEntry2Real cross leftA leftB rightA rightB = 0 := by
  have hbound :=
    candidateGramEntry2Real_cauchySchwarz
      cross leftA leftB rightA rightB hlower hupper
  have hnonpositive :
      candidateGramEntry2Real cross leftA leftB rightA rightB ^ 2 ≤ 0 := by
    simpa [hzero] using hbound
  nlinarith [sq_nonneg (candidateGramEntry2Real cross leftA leftB rightA rightB)]

/-- Exact integer determinant margin used by the runtime certificate. -/
def candidatePairDeterminantMargin2
    (cross leftA leftB rightA rightB : ℤ) : ℤ :=
  candidateGramEntry2 cross leftA leftB leftA leftB *
      candidateGramEntry2 cross rightA rightB rightA rightB -
    candidateGramEntry2 cross leftA leftB rightA rightB ^ 2

/-- Cross-multiplied exact normalized-coherence-square equation. -/
def normalizedCoherenceSquareEquation
    (cross leftA leftB rightA rightB numerator denominator : ℤ) : Prop :=
  candidateGramEntry2 cross leftA leftB rightA rightB ^ 2 * denominator =
    candidateGramEntry2 cross leftA leftB leftA leftB *
      candidateGramEntry2 cross rightA rightB rightA rightB * numerator

/-- `continue` and `hold` have exact determinant margins `[0, 12, 16]`. -/
theorem reference_continue_hold_determinant_margins :
    candidatePairDeterminantMargin2 2 1 1 1 (-1) = 0 ∧
      candidatePairDeterminantMargin2 1 1 1 1 (-1) = 12 ∧
      candidatePairDeterminantMargin2 0 1 1 1 (-1) = 16 := by
  norm_num [candidatePairDeterminantMargin2, candidateGramEntry2]

/-- `continue` and `reobserve` have exact margins `[0, 3, 4]`. -/
theorem reference_continue_reobserve_determinant_margins :
    candidatePairDeterminantMargin2 2 1 1 1 0 = 0 ∧
      candidatePairDeterminantMargin2 1 1 1 1 0 = 3 ∧
      candidatePairDeterminantMargin2 0 1 1 1 0 = 4 := by
  norm_num [candidatePairDeterminantMargin2, candidateGramEntry2]

/-- The negative `hold`--`terminate` entries still have nonnegative determinant
    margins `[0, 3, 4]`. -/
theorem reference_hold_terminate_determinant_margins :
    candidatePairDeterminantMargin2 2 1 (-1) 0 1 = 0 ∧
      candidatePairDeterminantMargin2 1 1 (-1) 0 1 = 3 ∧
      candidatePairDeterminantMargin2 0 1 (-1) 0 1 = 4 := by
  norm_num [candidatePairDeterminantMargin2, candidateGramEntry2]

/-- `reobserve` and `terminate` have exact margins `[0, 3, 4]`. -/
theorem reference_reobserve_terminate_determinant_margins :
    candidatePairDeterminantMargin2 2 1 0 0 1 = 0 ∧
      candidatePairDeterminantMargin2 1 1 0 0 1 = 3 ∧
      candidatePairDeterminantMargin2 0 1 0 0 1 = 4 := by
  norm_num [candidatePairDeterminantMargin2, candidateGramEntry2]

/-- Exact normalized coherence squares for `continue`--`reobserve` are
    `[1, 3/4, 1/2]`. -/
theorem reference_continue_reobserve_normalized_square :
    normalizedCoherenceSquareEquation 2 1 1 1 0 1 1 ∧
      normalizedCoherenceSquareEquation 1 1 1 1 0 3 4 ∧
      normalizedCoherenceSquareEquation 0 1 1 1 0 1 2 := by
  norm_num [normalizedCoherenceSquareEquation, candidateGramEntry2]

/-- Exact normalized coherence squares for `hold`--`terminate` are
    `[0, 1/4, 1/2]`, despite the later raw entries being negative. -/
theorem reference_hold_terminate_normalized_square :
    normalizedCoherenceSquareEquation 2 1 (-1) 0 1 0 1 ∧
      normalizedCoherenceSquareEquation 1 1 (-1) 0 1 1 4 ∧
      normalizedCoherenceSquareEquation 0 1 (-1) 0 1 1 2 := by
  norm_num [normalizedCoherenceSquareEquation, candidateGramEntry2]

/-- Exact normalized coherence squares for `reobserve`--`terminate` are
    `[1, 1/4, 0]`. -/
theorem reference_reobserve_terminate_normalized_square :
    normalizedCoherenceSquareEquation 2 1 0 0 1 1 1 ∧
      normalizedCoherenceSquareEquation 1 1 0 0 1 1 4 ∧
      normalizedCoherenceSquareEquation 0 1 0 0 1 0 1 := by
  norm_num [normalizedCoherenceSquareEquation, candidateGramEntry2]

/-- Off-diagonal sign is retained but cannot be interpreted as preference. -/
theorem reference_negative_offdiagonal_sign_retained :
    candidateGramEntry2 2 1 (-1) 0 1 = 0 ∧
      candidateGramEntry2 1 1 (-1) 0 1 = -1 ∧
      candidateGramEntry2 0 1 (-1) 0 1 = -2 := by
  norm_num [candidateGramEntry2]

/-- Bounded MemoryOS v0.46 certificate surface. -/
structure CandidatePairCauchySchwarzRelationalCoherenceEnvelopeCertificate where
  sourceMemoryOSV045Bound : Bool
  allOrderedCandidatePairSupportRetained : Bool
  allCauchySchwarzBoundsHold : Bool
  allNormalizedCoherenceSquaresBoundedByOne : Bool
  allZeroDiagonalPairsHaveZeroCoherence : Bool
  allCandidateDiagonalsNonnegative : Bool
  sourceCandidateGramKernelExact : Bool
  relationalFrontierPreserved : Bool
  requiredReviewSetPreserved : Bool
  dissentVisibilityPreserved : Bool
  minorityVisibilityPreserved : Bool
  normalizedCoherenceAdvisoryOnly : Bool
  normalizedCoherenceUsedAsScalarUtility : Bool
  offDiagonalSignUsedAsPreference : Bool
  candidateRankingPerformed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  decisionReceiptIssued : Bool
  planSynthesisPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV045Mutated : Bool
  sourceDecisionOSV06Mutated : Bool
  persistentWorldStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

/-- v0.46 preserves exact pair support, Cauchy-Schwarz bounds, degenerate-pair
    behavior, and all DecisionOS relational review sets. -/
theorem candidate_pair_envelope_preserves_bounds_and_review
    (certificate : CandidatePairCauchySchwarzRelationalCoherenceEnvelopeCertificate)
    (hsource : certificate.sourceMemoryOSV045Bound = true)
    (hpairs : certificate.allOrderedCandidatePairSupportRetained = true)
    (hcs : certificate.allCauchySchwarzBoundsHold = true)
    (hnormalized : certificate.allNormalizedCoherenceSquaresBoundedByOne = true)
    (hzero : certificate.allZeroDiagonalPairsHaveZeroCoherence = true)
    (hdiagonal : certificate.allCandidateDiagonalsNonnegative = true)
    (hexact : certificate.sourceCandidateGramKernelExact = true)
    (hfrontier : certificate.relationalFrontierPreserved = true)
    (hreview : certificate.requiredReviewSetPreserved = true)
    (hdissent : certificate.dissentVisibilityPreserved = true)
    (hminority : certificate.minorityVisibilityPreserved = true) :
    certificate.sourceMemoryOSV045Bound = true ∧
      certificate.allOrderedCandidatePairSupportRetained = true ∧
      certificate.allCauchySchwarzBoundsHold = true ∧
      certificate.allNormalizedCoherenceSquaresBoundedByOne = true ∧
      certificate.allZeroDiagonalPairsHaveZeroCoherence = true ∧
      certificate.allCandidateDiagonalsNonnegative = true ∧
      certificate.sourceCandidateGramKernelExact = true ∧
      certificate.relationalFrontierPreserved = true ∧
      certificate.requiredReviewSetPreserved = true ∧
      certificate.dissentVisibilityPreserved = true ∧
      certificate.minorityVisibilityPreserved = true := by
  exact ⟨hsource, hpairs, hcs, hnormalized, hzero, hdiagonal, hexact,
    hfrontier, hreview, hdissent, hminority⟩

/-- The normalized envelope grants no utility, preference, ranking, selection,
    decision, synthesis, activation, execution, mutation, verification, or
    truth authority. -/
theorem candidate_pair_envelope_grants_no_authority
    (certificate : CandidatePairCauchySchwarzRelationalCoherenceEnvelopeCertificate)
    (hadvisory : certificate.normalizedCoherenceAdvisoryOnly = true)
    (hutility : certificate.normalizedCoherenceUsedAsScalarUtility = false)
    (hpreference : certificate.offDiagonalSignUsedAsPreference = false)
    (hrank : certificate.candidateRankingPerformed = false)
    (hprune : certificate.candidatePruningPerformed = false)
    (hselect : certificate.candidateSelectionPerformed = false)
    (hcommit : certificate.decisionCommitPerformed = false)
    (hreceipt : certificate.decisionReceiptIssued = false)
    (hsynthesis : certificate.planSynthesisPerformed = false)
    (hactivate : certificate.activationPerformed = false)
    (hexecute : certificate.executionPermission = false)
    (hsource : certificate.sourceMemoryOSV045Mutated = false)
    (hdecision : certificate.sourceDecisionOSV06Mutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hverify : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false)
    (hfuture : certificate.futureOnly = true)
    (hreadonly : certificate.readOnly = true) :
    certificate.normalizedCoherenceAdvisoryOnly = true ∧
      certificate.normalizedCoherenceUsedAsScalarUtility = false ∧
      certificate.offDiagonalSignUsedAsPreference = false ∧
      certificate.candidateRankingPerformed = false ∧
      certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.decisionReceiptIssued = false ∧
      certificate.planSynthesisPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV045Mutated = false ∧
      certificate.sourceDecisionOSV06Mutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false ∧
      certificate.futureOnly = true ∧
      certificate.readOnly = true := by
  exact ⟨hadvisory, hutility, hpreference, hrank, hprune, hselect, hcommit,
    hreceipt, hsynthesis, hactivate, hexecute, hsource, hdecision, hworld,
    hverify, htruth, hfuture, hreadonly⟩

end KUOS.OpenHorizon.MemoryOSCandidatePairCauchySchwarzRelationalCoherenceEnvelopeV0_46
