/-
Regge Zero Governance v0.1

Lean-facing non-authoritative formal surface.
This file models governance distinctions only. It does not prove string theory,
derive physical amplitudes, authorize execution, or authorize medical action.
-/

namespace KuuOS
namespace ReggeZeroGovernance

inductive CandidateKind where
  | designCandidate
  | runtimeTick
  | qiReadout
  | ciReceipt
  | memoryRecord
  | reflectionSummary
  | crossOSCandidate
  deriving DecidableEq, Repr

inductive AuthorityKind where
  | noAuthority
  | theoremAuthority
  | autonomousExecutionAuthority
  | treatmentAuthorization
  | beliefSovereignty
  | rootRewrite
  deriving DecidableEq, Repr

inductive Witness where
  | boundaryViolation
  | provenanceGap
  | supportGap
  | harmVisibilityGap
  | authorityShortcut
  | consistencyFailure
  | cyclicInconsistency
  | runtimeLicenseFailure
  | medicalAuthorizationShortcut
  | proofAuthorityShortcut
  | memorySovereigntyShortcut
  | silentOverwriteRisk
  | uncertaintyCollapse
  deriving DecidableEq, Repr

inductive SoftConcern where
  | novelty
  | complexity
  | unfamiliarity
  | nonstandardFraming
  | lowAestheticFit
  deriving DecidableEq, Repr

inductive Outcome where
  | pass
  | hold
  | repair
  | reject
  | quarantine
  | advisoryOnly
  deriving DecidableEq, Repr

structure Candidate where
  kind : CandidateKind
  claimedAuthority : AuthorityKind
  witnesses : List Witness
  softConcerns : List SoftConcern
  inheritedNulls : List Witness
  cyclicReceiptPass : Bool
  destructiveReplacementClaimed : Bool
  deriving Repr

def hasWitness (c : Candidate) : Bool :=
  !(c.witnesses ++ c.inheritedNulls).isEmpty

def isBlocking : Outcome -> Bool
  | Outcome.hold => true
  | Outcome.repair => true
  | Outcome.reject => true
  | Outcome.quarantine => true
  | _ => false

def authorityShortcut (c : Candidate) : Bool :=
  c.claimedAuthority != AuthorityKind.noAuthority

def destructiveRootRewrite (c : Candidate) : Bool :=
  c.kind == CandidateKind.reflectionSummary &&
  c.claimedAuthority == AuthorityKind.rootRewrite &&
  c.destructiveReplacementClaimed

def cyclicFailure (c : Candidate) : Bool :=
  c.cyclicReceiptPass == false

def reggeZeroGate (c : Candidate) : Outcome :=
  if destructiveRootRewrite c then Outcome.reject
  else if authorityShortcut c then Outcome.hold
  else if cyclicFailure c then Outcome.hold
  else if hasWitness c then Outcome.hold
  else if !c.softConcerns.isEmpty then Outcome.advisoryOnly
  else Outcome.pass

theorem no_soft_concern_blocks_without_witness
    (c : Candidate)
    (hAuth : c.claimedAuthority = AuthorityKind.noAuthority)
    (hCyclic : c.cyclicReceiptPass = true)
    (hNoWitness : c.witnesses = [] ∧ c.inheritedNulls = [])
    (hSoft : c.softConcerns ≠ []) :
    reggeZeroGate c = Outcome.advisoryOnly := by
  unfold reggeZeroGate destructiveRootRewrite authorityShortcut cyclicFailure hasWitness
  simp [hAuth, hCyclic, hNoWitness.1, hNoWitness.2, hSoft]

theorem authority_shortcut_holds
    (c : Candidate)
    (h : c.claimedAuthority ≠ AuthorityKind.noAuthority)
    (hNotRewrite : destructiveRootRewrite c = false) :
    reggeZeroGate c = Outcome.hold := by
  unfold reggeZeroGate authorityShortcut
  simp [hNotRewrite, h]

theorem destructive_reflection_rewrite_rejects
    (c : Candidate)
    (h : destructiveRootRewrite c = true) :
    reggeZeroGate c = Outcome.reject := by
  unfold reggeZeroGate
  simp [h]

theorem cyclic_failure_holds_without_authority_shortcut
    (c : Candidate)
    (hRewrite : destructiveRootRewrite c = false)
    (hAuth : c.claimedAuthority = AuthorityKind.noAuthority)
    (hCyclic : c.cyclicReceiptPass = false) :
    reggeZeroGate c = Outcome.hold := by
  unfold reggeZeroGate authorityShortcut cyclicFailure
  simp [hRewrite, hAuth, hCyclic]

end ReggeZeroGovernance
end KuuOS
