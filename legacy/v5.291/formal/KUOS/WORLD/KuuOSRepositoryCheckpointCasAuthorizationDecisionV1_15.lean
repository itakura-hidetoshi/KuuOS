import KUOS.WORLD.KuuOSRepositoryCheckpointCasAuthorizationRequestV1_14

namespace KUOS.WORLD.KuuOSRepositoryCheckpointCasAuthorizationDecisionV1_15

inductive DecisionStatus where
  | granted
  | denied
  | rejected
  deriving DecidableEq, Repr

structure CasAuthorizationDecisionWitness where
  requestValid : Prop
  requestReady : Prop
  requestBindingExact : Prop
  decisionPolicyValid : Prop
  externalDecisionReceiptValid : Prop
  decisionBindingExact : Prop
  decisionAuthorityAuthorized : Prop
  signatureVerificationValid : Prop
  authorityIdentityVerified : Prop
  decisionNotRevoked : Prop
  decisionWithinRequestLifetime : Prop
  nonceStatusValid : Prop
  nonceScopeBound : Prop
  nonceAuthorityAuthorized : Prop
  nonceStatusFresh : Prop
  nonceUnused : Prop
  nonceNotRevoked : Prop
  status : DecisionStatus
  authorizationGranted : Bool
  singleUseCasEligible : Bool
  nonceConsumed : Bool
  executionPerformed : Bool
  liveGitCommandInvoked : Bool
  referenceMutated : Bool

structure CasAuthorizationDecisionWitness.ValidGranted
    (w : CasAuthorizationDecisionWitness) : Prop where
  requestValid : w.requestValid
  requestReady : w.requestReady
  requestBindingExact : w.requestBindingExact
  decisionPolicyValid : w.decisionPolicyValid
  externalDecisionReceiptValid : w.externalDecisionReceiptValid
  decisionBindingExact : w.decisionBindingExact
  decisionAuthorityAuthorized : w.decisionAuthorityAuthorized
  signatureVerificationValid : w.signatureVerificationValid
  authorityIdentityVerified : w.authorityIdentityVerified
  decisionNotRevoked : w.decisionNotRevoked
  decisionWithinRequestLifetime : w.decisionWithinRequestLifetime
  nonceStatusValid : w.nonceStatusValid
  nonceScopeBound : w.nonceScopeBound
  nonceAuthorityAuthorized : w.nonceAuthorityAuthorized
  nonceStatusFresh : w.nonceStatusFresh
  nonceUnused : w.nonceUnused
  nonceNotRevoked : w.nonceNotRevoked
  statusGranted : w.status = DecisionStatus.granted
  granted : w.authorizationGranted = true
  eligible : w.singleUseCasEligible = true
  noncePreserved : w.nonceConsumed = false
  noExecution : w.executionPerformed = false
  noLiveGit : w.liveGitCommandInvoked = false
  noMutation : w.referenceMutated = false

structure CasAuthorizationDecisionWitness.ValidDenied
    (w : CasAuthorizationDecisionWitness) : Prop where
  requestValid : w.requestValid
  requestBindingExact : w.requestBindingExact
  decisionPolicyValid : w.decisionPolicyValid
  externalDecisionReceiptValid : w.externalDecisionReceiptValid
  decisionBindingExact : w.decisionBindingExact
  statusDenied : w.status = DecisionStatus.denied
  notGranted : w.authorizationGranted = false
  notEligible : w.singleUseCasEligible = false
  noncePreserved : w.nonceConsumed = false
  noExecution : w.executionPerformed = false
  noLiveGit : w.liveGitCommandInvoked = false
  noMutation : w.referenceMutated = false


theorem granted_decision_has_complete_evidence
    (w : CasAuthorizationDecisionWitness)
    (h : w.ValidGranted) :
    w.requestValid ∧ w.requestReady ∧ w.requestBindingExact ∧
      w.decisionPolicyValid ∧ w.externalDecisionReceiptValid ∧
      w.decisionBindingExact ∧ w.decisionAuthorityAuthorized ∧
      w.signatureVerificationValid ∧ w.authorityIdentityVerified ∧
      w.decisionNotRevoked ∧ w.decisionWithinRequestLifetime ∧
      w.nonceStatusValid ∧ w.nonceScopeBound ∧
      w.nonceAuthorityAuthorized ∧ w.nonceStatusFresh ∧
      w.nonceUnused ∧ w.nonceNotRevoked := by
  exact ⟨h.requestValid, h.requestReady, h.requestBindingExact,
    h.decisionPolicyValid, h.externalDecisionReceiptValid,
    h.decisionBindingExact, h.decisionAuthorityAuthorized,
    h.signatureVerificationValid, h.authorityIdentityVerified,
    h.decisionNotRevoked, h.decisionWithinRequestLifetime,
    h.nonceStatusValid, h.nonceScopeBound, h.nonceAuthorityAuthorized,
    h.nonceStatusFresh, h.nonceUnused, h.nonceNotRevoked⟩


theorem granted_decision_is_eligibility_only
    (w : CasAuthorizationDecisionWitness)
    (h : w.ValidGranted) :
    w.authorizationGranted = true ∧
      w.singleUseCasEligible = true ∧
      w.nonceConsumed = false ∧
      w.executionPerformed = false ∧
      w.liveGitCommandInvoked = false ∧
      w.referenceMutated = false := by
  exact ⟨h.granted, h.eligible, h.noncePreserved, h.noExecution,
    h.noLiveGit, h.noMutation⟩


theorem denied_decision_grants_no_eligibility
    (w : CasAuthorizationDecisionWitness)
    (h : w.ValidDenied) :
    w.authorizationGranted = false ∧
      w.singleUseCasEligible = false ∧
      w.nonceConsumed = false ∧
      w.executionPerformed = false ∧
      w.liveGitCommandInvoked = false ∧
      w.referenceMutated = false := by
  exact ⟨h.notGranted, h.notEligible, h.noncePreserved, h.noExecution,
    h.noLiveGit, h.noMutation⟩

structure DecisionDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_authorization_decision
    {Input Output : Type}
    (derivation : DecisionDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointCasAuthorizationDecisionV1_15
