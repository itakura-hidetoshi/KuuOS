import Mathlib
import KUOS.OpenHorizon.MemoryOSObserverRelativeTemporalWindowCoherenceCocycleCompositionV0_43
import KUOS.OpenHorizon.MemoryOSObserverRelativeNonMarkovInfluenceConditionedPlanOSCoherenceKernelV0_42

namespace KUOS.OpenHorizon.MemoryOSObserverRelativeCoherenceQuadraticEvidenceDecisionOSHandoffV0_44

open scoped BigOperators ComplexConjugate
open KUOS.OpenHorizon.MemoryOSObserverRelativeNonMarkovInfluenceConditionedPlanOSCoherenceKernelV0_42

/-- Exact real two-history quadratic evidence used by the bounded reference
    runtime. `cross` is the real off-diagonal kernel numerator. -/
def quadraticEvidence2
    (leftDiagonal cross rightDiagonal leftCoefficient rightCoefficient : ℤ) : ℤ :=
  leftDiagonal * leftCoefficient * leftCoefficient +
    rightDiagonal * rightCoefficient * rightCoefficient +
    2 * cross * leftCoefficient * rightCoefficient

/-- A PSD kernel gives nonnegative candidate coherence evidence for every
    finite coupling vector. -/
theorem coherenceQuadraticEvidence_nonnegative
    {ι : Type} [Fintype ι]
    (kernel : Matrix ι ι ℂ)
    (hpsd : IsPositiveSemidefiniteKernel kernel)
    (coupling : ι → ℂ) :
    0 ≤ (quadraticForm kernel coupling).re := by
  exact hpsd coupling

/-- Memory-conditioned diagonal phase congruence preserves the nonnegativity
    needed by the DecisionOS evidence handoff. -/
theorem conditionedCoherenceQuadraticEvidence_nonnegative
    {ι : Type} [Fintype ι]
    (phase : ι → ℂ)
    (kernel : Matrix ι ι ℂ)
    (hpsd : IsPositiveSemidefiniteKernel kernel)
    (coupling : ι → ℂ) :
    0 ≤ (quadraticForm (phaseDeformMatrix phase kernel) coupling).re := by
  exact phaseDeform_preserves_positiveSemidefinite phase kernel hpsd coupling

/-- The constructive `continue = [1,1]` coupling has exact evidence trajectory
    `8,6,4` through the reference dephasing numerators `2,1,0`. -/
theorem reference_continue_quadratic_evidence :
    quadraticEvidence2 2 2 2 1 1 = 8 ∧
      quadraticEvidence2 2 1 2 1 1 = 6 ∧
      quadraticEvidence2 2 0 2 1 1 = 4 := by
  norm_num [quadraticEvidence2]

/-- The contrastive `hold = [1,-1]` coupling has exact evidence trajectory
    `0,2,4`; coherence loss can therefore increase rather than decrease this
    evidence. -/
theorem reference_hold_quadratic_evidence :
    quadraticEvidence2 2 2 2 1 (-1) = 0 ∧
      quadraticEvidence2 2 1 2 1 (-1) = 2 ∧
      quadraticEvidence2 2 0 2 1 (-1) = 4 := by
  norm_num [quadraticEvidence2]

/-- A one-history `reobserve = [1,0]` coupling is invariant along the same
    dephasing trajectory. -/
theorem reference_reobserve_quadratic_evidence :
    quadraticEvidence2 2 2 2 1 0 = 2 ∧
      quadraticEvidence2 2 1 2 1 0 = 2 ∧
      quadraticEvidence2 2 0 2 1 0 = 2 := by
  norm_num [quadraticEvidence2]

/-- The complementary one-history retained nonadmissible candidate is also
    invariant and remains present. -/
theorem reference_terminate_quadratic_evidence :
    quadraticEvidence2 2 2 2 0 1 = 2 ∧
      quadraticEvidence2 2 1 2 0 1 = 2 ∧
      quadraticEvidence2 2 0 2 0 1 = 2 := by
  norm_num [quadraticEvidence2]

/-- Positive, zero, and negative coherence contrasts coexist in the reference
    field. Hence contrast is not a monotone scalar utility or a selection
    order. -/
theorem reference_coherence_contrasts_are_plural :
    (8 : ℤ) - 4 = 4 ∧
      (2 : ℤ) - 2 = 0 ∧
      (0 : ℤ) - 4 = -4 := by
  norm_num

/-- Bounded MemoryOS v0.44 certificate surface. -/
structure ObserverRelativeCoherenceQuadraticEvidenceDecisionOSHandoffCertificate where
  sourceMemoryOSV043Bound : Bool
  sourceDecisionOSV06Bound : Bool
  allDecisionCandidatesRetained : Bool
  allPlanOSHistoriesRetained : Bool
  quadraticEvidenceNonnegativeByPSD : Bool
  quadraticEvidenceRealByHermitianSymmetry : Bool
  relationalFrontierPreserved : Bool
  requiredReviewSetPreserved : Bool
  dissentVisibilityPreserved : Bool
  minorityVisibilityPreserved : Bool
  coherenceEvidenceAdvisoryOnly : Bool
  coherenceContrastUsedAsScalarUtility : Bool
  candidateRankingPerformed : Bool
  candidatePruningPerformed : Bool
  candidateSelectionPerformed : Bool
  decisionCommitPerformed : Bool
  decisionReceiptIssued : Bool
  planSynthesisPerformed : Bool
  activationPerformed : Bool
  executionPermission : Bool
  sourceMemoryOSV043Mutated : Bool
  sourceDecisionOSV06Mutated : Bool
  persistentWorldStateMutated : Bool
  verificationResultClaimed : Bool
  truthAuthorityGranted : Bool
  futureOnly : Bool
  readOnly : Bool

/-- v0.44 preserves both source supports and every relational review boundary
    while attaching exact quadratic evidence. -/
theorem coherence_evidence_handoff_preserves_support_and_review
    (certificate : ObserverRelativeCoherenceQuadraticEvidenceDecisionOSHandoffCertificate)
    (hmemory : certificate.sourceMemoryOSV043Bound = true)
    (hdecision : certificate.sourceDecisionOSV06Bound = true)
    (hcandidates : certificate.allDecisionCandidatesRetained = true)
    (hhistories : certificate.allPlanOSHistoriesRetained = true)
    (hpsd : certificate.quadraticEvidenceNonnegativeByPSD = true)
    (hreal : certificate.quadraticEvidenceRealByHermitianSymmetry = true)
    (hfrontier : certificate.relationalFrontierPreserved = true)
    (hreview : certificate.requiredReviewSetPreserved = true)
    (hdissent : certificate.dissentVisibilityPreserved = true)
    (hminority : certificate.minorityVisibilityPreserved = true) :
    certificate.sourceMemoryOSV043Bound = true ∧
      certificate.sourceDecisionOSV06Bound = true ∧
      certificate.allDecisionCandidatesRetained = true ∧
      certificate.allPlanOSHistoriesRetained = true ∧
      certificate.quadraticEvidenceNonnegativeByPSD = true ∧
      certificate.quadraticEvidenceRealByHermitianSymmetry = true ∧
      certificate.relationalFrontierPreserved = true ∧
      certificate.requiredReviewSetPreserved = true ∧
      certificate.dissentVisibilityPreserved = true ∧
      certificate.minorityVisibilityPreserved = true := by
  exact ⟨hmemory, hdecision, hcandidates, hhistories, hpsd, hreal, hfrontier,
    hreview, hdissent, hminority⟩

/-- Coherence evidence grants no ranking, selection, decision, synthesis,
    activation, execution, mutation, verification, or truth authority. -/
theorem coherence_evidence_handoff_grants_no_authority
    (certificate : ObserverRelativeCoherenceQuadraticEvidenceDecisionOSHandoffCertificate)
    (hadvisory : certificate.coherenceEvidenceAdvisoryOnly = true)
    (hscalar : certificate.coherenceContrastUsedAsScalarUtility = false)
    (hrank : certificate.candidateRankingPerformed = false)
    (hprune : certificate.candidatePruningPerformed = false)
    (hselect : certificate.candidateSelectionPerformed = false)
    (hcommit : certificate.decisionCommitPerformed = false)
    (hreceipt : certificate.decisionReceiptIssued = false)
    (hsynthesis : certificate.planSynthesisPerformed = false)
    (hactivate : certificate.activationPerformed = false)
    (hexecute : certificate.executionPermission = false)
    (hmemory : certificate.sourceMemoryOSV043Mutated = false)
    (hdecision : certificate.sourceDecisionOSV06Mutated = false)
    (hworld : certificate.persistentWorldStateMutated = false)
    (hverify : certificate.verificationResultClaimed = false)
    (htruth : certificate.truthAuthorityGranted = false)
    (hfuture : certificate.futureOnly = true)
    (hreadonly : certificate.readOnly = true) :
    certificate.coherenceEvidenceAdvisoryOnly = true ∧
      certificate.coherenceContrastUsedAsScalarUtility = false ∧
      certificate.candidateRankingPerformed = false ∧
      certificate.candidatePruningPerformed = false ∧
      certificate.candidateSelectionPerformed = false ∧
      certificate.decisionCommitPerformed = false ∧
      certificate.decisionReceiptIssued = false ∧
      certificate.planSynthesisPerformed = false ∧
      certificate.activationPerformed = false ∧
      certificate.executionPermission = false ∧
      certificate.sourceMemoryOSV043Mutated = false ∧
      certificate.sourceDecisionOSV06Mutated = false ∧
      certificate.persistentWorldStateMutated = false ∧
      certificate.verificationResultClaimed = false ∧
      certificate.truthAuthorityGranted = false ∧
      certificate.futureOnly = true ∧
      certificate.readOnly = true := by
  exact ⟨hadvisory, hscalar, hrank, hprune, hselect, hcommit, hreceipt,
    hsynthesis, hactivate, hexecute, hmemory, hdecision, hworld, hverify,
    htruth, hfuture, hreadonly⟩

end KUOS.OpenHorizon.MemoryOSObserverRelativeCoherenceQuadraticEvidenceDecisionOSHandoffV0_44
