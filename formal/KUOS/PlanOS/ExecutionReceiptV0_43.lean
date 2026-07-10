import Mathlib
import KUOS.PlanOS.ExecutionAuthorizationGrantV0_42

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure ExecutionReceiptSurface where
  sourceExecutionGrant : ExecutionAuthorizationGrantSurface
  sourceBoundary : ExecutionAuthorizationGrantBoundary
  sourceExecutionGrantBound : Bool
  selectedCandidateBoundToExecutionGrant : Bool
  materializationExecutionPreserved : Bool
  activationAuthorizationPreserved : Bool
  actOSInvocationPreserved : Bool
  literatureGroundingPreserved : Bool
  dynamicPlanningComputeAccounted : Bool
  selectiveForesightPreserved : Bool
  uncertaintyCalibrationPreserved : Bool
  memoryMismatchReviewPreserved : Bool
  counterfactualCoveragePreserved : Bool
  costSafetyRobustnessEvaluationPreserved : Bool
  executionAuthorizationGrantPreserved : Bool
  executionReceiptOnly : Bool
  executionAuthorizationRequested : Bool
  executionAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceExecutionGrantBound = true
  selectedBoundRequired : selectedCandidateBoundToExecutionGrant = true
  materializationPreservedRequired : materializationExecutionPreserved = true
  activationPreservedRequired : activationAuthorizationPreserved = true
  invocationPreservedRequired : actOSInvocationPreserved = true
  literatureGroundingRequired : literatureGroundingPreserved = true
  dynamicComputeRequired : dynamicPlanningComputeAccounted = true
  foresightPreservedRequired : selectiveForesightPreserved = true
  uncertaintyPreservedRequired : uncertaintyCalibrationPreserved = true
  memoryMismatchPreservedRequired : memoryMismatchReviewPreserved = true
  counterfactualPreservedRequired : counterfactualCoveragePreserved = true
  evaluationPreservedRequired : costSafetyRobustnessEvaluationPreserved = true
  grantPreservedRequired : executionAuthorizationGrantPreserved = true
  receiptOnlyRequired : executionReceiptOnly = true
  requestRequired : executionAuthorizationRequested = true
  authorizationGrantedRequired : executionAuthorizationGranted = true
  executionRequired : executionGranted = true
  truthForbidden : truthAuthorityGranted = false

structure ExecutionReceiptBoundary where
  receiptOwnedByPlanOS : Bool
  sourceExecutionAuthorizationGrantPreserved : Bool
  selectedCandidateBoundToExecutionGrant : Bool
  materializationExecutionPreserved : Bool
  activationAuthorizationPreserved : Bool
  actOSInvocationPreserved : Bool
  literatureGroundingPreserved : Bool
  dynamicPlanningComputeAccounted : Bool
  selectiveForesightPreserved : Bool
  uncertaintyCalibrationPreserved : Bool
  memoryMismatchReviewPreserved : Bool
  counterfactualCoveragePreserved : Bool
  costSafetyRobustnessEvaluationPreserved : Bool
  executionAuthorizationGrantPreserved : Bool
  executionReceiptOnly : Bool
  executionAuthorizationRequested : Bool
  executionAuthorizationGranted : Bool
  executionGranted : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  receiptOwnerRequired : receiptOwnedByPlanOS = true
  sourcePreservedRequired : sourceExecutionAuthorizationGrantPreserved = true
  selectedBoundRequired : selectedCandidateBoundToExecutionGrant = true
  materializationPreservedRequired : materializationExecutionPreserved = true
  activationPreservedRequired : activationAuthorizationPreserved = true
  invocationPreservedRequired : actOSInvocationPreserved = true
  literatureGroundingRequired : literatureGroundingPreserved = true
  dynamicComputeRequired : dynamicPlanningComputeAccounted = true
  foresightPreservedRequired : selectiveForesightPreserved = true
  uncertaintyPreservedRequired : uncertaintyCalibrationPreserved = true
  memoryMismatchPreservedRequired : memoryMismatchReviewPreserved = true
  counterfactualPreservedRequired : counterfactualCoveragePreserved = true
  evaluationPreservedRequired : costSafetyRobustnessEvaluationPreserved = true
  grantPreservedRequired : executionAuthorizationGrantPreserved = true
  receiptOnlyRequired : executionReceiptOnly = true
  requestRequired : executionAuthorizationRequested = true
  authorizationGrantedRequired : executionAuthorizationGranted = true
  executionRequired : executionGranted = true
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSExecutionReceiptBridge where
  Digest : Type
  digestOf : ExecutionReceiptSurface → ExecutionReceiptBoundary → Nat → Digest
  surface : ExecutionReceiptSurface
  boundary : ExecutionReceiptBoundary
  eventIndex : Nat
  historyDelta : Nat
  digest : Digest
  nonAuthority : AdapterNonAuthority
  historyDeltaRequired : historyDelta = 1
  digestExact : digest = digestOf surface boundary eventIndex
  truthForbidden : nonAuthority.truthAuthority = false
  clinicalForbidden : nonAuthority.clinicalAuthority = false
  legalForbidden : nonAuthority.legalAuthority = false
  overwriteForbidden : nonAuthority.memoryOverwrite = false

namespace PlanOSExecutionReceiptBridge

theorem source_grant_authorizes_but_does_not_execute
    (b : PlanOSExecutionReceiptBridge) :
    b.surface.sourceExecutionGrant.executionAuthorizationGrantOnly = true ∧
      b.surface.sourceExecutionGrant.executionAuthorizationRequested = true ∧
      b.surface.sourceExecutionGrant.executionAuthorizationGranted = true ∧
      b.surface.sourceExecutionGrant.executionGranted = false ∧
      b.surface.sourceBoundary.executionAuthorizationGrantOnly = true ∧
      b.surface.sourceBoundary.executionAuthorizationGranted = true ∧
      b.surface.sourceBoundary.executionGranted = false := by
  exact ⟨b.surface.sourceExecutionGrant.grantOnlyRequired,
    b.surface.sourceExecutionGrant.requestRequired,
    b.surface.sourceExecutionGrant.authorizationGrantedRequired,
    b.surface.sourceExecutionGrant.executionForbidden,
    b.surface.sourceBoundary.grantOnlyRequired,
    b.surface.sourceBoundary.authorizationGrantedRequired,
    b.surface.sourceBoundary.executionForbidden⟩

theorem receipt_binds_candidate_and_preserves_prerequisites
    (b : PlanOSExecutionReceiptBridge) :
    b.surface.sourceExecutionGrantBound = true ∧
      b.surface.selectedCandidateBoundToExecutionGrant = true ∧
      b.surface.materializationExecutionPreserved = true ∧
      b.surface.activationAuthorizationPreserved = true ∧
      b.surface.actOSInvocationPreserved = true ∧
      b.surface.literatureGroundingPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.materializationPreservedRequired, b.surface.activationPreservedRequired,
    b.surface.invocationPreservedRequired, b.surface.literatureGroundingRequired⟩

theorem receipt_records_execution_but_not_commit_memory_truth_or_blocker_release
    (b : PlanOSExecutionReceiptBridge) :
    b.surface.executionAuthorizationGrantPreserved = true ∧
      b.surface.executionReceiptOnly = true ∧
      b.surface.executionAuthorizationRequested = true ∧
      b.surface.executionAuthorizationGranted = true ∧
      b.surface.executionGranted = true ∧
      b.surface.truthAuthorityGranted = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false ∧
      b.nonAuthority.truthAuthority = false ∧
      b.nonAuthority.memoryOverwrite = false := by
  exact ⟨b.surface.grantPreservedRequired, b.surface.receiptOnlyRequired,
    b.surface.requestRequired, b.surface.authorizationGrantedRequired,
    b.surface.executionRequired, b.surface.truthForbidden,
    b.boundary.externalCommitForbidden, b.boundary.overwriteForbidden,
    b.boundary.blockerReleaseForbidden, b.truthForbidden, b.overwriteForbidden⟩

theorem boundary_preserves_execution_receipt_only
    (b : PlanOSExecutionReceiptBridge) :
    b.boundary.receiptOwnedByPlanOS = true ∧
      b.boundary.sourceExecutionAuthorizationGrantPreserved = true ∧
      b.boundary.selectedCandidateBoundToExecutionGrant = true ∧
      b.boundary.executionAuthorizationGrantPreserved = true ∧
      b.boundary.executionReceiptOnly = true ∧
      b.boundary.executionAuthorizationRequested = true ∧
      b.boundary.executionAuthorizationGranted = true ∧
      b.boundary.executionGranted = true ∧
      b.boundary.externalCommit = false := by
  exact ⟨b.boundary.receiptOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.grantPreservedRequired,
    b.boundary.receiptOnlyRequired, b.boundary.requestRequired,
    b.boundary.authorizationGrantedRequired, b.boundary.executionRequired,
    b.boundary.externalCommitForbidden⟩

theorem history_appends_one_execution_receipt_record
    (b : PlanOSExecutionReceiptBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSExecutionReceiptBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSExecutionReceiptBridge

end PlanOS
end KUOS
