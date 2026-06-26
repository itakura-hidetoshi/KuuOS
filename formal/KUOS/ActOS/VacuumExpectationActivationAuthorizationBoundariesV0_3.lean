import Mathlib

namespace KUOS
namespace ActOS

structure IndependentActFreshnessRevalidation where
  targetCycle : Nat
  adaptiveEpoch : Nat
  capabilityEpoch : Nat
  handoffFresh : Bool
  approvalFresh : Bool
  licenseFresh : Bool
  capabilityFresh : Bool
  leaseFresh : Bool
  sessionFresh : Bool
  intentFresh : Bool
  adaptiveEpochRequired : adaptiveEpoch = targetCycle
  capabilityEpochRequired : capabilityEpoch = adaptiveEpoch
  handoffRequired : handoffFresh = true
  approvalRequired : approvalFresh = true
  licenseRequired : licenseFresh = true
  capabilityRequired : capabilityFresh = true
  leaseRequired : leaseFresh = true
  sessionRequired : sessionFresh = true
  intentRequired : intentFresh = true

structure CapabilityRegistryConfirmation where
  registryEntryPresent : Bool
  registryEntryRevoked : Bool
  ownerExact : Bool
  lineageExact : Bool
  capabilityIdExact : Bool
  adapterKindExact : Bool
  capabilityEpochExact : Bool
  operationAllowed : Bool
  resourceAllowed : Bool
  effectWithinCeiling : Bool
  entryRequired : registryEntryPresent = true
  revocationForbidden : registryEntryRevoked = false
  ownerRequired : ownerExact = true
  lineageRequired : lineageExact = true
  capabilityIdRequired : capabilityIdExact = true
  adapterKindRequired : adapterKindExact = true
  epochRequired : capabilityEpochExact = true
  operationRequired : operationAllowed = true
  resourceRequired : resourceAllowed = true
  effectRequired : effectWithinCeiling = true

structure LeaseUseReservationBoundary where
  leaseValid : Bool
  leaseExpired : Bool
  holderExact : Bool
  scopeExact : Bool
  sessionExact : Bool
  intentExact : Bool
  remainingUsesBefore : Nat
  remainingUsesAfter : Nat
  reservationCount : Nat
  reservationCommitted : Bool
  duplicateReservation : Bool
  exactReplayIdempotent : Bool
  validityRequired : leaseValid = true
  expiryForbidden : leaseExpired = false
  holderRequired : holderExact = true
  scopeRequired : scopeExact = true
  sessionRequired : sessionExact = true
  intentRequired : intentExact = true
  remainingPositive : 0 < remainingUsesBefore
  decrementExact : remainingUsesAfter + 1 = remainingUsesBefore
  reservationCountExact : reservationCount = 1
  reservationRequired : reservationCommitted = true
  duplicateForbidden : duplicateReservation = false
  replayRequired : exactReplayIdempotent = true

structure SessionIntentReplayBoundary where
  sessionOpen : Bool
  sessionIdExact : Bool
  generationExact : Bool
  actionIntentBound : Bool
  actionIntentDistinctFromDecision : Bool
  intentNonceFresh : Bool
  intentPreviouslyConsumed : Bool
  conflictingReplayDetected : Bool
  exactReceiptReplayIdempotent : Bool
  sessionOpenRequired : sessionOpen = true
  sessionIdRequired : sessionIdExact = true
  generationRequired : generationExact = true
  intentRequired : actionIntentBound = true
  distinctIntentRequired : actionIntentDistinctFromDecision = true
  nonceRequired : intentNonceFresh = true
  previousConsumptionForbidden : intentPreviouslyConsumed = false
  conflictForbidden : conflictingReplayDetected = false
  replayRequired : exactReceiptReplayIdempotent = true

structure StagedEffectAuthorizationBoundary where
  selectedStepBound : Bool
  operationInputBound : Bool
  stopConditionsPreserved : Bool
  observationDigestPreserved : Bool
  verificationCriterionPreserved : Bool
  projectedOnly : Bool
  hostAdapterInvoked : Bool
  externalEffectPerformed : Bool
  effectRecordCount : Nat
  stepRequired : selectedStepBound = true
  inputRequired : operationInputBound = true
  stopRequired : stopConditionsPreserved = true
  observationRequired : observationDigestPreserved = true
  verificationRequired : verificationCriterionPreserved = true
  projectionRequired : projectedOnly = true
  invocationForbidden : hostAdapterInvoked = false
  effectForbidden : externalEffectPerformed = false
  recordCountRequired : effectRecordCount = 0

structure ActivationAuthorizationReceiptBoundary where
  handoffIntakeBound : Bool
  freshnessRevalidated : Bool
  capabilityRegistryConfirmed : Bool
  leaseReservationBound : Bool
  sessionIntentConfirmed : Bool
  stagedEffectConfirmed : Bool
  activationAuthorized : Bool
  authorizationCommitted : Bool
  planActivated : Bool
  adapterInvoked : Bool
  externalEffectPerformed : Bool
  effectRecordCount : Nat
  intakeRequired : handoffIntakeBound = true
  freshnessRequired : freshnessRevalidated = true
  registryRequired : capabilityRegistryConfirmed = true
  leaseRequired : leaseReservationBound = true
  sessionIntentRequired : sessionIntentConfirmed = true
  stagedEffectRequired : stagedEffectConfirmed = true
  authorizationRequired : activationAuthorized = true
  commitRequired : authorizationCommitted = true
  activationForbidden : planActivated = false
  invocationForbidden : adapterInvoked = false
  effectForbidden : externalEffectPerformed = false
  recordCountRequired : effectRecordCount = 0

end ActOS
end KUOS
