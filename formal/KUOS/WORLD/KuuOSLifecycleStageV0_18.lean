import KUOS.WORLD.KuuOSLifecycleStageV0_17

namespace KUOS.WORLD.KuuOSLifecycleBoundedTransitionDecisionV0_18

inductive TransitionDecisionStatus where
  | approvedForSeparateTransitionPreparation
  | denied
  | rejected
  deriving DecidableEq, Repr

structure LifecycleStateWitness where
  stateDigest : String
  stateRevision : Nat

structure TransitionRelationWitness where
  currentState : LifecycleStateWitness
  targetState : LifecycleStateWitness
  transitionKind : String
  ruleCurrentStateDigest : String
  ruleTargetStateDigest : String
  ruleTransitionKind : String
  ruleActive : Bool

structure TransitionRelationWitness.Allowed
    (r : TransitionRelationWitness) : Prop where
  ruleActive : r.ruleActive = true
  currentStateBound :
    r.ruleCurrentStateDigest = r.currentState.stateDigest
  targetStateBound :
    r.ruleTargetStateDigest = r.targetState.stateDigest
  transitionKindBound :
    r.ruleTransitionKind = r.transitionKind
  stateChanged :
    r.currentState.stateDigest ≠ r.targetState.stateDigest
  revisionAdvanced :
    r.currentState.stateRevision < r.targetState.stateRevision

structure DecisionEffects where
  lifecycleTransitionPrepared : Bool
  lifecycleTransitionApproved : Bool
  lifecycleTransitionStarted : Bool
  lifecycleTransitionCompleted : Bool
  lifecycleTransitionPerformed : Bool
  authorityChanged : Bool
  quiescenceStateChanged : Bool
  terminalStateChanged : Bool
  terminalMarkerWritten : Bool
  resourceRemoved : Bool
  externalOperationPerformed : Bool
  repositoryChanged : Bool

structure DecisionEffects.NonePerformed
    (e : DecisionEffects) : Prop where
  transitionNotPrepared : e.lifecycleTransitionPrepared = false
  transitionNotApproved : e.lifecycleTransitionApproved = false
  transitionNotStarted : e.lifecycleTransitionStarted = false
  transitionNotCompleted : e.lifecycleTransitionCompleted = false
  transitionNotPerformed : e.lifecycleTransitionPerformed = false
  authorityNotChanged : e.authorityChanged = false
  quiescenceStateNotChanged : e.quiescenceStateChanged = false
  terminalStateNotChanged : e.terminalStateChanged = false
  terminalMarkerNotWritten : e.terminalMarkerWritten = false
  resourceNotRemoved : e.resourceRemoved = false
  externalOperationNotPerformed : e.externalOperationPerformed = false
  repositoryNotChanged : e.repositoryChanged = false

structure TransitionDecisionWitness where
  sourceRecomputedValid : Bool
  sourceTransitionReviewClear : Bool
  sourceTransitionReviewCompleted : Bool
  sourceBindingValid : Bool
  stateSnapshotBindingValid : Bool
  currentStateNotStale : Bool
  preparationRouteBindingValid : Bool
  decisionMakerSeparatedFromSourceReviewer : Bool
  decisionMakerSeparatedFromPriorActors : Bool
  decisionMakerSeparatedFromPreparer : Bool
  decisionMakerOrganizationSeparated : Bool
  decisionMakerMandateVerified : Bool
  decisionMakerQualified : Bool
  decisionMakerIdentityConfirmed : Bool
  decisionReady : Bool
  transitionRelation : TransitionRelationWitness
  transitionRelationAllowed : Bool
  decisionApproved : Bool
  status : TransitionDecisionStatus
  transitionDecisionRecordIssued : Bool
  transitionDecisionMade : Bool
  transitionApprovedForPreparation : Bool
  transitionDenied : Bool
  transitionPreparationRequiredNext : Bool
  transitionPreparationRouteRequiredNext : Bool
  appealOrReconsiderationAvailable : Bool
  decisionEffects : DecisionEffects

structure TransitionDecisionWitness.ValidApproved
    (w : TransitionDecisionWitness) : Prop where
  sourceRecomputedValid : w.sourceRecomputedValid = true
  sourceTransitionReviewClear : w.sourceTransitionReviewClear = true
  sourceTransitionReviewCompleted :
    w.sourceTransitionReviewCompleted = true
  sourceBindingValid : w.sourceBindingValid = true
  stateSnapshotBindingValid : w.stateSnapshotBindingValid = true
  currentStateNotStale : w.currentStateNotStale = true
  preparationRouteBindingValid : w.preparationRouteBindingValid = true
  decisionMakerSeparatedFromSourceReviewer :
    w.decisionMakerSeparatedFromSourceReviewer = true
  decisionMakerSeparatedFromPriorActors :
    w.decisionMakerSeparatedFromPriorActors = true
  decisionMakerSeparatedFromPreparer :
    w.decisionMakerSeparatedFromPreparer = true
  decisionMakerOrganizationSeparated :
    w.decisionMakerOrganizationSeparated = true
  decisionMakerMandateVerified : w.decisionMakerMandateVerified = true
  decisionMakerQualified : w.decisionMakerQualified = true
  decisionMakerIdentityConfirmed : w.decisionMakerIdentityConfirmed = true
  decisionReady : w.decisionReady = true
  transitionRelationAllowed : w.transitionRelationAllowed = true
  relationAllowed : w.transitionRelation.Allowed
  decisionApproved : w.decisionApproved = true
  statusApproved :
    w.status =
      TransitionDecisionStatus.approvedForSeparateTransitionPreparation
  transitionDecisionRecordIssued :
    w.transitionDecisionRecordIssued = true
  transitionDecisionMade : w.transitionDecisionMade = true
  transitionApprovedForPreparation :
    w.transitionApprovedForPreparation = true
  transitionNotDenied : w.transitionDenied = false
  transitionPreparationRequiredNext :
    w.transitionPreparationRequiredNext = true
  transitionPreparationRouteRequiredNext :
    w.transitionPreparationRouteRequiredNext = true
  appealOrReconsiderationNotRequired :
    w.appealOrReconsiderationAvailable = false

structure TransitionDecisionWitness.ValidDenied
    (w : TransitionDecisionWitness) : Prop where
  sourceTransitionReviewClear : w.sourceTransitionReviewClear = true
  sourceTransitionReviewCompleted :
    w.sourceTransitionReviewCompleted = true
  transitionRelationAllowed : w.transitionRelationAllowed = true
  relationAllowed : w.transitionRelation.Allowed
  decisionNotApproved : w.decisionApproved = false
  statusDenied : w.status = TransitionDecisionStatus.denied
  transitionDecisionRecordIssued :
    w.transitionDecisionRecordIssued = true
  transitionDecisionMade : w.transitionDecisionMade = true
  transitionNotApprovedForPreparation :
    w.transitionApprovedForPreparation = false
  transitionDenied : w.transitionDenied = true
  transitionPreparationNotRequiredNext :
    w.transitionPreparationRequiredNext = false
  transitionPreparationRouteNotRequiredNext :
    w.transitionPreparationRouteRequiredNext = false
  appealOrReconsiderationAvailable :
    w.appealOrReconsiderationAvailable = true

structure TransitionDecisionWitness.ValidRejected
    (w : TransitionDecisionWitness) : Prop where
  statusRejected : w.status = TransitionDecisionStatus.rejected
  transitionDecisionRecordNotIssued :
    w.transitionDecisionRecordIssued = false
  transitionDecisionNotMade : w.transitionDecisionMade = false
  transitionNotApprovedForPreparation :
    w.transitionApprovedForPreparation = false
  transitionNotDenied : w.transitionDenied = false
  transitionPreparationNotRequiredNext :
    w.transitionPreparationRequiredNext = false
  transitionPreparationRouteNotRequiredNext :
    w.transitionPreparationRouteRequiredNext = false
  appealOrReconsiderationNotAvailable :
    w.appealOrReconsiderationAvailable = false

def TransitionDecisionWitness.Valid
    (w : TransitionDecisionWitness) : Prop :=
  (w.ValidApproved ∨ w.ValidDenied ∨ w.ValidRejected) ∧
    w.decisionEffects.NonePerformed

theorem approved_requires_allowed_transition_relation
    (w : TransitionDecisionWitness)
    (h : w.ValidApproved) :
    w.sourceTransitionReviewClear = true ∧
      w.currentStateNotStale = true ∧
      w.transitionRelation.Allowed := by
  exact ⟨h.sourceTransitionReviewClear,
    h.currentStateNotStale,
    h.relationAllowed⟩

theorem approved_routes_only_to_separate_transition_preparation
    (w : TransitionDecisionWitness)
    (h : w.ValidApproved) :
    w.transitionDecisionMade = true ∧
      w.transitionPreparationRequiredNext = true ∧
      w.transitionPreparationRouteRequiredNext = true ∧
      w.decisionEffects.lifecycleTransitionPerformed = false := by
  exact ⟨h.transitionDecisionMade,
    h.transitionPreparationRequiredNext,
    h.transitionPreparationRouteRequiredNext,
    rfl⟩

theorem denied_issues_record_without_preparation
    (w : TransitionDecisionWitness)
    (h : w.ValidDenied) :
    w.transitionDecisionRecordIssued = true ∧
      w.transitionDecisionMade = true ∧
      w.transitionPreparationRequiredNext = false ∧
      w.appealOrReconsiderationAvailable = true := by
  exact ⟨h.transitionDecisionRecordIssued,
    h.transitionDecisionMade,
    h.transitionPreparationNotRequiredNext,
    h.appealOrReconsiderationAvailable⟩

theorem rejected_issues_no_valid_decision_record
    (w : TransitionDecisionWitness)
    (h : w.ValidRejected) :
    w.transitionDecisionRecordIssued = false ∧
      w.transitionDecisionMade = false ∧
      w.transitionPreparationRequiredNext = false := by
  exact ⟨h.transitionDecisionRecordNotIssued,
    h.transitionDecisionNotMade,
    h.transitionPreparationNotRequiredNext⟩

theorem valid_decision_performs_no_transition_or_repository_effect
    (w : TransitionDecisionWitness)
    (h : w.Valid) :
    w.decisionEffects.NonePerformed := by
  exact h.2

structure TransitionDecisionDerivation (Input Output : Type) where
  derive : Input → Output

theorem same_input_has_same_transition_decision
    {Input Output : Type}
    (derivation : TransitionDecisionDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSLifecycleBoundedTransitionDecisionV0_18
