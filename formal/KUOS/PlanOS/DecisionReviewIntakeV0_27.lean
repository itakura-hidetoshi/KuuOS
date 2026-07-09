import Mathlib
import KUOS.PlanOS.WeightedDecisionEvidenceHandoffV0_26

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure DecisionReviewIntakeSurface where
  sourceHandoff : WeightedDecisionEvidenceSurface
  sourceBoundary : DecisionEvidenceHandoffBoundary
  sourceHandoffBound : Bool
  decisionReviewInputOnly : Bool
  reviewCandidateIdsBound : Bool
  probeCandidateIdsBound : Bool
  barrierCandidatesExcluded : Bool
  silentSubstitutionForbidden : Bool
  reviewOwnedByDecisionOS : Bool
  selectableHere : Bool
  decisionMade : Bool
  decisionReceiptIssued : Bool
  activationAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceHandoffBound = true
  inputOnlyRequired : decisionReviewInputOnly = true
  reviewIdsRequired : reviewCandidateIdsBound = true
  probeIdsRequired : probeCandidateIdsBound = true
  barrierExcludedRequired : barrierCandidatesExcluded = true
  noSilentSubstitutionRequired : silentSubstitutionForbidden = true
  decisionOwnerRequired : reviewOwnedByDecisionOS = true
  selectableForbidden : selectableHere = false
  decisionForbidden : decisionMade = false
  decisionReceiptForbidden : decisionReceiptIssued = false
  activationForbidden : activationAuthorizationGranted = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure DecisionReviewIntakeBoundary where
  intakeOwnedByPlanOS : Bool
  decisionReviewInputOnly : Bool
  probeCandidateReviewFlagRequired : Bool
  barrierCandidateReviewBlockedHere : Bool
  selectedCandidateCommitted : Bool
  decisionReceiptIssued : Bool
  actOSInvoked : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  planOwnerRequired : intakeOwnedByPlanOS = true
  inputOnlyRequired : decisionReviewInputOnly = true
  probeFlagRequired : probeCandidateReviewFlagRequired = true
  barrierBlockedRequired : barrierCandidateReviewBlockedHere = true
  selectionCommitForbidden : selectedCandidateCommitted = false
  decisionReceiptForbidden : decisionReceiptIssued = false
  invocationForbidden : actOSInvoked = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSDecisionReviewIntakeBridge where
  Digest : Type
  digestOf : DecisionReviewIntakeSurface → DecisionReviewIntakeBoundary → Nat → Digest
  surface : DecisionReviewIntakeSurface
  boundary : DecisionReviewIntakeBoundary
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

namespace PlanOSDecisionReviewIntakeBridge

theorem source_handoff_remains_evidence_only (b : PlanOSDecisionReviewIntakeBridge) :
    b.surface.sourceHandoff.decisionEvidenceOnly = true ∧
      b.surface.sourceHandoff.selectionOwnedByDecisionOS = true ∧
      b.surface.sourceBoundary.decisionEvidenceOnly = true ∧
      b.surface.sourceBoundary.selectedCandidateCommitted = false ∧
      b.surface.sourceBoundary.decisionReceiptIssued = false := by
  exact ⟨b.surface.sourceHandoff.evidenceOnlyRequired,
    b.surface.sourceHandoff.decisionOwnerRequired,
    b.surface.sourceBoundary.evidenceOnlyRequired,
    b.surface.sourceBoundary.selectionCommitForbidden,
    b.surface.sourceBoundary.decisionReceiptForbidden⟩

theorem intake_is_review_input_only (b : PlanOSDecisionReviewIntakeBridge) :
    b.surface.sourceHandoffBound = true ∧
      b.surface.decisionReviewInputOnly = true ∧
      b.surface.reviewCandidateIdsBound = true ∧
      b.surface.probeCandidateIdsBound = true ∧
      b.surface.barrierCandidatesExcluded = true ∧
      b.surface.silentSubstitutionForbidden = true ∧
      b.surface.reviewOwnedByDecisionOS = true := by
  exact ⟨b.surface.sourceRequired, b.surface.inputOnlyRequired,
    b.surface.reviewIdsRequired, b.surface.probeIdsRequired,
    b.surface.barrierExcludedRequired, b.surface.noSilentSubstitutionRequired,
    b.surface.decisionOwnerRequired⟩

theorem intake_grants_no_selection_decision_activation_execution_or_truth
    (b : PlanOSDecisionReviewIntakeBridge) :
    b.surface.selectableHere = false ∧
      b.surface.decisionMade = false ∧
      b.surface.decisionReceiptIssued = false ∧
      b.surface.activationAuthorizationGranted = false ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.selectableForbidden, b.surface.decisionForbidden,
    b.surface.decisionReceiptForbidden, b.surface.activationForbidden,
    b.surface.executionForbidden, b.surface.truthForbidden,
    b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_execution_commit_memory_and_blocker_release
    (b : PlanOSDecisionReviewIntakeBridge) :
    b.boundary.intakeOwnedByPlanOS = true ∧
      b.boundary.decisionReviewInputOnly = true ∧
      b.boundary.probeCandidateReviewFlagRequired = true ∧
      b.boundary.barrierCandidateReviewBlockedHere = true ∧
      b.boundary.selectedCandidateCommitted = false ∧
      b.boundary.decisionReceiptIssued = false ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.planOwnerRequired, b.boundary.inputOnlyRequired,
    b.boundary.probeFlagRequired, b.boundary.barrierBlockedRequired,
    b.boundary.selectionCommitForbidden, b.boundary.decisionReceiptForbidden,
    b.boundary.invocationForbidden, b.boundary.externalCommitForbidden,
    b.boundary.overwriteForbidden, b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_review_intake_record (b : PlanOSDecisionReviewIntakeBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSDecisionReviewIntakeBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSDecisionReviewIntakeBridge

end PlanOS
end KUOS
