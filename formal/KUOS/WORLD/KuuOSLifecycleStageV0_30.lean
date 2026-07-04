import KUOS.WORLD.KuuOSLifecycleStageV0_29

namespace KUOS.WORLD.KuuOSLifecycleExecutionResultReviewV0_30

inductive ExecutionResultReviewStatus where
  | acceptedForSeparateResultAdoption
  | failed
  | rejected
  deriving DecidableEq, Repr

structure ExecutionResultReviewWitness where
  sourceExecutionRecorded : Bool
  sourceRecomputedValid : Bool
  sourceResultReviewRouteBound : Bool
  resultAdoptionRouteBound : Bool
  resultReviewerAuthorityVerified : Bool
  resultReviewerSeparated : Bool
  executionRecordFresh : Bool
  boundedExecutionReceiptFresh : Bool
  resultConsistencyValid : Bool
  sourceTraceValid : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : ExecutionResultReviewStatus
  recordIssued : Bool
  reviewCompleted : Bool
  resultAdoptionRequiredNext : Bool
  resultAdoptionRouteRequiredNext : Bool
  replanRequiredNext : Bool
  repositoryChanged : Bool
  fileWritten : Bool
  refUpdated : Bool
  branchMoved : Bool
  externalOperationPerformed : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool

structure ExecutionResultReviewWitness.ValidAccepted
    (w : ExecutionResultReviewWitness) : Prop where
  sourceExecutionRecorded : w.sourceExecutionRecorded = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceResultReviewRouteBound : w.sourceResultReviewRouteBound = true
  resultAdoptionRouteBound : w.resultAdoptionRouteBound = true
  resultReviewerAuthorityVerified : w.resultReviewerAuthorityVerified = true
  resultReviewerSeparated : w.resultReviewerSeparated = true
  executionRecordFresh : w.executionRecordFresh = true
  boundedExecutionReceiptFresh : w.boundedExecutionReceiptFresh = true
  resultConsistencyValid : w.resultConsistencyValid = true
  sourceTraceValid : w.sourceTraceValid = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusAccepted : w.status = ExecutionResultReviewStatus.acceptedForSeparateResultAdoption
  recordIssued : w.recordIssued = true
  reviewCompleted : w.reviewCompleted = true
  resultAdoptionRequiredNext : w.resultAdoptionRequiredNext = true
  resultAdoptionRouteRequiredNext : w.resultAdoptionRouteRequiredNext = true
  replanNotRequiredNext : w.replanRequiredNext = false

structure ExecutionResultReviewWitness.ValidFailed
    (w : ExecutionResultReviewWitness) : Prop where
  sourceExecutionRecorded : w.sourceExecutionRecorded = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceResultReviewRouteBound : w.sourceResultReviewRouteBound = true
  statusFailed : w.status = ExecutionResultReviewStatus.failed
  recordIssued : w.recordIssued = true
  reviewCompleted : w.reviewCompleted = true
  resultAdoptionNotRequiredNext : w.resultAdoptionRequiredNext = false
  resultAdoptionRouteNotRequiredNext : w.resultAdoptionRouteRequiredNext = false
  replanRequiredNext : w.replanRequiredNext = true

structure ExecutionResultReviewWitness.ValidRejected
    (w : ExecutionResultReviewWitness) : Prop where
  statusRejected : w.status = ExecutionResultReviewStatus.rejected
  recordNotIssued : w.recordIssued = false
  reviewNotCompleted : w.reviewCompleted = false
  resultAdoptionNotRequiredNext : w.resultAdoptionRequiredNext = false
  resultAdoptionRouteNotRequiredNext : w.resultAdoptionRouteRequiredNext = false
  replanNotRequiredNext : w.replanRequiredNext = false

structure ExecutionResultReviewWitness.NoRepositoryOrExternalEffect
    (w : ExecutionResultReviewWitness) : Prop where
  repositoryChangeAbsent : w.repositoryChanged = false
  fileWriteAbsent : w.fileWritten = false
  refUpdateAbsent : w.refUpdated = false
  branchMoveAbsent : w.branchMoved = false
  externalOperationAbsent : w.externalOperationPerformed = false
  terminalMarkerAbsent : w.terminalMarkerWritten = false
  resourceRemovalAbsent : w.resourceRemoved = false

structure ExecutionResultReviewWitness.Valid
    (w : ExecutionResultReviewWitness) : Prop where
  caseValid : w.ValidAccepted ∨ w.ValidFailed ∨ w.ValidRejected
  noRepositoryOrExternalEffect : w.NoRepositoryOrExternalEffect

theorem accepted_routes_only_to_execution_result_adoption
    (w : ExecutionResultReviewWitness) (h : w.ValidAccepted) :
    w.resultAdoptionRequiredNext = true ∧
      w.resultAdoptionRouteRequiredNext = true ∧
      w.replanRequiredNext = false := by
  exact ⟨h.resultAdoptionRequiredNext,
    h.resultAdoptionRouteRequiredNext,
    h.replanNotRequiredNext⟩

theorem failed_does_not_route_to_execution_result_adoption
    (w : ExecutionResultReviewWitness) (h : w.ValidFailed) :
    w.resultAdoptionRequiredNext = false ∧
      w.resultAdoptionRouteRequiredNext = false ∧
      w.replanRequiredNext = true := by
  exact ⟨h.resultAdoptionNotRequiredNext,
    h.resultAdoptionRouteNotRequiredNext,
    h.replanRequiredNext⟩

theorem rejected_issues_no_execution_result_review_record
    (w : ExecutionResultReviewWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.reviewCompleted = false := by
  exact ⟨h.recordNotIssued, h.reviewNotCompleted⟩

theorem valid_execution_result_review_has_no_repository_or_external_effect
    (w : ExecutionResultReviewWitness) (h : w.Valid) :
    w.NoRepositoryOrExternalEffect := by
  exact h.noRepositoryOrExternalEffect

end KUOS.WORLD.KuuOSLifecycleExecutionResultReviewV0_30
