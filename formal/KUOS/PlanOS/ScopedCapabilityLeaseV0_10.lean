import Mathlib
import KUOS.PlanOS.CapabilityRotationRevocationV0_9

namespace KUOS.PlanOS

structure CapabilityLease where
  currentOwner : Nat
  currentEpoch : Nat
  scopeDigest : Nat
  maxUses : Nat
  remainingUses : Nat
  maxCost : Nat
  remainingCost : Nat
  notBefore : Nat
  expiresAt : Nat
  useBound : remainingUses ≤ maxUses
  costBound : remainingCost ≤ maxCost

structure LeaseConsumption where
  owner : Nat
  epoch : Nat
  scopeDigest : Nat
  stageAllowed : Bool
  operationAllowed : Bool
  cost : Nat
  consumedAt : Nat


def leaseConsumptionAdmissible
    (lease : CapabilityLease)
    (request : LeaseConsumption) : Prop :=
  request.owner = lease.currentOwner ∧
  request.epoch = lease.currentEpoch ∧
  request.scopeDigest = lease.scopeDigest ∧
  request.stageAllowed = true ∧
  request.operationAllowed = true ∧
  0 < lease.remainingUses ∧
  request.cost ≤ lease.remainingCost ∧
  lease.notBefore ≤ request.consumedAt ∧
  request.consumedAt < lease.expiresAt


theorem admissible_consumption_uses_current_owner
    (lease : CapabilityLease)
    (request : LeaseConsumption)
    (h : leaseConsumptionAdmissible lease request) :
    request.owner = lease.currentOwner := by
  exact h.1


theorem admissible_consumption_uses_current_epoch
    (lease : CapabilityLease)
    (request : LeaseConsumption)
    (h : leaseConsumptionAdmissible lease request) :
    request.epoch = lease.currentEpoch := by
  exact h.2.1


theorem admissible_consumption_preserves_scope
    (lease : CapabilityLease)
    (request : LeaseConsumption)
    (h : leaseConsumptionAdmissible lease request) :
    request.scopeDigest = lease.scopeDigest := by
  exact h.2.2.1


theorem admissible_consumption_is_current
    (lease : CapabilityLease)
    (request : LeaseConsumption)
    (h : leaseConsumptionAdmissible lease request) :
    lease.notBefore ≤ request.consumedAt ∧
      request.consumedAt < lease.expiresAt := by
  exact ⟨h.2.2.2.2.2.2.2.1, h.2.2.2.2.2.2.2.2⟩


theorem admissible_consumption_fits_budgets
    (lease : CapabilityLease)
    (request : LeaseConsumption)
    (h : leaseConsumptionAdmissible lease request) :
    0 < lease.remainingUses ∧ request.cost ≤ lease.remainingCost := by
  exact ⟨h.2.2.2.2.2.1, h.2.2.2.2.2.2.1⟩


theorem use_budget_decreases
    (remainingUses : Nat)
    (positive : 0 < remainingUses) :
    remainingUses - 1 < remainingUses := by
  omega


theorem cost_budget_does_not_increase
    (remainingCost cost : Nat) :
    remainingCost - cost ≤ remainingCost := by
  omega

structure LeaseRenewal where
  owner : Nat
  epoch : Nat
  scopeDigest : Nat
  externalReceiptPresent : Bool
  automaticRenewal : Bool
  additionalUses : Nat
  additionalCost : Nat
  newExpiresAt : Nat


def leaseRenewalAdmissible
    (lease : CapabilityLease)
    (renewal : LeaseRenewal) : Prop :=
  renewal.owner = lease.currentOwner ∧
  renewal.epoch = lease.currentEpoch ∧
  renewal.scopeDigest = lease.scopeDigest ∧
  renewal.externalReceiptPresent = true ∧
  renewal.automaticRenewal = false ∧
  0 < renewal.additionalUses ∧
  0 < renewal.additionalCost ∧
  lease.expiresAt < renewal.newExpiresAt


theorem renewal_requires_external_receipt
    (lease : CapabilityLease)
    (renewal : LeaseRenewal)
    (h : leaseRenewalAdmissible lease renewal) :
    renewal.externalReceiptPresent = true := by
  exact h.2.2.2.1


theorem automatic_renewal_is_forbidden
    (lease : CapabilityLease)
    (renewal : LeaseRenewal)
    (h : leaseRenewalAdmissible lease renewal) :
    renewal.automaticRenewal = false := by
  exact h.2.2.2.2.1


theorem renewal_revalidates_owner_epoch_scope
    (lease : CapabilityLease)
    (renewal : LeaseRenewal)
    (h : leaseRenewalAdmissible lease renewal) :
    renewal.owner = lease.currentOwner ∧
      renewal.epoch = lease.currentEpoch ∧
      renewal.scopeDigest = lease.scopeDigest := by
  exact ⟨h.1, h.2.1, h.2.2.1⟩

structure LeaseAuthorityBoundary where
  executionGranted : Bool
  hostAccessGranted : Bool
  approvalGranted : Bool
  memoryOverwrite : Bool
  noExecution : executionGranted = false
  noHostAccess : hostAccessGranted = false
  noApproval : approvalGranted = false
  noOverwrite : memoryOverwrite = false


theorem lease_wrapper_grants_no_authority
    (boundary : LeaseAuthorityBoundary) :
    boundary.executionGranted = false ∧
    boundary.hostAccessGranted = false ∧
    boundary.approvalGranted = false ∧
    boundary.memoryOverwrite = false := by
  exact ⟨boundary.noExecution, boundary.noHostAccess,
    boundary.noApproval, boundary.noOverwrite⟩

end KUOS.PlanOS
