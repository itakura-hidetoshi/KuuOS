import KUOS.WORLD.KuuOSRepositoryCheckpointReflogV1_24

namespace KUOS.WORLD.KuuOSCheckpointRecoveryProposalV0_1

inductive RecoveryProposalStatus where
  | proposed
  | rejected
  deriving DecidableEq, Repr

structure RecoveryProposalWitness where
  sourceV124ResultAccepted : Prop
  sourceBindingExact : Prop
  requestorAuthorized : Prop
  targetReferenceAllowed : Prop
  sourceTargetDistinct : Prop
  objectiveCompareOnly : Bool
  status : RecoveryProposalStatus
  comparisonRequired : Bool
  sourceTargetComparisonPerformed : Bool
  externalReviewRequired : Bool
  explicitAuthorizationDecisionRequired : Bool
  recoveryAuthorityGranted : Bool
  liveGitExecutionPerformed : Bool
  repositoryMutationPerformed : Bool
  continuesV124MutationSeries : Bool

structure RecoveryProposalWitness.ValidProposed
    (w : RecoveryProposalWitness) : Prop where
  sourceV124ResultAccepted : w.sourceV124ResultAccepted
  sourceBindingExact : w.sourceBindingExact
  requestorAuthorized : w.requestorAuthorized
  targetReferenceAllowed : w.targetReferenceAllowed
  sourceTargetDistinct : w.sourceTargetDistinct
  objectiveCompareOnly : w.objectiveCompareOnly = true
  statusProposed : w.status = RecoveryProposalStatus.proposed
  comparisonRequired : w.comparisonRequired = true
  sourceTargetComparisonNotPerformed :
    w.sourceTargetComparisonPerformed = false
  externalReviewRequired : w.externalReviewRequired = true
  explicitAuthorizationDecisionRequired :
    w.explicitAuthorizationDecisionRequired = true
  recoveryAuthorityNotGranted : w.recoveryAuthorityGranted = false
  liveGitExecutionNotPerformed : w.liveGitExecutionPerformed = false
  repositoryMutationNotPerformed : w.repositoryMutationPerformed = false
  doesNotContinueV124MutationSeries :
    w.continuesV124MutationSeries = false

structure RecoveryProposalWitness.ValidRejected
    (w : RecoveryProposalWitness) : Prop where
  statusRejected : w.status = RecoveryProposalStatus.rejected
  comparisonNotRequired : w.comparisonRequired = false
  sourceTargetComparisonNotPerformed :
    w.sourceTargetComparisonPerformed = false
  externalReviewNotRequired : w.externalReviewRequired = false
  explicitAuthorizationDecisionNotRequired :
    w.explicitAuthorizationDecisionRequired = false
  recoveryAuthorityNotGranted : w.recoveryAuthorityGranted = false
  liveGitExecutionNotPerformed : w.liveGitExecutionPerformed = false
  repositoryMutationNotPerformed : w.repositoryMutationPerformed = false
  doesNotContinueV124MutationSeries :
    w.continuesV124MutationSeries = false


theorem valid_proposal_requires_comparison_review_and_decision
    (w : RecoveryProposalWitness)
    (h : w.ValidProposed) :
    w.comparisonRequired = true ∧
      w.sourceTargetComparisonPerformed = false ∧
      w.externalReviewRequired = true ∧
      w.explicitAuthorizationDecisionRequired = true := by
  exact ⟨h.comparisonRequired, h.sourceTargetComparisonNotPerformed,
    h.externalReviewRequired, h.explicitAuthorizationDecisionRequired⟩


theorem valid_proposal_grants_no_recovery_authority
    (w : RecoveryProposalWitness)
    (h : w.ValidProposed) :
    w.recoveryAuthorityGranted = false ∧
      w.liveGitExecutionPerformed = false ∧
      w.repositoryMutationPerformed = false := by
  exact ⟨h.recoveryAuthorityNotGranted,
    h.liveGitExecutionNotPerformed,
    h.repositoryMutationNotPerformed⟩


theorem recovery_proposal_is_not_v124_mutation_continuation
    (w : RecoveryProposalWitness)
    (h : w.ValidProposed ∨ w.ValidRejected) :
    w.continuesV124MutationSeries = false := by
  rcases h with h | h
  · exact h.doesNotContinueV124MutationSeries
  · exact h.doesNotContinueV124MutationSeries


structure RecoveryProposalDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_recovery_proposal
    {Input Output : Type}
    (derivation : RecoveryProposalDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSCheckpointRecoveryProposalV0_1
