import KUOS.WORLD.KuuOSLifecycleStageV0_25

namespace KUOS.WORLD.KuuOSLifecycleBoundedRepositoryMutationReviewV0_26

inductive RepositoryMutationReviewStatus where
  | approvedForSeparateRepositoryMutationAuthorization
  | denied
  | rejected
  deriving DecidableEq, Repr

structure RepositoryMutationReviewWitness where
  sourceAdopted : Bool
  sourceRecomputedValid : Bool
  sourceRepositoryReviewRouteBound : Bool
  mutationAuthorizationRouteBound : Bool
  mutationReviewerAuthorityVerified : Bool
  mutationReviewerSeparated : Bool
  reviewReceiptValid : Bool
  proposedMutationPackageFresh : Bool
  proposedMutationPackageBounded : Bool
  adoptedStateNotStale : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : RepositoryMutationReviewStatus
  recordIssued : Bool
  reviewCompleted : Bool
  repositoryMutationAuthorizationRequiredNext : Bool
  repositoryMutationAuthorizationRouteRequiredNext : Bool
  replanRequiredNext : Bool
  repositoryMutationPerformed : Bool
  fileWritten : Bool
  refUpdated : Bool
  branchMoved : Bool
  externalOperationPerformed : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool

structure RepositoryMutationReviewWitness.ValidApproved
    (w : RepositoryMutationReviewWitness) : Prop where
  sourceAdopted : w.sourceAdopted = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceRepositoryReviewRouteBound : w.sourceRepositoryReviewRouteBound = true
  mutationAuthorizationRouteBound : w.mutationAuthorizationRouteBound = true
  mutationReviewerAuthorityVerified :
    w.mutationReviewerAuthorityVerified = true
  mutationReviewerSeparated : w.mutationReviewerSeparated = true
  reviewReceiptValid : w.reviewReceiptValid = true
  proposedMutationPackageFresh : w.proposedMutationPackageFresh = true
  proposedMutationPackageBounded : w.proposedMutationPackageBounded = true
  adoptedStateNotStale : w.adoptedStateNotStale = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusApproved :
    w.status =
      RepositoryMutationReviewStatus.approvedForSeparateRepositoryMutationAuthorization
  recordIssued : w.recordIssued = true
  reviewCompleted : w.reviewCompleted = true
  repositoryMutationAuthorizationRequiredNext :
    w.repositoryMutationAuthorizationRequiredNext = true
  repositoryMutationAuthorizationRouteRequiredNext :
    w.repositoryMutationAuthorizationRouteRequiredNext = true
  replanNotRequiredNext : w.replanRequiredNext = false

structure RepositoryMutationReviewWitness.ValidDenied
    (w : RepositoryMutationReviewWitness) : Prop where
  sourceAdopted : w.sourceAdopted = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceRepositoryReviewRouteBound : w.sourceRepositoryReviewRouteBound = true
  statusDenied : w.status = RepositoryMutationReviewStatus.denied
  recordIssued : w.recordIssued = true
  reviewCompleted : w.reviewCompleted = true
  repositoryMutationAuthorizationNotRequiredNext :
    w.repositoryMutationAuthorizationRequiredNext = false
  repositoryMutationAuthorizationRouteNotRequiredNext :
    w.repositoryMutationAuthorizationRouteRequiredNext = false
  replanRequiredNext : w.replanRequiredNext = true

structure RepositoryMutationReviewWitness.ValidRejected
    (w : RepositoryMutationReviewWitness) : Prop where
  statusRejected : w.status = RepositoryMutationReviewStatus.rejected
  recordNotIssued : w.recordIssued = false
  reviewNotCompleted : w.reviewCompleted = false
  repositoryMutationAuthorizationNotRequiredNext :
    w.repositoryMutationAuthorizationRequiredNext = false
  repositoryMutationAuthorizationRouteNotRequiredNext :
    w.repositoryMutationAuthorizationRouteRequiredNext = false
  replanNotRequiredNext : w.replanRequiredNext = false

structure RepositoryMutationReviewWitness.NoRepositoryOrExternalEffect
    (w : RepositoryMutationReviewWitness) : Prop where
  repositoryMutationAbsent : w.repositoryMutationPerformed = false
  fileWriteAbsent : w.fileWritten = false
  refUpdateAbsent : w.refUpdated = false
  branchMoveAbsent : w.branchMoved = false
  externalOperationAbsent : w.externalOperationPerformed = false
  terminalMarkerAbsent : w.terminalMarkerWritten = false
  resourceRemovalAbsent : w.resourceRemoved = false

structure RepositoryMutationReviewWitness.Valid
    (w : RepositoryMutationReviewWitness) : Prop where
  caseValid :
    w.ValidApproved ∨ w.ValidDenied ∨ w.ValidRejected
  noRepositoryOrExternalEffect : w.NoRepositoryOrExternalEffect

theorem approved_routes_only_to_repository_mutation_authorization
    (w : RepositoryMutationReviewWitness) (h : w.ValidApproved) :
    w.repositoryMutationAuthorizationRequiredNext = true ∧
      w.repositoryMutationAuthorizationRouteRequiredNext = true ∧
      w.replanRequiredNext = false := by
  exact ⟨h.repositoryMutationAuthorizationRequiredNext,
    h.repositoryMutationAuthorizationRouteRequiredNext,
    h.replanNotRequiredNext⟩

theorem denied_does_not_route_to_repository_mutation_authorization
    (w : RepositoryMutationReviewWitness) (h : w.ValidDenied) :
    w.repositoryMutationAuthorizationRequiredNext = false ∧
      w.repositoryMutationAuthorizationRouteRequiredNext = false ∧
      w.replanRequiredNext = true := by
  exact ⟨h.repositoryMutationAuthorizationNotRequiredNext,
    h.repositoryMutationAuthorizationRouteNotRequiredNext,
    h.replanRequiredNext⟩

theorem rejected_issues_no_repository_review_record
    (w : RepositoryMutationReviewWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.reviewCompleted = false := by
  exact ⟨h.recordNotIssued, h.reviewNotCompleted⟩

theorem valid_repository_review_has_no_repository_or_external_effect
    (w : RepositoryMutationReviewWitness) (h : w.Valid) :
    w.NoRepositoryOrExternalEffect := by
  exact h.noRepositoryOrExternalEffect

end KUOS.WORLD.KuuOSLifecycleBoundedRepositoryMutationReviewV0_26
