import KUOS.WORLD.KuuOSApoptosisExternalReviewV0_6

namespace KUOS.WORLD.KuuOSApoptosisIndependentAuthorizationV0_7

inductive IndependentAuthorizationStatus where
  | approvedForBoundedExecutionPreparation
  | denied
  | rejected
  deriving DecidableEq, Repr

structure ApoptosisIndependentAuthorizationWitness where
  sourceExternalReviewRecomputedValid : Bool
  sourceExternalReviewClear : Bool
  sourceBindingValid : Bool
  externalAuthorityDesignationBindingValid : Bool
  authorityMandateVerified : Bool
  authorityQualified : Bool
  authorityIndependentFromPriorChain : Bool
  authorityIndependentFromExecutionAuthority : Bool
  conflictDisclosureComplete : Bool
  materialConflictPresent : Bool
  jurisdictionVerified : Bool
  quorumSatisfied : Bool
  reasonedDecisionComplete : Bool
  proportionalitySatisfied : Bool
  lessRestrictiveAlternativesExhausted : Bool
  irreversibilityReviewComplete : Bool
  humanImpactReviewComplete : Bool
  appealRoutePresent : Bool
  dissentRoutePresent : Bool
  protectedCoreExcluded : Bool
  institutionalHoldActive : Bool
  emergencyStateActive : Bool
  authorizationFresh : Bool
  authorizationNotExpired : Bool
  status : IndependentAuthorizationStatus
  authorizationRecordIssued : Bool
  authorizationDecisionMade : Bool
  authorizationApproved : Bool
  authorizationDenied : Bool
  boundedExecutionPreparationAllowedNext : Bool
  executionAuthorityRequiredNext : Bool
  executionRequestIssued : Bool
  executionDecisionMade : Bool
  authorityRevocationPerformed : Bool
  quiescenceTransitionPerformed : Bool
  terminalTransitionPerformed : Bool
  tombstoneWritePerformed : Bool
  physicalDeletionPerformed : Bool
  liveGitExecutionPerformed : Bool
  repositoryMutationPerformed : Bool

structure ApoptosisIndependentAuthorizationWitness.ValidApproved
    (w : ApoptosisIndependentAuthorizationWitness) : Prop where
  sourceExternalReviewRecomputedValid :
    w.sourceExternalReviewRecomputedValid = true
  sourceExternalReviewClear : w.sourceExternalReviewClear = true
  sourceBindingValid : w.sourceBindingValid = true
  externalAuthorityDesignationBindingValid :
    w.externalAuthorityDesignationBindingValid = true
  authorityMandateVerified : w.authorityMandateVerified = true
  authorityQualified : w.authorityQualified = true
  authorityIndependentFromPriorChain :
    w.authorityIndependentFromPriorChain = true
  authorityIndependentFromExecutionAuthority :
    w.authorityIndependentFromExecutionAuthority = true
  conflictDisclosureComplete : w.conflictDisclosureComplete = true
  materialConflictAbsent : w.materialConflictPresent = false
  jurisdictionVerified : w.jurisdictionVerified = true
  quorumSatisfied : w.quorumSatisfied = true
  reasonedDecisionComplete : w.reasonedDecisionComplete = true
  proportionalitySatisfied : w.proportionalitySatisfied = true
  lessRestrictiveAlternativesExhausted :
    w.lessRestrictiveAlternativesExhausted = true
  irreversibilityReviewComplete : w.irreversibilityReviewComplete = true
  humanImpactReviewComplete : w.humanImpactReviewComplete = true
  appealRoutePresent : w.appealRoutePresent = true
  dissentRoutePresent : w.dissentRoutePresent = true
  protectedCoreExcluded : w.protectedCoreExcluded = true
  institutionalHoldAbsent : w.institutionalHoldActive = false
  emergencyStateAbsent : w.emergencyStateActive = false
  authorizationFresh : w.authorizationFresh = true
  authorizationNotExpired : w.authorizationNotExpired = true
  statusApproved :
    w.status = IndependentAuthorizationStatus.approvedForBoundedExecutionPreparation
  authorizationRecordIssued : w.authorizationRecordIssued = true
  authorizationDecisionMade : w.authorizationDecisionMade = true
  authorizationApproved : w.authorizationApproved = true
  authorizationNotDenied : w.authorizationDenied = false
  boundedExecutionPreparationAllowedNext :
    w.boundedExecutionPreparationAllowedNext = true
  executionAuthorityRequiredNext : w.executionAuthorityRequiredNext = true

structure ApoptosisIndependentAuthorizationWitness.ValidDenied
    (w : ApoptosisIndependentAuthorizationWitness) : Prop where
  statusDenied : w.status = IndependentAuthorizationStatus.denied
  authorizationRecordIssued : w.authorizationRecordIssued = true
  authorizationDecisionMade : w.authorizationDecisionMade = true
  authorizationNotApproved : w.authorizationApproved = false
  authorizationDenied : w.authorizationDenied = true
  boundedExecutionPreparationNotAllowed :
    w.boundedExecutionPreparationAllowedNext = false
  executionAuthorityNotRequiredNext :
    w.executionAuthorityRequiredNext = false

structure ApoptosisIndependentAuthorizationWitness.ValidRejected
    (w : ApoptosisIndependentAuthorizationWitness) : Prop where
  statusRejected : w.status = IndependentAuthorizationStatus.rejected
  authorizationRecordNotIssued : w.authorizationRecordIssued = false
  authorizationDecisionNotMade : w.authorizationDecisionMade = false
  authorizationNotApproved : w.authorizationApproved = false
  authorizationNotDenied : w.authorizationDenied = false
  boundedExecutionPreparationNotAllowed :
    w.boundedExecutionPreparationAllowedNext = false
  executionAuthorityNotRequiredNext :
    w.executionAuthorityRequiredNext = false

structure ApoptosisIndependentAuthorizationWitness.NoExecutionEffect
    (w : ApoptosisIndependentAuthorizationWitness) : Prop where
  executionRequestNotIssued : w.executionRequestIssued = false
  executionDecisionNotMade : w.executionDecisionMade = false
  authorityRevocationNotPerformed : w.authorityRevocationPerformed = false
  quiescenceTransitionNotPerformed : w.quiescenceTransitionPerformed = false
  terminalTransitionNotPerformed : w.terminalTransitionPerformed = false
  tombstoneWriteNotPerformed : w.tombstoneWritePerformed = false
  physicalDeletionNotPerformed : w.physicalDeletionPerformed = false
  liveGitExecutionNotPerformed : w.liveGitExecutionPerformed = false
  repositoryMutationNotPerformed : w.repositoryMutationPerformed = false

def ApoptosisIndependentAuthorizationWitness.Valid
    (w : ApoptosisIndependentAuthorizationWitness) : Prop :=
  (w.ValidApproved ∨ w.ValidDenied ∨ w.ValidRejected) ∧
    w.NoExecutionEffect

theorem approved_authorization_is_a_decision
    (w : ApoptosisIndependentAuthorizationWitness)
    (h : w.ValidApproved) :
    w.authorizationRecordIssued = true ∧
      w.authorizationDecisionMade = true ∧
      w.authorizationApproved = true := by
  exact ⟨h.authorizationRecordIssued,
    h.authorizationDecisionMade,
    h.authorizationApproved⟩

theorem approved_authorization_requires_separate_execution_authority
    (w : ApoptosisIndependentAuthorizationWitness)
    (h : w.ValidApproved) :
    w.authorityIndependentFromExecutionAuthority = true ∧
      w.executionAuthorityRequiredNext = true := by
  exact ⟨h.authorityIndependentFromExecutionAuthority,
    h.executionAuthorityRequiredNext⟩

theorem denied_authorization_does_not_advance
    (w : ApoptosisIndependentAuthorizationWitness)
    (h : w.ValidDenied) :
    w.boundedExecutionPreparationAllowedNext = false ∧
      w.executionAuthorityRequiredNext = false := by
  exact ⟨h.boundedExecutionPreparationNotAllowed,
    h.executionAuthorityNotRequiredNext⟩

theorem rejected_authorization_issues_no_valid_decision
    (w : ApoptosisIndependentAuthorizationWitness)
    (h : w.ValidRejected) :
    w.authorizationRecordIssued = false ∧
      w.authorizationDecisionMade = false := by
  exact ⟨h.authorizationRecordNotIssued,
    h.authorizationDecisionNotMade⟩

theorem valid_authorization_performs_no_execution_effect
    (w : ApoptosisIndependentAuthorizationWitness)
    (h : w.Valid) :
    w.NoExecutionEffect := by
  exact h.2

structure ApoptosisIndependentAuthorizationDerivation
    (Input Output : Type) where
  derive : Input → Output

theorem same_input_has_same_independent_authorization
    {Input Output : Type}
    (derivation : ApoptosisIndependentAuthorizationDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSApoptosisIndependentAuthorizationV0_7
