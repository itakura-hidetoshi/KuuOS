import Mathlib
import KUOS.PlanOS.ExternalResumeHandoverReentryV0_7

namespace KUOS.PlanOS

inductive OwnershipStage where
  | plan
  | act
  | observe
  | verify
  | learn
  deriving DecidableEq


def stageRank : OwnershipStage → Nat
  | OwnershipStage.plan => 0
  | OwnershipStage.act => 1
  | OwnershipStage.observe => 2
  | OwnershipStage.verify => 3
  | OwnershipStage.learn => 4

structure OwnershipRoot where
  previousOwner : Nat
  currentOwner : Nat
  handover : Bool
  externalReceiptDigest : Nat
  reentryDecisionDigest : Nat
  reentryEventDigest : Nat
  reenteredStateDigest : Nat
  targetActiveStateDigest : Nat

structure OwnershipStageReceipt where
  stage : OwnershipStage
  stageIndex : Nat
  owner : Nat
  externalReceiptDigest : Nat
  reentryDecisionDigest : Nat
  reentryEventDigest : Nat
  reenteredStateDigest : Nat
  targetActiveStateDigest : Nat
  predecessorStateDigest : Nat
  predecessorStageDigest : Nat
  handoffReceiptDigest : Nat
  completionReceiptDigest : Nat


def ownerAdmissible (root : OwnershipRoot) (owner : Nat) : Prop :=
  owner = root.currentOwner ∧
    (root.handover = true → owner ≠ root.previousOwner)


def stageAdmissible
    (root : OwnershipRoot)
    (expectedStage : OwnershipStage)
    (expectedIndex : Nat)
    (receipt : OwnershipStageReceipt) : Prop :=
  receipt.stage = expectedStage ∧
  receipt.stageIndex = expectedIndex ∧
  ownerAdmissible root receipt.owner ∧
  receipt.externalReceiptDigest = root.externalReceiptDigest ∧
  receipt.reentryDecisionDigest = root.reentryDecisionDigest ∧
  receipt.reentryEventDigest = root.reentryEventDigest ∧
  receipt.reenteredStateDigest = root.reenteredStateDigest ∧
  receipt.targetActiveStateDigest = root.targetActiveStateDigest


theorem admissible_stage_uses_current_owner
    (root : OwnershipRoot)
    (receipt : OwnershipStageReceipt)
    (stage : OwnershipStage)
    (index : Nat)
    (h : stageAdmissible root stage index receipt) :
    receipt.owner = root.currentOwner := by
  exact h.2.2.1


theorem handover_previous_owner_not_admissible
    (root : OwnershipRoot)
    (handover : root.handover = true)
    (ownersDiffer : root.previousOwner ≠ root.currentOwner) :
    ¬ ownerAdmissible root root.previousOwner := by
  intro h
  exact ownersDiffer h.1


theorem admissible_stage_preserves_reentry_bindings
    (root : OwnershipRoot)
    (receipt : OwnershipStageReceipt)
    (stage : OwnershipStage)
    (index : Nat)
    (h : stageAdmissible root stage index receipt) :
    receipt.externalReceiptDigest = root.externalReceiptDigest ∧
    receipt.reentryDecisionDigest = root.reentryDecisionDigest ∧
    receipt.reentryEventDigest = root.reentryEventDigest ∧
    receipt.reenteredStateDigest = root.reenteredStateDigest ∧
    receipt.targetActiveStateDigest = root.targetActiveStateDigest := by
  exact h.2.2.2


theorem admissible_stage_preserves_order
    (root : OwnershipRoot)
    (receipt : OwnershipStageReceipt)
    (stage : OwnershipStage)
    (index : Nat)
    (h : stageAdmissible root stage index receipt) :
    receipt.stage = stage ∧ receipt.stageIndex = index := by
  exact ⟨h.1, h.2.1⟩


theorem fixed_pipeline_ranks :
    stageRank OwnershipStage.plan = 0 ∧
    stageRank OwnershipStage.act = 1 ∧
    stageRank OwnershipStage.observe = 2 ∧
    stageRank OwnershipStage.verify = 3 ∧
    stageRank OwnershipStage.learn = 4 := by
  decide

structure OwnershipAuthorityBoundary where
  executionGranted : Bool
  hostLicenseGranted : Bool
  memoryOverwrite : Bool
  noExecution : executionGranted = false
  noHostLicense : hostLicenseGranted = false
  noOverwrite : memoryOverwrite = false


theorem ownership_wrapper_grants_no_authority
    (boundary : OwnershipAuthorityBoundary) :
    boundary.executionGranted = false ∧
    boundary.hostLicenseGranted = false ∧
    boundary.memoryOverwrite = false := by
  exact ⟨boundary.noExecution, boundary.noHostLicense, boundary.noOverwrite⟩

end KUOS.PlanOS
