import KUOS.WORLD.KuuOSLifecycleStageV0_30

namespace KUOS.WORLD.KuuOSLifecycleExecutionResultAdoptionV0_31

inductive ExecutionResultAdoptionStatus where
  | adoptedForSeparateCompletionReview
  | deferred
  | rejected
  deriving DecidableEq, Repr

structure ExecutionResultAdoptionWitness where
  sourceReviewAccepted : Bool
  sourceRecomputedValid : Bool
  sourceResultAdoptionRouteBound : Bool
  completionReviewRouteBound : Bool
  adopterAuthorityVerified : Bool
  adopterSeparated : Bool
  resultReviewRecordFresh : Bool
  adoptionConsistencyValid : Bool
  completionScopeValid : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : ExecutionResultAdoptionStatus
  recordIssued : Bool
  adoptionCompleted : Bool
  completionReviewRequiredNext : Bool
  completionReviewRouteRequiredNext : Bool
  replanRequiredNext : Bool
  repositoryChanged : Bool
  fileWritten : Bool
  refUpdated : Bool
  branchMoved : Bool
  externalOperationPerformed : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool

structure ExecutionResultAdoptionWitness.ValidAdopted
    (w : ExecutionResultAdoptionWitness) : Prop where
  sourceReviewAccepted : w.sourceReviewAccepted = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceResultAdoptionRouteBound : w.sourceResultAdoptionRouteBound = true
  completionReviewRouteBound : w.completionReviewRouteBound = true
  adopterAuthorityVerified : w.adopterAuthorityVerified = true
  adopterSeparated : w.adopterSeparated = true
  resultReviewRecordFresh : w.resultReviewRecordFresh = true
  adoptionConsistencyValid : w.adoptionConsistencyValid = true
  completionScopeValid : w.completionScopeValid = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusAdopted : w.status = ExecutionResultAdoptionStatus.adoptedForSeparateCompletionReview
  recordIssued : w.recordIssued = true
  adoptionCompleted : w.adoptionCompleted = true
  completionReviewRequiredNext : w.completionReviewRequiredNext = true
  completionReviewRouteRequiredNext : w.completionReviewRouteRequiredNext = true
  replanNotRequiredNext : w.replanRequiredNext = false

structure ExecutionResultAdoptionWitness.ValidDeferred
    (w : ExecutionResultAdoptionWitness) : Prop where
  sourceReviewAccepted : w.sourceReviewAccepted = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceResultAdoptionRouteBound : w.sourceResultAdoptionRouteBound = true
  statusDeferred : w.status = ExecutionResultAdoptionStatus.deferred
  recordIssued : w.recordIssued = true
  adoptionCompleted : w.adoptionCompleted = true
  completionReviewNotRequiredNext : w.completionReviewRequiredNext = false
  completionReviewRouteNotRequiredNext : w.completionReviewRouteRequiredNext = false
  replanRequiredNext : w.replanRequiredNext = true

structure ExecutionResultAdoptionWitness.ValidRejected
    (w : ExecutionResultAdoptionWitness) : Prop where
  statusRejected : w.status = ExecutionResultAdoptionStatus.rejected
  recordNotIssued : w.recordIssued = false
  adoptionNotCompleted : w.adoptionCompleted = false
  completionReviewNotRequiredNext : w.completionReviewRequiredNext = false
  completionReviewRouteNotRequiredNext : w.completionReviewRouteRequiredNext = false
  replanNotRequiredNext : w.replanRequiredNext = false

structure ExecutionResultAdoptionWitness.NoRepositoryOrExternalEffect
    (w : ExecutionResultAdoptionWitness) : Prop where
  repositoryChangeAbsent : w.repositoryChanged = false
  fileWriteAbsent : w.fileWritten = false
  refUpdateAbsent : w.refUpdated = false
  branchMoveAbsent : w.branchMoved = false
  externalOperationAbsent : w.externalOperationPerformed = false
  terminalMarkerAbsent : w.terminalMarkerWritten = false
  resourceRemovalAbsent : w.resourceRemoved = false

structure ExecutionResultAdoptionWitness.Valid
    (w : ExecutionResultAdoptionWitness) : Prop where
  caseValid : w.ValidAdopted ∨ w.ValidDeferred ∨ w.ValidRejected
  noRepositoryOrExternalEffect : w.NoRepositoryOrExternalEffect

theorem adopted_routes_only_to_completion_review
    (w : ExecutionResultAdoptionWitness) (h : w.ValidAdopted) :
    w.completionReviewRequiredNext = true ∧
      w.completionReviewRouteRequiredNext = true ∧
      w.replanRequiredNext = false := by
  exact ⟨h.completionReviewRequiredNext,
    h.completionReviewRouteRequiredNext,
    h.replanNotRequiredNext⟩

theorem deferred_does_not_route_to_completion_review
    (w : ExecutionResultAdoptionWitness) (h : w.ValidDeferred) :
    w.completionReviewRequiredNext = false ∧
      w.completionReviewRouteRequiredNext = false ∧
      w.replanRequiredNext = true := by
  exact ⟨h.completionReviewNotRequiredNext,
    h.completionReviewRouteNotRequiredNext,
    h.replanRequiredNext⟩

theorem rejected_issues_no_execution_result_adoption_record
    (w : ExecutionResultAdoptionWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.adoptionCompleted = false := by
  exact ⟨h.recordNotIssued, h.adoptionNotCompleted⟩

theorem valid_execution_result_adoption_has_no_repository_or_external_effect
    (w : ExecutionResultAdoptionWitness) (h : w.Valid) :
    w.NoRepositoryOrExternalEffect := by
  exact h.noRepositoryOrExternalEffect

end KUOS.WORLD.KuuOSLifecycleExecutionResultAdoptionV0_31
