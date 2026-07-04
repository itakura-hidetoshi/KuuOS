import KUOS.WORLD.KuuOSLifecycleStageV0_26

namespace KUOS.WORLD.KuuOSLifecycleBoundedRepositoryMutationAuthorizationV0_27

inductive RepositoryMutationAuthorizationStatus where
  | authorizedForSeparateRepositoryMutationExecutionPreparation
  | denied
  | rejected
  deriving DecidableEq, Repr

structure RepositoryMutationAuthorizationWitness where
  sourceReviewApproved : Bool
  sourceRecomputedValid : Bool
  sourceMutationAuthorizationRouteBound : Bool
  executionPreparationRouteBound : Bool
  authorizerAuthorityVerified : Bool
  authorizerSeparated : Bool
  authorizationReceiptValid : Bool
  proposedMutationPackageFresh : Bool
  proposedMutationPackageBounded : Bool
  adoptedStateNotStale : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : RepositoryMutationAuthorizationStatus
  recordIssued : Bool
  authorizationCompleted : Bool
  executionPreparationRequiredNext : Bool
  executionPreparationRouteRequiredNext : Bool
  replanRequiredNext : Bool
  repositoryMutationPerformed : Bool
  executionPrepared : Bool
  fileWritten : Bool
  refUpdated : Bool
  branchMoved : Bool
  externalOperationPerformed : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool

structure RepositoryMutationAuthorizationWitness.ValidAuthorized
    (w : RepositoryMutationAuthorizationWitness) : Prop where
  sourceReviewApproved : w.sourceReviewApproved = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceMutationAuthorizationRouteBound :
    w.sourceMutationAuthorizationRouteBound = true
  executionPreparationRouteBound : w.executionPreparationRouteBound = true
  authorizerAuthorityVerified : w.authorizerAuthorityVerified = true
  authorizerSeparated : w.authorizerSeparated = true
  authorizationReceiptValid : w.authorizationReceiptValid = true
  proposedMutationPackageFresh : w.proposedMutationPackageFresh = true
  proposedMutationPackageBounded : w.proposedMutationPackageBounded = true
  adoptedStateNotStale : w.adoptedStateNotStale = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusAuthorized :
    w.status =
      RepositoryMutationAuthorizationStatus.authorizedForSeparateRepositoryMutationExecutionPreparation
  recordIssued : w.recordIssued = true
  authorizationCompleted : w.authorizationCompleted = true
  executionPreparationRequiredNext :
    w.executionPreparationRequiredNext = true
  executionPreparationRouteRequiredNext :
    w.executionPreparationRouteRequiredNext = true
  replanNotRequiredNext : w.replanRequiredNext = false

structure RepositoryMutationAuthorizationWitness.ValidDenied
    (w : RepositoryMutationAuthorizationWitness) : Prop where
  sourceReviewApproved : w.sourceReviewApproved = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceMutationAuthorizationRouteBound :
    w.sourceMutationAuthorizationRouteBound = true
  statusDenied : w.status = RepositoryMutationAuthorizationStatus.denied
  recordIssued : w.recordIssued = true
  authorizationCompleted : w.authorizationCompleted = true
  executionPreparationNotRequiredNext :
    w.executionPreparationRequiredNext = false
  executionPreparationRouteNotRequiredNext :
    w.executionPreparationRouteRequiredNext = false
  replanRequiredNext : w.replanRequiredNext = true

structure RepositoryMutationAuthorizationWitness.ValidRejected
    (w : RepositoryMutationAuthorizationWitness) : Prop where
  statusRejected : w.status = RepositoryMutationAuthorizationStatus.rejected
  recordNotIssued : w.recordIssued = false
  authorizationNotCompleted : w.authorizationCompleted = false
  executionPreparationNotRequiredNext :
    w.executionPreparationRequiredNext = false
  executionPreparationRouteNotRequiredNext :
    w.executionPreparationRouteRequiredNext = false
  replanNotRequiredNext : w.replanRequiredNext = false

structure RepositoryMutationAuthorizationWitness.NoRepositoryOrExternalEffect
    (w : RepositoryMutationAuthorizationWitness) : Prop where
  repositoryMutationAbsent : w.repositoryMutationPerformed = false
  executionPreparationAbsent : w.executionPrepared = false
  fileWriteAbsent : w.fileWritten = false
  refUpdateAbsent : w.refUpdated = false
  branchMoveAbsent : w.branchMoved = false
  externalOperationAbsent : w.externalOperationPerformed = false
  terminalMarkerAbsent : w.terminalMarkerWritten = false
  resourceRemovalAbsent : w.resourceRemoved = false

structure RepositoryMutationAuthorizationWitness.Valid
    (w : RepositoryMutationAuthorizationWitness) : Prop where
  caseValid :
    w.ValidAuthorized ∨ w.ValidDenied ∨ w.ValidRejected
  noRepositoryOrExternalEffect : w.NoRepositoryOrExternalEffect

theorem authorized_routes_only_to_repository_mutation_execution_preparation
    (w : RepositoryMutationAuthorizationWitness) (h : w.ValidAuthorized) :
    w.executionPreparationRequiredNext = true ∧
      w.executionPreparationRouteRequiredNext = true ∧
      w.replanRequiredNext = false := by
  exact ⟨h.executionPreparationRequiredNext,
    h.executionPreparationRouteRequiredNext,
    h.replanNotRequiredNext⟩

theorem denied_does_not_route_to_repository_mutation_execution_preparation
    (w : RepositoryMutationAuthorizationWitness) (h : w.ValidDenied) :
    w.executionPreparationRequiredNext = false ∧
      w.executionPreparationRouteRequiredNext = false ∧
      w.replanRequiredNext = true := by
  exact ⟨h.executionPreparationNotRequiredNext,
    h.executionPreparationRouteNotRequiredNext,
    h.replanRequiredNext⟩

theorem rejected_issues_no_repository_authorization_record
    (w : RepositoryMutationAuthorizationWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.authorizationCompleted = false := by
  exact ⟨h.recordNotIssued, h.authorizationNotCompleted⟩

theorem valid_repository_authorization_has_no_repository_or_external_effect
    (w : RepositoryMutationAuthorizationWitness) (h : w.Valid) :
    w.NoRepositoryOrExternalEffect := by
  exact h.noRepositoryOrExternalEffect

end KUOS.WORLD.KuuOSLifecycleBoundedRepositoryMutationAuthorizationV0_27
