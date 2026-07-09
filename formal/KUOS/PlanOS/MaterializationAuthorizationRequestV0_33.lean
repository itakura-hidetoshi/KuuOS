import Mathlib
import KUOS.PlanOS.SelectedCandidateMaterializationPreflightV0_32

namespace KUOS
namespace PlanOS

open WORLD ObserveOS VerifyOS LearnOS DecisionOS

structure MaterializationAuthorizationRequestSurface where
  sourcePreflight : SelectedCandidateMaterializationPreflightSurface
  sourceBoundary : SelectedCandidateMaterializationPreflightBoundary
  sourcePreflightBound : Bool
  selectedCandidateBoundToPreflight : Bool
  materializationAuthorizationRequestOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  activationAuthorizationGranted : Bool
  executionGranted : Bool
  truthAuthorityGranted : Bool
  sourceRequired : sourcePreflightBound = true
  selectedBoundRequired : selectedCandidateBoundToPreflight = true
  requestOnlyRequired : materializationAuthorizationRequestOnly = true
  materializationAuthorizationForbidden : materializationAuthorizationGranted = false
  materializationExecutionForbidden : materializationExecuted = false
  activationForbidden : activationAuthorizationGranted = false
  executionForbidden : executionGranted = false
  truthForbidden : truthAuthorityGranted = false

structure MaterializationAuthorizationRequestBoundary where
  requestOwnedByPlanOS : Bool
  sourceMaterializationPreflightPreserved : Bool
  selectedCandidateBoundToPreflight : Bool
  materializationAuthorizationRequestOnly : Bool
  materializationAuthorizationGranted : Bool
  materializationExecuted : Bool
  actOSInvoked : Bool
  externalCommit : Bool
  memoryOverwrite : Bool
  blockerReleaseGranted : Bool
  requestOwnerRequired : requestOwnedByPlanOS = true
  sourcePreservedRequired : sourceMaterializationPreflightPreserved = true
  selectedBoundRequired : selectedCandidateBoundToPreflight = true
  requestOnlyRequired : materializationAuthorizationRequestOnly = true
  materializationAuthorizationForbidden : materializationAuthorizationGranted = false
  materializationExecutionForbidden : materializationExecuted = false
  invocationForbidden : actOSInvoked = false
  externalCommitForbidden : externalCommit = false
  overwriteForbidden : memoryOverwrite = false
  blockerReleaseForbidden : blockerReleaseGranted = false

structure PlanOSMaterializationAuthorizationRequestBridge where
  Digest : Type
  digestOf : MaterializationAuthorizationRequestSurface → MaterializationAuthorizationRequestBoundary → Nat → Digest
  surface : MaterializationAuthorizationRequestSurface
  boundary : MaterializationAuthorizationRequestBoundary
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

namespace PlanOSMaterializationAuthorizationRequestBridge

theorem source_preflight_remains_preflight_only
    (b : PlanOSMaterializationAuthorizationRequestBridge) :
    b.surface.sourcePreflight.materializationPreflightOnly = true ∧
      b.surface.sourcePreflight.selectedCandidateBoundToSynthesisReceipt = true ∧
      b.surface.sourceBoundary.materializationPreflightOnly = true ∧
      b.surface.sourceBoundary.materializationAuthorizationGranted = false ∧
      b.surface.sourceBoundary.materializationExecuted = false := by
  exact ⟨b.surface.sourcePreflight.preflightOnlyRequired,
    b.surface.sourcePreflight.selectedBoundRequired,
    b.surface.sourceBoundary.preflightOnlyRequired,
    b.surface.sourceBoundary.materializationAuthorizationForbidden,
    b.surface.sourceBoundary.materializationExecutionForbidden⟩

theorem request_binds_selected_candidate_to_preflight
    (b : PlanOSMaterializationAuthorizationRequestBridge) :
    b.surface.sourcePreflightBound = true ∧
      b.surface.selectedCandidateBoundToPreflight = true ∧
      b.surface.materializationAuthorizationRequestOnly = true := by
  exact ⟨b.surface.sourceRequired, b.surface.selectedBoundRequired,
    b.surface.requestOnlyRequired⟩

theorem request_grants_no_authorization_execution_activation_or_truth
    (b : PlanOSMaterializationAuthorizationRequestBridge) :
    b.surface.materializationAuthorizationGranted = false ∧
      b.surface.materializationExecuted = false ∧
      b.surface.activationAuthorizationGranted = false ∧
      b.surface.executionGranted = false ∧
      b.surface.truthAuthorityGranted = false ∧
      b.nonAuthority.executionGranted = false ∧
      b.nonAuthority.truthAuthority = false := by
  exact ⟨b.surface.materializationAuthorizationForbidden,
    b.surface.materializationExecutionForbidden,
    b.surface.activationForbidden, b.surface.executionForbidden,
    b.surface.truthForbidden, b.executionForbidden, b.truthForbidden⟩

theorem boundary_blocks_materialization_execution_commit_memory_and_blocker_release
    (b : PlanOSMaterializationAuthorizationRequestBridge) :
    b.boundary.requestOwnedByPlanOS = true ∧
      b.boundary.sourceMaterializationPreflightPreserved = true ∧
      b.boundary.selectedCandidateBoundToPreflight = true ∧
      b.boundary.materializationAuthorizationRequestOnly = true ∧
      b.boundary.materializationAuthorizationGranted = false ∧
      b.boundary.materializationExecuted = false ∧
      b.boundary.actOSInvoked = false ∧
      b.boundary.externalCommit = false ∧
      b.boundary.memoryOverwrite = false ∧
      b.boundary.blockerReleaseGranted = false := by
  exact ⟨b.boundary.requestOwnerRequired, b.boundary.sourcePreservedRequired,
    b.boundary.selectedBoundRequired, b.boundary.requestOnlyRequired,
    b.boundary.materializationAuthorizationForbidden,
    b.boundary.materializationExecutionForbidden,
    b.boundary.invocationForbidden, b.boundary.externalCommitForbidden,
    b.boundary.overwriteForbidden, b.boundary.blockerReleaseForbidden⟩

theorem history_appends_one_authorization_request_record
    (b : PlanOSMaterializationAuthorizationRequestBridge) :
    b.historyDelta = 1 := by
  exact b.historyDeltaRequired

theorem digest_is_exact (b : PlanOSMaterializationAuthorizationRequestBridge) :
    b.digest = b.digestOf b.surface b.boundary b.eventIndex := by
  exact b.digestExact

end PlanOSMaterializationAuthorizationRequestBridge

end PlanOS
end KUOS
