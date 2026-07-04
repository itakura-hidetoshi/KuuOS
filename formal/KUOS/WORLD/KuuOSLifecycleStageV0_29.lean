import KUOS.WORLD.KuuOSLifecycleStageV0_28

namespace KUOS.WORLD.KuuOSLifecycleBoundedRepositoryMutationExecutionV0_29

inductive BoundedRepositoryMutationExecutionStatus where
  | recordedForSeparateExecutionResultReview
  | aborted
  | rejected
  deriving DecidableEq, Repr

structure BoundedRepositoryMutationExecutionWitness where
  sourcePreparationPrepared : Bool
  sourceRecomputedValid : Bool
  sourceMutationExecutionRouteBound : Bool
  resultReviewRouteBound : Bool
  executorAuthorityVerified : Bool
  executorSeparated : Bool
  boundedExecutionReceiptValid : Bool
  packageIntegrityValid : Bool
  sandboxReceiptValid : Bool
  rollbackGuardValid : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : BoundedRepositoryMutationExecutionStatus
  recordIssued : Bool
  executionCompleted : Bool
  resultReviewRequiredNext : Bool
  resultReviewRouteRequiredNext : Bool
  replanRequiredNext : Bool
  repositoryMutationApplied : Bool
  uncontrolledFileWritten : Bool
  uncontrolledRefUpdated : Bool
  uncontrolledBranchMoved : Bool
  externalOperationPerformed : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool

structure BoundedRepositoryMutationExecutionWitness.ValidRecorded
    (w : BoundedRepositoryMutationExecutionWitness) : Prop where
  sourcePreparationPrepared : w.sourcePreparationPrepared = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceMutationExecutionRouteBound : w.sourceMutationExecutionRouteBound = true
  resultReviewRouteBound : w.resultReviewRouteBound = true
  executorAuthorityVerified : w.executorAuthorityVerified = true
  executorSeparated : w.executorSeparated = true
  boundedExecutionReceiptValid : w.boundedExecutionReceiptValid = true
  packageIntegrityValid : w.packageIntegrityValid = true
  sandboxReceiptValid : w.sandboxReceiptValid = true
  rollbackGuardValid : w.rollbackGuardValid = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusRecorded :
    w.status = BoundedRepositoryMutationExecutionStatus.recordedForSeparateExecutionResultReview
  recordIssued : w.recordIssued = true
  executionCompleted : w.executionCompleted = true
  resultReviewRequiredNext : w.resultReviewRequiredNext = true
  resultReviewRouteRequiredNext : w.resultReviewRouteRequiredNext = true
  replanNotRequiredNext : w.replanRequiredNext = false

structure BoundedRepositoryMutationExecutionWitness.ValidAborted
    (w : BoundedRepositoryMutationExecutionWitness) : Prop where
  sourcePreparationPrepared : w.sourcePreparationPrepared = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceMutationExecutionRouteBound : w.sourceMutationExecutionRouteBound = true
  statusAborted : w.status = BoundedRepositoryMutationExecutionStatus.aborted
  recordIssued : w.recordIssued = true
  executionCompleted : w.executionCompleted = true
  resultReviewNotRequiredNext : w.resultReviewRequiredNext = false
  resultReviewRouteNotRequiredNext : w.resultReviewRouteRequiredNext = false
  replanRequiredNext : w.replanRequiredNext = true

structure BoundedRepositoryMutationExecutionWitness.ValidRejected
    (w : BoundedRepositoryMutationExecutionWitness) : Prop where
  statusRejected : w.status = BoundedRepositoryMutationExecutionStatus.rejected
  recordNotIssued : w.recordIssued = false
  executionNotCompleted : w.executionCompleted = false
  resultReviewNotRequiredNext : w.resultReviewRequiredNext = false
  resultReviewRouteNotRequiredNext : w.resultReviewRouteRequiredNext = false
  replanNotRequiredNext : w.replanRequiredNext = false

structure BoundedRepositoryMutationExecutionWitness.NoUncontrolledRepositoryOrExternalEffect
    (w : BoundedRepositoryMutationExecutionWitness) : Prop where
  repositoryMutationNotApplied : w.repositoryMutationApplied = false
  uncontrolledFileWriteAbsent : w.uncontrolledFileWritten = false
  uncontrolledRefUpdateAbsent : w.uncontrolledRefUpdated = false
  uncontrolledBranchMoveAbsent : w.uncontrolledBranchMoved = false
  externalOperationAbsent : w.externalOperationPerformed = false
  terminalMarkerAbsent : w.terminalMarkerWritten = false
  resourceRemovalAbsent : w.resourceRemoved = false

structure BoundedRepositoryMutationExecutionWitness.Valid
    (w : BoundedRepositoryMutationExecutionWitness) : Prop where
  caseValid : w.ValidRecorded ∨ w.ValidAborted ∨ w.ValidRejected
  noUncontrolledEffect : w.NoUncontrolledRepositoryOrExternalEffect

theorem recorded_routes_only_to_execution_result_review
    (w : BoundedRepositoryMutationExecutionWitness) (h : w.ValidRecorded) :
    w.resultReviewRequiredNext = true ∧
      w.resultReviewRouteRequiredNext = true ∧
      w.replanRequiredNext = false := by
  exact ⟨h.resultReviewRequiredNext,
    h.resultReviewRouteRequiredNext,
    h.replanNotRequiredNext⟩

theorem aborted_does_not_route_to_execution_result_review
    (w : BoundedRepositoryMutationExecutionWitness) (h : w.ValidAborted) :
    w.resultReviewRequiredNext = false ∧
      w.resultReviewRouteRequiredNext = false ∧
      w.replanRequiredNext = true := by
  exact ⟨h.resultReviewNotRequiredNext,
    h.resultReviewRouteNotRequiredNext,
    h.replanRequiredNext⟩

theorem rejected_issues_no_bounded_execution_record
    (w : BoundedRepositoryMutationExecutionWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.executionCompleted = false := by
  exact ⟨h.recordNotIssued, h.executionNotCompleted⟩

theorem valid_bounded_execution_has_no_uncontrolled_effect
    (w : BoundedRepositoryMutationExecutionWitness) (h : w.Valid) :
    w.NoUncontrolledRepositoryOrExternalEffect := by
  exact h.noUncontrolledEffect

end KUOS.WORLD.KuuOSLifecycleBoundedRepositoryMutationExecutionV0_29
