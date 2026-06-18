import Mathlib
import KUOS.PlanOS.BoundedMultiGenerationSupervisorV0_6

namespace KUOS.PlanOS

inductive TerminalKind where
  | hold | handover | stopped
  deriving DecidableEq

inductive ReentryKind where
  | resumeHold | acceptHandover
  deriving DecidableEq

structure ReentryReceipt where
  kind : ReentryKind
  source : TerminalKind
  currentOwner proposedOwner delegatedBy acceptedBy : Nat
  sourceDigest expectedDigest : Nat
  lineagePreserved missionPreserved policyPreserved singleUse : Bool


def admissibleReentry (r : ReentryReceipt) : Prop :=
  r.sourceDigest = r.expectedDigest ∧
  r.lineagePreserved = true ∧
  r.missionPreserved = true ∧
  r.policyPreserved = true ∧
  r.singleUse = true ∧
  match r.kind, r.source with
  | .resumeHold, .hold =>
      r.proposedOwner = r.currentOwner ∧
      r.delegatedBy = r.currentOwner ∧
      r.acceptedBy = r.currentOwner
  | .acceptHandover, .handover =>
      r.proposedOwner ≠ r.currentOwner ∧
      r.delegatedBy = r.currentOwner ∧
      r.acceptedBy = r.proposedOwner
  | _, _ => False


theorem stopped_not_reenterable (r : ReentryReceipt)
    (h : r.source = .stopped) : ¬ admissibleReentry r := by
  intro hadm
  rcases hadm with ⟨_, _, _, _, _, route⟩
  cases r.kind <;> simp [h] at route


theorem hold_resume_preserves_owner (r : ReentryReceipt)
    (hk : r.kind = .resumeHold) (hs : r.source = .hold)
    (hadm : admissibleReentry r) :
    r.proposedOwner = r.currentOwner := by
  rcases hadm with ⟨_, _, _, _, _, route⟩
  simpa [hk, hs] using route.1


theorem handover_requires_new_owner (r : ReentryReceipt)
    (hk : r.kind = .acceptHandover) (hs : r.source = .handover)
    (hadm : admissibleReentry r) :
    r.proposedOwner ≠ r.currentOwner := by
  rcases hadm with ⟨_, _, _, _, _, route⟩
  simpa [hk, hs] using route.1

structure ReentryBoundary where
  executionGranted hostLicenseGranted memoryOverwrite : Bool
  noExecution : executionGranted = false
  noHostLicense : hostLicenseGranted = false
  noOverwrite : memoryOverwrite = false


theorem reentry_grants_no_authority (b : ReentryBoundary) :
    b.executionGranted = false ∧
    b.hostLicenseGranted = false ∧
    b.memoryOverwrite = false := by
  exact ⟨b.noExecution, b.noHostLicense, b.noOverwrite⟩

structure ReentryTransition where
  sourceDigest preservedSourceDigest : Nat
  nextGenerationAuthorized : Bool
  sourcePreserved : preservedSourceDigest = sourceDigest
  nextAuthorized : nextGenerationAuthorized = true


theorem reentry_preserves_source_and_authorizes_next
    (t : ReentryTransition) :
    t.preservedSourceDigest = t.sourceDigest ∧
    t.nextGenerationAuthorized = true := by
  exact ⟨t.sourcePreserved, t.nextAuthorized⟩

end KUOS.PlanOS
