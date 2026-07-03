import KUOS.WORLD.KuuOSLifecycleStageV0_18

namespace KUOS.WORLD.KuuOSLifecycleBoundedTransitionPreparationV0_19

inductive PreparationStatus where
  | readyForSeparateApproval
  | blocked
  | rejected
  deriving DecidableEq, Repr

structure PackageWitness where
  sourceDecisionApproved : Bool
  sourceRecomputedValid : Bool
  stateAndRuleBound : Bool
  stepsOrderedAndContinuous : Bool
  rollbackAndRecoveryComplete : Bool
  monitoringAndEvidenceComplete : Bool
  reservationsAndAuthorityComplete : Bool
  irreversibleStepsJustified : Bool
  stopConditionsComplete : Bool
  approvalRouteBound : Bool

structure PackageWitness.Complete (p : PackageWitness) : Prop where
  sourceDecisionApproved : p.sourceDecisionApproved = true
  sourceRecomputedValid : p.sourceRecomputedValid = true
  stateAndRuleBound : p.stateAndRuleBound = true
  stepsOrderedAndContinuous : p.stepsOrderedAndContinuous = true
  rollbackAndRecoveryComplete : p.rollbackAndRecoveryComplete = true
  monitoringAndEvidenceComplete : p.monitoringAndEvidenceComplete = true
  reservationsAndAuthorityComplete :
    p.reservationsAndAuthorityComplete = true
  irreversibleStepsJustified : p.irreversibleStepsJustified = true
  stopConditionsComplete : p.stopConditionsComplete = true
  approvalRouteBound : p.approvalRouteBound = true

structure PreparationWitness where
  package : PackageWitness
  preparerBoundAndSeparated : Bool
  approverAndOperatorSeparated : Bool
  preparerAuthorityVerified : Bool
  status : PreparationStatus
  recordIssued : Bool
  preparationCompleted : Bool
  packagePrepared : Bool
  approvalRequiredNext : Bool
  approvalRouteRequiredNext : Bool
  repreparationRequiredNext : Bool
  repreparationRouteRequiredNext : Bool
  transitionEffectPerformed : Bool
  repositoryEffectPerformed : Bool

structure PreparationWitness.ValidPrepared (w : PreparationWitness) : Prop where
  packageComplete : w.package.Complete
  preparerBoundAndSeparated : w.preparerBoundAndSeparated = true
  approverAndOperatorSeparated : w.approverAndOperatorSeparated = true
  preparerAuthorityVerified : w.preparerAuthorityVerified = true
  statusPrepared : w.status = PreparationStatus.readyForSeparateApproval
  recordIssued : w.recordIssued = true
  preparationCompleted : w.preparationCompleted = true
  packagePrepared : w.packagePrepared = true
  approvalRequiredNext : w.approvalRequiredNext = true
  approvalRouteRequiredNext : w.approvalRouteRequiredNext = true
  repreparationNotRequiredNext : w.repreparationRequiredNext = false
  repreparationRouteNotRequiredNext :
    w.repreparationRouteRequiredNext = false

structure PreparationWitness.ValidBlocked (w : PreparationWitness) : Prop where
  sourceDecisionApproved : w.package.sourceDecisionApproved = true
  statusBlocked : w.status = PreparationStatus.blocked
  recordIssued : w.recordIssued = true
  preparationCompleted : w.preparationCompleted = true
  packageNotPrepared : w.packagePrepared = false
  approvalNotRequiredNext : w.approvalRequiredNext = false
  approvalRouteNotRequiredNext : w.approvalRouteRequiredNext = false
  repreparationRequiredNext : w.repreparationRequiredNext = true
  repreparationRouteRequiredNext : w.repreparationRouteRequiredNext = true

structure PreparationWitness.ValidRejected (w : PreparationWitness) : Prop where
  statusRejected : w.status = PreparationStatus.rejected
  recordNotIssued : w.recordIssued = false
  preparationNotCompleted : w.preparationCompleted = false
  packageNotPrepared : w.packagePrepared = false
  approvalNotRequiredNext : w.approvalRequiredNext = false
  approvalRouteNotRequiredNext : w.approvalRouteRequiredNext = false
  repreparationNotRequiredNext : w.repreparationRequiredNext = false
  repreparationRouteNotRequiredNext : w.repreparationRouteRequiredNext = false

structure PreparationWitness.NoEffects (w : PreparationWitness) : Prop where
  transitionEffectAbsent : w.transitionEffectPerformed = false
  repositoryEffectAbsent : w.repositoryEffectPerformed = false

def PreparationWitness.Valid (w : PreparationWitness) : Prop :=
  (w.ValidPrepared ∨ w.ValidBlocked ∨ w.ValidRejected) ∧ w.NoEffects

theorem prepared_requires_complete_package
    (w : PreparationWitness) (h : w.ValidPrepared) :
    w.package.Complete := by
  exact h.packageComplete

theorem prepared_routes_only_to_separate_approval
    (w : PreparationWitness) (h : w.ValidPrepared) :
    w.packagePrepared = true ∧
      w.approvalRequiredNext = true ∧
      w.approvalRouteRequiredNext = true := by
  exact ⟨h.packagePrepared, h.approvalRequiredNext,
    h.approvalRouteRequiredNext⟩

theorem blocked_routes_to_repreparation
    (w : PreparationWitness) (h : w.ValidBlocked) :
    w.packagePrepared = false ∧
      w.approvalRequiredNext = false ∧
      w.repreparationRequiredNext = true := by
  exact ⟨h.packageNotPrepared, h.approvalNotRequiredNext,
    h.repreparationRequiredNext⟩

theorem rejected_issues_no_record
    (w : PreparationWitness) (h : w.ValidRejected) :
    w.recordIssued = false ∧ w.preparationCompleted = false := by
  exact ⟨h.recordNotIssued, h.preparationNotCompleted⟩

theorem valid_preparation_has_no_effects
    (w : PreparationWitness) (h : w.Valid) : w.NoEffects := by
  exact h.2

structure PreparationDerivation (Input Output : Type) where
  derive : Input → Output

theorem same_input_same_preparation
    {Input Output : Type}
    (d : PreparationDerivation Input Output)
    (left right : Input)
    (h : left = right) : d.derive left = d.derive right := by
  exact congrArg d.derive h

end KUOS.WORLD.KuuOSLifecycleBoundedTransitionPreparationV0_19
