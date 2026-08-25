import KuuOSGitHubMCPServerBridgeV0_1.V1_2

namespace KuuOS.GitHubMCPServerBridgeV1_3

/-- Admission gate for a CI-completion signal that has been persisted in a
GitHub-backed durable inbox and is later consumed through the MCP path.
The inbox signal remains non-authoritative until a fresh MCP re-observation
verifies the exact CI identity. -/
structure DurableInboxReentryGate where
  eventPersistedDurably : Bool
  pendingUntilAck : Bool
  mcpConsumerObservedPending : Bool
  freshMcpReobservation : Bool
  exactIdentity : Bool
  ackAfterFreshVerification : Bool
  eventUsedAsSuccessEvidence : Bool
  mergeAuthorityGranted : Bool
  writeAuthorityGranted : Bool
  deriving DecidableEq, Repr

def DurableInboxReentryGate.Admitted (gate : DurableInboxReentryGate) : Prop :=
  gate.eventPersistedDurably = true ∧
  gate.pendingUntilAck = true ∧
  gate.mcpConsumerObservedPending = true ∧
  gate.freshMcpReobservation = true ∧
  gate.exactIdentity = true ∧
  gate.ackAfterFreshVerification = true ∧
  gate.eventUsedAsSuccessEvidence = false ∧
  gate.mergeAuthorityGranted = false ∧
  gate.writeAuthorityGranted = false

theorem admitted_preserves_durable_pending_and_fresh_verification
    (gate : DurableInboxReentryGate) (h : gate.Admitted) :
    gate.eventPersistedDurably = true ∧
    gate.pendingUntilAck = true ∧
    gate.mcpConsumerObservedPending = true ∧
    gate.freshMcpReobservation = true ∧
    gate.exactIdentity = true ∧
    gate.ackAfterFreshVerification = true := by
  rcases h with ⟨hPersisted, hPending, hObserved, hFresh, hIdentity, hAck, _, _, _⟩
  exact ⟨hPersisted, hPending, hObserved, hFresh, hIdentity, hAck⟩

theorem admitted_preserves_non_authority_boundary
    (gate : DurableInboxReentryGate) (h : gate.Admitted) :
    gate.eventUsedAsSuccessEvidence = false ∧
    gate.mergeAuthorityGranted = false ∧
    gate.writeAuthorityGranted = false := by
  rcases h with ⟨_, _, _, _, _, _, hSignal, hMerge, hWrite⟩
  exact ⟨hSignal, hMerge, hWrite⟩

@[simp] theorem non_durable_signal_never_admits
    (gate : DurableInboxReentryGate)
    (hEphemeral : gate.eventPersistedDurably = false) :
    ¬ gate.Admitted := by
  simp [DurableInboxReentryGate.Admitted, hEphemeral]

@[simp] theorem consumed_without_pending_receipt_never_admits
    (gate : DurableInboxReentryGate)
    (hNotPending : gate.pendingUntilAck = false) :
    ¬ gate.Admitted := by
  simp [DurableInboxReentryGate.Admitted, hNotPending]

@[simp] theorem unobserved_pending_issue_never_admits
    (gate : DurableInboxReentryGate)
    (hUnobserved : gate.mcpConsumerObservedPending = false) :
    ¬ gate.Admitted := by
  simp [DurableInboxReentryGate.Admitted, hUnobserved]

@[simp] theorem ack_before_fresh_mcp_verification_never_admits
    (gate : DurableInboxReentryGate)
    (hNoFresh : gate.freshMcpReobservation = false) :
    ¬ gate.Admitted := by
  simp [DurableInboxReentryGate.Admitted, hNoFresh]

@[simp] theorem wrong_identity_never_admits
    (gate : DurableInboxReentryGate)
    (hWrong : gate.exactIdentity = false) :
    ¬ gate.Admitted := by
  simp [DurableInboxReentryGate.Admitted, hWrong]

@[simp] theorem ack_without_verified_predecessor_never_admits
    (gate : DurableInboxReentryGate)
    (hAckEarly : gate.ackAfterFreshVerification = false) :
    ¬ gate.Admitted := by
  simp [DurableInboxReentryGate.Admitted, hAckEarly]

@[simp] theorem durable_signal_as_success_evidence_never_admits
    (gate : DurableInboxReentryGate)
    (hAuthority : gate.eventUsedAsSuccessEvidence = true) :
    ¬ gate.Admitted := by
  simp [DurableInboxReentryGate.Admitted, hAuthority]

@[simp] theorem merge_authority_never_follows_from_durable_reentry
    (gate : DurableInboxReentryGate)
    (hMerge : gate.mergeAuthorityGranted = true) :
    ¬ gate.Admitted := by
  simp [DurableInboxReentryGate.Admitted, hMerge]

@[simp] theorem write_authority_never_follows_from_durable_reentry
    (gate : DurableInboxReentryGate)
    (hWrite : gate.writeAuthorityGranted = true) :
    ¬ gate.Admitted := by
  simp [DurableInboxReentryGate.Admitted, hWrite]

end KuuOS.GitHubMCPServerBridgeV1_3
