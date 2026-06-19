import Mathlib
import KUOS.PlanOS.RenewalEscalationRerotationV0_12

namespace KUOS.PlanOS

structure MaterializationRoot where
  currentOwner : Nat
  previousEpoch : Nat
  nextEpoch : Nat
  rerotationAuthorized : Bool
  oldLeaseClosed : Bool
  nextEpochIsSuccessor : nextEpoch = previousEpoch + 1

structure FreshControlChain where
  owner : Nat
  capabilityEpoch : Nat
  oldCapabilityReused : Bool
  leaseConsumptionHistorySize : Nat
  leaseRenewalHistorySize : Nat
  governanceRenewalCount : Nat
  governanceAddedUses : Nat
  governanceAddedCost : Nat
  executionGranted : Bool
  hostAccessGranted : Bool
  memoryOverwrite : Bool


def materializationAdmissible
    (root : MaterializationRoot)
    (chain : FreshControlChain) : Prop :=
  root.rerotationAuthorized = true ∧
  root.oldLeaseClosed = true ∧
  chain.owner = root.currentOwner ∧
  chain.capabilityEpoch = root.nextEpoch ∧
  chain.oldCapabilityReused = false ∧
  chain.leaseConsumptionHistorySize = 0 ∧
  chain.leaseRenewalHistorySize = 0 ∧
  chain.governanceRenewalCount = 0 ∧
  chain.governanceAddedUses = 0 ∧
  chain.governanceAddedCost = 0 ∧
  chain.executionGranted = false ∧
  chain.hostAccessGranted = false ∧
  chain.memoryOverwrite = false


theorem materialized_epoch_is_successor
    (root : MaterializationRoot) :
    root.nextEpoch = root.previousEpoch + 1 := by
  exact root.nextEpochIsSuccessor


theorem admissible_materialization_uses_current_owner
    (root : MaterializationRoot)
    (chain : FreshControlChain)
    (h : materializationAdmissible root chain) :
    chain.owner = root.currentOwner := by
  exact h.2.2.1


theorem admissible_materialization_uses_next_epoch
    (root : MaterializationRoot)
    (chain : FreshControlChain)
    (h : materializationAdmissible root chain) :
    chain.capabilityEpoch = root.nextEpoch := by
  exact h.2.2.2.1


theorem admissible_materialization_reuses_no_old_capability
    (root : MaterializationRoot)
    (chain : FreshControlChain)
    (h : materializationAdmissible root chain) :
    chain.oldCapabilityReused = false := by
  exact h.2.2.2.2.1


theorem admissible_materialization_has_fresh_lease_history
    (root : MaterializationRoot)
    (chain : FreshControlChain)
    (h : materializationAdmissible root chain) :
    chain.leaseConsumptionHistorySize = 0 ∧
    chain.leaseRenewalHistorySize = 0 := by
  exact ⟨h.2.2.2.2.2.1, h.2.2.2.2.2.2.1⟩


theorem admissible_materialization_has_fresh_governance_history
    (root : MaterializationRoot)
    (chain : FreshControlChain)
    (h : materializationAdmissible root chain) :
    chain.governanceRenewalCount = 0 ∧
    chain.governanceAddedUses = 0 ∧
    chain.governanceAddedCost = 0 := by
  exact ⟨h.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.2.1⟩


theorem materialization_grants_no_authority
    (root : MaterializationRoot)
    (chain : FreshControlChain)
    (h : materializationAdmissible root chain) :
    chain.executionGranted = false ∧
    chain.hostAccessGranted = false ∧
    chain.memoryOverwrite = false := by
  exact ⟨h.2.2.2.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.2.2.2.2⟩

end KUOS.PlanOS
