import Mathlib
import KUOS.PlanOS.PathIntegralCandidateWeightingV0_25

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure WeightedDecisionEvidenceSurface where
  sourceWeighting : PathIntegralCandidateWeightSurface
  sourceReceiptBoundary : CandidateWeightReceiptBoundary
  sourceWeightingBound : Bool
  decisionEvidenceOnly : Bool
  advisoryScoresBound : Bool
  retainedCandidateIdsBound : Bool
  probeCandidateIdsBound : Bool
  barrierCandidateIdsBound : Bool
  selectionOwnedByDecisionOS : Bool
  selectionAuthorityGranted : Bool
  decisionMade : Bool
  activationAuthorizationGranted : Bool
  actOSInvoked : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceWeightingBound = true
  evidenceOnlyRequired : decisionEvidenceOnly = true
  advisoryRequired : advisoryScoresBound = true
  retainedRequired : retainedCandidateIdsBound = true
  probeRequired : probeCandidateIdsBound = true
  barrierRequired : barrierCandidateIdsBound = true
  decisionOwnerRequired : selectionOwnedByDecisionOS = true
  selectionForbidden : selectionAuthorityGranted = false
  decisionForbidden : decisionMade = false
  activationForbidden : activationAuthorizationGranted = false
  invocationForbidden : actOSInvoked = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure DecisionEvidenceHandoffBoundary where
  handoffOwnedByPlanOS : Bool
  decisionEvidenceOnly : Bool
  noSilentCandidateSubstitution : Bool
  barrierCandidatesNotSelectableHere : Bool
  probeCandidatesRequireReview : Bool
  selectedCandidateCommitted : Bool
  decisionReceiptIssued : Bool
  executionReady : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  planOwnerRequired : handoffOwnedByPlanOS = true
  evidenceOnlyRequired : decisionEvidenceOnly = true
  noSilentSubstitutionRequired : noSilentCandidateSubstitution = true
  barrierRuleRequired : barrierCandidatesNotSelectableHere = true
  probeRuleRequired : probeCandidatesRequireReview = true
  selectionCommitForbidden : selectedCandidateCommitted = false
  decisionReceiptForbidden : decisionReceiptIssued = false
  executionReadyForbidden : executionReady = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSWeightedDecisionEvidenceHandoffBridge where
  Digest : Type
  digestOf : WeightedDecisionEvidenceSurface → DecisionEvidenceHandoffBoundary → Nat → Digest
  surface : WeightedDecisionEvidenceSurface
  boundary : DecisionEvidenceHandoffBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  nonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  executionForbidden : nonAuthority.executionGranted = false
  truthForbidden : nonAuthority.truthAuthority = false
  clinicalForbidden : nonAuthority.clinicalAuthority = false
  legalForbidden : nonAuthority.legalAuthority = false
  overwriteForbidden : nonAuthority.memoryOverwrite = false

namespace PlanOSWeightedDecisionEvidenceHandoffBridge

theorem source_weighting_remains_advisory (b : PlanOSWeightedDecisionEvidenceHandoffBridge) :
    b.surface.sourceWeighting.candidateWeightingAdvisoryOnly = true ∧
      b.surface.sourceReceiptBoundary.replanRecommendationOnly = true ∧
      b.surface.sourceReceiptBoundary.selectedCandidateCommitted = false ∧
      b.surface.sourceReceiptBoundary.actOSInvoked = false ∧
      b.surface.sourceReceiptBoundary.executionReady = false := by
  exact ⟨b.surface.sourceWeighting.advisoryRequired,
    b.surface.sourceReceiptBoundary.recommendationOnlyRequired,
    b.surface.sourceReceiptBoundary.selectionCommitForbidden,
    b.surface.sourceReceiptBoundary.invocationForbidden,
    b.surface.sourceReceiptBoundary.executionReadyForbidden⟩

theorem handoff_is_decision_evidence_only (b : PlanOSWeightedDecisionEvidenceHandoffBridge) :
    b.surface.sourceWeightingBound = true ∧
      b.surface.decisionEvidenceOnly = true ∧
      b.surface.advisoryScoresBound = true ∧
      b.surface.retainedCandidateIdsBound = true ∧
      b.surface.probeCandidateIdsBound = true ∧
      b.surface.barrierCandidateIdsBound = true ∧
      b.surface.selectionOwnedByDecisionOS = true := by
  exact ⟨b.surface.sourceRequired, b.surface.evidenceOnlyRequired,
    b.surface.advisoryRequired, b.surface.retainedRequired,
    b.surface.probeRequired, b.surface.barrierRequired,
    b.surface.decisionOwnerRequired⟩

theorem handoff_grants_no_decision_activation_execution_or_truth
    (b : PlanOSWeightedDecisionEvidenceHandoffBridge) :
    b.surface.selectionAuthorityGranted = false ∧
      b.surface.decisionMade = false ∧
      b.surface.activationAuthorizationGranted = false ∧
      b.surface.actOSInvoked = false ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.selectionForbidden, b.surface.decisionForbidden,
    b.surface.activationForbidden, b.surface.invocationForbidden,
    b.surface.executionForbidden, b.surface.truthForbidden,
    b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_selection_and_commit_here
    (b : PlanOSWeightedDecisionEvidenceHandoffBridge) :
    b.boundary.handoffOwnedByPlanOS = true ∧
      b.boundary.decisionEvidenceOnly = true ∧
      b.boundary.noSilentCandidateSubstitution = true ∧
      b.boundary.barrierCandidatesNotSelectableHere = true ∧
      b.boundary.probeCandidatesRequireReview = true ∧
      b.boundary.selectedCandidateCommitted = false ∧
      b.boundary.decisionReceiptIssued = false ∧
      b.boundary.executionReady = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.planOwnerRequired, b.boundary.evidenceOnlyRequired,
    b.boundary.noSilentSubstitutionRequired, b.boundary.barrierRuleRequired,
    b.boundary.probeRuleRequired, b.boundary.selectionCommitForbidden,
    b.boundary.decisionReceiptForbidden, b.boundary.executionReadyForbidden,
    b.boundary.externalCommitForbidden, b.boundary.overwriteForbidden,
    b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_handoff_record (b : PlanOSWeightedDecisionEvidenceHandoffBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSWeightedDecisionEvidenceHandoffBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSWeightedDecisionEvidenceHandoffBridge

end PlanOS
end KUOS
