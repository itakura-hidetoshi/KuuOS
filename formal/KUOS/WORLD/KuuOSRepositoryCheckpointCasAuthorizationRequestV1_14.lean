import KUOS.WORLD.KuuOSRepositoryCheckpointCasCoherenceV1_13

namespace KUOS.WORLD.KuuOSRepositoryCheckpointCasAuthorizationRequestV1_14

inductive RequestStatus where
  | ready
  | denied
  | rejected
  deriving DecidableEq, Repr

structure CasAuthorizationRequestWitness where
  coherenceReceiptValid : Prop
  policyValid : Prop
  repositoryAllowed : Prop
  checkpointReferenceAllowed : Prop
  lifetimeWithinPolicy : Prop
  noncePresent : Prop
  status : RequestStatus
  singleUseAuthorizationRequired : Bool
  authorizationGranted : Bool
  executionPerformed : Bool
  liveGitCommandInvoked : Bool
  referenceMutated : Bool

structure CasAuthorizationRequestWitness.ValidReady
    (w : CasAuthorizationRequestWitness) : Prop where
  coherenceReceiptValid : w.coherenceReceiptValid
  policyValid : w.policyValid
  repositoryAllowed : w.repositoryAllowed
  checkpointReferenceAllowed : w.checkpointReferenceAllowed
  lifetimeWithinPolicy : w.lifetimeWithinPolicy
  noncePresent : w.noncePresent
  statusReady : w.status = RequestStatus.ready
  singleUseRequired : w.singleUseAuthorizationRequired = true
  noAuthorization : w.authorizationGranted = false
  noExecution : w.executionPerformed = false
  noLiveGit : w.liveGitCommandInvoked = false
  noMutation : w.referenceMutated = false

structure CasAuthorizationRequestWitness.ValidDenied
    (w : CasAuthorizationRequestWitness) : Prop where
  coherenceReceiptValid : w.coherenceReceiptValid
  policyValid : w.policyValid
  repositoryAllowed : w.repositoryAllowed
  checkpointReferenceAllowed : w.checkpointReferenceAllowed
  lifetimeWithinPolicy : w.lifetimeWithinPolicy
  noncePresent : w.noncePresent
  statusDenied : w.status = RequestStatus.denied
  noSingleUseRequest : w.singleUseAuthorizationRequired = false
  noAuthorization : w.authorizationGranted = false
  noExecution : w.executionPerformed = false
  noLiveGit : w.liveGitCommandInvoked = false
  noMutation : w.referenceMutated = false


theorem ready_request_has_complete_input_binding
    (w : CasAuthorizationRequestWitness)
    (h : w.ValidReady) :
    w.coherenceReceiptValid ∧ w.policyValid ∧ w.repositoryAllowed ∧
      w.checkpointReferenceAllowed ∧ w.lifetimeWithinPolicy ∧
      w.noncePresent := by
  exact ⟨h.coherenceReceiptValid, h.policyValid, h.repositoryAllowed,
    h.checkpointReferenceAllowed, h.lifetimeWithinPolicy, h.noncePresent⟩


theorem ready_request_grants_no_authorization
    (w : CasAuthorizationRequestWitness)
    (h : w.ValidReady) :
    w.singleUseAuthorizationRequired = true ∧
      w.authorizationGranted = false ∧
      w.executionPerformed = false ∧
      w.liveGitCommandInvoked = false ∧
      w.referenceMutated = false := by
  exact ⟨h.singleUseRequired, h.noAuthorization, h.noExecution,
    h.noLiveGit, h.noMutation⟩


theorem denied_request_has_no_authorization_candidate
    (w : CasAuthorizationRequestWitness)
    (h : w.ValidDenied) :
    w.singleUseAuthorizationRequired = false ∧
      w.authorizationGranted = false ∧
      w.executionPerformed = false ∧
      w.liveGitCommandInvoked = false ∧
      w.referenceMutated = false := by
  exact ⟨h.noSingleUseRequest, h.noAuthorization, h.noExecution,
    h.noLiveGit, h.noMutation⟩

structure RequestDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_authorization_request
    {Input Output : Type}
    (derivation : RequestDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointCasAuthorizationRequestV1_14
