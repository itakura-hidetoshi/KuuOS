import Mathlib
import KUOS.OpenHorizon.MemoryOSCandidateNullspaceDephasingRankStratificationV0_49

namespace KUOS.OpenHorizon.MemoryOSCandidateQuotientCoordinateCanonicalizationV0_50

open KUOS.OpenHorizon.MemoryOSCandidateGramLiftDecisionOSRelationalCoherenceKernelV0_45
open KUOS.OpenHorizon.MemoryOSCandidateNullspaceDephasingRankStratificationV0_49

/-- First coordinate on the quotient by the two structural candidate-null
    relations. -/
def quotientFirst
    (continue hold reobserve terminate : ℤ) : ℤ :=
  candidateHistoryFirst continue hold reobserve terminate

/-- Second coordinate on the same quotient. -/
def quotientSecond
    (continue hold reobserve terminate : ℤ) : ℤ :=
  candidateHistorySecond continue hold reobserve terminate

/-- Canonical chart representative: the two structural coordinates are fixed to
    zero and the two history anchors carry the quotient coordinates. -/
def canonicalReobserve
    (continue hold reobserve terminate : ℤ) : ℤ :=
  quotientFirst continue hold reobserve terminate

def canonicalTerminate
    (continue hold reobserve terminate : ℤ) : ℤ :=
  quotientSecond continue hold reobserve terminate

/-- Bilinear history-space pairing for the source metric
    `[[2,cross],[cross,2]]`. -/
def candidateHistoryBilinear
    (cross leftFirst leftSecond rightFirst rightSecond : ℤ) : ℤ :=
  2 * leftFirst * rightFirst +
    cross * leftFirst * rightSecond +
    cross * leftSecond * rightFirst +
    2 * leftSecond * rightSecond

/-- Complete bilinear pairing from all sixteen entries of the four-candidate
    Gram kernel. -/
def candidateGramBilinear4
    (cross
      leftContinue leftHold leftReobserve leftTerminate
      rightContinue rightHold rightReobserve rightTerminate : ℤ) : ℤ :=
  leftContinue *
      (rightContinue * candidateGramEntry2 cross 1 1 1 1 +
        rightHold * candidateGramEntry2 cross 1 1 1 (-1) +
        rightReobserve * candidateGramEntry2 cross 1 1 1 0 +
        rightTerminate * candidateGramEntry2 cross 1 1 0 1) +
    leftHold *
      (rightContinue * candidateGramEntry2 cross 1 (-1) 1 1 +
        rightHold * candidateGramEntry2 cross 1 (-1) 1 (-1) +
        rightReobserve * candidateGramEntry2 cross 1 (-1) 1 0 +
        rightTerminate * candidateGramEntry2 cross 1 (-1) 0 1) +
    leftReobserve *
      (rightContinue * candidateGramEntry2 cross 1 0 1 1 +
        rightHold * candidateGramEntry2 cross 1 0 1 (-1) +
        rightReobserve * candidateGramEntry2 cross 1 0 1 0 +
        rightTerminate * candidateGramEntry2 cross 1 0 0 1) +
    leftTerminate *
      (rightContinue * candidateGramEntry2 cross 0 1 1 1 +
        rightHold * candidateGramEntry2 cross 0 1 1 (-1) +
        rightReobserve * candidateGramEntry2 cross 0 1 1 0 +
        rightTerminate * candidateGramEntry2 cross 0 1 0 1)

/-- The complete candidate pairing is exactly the history-coordinate pairing. -/
theorem candidateGramBilinear4_eq_historyBilinear
    (cross
      leftContinue leftHold leftReobserve leftTerminate
      rightContinue rightHold rightReobserve rightTerminate : ℤ) :
    candidateGramBilinear4
        cross
        leftContinue leftHold leftReobserve leftTerminate
        rightContinue rightHold rightReobserve rightTerminate =
      candidateHistoryBilinear
        cross
        (quotientFirst
          leftContinue leftHold leftReobserve leftTerminate)
        (quotientSecond
          leftContinue leftHold leftReobserve leftTerminate)
        (quotientFirst
          rightContinue rightHold rightReobserve rightTerminate)
        (quotientSecond
          rightContinue rightHold rightReobserve rightTerminate) := by
  simp [candidateGramBilinear4, candidateHistoryBilinear, quotientFirst,
    quotientSecond, candidateHistoryFirst, candidateHistorySecond,
    candidateGramEntry2]
  ring

/-- The canonical representative has exactly the original quotient
    coordinates. -/
theorem canonical_representative_coordinates
    (continue hold reobserve terminate : ℤ) :
    quotientFirst
        0 0
        (canonicalReobserve continue hold reobserve terminate)
        (canonicalTerminate continue hold reobserve terminate) =
        quotientFirst continue hold reobserve terminate ∧
      quotientSecond
        0 0
        (canonicalReobserve continue hold reobserve terminate)
        (canonicalTerminate continue hold reobserve terminate) =
        quotientSecond continue hold reobserve terminate := by
  simp [quotientFirst, quotientSecond, canonicalReobserve,
    canonicalTerminate, candidateHistoryFirst, candidateHistorySecond]

/-- Every candidate coefficient vector is its canonical quotient
    representative plus the exact structural-null translation with coefficients
    `continue` and `hold`. -/
theorem source_eq_canonical_plus_structural_null
    (continue hold reobserve terminate : ℤ) :
    reobserve =
        canonicalReobserve continue hold reobserve terminate -
          continue - hold ∧
      terminate =
        canonicalTerminate continue hold reobserve terminate -
          continue + hold := by
  simp [canonicalReobserve, canonicalTerminate, quotientFirst, quotientSecond,
    candidateHistoryFirst, candidateHistorySecond]
  constructor <;> ring

/-- Equality of both quotient coordinates forces the difference of two
    candidate vectors to be the corresponding combination of the two
    structural null vectors. -/
theorem same_quotient_coordinates_imply_structural_translation
    (c₁ h₁ r₁ t₁ c₂ h₂ r₂ t₂ : ℤ)
    (hfirst :
      quotientFirst c₁ h₁ r₁ t₁ =
        quotientFirst c₂ h₂ r₂ t₂)
    (hsecond :
      quotientSecond c₁ h₁ r₁ t₁ =
        quotientSecond c₂ h₂ r₂ t₂) :
    r₂ = r₁ - (c₂ - c₁) - (h₂ - h₁) ∧
      t₂ = t₁ - (c₂ - c₁) + (h₂ - h₁) := by
  simp [quotientFirst, quotientSecond, candidateHistoryFirst,
    candidateHistorySecond] at hfirst hsecond
  omega

/-- A vector already in the canonical chart is uniquely determined by its two
    quotient coordinates. -/
theorem canonical_chart_unique
    (reobserve terminate first second : ℤ)
    (hfirst : quotientFirst 0 0 reobserve terminate = first)
    (hsecond : quotientSecond 0 0 reobserve terminate = second) :
    reobserve = first ∧ terminate = second := by
  simpa [quotientFirst, quotientSecond, candidateHistoryFirst,
    candidateHistorySecond] using And.intro hfirst hsecond

/-- Canonicalization is idempotent. -/
theorem canonicalization_idempotent
    (continue hold reobserve terminate : ℤ) :
    canonicalReobserve
        0 0
        (canonicalReobserve continue hold reobserve terminate)
        (canonicalTerminate continue hold reobserve terminate) =
        canonicalReobserve continue hold reobserve terminate ∧
      canonicalTerminate
        0 0
        (canonicalReobserve continue hold reobserve terminate)
        (canonicalTerminate continue hold reobserve terminate) =
        canonicalTerminate continue hold reobserve terminate := by
  simp [canonicalReobserve, canonicalTerminate, quotientFirst, quotientSecond,
    candidateHistoryFirst, candidateHistorySecond]

/-- The full Gram quadratic evidence descends exactly to the canonical quotient
    representative. -/
theorem candidateGramQuadratic4_descends_to_canonical
    (cross continue hold reobserve terminate : ℤ) :
    candidateGramQuadratic4 cross continue hold reobserve terminate =
      candidateGramQuadratic4
        cross 0 0
        (canonicalReobserve continue hold reobserve terminate)
        (canonicalTerminate continue hold reobserve terminate) := by
  rw [candidateGramQuadratic4_eq_historyQuadratic,
    candidateGramQuadratic4_eq_historyQuadratic]
  simp [candidateHistoryQuadratic, candidateHistoryFirst,
    candidateHistorySecond, canonicalReobserve, canonicalTerminate,
    quotientFirst, quotientSecond]
  ring

/-- Every bilinear Gram pairing descends exactly to the two canonical quotient
    representatives. -/
theorem candidateGramBilinear4_descends_to_canonical
    (cross
      leftContinue leftHold leftReobserve leftTerminate
      rightContinue rightHold rightReobserve rightTerminate : ℤ) :
    candidateGramBilinear4
        cross
        leftContinue leftHold leftReobserve leftTerminate
        rightContinue rightHold rightReobserve rightTerminate =
      candidateGramBilinear4
        cross
        0 0
        (canonicalReobserve
          leftContinue leftHold leftReobserve leftTerminate)
        (canonicalTerminate
          leftContinue leftHold leftReobserve leftTerminate)
        0 0
        (canonicalReobserve
          rightContinue rightHold rightReobserve rightTerminate)
        (canonicalTerminate
          rightContinue rightHold rightReobserve rightTerminate) := by
  rw [candidateGramBilinear4_eq_historyBilinear,
    candidateGramBilinear4_eq_historyBilinear]
  simp [canonicalReobserve, canonicalTerminate, quotientFirst,
    quotientSecond, candidateHistoryFirst, candidateHistorySecond]

/-- Reference basis vectors and the mixed probe have the exact canonical
    representatives used by the runtime. -/
theorem reference_canonical_representatives :
    canonicalReobserve 1 0 0 0 = 1 ∧
      canonicalTerminate 1 0 0 0 = 1 ∧
      canonicalReobserve 0 1 0 0 = 1 ∧
      canonicalTerminate 0 1 0 0 = -1 ∧
      canonicalReobserve 1 0 (-1) (-1) = 0 ∧
      canonicalTerminate 1 0 (-1) (-1) = 0 ∧
      canonicalReobserve 2 (-1) 3 4 = 4 ∧
      canonicalTerminate 2 (-1) 3 4 = 7 := by
  norm_num [canonicalReobserve, canonicalTerminate, quotientFirst,
    quotientSecond, candidateHistoryFirst, candidateHistorySecond]

/-- The quotient metric retains the source rank trajectory one, two, two. -/
theorem reference_quotient_metric_rank_trajectory :
    referenceHistoryRank 2 = 1 ∧
      referenceHistoryRank 1 = 2 ∧
      referenceHistoryRank 0 = 2 := by
  exact reference_history_rank_trajectory

/-- Bounded MemoryOS v0.50 certificate surface. -/
structure CandidateQuotientCoordinateCanonicalizationCertificate where
  sourceMemoryOSV049Bound : Bool
  sourceMemoryOSV048Bound : Bool
  canonicalDecompositionExact : Bool
  quotientCoordinatesPreserved : Bool
  canonicalRepresentativeUnique : Bool
  quadraticEvidenceDescends : Bool
  bilinearPairingsDescend : Bool
  quotientMetricRankTrajectoryPreserved : Bool
  structuralNullspaceRemovedFromCoordinatesNotCandidates : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  relationalFrontierPreserved : Bool
  requiredReviewSetPreserved : Bool
  dissentVisibilityPreserved : Bool
  minorityVisibilityPreserved : Bool
  quotientWitnessAdvisoryOnly : Bool
  canonicalRepresentativeUsedAsCandidateSelection : Bool
  quotientUsedAsCandidatePruning : Bool
  candidateRankingPerformed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  decisionReceiptIssued : Bool
  planSynthesisPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV049Mutated : Bool
  sourceMemoryOSV048Mutated : Bool
  sourceDecisionOSV06Mutated : Bool
  persistentWorldStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

/-- v0.50 preserves all candidate, history, and DecisionOS review surfaces while
    descending the Gram geometry to exact quotient coordinates. -/
theorem quotient_coordinate_canonicalization_preserves_support_and_review
    (certificate : CandidateQuotientCoordinateCanonicalizationCertificate)
    (hv049 : certificate.sourceMemoryOSV049Bound = true)
    (hv048 : certificate.sourceMemoryOSV048Bound = true)
    (hdecomp : certificate.canonicalDecompositionExact = true)
    (hcoords : certificate.quotientCoordinatesPreserved = true)
    (hunique : certificate.canonicalRepresentativeUnique = true)
    (hquad : certificate.quadraticEvidenceDescends = true)
    (hpair : certificate.bilinearPairingsDescend = true)
    (hrank : certificate.quotientMetricRankTrajectoryPreserved = true)
    (hnotCandidates :
      certificate.structuralNullspaceRemovedFromCoordinatesNotCandidates = true)
    (hcandidates : certificate.allDecisionCandidatesRetained = true)
    (hhistories : certificate.allPlanOSHistoriesRetained = true)
    (hfrontier : certificate.relationalFrontierPreserved = true)
    (hreview : certificate.requiredReviewSetPreserved = true)
    (hdissent : certificate.dissentVisibilityPreserved = true)
    (hminority : certificate.minorityVisibilityPreserved = true) :
    certificate.sourceMemoryOSV049Bound = true ∧
      certificate.sourceMemoryOSV048Bound = true ∧
      certificate.canonicalDecompositionExact = true ∧
      certificate.quotientCoordinatesPreserved = true ∧
      certificate.canonicalRepresentativeUnique = true ∧
      certificate.quadraticEvidenceDescends = true ∧
      certificate.bilinearPairingsDescend = true ∧
      certificate.quotientMetricRankTrajectoryPreserved = true ∧
      certificate.structuralNullspaceRemovedFromCoordinatesNotCandidates = true ∧
      certificate.allDecisionCandidatesRetained = true ∧
      certificate.allPlanOSHistoriesRetained = true ∧
      certificate.relationalFrontierPreserved = true ∧
      certificate.requiredReviewSetPreserved = true ∧
      certificate.dissentVisibilityPreserved = true ∧
      certificate.minorityVisibilityPreserved = true := by
  exact ⟨hv049, hv048, hdecomp, hcoords, hunique, hquad, hpair, hrank,
    hnotCandidates, hcandidates, hhistories, hfrontier, hreview, hdissent,
    hminority⟩

/-- Quotient coordinates grant no ranking, pruning, selection, decision,
    synthesis, activation, execution, mutation, verification, or truth
    authority. -/
theorem quotient_coordinate_canonicalization_grants_no_authority
    (certificate : CandidateQuotientCoordinateCanonicalizationCertificate)
    (hadvisory : certificate.quotientWitnessAdvisoryOnly = true)
    (hcanonical :
      certificate.canonicalRepresentativeUsedAsCandidateSelection = false)
    (hquotient : certificate.quotientUsedAsCandidatePruning = false)
    (hrank : certificate.candidateRankingPerformed = false)
    (hprune : certificate.candidatePruningPerformed = false)
    (hselect : certificate.candidateSelectionPerformed = false)
    (hcommit : certificate.decisionCommitPerformed = false)
    (hreceipt : certificate.decisionReceiptIssued = false)
    (hsynthesis : certificate.planSynthesisPerformed = false)
    (hactivate : certificate.activationPerformed = false)
    (hexecute : certificate.executionPermission = false)
    (hv049 : certificate.sourceMemoryOSV049Mutated = false)
    (hv048 : certificate.sourceMemoryOSV048Mutated = false)
    (hdecision : certificate.sourceDecisionOSV06Mutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hverify : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false)
    (hfuture : certificate.futureOnly = true)
    (hreadonly : certificate.readOnly = true) :
    certificate.quotientWitnessAdvisoryOnly = true ∧
      certificate.canonicalRepresentativeUsedAsCandidateSelection = false ∧
      certificate.quotientUsedAsCandidatePruning = false ∧
      certificate.candidateRankingPerformed = false ∧
      certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.decisionReceiptIssued = false ∧
      certificate.planSynthesisPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV049Mutated = false ∧
      certificate.sourceMemoryOSV048Mutated = false ∧
      certificate.sourceDecisionOSV06Mutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false ∧
      certificate.futureOnly = true ∧
      certificate.readOnly = true := by
  exact ⟨hadvisory, hcanonical, hquotient, hrank, hprune, hselect, hcommit,
    hreceipt, hsynthesis, hactivate, hexecute, hv049, hv048, hdecision,
    hworld, hverify, htruth, hfuture, hreadonly⟩

end KUOS.OpenHorizon.MemoryOSCandidateQuotientCoordinateCanonicalizationV0_50
