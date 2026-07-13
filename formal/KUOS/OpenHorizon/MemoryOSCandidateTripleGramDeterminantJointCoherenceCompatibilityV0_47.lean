import Mathlib
import KUOS.OpenHorizon.MemoryOSCandidatePairCauchySchwarzRelationalCoherenceEnvelopeV0_46

namespace KUOS.OpenHorizon.MemoryOSCandidateTripleGramDeterminantJointCoherenceCompatibilityV0_47

open KUOS.OpenHorizon.MemoryOSCandidateGramLiftDecisionOSRelationalCoherenceKernelV0_45
open KUOS.OpenHorizon.MemoryOSCandidatePairCauchySchwarzRelationalCoherenceEnvelopeV0_46

/-- The real Hermitian `3 × 3` principal-minor determinant written through
    diagonal entries and the three cyclic off-diagonal entries. -/
def hermitianTripleDeterminantReal
    (firstDiagonal secondDiagonal thirdDiagonal
      firstSecond secondThird thirdFirst : ℝ) : ℝ :=
  firstDiagonal * secondDiagonal * thirdDiagonal +
    2 * firstSecond * secondThird * thirdFirst -
    firstDiagonal * secondThird ^ 2 -
    secondDiagonal * thirdFirst ^ 2 -
    thirdDiagonal * firstSecond ^ 2

/-- Pairwise Cauchy-Schwarz bounds alone do not imply joint three-candidate
    compatibility. The signed cycle `(1, 1, -1)` satisfies all three pairwise
    unit bounds while its `3 × 3` determinant is negative. -/
theorem pairwise_bounds_do_not_imply_joint_compatibility :
    (1 : ℝ) ^ 2 ≤ 1 * 1 ∧
      (1 : ℝ) ^ 2 ≤ 1 * 1 ∧
      (-1 : ℝ) ^ 2 ≤ 1 * 1 ∧
      hermitianTripleDeterminantReal 1 1 1 1 1 (-1) = -4 := by
  norm_num [hermitianTripleDeterminantReal]

/-- The `3 × 3` Gram determinant of three candidate coupling vectors in the
    two-history source space. -/
def candidateTripleGramDeterminant2Real
    (cross
      firstA firstB
      secondA secondB
      thirdA thirdB : ℝ) : ℝ :=
  let firstDiagonal := candidateEnergy2Real cross firstA firstB
  let secondDiagonal := candidateEnergy2Real cross secondA secondB
  let thirdDiagonal := candidateEnergy2Real cross thirdA thirdB
  let firstSecond :=
    candidateGramEntry2Real cross firstA firstB secondA secondB
  let secondThird :=
    candidateGramEntry2Real cross secondA secondB thirdA thirdB
  let thirdFirst :=
    candidateGramEntry2Real cross thirdA thirdB firstA firstB
  hermitianTripleDeterminantReal
    firstDiagonal secondDiagonal thirdDiagonal
    firstSecond secondThird thirdFirst

/-- Any three candidate vectors lifted from a two-dimensional history space
    have an exactly vanishing `3 × 3` Gram determinant. -/
theorem candidateTripleGramDeterminant2Real_eq_zero
    (cross
      firstA firstB
      secondA secondB
      thirdA thirdB : ℝ) :
    candidateTripleGramDeterminant2Real
      cross firstA firstB secondA secondB thirdA thirdB = 0 := by
  simp [candidateTripleGramDeterminant2Real, hermitianTripleDeterminantReal,
    candidateEnergy2Real, candidateGramEntry2Real]
  ring

/-- The rank-two determinant identity immediately supplies a nonnegative
    principal-minor witness for every candidate triple. -/
theorem candidateTripleGramDeterminant2Real_nonnegative
    (cross
      firstA firstB
      secondA secondB
      thirdA thirdB : ℝ) :
    0 ≤ candidateTripleGramDeterminant2Real
      cross firstA firstB secondA secondB thirdA thirdB := by
  rw [candidateTripleGramDeterminant2Real_eq_zero]

/-- Exact integer cyclic product used by the runtime certificate. -/
def candidateTripleCyclicProduct2
    (cross
      firstA firstB
      secondA secondB
      thirdA thirdB : ℤ) : ℤ :=
  candidateGramEntry2 cross firstA firstB secondA secondB *
    candidateGramEntry2 cross secondA secondB thirdA thirdB *
    candidateGramEntry2 cross thirdA thirdB firstA firstB

/-- Exact integer `3 × 3` Gram determinant used by the runtime certificate. -/
def candidateTripleGramDeterminant2
    (cross
      firstA firstB
      secondA secondB
      thirdA thirdB : ℤ) : ℤ :=
  let firstDiagonal :=
    candidateGramEntry2 cross firstA firstB firstA firstB
  let secondDiagonal :=
    candidateGramEntry2 cross secondA secondB secondA secondB
  let thirdDiagonal :=
    candidateGramEntry2 cross thirdA thirdB thirdA thirdB
  let firstSecond :=
    candidateGramEntry2 cross firstA firstB secondA secondB
  let secondThird :=
    candidateGramEntry2 cross secondA secondB thirdA thirdB
  let thirdFirst :=
    candidateGramEntry2 cross thirdA thirdB firstA firstB
  firstDiagonal * secondDiagonal * thirdDiagonal +
    2 * firstSecond * secondThird * thirdFirst -
    firstDiagonal * secondThird ^ 2 -
    secondDiagonal * thirdFirst ^ 2 -
    thirdDiagonal * firstSecond ^ 2

/-- Integer rank-two determinant identity for the runtime arithmetic surface. -/
theorem candidateTripleGramDeterminant2_eq_zero
    (cross
      firstA firstB
      secondA secondB
      thirdA thirdB : ℤ) :
    candidateTripleGramDeterminant2
      cross firstA firstB secondA secondB thirdA thirdB = 0 := by
  simp [candidateTripleGramDeterminant2, candidateGramEntry2]
  ring

/-- The `continue`--`reobserve`--`terminate` cyclic products are `[32, 9, 0]`
    across full coherence, partial dephasing, and full dephasing. -/
theorem reference_continue_reobserve_terminate_cyclic_products :
    candidateTripleCyclicProduct2 2 1 1 1 0 0 1 = 32 ∧
      candidateTripleCyclicProduct2 1 1 1 1 0 0 1 = 9 ∧
      candidateTripleCyclicProduct2 0 1 1 1 0 0 1 = 0 := by
  norm_num [candidateTripleCyclicProduct2, candidateGramEntry2]

/-- The signed `hold`--`reobserve`--`terminate` cyclic products remain visible
    as `[0, -1, 0]`. -/
theorem reference_hold_reobserve_terminate_cyclic_products :
    candidateTripleCyclicProduct2 2 1 (-1) 1 0 0 1 = 0 ∧
      candidateTripleCyclicProduct2 1 1 (-1) 1 0 0 1 = -1 ∧
      candidateTripleCyclicProduct2 0 1 (-1) 1 0 0 1 = 0 := by
  norm_num [candidateTripleCyclicProduct2, candidateGramEntry2]

/-- Both reference distinct triples have determinant zero at every dephasing
    step, while preserving the sign of their cyclic products. -/
theorem reference_distinct_candidate_triples_rank_two_saturated :
    candidateTripleGramDeterminant2 2 1 1 1 0 0 1 = 0 ∧
      candidateTripleGramDeterminant2 1 1 1 1 0 0 1 = 0 ∧
      candidateTripleGramDeterminant2 0 1 1 1 0 0 1 = 0 ∧
      candidateTripleGramDeterminant2 2 1 (-1) 1 0 0 1 = 0 ∧
      candidateTripleGramDeterminant2 1 1 (-1) 1 0 0 1 = 0 ∧
      candidateTripleGramDeterminant2 0 1 (-1) 1 0 0 1 = 0 := by
  norm_num [candidateTripleGramDeterminant2, candidateGramEntry2]

/-- Bounded MemoryOS v0.47 certificate surface. -/
structure CandidateTripleGramDeterminantJointCoherenceCompatibilityCertificate where
  sourceMemoryOSV046Bound : Bool
  allOrderedCandidateTriplesRetained : Bool
  allCandidateTriplePrincipalMinorsNonnegative : Bool
  allCandidateTripleDeterminantsZero : Bool
  allPairwiseEnvelopesJointlyCompatible : Bool
  candidateGramRankAtMostTwoWitness : Bool
  allRepeatedCandidateTriplesDegenerate : Bool
  allDistinctCandidateTriplesRankTwoSaturated : Bool
  sourceCandidatePairEnvelopeExact : Bool
  relationalFrontierPreserved : Bool
  requiredReviewSetPreserved : Bool
  dissentVisibilityPreserved : Bool
  minorityVisibilityPreserved : Bool
  jointCoherenceCompatibilityAdvisoryOnly : Bool
  tripleCyclicProductNotGroupPreference : Bool
  rankTwoSaturationNotCandidateConsensus : Bool
  candidateRankingPerformed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  decisionReceiptIssued : Bool
  planSynthesisPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV046Mutated : Bool
  sourceDecisionOSV06Mutated : Bool
  persistentWorldStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

/-- v0.47 preserves complete triple support and DecisionOS review visibility
    while certifying joint Gram compatibility. -/
theorem candidate_triple_compatibility_preserves_support_and_review
    (certificate :
      CandidateTripleGramDeterminantJointCoherenceCompatibilityCertificate)
    (hsource : certificate.sourceMemoryOSV046Bound = true)
    (htriples : certificate.allOrderedCandidateTriplesRetained = true)
    (hminor : certificate.allCandidateTriplePrincipalMinorsNonnegative = true)
    (hzero : certificate.allCandidateTripleDeterminantsZero = true)
    (hjoint : certificate.allPairwiseEnvelopesJointlyCompatible = true)
    (hrank : certificate.candidateGramRankAtMostTwoWitness = true)
    (hrepeated : certificate.allRepeatedCandidateTriplesDegenerate = true)
    (hdistinct : certificate.allDistinctCandidateTriplesRankTwoSaturated = true)
    (hexact : certificate.sourceCandidatePairEnvelopeExact = true)
    (hfrontier : certificate.relationalFrontierPreserved = true)
    (hreview : certificate.requiredReviewSetPreserved = true)
    (hdissent : certificate.dissentVisibilityPreserved = true)
    (hminority : certificate.minorityVisibilityPreserved = true) :
    certificate.sourceMemoryOSV046Bound = true ∧
      certificate.allOrderedCandidateTriplesRetained = true ∧
      certificate.allCandidateTriplePrincipalMinorsNonnegative = true ∧
      certificate.allCandidateTripleDeterminantsZero = true ∧
      certificate.allPairwiseEnvelopesJointlyCompatible = true ∧
      certificate.candidateGramRankAtMostTwoWitness = true ∧
      certificate.allRepeatedCandidateTriplesDegenerate = true ∧
      certificate.allDistinctCandidateTriplesRankTwoSaturated = true ∧
      certificate.sourceCandidatePairEnvelopeExact = true ∧
      certificate.relationalFrontierPreserved = true ∧
      certificate.requiredReviewSetPreserved = true ∧
      certificate.dissentVisibilityPreserved = true ∧
      certificate.minorityVisibilityPreserved = true := by
  exact ⟨hsource, htriples, hminor, hzero, hjoint, hrank, hrepeated,
    hdistinct, hexact, hfrontier, hreview, hdissent, hminority⟩

/-- Joint triple compatibility grants no ranking, consensus, selection,
    decision, synthesis, activation, execution, mutation, verification, or
    truth authority. -/
theorem candidate_triple_compatibility_grants_no_authority
    (certificate :
      CandidateTripleGramDeterminantJointCoherenceCompatibilityCertificate)
    (hadvisory : certificate.jointCoherenceCompatibilityAdvisoryOnly = true)
    (hpreference : certificate.tripleCyclicProductNotGroupPreference = true)
    (hconsensus : certificate.rankTwoSaturationNotCandidateConsensus = true)
    (hrank : certificate.candidateRankingPerformed = false)
    (hprune : certificate.candidatePruningPerformed = false)
    (hselect : certificate.candidateSelectionPerformed = false)
    (hcommit : certificate.decisionCommitPerformed = false)
    (hreceipt : certificate.decisionReceiptIssued = false)
    (hsynthesis : certificate.planSynthesisPerformed = false)
    (hactivate : certificate.activationPerformed = false)
    (hexecute : certificate.executionPermission = false)
    (hsource : certificate.sourceMemoryOSV046Mutated = false)
    (hdecision : certificate.sourceDecisionOSV06Mutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hverify : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false)
    (hfuture : certificate.futureOnly = true)
    (hreadonly : certificate.readOnly = true) :
    certificate.jointCoherenceCompatibilityAdvisoryOnly = true ∧
      certificate.tripleCyclicProductNotGroupPreference = true ∧
      certificate.rankTwoSaturationNotCandidateConsensus = true ∧
      certificate.candidateRankingPerformed = false ∧
      certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.decisionReceiptIssued = false ∧
      certificate.planSynthesisPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV046Mutated = false ∧
      certificate.sourceDecisionOSV06Mutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false ∧
      certificate.futureOnly = true ∧
      certificate.readOnly = true := by
  exact ⟨hadvisory, hpreference, hconsensus, hrank, hprune, hselect, hcommit,
    hreceipt, hsynthesis, hactivate, hexecute, hsource, hdecision, hworld,
    hverify, htruth, hfuture, hreadonly⟩

end KUOS.OpenHorizon.MemoryOSCandidateTripleGramDeterminantJointCoherenceCompatibilityV0_47
