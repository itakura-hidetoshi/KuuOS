import KuuOSGitHubMCPServerBridgeV0_1.V0_2

namespace KuuOS.GitHubMCPServerBridgeV0_3

structure LiveWriteVerificationGate where
  writeAuthority : KuuOS.GitHubMCPServerBridgeV0_2.MCPWriteAuthority
  writeApplied : Bool
  reobservationAllowed : Bool
  verificationToolReadOnly : Bool
  repositoryMatches : Bool
  observedEffectMatches : Bool
  deriving DecidableEq, Repr

def LiveWriteVerificationGate.Admitted
    (gate : LiveWriteVerificationGate) : Prop :=
  gate.writeAuthority.Admitted ∧
  gate.writeApplied = true ∧
  gate.reobservationAllowed = true ∧
  gate.verificationToolReadOnly = true ∧
  gate.repositoryMatches = true ∧
  gate.observedEffectMatches = true

theorem admitted_implies_write_authority
    (gate : LiveWriteVerificationGate)
    (h : gate.Admitted) : gate.writeAuthority.Admitted :=
  h.1

theorem admitted_implies_write_applied
    (gate : LiveWriteVerificationGate)
    (h : gate.Admitted) : gate.writeApplied = true :=
  h.2.1

theorem admitted_implies_reobservation_authority
    (gate : LiveWriteVerificationGate)
    (h : gate.Admitted) : gate.reobservationAllowed = true :=
  h.2.2.1

theorem admitted_implies_read_only_verification_tool
    (gate : LiveWriteVerificationGate)
    (h : gate.Admitted) : gate.verificationToolReadOnly = true :=
  h.2.2.2.1

theorem admitted_implies_exact_repository
    (gate : LiveWriteVerificationGate)
    (h : gate.Admitted) : gate.repositoryMatches = true :=
  h.2.2.2.2.1

theorem admitted_implies_observed_effect
    (gate : LiveWriteVerificationGate)
    (h : gate.Admitted) : gate.observedEffectMatches = true :=
  h.2.2.2.2.2

theorem admitted_implies_write_capable_session
    (gate : LiveWriteVerificationGate)
    (h : gate.Admitted) : gate.writeAuthority.readOnly = false :=
  h.1.1

theorem admitted_implies_complete_live_closeout
    (gate : LiveWriteVerificationGate)
    (h : gate.Admitted) :
    gate.writeAuthority.Admitted ∧
    gate.writeApplied = true ∧
    gate.reobservationAllowed = true ∧
    gate.verificationToolReadOnly = true ∧
    gate.repositoryMatches = true ∧
    gate.observedEffectMatches = true :=
  h

end KuuOS.GitHubMCPServerBridgeV0_3
