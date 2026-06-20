import Mathlib
import KUOS.Architecture.QiWorldLicensedMultiCycleChainInductionV2_1

namespace KUOS.Architecture

open InductiveLicensedCycleChain

structure ConcreteThirdCycle
    (c : InductiveLicensedCycleChain) where
  predecessorReceipt : Nat
  closedReceipt : Nat
  authorityDigest : Nat
  approvalDigest : Nat
  hostLicenseDigest : Nat
  source_count_two : c.cycleCount = 2
  predecessor_exact : predecessorReceipt = c.lastReceiptDigest
  authority_fresh : authorityDigest ∉ c.authorityInventory
  approval_fresh : approvalDigest ∉ c.humanApprovalInventory
  host_license_fresh : hostLicenseDigest ∉ c.hostLicenseInventory
  actEffectRecorded : Bool
  observationClosed : Bool
  verificationClosed : Bool
  learningClosed : Bool
  replanClosed : Bool
  explicitDischargeCompleted : Bool
  receiptConsumptionCount : Nat
  authorityConsumptionCount : Nat
  authorityRenewable : Bool
  authorityInheritable : Bool
  nextActStarted : Bool
  allBlockersActive : Bool
  exactWorldUpdated : Bool
  historyOverwritten : Bool
  truthPromoted : Bool
  grantsExecution : Bool
  act_effect_recorded : actEffectRecorded = true
  observation_closed : observationClosed = true
  verification_closed : verificationClosed = true
  learning_closed : learningClosed = true
  replan_closed : replanClosed = true
  discharge_completed : explicitDischargeCompleted = true
  receipt_not_consumed : receiptConsumptionCount = 0
  authority_consumed_once : authorityConsumptionCount = 1
  authority_not_renewable : authorityRenewable = false
  authority_not_inheritable : authorityInheritable = false
  next_act_not_started : nextActStarted = false
  blockers_active : allBlockersActive = true
  exact_world_not_updated : exactWorldUpdated = false
  history_not_overwritten : historyOverwritten = false
  truth_not_promoted : truthPromoted = false
  non_authoritative : grantsExecution = false

namespace ConcreteThirdCycle


def toExtensionWitness
    {c : InductiveLicensedCycleChain}
    (m : ConcreteThirdCycle c) :
    LicensedCycleExtensionWitness c where
  targetCycleOrdinal := 3
  predecessorReceiptDigest := m.predecessorReceipt
  closedCycleReceiptDigest := m.closedReceipt
  freshAuthorityDigest := m.authorityDigest
  newHumanApprovalDigest := m.approvalDigest
  newHostLicenseDigest := m.hostLicenseDigest
  cycleMaterialized := true
  nativeClosureCompleted := true
  cycleClosed := true
  receiptImmutable := true
  receiptAppendOnly := true
  receiptConsumptionCount := 0
  authorityConsumptionCount := 1
  authorityRenewable := false
  authorityInheritable := false
  nextActStarted := false
  allBlockersActive := true
  witnessGrantsExecution := false
  target_is_immediate_successor := by
    simp [m.source_count_two]
  predecessor_link_exact := m.predecessor_exact
  authority_fresh := m.authority_fresh
  approval_fresh := m.approval_fresh
  host_license_fresh := m.host_license_fresh
  cycle_materialized := rfl
  native_closure_completed := rfl
  cycle_closed := rfl
  receipt_immutable := rfl
  receipt_append_only := rfl
  receipt_not_consumed := rfl
  authority_consumed_once := rfl
  authority_not_renewable := rfl
  authority_not_inheritable := rfl
  next_act_not_started := rfl
  blockers_active := rfl
  witness_non_authoritative := rfl


theorem concrete_third_cycle_boundary
    {c : InductiveLicensedCycleChain}
    (m : ConcreteThirdCycle c) :
    let next := appendClosedCycle c m.toExtensionWitness
    next.cycleCount = 3 ∧
      next.lastCycleOrdinal = 3 ∧
      next.lastReceiptDigest = m.closedReceipt ∧
      next.receiptDigests = c.receiptDigests ++ [m.closedReceipt] ∧
      next.authorityInventory = c.authorityInventory ++ [m.authorityDigest] ∧
      m.actEffectRecorded = true ∧
      m.observationClosed = true ∧
      m.verificationClosed = true ∧
      m.learningClosed = true ∧
      m.replanClosed = true ∧
      next.allCyclesClosed = true ∧
      next.allReceiptsNonConsumable = true ∧
      next.nextActStarted = false ∧
      next.allBlockersActive = true ∧
      next.chainGrantsExecution = false := by
  simp [toExtensionWitness, appendClosedCycle, m.source_count_two,
    m.act_effect_recorded, m.observation_closed, m.verification_closed,
    m.learning_closed, m.replan_closed]

end ConcreteThirdCycle

end KUOS.Architecture
