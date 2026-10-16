import Mathlib
import KUOS.PlanOS.ReentryOwnershipContinuityV0_8

namespace KUOS.PlanOS

inductive CapabilityKind where
  | hostAccess
  | humanApproval
  | stepAuthorization
  | operationAuthorization
  deriving DecidableEq

structure CapabilityEpochRoot where
  previousOwner : Nat
  currentOwner : Nat
  previousEpoch : Nat
  currentEpoch : Nat
  handover : Bool
  allPreviousRevoked : Bool
  epochMonotone : currentEpoch = previousEpoch + 1
  revocationComplete : allPreviousRevoked = true

structure CapabilityReissueBinding where
  kind : CapabilityKind
  owner : Nat
  epoch : Nat
  lowerReceiptDigest : Nat
  issuedCapabilityDigest : Nat
  lowerLayerValidated : Bool
  authorityGrantedByBinding : Bool


def capabilityOwnerAdmissible
    (root : CapabilityEpochRoot)
    (owner : Nat) : Prop :=
  owner = root.currentOwner ∧
    (root.handover = true → owner ≠ root.previousOwner)


def capabilityBindingAdmissible
    (root : CapabilityEpochRoot)
    (binding : CapabilityReissueBinding) : Prop :=
  capabilityOwnerAdmissible root binding.owner ∧
  binding.epoch = root.currentEpoch ∧
  binding.lowerLayerValidated = true ∧
  binding.authorityGrantedByBinding = false


theorem capability_epoch_strictly_rotates
    (root : CapabilityEpochRoot) :
    root.currentEpoch = root.previousEpoch + 1 := by
  exact root.epochMonotone


theorem all_previous_capabilities_are_revoked
    (root : CapabilityEpochRoot) :
    root.allPreviousRevoked = true := by
  exact root.revocationComplete


theorem admissible_binding_uses_current_owner
    (root : CapabilityEpochRoot)
    (binding : CapabilityReissueBinding)
    (h : capabilityBindingAdmissible root binding) :
    binding.owner = root.currentOwner := by
  exact h.1.1


theorem handover_previous_owner_cannot_reissue
    (root : CapabilityEpochRoot)
    (handover : root.handover = true) :
    ¬ capabilityOwnerAdmissible root root.previousOwner := by
  intro h
  exact (h.2 handover) rfl


theorem admissible_binding_uses_current_epoch
    (root : CapabilityEpochRoot)
    (binding : CapabilityReissueBinding)
    (h : capabilityBindingAdmissible root binding) :
    binding.epoch = root.currentEpoch := by
  exact h.2.1


theorem admissible_binding_requires_lower_validation
    (root : CapabilityEpochRoot)
    (binding : CapabilityReissueBinding)
    (h : capabilityBindingAdmissible root binding) :
    binding.lowerLayerValidated = true := by
  exact h.2.2.1


theorem admissible_binding_grants_no_authority
    (root : CapabilityEpochRoot)
    (binding : CapabilityReissueBinding)
    (h : capabilityBindingAdmissible root binding) :
    binding.authorityGrantedByBinding = false := by
  exact h.2.2.2

structure CapabilityAuthorityBoundary where
  executionGranted : Bool
  hostAccessGranted : Bool
  approvalGranted : Bool
  memoryOverwrite : Bool
  noExecution : executionGranted = false
  noHostAccess : hostAccessGranted = false
  noApproval : approvalGranted = false
  noOverwrite : memoryOverwrite = false


theorem rotation_wrapper_grants_no_authority
    (boundary : CapabilityAuthorityBoundary) :
    boundary.executionGranted = false ∧
    boundary.hostAccessGranted = false ∧
    boundary.approvalGranted = false ∧
    boundary.memoryOverwrite = false := by
  exact ⟨boundary.noExecution, boundary.noHostAccess,
    boundary.noApproval, boundary.noOverwrite⟩

end KUOS.PlanOS
