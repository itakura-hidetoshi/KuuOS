import Mathlib
import KUOS.Architecture.QiWorldCrossCycleReentryV1_4

namespace KUOS.Architecture

inductive CrossCycleBlocker
  | presentActivation
  | executionBoundary
  | memoryPreservation
  | worldPreservation
  | truthSeparation
  | cycleSeparation
  | noncollapse
  deriving DecidableEq, Fintype

abbrev CrossCycleBlockerVector := CrossCycleBlocker → Bool

def blockerTop : CrossCycleBlockerVector := fun _ => true

def blockerMeet
    (left right : CrossCycleBlockerVector) : CrossCycleBlockerVector :=
  fun blocker => left blocker && right blocker

def AllBlockersActive (vector : CrossCycleBlockerVector) : Prop :=
  ∀ blocker, vector blocker = true

def BlockerLe (left right : CrossCycleBlockerVector) : Prop :=
  ∀ blocker, left blocker = true → right blocker = true

theorem blockerMeet_comm (left right : CrossCycleBlockerVector) :
    blockerMeet left right = blockerMeet right left := by
  funext blocker
  cases h₁ : left blocker <;> cases h₂ : right blocker <;>
    simp [blockerMeet, h₁, h₂]

theorem blockerMeet_assoc
    (first second third : CrossCycleBlockerVector) :
    blockerMeet (blockerMeet first second) third =
      blockerMeet first (blockerMeet second third) := by
  funext blocker
  cases h₁ : first blocker <;>
    cases h₂ : second blocker <;>
      cases h₃ : third blocker <;>
        simp [blockerMeet, h₁, h₂, h₃]

theorem blockerMeet_idem (vector : CrossCycleBlockerVector) :
    blockerMeet vector vector = vector := by
  funext blocker
  cases h : vector blocker <;> simp [blockerMeet, h]

theorem blockerMeet_top (vector : CrossCycleBlockerVector) :
    blockerMeet vector blockerTop = vector := by
  funext blocker
  cases h : vector blocker <;> simp [blockerMeet, blockerTop, h]

theorem blockerMeet_le_left (left right : CrossCycleBlockerVector) :
    BlockerLe (blockerMeet left right) left := by
  intro blocker h
  cases h₁ : left blocker <;> cases h₂ : right blocker <;>
    simp [blockerMeet, h₁, h₂] at h ⊢

theorem blockerMeet_le_right (left right : CrossCycleBlockerVector) :
    BlockerLe (blockerMeet left right) right := by
  rw [blockerMeet_comm]
  exact blockerMeet_le_left right left

def blockerVectorOf
    (reentry : QiWorldCrossCycleReentry) : CrossCycleBlockerVector
  | .presentActivation => !reentry.nextActStarted
  | .executionBoundary =>
      (!reentry.bridgeGrantsExecution) && (!reentry.bridgeIssuesAuthority)
  | .memoryPreservation => !reentry.bridgeOverwritesPreviousCycle
  | .worldPreservation => !reentry.exactWorldUpdated
  | .truthSeparation => !reentry.bridgeIssuesAuthority
  | .cycleSeparation =>
      (!reentry.nextActStarted) && (!reentry.bridgeGrantsExecution)
  | .noncollapse => !reentry.exactWorldUpdated

theorem blockerVectorOf_all_active
    (reentry : QiWorldCrossCycleReentry) :
    AllBlockersActive (blockerVectorOf reentry) := by
  intro blocker
  cases blocker <;>
    simp [blockerVectorOf,
      reentry.next_act_not_started,
      reentry.no_bridge_execution_authority,
      reentry.no_bridge_authority_issue,
      reentry.no_previous_cycle_overwrite,
      reentry.exact_world_not_updated]

structure CrossCycleBlockerCertificate where
  source : QiWorldCrossCycleReentry
  vector : CrossCycleBlockerVector
  vector_eq : vector = blockerVectorOf source
  all_active : AllBlockersActive vector
  bounded : Prop
  boundedProof : bounded
  contextual : Prop
  contextualProof : contextual
  repairable : Prop
  repairableProof : repairable
  failClosed : Prop
  failClosedProof : failClosed
  grantsExecution : Bool
  noExecution : grantsExecution = false
  grantsTruth : Bool
  noTruth : grantsTruth = false
  updatesWorld : Bool
  noWorldUpdate : updatesWorld = false

namespace CrossCycleBlockerCertificate

variable (certificate : CrossCycleBlockerCertificate)

theorem active_package :
    certificate.vector .presentActivation = true ∧
    certificate.vector .executionBoundary = true ∧
    certificate.vector .memoryPreservation = true ∧
    certificate.vector .worldPreservation = true ∧
    certificate.vector .truthSeparation = true ∧
    certificate.vector .cycleSeparation = true ∧
    certificate.vector .noncollapse = true :=
  ⟨certificate.all_active .presentActivation,
    certificate.all_active .executionBoundary,
    certificate.all_active .memoryPreservation,
    certificate.all_active .worldPreservation,
    certificate.all_active .truthSeparation,
    certificate.all_active .cycleSeparation,
    certificate.all_active .noncollapse⟩

theorem bounded_contextual_repairable :
    certificate.bounded ∧ certificate.contextual ∧
    certificate.repairable ∧ certificate.failClosed :=
  ⟨certificate.boundedProof, certificate.contextualProof,
    certificate.repairableProof, certificate.failClosedProof⟩

theorem no_positive_authority :
    certificate.grantsExecution = false ∧
    certificate.grantsTruth = false ∧
    certificate.updatesWorld = false :=
  ⟨certificate.noExecution, certificate.noTruth, certificate.noWorldUpdate⟩

end CrossCycleBlockerCertificate

theorem boundary_loss_not_all_active
    (vector : CrossCycleBlockerVector)
    (loss : ∃ blocker, vector blocker = false) :
    ¬AllBlockersActive vector := by
  intro allActive
  rcases loss with ⟨blocker, hFalse⟩
  have hTrue := allActive blocker
  rw [hFalse] at hTrue
  cases hTrue

end KUOS.Architecture
