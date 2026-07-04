import KUOS.WORLD.KuuOSLifecycleStageV0_30

namespace KUOS.WORLD.KuuOSLifecycleExecutionResultAdoptionV0_31

inductive ExecutionResultAdoptionStatus where
  | adoptedForSeparateLifecycleClosureReview
  | held
  | rejected
  deriving DecidableEq, Repr

structure ExecutionResultAdoptionWitness where
  sourceReviewAccepted : Bool
  sourceRecomputedValid : Bool
  sourceResultAdoptionRouteBound : Bool
  closureReviewRouteBound : Bool
  adopterAuthorityVerified : Bool
  adopterSeparated : Bool
  reviewRecordFresh : Bool
  resultAdoptionReceiptValid : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : ExecutionResultAdoptionStatus
  recordIssued : Bool
  adoptionCompleted : Bool
  closureReviewRequiredNext : Bool
  closureReviewRouteRequiredNext : Bool
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
  closureReviewRouteBound : w.closureReviewRouteBound = true
  adopterAuthorityVerified : w.adopterAuthorityVerified = true
  adopterSeparated : w.adopterSeparated = true
  reviewRecordFresh : w.reviewRecordFresh = true
  resultAdoptionReceiptValid : w.resultAdoptionReceiptValid = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusAdopted :
    w.status = ExecutionResultAdoptionStatus.adoptedForSeparateLifecycleClosureReview
  recordIssued : w.recordIssued = true
  adoptionCompleted : w.adoptionCompleted = true
  closureReviewRequiredNext : w.closureReviewRequiredNext = true
  closureReviewRouteRequiredNext : w.closureReviewRouteRequiredNext = true
  replanNotRequiredNext : w.replanRequiredNext = false

structure ExecutionResultAdoptionWitness.ValidHeld
    (w : ExecutionResultAdoptionWitness) : Prop where
  sourceReviewAccepted : w.sourceReviewAccepted = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceResultAdoptionRouteBound : w.sourceResultAdoptionRouteBound = true
  statusHeld : w.status = ExecutionResultAdoptionStatus.held
  recordIssued : w.recordIssued = true
  adoptionCompleted : w.adoptionCompleted = true
  closureReviewNotRequiredNext : w.closureReviewRequiredNext = false
  closureReviewRouteNotRequiredNext : w.closureReviewRouteRequiredNext = false
  replanRequiredNext : w.replanRequiredNext = true

structure ExecutionResultAdoptionWitness.ValidRejected
    (w : ExecutionResultAdoptionWitness) : Prop where
  statusRejected : w.status = ExecutionResultAdoptionStatus.rejected
  recordNotIssued : w.recordIssued = false
  adoptionNotCompleted : w.adoptionCompleted = false
  closureReviewNotRequiredNext : w.closureReviewRequiredNext = false
  closureReviewRouteNotRequiredNext : w.closureReviewRouteRequiredNext = false
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
  caseValid : w.ValidAdopted ∨ w.ValidHeld ∨ w.ValidRejected
  noRepositoryOrExternalEffect : w.NoRepositoryOrExternalEffect

theorem adopted_routes_only_to_lifecycle_closure_review
    (w : ExecutionResultAdoptionWitness) (h : w.ValidAdopted) :
    w.closureReviewRequiredNext = true ∧
      w.closureReviewRouteRequiredNext = true ∧
      w.replanRequiredNext = false := by
  exact ⟨h.closureReviewRequiredNext,
    h.closureReviewRouteRequiredNext,
    h.replanNotRequiredNext⟩

theorem held_does_not_route_to_lifecycle_closure_review
    (w : ExecutionResultAdoptionWitness) (h : w.ValidHeld) :
    w.closureReviewRequiredNext = false ∧
      w.closureReviewRouteRequiredNext = false ∧
      w.replanRequiredNext = true := by
  exact ⟨h.closureReviewNotRequiredNext,
    h.closureReviewRouteNotRequiredNext,
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
