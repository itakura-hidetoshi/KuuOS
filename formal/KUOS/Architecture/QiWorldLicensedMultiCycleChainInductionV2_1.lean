import Mathlib
import KUOS.Architecture.QiWorldSuccessorLicensedCycleMaterializationV2_0

/-!
Qi–WORLD licensed multi-cycle chain induction v2.1.

v2.1 generalizes the concrete two-cycle v2.0 chain into an append-only finite
induction principle.  The append witness must bind the immediate successor
ordinal and exact predecessor receipt digest, and must provide fresh authority,
human-approval, and host-license digests.  The chain remains evidence only.
-/

namespace KUOS.Architecture

structure TwoCycleLicensedChainSeed where
  firstReceiptDigest : Nat
  secondReceiptDigest : Nat
  firstAuthorityDigest : Nat
  secondAuthorityDigest : Nat
  firstHumanApprovalDigest : Nat
  secondHumanApprovalDigest : Nat
  firstHostLicenseDigest : Nat
  secondHostLicenseDigest : Nat
  secondPredecessorDigest : Nat
  predecessor_link_exact : secondPredecessorDigest = firstReceiptDigest
  authority_distinct : firstAuthorityDigest ≠ secondAuthorityDigest
  approval_distinct : firstHumanApprovalDigest ≠ secondHumanApprovalDigest
  host_license_distinct : firstHostLicenseDigest ≠ secondHostLicenseDigest

structure InductiveLicensedCycleChain where
  cycleCount : Nat
  lastCycleOrdinal : Nat
  lastReceiptDigest : Nat
  receiptDigests : List Nat
  authorityInventory : List Nat
  humanApprovalInventory : List Nat
  hostLicenseInventory : List Nat
  allDigestLinksExact : Bool
  allCyclesMaterialized : Bool
  allNativeClosuresCompleted : Bool
  allCyclesClosed : Bool
  allReceiptsImmutable : Bool
  allReceiptsAppendOnly : Bool
  allReceiptsNonConsumable : Bool
  allAuthoritiesSingleUse : Bool
  noAuthorityInheritance : Bool
  noAuthorityRenewal : Bool
  prefixImmutable : Bool
  appendOnlyExtension : Bool
  nextActStarted : Bool
  allBlockersActive : Bool
  exactWorldUpdated : Bool
  historyOverwritten : Bool
  truthPromoted : Bool
  chainGrantsExecution : Bool
  cycle_count_positive : 0 < cycleCount
  cycle_count_matches_last : cycleCount = lastCycleOrdinal
  receipt_count_exact : receiptDigests.length = cycleCount
  authority_count_exact : authorityInventory.length = cycleCount
  approval_count_exact : humanApprovalInventory.length = cycleCount
  host_license_count_exact : hostLicenseInventory.length = cycleCount
  digest_links_exact : allDigestLinksExact = true
  cycles_materialized : allCyclesMaterialized = true
  native_closures_completed : allNativeClosuresCompleted = true
  cycles_closed : allCyclesClosed = true
  receipts_immutable : allReceiptsImmutable = true
  receipts_append_only : allReceiptsAppendOnly = true
  receipts_non_consumable : allReceiptsNonConsumable = true
  authorities_single_use : allAuthoritiesSingleUse = true
  authority_not_inherited : noAuthorityInheritance = true
  authority_not_renewed : noAuthorityRenewal = true
  prefix_immutable : prefixImmutable = true
  append_only : appendOnlyExtension = true
  next_act_not_started : nextActStarted = false
  blockers_active : allBlockersActive = true
  exact_world_not_updated : exactWorldUpdated = false
  history_not_overwritten : historyOverwritten = false
  truth_not_promoted : truthPromoted = false
  chain_non_authoritative : chainGrantsExecution = false

namespace InductiveLicensedCycleChain


def fromTwoCycleSeed (s : TwoCycleLicensedChainSeed) :
    InductiveLicensedCycleChain where
  cycleCount := 2
  lastCycleOrdinal := 2
  lastReceiptDigest := s.secondReceiptDigest
  receiptDigests := [s.firstReceiptDigest, s.secondReceiptDigest]
  authorityInventory := [s.firstAuthorityDigest, s.secondAuthorityDigest]
  humanApprovalInventory := [s.firstHumanApprovalDigest, s.secondHumanApprovalDigest]
  hostLicenseInventory := [s.firstHostLicenseDigest, s.secondHostLicenseDigest]
  allDigestLinksExact := true
  allCyclesMaterialized := true
  allNativeClosuresCompleted := true
  allCyclesClosed := true
  allReceiptsImmutable := true
  allReceiptsAppendOnly := true
  allReceiptsNonConsumable := true
  allAuthoritiesSingleUse := true
  noAuthorityInheritance := true
  noAuthorityRenewal := true
  prefixImmutable := true
  appendOnlyExtension := true
  nextActStarted := false
  allBlockersActive := true
  exactWorldUpdated := false
  historyOverwritten := false
  truthPromoted := false
  chainGrantsExecution := false
  cycle_count_positive := by decide
  cycle_count_matches_last := rfl
  receipt_count_exact := rfl
  authority_count_exact := rfl
  approval_count_exact := rfl
  host_license_count_exact := rfl
  digest_links_exact := rfl
  cycles_materialized := rfl
  native_closures_completed := rfl
  cycles_closed := rfl
  receipts_immutable := rfl
  receipts_append_only := rfl
  receipts_non_consumable := rfl
  authorities_single_use := rfl
  authority_not_inherited := rfl
  authority_not_renewed := rfl
  prefix_immutable := rfl
  append_only := rfl
  next_act_not_started := rfl
  blockers_active := rfl
  exact_world_not_updated := rfl
  history_not_overwritten := rfl
  truth_not_promoted := rfl
  chain_non_authoritative := rfl

structure LicensedCycleExtensionWitness
    (c : InductiveLicensedCycleChain) where
  targetCycleOrdinal : Nat
  predecessorReceiptDigest : Nat
  closedCycleReceiptDigest : Nat
  freshAuthorityDigest : Nat
  newHumanApprovalDigest : Nat
  newHostLicenseDigest : Nat
  cycleMaterialized : Bool
  nativeClosureCompleted : Bool
  cycleClosed : Bool
  receiptImmutable : Bool
  receiptAppendOnly : Bool
  receiptConsumptionCount : Nat
  authorityConsumptionCount : Nat
  authorityRenewable : Bool
  authorityInheritable : Bool
  nextActStarted : Bool
  allBlockersActive : Bool
  witnessGrantsExecution : Bool
  target_is_immediate_successor : targetCycleOrdinal = c.cycleCount + 1
  predecessor_link_exact : predecessorReceiptDigest = c.lastReceiptDigest
  authority_fresh : freshAuthorityDigest ∉ c.authorityInventory
  approval_fresh : newHumanApprovalDigest ∉ c.humanApprovalInventory
  host_license_fresh : newHostLicenseDigest ∉ c.hostLicenseInventory
  cycle_materialized : cycleMaterialized = true
  native_closure_completed : nativeClosureCompleted = true
  cycle_closed : cycleClosed = true
  receipt_immutable : receiptImmutable = true
  receipt_append_only : receiptAppendOnly = true
  receipt_not_consumed : receiptConsumptionCount = 0
  authority_consumed_once : authorityConsumptionCount = 1
  authority_not_renewable : authorityRenewable = false
  authority_not_inheritable : authorityInheritable = false
  next_act_not_started : nextActStarted = false
  blockers_active : allBlockersActive = true
  witness_non_authoritative : witnessGrantsExecution = false


def appendClosedCycle
    (c : InductiveLicensedCycleChain)
    (w : LicensedCycleExtensionWitness c) :
    InductiveLicensedCycleChain where
  cycleCount := c.cycleCount + 1
  lastCycleOrdinal := w.targetCycleOrdinal
  lastReceiptDigest := w.closedCycleReceiptDigest
  receiptDigests := c.receiptDigests ++ [w.closedCycleReceiptDigest]
  authorityInventory := c.authorityInventory ++ [w.freshAuthorityDigest]
  humanApprovalInventory := c.humanApprovalInventory ++ [w.newHumanApprovalDigest]
  hostLicenseInventory := c.hostLicenseInventory ++ [w.newHostLicenseDigest]
  allDigestLinksExact := true
  allCyclesMaterialized := true
  allNativeClosuresCompleted := true
  allCyclesClosed := true
  allReceiptsImmutable := true
  allReceiptsAppendOnly := true
  allReceiptsNonConsumable := true
  allAuthoritiesSingleUse := true
  noAuthorityInheritance := true
  noAuthorityRenewal := true
  prefixImmutable := true
  appendOnlyExtension := true
  nextActStarted := false
  allBlockersActive := true
  exactWorldUpdated := false
  historyOverwritten := false
  truthPromoted := false
  chainGrantsExecution := false
  cycle_count_positive := Nat.succ_pos c.cycleCount
  cycle_count_matches_last := by
    simpa [w.target_is_immediate_successor]
  receipt_count_exact := by
    simp [c.receipt_count_exact]
  authority_count_exact := by
    simp [c.authority_count_exact]
  approval_count_exact := by
    simp [c.approval_count_exact]
  host_license_count_exact := by
    simp [c.host_license_count_exact]
  digest_links_exact := rfl
  cycles_materialized := rfl
  native_closures_completed := rfl
  cycles_closed := rfl
  receipts_immutable := rfl
  receipts_append_only := rfl
  receipts_non_consumable := rfl
  authorities_single_use := rfl
  authority_not_inherited := rfl
  authority_not_renewed := rfl
  prefix_immutable := rfl
  append_only := rfl
  next_act_not_started := rfl
  blockers_active := rfl
  exact_world_not_updated := rfl
  history_not_overwritten := rfl
  truth_not_promoted := rfl
  chain_non_authoritative := rfl


theorem append_increments_cycle_count
    (c : InductiveLicensedCycleChain)
    (w : LicensedCycleExtensionWitness c) :
    (appendClosedCycle c w).cycleCount = c.cycleCount + 1 := rfl


theorem append_preserves_receipt_prefix
    (c : InductiveLicensedCycleChain)
    (w : LicensedCycleExtensionWitness c) :
    (appendClosedCycle c w).receiptDigests =
      c.receiptDigests ++ [w.closedCycleReceiptDigest] := rfl


theorem append_preserves_authority_prefix
    (c : InductiveLicensedCycleChain)
    (w : LicensedCycleExtensionWitness c) :
    (appendClosedCycle c w).authorityInventory =
      c.authorityInventory ++ [w.freshAuthorityDigest] := rfl


theorem appended_authority_was_fresh
    (c : InductiveLicensedCycleChain)
    (w : LicensedCycleExtensionWitness c) :
    w.freshAuthorityDigest ∉ c.authorityInventory :=
  w.authority_fresh


theorem licensed_multi_cycle_chain_induction_boundary
    (c : InductiveLicensedCycleChain)
    (w : LicensedCycleExtensionWitness c) :
    let next := appendClosedCycle c w
    next.cycleCount = c.cycleCount + 1 ∧
      next.lastCycleOrdinal = w.targetCycleOrdinal ∧
      w.predecessorReceiptDigest = c.lastReceiptDigest ∧
      next.receiptDigests = c.receiptDigests ++ [w.closedCycleReceiptDigest] ∧
      next.authorityInventory = c.authorityInventory ++ [w.freshAuthorityDigest] ∧
      w.freshAuthorityDigest ∉ c.authorityInventory ∧
      w.newHumanApprovalDigest ∉ c.humanApprovalInventory ∧
      w.newHostLicenseDigest ∉ c.hostLicenseInventory ∧
      next.allCyclesClosed = true ∧
      next.allReceiptsNonConsumable = true ∧
      next.nextActStarted = false ∧
      next.allBlockersActive = true ∧
      next.chainGrantsExecution = false := by
  exact ⟨rfl, rfl, w.predecessor_link_exact, rfl, rfl,
    w.authority_fresh, w.approval_fresh, w.host_license_fresh,
    rfl, rfl, rfl, rfl, rfl⟩

end InductiveLicensedCycleChain

end KUOS.Architecture
