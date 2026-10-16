import Mathlib
import KUOS.PlanOS.BoundedMultiGenerationSupervisorV0_6

namespace KUOS.PlanOS

inductive TerminalKind where
  | hold
  | handover
  | stopped
  deriving DecidableEq

inductive ReentryKind where
  | resumeHold
  | acceptHandover
  deriving DecidableEq

structure ReentryReceipt where
  kind : ReentryKind
  source : TerminalKind
  currentOwner : Nat
  proposedOwner : Nat
  delegatedBy : Nat
  acceptedBy : Nat
  sourceDigest : Nat
  expectedDigest : Nat
  lineagePreserved : Bool
  missionPreserved : Bool
  policyPreserved : Bool
  singleUse : Bool


def admissibleReentry (r : ReentryReceipt) : Prop :=
  r.sourceDigest = r.expectedDigest ∧
  r.lineagePreserved = true ∧
  r.missionPreserved = true ∧
  r.policyPreserved = true ∧
  r.singleUse = true ∧
  match r.kind, r.source with
  | ReentryKind.resumeHold, TerminalKind.hold =>
      r.proposedOwner = r.currentOwner ∧
      r.delegatedBy = r.currentOwner ∧
      r.acceptedBy = r.currentOwner
  | ReentryKind.acceptHandover, TerminalKind.handover =>
      r.proposedOwner ≠ r.currentOwner ∧
      r.delegatedBy = r.currentOwner ∧
      r.acceptedBy = r.proposedOwner
  | _, _ => False


theorem stopped_not_reenterable (r : ReentryReceipt)
    (h : r.source = TerminalKind.stopped) :
    ¬ admissibleReentry r := by
  intro hadm
  rcases hadm with ⟨_, _, _, _, _, route⟩
  rw [h] at route
  cases r.kind <;> simp at route


theorem hold_resume_preserves_owner (r : ReentryReceipt)
    (hk : r.kind = ReentryKind.resumeHold)
    (hs : r.source = TerminalKind.hold)
    (hadm : admissibleReentry r) :
    r.proposedOwner = r.currentOwner := by
  rcases hadm with ⟨_, _, _, _, _, route⟩
  rw [hk, hs] at route
  exact route.1


theorem handover_requires_new_owner (r : ReentryReceipt)
    (hk : r.kind = ReentryKind.acceptHandover)
    (hs : r.source = TerminalKind.handover)
    (hadm : admissibleReentry r) :
    r.proposedOwner ≠ r.currentOwner := by
  rcases hadm with ⟨_, _, _, _, _, route⟩
  rw [hk, hs] at route
  exact route.1

structure ReentryBoundary where
  executionGranted : Bool
  hostLicenseGranted : Bool
  memoryOverwrite : Bool
  noExecution : executionGranted = false
  noHostLicense : hostLicenseGranted = false
  noOverwrite : memoryOverwrite = false


theorem reentry_grants_no_authority (b : ReentryBoundary) :
    b.executionGranted = false ∧
    b.hostLicenseGranted = false ∧
    b.memoryOverwrite = false := by
  exact ⟨b.noExecution, b.noHostLicense, b.noOverwrite⟩

structure ReentryTransition where
  sourceDigest : Nat
  preservedSourceDigest : Nat
  nextGenerationAuthorized : Bool
  sourcePreserved : preservedSourceDigest = sourceDigest
  nextAuthorized : nextGenerationAuthorized = true


theorem reentry_preserves_source_and_authorizes_next
    (t : ReentryTransition) :
    t.preservedSourceDigest = t.sourceDigest ∧
    t.nextGenerationAuthorized = true := by
  exact ⟨t.sourcePreserved, t.nextAuthorized⟩

end KUOS.PlanOS
