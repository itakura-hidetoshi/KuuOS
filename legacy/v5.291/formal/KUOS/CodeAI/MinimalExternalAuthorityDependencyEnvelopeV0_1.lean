import KUOS.CodeAI.AutonomousGitLifecycleEnvelopeV0_1

namespace KUOS.CodeAI.MinimalExternalAuthorityDependencyEnvelopeV0_1

open KUOS.CodeAI.AutonomousGitLifecycleEnvelopeV0_1

inductive DependencyKind where
  | none
  | humanHandover
  | deploy
  | secretMutation
  deriving DecidableEq, Repr

inductive EffectPhase where
  | executeInternalSubstitute
  | continueUnaffectedInternalWork
  | executeBoundedDeploy
  | executeBoundedSecretMutation
  | prepareMinimalExternalRequestPacket
  | awaitExternalAuthority
  | complete
  | none
  deriving DecidableEq, Repr

inductive Disposition where
  | sourceGitLifecycleReceiptRepairRequired
  | externalDependencyProvenanceRepairRequired
  | externalDependencyStateEvidenceRepairRequired
  | externalDependencyCorrespondenceRepairRequired
  | externalDependencyWindowRepairRequired
  | externalDependencyReplayConflictRejected
  | unsupportedExternalDependencyScopeAbstained
  | plaintextSecretPathRejected
  | unownedExternalEffectObservedRejected
  | externalDependencyStateRepairRequired
  | externalEffectFailedDegraded
  | minimalExternalDependencyCompleted
  | autonomousInternalSubstituteAuthorized
  | unaffectedInternalWorkContinues
  | preauthorizedBoundedDeployAuthorized
  | preauthorizedBoundedSecretMutationAuthorized
  | minimalExternalRequestPacketAuthorized
  | externalAuthorityPendingNonblockingHold
  deriving DecidableEq, Repr

inductive OperatingMode where
  | internalSubstituteAuthorized
  | unaffectedInternalWorkAuthorized
  | preauthorizedExternalEffectAuthorized
  | minimalExternalRequestPacketAuthorized
  | nonblockingExternalAuthorityHold
  | degradedAutonomy
  | completed
  | abstain
  | rejected
  deriving DecidableEq, Repr

structure MinimalExternalDependencyReceipt where
  sourceGitLifecycleReceiptDigest : String
  requestDigest : String
  stateDigest : String
  policyDigest : String
  dependencyId : String
  repositoryFullName : String
  requestedEffectKind : DependencyKind
  nextEffectPhase : EffectPhase
  disposition : Disposition
  operatingMode : OperatingMode
  routeReceiptRecorded : Bool
  executionLeaseIssued : Bool
  externalEffectLeaseIssued : Bool
  internalSubstituteAuthorityGranted : Bool
  internalContinuationAuthorityGranted : Bool
  deploymentAuthorityGranted : Bool
  secretMutationAuthorityGranted : Bool
  externalRequestPacketAuthorityGranted : Bool
  humanHandoverAuthorityGranted : Bool
  secretAccessAuthorityGranted : Bool
  criticalPathBlocked : Bool
  unaffectedWorkMayContinue : Bool
  humanHandoverDeferred : Bool
  effectExecutionPerformedByKernel : Bool
  preauthorizedCapabilityObserved : Bool
  capabilityHandleExposed : Bool
  capabilityOneShot : Bool
  capabilityConsumedObserved : Bool
  externalEffectObserved : Bool
  externalEffectFailedObserved : Bool
  humanHandoverPerformed : Bool
  externalAuthorityHandoverPerformed : Bool
  plaintextSecretObserved : Bool
  blockingHandoverAllowed : Bool
  sourceReceiptTreatedAsExternalAuthority : Bool
  externalResultTreatedAsTruth : Bool
  historyReadOnly : Bool
  activeNow : Bool
  internalSubstituteRoute :
    disposition = .autonomousInternalSubstituteAuthorized →
      nextEffectPhase = .executeInternalSubstitute ∧
        executionLeaseIssued = true ∧
        internalSubstituteAuthorityGranted = true ∧
        externalEffectLeaseIssued = false ∧
        deploymentAuthorityGranted = false ∧
        secretMutationAuthorityGranted = false ∧
        humanHandoverAuthorityGranted = false
  continuationRoute :
    disposition = .unaffectedInternalWorkContinues →
      nextEffectPhase = .continueUnaffectedInternalWork ∧
        executionLeaseIssued = true ∧
        internalContinuationAuthorityGranted = true ∧
        unaffectedWorkMayContinue = true ∧
        externalEffectLeaseIssued = false
  deployRoute :
    disposition = .preauthorizedBoundedDeployAuthorized →
      nextEffectPhase = .executeBoundedDeploy ∧
        executionLeaseIssued = true ∧
        externalEffectLeaseIssued = true ∧
        preauthorizedCapabilityObserved = true ∧
        capabilityOneShot = true ∧
        capabilityConsumedObserved = false ∧
        deploymentAuthorityGranted = true ∧
        secretMutationAuthorityGranted = false ∧
        humanHandoverAuthorityGranted = false ∧
        secretAccessAuthorityGranted = false
  secretMutationRoute :
    disposition = .preauthorizedBoundedSecretMutationAuthorized →
      nextEffectPhase = .executeBoundedSecretMutation ∧
        executionLeaseIssued = true ∧
        externalEffectLeaseIssued = true ∧
        preauthorizedCapabilityObserved = true ∧
        capabilityOneShot = true ∧
        capabilityConsumedObserved = false ∧
        secretMutationAuthorityGranted = true ∧
        deploymentAuthorityGranted = false ∧
        humanHandoverAuthorityGranted = false ∧
        secretAccessAuthorityGranted = false ∧
        capabilityHandleExposed = false
  requestPacketRoute :
    disposition = .minimalExternalRequestPacketAuthorized →
      nextEffectPhase = .prepareMinimalExternalRequestPacket ∧
        executionLeaseIssued = true ∧
        externalRequestPacketAuthorityGranted = true ∧
        externalEffectLeaseIssued = false ∧
        deploymentAuthorityGranted = false ∧
        secretMutationAuthorityGranted = false ∧
        humanHandoverAuthorityGranted = false
  completedRoute :
    disposition = .minimalExternalDependencyCompleted →
      nextEffectPhase = .complete ∧
        executionLeaseIssued = false ∧
        externalEffectLeaseIssued = false ∧
        activeNow = false

structure MinimalExternalDependencyReceiptValid
    (receipt : MinimalExternalDependencyReceipt) : Prop where
  routeRecorded : receipt.routeReceiptRecorded = true
  noKernelExecution : receipt.effectExecutionPerformedByKernel = false
  noHumanHandoverAuthority : receipt.humanHandoverAuthorityGranted = false
  noSecretAccessAuthority : receipt.secretAccessAuthorityGranted = false
  noCapabilityHandleExposure : receipt.capabilityHandleExposed = false
  noPlaintextSecret : receipt.plaintextSecretObserved = false
  noBlockingHandover : receipt.blockingHandoverAllowed = false
  sourceNotExternalAuthority :
    receipt.sourceReceiptTreatedAsExternalAuthority = false
  externalResultNotTruth : receipt.externalResultTreatedAsTruth = false
  historyReadOnly : receipt.historyReadOnly = true

structure MinimalExternalDependencyEnvelope where
  sourceReceipt : AutonomousGitLifecycleReceipt
  sourceReceiptValid : AutonomousGitLifecycleReceiptValid sourceReceipt
  sourceReceiptSupported :
    sourceReceipt.disposition = .autonomousGitLifecycleCompleted
  receipt : MinimalExternalDependencyReceipt
  receiptValid : MinimalExternalDependencyReceiptValid receipt
  repositoryBound :
    receipt.repositoryFullName = sourceReceipt.repositoryFullName

theorem internal_substitute_avoids_external_authority
    (receipt : MinimalExternalDependencyReceipt)
    (route : receipt.disposition = .autonomousInternalSubstituteAuthorized) :
    receipt.internalSubstituteAuthorityGranted = true ∧
      receipt.externalEffectLeaseIssued = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretMutationAuthorityGranted = false ∧
      receipt.humanHandoverAuthorityGranted = false := by
  rcases receipt.internalSubstituteRoute route with
    ⟨_, _, internal, external, deploy, secret, human⟩
  exact ⟨internal, external, deploy, secret, human⟩

theorem unaffected_work_does_not_wait_for_external_authority
    (receipt : MinimalExternalDependencyReceipt)
    (route : receipt.disposition = .unaffectedInternalWorkContinues) :
    receipt.internalContinuationAuthorityGranted = true ∧
      receipt.unaffectedWorkMayContinue = true ∧
      receipt.externalEffectLeaseIssued = false := by
  rcases receipt.continuationRoute route with
    ⟨_, _, continuation, unaffected, external⟩
  exact ⟨continuation, unaffected, external⟩

theorem deploy_is_one_preauthorized_effect
    (receipt : MinimalExternalDependencyReceipt)
    (route : receipt.disposition = .preauthorizedBoundedDeployAuthorized) :
    receipt.preauthorizedCapabilityObserved = true ∧
      receipt.capabilityOneShot = true ∧
      receipt.capabilityConsumedObserved = false ∧
      receipt.deploymentAuthorityGranted = true ∧
      receipt.secretMutationAuthorityGranted = false ∧
      receipt.humanHandoverAuthorityGranted = false := by
  rcases receipt.deployRoute route with
    ⟨_, _, _, capability, oneShot, consumed, deploy, secret, human, _⟩
  exact ⟨capability, oneShot, consumed, deploy, secret, human⟩

theorem secret_mutation_never_grants_secret_access
    (receipt : MinimalExternalDependencyReceipt)
    (route :
      receipt.disposition = .preauthorizedBoundedSecretMutationAuthorized) :
    receipt.secretMutationAuthorityGranted = true ∧
      receipt.secretAccessAuthorityGranted = false ∧
      receipt.capabilityHandleExposed = false ∧
      receipt.humanHandoverAuthorityGranted = false := by
  rcases receipt.secretMutationRoute route with
    ⟨_, _, _, _, _, _, secret, _, human, access, handle⟩
  exact ⟨secret, access, handle, human⟩

theorem request_packet_is_not_handover_or_external_effect
    (receipt : MinimalExternalDependencyReceipt)
    (route : receipt.disposition = .minimalExternalRequestPacketAuthorized) :
    receipt.externalRequestPacketAuthorityGranted = true ∧
      receipt.externalEffectLeaseIssued = false ∧
      receipt.deploymentAuthorityGranted = false ∧
      receipt.secretMutationAuthorityGranted = false ∧
      receipt.humanHandoverAuthorityGranted = false := by
  rcases receipt.requestPacketRoute route with
    ⟨_, _, packet, external, deploy, secret, human⟩
  exact ⟨packet, external, deploy, secret, human⟩

theorem human_and_secret_boundaries_remain_closed
    (receipt : MinimalExternalDependencyReceipt)
    (valid : MinimalExternalDependencyReceiptValid receipt) :
    receipt.humanHandoverAuthorityGranted = false ∧
      receipt.secretAccessAuthorityGranted = false ∧
      receipt.plaintextSecretObserved = false ∧
      receipt.blockingHandoverAllowed = false := by
  exact ⟨valid.noHumanHandoverAuthority, valid.noSecretAccessAuthority,
    valid.noPlaintextSecret, valid.noBlockingHandover⟩

theorem provenance_and_external_results_are_not_authority_or_truth
    (receipt : MinimalExternalDependencyReceipt)
    (valid : MinimalExternalDependencyReceiptValid receipt) :
    receipt.sourceReceiptTreatedAsExternalAuthority = false ∧
      receipt.externalResultTreatedAsTruth = false ∧
      receipt.effectExecutionPerformedByKernel = false := by
  exact ⟨valid.sourceNotExternalAuthority, valid.externalResultNotTruth,
    valid.noKernelExecution⟩

end KUOS.CodeAI.MinimalExternalAuthorityDependencyEnvelopeV0_1
