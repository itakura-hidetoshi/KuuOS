import Mathlib
import KUOS.PlanOS.ExecutionAuthorizationRequestV0_41

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure ExecutionAuthorizationGrantSurface where
  sourceExecutionRequest : ExecutionAuthorizationRequestSurface
  sourceBoundary : ExecutionAuthorizationRequestBoundary
  sourceExecutionRequestBound : Bool
  selectedCandidateBoundToExecutionRequest : Bool
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
  executionAuthorizationRequestPreserved : Bool
  executionAuthorizationGrantOnly : Bool
  executionAuthorizationRequested : Bool
  executionAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourceExecutionRequestBound = true
  selectedBoundRequired : selectedCandidateBoundToExecutionRequest = true
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
  requestPreservedRequired : executionAuthorizationRequestPreserved = true
  grantOnlyRequired : executionAuthorizationGrantOnly = true
  requestRequired : executionAuthorizationRequested = true
  authorizationGrantedRequired : executionAuthorizationGranted = true
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure ExecutionAuthorizationGrantBoundary where
  grantOwnedByPlanOS : Bool
  sourceExecutionAuthorizationRequestPreserved : Bool
  selectedCandidateBoundToExecutionRequest : Bool
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
  executionAuthorizationRequestPreserved : Bool
  executionAuthorizationGrantOnly : Bool
  executionAuthorizationRequested : Bool
  executionAuthorizationGranted : Bool
  executionGranted : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  grantOwnerRequired : grantOwnedByPlanOS = true
  sourcePreservedRequired : sourceExecutionAuthorizationRequestPreserved = true
  selectedBoundRequired : selectedCandidateBoundToExecutionRequest = true
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
  requestPreservedRequired : executionAuthorizationRequestPreserved = true
  grantOnlyRequired : executionAuthorizationGrantOnly = true
  requestRequired : executionAuthorizationRequested = true
  authorizationGrantedRequired : executionAuthorizationGranted = true
  executionForbidden : executionGranted = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSExecutionAuthorizationGrantBridge where
  Digest : Type
  digestOf : ExecutionAuthorizationGrantSurface → ExecutionAuthorizationGrantBoundary → Nat → Digest
  surface : ExecutionAuthorizationGrantSurface
  boundary : ExecutionAuthorizationGrantBoundary
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

namespace PlanOSExecutionAuthorizationGrantBridge

theorem source_request_remains_request_only
    (b : PlanOSExecutionAuthorizationGrantBridge) :
    b.surface.sourceExecutionRequest.executionAuthorizationRequestOnly = true ∧
      b.surface.sourceExecutionRequest.executionAuthorizationRequested = true ∧
      b.surface.sourceExecutionRequest.executionAuthorizationGranted = false ∧
      b.surface.sourceExecutionRequest.executionGranted = false ∧
      b.surface.sourceBoundary.executionAuthorizationRequestOnly = true ∧
      b.surface.sourceBoundary.executionAuthorizationRequested = true ∧
      b.surface.sourceBoundary.executionAuthorizationGranted = false ∧
      b.surface.sourceBoundary.executionGranted = false := by
  exact ⟨b.surface.sourceExecutionRequest.requestOnlyRequired,
    b.surface.sourceExecutionRequest.requestRequired,
    b.surface.sourceExecutionRequest.authorizationForbidden,
    b.surface.sourceExecutionRequest.executionForbidden,
    b.surface.sourceBoundary.requestOnlyRequired,
    b.surface.sourceBoundary.requestRequired,
    b.surface.sourceBoundary.authorizationForbidden,
    b.surface.sourceBoundary.executionForbidden⟩

theorem grant_binds_candidate_and_preserves_prerequisites
    (b : PlanOSExecutionAuthorizationGrantBridge) :
    b.surface.sourceExecutionRequestBound = true ∧
      b.surface.selectedCandidateBoundToExecutionRequest = true ∧
      b.surface.materializationExecutionPreserved = true ∧
      b.surface.activationAuthorizationPreserved = true ∧
      b.surface.actOSInvocationPreserved = true ∧
      b.surface.literatureGroundingPreserved = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.materializationPreservedRequired, b.surface.activationPreservedRequired,
    b.surface.invocationPreservedRequired, b.surface.literatureGroundingRequired⟩

theorem grant_preserves_literature_grounded_execution_prerequisites
    (b : PlanOSExecutionAuthorizationGrantBridge) :
    b.surface.dynamicPlanningComputeAccounted = true ∧
      b.surface.selectiveForesightPreserved = true ∧
      b.surface.uncertaintyCalibrationPreserved = true ∧
      b.surface.memoryMismatchReviewPreserved = true ∧
      b.surface.counterfactualCoveragePreserved = true ∧
      b.surface.costSafetyRobustnessEvaluationPreserved = true := by
  exact ⟨b.surface.dynamicComputeRequired, b.surface.foresightPreservedRequired,
    b.surface.uncertaintyPreservedRequired, b.surface.memoryMismatchPreservedRequired,
    b.surface.counterfactualPreservedRequired, b.surface.evaluationPreservedRequired⟩

theorem grant_authorizes_execution_but_does_not_execute_or_commit
    (b : PlanOSExecutionAuthorizationGrantBridge) :
    b.surface.executionAuthorizationRequestPreserved = true ∧
      b.surface.executionAuthorizationGrantOnly = true ∧
      b.surface.executionAuthorizationRequested = true ∧
      b.surface.executionAuthorizationGranted = true ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.boundary.executionGranted = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.requestPreservedRequired, b.surface.grantOnlyRequired,
    b.surface.requestRequired, b.surface.authorizationGrantedRequired,
    b.surface.executionForbidden, b.surface.truthForbidden,
    b.boundary.executionForbidden, b.boundary.externalCommitForbidden,
    b.boundary.overwriteForbidden, b.boundary.blockerReleaseForbidden,
    b.executionForbidden, b.truthForbidden⟩

theorem boundary_preserves_execution_authorization_grant_only
    (b : PlanOSExecutionAuthorizationGrantBridge) :
    b.boundary.grantOwnedByPlanOS = true ∧
      b.boundary.sourceExecutionAuthorizationRequestPreserved = true ∧
      b.boundary.selectedCandidateBoundToExecutionRequest = true ∧
      b.boundary.executionAuthorizationRequestPreserved = true ∧
      b.boundary.executionAuthorizationGrantOnly = true ∧
      b.boundary.executionAuthorizationRequested = true ∧
      b.boundary.executionAuthorizationGranted = true ∧
      b.boundary.executionGranted = false := by
  exact ⟨b.boundary.grantOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.requestPreservedRequired,
    b.boundary.grantOnlyRequired, b.boundary.requestRequired,
    b.boundary.authorizationGrantedRequired, b.boundary.executionForbidden⟩

theorem history_appends_one_execution_authorization_grant_record
    (b : PlanOSExecutionAuthorizationGrantBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSExecutionAuthorizationGrantBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSExecutionAuthorizationGrantBridge

end PlanOS
end KUOS
