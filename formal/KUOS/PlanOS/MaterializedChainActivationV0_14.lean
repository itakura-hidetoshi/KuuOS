import Mathlib
import KUOS.PlanOS.RerotationMaterializationV0_13

namespace KUOS.PlanOS

structure MaterializedActivationRoot where
  owner : Nat
  epoch : Nat
  currentCycle : Nat
  materialized : Bool
  capabilityBound : Bool
  allLeasesCurrent : Bool
  renewalGovernanceFresh : Bool

structure NextPlanActivationHandoff where
  owner : Nat
  epoch : Nat
  activeFromCycle : Nat
  planPhase : Bool
  scopeInventoryBound : Bool
  singleUse : Bool
  executionGranted : Bool
  hostAccessGranted : Bool
  memoryOverwrite : Bool


def activationHandoffAdmissible
    (root : MaterializedActivationRoot)
    (handoff : NextPlanActivationHandoff) : Prop :=
  root.materialized = true ∧
  root.capabilityBound = true ∧
  root.allLeasesCurrent = true ∧
  root.renewalGovernanceFresh = true ∧
  handoff.owner = root.owner ∧
  handoff.epoch = root.epoch ∧
  handoff.activeFromCycle = root.currentCycle + 1 ∧
  handoff.planPhase = true ∧
  handoff.scopeInventoryBound = true ∧
  handoff.singleUse = true ∧
  handoff.executionGranted = false ∧
  handoff.hostAccessGranted = false ∧
  handoff.memoryOverwrite = false


theorem admissible_activation_requires_materialized_bound_chain
    (root : MaterializedActivationRoot)
    (handoff : NextPlanActivationHandoff)
    (h : activationHandoffAdmissible root handoff) :
    root.materialized = true ∧
    root.capabilityBound = true ∧
    root.allLeasesCurrent = true ∧
    root.renewalGovernanceFresh = true := by
  exact ⟨h.1, h.2.1, h.2.2.1, h.2.2.2.1⟩


theorem admissible_activation_preserves_owner_epoch
    (root : MaterializedActivationRoot)
    (handoff : NextPlanActivationHandoff)
    (h : activationHandoffAdmissible root handoff) :
    handoff.owner = root.owner ∧ handoff.epoch = root.epoch := by
  exact ⟨h.2.2.2.2.1, h.2.2.2.2.2.1⟩


theorem admissible_activation_targets_next_cycle
    (root : MaterializedActivationRoot)
    (handoff : NextPlanActivationHandoff)
    (h : activationHandoffAdmissible root handoff) :
    handoff.activeFromCycle = root.currentCycle + 1 := by
  exact h.2.2.2.2.2.2.1


theorem admissible_activation_targets_plan_phase
    (root : MaterializedActivationRoot)
    (handoff : NextPlanActivationHandoff)
    (h : activationHandoffAdmissible root handoff) :
    handoff.planPhase = true := by
  exact h.2.2.2.2.2.2.2.1


theorem admissible_activation_binds_scope_inventory
    (root : MaterializedActivationRoot)
    (handoff : NextPlanActivationHandoff)
    (h : activationHandoffAdmissible root handoff) :
    handoff.scopeInventoryBound = true := by
  exact h.2.2.2.2.2.2.2.2.1


theorem admissible_activation_is_single_use
    (root : MaterializedActivationRoot)
    (handoff : NextPlanActivationHandoff)
    (h : activationHandoffAdmissible root handoff) :
    handoff.singleUse = true := by
  exact h.2.2.2.2.2.2.2.2.2.1


theorem activation_handoff_grants_no_authority
    (root : MaterializedActivationRoot)
    (handoff : NextPlanActivationHandoff)
    (h : activationHandoffAdmissible root handoff) :
    handoff.executionGranted = false ∧
    handoff.hostAccessGranted = false ∧
    handoff.memoryOverwrite = false := by
  exact ⟨h.2.2.2.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.2.2.2.1,
    h.2.2.2.2.2.2.2.2.2.2.2.2⟩

end KUOS.PlanOS
