import KUOS.WORLD.KuuOSLifecycleStageV0_24

namespace KUOS.WORLD.KuuOSLifecycleBoundedStateAdoptionV0_25

inductive StateAdoptionStatus where
  | adoptedForSeparateRepositoryReview
  | denied
  | rejected
  deriving DecidableEq, Repr

structure StateAdoptionWitness where
  sourceCompleted : Bool
  sourceRecomputedValid : Bool
  sourceStateAdoptionRouteBound : Bool
  repositoryReviewRouteBound : Bool
  stateAdopterAuthorityVerified : Bool
  stateAdopterSeparated : Bool
  adoptionReceiptValid : Bool
  packageFresh : Bool
  previousStateNotStale : Bool
  targetStateStillValid : Bool
  noHoldRecoveryOrAnomaly : Bool
  status : StateAdoptionStatus
  recordIssued : Bool
  adoptionCompleted : Bool
  lifecycleStateAdopted : Bool
  lifecycleTransitionPerformed : Bool
  lifecycleStateChanged : Bool
  repositoryReviewRequiredNext : Bool
  repositoryReviewRouteRequiredNext : Bool
  replanRequiredNext : Bool
  authorityChanged : Bool
  repositoryEffectPerformed : Bool
  externalOperationPerformed : Bool

structure StateAdoptionWitness.ValidAdopted
    (w : StateAdoptionWitness) : Prop where
  sourceCompleted : w.sourceCompleted = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceStateAdoptionRouteBound : w.sourceStateAdoptionRouteBound = true
  repositoryReviewRouteBound : w.repositoryReviewRouteBound = true
  stateAdopterAuthorityVerified : w.stateAdopterAuthorityVerified = true
  stateAdopterSeparated : w.stateAdopterSeparated = true
  adoptionReceiptValid : w.adoptionReceiptValid = true
  packageFresh : w.packageFresh = true
  previousStateNotStale : w.previousStateNotStale = true
  targetStateStillValid : w.targetStateStillValid = true
  noHoldRecoveryOrAnomaly : w.noHoldRecoveryOrAnomaly = true
  statusAdopted :
    w.status = StateAdoptionStatus.adoptedForSeparateRepositoryReview
  recordIssued : w.recordIssued = true
  adoptionCompleted : w.adoptionCompleted = true
  lifecycleStateAdopted : w.lifecycleStateAdopted = true
  lifecycleTransitionPerformed : w.lifecycleTransitionPerformed = true
  lifecycleStateChanged : w.lifecycleStateChanged = true
  repositoryReviewRequiredNext : w.repositoryReviewRequiredNext = true
  repositoryReviewRouteRequiredNext : w.repositoryReviewRouteRequiredNext = true
  replanNotRequiredNext : w.replanRequiredNext = false

structure StateAdoptionWitness.ValidDenied
    (w : StateAdoptionWitness) : Prop where
  sourceCompleted : w.sourceCompleted = true
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceStateAdoptionRouteBound : w.sourceStateAdoptionRouteBound = true
  statusDenied : w.status = StateAdoptionStatus.denied
  recordIssued : w.recordIssued = true
  adoptionCompleted : w.adoptionCompleted = true
  lifecycleStateNotAdopted : w.lifecycleStateAdopted = false
  lifecycleTransitionNotPerformed : w.lifecycleTransitionPerformed = false
  lifecycleStateUnchanged : w.lifecycleStateChanged = false
  repositoryReviewNotRequiredNext : w.repositoryReviewRequiredNext = false
  repositoryReviewRouteNotRequiredNext :
    w.repositoryReviewRouteRequiredNext = false
  replanRequiredNext : w.replanRequiredNext = true

structure StateAdoptionWitness.ValidRejected
    (w : StateAdoptionWitness) : Prop where
  statusRejected : w.status = StateAdoptionStatus.rejected
  recordNotIssued : w.recordIssued = false
  adoptionNotCompleted : w.adoptionCompleted = false
  lifecycleStateNotAdopted : w.lifecycleStateAdopted = false
  lifecycleTransitionNotPerformed : w.lifecycleTransitionPerformed = false
  lifecycleStateUnchanged : w.lifecycleStateChanged = false
  repositoryReviewNotRequiredNext : w.repositoryReviewRequiredNext = false
  repositoryReviewRouteNotRequiredNext :
    w.repositoryReviewRouteRequiredNext = false
  replanNotRequiredNext : w.replanRequiredNext = false

structure StateAdoptionWitness.NoRepositoryOrExternalEffect
    (w : StateAdoptionWitness) : Prop where
  authorityUnchanged : w.authorityChanged = false
  repositoryEffectAbsent : w.repositoryEffectPerformed = false
  externalOperationAbsent : w.externalOperationPerformed = false

structure StateAdoptionWitness.Valid
    (w : StateAdoptionWitness) : Prop where
  caseValid :
    w.ValidAdopted ∨ w.ValidDenied ∨ w.ValidRejected
  noRepositoryOrExternalEffect : w.NoRepositoryOrExternalEffect

theorem adopted_routes_only_to_repository_review
    (w : StateAdoptionWitness) (h : w.ValidAdopted) :
    w.lifecycleStateAdopted = true ∧
      w.repositoryReviewRequiredNext = true ∧
      w.repositoryReviewRouteRequiredNext = true := by
  exact ⟨h.lifecycleStateAdopted, h.repositoryReviewRequiredNext,
    h.repositoryReviewRouteRequiredNext⟩

theorem denied_does_not_route_to_repository_review
    (w : StateAdoptionWitness) (h : w.ValidDenied) :
    w.lifecycleStateAdopted = false ∧
      w.repositoryReviewRequiredNext = false ∧
      w.replanRequiredNext = true := by
  exact ⟨h.lifecycleStateNotAdopted, h.repositoryReviewNotRequiredNext,
    h.replanRequiredNext⟩

theorem rejected_issues_no_record
    (w : StateAdoptionWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.adoptionCompleted = false := by
  exact ⟨h.recordNotIssued, h.adoptionNotCompleted⟩

theorem valid_adoption_has_no_repository_or_external_effect
    (w : StateAdoptionWitness) (h : w.Valid) :
    w.NoRepositoryOrExternalEffect := by
  exact h.noRepositoryOrExternalEffect

end KUOS.WORLD.KuuOSLifecycleBoundedStateAdoptionV0_25
