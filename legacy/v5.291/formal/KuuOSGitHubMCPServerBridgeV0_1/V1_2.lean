import KuuOSGitHubMCPServerBridgeV0_1.V1_1

namespace KuuOS.GitHubMCPServerBridgeV1_2

structure PublicPollWakeupGate where
  sourceRepositoryPublic : Bool
  workflowExact : Bool
  canonicalBaseExact : Bool
  sameRepositoryHead : Bool
  workflowCompleted : Bool
  exactJobTerminal : Bool
  exactRequiredStepTerminal : Bool
  pollSignalUsedAsSuccessEvidence : Bool
  selfDispatchWithinKuuOS : Bool
  v11FreshMcpReentryRequired : Bool
  mergeAuthorityGranted : Bool
  writeAuthorityGranted : Bool
  deriving DecidableEq, Repr

def PublicPollWakeupGate.SafeWakeup (gate : PublicPollWakeupGate) : Prop :=
  gate.sourceRepositoryPublic = true ∧
  gate.workflowExact = true ∧
  gate.canonicalBaseExact = true ∧
  gate.sameRepositoryHead = true ∧
  gate.workflowCompleted = true ∧
  gate.exactJobTerminal = true ∧
  gate.exactRequiredStepTerminal = true ∧
  gate.pollSignalUsedAsSuccessEvidence = false ∧
  gate.selfDispatchWithinKuuOS = true ∧
  gate.v11FreshMcpReentryRequired = true ∧
  gate.mergeAuthorityGranted = false ∧
  gate.writeAuthorityGranted = false

theorem safe_wakeup_preserves_reentry_authority_boundary
    (gate : PublicPollWakeupGate) (h : gate.SafeWakeup) :
    gate.pollSignalUsedAsSuccessEvidence = false ∧
    gate.v11FreshMcpReentryRequired = true ∧
    gate.mergeAuthorityGranted = false ∧
    gate.writeAuthorityGranted = false := by
  rcases h with ⟨_, _, _, _, _, _, _, hSignal, _, hFresh, hMerge, hWrite⟩
  exact ⟨hSignal, hFresh, hMerge, hWrite⟩

@[simp] theorem wrong_canonical_base_never_safe
    (gate : PublicPollWakeupGate) (hWrong : gate.canonicalBaseExact = false) :
    ¬ gate.SafeWakeup := by
  simp [PublicPollWakeupGate.SafeWakeup, hWrong]

@[simp] theorem fork_head_never_safe
    (gate : PublicPollWakeupGate) (hFork : gate.sameRepositoryHead = false) :
    ¬ gate.SafeWakeup := by
  simp [PublicPollWakeupGate.SafeWakeup, hFork]

@[simp] theorem pending_workflow_never_safe
    (gate : PublicPollWakeupGate) (hPending : gate.workflowCompleted = false) :
    ¬ gate.SafeWakeup := by
  simp [PublicPollWakeupGate.SafeWakeup, hPending]

@[simp] theorem missing_required_step_never_safe
    (gate : PublicPollWakeupGate) (hMissing : gate.exactRequiredStepTerminal = false) :
    ¬ gate.SafeWakeup := by
  simp [PublicPollWakeupGate.SafeWakeup, hMissing]

@[simp] theorem poll_signal_as_success_evidence_never_safe
    (gate : PublicPollWakeupGate)
    (hAuthority : gate.pollSignalUsedAsSuccessEvidence = true) :
    ¬ gate.SafeWakeup := by
  simp [PublicPollWakeupGate.SafeWakeup, hAuthority]

@[simp] theorem bypassing_v11_fresh_mcp_never_safe
    (gate : PublicPollWakeupGate)
    (hBypass : gate.v11FreshMcpReentryRequired = false) :
    ¬ gate.SafeWakeup := by
  simp [PublicPollWakeupGate.SafeWakeup, hBypass]

@[simp] theorem merge_authority_never_follows_from_poll_wakeup
    (gate : PublicPollWakeupGate) (hMerge : gate.mergeAuthorityGranted = true) :
    ¬ gate.SafeWakeup := by
  simp [PublicPollWakeupGate.SafeWakeup, hMerge]

@[simp] theorem write_authority_never_follows_from_poll_wakeup
    (gate : PublicPollWakeupGate) (hWrite : gate.writeAuthorityGranted = true) :
    ¬ gate.SafeWakeup := by
  simp [PublicPollWakeupGate.SafeWakeup, hWrite]

end KuuOS.GitHubMCPServerBridgeV1_2
