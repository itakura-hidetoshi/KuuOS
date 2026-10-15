import KuuOSGitHubMCPServerBridgeV0_1.V0_4

namespace KuuOS.GitHubMCPServerBridgeV0_5

structure WorkflowDispatchGate where
  writeAuthority : KuuOS.GitHubMCPServerBridgeV0_2.MCPWriteAuthority
  explicitConfirmation : Bool
  triggerToolWrite : Bool
  listToolReadOnly : Bool
  exactWorkflow : Bool
  exactRef : Bool
  expectedHeadShaMatches : Bool
  nonceBound : Bool
  dispatchAccepted : Bool
  newRunObserved : Bool
  runEventMatches : Bool
  runRefMatches : Bool
  runNonceMatches : Bool
  runHeadShaMatches : Bool
  mismatchCancellationUsed : Bool
  deriving DecidableEq, Repr

def WorkflowDispatchGate.Admitted (gate : WorkflowDispatchGate) : Prop :=
  gate.writeAuthority.Admitted ∧
  gate.explicitConfirmation = true ∧
  gate.triggerToolWrite = true ∧
  gate.listToolReadOnly = true ∧
  gate.exactWorkflow = true ∧
  gate.exactRef = true ∧
  gate.expectedHeadShaMatches = true ∧
  gate.nonceBound = true ∧
  gate.dispatchAccepted = true ∧
  gate.newRunObserved = true ∧
  gate.runEventMatches = true ∧
  gate.runRefMatches = true ∧
  gate.runNonceMatches = true ∧
  gate.runHeadShaMatches = true ∧
  gate.mismatchCancellationUsed = false

theorem admitted_implies_write_authority
    (gate : WorkflowDispatchGate)
    (h : gate.Admitted) : gate.writeAuthority.Admitted := by
  rcases h with ⟨hWrite, _, _, _, _, _, _, _, _, _, _, _, _, _, _⟩
  exact hWrite

theorem admitted_implies_explicit_confirmation
    (gate : WorkflowDispatchGate)
    (h : gate.Admitted) : gate.explicitConfirmation = true := by
  rcases h with ⟨_, hConfirmation, _, _, _, _, _, _, _, _, _, _, _, _, _⟩
  exact hConfirmation

theorem admitted_implies_exact_expected_head
    (gate : WorkflowDispatchGate)
    (h : gate.Admitted) : gate.expectedHeadShaMatches = true := by
  rcases h with ⟨_, _, _, _, _, _, hExpected, _, _, _, _, _, _, _, _⟩
  exact hExpected

theorem admitted_implies_nonce_binding
    (gate : WorkflowDispatchGate)
    (h : gate.Admitted) : gate.nonceBound = true := by
  rcases h with ⟨_, _, _, _, _, _, _, hNonce, _, _, _, _, _, _, _⟩
  exact hNonce

theorem admitted_implies_dispatch_accepted
    (gate : WorkflowDispatchGate)
    (h : gate.Admitted) : gate.dispatchAccepted = true := by
  rcases h with ⟨_, _, _, _, _, _, _, _, hAccepted, _, _, _, _, _, _⟩
  exact hAccepted

theorem admitted_implies_new_run_observed
    (gate : WorkflowDispatchGate)
    (h : gate.Admitted) : gate.newRunObserved = true := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, hObserved, _, _, _, _, _⟩
  exact hObserved

theorem admitted_implies_exact_run_head
    (gate : WorkflowDispatchGate)
    (h : gate.Admitted) : gate.runHeadShaMatches = true := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, hHead, _⟩
  exact hHead

theorem admitted_excludes_mismatch_cancellation
    (gate : WorkflowDispatchGate)
    (h : gate.Admitted) : gate.mismatchCancellationUsed = false := by
  rcases h with ⟨_, _, _, _, _, _, _, _, _, _, _, _, _, _, hNoCancel⟩
  exact hNoCancel

@[simp] theorem mismatch_cancellation_never_admits
    (gate : WorkflowDispatchGate)
    (hCancelled : gate.mismatchCancellationUsed = true) : ¬ gate.Admitted := by
  intro h
  have hNoCancel : gate.mismatchCancellationUsed = false :=
    admitted_excludes_mismatch_cancellation gate h
  simp [hCancelled] at hNoCancel

@[simp] theorem unobserved_run_never_admits
    (gate : WorkflowDispatchGate)
    (hUnobserved : gate.newRunObserved = false) : ¬ gate.Admitted := by
  intro h
  have hObserved : gate.newRunObserved = true :=
    admitted_implies_new_run_observed gate h
  simp [hUnobserved] at hObserved

@[simp] theorem wrong_head_run_never_admits
    (gate : WorkflowDispatchGate)
    (hMismatch : gate.runHeadShaMatches = false) : ¬ gate.Admitted := by
  intro h
  have hMatched : gate.runHeadShaMatches = true :=
    admitted_implies_exact_run_head gate h
  simp [hMismatch] at hMatched

theorem admitted_implies_complete_workflow_dispatch_closeout
    (gate : WorkflowDispatchGate)
    (h : gate.Admitted) :
    gate.writeAuthority.Admitted ∧
    gate.explicitConfirmation = true ∧
    gate.triggerToolWrite = true ∧
    gate.listToolReadOnly = true ∧
    gate.exactWorkflow = true ∧
    gate.exactRef = true ∧
    gate.expectedHeadShaMatches = true ∧
    gate.nonceBound = true ∧
    gate.dispatchAccepted = true ∧
    gate.newRunObserved = true ∧
    gate.runEventMatches = true ∧
    gate.runRefMatches = true ∧
    gate.runNonceMatches = true ∧
    gate.runHeadShaMatches = true ∧
    gate.mismatchCancellationUsed = false :=
  h

end KuuOS.GitHubMCPServerBridgeV0_5
