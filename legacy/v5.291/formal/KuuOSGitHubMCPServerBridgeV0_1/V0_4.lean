import KuuOSGitHubMCPServerBridgeV0_1.V0_3

namespace KuuOS.GitHubMCPServerBridgeV0_4

structure LiveCanaryGate where
  createCloseout : KuuOS.GitHubMCPServerBridgeV0_3.LiveWriteVerificationGate
  explicitConfirmation : Bool
  officialImagePinned : Bool
  resolvedImageDigestRecorded : Bool
  sameIssueBound : Bool
  closeApplied : Bool
  closedReobserved : Bool
  compensationUsed : Bool
  deriving DecidableEq, Repr

def LiveCanaryGate.Admitted (gate : LiveCanaryGate) : Prop :=
  gate.createCloseout.Admitted ∧
  gate.explicitConfirmation = true ∧
  gate.officialImagePinned = true ∧
  gate.resolvedImageDigestRecorded = true ∧
  gate.sameIssueBound = true ∧
  gate.closeApplied = true ∧
  gate.closedReobserved = true ∧
  gate.compensationUsed = false

theorem admitted_implies_create_closeout
    (gate : LiveCanaryGate)
    (h : gate.Admitted) : gate.createCloseout.Admitted :=
  h.1

theorem admitted_implies_explicit_confirmation
    (gate : LiveCanaryGate)
    (h : gate.Admitted) : gate.explicitConfirmation = true :=
  h.2.1

theorem admitted_implies_pinned_official_image
    (gate : LiveCanaryGate)
    (h : gate.Admitted) : gate.officialImagePinned = true :=
  h.2.2.1

theorem admitted_implies_resolved_digest
    (gate : LiveCanaryGate)
    (h : gate.Admitted) : gate.resolvedImageDigestRecorded = true :=
  h.2.2.2.1

theorem admitted_implies_same_issue
    (gate : LiveCanaryGate)
    (h : gate.Admitted) : gate.sameIssueBound = true :=
  h.2.2.2.2.1

theorem admitted_implies_close_applied
    (gate : LiveCanaryGate)
    (h : gate.Admitted) : gate.closeApplied = true :=
  h.2.2.2.2.2.1

theorem admitted_implies_closed_reobserved
    (gate : LiveCanaryGate)
    (h : gate.Admitted) : gate.closedReobserved = true :=
  h.2.2.2.2.2.2.1

theorem admitted_excludes_compensation
    (gate : LiveCanaryGate)
    (h : gate.Admitted) : gate.compensationUsed = false :=
  h.2.2.2.2.2.2.2

@[simp] theorem compensation_never_admits
    (gate : LiveCanaryGate)
    (hCompensation : gate.compensationUsed = true) : ¬ gate.Admitted := by
  intro h
  have hNoCompensation : gate.compensationUsed = false :=
    admitted_excludes_compensation gate h
  simp [hCompensation] at hNoCompensation

@[simp] theorem unclosed_canary_never_admits
    (gate : LiveCanaryGate)
    (hOpen : gate.closedReobserved = false) : ¬ gate.Admitted := by
  intro h
  have hClosed : gate.closedReobserved = true :=
    admitted_implies_closed_reobserved gate h
  simp [hOpen] at hClosed

theorem admitted_implies_reversible_live_canary_closeout
    (gate : LiveCanaryGate)
    (h : gate.Admitted) :
    gate.createCloseout.Admitted ∧
    gate.explicitConfirmation = true ∧
    gate.officialImagePinned = true ∧
    gate.resolvedImageDigestRecorded = true ∧
    gate.sameIssueBound = true ∧
    gate.closeApplied = true ∧
    gate.closedReobserved = true ∧
    gate.compensationUsed = false :=
  h

end KuuOS.GitHubMCPServerBridgeV0_4
