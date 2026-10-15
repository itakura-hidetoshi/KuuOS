import Mathlib

namespace KuuOS.GitHubMCPServerBridgeV0_2

structure MCPWriteAuthority where
  readOnly : Bool
  runtimeExecuteExternalActions : Bool
  planExecuteExternalActions : Bool
  externalActionAllowed : Bool
  mcpWriteToolCallAllowed : Bool
  operationApproved : Bool
  repositoryMatches : Bool
  baseShaMatches : Bool
  deriving DecidableEq, Repr

def MCPWriteAuthority.Admitted (gate : MCPWriteAuthority) : Prop :=
  gate.readOnly = false ∧
  gate.runtimeExecuteExternalActions = true ∧
  gate.planExecuteExternalActions = true ∧
  gate.externalActionAllowed = true ∧
  gate.mcpWriteToolCallAllowed = true ∧
  gate.operationApproved = true ∧
  gate.repositoryMatches = true ∧
  gate.baseShaMatches = true

@[simp] theorem readOnly_never_admits (gate : MCPWriteAuthority)
    (hReadOnly : gate.readOnly = true) : ¬ gate.Admitted := by
  intro h
  have hFalse : gate.readOnly = false := h.1
  simp [hReadOnly] at hFalse

theorem admitted_implies_write_enabled (gate : MCPWriteAuthority)
    (h : gate.Admitted) : gate.readOnly = false :=
  h.1

theorem admitted_implies_external_authority (gate : MCPWriteAuthority)
    (h : gate.Admitted) : gate.externalActionAllowed = true :=
  h.2.2.2.1

theorem admitted_implies_mcp_write_authority (gate : MCPWriteAuthority)
    (h : gate.Admitted) : gate.mcpWriteToolCallAllowed = true :=
  h.2.2.2.2.1

theorem admitted_implies_exact_repository (gate : MCPWriteAuthority)
    (h : gate.Admitted) : gate.repositoryMatches = true :=
  h.2.2.2.2.2.2.1

theorem admitted_implies_exact_base_sha (gate : MCPWriteAuthority)
    (h : gate.Admitted) : gate.baseShaMatches = true :=
  h.2.2.2.2.2.2.2

structure ExactGitDelegationGate where
  writeAuthority : MCPWriteAuthority
  exactGitDelegationAllowed : Bool
  exactMutationPreconditionPresent : Bool
  deriving DecidableEq, Repr

def ExactGitDelegationGate.Admitted (gate : ExactGitDelegationGate) : Prop :=
  gate.writeAuthority.Admitted ∧
  gate.exactGitDelegationAllowed = true ∧
  gate.exactMutationPreconditionPresent = true

theorem exactDelegation_implies_write_authority (gate : ExactGitDelegationGate)
    (h : gate.Admitted) : gate.writeAuthority.Admitted :=
  h.1

theorem exactDelegation_implies_explicit_delegation (gate : ExactGitDelegationGate)
    (h : gate.Admitted) : gate.exactGitDelegationAllowed = true :=
  h.2.1

theorem exactDelegation_implies_exact_precondition (gate : ExactGitDelegationGate)
    (h : gate.Admitted) : gate.exactMutationPreconditionPresent = true :=
  h.2.2

theorem exactDelegation_implies_not_readOnly (gate : ExactGitDelegationGate)
    (h : gate.Admitted) : gate.writeAuthority.readOnly = false :=
  h.1.1

end KuuOS.GitHubMCPServerBridgeV0_2
