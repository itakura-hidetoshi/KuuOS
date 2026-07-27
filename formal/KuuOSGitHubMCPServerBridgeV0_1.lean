import Mathlib
import KuuOSGitHubMCPServerBridgeV0_2

namespace KuuOS.GitHubMCPServerBridgeV0_1

structure WriteGate where
  readOnly : Bool
  runtimeExecuteExternalActions : Bool
  planExecuteExternalActions : Bool
  externalActionAllowed : Bool
  writeToolCallAllowed : Bool
  operationApproved : Bool
  repositoryMatches : Bool
  baseShaMatches : Bool
  deriving DecidableEq, Repr

def WriteGate.Admitted (gate : WriteGate) : Prop :=
  gate.readOnly = false ∧
  gate.runtimeExecuteExternalActions = true ∧
  gate.planExecuteExternalActions = true ∧
  gate.externalActionAllowed = true ∧
  gate.writeToolCallAllowed = true ∧
  gate.operationApproved = true ∧
  gate.repositoryMatches = true ∧
  gate.baseShaMatches = true

@[simp] theorem readOnly_never_admits (gate : WriteGate)
    (hReadOnly : gate.readOnly = true) : ¬ gate.Admitted := by
  intro h
  have hFalse : gate.readOnly = false := h.1
  simp [hReadOnly] at hFalse

theorem admitted_implies_runtime_gate (gate : WriteGate)
    (h : gate.Admitted) : gate.runtimeExecuteExternalActions = true :=
  h.2.1

theorem admitted_implies_plan_gate (gate : WriteGate)
    (h : gate.Admitted) : gate.planExecuteExternalActions = true :=
  h.2.2.1

theorem admitted_implies_external_authority (gate : WriteGate)
    (h : gate.Admitted) : gate.externalActionAllowed = true :=
  h.2.2.2.1

theorem admitted_implies_write_authority (gate : WriteGate)
    (h : gate.Admitted) : gate.writeToolCallAllowed = true :=
  h.2.2.2.2.1

theorem admitted_implies_operation_approval (gate : WriteGate)
    (h : gate.Admitted) : gate.operationApproved = true :=
  h.2.2.2.2.2.1

theorem admitted_implies_exact_repository (gate : WriteGate)
    (h : gate.Admitted) : gate.repositoryMatches = true :=
  h.2.2.2.2.2.2.1

theorem admitted_implies_exact_base_sha (gate : WriteGate)
    (h : gate.Admitted) : gate.baseShaMatches = true :=
  h.2.2.2.2.2.2.2

theorem admitted_implies_all_authority_and_scope (gate : WriteGate)
    (h : gate.Admitted) :
    gate.readOnly = false ∧
    gate.runtimeExecuteExternalActions = true ∧
    gate.planExecuteExternalActions = true ∧
    gate.externalActionAllowed = true ∧
    gate.writeToolCallAllowed = true ∧
    gate.operationApproved = true ∧
    gate.repositoryMatches = true ∧
    gate.baseShaMatches = true :=
  h

end KuuOS.GitHubMCPServerBridgeV0_1
