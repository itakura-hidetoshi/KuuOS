namespace KUOS.WORLD.DukkhaPreservingSingleUseWorldMutationApplicationIntakeV0_62

inductive ApplicationDisposition where
  | ready
  | worldRefresh
  | contextRefresh
  | reviewRefresh
  | authorizationExpired
  | authorizationRevalidation
  | patchRepair
  | preconditionRepair
  | engineRejected
  | atomicityRepair
  | postconditionObservation
  | provenanceRepair
  | nonexternalizationReview
  | dukkhaReview
  | compensationRepair
  | truthPromotionRejected
  | replayRejected
  deriving DecidableEq, Repr

structure Intake where
  sourceReceiptRevalidated : Bool
  authorizationValid : Bool
  candidateIdentityMatch : Bool
  patchIdentityMatch : Bool
  preconditionsSatisfied : Bool
  mutationEngineAdmitted : Bool
  atomicApplicationSupported : Bool
  postconditionObservationReady : Bool
  lineagePreserved : Bool
  responsibilityPreserved : Bool
  protectedGroupNonexternalization : Bool
  futureNonexternalization : Bool
  dukkhaPreservationSupported : Bool
  compensationRouteReady : Bool
  truthPromotionClaimed : Bool
  replayFresh : Bool
  worldCurrent : Bool
  contextCurrent : Bool
  reviewCurrent : Bool
  authorizationCurrent : Bool

structure Receipt where
  disposition : ApplicationDisposition
  mutationApplied : Bool
  authorizationConsumed : Bool
  candidateCommitCompleted : Bool
  persistentWorldChanged : Bool
  revisionIncrementedOnce : Bool
  postApplicationVerificationCompleted : Bool
  worldFactConfirmed : Bool
  causalAttributionConfirmed : Bool
  dukkhaRealizationConfirmed : Bool
  generalWorldMutationAuthority : Bool
  externalSideEffectOutsideBound : Bool
  compensationPerformed : Bool


def route (i : Intake) : ApplicationDisposition :=
  if !i.replayFresh then .replayRejected
  else if !i.worldCurrent then .worldRefresh
  else if !i.contextCurrent then .contextRefresh
  else if !i.reviewCurrent then .reviewRefresh
  else if !i.authorizationCurrent then .authorizationExpired
  else if i.truthPromotionClaimed then .truthPromotionRejected
  else if !i.sourceReceiptRevalidated || !i.authorizationValid then .authorizationRevalidation
  else if !i.candidateIdentityMatch || !i.patchIdentityMatch then .patchRepair
  else if !i.preconditionsSatisfied then .preconditionRepair
  else if !i.mutationEngineAdmitted then .engineRejected
  else if !i.atomicApplicationSupported then .atomicityRepair
  else if !i.postconditionObservationReady then .postconditionObservation
  else if !i.lineagePreserved || !i.responsibilityPreserved then .provenanceRepair
  else if !i.protectedGroupNonexternalization || !i.futureNonexternalization then .nonexternalizationReview
  else if !i.dukkhaPreservationSupported then .dukkhaReview
  else if !i.compensationRouteReady then .compensationRepair
  else .ready


def issue (i : Intake) : Receipt :=
  let ready := route i == .ready
  {
    disposition := route i
    mutationApplied := ready
    authorizationConsumed := ready
    candidateCommitCompleted := ready
    persistentWorldChanged := ready
    revisionIncrementedOnce := ready
    postApplicationVerificationCompleted := false
    worldFactConfirmed := false
    causalAttributionConfirmed := false
    dukkhaRealizationConfirmed := false
    generalWorldMutationAuthority := false
    externalSideEffectOutsideBound := false
    compensationPerformed := false
  }


theorem ready_applies_once (i : Intake) (h : route i = .ready) :
    (issue i).mutationApplied = true ∧
    (issue i).authorizationConsumed = true ∧
    (issue i).candidateCommitCompleted = true ∧
    (issue i).persistentWorldChanged = true ∧
    (issue i).revisionIncrementedOnce = true := by
  simp [issue, h]


theorem nonready_does_not_apply (i : Intake) (h : route i ≠ .ready) :
    (issue i).mutationApplied = false ∧
    (issue i).authorizationConsumed = false ∧
    (issue i).candidateCommitCompleted = false ∧
    (issue i).persistentWorldChanged = false := by
  simp [issue, h]


theorem application_is_not_fact_promotion (i : Intake) :
    (issue i).postApplicationVerificationCompleted = false ∧
    (issue i).worldFactConfirmed = false ∧
    (issue i).causalAttributionConfirmed = false ∧
    (issue i).dukkhaRealizationConfirmed = false := by
  simp [issue]


theorem bounded_application_grants_no_general_authority (i : Intake) :
    (issue i).generalWorldMutationAuthority = false ∧
    (issue i).externalSideEffectOutsideBound = false ∧
    (issue i).compensationPerformed = false := by
  simp [issue]

end KUOS.WORLD.DukkhaPreservingSingleUseWorldMutationApplicationIntakeV0_62
